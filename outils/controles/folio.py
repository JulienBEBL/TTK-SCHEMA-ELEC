# v43 : lecture d'un folio par calcul (avant : script du scratchpad, v40)
"""Vue texte d'un folio (numéro affiché) : symboles (bbox), champs visibles, textes, câbles, cadres, renvois, numéros, fils.
Usage : python dump.py fichier.xrs 20 [sym|txt|cab|cad|ren|num|fil ...]"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import xrs_tool as T
P, F = sys.argv[1], sys.argv[2]
what = set(sys.argv[3:]) or {"sym", "txt", "cab", "cad", "ren", "num", "fil"}
m = T.parse(P)
idx = next(f["index"] for f in m["folios"] if f["numero"] == F)
L = open(P, "rb").read().decode("utf-8-sig").replace("\r\n", "\n").split("\n")
S = "\u00b7"
if "sym" in what:
    i = 0
    while i < len(L):
        if L[i].startswith("\u00a4#Symbole" + S):
            hdr = L[i + 3].split(S)
            if int(hdr[8]) == idx:
                j = i + 1; sec = None; xs = []; ys = []; ch = []; pins = []
                while L[j] != "\u00a4#FIN\u00a4":
                    if L[j].startswith("\u00a4#"):
                        sec = L[j]
                    else:
                        f = L[j].split(S)
                        if sec == "\u00a4#Contour\u00a4" and len(f) > 4:
                            xs += [int(f[0]), int(f[2])]; ys += [int(f[1]), int(f[3])]
                        if sec == "\u00a4#Arc\u00a4" and len(f) > 3:
                            xs += [int(f[0]) - int(f[2]), int(f[0]) + int(f[2])]; ys += [int(f[1]) - int(f[2]), int(f[1]) + int(f[2])]
                        if sec == "\u00a4#Broche\u00a4" and len(f) > 3:
                            pins.append(f"{f[0]}@{f[1]},{f[2]}")
                    j += 1
                rep = L[i + 4].split(S)[0]
                for k in range(i + 4, i + 12):
                    f = L[k].split(S)
                    if f[3] == "1" and f[0]:
                        ch.append(f"'{f[0]}'@{f[1]},{f[2]} s{f[6]} a{f[4]}")
                bb = (min(xs), min(ys), max(xs), max(ys)) if xs else None
                print(f"SYM {rep:10} {hdr[2][:30]:30} o={L[i+2].split(S)[0]},{L[i+2].split(S)[1]} bb={bb} ch={ch} pins={pins[:12]}")
            i = j if 'j' in dir() and j > i else i + 1
        else:
            i += 1
if "txt" in what:
    for t in m["textes"]:
        if t["folio"] == idx:
            print(f"TXT {t['x']},{t['y']} '{t['texte']}'")
    # lignes brutes texte pour taille / angle
if "cab" in what:
    i = 0
    while i < len(L):
        if L[i].startswith("\u00a4#DefCable") and int(L[i + 2].split(S)[0]) == idx:
            g = L[i + 2].split(S)
            print("CAB", L[i + 6].split(S)[:7], "trait", g[1:4], "| l7", L[i + 7].split(S)[:7], "| l8", L[i + 8].split(S)[:7])
        i += 1
if "cad" in what:
    i = L.index("\u00a4#DSansTexte\u00a4") + 1
    while not L[i].startswith("\u00a4#"):
        f = L[i].split(S)
        if len(f) > 5 and int(f[5]) == idx:
            print("DST", f[:14])
        i += 1
if "ren" in what:
    for r in m["renvois"]:
        if idx in (r["folioA"], r["folioB"]):
            print("REN", r)
if "num" in what:
    for n in m["numeros"]:
        if n["folio"] == idx:
            print(f"NUM {n['x']},{n['y']} {n['texte']}")
if "fil" in what:
    for w in m["fils"]:
        if w["folio"] == idx:
            print(f"FIL {w['x1']},{w['y1']} -> {w['x2']},{w['y2']} {w['type']}")
