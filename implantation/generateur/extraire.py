"""Extraction des données du schéma (.xrs) pour le dossier d'implantation.

Lit le .xrs avec outils/xrs_tool.py (parseur du dépôt), lit saisie.json (données
hors schéma : rails, câbles achetés, décisions), et écrit donnees.json, le fichier
unique d'où sont générés l'implantation, la liste des câbles et le synoptique.

Usage : python -I extraire.py [fichier.xrs]
"""
import glob
import json
import os
import re
import sys
from collections import defaultdict

ICI = os.path.dirname(os.path.abspath(__file__))
DEPOT = os.path.dirname(os.path.dirname(ICI))
sys.path.insert(0, os.path.join(DEPOT, "outils"))
import xrs_tool  # noqa: E402

# appareils hors armoire (+M machine, +P1 pupitre)
# v14 : les bornes X1.n de la boîte +BJM (hors armoire) sont du côté extérieur
TERRAIN = re.compile(r"^(B\d|M\d|S2|S3|P1|H1|X1\.\d+)$")
# appareils de porte (+A1, porte)
PORTE = re.compile(r"^(S1|S4|H2|H3|H4)$")


def derniere_release():
    f = sorted(glob.glob(os.path.join(DEPOT, "schema", "generes", "release", "*.xrs")))
    if len(f) != 1:
        sys.exit(f"release : {len(f)} fichier(s) .xrs, 1 attendu")
    return f[0]


def extraire(path):
    m = xrs_tool.parse(path)
    num = {f["index"]: f["numero"] for f in m["folios"]}
    # bornes non passantes : chaque côté d'une borne a sa propre équipotentielle
    for s in m["symboles"]:
        s["borne_vraie"] = s.get("borne")
        s["borne"] = False
    uf, _ = xrs_tool.build_nets(m)
    membres = defaultdict(list)
    for s in m["symboles"]:
        for b in s["broches"]:
            membres[uf.find(("B", s["index"], b["nom"], b["x"], b["y"]))].append((s, b["nom"]))

    # numéros de fil : rattachés au fil le plus proche (même règle que outils/xrs_numeros.py)
    lignes = open(path, "rb").read().decode("utf-8-sig").replace("\r\n", "\n").split("\n")
    angle, i = {}, lignes.index("¤#Numero¤") + 1
    while not lignes[i].startswith("¤#"):
        f = lignes[i].split("·")
        if len(f) > 7:
            angle[(int(f[3]), int(f[0]), int(f[1]), f[2])] = int(f[7])
        i += 1
    numero_pot = defaultdict(set)
    for n in m["numeros"]:
        vert = angle.get((n["folio"], n["x"], n["y"], n["texte"])) == 90
        best, d_best = None, 801
        for w in m["fils"]:
            if w["folio"] != n["folio"]:
                continue
            x1, x2 = sorted((w["x1"], w["x2"]))
            y1, y2 = sorted((w["y1"], w["y2"]))
            if vert and x1 == x2 == n["x"]:
                d = max(y1 - n["y"], n["y"] - y2, 0)
            elif not vert and y1 == y2 == n["y"]:
                d = max(x1 - n["x"], n["x"] - x2, 0)
            else:
                continue
            if d < d_best:
                best, d_best = w, d
        if best is not None and not n["texte"].startswith("PN"):
            numero_pot[uf.find(("P", best["folio"], best["x1"], best["y1"]))].add(n["texte"])

    designation, reference = {}, {}
    for s in m["symboles"]:
        if s["champs"] and s["champs"][1]:
            designation.setdefault(s["nom"], s["champs"][1])
        if s["reference"]:
            reference.setdefault(s["nom"], s["reference"])

    bornes = {}
    for s in m["symboles"]:
        if not s["borne_vraie"] or not s["nom"].startswith("X") or s["nom"] == "XD1":
            continue
        cotes = []
        for b in s["broches"]:
            r = uf.find(("B", s["index"], b["nom"], b["x"], b["y"]))
            autres = sorted({f"{o['nom']}:{p}" for o, p in membres[r] if o is not s})
            cotes.append({"broche": b["nom"], "raccords": autres, "numeros": sorted(numero_pot.get(r, ()))})
        rec = bornes.setdefault(s["nom"], {
            "repere": s["nom"], "folio": num[s["folio"]], "symbole": s["symbole"],
            "reference": s["reference"], "fonction": s["champs"][1] if s["champs"] else "",
            "cotes": []})
        rec["cotes"].extend(cotes)
    # côté terrain / côté armoire (bornes simples, 2 broches)
    for rec in bornes.values():
        if rec["symbole"].startswith("borne distribution"):
            rec["type"] = "PTFIX"
            continue
        rec["type"] = "terre" if "terre" in rec["symbole"] else "borne"
        ext, inte, nums = [], [], set()
        for c in rec["cotes"]:
            devs = [r.split(":")[0] for r in c["raccords"]]
            nums.update(c["numeros"])
            if devs and all(TERRAIN.match(d) or PORTE.match(d) for d in devs):
                ext.extend(c["raccords"])
            else:
                inte.extend(c["raccords"])
        rec["cote_armoire"] = sorted(set(inte))
        rec["cote_exterieur"] = sorted(set(ext))
        rec["numero_fil"] = "/".join(sorted(nums))

    cables = []
    for c in m["cables"]:
        ch = [x for x in c["champs"] if x]
        cables.append({"repere": c["nom"], "folio": num.get(c["folio"], c["folio"]),
                       "composition": ch[1] if len(ch) > 1 else "",
                       "designation": ch[2] if len(ch) > 2 else "", "brins": c["brins"]})
    appareils = sorted({s["nom"] for s in m["symboles"] if not s["nom"].startswith("X")})
    return {
        "source": os.path.relpath(path, DEPOT).replace("\\", "/"),
        "folios": {str(f["index"]): f["numero"] for f in m["folios"]},
        "bornes": dict(sorted(bornes.items())),
        "cables_schema": cables,
        "appareils": {a: {"designation": designation.get(a, ""), "reference": reference.get(a, "")}
                      for a in appareils},
    }


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else derniere_release()
    data = extraire(path)
    with open(os.path.join(ICI, "saisie.json"), encoding="utf-8") as f:
        data["saisie"] = json.load(f)
    with open(os.path.join(ICI, "donnees.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"{data['source']} : {len(data['bornes'])} bornes, {len(data['cables_schema'])} câbles -> donnees.json")


if __name__ == "__main__":
    main()
