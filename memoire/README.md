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
| [08_IMPLANTATION.md](08_IMPLANTATION.md) | Dossier d'implantation généré (PDF de 2 pages depuis la v12) : demande, générateur, saisie.json, points ouverts |
| [09_STOCK.md](09_STOCK.md) | Stock de câbles et de bornes (source unique, « on ne commande plus rien ») |
| [revues/](revues/) | Revues extérieures du schéma : notes brutes recopiées telles quelles (`AAAA-MM-JJ_auteur_vN_notes_brutes.txt`) + demandes rédigées et suivies (`…_demandes.md`). Revue Krizox v36 (faite en v37) : [demandes](revues/2026-11-20_krizox_v36_demandes.md) ; [retours de Julien sur la v37](revues/2026-11-23_retours_julien_v37.md) (faits en v38) ; [retours v38](revues/2026-11-24_retours_julien_v38.md) (faits en v39) |

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

Dernière mise à jour : 24/11/2026 (v39 : colonnes f41/f42, symbole entrées CPU élargi, f70 supprimé, plans de bornier) ; 24/11/2026 (v38 : lisibilité, numéros en 200, f60 coupé en deux) ; 24/11/2026 (valeurs orales SEW : frein 0,18 A, STO 150 mW, à confirmer par écrit) ; 24/11/2026 (retours v37 notés, questions avant v38) ; 23/11/2026 (v37 : revue Krizox réalisée, boîte +BJM, f43, plans de bornier) ; 23/11/2026 (revue Krizox v36 : dossier revues/) ; 23/11/2026 (PC PERSO JULIEN, 3e clone dans 07) ; 20/11/2026 (implantation v13) ; 20/11/2026 (stock de fil, couleurs 24 V, passe de vérification) ; 20/11/2026 (v35 : QF10 en 2 A, sections proposées) ; 18/11/2026 (implantation v12, 2 pages) ; 18/11/2026 (v34 : corrections de la revue v33) ; 18/11/2026 (revue v33 : `docs/REVUE_SCHEMA_v33_2026-11-18.md`) ; 18/11/2026 (v33 : retours v32, f80 généré, nomenclature sur 3 folios) ; 18/11/2026 (v32 : nomenclature générée, fins de course NF, types de bornes, images relatives) ; 18/11/2026 (reprise sur le PC PRO RIMANE, 2 clones dans 07) ; 17/11/2026 (09_STOCK.md créé, méthode câbles / bornes proposée) ; 17/11/2026 (08_IMPLANTATION.md créé) ; 17/11/2026 (dossier d'implantation v11 généré, décisions câbles) ; 16/11/2026 (v31 : 2L+ / 2M, tableau f80) ; 16/11/2026 (v30 : numérotation de tous les folios) ; 16/11/2026 (v29 : revue complète, f70 agrandi) ; 16/11/2026 (v28 : X21.14 capteurs, H1 / H4 au f62, réserves, revue des folios) ; 13/11/2026 (v27 : PN1-PN4, bornes X13, numérotation f20-f30) ; 13/11/2026 (v26 : numérotation f11-f13, contrôle des fils) ; 13/11/2026 (v25 : numérotation f10, XR1 / XR2 sur R2) ; 09/11/2026 (v24 : f70 rail par rail) ; 06/11/2026 (v23 : STO en chaîne, f70) ; 05/11/2026 (v22 : bornes de porte au f70, f62 validé) ; 05/11/2026 (v21 : fils Profinet) ; 05/11/2026 (v20 : PTFIX 6/12X2,5 au f21, type des câbles) ; 05/11/2026 (v19 : W11 / W12 au f70) ; 05/11/2026 (v18 : frein unique -W4, terre du bâti -W13) ; 05/11/2026 (v17 : S3 AUTO-A à MANU-D, bornes de porte et de la colonne) ; 05/11/2026 (agent d'implantation : câble frein unique, XR1 / XR2, bornier R5 par câble) ; 04/11/2026 (v16) ; avant : 03/11/2026 (clôture des achats, v15 inchangée).
