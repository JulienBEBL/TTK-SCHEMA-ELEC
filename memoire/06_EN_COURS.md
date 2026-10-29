# 06 · Travail en cours (version actuelle et suite)

## Version actuelle : v7 (29/10/2026)
`schema/generes/TTK_2026-10-29_v7.xrs` : 28 folios, 137 symboles, 631 fils, 102 renvois ; 0 problème au contrôle interne, 0 erreur au verifier (26 attentions connues). **En attente des retours de Julien.**

### Fait en v7 (retours du 29/10)
| Folio | Changement |
|---|---|
| tous | Notes encadrées supprimées (11 zones) |
| 10 | PE dans le faisceau avec L1 L2 L3 N, renvoi vers X13 (option A) ; phases remises dans l'ordre (QF1 2 → barre L1, 6 → barre L3) ; description du cartouche sans « parafoudre » |
| 11 | 3 départs (11, 21, 31) vers le bus du f12, au lieu de 10 ; départ PE vers X14 (f14) |
| 12 | Bus L1 L2 L3 en haut du folio, piquages avec points de jonction |
| 13 | Devient « DISTRIBUTION 230 V - ALIMENTATIONS » : QF4, QF5, QF6, voyant H2 |
| 14 | Nouveau « DISTRIBUTION 230 V - SERVICES » : QF7, QF8 (Hager NFT702), QF9, QF10, X14, EL1 / EL2 sans croisement, EV1 / EV2 ; PE de X14 en renvoi court (option C) |
| 43 | Supprimé (contenu dans `03_ARCHITECTURE.md`) |
| 10 à 32 | Numéros de fil sur chaque tronçon de puissance : L1 L2 L3 N PE, U V W en sortie de variateur |
| 03, 20, 30, 31, 40, 60 | Potentiels renommés 24VSEC (T1) / 24VELEC (T2) |
| 32 | Description de X34 / X35 affichée sur le symbole |
| 02, 03 | Descriptions de cartouche corrigées |

### Choix faits par l'assistant, à valider
- Nom de T2 : **24VELEC** (Julien : « à toi de trouver »).
- N° de départ du répartiteur non affiché sur le bus du f12.
- Ordre des phases au f10 : L3 en haut, L1 en bas, PE tout en bas (seul ordre sans croisement avec les pôles de QF1).

## À faire ensuite (repris de la passation, §11)
1. Câbler moteurs, freins et sondes TF par X70 aux f20 / f21 ; mettre à jour f70 et `MEMES`.
2. Champs « câble blindé » et « afficher les numéros » dès réception du .xrs de test de Julien.
3. Type de conducteur PROFINET.
4. Liste d'E/S (f50 à f52) : seulement après validation de Julien.
5. PE en renvoi court sur f20, f21, f30, f32 si Julien le veut.
