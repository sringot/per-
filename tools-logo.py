#!/usr/bin/env python3
"""Découpe le pictogramme du logo fourni et fabrique les fichiers du site.

Le fichier livré (`logov2.png`) a un **fond opaque** : le M orange est posé
sur un halo de la même couleur. Posé tel quel dans l'en-tête, il afficherait
un rectangle brun ; et un détourage par couleur ne marche pas non plus,
puisque le fond immédiat du M est aussi orange que lui :

    intérieur du M   (254,  93, 40)
    halo au contact  (250, 101, 48)   ← quasi identique
    fond lointain    (147, 113, 77)

La seule frontière est le **filet plus sombre** qui cerne le pictogramme,
lui bien tranché : (255, 69, 15), soit un bleu deux fois plus bas que
partout ailleurs. On s'en sert comme d'une digue — un remplissage lancé
depuis un coin de l'image inonde tout l'extérieur sans pouvoir la franchir.
Ce que le remplissage n'atteint pas est le pictogramme.

Rien n'est redessiné : la silhouette vient du fichier fourni. Le masque est
calculé en pleine résolution puis réduit, la réduction produisant elle-même
l'anticrénelage.

    python3 tools-logo.py
"""
import pathlib
from PIL import Image, ImageDraw

ROOT   = pathlib.Path(__file__).parent
SOURCE = ROOT / 'logov2.png'
IMG    = ROOT / 'assets/img'

# Seuil du filet de contour, relevé sur le fichier (voir l'en-tête).
B_MAX = 32
# Le pictogramme est reteinté sur l'ocre du site (--ochre). Seule la
# silhouette vient du fichier fourni ; l'orange d'origine (#FD5D28) jurait
# à côté des boutons, qui sont l'aplat le plus présent de la page.
TEINTE_SITE = (172, 75, 40)
# Est « orange » tout pixel dont le rouge dépasse largement le bleu. Sert à
# réaccorder le bloc texte sans toucher au sous-titre gris.
ORANGE_MIN = 80
# Le pictogramme seul se perdrait sur une barre d'onglets sombre : le
# favicon garde un fond crème arrondi.
FAVI_BG, FAVI_PAD, FAVI_RADIUS = (248, 241, 231), 0.13, 0.19


def silhouette(im):
    """Masque du pictogramme, par remplissage de l'extérieur."""
    _, _, b = im.convert('RGB').split()
    digue = Image.new('L', im.size)
    digue.putdata([0 if pb <= B_MAX else 255 for pb in b.get_flattened_data()])
    ImageDraw.floodfill(digue, (0, 0), 128)
    # Tout ce que l'inondation n'a pas atteint : l'intérieur, filet compris.
    return digue.point(lambda v: 255 if v != 128 else 0)


def teinte(im, m):
    """Couleur du M, moyennée sur son cœur — le filet est écarté."""
    coeur = m.point(lambda v: 255 if v > 250 else 0)
    n, tot = 0, [0, 0, 0]
    for px, sel, pb in zip(im.convert('RGB').get_flattened_data(),
                           coeur.get_flattened_data(),
                           im.convert('RGB').split()[2].get_flattened_data()):
        if sel and pb > B_MAX:          # hors filet
            n += 1
            for i in range(3):
                tot[i] += px[i]
    return tuple(round(c / n) for c in tot)


def poids(nom):
    return f'{(IMG / nom).stat().st_size / 1024:.1f} Ko'


def enregistre(im, chemin, k=4, n=64):
    """Écrit un PNG à palette : k teintes × n opacités.

    Le logo n'a qu'une ou deux teintes, tout le dégradé est dans la
    transparence. En RGBA, PNG dépense 4 octets par pixel et compresse mal ;
    avec une palette indexée il n'en dépense qu'un. Le pictogramme tombe
    ainsi de 17,6 à 5,5 Ko, pour un écart d'opacité plafonné à 3/255.
    """
    if k * n > 256:
        raise ValueError('palette au-delà de 256 entrées')
    # Les teintes se relèvent sur les seuls pixels opaques. Sur toute
    # l'image, les pixels transparents — majoritairement orange — noyaient
    # le gris du sous-titre, qui repassait orange.
    opaques = [px[:3] for px in im.get_flattened_data() if px[3] > 128]
    echant = Image.new('RGB', (len(opaques), 1))
    echant.putdata(opaques)
    ref = echant.quantize(colors=k)
    palette = ref.getpalette()[:k * 3]
    idx_t = list(im.convert('RGB').quantize(palette=ref, dither=Image.Dither.NONE)
                 .get_flattened_data())
    idx_a = [min(n - 1, a * n // 256) for a in im.getchannel('A').get_flattened_data()]

    out = Image.new('P', im.size)
    out.putdata([t * n + a for t, a in zip(idx_t, idx_a)])
    out.putpalette([palette[t * 3 + c] for t in range(k) for _ in range(n) for c in range(3)])
    trans = bytes(min(255, round((i % n) * 255 / (n - 1))) for i in range(k * n))
    out.save(chemin, optimize=True, transparency=trans)


def main():
    if not SOURCE.exists():
        raise SystemExit(f'fichier source introuvable : {SOURCE.name}')

    src = Image.open(SOURCE)
    m = silhouette(src)
    box = m.getbbox()
    if not box:
        raise SystemExit('aucun pictogramme détecté — seuil du filet à revoir')

    origine = '#%02X%02X%02X' % teinte(src, m)
    couleur = TEINTE_SITE
    hexa = '#%02X%02X%02X' % couleur
    m = m.crop(box)
    print(f'pictogramme : {m.size[0]}×{m.size[1]} px, '
          f'teinte {origine} du fichier → {hexa} (ocre du site)')

    # Aplat de la teinte du site, découpé par le masque : le filet de
    # contour s'en va avec le fond qu'il servait à délimiter.
    plein = Image.new('RGBA', m.size, couleur + (255,))
    plein.putalpha(m)
    a_hauteur = lambda h: plein.resize(
        (round(m.size[0] * h / m.size[1]), h), Image.LANCZOS)

    # ---- pictogramme du site ----
    mark = a_hauteur(300)
    enregistre(mark, IMG / 'logo-mark.png')
    print(f'  logo-mark.png     {mark.size[0]}×{mark.size[1]}  {poids("logo-mark.png")}')

    # ---- bloc texte réaccordé ----
    # Le site n'insère plus que le pictogramme : ce fichier n'est plus
    # affiché nulle part. Il reste tenu à jour pour qu'on puisse remettre
    # le nom à côté du M sans se retrouver avec deux oranges différents.
    # Seul l'orange bouge, le sous-titre gris ne bronche pas ; l'opération
    # est idempotente.
    txt = Image.open(IMG / 'logo-text.png').convert('RGBA')
    px = [(couleur + (a,)) if (r - b) > ORANGE_MIN else (r, g, b, a)
          for r, g, b, a in txt.get_flattened_data()]
    txt.putdata(px)
    enregistre(txt, IMG / 'logo-text.png')
    print(f'  logo-text.png     réaccordé sur {hexa}  {poids("logo-text.png")}')

    # ---- favicons ----
    for taille, nom in ((180, 'favicon-180.png'), (32, 'favicon.png')):
        fav = Image.new('RGBA', (taille,) * 2, (0, 0, 0, 0))
        # Coins arrondis tracés ×4 puis réduits : tracés directement à 32 px
        # ils feraient des marches d'escalier.
        fond = Image.new('RGBA', (taille * 4,) * 2, (0, 0, 0, 0))
        ImageDraw.Draw(fond).rounded_rectangle(
            [0, 0, taille * 4 - 1, taille * 4 - 1],
            radius=round(taille * FAVI_RADIUS) * 4, fill=FAVI_BG + (255,))
        fav.alpha_composite(fond.resize((taille,) * 2, Image.LANCZOS))

        picto = a_hauteur(round(taille * (1 - 2 * FAVI_PAD)))
        fav.alpha_composite(picto, ((taille - picto.size[0]) // 2,
                                    (taille - picto.size[1]) // 2))
        fav.save(IMG / nom, optimize=True)
        print(f'  {nom:17s} {taille}×{taille}  {poids(nom)}')

    print(f'\nÀ répercuter si la teinte a changé : --brand dans style.css → {hexa}')


if __name__ == '__main__':
    main()
