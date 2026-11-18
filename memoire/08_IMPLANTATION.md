# 08 · Dossier d'implantation +A1 (généré)

Créé le 17/11/2026. Version actuelle : **v12, indice B** (18/11, schéma v34, PC PRO RIMANE), **2 pages**, en attente des retours de Julien. v11 (10 pages) dans `old/`.

## Demande de Julien (18/11) [D]
- **2 pages seulement** : plan de la plaque, détail des borniers (bornes élargies, groupes par câble / fonction). Générateur gardé, **draw.io abandonné**.
- Travail limité à R3, R4, R5 (R1, R2, variateurs, résistances, alimentations déjà fixés). Ordre de R4 confirmé : QF4 … QF10, XD1 | X13 | S1, S4, H3, H4 | vis | H2.
- Répartition W11 / W12 (Q32) à marquer « à valider » (voir 05, Q32 : contradiction avec la validation du 05/11, question posée le 18/11).
- Freins M1 + M2 : un seul 5G1,5, repère W4 inchangé.

## Demande de Julien (17/11) [D]
Un seul PDF, dans cet ordre :
1. Garde, sommaire, indice de révision.
2. Charte (règles de dessin du dossier).
3. Implantation : plaque, borniers dessinés comme en vrai (porte / pupitre si utile).
4. Liste des câbles, une ligne par câble : repère | fonction | origine | destination | type | référence | conducteurs × section | blindage | longueur | statut | folio. Puis l'affectation des conducteurs de chaque câble multiconducteur.
5. Synoptique : flèches repérées comme dans la liste.

Méthode : étape 0 → charte → implantation → câbles → synoptique → assemblage → vérification. Rien d'inventé (« ? » ou « à vérifier »), une seule livraison puis attente des retours. Méthode A retenue (SVG → PDF par Edge, rastérisation PNG permise pour le contrôle visuel).

## Contenu de la v12 (2 pages A3)
| Page | Contenu |
|---|---|
| 1 | Plaque 1100 × 1670 au 1:7 + liste des appareils (statut) |
| 2 | Borniers R4, R5 t1, t2-3, t4 (de haut en bas), bornes x 1,2 ; R3 en dessin réduit ; légende |

Points ouverts : dans `release/…_v12_verification.md` (plus de page de garde).

## Contenu de la v11 (10 pages A3 paysage, old/)
| Page | Contenu |
|---|---|
| 1 | Garde, sommaire, révisions, points ouverts |
| 2 | Charte |
| 3 | Plaque 1100 × 1670 au 1:7 + liste des appareils (statut fixe / à poser / déplacé / proposé) |
| 4-6 | Borniers R5 (2 pages), R4 + R3, à l'échelle K = 1,35 |
| 7 | Liste des câbles (17 câbles : W1-W6, W8-W14, PN1-PN4) |
| 8-9 | Affectation des conducteurs |
| 10 | Synoptique |

## Générateur (`implantation/generateur/`)
- `extraire.py` : lit **la** release .xrs (une seule dans `schema/generes/release/`) avec `outils/xrs_tool.py` + `saisie.json` → `donnees.json`.
  - Bornes rendues non passantes (`s["borne"]=False`) avant `build_nets` : chaque côté a sa propre équipotentielle.
  - Numéro de fil = fil le plus proche (même règle que `outils/xrs_numeros.py`, angle lu dans `¤#Numero¤`).
  - Côté extérieur d'une borne = côté où tous les appareils sont terrain (`B\d|M\d|S2|S3|P1|H1`) ou porte (`S1|S4|H2|H3|H4`).
- `generer.py` + `svg.py` : pages SVG en mm, PDF par Edge sans fenêtre (`--headless=new --print-to-pdf`), PNG par `--screenshot` (option `--png <dossier>`).
- Contrôle écrit dans `release/…_vN_verification.md` : textes trop larges (chasse Arial), chevauchements de textes, croisement avec le .xrs (chaque borne dessinée une fois, câbles schéma / liste / synoptique, conducteurs / borniers, compositions), comptage des bornes. **Attendu : 0 / 0 / 0.**
- Python sans module externe (`python -I`, `sys.stdout.reconfigure(encoding="utf-8")` car `-I` ignore PYTHONIOENCODING). Excel lu par `outils/lire_tableau.py` (pas d'openpyxl).

## `saisie.json` (données hors schéma, à la main)
- `document` : indice, version, date, auteur, révisions → à changer à chaque version.
- `plaque`, `goulottes`, `rails` R1-R5 (x, y, l, vis, supports ; géométrie de la v10 indice K moins le décalage (200, 160)).
- `appareils` (rep, rail, x, y, w, h, état, famille), `hors_plaque`.
- `borniers` : un par tronçon, `x0` + groupes. Options d'un groupe : `sans_butee` (suit le précédent avec son seul embout), `apres_vis` (commence après une vis).
- `types_bornes` : achetées PT 2,5 = 70, PT 4 = 15, terre = 4 ; largeurs 5,2 / 6,2 / 5,2 mm ; liste des PT 4 et des terres.
- `cables` (17), `conducteurs` (affectation par câble), `notes_conducteurs`, `boite` (+M-X1), `apres_boite`, `stock_libre`, `couleurs_cables`.

## Règles du moteur de bornier [C v10 / D Julien]
- Butée 10 mm de chaque côté de chaque groupe ; 2 groupes voisins partagent une butée. Embout 2,2 mm.
- Zones des vis et supports à 45° : 20 mm, laissées libres.
- R5 t1 x0 162,5 (W11, W12) ; R5 t2-t3 x0 512,5 (W14 B2, W8 X63, W3, W6, W9, W10) ; R5 t4 x0 788,1 (W4, W2, W5, W1) ; R4 x0 497,5 (X13, porte, H2 230 V après la vis 702,5).
- v12 : largeurs PT 2,5 5,2 / PT 4 6,2 / PTFIX 2X4 6,0 / terre 5,2 mm. R5 t1 = 152,5 à 469 (support 477,5). W10 + X20.25 sauté après le support 702,5 (722,5 à 761). t4 à partir de 778.

## Décisions prises pour la v11 (17/11)
- PC = PRO JULIEN [D]. Thermocouple : bornes X63.11 / X63.12 gardées même inutilisées [D].
- W9 / W10 = LIYCY-JZ 5G1,5 [D]. Sourcing = 1 armoire [D]. Boîte machine = +M-X1 [D]. Blindage d'un seul côté (armoire) [D].
- XR1 597,5 et XR2 669,5 sur R2 [C Julien 13/11]. X21.14 à droite de K4 sur R3 (737,5) [H]. W14 = câble M12 de B2 [H].

## Points ouverts (à trancher par Julien)
1. **4 bornes PT 2,5 manquantes** (74 pour 70). a) éclairage + ventilation en direct (libère les 4 X13) ; b) H3 / H4 en direct (casse la règle « tout par bornes ou rien »).
2. X21.14 à droite de K4 : à valider.
3. W14 : repère et référence (RS 285-9453 SICK 20 m) à valider.
4. Câbles boîte +M-X1 → appareils (freins BE5, B1, B3-B6, H1) : non définis.
5. Au schéma (script, pas l'implantation) : W9 / W10 décrits « 4 cond. » → 5G1,5 ; W11 / W12 / W14 / PN1-PN4 absents du tableau f80.
6. Sourcing : 236-3959 et 708-1687 notés non commandés (K = 0) ; PN4 20 m bleu.

## Renommage (17/11)
- La boîte +M-X1 s'appelle maintenant **+BJM** (boîte de jonction machine), bornier +BJM-X1 : `saisie.json` (`boite`, `apres_boite`) à mettre à jour à la prochaine version.

## Changé dans saisie.json le 18/11 (schéma v32)
- Types de bornes : freins X31.31-32 / X32.31-32 en PT 4, X13 en PT 2,5, nouvelle liste « PTFIX 2X4 » (W11 / W12). Le générateur ne connaît pas encore ce type : largeur **6 mm** (Julien 18/11), 2 trous ; couleur à choisir. À faire avant la v12.

- 18/11 (v33) : `cables` W4 / W12 : destination « +BJM » ; `apres_boite` B3-B6 en NF 11-12. `boite` et les autres textes « +M-X1 » restent à renommer avec le générateur.

- 18/11 (v34) : `types_bornes.terre` + X20.15, X20.25 (V/J de W9 / W10) ; origine de W9 / W10 jusqu'à X20.15 / X20.25. Implantation à régénérer (2 bornes de terre de plus sur R5).

- 18/11 (v12) : `document` v12 / B ; `types_bornes` : PTFIX 2X4 (46 en stock, 6 mm) ; X20.15 / X20.25 dans les groupes W9 / W10 et V/J de leurs conducteurs ; `boite` = +BJM (plus aucun « +M-X1 ») ; XR2 « fixe ».

## Faire une nouvelle version
1. `git pull` ; passer l'ancien PDF + son `_verification.md` dans `implantation/old/` (`git mv`).
2. `saisie.json` : `version`, `indice` (lettre suivante), `date`, ligne dans `revisions`.
3. `cd implantation/generateur` ; `python -I extraire.py` ; `python -I generer.py --png <scratchpad>`.
4. Contrôle 0 / 0 / 0 dans le `_verification.md` ; regarder les PNG.
5. `implantation/JOURNAL.md`, `docs/DECISIONS.md`, `docs/JOURNAL_ECHANGES.md`, ce fichier ; commit préfixé par le PC (`[PRO JULIEN]`, `[PRO RIMANE]`) ; **push seulement avec l'accord de Julien**.
6. PC Rimane : lancer `generer.py` hors bac à sable de l'assistant (Edge sort sinon sans PDF) ; contrôle visuel dans `build/dossier.html`.
