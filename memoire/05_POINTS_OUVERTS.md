# 05 · Points ouverts et valeurs à vérifier

Ne jamais inventer de valeur : tant qu'un point est ici, le schéma porte la valeur provisoire ou rien.
Ces points étaient dans les notes encadrées des folios jusqu'à la v6 ; ils sont maintenant **uniquement ici**.

## Questions à Julien
| # | Sujet | État |
|---|---|---|
| Q8 | Retours sur la v20 (v19 relue le 05/11 : aucune retouche de position) | **réglé le 18/11** : dépassé, v33 relue |
| Q9 | Ordre interne du bloc sécurité | réglé le 30/10 : retour à l'ordre d'origine, f40 relais, f41 entrées, f42 sorties |
| Q10 | X12 (répartiteur) et X13 (barrette de terre) hors nomenclature WinRelais (non dessinés) | réglé le 29/10 : Julien les ajoute lui-même à la nomenclature |
| Q11 | Noms de broches | réglé le 02/11 : au cas par cas, à la demande de Julien |
| Q12 | f31 / f32 : l'image du défaut d'affichage des câbles n'est pas arrivée (reçu : f10, f13, f60). Corrigé par calcul ; à confirmer à l'écran | **réglé le 18/11** : bloc de droite refait en v33 |
| Q13 | f62 : mention rouge « PROPOSITION A VALIDER » | **réglé le 05/11** : retirée en v22 (E/S validées) |
| Q14 | W1 au f10 | réglé le 02/11 : on le garde |
| Q15 | Notes du .xrs du 02/11 | réglé : f41 barres retirées ; f63 bornes TC posées (type à définir) ; f21 « borniers sur la page alims » **en pause** |
| Q16 | f20 « Pour simplifier le » | réglé : rien à ajouter |
| Q17 | Plan de folios et repérage des bornes | réglé le 02/11 : appliqué en v12 (1 seul point dans le repère) |
| Q18 | Prise de service X14 → XD1 | réglé le 02/11 : oui |
| Q19 | Référence des bornes thermocouple (f63) | à définir à l'achat |
| Q20 | Câbles M1 / M2 | réglé : frein LIYCY-JZ 5G1,5 blindé de réserve (03/11), sonde TF 2x0,75 blindé (02/11) |
| Q21 | Retouches de Julien dans la v12 | réglé : reprises en v15 (R1 et R2 décalées, textes f10 et f63) |
| Q22 | Fusible R-33 en amont des contacts 13 / 23 / 33 de KA1 | **réglé et dessiné en v16 (04/11)** : FA1 au f40, Mersen CMC101 + FR10GG50V4 gG 4 A ; repère FA1 validé par Julien |
| Q23 | Z1 → I1.5 | fait en v15 ; décodage des trames à confirmer dans TIA |
| Q24 | Capteur de capot B2 codé ou non | **réglé le 02/11 : codé** (ifm MN508S). La base XPSUAF (§14.1, « non codé ») est fausse sur ce point |
| Q25 | Contacts des AU S1 / S2 | **réglé le 03/11** : Julien change la commande, **2 NF + 1 NO** par AU (XB5AS8442 + ZBE102 + ZBE101) ; schéma inchangé |
| Q26 | W10 : brins « 1-2-3-3 » vus dans WinRelais après déplacement du câble à la main ; le fichier généré porte 1-2-3-4 | **réglé le 18/11** : fichier généré juste (W10 en 5G1,5 depuis la v34) |
| Q27 | Clôture des achats : `docs/REVUE_ACHATS_2026-11-03.md` | 03/11 : A1, A2, A4 au tableau ; A6 déjà commandé ; A3 et A5 sans achat ; B1 fusible retenu ; B2 sans objet (antiparasite intégré). Restent : A7, B3 à B6, C1 à C14 |
| Q28 | Jonction sonde K (câble 2 m) / câble de compensation 25 m | 03/11 : proposé RS 891-9031 (paire fiche + prise miniature type K, 220 °C, câble ≤ Ø 4 mm), à placer là où l'ambiance reste < 105 °C (limite du câble 236-3959). Diamètre du 236-3959 et terminaison de la sonde 350-398 non indiqués par RS. Validation de Julien attendue |
| Q29 | Fixation de la sonde 350-398 : écrou 1/2 pouce (RS) contre cote Microdia « 12/Ø8 x 20 » | compatibilité à confirmer avant commande (sonde encore à FALSE) |
| Q30 | Câble moteur 2XSLCY-K 50 m : 1 machine ou 2 ? Julien a répondu « OUI » | à préciser |
| Q31 | Repères du répartiteur 4P AEE300427 et du bornier de terre Legrand 404839 (anciens X12 / X13, non dessinés) | **réglé le 05/11** : répartiteurs **-XR1 / -XR2** (Julien), bornier de terre **-XPE1** |
| Q32 | Répartition des câbles 27G1 (-W11) / 19G1 (-W12) | **validée par Julien le 05/11, reconfirmée le 18/11**, dessinée au f70 en v19 (conducteur → borne, butées entre fonctions). Risque du 03/11 (+24 V permanent à côté des fils après KA1) : **pas un risque pour Julien** (chaque conducteur a sa gaine, cheminement soigné) |
| Q33 | Câble frein unique M1 + M2 (5G1,5) | **réglé, dessiné en v18** : repère **W4** (W7 supprimé ; W3 / W6 = sondes TF), V/J → -XPE1 et boîte de dérivation |
| Q34 | Repère du 2e répartiteur : -XR2 | **réglé le 05/11** : XR1 et XR2 (Julien) |
| Q35 | Sélecteur S3 : la fiche Eaton montre des ponts 2-4, 6-8, 10-12, 14-16 → 4 inverseurs (1 commun + 2 sorties), pas 8 NO indépendants. Le schéma (8 NO, 7 utilisés, chacun sur son potentiel) ne tient pas | **réglé le 05/11** : les ponts sont des fils sur les bornes paires, **Julien les a retirés** (photos) → 8 contacts NO indépendants, option D abandonnée. Vraie numérotation et noms AUTO-A à MANU-D **dessinés en v17** |
| Q36 | Porte : S4 (réarmement, f40), H2 (voyant 230 V, f12), H3 (voyant 24VELEC, f21), H4 (voyant défaut, f61) câblés en direct alors que S1 passe par des bornes en bas | **réglé le 05/11** : tous par des bornes (X40.11-12, X12.21-22, X21.21-22, X61.21-22), dessiné en v17 ; règle « tous ou aucun » selon la place sur R5 |
| Q37 | Sondes TF des moteurs SEW livrées ? | 06/11 : SEW n'a pas l'information ; à voir à la réception des moteurs (le schéma garde W3 / W6 et X10) |
| Q38 | Liaison équipotentielle armoire ↔ bâti machine | **réglé, dessiné en v18** : -W13, V/J seul 4 mm², au f10 |
| Q39 | Butées d'arrêt sur rail DIN entre les fonctions d'un même câble (27G1 : AU / sélecteur / IHM / réserve) et autour des bornes TF X31.2x / X32.2x | **demandé par Julien le 05/11** ; dessiné en implantation v8 : 20 butées (R5 + porte), 10 mm chacune. **Stock suffisant** pour la 1re armoire (Julien 05/11 : 50 + 60 + 50 pour tous les projets) |

## Sécurité
1. Sortie de diagnostic du XPSUAF13AP : c'est Z1 (24 V, 20 mA, pulsée, non sécuritaire), déjà dans le symbole ; câblée sur I1.5 en v15 (Q23). B2 raccordée au 0 V en v13.
1 bis. Courant minimal des contacts du KA1 : 10 mA / 15 V (R-32) : courant des entrées STO des 2 MCX91A (en chaîne depuis la v23) à lire (SEW). **Réponse partielle ORALE du 24/11 [?], à confirmer par écrit** : entrée STO 150 mW **par variateur** (précisé par Julien le même jour) : **cas A retenu, 12,5 mA pour les 2, au-dessus de 10 mA** ; le cas B ci-dessous est écarté tant que l'écrit ne dit pas le contraire. Question 2 de `docs/QUESTIONS_SEW.md` **toujours ouverte**.
   - Calcul [H] (aucune valeur ajoutée) : 150 mW / 24 V = 6,25 mA.
   - Cas A, 150 mW par variateur : 2 × 6,25 = **12,5 mA** ≥ 10 mA ; marge 2,5 mA (25 %). Si l'entrée est résistive [H] (R ≈ 24² / 0,150 = 3,84 kΩ), le courant suit la tension : 10 mA atteints vers 19,2 V.
   - Cas B, 150 mW au total : **6,25 mA** < 10 mA ; il manque 3,75 mA. 15 V : 24 V suffit dans les 2 cas.
   - Le minimum de Schneider fixe la fiabilité du contact, pas le fonctionnement du STO. Le contact AUTO-B de S3 (Eaton) est en série : sa fiche donne la fiabilité à 24 V CC / 10 mA [C], rien en dessous.
   - Options si la marge ne suffit pas (aucune décision) : (a) confirmation écrite SEW, puis mesure du courant de la ligne STO au banc (02/12) : sans risque, mais après le câblage du 26/11 ; (b) résistance de charge sur la ligne STO, déjà envisagée en B3 de `docs/REVUE_ACHATS_2026-11-03.md` : pour ajouter 3,75 mA sous 24 V, R ≤ 6,4 kΩ (≈ 90 mW) ; risques : composant à ajouter à la nomenclature et au f42, nouveau point de défaut dans la chaîne STO, accord SEW nécessaire ; (c) faire commuter le STO par un contact de KA1 déjà chargé par des bobines (13-14 : 0,68 A, 23-24 : 0,45 A) ; risques : change la répartition validée le 06/11, charge min. assurée mais STO et bobines sur le même contact ; (d) garder tel quel si le cas A est confirmé par écrit ; risque : à 12,5 mA la marge est mince et la tension réelle n'est pas connue ; si le cas B : contact hors garantie, panne probable côté disponibilité (STO non libéré) plutôt que côté sécurité [H].
1 ter. Capot à deux technologies (B1 mécanique voie 1, B2 magnétique voie 2) : écart d'ouverture > 200 ms = alerte (R-16), à essayer au banc.
2. Charge de la sortie 13-14 : 3 bobines LC1D09BD à 5,4 W = 0,68 A sous 24 V, < 3 A DC-13 [C fiche Schneider LC1D09BD, 03/11]. 23-24 : 0,45 A.
3. Antiparasites des bobines LC1D09BD : **réglé, rien à ajouter** : « Built-in bidirectional peak limiting diode suppressor » [C fiche Schneider, 03/11].
4. Sélecteur Eaton T0-4-8223/E (RS 257-9558) : fiche reçue le 05/11 (`Documents/10. TTK/eaton_com_ttk.md`). Courant minimal **réglé** : fiabilité < 10^-5 à 24 V CC / 10 mA, DC-13 10 A [C fiche Eaton]. **Numérotation reçue le 05/11** (images du PDF) : position 1 ferme 1-2, 5-6, 9-10, 13-14 ; position 2 ferme 3-4, 7-8, 11-12, 15-16 ; ponts 2-4, 6-8, 10-12, 14-16 (Q35). Recouvrement Auto / Manu à la continuité.
5. ifm MN508S : homologation sécurité (EN 60947-5-3 / ISO 14119) ; actionneur codé commandé ? ; brochage M12 8 broches ; câble M12.
6. AU XB5AS8442 : 2 NF + 1 NO (ZBE102 = NF, ZBE101 = NO), réglé le 03/11 (Q25).
7. Fins de course B3 à B6 : NO le 05/11, **NF 11-12 depuis le 18/11 (v32, Julien)**.

## Puissance et variateurs
8. Courant du frein BE5 → calibre et courbe de QF2 / QF3 ; section du câble frein (appel SEW). **Réponse partielle ORALE du 24/11 [?], à confirmer par écrit** : redresseur BGE1.5, courant de **maintien 0,18 A** ; **courant d'appel non donné** ; côté CA ou CC et « par frein » non précisés. Question 1 de `docs/QUESTIONS_SEW.md` **toujours ouverte**.
   - Maintien 0,18 A contre QF2 / QF3 (2 A C) : 9 % du calibre. Chaque frein a son disjoncteur et ses propres brins dans W4 (M1 : L1 / L2, M2 : L1 / L3), donc 0,18 A par conducteur [H].
   - Câble 5G1,5 : 0,18 A est très inférieur à 2 A, et QF2 / QF3 protègent le câble. Tenue exacte (NF EN 60204-1, tableau 6) non relevée ; longueur de W4 non définie, donc chute de tension non calculée.
   - Charge de KA1 13-14 : **inchangée**. Le courant du frein passe par les contacts de puissance de KF1 / KF2, pas par KA1. 13-14 ne porte que les bobines (KF1, KF2, KA2 : 0,68 A < 3 A DC-13). Pouvoir de coupure des contacts de KF1 / KF2 : fiche non dans le dépôt [?].
   - **Appel manquant** : on ne peut pas juger le déclenchement magnétique de la courbe C. Seuil indicatif de 5 à 10 × In (IEC 60898) [H, à lire sur la fiche A9F74202], soit 10 à 20 A, soit 55 à 110 × 0,18 A. Le rapport appel / maintien du BGE1.5 est à demander.
   - 0,18 A est cohérent avec les 0,183 A à 400 V d'un chat du 27/08 (écart 1,6 %). Ce chat n'avait pas été vérifié ; l'accord ne prouve pas deux sources indépendantes (le technicien a pu lire la même table). Si 0,18 A est un courant CC de bobine, il ne dit rien du courant CA vu par QF2 / QF3.
   - Rien modifié : calibre, courbe et câble inchangés tant que l'appel manque.
9. X6 (STO) **réglé le 05/11** (Julien, notice SEW) : X6.1 / X6.3 = F_STO_P +24 V, X6.2 / X6.4 = F_STO_M 0 V, X6.5 VO24_STO / X6.6 GND non utilisés ; câblage du schéma conforme. Reste X10 (TF) et le courant des entrées STO (point 1 bis).
10. Mises sous tension du MCX91A (= fermeture de KM1 / KM2, 400 V sur L1-L3) : réponse SEW « 1 » (06/11). Usage (Julien, 09/11) : environ **1 mise sous tension toutes les 8 h** (passage en Manu pour la maintenance, puis retour en Auto) ; l'AU est réservé aux urgences, pas d'usage normal. Compatible avec la réponse « 1 » de SEW : **on garde KM1 / KM2**, point clos pour le schéma. **Rouvert le 18/11 pour le programme** (chat automate) : **réglé le 18/11 (Julien) : 1 mise sous tension par heure**. Programme : `T_SEW_ON` = 3600 s (AL04 dure 1 h après chaque retour en Auto) ; l'alarme AL04 supposait 1 / min (60 s).
11. Câbles frein 5G1,5 (réserve) et TF 2x0,75 blindé (acheté) : longueurs à définir. Câbles pas-à-pas W9 / W10 : **réglé le 17/11**, LIYCY-JZ 5G1,5 (étiquettes en v34).

## Très basse tension
12. DC-1 du LC1D09BD sous 48 V (KA2).
13. ENA du DM860H : **réglé le 05/11** (Julien) : ENA alimenté = moteur libre ; ENA non alimenté = driver actif. Q0.4 / Q0.5 à 1 pour libérer l'axe ; automate en STOP = axes tenus (le 48 V reste coupé par KA2 après un AU).

## Automate
14. Liste d'E/S : **validée par Julien le 05/11** (`docs/LISTE_ES_AUTOMATE.md`), revue par l'assistant : logique cohérente. Reste à vérifier au banc : I0.2 / I0.3 à 1 quand le capot est ouvert ; décodage des trames Z1 (I1.5) dans TIA.
15. Brochages G2 à confirmer (seuls ceux de la génération 1 ont été trouvés).
16. PUL sur Q0.0 (U3) et Q0.2 (U4) : sorties 100 kHz de la CPU d'après la fiche Siemens [C] ; la SM 1223 ne pilote **aucun** driver (colonne et voyant seulement). Fréquence utile = vitesse (tr/s) × pas par tour réglés sur le DM860H : choisir le micro-pas pour rester sous 100 kHz. Affectation PTO (impulsion + direction) à vérifier dans TIA V21.

## WinRelais (champs du format .xrs inconnus)
17. Champ « câble blindé » : **réglé le 05/11** (.xrs de Julien) : 3e valeur de la ligne `802·500·n` du DefCable = type : 0 Simple, 1 Rectangle, 2 Blindé (Ellipse), 3 Blindé (Ellipse + Trait), 4 / 5 Blindé (Rectangle arrondi / + Trait). v20 : 3 pour W2 à W6, W9, W10 ; 0 pour W1, W8, W13 (paramètre `blinde` de `g.cable`). Avant la v20, W1 et W8 portaient 5 et 2 par erreur.
18. Champ « afficher les numéros » des broches : **réglé le 05/11** : 6e champ (index 5) de la 3e ligne du symbole, déjà piloté par `noms=` dans `g.place` (Julien : U4 mis à 1 dans son test, U3 à 0). U3 / U4 restent à 0 dans la v20 (à changer si Julien le veut).
19. Type de conducteur PROFINET : **réglé le 05/11, appliqué en v21** : nom « Profinet » (type personnalisé de Julien), rose foncé RGB(199, 21, 133) = 8721863, épaisseur 44 (puissance 40 + 10 %). Type `PN` de `xrs_gen.TYPES`.
20. Numéros de fil générés : reconnus par WinRelais comme numéros ou comme texte libre ? Messages du Journal à l'ouverture ?
21. Symbole Hager NFT702 : créé par copie du NFT706 dans `outils/librairie/CUSTOM/`, pas dans la librairie WinRelais du PC. **Réglé le 18/11** : symboles CUSTOM installés sur les 2 PC.

## Divers
22. (réglé le 29/10 : KM3 renommé KA2, contacteur auxiliaire.)
23. Câbles 27G1 / 19G1 : proposition du 05/11 (Q32) dans `02_MATERIEL.md`.
24. Classeur Excel à mettre à jour avec le nommage du 28/10.
25. Description de cartouche obsolète du f51 « contacteurs, freins » (f51 figé ; f02, f10 corrigés en v7). **Réglé** : description du f61 juste (revue v33).
26. f21 : images des borniers à insérer par Julien. f01 : logos **insérés par Julien en v24** (09/11), repris par le script (`schema/images/`). **Réglé** : images en chemin relatif (18/11).

## Essais de banc à prévoir (05/11)
Procédure pour un nouveau chat : `docs/ESSAI_BANC_BOUCLE_RETOUR.md`.
- Boucle Y1-Y2 avec un NF miroir de LC1D09BD en série avec le bouton (START 3) : réarmement normal accepté ; NF ouvert (fil retiré, contacteur tenu enclenché) : réarmement refusé. Déjà constaté le 02/11 : bouton enfoncé = START clignote, relâchement = sorties fermées (front descendant).

## Questions à SEW
Liste à jour : `docs/QUESTIONS_SEW.md` (24/11, 16 questions). Réponses **orales partielles** du 24/11 sur les questions 1 (frein : maintien 0,18 A) et 2 (STO : 150 mW), à confirmer par écrit : voir points 1 bis et 8.

## Contrôle des fils v26 (13/11)
- **H2 voyant 230 V de porte** : piqué directement sur L3 / N du bus, seule protection QF1 20 A. **Julien (13/11) : il garde ce branchement.** Rappel fait une fois (NF EN 60204-1, 7.2) : pas de disjoncteur obligatoire pour un voyant, mais chaque fil doit être protégé contre les surintensités ; les fils de H2 (jusqu'à la porte) doivent donc tenir les 20 A de QF1 (1,5 mm² ne convient pas ; 2,5 mm² à vérifier selon le mode de pose dans le tableau de la norme), sinon un fusible 2 A sur L3. Numéros : 1023 / 1024. Détail : `docs/CONTROLE_FILS_v26.md`.

## v27 (13/11)
- Bornes : 93 dessinées (+ 4 bornes 230 V éclairage / ventilation) pour 85 achetées.
- EL1 / EL2 (RS 194-0417) et EV1 / EV2 (IDE VF92AC) : borne PE nécessaire ? (classe de l'appareil à vérifier).

## v28 (16/11)
- Achat / implantation : 4e bloc PTFIX 6/12 noir (-X21.14) sur R3 : en stock ? place sur R3 à confirmer (R3 était plein sur sa 1re partie).
- f80 / f85 / f90 : **réglé** : f80 et f90-f92 générés par le script (v32 / v33) ; f85 = image du plan d'implantation quand il sera validé (Julien 18/11).

## Revue complète v29 (16/11)
Liste à jour des doutes, inconnus et manques : `docs/REVUE_COMPLETE_v29.md` (§ 3 à 6). Nouveaux :
- Nom des broches d'alimentation des sorties de la CPU : corrigé en 2L+ / 2M (v31). Reste : SM 1223 (K2) porte encore 3L+ / 3M, nom G2 à vérifier dans la doc Siemens.
- Réglage de QM1 / QM2 (GV2ME14 6-10 A) sur le courant d'entrée réel du MCX91A ; T3 240 W pour les 2 axes ; DC-1 du LC1D09BD sous 48 V.
- Nomenclature : références manquantes B3-B6, B7, W8, H2-H4, bornes, butées, PTFIX, câbles. S1 / S2 / S3 ajoutées en v29.
- PTFIX noir : en stock, place sur R3 OK (Julien 16/11).

## Câbles sortants (17/11, `cablage/TTK_CABLES.xlsx`)
- Colonne H1 : **réglé le 17/11**, la colonne reçue a bien 3 couleurs (Julien) ; la désignation « vert/rouge » de la commande est fausse.
- M3 / M4 (Nema 34) : **réglé le 17/11**, pas de borne de terre ; Julien raccorde le V/J de W9 / W10 à la masse du moteur. **Changé le 18/11 (v34)** : V/J sur une borne de terre côté armoire (X20.15, X20.25), **non raccordé au moteur** (fil de terre en plus).
- B2 (MN508S) : contact NF 33-34 non utilisé (réserve) ; W14 a 4 conducteurs libres.
- S3 13-14 (AUTO-D) : réserve, non dessiné. B3-B6 : **RS 902-6874** (Julien 17/11), contact NF libre (n° des bornes NF à relever). B2 33-34 : réserve « bonus ».
- Boîte de jonction machine +BJM (17/11) : tout passe par la boîte → 57 bornes (84 avec le pupitre W11) ; W11 par la boîte ou en direct ? blindage des tronçons boîte → appareil (côté boîte ?) ; W8 : 2 bornes cuivre acceptables si les deux sont à la même température ; W14 : câble M12 coupé en deux ; stock de PT 2,5 à confirmer (mémoire : 70 ; fichier de commande : 40 + 200) ; boîte elle-même non achetée ; câbles boîte → appareils non prévus.
- W14 (M12) : couleurs des 4 conducteurs utilisés à relever ; W2 / W5 : marquage U V W à relever ; W3 / W6 : blanc = 1b proposé ; W9 / W10 : V/J côté moteur à vérifier.

## Implantation v12 (18/11)
- Stock (bornes, câbles) : **plus suivi** (Julien 18/11 : « oublie les histoires de stock »). L'implantation compte les bornes dessinées, sans comparaison au stock.
- Q32 (W11 / W12) : **reconfirmée validée le 18/11** (la demande d'implantation la disait non validée : texte périmé).
- X21.14 à droite de K4 [H] (seul point ouvert de l'implantation). W14 **validé** (18/11). Câbles +BJM → appareils : **Julien les définira plus tard**, pas à traiter.

## Revue v33 (18/11)
Liste à jour des zones d'ombre : `docs/REVUE_SCHEMA_v33_2026-11-18.md` § 1 (remplace `REVUE_COMPLETE_v29.md` § 3). Nouveaux :
- **+BJM** : **réglé le 18/11**, la boîte n'est pas dessinée (Julien). f80 : W4 / W12 vers +BJM, les autres vers +M.
- V/J de W9 / W10 : **réglé le 18/11 (v34)**, bornes de terre X20.15 / X20.25, non raccordé au moteur. **Stock : 6 bornes de terre dessinées pour 4 achetées** [?].
- Bornes X63 : **PT 2,5** (Julien 18/11, v34).
- f85 : **réglé le 18/11**, image du plan d'implantation à insérer quand il sera validé (Julien).
- Fils de H2 : **2,5 mm²** (Julien 18/11, « normalement »). Rappel : tenue sous QF1 20 A à vérifier selon le mode de pose (NF EN 60204-1, tableau 6) [?].
- Courant du frein BE5 : toujours inconnu (Julien 18/11).
- Revue § 1.D fermée le 18/11 (go v34).

## Sections des fils 230 V et 24 V (question de Julien, 20/11) [H]
- Règle : un fil doit tenir le calibre du disjoncteur juste en amont ; derrière une alimentation sans fusible, son courant maxi. Valeurs exactes : NF EN 60204-1, tableau 6, selon la pose [à vérifier].
- Proposé : 1323 / 1324 (QF9 16 A → QF10) **2,5 mm²** ; 1333 / 1334 (QF10 2 A → XD1) **1,5 mm²** ; bus → QF4 / QF5 / QF6 (sous QF1 20 A) comme le reste du bus ; QF4 / QF5 6 A → T1 / T2 et QF6 4 A → T3 (1201 / 1204, 1211 / 1214, 1222 / 1224) **1,5 mm²** ; T1 / T2 (10 A) → X21.11 / X21.12 / X21.13 **2,5 mm²** ; T3 (5 A) → U3 / U4 **1,5 mm²** ; départs 24 V de commande 0,75-1 mm² [à valider par Julien].
- Fils de la prise (Julien 20/11 : il parlait de 1323 / 1324 et 1333 / 1334, f13) : 1323 / 1324 en 2,5 mm² (sous QF9 16 A), 1333 / 1334 en 1,5 mm² (sous QF10 2 A). Sections non écrites sur les folios (pas de règle de dessin pour ça).
- Fil de câblage intérieur (20/11) : **aucun stock noté dans la mémoire** (09 ne couvre que les câbles sortants). Besoin déduit du schéma et des couleurs (04) : 2,5 mm² noir, bleu clair, bleu foncé, vert-jaune ; 1,5 mm² noir, bleu clair, vert-jaune (+ bleu foncé si 24 V en 1,5). Stock réel à donner par Julien [?].

## v38 (24/11) : à regarder par Julien
Détail : `docs/RAPPORT_v38_2026-11-24.md`.
- Lisibilité dans WinRelais des f20, f31, f32, f41-f43, f50, f60-f64 : **dépassé**, retours v38 / v39 traités en v39 / v40.
- f60 presque vide (CPU seule) : **réglé en v39** (tableau des entrées au f60).
- Repères déjà posés en X60 / X62 / X63 : à refaire (X61 / X63 / X64).
- Implantation à régénérer (boîte +BJM, X43, X61 / X63 / X64).

## v37 (23/11) : à valider par Julien
Détail : `docs/RAPPORT_v37_2026-11-23.md`.
- f41 coupé en deux (f43 = capots) et bornes X41.2x-4x renommées X43.1x-3x [H].
- Numérotation et ordre des 69 bornes de la boîte +BJM ; type de borne de la boîte [?].
- Sections des fils boîte -> appareils (proposées) [H] ; thermocouple : 2 bornes cuivre de plus dans la boîte [?].
- Images en chemin complet : justes seulement sur le PC qui génère.
- Export PDF de W1 (et W13) à revoir dans WinRelais.
- Implantation : la boîte et les bornes X43 ne sont pas encore dans le dossier d'implantation (check global prévu par Julien).

## Revue Krizox v36 (23/11)
- Questions Q1 à Q10 et demandes D01 à D25 : suivies dans `memoire/revues/2026-11-20_krizox_v36_demandes.md` (pas en double ici).
- **Revue faite le 23/11** (Julien, point par point) : 20 demandes pour la v37, 3 closes sans changement, 2 hors schéma.
- **Freins (D17), action externe au schéma** [?] : vérifier le câblage du frein réellement monté (plaque moteur, redresseur BG / BGE) et la logique de pilotage (notice SEW MCX91A, courant du frein pour QF2 / QF3, essais de rotation à la main en Manu, en Auto à l'arrêt, après AU). Lancée à part par Julien ; schéma modifié ensuite si besoin.
- **Après la v37** : check global des bornes et de l'implantation (Julien, D04).
- Adresses IP (D15) : fixées par Julien dans TIA, puis reportées au f30.
- Revenait sur des décisions passées : bornes de porte « tous ou aucun » (05/11, D04 / D23), boîte +BJM non dessinée (18/11, D08), freins desserrés en Manu par KA1 (05/11, D17).

## Reprise PC PERSO JULIEN (23/11)
- Symboles CUSTOM (54, `librairie_winrelais/`) à copier dans `C:\Users\Public\Documents\Elec-CAO\sym_electrotech\CUSTOM` : **réglé le 23/11** (accord de Julien) : installés, v36 régénérée à l'identique.

## Reprise PC PRO RIMANE (18/11)
- Identité git du PC Rimane : **réglé le 18/11**, `--local` JulienBEBL / julien@bebl.fr.
- Python sur le PC Rimane : **réglé le 18/11** (3.15.2, contrôles identiques au PC de Julien).
- Symboles CUSTOM sur le PC Rimane : **réglé le 18/11** (54 symboles installés).
- Nomenclature : **réglé le 18/11**, option B (script), S1 / S2 sur une ligne, TR1 gardé (EXT). Restent à compléter : références B7, H2, H3, H4, butées, +BJM.
- Valeurs du script absentes de la mémoire (source à retrouver) : QF1 10 kA, QS1 690 V, QF9 6 kA, T3 5 A et RS 122-2229, R1 / R2 08281718, U1 5,5 A, U3 6,0 A, M3 6 A - 8,5 Nm, EL 14 W, EV 19 W, S4 « Z000263594 ». (QF10 4,5 kA : source trouvée le 20/11, fiches distributeurs de l'A9P71602.) XD1 « limitée 1,5 kW » : **corrigé en v36** (« limitée à 2 A par -QF10 »).
- Images : chemin absolu `C:\Users\Julien\…` dans `¤#Logo¤`, cassé sur le PC Rimane. **Réglé le 18/11** : chemin relatif, images visibles (Julien) ; v32 en relatif. **Réglé le 18/11** : la v33 réenregistrée garde le chemin relatif.
- PTFIX 2X4 Phoenix 1028361 : 2 trous, 6 mm, 19 + 27 blocs (Julien 18/11). **Réglé le 18/11** : réserves non bornées, X50.13 reste une borne de terre vert/jaune ; 38 blocs dessinés.
- Bornes PE X10.11, X31.11, X32.11, X50.13 en bornes de terre ; X12.11 en PT 4 : **confirmé par Julien le 18/11**.
- Zoom écrit avec une virgule par WinRelais sur le PC Rimane (`0,749…`) : lecture par le WinRelais de Julien à vérifier.

## Fils 48 V : T3 -> KA2 -> U3 / U4 (question de Julien, 25/11) : **réglé le 25/11, noir 2,5 mm² (stock)** ; reste : section maxi des bornes du DM860H [?]
- Fils : +48 V 1251 (T3 -> KA2 1 et 3), 2001 (KA2 2 -> U3), 2011 (KA2 4 -> U4) ; 0 V 48 1250 (T3 -> U3, T3 -> U4, en direct). 0 V 48 (1250) distinct du 0 V commun 24 V (1230).
- Section proposée [H] : 1,5 mm² (T3 5 A, valeur du script, source à retrouver). Bornes du DM860H : section maxi à vérifier.
- Couleur : **noir 2,5 mm² pour le + et le -** [D 25/11, Julien], conforme à la norme (04). Repérage par les numéros de fil (1251, 2001, 2011, 1250). Rouge / bleu écartés (codes du 24 V).

## v40 (25/11) : à regarder par Julien
Détail : `docs/RAPPORT_v40_2026-11-25.md`.
- **f40 : réglé en v43** (textes à droite du contact, accrochés à gauche, décision de Julien du 26/11). Historique : accrochage du texte des contacts de retour. Le fichier porte déjà le code 0 (librairie : 0 = gauche, 2 = droite, 6 = centré) : valeur vue dans WinRelais et valeur voulue ? [?]
  26/11 : capture de Julien (v41) : textes de -KM1, -KM2, -KF1 alignés à gauche, à gauche du contact. Lecture : accrochage à gauche déjà en place ; confirmation demandée à Julien [?]
- f31 / f32 : résistance avec son repère seul (désignation masquée, faute de place) [H].
- f21 : pas d'image pour le bloc noir -X21.14 (aucune image noire) [?].
- Plans de bornier : rendu du vert / jaune dans WinRelais : **vu par Julien (26/11), rayé plus marqué en v42**.
  26/11 : capture de Julien (v41, -X31.11) : fond jaune, une bande verte en haut et en bas (sous les carrés de connexion), contour vert, numéro sur le jaune. Avis de Julien demandé (garder, ou plus de bandes) [?]

## v42 (26/11) : à regarder par Julien
Détail : `docs/RAPPORT_v42_2026-11-26.md`.
- f40 : textes à droite, accrochés à droite en v42, puis **accrochés à gauche en v43** (Julien : « je me suis trompé »).
- Plans de bornier : vert / jaune vu par Julien (26/11) ; **rayé plus marqué en v42** (bandes de 100).
- Rendu dans WinRelais : variateur élargi (f31 / f32) **validé par Julien (26/11)** ; thermocouple retourné (f64), gras et résumés des plans de bornier (résumé sous le cadre du repère en v43) : à relire sur la v43 [?].
- `implantation/generateur/saisie.json` : folios et origines de W8 (f64), W11 (X43.1x, pas de X41.2x), W12 (X43.2x, f43 / f61 / f63), W14 (f43) d'avant la v37 ; le schéma les relit sur le dessin. **Corrigé le 26/11** (accord de Julien) dans `saisie.json`.
- Haut des variateurs f31 / f32 : numéros sur une rangée juste au-dessus des broches (alignement v40), pas centrés (fils 24 V de 600) [H].
- Nomenclature : 6 bornes de terre dessinées pour 4 achetées ; références B7, H2, H3, H4, bornes +BJM, butées : à vérifier (inchangé) [?].

## v43 (26/11)
- W9 / W10 : le brin du V/J porte le n° 4 (comme le conducteur 4), repris de la retouche de Julien : voulu ? [?]
- f31 / f32 : variateur élargi validé par Julien (26/11).
- Relecture de la v43 par Julien dans WinRelais (W1, W9 / W10 repris, f40, plans de bornier, nomenclature en 300) [?].
