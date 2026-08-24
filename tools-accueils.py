#!/usr/bin/env python3
"""Construit la page de comparaison des quatre accueils.

Chaque maquette est rendue **à l'échelle réelle du téléphone** : le cadre
porte le rapport 390 × 844 et tout ce qu'il contient est exprimé en unités
de conteneur (`cqw`, `cqh`). La maquette est donc proportionnellement
identique au vrai site, que le cadre fasse 390 px sur un ordinateur ou
340 px sur un téléphone.

Les visuels, la police et le filigrane sont embarqués : un artifact ne
sert qu'un fichier.
"""
import base64
import pathlib

SITE = pathlib.Path(__file__).parent
SORTIE = pathlib.Path('/tmp/claude-0/-home-user-per-'
                      '/0ab23514-8cad-52d4-a3c4-7a8a46290735/scratchpad/accueils.html')


def b64(rel):
    return base64.b64encode((SITE / rel).read_bytes()).decode()


POLICE = b64('assets/fonts/figtree-400-latin.woff2')
LOGO = b64('assets/img/logo-officiel.webp')
PHOTO = b64('assets/img/marie-hero-m.webp')
SIGNE = b64('assets/img/logo-m.svg')

# Les tracés viennent d'index.html — les mêmes icônes que le site, pas des
# approximations : une maquette qui ne montre pas les vrais signes ne se
# compare pas au vrai écran.
ICONES = {
    'moi': '<circle cx="12" cy="8.4" r="3.9"/><path d="M4.6 20.2a7.4 7.4 0 0 1 14.8 0"/>',
    'lieu': '<path d="M4 20V9.6L12 4l8 5.6V20"/><path d="M9.4 20v-5.4h5.2V20"/>',
    'massages': '<path d="M8.6 13.4V5.6a1.6 1.6 0 0 1 3.2 0v5.2"/>'
                '<path d="M11.8 10.4V6.4a1.6 1.6 0 0 1 3.2 0v4.4"/>'
                '<path d="M15 10.8V8.2a1.5 1.5 0 0 1 3 0v6.2a5.6 5.6 0 0 1-5.6 5.6H11'
                'a5 5 0 0 1-4.3-2.5L5 14.7a1.5 1.5 0 0 1 2.4-1.8Z"/>',
    'avis': '<path d="m12 4 2.5 5 5.5.8-4 3.9.9 5.5-4.9-2.6-4.9 2.6.9-5.5-4-3.9L9.5 9Z"/>',
    'rdv': '<path d="M6 4h3l2 5-2.4 1.4a12 12 0 0 0 5 5L15 13l5 2v3a2 2 0 0 1-2.2 2'
           'A16 16 0 0 1 4 6.2 2 2 0 0 1 6 4Z"/>',
}
NOMS = {'moi': 'Moi', 'lieu': 'Le lieu', 'massages': 'Massages',
        'avis': 'Avis', 'rdv': 'Rendez-vous'}


def bulle(cle, phare=False):
    return (f'<span class="bulle{" bulle--phare" if phare else ""}" data-r="{cle}">'
            f'<span class="bulle__rond"><svg viewBox="0 0 24 24" aria-hidden="true">'
            f'{ICONES[cle]}</svg></span>'
            f'<span class="bulle__nom">{NOMS[cle]}</span></span>')


LOGO_IMG = (f'<img class="logo" src="data:image/webp;base64,{LOGO}" alt="" '
            f'width="200" height="200">')
PHOTO_IMG = (f'<img src="data:image/webp;base64,{PHOTO}" alt="Marie" '
             f'width="700" height="938">')
FILIGRANE = '<span class="filigrane" aria-hidden="true"></span>'

FAITS = ('<p class="faits"><span>Réservé aux femmes</span>'
         '<span>Dès 60&nbsp;€</span>'
         '<span>Montigny-le-Bretonneux</span></p>')
# Dans la carte centrée, les trois pastilles se cassaient en 2 + 1 et le
# bloc perdait sa symétrie. Sur une seule ligne, les mêmes trois faits.
FAITS_LIGNE = ('<p class="faits-ligne">Réservé aux femmes · Dès 60&nbsp;€ · '
               'Montigny-le-Bretonneux</p>')

ACCROCHE = 'Une heure pour vous, dans une pièce pensée pour ça.'

# Le vrai site porte ce pied de page sous l'accueil : sans lui, les
# maquettes montreraient un bas d'écran plus vide qu'il ne l'est.
PIED = '<p class="pied">© 2026 Marie Massage · Mentions légales</p>'

# ---------------------------------------------------------------- maquettes

A = f'''
<div class="ec ec--a">
  {FILIGRANE}
  {LOGO_IMG}
  <figure class="portrait">{PHOTO_IMG}</figure>
  <nav class="bulles">{''.join(bulle(c, c == 'rdv') for c in NOMS)}</nav>
  <div class="mot">
    <h2 class="titre">marieemassage</h2>
    <p class="accroche">{ACCROCHE}</p>
    {FAITS}
  </div>
  {PIED}
</div>'''

B = f'''
<div class="ec ec--b">
  <figure class="fond">{PHOTO_IMG}</figure>
  {LOGO_IMG}
  <div class="voile">
    <h2 class="titre">marieemassage</h2>
    <p class="accroche">{ACCROCHE}</p>
    {FAITS}
    <nav class="bulles">{''.join(bulle(c, c == 'rdv') for c in NOMS)}</nav>
    {PIED}
  </div>
</div>'''

C = f'''
<div class="ec ec--c">
  {FILIGRANE}
  <div class="carte">
    {LOGO_IMG}
    <figure class="portrait">{PHOTO_IMG}</figure>
    <h2 class="titre">marieemassage</h2>
    <p class="accroche">{ACCROCHE}</p>
    {FAITS_LIGNE}
    <nav class="bulles">{''.join(bulle(c) for c in ('moi', 'lieu', 'massages', 'avis'))}</nav>
    <span class="cta"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONES['rdv']}</svg>Prendre rendez-vous</span>
  </div>
  {PIED}
</div>'''

RANGS = [
    ('massages', 'Massages', 'Cinq soins, dès 60&nbsp;€'),
    ('avis', 'Avis', 'Ce qu’elles en disent'),
    ('lieu', 'Le lieu', 'Une pièce dédiée, à Montigny'),
    ('moi', 'Moi', 'Réservé aux femmes, par une femme'),
]
D = f'''
<div class="ec ec--d">
  {FILIGRANE}
  <header class="tete">
    {LOGO_IMG}
    <div>
      <h2 class="titre">marieemassage</h2>
      <p class="sous">Masseuse bien-être · Montigny-le-Bretonneux</p>
    </div>
    <figure class="pastille">{PHOTO_IMG}</figure>
  </header>
  <p class="accroche">{ACCROCHE}</p>
  <nav class="rangs">
    {''.join(f"""<span class="rang" data-r="{c}">
      <span class="bulle__rond"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONES[c]}</svg></span>
      <span class="rang__mot"><b>{nom}</b><em>{sous}</em></span>
      <svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="m9 5 7 7-7 7"/></svg>
    </span>""" for c, nom, sous in RANGS)}
  </nav>
  <span class="cta"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONES['rdv']}</svg>Prendre rendez-vous</span>
  {PIED}
</div>'''

# ------------------------------------------------------------------- notice

MAQUETTES = [
    ('A', 'Le retour du vide', A,
     'La composition d’aujourd’hui, sans rien déplacer : on remplit les '
     '116 px qui restaient sous le nom.',
     [('Ce que ça change',
       'Une phrase qui promet quelque chose remplace l’étiquette de métier, '
       'et trois faits — femmes, prix d’appel, ville — passent devant, au lieu '
       'd’attendre à un clic.'),
      ('Le risque',
       'Aucun, ou presque : c’est la même page. Mais ça ne règle pas '
       'l’absence de bouton de rendez-vous dans les panneaux.')]),
    ('B', 'Plein cadre', B,
     'La photo prend tout l’écran. Le nom, la promesse et les bulles se '
     'posent sur un voile sombre en bas.',
     [('Ce que ça change',
       'C’est l’écran qui « sort de l’ordinaire ». Sur Instagram, où la '
       'plupart arriveront, la première image est une vraie image, pas une '
       'mise en page.'),
      ('Le risque',
       'On perd le calme et le vide crème qui font une partie de la douceur '
       'du site. Et la photo verticale est très recadrée sur les côtés.')]),
    ('C', 'La carte de visite', C,
     'Un seul bloc posé au milieu du crème, qui contient tout : logo, '
     'portrait rond, promesse, quatre bulles et le bouton de rendez-vous.',
     [('Ce que ça change',
       'Le rendez-vous cesse d’être une bulle parmi cinq : c’est un vrai '
       'bouton, pleine largeur, en bas. C’est la disposition qui fait le plus '
       'pour la prise de rendez-vous.'),
      ('Le risque',
       'Le relief doux se voit moins bien quand une carte est posée sur le '
       'même crème que le fond — c’est le détail à surveiller.')]),
    ('D', 'Le menu', D,
     'La photo devient une pastille dans l’en-tête, et les rubriques '
     'deviennent quatre lignes pleine largeur, chacune avec sa raison '
     'd’être ouverte.',
     [('Ce que ça change',
       'On lit ce qu’il y a derrière chaque rubrique avant de cliquer : '
       '« Cinq soins, dès 60 € », « Ce qu’elles en disent ». Les zones '
       'touchables sont deux fois plus grandes que les bulles.'),
      ('Le risque',
       'C’est le plus efficace et le moins singulier — on s’approche de '
       'l’application. Les bulles rondes, qui font l’identité de la V2, '
       'ne sont plus que des icônes.')]),
]


def section(lettre, nom, ecran, intention, notes):
    items = ''.join(f'<div class="note"><h4>{t}</h4><p>{c}</p></div>' for t, c in notes)
    return f'''
<section class="prop" id="prop-{lettre.lower()}">
  <div class="prop__tete">
    <span class="lettre" aria-hidden="true">{lettre}</span>
    <div>
      <h3>{nom}</h3>
      <p class="intention">{intention}</p>
    </div>
  </div>
  <div class="prop__corps">
    <div class="tel"><div class="tel__ecran">{ecran}</div></div>
    <div class="notes">{items}</div>
  </div>
</section>'''


CSS = f'''
@font-face{{
  font-family:'Figtree'; font-style:normal; font-weight:400 600; font-display:swap;
  src:url(data:font/woff2;base64,{POLICE}) format('woff2');
}}

/* ---- La page qui présente : un mur d'atelier, volontairement plus sourd
   que le crème de Marie, pour que les écrans se détachent comme des objets
   posés dessus. Les quatre maquettes, elles, gardent sa charte exacte. ---- */
:root{{
  --mur:#E6DDD2; --mur-2:#EFE8DF;
  --texte:#2A2320; --sourd:#6B6058; --trait:rgba(42,35,32,.14);
  --accent:#6A2F3C; --bezel:#D4C8BA;
}}
:root:not([data-theme="light"]){{ color-scheme:light }}
@media (prefers-color-scheme:dark){{
  :root:not([data-theme="light"]){{
    --mur:#1E1917; --mur-2:#2A2320;
    --texte:#F3ECE4; --sourd:#A79C92; --trait:rgba(243,236,228,.16);
    --accent:#D9A0AC; --bezel:#3A322D;
    color-scheme:dark;
  }}
}}
:root[data-theme="dark"]{{
  --mur:#1E1917; --mur-2:#2A2320;
  --texte:#F3ECE4; --sourd:#A79C92; --trait:rgba(243,236,228,.16);
  --accent:#D9A0AC; --bezel:#3A322D;
  color-scheme:dark;
}}

*,*::before,*::after{{ box-sizing:border-box }}
body{{
  margin:0; background:var(--mur); color:var(--texte);
  font-family:'Figtree',system-ui,-apple-system,'Segoe UI',sans-serif;
  font-size:16px; line-height:1.6; -webkit-font-smoothing:antialiased;
}}
.page{{ max-width:1140px; margin-inline:auto; padding:clamp(1.5rem,5vw,4rem) clamp(1.1rem,4vw,2.5rem) 5rem; }}

.chapeau{{ display:flex; flex-direction:column; gap:.9rem; margin-bottom:clamp(2rem,6vw,3.5rem) }}
.oeil{{ font-size:.72rem; letter-spacing:.22em; text-transform:uppercase; color:var(--sourd); margin:0 }}
h1{{ font-size:clamp(2rem,6vw,3.1rem); line-height:1.04; letter-spacing:-.035em;
    font-weight:600; margin:0; text-wrap:balance }}
.chapeau p:not(.oeil){{ margin:0; max-width:60ch; color:var(--sourd); font-size:clamp(.95rem,2.4vw,1.05rem) }}
.chapeau b{{ color:var(--texte); font-weight:600 }}

.prop{{ padding-top:clamp(2rem,6vw,3.2rem); margin-top:clamp(2rem,6vw,3.2rem); border-top:1px solid var(--trait) }}
.prop__tete{{ display:flex; gap:1rem; align-items:flex-start; margin-bottom:1.6rem }}
.lettre{{
  flex:none; width:2.5rem; height:2.5rem; border-radius:50%;
  display:grid; place-items:center; font-weight:600; font-size:1.05rem;
  background:var(--mur-2); color:var(--accent); border:1px solid var(--trait);
}}
.prop__tete h3{{ margin:0; font-size:clamp(1.3rem,3.6vw,1.7rem); font-weight:600; letter-spacing:-.02em }}
.intention{{ margin:.3rem 0 0; color:var(--sourd); max-width:52ch }}
.prop__corps{{ display:grid; gap:clamp(1.4rem,4vw,2.6rem); align-items:start }}
@media (min-width:820px){{ .prop__corps{{ grid-template-columns:390px minmax(0,1fr) }} }}
.notes{{ display:grid; gap:1.3rem; align-content:start }}
.note h4{{ margin:0 0 .25rem; font-size:.72rem; letter-spacing:.14em; text-transform:uppercase;
           color:var(--accent); font-weight:600 }}
.note p{{ margin:0; color:var(--sourd); max-width:56ch }}

.fin{{ margin-top:clamp(2.5rem,7vw,4rem); padding-top:clamp(1.6rem,5vw,2.4rem);
       border-top:1px solid var(--trait); color:var(--sourd); max-width:62ch }}
.fin h3{{ margin:0 0 .6rem; color:var(--texte); font-size:1.15rem; font-weight:600 }}
.fin p{{ margin:0 0 .8rem }}

/* ===================== LE CADRE DU TÉLÉPHONE =====================
   Le cadre porte le rapport 390 × 844 et sert de **conteneur de taille** :
   tout ce qu'il y a dedans est mesuré en `cqw` / `cqh`, jamais en pixels.
   Une maquette rendue dans un cadre de 340 px est donc exactement la même
   image que dans un cadre de 390 — ce qui n'aurait pas été vrai avec des
   tailles fixes, où seul le cadre aurait rétréci. */
.tel{{
  width:min(390px,100%); aspect-ratio:390/844;
  border-radius:9.5cqw; padding:1.1cqw;
  background:var(--bezel);
  box-shadow:0 1.4rem 3rem rgba(42,35,32,.22), 0 .2rem .6rem rgba(42,35,32,.12);
  container-type:size;
}}
.tel__ecran{{ width:100%; height:100%; border-radius:8.6cqw; overflow:hidden; position:relative }}

/* ---- La charte de Marie, telle quelle, dans le cadre ---- */
.ec{{
  --card:#FCF0E2; --ink:#2A2320; --ink-soft:#635D57; --or:#6A2F3C; --blanc:#fff;
  --moi:#A47864; --lieu:#898D7F; --massages:#988968; --avis:#B37D79; --rdv:#6A2F3C;
  --nm-out:-1.3cqw -1.3cqw 3.1cqw rgba(255,255,255,.95), 1.5cqw 1.8cqw 4.1cqw rgba(122,104,84,.18);
  --nm-out-lg:-2cqw -2cqw 5.1cqw rgba(255,255,255,.95), 2.6cqw 3.1cqw 6.7cqw rgba(122,104,84,.18);
  --pad:4.5cqw;
  position:absolute; inset:0; background:var(--card); color:var(--ink);
  font-size:3.85cqw; line-height:1.6; overflow:hidden;
}}
.ec [data-r=moi]{{ --teinte:var(--moi) }}
.ec [data-r=lieu]{{ --teinte:var(--lieu) }}
.ec [data-r=massages]{{ --teinte:var(--massages) }}
.ec [data-r=avis]{{ --teinte:var(--avis) }}
.ec [data-r=rdv]{{ --teinte:var(--rdv) }}

.filigrane{{
  position:absolute; right:-8%; top:11cqh; width:80%; aspect-ratio:627/593;
  background:var(--moi); opacity:.06; pointer-events:none;
  -webkit-mask:url('data:image/svg+xml;base64,{SIGNE}') center/contain no-repeat;
  mask:url('data:image/svg+xml;base64,{SIGNE}') center/contain no-repeat;
}}
.ec .logo{{ width:13.3cqw; height:auto; display:block }}
.ec .titre{{ font-size:7.2cqw; font-weight:600; line-height:1; letter-spacing:-.035em;
             margin:0; color:var(--ink); overflow-wrap:anywhere }}
.ec .accroche{{ font-size:3.4cqw; line-height:1.45; color:var(--ink-soft); margin:0; text-wrap:balance }}
.faits{{ display:flex; flex-wrap:wrap; gap:1.5cqw; margin:0; font-size:2.7cqw; line-height:1 }}
.faits span{{ padding:1.5cqw 2.6cqw; border-radius:5cqw; background:var(--card);
              box-shadow:var(--nm-out); color:var(--ink-soft); white-space:nowrap }}
.faits-ligne{{ margin:0; font-size:2.8cqw; letter-spacing:.01em; color:var(--ink-soft);
               text-wrap:balance }}
.pied{{ position:absolute; left:0; right:0; bottom:1.8cqh; margin:0; text-align:center;
        font-size:2.3cqw; line-height:1; color:var(--ink-soft); opacity:.7 }}

.bulle{{ display:flex; flex-direction:column; align-items:center; gap:.9cqw;
         width:18cqw; color:var(--ink-soft) }}
.bulle__rond{{
  width:15cqw; aspect-ratio:1; display:grid; place-items:center; border-radius:50%;
  background:color-mix(in srgb, var(--teinte,var(--or)) 8%, var(--card));
  box-shadow:var(--nm-out); color:var(--teinte,var(--or)); flex:none;
}}
.bulle__rond svg{{ width:44%; height:44%; fill:none; stroke:currentColor;
                   stroke-width:1.6; stroke-linecap:round; stroke-linejoin:round }}
.bulle__nom{{ font-size:2.46cqw; font-weight:500; letter-spacing:.02em; line-height:1.15; text-align:center }}
.bulle--phare .bulle__rond{{ background:var(--rdv); color:var(--blanc) }}
.bulle--phare{{ color:var(--ink) }}

.cta{{
  display:flex; align-items:center; justify-content:center; gap:2.2cqw;
  padding:4.2cqw; border-radius:5cqw; background:var(--or); color:var(--blanc);
  font-size:3.9cqw; font-weight:600; letter-spacing:-.01em;
}}
.cta svg{{ width:4.6cqw; height:4.6cqw; fill:none; stroke:currentColor;
           stroke-width:1.7; stroke-linecap:round; stroke-linejoin:round }}

/* ---------- A : la composition d'aujourd'hui, complétée ---------- */
.ec--a{{
  display:grid; align-content:center; justify-items:start;
  grid-template-columns:minmax(0,1fr) auto;
  grid-template-areas:"logo logo" "photo bulles" "mot mot";
  column-gap:3cqw; row-gap:2.2cqh; padding:3.5cqh var(--pad);
}}
.ec--a .logo{{ grid-area:logo }}
.ec--a .portrait{{ grid-area:photo }}
.ec--a .bulles{{ grid-area:bulles }}
.ec--a .mot{{ grid-area:mot; display:flex; flex-direction:column; gap:1.4cqh; min-width:0 }}
.ec--a .portrait{{
  margin:0; width:100%; align-self:stretch; overflow:hidden;
  border-radius:50cqw 50cqw 6.7cqw 6.7cqw; box-shadow:var(--nm-out-lg);
}}
.ec--a .portrait img{{ width:100%; height:100%; object-fit:cover; object-position:50% 32%; display:block }}
.ec--a .bulles{{ display:flex; flex-direction:column; align-items:center;
                 justify-content:space-between; gap:.6cqh; height:100% }}

/* ---------- B : la photo prend tout, le texte se pose dessus ---------- */
.ec--b{{ display:block }}
.ec--b .fond{{ margin:0; position:absolute; inset:0 }}
.ec--b .fond img{{ width:100%; height:100%; object-fit:cover; object-position:50% 26%; display:block }}
.ec--b .logo{{ position:absolute; top:4cqh; left:var(--pad); width:12cqw;
               filter:drop-shadow(0 .6cqw 1.6cqw rgba(42,35,32,.45)) }}
/* Le voile monte haut et s'éteint par paliers : sur une seule bascule, la
   photo s'assombrissait d'un coup et la coupure se voyait comme une barre. */
.ec--b .voile{{
  position:absolute; inset:auto 0 0 0; padding:24cqh var(--pad) 6.5cqh;
  display:flex; flex-direction:column; gap:1.7cqh;
  background:linear-gradient(to top,
    rgba(30,24,21,.95) 0%, rgba(30,24,21,.93) 26%, rgba(30,24,21,.80) 46%,
    rgba(30,24,21,.52) 66%, rgba(30,24,21,.22) 84%, rgba(30,24,21,0) 100%);
}}
.ec--b .titre, .ec--b .accroche{{ color:#FDF6EE }}
.ec--b .accroche{{ color:#E4D8CC }}
.ec--b .faits span{{ background:rgba(253,246,238,.14); color:#F3E8DC; box-shadow:none;
                     backdrop-filter:blur(2px) }}
.ec--b .bulles{{ display:flex; justify-content:space-between; margin-top:.8cqh }}
.ec--b .bulle{{ color:#E4D8CC; width:17.5cqw }}
.ec--b .bulle__rond{{ width:14cqw; background:rgba(253,246,238,.93); box-shadow:none;
                      color:var(--teinte) }}
.ec--b .bulle--phare .bulle__rond{{ background:var(--rdv); color:#FDF6EE;
                                    box-shadow:0 0 0 .5cqw rgba(253,246,238,.85) }}
.ec--b .bulle--phare{{ color:#FDF6EE }}
.ec--b .pied{{ color:#C9BBAE; opacity:.9 }}

/* ---------- C : un seul bloc, et le rendez-vous devient un bouton ---------- */
.ec--c{{ display:grid; place-items:center; padding:var(--pad) }}
.ec--c .carte{{
  width:100%; display:flex; flex-direction:column; align-items:center; gap:2.4cqh;
  padding:4.5cqh 5.5cqw 5cqh; border-radius:8cqw;
  background:var(--card); box-shadow:var(--nm-out-lg); text-align:center;
}}
.ec--c .logo{{ width:11cqw }}
.ec--c .portrait{{ margin:0; width:38cqw; aspect-ratio:1; border-radius:50%;
                   overflow:hidden; box-shadow:var(--nm-out) }}
.ec--c .portrait img{{ width:100%; height:100%; object-fit:cover; object-position:50% 36%; display:block }}
.ec--c .titre{{ font-size:6.6cqw }}
.ec--c .accroche{{ max-width:30ch }}
.ec--c .faits{{ justify-content:center }}
.ec--c .bulles{{ display:flex; justify-content:center; gap:2.5cqw; width:100% }}
.ec--c .bulle{{ width:16cqw }}
.ec--c .bulle__rond{{ width:13.5cqw }}
.ec--c .cta{{ width:100%; margin-top:.4cqh }}

/* ---------- D : les rubriques deviennent des lignes qui se lisent ---------- */
.ec--d{{ display:flex; flex-direction:column; gap:2.6cqh; padding:5cqh var(--pad) 7cqh }}
.ec--d .tete{{ display:flex; align-items:center; gap:3cqw }}
.ec--d .logo{{ width:11cqw }}
.ec--d .tete > div{{ flex:1; min-width:0 }}
.ec--d .titre{{ font-size:5.6cqw }}
.ec--d .sous{{ margin:.4cqh 0 0; font-size:2.7cqw; color:var(--ink-soft); line-height:1.2 }}
.ec--d .pastille{{ margin:0; width:13cqw; aspect-ratio:1; border-radius:50%; overflow:hidden;
                   box-shadow:var(--nm-out); flex:none }}
.ec--d .pastille img{{ width:100%; height:100%; object-fit:cover; object-position:50% 34%; display:block }}
.ec--d .accroche{{ font-size:5.4cqw; line-height:1.25; color:var(--ink); max-width:16ch;
                   letter-spacing:-.02em }}
.ec--d .rangs{{ display:flex; flex-direction:column; gap:1.8cqh; flex:1 }}
/* Les lignes se partagent la hauteur restante au lieu de se tasser en haut :
   c'est ce qui donne des zones touchables d'une centaine de pixels, deux
   fois les bulles, et ce qui supprime le trou avant le bouton. */
.ec--d .rang{{ flex:1; display:flex; align-items:center; gap:3.4cqw; padding:2.6cqh 4cqw;
               border-radius:6.5cqw; background:var(--card); box-shadow:var(--nm-out) }}
.ec--d .rang .bulle__rond{{ width:12cqw }}
.ec--d .rang__mot{{ flex:1; min-width:0; display:flex; flex-direction:column; gap:.3cqh }}
.ec--d .rang__mot b{{ font-size:3.9cqw; font-weight:600; line-height:1.1; letter-spacing:-.015em }}
.ec--d .rang__mot em{{ font-size:2.9cqw; font-style:normal; color:var(--ink-soft); line-height:1.2 }}
.ec--d .chev{{ width:4.4cqw; height:4.4cqw; fill:none; stroke:var(--ink-soft);
               stroke-width:1.8; stroke-linecap:round; stroke-linejoin:round; flex:none; opacity:.55 }}

@media (prefers-reduced-motion:reduce){{
  *,*::before,*::after{{ animation-duration:.01ms !important; animation-delay:0s !important;
                         transition-duration:.01ms !important; transition-delay:0s !important }}
}}
'''

CORPS = ''.join(section(*m) for m in MAQUETTES)

HTML = f'''<title>Quatre accueils</title>
<style>{CSS}</style>
<div class="page">

  <header class="chapeau">
    <p class="oeil">marieemassage · page d’accueil</p>
    <h1>Quatre accueils</h1>
    <p>Quatre façons de disposer le premier écran, rendues à l’échelle réelle
    du téléphone — c’est le format de référence, et c’est par là que la
    plupart des clientes arriveront. Les quatre disent la même chose :
    <b>une promesse</b> au lieu d’une étiquette de métier, <b>le prix d’appel</b>
    et <b>« réservé aux femmes »</b> dès le premier écran, au lieu d’un clic plus loin.
    Ce qui change d’une maquette à l’autre, c’est la place que prend la photo
    et la façon dont on arrive au rendez-vous.</p>
  </header>

  {CORPS}

  <div class="fin">
    <h3>Comment choisir</h3>
    <p><b>A</b> si Marie tient à l’écran d’aujourd’hui — c’est le même, en
    mieux rempli. <b>B</b> si on veut qu’on s’arrête dessus. <b>C</b> si la
    priorité est qu’on prenne rendez-vous. <b>D</b> si la priorité est qu’on
    comprenne tout de suite ce qu’il y a derrière chaque rubrique.</p>
    <p>Rien n’oblige à en prendre une entière : le bouton de rendez-vous de
    <b>C</b> peut très bien se poser dans <b>A</b>, et les sous-titres de
    <b>D</b> pourraient devenir les infobulles des bulles actuelles.
    Dis-moi celle qui te parle et je la monte pour de vrai.</p>
  </div>

</div>
'''

SORTIE.parent.mkdir(parents=True, exist_ok=True)
SORTIE.write_text(HTML, encoding='utf-8')
print(f'{SORTIE} — {round(len(HTML.encode()) / 1024)} Ko')
