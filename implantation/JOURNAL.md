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

**Statut** : commitée et poussée le 05/11 (a680718), remplacée par la v7.

## v7 — 05/11/2026
Fichiers : `release/TTK_implantation_2026-11-05_v7.drawio` + `.pdf` ; v6 dans `old/`.
- Câble frein unique = W3 (W6 supprimé) ; -XR2 validé par Julien.
- W11 / W12 (Q32) : toujours en attente de Julien.

**Statut** : commitée et poussée le 05/11 (9483376), remplacée par la v8.

## v8 — 05/11/2026 (schéma v19)
Fichiers : `release/TTK_implantation_2026-11-05_v8.drawio` + `.pdf` ; v7 dans `old/`.

**Prises en compte (v17 à v19)** : freins = W4 (W7 supprimé), TF = W3 / W6 ; W11 (27G1) et W12 (19G1) validés, ordre des bornes = n° de conducteur ; colonne H1 X61.11-14 ; bornes de porte X40.11-12, X12.21-22, X21.21-22, X61.21-22 ; butées entre fonctions et autour des TF (Q39) ; W13 V/J 4 mm² vers le bâti (sur XPE1).

**Bornier** : 88 bornes (R5 : 74, R4 : 14), 20 butées, 18 capots.
- R5 t1 : W11 (AU S2 | S3 | IHM) | W12 (B1 | B3-B6 | H1) — 286 / 320 mm.
- R5 t2 : B2, B7 | TF W3 + W6 | — 89 / 95 mm. t3 : W9, W10 — 66 / 70 mm.
- R5 t4 : W4 (M1 | M2) | W2 | W5 | W1 — 169 / 220 mm.
- R4 à droite de XR2 : H2 230 V | porte S1, S4, H3, H4 — 97 / 113 mm.

**Choix à valider** : porte sur R4 (plus de place sur R5 avec les butées) ; pas de butée entre B2 / B7 et entre W9 / W10.
**Passe-câbles** : W4 en CEM M20 (1 à acheter), W3 / W6 en CEM M16, W13 en M16 (à acheter).

**Retours de Julien (05/11)** : porte sur R4 validée ; butées 10 mm, stock suffisant. Schéma v20 généré par Julien, pas encore ouvert : implantation en attente.

**Statut** : commitée et poussée le 05/11 (f622e2b), remplacée par la v9.

## v9 — 06/11/2026 (schéma v22)
Fichiers : `release/TTK_implantation_2026-11-06_v9.drawio` + `.pdf` ; v8 dans `old/`.

**Prises en compte (v20 à v22)** : X21.11-13 = PTFIX 6/12X2,5 (RD / BU / GY) ; porte dans l'ordre du f70 (S1, S4, H3, H4, H2 au bout) ; règle « une butée de chaque côté de chaque appareil sur tous les rails » ; 89 bornes (88 sur R5 / R4 + X12.11).

**Placement**
- R2 : QF2-KF1 | QF3-KF2 (192 / 205) ; QM1-KM1-QM2-KM2 sans butée intérieure (200 / 205 ; avec butées : 230) ; XR1 ; QF1 | QS1 (223 / 230).
- R3 : X21.11 | X21.12 | X12.11 (129 / 130) ; X21.13 | FA1 | KA1 ; K1-K3 (bus) ; K4 ; KA2.
- R4 : QF4 | QF5 | QF6 | QF7 | QF8 ; QF9 | QF10 | XD1 ; XR2 | S1 | S4 | H3 | H4 (111 / 113) ; H2 seul après la vis (33 / 55).
- R5 inchangé depuis la v8.

**À vérifier** : sens de pose et largeur des PTFIX 6/12 sur rail (41 ou 28,6 mm) ; références RD / GY ; 4 bornes 4 mm à acheter (89 pour 85).

**Statut** : commitée et poussée le 06/11 (214bb78), remplacée par la v10.

## v10 — 06/11/2026 (schéma v23)
Fichiers : `release/TTK_implantation_2026-11-06_v10.drawio` + `.pdf` (2 pages) ; v9 dans `old/`.
- Julien : PTFIX 6/12 en long (41 mm) ; R2 déjà fixé (trait épais, hors étude) ; seulement le plan et le détail des borniers.
- v23 : aucune borne modifiée (STO en chaîne interne à l'armoire).
- Page 2 refaite : bornes à l'échelle ≈ 1:0,22, repère, fonction, n° de conducteur (W11 / W12), butées, capots, bandeau par câble (repère, composition, destination), étiquette par fonction.

## v11 (indice A) — 17/11/2026 (schéma v31)
Fichiers : `release/TTK_implantation_2026-11-17_v11.pdf` (10 pages A3) + `_verification.md` ; v10 dans `old/`. Généré par `generateur/` (méthode A validée par Julien).
- Reprises depuis la v10 : XR2 sur R2 à côté de XR1 ; X13.11-22 sur R4 après XD1 ; X61.1x / X61.2x → X62.1x / X62.2x ; -X21.14 noir proposé sur R3 à droite de K4.
- Bornes : côté armoire, côté extérieur, n° de fil et n° de conducteur relus dans le .xrs. B2 / B7 et TF M1 / M2 sans butée intérieure (comme v10) pour tenir avant le support 45°.
- Décisions du 17/11 : X63 gardées ; W9 / W10 en 5G1,5 ; +M-X1 ; blindage un côté ; W14 proposé (câble M12 de B2).
- Contrôle : 0 texte trop large, 0 chevauchement, 0 écart avec le .xrs ; pages rastérisées et relues.
- Ouvert : manque 4 PT 2,5 (74 pour 70) ; liaisons boîte → appareils non définies.

## v12 (indice B) — 18/11/2026 (schéma v34), PC PRO RIMANE
Fichiers : `release/TTK_implantation_2026-11-18_v12.pdf` (**2 pages A3**) + `_verification.md` ; v11 dans `old/`.
- Demande de Julien (18/11) : 2 pages seulement (plaque, détail des borniers) ; travail limité à R3, R4, R5 ; générateur gardé, draw.io abandonné.
- Page 2 refaite : tous les borniers sur une page, de haut en bas comme sur la plaque (R4, R5 t1, t2-3, t4), bornes x 1,2 (au lieu de 1,35), rangées compactes ; R3 (PTFIX 6/12, X12.11, X21.14) en dessin réduit ; légende en colonne.
- PTFIX 2X4 (Phoenix 1028361, 6 mm) pour les 38 bornes de W11 / W12 : R5 t1 finit à 469 mm (support à 477,5).
- X20.15 / X20.25 (V/J de W9 / W10, v34) ajoutées : W10 passe après le support 702,5 (722,5 à 761 mm).
- W11 / W12 : bandeau en tireté rouge « répartition à valider » (demande du 18/11).
- +M-X1 → +BJM ; XR2 « déjà fixé » (monté le 13/11).
- Contrôle : 0 texte trop large, 0 chevauchement, 0 écart avec le .xrs. Bornes : PT 2,5 36 / 70, PT 4 15 / 15, PTFIX 2X4 38 / 46, terre 6 / 4 (manque 2).
- Retours de Julien (18/11) : W11 / W12 validés (marque « à valider » retirée, v12 régénérée) ; frein W4 ok ; push accordé.
- Suite (18/11) : stock plus comparé (rapport : comptage des bornes dessinées seul) ; W14 validé ; câbles +BJM → appareils hors sujet (Julien plus tard). Reste ouvert : X21.14.

## v13 (indice C) — 20/11/2026 (schéma v36), PC PRO RIMANE
Fichiers : `release/TTK_implantation_2026-11-20_v13.pdf` (2 pages A3) + `_verification.md` ; v12 dans `old/`.
- Repris depuis les commits du 18 au 20/11 : QF10 Schneider iDT40K A9P71602 2 A (v35) ; XD1 limitée à 2 A par QF10 (v36).
- Bornes et câbles du .xrs v36 identiques à la v34 : borniers inchangés.
- Page 1 : renvoi « détail page 2 » (était « pages suivantes »).
- Contrôle : 0 texte trop large, 0 chevauchement, 0 écart avec le .xrs. Seul point ouvert : X21.14 à droite de K4.

## v14 (indice D) — 26/11/2026 (schéma v45), PC PERSO JULIEN
Fichiers : `release/TTK_implantation_2026-11-26_v14.pdf` (**3 pages A3**) + `_verification.md` ; v13 dans `old/`.
- État des lieux v36 -> v45 : 99 bornes d'armoire identiques (noms X43 / X61 / X63 / X64 déjà dans `saisie.json`), mêmes types : R3, R4, R5 inchangés.
- Réponses de Julien (26/11) : bas des bornes R5 = « +BJM X1.n » seulement ; bornier +BJM-X1 ajouté ; X21.14 à droite de K4 validé ; bornes de la boîte dessinées en largeur PT 2,5 (type à choisir).
- `extraire.py` : X1.n = côté extérieur. `generer.py` : page 3 (boîte, 2 rangées : X1.1-24, X1.25-69 ; haut = borne d'armoire, bas = appareil ; un groupe par câble, butées) ; contrôle des bornes X1 (posées une fois, conducteurs = borne d'armoire raccordée) ; comptage armoire / boîte séparé ; X21.14 plus en tireté rouge.
- Page 2 pleine : la boîte ne tenait pas, d'où la 3e page (écart à la règle « 2 pages », signalé à Julien).
- Contrôle : 0 texte trop large, 0 chevauchement, 0 écart avec le .xrs ; 3 PNG relus. Bornes : armoire PT 2,5 36, PT 4 15, terre 6, PTFIX 2X4 38 ; boîte 66 passage + 3 terre.
- Julien (26/11) : 3e page gardée.

## v15 (indice E) — 26/11/2026 (schéma v45), PC PERSO JULIEN
Fichiers : `release/TTK_implantation_2026-11-26_v15.pdf` (3 pages A3) + `_verification.md` ; v14 dans `old/`.
- Julien (26/11) : boîte en PT 2,5 ; PT 4 pour les arrivées moteurs et freins ; terre en PT 4.
- `saisie.json` (`boite.bornier`) : liste PT 4 (X1.1-3, X1.5-7, X1.9-12), largeurs PT 2,5 5,2 / PT 4 6,2 / terre 6,2 [H] ; `generer.py` : types de la boîte, comptage par type, légende de la page 3.
- Comme dans l'armoire : W9 / W10 (pas-à-pas) restent en PT 2,5.
- Contrôle : 0 / 0 / 0. Boîte : 56 PT 2,5, 10 PT 4, 3 terre (PT 4).
- Julien (26/11) : W9 / W10 en PT 2,5 et terre PT 4 à 6,2 mm confirmés. Générateur corrigé (plus de « à vérifier ») ; PDF non régénéré.

## v16 (indice F) — 26/11/2026 (schéma v45), PC PERSO JULIEN
Fichiers : `release/TTK_implantation_2026-11-26_v16.pdf` (3 pages A3) + `_verification.md` ; v15 dans `old/`.
- Demande de Julien : régénérer sans « à vérifier » (terre PT 4 6,2 mm et W9 / W10 en PT 2,5 confirmés). Seule la note de la page 3 et l'indice changent.
- Contrôle : 0 / 0 / 0, aucun point ouvert ; page 3 relue.
