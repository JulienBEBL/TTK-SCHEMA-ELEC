# 06 · Travail en cours (version actuelle et suite)

## Version actuelle : v15 (02/11/2026, nuit)
`schema/generes/release/TTK_2026-11-02_v15.xrs` : 25 folios, 165 symboles, 642 fils, 92 renvois ; 0 problème au contrôle interne, 0 erreur au verifier (28 attentions connues), 0 chevauchement. **En attente : retours de Julien (Q8), Q22 (fusible R-33), Q25 (contacts des AU).**
Pas de v14 publiée : ses changements (retouches v12, Z1) sont dans la v15. La v13 réenregistrée par Julien est archivée (`schema/recus/2026-11-02_v13_ouverte_WinRelais.xrs`) et ses retouches sont reprises.
But de Julien (02/11) : un schéma propre (borniers, sécurité, automate) **avant** la numérotation des fils.

### Fait en v15 — numéros affichés
| Folio | Changement |
|---|---|
| 10 | Cadre « ARRIVEE RESEAU » en pointillé ; étiquette « Distribution » placée comme Julien |
| 11 | Étiquettes VARIATEUR 1 / 2, FREIN M1 placées comme Julien |
| 20 | Bornes 800 sous les drivers, câbles W9 / W10 à mi-chemin bornes-moteurs, compositions à gauche de l'ovale |
| 30 | « Port 5 : réserve » placé comme Julien |
| 31, 32 | R1 / R2 décalées de 2000 à gauche ; compositions des câbles sous l'ovale comme Julien (moteur, TF, frein) |
| 40 | Bouton de réarmement S4 (déplacé du f41) au bout de la boucle Y1-Y2 ; Z1 → I1.5 ; texte de réglage descendu |
| 41 | AU armoire S1 par 4 bornes de porte (X41.51 à X41.54) ; chaîne descendue de 1600 ; tête de S3 placée comme Julien ; bornes X41.34 / X41.44 descendues de 400 |
| 42 | « 0 V STO X6 » placé comme Julien |
| 60 | Contact NO de S1 par 2 bornes (X60.41 / X60.42) ; I1.5 = diagnostic Z1 |
| 61, 62 | Repère K1 / K2 tout près du module ; tableaux remontés près des modules (comme Julien) |
| 63 | « AI1 à AI7 : réserve » placé comme Julien (v12) |

## À faire ensuite
1. Q22 : fusible gG ≤ 10 A en amont des contacts du KA1 (décision de Julien).
2. Q25 : contacts réels des AU.
3. f70 / f71 : les bornes de porte (X41.5x, X60.4x) n'y figurent pas (destination « porte ») : à ajouter si Julien le veut.
4. Champs « câble blindé » et « afficher les numéros » dès réception du .xrs de test de Julien ; type de conducteur PROFINET.
5. Liste d'E/S (f60 à f62) : seulement après validation de Julien. Numérotation des fils : après le schéma propre.
