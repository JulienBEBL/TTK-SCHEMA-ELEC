# Format des fichiers WinRelais `.xrs` / `.xrm` (rétro-ingénierie)

Établi le 22/10/2026 à partir de `SCHEMA_ELEC_TTK.xrs` (WinRelais **2.6b Expert**) et des 36 exemples
de `C:\Users\Public\Documents\Elec-CAO\wr-schema`, recoupés avec l'aide officielle (`WinRelais.chm`,
`WinRelaisExpert.chm`). Le format n'est pas documenté par l'éditeur (Ingerea / P. Eynard) : les champs
marqués **?** sont déduits, pas confirmés.

Outil associé : [outils/xrs_tool.py](outils/xrs_tool.py) (lecture seule).

---

## 1. Généralités

| Élément | Valeur |
|---|---|
| Nature | Texte, une info par ligne, organisé en sections |
| Encodage | v2.6 : **UTF-8 avec BOM**. Versions ≤ 2.5 : **Windows-1252** sans BOM |
| Fin de ligne | CRLF |
| Séparateur de champs | `·` (U+00B7, point médian). Chaque ligne de données **se termine par `·`** |
| En-tête de section | `¤#Nom¤` ou `¤#Nom·n¤` (`¤` = U+00A4), ex. `¤#Folio·3¤`, `¤#Symbole·12¤` |
| Fin de bloc | `¤#FIN¤` (les blocs Folio, Symbole, DefCable, Bornier sont fermés par un `¤#FIN¤`) |
| Unité | **1/100 mm**. Origine = coin haut-gauche du folio, Y vers le bas |
| Grille | 4 mm = **400**. Pas des broches et des fils : 400 (parfois 200) |
| Couleurs | entier COLORREF Windows `R + 256·G + 65536·B` (255 = rouge, 0 = noir, -1 = défaut) |
| Index de folio | Les objets globaux (fils, jonctions, textes, câbles…) portent l'**index d'ordre** du folio (0 = 1er), pas son numéro affiché |
| `.xrm` (modèle) | Même format que `.xrs` (dixit l'aide) |

Une même liste de 8 « champs texte » revient pour les symboles, les câbles et les borniers :
`texte·x·y·visible(0/1)·alignement·police·taille·?·couleur·?·?·`.

## 2. Ordre des sections dans le fichier

```
<< Schéma WinRelais >>
¤#Version¤            2·6·  /  auteur·société·  /  "Version 2.6b Expert"  / infos OS (v2.6)
¤#Compteur¤           compteur interne (identifiants)
¤#NewCompteur¤
¤#Schema¤             paramètres globaux du schéma (~30 champs, non décodés)
¤#Schema1¤
¤#StyleNum¤           style de numérotation
¤#Filtre¤             M,S,H…  filtres de numérotation automatique
¤#LienXLS¤            liaison Excel : actif·?·?  / nom fichier xls
¤#ImageAP¤
¤#NombreFolio¤        N
  ¤#Folio·0¤ … ¤#FIN¤          × N   (voir §3)
¤#NombreSymbole¤      N
  ¤#Symbole·0¤ … ¤#FIN¤        × N   (voir §4)
¤#FilBus¤             tous les fils, tous folios confondus (§5)
¤#Jonction¤           points de jonction (§5)
¤#Numero¤             numéros de fil / potentiels (absent si aucun)
¤#RenvoiF¤            renvois de folio (§6)
¤#Texte¤              textes libres (§7)
¤#ZoneTexte¤          zones de texte multilignes
¤#DSansTexte¤         dessins : traits, rectangles (cadres pointillés…)
¤#DAvecTexte¤         traits avec texte (flèches de commentaire)
¤#Logo¤               images (chemin ABSOLU du fichier image)
¤#NombreDefCable¤     N
  ¤#DefCable·0¤ … ¤#FIN¤       × N   (§8)
¤#NewNombreBornier¤   N  (borniers générés, §9)
  ¤#NewBornier·0¤ … ¤#FIN¤
¤#FIN¤
```

Les sections absentes sont simplement omises.

## 3. Folio

```
¤#Folio·k¤
¤#Autre¤
29700·21000·29022·20408·296·296·339·339·3·k·Folio 1·0·1·500·500·500·500·1·1·01·0·
 ...2 lignes de style du cadre repère (colonnes/lignes)...
¤#CartoucheTexte¤     une ligne par texte du cartouche
¤#CartoucheDessinDst¤ traits du cartouche
¤#VueFolio¤ / ¤#VerrouFolio¤ / ¤#InfoRevision¤ / ¤#DxfDwgAP¤
¤#SymboleSupportFolioRec<k>_<1..3>¤ + ¤#SymboleSupportFolioSym<k>_<1..3>¤ … ¤#FIN¤
                      3 symboles « support » (arrière-plan) par folio, vides en général
¤#FIN¤
```

Ligne `Autre` (index des champs à partir de 0) :

| # | Sens |
|---|---|
| 0-1 | largeur, hauteur du folio (29700×21000 = A4 paysage ; 21000×29700 = A4 portrait) |
| 2-3 | zone imprimable |
| 9 | index d'ordre (redondant avec l'en-tête) |
| 10 | **nom interne** du folio (« Folio 12 ») |
| 13-16 | marges |
| 19 | **numéro affiché** du folio (« 10 », « 32 »…), utilisé dans les renvois et le cartouche |

`CartoucheTexte` : `x·y·valeur·clé·folio·align·police·taille·…`. La **clé** est le nom du champ du
modèle de cartouche (`TITRE FOLIO`, `DESCRIPTION FOLIO`, `DATE DESSIN`, `NOM DESSINATEUR`, `SOCIETE`,
`Adresse société`…). La clé `01` désigne les champs automatiques (n° de folio, nombre total de folios).

## 4. Symbole

Ligne 2 de `Autre` du symbole : `100·famille·symbole··préfixe·N·…·folio·…`. **Champ 5 (`N`) = afficher les noms de broches** (1 = oui, 0 = non), mesuré le 30/10 sur U3 / U4 : seul ce champ change, les textes `MDessin` restent dans le fichier.

Un symbole est **entièrement copié dans le schéma** (dessin compris) : le fichier `.xsy` de la
librairie n'est plus nécessaire après insertion. Toutes les coordonnées (contours, broches, champs)
sont **absolues** sur le folio : déplacer un symbole oblige à décaler toutes ses lignes.

```
¤#Symbole·n¤
¤#Autre¤
5200·5600·                                    origine (point d'insertion)
100·CUSTOM·Legrand_Vistop_022515_4P_63A··Q·1·1·1·4·0·4·0·0·0·
Q1·8100·5600·1·0·Arial·300·0·0·0·0·            champ 1 = REPÈRE
Sectionneur général·8100·6000·1·0·Arial·200·…  champ 2 (« Valeur » par défaut)
… champs 3 à 8 …
¤#Contour¤     segments : x1·y1·x2·y2·épaisseur·style·couleur·…
¤#Arc¤         cercles/arcs : xc·yc·rayon·angle début·angle fin·épaisseur·…
¤#ZoneDessin¤  polygones pleins
¤#MDessin¤     textes dessinés dans le symbole (« M », « 3~ », « 3L+ »…)
¤#Broche¤      une ligne par borne (voir ci-dessous)
¤#WinEcad¤     (option) n° d'étage pour borniers à étages
¤#RefCroise¤   paramètres de référence croisée (+ liste des esclaves si maître)
¤#RefConstructeur¤  fabricant··référence··
¤#LienInternet¤
¤#VueArmoire¤  données d'implantation WinArmoire
¤#VersionSymbole¤   version·?·dossier de librairie·
¤#AuteurSymbole¤    auteur·société·date·version·  (v2.6)
¤#FIN¤
```

Ligne 2 de `Autre` :

| # | Sens |
|---|---|
| 0 | 100 (échelle en % ?) |
| 1 | famille / dossier de librairie (`CUSTOM`, `Bornes - Standard`, `Bobines`…) |
| 2 | nom du symbole (= nom du `.xsy`) |
| 4 | **préfixe** de repère proposé (Q, K, X, T…) |
| 5-7 | drapeaux (?) |
| 8 | **index du folio** où se trouve le symbole |
| 10 | 4 (?) |
| 11 | **1 = borne** (prise en compte par la génération de bornier) |
| 12 | angle de rotation (0/90/180/270) |

`Broche` : `nom·x·y·xi·yi·xtexte·ytexte·police…·direction(champ 17)·…`
- `x·y` = **point de raccordement** (un fil est raccordé si son extrémité tombe exactement dessus),
- `xi·yi` = extrémité intérieure du trait de broche,
- direction : 0 haut, 1 bas, 2 droite, 3 gauche.

`RefCroise` : 1er champ = rôle (**-1 aucun lien**, 1 = maître, 2/3 = esclave NO/NC ?). Un maître (bobine)
est suivi d'une ligne par esclave : `famille·symbole·?·?·?·( folio - colonne )·index·…`.

## 5. Fils et jonctions

`¤#FilBus¤`, une ligne par segment :

```
x1·y1·x2·y2·folio·1·épaisseur·couleur·style·TYPE·tiret1·tiret2·couleur1·couleur2·0·
5200·5600·5200·4000·4·1·40·16757612·0·Neutre Puissance·0·0·0·0·0·
6000·5600·6000·4000·4·1·30·0·7·Conducteur terre·500·500·65535·65280·0·   (vert/jaune alterné)
```

`TYPE` = nom du **type de conducteur** (onglet Conducteurs, menu Fichier / Préférences). C'est lui
qui fixe la couleur et sert à la numérotation automatique. Types présents dans le schéma TTK :
`Puissance`, `Neutre Puissance`, `Conducteur terre`, `Commande 24V~`, `Commande 24VDC`, `0V`,
`Autre tension DC`.

Raccordement : il n'y a **aucun lien explicite fil ↔ broche** dans le fichier. WinRelais déduit la
connexion de la **coïncidence exacte des coordonnées**. Un fil qui s'arrête à 1 mm d'une broche paraît
raccordé à l'écran mais ne l'est pas (numérotation et bornier faux).

`¤#Jonction¤` : `x·y·folio·taille·?·style(1/2)·couleur·?·`.

## 6. Renvois de folio

`¤#RenvoiF¤` : un renvoi = une paire de flèches reliant 2 folios.

```
folioA·folioB·xA·yA·xB·yB·?·?·?·?·texteA·texteB·tailleA·tailleB·police…
4·5·24800·12000·4000·3600·1·1·2·2·(11-B2)·(10-L6)·40·40·Arial·300·…
```

`texteA` (affiché sur le folio A) pointe vers le folio B : `(numéro-colonneLigne)`. Les textes sont
**stockés** : un renumérotage de folios sans régénération laisse des renvois faux.

## 7. Textes

`¤#Texte¤` : `x·y·texte··folio·0·police·taille·angle·couleur·gras·align·…`
`¤#ZoneTexte¤` : `x·y·folio·…·texte` (les retours à la ligne sont codés par `·`).

## 8. Câbles

```
¤#DefCable·n¤
¤#Autre¤
4·4400·2800·7600·2800·0·0·0·0·      folio·x1·y1·x2·y2 (trait du câble)
… 3 lignes de style …
W1·3800·2650·…                      champs 1-7 : repère, section (5G2.5), désignation…
¤#BrinCable¤
1-2-3-4-5·                           liste des brins
…
4400·2800·1·0·                       position de chaque brin et son n°
¤#FIN¤
```

## 9. Borniers générés (Exemples 16, 24)

`¤#NewBornier·n¤` → `¤#BorAutre¤` (repère X1, position, styles), `¤#BorDstEnt¤` / `¤#BorDstBor¤`
(dessin), `¤#BorLBorne¤` (une ligne de style + une ligne de données par borne : n°, position, repère
de la borne schéma `X1.1.2`…). Générés par WinRelais à partir des symboles dont le drapeau « borne »
vaut 1 et dont le repère est `Xn.m` (ou `Xn.m.étage`).

---

## 10. Règles pour modifier un `.xrs` par script

1. **WinRelais fermé**, copie de sauvegarde avant toute écriture (`wr-sauvegarde` n'est pas un
   historique fiable pour ça).
2. Réécrire **dans l'encodage d'origine** (UTF-8 BOM ici), en CRLF, sans toucher aux lignes non
   modifiées. Ne jamais passer par un éditeur qui « normalise » le fichier.
3. Garder le `·` final de chaque ligne.
4. Ajouter un symbole = copier un bloc `¤#Symbole¤` existant, **décaler toutes ses coordonnées**,
   renuméroter les en-têtes `¤#Symbole·n¤` (0..N-1) et mettre à jour `¤#NombreSymbole¤`.
   Même logique pour les folios (`¤#Folio·k¤`, `¤#NombreFolio¤`, et l'index de folio des objets
   globaux qui suivent).
5. Rouvrir le fichier dans WinRelais et contrôler le **Journal** à l'ouverture.

Les macros **WinRelaisExpert** (installé : `C:\Program Files (x86)\Elec-CAO\Bin\WinRelaisExpert.exe`)
offrent une voie officielle pour une partie de ces opérations : `Ajouter_Symbole fichier.xsy folio
repère X;Y`, `Ajouter_Bloc`, `Ajouter_Folio`, `Ajouter_Fichier_complet`, `Supprimer_Symbole`,
`Numeroter_Folio_Numero`… (une macro par ligne dans un fichier Excel/CSV). Voir l'aide WinRelaisExpert.
