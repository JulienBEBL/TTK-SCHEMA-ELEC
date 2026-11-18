# Reprise sur le PC PRO RIMANE (18/11/2026) : analyse, sans correction

Clone : `C:\Users\Rimane\Documents\10. TTK\TTK-SCHEMA-ELEC` (hostname DESKTOP-G68K9P5).
Rien n'a été modifié dans le script ni dans les .xrs. Seule action : copie de la release ouverte dans WinRelais.

## 1. État du PC
| Point | Constat |
|---|---|
| git | `main` à jour avec `origin/main` (d05d619). Seul fichier modifié : la release v31 (réenregistrée par WinRelais). |
| Identité git | Aucune (ni locale, ni globale). Commits précédents : `JulienBEBL <julien@bebl.fr>` (68), `Julien <julien@bebl.fr>` (1), `Claude <noreply@anthropic.com>` (20). |
| GitHub | `git ls-remote` OK. `git push --dry-run` : « Everything up-to-date » (authentification OK, rien envoyé). Identifiant enregistré dans le gestionnaire Windows : compte `JulienBEBL`. |
| Fins de ligne | `core.autocrlf = true`. Le dépôt stocke les .xrs en LF ; la copie de travail est en CRLF. Normal. |
| Python | **Absent** (seul l'alias Microsoft Store répond). Aucun script ne peut tourner ici : ni génération, ni `verifier`, ni chevauchements, ni `xrs_numeros.py`, ni implantation. Comparaison faite en Perl (fourni avec Git). |
| TTK_LIB | `C:\Users\Public\Documents\Elec-CAO\sym_electrotech` existe (197 entrées). |
| Symboles CUSTOM | **Pas installés** dans `sym_electrotech\CUSTOM`. Le dépôt en a 53 (`librairie_winrelais/`). WinRelais ouvre quand même le schéma (symboles copiés dans le .xrs) ; il en a besoin pour poser un symbole CUSTOM à la main. |

## 2. v31 ouverte dans WinRelais sur ce PC, comparée à `HEAD`
Copie : `schema/recus/2026-11-18_v31_ouverte_WinRelais.xrs` (identique octet pour octet à la release modifiée).

| Section | Résultat |
|---|---|
| En-tête | Auteur OS « Rimane » ; compteurs 18120 → 18410 ; `¤#Schema¤` champ 3 : 7 → 24 (sens inconnu) ; `NombreFolio` 25 → 26. |
| Folios 01 à 85 (index 0-23) | Contenu identique. Seuls changent : nombre total de folios (26) dans le cartouche, drapeaux internes des 3 symboles support, zoom (`VueFolio`). |
| f90 (index 24) | Renommé « Nomenclature », numéro affiché **91**. Les 2 textes « Nomenclature : à générer par WinRelais… » supprimés. |
| f92 (index 25) | **Nouveau** folio « Nomenclature », titre NOMENCLATURE, description LISTE DU MATERIEL, date modif 16/11 recopiée. |
| Symboles | 182 = 182, mêmes repères, mêmes positions, mêmes champs, mêmes broches. Différences de format seulement : sections `Arc` / `MDessin` vides supprimées, 4 zéros ajoutés en fin de ligne `Arc` (128 symboles), drapeau `VueArmoire` 0·255 → 255·0. |
| Fils, jonctions, numéros, renvois | Identiques (658, 87, 333, 87). |
| Textes | 589 → 587 (les 2 textes du f90). |
| Cadres, images (`Logo`) | Identiques (326 traits, 6 images, chemins `C:\Users\Julien\…` gardés). |
| Câbles | 11 = 11, identiques. |
| Tableaux | 0 et 1 (f80) identiques. **Ajoutés** : tableau 2 (f91, 8 colonnes, 36 lignes) et tableau 3 (f92, 8 colonnes, 25 lignes). |

Conclusion : ton constat est confirmé. 26 folios ; f90 remplacé par f91 et f92 générés par WinRelais ; le reste ne diffère que par le zoom et des détails de format.

Incohérences relevées :
- Le sommaire (f02) affiche toujours « 90 NOMENCLATURE » : il ne connaît ni 91 ni 92.
- f91 et f92 portent le même titre et la même description.
- Le script ne connaît que f90 : à la prochaine génération, f91 / f92 disparaissent (même mécanisme que le f80 : il faudra recopier le bloc ou générer la nomenclature).

### Virgule décimale
Sur ce PC, WinRelais écrit le zoom avec une virgule : `0,749074074074074` (PC de Julien : `1.1287037037037`).
- Outils Python : sans effet. Aucun ne lit `VueFolio` ; `xrs_tool.to_int` renverrait 0 sans erreur.
- Le script régénère tout : la virgule ne revient pas dans les fichiers générés.
- Risque : si le fichier enregistré ici est rouvert sur le PC de Julien, son WinRelais peut mal lire ce zoom (à vérifier). Aucune autre valeur à virgule hors textes.

## 3. Nomenclature f91 / f92 : écarts
Colonnes WinRelais : Nom = champ 1, Valeur = champ 2, Désignation = champ 3, Champ 4, Champ 5, Constructeur = 1er champ de `RefConstructeur`, **Réf. = 2e champ de `RefConstructeur`**, Qte = nombre de symboles du repère.
Ligne d'un repère à plusieurs symboles = **le 1er symbole du fichier** (souvent un esclave).

### 3.1 Causes (dans le script)
| # | Cause | Effet |
|---|---|---|
| a | `ref=(fabricant, "", référence)` : la référence va dans le **3e** champ de `RefConstructeur`. WinRelais lit le **2e**. | Réf. vide pour 50 lignes sur 59. |
| b | Champ 3 masqué (`shown=(2, 4)`) : `xrs_gen.place` n'écrit que le 1er morceau coupé au `wrap` ; la suite est perdue. | U1 / U2 « SEW », FA1 « Mersen CMC101 + », S4 et bobines « Schneider ». |
| c | Champ 2 coupé au `wrap` (24 par défaut dans `_place`), la suite écrite dans les champs 5 à 8. | Textes coupés entre Valeur et Champ 5 (« Disjoncteur alimentation 24 » / « V n°1 »). |
| d | Qte = nombre de symboles, pas d'appareils. | K1, K2, KA2, KF, KM, S1, S2, S3 faux. |
| e | Ligne = 1er symbole lu : contacts de puissance (f11 / f20) ou contact MANU-A (f41), sans référence. | Constructeur vide pour KA2, KF1, KF2, KM1, KM2 ; S3 = « MANU-A : ». |
| f | Champ 3 = « À définir » alors que la référence est dans `RefConstructeur` ou dans la mémoire. | B1, H1, S1, S2, B3-B6. |
| g | Champs 4 et 5 sans nom dans les symboles. | En-têtes « Champ 4 », « Champ 5 ». |
| h | Bornes (drapeau borne = 1) et câbles non comptés par WinRelais. | 97 symboles X (93 bornes + 4 PTFIX) et 17 câbles absents. |

### 3.2 Écarts ligne par ligne
| Repère | Colonne | f91 / f92 | Attendu | Source |
|---|---|---|---|---|
| K1 | Qte | 2 | 1 | 2 symboles (f60, f61) ; 02_MATERIEL : 1 CPU 6ES7214-1AH50-0XB0 |
| K2 | Qte | 2 | 1 | 2 symboles (f62) ; 02 : 1 SM 1223 |
| KA2 | Qte / Constructeur / Désignation | 4 / vide / « Schneider Electric » | 1 / SCHNEIDER ELECTRIC / Schneider LC1D09BD | 4 symboles (f20, f40, f42, f60) ; maître f42 : LC1D09BD ; 02 |
| KF1, KF2 | idem | 3 / vide / « Schneider Electric » | 1 / SCHNEIDER ELECTRIC / LC1D09BD | 3 symboles (f11, f40, f42) ; 02 |
| KM1, KM2 | idem | 4 / vide / « Schneider Electric » | 1 / SCHNEIDER ELECTRIC / LC1D09BD | 4 symboles (f11, f40, f42, f60) ; 02 |
| S1, S2 | Qte / Désignation | 3 / « À définir » | 1 / XB5AS8442 + ZBE102 + ZBE101 | 3 symboles chacun ; 02 [D 03/11]. 1 ligne ou 3 (tête, NF, NO) : à décider |
| S2 | Champ 4 | « 3 contacts » | « 2 NF + 1 NO » (comme S1) | 02 [D 03/11] |
| S3 | toute la ligne | « MANU-A : … shunt capot », Qte 8 | Sélecteur Eaton T0-4-8223/E, Qte 1 | maître f41 ; 02 [C 05/11]. 8 symboles (tête + 7 contacts) |
| B1 | Désignation | « À définir » | RS PRO 902-6874 | RefConstructeur ; 02 |
| B3-B6 | Désignation / Constructeur / Réf. | « À définir » / vide / vide | RS PRO 902-6874 | Julien 17/11 (05_POINTS_OUVERTS) ; pas encore au script |
| B7 | Désignation | « Type K (réf. à définir) » | à vérifier | sonde RS 350-398 citée en Q29, non confirmée |
| H1 | Désignation | « À définir » | RS PRO 199-9760 | RefConstructeur ; 02 ; 3 couleurs [C 17/11] |
| H2 | Désignation | « À définir » | à vérifier | référence à relever (06) |
| H3, H4 | Désignation | vide ; Valeur coupée « Voyant porte : » | à vérifier | 02 : voyants 24 V, référence inconnue |
| U1, U2 | Désignation / Réf. | « SEW » / vide | SEW MCX91A-0055-5E3 | 02 ; RefConstructeur porte MCX91A-0055-5E3-4-T00/001/CSO/CFN/CDM/CMM (variante complète à vérifier) |
| FA1 | Désignation | « Mersen CMC101 + » | Mersen CMC101 + cartouche FR10GG50V4 gG 4 A | 02 [D 03/11] ; cartouche RS 188-6962 absente de la liste |
| S4 | Désignation / Réf. | « Schneider » / vide | Schneider XB4BA21 | RefConstructeur ; 02 |
| tous (50 lignes) | Réf. | vide | référence de `RefConstructeur` | cause a |
| T3 | Réf. | « RS 122-2229 » | à vérifier | dans le script, pas dans la mémoire |
| R1, R2 | Réf. | « 08281718 » | à vérifier | dans le script, pas dans la mémoire |
| FA1, H2-H4, KA1, KA2, QF4-QF8, QF10, QM1, QM2, TR1, QS1, B1, B7, M3, M4, R1, R2 | Valeur / Champ 5 | texte coupé en deux colonnes | texte entier | cause c |
| TR1 | ligne | présente | à décider | variante US, hors armoire, fourni par BEBL (01_PROJET) |
| bornes | absentes | — | 74 PT 2,5 (3209510), 15 PT 4 (3211757), 4 terre (RS 708-1687) | 09_STOCK (dessinées v31) |
| X21.11-14 | absents | — | 4 PTFIX 6/12X2,5 (3273354) | 09_STOCK |
| XR1, XR2 | absents | — | 2 répartiteurs AEE300427 | 02, 09 (non dessinés) |
| XPE1 | absent | — | Legrand 404839 | 02, 09 (non dessiné) |
| câbles | absents | — | W1-W6, W8-W14, PN1-PN4 | f80, cablage/TTK_CABLES.xlsx |
| butées, +BJM, presse-étoupes | absents | — | références à vérifier | 09_STOCK |

Valeurs écrites par le script mais absentes de `memoire/` (source à retrouver, à vérifier) : QF1 10 kA, QS1 690 V, QF9 6 kA, QF10 4,5 kA, T3 5 A, U1 / U2 5,5 A, U3 / U4 6,0 A, M3 / M4 6 A - 8,5 Nm, EL1 / EL2 14 W, EV1 / EV2 19 W, XD1 1,5 kW, S4 champ 7 « Z000263594 ».

Le CSV `TTK_2026-11-16_v31_nomenclature.csv` (182 lignes, une par symbole) lit le 3e champ de `RefConstructeur` : il montre la référence, la nomenclature WinRelais ne la montre pas. Même donnée, deux lectures.

### 3.3 Options
| Option | Principe | Avantages | Risques |
|---|---|---|---|
| A | Le script remplit proprement le maître (référence au 2e champ, champ 3 entier, champs 4 / 5 sans coupure, maître en 1er dans le fichier) ; Julien régénère la nomenclature dans WinRelais ; on recopie le bloc (comme le f80). | Outil de WinRelais, mise à jour en un clic. | Qte restera fausse si WinRelais compte les symboles (lien maître / esclave à tester) ; bornes et câbles absents ; aller-retour manuel à chaque version ; tableau perdu si on oublie de recopier. |
| B | Le script génère lui-même le tableau (`g.tableau`, comme le sommaire f02), une ligne par appareil, données lues dans le schéma + `09_STOCK` / `cablage/`. | Qte juste, bornes, câbles, accessoires ; colonnes nommées ; contrôlé par calcul ; plus d'aller-retour. | Plus de code ; ce n'est plus la nomenclature native de WinRelais (exports WinRelais à part) ; une retouche à la main sera écrasée. |
La correction a (référence au bon champ) sert aux deux options.

## 4. Images (C.2)
- Les chemins sont dans la section `¤#Logo¤` (pas `¤#ImageAP¤`, qui est vide : `·0·0·0·0·0·1·0·`). Script : `ttk_schema.py` lignes 616 (logos f01) et 999 (PTFIX f21).
- Le chemin est déjà recalculé depuis le dossier du script (`ICI`) : généré ici, il vaudrait `C:\Users\Rimane\…`. Le problème est donc **l'autre PC**, pas la génération.
- Sur ce PC, la release porte `C:\Users\Julien\…\Repo_git\…` : images absentes à l'écran ; WinRelais garde le chemin tel quel à l'enregistrement.
- `Image_Collée_*.jpg` : quand on **colle** une image, WinRelais l'écrit dans le dossier du .xrs et pointe dessus en absolu (v24 : `…\release\Image_Collée_5S5URXMW9C.jpg`). Une image **insérée depuis un fichier** : copie ou non, à vérifier.

| Option | Avantages | Risques |
|---|---|---|
| Chemin relatif (`..\..\images\logo_TTK.jpg`) | Marche sur les 2 PC sans réglage | WinRelais l'accepte-t-il ? À tester sur une copie de test (pas la release) ; relatif au .xrs ou au dossier courant ? |
| Dossier commun aux 2 PC (ex. `C:\Users\Public\Documents\TTK\images`) | Même chemin partout, comme la librairie | Images à copier sur chaque PC (et à chaque ajout) ; hors git |
| Variable d'environnement (`TTK_IMG`) | Le script s'adapte au PC | Le .xrs ne garde qu'un chemin : cassé sur l'autre PC quand même |
| Régénérer sur chaque PC | Déjà le cas | Python sur les 2 PC ; la release dans git porte le chemin du dernier PC ; diff à chaque changement de PC |

## 5. Chemins des clones (B)
- `memoire/07_METHODE_TRAVAIL.md` « Source de vérité » : mis à jour (les 2 clones).
- Autres endroits (non corrigés, en attente) :
  - `CLAUDE.md` § 7 : cite l'ancien dossier, pas de clone : ajouter les 2 clones.
  - `README.md` : aucun chemin de clone (commandes relatives) : rien à faire.
  - `implantation/README.md`, scripts (`outils/`, `implantation/generateur/`) : chemins relatifs ; seul absolu : Edge (`generer.py`, identique sur les 2 PC à vérifier).
  - `memoire/02_MATERIEL.md` l. 119 et `09_STOCK.md` l. 18 : fichiers `Downloads/…xlsx` du PC de Julien seulement.
  - Historique (à garder tel quel) : `docs/DECISIONS.md` l. 87, `docs/JOURNAL_ECHANGES.md` l. 39, `docs/local/CONNAISSANCES_WINRELAIS_TTK_ClaudeCode_22-10.md` l. 367-369.
  - Les .xrs (section `Logo`) : voir § 4.
