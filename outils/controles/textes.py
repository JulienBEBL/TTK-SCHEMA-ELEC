"""Contrôle des folios hors 10-69 : textes qui se chevauchent, textes coupés par un trait ou un bord de cadre.
Usage : textes.py fichier.xrs folio[,folio]"""
import sys
sys.path.insert(0, r"C:\Users\Julien\Documents\10. TTK\TTK-SCHEMA-ELEC\outils")
import xrs_tool as T
from xrs_gen import largeur
P = sys.argv[1]
fols = sys.argv[2].split(",")
m = T.parse(P)
num = {f["index"]: f["numero"] for f in m["folios"]}
L = open(P, "rb").read().decode("utf-8-sig").replace("\r\n", "\n").split("\n")
i = L.index("¤#Texte¤") + 1
tx = []
while not L[i].startswith("¤#"):
    f = L[i].split("·")
    if f[2]:
        x, y, s, a = int(f[0]), int(f[1]), int(f[7]), int(f[8] or 0)
        w = largeur(f[2], s)
        box = (x, y - w, x + s, y) if a == 90 else (x, y, x + w, y + s)
        tx.append((int(f[4]), f[2], box))
    i += 1
i = L.index("¤#DSansTexte¤") + 1
segs = []
while not L[i].startswith("¤#"):
    f = L[i].split("·")
    x1, y1, x2, y2, forme, k = map(int, f[:6])
    if forme == 2:
        segs.append((k, (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))))
    else:
        for s_ in ((x1, y1, x2, y1), (x1, y2, x2, y2), (x1, y1, x1, y2), (x2, y1, x2, y2)):
            segs.append((k, (min(s_[0], s_[2]), min(s_[1], s_[3]), max(s_[0], s_[2]), max(s_[1], s_[3]))))
    i += 1
ov = lambda a, b: a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]
n = 0
for k in num:
    if num[k] not in fols:
        continue
    t_ = [t for t in tx if t[0] == k]
    for a in range(len(t_)):
        for b in range(a + 1, len(t_)):
            if ov(t_[a][2], t_[b][2]):
                print(f"f{num[k]} : textes « {t_[a][1][:30]} » x « {t_[b][1][:30]} »"); n += 1
        for kk, s in segs:
            if kk == k and ov(t_[a][2], (s[0] - 1, s[1] - 1, s[2] + 1, s[3] + 1)):
                print(f"f{num[k]} : texte « {t_[a][1][:30]} » coupé par un trait {s}"); n += 1
    for b_ in t_:
        if b_[2][0] < 1300 or b_[2][2] > 29600 or b_[2][1] < 1300 or b_[2][3] > 19600:
            print(f"f{num[k]} : texte hors zone « {b_[1][:30]} » {b_[2]}"); n += 1
print("textes : problèmes", n)
