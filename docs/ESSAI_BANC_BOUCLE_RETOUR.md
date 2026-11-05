# Essai de banc : boucle de retour (contacts miroirs) du relais de sécurité KA1

Fichier à lire par un nouveau chat Claude, pour aider Julien à faire l'essai au banc. Préparé le 05/11/2026.

## Pour le chat qui lit ce fichier
- Julien Thro, seul ingénieur BEBL. Réponds en français, phrases courtes, au plus 3-4 questions numérotées.
- **Aucune valeur inventée.** Ce qui n'est pas dans la notice ou constaté au banc s'écrit « à constater ».
- Lis d'abord `docs/references/XPSUAF13AP_base_connaissances_cablage.md` : §2 (bornes), §5 R-20 à R-23 (réarmement), §6.3 (schéma type), §13 (constats du 02/11).
- Contexte du schéma : `memoire/03_ARCHITECTURE.md` (sécurité). Folio 40 du schéma = relais KA1 et boucle Y1-Y2.
- À la fin : noter les constats dans le §13 de la base de connaissances et dans `memoire/05_POINTS_OUVERTS.md` (section « Essais de banc à prévoir »), puis `docs/JOURNAL_ECHANGES.md`, commit + push.

## Pourquoi cet essai
Sur la machine, la boucle Y1-Y2 de KA1 passe par un contact NF miroir de chaque contacteur commandé (KM1, KM2, KF1, KF2, KA2), puis par le bouton de réarmement S4 (NO). Règle R-22 : un contacteur resté collé garde son NF ouvert, et le réarmement doit être refusé.
On veut constater au banc :
1. qu'un réarmement normal fonctionne avec un NF miroir dans la boucle ;
2. qu'un NF ouvert (contacteur collé) empêche le réarmement ;
3. que l'ouverture du NF quand le contacteur colle (après le relâchement du bouton) ne gêne pas.

## Matériel
- Relais Schneider XPSUAF13AP.
- Alimentation 24 V CC (PELV).
- Un arrêt d'urgence à 2 contacts NF (ou 2 ponts S11-S12 / S21-S22 pour simplifier).
- Un bouton NO (S4 XB4BA21 ou tout bouton NO).
- Un contacteur Schneider LC1D09BD (bobine 24 V CC) : NF auxiliaire 21-22 = contact miroir (fiche Schneider, IEC 60947-4-1).
- Fils, embouts, multimètre. Option : un voyant 24 V CC sur une autre sortie.
- **Aucune tension de puissance** sur les pôles du contacteur : essai en 24 V seulement.

## Réglages du relais (hors tension)
FUNCTION 1, START 3 (réarmement surveillé, sur front descendant, bouton entre Y1 et Y2).

## Câblage du banc
```
+24 V ─ A1            A2 ─ 0 V            B2 ─ 0 V
S11 ─ NF1 (AU) ─ S12
S21 ─ NF2 (AU) ─ S22
+24 V ─ 13 ;  14 ─ A1 (bobine LC1D09BD) ;  A2 (bobine) ─ 0 V
Y1 ─ 21 (NF miroir LC1D09BD) ;  22 ─ bouton NO ─ Y2
Option : +24 V ─ 23 ;  24 ─ voyant + ;  voyant − ─ 0 V
```
Ne jamais alimenter Y2, S12 ou S22 depuis le +24 V (R-10, R-20).

## Essais
| N° | Action | Attendu | Constaté (à remplir) |
|---|---|---|---|
| E1 | Mise sous tension, AU déverrouillé, contacteur au repos | Sorties ouvertes, START éteinte (constat du 02/11) | |
| E2 | Appuyer sur le bouton et le garder enfoncé | START clignote ; sorties encore ouvertes ; contacteur au repos | |
| E3 | Relâcher le bouton | Sorties fermées, le contacteur colle, son NF s'ouvre ; le relais reste armé | |
| E4 | Appuyer sur l'AU | Sorties ouvertes, le contacteur retombe, son NF se referme | |
| E5 | Déverrouiller l'AU, appuyer puis relâcher le bouton | Réarmement accepté, comme E2 + E3 | |
| E6 | Après un AU (relais désarmé) : débrancher un fil du NF 21-22 (contacteur « collé »), appuyer puis relâcher le bouton | Réarmement **refusé** ; LED et comportement à constater | |
| E7 | Rebrancher le fil, appuyer puis relâcher | Réarmement accepté | |
| E8 | Relais désarmé : alimenter la bobine du contacteur par une source à part (débrancher A1 de 14, +24 V sur A1), puis bouton | Contacteur collé, NF ouvert → réarmement **refusé** | |

## Essais en plus, si le temps le permet (restants dans la base, §13)
| N° | Action | Attendu | Constaté |
|---|---|---|---|
| E9 | Pont permanent Y1-Y2 (bouton bloqué), puis AU / déverrouillage | À constater (R-23 : le réarmement agit sur le relâchement) | |
| E10 | Coupure puis retour de l'alimentation, relais armé avant | À constater (START 3 : pas de redémarrage seul attendu) | |
| E11 | Court-circuit S12-S22 | Erreur de court-circuit croisé (tableaux des LED et des trames Z1 de la base) | |

## Après l'essai
- Si E6 et E8 refusent le réarmement : la boucle de retour est validée. Le schéma (f40) reste tel quel.
- Si un essai ne donne pas l'attendu : décrire précisément (LED, ordre des actions) et ne rien modifier au schéma sans l'accord de Julien.
