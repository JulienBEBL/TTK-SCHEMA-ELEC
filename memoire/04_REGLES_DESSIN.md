# 04 · Règles de dessin (demandes de Julien)

À appliquer sur **tous les folios**, à chaque version. Date = date de la demande.

## Ordre des folios (v9, 30/10)
Ordre voulu par Julien : alimentations (400, 230, 48, 24), switch, variateurs, sécurité, IHM, automate, borniers.
Le 29/10 la sécurité a été mise en tête par erreur (« AU » compris comme tout le bloc sécurité) : **remise à sa place le 30/10, f40 à f42.**
Le script garde les **anciens numéros en interne** (clés de `F`, textes « fNN ») ; le dict `NUMFOL` de `ttk_schema.py` donne le numéro affiché et `ren()` traduit les « fNN » des textes. **Dans le script, écrire toujours l'ancien numéro.**

| Affiché (v9) | Ancien (script) | Contenu |
|---|---|---|
| 01, 02, 04 | idem | garde, sommaire, synoptique en logigramme (f03 légende supprimé le 02/11) |
| 20 | 10 | arrivée, QS1, QF1, départs PE, variante USA |
| 21 | 12 | distribution 400 V (bus) |
| 22 | 13 + 30 | 230 V alimentations : QF4 / QF5 → T1 / T2, QF6 → T3 48 V, H2, PELV X36.1 |
| 23 | 14 | 230 V services : QF7 à QF10, X14, EL1 / EL2, EV1 / EV2 |
| 24 | 32 | 48 V : 4 arrivées de T3, KA2 (2 pôles), drivers, moteurs pas-à-pas |
| 25 | 31 | distribution 24 V : X31, X32, X33, voyant H3 |
| 30 | 54 | switch PROFINET (avant les variateurs, demande de Julien) |
| 31, 32 | 20, 21 | variateurs U1, U2 |
| 40, 41, 42 | idem | sécurité : relais KA1, entrées (AU, capots, sélecteur, réarmement), sorties (bobines, STO) |
| 45 | 60 | pupitre (IHM) |
| 50 à 53, 70, 71, 80, 85, 90 | idem | automate, borniers, câbles, implantation, nomenclature |

Supprimés : f11 (répartiteur X12 et barrette de terre X13 : pas de symbole, demande du 29/10), f30 (fondu dans f22), f43.
Le sommaire (f02) est généré à partir de cette liste : Julien veut qu'il soit tenu à jour à chaque version.

## Mise en page
1. **Aucune note encadrée** sur les folios (29/10). Les points à vérifier vont dans `05_POINTS_OUVERTS.md`.
2. **Contenu centré** dans le cadre de chaque folio (23/10, redemandé le 29/10 pour f22) : `g.centrer` automatique. Exception (30/10) : bus, barres et variateurs restent **en haut, à la même hauteur d'un folio à l'autre**, centrés en largeur seulement (`HAUT` dans le script : f21, f22, f23, f25, f30, f31, f32, f40 à f42, f45, f50 à f53). Modèle : le f22.
3. **Aucun texte qui se superpose** (23/10) : textes, étiquettes de câble, renvois. Le bloc d'information d'un composant peut être déplacé indépendamment du symbole (`fpos`).
4. **Pas de pastille d'état** : le carré de couleur en haut des folios est supprimé (30/10).
5. **Rendu propre « comme un vrai schéma »** (29/10) : pas de longs fils qui font le tour du folio, pas de croisements inutiles. Appareils en parallèle : l'un sous l'autre (EL1 / EL2, EV1 / EV2 au f23). Les piquages d'un bus croisent les autres lignes du bus : normal.
6. Un folio trop chargé se **sépare en deux** (29/10 : f13 → alimentations + services). Un folio inutile se supprime.
7. **Fils assez longs** entre deux appareils (au moins 1600 à 2400) pour que le numéro de fil soit lisible (29/10, f22 / f23). Appareils d'une même chaîne **dans l'axe** (QF9 → QF10 → X14).
8. Arrivée réseau : texte « ARRIVEE RESEAU ... » **dans un cadre** (29/10, f20).

## Composants
9. Affichage : **fonction + caractéristiques** seulement. Marque et référence (champ 3) **masquées** sur tous les composants sauf les borniers (29/10) ; la donnée reste dans le symbole (nomenclature). Fait dans `_place_ren` (`shown=(2, 4)` par défaut).
9 bis. **Noms de broches** (30/10) : case WinRelais = champ 5 de la 2e ligne de `Autre` du symbole (1 = affichés, 0 = masqués). Dans le script : `noms=True / False` à la pose. **Règle de Julien (02/11) : on ne masque pas par principe, cas par cas quand il le demande.** Masqués : TR1 (f20), U3, U4, M3, M4 (f24).
10. Repérage : lettres de fonction + n° d'ordre, sens de l'énergie (28/10, `docs/NOMMAGE_2026-10-28.md`). Maître = référence fabricant ; esclaves = même repère, sans référence. Contacteur utilisé comme relais / contacteur auxiliaire = **KA** (KA2, 29/10), même si la référence est celle d'un contacteur moteur.

## Synoptique (f04, 02/11)
Logigramme : blocs encadrés (titre en gras + 1 à 3 lignes, n° de folio dans le titre), flèches dans le sens de l'énergie, PROFINET en pointillés, variante USA en pointillés. Pas de note en bas. Un texte plus large que son cadre arrête le script.

## Disposition d'une rangée de contacts (f50, alignement de Julien du 30/10)
Modèle à reprendre pour les folios d'E/S (`entree()` dans le script, coordonnées du fichier) :
- Pas entre colonnes : **800**. Trop étroit pour les textes à côté des contacts : d'où 2 niveaux en quinconce.
- **Bornes alignées sur 2 lignes** : haut y = 4400, bas y = 11200, quelle que soit la colonne.
- **Contacts sur 2 niveaux** : haut y = 5600, bas y = 8000, en alternance d'une colonne à l'autre (un repère ne touche jamais celui du voisin).
- Écarts verticaux : collecteur 24 V → borne 400 ; borne 400 de haut ; borne → contact haut 800 ; contact 1600 ; contact haut → contact bas 800 ; contact bas → borne du bas 1600 ; borne du bas → broche automate 1200.
- Une colonne sans borne (KM1, KM2, KA2) garde les mêmes niveaux de contact.
Julien a laissé S1 et S2 un peu décalés dans son fichier ; le script les aligne sur les mêmes niveaux.

## Câbles variateur (f31, f32, 30/10)
Moteur dans l'axe de X2 (fils droits, plus d'escalier). Les 3 câbles W sur **une seule ligne**, textes à côté de leur câble, sans chevauchement. Frein sans croisement.

## Renvois
11. Le texte de description d'un renvoi est **bien placé** (centré sur le renvoi ou le groupe de renvois) (23/10).
12. Le renvoi ne doit **jamais** être dessiné sur le fil : flèche du côté opposé au fil (codes A/B, voir `07_METHODE_TRAVAIL.md`).
13. Distribution de puissance (29/10) : **bus tétra L1 L2 L3 N** en haut des folios f21, f22, f23, enchaîné par renvois, chaque appareil se pique sur ses phases [D]. Points de jonction acceptés sur un bus.

## Potentiels de commande
14. **Barres 24VELEC et 0 V en haut** du folio (24 V au-dessus, 0 V dessous), « comme dans tous les schémas » (29/10), sur tous les folios de commande. Un piquage 24 V croise la barre 0 V : normal. Un appareil dont le 0 V est en bas remonte par un collecteur sur le côté.
15. Distribution TBT : **un fil par appareil** depuis le bornier de distribution, sans point de dérivation (28/10). Croisement sans jonction accepté.
16. **24VSEC** (T1, X33) et **24VELEC** (T2, X31), 0 V, +48 V / 0 V 48 (29/10).

## Fils
17. **Numéros de fil** : les fils de puissance portent le nom de leur potentiel, **L1, L2, L3, N, PE** (et U, V, W en sortie de variateur), sur **chaque tronçon**, même court (28/10, précisé le 29/10). PE nommé sur les folios de puissance (pas les FE de l'automate / IHM). Les autres fils ne sont pas numérotés tant que le schéma n'est pas fini.
18. Numéros **alignés et centrés** (29/10, « carré et propre ») : noms des fils parallèles voisins sur une même ligne ; nom d'un bus près de son extrémité gauche, aligné sur les autres lignes du bus. **Jamais sur le numéro de brin d'un câble** (30/10, f20) : WinRelais écrit le brin juste au-dessus du croisement, le nom du fil reste au moins 400 au-dessus ou 100 en dessous.
19. **Terre, règle C partout** (29/10) : pas de PE qui descend en bas du folio. Chaque appareil : **fil PE court + renvoi** vers la terre de l'arrivée (f20), où le PE de X11 se divise en un départ par appareil. Moteur : PE → X2 PE du variateur, puis X1 PE du variateur en renvoi court.
20. Types de conducteur : `Puissance` (phases), `Neutre Puissance`, `Conducteur terre` (PE), `Commande 24VDC`, `0V`, `Autre tension DC` (48 V, TF ; PROFINET provisoire). Jamais `Commande 24V~` sur un circuit continu.

## Textes
21. Phase de chaque départ 230 V : visible par le piquage sur le bus et le numéro de fil (les petits textes « L1 / L2 / L3 » du 23/10 sont retirés en v8).
22. Borniers f70 / f71 : provenance du fil écrite **des deux côtés** de la borne (23/10).
23. Folio PROFINET : texte sur chaque fil indiquant le composant de destination (23/10).
