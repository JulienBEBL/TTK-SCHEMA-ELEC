# 06 · Travail en cours (version actuelle et suite)

## Version actuelle : v9 (30/10/2026)
`schema/generes/TTK_2026-10-30_v9.xrs` : 26 folios, 135 symboles, 600 fils, 94 renvois ; 0 problème au contrôle interne, 0 erreur au verifier (28 attentions connues), 0 chevauchement (`xrs_chevauchements.py`). **En attente des retours de Julien (Q8).**
La v8 réenregistrée par Julien est archivée : `schema/recus/2026-10-30_v8_ouverte_WinRelais.xrs` ; ses retouches sont reprises dans le script (f50, f51, U3).

### Fait en v9 (retours du 30/10) — numéros affichés
| Folio | Changement |
|---|---|
| tous | Carré de couleur supprimé |
| 40 à 42 | Sécurité remise à sa place (ancien 10 à 12) ; IHM passe de 40 à **45** |
| 20 | Numéros de fil écartés des numéros de brin du câble W1 |
| 21, 22, 23 | Bus en haut, à la même hauteur (y = 2400), modèle f22 |
| 23 | Lampes et ventilateurs écartés (4400 au lieu de 2000 / 2400) ; colonnes écartées |
| 24 | U3 sans noms de broches, U4 avec (test de Julien) ; 0 V 48 descendu de 400 (il coupait le texte de KA2) |
| 31, 32 | Variateur remonté de 800 ; moteur dans l'axe de X2 ; 3 câbles sur une ligne ; frein sans croisement ; textes séparés |
| 50 | Alignement de Julien repris (règle dans `04_REGLES_DESSIN.md`) ; S1 et S2 alignés aussi |
| 50, 51 | Mention « PROPOSITION A VALIDER » retirée (fait par Julien) |
| 51 | PUL sur 100 kHz : Q0.0 U3, Q0.2 U4 ; DIR Q0.1 / Q0.3 ; ENA Q0.4 / Q0.5 |
| 25, 30, 40 à 42, 45, 50 à 53 | Barres 24 V / 0 V à la même hauteur partout (y = 2000 / 2800) |

### Choix faits par l'assistant, à valider
- IHM numérotée f45 (entre la sécurité et l'automate), les alimentations gardent 20 à 25 : il n'y a plus de folio de 05 à 19.
- f31 / f32 : l'image n'est pas arrivée, le défaut a été cherché par calcul. Sonde TF : 1 croisement imposé par 1b → X10:1 et 2b → X10:2.
- f51 : la paire impulsion + direction est groupée (Q0.0 / Q0.1, Q0.2 / Q0.3) ; à vérifier dans TIA.

## À faire ensuite
1. Câbler moteurs, freins et sondes TF par X70 aux f31 / f32 ; mettre à jour f70 et `MEMES`.
2. Champs « câble blindé » et « afficher les numéros » dès réception du .xrs de test de Julien.
3. Type de conducteur PROFINET.
4. Liste d'E/S (f50 à f52) : seulement après validation de Julien.
5. Appliquer la disposition du f50 aux autres folios d'E/S si Julien le demande.
