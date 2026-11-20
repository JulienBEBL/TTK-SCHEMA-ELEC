# 09 · Stock : câbles et bornes (1 armoire)

Créé le 17/11/2026. **18/11 : Julien ne veut plus de suivi du stock (« oublie les histoires de stock ») ; fichier gardé pour mémoire, ne plus en tirer de « manque ».** **Source unique** du matériel disponible pour les câbles et les bornes.
Principe de Julien (17/11) : **on ne commande plus rien**, sauf urgence ou problème grave. Le schéma s'adapte au stock.
Statuts : [C] confirmé par Julien ou document ; [?] à vérifier. Ce fichier est à valider ligne par ligne par Julien (méthode du 17/11, étape 1).

## Méthode (Julien, 17/11) [D]
- La vérité est fixée **hors du schéma**, dans le classeur `cablage/TTK_CABLES.xlsx` (Excel, importable dans Google Sheets). Le schéma est ensuite corrigé pour le suivre (script `ttk_schema.py`).
- Portée : **seulement les câbles qui sortent de l'armoire**.
- On raisonne en **type de câble et fonction, jamais en mètres** (Julien 17/11) : s'il manque des mètres, Julien rachète. Distinguer un manque de longueur (hors sujet) d'un **câble non prévu ou non attribué** (vrai manque). Statuts d'une liaison : « En stock, attribué », « En stock, à attribuer », « Pas de câble prévu ».
- Ordre : 1) les câbles en stock (onglet « Stock câbles », d'après le fichier de suivi de commande de Julien) ; 2) la répartition par fonction (onglet « Liaisons » : moteur, frein, sonde, pas-à-pas, capteurs, signalisation, pupitre, réseau, terre) ; 3) conducteur → borne ; 4) références réelles des bornes, données une par une par Julien.
- Un onglet validé (colonne « Validé ») est exporté en CSV dans `cablage/` pour être lu par l'assistant, puis reporté au schéma.
- Lecture du classeur par l'assistant : `outils/lire_tableau.py` (`lire_xlsx`, sans openpyxl).

## Câbles
Tableau dans `cablage/TTK_CABLES.xlsx` (onglets « Stock câbles » et « Liaisons »), refait le 17/11 sans longueurs.
- Stock donné par Julien le 17/11 [C] : 2 x 0,75 (PPMM0180), 4G2,5 blindé (moteurs), 5G1,5 LIYCY-JZ (2 commandes), 27G1, 19G1, câble de compensation K (Julien écrit « 2363958 », la commande dit **RS 236-3959**).
- Fichier de commande : `Downloads/Demande de Commande Hugo.xlsx` (17/11). Câbles reçus mais absents de la liste de Julien : M12 SICK 285-9453, Roline 616-2586, fil V/J 4 mm² 811-4463 [?]. H05VV-F 2 x 1 (PPMM0114) et 2 x 0,75 (PPMM0104) : commandés, réception non notée [?].
- Julien : 19G1 et 27G1 partent tous deux de l'armoire vers la machine ; l'affectation de leurs conducteurs est celle du schéma.
- Pas de câble prévu : boîte +BJM → freins M1 / M2, B1, B3-B6, H1 (**Julien 17/11 : pas de câble prévu pour l'instant**).
- Réponses du 17/11 [C] : M12 SICK 285-9453, Roline 616-2586 et fil V/J 4 mm² 811-4463 **en stock** ; H05VV-F 2 x 1 et 2 x 0,75 **pas en stock** ; 27G1 = pupitre +P1 (posé sur la machine).
- Onglet « Conducteurs » (17/11) : un conducteur par ligne (câble, n°, borne, n° de fil, côté armoire, côté terrain, fonction, famille, statut), relevé du schéma v31. Libres : W11 23-26, W12 17-18, 4 conducteurs de W14.
- Onglet « Composants » (17/11) : chaque broche de chaque appareil hors armoire (S2, S3, P1, B1-B7, H1, M1-M4), relevée dans le .xrs v31 par équipotentielles ; statut raccordée / via +BJM / réserve / à vérifier. Résultat : toutes les broches dessinées sont raccordées, sauf B2 33-34 (réserve).
- Vision élec (Julien 17/11) : l'onglet Conducteurs et l'aperçu câbles ne montrent ni PN4 ni la sortie de la boîte (celle-ci reste dans l'onglet Liaisons, statut « Pas de câble prévu »).
- Aperçus gardés dans le dépôt (Julien 17/11) : `cablage/REFERENTIEL_CABLE.html`, `cablage/REFERENTIEL_COMPOSANT.html`. À refaire si un onglet change.
- **Boîte de jonction machine +BJM** (nom donné le 17/11, ancien +M-X1 ; bornier +BJM-X1). **Hypothèse de Julien (17/11) : tous les conducteurs de tous les câbles passent par la boîte**, réserves comprises ; onglet « Boîte BJM ». Sans le pupitre W11 : **57 bornes** (6 PT 4 pour U V W des moteurs, 44 PT 2,5, 7 terre), 11 groupes, **447 mm de bornes, rail ≈ 490 mm**. Avec W11 : **84 bornes** (6 PT 4, 70 PT 2,5, 8 terre), 12 groupes, **599 mm, rail ≈ 640 mm**. Ordre du rail : 400 V (W2, W5, W4) | 48 V (W9, W10) | TF (W3, W6) | W12 | W14 | W8 | terre | W11. Calcul : PT 4 6,2 mm, PT 2,5 et terre 5,2 mm, butée 10 mm de chaque côté de chaque groupe, embout 2,2 mm, rail + 2 x 20 mm. Julien rachète des PT si besoin.
- Julien a demandé un aperçu visuel des câbles le 17/11 (widget dans le chat, pas un rendu du schéma) : exception à la règle « pas d'aperçu » quand il le demande.

## Fil de câblage intérieur (Julien 20/11) [C]
| Section | Couleurs en stock |
|---|---|
| 1 mm² | blanc, bleu, gris, violet, orange |
| 1,5 mm² | rouge, bleu |
| 2,5 mm² | gris, noir, bleu, vert-jaune |
| 4 mm² | noir, vert-jaune, bleu |
| ≈ 1 ou 1,5 mm² (non identifié) | 2 bobines noires, 2 bobines bleues |

- Bleu clair ou foncé : non précisé [?]. Manques par rapport au besoin (05, 20/11) : 1,5 mm² noir (peut-être les bobines non identifiées), 1,5 mm² vert-jaune (2,5 mm² V/J à la place, sans souci), bleu foncé 24 V si les bleus sont clairs [?].

## Bornes et accessoires
| Article | Référence | Stock | Dessinées au schéma (v31) | Statut |
|---|---|---|---|---|
| Borne PT 2,5 | Phoenix 3209510 | 70 (20 + 50) | 36 (v32) | [C 17/11] ; [D 18/11] tout le rail R4 (porte, X13) |
| Borne PT 4 | Phoenix 3211757 | 15 | 15 (v32) | [D 18/11] arrivée X10.12-15, moteurs X31.12-14 / X32.12-14, freins X31.31-32 / X32.31-32 ; + X12.11 [H] |
| Bloc distributeur PTFIX 2X4 | Phoenix 1028361 | ? | 38 points (v32) | [D 18/11] bornes des appareils des câbles 27G1 (W11) et 19G1 (W12). Bloc de passage classique, **2 trous**, **6 mm** (Julien 18/11). Julien : « 19 et 27 » blocs ; réserves non bornées, X50.13 en terre (Julien 18/11) : 38 blocs utilisés |
| Borne de terre | RS 708-1687 (Phoenix 3211867) | 4, en livraison | **6** (X10.11, X31.11, X32.11, X50.13 ; + X20.15, X20.25 en v34) | [C 17/11] ; **manque 2** [?] (V/J de W9 / W10, Julien 18/11) |
| Bloc PTFIX 6/12X2,5 | Phoenix 3273354 (couleurs RD, BK, GY, BU) | 4 | 4 (X21.11 à X21.14) | [C 16/11] référence par couleur [?] |
| Butées d'arrêt | ? | 50 + 60 + 50 (tous projets) | 20 (implantation v8) | [C 05/11] référence [?] |
| Répartiteur 4P 125 A 7 départs | AEE300427 | 2 | XR1, XR2 (non dessinés) | [C] |
| Bornier de terre 27 | Legrand 404839 | 1 | XPE1 (non dessiné) | [C] |
| Couvercles, ponts, repères de borne | ? | ? | — | [?] à relever |
