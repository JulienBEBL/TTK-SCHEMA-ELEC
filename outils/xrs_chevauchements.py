"""Contrôle par calcul des chevauchements sur un .xrs : numéros de fil et de brin, textes de câble, textes libres,
champs de symbole, renvois, fils. Usage : python xrs_chevauchements.py <fichier.xrs> [numéros de folio].
Tailles de texte estimées (0,55 x hauteur par caractère). Le fichier n'est jamais modifié."""
import sys
import xrs_tool as T
from xrs_gen import RENVOI_L, RENVOI_W
SEP = "\u00b7"
P = sys.argv[1]
m = T.parse(P)
L = open(P, "rb").read().decode("utf-8-sig").replace("\r\n", "\n").split("\n")
num = {f["index"]: f["numero"] for f in m["folios"]}
box = {k: [] for k in num}
W = lambda t, s: int(len(t) * s * 0.55)
# numéros de fil
i = L.index("\u00a4#Numero\u00a4") + 1
while not L[i].startswith("\u00a4#"):
    f = L[i].split(SEP)
    if len(f) > 7:
        x, y, t, k, s, a = int(f[0]), int(f[1]), f[2], int(f[3]), int(f[6]), int(f[7])
        box[k].append(("fil " + t, (x, y - W(t, s), x + s, y) if a == 90 else (x, y, x + W(t, s), y + s)))
    i += 1
# textes libres
for t in m["textes"]:
    if t.get("texte"):
        s = t.get("taille", 200) or 200
        box[t["folio"]].append(("txt " + t["texte"][:28], (t["x"], t["y"], t["x"] + W(t["texte"], s), t["y"] + s)))
# champs visibles
i = 0
while i < len(L):
    if L[i].startswith("\u00a4#Symbole" + SEP):
        k = int(L[i + 3].split(SEP)[8])
        rep = L[i + 4].split(SEP)[0]
        for j in range(i + 4, i + 12):
            f = L[j].split(SEP)
            if f[3] == "1" and f[0]:
                s = int(f[6] or 300)
                x = int(f[1]) - (W(f[0], s) // 2 if f[4] == "6" else 0)
                box[k].append((f"{rep}:{f[0][:24]}", (x, int(f[2]), x + W(f[0], s), int(f[2]) + s)))
        i += 12
    elif L[i].startswith("\u00a4#DefCable"):
        k = int(L[i + 2].split(SEP)[0])
        rep = L[i + 6].split(SEP)[0]
        for j in (6, 7, 8):
            f = L[i + j].split(SEP)
            if f[0]:
                s = int(f[6] or 200)
                box[k].append((f"cable {rep}:{f[0][:24]}", (int(f[1]), int(f[2]), int(f[1]) + W(f[0], s), int(f[2]) + s)))
        j = i + 9
        while not L[j].startswith("\u00a4#BrinCable"):
            j += 1
        j += 4
        while L[j].count(SEP) == 4 and not L[j].startswith("\u00a4"):
            f = L[j].split(SEP)
            box[k].append((f"brin {rep}.{f[2]}", (int(f[0]), int(f[1]) - 300, int(f[0]) + 170, int(f[1]))))
            j += 1
        i = j
    else:
        i += 1
# renvois
def dirs(k, x, y):
    for w in m["fils"]:
        if w["folio"] == k:
            if (w["x1"], w["y1"]) == (x, y): return (w["x2"] - x, w["y2"] - y)
            if (w["x2"], w["y2"]) == (x, y): return (w["x1"] - x, w["y1"] - y)
    return (0, 1)
for r in m["renvois"]:
    for k, x, y, t in ((r["folioA"], r["xA"], r["yA"], r["texteA"]), (r["folioB"], r["xB"], r["yB"], r["texteB"])):
        d = dirs(k, x, y)
        if d[0] > 0: b = (x - RENVOI_L, y - RENVOI_W, x, y + RENVOI_W)
        elif d[0] < 0: b = (x, y - RENVOI_W, x + RENVOI_L, y + RENVOI_W)
        elif d[1] > 0: b = (x - RENVOI_W, y - RENVOI_L, x + RENVOI_W, y)
        else: b = (x - RENVOI_W, y, x + RENVOI_W, y + RENVOI_L)
        box[k].append((f"renvoi {t}@{x},{y}", b))
ov = lambda a, b: a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]
only = sys.argv[2:]
tot = 0
for k, lst in box.items():
    if only and num[k] not in only:
        continue
    if not "10" <= num[k] <= "69":
        continue
    out = []
    for a in range(len(lst)):
        for b in range(a + 1, len(lst)):
            if ov(lst[a][1], lst[b][1]):
                out.append(f"  {lst[a][0]} x {lst[b][0]}")
    # textes traversés par un fil
    for n, b in lst:
        if n.startswith(("renvoi",)):
            continue
        for w in m["fils"]:
            if w["folio"] != k:
                continue
            seg = (min(w["x1"], w["x2"]) - 1, min(w["y1"], w["y2"]) - 1, max(w["x1"], w["x2"]) + 1, max(w["y1"], w["y2"]) + 1)
            if ov(b, seg):
                if n.startswith("fil ") and (w["x1"] == b[0] or w["y1"] == b[1]):
                    continue
                if n.startswith("brin"):
                    continue
                out.append(f"  {n} traversé par fil {(w['x1'], w['y1'])}-{(w['x2'], w['y2'])}")
                break
    # renvois / fils des autres : renvoi traversé
    if out:
        print(f"--- f{num[k]} : {len(out)}")
        print("\n".join(out))
        tot += len(out)
print("total", tot)
