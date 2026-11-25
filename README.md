# TTK-SCHEMA-ELEC

Schéma électrique de la **machine de tressage TTK** (n° 001-EU), sous **WinRelais 2.6b Expert**.
BE Bailly Levert (BEBL), dessinateur Julien Thro (THRO.J).

Le schéma n'est pas dessiné à la main : il est **généré par un script Python** (`outils/ttk_schema.py`), puis ouvert et relu dans WinRelais.

## État actuel (25/11/2026)
| | |
|---|---|
| Dernière version | **v40**, `schema/generes/release/TTK_2026-11-25_v40.xrs` (rapport `docs/RAPPORT_v40_2026-11-25.md`) |
| Contenu | 31 folios, 254 symboles, 712 fils, 93 renvois, 407 numéros de fil, 168 bornes ; boîte +BJM, plans de bornier f70-f73, liste des câbles f80, nomenclature f90-f92 générées |
| Contrôles | `sh outils/controles/tout.sh <essai.xrs> JJ/MM/AAAA` : 0 problème, 0 erreur (28 attentions connues), 0 chevauchement (contrôle élargi), numéros, cadres, textes, 24 V / 0 V, bornes : 0 |
| Implantation de l'armoire | v13 (20/11, schéma v36), `implantation/release/` ; à régénérer |

La liste des folios et l'arborescence ci-dessous datent de la v36 : la référence à jour est `memoire/04_REGLES_DESSIN.md` (ordre des folios) et `memoire/06_EN_COURS.md`.

## La machine en bref
- Réseau 400 V 3P+N+PE (TN-S), armoire +A1, pupitre +P1 posé sur la machine, machine +M.
- 2 motoréducteurs SEW (frein BE5, sonde TF), chacun avec un variateur MCX91A (STO, PROFINET).
- 2 axes pas-à-pas (drivers DM860H, 48 V) pour la translation en mode Manu.
- Sécurité : relais XPSUAF13AP (KA1), AU armoire S1 et pupitre S2, capots B1 / B2, sélecteur Auto / Manu S3.
- Automate S7-1200 G2 (CPU 1214C, SM 1223, SM 1231 TC), IHM KTP700, switch PROFINET.

## Folios (numéros affichés)
| N° | Contenu |
|---|---|
| 01-03 | Garde, sommaire, synoptique |
| 10-13 | Arrivée, distribution 400 V, alimentations 230 V, services |
| 20-21 | 48 V et pas-à-pas, distribution 24 V |
| 30-32 | Switch PROFINET, variateurs et moteurs M1 / M2 |
| 40-42 | Sécurité : relais KA1, entrées, sorties |
| 50 | Pupitre (IHM) |
| 60-63 | Automate : entrées, sorties (drivers), SM 1223 (colonne, voyant défaut), thermocouple |
| 70-71 | Borniers rail par rail (f70), tableau du bornier pupitre (f71) |
| 80-90 | Liste des câbles, implantation, nomenclature : à générer par WinRelais |

Le script garde d'anciens numéros en interne (table `NUMFOL`, voir `memoire/04_REGLES_DESSIN.md`).

## Repérage
- Appareils : préfixes fonctionnels (QS1, QF1…, KM1, KA1, U1…, S1…, B1…, H1…), dict `RENOMME` du script.
- Bornes : **X + n° du folio + « . » + n° de borne**, une dizaine par fonction (X31.11 à X31.14 = moteur M1 au f31).
- Couleurs des fils : IEC 60204-1 (noir puissance, bleu clair neutre, bleu foncé 24 V CC, vert/jaune terre).

## Arborescence
| Dossier | Contenu |
|---|---|
| `memoire/` | **Mémoire du projet** : à lire en premier (README puis 01 à 07) |
| `docs/` | Décisions datées (`DECISIONS.md`), journal des échanges, revue des achats, références (relais de sécurité) |
| `outils/` | `ttk_schema.py` (le schéma), `xrs_gen.py` (écriture .xrs), `xrs_tool.py` (vérification, nomenclature), `xrs_chevauchements.py`, `xrs_numeros.py` (contrôle des numéros de fil), `librairie/CUSTOM/` (symboles créés pour le projet) |
| `schema/images/` | Images posées par le script (logos f01, blocs PTFIX f21) |
| `schema/modele/` | `SCHEMA_ELEC_TTK.xrs` : modèle (en-tête, cartouche), **à ne jamais modifier** |
| `schema/generes/release/` | La dernière version seule (+ vérification, nomenclature) |
| `schema/generes/old/` | Versions précédentes |
| `schema/recus/` | Fichiers renvoyés par Julien (ouverts et réenregistrés par WinRelais) |
| `implantation/` | Implantation de l'armoire (draw.io), tenue par un agent dédié |
| `livrables/` | Anciens livrables (classeur de repères, récapitulatifs) |

## Générer une version
```bash
cd outils
export PYTHONIOENCODING=utf-8 TTK_LIB='C:\Users\Public\Documents\Elec-CAO\sym_electrotech' TTK_DATE=JJ/MM/AAAA
python ttk_schema.py ../schema/generes/release/TTK_AAAA-MM-JJ_vN.xrs
# option : TTK_IMAGES=<dossier des images écrit dans le .xrs> (défaut v37 : chemin complet de schema/images sur le PC qui génère)
python xrs_tool.py verifier <fichier.xrs> > <fichier>_verification.md
python xrs_tool.py nomenclature <fichier.xrs> > <fichier>_nomenclature.csv
python xrs_chevauchements.py <fichier.xrs>            # option --marge=N : écart minimal voulu (v38)
python xrs_numeros.py <fichier.xrs> 10,11,12,13,20,21,30,31,32,40,41,42,43,50,60,61,62,63,64
```
Avant de passer l'ancienne version dans `old/` : `git status`. Si WinRelais l'a réenregistrée, l'archiver dans `schema/recus/` et reprendre les retouches de Julien dans le script (une retouche faite seulement dans WinRelais est perdue à la génération suivante).
