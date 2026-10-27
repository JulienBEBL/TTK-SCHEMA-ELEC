"""Reconstruit outils/librairie/ (symboles .xsy utilisés par ttk_schema.py) à partir d'un .xrs déjà généré.

À utiliser uniquement quand la librairie WinRelais (sym_electrotech) n'est pas disponible
(session cloud). Chaque symbole du .xrs est une copie du .xsy ; on rejoue ttk_schema.py en
associant le N-ième appel de Gen.place au N-ième symbole du fichier source.
Usage : python reconstruire_librairie.py source.xrs
"""
import os, re, runpy, sys, tempfile
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import xrs_gen

src = sys.argv[1]
t = open(src, encoding="utf-8-sig").read().replace("\r\n", "\n")
blocks = [m.group(1).split("\n") for m in re.finditer(r"¤#Symbole·\d+¤\n(.*?)\n¤#FIN¤", t[t.index("¤#NombreSymbole¤"):], re.S)]
lib, count = {}, [0]
orig_place = xrs_gen.Gen.place

def place(self, xsy, rep, *a, **k):
    self._seq_block = blocks[count[0]]
    count[0] += 1
    lib.setdefault(xsy.replace("\\", "/"), self._seq_block)
    return orig_place(self, xsy, rep, *a, **k)

def load(self, path):
    return [l for l in self._seq_block]

xrs_gen.Gen.place = place
xrs_gen.Gen._load_xsy = load
tmp = os.path.join(tempfile.mkdtemp(), "x.xrs")
sys.argv = ["ttk_schema.py", tmp]
try:
    runpy.run_path(os.path.join(ICI, "ttk_schema.py"), run_name="__main__")
except SystemExit:
    pass
out = os.path.join(ICI, "librairie")
for path, blk in lib.items():
    # retire les sections que Gen ajoute ou ignore
    keep, skip = [], False
    for l in blk:
        if l.startswith("¤#"):
            skip = l in ("¤#RefBaseData¤", "¤#AuteurSymbole¤")
        if not skip:
            keep.append(l)
    full = os.path.join(out, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(keep + ["¤#FIN¤", ""]))
print(len(lib), "symboles écrits dans", out, "(appels place :", count[0], "/", len(blocks), ")")
