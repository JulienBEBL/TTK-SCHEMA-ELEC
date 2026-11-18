# 06 · Travail en cours (version actuelle et suite)

## Version actuelle : v34 (18/11/2026, PC PRO RIMANE)
`schema/generes/release/TTK_2026-11-18_v34.xrs` : 27 folios, 184 symboles, 668 fils, 89 renvois, 337 numéros ; 0 problème, 0 erreur, 30 attentions (28 connues + 2 fils V/J en attente, voulus), 0 chevauchement, numéros 0 problème. v33 dans old/ (copie WinRelais sans retouche dans `schema/recus/`).

### Fait en v34 (revue v33 + réponses de Julien du 18/11)
| Folio | Changement |
|---|---|
| 03 | Bloc 24 V : -X21.14 capteurs |
| 20 | W9 / W10 « 5G1,5 blindé » ; V/J sur bornes de terre X20.15 / X20.25, « V/J non raccordé au moteur » |
| 63 | Texte « type à définir » retiré (X63 en PT 2,5) ; W8 « compensation type K RS 236-3959 » |
| 70 | « boîte +BJM » ; X20.15 / X20.25 dans le tronçon 3 |
| 71 | Côté armoire : « +24 V capteurs (-X21.14 noir) », « Terre PE / FE (-XPE1) » |
| 85 | « image du plan d'implantation à insérer quand il sera validé » |
| 90-92 | B3-B6 « contact NF 11-12 (0 = fin de course atteinte) » ; PTFIX 2X4 « 2 trous - 6 mm » ; H3 / H4 avec caractéristiques ; terre 6 |

### Suite
- Julien : relire la v34 ; 2 bornes de terre à prévoir (6 dessinées, 4 achetées).
- Implantation : **v12 faite le 18/11** (2 pages, schéma v34, PTFIX 2X4, X20.15 / X20.25, +BJM) : relecture de Julien attendue. Détail : `08_IMPLANTATION.md`.

## Version précédente : v33 (18/11/2026, PC PRO RIMANE)
`schema/generes/release/TTK_2026-11-18_v33.xrs` : 27 folios, 182 symboles, 658 fils, 87 renvois, 333 numéros ; 0 problème, 0 erreur, 28 attentions (connues), 0 chevauchement, numéros 0 problème. v32 dans old/ (non réenregistrée).

### Fait en v33 (retours de Julien sur la v32)
| Folio | Changement |
|---|---|
| 30 | Textes des ports PROFINET décalés à droite des repères PN1-PN4 (x 9600) |
| 31, 32 | Bloc de droite réduit à 2 lignes : « X40 : PROFINET (f30) », « X5 : 24VELEC (f21) - X6 : STO (f42) » |
| 71 | Texte du bas : une ligne « Côté armoire en haut de la borne, côté terrain en bas. » |
| 80 | Liste des câbles générée par le script depuis `saisie.json` (17 câbles, 7 colonnes, texte 240) ; tableau WinRelais du 16/11 et texte retirés ; contrôle : chaque câble une fois |
| 90, 91, 92 | Nomenclature sur 3 folios (f92 ajouté), texte 280, tableau centré sur toute la zone utile, colonnes au prorata du contenu |
| saisie.json | W4 / W12 vers « +BJM » ; B3-B6 en NF 11-12 dans `apres_boite` |

### Retours de Julien sur la v33 (18/11)
- f80 (liste des câbles) : OK. Nomenclature : OK ; nouvelle passe dans quelques jours.
- v33 réenregistrée par WinRelais sur le PC Rimane, sans retouche (copie `schema/recus/2026-11-18_v33_ouverte_WinRelais.xrs`) ; **chemins d'images restés relatifs**.
- Revue complète demandée (schéma seulement) : `docs/REVUE_SCHEMA_v33_2026-11-18.md` (zones d'ombre § 1, folio par folio § 2, corrections proposées § 3). Rien corrigé ; v34 après le go de Julien.

### Suite
- Julien : trancher les points A1 (+BJM : quels câbles ?), A5 (V/J de W9 / W10), A6 (bornes X63), f85 ; go pour la v34 (§ 3 de la revue).
- Implantation : type PTFIX 2X4 (6 mm) à ajouter au générateur ; `boite` / `apres_boite` encore en « +M-X1 ».

## Version précédente : v32 (18/11/2026, PC PRO RIMANE)
`schema/generes/release/TTK_2026-11-18_v32.xrs` : 26 folios, 182 symboles, 658 fils, 87 renvois, 333 numéros ; 0 problème, 0 erreur, 28 attentions (connues), 0 chevauchement, numéros 0 problème. v31 dans old/ (copie WinRelais du PC Rimane : `schema/recus/2026-11-18_v31_ouverte_WinRelais.xrs`).

### Fait en v32
| Folio | Changement |
|---|---|
| 90, 91 | Nomenclature générée par le script (89 lignes) + contrôle d'exhaustivité ; f91 ajouté |
| 60 | Fins de course B3-B6 en **NF 11-12** (symbole CUSTOM `Fin_de_course_NF_11-12.xsy`), tableau « (NF) » |
| 41 | S2 « 2 NF + 1 NO » |
| 01, 21 | Images en chemin **relatif** `..\..\images\` (essai réussi dans WinRelais, 18/11) |
| nomenclature | Types de bornes de Julien : PT 4 (arrivée, moteurs, freins), PTFIX 2X4 1028361 (W11 / W12), PT 2,5 (R4) ; références B1, B3-B6, H1, S1, S2 ; H1 et B7 en +M |

### Retours de Julien sur la v32 (18/11) : à faire en v33, **après son go**
| Folio | Demande |
|---|---|
| 30 | Textes des fils PROFINET (« Port 1 -> K1 automate… ») superposés aux repères PN1-PN4 : les décaler |
| 31, 32 | Bloc de texte à droite (X40, X5 / X6, « TF X10 : bornes à confirmer » en rouge, blindage W5 / W6, note W4) : mal intégré ; garder l'essentiel d'un schéma élec, bien placé dans la page |
| 71 | Texte du bas (méthode, « Bornier graphique : Optimisation / Générer… ») : à intégrer proprement, garder l'essentiel |
| 80 | Liste des câbles à revoir : recouper avec la mémoire (09_STOCK, saisie.json, cablage/) ; recadrer le tableau ; enlever le texte |
| 90, 91 | Police plus grande, tableau centré, sur toute la place disponible, largeurs de colonnes réajustées |
| bornes | PTFIX 2X4 : 1 bloc = 2 trous (bloc de passage classique), 19 + 27 blocs (W12 + W11), largeur 6 mm |

### Suite
- Julien : v32 ouverte dans WinRelais le 18/11 (images relatives affichées) ; retours ci-dessus.
- PTFIX 2X4 : nombre de blocs, câblage d'un bloc (2 x 4 points ?), stock ; le symbole des bornes W11 / W12 reste « borne 4 mm ».
- Programme TIA : B3-B6 lus à 0 en fin de course.
- Implantation : `saisie.json` porte les nouveaux types (PT 4 freins, X13 en PT 2,5, PTFIX 2X4) ; le dossier d'implantation n'est pas régénéré (largeur des PTFIX 2X4 inconnue).

## 18/11/2026 : reprise sur le PC PRO RIMANE (analyse, rien corrigé)
- v31 ouverte dans WinRelais sur ce PC : copie `schema/recus/2026-11-18_v31_ouverte_WinRelais.xrs`. **Release pas encore restaurée** (`git checkout` en attente de l'accord de Julien).
- Comparaison à `HEAD` : 26 folios ; f90 remplacé par **f91 et f92 « Nomenclature »** générés par WinRelais (tableaux 2 et 3, 8 colonnes) ; le reste identique (zoom et format seulement). Le sommaire f02 dit encore « 90 ».
- Nomenclature : 8 causes dans le script (référence au 3e champ de `RefConstructeur` alors que WinRelais lit le 2e, champ 3 masqué tronqué, Qte = nb de symboles…). Options A (script + régénération WinRelais) / B (script génère le tableau). Détail : `docs/ANALYSE_PC_RIMANE_2026-11-18.md`.
- PC : identité git `--local` JulienBEBL / julien@bebl.fr (Julien 18/11) ; Python 3.15.2 installé : sur la v31 de HEAD, verifier 0 erreur / 28 attentions, chevauchements 0, numéros 0 problème (comme sur le PC de Julien) ; symboles CUSTOM non installés ; push GitHub OK (compte JulienBEBL).
- `CLAUDE.md` § 7 : les 2 clones (accord de Julien 18/11).
- Fait (Julien OK) : release v31 restaurée (`git checkout`), 53 symboles CUSTOM copiés dans `sym_electrotech\CUSTOM`, commit c542fcc poussé.
- Nomenclature **option B** codée (`outils/nomenclature.py`, f90 + nouveau f91), avec contrôle d'exhaustivité. Essai de génération hors release : 26 folios, 0 problème ; verifier 0 erreur / 28 attentions (identiques) ; 0 chevauchement ; numéros 0 problème. 88 lignes : 59 appareils, 97 bornes (PT 2,5 74, PT 4 15, PTFIX 4, terre 4), 17 câbles. À compléter : B7, H2, H3, H4, butées, +BJM.
- Autres changements dans le script : références B1, B3-B6 (RS PRO 902-6874), H1 (RS PRO 199-9760), S1 / S2 (XB5AS8442 + ZBE102 + ZBE101) au champ 3 ; S2 « 2 NF + 1 NO » (affiché au f41) ; localisation M pour H1 et B7 ; variable `TTK_IMAGES`.
- Essai PC Rimane : le script génère la v31 à l'identique (seuls les chemins d'images changent).
- En attente de Julien : générer la v32 en release ; ouvrir la copie de test des images ; push.

## Version actuelle : v31 (16/11/2026)
`schema/generes/release/TTK_2026-11-16_v31.xrs` : 25 folios, 182 symboles, 658 fils, 87 renvois, 333 numéros ; 0 erreur, 28 attentions (connues), 0 chevauchement, numéros 0 problème. v30 réenregistrée par Julien (copie `schema/recus/2026-11-16_v30_ouverte_WinRelais.xrs`).

### Fait en v31
| Folio | Changement |
|---|---|
| 80 | Tableau des câbles fait par Julien sous WinRelais, recopié par le script (`outils/blocs/`) |
| 85 | Textes remontés (Julien) |
| 60, 61 | Broches de la CPU 3L+ / 3M renommées **2L+ / 2M** (noms G2) dans le symbole CUSTOM et le script |

### Où on en est (16/11, v31)
- Suite :
  1. Références de nomenclature manquantes (Julien : B3-B6, B7, H2-H4, bornes, butées, câbles W1-W13 / PN1-PN4).
  2. Nom G2 des broches du SM 1223 (K2 porte 3L+ / 3M) : à vérifier.
  3. Implantation sous WinArmoire (f85) : procédure expliquée à Julien le 16/11 (transfert WinRelais -> fichier .wali -> WinArmoire .wavu -> export image / PDF -> f85). Doublon possible avec l'implantation draw.io (`implantation/`).
  4. Côté WinRelais (Julien) : références croisées, f90, relecture à l'écran.

## Version précédente : v30 (16/11/2026)
`schema/generes/release/TTK_2026-11-16_v30.xrs` : 25 folios, 182 symboles, 658 fils, 87 renvois, 333 numéros ; 0 erreur, 28 attentions (connues), 0 chevauchement, numéros 0 problème (tous les folios). v29 non réenregistrée.

### Fait en v30
| Folio | Changement |
|---|---|
| 31, 32, 40-42, 50, 60-63 | Numérotation des fils (détail : `04_REGLES_DESSIN.md`, « Numérotation f31... ») : tous les folios sont numérotés |
| 60 | Fils d'entrée de la CPU = n° de l'entrée (6011-6018, 6021-6026) : **validé par Julien (16/11)** |
| 31, 32, 41, 42, 60 | Bouts de fil de 400 allongés (place des numéros) ; f41 descendu de 400 |
| 40-42, 62 | Repère des bornes à côté de la borne |

### Où on en est (16/11, v30)
- Suite proposée :
  1. Références de nomenclature manquantes (à fournir par Julien : B3-B6, B7, W8, H2-H4, bornes, butées, PTFIX, câbles).
  2. Noms de broche 2L+ / 2M de la CPU (accord de Julien : symbole de sa librairie).
  3. Côté WinRelais (Julien) : références croisées, f80 / f90, relecture à l'écran.
- Implantation : brief `docs/A_FAIRE_IMPLANTATION_2026-11-16.md` (inchangé en v30 : aucune borne ajoutée).

## Version précédente : v29 (16/11/2026)
`schema/generes/release/TTK_2026-11-16_v29.xrs` : 25 folios, 182 symboles, 654 fils, 87 renvois ; 0 erreur, 28 attentions (connues), 0 chevauchement, numéros 0 problème. v28 réouverte par Julien sans retouche (copie `schema/recus/2026-11-16_v28_ouverte_WinRelais.xrs`).

### Fait en v29
| Folio | Changement |
|---|---|
| 70 | Borniers agrandis sur tout le folio (Julien) |
| 41 | Références S1 / S2 (XB5AS8442 + ZBE102 + ZBE101) et S3 (Eaton T0-4-8223/E) pour la nomenclature |
| dépôt | `.gitignore` (pycache, temporaires, images collées), README à jour, `docs/REVUE_COMPLETE_v29.md`, `docs/A_FAIRE_IMPLANTATION_2026-11-16.md` |

### Où on en est (16/11, v29, avant compaction)
- Revue complète faite : **cohérent électriquement, pas encore prêt pour le stagiaire** (détail `docs/REVUE_COMPLETE_v29.md` § 6).
- Suite proposée, dans l'ordre :
  1. Numérotation des fils de f31, f32, f40 à f42, f50, f60 à f63 (outil de contrôle `outils/xrs_numeros.py`, sources dans `SOURCES_NUM`).
  2. Références de nomenclature manquantes (à fournir par Julien).
  3. Noms de broche 2L+ / 2M de la CPU (accord de Julien : symbole de sa librairie).
- Julien relance un chat pour l'implantation : brief `docs/A_FAIRE_IMPLANTATION_2026-11-16.md` (XR2 sur R2, X13 sur R4, X21.14 noir sur R3, X62).

## Version précédente : v28 (16/11/2026)
`schema/generes/release/TTK_2026-11-16_v28.xrs` : 25 folios, 182 symboles, 654 fils, 87 renvois ; 0 problème, 0 erreur, 28 attentions (connues), 0 chevauchement, numéros 0 problème. v27 réenregistrée par Julien (copie `schema/recus/2026-11-16_v27_ouverte_WinRelais.xrs`) : seule retouche, les textes de S4 au f40 (repris : fpos (-2000, 0)).

### Fait en v28 (décisions de Julien du 16/11)
| Folio | Changement |
|---|---|
| 21, 60 | Bloc PTFIX noir **-X21.14** = 24 V capteurs, alimenté par L+ capt ; bus des capteurs = ses départs |
| 61, 62 | Colonne H1 et voyant H4 passés au f62 (bornes **X62.11-14**, **X62.21-22**) ; f61 = sorties vers les drivers seulement |
| 60, 61, 62 | Tableaux vérifiés ; corrigés : B1 / B2 « aux. 23-24 », ligne SM 1223 du f61 |
| 61, 62, 63 | Réserves : accolade + « Réserve » |
| tous | Titres et descriptions revus ; textes périmés corrigés (f03 PELV X12.11 et X13, f31 / f32 n° de folio des freins, f50 bornes X50, f80 liste des câbles) |
| 63 | Mise en forme (W8, réserve) |
| 70, 71 | f70 centrage ; f71 potentiels nommés justes |

### Où on en est (16/11, v28)
- Numérotation : f10-f13, f20, f21, f30 + 6001 ; restent f31, f32, f40-f42, f50, f60-f63.
- À confirmer : bloc noir en stock et place sur R3 ; implantation à mettre à jour (XR2 sur R2, X13 sur R4, X21.14 sur R3).

## Version précédente : v27 (13/11/2026)
`schema/generes/release/TTK_2026-11-13_v27.xrs` : 25 folios, 181 symboles, 647 fils, 89 renvois ; 0 problème, 0 erreur, 28 attentions (connues), 0 chevauchement, contrôle des numéros 0 problème. v26 réenregistrée par Julien (copie `schema/recus/2026-11-13_v26_ouverte_WinRelais.xrs`) : H2 descendu à 6800 et X12.22 à 10000 au f12, nouvelles images des blocs au f21 ; repris.

### Fait en v27
| Folio | Changement |
|---|---|
| 12 | H2 et X12.22 déplacés (Julien) |
| 13 | Bornes X13.11-12 (éclairage) et X13.21-22 (ventilation), appareils descendus de 800 |
| 20, 21, 30 | Numérotation des fils (table dans `04_REGLES_DESSIN.md`) ; bornes X20 descendues de 400, X21.22 de 800 (place des numéros) |
| 21 | Images des blocs : rouge X21.11, gris X21.13, bleu X21.12, centrées, hauteur 2600 |
| tous | Câbles PROFINET repérés PN1 à PN4 |
| 70 | R4 : bornes éclairage et ventilation avant la porte |

### Où on en est (13/11, v27)
- Numérotation : f10 à f13, f20, f21, f30 faits ; contrôle `outils/xrs_numeros.py` : 0 problème. Suite : f31 / f32 (encore L1 / L2 / L3 pour les potentiels du f11), puis sécurité, pupitre, automate.
- H2 : Julien garde le branchement sur le bus (fils à dimensionner pour 20 A).
- Toujours en attente : relecture automate (f60 à f63) puis borniers (f70 / f71) ; implantation : XR2 sur R2 et bornes X13 sur R4 à reporter.

## Version précédente : v26 (13/11/2026)
`schema/generes/release/TTK_2026-11-13_v26.xrs` : 25 folios, 177 symboles, 643 fils, 89 renvois ; 0 problème, 0 erreur, 28 attentions (connues), 0 chevauchement. La v25 réenregistrée par Julien (copie `schema/recus/2026-11-13_v25_ouverte_WinRelais.xrs`) : seule retouche = image du bornier au f21, reprise.

### Fait en v26
| Folio | Changement |
|---|---|
| 10 | Arrivée aérée ; W13 câble simple de 800 (plus de câble de longueur nulle : bug d'export PDF) |
| 11, 12, 13 | Numérotation des fils (table dans `04_REGLES_DESSIN.md`) |
| 21 | Image du bornier PTFIX dans les 3 cadres, textes « à insérer » retirés |
| 31, 32 | Fils TF en « Autre tension DC » |
| tous | Contrôle complet de la logique des fils hors E/S automate : `docs/CONTROLE_FILS_v26.md` (conforme ; 1 point : protection de H2) |

### Où on en est (13/11, v26)
- Numérotation : f10 à f13 faits ; suite folio par folio sur demande de Julien.
- À décider par Julien : protection du voyant H2 230 V (piqué sur le bus, QF1 20 A seulement).
- Toujours en attente : relecture automate (f60 à f63) puis borniers (f70 / f71).

## Version précédente : v25 (13/11/2026)
`schema/generes/release/TTK_2026-11-13_v25.xrs` : 25 folios, 177 symboles, 643 fils, 89 renvois ; 0 problème, 0 erreur, 28 attentions (connues), 0 chevauchement. v24 et ses logos collés dans `old/`. La v24 réouverte le 13/11 (copie `schema/recus/2026-11-13_v24_ouverte_WinRelais.xrs`) n'avait que des fils du f10 retournés (mêmes extrémités) : aucune retouche.

### Fait en v25
| Folio | Changement |
|---|---|
| 01, 10, 40 | Retouches de Julien dans la v24 reprises : logos (`schema/images/`), textes f10 / f40 déplacés, texte boucle Y1-Y2 du f40 retiré |
| 10 | **Numérotation des fils** (convention v2) : 1001-1004, 1011-1014, 1021-1024, variante USA 1031-1033 / 1041-1044 ; PE inchangé |
| 70 | Titre R4 : « R4 : porte de l'armoire » (XR2 n'y est plus) |

### Où on en est (13/11)
- **Numérotation des fils commencée** (Julien a les repères 4 mm²) : f10 fait ; suite folio par folio sur demande (f11 ensuite : bus 1021-1024).
- **Répartiteurs** : XR1 et XR2 collés sur le rail de QS1 (R2), rail plein (Julien, monté). Voir `03_ARCHITECTURE.md`.
- Toujours en attente : relecture automate (f60 à f63) puis borniers (f70 / f71) par Julien.
- Mises sous tension MCX91A : réglé (≈ 1 / 8 h, KM1 / KM2 gardés).

## Version précédente : v24 (09/11/2026)
`schema/generes/release/TTK_2026-11-09_v24.xrs` : 25 folios, 177 symboles, 643 fils, 89 renvois ; 0 problème, 0 erreur au verifier, 28 attentions (27 connues + bout libre voulu vers le bâti, f10), 0 chevauchement. La v23 réenregistrée par WinRelais (`schema/recus/2026-11-09_v23_ouverte_WinRelais.xrs`) n'avait aucune retouche.

### Où on en est (09/11, avant compaction)
- **Validé par Julien** : sécurité (06/11, avec STO en chaîne), E/S de l'automate (05/11), répartition 27G1 / 19G1, convention de numérotation v2 sans point.
- **En cours** : Julien relit la partie **automate** (f60 à f63) sur la v24 et revient avec ses remarques ; ensuite les **borniers** (f70 / f71).
- **En dernier** : numérotation des fils (méthode dans `04_REGLES_DESSIN.md`), après validation automate + borniers.
- **Mises sous tension MCX91A : réglé (09/11)**. Usage (Julien, 09/11) : environ **1 mise sous tension toutes les 8 h** (passage en Manu pour la maintenance, puis retour en Auto) ; l'AU est réservé aux urgences, pas d'usage normal. Compatible avec la réponse « 1 » de SEW : **on garde KM1 / KM2**, point clos.
- **Retouches de Julien dans la v24 (09/11), reprises dans le script, générées en v25** (Julien : ne pas modifier le schéma pour le moment) : logos TTK / BEBL / LEVERT INDUSTRIE au f01 (section `¤#Logo¤`, images `schema/images/logo_*.jpg`, textes « Logo ... » retirés) ; f10 « Bâti machine +M » déplacé (19300, 15700) ; f40 « Réglage -KA1 » déplacé (6600, 15300) ; f40 texte « Boucle de retour Y1-Y2 ... » supprimé. Essai de génération = identique à sa v24 (0 écart texte / symbole / fil). La release v24 gardée est **celle de Julien** (avec logos) ; copie `schema/recus/2026-11-09_v24_ouverte_WinRelais.xrs`.
- Bilan 24 V (`docs/BILAN_24V.md`) : Julien le juge bon ; calculs refaits, valeurs Siemens de copies distributeurs à recouper.

### Fait en v24
| Folio | Changement |
|---|---|
| 70 | Refait **rail par rail, dans l'ordre de l'implantation v10** (Julien 09/11) : R5 t1 W11 (S2 / S3 / IHM) ; R5 t1 suite W12 (B1 / B3-B6 / H1) ; R5 t2 B2, B7, TF M1, TF M2 ; R5 t3 W9, W10 ; R5 t4 freins W4, M1 W2, M2 W5, arrivée W1 ; R4 porte S1, S4, H3, H4, H2 ; R3 X21.11, X21.12, X12.11, X21.13. Cases réduites (520 de large, pas 640), butée de chaque côté de chaque groupe, conducteurs de réserve non bornés. Table `RAILS_X70` du script ; à tenir à jour avec `implantation/JOURNAL.md` |

## Version précédente : v23 (06/11/2026)
### Fait en v23
| Folio | Changement |
|---|---|
| 42, 31, 32 | STO **en chaîne** (Julien, validé SEW) : AUTO-B → -U1 X6.1, 0 V → -U1 X6.2 ; -U1 X6.3 / X6.4 → -U2 X6.1 / X6.2 ; -U2 X6.3 / X6.4 libres. Plus de peigne de 4 renvois au f42, un seul 0 V STO |
| 70 | Titre « BORNIERS DE L'ARMOIRE +A1 : GROUPES DE BORNES, CABLES ET PORTE » ; câble de chaque groupe dans son titre (W1, W2… W12, câble M12) |
Bilan des consommations 24 V : `docs/BILAN_24V.md`.

## Version précédente : v22 (05/11/2026)
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
7. Agent d'implantation : **implantation v10 (06/11, schéma v23)** : 2 pages (plaque, détail des borniers). R2 fixé par Julien (hors périmètre). PTFIX 6/12 posés en long (41 mm, Julien). À valider par Julien.
8. Après J2 : câblage, essais au banc (capot B1 / B2 écart 200 ms, essais KA1 restants), programme TIA (PTO, ENA, trames Z1).

## À faire ensuite (détail)
1. H2 : reporter la référence du voyant 230 V quand Julien l'aura.
2. f70 / f71 : les bornes de porte (X41.5x, X60.4x) n'y figurent pas (destination « porte ») : à ajouter si Julien le veut.
3. Champs « câble blindé » et « afficher les numéros » dès réception du .xrs de test de Julien ; type de conducteur PROFINET.
4. Liste d'E/S (f60 à f62) : seulement après validation de Julien. Numérotation des fils : après le schéma propre.
5. Achats : Q28 à Q30 (raccord thermocouple, fixation sonde, câble moteur 50 m).

## Validation par Julien (liste mise à jour le 05/11, v22)
- Sécurité : **validée par Julien le 06/11** ; restent le courant STO (SEW) et les essais de banc (boucle Y1-Y2, écart B1 / B2).
- Automate : réglé (E/S validées, mention f62 retirée) ; bornes du thermocouple à l'achat (Q19).
- Borniers : 89 bornes pour 85 achetées (+ réserve 10 %, + 6 si les conducteurs de réserve des 27G1 / 19G1 sont bornés) ; type des 4 bornes de terre en stock ? ; 5 bornes PT 4 pour l'arrivée X10 (5G4) ; butées de chaque côté de chaque appareil sur tous les rails (règle de Julien) ; H2 230 V séparé des bornes 24 V sur R4 (butée, cloison ?).
- Agent d'implantation : bornes de porte sur **R4** (bloc du f70), butées de chaque côté de chaque appareil sur tous les rails, câble frein W4, W13.

## Reste à valider sur tout le schéma (bilan du 13/11, après la v26)
Julien câble l'armoire avec la numérotation v26 ; **pas de v27 avant ses retours**.
- **Folios** : automate f60 à f63 (relecture de Julien en cours) ; borniers f70 / f71 ; f71, f80, f85, f90 n'ont que leur cartouche (remplir ou supprimer ?) ; contrôle à l'écran de f31 / f32 (Q12), des brins de W10 (Q26) et de l'export PDF (W13).
- **Numérotation** : faite f10 à f13 ; restent f20, f21, f30, f31, f32, f40 à f42, f50, f60 à f63.
- **Composants** (valeurs ou références manquantes) : H2, H3, H4 (références des voyants) ; bornes du thermocouple (Q19) ; bornes X10 de la sonde TF (SEW) ; courant des entrées STO, courant du frein BE5 (calibre de QF2 / QF3), consommation X5 (SEW) ; ifm MN508S (homologation, actionneur codé) ; DC-1 du LC1D09BD sous 48 V ; brochages G2 Siemens.
- **Fils et câbles** : section des fils de H2 (20 A) ; longueurs W3 à W6, W9 à W12 ; section W9 / W10 ; câble moteur 50 m pour 60 m (Q30) ; bornes : 89 pour 85 achetées, type des bornes de terre, séparation H2 230 V / 24 V sur R4.
- **Fonctions, au banc** : boucle Y1-Y2 (`docs/ESSAI_BANC_BOUCLE_RETOUR.md`) ; écart d'ouverture B1 / B2 (200 ms) ; I0.2 / I0.3 à 1 capot ouvert ; trames Z1 (I1.5) ; PTO dans TIA et micro-pas des DM860H (< 100 kHz).
- **Implantation** : XR2 déplacé sur R2 à reporter par l'agent draw.io.

## 17/11/2026 : librairie CUSTOM dans le dépôt (nouveau PC)
- `librairie_winrelais/sym_electrotech/CUSTOM/` : copie octet pour octet des 42 symboles CUSTOM du PC (`.gitattributes` : pas de conversion). Installation sur un autre PC : `librairie_winrelais/README.md`.
- Écart avec `outils/librairie/CUSTOM` (copie du script) : 10 symboles seulement dans le script (Eaton T0, PTFIX 3273354, borne terre, Hager NFT702), 5 seulement sur le PC.
- Complété (Julien : oui) avec les 11 symboles présents seulement dans le script : 53 symboles dans `librairie_winrelais`.

## 17/11/2026 : dossier d'implantation v11 (indice A), en attente des retours de Julien
- PDF unique `implantation/release/TTK_implantation_2026-11-17_v11.pdf` : garde, charte, plaque 1:7, borniers R5 (2 pages), R4 + R3, liste des câbles, affectation des conducteurs (2 pages), synoptique. Remplace l'implantation draw.io v10 (old/).
- Génération : `cd implantation/generateur` ; `python -I extraire.py` (lit la release .xrs + saisie.json → donnees.json) ; `python -I generer.py [--png dossier]`. Contrôle écrit dans `_verification.md` (textes trop larges, chevauchements, croisement bornes / câbles avec le .xrs). Attendu : 0 / 0 / 0.
- Données hors schéma (rails, appareils, câbles achetés, conducteurs) : `implantation/generateur/saisie.json`. Géométrie de la plaque reprise de la v10 (indice K).
- Points ouverts : manque 4 PT 2,5 ; X21.14 à droite de K4 (proposé) ; W14 (proposé) ; liaisons boîte +M-X1 → appareils ; au schéma : W9 / W10 « 4 cond. » → 5G1,5, W11 / W12 / W14 / PN absents du tableau f80.
