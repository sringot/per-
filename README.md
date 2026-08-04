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
  fonts/              Figtree 300–800 (woff2, sous-ensembles latin)
  img/logo.svg        logo
  img/favicon.svg     favicon
```

Les sections suivent le parcours client : présentation de Marie → le cabinet →
les massages et tarifs → les avis → le contact.

## Charte graphique

Le site est volontairement presque entièrement clair : la couleur ne sert que
pour les accents, pas en grands aplats.

Trois familles seulement : **vert, orange, jaune**, sur blanc cassé.
Le burgundy a été retiré (il tirait vers le prune sur les grands titres).

| Rôle           | Hex       | Usage                                        |
| -------------- | --------- | -------------------------------------------- |
| Vert profond   | `#3F4A38` | titres, textes forts, survols                |
| Orange (ocre)  | `#C15A32` | boutons, CTA, icônes — **seul accent vif**   |
| Kaki           | `#9A8B5F` | petits détails, carte cadeau                 |
| Sauge          | `#A7AE9B` | petits détails, fond de section très dilué   |
| Jaune pastel   | `#F2E7B3` | dérivés dilués pour les fonds doux           |
| Blanc cassé    | `#FBF9F4` | fond principal                               |
| Doré du logo   | `#D9B871` | logo uniquement                              |

Typographie : **Figtree** pour tout (titres en 600, texte en 400).
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

## Point d'attention : lisibilité du logo

Le logo fourni est doré clair. Posé sur le fond crème du site, ce doré ne
passe pas le contraste minimum pour du texte. Le pictogramme garde donc la
teinte d'origine (`#D9B871`), mais le nom « MARIE MASSAGE » et le sous-titre
utilisent une version assombrie du même doré (`--gold-ink`, `#A8823A`).
Pour revenir au doré exact, remplacer `--gold-ink` par `--gold` dans
`style.css` — au prix de la lisibilité.

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
