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
| `avis/index.html` | La page du QR code de la salle (marieemassage.com/avis/) : un merci et le bouton vers le formulaire d'avis Google. |
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
- **Le lien d'avis Google** : dans `avis/index.html`, seul endroit où il est
  écrit. Le QR imprimé ne change pas.
- **Le domaine** : une seule ligne, `DOMAINE` dans `tools-publier.py`.

## Publier

À chaque changement poussé sur la branche du site, GitHub publie tout seul
(`.github/workflows/publier.yml`). `tools-publier.py` rassemble dans
`_site/` **uniquement** les fichiers que les pages utilisent — ni les
originaux, ni les outils — y écrit l'adresse du site et retire les
commentaires de travail.

Réglage GitHub, une fois : *Settings › Pages › Source : GitHub Actions*,
et la branche autorisée dans *Settings › Environments › github-pages*.

## Les avis Google automatiques

Chaque matin, et à chaque publication, `tools-avis-google.py` lit les avis
de la fiche Google de Marie et ajoute au site ceux qu'il n'a pas encore.
Google n'en donne que **cinq**, les plus récents ou pertinents : pour garder
un avis pour de bon, le recopier dans `index.html`. Treatwell n'a pas
d'accès de ce genre, ses avis se recopient à la main.

Réglage, une fois :

1. Sur console.cloud.google.com, avec le compte Google de Marie : créer un
   projet, activer la facturation (obligatoire chez Google ; une lecture par
   jour reste dans la part gratuite) et l'API **Places API (New)**.
2. *APIs & Services › Identifiants* : créer une **clé API**, la restreindre
   à *Places API (New)*. Dans *Quotas*, plafonner à 100 requêtes par jour.
3. Sur GitHub : *Settings › Secrets and variables › Actions › New
   repository secret*, nom `GOOGLE_PLACES_KEY`, valeur : la clé.
4. Lancer la publication (*Actions › Publication du site › Run workflow*) :
   le journal affiche la fiche trouvée et son `PLACE_ID`. Le mettre dans
   *Variables* sous le nom `GOOGLE_PLACE_ID`.

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
| `tools-carte-avis.js` | Carte A6 « Votre avis compte » avec le QR code, à imprimer pour la salle. | `sources/carte-avis-qr.svg` |
| `tools-preview.py` | Aperçu en un seul fichier autonome. | le site |
| `tools-publier.py` | Version en ligne, dans `_site/`. | le site |
| `tools-avis-google.py` | Ajoute les derniers avis Google à la version en ligne, à chaque publication et chaque matin. | la fiche Google de Marie |

Python 3 avec Pillow et NumPy ; Node avec Playwright pour les deux outils
`.js`.

## Ce qui reste à faire avant la mise en ligne

- Mentions légales : nom de famille, SIRET et adresse de Marie, téléphone
  de l'hébergeur.
