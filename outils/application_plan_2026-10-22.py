"""Application du tableau TTK_Plan_Folios_Reperes.xlsx (22/10/2026) à test_xrs_claude.xrs.

À lancer APRÈS corrections_2026-10-22.py. Repères écrits sans « - » (comme dans le reste du
schéma : WinRelais affiche le repère tel quel). Index de folio = ordre - 1 :
4=f10 5=f11 6=f12 7=f13 8=f20 9=f21 10=f30 11=f31 12=f32 13=f40 15=f42.

Non traité ici (décision ou matériel manquant, voir le compte rendu) : f41 sécurité, f50-f54
câblage automate, TF -> X10, renvois X5/X6/X40, Q12/Q13, folios 70-90, synoptique f04.
"""
import sys
from xrs_edit import XrsDoc

path = sys.argv[1] if len(sys.argv) > 1 else "../test_xrs_claude.xrs"
d = XrsDoc(path)
BOBINE = r"C:\Users\Public\Documents\Elec-CAO\sym_electrotech\--- M Bobine\Bobine KM.xsy"
AUTEUR = "Julien\u00b7Ingerea\u00b722/10/2026\u00b71.0\u00b70\u00b7"


def zone(x, y):
    """Case du cadre repère (colonnes de 20 mm à partir de x=13 mm, lignes idem)."""
    return f"{chr(65 + (x - 1300) // 2000)}{(y - 1300) // 2000 + 1}"


# ===================================================================== onglet Repères
# repère actuel -> (repère cible, désignation, fabricant + référence, caractéristiques)
REPERES = {
    "Q1": ("Q101", "Sectionneur général cadenassable", "Legrand 022515 Vistop", "63 A - 4P - 690 V"),
    "Q2": ("Q102", "Disjoncteur de tête", "Hager NFT820", "20 A courbe C - 10 kA - 3P+N"),
    "F1": ("F101", "Parafoudre type 2 (option non montée)", "Schneider A9L16297", "Imax 20 kA - Up 1,5 kV - 3P+N"),
    "T5": ("T101", "Transformateur US -> UE (variante US)", "TEMCo TT1041", "15 kVA - 480 V triangle / 400Y/230 V"),
    "X1": ("X111", "Répartiteur tétrapolaire", "AE AEE300427", "125 A - 1 entrée + 7 départs"),
    "X2": ("X112", "Bornier de terre PE", "Legrand 404839", "1 x 6-25 mm² + 26 x 1,5-16 mm² - 100 A"),
    "Q3": ("Q121", "Disjoncteur moteur départ variateur 1", "Schneider GV2ME14", "6-10 A - réglage 6,5 A"),
    "Q4": ("Q122", "Disjoncteur moteur départ variateur 2", "Schneider GV2ME14", "6-10 A - réglage 6,5 A"),
    "Q5": ("Q123", "Disjoncteur départ frein M1", "Schneider A9F74202 (iC60N)", "2 A courbe C - 2P"),
    "Q6": ("Q124", "Disjoncteur départ frein M2", "Schneider A9F74202 (iC60N)", "2 A courbe C - 2P"),
    "Q7": ("Q131", "Disjoncteur différentiel prise de service", "IMO B6CR1N1630A", "16 A C - 30 mA type A - 6 kA"),
    "Q8": ("Q132", "Disjoncteur alimentation 24 V n°1", "Hager NFT706", "6 A C - 10 kA - 1P+N"),
    "Q9": ("Q133", "Disjoncteur alimentation 24 V n°2", "Hager NFT706", "6 A C - 10 kA - 1P+N"),
    "Q10": ("Q134", "Disjoncteur alimentation 48 V", "Schneider A9F75204 (iC60N)", "4 A courbe D - 2P"),
    "Q11": ("Q135", "Disjoncteur limitation prise de service à 6 A (choix BEBL)", "Schneider A9P71606 (iDT40K)", "6 A C - 4,5 kA"),
    "X3": ("X131", "Prise de service", "Legrand 004280", "2P+T 16 A 250 V - limitée 1,5 kW"),
    "G1": ("G131", "Ventilateur armoire", "IDE VF92AC", "230 V - 19 W"),
    "G2": ("G132", "Ventilateur armoire", "IDE VF92AC", "230 V - 19 W"),
    "E1": ("E131", "Éclairage armoire n°1", "RS PRO 194-0417", "230 V - 14 W LED"),
    "T1": ("T201", "Variateur M1", "SEW MCX91A-0055-5E3-4-T00/001/CSO/CFN/CDM/CMM", "2,2 kW - 5,5 A - STO - PROFINET"),
    "R1": ("R201", "Résistance de freinage T201", "SEW BW100-001", "100 Ω - 0,1 kW"),
    "M1": ("M201", "Motoréducteur frein", "SEW K39 DRN100LS4/BE5/TF", "2,2 kW - 400 V Y - frein 400 V CA"),
    "T2": ("T211", "Variateur M2", "SEW MCX91A-0055-5E3-4-T00/001/CSO/CFN/CDM/CMM", "2,2 kW - 5,5 A - STO - PROFINET"),
    "R2": ("R211", "Résistance de freinage T211", "SEW BW100-001", "100 Ω - 0,1 kW"),
    "M2": ("M211", "Motoréducteur frein", "SEW K39 DRN100LS4/BE5/TF", "2,2 kW - 400 V Y - frein 400 V CA"),
    "T3": ("T301", "Alimentation 24 V CC n°1", "RS PRO 284-0491", "24 V - 10 A - 240 W"),
    "T4": ("T302", "Alimentation 24 V CC n°2", "RS PRO 284-0491", "24 V - 10 A - 240 W"),
    "T6": ("T321", "Alimentation 48 V CC", "Mean Well NDR-240-48", "48 V - 5 A - 240 W"),
    "T7": ("T322", "Driver pas-à-pas axe 1", "Jkongmotor JKDM860H", "48 V CC - 6,0 A"),
    "T8": ("T323", "Driver pas-à-pas axe 2", "Jkongmotor JKDM860H", "48 V CC - 6,0 A"),
    "M3": ("M321", "Moteur pas-à-pas translation 1", "StepperOnline 34IP65-85", "Nema 34 - 6 A - 8,5 Nm"),
    "M4": ("M322", "Moteur pas-à-pas translation 2", "StepperOnline 34IP65-85", "Nema 34 - 6 A - 8,5 Nm"),
    "K1": ("K401", "Relais de sécurité AU / protecteur", "Schneider XPSUAF13AP", "Fonction 1 - départ 3 - 24 V"),
    "K2": ("K501", "Automate CPU 1214C G2 DC/DC/DC", "Siemens 6ES7214-1AH50-0XB0", "14 DI / 10 DQ 24 V CC - brochage G2 provisoire"),
    "K4": ("K521", "Module E/S SM 1223 G2 8DI/8DQ", "Siemens 6ES7223-5BH50-0XB0", "8 DI / 8 DQ 24 V CC - brochage G2 provisoire"),
    "K6": ("K531", "Module SM 1231 TC G2", "Siemens 6ES7231-5QF50-0XB0", "8 AI thermocouple - brochage G2 provisoire"),
    "K7": ("K541", "Switch PROFINET armoire", "Weidmüller 2682250000", "5 ports - 2 alim."),
    "P1": ("P601", "IHM pupitre", "Siemens 6AV2123-2GB03-0AX0 (KTP700 Basic PN)", "24 V CC - PROFINET"),
}
# renommage seul (esclaves, bornes) : les champs descriptifs restent
RENOMMAGES = {"X1.1": "X101.1", "X1.2": "X101.2", "X1.3": "X101.3", "X1.4": "X101.4", "X1.VJ": "X101.VJ",
              "K3": "K501", "K5": "K521", "KM3": "Q421", "KM4": "Q422", "Q14": "Q423"}
CABLES = {"W1": "W101", "W2": "W201", "W3": "W211"}

# 1. champs 2-4 (avant renommage : K2/K3 deviendront tous deux K501)
for old, (_, c2, c3, c4) in REPERES.items():
    d.set_champ(old, 2, c2)
    d.set_champ(old, 3, c3)
    d.set_champ(old, 4, c4)
# 2. références constructeur : référence en « Réf 2 » partout (E1, T3, T4, X1 étaient décalés)
d.set_refconstructeur("E1", "RS PRO", "", "194-0417")
d.set_refconstructeur("T3", "RS PRO", "", "284-0491")
d.set_refconstructeur("T4", "RS PRO", "", "284-0491")
d.set_refconstructeur("X1", "AE", "", "AEE300427")
# 3. règle R3 : les représentations esclaves n'ont pas de référence (comptées 1 fois en nomenclature)
for slave in ("K3", "K5", "KM1", "KM2", "KM3", "KM4", "Q14"):
    d.set_refconstructeur(slave, "", "", "")
# 4. règle R8 : KM réservé à KM1 / KM2
d.set_prefix("KM1", "KM")
d.set_prefix("KM2", "KM")
# 5. renommages
for old, (new, *_) in REPERES.items():
    d.rename_symbol(old, new)
for old, new in RENOMMAGES.items():
    d.rename_symbol(old, new)
for old, new in CABLES.items():
    d.set_cable_name(old, new)

# ===================================================================== onglet Folios / anomalies 12, 15, 16
d.set_cartouche(8, "DESCRIPTION FOLIO", "VARIATEUR -T201, RESISTANCE -R201, MOTEUR -M201")
d.set_cartouche(9, "DESCRIPTION FOLIO", "VARIATEUR -T211, RESISTANCE -R211, MOTEUR -M211")
d.set_cartouche(11, "DESCRIPTION FOLIO", "DEPARTS 24 VDC : CPU, IHM, SWITCH, RELAIS SECU, VARIATEURS, BOBINES, COLONNE, CAPTEURS")
d.set_cartouche(13, "DESCRIPTION FOLIO", "RELAIS -K401 : ALIMENTATION, BORNES, REGLAGES")
d.replace_cartouche_text("BAILlY", "BAILLY")
for k, num in enumerate(["01", "02", "03", "04", "10", "11", "12", "13", "20", "21", "30", "31", "32",
                         "40", "41", "42", "50", "51", "52", "53", "54", "60"]):
    d.set_folio_nom(k, f"Folio {num}")

# ===================================================================== anomalie 10 : types de fil
NEUTRE = d.wire_attrs(4, (5200, 5600), (5200, 4000))
TERRE = d.wire_attrs(4, (4400, 3600), (4400, 1600))
PUISS = d.wire_attrs(4, (6000, 5600), (6000, 4000))
DC24 = d.wire_attrs(13, (16800, 9200), (16800, 7600))      # « Commande 24VDC » existant (K1:13)
ZEROV = d.wire_attrs(12, (4400, 12000), (4400, 11200))     # « 0V » existant (f32)
assert "Commande 24VDC" in DC24 and "0V" in ZEROV and "Neutre" in NEUTRE and "terre" in TERRE
d.set_wire_attrs(4, (20800, 8000), (20800, 8800), NEUTRE, "T101:X0 = neutre secondaire")
d.set_wire_attrs(4, (20000, 5200), (20000, 4400), TERRE, "T101:GND = terre")
for x in (9600, 10400):
    d.set_wire_attrs(8, (x, 15600), (x, 14400), DC24, "sonde TF M201 : 24 V CC")
for x in (12400, 13200):
    d.set_wire_attrs(9, (x, 15600), (x, 13600), PUISS, "frein M211 : 400 V CA")
for y in (9200, 9600, 10000, 10400, 10800, 11200):
    d.set_wire_attrs(12, (23200, y), (22800, y), DC24, "commande T323 : 24 V CC")
    d.set_wire_attrs(12, (12800, y), (13200, y), DC24, "commande T322 : 24 V CC")
d.set_wire_attrs(13, (11200, 11200), (11200, 12800), ZEROV, "K401:A2 = 0 V")
for x, y1, y2 in ((12800, 11200, 12800), (16800, 11200, 12800), (17600, 11200, 12800), (18400, 11200, 12800),
                  (12000, 11200, 12800), (11200, 9200, 7600), (12000, 9200, 7600), (12800, 9200, 7600),
                  (13600, 9200, 7600), (14400, 9200, 7600), (15200, 9200, 7600), (16000, 9200, 7600)):
    d.set_wire_attrs(13, (x, y1), (x, y2), DC24, "relais de sécurité K401 : 24 V CC")

# ===================================================================== anomalie 8 : renvois freins f12 -> f20 / f21
for (xa, xb) in ((18400, 12400), (19200, 13200)):          # Q421 -> M201 (bornes 2-3 frein)
    d.add_renvoi("(12-L2)", 6, 8, (xa, 14800), (xb, 14400),
                 f"(20-{zone(xb, 14400)})", f"(12-{zone(xa, 14800)})", "renvoi frein 1 f12 -> f20")
for (xa, xb) in ((24000, 12400), (24800, 13200)):          # Q422 -> M211
    d.add_renvoi("(12-L2)", 6, 9, (xa, 14800), (xb, 13600),
                 f"(21-{zone(xb, 13600)})", f"(12-{zone(xa, 14800)})", "renvoi frein 2 f12 -> f21")

# ===================================================================== anomalie 1 : f13 protection ventilateurs / éclairage
N_ATTR = d.wire_attrs(7, (19200, 6000), (19200, 3200))
L_ATTR = d.wire_attrs(7, (20000, 6000), (20000, 3200))
NCOL, LCOL = 16757612, 0
for p1, p2 in (((19200, 9600), (19200, 6000)), ((20000, 8800), (20000, 6000)),
               ((15200, 14000), (15200, 9600)), ((15200, 9600), (19200, 9600)),
               ((18400, 14000), (18400, 9600)), ((22000, 14000), (22000, 9600)),
               ((19200, 9600), (22000, 9600)), ((16800, 14000), (16800, 8800)),
               ((16800, 8800), (20000, 8800)), ((19200, 14000), (19200, 10400)),
               ((19200, 10400), (20000, 10400)), ((20000, 10400), (20000, 8800)),
               ((22800, 14000), (22800, 8800)), ((20000, 8800), (22800, 8800))):
    d.delete_wire(7, p1, p2, "f13 : ancienne distribution directe ventilateurs / éclairage")
for x, y in ((18400, 9600), (19200, 9600), (20000, 8800)):
    d.delete_jonction(7, x, y, "f13 : ancienne distribution")
d.move_wire_end(7, (20000, 6000), (20000, 3200), (20000, 6000), (20000, 5600), "f13 : arrivée L sur le bus L")
# disjoncteurs : copies de Q132 (Hager 1P+N), référence à définir
for name, dx, desig in (("Q137", 12400, "Disjoncteur éclairage (2 lampes)"),
                        ("Q136", 17600, "Disjoncteur ventilateurs")):
    d.copy_symbol("Q132", name, dx, 1200)
    d.set_champ(name, 2, desig)
    d.set_champ(name, 3, "À définir")
    d.set_champ(name, 4, "")
    d.set_refconstructeur(name, "", "", "")
d.copy_symbol("E131", "E132", -2000, 0)
d.set_champ("E132", 2, "Éclairage armoire n°2")
for k, y in ((1, 14400), (2, 14800), (3, 15100), (4, 15400)):
    d.move_champ("E132", k, 12400, y)
W = []   # (p1, p2, attrs)
W += [((15600, 6000), (19200, 6000), N_ATTR), ((19200, 6000), (20800, 6000), N_ATTR),     # bus N
      ((16400, 5600), (20000, 5600), L_ATTR), ((20000, 5600), (21600, 5600), L_ATTR),     # bus L
      ((15600, 6000), (15600, 7200), N_ATTR), ((16400, 5600), (16400, 7200), L_ATTR),     # -> Q137
      ((20800, 6000), (20800, 7200), N_ATTR), ((21600, 5600), (21600, 7200), L_ATTR)]     # -> Q136
W += [((15600, 9600), (15600, 12800), N_ATTR), ((16400, 9600), (16400, 12000), L_ATTR),  # Q137 ->
      ((13200, 12800), (15200, 12800), N_ATTR), ((15200, 12800), (15600, 12800), N_ATTR),
      ((14800, 12000), (16400, 12000), L_ATTR), ((16400, 12000), (16800, 12000), L_ATTR),
      ((13200, 12800), (13200, 14000), N_ATTR), ((14800, 12000), (14800, 14000), L_ATTR),  # E132
      ((15200, 12800), (15200, 14000), N_ATTR), ((16800, 12000), (16800, 14000), L_ATTR)]  # E131
W += [((20800, 9600), (20800, 11200), N_ATTR), ((21600, 9600), (21600, 10400), L_ATTR),  # Q136 ->
      ((18400, 11200), (20800, 11200), N_ATTR), ((20800, 11200), (22000, 11200), N_ATTR),
      ((19200, 10400), (21600, 10400), L_ATTR), ((21600, 10400), (22800, 10400), L_ATTR),
      ((18400, 11200), (18400, 14000), N_ATTR), ((19200, 10400), (19200, 14000), L_ATTR),  # G131
      ((22000, 11200), (22000, 14000), N_ATTR), ((22800, 10400), (22800, 14000), L_ATTR)]  # G132
for p1, p2, a in W:
    d.add_wire(7, p1, p2, a, "f13 : distribution protégée Q136 / Q137")
for (x, y), c in (((19200, 6000), NCOL), ((20000, 5600), LCOL), ((15200, 12800), NCOL),
                  ((16400, 12000), LCOL), ((20800, 11200), NCOL), ((21600, 10400), LCOL)):
    d.add_jonction(7, x, y, c, "f13 : dérivation")

# ===================================================================== anomalie 5 : bobines maîtres sur f42
LC1D = ("SCHNEIDER ELECTRIC", "", "LC1D09BD")
for k, (name, desig, pref) in enumerate((("KM1", "Contacteur amont variateur 1", "KM"),
                                         ("KM2", "Contacteur amont variateur 2", "KM"),
                                         ("Q421", "Contacteur frein M1", "Q"),
                                         ("Q422", "Contacteur frein M2", "Q"),
                                         ("Q423", "Contacteur coupure 48 V CC", "Q"))):
    x = 4000 + 4800 * k
    d.insert_xsy(BOBINE, name, 15, x, 8000, AUTEUR, prefix=pref, ref=LC1D,
                 champs={2: (desig, True, 600, 400, 200), 3: ("Schneider LC1D09BD", True, 600, 700, 200),
                         4: ("Bobine 24 V CC", True, 600, 1000, 200)})
d.add_texte("CPU", 15, 2800, 5600,
            "BOBINES (maîtres des références croisées) - commande A1 / A2 à câbler (ordre API / relais sécurité non décidé)",
            "f42 : note")

d.save()
last = None
for n, why, old, new in d.log:
    if why != last:
        print(f"# {why}")
        last = why
print(f"\n{len(d.log)} modifications -> {path}")
