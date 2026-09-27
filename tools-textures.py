#!/usr/bin/env python3
"""Prépare le fond commun des pages et les touches de couleur de chacune.

Les sources sont dans `sources/pages/`, créées par Marie au format
téléphone (774 × 2033). `orange.png` n'a pas de page : l'orange reste la
couleur de la seule carte Madéro.

**Le fond.** Toutes les pages ont le même : le blanc cassé de Marie
(`fond.png`), adouci. La texture d'origine a de grandes taches de
lumière ; derrière du texte, et à côté des bandeaux et des encadrés qui
ont déjà leur grain, elles faisaient trop. On sépare l'image en deux :
les taches (un flou large) et le grain (ce que le flou retire). Les taches
sont ramenées à `ADOUCI` de leur écart à la teinte médiane, le grain est
gardé entier — un blanc cassé vivant, pas une photo de papier.

**Les touches.** La couleur de chaque page ne tient plus le fond : elle
revient en petites surfaces. Moi et Le lieu empruntent la texture d'une
carte (l'orange de Madéro, le jaune de Deep tissus), déjà produite par
`tools-cartes-images.py`. Avis et Rendez-vous gardent la leur : une bande
de leur texture de page, en 2:1, comme les encadrés de prix des fiches.

    python3 tools-textures.py
"""
import pathlib

import numpy as np
from PIL import Image, ImageFilter

ROOT    = pathlib.Path(__file__).parent
SOURCES = ROOT / 'sources/pages'
DEST    = ROOT / 'assets/img/pages'

FOND   = 'fond'
ADOUCI = .3
# Rayon du flou qui sépare les taches du grain : au-dessus du grain (quelques
# pixels), en dessous des taches (une centaine).
RAYON  = 30

TOUCHES = ['avis', 'rdv']
TOUCHE_RAPPORT = 2
TOUCHE_LARGEUR = 800

QUALITE = 80


def source(nom):
    src = SOURCES / f'{nom}.png'
    if not src.exists():
        raise SystemExit(f'texture introuvable : {src}')
    return Image.open(src).convert('RGB')


def main():
    DEST.mkdir(parents=True, exist_ok=True)

    im = source(FOND)
    a = np.asarray(im).astype(float)
    taches = np.asarray(im.filter(ImageFilter.GaussianBlur(RAYON))).astype(float)
    grain = a - taches
    mediane = np.median(a.reshape(-1, 3), axis=0)
    fond = np.clip(mediane + ADOUCI * (taches - mediane) + grain, 0, 255).astype('uint8')
    chemin = DEST / 'fond.webp'
    Image.fromarray(fond).save(chemin, quality=QUALITE, method=6)
    print(f'fond   {im.size[0]}×{im.size[1]}  {chemin.stat().st_size / 1024:.0f} Ko')

    for page in TOUCHES:
        im = source(page)
        W, H = im.size
        h = round(W / TOUCHE_RAPPORT)
        haut = (H - h) // 2
        bande = im.crop((0, haut, W, haut + h)).resize(
            (TOUCHE_LARGEUR, round(TOUCHE_LARGEUR / TOUCHE_RAPPORT)), Image.LANCZOS)
        chemin = DEST / f'{page}-touche.webp'
        bande.save(chemin, quality=QUALITE, method=6)
        print(f'{page:6s} touche  {chemin.stat().st_size / 1024:.0f} Ko')


if __name__ == '__main__':
    main()
