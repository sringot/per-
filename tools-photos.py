#!/usr/bin/env python3
"""Découpe le portrait de Marie aux formats attendus par les gabarits.

Une seule photo alimente trois emplacements, chacun avec son propre
rapport d'aspect. Recadrer à la main donnerait trois fichiers qu'on ne
saurait plus régénérer : le cadrage est donc décrit ici, en fractions de
l'image d'origine, et le script produit les fichiers.

Le point de visée est le **visage**, pas le centre de l'image : un
recadrage centré coupait le haut du crâne sur le format le plus carré.

    python3 tools-photos.py
"""
import pathlib
from PIL import Image

ROOT   = pathlib.Path(__file__).parent
SOURCE = ROOT / 'assets/img/marie-source.png'
DEST   = ROOT / 'assets/img'

# Repères relevés sur la photo (fractions de largeur / hauteur).
VISAGE_X, VISAGE_Y = 0.55, 0.40

# nom, rapport, largeur finale, part de l'image gardée, visée verticale
# (la visée par défaut convient aux formats hauts ; un bandeau large doit
#  viser plus haut, sinon le crâne sort du cadre)
FORMATS = [
    # Héros de l'accueil : arche, un peu plus haute que large.
    ('marie-hero.webp',      1 / 1.1, 1040, 0.98, VISAGE_Y),
    # Page « à propos » : portrait 4/5.
    ('marie-portrait.webp',  4 / 5,    800, 0.92, VISAGE_Y),
    # Héros sur téléphone : l'arche y est large et basse. Recadrer la
    # version verticale à cette hauteur rognait les côtés et cassait la
    # composition ; cette découpe-ci est cadrée pour ce format.
    # Cadrée large mais pas en bandeau : c'est le conteneur qui découpe
    # la bande finale, via `object-position`. Une découpe 16/9 ne pouvait
    # pas contenir la tête entière, la photo d'origine étant verticale.
    # Toute la largeur disponible : moins on zoome, moins la tête occupe
    # de hauteur une fois rendue, et plus la bande visible peut être basse.
    ('marie-hero-large.webp', 4 / 3,   930, 1.00, 0.385),
    # V2 : le portrait est un disque. Deux tailles — sur téléphone il
    # occupe une bien plus grande part de l'écran, donc moins de pixels
    # suffisent pour la même netteté apparente.
    ('marie-rond.webp',       1 / 1,    900, 0.86, 0.375),
    ('marie-rond-m.webp',     1 / 1,    700, 0.86, 0.375),
]


def recadre(im, rapport, part, visee_y):
    """Recadre autour du visage, en gardant `part` de la dimension limitante."""
    W, H = im.size
    # Plus grande boîte au bon rapport qui tienne dans l'image.
    if W / H > rapport:
        h = H * part
        w = h * rapport
    else:
        w = W * part
        h = w / rapport

    cx, cy = W * VISAGE_X, H * visee_y
    x = min(max(cx - w / 2, 0), W - w)
    y = min(max(cy - h / 2, 0), H - h)
    return im.crop((round(x), round(y), round(x + w), round(y + h)))


def main():
    if not SOURCE.exists():
        raise SystemExit(f'photo introuvable : {SOURCE}')
    src = Image.open(SOURCE).convert('RGB')
    print(f'source : {src.size[0]}×{src.size[1]}')

    for nom, rapport, largeur, part, visee in FORMATS:
        im = recadre(src, rapport, part, visee)
        im = im.resize((largeur, round(largeur / rapport)), Image.LANCZOS)
        chemin = DEST / nom
        im.save(chemin, quality=82, method=6)
        print(f'  {nom:22s} {im.size[0]}×{im.size[1]}  '
              f'{chemin.stat().st_size / 1024:.1f} Ko')


if __name__ == '__main__':
    main()
