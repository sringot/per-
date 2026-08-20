#!/usr/bin/env python3
"""Prépare le logo officiel de Marie pour le web et l'impression.

Sort le logo détouré et les deux favicons, tous depuis le même fichier :
c'est ce qui garantit qu'ils ne divergeront pas.

Le fichier qu'elle fournit est un carré blanc de 1254 px avec le disque
posé au milieu. Tel quel, ses angles blancs se verraient sur le socle crème
de l'affiche : on le recadre au disque et on le détoure.

Le logo n'est jamais redessiné — ce script ne fait que recadrer, détourer
et redimensionner le fichier d'origine.

    python3 tools-logo-officiel.py "new logo.png"
"""
import pathlib
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).parent
DEST = ROOT / 'assets/img/logo-officiel.png'
# La version servie au navigateur. Le PNG de 300 px pèse 72 Ko et reste le
# fichier le plus lourd du site, pour une image affichée à 52 px au plus ;
# en WebP à 200 px il en fait 5. Le PNG est gardé pour l'affiche imprimée,
# où l'on veut les pixels.
DEST_WEB = ROOT / 'assets/img/logo-officiel.webp'
COTE_WEB = 200
# Le favicon est le logo : le régénérer d'ici évite qu'il reste sur une
# ancienne version le jour où le logo change.
FAVICONS = [('assets/img/favicon.png', 32), ('assets/img/favicon-180.png', 180)]
# Le socle du site. iOS compose l'icône d'accueil sur du noir si elle est
# transparente : celle de 180 px est donc aplatie sur ce fond.
SOCLE = (0xFC, 0xF0, 0xE2)
# Le logo est imprimé à 14 mm, soit 165 px à 300 dpi. Le double laisse de la
# marge, et le fichier est embarqué en base64 dans l'affiche : inutile de
# transporter les 1254 px d'origine.
COTE = 300
# Écart au blanc du fond au-delà duquel un pixel appartient au dessin. Assez
# haut pour ignorer le bruit de compression, assez bas pour attraper le bord
# du disque, qui est sombre.
SEUIL = 16

# Le M seul, détaché de son disque, pour le filigrane des panneaux. Le M du
# logo officiel n'a pas le même dessin que l'ancien : ses jambages s'évasent
# vers le bas et ses têtes sont plus petites et plus rapprochées. Le
# filigrane portait donc encore l'ancien tracé.
SIGNE = ROOT / 'assets/img/logo-m.svg'


def cadre_du_disque(im):
    """Étendue réelle du dessin dans le carré blanc.

    Mesurée plutôt que supposée : recadrer sur une marge estimée à l'œil
    laisserait un liseré blanc d'un côté.
    """
    px = im.load()
    w, h = im.size
    fond = px[2, 2][:3]
    dessin = lambda p: max(abs(a - b) for a, b in zip(p[:3], fond)) > SEUIL
    xs = [x for x in range(w) if any(dessin(px[x, y]) for y in range(0, h, 4))]
    ys = [y for y in range(h) if any(dessin(px[x, y]) for x in range(0, w, 4))]
    if not xs or not ys:
        raise SystemExit('aucun dessin trouvé : le fond n\'est pas uni ?')
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def signe(disque):
    """Détoure le M de son disque et le vectorise.

    Le M est le seul aplat clair du logo : on sépare sur la distance à sa
    couleur plutôt que sur un seuil de luminosité, qui attraperait aussi le
    bord adouci du disque.
    """
    px = disque.convert('RGB').load()
    w, h = disque.size
    # Couleur du M, relevée au centre d'un de ses jambages plutôt que
    # supposée : elle suit le fichier si Marie le change.
    encre = px[int(w * .32), int(h * .62)]
    binaire = Image.new('1', disque.size, 1)   # 1 = blanc = fond, pour potrace
    bp = binaire.load()
    boite = [w, h, 0, 0]
    # Le bord du disque est adouci : sur quelques pixels il traverse toutes
    # les valeurs entre le bordeaux et le blanc, dont une qui passe à moins
    # de 90 du rose. Sans cette bordure exclue, l'anneau entier était pris
    # pour du M et le cadrage couvrait l'image entière.
    cx, cy = w / 2, h / 2
    dedans = .96 ** 2
    for y in range(h):
        dy = (y - cy) / cy
        for x in range(w):
            dx = (x - cx) / cx
            if dx * dx + dy * dy > dedans:
                continue
            if sum(abs(a - b) for a, b in zip(px[x, y], encre)) < 90:
                bp[x, y] = 0
                boite = [min(boite[0], x), min(boite[1], y),
                         max(boite[2], x), max(boite[3], y)]
    marge = 4
    binaire = binaire.crop((max(boite[0] - marge, 0), max(boite[1] - marge, 0),
                            min(boite[2] + marge, w), min(boite[3] + marge, h)))

    with tempfile.TemporaryDirectory() as tmp:
        pbm = pathlib.Path(tmp) / 'm.pbm'
        svg = pathlib.Path(tmp) / 'm.svg'
        binaire.save(pbm)
        subprocess.run(['potrace', str(pbm), '-s', '-o', str(svg),
                        '--turdsize', '8',      # ignore les îlots de bruit
                        '--alphamax', '1.2',    # coins arrondis : le dessin l'est
                        '--opttolerance', '.4'], check=True)
        SIGNE.write_text(svg.read_text(), encoding='utf-8')
    return binaire.size


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    source = pathlib.Path(sys.argv[1])
    im = Image.open(source).convert('RGBA')
    coupe = im.crop(cadre_du_disque(im))

    # Une ellipse inscrite dans le cadre mesuré, pas un cercle : le disque du
    # fichier n'est pas parfaitement rond (1177 × 1191), et un cercle le
    # rognerait en haut et en bas.
    masque = Image.new('L', coupe.size, 0)
    ImageDraw.Draw(masque).ellipse((0, 0, coupe.size[0] - 1, coupe.size[1] - 1), fill=255)
    coupe.putalpha(masque)

    coupe.resize((COTE, COTE), Image.LANCZOS).save(DEST, optimize=True)
    print(f'{DEST.relative_to(ROOT)} — {coupe.size[0]}×{coupe.size[1]} px recadrés '
          f'→ {COTE}×{COTE}, {DEST.stat().st_size // 1024} Ko')

    for rel, taille in FAVICONS:
        icone = coupe.resize((taille, taille), Image.LANCZOS)
        if taille >= 180:
            plat = Image.new('RGB', icone.size, SOCLE)
            plat.paste(icone, mask=icone.getchannel('A'))
            icone = plat
        chemin = ROOT / rel
        # Deux aplats et un bord adouci : une palette de 32 couleurs les
        # rend à l'identique pour moitié moins lourd.
        methode = Image.FASTOCTREE if icone.mode == 'RGBA' else Image.MEDIANCUT
        icone.quantize(colors=32, method=methode).save(chemin, optimize=True)
        print(f'{rel} — {taille}×{taille}, {chemin.stat().st_size / 1024:.1f} Ko')

    coupe.resize((COTE_WEB, COTE_WEB), Image.LANCZOS).save(
        DEST_WEB, quality=86, method=6)
    print(f'{DEST_WEB.relative_to(ROOT)} — {COTE_WEB}×{COTE_WEB}, '
          f'{DEST_WEB.stat().st_size / 1024:.1f} Ko')

    w, h = signe(coupe)
    print(f'{SIGNE.relative_to(ROOT)} — M détouré {w}×{h} px, '
          f'{SIGNE.stat().st_size // 1024} Ko')


if __name__ == '__main__':
    main()
