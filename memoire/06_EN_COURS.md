# 06 · Travail en cours (version actuelle et suite)

## Version actuelle : v16 (04/11/2026)
`schema/generes/release/TTK_2026-11-04_v16.xrs` : 25 folios, 165 symboles, 640 fils, 91 renvois ; 0 problème au contrôle interne, 0 erreur au verifier (27 attentions connues), 0 chevauchement. **En attente : retours de Julien (Q8).**
La v15 n'a pas été réenregistrée par WinRelais (rien à reprendre). But de Julien : un schéma propre (borniers, sécurité, automate) **avant** la numérotation des fils.

### Fait en v16 — décisions du 03/11 (revue des achats)
| Folio | Changement |
|---|---|
| 40 | Fusible **FA1** (Mersen CMC101 + FR10GG50V4 gG 4 A) entre le 24VSEC et le départ commun 13 / 23 / 33 de KA1 ; S4 = XB4BA21 non lumineux (symbole BP affleurant noir, référence XB4BA21) |
| 61 | Voyant de S4 retiré |
| 62 | Q8.3 en réserve (sortie libre, tableau à jour) |
| 31, 32 | Câble frein W3 / W6 : « 5G1,5 blindé » (LIYCY-JZ de réserve), texte décalé à gauche pour ne pas couper le 1er brin |
| 10, 31, 32, 50 | Bornes de terre vert/jaune : X10.11, X31.11, X32.11, X50.13 |

Positions de Julien (POS_JULIEN, tableaux f61 / f62) vérifiées par calcul : inchangées.

## Prêt pour la v17 (script modifié, pas encore généré)
- f31 / f32 : texte rouge réduit à « TF X10 : bornes à confirmer » (X6 confirmé le 05/11).
- En attente de Julien : répartition 27G1 / 19G1 (Q32) ; si validée, bornes de la colonne H1 (X61.11-14) et repères -W11 / -W12 au f70.

## À faire ensuite
1. H2 : reporter la référence du voyant 230 V quand Julien l'aura.
2. f70 / f71 : les bornes de porte (X41.5x, X60.4x) n'y figurent pas (destination « porte ») : à ajouter si Julien le veut.
3. Champs « câble blindé » et « afficher les numéros » dès réception du .xrs de test de Julien ; type de conducteur PROFINET.
4. Liste d'E/S (f60 à f62) : seulement après validation de Julien. Numérotation des fils : après le schéma propre.
5. Achats : Q28 à Q30 (raccord thermocouple, fixation sonde, câble moteur 50 m).
