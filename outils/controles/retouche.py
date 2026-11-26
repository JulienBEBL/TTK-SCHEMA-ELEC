"""v43 : compare deux .xrs (release générée et release réenregistrée par WinRelais) : fils, textes, numéros, renvois,
jonctions, symboles, câbles, folios. Usage : python retouche.py generee.xrs ouverte_WinRelais.xrs
Les positions des textes de câble ne sont pas comparées ici : comparer aussi les blocs ¤#DefCable (W1, W9, W10 en v43)."""
import os
import sys
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import xrs_tool as t

a = t.parse(sys.argv[1])
b = t.parse(sys.argv[2])


def key_sym(s):
    return tuple(sorted((k, str(v)) for k, v in s.items() if k not in ("index", "ligne")))


for nm, kf in [("fils", lambda f: (f["x1"], f["y1"], f["x2"], f["y2"], f["folio"], f["couleur"], f["epaisseur"])),
               ("textes", lambda f: (f["x"], f["y"], f["texte"], f["folio"])),
               ("numeros", lambda f: (f["x"], f["y"], f["texte"], f["folio"])),
               ("renvois", lambda f: (f["folioA"], f["folioB"], f["xA"], f["yA"], f["xB"], f["yB"])),
               ("jonctions", lambda f: (f["x"], f["y"], f["folio"])),
               ("symboles", key_sym),
               ("cables", lambda c: (c["folio"], c["nom"], tuple(c["champs"]), c["brins"]))]:
    ca, cb = Counter(map(kf, a[nm])), Counter(map(kf, b[nm]))
    # fils : normaliser le sens
    if nm == "fils":
        n = lambda k: (min(k[:2], k[2:4]) + max(k[:2], k[2:4]) + k[4:])
        ca, cb = Counter(n(k) for k in ca.elements()), Counter(n(k) for k in cb.elements())
    print(nm, len(a[nm]), len(b[nm]), "seulement A:", sum((ca - cb).values()), "seulement B:", sum((cb - ca).values()))
    for k in list((ca - cb))[:8]:
        print("  A", str(k)[:200])
    for k in list((cb - ca))[:8]:
        print("  B", str(k)[:200])
fa = [(f["nom"], f["numero"], f["titre"], f["description"]) for f in a["folios"]]
fb = [(f["nom"], f["numero"], f["titre"], f["description"]) for f in b["folios"]]
print("folios identiques:", fa == fb)
