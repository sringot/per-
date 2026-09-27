#!/usr/bin/env python3
"""Prépare les textures de Marie pour le haut des rubriques.

Les sources sont dans `sources/fonds/` : cinq PNG de 900 × 1600, un fondu
de lumière et d'ombres de feuillage, recouvert d'un grain fin. 2,5 Mo pièce.

Une texture floue n'a pas besoin de ses 900 px : réduite à 480, elle ne
perd rien de ce qu'on voit — des taches de lumière larges comme la main.
Ce qu'elle perd, c'est son grain, qui disparaît dans la réduction. Il est
recréé par le CSS, à la résolution de l'écran (voir `.affiche::before`),
ce qui vaut mieux de toute façon : un grain servi en image puis agrandi
par le navigateur devient une bouillie, un grain généré reste net.

Résultat : une vingtaine de kilo-octets par texture au lieu de 2,5 Mo.

    python3 tools-textures.py
"""
import pathlib

from PIL import Image, ImageFilter

ROOT    = pathlib.Path(__file__).parent
SOURCES = ROOT / 'sources/fonds'
DEST    = ROOT / 'assets/img/fonds'

TEXTURES = ['vert', 'jaune', 'marron', 'orange', 'rouge']

LARGEUR = 480
# Un léger flou avant la réduction : le grain d'origine, simplement réduit,
# laissait un fourmillement qui se battait avec le grain du CSS.
FLOU = 2.5
QUALITE = 78


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    for nom in TEXTURES:
        src = SOURCES / f'fond-{nom}.png'
        if not src.exists():
            raise SystemExit(f'texture introuvable : {src}')
        im = Image.open(src).convert('RGB').filter(ImageFilter.GaussianBlur(FLOU))
        im = im.resize((LARGEUR, round(LARGEUR * im.height / im.width)), Image.LANCZOS)
        chemin = DEST / f'{nom}.webp'
        im.save(chemin, quality=QUALITE, method=6)
        print(f'{nom:7s} {im.size[0]}×{im.size[1]}  {chemin.stat().st_size / 1024:.0f} Ko')


if __name__ == '__main__':
    main()
