# 07 · Méthode de travail

## Source de vérité
- **Dépôt** https://github.com/JulienBEBL/TTK-SCHEMA-ELEC, branche `main`. Clone local : `C:\Users\Julien\Documents\10. TTK\Repo_git\TTK-SCHEMA-ELEC`.
- Le schéma est **généré** par `outils/ttk_schema.py` (+ `outils/xrs_gen.py`). Toute retouche faite à la main dans WinRelais est écrasée à la régénération : elle doit être décrite à l'assistant.
- L'ancien dossier `Documents\10. TTK\Schema Elec` n'est plus utilisé (29/10).
- `schema/modele/SCHEMA_ELEC_TTK.xrs` : modèle (en-tête, cartouche). **Ne jamais le modifier.**
- Ne jamais modifier un .xrs de travail directement ; en local, seulement des copies, WinRelais fermé.

## Arborescence
| Dossier | Contenu |
|---|---|
| `memoire/` | Ce dossier : synthèse à jour par thème |
| `docs/DECISIONS.md` | Décisions datées [D] [C] [H] [?] |
| `docs/JOURNAL_ECHANGES.md` | Un paragraphe par échange |
| `docs/` (autres) | Nommage, sécurité, passation, format .xrs (`docs/local/`) |
| `outils/` | Scripts Python, librairie de symboles reconstruite |
| `schema/generes/` | `TTK_AAAA-MM-JJ_vN.xrs` + `_verification.md` + `_nomenclature.csv` |
| `schema/recus/` | .xrs renvoyés par Julien, datés |
| `livrables/` | Classeur Excel de Julien (non modifié par script), CSV, macros |

## Boucle d'une version
1. Discuter les points avec Julien, par blocs. **Ne générer que quand il le demande.**
2. Modifier `outils/ttk_schema.py` (renommer un appareil : seulement le dict `RENOMME` ; états des folios : `STATUT`).
3. Générer et contrôler (PC de Julien, librairie WinRelais réelle) :
   ```
   cd outils
   set TTK_LIB=C:\Users\Public\Documents\Elec-CAO\sym_electrotech
   set TTK_DATE=JJ/MM/AAAA
   python ttk_schema.py ..\schema\generes\TTK_AAAA-MM-JJ_vN.xrs
   python xrs_tool.py verifier ..\schema\generes\TTK_AAAA-MM-JJ_vN.xrs
   ```
   Attendu : « 0 problème(s) de contrôle » et 0 erreur au verifier. Les 27 « attention » connues sont normales (références croisées à lancer dans WinRelais, 0 V / PE liés par X36.1).
4. Mettre à jour `docs/DECISIONS.md`, `docs/JOURNAL_ECHANGES.md` et `memoire/`.
5. Commit + push (message en français, fin : `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`).
6. Julien ouvre le .xrs, lit le Journal, lance « Références croisées automatique », renvoie ses retours.

## Contrôles : pas de rendu
- **Pas d'aperçu HTML / SVG / image des schémas.** On contrôle par calcul : équipotentielles (`xrs_tool.build_nets`), géométrie (`geometry_issues`), verifier.

## Pièges du format .xrs (détail : `docs/local/FORMAT_XRS.md`)
- UTF-8 avec BOM, CRLF, séparateur « · », sections « ¤#Nom¤ ». En Python : lire avec `newline=""` ; écrire les scripts dans des fichiers (les heredocs bash abîment ¤ et ·).
- Unités 1/100 mm, grille 400, Y vers le bas. Un fil n'est raccordé que si son extrémité tombe **exactement** sur la broche ; les bornes court-circuitent leurs broches.
- Renvois (champs 9-10) : 0 = fil en dessous (flèche au-dessus), 1 = fil au-dessus. Horizontal, flèche toujours vers la droite : côté A (départ) 2 = fil à gauche, 3 = fil à droite ; côté B (arrivée) 2 = fil à droite, 3 = fil à gauche. Le point de renvoi est au bout d'un fil droit ; renvois voisins espacés d'au moins 4,4 mm.
- Numéros de fil (section `¤#Numero¤`) : `x·y·texte·indexFolio·0·Arial·300·angle·8388608·0·0·0·`, au milieu du segment, angle 90 en vertical.
- Au réenregistrement, WinRelais réordonne des segments et change des drapeaux internes : ce n'est pas une modification de contenu.

## Répondre à Julien
- Français, phrases courtes, concret. « Trop de texte » est un défaut.
- Aucune valeur inventée : citer la source ou écrire « à vérifier ».
- Signaler les incohérences (entre ses messages, ou avec l'historique).
- Au plus 3-4 questions numérotées, groupées dans un message.
- Contester un choix une fois (raison + alternative), puis respecter sa décision.
- Faire avec le matériel commandé. Travailler par blocs validés.
