# 04 · Règles de dessin (demandes de Julien)

À appliquer sur **tous les folios**, à chaque version. Date = date de la demande.

## Mise en page
1. **Aucune note encadrée** sur les folios (29/10). Les points à vérifier vont dans `05_POINTS_OUVERTS.md`.
2. **Contenu centré** dans le cadre de chaque folio (23/10) : `g.centrer` automatique sur les folios 10 à 69.
3. **Aucun texte qui se superpose** (23/10) : textes, étiquettes de câble, renvois. Le bloc d'information d'un composant peut être déplacé indépendamment du symbole (`fpos`).
4. **Pastille d'état** en haut à droite de chaque folio (28/10) : vert = validé par Julien (tout le folio), orange = presque fini, rouge = moins de 50 %. Dictionnaire `STATUT` ; seul Julien passe un folio au vert.
5. **Rendu propre « comme un vrai schéma »** (29/10) : pas de longs fils qui font le tour du folio, pas de croisements inutiles. Ex. EL1 / EL2 (f14) : lampes l'une sous l'autre, N à gauche, L à droite. Limite : deux appareils en parallèle dont les bornes N et L sont toutes les deux en haut (ventilateurs EV1 / EV2) gardent un croisement, sauf détour. Les piquages d'un bus croisent les autres lignes du bus : normal.
6. Un folio trop chargé se **sépare en deux** (29/10 : f13 → f13 alimentations + f14 services). Un folio inutile se supprime (f43 supprimé le 29/10, son contenu est dans `03_ARCHITECTURE.md`).

## Composants
7. Contacteurs moteurs (et appareils de puissance) : 3 lignes d'information = **fonction**, **marque + référence**, **caractéristiques** (23/10).
8. Repérage : lettres de fonction + n° d'ordre, sens de l'énergie (28/10, `docs/NOMMAGE_2026-10-28.md`). Maître = référence fabricant ; esclaves = même repère, sans référence.

## Renvois
9. Le texte de description d'un renvoi est **bien placé** (centré sur le renvoi ou le groupe de renvois) (23/10).
10. Le renvoi ne doit **jamais** être dessiné sur le fil : flèche du côté opposé au fil (codes A/B, voir `07_METHODE_TRAVAIL.md`).
11. Renvois de la terre : même règle (23/10).
12. Distribution de puissance (29/10, f12) : **bus tri / tétra** (L1 L2 L3 [N]) avec piquages et points de jonction, plutôt qu'une série de renvois au-dessus des appareils [D]. Les points de jonction sont acceptés sur un bus (il représente des barres) ; ailleurs, la règle 14 s'applique. Le n° de départ du répartiteur n'est pas affiché (départs équivalents par phase) [H].

## Fils
13. **Numéros de fil** : les fils de puissance portent le nom de leur potentiel, **L1, L2, L3, N, PE** (et U, V, W en sortie de variateur), sans différenciation, sur **chaque tronçon**, même court (28/10, précisé le 29/10). PE nommé sur les folios 10 à 32 (pas les FE de l'automate / IHM). Les autres fils ne sont pas numérotés tant que le schéma n'est pas fini.
14. Distribution TBT : **un fil par appareil** depuis le bornier de distribution, sans point de dérivation (28/10, f32). Croisement sans jonction accepté.
15. **Terre** (29/10) : plus de PE qui descend en bas du folio et le traverse. Arrivée (f10) : **PE dans le faisceau**, 5e conducteur avec L1 L2 L3 N, renvoi vers X13 à côté des autres [D]. Appareil (f14, X14) : **fil PE court + renvoi** « PE » vers X13 (f11) [D]. Les f20, f21, f30, f32 gardent encore le rail PE du bas (à passer en renvoi court si Julien le demande).
16. Types de conducteur : `Puissance` (phases), `Neutre Puissance`, `Conducteur terre` (PE), `Commande 24VDC`, `0V`, `Autre tension DC` (48 V, TF ; PROFINET provisoire). Jamais `Commande 24V~` sur un circuit continu.

## Noms des potentiels
20. **24VSEC** (T1, X33) et **24VELEC** (T2, X31), 0 V, +48 V / 0 V 48 (29/10).

## Textes
17. Au f13, petit texte indiquant la phase utilisée (L1, L2 ou L3) par chaque départ 230 V (23/10).
18. Borniers f70 / f71 : provenance du fil écrite **des deux côtés** de la borne (23/10).
19. Folio PROFINET : texte sur chaque fil indiquant le composant de destination (23/10).
