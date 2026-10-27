# Méthode borniers – projet TTK (WinRelais 2.6b)

Objectif : faire les folios de bornier vite et sans oubli, que le matériel soit déjà là ou pas.
Principe : **le bornier se déduit du schéma, il ne se dessine pas**. On décide une fois pour toutes
quelles liaisons sortent de l'armoire, on pose une borne sur chacune dans le schéma, et WinRelais
génère le folio de bornier à la fin.

## 1. Avant de dessiner : la liste des sorties d'armoire (15 min, une fois)

Pour chaque appareil **hors armoire** (moteur, capteur, AU, pupitre, lampe…), noter :

| Appareil | Où (+M machine / +P1 pupitre) | Nb de conducteurs | Câble | Bornier |
|---|---|---|---|---|

Règles TTK retenues :

1. **Un bornier par destination** : X701 = armoire ↔ machine (+M), X711 = armoire ↔ pupitre (+P1).
   Les puissances déjà sur bornier dédié restent à part (X101 arrivée, X131 230 V, X31x 24 V).
2. **Une borne par conducteur qui sort** (pas de borne pour un fil qui reste dans l'armoire).
3. **Bornes regroupées par appareil, dans l'ordre du câble** : toutes les bornes d'un même câble se
   suivent (ex. X701.17-.20 = M201 frein + TF, câble W202). On laisse 1-2 bornes de réserve entre
   groupes si on pense ajouter du matériel.
4. **PE** : sur borne de terre (X112 / borne PE du bornier), pas mélangé avec les bornes « signal ».
5. **Moteurs SEW** : câble moteur blindé (W201 / W211), câble frein + TF blindé (W202 / W212) ;
   blindage repris à 360° au presse-étoupe CEM ou sur l'étrier de reprise de blindage, **pas sur une
   borne**.
6. Sens de la borne sur le schéma : **côté armoire en haut, côté terrain en bas** (c'est ce que
   WinRelais lit pour remplir « intérieur / extérieur » du bornier généré).

## 2. Pendant le dessin du schéma

- Poser le symbole borne (bibliothèque `Borne`) **sur le fil**, repère `X701.n`. Le repère complet
  (bornier.numéro) suffit : WinRelais regroupe tout seul les `X701.*`.
- Numéroter dans l'ordre du câble, appareil par appareil (voir tableau ci-dessous).
- Un même potentiel distribué à plusieurs capteurs (ex. +24 V capteurs) = **une borne par capteur**
  (on raccorde un câble par borne), pas une borne commune avec 4 fils dessous.

## 3. Quand le schéma est fini : générer le folio de bornier

1. Insérer un folio vide après le dernier folio (f70 pour X701, f71 pour X711).
2. Menu **Optimisation / Générer / Bornier**, onglet **Automatique**.
3. Choisir le bornier à extraire (X701), cocher « folio visible ».
4. Cocher **Matériel connecté via un bornier** + **Pré-remplissage** ; filtre des appareils
   terrain : `B,M,S412,S413,P601` (ce qui est dehors).
5. Valider : WinRelais dessine les bornes avec, au-dessus, ce qui part vers l'armoire et, en dessous,
   ce qui part vers le terrain.
6. Contrôler avec le tableau ci-dessous (f70 / f71 du fichier `test_xrs_claude.xrs` contient déjà
   ce tableau de contrôle) : chaque ligne doit se retrouver.
7. **Regénérer** le bornier après chaque modification du schéma (il n'est pas mis à jour tout seul).

## 4. Avec le matériel réel (câblage / vérification en atelier)

- Imprimer le folio de bornier + le tableau ci-dessous, un surligneur par câble.
- Câbler **câble par câble** (pas borne par borne) : on prend W202, on fait X701.17 à .20, on
  surligne, câble suivant.
- Étiqueter le câble aux deux bouts avec son repère (W202) et chaque conducteur avec le numéro de
  borne.
- Toute modification faite en atelier est reportée **dans le schéma** (borne déplacée, réserve
  utilisée), puis bornier regénéré : le folio de bornier ne doit jamais être modifié à la main.

## 5. Plan des bornes actuel (calculé depuis `test_xrs_claude.xrs`)

« (fNN) » = folio où se trouve la broche. Une borne qui ne va qu'à une autre borne (ex. X701.1 ↔
X711.2, chaîne AU) est indiquée par le repère de cette borne.

### X701
| Borne | Côté armoire (haut) | Côté terrain (bas) |
|---|---|---|
| 1 | -X711:2 (f41) | -B411:11 (f41) |
| 2 | -K401:S12 (f40) | -B411:12 (f41) |
| 3 | -K501:L+ capt (f50), -S411:13 (f50) | -B411:23 (f41) |
| 4 | -K501:I0.2 (f50) | -B411:24 (f41) |
| 5 | -X711:4 (f41) | -B412:11 (f41) |
| 6 | -K401:S22 (f40) | -B412:12 (f41) |
| 7 | -K501:L+ capt (f50), -S411:13 (f50) | -B412:23 (f41) |
| 8 | -K501:I0.3 (f50) | -B412:24 (f41) |
| 9 | -K501:L+ capt (f50), -S411:13 (f50) | -B501:13 (f50) |
| 10 | -K501:I1.0 (f50) | -B501:14 (f50) |
| 11 | -K501:L+ capt (f50), -S411:13 (f50) | -B502:13 (f50) |
| 12 | -K501:I1.1 (f50) | -B502:14 (f50) |
| 13 | -K501:L+ capt (f50), -S411:13 (f50) | -B503:13 (f50) |
| 14 | -K501:I1.2 (f50) | -B503:14 (f50) |
| 15 | -K501:L+ capt (f50), -S411:13 (f50) | -B504:13 (f50) |
| 16 | -K501:I1.3 (f50) | -B504:14 (f50) |
| 17 | -Q421:4/T2 (f12) | -M201:2 (f20) |
| 18 | -Q421:6/T3 (f12) | -M201:3 (f20) |
| 19 | -T201:X10:1 (f20) | -M201:1b (f20) |
| 20 | -T201:X10:2 (f20) | -M201:2b (f20) |
| 21 | -Q422:4/T2 (f12) | -M211:2 (f21) |
| 22 | -Q422:6/T3 (f12) | -M211:3 (f21) |
| 23 | -T211:X10:1 (f21) | -M211:1b (f21) |
| 24 | -T211:X10:2 (f21) | -M211:2b (f21) |

### X711
| Borne | Côté armoire (haut) | Côté terrain (bas) |
|---|---|---|
| 1 | -S411:2 (f41) | -S412:1 (f41) |
| 2 | -X701:1 (f41) | -S412:2 (f41) |
| 3 | -S411:22 (f41) | -S412:21 (f41) |
| 4 | -X701:5 (f41) | -S412:22 (f41) |
| 5 | -K501:L+ capt (f50), -S411:13 (f50) | -S412:13 (f50) |
| 6 | -K501:I0.1 (f50) | -S412:14 (f50) |
| 7 | -K401:14 (f40) | -S413:13 (f42) |
| 8 | -T201:X6:1 (f20), -T211:X6:1 (f21) | -S413:14 (f42) |
| 9 | -K401:24 (f40) | -S413:23 (f42) |
| 10 | -T201:X6:3 (f20), -T211:X6:3 (f21) | -S413:24 (f42) |
| 11 | -K401:34 (f40) | -S413:33 (f42) |
| 12 | -K501:3L+ (f51), -K521:3L+ (f52) | -S413:34 (f42) |
| 13 | -K501:L+ capt (f50), -S411:13 (f50) | -S413:43 (f50) |
| 14 | -K501:I0.4 (f50) | -S413:44 (f50) |
| 15 | -K501:L+ capt (f50), -S411:13 (f50) | -S413:53 (f50) |
| 16 | -K501:I0.5 (f50) | -S413:54 (f50) |
| 17 | -K401:13 (f40), -K401:23 (f40), -K401:33 (f40) ... | -P601:L+ (f60) |
| 18 | -K401:A2 (f40), -K501:1M (f50), -K501:3M (f51) ... | -P601:M (f60) |
| 19 | -F101:PE (f10), -K501:FE (f50), -M201:PE (f20) ... | -P601:FE (f60) |

À valider par Julien : le regroupement X701 (1-8 = interrupteurs de capot B411 / B412, 9-16 = capteurs
B501-B504 — repères provisoires, absents de ton tableau —, 17-24 = freins + TF des moteurs M201 / M211)
et X711 (1-6 = AU pupitre S412, 7-16 = sélecteur Auto/Manu S413, 17-19 = alimentation pupitre P601).
