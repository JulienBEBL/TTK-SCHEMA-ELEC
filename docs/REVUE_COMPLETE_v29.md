# Revue complète du schéma : v29 (16/11/2026)

Demande de Julien : reprendre tout le schéma, dire s'il reste un problème, une erreur, un doute, un inconnu, une optimisation, et s'il est prêt à être donné au stagiaire (électrique, nomenclature, visuel).
Méthode : contrôles par calcul sur le `.xrs` généré. Rien n'a été vu dans WinRelais.
- `xrs_tool.py verifier` : 0 erreur, 28 points d'attention connus.
- `xrs_chevauchements.py` : 0 chevauchement.
- `xrs_numeros.py` : 0 problème de numérotation.
- Spécification des liaisons du script : 0 écart.
- Relecture des équipotentielles : contrôle complet en v26 (`docs/CONTROLE_FILS_v26.md`), puis changements v27 à v29 revus un par un.

## 1. L+ / M capteurs de la CPU (question de Julien)
Source : manuel Siemens « S7-1200 G2 Programmable Logic Controller » (V1.0.1, 04/2025), CPU 1214C, pages « Wiring diagrams », « Power supply and sensor power », « Digital inputs and outputs » (entrée 109988293).

**Connecteur X80 de la CPU 1214C DC/DC/DC**
- 1re rangée = **alimentation de la CPU** : L+, M.
- 2e rangée = **sortie « Sensor power »** : GND, L+, M.
  - GND = masse châssis : sur le schéma, c'est la broche FE.
  - L+ et M de cette rangée = « L+ capt » et « M capt » du schéma.

**Sortie capteurs (L+ capt / M capt)**
- C'est une **sortie** 24 V fournie par la CPU, pas une entrée. Elle ne se raccorde jamais à un 24 V extérieur.
- Courant : 400 mA max, protégée contre les courts-circuits.
- Tension : L+ moins 4 V au minimum.
- **Non isolée** : son M est le M de la CPU (0 V commun).
- Section de fil : 0,2 à 1,5 mm².
- Rôle : alimenter les contacts et capteurs des entrées.
- **M capt** sert seulement aux capteurs électroniques 3 fils. Nos entrées sont toutes des contacts secs : M capt reste **libre**, c'est normal.

**Entrées (X10)**
- 14 entrées, type « sink/source », commun **1M** sur 2 broches.
- Note ② de Siemens : « for sinking inputs, connect "-" to "M" ». Donc **1M au 0 V** : c'est le cas sur le schéma.
- Courant par entrée, contact fermé : 6 mA pour Ia.0 à Ia.5, 4 mA pour Ia.6 à Ib.5.

**Consommation de -X21.14 (13 points)**
- I0.0 à I0.5 : 6 entrées × 6 mA = 36 mA.
- I0.6 à I1.4 : 7 entrées × 4 mA = 28 mA.
- Total ≈ **64 mA, soit 16 % des 400 mA** : très à l'aise.
- I1.5 (Z1 de KA1) est alimentée par KA1, pas par L+ capt.

**Sorties (X11)**
- Sorties à transistor « sourcing » (+24 V commuté), 0,5 A max.
- Train d'impulsions (PTO) : 100 kHz sur Qa.0 à Qa.3, 20 kHz sur Qa.4 à Qb.1.
- Le schéma est conforme : PUL sur Q0.0 / Q0.2, DIR sur Q0.1 / Q0.3, ENA sur Q0.4 / Q0.5.
- Note 3 de Siemens : une résistance de charge (au moins 10 % du courant nominal) peut améliorer les impulsions. À essayer seulement si les drivers perdent des pas.
- **Erreur de nom de broche** : en G2, l'alimentation des sorties s'appelle **2L+ / 2M** (connecteur X11). Le symbole de la CPU porte **3L+ / 3M** (nom des CPU de 1re génération). Le câblage est juste, seul le texte est faux. Il faut corriger 2 noms de broche dans le symbole `CUSTOM\Siemens_6ES7214-1AH50-0XB0_CPU1214C_G2_sorties.xsy` (librairie du PC et copie du dépôt), puis dans le script. Non fait : c'est ta librairie.

**Note ① de Siemens** (« jumper the 24 V DC Power M to chassis ground » pour plus d'immunité aux parasites)
- **Ne pas le faire.**
- Le 0 V est déjà relié à la terre en un seul point, par X12.11 (liaison PELV, borne sectionnable pour la mesure d'isolement).
- Un 2e pont 0 V – terre à la CPU ferait double liaison et fausserait la mesure.

## 2. Électrique : erreurs
Aucune erreur de connexion trouvée.
- Points corrigés en v28 / v29 : textes de tableaux, titres de folios, libellés du f71, références de S1 / S2 / S3.
- Reste le nom de broche 3L+ / 3M au lieu de 2L+ / 2M (voir § 1).

## 3. Électrique : doutes et inconnus (valeurs manquantes)
| # | Sujet | Effet | Qui |
|---|---|---|---|
| 1 | Courant du frein BE5 (appel et maintien) | Calibre 2 A courbe C de QF2 / QF3 à confirmer | SEW |
| 2 | Bornes X10 de la sonde TF du MCX91A ; sondes TF montées sur les moteurs livrés ? | Câblage de W3 / W6 à confirmer | SEW, réception des moteurs |
| 3 | Courant des entrées STO X6 | KA1 demande au moins 10 mA / 15 V par contact | SEW |
| 4 | Consommation X5 des MCX91A | Bilan 24 V incomplet (marge large : 0,66 A connus sur 10 A) | SEW |
| 5 | Réglage de QM1 / QM2 (GV2ME14, 6 à 10 A) | À caler sur le courant d'entrée réel du MCX91A avec un moteur 2,2 kW (notice SEW) | Julien |
| 6 | KA2 (LC1D09BD) coupe du 48 V continu : tenue en DC-1 sous 48 V | Pouvoir de coupure du contact à vérifier | fiche Schneider |
| 7 | T3 48 V 240 W (5 A) pour 2 drivers DM860H et 2 moteurs Nema 34 | Suffisant si les 2 axes ne sont pas à pleine charge en même temps ; à vérifier selon vitesse et couple | Julien |
| 8 | Section des fils de H2 (piqué sur le bus, protégé par QF1 20 A) | Fils prévus pour 20 A, sinon fusible 2 A | Julien |
| 9 | ifm MN508S : homologation sécurité, actionneur codé commandé ? | Capot B2 | Julien |
| 10 | Bornes du thermocouple (type K compensé ?) | Mesure de B7 | achat |
| 11 | EL1 / EL2, EV1 / EV2 : borne PE nécessaire ? | Bornes X13 | classe des appareils |
| 12 | Brochage G2 des modules SM 1223 et SM 1231 TC | Noms de broches à confirmer (comme la CPU, § 1) | doc Siemens |

## 4. Essais de banc à faire avant la mise en service
- Boucle de retour Y1-Y2 (`docs/ESSAI_BANC_BOUCLE_RETOUR.md`).
- Écart d'ouverture entre B1 et B2 (200 ms).
- I0.2 / I0.3 à 1 quand le capot est ouvert.
- Décodage de Z1 (I1.5) dans TIA.
- Impulsions dans TIA et micro-pas des DM860H (rester sous 100 kHz).

## 5. Optimisations possibles (non faites)
- Tableau des conducteurs pour le câbleur : section et couleur par type de fil. Le f03 (légende) a été supprimé le 02/11 ; à remettre si le stagiaire en a besoin.
- Résistance de charge sur les sorties PUL si les impulsions sont mauvaises (§ 1).
- Liste des câbles (f80) et nomenclature (f90) à générer par WinRelais.

## 6. Prêt pour le stagiaire ?
**Pas encore.** Le schéma est cohérent électriquement : aucune erreur de connexion, tous les contrôles à 0. Il manque :

1. **Numérotation des fils** : **faite en v30 sur tous les folios** (16/11).
2. **Nomenclature** : références manquantes.
   - B3 à B6 (fins de course), B7 (sonde) et câble W8.
   - Voyants H2, H3, H4.
   - Bornes (PT 2,5 / PT 4 / terre), butées, PTFIX.
   - Câbles W1 à W13 et PN1 à PN4.
   - Ajoutées en v29 : S1 / S2 (XB5AS8442 + ZBE102 + ZBE101), S3 (Eaton T0-4-8223/E).
3. **WinRelais** :
   - lancer les références croisées automatiques (KM1, KM2, KF1, KF2, KA2, S1 à S3, K1, K2 apparaissent sur plusieurs folios) ;
   - générer f80 et f90 ;
   - relire tous les folios à l'écran.
4. **Nom de broche** 3L+ / 3M à corriger en 2L+ / 2M (§ 1).
5. **Implantation** à mettre à jour : XR2, X13, X21.14 (`docs/A_FAIRE_IMPLANTATION_2026-11-16.md`).
6. Les inconnus du § 3 ne bloquent pas le câblage, sauf les n° 1 (calibre QF2 / QF3) et 2 (bornes X10 de la sonde TF), à fixer avant la mise sous tension.
