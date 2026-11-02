# 06 · Travail en cours (version actuelle et suite)

## Version actuelle : v13 (02/11/2026, nuit)
`schema/generes/release/TTK_2026-11-02_v13.xrs` : 25 folios, 159 symboles, 631 fils, 93 renvois ; 0 problème au contrôle interne, 0 erreur au verifier (28 attentions connues), 0 chevauchement. **En attente : retours de Julien (Q8) et réponses Q21 à Q24.**
La v12 réenregistrée par Julien dans WinRelais est archivée (`schema/recus/2026-11-02_v12_ouverte_WinRelais.xrs`) ; ses 3 retouches ne sont pas reprises (Q21).

### Fait en v13 — numéros affichés
| Folio | Changement |
|---|---|
| tous | Couleurs revues selon IEC 60204-1 (table dans `04_REGLES_DESSIN.md`) : plus d'orange ; 48 V, phases pas-à-pas et résistance de freinage en noir ; thermocouple en vert |
| 11 | Neutre retiré (rien ne s'y pique) ; le N part de QF1 (f10) directement vers le f12 |
| 20 | Drivers remontés de 1600, bornes descendues de 400 ; un câble blindé par moteur pas-à-pas (W9, W10, « 4 cond. blindé ») |
| 31, 32 | Noms de broches du bloc moteur / TF / frein masqués ; sonde TF en 2x0,75 blindé ; fils du frein remontés avant de partir à droite (plus de superposition sur X31.32) ; compositions TF et frein à droite du câble (pas de place à gauche) |
| 40 | B2 du KA1 au 0 V ; texte « Réglage -KA1 : FUNCTION 1, START 3 » |

### Choix faits par l'assistant, à valider
- Fils du frein : broche 2 à y 12000 vers un renvoi décalé à droite, broche 3 à y 12400.
- 0 V 48 en noir comme le +48 V (puissance CC) : la polarité se lit par les renvois et les bornes.

## À faire ensuite
1. Q22 / Q23 : fusible en amont des contacts du KA1, Z1 → I1.5 (si Julien valide).
2. Champs « câble blindé » et « afficher les numéros » dès réception du .xrs de test de Julien.
3. Type de conducteur PROFINET.
4. Liste d'E/S (f60 à f62) : seulement après validation de Julien.
5. f21 « borniers sur la page alims » : en pause (Julien, 02/11).
