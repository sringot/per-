#!/usr/bin/env python3
"""Assemble le site en un fichier unique et autonome, pour l'aperçu.

Un artifact ne peut héberger qu'un seul fichier : ce script embarque les
polices, la feuille de style, le script et les illustrations dans la page
d'accueil. La V2 tenant déjà en une seule page — les rubriques sont des
panneaux présents dans le document —, il n'y a plus de routeur à simuler :
l'aperçu se comporte exactement comme le site en ligne.

Ne sert qu'à la prévisualisation — le vrai site reste multi-fichiers.
"""
import base64, pathlib, re

ROOT = pathlib.Path(__file__).parent

# ---- polices ----
# Une seule déclaration : Figtree est une police variable, les « trois
# graisses » livrées par Google en étaient trois copies du même fichier.
b64 = base64.b64encode((ROOT / 'assets/fonts/figtree-400-latin.woff2').read_bytes()).decode()
faces = ["@font-face{font-family:'Figtree';font-style:normal;font-weight:400 600;"
         "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2');}" % b64]

# ---- visuels ----
MIME = {'.svg': 'image/svg+xml', '.png': 'image/png',
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp'}

def inline_illus(html):
    """Intègre tout visuel local en data: URI.

    Un artifact ne sert qu'un fichier : le moindre chemin relatif oublié
    donne une image cassée. On balaie donc `assets/img` en entier plutôt
    qu'un sous-dossier.
    """
    def sub(m):
        rel = m.group(1)
        f = ROOT / rel
        if not f.exists():
            raise SystemExit(f'visuel introuvable : {rel}')
        b64 = base64.b64encode(f.read_bytes()).decode()
        attr = m.group(0).split('=')[0]
        return f'{attr}="data:{MIME[f.suffix.lower()]};base64,{b64}"'
    # `srcset` autant que `src` : depuis que le portrait sert une découpe
    # par format, oublier le second laissait l'image mobile introuvable.
    return re.sub(r'(?:src|srcset)="(assets/img/[\w./-]+)"', sub, html)

def inline_css(css):
    """Intègre les visuels appelés depuis le CSS (`url(../img/…)`).

    Les monogrammes des cartes de soins sont posés en masque CSS, pas en
    balise `<img>` : le balayage du HTML ne les voit donc pas, et sans
    cette passe-ci les cinq cartes s'affichent vides dans l'aperçu.
    """
    def sub(m):
        rel = 'assets/' + m.group(1)
        f = ROOT / rel
        if not f.exists():
            raise SystemExit(f'visuel CSS introuvable : {rel}')
        b64 = base64.b64encode(f.read_bytes()).decode()
        return f'url(data:{MIME[f.suffix.lower()]};base64,{b64})'
    # Les guillemets sont optionnels dans `url()` : les ignorer laissait
    # passer le fond, déclaré `url('../img/fond.webp')`.
    return re.sub(r'''url\(\s*['"]?\.\./([\w./-]+)['"]?\s*\)''', sub, css)


css = inline_css((ROOT / 'assets/css/v2.css').read_text(encoding='utf-8'))
js  = (ROOT / 'assets/js/v2.js').read_text(encoding='utf-8')

src = (ROOT / 'index.html').read_text(encoding='utf-8')
# Le titre du site porte la ville et la spécialité — utile pour Google,
# encombrant comme nom d'aperçu. Et il bougera le jour où la ville change,
# alors qu'un aperçu republié doit garder le même nom pour rester
# reconnaissable. On s'en tient donc à la marque.
title = 'marieemassage'
body = re.search(r'<body[^>]*>(.*)</body>', src, re.S).group(1)
body = inline_illus(body)
# Feuille et script sont embarqués plus bas ; les balises d'origine
# pointeraient vers des fichiers que l'artifact ne sert pas.
body = re.sub(r'<script src="assets/js/v2\.js"[^>]*></script>', '', body)

if 'assets/img/' in body or '../img/' in css or '../fonts/' in css:
    raise SystemExit('un chemin de visuel n’a pas été embarqué')

# L'artifact suit le thème du lecteur ; le site n'a qu'un mode clair.
lock = (':root{color-scheme:light}\n'
        ':root[data-theme="dark"],:root[data-theme="light"]{color-scheme:light}')

out = (f"<title>{title}</title>\n"
       f"<style>\n{chr(10).join(faces)}\n{lock}\n{css}\n</style>\n"
       f"{body}\n<script>\n{js}\n</script>\n")

dest = pathlib.Path('/tmp/claude-0/-home-user-per-/0ab23514-8cad-52d4-a3c4-7a8a46290735'
                    '/scratchpad/marie-massage-v2.html')
dest.write_text(out, encoding='utf-8')
print(f'aperçu écrit — {round(len(out.encode())/1024)} Ko → {dest}')
