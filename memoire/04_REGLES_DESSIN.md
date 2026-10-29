# 04 · Règles de dessin (demandes de Julien)

À appliquer sur **tous les folios**, à chaque version. Date = date de la demande.

## Mise en page
1. **Aucune note encadrée** sur les folios (29/10). Les points à vérifier vont dans `05_POINTS_OUVERTS.md`.
2. **Contenu centré** dans le cadre de chaque folio (23/10) : `g.centrer` automatique sur les folios 10 à 69.
3. **Aucun texte qui se superpose** (23/10) : textes, étiquettes de câble, renvois. Le bloc d'information d'un composant peut être déplacé indépendamment du symbole (`fpos`).
4. **Pastille d'état** en haut à droite de chaque folio (28/10) : vert = validé par Julien (tout le folio), orange = presque fini, rouge = moins de 50 %. Dictionnaire `STATUT` ; seul Julien passe un folio au vert.
5. **Rendu propre « comme un vrai schéma »** (29/10) : pas de longs fils qui font le tour du folio, pas de croisements inutiles (ex. EL1 / EL2 au f13).
6. Un folio trop chargé se **sépare en deux** (29/10, ex. f13).

## Composants
7. Contacteurs moteurs (et appareils de puissance) : 3 lignes d'information = **fonction**, **marque + référence**, **caractéristiques** (23/10).
8. Repérage : lettres de fonction + n° d'ordre, sens de l'énergie (28/10, `docs/NOMMAGE_2026-10-28.md`). Maître = référence fabricant ; esclaves = même repère, sans référence.

## Renvois
9. Le texte de description d'un renvoi est **bien placé** (centré sur le renvoi ou le groupe de renvois) (23/10).
10. Le renvoi ne doit **jamais** être dessiné sur le fil : flèche du côté opposé au fil (codes A/B, voir `07_METHODE_TRAVAIL.md`).
11. Renvois de la terre : même règle (23/10).
12. Distribution de puissance (29/10, f12) : Julien préfère **tirer un bus tri / tétra** (L1 L2 L3 [N]) et y piquer les phases utiles, plutôt qu'une série de renvois au-dessus des appareils. Modalités à discuter (voir `06_V7_A_FAIRE.md`).

## Fils
13. **Numéros de fil** : les fils de puissance portent le nom de leur potentiel, **L1, L2, L3, N, PE**, sans différenciation (28/10, précisé le 29/10 : PE compris, et sur tous les folios de puissance f10 à f13). Les autres fils ne sont pas numérotés tant que le schéma n'est pas fini.
14. Distribution TBT : **un fil par appareil** depuis le bornier de distribution, sans point de dérivation (28/10, f32). Croisement sans jonction accepté.
15. Terre : le PE qui part en bas du folio et le traverse « fait moche » (29/10, f10 et f13). Représentation à arrêter (voir `06_V7_A_FAIRE.md`).
16. Types de conducteur : `Puissance` (phases), `Neutre Puissance`, `Conducteur terre` (PE), `Commande 24VDC`, `0V`, `Autre tension DC` (48 V, TF ; PROFINET provisoire). Jamais `Commande 24V~` sur un circuit continu.

## Textes
17. Au f13, petit texte indiquant la phase utilisée (L1, L2 ou L3) par chaque départ 230 V (23/10).
18. Borniers f70 / f71 : provenance du fil écrite **des deux côtés** de la borne (23/10).
19. Folio PROFINET : texte sur chaque fil indiquant le composant de destination (23/10).
