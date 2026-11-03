# 02 · Matériel retenu

Le matériel est **commandé et en grande partie reçu** ; l'armoire est en montage. On fait avec, on n'ajoute qu'en cas de vraie nécessité.
Source : symboles CUSTOM posés (`outils/librairie/CUSTOM/`), passation du 29/10, décisions datées. « à vérifier » = non confirmé.

## Puissance 400 / 230 V (f10 à f13)
| Repère | Matériel | Remarque |
|---|---|---|
| W1 | Câble client 5G4 mm² [D 28/10] | |
| X11 | Bornes d'arrivée | |
| QS1 | Legrand Vistop 022515, 4P 63 A | manœuvre armoire ouverte |
| QF1 | Hager NFT820, 3P+N 20 A courbe C | disjoncteur de tête |
| TR1 | TEMCo TT1041, 480 D / 400 Y-230, 15 kVA | variante US, hors armoire |
| X12 | Répartiteur 4P 125 A 7 départs AEE300427 | non dessiné depuis le 29/10 (renvois directs QF1 → bus f11) |
| X13 | Legrand 404839, bornier de terre 27 | non dessiné depuis le 29/10 (départs PE au f10) |
| QM1 / QM2 | Schneider GV2ME14, réglés 6,5 A | amont variateurs |
| KM1 / KM2 | Schneider LC1D09BD (bobine 24 V CC) | contacteurs variateurs |
| QF2 / QF3 | Schneider iC60N A9F74202, 2P 2 A courbe C | freins ; calibre à confirmer avec le courant du BE5 |
| KF1 / KF2 | Schneider LC1D09BD | contacteurs de frein |
| QF4 / QF5 | Hager NFT706, 1P+N 6 A courbe C | alimentations 24 V |
| QF6 | Schneider iC60N A9F75204, 2P 4 A courbe D | alimentation 48 V |
| QF7 / QF8 | **Hager NFT702, 1P+N 2 A courbe C, 6-10 kA, 1 module** [D 29/10] | QF7 ventilateurs, QF8 éclairage (symbole NFT706 à remplacer en v7) |
| QF9 | IMO B6CR1N1630A, différentiel 1P+N 16 A 30 mA | prise |
| QF10 | Schneider iDT40K A9P71606, 1P+N 6 A courbe C | limitation prise |
| X14 | Legrand 004280, prise 2P+T 16 A | |
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
| W3 / W6 | Frein : LIYCY-JZ 5G1,5 blindé de réserve (AEE261168, 80 m) [D 03/11] | 300/500 V CA [C fiche Achat Electrique] : convient au 400 V entre phases, en dessous du ≥ 450/750 V du 26/10 ; 2 conducteurs + V/J utilisés, 2 en réserve. Composition « 2G1,5 » des folios 31 / 32 à passer en 5G1,5 |
| W4 / W7 | Sonde TF 2x0,75 blindé (LIYCY PPMM0180) [D 02/11] | acheté |

## Très basse tension (f12, f20, f21)
| Repère | Matériel | Remarque |
|---|---|---|
| T1 / T2 | RS PRO 284-0491, 24 V 240 W (10 A) | T1 = COMMANDE, T2 = ELEC (noms à changer, voir 03) |
| T3 | Mean Well NDR-240-48, 48 V 240 W | |
| KA2 (ex KM3) | Schneider LC1D09BD, contacteur auxiliaire, 1 pôle (1-2) sur le +48 V | pouvoir de coupure DC-1 sous 48 V à vérifier |
| X31 à X33 | Phoenix 3002781 PTFIX 6X1,5-BK (6 points, 17,5 A) | X36 = borne sectionnable PELV ; X34 / X35 (48 V) supprimés le 02/11 |
| U3 / U4 | Jkongmotor JKDM860H | entrées PUL / DIR / ENA en **24 V CC** [C 27/10] ; polarité ENA à vérifier |
| M3 / M4 | StepperOnline 34IP65-85 (Nema 34) | |

## Sécurité, commande (f40 à f42, f50)
| Repère | Matériel | Remarque |
|---|---|---|
| KA1 | Schneider XPSUAF13AP | cat. 0, PL d visé, démarrage surveillé par S4 |
| S1 / S2 | AU XB5AS8442 (armoire / pupitre) | ZBE101 / ZBE102 : NO ou NF ? à vérifier |
| S3 | Eaton T0-4-8223/E, 2 positions | **4 NO par position, 8 en tout** [C 27/10] ; Auto = position 1, Manu = position 2 ; numérotation des bornes provisoire |
| S4 | Schneider XB4BA21, BP noir 1 NO, **non lumineux** [D 03/11] | voyant Q8.3 (f61) à retirer, Q8.3 en réserve |
| FU1 (repère à valider) | Mersen CMC101 (RS 189-5333) + cartouche FR10GG50V4 gG 4 A (RS 188-6962) [D 03/11] | R-33, amont 13 / 23 / 33 de KA1 ; à dessiner |
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
- 19G1 et 27G1 (27G1 = machine ↔ armoire) : répartition non attribuée.
- LIYCY-JZ 5G1,5 (80 m) : **réserve** [D 27/10].
