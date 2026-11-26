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
# zone utile du folio : cadre repère A..N (x 1300 à 29300) et 1..9 (y 1300 à 19300), marge de 200 (v33, 18/11)
ZONE = (1500, 1500, 29100, 19100)
TAILLES = (300, 280, 260, 250, 240, 220, 200)   # plus grande taille qui tient en largeur (Julien : police plus grande)
TAILLE_FOLIO = {}     # index du folio -> taille retenue au dessin (relue par le contrôle)
ENTETE = ["Repère", "Désignation", "Marque et référence", "Caractéristiques", "Qté", "Loc.", "Folio"]
ENTETE_CABLES = ["Repère", "Fonction", "Origine", "Destination", "Type et référence", "Conducteurs", "Folio"]
A_VERIFIER = "à vérifier"

# Bornes : désignation, marque et référence, source (memoire/09_STOCK.md, 17/11)
TYPES_BORNES = {
    "PT 2,5": ("Borne de passage PT 2,5", "Phoenix 3209510"),
    "PT 4": ("Borne de passage PT 4", "Phoenix 3211757"),
    "terre": ("Borne de terre vert/jaune", "Phoenix 3211867 (RS 708-1687)"),
    "PTFIX 6/12": ("Bloc de distribution PTFIX 6/12X2,5", "Phoenix 3273354"),
    "PTFIX 2X4": ("Bloc distributeur PTFIX 2X4 (bornes W11 / W12)", "Phoenix 1028361"),
    # v37 (revue Krizox, D08) : bornier de la boîte de jonction machine +BJM-X1 (boîte fabriquée par BEBL, bornes à choisir)
    "BJM": ("Borne de passage, boîte +BJM", A_VERIFIER),
    "BJM terre": ("Borne de terre, boîte +BJM", A_VERIFIER),
}
LOC_BORNES = {"BJM": "BJM", "BJM terre": "BJM"}     # les autres bornes sont dans l'armoire (A1)
CARAC_BORNES = {"PTFIX 2X4": "2 trous - 6 mm"}   # Julien 18/11   # Qté = nombre de bornes dessinées
# Matériel acheté mais non dessiné (memoire/02_MATERIEL.md, 09_STOCK.md) : repère, désignation, marque et réf.,
# caractéristiques, quantité, localisation
HORS_SCHEMA = [
    ("XR1", "Répartiteur 4P 125 A 7 départs (non dessiné)", "AEE300427", "", "1", "A1"),
    ("XR2", "Répartiteur 4P 125 A 7 départs (non dessiné)", "AEE300427", "", "1", "A1"),
    ("XPE1", "Bornier de terre 27 (non dessiné)", "Legrand 404839", "", "1", "A1"),
    ("", "Butées d'arrêt rail DIN", A_VERIFIER, "", A_VERIFIER, "A1"),
    ("+BJM", "Boîte de jonction machine (fabrication BEBL)", "BEBL", "", "1", "M"),     # v43 : « Julien 23/11 » retiré
]


def _naturel(s):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]


def _saisie():
    with open(SAISIE, encoding="utf-8") as fh:
        return json.load(fh)


# noms des symboles de borne du schéma (relevés le 18/11) ; un autre nom arrête le contrôle
SYMBOLES_BORNES = {"borne 4 mm": "passage", "borne 4 mm terre": "terre", "borne distribution ptfix 6/12x2.5": "PTFIX 6/12"}


def est_bjm(rep):
    """Borne de la boîte +BJM (bornier X1, v37)."""
    return rep.startswith("X1.")


def type_borne(rep, symbole, tb):
    nature = SYMBOLES_BORNES.get(symbole.lower(), "?")
    if est_bjm(rep):
        return "BJM terre" if nature == "terre" else "BJM"
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


def _cable(c, schema):
    """v42 : folio(s) et origine relus sur le schéma (schema = {repère : {folio, origine}}) ; saisie.json sinon."""
    s = (schema or {}).get(c["repere"], {})
    return s.get("folio") or c["folio"], s.get("origine") or c["origine"]


def lignes(g, schema=None):
    """Lignes de la nomenclature [(famille, [7 textes])], famille = appareil / borne / hors / cable / titre.
    schema (v42) : folios et origines des câbles relus sur le dessin (saisie.json gardait ceux d'avant la v37)."""
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
            out.append(("borne", ["X", d, m, CARAC_BORNES.get(t, ""), str(bornes[t]), LOC_BORNES.get(t, "A1"),
                                  ", ".join(sorted(folios_bornes[t], key=_naturel))]))
    for rep, d, m, c, q, l in HORS_SCHEMA:
        out.append(("hors", [rep, d, m, c, q, l, "-"]))
    out.append(("titre", ["", "CABLES", "", "", "", "", ""]))
    for c in _saisie()["cables"]:
        dest = re.search(r"\+([A-Z0-9]+)", c["destination"])
        lieu = {"BJM": "M"}.get(dest.group(1), dest.group(1)) if dest else ""
        # v43 : « broches » abrégé (largeur de colonne, police plus grande)
        out.append(("cable", [c["repere"], c["fonction"], f"{c['type']} {c['reference']}".strip().replace(" broches ", " br. "),
                              c["conducteurs"], "1", lieu, _cable(c, schema)[0]]))
    return out


def lignes_cables(schema=None):
    """Liste des câbles (f80, v33) : saisie.json, une ligne par câble ; folio et origine relus sur le schéma (v42)."""
    return [("cable", [c["repere"], c["fonction"], _cable(c, schema)[1], c["destination"],
                       f"{c['type']} {c['reference']}".strip(), c["conducteurs"], _cable(c, schema)[0]])
            for c in _saisie()["cables"]]


def _coupe(txt):
    """Texte coupé en 2 lignes à l'espace le plus proche du milieu (v40, f80) ; [txt] si pas d'espace."""
    esp = [i for i, c in enumerate(txt) if c == " "]
    if not esp:
        return [txt]
    i = min(esp, key=lambda k: abs(k - len(txt) / 2))
    return [txt[:i], txt[i + 1:]]


def tableau_pages(g, texte, folios, entete, rows, ligne_max=900, tailles=TAILLES, coupe=False, marge=1.0):
    """Tableau centré sur toute la zone utile des folios (index), en-tête sur chaque folio, lignes réparties
    également. Taille de texte = la plus grande de TAILLES qui tient en largeur ; colonnes élargies au prorata
    du contenu jusqu'à la largeur utile. Retourne (taille, hauteur de ligne, lignes par folio).
    coupe=True (v40, f80, Julien 25/11 : police plus grande) : une colonne trop large passe sur 2 lignes
    (les plus larges d'abord) ; la hauteur de ligne suit (2 lignes de texte).
    marge (v43) : blanc total d'une colonne, en fraction de la taille du texte (1.0 avant ; 0.6 pour la nomenclature,
    Julien 26/11 : « augmente un peu la taille de la police de la nomenclature »)."""
    xa, ya, xb, yb = ZONE
    W = xb - xa
    par = -(-len(rows) // len(folios))
    dispo = (yb - ya) // (par + 1) // 20 * 20
    for taille in tailles:
        pad = int(taille * marge)
        larg1 = lambda k: max(largeur(r[k], taille) for r in [entete] + [x[1] for x in rows]) + pad
        larg2 = lambda k: max(max(largeur(s, taille) for s in _coupe(r[k])) for r in [entete] + [x[1] for x in rows]) + pad
        cont = [larg1(k) for k in range(len(entete))]
        deux = set()
        if coupe and min(ligne_max, dispo) >= 2 * taille + 300:
            for k in sorted(range(len(entete)), key=lambda k: -(cont[k] - larg2(k))):
                if sum(cont) <= W:
                    break
                if larg2(k) < cont[k]:
                    cont[k] = larg2(k)
                    deux.add(k)
        if sum(cont) <= W:
            break
    else:
        raise ValueError(f"tableau trop large même en {tailles[-1]} : {sum(cont)} > {W}")
    reste = W - sum(cont)
    w = [c + reste * c // sum(cont) for c in cont]
    w[-1] += W - sum(w)
    ligne = min(ligne_max, dispo)
    if ligne < (2 * taille + 200 if deux else taille + 100):
        raise ValueError(f"tableau : {len(rows)} lignes sur {len(folios)} folios, lignes de {ligne} trop basses")
    paquets = [rows[i:i + par] for i in range(0, len(rows), par)]
    for f, paquet in zip(folios, paquets):
        TAILLE_FOLIO[f] = taille
        tab = [("entete", entete)] + paquet
        H = ligne * len(tab)
        y0 = ya + ((yb - ya) - H) // 2 // 100 * 100
        g.cadre(f, xa, y0, xb, y0 + H, width=20)
        for r in range(1, len(tab)):
            g.ligne(f, xa, y0 + r * ligne, xb, y0 + r * ligne, width=20 if tab[r][0] == "titre" or r == 1 else 10)
        cx = xa
        for c in w[:-1]:
            cx += c
            g.ligne(f, cx, y0, cx, y0 + H, width=10)
        for r, (fam, row) in enumerate(tab):
            cx = xa
            for k, (c, txt) in enumerate(zip(w, row)):
                if txt:
                    morceaux = _coupe(txt) if k in deux and largeur(txt, taille) + pad > c else [txt]
                    h_ = len(morceaux) * taille + (len(morceaux) - 1) * 80
                    for i_, s_ in enumerate(morceaux):
                        texte(f, cx + pad // 2, y0 + r * ligne + (ligne - h_) // 2 + i_ * (taille + 80), s_, taille, 0,
                              1 if fam in ("entete", "titre") else 0)
                cx += c
    return taille, ligne, [len(p) for p in paquets]


def dessiner(g, texte, folios, rows):
    # v43 (Julien 26/11) : police plus grande : tailles jusqu'à 340, blanc des colonnes réduit (0,4 x la taille)
    return tableau_pages(g, texte, folios, ENTETE, rows, tailles=(340, 320, 300) + TAILLES[1:], marge=0.4)


def controle_cables(chemin, numero_folio):
    """f80 (v33) : chaque câble du schéma (DefCable) et de saisie.json sur une seule ligne, rien d'autre."""
    m = xrs_tool.parse(chemin)
    idx = {f["index"] for f in m["folios"] if f["numero"] == numero_folio}
    par_ligne = defaultdict(list)
    for t in m["textes"]:
        if t["folio"] in idx:
            par_ligne[t["y"]].append((t["x"], t["texte"]))
    # v40 : cellules sur 2 lignes possibles ; une ligne du tableau = un texte dans la 1re colonne (repère, jamais coupé)
    xmin = min(x for v in par_ligne.values() for x, _ in v)
    reps = Counter(tx for v in par_ligne.values() for x, tx in v if x == xmin)
    pb = []
    attendus = {c["repere"] for c in _saisie()["cables"]} | {c["nom"] for c in m["cables"] if c["nom"]}
    for r in sorted(attendus, key=_naturel):
        if reps[r] != 1:
            pb.append(f"liste des câbles : {r} sur {reps[r]} ligne(s)")
    for r in reps:
        if r not in attendus and r != ENTETE_CABLES[0]:
            pb.append(f"liste des câbles : ligne inconnue « {r} »")
    return pb


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
            if not est_bjm(s_["nom"]) and (nat == "terre") != (s_["nom"] in tb["terre"]):
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
            tf = TAILLE_FOLIO.get(f, 200)
            fin = xs[k + 1] - tf // 2 + 50 if k + 1 < len(xs) else None
            if fin and x + largeur(t, tf) > fin:
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
