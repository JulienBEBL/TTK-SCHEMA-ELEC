# Revue de la v36 par Krizox (visio du 20/11/2026) : demandes de modification

Source : notes brutes de Julien, recopiées telles quelles dans [2026-11-20_krizox_v36_notes_brutes.txt](2026-11-20_krizox_v36_notes_brutes.txt).
Chaque demande indique : ce que Krizox a écrit, ce que l'assistant en comprend, l'état de la v36 (relu dans le .xrs), ce qu'il faut faire, et **qui** le fait.
Rien n'est modifié tant que Julien n'a pas validé la demande. **Statut : revue faite avec Julien le 23/11, point par point** : chaque demande porte sa décision. À faire en v37 : demandes « à faire » du tableau.

## Qui fait quoi
| Code | Signification |
|---|---|
| **C** | Claude seul : script `ttk_schema.py` (ou générateur d'implantation), puis génération et contrôle par calcul |
| **J** | Julien seul : décision, information à fournir, travail dans WinRelais, câblage ou essai réel |
| **J+C** | Les deux : Julien décide ou donne une donnée, puis Claude dessine |

## Tableau de synthèse (après la revue du 23/11)
| N° | Folio | Demande (courte) | Décision de Julien | Qui | Statut |
|---|---|---|---|---|---|
| D01 | 10 | Brins des câbles sans le V/J | tous les câbles en « G » | C | **fait v37** |
| D02 | 10 | Pas de numéro de fil côté câble client | validé | C | **fait v37** |
| D03 | 10 | « Incrémenter » entre câble client et QF1 | déjà fait | — | clos |
| D04 | 12 | Bornes de H2 | gardées (toute la porte) | — | clos |
| D05 | 13 | Bornes ventilateurs / éclairage | gardées | — | clos |
| D06 | 20 | Pôle 5-6 de KA2 | plus dessiné | C | **fait v37** |
| D07 | 20 | « Enlever le num » | = brin 5 (V/J) de W9 / W10 (D01) | C | **fait v37** |
| D08 | tous | Bornes de la boîte +BJM | tous les câbles, W11 compris ; fils boîte → appareils | C + J | **fait v37** (à valider) |
| D09 | tous | Cadre pointillé hors armoire | validé, +BJM dans son propre cadre | C | **fait v37** |
| D10 | tous | Localisations | noms gardés, affichés partout | C | **fait v37** |
| D11 | tous | 24 V / 0 V drivers et E/S | contrôle pendant la v37 | C | **fait v37** |
| D12 | tous | Câbles W11, W12, W14 sur les folios | validé + vérifier qu'aucune borne ne manque | C | **fait v37** |
| D13 | 21 | Barres du haut | supprimées au f21 | C | **fait v37** |
| D14 | 21 | Folio 21 refait au propre | 4 blocs alignés, images retirées | C | **fait v37** |
| D15 | 30 | Adresses IP | « IP : à définir » ; valeurs plus tard (TIA) | C puis J | **fait v37** (IP à donner) |
| D16 | 31, 32 | Fils STO et 24 V | retracés | C | **fait v37** |
| D17 | 31, 32 | Freins : câblage et pilotage | action externe au schéma | J | hors v37 |
| D18 | 03 | Synoptique | par lieu, avec les câbles | C | **fait v37** |
| D19 | 60 | Renvois du haut horizontaux | validé | C | **fait v37** |
| D20 | 60 | L+ capt | textes courts | C | **fait v37** |
| D21 | 61, 62 | Réserves regroupées | validé, aussi au f62 | C | **fait v37** |
| D22 | 62 | Colonne H1 centrée | validé | C | **fait v37** |
| D23 | 62 | Bornes de H4 | gardées | — | clos |
| D24 | 70, 71+ | Plans de bornier | f70 gardé, f71 remplacé, f72… si besoin | C | **fait v37** |
| D25 | automate | Mnémoniques | seulement dans TIA | J | hors schéma |

**Après la v37 (Julien, D04)** : check global des bornes et de l'implantation.

**v37 générée le 23/11** : `schema/generes/release/TTK_2026-11-23_v37.xrs`, rapport `docs/RAPPORT_v37_2026-11-23.md` (choix à valider : f43, bornes X43, ordre de la boîte, sections des fils).

## Détail

### D01 · f10 · Brins du câble client W1 (C)
- Krizox : « Le câble client ne peut pas avoir 1 2 3 4 5, seulement 1 à 4. »
- v36 : W1 « 5G4 », brins numérotés `1-2-3-4-5`.
- Compris : le 5e conducteur est le vert/jaune (PE). Il ne porte pas de numéro. Brins 1 à 4, PE repéré V/J.
- À faire : W1 en `1-2-3-4` + PE.
- **Validé par Julien (23/11)** : règle appliquée à **tous les câbles en « G »** (W1, W4, W9, W10, W11, W12…) : brins numérotés sans le vert/jaune, PE repéré par sa couleur.

### D02 · f10 · Pas de numéro de fil sur le câble client (C)
- Krizox : « supprimer f10 les numéros de câbles client car il n'y en a pas ».
- v36 : 1001 à 1004 sur le câble client (au-dessus de X10) et de X10 à QS1.
- Compris : le câble client est posé par l'installateur, il n'a pas nos repères. On garde le numéro seulement côté armoire (X10 → QS1).
- À faire : retirer les numéros du tronçon câble client → X10.
- **Validé par Julien (23/11)**, sans changement.

### D03 · f10 · « Incrémenter » entre câble client et QF1 (J+C)
- Krizox : « il faut peut-être incrémenter sur les fils f10 entre câble client et QF1 ».
- v36 : X10 → QS1 = 1001-1004, QS1 → QF1 = 1011-1014 : le numéro change déjà à chaque appareil.
- Pas clair. Deux lectures : a) c'est déjà fait (rien à changer) ; b) changer aussi de numéro après la borne X10, ce qui contredit la règle du 05/11 (« une borne ne change pas le numéro »).
- Question Q1.
- **Réponse de Julien (23/11) : a), rien à changer** (déjà incrémenté à chaque appareil). D03 close.

### D04 · f12 · Supprimer les bornes du voyant H2 (J+C)
- Krizox : « supprimer borne H2 ».
- v36 : H2 (voyant 230 V de porte) par X12.21 / X12.22.
- Conflit : règle de Julien du 05/11 pour la porte : « tous les appareils par des bornes, ou aucun » (S1, S4, H2, H3, H4). Krizox demande aussi « pas de bornier pour voyant » au f62 (D23).
- Conséquences : implantation R4 à refaire (C) ; câblage déjà fait à reprendre (J).
- Question Q2.
- **Décision de Julien (23/11) : on garde les bornes de H2**, et de tous les appareils de la porte (S1, S4, H2, H3, H4) : règle du 05/11 maintenue. Bornes posées sur R4, pas encore câblées. **Rien à changer** au schéma.
- **À faire après la revue** (Julien) : check global des bornes et de l'implantation.

### D05 · f13 · Supprimer les bornes des ventilateurs (J+C)
- Krizox : « supprimer borne ventilo ».
- v36 : EV1 / EV2 par X13.21 (L) / X13.22 (N). L'éclairage EL1 / EL2 a aussi ses bornes X13.11 / X13.12.
- Compris : les ventilateurs sont dans l'armoire, ils n'ont pas besoin de bornes. L'éclairage non plus ?
- Question Q2.
- **Décision de Julien (23/11) : on garde les bornes** des ventilateurs (X13.21-22) et de l'éclairage (X13.11-12). **Rien à changer.**

### D06 · f20 · Enlever un contact de KA2 (J+C)
- Krizox : « enlever un contact KA2 ».
- v36 : KA2 dessiné avec ses 3 pôles : 1-2 → U3, 3-4 → U4, **5-6 libre**.
- Deux lectures : a) ne pas dessiner le pôle 5-6 inutilisé ; b) couper les deux +48 V par un seul pôle (02_MATERIEL disait « 1 pôle (1-2) »).
- Question Q3.
- **Décision de Julien (23/11) : a)**, ne plus dessiner le pôle 5-6 (inutilisé). Câblage inchangé (1-2 → U3, 3-4 → U4). Qui : C.

### D07 · f20 · « Enlever le num » (J+C)
- Krizox : « enlever le num ».
- Pas clair : quel numéro ? (numéros de fil 2001 / 2011 entre KA2 et les drivers, numéros des brins de W9 / W10, autre ?)
- Question Q3.
- **Réponse de Julien (23/11)** : c'est le brin **5 (V/J) de W9 et W10** : le vert/jaune d'un câble n'est jamais numéroté. Même règle que D01 (déjà couverte). Qui : C.

### D08 · tous · Bornes de la boîte de jonction machine +BJM (J+C)
- Krizox : « rajouter des bornes pour celles du boîtier de dérivation ».
- v36 : la boîte +BJM n'est **pas dessinée** (décision de Julien du 18/11). W4 et W12 vont « vers +BJM ».
- Revient sur la décision du 18/11. Calcul du 17/11 (09_STOCK) : 57 bornes sans le pupitre, 84 avec W11.
- Il manque : quels câbles passent par la boîte (Julien 17/11 : « tous », réserves comprises ; W11 ?), et les **câbles boîte → appareils**, jamais définis (repères, types).
- À faire : Julien fixe le contenu ; Claude dessine les bornes +BJM-X1 entre la borne d'armoire et l'appareil, sur chaque folio concerné.
- Question Q4.
- **Réponses de Julien (23/11)** :
  1. Câbles par la boîte : **tous** (« normalement »), **W11 (pupitre) compris** (confirmé le 23/11).
  2. Boîte → appareils : **des fils**, pas des câbles. Numéros et sections à définir par Claude selon la logique de chaque fonction (numéro du potentiel côté armoire, section du circuit), proposés à Julien.
  3. Boîte : **fabrication BEBL** (« custom »), pas de référence du commerce.
- Qui : C (dessin, numéros, sections proposés), J (validation, fabrication de la boîte).

### D09 · tous · Cadre pointillé autour des appareils hors armoire (C)
- Krizox : « revérifier si pointillé autour symbole si extérieur armoire ».
- v36 : aucun cadre pointillé autour des appareils +M ou +P1 (seulement l'arrivée au f10 et les liaisons PROFINET).
- À faire : cadre pointillé autour de chaque appareil hors armoire (M1 à M4, B1 à B7, H1, S2, S3, P1), avec sa localisation.
- **Validé par Julien (23/11)** ; les bornes de la boîte ont leur **propre cadre pointillé « +BJM »**. Qui : C.

### D10 · tous · Localisations +1, +2… (J+C)
- Krizox : « mettre un +1 pour armoire, +2 pour IHM, etc. ».
- v36 : +A1 armoire, +P1 pupitre, +M machine (01_PROJET).
- Krizox écrit lui-même « +P1 » dans la demande D18. Pas sûr qu'il veuille changer les noms : peut-être seulement **afficher** la localisation partout.
- Question Q5.
- **Décision de Julien (23/11) : b)**, on garde +A1, +P1, +M, +BJM et on les affiche partout (cadres pointillés D09, synoptique D18). Qui : C.

### D11 · tous · 24 V et 0 V des drivers et des E/S automate (C)
- Krizox : « vérifier le 24 et le 0 pour les drivers, et les entrées / sorties automate ».
- v36 (relu) : PUL+ / DIR+ / ENA+ de U3 / U4 sur Q0.0 à Q0.5 (6101-6106) ; PUL- / DIR- / ENA- au 0 V commun 1230 ; sorties CPU alimentées par 2L+ / 2M ; entrées sur L+ capt 6001 (X21.14), 1M au 0 V.
- À faire : contrôle complet par calcul (équipotentielles), puis compte rendu à Julien. Correction seulement si une erreur est trouvée.
- **Validé par Julien (23/11)** : contrôle fait **pendant la préparation de la v37**. Qui : C, relecture J.

### D12 · tous · Câbles 27G1 (W11) et 19G1 (W12) sur les folios (C) **important**
- Krizox : « important => rajouter les câbles 27G1 et 19G1 !!! »
- v36 : W11 et W12 n'apparaissent qu'aux f70, f80 et f92. Aucun câble dessiné sur les folios où passent leurs conducteurs (f41, f42, f50, f60, f62). W14 (M12 de B2) n'est pas dessiné non plus.
- À faire : dessiner W11, W12 (et W14) entre les bornes et les appareils, avec le n° de conducteur sur chaque brin (répartition validée du 05/11, 02_MATERIEL).
- **Validé par Julien (23/11)**, avec une demande en plus : **vérifier qu'aucune borne ne manque**. Chaque liaison armoire ↔ extérieur (+P1, +M, +BJM) doit passer par une borne ; compte rendu des bornes manquantes à Julien avant de les ajouter. Qui : C.

### D13 · f21 · Renvoi de folio manquant (C)
- Krizox : « renvoi de folio manquant ».
- v36 : les barres 24VELEC et 0 V du haut du f21 commencent dans le vide à gauche (fils en attente en (3200, 2000) et (3200, 2800), déjà dans les « attentions » du verifier).
- Compris : il manque l'origine des barres (X21.11 / X21.12 sur le même folio, ou renvoi depuis le f12).
- À faire : relier le début des barres à leur source. À confirmer avec Julien si Krizox visait un autre renvoi.
- **Décision de Julien (23/11)** : les barres du haut sont **en trop** au f21 (les potentiels 1241 / 1231 / 1230 arrivent déjà par les renvois de gauche depuis le f12). On **supprime les 2 barres du haut au f21** ; H3 (X21.21 / X21.22) prend son propre départ sur X21.11 et X21.12 ; un départ de X21.11 et un de X21.12 partent par renvoi vers le f30, où les barres commencent. Exception à la règle 14 (04_REGLES_DESSIN) : le f21 est le seul folio de commande sans barres. Qui : C.

### D14 · f21 · Bloc noir X21.14 (C)
- Krizox : « bornier noir chelou, dégueu comme il est ».
- v36 : X21.14 (24 V capteurs, L+ capt de la CPU), ajouté en v28 à côté des 3 autres blocs.
- À faire : le redessiner comme les 3 autres (cadre, image, place, départs). Si Julien sait ce qui gênait Krizox (place, texte, liaison), le dire.
- **Julien (23/11)** : le symbole est bon, c'est **sa position** qui ne va pas. **Refaire tout le f21 au propre** (avec D13). Proposition de l'assistant : les 4 blocs sur une même ligne, même hauteur, même pas, dans l'ordre X21.11 rouge, X21.12 bleu, X21.13 gris, X21.14 noir, chacun avec son cadre et son image ; arrivées à gauche de chaque bloc ; départs vers les autres folios en renvois alignés ; H3 et ses bornes à part, à droite. Qui : C.
- **Validé par Julien (23/11)**, avec : **images des blocs retirées** pour le moment (gardées seulement s'il reste vraiment la place) ; **attention aux renvois de folio** (chaque départ, chaque arrivée, textes justes) **et aux numéros de fil** (1241, 1230, 1231, 6001 sur chaque tronçon, contrôle `xrs_numeros.py`).

### D15 · f30 · Adresses IP (J+C)
- Krizox : « préciser les adresses IP ».
- Connu (dépôt TTK-AUTOMATISME, 19/11) : PC de banc 192.168.0.10 / 255.255.255.0 ; CPU et variateurs dans 192.168.0.x, **adresses à fixer**. Rien pour le switch et l'IHM.
- À faire : Julien fixe le plan d'adresses (CPU, U1, U2, IHM, switch s'il en a une, masque), et si besoin les noms PROFINET ; Claude l'écrit au f30.
- Question Q6.
- **Décision de Julien (23/11)** : adresses fixées plus tard **dans TIA** par Julien. En v37 : un champ « IP : à définir » à côté de chaque appareil PROFINET au f30 (K1, U1, U2, P1, et K4 s'il a une adresse), masque « à définir ». Les vraies valeurs seront reportées quand Julien les donnera. Qui : C (champs vides), puis J (valeurs).

### D16 · f31, f32 · Fils STO et 24 V (C)
- Krizox : « fil bleu STO et 24 dégueu ».
- v36 : renvois 24VELEC vers X5 (f21) et STO depuis le f42 (X6.1 / X6.2, chaîne U1 → U2), avec des bouts allongés en v30.
- À faire : retracer ces fils proprement (droits, sans détour ni croisement inutile).
- **Validé par Julien (23/11)**, sans changement. Compte rendu des changements de tracé à la v37. Qui : C.

### D17 · f31, f32 · Câblage des freins (J+C) **important**
- Krizox : « revoir aussi le câblage frein !!!! important !! vérifier la rotation manuelle pendant test ».
- v36 : chaque frein BE5 est alimenté en 400 V CA par QF2 / QF3 → KF1 / KF2 ; KF1 / KF2 commandés par KA1 13-14, **sans le variateur** et sans S3. Freins desserrés dès que KA1 est armé, y compris en Manu (voulu par Julien le 05/11, pour tourner l'arbre à la clé).
- Points possibles derrière la remarque (à confirmer) :
  - frein desserré même quand le variateur n'est pas prêt ou ne tient pas le moteur (Auto, arrêt, défaut variateur) : pas de couple de maintien ;
  - frein non piloté par la sortie frein du variateur (pratique SEW courante) ;
  - courant du frein BE5 et calibre de QF2 / QF3 toujours inconnus (05, point 8).
- « Rotation manuelle pendant test » : essai à faire (J) : en Manu, KA1 armé, l'arbre tourne-t-il à la main ? En Auto à l'arrêt ?
- Question Q7.
- **Réponse de Julien (23/11)** : Krizox demande de vérifier (1) que le **câblage** du frein est bon pour le frein réellement monté, (2) que la **logique de pilotage** du frein est bonne.
- **Décision** : **action externe au schéma**, lancée à part par Julien (avec l'assistant ou un autre chat) : plaque moteur, redresseur BG / BGE, notice SEW MCX91A (pilotage du frein par le variateur ?), courant du frein (calibre QF2 / QF3), essais de rotation à la main (Manu, Auto à l'arrêt, après AU). **Rien à changer en v37** ; le schéma sera modifié ensuite, si besoin, à la demande de Julien. Qui : J (+ C sur demande).

### D18 · f03 · Synoptique (C)
- Krizox : « remettre le synoptique avec +P1 etc. et les encadrés ».
- v36 : blocs de texte par fonction (arrivée, distribution, variateurs…), sans regroupement par lieu.
- À faire : regrouper les blocs dans des cadres par localisation (armoire, pupitre +P1, machine +M), câbles entre cadres. Dépend de Q5 pour les noms.
- **Décision de Julien (23/11) : a)**, le synoptique par fonction est **remplacé** par un synoptique **par lieu** : un cadre par localisation (réseau client, +A1, +P1, +BJM, +M) avec ses appareils principaux, et les câbles entre cadres (repère + type : W1 à W14, PN1 à PN4), +BJM entre l'armoire et la machine (D08). Noms gardés (D10). Qui : C.

### D19 · f60 · Renvois du haut à l'horizontale (C)
- Krizox : « mettre les renvois de folio ligne haut en horizontale comme ligne du haut ».
- v36 : en haut du f60, le renvoi (41-E6) arrive à l'horizontale mais (41-J6) et le L+ capt (21-L7) arrivent à la verticale.
- À faire : renvois du haut à l'horizontale, alignés comme les barres 24 V / 0 V.
- **Validé par Julien (23/11)**, sans changement. Qui : C.

### D20 · f60 · « L+ des sorties » (J+C)
- Krizox : « éclaircir le L+ des sorties, car bizarre ».
- Lecture probable : le L+ capt est une **sortie** de la CPU (alimentation des capteurs). Au f60 il part vers X21.14 (f21) puis revient vers les contacts : le trajet n'est pas lisible.
- Autre lecture : le 2L+ des sorties de la CPU (f61).
- À faire : texte court près de la broche (« sortie 24 V capteurs -> -X21.14 ») ou tracé plus direct.
- Question Q8.
- **Réponse de Julien (23/11)** : c'est bien le **L+ capt du f60**. À faire : texte court près de la broche (« sortie 24 V capteurs -> -X21.14 (f21) ») et sur la ligne du haut (« 24 V capteurs (-X21.14) ») ; renvoi du haut à l'horizontale (D19). Qui : C.

### D21 · f61 · Réserve en un seul groupe (C)
- Krizox : « réserve sur les 4 pins au lieu de 2 groupes de 2 ».
- v36 : Q0.6 / Q0.7 et Q1.0 / Q1.1 ont chacun leur accolade « Réserve ».
- À faire : une seule accolade « Réserve » sur les 4 broches.
- **Validé par Julien (23/11)**, étendu au **f62** : réserves regroupées en une accolade quand les broches se suivent (I8.x, Q8.5 à Q8.7 ; Q8.3 seule entre Q8.2 et Q8.4). Règle générale pour les folios d'E/S. Qui : C.

### D22 · f62 · Colonne lumineuse H1 (C)
- Krizox : « recentrer les lampes colonne lumineuse ».
- À faire : centrer H1 sous ses sorties Q8.0 à Q8.2 et ses bornes X62.11-14.
- **Validé par Julien (23/11)**, sans changement ; décalage mesuré par calcul à la v37. Qui : C.

### D23 · f62 · Pas de bornes pour le voyant H4 (J+C)
- Krizox : « pas de bornier pour voyant car dans l'armoire, à vérifier ».
- v36 : H4 par X62.21 / X62.22. Même question que D04 (règle de la porte).
- Question Q2.
- **Décision de Julien (23/11)** : on **garde les bornes de H4** (règle de la porte, D04). **Rien à changer.**

### D24 · f70 · Borniers comme un vrai schéma (J+C)
- Krizox : « revoir schéma bornier (en plus de l'implantation déjà existante). Faire comme les schémas en vrai (see electrical) ».
- v36 : f70 = cases rangées rail par rail (comme l'implantation), f71 = tableau des bornes du pupitre.
- Compris : un **plan de bornier** classique (style SEE Electrical) : une ligne par borne, côté armoire à gauche (appareil, broche, n° de fil), côté terrain à droite (câble, n° de conducteur, appareil), ponts, butées.
- Il manque : un exemple de ce que Krizox attend (copie d'écran ou PDF d'un schéma SEE Electrical).
- Question Q9.
- **Réponse de Julien (23/11)** : 4 images d'exemple, gardées dans [2026-11-20_krizox_v36_exemples_bornier/](2026-11-20_krizox_v36_exemples_bornier/). **f70 gardé** (mis à jour si besoin) ; **f71 remplacé** par des plans de bornier de ce type ; **f72, f73…** ajoutés si besoin.
- Ce que montrent les exemples (lecture de l'assistant) :
  - bornier **horizontal** : un rectangle à gauche avec le repère du bornier (XP, XC, -X16), relié à la rangée de bornes ;
  - une **colonne par borne** : vis en haut et en bas, numéro de borne au milieu ; borne de terre avec le symbole de terre en bout ; butée en trait épais (ex. 3) ; formes différentes selon le type de borne (ex. 2) ;
  - **textes verticaux** au-dessus (côté armoire) et en dessous (côté terrain), un par fil : destination sous la forme folio-repère-broche-n° (ex. « 02-KA1-14-07 ») ;
  - ex. 3 (SEE Electrical) : en plus, n° de fil sur chaque fil, câble terrain dessiné (repère « -LE_PREMIX_PP_CC_AMS », type « LIY-CY 2x0,5 »), couleur de conducteur (BN, WH), destination terrain (« DALLE TECHNIQUE POM. »).
- Proposition (format des textes, à valider) : au-dessus « -appareil:broche (fNN) » + n° de fil sur le fil ; en dessous, câble (repère + n° de conducteur ou couleur) puis « -appareil:broche (fNN) » côté terrain. Qui : C.
- **Validé par Julien (23/11)** : format « -KA1:14 (f40) » + n° de fil sur le fil, **provisoire** (« on modifiera si besoin plus tard »). Un plan par bornier (X10, X20, X31, X32, X41, X42, X50, X60, X62, X63, +BJM-X1). Contrôle : chaque borne une fois, deux côtés câblés.

### D25 · Automate (J)
- Krizox : « AUTOM => krizox ; programme automate => mnémoniques importants ».
- Compris : Krizox aide (ou relit) le programme ; il insiste sur des mnémoniques clairs (table des variables TIA).
- Hors schéma : à traiter dans le dépôt TTK-AUTOMATISME. Option : écrire le mnémonique de chaque E/S sur les folios 60 à 63.
- **Décision de Julien (23/11)** : mnémoniques **seulement dans TIA** pour l'instant ; rien sur les folios. Qui : J.
- Question Q10.

## Questions à Julien
Posées par lots de 4 au plus. Réponses notées ici, puis reportées dans la demande.
| N° | Demandes | Question | Lot | Réponse |
|---|---|---|---|---|
| Q1 | D01, D03 | « Incrémenter » au f10 : déjà fait (1001 → 1011 → 1021) ou nouveau numéro après X10 ? Brins sans PE : sur tous les câbles en « G » ? | 2 | a) déjà fait ; brins sans V/J sur tous les câbles en G (23/11) |
| Q2 | D04, D05, D23 | Bornes des appareils de l'armoire : on retire celles de H2, H4, des ventilateurs ; et H3, S1, S4, l'éclairage ? | 1 | bornes gardées partout (23/11) |
| Q3 | D06, D07 | KA2 : ne plus dessiner le pôle 5-6, ou un seul pôle pour les deux +48 V ? « enlever le num » : quel numéro ? | 1 | pôle 5-6 plus dessiné ; « num » = brin 5 V/J de W9 / W10 (23/11) |
| Q4 | D08 | Boîte +BJM : quels câbles y passent (W11 ?), et quels câbles boîte → appareils ? | 2 | tous, W11 compris ; fils boîte → appareils ; boîte BEBL (23/11) |
| Q5 | D10, D18 | Localisations : renommer (+1, +2…) ou garder +A1 / +P1 / +M et les afficher partout ? | 1 | noms gardés, affichés (23/11) |
| Q6 | D15 | Plan d'adresses IP (CPU, U1, U2, IHM, switch, masque) ? | 2 | plus tard dans TIA ; « à définir » en attendant (23/11) |
| Q7 | D17 | Freins : qu'est-ce qui gêne Krizox exactement ? | 1 | vérifier câblage et pilotage : action externe (23/11) |
| Q8 | D20 | « L+ des sorties » : le L+ capt (f60) ou le 2L+ (f61) ? | 2 | L+ capt du f60 (23/11) |
| Q9 | D24 | Exemple de bornier SEE Electrical voulu par Krizox ? | 2 | 4 images ; f71 remplacé (23/11) |
| Q10 | D25 | Mnémoniques : seulement dans TIA, ou aussi sur les folios 60 à 63 ? | 2 | seulement dans TIA (23/11) |
