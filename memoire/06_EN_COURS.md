# 06 · Travail en cours (version actuelle et suite)

## Version actuelle : v12 (02/11/2026, soir)
`schema/generes/release/TTK_2026-11-02_v12.xrs` : 25 folios, 159 symboles, 628 fils, 94 renvois ; 0 problème au contrôle interne, 0 erreur au verifier (28 attentions connues), 0 chevauchement. **En attente des retours de Julien (Q8).**
Rangement (02/11) : `schema/generes/release/` = la dernière version seule ; `schema/generes/old/` = toutes les précédentes.
La v11 réenregistrée par Julien est archivée (`schema/recus/2026-11-02_v11_ouverte_WinRelais.xrs`) : câbles du f32 replacés à la main, repris dans le script pour f31 et f32.

### Fait en v12 — numéros affichés v12
| Folio | Changement |
|---|---|
| tous | Nouveaux numéros par dizaines (table dans `04_REGLES_DESSIN.md`) ; sommaire et synoptique à jour |
| tous | Bornes renommées X + folio + n° par dizaine (ex. X31.11) ; prise X14 → XD1 ; X31 / X32 / X33 → X21.11 / X21.12 / X21.13 |
| 31, 32 | Câbles présentés comme Julien au f32 (ovale à gauche, composition dessous) ; numérotés moteur, TF, frein de gauche à droite |
| 70 | Groupes de bornes vers la machine et le réseau, avec leur repère (X31.11 à 14...) ; câbles 19G1 / 27G1 « à attribuer » |
| 71 | Tableau de toutes les bornes vers le pupitre (X41, X42, X50, X60), 23 bornes |

### Choix faits par l'assistant, à valider
- Découpage des dizaines (table `GROUPES` du script), par exemple X60.11-12 AU pupitre, X60.21-24 sélecteur, X60.31-38 fins de course.
- Frein : composition 2G1,5 gardée (Q20).

## À faire ensuite
1. Champs « câble blindé » et « afficher les numéros » dès réception du .xrs de test de Julien.
2. Type de conducteur PROFINET.
3. Liste d'E/S (f60 à f62) : seulement après validation de Julien.
4. f21 « borniers sur la page alims » : en pause (Julien, 02/11).
