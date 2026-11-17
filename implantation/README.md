# Implantation de l'armoire +A1

Depuis le 17/11/2026 (v11), le dossier est **généré** : un seul PDF A3 (implantation, borniers, liste des câbles, affectation des conducteurs, synoptique), tiré du schéma et d'un fichier de saisie.

| Dossier / fichier | Contenu |
|---|---|
| `release/` | La dernière version seule : `TTK_implantation_AAAA-MM-JJ_vN.pdf` + `TTK_implantation_AAAA-MM-JJ_vN_verification.md` |
| `old/` | Versions précédentes (draw.io v1 à v10, indices A à K) |
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
