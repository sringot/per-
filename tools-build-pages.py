#!/usr/bin/env python3
"""Éclate le site en une page HTML par onglet.

Script d'échafaudage, lancé une seule fois : après quoi les fichiers .html
générés deviennent la source de vérité et s'éditent directement.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).parent
src = (ROOT / 'index.html').read_text(encoding='utf-8')

# ---------------------------------------------------------------- extraction
def grab(pattern):
    m = re.search(pattern, src, re.S)
    if not m:
        raise SystemExit('introuvable : ' + pattern[:60])
    return m.group(0)

hero    = grab(r'  <section class="hero" id="accueil">.*?\n  </section>')
marquee = grab(r'  <!-- ---------- BANDEAU DÉFILANT ---------- -->.*?\n  </div>')
apropos = grab(r'  <section class="section" id="apropos">.*?\n  </section>')
lieu    = grab(r'  <section class="section" id="lieu">.*?\n  </section>')
massages= grab(r'  <section class="section section--menu" id="massages">.*?\n  </section>')
avis    = grab(r'  <section class="section section--reviews" id="avis">.*?\n  </section>')
contact = grab(r'  <section class="section section--contact" id="contact">.*?\n  </section>')


def split_head(section):
    """Sort l'en-tête d'une section pour en faire l'en-tête de page."""
    m = re.search(r'      <header class="section__head[^"]*"[^>]*>(.*?)\n      </header>\n', section, re.S)
    if not m:
        return '', section
    return m.group(1).strip(), section.replace(m.group(0), '')


# ------------------------------------------------------------------- gabarit
NAV = [('index.html',      'Accueil'),
       ('a-propos.html',   'À propos'),
       ('le-cabinet.html', 'Le cabinet'),
       ('massages.html',   'Massages'),
       ('avis.html',       'Avis'),
       ('contact.html',    'Contact')]

MARK = '''<svg viewBox="0 0 100 100" aria-hidden="true">
            <circle cx="21" cy="17" r="11.5"/><circle cx="79" cy="17" r="11.5"/>
            <rect x="11.5" y="33" width="19" height="54" rx="9.5"/>
            <rect x="69.5" y="33" width="19" height="54" rx="9.5"/>
            <path d="M30 38 L50 68 L70 38" fill="none" stroke="currentColor" stroke-width="18"
                  stroke-linecap="round" stroke-linejoin="round"/>
          </svg>'''


def nav_items(current, cls='nav__link'):
    out = []
    for href, label in NAV[1:]:                      # « Accueil » vit dans le logo
        cur = ' aria-current="page"' if href == current else ''
        out.append(f'          <li><a href="{href}" class="{cls}"{cur}>{label}</a></li>')
    return '\n'.join(out)


def footer_items(current):
    out = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ''
        out.append(f'        <a href="{href}"{cur}>{label}</a>')
    return '\n'.join(out)


def layout(current, title, desc, body, preloader=False):
    pre = '''
<!-- ============ PRELOADER (accueil uniquement) ============ -->
<div class="preloader" id="preloader">
  <div class="preloader__logo">
    <svg viewBox="0 0 100 100" aria-hidden="true">
      <circle cx="21" cy="17" r="11.5"/><circle cx="79" cy="17" r="11.5"/>
      <rect x="11.5" y="33" width="19" height="54" rx="9.5"/>
      <rect x="69.5" y="33" width="19" height="54" rx="9.5"/>
      <path d="M30 38 L50 68 L70 38" fill="none" stroke="currentColor" stroke-width="18"
            stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>
  <span class="preloader__bar"><i></i></span>
</div>
''' if preloader else ''

    slug = current.replace('.html', '')
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">

  <link rel="preload" as="font" type="font/woff2" href="assets/fonts/figtree-400-latin.woff2" crossorigin>
  <link rel="preload" as="font" type="font/woff2" href="assets/fonts/figtree-700-latin.woff2" crossorigin>

  <link rel="stylesheet" href="assets/css/fonts.css">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body class="p-{slug}">
{pre}
<a class="skip-link" href="#main">Aller au contenu</a>

<div class="page">

  <!-- ---------- HEADER ---------- -->
  <header class="header" id="header">
    <div class="shell header__inner">

      <a href="index.html" class="brand" aria-label="Marie Massage — accueil">
        <span class="brand__mark">
          {MARK}
        </span>
        <span class="brand__text">
          <strong>Marie Massage</strong>
          <em>Masseuse bien-être</em>
        </span>
      </a>

      <nav class="nav" id="nav" aria-label="Navigation principale">
        <ul class="nav__list" id="navList">
          <span class="nav__pill" id="navPill" aria-hidden="true"></span>
{nav_items(current)}
        </ul>
        <a href="contact.html" class="btn btn--primary nav__cta-m">Prendre rendez-vous</a>
      </nav>

      <div class="header__end">
        <a href="contact.html" class="btn btn--primary magnetic nav__cta">
          <span>Prendre rendez-vous</span>
        </a>
        <button class="burger" id="burger" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="nav">
          <span></span><span></span><span></span>
        </button>
      </div>

    </div>
  </header>

<main id="main">

{body}

</main>

  <!-- ---------- FOOTER ---------- -->
  <footer class="footer">
    <div class="shell footer__inner">
      <a href="index.html" class="brand brand--footer">
        <span class="brand__mark">
          {MARK}
        </span>
        <span class="brand__text"><strong>Marie Massage</strong><em>Masseuse bien-être</em></span>
      </a>

      <nav class="footer__nav" aria-label="Navigation pied de page">
{footer_items(current)}
      </nav>

      <p class="footer__legal">
        © <span id="year">2026</span> Marie Massage · Voisins-le-Bretonneux<br>
        <small>Les massages proposés sont des soins de bien-être, non thérapeutiques.</small>
      </p>
    </div>
  </footer>

</div><!-- /.page -->

<a href="#main" class="totop" id="totop" aria-label="Remonter en haut">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5m0 0-6 6m6-6 6 6"/></svg>
</a>

<script src="assets/js/main.js"></script>
</body>
</html>
'''


def page_head(eyebrow, h1, intro):
    intro_html = f'\n      <p class="page-head__intro">{intro}</p>' if intro else ''
    return f'''  <header class="page-head">
    <span class="page-head__aura" aria-hidden="true"></span>
    <div class="shell">
      <p class="eyebrow reveal" style="--d:.05s">{eyebrow}</p>
      <h1 class="page-head__title"><span class="ln"><span style="--d:.12s">{h1}</span></span></h1>
      <div class="reveal" style="--d:.3s">{intro_html}
      </div>
    </div>
  </header>

'''


# --------------------------------------------------------------------- pages
BASE = 'Marie Massage, masseuse bien-être à Voisins-le-Bretonneux.'
pages = {}

# Accueil : le héros, rien d'autre — c'est une page d'atterrissage.
hero_home = hero.replace('href="#apropos" class="cue"', 'href="a-propos.html" class="cue"')
hero_home = hero_home.replace('href="#contact"', 'href="contact.html"')
hero_home = hero_home.replace('href="#massages"', 'href="massages.html"')
pages['index.html'] = (
    'Marie Massage — Masseuse bien-être à Voisins-le-Bretonneux',
    BASE + ' Kobido, madérothérapie, drainage lymphatique, massage bébé et relaxation.',
    hero_home + '\n\n' + marquee, True)

# À propos
_, ap = split_head(apropos)
pages['a-propos.html'] = (
    'À propos — Marie Massage',
    "Marie, masseuse bien-être à Voisins-le-Bretonneux : son parcours et sa façon de travailler.",
    page_head('À propos', "Prendre soin de vous,<br>c'est mon métier",
              'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas aliquam risus ut volutpat pretium.')
    + ap.replace('''        <p class="eyebrow">À propos</p>
        <h2 class="h2">Prendre soin de vous,<br>c'est mon métier</h2>
''', ''), False)

# Le cabinet
head_lieu, lieu_body = split_head(lieu)
pages['le-cabinet.html'] = (
    'Le cabinet — Marie Massage',
    'Le cabinet de Marie Massage à Voisins-le-Bretonneux : un cadre chaleureux et apaisant.',
    page_head('Le cabinet', 'Une parenthèse<br>hors du temps',
              'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas aliquam risus ut volutpat pretium, nunc velit tincidunt orci vitae dictum.')
    + lieu_body, False)

# Massages
head_mas, mas_body = split_head(massages)
pages['massages.html'] = (
    'Les massages & tarifs — Marie Massage',
    'Kobido, madérothérapie, relaxation, drainage lymphatique, massage bébé, dos & nuque : les soins et leurs tarifs.',
    page_head('Les massages', 'Choisissez<br>votre soin',
              'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Chaque soin est adapté à vos besoins du moment.')
    + mas_body, False)

# Avis
head_avis, avis_body = split_head(avis)
pages['avis.html'] = (
    'Avis clientes — Marie Massage',
    'Les retours des clientes de Marie Massage à Voisins-le-Bretonneux.',
    page_head('Retours clientes', 'Elles en parlent<br>mieux que moi', '')
    + avis_body, False)

# Contact
pages['contact.html'] = (
    'Contact & rendez-vous — Marie Massage',
    'Prendre rendez-vous avec Marie Massage à Voisins-le-Bretonneux.',
    contact.replace('''        <p class="eyebrow">Contact</p>
        <h2 class="h2">Prenons<br>rendez-vous</h2>''',
                    '''        <p class="eyebrow">Contact</p>
        <h1 class="h2">Prenons<br>rendez-vous</h1>'''), False)

for name, (title, desc, body, pre) in pages.items():
    # Les ancres internes deviennent des liens de page
    body = (body.replace('href="#contact"', 'href="contact.html"')
                .replace('href="#massages"', 'href="massages.html"')
                .replace('href="#apropos"', 'href="a-propos.html"')
                .replace('href="#lieu"', 'href="le-cabinet.html"')
                .replace('href="#avis"', 'href="avis.html"'))
    (ROOT / name).write_text(layout(name, title, desc, body, pre), encoding='utf-8')
    print(f'  {name:18} {len(body):>6} caractères de contenu')

print(f'\n{len(pages)} pages générées.')
