# 09 · Stock : câbles et bornes (1 armoire)

Créé le 17/11/2026. **Source unique** du matériel disponible pour les câbles et les bornes.
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
- Pas de câble prévu : boîte +M-X1 → freins M1 / M2, B1, B3-B6, H1 (**Julien 17/11 : pas de câble prévu pour l'instant**).
- Réponses du 17/11 [C] : M12 SICK 285-9453, Roline 616-2586 et fil V/J 4 mm² 811-4463 **en stock** ; H05VV-F 2 x 1 et 2 x 0,75 **pas en stock** ; 27G1 = pupitre +P1 (posé sur la machine).
- Onglet « Conducteurs » (17/11) : un conducteur par ligne (câble, n°, borne, n° de fil, côté armoire, côté terrain, fonction, famille, statut), relevé du schéma v31. Libres : W11 23-26, W12 17-18, 4 conducteurs de W14.
- Julien a demandé un aperçu visuel des câbles le 17/11 (widget dans le chat, pas un rendu du schéma) : exception à la règle « pas d'aperçu » quand il le demande.

## Bornes et accessoires
| Article | Référence | Stock | Dessinées au schéma (v31) | Statut |
|---|---|---|---|---|
| Borne PT 2,5 | Phoenix 3209510 | 70 (20 + 50) | 74 | [C 17/11] **manque 4** |
| Borne PT 4 | Phoenix 3211757 | 15 | 15 | [C 17/11] |
| Borne de terre | RS 708-1687 (Phoenix 3211867) | 4, en livraison | 4 (X10.11, X31.11, X32.11, X50.13) | [C 17/11] |
| Bloc PTFIX 6/12X2,5 | Phoenix 3273354 (couleurs RD, BK, GY, BU) | 4 | 4 (X21.11 à X21.14) | [C 16/11] référence par couleur [?] |
| Butées d'arrêt | ? | 50 + 60 + 50 (tous projets) | 20 (implantation v8) | [C 05/11] référence [?] |
| Répartiteur 4P 125 A 7 départs | AEE300427 | 2 | XR1, XR2 (non dessinés) | [C] |
| Bornier de terre 27 | Legrand 404839 | 1 | XPE1 (non dessiné) | [C] |
| Couvercles, ponts, repères de borne | ? | ? | — | [?] à relever |
