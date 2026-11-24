import sys
sys.path.insert(0, r"C:\Users\Julien\Documents\10. TTK\TTK-SCHEMA-ELEC\outils")
import xrs_tool as T
from collections import defaultdict
m = T.parse(sys.argv[1])
uf, _ = T.build_nets(m)
for s_ in m["symboles"]:            # alimentations : bornes +V / -V reliées en interne
    if s_["nom"] in ("T1", "T2", "T3"):
        for nom in ("+V", "-V"):
            bs = [b for b in s_["broches"] if b["nom"] == nom]
            for b in bs[1:]:
                uf.union(("B", s_["index"], nom, bs[0]["x"], bs[0]["y"]), ("B", s_["index"], nom, b["x"], b["y"]))
net = defaultdict(set)
for s_ in m["symboles"]:
    for b in s_["broches"]:
        net[f"{s_['nom']}:{b['nom']}"].add(uf.find(("B", s_["index"], b["nom"], b["x"], b["y"])))
def pot(p):
    r = net.get(p)
    if not r:
        return None
    return sorted(r)[0] if len(r) == 1 else tuple(sorted(r))
REF = {"24VELEC": "X21.11:E", "24VSEC": "X21.13:E", "24V capteurs": "X21.14:E", "0 V commun": "X21.12:E",
       "+48 V": "T3:+V", "0 V 48": "T3:-V"}
refpot = {k: pot(v) for k, v in REF.items()}
nom = {v: k for k, v in refpot.items()}
print("potentiels de référence distincts :", len(set(refpot.values())) == len(refpot))
attendu = {
    # drivers pas-à-pas : commande par la CPU, référence au 0 V commun ; puissance 48 V à part
    "U3:PUL+": "Q0.0", "U3:DIR+": "Q0.1", "U3:ENA+": "Q0.4", "U4:PUL+": "Q0.2", "U4:DIR+": "Q0.3", "U4:ENA+": "Q0.5",
    "U3:PUL-": "0 V commun", "U3:DIR-": "0 V commun", "U3:ENA-": "0 V commun",
    "U4:PUL-": "0 V commun", "U4:DIR-": "0 V commun", "U4:ENA-": "0 V commun",
    "U3:-V": "0 V 48", "U4:-V": "0 V 48",
    # CPU
    "K1:L+": "24VELEC", "K1:M": "0 V commun", "K1:1M": "0 V commun", "K1:2L+": "24VELEC", "K1:2M": "0 V commun",
    "K1:L+ capt": "24V capteurs",
    # SM 1223 / SM 1231
    "K2:L+": "24VELEC", "K2:M": "0 V commun", "K2:1M": "0 V commun", "K2:2M": "0 V commun", "K2:3L+": "24VSEC", "K2:3M": "0 V commun",
    "K3:L+": "24VELEC", "K3:M": "0 V commun",
    # variateurs, switch, IHM
    "U1:X5:24V": "24VELEC", "U1:X5:GND": "0 V commun", "U2:X5:24V": "24VELEC", "U2:X5:GND": "0 V commun",
    "U1:X6:2": "0 V commun", "K4:V1+": "24VELEC", "K4:V1-": "0 V commun", "P1:L+": "24VELEC", "P1:M": "0 V commun",
}
pb = 0
for p, att in attendu.items():
    if att.startswith("Q"):
        ok = pot(p) is not None and pot(p) == pot(f"K1:{att}")
        lu = att if ok else "?"
    else:
        lu = nom.get(pot(p), "autre")
        ok = lu == att
    if not ok:
        pb += 1
    print(f"{'OK ' if ok else 'ERR'} {p:12s} attendu {att:14s} lu {lu}")
# entrées CPU / SM 1223 : leur contact est-il alimenté par le 24 V capteurs (L+ capt) ?
print("entrées :")
for s_ in m["symboles"]:
    if s_["nom"] == "K1":
        for b in s_["broches"]:
            if b["nom"].startswith("I"):
                print("  ", b["nom"], "->", nom.get(pot(f"K1:{b['nom']}"), "signal"))
print("problèmes :", pb)
