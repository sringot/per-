#!/usr/bin/env python3
"""Prépare les cartes de soins dessinées par Marie pour le site.

Les sources sont dans `sources/cartes/` : cinq PNG de 900 × 1600, une
texture granuleuse et un monogramme posé au centre. Elles pèsent 2,5 Mo
chacune — le site entier en pesait 224 Ko. Ce script en tire deux formats
par carte, en WebP :

- la carte entière, pour la planche de l'onglet Massages ;
- un bandeau 16:9 centré sur le monogramme, pour le haut de la fiche.

Le cadrage du bandeau n'est pas estimé à l'œil. Marie a fourni les mêmes
textures sans lettre (`sources/fonds/`) : la différence entre une carte et
son fond est nulle partout sauf sur le monogramme, ce qui donne sa position
exacte. Sur les cinq cartes, il tient entre 33 et 58 % de la hauteur.

    python3 tools-cartes-images.py
"""
import pathlib

import numpy as np
from PIL import Image

ROOT    = pathlib.Path(__file__).parent
SOURCES = ROOT / 'sources'
DEST    = ROOT / 'assets/img/cartes'

# lettre du fichier source, texture sans lettre, nom utilisé sur le site
CARTES = [
    ('K', 'rouge',  'kobido'),
    ('r', 'vert',   'relaxant'),
    ('m', 'orange', 'madero'),
    ('d', 'marron', 'drainage'),
    ('t', 'jaune',  'deep-tissus'),
]

# 600 px : sur la planche, une carte fait 173 px de large sur un téléphone
# de 390 px, soit 519 pixels réels sur un écran à forte densité.
CARTE_LARGEUR = 600

# 16:9 et non 2,4:1 comme l'ancien bandeau. Le monogramme occupe 40 % de
# la hauteur de la carte, soit 400 px sur 1600 ; un bandeau de 2,4:1 sur
# toute la largeur n'en fait que 375, et coupait la lettre.
BANDEAU_RAPPORT = 16 / 9
BANDEAU_LARGEUR = 900

QUALITE = 80


def monogramme(carte, fond):
    """Boîte englobante du monogramme : là où la carte diffère de son fond."""
    c = np.asarray(carte).astype(int)
    f = np.asarray(fond).astype(int)
    ys, xs = np.where(np.abs(c - f).sum(axis=2) > 60)
    return xs.min(), ys.min(), xs.max(), ys.max()


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    for lettre, texture, nom in CARTES:
        carte = Image.open(SOURCES / 'cartes' / f'{lettre}-img.png').convert('RGB')
        fond  = Image.open(SOURCES / 'fonds' / f'fond-{texture}.png').convert('RGB')
        W, H = carte.size
        x0, y0, x1, y1 = monogramme(carte, fond)

        im = carte.resize((CARTE_LARGEUR, round(CARTE_LARGEUR * H / W)), Image.LANCZOS)
        chemin = DEST / f'{nom}.webp'
        im.save(chemin, quality=QUALITE, method=6)

        # Bandeau : toute la largeur, centré en hauteur sur le monogramme.
        h = round(W / BANDEAU_RAPPORT)
        cy = (y0 + y1) / 2
        haut = int(min(max(cy - h / 2, 0), H - h))
        bandeau = carte.crop((0, haut, W, haut + h))
        bandeau = bandeau.resize((BANDEAU_LARGEUR, round(BANDEAU_LARGEUR / BANDEAU_RAPPORT)),
                                 Image.LANCZOS)
        chemin_b = DEST / f'{nom}-bandeau.webp'
        bandeau.save(chemin_b, quality=QUALITE, method=6)

        print(f'{nom:12s} monogramme y {y0 / H:.2f}-{y1 / H:.2f}  '
              f'carte {chemin.stat().st_size / 1024:.0f} Ko  '
              f'bandeau {chemin_b.stat().st_size / 1024:.0f} Ko')


if __name__ == '__main__':
    main()
