# Mémoire du projet TTK (schéma électrique)

Point d'entrée unique pour reprendre le projet sans relire tout l'historique.
À lire dans l'ordre, puis `docs/DECISIONS.md` pour le détail daté.

| Fichier | Contenu |
|---|---|
| [01_PROJET.md](01_PROJET.md) | Machine, client, personnes, postes, planning |
| [02_MATERIEL.md](02_MATERIEL.md) | Matériel retenu, repère par repère, avec sa source |
| [03_ARCHITECTURE.md](03_ARCHITECTURE.md) | Puissance, 24 V, 48 V, sécurité, automate, PROFINET |
| [04_REGLES_DESSIN.md](04_REGLES_DESSIN.md) | Règles de Julien pour le dessin (à respecter sur tous les folios) |
| [05_POINTS_OUVERTS.md](05_POINTS_OUVERTS.md) | Questions en suspens et valeurs à vérifier |
| [06_EN_COURS.md](06_EN_COURS.md) | Version actuelle, ce qui a changé, travail en cours |
| [07_METHODE_TRAVAIL.md](07_METHODE_TRAVAIL.md) | Dépôt, génération, contrôle, commit, façon de répondre à Julien |

## Statuts utilisés
- **[D]** décision de Julien
- **[C]** confirmé (document, fournisseur, essai)
- **[H]** hypothèse ou proposition de l'assistant, non validée
- **[?]** ouvert

## Règle de mise à jour
- Une information nouvelle va dans le fichier de son thème, avec sa date et son statut.
- Une information qui change remplace l'ancienne (pas de doublon). L'historique reste dans `docs/DECISIONS.md` et `docs/JOURNAL_ECHANGES.md`.
- Les points « à vérifier » vont dans `05_POINTS_OUVERTS.md`, **jamais sur le schéma** (plus de notes encadrées, demande du 29/10).

`CLAUDE.md` (racine du dépôt) renvoie ici : un nouveau chat Claude Code le lit au démarrage.

Dernière mise à jour : 02/11/2026 nuit (v15).
