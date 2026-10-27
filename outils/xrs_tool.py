"""Lecture, analyse et contrôle d'un schéma WinRelais (.xrs / .xrm).

Usage :
    python xrs_tool.py resume       <fichier.xrs>   inventaire folio par folio (Markdown)
    python xrs_tool.py nomenclature <fichier.xrs>   liste des symboles (CSV ; séparateur ;)
    python xrs_tool.py verifier     <fichier.xrs>   contrôles de cohérence
    python xrs_tool.py json         <fichier.xrs>   modèle complet en JSON

Le fichier n'est jamais modifié. Format décrit dans ../FORMAT_XRS.md.
"""
import csv
import io
import json
import re
import sys
from collections import Counter, defaultdict

SEP = "·"      # « · » séparateur de champs
GRID = 400          # grille WinRelais : 4 mm = 400 (unité 1/100 mm)


# --------------------------------------------------------------------------- lecture

def read_lines(path):
    raw = open(path, "rb").read()
    body = raw[3:] if raw.startswith(b"\xef\xbb\xbf") else raw
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError:
        # anciens fichiers (v1.x / 2.0-2.3) : Windows-1252, mêmes séparateurs
        text = body.decode("cp1252")
    return text.replace("\r\n", "\n").split("\n")


def fields(line):
    f = line.split(SEP)
    if f and f[-1] == "":
        f.pop()
    return f


def is_header(line):
    return line.startswith("¤#")


def header_name(line):
    # « ¤#Folio·3¤ » -> ("Folio", "3")
    m = re.match("¤#([^¤·]+)(?:·([^¤]*))?¤", line)
    return (m.group(1), m.group(2)) if m else (line, None)


def to_int(s, default=0):
    try:
        return int(float(s))
    except (ValueError, TypeError):
        return default


def split_sections(lines):
    """Découpe une liste de lignes en [(nom, arg, [lignes])] au premier niveau."""
    out = []
    cur = None
    for l in lines:
        if is_header(l):
            name, arg = header_name(l)
            cur = (name, arg, [])
            out.append(cur)
        elif cur is not None:
            cur[2].append(l)
    return out


def parse_symbol(block, index):
    """block = lignes entre ¤#Symbole·n¤ et son ¤#FIN¤ (exclus)."""
    secs = {}
    for name, _, body in split_sections(block):
        secs.setdefault(name, []).extend(body)
    a = secs.get("Autre", [])
    origin = fields(a[0]) if a else ["0", "0"]
    info = fields(a[1]) if len(a) > 1 else []
    info += [""] * (15 - len(info))
    champs = []
    for l in a[2:10]:
        f = fields(l)
        f += [""] * (5 - len(f))
        champs.append({"texte": f[0], "x": to_int(f[1]), "y": to_int(f[2]), "visible": f[3] == "1"})
    pins = []
    for l in secs.get("Broche", []):
        f = fields(l)
        if len(f) < 18:
            continue
        pins.append({"nom": f[0], "x": to_int(f[1]), "y": to_int(f[2]),
                     "xi": to_int(f[3]), "yi": to_int(f[4]), "dir": to_int(f[17])})
    ref = fields(secs.get("RefCroise", [""])[0]) if secs.get("RefCroise") else []
    fab = fields(secs.get("RefConstructeur", [""])[0]) if secs.get("RefConstructeur") else []
    fab += [""] * (4 - len(fab))
    lib = fields(secs.get("VersionSymbole", [""])[0]) if secs.get("VersionSymbole") else []
    nom = champs[0]["texte"] if champs else ""
    return {
        "index": index,
        "x": to_int(origin[0]), "y": to_int(origin[1]),
        "famille": info[1], "symbole": info[2], "prefixe": info[4],
        "folio": to_int(info[8]),
        "borne": info[11] == "1",
        "nom": nom,
        "champs": [c["texte"] for c in champs],
        "broches": pins,
        "refcroise_type": to_int(ref[0], -1) if ref else -1,
        "fabricant": fab[0], "reference": fab[2],
        "librairie": lib[2] if len(lib) > 2 else "",
        "n_contours": len(secs.get("Contour", [])),
    }


def parse(path):
    lines = read_lines(path)
    model = {"fichier": path, "version": "", "folios": [], "symboles": [], "fils": [],
             "jonctions": [], "renvois": [], "numeros": [], "textes": [], "cables": [],
             "sections_inconnues": Counter()}
    i, n = 0, len(lines)

    def take_until_fin(start):
        """Renvoie (lignes du bloc, index après le ¤#FIN¤ correspondant), gère l'imbrication."""
        depth, j = 0, start
        body = []
        while j < n:
            l = lines[j]
            if is_header(l):
                name, _ = header_name(l)
                if name == "FIN":
                    if depth == 0:
                        return body, j + 1
                    depth -= 1
                elif name.startswith("SymboleSupportFolioSym"):
                    depth += 1
            body.append(l)
            j += 1
        return body, j

    while i < n:
        l = lines[i]
        if not is_header(l):
            i += 1
            continue
        name, arg = header_name(l)
        if name == "Version":
            model["version"] = (fields(lines[i + 3]) or [""])[0] if i + 3 < n else ""
            i += 1
        elif name == "Folio":
            body, i = take_until_fin(i + 1)
            secs = split_sections(body)
            autre = next((b for nm, _, b in secs if nm == "Autre"), [])
            f = fields(autre[0]) if autre else []
            f += [""] * (21 - len(f))
            cart = {}
            for nm, _, b in secs:
                if nm == "CartoucheTexte":
                    for cl in b:
                        cf = fields(cl)
                        if len(cf) > 3:
                            cart.setdefault(cf[3], cf[2])
            model["folios"].append({
                "index": to_int(arg), "largeur": to_int(f[0]), "hauteur": to_int(f[1]),
                "nom": f[10], "numero": f[19],
                "titre": cart.get("TITRE FOLIO", ""), "description": cart.get("DESCRIPTION FOLIO", ""),
            })
        elif name == "Symbole":
            body, i = take_until_fin(i + 1)
            model["symboles"].append(parse_symbol(body, to_int(arg)))
        elif name == "DefCable":
            body, i = take_until_fin(i + 1)
            secs = split_sections(body)
            autre = next((b for nm, _, b in secs if nm == "Autre"), [])
            brins = next((b for nm, _, b in secs if nm == "BrinCable"), [])
            f0 = fields(autre[0]) if autre else []
            champs = [fields(x)[0] if fields(x) else "" for x in autre[4:11]]
            model["cables"].append({"folio": to_int(f0[0]) if f0 else -1,
                                    "nom": champs[0] if champs else "",
                                    "champs": champs,
                                    "brins": (fields(brins[0]) or [""])[0] if brins else ""})
        elif name in ("FilBus", "Jonction", "RenvoiF", "Numero", "Texte"):
            j = i + 1
            while j < n and not is_header(lines[j]):
                f = fields(lines[j])
                if f:
                    if name == "FilBus" and len(f) >= 10:
                        model["fils"].append({"x1": to_int(f[0]), "y1": to_int(f[1]), "x2": to_int(f[2]),
                                              "y2": to_int(f[3]), "folio": to_int(f[4]),
                                              "epaisseur": to_int(f[6]), "couleur": to_int(f[7]),
                                              "type": f[9], "ligne": j + 1})
                    elif name == "Jonction" and len(f) >= 3:
                        model["jonctions"].append({"x": to_int(f[0]), "y": to_int(f[1]), "folio": to_int(f[2])})
                    elif name == "RenvoiF" and len(f) >= 12:
                        model["renvois"].append({"folioA": to_int(f[0]), "folioB": to_int(f[1]),
                                                 "xA": to_int(f[2]), "yA": to_int(f[3]),
                                                 "xB": to_int(f[4]), "yB": to_int(f[5]),
                                                 "texteA": f[10], "texteB": f[11], "ligne": j + 1})
                    elif name == "Numero" and len(f) >= 3:
                        model["numeros"].append({"x": to_int(f[0]), "y": to_int(f[1]), "texte": f[2],
                                                 "folio": to_int(f[3]) if len(f) > 3 else 0})
                    elif name == "Texte" and len(f) >= 5:
                        model["textes"].append({"x": to_int(f[0]), "y": to_int(f[1]), "texte": f[2],
                                                "folio": to_int(f[4])})
                j += 1
            i = j
        else:
            i += 1
    return model


# --------------------------------------------------------------------------- utilitaires

def folio_label(model, idx):
    for f in model["folios"]:
        if f["index"] == idx:
            return f["numero"] or str(idx)
    return f"?{idx}"


def on_segment(px, py, w):
    """Point strictement à l'intérieur d'un fil horizontal ou vertical (ou oblique)."""
    x1, y1, x2, y2 = w["x1"], w["y1"], w["x2"], w["y2"]
    if (px, py) in ((x1, y1), (x2, y2)):
        return False
    if (x2 - x1) * (py - y1) != (y2 - y1) * (px - x1):
        return False
    return min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2)


class UF:
    def __init__(self):
        self.p = {}

    def find(self, a):
        self.p.setdefault(a, a)
        while self.p[a] != a:
            self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


def build_nets(model):
    """Calcule les équipotentielles (fils + broches + renvois de folio)."""
    uf = UF()
    by_folio = defaultdict(list)
    for k, w in enumerate(model["fils"]):
        by_folio[w["folio"]].append((k, w))
        uf.union(("P", w["folio"], w["x1"], w["y1"]), ("P", w["folio"], w["x2"], w["y2"]))
    t_sans_jonction = []
    jset = {(j["folio"], j["x"], j["y"]) for j in model["jonctions"]}
    for fol, ws in by_folio.items():
        for _, w in ws:
            for (px, py) in ((w["x1"], w["y1"]), (w["x2"], w["y2"])):
                for _, o in ws:
                    if o is not w and on_segment(px, py, o):
                        uf.union(("P", fol, px, py), ("P", fol, o["x1"], o["y1"]))
                        if (fol, px, py) not in jset:
                            t_sans_jonction.append((fol, px, py))
    for r in model["renvois"]:
        uf.union(("P", r["folioA"], r["xA"], r["yA"]), ("P", r["folioB"], r["xB"], r["yB"]))
    for s in model["symboles"]:
        for b in s["broches"]:
            uf.union(("B", s["index"], b["nom"], b["x"], b["y"]), ("P", s["folio"], b["x"], b["y"]))
        if s.get("borne"):      # une borne relie ses deux côtés (même équipotentielle)
            bs = s["broches"]
            for b in bs[1:]:
                uf.union(("B", s["index"], bs[0]["nom"], bs[0]["x"], bs[0]["y"]),
                         ("B", s["index"], b["nom"], b["x"], b["y"]))
    return uf, t_sans_jonction


# --------------------------------------------------------------------------- commandes

def cmd_resume(model):
    out = io.StringIO()
    p = lambda *a: print(*a, file=out)
    p(f"# Résumé : {model['fichier']}")
    p(f"\nWinRelais {model['version']} - {len(model['folios'])} folios, {len(model['symboles'])} symboles, "
      f"{len(model['fils'])} fils, {len(model['renvois'])} renvois, {len(model['cables'])} câbles, "
      f"{len(model['numeros'])} numéros de fil\n")
    sym_f = defaultdict(list)
    for s in model["symboles"]:
        sym_f[s["folio"]].append(s)
    fil_f = Counter(w["folio"] for w in model["fils"])
    p("| Ordre | N° | Titre | Description | Symboles | Fils |")
    p("|---|---|---|---|---|---|")
    for f in model["folios"]:
        noms = ", ".join(s["nom"] for s in sym_f[f["index"]]) or "-"
        p(f"| {f['index'] + 1} | {f['numero']} | {f['titre']} | {f['description']} | {noms} | {fil_f[f['index']]} |")
    return out.getvalue()


def cmd_nomenclature(model):
    out = io.StringIO()
    w = csv.writer(out, delimiter=";", lineterminator="\n")
    w.writerow(["Repère", "Folio", "Désignation", "Champ 3", "Champ 4", "Fabricant", "Référence",
                "Symbole", "Nb broches", "X", "Y"])
    for s in sorted(model["symboles"], key=lambda s: (s["prefixe"], natural(s["nom"]))):
        c = s["champs"] + [""] * 4
        w.writerow([s["nom"], folio_label(model, s["folio"]), c[1], c[2], c[3], s["fabricant"],
                    s["reference"], s["symbole"], len(s["broches"]), s["x"], s["y"]])
    return out.getvalue()


def natural(s):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]


def cmd_verifier(model):
    issues = []   # (gravité, catégorie, message)
    add = lambda g, c, m: issues.append((g, c, m))
    folios = {f["index"]: f for f in model["folios"]}
    lab = lambda i: folio_label(model, i)

    # --- folios
    for key, label in (("numero", "numéro"), ("nom", "nom interne"), ("titre", "titre"),
                       ("description", "description")):
        cnt = Counter(f[key] for f in model["folios"] if f[key])
        for v, c in cnt.items():
            if c > 1:
                which = ", ".join(f["numero"] for f in model["folios"] if f[key] == v)
                g = "ERREUR" if key == "numero" else "ATTENTION"
                add(g, "Folios", f"{label} « {v} » utilisé {c} fois (folios {which})")

    # --- repères
    names = defaultdict(list)
    for s in model["symboles"]:
        names[s["nom"]].append(s)
        if not s["nom"] or s["nom"].endswith("?"):
            add("ERREUR", "Repères", f"symbole sans repère sur folio {lab(s['folio'])} ({s['symbole']})")
        elif not s["nom"].startswith(s["prefixe"]) and s["prefixe"] not in ("", "Abr."):
            add("ATTENTION", "Repères", f"{s['nom']} : préfixe de la librairie « {s['prefixe']} » différent du repère")
        if s["folio"] not in folios:
            add("ERREUR", "Repères", f"{s['nom']} rattaché à un folio inexistant ({s['folio']})")
    for nm, lst in names.items():
        if len(lst) > 1 and nm:
            same_sym = len({s["symbole"] for s in lst}) == 1
            fl = ", ".join(lab(s["folio"]) for s in lst)
            if lst[0]["refcroise_type"] == -1:
                add("ERREUR" if same_sym else "ATTENTION", "Repères",
                    f"repère {nm} présent {len(lst)} fois (folios {fl}) sans lien de référence croisée")
    by_ref = defaultdict(set)
    for s in model["symboles"]:
        if s["reference"]:
            m = re.match(r"([A-Z]+)", s["nom"])
            by_ref[s["reference"]].add(m.group(1) if m else s["nom"])
    for ref, prefs in by_ref.items():
        if len(prefs) > 1:
            who = [s["nom"] for s in model["symboles"] if s["reference"] == ref]
            add("ATTENTION", "Repères", f"même référence {ref} repérée avec des préfixes différents : {', '.join(who)}")
    for s in model["symboles"]:
        cnt = Counter(b["nom"] for b in s["broches"] if b["nom"])
        dup = [k for k, v in cnt.items() if v > 1]
        if dup:
            add("INFO", "Symboles", f"{s['nom']} : broches de même nom {dup} (bornier/nomenclature ambigus)")
        if s["n_contours"] == 0 and not s["broches"]:
            add("ATTENTION", "Symboles", f"{s['nom']} : symbole vide")

    # --- fils
    seen = Counter((w["folio"], *sorted([(w["x1"], w["y1"]), (w["x2"], w["y2"])])) for w in model["fils"])
    for k, c in seen.items():
        if c > 1:
            add("ATTENTION", "Fils", f"folio {lab(k[0])} : fil en double {k[1]}->{k[2]} ({c}x)")
    for w in model["fils"]:
        if (w["x1"], w["y1"]) == (w["x2"], w["y2"]):
            add("ATTENTION", "Fils", f"folio {lab(w['folio'])} : fil de longueur nulle en ({w['x1']},{w['y1']})")
        elif w["x1"] != w["x2"] and w["y1"] != w["y2"]:
            add("INFO", "Fils", f"folio {lab(w['folio'])} : fil oblique ({w['x1']},{w['y1']})->({w['x2']},{w['y2']})")
        for v in (w["x1"], w["y1"], w["x2"], w["y2"]):
            if v % (GRID // 2):
                add("INFO", "Fils", f"folio {lab(w['folio'])} : extrémité hors grille ({w['x1']},{w['y1']})->({w['x2']},{w['y2']})")
                break

    # --- connectivité
    uf, t_sans_j = build_nets(model)
    pin_pts = defaultdict(list)
    for s in model["symboles"]:
        for b in s["broches"]:
            pin_pts[(s["folio"], b["x"], b["y"])].append(f"{s['nom']}:{b['nom']}")
    end_cnt = Counter()
    for w in model["fils"]:
        end_cnt[(w["folio"], w["x1"], w["y1"])] += 1
        end_cnt[(w["folio"], w["x2"], w["y2"])] += 1
    renvoi_pts = set()
    for r in model["renvois"]:
        renvoi_pts.add((r["folioA"], r["xA"], r["yA"]))
        renvoi_pts.add((r["folioB"], r["xB"], r["yB"]))
    fils_par_folio = defaultdict(list)
    for w in model["fils"]:
        fils_par_folio[w["folio"]].append(w)
    jset = {(j["folio"], j["x"], j["y"]) for j in model["jonctions"]}
    for pt, c in end_cnt.items():
        if c > 1 or pt in pin_pts or pt in renvoi_pts:
            continue
        if any(on_segment(pt[1], pt[2], o) for o in fils_par_folio[pt[0]]):
            continue
        if pt in jset:
            add("INFO", "Connexions", f"folio {lab(pt[0])} : fil terminé sur un point de jonction seul en ({pt[1]},{pt[2]})")
            continue
        near = min(((abs(b["x"] - pt[1]) + abs(b["y"] - pt[2]), f"{s['nom']}:{b['nom']}", (b["x"], b["y"]))
                    for s in model["symboles"] if s["folio"] == pt[0] for b in s["broches"]), default=None)
        # attente partant de la broche elle-même (l'autre bout du fil est sur la broche) : normal
        autre_bout = {(w["x2"], w["y2"]) if (w["x1"], w["y1"]) == pt[1:] else (w["x1"], w["y1"])
                      for w in fils_par_folio[pt[0]] if pt[1:] in ((w["x1"], w["y1"]), (w["x2"], w["y2"]))}
        if near and near[0] <= GRID and near[2] not in autre_bout:
            add("ERREUR", "Connexions",
                f"folio {lab(pt[0])} : fil arrêté à {near[0] / 100:g} mm de la broche {near[1]} en ({pt[1]},{pt[2]}) - NON raccordé")
        else:
            add("ATTENTION", "Connexions", f"folio {lab(pt[0])} : fil en attente (extrémité libre) en ({pt[1]},{pt[2]})")
    for s in model["symboles"]:
        if s["x"] % (GRID // 2) or s["y"] % (GRID // 2):
            add("ATTENTION", "Symboles", f"{s['nom']} (folio {lab(s['folio'])}) posé hors grille ({s['x']},{s['y']}) : ses broches ne tombent pas sur la grille des fils")
    for fol, x, y in sorted(set(t_sans_j)):
        add("INFO", "Connexions", f"folio {lab(fol)} : dérivation en T sans point de jonction en ({x},{y})")
    for s in model["symboles"]:
        libres = []
        for b in s["broches"]:
            pt = (s["folio"], b["x"], b["y"])
            if pt in end_cnt or pt in renvoi_pts:
                continue
            if any(on_segment(b["x"], b["y"], o) for o in fils_par_folio[s["folio"]]):
                add("ATTENTION", "Connexions", f"{s['nom']}:{b['nom']} (folio {lab(s['folio'])}) : un fil passe sur la broche sans s'y arrêter")
            else:
                libres.append(b["nom"] or "?")
        if libres:
            tot = len(s["broches"])
            add("INFO", "Broches libres", f"{s['nom']} (folio {lab(s['folio'])}) : {len(libres)}/{tot} libres - {', '.join(libres)}")
    for (fol, x, y), who in pin_pts.items():
        if len(who) > 1:
            add("ATTENTION", "Connexions", f"folio {lab(fol)} : broches superposées {who} en ({x},{y})")

    # --- équipotentielles et types de conducteur
    nets = defaultdict(lambda: {"types": Counter(), "broches": [], "folios": set()})
    for w in model["fils"]:
        r = uf.find(("P", w["folio"], w["x1"], w["y1"]))
        nets[r]["types"][w["type"] or "(sans type)"] += 1
        nets[r]["folios"].add(lab(w["folio"]))
    for s in model["symboles"]:
        for b in s["broches"]:
            r = uf.find(("B", s["index"], b["nom"], b["x"], b["y"]))
            if r in nets:
                nets[r]["broches"].append(f"{s['nom']}:{b['nom']}")
    for net in nets.values():
        types = [t for t in net["types"] if t != "Conducteur terre"]
        if len(set(net["types"])) > 1:
            add("ATTENTION", "Types de conducteur",
                f"un même potentiel mélange {dict(net['types'])} - folios {sorted(net['folios'])} - "
                f"broches {net['broches'][:8]}{'…' if len(net['broches']) > 8 else ''}")
    # 24 V alternatif utilisé sur un folio dont le titre parle de continu
    for f in model["folios"]:
        txt = (f["titre"] + " " + f["description"]).upper()
        n_ac = sum(1 for w in model["fils"] if w["folio"] == f["index"] and "~" in w["type"])
        if n_ac and ("VDC" in txt or "SECURITE" in txt or "RELAIS" in txt or "AUTOMATE" in txt):
            add("ATTENTION", "Types de conducteur",
                f"folio {f['numero']} ({f['titre']}) : {n_ac} fils de type « Commande 24V~ » (alternatif) sur un circuit a priori continu")

    # --- renvois de folio
    num_of = {f["index"]: f["numero"] for f in model["folios"]}
    for r in model["renvois"]:
        for side, other in (("texteA", "folioB"), ("texteB", "folioA")):
            m = re.match(r"\((\w+)-", r[side])
            if m and num_of.get(r[other]) and m.group(1) != num_of[r[other]]:
                add("ERREUR", "Renvois",
                    f"renvoi folio {lab(r['folioA'])}<->{lab(r['folioB'])} : texte « {r[side]} » ne pointe pas vers le folio {num_of[r[other]]} (ligne {r['ligne']})")
        for fol, x, y in ((r["folioA"], r["xA"], r["yA"]), (r["folioB"], r["xB"], r["yB"])):
            if (fol, x, y) in end_cnt:
                continue
            if any(on_segment(x, y, o) for o in fils_par_folio[fol]):
                add("ATTENTION", "Renvois", f"renvoi folio {lab(fol)} en ({x},{y}) posé au milieu d'un fil, pas sur une extrémité")
                continue
            d_end = min((abs(ex - x) + abs(ey - y) for (ef, ex, ey) in end_cnt if ef == fol), default=None)
            if d_end is not None and d_end <= GRID:
                add("ERREUR", "Renvois", f"renvoi folio {lab(fol)} en ({x},{y}) à {d_end / 100:g} mm de l'extrémité d'un fil - NON raccordé")
            else:
                add("ATTENTION", "Renvois", f"renvoi folio {lab(fol)} en ({x},{y}) non relié à un fil")

    # --- divers
    if not model["numeros"]:
        add("INFO", "Numérotation", "aucun numéro de fil/équipotentielle placé (section ¤#Numero absente)")
    for f in model["folios"]:
        if not any(s["folio"] == f["index"] for s in model["symboles"]) and \
                not any(w["folio"] == f["index"] for w in model["fils"]) and f["index"] > 3:
            add("INFO", "Folios", f"folio {f['numero']} ({f['titre']}) : aucun symbole ni fil")

    order = {"ERREUR": 0, "ATTENTION": 1, "INFO": 2}
    issues.sort(key=lambda t: (order[t[0]], t[1]))
    out = io.StringIO()
    p = lambda *a: print(*a, file=out)
    cnt = Counter(g for g, _, _ in issues)
    p(f"# Vérification : {model['fichier']}")
    p(f"\n{cnt['ERREUR']} erreur(s), {cnt['ATTENTION']} point(s) d'attention, {cnt['INFO']} info(s)\n")
    cur = None
    for g, c, m in issues:
        if (g, c) != cur:
            cur = (g, c)
            p(f"\n## {g} - {c}\n")
        p(f"- {m}")
    return out.getvalue()


def main(argv):
    if len(argv) < 3 or argv[1] not in ("resume", "nomenclature", "verifier", "json"):
        print(__doc__)
        return 1
    model = parse(argv[2])
    if argv[1] == "resume":
        txt = cmd_resume(model)
    elif argv[1] == "nomenclature":
        txt = cmd_nomenclature(model)
    elif argv[1] == "verifier":
        txt = cmd_verifier(model)
    else:
        model["sections_inconnues"] = dict(model["sections_inconnues"])
        txt = json.dumps(model, ensure_ascii=False, indent=1)
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdout.write(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
