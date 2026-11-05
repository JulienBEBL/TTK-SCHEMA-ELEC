# Génération du schéma (.xrs)

Le `.xrs` est **généré par script** (décision de Julien, 27/10/2026). Boucle de travail :

1. Claude modifie `outils/ttk_schema.py` et régénère : `cd outils && python ttk_schema.py ../schema/generes/release/TTK_AAAA-MM-JJ_vN.xrs` (commandes complètes à jour : `README.md`)
2. Julien télécharge le `.xrs` (GitHub ou chat), l'ouvre dans WinRelais, lit le Journal à l'ouverture.
3. Julien renvoie ses retours (captures, texte). Claude corrige le script et régénère.

Attention : toute retouche faite à la main dans WinRelais est perdue à la régénération suivante.
Il faut donc la décrire dans les retours, ou arrêter de régénérer le jour où on passe en finition manuelle.

Entrées : `livrables/TTK_Plan_Folios_Reperes.xlsx` (repères), `schema/modele/SCHEMA_ELEC_TTK.xrs` (en-tête, cartouche),
`outils/librairie/` (symboles `.xsy`, **reconstruits** depuis le fichier du 27/10 par `reconstruire_librairie.py` ;
ils sont fidèles à ce qui est posé dans le schéma, mais ce n'est pas la librairie WinRelais d'origine).
Pour utiliser la vraie librairie : `TTK_LIB="C:\Users\Public\Documents\Elec-CAO\sym_electrotech" python ttk_schema.py ...`.

Contrôles : `python3 xrs_tool.py verifier fichier.xrs` ; aperçu approximatif d'un folio : `python3 apercu_xrs.py fichier.xrs 42 f42.png` (nécessite matplotlib).
Après ouverture dans WinRelais : lancer « Références croisées automatique » (le générateur ne les crée pas), puis numéroter les fils.
