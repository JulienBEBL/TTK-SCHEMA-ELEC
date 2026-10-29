# 06 · À faire pour la v7

**Pas de génération avant d'avoir discuté les points « à discuter »** (demande de Julien, 29/10).
Statut : **acté** = décidé, à appliquer ; **à discuter** = solution à choisir avec Julien.

## Retours de Julien du 29/10 sur la v6

### Tous les folios
| # | Demande | Statut |
|---|---|---|
| 1 | Supprimer toutes les notes encadrées (`notes(...)` : f30, f31, f32, f40, f41, f42, f43, f54, f60, f70) | acté |
| 2 | f43 (tableaux de sécurité, risques résiduels) : garder les tableaux sans cadre, ou supprimer le folio ? | à discuter |

### Folio 10 : arrivée (« ok sauf la terre »)
| # | Demande | Statut |
|---|---|---|
| 3 | Terre en bas du folio : « c'est moche », faire comme les vrais schémas | à discuter (options ci-dessous) |
| 4 | Numéros de fil L1, L2, L3, N, **PE** : il en manque (PE jamais numéroté) | acté |
| 5 | **Incohérence trouvée** : la phase L3 du réseau (QS1 5/L3, QF1 6) part sur la barre L1 du répartiteur X12, et L1 sur la barre L3 (les 3 fils vers les renvois sont croisés dans l'ordre). Les noms générés affichent donc L3 sur QS1 1/L1. À corriger : L1 → L1, L2 → L2, L3 → L3. | acté |

### Folio 12 : distribution 400 V
| # | Demande | Statut |
|---|---|---|
| 6 | Pas de renvois au-dessus de chaque appareil : tirer un bus tri / tétra et piquer les phases utiles | à discuter |
| 7 | Numéros de fil manquants (tronçons courts entre renvoi et appareil) | acté |

### Folio 13 : distribution 230 V (« ok »)
| # | Demande | Statut |
|---|---|---|
| 8 | Séparer en 2 folios (esthétique uniquement) | à discuter (découpage) |
| 9 | Numéros de fil manquants (sorties des disjoncteurs, PE) | acté |
| 10 | Un des deux 24 V s'appelle **24VSEC** | à discuter (lequel, nom de l'autre) |
| 11 | EL1 / EL2 : croisement des fils « dégueu » → un départ propre par lampe, sans croisement | acté |
| 12 | Terre en bas : même problème que f10 | à discuter |
| 13 | QF7 / QF8 = Hager NFT702 (2 A, 1P+N, courbe C, 6-10 kA, 1 module) : symbole et champs | acté |

### 24 V
| # | Demande | Statut |
|---|---|---|
| 14 | Répartition ELEC / COMMANDE : **ok pour le tableau actuel** (voir `03_ARCHITECTURE.md`), pas de contacteur en plus | acté |

## Options proposées pour la terre (f10, f13)
- **A. PE dans le faisceau** : le PE suit les phases comme un 5e conducteur (L1 L2 L3 N PE côte à côte), vert-jaune, et sort par un renvoi à la même hauteur que les autres vers X13 (f11). C'est la présentation habituelle d'une arrivée.
- **B. Symbole de terre local** : fil PE court depuis la borne de l'appareil vers le symbole « Terre » de la librairie (`Masse - Terre/Terre.xsy`), plus le texte « X13 ». Plus léger, mais à vérifier : WinRelais relie-t-il ces symboles au bornier X13 (carnet de câbles, bornier généré) ?
- **C. Renvoi PE court** : fil PE court depuis l'appareil, terminé par un renvoi « PE → X13 » juste à côté. Garde le lien électrique, pas de grand fil.
- Proposition de l'assistant [H] : **A au f10, C au f13** (et aux autres folios avec du PE).

## Proposition pour le f12 (bus tri)
- [H] 3 renvois en entrée (L1, L2, L3 depuis X12), puis 3 lignes horizontales en haut du folio ; chaque appareil (QM1, QM2, QF2, QF3) se pique dessus avec un point de jonction.
- À discuter : ça crée des points de jonction, refusés au f32 (règle « un fil par appareil »). Pour l'assistant, c'est acceptable ici car le bus représente les barres du répartiteur. Le n° de départ de X12 (11, 21, 31…) disparaît du folio, sauf si on l'écrit au-dessus du piquage.

## Proposition pour le découpage du f13
- [H] **f13 « DISTRIBUTION 230 V - ALIMENTATIONS »** : QF4, QF5, QF6 vers T1, T2, T3, plus le voyant H2.
- [H] **f14 « DISTRIBUTION 230 V - SERVICES ARMOIRE »** : QF7 → EV1 / EV2, QF8 → EL1 / EL2, QF9 → QF10 → X14.

## Repris de la passation (§11), toujours à faire
15. Câbler moteurs, freins et sondes TF par X70 aux f20 / f21 ; mettre à jour f70 et `MEMES`.
16. Champs « câble blindé » et « afficher les numéros » dès réception du .xrs de test de Julien.
17. Type de conducteur PROFINET.
18. Descriptions de cartouche obsolètes (f02, f03, f10, f51).
19. Liste d'E/S (f50 à f52) : seulement après validation de Julien.
