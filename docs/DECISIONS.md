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
