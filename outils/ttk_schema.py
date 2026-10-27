"""Schéma électrique TTK reconstruit à partir de TTK_Plan_Folios_Reperes.xlsx.

Usage : python ttk_schema.py [sortie.xrs] [tableau.xlsx]
Écrit le schéma puis affiche le contrôle (équipotentielles, chevauchements, xrs_tool.verifier).

Conventions : coordonnées en 1/100 mm, grille 400 ; repères sans « - » ; maîtres = référence
fabricant (onglet Repères), esclaves = même repère sans référence (règles R1-R3).
Tout ce que le tableau ne décide pas est marqué « PROPOSITION A VALIDER » sur le folio.
"""
import os
import sys

import lire_tableau
from xrs_gen import Gen, check

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ICI, "..", "schema", "generes", "TTK_genere.xrs")
TABLEAU = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ICI, "..", "livrables", "TTK_Plan_Folios_Reperes.xlsx")
MODELE = os.path.join(ICI, "..", "schema", "modele", "SCHEMA_ELEC_TTK.xrs")

REP = lire_tableau.reperes(TABLEAU)
FOL = lire_tableau.folios(TABLEAU)
# décisions postérieures au classeur (27/10/2026) : le classeur de Julien n'est pas modifié, voir livrables/MAJ_Reperes_2026-10-27.csv
REP["B412"].update({"fab": "ifm MN508S (RS 016-3138)", "carac": "codé - 2 NO + 1 NF - M12 - 24 V 50 mA"})
REP["S413"].update({"fab": "Eaton T0-4-8223/E", "carac": "8 contacts NO (4 par position) - numérotation provisoire"})
FOL.insert(next(i for i, f in enumerate(FOL) if f["num"] == "42") + 1,
           {"num": "43", "titre": "SECURITE - FONCTIONNEMENT", "desc": "SELECTEUR AUTO/MANU : CONTACTS, ETATS, TRANSITIONS",
            "loc": "", "maitres": ""})
for f in FOL:      # AU et sélecteur dessinés là où travaillent leurs contacts (règle R4) : f60 = IHM seule
    if f["num"] == "60":
        f["desc"] = "IHM KTP700 : ALIMENTATION ET LIAISONS DU PUPITRE"
g = Gen(MODELE)
F = {f["num"]: g.folio(f["num"], f["titre"], f["desc"]) for f in FOL}

C = "CUSTOM\\"
BORNE = "Bornes - Standard\\Borne 4 mm.xsy"
ROUGE = 255
PE_Y, RAIL24_Y, RAIL0_Y = 19400, 2000, 19000


def info(rep, **over):
    r = REP.get(rep, {"des": "", "fab": "", "carac": "", "loc": ""})
    d = {2: r["des"], 3: r["fab"], 4: r["carac"]}
    for k, v in over.items():
        d[int(k[1:])] = v
    return {k: ("" if v == "None" else v) for k, v in d.items()}


def loc(rep):
    l = REP.get(rep, {}).get("loc", "")
    return {"+A1": "A1", "+P1": "P1", "+M": "M", "Extérieur": "EXT"}.get(l)


def maitre(xsy, rep, f, x, y, ref=None, base=None, **kw):
    """Symbole maître : champs du tableau (base = repère du tableau si différent)."""
    b = base or rep
    return g.place(xsy, rep, F[f], x, y, champs=info(b), ref=ref, loc=loc(b), **kw)


def esclave(xsy, rep, f, x, y, des="", base=None, **kw):
    b = base or rep
    kw.setdefault("rep_size", 200)
    return g.place(xsy, rep, F[f], x, y, champs={2: des or REP.get(b, {}).get("des", "")}, ref=(),
                   compact=True, loc=loc(b), **kw)


def contacteur(xsy, rep, f, x, y, **kw):
    """Pôles de puissance d'un LC1D09 : mêmes infos que les autres appareils (fonction, marque + réf.,
    caractéristiques) ; la référence constructeur reste sur la bobine (f42) pour la nomenclature."""
    r = REP.get(rep, {})
    fab = r.get("fab", "").replace("Schneider ", "Schneider Electric ")
    champs = {2: r.get("des", ""), 3: fab, 4: "3P - 9 A AC-3 - bobine 24 V CC (f42)"}
    kw.setdefault("prefix", "KM" if rep.startswith("KM") else "Q")
    return g.place(xsy, rep, F[f], x, y, champs=champs, ref=(), loc=loc(rep), wrap=24, **kw)


def borne(rep, f, x, y):
    """Borne 4 mm verticale : broche 1 en (x, y), broche 2 en (x, y + 400)."""
    bornier = rep.split(".")[0]
    return g.place(BORNE, rep, F[f], x, y, champs={2: REP.get(bornier, {}).get("des", "")}, ref=(),
                   compact=True, rep_size=150, fpos=(100, -250), loc="A1", prefix="X")


def W(f, pts, t):
    return g.wire(F[f], pts, t)


def stub(f, pt, to, t):
    """Fil de pt vers to ; rend pt (point de renvoi)."""
    W(f, [pt, to], t)
    return pt


def renvoi(fa, pa, fb, pb, t, vertical=True):
    g.renvoi(F[fa], pa, F[fb], pb, t, vertical)


def texte(f, x, y, txt, size=250, color=0, bold=0):
    g.texte(F[f], x, y, txt, size, color, bold)


def notes(f, x1, y1, x2, lignes, titre="NOTES", size=180):
    """Zone de notes encadrée (une par folio) ; une ligne commençant par « ! » est écrite en rouge."""
    pas = size + 120
    y2 = y1 + 500 + pas * len(lignes) + 150
    g.cadre(F[f], x1, y1, x2, y2, width=15)
    texte(f, x1 + 150, y1 + 120, titre, 220, 0, 1)
    for i, l in enumerate(lignes):
        rouge = l.startswith("!")
        texte(f, x1 + 150, y1 + 500 + pas * i, l.lstrip("! "), size, ROUGE if rouge else 0)
    return y2


def proposition(f, lignes, x=2400, y=1400):
    texte(f, x, y, "PROPOSITION A VALIDER : " + lignes[0], 250, ROUGE, 1)
    for i, l in enumerate(lignes[1:], 1):
        texte(f, x, y + 300 * i, l, 220, ROUGE)


# ======================================================================== 01 - 04
texte("01", 4000, 3600, "MACHINE DE TRESSAGE TTK", 900, 0, 1)
texte("01", 4000, 5000, "DOSSIER DE SCHEMAS ELECTRIQUES", 600, 0, 1)
texte("01", 4000, 6200, "Client : TTK          Affaire : à compléter          N° machine : 001-EU", 300)
g.tableau(F["01"], 4000, 7600, [6000, 10000], 500, [
    ["Caractéristiques d'alimentation", ""],
    ["Réseau", "3 x 400 V + N + PE - 50 Hz (câble client -W101 5G2,5)"],
    ["Variante USA", "3 x 480 V via transformateur -T101 15 kVA (option)"],
    ["Protection de tête", "-Q102 : 20 A courbe C - 10 kA"],
    ["Régime de neutre / Icc", "TN-S / Icc présumé 6 kA au point de livraison"],
    ["Commande", "24 V CC PELV (-T301 / -T302), 48 V CC pas-à-pas (-T321)"],
    ["Puissance installée", "à calculer (2 x 2,2 kW + alimentations)"],
], size=250)
g.tableau(F["01"], 4000, 12400, [1600, 2800, 12600, 3000], 500, [
    ["Indice", "Date", "Objet", "Par"],
    ["A", "22/10/2026", "Création - reconstruction d'après TTK_Plan_Folios_Reperes.xlsx", "THRO.J"],
    ["B", "27/10/2026", "Sécurité f41-f42, câbles frein / TF séparés, E/S automate, colonne et voyants", "THRO.J"],
    ["C", "27/10/2026", "Sécurité selon fiche du 27/10, folio 43 ; -KM1 / -KM2 sans ordre automate ; -B412 MN508S", "THRO.J"],
], size=250)

rows = [["N°", "Titre", "Description", "Ind."]] + [[f["num"], f["titre"], f["desc"][:70], "A"] for f in FOL]
g.tableau(F["02"], 2400, 2000, [1200, 8400, 15200, 1200], 580, rows, size=220)

g.tableau(F["03"], 2000, 2000, [2400, 10400], 450, [
    ["Repérage", "IEC 81346-2 - règles BEBL"],
    ["Repère", "lettre de classe + n° du folio maître + rang sur ce folio (ex. -Q121)"],
    ["Maître", "porte la référence fabricant, compté en nomenclature"],
    ["Esclave", "même repère, sans référence (contacts, parties d'appareil)"],
    ["Exception", "-KM1 / -KM2 réservés aux contacteurs amont variateurs"],
    ["Localisation", "+A1 armoire, +P1 pupitre, +M machine"],
], size=220)
g.tableau(F["03"], 2000, 5600, [1200, 11600], 450, [
    ["Lettre", "Classe"], ["Q", "commutation (sectionneur, disjoncteur, contacteur)"],
    ["F", "protection"], ["K", "traitement (automate, relais, switch)"],
    ["T", "conversion (alimentation, variateur, driver, transformateur)"],
    ["M", "moteur"], ["R", "résistance"], ["S", "commande manuelle"], ["B", "capteur"],
    ["P", "signalisation / IHM"], ["G", "ventilateur"], ["E", "éclairage"],
    ["X", "connexion (borne, répartiteur)"], ["W", "câble"],
], size=220)
g.tableau(F["03"], 16000, 2000, [5200, 6400], 450, [
    ["Type de conducteur", "Couleur / usage"],
    ["Puissance", "noir - phases 400 / 230 V CA"],
    ["Neutre Puissance", "bleu clair - neutre"],
    ["Conducteur terre", "vert / jaune - PE"],
    ["Commande 24VDC", "bleu foncé - +24 V CC"],
    ["0V", "bleu - 0 V CC"],
    ["Autre tension DC", "orange - 48 V CC, signaux"],
], size=220)
g.tableau(F["03"], 16000, 5600, [3600, 8000], 450, [
    ["Potentiel", "Origine"],
    ["L1 L2 L3 N PE", "réseau via -Q101 / -Q102"],
    ["+24 V SECU", "-T302 (f30) : automate, IHM, switch, relais sécu"],
    ["+24 V AUTRE", "-T301 (f30) : variateurs (X5)"],
    ["+24 VS", "+24 V coupé par -K401 (34) et -S413 : sorties automate"],
    ["0 V", "commun -T301 / -T302, relié au PE en un point (PELV)"],
    ["+48 V / 0 V 48", "-T321 via -Q423 : drivers pas-à-pas"],
], size=220)

# synoptique
SY = F["04"]
g.cadre(SY, 2000, 2400, 18800, 17600, width=40, dashed=True)
texte("04", 2200, 2500, "+A1 ARMOIRE", 350, 0, 1)
g.cadre(SY, 20400, 2400, 28400, 8800, width=40, dashed=True)
texte("04", 20600, 2500, "+P1 PUPITRE", 350, 0, 1)
g.cadre(SY, 20400, 10000, 28400, 17600, width=40, dashed=True)
texte("04", 20600, 10100, "+M MACHINE", 350, 0, 1)
blocs = [
    (2800, 3600, "Arrivée -X101 / -Q101 / -Q102 / -F101 (f10)"),
    (2800, 4400, "Répartiteur -X111, terre -X112 (f11)"),
    (2800, 5200, "Départs 400 V : -Q121 -Q122 -KM1 -KM2 -Q123 -Q124 -Q421 -Q422 (f12)"),
    (2800, 6000, "Départs 230 V : -Q131 à -Q137, -X131, -G131 -G132, -E131 -E132 (f13)"),
    (2800, 6800, "Variateurs -T201 / -T211 + résistances -R201 / -R211 (f20, f21)"),
    (2800, 7600, "Alimentations 24 V -T301 / -T302 (f30, f31), 48 V -T321 + -Q423 (f32)"),
    (2800, 8400, "Drivers pas-à-pas -T322 / -T323 (f32)"),
    (2800, 9200, "Relais de sécurité -K401 (f40), bobines contacteurs (f42)"),
    (2800, 10000, "Automate -K501 (CPU 1214C G2), -K521 (SM 1223), -K531 (SM 1231 TC) (f50-f53)"),
    (2800, 10800, "Switch PROFINET -K541 (f54)"),
    (2800, 11600, "AU armoire -S411, réarmement -S414 (f41), colonne -P511 (f51)"),
    (2800, 12400, "Borniers -X701 (machine), -X711 (pupitre)"),
    (21000, 3600, "IHM -P601 KTP700 (f60)"),
    (21000, 4400, "AU pupitre -S412 (f41)"),
    (21000, 5200, "Sélecteur Auto/Manu -S413"),
    (21000, 10800, "Motoréducteurs -M201 / -M211"),
    (21000, 11600, "Moteurs pas-à-pas -M321 / -M322"),
    (21000, 12400, "Capots -B411 / -B412 (f41)"),
    (21000, 13200, "Fins de course -B501 à -B504 (f50)"),
    (21000, 14000, "Thermocouple tête -B531 (f53)"),
]
for x, y, t in blocs:
    texte("04", x, y, t, 250)
liaisons = [
    (11600, 1400, 11600, 2400, 11800, 1500, "-W101 réseau client 5G2,5"),
    (18800, 6000, 20400, 6000, 18900, 6600, "-W711 + PROFINET"),
    (18800, 15200, 20400, 15200, 13600, 15000, "-W201 -W202 -W203 -W211 -W212 -W213 (moteurs)"),
    (18800, 16000, 20400, 16000, 13600, 15800, "-X701 capteurs / fins de course"),
    (18800, 16800, 20400, 16800, 13600, 16600, "-W531 compensation TC"),
]
for x1, y1, x2, y2, tx, ty, t in liaisons:
    g.ligne(SY, x1, y1, x2, y2, width=40)
    texte("04", tx, ty, t, 200)
texte("04", 2400, 18200, "Le synoptique remplace l'image collée (repères et folios à jour au 27/10/2026).", 220)

# ======================================================================== règles de mise en page
# Un renvoi WinRelais dessine flèche + texte sur ~1,6 cm AU-DELA de son point, côté opposé au fil :
# barres de potentiel de XL à XR, renvois du haut à y >= 3200, renvois voisins espacés de 800.
XL, XR = 3200, 27200


def decrit(xsy, rep, f, x, y, des, **kw):
    """Esclave affichant repère + description (pour savoir à quel appareil il appartient)."""
    kw.setdefault("rep_size", 200)
    kw.setdefault("wrap", 22)
    return g.place(xsy, rep, F[f], x, y, champs={2: des}, ref=(), compact=False, shown=(2,),
                   loc=loc(rep), **kw)


# ======================================================================== 10 ARRIVEE
f = "10"
texte(f, 3600, 1400, "ARRIVEE RESEAU 3 x 400 V + N + PE - 50 Hz", 250, 0, 1)
for x, t in ((4400, "PE"), (5200, "N"), (6000, "L1"), (6800, "L2"), (7600, "L3")):
    texte(f, x - 150, 1700, t, 200)
xb = {"X101.VJ": 4400, "X101.1": 5200, "X101.2": 6000, "X101.3": 6800, "X101.4": 7600}
B = {r: borne(r, f, x, 3600) for r, x in xb.items()}
for r, x in xb.items():
    W(f, [(x, 2000), B[r]["1"]], "PE" if r.endswith("VJ") else ("N" if x == 5200 else "L"))
g.cable(F[f], 4000, 8000, 2800, "W101", "5G2,5", "Câble client", [4400, 5200, 6000, 6800, 7600])
q101 = maitre(C + "Legrand_Vistop_022515_4P_63A.xsy", "Q101", f, 5200, 5200)
q102 = maitre(C + "Hager_NFT820_disjoncteur_3P+N_20A.xsy", "Q102", f, 5200, 8000)
for r, p in (("X101.1", ("N", 0)), ("X101.2", "1/L1"), ("X101.3", "3/L2"), ("X101.4", "5/L3")):
    W(f, [B[r]["2"], q101[p]], "N" if r == "X101.1" else "L")
W(f, [B["X101.VJ"]["2"], (4400, 4400), (3600, 4400), (3600, PE_Y)], "PE")
for a, b, t in ((("N", 1), ("N", 0), "N"), ("2/T1", "1", "L"), ("4/T2", "3", "L"), ("6/T3", "5", "L")):
    W(f, [q101[a], q102[b]], t)
ends10 = {}
for pin, y in {"6": 11600, "4": 12400, "2": 13200, ("N", 1): 14000}.items():
    p = q102[pin]
    ends10[pin] = W(f, [p, (p.x, y), (XR, y)], "N" if pin == ("N", 1) else "L")
f101 = maitre(C + "Schneider_A9L16297_parafoudre_3P+N.xsy", "F101", f, 12000, 15200)
for pin, y in (("N", 14000), ("L1", 13200), ("L2", 12400), ("L3", 11600)):
    W(f, [f101[pin], (f101[pin].x, y)], "N" if pin == "N" else "L")
W(f, [(XL, PE_Y), (XR, PE_Y)], "PE")
W(f, [f101["PE"], (f101["PE"].x, PE_Y)], "PE")
t101 = maitre(C + "TEMCo_TT1041_transformateur_480D_400Y230_15kVA.xsy", "T101", f, 21200, 5600, wrap=24)
g.cadre(F[f], 18400, 2800, 28800, 10000, width=20, dashed=True)
texte(f, 18600, 2900, "VARIANTE USA (option) - réseau 3 x 480 V", 220, 0, 1)
for pin in ("H1", "H2", "H3", "GND"):
    W(f, [t101[pin], (t101[pin].x, 4400)], "PE" if pin == "GND" else "L")
for pin in ("X0", "X1", "X2", "X3"):
    W(f, [t101[pin], (t101[pin].x, 9200)], "N" if pin == "X0" else "L")
texte(f, 18600, 3500, "480 V L1 L2 L3 / PE", 200)
texte(f, 18600, 9400, "vers -X101 : N, L1, L2, L3 (à la place du réseau 400 V)", 200)

# ======================================================================== 11 REPARTITEUR
f = "11"
x111 = maitre(C + "Repartiteur_4P_125A_7departs_AEE300427.xsy", "X111", f, 4800, 9200, fpos=(14400, -4000))
entree11 = {"10": 6000, "20": 6800, "30": 7600, "N0": 8400}
for pin, y in entree11.items():
    W(f, [(4000, y), x111[pin]], "N" if pin == "N0" else "L")
for q102pin, x111pin in (("6", "10"), ("4", "20"), ("2", "30"), (("N", 1), "N0")):
    renvoi("10", ends10[q102pin], "11", (4000, entree11[x111pin]), "N" if x111pin == "N0" else "L")
dep11 = ["11", "21", "31", "12", "22", "32", "13", "23", "14", "34", "15", "N5", "26", "N6", "37", "N7"]
pts11 = {}
for i, pin in enumerate(sorted(dep11, key=lambda p: x111[p].x)):
    pts11[pin] = W(f, [x111[pin], (x111[pin].x, 10400 if i % 2 == 0 else 12000)], "N" if pin.startswith("N") else "L")
for x, t in ((7200, "VARIATEUR 1"), (8800, "VARIATEUR 2"), (10400, "FREIN 1"), (12000, "FREIN 2"),
             (13600, "24 V"), (15600, "48 V"), (17600, "230 V AUX.")):
    texte(f, x, 14000, t, 200)
x112 = maitre(C + "Legrand_404839_bornier_terre_27.xsy", "X112", f, 4800, 16400, fpos=(12800, -1200))
W(f, [(XL, PE_Y), (XR, PE_Y)], "PE")
W(f, [x112["E"], (x112["E"].x, PE_Y)], "PE")
fe11 = {"1": stub(f, (22400, 17600), (22400, PE_Y), "PE"), "2": stub(f, (23200, 17600), (23200, PE_Y), "PE")}
texte(f, 23600, 17000, "FE -K501 (f50), FE -P601 (f60)", 200)

# ======================================================================== 12 DISTRIBUTION 400 V
f = "12"
gv = C + "Schneider_GV2ME14_disjoncteur_moteur.xsy"
poles = C + "Schneider_LC1D09BD_contacts_puissance_3P.xsy"
q121 = maitre(gv, "Q121", f, 3200, 3600)
km1p = contacteur(poles, "KM1", f, 3200, 8400, prefix="KM")
q122 = maitre(gv, "Q122", f, 11200, 3600)
km2p = contacteur(poles, "KM2", f, 11200, 8400, prefix="KM")
q123 = maitre(C + "Schneider_A9F74202_iC60N_2P_2A_C.xsy", "Q123", f, 17600, 3600)
q421p = contacteur(poles, "Q421", f, 16800, 8400)
q124 = maitre(C + "Schneider_A9F74202_iC60N_2P_2A_C.xsy", "Q124", f, 23200, 3600)
q422p = contacteur(poles, "Q422", f, 22400, 8400)
in12 = {}
for q, pins in ((q121, ("1/L1", "3/L2", "5/L3")), (q122, ("1/L1", "3/L2", "5/L3")),
                (q123, ("1", "3")), (q124, ("1", "3"))):
    for p in pins:
        in12[(q.rep, p)] = stub(f, (q[p].x, 3200), q[p], "L")
for q, k in ((q121, km1p), (q122, km2p)):
    for a, b in (("2/T1", "1/L1"), ("4/T2", "3/L2"), ("6/T3", "5/L3")):
        W(f, [q[a], k[b]], "L")
for q, k in ((q123, q421p), (q124, q422p)):
    W(f, [q["2"], k["3/L2"]], "L")
    W(f, [q["4"], k["5/L3"]], "L")
out12 = {}
for k in (km1p, km2p):
    for p in ("2/T1", "4/T2", "6/T3"):
        out12[(k.rep, p)] = W(f, [k[p], (k[p].x, 11600)], "L")
for k in (q421p, q422p):
    for p in ("4/T2", "6/T3"):
        out12[(k.rep, p)] = W(f, [k[p], (k[p].x, 11600)], "L")
for x, t in ((2800, "VARIATEUR 1"), (10800, "VARIATEUR 2"), (16400, "FREIN M201"), (22000, "FREIN M211")):
    texte(f, x, 13600, t, 200)
for x111pin, key in (("11", ("Q121", "1/L1")), ("21", ("Q121", "3/L2")), ("31", ("Q121", "5/L3")),
                     ("12", ("Q122", "1/L1")), ("22", ("Q122", "3/L2")), ("32", ("Q122", "5/L3")),
                     ("13", ("Q123", "1")), ("23", ("Q123", "3")), ("14", ("Q124", "1")), ("34", ("Q124", "3"))):
    renvoi("11", pts11[x111pin], "12", in12[key], "L")

# ======================================================================== 13 DISTRIBUTION 230 V
f = "13"
nft = C + "Hager_NFT706_disjoncteur_1P+N_6A_C.xsy"
q132 = maitre(nft, "Q132", f, 2400, 4800)
q133 = maitre(nft, "Q133", f, 8800, 4800)
q134 = maitre(C + "Schneider_A9F75204_iC60N_2P_4A_D.xsy", "Q134", f, 15200, 4800)
W(f, [(2400, 3200), q132[("N", 0)]], "N")
W(f, [(3200, 3200), q132["1"]], "L")
W(f, [(2400, 3600), (8800, 3600), q133[("N", 0)]], "N")
W(f, [(3200, 4000), (9600, 4000), q133["1"]], "L")
renvoi("11", pts11["N5"], f, (2400, 3200), "N")
renvoi("11", pts11["15"], f, (3200, 3200), "L")
W(f, [(15200, 3200), q134["1"]], "N")
W(f, [(16000, 3200), q134["3"]], "L")
renvoi("11", pts11["N6"], f, (15200, 3200), "N")
renvoi("11", pts11["26"], f, (16000, 3200), "L")
out13 = {}
for q, pn, pl in ((q132, ("N", 1), "2"), (q133, ("N", 1), "2"), (q134, "2", "4")):
    out13[(q.rep, "N")] = W(f, [q[pn], (q[pn].x, 7600)], "N")
    out13[(q.rep, "L")] = W(f, [q[pl], (q[pl].x, 7600)], "L")
q137 = maitre(nft, "Q137", f, 4400, 11200, ref=())
q136 = maitre(nft, "Q136", f, 11200, 11200, ref=())
q131 = maitre(C + "IMO_B6CR1N1630A_disj_diff_1P+N_16A_30mA.xsy", "Q131", f, 18000, 11200)
W(f, [(XL, 10400), (18000, 10400), q131[("N", 0)]], "N")
W(f, [(XL, 9600), (18800, 9600), q131["1"]], "L")
for q in (q137, q136):
    W(f, [(q[("N", 0)].x, 10400), q[("N", 0)]], "N")
    W(f, [(q["1"].x, 9600), q["1"]], "L")
renvoi("11", pts11["N7"], f, (XL, 10400), "N")
renvoi("11", pts11["37"], f, (XL, 9600), "L")
q135 = maitre(C + "Schneider_A9P71606_iDT40K_disjoncteur_1PN_6A_C.xsy", "Q135", f, 21600, 14400)
x131 = maitre(C + "Legrand_004280_prise_2P+T_16A.xsy", "X131", f, 21600, 17200)
W(f, [q131[("N", 1)], (18000, 14400), q135[("N", 0)]], "N")
W(f, [q131["2"], (18800, 14000), (22400, 14000), q135["1"]], "L")
W(f, [q135[("N", 1)], x131["N"]], "N")
W(f, [q135["2"], x131["L"]], "L")
lampe = C + "RSPRO_194-0417_eclairage_armoire_LED.xsy"
e131 = maitre(lampe, "E131", f, 4400, 15600)
e132 = maitre(lampe, "E132", f, 7600, 15600)
W(f, [q137[("N", 1)], e131["N"]], "N")
W(f, [(4400, 14800), (7600, 14800), e132["N"]], "N")
W(f, [q137["2"], (5200, 14400), (9200, 14400), e132["L"]], "L")
W(f, [(6000, 14400), e131["L"]], "L")
vent = C + "IDE_VF92AC_ventilateur_230V.xsy"
g131 = maitre(vent, "G131", f, 11200, 15600)
g132 = maitre(vent, "G132", f, 14800, 15600)
W(f, [q136[("N", 1)], g131["N"]], "N")
W(f, [(11200, 14800), (14800, 14800), g132["N"]], "N")
W(f, [q136["2"], g131["L"]], "L")
W(f, [(12000, 14400), (15600, 14400), g132["L"]], "L")
W(f, [(XL, PE_Y), (XR, PE_Y)], "PE")
W(f, [x131["PE"], (x131["PE"].x, PE_Y)], "PE")
# phase de chaque départ (X111 : 1er chiffre = phase, 2e = n° de départ)
for x, y, ph in ((3300, 4300, "L1"), (9700, 4300, "L1"), (16100, 3700, "L2"), (6400, 9200, "L3")):
    texte(f, x, y, ph, 200, 16711680)
texte(f, 2400, 18000, "Phases : 24 V sur L1 (X111 départ 5), 48 V sur L2 (départ 6), 230 V aux. sur L3 (départ 7)", 200)
texte(f, 2400, 18400, "Q12 / Q13 supprimés (décision 04/10) : coupure 48 V par -Q423 seul, sorties coupées par -K401.", 200)

# ======================================================================== 20 / 21 VARIATEURS
mcx = C + "SEW_Variateur_MCX91A-0055-5E3_CSO_CFN.xsy"
mot = C + "SEW_K39-DRN100LS4-BE5-TF_motoreducteur_frein.xsy"
res = C + "SEW_BW100-001_resistance_freinage.xsy"
VAR = {}
for f, t, r, m, w1, w2, w3, km, qf in (("20", "T201", "R201", "M201", "W201", "W202", "W203", "KM1", "Q421"),
                                       ("21", "T211", "R211", "M211", "W211", "W212", "W213", "KM2", "Q422")):
    T = maitre(mcx, t, f, 4000, 6000, wrap=34)
    R = maitre(res, r, f, 9600, 10000, shown=(2,), wrap=22)
    M = maitre(mot, m, f, 5200, 15600, fpos=(10000, 0), wrap=36)   # textes à droite du moteur
    for p, kp in (("X1:L1", "2/T1"), ("X1:L2", "4/T2"), ("X1:L3", "6/T3")):
        renvoi("12", out12[(km, kp)], f, stub(f, (T[p].x, 4800), T[p], "L"), "L")
    W(f, [T["X1:PE"], (4000, 5200), (3600, 5200), (3600, PE_Y)], "PE")
    W(f, [(XL, PE_Y), (XR, PE_Y)], "PE")
    W(f, [T["X2:PE"], (4000, 12000), (4400, 12000), M["PE"]], "PE")
    W(f, [(4000, 9600), (3600, 9600)], "PE")
    W(f, [T["X2:U"], (4800, 12400), (5200, 12400), M["U1"]], "L")
    W(f, [T["X2:V"], (5600, 12800), (6000, 12800), M["V1"]], "L")
    W(f, [T["X2:W"], (6400, 13200), (6800, 13200), M["W1"]], "L")
    g.cable(F[f], 4000, 7000, 14400, w1, "4G2,5 blindé", "Câble moteur CEM", [4400, 5200, 6000, 6800],
            etiq=(1600, 13800), size=200)
    W(f, [T["X2:-R"], (8000, 9600), (9600, 9600), R["1"]], "DC")
    W(f, [T["X2:+R"], (7200, 12000), (9600, 12000), R["2"]], "DC")
    # frein (2G1,5) et sonde TF (2G1 blindé) : câbles séparés, en direct (sans bornier), décision 26/10
    renvoi("12", out12[(qf, "4/T2")], f, W(f, [M["2"], (M["2"].x, 12000), (13600, 12000)], "L"), "L")
    renvoi("12", out12[(qf, "6/T3")], f, W(f, [M["3"], (M["3"].x, 11200), (13600, 11200)], "L"), "L")
    W(f, [M["1b"], (M["1b"].x, 12800), (21200, 12800), (21200, 5200), (11600, 5200), T["X10:1"]], "24")
    W(f, [M["2b"], (M["2b"].x, 12400), (21600, 12400), (21600, 5600), (12000, 5600), T["X10:2"]], "24")
    g.cable(F[f], M["1b"].x - 400, M["2b"].x + 400, 14400, w3, "2G1 blindé", "Câble sonde TF CEM",
            [M["1b"].x, M["2b"].x], etiq=(14800, 13800), size=200)
    g.cable(F[f], M["2"].x - 400, M["3"].x + 400, 14400, w2, "2G1,5", "Câble frein 400 V CA",
            [M["2"].x, M["3"].x], etiq=(12000, 13800), size=200)
    VAR[(f, "24")] = W(f, [T["X5:24V"], (7600, 4800)], "24")
    VAR[(f, "0V")] = W(f, [T["X5:GND"], (8000, 3200)], "0V")
    VAR[(f, "STO1")] = W(f, [T["X6:1"], (8800, 4800)], "24")
    VAR[(f, "STO2")] = W(f, [T["X6:3"], (9600, 3200)], "24")
    W(f, [T["X6:2"], (9200, 5200), (10000, 5200)], "0V")
    W(f, [T["X6:4"], (10000, 5200)], "0V")
    VAR[(f, "STO0")] = W(f, [(10000, 5200), (10000, 4800)], "0V")
    texte(f, 22400, 4400, "X40 : PROFINET -> -K541 (f54)", 200)
    texte(f, 22400, 4800, "X5 : +24 V AUTRE (f31) - X6 : STO (f42)", 200)
    texte(f, 22400, 5200, "STO X6 et TF X10 : bornes à confirmer", 200, ROUGE)
    texte(f, 22400, 5600, "(notice SEW MCX91A)", 200, ROUGE)
    texte(f, 22400, 6400, f"{w1} / {w3} blindés : blindage repris à 360°", 200)
    texte(f, 22400, 6800, "(presse-étoupe CEM côté moteur,", 200)
    texte(f, 22400, 7200, "collier de masse côté variateur)", 200)

# ======================================================================== 30 ALIMENTATIONS 24 V
f = "30"
alim = C + "RSPRO_284-0491_alim_24V_240W.xsy"
t301 = maitre(alim, "T301", f, 4000, 5200)
t302 = maitre(alim, "T302", f, 16000, 5200)
for T, q in ((t301, "Q132"), (t302, "Q133")):
    renvoi("13", out13[(q, "N")], f, stub(f, (T["N"].x, 3600), T["N"], "N"), "N")
    renvoi("13", out13[(q, "L")], f, stub(f, (T["L"].x, 3600), T["L"], "L"), "L")
W(f, [t301["PE"], (3600, PE_Y)], "PE")
W(f, [t302["PE"], (14400, 6000), (14400, PE_Y)], "PE")
W(f, [(XL, PE_Y), (XR, PE_Y)], "PE")
a24 = W(f, [t301[("+V", 0)], (5200, 10400), (XR, 10400)], "24")
s24 = W(f, [t302[("+V", 0)], (17200, 11200), (XR, 11200)], "24")
z30 = W(f, [t301[("-V", 0)], (4000, 12000), (XR, 12000)], "0V")
W(f, [t302[("-V", 0)], (16000, 12000)], "0V")
texte(f, 20000, 9900, "+24 V AUTRE (-T301)", 220)
texte(f, 20000, 10700, "+24 V SECU (-T302)", 220)
texte(f, 20000, 11500, "0 V commun", 220)
texte(f, 4400, 13200, "PELV : 0 V relié au PE en un point unique,", 220)
texte(f, 4400, 13600, "par borne sectionnable (à définir), non dessiné pour", 220)
texte(f, 4400, 14000, "garder des potentiels distincts (règle VRE 106p1)", 220)

# ======================================================================== 31 DISTRIBUTION 24 V
f = "31"
ptf = C + "Phoenix_3002781_PTFIX_6x1.5_BK.xsy"
DESC31 = {"X311": "Distribution +24 V SECU", "X312": "Distribution 0 V", "X313": "Distribution +24 V AUTRE"}
P31 = {}
for rep, x, y in (("X311", 6000, 6400), ("X312", 6000, 15200), ("X313", 16000, 6400)):
    P31[rep] = g.place(ptf, rep, F[f], x, y, champs={2: DESC31[rep], 3: "Phoenix 3002781 PTFIX 6X1,5-BK",
                                                    4: "6 points - 17,5 A"}, loc="A1", wrap=34)
x311, x312, x313 = P31["X311"], P31["X312"], P31["X313"]
W(f, [(XL, 11200), (4800, 11200), (4800, 5600), (6000, 5600), x311["1"]], "24")
W(f, [(XL, 12000), (4000, 12000), (4000, 14800), (6000, 14800), x312["1"]], "0V")
W(f, [(XL, 10400), (14800, 10400), (14800, 5600), (16000, 5600), x313["1"]], "24")
renvoi("30", a24, f, (XL, 10400), "24")
renvoi("30", s24, f, (XL, 11200), "24")
renvoi("30", z30, f, (XL, 12000), "0V")
W(f, [x311["2"], (6400, RAIL24_Y), (XR, RAIL24_Y)], "24")
W(f, [x312["4"], (6000, RAIL0_Y), (XR, RAIL0_Y)], "0V")
d31 = {"0V20": W(f, [x312["5"], (6400, 16800), (8800, 16800)], "0V"),
       "0V21": W(f, [x312["6"], (6800, 17600), (8800, 17600)], "0V"),
       "0V32a": W(f, [x312["2"], (6400, 14400), (8800, 14400)], "0V"),
       "0V32b": W(f, [x312["3"], (6800, 13600), (8800, 13600)], "0V"),
       "24V20": W(f, [x313["2"], (16400, 4800)], "24"), "24V21": W(f, [x313["5"], (16400, 8000)], "24")}
for ff in ("20", "21"):
    renvoi(f, d31["24V" + ff], ff, VAR[(ff, "24")], "24")
    renvoi(f, d31["0V" + ff], ff, VAR[(ff, "0V")], "0V")
REP["P512"] = {"des": "Voyant porte : tension de commande présente", "fab": "À définir", "carac": "24 V CC - blanc ou vert", "loc": "+A1"}
p512 = decrit("Signalisation et voyants\\Voyant.xsy", "P512", f, 24800, 8800, "Voyant porte : tension de commande présente",
              fpos=(600, 400), wrap=20, prefix="P")
W(f, [p512["X1"], (24800, RAIL24_Y)], "24")
W(f, [p512["X2"], (24800, RAIL0_Y)], "0V")
texte(f, 7600, 2200, "+24 V SECU -> f40 à f60 : relais sécu, CPU, IHM, switch, modules", 200)
texte(f, 7600, 18600, "0 V -> f40 à f60", 200)
texte(f, 17600, 3600, "+24 V AUTRE -> X5 des variateurs (f20, f21)", 200)
proposition(f, ["répartition des départs 24 V entre -T301 et -T302,",
                "repères -X311 / -X312 / -X313 à ajouter au tableau"], x=12000, y=14400)

# ======================================================================== 32 48 V ET PAS-A-PAS
f = "32"
t321 = maitre(C + "MeanWell_NDR-240-48_alim_48V_240W.xsy", "T321", f, 4000, 5200)
for p, side in (("N", "N"), ("L", "L")):
    renvoi("13", out13[("Q134", side)], f, stub(f, (t321[p].x, 3600), t321[p], side), side)
q423p = contacteur(poles, "Q423", f, 3600, 8400)
W(f, [t321[("-V", 1)], q423p["3/L2"]], "0V")
W(f, [t321[("+V", 0)], q423p["5/L3"]], "DC")
W(f, [q423p["6/T3"], (5200, 11200), (24000, 11200)], "DC")
W(f, [q423p["4/T2"], (4400, 11600), (24800, 11600)], "0V")
W(f, [t321["PE"], (2800, 6000), (2800, PE_Y), (3600, PE_Y)], "PE")
drv = C + "Jkongmotor_JKDM860H_driver_pas-a-pas.xsy"
mpp = C + "StepperOnline_34IP65-85_moteur_pas-a-pas.xsy"
CMD32 = {}
for T, Mrep, x0 in (("T322", "M321", 12000), ("T323", "M322", 24000)):
    D = maitre(drv, T, f, x0, 12400)
    Mo = maitre(mpp, Mrep, f, x0 - 800, 16000)
    W(f, [(x0, 11200), D["+V"]], "DC")
    W(f, [(x0 + 800, 11600), D["-V"]], "0V")
    for p in ("A+", "A-", "B+", "B-"):
        W(f, [D[p], Mo[p]], "DC")
    xin, xbus = x0 - 4000, x0 - 3200
    for s in ("PUL", "DIR", "ENA"):
        CMD32[(T, s)] = W(f, [D[s + "+"], (xin, D[s + "+"].y)], "24")
        W(f, [D[s + "-"], (xbus, D[s + "-"].y)], "0V")
    CMD32[(T, "0V")] = W(f, [(xbus, D["PUL-"].y), (xbus, 15600)], "0V")
renvoi("31", d31["0V32a"], f, CMD32[("T322", "0V")], "0V")
renvoi("31", d31["0V32b"], f, CMD32[("T323", "0V")], "0V")
texte(f, 8800, 10800, "+48 V", 200)
texte(f, 8800, 11800, "0 V 48", 200)

# ======================================================================== chaînes PE et +24 V / 0 V
PEC = [("10", None, (XR, PE_Y)), ("11", (XL, PE_Y), (XR, PE_Y)), ("13", (XL, PE_Y), (XR, PE_Y)),
       ("20", (XL, PE_Y), (XR, PE_Y)), ("21", (XL, PE_Y), (XR, PE_Y)), ("30", (XL, PE_Y), (XR, PE_Y)),
       ("32", (3600, PE_Y), None)]
for (fa, _, ra), (fb, lb, _) in zip(PEC, PEC[1:]):
    renvoi(fa, ra, fb, lb, "PE")
for fpe, _, _ in PEC[:-1]:
    texte(fpe, 24000, PE_Y - 300, "PE", 200)
CH = ["31", "40", "41", "42", "43", "50", "51", "52", "53", "54", "60"]
for i, f in enumerate(CH[1:], 1):
    last = f == "60"
    W(f, [(XL, RAIL24_Y), (3600 if last else XR, RAIL24_Y)], "24")
    W(f, [(XL, RAIL0_Y), (7200 if last else XR, RAIL0_Y)], "0V")
    renvoi(CH[i - 1], (XR, RAIL24_Y), f, (XL, RAIL24_Y), "24")
    renvoi(CH[i - 1], (XR, RAIL0_Y), f, (XL, RAIL0_Y), "0V")
for f in CH:
    texte(f, 24000, RAIL24_Y - 300, "+24 V SECU", 200)
    texte(f, 24000, RAIL0_Y - 300, "0 V", 200)

# ======================================================================== 40 RELAIS DE SECURITE
f = "40"
k401 = maitre(C + "Schneider_XPSUAF13AP_relais_securite.xsy", "K401", f, 4400, 8000)
W(f, [k401["A1"], (4400, RAIL24_Y)], "24")
W(f, [k401["A2"], (4400, RAIL0_Y)], "0V")
for p in ("13", "23", "33"):
    W(f, [k401[p], (k401[p].x, RAIL24_Y)], "24")
S40 = {p: W(f, [k401[p], (k401[p].x, 4800)], "24") for p in ("S11", "S12", "S21", "S22")}
O40 = {p: W(f, [k401[p], (k401[p].x, 11200)], "24") for p in ("14", "24", "34")}
miroir = C + "Schneider_LC1D09BD_contact_aux_NC_21-22_miroir.xsy"
prev = W(f, [k401["Y1"], (8400, 2800), (20000, 2800), (20000, 3200)], "24")
DESC_KM = {"KM1": "contacteur amont variateur 1", "KM2": "contacteur amont variateur 2",
           "Q421": "contacteur frein M1", "Q422": "contacteur frein M2", "Q423": "contacteur coupure 48 V"}
for i, rep in enumerate(DESC_KM):
    c = decrit(miroir, rep, f, 20000, 3200 + 2400 * i, f"Retour {DESC_KM[rep]}",
               prefix="KM" if rep.startswith("KM") else "Q", wrap=24, fpos=(2200, 200))
    if i:
        W(f, [prev, c["21"]], "24")
    prev = c["22"]
y_s414 = W(f, [prev, (20000, 15200)], "24")
y2 = W(f, [k401["Y2"], (9200, 6000)], "24")
texte(f, 20800, 2400, "Boucle de retour Y1-Y2 : contacts miroir + réarmement -S414 (f41)", 200)
notes(f, 4400, 13200, 19200, [
    "Relais -K401 : AU + capot, arrêt catégorie 0 (pas de sortie temporisée), PL d visé.",
    "Entrées : voie 1 S11-S12, voie 2 S21-S22 (f41) sur sorties de test distinctes.",
    "Sorties (f42) : 13-14 = freins -Q421 / -Q422 + 48 V -Q423 via Manu-D ;",
    "23-24 = Auto-A -> -KM1 / -KM2 (sans ordre automate) ; 33-34 = Auto-B -> STO.",
    "Réarmement -S414 en série avec la boucle de retour (NF miroir des 5 LC1D09BD).",
    "Réglages : FONCTION 1 (AU + protecteurs, entrées dynamisées, surveillance S12-S22),",
    "DEPART 3 (démarrage surveillé, sans test au démarrage, avec dynamisation).",
    "! B2 et Z1 non raccordées : à confirmer (notice XPSUAF13AP).",
    "! Sortie diagnostic statique -> automate I1.5 : borne absente du symbole (notice).",
    "! Affectation des sorties 1 / 2 / 3 à valider.",
])

# ======================================================================== 41 SECURITE - ENTREES
f = "41"
au = "BP & Commut & Voyants\\Arret urgence NC déverr tournant.xsy"
nc2 = "--- X Contact\\RC Contact NC 21-22.xsy"
# -S413 (Eaton T0-4-8223/E, essai du 27/10 : 4 contacts NO par position, 8 en tout, numérotation provisoire)
#   position 1 = Auto : 13-14 STO, 23-24 ordre contacteurs, 33-34 information automate, 43-44 réserve
#   position 2 = Manu : 53-54 pontage capot voie 1, 63-64 pontage capot voie 2, 73-74 information automate, 83-84 réserve
CT = {n: f"--- X Contact\\RC Contact NO {n}-{n + 1}.xsy" for n in (13, 23, 33, 43, 53, 63, 73, 83)}
VOIES = {}
for voie, x, s1, s2, cap, capxsy, bornes, src, ret, byp in (
        (1, 7200, "S411", "S412", "B411", C + "RSPRO_902-6874_interrupteur_position.xsy",
         ("X711.1", "X711.2", "X701.1", "X701.2", "X701.3", "X701.4"), "S11", "S12", (53, ("X711.13", "X711.14"))),
        (2, 17200, "S411", "S412", "B412", C + "ifm_MN508S_capteur_magnetique_code.xsy",
         ("X711.3", "X711.4", "X701.5", "X701.6", "X701.7", "X701.8"), "S21", "S22", (63, ("X711.15", "X711.16")))):
    if voie == 1:
        c1 = maitre(au, s1, f, x, 4400, prefix="S")
        c2 = maitre(au, s2, f, x, 8000, prefix="S")
        p1, p2 = ("1", "2"), ("1", "2")
    else:
        c1 = decrit(nc2, s1, f, x, 4400, "AU armoire - 2e contact NF (voie 2)")
        c2 = decrit(nc2, s2, f, x, 8000, "AU pupitre (+P1) - 2e contact NF (voie 2)")
        p1, p2 = ("21", "22"), ("21", "22")
    top = stub(f, (x, 4000), c1[p1[0]], "24")
    ta, tb, tc, td, te, tf = bornes
    b1, b2 = borne(ta, f, x, 6800), borne(tb, f, x, 10400)
    b3, b4 = borne(tc, f, x, 11600), borne(td, f, x, 15200)
    cp = maitre(capxsy, cap, f, x, 12800)
    for a_, b_ in ((c1[p1[1]], b1["1"]), (b1["2"], c2[p2[0]]), (c2[p2[1]], b2["1"]), (b2["2"], b3["1"]),
                   (b3["2"], cp["11"]), (cp["12"], b4["1"])):
        W(f, [a_, b_], "24")
    bot = stub(f, (x, 16400), b4["2"], "24")
    # pontage du capot par -S413 position Manu (contact NO en parallèle de la chaîne -X701 / capot)
    n_c, (bya, byb) = byp
    xb = x - 3200
    ba, bb = borne(bya, f, xb, 11600), borne(byb, f, xb, 15200)
    ctc = decrit(CT[n_c], "S413", f, xb, 12800, f"Manu-{'AB'[voie - 1]} : shunt capot voie {voie}", wrap=12)
    W(f, [(x, 11200), (xb, 11200), ba["1"]], "24")
    W(f, [ba["2"], ctc[str(n_c)]], "24")
    W(f, [ctc[str(n_c + 1)], bb["1"]], "24")
    W(f, [bb["2"], (xb, 16000), (x, 16000)], "24")
    renvoi("40", S40[src], f, top, "24")
    renvoi("40", S40[ret], f, bot, "24")
    # contact NO du capot -> automate (f50)
    t1, t2 = borne(te, f, x + 800, 12000), borne(tf, f, x + 800, 14800)
    plus = W(f, [t1["1"], (x + 800, 11600), (x + 2800, 11600)], "24")
    W(f, [t1["2"], cp["23"]], "24")
    W(f, [cp["24"], t2["1"]], "24")
    entree = W(f, [t2["2"], (x + 800, 16000), (x + 2800, 16000)], "24")
    VOIES[cap] = (plus, entree)
s414 = maitre("BP & Commut & Voyants\\BP lumineux NO.xsy", "S414", f, 21600, 4400, prefix="S", fpos=(600, 0))
a414 = stub(f, (21600, 4000), s414["3"], "24")
b414 = W(f, [s414["4"], (21600, 6800)], "24")
renvoi("40", y_s414, f, a414, "24")
renvoi(f, b414, "40", y2, "24")
maitre("Poussoirs et commutateurs\\Tête 2 pos fixes NO.xsy", "S413", f, 21600, 9600, prefix="S", fpos=(600, 0))
notes(f, 22000, 12400, 29400, [
    "Voie 1 : AU armoire NF1 - AU pupitre NF1 -",
    "         [capot mécanique -B411 NF  OU  Manu-A]",
    "Voie 2 : AU armoire NF2 - AU pupitre NF2 -",
    "         [capot magnétique -B412  OU  Manu-B]",
    "Un contact Manu par voie, jamais commun.",
    "Contacts NO des capots -> automate (discordance).",
    "! -S413 : numérotation provisoire (photo plaque).",
    "! -B412 (ifm MN508S, 2 NO + 1 NF) : 1 NO en voie 2,",
    "! NF vers I0.3, 2e NO en réserve ; brochage M12 à relever.",
])

# ======================================================================== 42 SECURITE - SORTIES
# Architecture du 27/10 (fiche de Julien) :
#   sortie 1 (13-14) -> bobines freins -Q421 / -Q422, et via Manu-D -> bobine -Q423 (48 V en Manu seulement)
#   sortie 2 (23-24) -> Auto-A -> bobines -KM1 / -KM2 (pas d'ordre automate, option A du 27/10)
#   sortie 3 (33-34) -> Auto-B -> STO des 2 variateurs en parallèle
f = "42"
bob = C + "Schneider_LC1D09BD_contacteur_bobine.xsy"
YC = 12800                                  # ligne des bobines


def chaine_s413(x, ba, bb, n_c, des, y0=4400):
    """Borne -X711 / contact -S413 / borne -X711, de haut en bas ; rend (entrée, borne de sortie)."""
    t1 = borne(ba, f, x, y0)
    c = decrit(CT[n_c], "S413", f, x, y0 + 1200, des, wrap=18)
    t2 = borne(bb, f, x, y0 + 3600)
    W(f, [t1["2"], c[str(n_c)]], "24")
    W(f, [c[str(n_c + 1)], t2["1"]], "24")
    return t1, t2


COIL = {}
for rep, x, pref in (("Q421", 4400, "Q"), ("Q422", 7600, "Q"), ("Q423", 11200, "Q"),
                     ("KM1", 15200, "KM"), ("KM2", 18400, "KM")):
    k = maitre(bob, rep, f, x, YC, ref=("SCHNEIDER ELECTRIC", "", "LC1D09BD"), prefix=pref, wrap=16)
    W(f, [k["A2"], (x, RAIL0_Y)], "0V")
    COIL[rep] = k
# --- sortie 1 : freins (toujours, seul l'AU les coupe) et 48 V (Manu-D)
s1 = (4400, 4000)
W(f, [s1, COIL["Q421"]["A1"]], "24")
W(f, [(4400, 4800), (11200, 4800)], "24")
W(f, [(7600, 4800), COIL["Q422"]["A1"]], "24")
t1, t2 = chaine_s413(11200, "X711.19", "X711.20", 83, "Manu-D : 48 V en Manu seulement", y0=5600)
W(f, [(11200, 4800), t1["1"]], "24")
W(f, [t2["2"], COIL["Q423"]["A1"]], "24")
renvoi("40", O40["14"], f, s1, "24")
texte(f, 4800, 3000, "Sortie 1 (13-14) : freins + 48 V", 220, 0, 1)
# --- sortie 2 : Auto-A -> -KM1 / -KM2 (pas d'ordre automate, décision du 27/10, option A)
t1, t2 = chaine_s413(15200, "X711.7", "X711.8", 13, "Auto-A : commande -KM1 / -KM2")
s2 = stub(f, (15200, 4000), t1["1"], "24")
W(f, [t2["2"], COIL["KM1"]["A1"]], "24")
W(f, [(15200, 12000), (18400, 12000), COIL["KM2"]["A1"]], "24")
renvoi("40", O40["24"], f, s2, "24")
texte(f, 15600, 3000, "Sortie 2 (23-24) : -KM1 / -KM2", 220, 0, 1)
# --- sortie 3 : Auto-B -> STO des 2 variateurs (validé SEW)
t1, t2 = chaine_s413(21600, "X711.9", "X711.10", 23, "Auto-B : autorisation STO")
s3 = stub(f, (21600, 4000), t1["1"], "24")
W(f, [t2["2"], (21600, 10400)], "24")
W(f, [(21600, 9200), (24000, 9200)], "24")
for xx in (22400, 23200, 24000):
    W(f, [(xx, 9200), (xx, 10400)], "24")
renvoi("40", O40["34"], f, s3, "24")
renvoi(f, (21600, 10400), "20", VAR[("20", "STO1")], "24")
renvoi(f, (22400, 10400), "20", VAR[("20", "STO2")], "24")
renvoi(f, (23200, 10400), "21", VAR[("21", "STO1")], "24")
renvoi(f, (24000, 10400), "21", VAR[("21", "STO2")], "24")
texte(f, 22000, 3000, "Sortie 3 (33-34) : STO", 220, 0, 1)
texte(f, 21200, 12400, "STO X6 des 2 variateurs", 200)
texte(f, 21200, 12700, "en parallèle (validé SEW)", 200)
g0 = {"20": W(f, [(21600, RAIL0_Y), (21600, 17600)], "0V"), "21": W(f, [(22400, RAIL0_Y), (22400, 17600)], "0V")}
renvoi(f, g0["20"], "20", VAR[("20", "STO0")], "0V")
renvoi(f, g0["21"], "21", VAR[("21", "STO0")], "0V")
texte(f, 23200, 17600, "0 V STO X6 (f20, f21)", 200)
notes(f, 25200, 4000, 29400, [
    "Freins : coupés par l'AU ou",
    "le capot en Auto, jamais par",
    "le changement de mode.",
    "48 V pas-à-pas : en Manu",
    "seulement (Manu-D).",
    "-KM1 / -KM2 : fermés dès que",
    "le relais est armé en Auto",
    "(pas d'ordre automate).",
    "Arrêt de service : rampe + STO,",
    "pas -KM1 / -KM2.",
    "STO : Auto-B, entrées X6 des",
    "2 variateurs en parallèle.",
    "! Antiparasite des bobines",
    "! LC1D09BD : à vérifier.",
    "! Sortie 1 : 3 bobines en",
    "! parallèle, comparer à 3 A",
    "! DC-13 (notice XPSUAF13AP).",
    "! Manu-D : 1 seul contact,",
    "! PL c accepté (translation).",
])

# ======================================================================== 43 SECURITE - FONCTIONNEMENT
f = "43"
texte(f, 2400, 2800, "SELECTEUR -S413 (Eaton T0-4-8223/E) : 4 contacts NO par position - position 1 = Auto, position 2 = Manu", 250, 0, 1)
g.tableau(F[f], 2400, 3400, [1800, 1400, 1600, 9600], 330, [
    ["Contact", "Bornes", "Fermé en", "Rôle (folio)"],
    ["Auto-A", "13-14", "Auto", "commande -KM1 / -KM2 (f42), sans ordre automate"],
    ["Auto-B", "23-24", "Auto", "autorisation STO des 2 variateurs (f42)"],
    ["Auto-C", "33-34", "Auto", "entrée automate I0.4 « Auto » (f50)"],
    ["Auto-D", "43-44", "Auto", "réserve"],
    ["Manu-A", "53-54", "Manu", "shunt capot mécanique -B411, voie 1 (f41)"],
    ["Manu-B", "63-64", "Manu", "shunt capot magnétique -B412, voie 2 (f41)"],
    ["Manu-C", "73-74", "Manu", "entrée automate I0.5 « Manu » (f50)"],
    ["Manu-D", "83-84", "Manu", "bobine -Q423 : 48 V pas-à-pas en Manu seulement (f42)"],
], size=200)
texte(f, 2400, 7000, "COMPORTEMENT PAR ETAT", 250, 0, 1)
g.tableau(F[f], 2400, 7400, [1500, 2600, 1300, 2200, 1700, 2600, 1500, 2800], 330, [
    ["Sélecteur", "Capot", "AU", "Freins", "48 V", "-KM1 / -KM2", "STO", "Automate"],
    ["Auto", "fermé", "OK", "alimentés", "coupé", "fermés", "libéré", "I0.4 = 1"],
    ["Auto", "ouvert", "OK", "coupés", "coupé", "coupés", "actif", "relais retombé"],
    ["Manu", "ouvert ou fermé", "OK", "alimentés", "alimenté", "coupés", "actif", "I0.5 = 1"],
    ["tous", "tous", "enfoncé", "coupés", "coupé", "coupés", "actif", "relais retombé"],
], size=200)
texte(f, 2400, 9600, "TRANSITIONS", 250, 0, 1)
g.tableau(F[f], 2400, 10000, [3600, 12600], 330, [
    ["Passage", "Effet"],
    ["Auto -> Manu, capot fermé", "-KM1 / -KM2 et STO retombent, shunts ajoutés sur voies fermées, 48 V alimenté, pas de réarmement"],
    ["Auto -> Manu, en rotation", "idem, moteurs en roue libre freins desserrés (≈ 10 s à mesurer) : risque résiduel accepté"],
    ["Auto -> Manu, capot ouvert", "relais déjà retombé : réarmement -S414 après passage en Manu"],
    ["Manu -> Auto, capot fermé", "48 V coupé, STO libéré et -KM1 / -KM2 fermés ; rien ne démarre sans ordre de marche IHM"],
    ["Manu -> Auto, capot ouvert", "shunts ouverts : le relais retombe ; fermer le capot puis réarmer"],
], size=200)
notes(f, 2400, 12600, 19000, [
    "Défaut sélecteur : I0.4 = I0.5 en régime établi (0/0 ou 1/1) =",
    "défaut, filtrage de quelques centaines de ms à la commutation.",
    "Procédure normale : demande Manu sur l'IHM, arrêt en rampe,",
    "puis rotation du sélecteur.",
    "! Recouvrement Auto / Manu à mesurer à la continuité :",
    "! aucun contact Auto et Manu fermés en même temps.",
    "! Courant mini des contacts Eaton sous 24 V (entrées relais).",
], titre="POINTS A VERIFIER")
notes(f, 19800, 12600, 28800, [
    "Risques résiduels (à la liste client) :",
    "- sélecteur manœuvrable par tous (sans clé",
    "  ni cadenas, choix client) : capot shunté en Manu ;",
    "- roue libre des moteurs si sélecteur",
    "  manœuvré en rotation ;",
    "- 48 V : un seul contact Manu-D, l'ENA automate",
    "  reste seul garant en cas de défaut (PL c).",
], titre="RISQUES RESIDUELS")

# ======================================================================== 50 AUTOMATE ENTREES
f = "50"
k501e = maitre(C + "Siemens_6ES7214-1AH50-0XB0_CPU1214C_G2_alim_entrees.xsy", "K501", f, 4800, 12000, wrap=30)
W(f, [k501e["L+"], (4800, RAIL24_Y)], "24")
W(f, [k501e["M"], (5600, 11200)], "0V")
W(f, [(3600, 11200), (9200, 11200)], "0V")
W(f, [k501e["1M"], (9200, 11200)], "0V")
W(f, [(3600, 11200), (3600, RAIL0_Y)], "0V")
renvoi("11", fe11["1"], f, W(f, [k501e["FE"], (6400, 10400)], "PE"), "PE")
W(f, [k501e["L+ capt"], (7200, 3200), (23600, 3200)], "24")
W(f, [(22400, 3200), (22400, 4000)], "24")
renvoi(f, (23600, 3200), "41", VOIES["B411"][0], "24")
renvoi(f, (22400, 4000), "41", VOIES["B412"][0], "24")
fdc = "Contacts Fin de course et rupteurs\\Fin de course NO.xsy"
nom = "--- X Contact\\RC Contact NO 13-14.xsy"


def entree(inp, row, elems):
    """elems : liste de (type, repère, fichier, description, broches) du haut vers le bas."""
    p = k501e[inp]
    x = p.x
    y = 4400 if row == 1 else 7600
    yt1, yt2 = (3600, 6400) if row == 1 else (6400, 9600)
    cur = (x, 3200)
    for kind, rep, xsy, des, pins in elems:
        if kind == "borne":
            b = borne(rep, f, x, yt1 if cur[1] < y else yt2)
            W(f, [cur, b["1"]], "24")
            cur = b["2"].xy
        else:
            if kind == "maitre":
                s = g.place(xsy, rep, F[f], x, y, champs=info(rep), loc=loc(rep), compact=True, rep_size=200,
                            prefix=rep[0])
            else:
                s = esclave(xsy, rep, f, x, y, des=des, prefix=rep[:2] if rep.startswith("KM") else rep[0])
            W(f, [cur, s[pins[0]]], "24")
            cur = s[pins[1]].xy
    W(f, [cur, p], "24")


nom = CT[13]
entree("I0.0", 1, [("borne", "X711.5", None, None, None),
                   ("esclave", "S412", nom, "AU pupitre - contact NO", ("13", "14")),
                   ("borne", "X711.6", None, None, None)])
entree("I0.1", 2, [("esclave", "S411", nom, "AU armoire - contact NO", ("13", "14"))])
entree("I0.4", 1, [("borne", "X711.11", None, None, None),
                   ("esclave", "S413", CT[33], "Sélecteur - Auto", ("33", "34")),
                   ("borne", "X711.12", None, None, None)])
entree("I0.5", 2, [("borne", "X711.17", None, None, None),
                   ("esclave", "S413", CT[73], "Sélecteur - Manu", ("73", "74")),
                   ("borne", "X711.18", None, None, None)])
FDC = {"I0.6": ("B501", "Fin de course axe 1 min", 1, "X701.9", "X701.10"),
       "I0.7": ("B502", "Fin de course axe 1 max", 2, "X701.11", "X701.12"),
       "I1.0": ("B503", "Fin de course axe 2 min", 1, "X701.13", "X701.14"),
       "I1.1": ("B504", "Fin de course axe 2 max", 2, "X701.15", "X701.16")}
for inp, (rep, des, row, t1, t2) in FDC.items():
    REP[rep] = {"des": des, "fab": "À définir", "carac": "contact NF (0 = atteint ou fil coupé) - symbole NO provisoire", "loc": "+M"}
    entree(inp, row, [("borne", t1, None, None, None), ("maitre", rep, fdc, "", ("13", "14")),
                      ("borne", t2, None, None, None)])
for inp, rep, pref, row, des in (("I1.2", "KM1", "KM", 1, "Retour contacteur amont variateur 1 (aux NO)"),
                                 ("I1.3", "KM2", "KM", 2, "Retour contacteur amont variateur 2 (aux NO)"),
                                 ("I1.4", "Q423", "Q", 1, "Retour contacteur 48 V (aux NO)")):
    entree(inp, row, [("esclave", rep, nom, des, ("13", "14"))])
I50 = {inp: stub(f, (k501e[inp].x, 11200), k501e[inp], "24") for inp in ("I0.2", "I0.3")}
renvoi("41", VOIES["B411"][1], f, I50["I0.2"], "24")
renvoi("41", VOIES["B412"][1], f, I50["I0.3"], "24")
texte(f, 24800, 12400, "X1 P1 : PROFINET -> -K541 (f54)", 200)
g.tableau(F[f], 13600, 14400, [1400, 1600, 8400], 300, [
    ["Entrée", "Repère", "Fonction"], ["I0.0", "-S412", "AU pupitre actionné (NO)"], ["I0.1", "-S411", "AU armoire actionné (NO)"],
    ["I0.2", "-B411", "capot ouvert, mécanique (NO aux.)"], ["I0.3", "-B412", "capot ouvert, magnétique (NF aux.)"],
    ["I0.4", "-S413", "mode Auto"], ["I0.5", "-S413", "mode Manu"],
    ["I0.6 / I0.7", "-B501 / -B502", "fins de course axe 1 min / max (NF)"],
    ["I1.0 / I1.1", "-B503 / -B504", "fins de course axe 2 min / max (NF)"],
    ["I1.2 / I1.3", "-KM1 / -KM2", "retour contacteurs amont variateurs"],
    ["I1.4", "-Q423", "retour contacteur 48 V"], ["I1.5", "-K401", "diagnostic relais sécu (borne à confirmer)"],
], size=200)
proposition(f, ["affectation des entrées automate"], x=13600, y=13700)

# ======================================================================== 51 AUTOMATE SORTIES
f = "51"
k501s = maitre(C + "Siemens_6ES7214-1AH50-0XB0_CPU1214C_G2_sorties.xsy", "K501", f, 4800, 6400, ref=(),
               base="K501", compact=True, rep_size=300)
vs51 = (3600, 7200)
W(f, [vs51, (4800, 7200), k501s["3L+"]], "24")
W(f, [(3600, RAIL24_Y), vs51], "24")
W(f, [k501s["3M"], (5600, RAIL0_Y)], "0V")
Q51 = {q: W(f, [k501s[q], (k501s[q].x, 8000)], "24") for q in ("Q0.0", "Q0.1", "Q0.2", "Q0.4", "Q0.5", "Q0.6")}
voyant = "Signalisation et voyants\\Voyant.xsy"
col = maitre(C + "RSPRO_199-9760_colonne_lumineuse.xsy", "P511", f, 17600, 12800)
COL51 = {c: stub(f, (col[c].x, 11200), col[c], "24") for c in ("RD", "OG", "GN")}
W(f, [col["COM"], (19200, RAIL0_Y)], "0V")
REP["P513"] = {"des": "Voyant porte : défaut machine", "fab": "À définir", "carac": "24 V CC - rouge", "loc": "+A1"}
p513 = decrit(voyant, "P513", f, 7600, 12800, "Voyant porte : défaut machine", fpos=(600, 400), wrap=20, prefix="P")
V513 = stub(f, (7600, 11200), p513["X1"], "24")
W(f, [p513["X2"], (7600, RAIL0_Y)], "0V")
voy = decrit(voyant, "S414", f, 12000, 12800, "Voyant du bouton de réarmement", fpos=(600, 400), wrap=20)
V414 = stub(f, (12000, 11200), voy["X1"], "24")
W(f, [voy["X2"], (12000, RAIL0_Y)], "0V")
for q, (T, sg) in (("Q0.0", ("T322", "PUL")), ("Q0.1", ("T322", "DIR")), ("Q0.2", ("T322", "ENA")),
                   ("Q0.4", ("T323", "PUL")), ("Q0.5", ("T323", "DIR")), ("Q0.6", ("T323", "ENA"))):
    renvoi(f, Q51[q], "32", CMD32[(T, sg)], "24")

texte(f, 16000, 8400, "Q0.3, Q0.7, Q1.0, Q1.1 : réserve", 200)
g.tableau(F[f], 20800, 15600, [1800, 1600, 4800], 300, [
    ["Sortie", "Repère", "Fonction"], ["Q0.0 / 0.1 / 0.2", "-T322", "PUL / DIR / ENA axe 1 (PTO1)"],
    ["Q0.4 / 0.5 / 0.6", "-T323", "PUL / DIR / ENA axe 2 (PTO2)"],
    ["Q0.3, Q0.7, Q1.0, Q1.1", "", "réserve"],
    ["SM 1223 (f52)", "", "colonne, voyants, alarme switch"],
], size=200)
proposition(f, ["affectation des sorties automate (liste d'E/S du 06/10, à confirmer)"], x=13600, y=1300)

# ======================================================================== 52 MODULE SM 1223
f = "52"
k521e = maitre(C + "Siemens_6ES7223-5BH50-0XB0_SM1223_G2_alim_entrees.xsy", "K521", f, 4800, 4400, wrap=30)
W(f, [k521e["L+"], (4800, RAIL24_Y)], "24")
W(f, [k521e["M"], (5600, 3600)], "0V")
W(f, [(3600, 3600), (10800, 3600)], "0V")
W(f, [k521e["1M"], (6800, 3600)], "0V")
W(f, [k521e["2M"], (10800, 3600)], "0V")
W(f, [(3600, 3600), (3600, RAIL0_Y)], "0V")
# I8.4 : alarme du switch (contact ALM2), le fil part vers la droite pour ne pas croiser la ligne 0 V
I52 = W(f, [k521e["I8.4"], (11600, 3200), (15200, 3200)], "24")
k521s = maitre(C + "Siemens_6ES7223-5BH50-0XB0_SM1223_G2_sorties.xsy", "K521", f, 4800, 14400, ref=(),
               compact=True, rep_size=300)
W(f, [(4000, RAIL24_Y), (4000, 16800), (4800, 16800)], "24")
W(f, [(4800, 16800), k521s["3L+"]], "24")
W(f, [k521s["3M"], (5600, RAIL0_Y)], "0V")
for q, dest in (("Q8.0", COL51["RD"]), ("Q8.1", COL51["OG"]), ("Q8.2", COL51["GN"]), ("Q8.3", V414), ("Q8.4", V513)):
    pt = W(f, [k521s[q], (k521s[q].x, 16000)], "24")
    renvoi(f, pt, "51", dest, "24")
g.tableau(F[f], 16000, 12800, [2800, 1600, 5600], 300, [
    ["E/S", "Repère", "Fonction"], ["I8.4", "-K541", "alarme switch (ALM2)"], ["I8.0..I8.3, I8.5..I8.7", "", "réserve"],
    ["Q8.0 / 8.1 / 8.2", "-P511", "colonne rouge / orange / vert"],
    ["Q8.3", "-S414", "voyant réarmement requis"], ["Q8.4", "-P513", "voyant défaut machine"],
    ["Q8.5..Q8.7", "", "réserve"],
], size=200)
proposition(f, ["affectation des E/S du module SM 1223"], x=16000, y=12100)

# ======================================================================== 53 MODULE SM 1231 TC
f = "53"
k531 = maitre(C + "Siemens_6ES7231-5QF50-0XB0_SM1231_TC_G2.xsy", "K531", f, 4800, 12000, wrap=30)
W(f, [k531["L+"], (4800, RAIL24_Y)], "24")
W(f, [k531["M"], (5600, 11200), (3600, 11200), (3600, RAIL0_Y)], "0V")
REP["B531"]["fab"] = REP["B531"]["fab"] or "Type K"
b531 = maitre("Contacts Capteurs\\Thermocouple.xsy", "B531", f, 6800, 7200, prefix="B", fpos=(2000, 0))
W(f, [b531["1"], (6800, 6400), (6000, 6400), (6000, 10400), (6800, 10400), k531["AI0+"]], "DC")
W(f, [b531["2"], (7600, 6400), (8400, 6400), (8400, 10400), (7600, 10400), k531["AI0-"]], "DC")
g.cable(F[f], 5600, 8800, 9600, "W531", "compensation type K", "", [6000, 8400])
texte(f, 10400, 10400, "AI1 à AI7 : réserve", 200)

# ======================================================================== 54 PROFINET
f = "54"
k541 = maitre(C + "Weidmuller_2682250000_switch_IE-SW-AL05LM-5TX.xsy", "K541", f, 16000, 4400)
W(f, [k541["V1+"], (16000, RAIL24_Y)], "24")
W(f, [k541["V1-"], (16800, 3600), (26400, 3600), (26400, RAIL0_Y)], "0V")
W(f, [k541["ALM1"], (19200, RAIL24_Y)], "24")
renvoi(f, W(f, [k541["ALM2"], (20000, 3200), (21600, 3200)], "24"), "52", I52, "24")
for p, t in (("P1", "Port 1 -> -K501 automate CPU 1214C, port X1 P1 (f50)"),
             ("P2", "Port 2 -> -T201 variateur M1, port X40 (f20)"),
             ("P3", "Port 3 -> -T211 variateur M2, port X40 (f21)"),
             ("P4", "Port 4 -> -P601 IHM pupitre KTP700, port X1 (f60)"), ("P5", "Port 5 : réserve")):
    px, py = k541[p].xy
    g.ligne(F[f], 8000, py, px, py, color=32768, width=30)
    texte(f, 8000, py - 350, t, 220)
texte(f, 8000, 13600, "Liaisons PROFINET (câbles RJ45 à repérer) - V2+ / V2- : 2e alimentation non utilisée", 200)

# ======================================================================== 60 PUPITRE
f = "60"
p601 = maitre(C + "Siemens_6AV2123-2GB03-0AX0_IHM_KTP700_Basic_PN.xsy", "P601", f, 6400, 10000)
t17, t18, t19 = borne("X711.21", f, 6400, 10800), borne("X711.22", f, 7200, 10800), borne("X711.23", f, 8000, 10800)
W(f, [p601["L+"], t17["1"]], "24")
W(f, [p601["M"], t18["1"]], "0V")
W(f, [p601["FE"], t19["1"]], "PE")
W(f, [t17["2"], (6400, 12400), (3600, 12400), (3600, RAIL24_Y)], "24")
W(f, [t18["2"], (7200, RAIL0_Y)], "0V")
renvoi("11", fe11["2"], f, W(f, [t19["2"], (8000, 12000)], "PE"), "PE")
g.cable(F[f], 6000, 8400, 11600, "W711", "à définir (≈ 10 m)", "", [6400, 7200, 8000])
g.cadre(F[f], 5200, 4800, 16800, 10400, width=20, dashed=True)
texte(f, 5400, 4900, "+P1 PUPITRE", 250, 0, 1)
texte(f, 11200, 10400, "X1 : PROFINET -> -K541 (f54)", 200)
texte(f, 8800, 14000, "Contenu du pupitre +P1 :", 220, 0, 1)
texte(f, 8800, 14400, "-P601 IHM KTP700 : ce folio", 220)
texte(f, 8800, 14800, "-S412 arrêt d'urgence pupitre : contacts f41 (sécurité) et f50 (retour automate)", 220)
texte(f, 8800, 15200, "-S413 sélecteur Auto/Manu : contacts f42 (sécurité) et f50 (automate)", 220)
texte(f, 8800, 15600, "Liaisons armoire <-> pupitre : bornes -X711 (f71) et câble -W711", 220)

# ======================================================================== 80 - 90 (générés par WinRelais)
for num, lignes in (("80", ["Liste des câbles extérieurs : à générer par WinRelais (carnet de câbles)",
                            "-W101, -W201, -W202, -W203, -W211, -W212, -W213, -W531, -W711."]),
                    ("85", ["Implantation armoire +A1 : à réaliser sous WinArmoire",
                            "(les symboles portent la localisation A1 / P1 / M dans Vue armoire)."]),
                    ("90", ["Nomenclature : à générer par WinRelais (Optimisation / Générer / Nomenclature),",
                            "seuls les symboles maîtres portent une référence fabricant."])):
    for i, l in enumerate(lignes):
        texte(num, 3200, 4000 + 600 * i, l, 300)

# ======================================================================== spécification des liaisons
MEMES = [
    # chaîne d'arrêt d'urgence et capots (deux voies), pontage Manu par -S413
    ["K401:S11", "S411:1"], ["S411:2", "X711.1:1"], ["X711.1:2", "S412:1"], ["S412:2", "X711.2:1"],
    ["X711.2:2", "X701.1:1", "X711.13:1"], ["X701.1:2", "B411:11"], ["B411:12", "X701.2:1"],
    ["X701.2:2", "K401:S12", "X711.14:2"], ["X711.13:2", "S413:53"], ["S413:54", "X711.14:1"],
    ["K401:S21", "S411:21"], ["S411:22", "X711.3:1"], ["X711.3:2", "S412:21"], ["S412:22", "X711.4:1"],
    ["X711.4:2", "X701.5:1", "X711.15:1"], ["X701.5:2", "B412:11"], ["B412:12", "X701.6:1"],
    ["X701.6:2", "K401:S22", "X711.16:2"], ["X711.15:2", "S413:63"], ["S413:64", "X711.16:1"],
    ["B411:23", "X701.3:2"], ["B411:24", "X701.4:1"], ["B412:23", "X701.7:2"], ["B412:24", "X701.8:1"],
    # boucle de retour (EDM) et réarmement
    ["K401:Y1", "KM1:21"], ["KM1:22", "KM2:21"], ["Q423:22", "S414:3"], ["S414:4", "K401:Y2"],
    # sorties du relais de sécurité (architecture du 27/10)
    ["K401:14", "Q421:A1", "Q422:A1", "X711.19:1"], ["X711.19:2", "S413:83"], ["S413:84", "X711.20:1"],
    ["X711.20:2", "Q423:A1"],
    ["K401:24", "X711.7:1"], ["X711.7:2", "S413:13"], ["S413:14", "X711.8:1"], ["X711.8:2", "KM1:A1", "KM2:A1"],
    ["K401:34", "X711.9:1"], ["X711.9:2", "S413:23"], ["S413:24", "X711.10:1"],
    ["X711.10:2", "T201:X6:1", "T201:X6:3", "T211:X6:1", "T211:X6:3"],
    # sorties automate
    ["K501:Q0.0", "T322:PUL+"], ["K501:Q0.1", "T322:DIR+"], ["K501:Q0.2", "T322:ENA+"],
    ["K501:Q0.4", "T323:PUL+"], ["K501:Q0.5", "T323:DIR+"], ["K501:Q0.6", "T323:ENA+"],
    ["K521:Q8.0", "P511:RD"], ["K521:Q8.1", "P511:OG"], ["K521:Q8.2", "P511:GN"],
    ["K521:Q8.3", "S414:X1"], ["K521:Q8.4", "P513:X1"],
    # entrées automate
    ["K501:I0.0", "X711.6:2"], ["K501:I0.1", "S411:14"], ["K501:I0.2", "X701.4:2"], ["K501:I0.3", "X701.8:2"],
    ["K501:I0.4", "X711.12:2"], ["K501:I0.5", "X711.18:2"], ["K501:I0.6", "X701.10:2"], ["K501:I0.7", "X701.12:2"],
    ["K501:I1.0", "X701.14:2"], ["K501:I1.1", "X701.16:2"], ["K501:I1.2", "KM1:14"], ["K501:I1.3", "KM2:14"],
    ["K501:I1.4", "Q423:14"], ["K521:I8.4", "K541:ALM2"],
    ["K501:L+ capt", "X701.3:1", "X701.7:1", "X701.9:1", "X701.11:1", "X701.13:1", "X701.15:1", "X711.5:1",
     "X711.11:1", "X711.17:1", "S411:13", "KM1:13", "KM2:13", "Q423:13"],
    ["X311:1", "K401:A1", "K401:13", "K401:23", "K401:33", "K501:L+", "K501:3L+", "K521:L+", "K521:3L+",
     "K531:L+", "K541:V1+", "K541:ALM1", "P512:X1", "X711.21:2"],
    ["X312:1", "K401:A2", "K501:M", "K501:1M", "K501:3M", "K521:M", "K521:3M", "K531:M", "K541:V1-",
     "KM1:A2", "KM2:A2", "Q421:A2", "Q422:A2", "Q423:A2", "P511:COM", "P512:X2", "P513:X2", "S414:X2",
     "T201:X5:GND", "T211:X5:GND", "T201:X6:2", "T201:X6:4", "T211:X6:2", "T211:X6:4",
     "T322:PUL-", "T322:DIR-", "T322:ENA-", "T323:PUL-", "T323:DIR-", "T323:ENA-", "X711.22:2"],
    ["X313:1", "T201:X5:24V", "T211:X5:24V"],
    ["K501:FE", "X112:E", "P601:FE", "F101:PE", "T301:PE", "M201:PE", "X131:PE", "T321:PE"],
    ["B531:1", "K531:AI0+"], ["B531:2", "K531:AI0-"],
    # moteurs SEW : frein (W202 / W212) et sonde TF (W203 / W213) en direct, sans bornier
    ["M201:1b", "T201:X10:1"], ["M201:2b", "T201:X10:2"], ["M211:1b", "T211:X10:1"], ["M211:2b", "T211:X10:2"],
    ["Q421:4/T2", "M201:2"], ["Q421:6/T3", "M201:3"], ["Q422:4/T2", "M211:2"], ["Q422:6/T3", "M211:3"],
    ["Q102:2", "F101:L1", "X111:30"], ["Q102:4", "F101:L2", "X111:20"], ["Q102:6", "F101:L3", "X111:10"],
    ["KM1:2/T1", "T201:X1:L1"], ["KM2:6/T3", "T211:X1:L3"],
    ["Q423:6/T3", "T322:+V", "T323:+V"], ["Q423:4/T2", "T322:-V", "T323:-V"],
]
DIFFERENTS = ["X112:E", "X311:1", "X312:1", "X313:1", "X711.8:2", "X711.10:2", "X711.20:2", "K401:14", "K401:24", "K401:34", "Q423:6/T3", "Q423:4/T2",
              "X111:10", "X111:20", "X111:30", "X111:N0", "K401:S11", "K401:S12", "K401:S21", "K401:S22",
              "K401:Y1", "K401:Y2", "K501:I0.2", "K501:I0.3", "K501:I0.0", "K501:I0.1"]


def nets_par_broche(path, bornes_passantes=True):
    import xrs_tool
    from collections import defaultdict
    m = xrs_tool.parse(path)
    if not bornes_passantes:
        for s_ in m["symboles"]:
            s_["borne"] = False
    uf, _ = xrs_tool.build_nets(m)
    net = defaultdict(set)
    membres = defaultdict(list)
    num = {fo["index"]: fo["numero"] for fo in m["folios"]}
    for s_ in m["symboles"]:
        for b in s_["broches"]:
            r = uf.find(("B", s_["index"], b["nom"], b["x"], b["y"]))
            net[f"{s_['nom']}:{b['nom']}"].add(r)
            membres[r].append((s_["nom"], b["nom"], num[s_["folio"]]))
    return net, membres


def controle_specification(path):
    net, _ = nets_par_broche(path)
    out = []
    for grp in MEMES:
        for p in grp:
            if p not in net:
                out.append(f"spécification : broche {p} absente du schéma")
        ids = [net[p] for p in grp if p in net]
        if ids and not set.intersection(*ids):
            out.append("spécification : pas sur la même équipotentielle : " + ", ".join(grp))
    seen = {}
    for p in DIFFERENTS:
        for r in net.get(p, ()):
            if r in seen:
                out.append(f"spécification : court-circuit entre {seen[r]} et {p}")
            seen[r] = p
    return out


# ======================================================================== plans de bornier (f70, f71)
TERRAIN = ("B4", "B5", "M2", "S412", "S413", "P601")    # appareils hors armoire (+M, +P1)


# potentiels communs à plusieurs appareils : nommés dans les tableaux de bornier
POTENTIELS = [("-K501:L+ capt", "+24 V capteurs (-K501 L+ capt, f50)"),
              ("-K401:13", "+24 V commande (-X311, f31)"),
              ("-K401:A2", "0 V commande (-X312, f31)"),
              ("-F101:PE", "Terre PE / FE (-X112, f11)"),
              ("-T201:X6:1", "STO voie 1 des variateurs -T201 (f20) / -T211 (f21)"),
              ("-T201:X6:3", "STO voie 2 des variateurs -T201 (f20) / -T211 (f21)"),
              ("-K501:3L+", "+24 V sorties automate -K501 / -K521 (3L+, f51-f52)")]


def designations():
    """Repère -> désignation (champ 2 du symbole maître, sinon du premier symbole)."""
    des = {}
    for p in g.symbols:
        d = p.block[4].split("·")[0]
        if d:
            des.setdefault(p.rep, d)
    for rep, r in REP.items():
        if r.get("des"):
            des[rep] = r["des"]
    return des


def plan_bornier(path, bornier):
    """Pour chaque borne : appareils raccordés côté armoire / côté terrain (broches 1 / 2)."""
    import re
    net, membres = nets_par_broche(path, bornes_passantes=False)
    lignes = []
    noms = sorted({p.split(":")[0] for p in net if p.startswith(bornier + ".")},
                  key=lambda n: int(re.findall(r"\d+", n.split(".")[1])[0]))
    for nom in noms:
        cotes, terrain = [], []
        for pin in ("1", "2"):
            autres, ponts, ext = [], [], []
            for r in net.get(f"{nom}:{pin}", ()):
                for rep, b, fo in membres[r]:
                    if rep == nom:
                        continue
                    if rep.startswith(("X7", "X31")):
                        ponts.append(f"-{rep.replace('.', ':')} (f{fo})")
                    else:
                        autres.append(f"-{rep}:{b} (f{fo})")
                        ext.append(rep.startswith(TERRAIN))
            # une borne reliée seulement à une autre borne : on nomme cette borne
            autres = sorted(set(autres)) or sorted(set(ponts))
            nom_pot = [t for k, t in POTENTIELS if any(a.startswith(k + " ") for a in autres)]
            if len(autres) > 1 and nom_pot:
                autres = nom_pot[:1]
            if len(autres) == 1:            # un seul appareil : on dit ce que c'est
                rep = autres[0][1:].split(":")[0]
                if DES.get(rep):
                    autres = [f"{autres[0]} {DES[rep]}"]
            cotes.append(", ".join(autres[:3]) + (" ..." if len(autres) > 3 else "") or "-")
            terrain.append(bool(ext) and all(ext))
        # le côté terrain est celui où tous les appareils sont hors armoire
        if terrain[0] and not terrain[1]:
            cotes.reverse()
        lignes.append([nom.split(".", 1)[1], cotes[0], cotes[1]])
    return lignes


def ecrire_borniers(path):
    global DES
    DES = designations()
    for num, bornier, titre in (("70", "X701", "BORNIER -X701 : ARMOIRE +A1 <-> MACHINE +M"),
                                ("71", "X711", "BORNIER -X711 : ARMOIRE +A1 <-> PUPITRE +P1")):
        lignes = plan_bornier(path, bornier)
        texte(num, 2400, 1600, titre, 300, 0, 1)
        g.tableau(F[num], 2400, 2400, [1400, 11000, 11000], 380,
                  [["Borne", "Côté armoire (intérieur)", "Côté terrain (extérieur)"]] + lignes, size=200)
        y = 2400 + 380 * (len(lignes) + 1) + 600
        for l in ("Méthode : 1 borne par conducteur qui sort de l'armoire, bornes regroupées par appareil / câble,",
                  "côté armoire en haut de la borne sur le schéma, côté terrain en bas.",
                  f"Bornier graphique : Optimisation / Générer / Bornier, onglet Automatique, extraire {bornier},",
                  "folio visible, option Matériel connecté via un bornier + Pré-remplissage + filtre B,M,S412,S413,P601."):
            texte(num, 2400, y, l, 220)
            y += 400


# ======================================================================== écriture + contrôle
for num in F:                       # contenu centré dans le cadre (pas la garde, la légende, les notes)
    if "10" <= num <= "69":
        g.centrer(F[num])
g.write(SORTIE)
ecrire_borniers(SORTIE)
for num in ("70", "71"):
    g.centrer(F[num])
g.write(SORTIE)
pb = check(g, SORTIE) + controle_specification(SORTIE)
print(f"{len(g.folios)} folios, {len(g.symbols)} symboles, {len(g.wires)} fils, {len(g.renvois)} renvois")
print(f"{len(pb)} problème(s) de contrôle")
for p in pb:
    print(" -", p)
