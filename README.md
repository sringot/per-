# Marie Massage — site vitrine (V2, « les bulles »)

Site vitrine statique pour **Marie Massage**, masseuse bien-être à Voisins-le-Bretonneux.

> ⚠️ **En cours.** Les textes de présentation viennent de Marie ; il reste du
> lorem ipsum sur les avis et les descriptions de soins, et les tarifs sont
> notés `XX €`. Voir « À compléter » plus bas.

## Deux versions, deux branches

Marie a demandé un site plus radical : *« sur la page d'accueil juste un titre
et sa photo, des onglets sous forme de bulles imagées par des logos, un site
qui sort de l'ordinaire, très smooth, pas bourré d'informations »*. Plutôt que
d'écraser le premier site, chaque parti pris vit sur sa branche :

| Branche | Ce que c'est |
| ------- | ------------ |
| `claude/git-repo-access-ea5z33` | **V1** — site classique en 6 pages, en-tête, héros, sections. |
| `claude/v2-bulles` | **V2** — un seul écran : le pictogramme, la photo, `marieemassage`, cinq bulles. *(cette branche)* |

Les deux partagent la charte, les polices, la photo source et l'outillage. Une
idée de mise en forme adoptée d'un côté se transpose sans peine de l'autre.

## Le parti pris de la V2

Une page. Pas de défilement à l'accueil : tout tient dans la fenêtre, sur
téléphone comme sur écran large — **par la mise en page, pas par un verrou**.
Un `overflow:hidden` a existé un temps ; à 200 % de zoom, ou avec une police
système à 24 px, la composition dépasse la fenêtre et le verrou rendait alors
les bulles et le pied de page inatteignables, ni au doigt ni au clavier. Aux
tailles normales rien ne défile de toute façon. Les cinq rubriques sont
des **panneaux déjà présents dans le document**, masqués par `clip-path`, et
révélés au toucher : le disque de la bulle grandit jusqu'à remplir l'écran.
L'ouverture part donc **de l'endroit qu'on a touché**, pas du milieu de l'écran
— c'est là que se joue l'impression de fluidité.

Les panneaux restant dans le HTML, les moteurs de recherche lisent tout le
contenu sans exécuter une ligne de script ; `inert` les retire du clavier et
des lecteurs d'écran tant qu'ils sont fermés. Chaque panneau a son adresse
(`…/#massages`), partageable et compatible avec le bouton « retour ».

**La composition est décentrée.** La photo se pose à gauche, le nom et les
bulles la suivent ; le vide à droite est voulu, c'est lui qui donne au premier
regard son air de ne pas être une page d'accueil ordinaire.

Sur **téléphone**, les cinq bulles se rangent en **colonne contre la photo**,
et la photo **s'étire à la hauteur exacte de cette colonne** : haut contre
haut, bas contre bas. Elle passe de 253 × 279 à 273 × 385 px sur un écran de
390 — la moitié de surface en plus.

> L'égalité est obtenue par construction, pas par calcul : la colonne fixe la
> hauteur de la rangée, la photo la remplit. Un rapport d'image figé ne pouvait
> pas la garantir — la hauteur des bulles dépend de leur taille, celle de la
> photo de sa largeur, et les deux ne tombaient juste qu'à une largeur d'écran
> précise. Écart mesuré : **0 px**, de 280 à 430 px de large.

> Sur un écran court, c'est donc **la colonne** qu'il faut réduire, jamais la
> photo : la rétrécir en largeur pendant que sa hauteur restait celle des
> bulles la transformait en bandeau vertical, jusqu'à 1/2,3 sur un 320 × 568.

Au-delà de **700 px de large *et* 560 px de haut**, deux colonnes : le
pictogramme coiffe la photo à gauche, le nom et les bulles — remises en ligne —
occupent la droite. La double condition sépare une tablette, qui mérite cette
composition, d'un téléphone couché, qui est large mais court.

> Les surcharges « écran large » sont déclarées **après** les règles de base
> des bulles, et non dans la requête média du haut de la feuille : à
> spécificité égale c'est la dernière déclaration qui l'emporte, et la colonne
> du téléphone reprenait le dessus sur le desktop.

> La photo a **deux bornes**, pas une : `width: min(100%, 40vh)`. La largeur
> de sa colonne la dimensionne, mais sur un téléphone couché cette colonne est
> très large et la photo dépassait de 280 px. La hauteur d'écran est la
> seconde limite.

> Sur un écran court, le libellé passe **à côté** du rond au lieu de dessous :
> la colonne perd un tiers de sa hauteur et gagne une largeur dont on dispose
> justement en paysage.

## Lancer le site en local

Aucune installation, aucune dépendance. Il suffit d'un serveur HTTP statique
(l'ouverture directe du fichier en `file://` bloque le chargement des polices) :

```bash
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

## Structure

```
index.html            Le site entier : l'accueil + les cinq panneaux
mentions-legales.html Mentions légales (squelette — voir « À compléter »)
404.html              Page introuvable
robots.txt            indexation
sitemap.xml           plan du site
assets/
  css/fonts.css       polices auto-hébergées (@font-face)
  css/v2.css          styles, animations, panneaux
  js/v2.js            ouverture des panneaux, historique, synthèse des avis
  fonts/              Figtree variable 400-600 (woff2, latin + latin-ext)
  img/marie-hero*.webp portrait dans son arche (deux tailles)
  img/logo-mark.png   pictogramme, seul en-tête du site
  img/favicon*.png    favicons (onglet + écran d'accueil iOS)
  img/soins/*.svg     monogrammes des cinq cartes (masques, sans couleur)
tools-cartes.py       relève couleurs et monogrammes de la planche de soins
tools-photos.py       découpe le portrait aux formats du gabarit
tools-logo.py         découpe le pictogramme de logov2.png et fait les favicons
tools-preview.py      assemble tout en un fichier autonome (aperçu partageable)
```

Le site tient dans **un seul fichier HTML**. Pas d'en-tête à dupliquer, pas de
navigation à répercuter : ajouter une rubrique, c'est une bulle dans `<nav>` et
une `<section class="panneau">` plus bas, reliées par `data-ouvre` /
`id`. Le script ne connaît aucune liste de pages, il lit le document.

La feuille et le script de la V1 ont été **supprimés de cette branche** : plus
aucune page ne les chargeait, et 74 Ko de code mort finissent toujours par être
lus comme s'ils étaient vivants. Ils restent intacts sur la branche V1, et dans
l'historique.

## Charte graphique

Langage visuel : **minimaliste + soft UI** (neumorphisme léger). Un seul fond
sur tout le site ; la profondeur ne vient plus des contours ni des aplats, mais
d'un relief discret — reflet clair en haut à gauche, ombre chaude en bas à
droite. Les panneaux partagent la couleur du fond, les creux servent aux blocs
en retrait, et les boutons s'enfoncent au clic.

Le socle `#F4F1E9` est un ton moyen et non du blanc : sans cela les reflets
clairs du relief ne se détachent pas.

### Le fond n'est pas un aplat

Deux choses le tirent du côté de la matière.

**Un grain, sur tout le site.** Un aplat se lit comme une couleur ; il lui faut
un grain très fin — 3,5 % — pour passer pour du papier. On ne le voit pas ; on
voit qu'il manque quand on l'enlève. Le bruit est calculé par le navigateur
(`feTurbulence`) plutôt que servi en image : **300 octets** au lieu de plusieurs
dizaines de kilo-octets, et aucun motif qui se répète. Mesuré à processeur bridé
×6, il ne coûte rien — médiane d'image identique avec et sans, à 16,6 ms.

**Une image de fond.** Crèmes très doux, formes organiques et le pictogramme
en filigrane — fournie par Sacha (`fond-source.png`). Elle respire très
lentement : une dérive de quelques pourcents, en boucle.

> 1,6 Mo de PNG pour un dégradé. `tools-fond.py` la ramène à **6 Ko** en WebP,
> sans différence visible — un dégradé se compresse d'autant mieux qu'il est
> lisse. Le format téléphone reçoit sa **propre découpe verticale** : servie
> telle quelle, l'image paysage était agrandie 1,4× pour couvrir la hauteur et
> l'on n'en voyait plus qu'un tiers.

> L'image est **fixée à la fenêtre**, pas posée dans la scène. La scène est
> bornée à 1180 px : le fond s'y serait arrêté et les bords d'un grand écran
> seraient restés unis. Fixée, elle ne compte pas non plus dans le débordement
> de la page.

> La dérive porte sur `transform`, jamais sur l'image : déplacer une couche
> déjà dessinée ne coûte qu'une recomposition, la redessiner coûte une image
> entière.

**Le socle a suivi.** `--card` est désormais **relevé sur l'image** (sa teinte
médiane, `#FCF0E2`) et non choisi à part. Tout le langage de relief repose sur
des surfaces qui partagent la couleur du fond : resté au crème d'avant, plus
gris que l'image, chaque bulle se détachait comme un disque gris posé dessus
au lieu d'être creusée dans la page.

Contrastes relevés sur le rendu, aux points les plus teintés du fond : le texte
secondaire tient **5,5:1** et les titres **7,8:1**. L'image étant plus claire
que l'ancien socle, la lecture y gagne.

> Le neumorphisme *franc* est écarté volontairement : il repose sur des écarts
> de luminosité trop faibles pour rester lisible. C'est sa variante accessible
> qui est appliquée (ombres douces multi-couches, rayons 8-12 px, animations
> 200-300 ms, contraste ≥ 4,5:1).

Le socle est commun à tout le site, et deux couleurs y portent la structure :

| Rôle           | Hex       | Usage                                        |
| -------------- | --------- | -------------------------------------------- |
| Vert profond   | `#3F4A38` | titres, textes forts, survols                |
| Orange (ocre)  | `#AC4B28` | l'action — boutons, appel, bulle du rendez-vous |
| Encre          | `#2A2320` | texte courant                                |
| Encre douce    | `#635D57` | texte secondaire                             |
| Socle          | `#F4F1E9` | fond unique, support du relief               |

### Une couleur par rubrique

La planche des soins a apporté cinq teintes. Elles ne servent pas qu'aux
cartes : **chaque rubrique en porte une**, de sa bulle à son panneau. C'est ce
qui fait qu'on reconnaît une section avant même de l'avoir lue.

| Rubrique | Teinte | Tracés (≥ 3:1) | Petit texte (≥ 4,5:1) |
| -------- | ------ | -------------- | --------------------- |
| Moi         | bordeaux | `#7E3D49` | `#7E3D49` |
| Le lieu     | sauge    | `#898D7F` | `#67695F` |
| Massages    | jaune    | `#988968` | `#786C52` |
| Avis        | rose     | `#B37D79` | `#875E5B` |
| Rendez-vous | ocre     | `#AC4B28` | `#A24626` |

Deux valeurs par teinte, et elles sont **calculées, pas choisies** : les tons
bruts de la planche sont faits pour du texte blanc sur fond plein, pas pour du
tracé sur crème. La sauge y tombe à 2:1, le rose à 1,9:1, le jaune à 1,1:1 —
autant dire invisible. Chacune est donc foncée juste ce qu'il faut, du côté
opposé au fond, par le même calcul que celui des cartes.

> Les valeurs de texte sont calculées non pas sur le crème nu mais sur le
> **crème lavé de 13 % de la teinte** — celui du haut des panneaux. Le lavis
> assombrit le fond, et trois d'entre elles y retombaient à 4,1-4,2:1.

**Où la couleur apparaît, et où elle s'arrête.** Le disque des bulles reste
crème et ne prend que 8 % de sa teinte ; seul le tracé se colore. Cinq ronds
pleins et vifs sur la page d'accueil basculeraient du côté de l'application
pour enfants — et au-delà de ~10 %, le disque cesse de partager le fond, ce
qui fait tomber l'illusion de relief. Le panneau, lui, **s'ouvre dans sa
couleur** puis la laisse se retirer : on voit passer une teinte sans jamais
lire une page colorée. Il en reste un lavis en tête, assez faible pour ne pas
se voir et assez présent pour qu'« Avis » et « Le lieu » n'aient pas la même
température.

Typographie : **Figtree** pour tout (titres en 600, texte en 400).
Toutes les valeurs sont des variables CSS en haut de `v2.css` — les changer
là suffit à répercuter partout.

La page occupe toute la fenêtre, sans cadre ni bloc flottant. La largeur utile
(`--shell`, 1460 px) suit l'écran : le titre et le texte du héros grandissent
avec, pour ne pas laisser le contenu flotter au milieu d'un écran large.

Les polices sont auto-hébergées plutôt que chargées depuis le CDN Google Fonts :
c'est plus rapide, et cela évite le transfert d'adresses IP vers Google, que la
CNIL considère comme non conforme au RGPD.

## Ce qui est déjà en place

- Un écran unique qui ne défile pas, sur téléphone comme sur desktop : le
  pictogramme, la photo de Marie dans son arche, `marieemassage`, cinq bulles
- Composition décentrée : la photo à gauche, le nom et les bulles à sa suite
- Une couleur par rubrique, de la bulle au panneau, contrastes calculés
- Cinq bulles, la dernière (« Rendez-vous ») pleine et colorée : c'est l'action
  attendue, la prise de rendez-vous se faisant uniquement par téléphone
- Ouverture des panneaux en `clip-path`, ancrée sur la bulle touchée
- Panneau « Massages » : cinq cartes colorées qui se retournent au toucher
- Adresses partageables (`#massages`) et bouton « retour » du téléphone géré
- Note moyenne des avis **calculée** à partir des avis présents, jamais écrite
  en dur (voir « Les chiffres affichés »)
- Métadonnées de partage, JSON-LD, `robots.txt`, `sitemap.xml`, page 404
- Accessibilité : navigation clavier, `inert` sur les panneaux fermés, focus
  rendu à la bulle d'origine, lien d'évitement, `prefers-reduced-motion`

## Les cartes de soins

Le panneau « Massages » présente les cinq soins en cartes, reprises d'une
planche dessinée pour Marie (`reference-cartes-soins.png`) : une couleur par
soin, un monogramme dans l'esprit du logo — deux têtes rondes posées sur une
lettre pleine — et le nom en bas. **Un appui retourne la carte** et découvre la
description, la durée et le tarif.

Rien n'est relevé à l'œil : `tools-cartes.py` lit la planche et en tire tout.

```bash
python3 tools-cartes.py
```

**Les couleurs, à la médiane.** La planche est bruitée : sa couleur la plus
fréquente n'y représente que 6 à 14 % des pixels, si bien qu'un simple mode
attrape un grain plutôt qu'un ton. Chaque carte est donc séparée en deux
groupes — le fond et ce qui s'en éloigne — et chaque groupe rend sa médiane.

**Les monogrammes, vectorisés.** À 1799 px de large, la planche ne donne que
~150 px par monogramme : posé tel quel dans une carte de 220 px sur un écran
dense, il piquerait. Chaque silhouette est donc agrandie ×5, puis tracée par
`potrace`. Le résultat pèse quelques kilo-octets et ne pique jamais.

> Le vignettage de la planche passe le seuil sur les fonds sombres et laisse
> de longs filets verticaux au bord des cartes, qui se retrouvaient tracés à
> côté de la lettre. Ils sont fins mais hauts : une aire minimale absolue ne
> les distingue pas. C'est leur taille **relative** au monogramme qui les
> trahit — on ne garde que les taches d'au moins 4 % de la plus grande.

Les cinq silhouettes n'ont pas les mêmes proportions ; chacune est posée dans
une toile carrée, centrée. Sans cela elles paraîtraient de tailles
différentes, comme des capitales de hauteurs inégales.

**Le monogramme est un masque CSS, pas une image.** Le fichier SVG ne porte
aucune couleur : c'est le CSS qui la donne, via `mask`. Changer une teinte se
fait donc dans `v2.css`, sans retoucher un seul dessin.

**Le contraste est recalculé.** Sur la planche, trois cartes sur cinq écrivent
leur nom autour de 2:1 — très en dessous des 4,5:1 exigés pour du petit texte.
La grande forme du monogramme garde sa couleur d'origine, mais le texte reçoit
la **même teinte poussée** jusqu'au seuil, du côté opposé au fond :

| Carte | Fond | Monogramme | Texte | Après |
| ----- | ---- | ---------- | ----- | ----- |
| Kobido               | `#7E3D49` | `#F8E2AF` (6,2:1) | inchangé  | —     |
| Relaxant             | `#A9AE9D` | `#707550` (2,1:1) | `#3F422D` | 4,5:1 |
| Deep Tissus          | `#FAE1AB` | `#D59C40` (1,9:1) | `#825F27` | 4,5:1 |
| Madéro               | `#D15929` | `#FDF5E8` (3,8:1) | `#141413` | 4,5:1 |
| Drainage lymphatique | `#E39E99` | `#BF585A` (2,0:1) | `#6B3132` | 4,6:1 |

> Sur l'orange, éclaircir plafonne à 4,1:1 **même en blanc pur** : c'est la
> seule carte où il faut assombrir. Les deux directions sont donc essayées, et
> on retient celle qui atteint la cible en s'écartant le moins de la teinte.

**Le retournement.** Tout l'état tient dans `aria-expanded` : le CSS s'en sert
pour la rotation, un lecteur d'écran y lit la même chose que ce qu'on voit. La
perspective est portée par le conteneur et la rotation par la carte — sur le
même élément, la perspective s'appliquerait à la carte elle-même et le
retournement paraîtrait plat. `backface-visibility` cache la face arrière à
l'œil ; `visibility`, retardée jusqu'au milieu du mouvement, la cache aussi
aux lecteurs d'écran.

**Le mouvement complet.** Une rotation seule paraît plate. La carte
s'**élève** vers l'œil pendant qu'elle tourne, puis se repose — le geste de
quelqu'un qui prend une carte, la retourne, et la remet sur la table. Trois
choses l'accompagnent : l'ombre s'agrandit et s'adoucit avec la hauteur, un
reflet balaie la surface au moment où la carte est de chant, et le contenu de
la face qui arrive se pose juste derrière elle, ligne après ligne.

> Deux mouvements, donc **deux éléments** : la carte s'élève, un pivot tourne.
> `transform` est une propriété unique — une seule durée, une seule courbe —
> et l'élévation doit culminer à mi-course quand la rotation, elle, avance
> tout droit. Sur un seul élément c'est impossible.

> L'élévation est une classe posée puis retirée à mi-parcours : une transition
> ne sait aller que d'un point à un autre, elle ne peut pas culminer en chemin.

> L'échelon du contenu passe par une **variable** (`--pose`), et non par un
> `transition-delay` posé sur `:nth-child` : les règles d'état sont plus
> spécifiques et l'écrasaient — tout arrivait au même instant, et le contenu
> qui part attendait un tiers de seconde avant de s'effacer.

Trois pièges se cachent dans la rotation elle-même, et chacun cassait la
fluidité :

**La souplesse doit être symétrique.** Le reste du site sort en `ease-out`,
très en avance sur lui-même. Appliquée à un retournement, cette courbe
franchissait les 90° en 110 ms puis rampait 600 ms — et comme les deux faces
sont cachées de part et d'autre de cet angle, la carte restait **un quart de
seconde parfaitement invisible**. Une courbe symétrique
(`cubic-bezier(.45,0,.55,1)`) fait coïncider la moitié du temps avec la moitié
de la rotation, ce qui aligne le passage de `visibility` sur le moment où la
carte est de chant.

**Toutes les variantes déclarent la même suite de fonctions.** Avec `transform:
translateY(-5px)` au survol face à `transform: rotateY(180deg)` retournée, les
suites diffèrent : le navigateur ne peut plus interpoler fonction par fonction
et décompose les matrices. Une rotation d'exactement 180° s'y lit comme un
aplatissement — la carte s'écrasait au lieu de tourner. D'où
`rotateY(…) translateY(…) scale(…)` partout, même à zéro.

**L'amorce est une classe, pas une `@keyframes`.** Une animation prend la main
sur `transform` ; un appui pendant qu'elle jouait ne déclenchait plus aucune
transition et la carte sautait d'un coup à 180°. Une simple classe posée puis
retirée laisse la transition en place : l'appui ne fait que lui redonner une
cible.

**Faire comprendre qu'une carte se retourne.** Rien ne le dit d'une image
immobile. Trois repères, cumulés : un pictogramme de rotation dans le coin de
chaque face, une ligne d'invite au-dessus de la grille, et au survol une carte
légèrement pivotée — on voit qu'elle a une épaisseur, donc un dos. Le toucher
n'ayant pas de survol, le téléphone reçoit à la place une **amorce** : à la
première ouverture du panneau, une carte entrouvre son dos puis se referme.
Une seule fois, sur une seule carte.

## Les tarifs

Transmis par Marie :

| Soin | Séance | Forfait |
| ---- | ------ | ------- |
| Kobido               | 1 h — 60 €    | — |
| Relaxant             | 1 h — 60 €    | 3 séances — 160 € |
|                      | 1 h 30 — 90 € | 3 séances — 240 € |
| Deep Tissus          | 1 h — 70 €    | 3 séances — 180 € |
| Madéro               | 1 h — 70 €    | 5 séances — 300 € |
| Drainage lymphatique | 1 h — 80 €    | 5 séances — 350 € |

**Ils vivent dans un tableau sous les cartes, pas au dos de chacune.** On lit
des prix **côte à côte** : les porter au dos obligeait à retourner cinq cartes
pour en comparer deux, donc à retenir un chiffre en changeant d'écran. Le dos
de la carte reprend ce qu'il fait bien — la description du soin.

**Le prix de référence, pas la remise.** Le forfait affiche « au lieu de 180 € »
et non « −20 € » : une remise brute posée à côté d'un prix ne dit pas ce qu'elle
est — remise ? acompte ? part par séance ? Il reste **calculé** et jamais écrit :
chaque forfait porte le prix à la séance, le nombre de séances et le prix du lot.

```html
<span class="t-l" data-unite="70" data-lot="5" data-prix="300">
```

**Sur téléphone, le tableau se réempile en blocs.** Il défilait latéralement, et
c'est la colonne des forfaits — la plus utile — qui sortait de l'écran. Chaque
cellule reprend son intitulé de colonne (`data-col`), sans quoi les prix se
retrouveraient sans étiquette.

> **Jamais de `rowspan`.** Le Relaxant a deux durées, mais une cellule fusionnée
> ne survit pas au réempilement en blocs : ses deux durées vivent donc *dans*
> une cellule, en liste. Une ligne de tableau par soin, toujours.

> Le bloc des tarifs est un **enfant à part** de la feuille. Celle-ci borne ses
> paragraphes à une longueur de ligne lisible (34 rem) ; le tableau s'y
> retrouvait à l'étroit et « 1 h 30 » passait au-dessus de « 90 € ». Un tableau
> n'est pas de la prose : il lui faut la largeur de ses colonnes.

> Les deux forfaits du Relaxant s'appelaient tous deux « 3 séances ». Alignés en
> tableau, la ligne disait lequel portait sur l'heure ; empilés sur téléphone,
> plus rien ne le disait. Ils annoncent maintenant leur durée.

**Le monogramme sert de repère de ligne**, avec le même masque que la carte.
Hors de sa carte il perd le fond coloré qui le faisait ressortir : `--marque`
est la même teinte poussée jusqu'à 3:1 sur le socle du site — un tracé, pas du
texte (WCAG 1.4.11). Calculée par `tools-cartes.py`, comme le reste.

Contrastes relevés sur le rendu : de **5,78:1** (intitulés, « au lieu de ») à
**13,75:1** (les prix).

## Les illustrations

La V2 n'en affiche aucune : elle ne montre que le portrait de Marie. Les 19
illustrations vectorielles plates de la V1 (`assets/img/illus/` : le cabinet,
les soins, les avatars) restent au dépôt, générées par `tools-illustrations.py`
à partir d'une palette et de primitives communes (tête, main, feuille, bougie,
flacon). Si un panneau devait un jour porter un visuel, il est là :

```bash
python3 tools-illustrations.py
```

## La photo de Marie

C'est le premier regard : à l'accueil il n'y a que le pictogramme, elle, et le
nom de la marque. Une seule photo source alimente toutes les découpes —
`tools-photos.py` les tire de `assets/img/marie-source.png` :

```bash
python3 tools-photos.py
```

| Fichier | Usage | Format |
| ------- | ----- | ------ |
| `marie-hero.webp`       | portrait de l'accueil, desktop   | 1040 × 1144 |
| `marie-hero-m.webp`     | portrait de l'accueil, téléphone | 700 × 770   |
| `marie-hero-large.webp` | héros de la V1, téléphone        | 930 × 698   |
| `marie-portrait.webp`   | bloc « à propos » de la V1       | 800 × 1000  |

**Le cadre est l'arche de la V1**, reprise telle quelle : plus haute que large,
arrondie en demi-cercle vers le haut, posée sur deux angles doux. Un disque
avait été essayé ; Marie a demandé à revenir au cadre d'origine.

Deux tailles pour ce cadre, servies par `<picture>` : le cadre étant plus petit
sur téléphone, 700 px suffisent à la même netteté apparente pour la moitié du
poids. Le script d'aperçu intègre `srcset` autant que `src`, sans quoi l'image
mobile serait introuvable dans l'artifact.

Le point de visée est le **visage**, pas le centre de l'image : un recadrage
centré coupait le haut du crâne sur le format carré. Les repères sont en tête
du script, en fractions de l'image d'origine.

L'arche est dimensionnée **par sa hauteur** (`clamp(168px, 33vh, 380px)`), la
largeur en découlant du rapport : dans un écran qui ne défile pas, c'est la
hauteur qui est rare, pas la largeur. Elle garde ainsi la même part d'écran du
plus petit téléphone au plus grand, sans jamais pousser les bulles hors de vue.
Un halo très dilué derrière elle l'assoit sur le fond, et une respiration de
neuf secondes (`souffle`) l'anime à peine — assez pour que la page ne paraisse
pas figée, trop peu pour distraire.

> `animation` étant un raccourci, la respiration doit être déclarée **dans la
> même règle** que l'animation d'entrée : posée séparément, la seconde écrasait
> la première et le souffle ne jouait jamais.

## Le nom et le pictogramme

L'accueil s'ouvre sur le **pictogramme seul** — le M de `logo-mark.png`, en
ocre, en haut de l'écran. Il tient lieu d'en-tête : il n'y en a pas d'autre sur
ce site. Son `alt` est vide, le nom de la marque figurant juste dessous en
titre ; le répéter n'apprendrait rien à un lecteur d'écran.

Le titre affiche **`marieemassage`**, le nom sous lequel Marie est connue de sa
clientèle, et non « Marie ». Treize signes au lieu de cinq : l'échelle
typographique est recalée pour qu'il tienne sur une ligne dès 320 px de large,
sans quoi il se couperait en plein milieu du mot.

> Le `<h1>` ne contient donc plus « massage à Voisins-le-Bretonneux ». Ce n'est
> pas perdu pour le référencement : le titre d'onglet, la ligne d'accroche
> juste dessous et les données structurées le portent toujours.

## Mise en ligne

Ce qu'un site publié doit porter, et qui est en place :

- **Aperçu des liens partagés** (`og:` / `twitter:`) sur les 3 pages, avec une
  image dédiée `assets/img/partage.jpg` (1200 × 630). Sans elle, un lien envoyé
  sur WhatsApp ou Instagram s'affiche sans visuel.
- **Données structurées** `HealthAndBeautyBusiness` sur l'accueil : nom,
  téléphone, adresse, horaires, Instagram. C'est ce qui alimente la fiche locale
  dans les résultats de recherche — le premier levier pour une praticienne.
- **`robots.txt` et `sitemap.xml`**, **`canonical`** sur chaque page.
- **Page 404** et **mentions légales**, liées depuis le pied de page.

> ⚠️ Les URL absolues (`og:url`, `canonical`, sitemap, robots) pointent vers
> l'adresse GitHub Pages de relecture. **À remplacer par le vrai domaine** avant
> la mise en ligne — un `canonical` faux fait disparaître le site des résultats.

## Les photos et leur enregistrement

Le portrait de Marie est protégé contre l'enregistrement **occasionnel** :
`pointer-events:none` sur les images fait porter le clic droit au conteneur,
qui n'a pas d'image à proposer au menu contextuel ; le glisser-déposer et la
sélection sont désactivés ; le menu contextuel est bloqué sur les cadres de
visuels. Les liens parents continuent de fonctionner, l'événement leur revenant.

**Cela décourage, cela n'empêche pas.** Une capture d'écran, l'inspecteur du
navigateur ou un simple `curl` sur l'URL de l'image restent hors de portée de
toute page web — c'est vrai de n'importe quel site. La seule protection réelle
est juridique : c'est l'objet du paragraphe « Propriété intellectuelle » des
mentions légales.

## Le téléphone d'abord

> Une barre d'appel fixe en bas de l'écran a existé un temps ; Marie l'a fait
> retirer. Ne pas la réintroduire sans le lui redemander.

Trois clientes sur quatre arriveront depuis un téléphone : c'est le format de
référence, pas une adaptation du desktop. La V2 est née de là — le meilleur
moyen d'alléger une page mobile étant de ne pas la remplir.

**Tout tient dans la fenêtre.** L'accueil ne défile pas : portrait, prénom,
accroche et cinq bulles. La V1 demandait 1,8 à 3 écrans par page ; ici il n'y
a plus d'écran à parcourir avant de trouver quoi que ce soit. Les hauteurs sont
en `vh` et non en pixels, donc la composition tient aussi bien sur un petit
téléphone que sur un grand.

**L'échelle typographique est calée sur le téléphone.** Les bornes basses des
`clamp()` ne s'appliquent qu'aux petits écrans : les baisser ne touche que le
mobile, sans un empilement d'exceptions.

**Les cibles tactiles.** Chaque bulle fait 64 px de diamètre minimum et son
libellé fait partie du bouton : la zone de contact dépasse largement les 44 px
recommandés. Rien ne descend sous 11 px de texte.

**Le paysage et les petits écrans.** Les bulles et le pied de page ne
rétrécissent pas avec la hauteur de l'écran ; la photo et le pictogramme le
peuvent, et ce sont donc eux qui cèdent. Sous 700 px de haut la photo passe de
33 à 23 % de la fenêtre et le pictogramme perd sa marge — sans quoi un
320 × 568 débordait de 28 px, et comme rien ne défile ici, ces 28 px étaient
perdus, pas repoussés. Sous 520 px — un téléphone couché, ou un clavier ouvert
— tout rétrécit encore et l'accroche disparaît : la commune figure déjà dans le
panneau « Le lieu ». Les bulles, elles, restent toujours visibles. Vérifié de
280 × 653 à 1920 × 1080 : aucun débord, et de 16 à 148 px de marge libre.

**Au toucher.** `touch-action: manipulation` écarte le double-appui pour zoomer
et le délai que le navigateur garde en réserve avant de valider un appui. Le
voile gris d'iOS est retiré au profit d'états `:active` conformes à la charte —
sur un écran tactile `:hover` ne se déclenche jamais. Les panneaux portent
`overscroll-behavior: contain` : le rebond de fin de course ne se propage pas
au fond.

## Les panneaux

Le geste central du site : la bulle s'ouvre en panneau. Trois points le font
tenir.

**Le disque part de la bulle.** Au clic, le JS relève le centre du rond touché
et le pose en `--x` / `--y` sur le panneau ; le CSS anime
`clip-path: circle(0 → 150% at var(--x) var(--y))`. Sans ces coordonnées
l'ouverture partirait du milieu de l'écran et perdrait son lien avec ce qu'on
vient de toucher. `clip-path` s'anime sur le compositeur : aucune remise en
page, donc aucune saccade.

**`visibility` doit être décalée dans le temps.** Un panneau réduit à un disque
de rayon nul reste techniquement affiché ; il capterait les clics par-dessus
l'accueil. On le passe donc en `visibility:hidden`, mais **après** la fermeture
(`transition: visibility 0s linear .55s`), sinon il disparaîtrait avant que
l'animation ait joué. À l'ouverture, la même transition est remise à `0s`.

**Le clavier suit le doigt.** `inert` est retiré à l'ouverture et remis à la
fermeture : tant qu'un panneau est fermé, ni la tabulation ni un lecteur
d'écran ne le traversent — alors que son contenu reste dans le document pour
les moteurs de recherche. Le focus part sur la croix de fermeture, et revient
sur la bulle d'origine quand on referme, sinon il retombe en tête de document
et l'on perd sa place.

`Échap`, le bouton « retour » du téléphone et l'arrivée directe sur une
adresse `#…` passent tous par les deux mêmes fonctions, `ouvrir()` et
`fermer()`.

## Fluidité

Le défilement tient **60 images par seconde** sur les trois formats, y compris
avec le processeur bridé ×4 pour approcher un vrai téléphone : aucune image au
delà de 20 ms sur 118 mesurées par page. Il n'y a donc pas de saccade à
corriger — le confort se joue ailleurs, sur ce qui se charge et sur la réponse
au doigt.

**Polices.** Le site n'emploie que trois graisses (400, 500, 600). Il en
déclarait six et préchargeait la 700, jamais utilisée, tandis que la 600 —
celle de tous les titres — ne l'était pas : les titres s'affichaient en police
de secours puis basculaient. Préchargements corrigés, graisses inutiles
supprimées (89 Ko de moins dans le dépôt).

**Visuels.** Le logo et l'illustration du héros passent en `fetchpriority=high`,
tout le reste en `loading=lazy` : la page d'accueil descend de 91 à 73 Ko et de
6 à 3 visuels au premier rendu.

**Au toucher.** `touch-action: manipulation` écarte le double-appui pour zoomer,
et avec lui le délai que le navigateur garde en réserve avant de valider un
appui. Le voile gris d'iOS est retiré au profit d'états `:active` conformes à la
charte — sur un écran tactile `:hover` ne se déclenche jamais, donc appuyer sur
une bulle ne renvoyait aucun retour. Les panneaux portent `overscroll-behavior:
contain` : le rebond de fin de course ne se propage plus au fond.

## Le passage d'une page à l'autre

Sans objet ici : il n'y a plus qu'une page. C'était le principal reproche fait
à la V1 — chaque onglet rechargeait le document, et trois délais s'y étaient
ajoutés pour un temps perçu d'une seconde (fondu de sortie retenant la
navigation 280 ms, animation d'entrée 600 ms, préchargeur rejoué à chaque
retour ~1100 ms). Ramenés à 336 ms là-bas, ils tombent à zéro ici : le contenu
est déjà chargé, l'ouverture d'un panneau est une animation, pas une
navigation.

## La prise de rendez-vous

Les rendez-vous se prennent **uniquement par téléphone**. C'est pour cela que
la cinquième bulle est pleine et colorée quand les autres sont creuses : elle
ouvre un panneau bâti autour de l'appel, le numéro en grand, en `tel:` — un
appui suffit depuis un mobile — et les horaires juste dessous.

Le formulaire de contact qui occupait cette place a été **retiré**, pas
seulement masqué : il ne pouvait pas prendre de rendez-vous et laissait croire
le contraire (sa soumission était simulée, aucun email n'était envoyé). Son
CSS et son module JS sont partis avec lui.

L'email reste affiché, mais présenté comme ce qu'il est — « une question ? »,
pas un canal de réservation.

## Les chiffres affichés

Aucune statistique n'est écrite en dur : **rien n'est inventé**. La note
moyenne et le nombre d'avis du panneau « Avis » sont recalculés au chargement
à partir des témoignages réellement présents dans `index.html`. Chaque
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

## Ce que la relecture a corrigé

Une relecture complète du site déployé a relevé quinze défauts ; ils sont tous
corrigés. Les plus coûteux, pour mémoire — ce sont des pièges qui se
reproduisent :

**Une adresse ordinaire emportait tout le script.** `ouvrir()` acceptait
n'importe quel `id` trouvé dans la page, pas seulement les panneaux. Arriver
sur `…/#bulles` — la cible du lien d'évitement du site lui-même — cherchait un
bouton de fermeture dans un `<nav>`, et l'exception coupait le fichier : plus
aucune carte ne se retournait, la note moyenne restait vide, l'année du pied de
page restait figée. Douze `id` de la page menaient à ce chemin.

**Le fond restait atteignable sous un panneau ouvert.** `clip-path` masque à
l'œil et rien d'autre : la tabulation sortait du panneau et parcourait les
bulles et le pied de page invisibles en dessous. Le fond reçoit maintenant
`inert` — le même mécanisme que celui déjà employé pour les panneaux fermés —
et le retire **avant** qu'on y remette le focus.

**Fermer empilait au lieu de revenir.** Chaque fermeture ajoutait une entrée
d'historique : le bouton « retour » du téléphone rouvrait le panneau qu'on
venait de fermer, et cinq rubriques visitées demandaient onze retours pour
sortir du site. La croix appelle désormais `history.back()`.

**Trois copies de la même police.** Figtree est une police **variable** : les
fichiers 400, 500 et 600 livrés par Google avaient le même md5. Déclarés
séparément, ils se téléchargeaient trois fois — 60 Ko pour 20 Ko utiles.

**Un verrou de défilement rendait le contenu inatteignable.** `overflow:hidden`
sur `html` tenait l'accueil dans un écran ; à 200 % de zoom la composition
dépasse, et les bulles comme le pied de page devenaient hors d'atteinte, au
doigt comme au clavier. Retiré : aux tailles normales rien ne défile de toute
façon.

**Deux `opacity` défaisaient des contrastes calculés.** `tools-cartes.py`
calcule chaque encre pour tenir 4,5:1 ; un `opacity:.82` sur la ligne
durée-et-tarif la recomposait sur le fond de la carte et la ramenait entre 3,3
et 3,8:1 sur quatre cartes sur cinq. Même chose pour la mention « soins de
bien-être, non thérapeutiques », à 3,1:1. Une opacité n'éclaircit pas un texte,
elle le mélange au fond — la couleur se choisit, elle ne se dilue pas.

**Les survols collaient sur iOS.** `:hover` y reste appliqué au dernier élément
touché : après un appui, la carte restait posée à 189°, de travers, flottant
au-dessus de ses voisines. Tous les survols sont passés sous
`@media (hover:hover) and (pointer:fine)`.

**Les deux pages annexes n'avaient plus de style.** Elles gardaient le balisage
de la V1 alors qu'elles ne chargent plus que `v2.css` : un mur de texte sans
respiration, et des liens rendus invisibles par `a{text-decoration:none}`. La
404 est en outre devenue **autonome** — styles inclus, aucun fichier externe :
GitHub Pages la sert depuis n'importe quelle profondeur d'adresse, où tout
chemin relatif se serait perdu.

## À compléter

- [ ] **Textes** — remplacer tout le lorem ipsum (présentation, cabinet, soins)
- [ ] **Photos** — le portrait de Marie est en place ; le cabinet et les soins
      sont encore illustrés
- [ ] **Descriptions des soins** — les textes au dos des cartes sont des
      exemples, à écrire avec Marie
- [ ] **Nom du soin « Deep Tissus »** — la planche l'écrit ainsi ; le terme
      consacré est *deep tissue*. À trancher avec Marie.
- [x] ~~**Tarifs et durées**~~ — transmis par Marie, en place sur les cartes
- [ ] **Panneau « Moi »** — la structure est posée, les contenus manquent :
      formations (école + année), ancienneté (« je masse depuis X ans »),
      photo de Marie en séance, déroulé réel d'une séance. Chaque champ à
      remplir est entre crochets dans `index.html`.
- [ ] **Avis** — les témoignages sont des exemples, à remplacer par les vrais
- [ ] **Coordonnées** — téléphone et email sont des valeurs fictives, à
      remplacer dans `index.html` (panneau « Rendez-vous », JSON-LD) et dans
      `mentions-legales.html`
- [ ] **Mentions légales** — la page existe, chaque `[À COMPLÉTER]` doit être
      renseigné : nom de famille, SIRET, adresse, hébergeur
- [ ] **Nom de domaine** — remplacer l'adresse GitHub Pages dans les balises
      `og:`/`canonical` des 3 pages, `robots.txt` et `sitemap.xml`
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

## Mettre le site en ligne (GitHub Pages)

Le plus court chemin pour obtenir une adresse partageable, sans rien installer :

1. Sur GitHub, dépôt **`sringot/per-`** → onglet **Settings** → **Pages**
2. Sous *Build and deployment* → *Source*, choisir **Deploy from a branch**
3. Branche : **`claude/v2-bulles`** pour la V2, **`claude/git-repo-access-ea5z33`**
   pour la V1 ; dossier **`/ (root)`** → **Save**. Changer de branche ici, c'est
   changer la version en ligne — pratique pour les faire comparer à Marie.

Une minute plus tard, le site est servi sur :

```
https://sringot.github.io/per-/
```

Chaque `git push` sur cette branche met la page en ligne à jour.

Le site n'utilise **aucun chemin absolu** : il fonctionne aussi bien à la racine
d'un domaine que dans un sous-dossier comme `/per-/`.

Les URL absolues (`og:`, `canonical`, `sitemap.xml`, `robots.txt`) pointent sur
cette adresse GitHub Pages, pour que les aperçus de lien fonctionnent pendant la
phase de relecture. **À rebasculer sur le vrai domaine** le jour de la mise en
ligne définitive — un `canonical` erroné fait disparaître le site des résultats.

## Hébergement

Le site étant entièrement statique, il se déploie tel quel sur Netlify, Vercel,
GitHub Pages ou tout hébergement classique — rien à construire au préalable.
