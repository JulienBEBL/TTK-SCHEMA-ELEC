# 06 · Travail en cours (version actuelle et suite)

## Version actuelle : v43 (26/11/2026, PC PERSO JULIEN)
`schema/generes/release/TTK_2026-11-26_v43.xrs` : tous contrôles à 0. v42 dans old/ ; v42 retouchée par Julien archivée (`schema/recus/2026-11-26_v42_ouverte_WinRelais.xrs`).
Rapport : `docs/RAPPORT_v43_2026-11-26.md`.
- Retouches de Julien reprises : W1 (f10, textes à droite sans ovale), W9 / W10 (f20, câble 200 plus bas, composition, ellipse, brin 4 sur le V/J, texte « V/J non raccordé »).
- f40 : textes des contacts accrochés à gauche (Julien s'était trompé en v42). Variateur f31 / f32 : OK (Julien).
- Plans de bornier : résumé sous le cadre du repère du bornier. Nomenclature : police 300 (280).
- Brin V/J de W9 / W10 : n° 4 **non voulu** (Julien 26/11) : `vj_num=4` retiré du script (essai : seul changement, 2 brins ; contrôles à 0). Sortira avec la v44, après les autres retours v43.
- Bornes de terre (6 dessinées / 4 achetées) : point abandonné (Julien 26/11) ; plus signalé par la nomenclature.
- Suite : Julien envoie les réponses de SEW au prochain message.
- 26/11 (nouveau chat, passation) : mémoire relue, release v43 non réenregistrée ; attente des retours de Julien sur la v43.

## Version précédente : v42 (26/11/2026, PC PERSO JULIEN)
`schema/generes/release/TTK_2026-11-26_v42.xrs` : 31 folios, 254 symboles, 708 fils, 93 renvois, 407 numéros ; tous contrôles à 0 (verifier : 28 attentions connues ; contrôle élargi v42 : corps des symboles, noms de broches, points de connexion). v41 dans old/ (ouverte dans WinRelais, sans retouche : `schema/recus/2026-11-25_v41_ouverte_WinRelais.xrs`).
Rapport : `docs/RAPPORT_v42_2026-11-26.md`. Demandes : `memoire/revues/2026-11-26_retours_julien_v41.md` (faites).

### Fait en v42 (retours de Julien sur la v41, 26/11)
| Folio | Changement |
|---|---|
| 01 | « Affaire » retiré |
| 10 | W1 / 5G4 à droite du câble (`droite=True`) ; repère QS1 décalé |
| 20 | Retour 0 V à 800 sous ENA- ; bornes +BJM à 400 ; cadre +M avec les broches ; numéros entre les cadres ; texte KA2 centré |
| 31, 32 | Variateur élargi (pas de 600, CUSTOM, 3 copies) ; résistance sous -R ; sonde TF et textes à droite |
| 40 | Textes des contacts à droite, accrochés à droite ; « contact miroir » à gauche ; renvois du bas de KA1 800 plus bas ; noms de broches de KA1 masqués (doublon) |
| 64 | Thermocouple retourné (CUSTOM `Thermocouple_bas.xsy`) |
| tous | Numéros centrés sur la longueur du tronçon (`centre_troncon`) ; cadres de lieu avec broches et noms de broches |
| 70-73 | Rayé vert / jaune en bandes de 100 ; câble et n° de fil en gras ; résumé des fonctions sous chaque bornier |
| 80, 92 | Folios et origines des câbles relus sur le dessin (W8, W11, W12, W14 corrigés) |

### Suite
- Julien : relire la v42 dans WinRelais (f31 / f32, f40, f64, plans de bornier).
- `implantation/generateur/saisie.json` : folios et origines de W8, W11, W12, W14 corrigés le 26/11 (accord de Julien) ; v42 régénérée (seul le f80 change). Implantation à régénérer pour en tenir compte.
- Implantation à régénérer ; freins (D17) ; TIA ; SEW (réponses écrites reçues, à reporter).

## Historique
Versions v17 à v41, feuilles de route et bilans du 05/11 au 25/11 : `docs/HISTORIQUE_VERSIONS.md` (déplacé le 26/11, demande de Julien). Chaque version a aussi son rapport `docs/RAPPORT_vNN_*.md`.
