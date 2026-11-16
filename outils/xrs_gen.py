"""Générateur de schéma WinRelais (.xrs) à partir d'une description Python.

Principe : on décrit les folios (symboles de librairie posés à des coordonnées, liaisons broche à
broche, renvois), le module écrit un .xrs complet (UTF-8 BOM, CRLF) en reprenant l'en-tête et le
cartouche d'un schéma modèle, puis contrôle le résultat :
  - équipotentielles voulues == équipotentielles relues dans le fichier (ni court-circuit, ni oubli),
  - symboles qui se chevauchent, fil qui traverse un symbole, objet hors cadre,
  - contrôles généraux de xrs_tool.verifier.

Unités : 1/100 mm, grille 400. Format : ../FORMAT_XRS.md.
"""
import os
import re
from collections import defaultdict

from xrs_edit import XrsDoc, SEP
from xrs_tool import split_sections, fields, to_int

LIB = os.environ.get("TTK_LIB") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "librairie")
GRID = 400
DATE = os.environ.get("TTK_DATE") or "28/10/2026"     # date de modification inscrite au cartouche et dans les symboles
ZONE_X = (1300, 29600)          # cadre utile (hors marges)
ZONE_Y = (1300, 19600)          # au-dessus du cartouche
RENVOI_L = 1600                 # emprise flèche + texte d'un renvoi au-delà de son point (mesurée sur WinRelais)
RENVOI_W = 220                  # demi-largeur de cette emprise

# attributs de fil (champs 5.. d'une ligne ¤#FilBus¤), repris du schéma TTK
TYPES = {
    "L": ("1·40·0·0·Puissance·0·0·0·0·0·", 40, 0),
    "N": ("1·40·16757612·0·Neutre Puissance·0·0·0·0·0·", 40, 16757612),
    "PE": ("1·30·0·7·Conducteur terre·500·500·65535·65280·0·", 30, 0),
    "24": ("1·20·11302912·0·Commande 24VDC·0·0·0·0·0·", 20, 11302912),
    "0V": ("1·20·16744448·0·0V·0·0·0·0·0·", 20, 16744448),
    "DC": ("1·20·4227327·0·Autre tension DC·0·0·0·0·0·", 20, 4227327),
    # PROFINET : type « Autre tension DC » affiché en vert, en attendant un type de conducteur dédié dans WinRelais
    # type « Profinet » de Julien (05/11) : rose foncé RGB(199, 21, 133), 10 % plus épais que la puissance (40 -> 44)
    "PN": ("1·44·8721863·0·Profinet·0·0·0·0·0·", 44, 8721863),
    # 02/11 (IEC 60204-1 13.2.4) : puissance en continu (48 V drivers, phases pas-à-pas, résistance de freinage) en noir ;
    # l'orange est réservé aux circuits exceptés (sous tension après QS1 ouvert), il n'y en a pas sur TTK
    "PDC": ("1·30·0·0·Autre tension DC·0·0·0·0·0·", 30, 0),
    # thermocouple type K (IEC 60584-3 : + vert, - blanc), affiché en vert
    "TC": ("1·20·32768·0·Autre tension DC·0·0·0·0·0·", 20, 32768),
}


# largeur des caractères Arial (fraction de la hauteur de police), pour estimer la longueur d'un texte
_AW = dict.fromkeys("ijl.,;:'|! ", 0.278)
_AW.update(dict.fromkeys("ftrI-()[]/", 0.333))
_AW.update(dict.fromkeys("ckszvxyJ*", 0.5))
_AW.update(dict.fromkeys("mMW", 0.833))
_AW.update(dict.fromkeys("wCDGHNOQRU", 0.75))
_AW.update(dict.fromkeys("ABEKPSVXYZ&", 0.667))
_AW.update(dict.fromkeys("FTL", 0.611))


def largeur(txt, size):
    """Largeur estimée d'un texte (02/11 : chasse Arial x 0,85, mesurée sur des copies d'écran de Julien).
    Sert aux contrôles de chevauchement ; la mise en page garde l'estimation de 0,55 par caractère."""
    return int(sum(_AW.get(c, 0.556) for c in txt) * size * 0.85)


class GenError(Exception):
    pass


def zone(x, y):
    """Case du cadre repère : colonnes A..N et lignes 1..9 de 20 mm à partir de 13 mm."""
    col = min(max((x - 1300) // 2000, 0), 13)
    row = min(max((y - 1300) // 2000 + 1, 1), 9)
    return f"{chr(65 + col)}{row}"


class Placed:
    """Symbole posé : broches absolues par nom (liste si le nom est répété)."""

    def __init__(self, gen, folio, rep, block, bbox):
        self.gen, self.folio, self.rep, self.block, self.bbox = gen, folio, rep, block, bbox
        self.pins = defaultdict(list)
        sec = None
        for l in block:
            if l.startswith("\u00a4#"):
                sec = l
                continue
            if sec == "\u00a4#Broche\u00a4":
                f = l.split(SEP)
                self.pins[f[0]].append((int(f[1]), int(f[2])))

    def __getitem__(self, key):
        name, k = (key, 0) if isinstance(key, str) else key
        if name not in self.pins:
            raise GenError(f"{self.rep} : broche {name} inexistante ({list(self.pins)})")
        return Pin(self, name, self.pins[name][k])


class Pin:
    def __init__(self, sym, name, xy):
        self.sym, self.name, self.xy = sym, name, xy
        self.x, self.y = xy

    @property
    def key(self):
        return f"{self.sym.rep}:{self.name}"


class Gen:
    def __init__(self, template):
        t = XrsDoc(template)
        L = t.lines
        self.header = L[:L.index("\u00a4#NombreFolio\u00a4")]
        i = L.index("\u00a4#Folio\u00b71\u00a4")
        j = L.index("\u00a4#Folio\u00b72\u00a4")
        self.folio_tpl = L[i + 1:j]
        self.text_tpl = None
        self.folios = []            # (numero, titre, description)
        self.symbols = []           # Placed
        self.wires = []             # (folio, x1, y1, x2, y2, type)
        self.jonctions = []
        self.numeros = []           # (folio, x, y, texte, angle) : numéros / noms de fil (¤#Numero)
        self.renvois = []
        self.textes = []
        self.dessins = []
        self.tableaux_bruts = []  # (index folio, lignes) : tableaux WinRelais recopiés tels quels (un bloc ¤#Tableau·n¤ chacun)
        self.logos = []           # (index folio, x, y, largeur, hauteur, chemin absolu, ratio de l'image x 1000)
        self.cables = []
        self.cable_nums = {}      # index du câble -> numéros des brins (câble sur 2 folios)
        self.cable_type = {}      # index du câble -> type WinRelais (0 simple, 3 blindé ellipse + trait)
        self.nets = {}              # union-find des équipotentielles voulues
        self.net_names = {}
        self.tee_issues = []
        self._xsy_cache = {}

    # ------------------------------------------------------------------ folios
    def folio(self, numero, titre, description):
        self.folios.append((numero, titre, description))
        return len(self.folios) - 1

    def num(self, k):
        return self.folios[k][0]

    # ------------------------------------------------------------------ symboles
    def _load_xsy(self, path):
        if path not in self._xsy_cache:
            path = path.replace("\\", "/")
            full = path if os.path.isabs(path) else os.path.join(LIB, path)
            lines = XrsDoc(full).lines
            a = lines.index("\u00a4#Autre\u00a4")
            z = len(lines) - 1 - lines[::-1].index("\u00a4#FIN\u00a4")
            raw, skip = [], False
            for l in lines[a:z]:
                if l.startswith("\u00a4#"):
                    skip = l in ("\u00a4#RefBaseData\u00a4", "\u00a4#AuteurSymbole\u00a4")
                if not skip:
                    raw.append(l)
            self._xsy_cache[path] = raw
        return list(self._xsy_cache[path])

    def place(self, xsy, rep, folio, x, y, champs=None, ref=None, prefix=None, compact=False,
              rep_size=None, wrap=28, fpos=None, loc=None, shown=(2, 3, 4), noms=None):
        """Pose un symbole de librairie, origine en (x, y).

        champs = {2: désignation, 3: fabricant + réf., 4: caractéristiques} (données nomenclature,
        toujours écrites) ; shown = champs affichés ; compact = n'afficher que le repère.
        Les textes longs sont coupés (wrap caractères) dans les champs libres 5 à 8.
        fpos = position du repère relative à l'origine (sinon celle de la librairie).
        ref = (fabricant, réf1, réf2), () pour effacer (esclave). loc = localisation (A1, P1, M).
        noms = afficher les noms de broches (True / False), sinon valeur de la librairie.
        """
        if x % 200 or y % 200:
            raise GenError(f"{rep} : origine hors grille ({x},{y})")
        raw = self._load_xsy(xsy)
        o = raw[1].split(SEP)
        block = XrsDoc.shift_block(raw, x - int(o[0]), y - int(o[1]), rep)
        info = block[2].split(SEP)
        info[8] = str(folio)
        if prefix:
            info[4] = prefix
        if noms is not None:
            info[5] = "1" if noms else "0"
        block[2] = SEP.join(info)
        ch = [block[3 + k].split(SEP) for k in range(8)]       # ch[0] = champ 1
        ax, ay = (x + fpos[0], y + fpos[1]) if fpos else (int(ch[0][1]), int(ch[0][2]))
        size1 = rep_size or int(ch[0][6] or 300)
        champs = dict(champs or {})
        rows = [(0, rep, size1)]
        free = [4, 5, 6, 7]                                       # index des champs 5 à 8
        for k in (2, 3, 4):
            txt = champs.get(k, "")
            parts = _wrap(txt, wrap) if txt else [""]
            ch[k - 1][0] = parts[0]
            if compact or k not in shown or not txt:
                continue
            rows.append((k - 1, parts[0], 200))
            for extra in parts[1:]:
                if not free:
                    break
                j = free.pop(0)
                ch[j][0] = extra
                rows.append((j, extra, 200))
        ch[0][0] = rep
        for c in ch:
            c[3] = "0"
        yy = ay
        for idx, txt, sz in rows:
            c = ch[idx]
            c[1], c[2], c[3], c[6], c[7] = str(ax), str(yy), "1", str(sz), "0"
            if idx:
                c[4] = "0"
            yy += sz + 100 if idx == 0 else 300
        for k in range(8):
            block[3 + k] = SEP.join(ch[k])
        if ref is not None:
            n = block.index("¤#RefConstructeur¤") + 1
            c = block[n].split(SEP)
            c[0], c[1], c[2] = (tuple(ref) + ("", "", ""))[:3]
            block[n] = SEP.join(c)
        if loc:
            n = block.index("¤#VueArmoire¤") + 1
            c = block[n].split(SEP)
            c[0] = loc
            block[n] = SEP.join(c)
        block += ["¤#AuteurSymbole¤", f"Julien·Ingerea·{DATE}·1.0·0·"]
        p = Placed(self, folio, rep, block, self._bbox(block))
        p.texts = []
        for c in ch:
            if c[3] == "1" and c[0]:
                sz = int(c[6] or 300)
                w = int(len(c[0]) * sz * 0.55)
                tx = int(c[1]) - (w // 2 if c[4] == "6" else 0)
                p.texts.append((c[0], (tx, int(c[2]), tx + w, int(c[2]) + sz)))
        self.symbols.append(p)
        allpins = [xy for pins in p.pins.values() for xy in pins]
        for xy in allpins:
            self._node(("P", folio) + xy)
        if block[2].split(SEP)[11] == "1":      # borne : ses broches sont au même potentiel
            for xy in allpins[1:]:
                self._union(("P", folio) + allpins[0], ("P", folio) + xy)
        return p

    @staticmethod
    def _bbox(block):
        xs, ys, sec = [], [], None
        for l in block:
            if l.startswith("\u00a4#"):
                sec = l
                continue
            f = l.split(SEP)
            if sec == "\u00a4#Contour\u00a4":
                xs += [int(f[0]), int(f[2])]
                ys += [int(f[1]), int(f[3])]
            elif sec == "\u00a4#Arc\u00a4" and len(f) > 2 and f[2]:
                r = int(f[2])
                xs += [int(f[0]) - r, int(f[0]) + r]
                ys += [int(f[1]) - r, int(f[1]) + r]
            elif sec == "\u00a4#ZoneDessin\u00a4":
                for p in range(int(f[3])):
                    xs.append(int(f[6 + 2 * p]))
                    ys.append(int(f[7 + 2 * p]))
        return (min(xs), min(ys), max(xs), max(ys)) if xs else None

    # ------------------------------------------------------------------ équipotentielles voulues
    def _node(self, n):
        self.nets.setdefault(n, n)
        return n

    def _find(self, n):
        self._node(n)
        while self.nets[n] != n:
            self.nets[n] = self.nets[self.nets[n]]
            n = self.nets[n]
        return n

    def _union(self, a, b):
        ra, rb = self._find(a), self._find(b)
        if ra != rb:
            self.nets[ra] = rb

    # ------------------------------------------------------------------ fils
    @staticmethod
    def _xy(p):
        return p.xy if isinstance(p, Pin) else tuple(p)

    def wire(self, folio, points, t, name=None):
        """Polyligne orthogonale (points = Pin ou (x, y)). Retourne le dernier point."""
        pts = [self._xy(p) for p in points]
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            if (x1, y1) == (x2, y2):
                continue
            if x1 != x2 and y1 != y2:
                raise GenError(f"folio {self.num(folio)} : segment oblique {(x1, y1)}->{(x2, y2)}")
            for v in (x1, y1, x2, y2):
                if v % 100:
                    raise GenError(f"folio {self.num(folio)} : coordonnée hors pas {(x1, y1)}->{(x2, y2)}")
            self.wires.append([folio, x1, y1, x2, y2, t])
            self._union(("P", folio, x1, y1), ("P", folio, x2, y2))
        if name:
            self.net_names[self._find(("P", folio) + pts[0])] = name
        return pts[-1]

    def link(self, folio, a, b, t, via=None, horiz_first=False):
        """Relie a à b : vertical depuis a jusqu'à via (y), horizontal, vertical vers b.

        Sans via : vertical puis horizontal (ou l'inverse si horiz_first).
        """
        (xa, ya), (xb, yb) = self._xy(a), self._xy(b)
        if via is not None:
            pts = [(xa, ya), (xa, via), (xb, via), (xb, yb)]
        elif xa == xb or ya == yb:
            pts = [(xa, ya), (xb, yb)]
        elif horiz_first:
            pts = [(xa, ya), (xb, ya), (xb, yb)]
        else:
            pts = [(xa, ya), (xa, yb), (xb, yb)]
        return self.wire(folio, pts, t)

    def tap(self, folio, pin, bus_y, t):
        """Descente verticale d'une broche sur une barre horizontale y = bus_y."""
        return self.wire(folio, [pin, (self._xy(pin)[0], bus_y)], t)

    # ------------------------------------------------------------------ renvois, textes, dessins
    def renvoi(self, fa, pa, fb, pb, t, vertical=True):
        pa, pb = self._xy(pa), self._xy(pb)
        self.renvois.append((fa, pa, fb, pb, t, vertical))
        self._union(("P", fa) + pa, ("P", fb) + pb)

    def _wire_dir(self, folio, pt):
        """Direction (dx, dy) du fil qui part de pt (premier trouvé)."""
        for w in self.wires:
            if w[0] != folio:
                continue
            if (w[1], w[2]) == pt:
                return (w[3] - w[1], w[4] - w[2])
            if (w[3], w[4]) == pt:
                return (w[1] - w[3], w[2] - w[4])
        return None

    def _wire_dirs(self, folio, pt):
        """Toutes les directions de fil qui partent de pt."""
        out = set()
        for w in self.wires:
            if w[0] != folio:
                continue
            for a, b in ((w[1:3], w[3:5]), (w[3:5], w[1:3])):
                if tuple(a) == pt:
                    out.add(((b[0] > a[0]) - (b[0] < a[0]), (b[1] > a[1]) - (b[1] < a[1])))
        return out

    def renvoi_code(self, folio, pt, depart=True):
        """Code WinRelais (mesuré sur les 36 exemples livrés) :
        0 = fil en dessous (flèche au-dessus), 1 = fil au-dessus (flèche en dessous) ;
        horizontal, côté départ (A) : 2 = fil à gauche, 3 = fil à droite ;
        côté arrivée (B) : 2 = fil à droite, 3 = fil à gauche (la flèche pointe toujours à droite)."""
        d = self._wire_dir(folio, pt)
        if not d:
            return 2
        if d[0]:
            return 2 if (d[0] < 0) == depart else 3
        return 0 if d[1] > 0 else 1

    def renvoi_box(self, folio, pt):
        """Emprise de la flèche et du texte, du côté opposé au fil."""
        x, y = pt
        d = self._wire_dir(folio, pt) or (0, 1)
        L, H = RENVOI_L, RENVOI_W
        if d[0] > 0:
            return (x - L, y - H, x, y + H)
        if d[0] < 0:
            return (x, y - H, x + L, y + H)
        if d[1] > 0:
            return (x - H, y - L, x + H, y)
        return (x - H, y, x + H, y + L)

    def texte(self, folio, x, y, txt, size=300, color=0, bold=0):
        self.textes.append((folio, x, y, txt, size, color, bold))

    def ligne(self, folio, x1, y1, x2, y2, color=0, width=20, dashed=False):
        self.dessins.append((folio, x1, y1, x2, y2, 2, color, width, 2 if dashed else 0))

    def cadre(self, folio, x1, y1, x2, y2, color=0, width=20, dashed=False):
        self.dessins.append((folio, x1, y1, x2, y2, 0, color, width, 2 if dashed else 0))

    def tableau(self, folio, x, y, col_w, row_h, rows, size=250, entete=True):
        """Tableau simple : rows = liste de listes de textes ; col_w = largeurs de colonnes."""
        W = sum(col_w)
        H = row_h * len(rows)
        self.cadre(folio, x, y, x + W, y + H, width=20)
        for r in range(1, len(rows)):
            self.ligne(folio, x, y + r * row_h, x + W, y + r * row_h, width=10)
        cx = x
        for c in col_w[:-1]:
            cx += c
            self.ligne(folio, cx, y, cx, y + H, width=10)
        for r, row in enumerate(rows):
            cx = x
            for c, txt in zip(col_w, row):
                if txt:
                    self.texte(folio, cx + 100, y + r * row_h + (row_h - size) // 2, str(txt), size,
                               bold=1 if (entete and r == 0) else 0)
                cx += c

    def cable(self, folio, x1, x2, y, rep, compo, desig, brins_x, etiq=None, size=300, ovale=False, compo_dx=None, nums=None, blinde=None):
        """Câble (DefCable). etiq = (x, y) du bloc repère / composition / désignation (3 lignes),
        sinon repère à gauche du trait et composition / désignation à droite (défaut WinRelais).
        ovale=True : présentation de Julien (f32, 02/11) : trait du 1er au dernier brin, repère dans un ovale
        à gauche, composition dessous à gauche, désignation gardée mais masquée.
        compo_dx : abscisse de la composition par rapport au 1er brin (placement de Julien, f31 du 02/11)."""
        if ovale:
            x1, x2, etiq, size = brins_x[0], brins_x[-1], "ovale" if compo_dx is None else f"ovale:{compo_dx}", 300
        if nums:
            self.cable_nums[len(self.cables)] = list(nums)
        # type (relu sur le .xrs de Julien du 05/11) : 0 Simple, 1 Rectangle, 2 Blindé (Ellipse), 3 Blindé (Ellipse + Trait),
        # 4 / 5 Blindé (Rectangle arrondi / + Trait). Par défaut : présentation ovale = blindé, sinon simple
        self.cable_type[len(self.cables)] = 3 if (ovale if blinde is None else blinde) else 0
        self.cables.append((folio, x1, x2, y, rep, compo, desig, brins_x, etiq, size))

    def cable_textes(self, c):
        """[(texte, x, y, taille)] des 3 textes d'un câble, tels qu'écrits dans le fichier."""
        f, x1, x2, y, rep, compo, desig, brins, etiq, size = c
        if isinstance(etiq, str):
            w = int(len(rep) * size * 0.55)
            # composition sous l'ovale, arrêtée avant le 1er brin (texte long : décalée à gauche, 02/11)
            cx = min(x1 - 2000, (x1 - 300 - int(len(compo) * size * 0.55)) // 100 * 100)
            if ":" in etiq:
                cx = x1 + int(etiq.split(":")[1])
            return [(rep, x1 - 600 - w // 2, y - 150, size), (compo, cx, y + 400, size), ("", x1, y + 700, size)]
        if etiq:
            ex, ey = etiq
            return [(rep, ex, ey, size), (compo, ex, ey + size + 100, size), (desig, ex, ey + 2 * (size + 100), size)]
        return [(rep, x1 - 600, y - 150, size), (compo, x2 + 400, y - 300, size), (desig, x2 + 400, y, size)]

    # ------------------------------------------------------------------ écriture
    def _finalize_wires(self):
        """Coupe les fils aux dérivations en T et ajoute les points de jonction."""
        changed = True
        tees = set()
        while changed:
            changed = False
            ends = defaultdict(int)
            for w in self.wires:
                ends[(w[0], w[1], w[2])] += 1
                ends[(w[0], w[3], w[4])] += 1
            for k, w in enumerate(self.wires):
                f, x1, y1, x2, y2, t = w
                for (ef, ex, ey) in list(ends):
                    if ef != f or (ex, ey) in ((x1, y1), (x2, y2)):
                        continue
                    on = (x1 == x2 == ex and min(y1, y2) < ey < max(y1, y2)) or \
                         (y1 == y2 == ey and min(x1, x2) < ex < max(x1, x2))
                    if on:
                        self.wires[k] = [f, x1, y1, ex, ey, t]
                        self.wires.append([f, ex, ey, x2, y2, t])
                        tees.add((f, ex, ey, t))
                        # types des autres fils qui aboutissent au point de dérivation
                        host = (self.wires[k], self.wires[-1])
                        others = [w2 for w2 in self.wires if w2[0] == f and w2 is not host[0] and w2 is not host[1]
                                  and (ex, ey) in ((w2[1], w2[2]), (w2[3], w2[4]))]
                        if any(w2[5] == t for w2 in others):
                            self._union(("P", f, ex, ey), ("P", f, x1, y1))
                        else:
                            self.tee_issues.append(
                                f"folio {self.num(f)} : dérivation en T entre types différents en ({ex},{ey}) "
                                f"({t} / {', '.join(sorted({w2[5] for w2 in others}))})")
                        changed = True
                        break
                if changed:
                    break
        ends = defaultdict(int)
        for w in self.wires:
            ends[(w[0], w[1], w[2])] += 1
            ends[(w[0], w[3], w[4])] += 1
        self.jonctions = []
        ttype = {}
        for w in self.wires:
            ttype.setdefault((w[0], w[1], w[2]), w[5])
            ttype.setdefault((w[0], w[3], w[4]), w[5])
        for (f, x, y), c in ends.items():
            if c >= 3:
                t = ttype[(f, x, y)]
                self.jonctions.append((f, x, y, TYPES[t][1], TYPES[t][2]))

    def emprise(self, folio):
        """Rectangle occupé par tout ce qui est dessiné sur le folio (textes estimés)."""
        bx = []
        for p in self.symbols:
            if p.folio == folio:
                if p.bbox:
                    bx.append(p.bbox)
                bx += [b for _, b in p.texts]
        bx += [(min(w[1], w[3]), min(w[2], w[4]), max(w[1], w[3]), max(w[2], w[4]))
               for w in self.wires if w[0] == folio]
        for f, x, y, txt, size, _, _ in self.textes:
            if f == folio:
                bx.append((x, y, x + int(len(txt) * size * 0.55), y + size))
        bx += [(min(d[1], d[3]), min(d[2], d[4]), max(d[1], d[3]), max(d[2], d[4]))
               for d in self.dessins if d[0] == folio]
        for fa, pa, fb, pb, _, _ in self.renvois:
            for f, pt in ((fa, pa), (fb, pb)):
                if f == folio:
                    bx.append(self.renvoi_box(f, pt))
        for c in self.cables:
            if c[0] == folio:
                bx.append((c[1], c[3], c[2], c[3]))
                for txt, x, y, sz in self.cable_textes(c):
                    bx.append((x, y, x + int(len(txt) * sz * 0.55), y + sz))
        if not bx:
            return None
        return (min(b[0] for b in bx), min(b[1] for b in bx), max(b[2] for b in bx), max(b[3] for b in bx))

    def centrer(self, folio, zone_x=None, zone_y=None, pas=400, vertical=True):
        """Décale tout le contenu du folio pour le centrer dans le cadre (pas de grille 400).
        vertical=False : centrage horizontal seul, le haut du folio reste où il est."""
        zx, zy = zone_x or ZONE_X, zone_y or ZONE_Y
        e = self.emprise(folio)
        if not e:
            return (0, 0)
        def pas_vers(d, mini, maxi):     # arrondi vers zéro au pas de grille, sans sortir du cadre
            d = int(d / pas) * pas
            return max(min(d, maxi // pas * pas), -(mini // pas * pas))
        dx = pas_vers(((zx[0] + zx[1]) - (e[0] + e[2])) / 2, e[0] - zx[0], zx[1] - e[2])
        dy = pas_vers(((zy[0] + zy[1]) - (e[1] + e[3])) / 2, e[1] - zy[0], zy[1] - e[3]) if vertical else 0
        if dx or dy:
            self.decaler(folio, dx, dy)
        return (dx, dy)

    def decaler(self, folio, dx, dy):
        mv = lambda xy: (xy[0] + dx, xy[1] + dy)
        for p in self.symbols:
            if p.folio != folio:
                continue
            p.block = XrsDoc.shift_block(p.block, dx, dy, p.rep)
            for k, lst in p.pins.items():
                p.pins[k] = [mv(xy) for xy in lst]
            if p.bbox:
                p.bbox = (p.bbox[0] + dx, p.bbox[1] + dy, p.bbox[2] + dx, p.bbox[3] + dy)
            p.texts = [(t, (b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy)) for t, b in p.texts]
        self.wires = [[w[0], w[1] + dx, w[2] + dy, w[3] + dx, w[4] + dy, w[5]] if w[0] == folio else w
                      for w in self.wires]
        self.renvois = [(fa, mv(pa) if fa == folio else pa, fb, mv(pb) if fb == folio else pb, t, v)
                        for fa, pa, fb, pb, t, v in self.renvois]
        self.textes = [(t[0], t[1] + dx, t[2] + dy) + tuple(t[3:]) if t[0] == folio else t
                       for t in self.textes]
        self.dessins = [(d[0], d[1] + dx, d[2] + dy, d[3] + dx, d[4] + dy) + d[5:] if d[0] == folio else d
                        for d in self.dessins]
        self.logos = [(l[0], l[1] + dx, l[2] + dy) + tuple(l[3:]) if l[0] == folio else l for l in self.logos]
        self.cables = [(c[0], c[1] + dx, c[2] + dx, c[3] + dy) + c[4:7] + ([b + dx for b in c[7]],)
                       + ((c[8][0] + dx, c[8][1] + dy) if isinstance(c[8], tuple) else c[8], c[9])
                       if c[0] == folio else c for c in self.cables]
        key = lambda n: ("P", n[1], n[2] + dx, n[3] + dy) if n[0] == "P" and n[1] == folio else n
        self.nets = {key(a): key(b) for a, b in self.nets.items()}
        self.net_names = {key(a): v for a, v in self.net_names.items()}

    def _folio_block(self, k):
        numero, titre, desc = self.folios[k]
        out = []
        sec = None
        sup = 0
        for l in self.folio_tpl:
            if l.startswith("\u00a4#"):
                m = re.match("\u00a4#(SymboleSupportFolio(?:Rec|Sym))\\d+_(\\d)\u00a4", l)
                if m:
                    l = f"\u00a4#{m.group(1)}{k}_{m.group(2)}\u00a4"
                sec = l
                sup = 0
                out.append(l)
                continue
            f = l.split(SEP)
            if sec == "\u00a4#Autre\u00a4" and len(f) > 19 and f[10].startswith("Folio"):
                f[9], f[10], f[19] = str(k), f"Folio {numero}", numero
            elif sec == "\u00a4#CartoucheTexte\u00a4":
                f[4] = str(k)
                key = f[3]
                if key == "TITRE FOLIO":
                    f[2] = titre
                elif key == "DESCRIPTION FOLIO":
                    f[2] = desc
                elif key == "DATE MODIF":
                    f[2] = DATE
                elif key == "01" and f[11] == "4":
                    f[2] = str(len(self.folios))
                elif key == "01" and f[11] == "1":
                    f[2] = numero
                elif "BAILlY" in f[2]:
                    f[2] = f[2].replace("BAILlY", "BAILLY")
            elif sec == "\u00a4#CartoucheDessinDst\u00a4":
                f[5] = str(k)
            elif sec and sec.startswith("\u00a4#SymboleSupportFolioSym"):
                if sup == 1 and len(f) > 8:     # ligne 2 du ¤#Autre¤ du symbole support
                    f[8] = str(k)
                sup += 1
            out.append(SEP.join(f))
        return out

    def build(self):
        self._finalize_wires()
        L = list(self.header)
        L += ["\u00a4#NombreFolio\u00a4", f"{len(self.folios)}{SEP}"]
        for k in range(len(self.folios)):
            L.append(f"\u00a4#Folio\u00b7{k}\u00a4")
            L += self._folio_block(k)
        L += ["\u00a4#NombreSymbole\u00a4", f"{len(self.symbols)}{SEP}"]
        for n, s in enumerate(self.symbols):
            L.append(f"\u00a4#Symbole\u00b7{n}\u00a4")
            L += s.block
            L.append("\u00a4#FIN\u00a4")
        L.append("\u00a4#FilBus\u00a4")
        for f, x1, y1, x2, y2, t in self.wires:
            L.append(SEP.join(map(str, (x1, y1, x2, y2, f))) + SEP + TYPES[t][0])
        L.append("\u00a4#Jonction\u00a4")
        for f, x, y, w, c in self.jonctions:
            L.append(SEP.join(map(str, (x, y, f, w, 0, 2, c, 0))) + SEP)
        if self.numeros:
            # format relevé sur un fichier numéroté par WinRelais (28/10/2026) :
            # x·y·texte·folio·0·police·taille·angle·couleur·0·0·0·
            L.append("\u00a4#Numero\u00a4")
            for f, x, y, txt, ang in self.numeros:
                L.append(SEP.join(map(str, (x, y, txt, f, 0, "Arial", 300, ang, 8388608, 0, 0, 0))) + SEP)
        if self.renvois:
            L.append("\u00a4#RenvoiF\u00a4")
            for fa, pa, fb, pb, t, vert in self.renvois:
                w = TYPES[t][1]
                ori = f"1\u00b71\u00b7{self.renvoi_code(fa, pa)}\u00b7{self.renvoi_code(fb, pb, False)}"
                ta = f"({self.num(fb)}-{zone(*pb)})"
                tb = f"({self.num(fa)}-{zone(*pa)})"
                L.append(SEP.join(map(str, (fa, fb, pa[0], pa[1], pb[0], pb[1]))) + SEP + ori + SEP +
                         f"{ta}\u00b7{tb}\u00b7{w}\u00b7{w}\u00b7Arial\u00b7300\u00b70\u00b7255\u00b70\u00b70\u00b70\u00b70"
                         "\u00b7\u00b70\u00b71200\u00b7400\u00b71\u00b7\u00b70\u00b71200\u00b7400\u00b71\u00b70\u00b7")
        if self.textes:
            L.append("\u00a4#Texte\u00a4")
            for f, x, y, txt, size, color, bold in self.textes:
                L.append(SEP.join(map(str, (x, y, txt, "", f, 0, "Arial", size, 0, color, bold, -1, 0, 0, "", 0, "", 0))) + SEP)
        if self.dessins:
            L.append("\u00a4#DSansTexte\u00a4")
            for f, x1, y1, x2, y2, forme, color, width, style in self.dessins:
                L.append(SEP.join(map(str, (x1, y1, x2, y2, forme, f, color, width, 0, style, 1, 16777215, 0, 0))) + SEP)
        if self.logos:
            L.append("\u00a4#Logo\u00a4")
            for f, x, y, w, h, chemin, ratio in self.logos:
                L.append(SEP.join(map(str, (x, y, w, h, chemin, 1, ratio, f, 0))) + SEP)
        if self.tableaux_bruts:
            L.append("\u00a4#NombreTableau\u00a4")
            L.append(f"{len(self.tableaux_bruts)}{SEP}")
            for n, (f, lignes) in enumerate(self.tableaux_bruts):
                L.append(f"\u00a4#Tableau\u00b7{n}\u00a4")
                for i, l in enumerate(lignes):
                    if i and lignes[i - 1] == "\u00a4#TableauAutre\u00a4":
                        l = str(f) + l[l.index(SEP):]   # 1er champ = index du folio
                    L.append(l)
        if self.cables:
            L.append("\u00a4#NombreDefCable\u00a4")
            L.append(f"{len(self.cables)}{SEP}")
            for n, c in enumerate(self.cables):
                f, x1, x2, y, rep, compo, desig, brins, etiq, size = c
                (_, rx, ry, _), (_, cx, cy, _), (_, dx_, dy_, _) = self.cable_textes(c)
                L.append(f"\u00a4#DefCable\u00b7{n}\u00a4")
                L.append("\u00a4#Autre\u00a4")
                L.append(SEP.join(map(str, (f, x1, y, x2, y, 0, 0, 0, 0))) + SEP)
                L.append("0\u00b740\u00b70\u00b70\u00b71\u00b716777215\u00b7")
                ov = isinstance(etiq, str)
                L.append(f"802\u00b7500\u00b7{self.cable_type.get(n, 0)}\u00b71\u00b71\u00b711\u00b70\u00b70\u00b7")
                L.append("4\u00b70\u00b7400\u00b7400\u00b7400\u00b7400\u00b70\u00b7")
                if ov:
                    rx = x1 - 600            # repère centré (alignement 6) dans l'ovale
                L.append(SEP.join(map(str, (rep, rx, ry, 1, 6 if ov or not etiq else 0, "Arial", size, 0, 0, 0, 0))) + SEP)
                L.append(SEP.join(map(str, (compo, cx, cy, 1, 0, "Arial", size, 0, 0, 0, 0))) + SEP)
                L.append(SEP.join(map(str, (desig, dx_, dy_, 0 if ov or not desig else 1, 0, "Arial", size, 0, 0, 0, 0))) + SEP)
                for k in range(4):
                    L.append(SEP.join(map(str, ("", x1, y + 1000 + 300 * k, 0, 2, "Arial", 300, 0, 0, 0, 0))) + SEP)
                L.append("\u00a4#BrinCable\u00a4")
                nums = self.cable_nums.get(n) or [i + 1 for i in range(len(brins))]
                L.append("-".join(str(k) for k in nums) + SEP)
                L.append("Arial\u00b7300\u00b70\u00b70\u00b70\u00b7")
                L.append("1\u00b710\u00b70\u00b7")
                for i, bx in enumerate(brins):
                    L.append(SEP.join(map(str, (bx, y, nums[i], 0))) + SEP)
                L.append("\u00a4#FIN\u00a4")
        L.append("\u00a4#FIN\u00a4")
        L.append("")
        return L

    def write(self, path):
        lines = self.build()
        data = "\r\n".join(lines).encode("utf-8")
        with open(path, "wb") as f:
            f.write(b"\xef\xbb\xbf" + data)

    # ------------------------------------------------------------------ contrôles
    def intended_partition(self):
        """{frozenset(clés broches)} des équipotentielles voulues (broches seulement)."""
        groups = defaultdict(set)
        for s in self.symbols:
            for name, pins in s.pins.items():
                for xy in pins:
                    groups[self._find(("P", s.folio) + xy)].add(f"{s.rep}@{s.folio}:{name}")
        return {frozenset(g) for g in groups.values()}

    def geometry_issues(self):
        out = []
        by_folio = defaultdict(list)
        for s in self.symbols:
            by_folio[s.folio].append(s)
            if s.bbox:
                x1, y1, x2, y2 = s.bbox
                if x1 < ZONE_X[0] or x2 > ZONE_X[1] or y1 < ZONE_Y[0] or y2 > ZONE_Y[1]:
                    out.append(f"folio {self.num(s.folio)} : {s.rep} sort du cadre {s.bbox}")
        for f, syms in by_folio.items():
            for i, a in enumerate(syms):
                for b in syms[i + 1:]:
                    if a.bbox and b.bbox and _overlap(_shrink(a.bbox, 50), _shrink(b.bbox, 50)):
                        out.append(f"folio {self.num(f)} : {a.rep} chevauche {b.rep}")
        for w in self.wires:
            f, x1, y1, x2, y2, _ = w
            for v in (x1, x2):
                if not ZONE_X[0] <= v <= ZONE_X[1]:
                    out.append(f"folio {self.num(f)} : fil hors cadre {(x1, y1)}->{(x2, y2)}")
            for v in (y1, y2):
                if not ZONE_Y[0] <= v <= ZONE_Y[1]:
                    out.append(f"folio {self.num(f)} : fil hors cadre {(x1, y1)}->{(x2, y2)}")
            for s in by_folio[f]:
                if not s.bbox:
                    continue
                own = {xy for pins in s.pins.values() for xy in pins}
                bx1, by1, bx2, by2 = _shrink(s.bbox, 60)
                # le fil traverse-t-il le corps du symbole (hors broches du symbole) ?
                if x1 == x2 and bx1 < x1 < bx2:
                    lo, hi = sorted((y1, y2))
                    if lo < by2 and hi > by1 and not ({(x1, y1), (x2, y2)} & own):
                        out.append(f"folio {self.num(f)} : fil x={x1} y={lo}..{hi} traverse {s.rep}")
                if y1 == y2 and by1 < y1 < by2:
                    lo, hi = sorted((x1, x2))
                    if lo < bx2 and hi > bx1 and not ({(x1, y1), (x2, y2)} & own):
                        out.append(f"folio {self.num(f)} : fil y={y1} x={lo}..{hi} traverse {s.rep}")
        # textes (champs visibles des symboles + textes libres)
        texts = defaultdict(list)       # folio -> (propriétaire, texte, boîte)
        for s in self.symbols:
            for txt, box in getattr(s, "texts", []):
                # largeur Arial (02/11) ; le bord gauche reste celui de la mise en page
                box = (box[0], box[1], box[0] + min(box[2] - box[0], largeur(txt, box[3] - box[1])), box[3])
                texts[s.folio].append((s.rep, txt, box))
        for f, x, y, txt, size, _, _ in self.textes:
            texts[f].append(("texte", txt, (x, y, x + largeur(txt, size), y + size)))
        for c in self.cables:
            for txt, x, y, sz in self.cable_textes(c):
                if txt:
                    texts[c[0]].append((f"câble {c[4]}", txt, (x, y, x + largeur(txt, sz), y + sz)))
        for f, lst in texts.items():
            for i, (own, txt, box) in enumerate(lst):
                b = _shrink(box, 20)
                if b[2] > ZONE_X[1] + 200:
                    out.append(f"folio {self.num(f)} : texte « {txt} » ({own}) sort du cadre")
                for s in by_folio[f]:
                    if s.rep != own and s.bbox and _overlap(b, _shrink(s.bbox, 40)):
                        out.append(f"folio {self.num(f)} : texte « {txt} » ({own}) chevauche le symbole {s.rep}")
                for (own2, txt2, box2) in lst[i + 1:]:
                    if _overlap(b, _shrink(box2, 20)):
                        out.append(f"folio {self.num(f)} : texte « {txt} » ({own}) chevauche « {txt2} » ({own2})")
                for w in self.wires:
                    if w[0] != f:
                        continue
                    _, x1, y1, x2, y2, _ = w
                    seg = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
                    if seg[0] == seg[2]:
                        seg = (seg[0] - 1, seg[1], seg[2] + 1, seg[3])
                    else:
                        seg = (seg[0], seg[1] - 1, seg[2], seg[3] + 1)
                    if _overlap(b, seg):
                        out.append(f"folio {self.num(f)} : texte « {txt} » ({own}) traversé par un fil ({x1},{y1})->({x2},{y2})")
                        break
        # emprise des renvois (flèche + texte) : dans le cadre, sans chevauchement
        boxes = defaultdict(list)
        for fa, pa, fb, pb, _, _ in self.renvois:
            for f, p in ((fa, pa), (fb, pb)):
                boxes[f].append((p, self.renvoi_box(f, p)))
        for f, lst in boxes.items():
            for i, (p, b) in enumerate(lst):
                lab = f"folio {self.num(f)} : renvoi en {p}"
                if b[0] < ZONE_X[0] or b[2] > ZONE_X[1] or b[1] < ZONE_Y[0] or b[3] > ZONE_Y[1] + 100:
                    out.append(f"{lab} : flèche / texte hors du cadre")
                if len(self._wire_dirs(f, p)) != 1:
                    out.append(f"{lab} : doit être au bout d'un fil droit (pas dans un angle ni sur un T)")
                for w in self.wires:
                    seg = (min(w[1], w[3]), min(w[2], w[4]), max(w[1], w[3]), max(w[2], w[4]))
                    if w[0] == f and _overlap(b, seg) and p not in (tuple(w[1:3]), tuple(w[3:5])):
                        out.append(f"{lab} : flèche / texte traversé par un fil {w[1:5]}")
                        break
                for (p2, b2) in lst[i + 1:]:
                    if _overlap(b, b2):
                        out.append(f"{lab} : chevauche le renvoi en {p2}")
                for s in by_folio[f]:
                    if s.bbox and _overlap(b, _shrink(s.bbox, 40)):
                        out.append(f"{lab} : chevauche le symbole {s.rep}")
                for own, txt, tb in texts[f]:
                    if _overlap(b, tb):
                        out.append(f"{lab} : chevauche le texte « {txt} » ({own})")
                for w in self.wires:
                    if w[0] != f or p in ((w[1], w[2]), (w[3], w[4])):
                        continue
                    seg = (min(w[1], w[3]) - 1, min(w[2], w[4]) - 1, max(w[1], w[3]) + 1, max(w[2], w[4]) + 1)
                    if _overlap(b, seg):
                        out.append(f"{lab} : traversé par un fil ({w[1]},{w[2]})->({w[3]},{w[4]})")
                        break
        # chevauchement de fils colinéaires appartenant à des potentiels différents
        segs = defaultdict(list)
        for w in self.wires:
            f, x1, y1, x2, y2, _ = w
            if x1 == x2:
                segs[(f, "v", x1)].append((min(y1, y2), max(y1, y2), (x1, y1)))
            else:
                segs[(f, "h", y1)].append((min(x1, x2), max(x1, x2), (x1, y1)))
        for (f, o, c), lst in segs.items():
            lst.sort()
            for (a1, a2, pa), (b1, b2, pb) in zip(lst, lst[1:]):
                if b1 < a2:     # règle VRE 107 : deux fils ne se chevauchent jamais
                    out.append(f"folio {self.num(f)} : fils superposés ({o} {c}, {b1}..{a2})")
        return out


def _wrap(txt, n):
    words, lines, cur = [], [], ""
    for w in txt.split(" "):            # mots trop longs : coupe aux « / » puis en dur
        while len(w) > n:
            cut = w.rfind("/", 0, n)
            cut = cut + 1 if cut > 0 else n
            words.append(w[:cut])
            w = w[cut:]
        words.append(w)
    for w in words:
        if cur and len(cur) + 1 + len(w) > n:
            if cur.endswith(" -"):          # le tiret passe en début de ligne suivante
                lines.append(cur[:-2])
                cur = f"- {w}"
                continue
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    lines.append(cur)
    return lines


def _shrink(b, d):
    return (b[0] + d, b[1] + d, b[2] - d, b[3] - d)


def _overlap(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def check(gen, path):
    """Relit le fichier écrit et compare aux intentions. Retourne la liste des problèmes."""
    import xrs_tool
    issues = []
    m = xrs_tool.parse(path)
    uf, _ = xrs_tool.build_nets(m)
    groups = defaultdict(set)
    for s in m["symboles"]:
        for b in s["broches"]:
            groups[uf.find(("B", s["index"], b["nom"], b["x"], b["y"]))].add(f"{s['nom']}@{s['folio']}:{b['nom']}")
    actual = {frozenset(g) for g in groups.values()}
    wanted = gen.intended_partition()
    # une broche de nom répété (ex. N/N) apparaît une fois par position : comparer sur les ensembles
    for g in wanted - actual:
        issues.append("équipotentielle voulue non retrouvée : " + ", ".join(sorted(g)))
    for g in actual - wanted:
        issues.append("équipotentielle relue non voulue : " + ", ".join(sorted(g)))
    issues += gen.tee_issues
    issues += gen.geometry_issues()
    return issues
