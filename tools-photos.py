#!/usr/bin/env python3
"""Prépare les photos du site aux formats attendus par les gabarits.

Deux photographies alimentent le site : une scène de massage, qui tient
l'accueil, et un portrait posé, qui reste dans « Moi ». Chaque emplacement
a son propre rapport d'aspect. Recadrer à la main donnerait des fichiers
qu'on ne saurait plus régénérer : le cadrage est décrit ici, en fractions
de l'image d'origine, et le script produit les fichiers.

Le point de visée n'est jamais le centre de l'image : sur le portrait
c'est le visage — un recadrage centré coupait le haut du crâne sur le
format le plus carré — et sur la scène c'est le point entre le visage de
Marie et ses mains.

    python3 tools-photos.py
"""
import pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).parent
DEST = ROOT / 'assets/img'

# Le cliché de Marie en séance qui reste propre au panneau « Moi ». Il
# arrive déjà cadré en 3/4, celui du gabarit : rien à recadrer, seulement à
# convertir. Il fait 2 Mo de PNG, ce qui est hors de question sur une page
# ouverte au téléphone.
#
# Le second cliché de la série ne passe plus par ici : il est devenu la
# photo de l'accueil, et il est donc recadré comme les autres, plus bas.
#
# 620 px de large : le cadre le plus grand fait 265 px sur grand écran, et
# 620 couvre le double pour les écrans à forte densité sans payer plus.
SEANCES = [('seance-source-2.png', 'marie-seance-2.webp')]
SEANCE_LARGEUR = 620

# Repères relevés sur les photos (fractions de largeur / hauteur).
# Le portrait posé : le visage est haut et à droite du centre.
VISAGE_X, VISAGE_Y = 0.55, 0.40
# La photo en séance : deux personnes, pas une. La visée est prise entre le
# visage de Marie et ses mains — c'est le geste qui fait l'image, et viser
# le seul visage repoussait les mains hors du cadre sur les formats courts.
SEANCE_X, SEANCE_Y = 0.52, 0.44

# source, nom, rapport, largeur finale, part de l'image gardée, visée
# (chaque découpe nomme sa source : l'accueil et le panneau « Moi » ne
#  montrent plus la même photographie, et une visée unique ne pouvait pas
#  convenir à un portrait posé comme à une scène à deux personnages)
FORMATS = [
    # Arche de l'accueil. La photo en séance a presque exactement le
    # rapport de l'arche (0,750 contre 0,746) : elle y entre entière, on ne
    # rogne que 2 % pour absorber l'écart.
    ('seance-source-1.png', 'marie-hero.webp',   1 / 1.34, 1040, 0.98,
     SEANCE_X, SEANCE_Y),
    # Même cadrage sur téléphone, moins de pixels : le cadre y est plus
    # petit, et la netteté apparente est la même pour la moitié du poids.
    ('seance-source-1.png', 'marie-hero-m.webp', 1 / 1.34,  700, 0.98,
     SEANCE_X, SEANCE_Y),
    # Portrait posé, gardé pour le panneau « Moi » et les partages.
    ('marie-source.png', 'marie-portrait.webp',  4 / 5,     800, 0.92,
     VISAGE_X, VISAGE_Y),
    # Le même portrait au rapport des vignettes de « Moi ». Depuis que la
    # scène de massage tient l'accueil, elle ne peut plus servir aussi de
    # vignette : c'est le visage de Marie qui prend sa place, et il lui faut
    # le 3/4 de l'autre vignette pour que la paire s'aligne.
    ('marie-source.png', 'marie-moi.webp',       3 / 4,     620, 0.92,
     VISAGE_X, VISAGE_Y),
    # Découpe large du portrait. Cadrée large mais pas en bandeau : c'est
    # le conteneur qui découpe la bande finale, via `object-position`. Une
    # découpe 16/9 ne pouvait pas contenir la tête entière, la photo
    # d'origine étant verticale.
    ('marie-source.png', 'marie-hero-large.webp', 4 / 3,    930, 1.00,
     VISAGE_X, 0.385),
]


def recadre(im, rapport, part, visee_x, visee_y):
    """Recadre autour du point visé, en gardant `part` de la dimension limitante."""
    W, H = im.size
    # Plus grande boîte au bon rapport qui tienne dans l'image.
    if W / H > rapport:
        h = H * part
        w = h * rapport
    else:
        w = W * part
        h = w / rapport

    cx, cy = W * visee_x, H * visee_y
    x = min(max(cx - w / 2, 0), W - w)
    y = min(max(cy - h / 2, 0), H - h)
    return im.crop((round(x), round(y), round(x + w), round(y + h)))


def main():
    ouvertes = {}
    for source, nom, rapport, largeur, part, vx, vy in FORMATS:
        if source not in ouvertes:
            chemin_src = DEST / source
            if not chemin_src.exists():
                raise SystemExit(f'photo introuvable : {chemin_src}')
            ouvertes[source] = Image.open(chemin_src).convert('RGB')
            print(f'source : {source} — '
                  f'{ouvertes[source].size[0]}×{ouvertes[source].size[1]}')
        im = recadre(ouvertes[source], rapport, part, vx, vy)
        im = im.resize((largeur, round(largeur / rapport)), Image.LANCZOS)
        chemin = DEST / nom
        im.save(chemin, quality=82, method=6)
        print(f'  {nom:22s} {im.size[0]}×{im.size[1]}  '
              f'{chemin.stat().st_size / 1024:.1f} Ko')

    for source, nom in SEANCES:
        src = DEST / source
        if not src.exists():
            raise SystemExit(f'photo introuvable : {src}')
        im = Image.open(src).convert('RGB')
        haut = round(SEANCE_LARGEUR * im.height / im.width)
        im = im.resize((SEANCE_LARGEUR, haut), Image.LANCZOS)
        chemin = DEST / nom
        im.save(chemin, quality=82, method=6)
        print(f'  {nom:22s} {im.size[0]}×{im.size[1]}  '
              f'{chemin.stat().st_size / 1024:.1f} Ko')


if __name__ == '__main__':
    main()
