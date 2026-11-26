# Réponse écrite de SEW (Xavier), 26/11/2026 : analyse

Sources : 7 extraits de documentation SEW, dans `memoire/sew/2026-11-26_reponses_xavier/` (liste et pages dans le README du dossier).
[C] = lu dans la doc SEW. [H] = calcul ou déduction de l'assistant. [?] = manque.

## 1. Point urgent : bornes de la sonde TF (X10)
- Doc [C] (§ 4.7.6 et 4.7.7) : **X10:1 = DB0/DB00 (sortie de commande de frein 24 V, 150 mA)**, X10:2 = GND ; **X10:3 = TF1**, **X10:4 = GND** (entrée sonde).
- Seuil de déclenchement TF : 1830 Ω. Capteurs acceptés : TF, TH (bilame), KTY84-130, Pt1000.
- **Le schéma (f31 / f32, depuis la v11) raccorde la sonde TF sur X10:1 / X10:2 : c'est faux.** Il faut X10:3 / X10:4. Sur X10:1, la sonde serait sur une sortie 24 V.
- À changer dans le script (fils 3131 / 3132 et 3231 / 3232 ; liste des liaisons ligne 2058 de `ttk_schema.py`). Le symbole a déjà les 4 broches X10:1 à X10:4.
- Pas de réponse sur le paramètre du type de sonde ni sur la réaction / le réarmement [?].

## 2. Frein BE5 400 V CA (QF2 / QF3)
- Doc [C] (moteurs triphasés, § 8.5.4) : BE5, tension 400 V (380-431) CA : **courant de maintien I_H = 0,18 A côté CA**. Puissance de la bobine 50 W. **Rapport appel / maintien = 5,9.**
- Appel [H] : 0,18 × 5,9 = **1,06 A**. Durée non donnée [?].
- Effet [H] : 1,06 A est sous le calibre de QF2 / QF3 (2 A). Le disjoncteur ne déclenche donc pas, quelle que soit la durée de l'appel. **2 A courbe C convient.** Le câble 5G1,5 et les contacts de KF1 / KF2 portent sans souci 1,06 A.
- Question 1 de `QUESTIONS_SEW.md` : réglée (la durée de l'appel n'est plus utile).

## 3. STO (X6) et contact KA1 33-34
- Doc [C] (§ 4.7.11) : X6 (1 par variateur) : **puissance absorbée 150 mW**, entrée type 2 selon IEC 61131-2. X6:1 / X6:3 = F_STO_P reliées en interne, X6:2 / X6:4 = F_STO_M. Jusqu'à 10 appareils reliés en chaîne. Liaison 30 m max.
- Tension de la valeur : non donnée [?].
- Calcul [H] : 150 mW / 24 V = 6,25 mA par variateur ; 2 en chaîne (entrées en parallèle par les liaisons internes) = **12,5 mA ≥ 10 mA** (minimum de KA1, R-32). C'est le cas A du 24/11 : confirmé par la doc.
- Question 2 de `QUESTIONS_SEW.md` : réglée. Schéma inchangé.

## 4. Variateur MCX91A-0055-5E3 (taille 0S)
- Doc [C] (§ 4.4.1) : courant d'entrée nominal **5 A CA** (400 V) ; courant de sortie 5,5 A ; surcharge 150 % pendant 30 s ; pertes 50 W ; 24 V absorbé 8,5 W max.
- **Mises sous / hors tension réseau : 1 par minute au plus ; durée minimale hors tension : 10 s.** Nous visons 1 par heure : conforme. Pour le programme : après l'ouverture de KM1 / KM2, attendre au moins 10 s avant de les refermer.
- Protection (§ 5.12.1) [C] : disjoncteur moteur admis. Calibre ≥ 1,1 × courant calculé par SEW-Workbench ; sans calcul, ≥ 1,1 × courant nominal du moteur.
- Effet [H] : 1,1 × 5 A = 5,5 A ; QM1 / QM2 réglés à 6,5 A : au-dessus. Le critère « 1,1 × I nominal du moteur » demande le courant de plaque du DRN100LS4 [?].
- Courant d'appel / précharge : non donné [?].

## 5. 24 V de l'électronique (X5)
- Doc [C] : X5 : 24 V -10 % / +20 %. Puissance absorbée (§ 5.14.3), taille 0S, PROFINET -T0/../CSO/CFN, sans E/S, codeur ni frein moteur : **6 W**. Maximum général : 8,5 W.
- Calcul [H] : 6 W / 24 V = 0,25 A par variateur, 0,5 A pour 2 (8,5 W : 0,35 A, 0,71 A pour 2).
- Bilan T2 (24VELEC) [H] : 0,655 A connus + 0,5 A = 1,16 A (12 % de 10 A) ; avec 8,5 W : 1,36 A (14 %). Large marge.

## 6. Précision de vitesse sans codeur (question principale)
- Doc [C] (p. 142) : moteur asynchrone en **VFC^PLUS sans codeur** : imprécision statique de la vitesse = **écart typique 0,2 × fréquence de glissement nominale**, « en fonction de la précision des paramètres moteur ». Imprécision statique = écart entre la valeur moyenne réelle et la consigne.
- Pas de valeur en U/f dans ce tableau. Le mode à retenir est donc VFC^PLUS [H].
- Pour un chiffre, il faut le glissement nominal du moteur : vitesse nominale n_N de la plaque du DRN100LS4 [?]. Formule [H] (4 pôles, 50 Hz : 1500 tr/min synchrone, rapport 10,61) :
  - écart en sortie ≈ 0,2 × (1500 − n_N) / 10,61 tr/min ;
  - c'est un écart en tr/min, à peu près le même à 30 et à 137 tr/min : en %, il pèse 4,5 fois plus à 30 tr/min.
- Critère [H] pour l'exigence ≤ 2 tr/min entre les 2 axes :
  - si les 2 écarts vont en sens opposé (cas pessimiste) : 2 × 0,2 × (1500 − n_N) / 10,61 ≤ 2, donc **n_N ≥ 1447 tr/min** ;
  - un axe seul (≤ 2 tr/min) : n_N ≥ 1394 tr/min.
- « Écart typique » n'est pas un maximum. La doc parle de « précision des paramètres moteur » : faire l'identification du moteur à la mise en service [H].
- Sans réponse [?] : dispersion entre 2 ensembles, effet de l'échauffement et de la tension réseau, paramètres à régler (compensation de glissement).
- À vide, le glissement réel est faible : l'écart réel devrait rester sous l'écart typique [H, à mesurer au banc].

## 7. Ce qui reste sans réponse
| Question du mail | Manque |
|---|---|
| 1 | Dispersion entre 2 ensembles ; échauffement ; tension réseau ; paramètres (compensation de glissement) |
| 2 (STO) | Tension à laquelle 150 mW est donné (sans effet sur la conclusion) |
| 3 | Courant d'appel / précharge réseau ; paramètre de type de sonde TF, réaction et réarmement |

## 8. Effets
- **Schéma** : TF de X10:1 / X10:2 vers **X10:3 / X10:4** (f31, f32). À faire en v44 avec l'accord de Julien. Vérifier aussi le câblage réel si l'armoire est déjà câblée.
- QF2 / QF3 (2 A C), STO, QM1 / QM2 (6,5 A) : inchangés.
- Programme (dépôt automatisme) : 10 s mini entre ouverture et fermeture de KM1 / KM2 ; mode VFC^PLUS ; identification du moteur.

## 9. Suite (Julien, 26/11)
- Sonde TF pas encore câblée ; schéma corrigé en v44 (X10:3 / X10:4).
- Plaque : n_N = 1450 tr/min, I_N = 4,75 A. Écart typique : 0,2 × 50 / 10,61 = **0,94 tr/min par axe** ; au pire **1,89 tr/min** entre les axes (≤ 2).
- Pas de relance de SEW. Calcul des disjoncteurs moteur : `docs/RAPPORT_v44_2026-11-26.md`.
