# TTK-SCHEMA-ELEC

Schéma électrique de la **machine de tressage TTK** (n° 001-EU), sous **WinRelais 2.6b Expert**.
BE Bailly Levert (BEBL), dessinateur Julien Thro (THRO.J).

Le schéma n'est pas dessiné à la main. Il est **généré par un script Python** (`outils/ttk_schema.py`), puis ouvert et relu dans WinRelais.
Assistant : lire d'abord `CLAUDE.md`, puis `memoire/` (README, 10, puis 01 à 09).

## État actuel (26/11/2026)
| | |
|---|---|
| Dernière version | **v44**, `schema/generes/release/TTK_2026-11-26_v44.xrs` (rapport `docs/RAPPORT_v44_2026-11-26.md`) |
| Contenu | 31 folios, 254 symboles, 708 fils, 93 renvois, 407 numéros de fil, 168 bornes ; boîte +BJM, plans de bornier f70-f73, liste des câbles f80, nomenclature f90-f92 générés par le script |
| Contrôles | `sh outils/controles/tout.sh <essai.xrs> JJ/MM/AAAA` : tout à 0 (verifier : 0 erreur, 28 attentions connues) |
| En attente | Relecture de la v44 par Julien dans WinRelais ; référence montée de QM1 / QM2 ; points ouverts : `memoire/05_POINTS_OUVERTS.md` |
| Implantation de l'armoire | v13 (20/11, schéma v36), `implantation/release/` ; à régénérer (accord de Julien avant push) |

## La machine en bref
- Réseau 400 V 3P+N+PE (TN-S), armoire +A1, boîte de jonction machine +BJM, machine +M, pupitre +P1 posé sur la machine.
- 2 motoréducteurs SEW (frein BE5, sonde TF), chacun avec un variateur MCX91A (STO, PROFINET).
- 2 axes pas-à-pas (drivers Jkongmotor JKDM860H, 48 V) pour la translation en mode Manu.
- Sécurité : relais XPSUAF13AP (KA1), AU armoire S1 et pupitre S2, capots B1 / B2, sélecteur Auto / Manu S3.
- Automate S7-1200 G2 (CPU 1214C, SM 1223, SM 1231 TC), IHM KTP700, switch PROFINET.

## Folios (numéros affichés)
| N° | Titre |
|---|---|
| 01 | Page de garde |
| 02 | Sommaire |
| 03 | Synoptique général (par lieu) |
| 10 | Arrivée et sectionnement (W1, QS1, QF1, terre, variante USA TR1) |
| 11 | Distribution 400 V (variateurs, freins) |
| 12 | Distribution 230 V : alimentations 24 V / 48 V, voyant H2, liaison PELV |
| 13 | Distribution 230 V : éclairage, ventilation, prise de service |
| 20 | 48 V CC et moteurs pas-à-pas (KA2, drivers U3 / U4, M3 / M4) |
| 21 | Distribution 24 V CC (blocs X21.11 à X21.14, voyant H3) |
| 30 | Réseau PROFINET (switch K4, adresses IP) |
| 31, 32 | Puissance variateur 1 / 2 (U1 / U2, résistances, moteurs M1 / M2) |
| 40 | Relais de sécurité KA1 (boucle de retour, réarmement S4) |
| 41 | Sécurité : entrées (AU S1 / S2) |
| 42 | Sécurité : sorties (freins, KM1 / KM2, 48 V, STO) |
| 43 | Sécurité : capots B1 / B2, shunts Manu |
| 50 | Pupitre opérateur (IHM P1) |
| 60 | Automate : alimentation et PROFINET |
| 61 | Automate : entrées TOR |
| 62 | Automate : sorties TOR (drivers) |
| 63 | Module SM 1223 : colonne H1, voyant défaut H4 |
| 64 | Module SM 1231 TC : thermocouple B7 |
| 70-73 | Plans de bornier (armoire +A1 et boîte +BJM) |
| 80 | Liste des câbles |
| 85 | Implantation armoire (image à insérer quand elle sera validée) |
| 90-92 | Nomenclature |

Le script garde d'anciens numéros en interne (table `NUMFOL`, voir `memoire/04_REGLES_DESSIN.md`) : affiché f20 = interne "32", f31 = "20", f61 = "50", etc.

## Repérage
- Appareils : préfixes fonctionnels (QS1, QF1…, KM1, KA1, U1…, S1…, B1…, H1…), dict `RENOMME` du script.
- Bornes : **X + n° du folio + « . » + n° de borne**, une dizaine par fonction (X31.11 à X31.14 = moteur M1 au f31). Boîte : +BJM-X1.1 à X1.69.
- Numéros de fil : FFNN (folio de naissance + dizaine de l'appareil + conducteur), centrés sur la longueur du fil (v42).
- Couleurs des fils : IEC 60204-1 (noir puissance, bleu clair neutre, bleu foncé 24 V CC, vert/jaune terre).

## Arborescence
| Dossier | Contenu |
|---|---|
| `memoire/` | **Mémoire du projet** : README, puis 10 (reprise), puis 01 à 09 ; `revues/` (retours de Julien par version, revues extérieures) |
| `docs/` | `DECISIONS.md` (décisions datées), `JOURNAL_ECHANGES.md`, rapports de version `RAPPORT_vNN_*.md`, revue des achats, références |
| `outils/` | `ttk_schema.py` (le schéma), `xrs_gen.py` (écriture .xrs), `nomenclature.py` (f80, f90-f92), `xrs_tool.py` (vérification, nomenclature WinRelais), `xrs_chevauchements.py`, `xrs_numeros.py` |
| `outils/controles/` | `tout.sh` (génère + tout contrôle), `symboles.py`, `cadres.py`, `textes.py`, `d11.py`, `bornes.py`, `bbox.py` ; aides : `folio.py` (lecture d'un folio par calcul), `retouche.py` (comparer une release réenregistrée par WinRelais), `centrage.py` (centrage des numéros) |
| `outils/librairie/CUSTOM/` | Symboles créés pour le projet (copie du dépôt) ; `outils/librairie/scripts/` : scripts de modification de symboles déjà appliqués |
| `librairie_winrelais/` | Copie de la librairie WinRelais du PC (`sym_electrotech/CUSTOM` identique à `C:\Users\Public\Documents\Elec-CAO\sym_electrotech\CUSTOM`) |
| `schema/images/` | Images posées par le script (logos f01, blocs PTFIX f21) |
| `schema/modele/` | `SCHEMA_ELEC_TTK.xrs` : modèle (en-tête, cartouche), **à ne jamais modifier** |
| `schema/generes/release/` | La dernière version seule (+ vérification, nomenclature) |
| `schema/generes/old/` | Versions précédentes |
| `schema/recus/` | Releases ouvertes et réenregistrées par WinRelais (retouches de Julien) |
| `implantation/` | Dossier d'implantation de l'armoire, généré (`implantation/generateur/`, `saisie.json`) |
| `livrables/` | Anciens livrables (classeur de repères, récapitulatifs) |

## Générer une version
```bash
cd outils
export PYTHONIOENCODING=utf-8 TTK_LIB='C:\Users\Public\Documents\Elec-CAO\sym_electrotech' TTK_DATE=JJ/MM/AAAA
python ttk_schema.py ../schema/generes/release/TTK_AAAA-MM-JJ_vN.xrs
# option : TTK_IMAGES=<dossier des images écrit dans le .xrs> (défaut : chemin complet de schema/images sur le PC qui génère)
python xrs_tool.py verifier <fichier.xrs> > <fichier>_verification.md
python xrs_tool.py nomenclature <fichier.xrs> > <fichier>_nomenclature.csv
```
Contrôle complet d'un essai : `sh outils/controles/tout.sh <essai.xrs> JJ/MM/AAAA` (depuis la racine du dépôt).

Avant de passer l'ancienne version dans `old/` : `git status`. Si WinRelais l'a réenregistrée, l'archiver dans `schema/recus/AAAA-MM-JJ_vNN_ouverte_WinRelais.xrs`, la comparer (`outils/controles/retouche.py` et blocs des câbles) et reprendre les retouches de Julien dans le script, puis `git checkout` du fichier généré. Une retouche faite seulement dans WinRelais est perdue à la génération suivante.
