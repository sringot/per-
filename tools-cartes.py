#!/usr/bin/env python3
"""Extrait les cinq cartes de soins de la planche de référence.

`reference-cartes-soins.png` est une planche fournie par Marie :
cinq cartes, chacune avec sa couleur de fond, un monogramme dessiné dans
l'esprit du logo (deux têtes rondes posées sur une lettre pleine), et le
nom du soin en bas.

Deux choses en sont tirées, et elles le sont **par le script** plutôt qu'à
l'œil : les couleurs, relevées à la médiane pour ne pas se faire piéger par
le grain de l'image, et les monogrammes, vectorisés — la planche est en
1799 px de large, soit ~150 px par monogramme, ce qui piquerait sur un
écran dense. Tracés, ils pèsent quelques centaines d'octets et ne piquent
jamais.

    python3 tools-cartes.py

Écrit `assets/img/soins/*.svg` et affiche le bloc CSS des couleurs, à
recopier dans `assets/css/v2.css`.
"""
import pathlib
import re
import subprocess
import tempfile

import numpy as np
from PIL import Image

ROOT      = pathlib.Path(__file__).parent
SOURCE    = ROOT / 'reference-cartes-soins.png'
DEST      = ROOT / 'assets/img/soins'

# Le monogramme occupe la partie haute de la carte ; le nom du soin, écrit
# en clair, occupe le bas. Le borner évite d'avaler le texte dans le tracé.
HAUT, BAS = 0.10, 0.76

# Agrandissement avant vectorisation : potrace suit l'escalier des pixels,
# et à 150 px de haut cet escalier se voit. Interpolé ×5, il s'efface.
ZOOM = 5

NOMS = ['kobido', 'relaxant', 'deep-tissus', 'madero', 'drainage']

# Le socle du site, relevé sur l'image de fond. Sert à vérifier les teintes
# qui sortent de leur carte — le repère du tableau des tarifs.
SOCLE = (0xFC, 0xF0, 0xE2)


def cartes(im):
    """Repère les colonnes de la planche : les cartes sont sur fond blanc."""
    blanc = (im > 238).all(axis=2)
    plein = blanc.mean(axis=0) < .5
    bornes, dedans = [], False
    for x, p in enumerate(plein):
        if p and not dedans:
            deb, dedans = x, True
        elif not p and dedans:
            bornes.append((deb, x)); dedans = False
    if dedans:
        bornes.append((deb, len(plein)))

    lig = blanc[:, bornes[0][0]:bornes[0][1]].mean(axis=1) < .5
    ys = np.where(lig)[0]
    return bornes, (ys[0], ys[-1] + 1)


def deux_couleurs(bloc):
    """Sépare fond et monogramme, et rend les deux couleurs médianes.

    La planche est bruitée : la couleur la plus fréquente n'y représente
    que 6 à 14 % des pixels. Une médiane sur chaque groupe donne le ton
    réel, là où un simple mode attrape un pixel de grain.
    """
    plat = bloc.reshape(-1, 3)
    fond = np.median(plat, axis=0)
    ecart = np.abs(plat - fond).sum(axis=1)
    # Seuil à mi-chemin entre le fond et ce qui s'en éloigne le plus.
    seuil = ecart.max() * .45
    loin = plat[ecart > seuil]
    return (np.median(plat[ecart <= seuil], axis=0).astype(int),
            np.median(loin, axis=0).astype(int),
            seuil)


def sans_bruit(m, part=.04):
    """Ne garde que les taches d'encre d'aire comparable à la plus grande.

    La planche porte un léger vignettage : sur les fonds sombres, ses bords
    passent le seuil et laissent de longs filets verticaux qui se retrouvent
    tracés à côté du monogramme. Les filets sont fins mais hauts, donc une
    simple aire minimale absolue ne les distingue pas — c'est leur taille
    *relative* au monogramme qui les trahit.
    """
    h, w = m.shape
    vu = np.zeros_like(m, dtype=np.int32)
    aires, n = [0], 0
    for y0 in range(h):
        for x0 in range(w):
            if not m[y0, x0] or vu[y0, x0]:
                continue
            n += 1
            pile, aire = [(y0, x0)], 0
            vu[y0, x0] = n
            while pile:
                y, x = pile.pop()
                aire += 1
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    v, u = y + dy, x + dx
                    if 0 <= v < h and 0 <= u < w and m[v, u] and not vu[v, u]:
                        vu[v, u] = n
                        pile.append((v, u))
            aires.append(aire)
    aires = np.array(aires)
    garde = aires >= aires.max() * part
    garde[0] = False
    return garde[vu]


def luminance(c):
    v = np.asarray(c, dtype=float) / 255
    v = np.where(v <= .03928, v / 12.92, ((v + .055) / 1.055) ** 2.4)
    return float(v @ (.2126, .7152, .0722))


def contraste(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + .05) / (min(la, lb) + .05)


def encre_lisible(signe, fond, vise=4.5):
    """Assombrit (ou éclaircit) la couleur du monogramme jusqu'à être lisible.

    Le monogramme est une grande forme pleine : sa couleur d'origine suffit
    à le lire. Le nom du soin et sa description, eux, sont du petit texte —
    et sur la planche, trois cartes sur cinq tombent autour de 2:1, très en
    dessous des 4,5:1 exigés. On garde donc la teinte, en poussant sa
    clarté du côté opposé au fond jusqu'à passer le seuil.
    """
    if contraste(signe, fond) >= vise:
        return np.asarray(signe, dtype=int)

    # Les deux directions sont essayées : sur l'orange, éclaircir plafonne à
    # 4,1:1 même en blanc pur, alors qu'assombrir passe. On retient celle qui
    # atteint la cible en s'écartant le moins de la teinte d'origine.
    depart = np.asarray(signe, dtype=float)
    meilleures = []
    for vers in (np.zeros(3), np.full(3, 255.)):
        for k in range(1, 101):
            essai = np.round(depart + (vers - depart) * k / 100).astype(int)
            if contraste(essai, fond) >= vise:
                meilleures.append((k, essai))
                break
    if not meilleures:
        raise SystemExit(f'aucune encre à {vise}:1 sur {fond}')
    return min(meilleures)[1]


def trace(masque):
    """Vectorise un masque binaire avec potrace, et rend le SVG."""
    with tempfile.TemporaryDirectory() as tmp:
        pbm = pathlib.Path(tmp) / 'm.pbm'
        svg = pathlib.Path(tmp) / 'm.svg'
        masque.save(pbm)
        subprocess.run(
            ['potrace', str(pbm), '-s', '-o', str(svg),
             '--turdsize', '8',      # ignore les îlots de bruit
             '--alphamax', '1.2',    # coins arrondis : le dessin l'est
             '--opttolerance', '.4'],
            check=True)
        return svg.read_text()


def main():
    if not SOURCE.exists():
        raise SystemExit(f'planche introuvable : {SOURCE}')
    im = np.asarray(Image.open(SOURCE).convert('RGB')).astype(int)
    colonnes, (y0, y1) = cartes(im)
    if len(colonnes) != len(NOMS):
        raise SystemExit(f'{len(colonnes)} cartes trouvées, {len(NOMS)} attendues')

    DEST.mkdir(parents=True, exist_ok=True)
    couleurs = []

    for nom, (x0, x1) in zip(NOMS, colonnes):
        carte = im[y0:y1, x0:x1]
        h = carte.shape[0]
        zone = carte[int(h * HAUT):int(h * BAS)]
        fond, signe, seuil = deux_couleurs(zone)

        # Masque du monogramme : noir = encre, pour potrace.
        ecart = np.abs(zone - fond).sum(axis=2)
        m = sans_bruit(ecart > seuil)
        ys, xs = np.where(m)
        marge = 4
        m = m[max(ys.min() - marge, 0):ys.max() + marge,
              max(xs.min() - marge, 0):xs.max() + marge]

        img = Image.fromarray(np.where(m, 0, 255).astype('uint8'), 'L')
        img = img.resize((img.width * ZOOM, img.height * ZOOM), Image.LANCZOS)
        img = img.point(lambda v: 0 if v < 128 else 255).convert('1')

        svg = trace(img)
        larg = float(re.search(r'width="([\d.]+)pt"', svg).group(1))
        haut = float(re.search(r'height="([\d.]+)pt"', svg).group(1))
        corps = re.search(r'(<g transform=.*?</g>)', svg, re.S).group(1)

        # Toile carrée, dessin centré : les cinq monogrammes n'ont pas les
        # mêmes proportions, et les poser tels quels dans la carte les
        # ferait paraître de tailles différentes. Une toile commune leur
        # donne la même hauteur apparente, comme les capitales d'une fonte.
        cote = max(larg, haut)
        dx, dy = (cote - larg) / 2, (cote - haut) / 2

        chemin = DEST / f'{nom}.svg'
        chemin.write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cote:.0f} {cote:.0f}">'
            f'<g transform="translate({dx:.1f} {dy:.1f})">{corps}</g></svg>\n',
            encoding='utf-8')

        hexa = lambda c: '#%02X%02X%02X' % tuple(c)
        texte = encre_lisible(signe, fond)
        # Hors de sa carte, le monogramme se pose sur le socle du site : sa
        # teinte doit y être lisible aussi. 3:1 suffit — c'est un tracé, pas
        # du texte (WCAG 1.4.11).
        marque = encre_lisible(signe, SOCLE, vise=3.0)
        couleurs.append((nom, hexa(fond), hexa(signe), hexa(texte),
                         contraste(signe, fond), contraste(texte, fond),
                         hexa(marque)))
        print(f'  {nom:12s} fond {hexa(fond)}  signe {hexa(signe)}'
              f' ({contraste(signe, fond):.1f}:1)  texte {hexa(texte)}'
              f' ({contraste(texte, fond):.1f}:1)  marque {hexa(marque)}'
              f' ({contraste(marque, SOCLE):.1f}:1)')

    print('\n/* Relevé sur la planche de référence par tools-cartes.py.')
    print('   `signe` est la couleur du monogramme, `texte` la même teinte')
    print('   poussée jusqu\'à 4,5:1 — le petit texte l\'exige, pas la grande forme. */')
    for nom, fond, signe, texte, _, _, marque in couleurs:
        print(f'.soin--{nom}{{ --fond:{fond}; --signe-c:{signe}; --texte:{texte};'
              f' --marque:{marque}; --signe:url(../img/soins/{nom}.svg); }}')
    print()
    print(f'/* `--marque` : la même teinte, lisible sur le socle du site')
    print(f'   ({hex(SOCLE[0])[2:].upper()}… soit #%02X%02X%02X) — le monogramme sert de repère' % tuple(SOCLE))
    print('   dans le tableau des tarifs, hors de sa carte et donc hors de son fond. */')


if __name__ == '__main__':
    main()
