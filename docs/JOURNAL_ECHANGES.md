# Journal des échanges

Une entrée par échange : date, sujet, décisions [D], points ouverts [?], remises en question.

## 26/10/2026
- Démarrage : base de connaissances transmise. Priorité : sécurité (f40-42) puis automate (f50-54). J1 = 05/11.
- Dépôt GitHub créé comme référentiel (structure, outil `xrs_check.py`, `DECISIONS.md`).
- [D] Câble frein 2G1,5 + câble TF 2G1 blindé, séparés. [D] Un repère par câble (-W201/202/203 ; -W211/212/213).
- Remise en question : prévoir la commande des 2 nouveaux câbles (hors commande actuelle) ; frein 400 V CA donc isolation adaptée.
- En attente : `.xrs` récent (envoi dans le chat) ; réponses sur repères cibles (maintenant/fin) et Q12/Q13.

## 27/10/2026
- Reçus et archivés dans `docs/local/` : METHODE_BORNIERS, FORMAT_XRS, base Claude Code du 22/10, 2 rapports de vérification.
- État de `test_xrs_claude.xrs` (22-23/10) : généré par script (27 folios, 131 symboles, 597 fils, 104 renvois), 0 erreur. Folios 70/71/80/85/90 créés mais vides, sauf tableaux de contrôle f70/f71.
- Incohérences relevées entre ces fichiers et la décision du 26/10 ou la base de session :
  1. Câbles SEW : `W202/W212 = 4 x 1 mm² blindé frein + TF` et bornes X701.17-.24 groupées par câble frein+TF. Décision [D] du 26/10 : frein 2G1,5 (W202/W212) + TF 2G1 blindé (W203/W213). À refaire dans le script et le plan de bornes.
  2. AU : plan de bornes X711 = S412 info → I0.1. Liste d'E/S gelée du 06/10 = AU pupitre S412 → I0.0, AU armoire S411 → I0.1.
  3. Fins de course : plan X701 = B501…B504 → I1.0…I1.3. Liste d'E/S du 06/10 = I0.6, I0.7, I1.0, I1.1 ; I1.2/I1.3 = retours KM1/KM2. `PROPOSITION_ES_AUTOMATE.csv` non validé : conflit à trancher.
  4. Sorties du relais K401 : plan X711 fait passer 33-34 par un contact S413 vers 3L+ des sorties CPU/SM (alimentation des sorties automate coupée par la sécurité). Architecture figée du 30/09 : 33-34 → bobines Q421, Q422, Q423 ; 13-14 → STO ; 23-24 → KM1/KM2. Les f40-f42 du fichier étaient « en attente des explications de Julien » : donc provisoires.
  5. S413 : le plan utilise 5 paires de contacts (13-14 … 53-54) ; l'Eaton T0-4-8223/E a 4 pôles. Confirme le point ouvert du 26/10.
  6. Préfixe librairie de S414 = H alors que le repère est S ; LC1D09BD avec 5 préfixes (KM, Q) : voulu (exception R8), mais à ne pas laisser comme « attention » au contrôle.
  7. Source de vérité : `test_xrs_claude.xrs` est régénéré par `ttk_schema.py`. Toute modification faite à la main dans WinRelais est écrasée à la régénération. À trancher : script ou fichier WinRelais, lequel fait foi ?
- Remise en question : BASE du 22/10 décrit Julien comme « dessinateur » (faux, corrigé) et conseille de ne pas toucher au fichier de travail : cohérent avec la base de session.

## 27/10/2026 (suite) : deux .xrs reçus
- Archivés : `schema/recus/2026-10-27_SCHEMA_ELEC_TTK_main.xrs` (à la main) et `2026-10-27_test_xrs_claude_script.xrs` (généré par script).
- Fichier à la main : 22 folios, 52 symboles, compteur 18120. Quasi identique à l'état du 22/10 (anomalies inchangées sauf T7 recalé sur la grille et le fil PUL+ de T7 repris). Reste : repères anciens, F1:N, G1:L, G2:L, T5:H1-H3 à 1 mm, M3/K4/K5 hors grille, K2/K3 et K4/K5 en double, noms internes de folios en double, descriptions f31 et f40 fausses, synoptique avec image à chemin absolu.
- Fichier script : 27 folios, 131 symboles, 0 hors grille, 0 erreur ≤ 2 mm, repères cibles, f31 à f60 remplis, f70/f71 présents. Plus de logo (le synoptique f04 n'a plus d'image).
- 22 « attente? » à 4 mm (f12, f13, f41, f42) : faux positifs de l'outil (extrémité libre du même fil que la broche). À corriger dans `xrs_check.py`.
- Point ouvert : lequel fait foi ? Voir réponse de Julien.

## 27/10/2026 (suite) : outils Python reçus
- Archivés dans `outils/` : `xrs_tool.py` (lecture, `verifier`), `xrs_edit.py` (édition sûre), `xrs_gen.py` (générateur). Manque encore `ttk_schema.py` (description du schéma) et `corrections_*.py`.
- `xrs_tool.py verifier` donne : fichier à la main 8 erreurs / 62 attentions ; fichier script 0 erreur / 27 attentions (identique au rapport du 22-23/10). Il traite déjà le faux positif « extrémité libre à 4 mm de sa propre broche » : `xrs_check.py` (annexe A) est donc redondant, on utilise `xrs_tool.py`.
- Constat : références croisées toujours à -1 dans le fichier script (pas de lien bobine ↔ contacts). Dates codées en dur « 22/10/2026 » dans `xrs_gen.py` (cartouche, auteur des symboles).
