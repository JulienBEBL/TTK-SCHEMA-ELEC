# Retours de Julien sur la v37 (23/11/2026, captures WinRelais) : à faire en v38

Statut : **questions posées à Julien (24/11), réponses attendues avant la v38.**

## Défaut commun (diagnostic de l'assistant, à corriger en priorité)
Les numéros de fil (verticaux, taille 300, ≈ 650 de long) tombent sur :
- l'**ellipse pointillée** que WinRelais dessine autour d'un câble blindé (≈ ±350 autour du trait, un peu au-delà des brins) ;
- le **cadre arrondi du repère** de câble (« W11 », ≈ 1000 x 500, dessiné même avec `court=True`) ;
- les **numéros de brin** (écrits au croisement) ;
- les **bords des cadres pointillés** +BJM / +M / +P1.
Cause : `xrs_chevauchements.py` ne connaît ni ces dessins de câble ni les cadres (dessins) ; rangées trop serrées (400 à 800 entre borne / câble / boîte / appareil).
Méthode prévue :
1. Ajouter au contrôle : ellipse, cadre du repère, numéros de brin, bords des cadres pointillés (tailles mesurées sur les captures : points de grille = 400).
2. Aérer : ≈ 1600 libres de chaque côté d'un câble ; cadres qui ne coupent ni numéro ni câble.
3. v38 seulement si ce contrôle est à 0.

## Demandes par folio
| Folio | Demande de Julien |
|---|---|
| 12 | Texte PE à gauche du fil (sinon difficile à lire) |
| 13 | Égaliser la hauteur totale de chaque colonne |
| 20 | Beaucoup trop d'infos en bas, illisible ; textes des moteurs centrés sur le cercle du symbole (plus haut) |
| 31, 32 | Harmoniser la hauteur des numéros de fil (X5 / X6) ; numéros cachés par les cadres pointillés |
| 40 | Numéros de fil peu visibles (borne X40.11 de S4) : espacer |
| 41 | Illisible (câble W11, numéros) : refaire propre |
| 42 | Pareil que f41 |
| 43 | Espacer, on ne voit rien |
| 50 | Pareil que f43 (IHM, boîte, W11) |
| 60 | Illisible ; proposition de Julien : modifier les symboles, un folio alimentation + PROFINET de la CPU, puis un folio d'entrées seules en f61 ; adapter / décaler les autres f6x |
| 62 | Illisible aux bornes de la colonne lumineuse (X62.11-14, W12, +BJM) |
| 63 | Texte superposé (W8, +BJM, 1230 / 1241) : à revoir |
| 71-73 | Plans de bornier : **bien, c'est la forme voulue** ; supprimer la note en haut (à retravailler plus tard) |

## Questions posées (24/11), réponses attendues
1. Découpe du f60 : renommer bornes (X60 -> X61, X62 -> X63, X63 -> X64) et numéros de fil (60xx -> 61xx…) ? Repères déjà posés ? Choix : a) tout renommer ; b) découper sans renommer ; c) f60 = entrées, alimentation + PROFINET CPU sur un nouveau f64.
2. Place : accepter plus de folios (ex. entrées sur 2 folios) ou numéros de fil en taille 250 ?
3. f20 : arrêter le V/J de W9 / W10 à la borne de terre avec « V/J non raccordé », sans fil jusqu'en bas ?
4. f13 : « égaliser » = aligner le bas des 3 colonnes (éclairage, ventilation, prise XD1) ?

Après les réponses : faire la v38, commit + push (sync).
