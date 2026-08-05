#!/usr/bin/env python3
"""Assemble les 6 pages en un fichier unique et autonome, pour l'aperçu.

Un artifact ne peut héberger qu'un seul fichier : ce script embarque les
polices et les illustrations en data: URI, place le contenu des 6 pages
dans des gabarits, et ajoute un routeur minimal qui les échange au clic.

Ne sert qu'à la prévisualisation — le vrai site reste multi-fichiers.
"""
import base64, pathlib, re

ROOT = pathlib.Path(__file__).parent
PAGES = ['index', 'a-propos', 'le-cabinet', 'massages', 'avis', 'contact']

# ---- polices ----
faces = []
for w in (400, 500, 600, 700):
    b64 = base64.b64encode((ROOT / f'assets/fonts/figtree-{w}-latin.woff2').read_bytes()).decode()
    faces.append("@font-face{font-family:'Figtree';font-style:normal;font-weight:%d;"
                 "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2');}" % (w, b64))

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
        return f'src="data:{MIME[f.suffix.lower()]};base64,{b64}"'
    return re.sub(r'src="(assets/img/[\w./-]+)"', sub, html)

css = (ROOT / 'assets/css/style.css').read_text(encoding='utf-8')
js  = (ROOT / 'assets/js/main.js').read_text(encoding='utf-8')

# ---- extraction des contenus ----
mains, titles = {}, {}
for name in PAGES:
    src = (ROOT / f'{name}.html').read_text(encoding='utf-8')
    mains[name] = inline_illus(re.search(r'<main id="main">(.*?)</main>', src, re.S).group(1))
    titles[name] = re.search(r'<title>(.*?)</title>', src, re.S).group(1)

shell = (ROOT / 'index.html').read_text(encoding='utf-8')
body = re.search(r'<body[^>]*>(.*)</body>', shell, re.S).group(1)
body = inline_illus(body)
body = body.replace('<script src="assets/js/main.js"></script>', '')
# le contenu de l'accueil est injecté par le routeur
body = re.sub(r'<main id="main">.*?</main>', '<main id="main"></main>', body, flags=re.S)

templates = '\n'.join(
    f'<template data-page="{n}.html" data-title="{titles[n]}">{mains[n]}</template>'
    for n in PAGES)

router = '''
/* Routeur d'aperçu — remplace la navigation entre fichiers, qu'un
   artifact ne peut pas servir. Le vrai site navigue normalement. */
(function () {
  const main = document.getElementById('main');
  const tpl  = {};
  document.querySelectorAll('template[data-page]').forEach(t => {
    tpl[t.dataset.page] = { html: t.innerHTML, title: t.dataset.title };
  });

  function show(page, animate) {
    const entry = tpl[page];
    if (!entry) return;
    const swap = () => {
      main.innerHTML = entry.html;
      document.title = entry.title;
      document.body.className = 'p-' + page.replace('.html', '');
      document.querySelectorAll('.nav__link, .footer__nav a').forEach(a => {
        const on = a.getAttribute('href') === page;
        if (on) a.setAttribute('aria-current', 'page');
        else a.removeAttribute('aria-current');
      });
      window.scrollTo(0, 0);
      document.body.classList.add('ready');
      window.marieMassage.initPage(main);
      requestAnimationFrame(() => document.body.classList.remove('leaving'));
    };
    if (animate) { document.body.classList.add('leaving'); setTimeout(swap, 280); }
    else swap();
  }

  document.addEventListener('click', e => {
    const a = e.target.closest('a[href$=".html"]');
    if (!a || !tpl[a.getAttribute('href')]) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    show(a.getAttribute('href'), true);
  }, true);

  show('index.html', false);
})();
'''

lock = ':root{color-scheme:light}\n:root[data-theme="dark"],:root[data-theme="light"]{color-scheme:light}'
out = (f"<title>Marie Massage — Masseuse bien-être</title>\n"
       f"<style>\n{chr(10).join(faces)}\n{lock}\n{css}\n</style>\n"
       f"{body}\n{templates}\n<script>\n{js}\n</script>\n<script>\n{router}\n</script>\n")

dest = pathlib.Path('/tmp/claude-0/-home-user-per-/0ab23514-8cad-52d4-a3c4-7a8a46290735/scratchpad/marie-massage.html')
dest.write_text(out, encoding='utf-8')
print(f'{len(PAGES)} pages embarquées — {round(len(out.encode())/1024)} Ko')
