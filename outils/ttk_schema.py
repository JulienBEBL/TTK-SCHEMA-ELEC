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

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ICI, "..", "schema", "generes", "TTK_genere.xrs")
TABLEAU = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ICI, "..", "livrables", "TTK_Plan_Folios_Reperes.xlsx")
MODELE = os.path.join(ICI, "..", "schema", "modele", "SCHEMA_ELEC_TTK.xrs")

REP = lire_tableau.reperes(TABLEAU)
FOL = lire_tableau.folios(TABLEAU)
# décisions postérieures au classeur (27/10/2026) : le classeur de Julien n'est pas modifié, voir livrables/MAJ_Reperes_2026-10-27.csv
REP["B412"].update({"fab": "ifm MN508S (RS 016-3138)", "carac": "codé - 2 NO + 1 NF - M12 - 24 V 50 mA"})
REP["S413"].update({"fab": "Eaton T0-4-8223/E", "carac": "8 contacts NO 1-2 à 15-16 (ponts d'usine retirés)"})
# f13 séparé en deux (29/10) : f13 alimentations, f14 services armoire ; f43 supprimé (29/10)
FOL.insert(next(i for i, f in enumerate(FOL) if f["num"] == "13") + 1,
           {"num": "14", "titre": "DISTRIBUTION 230 V - SERVICES", "desc": "VENTILATION, ECLAIRAGE, PRISE DE SERVICE",
            "loc": "+A1", "maitres": ""})
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
    "31": "BLOCS -X21.11 24VELEC, -X21.12 0 V, -X21.13 24VSEC ; VOYANT -H3",
    "20": "VARIATEUR -U1, RESISTANCE -R1, MOTEUR -M1 (FREIN, SONDE TF)",
    "21": "VARIATEUR -U2, RESISTANCE -R2, MOTEUR -M2 (FREIN, SONDE TF)",
    "40": "RELAIS -KA1 : ALIMENTATION, BOUCLE DE RETOUR, REARMEMENT -S4, REGLAGES",
    "41": "ARRETS D'URGENCE -S1 / -S2, CAPOT -B1 / -B2, SHUNTS MANU DU SELECTEUR -S3",
    "42": "STO VARIATEURS, CONTACTEURS -KM1 / -KM2, FREINS -KF1 / -KF2, 48 V -KA2",
    "50": "ALIMENTATION CPU & ENTREES : AU, CAPOT, SELECTEUR, FINS DE COURSE, RETOURS",
    "51": "SORTIES RAPIDES CPU : DRIVERS PAS A PAS (PUL / DIR / ENA)",
    "52": "SIGNALISATION : COLONNE LUMINEUSE -H1, VOYANT DEFAUT -H4",
    "70": "BORNES RAIL PAR RAIL : MACHINE, PUPITRE, PORTE, INTERNES",
})
TITRES_FOL = {"13": "DISTRIBUTION 230 V - ALIMENTATIONS", "32": "48 VDC ET MOTEURS PAS A PAS",
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
          "60": "50", "50": "60", "51": "61", "52": "62", "53": "63"}
FOL = sorted((f for f in FOL if f["num"] not in ("03", "11", "30")), key=lambda f: NUMFOL.get(f["num"], f["num"]))
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
    ("X20", 1, "32", "Moteur pas-à-pas M3", "+M", [(f"X701.{33 + i}", p) for i, p in enumerate(("A+", "A-", "B+", "B-"))]),
    ("X20", 2, "32", "Moteur pas-à-pas M4", "+M", [(f"X701.{37 + i}", p) for i, p in enumerate(("A+", "A-", "B+", "B-"))]),
    ("X31", 1, "20", "Moteur M1", "+M", [(f"X701.{17 + i}", p) for i, p in enumerate(("PE", "U", "V", "W"))]),
    ("X31", 2, "20", "Sonde TF M1", "+M", [("X701.21", "1b"), ("X701.22", "2b")]),
    ("X31", 3, "20", "Frein M1", "+M", [("X701.23", "2"), ("X701.24", "3")]),
    ("X32", 1, "21", "Moteur M2", "+M", [(f"X701.{25 + i}", p) for i, p in enumerate(("PE", "U", "V", "W"))]),
    ("X32", 2, "21", "Sonde TF M2", "+M", [("X701.29", "1b"), ("X701.30", "2b")]),
    ("X32", 3, "21", "Frein M2", "+M", [("X701.31", "2"), ("X701.32", "3")]),
    ("X41", 1, "41", "AU pupitre -S2, voies 1 et 2", "+P1", [(f"X711.{n}", "") for n in (1, 2, 3, 4)]),
    ("X41", 2, "41", "Sélecteur -S3 Manu : shunt des capots", "+P1", [(f"X711.{n}", "") for n in (13, 14, 15, 16)]),
    ("X41", 3, "41", "Capot -B1", "+M", [("X701.1", "11"), ("X701.2", "12"), ("X701.3", "23"), ("X701.4", "24")]),
    ("X41", 4, "41", "Capot -B2", "+M", [("X701.5", "11"), ("X701.6", "12"), ("X701.7", "23"), ("X701.8", "24")]),
    # AU armoire -S1 sur la porte (Julien 02/11) : par des bornes en bas de l'armoire, pas de fil direct
    ("X41", 5, "41", "AU armoire -S1 (porte), voies 1 et 2", "porte", [(f"X721.{n}", "") for n in (1, 2, 3, 4)]),
    ("X42", 1, "42", "Sélecteur -S3 : MANU-D, AUTO-A, AUTO-B", "+P1", [(f"X711.{n}", "") for n in (19, 20, 7, 8, 9, 10)]),
    ("X50", 1, "60", "Alimentation IHM -P1", "+P1", [("X711.21", "L+"), ("X711.22", "M"), ("X711.23", "FE")]),
    ("X60", 1, "50", "AU pupitre -S2 (contact NO)", "+P1", [("X711.5", ""), ("X711.6", "")]),
    ("X60", 2, "50", "Sélecteur -S3 Auto / Manu", "+P1", [(f"X711.{n}", "") for n in (11, 12, 17, 18)]),
    ("X60", 3, "50", "Fins de course -B3 à -B6", "+M", [(f"X701.{9 + i}", f"B{3 + i // 2}") for i in range(8)]),
    ("X60", 4, "50", "AU armoire -S1 (porte), contact NO", "porte", [("X721.5", ""), ("X721.6", "")]),
    ("X63", 1, "53", "Thermocouple -B7", "+M", [("X701.41", "+"), ("X701.42", "-")]),
    # 05/11 (Julien) : colonne -H1 par des bornes (câble) ; appareils de porte tous par des bornes, comme -S1
    ("X62", 1, "52", "Colonne -H1", "+M", [("X701.43", "RD"), ("X701.44", "OG"), ("X701.45", "GN"), ("X701.46", "COM")]),
    ("X40", 1, "40", "Réarmement -S4 (porte)", "porte", [("X721.7", ""), ("X721.8", "")]),
    ("X12", 2, "13", "Voyant -H2 230 V (porte)", "porte", [("X721.9", ""), ("X721.10", "")]),
    ("X21", 2, "31", "Voyant -H3 (porte)", "porte", [("X721.11", ""), ("X721.12", "")]),
    ("X62", 2, "52", "Voyant -H4 (porte)", "porte", [("X721.13", ""), ("X721.14", "")]),
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
NUMEROTES = {"10", "12", "13", "14", "32", "31", "54"}   # folios internes (affichés 10 à 13, 20, 21, 30)
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
    ("50", "K501", [("L+ capt", 0, 1)], 0),            # 24 V capteurs (L+ capt CPU -> -X21.14) : 6001
    ("51", "K501", [("Q0.0", 0, 1), ("Q0.1", 0, 2), ("Q0.2", 0, 3), ("Q0.3", 0, 4), ("Q0.4", 0, 5), ("Q0.5", 0, 6)], 0),
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
    for fol, rep_, pins_, dizaine in SOURCES_NUM:
        s_ = next((x for x in g.symbols if x.rep == rep_ and x.folio == F[fol]), None)
        if s_ is None:
            NUM_ALERTES.append(f"numérotation : {rep_} absent du folio {NUMFOL.get(fol, fol)}")
            continue
        for nom, k, unite in pins_:
            pts = s_.pins.get(nom, [])
            if len(pts) <= k:
                NUM_ALERTES.append(f"numérotation : broche {rep_}:{nom}/{k} absente")
                continue
            g_ = g._find(("P", s_.folio) + (pts[k][0], pts[k][1]))
            u = unite if unite is not None else UNITE.get(phase.get(g_))
            if u is None:
                continue                      # broche non câblée
            n_ = f"{NUMFOL.get(fol, fol)}{dizaine + u:02d}"
            if num.setdefault(r(g_), n_) != n_:
                NUM_ALERTES.append(f"numérotation : {rep_}:{nom} -> {n_}, potentiel déjà numéroté {num[r(g_)]}")
    return num, (lambda f_, x, y: r(g._find(("P", f_, x, y))))


def troncon_libre(f_, vertical, pos, lo, hi):
    """Plus longue partie [lo, hi] d'un fil où son numéro (bande de 300 à droite / sous le fil, comme le relit
    xrs_chevauchements) ne touche ni un fil perpendiculaire ni un texte de symbole (13/11)."""
    bloc = []
    for w in g.wires:
        if w[0] != f_:
            continue
        if vertical and w[2] == w[4] and min(w[1], w[3]) < pos + 300 and max(w[1], w[3]) > pos:
            bloc.append((w[2] - 100, w[2] + 100))
        if not vertical and w[1] == w[3] and min(w[2], w[4]) < pos + 300 and max(w[2], w[4]) > pos:
            bloc.append((w[1] - 100, w[1] + 100))
    for s_ in g.symbols:
        if s_.folio != f_:
            continue
        for _, b in s_.texts:
            x1, x2, y1, y2 = min(b[0], b[2]), max(b[0], b[2]), min(b[1], b[3]), max(b[1], b[3])
            if vertical and x1 < pos + 300 and x2 > pos:
                bloc.append((y1 - 100, y2 + 100))
            if not vertical and y1 < pos + 300 and y2 > pos:
                bloc.append((x1 - 100, x2 + 100))
    segs = [(lo, hi)]
    for a, b in bloc:
        segs = [z for c, d in segs for z in ((c, d),) if b <= c or a >= d] + \
               [z for c, d in segs if not (b <= c or a >= d) for z in ((c, a), (b, d)) if z[1] > z[0]]
    return max(segs, key=lambda z: z[1] - z[0]) if segs else (lo, hi)


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
    num_pot, racine_pot = numeros_potentiels(phase)
    numerotes = {F[n_] for n_ in NUMEROTES}
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
    for ws in troncons.values():
        f_ = ws[0][0]
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
        if yb is not None and lignes[yb] >= 6000:
            w = min((w for w in ws if w[2] == w[4] == yb), key=lambda w_: min(w_[1], w_[3]))
            lo, hi = min(w[1], w[3]), max(w[1], w[3])
            poses.append([f_, yb, lo, hi, ph, 0, lo + 800])
            continue
        w = max(ws, key=lambda w_: abs(w_[3] - w_[1]) + abs(w_[4] - w_[2]))
        if w[1:3] == w[3:5]:
            continue
        if w[1] == w[3]:
            lo, hi = min(w[2], w[4]), max(w[2], w[4])
            if f_ in numerotes:
                lo, hi = troncon_libre(f_, True, w[1], lo, hi)
            # le numéro de brin d'un câble s'écrit juste au-dessus du croisement (f20, 30/10) : on reste à l'écart
            for c_ in g.cables:
                if c_[0] == f_ and w[1] in c_[7] and lo < c_[3] < hi:
                    lo, hi = max(((lo, c_[3] - 400), (c_[3] + 100, hi)), key=lambda a: a[1] - a[0])
            poses.append([f_, w[1], lo, hi, ph, 90, (lo + hi) // 2])
        else:
            lo, hi = min(w[1], w[3]), max(w[1], w[3])
            if f_ in numerotes:
                lo, hi = troncon_libre(f_, False, w[2], lo, hi)
            poses.append([f_, w[2], lo, hi, ph, 0, (lo + hi) // 2])
    # alignement (29/10) : fils parallèles voisins (<= 1200) qui se recouvrent sur au moins 400 -> même ligne
    for ang in (0, 90):
        groupes = []
        for p in sorted((p for p in poses if p[5] == ang), key=lambda p: (p[0], p[1])):
            for c in groupes:
                if c[-1][0] == p[0] and 0 < p[1] - c[-1][1] <= 1200 and (c[-1][4] == "PE") == (p[4] == "PE") and \
                        max(q[2] for q in c + [p]) + 400 <= min(q[3] for q in c + [p]):
                    c.append(p)
                    break
            else:
                groupes.append([p])
        for c in groupes:
            lo, hi = max(q[2] for q in c) + 200, min(q[3] for q in c) - 200
            voulu = sum(q[6] for q in c) // len(c)
            demi = max(len(q[4]) for q in c) * 300 * 0.55 / 2     # texte centré (l'ancre est au début du texte)
            if ang == 0 and lo + demi <= hi - demi:               # 13/11 : texte horizontal entier sur son fil
                lo, hi = lo + demi, hi - demi
            mid = min(max(voulu, lo), hi) if lo <= hi else (lo + hi) // 2
            for f_, pos, _, _, ph, _, _ in c:
                if ang == 90:
                    g.numeros.append((f_, pos, int(round((mid + demi) / 100)) * 100, ph, 90))
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
BORNES_PE = {"X101.VJ", "X701.17", "X701.25", "X711.23"}
BORNE_PE = os.path.join(ICI, "librairie", "CUSTOM", "Borne_4mm_terre_vert-jaune.xsy")


def borne(rep, f, x, y, fpos=(100, -250)):
    """Borne 4 mm verticale : broche 1 en (x, y), broche 2 en (x, y + 400). fpos = repère (à droite par défaut).
    Borne de terre vert/jaune pour les repères de BORNES_PE (même géométrie)."""
    bornier = rep.split(".")[0]
    des = DES_BORNE.get(rep) or REP.get(rep, {}).get("des") or REP.get(bornier, {}).get("des", "")
    pe = rep in BORNES_PE
    return g.place(BORNE_PE if pe else BORNE, rep, F[f], x, y, champs={2: des, 4: "borne de terre vert/jaune" if pe else ""}, ref=(),
                   compact=True, rep_size=150, fpos=fpos, loc="A1", prefix="X")


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
texte("01", 4000, 6200, "Client : TTK          Affaire : à compléter          N° machine : 001-EU", 300)
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
IMG = os.path.join(os.path.dirname(ICI), "schema", "images")
for nom_, x_, y_, w_, h_, r_ in (("logo_TTK.jpg", 4500, 12700, 5480, 3480, 1575), ("logo_BEBL.jpg", 11500, 13100, 5806, 2615, 2221),
                             ("logo_LEVERT_INDUSTRIE.jpg", 18600, 13700, 6000, 1308, 4588)):
    g.logos.append((F["01"], x_, y_, w_, h_, os.path.join(IMG, nom_), r_))

rows = [["N°", "Titre", "Description"]] + [[NUMFOL.get(f["num"], f["num"]), f["titre"], ren(f["desc"])] for f in FOL]
g.tableau(F["02"], 1600, 1600, [1600, 9200, 16800], (19200 - 1600) // len(rows), rows, size=260)

# synoptique en logigramme (02/11) : blocs encadrés reliés par des flèches, dans le sens de l'énergie
SY = F["04"]


def bloc(x1, y1, x2, lignes, dashed=False):
    """Cadre + titre en gras + lignes ; rend (x1, y1, x2, y2). Refuse un texte plus large que le cadre."""
    y2 = y1 + 330 * len(lignes) + 300
    g.cadre(SY, x1, y1, x2, y2, width=30, dashed=dashed)
    for i, t in enumerate(lignes):
        sz = 220 if i == 0 else 200
        if len(ren(t)) * sz * 0.55 > x2 - x1 - 400:
            raise SystemExit(f"f04 : texte trop long pour son cadre : {t}")
        texte("04", x1 + 200, y1 + 150 + 330 * i, t, sz, 0, 1 if i == 0 else 0)
    return (x1, y1, x2, y2)


def fleche(pts, dashed=False, tete=True):
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        g.ligne(SY, xa, ya, xb, yb, width=30, dashed=dashed)
    if tete:
        (xa, ya), (xb, yb) = pts[-2], pts[-1]
        dx, dy = (xb > xa) - (xb < xa), (yb > ya) - (yb < ya)
        for k in (-1, 1):
            g.ligne(SY, xb - 250 * dx + 150 * k * dy, yb - 250 * dy + 150 * k * dx, xb, yb, width=30)


C1, C2, C3 = 5600, 14800, 24000                      # colonnes : 400 V moteurs, alimentations, services
col = lambda c: (c - 3800, c + 3800)
res = bloc(*col(C2)[:1], 1600, col(C2)[1], ["ARRIVEE RESEAU (f10)", "3 x 400 V + N + PE - câble client -W1, bornes -X10"])
usa = bloc(*col(C3)[:1], 1600, col(C3)[1], ["VARIANTE USA (option, f10)", "3 x 480 V -> -TR1 15 kVA -> 400 V"], dashed=True)
fleche([(usa[0], 2080), (res[2], 2080)], dashed=True)
pro = bloc(*col(C2)[:1], 3200, col(C2)[1], ["SECTIONNEMENT ET PROTECTION (f10)", "-QS1, -QF1 20 A ; terre PE vers chaque appareil"])
fleche([(C2, res[3]), (C2, pro[1])])
fleche([(C2, pro[3]), (C2, 4800)], tete=False)
fleche([(C1, 4800), (C3, 4800)], tete=False)
for c in (C1, C2, C3):
    fleche([(c, 4800), (c, 5400)])
texte("04", 15000, 4450, "3 x 400 V + N", 200)
d400 = bloc(*col(C1)[:1], 5400, col(C1)[1], ["DISTRIBUTION 400 V (f12)", "-QM1 + -KM1 -> variateur 1", "-QM2 + -KM2 -> variateur 2",
                                             "-QF2 + -KF1, -QF3 + -KF2 -> freins"])
ali = bloc(*col(C2)[:1], 5400, col(C2)[1], ["ALIMENTATIONS (f13)", "-QF4 -> -T1 24VSEC", "-QF5 -> -T2 24VELEC",
                                            "-QF6 -> -T3 48 V ; voyant -H2 ; PELV -X12.11"])
srv = bloc(*col(C3)[:1], 5400, col(C3)[1], ["SERVICES 230 V (f14)", "-QF7 -> ventilateurs -EV1 -EV2 (-X13)", "-QF8 -> éclairage -EL1 -EL2 (-X13)",
                                            "-QF9 -> -QF10 -> prise -XD1"])
var = bloc(*col(C1)[:1], 8400, col(C1)[1], ["VARIATEURS (f20, f21)", "-U1, -U2 MCX91A + résistances -R1 -R2", "STO commandé par la sécurité (f42)"])
pap = bloc(*col(C2)[:1], 8400, col(C2)[1], ["48 V PAS-A-PAS (f32)", "-KA2 coupe les 2 x +48 V", "drivers -U3 / -U4"])
d24 = bloc(*col(C3)[:1], 8400, col(C3)[1], ["DISTRIBUTION 24 V (f31)", "-X21.11 24VELEC, -X21.13 24VSEC", "-X21.12 0 V commun, voyant -H3"])
fleche([(C1, d400[3]), (C1, var[1])])
fleche([(C2, ali[3]), (C2, pap[1])])
texte("04", C2 + 200, 7400, "48 V", 200)
fleche([(17800, ali[3]), (17800, 7800), (22400, 7800), (22400, d24[1])])
texte("04", 19200, 7400, "24 V", 200)
mot = bloc(*col(C1)[:1], 10800, col(C1)[1], ["MOTOREDUCTEURS -M1 / -M2 (+M)", "câbles -W2 à -W6 : moteur, frein, sonde TF"])
mpp = bloc(*col(C2)[:1], 10800, col(C2)[1], ["MOTEURS PAS-A-PAS -M3 / -M4 (+M)", "Nema 34 - 6 A"])
fleche([(C1, var[3]), (C1, mot[1])])
fleche([(C2, pap[3]), (C2, mpp[1])])
# consommateurs 24 V
F4 = [(2000, 8000), (8800, 14800), (15600, 21600), (22400, 28400)]
cx = [(a + b) // 2 for a, b in F4]
fleche([(C3, d24[3]), (C3, 12600)], tete=False)
fleche([(cx[0], 12600), (cx[-1], 12600)], tete=False)
for c in cx:
    fleche([(c, 12600), (c, 13200)])
texte("04", C3 + 200, 11000, "24 V / 0 V", 200)
sec = bloc(F4[0][0], 13200, F4[0][1], ["SECURITE (f40-f42)", "relais -KA1, AU -S1 -S2, capots -B1 -B2", "coupe -KM -KF -KA2, STO -U1 -U2"])
api = bloc(F4[1][0], 13200, F4[1][1], ["AUTOMATE (f50-f53)", "-K1 CPU 1214C, -K2 SM 1223", "-K3 SM 1231 TC (thermocouple -B7)"])
swi = bloc(F4[2][0], 13200, F4[2][1], ["SWITCH PROFINET (f54)", "-K4 : -K1, -U1, -U2, -P1"])
pup = bloc(F4[3][0], 13200, F4[3][1], ["PUPITRE +P1 (f60)", "IHM -P1 KTP700", "AU -S2, sélecteur -S3"])
# PROFINET (pointillés)
fleche([(cx[2], swi[3]), (cx[2], 15200)], dashed=True, tete=False)
fleche([(cx[1], 15200), (cx[3], 15200)], dashed=True, tete=False)
fleche([(cx[1], 15200), (cx[1], api[3])], dashed=True)
fleche([(cx[3], 15200), (cx[3], pup[3])], dashed=True)
texte("04", 19000, 15300, "PROFINET (et -U1, -U2 : f20, f21)", 200)
ter = bloc(2000, 16000, 28400, ["BORNIERS (f70, f71)", "vers la machine +M : -X20, -X31, -X32, -X41, -X60, -X62, -X63",
                                 "vers le pupitre +P1 : -X41, -X42, -X50, -X60"])
fleche([(cx[0], sec[3]), (cx[0], ter[1])])
fleche([(10400, api[3]), (10400, ter[1])])

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
# arrivée réseau dans un cadre (demande du 29/10)
g.cadre(F[f], 3200, 1300, 9800, 2000, width=20, dashed=True)     # pointillé (Julien, 02/11)
texte(f, 3400, 1400, "ARRIVEE RESEAU 3 x 400 V + N + PE - 50 Hz", 250, 0, 1)
for x, t in ((4400, "PE"), (5200, "N"), (6000, "L1"), (6800, "L2"), (7600, "L3")):
    texte(f, x - 150, 1700, t, 200)
xb = {"X101.VJ": 4400, "X101.1": 5200, "X101.2": 6000, "X101.3": 6800, "X101.4": 7600}
B = {r: borne(r, f, x, 4400) for r, x in xb.items()}     # 13/11 : 3600 -> 4400 (arrivée aérée, Julien)
for r, x in xb.items():
    W(f, [(x, 2000), B[r]["1"]], "PE" if r.endswith("VJ") else ("N" if x == 5200 else "L"))
g.cable(F[f], 4000, 8000, 2400, "W101", "5G4", "Câble client", [4400, 5200, 6000, 6800, 7600])
q101 = maitre(C + "Legrand_Vistop_022515_4P_63A.xsy", "Q101", f, 5200, 6000)
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
q135 = maitre(C + "Schneider_A9P71606_iDT40K_disjoncteur_1PN_6A_C.xsy", "Q135", f, 20000, 8800)
x131 = maitre(C + "Legrand_004280_prise_2P+T_16A.xsy", "X131", f, 20000, 13200)
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
e132 = maitre(lampe, "E132", f, 4400, 13600, fpos=(2400, -300))
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
for f, t, r, m, w1, w2, w3, km, qf in (("20", "T201", "R201", "M201", "W201", "W202", "W203", "KM1", "Q421"),
                                       ("21", "T211", "R211", "M211", "W211", "W212", "W213", "KM2", "Q422")):
    # variateur remonté, moteur dans l'axe de X2 (fils droits), câbles W sur une seule ligne (30/10)
    T = maitre(mcx, t, f, 4000, 5200, wrap=34)
    R = maitre(res, r, f, 8400, 8800, shown=(2,), wrap=22)        # 2000 plus à gauche (Julien, v12)
    # symbole modifié par Julien le 02/11 : moteur, sonde TF, frein BE5 dans un même cadre, origine sur U1
    M = maitre(mot, m, f, 4800, 15200, fpos=(10800, 0), wrap=36, noms=False)   # textes à droite du symbole
    YC = 14000                                                     # ligne des 3 câbles moteur
    # bornier armoire -> machine (02/11) : une borne par conducteur, sur une ligne, dans l'axe des broches du moteur
    BM = {p: borne(nb, f, M[p].x, 12800) for p, nb in zip(("PE", "U1", "V1", "W1", "1b", "2b", "2", "3"), BORNES_MOT[m])}
    for p in BM:
        W(f, [BM[p]["2"], M[p]], "PE" if p == "PE" else ("L" if p in ("U1", "V1", "W1", "2", "3") else "PDC"))   # TF : Autre tension DC (13/11)
    for p, kp in (("X1:L1", "2/T1"), ("X1:L2", "4/T2"), ("X1:L3", "6/T3")):
        renvoi("12", out12[(km, kp)], f, stub(f, (T[p].x, 4000), T[p], "L"), "L")
    # terre (29/10) : PE moteur -> X2 PE du variateur ; X1 PE -> fil court + renvoi vers la terre (f10)
    PE_DEST.append((f, W(f, [T["X1:PE"], (4000, 4000)], "PE")))
    W(f, [T["X2:PE"], BM["PE"]["1"]], "PE")
    W(f, [T["X2:U"], BM["U1"]["1"]], "L")
    W(f, [T["X2:V"], BM["V1"]["1"]], "L")
    W(f, [T["X2:W"], BM["W1"]["1"]], "L")
    g.cable(F[f], 0, 0, YC, w1, "4G2,5 blindé", f"Moteur {m} -> {t} X2", [M[p].x for p in ("PE", "U1", "V1", "W1")], ovale=True,
            compo_dx=-2300)                     # compositions sous l'ovale, placées comme Julien au f31 (02/11)
    W(f, [T["X2:-R"], (8000, 8400), (R["1"].x, 8400), R["1"]], "PDC")
    W(f, [T["X2:+R"], (7200, 10800), (R["2"].x, 10800), R["2"]], "PDC")
    # frein (2G1,5) et sonde TF (2 x 0,75 blindé, Julien 02/11) : câbles séparés, par le bornier (02/11)
    # frein (02/11) : les 2 fils remontent avant de partir à droite (plus de fil ni de renvoi sur le repère de la borne) ;
    # broche 2 au-dessus de la broche 3, renvois décalés en x (pas de recouvrement des flèches)
    renvoi("12", out12[(qf, "4/T2")], f, W(f, [BM["2"]["1"], (M["2"].x, 12000), (16800, 12000)], "L"), "L")
    renvoi("12", out12[(qf, "6/T3")], f, W(f, [BM["3"]["1"], (M["3"].x, 12400), (14400, 12400)], "L"), "L")
    # sonde TF : remonte à droite du variateur vers X10 (1b -> X10:1 impose un croisement)
    W(f, [BM["1b"]["1"], (M["1b"].x, 11600), (21600, 11600), (21600, 3600), (11600, 3600), T["X10:1"]], "PDC")   # TF : Autre tension DC (règle 20, contrôle du 13/11)
    W(f, [BM["2b"]["1"], (M["2b"].x, 11200), (21200, 11200), (21200, 4000), (12000, 4000), T["X10:2"]], "PDC")   # TF : Autre tension DC (règle 20, contrôle du 13/11)
    VAR[(f, "PN")] = W(f, [T["X40"], (13600, 4800), (16000, 4800)], "PN")
    g.cable(F[f], 0, 0, YC, w3, "2x0,75 blindé", f"Sonde TF {m} (1b-2b) -> {t} X10", [M["1b"].x, M["2b"].x], ovale=True, compo_dx=-1600)
    # freins M1 + M2 : UN SEUL câble -W4 (W202) LIYCY-JZ 5G1,5 blindé (05/11, W7 supprimé) : conducteurs 1-2 au f31,
    # 3-4 au f32 ; V/J vers le bornier de terre -XPE1 et la boîte de dérivation côté machine
    g.cable(F[f], 0, 0, YC, "W202", "5G1,5 blindé", f"Freins M1 + M2 (2-3), 400 V CA -> {qf}", [M["2"].x, M["3"].x], ovale=True,
            compo_dx=-1700, nums=(1, 2) if f == "20" else (3, 4))
    VAR[(f, "24")] = W(f, [T["X5:24V"], (7600, 4800)], "24")
    VAR[(f, "0V")] = W(f, [T["X5:GND"], (8000, 3200)], "0V")
    # X6 confirmé par Julien (05/11, notice SEW) : X6.1 / X6.3 = F_STO_P (+24 V), X6.2 / X6.4 = F_STO_M (0 V),
    # X6.5 VO24_STO / X6.6 GND (alimentation interne, seulement si le réseau est présent) : non utilisés
    # STO en chaîne (Julien 06/11, validé SEW) : KA1 (AUTO-B) -> -U1 X6.1, 0 V -> -U1 X6.2 ;
    # -U1 X6.3 / X6.4 repartent vers -U2 X6.1 / X6.2 ; -U2 X6.3 / X6.4 libres (fin de chaîne)
    VAR[(f, "STO1")] = W(f, [T["X6:1"], (8800, 4800)], "24")
    if f == "20":
        W(f, [T["X6:2"], (9200, 4800), (10400, 4800)], "0V")
        VAR[(f, "STO0")] = W(f, [(10400, 4800), (10400, 4000)], "0V")
        VAR[(f, "STOout+")] = W(f, [T["X6:3"], (9600, 3200)], "24")
        VAR[(f, "STOout0")] = W(f, [T["X6:4"], (10000, 4400), (11200, 4400), (11200, 3600)], "0V")   # renvoi écarté des autres
    else:
        VAR[(f, "STOin0")] = W(f, [T["X6:2"], (9200, 4800), (10400, 4800), (10400, 4000)], "0V")
        renvoi("20", VAR[("20", "STOout+")], f, VAR[(f, "STO1")], "24")
        renvoi("20", VAR[("20", "STOout0")], f, VAR[(f, "STOin0")], "0V")
    texte(f, 22400, 4400, "X40 : PROFINET (f54)", 200)
    texte(f, 22400, 4800, "X5 : 24VELEC (f31) - X6 : STO (f42)", 200)
    texte(f, 22400, 5200, "TF X10 : bornes à confirmer", 200, ROUGE)
    texte(f, 22400, 5600, "(notice SEW MCX91A)", 200, ROUGE)
    texte(f, 22400, 6400, f"{w1} / {w3} blindés : blindage repris à 360°", 200)
    texte(f, 22400, 6800, "(presse-étoupe CEM côté moteur,", 200)
    texte(f, 22400, 7200, "collier de masse côté variateur)", 200)
    texte(f, 22400, 8000, "-W4 : un seul câble 5G1,5 blindé pour les 2 freins,", 200)
    texte(f, 22400, 8400, "conducteurs 1-2 = M1 (f20), 3-4 = M2 (f21),", 200)
    texte(f, 22400, 8800, "V/J -> -XPE1 et boîte de dérivation (machine)", 200)

# ======================================================================== 31 DISTRIBUTION 24 V
# barres 24VELEC / 0 V en haut (tracées avec la chaîne, plus bas) ; -X31 et -X32 s'y piquent
f = "31"
# 05/11 (Julien) : 3 blocs Phoenix PTFIX 6/12X2,5 (3273354) à la place des PTFIX 6X1,5 : 1 entrée E + 12 départs
# (1 à 6 en haut, 7 à 12 en bas) ; couleurs prises dans le stock de Julien (RD, BK, GY, BU)
ptf = os.path.join(ICI, "librairie", "CUSTOM", "Phoenix_3273354_PTFIX_6-12x2.5.xsy")
DESC31 = {"X311": ("Distribution 24VELEC", "rouge"), "X312": ("Distribution 0 V", "bleu"),
          "X313": ("Distribution 24VSEC", "gris")}
P31 = {}
for rep_, x, y in (("X311", 6000, 4800), ("X313", 6000, 9600), ("X312", 6000, 14400)):
    P31[rep_] = g.place(ptf, rep_, F[f], x, y, champs={2: DESC31[rep_][0], 3: "Phoenix 3273354 PTFIX 6/12X2,5",
                                                     4: f"1 entrée + 12 départs - {DESC31[rep_][1]}"}, loc="A1", wrap=34,
                        ref=("PHOENIX CONTACT", "", "3273354"))
    g.cadre(F[f], 13200, y - 1200, 19600, y + 1800, width=10, dashed=True)
    # image du bornier (Julien, v25 du 13/11 : 2997 x 3000 en (14900, haut du cadre)) ; même bloc pour les 3
    img_, ratio_ = {"X311": ("Phoenix_PTFIX_6-12x2.5_rouge.jpg", 1233), "X313": ("Phoenix_PTFIX_6-12x2.5_gris.jpg", 1166),
                    "X312": ("Phoenix_PTFIX_6-12x2.5.jpg", 999)}[rep_]          # rouge 24VELEC, gris 24VSEC, bleu 0 V
    h_ = 2600
    w_ = h_ * ratio_ // 1000
    g.logos.append((F[f], 16400 - w_ // 2, y - 1000, w_, h_, os.path.join(os.path.dirname(ICI), "schema", "images", img_), ratio_))
x311, x312, x313 = P31["X311"], P31["X312"], P31["X313"]
W(f, [(XL, 4400), (6000, 4400), x311["E"]], "24")
W(f, [(XL, 9200), (6000, 9200), x313["E"]], "24")
W(f, [(XL, 13200), (6000, 13200), x312["E"]], "0V")
renvoi("13", s24, f, (XL, 4400), "24")
renvoi("13", a24, f, (XL, 9200), "24")
renvoi("13", z30, f, (XL, 13200), "0V")
W(f, [x311["1"], (x311["1"].x, RAIL24_Y)], "24")
W(f, [x312["1"], (x312["1"].x, 13600), (12400, 13600), (12400, RAIL0_Y)], "0V")     # à droite des textes des blocs


d31 = {"24V20": W(f, [x311["12"], (x311["12"].x, 6400), (8800, 6400)], "24"),
       "24V21": W(f, [x311["11"], (x311["11"].x, 7200), (8800, 7200)], "24"),
       "0V32a": W(f, [x312["6"], (x312["6"].x, 14000), (8800, 14000)], "0V"),
       "0V20": W(f, [x312["12"], (x312["12"].x, 16000), (8800, 16000)], "0V"),
       "0V21": W(f, [x312["11"], (x312["11"].x, 16800), (8800, 16800)], "0V"),
       "0V32b": W(f, [x312["10"], (x312["10"].x, 17600), (8800, 17600)], "0V")}
d31["CMD40"] = W(f, [x313["12"], (x313["12"].x, 11200), (8800, 11200)], "24")
d31["CMD52"] = W(f, [x313["11"], (x313["11"].x, 12000), (8800, 12000)], "24")
for ff in ("20", "21"):
    renvoi(f, d31["24V" + ff], ff, VAR[(ff, "24")], "24")
    renvoi(f, d31["0V" + ff], ff, VAR[(ff, "0V")], "0V")
# 16/11 (Julien) : 4e bloc PTFIX 6/12, noir : 24 V capteurs, alimenté par L+ capt de la CPU (400 mA, protégé) ;
# 12 départs vers les 13 points des entrées (KM1 13 et KM2 13 reliés par un pont court)
x314 = g.place(ptf, "X314", F[f], 21600, 12000, champs={2: "Distribution 24 V capteurs (L+ capt CPU)",
               3: "Phoenix 3273354 PTFIX 6/12X2,5", 4: "1 entrée + 12 départs - noir"}, loc="A1", wrap=30,
               ref=("PHOENIX CONTACT", "", "3273354"))
d31["LPC_E"] = W(f, [x314["E"], (21600, 10400)], "24")
d31["LPC_S"] = W(f, [x314["12"], (x314["12"].x, 14400)], "24")
REP["P512"] = {"des": "Voyant porte : tension de commande présente", "fab": "À définir", "carac": "24 V CC - blanc ou vert", "loc": "+A1"}
p512 = decrit("Signalisation et voyants\\Voyant.xsy", "P512", f, 20800, 4400, "Voyant porte : 24VELEC présent",
              fpos=(600, 400), wrap=20, prefix="P")
bh3a, bh3b = borne("X721.11", f, 20800, 3200), borne("X721.12", f, 20800, 7200)     # porte (05/11) ; 13/11 : 6400 -> 7200 (place du n° 1230)
W(f, [(20800, RAIL24_Y), bh3a["1"]], "24")
W(f, [bh3a["2"], p512["X1"]], "24")
W(f, [p512["X2"], bh3b["1"]], "0V")
W(f, [bh3b["2"], (20800, 8000), (20000, 8000), (20000, RAIL0_Y)], "0V")

# ======================================================================== 32 48 V ET PAS-A-PAS
# 02/11 : -T3 sur f13 ; ici 2 arrivées +48 V et 2 arrivées 0 V 48 (un + et un - par driver), sans bornier.
# Les 2 +48 V passent chacun par un pôle de -KA2 (1-2 -> -U3, 3-4 -> -U4) ; 0 V 48 non coupé.
f = "32"
REP["Q423"]["des"] = "Contacteur auxiliaire : coupure du +48 V des drivers"
q423p = contacteur(poles, "Q423", f, 5200, 5600)
A48 = {"-U4": W(f, [(XL, 2800), (24000, 2800)], "PDC"),
       "+U4": W(f, [(XL, 3600), (q423p["3/L2"].x, 3600), q423p["3/L2"]], "PDC"),
       "+U3": W(f, [(XL, 4400), (q423p["1/L1"].x, 4400), q423p["1/L1"]], "PDC")}
for cle in ("-U4", "+U4", "+U3"):
    renvoi("13", d48[cle], f, (XL, {"-U4": 2800, "+U4": 3600, "+U3": 4400}[cle]), "PDC")
drv = C + "Jkongmotor_JKDM860H_driver_pas-a-pas.xsy"
mpp = C + "StepperOnline_34IP65-85_moteur_pas-a-pas.xsy"
CMD32, DRV = {}, {}
for T, Mrep, x0 in (("T322", "M321", 12000), ("T323", "M322", 23200)):
    # drivers remontés de 1600 le 02/11 : place pour les fils driver -> bornier et pour le câble blindé bornier -> moteur
    D = maitre(drv, T, f, x0, 10000, fpos=(2600, 0), wrap=22, noms=False)
    Mo = maitre(mpp, Mrep, f, x0 - 800, 17200, noms=False)
    DRV[T] = D
    # moteurs hors armoire (02/11) : bornier entre driver et moteur ; broches à 400 -> bornes sur 2 niveaux
    for p, nb in zip(("A+", "A-", "B+", "B-"), BORNES_MOT[Mrep]):
        haut = p.endswith("+")
        # 02/11 : bornes à 800 sous le driver, câble à mi-chemin entre les bornes et le moteur
        b = borne(nb, f, D[p].x, 14000 if haut else 14800, fpos=(-600, -250) if haut else (100, -250))   # 13/11 : +400 (place des numéros)
        W(f, [D[p], b["1"]], "PDC")
        W(f, [b["2"], Mo[p]], "PDC")
    # un câble blindé par moteur, du bornier au moteur (Julien 02/11) ; section à définir
    g.cable(F[f], 0, 0, 16000, {"M321": "W321", "M322": "W322"}[Mrep], "4 cond. blindé",
            f"Moteur pas-à-pas {Mrep} -> {T}", [Mo[p].x for p in ("A+", "A-", "B+", "B-")], ovale=True, compo_dx=-2000)
    xin, xbus = x0 - 4000, x0 - 3200
    for s in ("PUL", "DIR", "ENA"):
        CMD32[(T, s)] = W(f, [D[s + "+"], (xin, D[s + "+"].y)], "24")
        W(f, [D[s + "-"], (xbus, D[s + "-"].y)], "0V")
    CMD32[(T, "0V")] = W(f, [(xbus, D["PUL-"].y), (xbus, D["ENA-"].y + 800)], "0V")
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
k401 = maitre(C + "Schneider_XPSUAF13AP_relais_securite.xsy", "K401", f, 4400, 8000)
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
O40 = {p: W(f, [k401[p], (k401[p].x, 11200)], "24") for p in ("14", "24", "34")}
miroir = C + "Schneider_LC1D09BD_contact_aux_NC_21-22_miroir.xsy"
prev = W(f, [k401["Y1"], (8400, 3200), (20000, 3200)], "24")
DESC_KM = {"KM1": "contacteur amont variateur 1", "KM2": "contacteur amont variateur 2",
           "Q421": "contacteur frein M1", "Q422": "contacteur frein M2", "Q423": "contacteur auxiliaire 48 V"}
for i, rep in enumerate(DESC_KM):
    c = decrit(miroir, rep, f, 20000, 3200 + 2400 * i, f"Retour {DESC_KM[rep]}",
               prefix="KM" if rep.startswith("KM") else "Q", wrap=24, fpos=(2200, 200))
    if i:
        W(f, [prev, c["21"]], "24")
    prev = c["22"]
REP["S414"].update({"des": "Bouton de réarmement", "fab": "Schneider XB4BA21", "carac": "1 NO - noir - non lumineux"})   # 03/11
s414 = maitre("BP & Commut & Voyants\\BP Affleurant Noir.xsy", "S414", f, 20000, 15600, prefix="S", fpos=(-2000, 0), wrap=16,
              ref=("SCHNEIDER ELECTRIC", "", "XB4BA21"))
# S4 sur la porte : une borne avant, une sur le retour (05/11)
bs4a, bs4b = borne("X721.7", f, 20000, 14800), borne("X721.8", f, 21600, 16400)
W(f, [prev, bs4a["1"]], "24")
W(f, [bs4a["2"], s414["3"]], "24")
# retour vers Y2 par la droite de la chaîne, au-dessus de Y1 (un seul croisement, avec Y1)
W(f, [s414["4"], (20000, 17600), (21600, 17600), bs4b["2"]], "24")
W(f, [bs4b["1"], (21600, 2800), (9200, 2800), k401["Y2"]], "24")
# Z1 (diagnostic, non sécuritaire) -> I1.5 de l'automate (Julien 02/11)
Z1_40 = W(f, [k401["Z1"], (k401["Z1"].x, k401["Z1"].y + 800)], "24")
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
VOIES = {}
for voie, x, s1, s2, cap, capxsy, bornes, src, ret, byp, porte in (
        (1, 7200, "S411", "S412", "B411", C + "RSPRO_902-6874_interrupteur_position.xsy",
         ("X711.1", "X711.2", "X701.1", "X701.2", "X701.3", "X701.4"), "S11", "S12", (3, ("X711.13", "X711.14")),
         ("X721.1", "X721.2")),
        (2, 17200, "S411", "S412", "B412", C + "ifm_MN508S_capteur_magnetique_code.xsy",
         ("X711.3", "X711.4", "X701.5", "X701.6", "X701.7", "X701.8"), "S21", "S22", (7, ("X711.15", "X711.16")),
         ("X721.3", "X721.4"))):
    # AU armoire -S1 sur la porte (02/11) : une borne avant et une après son contact ; le reste descend de 1200
    D = 1600
    da = borne(porte[0], f, x, 4400)
    top = stub(f, (x, 4000), da["1"], "24")
    if voie == 1:
        c1 = maitre(au, s1, f, x, 5200, prefix="S", ref=("SCHNEIDER ELECTRIC", "", "XB5AS8442 + ZBE102 + ZBE101"))   # AU : réf. du 03/11
        c2 = maitre(au, s2, f, x, 8000 + D, prefix="S", ref=("SCHNEIDER ELECTRIC", "", "XB5AS8442 + ZBE102 + ZBE101"))
        p1, p2 = ("1", "2"), ("1", "2")
    else:
        c1 = decrit(nc2, s1, f, x, 5200, "AU armoire - 2e contact NF (voie 2)")
        c2 = decrit(nc2, s2, f, x, 8000 + D, "AU pupitre (+P1) - 2e contact NF (voie 2)")
        p1, p2 = ("21", "22"), ("21", "22")
    db = borne(porte[1], f, x, 7600)
    ta, tb, tc, td, te, tf = bornes
    b1, b2 = borne(ta, f, x, 6800 + D), borne(tb, f, x, 10400 + D)
    b3, b4 = borne(tc, f, x, 11600 + D), borne(td, f, x, 15200 + D)
    cp = maitre(capxsy, cap, f, x, 12800 + D)
    for a_, b_ in ((da["2"], c1[p1[0]]), (c1[p1[1]], db["1"]), (db["2"], b1["1"]),
                   (b1["2"], c2[p2[0]]), (c2[p2[1]], b2["1"]), (b2["2"], b3["1"]),
                   (b3["2"], cp["11"]), (cp["12"], b4["1"])):
        W(f, [a_, b_], "24")
    bot = stub(f, (x, 16400 + D), b4["2"], "24")
    # pontage du capot par -S413 position Manu (contact NO en parallèle de la chaîne -X701 / capot)
    n_c, (bya, byb) = byp
    xb = x - 3200
    ba, bb = borne(bya, f, xb, 11600 + D), borne(byb, f, xb, 15200 + D)
    ctc = decrit(CT[n_c], "S413", f, xb, 12800 + D, f"MANU-{'AB'[voie - 1]} : shunt capot voie {voie}", wrap=12)
    W(f, [(x, 11200 + D), (xb, 11200 + D), ba["1"]], "24")
    W(f, [ba["2"], ctc[str(n_c)]], "24")
    W(f, [ctc[str(n_c + 1)], bb["1"]], "24")
    W(f, [bb["2"], (xb, 16000 + D), (x, 16000 + D)], "24")
    renvoi("40", S40[src], f, top, "24")
    renvoi("40", S40[ret], f, bot, "24")
    # contact NO du capot -> automate (f50) ; borne du bas descendue de 400 (Julien, v13)
    t1, t2 = borne(te, f, x + 800, 12000 + D), borne(tf, f, x + 800, 14800 + D + 400)
    plus = W(f, [t1["1"], (x + 800, 11600 + D), (x + 2800, 11600 + D)], "24")
    W(f, [t1["2"], cp["23"]], "24")
    W(f, [cp["24"], t2["1"]], "24")
    entree = W(f, [t2["2"], (x + 800, 16400 + D), (x + 2800, 16400 + D)], "24")
    VOIES[cap] = (plus, entree)
# -S414 (réarmement) déplacé au f40 (Julien 02/11) ; tête du sélecteur placée comme Julien (v13)
maitre("Poussoirs et commutateurs\\Tête 2 pos fixes NO.xsy", "S413", f, 24400, 10800, prefix="S", fpos=(600, 0), ref=("EATON", "", "T0-4-8223/E"))

# ======================================================================== 42 SECURITE - SORTIES
# Architecture du 27/10 (fiche de Julien) :
#   sortie 1 (13-14) -> bobines freins -Q421 / -Q422, et via Manu-D -> bobine -Q423 (48 V en Manu seulement)
#   sortie 2 (23-24) -> Auto-A -> bobines -KM1 / -KM2 (pas d'ordre automate, option A du 27/10)
#   sortie 3 (33-34) -> Auto-B -> STO de -U1, puis -U2 en chaîne par X6.3 / X6.4 de -U1 (06/11)
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
    COIL[rep] = k            # A2 : collecteur 0 V tracé après le décalage du folio
# --- sortie 1 : freins (toujours, seul l'AU les coupe) et 48 V (Manu-D)
s1 = (4400, 4000)
W(f, [s1, COIL["Q421"]["A1"]], "24")
W(f, [(4400, 4800), (11200, 4800)], "24")
W(f, [(7600, 4800), COIL["Q422"]["A1"]], "24")
t1, t2 = chaine_s413(11200, "X711.19", "X711.20", 15, "MANU-D : 48 V en Manu seulement", y0=5600)
W(f, [(11200, 4800), t1["1"]], "24")
W(f, [t2["2"], COIL["Q423"]["A1"]], "24")
renvoi("40", O40["14"], f, s1, "24")
texte(f, 4800, 3000, "Sortie 1 (13-14) : freins + 48 V", 220, 0, 1)
# --- sortie 2 : Auto-A -> -KM1 / -KM2 (pas d'ordre automate, décision du 27/10, option A)
t1, t2 = chaine_s413(15200, "X711.7", "X711.8", 1, "AUTO-A : commande -KM1 / -KM2")
s2 = stub(f, (15200, 4000), t1["1"], "24")
W(f, [t2["2"], COIL["KM1"]["A1"]], "24")
W(f, [(15200, 12000), (18400, 12000), COIL["KM2"]["A1"]], "24")
renvoi("40", O40["24"], f, s2, "24")
texte(f, 15600, 3000, "Sortie 2 (23-24) : -KM1 / -KM2", 220, 0, 1)
# --- sortie 3 : Auto-B -> STO des 2 variateurs (validé SEW)
t1, t2 = chaine_s413(21600, "X711.9", "X711.10", 5, "AUTO-B : autorisation STO")
s3 = stub(f, (21600, 4000), t1["1"], "24")
W(f, [t2["2"], (21600, 10400)], "24")
renvoi("40", O40["34"], f, s3, "24")
renvoi(f, (21600, 10400), "20", VAR[("20", "STO1")], "24")
texte(f, 22000, 3000, "Sortie 3 (33-34) : STO", 220, 0, 1)
texte(f, 21200, 12400, "STO : -U1 X6.1 / X6.2, puis -U2", 200)
texte(f, 21200, 12700, "en chaîne par -U1 X6.3 / X6.4 (validé SEW)", 200)
# 0 V des STO (X6:2 / X6:4) : piqués sur la barre 0 V du haut, après le décalage du folio

# ======================================================================== 50 AUTOMATE ENTREES
f = "50"
k501e = maitre(C + "Siemens_6ES7214-1AH50-0XB0_CPU1214C_G2_alim_entrees.xsy", "K501", f, 4800, 12000, wrap=30)
# L+, M et 1M : raccordés aux barres du haut après le décalage du folio
PE_DEST.append((f, W(f, [k501e["FE"], (6400, 10400)], "PE")))
LPC50 = W(f, [k501e["L+ capt"], (7200, 8800)], "24")             # vers l'entrée de -X21.14 (f21)
W(f, [(7200, 4000), (7200, 3200), (23600, 3200)], "24")          # départs de -X21.14 : un fil par point
renvoi(f, LPC50, "31", d31["LPC_E"], "24")
renvoi("31", d31["LPC_S"], f, (7200, 4000), "24")
texte(f, 10000, 2600, "Départs du bloc -X314 (noir, f31) : un fil par point ; -KM1 13 et -KM2 13 reliés par un pont", 180)
W(f, [(22400, 3200), (22400, 4000)], "24")
renvoi(f, (23600, 3200), "41", VOIES["B411"][0], "24")
renvoi(f, (22400, 4000), "41", VOIES["B412"][0], "24")
fdc = "Contacts Fin de course et rupteurs\\Fin de course NO.xsy"
nom = "--- X Contact\\RC Contact NO 13-14.xsy"


def entree(inp, row, elems):
    """elems : liste de (type, repère, fichier, description, broches) du haut vers le bas."""
    p = k501e[inp]
    x = p.x
    # alignement de Julien (30/10) : bornes sur 2 lignes (haut, bas), contacts sur 2 niveaux en quinconce
    y = 4800 if row == 1 else 7200
    yt1, yt2 = 3600, 10400
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


nom = "--- X Contact\\RC Contact NO 13-14.xsy"
entree("I0.0", 1, [("borne", "X711.5", None, None, None),
                   ("esclave", "S412", nom, "AU pupitre - contact NO", ("13", "14")),
                   ("borne", "X711.6", None, None, None)])
entree("I0.1", 2, [("borne", "X721.5", None, None, None),
                   ("esclave", "S411", nom, "AU armoire - contact NO", ("13", "14")),
                   ("borne", "X721.6", None, None, None)])
entree("I0.4", 1, [("borne", "X711.11", None, None, None),
                   ("esclave", "S413", CT[9], "AUTO-C : info Auto", ("9", "10")),
                   ("borne", "X711.12", None, None, None)])
entree("I0.5", 2, [("borne", "X711.17", None, None, None),
                   ("esclave", "S413", CT[11], "MANU-C : info Manu", ("11", "12")),
                   ("borne", "X711.18", None, None, None)])
FDC = {"I0.6": ("B501", "Fin de course axe 1 min", 1, "X701.9", "X701.10"),
       "I0.7": ("B502", "Fin de course axe 1 max", 2, "X701.11", "X701.12"),
       "I1.0": ("B503", "Fin de course axe 2 min", 1, "X701.13", "X701.14"),
       "I1.1": ("B504", "Fin de course axe 2 max", 2, "X701.15", "X701.16")}
for inp, (rep, des, row, t1, t2) in FDC.items():
    REP[rep] = {"des": des, "fab": "À définir", "carac": "contact NO (1 = fin de course atteinte), choix de Julien 05/11", "loc": "+M"}
    entree(inp, row, [("borne", t1, None, None, None), ("maitre", rep, fdc, "", ("13", "14")),
                      ("borne", t2, None, None, None)])
for inp, rep, pref, row, des in (("I1.2", "KM1", "KM", 1, "Retour contacteur amont variateur 1 (aux NO)"),
                                 ("I1.3", "KM2", "KM", 2, "Retour contacteur amont variateur 2 (aux NO)"),
                                 ("I1.4", "Q423", "Q", 1, "Retour contacteur 48 V (aux NO)")):
    entree(inp, row, [("esclave", rep, nom, des, ("13", "14"))])
I50 = {inp: stub(f, (k501e[inp].x, 11200), k501e[inp], "24") for inp in ("I0.2", "I0.3")}
# I1.5 : renvoi à droite (au-dessus, il chevaucherait le repère de la borne de I0.1)
I50["I1.5"] = W(f, [k501e["I1.5"], (k501e["I1.5"].x, 11600), (k501e["I1.5"].x + 1600, 11600)], "24")
renvoi("40", Z1_40, f, I50["I1.5"], "24")
renvoi("41", VOIES["B411"][1], f, I50["I0.2"], "24")
renvoi("41", VOIES["B412"][1], f, I50["I0.3"], "24")
PN50 = W(f, [k501e["X1 P1"], (26000, k501e["X1 P1"].y)], "PN")
texte(f, 24800, 12000, "PROFINET", 200)
g.tableau(F[f], 13600, 14400, [1400, 1600, 8400], 300, [
    ["Entrée", "Repère", "Fonction"], ["I0.0", "-S412", "AU pupitre actionné (NO)"], ["I0.1", "-S411", "AU armoire actionné (NO)"],
    ["I0.2", "-B411", "capot ouvert, mécanique (aux. 23-24)"], ["I0.3", "-B412", "capot ouvert, magnétique (aux. 23-24)"],
    ["I0.4", "-S413", "mode Auto (AUTO-C)"], ["I0.5", "-S413", "mode Manu (MANU-C)"],
    ["I0.6 / I0.7", "-B501 / -B502", "fins de course axe 1 min / max (NO)"],
    ["I1.0 / I1.1", "-B503 / -B504", "fins de course axe 2 min / max (NO)"],
    ["I1.2 / I1.3", "-KM1 / -KM2", "retour contacteurs amont variateurs"],
    ["I1.4", "-Q423", "retour contacteur 48 V"], ["I1.5", "-K401", "diagnostic relais sécu (Z1, trames)"],
], size=200)

# ======================================================================== 51 AUTOMATE SORTIES
f = "51"
k501s = maitre(C + "Siemens_6ES7214-1AH50-0XB0_CPU1214C_G2_sorties.xsy", "K501", f, 4800, 6400, ref=(),
               base="K501", compact=True, rep_size=300, fpos=(-400, -2000))     # repère près du module (Julien)
W(f, [k501s["3L+"], (4800, 7200), (4000, 7200), (4000, RAIL24_Y)], "24")
W(f, [k501s["3M"], (5600, 7600), (3600, 7600), (3600, RAIL0_Y)], "0V")
Q51 = {q: W(f, [k501s[q], (k501s[q].x, 8000)], "24") for q in ("Q0.0", "Q0.1", "Q0.2", "Q0.3", "Q0.4", "Q0.5")}
# 16/11 (Julien) : colonne -H1 et voyant -H4 dessinés au f62, avec la SM 1223 qui les commande
# PUL des 2 drivers obligatoirement en 100 kHz (Julien, 30/10) : Q0.0 à Q0.3 seulement, Q0.4 et suivantes = 20 kHz
for q, (T, sg) in (("Q0.0", ("T322", "PUL")), ("Q0.1", ("T322", "DIR")), ("Q0.2", ("T323", "PUL")),
                   ("Q0.3", ("T323", "DIR")), ("Q0.4", ("T322", "ENA")), ("Q0.5", ("T323", "ENA"))):
    renvoi(f, Q51[q], "32", CMD32[(T, sg)], "24")

reserve(f, [k501s["Q0.6"], k501s["Q0.7"]], True)
reserve(f, [k501s["Q1.0"], k501s["Q1.1"]], True)
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
col = maitre(C + "RSPRO_199-9760_colonne_lumineuse.xsy", "P511", f, 17600, 14400)
BCOL = {c: borne(t, f, col[c].x, 13200) for c, t in (("RD", "X701.43"), ("OG", "X701.44"), ("GN", "X701.45"))}
REP["P513"] = {"des": "Voyant porte : défaut machine", "fab": "À définir", "carac": "24 V CC - rouge", "loc": "+A1"}
p513 = decrit(voyant, "P513", f, 25600, 14400, "Voyant porte : défaut machine", fpos=(600, 400), wrap=20, prefix="P")
bh4a, bh4b = borne("X721.13", f, 25600, 13200), borne("X721.14", f, 25600, 16400)     # porte (05/11)
# sorties -> appareils : la sortie la plus à gauche descend le plus bas (aucun croisement)
for q, dest, yh in (("Q8.0", BCOL["RD"]["1"], 12400), ("Q8.1", BCOL["OG"]["1"], 12000), ("Q8.2", BCOL["GN"]["1"], 11600),
                    ("Q8.4", bh4a["1"], 11200)):
    W(f, [k521s[q], (k521s[q].x, yh), (dest.x, yh), dest], "24")
for c in BCOL:
    W(f, [BCOL[c]["2"], col[c]], "24")
W(f, [bh4a["2"], p513["X1"]], "24")
W(f, [p513["X2"], bh4b["1"]], "0V")
bcom = borne("X701.46", f, col["COM"].x, 16800)
W(f, [col["COM"], bcom["1"]], "0V")
# 0 V de la colonne et du voyant : collecteur sous les appareils, rejoint le 0 V de la SM 1223 à gauche
for p in (bh4b["2"], bcom["2"]):
    W(f, [p, (p.x, 17600)], "0V")
W(f, [(bh4b["2"].x, 17600), (3600, 17600), (3600, 13200)], "0V")
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
b531 = maitre("Contacts Capteurs\\Thermocouple.xsy", "B531", f, 6800, 7200, prefix="B", fpos=(2000, 0))
# 02/11 : 2 bornes pour thermocouple (référence à définir, pas encore achetée), entre le câble W8 et -K3
REP["X701.41"] = REP["X701.42"] = {"des": "Borne pour thermocouple type K (à définir)", "fab": "", "carac": "", "loc": "+A1"}
bt1, bt2 = borne("X701.41", f, 6000, 9600), borne("X701.42", f, 8400, 9600)
W(f, [b531["1"], (6800, 6400), (6000, 6400), bt1["1"]], "TC")
W(f, [bt1["2"], (6000, 10400), (6800, 10400), k531["AI0+"]], "TC")
W(f, [b531["2"], (7600, 6400), (8400, 6400), bt2["1"]], "TC")
W(f, [bt2["2"], (8400, 10400), (7600, 10400), k531["AI0-"]], "TC")
# 16/11 : repère et composition du câble à droite (plus sur les fils), réserve AI1 à AI7 par une accolade
g.cable(F[f], 5600, 8800, 8800, "W531", "compensation type K", "", [6000, 8400], etiq=(9200, 8400), size=250)
texte(f, 9200, 9800, "Bornes thermocouple : type à définir", 200)
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
    texte(f, 8000, py - 350, t, 220)
renvoi(f, PN54["P1"], "50", PN50, "PN")
renvoi(f, PN54["P2"], "20", VAR[("20", "PN")], "PN")
renvoi(f, PN54["P3"], "21", VAR[("21", "PN")], "PN")

# ======================================================================== 60 PUPITRE
f = "60"
g.cadre(F[f], 4800, 3200, 27200, 10800, width=20, dashed=True)
texte(f, 5000, 3300, "+P1 PUPITRE", 300, 0, 1)
p601 = maitre(C + "Siemens_6AV2123-2GB03-0AX0_IHM_KTP700_Basic_PN.xsy", "P601", f, 8000, 9600)
t21, t22, t23 = borne("X711.21", f, 8000, 12400), borne("X711.22", f, 8800, 12400), borne("X711.23", f, 9600, 12400)
W(f, [p601["L+"], t21["1"]], "24")
W(f, [p601["M"], t22["1"]], "0V")
W(f, [p601["FE"], t23["1"]], "PE")
W(f, [t21["2"], (8000, 13600), (4000, 13600), (4000, RAIL24_Y)], "24")
W(f, [t22["2"], (8800, 14000), (3600, 14000), (3600, RAIL0_Y)], "0V")
PE_DEST.append((f, W(f, [t23["2"], (9600, 14400)], "PE")))
renvoi(f, W(f, [p601["X1"], (p601["X1"].x, 11600)], "PN"), "54", PN54["P4"], "PN")
texte(f, 4200, 13300, "24VELEC", 220)
texte(f, 10000, 13600, "Bornes -X50.11 à -X50.13 (armoire)", 220)

# ======================================================================== 80 - 90 (générés par WinRelais)
for num, lignes in (("80", ["Liste des câbles extérieurs : à générer par WinRelais (carnet de câbles)",
                            "-W101, -W201 à -W203, -W211, -W213, -W321, -W322, -W531, -W11, -W12, -W13 ; PROFINET PN1 à PN4."]),
                    ("85", ["Implantation armoire +A1 : à réaliser sous WinArmoire",
                            "(les symboles portent la localisation A1 / P1 / M dans Vue armoire)."]),
                    ("90", ["Nomenclature : à générer par WinRelais (Optimisation / Générer / Nomenclature),",
                            "seuls les symboles maîtres portent une référence fabricant."])):
    for i, l in enumerate(lignes):
        texte(num, 3200, 4000 + 600 * i, l, 300)

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
    ["X311:1", "K401:A1", "K501:L+", "K501:3L+", "K521:L+",
     "K531:L+", "K541:V1+", "X721.11:1", "T201:X5:24V", "T211:X5:24V", "X711.21:2"],
    ["X312:1", "K401:A2", "K501:M", "K501:1M", "K501:3M", "K521:M", "K521:3M", "K531:M", "K541:V1-",
     "KM1:A2", "KM2:A2", "Q421:A2", "Q422:A2", "Q423:A2", "X701.46:2", "X721.12:2", "X721.14:2",
     "T201:X5:GND", "T211:X5:GND", "T201:X6:2",
     "T322:PUL-", "T322:DIR-", "T322:ENA-", "T323:PUL-", "T323:DIR-", "T323:ENA-", "X711.22:2"],
    ["K501:FE", "P601:FE", "X101.VJ:2", "T301:PE", "T302:PE", "X36.1:2", "X131:PE", "T321:PE",
     "T201:X1:PE", "T211:X1:PE"],
    ["M201:PE", "T201:X2:PE"], ["M211:PE", "T211:X2:PE"],
    ["B531:1", "K531:AI0+"], ["B531:2", "K531:AI0-"],
    # moteurs SEW : frein (W202 / W212) et sonde TF (W203 / W213) en direct, sans bornier
    ["M201:1b", "T201:X10:1"], ["M201:2b", "T201:X10:2"], ["M211:1b", "T211:X10:1"], ["M211:2b", "T211:X10:2"],
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
    ("R5, tronçon 1 : câble -W11 (27G1 : 26 + PE, 4 de réserve non bornés) -> pupitre +P1", [
        ("AU -S2", _n("", [f"X711.{n}" for n in (1, 2, 3, 4, 5, 6)], range(1, 7))),
        ("Sélecteur -S3", _n("", [f"X711.{n}" for n in (13, 14, 15, 16, 19, 20, 7, 8, 9, 10, 11, 12, 17, 18)], range(7, 21))),
        ("IHM -P1", [("X711.21", "21"), ("X711.22", "22"), ("X711.23", "PE")])]),
    ("R5, tronçon 1 (suite) : câble -W12 (19G1 : 18 + PE, 2 de réserve non bornés, V/J -> -XPE1) -> boîte machine", [
        ("Capot -B1", _n("", [f"X701.{n}" for n in (1, 2, 3, 4)], range(1, 5))),
        ("Fins de course -B3 à -B6", _n("", [f"X701.{n}" for n in range(9, 17)], range(5, 13))),
        ("Colonne -H1", _n("", [f"X701.{n}" for n in (43, 44, 45, 46)], range(13, 17)))]),
    ("R5, tronçon 2 : capteurs et sondes", [
        _g("Capot -B2 (câble M12)", [f"X701.{n}" for n in (5, 6, 7, 8)]),
        _g("Thermocouple -B7 (W8)", ["X701.41", "X701.42"]),
        _g("Sonde TF M1 (W3)", ["X701.21", "X701.22"]),
        _g("Sonde TF M2 (W6)", ["X701.29", "X701.30"])]),
    ("R5, tronçon 3 : moteurs pas-à-pas", [
        _g("M3 (W9)", [f"X701.{n}" for n in range(33, 37)]),
        _g("M4 (W10)", [f"X701.{n}" for n in range(37, 41)])]),
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
    organisation_x70()
    # f71 : toutes les bornes vers le pupitre +P1, quel que soit leur folio
    noms = [ren(i) for b, d, fi, fn, dest, bs in GROUPES if dest == "+P1" for i, _ in bs]
    for num, titre in (("71", "BORNES ARMOIRE +A1 <-> PUPITRE +P1 (X41, X42, X50, X60)"),):
        lignes = plan_bornier(path, noms)
        texte(num, 2400, 1600, titre, 300, 0, 1)
        # les lignes portent déjà les nouveaux numéros de folio (relus dans le fichier) : pas de 2e traduction
        g.texte = lambda folio, x, y, txt, *a, **k: _texte(folio, x, y, ren_rep(txt), *a, **k)
        g.tableau(F[num], 1800, 2400, [1800, 12400, 12400], 560,
                  [["Borne", "Côté armoire (intérieur)", "Côté terrain (extérieur)"]] + lignes, size=230)
        g.texte = lambda folio, x, y, txt, *a, **k: _texte(folio, x, y, ren(txt), *a, **k)
        y = 2400 + 560 * (len(lignes) + 1) + 300
        for l in ("Méthode : 1 borne par conducteur qui sort de l'armoire, côté armoire en haut de la borne, côté terrain en bas.",
                  "Bornier graphique : Optimisation / Générer / Bornier, onglet Automatique, extraire X41, X42, X50, X60,",
                  "folio visible, option Matériel connecté via un bornier + Pré-remplissage + filtre B,M,S2,S3,P1."):
            texte(num, 2400, y, l, 200)
            y += 350


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
for num_, dy_ in (("40", 800), ("42", 1200), ("50", 800)):
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
f = "50"
W(f, [k501e["L+"], (k501e["L+"].x, RAIL24_Y)], "24")
for p in ("M", "1M"):
    W(f, [k501e[p], (k501e[p].x, RAIL0_Y)], "0V")
CH = sorted(["31", "40", "42", "50", "51", "52", "53", "54", "60"], key=lambda n: NUMFOL.get(n, n))   # f41 : pas de piquage
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
for num_, (x1_, y1_, x2_, y2_), dx_, dy_ in (("51", (20700, 15500, 29100, 17200), -4400, -10800),
                                            ("52", (15900, 12000, 26100, 14700), -1200, -4200)):
    dans = lambda x, y: x1_ <= x <= x2_ and y1_ <= y <= y2_
    g.textes = [(t[0], t[1] + dx_, t[2] + dy_) + tuple(t[3:]) if t[0] == F[num_] and dans(t[1], t[2]) else t
                for t in g.textes]
    g.dessins = [(d[0], d[1] + dx_, d[2] + dy_, d[3] + dx_, d[4] + dy_) + tuple(d[5:])
                 if d[0] == F[num_] and dans(d[1], d[2]) and dans(d[3], d[4]) else d for d in g.dessins]
nommer_phases()
for a_ in NUM_ALERTES:
    print("ATTENTION", a_)
renommer_symboles()
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
