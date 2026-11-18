"""Nomenclature TTK générée par le script (option B, Julien 18/11/2026).

Une ligne par appareil (repère), puis les bornes par type, le matériel non dessiné et les câbles.
- Appareils : lus dans les symboles posés (champs entiers, non coupés ; RefConstructeur).
- Bornes : symboles « borne » du schéma, classés par type d'après `implantation/generateur/saisie.json`
  (listes PT 4 et terre) ; PTFIX d'après le nom du symbole ; le reste en PT 2,5.
- Câbles : `saisie.json` (même source que le dossier d'implantation).
- Matériel non dessiné : table HORS_SCHEMA (sources : memoire/02_MATERIEL.md, 09_STOCK.md).

`controle(chemin)` relit le .xrs écrit et vérifie que la nomenclature n'a rien oublié (demande de Julien du 18/11).
"""
import json
import os
import re
from collections import Counter, defaultdict

import xrs_tool
from xrs_gen import largeur

ICI = os.path.dirname(os.path.abspath(__file__))
SAISIE = os.path.join(ICI, "..", "implantation", "generateur", "saisie.json")
SEP = "·"
TAILLE = 200          # hauteur des textes du tableau
LIGNE = 380           # hauteur d'une ligne (88 lignes sur 2 folios, 18/11)
X0, Y0 = 1200, 1400   # coin haut gauche du tableau
Y_MAX = 19300         # bas utile du folio (cartouche à 19700)
LARGEUR_MAX = 27800   # largeur utile (cadre 29022, marge gauche 1200)
ENTETE = ["Repère", "Désignation", "Marque et référence", "Caractéristiques", "Qté", "Loc.", "Folio"]
A_VERIFIER = "à vérifier"

# Bornes : désignation, marque et référence, source (memoire/09_STOCK.md, 17/11)
TYPES_BORNES = {
    "PT 2,5": ("Borne de passage PT 2,5", "Phoenix 3209510"),
    "PT 4": ("Borne de passage PT 4", "Phoenix 3211757"),
    "terre": ("Borne de terre vert/jaune", "Phoenix 3211867 (RS 708-1687)"),
    "PTFIX 6/12": ("Bloc de distribution PTFIX 6/12X2,5", "Phoenix 3273354"),
    "PTFIX 2X4": ("Bloc distributeur PTFIX 2X4 (bornes W11 / W12)", "Phoenix 1028361"),
}
CARAC_BORNES = {"PTFIX 2X4": "nombre de blocs : " + A_VERIFIER}   # Qté = nombre de bornes dessinées
# Matériel acheté mais non dessiné (memoire/02_MATERIEL.md, 09_STOCK.md) : repère, désignation, marque et réf.,
# caractéristiques, quantité, localisation
HORS_SCHEMA = [
    ("XR1", "Répartiteur 4P 125 A 7 départs (non dessiné)", "AEE300427", "", "1", "A1"),
    ("XR2", "Répartiteur 4P 125 A 7 départs (non dessiné)", "AEE300427", "", "1", "A1"),
    ("XPE1", "Bornier de terre 27 (non dessiné)", "Legrand 404839", "", "1", "A1"),
    ("", "Butées d'arrêt rail DIN", A_VERIFIER, "", A_VERIFIER, "A1"),
    ("+BJM", "Boîte de jonction machine (non achetée)", A_VERIFIER, "", "1", "M"),
]


def _naturel(s):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]


def _saisie():
    with open(SAISIE, encoding="utf-8") as fh:
        return json.load(fh)


# noms des symboles de borne du schéma (relevés le 18/11) ; un autre nom arrête le contrôle
SYMBOLES_BORNES = {"borne 4 mm": "passage", "borne 4 mm terre": "terre", "borne distribution ptfix 6/12x2.5": "PTFIX 6/12"}


def type_borne(rep, symbole, tb):
    nature = SYMBOLES_BORNES.get(symbole.lower(), "?")
    if nature in ("PTFIX 6/12", "terre"):
        return nature
    if rep in tb.get("PTFIX 2X4", ()):
        return "PTFIX 2X4"
    if rep in tb["PT 4"]:
        return "PT 4"
    return "PT 2,5"


def _champs_bloc(block):
    """(champs 1 à 8, RefConstructeur, localisation, drapeau borne, nom du symbole) lus dans le bloc."""
    ch = [block[3 + k].split(SEP)[0] for k in range(8)]
    info = block[2].split(SEP)
    ref = block[block.index("¤#RefConstructeur¤") + 1].split(SEP) + ["", "", ""]
    va = block.index("¤#VueArmoire¤") if "¤#VueArmoire¤" in block else -1
    loc = block[va + 1].split(SEP)[0] if va >= 0 else ""
    return ch, ref[:3], loc, info[11] == "1", info[2]


def lignes(g):
    """Lignes de la nomenclature [(famille, [7 textes])], famille = appareil / borne / hors / cable / titre."""
    par_rep = defaultdict(list)
    bornes = Counter()
    folios_bornes = defaultdict(set)
    tb = _saisie()["types_bornes"]
    for p in g.symbols:
        ch, ref, loc, est_borne, sym = _champs_bloc(p.block)
        rep = ch[0]
        if est_borne:
            t = type_borne(rep, sym, tb)
            bornes[t] += 1
            folios_bornes[t].add(g.num(p.folio))
            continue
        par_rep[rep].append((p, ch, ref, loc))
    out = [("titre", ["", "APPAREILS", "", "", "", "", ""])]
    for rep in sorted(par_rep, key=_naturel):
        syms = par_rep[rep]
        avec_ref = [s for s in syms if any(s[2])]
        avec_champs = [s for s in syms if s[0].champs_complets.get(3) or s[0].champs_complets.get(4)]
        p, ch, ref, loc = (avec_ref or avec_champs or syms)[0]
        cc = p.champs_complets
        des = cc.get(2, ch[1])
        marque = cc.get(3, "")
        if not marque or "définir" in marque:
            r = ref[1] or ref[2]
            marque = f"{ref[0]} {r}".strip() if (ref[0] or r) else A_VERIFIER
        carac = cc.get(4, "")
        folios = sorted({g.num(s[0].folio) for s in syms}, key=_naturel)
        out.append(("appareil", [rep, des, marque, carac, "1", loc, ", ".join(folios)]))
    out.append(("titre", ["", "BORNES ET MATERIEL NON DESSINE", "", "", "", "", ""]))
    for t in TYPES_BORNES:
        if bornes[t]:
            d, m = TYPES_BORNES[t]
            out.append(("borne", ["X", d, m, CARAC_BORNES.get(t, ""), str(bornes[t]), "A1",
                                  ", ".join(sorted(folios_bornes[t], key=_naturel))]))
    for rep, d, m, c, q, l in HORS_SCHEMA:
        out.append(("hors", [rep, d, m, c, q, l, "-"]))
    out.append(("titre", ["", "CABLES", "", "", "", "", ""]))
    for c in _saisie()["cables"]:
        dest = re.search(r"\+([A-Z0-9]+)", c["destination"])
        out.append(("cable", [c["repere"], c["fonction"], f"{c['type']} {c['reference']}".strip(),
                              c["conducteurs"], "1", dest.group(1) if dest else "", c["folio"]]))
    return out


def largeurs(rows):
    w = [max(largeur(r[k], TAILLE) for r in [ENTETE] + [x[1] for x in rows]) + 300 for k in range(7)]
    if sum(w) > LARGEUR_MAX:
        raise ValueError(f"nomenclature trop large : {sum(w)} > {LARGEUR_MAX} ({w})")
    return w


def dessiner(g, texte, folios, rows):
    """Tableau sur les folios donnés (index), en-tête répété sur chaque folio. Retourne le nb de lignes par folio."""
    w = largeurs(rows)
    par_folio = (Y_MAX - Y0) // LIGNE - 1
    paquets = [rows[i:i + par_folio] for i in range(0, len(rows), par_folio)]
    if len(paquets) > len(folios):
        raise ValueError(f"nomenclature : {len(rows)} lignes, {len(folios)} folios de {par_folio} lignes")
    for f, paquet in zip(folios, paquets):
        tab = [("entete", ENTETE)] + paquet
        W, H = sum(w), LIGNE * len(tab)
        g.cadre(f, X0, Y0, X0 + W, Y0 + H, width=20)
        for r in range(1, len(tab)):
            g.ligne(f, X0, Y0 + r * LIGNE, X0 + W, Y0 + r * LIGNE, width=20 if tab[r][0] == "titre" or r == 1 else 10)
        cx = X0
        for c in w[:-1]:
            cx += c
            g.ligne(f, cx, Y0, cx, Y0 + H, width=10)
        for r, (fam, row) in enumerate(tab):
            cx = X0
            for c, txt in zip(w, row):
                if txt:
                    texte(f, cx + 150, Y0 + r * LIGNE + (LIGNE - TAILLE) // 2, txt, TAILLE, 0,
                          1 if fam in ("entete", "titre") else 0)
                cx += c
    return [len(p) for p in paquets]


def controle(chemin, numeros_folios):
    """Relit le .xrs écrit : la nomenclature (folios affichés numeros_folios) n'a-t-elle rien oublié ?
    Retourne (problèmes, informations)."""
    m = xrs_tool.parse(chemin)
    idx = {f["index"] for f in m["folios"] if f["numero"] in numeros_folios}
    pb, infos = [], []
    # relecture du tableau : textes rangés par folio et par ligne, colonnes repérées par les x de l'en-tête
    par_ligne = defaultdict(list)
    for t in m["textes"]:
        if t["folio"] in idx:
            par_ligne[(t["folio"], t["y"])].append((t["x"], t["texte"]))
    tab = []
    for (f, y) in sorted(par_ligne, key=lambda k: (sorted(idx).index(k[0]), k[1])):
        tab.append((f, y, sorted(par_ligne[(f, y)])))
    entetes = [r for r in tab if [t for _, t in r[2]] == ENTETE]
    if len(entetes) != len(idx):
        pb.append(f"nomenclature : {len(entetes)} en-tête(s) pour {len(idx)} folio(s)")
    cols = {}
    for f, y, r in entetes:
        cols[f] = [x for x, _ in r]
    lignes_ = []
    for f, y, r in tab:
        if [t for _, t in r] == ENTETE or f not in cols:
            continue
        row = [""] * 7
        for x, t in r:
            k = max(i for i, cx in enumerate(cols[f]) if cx <= x + 1)
            row[k] = t
        lignes_.append(row)
    # 1. chaque appareil dessiné (symbole non borne) : exactement une ligne
    reps_schema = {s["nom"] for s in m["symboles"] if not s["borne"]}
    vus = Counter(r[0] for r in lignes_ if r[0])
    for rep in sorted(reps_schema, key=_naturel):
        if vus[rep] == 0:
            pb.append(f"nomenclature : appareil {rep} absent")
    hors = {h[0] for h in HORS_SCHEMA if h[0]}
    cables_saisie = {c["repere"] for c in _saisie()["cables"]}
    for rep, n in vus.items():
        if rep == "X":
            continue
        if n != 1:
            pb.append(f"nomenclature : {rep} sur {n} lignes (attendu 1)")
        if rep not in reps_schema and rep not in hors and rep not in cables_saisie:
            pb.append(f"nomenclature : {rep} n'existe ni au schéma, ni au matériel non dessiné, ni aux câbles")
    # 2. bornes : total et répartition par type, recalculés depuis le fichier
    tb = _saisie()["types_bornes"]
    attendu = Counter(type_borne(s["nom"], s["symbole"], tb) for s in m["symboles"] if s["borne"])
    lu = Counter()
    for r in lignes_:
        if r[0] == "X":
            t = next(k for k, v in TYPES_BORNES.items() if v[0] == r[1])
            lu[t] += int(r[4])
    if lu != attendu:
        pb.append(f"nomenclature : bornes {dict(lu)} au tableau, {dict(attendu)} au schéma")
    noms_bornes = {s["nom"] for s in m["symboles"] if s["borne"]}
    for t in ("PT 4", "terre", "PTFIX 2X4"):
        for rep in tb.get(t, ()):
            if rep not in noms_bornes:
                pb.append(f"nomenclature : borne {rep} ({t}, saisie.json) absente du schéma")
    for s_ in m["symboles"]:
        if s_["borne"]:
            nat = SYMBOLES_BORNES.get(s_["symbole"].lower())
            if nat is None:
                pb.append(f"nomenclature : borne {s_['nom']} : symbole « {s_['symbole']} » de type inconnu")
            if (nat == "terre") != (s_["nom"] in tb["terre"]):
                pb.append(f"nomenclature : borne {s_['nom']} : symbole de terre et liste terre de saisie.json en désaccord")
    for a_, b_ in (("PT 4", "terre"), ("PT 4", "PTFIX 2X4"), ("terre", "PTFIX 2X4")):
        for rep in set(tb.get(a_, ())) & set(tb.get(b_, ())):
            pb.append(f"nomenclature : borne {rep} à la fois {a_} et {b_} (saisie.json)")
    stock = []
    for t, n in sorted(lu.items()):
        achat = tb["achetes"].get(t)
        if achat is not None and n > achat:
            stock.append(f"{t} : {n} dessinées pour {achat} achetées")
    # 3. câbles : ceux du schéma (DefCable) et ceux de saisie.json
    for c in m["cables"]:
        if c["nom"] and vus[c["nom"]] == 0:
            pb.append(f"nomenclature : câble {c['nom']} du schéma absent")
    for rep in sorted(cables_saisie, key=_naturel):
        if vus[rep] == 0:
            pb.append(f"nomenclature : câble {rep} (saisie.json) absent")
    # 4. quantités : nombre entier pour les appareils et les câbles
    for r in lignes_:
        if r[0] and r[0] != "X" and r[4] not in ("1",) and r[4] != A_VERIFIER:
            pb.append(f"nomenclature : {r[0]} quantité « {r[4]} »")
    # 5. textes trop larges pour leur colonne
    for f, y, r in tab:
        xs = cols.get(f, [])
        for x, t in r:
            k = max(i for i, cx in enumerate(xs) if cx <= x + 1)
            fin = xs[k + 1] - 150 if k + 1 < len(xs) else None
            if fin and x + largeur(t, TAILLE) > fin:
                pb.append(f"nomenclature : « {t} » déborde de sa colonne")
    # informations : lignes à compléter
    for r in lignes_:
        if any(A_VERIFIER in c or "définir" in c for c in r):
            infos.append(f"{r[0] or '-'} {r[1]} : {' | '.join(c for c in r[2:4] if c)}")
    n_app = len({r[0] for r in lignes_ if r[0] in reps_schema})
    infos.insert(0, f"{len(lignes_)} lignes : {n_app} appareils dessinés, {sum(lu.values())} bornes "
                    f"({', '.join(f'{k} {v}' for k, v in sorted(lu.items()))}), "
                    f"{sum(1 for r in lignes_ if r[0] in cables_saisie)} câbles" + (" ; stock : " + " ; ".join(stock) if stock else "")
                    + " ; à compléter :")
    return pb, infos
