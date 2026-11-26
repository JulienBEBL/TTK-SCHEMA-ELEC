"""Schéma électrique TTK reconstruit à partir de TTK_Plan_Folios_Reperes.xlsx.

Usage : python ttk_schema.py [sortie.xrs] [tableau.xlsx]
Écrit le schéma puis affiche le contrôle (équipotentielles, chevauchements, xrs_tool.verifier).

Conventions : coordonnées en 1/100 mm, grille 400 ; repères sans « - » ; maîtres = référence
fabricant (onglet Repères), esclaves = même repère sans référence (règles R1-R3).
Tout ce que le tableau ne décide pas est marqué « PROPOSITION A VALIDER » sur le folio.
"""
import os
import re
import sys

import lire_tableau
from xrs_gen import Gen, check
import nomenclature

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ICI, "..", "schema", "generes", "TTK_genere.xrs")
TABLEAU = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ICI, "..", "livrables", "TTK_Plan_Folios_Reperes.xlsx")
MODELE = os.path.join(ICI, "..", "schema", "modele", "SCHEMA_ELEC_TTK.xrs")

REP = lire_tableau.reperes(TABLEAU)
FOL = lire_tableau.folios(TABLEAU)
# décisions postérieures au classeur (27/10/2026) : le classeur de Julien n'est pas modifié, voir livrables/MAJ_Reperes_2026-10-27.csv
REP["B412"].update({"fab": "ifm MN508S (RS 016-3138)", "carac": "codé - 2 NO + 1 NF - M12 - 24 V 50 mA"})
REP["S413"].update({"fab": "Eaton T0-4-8223/E", "carac": "8 contacts NO 1-2 à 15-16 (ponts d'usine retirés)"})
# 18/11 (nomenclature) : références connues mais restées « À définir » dans le classeur (memoire/02_MATERIEL.md)
REP["B411"]["fab"] = "RS PRO 902-6874"
REP["P511"]["fab"] = "RS PRO 199-9760"
for k_ in ("S411", "S412"):
    REP[k_]["fab"] = "Schneider XB5AS8442 + ZBE102 + ZBE101"
REP["S412"]["carac"] = "2 NF + 1 NO"          # comme S1 (Julien 03/11)
REP["Q135"].update({"des": "Disjoncteur limitation prise de service à 2 A (choix BEBL)", "fab": "Schneider A9P71602 (iDT40K)", "carac": "2 A C - 4,5 kA"})   # v35, Julien 20/11
REP["X131"]["carac"] = "2P+T 16 A 250 V - limitée à 2 A par -QF10"   # v36 : QF10 en 2 A (était « limitée 1,5 kW »)
REP["P511"]["loc"] = "+M"                    # colonne lumineuse de la machine (02_MATERIEL)
# f13 séparé en deux (29/10) : f13 alimentations, f14 services armoire ; f43 supprimé (29/10)
FOL.insert(next(i for i, f in enumerate(FOL) if f["num"] == "13") + 1,
           {"num": "14", "titre": "DISTRIBUTION 230 V - SERVICES", "desc": "VENTILATION, ECLAIRAGE, PRISE DE SERVICE",
            "loc": "+A1", "maitres": ""})
# 18/11 : nomenclature générée sur trois folios (90 à 92, police 300 en v33)
# v37 (revue Krizox, D08) : f41 coupé en deux avec la boîte +BJM : f43 = capots (internes et affichés : 43)
FOL.insert(next(i for i, f in enumerate(FOL) if f["num"] == "42") + 1,
           {"num": "43", "titre": "SECURITE - CAPOTS", "desc": "CAPOTS -B1 / -B2, SHUNTS MANU -S3, INFOS CAPOTS VERS L'AUTOMATE",
            "loc": "+A1", "maitres": ""})
FOL.insert(next(i for i, f in enumerate(FOL) if f["num"] == "50"),
           {"num": "55", "titre": "AUTOMATE - ALIMENTATION & PROFINET", "desc": "CPU -K1 : ALIMENTATION 24 V, SORTIE 24 V CAPTEURS, PROFINET",
            "loc": "+A1", "maitres": ""})
# v37 (revue Krizox, D24) : plans de bornier sur 3 folios (71 à 73), à la place de l'ancien tableau du f71
for n_, k_ in (("72", 2), ("73", 3), ("74", 4)):         # v39 : 4e folio (borniers plus écartés)
    FOL.insert(next(i for i, f in enumerate(FOL) if f["num"] == str(int(n_) - 1)) + 1,
               {"num": n_, "titre": f"PLANS DE BORNIER ({k_}/4)",
                "desc": "BORNIERS DE L'ARMOIRE +A1 ET DE LA BOITE +BJM : " + ("FIN" if k_ == 4 else f"SUITE ({k_}/4)"),
                "loc": "+A1", "maitres": None})
FOL.insert(next(i for i, f in enumerate(FOL) if f["num"] == "90") + 1,
           {"num": "91", "titre": "NOMENCLATURE (2/3)", "desc": "LISTE DU MATERIEL : SUITE", "loc": "—", "maitres": None})
FOL.insert(next(i for i, f in enumerate(FOL) if f["num"] == "91") + 1,
           {"num": "92", "titre": "NOMENCLATURE (3/3)", "desc": "LISTE DU MATERIEL : FIN", "loc": "—", "maitres": None})
DESC_FOL = {"02": "LISTE DES FOLIOS",
            "03": "COULEURS DES CONDUCTEURS",
            "10": "RACCORDEMENT RESEAU, SECTIONNEMENT, PROTECTION GENERALE",
            "13": "ALIMENTATIONS 24 V (-T1, -T2), DEPART 48 V, VOYANT PRESENCE TENSION, LIAISON PELV",
            # AU et sélecteur dessinés là où travaillent leurs contacts (règle R4) : f60 = IHM seule
            "60": "IHM KTP700 : ALIMENTATION ET LIAISONS DU PUPITRE"}
# revue complète du 16/11 (Julien) : chaque titre / description dit ce que contient le folio (n° internes)
DESC_FOL.update({
    "12": "DEPARTS VARIATEURS (-QM1 / -KM1, -QM2 / -KM2) ET FREINS (-QF2 / -KF1, -QF3 / -KF2)",
    "13": "ALIMENTATIONS 24 V (-T1, -T2) ET 48 V (-T3), VOYANT -H2, LIAISON PELV",
    "14": "ECLAIRAGE, VENTILATION (BORNES -X13), PRISE DE SERVICE",
    "32": "COUPURE DU 48 V (-KA2), DRIVERS -U3 / -U4, MOTEURS -M3 / -M4",
    "31": "BLOCS -X21.11 24VELEC, -X21.12 0 V, -X21.13 24VSEC, -X21.14 24 V CAPTEURS ; VOYANT -H3",
    "04": "PAR LIEU : RESEAU CLIENT, ARMOIRE +A1, BOITE +BJM, MACHINE +M, PUPITRE +P1 ET CABLES",   # v37 (D18)
    "54": "TOPOLOGIE : CPU, VARIATEURS, IHM, SWITCH ; ADRESSES IP (A DEFINIR)",                      # v37 (D15)
    "20": "VARIATEUR -U1, RESISTANCE -R1, MOTEUR -M1 (FREIN, SONDE TF)",
    "21": "VARIATEUR -U2, RESISTANCE -R2, MOTEUR -M2 (FREIN, SONDE TF)",
    "40": "RELAIS -KA1 : ALIMENTATION, BOUCLE DE RETOUR, REARMEMENT -S4, REGLAGES",
    "41": "ARRETS D'URGENCE -S1 / -S2 (VOIES 1 ET 2), PAR LA BOITE +BJM POUR -S2",
    "42": "STO VARIATEURS, CONTACTEURS -KM1 / -KM2, FREINS -KF1 / -KF2, 48 V -KA2",
    "50": "ENTREES CPU : AU, CAPOTS, SELECTEUR, FINS DE COURSE, RETOURS",
    "51": "SORTIES RAPIDES CPU : DRIVERS PAS A PAS (PUL / DIR / ENA)",
    "52": "SIGNALISATION : COLONNE LUMINEUSE -H1, VOYANT DEFAUT -H4",
    "70": "BORNES RAIL PAR RAIL : MACHINE, PUPITRE, PORTE, INTERNES",
    "71": "BORNIERS DE L'ARMOIRE +A1 ET DE LA BOITE +BJM, BORNE PAR BORNE",
})
TITRES_FOL = {"50": "AUTOMATE - ENTREES TOR", "71": "PLANS DE BORNIER (1/4)", "90": "NOMENCLATURE (1/3)", "13": "DISTRIBUTION 230 V - ALIMENTATIONS", "32": "48 VDC ET MOTEURS PAS A PAS",
              "51": "AUTOMATE - SORTIES TOR", "52": "MODULE SM 1223 - SIGNALISATION", "70": "BORNIERS DE L'ARMOIRE"}
for f in FOL:
    f["titre"] = TITRES_FOL.get(f["num"], f["titre"])
    f["desc"] = DESC_FOL.get(f["num"], f["desc"])
# Ordre des folios (Julien, 29/10 et 30/10) : alimentations (400, 230, 48, 24), switch, variateurs, sécurité (f40-f42,
# remis à leur place le 30/10), IHM, automate, borniers. f11 (répartiteur, barrette de terre) et f30 (fondu dans f13) supprimés.
# f03 (légende et conventions) supprimé le 02/11 : Julien n'en a pas besoin.
# Le script garde les anciens numéros en interne ; NUMFOL donne le numéro affiché. Dans les textes du script,
# « fNN » est toujours un ANCIEN numéro (traduit à l'écriture par ren()).
# 02/11 : une dizaine par famille (plan validé par Julien) : 10-13 puissance, 20-21 très basse tension,
# 30-32 réseau et variateurs, 40-42 sécurité, 50 pupitre, 60-63 automate, 70-71 borniers, 80-90 listes
NUMFOL = {"04": "03", "12": "11", "13": "12", "14": "13", "32": "20", "31": "21", "54": "30", "20": "31", "21": "32",
          "60": "50", "55": "60", "50": "61", "51": "62", "52": "63", "53": "64", "71": "70", "72": "71", "73": "72", "74": "73"}
# v39 (Julien 24/11) : ancien f70 (borniers rail par rail) supprimé ; plans de bornier affichés f70 à f72 (internes 71 à 73)
# v38 (Julien 24/11, choix a) : ancien f60 coupé en deux : f60 = alimentation et PROFINET de la CPU (interne 55),
# f61 = entrées (interne 50) ; anciens f61 à f63 -> f62 à f64 (bornes X60 -> X61, X62 -> X63, X63 -> X64)
FOL = sorted((f for f in FOL if f["num"] not in ("03", "11", "30", "70")), key=lambda f: NUMFOL.get(f["num"], f["num"]))
g = Gen(MODELE)

# ---------------------------------------------------------------- nommage des appareils (décision de Julien du 28/10)
# Le script garde en interne les repères du classeur (Q121, T201...) ; ren() les traduit au moment de l'écriture
# (repère, champs, textes, câbles, folios). Logique : lettres de fonction + n° d'ordre dans la fonction,
# dans le sens de l'énergie ; -KM1 / -KM2 moteurs, -KF1 / -KF2 freins (choix de Julien) ; borniers par groupe
# de fonction (X1x puissance, X3x très basse tension, X70 machine, X71 pupitre).
RENOMME = {
    "X101": "X11", "W101": "W1", "Q101": "QS1", "Q102": "QF1", "T101": "TR1", "X111": "X12", "X112": "X13",
    "Q121": "QM1", "Q122": "QM2", "Q123": "QF2", "Q124": "QF3", "Q421": "KF1", "Q422": "KF2", "Q423": "KA2",
    "Q132": "QF4", "Q133": "QF5", "Q134": "QF6", "Q136": "QF7", "Q137": "QF8", "Q131": "QF9", "Q135": "QF10",
    "X131": "X14", "G131": "EV1", "G132": "EV2", "E131": "EL1", "E132": "EL2",
    "T201": "U1", "R201": "R1", "M201": "M1", "W201": "W2", "W203": "W3", "W202": "W4",
    "T211": "U2", "R211": "R2", "M211": "M2", "W211": "W5", "W213": "W6", "W212": "W7",
    "T301": "T1", "T302": "T2", "T321": "T3", "X311": "X31", "X312": "X32", "X313": "X33",
    "T322": "U3", "T323": "U4", "M321": "M3", "M322": "M4",
    "F401": "FA1", "K401": "KA1", "S411": "S1", "S412": "S2", "S413": "S3", "S414": "S4", "B411": "B1", "B412": "B2",
    "K501": "K1", "B501": "B3", "B502": "B4", "B503": "B5", "B504": "B6", "P511": "H1", "P512": "H3", "P513": "H4",
    "K521": "K2", "K531": "K3", "B531": "B7", "W531": "W8", "W321": "W9", "W322": "W10", "K541": "K4", "P601": "P1",
    "X701": "X70", "X711": "X71",
}
# Bornes (02/11) : X + n° du folio où elles sont dessinées + « . » + n° de borne, une dizaine par fonction
# (X31.11 à X31.14 moteur M1, X31.21 / X31.22 sonde TF...). WinRelais n'accepte qu'un seul point.
# (bornier, dizaine, folio interne, fonction, destination, [(borne interne, signal)])
GROUPES = [
    ("X10", 1, "10", "Arrivée réseau", "réseau", [("X101.VJ", "PE"), ("X101.1", "N"), ("X101.2", "L1"), ("X101.3", "L2"), ("X101.4", "L3")]),
    ("X12", 1, "13", "Liaison PELV 0 V - PE", "A1", [("X36.1", "0V-PE")]),
    ("X20", 1, "32", "Moteur pas-à-pas M3", "+M", [(f"X701.{33 + i}", p) for i, p in enumerate(("A+", "A-", "B+", "B-"))] + [("X701.47", "PE")]),
    ("X20", 2, "32", "Moteur pas-à-pas M4", "+M", [(f"X701.{37 + i}", p) for i, p in enumerate(("A+", "A-", "B+", "B-"))] + [("X701.48", "PE")]),
    ("X31", 1, "20", "Moteur M1", "+M", [(f"X701.{17 + i}", p) for i, p in enumerate(("PE", "U", "V", "W"))]),
    ("X31", 2, "20", "Sonde TF M1", "+M", [("X701.21", "1b"), ("X701.22", "2b")]),
    ("X31", 3, "20", "Frein M1", "+M", [("X701.23", "2"), ("X701.24", "3")]),
    ("X32", 1, "21", "Moteur M2", "+M", [(f"X701.{25 + i}", p) for i, p in enumerate(("PE", "U", "V", "W"))]),
    ("X32", 2, "21", "Sonde TF M2", "+M", [("X701.29", "1b"), ("X701.30", "2b")]),
    ("X32", 3, "21", "Frein M2", "+M", [("X701.31", "2"), ("X701.32", "3")]),
    ("X41", 1, "41", "AU pupitre -S2, voies 1 et 2", "+P1", [(f"X711.{n}", "") for n in (1, 2, 3, 4)]),
    # v37 : shunts et capots dessinés au f43 -> bornes X43 (anciennes X41.21-24, X41.31-34, X41.41-44)
    ("X43", 1, "43", "Sélecteur -S3 Manu : shunt des capots", "+P1", [(f"X711.{n}", "") for n in (13, 14, 15, 16)]),
    ("X43", 2, "43", "Capot -B1", "+M", [("X701.1", "11"), ("X701.2", "12"), ("X701.3", "23"), ("X701.4", "24")]),
    ("X43", 3, "43", "Capot -B2", "+M", [("X701.5", "11"), ("X701.6", "12"), ("X701.7", "23"), ("X701.8", "24")]),
    # AU armoire -S1 sur la porte (Julien 02/11) : par des bornes en bas de l'armoire, pas de fil direct
    ("X41", 5, "41", "AU armoire -S1 (porte), voies 1 et 2", "porte", [(f"X721.{n}", "") for n in (1, 2, 3, 4)]),
    ("X42", 1, "42", "Sélecteur -S3 : MANU-D, AUTO-A, AUTO-B", "+P1", [(f"X711.{n}", "") for n in (19, 20, 7, 8, 9, 10)]),
    ("X50", 1, "60", "Alimentation IHM -P1", "+P1", [("X711.21", "L+"), ("X711.22", "M"), ("X711.23", "FE")]),
    # v38 : entrées au f61 (bornes X61, ex X60), SM 1223 au f63 (X63, ex X62), SM 1231 au f64 (X64, ex X63)
    ("X61", 1, "50", "AU pupitre -S2 (contact NO)", "+P1", [("X711.5", ""), ("X711.6", "")]),
    ("X61", 2, "50", "Sélecteur -S3 Auto / Manu", "+P1", [(f"X711.{n}", "") for n in (11, 12, 17, 18)]),
    ("X61", 3, "50", "Fins de course -B3 à -B6", "+M", [(f"X701.{9 + i}", f"B{3 + i // 2}") for i in range(8)]),
    ("X61", 4, "50", "AU armoire -S1 (porte), contact NO", "porte", [("X721.5", ""), ("X721.6", "")]),
    ("X64", 1, "53", "Thermocouple -B7", "+M", [("X701.41", "+"), ("X701.42", "-")]),
    # 05/11 (Julien) : colonne -H1 par des bornes (câble) ; appareils de porte tous par des bornes, comme -S1
    ("X63", 1, "52", "Colonne -H1", "+M", [("X701.43", "RD"), ("X701.44", "OG"), ("X701.45", "GN"), ("X701.46", "COM")]),
    ("X40", 1, "40", "Réarmement -S4 (porte)", "porte", [("X721.7", ""), ("X721.8", "")]),
    ("X12", 2, "13", "Voyant -H2 230 V (porte)", "porte", [("X721.9", ""), ("X721.10", "")]),
    ("X21", 2, "31", "Voyant -H3 (porte)", "porte", [("X721.11", ""), ("X721.12", "")]),
    ("X63", 2, "52", "Voyant -H4 (porte)", "porte", [("X721.13", ""), ("X721.14", "")]),
    # 13/11 (Julien) : éclairage et ventilateurs par des bornes, rail R4 à la place laissée par XR2
    ("X13", 1, "14", "Eclairage armoire -EL1 / -EL2", "A1", [("X141.1", "L"), ("X141.2", "N")]),
    ("X13", 2, "14", "Ventilation -EV1 / -EV2", "A1", [("X142.1", "L"), ("X142.2", "N")]),
]
DES_BORNE = {}
for b_, d_, _, fn_, _, bs_ in GROUPES:
    for i_, (int_, _) in enumerate(bs_):
        RENOMME[int_] = f"{b_}.{d_}{i_ + 1}"
        DES_BORNE[int_] = fn_
RENOMME.update({"X311": "X21.11", "X312": "X21.12", "X313": "X21.13", "X314": "X21.14", "X131": "XD1"})
for k_ in ("X111", "X112"):          # répartiteur et barrette de terre non dessinés (29/10)
    RENOMME.pop(k_)
_RE = re.compile(r"(?<![A-Za-z0-9])(" + "|".join(sorted(map(re.escape, RENOMME), key=len, reverse=True))
                 + r")(?![0-9A-Za-z])")


_RE_F = re.compile(r"(?<![A-Za-z0-9])f(\d\d)(?!\d)")


def ren_rep(s):
    return _RE.sub(lambda m: RENOMME[m.group(1)], s) if isinstance(s, str) else s


def ren(s):
    """Nouveaux repères et nouveaux numéros de folio (« f13 » -> « f22 »)."""
    if not isinstance(s, str):
        return s
    return _RE_F.sub(lambda m: "f" + NUMFOL.get(m.group(1), m.group(1)), ren_rep(s))


_place, _texte, _cable, _folio = g.place, g.texte, g.cable, g.folio


def _place_ren(xsy, rep, folio, x, y, champs=None, **kw):
    """Pose avec l'ancien repère (clés internes du script), écrit le nouveau dans le champ 1.
    Marque et référence (champ 3) masquées sauf sur les borniers (demande du 29/10) : la donnée reste
    dans le symbole pour la nomenclature."""
    new = ren(rep)
    kw["prefix"] = re.match(r"[A-Z]+", new).group(0)
    if "shown" not in kw and "PTFIX" not in xsy and "Borne" not in xsy:
        kw["shown"] = (2, 4)
    p = _place(xsy, rep, folio, x, y, champs={k: ren(v) for k, v in (champs or {}).items()}, **kw)
    f1 = p.block[3].split("·")
    f1[0] = new
    p.block[3] = "·".join(f1)
    return p


POLES = [("1", "2"), ("3", "4"), ("5", "6"), ("1/L1", "2/T1"), ("3/L2", "4/T2"), ("5/L3", "6/T3")]


# Numérotation des fils, convention v2 sans point (04_REGLES_DESSIN, Julien 05/11), appliquée folio par folio
# (13/11 : f10, puis f11 à f13). Numéro FFNN : FF = folio affiché de naissance du potentiel, NN = dizaine de l'appareil
# dont il sort (ordre de lecture : gauche -> droite, haut -> bas) + conducteur (1 L1, 2 L2, 3 L3, 4 N ; continu : 1 = +,
# 0 = 0 V). Un potentiel garde son numéro à travers les bornes et les blocs de distribution, et d'un folio à l'autre.
# Le PE garde « PE » (repéré par sa couleur). Les folios non encore numérotés gardent L1 / L2 / L3 / N.
UNITE = {"L1": 1, "L2": 2, "L3": 3, "N": 4}
NUMEROTES = {"10", "12", "13", "14", "32", "31", "54", "20", "21", "40", "41", "42", "43", "60", "55", "50", "51", "52", "53"}
# folios internes : tous les folios dessinés (affichés 10 à 13, 20, 21, 30 le 13/11 ; 31, 32, 40 à 42, 50, 60 à 63 le 16/11)
# (folio interne, repère interne, broches de sortie [(broche, rang, unité imposée ou None = phase)], dizaine)
_S = lambda *pins: [(p_, 0, None) if isinstance(p_, str) else p_ for p_ in pins]
SOURCES_NUM = [
    # f10 : arrivée (câble client, bornes X10, entrée QS1) ; QS1 -> QF1 ; QF1 -> XR1 / XR2 -> bus f11 ; variante USA
    ("10", "X101.1", _S("1"), 0), ("10", "X101.2", _S("1"), 0), ("10", "X101.3", _S("1"), 0), ("10", "X101.4", _S("1"), 0),
    ("10", "Q101", _S("2/T1", "4/T2", "6/T3", ("N", 1, None)), 10),
    ("10", "Q102", _S("2", "4", "6", ("N", 1, None)), 20),
    ("10", "T101", _S("H1", "H2", "H3"), 30), ("10", "T101", _S("X0", "X1", "X2", "X3"), 40),
    # f11 : 1re ligne QM1, QM2, QF2, QF3 ; 2e ligne KM1, KM2, KF1, KF2
    ("12", "Q121", _S("2/T1", "4/T2", "6/T3"), 0), ("12", "Q122", _S("2/T1", "4/T2", "6/T3"), 10),
    ("12", "Q123", _S("2", "4"), 20), ("12", "Q124", _S("2", "4"), 30),
    ("12", "KM1", _S("2/T1", "4/T2", "6/T3"), 40), ("12", "KM2", _S("2/T1", "4/T2", "6/T3"), 50),
    ("12", "Q421", _S("4/T2", "6/T3"), 60), ("12", "Q422", _S("4/T2", "6/T3"), 70),
    # f12 : 1re ligne QF4, QF5, QF6 ; 2e ligne T1 (24VSEC + 0 V commun), T2 (24VELEC ; son 0 V = celui de T1), T3 (48 V)
    ("13", "Q132", _S("2", ("N", 1, None)), 0), ("13", "Q133", _S("2", ("N", 1, None)), 10),
    ("13", "Q134", _S("2", "4"), 20),
    ("13", "T301", [("+V", 0, 1), ("-V", 0, 0)], 30), ("13", "T302", [("+V", 0, 1)], 40),
    ("13", "T321", [("+V", 0, 1), ("+V", 1, 1), ("-V", 0, 0), ("-V", 1, 0)], 50),
    # f13 : QF8, QF7, QF9 (en haut), QF10 (sous QF9)
    ("14", "Q137", _S("2", ("N", 1, None)), 0), ("14", "Q136", _S("2", ("N", 1, None)), 10),
    ("14", "Q131", _S("2", ("N", 1, None)), 20), ("14", "Q135", _S("2", ("N", 1, None)), 30),
    # f20 (13/11) : KA2 pôle 1-2 -> U3 +48 V 2001, pôle 3-4 -> U4 2011 ; U3 -> M3 2021-2024, U4 -> M4 2031-2034
    # (A+ 1, A- 2, B+ 3, B- 4) ; 0 V 48 = 1250, +48 V avant KA2 = 1251
    ("32", "Q423", [("2/T1", 0, 1)], 0), ("32", "Q423", [("4/T2", 0, 1)], 10),
    ("32", "T322", [("A+", 0, 1), ("A-", 0, 2), ("B+", 0, 3), ("B-", 0, 4)], 20),
    ("32", "T323", [("A+", 0, 1), ("A-", 0, 2), ("B+", 0, 3), ("B-", 0, 4)], 30),
    # sorties CPU (f61) vers les drivers, numérotées dès maintenant pour le f20 (commande : un numéro par fil)
    ("55", "K501", [("L+ capt", 0, 1)], 0),          # v38 : sur le f60 (alimentation)            # 24 V capteurs (L+ capt CPU -> -X21.14) : 6001
    ("51", "K501", [("Q0.0", 0, 1), ("Q0.1", 0, 2), ("Q0.2", 0, 3), ("Q0.3", 0, 4), ("Q0.4", 0, 5), ("Q0.5", 0, 6)], 0),
    # 16/11 : f31 / f32 (variateurs) : U1 / U2 -> moteur U V W (01-03), résistance de freinage +R / -R (11 / 12),
    # chaîne STO X6:3 -> U2 X6:1 (21) et X6:4 -> U2 X6:2 (20, 0 V), sonde TF X10:3 / X10:4 (31 / 32 ; doc SEW 26/11)
    ("20", "T201", [("X2:U", 0, 1), ("X2:V", 0, 2), ("X2:W", 0, 3)], 0), ("20", "T201", [("X2:+R", 0, 1), ("X2:-R", 0, 2)], 10),
    ("20", "T201", [("X6:3", 0, 1), ("X6:4", 0, 0)], 20), ("20", "T201", [("X10:3", 0, 1), ("X10:4", 0, 2)], 30),
    ("21", "T211", [("X2:U", 0, 1), ("X2:V", 0, 2), ("X2:W", 0, 3)], 0), ("21", "T211", [("X2:+R", 0, 1), ("X2:-R", 0, 2)], 10),
    ("21", "T211", [("X10:3", 0, 1), ("X10:4", 0, 2)], 30),
    # f40 : KA1 (sorties de gauche à droite, rangée du haut puis du bas ; Z1 = entrée I1.5, voir f60), FA1, puis la boucle de retour Y1 -> Y2
    ("40", "K401", [("S11", 0, 1), ("S21", 0, 2), ("Y1", 0, 3), ("14", 0, 4), ("24", 0, 5), ("34", 0, 6)], 0),
    ("40", "F401", [("1", 0, 1)], 10), ("40", "KM1", [("22", 0, 1)], 20), ("40", "KM2", [("22", 0, 1)], 30),
    ("40", "Q421", [("22", 0, 1)], 40), ("40", "Q422", [("22", 0, 1)], 50), ("40", "Q423", [("22", 0, 1)], 60),
    ("40", "S414", [("4", 0, 1)], 70),
    # f41 : AU / capot, voie 1 puis voie 2 : S3 (retour vers S12 / S22), S1, S2
    ("43", "S413", [("4", 0, 1), ("8", 0, 2)], 0), ("41", "S411", [("2", 0, 1), ("22", 0, 2)], 10),   # v37 : shunts au f43
    ("41", "S412", [("2", 0, 1), ("22", 0, 2)], 20),
    # f42 : S3 vers les bobines (16 -> KA2, 2 -> KM1 / KM2) et vers le STO (6 -> U1 X6:1)
    ("42", "S413", [("16", 0, 1), ("2", 0, 2), ("6", 0, 3)], 0),
    # f60 : fils d'entrée de la CPU = n° de l'entrée (comme les sorties) : I0.n -> 601(n+1), I1.n -> 602(n+1),
    # y compris I0.2 / I0.3 (B1 / B2, f41) et I1.5 (Z1 de KA1, f40) : 11 appareils sources, trop pour une dizaine chacun
    ("50", "K501", [(f"I0.{n}", 0, n + 1) for n in range(8)], 10), ("50", "K501", [(f"I1.{n}", 0, n + 1) for n in range(6)], 20),
    # f62 : SM 1223 Q8.n -> 620(n+1) ; f63 : thermocouple B7 + / - -> 6301 / 6302
    ("52", "K521", [(f"Q8.{n}", 0, n + 1) for n in range(8)], 0), ("53", "B531", [("1", 0, 1), ("2", 0, 2)], 0),
]
# câbles PROFINET (13/11, Julien) : repère de câble PN1 à PN4, distinct des numéros de fil
CABLES_PN = {("K541", "P1"): "PN1", ("K541", "P2"): "PN2", ("K541", "P3"): "PN3", ("K541", "P4"): "PN4"}
NUM_ALERTES = []


def numeros_potentiels(phase):
    """{racine de potentiel : numéro}, et la fonction racine(point) qui traverse bornes et blocs de distribution."""
    pere = {}

    def r(k):
        while pere.setdefault(k, k) != k:
            pere[k] = pere[pere[k]]
            k = pere[k]
        return k
    for s_ in g.symbols:                     # bornes (broches 1 / 2) et blocs PTFIX : même potentiel
        if s_.rep[:1] == "X" and (set(s_.pins) == {"1", "2"} or s_.rep in ("X311", "X312", "X313", "X314")):
            pts = [g._find(("P", s_.folio) + tuple(xy)) for lst in s_.pins.values() for xy in lst]
            for q_ in pts[1:]:
                pere[r(pts[0])] = r(q_)
        if s_.rep in ("T301", "T302", "T321"):    # alimentations : bornes +V (et -V) reliées en interne
            for nom in ("+V", "-V"):
                pts = [g._find(("P", s_.folio) + (xy[0], xy[1])) for xy in s_.pins.get(nom, [])]
                for q_ in pts[1:]:
                    pere[r(pts[0])] = r(q_)
    num = {}
    cables = {g._find(("P", w[0], w[i], w[i + 1])) for w in g.wires for i in (1, 3)}
    for fol, rep_, pins_, dizaine in SOURCES_NUM:
        insts = [x for x in g.symbols if x.rep == rep_ and x.folio == F[fol]]
        if not insts:
            NUM_ALERTES.append(f"numérotation : {rep_} absent du folio {NUMFOL.get(fol, fol)}")
            continue
        for nom, k, unite in pins_:
            # 16/11 : un appareil peut être dessiné en plusieurs morceaux sur le folio (S1 voie 1 / voie 2)
            ss_ = [x for x in insts if len(x.pins.get(nom, [])) > k]
            if not ss_:
                NUM_ALERTES.append(f"numérotation : broche {rep_}:{nom}/{k} absente")
                continue
            for s_ in ss_:
                pts = s_.pins[nom]
                g_ = g._find(("P", s_.folio) + (pts[k][0], pts[k][1]))
                if g_ not in cables:
                    continue                  # broche non câblée
                u = unite if unite is not None else UNITE.get(phase.get(g_))
                if u is None:
                    continue
                n_ = f"{NUMFOL.get(fol, fol)}{dizaine + u:02d}"
                if num.setdefault(r(g_), n_) != n_:
                    NUM_ALERTES.append(f"numérotation : {rep_}:{nom} -> {n_}, potentiel déjà numéroté {num[r(g_)]}")
    return num, (lambda f_, x, y: r(g._find(("P", f_, x, y))))


NOUVEAUX_NUM = {"31", "32", "20", "21", "40", "41", "42", "43", "60", "55", "50", "51", "52", "53"}   # folios internes numérotés le 16/11


def zones_cables(f_):
    """v38 : rectangles où WinRelais dessine autour d'un câble (ellipse du blindé, cadre arrondi du repère, textes)
    et bords des cadres pointillés : aucun numéro de fil dessus (mêmes tailles que xrs_chevauchements)."""
    from xrs_gen import largeur
    out = []
    for n_, c in enumerate(g.cables):
        if c[0] != f_:
            continue
        _, x1, x2, y = c[:4]
        if g.cable_type.get(n_, 0) in (2, 3, 4, 5):
            out.append((x1 - 250, y - 350, x2 + 250, y + 350))
        for k_, (txt, tx, ty, sz) in enumerate(g.cable_textes(c)):
            if not txt:
                continue
            w_ = largeur(txt, sz)
            if k_ == 0 and isinstance(c[8], str) and c[8] != "bas":       # repère centré dans l'ovale (à gauche, ou à droite)
                tx = (x2 + 600 if c[8] == "texted" else x1 - 600) - w_ // 2
            out.append((tx - 150, ty - 100, tx + w_ + 150, ty + sz + 100) if k_ == 0 else (tx, ty, tx + w_, ty + sz))
    for tf, tx, ty, txt, sz, *_ in g.textes:      # v38 : textes libres du folio (lieux, notes)
        if tf == f_ and txt:
            out.append((tx, ty, tx + largeur(txt, sz), ty + sz))
    for d in g.dessins:
        if d[0] == f_ and d[5] == 0 and d[8] == 2:
            x1, x2, y1, y2 = min(d[1], d[3]), max(d[1], d[3]), min(d[2], d[4]), max(d[2], d[4])
            out += [(x1, y1 - 40, x2, y1 + 40), (x1, y2 - 40, x2, y2 + 40), (x1 - 40, y1, x1 + 40, y2), (x2 - 40, y1, x2 + 40, y2)]
    out += obstacles_symboles(f_)
    return out


_OBS = {}


def dessin_symbole(s_, point=100):
    """v42 : rectangles dessinés par un symbole : corps, textes dessinés dedans (BK, GN...), noms de broches affichés,
    points de connexion (± point)."""
    from xrs_gen import largeur
    out = [s_.bbox] if s_.bbox else []
    noms_ = s_.block[2].split("·")[5] == "1"
    sec = None
    for l in s_.block:
        if l.startswith("¤#"):
            sec = l
            continue
        f = l.split("·")
        if sec == "¤#MDessin¤" and len(f) > 5 and f[5]:
            sz = int(f[4] or 150)
            out.append((int(f[1]), int(f[2]), int(f[1]) + largeur(f[5], sz), int(f[2]) + sz))
        elif sec == "¤#Broche¤" and len(f) > 13:
            px, py = int(f[1]), int(f[2])
            out.append((px - point, py - point, px + point, py + point))
            if noms_ and f[0]:
                sz = int(f[13] or 200)
                out.append((int(f[5]), int(f[6]), int(f[5]) + largeur(f[0], sz), int(f[6]) + sz))
    return out


def obstacles_symboles(f_):
    """v42 (Julien 26/11 : numéro dans le symbole f64, sur les points rouges et les noms de broche f20) : corps des
    symboles, textes dessinés dans le symbole (BK, GN...), noms de broches affichés, points de connexion (± 100)."""
    cle_ = (f_, len(g.symbols), id(g.symbols))
    if cle_ not in _OBS:
        _OBS[cle_] = [r for s_ in g.symbols if s_.folio == f_ for r in dessin_symbole(s_, 0)]   # + 150 dans troncon_libre
    return _OBS[cle_]


def troncon_libre(f_, vertical, pos, lo, hi, renv=False, tous=False):
    """Plus longue partie [lo, hi] d'un fil où son numéro (bande de 300 à droite / sous le fil, comme le relit
    xrs_chevauchements) ne touche ni un fil perpendiculaire ni un texte de symbole (13/11)."""
    from xrs_gen import NUM_T
    bloc = []
    for x1, y1, x2, y2 in zones_cables(f_):   # v38 : ellipses, repères et textes de câble, bords des cadres pointillés
        if vertical and x1 < pos + NUM_T and x2 > pos:
            bloc.append((y1 - 150, y2 + 150))       # + 200 de retrait au placement : au moins 130 entre texte et dessin
        if not vertical and y1 < pos + NUM_T and y2 > pos:
            bloc.append((x1 - 200, x2 + 200))
    for w in g.wires:
        if w[0] != f_:
            continue
        if vertical and w[2] == w[4] and min(w[1], w[3]) < pos + NUM_T and max(w[1], w[3]) > pos:
            bloc.append((w[2] - 100, w[2] + 100))
        if not vertical and w[1] == w[3] and min(w[2], w[4]) < pos + NUM_T and max(w[2], w[4]) > pos:
            bloc.append((w[1] - 100, w[1] + 100))
    for s_ in g.symbols:
        if s_.folio != f_:
            continue
        for _, b in s_.texts:
            x1, x2, y1, y2 = min(b[0], b[2]), max(b[0], b[2]), min(b[1], b[3]), max(b[1], b[3])
            if vertical and x1 < pos + NUM_T and x2 > pos:
                bloc.append((y1 - 100, y2 + 100))
            if not vertical and y1 < pos + NUM_T and y2 > pos:
                bloc.append((x1 - 100, x2 + 100))
    if renv:                                  # 16/11 : flèches et textes des renvois
        for fa, pa, fb, pb, _, _ in g.renvois:
            for fr, pt in ((fa, pa), (fb, pb)):
                if fr != f_:
                    continue
                x1, y1, x2, y2 = g.renvoi_box(fr, pt)
                if vertical and x1 < pos + NUM_T and x2 > pos:
                    bloc.append((y1 - 100, y2 + 100))
                if not vertical and y1 < pos + NUM_T and y2 > pos:
                    bloc.append((x1 - 100, x2 + 100))
    segs = [(lo, hi)]
    for a, b in bloc:
        segs = [z for c, d in segs for z in ((c, d),) if b <= c or a >= d] + \
               [z for c, d in segs if not (b <= c or a >= d) for z in ((c, a), (b, d)) if z[1] > z[0]]
    if tous:
        return sorted(segs)
    return max(segs, key=lambda z: z[1] - z[0]) if segs else (lo, hi)


def centre_troncon(f_, ws, ph, renv=True):
    """v42 (Julien 26/11 : « centrer le numéro de fil par rapport à la longueur du câble ; pour les fils à plusieurs
    coudes, le plus au centre possible, sans superposition, en fonction de la taille de la police et de la longueur
    du texte ») : centre du tronçon = milieu de son plus long chemin (longueur réelle des fils) ; parmi les parties
    libres de chaque fil (troncon_libre : fils, textes, câbles, cadres, renvois, symboles, broches), position la plus
    proche de ce centre, mesurée le long des fils. Rend [folio, position du fil, début, fin de la partie libre, texte,
    angle, position voulue du centre du texte], ou None si rien ne tient."""
    import heapq
    from collections import defaultdict
    from xrs_gen import largeur, NUM_T
    segs = [w for w in ws if w[1:3] != w[3:5]]
    if not segs:
        return None
    lg = largeur(ph, NUM_T)
    adj = defaultdict(list)
    for w in segs:
        a, b, d = (w[1], w[2]), (w[3], w[4]), abs(w[3] - w[1]) + abs(w[4] - w[2])
        adj[a].append((b, d))
        adj[b].append((a, d))

    def dij(src):
        dist, prev, pq = dict(src), {}, [(d, n) for n, d in src.items()]
        heapq.heapify(pq)
        while pq:
            d, n = heapq.heappop(pq)
            if d > dist.get(n, 1e18):
                continue
            for m, l in adj[n]:
                if d + l < dist.get(m, 1e18):
                    dist[m], prev[m] = d + l, n
                    heapq.heappush(pq, (d + l, m))
        return dist, prev
    n0 = next((n for n in adj if len(adj[n]) == 1), next(iter(adj)))
    d1, _ = dij({n0: 0})
    a_ = max(d1, key=d1.get)
    d2, prev = dij({a_: 0})
    b_ = max(d2, key=d2.get)
    demi = d2[b_] / 2
    # point du milieu, sur le chemin a_ -> b_
    n, centre = b_, None
    while n != a_:
        p_ = prev[n]
        if d2[p_] <= demi <= d2[n]:
            t_ = demi - d2[p_]
            dx, dy = (n[0] > p_[0]) - (n[0] < p_[0]), (n[1] > p_[1]) - (n[1] < p_[1])
            centre = (p_, n, (p_[0] + dx * t_, p_[1] + dy * t_))
            break
        n = p_
    if centre is None:
        centre = (a_, a_, a_)
    p_, n, c_ = centre
    dc, _ = dij({p_: abs(c_[0] - p_[0]) + abs(c_[1] - p_[1]), n: abs(c_[0] - n[0]) + abs(c_[1] - n[1])})
    cands = []
    # au moins 130 entre le texte et l'obstacle le plus proche ; 60 puis 0 si rien ne tient (fils courts entre bornes)
    for marge in (130, 60, 0):
        _centre_cands(f_, segs, lg, marge, renv, p_, n, c_, dc, cands)
        if cands:
            break
    if os.environ.get("TTK_DBG") == ph:
        print("DBG", g.num(f_), ph, "longueur", d2[b_], "centre", centre, sorted(cands)[:6])
    if not cands:
        return None
    cout, _, pos, c, d, t, ang = min(cands)
    return [f_, pos, c, d, ph, ang, int(t)]


def _centre_cands(f_, segs, lg, marge, renv, p_, n, c_, dc, cands):
    for w in segs:
        v_ = w[1] == w[3]
        pos = w[1] if v_ else w[2]
        A, B = ((w[1], w[2]), (w[3], w[4]))
        ka, kb = (A[1], B[1]) if v_ else (A[0], B[0])
        lo, hi = min(ka, kb), max(ka, kb)
        libres = troncon_libre(f_, v_, pos, lo, hi, renv, True)
        if v_:      # le numéro de brin d'un câble s'écrit juste au-dessus du croisement (f20, 30/10) : on reste à l'écart
            for c in g.cables:
                if c[0] == f_ and pos in c[7] and lo < c[3] < hi:
                    libres = [z for a, b in libres for z in ((a, min(b, c[3] - 400)), (max(a, c[3] + 100), b)) if z[1] > z[0]]
        sur = {p_, n} == {A, B}                 # le centre est sur ce fil
        kc = c_[1] if v_ else c_[0]
        da, db = dc.get(A, 1e18), dc.get(B, 1e18)
        for c, d in libres:
            t_lo, t_hi = c + marge + lg / 2, d - marge - lg / 2
            if t_lo > t_hi:
                continue
            essais = {t_lo, t_hi, min(max(ka, t_lo), t_hi), min(max(kb, t_lo), t_hi)}
            if sur:
                essais.add(min(max(kc, t_lo), t_hi))
            for t in essais:
                cout = abs(t - kc) if sur else min(da + abs(t - ka), db + abs(t - kb))
                cands.append((round(cout), -(d - c), pos, c, d, t, 90 if v_ else 0))


def nommer_phases():
    """Fils de puissance (L, N) : nom de la phase (L1, L2, L3, N) au lieu d'un numéro (choix de Julien, 28/10).
    Phase connue aux bornes d'arrivée -X101 (1 = N, 2 = L1, 3 = L2, 4 = L3), propagée à travers les pôles
    des disjoncteurs et contacteurs et par les renvois. Un nom par tronçon de fil, centré sur le plus long segment ;
    les noms voisins et parallèles sont alignés sur une même ligne (demande du 29/10)."""
    from collections import defaultdict
    g._finalize_wires()
    phase = {}
    for s_ in g.symbols:
        if s_.rep in ("X101.1", "X101.2", "X101.3", "X101.4"):
            for pts in s_.pins.values():
                for xy in pts:
                    phase[g._find(("P", s_.folio) + xy)] = {"1": "N", "2": "L1", "3": "L2", "4": "L3"}[s_.rep[-1]]
        if s_.rep in ("T201", "T211"):  # sortie variateur -> moteur : U, V, W
            for nom, ph in (("X2:U", "U"), ("X2:V", "V"), ("X2:W", "W")):
                for xy in s_.pins.get(nom, []):
                    phase[g._find(("P", s_.folio) + xy)] = ph
        if s_.rep == "T101":        # variante USA : primaire H1-H3, secondaire X0 (N) X1-X3
            for nom, ph in (("H1", "L1"), ("H2", "L2"), ("H3", "L3"), ("X0", "N"), ("X1", "L1"), ("X2", "L2"), ("X3", "L3")):
                for xy in s_.pins.get(nom, []):
                    phase[g._find(("P", s_.folio) + xy)] = ph
    liens = []
    for s_ in g.symbols:
        paires = [(s_.pins[a][0], s_.pins[b][0]) for a, b in POLES if a in s_.pins and b in s_.pins]
        if len(s_.pins.get("N", [])) == 2:
            paires.append(tuple(s_.pins["N"]))
        for a, b in paires:
            liens.append((g._find(("P", s_.folio) + a), g._find(("P", s_.folio) + b)))
    change = True
    while change:
        change = False
        for a, b in liens:
            for u, v in ((a, b), (b, a)):
                if u in phase and v not in phase:
                    phase[v] = phase[u]
                    change = True
    # tronçon = fils du même type reliés bout à bout sur le folio (un symbole ou un renvoi coupe le tronçon)
    puissance = {F[n_] for n_ in F if "10" <= n_ <= "32"}       # PE nommé sur les folios de puissance
    global NUMPOT
    num_pot, racine_pot = numeros_potentiels(phase)
    NUMPOT = (num_pot, racine_pot)            # v37 : relu par les plans de bornier (n° de fil de chaque borne)
    numerotes = {F[n_] for n_ in NUMEROTES}
    nouveaux = {F[n_] for n_ in NOUVEAUX_NUM}
    from xrs_gen import largeur, NUM_T
    fils = [w for w in g.wires if w[5] in ("L", "N", "PN") or (w[5] == "PE" and w[0] in puissance) or w[0] in numerotes]
    pn = {}
    for s_ in g.symbols:
        for nom, pts in s_.pins.items():
            if (s_.rep, nom) in CABLES_PN:
                pn[g._find(("P", s_.folio) + (pts[0][0], pts[0][1]))] = CABLES_PN[(s_.rep, nom)]
    vus = {}                                  # contrôle global : un numéro <-> un seul potentiel
    pere = {}

    def racine(k):
        while pere.setdefault(k, k) != k:
            pere[k] = pere[pere[k]]
            k = pere[k]
        return k
    for w in fils:
        pere[racine((w[0], w[1], w[2]))] = racine((w[0], w[3], w[4]))
    troncons = defaultdict(list)
    for w in fils:
        troncons[racine((w[0], w[1], w[2]))].append(w)
    poses = []                          # [folio, position du fil, début, fin, nom, angle, position voulue]
    # v37 (revue Krizox, D02) : pas de numéro sur le câble client (tronçons qui arrivent sur la broche 1 des bornes X10)
    client = {(s_.folio,) + tuple(s_.pins["1"][0]) for s_ in g.symbols if s_.rep.startswith("X101.")}
    for ws in troncons.values():
        f_ = ws[0][0]
        if any((w[0], w[1], w[2]) in client or (w[0], w[3], w[4]) in client for w in ws):
            continue
        ph = "PE" if ws[0][5] == "PE" else phase.get(g._find(("P", f_, ws[0][1], ws[0][2])))
        if ws[0][5] == "PN":
            ph = pn.get(g._find(("P", f_, ws[0][1], ws[0][2])))
            if not ph:
                NUM_ALERTES.append(f"câble PROFINET sans repère : folio {g.num(f_)} en {ws[0][1:5]}")
        elif f_ in numerotes and ws[0][5] != "PE":
            rac_ = racine_pot(f_, ws[0][1], ws[0][2])
            n_ = num_pot.get(rac_)
            if not n_:
                NUM_ALERTES.append(f"numérotation : folio {g.num(f_)}, fil sans numéro en {ws[0][1:5]}")
            elif vus.setdefault(n_, rac_) != rac_:
                NUM_ALERTES.append(f"numérotation : {n_} porté par deux potentiels différents (folio {g.num(f_)})")
            ph = n_ or ph
        if not ph:
            continue
        # bus (horizontale de plus de 6000) : nom près de l'extrémité gauche, aligné avec les autres lignes du bus
        lignes = defaultdict(int)
        for w in ws:
            if w[2] == w[4]:
                lignes[w[2]] += abs(w[3] - w[1])
        yb = max(lignes, key=lignes.get) if lignes else None
        # v42 : barre = ligne horizontale de plus de 6000 avec au moins 2 piquages (un long fil coudé n'est pas une barre)
        deg_ = defaultdict(int)
        for w in ws:
            deg_[(w[1], w[2])] += 1
            deg_[(w[3], w[4])] += 1
        if yb is not None and lignes[yb] >= 6000 and sum(1 for (x_, y_), d_ in deg_.items() if y_ == yb and d_ >= 3) < 2:
            yb = None
        if yb is not None and lignes[yb] >= 6000:
            w = min((w for w in ws if w[2] == w[4] == yb), key=lambda w_: min(w_[1], w_[3]))
            lo, hi = min(w[1], w[3]), max(w[1], w[3])
            if f_ in nouveaux:                # 16/11 : 1er morceau libre du bus entier (renvoi, descentes)
                lo = min(min(w_[1], w_[3]) for w_ in ws if w_[2] == w_[4] == yb)
                hi = max(max(w_[1], w_[3]) for w_ in ws if w_[2] == w_[4] == yb)
                lg = largeur(ph, NUM_T) + 400
                lo, hi = next(((a, b) for a, b in troncon_libre(f_, False, yb, lo, hi, True, True) if b - a >= lg), (lo, hi))
                poses.append([f_, yb, lo, hi, ph, 0, lo + 200 + lg // 2])
                continue
            poses.append([f_, yb, lo, hi, ph, 0, lo + 800])
            continue
        if f_ in numerotes:                   # v42 : numéro centré sur la longueur du tronçon (Julien 26/11)
            p_ = centre_troncon(f_, ws, ph)
            if p_:
                poses.append(p_)
                continue
            NUM_ALERTES.append(f"numérotation : folio {g.num(f_)}, {ph} : aucune place libre, ancien placement")
        w = max(ws, key=lambda w_: abs(w_[3] - w_[1]) + abs(w_[4] - w_[2]))
        if f_ in nouveaux:                    # 16/11 : le fil du tronçon qui a le plus de place libre
            def libre(w_):
                v_ = w_[1] == w_[3]
                a, b = (min(w_[2], w_[4]), max(w_[2], w_[4])) if v_ else (min(w_[1], w_[3]), max(w_[1], w_[3]))
                c, d = troncon_libre(f_, v_, w_[1] if v_ else w_[2], a, b, True)
                return d - c
            w = max((w_ for w_ in ws if w_[1:3] != w_[3:5]), key=libre, default=w)
        if w[1:3] == w[3:5]:
            continue
        if w[1] == w[3]:
            lo, hi = min(w[2], w[4]), max(w[2], w[4])
            if f_ in numerotes:
                lo, hi = troncon_libre(f_, True, w[1], lo, hi, f_ in nouveaux)
            # le numéro de brin d'un câble s'écrit juste au-dessus du croisement (f20, 30/10) : on reste à l'écart
            for c_ in g.cables:
                if c_[0] == f_ and w[1] in c_[7] and lo < c_[3] < hi:
                    lo, hi = max(((lo, c_[3] - 400), (c_[3] + 100, hi)), key=lambda a: a[1] - a[0])
            poses.append([f_, w[1], lo, hi, ph, 90, (lo + hi) // 2])
        else:
            lo, hi = min(w[1], w[3]), max(w[1], w[3])
            if f_ in numerotes:
                lo, hi = troncon_libre(f_, False, w[2], lo, hi, f_ in nouveaux)
            poses.append([f_, w[2], lo, hi, ph, 0, (lo + hi) // 2])
    # alignement (29/10) : fils parallèles voisins (<= 1200) qui se recouvrent sur au moins 400 -> même ligne
    for ang in (0, 90):
        groupes = []
        for p in sorted((p for p in poses if p[5] == ang), key=lambda p: (p[0], p[1])):
            for c in groupes:
                # v42 : on n'aligne que des numéros dont les centres voulus sont proches (sinon chacun au centre de son fil)
                if c[-1][0] == p[0] and 0 < p[1] - c[-1][1] <= 1200 and (c[-1][4] == "PE") == (p[4] == "PE") and \
                        max(q[2] for q in c + [p]) + 400 <= min(q[3] for q in c + [p]) and \
                        abs(p[6] - sum(q[6] for q in c) / len(c)) <= 400:
                    c.append(p)
                    break
            else:
                groupes.append([p])
        groupes2 = []
        for c in groupes:                     # 16/11 : groupe sans place commune -> chaque numéro sur son fil
            demi = max(largeur(q[4], NUM_T) for q in c) / 2
            if len(c) > 1 and max(q[2] for q in c) + 130 + demi > min(q[3] for q in c) - 130 - demi:
                groupes2 += [[q] for q in c]
            else:
                groupes2.append(c)
        for c in groupes2:
            # v42 : marge de 130 entre le texte et la fin de sa partie libre, texte entier dans la partie libre
            demi = max(largeur(q[4], NUM_T) for q in c) / 2     # texte centré (l'ancre est au début du texte)
            lo, hi = max(q[2] for q in c) + 130 + demi, min(q[3] for q in c) - 130 - demi
            voulu = sum(q[6] for q in c) // len(c)
            mid = min(max(voulu, lo), hi) if lo <= hi else (max(q[2] for q in c) + min(q[3] for q in c)) // 2
            for f_, pos, _, _, ph, _, _ in c:
                if ang == 90:
                    # v38 (Julien 24/11) : f12, « PE » à gauche du fil (à droite, il se lisait mal)
                    xg = pos - NUM_T - 100 if ph == "PE" and f_ == F["13"] else pos
                    g.numeros.append((f_, xg, int(round((mid + demi) / 100)) * 100, ph, 90))
                else:
                    g.numeros.append((f_, int(round((mid - demi) / 100)) * 100, pos, ph, 0))


def renommer_symboles():
    """À appeler avant l'écriture : les contrôles relisent le fichier avec les nouveaux repères."""
    for p_ in g.symbols:
        p_.rep = ren(p_.rep)


g.place = _place_ren
g.texte = lambda folio, x, y, txt, *a, **k: _texte(folio, x, y, ren(txt), *a, **k)
g.cable = lambda folio, x1, x2, y, rep_, compo, desig, *a, **k: _cable(folio, x1, x2, y, ren(rep_), compo, ren(desig), *a, **k)
g.folio = lambda numero, titre, description: _folio(numero, titre, ren(description))
F = {f["num"]: g.folio(NUMFOL.get(f["num"], f["num"]), f["titre"], f["desc"]) for f in FOL}

C = "CUSTOM\\"
BORNE = "Bornes - Standard\\Borne 4 mm.xsy"
ROUGE = 255
# barres 24VELEC et 0 V en haut des folios de commande (demande du 29/10)
RAIL24_Y, RAIL0_Y = 2000, 2800
PE_DEST = []        # (folio, point) : fils PE courts des appareils, renvoyés vers la terre de l'arrivée (f10)


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


# bornes de terre vert/jaune (achetées le 03/11) : PE arrivée, PE moteurs M1 / M2, FE de l'IHM
BORNES_PE = {"X101.VJ", "X701.17", "X701.25", "X711.23", "X701.47", "X701.48"}   # + V/J de W9 / W10 (18/11)
BORNE_PE = os.path.join(ICI, "librairie", "CUSTOM", "Borne_4mm_terre_vert-jaune.xsy")


def borne(rep, f, x, y, fpos=None):
    """Borne 4 mm verticale : broche 1 en (x, y), broche 2 en (x, y + 400). fpos = repère (à droite par défaut).
    Borne de terre vert/jaune pour les repères de BORNES_PE (même géométrie).
    16/11 : sur les folios de sécurité (40 à 42), repère à côté du corps de la borne, pour laisser le fil libre
    au numéro de fil (bornes à 400 l'une de l'autre) ; idem au f62 (interne 52)."""
    if fpos is None:
        fpos = (150, 125) if f in ("40", "41", "42", "43", "52") else (100, -250)
    bornier = rep.split(".")[0]
    des = DES_BORNE.get(rep) or REP.get(rep, {}).get("des") or REP.get(bornier, {}).get("des", "")
    pe = rep in BORNES_PE
    return g.place(BORNE_PE if pe else BORNE, rep, F[f], x, y, champs={2: des, 4: "borne de terre vert/jaune" if pe else ""}, ref=(),
                   compact=True, rep_size=150, fpos=fpos, loc="A1", prefix="X")


# v37 (revue Krizox, D08, Julien 23/11) : boîte de jonction machine +BJM dessinée. Tous les câbles sortants y passent
# (W11 du pupitre compris) ; de la boîte aux appareils : des fils. Bornier +BJM-X1, bornes X1.1 à X1.n numérotées dans
# l'ordre de la boîte (calcul du 17/11, 09_STOCK) : 400 V (W2, W5, W4) | 48 V (W9, W10) | sondes TF (W3, W6) | W12 | W14 |
# W8 | W11. Bornes de terre pour les PE des moteurs et le V/J de W11 (FE de l'IHM). Les conducteurs de réserve ne sont
# pas bornés au schéma. Repères internes des câbles (RENOMME) : W201 = W2, W211 = W5, W202 = W4, W321 / W322 = W9 / W10,
# W203 / W213 = W3 / W6, W531 = W8.
BJM_ORDRE = ([("W201", c) for c in ("U", "V", "W", "PE")] + [("W211", c) for c in ("U", "V", "W", "PE")]
             + [("W202", c) for c in (1, 2, 3, 4)] + [("W321", c) for c in (1, 2, 3, 4)] + [("W322", c) for c in (1, 2, 3, 4)]
             + [("W203", c) for c in (1, 2)] + [("W213", c) for c in (1, 2)] + [("W12", c) for c in range(1, 17)]
             + [("W14", c) for c in (1, 2, 3, 4)] + [("W531", c) for c in (1, 2)] + [("W11", c) for c in range(1, 23)]
             + [("W11", "PE")])
BJM_NUM = {k: i + 1 for i, k in enumerate(BJM_ORDRE)}
BJM_PE = {("W201", "PE"), ("W211", "PE"), ("W11", "PE")}
BJM_POSES = {}          # (câble, conducteur) -> repère de la borne posée


def bjm(f, x, y, cable, cond, fpos=None):
    """Borne de la boîte +BJM (X1.n, localisation BJM), même géométrie que borne() (broche 1 en haut)."""
    rep = f"X1.{BJM_NUM[(cable, cond)]}"
    if rep in BJM_POSES.values():
        raise SystemExit(f"borne +BJM {rep} posée deux fois")
    BJM_POSES[(cable, cond)] = rep
    if fpos is None:
        fpos = (150, 125)          # repère à côté du corps de la borne : fils libres au-dessus et en dessous (numéros)
    pe = (cable, cond) in BJM_PE
    return g.place(BORNE_PE if pe else BORNE, rep, F[f], x, y, champs={2: "Boîte de jonction machine +BJM",
                   4: "borne de terre vert/jaune" if pe else ""}, ref=(), compact=True, rep_size=150, fpos=fpos, loc="BJM",
                   prefix="X")


def emprise(elems):
    """Rectangle englobant (symboles avec leurs textes, ou rectangles) : (x1, y1, x2, y2). v40."""
    bx = []
    for e in elems:
        if isinstance(e, tuple):
            bx.append(e)
            continue
        bx += dessin_symbole(e, 0)               # v42 : corps, broches, noms de broches, textes dessinés
        bx += [b for _, b in e.texts]
    return (min(b[0] for b in bx), min(b[1] for b in bx), max(b[2] for b in bx), max(b[3] for b in bx))


def cadre_lieu(f, elems, lieu, marge=300, haut=None, droite=False, gauche=False, txt=None):
    """Cadre pointillé autour d'appareils hors armoire (v37, D09 / D10), localisation écrite en haut à gauche
    (droite=True : à droite du cadre, à mi-hauteur). elems : symboles posés (Placed) ou rectangles (x1, y1, x2, y2).
    haut : place réservée au-dessus pour le texte."""
    bx = []
    for e in elems:
        if isinstance(e, tuple):
            bx.append(e)
            continue
        bx += dessin_symbole(e, 0)               # v42 : corps, broches, noms de broches, textes dessinés
        bx += [b for _, b in e.texts]
    x1, y1 = min(b[0] for b in bx) - marge, min(b[1] for b in bx) - marge - (haut if haut is not None else 300)
    x2, y2 = max(b[2] for b in bx) + marge, max(b[3] for b in bx) + marge
    x1, y1, x2, y2 = x1 // 100 * 100, y1 // 100 * 100, -(-x2 // 100) * 100, -(-y2 // 100) * 100
    g.cadre(F[f], x1, y1, x2, y2, width=20, dashed=True)
    if txt:                                      # position imposée du texte (coordonnées du folio)
        texte(f, txt[0], txt[1], lieu, 200, 0, 1)
    elif droite:
        texte(f, x2 + 150, (y1 + y2) // 2 - 100, lieu, 200, 0, 1)
    elif gauche:
        from xrs_gen import largeur
        texte(f, x1 - 150 - largeur(lieu, 200) // 100 * 100 - 100, (y1 + y2) // 2 - 100, lieu, 200, 0, 1)
    else:
        texte(f, x1 + 100, y1 + 60, lieu, 200, 0, 1)
    return (x1, y1, x2, y2)


def W(f, pts, t):
    return g.wire(F[f], pts, t)


def reserve(f, pins, bas):
    """E/S de réserve (16/11, Julien) : trait fin le long des broches libres + « Réserve » centré, du côté des fils
    (bas=True : broches en bas du module). Remplace les phrases « ... : réserve »."""
    from xrs_gen import largeur
    xs = [p.x for p in pins]
    y0 = pins[0].y
    yl = y0 + 700 if bas else y0 - 900
    tick = -200 if bas else 200
    if len(xs) > 1:
        g.ligne(F[f], min(xs), yl, max(xs), yl, width=10)
        for x_ in (min(xs), max(xs)):
            g.ligne(F[f], x_, yl, x_, yl + tick, width=10)
    t_ = "Réserve"
    xc = (min(xs) + max(xs)) // 2
    texte(f, xc - largeur(t_, 180) // 2, yl + 80 if bas else yl - 260, t_, 180)


def stub(f, pt, to, t):
    """Fil de pt vers to ; rend pt (point de renvoi)."""
    W(f, [pt, to], t)
    return pt


def renvoi(fa, pa, fb, pb, t, vertical=True):
    g.renvoi(F[fa], pa, F[fb], pb, t, vertical)


def texte(f, x, y, txt, size=250, color=0, bold=0):
    g.texte(F[f], x, y, txt, size, color, bold)


def etiquette(f, xs, y, txt, size=300):
    """Texte centré sous / sur un groupe de renvois (xs = abscisses des renvois)."""
    xc = sum(xs) / len(xs)
    texte(f, int(round((xc - len(txt) * size * 0.55 / 2) / 100) * 100), y, txt, size, 0, 1)


def proposition(f, lignes, x=2400, y=1400):
    texte(f, x, y, "PROPOSITION A VALIDER : " + lignes[0], 250, ROUGE, 1)
    for i, l in enumerate(lignes[1:], 1):
        texte(f, x, y + 300 * i, l, 220, ROUGE)


# ======================================================================== 01 - 04
texte("01", 4000, 3600, "MACHINE DE TRESSAGE TTK", 900, 0, 1)
texte("01", 4000, 5000, "DOSSIER DE SCHEMAS ELECTRIQUES", 600, 0, 1)
texte("01", 4000, 6200, "Client : TTK          N° machine : 001-EU", 300)     # v42 (Julien 26/11) : « Affaire » retiré
g.tableau(F["01"], 4000, 7600, [6000, 10000], 500, [
    ["Caractéristiques d'alimentation", ""],
    ["Réseau", "3 x 400 V + N + PE - 50 Hz (câble client -W101 5G4)"],
    ["Variante USA", "3 x 480 V via transformateur -T101 15 kVA (option)"],
    ["Protection de tête", "-Q102 : 20 A courbe C - 10 kA"],
    ["Régime de neutre / Icc", "TN-S / Icc présumé 6 kA au point de livraison"],
], size=250)
for i, logo in enumerate(("TTK", "BEBL", "LEVERT INDUSTRIE")):
    x = 4000 + 7200 * i
    g.cadre(F["01"], x, 12400, x + 6400, 16400, width=20)

# logos insérés par Julien dans la v24 (09/11), positions et tailles relevées ; images dans schema/images
# TTK_IMAGES (18/11, essai des 2 PC) : dossier des images écrit dans le .xrs (relatif ou absolu) ; défaut : schema/images du dépôt
# Défaut (18/11, essai réussi dans WinRelais) : chemin relatif au .xrs, valable pour release/ et old/ sur les 2 PC
# v37 (23/11, PC PERSO JULIEN) : le chemin relatif n'est pas trouvé par WinRelais sur ce PC (« logo_TTK.jpg ? »).
# Défaut = chemin absolu de schema/images du dépôt, recalculé à chaque génération (juste sur le PC qui génère).
IMG = os.environ.get("TTK_IMAGES") or os.path.normpath(os.path.join(ICI, "..", "schema", "images"))
for nom_, x_, y_, w_, h_, r_ in (("logo_TTK.jpg", 4500, 12700, 5480, 3480, 1575), ("logo_BEBL.jpg", 11500, 13100, 5806, 2615, 2221),
                             ("logo_LEVERT_INDUSTRIE.jpg", 18600, 13700, 6000, 1308, 4588)):
    g.logos.append((F["01"], x_, y_, w_, h_, os.path.join(IMG, nom_), r_))

rows = [["N°", "Titre", "Description"]] + [[NUMFOL.get(f["num"], f["num"]), f["titre"], ren(f["desc"])] for f in FOL]
g.tableau(F["02"], 1600, 1600, [1600, 9200, 16800], (19200 - 1600) // len(rows), rows, size=260)

# synoptique en logigramme (02/11) : blocs encadrés reliés par des flèches, dans le sens de l'énergie
SY = F["04"]


def bloc(x1, y1, x2, lignes, dashed=False):
    """Cadre + titre en gras + lignes ; rend (x1, y1, x2, y2). Refuse un texte plus large que le cadre."""
    # v40 (Julien 25/11 : lisibilité) : textes 240 / 210 (220 / 200 avant), interligne 360
    y2 = y1 + 360 * len(lignes) + 300
    g.cadre(SY, x1, y1, x2, y2, width=30, dashed=dashed)
    for i, t in enumerate(lignes):
        sz = 240 if i == 0 else 210
        if len(ren(t)) * sz * 0.55 > x2 - x1 - 400:
            raise SystemExit(f"f04 : texte trop long pour son cadre : {t}")
        texte("04", x1 + 200, y1 + 150 + 360 * i, t, sz, 0, 1 if i == 0 else 0)
    return (x1, y1, x2, y2)


def fleche(pts, dashed=False, tete=True):
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        g.ligne(SY, xa, ya, xb, yb, width=30, dashed=dashed)
    if tete:
        (xa, ya), (xb, yb) = pts[-2], pts[-1]
        dx, dy = (xb > xa) - (xb < xa), (yb > ya) - (yb < ya)
        for k in (-1, 1):
            g.ligne(SY, xb - 250 * dx + 150 * k * dy, yb - 250 * dy + 150 * k * dx, xb, yb, width=30)


# v37 (revue Krizox, D18, Julien 23/11) : synoptique PAR LIEU (remplace le synoptique par fonction) : un cadre pointillé par
# localisation (réseau client, armoire +A1, boîte +BJM, machine +M, pupitre +P1), ses appareils principaux dans des blocs,
# les câbles entre les cadres (repère + composition), PROFINET en pointillés.
def lieu(x1, y1, x2, y2, titre):
    g.cadre(SY, x1, y1, x2, y2, width=30, dashed=True)
    texte("04", x1 + 200, y1 + 150, titre, 280, 0, 1)      # v40 : titre 260 -> 280


def liaison(pts, txt, y_txt=None, x_txt=None, dashed=False):
    fleche(pts, dashed=dashed)
    (xa, ya), (xb, yb) = pts[0], pts[1]
    texte("04", x_txt if x_txt is not None else min(xa, xb) + 150, (y_txt if y_txt is not None else ya - 300), txt, 200)


# réseau client (à gauche)
lieu(1600, 1600, 7200, 6800, "RESEAU CLIENT")
cli = bloc(1900, 2300, 6900, ["ARRIVEE (f10)", "3 x 400 V + N + PE - 50 Hz", "TN-S - Icc 6 kA"])
usa = bloc(1900, 4300, 6900, ["VARIANTE USA (option)", "3 x 480 V -> -TR1 15 kVA", "-> 400 V (f10)"], dashed=True)
# armoire +A1 (au centre)
XA1, XA2 = 8800, 17600         # v40 (Julien 25/11 : lisibilité) : armoire moins large, plus de place aux câbles
lieu(XA1, 1600, XA2, 19200, "ARMOIRE +A1")
ya = 2300
BL = {}
BLOCS_A1 = (("pui", ["PUISSANCE (f10 à f14)", "-QS1, -QF1 20 A ; -QM1 / -KM1, -QM2 / -KM2", "-QF2 / -KF1, -QF3 / -KF2 (freins)"]),
                    ("ali", ["ALIMENTATIONS (f13, f31)", "-T1 24VSEC, -T2 24VELEC, -T3 48 V", "blocs -X21.11 à -X21.14, PELV -X12.11"]),
                    ("var", ["VARIATEURS (f20, f21)", "-U1, -U2 MCX91A, résistances -R1 / -R2"]),
                    ("pap", ["PAS-A-PAS (f32)", "-KA2 (48 V en Manu), drivers -U3 / -U4"]),
                    ("sec", ["SECURITE (f40 à f43)", "relais -KA1, fusible -FA1"]),
                    ("api", ["AUTOMATE (f55 à f53)", "-K1 CPU 1214C, -K2 SM 1223, -K3 SM 1231 TC"]),
                    ("swi", ["RESEAU (f54)", "switch PROFINET -K4"]),
                    ("por", ["PORTE", "-S1 AU, -S4 réarmement, -H2 / -H3 / -H4"]),
                    ("bor", ["BORNIERS (f71 à f74)", "-X10 à -X64, terre -XPE1"]))
# v40 (Julien 25/11 : forme) : blocs de l'armoire répartis sur toute la hauteur du cadre (écart égal entre blocs)
GAP_A1 = (19200 - 400 - 2300 - sum(360 * len(l_) + 300 for _, l_ in BLOCS_A1)) // (len(BLOCS_A1) - 1) // 10 * 10
for cle, lignes in BLOCS_A1:
    BL[cle] = bloc(XA1 + 300, ya, XA2 - 300, lignes)
    ya = BL[cle][3] + GAP_A1
# boîte de jonction machine +BJM
XB1, XB2 = 20800, 23600
lieu(XB1, 4400, XB2, 15600, "BOITE +BJM")
bjm_b = bloc(XB1 + 200, 5200, XB2 - 200, ["BORNIER -X1", "69 bornes", "fabrication BEBL"])
# machine +M et pupitre +P1 (à droite)
XM1, XM2 = 24800, 29200
lieu(XM1, 1600, XM2, 12000, "MACHINE +M")
mac = bloc(XM1 + 200, 2300, XM2 - 200, ["APPAREILS", "-M1 / -M2 motoréducteurs", "-M3 / -M4 pas-à-pas", "-B1 / -B2 capots",
                                        "-B3 à -B6 fins de course", "-H1 colonne lumineuse", "-B7 thermocouple"])
lieu(XM1, 12800, XM2, 19200, "PUPITRE +P1")
pup = bloc(XM1 + 200, 13500, XM2 - 200, ["APPAREILS", "-P1 IHM KTP700", "-S2 arrêt d'urgence", "-S3 sélecteur Auto / Manu"])
# câbles entre les lieux
liaison([(7200, 6000), (XA1, 6000)], "-W1 5G4", y_txt=5650, x_txt=7300)
y_ = 5200
for txt in ("-W2 / -W5 4G2,5 (moteurs)", "-W3 / -W6 2x0,75 (sondes TF)", "-W4 5G1,5 (freins)", "-W9 / -W10 5G1,5 (pas-à-pas)",
            "-W8 compensation type K", "-W12 19G1 (machine)", "-W14 M12 (capot -B2)", "-W11 27G1 (pupitre)"):
    fleche([(XA2, y_), (XB1, y_)])
    texte("04", XA2 + 150, y_ - 300, txt, 180)          # v40 : 160 -> 180
    y_ += 1300
fleche([(XB2, 7600), (XM1, 7600)])
texte("04", XB2 + 150, 7250, "fils", 200)
fleche([(XB2, 14400), (24200, 14400), (24200, 16000), (XM1, 16000)])
texte("04", XB2 + 150, 14050, "fils", 200)
fleche([(XA2, 17600), (XM1, 17600)], dashed=True)
texte("04", XA2 + 200, 17250, "PN4 PROFINET (câble RJ45 direct)", 200)
fleche([(XA2, 2400), (XM1, 2400)])
texte("04", XA2 + 200, 2050, "-W13 V/J 4 mm² (bâti machine)", 200)


# ======================================================================== règles de mise en page
# Un renvoi WinRelais dessine flèche + texte sur ~1,6 cm AU-DELA de son point, côté opposé au fil :
# barres de potentiel de XL à XR, renvois du haut à y >= 3200, renvois voisins espacés de 800.
XL, XR = 3200, 27200


def decrit(xsy, rep, f, x, y, des, **kw):
    """Esclave affichant repère + description (pour savoir à quel appareil il appartient)."""
    kw.setdefault("rep_size", 200)
    kw.setdefault("wrap", 22)
    champs = {2: des}
    if kw.pop("nomenc", False):            # v34 : fabricant et caractéristiques écrits (non affichés) pour la nomenclature
        champs.update({3: REP.get(rep, {}).get("fab", ""), 4: REP.get(rep, {}).get("carac", "")})
    return g.place(xsy, rep, F[f], x, y, champs=champs, ref=(), compact=False, shown=(2,),
                   loc=loc(rep), **kw)


# ======================================================================== 10 ARRIVEE
f = "10"
# arrivée réseau dans un cadre (demande du 29/10)
g.cadre(F[f], 3200, 1300, 9800, 2000, width=20, dashed=True)     # pointillé (Julien, 02/11)
texte(f, 3400, 1400, "ARRIVEE RESEAU 3 x 400 V + N + PE - 50 Hz", 250, 0, 1)
for x, t in ((4400, "PE"), (5200, "N"), (6000, "L1"), (6800, "L2"), (7600, "L3")):
    texte(f, x - 150, 1700, t, 200)
xb = {"X101.VJ": 4400, "X101.1": 5200, "X101.2": 6000, "X101.3": 6800, "X101.4": 7600}
B = {r: borne(r, f, x, 4400) for r, x in xb.items()}     # 13/11 : 3600 -> 4400 (arrivée aérée, Julien)
for r, x in xb.items():
    W(f, [(x, 2000), B[r]["1"]], "PE" if r.endswith("VJ") else ("N" if x == 5200 else "L"))
# v37 (revue Krizox) : W1 dessiné comme les autres câbles (trait du 1er au dernier conducteur, repère dans l'ovale),
# non blindé ; V/J dans le trait sans numéro de brin (brins 1 à 4) ; l'ancien W1 sortait mal à l'export PDF (Julien)
# v40 (Julien 25/11 : « infos du câble W1 pas bonnes ») : trait au milieu entre le cadre d'arrivée et les bornes
# (brins à 500 du cadre), composition centrée sous le repère
from xrs_gen import largeur as _lg
# v42 (Julien 26/11 : « W1 et 5G4 à droite du câble ») ; v43 : retouche de Julien sur la v42 reprise (textes à droite, sans
# ovale : W1, puis 5G4 et « Câble client » dessous)
g.cable(F[f], 0, 0, 2800, "W101", "5G4", "Câble client", [5200, 6000, 6800, 7600], ovale=True, blinde=False, vj=[4400],
        droite=True)
q101 = maitre(C + "Legrand_Vistop_022515_4P_63A.xsy", "Q101", f, 5200, 6000, fpos=(3000, 0))   # v42 : repère 200 à droite (nom 5/L3)
q102 = maitre(C + "Hager_NFT820_disjoncteur_3P+N_20A.xsy", "Q102", f, 5200, 10000)
for r, p in (("X101.1", ("N", 0)), ("X101.2", "1/L1"), ("X101.3", "3/L2"), ("X101.4", "5/L3")):
    W(f, [B[r]["2"], q101[p]], "N" if r == "X101.1" else "L")
for a, b, t in ((("N", 1), ("N", 0), "N"), ("2/T1", "1", "L"), ("4/T2", "3", "L"), ("6/T3", "5", "L")):
    W(f, [q101[a], q102[b]], t)
# sorties de -QF1 : renvois directs vers le bus 400 V (f12), sans répartiteur dessiné (29/10)
ends10 = {pin: W(f, [q102[pin], (q102[pin].x, 15200)], "N" if pin == ("N", 1) else "L")
          for pin in (("N", 1), "2", "4", "6")}
etiquette(f, [q102[p_].x for p_ in (("N", 1), "2", "4", "6")], 17000, "Distribution (f12, N : f13)", 260)
# terre : PE dans le faisceau (option A), puis une dérivation courte par appareil (renvois posés à la fin)
PE10 = W(f, [B["X101.VJ"]["2"], (4400, B["X101.VJ"]["2"].y + 400), (3600, B["X101.VJ"]["2"].y + 400), (3600, 18000)], "PE")   # peigne en bas, renvois à droite
# variante USA : déplacée à gauche par Julien dans WinRelais (v7 du 29/10), reprise ici
t101 = maitre(C + "TEMCo_TT1041_transformateur_480D_400Y230_15kVA.xsy", "T101", f, 18000, 4800, wrap=24, noms=False)
g.cadre(F[f], 15200, 2000, 25600, 9200, width=20, dashed=True)
texte(f, 15400, 2100, "VARIANTE USA (option) - réseau 3 x 480 V", 220, 0, 1)
for pin in ("H1", "H2", "H3", "GND"):
    W(f, [t101[pin], (t101[pin].x, 3600)], "PE" if pin == "GND" else "L")
for pin in ("X0", "X1", "X2", "X3"):
    W(f, [t101[pin], (t101[pin].x, 8400)], "N" if pin == "X0" else "L")
texte(f, 15400, 2700, "480 V L1 L2 L3 / PE", 200)

# ======================================================================== 12 DISTRIBUTION 400 V
f = "12"
gv = C + "Schneider_GV2ME14_disjoncteur_moteur.xsy"
poles = C + "Schneider_LC1D09BD_contacts_puissance_3P.xsy"
DY12 = 2800                        # place pour le bus en haut du folio (descendu de 800 le 02/11)
q121 = maitre(gv, "Q121", f, 4800, 3600 + DY12)
km1p = contacteur(poles, "KM1", f, 4800, 8400 + DY12, prefix="KM")
q122 = maitre(gv, "Q122", f, 12000, 3600 + DY12)
km2p = contacteur(poles, "KM2", f, 12000, 8400 + DY12, prefix="KM")
q123 = maitre(C + "Schneider_A9F74202_iC60N_2P_2A_C.xsy", "Q123", f, 18400, 3600 + DY12)
q421p = contacteur(poles, "Q421", f, 17600, 8400 + DY12)
q124 = maitre(C + "Schneider_A9F74202_iC60N_2P_2A_C.xsy", "Q124", f, 24000, 3600 + DY12)
q422p = contacteur(poles, "Q422", f, 23200, 8400 + DY12)
# bus tétra L1 L2 L3 N : renvois depuis -QF1 (f10) à gauche, vers le bus 230 V (f13) à droite ;
# chaque appareil se pique sur les phases qu'il utilise
BUS12 = {"L1": 2400, "L2": 3200, "L3": 4000}      # N retiré le 02/11 : rien ne s'y pique, il part de QF1 vers f13
for q, pins in ((q121, (("1/L1", "L1"), ("3/L2", "L2"), ("5/L3", "L3"))), (q122, (("1/L1", "L1"), ("3/L2", "L2"), ("5/L3", "L3"))),
                (q123, (("1", "L1"), ("3", "L2"))), (q124, (("1", "L1"), ("3", "L3")))):
    for p, ph in pins:
        W(f, [(q[p].x, BUS12[ph]), q[p]], "L")
for ph, y in BUS12.items():
    W(f, [(XL, y), (XR, y)], "L")
for q, k in ((q121, km1p), (q122, km2p)):
    for a, b in (("2/T1", "1/L1"), ("4/T2", "3/L2"), ("6/T3", "5/L3")):
        W(f, [q[a], k[b]], "L")
for q, k in ((q123, q421p), (q124, q422p)):
    W(f, [q["2"], k["3/L2"]], "L")
    W(f, [q["4"], k["5/L3"]], "L")
out12 = {}
for k in (km1p, km2p):
    for p in ("2/T1", "4/T2", "6/T3"):
        out12[(k.rep, p)] = W(f, [k[p], (k[p].x, 11600 + DY12)], "L")
for k in (q421p, q422p):
    for p in ("4/T2", "6/T3"):
        out12[(k.rep, p)] = W(f, [k[p], (k[p].x, 11600 + DY12)], "L")
for k, pins, t in ((km1p, ("2/T1", "4/T2", "6/T3"), "VARIATEUR 1"), (km2p, ("2/T1", "4/T2", "6/T3"), "VARIATEUR 2"),
                   (q421p, ("4/T2", "6/T3"), "FREIN M201"), (q422p, ("4/T2", "6/T3"), "FREIN M211")):
    etiquette(f, [k[p_].x for p_ in pins], 13600 + DY12, t)
for q102pin, ph in (("2", "L1"), ("4", "L2"), ("6", "L3")):
    renvoi("10", ends10[q102pin], "12", (XL, BUS12[ph]), "L")

# ======================================================================== 13 DISTRIBUTION 230 V - ALIMENTATIONS
# bus L1 L2 L3 N depuis f12 ; -QF4 / -QF5 -> -T1 / -T2 (24 V, ancien f30 fondu ici le 29/10) ;
# -QF6 -> 48 V (f32) ; voyant -H2 ; sorties 24 V vers la distribution (f31)
f = "13"
nft = C + "Hager_NFT706_disjoncteur_1P+N_6A_C.xsy"
# QF7 / QF8 : Hager NFT702 (29/10) ; symbole copié du NFT706, dans la librairie du dépôt
nft702 = os.path.join(ICI, "librairie", "CUSTOM", "Hager_NFT702_disjoncteur_1P+N_2A_C.xsy")
for r_ in ("Q136", "Q137"):
    REP[r_].update({"fab": "Hager NFT702", "carac": "1P+N - 2 A courbe C - 6-10 kA - 1 module"})
BUS13 = {"L1": 2400, "L2": 3200, "L3": 4000, "N": 4800}
q132 = maitre(nft, "Q132", f, 4000, 5600)
q133 = maitre(nft, "Q133", f, 9600, 5600)
q134 = maitre(C + "Schneider_A9F75204_iC60N_2P_4A_D.xsy", "Q134", f, 15200, 5600)
REP["H2"] = {"des": "Voyant porte : armoire sous tension (230 V)", "fab": "À définir", "carac": "230 V CA - blanc",
            "loc": "+A1"}
h2 = maitre("Signalisation et voyants\\Voyant.xsy", "H2", f, 21600, 6800, fpos=(600, 400), wrap=22)   # 6400 -> 6800 (Julien, v26)
# piquages : 24 V sur L1, 48 V sur L2, voyant sur L3
for q, pin, ph in ((q132, ("N", 0), "N"), (q132, "1", "L1"), (q133, ("N", 0), "N"), (q133, "1", "L1"),
                   (q134, "1", "N"), (q134, "3", "L2")):
    W(f, [(q[pin].x, BUS13[ph]), q[pin]], "N" if ph == "N" else "L")
# H2 sur la porte : une borne de chaque côté (05/11)
bh2a, bh2b = borne("X721.9", f, 21600, 5200), borne("X721.10", f, 21600, 10000, fpos=(-700, -250))   # 8400 -> 10000 (Julien, v26)
W(f, [(21600, BUS13["L3"]), bh2a["1"]], "L")
W(f, [bh2a["2"], h2["X1"]], "L")
W(f, [h2["X2"], bh2b["1"]], "N")
W(f, [bh2b["2"], (21600, 11200), (20800, 11200), (20800, BUS13["N"])], "N")
fin13 = {"L1": q133["1"].x, "L2": q134["3"].x, "L3": XR, "N": XR}
for ph, y in BUS13.items():
    W(f, [(XL, y), (fin13[ph], y)], "N" if ph == "N" else "L")
    if ph == "N":
        renvoi("10", ends10[("N", 1)], f, (XL, y), "N")
    else:
        renvoi("12", (XR, BUS12[ph]), f, (XL, y), "L")
# alimentations 24 V sous leur disjoncteur, fils allongés (29/10)
alim = C + "RSPRO_284-0491_alim_24V_240W.xsy"
t301 = maitre(alim, "T301", f, 4000, 10400)
t302 = maitre(alim, "T302", f, 9600, 10400)
for T, q in ((t301, q132), (t302, q133)):
    W(f, [q[("N", 1)], T["N"]], "N")
    W(f, [q["2"], (q["2"].x, 9600), (T["L"].x, 9600), T["L"]], "L")
    PE_DEST.append((f, W(f, [T["PE"], (T["PE"].x, 12400)], "PE")))
# -T3 48 V sous -QF6 (déplacée du f32 le 02/11) : 4 départs vers les drivers (f32), un + et un - par driver
t321 = maitre(C + "MeanWell_NDR-240-48_alim_48V_240W.xsy", "T321", f, 15200, 10400)
W(f, [q134["2"], t321["N"]], "N")
W(f, [q134["4"], (q134["4"].x, 9600), (t321["L"].x, 9600), t321["L"]], "L")
PE_DEST.append((f, W(f, [t321["PE"], (t321["PE"].x, 12400)], "PE")))
# bornes de sortie de droite à gauche : +V (U4), +V (U3), -V (U4), -V (U3) ; chaque fil descend un cran plus bas
d48 = {}
for (pin, k), cle, y in ((("+V", 0), "+U4", 12400), (("+V", 1), "+U3", 13200), (("-V", 1), "-U4", 14000), (("-V", 0), "-U3", 14800)):
    d48[cle] = W(f, [t321[(pin, k)], (t321[(pin, k)].x, y), (XR, y)], "PDC")
    texte(f, 22400, y - 400, ("+48 V" if cle[0] == "+" else "0 V 48") + " -> -" + {"U3": "T322", "U4": "T323"}[cle[1:]], 220)
# sorties vers la distribution (f31) : 24VELEC (-T302), 24VSEC (-T301), 0 V commun (sous les départs 48 V)
s24 = W(f, [t302[("+V", 0)], (t302[("+V", 0)].x, 15600), (XR, 15600)], "24")
a24 = W(f, [t301[("+V", 0)], (t301[("+V", 0)].x, 16400), (XR, 16400)], "24")
z30 = W(f, [t301[("-V", 0)], (t301[("-V", 0)].x, 17200), (XR, 17200)], "0V")
W(f, [t302[("-V", 0)], (t302[("-V", 0)].x, 17200)], "0V")
texte(f, 22400, 15200, "24VELEC (-T302)", 220)
texte(f, 22400, 16000, "24VSEC (-T301)", 220)
texte(f, 22400, 16800, "0 V commun", 220)
# PELV : liaison unique 0 V - PE, par une borne sectionnable (mesure d'isolement)
b36 = borne("X36.1", f, 7200, 17600)
W(f, [(7200, 17200), b36["1"]], "0V")
PE_DEST.append((f, W(f, [b36["2"], (7200, 18400), (6400, 18400)], "PE")))

# ======================================================================== 14 DISTRIBUTION 230 V - SERVICES
f = "14"
BUS14 = {"L3": 2400, "N": 3200}
q137 = maitre(nft702, "Q137", f, 4400, 4400)
q136 = maitre(nft702, "Q136", f, 12000, 4400)
q131 = maitre(C + "IMO_B6CR1N1630A_disj_diff_1P+N_16A_30mA.xsy", "Q131", f, 20000, 4400)
for q in (q137, q136, q131):
    W(f, [(q[("N", 0)].x, BUS14["N"]), q[("N", 0)]], "N")
    W(f, [(q["1"].x, BUS14["L3"]), q["1"]], "L")
W(f, [(XL, BUS14["L3"]), (q131["1"].x, BUS14["L3"])], "L")
W(f, [(XL, BUS14["N"]), (q131[("N", 0)].x, BUS14["N"])], "N")
for ph in ("L3", "N"):
    renvoi("13", (XR, BUS13[ph]), f, (XL, BUS14[ph]), "N" if ph == "N" else "L")
# prise de service : -QF9 -> -QF10 -> -X14 dans l'axe, fils allongés (29/10)
# v35 (Julien 20/11) : QF10 en 2 A (A9P71602), symbole copié du 6 A, dans la librairie du dépôt
q135 = maitre(os.path.join(ICI, "librairie", "CUSTOM", "Schneider_A9P71602_iDT40K_disjoncteur_1PN_2A_C.xsy"), "Q135", f, 20000, 8800)
# v38 (Julien 24/11) : bas des 3 colonnes (éclairage, ventilation, prise) alignés à 15600
x131 = maitre(C + "Legrand_004280_prise_2P+T_16A.xsy", "X131", f, 20000, 13800)
W(f, [q131[("N", 1)], q135[("N", 0)]], "N")
W(f, [q131["2"], q135["1"]], "L")
W(f, [q135[("N", 1)], x131["N"]], "N")
W(f, [q135["2"], x131["L"]], "L")
PE_DEST.append((f, W(f, [x131["PE"], (x131["PE"].x, x131["PE"].y + 800)], "PE")))   # PE : renvoi court
# éclairage : lampes l'une sous l'autre, N à gauche, L à droite (pas de croisement)
lampe = C + "RSPRO_194-0417_eclairage_armoire_LED.xsy"
# 13/11 (Julien) : une borne L et une borne N par fonction (X13.11-12 éclairage, X13.21-22 ventilation), appareils
# descendus de 800 ; EL2 / EV2 toujours repiqués sur EL1 / EV1 comme avant
e131 = maitre(lampe, "E131", f, 4400, 9200, fpos=(2400, -300))
e132 = maitre(lampe, "E132", f, 4400, 15400, fpos=(2400, -300))
yt14 = q137["2"].y + 1200
bEL = borne("X141.1", f, e131["L"].x, yt14)
bEN = borne("X141.2", f, q137[("N", 1)].x, yt14, fpos=(-700, -250))
W(f, [q137[("N", 1)], bEN["1"]], "N")
W(f, [bEN["2"], e131["N"]], "N")
W(f, [e131["N"], e132["N"]], "N")
W(f, [q137["2"], (q137["2"].x, yt14 - 400), (bEL["1"].x, yt14 - 400), bEL["1"]], "L")
W(f, [bEL["2"], e131["L"]], "L")
W(f, [e131["L"], e132["L"]], "L")
# ventilateurs l'un sous l'autre : N contourne par la gauche, L par la droite (pas de croisement)
vent = C + "IDE_VF92AC_ventilateur_230V.xsy"
g131 = maitre(vent, "G131", f, 12000, 9600, fpos=(2000, 400))
g132 = maitre(vent, "G132", f, 12000, 14000, fpos=(2000, 400))
bVL = borne("X142.1", f, q136["2"].x, yt14)
bVN = borne("X142.2", f, q136[("N", 1)].x, yt14, fpos=(-700, -250))
W(f, [q136[("N", 1)], bVN["1"]], "N")
W(f, [bVN["2"], g131["N"]], "N")
W(f, [q136["2"], bVL["1"]], "L")
W(f, [bVL["2"], g131["L"]], "L")
W(f, [(12000, 9200), (11200, 9200), (11200, 13600), (12000, 13600), g132["N"]], "N")
W(f, [(12800, 8800), (13600, 8800), (13600, 13600), (12800, 13600), g132["L"]], "L")

# ======================================================================== 20 / 21 VARIATEURS
mcx = C + "SEW_Variateur_MCX91A-0055-5E3_CSO_CFN.xsy"
# bornes armoire -> machine (02/11), numéros provisoires de -X701 (repérage des borniers à valider par Julien)
BORNES_MOT = {"M201": [f"X701.{n}" for n in range(17, 25)], "M211": [f"X701.{n}" for n in range(25, 33)],
              "M321": [f"X701.{n}" for n in range(33, 37)], "M322": [f"X701.{n}" for n in range(37, 41)]}
mot = C + "SEW_K39-DRN100LS4-BE5-TF_motoreducteur_frein.xsy"
res = C + "SEW_BW100-001_resistance_freinage.xsy"
VAR = {}
VARIATEURS = []         # v40 : variateurs posés (alignement des numéros au-dessus des broches du haut)
for f, t, r, m, w1, w2, w3, km, qf in (("20", "T201", "R201", "M201", "W201", "W202", "W203", "KM1", "Q421"),
                                       ("21", "T211", "R211", "M211", "W211", "W212", "W213", "KM2", "Q422")):
    # variateur remonté, moteur dans l'axe de X2 (fils droits), câbles W sur une seule ligne (30/10)
    # v37 (revue Krizox) : variateur descendu de 400 (renvois X5 / X6 sur 2 niveaux, fils droits, D16) ;
    # bornier -X31 / -X32 remonté de 400, câbles W2 à W6 entre ce bornier et la boîte +BJM, fils de la boîte au moteur (D08)
    # v40 (Julien 25/11) : variateur remonté de 400 (place des numéros de fil, des bornes et de la résistance)
    T = maitre(mcx, t, f, 4000, 5200, wrap=34)
    VARIATEURS.append(T)
    # v38 : 1200 plus haut (place des fils TF / frein) ; v39 (Julien 24/11 : textes superposés aux broches X20 du variateur) :
    # textes à 1400 à droite, sous les broches, au-dessus du fil 2b (8800)
    # v40 (Julien 25/11 : « la résistance de freinage, toujours pas bon ») : résistance sous le variateur, entre +R et -R,
    # loin des broches X20 ; repère seul à droite (la désignation reste dans le symbole, nomenclature f90)
    # v42 (Julien 26/11, variateur élargi) : résistance sous la broche -R (fil -R droit et assez long pour son numéro)
    R = maitre(res, r, f, T["X2:-R"].x, 8800, shown=(), fpos=(150, 600))
    # symbole modifié par Julien le 02/11 : moteur, sonde TF, frein BE5 dans un même cadre, origine sur U1
    M = maitre(mot, m, f, 4800, 15200, fpos=(10800, 0), wrap=36, noms=False)   # textes à droite du symbole
    # v38 (retours v37) : bornier 10800, câbles 12400, boîte 13600, moteur 15600 : 1600 libres autour des câbles et des cadres
    YC = 12400                                                     # ligne des 3 câbles (bornier armoire -> boîte +BJM)
    # bornier armoire -> machine (02/11) : une borne par conducteur, sur une ligne, dans l'axe des broches du moteur
    BM = {p: borne(nb, f, M[p].x, 10800) for p, nb in zip(("PE", "U1", "V1", "W1", "1b", "2b", "2", "3"), BORNES_MOT[m])}
    CB = {"PE": (w1, "PE"), "U1": (w1, "U"), "V1": (w1, "V"), "W1": (w1, "W"), "1b": (w3, 1), "2b": (w3, 2),
          "2": ("W202", 1 if f == "20" else 3), "3": ("W202", 2 if f == "20" else 4)}
    BJ = {p: bjm(f, M[p].x, 13600, *CB[p]) for p in BM}
    for p in BM:
        t_ = "PE" if p == "PE" else ("L" if p in ("U1", "V1", "W1", "2", "3") else "PDC")   # TF : Autre tension DC (13/11)
        W(f, [BM[p]["2"], BJ[p]["1"]], t_)
        W(f, [BJ[p]["2"], M[p]], t_)
    for p, kp in (("X1:L1", "2/T1"), ("X1:L2", "4/T2"), ("X1:L3", "6/T3")):
        renvoi("12", out12[(km, kp)], f, stub(f, (T[p].x, 4400), T[p], "L"), "L")
    # terre (29/10) : PE moteur -> X2 PE du variateur ; X1 PE -> fil court + renvoi vers la terre (f10)
    PE_DEST.append((f, W(f, [T["X1:PE"], (4000, 4400)], "PE")))
    W(f, [T["X2:PE"], BM["PE"]["1"]], "PE")
    W(f, [T["X2:U"], BM["U1"]["1"]], "L")
    W(f, [T["X2:V"], BM["V1"]["1"]], "L")
    W(f, [T["X2:W"], BM["W1"]["1"]], "L")
    g.cable(F[f], 0, 0, YC, w1, "4G2,5 blindé", f"Moteur {m} -> {t} X2", [M[p].x for p in ("U1", "V1", "W1")], ovale=True,
            compo_dx=-2300, vj=[M["PE"].x])      # v37 : V/J sans numéro de brin ; compositions placées comme Julien (02/11)
    W(f, [T["X2:-R"], R["1"]], "PDC")                                                       # v42 : -R -> haut de R, droit
    W(f, [T["X2:+R"], (T["X2:+R"].x, R["2"].y + 200), (R["2"].x, R["2"].y + 200), R["2"]], "PDC")   # +R -> bas de R
    # frein et sonde TF par le bornier (02/11) ; frein : les 2 fils remontent avant de partir à droite ;
    # broche 2 au-dessus de la broche 3, renvois décalés en x (pas de recouvrement des flèches)
    renvoi("12", out12[(qf, "4/T2")], f, W(f, [BM["2"]["1"], (M["2"].x, 10000), (16800, 10000)], "L"), "L")
    renvoi("12", out12[(qf, "6/T3")], f, W(f, [BM["3"]["1"], (M["3"].x, 10400), (14400, 10400)], "L"), "L")
    # sonde TF : remonte à droite du variateur vers X10:3 (TF1) / X10:4 (GND) (doc SEW, Xavier 26/11 ;
    # X10:1 / X10:2 = sortie de commande de frein DB00, non utilisée ; avant la v44 : TF sur X10:1 / X10:2, faux)
    # v42 (Julien 26/11 : variateur élargi, pas de 600) : remontée de la sonde TF à droite des textes du variateur
    XTF = 23600
    W(f, [BM["1b"]["1"], (M["1b"].x, 9600), (XTF + 400, 9600), (XTF + 400, 4000), (T["X10:3"].x, 4000), T["X10:3"]], "PDC")
    W(f, [BM["2b"]["1"], (M["2b"].x, 8800), (XTF, 8800), (XTF, 4400), (T["X10:4"].x, 4400), T["X10:4"]], "PDC")
    VAR[(f, "PN")] = W(f, [T["X40"], (T["X40"].x, 4800), (T["X40"].x + 1600, 4800)], "PN")   # v42 : 1600 à droite de X40
    g.cable(F[f], 0, 0, YC, w3, "2x0,75 blindé", f"Sonde TF {m} (1b-2b) -> {t} X10", [M["1b"].x, M["2b"].x], ovale=True, compo_dx=-1600)
    # freins M1 + M2 : UN SEUL câble -W4 (W202) LIYCY-JZ 5G1,5 blindé (05/11, W7 supprimé) : conducteurs 1-2 au f31,
    # 3-4 au f32 ; V/J vers le bornier de terre -XPE1 et la boîte de dérivation côté machine
    g.cable(F[f], 0, 0, YC, "W202", "5G1,5 blindé", f"Freins M1 + M2 (2-3), 400 V CA -> {qf}", [M["2"].x, M["3"].x], ovale=True,
            compo_dx=-1700, nums=(1, 2) if f == "20" else (3, 4))
    # X6 confirmé par Julien (05/11, notice SEW) : X6.1 / X6.3 = F_STO_P (+24 V), X6.2 / X6.4 = F_STO_M (0 V),
    # X6.5 VO24_STO / X6.6 GND (alimentation interne, seulement si le réseau est présent) : non utilisés
    # STO en chaîne (Julien 06/11, validé SEW) : KA1 (AUTO-B) -> -U1 X6.1, 0 V -> -U1 X6.2 ;
    # -U1 X6.3 / X6.4 repartent vers -U2 X6.1 / X6.2 ; -U2 X6.3 / X6.4 libres (fin de chaîne)
    # v37 (D16) : chaque broche monte droit à son renvoi ; broches voisines à 400 -> 2 niveaux (pointe à 4600 : +24 V ;
    # pointe à 2900 : 0 V), flèches d'un niveau écartées de 1600 de l'autre niveau
    YA, YB_ = 4600, 2900          # v40 : niveaux inchangés (le variateur, 400 plus haut, raccourcit les fils de 400)
    VAR[(f, "24")] = W(f, [T["X5:24V"], (T["X5:24V"].x, YA)], "24")
    VAR[(f, "0V")] = W(f, [T["X5:GND"], (T["X5:GND"].x, YB_)], "0V")
    VAR[(f, "STO1")] = W(f, [T["X6:1"], (T["X6:1"].x, YA)], "24")
    if f == "20":
        VAR[(f, "STO0")] = W(f, [T["X6:2"], (T["X6:2"].x, YB_)], "0V")
        VAR[(f, "STOout+")] = W(f, [T["X6:3"], (T["X6:3"].x, YA)], "24")
        VAR[(f, "STOout0")] = W(f, [T["X6:4"], (T["X6:4"].x, YB_)], "0V")
    else:
        VAR[(f, "STOin0")] = W(f, [T["X6:2"], (T["X6:2"].x, YB_)], "0V")
        renvoi("20", VAR[("20", "STOout+")], f, VAR[(f, "STO1")], "24")
        renvoi("20", VAR[("20", "STOout0")], f, VAR[(f, "STOin0")], "0V")
    texte(f, XTF + 800, 4400, "X40 : PROFINET (f54)", 200)
    texte(f, XTF + 800, 4800, "X5 : 24VELEC (f31) - X6 : STO (f42)", 200)
    # v33 (Julien 18/11) : seulement l'essentiel ; TF X10, blindage et W4 : mémoire (05) et repères des câbles
    # v37 (D09) : moteur et bornes de la boîte dans des cadres pointillés (lieu)
    cadre_lieu(f, list(BJ.values()), "+BJM", marge=100, haut=0, droite=True)
    cadre_lieu(f, [M], "+M", marge=100, haut=0, gauche=True)

# ======================================================================== 31 DISTRIBUTION 24 V
# v37 : plus de barres en haut de ce folio ; les départs 24VELEC / 0 V vers les barres partent en renvoi vers le f30
f = "31"
# v37 (revue Krizox, D13 / D14, Julien 23/11) : folio refait. Les 4 blocs PTFIX 6/12 sur une ligne, même hauteur, même pas,
# dans l'ordre -X21.11 rouge (24VELEC), -X21.12 bleu (0 V), -X21.13 gris (24VSEC), -X21.14 noir (24 V capteurs).
# Entrée E et départs en haut (broches 2, 4, 6) : renvois vers le haut ; départs du bas (8, 10, 12) : renvois vers le bas.
# Une broche sur deux (pas 800) : renvois voisins écartés de 800. Plus de barres 24VELEC / 0 V en haut de ce folio
# (elles commencent au f30, alimentées par renvoi) ; plus d'images des blocs (Julien : seulement s'il reste la place).
ptf = os.path.join(ICI, "librairie", "CUSTOM", "Phoenix_3273354_PTFIX_6-12x2.5.xsy")
DESC31 = {"X311": ("Distribution 24VELEC", "rouge"), "X312": ("Distribution 0 V", "bleu"),
          "X313": ("Distribution 24VSEC", "gris"), "X314": ("Distribution 24 V capteurs (L+ capt CPU)", "noir")}
Y31 = 8400                                      # ligne des blocs (broches du haut)
X31B = {"X311": 4000, "X312": 10400, "X313": 16800, "X314": 23200}
P31 = {}
for rep_, x in X31B.items():
    P31[rep_] = g.place(ptf, rep_, F[f], x, Y31, champs={2: DESC31[rep_][0], 3: "Phoenix 3273354 PTFIX 6/12X2,5",
                                                     4: f"1 entrée + 12 départs - {DESC31[rep_][1]}"}, loc="A1", wrap=16,
                        ref=("PHOENIX CONTACT", "", "3273354"), fpos=(3200, -200), shown=(2, 4))
x311, x312, x313, x314 = P31["X311"], P31["X312"], P31["X313"], P31["X314"]
# v40 (Julien 25/11) : images des blocs remises, au-dessus des renvois du haut (hauteur 3200, centrées sur le bloc).
# Pas d'image du bloc noir -X21.14 (aucune image noire dans schema/images).
for rep_, (img_, ratio_) in (("X311", ("Phoenix_PTFIX_6-12x2.5_rouge.jpg", 1233)), ("X312", ("Phoenix_PTFIX_6-12x2.5.jpg", 999)),
                             ("X313", ("Phoenix_PTFIX_6-12x2.5_gris.jpg", 1166))):
    h_ = 3200
    w_ = h_ * ratio_ // 1000
    g.logos.append((F[f], X31B[rep_] + 1200 - w_ // 2, 2000, w_, h_, os.path.join(IMG, img_), ratio_))
YH, YB = Y31 - 1200, Y31 + 2000                 # bout des fils du haut / du bas (points de renvoi)


def dep31(blk, pin, t):
    """Départ (ou entrée E) d'un bloc jusqu'au point de renvoi, en haut ou en bas ; rend le point."""
    p = blk[pin]
    return W(f, [p, (p.x, YH if p.y == Y31 else YB)], t)


# entrées : renvois depuis le f12 (alimentations) et le f60 (L+ capt de la CPU)
renvoi("13", s24, f, dep31(x311, "E", "24"), "24")
renvoi("13", z30, f, dep31(x312, "E", "0V"), "0V")
renvoi("13", a24, f, dep31(x313, "E", "24"), "24")
d31 = {"LPC_E": dep31(x314, "E", "24"),
       "BAR24": dep31(x311, "2", "24"), "24V20": dep31(x311, "4", "24"), "24V21": dep31(x311, "6", "24"),
       "BAR0": dep31(x312, "2", "0V"), "0V20": dep31(x312, "4", "0V"), "0V21": dep31(x312, "6", "0V"),
       "0V32a": dep31(x312, "10", "0V"), "0V32b": dep31(x312, "12", "0V"),
       "CMD40": dep31(x313, "2", "24"), "CMD52": dep31(x313, "4", "24"),
       "LPC_S": dep31(x314, "2", "24")}
for ff in ("20", "21"):
    renvoi(f, d31["24V" + ff], ff, VAR[(ff, "24")], "24")
    renvoi(f, d31["0V" + ff], ff, VAR[(ff, "0V")], "0V")
# voyant de porte -H3 (24VELEC présent) sous le bloc 24VELEC : broche 12 -> -X21.21 -> -H3 -> -X21.22 -> broche 8 du 0 V
REP["P512"] = {"des": "Voyant porte : tension de commande présente", "fab": "À définir", "carac": "24 V CC - blanc ou vert", "loc": "+A1"}
xh3 = x311["12"].x
bh3a, bh3b = borne("X721.11", f, xh3, Y31 + 2400, fpos=(-900, -250)), borne("X721.12", f, xh3, Y31 + 6400, fpos=(-900, -250))
p512 = decrit("Signalisation et voyants\\Voyant.xsy", "P512", f, xh3, Y31 + 4000, "Voyant porte : 24VELEC présent",
              fpos=(600, 400), wrap=20, prefix="P", nomenc=True)
W(f, [x311["12"], bh3a["1"]], "24")
W(f, [bh3a["2"], p512["X1"]], "24")
W(f, [p512["X2"], bh3b["1"]], "0V")
W(f, [bh3b["2"], (xh3, Y31 + 7600), (x312["8"].x, Y31 + 7600), x312["8"]], "0V")

# ======================================================================== 32 48 V ET PAS-A-PAS
# 02/11 : -T3 sur f13 ; ici 2 arrivées +48 V et 2 arrivées 0 V 48 (un + et un - par driver), sans bornier.
# Les 2 +48 V passent chacun par un pôle de -KA2 (1-2 -> -U3, 3-4 -> -U4) ; 0 V 48 non coupé.
f = "32"
REP["Q423"]["des"] = "Contacteur auxiliaire : coupure du +48 V des drivers"
# v37 (revue Krizox, D06) : pôle 5-6 inutilisé plus dessiné (symbole 2 pôles copié du 3 pôles ; l'appareil reste un LC1D09BD 3P)
# v42 (Julien 26/11 : « recentre le texte de KA2 par rapport au symbole ») : bloc de texte centré sur la hauteur du
# contact (entre ses broches), 600 à droite du symbole
q423p = contacteur(os.path.join(ICI, "librairie", "CUSTOM", "Schneider_LC1D09BD_contacts_puissance_2P.xsy"), "Q423", f, 5200, 5600,
                   fpos=(1500, -100))
A48 = {"-U4": W(f, [(XL, 2800), (24000, 2800)], "PDC"),
       "+U4": W(f, [(XL, 3600), (q423p["3/L2"].x, 3600), q423p["3/L2"]], "PDC"),
       "+U3": W(f, [(XL, 4400), (q423p["1/L1"].x, 4400), q423p["1/L1"]], "PDC")}
for cle in ("-U4", "+U4", "+U3"):
    renvoi("13", d48[cle], f, (XL, {"-U4": 2800, "+U4": 3600, "+U3": 4400}[cle]), "PDC")
drv = C + "Jkongmotor_JKDM860H_driver_pas-a-pas.xsy"
mpp = C + "StepperOnline_34IP65-85_moteur_pas-a-pas.xsy"
CMD32, DRV = {}, {}
F20_RANGS = []          # v40 : (driver, bornes armoire, bornes +BJM, moteur, câble) pour aligner les numéros de fil
for T, Mrep, x0 in (("T322", "M321", 12000), ("T323", "M322", 23200)):
    # drivers remontés de 1600 le 02/11 : place pour les fils driver -> bornier et pour le câble blindé bornier -> moteur
    # v37 (revue Krizox, D08) : drivers remontés de 800 ; bornier -X20, câble W9 / W10, bornes de la boîte +BJM, fils au moteur
    D = maitre(drv, T, f, x0, 9200, fpos=(2600, 0), wrap=22, noms=False)
    # v38 (Julien 24/11) : moteur 400 plus bas, textes à droite centrés sur le cercle du symbole (centre à 1250 sous les broches)
    # v42 (Julien 26/11 : numéros, points rouges et noms des broches du moteur superposés) : bornes de la boîte sur 2 niveaux
    # à 400 (15800 / 16200, au lieu de 600 : leurs repères sont de part et d'autre, sans conflit) ; le cadre
    # +M englobe les broches et leurs couleurs (BK, GN...) ; numéros entre les cadres +BJM et +M
    Mo = maitre(mpp, Mrep, f, x0 - 800, 17600, noms=False, fpos=(2000, 800))
    DRV[T] = D
    # moteurs hors armoire (02/11) : bornier entre driver et moteur ; broches à 400 -> bornes sur 2 niveaux
    BJ20, BA20 = [], []
    for k_, (p, nb) in enumerate(zip(("A+", "A-", "B+", "B-"), BORNES_MOT[Mrep])):
        haut = p.endswith("+")
        # 02/11 : bornes à 800 sous le driver ; v37 : bornes armoire sur 2 niveaux (12800 / 13600), câble à 14400,
        # bornes de la boîte sur 2 niveaux (15200 / 16000), repère à côté du corps de la borne (gauche / droite)
        # v38 : niveaux à 600 (12800 / 13400 et 15600 / 16200), câble à 15000 : place des numéros autour du câble
        b = borne(nb, f, D[p].x, 12800 if haut else 13400, fpos=(-500, 125) if haut else (150, 125))
        # v40 (Julien 25/11 : cadres à égale distance) : boîte 200 plus bas, câble 200 plus haut (écart câble / cadre +BJM)
        bj = bjm(f, D[p].x, 15800 if haut else 16200, {"M321": "W321", "M322": "W322"}[Mrep], k_ + 1,
                 fpos=(-500, 125) if haut else (150, 125))
        BJ20.append(bj)
        BA20.append(b)
        W(f, [D[p], b["1"]], "PDC")
        W(f, [b["2"], bj["1"]], "PDC")
        W(f, [bj["2"], Mo[p]], "PDC")
    # un câble blindé par moteur, du bornier au moteur (Julien 02/11) ; section à définir
    # v34 (Julien 18/11) : V/J du 5G1,5 sur une borne de terre côté armoire, non raccordé au moteur pas-à-pas
    xpe = max(D[p].x for p in ("A+", "A-", "B+", "B-")) + 800
    bpe = borne({"M321": "X701.47", "M322": "X701.48"}[Mrep], f, xpe, 12800, fpos=(150, 125))
    PE_DEST.append((f, W(f, [bpe["1"], (xpe, 12400), (xpe + 1200, 12400)], "PE")))   # renvoi vers la droite (sous le driver)
    # v38 (Julien 24/11) : le V/J s'arrête sous le câble (plus de fil jusqu'en bas du folio)
    W(f, [bpe["2"], (xpe, 15200)], "PE")
    texte(f, xpe + (400 if Mrep == "M321" else 500), 14900, "V/J non raccordé", 180)   # v43 : place de Julien
    g.cable(F[f], 0, 0, 15000, {"M321": "W321", "M322": "W322"}[Mrep], "5G1,5 blindé",
            f"Moteur pas-à-pas {Mrep} -> {T}", [Mo[p].x for p in ("A+", "A-", "B+", "B-")], ovale=True, compo_dx=-2800,
            compo_dy=-100, vj=[xpe], ellipse=(0, 200, 0, 200))   # 26/11 : pas de n° sur le V/J (Julien)
    # v43 : retouches de Julien sur la v42 (WinRelais) reprises : câble 200 plus bas, composition à gauche de l'ovale,
    # ellipse « 0 200 0 200 », brin n° 4 écrit aussi sur le V/J
    xin, xbus = x0 - 4000, x0 - 3200
    for s in ("PUL", "DIR", "ENA"):
        CMD32[(T, s)] = W(f, [D[s + "+"], (xin, D[s + "+"].y)], "24")
        W(f, [D[s + "-"], (xbus, D[s + "-"].y)], "0V")
    # v40 (Julien 25/11) : renvoi du 0 V (1230) horizontal, aligné sous les renvois PUL / DIR / ENA (pas de 800)
    # v42 (Julien 26/11 : renvois 21-F5 vers les PUL- / DIR- / ENA- un peu plus bas, plus clair) : 400 -> 800 sous ENA-
    CMD32[(T, "0V")] = W(f, [(xbus, D["PUL-"].y), (xbus, D["ENA-"].y + 800), (xin, D["ENA-"].y + 800)], "0V")
    # v40 (Julien 25/11 : égaliser les cadres) : même marge (200), bords gauche et droit alignés (+BJM / +M)
    yp_ = Mo["A+"].y
    eb, em = emprise(BJ20), emprise([Mo, (Mo["A+"].x, yp_, Mo["B-"].x + 400, yp_)])
    xg_, xd_ = min(eb[0], em[0]), max(eb[2], em[2])
    cadre_lieu(f, BJ20 + [(xg_, eb[1], xd_, eb[1])], "+BJM", marge=200, haut=0, gauche=True)          # v37 (D09)
    cadre_lieu(f, [Mo, (xg_, em[1], xd_, em[1])], "+M", marge=200, haut=0, gauche=True)
    F20_RANGS.append((D, BA20, BJ20, Mo, len(g.cables) - 1))
renvoi("31", d31["0V32a"], f, CMD32[("T322", "0V")], "0V")
renvoi("31", d31["0V32b"], f, CMD32[("T323", "0V")], "0V")
# un fil par driver : les fils de -U4 passent au-dessus de ceux de -U3 (un seul croisement, 0 V 48 de -U3)
W(f, [q423p["4/T2"], (q423p["4/T2"].x, 8000), (DRV["T323"]["+V"].x, 8000), DRV["T323"]["+V"]], "PDC")
W(f, [q423p["2/T1"], (q423p["2/T1"].x, 8400), (DRV["T322"]["+V"].x, 8400), DRV["T322"]["+V"]], "PDC")
W(f, [(24000, 2800), DRV["T323"]["-V"]], "PDC")
renvoi("13", d48["-U3"], f, (XL, 8800), "PDC")
W(f, [(XL, 8800), (DRV["T322"]["-V"].x, 8800), DRV["T322"]["-V"]], "PDC")

# ======================================================================== 40 RELAIS DE SECURITE
f = "40"
# v42 : noms de broches masqués (déjà écrits en jaune dans le symbole : Z1, 14... apparaissaient deux fois)
k401 = maitre(C + "Schneider_XPSUAF13AP_relais_securite.xsy", "K401", f, 4400, 8000, noms=False)
# A1 / A2 : raccordés aux barres du haut après le décalage du folio (voir « barres 24 V / 0 V »)
for p in ("13", "23", "33"):
    W(f, [k401[p], (k401[p].x, 3600)], "24")
# fusible R-33 (03/11) : Mersen CMC101 + FR10GG50V4 gG 4 A ; le 24VSEC arrive par le bas (renvoi), remonte par FA1
REP["F401"] = {"des": "Protection des contacts de sécurité KA1 (R-33)", "fab": "Mersen CMC101 + FR10GG50V4",
               "carac": "gG 4 A 10x38", "loc": "+A1"}
W(f, [(k401["13"].x, 3600), (k401["33"].x + 1200, 3600)], "24")
f401 = maitre("Fusibles\\Fusible 1Ph.xsy", "F401", f, k401["33"].x + 1200, 4000, ref=("MERSEN", "", "CMC101"), prefix="F",
              fpos=(400, 400), wrap=22)
W(f, [(k401["33"].x + 1200, 3600), f401["1"]], "24")
CMD40 = W(f, [f401["2"], (f401["2"].x, f401["2"].y + 800)], "24")
texte(f, f401["2"].x + 400, f401["2"].y + 1200, "24VSEC (f31)", 200)
S40 = {p: W(f, [k401[p], (k401[p].x, 4800)], "24") for p in ("S11", "S12", "S21", "S22")}
# v42 (Julien 26/11 : renvois du bas de KA1 un peu plus bas, il y a la place) : 11200 -> 12000
O40 = {p: W(f, [k401[p], (k401[p].x, 12000)], "24") for p in ("14", "24", "34")}
miroir = C + "Schneider_LC1D09BD_contact_aux_NC_21-22_miroir.xsy"
prev = W(f, [k401["Y1"], (8400, 3200), (20000, 3200)], "24")
DESC_KM = {"KM1": "contacteur amont variateur 1", "KM2": "contacteur amont variateur 2",
           "Q421": "contacteur frein M1", "Q422": "contacteur frein M2", "Q423": "contacteur auxiliaire 48 V"}
# v42 (Julien 26/11 : « texte à droite du symbole contact ; déplacer proprement le texte jaune ») : textes à droite du
# contact ; « contact miroir » passe à gauche du contact ; retour vers Y2 décalé à droite (XRET40) pour laisser la place.
# v43 (Julien 26/11 : « accrochés à gauche, je me suis trompé ») : textes accrochés à gauche, début à XTX40
XTX40, XRET40 = 20800, 24400
for i, rep in enumerate(DESC_KM):
    c = decrit(miroir, rep, f, 20000, 3200 + 2400 * i, f"Retour {DESC_KM[rep]}",
               prefix="KM" if rep.startswith("KM") else "Q", wrap=24, fpos=(XTX40 - 20000, 400), align=0)
    sec_ = None
    for k_, l_ in enumerate(c.block):
        if l_.startswith("¤#"):
            sec_ = l_
        elif sec_ == "¤#MDessin¤" and "contact miroir" in l_:
            f_ = l_.split("·")
            f_[1] = str(c["21"].x - 1300)
            c.block[k_] = "·".join(f_)
    if i:
        W(f, [prev, c["21"]], "24")
    prev = c["22"]
REP["S414"].update({"des": "Bouton de réarmement", "fab": "Schneider XB4BA21", "carac": "1 NO - noir - non lumineux"})   # 03/11
s414 = maitre("BP & Commut & Voyants\\BP Affleurant Noir.xsy", "S414", f, 20000, 16400, prefix="S", fpos=(-2000, 0), wrap=16,
              ref=("SCHNEIDER ELECTRIC", "", "XB4BA21"))
# S4 sur la porte : une borne avant, une sur le retour (05/11)
# v38 (Julien 24/11 : numéros peu visibles) : fils de -X40.11 allongés à 800
bs4a, bs4b = borne("X721.7", f, 20000, 15200), borne("X721.8", f, XRET40, 17200)
W(f, [prev, bs4a["1"]], "24")
W(f, [bs4a["2"], s414["3"]], "24")
# retour vers Y2 par la droite de la chaîne, au-dessus de Y1 (un seul croisement, avec Y1)
W(f, [s414["4"], (20000, 18400), (XRET40, 18400), bs4b["2"]], "24")
W(f, [bs4b["1"], (XRET40, 2800), (9200, 2800), k401["Y2"]], "24")
# Z1 (diagnostic, non sécuritaire) -> I1.5 de l'automate (Julien 02/11)
Z1_40 = W(f, [k401["Z1"], (k401["Z1"].x, k401["Z1"].y + 1600)], "24")     # v42 : 800 -> 1600 (renvois du bas plus bas)
renvoi("31", d31["CMD40"], f, CMD40, "24")

# ======================================================================== 41 SECURITE - ENTREES
f = "41"
au = "BP & Commut & Voyants\\Arret urgence NC déverr tournant.xsy"
nc2 = "--- X Contact\\RC Contact NC 21-22.xsy"
# -S413 (Eaton T0-4-8223/E) : 8 contacts NO, ponts d'usine 2-4, 6-8, 10-12, 14-16 retirés par Julien (05/11).
# Vraie numérotation (fiche Eaton) : position 1 Auto ferme 1-2, 5-6, 9-10, 13-14 ; position 2 Manu ferme 3-4, 7-8...
# Noms (Julien 05/11), lettre = bloc : AUTO-A 1-2 -KM1/-KM2, MANU-A 3-4 shunt capot voie 1, AUTO-B 5-6 STO,
# MANU-B 7-8 shunt capot voie 2, AUTO-C 9-10 info Auto (I0.4), MANU-C 11-12 info Manu (I0.5),
# AUTO-D 13-14 réserve, MANU-D 15-16 48 V (-KA2)
CT = {n: os.path.join(ICI, "librairie", "CUSTOM", f"Eaton_T0_contact_NO_{n}-{n + 1}.xsy") for n in (1, 3, 5, 7, 9, 11, 13, 15)}
# v37 (revue Krizox, D08 / D12) : avec la boîte +BJM, le folio est coupé en deux : f41 = arrêts d'urgence -S1 / -S2
# (voies 1 et 2), f43 (nouveau) = capots -B1 / -B2, shunts Manu de -S3, contacts NO des capots vers l'automate.
# Bornes des capots et des shunts renommées X43 (règle X + n° du folio de la borne, Julien 02/11).
VOIES = {}
S41 = {}
for voie, x, s1, s2, bornes, src, ret, porte, conds in (
        (1, 7200, "S411", "S412", ("X711.1", "X711.2"), "S11", "S12", ("X721.1", "X721.2"), (1, 2)),
        (2, 17200, "S411", "S412", ("X711.3", "X711.4"), "S21", "S22", ("X721.3", "X721.4"), (3, 4))):
    # AU armoire -S1 sur la porte (02/11) : une borne avant et une après son contact (pas par la boîte)
    da = borne(porte[0], f, x, 4400)
    top = stub(f, (x, 3600), da["1"], "24")   # 16/11 : 4000 -> 3600 (place du numéro)
    if voie == 1:
        c1 = maitre(au, s1, f, x, 5600, prefix="S", ref=("SCHNEIDER ELECTRIC", "", "XB5AS8442 + ZBE102 + ZBE101"))   # AU : réf. du 03/11
        c2 = maitre(au, s2, f, x, 13200, prefix="S", ref=("SCHNEIDER ELECTRIC", "", "XB5AS8442 + ZBE102 + ZBE101"))
        p1, p2 = ("1", "2"), ("1", "2")
    else:
        c1 = decrit(nc2, s1, f, x, 5600, "AU armoire - 2e contact NF (voie 2)")
        c2 = decrit(nc2, s2, f, x, 13200, "AU pupitre (+P1) - 2e contact NF (voie 2)")
        p1, p2 = ("21", "22"), ("21", "22")
    db = borne(porte[1], f, x, 8000)
    # v38 (retours v37) : 1600 libres autour des câbles et des cadres : câbles à 10800 / 17200, boîte 11600 / 16000
    b1, b2 = borne(bornes[0], f, x, 9200), borne(bornes[1], f, x, 18400)
    ja, jb = bjm(f, x, 11600, "W11", conds[0]), bjm(f, x, 16000, "W11", conds[1])
    for a_, b_ in ((da["2"], c1[p1[0]]), (c1[p1[1]], db["1"]), (db["2"], b1["1"]), (b1["2"], ja["1"]),
                   (ja["2"], c2[p2[0]]), (c2[p2[1]], jb["1"]), (jb["2"], b2["1"])):
        W(f, [a_, b_], "24")
    S41[voie] = (c2, ja, jb, W(f, [b2["2"], (x, 19200), (x + 1200, 19200)], "24"))     # vers les capots (f43) ; v38 : renvoi à droite
    renvoi("40", S40[src], f, top, "24")
xs41 = [7200, 17200]
# v39 (Julien 24/11) : chaque colonne à part : un W11 et un cadre +BJM par colonne (4 au lieu de 2)
for x_, (na, nb) in zip(xs41, ((1, 2), (3, 4))):
    g.cable(F[f], 0, 0, 10800, "W11", "27G1 blindé", "Pupitre", [x_], ovale=True, compo_dx=-2400, nums=(na,))
    g.cable(F[f], 0, 0, 17200, "W11", "27G1 blindé", "Pupitre", [x_], ovale=True, compo_dx=-2400, nums=(nb,))
for v in (1, 2):
    cadre_lieu(f, [S41[v][1]], "+BJM", marge=100, haut=0, gauche=True)
    cadre_lieu(f, [S41[v][2]], "+BJM", marge=100, haut=0, gauche=True)
cadre_lieu(f, [S41[v][0] for v in (1, 2)], "+P1", marge=200, haut=0, gauche=True)

# ======================================================================== 43 SECURITE - CAPOTS (v37)
# Par voie : arrivée de l'AU (f41) -> borne -X43.2x / -X43.3x -> câble W12 (B1) ou W14 (B2, M12) -> +BJM -> capot ->
# +BJM -> câble -> borne -> retour vers -KA1 S12 / S22 (f40) ; shunt Manu -S3 en parallèle par W11 et +BJM (à gauche) ;
# contact NO du capot vers l'automate (à droite, même câble).
f = "43"
F43 = {}
for voie, x, cap, capxsy, bornes, ret, byp, cab, cab_compo in (
        (1, 10400, "B411", C + "RSPRO_902-6874_interrupteur_position.xsy",
         ("X701.1", "X701.2", "X701.3", "X701.4"), "S12", (3, ("X711.13", "X711.14"), (7, 8)), "W12", "19G1 blindé"),
        (2, 22000, "B412", C + "ifm_MN508S_capteur_magnetique_code.xsy",
         ("X701.5", "X701.6", "X701.7", "X701.8"), "S22", (7, ("X711.15", "X711.16"), (9, 10)), "W14", "M12 8 cond.")):
    arr = W(f, [(x, 3200), (x, 3600)], "24")
    renvoi("41", S41[voie][3], f, (x, 3200), "24")
    ta, tb, te, tf = bornes
    # v38 (retours v37) : 1600 libres autour des câbles et des cadres : bornes 4400 / 13600, câbles 6000 / 12400,
    # boîte 6800 / 11200, capot et shunt 8400
    YB4, YJ3, YJ4, YCP, YK1, YK2, YRET = 13600, 6800, 11200, 8400, 6000, 12400, 14800
    b3, b4 = borne(ta, f, x, 4400), borne(tb, f, x, YB4)
    j3, j4 = bjm(f, x, YJ3, cab, 1), bjm(f, x, YJ4, cab, 2)
    cp = maitre(capxsy, cap, f, x, YCP)
    for a_, b_ in ((b3["2"], j3["1"]), (j3["2"], cp["11"]), (cp["12"], j4["1"]), (j4["2"], b4["1"])):
        W(f, [a_, b_], "24")
    W(f, [(x, 3600), b3["1"]], "24")
    W(f, [b4["2"], (x, YRET), (x, YRET + 800)], "24")
    renvoi("40", S40[ret], f, (x, YRET + 800), "24")
    # pontage du capot par -S413 position Manu (contact NO en parallèle de la chaîne bornes / capot)
    n_c, (bya, byb), (ca, cb) = byp
    xb = x - 3200
    ba, bb = borne(bya, f, xb, 4400), borne(byb, f, xb, YB4)
    jba, jbb = bjm(f, xb, YJ3, "W11", ca), bjm(f, xb, YJ4, "W11", cb)
    ctc = decrit(CT[n_c], "S413", f, xb, YCP, f"MANU-{'AB'[voie - 1]} : shunt capot voie {voie}", wrap=12)
    W(f, [(x, 3600), (xb, 3600), ba["1"]], "24")
    for a_, b_ in ((ba["2"], jba["1"]), (jba["2"], ctc[str(n_c)]), (ctc[str(n_c + 1)], jbb["1"]), (jbb["2"], bb["1"])):
        W(f, [a_, b_], "24")
    W(f, [bb["2"], (xb, YRET), (x, YRET)], "24")
    # contact NO du capot -> automate (f60)
    t1, t2 = borne(te, f, x + 800, 4400), borne(tf, f, x + 800, YB4)
    j5, j6 = bjm(f, x + 800, YJ3, cab, 3), bjm(f, x + 800, YJ4, cab, 4)
    plus = W(f, [t1["1"], (x + 800, 4000), (x + 2800, 4000)], "24")
    for a_, b_ in ((t1["2"], j5["1"]), (j5["2"], cp["23"]), (cp["24"], j6["1"]), (j6["2"], t2["1"])):
        W(f, [a_, b_], "24")
    entree = W(f, [t2["2"], (x + 800, YRET), (x + 2800, YRET)], "24")
    VOIES[cap] = (plus, entree)
    g.cable(F[f], 0, 0, YK1, cab, cab_compo, "", [x, x + 800], ovale=True, compo_dx=-2000, nums=(1, 3))
    g.cable(F[f], 0, 0, YK2, cab, cab_compo, "", [x, x + 800], ovale=True, compo_dx=-2000, nums=(2, 4))
    g.cable(F[f], 0, 0, YK1, "W11", "27G1 blindé", "", [xb], ovale=True, compo_dx=-2200, nums=(ca,))
    g.cable(F[f], 0, 0, YK2, "W11", "27G1 blindé", "", [xb], ovale=True, compo_dx=-2200, nums=(cb,))
    cadre_lieu(f, [j3, j5], "+BJM", marge=100, haut=0, droite=True)
    cadre_lieu(f, [j4, j6], "+BJM", marge=100, haut=0, droite=True)
    cadre_lieu(f, [jba], "+BJM", marge=100, haut=0, droite=True)
    cadre_lieu(f, [jbb], "+BJM", marge=100, haut=0, droite=True)
    cadre_lieu(f, [cp], "+M", marge=200, haut=0, droite=True)
    # v40 (Julien 25/11) : texte +P1 hors du cadre, à gauche ; le cadre englobe les broches du contact (bords à 200)
    yp_ = [xy[1] for lst in ctc.pins.values() for xy in lst]
    cadre_lieu(f, [ctc, (ctc.bbox[0], min(yp_), ctc.bbox[2], max(yp_))], "+P1", marge=200, haut=0, gauche=True)
# -S414 (réarmement) déplacé au f40 (Julien 02/11) ; tête du sélecteur : avec les shunts (v37)
tete = maitre("Poussoirs et commutateurs\\Tête 2 pos fixes NO.xsy", "S413", f, 5600, 16800, prefix="S", fpos=(600, 0),
              ref=("EATON", "", "T0-4-8223/E"))
cadre_lieu(f, [tete], "+P1", marge=200, haut=0, droite=True)


# ======================================================================== 42 SECURITE - SORTIES
# Architecture du 27/10 (fiche de Julien) :
#   sortie 1 (13-14) -> bobines freins -Q421 / -Q422, et via Manu-D -> bobine -Q423 (48 V en Manu seulement)
#   sortie 2 (23-24) -> Auto-A -> bobines -KM1 / -KM2 (pas d'ordre automate, option A du 27/10)
#   sortie 3 (33-34) -> Auto-B -> STO de -U1, puis -U2 en chaîne par X6.3 / X6.4 de -U1 (06/11)
f = "42"
bob = C + "Schneider_LC1D09BD_contacteur_bobine.xsy"
YC = 16000                                  # ligne des bobines (v37 : 12800 -> 14400 ; v38 : 16000, chaînes aérées)
Y42 = 5600                                  # haut des 3 chaînes (v37 : même hauteur pour les 3)
BJ42 = []
P42 = []


def chaine_s413(x, ba, bb, n_c, des, conds, y0=Y42):
    """Borne -X42 / câble W11 / borne +BJM / contact -S3 (pupitre) / borne +BJM / câble W11 / borne -X42, de haut en bas
    (v37, revue Krizox D08 / D12) ; rend (borne d'entrée, borne de sortie)."""
    t1 = borne(ba, f, x, y0)
    # v38 (retours v37) : 1600 libres autour des câbles (y0 + 1600, y0 + 8000) et des cadres de la boîte
    ja = bjm(f, x, y0 + 2400, "W11", conds[0])
    c = decrit(CT[n_c], "S413", f, x, y0 + 4000, des, wrap=18, fpos=(200, 400))   # v42 : 200 plus haut (nom de la broche du bas)
    jb = bjm(f, x, y0 + 6800, "W11", conds[1])
    t2 = borne(bb, f, x, y0 + 9200)
    W(f, [t1["2"], ja["1"]], "24")
    W(f, [ja["2"], c[str(n_c)]], "24")
    W(f, [c[str(n_c + 1)], jb["1"]], "24")
    W(f, [jb["2"], t2["1"]], "24")
    BJ42.append((ja, jb))
    P42.append(c)
    return t1, t2


COIL = {}
for rep, x, pref in (("Q421", 4400, "Q"), ("Q422", 7600, "Q"), ("Q423", 11200, "Q"),
                     ("KM1", 15200, "KM"), ("KM2", 18400, "KM")):
    k = maitre(bob, rep, f, x, YC, ref=("SCHNEIDER ELECTRIC", "", "LC1D09BD"), prefix=pref, wrap=16)
    COIL[rep] = k            # A2 : collecteur 0 V tracé après le décalage du folio
# --- sortie 1 : freins (toujours, seul l'AU les coupe) et 48 V (Manu-D)
s1 = (4400, 4400)          # v40 : 4000 -> 4400 (folio descendu de 400 seulement)
W(f, [s1, COIL["Q421"]["A1"]], "24")
W(f, [(4400, 4800), (11200, 4800)], "24")
W(f, [(7600, 4800), COIL["Q422"]["A1"]], "24")
t1, t2 = chaine_s413(11200, "X711.19", "X711.20", 15, "MANU-D : 48 V en Manu seulement", (11, 12))
W(f, [(11200, 4800), t1["1"]], "24")
W(f, [t2["2"], COIL["Q423"]["A1"]], "24")
renvoi("40", O40["14"], f, s1, "24")
texte(f, 4800, 3400, "Sortie 1 (13-14) : freins + 48 V", 220, 0, 1)
# --- sortie 2 : Auto-A -> -KM1 / -KM2 (pas d'ordre automate, décision du 27/10, option A)
t1, t2 = chaine_s413(15200, "X711.7", "X711.8", 1, "AUTO-A : commande -KM1 / -KM2", (13, 14))
s2 = stub(f, (15200, 4400), t1["1"], "24")   # 16/11 : 4000 -> 3600 (place du numéro) ; v40 : 4400 (folio moins descendu)
W(f, [t2["2"], COIL["KM1"]["A1"]], "24")
W(f, [(15200, YC - 400), (18400, YC - 400), COIL["KM2"]["A1"]], "24")
renvoi("40", O40["24"], f, s2, "24")
texte(f, 15600, 3400, "Sortie 2 (23-24) : -KM1 / -KM2", 220, 0, 1)
# --- sortie 3 : Auto-B -> STO des 2 variateurs (validé SEW)
t1, t2 = chaine_s413(21600, "X711.9", "X711.10", 5, "AUTO-B : autorisation STO", (15, 16))
s3 = stub(f, (21600, 4400), t1["1"], "24")   # 16/11 : idem ; v40 : 4400
YSTO = t2["2"].y + 800
W(f, [t2["2"], (21600, YSTO)], "24")
renvoi("40", O40["34"], f, s3, "24")
renvoi(f, (21600, YSTO), "20", VAR[("20", "STO1")], "24")
texte(f, 22000, 3400, "Sortie 3 (33-34) : STO", 220, 0, 1)
texte(f, 22000, YSTO + 600, "STO : -U1 X6.1 / X6.2, puis -U2", 200)
texte(f, 22000, YSTO + 900, "en chaîne par -U1 X6.3 / X6.4 (validé SEW)", 200)
# câble W11 (pupitre) : une ligne au-dessus des bornes de la boîte, une en dessous (n° des conducteurs : 02_MATERIEL)
xs42 = [ja["1"].x for ja, _ in BJ42]
# v39 (Julien 24/11) : chaque colonne à part : un W11 et un cadre +BJM par colonne
for x_, (na, nb), (ja, jb) in zip(xs42, ((11, 12), (13, 14), (15, 16)), BJ42):
    g.cable(F[f], 0, 0, Y42 + 1600, "W11", "27G1 blindé", "Pupitre", [x_], ovale=True, compo_dx=-2400, nums=(na,))
    g.cable(F[f], 0, 0, Y42 + 8000, "W11", "27G1 blindé", "Pupitre", [x_], ovale=True, compo_dx=-2400, nums=(nb,))
    cadre_lieu(f, [ja], "+BJM", marge=100, haut=0, gauche=True)
    cadre_lieu(f, [jb], "+BJM", marge=100, haut=0, gauche=True)
# v40 (Julien 25/11 : les pointillés +P1 traversaient les points de connexion) : un cadre +P1 par contact (comme +BJM),
# qui englobe les broches du contact (bords à 200 des broches, sur les fils)
for c_ in P42:
    yp_ = [xy[1] for lst in c_.pins.values() for xy in lst]
    cadre_lieu(f, [c_, (c_.bbox[0], min(yp_), c_.bbox[2], max(yp_))], "+P1", marge=200, haut=0, gauche=True)
# 0 V des STO (X6:2 / X6:4) : piqués sur la barre 0 V du haut, après le décalage du folio

# ======================================================================== 50 AUTOMATE ENTREES
f = "50"
# v37 (revue Krizox, D08 / D12 / D19 / D20) : appareils du pupitre et de la machine par la boîte +BJM et les câbles W11 / W12 ;
# chaîne d'une entrée, de haut en bas : borne -X60 / câble / borne +BJM / contact / borne +BJM / câble / borne -X60 / entrée.
# CPU descendue de 2000 ; ligne 24 V capteurs du haut alimentée par un renvoi horizontal à gauche ; tableau à droite.
# v38 (Julien 24/11) : alimentation et PROFINET de la CPU au f60 (interne 55), entrées seules ici (f61) : symbole coupé en deux
Y60 = 3600                                   # rangée des bornes -X61 du haut
CPU_Y = 16400
# v39 (Julien 24/11) : symbole des entrées refait plus large (pas de 1600 entre entrées, 800 avant)
k501e = maitre(C + "Siemens_6ES7214-1AH50-0XB0_CPU1214C_G2_entrees.xsy", "K501", f, 3600, CPU_Y, ref=(), compact=True,
               rep_size=300)
# 1M : raccordé à la barre 0 V du haut après le décalage du folio
W(f, [(XL, 3200), (26800, 3200)], "24")          # départs de -X21.14 : un fil par point (ligne du haut)
renvoi("31", d31["LPC_S"], f, (XL, 3200), "24")
texte(f, 10000, 2600, "24 V capteurs : départs du bloc -X314 (noir, f31), un fil par point ; -KM1 13 et -KM2 13 pontés", 180)
W(f, [(25600, 3200), (25600, 4000), (26800, 4000)], "24")
renvoi(f, (26800, 3200), "43", VOIES["B411"][0], "24")
renvoi(f, (26800, 4000), "43", VOIES["B412"][0], "24")
# 18/11 (Julien) : fins de course en NF (mieux pour le programme : fil coupé = fin de course vue) ; contact NF 11-12
# du RS 902-6874 (mêmes bornes que -B411) ; symbole : copie de « Fin de course NC » de la librairie, broches 11 / 12
fdc = os.path.join(ICI, "librairie", "CUSTOM", "Fin_de_course_NF_11-12.xsy")
nom = "--- X Contact\\RC Contact NO 13-14.xsy"
BJ60 = {}            # (haut / bas, colonne x) -> borne +BJM
DEV60 = {}           # colonne x -> contact


def entree(inp, row, elems):
    """elems : liste de (type, repère, fichier, description, broches) du haut vers le bas ; type « bjm » : (câble, conducteur)
    dans repère / fichier."""
    p = k501e[inp]
    x = p.x
    # alignement de Julien (30/10) : bornes sur 2 lignes (haut, bas), contacts sur 2 niveaux en quinconce ;
    # v37 : bornes de la boîte sur 2 lignes entre les bornes et les contacts
    y = Y60 + (4000 if row == 1 else 6400)
    cur = (x, 3200)
    vu = False                                   # contact déjà passé ?
    for kind, rep, xsy, des, pins in elems:
        if kind == "borne":
            b = borne(rep, f, x, Y60 + 11600 if vu else Y60, fpos=(150, 125))
            W(f, [cur, b["1"]], "24")
            cur = b["2"].xy
        elif kind == "bjm":
            b = bjm(f, x, Y60 + 9200 if vu else Y60 + 2400, rep, xsy)        # v38 : 1600 libres autour des câbles
            BJ60[("bas" if vu else "haut", x)] = b
            W(f, [cur, b["1"]], "24")
            cur = b["2"].xy
        else:
            # v38 : 2e rangée, repère à gauche du contact (à droite, il coupait le cadre du lieu voisin)
            kw_ = {"fpos": (-500, 700)} if row == 2 else {}
            if kind == "maitre":
                s = g.place(xsy, rep, F[f], x, y, champs=info(rep), loc=loc(rep), compact=True, rep_size=200,
                            prefix=rep[0], **kw_)
            else:
                s = esclave(xsy, rep, f, x, y, des=des, prefix=rep[:2] if rep.startswith("KM") else rep[0], **kw_)
            DEV60[x] = s
            W(f, [cur, s[pins[0]]], "24")
            cur = s[pins[1]].xy
            vu = True
    W(f, [cur, p], "24")


def ext(b1, c1, dev, c2, b2, cable):
    """Entrée par la boîte : borne, +BJM, contact, +BJM, borne."""
    return [("borne", b1, None, None, None), ("bjm", cable, c1, None, None), dev, ("bjm", cable, c2, None, None),
            ("borne", b2, None, None, None)]


entree("I0.0", 1, ext("X711.5", 5, ("esclave", "S412", nom, "AU pupitre - contact NO", ("13", "14")), 6, "X711.6", "W11"))
entree("I0.1", 2, [("borne", "X721.5", None, None, None),
                   ("esclave", "S411", nom, "AU armoire - contact NO", ("13", "14")),
                   ("borne", "X721.6", None, None, None)])
entree("I0.4", 1, ext("X711.11", 17, ("esclave", "S413", CT[9], "AUTO-C : info Auto", ("9", "10")), 18, "X711.12", "W11"))
entree("I0.5", 2, ext("X711.17", 19, ("esclave", "S413", CT[11], "MANU-C : info Manu", ("11", "12")), 20, "X711.18", "W11"))
FDC = {"I0.6": ("B501", "Fin de course axe 1 min", 1, "X701.9", "X701.10", 5),
       "I0.7": ("B502", "Fin de course axe 1 max", 2, "X701.11", "X701.12", 7),
       "I1.0": ("B503", "Fin de course axe 2 min", 1, "X701.13", "X701.14", 9),
       "I1.1": ("B504", "Fin de course axe 2 max", 2, "X701.15", "X701.16", 11)}
for inp, (rep, des, row, t1, t2, c_) in FDC.items():
    REP[rep] = {"des": des, "fab": "RS PRO 902-6874", "carac": "contact NF 11-12 (0 = fin de course atteinte)", "loc": "+M"}
    entree(inp, row, ext(t1, c_, ("maitre", rep, fdc, "", ("11", "12")), c_ + 1, t2, "W12"))
for inp, rep, pref, row, des in (("I1.2", "KM1", "KM", 1, "Retour contacteur amont variateur 1 (aux NO)"),
                                 ("I1.3", "KM2", "KM", 2, "Retour contacteur amont variateur 2 (aux NO)"),
                                 ("I1.4", "Q423", "Q", 1, "Retour contacteur 48 V (aux NO)")):
    entree(inp, row, [("esclave", rep, nom, des, ("13", "14"))])
I50 = {inp: stub(f, (k501e[inp].x, CPU_Y - 1200), k501e[inp], "24") for inp in ("I0.2", "I0.3")}
# I1.5 : renvoi à droite (au-dessus, il chevaucherait le repère de la borne de I0.1)
I50["I1.5"] = W(f, [k501e["I1.5"], (k501e["I1.5"].x, CPU_Y - 400), (k501e["I1.5"].x + 1600, CPU_Y - 400)], "24")
renvoi("40", Z1_40, f, I50["I1.5"], "24")
renvoi("43", VOIES["B411"][1], f, I50["I0.2"], "24")
renvoi("43", VOIES["B412"][1], f, I50["I0.3"], "24")
# câbles : W11 (pupitre) pour -S2 seul et pour -S3, W12 (machine) pour -B3 à -B6 ; une ligne en haut, une en bas
for xs_, rep_, compo_, haut_, bas_ in (([k501e["I0.0"].x], "W11", "27G1 blindé", (5,), (6,)),
                                      ([k501e["I0.4"].x, k501e["I0.5"].x], "W11", "27G1 blindé", (17, 19), (18, 20)),
                                      ([k501e[i].x for i in ("I0.6", "I0.7", "I1.0", "I1.1")], "W12", "19G1 blindé",
                                       (5, 7, 9, 11), (6, 8, 10, 12))):
    for y_, n_ in ((Y60 + 1600, haut_), (Y60 + 10400, bas_)):
        g.cable(F[f], 0, 0, y_, rep_, compo_, "", xs_, ovale=True, nums=n_, court=True)
# cadres pointillés (lieu) : boîte +BJM (en haut, en bas), pupitre +P1, machine +M
xS2, xS3, xB = [k501e["I0.0"].x], [k501e["I0.4"].x, k501e["I0.5"].x], [k501e[i].x for i in ("I0.6", "I0.7", "I1.0", "I1.1")]
for cote in ("haut", "bas"):
    for xs_ in (xS2, xS3 + xB):
        cadre_lieu(f, [BJ60[(cote, x_)] for x_ in xs_], "+BJM", marge=100, haut=0, droite=xs_ == xS2, gauche=xs_ != xS2)
# v40 (Julien 25/11 : les cadres doivent bien englober les contacts, attention aux numéros des broches) :
# chaque cadre contient le contact ENTIER, broches et leurs numéros compris (bords à 200 des broches, sur les fils)


def avec_broches(s_):
    yp_ = [xy[1] for lst in s_.pins.values() for xy in lst]
    xp_ = [xy[0] for lst in s_.pins.values() for xy in lst]
    return (min(s_.bbox[0], min(xp_) - 300), min(yp_), max(s_.bbox[2], max(xp_) + 300), max(yp_))


cadre_lieu(f, [DEV60[x_] for x_ in xS2] + [avec_broches(DEV60[x_]) for x_ in xS2], "+P1", marge=200, haut=0, droite=True)
# S3 et B3 à 800 l'un de l'autre : cadres sur le contour des symboles seulement (pas leurs repères), sinon ils se croisent
cadre_lieu(f, [avec_broches(DEV60[x_]) for x_ in xS3], "+P1", marge=200, haut=0, txt=(xS3[0] + 100, Y60 + 6600))
cadre_lieu(f, [avec_broches(DEV60[x_]) for x_ in xB], "+M", marge=200, haut=0, txt=(xB[0] + 100, Y60 + 6600))
# v39 : tableau des entrées déplacé au f60 (plus de place au f61, symbole élargi)


# ======================================================================== 55 AUTOMATE ALIMENTATION & PROFINET (v38)
# Julien 24/11 : folio à part (f60 affiché) : L+ / M aux barres du haut, FE vers la terre (f10), sortie 24 V capteurs
# vers -X21.14 (f31), PROFINET X1 P1 vers le switch (f54) ; X1 P2 et M capt non utilisés
f = "55"
CPU55_Y = 9600
k501a = maitre(C + "Siemens_6ES7214-1AH50-0XB0_CPU1214C_G2_alim_profinet.xsy", "K501", f, 4800, CPU55_Y, wrap=30)
PE_DEST.append((f, W(f, [k501a["FE"], (6400, CPU55_Y - 1600)], "PE")))
LPC50 = W(f, [k501a["L+ capt"], (7200, CPU55_Y - 3200)], "24")      # sortie 24 V capteurs -> entrée de -X21.14 (f31)
renvoi(f, LPC50, "31", d31["LPC_E"], "24")
for i_, l_ in enumerate(("Sortie 24 V capteurs", "-> -X314 (f31), départs au f50")):
    texte(f, 7600, CPU55_Y - 2400 + 300 * i_, l_, 200)
PN50 = W(f, [k501a["X1 P1"], (k501a["X1 P1"].x + 3600, k501a["X1 P1"].y)], "PN")
texte(f, k501a["X1 P1"].x + 400, k501a["X1 P1"].y - 500, "PROFINET -> switch -K4 (f54)", 200)
# v39 (Julien 24/11) : tableau des entrées de la CPU (plus de place au f61)
g.tableau(F[f], 16800, 3600, [1200, 1400, 5600], 300, [
    ["Entrée", "Repère", "Fonction"], ["I0.0", "-S412", "AU pupitre actionné (NO)"], ["I0.1", "-S411", "AU armoire actionné (NO)"],
    ["I0.2", "-B411", "capot ouvert, mécanique (23-24)"], ["I0.3", "-B412", "capot ouvert, magnétique (23-24)"],
    ["I0.4", "-S413", "mode Auto (AUTO-C)"], ["I0.5", "-S413", "mode Manu (MANU-C)"],
    ["I0.6 / I0.7", "-B501 / -B502", "fins de course axe 1 (NF)"],
    ["I1.0 / I1.1", "-B503 / -B504", "fins de course axe 2 (NF)"],
    ["I1.2 / I1.3", "-KM1 / -KM2", "retour contacteurs variateurs"],
    ["I1.4", "-Q423", "retour contacteur 48 V"], ["I1.5", "-K401", "diagnostic relais sécu (Z1)"],
], size=180)

# ======================================================================== 51 AUTOMATE SORTIES
f = "51"
k501s = maitre(C + "Siemens_6ES7214-1AH50-0XB0_CPU1214C_G2_sorties.xsy", "K501", f, 4800, 6400, ref=(),
               base="K501", compact=True, rep_size=300, fpos=(-400, -2000))     # repère près du module (Julien)
W(f, [k501s["2L+"], (4800, 7200), (4000, 7200), (4000, RAIL24_Y)], "24")
W(f, [k501s["2M"], (5600, 7600), (3600, 7600), (3600, RAIL0_Y)], "0V")
Q51 = {q: W(f, [k501s[q], (k501s[q].x, 8000)], "24") for q in ("Q0.0", "Q0.1", "Q0.2", "Q0.3", "Q0.4", "Q0.5")}
# 16/11 (Julien) : colonne -H1 et voyant -H4 dessinés au f62, avec la SM 1223 qui les commande
# PUL des 2 drivers obligatoirement en 100 kHz (Julien, 30/10) : Q0.0 à Q0.3 seulement, Q0.4 et suivantes = 20 kHz
for q, (T, sg) in (("Q0.0", ("T322", "PUL")), ("Q0.1", ("T322", "DIR")), ("Q0.2", ("T323", "PUL")),
                   ("Q0.3", ("T323", "DIR")), ("Q0.4", ("T322", "ENA")), ("Q0.5", ("T323", "ENA"))):
    renvoi(f, Q51[q], "32", CMD32[(T, sg)], "24")

reserve(f, [k501s[q] for q in ("Q0.6", "Q0.7", "Q1.0", "Q1.1")], True)   # v37 (D21) : une seule accolade
g.tableau(F[f], 20800, 15600, [1800, 1600, 4800], 300, [
    ["Sortie", "Repère", "Fonction"], ["Q0.0 / 0.1 / 0.4", "-T322", "PUL / DIR / ENA axe 1 (PUL 100 kHz)"],
    ["Q0.2 / 0.3 / 0.5", "-T323", "PUL / DIR / ENA axe 2 (PUL 100 kHz)"],
    ["Q0.6, Q0.7, Q1.0, Q1.1", "", "réserve"],
    ["SM 1223 (f52)", "", "colonne -P511, voyant défaut -P513"],
], size=200)

# ======================================================================== 52 MODULE SM 1223
f = "52"
k521e = maitre(C + "Siemens_6ES7223-5BH50-0XB0_SM1223_G2_alim_entrees.xsy", "K521", f, 4800, 4400, wrap=30)
W(f, [k521e["L+"], (4800, RAIL24_Y)], "24")
for p in ("M", "1M", "2M"):
    W(f, [k521e[p], (k521e[p].x, RAIL0_Y)], "0V")
# 16/11 (Julien) : sorties remontées, colonne -H1 et voyant -H4 dessinés ici (avant : f61, par renvois)
k521s = maitre(C + "Siemens_6ES7223-5BH50-0XB0_SM1223_G2_sorties.xsy", "K521", f, 4800, 9600, ref=(),
               compact=True, rep_size=300, fpos=(-400, -2100))                  # repère près du module (Julien)
CMD52 = W(f, [k521s["3L+"], (4800, 11200)], "24")
renvoi("31", d31["CMD52"], f, CMD52, "24")
W(f, [k521s["3M"], (5600, 13200), (3600, 13200), (3600, RAIL0_Y)], "0V")
voyant = "Signalisation et voyants\\Voyant.xsy"
# v37 (revue Krizox, D08 / D12 / D22) : colonne -H1 centrée sous ses bornes : sorties -> bornes -X62.11-13 -> câble W12
# (conducteurs 13 à 16) -> boîte +BJM -> fils -> -H1 ; commun : -H1 COM -> +BJM -> W12 -> -X62.14 -> 0 V (collecteur du bas).
# Voyant de porte -H4 à droite (par ses bornes -X62.21 / -X62.22, pas par la boîte).
# v38 (retours v37) : 1600 libres autour du câble W12 et des cadres : câble 14000, boîte 14800, colonne 16400
col = maitre(C + "RSPRO_199-9760_colonne_lumineuse.xsy", "P511", f, 16000, 16400, fpos=(-3400, 500))   # textes à gauche
BCOL = {c: borne(t, f, col[c].x, 12400) for c, t in (("RD", "X701.43"), ("OG", "X701.44"), ("GN", "X701.45"))}
XCOM = col["GN"].x + 1600
BJCOL = {c: bjm(f, col[c].x, 14800, "W12", n) for c, n in (("RD", 13), ("OG", 14), ("GN", 15))}
BJCOL["COM"] = bjm(f, XCOM, 14800, "W12", 16)
bcom = borne("X701.46", f, XCOM, 12400)
REP["P513"] = {"des": "Voyant porte : défaut machine", "fab": "À définir", "carac": "24 V CC - rouge", "loc": "+A1"}
XH4 = XCOM + 2400
p513 = decrit(voyant, "P513", f, XH4, 13200, "Voyant porte : défaut machine", fpos=(600, 400), wrap=20, prefix="P", nomenc=True)
# v40 (Julien 25/11 : bornes de -H4 trop serrées) : 1200 entre chaque borne et le voyant (800 avant)
bh4a, bh4b = borne("X721.13", f, XH4, 11600), borne("X721.14", f, XH4, 16000)     # porte (05/11)
# sorties -> appareils : la sortie la plus à gauche descend le plus bas (aucun croisement)
for q, dest, yh in (("Q8.0", BCOL["RD"]["1"], 12000), ("Q8.1", BCOL["OG"]["1"], 11600), ("Q8.2", BCOL["GN"]["1"], 11200),
                    ("Q8.4", bh4a["1"], 10800)):
    W(f, [k521s[q], (k521s[q].x, yh), (dest.x, yh), dest], "24")
for c in BCOL:
    W(f, [BCOL[c]["2"], BJCOL[c]["1"]], "24")
    W(f, [BJCOL[c]["2"], col[c]], "24")
W(f, [bh4a["2"], p513["X1"]], "24")
W(f, [p513["X2"], bh4b["1"]], "0V")
W(f, [col["COM"], (col["COM"].x, 18800), (XCOM, 18800), BJCOL["COM"]["2"]], "0V")
W(f, [BJCOL["COM"]["1"], bcom["2"]], "0V")
g.cable(F[f], 0, 0, 14000, "W12", "19G1 blindé", "Machine : capot B1, fins de course B3-B6, colonne H1",
        [col["RD"].x, col["OG"].x, col["GN"].x, XCOM], ovale=True, compo_dx=-2400, nums=(13, 14, 15, 16))
# 0 V de la colonne (par -X62.14) et du voyant : collecteur sous les appareils, rejoint le 0 V de la SM 1223 à gauche
W(f, [bcom["1"], (XCOM, 12000), (XCOM + 800, 12000), (XCOM + 800, 19200)], "0V")
W(f, [bh4b["2"], (XH4, 19200), (3600, 19200), (3600, 13200)], "0V")
cadre_lieu(f, list(BJCOL.values()), "+BJM", marge=100, haut=0, gauche=True)     # v37 (D09)
cadre_lieu(f, [col], "+M", marge=200, haut=500, gauche=True)        # v39 : au-dessus des repères RD / OG / GN
# v37 (D21) : I8.0-I8.3 et I8.4-I8.7 restent en 2 groupes (la broche 2M, câblée, est entre les deux) ; Q8.3 seule
reserve(f, [k521e[i] for i in ("I8.0", "I8.1", "I8.2", "I8.3")], False)
reserve(f, [k521e[i] for i in ("I8.4", "I8.5", "I8.6", "I8.7")], False)
reserve(f, [k521s["Q8.3"]], True)
reserve(f, [k521s[q] for q in ("Q8.5", "Q8.6", "Q8.7")], True)
g.tableau(F[f], 16000, 6800, [2800, 1600, 5600], 300, [
    ["E/S", "Repère", "Fonction"], ["I8.0..I8.7", "", "réserve"],
    ["Q8.0 / 8.1 / 8.2", "-P511", "colonne rouge / orange / vert"],
    ["Q8.3", "", "réserve"], ["Q8.4", "-P513", "voyant défaut machine"],
    ["Q8.5..Q8.7", "", "réserve"],
], size=200)
# 05/11 : E/S validées par Julien, mention « PROPOSITION A VALIDER » retirée

# ======================================================================== 53 MODULE SM 1231 TC
f = "53"
k531 = maitre(C + "Siemens_6ES7231-5QF50-0XB0_SM1231_TC_G2.xsy", "K531", f, 4800, 12000, wrap=30)
W(f, [k531["L+"], (4800, RAIL24_Y)], "24")
W(f, [k531["M"], (5600, RAIL0_Y)], "0V")
REP["B531"]["fab"] = REP["B531"]["fab"] or "Type K"
REP["B531"]["loc"] = "+M"                    # thermocouple de la tête d'extrusion, sur la machine (01_PROJET)
# v37 (revue Krizox, D08) : -B7 -> fils -> boîte +BJM -> câble W8 -> bornes -X63 -> -K3 ; -B7 remonté de 2000
# v39 (Julien 24/11 : trop serré, 24 V / 0 V mal placés) : thermocouple, boîte et bornes décalés de 4000 à droite
# v40 (Julien 25/11 : « Réserve » superposé au reste) : chaîne thermocouple dans l'axe de AI0+ / AI0- (fils droits,
# plus de fils horizontaux au-dessus des voies de réserve AI1 à AI7) ; 1200 à droite des fils 24 V / 0 V du module
# v42 (Julien 26/11 : « le numéro du fil est dans le symbole ») : le thermocouple de la librairie a ses broches en haut,
# les fils descendaient à travers son dessin ; symbole retourné (CUSTOM Thermocouple_bas, broches en bas)
b531 = maitre(C + "Thermocouple_bas.xsy", "B531", f, k531["AI0+"].x, 5200, prefix="B", fpos=(1400, -1200), align=0)
# 02/11 : 2 bornes pour thermocouple (référence à définir, pas encore achetée), entre le câble W8 et -K3
REP["X701.41"] = REP["X701.42"] = {"des": "Borne thermocouple (PT 2,5, Julien 18/11)", "fab": "", "carac": "", "loc": "+A1"}
xa_, xb_ = k531["AI0+"].x, k531["AI0-"].x
bt1, bt2 = borne("X701.41", f, xa_, 10000, fpos=(150, 125)), borne("X701.42", f, xb_, 10000, fpos=(150, 125))
bj1, bj2 = bjm(f, xa_, 7200, "W531", 1), bjm(f, xb_, 7200, "W531", 2)
W(f, [b531["1"], bj1["1"]], "TC")
W(f, [bj1["2"], bt1["1"]], "TC")
W(f, [bt1["2"], k531["AI0+"]], "TC")
W(f, [b531["2"], bj2["1"]], "TC")
W(f, [bj2["2"], bt2["1"]], "TC")
W(f, [bt2["2"], k531["AI0-"]], "TC")
# 16/11 : repère et composition du câble à droite (plus sur les fils), réserve AI1 à AI7 par une accolade
g.cable(F[f], xa_ - 400, xb_ + 400, 8800, "W531", "compensation type K RS 236-3959", "", [xa_, xb_], etiq=(xb_ + 800, 8700),
        size=250)
cadre_lieu(f, [bj1, bj2], "+BJM", marge=100, haut=0, droite=True)        # v37 (D09)
cadre_lieu(f, [b531], "+M", marge=200, haut=0, gauche=True)
reserve(f, [k531[p_] for p_ in ("AI1+", "AI7-")], False)

# ======================================================================== 54 PROFINET
f = "54"
k541 = maitre(C + "Weidmuller_2682250000_switch_IE-SW-AL05LM-5TX.xsy", "K541", f, 16000, 4400)
W(f, [k541["V1+"], (16000, RAIL24_Y)], "24")
W(f, [k541["V1-"], (16800, RAIL0_Y)], "0V")
PN54 = {}
for p_, t in (("P1", "Port 1 -> -K501 automate CPU 1214C, port X1 P1"),
              ("P2", "Port 2 -> -T201 variateur M1, port X40"),
              ("P3", "Port 3 -> -T211 variateur M2, port X40"),
              ("P4", "Port 4 -> -P601 IHM pupitre KTP700, port X1"), ("P5", "Port 5 : réserve")):
    px, py = k541[p_].xy
    if p_ != "P5":
        PN54[p_] = W(f, [k541[p_], (8000, py)], "PN")
    # v33 (Julien) : texte décalé à droite du repère PN1-PN4 (posé sur le fil en x 8600), au-dessus du fil
    texte(f, 9600 if p_ != "P5" else 8000, py - 350, t, 220)
# v37 (revue Krizox, D15) : adresses IP à fixer par Julien dans TIA, reportées ici ensuite
# v40 (Julien 25/11) : tableau centré sur la page (zone utile x 1500 à 29100), 800 sous le switch
g.tableau(F[f], (1500 + 29100) // 2 - (3000 + 6400 + 3600) // 2, 13200, [3000, 6400, 3600], 400, [
    ["Repère", "Appareil", "Adresse IP"], ["-K501", "Automate CPU 1214C (X1)", "à définir"],
    ["-T201", "Variateur M1 (X40)", "à définir"], ["-T211", "Variateur M2 (X40)", "à définir"],
    ["-P601", "IHM KTP700 (X1)", "à définir"], ["", "Masque de sous-réseau", "à définir"]], size=220)
renvoi(f, PN54["P1"], "55", PN50, "PN")
renvoi(f, PN54["P2"], "20", VAR[("20", "PN")], "PN")
renvoi(f, PN54["P3"], "21", VAR[("21", "PN")], "PN")

# ======================================================================== 60 PUPITRE
f = "60"
# v37 (revue Krizox, D08 / D09 / D12) : -P1 -> fils -> boîte +BJM -> câble W11 (conducteurs 21, 22, V/J) -> bornes -X50
p601 = maitre(C + "Siemens_6AV2123-2GB03-0AX0_IHM_KTP700_Basic_PN.xsy", "P601", f, 8000, 9600)
# v38 (retours v37) : 1600 libres autour du câble et du cadre de la boîte : boîte à 1200 sous l'IHM, câble à 2400, bornes à 3600
Y50 = p601["L+"].y
t21, t22, t23 = (borne(n_, f, x_, Y50 + 3600, fpos=(150, 125)) for n_, x_ in (("X711.21", 8000), ("X711.22", 8800), ("X711.23", 9600)))
bj50 = {p: bjm(f, x, Y50 + 1200, "W11", c) for p, x, c in (("L+", 8000, 21), ("M", 8800, 22), ("FE", 9600, "PE"))}
for p, tb, ty in (("L+", t21, "24"), ("M", t22, "0V"), ("FE", t23, "PE")):
    W(f, [p601[p], bj50[p]["1"]], ty)
    W(f, [bj50[p]["2"], tb["1"]], ty)
g.cable(F[f], 0, 0, Y50 + 2400, "W11", "27G1 blindé", "Pupitre : AU S2, sélecteur S3, alimentation IHM", [8000, 8800], ovale=True,
        compo_dx=-2200, nums=(21, 22), vj=[9600])
cadre_lieu(f, [p601], "+P1 PUPITRE", marge=400, haut=300)
cadre_lieu(f, list(bj50.values()), "+BJM", marge=100, haut=0, droite=True)
YT50 = Y50 + 4000                  # broches du bas des bornes -X50
W(f, [t21["2"], (8000, YT50 + 1200), (4000, YT50 + 1200), (4000, RAIL24_Y)], "24")
W(f, [t22["2"], (8800, YT50 + 1600), (3600, YT50 + 1600), (3600, RAIL0_Y)], "0V")
PE_DEST.append((f, W(f, [t23["2"], (9600, YT50 + 2000)], "PE")))
renvoi(f, W(f, [p601["X1"], (p601["X1"].x, Y50 + 2000)], "PN"), "54", PN54["P4"], "PN")
texte(f, 4200, YT50 + 900, "24VELEC", 220)
texte(f, 10000, YT50 + 1200, "Bornes -X50.11 à -X50.13 (armoire)", 220)

# ======================================================================== 80 - 92
# v33 (Julien 18/11) : f80 (liste des câbles, saisie.json) et f90 à f92 (nomenclature) générés par le script, en fin
# de script ; le tableau WinRelais du f80 (16/11) est abandonné : W11, W12, W14, PN1-PN4 absents, W9 / W10 « 4 cond. »
# v34 (Julien 18/11) : image du plan d'implantation (implantation/) à insérer quand il sera validé
texte("85", 1600, 1700, "Implantation armoire +A1 : image du plan d'implantation à insérer quand il sera validé.", 300)

# ======================================================================== spécification des liaisons
MEMES = [
    # B2 du relais de sécurité au 0 V commun (R-02, 02/11)
    ["K401:B2", "K401:A2", "X312:1"],
    # AU armoire par les bornes de la porte, Z1 -> I1.5 (02/11)
    ["K401:S11", "X721.1:1"], ["X721.1:2", "S411:1"], ["S411:2", "X721.2:1"], ["X721.2:2", "X711.1:1"],
    ["K401:S21", "X721.3:1"], ["X721.3:2", "S411:21"], ["S411:22", "X721.4:1"], ["X721.4:2", "X711.3:1"],
    ["K501:I0.1", "X721.6:2"], ["X721.6:1", "S411:14"], ["S411:13", "X721.5:2"], ["K401:Z1", "K501:I1.5"],
    # chaîne d'arrêt d'urgence et capots (deux voies), pontage Manu par -S413
    ["K401:S11", "S411:1"], ["S411:2", "X711.1:1"], ["X711.1:2", "S412:1"], ["S412:2", "X711.2:1"],
    ["X711.2:2", "X701.1:1", "X711.13:1"], ["X701.1:2", "B411:11"], ["B411:12", "X701.2:1"],
    ["X701.2:2", "K401:S12", "X711.14:2"], ["X711.13:2", "S413:3"], ["S413:4", "X711.14:1"],
    ["K401:S21", "S411:21"], ["S411:22", "X711.3:1"], ["X711.3:2", "S412:21"], ["S412:22", "X711.4:1"],
    ["X711.4:2", "X701.5:1", "X711.15:1"], ["X701.5:2", "B412:11"], ["B412:12", "X701.6:1"],
    ["X701.6:2", "K401:S22", "X711.16:2"], ["X711.15:2", "S413:7"], ["S413:8", "X711.16:1"],
    ["B411:23", "X701.3:2"], ["B411:24", "X701.4:1"], ["B412:23", "X701.7:2"], ["B412:24", "X701.8:1"],
    # boucle de retour (EDM) et réarmement
    ["K401:Y1", "KM1:21"], ["KM1:22", "KM2:21"], ["Q423:22", "X721.7:1"], ["X721.7:2", "S414:3"], ["S414:4", "X721.8:2"], ["X721.8:1", "K401:Y2"],
    # sorties du relais de sécurité (architecture du 27/10)
    ["K401:14", "Q421:A1", "Q422:A1", "X711.19:1"], ["X711.19:2", "S413:15"], ["S413:16", "X711.20:1"],
    ["X711.20:2", "Q423:A1"],
    ["K401:24", "X711.7:1"], ["X711.7:2", "S413:1"], ["S413:2", "X711.8:1"], ["X711.8:2", "KM1:A1", "KM2:A1"],
    ["K401:34", "X711.9:1"], ["X711.9:2", "S413:5"], ["S413:6", "X711.10:1"],
    ["X711.10:2", "T201:X6:1"], ["T201:X6:3", "T211:X6:1"], ["T201:X6:4", "T211:X6:2"],
    # sorties automate
    ["K501:Q0.0", "T322:PUL+"], ["K501:Q0.1", "T322:DIR+"], ["K501:Q0.4", "T322:ENA+"],
    ["K501:Q0.2", "T323:PUL+"], ["K501:Q0.3", "T323:DIR+"], ["K501:Q0.5", "T323:ENA+"],
    ["K521:Q8.0", "X701.43:1"], ["X701.43:2", "P511:RD"], ["K521:Q8.1", "X701.44:1"], ["X701.44:2", "P511:OG"],
    ["K521:Q8.2", "X701.45:1"], ["X701.45:2", "P511:GN"], ["P511:COM", "X701.46:1"],
    ["K521:Q8.4", "X721.13:1"], ["X721.13:2", "P513:X1"], ["P513:X2", "X721.14:1"],
    ["X721.11:2", "P512:X1"], ["P512:X2", "X721.12:1"], ["X721.9:2", "H2:X1"], ["H2:X2", "X721.10:1"],
    # entrées automate
    ["K501:I0.0", "X711.6:2"], ["K501:I0.1", "S411:14"], ["K501:I0.2", "X701.4:2"], ["K501:I0.3", "X701.8:2"],
    ["K501:I0.4", "X711.12:2"], ["K501:I0.5", "X711.18:2"], ["K501:I0.6", "X701.10:2"], ["K501:I0.7", "X701.12:2"],
    ["K501:I1.0", "X701.14:2"], ["K501:I1.1", "X701.16:2"], ["K501:I1.2", "KM1:14"], ["K501:I1.3", "KM2:14"],
    ["K501:I1.4", "Q423:14"],
    ["K501:L+ capt", "X314:E", "X701.3:1", "X701.7:1", "X701.9:1", "X701.11:1", "X701.13:1", "X701.15:1", "X711.5:1",
     "X711.11:1", "X711.17:1", "S411:13", "KM1:13", "KM2:13", "Q423:13"],
    ["X313:1", "K521:3L+", "F401:2"], ["F401:1", "K401:13", "K401:23", "K401:33"],
    ["X311:1", "K401:A1", "K501:L+", "K501:2L+", "K521:L+",
     "K531:L+", "K541:V1+", "X721.11:1", "T201:X5:24V", "T211:X5:24V", "X711.21:2"],
    ["X312:1", "K401:A2", "K501:M", "K501:1M", "K501:2M", "K521:M", "K521:3M", "K531:M", "K541:V1-",
     "KM1:A2", "KM2:A2", "Q421:A2", "Q422:A2", "Q423:A2", "X701.46:2", "X721.12:2", "X721.14:2",
     "T201:X5:GND", "T211:X5:GND", "T201:X6:2",
     "T322:PUL-", "T322:DIR-", "T322:ENA-", "T323:PUL-", "T323:DIR-", "T323:ENA-", "X711.22:2"],
    ["K501:FE", "P601:FE", "X101.VJ:2", "T301:PE", "T302:PE", "X36.1:2", "X131:PE", "T321:PE",
     "T201:X1:PE", "T211:X1:PE"],
    ["M201:PE", "T201:X2:PE"], ["M211:PE", "T211:X2:PE"],
    ["B531:1", "K531:AI0+"], ["B531:2", "K531:AI0-"],
    # moteurs SEW : frein (W202 / W212) et sonde TF (W203 / W213) en direct, sans bornier
    ["M201:1b", "T201:X10:3"], ["M201:2b", "T201:X10:4"], ["M211:1b", "T211:X10:3"], ["M211:2b", "T211:X10:4"],
    ["Q421:4/T2", "M201:2"], ["Q421:6/T3", "M201:3"], ["Q422:4/T2", "M211:2"], ["Q422:6/T3", "M211:3"],
    # distribution par bus (29/10) : phases de -QF1 jusqu'aux appareils
    ["Q102:2", "Q121:1/L1", "Q122:1/L1", "Q123:1", "Q124:1", "Q132:1", "Q133:1"],
    ["Q102:4", "Q121:3/L2", "Q122:3/L2", "Q123:3", "Q134:3"],
    ["Q102:6", "Q121:5/L3", "Q122:5/L3", "Q124:3", "X721.9:1", "Q136:1", "Q137:1", "Q131:1"],
    ["Q102:N", "Q132:N", "Q134:1", "X721.10:2", "Q136:N", "Q137:N", "Q131:N"],
    ["Q132:2", "T301:L"], ["Q133:2", "T302:L"], ["Q134:4", "T321:L"], ["Q134:2", "T321:N"],
    ["KM1:2/T1", "T201:X1:L1"], ["KM2:6/T3", "T211:X1:L3"],
    ["T321:+V", "Q423:1/L1"], ["T321:+V", "Q423:3/L2"], ["Q423:2/T1", "T322:+V"], ["Q423:4/T2", "T323:+V"],
    ["T321:-V", "T322:-V"], ["T321:-V", "T323:-V"],
    ["T301:-V", "T302:-V", "X312:1", "X36.1:1"], ["T302:+V", "X311:1"], ["T301:+V", "X313:1"],
]
DIFFERENTS = ["X311:1", "X312:1", "X313:1", "X711.8:2", "X711.10:2", "X711.20:2", "K401:14", "K401:24", "K401:34", "Q423:2/T1", "Q423:4/T2",
              "Q121:1/L1", "Q121:3/L2", "Q121:5/L3", "Q134:1", "K401:S11", "K401:S12", "K401:S21", "K401:S22",
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
    memes = [[ren(p) for p in grp] for grp in MEMES]
    differents = [ren(p) for p in DIFFERENTS]
    out = []
    for grp in memes:
        for p in grp:
            if p not in net:
                out.append(f"spécification : broche {p} absente du schéma")
        ids = [net[p] for p in grp if p in net]
        if ids and not set.intersection(*ids):
            out.append("spécification : pas sur la même équipotentielle : " + ", ".join(grp))
    seen = {}
    for p in differents:
        for r in net.get(p, ()):
            if r in seen:
                out.append(f"spécification : court-circuit entre {seen[r]} et {p}")
            seen[r] = p
    return out


# ======================================================================== plans de bornier (f70, f71)
TERRAIN = ("B", "M", "S2", "S3", "P1")    # appareils hors armoire (+M, +P1), nouveaux repères


# potentiels communs à plusieurs appareils : nommés dans les tableaux de bornier
POTENTIELS = [("-K501:L+ capt", "+24 V capteurs (-X314 noir, L+ capt -K501, f31)"),
              ("-Q423:13", "+24 V capteurs (-X314 noir, f31)"),           # v34 : départs du bloc X21.14
              ("-T301:PE", "Terre PE / FE (-XPE1, f10)"),
              ("-F401:2", "24VSEC (-X313, f31)"),
              ("-K401:A2", "0 V commande (-X312, f31)"),
              ("-X101.VJ:2", "Terre PE / FE (arrivée -X101, f10)"),
              ("-T201:X6:1", "STO de -T201 (f20), puis -T211 (f21) en chaîne"),
              ("-K401:A1", "24VELEC (-X311, f31)")]


def designations():
    """Repère -> désignation (champ 2 du symbole maître, sinon du premier symbole)."""
    des = {}
    for p in g.symbols:
        d = p.block[4].split("·")[0]
        if d:
            des.setdefault(p.rep, d)
    for rep, r in REP.items():
        if r.get("des"):
            des[ren(rep)] = ren(r["des"])
    return des


def plan_bornier(path, noms):
    """Pour chaque borne (noms, dans l'ordre) : appareils raccordés côté armoire / côté terrain (broches 1 / 2)."""
    net, membres = nets_par_broche(path, bornes_passantes=False)
    lignes = []
    for nom in noms:
        cotes, terrain = [], []
        for pin in ("1", "2"):
            autres, ponts, ext = [], [], []
            for r in net.get(f"{nom}:{pin}", ()):
                for rep, b, fo in membres[r]:
                    if rep == nom:
                        continue
                    if re.match(r"X\d", rep):
                        ponts.append(f"-{rep} (f{fo})")
                    else:
                        autres.append(f"-{rep}:{b} (f{fo})")
                        ext.append(rep.startswith(TERRAIN))
            # une borne reliée seulement à une autre borne : on nomme cette borne
            autres = sorted(set(autres)) or sorted(set(ponts))
            nom_pot = [ren(t) for k, t in POTENTIELS if any(a.startswith(ren(k) + " ") for a in autres)]
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
        lignes.append([nom, cotes[0], cotes[1]])
    return lignes


# f70 (09/11, Julien) : borniers rangés comme en vrai, rail par rail, dans l'ordre de l'implantation v10
# (implantation/JOURNAL.md). Une ligne par tronçon (ou par câble) ; butée (trait épais) de chaque côté de chaque groupe.
# Case : n° de conducteur (câbles W11 / W12) ou signal ; dessous : repère de la borne, puis nom du groupe.
# Les conducteurs de réserve des 27G1 / 19G1 ne sont pas bornés.
def _n(prefix, bornes, nums):
    return [(b, str(n)) for b, n in zip(bornes, nums)]


_SIG = {i: sg for _, _, _, _, _, bs in GROUPES for i, sg in bs}


def _g(nom, bornes):
    return (nom, [(b, _SIG.get(b, "")) for b in bornes])


RAILS_X70 = [
    ("R5, tronçon 1 : câble -W11 (27G1 : 26 + PE, 4 de réserve non bornés) -> boîte +BJM -> pupitre +P1", [
        ("AU -S2", _n("", [f"X711.{n}" for n in (1, 2, 3, 4, 5, 6)], range(1, 7))),
        ("Sélecteur -S3", _n("", [f"X711.{n}" for n in (13, 14, 15, 16, 19, 20, 7, 8, 9, 10, 11, 12, 17, 18)], range(7, 21))),
        ("IHM -P1", [("X711.21", "21"), ("X711.22", "22"), ("X711.23", "PE")])]),
    ("R5, tronçon 1 (suite) : câble -W12 (19G1 : 18 + PE, 2 de réserve non bornés, V/J -> -XPE1) -> boîte +BJM", [
        ("Capot -B1", _n("", [f"X701.{n}" for n in (1, 2, 3, 4)], range(1, 5))),
        ("Fins de course -B3 à -B6", _n("", [f"X701.{n}" for n in range(9, 17)], range(5, 13))),
        ("Colonne -H1", _n("", [f"X701.{n}" for n in (43, 44, 45, 46)], range(13, 17)))]),
    ("R5, tronçon 2 : capteurs et sondes", [
        _g("Capot -B2 (câble M12)", [f"X701.{n}" for n in (5, 6, 7, 8)]),
        _g("Thermocouple -B7 (W8)", ["X701.41", "X701.42"]),
        _g("Sonde TF M1 (W3)", ["X701.21", "X701.22"]),
        _g("Sonde TF M2 (W6)", ["X701.29", "X701.30"])]),
    ("R5, tronçon 3 : moteurs pas-à-pas", [
        _g("M3 (W9)", [f"X701.{n}" for n in range(33, 37)] + ["X701.47"]),
        _g("M4 (W10)", [f"X701.{n}" for n in range(37, 41)] + ["X701.48"])]),
    ("R5, tronçon 4 : puissance", [
        _g("Freins M1 + M2 (W4)", ["X701.23", "X701.24", "X701.31", "X701.32"]),
        _g("Moteur M1 (W2)", [f"X701.{n}" for n in range(17, 21)]),
        _g("Moteur M2 (W5)", [f"X701.{n}" for n in range(25, 29)]),
        _g("Arrivée réseau (W1)", ["X101.VJ", "X101.1", "X101.2", "X101.3", "X101.4"])]),
    ("R4 : services 230 V (à la place laissée par XR2), puis porte de l'armoire", [
        _g("Eclairage EL1 / EL2", ["X141.1", "X141.2"]),
        _g("Ventilation EV1 / EV2", ["X142.1", "X142.2"]),
        ("AU -S1", [(f"X721.{n}", "") for n in range(1, 7)]),
        ("Réarmement -S4", [("X721.7", ""), ("X721.8", "")]),
        ("Voyant -H3", [("X721.11", ""), ("X721.12", "")]),
        ("Voyant -H4", [("X721.13", ""), ("X721.14", "")]),
        ("Voyant -H2 230 V", [("X721.9", ""), ("X721.10", "")])]),
    ("R3 : distribution 24 V et liaison PELV (internes)", [
        ("24VELEC", [("X311", "+")]), ("0 V", [("X312", "0V")]), ("PELV 0 V - PE", [("X36.1", "PE")]),
        ("24VSEC", [("X313", "+")]), ("24 V capteurs", [("X314", "+")])]),
]


def organisation_x70():
    """Folio 70 : borniers rangés rail par rail comme dans l'implantation (Julien, 09/11)."""
    from xrs_gen import largeur
    f = "70"
    texte(f, 2400, 1300, "BORNIERS DE L'ARMOIRE +A1, RAIL PAR RAIL (ORDRE DE L'IMPLANTATION)", 300, 0, 1)
    texte(f, 2400, 1750, "Repère : X + n° du folio de la borne + n° de borne. Case : n° de conducteur (W11, W12) ou signal. "
                         "Trait épais : butée.", 200)
    # 16/11 (Julien) : cases agrandies pour occuper tout le folio (pas 1000, case 820 x 1000)
    PAS, CASE, BUT, DY = 1000, 820, 400, 2450
    y = 2400
    for titre, groupes in RAILS_X70:
        texte(f, 2400, y, titre, 240, 0, 1)
        x = 2400
        for nom, bornes in groupes:
            g.cadre(F[f], x - 50, y + 350, x + 50, y + 1450, width=40)          # butée avant le groupe
            x += BUT
            x0 = x
            for rep_, txt in bornes:
                g.cadre(F[f], x, y + 400, x + CASE, y + 1400, width=15)
                if txt:
                    texte(f, x + CASE // 2 - largeur(txt, 250) // 2, y + 775, txt, 250)
                lab = ren(rep_)
                texte(f, x + CASE // 2 - largeur(lab, 200) // 2, y + 1480, rep_, 200)
                x += PAS
            texte(f, x0, y + 1780, nom, 200, 0, 1)
            x += BUT - (PAS - CASE)
        g.cadre(F[f], x - 50, y + 350, x + 50, y + 1450, width=40)              # butée de fin
        y += DY


def ecrire_borniers(path):
    global DES
    DES = designations()
    plans_bornier(path)


# v37 (revue Krizox, D24, Julien 23/11) : plans de bornier « comme en vrai » (exemples SEE Electrical dans
# memoire/revues/2026-11-20_krizox_v36_exemples_bornier/), à la place de l'ancien tableau du f71, sur les f71 à f73.
# Chaque bornier : repère dans un cadre à gauche, une colonne par borne (vis en haut et en bas, n° au milieu),
# butée (trait épais) aux extrémités et entre deux fonctions (dizaines). Textes verticaux :
#   en haut (côté intérieur de l'armoire ; pour la boîte +BJM : côté câble) : appareil « -KA1:14 (f40) » et n° de fil ;
#   en bas (côté terrain ; pour la boîte : côté appareil) : appareil et câble « -W12 (6) » (repère, n° de conducteur).
# Format des textes provisoire (Julien : « on modifiera si besoin plus tard »).
PLANS_FOL = ("71", "72", "73", "74")
PAS_B, LB, HB = 600, 500, 1400          # pas des bornes, largeur, hauteur d'une borne
ECART_B = 1200                          # v39 (Julien 24/11) : écart de plus entre deux borniers d'une rangée
GRIS_TERRE = 15790320                   # v39 (Julien 24/11) : fond gris très clair (0xF0F0F0) ; remplacé en v40 par le vert / jaune
# v40 (Julien 25/11 : « en vert / jaune les borniers qui le sont, pas en nuance de gris ») : bandes jaunes et vertes (BGR)
JAUNE_VJ, VERT_VJ = 0x00E6FF, 0x40B000     # jaune RGB(255, 230, 0), vert RGB(0, 176, 64)


def cadre_vj(fo, x1, y1, x2, y2, color=0, width=20, bande=200, libre=None):
    """Rectangle rayé vert / jaune (borne ou bornier de terre) : fond jaune, bandes vertes, contour par-dessus.
    libre = (ya, yb) : zone sans bande verte (texte du numéro ou du repère, lisible et jamais coupé par un trait)."""
    g.cadre(F[fo], x1, y1, x2, y2, color=JAUNE_VJ, width=10, fond=JAUNE_VJ)
    y_ = y1 + bande
    while y_ < y2:
        a_, b_ = y_, min(y_ + bande, y2)
        for c_, d_ in ([(a_, b_)] if not libre else [(a_, min(b_, libre[0])), (max(a_, libre[1]), b_)]):
            if d_ - c_ >= 60:
                g.cadre(F[fo], x1, c_, x2, d_, color=VERT_VJ, width=10, fond=VERT_VJ)
        y_ += 2 * bande
    g.cadre(F[fo], x1, y1, x2, y2, color=color, width=width)
ZT, ZB = 2600, 2800                     # zones de texte au-dessus / en dessous des bornes
EXT_APP = ("B", "M", "S1", "S2", "S3", "S4", "H", "P1", "EL", "EV")   # appareils hors de l'armoire ou sur la porte


def _cables_par_borne():
    """{(repère de borne, broche) : (câble, n° de conducteur)} : borne atteinte depuis chaque brin, par les fils."""
    from collections import defaultdict
    adj = defaultdict(set)
    for w in g.wires:
        a, b = (w[0], w[1], w[2]), (w[0], w[3], w[4])
        adj[a].add(b)
        adj[b].add(a)
    broches = {}
    for s_ in g.symbols:
        for nom, pts in s_.pins.items():
            for xy in pts:
                broches[(s_.folio,) + tuple(xy)] = (s_, nom)
    out = {}
    for n, c in enumerate(g.cables):
        f_, y = c[0], c[3]
        nums = g.cable_nums.get(n) or [i + 1 for i in range(len(c[7]))]
        for xb, num_ in zip(c[7], nums):
            seg = next((w for w in g.wires if w[0] == f_ and w[1] == w[3] == xb and min(w[2], w[4]) < y < max(w[2], w[4])), None)
            if seg is None:
                continue
            pile, vus = [(f_, seg[1], seg[2]), (f_, seg[3], seg[4])], set()
            while pile:
                pt = pile.pop()
                if pt in vus:
                    continue
                vus.add(pt)
                if pt in broches:
                    s_, nom = broches[pt]
                    if s_.block[2].split("·")[11] == "1":        # borne : on s'arrête dessus
                        out[(s_.rep, nom)] = (ren(c[4]), num_)
                        continue
                    continue
                if len(adj[pt]) >= 3:                          # dérivation (peigne, bus) : ce n'est plus ce conducteur
                    continue
                pile += list(adj[pt])
    return out


def _cote(nom, pin, net, membres, num):
    """Appareils raccordés à une broche de borne (bornes non passantes) : liste de « -REP:broche (fNN) »."""
    autres, ponts = [], []
    for r in net.get(f"{nom}:{pin}", ()):
        for rep, b, fo in membres[r]:
            if rep == nom:
                continue
            (ponts if re.match(r"X\d", rep) else autres).append((rep, b, fo))
    return sorted(set(autres)), sorted(set(ponts))


# potentiels communs à plusieurs appareils : nom court sur les plans de bornier
POT_PLANS = [("-K501:FE", "Terre PE / FE"), ("-T301:PE", "Terre PE / FE"), ("-K501:L+ capt", "24 V capteurs (-X21.14)"),
             ("-Q423:13", "24 V capteurs (-X21.14)"), ("-F401:2", "24VSEC (-X21.13)"), ("-K401:A2", "0 V (-X21.12)"),
             ("-K401:A1", "24VELEC (-X21.11)"), ("-Q102:6", "L3 (bus 230 V)"), ("-Q102:N", "N (bus 230 V)")]


def _texte_cote(autres, ponts):
    if len(autres) > 1:
        noms = {f"-{r}:{b}" for r, b, _ in autres}
        for k_, nom_ in POT_PLANS:
            if ren(k_) in noms:
                return nom_
    if autres:
        rep, b, fo = autres[0]
        t = f"-{rep}:{b} (f{fo})"
        if len(autres) > 1:
            t += f" +{len(autres) - 1}"
        return t
    if ponts:
        rep, b, fo = ponts[0]
        return f"-{rep} (f{fo})"
    return ""


# v42 : fonction de chaque câble arrivant à la boîte +BJM (résumé sous les plans de bornier)
CAB_FN = {"W201": "moteur M1", "W211": "moteur M2", "W202": "freins M1 + M2", "W321": "pas-à-pas M3",
          "W322": "pas-à-pas M4", "W203": "sonde TF M1", "W213": "sonde TF M2",
          "W12": "machine : capot B1, fins de course B3-B6, colonne H1", "W14": "capot B2 (M12)",
          "W531": "thermocouple B7", "W11": "pupitre : AU S2, sélecteur S3, IHM P1"}


def resume_bornier(fo, x, y, larg, b, mo, taille=160, pas=220):
    """Texte court sous un bornier (v42) : bornes consécutives de même fonction regroupées, « 11-15 : fonction ».
    v43 (Julien 26/11 : « juste en dessous du rectangle avec le texte -X12 ») : sous le cadre du repère du bornier,
    sur sa largeur (larg), lignes coupées pour ne pas déborder sur les textes des bornes."""
    from xrs_gen import largeur, _wrap
    fn_ = {ren(i_): f for i_, f in DES_BORNE.items()}
    if b == "X1":
        fn_ = {r_: f"{ren(c_)} {CAB_FN.get(c_, '')}".strip() for (c_, _), r_ in BJM_POSES.items()}
    grp = []
    for r_ in mo:
        n_, f_ = r_.split(".")[1], fn_.get(r_, "")
        if grp and grp[-1][2] == f_:
            grp[-1][1] = n_
        else:
            grp.append([n_, n_, f_])
    for n_car in range(40, 8, -1):               # le plus de caractères par ligne qui tient dans la largeur
        lignes = []
        for a_, z_, f_ in grp:
            t_ = (a_ if a_ == z_ else f"{a_}-{z_}") + (f" : {ren(f_)}" if f_ else "")
            lignes += _wrap(t_, n_car)
        if max(largeur(l_, taille) for l_ in lignes) <= larg:
            break
    for i_, l_ in enumerate(lignes):
        texte(fo, x, y + pas * i_, l_, taille)


def plans_bornier(path):
    from xrs_gen import largeur
    net, membres = nets_par_broche(path, bornes_passantes=False)
    cab = _cables_par_borne()
    num_pot, racine_pot = NUMPOT
    bornes = {}
    for s_ in g.symbols:
        if s_.block[2].split("·")[11] == "1" and "PTFIX" not in s_.block[2].upper() and "." in s_.rep:
            bornes[s_.rep] = s_
    par_bornier = {}
    for rep in bornes:
        par_bornier.setdefault(rep.split(".")[0], []).append(rep)
    cle = lambda r: (r == "X1", int(r[1:]) if r[1:].isdigit() else 0)
    ordre = sorted(par_bornier, key=cle)
    # v40 (Julien 25/11 : « utiliser pleinement les 4 pages ») : les borniers, dans l'ordre, sont répartis sur les
    # 8 rangées (2 par folio) en équilibrant la largeur des rangées ; la boîte +BJM est coupée en morceaux égaux ;
    # dans une rangée, l'espace libre est réparti également entre les borniers et aux deux bords.
    NR, LU = 2 * len(PLANS_FOL), 27600
    larg_ = lambda mo: 2400 + len(mo) * PAS_B + 400
    meilleur = None
    for taille in range(40, 9, -1):
        segs = []
        for b in ordre:
            reps = sorted(par_bornier[b], key=lambda r: int(r.split(".")[1]))
            n_ = -(-len(reps) // taille)
            q_, r_ = divmod(len(reps), n_)
            i_ = 0
            for k_ in range(n_):
                m_ = q_ + (1 if k_ < r_ else 0)
                segs.append((b, reps[i_:i_ + m_]))
                i_ += m_
        if len(segs) < NR:
            continue
        # découpage optimal (programmation dynamique) : rangées consécutives, largeur maxi la plus petite
        W_ = [larg_(mo) for _, mo in segs]
        INF = float("inf")
        best = [[INF] * (NR + 1) for _ in range(len(segs) + 1)]
        cut = [[0] * (NR + 1) for _ in range(len(segs) + 1)]
        best[0][0] = 0
        for i_ in range(1, len(segs) + 1):
            for k_ in range(1, NR + 1):
                s_ = 0
                for j_ in range(i_, 0, -1):
                    s_ += W_[j_ - 1] + (ECART_B if j_ < i_ else 0)
                    if s_ > LU:
                        break
                    v_ = max(best[j_ - 1][k_ - 1], s_)
                    if v_ < best[i_][k_]:
                        best[i_][k_], cut[i_][k_] = v_, j_ - 1
        if best[len(segs)][NR] == INF:
            continue
        if meilleur is None or best[len(segs)][NR] < meilleur[0]:
            rangs_, i_ = [], len(segs)
            for k_ in range(NR, 0, -1):
                j_ = cut[i_][k_]
                rangs_.insert(0, segs[j_:i_])
                i_ = j_
            meilleur = (best[len(segs)][NR], rangs_)
    if meilleur is None:
        raise SystemExit("plans de bornier : pas de répartition sur les 8 rangées")
    rangs = meilleur[1]
    YR = (1900, 10900)                      # haut des 2 rangées d'un folio (zone de texte du haut comprise)
    for i, rang in enumerate(rangs):
        fo = PLANS_FOL[i // 2]
        y0 = YR[i % 2] + ZT                 # haut des bornes
        y1 = y0 + HB
        libre_ = LU - sum(larg_(mo) for _, mo in rang)
        if len(rang) > 1:                   # justifié : 1er bornier au bord gauche, dernier au bord droit
            ecart_ = libre_ // (len(rang) - 1) // 100 * 100
            x = 1600
        else:                               # bornier seul : centré
            ecart_ = 0
            x = 1600 + libre_ // 2 // 100 * 100
        for b, mo in rang:
            # repère du bornier dans un cadre, relié à la rangée
            nom_b = "+BJM -X1" if b == "X1" else f"-{b}"
            tout_terre = all("terre" in bornes[r_].block[2] for r_ in mo)
            xb0_ = x                             # v42 : début du bornier (résumé des fonctions dessous)
            if tout_terre:
                cadre_vj(fo, x, y0 + 200, x + 1800, y1 - 200, bande=100, libre=(y0 + HB // 2 - 250, y0 + HB // 2 + 250))
            else:
                g.cadre(F[fo], x, y0 + 200, x + 1800, y1 - 200, width=20)
            texte(fo, x + 900 - largeur(nom_b, 300) // 2, y0 + HB // 2 - 150, nom_b, 300, 0, 1)
            for yy in (y0 + 450, y1 - 450):
                g.ligne(F[fo], x + 1800, yy, x + 2400, yy, width=20)
            x += 2400
            g.ligne(F[fo], x, y0 - 100, x, y1 + 100, width=60)                # butée de début
            prec = None
            for rep in mo:
                s_ = bornes[rep]
                n_ = rep.split(".")[1]
                if prec is not None and n_[:-1] != prec[:-1]:
                    g.ligne(F[fo], x, y0 - 100, x, y1 + 100, width=60)        # butée entre deux fonctions
                prec = n_
                xc = x + PAS_B // 2
                terre = "terre" in s_.block[2]
                if terre:
                    # v42 (Julien 26/11 : rayé plus marqué) : bandes de 100 (200 avant)
                    cadre_vj(fo, xc - LB // 2, y0, xc + LB // 2, y1, color=32768, width=30, bande=100,
                             libre=(y0 + HB // 2 - 200, y0 + HB // 2 + 200))
                else:
                    g.cadre(F[fo], xc - LB // 2, y0, xc + LB // 2, y1, width=20)
                for yv in (y0 + 80, y1 - 300):
                    g.cadre(F[fo], xc - 120, yv, xc + 120, yv + 220, width=10)                       # vis
                lab = ("PE " if terre else "") + n_
                texte(fo, xc - largeur(n_, 220) // 2, y0 + HB // 2 - 110, n_, 220, 0, 1)
                # côtés : celui où passe un câble est le côté terrain (bornes d'armoire) ou le côté câble (boîte)
                c1, p1 = _cote(rep, "1", net, membres, None)
                c2, p2 = _cote(rep, "2", net, membres, None)
                k1, k2 = cab.get((rep, "1")), cab.get((rep, "2"))
                ext = lambda c: bool(c) and all(r.startswith(EXT_APP) for r, _, _ in c)
                if b == "X1":
                    bas_est_2 = not (k2 and not k1)                   # boîte : câble en haut, appareil en bas
                else:
                    bas_est_2 = bool(k2) or (not k1 and not ext(c1)) or ext(c2)
                (ch, ph, kh), (cb, pb, kb) = ((c1, p1, k1), (c2, p2, k2)) if bas_est_2 else ((c2, p2, k2), (c1, p1, k1))
                pin_h = "1" if bas_est_2 else "2"
                n_fil = "" if terre else num_pot.get(racine_pot(s_.folio, *s_.pins[pin_h][0]), "")
                # haut : fil, appareil (à gauche du fil), n° de fil (à droite) ; texte vertical, début près de la borne
                g.ligne(F[fo], xc, y0 - ZT + 200, xc, y0, width=10)
                # v42 (Julien 26/11) : nom du câble et n° de fil en GRAS (gras : largeur x 1,1)
                th = _texte_cote(ch, ph)
                yh_ = y0 - 150
                if kh and (b == "X1" or not th):
                    tc_ = f"{kh[0]} ({kh[1]})" if b == "X1" else "-" + kh[0]
                    g.texte_v(F[fo], xc - 190, yh_, tc_, 160, bold=1)
                    yh_ -= largeur(tc_, 160) * 11 // 10 + 80
                if th:
                    g.texte_v(F[fo], xc - 190, yh_, th[:28 if yh_ == y0 - 150 else 20], 160)
                if n_fil:
                    g.texte_v(F[fo], xc + 30, y0 - 150, n_fil, 160, bold=1)
                # bas : fil, appareil (à gauche), câble et conducteur (à droite)
                g.ligne(F[fo], xc, y1, xc, y1 + ZB - 200, width=10)
                tb = _texte_cote(cb, pb)
                if tb:
                    g.texte_v(F[fo], xc - 190, y1 + 150 + largeur(tb[:28], 160), tb[:28], 160)
                if kb and b != "X1":
                    tk = f"{kb[0]} ({kb[1]})"
                    g.texte_v(F[fo], xc + 30, y1 + 150 + largeur(tk, 160) * 11 // 10, tk, 160, bold=1)
                x += PAS_B
            g.ligne(F[fo], x, y0 - 100, x, y1 + 100, width=60)                # butée de fin
            # v42 (Julien 26/11 : « sous chaque bornier, un petit texte qui note les fonctions des câbles ou fils,
            # résumé simple et concis ») : une ligne par fonction, « n° des bornes : fonction »
            resume_bornier(fo, xb0_, y1 - 100, 2300, b, mo)          # v43 : sous le cadre du repère
            x += 400 + ecart_
    # v38 (Julien 24/11) : note du haut retirée (à retravailler plus tard) ; elle disait : haut = côté intérieur
    # (boîte : côté câble), bas = côté terrain (boîte : côté appareil) ; texte = appareil:broche (folio), n° de fil, câble (conducteur)


# ======================================================================== terre : départs PE de l'arrivée (f10)
# Règle C partout (29/10) : chaque appareil a un fil PE court + renvoi ; ici un départ par appareil,
# dans l'ordre des folios (la barrette de terre -X13 n'est pas dessinée)
f = "10"
PE_DEST.sort(key=lambda d: NUMFOL.get(d[0], d[0]))
# 02/11 : renvois à droite de la chaîne QS1 / QF1 (fils de la chaîne allongés), flèches vers le haut
xs = [10400 + 800 * i for i in range(len(PE_DEST))]
W(f, [PE10, (xs[-1], PE10[1])], "PE")
for x, (fd, pt) in zip(xs, PE_DEST):
    renvoi(f, W(f, [(x, PE10[1]), (x, PE10[1] - 800)], "PE"), fd, pt, "PE")
etiquette(f, xs, PE10[1] - 2800, "Terre PE vers les appareils", 260)
# liaison équipotentielle armoire -> bâti machine (Julien 05/11) : un conducteur V/J seul, 4 mm², repère -W13
xb_ = xs[-1] + 2400
W(f, [(xs[-1], PE10[1]), (xb_, PE10[1]), (xb_, PE10[1] - 1600)], "PE")
g.cable(F[f], xb_ - 400, xb_ + 400, PE10[1] - 1200, "W13", "1 x 4 mm² V/J", "Liaison équipotentielle", [xb_], blinde=False)
texte(f, xb_ - 1200, PE10[1] - 2400, "Bâti machine +M", 220, 0, 1)

# ======================================================================== barres 24 V / 0 V en haut (29/10)
# contenu descendu pour laisser la place aux barres (après la pose de tous les renvois vers ces folios)
# v40 (Julien 25/11 : f42, fil 0 V du bas trop près du cartouche) : f42 descendu de 400 seulement (1200 avant)
for num_, dy_ in (("40", 800), ("42", 400), ("50", 800)):
    g.decaler(F[num_], 0, dy_)
f = "40"
W(f, [k401["A1"], (k401["A1"].x, RAIL24_Y)], "24")
W(f, [k401["A2"], (k401["A2"].x, k401["A2"].y + 400), (3600, k401["A2"].y + 400), (3600, RAIL0_Y)], "0V")
# B2 : référence 0 V des signaux, au 0 V du 24 V PELV (règle R-02, 02/11)
W(f, [k401["B2"], (k401["B2"].x, k401["B2"].y + 400), (k401["A2"].x, k401["A2"].y + 400)], "0V")
texte(f, 4000, k401["A2"].y + 2800, "Réglage -KA1 : FUNCTION 1, START 3", 200)
f = "42"
ybas = max(k["A2"].y for k in COIL.values()) + 800          # collecteur 0 V sous les bobines, remonté à gauche
for k in COIL.values():
    W(f, [k["A2"], (k["A2"].x, ybas)], "0V")
W(f, [(max(k["A2"].x for k in COIL.values()), ybas), (3600, ybas), (3600, RAIL0_Y)], "0V")
renvoi(f, W(f, [(26000, RAIL0_Y), (26000, 4400)], "0V"), "20", VAR[("20", "STO0")], "0V")
texte(f, 23600, 6400, "0 V STO X6.2 de -U1 (f20)", 200)
f = "55"
W(f, [k501a["L+"], (k501a["L+"].x, RAIL24_Y)], "24")
W(f, [k501a["M"], (k501a["M"].x, RAIL0_Y)], "0V")
f = "50"
W(f, [k501e["1M"], (k501e["1M"].x, RAIL0_Y)], "0V")
CH = sorted(["40", "42", "55", "50", "51", "52", "53", "54", "60"], key=lambda n: NUMFOL.get(n, n))   # f41 : pas de piquage
# v37 (D13) : le f21 n'a plus de barres ; celles du f30 (1er folio de la chaîne) partent des blocs -X21.11 / -X21.12
renvoi("31", d31["BAR24"], CH[0], (XL, RAIL24_Y), "24")
renvoi("31", d31["BAR0"], CH[0], (XL, RAIL0_Y), "0V")
FIN = {CH[-1]: (k531["L+"].x, k531["M"].x)}      # dernier folio : barres arrêtées au dernier piquage
for i, f in enumerate(CH):
    x24, x0 = FIN.get(f, (XR, XR))
    W(f, [(XL, RAIL24_Y), (x24, RAIL24_Y)], "24")
    W(f, [(XL, RAIL0_Y), (x0, RAIL0_Y)], "0V")
    if i:
        renvoi(CH[i - 1], (XR, RAIL24_Y), f, (XL, RAIL24_Y), "24")
        renvoi(CH[i - 1], (XR, RAIL0_Y), f, (XL, RAIL0_Y), "0V")
    xt = 24000 if f not in FIN else x0 + 800
    texte(f, xt, RAIL24_Y - 300, "24VELEC", 200)
    texte(f, xt, RAIL0_Y - 300, "0 V", 200)

# ======================================================================== écriture + contrôle
# bus 400 / 230 V, barres 24 V / 0 V et variateurs : en haut du folio, même hauteur partout (30/10) ; centrés en largeur
HAUT = {"12", "13", "14", "20", "21"} | set(CH)
for num in F:                       # contenu centré dans le cadre (pas la garde, la légende, les notes)
    if "10" <= num <= "69":
        g.centrer(F[num], vertical=num not in HAUT)
# retouches de Julien dans WinRelais (v12, v13 du 02/11), reprises en coordonnées finales
POS_JULIEN = {("10", "Distribution (f12, N : f13)"): (6000, 17600), ("12", "VARIATEUR 1"): (4900, 16400),
              ("12", "VARIATEUR 2"): (12000, 16400), ("12", "FREIN M201"): (18300, 16400),
              ("54", "Port 5 : réserve"): (13800, 11500), ("42", "0 V STO X6.2 de -U1 (f20)"): (25700, 6200),
              ("53", "AI1 à AI7 : réserve"): (17400, 11200),
              ("10", "Bâti machine +M"): (19300, 15700), ("40", "Réglage -KA1 : FUNCTION 1, START 3"): (6600, 15300)}
g.textes = [(t[0], *POS_JULIEN[nf]) + tuple(t[3:])
            if (nf := next((n for n in POS_JULIEN if F.get(n[0]) == t[0] and t[3] in (n[1], ren(n[1]))), None)) else t
            for t in g.textes]
# tableaux remontés près des modules (Julien, v13) : (folio, zone x1 y1 x2 y2, dx, dy)
# v37 : plus de déplacement au f62 (le tableau est déjà à sa place ; la zone contient maintenant la boîte +BJM)
for num_, (x1_, y1_, x2_, y2_), dx_, dy_ in (("51", (20700, 15500, 29100, 17200), -4400, -10800),):
    dans = lambda x, y: x1_ <= x <= x2_ and y1_ <= y <= y2_
    g.textes = [(t[0], t[1] + dx_, t[2] + dy_) + tuple(t[3:]) if t[0] == F[num_] and dans(t[1], t[2]) else t
                for t in g.textes]
    g.dessins = [(d[0], d[1] + dx_, d[2] + dy_, d[3] + dx_, d[4] + dy_) + tuple(d[5:])
                 if d[0] == F[num_] and dans(d[1], d[2]) and dans(d[3], d[4]) else d for d in g.dessins]
nommer_phases()


def aligner_numeros_f20():
    """v40 (Julien 25/11 : « numéros de fil au même niveau ») : au f20, numéros verticaux des fils driver -> moteur
    sur 3 rangées (driver / bornes, bornes / câble, boîte / moteur) et numéros horizontaux PUL / DIR / ENA / 0 V
    sur une même colonne, entre le collecteur 0 V et le driver."""
    from xrs_gen import largeur, NUM_T
    f_ = F["32"]
    for D, bornes, BJ, Mo, ic in F20_RANGS:
        xs = {D[p].x for p in ("A+", "A-", "B+", "B-")}
        haut_ = min(s_.pins["1"][0][1] for s_ in bornes)              # haut des bornes d'armoire (rangée du haut)
        bas_ = max(s_.pins["2"][0][1] for s_ in bornes)               # bas des bornes d'armoire (rangée du bas)
        bj_haut = min(b_.pins["1"][0][1] for b_ in BJ)
        bj_bas = max(b_.pins["2"][0][1] for b_ in BJ)
        yc = g.cables[ic][3]
        ydrv = D["A+"].y
        c_a = (ydrv + haut_) / 2
        c_b = (bas_ + yc - 350) / 2                                   # sous les bornes, au-dessus des n° de brin
        c_d = (bj_bas + 200 + Mo["A+"].y - 200) / 2                   # v42 : entre les cadres +BJM et +M (broches dedans)
        nv = []
        for n_ in g.numeros:
            fo, x, y, txt, ang = n_
            if fo == f_ and ang == 90 and x in xs and txt != "PE":
                # rangée du numéro d'après les bornes de SON fil (bornes sur 2 niveaux)
                ba_ = next(s_ for s_ in bornes if s_.pins["1"][0][0] == x)
                bb_ = next(s_ for s_ in BJ if s_.pins["1"][0][0] == x)
                c = c_a if y <= ba_.pins["1"][0][1] else (c_b if ba_.pins["2"][0][1] <= y <= bb_.pins["1"][0][1]
                                                          else (c_d if y >= bb_.pins["2"][0][1] else None))
                if c is not None:
                    y = int(round((c + largeur(txt, NUM_T) / 2) / 100)) * 100
            if fo == f_ and ang == 0 and D["PUL+"].y <= y <= D["ENA-"].y and D["PUL-"].x - 4000 < x < D["PUL-"].x:
                xc = D["PUL-"].x - 400                                # milieu entre le collecteur 0 V et le driver
                x = int(round((xc - largeur(txt, NUM_T) / 2) / 100)) * 100
            nv.append((fo, x, y, txt, ang))
        g.numeros = nv


aligner_numeros_f20()


def aligner_haut_variateurs():
    """v40 (Julien 25/11) : f31 / f32, numéros des fils qui partent des broches du haut du variateur sur une même ligne,
    juste au-dessus des broches (sous les flèches des renvois)."""
    from xrs_gen import largeur, NUM_T
    for T in VARIATEURS:
        yp = min(xy[1] for lst in T.pins.values() for xy in lst)
        xs = {xy[0] for lst in T.pins.values() for xy in lst if xy[1] == yp}
        g.numeros = [(fo, x, yp - 100, txt, ang) if fo == T.folio and ang == 90 and x in xs and yp - 2400 < y < yp + 1
                     else (fo, x, y, txt, ang) for fo, x, y, txt, ang in g.numeros]


aligner_haut_variateurs()
for a_ in NUM_ALERTES:
    print("ATTENTION", a_)
renommer_symboles()
# nomenclature générée (option B, Julien 18/11) : une ligne par appareil, bornes par type, non dessiné, câbles (f90, f91)


def cables_schema():
    """v42 (check complet de la nomenclature, Julien 26/11) : pour chaque câble, folios où il est dessiné et bornes d'armoire
    où il arrive (relus sur le dessin). L'origine de saisie.json est gardée si elle cite les mêmes groupes de bornes."""
    from collections import defaultdict
    fol, born = defaultdict(set), defaultdict(set)
    for c in g.cables:
        fol[c[4]].add(g.num(c[0]))
    for fo, _, _, txt, _ in g.numeros:
        if txt.startswith("PN"):
            fol[txt].add(g.num(fo))
    for (rep_, _), (cab_, _) in _cables_par_borne().items():
        if not rep_.startswith("X1."):
            born[cab_].add(rep_)
    out = {}
    for c in nomenclature._saisie()["cables"]:
        r = c["repere"]
        d = {}
        if fol.get(r):
            d["folio"] = ", ".join(sorted(fol[r], key=nomenclature._naturel))
        if born.get(r):
            diz = defaultdict(list)
            for b_ in born[r]:
                bn, n_ = b_.split(".")
                diz[f"{bn}.{n_[:-1]}"].append(b_)
            vus = {f"{k}x" for k in diz}
            cites = {f"X{a_}.{b_}x" for a_, b_ in re.findall(r"X(\d+)\.(\d)[\dx]", c["origine"])}
            if cites and vus != cites:          # W1 : origine = le réseau du client, gardée
                parts = []
                for k in sorted(diz, key=nomenclature._naturel):
                    bs = sorted(diz[k], key=nomenclature._naturel)
                    parts.append(bs[0] if len(bs) == 1 else (f"{bs[0]} / {bs[1]}" if len(bs) == 2 else f"{bs[0]} à {bs[-1]}"))
                d["origine"] = "+A1 " + ", ".join(parts)
                print(f"câble {r} : origine relue sur le schéma ({c['origine']} -> {d['origine']})")
        if d.get("folio") and d["folio"] != c["folio"]:
            print(f"câble {r} : folio relu sur le schéma ({c['folio']} -> {d['folio']})")
        out[r] = d
    return out


CAB_SCHEMA = cables_schema()
NOMENC_LIGNES = nomenclature.lignes(g, CAB_SCHEMA)
print("nomenclature : taille, ligne, lignes par folio", nomenclature.dessiner(g, _texte, [F["90"], F["91"], F["92"]], NOMENC_LIGNES))
# v40 (Julien 25/11 : police plus grande au f80) : tailles jusqu'à 360, colonnes longues sur 2 lignes si besoin
print("liste des câbles : taille, ligne", nomenclature.tableau_pages(g, _texte, [F["80"]], nomenclature.ENTETE_CABLES,
                                                                     nomenclature.lignes_cables(CAB_SCHEMA), ligne_max=960,
                                                                     tailles=(360, 340, 320, 300, 280, 260, 240), coupe=True))
g.write(SORTIE)
ecrire_borniers(SORTIE)
g.write(SORTIE)
pb_nom, info_nom = nomenclature.controle(SORTIE, {"90", "91", "92"})
pb_nom += nomenclature.controle_cables(SORTIE, "80")
print("nomenclature :", info_nom[0])
for i_ in info_nom[1:]:
    print("   ", i_)
pb = check(g, SORTIE) + controle_specification(SORTIE) + pb_nom
print(f"{len(g.folios)} folios, {len(g.symbols)} symboles, {len(g.wires)} fils, {len(g.renvois)} renvois")
print(f"{len(pb)} problème(s) de contrôle")
for p in pb:
    print(" -", p)
