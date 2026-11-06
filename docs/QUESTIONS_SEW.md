# Questions à poser à SEW (05/11/2026)

Matériel : 2 motoréducteurs SEW K39 DRN100LS4 / BE5 / TF (2,2 kW, frein BE5 400 V CA, sonde TF), 2 variateurs MOVITRAC MCX91A-0055-5E3 (options CSO = STO, CFN = PROFINET).
Câblage prévu : réseau coupé par un contacteur KM1 / KM2 en amont de chaque variateur ; STO X6 commandé par le relais de sécurité ; frein alimenté en 400 V CA par un contacteur KF1 / KF2 ; sonde TF sur X10.

| N° | Question | Pourquoi |
|---|---|---|
| 1 | Les sondes TF sont-elles montées sur les moteurs livrés ? Bornes dans la boîte à bornes ? **06/11 : SEW n'a pas l'information** (à voir à la réception, plaque et boîte à bornes) | Le câble TF 2x0,75 blindé (W3 / W6) et les bornes X31.2x / X32.2x sont prévus |
| 2 | Bornes exactes de la sonde sur le MCX91A (X10) et paramétrage ; que faire à X10 si pas de sonde (pont, paramètre) ? | Texte « TF X10 : bornes à confirmer » encore au schéma (f31 / f32) |
| 3 | Courant consommé par les entrées STO X6.1 / X6.3 d'un MCX91A | Les 2 variateurs sont en parallèle sur un contact du relais KA1, qui demande au moins 10 mA (et 15 V) |
| 4 | Frein BE5 400 V CA : courant d'appel et de maintien, redresseur fourni (type, emplacement) ? | Calibre et courbe des disjoncteurs QF2 / QF3 ; section du câble frein (5G1,5) |
| 5 | Frein alimenté en permanence alors que le moteur est à l'arrêt et non alimenté (mode Manu : arbre tourné à la clé pour la maintenance) : admissible ? **06/11 : OUI** | Choix de Julien : moteurs libres en Manu |
| 6 | Nombre maximal de mises sous tension par heure du MCX91A **06/11 : « 1 » (réponse relayée par Julien), unité à confirmer : par heure ou par minute ?** | KM1 / KM2 coupent le réseau du variateur à chaque arrêt d'urgence |
| 7 | Longueur maximale de câble moteur blindé sans self ni filtre ; reprise du blindage conseillée | Câble 2XSLCY-K 4G2,5, environ 15 m par moteur |
| 8 | Consommation de l'électronique 24 V (X5) d'un MCX91A-0055-5E3 avec CSO et CFN | Bilan 24VELEC (`docs/BILAN_24V.md`) ; la page SEW « Power consumption of the 24 V supply » n'est pas lisible en ligne |
| 9 | STO en chaîne : 24 V et 0 V sur X6.1 / X6.2 de U1, puis X6.3 / X6.4 de U1 vers X6.1 / X6.2 de U2 : **validé par SEW (Julien, 06/11)** | Câblage dessiné en v23 |

Réponses à reporter dans `memoire/05_POINTS_OUVERTS.md` (points 1 bis, 8 à 11, Q37) et `docs/DECISIONS.md`.
