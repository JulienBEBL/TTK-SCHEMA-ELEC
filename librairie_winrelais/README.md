# Librairie WinRelais de Julien (symboles CUSTOM)

Copie **octet pour octet** du dossier du PC : `C:\Users\Public\Documents\Elec-CAO\sym_electrotech\CUSTOM` (42 symboles, copie du 17/11/2026).
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
Copy-Item -Force "C:\Users\Public\Documents\Elec-CAO\sym_electrotech\CUSTOM\*.xsy" "librairie_winrelais\sym_electrotech\CUSTOM\"
```

## À ne pas confondre
`outils/librairie/` est une autre copie : UTF-8, reconstruite depuis un `.xrs` par `outils/reconstruire_librairie.py` et utilisée par le script.
Elle n'a pas exactement les mêmes symboles que le PC.
- Seulement dans `outils/librairie/CUSTOM` :
  - Borne_4mm_terre_vert-jaune ;
  - Eaton_T0_contact_NO (8 fichiers) ;
  - Hager_NFT702 ;
  - Phoenix_3273354_PTFIX.
- Seulement sur le PC : Finder_22.32, Repartiteur_4P_125A_1entree_9departs, Schneider_A9F75202, GV2ME10, LC1D09BD_contact_aux_NO_13-14.
