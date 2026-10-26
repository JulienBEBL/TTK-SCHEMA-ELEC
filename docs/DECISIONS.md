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
