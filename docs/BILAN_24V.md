# Bilan des consommations 24 V CC (schéma v23, 06/11/2026)

Deux alimentations RS PRO 284-0491, 24 V 240 W (10 A) chacune :
- **T2 = 24VELEC** : électronique, toujours présente (automate, IHM, switch, relais KA1, électronique des variateurs) ;
- **T1 = 24VSEC** : charges coupées par la sécurité (bobines via FA1 et les contacts de KA1, STO), sorties de la SM 1223 (colonne, voyant défaut).
Aucune des deux n'est coupée par l'AU (c'est KA1 qui coupe les charges).

Règle : aucune valeur inventée. « ? » = valeur à lire sur la fiche ou à demander. Sources en bas de page.

## T2 : 24VELEC
| Appareil | Courant | Source |
|---|---|---|
| KA1 relais de sécurité XPSUAF13AP (A1) | 0,08 A (2,0 W) | notice Schneider [N] p.6 |
| K1 CPU 1214C G2 (L+) | 0,145 A | fiche 6ES7214-1AH50-0XB0 (copie distributeur) |
| K2 SM 1223 G2 (L+) | 0,045 A max (côté sorties) | fiche 6ES7223-5BH50-0XB0 (extrait) |
| K3 SM 1231 TC G2 (L+) | 0,015 A | fiche 6ES7231-5QF50-0XB0 (version allemande) |
| K4 switch IE-SW-AL05LM-5TX | 0,14 A | fiche Weidmüller 2682250000 |
| P1 IHM KTP700 Basic PN (via 27G1) | 0,23 A | fiche 6AV2123-2GB03-0AX0 |
| U1, U2 MCX91A : X5 électronique 24 V | ? × 2 | à demander à SEW (`docs/QUESTIONS_SEW.md`, question 8) |
| CPU 3L+ → entrées PUL / DIR / ENA des 2 drivers DM860H | ? (6 entrées) | notice DM860H |
| CPU L+ capteurs → contacts B1 à B6, S1 à S3, KM / KA2 (14 entrées) | ? (courant d'entrée de la CPU G2) | fiche CPU |
| H3 voyant porte 24VELEC | ? | référence à définir |
| **Total connu** | **0,655 A ≈ 15,7 W** | 6,5 % de T2 |

T2 consomme à peu près la même chose en permanence (min ≈ moy ≈ max), avec un petit appel à la mise sous tension (IHM, CPU).

## T1 : 24VSEC
| Appareil | Courant | Quand | Source |
|---|---|---|---|
| KF1, KF2 bobines LC1D09BD (freins) | 2 × 0,225 A (5,4 W chacune) | KA1 armé (Auto et Manu) | fiche Schneider LC1D09BD |
| KM1, KM2 bobines LC1D09BD (réseau des variateurs) | 2 × 0,225 A | Auto seulement (AUTO-A) | idem |
| KA2 bobine LC1D09BD (48 V des drivers) | 0,225 A | Manu seulement (MANU-D) | idem |
| STO de U1 (puis U2 en chaîne) | ? | Auto seulement (AUTO-B) | à demander à SEW (question 3) |
| H1 colonne (1 à 3 feux), par Q8.0 à Q8.2 | ? | selon le programme | fiche RS 199-9760 (onglet Documents) |
| H4 voyant défaut, par Q8.4 | ? | en défaut | référence à définir |

| Cas | Courant connu | % de T1 |
|---|---|---|
| Min : après un AU (KA1 ouvert) | 0 A (+ colonne / H4 si allumés) | 0 % |
| Manu : KF1 + KF2 + KA2 | 0,675 A (16,2 W) | 6,8 % |
| Auto en production : KF1 + KF2 + KM1 + KM2 | 0,90 A (21,6 W) + STO + colonne | 9 % |
| Max : Auto + colonne et H4 allumés | 0,90 A + ? | |

Les bobines LC1D09BD ont la même puissance à l'appel et au maintien (5,4 W) : pas de pointe à prévoir au collage.

## Conclusion
- Les deux alimentations sont très peu chargées par ce qu'on connaît : 0,66 A sur T2, 0,90 A au plus sur T1, pour 10 A chacune.
- Pour atteindre 50 % de T2, il faudrait 4,3 A de valeurs inconnues ; pour T1, 4,1 A. Peu probable avec les appareils restants, mais à confirmer avec les valeurs « ? ».
- La répartition suit la fonction, pas la charge : 24VSEC = tout ce que la sécurité coupe. C'est cohérent avec l'architecture ; T1 n'a pas besoin d'être plus chargée.

## Sources
- KA1 : notice Schneider XPSUAF13AP, dans `docs/references/XPSUAF13AP_base_connaissances_cablage.md` (R-03).
- LC1D09BD : fiche Schneider (`docs/DECISIONS.md`, 03/11).
- CPU 1214C G2 : https://my.goagilix.com/assets/a2/92/a292d5c7-1184-4152-a298-d0dd5f9d6225/Siemens_6ES72141AH500XB0_Specification_Sheet.pdf
- SM 1223 G2 : https://docs.rs-online.com/8527/A700000015919127.pdf
- SM 1231 TC G2 : https://www.stercontrol.pl/attachments/data//SIMATIC/6ES72315QF500XB0_datasheet_en.pdf
- Switch : https://datasheet.weidmueller.com/pdf/pl/2682250000/scope/2
- KTP700 : https://emin.com.mm/media/uploads/1308568.pdf
Les valeurs Siemens viennent de copies de distributeurs : à recouper avec les fiches Siemens officielles.
