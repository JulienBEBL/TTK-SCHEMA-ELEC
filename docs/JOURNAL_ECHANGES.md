# Journal des échanges

Une entrée par échange : date, sujet, décisions [D], points ouverts [?], remises en question.

## 26/10/2026
- Démarrage : base de connaissances transmise. Priorité : sécurité (f40-42) puis automate (f50-54). J1 = 05/11.
- Dépôt GitHub créé comme référentiel (structure, outil `xrs_check.py`, `DECISIONS.md`).
- [D] Câble frein 2G1,5 + câble TF 2G1 blindé, séparés. [D] Un repère par câble (-W201/202/203 ; -W211/212/213).
- Remise en question : prévoir la commande des 2 nouveaux câbles (hors commande actuelle) ; frein 400 V CA donc isolation adaptée.
- En attente : `.xrs` récent (envoi dans le chat) ; réponses sur repères cibles (maintenant/fin) et Q12/Q13.

## 27/10/2026
- Reçus et archivés dans `docs/local/` : METHODE_BORNIERS, FORMAT_XRS, base Claude Code du 22/10, 2 rapports de vérification.
- État de `test_xrs_claude.xrs` (22-23/10) : généré par script (27 folios, 131 symboles, 597 fils, 104 renvois), 0 erreur. Folios 70/71/80/85/90 créés mais vides, sauf tableaux de contrôle f70/f71.
- Incohérences relevées entre ces fichiers et la décision du 26/10 ou la base de session :
  1. Câbles SEW : `W202/W212 = 4 x 1 mm² blindé frein + TF` et bornes X701.17-.24 groupées par câble frein+TF. Décision [D] du 26/10 : frein 2G1,5 (W202/W212) + TF 2G1 blindé (W203/W213). À refaire dans le script et le plan de bornes.
  2. AU : plan de bornes X711 = S412 info → I0.1. Liste d'E/S gelée du 06/10 = AU pupitre S412 → I0.0, AU armoire S411 → I0.1.
  3. Fins de course : plan X701 = B501…B504 → I1.0…I1.3. Liste d'E/S du 06/10 = I0.6, I0.7, I1.0, I1.1 ; I1.2/I1.3 = retours KM1/KM2. `PROPOSITION_ES_AUTOMATE.csv` non validé : conflit à trancher.
  4. Sorties du relais K401 : plan X711 fait passer 33-34 par un contact S413 vers 3L+ des sorties CPU/SM (alimentation des sorties automate coupée par la sécurité). Architecture figée du 30/09 : 33-34 → bobines Q421, Q422, Q423 ; 13-14 → STO ; 23-24 → KM1/KM2. Les f40-f42 du fichier étaient « en attente des explications de Julien » : donc provisoires.
  5. S413 : le plan utilise 5 paires de contacts (13-14 … 53-54) ; l'Eaton T0-4-8223/E a 4 pôles. Confirme le point ouvert du 26/10.
  6. Préfixe librairie de S414 = H alors que le repère est S ; LC1D09BD avec 5 préfixes (KM, Q) : voulu (exception R8), mais à ne pas laisser comme « attention » au contrôle.
  7. Source de vérité : `test_xrs_claude.xrs` est régénéré par `ttk_schema.py`. Toute modification faite à la main dans WinRelais est écrasée à la régénération. À trancher : script ou fichier WinRelais, lequel fait foi ?
- Remise en question : BASE du 22/10 décrit Julien comme « dessinateur » (faux, corrigé) et conseille de ne pas toucher au fichier de travail : cohérent avec la base de session.

## 27/10/2026 (suite) : deux .xrs reçus
- Archivés : `schema/recus/2026-10-27_SCHEMA_ELEC_TTK_main.xrs` (à la main) et `2026-10-27_test_xrs_claude_script.xrs` (généré par script).
- Fichier à la main : 22 folios, 52 symboles, compteur 18120. Quasi identique à l'état du 22/10 (anomalies inchangées sauf T7 recalé sur la grille et le fil PUL+ de T7 repris). Reste : repères anciens, F1:N, G1:L, G2:L, T5:H1-H3 à 1 mm, M3/K4/K5 hors grille, K2/K3 et K4/K5 en double, noms internes de folios en double, descriptions f31 et f40 fausses, synoptique avec image à chemin absolu.
- Fichier script : 27 folios, 131 symboles, 0 hors grille, 0 erreur ≤ 2 mm, repères cibles, f31 à f60 remplis, f70/f71 présents. Plus de logo (le synoptique f04 n'a plus d'image).
- 22 « attente? » à 4 mm (f12, f13, f41, f42) : faux positifs de l'outil (extrémité libre du même fil que la broche). À corriger dans `xrs_check.py`.
- Point ouvert : lequel fait foi ? Voir réponse de Julien.

## 27/10/2026 (suite) : outils Python reçus
- Archivés dans `outils/` : `xrs_tool.py` (lecture, `verifier`), `xrs_edit.py` (édition sûre), `xrs_gen.py` (générateur). Manque encore `ttk_schema.py` (description du schéma) et `corrections_*.py`.
- `xrs_tool.py verifier` donne : fichier à la main 8 erreurs / 62 attentions ; fichier script 0 erreur / 27 attentions (identique au rapport du 22-23/10). Il traite déjà le faux positif « extrémité libre à 4 mm de sa propre broche » : `xrs_check.py` (annexe A) est donc redondant, on utilise `xrs_tool.py`.
- Constat : références croisées toujours à -1 dans le fichier script (pas de lien bobine ↔ contacts). Dates codées en dur « 22/10/2026 » dans `xrs_gen.py` (cartouche, auteur des symboles).

## 27/10/2026 (suite 2) : outils, 2e partie
- Archivés dans `outils/` : `ttk_schema.py` (995 lignes, description complète du schéma), `lire_tableau.py`, `corrections_2026-10-22.py`, `application_plan_2026-10-22.py`.
- `ttk_schema.py` n'est pas exécutable ici : il lit `TTK_Plan_Folios_Reperes.xlsx` (chemin `C:\Users\Julien\Downloads\`), la librairie `.xsy` (`C:\Users\Public\Documents\Elec-CAO\sym_electrotech`) et le modèle `SCHEMA_ELEC_TTK.xrs`. Il faut le lancer sur le PC de Julien.
- Constat sur le code (conforme au fichier, pas de nouvelle donnée) :
  - f20/f21 : câble `W202/W212 = "4 x 1 mm² blindé" frein + TF`, bornes `X701.17..24` ; à remplacer par 3 câbles (W201 moteur, W202 frein 2G1,5, W203 TF 2G1 blindé), bornes frein et TF séparées. Décision [D] du 26/10.
  - f41 : voies 1/2 = S411 + S412 + capot (B411 / B412) en série, S413 posé comme simple « Tête 2 pos fixes NO » sans pontage Manu du capot (architecture du 30/09 : capot en parallèle d'un contact Manu de S413). Marqué « PROPOSITION A VALIDER ».
  - f42 : STO via S413 Auto (13-14, 23-24) ; 33-34 via S413 vers « +24 VS sorties » (alimentation des sorties automate) ; bobines KM1, KM2, Q421, Q422, Q423 commandées « par l'automate » ; ordre API KM1/KM2 non décidé. Pas de boucle de retour EDM sur Y1-Y2 visible.
  - `Gen` et `ttk_schema.py` écrivent « 22/10/2026 » en dur.
- Conséquence : f41 et f42 sont à refaire avec les décisions de l'architecture figée (§3.5 de la base de session) une fois les points ouverts tranchés.

## 27/10/2026 (suite 3) : point d'avancement et plan de tâches
- Demande de Julien : repartir en ingénieur, état d'avancement, tâches, questions.
- Constat : les repères cibles sont déjà appliqués dans le fichier script. La question « repères maintenant ou à la fin » est caduque si le fichier script devient la base.
- Questions bloquantes posées : (1) base de travail, (2) architecture sécurité f41/f42 et S413, (3) Q12/Q13 et 24 V commuté, (4) liste d'E/S et relais d'interface Q0.7.
- Tâches proposées : voir `docs/PLAN_TACHES.md`.

## 27/10/2026 (suite 4) : génération du .xrs en session
- Julien : « tu dois générer le .xrs, je le télécharge, je teste dans WinRelais et je te fais des retours ». Réponses : S413 = 4 NO par position (8 au total) ; voyants : 2 minimum ; parafoudre supprimé ; 5G1,5 en réserve ; XB5AD25 supprimé ; câbles moteurs : choix laissé.
- Mise en place : `schema/modele/`, `outils/librairie/` (symboles reconstruits, `reconstruire_librairie.py`), `ttk_schema.py` et `xrs_gen.py` rendus portables (chemins relatifs, `TTK_LIB`, `TTK_DATE`). Reproduction du fichier script du 27/10 : 131 symboles, 597 fils, 0 problème.
- Modifications dans `ttk_schema.py` : câbles W201/202/203 et W211/212/213 en direct ; f41 avec pontage Manu des capots ; f42 refait (STO, -K511, -KM1/-KM2, freins et 48 V) ; f50 entrées (liste du 06/10) ; f51 sorties CPU + bobine -K511 ; f52 SM 1223 (colonne, voyants, alarme switch) ; f31 voyant tension -P512 ; bornes X711 1-21.
- Résultat : `schema/generes/TTK_2026-10-27_v1.xrs` (133 symboles, 627 fils, 0 problème au contrôle interne, 0 erreur `xrs_tool verifier`).
- Non vérifié : ouverture dans WinRelais (aucun accès). À faire par Julien.

## 27/10/2026 (soir) : passage en Opus, partie sécurité
- Julien fournit la fiche « architecture de sécurité (relais + sélecteur Auto/Manu) », direction souhaitée, à critiquer.
- Appliquée : f40 (notes), f41 (shunts Manu-A / Manu-B), f42 refait (sorties 1/2/3), f43 créé. Résultat `schema/generes/TTK_2026-10-27_v2.xrs` : 28 folios, 136 symboles, 630 fils, 0 problème au contrôle interne, 0 erreur `xrs_tool verifier`.
- Écarts relevés : voir `docs/ARCHITECTURE_SECURITE_2026-10-27.md`. Revue d'ensemble faite (réponse du 27/10 soir).

## 27/10/2026 (nuit)
- Julien : capteur magnétique codé RS 0163138 ; affectation des sorties « je ne sais pas » ; -K511 « pour quelles fonctions ? ».
- Claude : affectation des sorties figée avec justification ; explication de -K511 et proposition de le supprimer ; demande de la référence fabricant du capteur codé.

## 27/10/2026 (nuit, suite)
- Julien : capteur = ifm (série MN, 2 NO + 1 NF, M12, 50 mA) ; option A retenue ; demande la v3 et une fiche récapitulative pour un autre chat (local).
- v3 générée : `schema/generes/TTK_2026-10-27_v3.xrs` (28 folios, 134 symboles, 624 fils, 0 problème, 0 erreur verifier) + vérification + nomenclature. Récap : `docs/RECAP_2026-10-27.md`.

## 28/10/2026 : retours v3 -> v4
- Retours de Julien sur f01, f02, f03, f10, f20, f21, f30, f31, f32, f54, f60, f70 + nommage + 48 V + voyant 230 V (détail : `docs/DECISIONS.md` du 28/10).
- v4 générée : `schema/generes/TTK_2026-10-28_v4.xrs` (28 folios, 137 symboles, 630 fils, 109 renvois ; 0 problème au contrôle interne ; 0 erreur `xrs_tool verifier`). Attention attendue : 0 V et PE sur le même potentiel (liaison PELV -X36.1).
- Non fait, en attente d'un .xrs modifié par Julien : affichage câble blindé, masquage des numéros de broches des drivers.

## 28/10/2026 (suite)
- Julien : T1 OK mais « est-ce un 24 V coupé par l'AU ? » ; 27G1 machine <-> armoire, non attribué ; thermocouple en direct ; moteurs / freins / TF via bornier OK ; attendre sa relecture de la v4 avant toute nouvelle version.

## 28/10/2026 (soir) : v5
- Retours de Julien sur f10, f11, f12, f32, f70, règle des pastilles, numérotation des fils, potentiels 24 V.
- v5 : `schema/generes/TTK_2026-10-28_v5.xrs` ; 0 problème au contrôle interne, 0 erreur verifier.

## 28/10/2026 (nuit) : v6
- Retours v5 : f32 (un fil par driver, KM3 1 pôle), f70 (rectangles repérés), f71 (tableau plus grand), numérotation testée par Julien sur f12.
- v6 : `schema/generes/TTK_2026-10-28_v6.xrs` ; 0 problème au contrôle interne, 0 erreur verifier ; 84 noms de phase posés sur les fils de puissance (f10 à f21).

## 29/10/2026
- Fiche de passation complète pour le chat local : `docs/PASSATION_CHAT_LOCAL_2026-10-29.md` (copie dans `livrables/`). Julien la joint avec les .xrs v5 (ouvert, numérotation test f12) et v6 (non ouvert).

## 29/10/2026 (après-midi) : assistant local
- Reprise depuis la passation. v5 jointe = fichier déjà archivé ; v6 jointe = v6 générée, réenregistrée par WinRelais sans changement de contenu (archivée : `schema/recus/2026-10-29_v6_ouverte_WinRelais.xrs`). 0 erreur au verifier sur les deux.
- Tableau 24 V ELEC / COMMANDE envoyé ; incohérence signalée (« contacteur qui coupe le 24 V ELEC » : il n'existe pas et couperait automate et relais de sécurité). Julien : ok pour le tableau actuel.
- Retours de Julien sur f10, f12, f13 (terre, numéros de fil, bus tri, découpage f13, 24VSEC, EL1 / EL2). Détail : `memoire/06_EN_COURS.md`.
- Remise en question : bus tri du f12 = points de jonction, refusés au f32. Inversion de phases trouvée au f10.
- Dossier `memoire/` créé. Pas de .xrs généré (demande de Julien).

## 29/10/2026 (soir) : v7
- Julien : OK option A (f10) et C (f13), OK bus au f12, OK découpage f13, nom de T2 laissé à l'assistant, f43 à supprimer ; améliorer la mémoire si besoin.
- v7 : `schema/generes/TTK_2026-10-29_v7.xrs` (28 folios, 137 symboles, 631 fils, 102 renvois ; 0 problème au contrôle interne, 0 erreur verifier, 26 attentions connues). Détail : `memoire/06_EN_COURS.md`.
- Contrôles par calcul : chaque tronçon de puissance des f10 à f32 porte un nom ; QS1 1/L1 = L1 ; 0 croisement au f10 ; EL1 / EL2 sans croisement ; aucune note encadrée.
- Symbole Hager NFT702 créé dans `outils/librairie/CUSTOM/` (copie du NFT706, référence et caractéristiques changées).
- Limites signalées : EV1 / EV2 gardent un croisement (bornes N et L en haut du symbole) ; phases L3 en haut au f10.

## 29/10/2026 (nuit) : v8
- Retours de Julien sur la v7 (f01, f03, f05 = page 5 = f10, f06 = page 6 = f11, f11, f13, f14, f20, f21, f32, f50-f54, f60, ordre des folios, marque / référence, KM3). 4 questions posées : f11 supprimé (oui), switch avant les variateurs (oui), « AU » = arrêt d'urgence (sécurité en tête), barres 24 V / 0 V en haut partout (oui).
- v8 : `schema/generes/TTK_2026-10-29_v8.xrs` (26 folios, 135 symboles, 614 fils, 94 renvois ; 0 problème au contrôle interne, 0 erreur verifier, 28 attentions connues). Détail : `memoire/06_EN_COURS.md`.
- Contrôles par calcul : croisements f20 = 0, f23 = 2 (piquages du bus), f24 = 2 (+ 4 déjà présents sur les entrées des drivers), f25 = 2 (piquages des barres) ; chaque tronçon de puissance nommé, noms alignés.
- v7 réenregistrée par Julien archivée dans `schema/recus/`.
- Mémoire : table de correspondance des numéros de folio (affichés / internes) ajoutée, avec le piège signalé dans `CLAUDE.md` et la structure du script dans `07_METHODE_TRAVAIL.md`.

## 30/10/2026 : v9
- Retours de Julien sur la v8 (sécurité à remettre à sa place, f20, carré de couleur, f21, f23, f24, f31, f32, f50, f51) + v8 modifiée, archivée dans `schema/recus/`. Images reçues : f20, f23, f50 ; pas celles des f24 et f31.
- Différences relevées dans son fichier : f50 (19 symboles déplacés), U3 (noms de broches), f50 / f51 (PROPOSITION retirée, réserve déplacée), câbles W2 / W4 du f31 retouchés.
- v9 : `schema/generes/TTK_2026-10-30_v9.xrs` (26 folios, 135 symboles, 600 fils, 94 renvois ; 0 problème, 0 erreur verifier, 28 attentions connues, 0 chevauchement). Détail : `memoire/06_EN_COURS.md`.
- Fiche Siemens de la CPU relue : Q0.0 à Q0.3 en 100 kHz. Q0.4 (PUL U4 en v8) était à 20 kHz : corrigé.
- Mémoire : nouveau contrôle `outils/xrs_chevauchements.py`, règle de disposition du f50, format des noms de broches, table des folios, chemin du format .xrs corrigé dans la mémoire locale.

## 02/11/2026 : v10
- Retours de Julien (f03, f04, f20, f21, f22, f24) avec 4 images (f20 variante USA, f21, f22, f24) + v9 modifiée, archivée dans `schema/recus/`.
- Dans son fichier : TR1 / U3 / M3 sans noms de broches, f21 descendu de 700, W1 et texte « vers -X11 » retirés au f20, 4 notes (f24, f25, f41, f53).
- v10 : `schema/generes/TTK_2026-11-02_v10.xrs` (25 folios, 133 symboles, 606 fils, 96 renvois ; 0 problème, 0 erreur verifier, 28 attentions connues, 0 chevauchement ; f04 : 0 texte coupé par un cadre ou une flèche). Détail : `memoire/06_EN_COURS.md`.
- Mémoire : règle des noms de broches, règle du synoptique, questions Q14 à Q16.

## 02/11/2026 (après-midi) : v11
- Retours de Julien : nouveau symbole moteur, réponses aux questions de la v10, f20, plan de folios, repérage des borniers, borniers f24 / f31.
- v11 : `schema/generes/TTK_2026-11-02_v11.xrs` (25 folios, 159 symboles, 628 fils, 94 renvois ; 0 problème, 0 erreur verifier, 28 attentions connues, 0 chevauchement).
- Proposition écrite : `docs/PROPOSITION_FOLIOS_BORNIERS_2026-11-02.md` (plan de folios par dizaines, repérage X<folio>.<groupe>.<borne>, avis de l'assistant, test WinRelais à faire).

## 02/11/2026 (soir) : v12
- Julien valide le plan de folios et XD1, corrige la règle des bornes (un seul point), replace les câbles du f32 à la main, demande f70 / f71 à jour et le rangement release / old.
- v12 : `schema/generes/release/TTK_2026-11-02_v12.xrs` (25 folios, 159 symboles, 628 fils, 94 renvois ; 0 problème, 0 erreur verifier, 28 attentions connues, 0 chevauchement ; sommaire = folios, même ordre).
- Mémoire : numéros de folio des fichiers memoire/ passés aux numéros v12 ; règle des bornes ; rangement release / old.
- Julien annonce qu'il regarde la v12 dans WinRelais. Mémoire mise à jour (Q8 → v12, questions ouvertes Q13, Q19, Q20). Pas de changement du schéma.

## 02/11/2026 (nuit) : v13
- Retours de Julien sur la v12 : f11 neutre, couleurs de tous les fils, f20 drivers + câble blindé, f31 / f32 broches, câble TF, superposition frein, f40 B2 + base de connaissances XPSUAF13AP (copiée dans `docs/references/`).
- Constat : la v12 de `release/` avait été réenregistrée par WinRelais (Julien l'a ouverte) ; archivée dans `schema/recus/`, 3 retouches relevées (Q21). Règle ajoutée dans `memoire/07_METHODE_TRAVAIL.md`.
- v13 : `schema/generes/release/TTK_2026-11-02_v13.xrs` (25 folios, 159 symboles, 631 fils, 93 renvois ; 0 problème, 0 erreur verifier, 28 attentions connues, 0 chevauchement).

## 02/11/2026 (nuit, suite)
- Réponses de Julien : Q21 oui (+ R1 au f32), Q23 oui, Q24 capteur codé ; Q22 : « est-ce obligatoire ? » (réponse : prescription de la notice Schneider).
- Dossier `folios/` supprimé. Aucune modification du schéma : Julien relit la v13.

## 02/11/2026 (nuit) : v15
- Retours de Julien : f10 cadre pointillé, f20 câble / bornes, f31 / f32 textes des câbles, S4 au f40, bornes de l'AU armoire, f62 nom des modules. W10 « 1-2-3-3 » signalé (le fichier généré porte 1-2-3-4 ; apparu après son déplacement à la main).
- La v13 réenregistrée par Julien est archivée dans `schema/recus/` ; ses retouches (textes, tableaux f61 / f62, f41, câbles) sont relevées par comparaison et reprises.
- Contrôle des chevauchements : largeur des textes avec la chasse Arial.
- v15 : `schema/generes/release/TTK_2026-11-02_v15.xrs` (25 folios, 165 symboles, 642 fils, 92 renvois ; 0 problème, 0 erreur verifier, 28 attentions connues, 0 chevauchement). Pas de v14 publiée.

## 03/11/2026 : revue des achats avant clôture
- Demande de Julien : fin des commandes, plus d'achat possible ensuite. Croisement de `Sourcing_Composant_2.xlsx` avec la v15, `memoire/` et la mémoire du projet.
- Résultat : `docs/REVUE_ACHATS_2026-11-03.md` (7 manques, 6 décisions conditionnant un achat, 14 contrôles, 9 incohérences, 9 risques). Q27 ouverte. Aucune modification du schéma.

## 03/11/2026 (suite) : réponses de Julien sur la revue des achats
- Réponses sur A1 à A6 (voir DECISIONS). Demande : liste à commander refaite et 2 références RS (porte-fusible + fusible) pour R-33.
- Références vérifiées sur fr.rs-online.com et fiches Mersen / NHP ; voyant du CMC101I écarté (seuil 50 V, inopérant en 24 V CC).
- Schéma inchangé : fusible R-33 et suppression du voyant de S4 à faire dans la prochaine version.

## 03/11/2026 (soir) : câble frein, raccord thermocouple
- Julien : câble frein sur le 5G1,5 de réserve (mémorisé) ; demande un raccord RS sonde / câble de compensation ; réponse « OUI » à la question 1 ou 2 machines pour le 2XSLCY-K (ambiguë, Q30).
- Vérifié : LIYCY-JZ 300/500 V CA ; sonde 350-398 : câble fibre de verre 2 m, écrou 1/2 pouce, terminaison non indiquée ; RS 891-9031 retenu en proposition.

## 03/11/2026 : reprise après la revue des achats
- git pull des commits du 03/11 (revue des achats, décisions). Julien : AU en 2 NF + 1 NO, il corrige la commande.
- Repère du fusible proposé : FA1. Liste des modifications de la v16 dans `memoire/06_EN_COURS.md` ; v16 pas encore générée.

## 04/11/2026 : v16
- Julien valide FA1 et demande la v16.
- v16 : `schema/generes/release/TTK_2026-11-04_v16.xrs` (25 folios, 165 symboles, 640 fils, 91 renvois ; 0 problème, 0 erreur verifier, 27 attentions connues, 0 chevauchement). Nouveau symbole `librairie/CUSTOM/Borne_4mm_terre_vert-jaune.xsy`.

## 04/11/2026 : prompt pour l'agent d'implantation
- Julien demande un prompt de mise à jour pour son agent draw.io (implantation de l'armoire). Écrit : `docs/PROMPT_AGENT_IMPLANTATION_2026-11-04.md` ; dossier `implantation/` créé (README).
- Mémoire : anciens repères corrigés dans `memoire/02_MATERIEL.md` ; conflit X12 / X13 (répartiteur, barrette de terre) contre X12.11 relevé.


## 05/11/2026 : prochains points, câbles 27G1 / 19G1
- Julien : garder le NO sur B3 à B6 ; repères du répartiteur et du bornier de terre au choix (→ -XR1, -XPE1) ; brochage X6 du MCX91A ; question sur ENA (DIR+ / DIR- ?) ; fiche Eaton (`Documents/10. TTK/eaton_com_ttk.md`) ; demande quoi mettre dans le 27G1 (en priorité) et le 19G1.
- Réponse : X6 conforme au schéma ; ENA = question de logique (actif ou libéré quand alimenté), pas de câblage ; Eaton sans numérotation des contacts ; proposition de répartition 27G1 / 19G1 et analyse du risque du 03/11.

## 05/11/2026 : implantation v4, v5, v6
- v4 commitée et poussée (accord de Julien). v5 : QS1 à 140 mm, XR2 sur R4, R5 groupé par câble. v6 : frein en un seul 5G1,5 + PE à créer, W11 / W12 de la proposition Q32, B2 par son câble M12, repères XR1 / XR2 / XPE1.
- Julien : cotes de montage gérées par lui ; boîte de dérivation machine ; mise à jour de `memoire/` et `docs/` demandée.
- Julien (suite) : XR1 / XR2 ; images des contacts Eaton ; ENA alimenté = moteur libre ; tableau 27G1 par composant demandé ; 21-22 = IHM seulement ? ; quels fils oubliés ? ; sondes TF à voir avec SEW ; B2 par son câble M12 : oui.
- Réponse : ponts Eaton → 4 inverseurs, schéma S3 à revoir (option D) ; tableau par composant ; oublis possibles : bornes H1, appareils de porte S4 / H2 / H3 / H4, liaison équipotentielle, frein unique à dessiner.

## 05/11/2026 : implantation v7
- Julien : W3 pour le câble frein unique, XR2 validé, Q32 en attente. Implantation v7 (étiquettes W3 et XR2), mémoire à jour.
- Julien (suite 2) : ponts Eaton retirés (3 photos) ; séparer les bornes TF ; butées entre fonctions du 27G1 ; qui sont S4 / H2 / H3 / H4 ; câble de terre seul vers le bâti.
- Réponse : photos lues (ponts = fils sur bornes paires, côté impair sans pont) ; numérotation 1-16 proposée ; rappel des appareils de porte.

## 05/11/2026 : v17
- Julien : nommer les contacts AUTO-A, AUTO-B... avec leur fonction ; porte : bornes pour tous ou pour aucun ; colonne par des bornes.
- v17 : `schema/generes/release/TTK_2026-11-05_v17.xrs` (25 folios, 177 symboles, 652 fils, 91 renvois ; 0 problème, 0 erreur verifier, 27 attentions connues, 0 chevauchement).

## 05/11/2026 : v18
- Julien : redonner la répartition 27G1 / 19G1 complète ; câble frein 5G1,5 (seul câble en stock) ; terre du bâti 2,5 ou 4 mm², repère au choix.
- v18 : `schema/generes/release/TTK_2026-11-05_v18.xrs` (0 problème, 0 erreur, 28 attentions, 0 chevauchement). Frein unique -W4, terre du bâti -W13. Erreur W3 / W4 de la mémoire corrigée ; l'agent d'implantation doit passer son câble frein de W3 à W4.

## 05/11/2026 : v19
- Julien : le 24 V à côté des fils de KA1 n'est pas un risque (gaine par conducteur, cheminement soigné) ; valide la répartition 27G1 / 19G1.
- v19 : `schema/generes/release/TTK_2026-11-05_v19.xrs` (0 problème, 0 erreur, 28 attentions, 0 chevauchement) ; f70 : W11 / W12 conducteur par conducteur, butées.

## 05/11/2026 : implantation v8
- Julien : « regarde le repo et les mises à jour, fais les modifs, plan complet ». Implantation v8 selon la v19 : W11 / W12 avec butées, TF W3 / W6 isolés, freins W4, H1 X61.1x, porte sur R4, passe-câbles W4 / W13.

## 05/11/2026 : v20
- Julien : f21 en PTFIX 6/12X2,5 (3273354) avec couleurs du stock ; TF blanc / marron ; .xrs de test (blindé, numéros U3 / U4) ; type PROFINET créé en personnalisé ; demande une convention de numérotation simple, un tableau d'E/S d'ensemble, et pourquoi des contacts miroirs dans la boucle de réarmement.
- v20 générée ; tableau `docs/LISTE_ES_AUTOMATE.md` ; explication R-22 (boucle de retour) ; convention proposée.

## 05/11/2026 : v21
- Julien : type Profinet (rose foncé, +10 %) ; valide les E/S si l'assistant les valide ; veut des exemples de numérotation ; doute sur les contacts miroirs (le NC revient-il ?) ; la SM 1223 peut-elle piloter les drivers (PUL rapides) ?
- Réponse : v21 (fils Profinet) ; E/S revues, cohérentes ; drivers sur la CPU, pas sur la SM 1223 ; explication du retour des NC miroirs après un AU ; exemples de numéros.

## 05/11/2026 : retours implantation v8
- Julien valide la porte sur R4 et les butées (stock suffisant). Il a généré une v20, pas encore ouverte : l'agent d'implantation attend.

## 05/11/2026 : numérotation v2, réarmement
- Julien : ses collègues conseillent de numéroter aussi L1 / L2 / L3 / N, 24 V et 0 V ; demande la convention refaite avec exemples ; doute sur l'appui puis le relâchement du bouton de réarmement.
- Réponse : convention v2 (`memoire/04_REGLES_DESSIN.md`) ; séquence du réarmement START 3 expliquée, essai de banc proposé.
- Julien : retient la convention v2, envisage un point au milieu ; numérotation à la fin, après ses validations sécu / automate / borniers ; demande un .md pour faire l'essai des contacts miroirs avec un nouveau chat.
- Fait : `docs/ESSAI_BANC_BOUCLE_RETOUR.md` ; méthode de numérotation notée dans `memoire/04_REGLES_DESSIN.md`.
- Julien : numéros sans point ; demande ce qu'il reste à valider sur la v21. Réponse : liste sécurité / automate / borniers (`memoire/06_EN_COURS.md`).

## 05/11/2026 : v22
- Julien : freins libres en Manu voulus ; demande un récap SEW, les bornes de porte sur R4, des butées partout, une passe complète sur les bornes et une liste de validation à jour.
- v22 (`TTK_2026-11-05_v22.xrs`, 0 problème, 0 erreur, 0 chevauchement) ; `docs/QUESTIONS_SEW.md` ; liste de validation dans `memoire/06_EN_COURS.md`.

## 06/11/2026 : implantation v9
- Julien : « reprends à partir de la v21 » (release = v22). Implantation v9 : PTFIX 6/12 au f21, ordre de porte du f70 v22, butée de chaque côté de chaque appareil.

## 06/11/2026 : v23
- Julien : réponses SEW (TF : pas d'info ; frein permanent : oui ; 1 mise sous tension / h) ; explication des chaînes MANU-D et AUTO-A du f42 ; STO en chaîne U1 → U2 ; sécurité validée sinon ; bilan 24VSEC / 24VELEC ; revoir l'affichage du f70.
- v23 générée ; `docs/BILAN_24V.md` ; `docs/QUESTIONS_SEW.md` complété.

## 06/11/2026 : implantation v10
- Julien : PTFIX en long ; R2 fixé ; plan 1 page + détail des borniers comme au montage, groupes par câble et fonction. Fait (v10, schéma v23 sans changement de bornes).

## 09/11/2026 : v24
- Julien (retour le 09/11) : reposer la question SEW ; bilan 24 V bon ; f70 comme en vrai avec le rail ; il attaque la relecture de l'automate puis revient ; mise à jour complète des mémoires avant compaction.
- v24 (`TTK_2026-11-09_v24.xrs`, 0 problème, 0 erreur, 0 chevauchement) ; v23 réenregistrée archivée, sans retouche.
- Julien : « qu'appelles-tu mise sous tension ? je ne comprends pas le problème ». Expliqué : mise sous tension = fermeture de KM1 / KM2 (400 V sur L1-L3 du variateur, charge des condensateurs internes) ; chaque AU puis réarmement, et chaque Manu -> Auto, en fait une. Demandé la phrase exacte de SEW.
- Julien : logos des 3 entreprises au f01 et 2-3 retouches sur la v24, à reprendre ; mises sous tension ≈ 1 toutes les 8 h (Manu pour maintenance), AU seulement en urgence ; ne pas modifier le schéma pour le moment. Fait : comparaison (logos, 2 textes déplacés, 1 supprimé), reprise dans le script, essai identique, pas de nouvelle version.

## 13/11/2026 : v25
- Julien : repères 4 mm² reçus, numéroter les fils (f10 pour commencer) ; XR1 et XR2 collés sur le rail de QS1, rail plein, à noter et à reporter au schéma si besoin ; v25 avec les retouches de la v24.
- Fait : f10 numéroté, titre R4 du f70 corrigé, v25 générée (0 problème, 0 erreur, 0 chevauchement), mémoires à jour.
- Julien (v25) : numéroter f11, f12, f13 ; W13 au f10 bizarre ; arrivée trop serrée ; export PDF : un câble déborde sur toute la page ; f21 image du bornier, retirer les textes ; v26 avec contrôle complet des fils (sauf E/S automate).
- Fait : v26 (`TTK_2026-11-13_v26.xrs`, 0 erreur, 0 chevauchement) ; `docs/CONTROLE_FILS_v26.md`.
- Julien : garde H2 sur le bus (disjoncteur obligatoire ?) ; câble avec la numérotation v26 ; pas de v27 ; demande ce qui reste à valider. Répondu : pas de disjoncteur obligatoire mais fils de H2 à dimensionner pour 20 A (sinon fusible) ; bilan « reste à valider » dans `06_EN_COURS.md`.
- Julien : comment poser 1021-1024 et le 0 V des 2 alims en vrai ? Expliqué (un numéro = un potentiel, repère aux 2 bouts de chaque fil) ; noté dans 04_REGLES_DESSIN.
- Julien : numéros des câbles PROFINET ; bornes pour ventilateurs et éclairage avec leur position ; numéros f20, f21, f30 ; contrôle global des numéros ; images des blocs 24 V aux bonnes couleurs ; v27. Fait : v27 (`TTK_2026-11-13_v27.xrs`, 0 erreur, 0 chevauchement, numéros 0 problème).

## 16/11/2026 : v28
- Julien : L+ capt seul pour toutes les entrées ? ; vérifier les tableaux f60-f62 ; réserves plus propres ; H1 / H4 sur leur folio ; revoir noms, descriptions, contenu ; f63 propre ; f70 / f71 ; questions avant v28.
- Réponses : bloc noir X21.14 ; bornes X62 ; f80 / f85 / f90 gardés. v28 générée (0 erreur, 0 chevauchement, numéros 0 problème).
- Julien (16/11, après v28) : PTFIX noir en stock et place OK ; à quoi servent L+ / M capt ? ; f70 plus grand ; revue complète et état pour le stagiaire ; mise à jour du dépôt ; puis compaction. Fait : v29, `docs/REVUE_COMPLETE_v29.md`, `docs/A_FAIRE_IMPLANTATION_2026-11-16.md`, `.gitignore`, README.

## 16/11/2026 : v30
- Julien (après compaction) : OUI pour numéroter les folios restants. Fait : v30, tous les folios numérotés (333 numéros), 0 erreur, 0 chevauchement, numéros 0 problème.
- Julien : « Oui, garder » la numérotation des entrées CPU par l'entrée (6011-6026).

## 16/11/2026 : v31
- Julien : OK pour renommer 2L+ / 2M ; a modifié la v30 (tableau des câbles au f80, textes du f85) ; demande comment faire le folio Vue armoire avec WinArmoire. Fait : v31 (retouches reportées, 2L+ / 2M), procédure WinArmoire expliquée.

## 17/11/2026
- Julien (nouveau PC) : mettre les symboles CUSTOM sur git. Fait : `librairie_winrelais/sym_electrotech/CUSTOM` (42 fichiers, identiques au PC), README d'installation.
- Julien : oui pour compléter. Fait : 11 symboles du script ajoutés (cp1252, CRLF), 53 en tout.

## 17/11/2026 : dossier d'implantation, liste des câbles, synoptique
- Julien : mission en étapes (étape 0, charte, implantation, câbles, synoptique, PDF unique). Étape 0 rendue (sources, écarts v10 / v31, incohérences, questions).
- Julien : PC PRO JULIEN ; bornes X63 gardées ; W9 / W10 en 5G1,5 (« c'est quoi ces câbles ? » : câbles moteur pas-à-pas, driver → X20 → M3 / M4) ; sourcing pour 1 armoire ; bornes de terre en livraison ; +M-X1 validé ; blindage un seul côté ; méthode A ; travail dans `implantation/` ; « travaille en autonomie et propose la prochaine version ».
- Fait : `implantation/generateur/` (extraire.py, saisie.json, donnees.json, svg.py, generer.py), PDF `implantation/release/TTK_implantation_2026-11-17_v11.pdf` (10 pages, indice A) + rapport de contrôle : 0 texte trop large, 0 chevauchement, 0 écart avec le .xrs. v10 passée dans old/. v31 réenregistrée par WinRelais archivée dans `schema/recus/2026-11-17_v31_ouverte_WinRelais.xrs` (contenu identique), puis restaurée.
- Julien : « vérifie si ta mémoire est à jour, crée un .md si nécessaire » (avant compaction). Fait : `memoire/08_IMPLANTATION.md` (demande, générateur, saisie.json, règles du bornier, décisions, points ouverts, procédure de nouvelle version) ; renvois dans `memoire/README.md`, `CLAUDE.md` (01 à 08), `implantation/README.md`, `05_POINTS_OUVERTS.md`.

## 17/11/2026 : méthode câbles / bornes selon le stock
- Julien : fixer une méthode pour savoir comment le schéma est construit selon le stock ; d'abord les câbles, puis les références des bornes (réelles) ; un tableau borne / câble / direction / fonction ; on ne commande plus rien sauf urgence.
- Fait : mémoire relue, méthode en 5 étapes proposée (stock → tableau des liaisons généré depuis le .xrs → contrôles → validation câble par câble → références des bornes au script). `memoire/09_STOCK.md` créé (stock épars dans 02, 05, 08 et saisie.json). Questions posées sur le format et le stock.

## 17/11/2026 : classeur des câbles
- Julien : format Excel / Google Sheet ; envoie son fichier de suivi de commande pour le stock ; seulement les câbles qui sortent ; références des bornes données une par une ; vérité dans un fichier indépendant du schéma, puis report au schéma ; d'abord les câbles en stock, puis la répartition par fonction.
- Fait : `cablage/TTK_CABLES.xlsx` (Lisez-moi, Stock câbles pré-rempli depuis la mémoire avec « ? », Liaisons par fonction vide), `cablage/README.md`, `memoire/09_STOCK.md` (méthode, tableau câbles remplacé par un renvoi au classeur). Contestation faite une fois : risque d'écart entre le classeur et le schéma ; parade : comparaison automatique au moment du report.

## 17/11/2026 : stock câbles (sans longueurs)
- Julien : envoie `Demande de Commande Hugo.xlsx` ; pas de longueurs, on raisonne en type et fonction ; distinguer un manque de longueur d'un câble non prévu ou non attribué ; 19G1 et 27G1 sûrs (armoire → machine, fils au schéma) ; stock : 2 x 0,75, 4G2,5 blindé, 5G1,5 x 2, 27G1, 19G1, compensation « 2363958 ».
- Fait : classeur refait (colonnes de longueur retirées ; stock croisé avec la commande ; onglet Liaisons pré-rempli depuis le schéma v31 avec 3 statuts) ; `memoire/09_STOCK.md`.

## 17/11/2026 : conducteurs des câbles
- Julien : M12, Roline, V/J en stock ; H05VV-F pas en stock ; pas de câble après +M-X1 pour l'instant ; 27G1 au pupitre ; veut un aperçu clair des fonctions de chaque fil de chaque câble, avec les câbles et fonctions sans rien.
- Fait : onglet « Conducteurs » (88 lignes) dans `cablage/TTK_CABLES.xlsx`, relevé du schéma v31 ; aperçu visuel (widget) par destination : pupitre, boîte +M-X1, direct. Point H1 (2 ou 3 couleurs) ajouté à 05.

## 17/11/2026 : référentiels câble et composant
- Julien : tableau très bien ; retirer la sortie de la boîte et PN4 (vision élec) ; H1 a bien 3 couleurs ; veut un visuel en référentiel câble et le même tableau en référentiel composant (chaque broche hors armoire raccordée).
- Fait : broches relevées dans le .xrs v31 (équipotentielles, bornes non passantes) ; 2 aperçus (câble, composant) ; onglet « Composants » (76 lignes) ; Conducteurs sans PN4 ni sortie de boîte. Trouvé : terre M3 / M4 sans broche, B2 33-34 et S3 13-14 en réserve.

## 17/11/2026 : boîte de dérivation machine
- Julien : garder les 2 tableaux dans le dépôt ; liste des bornes d'un rail DIN côté machine (comme R5), nombre de bornes et longueur ; terre des pas-à-pas par le V/J ; B2 33-34 réserve ; B3-B6 = RS 902-6874.
- Fait : `cablage/REFERENTIEL_CABLE.html` et `REFERENTIEL_COMPOSANT.html` (vérifiés dans le navigateur : 12 cartes chacun) ; onglet « Boîte machine » (34 lignes : base 24, option pas-à-pas 10) ; Composants mis à jour (M3 / M4, B3-B6).

## 17/11/2026 : tout par la boîte de jonction machine
- Julien : hypothèse « tous les fils de tous les câbles passent par la boîte machine » ; il rachète des PT si besoin ; nouveau nom clair pour la boîte ; câbles boîte → appareils : pas pour le moment.
- Fait : onglet « Boîte BJM » (84 lignes, n° de borne +BJM-X1:1 à 84, pupitre W11 en fin de rail) ; renommage +M-X1 → +BJM dans le classeur, les 2 pages HTML et la mémoire.

## 18/11/2026 : reprise sur le PC PRO RIMANE
- Julien : reprise du schéma sur le PC Rimane ; lire la mémoire ; archiver la v31 ouverte dans WinRelais ; la comparer à HEAD ; préparer identité git, chemins, nomenclature, images ; ne rien générer ni commiter.
- Fait : mémoire relue ; v31 copiée dans `schema/recus/2026-11-18_v31_ouverte_WinRelais.xrs` (release non restaurée) ; comparaison section par section (Perl, Python absent) ; analyse `docs/ANALYSE_PC_RIMANE_2026-11-18.md` (nomenclature ligne par ligne, images, chemins, virgule) ; `memoire/07` (2 clones), 05, 06 mis à jour. Aucun commit (pas d'identité git).

## 18/11/2026 : identité git, Python, CLAUDE.md
- Julien : identité JulienBEBL / julien@bebl.fr en `--local` ; Python installé ; OK pour corriger `CLAUDE.md`.
- Fait : `git config --local` (vérifié) ; contrôles Python sur la v31 de HEAD (mêmes résultats que sur le PC de Julien) ; `CLAUDE.md` § 7 ; mémoire 05, 06, 07. Commit local sans push. Release v31 toujours non restaurée.

## 18/11/2026 : nomenclature générée, essai images
- Julien : OK pour restaurer la release et copier les symboles ; option B pour la nomenclature, avec une étape de vérification après génération ; S1 / S2 et TR1 « à toi de choisir » ; OK pour la copie de test des images ; push du commit précédent.
- Fait : push c542fcc ; release restaurée ; 53 symboles CUSTOM installés ; essai : le script reproduit la v31 à l'identique sur ce PC ; `outils/nomenclature.py` (f90 + f91, 88 lignes) et son contrôle (a trouvé puis fait corriger : PTFIX comptés en PT 2,5, cartouche FA1 en double) ; copie `schema/generes/test_images/TEST_images_relatives.xrs`. Pas de v32 en release (accord attendu).

## 18/11/2026 : v32
- Julien : fins de course en NF ; types des bornes (PT 4 arrivée / moteurs / freins, PTFIX 2X4 1028361 pour W11 / W12, PT 2,5 sur R4) ; test des images relatives réussi ; OK commit, push, v32.
- Fait : symbole CUSTOM `Fin_de_course_NF_11-12.xsy` (copie de « Fin de course NC », broches 11 / 12), B3-B6 en NF ; `saisie.json` (types de bornes) ; nomenclature avec PTFIX 2X4 ; images relatives par défaut ; v31 dans old/ ; v32 générée : 0 problème, 0 erreur, 0 chevauchement, numéros 0 problème ; `LISTE_ES_AUTOMATE.md` en NF.

## 18/11/2026 : retours v32
- Julien : PTFIX 2X4 = 19 et 27 blocs, 2 trous, 6 mm ; PE OK ; retours f30, f31 / f32, f71, f80, f90 / f91 (copies d'écran) ; mettre à jour la mémoire, poser les questions, attendre le go.
- Fait : mémoire (04, 05, 06, 08, 09), questions posées. Aucune génération. Commit local, sans push.

## 18/11/2026 : v33
- Julien : réserves non bornées et X50.13 en terre ; OK pour f31 / f32 (2 lignes), f71 (1 ligne), f80 généré, f92 ; go v33.
- Fait : f30 textes décalés (le contrôle a d'abord trouvé 4 chevauchements PN / texte, corrigés) ; f31 / f32, f71 épurés ; f80 et f90-f92 par `nomenclature.tableau_pages` ; contrôle de la liste des câbles ; v32 dans old/ ; v33 : 0 problème, 0 erreur, 0 chevauchement.

## 18/11/2026 : revue v33
- Julien : f80 et nomenclature OK ; demande deux passes (points en suspens, puis folio par folio) ; schéma seulement, rapport unique, rien corrigé.
- Fait : v33 réenregistrée archivée (aucune retouche, images relatives gardées), release restaurée ; `docs/REVUE_SCHEMA_v33_2026-11-18.md` ; mémoire 05 / 06. Commit local, sans push.

## 18/11/2026 : v34
- Julien : +BJM non dessinée ; V/J W9 / W10 sur borniers sans raccordement moteur ; X63 en PT 2,5 ; frein inconnu ; X10 pas compris ; H2 en 2,5 mm² ; f85 = image de l'implantation plus tard ; go v34.
- Fait : v34 (f03, f20, f63, f70, f71, f85, nomenclature) ; v33 dans old/ ; 0 problème, 0 erreur, 30 attentions (2 fils V/J voulus), 0 chevauchement ; mémoire 02, 04, 05, 06, 08, 09. Commit local, sans push. Expliqué : X10 (bornes de la sonde TF sur le variateur) et H2.

## 18/11/2026 : implantation v12 (PC PRO RIMANE)
- Demande de Julien : nouvelle implantation +A1, 2 pages, R3 / R4 / R5 seulement, règles listées. Incohérences signalées avant de dessiner : format (généré depuis le 17/11), frein = W4 (pas W3), Q32 validée le 05/11, XR2 sur R2 (plus sur R4), B2 par son câble M12, thermocouple déjà borné X63.
- Réponses : générateur, oublier draw.io ; ordre R4 oui ; les 2 freins dans un seul câble (question du repère mal comprise : W4 gardé) ; Q32 pas comprise (reformulée).
- Fait : v12 (2 pages, schéma v34 commité pendant le travail), PTFIX 2X4 6 mm, X20.15 / X20.25, +BJM, W11 / W12 « à valider » ; v11 dans old/ ; 0 / 0 / 0 ; mémoire 05, 06, 08, README, journal d'implantation. Commit local, sans push.
- Suite : Julien valide W11 / W12 et le repère W4, accorde le push. v12 régénérée sans la marque « à valider » (0 / 0 / 0) ; mémoire 05, 08 ; push.

## 18/11/2026 : incohérences du chat automate
- Julien : 4 incohérences relevées par le chat automate (S12 unité SEW, S13 ENA, S14 titre liste d'E/S, S3 voyant S4).
- Fait : les 4 vérifiées dans le dépôt et vraies ; corrigé 02, 03, 05, `LISTE_ES_AUTOMATE.md`, `QUESTIONS_SEW.md` (question 6 à reposer). Schéma inchangé (aucun folio concerné). Commit local.
- Suite : Julien : oublier le stock ; W14 ok ; câbles +BJM → appareils plus tard. Fait : rapport v12 sans comparaison au stock, W14 non proposé ; mémoire 02, 05, 06, 08, 09.

## 18/11/2026 : réponse sur les incohérences
- Julien : S12 = 1 mise sous tension par heure ; S13, S14, S3 OK ; mettre à jour, vérifier, pousser.
- Fait : 05, 06, `QUESTIONS_SEW.md`, DECISIONS ; vérifié qu'aucune mention « par minute » ne reste comme hypothèse.

## 20/11/2026 : sections, QF10 en 2 A
- Julien : sections de 1333 / 1334 / 1343 / 1344 (prise) ? QF10 passe en 2 A Schneider. Sections des fils d'entrée (N, L1 / L2 / L3) et de sortie des alimentations ?
- Fait : réponse avec la règle (fil ≥ calibre amont) et des sections proposées ; 1343 / 1344 n'existent pas ; QF10 2 A noté (02, 05, DECISIONS) ; schéma non régénéré, attente du go v35 et de la référence. Commit local.

## 20/11/2026 : v35
- Julien : les fils sont 1323 / 1324 et 1333 / 1334 (QF9, QF10, XD1) ; relire la mémoire ; go v35 ; mettre à jour la mémoire et le dépôt.
- Fait : référence A9P71602 vérifiée ; symbole 2 A créé ; v35 (f13 + nomenclature) : 0 problème, 0 erreur, 0 chevauchement ; v34 dans old/ ; mémoire 02, 05, 06, 08, README, CLAUDE.md ; `saisie.json`. Commit et push.

## 20/11/2026 : fil de câblage 2,5 / 1,5 mm²
- Julien : quel fil dois-je avoir en 2,5 et 1,5 mm², par couleur ?
- Fait : pas de stock de fil intérieur dans la mémoire ; besoin déduit du schéma (sections du 20/11, couleurs du 02/11) ; questions posées (stock réel, départs du bus, couleur du 0 V).

## 20/11/2026 : stock de fil
- Julien : stock de fil de câblage par section et couleur.
- Fait : noté dans 09 ; comparé au besoin ; questions : bleus clairs ou foncés, couleurs du 24 V, bobines non identifiées.

## 20/11/2026 : couleurs 24 V
- Julien : bleus non identifiables ; pas d'orange ; 2,5 noir au lieu de 1,5 noir ; 24VDC en rouge 1,5 mm², sections max ? ; bobines noires avec une référence, bleues sans rien.
- Fait : réponse sections (24VELEC, 24VSEC, 0 V), 04 et 09 mis à jour ; proposé de câbler les 0 V de T1 et T2 séparément sur X21.12.

## 20/11/2026 : passe de vérification
- Julien : oublier les bobines sans identifiant ; mettre à jour la mémoire et le schéma si besoin ; vérifier le schéma puis la mémoire ; push.
- Fait : contrôles v35 sans erreur ; anomalie trouvée : XD1 « limitée 1,5 kW » (faux avec QF10 en 2 A) → v36 (f13 + nomenclature), v35 dans old/ ; mémoire corrigée (README du dépôt, CLAUDE.md, 05, 06, 09) ; commit et push.

## 20/11/2026 : implantation v13
- Julien : refaire une implantation propre et à jour d'après la mémoire et les derniers commits.
- Fait : v13 (2 pages, schéma v36) ; seuls changements : QF10 2 A, XD1 limitée à 2 A, renvoi page 2 ; bornes identiques à la v34 ; v12 dans old/ ; 0 / 0 / 0. Commit local, sans push.

## 20/11/2026 : 0 V commun T1 / T2
- Julien : relit la v36 ; l'autre session refait l'implantation ; inquiet de mettre les deux 0 V ensemble, propose deux borniers 0 V séparés.
- Fait : expliqué pourquoi le 0 V commun est nécessaire ; 03 complété (et anciens noms X31 / X32 / X33 / X36.1 corrigés).
- Julien : garde le 0 V commun.


## 23/11/2026 : reprise sur le PC PERSO JULIEN
- Julien : lire CLAUDE.md et la mémoire ; nouveau PC perso pour 3 mois ; notes de visio avec un collègue élec à venir.
- Fait : mémoire lue ; essai de génération de la v36 sur ce PC (identique) ; 3e clone noté (CLAUDE.md, 07, 05, README) ; question : installer les symboles CUSTOM.

## 23/11/2026 : symboles CUSTOM sur le PC perso
- Julien : Documents et Téléchargements recopiés du PC Rimane ; WinRelais et TIA Portal installés ; oui pour installer les CUSTOM.
- Fait : 54 symboles copiés ; v36 régénérée à l'identique (0 problème, 0 erreur, 0 chevauchement) ; 05, 07, DECISIONS mis à jour.

## 23/11/2026 : revue Krizox v36
- Julien : v36 bonne dans WinRelais ; notes brutes de la visio avec Krizox ; copie dans la mémoire + document des demandes bien écrites ; certaines à faire par Julien, d'autres par Claude, ou les deux.
- Fait : notes copiées dans `memoire/revues/` ; v36 relue folio par folio pour chaque note ; 25 demandes (D01-D25) avec état v36, action et qui ; 10 questions, lot 1 posé (Q2, Q3, Q5, Q7). README, 01, 05, 06 mis à jour.

## 23/11/2026 : revue des demandes Krizox, une par une
- Julien : revoir chaque demande une par une (brute + réécrite), go entre chaque ; ordre du fichier ; commit à la fin.
- Fait : D01 à D25 passées avec Julien ; décisions dans le fichier des demandes ; 4 images d'exemple de bornier rangées dans `memoire/revues/` ; règles dans 04 ; 05, 06 à jour. Rien modifié dans le script.

## 23/11/2026 : v37
- Julien : v37 en autonomie (toutes les demandes validées), + images qui ne se chargent pas, sommaire, W1 à l'export PDF ; plan d'action, vérification à chaque étape, mini rapport.
- Fait : v37 (30 folios) : boîte +BJM et câbles sur tous les folios, f21 refait, f41 / f43, synoptique par lieu, plans de bornier f71-f73, IP, KA2 2 pôles, W1, images ; contrôles à 0 ; rapport ; mémoire (02, 03, 04, 05, 06, 08, README), CLAUDE.md, demandes Krizox.

## 24/11/2026 : retours v37
- Julien : captures WinRelais, folios illisibles (numéros de fil sur câbles et cadres), demandes par folio ; plans de bornier OK ; découper le f60 ; puis mise en mémoire avant compactage.
- Fait : diagnostic du défaut commun, méthode, 4 questions ; tout noté en mémoire ; commit + push.

## 24/11/2026 : valeurs orales SEW (frein, STO)
- Julien : un technicien SEW a donné par téléphone STO 150 mW et frein BE5 / BGE1.5 maintien 0,18 A ; reporter en « oral, à confirmer par écrit », calculer l'effet, signaler les incohérences, ne rien modifier au schéma ; puis attendre ses autres questions pour SEW.
- Fait : valeurs reportées (QUESTIONS_SEW 1 et 2 + section « réponses partielles orales », 05 points 1 bis et 8, BILAN_24V, DECISIONS) ; calculs STO (6,25 / 12,5 mA contre 10 mA) et frein (0,18 A contre 2 A C, appel manquant) ; corrections de texte (n° de questions du BILAN, « en chaîne »). Rien généré, aucun .xrs modifié, pas de push.

## 24/11/2026 : mail à Xavier (SEW)
- Julien : STO = 150 mW par variateur ; reprendre les questions SEW sans réponse ; mail à Xavier : contexte, écart consigne / réel à vide, puis autres questions.
- Fait : 3 réponses de cadrage (français, contexte technique, plage 30-137 tr/min) ; brouillon `docs/MAIL_SEW_XAVIER_2026-11-24.md` ; STO passé en cas A dans QUESTIONS_SEW, 05, BILAN, DECISIONS. Rien envoyé.
- Julien : rapport 10,61 ; mode de régulation = question à SEW ; signature automatique. Fait : mail sans champ à compléter.
- Julien : détailler la phrase de contexte du mail. Fait : machine de tressage, 2 axes indépendants, modes Auto / Manu (source : 01_PROJET, 03 ; sans nom de client).
- Julien : mail envoyé à Xavier, réponse attendue. Fait : statut noté (mail, QUESTIONS_SEW, DECISIONS).


## 24/11/2026 : v38
- Julien : réponses aux 4 questions (1 a, 2 numéros plus petits partout de 30-40 %, 3 oui, 4 oui) ; faire la v38, mémoire, commit + push ; vérifier les autres commits.
- Fait : commits [perso] SEW récupérés (aucun ne touche au schéma) ; contrôle élargi ; v38 (31 folios) ; rapport `docs/RAPPORT_v38_2026-11-24.md` ; mémoire (03, 04, 05, 06, 08, README, retours), CLAUDE.md, README.

## 24/11/2026 : retours v38
- Julien : captures de la v38 (f31/32, f40-43, f61, f63, f64, f70, f71-73) ; questions avant la v39 (`memoire/revues/2026-11-24_retours_julien_v38.md`).

- Julien : réponses (1 oui, 2 oui + tableau, 3 oui, 4 toutes les bornes de terre + bornier) ; GO v39, mémoire, sync ; rapport + phrase de reprise.
- Fait : v39 (rapport `docs/RAPPORT_v39_2026-11-24.md`), mémoire, commit + push.

- Julien : passage à Sonnet + compactage ; fait : `memoire/10_REPRISE_AUTRE_MODELE.md`, contrôles copiés du scratchpad dans `outils/controles/` (tout.sh), CLAUDE.md.
