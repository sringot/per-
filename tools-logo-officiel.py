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
import sys

from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).parent
DEST = ROOT / 'assets/img/logo-officiel.png'
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
        icone.save(chemin, optimize=True)
        print(f'{rel} — {taille}×{taille}, {chemin.stat().st_size // 1024} Ko')


if __name__ == '__main__':
    main()
