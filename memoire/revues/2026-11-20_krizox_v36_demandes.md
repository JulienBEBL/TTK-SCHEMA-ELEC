# Revue de la v36 par Krizox (visio du 20/11/2026) : demandes de modification

Source : notes brutes de Julien, recopiées telles quelles dans [2026-11-20_krizox_v36_notes_brutes.txt](2026-11-20_krizox_v36_notes_brutes.txt).
Chaque demande indique : ce que Krizox a écrit, ce que l'assistant en comprend, l'état de la v36 (relu dans le .xrs), ce qu'il faut faire, et **qui** le fait.
Rien n'est modifié tant que Julien n'a pas validé la demande. **Statut : à valider par Julien** (23/11).

## Qui fait quoi
| Code | Signification |
|---|---|
| **C** | Claude seul : script `ttk_schema.py` (ou générateur d'implantation), puis génération et contrôle par calcul |
| **J** | Julien seul : décision, information à fournir, travail dans WinRelais, câblage ou essai réel |
| **J+C** | Les deux : Julien décide ou donne une donnée, puis Claude dessine |

## Tableau de synthèse
| N° | Folio | Demande (courte) | Qui | Bloqué par |
|---|---|---|---|---|
| D01 | 10 | Câble client W1 : brins 1 à 4 seulement (pas 1 à 5) | C | — |
| D02 | 10 | Retirer les numéros de fil côté câble client | C | — |
| D03 | 10 | « Incrémenter » les fils entre câble client et QF1 | J+C | Q1 |
| D04 | 12 | Supprimer les bornes du voyant H2 | J+C | Q2 |
| D05 | 13 | Supprimer les bornes des ventilateurs | J+C | Q2 |
| D06 | 20 | Enlever un contact de KA2 | J+C | Q3 |
| D07 | 20 | « Enlever le num » | J+C | Q3 |
| D08 | tous | Dessiner les bornes de la boîte de jonction +BJM | J+C | Q4 |
| D09 | tous | Cadre pointillé autour des appareils hors armoire | C | — |
| D10 | tous | Localisations +1 armoire, +2 IHM… | J+C | Q5 |
| D11 | tous | Vérifier 24 V et 0 V des drivers et des E/S automate | C | — |
| D12 | tous | **Important** : dessiner les câbles 27G1 (W11) et 19G1 (W12) | C | — |
| D13 | 21 | Renvoi de folio manquant | C | — |
| D14 | 21 | Bloc noir X21.14 mal dessiné | C | — |
| D15 | 30 | Écrire les adresses IP | J+C | Q6 |
| D16 | 31, 32 | Fils STO et 24 V mal tracés | C | — |
| D17 | 31, 32 | **Important** : revoir le câblage des freins ; rotation manuelle en essai | J+C | Q7 |
| D18 | 03 | Synoptique avec les localisations (+P1…) et des cadres | C | Q5 |
| D19 | 60 | Renvois du haut à l'horizontale | C | — |
| D20 | 60 | Rendre clair le « L+ des sorties » | J+C | Q8 |
| D21 | 61 | Réserve : un seul groupe de 4 broches | C | — |
| D22 | 62 | Recentrer la colonne lumineuse H1 | C | — |
| D23 | 62 | Pas de bornes pour le voyant H4 | J+C | Q2 |
| D24 | 70 | Borniers dessinés comme un vrai schéma de bornier | J+C | Q9 |
| D25 | automate | Krizox pour l'automate ; mnémoniques importants | J | Q10 |

## Détail

### D01 · f10 · Brins du câble client W1 (C)
- Krizox : « Le câble client ne peut pas avoir 1 2 3 4 5, seulement 1 à 4. »
- v36 : W1 « 5G4 », brins numérotés `1-2-3-4-5`.
- Compris : le 5e conducteur est le vert/jaune (PE). Il ne porte pas de numéro. Brins 1 à 4, PE repéré V/J.
- À faire : W1 en `1-2-3-4` + PE.
- Même logique possible pour les autres câbles en « G » (W9, W10 en `1-2-3-4-5`, W4) : à appliquer partout si Julien est d'accord (Q1).

### D02 · f10 · Pas de numéro de fil sur le câble client (C)
- Krizox : « supprimer f10 les numéros de câbles client car il n'y en a pas ».
- v36 : 1001 à 1004 sur le câble client (au-dessus de X10) et de X10 à QS1.
- Compris : le câble client est posé par l'installateur, il n'a pas nos repères. On garde le numéro seulement côté armoire (X10 → QS1).
- À faire : retirer les numéros du tronçon câble client → X10.

### D03 · f10 · « Incrémenter » entre câble client et QF1 (J+C)
- Krizox : « il faut peut-être incrémenter sur les fils f10 entre câble client et QF1 ».
- v36 : X10 → QS1 = 1001-1004, QS1 → QF1 = 1011-1014 : le numéro change déjà à chaque appareil.
- Pas clair. Deux lectures : a) c'est déjà fait (rien à changer) ; b) changer aussi de numéro après la borne X10, ce qui contredit la règle du 05/11 (« une borne ne change pas le numéro »).
- Question Q1.

### D04 · f12 · Supprimer les bornes du voyant H2 (J+C)
- Krizox : « supprimer borne H2 ».
- v36 : H2 (voyant 230 V de porte) par X12.21 / X12.22.
- Conflit : règle de Julien du 05/11 pour la porte : « tous les appareils par des bornes, ou aucun » (S1, S4, H2, H3, H4). Krizox demande aussi « pas de bornier pour voyant » au f62 (D23).
- Conséquences : implantation R4 à refaire (C) ; câblage déjà fait à reprendre (J).
- Question Q2.

### D05 · f13 · Supprimer les bornes des ventilateurs (J+C)
- Krizox : « supprimer borne ventilo ».
- v36 : EV1 / EV2 par X13.21 (L) / X13.22 (N). L'éclairage EL1 / EL2 a aussi ses bornes X13.11 / X13.12.
- Compris : les ventilateurs sont dans l'armoire, ils n'ont pas besoin de bornes. L'éclairage non plus ?
- Question Q2.

### D06 · f20 · Enlever un contact de KA2 (J+C)
- Krizox : « enlever un contact KA2 ».
- v36 : KA2 dessiné avec ses 3 pôles : 1-2 → U3, 3-4 → U4, **5-6 libre**.
- Deux lectures : a) ne pas dessiner le pôle 5-6 inutilisé ; b) couper les deux +48 V par un seul pôle (02_MATERIEL disait « 1 pôle (1-2) »).
- Question Q3.

### D07 · f20 · « Enlever le num » (J+C)
- Krizox : « enlever le num ».
- Pas clair : quel numéro ? (numéros de fil 2001 / 2011 entre KA2 et les drivers, numéros des brins de W9 / W10, autre ?)
- Question Q3.

### D08 · tous · Bornes de la boîte de jonction machine +BJM (J+C)
- Krizox : « rajouter des bornes pour celles du boîtier de dérivation ».
- v36 : la boîte +BJM n'est **pas dessinée** (décision de Julien du 18/11). W4 et W12 vont « vers +BJM ».
- Revient sur la décision du 18/11. Calcul du 17/11 (09_STOCK) : 57 bornes sans le pupitre, 84 avec W11.
- Il manque : quels câbles passent par la boîte (Julien 17/11 : « tous », réserves comprises ; W11 ?), et les **câbles boîte → appareils**, jamais définis (repères, types).
- À faire : Julien fixe le contenu ; Claude dessine les bornes +BJM-X1 entre la borne d'armoire et l'appareil, sur chaque folio concerné.
- Question Q4.

### D09 · tous · Cadre pointillé autour des appareils hors armoire (C)
- Krizox : « revérifier si pointillé autour symbole si extérieur armoire ».
- v36 : aucun cadre pointillé autour des appareils +M ou +P1 (seulement l'arrivée au f10 et les liaisons PROFINET).
- À faire : cadre pointillé autour de chaque appareil hors armoire (M1 à M4, B1 à B7, H1, S2, S3, P1), avec sa localisation.

### D10 · tous · Localisations +1, +2… (J+C)
- Krizox : « mettre un +1 pour armoire, +2 pour IHM, etc. ».
- v36 : +A1 armoire, +P1 pupitre, +M machine (01_PROJET).
- Krizox écrit lui-même « +P1 » dans la demande D18. Pas sûr qu'il veuille changer les noms : peut-être seulement **afficher** la localisation partout.
- Question Q5.

### D11 · tous · 24 V et 0 V des drivers et des E/S automate (C)
- Krizox : « vérifier le 24 et le 0 pour les drivers, et les entrées / sorties automate ».
- v36 (relu) : PUL+ / DIR+ / ENA+ de U3 / U4 sur Q0.0 à Q0.5 (6101-6106) ; PUL- / DIR- / ENA- au 0 V commun 1230 ; sorties CPU alimentées par 2L+ / 2M ; entrées sur L+ capt 6001 (X21.14), 1M au 0 V.
- À faire : contrôle complet par calcul (équipotentielles), puis compte rendu à Julien. Correction seulement si une erreur est trouvée.

### D12 · tous · Câbles 27G1 (W11) et 19G1 (W12) sur les folios (C) **important**
- Krizox : « important => rajouter les câbles 27G1 et 19G1 !!! »
- v36 : W11 et W12 n'apparaissent qu'aux f70, f80 et f92. Aucun câble dessiné sur les folios où passent leurs conducteurs (f41, f42, f50, f60, f62). W14 (M12 de B2) n'est pas dessiné non plus.
- À faire : dessiner W11, W12 (et W14) entre les bornes et les appareils, avec le n° de conducteur sur chaque brin (répartition validée du 05/11, 02_MATERIEL).

### D13 · f21 · Renvoi de folio manquant (C)
- Krizox : « renvoi de folio manquant ».
- v36 : les barres 24VELEC et 0 V du haut du f21 commencent dans le vide à gauche (fils en attente en (3200, 2000) et (3200, 2800), déjà dans les « attentions » du verifier).
- Compris : il manque l'origine des barres (X21.11 / X21.12 sur le même folio, ou renvoi depuis le f12).
- À faire : relier le début des barres à leur source. À confirmer avec Julien si Krizox visait un autre renvoi.

### D14 · f21 · Bloc noir X21.14 (C)
- Krizox : « bornier noir chelou, dégueu comme il est ».
- v36 : X21.14 (24 V capteurs, L+ capt de la CPU), ajouté en v28 à côté des 3 autres blocs.
- À faire : le redessiner comme les 3 autres (cadre, image, place, départs). Si Julien sait ce qui gênait Krizox (place, texte, liaison), le dire.

### D15 · f30 · Adresses IP (J+C)
- Krizox : « préciser les adresses IP ».
- Connu (dépôt TTK-AUTOMATISME, 19/11) : PC de banc 192.168.0.10 / 255.255.255.0 ; CPU et variateurs dans 192.168.0.x, **adresses à fixer**. Rien pour le switch et l'IHM.
- À faire : Julien fixe le plan d'adresses (CPU, U1, U2, IHM, switch s'il en a une, masque), et si besoin les noms PROFINET ; Claude l'écrit au f30.
- Question Q6.

### D16 · f31, f32 · Fils STO et 24 V (C)
- Krizox : « fil bleu STO et 24 dégueu ».
- v36 : renvois 24VELEC vers X5 (f21) et STO depuis le f42 (X6.1 / X6.2, chaîne U1 → U2), avec des bouts allongés en v30.
- À faire : retracer ces fils proprement (droits, sans détour ni croisement inutile).

### D17 · f31, f32 · Câblage des freins (J+C) **important**
- Krizox : « revoir aussi le câblage frein !!!! important !! vérifier la rotation manuelle pendant test ».
- v36 : chaque frein BE5 est alimenté en 400 V CA par QF2 / QF3 → KF1 / KF2 ; KF1 / KF2 commandés par KA1 13-14, **sans le variateur** et sans S3. Freins desserrés dès que KA1 est armé, y compris en Manu (voulu par Julien le 05/11, pour tourner l'arbre à la clé).
- Points possibles derrière la remarque (à confirmer) :
  - frein desserré même quand le variateur n'est pas prêt ou ne tient pas le moteur (Auto, arrêt, défaut variateur) : pas de couple de maintien ;
  - frein non piloté par la sortie frein du variateur (pratique SEW courante) ;
  - courant du frein BE5 et calibre de QF2 / QF3 toujours inconnus (05, point 8).
- « Rotation manuelle pendant test » : essai à faire (J) : en Manu, KA1 armé, l'arbre tourne-t-il à la main ? En Auto à l'arrêt ?
- Question Q7.

### D18 · f03 · Synoptique (C)
- Krizox : « remettre le synoptique avec +P1 etc. et les encadrés ».
- v36 : blocs de texte par fonction (arrivée, distribution, variateurs…), sans regroupement par lieu.
- À faire : regrouper les blocs dans des cadres par localisation (armoire, pupitre +P1, machine +M), câbles entre cadres. Dépend de Q5 pour les noms.

### D19 · f60 · Renvois du haut à l'horizontale (C)
- Krizox : « mettre les renvois de folio ligne haut en horizontale comme ligne du haut ».
- v36 : en haut du f60, le renvoi (41-E6) arrive à l'horizontale mais (41-J6) et le L+ capt (21-L7) arrivent à la verticale.
- À faire : renvois du haut à l'horizontale, alignés comme les barres 24 V / 0 V.

### D20 · f60 · « L+ des sorties » (J+C)
- Krizox : « éclaircir le L+ des sorties, car bizarre ».
- Lecture probable : le L+ capt est une **sortie** de la CPU (alimentation des capteurs). Au f60 il part vers X21.14 (f21) puis revient vers les contacts : le trajet n'est pas lisible.
- Autre lecture : le 2L+ des sorties de la CPU (f61).
- À faire : texte court près de la broche (« sortie 24 V capteurs -> -X21.14 ») ou tracé plus direct.
- Question Q8.

### D21 · f61 · Réserve en un seul groupe (C)
- Krizox : « réserve sur les 4 pins au lieu de 2 groupes de 2 ».
- v36 : Q0.6 / Q0.7 et Q1.0 / Q1.1 ont chacun leur accolade « Réserve ».
- À faire : une seule accolade « Réserve » sur les 4 broches.

### D22 · f62 · Colonne lumineuse H1 (C)
- Krizox : « recentrer les lampes colonne lumineuse ».
- À faire : centrer H1 sous ses sorties Q8.0 à Q8.2 et ses bornes X62.11-14.

### D23 · f62 · Pas de bornes pour le voyant H4 (J+C)
- Krizox : « pas de bornier pour voyant car dans l'armoire, à vérifier ».
- v36 : H4 par X62.21 / X62.22. Même question que D04 (règle de la porte).
- Question Q2.

### D24 · f70 · Borniers comme un vrai schéma (J+C)
- Krizox : « revoir schéma bornier (en plus de l'implantation déjà existante). Faire comme les schémas en vrai (see electrical) ».
- v36 : f70 = cases rangées rail par rail (comme l'implantation), f71 = tableau des bornes du pupitre.
- Compris : un **plan de bornier** classique (style SEE Electrical) : une ligne par borne, côté armoire à gauche (appareil, broche, n° de fil), côté terrain à droite (câble, n° de conducteur, appareil), ponts, butées.
- Il manque : un exemple de ce que Krizox attend (copie d'écran ou PDF d'un schéma SEE Electrical).
- Question Q9.

### D25 · Automate (J)
- Krizox : « AUTOM => krizox ; programme automate => mnémoniques importants ».
- Compris : Krizox aide (ou relit) le programme ; il insiste sur des mnémoniques clairs (table des variables TIA).
- Hors schéma : à traiter dans le dépôt TTK-AUTOMATISME. Option : écrire le mnémonique de chaque E/S sur les folios 60 à 63.
- Question Q10.

## Questions à Julien
Posées par lots de 4 au plus. Réponses notées ici, puis reportées dans la demande.
| N° | Demandes | Question | Lot | Réponse |
|---|---|---|---|---|
| Q1 | D01, D03 | « Incrémenter » au f10 : déjà fait (1001 → 1011 → 1021) ou nouveau numéro après X10 ? Brins sans PE : sur tous les câbles en « G » ? | 2 | |
| Q2 | D04, D05, D23 | Bornes des appareils de l'armoire : on retire celles de H2, H4, des ventilateurs ; et H3, S1, S4, l'éclairage ? | 1 | |
| Q3 | D06, D07 | KA2 : ne plus dessiner le pôle 5-6, ou un seul pôle pour les deux +48 V ? « enlever le num » : quel numéro ? | 1 | |
| Q4 | D08 | Boîte +BJM : quels câbles y passent (W11 ?), et quels câbles boîte → appareils ? | 2 | |
| Q5 | D10, D18 | Localisations : renommer (+1, +2…) ou garder +A1 / +P1 / +M et les afficher partout ? | 1 | |
| Q6 | D15 | Plan d'adresses IP (CPU, U1, U2, IHM, switch, masque) ? | 2 | |
| Q7 | D17 | Freins : qu'est-ce qui gêne Krizox exactement ? | 1 | |
| Q8 | D20 | « L+ des sorties » : le L+ capt (f60) ou le 2L+ (f61) ? | 2 | |
| Q9 | D24 | Exemple de bornier SEE Electrical voulu par Krizox ? | 2 | |
| Q10 | D25 | Mnémoniques : seulement dans TIA, ou aussi sur les folios 60 à 63 ? | 2 | |
