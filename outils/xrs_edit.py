"""Modifications ciblées d'un schéma WinRelais (.xrs) en préservant l'encodage.

Principe : le fichier est manipulé ligne par ligne ; seules les lignes modifiées changent
(mêmes séparateurs « · », même « · » final, même encodage, mêmes fins de ligne).
Chaque opération vérifie l'état attendu et lève une erreur sinon : un script de correction
appliqué sur un fichier qui a évolué s'arrête au lieu d'écrire n'importe quoi.

WinRelais doit être fermé pendant l'écriture. Format : voir ../FORMAT_XRS.md.
"""
SEP = "·"


class XrsError(Exception):
    pass


class XrsDoc:
    def __init__(self, path):
        self.path = path
        raw = open(path, "rb").read()
        self.bom = raw.startswith(b"\xef\xbb\xbf")
        body = raw[3:] if self.bom else raw
        try:            # UTF-8 (avec ou sans BOM : les .xsy CUSTOM n'en ont pas) sinon Windows-1252
            text, self.encoding = body.decode("utf-8"), "utf-8"
        except UnicodeDecodeError:
            text, self.encoding = body.decode("cp1252"), "cp1252"
        self.eol = "\r\n" if "\r\n" in text else "\n"
        self.lines = text.split(self.eol)
        self.log = []

    # ------------------------------------------------------------------ utilitaires
    def save(self, path=None):
        data = self.eol.join(self.lines).encode(self.encoding)
        with open(path or self.path, "wb") as f:
            if self.bom:
                f.write(b"\xef\xbb\xbf")
            f.write(data)

    def _set(self, n, new_line, why):
        old = self.lines[n]
        if old != new_line:
            self.lines[n] = new_line
            self.log.append((n + 1, why, old, new_line))

    def section_range(self, header):
        """(début, fin) des lignes de données d'une section globale, ex. '¤#FilBus¤'."""
        start = self.lines.index(header) + 1
        end = start
        while end < len(self.lines) and not self.lines[end].startswith("¤#"):
            end += 1
        return start, end

    def symbol_range(self, name):
        """Lignes [début, fin) du bloc ¤#Symbole·n¤ dont le champ 1 (repère) vaut name."""
        found = []
        for i, l in enumerate(self.lines):
            if l.startswith("¤#Symbole·") and self.lines[i + 1] == "¤#Autre¤":
                rep = self.lines[i + 4].split(SEP)[0]
                if rep == name:
                    j = i
                    while self.lines[j] != "¤#FIN¤":
                        j += 1
                    found.append((i, j))
        if len(found) != 1:
            raise XrsError(f"symbole {name} trouvé {len(found)} fois")
        return found[0]

    # ------------------------------------------------------------------ opérations
    @staticmethod
    def shift_block(block, dx, dy, name="?"):
        """Décale toutes les coordonnées d'un bloc symbole (lignes entre ¤#Autre¤ et ¤#FIN¤)."""
        # index des champs X (Y = X+1) par section
        coord_fields = {"Contour": (0, 2), "Arc": (0,), "MDessin": (1,), "Broche": (1, 3, 5),
                        "RefCroise": (5,), "VueArmoire": (1,)}
        no_coord = {"RefConstructeur", "LienInternet", "VersionSymbole", "AuteurSymbole", "WinEcad",
                    "RefBaseData"}
        out, sec, k = [], None, 0
        for l in block:
            if l.startswith("¤#"):
                sec, k = l.strip("¤#"), 0
                out.append(l)
                continue
            f = l.split(SEP)
            xs = ()
            if sec == "Autre":
                xs = (0,) if k == 0 else () if k == 1 else (1,)
            elif sec == "ZoneDessin":
                xs = tuple(6 + 2 * p for p in range(int(f[3])))
            elif sec in ("RefCroise", "VueArmoire"):
                xs = coord_fields[sec] if k == 0 else ()
            elif sec in coord_fields:
                xs = coord_fields[sec]
            elif sec not in no_coord:
                raise XrsError(f"{name} : section {sec} inconnue, déplacement refusé")
            for a in xs:
                if f[a] == "" and f[a + 1] == "":
                    continue
                f[a] = str(int(f[a]) + dx)
                f[a + 1] = str(int(f[a + 1]) + dy)
            out.append(SEP.join(f))
            k += 1
        return out

    def move_symbol(self, name, dx, dy, expect_origin):
        """Déplace un symbole et tout son dessin (coordonnées absolues)."""
        i, j = self.symbol_range(name)
        o = self.lines[i + 2].split(SEP)
        if (int(o[0]), int(o[1])) != tuple(expect_origin):
            raise XrsError(f"{name} : origine {o[0]},{o[1]} au lieu de {expect_origin}")
        new = self.shift_block(self.lines[i + 1:j], dx, dy, name)
        for n, l in enumerate(new, start=i + 1):
            self._set(n, l, f"déplacement {name} ({dx:+},{dy:+})")

    # --- symboles : champs, repère, référence
    def rename_symbol(self, old, new):
        i, _ = self.symbol_range(old)
        f = self.lines[i + 4].split(SEP)
        f[0] = new
        self._set(i + 4, SEP.join(f), f"repère {old} -> {new}")

    def set_champ(self, name, k, text, visible=None):
        """Champ k (1..8) du symbole ; champ 1 = repère."""
        i, _ = self.symbol_range(name)
        n = i + 3 + k
        f = self.lines[n].split(SEP)
        f[0] = text
        if visible is not None:
            f[3] = "1" if visible else "0"
        self._set(n, SEP.join(f), f"{name} champ {k}")

    def move_champ(self, name, k, x, y):
        i, _ = self.symbol_range(name)
        n = i + 3 + k
        f = self.lines[n].split(SEP)
        f[1], f[2] = str(x), str(y)
        self._set(n, SEP.join(f), f"{name} champ {k} déplacé")

    def set_prefix(self, name, prefix):
        i, _ = self.symbol_range(name)
        f = self.lines[i + 3].split(SEP)
        f[4] = prefix
        self._set(i + 3, SEP.join(f), f"{name} préfixe -> {prefix}")

    def set_refconstructeur(self, name, nom, ref1, ref2):
        i, j = self.symbol_range(name)
        n = self.lines.index("¤#RefConstructeur¤", i, j) + 1
        f = self.lines[n].split(SEP)
        f[0], f[1], f[2] = nom, ref1, ref2
        self._set(n, SEP.join(f), f"{name} référence constructeur")

    # --- symboles : création
    def _symbols_end(self):
        last = max(i for i, l in enumerate(self.lines) if l.startswith("¤#Symbole·"))
        j = last
        while self.lines[j] != "¤#FIN¤":
            j += 1
        return j + 1

    def _append_symbol(self, block, name, why):
        n_idx = self.lines.index("¤#NombreSymbole¤") + 1
        count = int(self.lines[n_idx].split(SEP)[0])
        pos = self._symbols_end()
        new = [f"¤#Symbole·{count}¤"] + block + ["¤#FIN¤"]
        self.lines[pos:pos] = new
        self.log.append((pos + 1, why, "", f"{len(new)} lignes (¤#Symbole·{count}¤ {name})"))
        self._set(n_idx, f"{count + 1}{SEP}", "nombre de symboles")

    def copy_symbol(self, src, new_name, dx, dy, folio=None):
        i, j = self.symbol_range(src)
        block = self.shift_block(self.lines[i + 1:j], dx, dy, src)
        f = block[3].split(SEP)            # champ 1
        f[0] = new_name
        block[3] = SEP.join(f)
        if folio is not None:
            g = block[2].split(SEP)
            g[8] = str(folio)
            block[2] = SEP.join(g)
        self._append_symbol(block, new_name, f"nouveau symbole {new_name} (copie de {src})")

    def insert_xsy(self, xsy_path, name, folio, x, y, auteur, champs=None, ref=None, prefix=None):
        """Insère un symbole de librairie WinSymbole (.xsy), origine en (x, y).

        champs = {k: (texte, visible, dx, dy)} (k = 2..8, position relative à l'origine) ;
        ref = (nom, ref1, ref2) ; à renseigner ici car le repère peut déjà exister (esclaves).
        """
        lib = XrsDoc(xsy_path).lines
        a = lib.index("¤#Autre¤")
        z = len(lib) - 1 - lib[::-1].index("¤#FIN¤")
        raw, skip = [], False
        for l in lib[a:z]:
            if l.startswith("¤#"):
                skip = l == "¤#RefBaseData¤"
            if not skip:
                raw.append(l)
        o = raw[1].split(SEP)
        block = self.shift_block(raw, x - int(o[0]), y - int(o[1]), name)
        f = block[3].split(SEP)
        f[0] = name
        block[3] = SEP.join(f)
        g = block[2].split(SEP)
        g[8] = str(folio)
        if prefix is not None:
            g[4] = prefix
        block[2] = SEP.join(g)
        for k, (txt, vis, cdx, cdy, *taille) in (champs or {}).items():
            c = block[2 + k].split(SEP)
            c[0], c[1], c[2], c[3] = txt, str(x + cdx), str(y + cdy), "1" if vis else "0"
            if taille:
                c[6] = str(taille[0])
            block[2 + k] = SEP.join(c)
        if ref is not None:
            n = block.index("¤#RefConstructeur¤") + 1
            c = block[n].split(SEP)
            c[0], c[1], c[2] = ref
            block[n] = SEP.join(c)
        block += ["¤#AuteurSymbole¤", auteur]
        self._append_symbol(block, name, f"nouveau symbole {name} ({xsy_path.split(chr(92))[-1]})")

    # --- fils, jonctions, renvois, textes
    def add_wire(self, folio, p1, p2, attrs, why):
        """attrs = champs 5.. d'un fil modèle, ex. '1·40·0·0·Puissance·0·0·0·0·0·'."""
        _, e = self.section_range("¤#FilBus¤")
        line = SEP.join(str(v) for v in (*p1, *p2, folio)) + SEP + attrs
        self.lines.insert(e, line)
        self.log.append((e + 1, why, "", line))

    def wire_attrs(self, folio, p1, p2):
        f = self.lines[self._find_wire(folio, p1, p2)].split(SEP)
        return SEP.join(f[5:])

    def set_wire_attrs(self, folio, p1, p2, attrs, why):
        n = self._find_wire(folio, p1, p2)
        f = self.lines[n].split(SEP)
        self._set(n, SEP.join(f[:5]) + SEP + attrs, why)

    def add_jonction(self, folio, x, y, color, why):
        _, e = self.section_range("¤#Jonction¤")
        line = f"{x}{SEP}{y}{SEP}{folio}{SEP}40{SEP}0{SEP}2{SEP}{color}{SEP}0{SEP}"
        self.lines.insert(e, line)
        self.log.append((e + 1, why, "", line))

    def delete_jonction(self, folio, x, y, why):
        s, e = self.section_range("¤#Jonction¤")
        hits = [n for n in range(s, e) if self.lines[n].split(SEP)[:3] == [str(x), str(y), str(folio)]]
        if len(hits) != 1:
            raise XrsError(f"jonction folio {folio} ({x},{y}) trouvée {len(hits)} fois")
        self.log.append((hits[0] + 1, why, self.lines[hits[0]], "(ligne supprimée)"))
        del self.lines[hits[0]]

    def add_renvoi(self, model_line_match, folioA, folioB, pA, pB, texteA, texteB, why):
        """Ajoute un renvoi en copiant le style d'un renvoi existant (sous-chaîne model_line_match)."""
        s, e = self.section_range("¤#RenvoiF¤")
        model = next(self.lines[n] for n in range(s, e) if model_line_match in self.lines[n])
        f = model.split(SEP)
        f[0:6] = [str(folioA), str(folioB), str(pA[0]), str(pA[1]), str(pB[0]), str(pB[1])]
        f[10], f[11] = texteA, texteB
        line = SEP.join(f)
        self.lines.insert(e, line)
        self.log.append((e + 1, why, "", line))

    def add_texte(self, model_line_match, folio, x, y, texte, why):
        s, e = self.section_range("¤#Texte¤")
        model = next(self.lines[n] for n in range(s, e) if model_line_match in self.lines[n])
        f = model.split(SEP)
        f[0], f[1], f[2], f[4] = str(x), str(y), texte, str(folio)
        line = SEP.join(f)
        self.lines.insert(e, line)
        self.log.append((e + 1, why, "", line))

    # --- folios
    def folio_range(self, k):
        i = self.lines.index(f"¤#Folio·{k}¤")
        j = i + 1
        while not self.lines[j].startswith("¤#Folio·") and self.lines[j] != "¤#NombreSymbole¤":
            j += 1
        return i, j

    def set_folio_nom(self, k, nom):
        i, _ = self.folio_range(k)
        f = self.lines[i + 2].split(SEP)
        f[10] = nom
        self._set(i + 2, SEP.join(f), f"folio idx {k} nom interne")

    def set_cartouche(self, k, cle, valeur):
        i, j = self.folio_range(k)
        hits = []
        for n in range(i, j):
            f = self.lines[n].split(SEP)
            if len(f) > 4 and f[3] == cle and not self.lines[n].startswith("¤"):
                hits.append(n)
        if len(hits) != 1:
            raise XrsError(f"cartouche folio idx {k} clé {cle} trouvée {len(hits)} fois")
        f = self.lines[hits[0]].split(SEP)
        f[2] = valeur
        self._set(hits[0], SEP.join(f), f"folio idx {k} {cle}")

    def replace_cartouche_text(self, old, new):
        for n, l in enumerate(self.lines):
            f = l.split(SEP)
            if len(f) > 4 and old in f[2] and not l.startswith("¤"):
                # uniquement les lignes de cartouche (champ 3 = clé de modèle)
                f[2] = f[2].replace(old, new)
                self._set(n, SEP.join(f), f"cartouche « {old} » -> « {new} »")

    def set_cable_name(self, old, new):
        hits = []
        for n, l in enumerate(self.lines):
            if l.startswith("¤#DefCable·"):
                c = n + 6       # ¤#Autre¤ + 4 lignes de style, puis champ 1
                if self.lines[c].split(SEP)[0] == old:
                    hits.append(c)
        if len(hits) != 1:
            raise XrsError(f"câble {old} trouvé {len(hits)} fois")
        f = self.lines[hits[0]].split(SEP)
        f[0] = new
        self._set(hits[0], SEP.join(f), f"câble {old} -> {new}")

    def pins(self, name):
        i, j = self.symbol_range(name)
        folio = int(self.lines[i + 3].split(SEP)[8])
        out = {}
        start = self.lines.index("¤#Broche¤", i, j) + 1
        n = start
        while not self.lines[n].startswith("¤#"):
            f = self.lines[n].split(SEP)
            out.setdefault(f[0], []).append((int(f[1]), int(f[2])))
            n += 1
        return folio, out

    def _find_wire(self, folio, p1, p2):
        s, e = self.section_range("¤#FilBus¤")
        hits = []
        for n in range(s, e):
            f = self.lines[n].split(SEP)
            if len(f) < 10 or int(f[4]) != folio:
                continue
            a, b = (int(f[0]), int(f[1])), (int(f[2]), int(f[3]))
            if {a, b} == {tuple(p1), tuple(p2)}:
                hits.append(n)
        if len(hits) != 1:
            raise XrsError(f"fil folio idx {folio} {p1}->{p2} trouvé {len(hits)} fois")
        return hits[0]

    def move_wire_end(self, folio, p1, p2, old_end, new_end, why):
        """Déplace une extrémité (old_end) du fil p1-p2."""
        n = self._find_wire(folio, p1, p2)
        f = self.lines[n].split(SEP)
        for a in (0, 2):
            if (int(f[a]), int(f[a + 1])) == tuple(old_end):
                f[a], f[a + 1] = str(new_end[0]), str(new_end[1])
                self._set(n, SEP.join(f), why)
                return
        raise XrsError(f"extrémité {old_end} absente du fil {p1}->{p2}")

    def shift_wire(self, folio, p1, p2, dx, dy, why):
        n = self._find_wire(folio, p1, p2)
        f = self.lines[n].split(SEP)
        for a in (0, 2):
            f[a] = str(int(f[a]) + dx)
            f[a + 1] = str(int(f[a + 1]) + dy)
        self._set(n, SEP.join(f), why)

    def delete_wire(self, folio, p1, p2, why):
        n = self._find_wire(folio, p1, p2)
        self.log.append((n + 1, why, self.lines[n], "(ligne supprimée)"))
        del self.lines[n]

    def move_renvoi_point(self, folioA, folioB, side, old, new, why):
        s, e = self.section_range("¤#RenvoiF¤")
        a = 2 if side == "A" else 4
        hits = []
        for n in range(s, e):
            f = self.lines[n].split(SEP)
            if len(f) > 6 and (int(f[0]), int(f[1])) == (folioA, folioB) and \
                    (int(f[a]), int(f[a + 1])) == tuple(old):
                hits.append(n)
        if len(hits) != 1:
            raise XrsError(f"renvoi {folioA}->{folioB} {side}{old} trouvé {len(hits)} fois")
        f = self.lines[hits[0]].split(SEP)
        f[a], f[a + 1] = str(new[0]), str(new[1])
        self._set(hits[0], SEP.join(f), why)
