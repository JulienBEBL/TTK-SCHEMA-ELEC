# cablage/ : vérité terrain des câbles et des bornes

Décision de Julien (17/11/2026) : la vérité est fixée ici, **indépendamment du schéma**. Le schéma (`outils/ttk_schema.py`) est ensuite corrigé pour la suivre.

- `TTK_CABLES.xlsx` : classeur de référence (Excel ; importable dans Google Sheets). Onglets : Lisez-moi, Stock câbles, Liaisons.
- `REFERENTIEL_CABLE.html` et `REFERENTIEL_COMPOSANT.html` : les deux aperçus validés par Julien le 17/11 (pages autonomes, ouvrir dans un navigateur). Même contenu que les onglets Conducteurs et Composants.
- Onglet « Boîte machine » : bornier proposé pour +BJM (un rail DIN côté machine).
- Portée : seulement les câbles qui sortent de l'armoire. Principe : on ne commande plus rien, sauf urgence.
- « ? » = inconnu. Colonne « Validé » = oui quand Julien a vérifié la ligne.
- Un onglet validé est exporté en CSV dans ce dossier (lisible par l'assistant et par git).
- Détail de la méthode : `memoire/09_STOCK.md`.
