# 03 · Architecture électrique (état v6, 28/10)

## Puissance
- W1 → X11 → QS1 → QF1 → X12 (répartiteur) → départs.
- **f12 (400 V)** : QM1 / QM2 → KM1 / KM2 → U1 / U2. QF2 / QF3 → KF1 / KF2 → freins (alimentés côté CA, indépendamment du variateur).
- **f13 (230 V)** : QF4 / QF5 → T1 / T2 ; QF6 → T3 ; QF7 → EV1 / EV2 ; QF8 → EL1 / EL2 ; QF9 → QF10 → X14. Voyant H2 sur les départs libres 35 et N4.
- Phases au f13 : 24 V = L1, 48 V = L2, 230 V auxiliaires = L3 (notes du 23/10).
- Parafoudre **supprimé** [D 28/10].
- Moteurs, freins et TF **via le bornier X70** [D 28/10] : pas encore câblé aux f20 / f21 (v7).

## 24 V : deux alimentations, 0 V commun
| +24 V ELEC (T2, bornier X31) | +24 V COMMANDE (T1, bornier X33) |
|---|---|
| CPU K1 : L+ et sorties 3L+ (PUL / DIR / ENA des drivers) | KA1 13-14 → KF1, KF2 ; puis Manu-D → KM3 (48 V) |
| K2, K3 : L+ | KA1 23-24 → Auto-A → KM1, KM2 |
| Switch K4 | KA1 33-34 → Auto-B → STO de U1 / U2 |
| IHM P1 (X71.21) | K2 : sorties 3L+ → colonne H1, voyant S4, voyant H4 |
| KA1 : alimentation A1 | |
| U1 / U2 : X5 (24 V de sauvegarde) | |
| Voyant H3 | |

- **Répartition validée par Julien le 29/10** (« ok pour le tableau actuel »).
- **Renommage demandé le 29/10** : l'un des deux doit s'appeler **24VSEC**. Proposition : T1 (celui qui passe par les contacts de KA1) = 24VSEC. Nom de T2 à arrêter. [?]
- **Après un AU, les deux 24 V restent distribués.** L'AU ouvre les contacts de KA1 : bobines KM1, KM2, KM3, KF1, KF2 et STO perdent leur 24 V. Automate, IHM, switch, colonne et voyants restent alimentés (affichage du défaut). Seuls QS1 / QF1 / QF4 / QF5 coupent T1 / T2.
- 0 V commun (X32) [D 28/10] ; les deux +24 V ne sont **jamais** mis en parallèle. Liaison PELV unique 0 V – PE par la borne sectionnable X36.1 (f30).

## 48 V (f32)
- T3 → **KM3, 1 pôle sur le +48 V** → X34 → un fil par driver. 0 V 48 en direct T3 → X35 → un fil par driver [D 28/10].
- Bobine KM3 alimentée **uniquement en Manu** (Manu-D), depuis KA1 13-14 : le 48 V est coupé par l'AU et absent en Auto.

## Sécurité (f40 à f43), fiche de Julien du 27/10
- **KA1** XPSUAF13AP, cat. 0, PL d visé. Boucle de retour Y1-Y2 : NF miroir de KM1, KM2, KF1, KF2, KM3, puis S4.
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
| Manu-D | 83-84 | Manu | bobine KM3 | 19-20 |

| Sélecteur | Capot | AU | Freins | 48 V | KM1 / KM2 | STO |
|---|---|---|---|---|---|---|
| Auto | fermé | OK | alimentés | coupé | fermés | libéré |
| Auto | ouvert | OK | coupés | coupé | coupés | actif |
| Manu | ouvert ou fermé | OK | alimentés | alimenté | coupés | actif |
| tous | tous | enfoncé | coupés | coupé | coupés | actif |

Risques résiduels : sélecteur sans clé (capot shunté en Manu, choix du client) ; roue libre si le sélecteur tourne pendant la rotation (≈ 10 s, à mesurer) ; un seul contact Manu-D pour le 48 V (PL c accepté).

## Automate (f50 à f53) : liste d'E/S du 06/10, **gelée, non validée**
- **f50 à f52 figés** jusqu'à validation de la liste par Julien. f53 complet (validé le 23/10).
- Entrées CPU : I0.0 AU pupitre, I0.1 AU armoire, I0.2 / I0.3 capots B1 / B2 (1 = ouvert), I0.4 Auto, I0.5 Manu, I0.6 / I0.7 / I1.0 / I1.1 fins de course, I1.2 / I1.3 retours KM1 / KM2, I1.4 retour KM3, I1.5 diagnostic KA1.
- Sorties CPU : Q0.0-Q0.2 PUL / DIR / ENA U3, Q0.4-Q0.6 U4 ; Q0.3, Q0.7, Q1.0, Q1.1 réserve.
- SM 1223 : Q8.0-Q8.2 colonne, Q8.3 voyant S4, Q8.4 voyant H4 ; entrées en réserve ; alarme switch non câblée.
- Proposition détaillée (non validée) : `PROPOSITION_ES_AUTOMATE.csv` (ancien dossier local).

## PROFINET (f54) et pupitre (f60)
- K4 : P1 → K1 X1 P1 (f50), P2 → U1 X40 (f20), P3 → U2 X40 (f21), P4 → P1 X1 (f60), P5 réserve. Texte de destination sur chaque fil.
- Type de fil provisoire « Autre tension DC » en vert ; type « PROFINET » à créer dans WinRelais.
- f60 : on ne garde que l'IHM, alimentée par X71.21 (L+), .22 (M), .23 (FE).

## Borniers
- X70 (armoire ↔ machine) : en construction ; X70.1-4 B1, 5-8 B2, 9-16 fins de course.
- X71 (armoire ↔ pupitre) : 1-4 AU, 5-6 AU pupitre → automate, 7-20 sélecteur, 21-23 IHM.
- Méthode : `docs/local/METHODE_BORNIERS.md`. Sur f70 / f71 : description de la provenance du fil **des deux côtés** de la borne.
