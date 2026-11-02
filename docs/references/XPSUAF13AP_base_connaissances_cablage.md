# XPSUAF13AP — base de connaissances pour le câblage

Document de référence pour l'agent de schéma électrique. Il décrit le relais de sécurité Schneider Electric Preventa **XPSUAF13AP** : bornes, fonctionnement, réglages, règles de câblage, choix possibles et application au projet TTK.

Date : 02/11/2026. Auteur : BEBL (Julien).

## 0. Mode d'emploi pour l'agent

- Chaque donnée porte sa source. N'utilise que ces données. Ne complète jamais une valeur manquante par une estimation.
- Les règles **R-xx** (§5) sont impératives. Les options (§7) sont à soumettre à Julien avec leurs risques, jamais à trancher seul.
- Si une demande de câblage contredit une règle, signale-le explicitement avant de dessiner.
- Les points marqués **[à confirmer]** ne doivent pas être présentés comme acquis.

Sources :

| Code | Document | Fiabilité pour le XPSUAF13AP |
|---|---|---|
| [N] | Notice d'instructions PHA7184208 (11/2020), XPSUAF•3A• | Référence. Tableaux vérifiés visuellement |
| [F] | Fiche technique XPSUAF13AP (06/05/2022) | Bonne |
| [U] | Guide utilisateur EIO0000003454 (11/2020) | **Produit XPSUAB, pas XPSUAF.** Valable seulement pour le comportement commun à la gamme XPSU. Toujours [à confirmer] |
| [B] | Essais au banc BEBL du 02/11/2026 | Constaté sur le relais réel |
| [TTK] | Décisions du projet TTK | Acquis projet, à recouper avec le schéma en cours |

## 1. Identification

| Élément | Valeur | Source |
|---|---|---|
| Fabricant, gamme | Schneider Electric, Preventa XPSU (Harmony) | [F] |
| Référence | XPSUAF13AP : alimentation 24 V CA/CC, bornes à vis débrochables | [N] p.2 |
| Variantes | XPSUAF13AC (bornes à ressort), XPSUAF33AP / 33AC (48…240 V CA/CC) | [N] p.2 |
| Entrées de sécurité | 2 entrées monocanal : S11-S12 et S21-S22 | [N] p.6 |
| Sorties de sécurité | 3 contacts NO instantanés : 13-14, 23-24, 33-34 | [N] p.4, p.6 |
| Entrée démarrage (réarmement) | Y1 (DC+) / Y2 (CH+) | [N] p.4 |
| Sortie diagnostic | Z1, statique pulsée, non sécuritaire | [N] p.4, p.7 |
| Extension | Connecteur latéral EXT pour module XPSUEP•4A• (sorties supplémentaires) | [N] p.6 |
| Sorties temporisées | Aucune | [N] |

## 2. Bornes

| Borne | Rôle | Bornier | Remarque |
|---|---|---|---|
| A1 | Alimentation + (24 V) | haut | |
| A2 | Alimentation − (0 V) | bas | |
| S11 | Sortie DC+ de la voie 1, porte les impulsions de test | haut | Source de la voie 1 |
| S12 | Entrée CH+ de la voie 1 | haut | LED S12 |
| S21 | Sortie DC+ de la voie 2, porte les impulsions de test décalées | bas | Source de la voie 2 |
| S22 | Entrée CH+ de la voie 2 | bas | LED S22 |
| Y1 | Sortie DC+ de l'entrée démarrage, dynamisée selon START | haut | |
| Y2 | Entrée CH+ de démarrage | haut | LED START |
| B2 | Potentiel de référence commun des signaux 24 V CC | bas | |
| Z1 | Sortie de diagnostic pulsée, 24 V CC, 20 mA max | bas | Non sécuritaire |
| 13-14, 23-24, 33-34 | Contacts NO de sécurité (relais K1/K2 internes) | 13, 23, 33 en haut ; 14, 24, 34 en bas | Contacts secs |

Disposition des borniers [N] p.2 :

```
Bornier haut :  A1  13  23  33
                Y1  Y2  S11 S12
Bornier bas  :  B2  Z1  S21 S22
                A2  14  24  34
```

Les deux rangées de chaque bornier sont reprises du dessin de la notice. Les repères imprimés sur le relais font foi.

Piège constaté : S11-S12 (haut) et S21-S22 (bas) occupent la même position sur leur bornier. Une inversion de bornier est facile.

## 3. Fonctionnement

### 3.1 États

| État | Sorties NO | Indication |
|---|---|---|
| Initialisation (autotest, 2 500 ms) | ouvertes | toutes les LED brièvement |
| Attente | ouvertes | POWER ; S12 / S22 selon les voies |
| Attente du relâchement du bouton (démarrage surveillé) | ouvertes | START clignote [B] |
| Marche | fermées | STATE fixe |
| Alerte | ouvertes | ERROR clignote |
| Erreur | ouvertes | ERROR fixe |

Sources : [N] p.5, p.7 ; [U] p.29 ; [B].

### 3.2 Conditions de fermeture des sorties

Toutes les conditions suivantes doivent être réunies :
1. Alimentation correcte et initialisation terminée.
2. Voies 1 et 2 actives : S12 et S22 alimentées par S11 et S21, au travers de contacts fermés.
3. Condition de démarrage remplie. En START 3, il s'agit d'un front descendant sur Y2 après un appui d'au moins 80 ms.
4. Aucune alerte ni erreur.

Les sorties se ferment au plus 100 ms après la dernière condition [N] p.7.

### 3.3 Ouverture des sorties

| Cause | Temps max | Source |
|---|---|---|
| Ouverture d'une voie, ou des deux | 20 ms | [N] p.7, [F] |
| Coupure de l'alimentation (24 V CC) | 120 ms | [N] p.7 |
| Coupure de l'alimentation (24 V CA) | 200 ms | [N] p.7 |

Après une ouverture de voie, il faut un temps de rétablissement de 200 ms avant que l'entrée puisse être réactivée [N] p.7.

### 3.4 Mécanismes de surveillance

- **Dynamisation** : S11, S21 et Y1 émettent des impulsions de test de 2 ms toutes les 500 ms. Les impulsions de S11 et S21 sont décalées d'au moins 70 ms. Le relais détecte ainsi :
  - un court-circuit entre les deux voies ;
  - un court-circuit entre une voie et l'entrée démarrage ;
  - un court-circuit vers une alimentation externe ou vers la masse.

  Actif selon la fonction choisie [N] p.2, p.6.
- **Synchronisation** : les deux voies doivent s'activer dans un délai donné. Ce contrôle existe en fonctions 2, 3, 5 et 6 [N] p.2, p.6.
- **Verrouillage (« interlock »)** : les deux voies doivent se désactiver ensemble. Si une seule s'ouvre, le relais suppose un contact soudé sur l'autre voie. Il lève une alerte et bloque le réarmement.
  - Le délai de 200 ms et la sortie de l'alerte (deux voies ouvertes au moins 1 s) viennent de [U] p.36.
  - **Constaté en fonction 1 au banc [B]** : l'ouverture d'une seule voie lève l'alerte ; elle s'efface en ouvrant puis refermant les deux voies.

### 3.5 Alerte et erreur

| Type | LED ERROR | Sortie de l'état |
|---|---|---|
| Alerte (synchronisation, verrouillage) | clignote | Supprimer la cause, en général ouvrir puis refermer les deux voies [U] p.62, [B] |
| Erreur (court-circuit croisé, configuration, alimentation, sortie) | fixe | Supprimer la cause **puis couper et rétablir l'alimentation** [U] p.63 [à confirmer] |

## 4. Sélecteurs

Les réglages ne sont lus qu'à la mise sous tension. Une modification sous tension provoque une erreur de configuration. Après réglage, fermer le capot transparent et le plomber [N] p.3, [U] p.58-59.

### 4.1 Sélecteur FUNCTION (5)

| Pos. | Application | Signal attendu | Bornes | Synchro (s) | Dynamisation | Anti-rebond |
|---|---|---|---|---|---|---|
| **1** | AU, catégorie d'arrêt 0 ; interrupteurs de position | NC, NO, C/O | S11–S12 / S21–S22 | — | Oui | Non |
| 2 | AU ; interrupteurs de position | NC, NO, C/O | S11–S12 / S21–S22 | 2 (S12 puis S22) / 4 (S22 puis S12) | Oui | Non |
| 3 | Interrupteur magnétique codé (NC + NO, antivalent) | NC, NO, C/O | S11–S12 / S21–S22 | 0,5 | Oui | Non |
| 4 | 2 capteurs PNP | PNP | S12 / S22 | — | Non | Non |
| 5 | 2 capteurs PNP | PNP | S12 / S22 | 0,5 | Non | Non |
| 6 | Barrière immatérielle type 4 (OSSD) | OSSD | S12 / S22 | 0,5 | Non | Oui (4 ms) |

Source : [N] p.2, p.6. L'exemple de câblage AU de la notice correspond aux positions 1 et 2 [N] p.4.

### 4.2 Sélecteur START (4)

| Pos. | Démarrage | Test au démarrage | Dynamisation Y1 | Usage typique |
|---|---|---|---|---|
| 1 | manuel ou automatique selon câblage Y | non | oui | Automatique (pont Y1–Y2) : essais uniquement |
| 2 | manuel ou automatique | oui | oui | Protecteur |
| **3** | **surveillé, front descendant** | non | oui | **Bouton de réarmement câblé sur Y1–Y2** |
| 4 | surveillé, front descendant | oui | oui | Bouton + protecteur |
| 5 | manuel ou automatique | non | non | Signal externe |
| 6 | manuel ou automatique | oui | non | Signal externe + protecteur |
| 7 | surveillé, front descendant | non | non | **Réarmement par automate sur Y2** |
| 8 | surveillé, front descendant | oui | non | Automate + protecteur |

Source : [N] p.3. Le test au démarrage impose d'ouvrir puis refermer les entrées après chaque mise sous tension [U] p.54-55.

Avertissement Schneider [N] p.3 : la fonction démarrage n'est pas une fonction de sécurité. Si un redémarrage intempestif est un danger, utiliser le démarrage surveillé ou le test au démarrage.

### 4.3 Réglage retenu pour un AU à bouton de réarmement

**FUNCTION 1, START 3.** Validé au banc [B].

## 5. Règles de câblage

### Alimentation

- **R-01** Alimenter A1 / A2 en 24 V CC (−20 % / +20 %) ou 24 V CA (−15 % / +10 %), par une source **PELV** selon IEC 60204-1 [N] p.1, p.6.
- **R-02** Raccorder B2 au 0 V de l'alimentation 24 V PELV dès qu'un signal externe arrive sur Y2, ou que Z1 est relié à un automate. Toutes les alimentations des équipements raccordés doivent partager ce potentiel [N] p.6, [U] p.42-43. Recommandé dans tous les cas.
- **R-03** Protéger l'alimentation A1 selon l'installation. La notice ne donne pas de calibre. La consommation est de 2,0 W en 24 V CC [N] p.6.

### Entrées de sécurité

- **R-10** En fonctions 1, 2 et 3, chaque voie part de **sa propre** sortie DC+ : S11 pour la voie 1, S21 pour la voie 2. Ne jamais alimenter S12 ou S22 depuis un +24 V externe : la dynamisation le détecte comme un court-circuit [N] p.4, p.6.
- **R-11** Chaque organe de sécurité (AU, interrupteur de protecteur) doit ouvrir **les deux voies**. Un AU porte donc deux contacts NC à manœuvre positive d'ouverture, un par voie [B], [U] p.36.
- **R-12** Interdit : un organe sur la voie 1 et un autre organe sur la voie 2. Chaque organe n'ouvrirait qu'une voie, ce qui lève l'alerte de verrouillage et supprime la redondance [B].
- **R-13** Plusieurs organes sur une même entrée se câblent **en série, voie par voie** :
  - voie 1 : S11 → NC1 organe A → NC1 organe B → … → S12 ;
  - voie 2 : S21 → NC2 organe A → NC2 organe B → … → S22.
- **R-14** Les deux voies ne doivent jamais être reliées entre elles, même par un shunt de mode : un contact shunte la voie 1, un autre contact distinct shunte la voie 2.
- **R-15** Résistance de boucle de chaque voie : 500 Ω max [N] p.6. Sans utiliser S11 / S21, la longueur max est de 30 m [U] p.42.
- **R-16** Si deux organes de technologies différentes surveillent un même protecteur, par exemple un interrupteur mécanique sur une voie et un magnétique sur l'autre, leur ouverture doit rester quasi simultanée. Un écart supérieur à 200 ms lève l'alerte de verrouillage [U] p.36. Comportement à vérifier au banc [à confirmer].

### Démarrage (réarmement)

- **R-20** Bouton de réarmement : contact **NO** entre Y1 et Y2, avec START 3. Ne pas l'alimenter depuis le +24 V : c'est Y1 qui l'alimente [U] p.42, [B].
- **R-21** Réarmement par automate : sortie TOR de l'automate sur Y2 seul, Y1 libre, B2 au 0 V commun, START 7. Les positions 1 à 4 dynamisent Y1 et ne conviennent pas à un signal d'automate [U] p.42, p.55.
- **R-22** Contrôle des contacteurs commandés (boucle de retour) : le XPSUAF n'a pas d'entrée dédiée. Câbler un contact NC miroir de chaque contacteur commandé **en série avec le bouton de réarmement**, entre Y1 et Y2. Un contacteur resté collé empêche alors tout réarmement. Schneider renvoie à ses exemples « Safety Chain Solutions » pour ce câblage [U] p.40. Vérifier sur la fiche du contacteur que le NC auxiliaire est bien un contact miroir [à confirmer].
- **R-23** Placer le bouton de réarmement avec vue sur la zone dangereuse. Le réarmement agit sur le relâchement : un bouton bloqué qui se débloque réarme la machine [B].

### Sorties de sécurité

- **R-30** Les sorties 13-14, 23-24 et 33-34 sont des **contacts secs** à potentiel libre. Câblage type : + de l'alimentation de la charge → 13, puis 14 → charge → retour. Les trois contacts commutent ensemble.
- **R-31** Charge par contact : 3 A en DC-13 (24 V) ou AC-15 (250 V), 5 A en DC-1 ou AC-1. Courant permanent max : 6 A [N] p.6 (8 A selon [F], voir §12).
- **R-32** Charge **minimale** : 10 mA et 15 V par contact [N] p.6, [F]. Une entrée d'automate ou une entrée STO peut consommer moins de 10 mA. Vérifier le courant de chaque charge de faible puissance avant de la câbler seule sur un contact.
- **R-33** Fusible en amont des contacts : gG **10 A max** [N] p.6, [F]. Le courant de court-circuit conditionnel est de 1 kA [N] p.6.
- **R-34** Charges inductives, comme les bobines de contacteur : la catégorie DC-13 couvre ce cas. Le nombre de cycles diminue avec le courant (§10).
- **R-35** Besoin de plus de 3 contacts : utiliser le module d'extension XPSUEP•4A•, raccordé hors tension sur le connecteur EXT [N] p.6. Référence exacte et caractéristiques [à confirmer] sur sa propre fiche.
- **R-36** État sûr : sorties désexcitées, contacts NO ouverts [N] p.5. Chaque fonction commandée doit donc être **à sécurité positive** : bobine alimentée pour autoriser, retombée par ressort pour arrêter.

### Diagnostic et montage

- **R-40** Z1 n'est pas sécuritaire. Ne jamais l'utiliser dans une chaîne de sécurité [N] p.7. C'est une sortie statique de 24 V CC, 20 mA max, à relier à une entrée d'automate, longueur max 30 m [U] p.42. Son codage par trames est décrit au §9.
- **R-41** Montage sur rail DIN 35 × 15 ou 35 × 7,5, ou par vis M4 à 113 mm d'entraxe [N] p.4. À installer dans une enveloppe IP54 min, fermée à clé ou à l'outil [N] p.7, [U] p.38.
- **R-42** Conducteurs cuivre 75 °C [U] p.40 :
  - 1 fil : 0,2 à 2,5 mm² ;
  - 2 fils dans un embout double isolé : 0,5 à 1,5 mm² ;
  - dénudage 7 à 8 mm, couple 0,5 à 0,6 N·m, tournevis de 3,5 mm [N] p.2.

## 6. Schémas types (netlists)

### 6.1 AU seul, réarmement par bouton (validé au banc)

```
+24V ─ A1          A2 ─ 0V
S11 ─ NC1(AU) ─ S12
S21 ─ NC2(AU) ─ S22
Y1 ─ NO(bouton réarmement) ─ Y2
+24V ─ 13 ; 14 ─ voyant + ; voyant − ─ 0V
FUNCTION 1, START 3
```

### 6.2 Plusieurs organes en série

```
S11 ─ NC1(AU-A) ─ NC1(AU-B) ─ NC1(protecteur) ─ S12
S21 ─ NC2(AU-A) ─ NC2(AU-B) ─ NC2(protecteur) ─ S22
```

### 6.3 Réarmement avec contrôle des contacteurs

```
Y1 ─ NC miroir(KMa) ─ NC miroir(KMb) ─ … ─ NO(bouton) ─ Y2
```

Tous les contacteurs de la boucle doivent être retombés quand on réarme. Sinon, réarmement impossible.

### 6.4 Réarmement par automate

```
Sortie TOR API ─ Y2      Y1 libre      B2 ─ 0V commun API
START 7
```

### 6.5 Sortie vers bobine de contacteur

```
+24V ─ F(gG ≤ 10 A) ─ 23 ; 24 ─ A1 bobine KM ; A2 bobine KM ─ 0V
```

## 7. Choix de câblage à soumettre

| Choix | Option | Risque ou limite |
|---|---|---|
| Information « AU actionné » vers l'automate | NO supplémentaire sur chaque AU vers une entrée TOR | Aucun : solution recommandée |
| | Contact de sortie du relais vers une entrée TOR | Courant d'entrée de l'automate souvent inférieur à 10 mA (R-32), et consomme une sortie de sécurité |
| | Z1 vers une entrée de l'automate | Trames à décoder. La bibliothèque PreventaSupport est éditée pour automates Schneider, compatibilité S7 [à confirmer] |
| | Contact auxiliaire de contacteur vers une entrée TOR | Indique l'état réel du contacteur, mais pas la cause de l'arrêt |
| Réarmement | Bouton sur Y1–Y2, START 3 | Simple. Bouton avec vue sur la zone |
| | Automate sur Y2, START 7 | Réarmement logiciel, non sécuritaire. Câblage de B2 obligatoire |
| Plus de 3 charges | Plusieurs charges en parallèle sur un contact | Somme des courants ≤ 3 A en DC-13. Une même sortie commande alors toutes ces charges |
| | Module d'extension XPSUEP•4A• | Coût, place sur le rail |
| | Relais de recopie | Doit lui-même être de sécurité (contacts guidés) et surveillé |
| Organes sur un protecteur | 2 NC du même interrupteur | Même technologie, ouverture simultanée |
| | Interrupteur mécanique (voie 1) + magnétique (voie 2) | Diversité utile, mais alerte possible si l'écart dépasse 200 ms (R-16) |

## 8. Diagnostic par LED

| LED | État | Signification |
|---|---|---|
| POWER | fixe / éteinte | Alimentation présente / absente |
| S12, S22 | fixe / éteinte | Voie active / ouverte |
| START | éteinte | Pas de condition de démarrage [N] ; au repos en START 3 [B] |
| START | clignote | En attente : en START 3, bouton enfoncé, relâchement attendu [B] |
| STATE | fixe / éteinte | Contacts NO fermés / ouverts |
| ERROR clignote + S12, S22 en alternance | | Alerte de temps de synchronisation |
| ERROR clignote + S12, S22 en synchrone | | Alerte de verrouillage : une seule voie ouverte [B] |
| ERROR fixe + toutes LED (sauf POWER) clignotent | | Erreur générale |
| ERROR fixe + toutes LED (sauf POWER) fixes | | Erreur de configuration : sélecteur modifié sous tension |
| ERROR fixe + POWER clignote | | Défaut d'alimentation |
| ERROR fixe + S12, S22 clignotent en synchrone | | Court-circuit croisé sur une entrée de sécurité |
| ERROR fixe + START clignote | | Court-circuit croisé sur l'entrée démarrage |
| ERROR fixe + STATE clignote | | Défaut sur une sortie de sécurité |
| ERROR fixe + START et STATE clignotent | | Défaut sur une sortie du module d'extension |

Source : [N] p.5, sauf mention [B].

## 9. Codes de diagnostic Z1 [U] p.64-65, [à confirmer pour XPSUAF]

Trame de 10 bits de 200 ms chacun, soit 2 s au total. Les 4 premiers bits valent toujours `0010`, les 6 suivants portent le code.

| Trame | Type | Signification |
|---|---|---|
| 0010101101 | Erreur | Tension d'alimentation hors tolérance |
| 0010000011 | Erreur | Erreur générale |
| 0010000111 | Erreur | Erreur de configuration |
| 0010001100 | Erreur | Court-circuit croisé sur l'entrée S12 |
| 0010001101 | Erreur | Court-circuit croisé sur l'entrée S13 (XPSUAB ; équivalent S22 non documenté) |
| 0010110000 | Erreur | Court-circuit croisé sur l'entrée démarrage |
| 0010110011 | Alerte | Synchronisation : une entrée reste désactivée après le temps imparti |
| 0010100111 | Alerte | Synchronisation : entrées activées hors délai |
| 0010110111 | État | Entrées et sorties désactivées |
| 0010110101 | État | Changement d'état attendu sur S12 |
| 0010110100 | État | Changement d'état attendu sur la seconde entrée |
| 0010101011 | État | Attente du test au démarrage |
| 0010101010 | État | Attente du front montant de démarrage |
| 0010101110 | État | Démarrage activé, attente du front descendant |
| 0010101111 | État | Marche, sorties fermées |

## 10. Données techniques

| Paramètre | Valeur | Source |
|---|---|---|
| Consommation | 2,0 W (24 V CC) / 5,0 VA (24 V CA) | [N] p.6, [F] |
| Tension DC+ (S11, S21, Y1) | > 15 V CC | [N] p.6 |
| Seuils CH+ | activation > 15 V, désactivation < 5 V | [N] p.6 |
| Anti-rebond | 2,5 ms (standard), 4 ms (OSSD) | [N] p.6 |
| Retard à la mise sous tension | 2 500 ms | [N] p.7 |
| Durée min de l'appui de réarmement (START 3) | 80 ms | [N] p.7 |
| Catégorie de surtension, degré de pollution | II, 2 | [N] p.6 |
| Uimp | 4 kV | [N] p.6, [F] |
| Température de fonctionnement | −25 à 55 °C, sans givre | [N] p.7 |
| Altitude max | 2 000 m | [N] p.7 |
| Dimensions, masse | 22,5 × 99 × 117 mm, 0,2 kg | [N] p.6 |

Nombre de cycles max sur la durée de vie [N] p.5 :

| DC-13 24 V 1 A | DC-13 24 V 3 A | AC-1 250 V 4 A | AC-15 250 V 1 A | AC-15 250 V 3 A |
|---|---|---|---|---|
| 1 200 000 | 180 000 | 180 000 | 70 000 | 39 000 |

## 11. Sécurité fonctionnelle

| Paramètre | Valeur | Source |
|---|---|---|
| PL / catégorie max | PL e, cat. 4 (ISO 13849-1:2015) | [N] p.5, [F] |
| SIL / SILCL max | 3 / 3 | [N] p.5, [F] |
| PFHd | 1,13 × 10⁻⁹ /h | [N] p.5, [F] |
| MTTFd / DCavg | > 30 ans (haut) / ≥ 99 % | [N] p.5 |
| HFT / SFF / type | 1 / > 99 % / B | [N] p.5 |
| Catégorie d'arrêt AU | 0 | [N] p.5 |
| Durée de vie | 20 ans à 55 °C | [N] p.5 |

Ces valeurs sont des maximums. Le niveau réellement atteint dépend du câblage, des organes d'entrée, des contacteurs et de leur surveillance [N] p.5.

## 12. Incohérences documentaires

1. [U] concerne le XPSUAB : 1 entrée S11-S12-S13, 1 inverseur 11-12-14, PL c cat. 1, fusible 6 A, DC-13 2 A, tension min 12 V. Ne jamais reporter ces valeurs sur le XPSUAF.
2. Courant permanent : 6 A [N] contre Ith 8 A [F]. Retenir 6 A.
3. Tension d'isolement : 300 V [N] contre Ui 250 V [F]. Retenir 250 V.
4. Durée de 80 ms en démarrage surveillé : une note de [N] p.3 l'applique aux entrées de sécurité, le tableau des temps [N] p.7 l'applique à l'impulsion de démarrage. Retenir l'impulsion de démarrage.
5. Stockage : −25 à 85 °C [F] (valeur de transport dans [N]) contre −40 à 70 °C [N]. Retenir [N].
6. Verrouillage : [N] le liste dans les LED sans préciser les fonctions concernées. Il est actif en fonction 1 [B].

## 13. Constats de banc (02/11/2026, FUNCTION 1, START 3, 24 V CC)

| Essai | Constat |
|---|---|
| Ponts S11–S12, S21–S22, Y1–Y2, START 1 | Sorties fermées environ 2,5 s après la mise sous tension. Retrait d'un pont : ouverture. Remise : refermeture automatique |
| Bouton NO sur Y1–Y2, START 3 | Au repos, START éteinte. Bouton enfoncé : START clignote. Relâchement : STATE et voyant allumés |
| Un AU (1 NC) par voie | Alerte de verrouillage (ERROR, S12, S22 clignotent en synchrone). Réarmement seulement après ouverture puis refermeture des deux voies |
| Voyant 24 V CC 15 mA sur 13-14 | Fonctionne avec +24 V sur 13. Ne s'allume pas sans alimentation externe : contact sec |

Essais restant à réaliser : court-circuit S12–S22, Y1–Y2 ponté en permanence, coupure puis retour de l'alimentation, contrôle de contacteur avec NC miroir.

## 14. Application TTK

### 14.1 Décisions acquises [TTK]

- Un seul relais XPSUAF13AP câblé, sans programmation ni sortie temporisée. AU en catégorie d'arrêt 0. Objectif PL d. PL c accepté pour la translation pas à pas.
- AU : plusieurs boutons possibles, 3 contacts par AU : 2 NC (voies 1 et 2) + 1 NO (information automate).
- Capot en Auto : son ouverture équivaut à un AU. En Manu : il s'ouvre sans déclencher. Contacts Manu du commutateur en **parallèle** des interrupteurs de capot, un contact par voie (R-14).
- Interrupteurs de capot : un mécanique (NC à manœuvre positive d'ouverture) et un magnétique non codé, chacun 1 NO + 1 NC. Leurs contacts auxiliaires sont lus par le S7-1200 G2 pour un contrôle de discordance.
- Commutateur de mode Eaton à cames, sans clé : 2 positions, 4 contacts NO par position. Position 1 = Auto, 2 = Manu. 3 contacts utilisés par position (2 sécurité + 1 information automate), 1 en réserve.
- Contacts Auto du commutateur en série avec la sortie de sécurité qui commande les STO et KM1/KM2.
- KM1/KM2 (LC1D09BD) en amont des variateurs MCX91A. Les deux entrées STO des MCX91A sont câblées en parallèle sur une seule sortie de sécurité, ce qui a été vérifié sur le schéma SEW.
- Freins BE5 : coupés côté 400 V CA par KF1/KF2 (LC1D09BD, un par frein) sur une sortie du relais. Coupés **uniquement par l'AU, jamais par un changement de mode** : cette sortie ne doit pas passer par les contacts de mode.
- 48 V CC des pas-à-pas : coupé par un contacteur LC1D09BD unique, juste après l'alimentation 48 V. Contact Manu en série sur sa bobine. L'entrée ENA des drivers n'est câblée qu'au S7.
- Réarmement par bouton-poussoir sur l'armoire. État affiché sur l'IHM et par un voyant d'armoire.

### 14.2 Points de vigilance pour le schéma

1. **Nombre de sorties.** Une répartition possible des charges :
   - sortie A, via les contacts Auto : STO + KM1/KM2 ;
   - sortie B, AU seul : KF1/KF2 ;
   - sortie C, via le contact Manu : contacteur 48 V.

   Les 3 NO seraient alors tous utilisés, sans réserve. Toute fonction supplémentaire, comme l'ordre automate de l'ancien point « 23-24 », impose l'extension XPSUEP ou une autre solution (§7). Répartition à valider par Julien.
2. **Courant minimal (R-32).** Vérifier le courant d'entrée STO du MCX91A. Si les deux STO en parallèle consomment moins de 10 mA, la fiabilité du contact n'est plus garantie par Schneider. Valeur SEW [à confirmer].
3. **Boucle de retour (R-22).** NC miroirs de KM1, KM2, KF1, KF2 et du contacteur 48 V en série dans Y1–Y2. Chacun doit être retombé au moment du réarmement, quel que soit le mode. Contact miroir sur LC1D09BD [à confirmer].
4. **Capot à deux technologies (R-16).** Vérifier au banc qu'une ouverture lente du capot ne lève pas d'alerte de verrouillage récurrente.
5. **Shunts de mode (R-14).** Les contacts Manu en parallèle du capot doivent rester distincts par voie. Un même contact ne doit jamais shunter les deux voies.
6. **B2 (R-02).** Le relier au 0 V du 24 V PELV, ce 0 V étant lui-même relié à la PE en un point unique (règle TTK sur le PELV).
7. **Incohérence d'historique.** Une note de septembre 2026 indiquait « frein BE5 commandé par un contacteur piloté par l'automate ». Elle est remplacée par la décision d'octobre : KF1/KF2 sur une sortie du relais, coupés par l'AU uniquement. Vérifier que le schéma WinRelais suit la décision d'octobre.
