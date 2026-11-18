# 08 · Dossier d'implantation +A1 (généré)

Créé le 17/11/2026. Version actuelle : **v11, indice A** (17/11, schéma v31), **en attente des retours de Julien**.

## Demande de Julien (17/11) [D]
Un seul PDF, dans cet ordre :
1. Garde, sommaire, indice de révision.
2. Charte (règles de dessin du dossier).
3. Implantation : plaque, borniers dessinés comme en vrai (porte / pupitre si utile).
4. Liste des câbles, une ligne par câble : repère | fonction | origine | destination | type | référence | conducteurs × section | blindage | longueur | statut | folio. Puis l'affectation des conducteurs de chaque câble multiconducteur.
5. Synoptique : flèches repérées comme dans la liste.

Méthode : étape 0 → charte → implantation → câbles → synoptique → assemblage → vérification. Rien d'inventé (« ? » ou « à vérifier »), une seule livraison puis attente des retours. Méthode A retenue (SVG → PDF par Edge, rastérisation PNG permise pour le contrôle visuel).

## Contenu de la v11 (10 pages A3 paysage)
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

## Faire une nouvelle version
1. `git pull` ; passer l'ancien PDF + son `_verification.md` dans `implantation/old/` (`git mv`).
2. `saisie.json` : `version`, `indice` (lettre suivante), `date`, ligne dans `revisions`.
3. `cd implantation/generateur` ; `python -I extraire.py` ; `python -I generer.py --png <scratchpad>`.
4. Contrôle 0 / 0 / 0 dans le `_verification.md` ; regarder les PNG.
5. `implantation/JOURNAL.md`, `docs/DECISIONS.md`, `docs/JOURNAL_ECHANGES.md`, ce fichier ; commit préfixé `[PRO JULIEN]` ; **push seulement avec l'accord de Julien**.
