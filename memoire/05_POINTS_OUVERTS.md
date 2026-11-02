# 05 · Points ouverts et valeurs à vérifier

Ne jamais inventer de valeur : tant qu'un point est ici, le schéma porte la valeur provisoire ou rien.
Ces points étaient dans les notes encadrées des folios jusqu'à la v6 ; ils sont maintenant **uniquement ici**.

## Questions à Julien
| # | Sujet | État |
|---|---|---|
| Q8 | Retours sur la v9 | en attente |
| Q9 | Ordre interne du bloc sécurité | réglé le 30/10 : retour à l'ordre d'origine, f40 relais, f41 entrées, f42 sorties |
| Q10 | X12 (répartiteur) et X13 (barrette de terre) hors nomenclature WinRelais (non dessinés) | réglé le 29/10 : Julien les ajoute lui-même à la nomenclature |
| Q11 | Noms de broches | réglé le 02/11 : au cas par cas, à la demande de Julien |
| Q12 | f31 / f32 : l'image du défaut d'affichage des câbles n'est pas arrivée (reçu : f20, f23, f50). Corrigé par calcul ; à confirmer à l'écran | à vérifier |
| Q13 | f52 : mention rouge « PROPOSITION A VALIDER » conservée (Julien l'a retirée aux f50 et f51 seulement) | à confirmer |
| Q14 | W1 au f20 | réglé le 02/11 : on le garde |
| Q15 | Notes du .xrs du 02/11 | réglé : f41 barres retirées ; f53 bornes TC posées (type à définir) ; f25 « borniers sur la page alims » **en pause** |
| Q16 | f24 « Pour simplifier le » | réglé : rien à ajouter |
| Q17 | **Plan de folios et repérage des borniers** (`docs/PROPOSITION_FOLIOS_BORNIERS_2026-11-02.md`) | à valider ; test WinRelais d'un repère à 2 points avant renommage |
| Q18 | Prise de service X14 → -XD1 (IEC 81346-2) ? | à confirmer |
| Q19 | Référence des bornes thermocouple (f53) | à définir à l'achat |

## Sécurité
1. Sortie de diagnostic statique du XPSUAF13AP : borne à lire sur la notice, à ajouter au symbole, puis câbler sur I1.5. B2 et Z1 non raccordées : à confirmer.
2. Charge de la sortie 13-14 (3 bobines LC1D09BD) à comparer aux 3 A en DC-13 de la notice.
3. Antiparasites des bobines LC1D09BD : pas de diode simple sur KF1 / KF2 (retard de serrage des freins) ; varistance ou RC. Module intégré ?
4. Sélecteur Eaton : photo de la plaque (numérotation réelle) ; recouvrement Auto / Manu à la continuité ; courant minimal des contacts sous 24 V.
5. ifm MN508S : homologation sécurité (EN 60947-5-3 / ISO 14119) ; actionneur codé commandé ? ; brochage M12 8 broches ; câble M12.
6. AU XB5AS8442 : ZBE101 / ZBE102 NO ou NF ?
7. Fins de course : symbole « NF » (11-12) à poser, le symbole actuel est un NO.

## Puissance et variateurs
8. Courant du frein BE5 → calibre et courbe de QF2 / QF3 ; section du câble frein (appel SEW).
9. Bornes X6 (STO) et X10 (TF) du MCX91A (notice SEW).
10. Nombre de mises sous tension par heure du MCX91A (KM1 / KM2 ne servent pas d'arrêt de service).
11. Câbles frein 2G1,5 et TF 2G1 blindé : à commander, longueurs à définir.

## Très basse tension
12. DC-1 du LC1D09BD sous 48 V (KA2).
13. Polarité de l'entrée ENA du DM860H.

## Automate
14. Liste d'E/S à valider (f50 à f52 figés d'ici là).
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
26. f25 : images des borniers à insérer par Julien. f01 : logos à insérer.
