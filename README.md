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
  fonts/              Poppins 300–700 (woff2, sous-ensembles latin)
  img/logo.svg        logo
  img/favicon.svg     favicon
```

Les sections suivent le parcours client : présentation de Marie → le cabinet →
les massages et tarifs → les avis → le contact.

## Charte graphique

| Pantone            | Hex       | Usage                                        |
| ------------------ | --------- | -------------------------------------------- |
| 18-1354 Burnt Ochre| `#C15A32` | boutons principaux, CTA, logo, accents        |
| 19-1617 Burgundy   | `#6B2E3A` | titres, section contact, footer               |
| 17-0627 Dried Herb | `#9A8B5F` | encart carte cadeau, sous-titre de marque     |
| 16-0110 Desert Sage| `#A7AE9B` | fond de la section « Le cabinet »             |
| 11-0616 Pastel Yellow | `#F2E7B3` | cadre de page, fonds doux                  |
| Blanc cassé        | `#FCFBF8` | fond du grand bloc arrondi                    |

Typographie : **Poppins** pour tout (titres en 600, texte courant en 400).
Toutes les valeurs sont des variables CSS en haut de `style.css` — les changer
là suffit à répercuter partout.

La mise en page reprend le principe d'un grand bloc blanc arrondi posé sur un
fond jaune pastel, avec photo en arche et cartes flottantes.

Les polices sont auto-hébergées plutôt que chargées depuis le CDN Google Fonts :
c'est plus rapide, et cela évite le transfert d'adresses IP vers Google, que la
CNIL considère comme non conforme au RGPD.

## Ce qui est déjà en place

- Responsive (mobile, tablette, desktop) avec menu latéral sur mobile
- Animations : apparition au scroll, parallaxe, compteur, pastilles flottantes,
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
