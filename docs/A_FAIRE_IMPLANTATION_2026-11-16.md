# À reporter dans l'implantation de l'armoire (schéma v29, 16/11/2026)

Pour le chat d'implantation (draw.io, dossier `implantation/`). Dernière implantation : v10 (06/11, schéma v23).
Source de vérité des bornes : f70 du schéma v29 (`schema/generes/release/`), rail par rail.

## Changements depuis la v10
| # | Changement | Rail | Détail |
|---|---|---|---|
| 1 | **XR2 déplacé** | R4 → **R2** | XR1 et XR2 collés côte à côte, sur le rail de QS1 / QF1. Le R2 est plein (Julien, monté le 13/11). Électrique inchangé : QF1 → XR1 → XR2. |
| 2 | **Bornes éclairage et ventilation** | **R4** | X13.11 (L) / X13.12 (N) éclairage EL1 / EL2 ; X13.21 (L) / X13.22 (N) ventilation EV1 / EV2. Dans la place laissée par XR2 : après XD1, avant les bornes de porte. Une butée de chaque côté de chaque groupe. |
| 3 | **Bloc PTFIX 6/12 noir -X21.14** | **R3** | 24 V capteurs, alimenté par L+ capt de la CPU, à côté des 3 autres PTFIX (posé en long, 41 mm). En stock, place OK (Julien, 16/11). |
| 4 | Bornes colonne H1 et voyant H4 renommées | R5 / R4 | X61.11-14 → **X62.11-14** (colonne, câble W12) ; X61.21-22 → **X62.21-22** (H4, porte). Position inchangée. |

## Ordre du R4 (f70)
QF4 … QF10, XD1 | X13.11-12 | X13.21-22 | S1 (X41.51-54, X60.41-42) | S4 (X40.11-12) | H3 (X21.21-22) | H4 (X62.21-22) | H2 230 V (X12.21-22).

## Ordre du R3 (f70)
X21.11 (rouge, 24VELEC) | X21.12 (bleu, 0 V) | X12.11 (PELV) | X21.13 (gris, 24VSEC) | X21.14 (noir, 24 V capteurs).

## Comptage
- 93 bornes (89 + 4 bornes X13) pour 85 achetées.
- 4 blocs PTFIX 6/12.
- Butées : une de chaque côté de chaque appareil, sur tous les rails (règle de Julien).
