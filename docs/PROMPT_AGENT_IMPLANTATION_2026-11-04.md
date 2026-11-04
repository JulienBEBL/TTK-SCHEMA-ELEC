# Prompt : mise à jour de l'implantation de l'armoire TTK (draw.io)

À donner tel quel à l'agent qui dessine l'implantation de l'armoire sous draw.io.
Écrit le 04/11/2026 par l'assistant du schéma électrique (WinRelais), à la demande de Julien.

---

## 1. Ta mission

Tu refais l'**implantation de l'armoire électrique +A1** de la machine de tressage TTK (n° 001-EU) sous **draw.io**, en tenant compte de **tout ce qui a changé** dans le schéma électrique depuis ta dernière version.

Tu livres à Julien :
1. une **nouvelle version** de l'implantation (fichier `.drawio` + export PDF), rangée dans le dépôt Git (voir §8) ;
2. une **courte note** : ce qui a changé par rapport à ta version précédente, et pourquoi ;
3. tes **questions** (voir §6) : pose-les **avant** de dessiner ce qui dépend de la réponse.

Tu ne modifies **jamais** le schéma électrique : c'est le travail d'un autre agent. Si tu trouves une incohérence dans le schéma, tu la signales à Julien.

## 2. Qui est Julien, comment travailler avec lui

- Julien Thro, **seul ingénieur** de BEBL. Il fait le schéma, les achats, le câblage, le programme et les essais. **C'est lui qui décide.**
- Réponds en **français**, en **phrases courtes**, concrètes. Trop de texte est un défaut.
- **Aucune valeur inventée** : pas de dimension, de référence ni de distance devinée. Cite la source (fiche fabricant, dépôt, réponse de Julien) ou écris « à vérifier ».
- **Au plus 3 à 4 questions numérotées par message.**
- Si tu n'es pas d'accord avec un choix, conteste **une fois** (raison + alternative), puis applique sa décision.
- Le matériel est **déjà commandé** et en grande partie reçu. **L'armoire est en cours de montage** : demande ce qui est déjà fixé avant de le déplacer.
- Planning : J2 « bon pour câblage » le 13/11/2026, armoire 1 sous tension le 26/11/2026. Deux stagiaires câbleront l'armoire à partir de ton plan : il doit être lisible et sans ambiguïté.

## 3. Où trouver l'information

Dépôt Git (source de vérité) : **https://github.com/JulienBEBL/TTK-SCHEMA-ELEC** (branche `main`).
Commence par `git pull` (ou `git clone` si tu n'as pas encore le dépôt).

À lire dans cet ordre :

| Fichier | Contenu |
|---|---|
| `CLAUDE.md` | Règles générales du dépôt |
| `memoire/README.md` puis `memoire/01` à `07` | Projet, matériel, architecture, règles de dessin, points ouverts, version actuelle, méthode |
| `docs/DECISIONS.md` | Toutes les décisions datées. Lis au moins **depuis le 28/10** |
| `docs/REVUE_ACHATS_2026-11-03.md` | Revue des achats : manques, achetés non utilisés, points à contrôler (presse-étoupes, reprises de blindage, bornes…) |
| `schema/generes/release/TTK_2026-11-04_v16_nomenclature.csv` | **Liste officielle des repères v16** (séparateur `;`) |
| `schema/generes/release/TTK_2026-11-04_v16.xrs` | Schéma WinRelais v16. Lecture possible avec `python outils/xrs_tool.py resume <fichier>` (ou `nomenclature`, `json`) |
| `docs/references/XPSUAF13AP_base_connaissances_cablage.md` | Relais de sécurité KA1 (montage sur rail, IP54 mini) |

**Attention aux anciens repères.** Certains fichiers de `memoire/` citent encore d'anciens noms (X11, X14, X31 à X36, X70, X71). **Seuls les repères de la nomenclature v16 font foi.** Correspondance : X11 → X10.1x, X14 → XD1, X31 / X32 / X33 → X21.11 / X21.12 / X21.13, X36.1 → X12.11, X70.n / X71.n → bornes X<folio>.<n> (§5).

## 4. Ce qui a changé (à reprendre dans l'implantation)

Si ta version précédente date d'avant le 28/10, presque tous les repères ont changé.

1. **Repérage** (28/10) : lettres de fonction + numéro (QS1, QF1 à QF10, QM1 / QM2, KM1 / KM2, KF1 / KF2, KA1 / KA2, U1 à U4, T1 à T3, K1 à K4, S1 à S4, B1 à B7, H1 à H4, EL1 / EL2, EV1 / EV2, R1 / R2, FA1). Détail : `docs/NOMMAGE_2026-10-28.md` et la nomenclature v16.
2. **Bornes** (02/11) : repère **X + n° de folio + « . » + n° de borne**, une dizaine par fonction (ex. X31.11 à X31.14 = moteur M1). Ancien bornier unique X70 / X71 **éclaté** en groupes (tableau §5).
3. **48 V** (02/11) : T3 (Mean Well NDR-240-48) alimente directement les drivers U3 / U4 par KA2. **Plus de bornier 48 V** (X34 / X35 supprimés).
4. **Bornier entre l'armoire et tout appareil extérieur** (02/11) : moteurs M1 / M2 (moteur, sonde TF, frein), pas-à-pas M3 / M4, capots, fins de course, thermocouple, pupitre.
5. **AU armoire S1 sur la porte** (02/11) : raccordé **par des bornes en bas de l'armoire** (X41.51 à X41.54, X60.41 / X60.42), jamais en fil direct.
6. **Porte** : S1 (AU), **S4** (bouton de réarmement XB4BA21, noir, **non lumineux**, 03/11), H2 (voyant 230 V, référence à relever), H3 (voyant 24 V présent), H4 (voyant défaut). H2 en 230 V sur la porte : **tresse de masse de porte** (revue des achats C11).
7. **Fusible FA1** (04/11) : porte-fusible Mersen CMC101 (1P 10x38) + cartouche gG 4 A, juste en amont des contacts de sécurité de KA1. Nouvel appareil sur le rail.
8. **Bornes de terre vert/jaune** (03/11) : X10.11 (PE arrivée), X31.11 et X32.11 (PE moteurs), X50.13 (FE de l'IHM).
9. **Câbles** : moteurs 4G2,5 blindés (2XSLCY-K) ; frein **LIYCY-JZ 5G1,5 blindé** (W3 / W6) ; sonde TF 2x0,75 blindé (W4 / W7) ; pas-à-pas 4 conducteurs blindés (W9 / W10) ; thermocouple, câble de compensation K (W8) ; 19G1 et 27G1 vers la machine et le pupitre ; câble client 5G4 (W1). **Blindages repris à 360°** : presse-étoupes CEM et reprises de blindage dans l'armoire (revue des achats C2, C3).
10. **Non dessinés au schéma mais présents dans l'armoire** : répartiteur 4P 125 A (AEE300427) et bornier de terre Legrand 404839. Ils sont à implanter. Leurs anciens repères X12 / X13 entrent en conflit avec les bornes X12.11 (règle du 02/11) : **demande leur repère à Julien**.
11. **Achetés mais non utilisés** (ne pas implanter, voir revue §5) : NFT816, GV2ME10, relais Finder 22 et socles, XB5AD25, répartiteur RS 868-0720, LADN11, A9F74203 / A9F74201.
12. **R1 / R2** (résistances de freinage SEW BW100-001) : dans l'armoire. **Ne jamais proposer de les déplacer** (consigne de Julien). Elles chauffent : à placer en conséquence.

## 5. Inventaire v16 (extrait de la nomenclature du 04/11)

Localisations du schéma : **+A1** armoire (IDE 1800 × 1200 × 400), **+P1** pupitre posé sur la machine, **+M** machine. « Porte » = porte de +A1.

### Armoire +A1, sur la plaque de fond
| Repère | Matériel |
|---|---|
| QS1 | Legrand Vistop 022515, 4P 63 A (manœuvre) |
| QF1 | Hager NFT820, 3P+N 20 A C |
| (repère à fixer) | Répartiteur 4P 125 A AEE300427 et bornier de terre Legrand 404839 (non dessinés au schéma ; anciens X12 / X13) |
| QM1 / QM2 | Schneider GV2ME14 |
| KM1 / KM2, KF1 / KF2, KA2 | Schneider LC1D09BD (5 contacteurs) |
| QF2 / QF3 | Schneider iC60N A9F74202, 2P 2 A C |
| QF4 / QF5 | Hager NFT706, 1P+N 6 A C |
| QF6 | Schneider iC60N A9F75204, 2P 4 A D |
| QF7 / QF8 | Hager NFT702, 1P+N 2 A C |
| QF9 | IMO B6CR1N1630A, différentiel 1P+N 16 A 30 mA |
| QF10 | Schneider iDT40K A9P71606, 1P+N 6 A C |
| XD1 | Prise de service Legrand 004280, 2P+T 16 A |
| T1 / T2 | RS PRO 284-0491, 24 V 240 W |
| T3 | Mean Well NDR-240-48, 48 V 240 W |
| U1 / U2 | SEW MCX91A-0055-5E3 (variateurs 2,2 kW) |
| R1 / R2 | SEW BW100-001 (résistances de freinage) |
| U3 / U4 | Jkongmotor JKDM860H (drivers pas-à-pas) |
| KA1 | Schneider XPSUAF13AP (relais de sécurité) |
| FA1 | Mersen CMC101 + cartouche gG 4 A |
| K1 | Siemens CPU 1214C G2 6ES7214-1AH50-0XB0 |
| K2 | Siemens SM 1223 G2 6ES7223-5BH50-0XB0 |
| K3 | Siemens SM 1231 TC G2 6ES7231-5QF50-0XB0 |
| K4 | Switch Weidmüller 2682250000 (5 ports) |
| X21.11 / X21.12 / X21.13 | Blocs de distribution Phoenix PTFIX 6X1,5 (24VELEC, 0 V, 24VSEC) |
| EL1 / EL2 | RS PRO 194-0417, éclairage LED |
| EV1 / EV2 | IDE VF92AC, ventilateurs 230 V |

### Porte de +A1
S1 (AU XB5AS8442 + ZBE102 + ZBE101 : 2 NF + 1 NO), S4 (XB4BA21), H2 (230 V, référence à relever), H3, H4 (voyants 24 V).

### Hors armoire
- **+P1 pupitre** : P1 (IHM Siemens KTP700 Basic PN), S2 (AU), S3 (sélecteur Eaton T0-4-8223/E Auto / Manu).
- **+M machine** : M1 / M2 (SEW K39 DRN100LS4 / BE5 / TF), M3 / M4 (StepperOnline 34IP65-85), B1 (capot mécanique), B2 (ifm MN508S, codé), B3 à B6 (fins de course).
- **À confirmer avec Julien** : la nomenclature place H1 (colonne 3 couleurs) et B7 (thermocouple) dans +A1, mais la revue des achats les met côté machine (H1 dans le 19G1).
- TR1 (TEMCo 15 kVA) : variante US, **hors armoire**.

### Bornes (80 au schéma v16)
| Groupe | Nb | Fonction | Destination |
|---|---|---|---|
| X10.11 à X10.15 | 5 | Arrivée réseau (X10.11 = PE vert/jaune) | réseau (W1) |
| X12.11 | 1 | Liaison PELV 0 V - PE (borne sectionnable prévue, non achetée : revue B4) | interne |
| X20.11 à X20.24 | 8 | Moteurs pas-à-pas M3 / M4 | +M |
| X21.11 à X21.13 | 3 | Blocs de distribution 24 V (PTFIX, 6 points chacun) | interne |
| X31.11 à X31.32 | 8 | M1 : moteur (X31.11 = PE vert/jaune), sonde TF, frein | +M |
| X32.11 à X32.32 | 8 | M2 : idem (X32.11 = PE vert/jaune) | +M |
| X41.11 à X41.44 | 16 | AU voies 1 et 2, shunts Manu, capots B1 / B2 | +P1 et +M |
| X41.51 à X41.54 | 4 | AU armoire S1 | porte |
| X42.11 à X42.16 | 6 | Sélecteur S3 | +P1 |
| X50.11 à X50.13 | 3 | Alimentation IHM (X50.13 = FE vert/jaune) | +P1 |
| X60.11 à X60.38 | 14 | AU pupitre (NO), sélecteur, fins de course | +P1 et +M |
| X60.41 / X60.42 | 2 | AU armoire S1 (NO) | porte |
| X63.11 / X63.12 | 2 | Thermocouple (type de borne à définir) | +M |

Achat : 70 bornes PT 2,5 + 15 PT 4 + bornes de terre vert/jaune. Revue C6 : besoin 81 avec 4 bornes pour H1, réserve faible (moins de 10 %).

## 6. Questions à poser à Julien (au plus 3-4 par message)

Pose d'abord celles qui bloquent le dessin, par exemple :
1. Ta dernière version d'implantation : où est-elle, de quand date-t-elle ? Qu'est-ce qui est **déjà monté** dans l'armoire (rails, goulottes, appareils) ?
2. Cotes utiles : plaque de fond (largeur × hauteur), porte, position des entrées de câbles (bas ? presse-étoupes sur quelle face ?).
3. Organisation voulue : zones (puissance en haut, commande au milieu, borniers en bas ?), place des variateurs et des résistances, sens du flux d'air EV1 / EV2.
4. Disposition de la porte : S1, S4, H2, H3, H4 (hauteurs, alignement).
5. H1 et B7 : dans l'armoire ou sur la machine ? Repères du répartiteur et du bornier de terre (anciens X12 / X13) ?
6. Réserve de place souhaitée sur les rails et dans les goulottes.
7. Dimensions des appareils : à prendre sur les fiches fabricant. Si une fiche manque, demande-la, ne devine pas.

## 7. Règles de dessin et bonnes pratiques

À appliquer, sauf avis contraire de Julien. Chaque fois, demande-lui s'il est d'accord.
- Séparer puissance (400 / 230 V), très basse tension (24 / 48 V) et sécurité. Câbles moteurs et frein loin des signaux (PROFINET, thermocouple, sonde TF).
- Variateurs et résistances de freinage : respecter les dégagements de la notice SEW. Résistances loin des automates et des alimentations.
- Borniers en bas de l'armoire, groupés par destination (+M, +P1, porte), près des entrées de câbles.
- Reprises de blindage à 360° au plus près de l'entrée des câbles blindés.
- Repères identiques au schéma v16, sur chaque appareil et chaque groupe de bornes.
- Indique les cotes que tu as utilisées et leur source.

## 8. Dépôt Git : ton dossier

Idée de Julien (04/11), approuvée par l'assistant du schéma : ton travail est versionné dans le **même dépôt**, dans un dossier à toi seul.

```
implantation/
  README.md          règles du dossier (déjà créé)
  release/           la dernière version seule : TTK_implantation_AAAA-MM-JJ_vN.drawio + .pdf
  old/               toutes les versions précédentes (y compris celles d'avant le dépôt)
  JOURNAL.md         une entrée par version : date, ce qui change, questions posées, réponses de Julien
```

Règles :
1. `git pull` avant de commencer, puis de nouveau juste avant de pousser (`git pull --rebase`).
2. Tu ne modifies **que** le dossier `implantation/`. Ne touche jamais à `schema/`, `outils/`, `memoire/`, `docs/` (un autre agent y travaille).
3. Mets tes anciennes versions dans `implantation/old/`, la nouvelle seule dans `implantation/release/`. À chaque nouvelle version, déplace la précédente avec `git mv`.
4. Un commit par version, message clair en français, par exemple « implantation v3 : FA1, bornes de porte, bornes de terre ». Puis `git push` sur `main`. **Jamais de `--force`.**
5. Ne pousse rien sans l'accord de Julien sur le contenu de la version.

## 9. Ce que tu livres à la fin

- `implantation/release/TTK_implantation_AAAA-MM-JJ_vN.drawio` et son export PDF ;
- l'entrée correspondante dans `implantation/JOURNAL.md` ;
- dans ta réponse à Julien : le lien du commit, les changements, les points « à vérifier » et tes questions.
