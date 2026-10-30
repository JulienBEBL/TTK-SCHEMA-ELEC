# 03 · Architecture électrique (état v9, 30/10)

Numéros de folio : ceux **affichés depuis la v9** (ordre du 30/10). Correspondance avec les anciens numéros (encore utilisés dans le script) : `04_REGLES_DESSIN.md`, « Ordre des folios ».

## Puissance
- W1 → X11 → QS1 → QF1 (f20). Les sorties de QF1 partent en **renvois directs** vers le bus 400 V (f21). Le répartiteur X12 et la barrette de terre X13 existent dans l'armoire mais **ne sont plus dessinés** [D 29/10].
- **Bus tétra L1 L2 L3 N** en haut des folios, enchaîné par renvois : f20 (QF1) → f21 → f22 → f23 (L3 et N seulement).
- **f21 (400 V)** : piquages QM1 / QM2 (L1 L2 L3) → KM1 / KM2 → U1 / U2 ; QF2 (L1 L2) / QF3 (L1 L3) → KF1 / KF2 → freins (alimentés côté CA, indépendamment du variateur).
- **f22 (230 V alimentations, ancien f13 + ancien f30)** : QF4 (L1+N) → T1, QF5 (L1+N) → T2 ; QF6 (L2+N) → renvoi vers T3 (f24) ; voyant H2 (L3+N). Sorties 24VELEC, 24VSEC, 0 V commun → renvois vers f25 ; liaison PELV X36.1.
- **f23 (230 V services)** : QF8 → EL1 / EL2 (l'une sous l'autre) ; QF7 → EV1 / EV2 (l'un sous l'autre, N contourne à gauche, L à droite : 0 croisement) ; QF9 → QF10 → X14 dans l'axe.
- Phases : 24 V = L1, 48 V = L2, 230 V auxiliaires et voyant = L3 (visible par les piquages du bus et les numéros de fil).
- **Terre (règle C partout, 29/10)** : chaque appareil a un fil PE court + renvoi vers la terre de l'arrivée (f20). Au f20, le PE de X11 descend dans le faisceau puis se divise en un départ par appareil (T1, T2, X36.1, X14, T3, U1 X1, U2 X1, P1 FE, K1 FE). Moteur : PE → X2 PE du variateur (f31 / f32), sans renvoi.
- Parafoudre **supprimé** [D 28/10].
- Moteurs, freins et TF **via le bornier X70** [D 28/10] : pas encore câblé aux f31 / f32 (v9).

## 24 V : deux alimentations, 0 V commun
| 24VELEC (T2, bornier X31) | 24VSEC (T1, bornier X33) |
|---|---|
| CPU K1 : L+ et sorties 3L+ (PUL / DIR / ENA des drivers) | KA1 13-14 → KF1, KF2 ; puis Manu-D → KA2 (48 V) |
| K2, K3 : L+ | KA1 23-24 → Auto-A → KM1, KM2 |
| Switch K4 | KA1 33-34 → Auto-B → STO de U1 / U2 |
| IHM P1 (X71.21) | K2 : sorties 3L+ → colonne H1, voyant S4, voyant H4 |
| KA1 : alimentation A1 | |
| U1 / U2 : X5 (24 V de sauvegarde) | |
| Voyant H3 | |

- **Répartition validée par Julien le 29/10** (« ok pour le tableau actuel »).
- **Noms (29/10, v7)** : **24VSEC** = T1 (bornier X33, alimente les contacts de KA1) ; **24VELEC** = T2 (bornier X31, électronique). Anciens noms : +24 V COMMANDE / +24 V ELEC.
- **Après un AU, les deux 24 V restent distribués.** L'AU ouvre les contacts de KA1 : bobines KM1, KM2, KA2, KF1, KF2 et STO perdent leur 24 V. Automate, IHM, switch, colonne et voyants restent alimentés (affichage du défaut). Seuls QS1 / QF1 / QF4 / QF5 coupent T1 / T2.
- 0 V commun (X32) [D 28/10] ; les deux +24 V ne sont **jamais** mis en parallèle. Liaison PELV unique 0 V – PE par la borne sectionnable X36.1 (f22).
- **Barres 24VELEC et 0 V en haut** des folios de commande (f25, f30, f40 à f42, f45, f50 à f53), enchaînées par renvois dans l'ordre des pages ; X31 et X32 (f25) s'y piquent [D 29/10]. Les appareils dont le 0 V est en bas (bobines f12, voyants et colonne f51) rejoignent la barre par un collecteur remonté à gauche.

## 48 V (f24)
- T3 → **KA2, 1 pôle (1-2) sur le +48 V** → X34 → un fil par driver. 0 V 48 en direct T3 → X35 → un fil par driver [D 28/10]. Présentation descendante (T3, KA2, X34 / X35, drivers, moteurs) [D 29/10] ; 2 croisements sans jonction.
- **KA2** (ex KM3, renommé le 29/10) : contacteur LC1D09BD utilisé en contacteur auxiliaire, pas un contacteur moteur.
- Bobine KA2 alimentée **uniquement en Manu** (Manu-D), depuis KA1 13-14 : le 48 V est coupé par l'AU et absent en Auto.

## Sécurité (f40 relais, f41 entrées, f42 sorties), fiche de Julien du 27/10
- **KA1** XPSUAF13AP, cat. 0, PL d visé. Boucle de retour Y1-Y2 : NF miroir de KM1, KM2, KF1, KF2, KA2, puis S4.
- **Entrées (f41)**
  - Voie 1 : S11 → S1 NF1 → X71.1 → S2 NF1 → X71.2 → [X70.1 → B1 → X70.2] // [X71.13 → Manu-A → X71.14] → S12.
  - Voie 2 : idem NF2, [X70.5 → B2 (1 NO) → X70.6] // [X71.15 → Manu-B → X71.16] → S22.
  - Un contact Manu par voie, jamais commun.
- **Sorties (f42)** : 13-14 freins + 48 V (Manu-D) ; 23-24 Auto-A → KM1 / KM2 (pas d'ordre automate, option A) ; 33-34 Auto-B → STO des 2 MCX91A en parallèle (validé SEW).
- **L'automate ne commande rien en sécurité** : il reçoit seulement des états (AU, capots, mode, retours contacteurs, diagnostic KA1).

| Contact S3 | Bornes | Position | Rôle | X71 |
|---|---|---|---|---|
| Auto-A | 13-14 | Auto | KM1 / KM2 | 7-8 |
| Auto-B | 23-24 | Auto | STO | 9-10 |
| Auto-C | 33-34 | Auto | automate I0.4 | 11-12 |
| Auto-D | 43-44 | Auto | réserve | — |
| Manu-A | 53-54 | Manu | shunt capot voie 1 | 13-14 |
| Manu-B | 63-64 | Manu | shunt capot voie 2 | 15-16 |
| Manu-C | 73-74 | Manu | automate I0.5 | 17-18 |
| Manu-D | 83-84 | Manu | bobine KA2 | 19-20 |

| Sélecteur | Capot | AU | Freins | 48 V | KM1 / KM2 | STO |
|---|---|---|---|---|---|---|
| Auto | fermé | OK | alimentés | coupé | fermés | libéré |
| Auto | ouvert | OK | coupés | coupé | coupés | actif |
| Manu | ouvert ou fermé | OK | alimentés | alimenté | coupés | actif |
| tous | tous | enfoncé | coupés | coupé | coupés | actif |

Transitions (ancien f43, supprimé le 29/10) :

| Passage | Effet |
|---|---|
| Auto → Manu, capot fermé | KM1 / KM2 et STO retombent, shunts ajoutés, 48 V alimenté, pas de réarmement |
| Auto → Manu, en rotation | idem, moteurs en roue libre freins desserrés (≈ 10 s à mesurer) : risque résiduel |
| Auto → Manu, capot ouvert | relais déjà retombé : réarmement S4 après passage en Manu |
| Manu → Auto, capot fermé | 48 V coupé, STO libéré, KM1 / KM2 fermés ; rien ne démarre sans ordre de marche IHM |
| Manu → Auto, capot ouvert | shunts ouverts : le relais retombe ; fermer le capot puis réarmer |

Programme : défaut sélecteur si I0.4 = I0.5 en régime établi (0/0 ou 1/1), filtrage de quelques centaines de ms à la commutation. Procédure normale : demande Manu sur l'IHM, arrêt en rampe, puis rotation du sélecteur.

Risques résiduels : sélecteur sans clé (capot shunté en Manu, choix du client) ; roue libre si le sélecteur tourne pendant la rotation (≈ 10 s, à mesurer) ; un seul contact Manu-D pour le 48 V (PL c accepté).

## Automate (f50 à f53) : liste d'E/S du 06/10, **gelée, non validée**
- **f50 à f52 figés** jusqu'à validation de la liste par Julien. f53 complet (validé le 23/10).
- Entrées CPU : I0.0 AU pupitre, I0.1 AU armoire, I0.2 / I0.3 capots B1 / B2 (1 = ouvert), I0.4 Auto, I0.5 Manu, I0.6 / I0.7 / I1.0 / I1.1 fins de course, I1.2 / I1.3 retours KM1 / KM2, I1.4 retour KA2, I1.5 diagnostic KA1.
- Sorties CPU [D 30/10] : **PUL des 2 drivers en 100 kHz obligatoire** : Q0.0 PUL U3, Q0.2 PUL U4. Q0.1 DIR U3, Q0.3 DIR U4, Q0.4 ENA U3, Q0.5 ENA U4. Q0.6, Q0.7, Q1.0, Q1.1 réserve. Source : fiche Siemens 6ES7214-1AH50-0XB0 : Qa.0-Qa.3 100 kHz max, Qa.4-Qb.1 20 kHz max.
- SM 1223 : Q8.0-Q8.2 colonne, Q8.3 voyant S4, Q8.4 voyant H4 ; entrées en réserve ; alarme switch non câblée.
- Proposition détaillée (non validée) : `PROPOSITION_ES_AUTOMATE.csv` (ancien dossier local).

## PROFINET (f30) et pupitre (f45)
- K4 : P1 → K1 X1 P1 (f50), P2 → U1 X40 (f31), P3 → U2 X40 (f32), P4 → P1 X1 (f45), P5 réserve. Texte de destination sur chaque fil.
- Type de fil provisoire « Autre tension DC » en vert ; type « PROFINET » à créer dans WinRelais.
- Switch : V2+ / V2- (2e alimentation) non utilisée ; relais d'alarme ALM1 / ALM2 non câblé.
- f45 : on ne garde que l'IHM, alimentée par X71.21 (L+), .22 (M), .23 (FE).

## Borniers
- X70 (armoire ↔ machine) : en construction ; X70.1-4 B1, 5-8 B2, 9-16 fins de course.
- X71 (armoire ↔ pupitre) : 1-4 AU, 5-6 AU pupitre → automate, 7-20 sélecteur, 21-23 IHM.
- Méthode : `docs/local/METHODE_BORNIERS.md`. Sur f70 / f71 : description de la provenance du fil **des deux côtés** de la borne.
