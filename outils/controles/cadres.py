import sys
sys.path.insert(0, r"C:\Users\Julien\Documents\10. TTK\TTK-SCHEMA-ELEC\outils")
import xrs_tool as T
from xrs_gen import largeur
P = sys.argv[1]
m = T.parse(P)
num = {f["index"]: f["numero"] for f in m["folios"]}
L = open(P, "rb").read().decode("utf-8-sig").replace("\r\n", "\n").split("\n")
i = L.index("¤#DSansTexte¤") + 1
cad = {}
while not L[i].startswith("¤#"):
    f = L[i].split("·")
    if f[4] == "0" and f[9] == "2":
        x1, y1, x2, y2 = sorted((int(f[0]), int(f[2])))[0], sorted((int(f[1]), int(f[3])))[0], max(int(f[0]), int(f[2])), max(int(f[1]), int(f[3]))
        cad.setdefault(int(f[5]), []).append((x1, y1, x2, y2))
    i += 1
pb = 0
for k, lst in cad.items():
    for a in range(len(lst)):
        for b in range(a + 1, len(lst)):
            A, B = lst[a], lst[b]
            inter = A[0] < B[2] and B[0] < A[2] and A[1] < B[3] and B[1] < A[3]
            cont = (A[0] <= B[0] and A[1] <= B[1] and A[2] >= B[2] and A[3] >= B[3]) or (B[0] <= A[0] and B[1] <= A[1] and B[2] >= A[2] and B[3] >= A[3])
            if inter and not cont:
                print(f"f{num[k]} : cadres qui se croisent {A} {B}"); pb += 1
    # symboles coupés par un cadre (bord qui traverse le contour du symbole)
    for s in m["symboles"]:
        if s["folio"] != k or s["borne"]:
            continue
        for c in lst:
            for b in s["broches"]:
                pass
    # cadre hors zone
    for c in lst:
        if c[0] < 1300 or c[1] < 1300 or c[2] > 29600 or c[3] > 19600:
            print(f"f{num[k]} : cadre hors zone {c}"); pb += 1
print("cadres pointillés :", sum(len(v) for v in cad.values()), "problèmes :", pb)
