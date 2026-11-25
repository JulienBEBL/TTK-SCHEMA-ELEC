# 10 · Reprise (24/11/2026) : changement de modèle (Opus -> Sonnet) et compactage

À lire après CLAUDE.md et README. Résume **comment travailler** sur ce dépôt sans refaire les erreurs des v37 / v38.

## État
- Version : **v40** (`schema/generes/release/TTK_2026-11-25_v40.xrs`), rapport `docs/RAPPORT_v40_2026-11-25.md`.
- Attente : retours de Julien sur la v40 ; question du f40 (accrochage du texte des contacts).
- Lecture d'un folio par calcul (v40) : un petit script dans le scratchpad qui liste symboles (emprise, champs, broches), textes, câbles, cadres, renvois, numéros et fils d'un folio affiché ; il n'est pas dans le dépôt, à recréer au besoin.

## Méthode qui marche (à suivre à chaque version)
1. Lire la demande, noter les retours bruts dans `memoire/revues/AAAA-MM-JJ_retours_julien_vNN.md` (tableau folio / demande), **poser au plus 4 questions numérotées**, commit + push, attendre le GO.
2. Modifier **seulement `outils/ttk_schema.py`** (et `xrs_gen.py` si besoin). Folios : le script parle en **numéros internes** (table dans 04 : ex. affiché f61 = interne "50", f60 = "55", f31 = "20", f20 = "32", plans f70-f73 = "71"-"74").
3. Après chaque modification : `sh outils/controles/tout.sh <scratchpad>/essai.xrs JJ/MM/AAAA`. Tout doit être à 0 (verifier : 28 attentions connues). Ne jamais sortir une version sinon.
4. Release : `git status schema/` d'abord. Si la release a changé (WinRelais l'a réenregistrée) : la copier dans `schema/recus/AAAA-MM-JJ_vNN_ouverte_WinRelais.xrs`, comparer (symboles, fils, textes, numéros via `xrs_tool.parse`) et reprendre ses retouches ; puis `git mv` des 3 fichiers vers `old/`, générer la nouvelle avec les commandes du README (verifier, nomenclature).
5. Rapport `docs/RAPPORT_vNN_AAAA-MM-JJ.md`, mémoire (04 règles, 06 version, revues, README, DECISIONS, JOURNAL), CLAUDE.md (n° de version), commit `[PERSO JULIEN] …` + `git pull --rebase` + push.

## Pièges connus
- **Lisibilité** : WinRelais dessine autour d'un câble blindé une ellipse (±350) et un cadre arrondi autour du repère ; les cadres pointillés ont des bords. `zones_cables()` du script et `xrs_chevauchements.py` en tiennent compte. Règle d'espacement : voir 04 « Lisibilité (v38) ». Si le contrôle n'est pas à 0, **aérer** (déplacer bornes / câble / boîte), ne pas réduire les marges.
- Numéros de fil : taille `NUM_T = 200` (xrs_gen.py).
- Le contrôle ne voit **pas** les textes dessinés dans les symboles (noms de broches) : vérifier à la main les cadres autour des symboles.
- Fichiers : `ttk_schema.py` en LF, `xrs_gen.py` en CRLF : faire les remplacements avec un petit script Python (lire, `assert t.count(a) == 1`, remplacer, réécrire en gardant les fins de ligne). Écrire les gros scripts dans un fichier (pas de heredoc avec beaucoup de guillemets).
- Symboles CUSTOM : 3 copies à garder identiques : `outils/librairie/CUSTOM` (UTF-8), `librairie_winrelais/sym_electrotech/CUSTOM` et `C:\Users\Public\Documents\Elec-CAO\sym_electrotech\CUSTOM` (cp1252, CRLF).
- Bornes : renommer un folio renomme ses bornes (règle X + folio) : mettre aussi à jour `implantation/generateur/saisie.json` (sinon la nomenclature signale des bornes absentes).
- `implantation/` : ne pas régénérer le dossier sans accord ; `extraire.py` écrit `donnees.json` (le remettre avec `git checkout` après un essai).
- D'autres sessions peuvent pousser (SEW, docs) : toujours `git pull --rebase` avant de commencer et avant de pousser. Préfixe de commit unique `[PERSO JULIEN]` (25/11).

## Outils de contrôle (dans le dépôt depuis le 24/11, avant dans le scratchpad)
`outils/controles/` : `tout.sh` (génère + tout contrôle), `cadres.py` (cadres pointillés), `textes.py` (folios hors 10-69), `d11.py` (24 V / 0 V des drivers et E/S), `bornes.py` (doublons, règle X + folio, saisie.json), `bbox.py` (géométrie d'un symbole de la librairie).
