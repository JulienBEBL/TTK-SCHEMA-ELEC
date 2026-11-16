# 02 · Matériel retenu

Le matériel est **commandé et en grande partie reçu** ; l'armoire est en montage. On fait avec, on n'ajoute qu'en cas de vraie nécessité.
Source : symboles CUSTOM posés (`outils/librairie/CUSTOM/`), passation du 29/10, décisions datées. « à vérifier » = non confirmé.

## Puissance 400 / 230 V (f10 à f13)
| Repère | Matériel | Remarque |
|---|---|---|
| W1 | Câble client 5G4 mm² [D 28/10] | |
| X10.11 à X10.15 | Bornes d'arrivée (ancien X11) ; X10.11 = PE, borne de terre vert/jaune | |
| QS1 | Legrand Vistop 022515, 4P 63 A | manœuvre armoire ouverte |
| QF1 | Hager NFT820, 3P+N 20 A courbe C | disjoncteur de tête |
| TR1 | TEMCo TT1041, 480 D / 400 Y-230, 15 kVA | variante US, hors armoire |
| -XR1, -XR2 (ancien X12) | 2 répartiteurs 4P 125 A 7 départs AEE300427 par armoire | non dessinés depuis le 29/10 (renvois directs QF1 → bus f11). Fil 4 mm² seulement : seuls les 5 petits départs (1,5-6 mm²) serrent. QF1 → XR1, puis 1 pont 4 mm² par pôle XR1 → XR2 (la borne de QF1 n'accepte pas 2 × 4 mm²) [D 04/11]. Repères XR1 et XR2 [D 05/11]. Affectation des départs : `implantation/` page 5 ; **13/11 (Julien, monté)** : XR1 et XR2 **collés côte à côte sur le même rail que QS1 / QF1 (R2)** ; ce rail est plein. XR2 n'est plus sur le R4. Électriquement rien ne change (QF1 → XR1 → XR2, toujours non dessinés : renvois QF1 → bus f11). Ponts XR1 → XR2 : 1 pont 4 mm² par pôle, sauf indication contraire de Julien |
| (ancien X13) | Legrand 404839, bornier de terre 27 | non dessiné depuis le 29/10 (départs PE au f10) ; repère à fixer |
| QM1 / QM2 | Schneider GV2ME14, réglés 6,5 A | amont variateurs |
| KM1 / KM2 | Schneider LC1D09BD (bobine 24 V CC) | contacteurs variateurs |
| QF2 / QF3 | Schneider iC60N A9F74202, 2P 2 A courbe C | freins ; calibre à confirmer avec le courant du BE5 |
| KF1 / KF2 | Schneider LC1D09BD | contacteurs de frein |
| QF4 / QF5 | Hager NFT706, 1P+N 6 A courbe C | alimentations 24 V |
| QF6 | Schneider iC60N A9F75204, 2P 4 A courbe D | alimentation 48 V |
| QF7 / QF8 | **Hager NFT702, 1P+N 2 A courbe C, 6-10 kA, 1 module** [D 29/10] | QF7 ventilateurs, QF8 éclairage (symbole NFT706 à remplacer en v7) |
| QF9 | IMO B6CR1N1630A, différentiel 1P+N 16 A 30 mA | prise |
| QF10 | Schneider iDT40K A9P71606, 1P+N 6 A courbe C | limitation prise |
| XD1 (ancien X14) | Legrand 004280, prise 2P+T 16 A | |
| EV1 / EV2 | IDE VF92AC, ventilateurs 230 V | |
| EL1 / EL2 | RS PRO 194-0417, éclairage LED armoire | |
| H2 | Voyant 230 V présence tension | piqué sur L3 + N du bus (f12), câblé en 2,5 mm² ; ajouté au tableau le 03/11 (référence à relever) |

## Variateurs et moteurs (f31, f32)
| Repère | Matériel | Remarque |
|---|---|---|
| U1 / U2 | SEW MCX91A-0055-5E3 (CSO, CFN) | STO X6, TF X10, X5 24 V de sauvegarde, PROFINET X40 ; bornes X6 / X10 à confirmer |
| M1 / M2 | SEW K39 DRN100LS4 / BE5 / TF, 2,2 kW | frein BE5 400 V CA |
| R1 / R2 | SEW BW100-001 | **ne jamais proposer de les déplacer** |
| W2 / W5 | Moteur 4G2,5 blindé (2XSLCY-K, 50 m en stock) | |
| **W4** (W7 supprimé) [D 05/11, v18] | Freins M1 + M2 : **un seul** LIYCY-JZ 5G1,5 blindé de réserve (AEE261168, 80 m) | 300/500 V CA [C fiche Achat Electrique]. Conducteurs 1-2 = frein M1 (f31), 3-4 = frein M2 (f32), V/J → bornier de terre -XPE1 et boîte de dérivation côté machine (pas de borne sur rail). **Correction du 05/11** : le schéma appelle W4 / W7 les freins et W3 / W6 les sondes TF depuis la v11 ; « W3 » noté le 05/11 par l'agent d'implantation était faux (Julien : « le numéro m'importe peu ») |
| W3 / W6 | Sonde TF 2x0,75 blindé (LIYCY PPMM0180) [D 02/11] | acheté ; conducteurs **blanc et marron** (Julien 05/11) |
| W13 | Liaison équipotentielle armoire → bâti machine : conducteur V/J seul **4 mm²** [D 05/11, v18] | depuis la terre de l'arrivée (f10) ; Julien hésitait 2,5 / 4 : 4 retenu (conducteur seul, pas protégé mécaniquement) |
- **Stock de câble (Julien 05/11)** : seulement du 5G1,5 ; pas de 5G2,5 ni de 5G1.

## Très basse tension (f12, f20, f21)
| Repère | Matériel | Remarque |
|---|---|---|
| T1 / T2 | RS PRO 284-0491, 24 V 240 W (10 A) | T1 = COMMANDE, T2 = ELEC (noms à changer, voir 03) |
| T3 | Mean Well NDR-240-48, 48 V 240 W | |
| KA2 (ex KM3) | Schneider LC1D09BD, contacteur auxiliaire, 1 pôle (1-2) sur le +48 V | pouvoir de coupure DC-1 sous 48 V à vérifier |
| X21.11 à X21.13 (anciens X31 à X33) | **Phoenix PTFIX 6/12X2,5 (3273354)**, 1 entrée + 12 départs [D 05/11, v20] : X21.11 24VELEC **rouge**, X21.12 0 V **bleu**, X21.13 24VSEC **gris** (stock de Julien : RD, BK, GY, BU ; référence exacte par couleur à vérifier) | remplace les PTFIX 6X1,5 (3002781) ; X12.11 (ancien X36) = borne sectionnable PELV |
| U3 / U4 | Jkongmotor JKDM860H | entrées PUL / DIR / ENA en **24 V CC** [C 27/10] ; polarité ENA à vérifier |
| M3 / M4 | StepperOnline 34IP65-85 (Nema 34) | |

## Sécurité, commande (f40 à f42, f50)
| Repère | Matériel | Remarque |
|---|---|---|
| KA1 | Schneider XPSUAF13AP | cat. 0, PL d visé, démarrage surveillé par S4 |
| S1 / S2 | AU XB5AS8442 (armoire / pupitre) + ZBE102 (NF) + ZBE101 (NO) | **2 NF + 1 NO par AU** [D 03/11, Julien change la commande] |
| S3 | Eaton T0-4-8223/E (RS 257-9558, 78627324), 2 positions 90°, sans 0, 20 A | **4 inverseurs** [C fiche Eaton 05/11] : pos. 1 ferme 1-2, 5-6, 9-10, 13-14 ; pos. 2 ferme 3-4, 7-8, 11-12, 15-16 ; ponts 2-4, 6-8, 10-12, 14-16 (communs). Les ponts sont des fils montés d'usine sur les bornes paires : **Julien les a retirés** (photos du 05/11) → 8 NO indépendants, comme l'essai du 27/10. Auto = position 1, Manu = position 2 ; 24 V CC / 10 mA fiable (< 10^-5), DC-13 10 A [C fiche Eaton 05/11] ; numérotation des bornes provisoire |
| S4 | Schneider XB4BA21, BP noir 1 NO, **non lumineux** [D 03/11] | f40, symbole « BP Affleurant Noir » ; voyant retiré du f61 et Q8.3 en réserve (v16) |
| FA1 (IEC 81346-2, validé par Julien le 04/11) | Mersen CMC101 (RS 189-5333) + cartouche FR10GG50V4 gG 4 A (RS 188-6962) [D 03/11] | R-33, amont 13 / 23 / 33 de KA1 ; dessiné au f40 en v16 |
| B1 | RS PRO 902-6874, interrupteur de position (capot mécanique) | |
| B2 | ifm MN508S (RS 016-3138), capteur magnétique **codé** (confirmé par Julien le 02/11) | 2 NO + 1 NF, M12, 24 V 50 mA ; homologation sécurité et actionneur à vérifier |
| B3 à B6 | Fins de course (NF) | symbole posé = NO, à corriger |
| H1 | RS PRO 199-9760, colonne 3 couleurs | |
| H3 / H4 | Voyants 24 V ELEC présent / défaut | |
| P1 | Siemens KTP700 Basic PN 6AV2123-2GB03-0AX0 | |

## Automate et réseau (f60 à f63, switch f30)
| Repère | Matériel |
|---|---|
| K1 | CPU 1214C G2 DC/DC/DC 6ES7214-1AH50-0XB0 |
| K2 | SM 1223 G2 8DI/8DQ 6ES7223-5BH50-0XB0 |
| K3 | SM 1231 TC G2 6ES7231-5QF50-0XB0 (f63 validé par Julien le 23/10, à revalider après renommage) |
| K4 | Switch Weidmüller 2682250000 IE-SW-AL05LM-5TX |
| B7 / W8 | Thermocouple type K, câble de compensation en direct jusqu'à K3 [D 28/10] |

## Câbles multiconducteurs
- 19G1 et 27G1 : **validés par Julien le 05/11 (Q32)**, dessinés au f70 en v19 (table `CABLES_MULTI` du script). Julien veut utiliser le 27G1 en priorité, ranger par fonction ; conducteur n° = ordre des bornes.
  - **27G1 (repère proposé -W11) armoire → pupitre +P1** : 1-4 X41.11-14 (AU S2 voies 1 et 2), 5-8 X41.21-24 (S3 Manu, shunt des capots), 9-14 X42.11-16 (Manu-D, Auto-A, Auto-B : après KA1), 15-16 X60.11-12 (S2 NO → I0.0), 17-20 X60.21-24 (S3 → I0.4 / I0.5), 21-22 X50.11-12 (IHM L+ / M), PE → X50.13 (FE de l'IHM, masse du pupitre), 23-26 réserve.
  - **19G1 (-W12) armoire → boîte de jonction machine** : 1-4 X41.31-34 (B1), 5-12 X60.31-38 (B3 à B6), 13-16 colonne H1 (X62.11-14, v17), 17-18 réserve, PE → masse de la boîte. B2 (M12) par son propre câble jusqu'aux bornes X41.41-44 [D 05/11].
  - 27G1 rangé par composant (05/11) : S2 = 1-6 (X41.11-14 voies 1 et 2, X60.11-12 NO → I0.0) ; S3 = 7-20 (X41.21-24 shunts, X42.11-16 Manu-D / Auto-A / Auto-B, X60.21-24 infos) ; IHM = 21-22 (L+ / M seulement) + PE ; réserve 23-26. S3 passe à 9 fils avec l'option D.
  - Risque du 03/11 (revue, risque 1) : **écarté par Julien le 05/11** : chaque conducteur a sa propre gaine dans le câble ; il soigne le cheminement.
- Repères : 2 répartiteurs 4P AEE300427 = **-XR1 / -XR2** [D 05/11, Julien] ; bornier de terre Legrand 404839 = **-XPE1** [D 05/11].
- LIYCY-JZ 5G1,5 (80 m) : **réserve** [D 27/10].

## Sélecteur S3 : vraie numérotation et noms (dessinés en v17, 05/11)
Ponts retirés : on garde les 8 contacts séparés du schéma, avec les vrais numéros. 1 bloc = 1 contact Auto + 1 contact Manu.
| Bloc | Auto (position 1) | Manu (position 2) |
|---|---|---|
| 1 | 1-2 : Auto-A → KM1 / KM2 (provisoire 13-14) | 3-4 : Manu-D → KA2 (83-84) |
| 2 | 5-6 : Auto-B → STO (23-24) | 7-8 : shunt capot voie 1 (53-54) |
| 3 | 9-10 : info Auto → I0.4 (33-34) | 11-12 : info Manu → I0.5 (73-74) |
| 4 | 13-14 : réserve (43-44) | 15-16 : shunt capot voie 2 (63-64) |
Noms (Julien 05/11, lettre = bloc) : AUTO-A 1-2, MANU-A 3-4, AUTO-B 5-6, MANU-B 7-8, AUTO-C 9-10, MANU-C 11-12, AUTO-D 13-14 (réserve), MANU-D 15-16. Symboles `outils/librairie/CUSTOM/Eaton_T0_contact_NO_*.xsy` (copies de « RC Contact NO 13-14 »).

## Ancienne option D (05/11, abandonnée : ponts retirés)
Le schéma actuel demande 5 potentiels séparés (L+ capteurs pour les infos, voie 1, voie 2, KA1 24, KA1 34) pour 4 communs. Les deux voies (shunts) ne peuvent pas partager un commun (court-circuit croisé vu par KA1, R-10). Option D :
| Pôle | Commun | Position 1 Auto | Position 2 Manu |
|---|---|---|---|
| 1 (2/4) | KA1 24 | 1 → KM1 / KM2 (Auto-A) + I0.4 | 3 → KA2 (Manu-D) + I0.5 |
| 2 (6/8) | KA1 34 | 5 → STO (Auto-B) | 7 : réserve |
| 3 (10/12) | voie 1 (après les AU) | 9 : libre | 11 → S12 (shunt B1) |
| 4 (14/16) | voie 2 | 13 : libre | 15 → S22 (shunt B2) |
- KA1 14 n'alimente plus que KF1 / KF2 ; Manu-D passe de KA1 14 à KA1 24.
- Les infos automate lisent les lignes après S3 : mode connu seulement quand KA1 est fermé.
- Si les ponts sont amovibles, le schéma actuel (8 contacts séparés) reste possible.

## Porte de l'armoire (rappel du 05/11)
| Repère | Appareil | Folio |
|---|---|---|
| S1 | AU armoire (déjà par bornes X41.5x / X60.4x) | 41, 60 |
| S4 | Bouton de réarmement XB4BA21 (boucle Y1-Y2 de KA1) | 40 |
| H2 | Voyant « armoire sous tension » 230 V, blanc | 12 |
| H3 | Voyant « 24VELEC présent » | 21 |
| H4 | Voyant « défaut machine », rouge (sortie Q8.4) | 61 |
H1 n'est pas sur la porte : c'est la colonne lumineuse de la machine.
