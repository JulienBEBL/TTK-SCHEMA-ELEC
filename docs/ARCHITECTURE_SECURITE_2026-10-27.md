# Architecture de sécurité TTK (fiche de Julien du 27/10/2026) : écarts et traitement

Fiche source : direction souhaitée par Julien, non absolue (message du 27/10). Appliquée dans `schema/generes/TTK_2026-10-27_v2.xrs` (f40 à f43).

| Fiche | Schéma v2 | Statut |
|---|---|---|
| K1 / K2 | -KM1 / -KM2 (exception R8) | conforme |
| KF1 / KF2 | -Q421 / -Q422 | conforme |
| Q48 | -Q423 | conforme |
| Ordre automate | contact -K511, bobine sur f51 (Q0.7) | référence à choisir |
| Sortie 1 -> KF1, KF2 + Manu-D -> Q48 | 13-14 -> -Q421, -Q422 ; 83-84 (Manu-D) -> -Q423 | conforme |
| Sortie 2 -> Auto-A -> ordre -> K1, K2 | 23-24 -> 13-14 (Auto-A) -> -K511 -> -KM1, -KM2 | conforme |
| Sortie 3 -> Auto-B -> STO x2 | 33-34 -> 23-24 (Auto-B) -> X6 des 2 MCX91A | conforme |
| Auto-C / Manu-C -> DI | 33-34 -> I0.4 ; 73-74 -> I0.5 | conforme |
| Manu-A / Manu-B shunt capot | 53-54 voie 1, 63-64 voie 2 | conforme |
| Diagnostic statique -> automate | I1.5 réservée, borne absente du symbole | à compléter (notice + chat symboles) |
| EDM : NF miroir K1 K2 KF1 KF2 Q48 | boucle Y1-Y2 + -S414 (f40) | conforme |

Écarts relevés entre la fiche et le reste du projet :
1. 48 V : la base de session disait « -Q423 coupé par l'AU », le schéma v1 l'alimentait en Auto et en Manu. La fiche impose Manu seulement : appliqué.
2. Capot magnétique : la décision dit « non codé », le symbole posé est `ifm_MN508S_capteur_magnetique_code` (capteur codé). Quel produit est commandé ?
3. Sélecteur sans clé ni cadenas : en Manu, le capot est shunté. L'IEC 60204-1 (sélection des modes) demande alors un moyen de sélection protégé (clé, code). Choix client : inscrit au folio 43 en risque résiduel.
