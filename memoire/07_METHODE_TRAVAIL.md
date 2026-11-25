# 07 · Méthode de travail

## Source de vérité
- **Dépôt** https://github.com/JulienBEBL/TTK-SCHEMA-ELEC, branche `main`. Trois clones (18/11, 23/11). **Préfixe de commit unique `[PERSO JULIEN]` pour les deux dépôts (schéma et automatisme), décidé le 25/11** ; les anciens préfixes [PRO JULIEN], [PRO RIMANE], [perso] restent dans l'historique git :
  | PC | Ancien préfixe (avant le 25/11) | Clone |
  |---|---|---|
  | PC de Julien (BEBL-15-LAFITE) | [PRO JULIEN] | `C:\Users\Julien\Documents\10. TTK\Repo_git\TTK-SCHEMA-ELEC` |
  | PC Rimane (DESKTOP-G68K9P5) | [PRO RIMANE] | `C:\Users\Rimane\Documents\10. TTK\TTK-SCHEMA-ELEC` |
  | PC perso de Julien (DESKTOP-JEQGUKQ), depuis le 23/11 pour environ 3 mois (programme automate) | [PERSO JULIEN] | `C:\Users\Julien\Documents\10. TTK\TTK-SCHEMA-ELEC` |
  - PC perso (23/11) : identité git `--local` JulienBEBL / julien@bebl.fr ; Python 3.15.2 ; WinRelais installé (`C:\Users\Public\Documents\Elec-CAO\sym_electrotech`) TIA Portal installé ; dossiers Documents et Téléchargements recopiés du PC Rimane (Julien 23/11 : `Sourcing Composant (3).xlsx`, `Demande_de_Commande_Hugo_*.xlsx` présents). **Symboles CUSTOM installés le 23/11** (54, copie identique à `librairie_winrelais/` ; 56 depuis la v38 : CPU coupée en alim_profinet / entrees, installés le 24/11 ; entrees refait au pas de 1600 en v39). Avec la vraie librairie, la v36 se régénère **octet pour octet** : 0 problème, 0 erreur / 30 attentions, 0 chevauchement. Dossier voisin : `Documents\10. TTK\TTK-AUTOMATISME` (programme).
  - Identité git du PC Rimane : `--local` (ce dépôt seul), JulienBEBL / julien@bebl.fr, comme sur le PC de Julien (18/11).
  - Toujours `git pull --rebase` avant de travailler : l'autre PC a pu pousser.
  - Ce qui dépend du PC : chemins des images dans les .xrs (`¤#Logo¤`, chemin absolu), zoom écrit par WinRelais (virgule décimale sur le PC Rimane), Python (installé sur le PC Rimane le 18/11 : 3.15.2), symboles CUSTOM installés ou non. Détail : `docs/ANALYSE_PC_RIMANE_2026-11-18.md`.
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
| `schema/generes/release/` | **la dernière version seule** : `TTK_AAAA-MM-JJ_vN.xrs` + `_verification.md` + `_nomenclature.csv` |
| `implantation/` | Dossier d'implantation **généré** depuis le 17/11 (`implantation/generateur/`, PDF dans release/). Jusqu'à la v10 : agent draw.io. Commits préfixés `[PERSO JULIEN]` (25/11) ; pas de push sans accord de Julien |
| `cablage/` | Vérité terrain des câbles sortants et des bornes (`TTK_CABLES.xlsx`, CSV exportés), indépendante du schéma (17/11) |
| `schema/generes/old/` | toutes les versions précédentes (on y déplace l'ancienne release avec `git mv` à chaque nouvelle version) |
| attention | **Julien ouvre la release directement dans WinRelais, qui la réenregistre.** Avant le `git mv`, faire `git status` : si la release est modifiée, la copier dans `schema/recus/AAAA-MM-JJ_vN_ouverte_WinRelais.xrs`, la comparer à la version générée (section par section), puis `git checkout` la version générée (constaté le 02/11 sur la v12). |
| `schema/recus/` | .xrs renvoyés par Julien, datés |
| `livrables/` | Classeur Excel de Julien (non modifié par script), CSV, macros |

## Boucle d'une version
1. Discuter les points avec Julien, par blocs. **Ne générer que quand il le demande.**
2. Modifier `outils/ttk_schema.py` (renommer un appareil : seulement le dict `RENOMME`).
3. Générer et contrôler (PC de Julien, librairie WinRelais réelle) :
   ```
   cd outils
   set TTK_LIB=C:\Users\Public\Documents\Elec-CAO\sym_electrotech
   set TTK_DATE=JJ/MM/AAAA
   python ttk_schema.py ..\schema\generes\release\TTK_AAAA-MM-JJ_vN.xrs
   python xrs_tool.py verifier ..\schema\generes\release\TTK_AAAA-MM-JJ_vN.xrs
   python xrs_chevauchements.py ..\schema\generes\release\TTK_AAAA-MM-JJ_vN.xrs
   ```
   Contrôle complet en une commande (essai) : `sh outils/controles/tout.sh <essai.xrs> JJ/MM/AAAA` (numéros, cadres, textes, 24 V / 0 V, bornes, symboles CUSTOM).
   Attendu : « 0 problème(s) de contrôle », 0 erreur au verifier, « total 0 » aux chevauchements. Les 28 « attention » connues de la v9 sont normales (fils en attente de l'arrivée réseau et de la variante USA, début de barre au f25, références croisées à lancer dans WinRelais, 0 V / PE liés par X36.1).
4. Mettre à jour `docs/DECISIONS.md`, `docs/JOURNAL_ECHANGES.md` et `memoire/`.
5. Commit + push (message en français, fin : `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`).
6. Julien ouvre le .xrs, lit le Journal, lance « Références croisées automatique », renvoie ses retours.

## Structure de `ttk_schema.py` (à connaître avant de modifier)
- **Numéros de folio** : anciens numéros en interne (`F["13"]`, textes « (f13) ») ; `NUMFOL` donne le numéro affiché, `ren()` traduit les « fNN » des textes et les repères (`RENOMME`). Un texte qui contient déjà un nouveau numéro (relu dans le fichier, ex. tableaux de bornier f71) passe par `ren_rep()` seulement.
- **Terre** : chaque fil PE court d'appareil est ajouté à `PE_DEST` ; les départs PE du f20 et leurs renvois sont tracés à la fin, triés par folio.
- **Barres 24 V / 0 V** : tracées à la fin (liste `CH`, triée par numéro affiché) ; les folios 40, 41, 42, 50 (anciens numéros) sont d'abord descendus par `g.decaler` pour laisser la place, puis leurs liaisons aux barres sont tracées. Tout renvoi vers ces folios doit être posé **avant** le décalage.
- **Nomenclature** (18/11) : `outils/nomenclature.py`, appelé après `renommer_symboles()` ; contrôle relu sur le fichier à la fin.
- **Centrage** : `HAUT` liste les folios centrés en largeur seulement (bus, barres et variateurs à hauteur fixe).
- **Noms de broches** : `noms=True / False` à la pose d'un symbole.
- **Numéros de fil** : `nommer_phases()` (tronçon = fils reliés bout à bout sur le folio ; alignement des voisins ; nom des bus à gauche).

## Contrôles : pas de rendu
- **Pas d'aperçu HTML / SVG / image des schémas.** On contrôle par calcul : équipotentielles (`xrs_tool.build_nets`), géométrie (`geometry_issues`), verifier, et `outils/xrs_chevauchements.py` (30/10) : numéros de fil et de brin, textes de câble, champs, renvois, fils. Il retrouve les 5 chevauchements du f20 de la v8.

## Pièges du format .xrs (détail : `docs/local/FORMAT_XRS.md`)
- UTF-8 avec BOM, CRLF, séparateur « · », sections « ¤#Nom¤ ». En Python : lire avec `newline=""` ; écrire les scripts dans des fichiers (les heredocs bash abîment ¤ et ·).
- Unités 1/100 mm, grille 400, Y vers le bas. Un fil n'est raccordé que si son extrémité tombe **exactement** sur la broche ; les bornes court-circuitent leurs broches.
- Renvois (champs 9-10) : 0 = fil en dessous (flèche au-dessus), 1 = fil au-dessus. Horizontal, flèche toujours vers la droite : côté A (départ) 2 = fil à gauche, 3 = fil à droite ; côté B (arrivée) 2 = fil à droite, 3 = fil à gauche. Le point de renvoi est au bout d'un fil droit ; renvois voisins espacés d'au moins 4,4 mm.
- Numéros de fil (section `¤#Numero¤`) : `x·y·texte·indexFolio·0·Arial·300·angle·8388608·0·0·0·`, au milieu du segment, angle 90 en vertical.
- Câble (`DefCable`, `BrinCable`) : le numéro de brin s'écrit juste au-dessus du croisement ; un numéro de fil placé là devient illisible.
- Au réenregistrement, WinRelais réordonne des segments et change des drapeaux internes : ce n'est pas une modification de contenu.

## Répondre à Julien
- Français, phrases courtes, concret. « Trop de texte » est un défaut.
- Aucune valeur inventée : citer la source ou écrire « à vérifier ».
- Signaler les incohérences (entre ses messages, ou avec l'historique).
- Au plus 3-4 questions numérotées, groupées dans un message.
- Contester un choix une fois (raison + alternative), puis respecter sa décision.
- Faire avec le matériel commandé. Travailler par blocs validés.

## WinRelais réenregistre la release (rappel 06/11 et 09/11)
- Julien ouvre la release : WinRelais la réenregistre (fichier modifié dans git). Toujours : copier dans `schema/recus/AAAA-MM-JJ_vN_ouverte_WinRelais.xrs`, comparer textes / symboles / fils à la version générée (`git show HEAD:...`), reprendre les retouches éventuelles, puis `git checkout` du fichier généré, **avant** tout `git mv` vers old/.
- Le 06/11, une 2e réécriture de la v22 a été écrasée sans comparaison (seule la 1re copie est archivée) : faire la copie juste avant le `git mv`, même si une copie existe déjà.
