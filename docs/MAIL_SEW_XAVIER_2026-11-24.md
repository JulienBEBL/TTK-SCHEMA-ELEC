# Mail à Xavier (SEW) : brouillon du 24/11/2026

Statut : **brouillon, non envoyé**. Texte à copier dans la messagerie. Les `[crochets]` sont à compléter par Julien (valeurs à lire sur la plaque ou la commande ; aucune n'est inventée). Questions du dépôt concernées : 10 (précision de vitesse), 1 et 2 (confirmation écrite des valeurs orales), 3, 4, 5 (voir `docs/QUESTIONS_SEW.md`).

---

**Objet :** MCX91A / DRN100LS4 : écart de vitesse à vide sans codeur, et confirmation écrite de valeurs données par téléphone

Bonjour Xavier,

Suite à notre échange téléphonique du 24/11, je vous écris pour poser mes questions par écrit et garder une trace.

**Contexte**

Nous équipons une machine de deux axes motorisés indépendants, qui tournent en sens opposés, à des vitesses réglables de 30 à 137 tr/min en sortie de réducteur. Chaque axe comprend :
- un motoréducteur SEW K39 DRN100LS4 / BE5 / TF (2,2 kW), rapport de réduction [i = ...], frein BE5 400 V CA avec redresseur BGE1.5 (plaque du 18/11), sans codeur ;
- un variateur MOVITRAC MCX91A-0055-5E3-4-T00/001/CSO/CFN/CDM/CMM, alimenté en 400 V triphasé, avec une résistance de freinage BW100-001 ;
- une consigne de vitesse envoyée par PROFINET depuis un automate Siemens S7-1200 ; le STO (X6) est commandé par un relais de sécurité.

Mode de régulation actuellement prévu : [mode : à compléter]. Le réseau du variateur est coupé par contacteur ; l'électronique reste alimentée en 24 V (X5).

**1. Question principale : écart entre consigne et vitesse réelle, à vide**

Sans codeur, moteur à vide et en régime établi, quel écart peut-on attendre entre la consigne de vitesse et la vitesse réelle de l'arbre de sortie, pour cette configuration ?

Pour que votre réponse soit utilisable, pourriez-vous préciser :
- l'écart en tr/min (et en %) à 30 tr/min, à une vitesse intermédiaire et à 137 tr/min en sortie ;
- le mode de régulation qui donne le meilleur résultat sans codeur, et les paramètres à régler (par exemple la compensation de glissement) ;
- la dispersion à prévoir entre deux ensembles identiques (nos deux axes doivent rester proches l'un de l'autre : exigence de réception ≤ 2 tr/min d'écart entre eux, à vide) ;
- l'influence de l'échauffement du moteur et de la tension réseau.

**2. Confirmation écrite de valeurs données par téléphone**

- Frein BE5 avec redresseur BGE1.5 : courant de maintien de 0,18 A. Pourriez-vous confirmer cette valeur, préciser s'il s'agit du courant côté alimentation alternative (400 V) ou côté bobine en courant continu, et si elle est donnée par frein ? Nous n'avons pas le courant d'appel (valeur et durée) : pouvez-vous nous le communiquer ? Il nous sert à choisir la courbe de déclenchement du disjoncteur de chaque frein (2 A, courbe C pour l'instant).
- Entrée STO du MCX91A : puissance absorbée de 150 mW par variateur. Pourriez-vous confirmer, et indiquer la tension à laquelle cette valeur est donnée ? Nous en déduisons environ 6,25 mA par variateur sous 24 V, soit 12,5 mA pour les deux en chaîne.

**3. Autres points, si vous avez l'information**

- Courant réseau du MCX91A-0055-5E3 (nominal, appel à la mise sous tension, précharge) et protection amont recommandée. Nous avons prévu un disjoncteur-moteur réglable de 6 à 10 A par variateur.
- Entrée sonde TF (X10) : bornes exactes sur le MCX91A, paramètre du type de sonde, réaction et réarmement au déclenchement.
- Consommation 24 V de l'électronique (X5) pour cette variante (CSO / CFN / CDM / CMM).

Une réponse écrite, même brève, nous suffit. Merci d'avance pour votre aide.

Cordialement,

[Prénom Nom]
[Société] · [téléphone]

---

## Notes pour Julien (ne pas envoyer)

- Le rapport de réduction, le mode de régulation et la signature sont à compléter ; ils ne sont pas dans le dépôt.
- Exigence « ≤ 2 tr/min » : dans le dépôt c'est l'écart **entre les deux moteurs à vide** (recette) ; le mail ne la présente pas comme une exigence sur l'écart consigne / réel.
- « Résistance BW100-001 », « S7-1200 » : repris du dépôt (`memoire/02_MATERIEL.md`) ; à retirer si tu veux un mail plus court.
- Pas de nom de client, pas de nom de machine (décision du 24/11).
- Questions non reprises (à garder pour plus tard) : 7, 8 (frein), 9 (BW100), 11 (perte de bus), 12 (mises sous tension), 13 (US 60 Hz), 14 (rotation manuelle), 16 (références).
