# 05 · Points ouverts et valeurs à vérifier

Ne jamais inventer de valeur : tant qu'un point est ici, le schéma porte la valeur provisoire ou rien.
Ces points étaient dans les notes encadrées des folios jusqu'à la v6 ; ils sont maintenant **uniquement ici**.

## Questions à Julien (29/10)
| # | Sujet | État |
|---|---|---|
| Q1 | Représentation de la terre (f10, f13) : options A / B / C | en attente |
| Q2 | f12 en bus tri : points de jonction acceptés ici ? n° de départ du répartiteur à garder ? | en attente |
| Q3 | Nom des 24 V : T1 = 24VSEC ? nom de T2 ? | en attente |
| Q4 | Découpage du f13 en deux folios : contenu proposé | en attente |

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
12. DC-1 du LC1D09BD sous 48 V (KM3).
13. Polarité de l'entrée ENA du DM860H.

## Automate
14. Liste d'E/S à valider (f50 à f52 figés d'ici là).
15. Brochages G2 à confirmer (seuls ceux de la génération 1 ont été trouvés).
16. PTO sur Q0.0 / Q0.4 à vérifier dans TIA V21.

## WinRelais (champs du format .xrs inconnus)
17. Champ « câble blindé » (W2, W4, W5, W7) : Julien coche « blindé » sur W2, enregistre, envoie le .xrs.
18. Champ « afficher les numéros » des broches (U3, U4) : idem, décoché sur U3.
19. Type de conducteur PROFINET à créer (Préférences / Conducteurs).
20. Numéros de fil générés (v6) : reconnus par WinRelais comme numéros ou comme texte libre ? Messages du Journal à l'ouverture ?

## Divers
21. KM3 : nom à confirmer.
22. Câble 27G1 : répartition machine / pupitre ; repères des câbles 19G1 / 27G1 et RJ45 du pupitre.
23. Classeur Excel à mettre à jour avec le nommage du 28/10.
24. Descriptions de cartouche obsolètes (f02 « indices de révision », f03 « IEC 81346-2 », f10 « PARAFOUDRE », f51 « contacteurs, freins »).
25. f31 : images des borniers à insérer par Julien. f01 : logos à insérer.
