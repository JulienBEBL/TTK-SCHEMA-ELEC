# WinRelais `.xrs` et schéma électrique TTK : base de connaissances

> Document autonome destiné à un assistant IA qui aidera Julien à construire le schéma électrique
> de la machine TTK sous WinRelais, plus vite et avec moins d'erreurs.
> Rédigé le 22/10/2026 à partir de l'analyse du fichier `SCHEMA_ELEC_TTK.xrs` (WinRelais 2.6b Expert),
> de 36 schémas d'exemple fournis avec le logiciel et de l'aide officielle (fichiers .chm).
> **Le schéma est EN COURS DE CONSTRUCTION** : les folios incomplets et les fils en attente sont normaux.

---

## 0. Consignes pour l'assistant

1. Répondre en **français**. Julien est dessinateur électricien au bureau d'études ; il connaît WinRelais.
2. Le format `.xrs` **n'est pas documenté par l'éditeur**. Tout ce qui suit vient de rétro-ingénierie.
   Les champs marqués **?** sont des hypothèses : ne pas les présenter comme certains.
3. Ne **jamais** proposer de modifier le fichier de travail directement : travailler sur une **copie**
   (ex. `test_xrs_claude.xrs`), WinRelais **fermé**, puis rouvrir dans WinRelais et lire le Journal.
4. Respecter l'encodage : **UTF-8 avec BOM**, fins de ligne **CRLF**, séparateur `·` **et `·` final**
   sur chaque ligne de données. Un octet de travers = fichier illisible ou objets perdus.
5. Ne pas confondre une **erreur** (fil arrêté à 1 mm d'une broche, repère en double) avec un
   **travail en cours** (fil en attente vers un folio pas encore dessiné). En cas de doute, demander.
6. Les remarques de conception électrique (protection, sections, sécurité machine) se formulent comme
   des **questions ou points à vérifier**, pas comme des affirmations : l'assistant ne connaît pas tout
   le cahier des charges.

---

## PARTIE A : le format de fichier `.xrs`

### A.1 Généralités

| Élément | Valeur |
|---|---|
| Logiciel | WinRelais (Elec-CAO, éditeur Ingerea / Pascal Eynard). Version de Julien : **2.6b Expert** |
| Extensions | `.xrs` = schéma, `.xrm` = modèle de schéma (**même format**), `.xsy` = symbole (format différent), `.xrb` = bloc |
| Nature | Fichier texte, une information par ligne, organisé en sections |
| Encodage | v2.6 : **UTF-8 avec BOM**. Versions ≤ 2.5 : **Windows-1252** sans BOM (mêmes séparateurs) |
| Fins de ligne | CRLF |
| Séparateur de champs | `·` (U+00B7, point médian). Chaque ligne de données **finit par `·`** |
| En-tête de section | `¤#Nom¤` ou `¤#Nom·n¤` (`¤` = U+00A4). Ex. `¤#Folio·3¤`, `¤#Symbole·12¤` |
| Fin de bloc | `¤#FIN¤` (blocs Folio, Symbole, DefCable, Bornier, et fin de fichier) |
| Unité | **1/100 mm** (10000 = 10 cm). Origine = coin **haut-gauche** du folio, **Y vers le bas** |
| Grille | 4 mm = **400**. Broches et fils sur un pas de 400 (parfois 200) |
| Couleurs | entier COLORREF Windows `R + 256·G + 65536·B` (0 noir, 255 rouge, -1 = couleur par défaut) |
| Index de folio | Les objets globaux (fils, jonctions, textes, câbles, symboles) portent **l'index d'ordre** du folio (0 = 1er folio), **pas** son numéro affiché |

Les « champs texte » (8 par symbole, 7 par câble) ont tous la même forme :
`texte·x·y·visible(0/1)·alignement·police·taille·?·couleur·?·?·`

### A.2 Ordre des sections

```
<< Schéma WinRelais >>
¤#Version¤          2·6·  /  EYNARD Pascal·Ingerea·  /  Version 2.6b Expert·  / 4 lignes d'infos OS
¤#Compteur¤         compteur interne d'identifiants (17990 dans TTK)
¤#NewCompteur¤
¤#Schema¤           paramètres globaux (~30 champs, non décodés : NE PAS TOUCHER)
¤#Schema1¤
¤#StyleNum¤         style de numérotation
¤#Filtre¤           filtres de numérotation automatique (M,S,H)
¤#LienXLS¤          liaison Excel (actif·?·? / nom du fichier)
¤#ImageAP¤
¤#NombreFolio¤      N
  ¤#Folio·0¤ … ¤#FIN¤            × N
¤#NombreSymbole¤    N
  ¤#Symbole·0¤ … ¤#FIN¤          × N   (numérotés 0..N-1, sans trou)
¤#FilBus¤           tous les fils de tous les folios
¤#Jonction¤         points de jonction
¤#Numero¤           numéros de fil / d'équipotentielle (absent si aucun)
¤#RenvoiF¤          renvois de folio
¤#Texte¤            textes libres
¤#ZoneTexte¤        zones de texte multilignes
¤#DSansTexte¤       dessins (traits, rectangles, cadres pointillés)
¤#DAvecTexte¤       traits avec texte
¤#Logo¤             images (chemin ABSOLU du fichier image)
¤#NombreDefCable¤   N
  ¤#DefCable·0¤ … ¤#FIN¤         × N
¤#NewNombreBornier¤ N   (borniers générés)
  ¤#NewBornier·0¤ … ¤#FIN¤
¤#FIN¤
```

Une section sans contenu est omise.

### A.3 Folio

```
¤#Folio·k¤
¤#Autre¤
29700·21000·29022·20408·296·296·339·339·3·k·Folio 1·0·1·500·500·500·500·1·1·01·0·
1·0·400·2000·0·1·arial·300·0·0·0·0·5·0·0·1·0·0·0·        (style cadre repère, colonnes)
1·0·400·2000·0·0·arial·300·0·0·0·0·5·0·0·1·0·0·0·        (style cadre repère, lignes)
¤#CartoucheTexte¤      un texte de cartouche par ligne
¤#CartoucheDessinDst¤  traits du cartouche
¤#VueFolio¤ ¤#VerrouFolio¤ ¤#InfoRevision¤ ¤#DxfDwgAP¤
¤#SymboleSupportFolioRec<k>_<1..3>¤ / ¤#SymboleSupportFolioSym<k>_<1..3>¤ … ¤#FIN¤   (×3, symboles d'arrière-plan, vides)
¤#FIN¤
```

Champs de la ligne `Autre` (index à partir de 0) :

| # | Sens |
|---|---|
| 0-1 | largeur·hauteur (29700·21000 = A4 paysage ; 21000·29700 = A4 portrait) |
| 2-3 | zone imprimable |
| 9 | index d'ordre (= k) |
| 10 | **nom interne** (« Folio 12 ») : visible dans la liste des folios |
| 13-16 | marges |
| 19 | **numéro affiché** (« 10 », « 32 ») : utilisé dans les renvois et le cartouche |

`CartoucheTexte` : `x·y·VALEUR·CLÉ·indexFolio·align·police·taille·…`.
La CLÉ est le nom du champ du modèle : `TITRE FOLIO`, `DESCRIPTION FOLIO`, `DATE DESSIN`, `DATE MODIF`,
`NOM DESSINATEUR`, `SOCIETE`, `Adresse société`. La clé `01` = champ automatique (numéro du folio,
nombre total de folios).

### A.4 Symbole

Le dessin du symbole est **entièrement recopié dans le schéma** : le `.xsy` de la librairie n'est plus
nécessaire après insertion. Toutes les coordonnées (contours, broches, champs) sont **ABSOLUES** sur le
folio : déplacer un symbole = décaler **toutes** ses lignes du même (dx, dy).

Exemple complet (sectionneur Q1 du folio 10, dessin abrégé) :

```
¤#Symbole·5¤
¤#Autre¤
5200·5600·
100·CUSTOM·Legrand_Vistop_022515_4P_63A··Q·1·1·1·4·0·4·0·0·0·
Q1·8100·5600·1·0·Arial·300·0·0·0·0·
Sectionneur général·8100·6000·1·0·Arial·200·0·0·0·0·
Legrand 022515 Vistop·8100·6300·1·0·Arial·200·0·0·0·0·
63 A - 4P - 690 V·8100·6600·1·0·Arial·200·0·0·0·0·
·400·1600·0·0·Arial·300·0·0·0·0·
·400·1600·0·0·Arial·300·0·0·0·0·
·400·1600·0·0·Arial·300·0·0·0·0·
·400·1600·0·0·Arial·300·0·0·0·0·
¤#Contour¤
5100·6000·5300·6000·20·0·0·0·0·
5200·6800·4900·6100·20·0·0·0·0·
…
¤#Arc¤
5200·6050·50·0·360·20·0·0·0·0·0·0·0·0·
…
¤#Broche¤
N·5200·5600·5200·6000·5260·5660·Arial·300·0·0·0·Arial·200·0·0·0·0·0··400·2·0·0·0·0·
N·5200·7200·5200·6800·5260·7260·Arial·300·0·0·0·Arial·200·0·0·0·0·1··400·2·0·0·0·0·
1/L1·6000·5600·6000·6000·6060·5660·Arial·300·0·0·0·Arial·200·0·0·0·0·0··400·2·0·0·0·0·
2/T1·6000·7200·6000·6800·6060·7260·Arial·300·0·0·0·Arial·200·0·0·0·0·1··400·2·0·0·0·0·
…
¤#RefCroise¤
-1·0·-1·0·0·5200·8000·NC·NO·13·5·Arial·200·0·0·0·0·10·0·0·0·0·0·0·0·0·0·0·
¤#RefConstructeur¤
LEGRAND··022515··0·
¤#LienInternet¤
····0·
¤#VueArmoire¤
A1·5200·5600·0·0·Arial·200·0·0·0·0·
··1·1·0·255·····1··0·0·0·0·0·
¤#VersionSymbole¤
1·0·sectionneur·1·0·
¤#AuteurSymbole¤
Julien·Ingerea·04/10/2026·1.0·0·
¤#FIN¤
```

Ligne 1 de `Autre` : point d'insertion (origine) du symbole.
Ligne 2 de `Autre` :

| # | Sens |
|---|---|
| 0 | `100` (échelle % ?) |
| 1 | famille / dossier de librairie (`CUSTOM`, `Bornes - Standard`, `Bobines`…) |
| 2 | nom du symbole (= nom du `.xsy`) |
| 4 | **préfixe** de repère proposé par la librairie (Q, K, X…) |
| 5-7 | drapeaux (?) |
| 8 | **index du folio** contenant le symbole |
| 10 | `4` (?) |
| 11 | **1 = borne** (prise en compte par « Générer bornier ») |
| 12 | **rotation** 0/90/180/270 |

Lignes 3 à 10 = les 8 champs : **champ 1 = repère** (Q1), champ 2 = « Valeur » (désignation),
champs 3-8 libres (Julien y met : fonction / fabricant + référence / caractéristiques).

`Broche` : `nom·x·y·xi·yi·xtexte·ytexte·police·…·DIRECTION(champ 17)·…`
- `x·y` = **point de raccordement**,
- `xi·yi` = bout intérieur du trait de broche,
- direction : 0 haut, 1 bas, 2 droite, 3 gauche.

`RefCroise` (références croisées maître/esclave, ex. bobine KM1 ↔ contacts KM1) :
champ 0 = rôle : **-1 aucun lien** ; 1 = maître ; 2/3 = esclave (NO/NC ?). Un maître est suivi d'une
ligne par esclave : `famille·symbole·?·?·?·( folio - zone )·index·…`.
**Dans TTK, tous les symboles sont à -1 : aucune référence croisée.**

`RefConstructeur` : `fabricant··référence··0·` (sert à la nomenclature).

Borne (bloc type, symbole de librairie « borne 4 mm ») :

```
¤#Autre¤
5200·3600·
100·Bornes - Standard·borne 4 mm··X·0·0·1·4·0·4·1·0·0·        (champ 11 = 1 : borne)
X1.1·5300·3500·1·0·Arial·200·0·0·0·0·                          (repère Xbornier.n°borne)
Valeur·5300·3700·0·0·Arial·200·0·0·0·0·
… 6 champs vides …
¤#Contour¤
5200·3700·5200·3600·20·0·0·0·0·
5200·4000·5200·3900·20·0·0·0·0·
5050·3650·5350·3950·20·0·0·0·0·
¤#Arc¤
5200·3800·100·0·360·20·0·0·0·0·0·0·0·0·
¤#Broche¤
1·5200·3600·5200·3600·5250·3400·arial·300·0·0·0·arial·300·0·0·0·0·0·Nom·0·2·0·0·0·0·
2·5200·4000·5200·3600·5250·3800·arial·300·0·0·0·arial·300·0·0·0·0·1·Nom·0·2·0·0·0·0·
```

Bornes à étages : repère `X1.2.3` (bornier X1, borne 2, étage 3) + section `¤#WinEcad¤` (n° d'étage).

### A.5 Fils, jonctions, numéros

`¤#FilBus¤`, **un segment par ligne**, tous folios confondus :

```
x1·y1·x2·y2·folio·1·épaisseur·couleur·style·TYPE·tiret1·tiret2·couleur1·couleur2·0·
5200·5600·5200·4000·4·1·40·16757612·0·Neutre Puissance·0·0·0·0·0·
4400·3600·4400·1600·4·1·30·0·7·Conducteur terre·500·500·65535·65280·0·     (PE vert/jaune)
```

`TYPE` = nom du **type de conducteur** (menu Fichier / Préférences / Conducteurs). Il fixe la couleur
et pilote la numérotation automatique.

> **Règle capitale** : le fichier ne contient **aucun lien explicite fil ↔ broche**. WinRelais
> considère un fil raccordé seulement si son extrémité a **exactement** les coordonnées du point de
> raccordement de la broche, ou d'une autre extrémité de fil. Un fil arrêté à 1 mm de la broche paraît
> raccordé à l'écran, mais il ne l'est pas : numérotation, liste de fils et bornier deviennent faux.
> Un symbole posé **hors grille** décale toutes ses broches : c'est la cause principale de ces défauts.

`¤#Jonction¤` : `x·y·folio·taille·?·style(1 ou 2)·couleur·?·` (point de dérivation en T, ou arrivée).

`¤#Numero¤` : `x·y·TEXTE·folio·position·police·taille·angle·…` (angle 90 = vertical).
Ex. `14600·10000·01·1·3·Arial·300·90·0·0·0·0·`.

### A.6 Renvois de folio

`¤#RenvoiF¤`, une paire de flèches reliant deux folios :

```
folioA·folioB·xA·yA·xB·yB·?·?·?·?·texteA·texteB·tailleA·tailleB·police·…
4·5·24800·12000·4000·3600·1·1·2·2·(11-B2)·(10-L6)·40·40·Arial·300·0·255·…
```

`texteA` (affiché sur le folio A) désigne la destination : `(numéro du folio B - colonne+ligne)`.
Le renvoi relie électriquement le point (xA,yA) du folio A au point (xB,yB) du folio B. Les textes
sont **stockés** : après un renumérotage de folios, ils doivent être régénérés.

Champs 9-10 = **orientation** de chaque flèche (vérifié sur les 36 exemples livrés, 23/10/2026) :
`0` = le fil arrive par le bas (flèche dessinée au-dessus du point), `1` = le fil arrive par le
haut (flèche en dessous). Horizontal : la flèche pointe **toujours vers la droite**, donc le code
dépend du côté : départ (A) `2` = fil à gauche / `3` = fil à droite ; arrivée (B) `2` = fil à
droite / `3` = fil à gauche. Un mauvais code fait dessiner la flèche et le texte **sur le fil**
(défaut vu par Julien sur f20 et f32). Le point d'un renvoi doit être le bout d'un fil droit
(pas un angle, pas un T). WinRelais dessine
flèche + texte sur **~16 mm (1600)** au-delà du point, du côté opposé au fil, sur ~2,2 mm de part
et d'autre. Conséquences : un point de renvoi doit être à ≥ 16 mm du bord du cadre côté flèche, et
deux renvois voisins espacés d'au moins 4,4 mm perpendiculairement (sinon ils se chevauchent).
Texte : `(NN-CL)` avec colonne `chr(65+(x-1300)//2000)` et ligne `(y-1300)//2000+1`, bornés à A-N / 1-9.

### A.7 Textes, dessins, images

- `¤#Texte¤` : `x·y·TEXTE··folio·0·police·taille·angle·couleur·gras·align·…`
- `¤#ZoneTexte¤` : `x·y·folio·0·police·taille·…·TEXTE` (les retours à la ligne sont codés par `·`)
- `¤#DSansTexte¤` : `x1·y1·x2·y2·forme·folio·couleur·épaisseur·…` (forme 0 = rectangle, 2 = trait ?)
- `¤#Logo¤` : `x1·y1·x2·y2·CHEMIN ABSOLU·…·folio·…` → déplacer le dossier casse l'image.

### A.8 Câbles

```
¤#DefCable·n¤
¤#Autre¤
4·4400·2800·7600·2800·0·0·0·0·        folio·x1·y1·x2·y2 du trait de câble
0·40·0·0·1·16777215·                  style
802·500·3·1·1·11·0·0·
4·0·400·400·400·400·0·
W1·3800·2650·1·6·Arial·300·0·0·0·0·   champ 1 = repère
5G2.5·8200·2500·1·0·Arial·300·0·0·0·0· champ 2 = composition
CABLE CLIENT·8200·2800·…               champ 3 = désignation
… 4 champs …
¤#BrinCable¤
1-2-3-4-5·                             liste des brins
Arial·300·0·0·0·
1·10·0·
4400·2800·1·0·                         x·y·n° de brin (un par brin)
…
¤#FIN¤
```

### A.9 Borniers générés

`¤#NewBornier·n¤` → `¤#BorAutre¤` (repère X1, position), `¤#BorDstEnt¤` / `¤#BorDstBor¤` (dessin),
`¤#BorLBorne¤` (une ligne de style puis une ligne de données par borne). Ces sections sont générées
par WinRelais (« Générer bornier ») à partir des symboles borne : **ne pas les écrire à la main**,
les faire régénérer.

### A.10 Modifier un `.xrs` par script : règles

1. WinRelais **fermé** ; travailler sur une **copie**.
2. Lire et réécrire en **UTF-8 BOM + CRLF** sans altérer les lignes non modifiées.
3. Garder le `·` final de chaque ligne de données.
4. **Ajouter un symbole** : copier un bloc `¤#Symbole·n¤ … ¤#FIN¤` existant du même type, décaler
   **toutes** ses coordonnées (origine, champs, contours, arcs, MDessin, ZoneDessin, broches, VueArmoire,
   position RefCroise), changer le repère (champ 1) et l'index de folio (ligne 2, champ 8), renuméroter
   les en-têtes `¤#Symbole·0..N-1¤`, mettre à jour `¤#NombreSymbole¤`.
5. **Ajouter un fil** : une ligne dans `¤#FilBus¤` dont les extrémités tombent **exactement** sur les
   broches, sur la grille de 400, avec le bon TYPE de conducteur.
6. **Ajouter un folio** : copier un bloc `¤#Folio¤`, mettre à jour `¤#NombreFolio¤` ; si on insère
   au milieu, **décaler l'index de folio de tous les objets globaux** des folios suivants.
7. Rouvrir dans WinRelais, contrôler le **Journal** à l'ouverture, regénérer numéros et renvois.

### A.11 Voie officielle : macros WinRelaisExpert

WinRelaisExpert est installé chez Julien (`C:\Program Files (x86)\Elec-CAO\Bin\WinRelaisExpert.exe`).
Il exécute un fichier de macros (Excel/CSV, une macro par ligne, un paramètre par colonne,
commentaire = ligne commençant par `*`, `;` ou `/`). Macros utiles :

| Macro | Paramètres |
|---|---|
| `INITIALISER_VARIABLES_DOSSIER_DEFAUT` | aucun (dossiers = celui du fichier macro) |
| `Ouvrir_Schema` / `Ouvrir_Modele` | fichier |
| `Ajouter_Folio` | position · A4/A3 · portrait/paysage · nom |
| `Ajouter_Symbole` | fichier.xsy · n° d'ordre du folio · repère · `X;Y` (1/100 mm) |
| `Ajouter_Bloc` | fichier.xrb · n° d'ordre du folio · `X;Y` |
| `Ajouter_Fichier_complet` / `Ajouter_Fichier_FolioUn` | fichier xrs/xrm |
| `Supprimer_Symbole` / `…_Sur_Folio_Ordre` / `…_Sur_Folio_Numero` | repère (· folio) |
| `Supprimer_Folio_Numero_Ordre` / `_Numero` / `_Nom` | folio |
| `Numeroter_Folio_Numero` / `_Nom` / `_Nom_Numero` | aucun |
| `Generer_Schema_Type_A` / `_B` | fichier Excel · onglet · case de départ (schémas de boucle) |
| `Transformer_Liaison_XLS` | SD / PE |
| `Sauver_Fichier` / `Sauver_Fichier_Sous` · `Executer_WinRelais` | |

Autres fonctions WinRelais utiles pour la productivité : **liaison XLS** (champs des symboles et textes
lus dans un Excel, `#B8` = cellule B8), **export/import XLS des 8 champs** des symboles, **import CSV**,
**blocs** `.xrb` réutilisables, **références croisées automatiques**, **génération de bornier**,
**numérotation automatique** des fils, **liste de fils / nomenclature** exportables.

### A.11 bis Compléments vérifiés en pratique (22/10/2026)

- **Symbole de librairie `.xsy`** : même structure qu'un bloc `¤#Symbole¤` (`¤#Autre¤ … ¤#FIN¤`,
  coordonnées dans le repère du dessin WinSymbole). Pour l'insérer : décaler toutes les coordonnées
  vers l'origine voulue, mettre l'index de folio (ligne 2, champ 8), retirer `¤#RefBaseData¤`,
  ajouter `¤#AuteurSymbole¤`. Ex. bobines : `sym_electrotech\--- M Bobine\Bobine KM.xsy` (A1 en haut,
  A2 1600 plus bas).
- **Références croisées automatiques** (menu Optimisation / Générer / Références croisées automatique) :
  relie tous les symboles **de même repère** ; le maître est celui dont la famille commence par
  `--- m` ou dont le nom de fichier contient « bobine ». Il suffit donc de nommer bobine et contacts
  pareil puis de lancer la commande. Pour deux parties d'un automate (aucune « bobine »), le lien se
  fait à la main (Modifier un symbole / onglet Liaison).
- **Référence constructeur** `Nom·Réf1·Réf2·?·0·` : convention retenue dans TTK = fabricant en Nom,
  **référence en Réf 2**, Réf 1 vide (ou code distributeur). Les esclaves n'ont pas de référence.
- **Texte d'un renvoi** `(NN-Cr)` : NN = numéro du folio de destination, C = colonne
  `chr(65 + (x - 1300) // 2000)`, r = ligne `(y - 1300) // 2000 + 1` (cadre 20 mm à partir de 13 mm).
- **Croisement de fils** : deux fils qui se croisent au milieu ne sont pas reliés. Un raccordement
  = extrémité sur extrémité (plus un point de jonction pour une dérivation en T).

### A.12 Fichiers et dossiers utiles sur le poste

| Quoi | Où |
|---|---|
| Schéma de travail | `C:\Users\Julien\Documents\10. TTK\Schema Elec\SCHEMA_ELEC_TTK.xrs` |
| Copie de travail pour l'IA | `…\Schema Elec\test_xrs_claude.xrs` |
| Outil d'analyse Python | `…\Schema Elec\outils\xrs_tool.py` (`resume`, `nomenclature`, `verifier`, `json`) |
| Édition sûre (encodage préservé, contrôles) | `…\outils\xrs_edit.py` (déplacer/copier/insérer un symbole, fils, jonctions, renvois, champs, cartouche) |
| Scripts appliqués à la copie | `…\outils\corrections_2026-10-22.py`, `…\outils\application_plan_2026-10-22.py` |
| Tableau de suivi de Julien | `TTK_Plan_Folios_Reperes.xlsx` (onglets Folios, Avancement, Repères, Règles R1-R9, Anomalies) |
| Sauvegardes auto WinRelais | `C:\Users\Public\Documents\Elec-CAO\wr-sauvegarde\` |
| Exemples | `C:\Users\Public\Documents\Elec-CAO\wr-schema\` |
| Librairies de symboles | `C:\Users\Public\Documents\Elec-CAO\sym_*` ; blocs `wr-bloc\*.xrb` ; modèles `wr-modele\*.xrm` |
| Aide | `C:\Program Files (x86)\Elec-CAO\Aide\*.chm` |

---

## PARTIE B : le schéma électrique TTK

### B.1 Contexte

- Machine : **machine de tressage TTK** (tête d'extrusion chauffée, 2 motoréducteurs sur variateurs,
  2 axes de translation pas-à-pas, automate S7-1200 G2, IHM au pupitre, relais de sécurité).
- Cartouche : **BUREAU D'ETUDES BAILLY LEVERT**, 70 boulevard Beaumarchais Paris 75011 ;
  dessinateur **THRO.J** ; dessiné le 23/09/2026.
- Description générale : « DOSSIER DE SCHEMAS ELECTRIQUES - MACHINE DE TRESSAGE TTK ».
- Format : 22 folios A4 paysage, cadre repère colonnes A… / lignes 1…, cartouche en bas.
- Repérage **IEC 81346-2** (folio 03 « Légende et conventions »).
- Alimentation : réseau 400 V 3P+N+PE (câble client W1 5G2.5). **Variante USA** : transformateur
  d'isolement T5 480 V triangle → 400Y/230 V, 15 kVA (optionnel).
- Tous les symboles sont des symboles **personnalisés** (famille `CUSTOM`) créés par Julien, nommés
  `Fabricant_Référence_description`, avec fabricant et référence renseignés (nomenclature exploitable).

### B.2 Plan des folios

| Ordre | N° | Titre | Description | Contenu actuel |
|---|---|---|---|---|
| 1 | 01 | PAGE DE GARDE | Dossier de schémas électriques - machine de tressage TTK | - |
| 2 | 02 | SOMMAIRE | Liste des folios et indices de révision | - |
| 3 | 03 | LEGENDE ET CONVENTIONS | Repérage IEC 81346-2, symboles, couleurs des conducteurs | - |
| 4 | 04 | SYNOPTIQUE GENERAL | Architecture armoire, pupitre, machine et réseau Profinet | image |
| 5 | 10 | ARRIVEE ET SECTIONNEMENT | Raccordement réseau, sectionnement, protection générale, parafoudre | X1.1-X1.4, X1.VJ, Q1, Q2, F1, T5, câble W1 |
| 6 | 11 | REPARTITEUR | Séparation triphasé et monophasé | X1, X2 |
| 7 | 12 | DISTRIBUTION 400 V | Protection des départs variateurs et freins | Q3, Q4, Q5, Q6, KM1-KM4 |
| 8 | 13 | DISTRIBUTION 230 V | Alimentations, ventilation, éclairage, prise de service | Q7-Q11, Q12, Q13, X3, G1, G2, E1 |
| 9 | 20 | PUISSANCE VARIATEUR 1 | Variateur -T1, résistance -R1, moteur -M1 | T1, R1, M1, câble W2 |
| 10 | 21 | PUISSANCE VARIATEUR 2 | Variateur -T2, résistance -R2, moteur -M2 | T2, R2, M2, câble W3 |
| 11 | 30 | ALIMENTATIONS 24 VDC | Production du 24 VDC et liaison PELV au PE | T3, T4 |
| 12 | 31 | DISTRIBUTION 24 VDC | *(description copiée du folio 30, à corriger)* | textes seulement |
| 13 | 32 | ALIMENTATION & DISTRIBUTION 48 VDC | Coupure 48 VDC, drivers et moteurs pas-à-pas de translation | T6, Q14, T7, T8, M3, M4 |
| 14 | 40 | RELAIS DE SECURITE | Relais -K10 : alimentation, bornes, réglages | K1 |
| 15 | 41 | SECURITE - ENTREES | AU, capot, sélecteur de mode, réarmement | à faire |
| 16 | 42 | SECURITE - SORTIES | STO variateurs et commande des contacteurs de puissance | à faire |
| 17 | 50 | AUTOMATE - ALIM & ENTREES TOR | Alimentation CPU S7-1200 G2 & entrées TOR | K2 (pas de fils) |
| 18 | 51 | AUTOMATE - SORTIES TOR | Contacteurs, freins, pas-à-pas, signalisation | K3 (pas de fils) |
| 19 | 52 | MODULE SM 1223 | E/S TOR complémentaires | K4, K5 (pas de fils) |
| 20 | 53 | MODULE SM 1231 TC | Température tête d'extrusion | K6 (pas de fils) |
| 21 | 54 | RESEAU PROFINET | Topologie CPU, variateurs, IHM, switch | K7 |
| 22 | 60 | PUPITRE OPERATEUR | AU, sélecteur de mode, IHM KTP700 | P1 |

Logique de numérotation : dizaines par fonction (0x général, 1x distribution, 2x puissance moteurs,
3x alimentations TBT, 4x sécurité, 5x automate, 6x pupitre). Index d'ordre dans le fichier = rang − 1.

### B.3 Nomenclature (état au 22/10/2026)

| Repère | Folio | Fonction / caractéristiques | Fabricant · référence | Broches (noms) |
|---|---|---|---|---|
| X1.VJ, X1.1-X1.4 | 10 | Bornes d'arrivée réseau 4 mm (PE, N, L1, L2, L3) | - | 1, 2 |
| Q1 | 10 | Sectionneur général 63 A 4P 690 V | Legrand 022515 (Vistop) | N, N, 1/L1…6/T3 |
| Q2 | 10 | Disjoncteur de tête 3P+N 20 A courbe C 10 kA | Hager NFT820 | N, N, 1…6 |
| F1 | 10 | Parafoudre type 2 3P+N, Imax 20 kA, Up 1,5 kV | Schneider A9L16297 | N, L1, L2, L3, PE, 11, 12, 14 |
| T5 | 10 | Transfo d'isolement US→UE 15 kVA 480 V Δ / 400Y/230 V (variante USA) | TEMCo TT1041 | H1, H2, H3, X0, X1, X2, X3, GND |
| X1 | 11 | Répartiteur tétrapolaire 125 A, 1 entrée + 7 départs | AE AEE300427 | 10-17, 20-27, 30-37, N0-N7 |
| X2 | 11 | Bornier de terre PE 1×6-25 + 26×1,5-16 mm², 100 A | Legrand 404839 | E, 1…26 |
| Q3, Q4 | 12 | Disjoncteurs moteur 6-10 A, réglage 6,5 A (variateurs 1 et 2) | Schneider GV2ME14 | 1/L1…6/T3 |
| Q5, Q6 | 12 | Disjoncteurs 2P 2 A courbe C (freins 1 et 2) | Schneider A9F74202 iC60N | 1, 2, 3, 4 |
| KM1-KM4 | 12 | Contacteurs (contacts de puissance seulement) | Schneider LC1D09BD (bobine 24 VDC) | 1/L1…6/T3 |
| Q7 | 13 | Disjoncteur différentiel 1P+N 16 A C 30 mA type A (prise) | IMO B6CR1N1630A | 1, 2, N, N |
| Q8, Q9 | 13 | Disjoncteurs 1P+N 6 A C : Q8 → alim « 24VDC AUTRE », Q9 → alim « 24VDC SECU » (d'après les textes du folio) | Hager NFT706 | 1, 2, N, N |
| Q10 | 13 | Disjoncteur 2P 4 A courbe D → alim 48 VDC | Schneider A9F75204 iC60N | 1, 2, 3, 4 |
| Q11 | 13 | Disjoncteur 1P+N 6 A C (ventilation / éclairage ?) | Schneider A9P71606 iDT40K | 1, 2, N, N |
| Q12, Q13 | 13 | Contacteurs (coupure 24 V sécurisé ?) | Schneider LC1D09BD | 1/L1…6/T3 |
| X3 | 13 | Prise de service 2P+T 16 A | Legrand 004280 | N, L, PE |
| G1, G2 | 13 | Ventilateurs armoire 230 V 19 W 92 m³/h | IDE VF92AC | N, L |
| E1 | 13 | Éclairage armoire LED 230 V 14 W | RS PRO 194-0417 | N, L |
| T1 / T2 | 20 / 21 | Variateurs 2,2 kW 5,5 A 3×380-500 V, STO, PROFINET | SEW MCX91A-0055-5E3-4-T00 | X1:PE/L1/L2/L3, X2:PE/U/V/W/+R/-R, X5:24V/GND, X6:1-6 (STO), X10:1-4, X20:1-10, X22:1-3, X23:1-4, X40, X41 |
| R1 / R2 | 20 / 21 | Résistances de freinage 100 Ω 0,1 kW | SEW BW100-001 | 1, 2 |
| M1 / M2 | 20 / 21 | Motoréducteurs frein 2,2 kW 400 V Y 4,75 A, frein 400 V AC 28 Nm, TF | SEW K39 DRN100LS4/BE5/TF | PE, U1, V1, W1, 1b, 2b, 2, 3, 4, 5 |
| T3, T4 | 30 | Alimentations 24 VDC 10 A 240 W : T3 = « 24VDC AUTRE », T4 = « 24VDC SECURISE » | RS PRO 284-0491 | N, L, +V, -V, +V, -V, PE |
| T6 | 32 | Alimentation 48 VDC 5 A 240 W | Mean Well NDR-240-48 | N, L, +V, -V, +V, -V, PE |
| Q14 | 32 | Contacteur de coupure 48 VDC | Schneider LC1D09BD | 1/L1…6/T3 |
| T7, T8 | 32 | Drivers pas-à-pas 48 VDC 6 A RMS (SW1-3 OFF), E/S 24 V | Jkongmotor JKDM860H | +V, -V, PUL±, DIR±, ENA±, A±, B± |
| M3, M4 | 32 | Moteurs pas-à-pas Nema 34, 6 A, 8,5 Nm, IP65 (translation) | StepperOnline 34IP65-85 | A+, A-, B+, B- |
| K1 | 40 | Relais de sécurité AU / protecteur, fonction 1, départ 3 (surveillé), 24 V | Schneider XPSUAF13AP | A1, A2, B2, S11, S12, S21, S22, Y1, Y2, Z1, 13/14, 23/24, 33/34 |
| K2 | 50 | CPU 1214C G2 DC/DC/DC : alimentation + 14 DI | Siemens 6ES7214-1AH50-0XB0 | L+, M, FE, L+ capt, M capt, 1M, I0.0-I0.7, I1.0-I1.5, X1 P1, X1 P2 |
| K3 | 51 | CPU 1214C G2 : 10 DQ 24 VDC 0,5 A | (même) | 3L+, 3M, Q0.0-Q0.7, Q1.0, Q1.1 |
| K4 | 52 | SM 1223 G2 : alimentation + 8 DI | Siemens 6ES7223-5BH50-0XB0 | L+, M, 1M, 2M, I8.0-I8.7 |
| K5 | 52 | SM 1223 G2 : 8 DQ | (même) | 3L+, 3M, Q8.0-Q8.7 |
| K6 | 53 | SM 1231 TC G2 : 8 entrées thermocouple | Siemens 6ES7231-5QF50-0XB0 | L+, M, AI0±…AI7± |
| K7 | 54 | Switch PROFINET 5 ports, 2 alims 12/24/48 VDC, relais alarme | Weidmüller 2682250000 (IE-SW-AL05LM-5TX) | V1±, V2±, ALM1, ALM2, P1-P5 |
| P1 | 60 | IHM KTP700 Basic PN, 24 VDC | Siemens 6AV2123-2GB03-0AX0 | L+, M, FE, X1 |
| W1 | 10 | Câble client 5G2.5 | - | brins 1-5 |
| W2 / W3 | 20 / 21 | Câbles moteur 4G2.5 | - | brins 1-4 |

Les automates et modules sont **découpés en plusieurs symboles** (alim/entrées d'un côté, sorties de
l'autre), avec la mention « brochage G2 provisoire » : les brochages S7-1200 **G2** sont à confirmer
sur la documentation Siemens.

### B.4 Types de conducteur utilisés

| TYPE (nom exact) | Couleur (COLORREF → teinte) | Épaisseur | Usage |
|---|---|---|---|
| `Puissance` | 0 → noir | 40 | phases L1/L2/L3, 230 V L |
| `Neutre Puissance` | 16757612 → bleu clair | 40 | neutre |
| `Conducteur terre` | 0, style 7 tiret 500/500 jaune 65535 / vert 65280 | 30 | PE |
| `Commande 24V~` | 255 → rouge | 20 | commande alternative (**mal employé, voir B.6**) |
| `Commande 24VDC` | 11302912 → bleu foncé | 20 | commande 24 V continu (+24 V) |
| `0V` | 16744448 → bleu | 20 | 0 V continu |
| `Autre tension DC` | 4227327 → orange | 20 | 48 VDC, autres tensions continues |

Rappel (EN 60204-1 §13.2.4, à confirmer avec la légende du folio 03) : PE vert/jaune, neutre bleu
clair, puissance AC noir, commande AC rouge, commande DC bleu, circuits d'interverrouillage
alimentés par une source externe orange.

### B.5 Liaisons entre folios (renvois existants)

10↔11 (×5) · 11↔12 (×10) · 11↔13 (×7) · 12↔20 (×3) · 12↔21 (×3) · 13↔20 · 13↔30 (×4) · 13↔32 (×2) ·
20↔21 · 21↔30 · 30↔32 · 40↔41 (×2). Les renvois horizontaux en bas de folio (y ≈ 18800-19200)
chaînent le **PE** d'un folio au suivant.

### B.6 Points relevés (analyse du 22/10/2026, schéma en cours)

**Erreurs certaines (raccordements faux)**
- Fils arrêtés **à 1 mm** d'une broche, donc non raccordés : F1:N (folio 10), T5:H1, H2, H3
  (folio 10), G1:L et G2:L (folio 13), T7:PUL+ (folio 32).
- Fils arrêtés **à 4 mm** des broches PUL±, DIR± et ENA± de **T7 et T8** (folio 32).
- Symboles posés **hors grille** : T7 (15600, 8700), M3 (14800, 14700), K5 (9100, 8200). Les
  replacer sur la grille de 4 mm, puis reprendre les fils.

**Incohérences à corriger**
- Même contacteur LC1D09BD repéré **KM1-KM4** (folio 12) et **Q12, Q13, Q14** (folios 13 et 32) :
  choisir une convention unique. En IEC 81346-2, un contacteur est de classe Q (QA) ; KM est
  l'ancienne norme française.
- Folio 40 : la description annonce « -K10 » alors que le relais de sécurité est repéré **K1**.
- Copier-coller dans les champs : R2 décrit « Résistance de freinage **T1** », T2 « Variateur **M1** ».
- Description du folio 31 identique à celle du folio 30.
- Noms internes de folio en double : « Folio 12 » (folios 12 et 31), « Folio 13 » (13 et 32),
  « Folio 20 » (20 et 53), « Folio 21 » (21 et 54). Corrigible par la macro `Numeroter_Folio_Nom`.
- **Type de conducteur** : 13 fils « Commande 24V~ » (rouge, alternatif) sur le folio 40 (relais de
  sécurité 24 VDC) et 13 sur le folio 32 (commande des drivers), plus 2 sur chacun des folios 10, 20 et
  21. Vérifier s'il faut les passer en `Commande 24VDC` / `0V`.

**Normal à ce stade (travail en cours)**
- 30 fils en attente : sorties de T5 (folio 10), départs KM3 et KM4 (folio 12), câbles W2/W3 vers les
  bornes moteur et frein de M1 et M2 (folios 20/21), bornes de K1 vers les folios 41/42 (folio 40)…
- Folios 31, 41, 42 vides ; automates (50-53), switch (54) et IHM (60) posés sans aucun fil.
- Aucun numéro de fil (`¤#Numero` absent) et aucune référence croisée : les bobines des contacteurs
  KM1-KM4/Q12-Q14 ne sont pas encore dessinées (prévues folios 42/51).
- Broches en double dans certains symboles (N, N sur Q1, Q2, Q7…Q11 ; +V, -V doublés sur T3, T4,
  T6) : cohérent avec le matériel, mais rend la liste de fils ambiguë. Un nommage N/N' ou 7/8
  serait préférable.

### B.7 Questions ouvertes à poser à Julien avant de compléter

- Convention de repère des contacteurs : Q (IEC 81346-2) ou KM ?
- Rôle exact des contacteurs Q12/Q13 sur le folio 13 (coupure du primaire des alims ?) et de Q11.
- Les freins M1/M2 (400 V AC) sont-ils pilotés par les variateurs (sorties frein) ou par KM3/KM4 ?
- Câblage STO : X6 des MCX91A vers les sorties de sécurité de K1 (folio 42) ?
- Affectation des E/S automate (liste I/O) : existe-t-elle dans un Excel ? Si oui, la **liaison XLS**
  ou les macros WinRelaisExpert permettent de remplir les folios 50-53 automatiquement.

---

### B.8 Copie de travail `test_xrs_claude.xrs` (état au 22/10/2026 soir)

Les parties B.2 à B.6 décrivent l'**original** `SCHEMA_ELEC_TTK.xrs`. La copie a reçu en plus :

- **Repérage cible** du tableau de Julien (règle R6 : lettre + n° de folio maître + rang) :
  X101.1-4/X101.VJ, W101, Q101, Q102, F101, T101, X111, X112, Q121-Q124, Q131-Q137, X131, G131, G132,
  E131, E132, T201, R201, M201, W201, T211, R211, M211, W211, T301, T302, T321, T322, T323, M321, M322,
  K401, K501 (ex K2 + K3), K521 (ex K4 + K5), K531, K541, P601, KM1, KM2, Q421 (ex KM3), Q422 (ex KM4),
  Q423 (ex Q14). **Q12 et Q13 inchangés** (décision en attente). Repères écrits sans « - ».
- Champs 2-4 des symboles = colonnes Désignation / Fabricant + réf. / Caractéristiques du tableau.
- Esclaves sans référence constructeur : K501 et K521 partie sorties, pôles KM1, KM2, Q421-Q423.
- **f42** : 5 bobines maîtres KM1, KM2, Q421, Q422, Q423 (LC1D09BD, bobine 24 V CC), non câblées.
- **f13** : Q136 (ventilateurs) et Q137 (éclairage, 2 lampes) créés et câblés, E132 ajouté ;
  référence des 2 disjoncteurs « À définir ».
- **f12 → f20 / f21** : renvois des départs frein (Q421 → M201 bornes 2-3, Q422 → M211).
- Types de fil corrigés (anomalie 10) : 24 V CC sur f32 / f40 / TF, 0 V sur K401:A2, frein M211 en
  Puissance, T101:X0 en neutre, T101:GND en terre.
- Descriptions f20, f21, f31, f40 ; noms internes « Folio NN » ; « BAILLY » corrigé.
- Corrections géométriques : T322, M321, K521 recalés sur la grille, 11 fils raccordés, 2 renvois PE.

Reste à faire (décisions de Julien) : sécurité f41, ordres de commande des bobines f42, alimentation
24 V f31, câblage automate f50-f54, TF → X10, renvois X5 / X6 / X40-X41, Q12 / Q13, folios 70-90,
synoptique f04, puis références croisées automatiques et numérotation dans WinRelais.

### B.9 Reconstruction complète (22/10/2026 nuit) – génération par script

`test_xrs_claude.xrs` est maintenant **entièrement généré** par `outils/ttk_schema.py` (bibliothèque
`outils/xrs_gen.py`) : `python ttk_schema.py` réécrit la copie de travail et lance les contrôles
(géométrie, renvois dans le cadre, chevauchements, spécification des équipotentielles). État :
27 folios, 131 symboles, 597 fils, 104 renvois, 0 problème de contrôle, 0 erreur au vérificateur.

Retours de Julien intégrés : renvois tous dans le cadre et sans chevauchement (orientation A.6) ;
câbles moteurs SEW blindés (W201 / W211 « 4G2,5 blindé », W202 / W212 « 4 x 1 mm² blindé »
frein + TF, blindage repris au presse-étoupe CEM) ; contacts esclaves du folio 40 avec description
de l'appareil (« Retour <désignation> ») ; folio 41 refait en deux voies (voie 1 : S411 / S412
NF 1-2, B411 ; voie 2 : NF 21-22, B412) ; bornes X701.17-.24 = freins + TF des moteurs.
Retours du 23/10 intégrés : contenu de chaque folio 10-60 centré dans le cadre (`Gen.centrer`) ;
pôles des LC1D09 (KM1, KM2, Q421-Q423) avec fonction / marque + réf. / caractéristiques (sans
référence constructeur : elle reste sur la bobine f42) ; f13 : phase de chaque départ (24 V = L1,
48 V = L2, 230 V aux. = L3) ; f20 / f21 : textes moteur à droite du moteur, étiquettes de câble
déplacées (`cable(..., etiq=(x, y))`), plus de chevauchement ; f54 : destination de chaque port ;
f60 = IHM seule + liste du contenu du pupitre ; f70 / f71 : désignation des appareils des 2 côtés ;
garde : client TTK, machine 001-EU, TN-S, Icc 6 kA. Partie sécurité (f40-f42) en attente des
explications de Julien ; partie automate (f50-f52) gelée tant que `PROPOSITION_ES_AUTOMATE.csv`
n'est pas validé ; f53 validé par Julien.
Folios 70 / 71 : tableau de contrôle des borniers X701 / X711 calculé depuis le schéma ; méthode
complète dans `METHODE_BORNIERS.md`. La page de garde (f01) plaît à Julien : ne pas la changer.

## PARTIE C : contrôles à faire systématiquement

À chaque étape (manuellement, ou avec `python outils/xrs_tool.py verifier <fichier.xrs>`) :

1. **Raccordement** : chaque extrémité de fil coïncide exactement avec une broche, une autre extrémité
   de fil, un point d'un autre fil (dérivation, avec point de jonction) ou un renvoi. Sinon :
   - écart ≤ 4 mm d'une broche → **erreur** (fil faussement raccordé) ;
   - sinon → fil en attente (normal si le folio est en cours).
2. **Grille** : origine de chaque symbole multiple de 200 (idéalement 400).
3. **Repères** : uniques (sauf maître/esclaves liés), préfixe cohérent avec le type de matériel,
   même référence fabricant = même préfixe.
4. **Types de conducteur** : cohérents avec la tension (pas de `24V~` sur du continu), un seul type par
   équipotentielle.
5. **Renvois** : le texte `(NN-…)` pointe bien vers le numéro actuel du folio de destination.
6. **Folios** : numéros, noms, titres et descriptions uniques et à jour.
7. **Champs** : désignations sans copier-coller faux (T1/T2, M1/M2, R1/R2).
8. Avant livraison : numérotation des fils, références croisées bobines ↔ contacts, génération des
   borniers, nomenclature et liste de câbles depuis WinRelais.
