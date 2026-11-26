# Questions à poser à SEW (mise à jour du 24/11/2026)

Interlocuteurs chez SEW-USOCOME : **Xavier** et **Franck Strugareck**, deux personnes différentes (confirmé par Julien le 25/11). Mail du 24/11 envoyé à Xavier. Qui suit quel sujet : [?].

Matériel : 2 motoréducteurs SEW K39 DRN100LS4 / BE5 / TF (2,2 kW, frein BE5 400 V CA, redresseur BGE1.5 d'après la plaque du 18/11, sonde TF), 2 variateurs MOVITRAC MCX91A-0055-5E3-4-T00/001/CSO/CFN/CDM/CMM, 2 résistances BW100-001.
Câblage : réseau coupé par KM1 / KM2 en amont de chaque variateur ; STO X6 commandé par le relais de sécurité KA1 (33-34, 2 STO en chaîne) ; frein alimenté en 400 V CA par KF1 / KF2 (QF2 / QF3 en amont) ; sonde TF sur X10 ; X5 en 24 V permanent.

## Questions en suspens

### Avant câblage de l'armoire (J3, 26/11)

| N° | Question | Pourquoi |
|---|---|---|
| 1 | Frein BE5 400 V CA avec redresseur BGE1.5 : courant d'appel et de maintien. **RÉPONSE PARTIELLE, orale (technicien, 24/11), à confirmer par écrit : maintien 0,18 A ; appel non donné.** Restent à demander : appel (valeur, durée), côté (CA ou CC), tension, tolérance. | Calibre et courbe de QF2 / QF3 (2 A C posés), section du câble frein 5G1,5. Un chat du 27/08 cite 0,183 A à 400 V (non vérifié) : cohérent avec 0,18 A, mais pas un recoupement indépendant prouvé. Sans l'appel, on ne juge pas le déclenchement de la courbe C. |
| 2 | Courant consommé par les entrées STO X6.1 / X6.3 d'un MCX91A (2 en chaîne). **RÉPONSE PARTIELLE, orale (technicien, 24/11), à confirmer par écrit : entrée STO 150 mW par variateur (6,25 mA sous 24 V, 12,5 mA pour les 2 ; précisé par Julien le 24/11 : « 150 mW / var »).** Restent à demander : confirmation écrite, tension de mesure, tolérance. | KA1 33-34 exige au moins 10 mA et 15 V (R-32). 12,5 mA pour 2 : au-dessus de 10 mA, marge 2,5 mA. Détail : `memoire/05_POINTS_OUVERTS.md`, point 1 bis. |
| 3 | Sonde TF : bornes exactes de X10 sur le MCX91A, paramètre du type de sonde, réaction et reset au déclenchement, bornes dans la boîte à bornes moteur. | f31 / f32 : « TF X10 : bornes à confirmer ». Valeurs TF1 / GND, 1830 Ω issues de la doc MDX91A, non confirmées pour le MCX91A. W3 / W6, DF01 / DF02. |
| 4 | Consommation 24 V de l'électronique (X5), variante CSO / CFN / CDM / CMM. | `docs/BILAN_24V.md` porte « ? ». |
| 5 | Courant réseau d'entrée du MCX91A-0055-5E3 (nominal, appel, précharge) et protection amont recommandée. | Réglage de QM1 / QM2 (GV2ME14 6-10 A), point B3 de la revue v33. |
| 6 | Câble moteur blindé 2XSLCY-K 4G2,5 (≈ 15 m) : longueur max sans self ni filtre, reprise du blindage, section max de X2, courant de fuite. | CEM, section PE. Courant de fuite : point d'un chat de septembre, à vérifier s'il est encore utile. |

### Avant les essais (banc 02/12, recette 23/12)

| N° | Question | Pourquoi |
|---|---|---|
| 7 | Temps de retombée du BE5 avec coupure côté CA seule (KF1 / KF2) ; travail de freinage admissible par AU en rotation (1 AU / h au pire). | AU catégorie 0, coupure côté DC abandonnée en octobre. Roue libre ≈ 10 s à mesurer. Demande l'inertie J (client). |
| 8 | Frein alimenté en permanence quand le variateur n'est pas prêt ou en défaut, sans la sortie frein du variateur : réglage à faire (fonction frein désactivée) ? | Revue Krizox D17. SEW a répondu OUI le 06/11 pour le moteur à l'arrêt seulement. |
| 9 | BW100-001 : valeurs à paramétrer, seuil du hacheur, contact thermique éventuel, dégagements minimaux. | Dégagements montés (22/10) : 100 mm variateur-résistance, 70 mm au toit, inférieurs aux 150-200 mm et 300-350 mm relevés dans la doc SEW. Résistances non déplaçables. |
| 10 | Sans codeur, de 30 à 137 tr/min en sortie : précision de la vitesse estimée, écart entre les 2 moteurs, couple continu à basse vitesse (autoventilé), surcharge. | Recette : écart ≤ 2 tr/min à vide. Alarme AL01. **Mail à Xavier (SEW) envoyé le 24/11, réponse attendue** : `docs/MAIL_SEW_XAVIER_2026-11-24.md` (reprend aussi 1, 2, 3, 4, 5). |
| 11 | Perte du bus : le paramètre 8622.6 vaut-il pour PROFINET ? Délai (8455.3) ? Valeur du chien de garde PROFINET ? | TA06, DF03 / DF04, `T_COM`. `interface_sew.md` : point `[?]` (description citant EtherCAT). |
| 12 | Mises sous tension : confirmer par écrit « 1 par heure ». | SEW a répondu « 1 » sans unité ; la doc MDX91A donne 1 par minute. KM1 / KM2 retombent à chaque AU et passage en Manu. `T_SEW_ON` = 3600 s (AL04) repose sur la décision du 18/11. |
| 13 | Exemplaire US : MCX91A et redresseur BGE1.5 / BE5 à 60 Hz derrière le transformateur 480 → 400 V. | Armoire US identique à l'UE (`areas/us-transformer`). |
| 14 | Rotation manuelle de l'arbre de sortie à la clé : couple statique admissible, entraînement inverse, course 90° ou 180°. | Nettoyage en Manu. Mail du 27/08, réponse non retrouvée. |
| 15 | STO ouvert en même temps que KM1 / KM2 retombent (AU) : effet sur le MCX91A ? | Question proposée le 06/11, non validée par Julien : à retirer si inutile. |
| 16 | Confirmation écrite des références commandées (K39 DRN100LS4 / BE5 / TF, MCX91A…, BW100-001) et des délais. | Anciens échanges sur K47DRP90LJ4 et devis en commande binaire. Point du 02/11 : confirmation écrite des motoréducteurs. |

### À poser seulement si le banc ne tranche pas (essais E1 à E6, avant le 02/12)

- PROFINET actif avec 24 V seul sur X5, 400 V coupé (hypothèse `[H]`, décision du 18/11).
- Seuil du bit « moteur en marche » (EP 1.4), utilisé par TA05.
- Handshake SP 1.15 (MOVIKIT ≥ V10).
- Décélération « limite application » (arrêt FCB 13, au plus 5 s).
- Version du firmware par rapport au GSDML V2.42.

### Hors SEW (bloquent les questions 7 et 9)

- Inertie J des parties tournantes : à demander au client (Nicolas Ghut).
- Temps de roue libre : à mesurer à l'atelier.
- Présence des sondes TF : à voir à la réception des moteurs.
- Document de recette : « 10 Hz = 30 tr/min » est faux ; 10 Hz ≈ 27 tr/min, 30 tr/min ≈ 11 Hz.

## Réponses partielles orales (les questions restent OUVERTES)

Source : technicien SEW, par téléphone, 24/11/2026. Aucun document. **À confirmer par écrit.**

| Question | Valeur donnée | Ce qui manque |
|---|---|---|
| 1 (frein BE5 + BGE1.5) | Courant de maintien 0,18 A | Courant d'appel ; côté CA ou CC ; tension ; par frein ou pour les deux (non précisé) |
| 2 (STO X6) | Entrée STO : puissance absorbée 150 mW **par variateur** (6,25 mA sous 24 V, 12,5 mA pour 2) | Confirmation écrite ; tension de mesure |

## Réponses reçues (à ne pas reposer)

| Sujet | Réponse | Date |
|---|---|---|
| Sondes TF montées sur les moteurs livrés | SEW n'a pas l'information : voir à la réception (plaque, boîte à bornes) | 06/11 |
| Frein alimenté en permanence, moteur à l'arrêt et non alimenté (Manu) | OUI, admissible | 06/11 |
| Nombre de mises sous tension | « 1 », unité à confirmer (question 12) | 06/11 |
| STO en chaîne : 24 V / 0 V sur X6.1 / X6.2 de U1, puis X6.3 / X6.4 de U1 vers X6.1 / X6.2 de U2 | Validé par SEW (Julien) ; dessiné en v23 | 06/11 |
| Bornes X6 (STO) | Réglé d'après la notice : X6.1 / X6.3 = +24 V, X6.2 / X6.4 = 0 V | 05/11 |

Réponses à reporter dans `memoire/05_POINTS_OUVERTS.md` (points 1 bis, 8 à 11, Q37), `docs/DECISIONS.md` et `docs/BILAN_24V.md` (questions 2 et 4).

## Réponse écrite de Xavier (26/11/2026) : extraits de doc SEW
Images : `memoire/sew/2026-11-26_reponses_xavier/`. Analyse : `docs/RAPPORT_SEW_2026-11-26.md`.

| Question | Réponse [C doc SEW] | État |
|---|---|---|
| 1 (frein) | BE5 400 V CA : maintien 0,18 A (CA) ; rapport appel / maintien 5,9, soit 1,06 A [H] ; bobine 50 W | **Réglée** : 1,06 A < 2 A, QF2 / QF3 2 A C conviennent |
| 2 (STO) | X6 : 150 mW, type 2 IEC 61131-2 ; 12,5 mA pour 2 [H] | **Réglée** (tension de la valeur non donnée, sans effet) |
| 3 (TF) | **X10:3 = TF1, X10:4 = GND** (X10:1 / X10:2 = sortie frein DB00) ; seuil 1830 Ω | Bornes réglées : **schéma faux (TF sur X10:1 / X10:2)** ; paramètre, réaction, réarmement : sans réponse |
| 4 (24 V X5) | 6 W (taille 0S, CSO / CFN) ; 8,5 W max ; 24 V -10 % / +20 % | **Réglée** |
| 5 (réseau) | Entrée 5 A CA ; disjoncteur moteur ≥ 1,1 × courant calculé ou × I nominal moteur | Partielle : appel / précharge sans réponse |
| 10 (vitesse) | VFC^PLUS sans codeur : écart typique 0,2 × glissement nominal | Partielle : dispersion, échauffement, tension réseau sans réponse ; n_N de plaque nécessaire |
| 12 (mises sous tension) | 1 par minute au plus ; 10 s mini hors tension | **Réglée** (1 / h visé) |
