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

Langage visuel : **minimaliste + soft UI** (neumorphisme léger). Un seul fond
sur tout le site ; la profondeur ne vient plus des contours ni des aplats, mais
d'un relief discret — reflet clair en haut à gauche, ombre chaude en bas à
droite. Les panneaux partagent la couleur du fond, les champs de formulaire sont
creusés, les boutons s'enfoncent au clic.

Le socle `#F4F1E9` est un ton moyen et non du blanc : sans cela les reflets
clairs du relief ne se détachent pas.

> Le neumorphisme *franc* est écarté volontairement : il repose sur des écarts
> de luminosité trop faibles pour rester lisible. C'est sa variante accessible
> qui est appliquée (ombres douces multi-couches, rayons 8-12 px, animations
> 200-300 ms, contraste ≥ 4,5:1).

Trois familles de couleur seulement : **vert, orange, jaune**.
Le burgundy a été retiré (il tirait vers le prune sur les grands titres).

| Rôle           | Hex       | Usage                                        |
| -------------- | --------- | -------------------------------------------- |
| Vert profond   | `#3F4A38` | titres, textes forts, survols                |
| Orange (ocre)  | `#AC4B28` | boutons, CTA, icônes — **seul accent vif**   |
| Kaki           | `#9A8B5F` | petits détails, carte cadeau                 |
| Sauge          | `#A7AE9B` | petits détails, fond de section très dilué   |
| Jaune pastel   | `#F2E7B3` | dérivés dilués pour les fonds doux           |
| Socle          | `#F4F1E9` | fond unique, support du relief               |
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

## Contraste

Le Pantone Burnt Ochre à sa valeur exacte (`#C15A32`) tombe à 3,9:1 sur le socle
et 4,4:1 sous du texte blanc — sous le minimum de 4,5:1 pour du petit texte. Il
est donc approfondi d'un cran (`#AC4B28`), ce qui reste visuellement très proche.

Rapports mesurés sur le socle `#F4F1E9` :

| Rôle               | Rapport   |
| ------------------ | --------- |
| Texte courant      | 13,7:1    |
| Texte secondaire   | 4,9:1     |
| Titres (vert)      | 8,3:1     |
| Intitulés (ocre)   | 4,9:1     |
| Blanc sur bouton   | 5,5:1     |

Seul le nom « MARIE MASSAGE » du logo reste en dessous (2,3:1) : un nom de marque
échappe aux règles de contraste, et le sous-titre gris juste en dessous porte
l'information lisible.

## Le logo

Le logo fourni (`assets/img/logo-source.png`, 1024 × 1536, fond transparent) est
**inséré tel quel**, pas redessiné. Il est simplement découpé et optimisé pour
le web :

| Fichier           | Contenu                      | Poids   |
| ----------------- | ---------------------------- | ------- |
| `logo-mark.png`   | pictogramme seul             | 9,5 Ko  |
| `logo-text.png`   | nom + sous-titre             | 9,8 Ko  |
| `logo-full.png`   | verrou complet, à la verticale | 20,5 Ko |

Le fichier d'origine pèse 2 Mo : recadrage sur le contenu, redimensionnement et
quantification à 64 couleurs le ramènent à moins de 10 Ko sans perte visible —
l'image n'a que deux teintes plus l'anticrénelage.

Le verrou d'origine est **vertical** (pictogramme au-dessus du nom). Une barre
de navigation de 86 px ne peut pas l'accueillir à une taille lisible : le
pictogramme et le bloc texte sont donc découpés puis posés **côte à côte**. Les
pixels restent ceux du fichier fourni.

`tools-logo.py` (ancien tracé vectoriel) n'est plus utilisé par le site ; il est
conservé pour mémoire.

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
