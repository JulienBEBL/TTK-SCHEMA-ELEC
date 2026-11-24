import sys, json, re, collections
sys.path.insert(0, r"C:\Users\Julien\Documents\10. TTK\TTK-SCHEMA-ELEC\outils")
L = open(sys.argv[1], encoding="utf-8-sig").read().replace("\r\n", "\n").split("\n")
import xrs_tool as T
m = T.parse(sys.argv[1]); num = {f["index"]: f["numero"] for f in m["folios"]}
bornes = []
for i, l in enumerate(L):
    if l.startswith("¤#Symbole·"):
        rep = L[i + 4].split("·")[0]; k = int(L[i + 3].split("·")[8]); typ = L[i + 2]
        if re.match(r"^X[0-9A-Z]*\.\d+$", rep) and "ptfix" not in typ.lower():
            bornes.append((rep, num[k]))
c = collections.Counter(r for r, _ in bornes)
print("bornes :", len(bornes), "| doublons :", [r for r, n in c.items() if n > 1])
regle = [(r, f) for r, f in bornes if r.split(".")[0] not in ("X1", "XPE1") and r.split(".")[0][1:] != f]
print("hors règle X + folio :", regle)
s = json.load(open(r"C:\Users\Julien\Documents\10. TTK\TTK-SCHEMA-ELEC\implantation\generateur\saisie.json", encoding="utf-8"))
txt = json.dumps(s, ensure_ascii=False)
js = set(re.findall(r'"(X\d+\.\d+)"', txt))
sch = {r for r, _ in bornes}
print("saisie sans schéma :", sorted(js - sch - {r for r in js if r.startswith("X1.")}))
print("schéma sans saisie (hors boîte X1) :", sorted(r for r in sch - js if not r.startswith("X1.")))
nb = collections.defaultdict(list)
for r, f in bornes: nb[r.split(".")[0]].append(int(r.split(".")[1]))
for b in sorted(nb): print(b, sorted(nb[b]))
