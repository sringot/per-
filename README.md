# Marie Massage — site vitrine

Site vitrine statique pour **Marie Massage**, masseuse bien-être à Voisins-le-Bretonneux.

> ⚠️ **Version de base.** Tous les textes sont en lorem ipsum et les tarifs sont
> notés `XX €`. Les visuels, eux, sont définitifs : ce sont des illustrations
> vectorielles, pas des placeholders. Voir « À compléter » plus bas.

## Lancer le site en local

Aucune installation, aucune dépendance. Il suffit d'un serveur HTTP statique
(l'ouverture directe du fichier en `file://` bloque le chargement des polices) :

```bash
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

## Structure

```
index.html            Accueil (page d'atterrissage : le héros)
a-propos.html         À propos
le-cabinet.html       Le cabinet
massages.html         Les massages & tarifs
avis.html             Avis clientes
contact.html          Contact & rendez-vous
assets/
  css/fonts.css       polices auto-hébergées (@font-face)
  css/style.css       styles + animations
  js/main.js          interactions
  fonts/              Figtree 300–800 (woff2, sous-ensembles latin)
  img/logo.svg        logo
  img/favicon.svg     favicon
  img/illus/          19 illustrations plates (SVG)
tools-illustrations.py  script qui régénère les illustrations
tools-logo.py           trace le pictogramme et mesure l'écart avec la référence
tools-build-pages.py    échafaudage ayant produit les 6 pages (déjà joué)
```

Le site est **multi-pages** : on atterrit sur l'accueil, et chaque onglet de la
navigation est un fichier `.html` à part. C'est plus léger à charger sur mobile,
et chaque page se travaille isolément.

L'en-tête et le pied de page sont **dupliqués dans les 6 fichiers** — c'est le
prix à payer pour un site statique sans outil de build. Si tu modifies la
navigation ou le pied de page, répercute-le dans les 6.

`tools-build-pages.py` a servi une seule fois à découper la page unique
d'origine. **Ne le relance pas** : il écraserait tes modifications. Les fichiers
`.html` sont désormais la source de vérité et s'éditent directement.

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
| Orange du logo | `#EC8448` | logo uniquement (relevé sur le fichier fourni) |

Typographie : **Figtree** pour tout (titres en 600, texte en 400).
Toutes les valeurs sont des variables CSS en haut de `style.css` — les changer
là suffit à répercuter partout.

La page occupe toute la fenêtre, sans cadre ni bloc flottant. La largeur utile
(`--shell`, 1460 px) suit l'écran : le titre et le texte du héros grandissent
avec, pour ne pas laisser le contenu flotter au milieu d'un écran large.

Les polices sont auto-hébergées plutôt que chargées depuis le CDN Google Fonts :
c'est plus rapide, et cela évite le transfert d'adresses IP vers Google, que la
CNIL considère comme non conforme au RGPD.

## Ce qui est déjà en place

- Responsive (mobile, tablette, desktop) avec menu latéral sur mobile
- Animations : apparition au scroll, parallaxe, compteur, défilement inertiel,
  boutons magnétiques, préchargeur
- Carrousel d'avis (flèches, points, lecture auto, swipe tactile)
- Formulaire de contact avec validation en direct
- Accessibilité : navigation clavier, libellés ARIA, lien d'évitement,
  respect de `prefers-reduced-motion`

## Les illustrations

Le site n'utilise pas de photos : chaque visuel est une **illustration
vectorielle plate** aux couleurs de la marque (`assets/img/illus/`). C'est un
choix, pas un pis-aller — le site est complet dès maintenant, sans attendre de
séance photo, et l'univers visuel appartient à Marie Massage.

Elles sont générées par `tools-illustrations.py`, qui partage une palette et des
primitives communes (tête, main, feuille, bougie, flacon) pour que les 19 scènes
restent cohérentes entre elles. Pour ajuster une couleur ou une scène, modifier
le script puis le relancer :

```bash
python3 tools-illustrations.py
```

Si de vraies photos arrivent plus tard, il suffit de remplacer le `src` des
balises `<img>` dans `index.html` : la mise en page ne bouge pas, `.ill img`
applique déjà `object-fit: cover`.

## Le logo

Le logo de référence fourni par la cliente est dans
`assets/img/logo-reference.png`. Il n'est pas utilisé tel quel : c'est une
capture d'écran de 149 × 184 px, qui serait floue sur écran haute densité et
traînerait son fond crème. Le pictogramme est donc **redessiné en SVG**
(`assets/img/logo.svg`, et inline dans les pages).

Le tracé n'est pas fait à l'œil : `tools-logo.py` relève la silhouette de la
référence ligne par ligne, en déduit les coordonnées, puis **mesure le
recouvrement** entre le rendu et l'original (92 % actuellement — le reste est
le flou de la capture). Relancer le script après toute retouche du tracé.

Couleurs, relevées au pixel :

- pictogramme et nom « MARIE MASSAGE » : `#EC8448` (variable `--brand`)
- sous-titre « Masseuse bien-être » : gris, comme dans l'original

## À compléter

- [ ] **Textes** — remplacer tout le lorem ipsum (présentation, cabinet, soins)
- [ ] **Photos** — optionnel : les illustrations peuvent rester telles quelles,
      ou céder la place aux vraies photos (voir « Les illustrations »)
- [ ] **Tarifs et durées** — les `XX €` dans la section massages
- [ ] **Avis** — les témoignages sont des exemples, à remplacer par les vrais
- [ ] **Coordonnées** — téléphone et email sont des valeurs fictives
- [ ] **Envoi du formulaire** — aujourd'hui la soumission est simulée côté
      navigateur : **aucun email n'est réellement envoyé**. Il faut brancher un
      service (Formspree, Netlify Forms, EmailJS…) à l'endroit marqué `TODO`
      dans `assets/js/main.js`.
- [ ] **Mentions légales / politique de confidentialité** — obligatoires
- [ ] **Carte cadeau** — actuellement un simple encart « bientôt »

## Outillage

`.claude/skills/ui-ux-pro-max/` est une base de règles UI/UX consultable hors ligne
(styles, palettes, appariements de polices, garde-fous d'accessibilité), installée
depuis [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill).
Python 3, aucune dépendance externe. Elle ne sert qu'à la conception : elle
n'entre pas dans le site livré.

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness" --design-system
```

## Hébergement

Le site étant entièrement statique, il se déploie tel quel sur Netlify, Vercel,
GitHub Pages ou tout hébergement classique — rien à construire au préalable.
