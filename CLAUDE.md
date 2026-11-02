# TTK-SCHEMA-ELEC : consignes pour l'assistant

Ce fichier est lu automatiquement au démarrage d'une session Claude Code dans ce dépôt.

1. **Avant de répondre à Julien, lire `memoire/` en entier** (README puis 01 à 07). Tout le contexte du projet y est : machine, matériel, architecture, règles de dessin, points ouverts, travail en cours, méthode.
2. Le schéma est **généré** par `outils/ttk_schema.py`. Ne jamais modifier un .xrs à la main ; ne jamais toucher `schema/modele/SCHEMA_ELEC_TTK.xrs`.
   Versions : la dernière est seule dans `schema/generes/release/`, les autres dans `schema/generes/old/`.
   Piège : depuis la v8, les numéros de folio **affichés** (ceux de Julien) diffèrent des numéros **internes** du script (`NUMFOL`, table dans `memoire/04_REGLES_DESSIN.md`). Julien parle en numéros affichés ; le script s'écrit en anciens numéros.
3. Règles absolues de Julien : pas de notes encadrées sur les folios ; pas d'aperçu HTML / SVG / image (contrôle par calcul) ; aucune valeur inventée (« à vérifier ») ; français, phrases courtes, au plus 3-4 questions numérotées.
4. À chaque échange : mettre à jour `memoire/` (fichier du thème), `docs/DECISIONS.md` et `docs/JOURNAL_ECHANGES.md`, puis commit + push sur `main`.
5. Si le système de mémoire peut être amélioré (info manquante, mal rangée, en double), **le dire à Julien et le faire** (demande du 29/10).
