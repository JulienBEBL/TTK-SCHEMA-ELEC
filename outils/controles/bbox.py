import sys, os
sys.path.insert(0, r"C:\Users\Julien\Documents\10. TTK\TTK-SCHEMA-ELEC\outils")
from xrs_edit import XrsDoc
base = r"C:\Users\Julien\Documents\10. TTK\TTK-SCHEMA-ELEC\outils\librairie"
for fn in sys.argv[1:]:
    p = fn if os.path.isabs(fn) else os.path.join(base, fn)
    L = XrsDoc(p).lines
    o = L[L.index("¤#Autre¤") + 1].split("·")
    xs, ys, sec, pins = [], [], None, []
    for l in L:
        if l.startswith("¤#"):
            sec = l; continue
        f = l.split("·")
        if sec == "¤#Contour¤":
            xs += [int(f[0]), int(f[2])]; ys += [int(f[1]), int(f[3])]
        if sec == "¤#Broche¤":
            pins.append((f[0], int(f[1]) - int(o[0]), int(f[2]) - int(o[1])))
    print(os.path.basename(fn)[:34], "bbox rel", min(xs) - int(o[0]), min(ys) - int(o[1]), max(xs) - int(o[0]), max(ys) - int(o[1]), pins[:14])
