# Proposition du 02/11/2026 : numéros de folio et repérage des borniers

**Statut : appliqué en v12 (02/11), avec une correction de Julien : un seul point dans le repère (X31.11, pas X31.1.1), une dizaine par fonction. La règle à jour est dans `memoire/04_REGLES_DESSIN.md`.**
Les deux vont ensemble : le repère d'un bornier contient le numéro de son folio. Il faut donc figer les folios d'abord.

## 1. Numéros de folio

Pratique courante (la norme IEC 61082 n'impose pas de numérotation) :
- une **dizaine par famille de fonctions** ;
- des numéros **qui se suivent** dans une famille ;
- des **trous entre familles** pour ajouter des folios sans tout renuméroter.

Pourquoi il n'y a pas de f10 aujourd'hui : la sécurité était en 10-12 en v8. Elle est retournée en 40-42 en v9, et les alimentations ont gardé 20-25.

| Nouveau | Actuel (v11) | Contenu |
|---|---|---|
| 01 | 01 | Page de garde |
| 02 | 02 | Sommaire |
| 03 | 04 | Synoptique (logigramme) |
| **10** | 20 | Arrivée réseau, QS1, QF1, terre |
| 11 | 21 | Distribution 400 V (variateurs, freins) |
| 12 | 22 | 230 V alimentations : T1, T2, T3, H2, PELV |
| 13 | 23 | 230 V services : ventilation, éclairage, prise |
| **20** | 24 | 48 V : KA2, drivers, moteurs pas-à-pas |
| 21 | 25 | Distribution 24 V |
| **30** | 30 | Switch PROFINET |
| 31 | 31 | Variateur U1 / moteur M1 |
| 32 | 32 | Variateur U2 / moteur M2 |
| **40** | 40 | Sécurité : relais KA1 |
| 41 | 41 | Sécurité : entrées |
| 42 | 42 | Sécurité : sorties |
| **50** | 45 | Pupitre (IHM) |
| **60** | 50 | Automate : CPU, alimentation et entrées |
| 61 | 51 | Automate : sorties |
| 62 | 52 | Module SM 1223 |
| 63 | 53 | Module SM 1231 TC |
| **70** | 70, 71 | Plans de borniers (un folio par groupe de borniers si besoin) |
| **80** | 80 | Liste des câbles |
| 85 | 85 | Implantation armoire |
| **90** | 90 | Nomenclature |

## 2. Repérage des borniers : X + folio + groupe + borne

Logique de Julien : `X<folio>.<groupe>.<borne>`, par exemple X10.1.1, X10.1.2, etc.
Le groupe correspond à une destination ou à un câble sur ce folio. Voici le résultat avec les nouveaux numéros de folio :

| Folio | Actuel | Proposé | Groupe |
|---|---|---|---|
| 10 | X11.VJ, X11.1 à X11.4 | X10.1.1 à X10.1.5 (PE, N, L1, L2, L3) | arrivée réseau |
| 12 | X36.1 | X12.1.1 | liaison PELV 0 V - PE |
| 20 | X70.33 à X70.36 | X20.1.1 à X20.1.4 | moteur M3 |
| 20 | X70.37 à X70.40 | X20.2.1 à X20.2.4 | moteur M4 |
| 21 | X31, X32, X33 (PTFIX) | X21.1, X21.2, X21.3 (points .1 à .6) | 24VELEC, 0 V, 24VSEC |
| 31 | X70.17 à X70.20 | X31.1.1 à X31.1.4 | moteur M1 (PE, U, V, W) |
| 31 | X70.21, X70.22 | X31.2.1, X31.2.2 | sonde TF M1 |
| 31 | X70.23, X70.24 | X31.3.1, X31.3.2 | frein M1 |
| 32 | X70.25 à X70.32 | X32.1.x, X32.2.x, X32.3.x | même découpage pour M2 |
| 41 | X71.1 à X71.4, X71.13 à X71.16 | X41.1.1 à X41.1.8 | vers pupitre +P1 |
| 41 | X70.1 à X70.8 | X41.2.1 à X41.2.8 | vers machine +M (capots) |
| 42 | X71.7 à X71.10, X71.19, X71.20 | X42.1.1 à X42.1.6 | vers pupitre +P1 (sélecteur) |
| 50 | X71.21 à X71.23 | X50.1.1 à X50.1.3 | alimentation IHM |
| 60 | X71.5, .6, .11, .12, .17, .18 | X60.1.1 à X60.1.6 | vers pupitre +P1 |
| 60 | X70.9 à X70.16 | X60.2.1 à X60.2.8 | vers machine +M (fins de course) |
| 63 | X70.41, X70.42 | X63.1.1, X63.1.2 | thermocouple B7 |

Prise de service X14 : ce n'est pas un bornier. Selon IEC 81346-2, une prise est repérée **XD**. Proposition : -XD1.

## 3. Avis de l'assistant (contestation unique, Julien décide)

- **Repère lié au folio** : si un folio change de numéro, le repère de bornier change aussi. Cela touche les repères imprimés sur les fils. Il faut donc figer le plan de folios avant de renommer.
- **Un bornier physique devient plusieurs** : X70 « machine » est aujourd'hui un seul rail. Il serait éclaté en X31.1, X31.2, X41.2, X60.2, etc. C'est possible, mais les repères sont plus longs (X31.1.1) et les borniers plus nombreux.
- **Alternative IEC 81346** : un bornier par fonction ou par destination (-X1 puissance, -X2 24 V, -X3 machine, -X4 pupitre), borne notée -X3:12. Le repère ne dépend pas du folio, et la référence croisée de WinRelais donne le folio.
- **Test WinRelais nécessaire** : deux points dans le repère (X10.1.1). Il faut vérifier que « Générer bornier » voit bien le bornier X10.1 et la borne 1, et non X10 et la borne 1.1. Ce test est à faire avant le renommage.
