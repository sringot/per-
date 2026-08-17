#!/usr/bin/env python3
"""Compose l'affiche des tarifs à afficher dans la pièce de massage.

Un A4 autonome : polices, monogrammes et couleurs y sont embarqués, donc le
fichier s'ouvre et s'imprime partout, sans dépendre du dépôt ni d'une
connexion. C'est un document imprimable, pas une page du site — il n'est ni
listé dans le plan du site, ni indexable.

La mise en page suit celle que Marie a dessinée sur Canva : une vignette
par soin à gauche, le nom, le filet pointillé, puis les tarifs. Ce qui change, c'est l'habillage — la police, les couleurs et
les formes sont celles du site, là où Canva avait posé un titre à empattements
et des ornements qui ne venaient de nulle part.

Les tarifs et les couleurs ne sont pas ressaisis : ils viennent d'ici, et
d'ici seulement, à côté de ceux du site. Une teinte se change dans `SOINS`
et l'affiche suit.

    python3 tools-affiche.py          # écrit affiche-tarifs.html
    python3 tools-affiche.py --pdf    # et le PDF, via le navigateur
"""
import base64
import os
import pathlib
import sys

from tools_couleur import encre_lisible, hexa, melange, rgb

ROOT = pathlib.Path(__file__).parent
DEST = ROOT / 'affiche-tarifs.html'

# clé, nom, sous-titre, fond, encre du monogramme, offres
# Une offre : (durée, prix) et, s'il existe, (nombre de séances, prix du lot)
#
# L'ordre est celui de la carte de Marie, et il n'est pas alphabétique : le
# relaxant ouvre parce que c'est le soin d'appel, le drainage ferme parce
# que c'est le plus cher. Ne pas retrier.
SOINS = [
    ('relaxant', 'Relaxant', 'Massage corps complet',
     '#A9AE9D', '#3F422D',
     [(('1 heure', 60), (3, 150)), (('1 heure 30', 90), (3, 240))]),
    ('deep-tissus', 'Deep Tissus', 'Tensions profondes',
     '#FAE1AB', '#D59C40',
     [(('1 heure', 70), (3, 180))]),
    ('kobido', 'Kobido', 'Lifting japonais du visage',
     '#7E3D49', '#F8E2AF',
     [(('1 heure', 60), None)]),
    ('madero', 'Madéro', 'Soin corps remodelant',
     '#A47864', '#FDF5E8',
     [(('1 heure', 70), (5, 300))]),
    ('drainage', 'Drainage lymphatique', 'Méthode Nathalie Duarte',
     '#E39E99', '#6B3132',
     [(('1 heure', 80), (5, 350))]),
]

PACK = ('Pack combiné', 'Madéro & drainage lymphatique', 6, 390)
DECOUVERTE = 10

# Ligne supplémentaire sous le sous-titre, pour les soins qui en ont besoin.
APPUIS = {'drainage': 'De nombreux effets 🪄'}

# L'encre secondaire est un cran plus sombre que sur le site (#635D57) :
# les petits textes de l'affiche se posent sur des aplats teintés, et sur le
# forfait du drainage — le plus saturé — la valeur du site tombait à 4,5:1
# tout juste.
SOCLE, ENCRE, DOUX = '#FCF0E2', '#2A2320', '#565049'

# Groupé par deux, comme on le lit et comme on le dicte.
TEL = '06 31 18 34 81'
VILLE = 'Montigny-le-Bretonneux'

# Le logo officiel de Marie, inséré tel quel — jamais redessiné. Le fichier
# livré est un carré blanc avec le disque au milieu ; il est recadré au
# disque et détouré à l'ellipse par tools-logo-officiel.py, sans quoi ses
# angles blancs se verraient sur le socle crème.
LOGO = 'assets/img/logo-officiel.png'
# Relevées sur ce fichier, pas choisies : ce sont les deux aplats du logo.
# Elles portent tout l'accent de l'affiche — titre, cadre, blocs du bas — à
# la place du vert et de l'ocre, qui n'en venaient pas.
BORDEAUX, ROSE = '#6A2F3C', '#DC8C94'


def b64(chemin):
    return base64.b64encode((ROOT / chemin).read_bytes()).decode()


def masque(donnees):
    return (f'-webkit-mask:url(data:image/svg+xml;base64,{donnees}) center/contain no-repeat;'
            f'mask:url(data:image/svg+xml;base64,{donnees}) center/contain no-repeat')


def encre_sur(teinte, fond=SOCLE, vise=4.5):
    """Teinte du soin, poussée jusqu'à `vise` sur le fond qui l'accueille.

    Les noms des soins sont écrits à même le papier, pas sur un aplat : la
    sauge y tombe à 1,9:1 et le jaune du deep tissus à 1,2:1. On garde la
    teinte — c'est elle qui identifie le soin — et l'on ne joue que sur sa
    clarté.
    """
    return hexa(encre_lisible(rgb(teinte), rgb(fond), vise))


def prix(n):
    return f'{n}&nbsp;€'


def bloc(cle, nom, sous, fond, encre, offres):
    groupes = []
    for (duree, px), forfait in offres:
        abo = ''
        if forfait:
            lot, px_lot = forfait
            # L'économie est calculée, jamais saisie : un tarif qui change la
            # met à jour, et une addition fausse devient impossible.
            abo = (f'<p class="abo">Abonnement = {lot} séances pour '
                   f'{prix(px_lot)}<em>au lieu de {prix(px * lot)}</em></p>')
        groupes.append(
            f'<div class="groupe"><p class="ligne">{duree} — <b>{prix(px)}</b></p>{abo}</div>')

    appui = APPUIS.get(cle)
    appui = f'<p class="appui">{appui}</p>' if appui else ''

    return f'''
    <article class="soin" style="--fond:{fond};--encre:{encre};--titre:{encre_sur(fond)}">
      <div class="vignette"><span class="mono" style="{masque(b64(f'assets/img/soins/{cle}.svg'))}"></span></div>
      <div class="corps">
        <h2>{nom}</h2>
        <p class="sous">{sous}</p>
        {appui}
        <div class="groupes">{''.join(groupes)}</div>
      </div>
    </article>'''


def main():
    nom_pack, sous_pack, lot_pack, prix_pack = PACK
    # Même calcul que pour les noms de soins, appliqué au fond dilué du
    # bloc du pack.
    titre_pack = encre_sur(BORDEAUX, hexa(melange(rgb(BORDEAUX), rgb(SOCLE), .11)))

    html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Tarifs — marieemassage</title>
<meta name="robots" content="noindex">
<style>
@font-face{{
  font-family:'Figtree'; font-style:normal; font-weight:400 600;
  font-display:block;
  src:url(data:font/woff2;base64,{b64('assets/fonts/figtree-400-latin.woff2')}) format('woff2');
}}

/* Une feuille A4, sans marge d'impression : la marge est dans le dessin,
   pas dans le réglage du navigateur — sinon elle change d'une imprimante
   à l'autre et la composition se décale. */
@page{{ size:A4; margin:0; }}
*,*::before,*::after{{ box-sizing:border-box; margin:0; padding:0; }}

html{{ background:#E8E2D8; }}
body{{
  font-family:'Figtree',system-ui,sans-serif;
  color:{ENCRE};
  /* Les aplats de couleur doivent sortir à l'impression : par défaut les
     navigateurs les suppriment pour économiser l'encre, et l'affiche
     arriverait en blanc sur blanc. */
  -webkit-print-color-adjust:exact; print-color-adjust:exact;
  display:grid; place-items:center; padding:20px;
}}
.feuille{{
  width:210mm; height:297mm; background:{SOCLE};
  padding:15mm 14mm 11mm;
  display:flex; flex-direction:column;
  position:relative; overflow:hidden;
  box-shadow:0 8mm 20mm -10mm rgba(42,35,32,.4);
}}
/* Cette règle passe avant celle du cadre, et pas après : à spécificité
   égale c'est la dernière qui gagne, et déclarée plus bas elle rendait le
   cadre `relative`. Il reprenait alors sa place dans la colonne au lieu de
   se poser par-dessus, et son filet traversait le logo. */
.feuille > *{{ position:relative; }}
/* Le double filet de Marie, sans les rinceaux : le cadre fait l'affiche,
   les ornements venaient de la bibliothèque de Canva. */
.cadre{{
  position:absolute; inset:7mm; pointer-events:none;
  border:.35mm solid color-mix(in srgb, {BORDEAUX} 30%, {SOCLE});
  border-radius:2.5mm;
}}
.cadre::before{{
  content:''; position:absolute; inset:1.6mm;
  border:.2mm solid color-mix(in srgb, {BORDEAUX} 16%, {SOCLE});
  border-radius:1.4mm;
}}

/* ---- En-tête ---- */
header{{ text-align:center; margin-bottom:6mm; }}
.logo{{ width:14mm; height:14mm; display:block; margin:0 auto 2.6mm; }}
/* « Tarifs massage » est le titre de la feuille — c'est ce qu'on doit lire
   depuis l'autre bout de la pièce. Il est composé comme les noms de soins,
   en plus grand : capitales et interlettrage large donnaient l'impression
   d'une seconde police alors que c'est la même. */
.titre{{
  font-size:11mm; font-weight:600; line-height:1;
  letter-spacing:-.025em; color:{BORDEAUX};
}}
.marque{{
  margin-top:2.4mm;
  font-size:3.4mm; font-weight:600; letter-spacing:-.01em; color:{ENCRE};
}}

/* ---- Les soins ---- */
.soins{{ display:flex; flex-direction:column; gap:4mm; }}
.soin{{ display:grid; grid-template-columns:26mm 1fr; gap:6mm; align-items:stretch; }}
/* Vignette rectangulaire, comme sur le Canva : le disque est la forme du
   site, mais ici les cinq vignettes forment une colonne, et un rectangle
   arrondi la tient mieux qu'un cercle.

   Sa hauteur suit celle de son rang plutôt que d'être fixe : c'est la seule
   façon d'obtenir le même écart entre toutes les vignettes, puisque les
   rangs eux-mêmes ne peuvent pas être égaux — le relaxant a deux durées et
   deux abonnements là où le Kobido n'a qu'un prix. */
.vignette{{
  width:26mm; min-height:28mm; border-radius:3.4mm;
  background:var(--fond); display:grid; place-items:center;
}}
.mono{{ width:13.4mm; height:13.9mm; display:block; background:var(--encre); }}
.corps{{ padding-top:1.5mm; }}
.corps h2{{
  display:flex; align-items:center; gap:3mm;
  font-size:5mm; font-weight:600; line-height:1.1; color:var(--titre);
}}
.corps h2 i{{ font-style:normal; }}
/* Le filet pointillé prend la place qui reste : il tient la colonne des
   noms sans qu'on ait à lui fixer une longueur qui se décalerait au
   moindre changement de nom. */
.corps h2::after{{
  content:''; flex:1; height:0;
  border-bottom:.3mm dotted color-mix(in srgb, var(--fond) 60%, {SOCLE});
}}
.sous{{
  margin-top:1mm;
  font-size:3.1mm; font-weight:500; letter-spacing:.11em;
  text-transform:uppercase; color:{DOUX};
}}
.appui{{ margin-top:1mm; font-size:3.3mm; color:{ENCRE}; }}
.groupes{{ margin-top:2.4mm; display:flex; flex-direction:column; gap:2.2mm; }}
/* La durée et son prix sont ce qu'une cliente cherche sur cette feuille :
   ils passent devant l'abonnement, par la taille et par l'encre pleine, et
   non par une couleur de plus. */
.ligne{{ font-size:4mm; color:{ENCRE}; }}
.ligne b{{ font-size:6.4mm; font-weight:600; color:{ENCRE};
  font-variant-numeric:tabular-nums; }}
/* L'abonnement était à 12 px, lisible sur un écran mais pas sur un mur.
   Il monte à 14 px et se pose sur un aplat de sa propre teinte : ce fond
   le détache du papier et le rattache au prix qu'il prolonge, ce qu'une
   ligne de texte nue ne faisait ni l'un ni l'autre. */
.abo{{
  margin-top:1.2mm; padding:1.5mm 3mm; border-radius:2.4mm;
  background:color-mix(in srgb, var(--fond) 20%, {SOCLE});
  font-size:3.7mm; color:{ENCRE};
  display:inline-flex; align-items:baseline; gap:2.5mm;
}}
.abo em{{ font-style:normal; font-size:3.3mm; color:{DOUX}; }}

/* ---- Le pack et l'offre de découverte ----
   Marie trouvait que le pack ressortait trop : il ne s'adresse qu'aux
   habituées. Il reste au niveau d'un soin, et l'aplat plein va à la remise,
   qui est ce qui fait franchir la porte une première fois. */
.extras{{ margin-top:5mm; display:flex; gap:4mm; }}
.pack,.decouverte{{ flex:1; border-radius:4mm; padding:4mm 5.5mm; }}
.pack{{ background:color-mix(in srgb, {BORDEAUX} 11%, {SOCLE}); }}
.pack b{{ display:block; font-size:3.8mm; font-weight:600; color:{titre_pack}; }}
.pack span{{ display:block; margin-top:.8mm; font-size:3.2mm; color:{DOUX}; }}
.decouverte{{
  background:{BORDEAUX}; color:#FFF;
  display:flex; align-items:center; justify-content:center; gap:3.4mm;
}}
/* Le disque bordeaux et son M rose, à plat : le bloc reprend le logo mot
   pour mot au lieu d'inventer une couleur d'accent. */
.decouverte b{{ font-size:7mm; font-weight:600; line-height:1; color:{ROSE};
  white-space:nowrap; font-variant-numeric:tabular-nums; }}
.decouverte span{{ font-size:3.1mm; line-height:1.3; }}

/* ---- Pied ---- */
footer{{
  margin-top:auto; padding-top:5mm; text-align:center;
  border-top:.3mm solid rgba(42,35,32,.12);
}}
.tel{{ font-size:4.4mm; font-weight:600; color:{BORDEAUX}; }}
.mention{{ margin-top:1.4mm; font-size:2.6mm; color:{DOUX}; }}

@media print{{
  html{{ background:#FFF; }}
  body{{ padding:0; display:block; }}
  .feuille{{ box-shadow:none; }}
}}
</style>
</head>
<body>
<div class="feuille">
  <div class="cadre" aria-hidden="true"></div>

  <header>
    <img class="logo" src="data:image/png;base64,{b64(LOGO)}" alt="" width="300" height="300">
    <h1 class="titre">Tarifs Massage</h1>
    <p class="marque">marieemassage</p>
  </header>

  <section class="soins">{''.join(bloc(*s) for s in SOINS)}
  </section>

  <section class="extras">
    <p class="pack"><b>{nom_pack} — {prix(prix_pack)}</b>
      <span>{sous_pack}, {lot_pack} séances</span></p>
    <p class="decouverte"><b>−{DECOUVERTE}&nbsp;€</b>
      <span>sur votre massage inédit</span></p>
  </section>

  <footer>
    <p class="tel">Sur rendez-vous · {TEL}</p>
    <p class="mention">{VILLE} · Les massages proposés sont des soins de bien-être, non thérapeutiques.</p>
  </footer>

</div>
</body>
</html>
'''
    DEST.write_text(html, encoding='utf-8')
    print(f'{DEST.name} — {len(html.encode()) / 1024:.0f} Ko')

    if '--pdf' in sys.argv:
        import subprocess
        # Playwright est installé globalement ici ; node ne remonte pas jusqu'au
        # node_modules global tout seul, on le lui indique.
        env = dict(os.environ)
        racine = subprocess.run(['npm', 'root', '-g'], capture_output=True,
                                text=True, check=True).stdout.strip()
        env['NODE_PATH'] = racine
        subprocess.run(['node', str(ROOT / 'tools-affiche-pdf.js')],
                       check=True, env=env)


if __name__ == '__main__':
    main()
