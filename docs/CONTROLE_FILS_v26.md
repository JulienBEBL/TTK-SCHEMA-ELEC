# Contrôle de la logique des fils et câbles : schéma v26 (13/11/2026)

Demande de Julien (13/11) : revérifier tous les fils et câbles, sauf les E/S de l'automate (pas encore validées).
Méthode : liste des équipotentielles calculée sur le `.xrs` (fils, renvois, bornes traversées), relue appareil par appareil ;
contrôles `xrs_tool.py verifier` (0 erreur) et `xrs_chevauchements.py` (0).

## Conforme
| Partie | Chemin vérifié |
|---|---|
| Arrivée | W1 → X10.11 (PE) / X10.12 (N) / X10.13-15 (L1-L3) → QS1 → QF1 → bus f11 (L1-L3) et f12 (L1-L3, N) |
| 400 V moteurs | bus → QM1 → KM1 → U1 X1 ; bus → QM2 → KM2 → U2 X1 ; U1 / U2 X2 U V W PE → X31.11-14 / X32.11-14 → M1 / M2 ; R1 / R2 sur X2 +R / -R |
| Freins | L1 / L2 → QF2 → KF1 → X31.31-32 → M1 (2-3) ; L1 / L3 → QF3 → KF2 → X32.31-32 → M2 ; câble unique W4 |
| Sondes TF | M1 1b / 2b → X31.21-22 → U1 X10:1 / X10:2 ; idem M2 → U2 (bornes X10 toujours à confirmer par SEW) |
| 230 V | L1 → QF4 → T1, L1 → QF5 → T2, L2 / N → QF6 → T3 ; L3 / N → QF8 → EL1 / EL2, QF7 → EV1 / EV2, QF9 → QF10 → XD1 |
| 24 V | T1 +V = 24VSEC → X21.13 → FA1 et K2 3L+ ; T2 +V = 24VELEC → X21.11 → KA1 A1, K1, K2, K3, K4, P1, U1 / U2 X5, H3 ; 0 V commun T1 / T2 → X21.12 → toutes les références 0 V |
| PELV / PE | une seule liaison 0 V - PE, par X12.11 ; 0 V et PE séparés partout ailleurs ; PE : T1-T3, U1 / U2, M1 / M2, XD1, K1 FE, P1 FE, X10.11, W13 vers le bâti |
| Sécurité, voie 1 | KA1 S11 → S1 (1-2) → S2 (1-2) → B1 (11-12, shunté par MANU-A 3-4) → KA1 S12 |
| Sécurité, voie 2 | KA1 S21 → S1 (21-22) → S2 (21-22) → B2 (11-12, shunté par MANU-B 7-8) → KA1 S22 |
| Sorties KA1 | 24VSEC → FA1 → KA1 13 / 23 / 33 ; 14 → KF1 / KF2 A1 et MANU-D (15-16) → KA2 A1 ; 24 → AUTO-A (1-2) → KM1 / KM2 A1 ; 34 → AUTO-B (5-6) → U1 X6.1 |
| STO | U1 X6.2 au 0 V ; U1 X6.3 / X6.4 → U2 X6.1 / X6.2 ; U2 X6.3 / X6.4 libres |
| Boucle de retour | KA1 Y1 → KM1 21-22 → KM2 21-22 → KF1 21-22 → KF2 21-22 → KA2 21-22 → S4 (3-4) → KA1 Y2 |
| 48 V | T3 +V → KA2 1-2 → U3 +V et KA2 3-4 → U4 +V ; T3 -V → U3 / U4 -V ; U3 / U4 → X20.11-24 → M3 / M4 |
| PROFINET | K1 X1 P1 → K4 P1 ; K4 P2 → U1 X40, P3 → U2 X40, P4 → P1 IHM |
| Colonne, voyants | K2 Q8.0-8.2 → X61.11-13 → H1, COM au 0 V ; Q8.4 → X61.21 → H4 ; H3 sur 24VELEC (X21.21-22) |

## Corrigé en v26
- Fils des sondes TF : type « Commande 24VDC » → « Autre tension DC » (règle 20 de `04_REGLES_DESSIN.md`). Pas de changement de connexion.

## Points à décider par Julien
1. **H2 (voyant 230 V de porte)** : piqué directement sur L3 et N du bus 230 V, sans protection propre. Seul QF1 (20 A) le protège. Les fils de H2 (borne X12.21, porte) doivent alors tenir 20 A, ou bien H2 passe derrière un disjoncteur ou un fusible. Rien n'est modifié en attendant ta décision.
2. Hors périmètre (E/S automate, non validées) : rien n'a été relu en détail ; la liste des E/S reste `docs/LISTE_ES_AUTOMATE.md`.

## Connu et voulu (points d'attention du vérificateur)
- Fils en attente au f10 : arrivée client (au-dessus de W1), variante USA (TR1 non raccordé), W13 vers le bâti.
- Fils en attente au f21 : départs des barres 24VELEC / 0 V.
- Broches libres : KF1 / KF2 pôle 1-2, KA2 pôle 5-6, B2 33-34, contact AUTO-D (non dessiné), 2e borne +V / -V de T1 / T2, réserves automate.
