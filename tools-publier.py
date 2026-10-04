#!/usr/bin/env python3
"""Prépare la version en ligne du site dans `_site/`, pour GitHub Pages.

Le dépôt contient bien plus que le site : les photos originales en haute
définition, les outils, les brouillons, les sources de Marie. Rien de tout
cela n'a à être en ligne. Ce script ne copie que ce que les pages utilisent
vraiment — il le trouve en lisant les pages, les feuilles de style et le
script, pas dans une liste tenue à la main qui finirait par mentir.

Il refuse de publier tant qu'une donnée d'exemple (`class="fictif"`)
reste dans une page : les mentions légales en portent tant que Marie n'a
pas donné les siennes.

Il fait aussi trois retouches, sur la copie seulement :

- l'adresse du site est écrite partout où elle apparaît (partage, Google,
  plan du site, robots) à partir de `DOMAINE`, et un fichier `CNAME` la
  déclare à GitHub ;
- le lien de retour de la page 404 suit (`/per-/` sans domaine, `/` avec) ;
- les commentaires du HTML et du CSS sont retirés : ce sont des notes de
  travail, qui pèsent et n'ont rien à faire dans la page d'une cliente.

Seule la bibliothèque standard est utilisée : le script tourne tel quel
sur GitHub, à chaque publication (voir `.github/workflows/publier.yml`).

    python3 tools-publier.py
"""
import pathlib
import re
import shutil
import sys

# Le nom de domaine acheté chez OVH, sans « https:// » ni « www » — par
# exemple 'mariemassage.fr'. Tant qu'il vaut None, le site est publié à
# l'adresse GitHub par défaut.
DOMAINE = 'marieemassage.com'

ROOT   = pathlib.Path(__file__).parent
SORTIE = ROOT / '_site'

ANCIENNE_ADRESSE = 'https://sringot.github.io/per-/'
ADRESSE = f'https://{DOMAINE}/' if DOMAINE else ANCIENNE_ADRESSE
RACINE  = '/' if DOMAINE else '/per-/'

PAGES  = ['index.html', 'mentions-legales.html', '404.html', 'robots.txt', 'sitemap.xml']
TEXTES = {'.html', '.css', '.js', '.txt', '.xml', '.json', '.svg'}

# Tout chemin `assets/…` écrit dans une page ou un script.
CHEMIN = re.compile(r'''assets/[\w./-]+\.\w+''')
# `url(...)` dans une feuille de style, relatif à celle-ci.
URL_CSS = re.compile(r'''url\(\s*['"]?(?!data:|https?:|#|%23)([^'")]+)['"]?\s*\)''')


def references():
    """Les fichiers d'`assets/` dont le site a besoin, de proche en proche."""
    a_voir = [ROOT / p for p in PAGES]
    vus, besoins = set(), set()
    while a_voir:
        f = a_voir.pop()
        if f in vus or not f.exists():
            continue
        vus.add(f)
        if f.suffix not in TEXTES:
            continue
        # Lue telle qu'elle sera publiée, sans ses commentaires : une image
        # citée seulement dans une note (le portrait retiré de « Moi ») n'a
        # pas à partir en ligne.
        texte = retouche(f, f.read_text(encoding='utf-8'))
        trouves = {ROOT / m for m in CHEMIN.findall(texte)}
        if f.suffix == '.css':
            trouves |= {(f.parent / m).resolve() for m in URL_CSS.findall(texte)}
        for t in trouves:
            besoins.add(t)
            a_voir.append(t)
    return besoins


def retouche(chemin, texte):
    texte = texte.replace(ANCIENNE_ADRESSE, ADRESSE)
    if chemin.name == '404.html':
        texte = texte.replace('href="/per-/"', f'href="{RACINE}"')
    if chemin.suffix == '.html':
        texte = re.sub(r'<!--.*?-->', '', texte, flags=re.S)
    elif chemin.suffix == '.css':
        texte = re.sub(r'/\*.*?\*/', '', texte, flags=re.S)
    if chemin.suffix in {'.html', '.css'}:
        texte = re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+', '\n\n', texte)
    # Les rappels « TODO : remplacer le domaine » n'ont plus lieu d'être.
    texte = re.sub(r'^#\s*TODO.*\n', '', texte, flags=re.M)
    return texte


def main():
    if SORTIE.exists():
        shutil.rmtree(SORTIE)
    SORTIE.mkdir()

    # Des données d'exemple (`class="fictif"`, dans les mentions légales)
    # ne doivent jamais partir en ligne : on s'arrête avant de publier.
    # Comptées sur le texte tel qu'il sera publié, sans ses commentaires :
    # la note qui explique la règle ne doit pas la déclencher.
    fictives = {pg: retouche(ROOT / pg, (ROOT / pg).read_text(encoding='utf-8'))
                    .count('class="fictif"')
                for pg in PAGES if (ROOT / pg).suffix == '.html'}
    fictives = {pg: n for pg, n in fictives.items() if n}
    if fictives:
        sys.exit('publication refusée — données fictives à remplacer : '
                 + ', '.join(f'{pg} ({n})' for pg, n in fictives.items()))

    besoins = references()
    manquants = sorted(str(b.relative_to(ROOT)) for b in besoins if not b.exists())
    if manquants:
        sys.exit('fichiers référencés introuvables :\n  ' + '\n  '.join(manquants))

    total = 0
    for f in [ROOT / p for p in PAGES] + sorted(besoins):
        cible = SORTIE / f.relative_to(ROOT)
        cible.parent.mkdir(parents=True, exist_ok=True)
        if f.suffix in TEXTES:
            cible.write_text(retouche(f, f.read_text(encoding='utf-8')), encoding='utf-8')
        else:
            shutil.copyfile(f, cible)
        total += cible.stat().st_size

    # GitHub ne doit pas passer le site à Jekyll, et doit connaître le domaine.
    (SORTIE / '.nojekyll').write_text('')
    if DOMAINE:
        (SORTIE / 'CNAME').write_text(DOMAINE + '\n')

    fichiers = sum(1 for p in SORTIE.rglob('*') if p.is_file())
    print(f'{fichiers} fichiers, {total / 1024:.0f} Ko → {SORTIE.name}/  (adresse : {ADRESSE})')


if __name__ == '__main__':
    main()
