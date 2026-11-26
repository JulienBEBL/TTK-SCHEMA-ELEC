# Journal des décisions TTK (schéma électrique)

Statut : [D] décision de Julien · [C] confirmé · [H] hypothèse · [?] ouvert

## 26/10/2026
- [D] Câbles moteurs SEW : câbles **séparés** pour le frein et la sonde TF.
  - Frein BE5 (bornes 2-3) : **2G1,5**.
  - Sonde TF (1b-2b, vers X10 du variateur) : **2G1 blindé**.
  - [D] Un repère par câble : -W201 moteur, -W202 frein, -W203 TF (f20) ; -W211, -W212, -W213 (f21). Remplace l'ancien -W202 / -W212 « frein + TF ».
  - Section du frein à valider une fois le courant du BE5 connu (appel SEW).
- [D] Dépôt GitHub = référentiel du projet (schéma, outils, livrables).

- [D] Règle de session : à chaque message, prendre en compte le contexte et les décisions, remettre en question quand c'est justifié, et tracer les échanges dans `docs/JOURNAL_ECHANGES.md`.
- [?] À commander : câbles 2G1,5 (frein, isolation ≥ 450/750 V car frein 400 V CA) et 2G1 blindé (TF), longueurs à définir (≈ distance armoire–moteur). Les 50 m de 2XSLCY-K 4G2,5 ne couvrent que U/V/W/PE.

## Structure du dépôt
- `schema/` : fichiers `.xrs` de travail ; `schema/recus/` : exports reçus, datés.
- `outils/` : scripts (`xrs_check.py`).
- `docs/` : décisions, base de connaissances.
- `folios/` : fiches de saisie par folio.
- `livrables/` : listes d'E/S, carnet de câblage, `macros/` WinRelaisExpert.

## 27/10/2026
- [D] Le `.xrs` est généré par script (`outils/ttk_schema.py`), Julien teste dans WinRelais et renvoie ses retours (voir `docs/GENERATION.md`).
- [D] Commutateur -S413 (Eaton T0-4-8223/E), essai de Julien : 4 contacts NO par position, 8 en tout. Affectation retenue : position 1 = Auto (13-14 STO, 23-24 ordre contacteurs, 33-34 information, 43-44 réserve), position 2 = Manu (53-54 et 63-64 pontage capot voies 1 et 2, 73-74 information, 83-84 réserve). Numérotation provisoire.
- [D] Voyants en porte : 2 minimum (tension, défaut), plus si place. Retenu : tension (-P512), défaut (-P513), réarmement lumineux bleu (-S414), plus colonne 3 couleurs (-P511).
- [D] Parafoudre non monté : entrée I1.5 libérée (réserve).
- [D] Câble 5G1,5 (LIYCY-JZ, 80 m) : réserve, plus affecté à l'IHM ni au sélecteur (remplacé par les multiconducteurs).
- [D] Symbole XB5AD25 : supprimé.
- [D] Câbles moteurs : Julien laisse le choix. Retenu : motor U/V/W, frein (2G1,5) et sonde TF (2G1 blindé) en direct armoire -> moteur, sans bornier intermédiaire (moins de connexions, CEM, blindage repris à 360°). Les bornes X701.17 à .24 disparaissent.
- [H] Appliqué sans confirmation (à valider) : Q12 / Q13 supprimés (déjà dans le script, décision du 04/10 ; remplacés par les contacts de -K401) ; liste d'E/S du 06/10 (S412 I0.0, S411 I0.1, fins de course I0.6 à I1.1, retours KM1 / KM2 / Q423 I1.2 à I1.4, I0.5 = mode Manu) ; sorties CPU Q0.0 à Q0.2 / Q0.4 à Q0.6 = PUL / DIR / ENA, Q0.7 = relais d'interface -K511 ; SM 1223 : Q8.0 à Q8.2 colonne, Q8.3 voyant réarmement, Q8.4 voyant défaut, I8.4 alarme switch.
- [H] Architecture sécurité f42 conforme au §3.5 : 13-14 STO des 2 variateurs, 23-24 + -S413 Auto + -K511 -> -KM1 / -KM2, 33-34 -> -Q421 / -Q422 / -Q423 (sans passer par -S413).

## 27/10/2026 (soir) : sécurité selon la fiche de Julien
- [D] Sorties -K401 : 13-14 freins (+ 48 V via Manu-D), 23-24 Auto-A + ordre automate -> -KM1 / -KM2, 33-34 Auto-B -> STO. Affectation 1/2/3 proposée, à valider.
- [D] 48 V pas-à-pas alimenté uniquement en Manu (Manu-D, 83-84). Remplace « -Q423 sur la sortie de sécurité en Auto et en Manu » (v1).
- [D] Contacts -S413 : Auto-A 13-14, Auto-B 23-24, Auto-C 33-34, Auto-D 43-44 (réserve), Manu-A 53-54, Manu-B 63-64, Manu-C 73-74, Manu-D 83-84 (numérotation provisoire).
- [D] Bornes -X711 : 1-6 AU, 7-8 Auto-A, 9-10 Auto-B, 11-12 Auto-C, 13-14 Manu-A, 15-16 Manu-B, 17-18 Manu-C, 19-20 Manu-D, 21-23 alimentation IHM.
- [D] Nouveau folio 43 « SECURITE - FONCTIONNEMENT » : contacts du sélecteur, états, transitions, points à vérifier, risques résiduels. Une zone de notes par folio de sécurité.
- I1.5 = diagnostic -K401 (borne à confirmer).

## 27/10/2026 (nuit)
- [C] Capot magnétique : capteur **codé** commandé (RS 0163138, lien donné par Julien). Remplace « non codé » de la base. Fabricant, référence et contacts à relever (page RS inaccessible depuis la session).
- [D par Claude, Julien ne sait pas] Sorties -K401 figées : 13-14 freins + 48 V, 23-24 -KM1 / -KM2, 33-34 STO. Raison : le STO a une sortie dédiée qui ne coupe que quelques mA, jamais de bobine, donc pas d'usure du contact par les charges inductives ; freins et 48 V ensemble car ils tombent sur le même événement. À revoir seulement si la notice XPSUAF13AP montre des sorties différentes.
- [?] -K511 (ordre automate -KM1 / -KM2) : Julien demande à quoi il sert. Proposition : le supprimer (option A), en attente de sa réponse.
- [C] Capteur capot magnétique : RS 016-3138 = ifm MN508S (série MN), 2 NO + 1 NF, M12, 24 V CC 50 mA, IP67/IP69K. Le symbole posé (ifm_MN508S) est donc la bonne référence ; ses broches (11-12 / 23-24) ne reflètent pas 2 NO + 1 NF.
- [D par Claude] Câblage -B412 : 1 NO (fermé capot fermé) en voie 2 du relais ; NF -> automate I0.3 (1 = capot ouvert, même sens que -B411 sur I0.2) ; 2e NO en réserve. Contacts à 50 mA max : uniquement entrées relais / automate.
- [?] À vérifier sur la fiche ifm : homologation sécurité (EN 60947-5-3 / EN ISO 14119, absente des données RS), actionneur codé à associer (commandé ?), brochage M12. Câble : M12 (et non M8 comme noté en base), nombre de broches et longueur à définir.
- [D] Option A : pas d'ordre automate sur -KM1 / -KM2 (-K511 supprimé, Q0.7 en réserve). -KM1 / -KM2 fermés dès que -K401 est armé en Auto ; arrêt de service par rampe + STO.

## 28/10/2026 : retours de Julien sur la v3
- [D] Nouveau repérage (table : `docs/NOMMAGE_2026-10-28.md`) : lettres de fonction + n° d'ordre dans la fonction, sens de l'énergie ; -KM1 / -KM2 moteurs, -KF1 / -KF2 freins ; disjoncteurs QS1, QF1 à QF10, QM1 / QM2 ; borniers X1x / X3x / X70 / X71. Remplace la règle R6 (folio maître). Folio 03 refait.
- [D] Parafoudre supprimé du schéma (f10).
- [D] 48 V : contacteur -KM3 (LC1D09BD) juste après l'alimentation, puis borniers de distribution -X34 (+48 V) / -X35 (0 V 48) avant les drivers ; bobine alimentée par le 24 V qui traverse le sélecteur (Manu-D), **ce 24 V venant de la sortie 13-14 de -KA1** (condition pour que l'AU coupe le 48 V).
- [D] X5 des variateurs sur le +24 V SECU (-X31). Conséquence : -T1 (+24 V AUTRE) n'a plus aucun départ, affectation à décider.
- [D] 0 V commun aux 2 alimentations : conservé (explication sur f30). Liaison PELV dessinée : -X36.1 (borne sectionnable) entre 0 V et PE.
- [D] Voyant 230 V présence tension -H2 (f13), alimenté par les départs libres 35 (L3) et N4 du répartiteur -X12 (f11), protégé par -QF1 : câblage 2,5 mm².
- [D] f54 : renvois PROFINET (type provisoire « Autre tension DC » en vert) vers -K1 X1 P1 (f50), -U1 / -U2 X40 (f20 / f21), -P1 X1 (f60). Relais d'alarme du switch non câblé.
- [D] f60 : IHM sur +24 V SECU, câble -W711 retiré, mise en page aérée.
- [D] f70 en construction : groupes de bornes (19G1, 27G1, TF 4, moteurs 2x4, freins 2x2, M12 8 broches, thermocouple 2), non attribués. Moteurs, freins et TF via bornier : remplace le raccordement direct du 27/10.
- [D] f01 : encadrés logos TTK, BEBL, LEVERT INDUSTRIE ; tableau des indices supprimé. f02 : tableau pleine page, police 2,6 mm, colonne indice retirée.
- [?] Affichage « câble blindé » (W2, W5) et masquage des numéros de broches des drivers (U3, U4) : champs du format .xrs inconnus. Julien fait la modification sur un symbole / câble dans WinRelais et renvoie le .xrs pour repérer le champ.

## 28/10/2026 (suite) : réponses de Julien, en attente de sa relecture de la v4 (pas de nouvelle version)
- [D] +24 V AUTRE (-T1) : affecté aux charges « puissance de commande » (bobines via les contacts de -KA1, colonne, voyants, sorties automate 3L+ des voyants). Rappel : aucune des deux alimentations n'est coupée par l'AU ; l'AU agit par les contacts de -KA1.
- [D] Câble 27G1 : machine <-> armoire ; répartition machine / pupitre non attribuée.
- [D] Thermocouple : câble de compensation en direct jusqu'au module -K3, sans borne. Groupe « thermocouple » à retirer du folio 70.
- [D] Moteurs, freins et sondes TF via bornier -X70 : validé, à câbler aux folios 20 / 21 dans la prochaine version.
- [?] Renommer les potentiels « +24 V SECU » / « +24 V AUTRE » pour éviter de croire qu'ils sont coupés par l'AU (proposition : « +24 V ELECTRONIQUE » / « +24 V COMMANDE »).

## 28/10/2026 (soir) : retours v4 -> v5
- [D] Potentiels renommés : +24 V ELEC (-T2 : automate, IHM, switch, A1 du relais de sécurité, X5 variateurs) et +24 V COMMANDE (-T1 : contacts 13 / 23 / 33 de -KA1 -> bobines, sorties 3L+ de -K2 -> colonne et voyants). Aucun n'est coupé par l'AU.
- [D] Câble client -W1 : 5G4 mm².
- [D] f11 / f12 : étiquettes des départs centrées sur les renvois, police 2,6 / 3 mm.
- [D] f70 : groupe « arrivée réseau » (5 bornes) ajouté en bas, groupe thermocouple retiré.
- [D] Règle de Julien : pastille d'état en haut à droite de chaque folio (vert = validé par Julien, tous éléments compris ; orange = presque fini ; rouge = moins de 50 %). États initiaux proposés par Claude (aucun vert), dans `STATUT` de `ttk_schema.py`.
- [?] f32 « bornier pour le 0 V » : -X35 existe déjà ; demande à préciser.
- [?] Numérotation des fils : méthode à tester sur f12 (L1, L2, L3).

## 28/10/2026 (nuit) : v6
- [D] -KM3 coupe le +48 V seul, avec 1 pôle (pas de pôles en série) ; 0 V 48 non coupé, direct de -T3 à -X35.
- [D] f32 : un fil par driver depuis -X34 / -X35, sans dérivation (croisements sans jonction acceptés).
- [D] Numérotation des fils, convention A : les fils de puissance portent le nom de leur phase (L1, L2, L3, N), sans différenciation. Les autres fils ne sont pas numérotés tant que le schéma n'est pas fini. Format relevé sur le fichier numéroté par Julien (`schema/recus/2026-10-28_v5_numerotation_f12.xrs`) : `x·y·texte·folio·0·Arial·300·angle·8388608·0·0·0·`, un numéro par tronçon, au milieu du segment, angle 90 en vertical. Généré par `nommer_phases()` (phase connue aux départs de -X12, propagée à travers les pôles).
- [D] f70 : rectangles 6 x 12 mm repérés (1..n, PE, U V W, 1b 2b, 2 3, L1 L2 L3 N). f71 : tableau agrandi (ligne 6 mm, police 2,5 mm).

## 29/10/2026 : reprise en local, retours sur la v6
- [D] Travail uniquement dans le clone local du dépôt (`Repo_git/TTK-SCHEMA-ELEC`) ; commits, push et versions confiés à l'assistant.
- [D] QF7 / QF8 = Hager NFT702 (2 A, 1P+N, courbe C, 6-10 kA, 1 module).
- [D] **Plus aucune note encadrée** sur les folios. Points à vérifier : `memoire/05_POINTS_OUVERTS.md`.
- [D] Répartition 24 V ELEC / COMMANDE : tableau actuel conservé, pas de contacteur en plus. Les deux 24 V restent distribués après un AU (l'AU agit par les contacts de -KA1).
- [D] L'un des deux 24 V s'appelle **24VSEC**. [?] Lequel (proposition : T1, qui passe par -KA1) et nom de l'autre.
- [D] Numéros de fil L1, L2, L3, N, **PE** sur tous les tronçons de puissance des f10, f12, f13 (y compris les tronçons courts).
- [D] f13 à séparer en 2 folios (esthétique). [?] Découpage.
- [D] f13 : supprimer le croisement des fils de EL1 / EL2.
- [?] Terre en bas des f10 / f13 « moche » : options A (PE dans le faisceau), B (symbole terre local), C (renvoi PE court) proposées.
- [?] f12 : bus tri / tétra avec piquages au lieu des renvois au-dessus des appareils (points de jonction, à concilier avec la règle du f32).
- [C] Incohérence relevée sur la v6 : au f10, les fils QF1 → renvois vers X12 sont croisés (L3 réseau sur la barre L1 et inversement). À corriger en v7.
- [D] Pas de génération de la v7 avant d'avoir discuté ces points.
- Dossier `memoire/` créé : synthèse par thème (projet, matériel, architecture, règles de dessin, points ouverts, v7, méthode).

## 29/10/2026 (soir) : réponses de Julien, v7
- [D] Terre : option A au f10 (PE dans le faisceau), option C au f13 / f14 (fil PE court + renvoi vers X13).
- [D] f12 en bus L1 L2 L3 avec piquages (points de jonction acceptés sur un bus).
- [D] f13 séparé : f13 alimentations (QF4, QF5, QF6, H2), f14 services (QF7 à QF10, X14, EV1 / EV2, EL1 / EL2).
- [D] f43 supprimé (contenu repris dans `memoire/03_ARCHITECTURE.md`).
- [D par Claude, Julien « à toi de trouver »] T1 = **24VSEC**, T2 = **24VELEC**.
- [H] N° de départ du répartiteur non affiché sur le bus du f12 ; ordre L3 / L2 / L1 / N / PE de haut en bas au f10 (sans croisement).
- [D] Système de mémoire : Julien demande de signaler et faire toute amélioration. Ajout de `CLAUDE.md` à la racine (lu automatiquement par un nouveau chat Claude Code).
- v7 générée : `schema/generes/TTK_2026-10-29_v7.xrs`.

## 29/10/2026 (nuit) : retours v7 -> v8
- [D] Nouvel ordre des folios : AU / sécurité (f10-f12), alimentations 400 / 230 / 48 / 24 V (f20-f25), switch PROFINET (f30, avant les variateurs), variateurs (f31, f32), IHM (f40), automate (f50-f53), borniers (f70, f71). Table de correspondance : `memoire/04_REGLES_DESSIN.md`.
- [H] Ordre interne du bloc sécurité : entrées (AU) f10, relais KA1 f11, sorties f12.
- [D] Supprimés : ancien f11 (pas de symbole du répartiteur X12 ni de la barrette de terre X13), ancien f30 (fondu dans le 230 V alimentations, f22).
- [D] Règle C pour la terre sur tous les folios : fil PE court + renvoi vers l'arrivée (f20). Moteur : PE → X2 PE du variateur ; X1 PE en renvoi court.
- [D] Barres 24VELEC et 0 V en haut de tous les folios de commande.
- [D] Marque et référence masquées sur tous les composants sauf les borniers.
- [D] KM3 renommé : contacteur auxiliaire de coupure du +48 V → **KA2** (nom choisi par Claude, convention KA). Il coupe le 48 V, pas le 24 V.
- [D] f01 : lignes « Commande » et « Puissance installée » supprimées. f03 : seul le tableau des conducteurs reste. f20 : texte d'arrivée réseau dans un cadre.
- [D] f22 / f23 : éléments centrés, fils allongés après les disjoncteurs, prise de service dans l'axe. f24 : architecture descendante.
- [D] Numéros de fil centrés et alignés.
- [C] Julien a déplacé la variante USA (TR1) à gauche au f10 dans WinRelais : reprise dans le script.
- [D] X12 et X13 (non dessinés) : Julien les ajoute lui-même à la nomenclature. Rien à faire côté script.

## 30/10/2026 : retours v8 -> v9
- [D] Sécurité remise à sa place : f40 (relais KA1), f41 (entrées), f42 (sorties). La mise en tête de la v8 venait d'une mauvaise lecture de « AU ».
- [H] IHM numérotée f45 (entre sécurité et automate, conforme à la liste de Julien). Alimentations gardent 20 à 25.
- [D] Carré de couleur en haut des folios supprimé.
- [D] **PUL des 2 drivers sur des sorties 100 kHz** : Q0.0 (U3), Q0.2 (U4). DIR et ENA sans contrainte. [C] Fiche Siemens 6ES7214-1AH50-0XB0 : Qa.0-Qa.3 100 kHz, Qa.4-Qb.1 20 kHz. L'ancienne affectation Q0.4 pour PUL U4 était limitée à 20 kHz.
- [H] DIR Q0.1 / Q0.3, ENA Q0.4 / Q0.5 ; Q0.6, Q0.7, Q1.0, Q1.1 en réserve. PTO à vérifier dans TIA.
- [D] f50 : alignement de Julien (bornes sur 2 lignes, contacts sur 2 niveaux en quinconce), à garder comme modèle. Règle chiffrée : `memoire/04_REGLES_DESSIN.md`.
- [D] Bus des f21, f22, f23 en haut, à la même hauteur (modèle f22). [H] Étendu aux barres 24 V / 0 V et aux variateurs.
- [D] f23 : lampes et ventilateurs écartés. f20 : numéro de fil séparé du numéro de brin du câble.
- [D] f31, f32 : variateur remonté. [H] Moteur dans l'axe de X2, 3 câbles sur une ligne (image du défaut non reçue).
- [C] Noms de broches : réglables par symbole (champ 5). U3 masqué, U4 affiché. Règle générale à donner par Julien.

## 02/11/2026 : retours v9 -> v10
- [D] f03 (légende, conventions) supprimé. Sommaire mis à jour (ordre contrôlé).
- [D] f04 : synoptique en logigramme, plus de cadres ; note du bas supprimée.
- [D] Noms de broches : jamais masqués par principe, au cas par cas sur demande. Masqués : TR1, U3, U4, M3, M4.
- [D] f21 : composants descendus. f22 : note « Présence tension » supprimée.
- [D] T3 (48 V) déplacée au f22. Borniers X34 / X35 supprimés : les 2 sorties + et les 2 sorties - de T3 vont directement aux drivers, les 2 +48 V passent par KA2.
- [H] KA2 reste au f24 ; 1 pôle par driver (1-2 U3, 3-4 U4).
- [C] Repris du fichier de Julien : texte « vers -X11 » de la variante USA retiré. [?] W1 absent de son fichier : gardé.

## 02/11/2026 (après-midi) : v11
- [D] Rien à ajouter au message coupé du f24. W1 gardé au f20.
- [D] f41 : barres 24 V / 0 V retirées (pas de piquage). f25 « borniers sur la page alims » : en pause.
- [D] f53 : bornes pour thermocouple, référence à définir (pas encore achetées).
- [D] f20 : renvois de terre à droite, fils de la chaîne arrivée / QS1 / QF1 allongés (numérotation future).
- [D] Bornier entre l'armoire et tout appareil extérieur : moteurs M1 / M2 (moteur, TF, frein) et M3 / M4.
- [C] Nouveau symbole moteur SEW (Julien) repris : CUSTOM/SEW_K39-DRN100LS4-BE5-TF_motoreducteur_frein.xsy, copié dans outils/librairie.
- [?] Plan de folios et repérage X<folio>.<groupe>.<borne> : proposition dans docs/PROPOSITION_FOLIOS_BORNIERS_2026-11-02.md (Q17).

## 02/11/2026 (soir) : v12
- [D] Plan de folios par dizaines appliqué (table dans memoire/04_REGLES_DESSIN.md).
- [D] Repère des bornes : X + n° de folio + « . » + n° de borne, une dizaine par fonction (X31.11...). Un seul point : WinRelais refuse X.x.x (test de Julien).
- [D] Prise de service : XD1.
- [D] Câbles des moteurs présentés comme Julien les a placés au f32 (ovale à gauche, composition dessous).
- [D] f70 : groupes de bornes avec leur repère ; f71 : à jour.
- [D] Rangement : schema/generes/release (dernière version) et schema/generes/old (précédentes).
- [H] Câbles numérotés de gauche à droite (moteur, TF, frein) comme dans le fichier de Julien. [?] Composition du frein : 2G1,5 gardé (Julien a écrit 2G1 blindé).

## 02/11/2026 (nuit) : v13
- [D] f11 : neutre retiré du bus (rien ne s'y pique).
- [D] Couleurs des fils vérifiées par l'assistant à la demande de Julien. [C] IEC 60204-1 13.2.4 : noir puissance CA et CC, rouge commande CA, bleu commande CC, orange circuits exceptés, bleu clair neutre. Appliqué : plus d'orange (aucun circuit excepté) ; 48 V, pas-à-pas, résistance de freinage en noir ; thermocouple vert (IEC 60584-3).
- [D] f20 : drivers remontés ; un câble blindé (au minimum) du bornier à chaque moteur pas-à-pas.
- [D] f31 / f32 : noms de broches du bloc moteur masqués ; câble sonde TF 2x0,75 blindé ; superposition des fils du frein corrigée. Frein : 2G1,5 confirmé (Q20 réglé).
- [D] f40 : B2 du relais au 0 V (R-02). [C] Réglage FUNCTION 1, START 3 validé au banc par Julien.
- [?] Propositions f40 : fusible gG ≤ 10 A en amont des contacts (R-33), Z1 → I1.5, capteur magnétique codé ou non (Q22 à Q24).

## 02/11/2026 (nuit, suite)
- [D] Retouches de Julien dans la v12 à reprendre dans le script, R1 décalé aussi au f32 (Q21).
- [D] Z1 du KA1 → I1.5 (Q23).
- [D] Capteur de capot B2 : codé (ifm MN508S) (Q24).
- [D] Dossier `folios/` (vide depuis le 29/10) supprimé.
- [?] R-33 : fusible gG ≤ 10 A en amont des contacts du KA1, décision de Julien attendue (Q22).
- Modifications du schéma en attente : Julien relit d'abord la v13.

## 02/11/2026 (nuit) : v15
- [D] f10 : cadre de l'arrivée réseau en pointillé.
- [D] Pour chaque modification : regarder le .xrs actuel de Julien pour vérifier ou comparer ; ses retouches à la main sont reprises dans le script.
- [D] But : schéma propre (borniers, sécurité, automate) avant la numérotation des fils.
- [D] f20 : bornes et câble répartis sur la longueur driver-moteur. f31 / f32 : compositions des câbles placées comme Julien.
- [D] Bouton de réarmement S4 au f40.
- [D] AU armoire S1 (porte) raccordé par des bornes en bas de l'armoire, jamais en direct (f41, f60).
- [D] f61 / f62 : nom du module tout près, détails empilés proprement.
- [D] Q21 et Q23 appliqués : R1 / R2 décalées, textes f10 / f63, Z1 → I1.5.
- [?] Contacts des AU : Julien pense 3 NF ; schéma et base XPSUAF : 2 NF + 1 NO (Q25).

## 03/11/2026 : clôture des achats (revue `docs/REVUE_ACHATS_2026-11-03.md`)
- [D] Thermocouple K, câble de compensation K, embouts 4 mm², repères 4-6 mm² : déjà au tableau (lot N, à passer à Hugo).
- [D] Bornes de terre vert/jaune ajoutées au tableau.
- [D] 2e lampe d'armoire : déjà commandée.
- [D] S4 sans voyant : XB4BA21 non lumineux conservé. Voyant Q8.3 (f61) à retirer, Q8.3 en réserve.
- [D] Voyant H2 230 V ajouté au tableau.
- [D] Pas de connecteur type K : thermocouple « en direct depuis la sonde ». [?] Jonction câble sonde 2 m / compensation 25 m (Q28).
- [D] R-33 (Q22) : fusible gG en amont des contacts 13 / 23 / 33. Proposé : Mersen CMC101 (RS 189-5333, 1P 10x38, 32 A, 690 V CA/CC, sans voyant) + Mersen FR10GG50V4 gG 4 A, 500 V CA / 250 V CC (RS 188-6962, paquet de 10). Calibre : charge max 0,9 A (KM1, KM2, KF1, KF2 à 5,4 W), ≤ 10 A gG (notice). À dessiner.
- [C] LC1D09BD : bobine 5,4 W (appel et maintien), antiparasite bidirectionnel intégré, NF miroir IEC 60947-4-1 (fiche Schneider). Point antiparasites clos.

## 03/11/2026 (soir)
- [D] Câble frein W3 / W6 : LIYCY-JZ 5G1,5 de réserve (AEE261168). [C] 300/500 V CA, essai 2000 V, tresse Cu étamé ≤ 65 % (fiche Achat Electrique). Remplace le 2G1,5 ≥ 450/750 V du 26/10 : aucun achat.
- [H] Jonction sonde K / câble de compensation : paire miniature type K RS 891-9031 (fiche + prise, 220 °C, câble ≤ Ø 4 mm), hors zone > 105 °C. À valider (Q28).
- [?] Écrou 1/2 pouce de la sonde 350-398 contre « 12/Ø8 x 20 » Microdia (Q29). 50 m de 2XSLCY-K : 1 ou 2 machines (Q30).

## 03/11/2026 (suite)
- [D] AU S1 / S2 : 2 NF + 1 NO chacun ; Julien corrige la commande (Q25 réglé). Schéma inchangé.
- [H] Repère du fusible R-33 : FA1 (IEC 81346-2:2019, FA = protection contre les surintensités), à valider ; autre choix FU1.
- Décisions du 03/11 à dessiner en v16 : fusible R-33, S4 sans voyant (Q8.3 en réserve), frein 5G1,5, bornes de terre vert/jaune (X10.15, X31.11, X32.11, X50.13).

## 04/11/2026 : v16
- [D] Repère du fusible R-33 : FA1 (IEC 81346-2). Dessiné au f40 entre 24VSEC et le départ commun 13 / 23 / 33.
- [D] Appliqué : S4 XB4BA21 non lumineux (voyant retiré au f61, Q8.3 en réserve), frein W3 / W6 en 5G1,5 blindé, bornes de terre vert/jaune.
- [C] La borne PE de l'arrivée est X10.11 (X10.15 = L3) : la revue des achats est corrigée.

## 04/11/2026 : agent d'implantation
- [D] L'agent qui dessine l'implantation (draw.io) refait l'implantation selon la v16, pose ses questions à Julien et versionne son travail dans `implantation/` du dépôt (release / old / JOURNAL). Prompt : `docs/PROMPT_AGENT_IMPLANTATION_2026-11-04.md`.
- [?] Repères du répartiteur 4P et du bornier de terre (anciens X12 / X13) : en conflit avec les bornes X12.11, à fixer.


## 05/11/2026 : retours de Julien
- [D] Fins de course B3 à B6 : on garde le contact NO (choix de Julien).
- [D] Repères : répartiteur 4P AEE300427 = -XR1, bornier de terre Legrand 404839 = -XPE1 (Q31).
- [C] STO du MCX91A (Julien, notice SEW) : X6.1 / X6.3 = +24 V, X6.2 / X6.4 = 0 V ; X6.5 / X6.6 non utilisés. Câblage conforme ; texte rouge du f31 / f32 réduit à « TF X10 : bornes à confirmer » (script, prochaine version).
- [C] Sélecteur Eaton T0-4-8223/E : 24 V CC / 10 mA fiable, DC-13 10 A. Numérotation des contacts absente de la fiche convertie.
- [H] Proposition 27G1 (-W11) → pupitre, 19G1 (-W12) → boîte de jonction machine, B2 par son câble M12 ; détail dans `memoire/02_MATERIEL.md`. À valider (Q32).

## 05/11/2026 : agent d'implantation (v5, v6)
- [D] Freins M1 + M2 : un seul câble 5G1,5 (4 conducteurs + V/J), boîte de dérivation côté machine. Remplace W3 / W6. Borne PE et repère à fixer (Q33).
- [D] Boîte de dérivation dans la machine dans tous les cas ; capteurs et capots par un câble multiconducteur (cohérent avec la proposition W12, Q32).
- [D] Fins de course de translation B3 à B6 : 2 bornes par contact.
- [D] Bornier R5 groupé par câble (implantation v5 / v6). QS1 mesure environ 140 mm de large (Julien).
- [D] Distribution 400 V : 2 AEE300427, fil 4 mm², QF1 → XR1, ponts XR1 → XR2 (04/11). [H] Repère XR2 (Q34).
- [D] Drivers U3 / U4 vissés sur la plaque. Cotes réelles des rails : Julien ajuste au montage.

## 05/11/2026 : retours de Julien (suite)
- [D] Répartiteurs 4P = -XR1 / -XR2 (Julien, Q34 réglé) ; bornier de terre = -XPE1.
- [C] ENA du DM860H : alimenté = moteur libre, non alimenté = driver actif (Julien).
- [C] Sélecteur Eaton T0-4-8223/E : 4 inverseurs à commun ponté (2-4, 6-8, 10-12, 14-16), pas 8 NO indépendants. Proposition « option D » dans `memoire/02_MATERIEL.md` (Q35).
- [D] B2 par son propre câble M12 jusqu'à X41.41-44. Répartition 27G1 / 19G1 pas encore validée.
- Script : textes des fins de course B3 à B6 passés en NO (prochaine version).

## 05/11/2026 : suite (agent d'implantation)
- [D] Câble frein unique M1 + M2 : repère W3, W6 supprimé. Pour Julien, l'essentiel est un seul câble pour les 4 fils frein (Q33).
- [C] Sélecteur S3 : les ponts 2-4, 6-8, 10-12, 14-16 sont des fils ; Julien les a retirés (photos) → 8 NO indépendants, option D abandonnée. Vraie numérotation à poser (proposition dans `memoire/02_MATERIEL.md`).
- [D] Bornes TF X31.2x / X32.2x bien séparées des autres (Julien). Butées d'arrêt rail DIN entre les fonctions d'un même câble, ex. 27G1 entre AU (1-6) et sélecteur (7-20) (Q39).
- [D] Liaison équipotentielle armoire ↔ bâti machine : un câble de terre seul en plus des V/J et des blindages (Q38, section et repère à fixer).

## 05/11/2026 : v17
- [D] Contacts du sélecteur S3 nommés AUTO-A à AUTO-D et MANU-A à MANU-D (Julien), vrais numéros Eaton 1-2 à 15-16.
- [D] Porte : tous les appareils par des bornes, ou aucun (Julien). Dessinés : S4, H2, H3, H4 ; à retirer tous si la place manque.
- [D] Colonne H1 par des bornes (câble) : X61.11-14.

## 05/11/2026 : v18
- [D] Câble frein unique M1 + M2 = **-W4** (5G1,5 blindé), W7 supprimé. Correction : W3 / W6 sont les sondes TF dans le schéma depuis la v11 ; « W3 » noté pour le frein le 05/11 était une erreur.
- [D] Liaison équipotentielle armoire → bâti : -W13, conducteur V/J seul 4 mm² (Julien : 2,5 ou 4 ; 4 retenu, conducteur seul non protégé).
- [C] Stock de Julien : seulement du 5G1,5 (ni 5G2,5 ni 5G1).
- Répartition 27G1 / 19G1 redonnée complète avec les butées entre fonctions ; toujours à valider (Q32).

## 05/11/2026 : v19
- [D] Répartition 27G1 (-W11) / 19G1 (-W12) validée par Julien ; dessinée au f70 avec les butées entre fonctions.
- [D] Risque du 03/11 (+24 V permanent dans le 27G1 avec les fils après KA1) : pas un risque pour Julien, chaque conducteur a sa gaine ; il soigne le cheminement du câble.

## 05/11/2026 : implantation v8 (schéma v19)
- [H] Bornes de porte (S1, S4, H2, H3, H4 : 14 bornes) sur R4, à droite de XR2 : avec les butées (Q39), R5 manque de place (tronçon 1 : 286 / 320 mm sans la porte). H2 230 V séparé du TBTP par une butée. À valider par Julien.
- [H] Pas de butée entre deux câbles différents d'un même tronçon (B2 / B7, W9 / W10) : capot de fin + repère, faute de place.
- Passe-câbles : W4 freins = 1 CEM M20 (manque 1 CEM M20), W13 = 1 M16 non CEM à acheter.

## 05/11/2026 : v20
- [D] f21 : blocs de distribution Phoenix PTFIX 6/12X2,5 (3273354) à la place des 6X1,5 ; couleurs du stock : 24VELEC rouge, 0 V bleu, 24VSEC gris [H, choix de l'assistant, à valider].
- [C] Câble TF 2x0,75 blindé : conducteurs blanc et marron.
- [C] Fichier de test de Julien : champ type de câble (3 = blindé ellipse + trait) et champ « afficher les numéros » identifiés ; le type de conducteur PROFINET n'est pas dans le .xrs.
- [H] Liste d'E/S d'ensemble : `docs/LISTE_ES_AUTOMATE.md`, à valider.
- [H] Convention de numérotation des fils proposée : un numéro par potentiel, folio + n° d'ordre en chiffres seuls, potentiels fixes réservés ; à valider.

## 05/11/2026 : v21
- [D] Type de fil PROFINET : « Profinet », rose foncé RGB(199, 21, 133), épaisseur 44 (puissance + 10 %). Appliqué en v21.
- [D] Liste d'E/S CPU / SM 1223 / SM 1231 validée par Julien (et revue par l'assistant).
- [C] Drivers : PUL / DIR / ENA sur les sorties de la CPU (100 kHz sur Q0.0 et Q0.2) ; la SM 1223 ne pilote aucun driver.
- [H] Numérotation des fils : exemples donnés (`memoire/04_REGLES_DESSIN.md`), à valider.

## 05/11/2026 : retours sur l'implantation v8
- [D] Bornes de porte sur R4, à droite de XR2 : validé (« sépare bien visuellement »).
- [C] Butées : 10 mm chacune ; stock suffisant pour la 1re armoire (50 + 60 + 50, tous projets).

## 05/11/2026 : numérotation v2, réarmement
- [H] Numérotation des fils v2 (après l'avis des collègues de Julien) : tout numéroté, phases, N, 24 V et 0 V compris ; un numéro par potentiel ; FFNN, chiffre des unités = conducteur (1 L1, 2 L2, 3 L3, 4 N ; U V W ; + / 0 V). PE par la couleur. À valider. Remplace la convention A du 28/10.
- [C] Réarmement START 3 : le relais lit la boucle Y1-Y2 bouton enfoncé et arme au relâchement (constat de banc du 02/11) ; les NF miroirs ne s'ouvrent qu'après, quand les contacteurs collent : pas de conflit.
- [D] Numérotation des fils : convention v2 retenue par Julien. Point au milieu (10.13) envisagé, à trancher. Numérotation générée à la toute fin, après validation de la sécurité, de l'automate et des borniers.
- [D] Contacts miroirs dans la boucle Y1-Y2 : compris et validés par Julien ; essai de banc préparé (`docs/ESSAI_BANC_BOUCLE_RETOUR.md`).
- [D] Numéros de fil sans point (1013).
- [C] v21 : 89 bornes sur rail (85 bornes 4 mm + 4 de terre) pour 85 achetées : achat à compléter.

## 05/11/2026 : v22
- [D] Freins SEW libres en Manu : voulu (rotation de l'arbre à la clé pour la maintenance).
- [D] Bornes de la porte sur le rail R4 ; butée de chaque côté de chaque appareil sur tous les rails (Julien). Bloc porte ajouté au f70.
- [D] f62 : E/S validées, mention « PROPOSITION A VALIDER » retirée (Q13).
- [C] Contrôle complet des bornes : conforme ; 89 bornes pour 85 achetées.
- Questions à SEW regroupées : `docs/QUESTIONS_SEW.md`.

## 06/11/2026 : implantation v9 (schéma v22)
- [H] PTFIX 6/12X2,5 dessinés à 41 mm le long du rail (sens de pose à vérifier). X21.11 / X21.12 + X12.11 sur R3 à gauche (129 / 130 mm), X21.13 (24VSEC) devant FA1 et KA1.
- [H] Butée de chaque côté de chaque appareil appliquée partout où elle tient. Exceptions : R2 QM1-KM1-QM2-KM2 (il faudrait 230 mm pour 205), K1-K3 (modules reliés par le bus).
- [H] Porte : S1, S4, H3, H4 à droite de XR2 (111 / 113 mm), H2 230 V seul sur le tronçon suivant de R4, après la vis.

## 06/11/2026 : v23
- [D] STO en chaîne U1 → U2 par X6.3 / X6.4 de U1 (Julien, validé SEW). Dessiné en v23.
- [D] Partie sécurité validée par Julien.
- [C] SEW : frein alimenté moteur à l'arrêt = admissible ; MCX91A : « 1 » mise sous tension (unité à confirmer, par heure ?) ; sondes TF : pas d'information.
- f70 : titre élargi, câble indiqué pour chaque groupe.
- Bilan 24 V : `docs/BILAN_24V.md` (connu : 0,66 A sur T2, 0,90 A max sur T1, pour 10 A chacune).

## 06/11/2026 : implantation v10 (schéma v23)
- [D] R2 : tout est fixé par Julien, hors périmètre de l'implantation.
- [C] PTFIX 6/12X2,5 posés en long sur le rail (41 mm).
- [D] Livrable d'implantation réduit à 2 pages : plaque + détail des borniers (Julien).

## 09/11/2026 : v24
- [D] f70 rangé rail par rail comme dans l'implantation (Julien) ; rail indiqué ; textes et cases réduits.
- [?] SEW : « 1 » mise sous tension du MCX91A : par heure ou par minute ? Question reposée à Julien.

## 09/11/2026 : retouches v24 et mises sous tension
- [D] Mises sous tension des MCX91A : ≈ 1 toutes les 8 h (Manu pour maintenance), AU = urgences seulement. Compatible avec « 1 » de SEW : KM1 / KM2 gardés.
- [D] Logos au f01 (Julien) ; f10 / f40 textes déplacés, texte boucle Y1-Y2 du f40 supprimé (Julien). Repris dans le script, pas encore générés.

## 13/11/2026 : v25
- [D] Numérotation des fils commencée (Julien, repères 4 mm² reçus), folio par folio : f10 fait (1001-1004, 1011-1014, 1021-1024, USA 1031-1033 / 1041-1044).
- [D] XR1 et XR2 collés sur le même rail que QS1 (R2), rail plein (Julien). Électrique inchangé ; f70 : titre R4 corrigé.
- v25 : retouches v24 de Julien incluses (logos f01, textes f10 / f40).

## 13/11/2026 : v26
- [D] Numérotation f11 à f13 (même convention, dizaines dans l'ordre de lecture).
- [D] f10 aéré ; W13 en câble simple (le câble de longueur nulle faisait déborder l'export PDF) ; f21 image du bornier (Julien).
- [C] Contrôle complet des fils hors E/S automate : conforme ; fils TF passés en « Autre tension DC ».
- [?] Protection du voyant H2 230 V (sur le bus, QF1 20 A seulement) : à décider par Julien.
- [D] 13/11 : Julien garde H2 sur le bus (sans disjoncteur propre) ; condition rappelée : fils de H2 protégés par QF1 20 A (section adaptée), sinon fusible.
- [D] 13/11 : pas de v27 avant les retours de Julien ; il câble avec la numérotation v26.

## 13/11/2026 : v27
- [D] Câbles PROFINET repérés PN1 à PN4 (Julien : repère simple, distinct des fils).
- [D] Bornes éclairage X13.11-12 et ventilation X13.21-22, sur R4 à la place de XR2 (Julien : bornes à ajouter, implantation peu modifiée).
- [D] Numérotation f20, f21, f30 ; sorties CPU vers les drivers 6101-6106 ; contrôle global par `outils/xrs_numeros.py`.
- [D] f21 : images des blocs aux bonnes couleurs (Julien), centrées ; f12 : H2 / X12.22 déplacés (Julien).

## 16/11/2026 : v28
- [D] 24 V capteurs : bloc PTFIX 6/12 noir -X21.14 alimenté par L+ capt de la CPU (Julien).
- [D] H1 / H4 au f62, bornes X62.11-14 / X62.21-22 (Julien).
- [D] f80 / f85 / f90 gardés (Julien).
- [C] Tableaux f60-f62 vérifiés ; réserves en accolade ; titres et descriptions revus ; f63 remis en forme.

## 16/11/2026 : v29
- [C] L+ / M capt de la CPU : sortie capteurs 400 mA (manuel Siemens G2) ; M capt libre (contacts secs) ; 1M au 0 V ; pas de pont M - châssis (PELV unique X12.11).
- [D] PTFIX noir : en stock, place sur R3 OK (Julien).
- [D] f70 agrandi (Julien).
- [C] Revue complète : cohérent ; pas encore prêt pour le stagiaire (`docs/REVUE_COMPLETE_v29.md`).

## 16/11/2026 : v30
- [D] Numéroter les folios restants (Julien : OUI).
- [C] Fils d'entrée de la CPU numérotés par l'entrée (I0.n -> 601(n+1), I1.n -> 602(n+1)) : 11 appareils sources au f60, trop pour une dizaine chacun.
- [D] Julien valide : fils d'entrée CPU = n° de l'entrée (16/11).
- [C] f31 / f32 : U V W 3101-3103 / 3201-3203 ; f40 KA1 40xx ; f41 41xx ; f42 42xx ; f62 Q8.n 620(n+1) ; f63 6301 / 6302.

## 16/11/2026 : v31
- [D] Renommer les broches de la CPU 3L+ / 3M en 2L+ / 2M dans le symbole CUSTOM (Julien : OK).
- [D] f80 : liste des câbles = tableau WinRelais fait par Julien, recopié tel quel par le script.
- [D] f85 : textes remontés (Julien).

## 17/11/2026
- [D] Symboles CUSTOM de Julien versionnés dans `librairie_winrelais/` (nouveau PC).

## 17/11/2026 : dossier d'implantation unique (v11, indice A)
- [D] Ce PC = PRO JULIEN (hostname BEBL-15-LAFITE) ; commits préfixés [PRO JULIEN] ; pas de push sans accord de Julien.
- [D] Thermocouple : bornes X63.11 / X63.12 gardées, même si non utilisées (Julien).
- [D] W9 / W10 (pas-à-pas M3 / M4, A+ A- B+ B-) : LIYCY-JZ 5G1,5 (AEE261168), 4 conducteurs + V/J. Tableau V1 = 1 armoire.
- [D] Boîte de dérivation machine : repère +M-X1 (IEC 81346-2, classe X).
- [D] Blindage des câbles machine raccordé d'un seul côté (côté armoire, presse-étoupe CEM).
- [D] Bornes de terre RS 708-1687 : en cours de livraison.
- [D] Méthode A : un fichier de données (donnees.json, extrait du .xrs + saisie.json) → SVG → PDF A3 (Edge sans fenêtre). L'assistant reprend le dossier `implantation/` (sources : `implantation/generateur/`). Rastérisation du PDF autorisée pour le contrôle.
- [H] W14 : repère proposé pour le câble M12 de B2 (RS 285-9453).
- [H] X21.14 sur R3 à droite de K4 (FA1 / KA1 restent en place).
- [H] X13.11-22 et X12.11 en PT 4 (les 5 PT 4 restants) ; il manque alors 4 PT 2,5 (74 pour 70).
- [?] Liaisons boîte +M-X1 → freins BE5, B1, B3-B6, H1 : non définies au schéma.
- [D] Mémoire : le dossier d'implantation a son fichier `memoire/08_IMPLANTATION.md` (17/11).
- [D] 17/11 : principe de Julien : plus aucune commande sauf urgence ou problème grave ; le schéma s'adapte au stock.
- [D] Mémoire : le stock câbles / bornes a son fichier `memoire/09_STOCK.md` (17/11).
- [H] 17/11 : méthode câbles / bornes en 5 étapes, tableau des liaisons généré depuis le .xrs (en attente de l'accord de Julien).
- [D] 17/11 : vérité des câbles sortants et des bornes dans `cablage/TTK_CABLES.xlsx`, indépendante du schéma ; le schéma suit. Portée : câbles qui sortent de l'armoire. Ordre : stock câbles → liaisons par fonction → conducteurs → références des bornes (une par une).
- [D] 17/11 : câbles raisonnés en type et fonction, jamais en mètres ; s'il manque des mètres, Julien rachète. Statuts d'une liaison : en stock attribué / en stock à attribuer / pas de câble prévu.
- [C] 17/11 : stock câbles de Julien : 2 x 0,75 PPMM0180, 4G2,5 blindé AEE261757, 5G1,5 LIYCY-JZ AEE261168, 27G1 AEE261165, 19G1 AEE261164, compensation K (RS 236-3959 d'après la commande).

- [C] 17/11 : en stock : M12 SICK 285-9453, Roline 616-2586, fil V/J 811-4463 ; pas en stock : H05VV-F 2 x 1 et 2 x 0,75. 27G1 = pupitre +P1.
- [D] 17/11 : sorties de la boîte +M-X1 vers les appareils : pas de câble prévu pour l'instant.
- [?] 17/11 : colonne H1 commandée « vert/rouge » (RS 199-9760) contre 3 couleurs au schéma.

- [C] 17/11 : colonne H1 à 3 couleurs (Julien), conforme au schéma.
- [D] 17/11 : vision élec pour les tableaux de câbles (PROFINET retiré de l'aperçu et de l'onglet Conducteurs).
- [?] 17/11 : terre des pas-à-pas M3 / M4 (V/J de W9 / W10) : borne côté moteur à vérifier.

- [D] 17/11 : pas-à-pas M3 / M4 sans borne de terre : V/J de W9 / W10 à la masse du moteur. B3-B6 = RS 902-6874. B2 33-34 en réserve.
- [D] 17/11 : référentiels câble et composant gardés dans `cablage/` (HTML + onglets).
- [H] 17/11 : boîte machine +M-X1 sur un seul rail DIN : 24 bornes (base W12 + W4), 34 avec les pas-à-pas ; moteurs, TF, thermocouple, B2 et pupitre restent directs.

- [D] 17/11 : hypothèse de travail : tous les conducteurs de tous les câbles sortants passent par la boîte de jonction machine (réserves comprises). Julien rachète des PT si besoin.
- [H] 17/11 : boîte renommée **+BJM** (boîte de jonction machine), bornier +BJM-X1 (remplace +M-X1). 57 bornes sans W11, 84 avec.

## 18/11/2026 : reprise sur le PC PRO RIMANE
- [D] Ce PC = PRO RIMANE (DESKTOP-G68K9P5) ; clone `C:\Users\Rimane\Documents\10. TTK\TTK-SCHEMA-ELEC` ; commits préfixés [PRO RIMANE] ; aucun commit avant l'identité git ; pas de push sans accord de Julien.
- [C] v31 ouverte dans WinRelais sur ce PC : seuls changements de contenu, f90 → f91 + f92 « Nomenclature » (tableaux WinRelais 8 colonnes). Copie `schema/recus/2026-11-18_v31_ouverte_WinRelais.xrs`.
- [C] Nomenclature WinRelais : colonne Réf. = 2e champ de `RefConstructeur` ; le script écrit la référence dans le 3e. Qte = nombre de symboles du repère ; ligne = 1er symbole du fichier.
- [C] Images : chemin absolu dans `¤#Logo¤` (pas `¤#ImageAP¤`), recalculé depuis le dossier du script.
- [?] Identité git, Python, options nomenclature (A / B) et images : en attente de Julien.
- [D] 18/11 : identité git du PC Rimane `--local` : JulienBEBL / julien@bebl.fr (Julien).
- [C] 18/11 : Python 3.15.2 installé sur le PC Rimane ; contrôles de la v31 identiques au PC de Julien (0 erreur, 28 attentions, 0 chevauchement, numéros 0 problème).
- [D] 18/11 : `CLAUDE.md` § 7 cite les 2 clones (Julien).
- [D] 18/11 : release v31 restaurée, symboles CUSTOM installés sur le PC Rimane, push du commit c542fcc (Julien).
- [D] 18/11 : nomenclature option B : générée par le script, avec une étape de contrôle qui vérifie qu'elle n'a rien oublié (Julien).
- [H] 18/11 : S1 / S2 sur une ligne ; TR1 gardé en localisation EXT (Julien : « à toi de choisir »).
- [C] 18/11 : références B1, B3-B6, H1, S1, S2 reportées au champ 3 (02_MATERIEL, Julien 17/11) ; S2 « 2 NF + 1 NO » ; H1 et B7 localisés M.
- [D] 18/11 : essai du chemin d'image relatif sur une copie de test (Julien OK) ; variable TTK_IMAGES.

## 18/11/2026 : v32
- [D] Fins de course B3-B6 en NF (mieux pour le programme). Contact NF 11-12 du RS 902-6874 (mêmes bornes que B1).
- [D] Bornes : arrivée réseau, moteurs 1 / 2, freins 1 / 2 = PT 4 Phoenix 3211757 ; appareils des câbles 27G1 / 19G1 = PTFIX 2X4 Phoenix 1028361 ; rail R4 = PT 2,5 Phoenix 3209510.
- [H] Bornes PE (X10.11, X31.11, X32.11, X50.13) gardées en terre ; X12.11 gardé en PT 4.
- [C] Chemin d'image relatif : images affichées dans WinRelais (Julien). Défaut du script : ..\..\images.
- [D] v32 générée, commit et push (Julien).

## 18/11/2026 : retours sur la v32
- [C] PTFIX 2X4 1028361 : bloc de passage classique, 2 trous, 6 mm ; 19 + 27 blocs (Julien).
- [D] Bornes PE en terre et X12.11 en PT 4 : confirmé (Julien).
- [D] À faire en v33 après le go : f30 textes PROFINET décalés ; f31 / f32 bloc de droite épuré ; f71 texte du bas épuré ; f80 liste des câbles revue et recadrée, sans texte ; f90 / f91 police plus grande, tableau centré sur toute la page.

## 18/11/2026 : v33
- [D] PTFIX 2X4 : réserves non bornées, X50.13 reste une borne de terre vert/jaune (Julien).
- [D] f31 / f32 : 2 lignes (X40, X5 / X6) ; TF X10, blindage et W4 retirés du folio (Julien OK).
- [D] f71 : une ligne « Côté armoire en haut de la borne, côté terrain en bas. » (Julien OK).
- [D] f80 généré depuis saisie.json ; nomenclature sur 3 folios (f92) avec une police plus grande (Julien OK).
- [C] v33 : 0 problème, 0 erreur, 0 chevauchement, numéros 0 problème.

## 18/11/2026 : revue de la v33
- [C] Liste des câbles f80 : OK (Julien). Nomenclature : OK, à repasser dans quelques jours (Julien).
- [C] Chemin d'image relatif gardé par WinRelais à l'enregistrement (v33 réenregistrée sur le PC Rimane).
- [D] Revue limitée au schéma (pas l'implantation, pas TIA) ; rapport seul, aucune correction avant le go (Julien).

## 18/11/2026 : v34
- [D] Boîte +BJM : pas dessinée (Julien).
- [D] V/J de W9 / W10 : borne de terre côté armoire, pas de raccordement au moteur pas-à-pas (Julien).
- [D] Bornes du thermocouple X63 : PT 2,5 (Julien).
- [D] Fils de H2 : 2,5 mm² « normalement » (Julien) ; tenue sous 20 A à vérifier selon la pose (rappel fait une fois).
- [D] f85 : image du plan d'implantation quand il sera validé (Julien).
- [C] Courant du frein BE5 : inconnu (Julien).
- [D] Go v34 (Julien) ; v34 : 0 problème, 0 erreur, 0 chevauchement.

## 18/11/2026 : implantation v12
- [D] Implantation : générateur gardé, draw.io abandonné (Julien).
- [D] 2 pages seulement : plan de la plaque, détail des borniers (Julien). Travail limité à R3, R4, R5.
- [D] Ordre de R4 : QF4 … QF10, XD1 | X13 | S1, S4, H3, H4 | vis | H2 (Julien : oui).
- [D] Freins M1 + M2 : un seul 5G1,5 (repère W4 inchangé).
- [?] Répartition W11 / W12 (Q32) : demande du 18/11 « non validée, à marquer à valider », contre « validée le 05/11 » en mémoire. Marquée à valider en v12, question reposée.
- [C] v12 : 0 texte trop large, 0 chevauchement, 0 écart avec le .xrs v34. Bornes de terre : 6 pour 4.
- [D] Q32 : répartition W11 / W12 validée (Julien 18/11, confirme le 05/11) ; marque retirée de la v12.
- [D] Frein : repère W4 ok (Julien 18/11).

## 18/11/2026 : incohérences relevées par le chat automate
- [?] SEW « 1 » mise sous tension : unité à demander (AL04 / `T_SEW_ON` du programme). Schéma inchangé.
- [C] Polarité ENA : réglée le 05/11 ; `02_MATERIEL.md` corrigé (contradiction avec 05).
- [C] Liste d'E/S : titre passé en v34.
- [C] `03_ARCHITECTURE.md` : Q8.3 en réserve (plus de voyant S4).
- [D] Stock (bornes, câbles) : plus suivi, ne plus signaler de manque (Julien 18/11).
- [D] W14 = câble M12 de B2 (RS 285-9453) : validé (Julien 18/11).
- [D] Câbles +BJM → appareils : Julien les définira plus tard ; pas à traiter.

## 18/11/2026 : unité SEW
- [C] MCX91A : 1 mise sous tension **par heure** (Julien). Programme : `T_SEW_ON` = 3600 s. Schéma inchangé.
- [C] S13 (ENA), S14 (titre de la liste d'E/S), S3 (Q8.3 en réserve) : corrections validées (Julien).

## 20/11/2026 : prise et sections
- [D] QF10 (limitation prise) : Schneider iDT40K 1P+N **2 A** au lieu de 6 A (Julien, charge sur la phase). Référence exacte à confirmer ; à passer en v35 (attente du go).
- [H] Sections proposées (230 V entrée / sortie des alimentations, prise) : voir `memoire/05_POINTS_OUVERTS.md` ; à valider par Julien.

## 20/11/2026 : v35
- [D] QF10 : Schneider iDT40K A9P71602 (2 A C, 4,5 kA), référence vérifiée ; go v35 (Julien).
- [H] Fils de la prise : 1323 / 1324 en 2,5 mm², 1333 / 1334 en 1,5 mm² (Julien parlait de ces fils, f13).

## 20/11/2026 : stock de fil de câblage
- [C] Stock du 20/11 (Julien) : 1 mm² blanc, bleu, gris, violet, orange ; 1,5 mm² rouge, bleu ; 2,5 mm² gris, noir, bleu, V/J ; 4 mm² noir, V/J, bleu ; 2 bobines noires et 2 bleues ≈ 1 / 1,5 mm² non identifiées. Détail : `memoire/09_STOCK.md`.

## 20/11/2026 : couleurs du 24 V
- [D] 24VELEC en rouge 1,5 mm², 24VSEC en gris, 0 V en bleu (comme les blocs X21) ; orange non utilisé ; 2,5 noir à la place du 1,5 noir (Julien).
- [H] 0 V : chaque -V de T1 et T2 sur X21.12 par son propre fil (pas de T2 -V → T1 -V, sinon 20 A dans un seul fil).

## 20/11/2026 : vérifications
- [D] Bobines de fil non identifiées : oubliées (Julien).
- [C] Schéma v35 vérifié : 0 problème, 0 erreur, 30 attentions connues, 0 chevauchement, numéros 0 problème ; seule anomalie : XD1 (ligne ci-dessous). Le 0 V commun T1 / T2 reste dessiné en un point (même potentiel) ; au câblage, un fil par alimentation vers X21.12.
- [C] Mémoire : README du dépôt remis à jour (v35, implantation v12), titre v31 de 06, chemin de la v34, source de QF10 4,5 kA ; XD1 1,5 kW à revoir (prise limitée à 2 A).
- [C] Anomalie trouvée au schéma : XD1 « limitée 1,5 kW » alors que QF10 est en 2 A ; corrigé en v36 (« limitée à 2 A par -QF10 »).

## 20/11/2026 : implantation v13
- [C] Implantation v13 sur le schéma v36 : QF10 2 A, XD1 limitée à 2 A ; borniers inchangés ; 0 / 0 / 0.

## 20/11/2026 : 0 V commun
- [C] Julien demande s'il vaut mieux deux 0 V séparés : non, le 0 V commun (décision du 28/10) est nécessaire (STO, SM 1223, bobines via KA1) ; explication dans `memoire/03_ARCHITECTURE.md`. Anciens noms de borniers corrigés dans 03.
- [D] 0 V commun T1 / T2 gardé (Julien 20/11, après explication).


## 23/11/2026 : PC PERSO JULIEN
- [D] Julien travaille depuis son PC perso pendant environ 3 mois (programme automate), puis reprend son PC pro. Préfixe de commit [PERSO JULIEN].
- [C] Sur ce PC, le script régénère la v36 à l'identique (copie de la librairie + CUSTOM du dépôt). Symboles CUSTOM pas encore installés dans WinRelais.
- [C] 23/11 : symboles CUSTOM installés sur le PC PERSO JULIEN (accord de Julien) ; v36 régénérée à l'identique avec la vraie librairie. WinRelais et TIA Portal installés, Documents et Téléchargements recopiés du PC Rimane.

## 23/11/2026 : revue Krizox de la v36
- [C] Julien : la v36 a l'air bien dans WinRelais (PC perso).
- [H] 25 demandes rédigées depuis les notes de visio de Krizox (20/11) : `memoire/revues/2026-11-20_krizox_v36_demandes.md`. À valider par Julien ; rien modifié.
- [D] Rangement : revues extérieures dans `memoire/revues/` (brut + demandes).

## 23/11/2026 : revue Krizox, décisions point par point
- [D] Brins des câbles en « G » sans le V/J ; pas de numéro sur le câble client W1 ; pôle 5-6 de KA2 plus dessiné.
- [D] Bornes gardées : porte (S1, S4, H2, H3, H4), éclairage, ventilateurs (règle du 05/11 maintenue).
- [D] Boîte +BJM dessinée (revient sur le 18/11) : tous les câbles, W11 compris ; fils boîte → appareils ; boîte fabriquée par BEBL.
- [D] Cadres pointillés hors armoire ; localisations +A1 / +P1 / +M / +BJM gardées et affichées ; synoptique par lieu.
- [D] W11 / W12 / W14 dessinés sur les folios ; vérifier les bornes manquantes.
- [D] f21 refait : sans barres du haut, 4 blocs alignés, images retirées ; f30 « IP : à définir ».
- [D] f31 / f32 STO et 24 V retracés ; f60 renvois du haut horizontaux et textes L+ capt ; réserves regroupées (f61, f62) ; H1 centrée.
- [D] f70 gardé ; f71 remplacé par des plans de bornier (format « -KA1:14 (f40) », provisoire).
- [D] Freins : action externe au schéma (câblage du frein monté, logique de pilotage). Mnémoniques : seulement dans TIA.

## 23/11/2026 : v37
- [C] v37 générée (revue Krizox) : 0 problème, 0 erreur, 0 chevauchement ; rapport `docs/RAPPORT_v37_2026-11-23.md`.
- [H] f41 coupé en deux (f43 = capots) ; bornes X41.2x-4x -> X43.1x-3x ; boîte +BJM X1.1 à X1.69 (ordre du 17/11) ; sections des fils boîte -> appareils proposées ; à valider par Julien.
- [C] Images : chemin relatif non trouvé sur le PC perso ; chemin complet par défaut.
- [C] D11 : 24 V / 0 V des drivers et des E/S automate justes (37 broches contrôlées).

## 24/11/2026 : retours v37
- [?] Retours de Julien sur la v37 notés (`memoire/revues/2026-11-23_retours_julien_v37.md`) ; 4 questions posées avant la v38.
- [D] Plans de bornier f71-f73 : forme validée ; note du haut à supprimer.

## 24/11/2026 : valeurs orales SEW (frein BE5, STO)
- [?] Source orale (technicien SEW, téléphone, 24/11), **à confirmer par écrit**, aucun document. Questions 1 et 2 de `docs/QUESTIONS_SEW.md` **restent ouvertes** (réponses partielles).
- [?] Frein BE5 avec redresseur BGE1.5 : courant de maintien 0,18 A ; courant d'appel non donné ; côté CA / CC et « par frein » non précisés.
- [?] Entrée STO du MCX91A : 150 mW (6,25 mA sous 24 V) ; non précisé si par variateur (12,5 mA pour 2) ou pour les deux (6,25 mA).
- [H] STO : cas A (12,5 mA) au-dessus du minimum de 10 mA / 15 V de KA1 33-34 (R-32), marge 2,5 mA ; cas B (6,25 mA) en dessous, il manque 3,75 mA. Options notées en 05, point 1 bis, sans décision.
- [H] Frein : 0,18 A = 9 % de 2 A ; charge de KA1 13-14 inchangée (le frein passe par KF1 / KF2). Appel manquant : déclenchement de la courbe C non jugeable.
- [?] 0,18 A cohérent avec le 0,183 A à 400 V d'un chat du 27/08 (non vérifié) ; pas un recoupement indépendant prouvé.
- [C] Aucun changement de schéma, de calibre ni de nomenclature. Corrections de texte : BILAN_24V (n° de questions 3 -> 2 et 8 -> 4), 03 et 05 (STO « en chaîne » et non « en parallèle »).

## 24/11/2026 : précisions orales et mail à Xavier (SEW)
- [?] STO : 150 mW **par variateur** (Julien, 24/11, même source orale) : 12,5 mA pour les 2 en chaîne, au-dessus du minimum de 10 mA de KA1 33-34 ; marge 2,5 mA. Cas B écarté, **à confirmer par écrit**.
- [D] Mail à Xavier (SEW) en français, ton pro et neutre, contexte technique sans nom de client : `docs/MAIL_SEW_XAVIER_2026-11-24.md` (brouillon non envoyé). Question 1 : écart consigne / vitesse réelle à vide sur 30 à 137 tr/min ; puis confirmation écrite frein et STO, courant réseau, TF X10, 24 V X5.

- [D] Rapport de réduction des K39 : **10,61** (Julien, 24/11) ; repris dans le mail à Xavier. Cohérent avec « 10 Hz ≈ 27 tr/min » (4 pôles) [H]. Mode de régulation : non choisi, demandé à SEW ; signature : celle de la messagerie.

- [C] Mail à Xavier (SEW) **envoyé par Julien le 24/11/2026** : questions 10, 1, 2, 3, 4, 5 en attente de réponse écrite. Aucune réponse reçue à ce stade.


## 24/11/2026 : v38
- [D] Julien : f60 coupé en deux, tout renommer (choix a) : f60 = alimentation + PROFINET CPU, f61 = entrées, f62-f64 = anciens f61-f63 ; bornes X60 -> X61, X62 -> X63, X63 -> X64 ; fils 60xx -> 61xx…
- [D] Julien : numéros de fil plus petits sur tout le schéma, de 30 à 40 % (fait : 300 -> 200).
- [D] Julien : V/J de W9 / W10 arrêté sous le câble ; f13 : bas des colonnes alignés.
- [C] Défaut de lisibilité de la v37 reproduit par calcul (197 chevauchements avec les ellipses, repères de câble et bords de cadres) ; v38 : 0.
- [H] Symbole CPU coupé en deux (alim_profinet / entrees, CUSTOM) ; synoptique : numéros de folio corrigés.

## 24/11/2026 : v39
- [D] Julien : un W11 et un cadre +BJM par colonne (f41, f42) ; symbole des entrées CPU plus large ; f70 supprimé, plans de bornier renumérotés ; gris clair sur les bornes et borniers de terre.
- [C] Check global des bornes : 168, 0 doublon, règle X + folio respectée, saisie.json = schéma.
- [H] Tableau des entrées au f60 (pas la place au f61) ; 4e folio de plans de bornier ; remplissage des formes : champs déduits, à confirmer.

## 25/11/2026 : reprise, corrections de la mémoire (bloc 1)
- [D] Préfixe de commit unique `[PERSO JULIEN]` pour les deux dépôts (schéma et automatisme), quel que soit le PC. Remplace [PRO JULIEN], [PRO RIMANE], [perso].
- [C] Julien câble seul l'armoire (18/11) : les 2 stagiaires ne câblent pas.
- [C] Thermocouple : bornes gardées (17/11), X64.11 / X64.12 depuis la v38 ; la mention « en direct jusqu'à K3 » (28/10) est retirée.
- [C] Polarité ENA des DM860H confirmée le 18/11 (dépôt automatisme) : ENA alimenté = moteur libre.
- [C] Passage en Manu : arrêt depuis l'IHM, puis sélecteur ; pas de demande Manu sur l'IHM (bloc 3 du 18/11, dépôt automatisme). Remplace la procédure du 27/10.
- [C] Q8.3 : en réserve partout dans `03_ARCHITECTURE.md` (plus de « voyant S4 », déjà corrigé avant le 25/11).
- [C] `docs/LISTE_ES_AUTOMATE.md` : repères et folios passés en v39 (X61, X43, X63, X64 ; f60-f64). Affectation des E/S inchangée.
- [C] SEW : Xavier et Franck Strugareck sont deux personnes différentes (Julien, 25/11).
- [?] STO 150 mW : retenu « par variateur » (05, 06 alignés) ; réponse écrite de SEW reçue d'après le dépôt automatisme (25/11), document pas encore dans les dépôts.

## 25/11/2026 : fils 48 V
- [D] Fils +48 V (1251, 2001, 2011) et 0 V 48 (1250) entre T3, KA2 et U3 / U4 : **noir 2,5 mm²** du stock, + et - de même couleur, repérés par leur numéro. Rouge / bleu écartés (codes du 24VELEC et du 0 V 24).
- [?] Section maxi acceptée par les bornes d'alimentation du DM860H : à vérifier.

## 25/11/2026 : retours v39 et v40
- [D] Julien : retours sur la v39 (f03, f10, f20, f21, f30, f31/f32, f40, f42, f43, f61, f63, f64, f70-f73, f80) ; travail en autonomie, livrer une v40.
- [D] Règle de mémoire : toujours consigner les discussions (journal, décisions, fichier du thème), à chaque échange.
- [D] Symbole moteur SEW (CUSTOM, 3 copies) : contour extérieur plein.
- [D] Plans de bornier : utiliser les 4 folios ; bornes et bornier de terre en vert / jaune (plus de gris).
- [C] v40 générée : 0 problème, 0 erreur (28 attentions), 0 chevauchement ; numéros, cadres, textes, 24 V / 0 V, bornes à 0 ; rapport `docs/RAPPORT_v40_2026-11-25.md`.
- [H] Résistance de freinage avec repère seul ; pas d'image du bloc noir -X21.14 ; vert RGB(0, 176, 64), jaune RGB(255, 230, 0).
- [?] f40 : accrochage du texte des contacts non modifié (code 0 déjà dans le fichier) ; question posée à Julien.

## 25/11/2026 : v41 (contour moteur)
- [C] Julien (capture f31) : contour du moteur SEW beaucoup trop épais aux f31 / f32. Cause : erreur de l'assistant en v40 (épaisseur 200 au lieu de 20, champ de style perdu, 3 copies du symbole).
- [C] v41 : contour à 20, trait plein ; diff v40 -> v41 = 8 lignes ; tous contrôles à 0.
- [D] Nouveau contrôle `outils/controles/symboles.py` dans `tout.sh` (copies CUSTOM, format des contours).

## 26/11/2026 : captures v41
- [C] f40 dans WinRelais : textes des contacts de retour accrochés à gauche (code 0). Attente de la confirmation de Julien [?].
- [C] Borne de terre des plans de bornier : rendu jaune + bandes vertes visible dans WinRelais. Avis de Julien attendu [?].

## 26/11/2026 : captures v41, retours v41 et v42
- [D] Julien : f40, textes des contacts à droite du symbole, accrochés à droite ; « contact miroir » déplacé.
- [D] Julien : rayé vert / jaune plus marqué ; nom du câble et n° de fil en gras ; résumé des fonctions sous chaque bornier.
- [D] Julien : « Affaire » retiré du f01 ; W1 / 5G4 à droite du câble (f10).
- [D] Julien : variateur plus large (plus d'espace entre bornes, sans dépasser le folio) : pas de 600 dans les groupes X5, X6, X10, X40, X20, X22, X23.
- [D] Règle générale (Julien) : numéro de fil centré sur la longueur du tronçon, sans superposition, calculé avec la taille du texte.
- [H] f64 : thermocouple retourné (nouveau symbole CUSTOM `Thermocouple_bas.xsy`), cause du numéro « dans le symbole ».
- [H] f20 : bornes +BJM sur 2 niveaux à 400 (600 avant) pour dégager les broches du moteur.
- [H] KA1 : noms de broches masqués (doublon avec les textes jaunes du symbole).
- [C] Check folios : 31 folios cohérents, 336 renvois « fNN » justes. Check nomenclature : appareils cohérents ; câbles W8, W11, W12, W14 corrigés dans le schéma (folios et origines relus sur le dessin) ; `saisie.json` inchangé (implantation).
- [C] v42 générée : tous contrôles à 0 (contrôle élargi aux symboles).

## 26/11/2026 : saisie.json (câbles)
- [D] Julien : « oui, corrige-le » : `implantation/generateur/saisie.json` corrigé pour W8 (f64), W11 (origine X41.1x, X42.1x, X43.1x, X50.1x, X61.1x, X61.2x ; f41, 42, 43, 50, 61), W12 (X43.2x, X61.3x, X63.1x ; f43, 61, 63), W14 (f43).
- [C] v42 régénérée (même nom, pas encore ouverte dans WinRelais) : seul le f80 change ; contrôles à 0.

## 26/11/2026 : retours v42 et v43
- [D] Julien (retouches WinRelais sur la v42) : W1 textes à droite sans ovale ; W9 / W10 câble 200 plus bas, composition à gauche de l'ovale, brin 4 sur le V/J. Reprises dans le script.
- [D] Julien : variateur élargi OK (f31 / f32).
- [D] Julien : f40, textes des contacts accrochés à gauche (correction de sa demande de la v42).
- [D] Julien : résumé des plans de bornier juste sous le cadre du repère du bornier.
- [D] Julien : police de la nomenclature un peu plus grande -> 300.
- [C] v43 générée et vérifiée : tous contrôles à 0 ; W1, W9, W10 identiques à la retouche.
- [?] Brin V/J n° 4 de W9 / W10 : voulu ?

## 26/11/2026 : contrôle complet, README, passation
- [D] Julien : mettre à jour la mémoire, vérifier, mettre tout le dépôt à jour (README pas à jour), puis faire un prompt de passation pour le prochain chat.
- [C] README réécrit (folios v43, arborescence, contrôles) ; mémoire 05, 07, 08, 10, README corrigés (points réglés, outils) ; outils `folio.py`, `retouche.py`, `centrage.py` et scripts de symboles rangés dans le dépôt ; contrôle complet de la v43 : tout à 0 ; passation : `docs/PASSATION_2026-11-26.md`.

## 26/11/2026 : reprise (nouveau chat)
- [C] Dépôt à jour, release v43 non réenregistrée par WinRelais (git status propre). Aucune décision nouvelle ; attente des retours de Julien sur la v43.
