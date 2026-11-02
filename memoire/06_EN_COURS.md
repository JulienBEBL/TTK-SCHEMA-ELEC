# 06 · Travail en cours (version actuelle et suite)

## Version actuelle : v11 (02/11/2026, après-midi)
`schema/generes/TTK_2026-11-02_v11.xrs` : 25 folios, 159 symboles, 628 fils, 94 renvois ; 0 problème au contrôle interne, 0 erreur au verifier (28 attentions connues), 0 chevauchement. **En attente : Q17 (plan de folios + repérage des borniers), puis retours sur la v11.**
La v10 réenregistrée par Julien est archivée (`schema/recus/2026-11-02_v10_ouverte_WinRelais.xrs`) : aucune différence de contenu.

### Fait en v11 — numéros affichés
| Folio | Changement |
|---|---|
| 20 | QS1 descendu de 800, QF1 de 2000, départs allongés ; peigne de terre en bas, 9 renvois à droite de la chaîne (flèches vers le haut) |
| 24 | Drivers remontés de 1200 ; bornier entre drivers et moteurs (X70.33 à X70.40), bornes en quinconce |
| 31, 32 | Nouveau symbole moteur de Julien ; bornier de 8 bornes (X70.17 à X70.32) entre variateur et moteur / TF / frein ; résistance décalée à droite |
| 41 | Barres 24 V / 0 V retirées (aucun piquage) |
| 53 | 2 bornes thermocouple X70.41 / X70.42 (type à définir), câble W8 remonté |

### Choix faits par l'assistant, à valider
- Numéros de bornes provisoires dans X70 (en attendant Q17).
- f31 : la borne du frein broche 3 part à droite directement (pas de croisement avec la broche 2).

## À faire ensuite
1. Q17 : appliquer le plan de folios et le repérage des borniers une fois validés (dict `NUMFOL` + renommage des bornes dans le script ; plans f70 / f71 à refaire).
2. Champs « câble blindé » et « afficher les numéros » dès réception du .xrs de test de Julien.
3. Type de conducteur PROFINET.
4. Liste d'E/S (f50 à f52) : seulement après validation de Julien.
5. f25 « borniers sur la page alims » : en pause (Julien, 02/11).
