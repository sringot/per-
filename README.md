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
  img/logo-mark.png   pictogramme (découpé dans le logo fourni) — le logo
  img/logo-text.png   nom + sous-titre — plus inséré, tenu à jour au cas où
  img/favicon*.png    favicons (onglet + écran d'accueil iOS)
  img/illus/          19 illustrations plates (SVG)
tools-illustrations.py  script qui régénère les illustrations
tools-logo.py           découpe le pictogramme de logov2.png et fait les favicons
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
droite. Les panneaux partagent la couleur du fond, les creux servent aux blocs
en retrait, et les boutons s'enfoncent au clic.

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
  boutons magnétiques
- Navigation immédiate : aucun délai n'est ajouté au passage d'une page à
  l'autre (voir « Le passage d'une page à l'autre »)
- Carrousel d'avis (flèches, points, lecture auto, swipe tactile)
- Page avis : les 6 premiers témoignages affichés, les suivants repliés
  derrière « Voir tous les avis »
- Page contact tournée vers l'appel : le numéro en grand, cliquable
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

## Le menu mobile

En dessous de 1000 px, la navigation devient un tiroir latéral. Deux pièges
s'y sont cachés longtemps — les noter évite de les réintroduire :

**Le fond doit être figé en passant `<body>` en position fixe**, pas avec
`overflow:hidden`. C'est `<html>` qui défile, pas `<body>` : la règle ne
verrouillait rien. Pire, elle faisait de `<body>` un conteneur de défilement,
et l'en-tête `sticky` s'y accrochait — il partait donc hors de l'écran avec le
contenu, emportant le bouton qui sert à refermer le menu. Le JS mémorise la
position défilée, la pose en `top` négatif, et la restitue à la fermeture
(en `behavior:'instant'`, sinon `scroll-behavior:smooth` la fait glisser à vue).

**`.page` ne doit pas rester un contexte d'empilement.** Son animation
d'entrée était en `animation-fill-mode: both`, ce qui garde l'animation
d'opacité appliquée une fois finie — et une opacité animée crée un contexte
d'empilement permanent. L'en-tête et le tiroir s'y trouvaient enfermés au
niveau 0, donc **sous** le voile du menu (`z-index:940`), quel que soit le
`z-index` du header : on ne fait pas sortir un descendant du contexte de son
ancêtre. `backwards` pose l'état de départ avant l'animation puis rend la main.

L'ordre d'empilement attendu, une fois cela réglé : voile 940 < tiroir 950 <
en-tête et bouton 960. Un appui sur le voile referme le tiroir.

## Le passage d'une page à l'autre

Le site est multi-pages : chaque onglet est un vrai chargement. Trois délais
s'y étaient ajoutés, pour un temps perçu d'**une seconde** — mesuré à 1024 ms
vers une page, 1368 ms au retour sur l'accueil :

| Délai                                  | Coût     |
| -------------------------------------- | -------- |
| fondu de sortie retenant la navigation | 280 ms   |
| animation d'entrée (fondu + glissement)| 600 ms   |
| préchargeur rejoué à chaque retour     | ~1100 ms |

Les trois sont retirés ou réduits :

- **Le clic ne retient plus rien.** Le fondu de sortie imposait 280 ms
  d'attente avant même que le navigateur commence à charger — du temps ajouté
  pour masquer du temps.
- **L'animation d'entrée** passe de 600 ms avec glissement à un fondu de
  200 ms. Longue et mobile, elle se lisait comme un chargement alors que la
  page était déjà là.
- **Le préchargeur ne joue qu'à la première arrivée** de la session
  (`sessionStorage`). Revenir sur l'accueil le rejouait pour masquer un
  chargement déjà terminé.

Résultat mesuré : **336 ms** vers une page, **282 ms** au retour sur l'accueil.

## La prise de rendez-vous

Les rendez-vous se prennent **uniquement par téléphone**. La page contact est
donc bâtie autour de l'appel : le numéro en grand, en `tel:` — un appui suffit
depuis un mobile — et les horaires juste dessous.

Le formulaire de contact qui occupait cette place a été **retiré**, pas
seulement masqué : il ne pouvait pas prendre de rendez-vous et laissait croire
le contraire (sa soumission était simulée, aucun email n'était envoyé). Son
CSS et son module JS sont partis avec lui.

L'email reste affiché, mais présenté comme ce qu'il est — « une question ? »,
pas un canal de réservation.

## Les chiffres affichés

Aucune statistique n'est écrite en dur : **rien n'est inventé**. La note
moyenne et le nombre d'avis de la page « Avis » sont recalculés au chargement
à partir des témoignages réellement présents dans `avis.html`. Chaque
témoignage porte sa note :

```html
<figure class="rev" data-note="5"> … </figure>
```

Ajouter, retirer ou renoter un témoignage suffit : la synthèse suit. Les avis
au-delà des six premiers portent la classe `rev--extra` et l'attribut `hidden` ;
le bouton « Voir tous les avis » les déplie.

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

Le logo, lui, n'a plus de texte : c'est le pictogramme seul, à l'ocre — donc
au même rapport que les intitulés.

## Le logo

Le pictogramme vient de `logov2.png` (1024 × 1536). Il est **découpé dans le
fichier fourni**, jamais redessiné.

Ce fichier a un **fond opaque** : le M orange est posé sur un halo de la même
couleur. Un détourage par couleur ne marche donc pas — juste au contact du M,
le fond est aussi orange que lui :

| Zone              | Couleur         |
| ----------------- | --------------- |
| intérieur du M    | `(254, 93, 40)` |
| halo au contact   | `(250, 101, 48)` |
| fond lointain     | `(147, 113, 77)` |

La seule frontière est le **filet plus sombre** qui cerne le pictogramme, lui
bien tranché : `(255, 69, 15)`, un bleu deux fois plus bas que partout ailleurs.
`tools-logo.py` s'en sert comme d'une digue — un remplissage lancé depuis un
coin de l'image inonde tout l'extérieur sans pouvoir la franchir, et ce que le
remplissage n'atteint pas est le pictogramme.

```bash
python3 tools-logo.py
```

| Fichier             | Contenu                        | Poids   |
| ------------------- | ------------------------------ | ------- |
| `logo-mark.png`     | pictogramme seul, 281 × 300    | 6,9 Ko  |
| `logo-text.png`     | nom + sous-titre, 460 × 97     | 8,7 Ko  |
| `favicon.png`       | onglet, 32 × 32                | 1,4 Ko  |
| `favicon-180.png`   | écran d'accueil iOS, 180 × 180 | 9,7 Ko  |

Les fichiers sont écrits en PNG **à palette** (4 teintes × 64 opacités). Le logo
n'a qu'une ou deux couleurs, tout le dégradé est dans la transparence : en RGBA,
PNG dépense 4 octets par pixel et compresse mal ; indexé, il n'en dépense qu'un.
Le pictogramme passe de 17,6 à 6,9 Ko, pour un écart d'opacité plafonné à 3/255.

Seule la **silhouette** vient du fichier fourni : le pictogramme est reteinté
sur l'ocre du site (`--ochre`, `#AC4B28`). L'orange d'origine (`#FD5D28`)
jurait à côté des boutons, qui sont l'aplat le plus présent de la page.

Le site n'insère **que le pictogramme** — pas le nom. `logo-text.png` reste
généré et réaccordé sur la même teinte, pour qu'on puisse remettre le nom à
côté du M sans se retrouver avec deux oranges différents ; il n'est
aujourd'hui affiché nulle part. Le nom de la marque reste porté par le titre
de l'onglet et la ligne légale du pied de page.

Le favicon garde un fond crème arrondi : le pictogramme seul, tout en
transparence, se perdrait sur une barre d'onglets sombre. L'ancien
`favicon.svg` était un *tracé* du logo, pas le logo — il est supprimé.

## À compléter

- [ ] **Textes** — remplacer tout le lorem ipsum (présentation, cabinet, soins)
- [ ] **Photos** — optionnel : les illustrations peuvent rester telles quelles,
      ou céder la place aux vraies photos (voir « Les illustrations »)
- [ ] **Tarifs et durées** — les `XX €` dans la section massages
- [ ] **Avis** — les témoignages sont des exemples, à remplacer par les vrais
- [ ] **Coordonnées** — téléphone et email sont des valeurs fictives, à
      remplacer dans `contact.html` **et dans le pied de page des 6 pages**
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
