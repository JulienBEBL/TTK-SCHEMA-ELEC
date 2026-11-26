# Script déjà appliqué (v42) : gardé pour mémoire. Ne pas relancer avec --ecrire sans relire le diff.
"""v42 : symbole MCX91A élargi (pas de 600 au lieu de 400 dans les groupes X5, X6, X10, X40, X20, X22, X23).
Positions relatives à la broche X1:PE (origine du symbole). Applique aux 3 copies, chacune dans son encodage."""
import sys
SEP = "\u00b7"
NOM = "SEW_Variateur_MCX91A-0055-5E3_CSO_CFN.xsy"
COPIES = [(r"C:\Users\Julien\Documents\10. TTK\TTK-SCHEMA-ELEC\outils\librairie\CUSTOM", "utf-8-sig"),
          (r"C:\Users\Julien\Documents\10. TTK\TTK-SCHEMA-ELEC\librairie_winrelais\sym_electrotech\CUSTOM", "cp1252"),
          (r"C:\Users\Public\Documents\Elec-CAO\sym_electrotech\CUSTOM", "cp1252")]
PIN = {"X5:24V": 3600, "X5:GND": 4200, "X40": 11400, "X41": 12000}
PIN.update({f"X6:{k}": 5000 + 600 * (k - 1) for k in range(1, 7)})
PIN.update({f"X10:{k}": 8800 + 600 * (k - 1) for k in range(1, 5)})
PIN.update({f"X20:{k}": 4800 + 600 * (k - 1) for k in range(1, 11)})
PIN.update({f"X22:{k}": 11000 + 600 * (k - 1) for k in range(1, 4)})
PIN.update({f"X23:{k}": 13000 + 600 * (k - 1) for k in range(1, 5)})
DESSIN = {"X6 STO": 4950, "X10": 8750, "PROFINET": 11250, "X22 relais": 10950, "X23 ana.": 12950,
          "X6:1=X6:3  X6:2=X6:4": 8600, "GND reliés au PE en interne": 8600}
DROITE_OLD, DROITE_NEW = 12400, 15200          # bord droit du cadre
CHAMPS_OLD, CHAMPS_NEW = 12700, 15500          # textes du repère et des champs

for dossier, enc in COPIES:
    p = dossier + "\\" + NOM
    raw = open(p, "rb").read()
    txt = raw.decode(enc)
    nl = "\r\n" if "\r\n" in txt else "\n"
    L = txt.split(nl)
    i_a = L.index("\u00a4#Autre\u00a4")
    ox = int(L[i_a + 1].split(SEP)[0])
    # origine = X1:PE dans la copie WinRelais ; décalage relu sur la broche X1:PE
    sec, n_ch = None, 0
    pe = next(int(l.split(SEP)[1]) for l in L if l.startswith("X1:PE" + SEP))
    out = []
    for l in L:
        if l.startswith("\u00a4#"):
            sec, n_ch = l, 0
            out.append(l)
            continue
        f = l.split(SEP)
        if sec == "\u00a4#Autre\u00a4":
            n_ch += 1
            if n_ch >= 3 and len(f) > 2 and f[1].lstrip("-").isdigit() and int(f[1]) - pe == CHAMPS_OLD:
                f[1] = str(pe + CHAMPS_NEW)
        elif sec == "\u00a4#Contour\u00a4" and len(f) > 4:
            for k in (0, 2):
                if int(f[k]) - pe == DROITE_OLD:
                    f[k] = str(pe + DROITE_NEW)
        elif sec == "\u00a4#Broche\u00a4" and f[0] in PIN:
            nx = pe + PIN[f[0]]
            f[1], f[3], f[5] = str(nx), str(nx), str(nx + 60)
        elif sec == "\u00a4#MDessin\u00a4" and len(f) > 5 and f[5] in DESSIN:
            f[1] = str(pe + DESSIN[f[5]])
        out.append(SEP.join(f))
    new = nl.join(out)
    if new == txt:
        print("inchangé", p)
        continue
    if "--ecrire" in sys.argv:
        data = new.encode(enc)
        open(p, "wb").write(data)
    import difflib
    print("==", p, enc, "origine", ox, "X1:PE", pe)
    for d in difflib.unified_diff(L, out, lineterm="", n=0):
        if not d.startswith(("---", "+++", "@@")):
            print("  ", d[:120])
