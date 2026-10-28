"""Aperçu PNG d'un folio d'un .xrs (contrôle visuel hors WinRelais, approximatif).
Usage : python apercu_xrs.py fichier.xrs numéro_de_folio [sortie.png]
Dessine fils, contours/arcs des symboles, champs texte visibles, textes libres, renvois (points).
"""
import re, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SEP = "·"
path, num = sys.argv[1], sys.argv[2]
out = sys.argv[3] if len(sys.argv) > 3 else f"folio_{num}.png"
t = open(path, encoding="utf-8-sig").read().replace("\r\n", "\n")
idx = None
for m in re.finditer(r"¤#Folio·(\d+)¤\n¤#Autre¤\n([^\n]*)\n", t):
    if m.group(2).split(SEP)[19] == num:
        idx = m.group(1)
if idx is None:
    sys.exit("folio inconnu")
fig, ax = plt.subplots(figsize=(16.5, 11.7))
ax.set_xlim(0, 29700); ax.set_ylim(21000, 0); ax.set_aspect("equal"); ax.axis("off")
ax.plot([1300, 29600, 29600, 1300, 1300], [1300, 1300, 19600, 19600, 1300], color="0.7", lw=0.5)
COL = {"Puissance": "k", "Neutre Puissance": "tab:blue", "Conducteur terre": "tab:green", "Commande 24VDC": "navy",
       "0V": "tab:cyan", "Autre tension DC": "orange"}
body = t[t.index("¤#FilBus¤"):]
sec = None
for l in body.split("\n"):
    if l.startswith("¤#"):
        sec = l; continue
    f = l.split(SEP)
    if sec == "¤#FilBus¤" and len(f) > 9 and f[4] == idx:
        ax.plot([int(f[0]), int(f[2])], [int(f[1]), int(f[3])], color=COL.get(f[9], "r"), lw=1.2)
    elif sec == "¤#Jonction¤" and len(f) > 3 and f[2] == idx:
        ax.plot([int(f[0])], [int(f[1])], "o", color="k", ms=3)
    elif sec == "¤#Numero¤" and len(f) > 7 and f[3] == idx:
        ax.text(int(f[0]) - 150, int(f[1]), f[2], fontsize=5, color="navy", rotation=int(f[7]), va="center", ha="center")
    elif sec == "¤#Texte¤" and len(f) > 9 and f[4] == idx:
        ax.text(int(f[0]), int(f[1]), f[2], fontsize=int(f[7]) / 55, va="top", color="firebrick" if f[9] == "255" else "k")
    elif sec == "¤#DSansTexte¤" and len(f) > 9 and f[5] == idx:
        x1, y1, x2, y2 = map(int, f[:4])
        if f[4] == "0":
            ax.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], color="0.5", lw=0.7, ls="--" if f[9] == "2" else "-")
        else:
            ax.plot([x1, x2], [y1, y2], color="0.4", lw=0.7)
    elif sec == "¤#RenvoiF¤" and len(f) > 11:
        for fo, x, y, tx in ((f[0], f[2], f[3], f[10]), (f[1], f[4], f[5], f[11])):
            if fo == idx:
                ax.plot([int(x)], [int(y)], "s", color="m", ms=4); ax.text(int(x) + 150, int(y), tx, fontsize=5, color="m", va="center")
sy = t[t.index("¤#NombreSymbole¤"):t.index("¤#FilBus¤")]
for m in re.finditer(r"¤#Symbole·\d+¤\n(.*?)¤#FIN¤", sy, re.S):
    L = m.group(1).split("\n")
    if L[2].split(SEP)[8] != idx:
        continue
    cur = None
    for k, l in enumerate(L):
        if 3 <= k < 11:
            c = l.split(SEP)
            if len(c) > 6 and c[3] == "1" and c[0]:
                ax.text(int(c[1]), int(c[2]), c[0], fontsize=int(c[6] or 200) / 55, va="top", color="darkgreen")
        if l.startswith("¤#"):
            cur = l; continue
        c = l.split(SEP)
        if cur == "¤#Contour¤" and len(c) > 3:
            ax.plot([int(c[0]), int(c[2])], [int(c[1]), int(c[3])], color="0.2", lw=0.8)
        elif cur == "¤#Arc¤" and len(c) > 2 and c[2]:
            ax.add_patch(plt.Circle((int(c[0]), int(c[1])), int(c[2]), fill=False, color="0.2", lw=0.8))
        elif cur == "¤#Broche¤" and len(c) > 2:
            ax.plot([int(c[1])], [int(c[2])], ".", color="r", ms=3)
for m in re.finditer(r"¤#DefCable·\d+¤\n¤#Autre¤\n(.*?)¤#FIN¤", t, re.S):
    L = m.group(1).split("\n")
    a = L[0].split(SEP)
    if a[0] != idx:
        continue
    ax.plot([int(a[1]), int(a[3])], [int(a[2]), int(a[4])], color="purple", lw=2)
    for l in L[4:11]:
        c = l.split(SEP)
        if len(c) > 6 and c[3] == "1" and c[0]:
            ax.text(int(c[1]), int(c[2]), c[0], fontsize=int(c[6]) / 55, va="top", color="purple")
fig.savefig(out, dpi=110, bbox_inches="tight")
print(out)
