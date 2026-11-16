# 04 · Règles de dessin (demandes de Julien)

À appliquer sur **tous les folios**, à chaque version. Date = date de la demande.

## Ordre et numéros des folios (v12, 02/11, plan validé par Julien)
**Une dizaine par famille**, numéros qui se suivent dans la famille, trous entre familles pour ajouter des folios.
Le script garde les **anciens numéros en interne** (clés de `F`, textes « fNN ») ; le dict `NUMFOL` de `ttk_schema.py` donne le numéro affiché et `ren()` traduit les « fNN » des textes. **Dans le script, écrire toujours le numéro interne.** Dans `memoire/`, les numéros sont les numéros affichés.

| Affiché (v12) | Interne (script) | Contenu |
|---|---|---|
| 01, 02, 03 | 01, 02, 04 | garde, sommaire, synoptique en logigramme (légende supprimée le 02/11) |
| 10 | 10 | arrivée, QS1, QF1, peigne de terre, variante USA |
| 11 | 12 | distribution 400 V (bus) |
| 12 | 13 + 30 | 230 V alimentations : QF4 / QF5 → T1 / T2, QF6 → T3 48 V, H2, PELV |
| 13 | 14 | 230 V services : QF7 à QF10, prise XD1, EL1 / EL2, EV1 / EV2 |
| 20 | 32 | 48 V : 4 arrivées de T3, KA2 (2 pôles), drivers, bornier, moteurs pas-à-pas |
| 21 | 31 | distribution 24 V : X21.11 à X21.13, voyant H3 |
| 30 | 54 | switch PROFINET |
| 31, 32 | 20, 21 | variateurs U1, U2, bornier, moteurs M1, M2 |
| 40, 41, 42 | 40, 41, 42 | sécurité : relais KA1, entrées, sorties |
| 50 | 60 | pupitre (IHM) |
| 60, 61, 62, 63 | 50, 51, 52, 53 | automate : CPU entrées, sorties, SM 1223, SM 1231 TC |
| 70, 71 | 70, 71 | borniers : groupes vers machine / réseau (70), tableau des bornes pupitre (71) |
| 80, 85, 90 | idem | câbles, implantation, nomenclature |

Supprimés (anciens numéros) : f11 (répartiteur et barrette de terre : pas de symbole, 29/10), f30 (fondu dans l'actuel f12), f43, f03 légende (02/11).
Le sommaire (f02) est généré à partir de cette liste : Julien veut qu'il soit tenu à jour à chaque version.

## Mise en page
1. **Aucune note encadrée** sur les folios (29/10). Les points à vérifier vont dans `05_POINTS_OUVERTS.md`.
2. **Contenu centré** dans le cadre de chaque folio (23/10, redemandé le 29/10 pour f12) : `g.centrer` automatique. Exception (30/10) : bus, barres et variateurs restent **en haut, à la même hauteur d'un folio à l'autre**, centrés en largeur seulement (`HAUT` dans le script : f11, f12, f13, f21, f30, f31, f32, f40 à f42, f50, f60 à f63). Modèle : le f12.
3. **Aucun texte qui se superpose** (23/10) : textes, étiquettes de câble, renvois. Le bloc d'information d'un composant peut être déplacé indépendamment du symbole (`fpos`).
4. **Pas de pastille d'état** : le carré de couleur en haut des folios est supprimé (30/10).
5. **Rendu propre « comme un vrai schéma »** (29/10) : pas de longs fils qui font le tour du folio, pas de croisements inutiles. Appareils en parallèle : l'un sous l'autre (EL1 / EL2, EV1 / EV2 au f13). Les piquages d'un bus croisent les autres lignes du bus : normal.
6. Un folio trop chargé se **sépare en deux** (29/10 : f13 → alimentations + services). Un folio inutile se supprime.
7. **Fils assez longs** entre deux appareils (au moins 1600 à 2400) pour que le numéro de fil soit lisible (29/10, f12 / f13). Appareils d'une même chaîne **dans l'axe** (QF9 → QF10 → X14).
8. Arrivée réseau : texte « ARRIVEE RESEAU ... » **dans un cadre** (29/10, f10). Fils de la chaîne X11 → QS1 → QF1 → renvois **longs** (numérotation future) ; peigne de terre en bas, renvois à droite de la chaîne, flèches vers le haut (02/11).
8 bis. **Barres 24 V / 0 V seulement sur les folios qui s'y piquent** (02/11 : retirées du f41).

## Couleurs des conducteurs (02/11, IEC 60204-1 13.2.4, vérifiées à la demande de Julien)
| Fonction | Fil réel | Type dans le script (couleur affichée) |
|---|---|---|
| Puissance CA 400 / 230 V (phases, frein) | noir | `L` Puissance (noir) |
| Neutre | bleu clair (réservé au neutre) | `N` (bleu clair) |
| Terre | vert-jaune | `PE` |
| Puissance CC : 48 V drivers (+ et -), phases pas-à-pas, résistance de freinage | noir | `PDC` Autre tension DC (noir) |
| Commande CC +24 V (sécurité, STO, sonde TF, E/S) | bleu foncé | `24` Commande 24VDC (bleu foncé) |
| 0 V commande | bleu foncé / blanc (usage courant) | `0V` (bleu) |
| Thermocouple type K | vert (+) / blanc (-) (IEC 60584-3) | `TC` (vert) |
| PROFINET | câble vert | `PN` (vert) |

Orange = circuits exceptés (encore sous tension QS1 ouvert) : **aucun sur TTK**, donc plus d'orange (avant v13 : 48 V, résistance, thermocouple en orange). Rouge = commande en alternatif : aucune.

## Retouches de Julien dans WinRelais (02/11)
- **Toujours comparer le .xrs réenregistré par Julien à la version générée** (section par section, symboles par repère, textes par contenu) et reprendre ses déplacements dans le script (demande du 02/11 : « regarde le .xrs actuel pour vérifier ou comparer »).
- Reprises : `POS_JULIEN` (textes déplacés, coordonnées finales, appliqué après le centrage) et déplacement des tableaux des f61 / f62 près des modules (fin du script). Si le folio change de contenu, vérifier que ces positions tombent encore juste.
- Nom d'un module (repère) **tout près de son cadre**, détails empilés proprement dessous (f61 / f62, 02/11).
- f10 : cadre « ARRIVEE RESEAU » **en pointillé** (02/11).
- Câbles en ovale : composition sous l'ovale, abscisse relative au 1er brin (`compo_dx`) : moteur -2300, sonde TF -1600, frein -1200 (f31, f32), pas-à-pas -2000 (f20). Au f20 : bornes 800 sous le driver, câble à mi-chemin entre les bornes et le moteur.
- Contrôle des chevauchements : largeur des textes estimée avec la chasse Arial (`xrs_gen.largeur`, mesurée sur ses copies d'écran) ; la mise en page garde 0,55 par caractère.

## Bornes de terre (04/11)
Bornes de terre vert/jaune (achetées) : X10.11 (PE arrivée), X31.11 / X32.11 (PE moteurs), X50.13 (FE IHM). Symbole `librairie/CUSTOM/Borne_4mm_terre_vert-jaune.xsy` : même géométrie que la borne 4 mm, trait vert épais comme la Borne_PE de la librairie ; liste `BORNES_PE` du script. La revue des achats écrivait X10.15 : c'est L3, la borne PE de l'arrivée est X10.11.

## Composants
9. Affichage : **fonction + caractéristiques** seulement. Marque et référence (champ 3) **masquées** sur tous les composants sauf les borniers (29/10) ; la donnée reste dans le symbole (nomenclature). Fait dans `_place_ren` (`shown=(2, 4)` par défaut).
9 bis. **Noms de broches** (30/10) : case WinRelais = champ 5 de la 2e ligne de `Autre` du symbole (1 = affichés, 0 = masqués). Dans le script : `noms=True / False` à la pose. **Règle de Julien (02/11) : on ne masque pas par principe, cas par cas quand il le demande.** Masqués : TR1 (f10), U3, U4, M3, M4 (f20), M1, M2 (f31, f32, demande du 02/11).
10. Repérage : lettres de fonction + n° d'ordre, sens de l'énergie (28/10, `docs/NOMMAGE_2026-10-28.md`). Maître = référence fabricant ; esclaves = même repère, sans référence. Contacteur utilisé comme relais / contacteur auxiliaire = **KA** (KA2, 29/10), même si la référence est celle d'un contacteur moteur.

## Synoptique (f03, 02/11)
Logigramme : blocs encadrés (titre en gras + 1 à 3 lignes, n° de folio dans le titre), flèches dans le sens de l'énergie, PROFINET en pointillés, variante USA en pointillés. Pas de note en bas. Un texte plus large que son cadre arrête le script.

## Disposition d'une rangée de contacts (f60, alignement de Julien du 30/10)
Modèle à reprendre pour les folios d'E/S (`entree()` dans le script, coordonnées du fichier) :
- Pas entre colonnes : **800**. Trop étroit pour les textes à côté des contacts : d'où 2 niveaux en quinconce.
- **Bornes alignées sur 2 lignes** : haut y = 4400, bas y = 11200, quelle que soit la colonne.
- **Contacts sur 2 niveaux** : haut y = 5600, bas y = 8000, en alternance d'une colonne à l'autre (un repère ne touche jamais celui du voisin).
- Écarts verticaux : collecteur 24 V → borne 400 ; borne 400 de haut ; borne → contact haut 800 ; contact 1600 ; contact haut → contact bas 800 ; contact bas → borne du bas 1600 ; borne du bas → broche automate 1200.
- Une colonne sans borne (KM1, KM2, KA2) garde les mêmes niveaux de contact.
Julien a laissé S1 et S2 un peu décalés dans son fichier ; le script les aligne sur les mêmes niveaux.

## Repérage des bornes (02/11, règle de Julien)
**X + n° du folio où la borne est dessinée + « . » + n° de borne**, une **dizaine par fonction** : X31.11 à X31.14 moteur M1, X31.21 / X31.22 sonde TF, X31.31 / X31.32 frein. Un seul point : WinRelais refuse X31.1.1 (« Erreur d'analyse », séparateur « . »). Liste dans `GROUPES` (script) ; la prise de service est **XD1** (IEC 81346-2). Blocs de distribution 24 V : X21.11 (24VELEC), X21.12 (0 V), X21.13 (24VSEC).

## Borniers vers l'extérieur (02/11)
Tout appareil hors armoire (+M, +P1) passe par un bornier. Bornes sur une ligne, dans l'axe des broches de l'appareil ; broches espacées de 400 → bornes sur 2 niveaux en quinconce, repère à gauche en haut, à droite en bas (f20). Câble entre la borne et l'appareil.

## Câbles variateur (f31, f32, 30/10)
Présentation de Julien (f32, 02/11) : trait du 1er au dernier brin, repère dans un ovale à gauche, composition dessous à gauche, désignation gardée mais masquée (`g.cable(..., ovale=True)`). Câbles numérotés de gauche à droite : moteur, sonde TF, frein (W2 W3 W4, W5 W6 W7).
Moteur dans l'axe de X2 (fils droits, plus d'escalier). Depuis le 02/11 : X2 → bornier (y = 12800) → câble → moteur. Les 3 câbles W sur **une seule ligne**, textes à côté de leur câble, sans chevauchement. Frein sans croisement.

## Renvois
11. Le texte de description d'un renvoi est **bien placé** (centré sur le renvoi ou le groupe de renvois) (23/10).
12. Le renvoi ne doit **jamais** être dessiné sur le fil : flèche du côté opposé au fil (codes A/B, voir `07_METHODE_TRAVAIL.md`).
13. Distribution de puissance (29/10) : **bus tétra L1 L2 L3 N** en haut des folios f11, f12, f13, enchaîné par renvois, chaque appareil se pique sur ses phases [D]. Points de jonction acceptés sur un bus.

## Potentiels de commande
14. **Barres 24VELEC et 0 V en haut** du folio (24 V au-dessus, 0 V dessous), « comme dans tous les schémas » (29/10), sur tous les folios de commande. Un piquage 24 V croise la barre 0 V : normal. Un appareil dont le 0 V est en bas remonte par un collecteur sur le côté.
15. Distribution TBT : **un fil par appareil** depuis le bornier de distribution, sans point de dérivation (28/10). Croisement sans jonction accepté.
16. **24VSEC** (T1, X33) et **24VELEC** (T2, X31), 0 V, +48 V / 0 V 48 (29/10).

## Fils
17. **Numéros de fil** : les fils de puissance portent le nom de leur potentiel, **L1, L2, L3, N, PE** (et U, V, W en sortie de variateur), sur **chaque tronçon**, même court (28/10, précisé le 29/10). PE nommé sur les folios de puissance (pas les FE de l'automate / IHM). Les autres fils ne sont pas numérotés tant que le schéma n'est pas fini.
18. Numéros **alignés et centrés** (29/10, « carré et propre ») : noms des fils parallèles voisins sur une même ligne ; nom d'un bus près de son extrémité gauche, aligné sur les autres lignes du bus. **Jamais sur le numéro de brin d'un câble** (30/10, f10) : WinRelais écrit le brin juste au-dessus du croisement, le nom du fil reste au moins 400 au-dessus ou 100 en dessous.
19. **Terre, règle C partout** (29/10) : pas de PE qui descend en bas du folio. Chaque appareil : **fil PE court + renvoi** vers la terre de l'arrivée (f10), où le PE de X11 se divise en un départ par appareil. Moteur : PE → X2 PE du variateur, puis X1 PE du variateur en renvoi court.
20. Types de conducteur : `Puissance` (phases), `Neutre Puissance`, `Conducteur terre` (PE), `Commande 24VDC`, `0V`, `Autre tension DC` (48 V, TF ; PROFINET provisoire). Jamais `Commande 24V~` sur un circuit continu.

## Textes
21. Phase de chaque départ 230 V : visible par le piquage sur le bus et le numéro de fil (les petits textes « L1 / L2 / L3 » du 23/10 sont retirés en v8).
22. Borniers f70 / f71 : provenance du fil écrite **des deux côtés** de la borne (23/10).
23. Folio PROFINET : texte sur chaque fil indiquant le composant de destination (23/10).

## Numérotation des fils (convention v2, retenue par Julien le 05/11)
Julien : chiffres seuls (stock de repères presque sans lettres). Ses collègues : numéroter **aussi** les phases, le neutre, le 24 V et le 0 V (dépannage). Remplace la convention A du 28/10 (phases nommées L1 / L2 / L3 / N) et la v1 du 05/11 (potentiels fixes 0 / 24 / 25 / 48 / 49).
1. **Tout fil porte un numéro**, puissance comprise. Seul le PE reste repéré par sa couleur vert/jaune (à confirmer par Julien).
2. **Un numéro par potentiel** : il change à chaque appareil traversé (sectionneur, disjoncteur, contacteur, fusible, contact, transformateur, alimentation) ; une borne ou un bloc de distribution ne le change pas (le fil côté machine garde le numéro de l'armoire).
3. **Format FFNN** : FF = folio (affiché) où naît le potentiel ; NN par dizaine = un appareil, **chiffre des unités = conducteur** : 1 L1, 2 L2, 3 L3, 4 N ; sorties moteur 1 U, 2 V, 3 W ; continu 1 = +, 0 = 0 V. Commande : NN dans l'ordre gauche → droite, haut → bas.
4. Exemples (numéros indicatifs, la génération fixera les vrais) : arrivée X10 → QS1 = 1001 / 1002 / 1003 / 1004 ; QS1 → QF1 = 1011-1014 ; QF1 → XR1 / XR2 → bus f11 = 1021-1024 ; QM1 → KM1 = 1101-1103 ; KM1 → U1 = 1111-1113 ; U1 → X31.12-14 → M1 = 3101 / 3102 / 3103 ; QF5 → T2 = 1211 / 1214 ; +24VELEC (T2 → X21.11 → appareils) = 1221 ; +24VSEC (T1 → X21.13 → FA1, K2) = 1231 ; 0 V commun = 1220 ; +48 V (T3 → KA2) = 1241, 0 V 48 = 1240 ; FA1 → KA1 13/23/33 = 4001 ; KA1 14 → KF1 / KF2 / X42.11 → S3 15 = 4002 ; S3 16 → X42.12 → KA2 = 4201 ; L+ capteurs CPU = 6001 ; B3 → X60.32 → I0.6 = 6002 ; Q8.0 → X61.11 → H1 rouge = 6201.
5. **Sans point** : 1013, pas 10.13 [D 05/11, Julien] (confusion avec les bornes X41.11, point absent du stock en 2,5 et 4 mm²).
6. **Quand** : la numérotation se fait **à la toute fin**, après la validation par Julien de la sécurité, de l'automate et des borniers (05/11).
Méthode prévue (script) : potentiels calculés à partir des fils générés (union des extrémités, passage à travers les bornes et les blocs de distribution, renvois entre folios), folio de naissance = folio de la source, unité = conducteur ; écriture dans `¤#Numero` au format relevé le 28/10 (`x·y·texte·folio·0·Arial·300·angle·8388608·0·0·0·`), un numéro par tronçon, au milieu du segment, loin des brins de câble (07).

## Montage (règles de Julien, 05/11)
- Une butée d'arrêt de chaque côté de chaque appareil sur tous les rails DIN.
- Bornes de la porte de l'armoire sur le rail R4.

## Folio 70 (09/11)
- Les borniers y sont rangés **comme en vrai** : une ligne par rail / tronçon, dans l'ordre de l'implantation (agent draw.io, `implantation/JOURNAL.md`), rail indiqué dans le titre de ligne. Si l'implantation change l'ordre, mettre à jour `RAILS_X70`.

## Images (09/11)
- Les images (logos f01) sont dans `schema/images/` et écrites par le script dans la section `¤#Logo¤` : `x·y·largeur·hauteur·chemin absolu·1·ratio de l'image x 1000·index du folio·0·`. Le chemin est absolu : il est recalculé à chaque génération depuis le dépôt.

## Numérotation des fils : mise en application (13/11, v25)
- Julien a reçu des repères pour le 4 mm². Numérotation appliquée **folio par folio**, f10 d'abord (v25), à sa demande, avant la validation complète de l'automate et des borniers.
- Script : `numero_fil()` et `ETAGES_F10` dans `ttk_schema.py` (appareil amont du tronçon → dizaine ; phase → unité). Les autres folios gardent L1 / L2 / L3 / N tant qu'ils ne sont pas faits.
- f10 (v25) : arrivée (câble client W1, bornes X10, entrée QS1) **1001 L1, 1002 L2, 1003 L3, 1004 N** ; QS1 → QF1 **1011-1014** ; QF1 → XR1 / XR2 → bus f11 **1021-1024** ; variante USA : primaire TR1 **1031-1033**, secondaire **1041-1044**. PE : « PE » (vert/jaune, pas de numéro).
- Suite : le potentiel 1021-1024 continue sur le bus du f11 : à numéroter avec le f11 (aujourd'hui L1 / L2 / L3 / N).

## Numérotation f11 à f13 (13/11, v26)
- Script : table `SOURCES_NUM` (folio, appareil, broches de sortie, dizaine) et `numeros_potentiels()` ; un potentiel garde son numéro à travers bornes et blocs PTFIX et d'un folio à l'autre ; `NUMEROTES` = folios déjà faits. Alertes affichées à la génération (« ATTENTION numérotation »).
- Dizaines dans l'ordre de lecture du folio (gauche → droite, puis ligne suivante).
- f11 : QM1 1101-1103, QM2 1111-1113, QF2 1121 / 1122, QF3 1131 / 1133, KM1 → U1 1141-1143, KM2 → U2 1151-1153, KF1 → frein M1 1161 / 1162, KF2 → frein M2 1171 / 1173. Bus : 1021-1023 (de QF1).
- f12 : QF4 → T1 1201 / 1204, QF5 → T2 1211 / 1214, QF6 → T3 1222 / 1224 ; T1 24VSEC 1231, 0 V commun (T1 + T2) 1230, T2 24VELEC 1241, T3 +48 V 1251, 0 V 48 1250. H2 sur le bus : 1023 / 1024.
- f13 : QF8 → EL1 / EL2 1303 / 1304, QF7 → EV1 / EV2 1313 / 1314, QF9 → QF10 1323 / 1324, QF10 → XD1 1333 / 1334. Bus : 1023 / 1024.
- Ces potentiels continuent sur des folios pas encore numérotés (f20, f21, f31, f32, f40...) : ils y gardent L1 / L2 / L3 ou rien, jusqu'à leur tour.
- Placement : un numéro horizontal reste entier sur son fil (13/11) ; les étiquettes PE ne s'alignent plus avec les numéros.

## Câbles (13/11)
- Jamais de câble de longueur nulle (début = fin, ovale sur un seul brin) : rendu faux et export PDF qui déborde sur toute la page (W13, v25). Câble d'un seul conducteur : trait de 800 centré sur le fil, textes à droite.
- f10 : arrivée aérée (bornes X10 à 4400, câble client juste sous le cadre, numéros de fil sous le câble) (Julien, v25 trop serré).
- f21 : image du bornier PTFIX 6/12 (`schema/images/Phoenix_PTFIX_6-12x2.5.jpg`, fournie par Julien) dans chacun des 3 cadres, sans texte. Les images suivent maintenant le centrage du folio (`decaler`).

## Numérotation : comment la poser en vrai (expliqué à Julien le 13/11)
- Un numéro = un potentiel, pas un fil : tous les fils de ce potentiel portent le même numéro, un repère à chaque bout.
- 1021 / 1022 / 1023 / 1024 : QF1 → XR1, pont XR1 → XR2, et chaque départ de XR1 / XR2 vers un appareil (L1 1021 : QM1, QM2, QF2, QF3, QF4, QF5 ; L2 1022 : QM1, QM2, QF2, QF6 ; L3 1023 : QM1, QM2, QF3, QF7, QF8, QF9, H2 ; N 1024 : QF4, QF5, QF6, QF7, QF8, QF9, H2). Le numéro change à la sortie de l'appareil suivant (ex. QM1 → KM1 = 1101).
- 0 V commun 1230 : T1 -V → X21.12 (entrée E), T2 -V → T1 (2e borne -V) ou une sortie de X21.12, X21.12 → X12.11 (côté 0 V), et tous les départs 0 V de X21.12. Le fil X12.11 → PE est vert/jaune, sans numéro. Jamais 2 fils dans un même trou push-in sans l'accord de la notice. 24VELEC 1241 (T2 → X21.11 → départs), 24VSEC 1231 (T1 → X21.13 → départs, dont l'entrée de FA1). +48 V 1251, 0 V 48 1250.

## Numérotation f20, f21, f30 et câbles PROFINET (13/11, v27)
- f20 : KA2 pôle 1-2 → U3 +48 V **2001**, pôle 3-4 → U4 **2011** ; U3 → X20.11-14 → M3 **2021-2024**, U4 → M4 **2031-2034** (A+ 1, A- 2, B+ 3, B- 4) ; +48 V avant KA2 1251, 0 V 48 1250 ; PUL- / DIR- / ENA- au 0 V commun 1230.
- Sorties CPU vers les drivers (nées au f61, numérotées dès la v27 parce qu'elles passent au f20) : Q0.0 **6101** (PUL U3), Q0.1 6102 (DIR U3), Q0.2 6103 (PUL U4), Q0.3 6104 (DIR U4), Q0.4 6105 (ENA U3), Q0.5 6106 (ENA U4). À garder quand le f61 sera numéroté.
- f21 : 24VELEC 1241 (X21.11, H3 via X21.21), 24VSEC 1231 (X21.13), 0 V commun 1230 (X21.12, H3 via X21.22).
- f30 : switch K4 V1+ 1241, V1- 1230.
- **Câbles PROFINET : repères PN1 à PN4** (pas de numéro FFNN, Julien 13/11) : PN1 CPU K1 → switch K4 (P1), PN2 K4 P2 → U1, PN3 K4 P3 → U2, PN4 K4 P4 → IHM P1. Écrits sur chaque tronçon PROFINET, sur tous les folios (table `CABLES_PN`).
- Les 2 bornes +V (et -V) d'une alimentation T1 à T3 sont reliées en interne : même potentiel, même numéro.
- Placement : sur les folios numérotés, le numéro va sur la plus longue partie du fil libre de tout fil croisé et de tout texte de symbole (`troncon_libre`).
- **Contrôle** : `python outils/xrs_numeros.py <fichier.xrs> 10,11,12,13,20,21,30` (relit le fichier : un numéro = un potentiel, chaque tronçon numéroté, 0 V en unité 0, câbles PN). v27 : 0 problème.
- Restent à numéroter : f31, f32 (ils affichent encore L1 / L2 / L3 pour 1141-1153 et 1161-1173), f40 à f42, f50, f60 à f63.

## Réserves et revue des folios (16/11, v28)
- E/S de réserve : plus de phrase « ... : réserve » ; un trait fin le long des broches libres, deux petits retours, et « Réserve » centré (fonction `reserve()`), du côté des fils. Les tableaux gardent la ligne « réserve ».
- Titres et descriptions de tous les folios revus (tables `DESC_FOL` et `TITRES_FOL`, n° internes).
- f63 : câble W8 avec repère et composition à droite (plus sur les fils), accolade de réserve AI1 à AI7.
- f70 : textes des cases centrés à la chasse Arial (`largeur`).
- f71 : potentiels nommés justes (24VELEC, 24VSEC, 24 V capteurs) ; l'ancien libellé « +24 V sorties automate » sur X50.11 était faux.
- Numérotation : L+ capteurs **6001** (source K1 L+ capt).

## f70 agrandi (16/11, v29)
- Cases de 820 x 1000, pas 1000, butées 400, textes 250 (signal) / 200 (repère, groupe), 7 rails sur tout le folio (x 2800 à 27100, y 1300 à 18900).
