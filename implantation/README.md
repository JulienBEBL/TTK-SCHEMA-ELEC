# Implantation de l'armoire +A1 (draw.io)

Dossier de l'agent qui dessine l'implantation de l'armoire sous draw.io. Consignes complètes : `docs/PROMPT_AGENT_IMPLANTATION_2026-11-04.md`.

| Dossier / fichier | Contenu |
|---|---|
| `release/` | La dernière version seule : `TTK_implantation_AAAA-MM-JJ_vN.drawio` + export `.pdf` |
| `old/` | Toutes les versions précédentes |
| `JOURNAL.md` | Une entrée par version : date, changements, questions, réponses de Julien |

Règles :
- Seul l'agent d'implantation modifie ce dossier ; il ne touche à rien d'autre dans le dépôt.
- `git pull --rebase` avant chaque `git push`, jamais de `--force`.
- Les repères suivent la nomenclature du schéma (`schema/generes/release/*_nomenclature.csv`).
