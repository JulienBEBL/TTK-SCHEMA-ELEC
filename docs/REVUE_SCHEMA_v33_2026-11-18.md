# Revue du schéma v33 (18/11/2026, PC PRO RIMANE)

Demande de Julien (18/11) :
1. reprendre tous les points en suspens du schéma et dire les zones d'ombre ;
2. relire chaque folio (titre, contenu, phrases) et dire s'il est à jour.

Périmètre : le schéma seulement (pas l'implantation, pas le programme TIA).
Méthode : lecture de `memoire/`, `docs/REVUE_COMPLETE_v29.md`, `docs/QUESTIONS_SEW.md`, et relevé par calcul de tous les textes, champs et tableaux de `schema/generes/release/TTK_2026-11-18_v33.xrs`. Rien n'a été vu à l'écran.
**Rien n'est corrigé** : liste seulement. Julien tranche, puis v34 après son go.

## 0. v33 réenregistrée par WinRelais (PC Rimane)
- Copie : `schema/recus/2026-11-18_v33_ouverte_WinRelais.xrs`.
- Comparaison au fichier généré : aucune retouche. Seuls changent les numéros de ligne et le sens de 24 fils (mêmes extrémités).
- **Chemins d'images : restés relatifs** (`..\..\images\…`) après l'enregistrement. Point clos.
- Release remise à l'état généré (`git checkout`).

## 1. Zones d'ombre

### 1.A À régler avant le câblage ou la mise sous tension
| # | Sujet | Ce qu'on sait | Ce qui manque | Qui |
|---|---|---|---|---|
| A1 | **Boîte de jonction +BJM** : quels câbles y passent ? | Mémoire (17/11) : hypothèse « tous les câbles machine passent par la boîte ». Schéma v33 (f80) : seuls W4 et W12 vont à +BJM ; W2, W3, W5, W6, W8, W9, W10, W14 vont directement à « +M ». | Décision : tous, ou W4 + W12 seulement ? La boîte n'est dessinée nulle part (ni bornier +BJM-X1). Boîte non achetée, câbles boîte → appareils non prévus. | Julien |
| A2 | Calibre de QF2 / QF3 (2 A courbe C) | Frein BE5 400 V CA | Courant d'appel et de maintien du BE5 | SEW (question 4) |
| A3 | Sonde TF : bornes X10 du MCX91A ; sondes montées sur les moteurs livrés ? | W3 / W6 et bornes X31.2x / X32.2x dessinés | Bornes exactes, que faire si pas de sonde | SEW, réception des moteurs |
| A4 | Fils de H2 (piqué sur le bus, protégé par QF1 20 A) | Julien garde le branchement (13/11) | Section des fils pour 20 A, ou fusible 2 A sur L3 | Julien |
| A5 | V/J de W9 / W10 côté armoire | Côté moteur : à la masse du moteur (Julien 17/11). f80 : « 5G1,5 (4 + V/J) » | Où va le V/J dans l'armoire (XPE1 ?) : non dessiné | Julien |
| A6 | Bornes du thermocouple X63.11 / X63.12 | Gardées (Julien 17/11) | Type de borne : f63 dit « type à définir », la nomenclature les compte en PT 2,5. Jonction sonde / câble RS 891-9031 (Q28) et fixation de la sonde (Q29) non validées | Julien |

### 1.B À confirmer (ne bloque pas le câblage)
| # | Sujet | Qui |
|---|---|---|
| B1 | Courant des entrées STO X6 (KA1 demande au moins 10 mA / 15 V) | SEW (question 3) |
| B2 | Consommation X5 d'un MCX91A (bilan 24VELEC) | SEW (question 8) |
| B3 | Réglage de QM1 / QM2 (6,5 A) sur le courant d'entrée réel du MCX91A | Julien |
| B4 | KA2 (LC1D09BD) : coupure du 48 V continu en DC-1 | fiche Schneider |
| B5 | T3 240 W pour les 2 drivers et les 2 Nema 34 | Julien (vitesse, couple) |
| B6 | ifm MN508S : homologation sécurité, actionneur codé commandé ? | Julien |
| B7 | Noms de broches G2 du SM 1223 (encore 3L+ / 3M au f62) et du SM 1231 TC | doc Siemens |
| B8 | EL1 / EL2, EV1 / EV2 : borne PE nécessaire ? | classe des appareils |
| B9 | Références manquantes : H2, H3, H4, B7, butées, +BJM ; PTFIX 6/12 par couleur | Julien |
| B10 | Valeurs du script sans source dans la mémoire : QF1 10 kA, QS1 690 V, QF9 6 kA, QF10 4,5 kA, T3 5 A, U1 5,5 A, U3 / U4 6,0 A, M3 / M4 6 A - 8,5 Nm, EL 14 W, EV 19 W, XD1 1,5 kW, S4 « Z000263594 » | Julien ou fiches |
| B11 | Relevés sur le matériel : couleurs des 4 conducteurs utilisés de W14 et section ; marquage U V W de W2 / W5 ; blanc = 1b pour W3 / W6 | Julien, au câblage |
| B12 | f01 « Affaire : à compléter » | Julien |
| B13 | Zoom écrit avec une virgule par WinRelais sur le PC Rimane (`0,749…`) : relu sans souci par le WinRelais de Julien ? | Julien |

### 1.C Essais de banc (inchangés)
- Boucle de retour Y1-Y2 (`docs/ESSAI_BANC_BOUCLE_RETOUR.md`).
- Écart d'ouverture B1 / B2 (200 ms).
- I0.2 / I0.3 à 1 capot ouvert.
- Z1 (I1.5) dans TIA.
- Impulsions et micro-pas des DM860H (rester sous 100 kHz).
- Nouveau (v32) : B3-B6 lus à 0 en fin de course (NF).

### 1.D Points de `05_POINTS_OUVERTS.md` réglés ou périmés (à fermer)
| Point | Pourquoi le fermer |
|---|---|
| Q8 (retours v20) | Dépassé : v33 relue |
| Q12 (image f31 / f32) | Bloc de droite refait en v33 |
| Q26 (W10 « 1-2-3-3 ») | v15 ; le fichier généré porte 1-2-3-4, pas revu depuis |
| § 11 « W9 / W10 : section à définir » | Réglé le 17/11 : LIYCY-JZ 5G1,5 |
| § 21 Symbole NFT702 hors librairie | Réglé le 18/11 : 54 symboles CUSTOM installés |
| § 25 Cartouche obsolète du f51 | Description du f61 juste en v33 |
| § 26 Images f21 / f01 | Insérées, en chemin relatif |
| v28 « f80 / f90 à remplir par WinRelais » | Générés par le script depuis la v32 / v33 |
| PC Rimane « symboles CUSTOM non installés » | Réglé le 18/11 |
| PC Rimane « chemin relatif gardé à l'enregistrement ? » | Réglé le 18/11 (§ 0) |

## 2. Revue folio par folio
Légende : OK = à jour ; **à corriger** = proposition de correction (non faite).

| Folio | Titre | État | Remarques |
|---|---|---|---|
| 01 | PAGE DE GARDE | OK | « Affaire : à compléter » (B12). Icc 6 kA et TN-S : conformes à `01_PROJET.md` |
| 02 | SOMMAIRE | OK | 27 folios, généré depuis la liste ; f90 à f92 justes |
| 03 | SYNOPTIQUE GENERAL | **à corriger** | 1) « vers la machine +M : -X20, -X31… » : ne cite pas la boîte +BJM (dépend de A1). 2) Bloc « DISTRIBUTION 24 V (f21) » : -X21.14 (24 V capteurs, v28) absent |
| 10 | ARRIVEE ET SECTIONNEMENT | OK | QS1 690 V et QF1 10 kA sans source (B10) |
| 11 | DISTRIBUTION 400 V | OK | QF2 / QF3 2 A à confirmer (A2) ; réglage 6,5 A (B3) |
| 12 | DISTRIBUTION 230 V - ALIMENTATIONS | OK | H2 « À définir » (référence, B9) ; fils de H2 (A4) |
| 13 | DISTRIBUTION 230 V - SERVICES | OK | |
| 20 | 48 VDC ET MOTEURS PAS A PAS | **à corriger** | Étiquettes de W9 / W10 : « 4 cond. blindé » ; f80 et nomenclature : « LIYCY-JZ 5G1,5 (4 + V/J) » (décision du 17/11). V/J non dessiné (A5) |
| 21 | DISTRIBUTION 24 VDC | OK | H3 sans référence ni caractéristique (B9) |
| 30 | RESEAU PROFINET | OK | Textes des ports décalés en v33 |
| 31, 32 | PUISSANCE VARIATEUR 1 / 2 | OK, sauf A1 | Bloc de droite à 2 lignes (v33). W2 / W3 / W5 / W6 : passage par +BJM ou non (A1) |
| 40 | RELAIS DE SECURITE | OK | S4 : « Z000263594 » affiché, sans source (B10) |
| 41 | SECURITE - ENTREES | OK | S1 / S2 « 2 NF + 1 NO », B1 11-12 / 23-24. W14 (câble M12 de B2) sans étiquette de câble |
| 42 | SECURITE - SORTIES | OK | STO en chaîne validé SEW ; courant STO (B1) |
| 50 | PUPITRE OPERATEUR | OK | W11 et PN4 sans étiquette de câble |
| 60 | AUTOMATE - ALIMENTATION & ENTREES TOR | OK | Tableau à jour (NF pour B3-B6). Voir f90 pour le texte des B3-B6 |
| 61 | AUTOMATE - SORTIES TOR | OK | |
| 62 | MODULE SM 1223 - SIGNALISATION | OK | Broches 3L+ / 3M (B7) ; H4 sans référence (B9) |
| 63 | MODULE SM 1231 TC | **à corriger** | « Bornes thermocouple : type à définir » contre PT 2,5 dans la nomenclature (A6). Étiquette de W8 « compensation type K » sans la référence connue (RS 236-3959, au f80) |
| 70 | BORNIERS DE L'ARMOIRE | **à corriger** | « câble -W12 … -> boîte machine » : écrire « +BJM » (nom du 17/11). Comptes de W11 (22 + 4 réserve) et W12 (16 + 2 réserve) : justes |
| 71 | BORNIER PUPITRE | **à corriger** | Colonne « Côté armoire » de X60.11, X60.21, X60.23 : « -KA2:13, -KM1:13, -KM2:13 » (premiers appareils du potentiel). Plus clair : « 24 V capteurs (-X21.14, f21) ». X50.13 : « -K1:FE, -T1:PE, -T2:PE ... » ; plus clair : « PE (-XPE1) » |
| 80 | LISTE DES CABLES | OK (Julien) | Dépend de A1 (destinations « +M » ou « +BJM ») |
| 85 | IMPLANTATION ARMOIRE | **à revoir** | Texte « à réaliser sous WinArmoire » : l'implantation est faite dans `implantation/` (draw.io, générée). Garder, changer le texte, ou retirer le folio ? |
| 90, 91, 92 | NOMENCLATURE (1/3 à 3/3) | **à corriger** | 1) B3-B6, caractéristiques : « …, Julien 18/11 » (note de travail dans un document client) ; à retirer. 2) PTFIX 2X4 : « nombre de blocs : à vérifier » alors que c'est réglé (38 blocs, 2 trous, 6 mm). 3) H3 et H4 : caractéristiques vides alors que le script les porte (« 24 V CC - blanc ou vert », « 24 V CC - rouge ») : à chercher dans le script |

## 3. Corrections proposées pour la v34 (après le go de Julien)
1. f03 : -X21.14 dans le bloc 24 V ; +BJM selon A1.
2. f20 : étiquettes W9 / W10 en « 5G1,5 blindé ».
3. f63 : type des bornes X63 selon A6 ; référence de W8 sur l'étiquette.
4. f70 : « +BJM » à la place de « boîte machine ».
5. f71 : libellés côté armoire de X60.11 / X60.21 / X60.23 et X50.13.
6. f85 : selon la décision de Julien.
7. f90-f92 : retirer « Julien 18/11 » ; PTFIX 2X4 réglé ; caractéristiques de H3 / H4.
8. Mémoire : fermer les points du § 1.D.
