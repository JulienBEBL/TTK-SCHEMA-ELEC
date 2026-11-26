"""Dossier d'implantation de l'armoire +A1 : génération du PDF unique.

Entrée : donnees.json (python -I extraire.py). Sortie : ../release/TTK_implantation_<date>_<version>.pdf
et un rapport de contrôle (_verification.md). Toutes les pages viennent du même fichier de données :
l'implantation, la liste des câbles et le synoptique ne peuvent pas diverger.

Usage : python -I generer.py [--png dossier]   (--png : rastérise chaque page pour le contrôle visuel)
"""
import json
import os
import re
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
from svg import Page, largeur, coupe  # noqa: E402

D = json.load(open(os.path.join(ICI, "donnees.json"), encoding="utf-8"))
S = D["saisie"]
DOC = S["document"]
B = D["bornes"]
CAB = {c["repere"]: c for c in S["cables"]}
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

FAMILLE = {"alim": "#fff2cc", "variateur": "#f8cecc", "puissance": "#fbe3d6", "distrib": "#eeeeee",
           "automate": "#d5e8d4", "securite": "#ffe6cc"}
ETAT = {"fixe": "déjà fixé", "a_poser": "à poser", "deplace": "déplacé (13/11)", "propose": "proposé"}
TYPE_FILL = {"PT 2,5": "#d9d9d9", "PT 4": "#a6a6a6", "terre": "#7fbf5f", "PTFIX 2X4": "#c9d6e8",
             "boîte": "#f3e6c9"}
BJM = S["boite"]["bornier"]   # v14 : bornier +BJM-X1 (hors armoire)

PAGES = []


def nouvelle(titre):
    p = Page(titre, len(PAGES) + 1)
    PAGES.append(p)
    return p


# ------------------------------------------------------------------ cadre et cartouche
def cadre(p):
    p.rect(10, 7, 403, 283, sw=0.5)
    p.text(16, 16, p.titre, 5, gras=True, maxw=225)
    x, y, w, h = 243, 262, 170, 28
    p.rect(x, y, w, h, fill="#ffffff", sw=0.5)
    p.line(x + 40, y, x + 40, y + h)
    p.line(x + 130, y, x + 130, y + h)
    p.text(x + 20, y + 9, DOC["societe"], 6, ancre="middle", gras=True)
    p.text(x + 20, y + 16, "Dessiné : " + DOC["auteur"], 2.2, ancre="middle", maxw=38)
    p.text(x + 20, y + 21, "Généré par script", 2.2, ancre="middle", maxw=38)
    p.text(x + 20, y + 26, "(implantation/generateur)", 1.8, ancre="middle", maxw=38)
    p.text(x + 43, y + 6, DOC["machine"], 2.4, maxw=85)
    p.text(x + 43, y + 12, DOC["titre"], 2.8, gras=True, maxw=85)
    for i, l in enumerate(coupe(p.titre, 2.6, 85)[:2]):
        p.text(x + 43, y + 18 + 3.4 * i, l, 2.6, maxw=85)
    p.text(x + 43, y + 26.5, "Source : " + D["source"].split("/")[-1], 2.0, maxw=85)
    p.text(x + 150, y + 8, f"Indice {DOC['indice']}", 4.2, ancre="middle", gras=True)
    p.text(x + 150, y + 13.5, f"{DOC['version']} · {DOC['date']}", 2.4, ancre="middle", maxw=38)
    p.text(x + 150, y + 18.5, "A3 paysage · cotes en mm", 2.0, ancre="middle", maxw=38)
    p.text(x + 150, y + 25, f"Page {p.num} / {{N}}", 3, ancre="middle", gras=True)


# ------------------------------------------------------------------ libellés de borne
def cote_appareil(rec):
    """Borne interne (X13) : raccords du côté sans disjoncteur."""
    for c in rec["cotes"]:
        if c["raccords"] and not any(x.startswith("QF") for x in c["raccords"]):
            return " / ".join(c["raccords"])
    return "-"


def court_armoire(rec):
    if rec["repere"].startswith("X13."):
        for c in rec["cotes"]:
            if any(x.startswith("QF") for x in c["raccords"]):
                return " / ".join(c["raccords"])
    r = rec["cote_armoire"]
    if not r:
        return "-"
    s = " ".join(r)
    for cle, nom in (("X21.14", "24 V capteurs (X21.14)"), ("X21.12", "0 V (X21.12)"),
                     ("X21.11", "24VELEC (X21.11)"), ("XD1:PE", "PE (vers XPE1)")):
        if cle in s and len(r) > 2:
            return nom
    if "QF1:6" in s:
        return "L3 du bus 400 V (XR)"
    if "QF1:N" in s:
        return "N du bus (XR)"
    app = [x for x in r if not x.startswith("X")]
    if app:
        return " / ".join(app[:2]) + (" …" if len(app) > 2 else "")
    return "pont " + " / ".join(x.split(":")[0] for x in r[:2])


def court_ext(rec):
    ext = rec.get("cote_exterieur", [])
    if ext and all(x.startswith("X1.") for x in ext):   # v14 (Julien 26/11) : seulement « +BJM X1.n »
        return "+BJM " + " / ".join(x.split(":")[0] for x in ext)
    return " / ".join(ext) or "-"


def type_borne(rep):
    if rep.startswith("X1."):
        return "terre" if rep in BJM["terre"] else "PT 4" if rep in BJM["PT 4"] else "PT 2,5"
    t = S["types_bornes"]
    if rep in t["terre"]:
        return "terre"
    if rep in t["PT 4"]:
        return "PT 4"
    if rep in t.get("PTFIX 2X4", []):
        return "PTFIX 2X4"
    return "PT 2,5"


def larg_borne(rep):
    if rep.startswith("X1."):
        return BJM["largeur"][type_borne(rep)]
    return S["types_bornes"]["largeur"][type_borne(rep)]


def conducteur(cable, rep):
    if rep.startswith("X1."):   # boîte : n° du conducteur de la borne d'armoire raccordée
        arm = [x.split(":")[0] for x in B[rep]["cote_armoire"]]
        rep = arm[0] if arm else rep
    for n, b in S["conducteurs"].get(cable, []):
        if b == rep:
            return n
    return ""


# ------------------------------------------------------------------ disposition d'un tronçon (mm réels)
BUTEE, CAPOT, ZONE = 10.0, 2.2, 20.0


def disposer(bornier):
    """Positions réelles (mm) : butées, bornes, capots. Saute les vis / supports (zone de 20 mm)."""
    rail = S["rails"].get(bornier["rail"], {"x": 0, "l": 1e9})   # boîte +BJM : pas de rail
    obst = rail.get("vis", []) + rail.get("supports", [])
    x = bornier["x0"] - BUTEE
    out = []

    def libre(a, b):
        for o in obst:
            if a < o + ZONE and o < b:
                return o + ZONE
        return None

    for g in bornier["groupes"]:
        larg = sum(larg_borne(r) for r in g["bornes"]) + CAPOT
        if "apres_vis" in g:
            x = max(x, g["apres_vis"] + ZONE)
        if g.get("sans_butee") and out and out[-1][0] == "butee":
            out.pop()
            x -= BUTEE
        partage = bool(out) and out[-1][0] in ("butee", "capot") and abs(out[-1][1] + out[-1][2] - x) < 0.01
        while True:
            a = x - BUTEE if partage else x
            saut = libre(a, a + BUTEE + larg + BUTEE)
            if saut is None:
                break
            x, partage = saut, False
        if not g.get("sans_butee") and (not out or out[-1][0] != "butee" or abs(out[-1][1] + BUTEE - x) > 0.01):
            out.append(("butee", x, BUTEE))
            x += BUTEE
        x0 = x
        for r in g["bornes"]:
            w = larg_borne(r)
            out.append(("borne", x, w, r, g))
            x += w
        out.append(("capot", x, CAPOT))
        x += CAPOT
        g["_x"] = (x0, x)
        out.append(("butee", x, BUTEE))
        x += BUTEE
    fin = rail["x"] + rail["l"] if bornier["rail"] in S["rails"] else x
    return out, obst, x, fin


# ------------------------------------------------------------------ dessin d'une rangée de bornes
K = 1.2    # agrandissement des bornes (1 mm réel -> 1,2 mm sur la page) : tout le détail tient sur une A3
A_VALIDER = set()   # câbles dont la répartition est à valider (tireté rouge). W11 / W12 : validés (Julien 05/11, reconfirmé 18/11)


def rangee(p, bornier, y, titre, x_page=16):
    """Une rangée compacte (57 mm de haut). Retourne (y bas, x droit) sur la page."""
    pos, obst, xfin, fin = disposer(bornier)
    if xfin > fin + 0.01:
        p.erreurs.append(f"p{p.num} {titre} : le bornier dépasse le rail ({xfin:.0f} > {fin:.0f} mm)")
    xr0 = pos[0][1] - 4
    X = lambda xr: x_page + (xr - xr0) * K   # noqa: E731
    if X(xfin) > 410:
        p.erreurs.append(f"p{p.num} {titre} : rangée trop large pour la page ({X(xfin):.0f} mm)")
    p.text(x_page, y, titre, 2.8, gras=True, maxw=max(X(xfin) - x_page, 230))
    yb = y + 2.5
    Y_CORPS = yb + 18
    Y_COND, Y_BAS = Y_CORPS + 17.5, Y_CORPS + 20
    # rail (bande grise) et vis / supports
    p.rect(X(xr0), Y_CORPS + 2, X(min(xfin + 4, fin)) - X(xr0), 10, fill="#f2f2f2", stroke="#bfbfbf", sw=0.2)
    for o in obst:
        if xr0 <= o < xfin:
            lab = "support 45°" if bornier["rail"] == "R5" else "vis"
            p.rect(X(o), Y_CORPS, ZONE * K, 14, fill="#e8e0f0" if lab != "vis" else "#dbe8f5",
                   stroke="#7f7f7f", sw=0.2, dash="1,0.6")
            p.text(X(o) + ZONE * K / 2, Y_CORPS + 8, lab, 1.8, ancre="middle", coul="#555", maxw=ZONE * K - 0.5)
    # bandeaux de câble (groupes consécutifs du même câble)
    grp = []
    for g in bornier["groupes"]:
        if grp and grp[-1][0] == g["cable"]:
            grp[-1][2] = g["_x"][1]
        else:
            grp.append([g["cable"], g["_x"][0], g["_x"][1]])
    for cab, a, b in grp:
        coul = S["couleurs_cables"].get(cab, "#eeeeee")
        av = cab in A_VALIDER
        p.rect(X(a), yb, X(b) - X(a), 5, fill=coul, stroke="#d00000" if av else "#000", sw=0.4 if av else 0.25,
               dash="1.2,0.6" if av else None)
        if cab in CAB:
            c = CAB[cab]
            if bornier["rail"] == "+BJM":
                lieu = {"W11": "+P1 pupitre"}.get(cab, "+M")
            else:
                lieu = "réseau client" if cab == "W1" else "+BJM"
            lab = f"{cab} · {c['conducteurs'].split(' (')[0]} · vers {lieu}"
            if av:
                lab += " · répartition à valider"
        else:
            lab = {"int": "Interne armoire (230 V)", "porte": "Porte de l'armoire (TBTP)",
                   "porte230": "Porte : 230 V"}.get(cab, cab)
        larg_dispo = X(b) - X(a) - 1
        for essai in (lab, lab.split(" · vers")[0] + (" · à valider" if av else ""), cab):
            t = 2.2
            while largeur(essai, t, True) > larg_dispo and t > 1.6:
                t -= 0.1
            if largeur(essai, t, True) <= larg_dispo:
                break
        p.text((X(a) + X(b)) / 2, yb + 3.6, essai, t, ancre="middle", gras=True, maxw=larg_dispo,
               coul="#c00000" if av else "#000")
    # bornes
    for e in pos:
        if e[0] == "butee":
            p.rect(X(e[1]), Y_CORPS - 2, e[2] * K, 18, fill="#262626", stroke="#000", sw=0.2)
        elif e[0] == "capot":
            p.rect(X(e[1]), Y_CORPS - 1, e[2] * K, 16, fill="#8c8c8c", stroke="#000", sw=0.2)
        else:
            _, xr, w, rep, g = e
            rec = B[rep]
            tb = type_borne(rep)
            x0, ww = X(xr), w * K
            cx = x0 + ww / 2
            p.rect(x0, Y_CORPS, ww, 14, fill=TYPE_FILL[tb], stroke="#000", sw=0.25)
            if tb == "terre":
                for k in range(2):
                    p.rect(x0 + 0.4, Y_CORPS + 3 + k * 6, ww - 0.8, 2, fill="#ffd200", stroke="none", sw=0)
            p.rect(x0 + 1.2, Y_CORPS + 0.6, ww - 2.4, 1.6, fill="#ffffff", stroke="#000", sw=0.15)   # entrée haut
            p.rect(x0 + 1.2, Y_CORPS + 11.8, ww - 2.4, 1.6, fill="#ffffff", stroke="#000", sw=0.15)  # entrée bas
            p.text(cx - 0.8, Y_CORPS + 11.3, rep, 2.0, gras=True, rot=-90, maxw=9)
            fil = rec.get("numero_fil", "")
            if fil:
                p.text(cx + 1.7, Y_CORPS + 11.3, fil, 1.7, rot=-90, maxw=9, coul="#1f3f7f")
            # côté armoire (haut) et côté extérieur (bas), lus de bas en haut
            haut = ("+A1 " + " / ".join(x.split(":")[0] for x in rec["cote_armoire"])) if rep.startswith("X1.") \
                else court_armoire(rec)
            for i, l in enumerate(coupe(haut, 1.7, 10.8)[:2]):
                p.text(cx - 0.8 + 1.8 * i, Y_CORPS - 2.2, l, 1.7, rot=-90, maxw=10.8)
            n = conducteur(g["cable"], rep)
            n = {"vert (+)": "VE+", "blanc (-)": "BL-", "blanc": "BL", "marron": "MA"}.get(n, n)
            if n:
                p.rect(x0 + 0.4, Y_COND - 2.6, ww - 0.8, 3.6, fill="#ffffff", stroke="#1f3f7f", sw=0.2, rx=1)
                p.text(cx, Y_COND, n, 2.0 if len(n) < 3 else 1.6, ancre="middle", gras=True, coul="#1f3f7f",
                       maxw=ww - 1)
            ext = court_ext(rec)
            if g["cable"] == "W1":
                ext = "réseau client"
            if g["cable"] == "int":
                ext = cote_appareil(rec)
            for i, l in enumerate(coupe(ext, 1.7, 12.5)[:2]):
                p.text(cx - 0.8 + 1.8 * i, Y_BAS + 0.8, l, 1.7, rot=-90, ancre="end", maxw=12.5)
    # nom des groupes (fonction)
    for g in bornier["groupes"]:
        a, b = X(g["_x"][0]), X(g["_x"][1])
        yy = Y_BAS + 16
        for l in coupe(g["fonction"], 2.0, max(b - a + 6, 10))[:2]:
            p.text((a + b) / 2, yy, l, 2.0, ancre="middle", maxw=max(b - a + 6, 10))
            yy += 2.4
    return Y_BAS + 21, X(xfin)


def legende_borne(p, x, y):
    """Légende de lecture d'une borne."""
    p.text(x, y, "Lecture d'une borne", 2.6, gras=True)
    y += 3
    p.rect(x, y, 7, 22, fill=TYPE_FILL["PT 2,5"])
    p.text(x + 2.6, y + 19, "X41.11", 2.0, gras=True, rot=-90, maxw=18)
    p.text(x + 5, y + 19, "4111", 1.7, rot=-90, coul="#1f3f7f", maxw=18)
    items = ["Haut : côté armoire (appareil:broche, ou potentiel)", "Corps : repère de la borne (gras), n° de fil (bleu)",
             "Pastille : n° de conducteur du câble", "Bas : côté extérieur (appareil:broche)",
             "Bandeau : câble · composition · destination (tireté rouge : à valider)"]
    for i, it in enumerate(items):
        p.text(x + 10, y + 3 + 4.2 * i, it, 2.1, maxw=150)
    y += 25
    for i, (nom, f) in enumerate([("PT 2,5 (5,2 mm)", TYPE_FILL["PT 2,5"]), ("PT 4 (6,2 mm)", TYPE_FILL["PT 4"]),
                                  ("PTFIX 2X4 (6 mm)", TYPE_FILL["PTFIX 2X4"]), ("Terre V/J (5,2 mm)", TYPE_FILL["terre"]),
                                  ("Butée 10 mm", "#262626"), ("Capot de fin", "#8c8c8c")]):
        xx = x + (i % 3) * 42
        yy = y + (i // 3) * 5
        p.rect(xx, yy - 2.6, 4, 3, fill=f, stroke="#000", sw=0.2)
        p.text(xx + 5, yy, nom, 2.1, maxw=36)
    return y + 10


# ------------------------------------------------------------------ pages
def page_garde():
    p = nouvelle("Page de garde, sommaire et révisions")
    cadre(p)
    return p


def remplir_garde(p):
    p.text(16, 34, DOC["machine"], 5, maxw=380)
    p.text(16, 46, "ARMOIRE +A1", 11, gras=True)
    p.text(16, 58, "Implantation, borniers, liste des câbles et synoptique", 6, maxw=390)
    p.text(16, 67, f"Indice {DOC['indice']} ({DOC['version']}) du {DOC['date']} · schéma source : "
                   f"{D['source'].split('/')[-1]}", 3.2, maxw=390)
    p.text(16, 82, "Sommaire", 4, gras=True)
    y = 89
    for q in PAGES:
        p.text(20, y, f"{q.num}", 3, maxw=8)
        p.text(30, y, q.titre, 3, maxw=160)
        y += 5.2
    p.text(16, y + 6, "Révisions", 4, gras=True)
    y += 13
    p.rect(16, y - 4, 190, 5.5, fill="#eeeeee")
    for x, t in ((18, "Indice"), (32, "Date"), (56, "Objet")):
        p.text(x, y, t, 2.6, gras=True)
    for ind, date, obj in DOC["revisions"]:
        y += 6
        p.text(18, y, ind, 2.6)
        p.text(32, y, date, 2.6)
        yy = p.bloc(56, y, obj, 2.6, maxw=148)
        y = yy - 2.6
    # colonne de droite : sources et points ouverts
    x = 222
    p.text(x, 82, "Sources (par ordre de priorité)", 4, gras=True)
    sources = [f"1. Schéma WinRelais {D['source'].split('/')[-1]} (bornes, câbles, numéros de fil : relus par script).",
               "2. memoire/ et docs/ du dépôt (décisions datées).",
               "3. Sourcing Composant, feuille Tableau V1 (03/11, 1 armoire) : références et câbles achetés.",
               "4. Implantation draw.io v10 (06/11) : géométrie de la plaque, rails, vis, supports.",
               "Décisions de Julien du 17/11 : bornes X63 gardées ; W9 / W10 en LIYCY-JZ 5G1,5 ; boîte +BJM ; "
               "blindage raccordé d'un seul côté."]
    y = 89
    for s in sources:
        y = p.bloc(x, y, s, 2.6, maxw=185) + 1
    p.text(x, y + 5, "Points ouverts à trancher", 4, gras=True)
    y += 12
    for s in OUVERTS:
        y = p.bloc(x, y, "• " + s, 2.5, maxw=185) + 0.8
    return p


OUVERTS = []


def page_charte():
    p = nouvelle("Charte du document")
    cadre(p)
    col = [16, 150, 284]
    blocs = [
        ("Format et cartouche", [
            "A3 paysage (420 x 297 mm), vectoriel. Une page = un sujet. Cadre à 10 mm à gauche, 7 mm ailleurs.",
            "Cartouche en bas à droite : société, dessinateur, machine, titre du dossier et de la page, schéma source, "
            "indice, version, date, page n / N. L'indice change à chaque diffusion (A, B, C…).",
            "Le dossier est généré par script depuis le schéma : une modification se fait dans le schéma ou dans "
            "saisie.json, jamais dans le PDF."]),
        ("Repérage (IEC 81346-2, comme le schéma)", [
            "Lieux : +A1 armoire, +P1 pupitre, +M machine. Boîte de dérivation machine : +BJM.",
            "Appareils : lettre de fonction + n° (QF1, KA1, U1, K1, S1, B1, H1…), identiques au schéma.",
            "Bornes : X + n° du folio où la borne est dessinée + « . » + n° (X41.11 = folio 41, groupe 1, borne 1).",
            "Fils : n° de potentiel FFNN du schéma (ex. 4111), sans point. PE : vert/jaune, sans numéro.",
            "Câbles : W1, W2… (cuivre), PN1… (PROFINET). Un même repère partout : bornier, liste, synoptique."]),
        ("Groupement des borniers", [
            "Rail R5 (45°) : bornes vers l'extérieur, groupées par câble, puis par fonction dans le câble.",
            "N° de conducteur d'un câble multiconducteur = ordre des bornes. Conducteurs de réserve non bornés.",
            "Une butée de 10 mm de chaque côté de chaque groupe ; capot de fin à droite de chaque groupe.",
            "Fins de course B3 à B6 : 2 bornes par contact. Bornes de porte sur R4 ; le 230 V (H2) est isolé du "
            "TBTP par une vis de rail et une butée.",
            "Aucun groupe sur une vis de rail ou un support 45° (zone libre de 20 mm)."]),
        ("Code couleur des appareils (plan de plaque)", None),
        ("Statut", [
            "Trait épais : déjà fixé (ne pas déplacer). Trait fin : à poser. Tireté orange : déplacé.",
            "Tireté rouge : proposition à valider. Liste des câbles : acheté / à confirmer / manquant / client."]),
        ("Couleur des conducteurs (IEC 60204-1, comme le schéma)", [
            "Puissance CA et CC (phases, frein, 48 V, pas-à-pas) : noir. Neutre : bleu clair. Terre : vert/jaune.",
            "Commande 24 V CC : bleu foncé ; 0 V : bleu foncé ou blanc. Thermocouple K : vert (+), blanc (-).",
            "Câbles multiconducteurs LIYCY-JZ : conducteurs noirs numérotés + V/J."]),
        ("Ce qui a marché dans v1 à v10, repris ici", [
            "Plaque à l'échelle avec vis et supports déjà posés (v1), bornes groupées par câble (v5), butées entre "
            "fonctions (v8), bornes dessinées en largeur réelle avec repère, fonction et n° de conducteur (v10).",
            "Nouveau : côté armoire et côté extérieur écrits sur chaque borne, n° de fil, liste des câbles et "
            "synoptique dans le même document, contrôle automatique contre le schéma."]),
    ]
    y = [26, 26, 26]
    for i, (titre, lignes) in enumerate(blocs):
        c = i % 3
        x = col[c]
        p.text(x, y[c], titre, 3.4, gras=True, maxw=122)
        yy = y[c] + 5
        if lignes is None:
            for j, (fam, f) in enumerate(FAMILLE.items()):
                nom = {"alim": "Alimentations, drivers", "variateur": "Variateurs, résistances",
                       "puissance": "Puissance 400 / 230 V", "distrib": "Distribution 24 V (PTFIX)",
                       "automate": "Automate, réseau", "securite": "Sécurité"}[fam]
                p.rect(x, yy - 2.8, 6, 3.4, fill=f)
                p.text(x + 8, yy, nom, 2.6, maxw=118)
                yy += 4.6
        else:
            for l in lignes:
                yy = p.bloc(x, yy, l, 2.6, maxw=122) + 1.2
        y[c] = yy + 5
    yl = max(y) + 2
    legende_borne(p, col[0], yl)
    x = col[1]
    p.text(x, yl, "Couleurs des bandeaux de câble", 2.6, gras=True)
    yy = yl + 5
    vus = []
    for cab, f in S["couleurs_cables"].items():
        if f in [v[1] for v in vus]:
            vus[[v[1] for v in vus].index(f)][0] += " " + cab
            continue
        vus.append([cab, f])
    for i, (cab, f) in enumerate(vus):
        xx, yy2 = x + (i % 2) * 62, yy + (i // 2) * 4.6
        p.rect(xx, yy2 - 2.8, 6, 3.4, fill=f)
        noms = cab.replace("porte230", "porte 230 V").replace("int", "interne")
        p.text(xx + 8, yy2, noms, 2.3, maxw=52)
    return p


def page_plaque():
    p = nouvelle("Plan de la plaque de montage (échelle 1:7)")
    cadre(p)
    s = 1 / 7
    ox, oy = 22, 26
    P = lambda x, y: (ox + x * s, oy + y * s)   # noqa: E731
    pl = S["plaque"]
    p.rect(ox, oy, pl["largeur"] * s, pl["hauteur"] * s, fill="#ffffff", sw=0.5)
    for nom, x, y, w, h, dim in S["goulottes"]:
        p.rect(*P(x, y), w * s, h * s, fill="#e0e0e0", stroke="#9e9e9e", sw=0.15)
    for r, d in S["rails"].items():
        x, y = P(d["x"], d["y"])
        p.rect(x, y, d["l"] * s, 35 * s, fill="#f4f4f4", stroke="#7f7f7f", sw=0.6 if d["fixe"] else 0.2)
        for v in d.get("vis", []):
            p.rect(*P(v, d["y"]), 20 * s, 35 * s, fill="#dbe8f5", stroke="#4a78b0", sw=0.15)
        for v in d.get("supports", []):
            p.rect(*P(v, d["y"] - 22), 20 * s, 80 * s, fill="#e8e0f0", stroke="#7030a0", sw=0.15)
        p.text(ox - 1.5, y + 3.4, r, 2.4, ancre="end", gras=True, maxw=9)
    for rep, rail, x, y, w, h, etat, des, ref, fam in S["appareils"]:
        X0, Y0 = P(x, y)
        sw = {"fixe": 0.55, "a_poser": 0.2, "deplace": 0.35, "propose": 0.35}[etat]
        st = {"fixe": "#000", "a_poser": "#000", "deplace": "#e07000", "propose": "#d00000"}[etat]
        dash = "1.2,0.6" if etat in ("deplace", "propose") else None
        p.rect(X0, Y0, w * s, h * s, fill=FAMILLE[fam], stroke=st, sw=sw, dash=dash)
        t = 1.7 if largeur(rep, 1.7) <= w * s - 0.8 or w * s < 4 else 1.45
        if largeur(rep, t) <= w * s - 0.6:
            p.text(X0 + w * s / 2, Y0 + h * s / 2 + 0.6, rep, t, ancre="middle", maxw=w * s - 0.2)
        else:
            p.text(X0 + w * s / 2 + 0.6, Y0 + h * s - 0.5, rep, t, rot=-90, maxw=h * s - 0.6)
    # borniers R5 et R4 : un bloc par groupe, couleur du câble
    for br in S["borniers"]:
        disposer(br)
        rail = S["rails"][br["rail"]]
        for g in br["groupes"]:
            a, b = g["_x"]
            X0, Y0 = P(a, rail["y"] - 10)
            p.rect(X0, Y0, (b - a) * s, 55 * s, fill=S["couleurs_cables"].get(g["cable"], "#eee"), sw=0.15)
    # repères des câbles sous R5 (groupes consécutifs)
    rail = S["rails"]["R5"]
    for br in S["borniers"]:
        if br["rail"] != "R5":
            continue
        der = None
        for g in br["groupes"]:
            if g["cable"] == der:
                continue
            der = g["cable"]
            a = g["_x"][0]
            X0, Y0 = P(a, rail["y"] + 60)
            p.text(X0 + 0.6, Y0 + 0.5, g["cable"], 1.6, rot=-90, maxw=10, controle=False)
    # nomenclature à droite
    x0, y = 196, 24
    cols = [(x0, "Repère", 14), (x0 + 15, "Désignation", 76), (x0 + 92, "Référence", 64), (x0 + 157, "Emplacement", 24),
            (x0 + 182, "État", 34)]
    p.rect(x0 - 1, y - 3.4, 216, 4.6, fill="#eeeeee", sw=0.15)
    for x, t, w in cols:
        p.text(x, y, t, 2.3, gras=True, maxw=w)
    for rep, rail, x, yy, w, h, etat, des, ref, fam in S["appareils"]:
        y += 4.15
        for (xc, _, wc), v in zip(cols, (rep, des, ref, rail, ETAT[etat])):
            p.text(xc, y, v, 2.1, maxw=wc, coul={"deplace": "#b05000", "propose": "#c00000"}.get(etat, "#000")
                   if v == ETAT[etat] else "#000")
    nb = {"R5": 0, "R4": 0}
    for br in S["borniers"]:
        nb[br["rail"]] += sum(len(g["bornes"]) for g in br["groupes"])
    for rep, des, ref in S["hors_plaque"] + [["Borniers", f"R5 : {nb['R5']} bornes ; R4 : {nb['R4']} bornes "
                                              "(détail page 2) ; boîte +BJM-X1 : 69 bornes (page 3)", ""]]:
        y += 4.15
        p.text(x0, y, rep, 2.1, maxw=14 if len(rep) < 6 else 30)
        p.text(x0 + (15 if len(rep) < 6 else 31), y, des, 2.1, maxw=76 if len(rep) < 6 else 124)
        p.text(x0 + 92, y, ref, 2.1, maxw=64)
    y += 7
    notes = ["Rails : " + " ; ".join(f"{r} {d['role']}" for r, d in S["rails"].items()) + ".",
             "Cotes : plaque 1100 x 1670 depuis le coin haut gauche ; rails, vis et supports relevés sur l'indice K "
             "(v10). Pas de cote fine : ajustement au montage.",
             "R2 est plein et monté (13/11) : XR1 et XR2 côte à côte, l'ordre est juste, les positions sont indicatives.",
             "X21.14 : à droite de K4, près de K1 qui l'alimente (L+ capteurs), validé par Julien le 26/11.",
             "Rien sur les parois sauf les ventilateurs EV1 / EV2. U3 / U4 et -XPE1 vissés sur la plaque.",
             "R5 tronçon 1 : bornes W11 / W12 en PTFIX 2X4 (6 mm) ; répartition validée (Julien 05/11, 18/11)."]
    for n in notes:
        y = p.bloc(x0, y, "• " + n, 2.3, maxw=215) + 0.6
    return p


def page_borniers():
    """Page 2 : tous les borniers, de haut en bas comme sur la plaque (R4, puis R5 tronçons 1 à 4), et R3."""
    br = {b["troncon"]: b for b in S["borniers"]}
    p = nouvelle("Détail des borniers R4 et R5 (vue de face, bornes x 1,2) et distribution 24 V du rail R3")
    cadre(p)
    y, xd = rangee(p, br["après XD1 : services 230 V, puis porte"], 24,
                   "Rail R4, après XD1 : éclairage, ventilation, porte (S1, S4, H3, H4, puis H2 230 V après la vis)")
    legende_etroite(p, xd + 6, 30)
    y, xd = rangee(p, br["tronçon 1"], y + 3, "Rail R5 (45°), tronçon 1 : pupitre W11, machine W12 (par +BJM)")
    y, xd = rangee(p, br["tronçons 2 et 3"], y + 3, "Rail R5, tronçons 2 et 3 : B2, thermocouple, sondes TF, pas-à-pas")
    y3, xd = rangee(p, br["tronçon 4 (puissance)"], y + 3, "Rail R5, tronçon 4 : freins, moteurs, arrivée W1 (près de QS1)")
    r3(p, xd + 8, y + 3)
    return p


def page_boite():
    """Page 3 (v14) : bornier +BJM-X1 de la boîte de jonction machine (hors armoire)."""
    p = nouvelle("Bornier de la boîte de jonction machine +BJM-X1 (hors armoire, vue de face, bornes x 1,2)")
    cadre(p)
    y = 24
    for i, rg in enumerate(BJM["rangees"]):
        br = {"rail": "+BJM", "x0": 10.0, "groupes": rg["groupes"]}
        y, xd = rangee(p, br, y + (3 if i else 0), rg["troncon"] + " : haut = borne d'armoire raccordée (+A1), "
                       "bas = appareil sur la machine ou le pupitre")
    y += 6
    notes = ["Boîte de fabrication BEBL, bornier X1 de 69 bornes (66 de passage, 3 de terre : X1.4, X1.8, X1.69). "
             "Types (Julien 26/11) : PT 2,5 ; PT 4 pour les moteurs M1 / M2 (U V W) et les freins ; terre en PT 4 "
             "(largeur prise égale à la PT 4, 6,2 mm, à vérifier).",
             "Ordre des bornes = ordre du schéma (v37) : un groupe par câble, une butée de chaque côté de chaque groupe "
             "(règle des rails de l'armoire, appliquée à la boîte).",
             "N° de conducteur = celui de la borne d'armoire raccordée. Tous les câbles sortants passent par la boîte, "
             "W1 (réseau client) et W13 (V/J vers le bâti) exceptés.",
             "Plans de bornier du schéma : folios 70 à 73."]
    for n in notes:
        y = p.bloc(16, y, "• " + n, 2.4, maxw=222) + 0.8
    legende_etroite(p, 300, 162, bas="Bas : appareil (+M, +P1)", terre="Terre V/J PT 4 (6,2)")
    return p


def legende_etroite(p, x, y, bas="Bas : côté extérieur (+BJM X1.n)", terre="Terre V/J (5,2)"):
    """Légende de lecture d'une borne, en colonne (à droite du rail R4)."""
    w = 404 - x
    p.text(x, y, "Lecture d'une borne", 2.6, gras=True, maxw=w)
    y += 4.2
    for it in ["Haut : côté armoire", "Corps : repère (gras), n° de fil (bleu)", "Pastille : n° de conducteur",
               bas, "Bandeau : câble, destination"]:
        p.text(x, y, it, 2.0, maxw=w)
        y += 3.4
    y += 1.6
    for i, (nom, f) in enumerate([("PT 2,5 (5,2)", TYPE_FILL["PT 2,5"]), ("PT 4 (6,2)", TYPE_FILL["PT 4"]),
                                  ("PTFIX 2X4 (6)", TYPE_FILL["PTFIX 2X4"]), (terre, TYPE_FILL["terre"]),
                                  ("Butée (10)", "#262626"), ("Capot de fin", "#8c8c8c")]):
        xx = x + (i % 2) * (w / 2)
        yy = y + (i // 2) * 4.2
        p.rect(xx, yy - 2.6, 4, 3, fill=f, stroke="#000", sw=0.2)
        p.text(xx + 5, yy, nom, 2.0, maxw=w / 2 - 6)
    p.text(x, y + 16.5, "Largeurs réelles en mm", 1.9, coul="#555", maxw=w)


def r3(p, x, y):
    """Rail R3 : blocs PTFIX 6/12X2,5 posés en long et liaison PELV (dessin réduit, ordre réel)."""
    p.text(x, y, "Rail R3 : distribution 24 V (PTFIX 6/12X2,5 en long), PELV", 2.8, gras=True, maxw=404 - x)
    y += 3.5
    blocs = [("X21.11", "24VELEC", "#e06666", "1241"), ("X21.12", "0 V", "#6fa8dc", "1230"),
             ("X12.11", "PELV", TYPE_FILL["PT 4"], "1230 / PE"), ("X21.13", "24VSEC", "#b7b7b7", "1231"),
             ("…", "", "", ""), ("X21.14", "24 V capteurs", "#434343", "6001")]
    xx = x
    for rep, nom, f, fil in blocs:
        if rep == "…":
            p.text(xx, y + 10, "FA1 KA1 K1-K4", 2.0, coul="#555", maxw=22)
            xx += 23
            continue
        w = 7.4 if rep == "X12.11" else 26
        prop = False   # X21.14 validé à droite de K4 (Julien 26/11)
        p.rect(xx, y, w, 19, fill=f, stroke="#d00000" if prop else "#000", sw=0.35, dash="1.2,0.6" if prop else None)
        coul = "#ffffff" if rep in ("X21.11", "X21.14") else "#000"
        if rep == "X12.11":
            p.text(xx + 4.5, y + 18, rep, 2.1, gras=True, rot=-90, maxw=17)
        else:
            p.text(xx + w / 2, y + 5, rep, 2.5, gras=True, ancre="middle", coul=coul, maxw=w - 1)
            p.text(xx + w / 2, y + 9.5, nom, 2.1, ancre="middle", coul=coul, maxw=w - 1.5)
            p.text(xx + w / 2, y + 13.5, "fil " + fil, 1.9, ancre="middle", coul=coul, maxw=w - 1.5)
            p.text(xx + w / 2, y + 17.3, "1 entrée + 12", 1.7, ancre="middle", coul=coul, maxw=w - 1.5)
        xx += w + 2
    p.bloc(x, y + 23.5, "X21.14 à droite de K4, près de K1 (L+ capteurs), validé le 26/11. "
           "Dessin réduit, ordre réel de gauche à droite.", 2.0, maxw=404 - x)


def page_cables():
    p = nouvelle("Liste des câbles")
    cadre(p)
    cols = [("Repère", 14), ("Fonction", 46), ("Origine (appareil, borne)", 50), ("Destination (appareil, borne)", 44),
            ("Type", 34), ("Référence", 30), ("Conducteurs x section", 40), ("Blindage et raccordement", 44),
            ("Longueur", 30), ("Statut", 24), ("Folio", 20)]
    keys = ["repere", "fonction", "origine", "destination", "type", "reference", "conducteurs", "blindage",
            "longueur", "statut", "folio"]
    x0, y = 16, 26
    xs = [x0]
    for _, w in cols:
        xs.append(xs[-1] + w + 1)
    t = 2.45
    p.rect(x0 - 1, y - 3.6, xs[-1] - x0, 8.6, fill="#eeeeee", sw=0.2)
    for (h, w), x in zip(cols, xs):
        yy = y
        for l in coupe(h, t, w):
            p.text(x, yy, l, t, gras=True, maxw=w)
            yy += 3.0
    y += 8
    for c in S["cables"]:
        cell = []
        for k, (_, w) in zip(keys, cols):
            v = c.get(k, "")
            if k == "repere" and c.get("propose"):
                v += " *"
            cell.append(coupe(v, t, w))
        n = max(len(x) for x in cell)
        coul = {"acheté": "#000"}.get(c["statut"], "#c00000" if c["statut"] in ("à confirmer", "manquant") else "#000")
        for lignes, x, k in zip(cell, xs, keys):
            for i, l in enumerate(lignes):
                p.text(x, y + i * 3.1, l, t, maxw=cols[keys.index(k)][1],
                       gras=(k == "repere"), coul=coul if k == "statut" else "#000")
        y += n * 3.1 + 2.2
        p.line(x0 - 1, y - 3.4, xs[-1] - 1, y - 3.4, stroke="#bfbfbf", sw=0.15)
    y += 2
    notes = [
        "Longueur : 10 m maximum entre l'armoire et la machine (consigne du 17/11) ; à mesurer à l'installation. "
        "Stock (Tableau V1, 1 armoire) suffisant pour 10 m sur tous les câbles achetés ; 5G1,5 : W4 + W9 + W10 = 30 m.",
        "* W14 : repère proposé (le câble M12 de B2 n'a pas de repère dans le schéma).",
        "W8 « à confirmer » : le câble 236-3959 est marqué non commandé dans Tableau V1 ; sujet clos selon Julien.",
        "Blindage : raccordé d'un seul côté, côté armoire, par le presse-étoupe CEM (décision du 17/11). "
        "PN1 à PN4 : blindage repris par les fiches RJ45.",
        "Dans le schéma v31, W11, W12, W14 et PN1 à PN4 ne sont pas des objets câble (absents du tableau f80) ; "
        "W9 / W10 y sont encore « 4 cond. blindé »."]
    for n in notes:
        y = p.bloc(16, y, "• " + n, 2.4, maxw=222) + 0.6


def table_cond(p, cab, x, y, larg, titre_ext, t=2.0, pas=3.9):
    c = CAB[cab]
    p.text(x, y, f"{cab} · {c['type']} · {c['conducteurs']}", 3 if largeur(f"{cab} · {c['type']} · {c['conducteurs']}", 3, True) <= larg else 2.5, gras=True, maxw=larg)
    y += 2.5
    y = p.bloc(x, y + 2.6, S["notes_conducteurs"].get(cab, ""), 2.1, maxw=larg) + 2.4
    cols = [("Cond.", 0.15), ("Borne +A1", 0.15), ("Côté armoire", 0.28), ("Fil", 0.11), (titre_ext, 0.31)]
    xs, xx = [], x
    for _, f in cols:
        xs.append(xx)
        xx += larg * f
    p.rect(x - 0.8, y - 3, larg + 0.8, 4.2, fill="#eeeeee", sw=0.15)
    for (h, f), xc in zip(cols, xs):
        p.text(xc, y, h, t + 0.1, gras=True, maxw=larg * f - 1)
    for n, rep in S["conducteurs"][cab]:
        y += pas
        if rep in B:
            rec = B[rep]
            ext = court_ext(rec)
            if cab == "W12":
                ext = "+BJM → " + ext
            vals = [n, rep, court_armoire(rec), rec.get("numero_fil", ""), ext]
        elif rep == "XPE1":
            vals = [n, "-XPE1", "barrette de terre", "PE", "+BJM masse" if cab in ("W12", "W4") else "masse moteur ?"]
        else:
            vals = [n, "-", "réserve, non bornée", "", "-"]
        for v, (h, f), xc in zip(vals, cols, xs):
            txt = v
            while largeur(txt, t) > larg * f - 1 and len(txt) > 3:
                txt = txt[:-2] + "…"
            p.text(xc, y, txt, t, maxw=larg * f - 1)
        p.line(x - 0.8, y + pas * 0.3, x + larg, y + pas * 0.3, stroke="#d9d9d9", sw=0.1)
    return y + 7


def pages_conducteurs():
    p = nouvelle("Affectation des conducteurs : W11 (pupitre) et W12 (machine)")
    cadre(p)
    table_cond(p, "W11", 16, 27, 192, "Côté pupitre +P1", 2.7, 6.2)
    table_cond(p, "W12", 216, 27, 192, "Côté machine", 2.7, 6.2)
    p = nouvelle("Affectation des conducteurs : puissance, sondes, pas-à-pas, B2, câbles après la boîte")
    cadre(p)
    y1 = 27
    for cab in ("W4", "W2", "W5", "W9", "W10"):
        y1 = table_cond(p, cab, 16, y1, 128, "Côté machine")
    y2 = 27
    for cab in ("W3", "W6", "W8", "W14"):
        y2 = table_cond(p, cab, 152, y2, 128, "Côté machine")
    x, y = 290, 27
    p.text(x, y, "Après la boîte +BJM : câbles à définir", 3, gras=True, maxw=120)
    y = p.bloc(x, y + 5, "Le schéma s'arrête aux bornes de l'armoire : les liaisons boîte → appareils n'y sont pas. "
                         "À définir avec Julien (aucun achat possible).", 2.2, maxw=120) + 1
    for liaison, cond, nature in S["apres_boite"]:
        p.text(x, y, liaison, 2.3, gras=True, maxw=120)
        p.text(x + 3, y + 3.2, f"{cond} · {nature}", 2.2, maxw=117)
        y += 8
    p.text(x, y + 2, "Stock non affecté (Tableau V1) :", 2.4, gras=True, maxw=120)
    y += 6
    for nom, ref, src in S["stock_libre"]:
        y = p.bloc(x, y, f"{nom} ({ref}) : {src}", 2.2, maxw=120) + 1


def page_synoptique():
    p = nouvelle("Synoptique du système")
    cadre(p)

    def boite(x, y, w, h, titre, lignes, dash=None, fill="#ffffff"):
        p.rect(x, y, w, h, fill=fill, sw=0.4, dash=dash, rx=1.5)
        p.text(x + w / 2, y + 5, titre, 3, ancre="middle", gras=True, maxw=w - 2)
        yy = y + 9.5
        for l in lignes:
            p.text(x + w / 2, yy, l, 2.3, ancre="middle", maxw=w - 2)
            yy += 3.2
        return (x, y, w, h)

    def fl(pts, rep, pos=0, dash=None, cote="h"):
        p.poly(pts, sw=0.4, dash=dash, fleche=True)
        (x1, y1), (x2, y2) = pts[pos], pts[pos + 1]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        c = CAB.get(rep.split(" ")[0])
        sous = c["conducteurs"].split(" (")[0].split(" :")[0] if c else ""
        lab = rep + (f" · {sous}" if sous and sous != "RJ45" else "")
        w = largeur(lab, 2.4, True) + 2
        if cote == "h":
            p.rect(mx - w / 2, my - 2.6, w, 3.8, fill="#ffffff", stroke="none", sw=0)
            p.text(mx, my + 0.6, lab, 2.4, ancre="middle", gras=True)
        else:
            p.rect(mx - w / 2, my - 2.6, w, 3.8, fill="#ffffff", stroke="none", sw=0)
            p.text(mx, my + 0.6, lab, 2.4, ancre="middle", gras=True)

    # colonne gauche : réseau
    boite(16, 40, 58, 20, "Réseau client UE", ["400 V 3P+N+PE, TN-S", "Icc 6 kA"])
    boite(16, 78, 58, 26, "TR1 (exemplaire US)", ["TEMCo TT1041, 15 kVA", "480 V → 400 Y / 230 V", "hors armoire, posé client"],
          dash="2,1")
    boite(16, 118, 58, 14, "Réseau client US", ["480Y/277 V"], dash="2,1")
    p.poly([(45, 118), (45, 105)], sw=0.3, dash="2,1", fleche=True)
    # armoire
    A = boite(100, 30, 100, 196, "Armoire +A1", ["IDE 1800 x 1200 x 400", "QS1, QF1, U1 / U2 (SEW MCX91A),",
                                               "U3 / U4 (DM860H 48 V), K1 à K4 (S7-1200 G2),",
                                               "KA1 (sécurité), alimentations T1 à T3"], fill="#f7f7f7")
    p.rect(104, 60, 92, 20, fill="#ffffff", sw=0.2, dash="1,0.8")
    p.text(150, 66, "Borniers R5 / R4", 2.6, ancre="middle", gras=True)
    p.text(150, 71, "un groupe de bornes par câble", 2.3, ancre="middle")
    p.text(150, 75.5, "blindages repris côté armoire", 2.3, ancre="middle")
    p.text(150, 92, "Porte : AU S1, réarmement S4,", 2.4, ancre="middle")
    p.text(150, 96, "voyants H2 (230 V), H3, H4", 2.4, ancre="middle")
    fl([(74, 50), (100, 50)], "W1")
    p.poly([(74, 91), (88, 91), (88, 54)], sw=0.4, dash="2,1")
    p.text(90, 88, "US", 2.2, gras=True)
    # pupitre
    boite(100, 236, 100, 22, "Pupitre +P1 (posé sur la machine)", ["IHM P1 KTP700 Basic PN", "AU S2 · sélecteur Auto / Manu S3"])
    fl([(130, 226), (130, 236)], "W11", cote="v")
    fl([(170, 226), (170, 236)], "PN4", dash="2,1", cote="v")
    # machine à droite
    xm = 236
    p.rect(xm - 6, 24, 177, 236, fill="none", sw=0.4, dash="3,1.5", rx=2)
    p.text(xm, 29, "Machine +M", 3.4, gras=True)
    M1 = boite(xm + 70, 34, 56, 24, "M1 motoréducteur SEW", ["K39 DRN100LS4, 2,2 kW", "frein BE5 · sonde TF"])
    M2 = boite(xm + 70, 64, 56, 24, "M2 motoréducteur SEW", ["K39 DRN100LS4, 2,2 kW", "frein BE5 · sonde TF"])
    boite(xm + 70, 96, 56, 20, "M3 pas-à-pas", ["Nema 34, translation axe 1"])
    boite(xm + 70, 122, 56, 20, "M4 pas-à-pas", ["Nema 34, translation axe 2"])
    boite(xm + 2, 150, 46, 50, "Boîte +BJM", ["dérivation machine", "(une seule)"], fill="#fffbe6")
    boite(xm + 70, 150, 56, 13, "B1 capot mécanique", [])
    boite(xm + 70, 166, 56, 13, "B3 à B6 fins de course", [])
    boite(xm + 70, 182, 56, 13, "H1 colonne lumineuse", [])
    boite(xm + 70, 200, 56, 15, "B2 capot magnétique", ["capteur codé ifm MN508S (M12)"])
    boite(xm + 70, 218, 56, 15, "B7 thermocouple K", ["tête d'extrusion Microdia"])
    boite(xm + 132, 34, 37, 30, "Bâti machine", ["liaison", "équipotentielle"])
    # flèches armoire -> machine
    fl([(200, 40), (xm + 70, 40)], "W2")
    fl([(200, 50), (xm + 70, 50)], "W3")
    fl([(200, 70), (xm + 70, 70)], "W5")
    fl([(200, 80), (xm + 70, 80)], "W6")
    fl([(200, 106), (xm + 70, 106)], "W9")
    fl([(200, 132), (xm + 70, 132)], "W10")
    fl([(200, 160), (xm + 2, 160)], "W4")
    fl([(200, 185), (xm + 2, 185)], "W12")
    fl([(200, 207), (xm + 70, 207)], "W14")
    fl([(xm + 70, 222), (200, 222)], "W8")
    p.poly([(200, 33), (xm + 150, 33), (xm + 150, 34)], sw=0.4, fleche=True)
    p.rect(xm + 40, 30.4, 40, 3.8, fill="#ffffff", stroke="none", sw=0)
    p.text(xm + 60, 33, "W13 · 1 x 4 mm² V/J", 2.4, ancre="middle", gras=True)
    # boîte -> appareils (à définir)
    for yy in (156, 172, 188):
        p.poly([(xm + 48, yy), (xm + 70, yy)], sw=0.3, dash="1,1", fleche=True)
    p.poly([(xm + 30, 150), (xm + 30, 46), (xm + 70, 46)], sw=0.3, dash="1,1", fleche=True)
    p.poly([(xm + 38, 150), (xm + 38, 76), (xm + 70, 76)], sw=0.3, dash="1,1", fleche=True)
    p.text(150, 110, "PN1 à PN3 : PROFINET interne", 2.4, ancre="middle")
    p.text(150, 114, "K1 → K4 (PN1), K4 → U1 (PN2), K4 → U2 (PN3)", 2.2, ancre="middle", maxw=94)
    # légende
    y = 266
    p.text(16, y, "Lecture", 2.8, gras=True)
    p.text(16, y + 5, "Trait plein : câble de la liste (repère · composition). Tireté : PROFINET (PN4) et variante US.",
           2.4, maxw=222)
    p.text(16, y + 14, "Pointillé fin : liaisons boîte +BJM → appareils (freins BE5, B1, B3-B6, H1), non définies au schéma.",
           2.4, maxw=222)
    p.text(16, y + 9.5, "Sens des flèches : sens de l'énergie ou du signal. Repères identiques à la liste des câbles.",
           2.4, maxw=222)


# ------------------------------------------------------------------ contrôles
def ouverts():
    t = S["types_bornes"]
    besoin = {k: 0 for k in t["achetes"]}
    boite = {"PT 2,5": 0, "PT 4": 0, "terre (PT 4)": 0}
    for rep, rec in B.items():
        if rep.startswith("X1."):
            tb = type_borne(rep)
            boite["terre (PT 4)" if tb == "terre" else tb] += 1
        elif rec["type"] != "PTFIX":
            besoin[type_borne(rep)] += 1
    manque = {k: besoin[k] - t["achetes"][k] for k in besoin}
    OUVERTS.append("Boîte +BJM-X1 : bornes de terre en PT 4, largeur prise égale à la PT 4 (6,2 mm), à vérifier.")
    return besoin, manque, boite


def croisement():
    """Croise les repères et bornes écrits dans les pages avec le .xrs."""
    ecarts = []
    tous = " ".join(t for p in PAGES for t in p.textes)
    reps_pdf = set(re.findall(r"\bX\d\d\.\d\d\b", tous)) | set(re.findall(r"\bX1\.\d\d?\b", tous))
    reps_xrs = set(B)
    for r in sorted(reps_xrs - reps_pdf):
        ecarts.append(f"borne du schéma absente du dossier : {r}")
    for r in sorted(reps_pdf - reps_xrs):
        ecarts.append(f"borne du dossier absente du schéma : {r}")
    # chaque borne dessinée une seule fois dans les borniers
    vus = {}
    for br in S["borniers"] + BJM["rangees"]:
        for g in br["groupes"]:
            for r in g["bornes"]:
                vus[r] = vus.get(r, 0) + 1
    ptfix = {r for r, rec in B.items() if rec["type"] == "PTFIX"} | {"X12.11"}
    for r in sorted(reps_xrs - ptfix):
        if vus.get(r, 0) != 1:
            ecarts.append(f"borne {r} posée {vus.get(r, 0)} fois sur les rails")
    # câbles du schéma présents dans la liste, le synoptique et les borniers
    for c in D["cables_schema"]:
        if c["repere"] not in CAB:
            ecarts.append(f"câble du schéma absent de la liste : {c['repere']}")
    syn = " ".join(PAGES[-1].textes)
    if PAGES[-1].titre.startswith("Synoptique"):
        for rep in CAB:
            if not re.search(rf"\b{re.escape(rep)}\b", syn):
                ecarts.append(f"câble {rep} absent du synoptique")
    # bornes des tables de conducteurs = bornes du groupe du même câble
    for cab, lst in S["conducteurs"].items():
        bornes_cab = {r for br in S["borniers"] for g in br["groupes"] if g["cable"] == cab for r in g["bornes"]}
        # v14 : même contrôle côté boîte (borne X1 -> borne d'armoire raccordée)
        bjm = {B[r]["cote_armoire"][0].split(":")[0] for br in BJM["rangees"] for g in br["groupes"]
               if g["cable"] == cab for r in g["bornes"] if B[r]["cote_armoire"]}
        tab0 = {r for _, r in lst if r.startswith("X") and r in B}
        if bjm and not bjm <= tab0 | {"X31.11", "X32.11", "X50.13"}:
            ecarts.append(f"{cab} : bornes de la boîte raccordées à {sorted(bjm - tab0)}, absentes de la table")
        tab = {r for _, r in lst if r.startswith("X") and r in B}
        if bornes_cab and tab != bornes_cab:
            ecarts.append(f"{cab} : bornes de la table {sorted(tab ^ bornes_cab)} ≠ bornier")
    # composition et type des câbles : schéma / liste
    for c in D["cables_schema"]:
        l = CAB.get(c["repere"])
        if l and c["composition"].split(" ")[0].lower() not in (l["type"] + " " + l["conducteurs"]).replace(" x ", "x").lower():
            ecarts.append(f"{c['repere']} : schéma « {c['composition']} », liste « {l['conducteurs']} »")
    return ecarts


def main():
    besoin, manque, boite = ouverts()
    # v12 (Julien 18/11) : 2 pages seulement. Garde, charte, câbles, conducteurs et synoptique (v11) ne sont
    # plus imprimés ; leurs fonctions restent dans ce fichier. v14 (26/11) : 3e page, bornier de la boîte +BJM.
    page_plaque()
    page_borniers()
    page_boite()   # v14 : bornier +BJM-X1 (Julien 26/11 : « rajoute »)
    n = len(PAGES)
    erreurs = []
    for q in PAGES:
        erreurs += q.erreurs + q.chevauchements()
    html = ('<!doctype html><html><head><meta charset="utf-8"><title>TTK +A1</title><style>'
            '@page{size:420mm 297mm;margin:0}html,body{margin:0;padding:0}svg{display:block;break-after:page}'
            '</style></head><body>' + "".join(q.svg().replace("{N}", str(n)) for q in PAGES) + "</body></html>")
    build = os.path.join(ICI, "build")
    os.makedirs(build, exist_ok=True)
    fh = os.path.join(build, "dossier.html")
    open(fh, "w", encoding="utf-8").write(html)
    nom = f"TTK_implantation_{DOC['date'][6:]}-{DOC['date'][3:5]}-{DOC['date'][:2]}_{DOC['version']}"
    pdf = os.path.normpath(os.path.join(ICI, "..", "release", nom + ".pdf"))
    prof = os.path.join(build, "edge")
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--user-data-dir={prof}",
                    f"--print-to-pdf={pdf}", "file:///" + fh.replace("\\", "/")], check=True, capture_output=True,
                   timeout=120)
    if "--png" in sys.argv:
        dest = sys.argv[sys.argv.index("--png") + 1]
        os.makedirs(dest, exist_ok=True)
        for q in PAGES:
            f1 = os.path.join(build, f"page_{q.num:02d}.html")
            open(f1, "w", encoding="utf-8").write(
                '<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0}svg{width:2380px;'
                'height:1683px}</style></head><body>' + q.svg().replace("{N}", str(n)) + "</body></html>")
            subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={prof}",
                            "--window-size=2380,1683", f"--screenshot={os.path.join(dest, f'page_{q.num:02d}.png')}",
                            "file:///" + f1.replace("\\", "/")], check=True, capture_output=True, timeout=120)
    ecarts = croisement()
    data = open(pdf, "rb").read()
    nb_pages = len(re.findall(rb"/Type\s*/Page[^s]", data))
    rap = [f"# Contrôle de {nom}.pdf", "", f"Source : `{D['source']}` ; données : `implantation/generateur/donnees.json`.",
           f"Pages : {n} générées, {nb_pages} dans le PDF (A3 paysage).", "",
           f"## Mise en page (textes trop larges, chevauchements) : {len(erreurs)}"] + [f"- {e}" for e in erreurs] + [
           "", f"## Croisement avec le .xrs : {len(ecarts)} écart(s)"] + [f"- {e}" for e in ecarts] + [
           "", "## Points ouverts (hors dessin)"] + [f"- {o}" for o in OUVERTS] + [
           "", "## Comptage des bornes (dessinées au schéma, sans comparaison au stock : Julien 18/11)",
           "", "Armoire +A1 :"] + [f"- {k} : {v}" for k, v in besoin.items()] + [
           "", "Boîte +BJM-X1 (hors armoire) :"] + [f"- {k} : {v}" for k, v in boite.items()]
    open(os.path.join(ICI, "..", "release", nom + "_verification.md"), "w", encoding="utf-8", newline="\n").write(
        "\n".join(rap) + "\n")
    print("\n".join(rap))


if __name__ == "__main__":
    main()
