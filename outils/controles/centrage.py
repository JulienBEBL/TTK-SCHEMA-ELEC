# v42 : mesure du centrage des numéros de fil (règle de Julien du 26/11)
"""Écart (le long des fils) entre le centre de chaque numéro et le milieu de son tronçon (fils bout à bout, coupés par les
broches de symbole). Usage : centrage.py fichier.xrs [seuil]"""
import os
import sys
import heapq
from collections import defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import xrs_tool as T
from xrs_gen import largeur
P = sys.argv[1]
SEUIL = int(sys.argv[2]) if len(sys.argv) > 2 else 600
m = T.parse(P)
num = {f["index"]: f["numero"] for f in m["folios"]}
L = open(P, "rb").read().decode("utf-8-sig").replace("\r\n", "\n").split("\n")
i = L.index("¤#Numero¤") + 1
nums = []
while not L[i].startswith("¤#"):
    f = L[i].split("·")
    if len(f) > 7:
        nums.append((int(f[3]), int(f[0]), int(f[1]), f[2], int(f[7]), int(f[6])))
    i += 1
pins = defaultdict(set)
for s in m["symboles"]:
    for b in s["broches"]:
        pins[s["folio"]].add((b["x"], b["y"]))
adj = defaultdict(lambda: defaultdict(list))
for w in m["fils"]:
    a, b = (w["x1"], w["y1"]), (w["x2"], w["y2"])
    d = abs(a[0] - b[0]) + abs(a[1] - b[1])
    adj[w["folio"]][a].append((b, d))
    adj[w["folio"]][b].append((a, d))


def comp(fo, start):
    """composante : on ne traverse pas une broche de symbole"""
    seen, st = {start}, [start]
    while st:
        n = st.pop()
        if n in pins[fo] and n != start:
            continue
        for mm, _ in adj[fo][n]:
            if mm not in seen:
                seen.add(mm)
                st.append(mm)
    return seen


def dij(fo, nodes, src):
    dist, prev, pq = {src: 0}, {}, [(0, src)]
    while pq:
        d, n = heapq.heappop(pq)
        if d > dist[n]:
            continue
        for mm, l in adj[fo][n]:
            if mm in nodes and d + l < dist.get(mm, 1e18):
                dist[mm], prev[mm] = d + l, n
                heapq.heappush(pq, (d + l, mm))
    return dist, prev


tot, gros = 0, []
for fo, x, y, t, ang, s in nums:
    if not "10" <= num[fo] <= "69":
        continue
    lg = largeur(t, s)
    cx, cy = (x + s // 2, y - lg // 2) if ang == 90 else (x + lg // 2, y)
    px, py = (x, cy) if ang == 90 else (cx, y)          # point du fil au centre du texte
    # fil porteur
    w = next((w for w in m["fils"] if w["folio"] == fo and ((ang == 90 and w["x1"] == w["x2"] == px and min(w["y1"], w["y2"]) <= py <= max(w["y1"], w["y2"]))
                                                           or (ang == 0 and w["y1"] == w["y2"] == py and min(w["x1"], w["x2"]) <= px <= max(w["x1"], w["x2"])))), None)
    if w is None:
        continue
    nodes = comp(fo, (w["x1"], w["y1"])) | comp(fo, (w["x2"], w["y2"]))
    n0 = next(iter(nodes))
    d1, _ = dij(fo, nodes, n0)
    a = max(d1, key=d1.get)
    d2, prev = dij(fo, nodes, a)
    b = max(d2, key=d2.get)
    tot_l = d2[b]
    da, _ = dij(fo, nodes, a)
    # position du numéro le long du chemin : distance depuis a via les extrémités de son fil
    e1, e2 = (w["x1"], w["y1"]), (w["x2"], w["y2"])
    pos = min(da.get(e1, 1e18) + abs(px - e1[0]) + abs(py - e1[1]), da.get(e2, 1e18) + abs(px - e2[0]) + abs(py - e2[1]))
    ecart = abs(pos - tot_l / 2)
    tot += 1
    if ecart > SEUIL:
        gros.append((num[fo], t, int(ecart), tot_l))
print(f"{tot} numéros mesurés, {len(gros)} à plus de {SEUIL} du milieu de leur tronçon")
for g in sorted(gros)[:int(sys.argv[3]) if len(sys.argv) > 3 else 0]:
    print("  f%s %s écart %d (tronçon %d)" % g)
