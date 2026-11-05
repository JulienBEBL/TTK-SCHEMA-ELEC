# Journal de l'implantation +A1

## v1 — 04/11/2026 (schéma v16)
Fichiers : `release/TTK_implantation_2026-11-04_v1.drawio` (4 pages : plaque, bornier R5, porte gauche, passe-câbles) + `.pdf` (A3).
Versions précédentes (indices A à K, 13 au 15/10, avant le dépôt) : `old/`.

**Base conservée (déjà fixée, d'après Julien le 04/11)** : goulottes, rails R0 à R5 et leurs vis, supports 45° de R5, alimentations T1 / T2 / T3, variateurs U1 / U2, résistances R1 / R2 (géométrie de l'indice K). Hypothèse : le montage suit l'indice K (à confirmer, Q1).

**Changements par rapport à l'indice K**
- Repères v16 partout (T1-T3, U1-U4, QF1-QF10, QM, KM, KF, KA1, KA2, FA1, K1-K4, XD1 = prise).
- Retirés (non utilisés, revue §5) : A9F74203 / A9F74201, contacteur 24 V commuté, 2e répartiteur, LADN11, parafoudre.
- Ajoutés : FA1 (CMC101) à gauche de KA1, QF10 (iDT40K) entre QF9 et XD1, KA2 sur R3 à droite (près de U3 / U4), X21 (1 support PTFIX, 3 blocs) + X12.11 sur R3.
- R5 : 80 bornes v16 groupées par destination : porte (S1), +P1 pupitre, +M signaux (+ 4 réserves H1), thermocouple, pas-à-pas, moteurs M1 / M2, réseau W1. Plus de collecteur XPE ni de borne PE0 : bornes de terre v16 (X10.11, X31.11, X32.11, X50.13).
- Placement contraint par les vis déjà posées : chaque groupe tient entre deux zones de vissage, renforts de part et d'autre.
- Passe-câbles : freins W3 / W6 en blindé 5G1,5 → presse-étoupes CEM M20 (2 à acheter).

**Questions posées (04/11)** : Q1 montage = indice K ? ; Q2 repères répartiteur / bornier de terre (Q31) ; Q3 H1 et B7 côté machine ? ; Q4 modèle des bornes de terre V/J (largeur).

**Incohérences signalées au schéma** : X21.11 / X21.12 (6 points) < nombre de départs 24VELEC / 0 V ; bornes X63 (v16) contre décision du 28/10 « thermocouple en direct sur K3 » ; 11 câbles blindés pour 8 presse-étoupes CEM.

**Statut** : remplacée par la v2 (non commitée).

## v2 — 04/11/2026
Fichiers : `release/TTK_implantation_2026-11-04_v2.drawio` + `.pdf` ; v1 déplacée dans `old/`.

**Réponses de Julien (04/11)**
- Barrette PE Legrand 404839 vissée directement sur la plaque (pas de rail R0). Pas de repère pour la barrette ni pour le répartiteur.
- Un seul répartiteur AEE300427 ne suffit pas. En stock par armoire : 1 RS 868-0720, 2 AEE300427. Julien veut répartir avec les PTFIX 6/12X2,5 (RD, BK, GY, BU).
- Rails : rôles conservés (R1 alim / variateurs, R2 arrivée et puissance, R3 CPU, R4 drivers, R5 borniers à 45°) ; écarts entre rails un peu modifiés.
- Bornes de terre : RS 708-1687 = Phoenix 3211867, 5,2 mm [C fiche RS].

**Changements**
- Rail R0 supprimé ; barrette PE dessinée sur la plaque, position à relever.
- Répartiteur AEE300427 retiré de R2. Distribution L1 / L2 / L3 / N par 4 PTFIX 6/12X2,5 (1 par pôle) sur R4, segment libre.
  [C fiche Phoenix 3273366] 12 départs push-in 0,14-4 mm² (24 A), 1 entrée 0,5-10 mm² (41 A), 450 V, 41 × 28,6 × 21,7 mm.
  Besoin par pôle (v16) : L1 6, L2 4, L3 7, N 7 → réserve 6 / 8 / 5 / 5.
- X21 : 3 supports PTFIX 6X1,5 (24VELEC RD, 0 V BU, 24VSEC BK) ; nombre de blocs à fixer au schéma.
- Bornes de terre R5 : 5,2 mm.

**Questions (04/11)** : cotes réelles des rails (Y) et des vis (X) ; position de la barrette PE ; contenu réel de R4 (drivers sur rail ?) ; H1 / B7.

## v3 — 04/11/2026
Fichiers : `release/TTK_implantation_2026-11-04_v3.drawio` + `.pdf` (5 pages) ; v2 dans `old/`.

**Décisions de Julien (04/11)** : pas de PTFIX 6/12 pour le 400 V / neutre ; 2 répartiteurs AEE300427 ; fil 4 mm² uniquement ; barrette PE à la même position, vissée sur la plaque (sans rail).

**Changements**
- PTFIX 6/12 retirés de R4.
- RÉP1 et RÉP2 (AEE300427, sans repère) sur R2, à gauche de QF1. [C fiche Achat Electrique] entrée 10-35 mm², 2 départs 6-16 mm², 5 départs 1,5-6 mm², 4 modules.
- Avec du 4 mm², seuls les 5 petits départs serrent : chaque répartiteur est alimenté par QF1 (2 fils de 4 mm² par borne de sortie de QF1, à vérifier notice Hager).
- Page 5 : affectation trou par trou. Réserve : L1 2, L2 4, L3 1, N 1. H2, QF8, QF9 : phase sur RÉP2, neutre sur RÉP1.
- Barrette PE : fixée (trait épais).

**À vérifier** : 2 conducteurs de 4 mm² par borne de QF1 (sinon RÉP2 en cascade sur RÉP1 : L3 et N à 0 de réserve) ; largeur QS1 ; cotes réelles des rails.

**Statut** : remplacée par la v4 (non commitée).

## v4 — 04/11/2026
Fichiers : `release/TTK_implantation_2026-11-04_v4.drawio` + `.pdf` ; v3 dans `old/`.

**Réponses de Julien (04/11)** : drivers U3 / U4 vissés sur la plaque (pas sur rail) ; la borne de QF1 n'accepte pas 2 × 4 mm² ; un câble entre RÉP1 et RÉP2 pour chaque phase et pour le neutre.

**Changements**
- QF1 → RÉP1 : 1 fil 4 mm² par pôle, dans un petit départ. RÉP1 → RÉP2 : 1 pont 4 mm² par pôle (L1, L2, L3, N).
- Page 5 réaffectée. RÉP1 : QM1, QM2, freins, neutres T1-T3. RÉP2 : phases T1-T3, H2, QF7-QF9 (phase et neutre sur le même répartiteur).
- Réserve : L1 1, L2 3, L3 0, N 0.
- U3 / U4 : « vissé sur la plaque », position à relever.

**À vérifier** : courant admissible par petit départ AEE300427 (le trou d'arrivée de RÉP1 porte tout le courant de QF1) ; calibre de QF1.

**Statut** : commitée et poussée le 05/11 (2f35189), remplacée par la v5.

## v5 — 05/11/2026
Fichiers : `release/TTK_implantation_2026-11-05_v5.drawio` + `.pdf` ; v4 dans `old/`.

**Demandes de Julien (05/11)** : QS1 deux fois plus large que dessiné ; borniers R5 groupés par câble ; place réservée pour le thermocouple B7. Cotes réelles des rails : non disponibles.

**Changements**
- QS1 : 140 mm (à mesurer). R2 tronçon droit : QF1 + QS1. RÉP1 sur le tronçon précédent de R2. RÉP2 déplacé sur R4 (tronçon libre, à côté des QF4-QF10 qu'il alimente) ; ponts RÉP1 → RÉP2 par la goulotte verticale.
- R5 : un groupe par câble, capot de fin + repère de câble entre groupes, renforts aux bouts de tronçon seulement.
  Ordre : porte S1, +P1, capots B1 / B2, FdC B3 à B6, H1 (réserve) | B7 (réserve) | W9, W10 | W4, W7, cloison TBTP / 400 V, W3, W6, W2, W5, W1.
- Freins dessinés en 2 câbles W3 / W6 (schéma v16).

**À trancher** : un câble frein unique pour M1 + M2 (boîte de dérivation côté machine) ; FdC B3-B6 : 2 ou 3 fils ; câbles capteurs (un par capteur ou multiconducteur) ; référence de la cloison.

**Statut** : commitée et poussée le 05/11 (b46ddb3), remplacée par la v6.

## v6 — 05/11/2026
Fichiers : `release/TTK_implantation_2026-11-05_v6.drawio` + `.pdf` ; v5 dans `old/`.

**Réponses de Julien (05/11)** : freins M1 + M2 dans un seul 5G1,5 ; boîte de dérivation dans la machine ; capteurs en câble multiconducteur ; FdC de translation : 2 bornes par contact ; cotes au montage gérées par Julien.

**Changements**
- R5 : groupe « Freins M1+M2 5G1,5 » (X31.31-32, X32.31-32 + 1 borne PE à créer au schéma).
- Pupitre = W11 (27G1), boîte de jonction = W12 (19G1 : B1, B3-B6, colonne H1 X61.11-14 à créer), B2 par son câble M12 : proposition Q32 du schéma, en attente de validation.
- Repères : XR1 (décision 05/11), XR2 (proposé), XPE1 (décision 05/11).
