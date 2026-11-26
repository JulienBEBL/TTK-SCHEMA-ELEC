# Prompt de passation (26/11/2026) : à coller au début du prochain chat

---

Reprise du projet TTK-SCHEMA-ELEC (schéma électrique de la machine de tressage TTK, sous WinRelais). Je suis Julien.

**1. Avant de me répondre**
- Dépôt : `C:\Users\Julien\Documents\10. TTK\TTK-SCHEMA-ELEC` (PC perso). Toujours des chemins absolus.
- `git pull --rebase`.
- Lis `CLAUDE.md`, puis `memoire/` en entier, dans cet ordre : README, 10_REPRISE_AUTRE_MODELE (méthode et pièges), puis 01 à 09.
- Lis aussi les 2 derniers rapports : `docs/RAPPORT_v42_2026-11-26.md` et `docs/RAPPORT_v43_2026-11-26.md`.

**2. Où on en est**
- Dernière version : **v43**, `schema/generes/release/TTK_2026-11-26_v43.xrs`.
- Tous les contrôles sont à 0 : `sh outils/controles/tout.sh <essai.xrs> JJ/MM/AAAA` (verifier : 28 attentions connues).
- Le script reproduit la v43 octet pour octet.
- Fait le 25-26/11 (v40 à v43) :
  - numéros de fil centrés sur la longueur du fil ;
  - variateur MCX91A élargi (validé) ; thermocouple retourné (symbole CUSTOM `Thermocouple_bas`) ;
  - f40 : textes des contacts à droite du contact, accrochés à gauche ;
  - plans de bornier : terre rayée vert/jaune, câble et n° de fil en gras, résumé des fonctions sous le cadre du repère ;
  - nomenclature en police 300 ; folios et origines des câbles relus sur le dessin (`saisie.json` corrigé) ;
  - mes retouches WinRelais de W1 (f10) et W9 / W10 (f20) reprises dans le script.
- J'ouvre la release dans WinRelais et je la retouche parfois. Avant toute nouvelle version :
  - faire `git status` ;
  - si la release a changé, l'archiver dans `schema/recus/` ;
  - la comparer avec `outils/controles/retouche.py`, plus les blocs ¤#DefCable ;
  - reprendre mes retouches dans le script.

**3. En attente**
- Ma relecture de la v43 dans WinRelais.
- Question ouverte : le brin V/J de W9 / W10 porte le n° 4, comme le conducteur 4 (repris de ma retouche). Voulu, ou un autre repère ?
- Implantation de l'armoire à régénérer (`implantation/`) : pas de push sans mon accord.
- Autres points ouverts : `memoire/05_POINTS_OUVERTS.md`. Notamment :
  - références à vérifier : B7, H2, H3, H4, bornes +BJM, butées ;
  - 6 bornes de terre dessinées pour 4 achetées ;
  - freins (D17), TIA, réponses écrites de SEW à reporter.

**4. Règles (rappel, détail dans CLAUDE.md et la mémoire)**
- **Fichiers du schéma**
  - Ne jamais modifier un .xrs à la main. Tout passe par `outils/ttk_schema.py` (et `xrs_gen.py`, `nomenclature.py`).
  - Ne jamais toucher `schema/modele/SCHEMA_ELEC_TTK.xrs`.
  - Je parle en numéros de folio **affichés** ; le script utilise les numéros **internes** (table `NUMFOL`).
  - Symboles CUSTOM : 3 copies à garder identiques, contrôlées par `outils/controles/symboles.py`.
  - Pour un correctif qui contient des antislashs, écrire le script Python dans un fichier, pas dans un heredoc.
- **Mes règles**
  - Pas de notes encadrées sur les folios. Pas d'aperçu image : contrôle par calcul.
  - Aucune valeur inventée (« à vérifier »). Travailler avec le matériel déjà commandé.
  - Français, phrases courtes, au plus 3-4 questions numérotées. Contester un choix une fois, puis suivre ma décision.
- **Consigner chaque échange, même une simple question**
  - Mettre à jour le fichier du thème dans `memoire/`, `docs/DECISIONS.md` et `docs/JOURNAL_ECHANGES.md`.
  - Puis commit `[PERSO JULIEN] …` et push sur `main` (`git pull --rebase` avant, jamais `--force`).
- **Pour chaque nouvelle version**
  - Noter mes retours dans `memoire/revues/`.
  - Contrôle complet (`tout.sh`) : tout doit être à 0.
  - Ancienne version dans `old/`, nouvelle dans `release/` avec ses fichiers `_verification.md` et `_nomenclature.csv`.
  - Rapport `docs/RAPPORT_vNN_*.md`. Mettre à jour la mémoire (04, 05, 06, 10, README), `CLAUDE.md` et le `README.md` racine.

Quand tu as tout lu, dis-moi en 5 lignes où on en est, puis attends mes retours sur la v43.

---
