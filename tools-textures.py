#!/usr/bin/env python3
"""Prépare les textures de fond des pages Moi, Le lieu, Massages, Avis et Rendez-vous.

Les sources sont dans `sources/pages/`, une par page, créées par Marie au
format téléphone (774 × 2033). `orange.png` n'a pas de page : l'orange reste
la couleur de la seule carte Madéro.

Elles sont servies à leur largeur d'origine, sans flou ni réduction. Une
première version les floutait et les réduisait à 480 px, en recréant le
grain en CSS : c'était léger, mais la texture perdait sa force et son grain
propre, et fondue dans un aplat pâle elle faisait sale. C'est justement
le grain et la couleur pleine qu'on veut ici.

    python3 tools-textures.py
"""
import pathlib

from PIL import Image

ROOT    = pathlib.Path(__file__).parent
SOURCES = ROOT / 'sources/pages'
DEST    = ROOT / 'assets/img/pages'

PAGES = ['moi', 'lieu', 'massages', 'avis', 'rdv']
QUALITE = 80


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    for page in PAGES:
        src = SOURCES / f'{page}.png'
        if not src.exists():
            raise SystemExit(f'texture introuvable : {src}')
        im = Image.open(src).convert('RGB')
        chemin = DEST / f'{page}.webp'
        im.save(chemin, quality=QUALITE, method=6)
        print(f'{page:5s} {im.size[0]}×{im.size[1]}  {chemin.stat().st_size / 1024:.0f} Ko')


if __name__ == '__main__':
    main()
