#!/usr/bin/env python3
"""Ajoute au site, à chaque publication, les derniers avis Google de Marie.

Lancé par la publication (`.github/workflows/publier.yml`), juste après
`tools-publier.py`, et chaque matin par la même publication programmée :
il lit les avis de la fiche Google de Marie et ajoute en tête de la liste
de `_site/index.html` ceux qui n'y sont pas encore. La page calcule ensuite
seule la moyenne, les étoiles et les barres du résumé.

Ce que Google donne, et ce qu'on en fait :

- **Cinq avis au plus** — les plus récents ou les plus pertinents, au choix
  de Google. Les avis recopiés à la main dans `index.html` restent : c'est
  là qu'on garde pour de bon un avis qu'on veut voir durer.
- **Le texte original, mot pour mot**, comme les avis recopiés ; seules les
  apostrophes deviennent typographiques. Le nom est réduit au prénom et à
  l'initiale, comme les autres.
- **Tous les avis**, quelle que soit la note : n'afficher que les bons
  serait trompeur (Code de la consommation, art. L111-7-2).
- Rien n'est enregistré dans le dépôt : les avis sont relus à chaque
  publication, ce que demandent les conditions de Google.

Il ne bloque jamais la publication : sans clé, ou si Google ne répond pas,
le site part avec les avis qu'il a déjà.

Réglage, une fois (voir le README) : une clé « Places API (New) » dans les
secrets du dépôt, sous le nom GOOGLE_PLACES_KEY.

    GOOGLE_PLACES_KEY=… python3 tools-avis-google.py
    python3 tools-avis-google.py --essai reponse.json    (sans Google)
"""
import html
import json
import os
import pathlib
import re
import sys
import unicodedata
import urllib.request

ROOT = pathlib.Path(__file__).parent
PAGE = ROOT / '_site' / 'index.html'

# L'identifiant de la fiche Google de Marie. S'il est vide, le script la
# cherche par son nom et l'écrit dans le journal de la publication : on le
# recopie alors ici, pour ne plus dépendre d'une recherche.
PLACE_ID = os.environ.get('GOOGLE_PLACE_ID', '')
RECHERCHE = 'marieemassage Montigny-le-Bretonneux'

API = 'https://places.googleapis.com/v1'


def appel(url, cle, champs, corps=None):
    req = urllib.request.Request(
        url, data=json.dumps(corps).encode() if corps else None,
        headers={'X-Goog-Api-Key': cle, 'X-Goog-FieldMask': champs,
                 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def avis_google(cle):
    place = PLACE_ID
    if not place:
        trouve = appel(f'{API}/places:searchText', cle,
                       'places.id,places.displayName,places.formattedAddress',
                       {'textQuery': RECHERCHE, 'languageCode': 'fr'}).get('places', [])
        if not trouve:
            raise RuntimeError(f'aucune fiche trouvée pour « {RECHERCHE} »')
        p = trouve[0]
        place = p['id']
        print(f"fiche trouvée : {p.get('displayName', {}).get('text')} — "
              f"{p.get('formattedAddress')} — PLACE_ID = {place}")
    return appel(f'{API}/places/{place}?languageCode=fr', cle, 'reviews').get('reviews', [])


def cle_texte(t):
    """Pour reconnaître un avis déjà présent : lettres seules, sans accents."""
    t = unicodedata.normalize('NFKD', html.unescape(re.sub(r'<[^>]+>', ' ', t)))
    return re.sub(r'[^a-z0-9]', '', t.encode('ascii', 'ignore').decode().lower())


def nom_court(nom):
    mots = nom.split()
    if len(mots) < 2:
        return nom
    return f'{mots[0]} {mots[-1][0].upper()}.'


def li(avis):
    note = max(1, min(5, int(avis.get('rating', 5))))
    texte = (avis.get('originalText') or avis.get('text') or {}).get('text', '').strip()
    texte = html.escape(texte.replace("'", '’'), quote=False).replace('\n', '<br>')
    nom = html.escape(nom_court(avis.get('authorAttribution', {}).get('displayName', 'Cliente')))
    etoiles = '★' * note + '☆' * (5 - note)
    return (f'      <li data-note="{note}">\n'
            f'        <span class="avis__etoiles" role="img" aria-label="{note} étoile{"s" if note > 1 else ""} sur 5">{etoiles}</span>\n'
            f'        <q>{texte}</q>\n'
            f'        <cite><b>{nom}</b> · sur Google</cite>\n'
            f'      </li>\n')


def main():
    if '--essai' in sys.argv:
        avis = json.loads(pathlib.Path(sys.argv[sys.argv.index('--essai') + 1]).read_text())['reviews']
    else:
        cle = os.environ.get('GOOGLE_PLACES_KEY')
        if not cle:
            print('avis Google : pas de clé (GOOGLE_PLACES_KEY), le site garde ses avis.')
            return
        try:
            avis = avis_google(cle)
        except Exception as e:  # le site part quand même
            print(f'avis Google : lecture impossible ({e}), le site garde ses avis.')
            return

    if not PAGE.exists():
        print('avis Google : pas de site à compléter (lancer tools-publier.py avant).')
        return
    page = PAGE.read_text(encoding='utf-8')
    debut = page.find('<ul class="avis" id="avis-liste">')
    if debut < 0:
        print('avis Google : liste des avis introuvable dans la page.')
        return
    fin = page.find('</ul>', debut)
    presents = [cle_texte(q) for q in re.findall(r'<q>(.*?)</q>', page[debut:fin], re.S)]

    nouveaux = []
    for a in sorted(avis, key=lambda a: a.get('publishTime', ''), reverse=True):
        texte = (a.get('originalText') or a.get('text') or {}).get('text', '')
        k = cle_texte(texte)
        # Un avis sans texte (des étoiles seules) n'a rien à montrer ici.
        # Déjà présent : même début de texte — les avis recopiés à la main
        # sont parfois coupés (« […] »), on compare donc les 40 premiers signes.
        if not k or any(k[:40] == p[:40] for p in presents):
            continue
        nouveaux.append(li(a))
        presents.append(k)

    if nouveaux:
        coupe = page.index('>', debut) + 1
        page = page[:coupe] + '\n' + ''.join(nouveaux) + page[coupe:].lstrip('\n')
        PAGE.write_text(page, encoding='utf-8')
    print(f'avis Google : {len(avis)} lus, {len(nouveaux)} ajoutés.')


if __name__ == '__main__':
    main()
