# 06 · Travail en cours (version actuelle et suite)

## Version actuelle : v8 (29/10/2026, soir)
`schema/generes/TTK_2026-10-29_v8.xrs` : 26 folios, 135 symboles, 614 fils, 94 renvois ; 0 problème au contrôle interne, 0 erreur au verifier (28 attentions connues : fils en attente de l'arrivée réseau et de la variante USA, début de la barre 24 V au f10, références croisées à lancer dans WinRelais). **En attente des retours de Julien (Q8).**
La v7 réenregistrée par Julien (TR1 déplacé, numéros alignés au f11) est archivée : `schema/recus/2026-10-29_v7_ouverte_WinRelais.xrs` ; le déplacement de TR1 est repris dans le script.

### Fait en v8 (retours du 29/10 soir) — numéros affichés
| Folio | Changement |
|---|---|
| tous | Nouvel ordre et nouveaux numéros (table dans `04_REGLES_DESSIN.md`) ; marque et référence masquées (sauf borniers) ; numéros de fil centrés et alignés ; terre en fil court + renvoi partout |
| 01 | Lignes « Commande » et « Puissance installée » supprimées |
| 03 | Seul le tableau des conducteurs reste |
| 04 | Synoptique remis dans le nouvel ordre |
| 10 à 12 | Sécurité en tête ; barres 24VELEC / 0 V en haut ; bobines du f12 sur un collecteur 0 V remonté à gauche |
| 20 | Texte d'arrivée dans un cadre ; QF1 → renvois directs vers le bus (plus de répartiteur dessiné) ; PE dans le faisceau puis un départ par appareil ; phases L1 L2 L3 dans l'ordre naturel |
| 21 | Bus tétra L1 L2 L3 N, renvoyé vers f22 |
| 22 | Ancien f13 + ancien f30 : QF4 / QF5 → T1 / T2 sous le disjoncteur, QF6 → 48 V, H2, X36.1 ; sorties 24 V vers f25 |
| 23 | QF9 → QF10 → X14 dans l'axe, fils allongés ; EV1 / EV2 l'un sous l'autre (0 croisement) |
| 24 | 48 V descendant : T3 → KA2 (ex KM3, pôle 1-2) → X34 / X35 → drivers ; 2 croisements |
| 25 | Distribution 24 V sous les barres du haut ; X31 et X32 piqués dessus |
| 30 | Switch avant les variateurs |
| 31, 32 | PE moteur → X2 PE ; X1 PE en renvoi court ; plus de PE en bas |
| 40, 50 à 53 | Barres 24VELEC / 0 V en haut |
| 11 (ancien), 30 (ancien) | Supprimés |

### Choix faits par l'assistant, à valider
- Bloc sécurité : entrées (AU) en f10, relais en f11, sorties en f12 (« AU » en tête de la liste de Julien).
- KM3 → **KA2** (contacteur auxiliaire), pôle 1-2 au lieu de 5-6 (place pour le 0 V à gauche).
- Petits textes de phase (« L1 », « L2 », « L3 ») retirés : la phase se lit sur le bus et le numéro de fil.
- f24 : X35 (0 V 48) à droite de X34, pour n'avoir que 2 croisements.

## À faire ensuite
1. Câbler moteurs, freins et sondes TF par X70 aux f31 / f32 ; mettre à jour f70 et `MEMES`.
2. Champs « câble blindé » et « afficher les numéros » dès réception du .xrs de test de Julien.
3. Type de conducteur PROFINET.
4. Liste d'E/S (f50 à f52) : seulement après validation de Julien.
