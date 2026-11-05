# 06 · Travail en cours (version actuelle et suite)

## Version actuelle : v22 (05/11/2026)
`schema/generes/release/TTK_2026-11-05_v22.xrs` : 25 folios, 177 symboles, 654 fils, 91 renvois ; 0 problème, 0 erreur au verifier, 28 attentions (27 connues + bout libre voulu vers le bâti), 0 chevauchement. **En attente : validation de Julien (liste ci-dessous).**

### Fait en v22
| Folio | Changement |
|---|---|
| 70 | Bloc « Bornes de la porte de l'armoire (rail R4) » : S1, S4, H3, H4, puis H2 230 V au bout, une butée entre appareils |
| 62 | Mention « PROPOSITION A VALIDER » retirée (E/S validées) |
| 70 | Désignation du groupe X41.1 corrigée : « AU pupitre -S2, voies 1 et 2 » (S1 est sur X41.5) |

### Contrôle des bornes (v21 → v22, 05/11)
89 bornes sur rail (85 bornes 4 mm + 4 de terre) + 3 blocs PTFIX : repères conformes (X + folio + . + n°), folio du repère = folio de dessin, numéros sans trou ni doublon dans chaque groupe, les 2 côtés de chaque borne câblés. Seuls les PTFIX ont des points libres (voulu).

## Version précédente : v21 (05/11/2026)
### Fait en v21
| Folio | Changement |
|---|---|
| 30, 31, 32, 50 | Fils PROFINET (10 tronçons) : type « Profinet », rose foncé, épaisseur 44 |

## Version précédente : v20 (05/11/2026)
### Fait en v20
| Folio | Changement |
|---|---|
| 21 | X21.11 / .12 / .13 : **PTFIX 6/12X2,5** (3273354), symbole `librairie/CUSTOM/Phoenix_3273354_PTFIX_6-12x2.5.xsy` (entrée E, départs 1-6 en haut, 7-12 en bas) ; couleurs rouge / bleu / gris ; montée du 0 V vers la barre déplacée à x = 12400 ; cadres « image du bornier » décalés à droite |
| tous | Type des câbles : blindé (ellipse + trait) pour W2 à W6, W9, W10 ; simple pour W1, W8, W13 |

## Version précédente : v19 (05/11/2026)
### Fait en v19
| Folio | Changement |
|---|---|
| 70 | Câbles **-W11** (27G1, armoire → pupitre) et **-W12** (19G1, armoire → boîte de dérivation machine) validés : conducteur n → borne, nom du composant sous chaque groupe, **butée d'arrêt** (trait épais) entre deux fonctions. Table `CABLES_MULTI` du script |

## Version précédente : v18 (05/11/2026)
### Fait en v18
| Folio | Changement |
|---|---|
| 31, 32 | Freins M1 + M2 sur **un seul câble -W4** 5G1,5 blindé : brins 1-2 au f31, 3-4 au f32 (même repère sur les 2 folios ; paramètre `nums` de `g.cable`) ; W7 supprimé ; 3 lignes de texte sur le V/J (-XPE1, boîte de dérivation) |
| 10 | Liaison équipotentielle **-W13** (V/J 4 mm²) : départ du peigne de terre vers « Bâti machine +M » |
| 02 | Liste des câbles : -W212 retiré ; bloc « câbles -W2 à -W6 » |

## Version précédente : v17 (05/11/2026)
`schema/generes/release/TTK_2026-11-05_v17.xrs` : 25 folios, 177 symboles, 652 fils, 91 renvois ; 0 problème au contrôle interne, 0 erreur au verifier (27 attentions connues), 0 chevauchement. v16 non réenregistrée par WinRelais (rien à reprendre), passée dans old/. **En attente : retours de Julien (Q8).**
But de Julien : un schéma propre (borniers, sécurité, automate) **avant** la numérotation des fils.

### Fait en v17 — retours du 05/11
| Folio | Changement |
|---|---|
| 41, 42, 60 | Sélecteur S3 : vrais numéros Eaton (ponts retirés) et noms **AUTO-A** 1-2 (-KM1 / -KM2), **MANU-A** 3-4 (shunt capot voie 1), **AUTO-B** 5-6 (STO), **MANU-B** 7-8 (shunt voie 2), **AUTO-C** 9-10 (info Auto → I0.4), **MANU-C** 11-12 (info Manu → I0.5), **MANU-D** 15-16 (48 V, -KA2) ; AUTO-D 13-14 en réserve (non dessiné). Symboles `librairie/CUSTOM/Eaton_T0_contact_NO_*.xsy` |
| 61 | Colonne H1 par 4 bornes **X61.11-14** (RD, OG, GN, COM) ; voyant H4 par **X61.21-22** ; collecteur 0 V descendu à y = 16400 |
| 40 | Réarmement S4 par **X40.11** (avant) et **X40.12** (retour vers Y2) ; S4 descendu de 400 |
| 12 | Voyant H2 230 V par **X12.21-22** ; H2 descendu de 800 (bus N à y = 4800) |
| 21 | Voyant H3 par **X21.21-22** |
| 31, 32 | Texte rouge réduit à « TF X10 : bornes à confirmer » (X6 confirmé) |
| 60 | Fins de course B3 à B6 : désignation et tableau en NO |
Règle de Julien (05/11) pour la porte : **tous les appareils par des bornes, ou aucun**. Tous dessinés ; si le rail R5 manque de place (agent d'implantation), on les retire tous.

## Feuille de route (05/11, après la v19)
Jalon J2 « bon pour câblage » : 13/11/2026.
1. **Julien relit la v19 dans WinRelais** (Q8) : journal à l'ouverture, références croisées automatiques, f31 / f32 (Q12), f40 à f42 (S3, S4), f61 (H1, H4), f70. Aucune version depuis la v16 n'a été vue à l'écran.
2. **.xrs de test** de Julien : champ « câble blindé », « afficher les numéros », type PROFINET (points 17 à 20).
3. **Liste d'E/S f60 à f62** à valider ; puis retirer « PROPOSITION A VALIDER » du f62 (Q13).
4. **Numérotation des fils** : convention v2 **retenue** le 05/11 (`04_REGLES_DESSIN.md`), sans point (1013) ; à générer **en dernier**, après validation sécu, automate, borniers par Julien. Détail : (chiffres seuls, tout numéroté y compris phases, N, 24 V, 0 V ; FFNN, unité = conducteur) ; à valider par Julien. Ancien libellé : (revue C7 : repères en stock A L R S U X Z / . seulement, 0,5-1,5 mm², rien en 2,5 et 4 mm²), puis numérotation générée.
5. Données à obtenir : SEW (sondes TF livrées ? bornes X10, courant STO ≥ 10 mA, courant frein BE5 pour QF2 / QF3, mises sous tension / h) ; ifm MN508S (homologation, actionneur codé) ; DC-1 du LC1D09BD sous 48 V ; brochages G2 Siemens.
6. Achats : raccord thermocouple (Q28), fixation sonde (Q29), câble moteur 50 m pour un besoin de 60 m (Q30, C1), câble V/J 4 mm² (W13), câble M12 de B2, butées (Q39), presse-étoupes CEM et boîte de dérivation (C2, C5). Longueurs des câbles W3 à W6, W9 à W12.
7. Agent d'implantation : **fait en implantation v8** (05/11) : W4 freins, W3 / W6 TF, bornes de porte sur R4 (manque de place sur R5), H1 X61.1x, butées (20), W13 (passe-câble E15). À valider par Julien.
8. Après J2 : câblage, essais au banc (capot B1 / B2 écart 200 ms, essais KA1 restants), programme TIA (PTO, ENA, trames Z1).

## À faire ensuite (détail)
1. H2 : reporter la référence du voyant 230 V quand Julien l'aura.
2. f70 / f71 : les bornes de porte (X41.5x, X60.4x) n'y figurent pas (destination « porte ») : à ajouter si Julien le veut.
3. Champs « câble blindé » et « afficher les numéros » dès réception du .xrs de test de Julien ; type de conducteur PROFINET.
4. Liste d'E/S (f60 à f62) : seulement après validation de Julien. Numérotation des fils : après le schéma propre.
5. Achats : Q28 à Q30 (raccord thermocouple, fixation sonde, câble moteur 50 m).

## Validation par Julien (liste mise à jour le 05/11, v22)
- Sécurité : freins libres en Manu **voulus** (réglé) ; courant STO (SEW, `docs/QUESTIONS_SEW.md`) ; capot B1 / B2 écart 200 ms et boucle Y1-Y2 (essais de banc) ; relire f40 à f42 à l'écran.
- Automate : réglé (E/S validées, mention f62 retirée) ; bornes du thermocouple à l'achat (Q19).
- Borniers : 89 bornes pour 85 achetées (+ réserve 10 %, + 6 si les conducteurs de réserve des 27G1 / 19G1 sont bornés) ; type des 4 bornes de terre en stock ? ; 5 bornes PT 4 pour l'arrivée X10 (5G4) ; butées de chaque côté de chaque appareil sur tous les rails (règle de Julien) ; H2 230 V séparé des bornes 24 V sur R4 (butée, cloison ?).
- Agent d'implantation : bornes de porte sur **R4** (bloc du f70), butées de chaque côté de chaque appareil sur tous les rails, câble frein W4, W13.
