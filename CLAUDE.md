# TTK-SCHEMA-ELEC : consignes pour l'assistant

Ce fichier est lu automatiquement au démarrage d'une session Claude Code dans ce dépôt.

1. **Avant de répondre à Julien, lire `memoire/` en entier** (README, puis **10_REPRISE_AUTRE_MODELE.md** (méthode et pièges), puis 01 à 09). Tout le contexte du projet y est : machine, matériel, architecture, règles de dessin, points ouverts, travail en cours, méthode. Version actuelle : `memoire/06_EN_COURS.md` (v40 du 25/11/2026 à la dernière mise à jour de ce fichier).
2. Le schéma est **généré** par `outils/ttk_schema.py`. Ne jamais modifier un .xrs à la main ; ne jamais toucher `schema/modele/SCHEMA_ELEC_TTK.xrs`.
   - Versions : la dernière est seule dans `schema/generes/release/`, les autres dans `schema/generes/old/`. Commandes de génération et de contrôle : `README.md`. Contrôle complet en une commande : `sh outils/controles/tout.sh <essai.xrs> JJ/MM/AAAA`. Attendu : 0 problème, 0 erreur au verifier, 0 chevauchement (contrôle élargi v38 : ellipses et repères de câble, bords des cadres pointillés).
   - Piège : les numéros de folio **affichés** (ceux de Julien) diffèrent des numéros **internes** du script (`NUMFOL`, table dans `memoire/04_REGLES_DESSIN.md`). Julien parle en numéros affichés ; le script s'écrit en anciens numéros.
   - Julien ouvre la release dans WinRelais, qui la réenregistre. Avant tout `git mv` vers old/ : `git status` ; si elle a changé, l'archiver dans `schema/recus/…_ouverte_WinRelais.xrs`, la comparer à la version générée et reprendre ses retouches dans le script (`POS_JULIEN`…), puis `git checkout` du fichier généré.
   - Pour chaque modification, regarder le .xrs actuel pour vérifier ou comparer (demande du 02/11).
3. Règles absolues de Julien : pas de notes encadrées sur les folios ; pas d'aperçu HTML / SVG / image (contrôle par calcul) ; aucune valeur inventée (« à vérifier ») ; français, phrases courtes, au plus 3-4 questions numérotées. Contester un choix une fois, puis suivre sa décision. Travailler avec le matériel déjà commandé.
4. À chaque échange, **même une simple question** (règle de Julien, 25/11 : toujours consigner nos discussions) : mettre à jour `memoire/` (fichier du thème), `docs/DECISIONS.md` et `docs/JOURNAL_ECHANGES.md`, puis commit + push sur `main` (`git pull --rebase` avant, jamais de `--force`).
5. Si le système de mémoire peut être amélioré (info manquante, mal rangée, en double), **le dire à Julien et le faire** (demande du 29/10).
6. `implantation/` : dossier généré depuis le 17/11 (`implantation/generateur/`, voir son README). Préfixe de commit unique `[PERSO JULIEN]` (décision du 25/11, les deux dépôts) ; `git pull` avant d'éditer ; pas de push sans accord de Julien.
7. Toujours utiliser des chemins absolus vers ce dépôt : le répertoire de travail revient parfois à l'ancien dossier `Documents\10. TTK\Schema Elec`, qui est **dépassé**. Trois clones (détail : `memoire/07_METHODE_TRAVAIL.md`) ; poste de travail actuel : PC perso ; préfixe de commit `[PERSO JULIEN]` quel que soit le PC (25/11) :
   - PC pro de Julien : `C:\Users\Julien\Documents\10. TTK\Repo_git\TTK-SCHEMA-ELEC`
   - PC Rimane : `C:\Users\Rimane\Documents\10. TTK\TTK-SCHEMA-ELEC` (identité git `--local` : JulienBEBL / julien@bebl.fr)
   - PC perso de Julien (DESKTOP-JEQGUKQ), depuis le 23/11/2026 pour environ 3 mois (programme automate) : `C:\Users\Julien\Documents\10. TTK\TTK-SCHEMA-ELEC` (même identité git `--local`). Même début de chemin que l'ancien dossier `Schema Elec`, mais c'est bien le dépôt.
