# 06 · Travail en cours (version actuelle et suite)

## Version actuelle : v13 (02/11/2026, nuit)
`schema/generes/release/TTK_2026-11-02_v13.xrs` : 25 folios, 159 symboles, 631 fils, 93 renvois ; 0 problème au contrôle interne, 0 erreur au verifier (28 attentions connues), 0 chevauchement. **Julien ouvre la v13 dans WinRelais (02/11 nuit) : ne rien modifier au schéma avant son retour.** Avant la v14 : `git status` (WinRelais réenregistre la release), archiver dans `schema/recus/` si modifiée.
La v12 réenregistrée par Julien dans WinRelais est archivée (`schema/recus/2026-11-02_v12_ouverte_WinRelais.xrs`) ; ses 3 retouches sont à reprendre en v14 (Q21).

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
1. **v14, validé par Julien le 02/11, après son retour sur la v13** : reprendre ses retouches de la v12 (R1 à gauche de 2000 au f31 **et** au f32, étiquette « Distribution » du f10, texte « AI1 à AI7 » du f63) ; câbler Z1 → I1.5. Q22 (fusible R-33) : attendre sa décision.
2. Champs « câble blindé » et « afficher les numéros » dès réception du .xrs de test de Julien.
3. Type de conducteur PROFINET.
4. Liste d'E/S (f60 à f62) : seulement après validation de Julien.
5. f21 « borniers sur la page alims » : en pause (Julien, 02/11).
