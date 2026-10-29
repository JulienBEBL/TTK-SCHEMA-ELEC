# 01 · Projet

## Machine
- **Machine de tressage TTK** : tresse du caoutchouc autour d'un câble, en ligne avec une tête d'extrusion Microdia (hors périmètre, sauf la mesure de sa température).
- **Client** : TTK (Nicolas Ghut). **N° machine** : 001-EU. **Affaire** : inconnue (laissée vide).
- **Réseau UE** : 400 V 3P+N+PE, **TN-S**, **Icc 6 kA** (page de garde).
- **Variante US** : transformateur TEMCo 15 kVA hors armoire, fourni par BEBL, installé par le client (TR1 dessiné en variante au f10).
- **Pas de marquage CE** (accepté par le client). Normes en bonne pratique : IEC 60204-1, EN ISO 13849-1, 13850, 14119, 14118, 12100.

## Fonctionnement
- 2 motoréducteurs SEW (2,2 kW, frein BE5 400 V CA, sonde TF), chacun avec son variateur MCX91A (STO, PROFINET). Sens opposés, vitesses indépendantes 30 à 137 tr/min.
- **Mode Auto (production)** : ouverture du capot = AU.
- **Mode Manu (nettoyage)** : moteurs SEW jamais alimentés ; translation de chaque motoréducteur par un pas-à-pas (DM860H en 48 V, Nema 34), un axe à la fois, commande maintenue depuis l'IHM ; capot libre.

## Localisations
| Code | Lieu |
|---|---|
| +A1 | Armoire IDE 1800 × 1200 × 400 |
| +P1 | Pupitre posé sur la machine (IHM KTP700, AU, sélecteur Auto/Manu) |
| +M | Machine |

## Personnes
| Nom | Rôle |
|---|---|
| Julien Thro (THRO.J) | Seul ingénieur BEBL : schéma, achats, câblage, programme, essais. Il décide. |
| Nicolas | Dirigeant de BEBL |
| Nicolas Ghut | Client TTK |
| Hugo | Commandes (Levert Industrie) |
| Julien Rimoux | Installation électrique du site client |
| Samir (WAGO) | Équivalences borniers |
| 2 amis | Relecteurs le soir (électricien, automaticien) |
| 2 stagiaires | Câblage de l'armoire |

## Planning (validé le 20/10)
| Jalon | Date |
|---|---|
| J1 folios terminés | 05/11/2026 |
| J2 bon pour câblage | 13/11/2026 |
| J3 armoire 1 sous tension | 26/11/2026 |
| J4 moteurs pilotés | 28/11/2026 |
| J5 programme | 14/12/2026 |
| J6 machine 1 testée | 23/12/2026 |

Livraison machine 1 au plus tard le 22/01/2027.

## Logiciels
- Schéma : **WinRelais 2.6b Expert**.
- Automate : Siemens S7-1200 **G2**, **TIA Portal V21 Basic**. Julien n'a jamais programmé d'automate en conditions réelles.
