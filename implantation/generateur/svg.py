"""Petite couche SVG (unités : mm, page A3 paysage 420 x 297) avec contrôle des textes.

Chaque texte est mesuré (chasse Arial approchée) : un texte plus large que la place
donnée (maxw) est une erreur ; les cadres des textes d'une page sont comparés deux à deux
pour trouver les chevauchements. Rien n'est corrigé en silence : les erreurs sont listées.
"""
from xml.sax.saxutils import escape

W, H = 420.0, 297.0
# chasse Arial (fraction de la hauteur de police), mesurée sur les tables de la police Arial
_CH = {}
for c in "il.,:;'!|ijlI": _CH[c] = 0.24
for c in "ft()[]/-r ": _CH[c] = 0.31
for c in "0123456789abcdeghknopqsuvxyzéèêàâùûôîçJL+_=<>?$#": _CH[c] = 0.556
for c in "FTZ": _CH[c] = 0.611
for c in "ABEKPSVXYÉ": _CH[c] = 0.667
for c in "CDHNRU": _CH[c] = 0.722
for c in "GOQ": _CH[c] = 0.778
for c in "mwM": _CH[c] = 0.833
for c in "W%": _CH[c] = 0.944
for c in "→↔≤×°²": _CH[c] = 0.6


def largeur(txt, taille, gras=False):
    w = sum(_CH.get(c, 0.6) for c in txt) * taille
    return w * (1.06 if gras else 1.0)


def coupe(txt, taille, maxw, gras=False):
    """Coupe un texte en lignes de largeur <= maxw (mots entiers)."""
    lignes, cour = [], ""
    for mot in str(txt).split(" "):
        essai = (cour + " " + mot).strip()
        if cour and largeur(essai, taille, gras) > maxw:
            lignes.append(cour)
            cour = mot
        else:
            cour = essai
    if cour:
        lignes.append(cour)
    return lignes or [""]


class Page:
    def __init__(self, titre, num=0):
        self.titre = titre
        self.num = num
        self.el = []
        self.boites = []       # (x0, y0, x1, y1, texte) des textes, pour les chevauchements
        self.erreurs = []
        self.textes = []       # tous les textes écrits (contrôle croisé avec le .xrs)

    def rect(self, x, y, w, h, fill="none", stroke="#000", sw=0.25, dash=None, rx=0):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        r = f' rx="{rx}"' if rx else ""
        self.el.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}"{r} '
                       f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def line(self, x1, y1, x2, y2, stroke="#000", sw=0.25, dash=None, fleche=False):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = ' marker-end="url(#fl)"' if fleche else ""
        self.el.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                       f'stroke="{stroke}" stroke-width="{sw}"{d}{m}/>')

    def poly(self, pts, fill="none", stroke="#000", sw=0.25, dash=None, fleche=False):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = ' marker-end="url(#fl)"' if fleche else ""
        p = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
        self.el.append(f'<polyline points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{m}/>')

    def text(self, x, y, txt, t=2.5, ancre="start", gras=False, coul="#000", maxw=None, rot=0,
             controle=True, italique=False):
        """y = ligne de base. rot = -90 : texte vertical lu de bas en haut (x = axe, y = départ)."""
        txt = str(txt)
        if txt == "":
            return
        w = largeur(txt, t, gras)
        if maxw is not None and w > maxw + 0.01:
            self.erreurs.append(f"p{self.num} texte trop large ({w:.1f} > {maxw:.1f} mm) : « {txt} »")
        self.textes.append(txt)
        a = {"start": 0, "middle": 0.5, "end": 1}[ancre]
        if rot == 0:
            x0 = x - a * w
            boite = (x0, y - 0.72 * t, x0 + w, y + 0.2 * t)
        else:   # -90
            y0 = y + a * w
            boite = (x - 0.72 * t, y0 - w, x + 0.2 * t, y0)
        if controle:
            self.boites.append(boite + (txt,))
        st = f' font-weight="bold"' if gras else ""
        st += ' font-style="italic"' if italique else ""
        tr = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot else ""
        self.el.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{t}" text-anchor="{ancre}"{st} '
                       f'fill="{coul}"{tr}>{escape(txt)}</text>')

    def bloc(self, x, y, txt, t=2.5, maxw=100, interligne=1.3, **kw):
        """Paragraphe coupé à maxw ; renvoie le y suivant."""
        for ligne in coupe(txt, t, maxw, kw.get("gras", False)):
            self.text(x, y, ligne, t, maxw=maxw, **kw)
            y += t * interligne
        return y

    def chevauchements(self):
        out = []
        b = self.boites
        for i in range(len(b)):
            for j in range(i + 1, len(b)):
                p, q = b[i], b[j]
                if p[0] < q[2] - 0.05 and q[0] < p[2] - 0.05 and p[1] < q[3] - 0.05 and q[1] < p[3] - 0.05:
                    out.append(f"p{self.num} chevauchement : « {p[4]} » / « {q[4]} »")
        return out

    def svg(self):
        defs = ('<defs><marker id="fl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" '
                'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker></defs>')
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}" '
                f'font-family="Arial, Helvetica, sans-serif">{defs}' + "".join(self.el) + "</svg>")
