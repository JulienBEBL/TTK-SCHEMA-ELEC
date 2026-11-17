# 09 · Stock : câbles et bornes (1 armoire)

Créé le 17/11/2026. **Source unique** du matériel disponible pour les câbles et les bornes.
Principe de Julien (17/11) : **on ne commande plus rien**, sauf urgence ou problème grave. Le schéma s'adapte au stock.
Statuts : [C] confirmé par Julien ou document ; [?] à vérifier. Ce fichier est à valider ligne par ligne par Julien (méthode du 17/11, étape 1).

## Méthode (Julien, 17/11) [D]
- La vérité est fixée **hors du schéma**, dans le classeur `cablage/TTK_CABLES.xlsx` (Excel, importable dans Google Sheets). Le schéma est ensuite corrigé pour le suivre (script `ttk_schema.py`).
- Portée : **seulement les câbles qui sortent de l'armoire**.
- Ordre : 1) les câbles en stock (onglet « Stock câbles », d'après le fichier de suivi de commande de Julien) ; 2) la répartition par fonction (onglet « Liaisons » : moteur, frein, sonde, pas-à-pas, capteurs, signalisation, pupitre, réseau, terre) ; 3) conducteur → borne ; 4) références réelles des bornes, données une par une par Julien.
- Un onglet validé (colonne « Validé ») est exporté en CSV dans `cablage/` pour être lu par l'assistant, puis reporté au schéma.
- Lecture du classeur par l'assistant : `outils/lire_tableau.py` (`lire_xlsx`, sans openpyxl).

## Câbles
Tableau dans `cablage/TTK_CABLES.xlsx`, onglet « Stock câbles » (pré-rempli le 17/11 depuis la mémoire, valeurs inconnues = « ? », à valider par Julien).

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
