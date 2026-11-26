# 10 · Reprise (24/11/2026) : changement de modèle (Opus -> Sonnet) et compactage

À lire après CLAUDE.md et README. Résume **comment travailler** sur ce dépôt sans refaire les erreurs des v37 / v38.

## État
- Version : **v45** (`schema/generes/release/TTK_2026-11-26_v45.xrs`), rapport `docs/RAPPORT_v45_2026-11-26.md`.
- Attente : relecture de la v45 (QM1 / QM2 en GV2ME10, réglage 6,3 A). SEW : réponse écrite reçue et reportée (`docs/RAPPORT_SEW_2026-11-26.md`), pas de relance.
- Piège (v43) : dans ce terminal, un heredoc bash passé à python transforme « \\ » en « \ » : pour un correctif qui contient des antislashs (« \u00b7 » de xrs_gen), écrire le script Python dans un fichier (outil Write).
- Placement des numéros de fil (v42) : `centre_troncon` (milieu du plus long chemin, parties libres de `troncon_libre`) ; obstacles des symboles : `obstacles_symboles` / `dessin_symbole` ; débogage : `TTK_DBG=<numéro>` affiche les positions candidates.
- Lecture d'un folio par calcul : `outils/controles/folio.py <xrs> <folio affiché>` (dans le dépôt depuis la v43). Comparer une release réenregistrée : `outils/controles/retouche.py` + comparer à part les blocs ¤#DefCable (positions des textes de câble). Centrage des numéros : `outils/controles/centrage.py`.

## Méthode qui marche (à suivre à chaque version)
1. Lire la demande, noter les retours bruts dans `memoire/revues/AAAA-MM-JJ_retours_julien_vNN.md` (tableau folio / demande), **poser au plus 4 questions numérotées**, commit + push, attendre le GO.
2. Modifier **seulement `outils/ttk_schema.py`** (et `xrs_gen.py` si besoin). Folios : le script parle en **numéros internes** (table dans 04 : ex. affiché f61 = interne "50", f60 = "55", f31 = "20", f20 = "32", plans f70-f73 = "71"-"74").
3. Après chaque modification : `sh outils/controles/tout.sh <scratchpad>/essai.xrs JJ/MM/AAAA`. Tout doit être à 0 (verifier : 28 attentions connues). Ne jamais sortir une version sinon.
4. Release : `git status schema/` d'abord. Si la release a changé (WinRelais l'a réenregistrée) : la copier dans `schema/recus/AAAA-MM-JJ_vNN_ouverte_WinRelais.xrs`, comparer (symboles, fils, textes, numéros via `xrs_tool.parse`) et reprendre ses retouches ; puis `git mv` des 3 fichiers vers `old/`, générer la nouvelle avec les commandes du README (verifier, nomenclature).
5. Rapport `docs/RAPPORT_vNN_AAAA-MM-JJ.md`, mémoire (04 règles, 06 version, revues, README, DECISIONS, JOURNAL), CLAUDE.md (n° de version), commit `[PERSO JULIEN] …` + `git pull --rebase` + push.

## Pièges connus
- **Lisibilité** : WinRelais dessine autour d'un câble blindé une ellipse (±350) et un cadre arrondi autour du repère ; les cadres pointillés ont des bords. `zones_cables()` du script et `xrs_chevauchements.py` en tiennent compte. Règle d'espacement : voir 04 « Lisibilité (v38) ». Si le contrôle n'est pas à 0, **aérer** (déplacer bornes / câble / boîte), ne pas réduire les marges.
- Numéros de fil : taille `NUM_T = 200` (xrs_gen.py).
- Depuis la v42, le contrôle voit aussi les corps des symboles, les noms de broches, les textes dessinés (BK, GN…) et les points de connexion. Il ne voit pas le rendu réel de WinRelais (gras, taille exacte) : Julien relit.
- Fichiers : `ttk_schema.py` en LF, `xrs_gen.py` en CRLF : faire les remplacements avec un petit script Python (lire, `assert t.count(a) == 1`, remplacer, réécrire en gardant les fins de ligne). Écrire les gros scripts dans un fichier (pas de heredoc avec beaucoup de guillemets).
- Symboles CUSTOM : 3 copies : `outils/librairie/CUSTOM` (parfois un autre format : bloc brut UTF-8), `librairie_winrelais/sym_electrotech/CUSTOM` et `C:\Users\Public\Documents\Elec-CAO\sym_electrotech\CUSTOM` (cp1252, CRLF ; ces 2 dernières identiques octet pour octet, c'est celle du PC que lit le script). Contrôle : `outils/controles/symboles.py` (dans `tout.sh`). Nouveau symbole (v42, `Thermocouple_bas.xsy`) : l'écrire dans les 3 dossiers ; modification par script (`outils/librairie/scripts/tc_bas.py`, `mcx_large.py`, déjà appliqués : positions relatives à la broche d'origine, chaque copie dans son encodage), puis diff.
- **Retoucher un symbole** (erreur de la v40 : épaisseur 200 au lieu de 20) : remplacer la ligne de contour entière (10 champs : x1, y1, x2, y2, épaisseur, style 0 plein / 1 pointillé, 0, 0, 0, vide), jamais couper des octets (« · » fait 1 octet en cp1252, 2 en UTF-8) ; vérifier ensuite le diff du .xrs généré.
- Bornes : renommer un folio renomme ses bornes (règle X + folio) : mettre aussi à jour `implantation/generateur/saisie.json` (sinon la nomenclature signale des bornes absentes).
- `implantation/` : ne pas régénérer le dossier sans accord ; `extraire.py` écrit `donnees.json` (le remettre avec `git checkout` après un essai).
- D'autres sessions peuvent pousser (SEW, docs) : toujours `git pull --rebase` avant de commencer et avant de pousser. Préfixe de commit unique `[PERSO JULIEN]` (25/11).

## Outils de contrôle (dans le dépôt depuis le 24/11, avant dans le scratchpad)
`outils/controles/` : `folio.py`, `retouche.py`, `centrage.py` (aides, v43) ; `tout.sh` (génère + tout contrôle ; v42 : le contrôle élargi voit aussi corps des symboles, noms de broches et points de connexion), `symboles.py` (copies CUSTOM, format des contours, v41), `cadres.py` (cadres pointillés), `textes.py` (folios hors 10-69), `d11.py` (24 V / 0 V des drivers et E/S), `bornes.py` (doublons, règle X + folio, saisie.json), `bbox.py` (géométrie d'un symbole de la librairie).
