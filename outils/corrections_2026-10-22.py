"""Corrections du 22/10/2026 sur test_xrs_claude.xrs : symboles hors grille et fils non raccordés.

Index de folio (ordre - 1) : 4 = folio 10, 7 = folio 13, 10 = folio 30, 12 = folio 32, 18 = folio 52.
Le script s'arrête sans rien écrire si le fichier ne correspond pas à l'état attendu.
"""
import sys
from xrs_edit import XrsDoc

path = sys.argv[1] if len(sys.argv) > 1 else "../test_xrs_claude.xrs"
d = XrsDoc(path)

# --- 1. Symboles hors grille (grille 4 mm = 400)
# T7 et M3 sont 1 mm trop haut par rapport à T8 / M4 (même montage) : +100 en Y, fils compris.
d.move_symbol("T7", 0, 100, (15600, 8700))
d.move_symbol("M3", 0, 100, (14800, 14700))
d.move_wire_end(12, (15600, 8700), (15600, 5200), (15600, 8700), (15600, 8800), "T7:+V suit le symbole")
d.move_wire_end(12, (16400, 8700), (16400, 5900), (16400, 8700), (16400, 8800), "T7:-V suit le symbole")
for x in (14800, 15200, 16000, 16400):          # T7 A+/A-/B+/B- -> M3
    d.shift_wire(12, (x, 14700), (x, 11500), 0, 100, "liaison T7 -> M3 suit les symboles")
for y in (9100, 9500, 9900, 10300, 10700, 11100):  # attentes PUL/DIR/ENA de T7
    d.shift_wire(12, (12800, y), (13200, y), 0, 100, "attente commande T7 suit le symbole")
d.delete_wire(12, (13200, 9200), (13200, 9100), "fil parasite de 1 mm sur T7:PUL+")
# K4 / K5 (folio 52, encore sans fils) : alignés sur la grille, même écart entre eux.
d.move_symbol("K5", 100, 200, (9100, 8200))
d.move_symbol("K4", 0, 200, (9200, 13400))

# --- 2. Fils arrêtés à 1 mm d'une broche
d.move_wire_end(4, (12000, 14700), (12000, 14400), (12000, 14700), (12000, 14800), "raccordement F1:N")
d.move_wire_end(7, (19200, 13900), (19200, 10400), (19200, 13900), (19200, 14000), "raccordement G1:L")
d.move_wire_end(7, (22800, 13900), (22800, 8800), (22800, 13900), (22800, 14000), "raccordement G2:L")
for x, b in ((21600, "H1"), (22400, "H2"), (23200, "H3")):
    d.move_wire_end(4, (x, 5100), (x, 4400), (x, 5100), (x, 5200), f"raccordement T5:{b}")

# --- 3. Fil et renvois décalés de 1 mm
d.move_wire_end(12, (5600, 3100), (5600, 5600), (5600, 3100), (5600, 3200),
                "phase arrivant du folio 13 : départ sur le renvoi (5600,3200)")
d.move_renvoi_point(4, 5, "A", (28000, 19100), (28000, 19200), "renvoi PE folio 10 -> 11 sur l'extrémité du fil PE")
d.move_renvoi_point(10, 12, "A", (28500, 18800), (28400, 18800), "renvoi PE folio 30 -> 32 sur l'extrémité du fil PE")

d.save()
last = None
for n, why, old, new in d.log:
    if why != last:
        print(f"\n# {why}")
        last = why
    print(f"  L{n}: {old[:70]}\n     -> {new[:70]}")
print(f"\n{len(d.log)} lignes modifiées -> {path}")
