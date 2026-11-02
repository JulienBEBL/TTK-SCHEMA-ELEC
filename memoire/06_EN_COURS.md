# 06 · Travail en cours (version actuelle et suite)

## Version actuelle : v10 (02/11/2026)
`schema/generes/TTK_2026-11-02_v10.xrs` : 25 folios, 133 symboles, 606 fils, 96 renvois ; 0 problème au contrôle interne, 0 erreur au verifier (28 attentions connues), 0 chevauchement. **En attente des retours de Julien (Q8).**
La v9 réenregistrée par Julien est archivée : `schema/recus/2026-11-02_v9_ouverte_WinRelais.xrs` (TR1, U3, M3 sans noms de broches ; f21 descendu de 700 ; W1 et le texte « vers -X11 » retirés au f20 ; 4 notes : Q15).

### Fait en v10 (retours du 02/11) — numéros affichés
| Folio | Changement |
|---|---|
| 02 | Sommaire sans le f03 ; contrôlé : 25 lignes = 25 folios, même ordre, numéros croissants |
| 03 | Supprimé |
| 04 | Synoptique refait en logigramme (16 cadres, flèches, PROFINET en pointillés) ; note du bas supprimée |
| 20 | TR1 sans noms de broches ; texte « vers -X11 » retiré (comme dans le fichier de Julien) |
| 21 | Composants descendus de 800 (Julien : 700, hors grille du script) |
| 22 | Note « Présence tension » supprimée ; T3 sous QF6 ; 4 départs 48 V au-dessus des départs 24 V ; X36.1 et son PE en renvoi horizontal en bas |
| 24 | Borniers X34 / X35 supprimés ; 4 arrivées ; 2 x +48 V par KA2 (1-2 → U3, 3-4 → U4) ; U3, U4, M3, M4 sans noms de broches ; 1 croisement nouveau |

### Choix faits par l'assistant, à valider
- KA2 reste au f24 (les arrivées passent par lui avant les drivers).
- f22 : ordre des départs 48 V de haut en bas : +U4, +U3, 0 V U4, 0 V U3 (aucun croisement) ; 24 V descendus de 2800.
- W1 gardé au f20 (Q14).

## À faire ensuite
1. Réponses Q13 à Q16.
2. Câbler moteurs, freins et sondes TF par X70 aux f31 / f32 ; mettre à jour f70 et `MEMES`.
3. Champs « câble blindé » et « afficher les numéros » dès réception du .xrs de test de Julien.
4. Type de conducteur PROFINET.
5. Liste d'E/S (f50 à f52) : seulement après validation de Julien.
