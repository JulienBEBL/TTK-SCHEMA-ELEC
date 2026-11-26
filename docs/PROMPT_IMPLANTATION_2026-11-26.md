# Prompt : nouveau chat pour refaire l'implantation de l'armoire (26/11/2026)

---

Tu reprends le **dossier d'implantation de l'armoire +A1** du projet TTK (machine de tressage, schéma sous WinRelais). Je suis Julien. Tu travailles **seulement sur l'implantation**, pas sur le schéma.

## 1. Avant de me répondre
- Dépôt : `C:\Users\Julien\Documents\10. TTK\TTK-SCHEMA-ELEC` (PC perso). Toujours des chemins absolus.
- `git pull --rebase`.
- Lis `CLAUDE.md`, puis `memoire/` en entier : README, 10_REPRISE_AUTRE_MODELE, puis 01 à 09. **Surtout `memoire/08_IMPLANTATION.md`.**
- Lis aussi `implantation/README.md`, `implantation/JOURNAL.md`, `implantation/release/TTK_implantation_2026-11-20_v13_verification.md` et les rapports du schéma `docs/RAPPORT_v37_2026-11-23.md` à `docs/RAPPORT_v45_2026-11-26.md` (ce qui a changé depuis la v13).

## 2. Où on en est
- Implantation actuelle : **v13, indice C** (20/11, faite sur le schéma v36). 2 pages A3 : plan de la plaque, détail des borniers.
- Schéma actuel : **v45** (`schema/generes/release/TTK_2026-11-26_v45.xrs`). `extraire.py` le lit sans erreur : 168 bornes, 37 câbles.
- Générateur : `implantation/generateur/` (`extraire.py` → `donnees.json`, `generer.py` + `svg.py` → PDF par Edge). Données à la main : `saisie.json`.
- Changé au schéma depuis la v36, à reporter :
  - boîte de jonction machine **+BJM** (bornier X1, 69 bornes, hors armoire) ; tous les câbles sortants y passent ;
  - bornes renommées : X41.21-24 / 31-34 / 41-44 → **X43.11-14 / 21-24 / 31-34** (v37) ; X60 → **X61**, X62 → **X63**, X63 → **X64** (v38) ;
  - câbles W8, W11, W12, W14 : folios et origines corrigés dans `saisie.json` (26/11) ;
  - QM1 / QM2 : **GV2ME10** (26/11, mêmes dimensions que le GV2ME14).
- Point ouvert de la v13 : -X21.14 à droite de K4 sur R3 (proposé, non validé).

## 3. Ce que j'attends
1. D'abord un **état des lieux, sans rien générer** : compare `donnees.json` tiré de la v45 à celui de la v36 (bornes, groupes, câbles, conducteurs). Dis-moi ce qui change sur R3, R4, R5, ce qui ne tient plus sur les rails, et ce que tu proposes. Au plus 4 questions numérotées.
2. Après mon GO : implantation **v14, indice D** (`saisie.json` : version, indice, date, révisions ; ancien PDF et sa vérification dans `old/`).
3. Contrôle : **0 texte trop large, 0 chevauchement, 0 écart avec le .xrs** dans le `_verification.md`.
4. Mettre à jour `implantation/JOURNAL.md`, `memoire/08_IMPLANTATION.md`, `docs/DECISIONS.md`, `docs/JOURNAL_ECHANGES.md`.

## 4. Règles
- **Ne jamais toucher au schéma** : ni `outils/ttk_schema.py`, ni les `.xrs`. Si le schéma doit changer, tu me le dis.
- 2 pages seulement. Travail limité à R3, R4, R5 (R1, R2, variateurs, résistances, alimentations déjà fixés).
- Règles de montage : une butée de chaque côté de chaque groupe ; zones des vis et supports à 45° libres ; bornes de la porte sur R4.
- Aucune valeur inventée : « ? » ou « à vérifier ». Travailler avec le matériel déjà commandé. Le stock n'est plus suivi : compter les bornes dessinées, sans comparer au stock.
- Contrôle visuel : les PNG du générateur (`--png <scratchpad>`) sont permis pour l'implantation.
- `extraire.py` réécrit `donnees.json` : après un essai, `git checkout` ce fichier.
- Commit préfixé `[PERSO JULIEN]`, `git pull --rebase` avant. **Pas de push sans mon accord.**
- Français, phrases courtes. Contester un choix une fois, puis suivre ma décision.
- Consigner chaque échange (journal, décisions, `memoire/08`).

---
