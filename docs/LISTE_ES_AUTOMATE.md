# Liste des E/S de l'automate (schéma v34, 18/11/2026) : validée par Julien le 05/11, fins de course B3-B6 en NF depuis la v32

Vue d'ensemble pour validation par Julien (point 14 de `memoire/05_POINTS_OUVERTS.md`). Source : tableaux des f60 à f63 du script.
Numéros de folio = numéros affichés. « 1 » = signal présent (24 V sur l'entrée, sortie active).

## K1 : CPU 1214C G2 (6ES7214-1AH50-0XB0), f60 / f61
### Entrées TOR (14)
| Entrée | Repère | Fonction | Par les bornes |
|---|---|---|---|
| I0.0 | S2 | AU pupitre actionné (contact NO) | X60.11-12 (27G1) |
| I0.1 | S1 | AU armoire actionné (contact NO) | X60.41-42 (porte) |
| I0.2 | B1 | Capot ouvert, capteur mécanique (contact aux. 23-24) | X41.33-34 (19G1) |
| I0.3 | B2 | Capot ouvert, capteur magnétique (contact aux. 23-24) | X41.43-44 (câble M12) |
| I0.4 | S3 | Mode Auto (AUTO-C, 9-10) | X60.21-22 (27G1) |
| I0.5 | S3 | Mode Manu (MANU-C, 11-12) | X60.23-24 (27G1) |
| I0.6 | B3 | Fin de course axe 1 min (NF, 0 = atteinte, 18/11) | X60.31-32 (19G1) |
| I0.7 | B4 | Fin de course axe 1 max (NF) | X60.33-34 (19G1) |
| I1.0 | B5 | Fin de course axe 2 min (NF) | X60.35-36 (19G1) |
| I1.1 | B6 | Fin de course axe 2 max (NF) | X60.37-38 (19G1) |
| I1.2 | KM1 | Retour contacteur amont variateur 1 (aux. NO) | interne |
| I1.3 | KM2 | Retour contacteur amont variateur 2 (aux. NO) | interne |
| I1.4 | KA2 | Retour contacteur 48 V (aux. NO) | interne |
| I1.5 | KA1 | Diagnostic du relais de sécurité (Z1, trames, non sécuritaire) | interne |

### Sorties TOR (10)
| Sortie | Repère | Fonction |
|---|---|---|
| Q0.0 | U3 | PUL axe 1 (100 kHz) |
| Q0.1 | U3 | DIR axe 1 |
| Q0.2 | U4 | PUL axe 2 (100 kHz) |
| Q0.3 | U4 | DIR axe 2 |
| Q0.4 | U3 | ENA axe 1 (1 = moteur libre, 0 = driver actif) |
| Q0.5 | U4 | ENA axe 2 (1 = moteur libre, 0 = driver actif) |
| Q0.6, Q0.7, Q1.0, Q1.1 | | réserve |

## K2 : SM 1223 G2 (6ES7223-5BH50-0XB0), f62
| E/S | Repère | Fonction |
|---|---|---|
| I8.0 à I8.7 | | réserve (alarme du switch non câblée) |
| Q8.0 | H1 | Colonne rouge (X62.11) |
| Q8.1 | H1 | Colonne orange (X62.12) |
| Q8.2 | H1 | Colonne verte (X62.13) |
| Q8.3 | | réserve (ancien voyant de S4) |
| Q8.4 | H4 | Voyant porte « défaut machine » (X62.21-22) |
| Q8.5 à Q8.7 | | réserve |

## K3 : SM 1231 TC G2 (6ES7231-5QF50-0XB0), f63
| Voie | Repère | Fonction |
|---|---|---|
| AI0 | B7 | Thermocouple type K, température Microdia (bornes X63.11-12, câble W8) |
| AI1 à AI7 | | réserve |

## Bilan
| Module | Utilisé | Réserve |
|---|---|---|
| CPU entrées | 14 / 14 | 0 |
| CPU sorties | 6 / 10 | 4 |
| SM 1223 entrées | 0 / 8 | 8 |
| SM 1223 sorties | 4 / 8 | 4 |
| SM 1231 TC | 1 / 8 | 7 |

Les entrées de la CPU sont toutes prises : une nouvelle entrée ira sur la SM 1223 (I8.x).
Hors E/S : PROFINET (switch K4) vers U1, U2 (variateurs), P1 (IHM) ; la commande des moteurs SEW passe par PROFINET, pas par des E/S.

## Mise à jour du 16/11/2026 (v28)
- 24 V des capteurs : L+ capt de la CPU (24 V, 400 mA max, protégé) → bloc PTFIX 6/12 **noir -X21.14** (R3, f21) → 12 départs, un fil par point (S1 13, S2 13, S3 9 et 11, B1 23, B2 23, B3 à B6 11 (NF, 18/11), KA2 13, KM1 13 + KM2 13 par un pont). Potentiel **6001**.
- Colonne H1 et voyant H4 dessinés au f62 avec la SM 1223 ; bornes **X62.11-14** (H1) et **X62.21-22** (H4), ex-X61.
- Tableaux f60 / f61 / f62 vérifiés contre les liaisons : conformes. Corrigé : B1 / B2 « contact aux. 23-24 » (le tableau disait NO / NF) ; f61 « SM 1223 : colonne, voyant défaut » (l'alarme switch n'est pas câblée).
