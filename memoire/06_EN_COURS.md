# 06 · Travail en cours (version actuelle et suite)

## Version actuelle : v18 (05/11/2026)
`schema/generes/release/TTK_2026-11-05_v18.xrs` : 25 folios, 177 symboles, 654 fils, 91 renvois ; 0 problème, 0 erreur au verifier, **28** attentions (27 connues + le bout libre voulu du fil vers le bâti, f10), 0 chevauchement. **En attente : retours de Julien (Q8).**

### Fait en v18
| Folio | Changement |
|---|---|
| 31, 32 | Freins M1 + M2 sur **un seul câble -W4** 5G1,5 blindé : brins 1-2 au f31, 3-4 au f32 (même repère sur les 2 folios ; paramètre `nums` de `g.cable`) ; W7 supprimé ; 3 lignes de texte sur le V/J (-XPE1, boîte de dérivation) |
| 10 | Liaison équipotentielle **-W13** (V/J 4 mm²) : départ du peigne de terre vers « Bâti machine +M » |
| 02 | Liste des câbles : -W212 retiré ; bloc « câbles -W2 à -W6 » |

## Version précédente : v17 (05/11/2026)
`schema/generes/release/TTK_2026-11-05_v17.xrs` : 25 folios, 177 symboles, 652 fils, 91 renvois ; 0 problème au contrôle interne, 0 erreur au verifier (27 attentions connues), 0 chevauchement. v16 non réenregistrée par WinRelais (rien à reprendre), passée dans old/. **En attente : retours de Julien (Q8).**
But de Julien : un schéma propre (borniers, sécurité, automate) **avant** la numérotation des fils.

### Fait en v17 — retours du 05/11
| Folio | Changement |
|---|---|
| 41, 42, 60 | Sélecteur S3 : vrais numéros Eaton (ponts retirés) et noms **AUTO-A** 1-2 (-KM1 / -KM2), **MANU-A** 3-4 (shunt capot voie 1), **AUTO-B** 5-6 (STO), **MANU-B** 7-8 (shunt voie 2), **AUTO-C** 9-10 (info Auto → I0.4), **MANU-C** 11-12 (info Manu → I0.5), **MANU-D** 15-16 (48 V, -KA2) ; AUTO-D 13-14 en réserve (non dessiné). Symboles `librairie/CUSTOM/Eaton_T0_contact_NO_*.xsy` |
| 61 | Colonne H1 par 4 bornes **X61.11-14** (RD, OG, GN, COM) ; voyant H4 par **X61.21-22** ; collecteur 0 V descendu à y = 16400 |
| 40 | Réarmement S4 par **X40.11** (avant) et **X40.12** (retour vers Y2) ; S4 descendu de 400 |
| 12 | Voyant H2 230 V par **X12.21-22** ; H2 descendu de 800 (bus N à y = 4800) |
| 21 | Voyant H3 par **X21.21-22** |
| 31, 32 | Texte rouge réduit à « TF X10 : bornes à confirmer » (X6 confirmé) |
| 60 | Fins de course B3 à B6 : désignation et tableau en NO |
Règle de Julien (05/11) pour la porte : **tous les appareils par des bornes, ou aucun**. Tous dessinés ; si le rail R5 manque de place (agent d'implantation), on les retire tous.

## À faire ensuite
1. H2 : reporter la référence du voyant 230 V quand Julien l'aura.
2. f70 / f71 : les bornes de porte (X41.5x, X60.4x) n'y figurent pas (destination « porte ») : à ajouter si Julien le veut.
3. Champs « câble blindé » et « afficher les numéros » dès réception du .xrs de test de Julien ; type de conducteur PROFINET.
4. Liste d'E/S (f60 à f62) : seulement après validation de Julien. Numérotation des fils : après le schéma propre.
5. Achats : Q28 à Q30 (raccord thermocouple, fixation sonde, câble moteur 50 m).
