"""Contrôle des numéros de fil d'un .xrs (13/11) : relit le fichier, rattache chaque numéro à son fil,
puis vérifie sur les équipotentielles (fils + renvois + bornes traversées) :
- un numéro <-> un seul potentiel, et un potentiel <-> un seul numéro ;
- sur les folios numérotés, chaque tronçon (hors PE) porte un numéro ;
- cohérence du chiffre des unités avec le type de fil (0V -> 0) ; câbles PROFINET repérés PN.
Usage : python xrs_numeros.py <fichier.xrs> <folios numérotés séparés par des virgules>"""
import sys
from collections import defaultdict
import xrs_tool as T

m = T.parse(sys.argv[1])
SEP = "·"
_L = open(sys.argv[1], "rb").read().decode("utf-8-sig").replace("\r\n", "\n").split("\n")
_i = _L.index("¤#Numero¤") + 1
_ang = {}
while not _L[_i].startswith("¤#"):
    _f = _L[_i].split(SEP)
    if len(_f) > 7:
        _ang[(int(_f[3]), int(_f[0]), int(_f[1]), _f[2])] = int(_f[7])
    _i += 1
folios = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else set()
num = {f["index"]: f["numero"] for f in m["folios"]}
uf, _ = T.build_nets(m)
for s_ in m["symboles"]:            # alimentations T1 à T3 : les 2 bornes +V (et -V) sont reliées en interne
    if s_["nom"] in ("T1", "T2", "T3"):
        for nom in ("+V", "-V"):
            bs = [b_ for b_ in s_["broches"] if b_["nom"] == nom]
            for b_ in bs[1:]:
                uf.union(("B", s_["index"], nom, bs[0]["x"], bs[0]["y"]), ("B", s_["index"], nom, b_["x"], b_["y"]))
hors = defaultdict(set)              # potentiels numérotés qui gardent un nom de phase sur un folio pas encore fait
pb = []


def fil_du_numero(n):
    """Fil le plus proche du numéro, dans son sens (16/11 : entre deux bornes rapprochées, le plus proche, pas le 1er)."""
    vert = _ang.get((n["folio"], n["x"], n["y"], n["texte"])) == 90
    best, d_best = None, 801
    for w in m["fils"]:
        if w["folio"] != n["folio"]:
            continue
        x1, x2, y1, y2 = min(w["x1"], w["x2"]), max(w["x1"], w["x2"]), min(w["y1"], w["y2"]), max(w["y1"], w["y2"])
        if vert and x1 == x2 and x1 in (n["x"], n["x"] + 300):     # v38 : « PE » du f12 écrit à gauche du fil (300)
            d = max(y1 - n["y"], n["y"] - y2, 0)
        elif not vert and y1 == y2 == n["y"]:
            d = max(x1 - n["x"], n["x"] - x2, 0)
        else:
            continue
        if d < d_best:
            best, d_best = w, d
    return best


par_num, par_pot, troncon_ok = defaultdict(set), defaultdict(set), set()
for n in m["numeros"]:
    w = fil_du_numero(n)
    if w is None:
        pb.append(f"f{num[n['folio']]} : numéro {n['texte']} en ({n['x']},{n['y']}) sur aucun fil")
        continue
    if n["texte"] == "PE":
        continue
    pot = uf.find(("P", w["folio"], w["x1"], w["y1"]))
    if num[n["folio"]] not in folios and not n["texte"].startswith("PN"):
        hors[pot].add((n["texte"], num[n["folio"]]))
        continue
    troncon_ok.add((w["folio"], w["x1"], w["y1"], w["x2"], w["y2"]))
    if n["texte"].startswith("PN"):
        if w["type"] != "Profinet":
            pb.append(f"f{num[n['folio']]} : {n['texte']} sur un fil {w['type']}")
        par_num["câble " + n["texte"]].add(pot)
        continue
    par_num[n["texte"]].add(pot)
    par_pot[pot].add(n["texte"])
    if w["type"] == "0V" and n["texte"].isdigit() and not n["texte"].endswith("0"):
        pb.append(f"f{num[n['folio']]} : {n['texte']} sur un fil 0V (unité attendue 0)")
for t, pots in par_num.items():
    if len(pots) > 1 and not t.startswith("câble"):
        pb.append(f"numéro {t} porté par {len(pots)} potentiels différents")
for pot, ts in par_pot.items():
    if len(ts) > 1:
        pb.append(f"un même potentiel porte plusieurs numéros : {sorted(ts)}")
# chaque tronçon (fils bout à bout, coupés par les symboles) des folios numérotés porte un numéro
pieds = defaultdict(int)
for s in m["symboles"]:
    for b in s["broches"]:
        pieds[(s["folio"], b["x"], b["y"])] += 1
fils = [w for w in m["fils"] if num[w["folio"]] in folios and w["type"] != "Conducteur terre"]
pere = {}


def r(k):
    while pere.setdefault(k, k) != k:
        k = pere[k]
    return k


for w in fils:
    a, b = (w["folio"], w["x1"], w["y1"]), (w["folio"], w["x2"], w["y2"])
    pere[r(a)] = r(b)
for w in fils:          # un fil qui aboutit au milieu d'un autre (piquage) est du même tronçon
    for o in fils:
        if o is not w and o["folio"] == w["folio"] and T.on_segment(w["x1"], w["y1"], o):
            pere[r((w["folio"], w["x1"], w["y1"]))] = r((o["folio"], o["x1"], o["y1"]))
        if o is not w and o["folio"] == w["folio"] and T.on_segment(w["x2"], w["y2"], o):
            pere[r((w["folio"], w["x2"], w["y2"]))] = r((o["folio"], o["x1"], o["y1"]))
groupes = defaultdict(list)
for w in fils:
    groupes[r((w["folio"], w["x1"], w["y1"]))].append(w)
# v37 (revue Krizox) : le câble client (tronçon qui arrive en haut des bornes d'arrivée X10.1x) n'est pas numéroté
client = {(s["folio"], b["x"], b["y"]) for s in m["symboles"] if s["nom"].startswith("X10.1") for b in s["broches"] if b["nom"] == "1"}
for ws in groupes.values():
    if any((w["folio"], w["x1"], w["y1"]) in client or (w["folio"], w["x2"], w["y2"]) in client for w in ws):
        continue
    if not any((w["folio"], w["x1"], w["y1"], w["x2"], w["y2"]) in troncon_ok for w in ws):
        w = ws[0]
        pb.append(f"f{num[w['folio']]} : tronçon {w['type']} sans numéro, ({w['x1']},{w['y1']})-({w['x2']},{w['y2']})")
for pot, ts in hors.items():
    if pot in par_pot:
        print(f"info : {sorted(par_pot[pot])[0]} continue sur un folio pas encore numéroté : {sorted(ts)}")
print(f"{len(m['numeros'])} numéros, {len(par_pot)} potentiels numérotés, {len(pb)} problème(s)")
for p in pb:
    print("-", p)
for t in sorted(k for k in par_num if k.startswith("câble")):
    print(t, ":", len(par_num[t]), "potentiel(s)")
