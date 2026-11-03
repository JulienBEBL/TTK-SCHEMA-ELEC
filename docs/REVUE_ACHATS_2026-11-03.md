# Revue des achats avant clôture (03/11/2026)

Sources croisées : `Sourcing_Composant_2.xlsx` (Tableau V1, lots A à N), schéma v15 (`schema/generes/release/`, nomenclature et textes), `memoire/`, `docs/DECISIONS.md`, mémoire du projet.
Convention du tableau : quantités pour 1 machine, Hugo multiplie par 2. Exceptions : les lignes de câble marquées « pour les 2 machines » et le transformateur TEMCo (1 seul).

## 1. Manques vérifiés (rien dans le tableau, besoin au schéma ou décidé)
| # | Article | Constat |
|---|---|---|
| A1 | Thermocouple K RS 350-398, câble de compensation K RS 236-3959, embouts 4 mm² RS 157-1250, repères 4-6 mm² AEE300986 | colonne « Commandé à Hugo ? » = FALSE. La mémoire du 15/10 dit « thermocouple commandé » : à trancher |
| A2 | Bornes de terre (vert/jaune, contact rail) | aucune achetée. Besoin : X10.15 (PE arrivée), X31.11 et X32.11 (PE moteurs), X50.13 (FE IHM), conducteurs V/J des câbles extérieurs. Une PT 4 grise n'est pas une borne PE |
| A3 | Raccord sonde K (câble 2 m) / câble de compensation 25 m | aucun connecteur ni boîte de jonction type K acheté |
| A4 | Voyant H2 230 V CA blanc (f12, en porte) | seuls des voyants 24 V achetés (XB4BVB3 / B4 / B5) |
| A5 | S4 bouton de réarmement lumineux bleu (f40, voyant Q8.3 f61) | acheté : XB4BA21 noir, non lumineux |
| A6 | 2e lampe d'éclairage (EL2) | décision 22/10 : 2 lampes par armoire ; tableau : 194-0417 × 1 |
| A7 | Câble frein 2G1,5 (W3 / W6) | « à commander » (02_MATERIEL) ; absent du tableau. Option sans achat : LIYCY-JZ 5G1,5 de réserve (80 m), si sa tension assignée convient au 400 V CA |

## 2. Décisions qui conditionnent un achat
| # | Sujet | Options |
|---|---|---|
| B1 | R-33 (Q22) : fusible gG ≤ 10 A en amont des contacts 13 / 23 / 33 de KA1 | a) porte-fusible + cartouche gG ≤ 10 A (conforme notice) ; b) A9F74203 déjà acheté (disjoncteur, pas la prescription Schneider) ; c) rien (risque de soudure de contact sur court-circuit) |
| B2 | Antiparasites des 5 bobines LC1D09BD (point 3) | a) modules adaptés TeSys D (référence à vérifier) ; b) rien : usure accrue des contacts KA1, perturbations |
| B3 | Courant mini 10 mA des contacts KA1 (R-32) sur la sortie STO | si les 2 entrées STO en parallèle tirent < 10 mA : résistance de charge à prévoir. Valeur SEW à lire |
| B4 | Borne sectionnable PELV X12.11 | non achetée. Option sans achat : fil 0 V vissé sur une borne PE, démonté pour les mesures d'isolement |
| B5 | Bornes thermocouple X63.11 / .12 (Q19) | option sans achat : câble de compensation en direct sur K3 (décision du 28/10) |
| B6 | Carte mémoire SIMATIC (option) | sauvegarde / rechargement du programme par le technicien client sans TIA. Compatibilité G2 à vérifier |

## 3. À contrôler à réception ou sur pièce
| # | Point | Détail |
|---|---|---|
| C1 | 2XSLCY-K 4G2,5 | 50 m notés pour 2 machines ; besoin 4 × 15 m = 60 m (règle « 15 m borne à borne ») |
| C2 | Presse-étoupes CEM | 8 par machine (4 M25, 2 M20, 2 M16). Câbles blindés : 11 côté armoire (2 moteur, 2 TF, 2 frein, 2 pas-à-pas, 19G1, 27G1, TC), 6 côté moteurs SEW (note f31 / f32 : « presse-étoupe CEM côté moteur »). Plages de serrage contre diamètres réels |
| C3 | Reprise de blindage dans l'armoire | colliers / barre pour TF, frein, pas-à-pas, 19G1, 27G1 : rien au tableau (le MCX91A a son support) |
| C4 | Presse-étoupes des boîtes à bornes SEW | fournis avec les moteurs ? |
| C5 | Côté machine | boîte de jonction pour le 19G1 (B1, B3 à B6, H1) et raccord des pas-à-pas (WAGO, indice IP) : rien au tableau |
| C6 | Bornes | besoin 81 (77 au schéma + 4 pour H1, non dessinées) ; achat 70 PT 2,5 + 15 PT 4 = 85 par machine si Hugo a doublé : réserve 5 % (< 10 %). Repères de bornes : rien |
| C7 | Repères de fils | lettres A L R S U X Z / . en 0,5-1,5 mm² seulement ; pas de N ; aucune lettre en 2,5 et 4 mm². Convention de numérotation à fixer avant clôture, ou imprimante d'étiquettes (lot Amazon) |
| C8 | Fil bleu | nuance réelle des 196-4334, 811-4438, 811-4441, 811-4469 : neutre bleu clair, 24 V CC bleu foncé (IEC 60204-1 13.2.4) |
| C9 | Rail DIN 742-4138 × 1, goulotte 301-2006 × 1 | conditionnement contre le métré de l'implantation |
| C10 | ifm MN508S | actionneur codé absent du tableau |
| C11 | Porte | tresse de masse (H2 230 V en porte) |
| C12 | Bâti machine | conducteur de liaison équipotentielle armoire → bâti (V/J 4 mm² en stock + cosse) |
| C13 | BW100-001 × 4 | dans la commande SEW, reçues ? |
| C14 | Colonne Norelem 3 couleurs | absente du tableau ; tableau et symbole H1 = RS 199-9760 (vert / rouge) |

## 4. Incohérences relevées
1. ZBE101 libellé « Contact NF », ZBE102 « Contact NO » dans le tableau : c'est l'inverse (ZBE101 = 1F = NO, ZBE102 = 1O = NF). Quantités suffisantes dans les deux cas (Q25).
2. Thermocouple : « commandé » (mémoire 15/10) contre FALSE (tableau).
3. Colonne : décision 3 couleurs Norelem contre RS 199-9760 (tableau, symbole).
4. B3 à B6 : symbole NO, contact NF voulu (point 7).
5. A9F74203 × 2 et A9F74201 achetés, absents du schéma.
6. X13 : symbole Legrand 404839 ; tableau : bloc de terre RS 266-1257. Même article ?
7. US : mémoire du 15/10 « QF1 et QS1 à remplacer sur l'exemplaire US » contre consigne projet « armoire identique ».
8. 02_MATERIEL : W4 / W7 « 2G1 blindé, à commander » ; décision du 02/11 : 2x0,75 blindé, déjà acheté (PPMM0180, 100 m).
9. Tableau : quantités tantôt par machine, tantôt pour 2 machines (câbles, TEMCo).

## 5. Achetés, non utilisés (stock ou retour)
NFT816, GV2ME10 × 2, Finder 22 789-2708 × 4 et 789-2702 × 4, XB5AD25, répartiteur RS 868-0720, H05VV-F 2x0,75 50 m, LADN11 × 4 (contacts intégrés des LC1D09BD suffisants), un des deux jeux 2 A (A9F74202 courbe C / A9F75202 courbe D) selon le courant BE5, fil orange 1,5 mm² (plus d'orange depuis la v13), XB4BA21 si S4 lumineux.

## 6. Risques
1. 27G1 : le 24VELEC de l'IHM (permanent) voisine avec les fils après KA1 (Auto-A → KM1 / KM2, Auto-B → STO). Un court-circuit dans le câble alimente STO et bobines sans passer par KA1, sans détection. Options : exclusion de défaut (câble protégé, ISO 13849-2) ou alimentation IHM dans un autre câble.
2. Bornier X31 / X32 sur la sortie variateur : blindage interrompu, rayonnement dans l'armoire. Tronçon intérieur court, séparé des signaux.
3. Différentiel côté site (inconnu) : fuites des MCX91A, déclenchements possibles ; un type A peut être inadapté à un variateur triphasé. À signaler au client.
4. BW100-001 dans l'armoire : échauffement à mesurer en recette (décélérations répétées, +40 °C ambiant).
5. Thermocouple : soudure isolée ou à la masse inconnue, mise à la terre de la tête inconnue.
6. KA2 : DC-1 sous 48 V non vérifié (point 12).
7. B1 : ouverture positive du RS PRO 902-6874 non vérifiée.
8. S3 Eaton : courant mini des contacts sous 24 V (entrées automate, quelques mA) non vérifié.
9. Exemplaire US : prise XD1 au format français.
