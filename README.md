# marieemassage — site vitrine

Le site de **Marie**, masseuse bien-être à Montigny-le-Bretonneux :
kobido, massage relaxant, madérothérapie et drainage lymphatique, réservés
aux femmes. Adresse : **https://marieemassage.com** (hébergé sur GitHub
Pages, nom de domaine chez OVH).

Un site statique — du HTML, une feuille de style, un script — sans base de
données, sans formulaire et sans cookie. La réservation passe par
Treatwell et par SMS.

## Le site

| Fichier | Rôle |
| ------- | ---- |
| `index.html` | Tout le site : l'accueil et ses cinq rubriques (À propos, Le lieu, Massages, Avis, Rendez-vous), en panneaux qui s'ouvrent sur place. |
| `mentions-legales.html` | Les mentions légales. |
| `404.html` | La page « introuvable », autonome (styles inclus). |
| `assets/css/v2.css` | Toute la mise en forme — téléphone d'abord, puis « Grand écran » au-delà de 1024 px. |
| `assets/js/v2.js` | Ouverture des rubriques, fiches des massages, barre qui s'efface, calcul des prix et des avis. |
| `assets/img/`, `assets/fonts/` | Images et police (Figtree) utilisées par le site. |
| `robots.txt`, `sitemap.xml` | Pour les moteurs de recherche. |

Le code est commenté : chaque choix de mise en page y est expliqué à
l'endroit où il est fait.

## Modifier le contenu

- **Un prix** : dans le tableau caché des tarifs de `index.html`
  (`<div class="tarifs-source" hidden>`). Les fiches des massages le
  recopient, et les « au lieu de » des forfaits se calculent tout seuls.
- **La description d'un massage** : même tableau, ligne `t-desc` du soin.
- **Un avis** : ajouter un `<li data-note="5">` dans `#avis-liste`. La
  moyenne, les étoiles, les barres et le nombre d'avis se recalculent.
- **Le domaine** : une seule ligne, `DOMAINE` dans `tools-publier.py`.

## Publier

À chaque changement poussé sur la branche du site, GitHub publie tout seul
(`.github/workflows/publier.yml`). `tools-publier.py` rassemble dans
`_site/` **uniquement** les fichiers que les pages utilisent — ni les
originaux, ni les outils — y écrit l'adresse du site et retire les
commentaires de travail.

Réglage GitHub, une fois : *Settings › Pages › Source : GitHub Actions*,
et la branche autorisée dans *Settings › Environments › github-pages*.

## Les outils

Ils fabriquent les images du site à partir des originaux de `sources/`.
On ne les relance que si un original change.

| Outil | Ce qu'il fait | À partir de |
| ----- | ------------- | ----------- |
| `tools-photos.py` | Recadre et compresse les photos. | `sources/photos/` |
| `tools-cartes-images.py` | Cartes des massages, bandeaux et textures des fiches. | `sources/cartes/`, `sources/fonds/` |
| `tools-textures.py` | Fond blanc cassé des pages et touche terracotta. | `sources/pages/fond.png` |
| `tools-logo-officiel.py` | Logo détouré et favicons. | `sources/logo/logo-source.png` |
| `tools-partage.js` | Image de partage (WhatsApp, Instagram…). | les fichiers du site |
| `tools-cartes.py` | Monogrammes vectoriels, pour l'affiche. | `sources/cartes/reference-cartes-soins.png` |
| `tools-affiche.py` (+ `tools-affiche-pdf.js`, `tools_couleur.py`) | Affiche A4 des tarifs pour la pièce. | le site |
| `tools-preview.py` | Aperçu en un seul fichier autonome. | le site |
| `tools-publier.py` | Version en ligne, dans `_site/`. | le site |

Python 3 avec Pillow et NumPy ; Node avec Playwright pour les deux outils
`.js`.

## Ce qui reste à faire avant la mise en ligne

- Mentions légales : nom de famille, SIRET et adresse de Marie, téléphone
  de l'hébergeur.
