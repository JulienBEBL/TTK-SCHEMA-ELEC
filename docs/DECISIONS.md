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

## 27/10/2026
- [D] Le `.xrs` est généré par script (`outils/ttk_schema.py`), Julien teste dans WinRelais et renvoie ses retours (voir `docs/GENERATION.md`).
- [D] Commutateur -S413 (Eaton T0-4-8223/E), essai de Julien : 4 contacts NO par position, 8 en tout. Affectation retenue : position 1 = Auto (13-14 STO, 23-24 ordre contacteurs, 33-34 information, 43-44 réserve), position 2 = Manu (53-54 et 63-64 pontage capot voies 1 et 2, 73-74 information, 83-84 réserve). Numérotation provisoire.
- [D] Voyants en porte : 2 minimum (tension, défaut), plus si place. Retenu : tension (-P512), défaut (-P513), réarmement lumineux bleu (-S414), plus colonne 3 couleurs (-P511).
- [D] Parafoudre non monté : entrée I1.5 libérée (réserve).
- [D] Câble 5G1,5 (LIYCY-JZ, 80 m) : réserve, plus affecté à l'IHM ni au sélecteur (remplacé par les multiconducteurs).
- [D] Symbole XB5AD25 : supprimé.
- [D] Câbles moteurs : Julien laisse le choix. Retenu : motor U/V/W, frein (2G1,5) et sonde TF (2G1 blindé) en direct armoire -> moteur, sans bornier intermédiaire (moins de connexions, CEM, blindage repris à 360°). Les bornes X701.17 à .24 disparaissent.
- [H] Appliqué sans confirmation (à valider) : Q12 / Q13 supprimés (déjà dans le script, décision du 04/10 ; remplacés par les contacts de -K401) ; liste d'E/S du 06/10 (S412 I0.0, S411 I0.1, fins de course I0.6 à I1.1, retours KM1 / KM2 / Q423 I1.2 à I1.4, I0.5 = mode Manu) ; sorties CPU Q0.0 à Q0.2 / Q0.4 à Q0.6 = PUL / DIR / ENA, Q0.7 = relais d'interface -K511 ; SM 1223 : Q8.0 à Q8.2 colonne, Q8.3 voyant réarmement, Q8.4 voyant défaut, I8.4 alarme switch.
- [H] Architecture sécurité f42 conforme au §3.5 : 13-14 STO des 2 variateurs, 23-24 + -S413 Auto + -K511 -> -KM1 / -KM2, 33-34 -> -Q421 / -Q422 / -Q423 (sans passer par -S413).

## 27/10/2026 (soir) : sécurité selon la fiche de Julien
- [D] Sorties -K401 : 13-14 freins (+ 48 V via Manu-D), 23-24 Auto-A + ordre automate -> -KM1 / -KM2, 33-34 Auto-B -> STO. Affectation 1/2/3 proposée, à valider.
- [D] 48 V pas-à-pas alimenté uniquement en Manu (Manu-D, 83-84). Remplace « -Q423 sur la sortie de sécurité en Auto et en Manu » (v1).
- [D] Contacts -S413 : Auto-A 13-14, Auto-B 23-24, Auto-C 33-34, Auto-D 43-44 (réserve), Manu-A 53-54, Manu-B 63-64, Manu-C 73-74, Manu-D 83-84 (numérotation provisoire).
- [D] Bornes -X711 : 1-6 AU, 7-8 Auto-A, 9-10 Auto-B, 11-12 Auto-C, 13-14 Manu-A, 15-16 Manu-B, 17-18 Manu-C, 19-20 Manu-D, 21-23 alimentation IHM.
- [D] Nouveau folio 43 « SECURITE - FONCTIONNEMENT » : contacts du sélecteur, états, transitions, points à vérifier, risques résiduels. Une zone de notes par folio de sécurité.
- I1.5 = diagnostic -K401 (borne à confirmer).

## 27/10/2026 (nuit)
- [C] Capot magnétique : capteur **codé** commandé (RS 0163138, lien donné par Julien). Remplace « non codé » de la base. Fabricant, référence et contacts à relever (page RS inaccessible depuis la session).
- [D par Claude, Julien ne sait pas] Sorties -K401 figées : 13-14 freins + 48 V, 23-24 -KM1 / -KM2, 33-34 STO. Raison : le STO a une sortie dédiée qui ne coupe que quelques mA, jamais de bobine, donc pas d'usure du contact par les charges inductives ; freins et 48 V ensemble car ils tombent sur le même événement. À revoir seulement si la notice XPSUAF13AP montre des sorties différentes.
- [?] -K511 (ordre automate -KM1 / -KM2) : Julien demande à quoi il sert. Proposition : le supprimer (option A), en attente de sa réponse.
- [C] Capteur capot magnétique : RS 016-3138 = ifm MN508S (série MN), 2 NO + 1 NF, M12, 24 V CC 50 mA, IP67/IP69K. Le symbole posé (ifm_MN508S) est donc la bonne référence ; ses broches (11-12 / 23-24) ne reflètent pas 2 NO + 1 NF.
- [D par Claude] Câblage -B412 : 1 NO (fermé capot fermé) en voie 2 du relais ; NF -> automate I0.3 (1 = capot ouvert, même sens que -B411 sur I0.2) ; 2e NO en réserve. Contacts à 50 mA max : uniquement entrées relais / automate.
- [?] À vérifier sur la fiche ifm : homologation sécurité (EN 60947-5-3 / EN ISO 14119, absente des données RS), actionneur codé à associer (commandé ?), brochage M12. Câble : M12 (et non M8 comme noté en base), nombre de broches et longueur à définir.
- [D] Option A : pas d'ordre automate sur -KM1 / -KM2 (-K511 supprimé, Q0.7 en réserve). -KM1 / -KM2 fermés dès que -K401 est armé en Auto ; arrêt de service par rampe + STO.
