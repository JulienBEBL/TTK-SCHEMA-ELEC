"""v41 (25/11) : contrôle des symboles CUSTOM.
- La copie du dépôt `librairie_winrelais/sym_electrotech/CUSTOM` et celle du PC (`C:\\Users\\Public\\...\\CUSTOM`, lue par
  le script via TTK_LIB) sont identiques octet pour octet. (`outils/librairie/CUSTOM` a un autre format pour certains
  symboles : bloc brut en UTF-8 ; elle n'est pas comparée.)
- Traits de contour au bon format dans les 3 dossiers : 10 champs, épaisseur de 10 à 60, style 0 (plein) ou 1 (pointillé).
Origine : en v40, une retouche du contour moteur avait écrit une épaisseur de 200 (trait très épais dans WinRelais)."""
import glob
import os

R = r"C:\Users\Julien\Documents\10. TTK\TTK-SCHEMA-ELEC"
DEPOT = os.path.join(R, "librairie_winrelais", "sym_electrotech", "CUSTOM")
PC = r"C:\Users\Public\Documents\Elec-CAO\sym_electrotech\CUSTOM"
OUTILS = os.path.join(R, "outils", "librairie", "CUSTOM")


def lignes(raw):
    try:
        s_ = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        s_ = raw.decode("cp1252")
    return s_.replace("\r\n", "\n").split("\n")


pb = 0
noms = sorted({os.path.basename(p) for d in (DEPOT, PC) for p in glob.glob(os.path.join(d, "*.xsy"))})
for n in noms:
    a, b = os.path.join(DEPOT, n), os.path.join(PC, n)
    if not (os.path.exists(a) and os.path.exists(b)) or open(a, "rb").read() != open(b, "rb").read():
        print(f"{n} : copies du dépôt et du PC différentes (ou absente)")
        pb += 1
for d in (DEPOT, PC, OUTILS):
    for p in glob.glob(os.path.join(d, "*.xsy")):
        sec = None
        for l in lignes(open(p, "rb").read()):
            if l.startswith("\u00a4#"):
                sec = l
                continue
            if sec == "\u00a4#Contour\u00a4" and l:
                f = l.split("\u00b7")
                if len(f) != 10 or not 10 <= int(f[4] or 0) <= 60 or f[5] not in ("0", "1"):
                    print(f"{os.path.basename(p)} ({os.path.basename(os.path.dirname(os.path.dirname(p)))}) : contour anormal « {l} »")
                    pb += 1
print(f"symboles CUSTOM : {len(noms)} | problèmes : {pb}")
