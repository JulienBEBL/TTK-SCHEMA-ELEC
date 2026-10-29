# 04 · Règles de dessin (demandes de Julien)

À appliquer sur **tous les folios**, à chaque version. Date = date de la demande.

## Ordre des folios (29/10 soir, v8)
Ordre voulu par Julien : AU / sécurité, alimentations (400, 230, 48, 24), switch, variateurs, IHM, automate, borniers.
Le script garde les **anciens numéros en interne** (clés de `F`, `STATUT`, textes « fNN ») ; le dict `NUMFOL` de `ttk_schema.py` donne le numéro affiché et `ren()` traduit les « fNN » des textes. **Dans le script, écrire toujours l'ancien numéro.**

| Affiché (v8) | Ancien (script) | Contenu |
|---|---|---|
| 01 à 04 | 01 à 04 | garde, sommaire, légende (conducteurs seuls), synoptique |
| 10 | 41 | sécurité - entrées (AU, capots, sélecteur, réarmement) |
| 11 | 40 | relais de sécurité KA1 |
| 12 | 42 | sécurité - sorties (bobines, STO) |
| 20 | 10 | arrivée, QS1, QF1, départs PE, variante USA |
| 21 | 12 | distribution 400 V (bus) |
| 22 | 13 + 30 | 230 V alimentations : QF4 / QF5 → T1 / T2, QF6, H2, PELV X36.1 |
| 23 | 14 | 230 V services : QF7 à QF10, X14, EL1 / EL2, EV1 / EV2 |
| 24 | 32 | 48 V : T3, KA2, X34 / X35, drivers, moteurs pas-à-pas |
| 25 | 31 | distribution 24 V : X31, X32, X33, voyant H3 |
| 30 | 54 | switch PROFINET (avant les variateurs, demande de Julien) |
| 31, 32 | 20, 21 | variateurs U1, U2 |
| 40 | 60 | pupitre (IHM) |
| 50 à 53, 70, 71, 80, 85, 90 | idem | automate, borniers, câbles, implantation, nomenclature |

Supprimés : f11 (répartiteur X12 et barrette de terre X13 : pas de symbole, demande du 29/10), f30 (fondu dans f22), f43.
Le sommaire (f02) est généré à partir de cette liste : Julien veut qu'il soit tenu à jour à chaque version.

## Mise en page
1. **Aucune note encadrée** sur les folios (29/10). Les points à vérifier vont dans `05_POINTS_OUVERTS.md`.
2. **Contenu centré** dans le cadre de chaque folio (23/10, redemandé le 29/10 pour f22) : `g.centrer` automatique sur les folios 10 à 69.
3. **Aucun texte qui se superpose** (23/10) : textes, étiquettes de câble, renvois. Le bloc d'information d'un composant peut être déplacé indépendamment du symbole (`fpos`).
4. **Pastille d'état** en haut à droite de chaque folio (28/10) : vert = validé par Julien (tout le folio), orange = presque fini, rouge = moins de 50 %. Dictionnaire `STATUT` ; seul Julien passe un folio au vert.
5. **Rendu propre « comme un vrai schéma »** (29/10) : pas de longs fils qui font le tour du folio, pas de croisements inutiles. Appareils en parallèle : l'un sous l'autre (EL1 / EL2, EV1 / EV2 au f23). Les piquages d'un bus croisent les autres lignes du bus : normal.
6. Un folio trop chargé se **sépare en deux** (29/10 : f13 → alimentations + services). Un folio inutile se supprime.
7. **Fils assez longs** entre deux appareils (au moins 1600 à 2400) pour que le numéro de fil soit lisible (29/10, f22 / f23). Appareils d'une même chaîne **dans l'axe** (QF9 → QF10 → X14).
8. Arrivée réseau : texte « ARRIVEE RESEAU ... » **dans un cadre** (29/10, f20).

## Composants
9. Affichage : **fonction + caractéristiques** seulement. Marque et référence (champ 3) **masquées** sur tous les composants sauf les borniers (29/10) ; la donnée reste dans le symbole (nomenclature). Fait dans `_place_ren` (`shown=(2, 4)` par défaut).
10. Repérage : lettres de fonction + n° d'ordre, sens de l'énergie (28/10, `docs/NOMMAGE_2026-10-28.md`). Maître = référence fabricant ; esclaves = même repère, sans référence. Contacteur utilisé comme relais / contacteur auxiliaire = **KA** (KA2, 29/10), même si la référence est celle d'un contacteur moteur.

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
18. Numéros **alignés et centrés** (29/10, « carré et propre ») : noms des fils parallèles voisins sur une même ligne ; nom d'un bus près de son extrémité gauche, aligné sur les autres lignes du bus.
19. **Terre, règle C partout** (29/10) : pas de PE qui descend en bas du folio. Chaque appareil : **fil PE court + renvoi** vers la terre de l'arrivée (f20), où le PE de X11 se divise en un départ par appareil. Moteur : PE → X2 PE du variateur, puis X1 PE du variateur en renvoi court.
20. Types de conducteur : `Puissance` (phases), `Neutre Puissance`, `Conducteur terre` (PE), `Commande 24VDC`, `0V`, `Autre tension DC` (48 V, TF ; PROFINET provisoire). Jamais `Commande 24V~` sur un circuit continu.

## Textes
21. Phase de chaque départ 230 V : visible par le piquage sur le bus et le numéro de fil (les petits textes « L1 / L2 / L3 » du 23/10 sont retirés en v8).
22. Borniers f70 / f71 : provenance du fil écrite **des deux côtés** de la borne (23/10).
23. Folio PROFINET : texte sur chaque fil indiquant le composant de destination (23/10).
