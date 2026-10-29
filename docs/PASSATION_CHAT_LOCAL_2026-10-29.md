# TTK : passation complète vers l'assistant local (schéma électrique WinRelais)

> **À lire en entier avant de répondre à Julien.**
> Rédigé le 29/10/2026 par l'assistant de la session cloud (Claude Code, dépôt GitHub) qui a travaillé avec Julien du 26 au 28/10/2026.
> Fichiers joints par Julien avec ce document :
> - `TTK_2026-10-28_v5.xrs` : **ouvert et enregistré par Julien** dans WinRelais. Il y a lancé la numérotation automatique du **folio 12 uniquement** (test).
> - `TTK_2026-10-28_v6.xrs` : dernière version générée, **pas encore ouverte** dans WinRelais.
>
> Statut des informations : **[D]** décision de Julien, **[C]** confirmé sur document ou fournisseur, **[H]** hypothèse ou proposition de l'assistant, **[?]** ouvert.

---

## 0. Comment travailler avec Julien (à respecter)

**Qui est Julien**
- Ingénieur en électronique et électrotechnique, **seul ingénieur** de BEBL (Bureau d'Études Bailly Levert, Trappes).
- Il fait tout : schéma, achats, câblage, programme, essais, documentation.
- Il a les bases en automatisme, mais **n'a jamais programmé d'automate en conditions réelles**.

**Comment lui répondre**
1. **En français.** Phrases courtes, voix active, contenu concret. « Trop de texte » est un défaut pour lui.
2. **Zéro donnée inventée.** Chaque valeur technique cite sa source ; sinon, on écrit « à vérifier ».
3. **Signaler toute incohérence**, y compris entre ses messages et l'historique : « Incohérence : le X tu disais A, aujourd'hui B. Lequel retenir ? ».
4. **Poser les questions avant de supposer** : au plus 3 ou 4 questions numérotées, regroupées dans un seul message.
5. **Remettre en question ses choix** quand la norme, la sécurité ou la fiabilité le justifient. Donner la raison et une alternative une seule fois, **puis respecter sa décision**. Il décide.
6. **Faire avec l'existant.** Le matériel est commandé et en grande partie reçu, l'armoire est en montage. On n'ajoute du matériel qu'en cas de vraie nécessité. On ne propose jamais de déplacer les résistances de freinage.
7. **Travailler par blocs** : Julien valide un bloc avant qu'on passe au suivant.
8. **Tracer** chaque échange et chaque décision (voir le §2 sur le dépôt).
9. **Ne jamais modifier le .xrs de travail directement.** Le schéma est généré par script (voir le §2). En local, ne travailler que sur une **copie**, avec WinRelais **fermé**.
10. **Pas de marquage CE** : c'est accepté par le client. Les normes (IEC 60204-1, EN ISO 13849-1, 13850, 14119, 14118, 12100) servent de bonne pratique.

**Personnes**
- **Nicolas** : dirigeant de BEBL.
- **Nicolas Ghut** : client TTK.
- **Hugo** : passe les commandes, chez Levert Industrie.
- **Julien Rimoux** : installation électrique du site client.
- **Samir** (WAGO) : équivalences borniers.
- **Deux amis relecteurs** : un électricien et un automaticien, le soir.
- **Deux stagiaires** câbleront l'armoire.

---

## 1. Projet

**La machine**
- **Machine de tressage TTK** : elle tresse du caoutchouc autour d'un câble, en ligne avec une tête d'extrusion Microdia (hors périmètre, sauf la mesure de sa température).
- **Deux motoréducteurs SEW** K39 DRN100LS4/BE5/TF (2,2 kW, frein BE5 400 V CA, sonde TF). Chacun a son variateur MCX91A (STO, PROFINET). Ils tournent en sens opposés, à des vitesses indépendantes de 30 à 137 tr/min.
- **Mode Manu (nettoyage)**
  - Les moteurs SEW ne sont jamais alimentés.
  - Chaque motoréducteur est translaté par un **moteur pas-à-pas** : drivers DM860H en 48 V, moteurs Nema 34. Un axe à la fois, commande maintenue depuis l'IHM.
  - Le capot s'ouvre librement en Manu.
- **Mode Auto (production)** : l'ouverture du capot vaut un AU.

**Postes et alimentation**
- Trois localisations : **+A1** armoire (IDE 1800×1200×400), **+P1** pupitre posé sur la machine (IHM KTP700, AU, sélecteur Auto/Manu), **+M** machine.
- **Réseau UE** : 400 V 3P+N+PE, TN-S.
- **Variante US** : transformateur TEMCo 15 kVA placé hors armoire, fourni par BEBL et installé par le client.
- **Automate** : Siemens S7-1200 **G2** (CPU 1214C DC/DC/DC, SM 1223 8DI/8DQ, SM 1231 TC), programmé sous TIA Portal V21 **Basic**.

**Planning** (validé le 20/10)

| Jalon | Date |
|---|---|
| J1 folios terminés | 05/11 |
| J2 bon pour câblage | 13/11 |
| J3 armoire 1 sous tension | 26/11 |
| J4 moteurs pilotés | 28/11 |
| J5 programme | 14/12 |
| J6 machine 1 testée | 23/12 |

Livraison de la machine 1 au plus tard le 22/01/2027.

---

## 2. Méthode de travail, dépôt GitHub, génération

### 2.1 Le dépôt
- **Dépôt** : https://github.com/JulienBEBL/TTK-SCHEMA-ELEC (branche `main`). Tout y est versionné et tracé.

| Dossier / fichier | Contenu |
|---|---|
| `outils/ttk_schema.py` | **Description complète du schéma** : folios, symboles, fils, renvois, notes, contrôles, nommage. **C'est la source de vérité.** |
| `outils/xrs_gen.py` | Générateur `.xrs` (UTF-8 avec BOM, fins de ligne CRLF) et contrôles géométriques |
| `outils/xrs_tool.py` | Lecture et vérification : `python xrs_tool.py verifier|resume|nomenclature|json fichier.xrs` |
| `outils/xrs_edit.py` | Édition ciblée d'un `.xrs` existant (non utilisée depuis la v1) |
| `outils/lire_tableau.py` | Lecture de `TTK_Plan_Folios_Reperes.xlsx` |
| `outils/apercu_xrs.py` | Aperçu PNG approximatif d'un folio (matplotlib) |
| `outils/reconstruire_librairie.py` + `outils/librairie/` | Symboles `.xsy` **reconstruits** depuis un `.xrs` (la session cloud n'a pas la librairie WinRelais) |
| `livrables/TTK_Plan_Folios_Reperes.xlsx` | Classeur de Julien (onglets Repères, Folios…) : **non modifié** par l'assistant |
| `livrables/MAJ_Reperes_2026-10-27.csv` | Changements à reporter à la main dans le classeur (à compléter avec le nommage du 28/10) |
| `schema/modele/SCHEMA_ELEC_TTK.xrs` | Modèle (en-tête, cartouche) |
| `schema/generes/` | v1 à v6, avec leur rapport de vérification et leur nomenclature |
| `schema/recus/` | `.xrs` reçus de Julien, datés, dont `2026-10-28_v5_numerotation_f12.xrs` |
| `docs/DECISIONS.md` | **Journal des décisions** ([D] [C] [H] [?]), à jour au 28/10 |
| `docs/JOURNAL_ECHANGES.md` | Traçabilité des échanges |
| `docs/NOMMAGE_2026-10-28.md` | Table ancien → nouveau repère |
| `docs/ARCHITECTURE_SECURITE_2026-10-27.md` | Fiche sécurité de Julien et écarts relevés |
| `docs/GENERATION.md`, `docs/RECAP_2026-10-27.md` | Méthode de génération ; récap du 27/10 (complété par ce document) |
| `docs/local/` | Fichiers .md du PC de Julien : `FORMAT_XRS.md`, `METHODE_BORNIERS.md`, base Claude Code du 22/10 |

### 2.2 Boucle de travail (décision de Julien du 27/10)
1. L'assistant modifie `ttk_schema.py` et régénère un `.xrs` daté et versionné (`TTK_AAAA-MM-JJ_vN.xrs`).
2. Julien l'ouvre dans WinRelais, lit le **Journal** d'ouverture et renvoie ses retours (captures, texte).
3. L'assistant corrige le script, régénère, puis met à jour `DECISIONS.md` et `JOURNAL_ECHANGES.md` (commit + push).

> **Piège majeur** : toute retouche faite à la main dans WinRelais est **écrasée** à la régénération suivante. Elle doit être décrite à l'assistant ou reportée dans `ttk_schema.py`. On n'arrêtera de régénérer qu'au passage en finition manuelle, décision qui sera notée.

### 2.3 Régénérer en local (PC de Julien)
```
cd outils
set TTK_LIB=C:\Users\Public\Documents\Elec-CAO\sym_electrotech
set TTK_DATE=29/10/2026
python ttk_schema.py ..\schema\generes\TTK_2026-10-29_v7.xrs
python xrs_tool.py verifier ..\schema\generes\TTK_2026-10-29_v7.xrs
```

**Ce que doit afficher le script**
- La ligne « 0 problème(s) de contrôle ».
- Le contrôle couvre la géométrie, les chevauchements de textes et de renvois, les équipotentielles voulues (listes `MEMES` et `DIFFERENTS`) et les courts-circuits.

**Librairie de symboles**
- Sans `TTK_LIB`, le script prend `outils/librairie/` (symboles reconstruits).
- Les contacts `RC Contact NO 63-64 / 73-74 / 83-84` ont été **créés** par copie du 53-54. S'ils manquent dans la vraie librairie, garder ceux du dépôt.

**Dépendances** : Python 3 ; `matplotlib` seulement pour l'aperçu ; `openpyxl` n'est pas nécessaire (le classeur est lu en zip/xml).

### 2.4 Principes du générateur, à connaître avant de modifier
- **Unités** : 1/100 mm. Grille de 400 (4 mm). Y vers le bas.
- **Rails** : +24 V en haut (y = 2000), 0 V en bas (y = 19000), PE à y = 19400, chaînés de folio en folio par renvois.
- **Repères internes** : le script garde les **anciens repères du classeur** (Q121, T201, K401…). La fonction `ren()` et le dictionnaire **`RENOMME`** les traduisent à l'écriture : repère, champs, textes, câbles, descriptions de folio. **Pour renommer un appareil, on ne modifie que `RENOMME`.**
- **Centrage** : le contenu des folios 10 à 69 est recentré automatiquement (`g.centrer`). Les coordonnées affichées dans les messages du contrôle sont **après centrage**, celles du code **avant**.
- **Renvois** : flèche et texte d'environ 16 mm au-delà du point, du côté opposé au fil. Le point de renvoi doit être au bout d'un fil droit. Deux renvois voisins doivent être espacés d'au moins 4,4 mm.
- **Notes** : une zone de notes encadrée par folio, via `notes(...)`. Une ligne qui commence par « ! » s'écrit en rouge : c'est un point à vérifier.
- **Étiquettes centrées** sur un groupe de renvois : `etiquette(...)`.
- **Références croisées** : le générateur n'en crée pas (RefCroise = -1). Il faut lancer **« Références croisées automatique »** dans WinRelais après ouverture.

---

## 3. Fichiers joints : v5 et v6

### 3.1 v5 (ouverte par Julien, numérotation de test sur le folio 12)
Julien a lancé la numérotation automatique de WinRelais sur le folio 12. L'assistant a relevé le **format de la section `¤#Numero¤`** :
```
x·y·TEXTE·indexFolio·0·Arial·300·angle·8388608·0·0·0·
ex. 3600·5800·1·6·0·Arial·300·90·8388608·0·0·0·
```
- Une étiquette par tronçon de fil, au milieu du segment, angle 90 pour un fil vertical. La couleur 8388608 correspond au bleu marine.
- **Au réenregistrement, WinRelais modifie aussi le fichier** : il réordonne et inverse certains segments de fils, change le compteur et des drapeaux internes (`Abr.·1·1·1·n`, index des symboles support). Ce n'est pas une erreur.

### 3.2 Ce qui change de la v5 à la v6
- **Folio 32**
  - -KM3 coupe le **+48 V seul, avec un pôle** (5/L3 → 6/T3) [D]. Le 0 V 48 n'est plus coupé : il va directement de -T3 à -X35.
  - Un fil par driver depuis -X34 et -X35, **sans point de dérivation** [D]. Il reste des croisements sans jonction.
  - Les borniers n'affichent que leur repère ; leur description est dans la zone de notes.
- **Numérotation (convention A, Julien)**
  - Les fils de puissance portent le **nom de leur phase : L1, L2, L3 ou N, sans différenciation** [D].
  - La phase est connue aux départs du répartiteur -X12 (1x = L1, 2x = L2, 3x = L3, Nx = N), puis propagée à travers les pôles des disjoncteurs et contacteurs (`nommer_phases()`). Résultat : 84 noms posés, du folio 10 au folio 21.
  - Les autres fils ne sont **pas numérotés** tant que le schéma n'est pas fini.
- **Folio 70** : rectangles de 6 × 12 mm, chacun repéré (1..n et PE, U V W PE, 1b 2b, 2 3, 1..8, L1 L2 L3 N PE).
- **Folio 71** : tableau agrandi (lignes de 6 mm, police de 2,5 mm).

### 3.3 À vérifier par Julien à l'ouverture de la v6
1. Le Journal d'ouverture : aucun message attendu.
2. Les étiquettes L1/L2/L3/N sont-elles **reconnues comme numéros de fil** et rattachées aux fils, et non comme du texte libre ?
3. Faut-il aussi une étiquette sur les tronçons courts (moins de 8 mm, entre un renvoi et une borne) ? Aujourd'hui, ils n'en ont pas.
4. La lisibilité des folios 32, 70 et 71.

---

## 4. Repérage (décision de Julien du 28/10)

**Règle**
- **Lettres de fonction + numéro d'ordre dans la fonction**, dans le sens de l'énergie et selon l'implantation.
- **-KM1 / -KM2** pour les contacteurs des moteurs SEW, **-KF1 / -KF2** pour les freins (choix de Julien).
- **Borniers par groupe de fonction** : X1x puissance, X3x très basse tension, X70 machine, X71 pupitre.
- Repères écrits sans « - » dans le `.xrs`.
- **Maître et esclaves** : le maître porte la référence fabricant et compte en nomenclature. L'esclave (contact, pôle, partie d'appareil) a le même repère, sans référence. Une bobine est maître de ses pôles et de ses contacts.

| Préfixe | Appareils |
|---|---|
| QS | sectionneur : QS1 |
| QF | disjoncteurs : QF1 tête ; QF2 / QF3 freins ; QF4 / QF5 alimentations 24 V ; QF6 alimentation 48 V ; QF7 ventilateurs ; QF8 éclairage ; QF9 différentiel prise ; QF10 limitation prise |
| QM | disjoncteurs moteur : QM1 / QM2 (GV2ME14, variateurs) |
| KM | KM1 / KM2 contacteurs amont variateurs ; KM3 contacteur 48 V (classé KM parce qu'il alimente les pas-à-pas, nom à confirmer par Julien) |
| KF | KF1 / KF2 contacteurs de frein |
| KA | KA1 relais de sécurité |
| K | K1 CPU, K2 SM 1223, K3 SM 1231 TC, K4 switch PROFINET |
| U | U1 / U2 variateurs, U3 / U4 drivers pas-à-pas |
| T / TR | T1 alimentation +24 V COMMANDE, T2 alimentation +24 V ELEC, T3 alimentation 48 V ; TR1 transformateur US |
| M / R | M1 / M2 motoréducteurs, M3 / M4 pas-à-pas ; R1 / R2 résistances de freinage |
| S | S1 AU armoire, S2 AU pupitre, S3 sélecteur Auto/Manu, S4 réarmement |
| B | B1 capot mécanique, B2 capot magnétique, B3 à B6 fins de course, B7 thermocouple |
| H / P | H1 colonne, H2 voyant 230 V, H3 voyant 24 V ELEC, H4 voyant défaut ; P1 IHM |
| EV / EL | EV1 / EV2 ventilateurs, EL1 / EL2 éclairage |
| X | X11 arrivée, X12 répartiteur, X13 bornier PE, X14 prise ; X31 +24 V ELEC, X32 0 V, X33 +24 V COMMANDE, X34 +48 V, X35 0 V 48, X36 liaison PELV ; X70 machine, X71 pupitre |
| W | W1 câble client (5G4) ; W2 / W3 / W4 moteur / frein / TF de M1 ; W5 / W6 / W7 pour M2 ; W8 thermocouple |

Table complète ancien → nouveau : `docs/NOMMAGE_2026-10-28.md`. **Le classeur Excel n'est pas encore à jour** de ce nommage.

---

## 5. Architecture électrique (état de la v6)

### 5.1 Puissance (folios 10 à 13)
- **Arrivée**
  - Câble client **W1 5G4 mm²** [D], bornes X11, sectionneur QS1 (Legrand Vistop 63 A, manœuvre armoire ouverte), disjoncteur de tête QF1 (Hager NFT820, 20 A courbe C).
  - **Parafoudre supprimé** [D].
  - Transformateur US TR1 dessiné en variante.
- **Répartiteur X12**
  - Départs : 1x = L1, 2x = L2, 3x = L3, Nx = N.
  - Les départs libres **35 (L3) et N4** alimentent le **voyant 230 V H2** (présence tension), dessiné au folio 13.
  - H2 n'est protégé que par QF1 (20 A) : **câblage en 2,5 mm²**. C'est une information seulement, pas une vérification d'absence de tension.
- **Folio 12**
  - QM1 / QM2 (GV2ME14, réglés à 6,5 A) → KM1 / KM2 → variateurs.
  - QF2 / QF3 (iC60N 2P 2 A, courbe C) → KF1 / KF2 → freins. **Freins alimentés côté CA, indépendamment du variateur.**
- **Folio 13**
  - QF4 / QF5 → alimentations 24 V ; QF6 → alimentation 48 V.
  - QF7 → ventilateurs EV1 / EV2 ; QF8 → éclairage EL1 / EL2.
  - QF9 (différentiel 30 mA) → QF10 (limitation à 6 A) → prise X14.

### 5.2 Variateurs (folios 20 et 21)
- **Variateurs** U1 / U2 (MCX91A), résistances R1 / R2 (BW100-001), moteurs M1 / M2.
- **Câbles moteur**
  - W2 / W5 moteur : 4G2,5 blindé.
  - W3 / W6 frein : **2G1,5**, 400 V CA.
  - W4 / W7 sonde TF : **2G1 blindé**, vers X10 du variateur.
- **X5** (24 V de sauvegarde) sur le **+24 V ELEC** [D].
- **STO** (X6) : vient du folio 42.
- **PROFINET** (X40) : renvoi vers le folio 54.
- **[D] Moteurs, freins et TF passeront par le bornier X70** (validé le 28/10, remplace le raccordement direct du 27/10). **Pas encore câblé aux folios 20 / 21 : à faire en v7.** Les blindages se reprennent sur un étrier, pas sur une borne.
- **[?] Affichage « câble blindé »** dans WinRelais : on ne connaît pas le champ correspondant dans le format `.xrs` (voir le §9).

### 5.3 Très basse tension (folios 30 à 32)
- **Deux alimentations 24 V (RS PRO 284-0491, 10 A)**
  - **T2 = +24 V ELEC** : automate, IHM, switch, alimentation A1 du relais de sécurité, X5 des variateurs, voyant H3.
  - **T1 = +24 V COMMANDE** : contacts 13 / 23 / 33 de KA1 (donc les bobines) et sorties 3L+ du module K2 (colonne, voyants).
  - Renvois entre les folios 31, 40 et 52.
  - **Aucune des deux n'est coupée par l'AU** : l'AU agit uniquement par les contacts de KA1. Pendant un AU, la colonne reste alimentée et peut afficher le rouge.
- **0 V commun** aux deux alimentations [D]. Explication portée sur le folio 30 : c'est nécessaire, et les deux +24 V ne doivent **jamais** être mis en parallèle.
- **PELV** : une liaison unique 0 V – PE par la **borne sectionnable X36.1** (folio 30).
- **Folio 31** : borniers X31 (+24 V ELEC), X33 (+24 V COMMANDE), X32 (0 V) en colonne, chacun avec un **cadre vide pour l'image du bornier**, que Julien insérera. Le voyant H3 (+24 V ELEC présent) est en porte.
- **Folio 32 : 48 V** [D]
  - T3 (Mean Well NDR-240-48) → **KM3, 1 pôle sur le +48 V** → X34 (+48 V) → un fil par driver.
  - 0 V 48 en direct de T3 → X35 → un fil par driver.
  - La bobine de KM3 est alimentée **uniquement en Manu**, par le contact Manu-D, depuis la sortie 13-14 de KA1. Conséquence : le 48 V est coupé par l'AU et absent en Auto.
  - **[?] Pouvoir de coupure DC-1 du LC1D09BD sous 48 V** : à vérifier sur la notice.

### 5.4 Sécurité (folios 40 à 43) : architecture du 27/10 (fiche de Julien), appliquée
- **Relais KA1**
  - Schneider **XPSUAF13AP**, arrêt de catégorie 0, PL d visé, démarrage surveillé par S4.
  - Boucle de retour Y1-Y2 : NF miroir de KM1, KM2, KF1, KF2 et KM3, puis S4.
  - Alimentation A1 sur le +24 V ELEC ; contacts 13 / 23 / 33 sur le +24 V COMMANDE.
- **Entrées (folio 41)**
  - Voie 1 : S11 → S1 NF1 → X71.1 → S2 NF1 → X71.2 → [X70.1 → **B1** NF (capot mécanique, ouverture positive) → X70.2] **en parallèle avec** [X71.13 → **Manu-A** → X71.14] → S12.
  - Voie 2 : idem avec NF2, [X70.5 → **B2** (capot magnétique **codé ifm MN508S**, 2 NO + 1 NF, M12, 50 mA, un NO en voie 2) → X70.6] en parallèle avec [X71.15 → **Manu-B** → X71.16] → S22.
  - Un contact Manu par voie, jamais un contact commun.
- **Sorties (folio 42), affectation figée par l'assistant** (Julien ne savait pas). Le STO a une sortie dédiée qui ne coupe que quelques mA, donc pas d'usure du contact.
  - **13-14** → bobines KF1 et KF2 (freins), puis X71.19 → **Manu-D** → X71.20 → bobine KM3 (48 V en Manu seulement).
  - **23-24** → X71.7 → **Auto-A** → X71.8 → bobines **KM1 / KM2**. **Pas d'ordre automate** (option A du 27/10, relais K511 supprimé). KM1 / KM2 se ferment dès que le relais est armé en Auto ; l'arrêt de service se fait par la rampe et le STO.
  - **33-34** → X71.9 → **Auto-B** → X71.10 → **STO des deux MCX91A en parallèle**. X6:1 et X6:3 sont reliés à la même sortie, ce qui est validé par SEW.
- **Sélecteur S3** (Eaton T0-4-8223/E, à cames, sans clé ni cadenas)
  - Essai de Julien : **4 contacts NO par position**, 8 au total. Position 1 = Auto, position 2 = Manu. **Numérotation des bornes provisoire.**

| Contact | Bornes | Position | Rôle | Bornes X71 |
|---|---|---|---|---|
| Auto-A | 13-14 | Auto | KM1 / KM2 | 7-8 |
| Auto-B | 23-24 | Auto | STO | 9-10 |
| Auto-C | 33-34 | Auto | automate I0.4 | 11-12 |
| Auto-D | 43-44 | Auto | réserve | — |
| Manu-A | 53-54 | Manu | shunt capot voie 1 | 13-14 |
| Manu-B | 63-64 | Manu | shunt capot voie 2 | 15-16 |
| Manu-C | 73-74 | Manu | automate I0.5 | 17-18 |
| Manu-D | 83-84 | Manu | bobine KM3 (48 V) | 19-20 |

- **Folio 43** : tableaux des contacts, comportement par état, transitions, points à vérifier, risques résiduels.

| Sélecteur | Capot | AU | Freins | 48 V | KM1 / KM2 | STO |
|---|---|---|---|---|---|---|
| Auto | fermé | OK | alimentés | coupé | fermés | libéré |
| Auto | ouvert | OK | coupés | coupé | coupés | actif |
| Manu | ouvert ou fermé | OK | alimentés | alimenté | coupés | actif |
| tous | tous | enfoncé | coupés | coupé | coupés | actif |

### 5.5 Automate (folios 50 à 53) : liste d'E/S du 06/10, encore « à valider »

**CPU K1, entrées**

| Entrée | Signal |
|---|---|
| I0.0 | AU pupitre S2 (NO, via X71.5-6) |
| I0.1 | AU armoire S1 (NO) |
| I0.2 | Capot B1 (NO auxiliaire, 1 = ouvert) |
| I0.3 | Capot B2 (NF, 1 = ouvert) |
| I0.4 | Mode Auto (Auto-C) |
| I0.5 | Mode Manu (Manu-C) |
| I0.6 / I0.7 | Fins de course axe 1 min / max (B3 / B4, NF) |
| I1.0 / I1.1 | Fins de course axe 2 min / max (B5 / B6, NF) |
| I1.2 / I1.3 | Retours KM1 / KM2 |
| I1.4 | Retour KM3 |
| I1.5 | Diagnostic KA1 (borne absente du symbole) |

**CPU K1, sorties**
- Q0.0 / Q0.1 / Q0.2 : PUL / DIR / ENA du driver U3.
- Q0.4 / Q0.5 / Q0.6 : PUL / DIR / ENA du driver U4.
- Q0.3, Q0.7, Q1.0, Q1.1 : réserve.
- Le 3L+ de la CPU est sur le +24 V ELEC.

**SM 1223 K2**
- Q8.0 / Q8.1 / Q8.2 : colonne H1 (rouge / orange / vert).
- Q8.3 : voyant du bouton S4 (réarmement requis).
- Q8.4 : voyant défaut H4.
- 3L+ sur le **+24 V COMMANDE**. Entrées I8.x en réserve.
- L'alarme du switch **n'est pas câblée** [D].

**SM 1231 TC K3** : thermocouple type K **B7, câble de compensation W8 en direct jusqu'au module, sans borne** [D].

**Brochages G2 provisoires** : seuls les schémas des modules de génération 1 ont été trouvés. À valider sur le manuel G2.

### 5.6 PROFINET et pupitre (folios 54 et 60)
- **Switch K4** : chaque port a un fil et un renvoi vers son appareil, avec un renvoi retour sur l'appareil.
  - P1 → K1 port X1 P1 (folio 50) ;
  - P2 → U1 port X40 (folio 20) ;
  - P3 → U2 port X40 (folio 21) ;
  - P4 → P1 port X1 (folio 60) ;
  - P5 : réserve.
- **Type de fil provisoire** : « Autre tension DC » dessiné en vert (code `PN` dans `xrs_gen.TYPES`). **Un type de conducteur « PROFINET » est à créer** dans WinRelais (Préférences / Conducteurs).
- **Pupitre P1 (folio 60)** : IHM sur le +24 V ELEC, par les bornes X71.21 (L+), .22 (M) et .23 (FE). Le câble W711 est retiré. Mise en page aérée, avec une zone « contenu du pupitre ».

### 5.7 Borniers (folios 70 et 71)
- **Folio 70 (X70, armoire ↔ machine) : en construction, non attribué.** Les groupes sont dessinés comme de simples cadres repérés, sans symbole :
  - câble 19G1 (18 + PE) ;
  - câble 27G1 (26 + PE ; liaison machine ↔ armoire, répartition non attribuée) ;
  - sondes TF (2 × 2) ;
  - moteurs (2 × U V W PE) ;
  - freins (2 × 2) ;
  - capteur M12 à 8 broches ;
  - arrivée réseau (L1 L2 L3 N PE).
- **Bornes X70 déjà posées sur les folios fonctionnels** : 1 à 4 pour B1, 5 à 8 pour B2, 9 à 16 pour les fins de course B3 à B6.
- **Folio 71 (X71, armoire ↔ pupitre)** : tableau calculé depuis le schéma.
  - 1 à 4 : voies d'AU ;
  - 5 et 6 : AU pupitre vers l'automate ;
  - 7 à 20 : contacts du sélecteur ;
  - 21 à 23 : alimentation de l'IHM.
- Méthode : `docs/local/METHODE_BORNIERS.md` (une borne par conducteur qui sort, regroupée par câble ; bornier graphique généré par WinRelais).

---

## 6. Folio par folio : contenu et état

**Règle de Julien (28/10)** : une **pastille d'état**, petit carré plein en haut à droite de chaque folio.
- **Vert** : folio **validé par Julien**, c'est-à-dire tous ses éléments (symboles, tableaux, formes, textes).
- **Orange** : presque fini.
- **Rouge** : moins de 50 %.

Les états sont dans le dictionnaire `STATUT` de `ttk_schema.py`. **Aucun folio n'est vert à ce jour** ; les états actuels sont des propositions de l'assistant.

| N° | Titre | État | Reste à faire / remarques |
|---|---|---|---|
| 01 | Page de garde | orange | Insérer les logos TTK, BEBL et LEVERT INDUSTRIE dans les cadres. Tableau des indices supprimé (schéma en construction). |
| 02 | Sommaire | orange | Tableau pleine page, police 2,6 mm, colonne « indice » retirée. Description du cartouche « liste des folios et **indices de révision** » à corriger. |
| 03 | Légende et conventions | orange | Refait avec le nouveau repérage et les potentiels. Description du cartouche « IEC 81346-2 » à corriger. |
| 04 | Synoptique | rouge | Blocs texte avec les nouveaux repères. Vrai synoptique à faire. |
| 10 | Arrivée | orange | Description du cartouche qui mentionne encore « PARAFOUDRE » à corriger. W1 en 5G4. |
| 11 | Répartiteur | orange | Étiquettes centrées sous les renvois, en quinconce. Départs du voyant H2. |
| 12 | Distribution 400 V | orange | Étiquettes centrées. Noms de phase posés. **Folio de test de la numérotation.** |
| 13 | Distribution 230 V | orange | Voyant H2. Références de QF7 / QF8 « à définir ». |
| 20 / 21 | Variateurs | orange | **Passer moteurs, freins et TF par X70.** Affichage blindé. Bornes X6 / X10 à confirmer (notice SEW). |
| 30 | Alimentations 24 V | orange | PELV X36.1, note sur le 0 V commun. |
| 31 | Distribution 24 V | orange | Images des borniers à insérer. |
| 32 | 48 V | orange | DC-1 du LC1D09BD sous 48 V. Masquer les numéros de broches de U3 / U4. |
| 40 à 43 | Sécurité | orange | Points de la §8 (diagnostic KA1, plaque Eaton, antiparasites…). |
| 50 à 52 | Automate | rouge | Liste d'E/S à valider, brochages G2 provisoires. Description du cartouche f51 « contacteurs, freins » obsolète (les sorties ne pilotent plus les contacteurs). |
| 53 | SM 1231 TC | orange | Validé par Julien le 23/10, avant le renommage. À revalider. |
| 54 | PROFINET | orange | Type de conducteur PROFINET à créer. |
| 60 | Pupitre | orange | Repère du câble multiconducteur et du RJ45 à définir. |
| 70 | Bornier machine | rouge | En construction (§5.7). |
| 71 | Bornier pupitre | rouge | Tableau à regénérer après chaque modification. |
| 80 / 85 / 90 | Câbles, implantation, nomenclature | rouge | À générer par WinRelais (carnet de câbles, WinArmoire, nomenclature). |

---

## 7. Règles de dessin en vigueur

1. **Repérage** : voir le §4. Le maître porte la référence ; les esclaves ont le même repère, sans référence.
2. **Types de conducteur WinRelais**

| Type | Usage |
|---|---|
| `Puissance` | noir, phases |
| `Neutre Puissance` | bleu clair |
| `Conducteur terre` | vert-jaune, PE |
| `Commande 24VDC` | +24 V |
| `0V` | 0 V |
| `Autre tension DC` | orange : 48 V et sonde TF ; en vert (provisoire) : PROFINET |

   Ne jamais utiliser `Commande 24V~` (rouge, alternatif) sur un circuit continu.
3. **Numérotation des fils** : les fils de puissance portent le nom de leur phase (L1, L2, L3, N), sans numéro [D]. Le reste n'est pas numéroté avant la fin du schéma. Convention A pressentie : potentiels de distribution nommés (L1, L2, L3, N, PE, +24E, +24C, 0V, +48, 0V48), autres fils au format « folio.compteur ». **Format exact à arrêter avec Julien.**
4. **Zones de notes** : une par folio si nécessaire, points à vérifier en rouge.
5. **Pastilles d'état** : voir le §6.
6. **Pas de point d'intersection** : chaque appareil reçoit son propre fil depuis le bornier de distribution (demande de Julien sur le folio 32). Un croisement sans jonction est accepté.
7. **Un fil n'est raccordé que si son extrémité tombe exactement** sur la broche (aucun lien explicite fil ↔ broche dans le `.xrs`). Un symbole hors grille provoque des faux raccordements.

---

## 8. Points ouverts et à vérifier (ne jamais inventer de valeur)

**Sécurité**
1. Sortie de diagnostic statique du XPSUAF13AP : borne à lire sur la notice, à ajouter au symbole (chat symboles), puis à câbler sur I1.5.
2. Charge de la sortie 13-14 : 3 bobines LC1D09BD, à comparer aux 3 A en DC-13 de la notice.
3. Antiparasites des bobines LC1D09BD. **Éviter la diode simple sur KF1 / KF2**, qui retarde le serrage des freins : préférer une varistance ou un RC. Vérifier d'abord si un module est intégré.
4. Sélecteur Eaton :
   - photo de la plaque pour la numérotation réelle des bornes ;
   - recouvrement Auto / Manu à mesurer à la continuité (aucun contact Auto et Manu fermés en même temps) ;
   - courant minimal des contacts sous 24 V.
5. Capteur ifm MN508S :
   - homologation sécurité à confirmer sur la fiche ifm (EN 60947-5-3 / ISO 14119 ; RS ne cite que l'IEC 60947-5-1) ;
   - actionneur codé : commandé ?
   - brochage M12 8 broches ;
   - câble M12 (et non M8 comme noté au départ).
6. Contacts de l'AU XB5AS8442 : ZBE101 / ZBE102 sont-ils NO ou NF ?
7. Symbole « fin de course **NF** » (bornes 11-12) : le symbole posé est un NO.

**Puissance et variateurs**

8. Courant du frein BE5 : il fixe le calibre et la courbe de QF2 / QF3 (appel SEW).
9. Bornes X6 (STO) et X10 (TF) du MCX91A à confirmer sur la notice SEW.
10. Nombre de mises sous tension par heure du MCX91A : KM1 / KM2 ne doivent pas servir d'arrêt de service.

**Très basse tension**

11. DC-1 du LC1D09BD sous 48 V.
12. Polarité de l'entrée ENA du DM860H.

**Automate**

13. Liste d'E/S à valider.
14. Brochages G2 à confirmer.
15. PTO sur Q0.0 / Q0.4 à vérifier dans TIA V21.

**Divers**

16. Références de QF7 / QF8 à choisir.
17. KM3 : nom à confirmer par Julien.
18. Câble 27G1 : répartition entre machine et pupitre.
19. Repères des câbles multiconducteurs 19G1 / 27G1 et du câble RJ45 du pupitre.
20. Classeur Excel à mettre à jour avec le nommage du 28/10 (le script n'écrit pas dedans pour ne pas casser sa mise en forme conditionnelle).
21. Descriptions de cartouche obsolètes (f02, f03, f10, f51), venant du classeur.

**Risques résiduels inscrits au folio 43**
- Sélecteur sans clé ni cadenas, choix du client : le capot est shunté en Manu. L'IEC 60204-1 demande une sélection de mode protégée.
- Roue libre des moteurs si le sélecteur est tourné pendant la rotation (≈ 10 s, à mesurer).
- Un seul contact Manu-D pour le 48 V (PL c accepté pour la translation).

---

## 9. Demandes en attente auprès de Julien (dans WinRelais)

1. **Champ « câble blindé »** : cocher « blindé » sur le câble W2, enregistrer, envoyer le `.xrs`. On compare avec la version d'origine pour repérer le champ de la section `¤#DefCable`, puis on l'applique à W2 / W4 / W5 / W7 dans le générateur.
2. **Champ « afficher les numéros » des broches** : le décocher sur le driver U3, enregistrer, envoyer. On repère le champ de la ligne `¤#Broche` et on l'applique à U3 / U4.
3. **Ouverture de la v6** : messages du Journal, reconnaissance des noms de phase comme numéros de fil.
4. **États des folios** : lesquels passer au vert ?

---

## 10. Historique des versions générées

| Version | Date | Contenu principal |
|---|---|---|
| (base) | 22-23/10 | `test_xrs_claude.xrs` généré par la base Claude Code du 22/10 |
| v1 | 27/10 | Script rendu portable, librairie reconstruite ; câbles frein / TF séparés ; folios 41 / 42 refaits ; E/S du 06/10 ; colonne et voyants |
| v2 | 27/10 | Sécurité selon la fiche de Julien (sorties 1/2/3, 48 V en Manu par Manu-D), folio 43, zones de notes |
| v3 | 27/10 | Option A : KM1 / KM2 sans ordre automate (K511 supprimé) ; capteur B2 = ifm MN508S |
| v4 | 28/10 | Nouveau repérage ; parafoudre supprimé ; borniers X34 / X35 ; voyant 230 V H2 ; PELV X36.1 ; X5 et IHM sur 24 V ELEC ; renvois PROFINET ; folios 01 / 02 / 03 / 60 / 70 |
| v5 | 28/10 | +24 V ELEC / COMMANDE ; W1 en 5G4 ; étiquettes centrées sur f11 / f12 ; f70 avec l'arrivée réseau ; pastilles d'état |
| v6 | 28/10 | KM3 sur 1 pôle (+48 V seul) ; un fil par driver ; noms de phase sur les fils de puissance ; f70 repéré ; f71 agrandi |

Toutes les versions de la v1 à la v6 donnent « 0 problème » au contrôle interne et « 0 erreur » à `xrs_tool verifier`. Les 27 points d'attention restants sont normaux : repères en double sans référence croisée (à lancer dans WinRelais), et 0 V / PE sur le même potentiel à cause de la liaison PELV, ce qui est voulu.

---

## 11. Prochaines étapes proposées (v7)

1. Intégrer les retours de Julien sur la v6, puis les champs « blindé » et « afficher les numéros » dès réception.
2. **Câbler moteurs, freins et sondes TF par X70** aux folios 20 et 21. Mettre à jour le folio 70 (bornes attribuées) et les spécifications d'équipotentielles (`MEMES`).
3. Corriger les descriptions de cartouche obsolètes (f02, f03, f10, f51) : surcharger `FOL` dans le script ou les corriger dans le classeur.
4. Créer le type de conducteur PROFINET et l'utiliser.
5. Valider la liste d'E/S avec Julien (folios 50 à 52), puis passer ces folios à l'orange.
6. Mettre le classeur Excel à jour avec le nouveau nommage.
7. À la fin : références croisées, numérotation complète, génération des borniers, carnet de câbles et nomenclature dans WinRelais.
