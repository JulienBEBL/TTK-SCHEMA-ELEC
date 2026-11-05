# TTK-SCHEMA-ELEC

Schéma électrique de la **machine de tressage TTK** (n° 001-EU), sous **WinRelais 2.6b Expert**.
BE Bailly Levert (BEBL), dessinateur Julien Thro (THRO.J).

Le schéma n'est pas dessiné à la main : il est **généré par un script Python** (`outils/ttk_schema.py`), puis ouvert et relu dans WinRelais.

## État actuel (05/11/2026)
| | |
|---|---|
| Dernière version | **v20**, `schema/generes/release/TTK_2026-11-05_v20.xrs` |
| Contenu | 25 folios, 177 symboles, 654 fils, 91 renvois |
| Contrôles | 0 problème, 0 erreur au verifier (28 attentions connues), 0 chevauchement |
| En attente | relecture de Julien (v20), liste d'E/S (`docs/LISTE_ES_AUTOMATE.md`), convention de numérotation des fils |
| Implantation de l'armoire | v7 (draw.io), `implantation/release/` |
| Planning | J1 folios finis 05/11/2026 ; J2 bon pour câblage 13/11/2026 |

Détail de la version, points ouverts et suite : `memoire/06_EN_COURS.md` et `memoire/05_POINTS_OUVERTS.md`.

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
| 60-63 | Automate : entrées, sorties, SM 1223, thermocouple |
| 70-71 | Borniers machine / réseau et pupitre |

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
| `outils/` | `ttk_schema.py` (le schéma), `xrs_gen.py` (écriture .xrs), `xrs_tool.py` (vérification, nomenclature), `xrs_chevauchements.py`, `librairie/CUSTOM/` (symboles créés pour le projet) |
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
python xrs_tool.py verifier <fichier.xrs> > <fichier>_verification.md
python xrs_tool.py nomenclature <fichier.xrs> > <fichier>_nomenclature.csv
python xrs_chevauchements.py <fichier.xrs>
```
Avant de passer l'ancienne version dans `old/` : `git status`. Si WinRelais l'a réenregistrée, l'archiver dans `schema/recus/` et reprendre les retouches de Julien dans le script (une retouche faite seulement dans WinRelais est perdue à la génération suivante).
