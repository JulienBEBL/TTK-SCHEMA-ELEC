# Journal des décisions TTK (schéma électrique)

Statut : [D] décision de Julien · [C] confirmé · [H] hypothèse · [?] ouvert

## 26/10/2026
- [D] Câbles moteurs SEW : câbles **séparés** pour le frein et la sonde TF.
  - Frein BE5 (bornes 2-3) : **2G1,5**.
  - Sonde TF (1b-2b, vers X10 du variateur) : **2G1 blindé**.
  - Repères : -W202 / -W212 (frein + TF, à scinder en deux repères ou à nommer, à trancher), puis folios 20 / 21.
  - Section du frein à valider une fois le courant du BE5 connu (appel SEW).
- [D] Dépôt GitHub = référentiel du projet (schéma, outils, livrables).

## Structure du dépôt
- `schema/` : fichiers `.xrs` de travail ; `schema/recus/` : exports reçus, datés.
- `outils/` : scripts (`xrs_check.py`).
- `docs/` : décisions, base de connaissances.
- `folios/` : fiches de saisie par folio.
- `livrables/` : listes d'E/S, carnet de câblage, `macros/` WinRelaisExpert.
