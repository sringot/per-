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
revient en petites surfaces : terracotta pour Moi, Le lieu et
Rendez-vous (tiré de la carte Madéro), doré pour Avis (tiré de sa texture
de page). Chacune est une **teinte recomposée**, en bande 2:1. Même séparation que
pour le fond : la couleur devient une teinte fixe, et la lumière des
taches et le grain y sont reposés, bornés. Ce sont des tons moyens, où ni
le noir ni le blanc ne tiennent si la texture s'écarte trop ; bornés
ainsi, le blanc tient sur le terracotta (4,7:1 au pire pixel) et le noir
sur le doré (5,3:1).

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

# nom : (texture d'origine, teinte, écart maximal des taches, du grain)
TEINTES = {
    'terracotta': ('assets/img/cartes/madero-texture.webp', (146, 74, 49), 10, 9),
    'dore':       ('sources/pages/avis.png',                (206, 158, 76), 18, 12),
}
TOUCHE_RAPPORT = 2
TOUCHE_LARGEUR = 800

QUALITE = 80


def source(nom):
    src = SOURCES / f'{nom}.png'
    if not src.exists():
        raise SystemExit(f'texture introuvable : {src}')
    return Image.open(src).convert('RGB')


def bande(im):
    """Une bande 2:1 au milieu de la texture, à la largeur des touches."""
    W, H = im.size
    h = min(H, round(W / TOUCHE_RAPPORT))
    haut = (H - h) // 2
    return im.crop((0, haut, W, haut + h)).resize(
        (TOUCHE_LARGEUR, round(TOUCHE_LARGEUR / TOUCHE_RAPPORT)), Image.LANCZOS)


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

    for nom, (origine, teinte, ecart_lumiere, ecart_grain) in TEINTES.items():
        im = bande(Image.open(ROOT / origine).convert('RGB'))
        a = np.asarray(im).astype(float)
        taches = np.asarray(im.filter(ImageFilter.GaussianBlur(20))).astype(float)
        grain = a - taches
        lumiere = (taches - np.median(a.reshape(-1, 3), axis=0)).mean(axis=2, keepdims=True)
        p = (np.array(teinte)
             + np.clip(.4 * lumiere, -ecart_lumiere, ecart_lumiere)
             + np.clip(.6 * grain, -ecart_grain, ecart_grain))
        chemin = DEST / f'{nom}-touche.webp'
        Image.fromarray(np.clip(p, 0, 255).astype('uint8')).save(chemin, quality=QUALITE, method=6)
        print(f'{nom:10s} touche  {chemin.stat().st_size / 1024:.0f} Ko')


if __name__ == '__main__':
    main()
