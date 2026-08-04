# Marie Massage — site vitrine

Site vitrine statique pour **Marie Massage**, masseuse bien-être à Voisins-le-Bretonneux.

> ⚠️ **Version de base.** Tous les textes sont en lorem ipsum, les photos sont des
> placeholders gris et les tarifs sont notés `XX €`. Voir « À compléter » plus bas.

## Lancer le site en local

Aucune installation, aucune dépendance. Il suffit d'un serveur HTTP statique
(l'ouverture directe du fichier en `file://` bloque le chargement des polices) :

```bash
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

## Structure

```
index.html            page unique, 5 sections
assets/
  css/fonts.css       polices auto-hébergées (@font-face)
  css/style.css       styles + animations
  js/main.js          interactions
  fonts/              Playfair Display + Poppins (woff2, sous-ensembles latin)
  img/logo.svg        logo
  img/favicon.svg     favicon
```

Les sections suivent le parcours client : présentation de Marie → le cabinet →
les massages et tarifs → les avis → le contact.

## Charte graphique

| Couleur       | Hex       | Usage                                      |
| ------------- | --------- | ------------------------------------------ |
| Burgundy      | `#6B2E3A` | titres, textes importants, footer, contact |
| Tangerine     | `#F28C52` | boutons principaux, CTA, icônes            |
| Dusty Rose    | `#E98BA3` | accents, section avis                      |
| Pastel Yellow | `#F2E7B3` | fonds doux, surlignages                    |
| Desert Sage   | `#A7AE9B` | fond de la section « Le cabinet »          |
| Blanc cassé   | `#FAF8F4` | fond principal                             |

Typographie : **Playfair Display** (titres) + **Poppins** (texte courant).
Toutes les valeurs sont des variables CSS en haut de `style.css` — les changer
là suffit à répercuter partout.

Les polices sont auto-hébergées plutôt que chargées depuis le CDN Google Fonts :
c'est plus rapide, et cela évite le transfert d'adresses IP vers Google, que la
CNIL considère comme non conforme au RGPD.

## Ce qui est déjà en place

- Responsive (mobile, tablette, desktop) avec menu latéral sur mobile
- Animations : apparition au scroll, parallaxe, compteurs, curseur personnalisé,
  bandeau défilant, préchargeur
- Carrousel d'avis (flèches, points, lecture auto, swipe tactile)
- Formulaire de contact avec validation en direct
- Accessibilité : navigation clavier, libellés ARIA, lien d'évitement,
  respect de `prefers-reduced-motion`

## À compléter

- [ ] **Textes** — remplacer tout le lorem ipsum (présentation, cabinet, soins)
- [ ] **Photos** — remplacer les placeholders `.ph` par de vraies `<img>`
      (dimensions indicatives affichées dans chaque placeholder)
- [ ] **Tarifs et durées** — les `XX €` dans la section massages
- [ ] **Avis** — les témoignages sont des exemples, à remplacer par les vrais
- [ ] **Coordonnées** — téléphone et email sont des valeurs fictives
- [ ] **Envoi du formulaire** — aujourd'hui la soumission est simulée côté
      navigateur : **aucun email n'est réellement envoyé**. Il faut brancher un
      service (Formspree, Netlify Forms, EmailJS…) à l'endroit marqué `TODO`
      dans `assets/js/main.js`.
- [ ] **Mentions légales / politique de confidentialité** — obligatoires
- [ ] **Carte cadeau** — actuellement un simple encart « bientôt »

## Hébergement

Le site étant entièrement statique, il se déploie tel quel sur Netlify, Vercel,
GitHub Pages ou tout hébergement classique — rien à construire au préalable.
