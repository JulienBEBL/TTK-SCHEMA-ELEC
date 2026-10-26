#!/usr/bin/env python3
"""Analyse d'un schéma WinRelais .xrs (v2.6, UTF-8 BOM). Usage : python3 -I xrs_check.py fichier.xrs"""
import re, sys, math
from collections import Counter, defaultdict
t = open(sys.argv[1], encoding="utf-8-sig").read().replace("\r\n", "\n")

def block(name):
    m = re.search(r"¤#" + name + r"¤\n(.*?)(?=\n¤#)", t, re.S)
    return [l for l in m.group(1).split("\n") if l] if m else []

# Folios : index d'ordre -> numéro affiché, titre, description
num, folios = {}, []
for m in re.finditer(r"¤#Folio·(\d+)¤\n¤#Autre¤\n([^\n]*)\n(.*?)¤#FIN¤", t, re.S):
    k = int(m.group(1)); f = m.group(2).split("·"); seg = m.group(3)
    num[k] = f[19]
    ct = lambda key: (re.search(r"·([^·\n]*)·" + key + "·", seg) or [None, ""])[1]
    folios.append((f[19], f[10], ct("TITRE FOLIO"), ct("DESCRIPTION FOLIO")))

# Symboles
sy = t[t.index("¤#NombreSymbole¤"):]
syms, pins = [], []
for m in re.finditer(r"¤#Symbole·(\d+)¤\n(.*?)¤#FIN¤", sy, re.S):
    L = m.group(2).split("\n")
    o, h = L[1].split("·"), L[2].split("·")
    champs = [L[3 + i].split("·")[0] for i in range(4)]
    fo = int(h[8])
    rc = re.search(r"¤#RefCroise¤\n([^\n]*)", m.group(2))
    syms.append(dict(rep=champs[0], fct=champs[1], ref=champs[2], car=champs[3], folio=num[fo],
                     x=int(o[0]), y=int(o[1]), lib=h[2], refcroise=rc.group(1).split("·")[0] if rc else "?"))
    b = re.search(r"¤#Broche¤\n(.*?)\n¤#", m.group(2), re.S)
    if b:
        for l in b.group(1).split("\n"):
            p = l.split("·"); pins.append((fo, int(p[1]), int(p[2]), champs[0] + ":" + p[0]))

print("== FOLIOS"); [print(" ", *f, sep=" | ") for f in folios]
print("== SYMBOLES"); [print(f"  f{s['folio']} {s['rep']:6} {s['fct']} | {s['ref']} | {s['car']} | RefCroise={s['refcroise']}") for s in syms]

print("== REPERES EN DOUBLE")
for r, n in Counter(s["rep"] for s in syms).items():
    if n > 1: print("  ", r, n)

print("== HORS GRILLE 400 (origine)")
for s in syms:
    if s["x"] % 400 or s["y"] % 400: print(f"  f{s['folio']} {s['rep']} ({s['x']}, {s['y']})")

print("== FILS : extrémité non raccordée près d'une broche (<= 2 mm = ERREUR, 2-4 mm = en attente ?)")
types = defaultdict(Counter); ends = Counter(); segs = []
for l in block("FilBus"):
    f = l.split("·"); fo = int(f[4]); types[num[fo]][f[9]] += 1
    a, b = (fo, int(f[0]), int(f[1])), (fo, int(f[2]), int(f[3])); ends[a] += 1; ends[b] += 1; segs += [a, b]
pinset = {(fo, x, y) for fo, x, y, _ in pins}
for fo, x, y in segs:
    if ends[(fo, x, y)] > 1 or (fo, x, y) in pinset: continue
    d = [(math.hypot(x - px, y - py), n) for pf, px, py, n in pins if pf == fo]
    if d:
        dm, n = min(d)
        if dm <= 400: print(f"  {'ERREUR' if dm <= 200 else 'attente?'} f{num[fo]} ({x},{y}) -> {n} à {dm/100:.0f} mm")

print("== TYPES DE FIL PAR FOLIO"); [print(f"  f{k}", dict(v)) for k, v in sorted(types.items())]
print("== RENVOIS"); [print("  f" + num[int(l.split('·')[0])], "->", "f" + num[int(l.split('·')[1])], l.split("·")[10], l.split("·")[11]) for l in block("RenvoiF")]
print("== TEXTES LIBRES"); [print("  ", l.split("·")[2]) for l in block("Texte")]
