# Librairie WinRelais de Julien (symboles CUSTOM)

Copie **octet pour octet** du dossier du PC : `C:\Users\Public\Documents\Elec-CAO\sym_electrotech\CUSTOM` (42 symboles, copie du 17/11/2026), complétée par 11 symboles de `outils/librairie/CUSTOM` absents du PC : 53 en tout.
Les fichiers restent en cp1252 avec fins de ligne CRLF : `.gitattributes` empêche git de les convertir.

## Installer sur un nouveau PC
1. Installer WinRelais.
2. Cloner le dépôt.
3. Copier le dossier `librairie_winrelais\sym_electrotech\CUSTOM` dans `C:\Users\Public\Documents\Elec-CAO\sym_electrotech\` (créer `CUSTOM` s'il n'existe pas).

Commande PowerShell, lancée depuis le dossier du dépôt :
```
Copy-Item -Recurse -Force "librairie_winrelais\sym_electrotech\CUSTOM" "C:\Users\Public\Documents\Elec-CAO\sym_electrotech\"
```

## Mettre à jour après une modification d'un symbole
Copier dans l'autre sens, puis commit et push :
```
Copy-Item -Force "C:\Users\Public\Documents\Elec-CA## Les 11 symboles ajoutés depuis le script (17/11)
Ils n'étaient pas dans la librairie du PC : Borne_4mm_terre_vert-jaune, Eaton_T0_contact_NO (8 fichiers), Hager_NFT702, Phoenix_3273354_PTFIX.
Ils viennent de `outils/librairie/CUSTOM` et sont convertis au format du PC (cp1252, CRLF). Ils n'ont jamais été ouverts dans WinSymbole : à contrôler à la 1re utilisation.

## À ne pas confondre
`outils/librairie/` est une autre copie : UTF-8, reconstruite depuis un `.xrs` par `outils/reconstruire_librairie.py`. C'est celle que le script utilise.
5 symboles ne sont que sur le PC : Finder_22.32, Repartiteur_4P_125A_1entree_9departs, Schneider_A9F75202, GV2ME10, LC1D09BD_contact_aux_NO_13-14.
