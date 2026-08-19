#!/usr/bin/env python3
"""

⚠️ Ce fond n'est plus servi. L'accueil porte désormais le même filigrane que
les panneaux — le M du logo officiel en masque CSS, posé par v2.css. Ce
script et les `fond*.webp` qu'il produit ne sont gardés que pour l'historique.
Prépare l'image de fond aux formats servis par le site.

`fond-source.png` fait 1536 × 1024 pour 1,6 Mo : c'est un aplat de crèmes
et de formes très douces, donc du PNG qui code en 24 bits ce qui n'a
presque pas de détail. En WebP, la même image tombe à quelques dizaines de
kilo-octets sans différence visible — un dégradé se compresse d'autant
mieux qu'il est lisse.

Deux tailles, servies par une requête média : le fond couvre la fenêtre,
et un téléphone n'a pas besoin de 1536 px de large pour cela.

    python3 tools-fond.py
"""
import pathlib

from PIL import Image

ROOT   = pathlib.Path(__file__).parent
SOURCE = ROOT / 'fond-source.png'
DEST   = ROOT / 'assets/img'

# nom, largeur finale, rapport voulu (None = celui de la source), qualité
#
# La source est au format paysage. Servie telle quelle à un téléphone, elle
# est agrandie 1,4× pour couvrir la hauteur : on n'en voit plus qu'un tiers,
# et le pictogramme en filigrane sort du cadre. Le format téléphone reçoit
# donc **sa propre découpe**, verticale, recadrée au centre.
FORMATS = [
    ('fond.webp',   1600, None,     74),
    ('fond-m.webp',  760,  2 / 3,   72),
]


def recadre(im, rapport):
    if rapport is None:
        return im
    W, H = im.size
    if W / H > rapport:                 # trop large : on rogne les côtés
        w = round(H * rapport); h = H
    else:                               # trop haute : on rogne en hauteur
        w = W; h = round(W / rapport)
    x, y = (W - w) // 2, (H - h) // 2
    return im.crop((x, y, x + w, y + h))


def main():
    if not SOURCE.exists():
        raise SystemExit(f'fond introuvable : {SOURCE}')
    src = Image.open(SOURCE).convert('RGB')
    print(f'source : {src.size[0]}×{src.size[1]} · '
          f'{SOURCE.stat().st_size / 1024:.0f} Ko')

    for nom, largeur, rapport, qualite in FORMATS:
        im = recadre(src, rapport)
        h = round(largeur * im.size[1] / im.size[0])
        im = im.resize((largeur, h), Image.LANCZOS)
        chemin = DEST / nom
        im.save(chemin, quality=qualite, method=6)
        print(f'  {nom:14s} {largeur}×{h}  {chemin.stat().st_size / 1024:.1f} Ko')


if __name__ == '__main__':
    main()
