# Script déjà appliqué (v42) : gardé pour mémoire. Ne pas relancer avec --ecrire sans relire le diff.
"""v42 : Thermocouple_bas.xsy = « Contacts Capteurs\\Thermocouple.xsy » retourné haut / bas (broches en bas, fils vers le bas).
Symétrie y' = 6600 - y (broches 2800 -> 3800). Écrit dans les 3 dossiers CUSTOM (cp1252 + CRLF ; outils : UTF-8 + CRLF)."""
import sys
SEP = "\u00b7"
SRC = r"C:\Users\Public\Documents\Elec-CAO\sym_electrotech\Contacts Capteurs\Thermocouple.xsy"
DST = [(r"C:\Users\Julien\Documents\10. TTK\TTK-SCHEMA-ELEC\outils\librairie\CUSTOM", "utf-8"),
       (r"C:\Users\Julien\Documents\10. TTK\TTK-SCHEMA-ELEC\librairie_winrelais\sym_electrotech\CUSTOM", "cp1252"),
       (r"C:\Users\Public\Documents\Elec-CAO\sym_electrotech\CUSTOM", "cp1252")]
raw = open(SRC, "rb").read()
try:
    txt, enc0 = raw.decode("utf-8"), "utf-8"
except UnicodeDecodeError:
    txt, enc0 = raw.decode("cp1252"), "cp1252"
nl = "\r\n" if "\r\n" in txt else "\n"
L = txt.split(nl)
Y = lambda v: str(6600 - int(v))
out, sec, n_a = [], None, 0
for l in L:
    if l.startswith("\u00a4#"):
        sec, n_a = l, 0
        out.append(l)
        continue
    f = l.split(SEP)
    if sec == "\u00a4#Autre\u00a4":
        n_a += 1
        if n_a == 1:                              # origine : broche 1
            f[1] = Y(f[1])
        elif n_a == 2:
            f[2] = "thermocouple broches en bas"
        elif n_a == 3:                            # repère au-dessus de la pointe (centré)
            f[2] = "2350"
    elif sec == "\u00a4#Contour\u00a4" and len(f) > 4:
        f[1], f[3] = Y(f[1]), Y(f[3])
    elif sec == "\u00a4#Broche\u00a4" and len(f) > 6:
        f[2], f[4] = Y(f[2]), Y(f[4])
        f[6] = str(int(f[2]) - 250)               # nom de broche au-dessus du bout (côté symbole)
        f[18] = "1"                               # sens de la broche : fil vers le bas (comme les broches du bas)
    out.append(SEP.join(f))
new = nl.join(out)
if "--ecrire" in sys.argv:
    for d, enc in DST:
        open(d + "\\Thermocouple_bas.xsy", "wb").write(new.replace("\r\n", "\n").replace("\n", "\r\n").encode(enc))
print(enc0)
print(new.replace(SEP, "|"))
