# 05 · Points ouverts et valeurs à vérifier

Ne jamais inventer de valeur : tant qu'un point est ici, le schéma porte la valeur provisoire ou rien.
Ces points étaient dans les notes encadrées des folios jusqu'à la v6 ; ils sont maintenant **uniquement ici**.

## Questions à Julien
| # | Sujet | État |
|---|---|---|
| Q8 | Retours sur la v20 (v19 relue le 05/11 : aucune retouche de position) | en attente |
| Q9 | Ordre interne du bloc sécurité | réglé le 30/10 : retour à l'ordre d'origine, f40 relais, f41 entrées, f42 sorties |
| Q10 | X12 (répartiteur) et X13 (barrette de terre) hors nomenclature WinRelais (non dessinés) | réglé le 29/10 : Julien les ajoute lui-même à la nomenclature |
| Q11 | Noms de broches | réglé le 02/11 : au cas par cas, à la demande de Julien |
| Q12 | f31 / f32 : l'image du défaut d'affichage des câbles n'est pas arrivée (reçu : f10, f13, f60). Corrigé par calcul ; à confirmer à l'écran | à vérifier |
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
| Q26 | W10 : brins « 1-2-3-3 » vus dans WinRelais après déplacement du câble à la main ; le fichier généré porte 1-2-3-4 | à revoir à l'ouverture de la v15 |
| Q27 | Clôture des achats : `docs/REVUE_ACHATS_2026-11-03.md` | 03/11 : A1, A2, A4 au tableau ; A6 déjà commandé ; A3 et A5 sans achat ; B1 fusible retenu ; B2 sans objet (antiparasite intégré). Restent : A7, B3 à B6, C1 à C14 |
| Q28 | Jonction sonde K (câble 2 m) / câble de compensation 25 m | 03/11 : proposé RS 891-9031 (paire fiche + prise miniature type K, 220 °C, câble ≤ Ø 4 mm), à placer là où l'ambiance reste < 105 °C (limite du câble 236-3959). Diamètre du 236-3959 et terminaison de la sonde 350-398 non indiqués par RS. Validation de Julien attendue |
| Q29 | Fixation de la sonde 350-398 : écrou 1/2 pouce (RS) contre cote Microdia « 12/Ø8 x 20 » | compatibilité à confirmer avant commande (sonde encore à FALSE) |
| Q30 | Câble moteur 2XSLCY-K 50 m : 1 machine ou 2 ? Julien a répondu « OUI » | à préciser |
| Q31 | Repères du répartiteur 4P AEE300427 et du bornier de terre Legrand 404839 (anciens X12 / X13, non dessinés) | **réglé le 05/11** : répartiteurs **-XR1 / -XR2** (Julien), bornier de terre **-XPE1** |
| Q32 | Répartition des câbles 27G1 (-W11) / 19G1 (-W12) | **validée par Julien le 05/11**, dessinée au f70 en v19 (conducteur → borne, butées entre fonctions). Risque du 03/11 (+24 V permanent à côté des fils après KA1) : **pas un risque pour Julien** (chaque conducteur a sa gaine, cheminement soigné) |
| Q33 | Câble frein unique M1 + M2 (5G1,5) | **réglé, dessiné en v18** : repère **W4** (W7 supprimé ; W3 / W6 = sondes TF), V/J → -XPE1 et boîte de dérivation |
| Q34 | Repère du 2e répartiteur : -XR2 | **réglé le 05/11** : XR1 et XR2 (Julien) |
| Q35 | Sélecteur S3 : la fiche Eaton montre des ponts 2-4, 6-8, 10-12, 14-16 → 4 inverseurs (1 commun + 2 sorties), pas 8 NO indépendants. Le schéma (8 NO, 7 utilisés, chacun sur son potentiel) ne tient pas | **réglé le 05/11** : les ponts sont des fils sur les bornes paires, **Julien les a retirés** (photos) → 8 contacts NO indépendants, option D abandonnée. Vraie numérotation et noms AUTO-A à MANU-D **dessinés en v17** |
| Q36 | Porte : S4 (réarmement, f40), H2 (voyant 230 V, f12), H3 (voyant 24VELEC, f21), H4 (voyant défaut, f61) câblés en direct alors que S1 passe par des bornes en bas | **réglé le 05/11** : tous par des bornes (X40.11-12, X12.21-22, X21.21-22, X61.21-22), dessiné en v17 ; règle « tous ou aucun » selon la place sur R5 |
| Q37 | Sondes TF des moteurs SEW livrées ? | 06/11 : SEW n'a pas l'information ; à voir à la réception des moteurs (le schéma garde W3 / W6 et X10) |
| Q38 | Liaison équipotentielle armoire ↔ bâti machine | **réglé, dessiné en v18** : -W13, V/J seul 4 mm², au f10 |
| Q39 | Butées d'arrêt sur rail DIN entre les fonctions d'un même câble (27G1 : AU / sélecteur / IHM / réserve) et autour des bornes TF X31.2x / X32.2x | **demandé par Julien le 05/11** ; dessiné en implantation v8 : 20 butées (R5 + porte), 10 mm chacune. **Stock suffisant** pour la 1re armoire (Julien 05/11 : 50 + 60 + 50 pour tous les projets) |

## Sécurité
1. Sortie de diagnostic du XPSUAF13AP : c'est Z1 (24 V, 20 mA, pulsée, non sécuritaire), déjà dans le symbole ; câblée sur I1.5 en v15 (Q23). B2 raccordée au 0 V en v13.
1 bis. Courant minimal des contacts du KA1 : 10 mA / 15 V (R-32) : courant des entrées STO des 2 MCX91A en parallèle à lire (SEW).
1 ter. Capot à deux technologies (B1 mécanique voie 1, B2 magnétique voie 2) : écart d'ouverture > 200 ms = alerte (R-16), à essayer au banc.
2. Charge de la sortie 13-14 : 3 bobines LC1D09BD à 5,4 W = 0,68 A sous 24 V, < 3 A DC-13 [C fiche Schneider LC1D09BD, 03/11]. 23-24 : 0,45 A.
3. Antiparasites des bobines LC1D09BD : **réglé, rien à ajouter** : « Built-in bidirectional peak limiting diode suppressor » [C fiche Schneider, 03/11].
4. Sélecteur Eaton T0-4-8223/E (RS 257-9558) : fiche reçue le 05/11 (`Documents/10. TTK/eaton_com_ttk.md`). Courant minimal **réglé** : fiabilité < 10^-5 à 24 V CC / 10 mA, DC-13 10 A [C fiche Eaton]. **Numérotation reçue le 05/11** (images du PDF) : position 1 ferme 1-2, 5-6, 9-10, 13-14 ; position 2 ferme 3-4, 7-8, 11-12, 15-16 ; ponts 2-4, 6-8, 10-12, 14-16 (Q35). Recouvrement Auto / Manu à la continuité.
5. ifm MN508S : homologation sécurité (EN 60947-5-3 / ISO 14119) ; actionneur codé commandé ? ; brochage M12 8 broches ; câble M12.
6. AU XB5AS8442 : 2 NF + 1 NO (ZBE102 = NF, ZBE101 = NO), réglé le 03/11 (Q25).
7. Fins de course B3 à B6 : **réglé le 05/11, on garde le NO** (choix de Julien).

## Puissance et variateurs
8. Courant du frein BE5 → calibre et courbe de QF2 / QF3 ; section du câble frein (appel SEW).
9. X6 (STO) **réglé le 05/11** (Julien, notice SEW) : X6.1 / X6.3 = F_STO_P +24 V, X6.2 / X6.4 = F_STO_M 0 V, X6.5 VO24_STO / X6.6 GND non utilisés ; câblage du schéma conforme. Reste X10 (TF) et le courant des entrées STO (point 1 bis).
10. Mises sous tension du MCX91A (= fermeture de KM1 / KM2, 400 V sur L1-L3) : réponse SEW « 1 » (06/11). Usage (Julien, 09/11) : environ **1 mise sous tension toutes les 8 h** (passage en Manu pour la maintenance, puis retour en Auto) ; l'AU est réservé aux urgences, pas d'usage normal. Compatible avec la réponse « 1 » de SEW : **on garde KM1 / KM2**, point clos.
11. Câbles frein 5G1,5 (réserve) et TF 2x0,75 blindé (acheté) : longueurs à définir. Câbles pas-à-pas W9 / W10 (4 conducteurs blindés) : section et longueur à définir.

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
21. Symbole Hager NFT702 : créé par copie du NFT706 dans `outils/librairie/CUSTOM/`, pas dans la librairie WinRelais du PC. À copier dans `sym_electrotech\CUSTOM` si Julien veut le poser à la main.

## Divers
22. (réglé le 29/10 : KM3 renommé KA2, contacteur auxiliaire.)
23. Câbles 27G1 / 19G1 : proposition du 05/11 (Q32) dans `02_MATERIEL.md`.
24. Classeur Excel à mettre à jour avec le nommage du 28/10.
25. Description de cartouche obsolète du f51 « contacteurs, freins » (f51 figé ; f02, f10 corrigés en v7).
26. f21 : images des borniers à insérer par Julien. f01 : logos **insérés par Julien en v24** (09/11), repris par le script (`schema/images/`).

## Essais de banc à prévoir (05/11)
Procédure pour un nouveau chat : `docs/ESSAI_BANC_BOUCLE_RETOUR.md`.
- Boucle Y1-Y2 avec un NF miroir de LC1D09BD en série avec le bouton (START 3) : réarmement normal accepté ; NF ouvert (fil retiré, contacteur tenu enclenché) : réarmement refusé. Déjà constaté le 02/11 : bouton enfoncé = START clignote, relâchement = sorties fermées (front descendant).

## Questions à SEW
Liste à jour : `docs/QUESTIONS_SEW.md` (05/11) : TF livrées, X10, courant STO, frein BE5, frein alimenté moteur à l'arrêt, mises sous tension / h, longueur de câble.

## Contrôle des fils v26 (13/11)
- **H2 voyant 230 V de porte** : piqué directement sur L3 / N du bus, seule protection QF1 20 A. **Julien (13/11) : il garde ce branchement.** Rappel fait une fois (NF EN 60204-1, 7.2) : pas de disjoncteur obligatoire pour un voyant, mais chaque fil doit être protégé contre les surintensités ; les fils de H2 (jusqu'à la porte) doivent donc tenir les 20 A de QF1 (1,5 mm² ne convient pas ; 2,5 mm² à vérifier selon le mode de pose dans le tableau de la norme), sinon un fusible 2 A sur L3. Numéros : 1023 / 1024. Détail : `docs/CONTROLE_FILS_v26.md`.

## v27 (13/11)
- Bornes : 93 dessinées (+ 4 bornes 230 V éclairage / ventilation) pour 85 achetées.
- EL1 / EL2 (RS 194-0417) et EV1 / EV2 (IDE VF92AC) : borne PE nécessaire ? (classe de l'appareil à vérifier).

## v28 (16/11)
- Achat / implantation : 4e bloc PTFIX 6/12 noir (-X21.14) sur R3 : en stock ? place sur R3 à confirmer (R3 était plein sur sa 1re partie).
- f80 / f85 / f90 : gardés (Julien 16/11), à remplir par WinRelais.

## Revue complète v29 (16/11)
Liste à jour des doutes, inconnus et manques : `docs/REVUE_COMPLETE_v29.md` (§ 3 à 6). Nouveaux :
- Nom des broches d'alimentation des sorties de la CPU : corrigé en 2L+ / 2M (v31). Reste : SM 1223 (K2) porte encore 3L+ / 3M, nom G2 à vérifier dans la doc Siemens.
- Réglage de QM1 / QM2 (GV2ME14 6-10 A) sur le courant d'entrée réel du MCX91A ; T3 240 W pour les 2 axes ; DC-1 du LC1D09BD sous 48 V.
- Nomenclature : références manquantes B3-B6, B7, W8, H2-H4, bornes, butées, PTFIX, câbles. S1 / S2 / S3 ajoutées en v29.
- PTFIX noir : en stock, place sur R3 OK (Julien 16/11).

## Câbles sortants (17/11, `cablage/TTK_CABLES.xlsx`)
- Colonne H1 : **réglé le 17/11**, la colonne reçue a bien 3 couleurs (Julien) ; la désignation « vert/rouge » de la commande est fausse.
- M3 / M4 (Nema 34) : **réglé le 17/11**, pas de borne de terre ; Julien raccorde le V/J de W9 / W10 à la masse du moteur.
- B2 (MN508S) : contact NF 33-34 non utilisé (réserve) ; W14 a 4 conducteurs libres.
- S3 13-14 (AUTO-D) : réserve, non dessiné. B3-B6 : **RS 902-6874** (Julien 17/11), contact NF libre (n° des bornes NF à relever). B2 33-34 : réserve « bonus ».
- Boîte machine +M-X1 (17/11, [H]) : 24 bornes de base (W12 + W4 : 22 PT 2,5 + 2 terre), 34 avec l'option pas-à-pas ; stock de PT 2,5 à confirmer (mémoire : 70 ; fichier de commande : 40 + 200) ; boîte elle-même non achetée ; câbles boîte → appareils non prévus.
- W14 (M12) : couleurs des 4 conducteurs utilisés à relever ; W2 / W5 : marquage U V W à relever ; W3 / W6 : blanc = 1b proposé ; W9 / W10 : V/J côté moteur à vérifier.

## Implantation v11 (17/11)
Détail : `08_IMPLANTATION.md` § Points ouverts. 4 PT 2,5 manquantes (74 / 70) ; X21.14 à droite de K4 [H] ; W14 [H] ; câbles +M-X1 → appareils ; au schéma : W9 / W10 « 4 cond. » → 5G1,5, W11 / W12 / W14 / PN absents du f80.
