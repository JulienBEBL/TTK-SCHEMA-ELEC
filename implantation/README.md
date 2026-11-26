# Implantation de l'armoire +A1

Depuis le 17/11/2026 (v11), le dossier est **généré**, tiré du schéma et d'un fichier de saisie. Depuis la v12 (18/11) : **2 pages A3** (plan de la plaque, détail des borniers) ; depuis la v14 (26/11) : **3e page**, bornier de la boîte +BJM-X1 (hors armoire, demande de Julien). Les fonctions des pages câbles / conducteurs / synoptique restent dans `generer.py`, non imprimées.

| Dossier / fichier | Contenu |
|---|---|
| `release/` | La dernière version seule : `TTK_implantation_AAAA-MM-JJ_vN.pdf` + `TTK_implantation_AAAA-MM-JJ_vN_verification.md` |
| `old/` | Versions précédentes (draw.io v1 à v10, indices A à K ; PDF v11) |
| `generateur/` | `extraire.py` (lit le .xrs de `schema/generes/release/` + `saisie.json` → `donnees.json`), `generer.py` + `svg.py` (PDF + contrôle) |
| `JOURNAL.md` | Une entrée par version |

Contexte, règles du générateur et points ouverts : `memoire/08_IMPLANTATION.md`.

Régénérer (Python sans module externe, Edge installé) :
```
cd implantation/generateur
python -I extraire.py
python -I generer.py --png <dossier temporaire>
```
Attendu dans `_verification.md` : 0 texte trop large, 0 chevauchement, 0 écart avec le .xrs. Avant de régénérer : passer l'ancien PDF dans `old/`, changer `version` / `indice` / `revisions` dans `saisie.json`.

PC Rimane (18/11) : Edge ne sort ni PDF ni PNG quand il est lancé depuis le bac à sable de l'assistant (code 13) : lancer `generer.py` hors bac à sable. `--screenshot` ne produit rien : contrôle visuel en ouvrant `build/dossier.html`.
