# 05 · Points ouverts et valeurs à vérifier

Ne jamais inventer de valeur : tant qu'un point est ici, le schéma porte la valeur provisoire ou rien.
Ces points étaient dans les notes encadrées des folios jusqu'à la v6 ; ils sont maintenant **uniquement ici**.

## Questions à Julien
| # | Sujet | État |
|---|---|---|
| Q8 | Retours sur la v16 | en attente |
| Q9 | Ordre interne du bloc sécurité | réglé le 30/10 : retour à l'ordre d'origine, f40 relais, f41 entrées, f42 sorties |
| Q10 | X12 (répartiteur) et X13 (barrette de terre) hors nomenclature WinRelais (non dessinés) | réglé le 29/10 : Julien les ajoute lui-même à la nomenclature |
| Q11 | Noms de broches | réglé le 02/11 : au cas par cas, à la demande de Julien |
| Q12 | f31 / f32 : l'image du défaut d'affichage des câbles n'est pas arrivée (reçu : f10, f13, f60). Corrigé par calcul ; à confirmer à l'écran | à vérifier |
| Q13 | f62 : mention rouge « PROPOSITION A VALIDER » conservée (Julien l'a retirée aux f60 et f61 seulement) | à confirmer |
| Q14 | W1 au f10 | réglé le 02/11 : on le garde |
| Q15 | Notes du .xrs du 02/11 | réglé : f41 barres retirées ; f63 bornes TC posées (type à définir) ; f21 « borniers sur la page alims » **en pause** |
| Q16 | f20 « Pour simplifier le » | réglé : rien à ajouter |
| Q17 | Plan de folios et repérage des bornes | réglé le 02/11 : appliqué en v12 (1 seul point dans le repère) |
| Q18 | Prise de service X14 → XD1 | réglé le 02/11 : oui |
| Q19 | Référence des bornes thermocouple (f63) | à définir à l'achat |
| Q20 | Câbles M1 / M2 | réglé le 02/11 : frein 2G1,5, sonde TF 2x0,75 blindé |
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
| Q31 | Repères du répartiteur 4P AEE300427 et du bornier de terre Legrand 404839 (anciens X12 / X13, non dessinés) : conflit avec les bornes X12.11 | à fixer (question aussi posée par l'agent d'implantation) |

## Sécurité
1. Sortie de diagnostic du XPSUAF13AP : c'est Z1 (24 V, 20 mA, pulsée, non sécuritaire), déjà dans le symbole ; câblage sur I1.5 validé (Q23), à faire. B2 raccordée au 0 V en v13.
1 bis. Courant minimal des contacts du KA1 : 10 mA / 15 V (R-32) : courant des entrées STO des 2 MCX91A en parallèle à lire (SEW).
1 ter. Capot à deux technologies (B1 mécanique voie 1, B2 magnétique voie 2) : écart d'ouverture > 200 ms = alerte (R-16), à essayer au banc.
2. Charge de la sortie 13-14 : 3 bobines LC1D09BD à 5,4 W = 0,68 A sous 24 V, < 3 A DC-13 [C fiche Schneider LC1D09BD, 03/11]. 23-24 : 0,45 A.
3. Antiparasites des bobines LC1D09BD : **réglé, rien à ajouter** : « Built-in bidirectional peak limiting diode suppressor » [C fiche Schneider, 03/11].
4. Sélecteur Eaton : photo de la plaque (numérotation réelle) ; recouvrement Auto / Manu à la continuité ; courant minimal des contacts sous 24 V.
5. ifm MN508S : homologation sécurité (EN 60947-5-3 / ISO 14119) ; actionneur codé commandé ? ; brochage M12 8 broches ; câble M12.
6. AU XB5AS8442 : 2 NF + 1 NO (ZBE102 = NF, ZBE101 = NO), réglé le 03/11 (Q25).
7. Fins de course : symbole « NF » (11-12) à poser, le symbole actuel est un NO.

## Puissance et variateurs
8. Courant du frein BE5 → calibre et courbe de QF2 / QF3 ; section du câble frein (appel SEW).
9. Bornes X6 (STO) et X10 (TF) du MCX91A (notice SEW).
10. Nombre de mises sous tension par heure du MCX91A (KM1 / KM2 ne servent pas d'arrêt de service).
11. Câbles frein 2G1,5 et TF 2x0,75 blindé : à commander, longueurs à définir. Câbles pas-à-pas W9 / W10 (4 conducteurs blindés) : section et longueur à définir.

## Très basse tension
12. DC-1 du LC1D09BD sous 48 V (KA2).
13. Polarité de l'entrée ENA du DM860H.

## Automate
14. Liste d'E/S à valider (f60 à f62 figés d'ici là).
15. Brochages G2 à confirmer (seuls ceux de la génération 1 ont été trouvés).
16. PUL sur Q0.0 (U3) et Q0.2 (U4) : sorties 100 kHz d'après la fiche Siemens [C]. Affectation PTO (impulsion + direction) à vérifier dans TIA V21.

## WinRelais (champs du format .xrs inconnus)
17. Champ « câble blindé » (W2, W4, W5, W7) : Julien coche « blindé » sur W2, enregistre, envoie le .xrs.
18. Champ « afficher les numéros » des broches (U3, U4) : idem, décoché sur U3.
19. Type de conducteur PROFINET à créer (Préférences / Conducteurs).
20. Numéros de fil générés : reconnus par WinRelais comme numéros ou comme texte libre ? Messages du Journal à l'ouverture ?
21. Symbole Hager NFT702 : créé par copie du NFT706 dans `outils/librairie/CUSTOM/`, pas dans la librairie WinRelais du PC. À copier dans `sym_electrotech\CUSTOM` si Julien veut le poser à la main.

## Divers
22. (réglé le 29/10 : KM3 renommé KA2, contacteur auxiliaire.)
23. Câble 27G1 : répartition machine / pupitre ; repères des câbles 19G1 / 27G1 et RJ45 du pupitre.
24. Classeur Excel à mettre à jour avec le nommage du 28/10.
25. Description de cartouche obsolète du f51 « contacteurs, freins » (f51 figé ; f02, f10 corrigés en v7).
26. f21 : images des borniers à insérer par Julien. f01 : logos à insérer.
