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
