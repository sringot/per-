#!/usr/bin/env python3
"""Compose l'affiche des tarifs à afficher dans la pièce de massage.

Un A4 autonome : polices, monogrammes et couleurs y sont embarqués, donc le
fichier s'ouvre et s'imprime partout, sans dépendre du dépôt ni d'une
connexion. C'est un document imprimable, pas une page du site — il n'est ni
listé dans le plan du site, ni indexable.

La mise en page suit celle que Marie a dessinée sur Canva : une vignette
par soin à gauche, le nom précédé de son initiale, le filet pointillé, puis
les tarifs. Ce qui change, c'est l'habillage — la police, les couleurs et
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

# clé, initiale, nom, sous-titre, fond, encre du monogramme, offres
# Une offre : (durée, prix) et, s'il existe, (nombre de séances, prix du lot)
#
# L'ordre est celui de la carte de Marie, et il n'est pas alphabétique : le
# relaxant ouvre parce que c'est le soin d'appel, le drainage ferme parce
# que c'est le plus cher. Ne pas retrier.
#
# Les initiales sont celles des monogrammes, pas des noms : le deep tissus
# est signé d'un T. C'est ce qui permet de le distinguer du drainage, qui
# prend le D.
SOINS = [
    ('relaxant', 'R', 'Relaxant', 'Massage corps complet',
     '#A9AE9D', '#3F422D',
     [(('1 heure', 60), (3, 150)), (('1 heure 30', 90), (3, 240))]),
    ('deep-tissus', 'T', 'Deep Tissus', 'Tensions profondes',
     '#FAE1AB', '#D59C40',
     [(('1 heure', 70), (3, 180))]),
    ('kobido', 'K', 'Kobido', 'Lifting japonais du visage',
     '#7E3D49', '#F8E2AF',
     [(('1 heure', 60), None)]),
    ('madero', 'M', 'Madéro', 'Soin corps remodelant',
     '#D15929', '#FDF5E8',
     [(('1 heure', 70), (5, 300))]),
    ('drainage', 'D', 'Drainage lymphatique', 'Méthode Nathalie Duarte',
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
SOCLE, ENCRE, DOUX, VERT, OCRE = '#FCF0E2', '#2A2320', '#565049', '#3F4A38', '#AC4B28'

# Groupé par deux, comme on le lit et comme on le dicte.
TEL = '06 31 18 34 81'
VILLE = 'Montigny-le-Bretonneux'

# Le monogramme du logo, posé dans un disque. Marie a proposé deux accords ;
# celui-ci tient à l'impression (3,6:1 entre le M et son disque, 7:1 entre le
# disque et le papier). L'autre — M jaune sur disque rose — tombe à 1,7:1 et
# s'efface une fois imprimé.
LOGO_FOND, LOGO_ENCRE = '#7E3D49', '#E39E99'


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


def bloc(cle, initiale, nom, sous, fond, encre, offres):
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
        <h2><i>{initiale}</i> — {nom}</h2>
        <p class="sous">{sous}</p>
        {appui}
        <div class="groupes">{''.join(groupes)}</div>
      </div>
    </article>'''


def main():
    nom_pack, sous_pack, lot_pack, prix_pack = PACK
    # Même correction que pour les noms de soins : l'ocre pur tombe à 4,2:1
    # sur le fond dilué de son propre bloc.
    titre_pack = encre_sur(OCRE, hexa(melange(rgb(OCRE), rgb(SOCLE), .12)))

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
/* Une seule tache de couleur, très diluée, dans l'angle — la même idée que
   le fond du site, en beaucoup plus discret : sur papier, un dégradé large
   se banderait à l'impression. */
.feuille::before{{
  content:''; position:absolute; right:-30mm; top:-30mm;
  width:110mm; height:110mm; border-radius:50%;
  background:radial-gradient(circle, rgba(242,231,179,.55) 0%, transparent 70%);
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
  border:.35mm solid color-mix(in srgb, {OCRE} 34%, {SOCLE});
  border-radius:2.5mm;
}}
.cadre::before{{
  content:''; position:absolute; inset:1.6mm;
  border:.2mm solid color-mix(in srgb, {OCRE} 20%, {SOCLE});
  border-radius:1.4mm;
}}

/* ---- En-tête ---- */
header{{ text-align:center; margin-bottom:6mm; }}
.logo{{
  width:12mm; height:12mm; border-radius:50%;
  background:{LOGO_FOND};
  margin:0 auto 2.4mm; display:grid; place-items:center;
}}
.logo span{{
  width:6.5mm; height:6.7mm; display:block;
  background:{LOGO_ENCRE};
  {masque(b64('assets/img/logo.svg'))};
}}
/* « Tarifs massage » est le titre de la feuille — c'est ce qu'on doit lire
   depuis l'autre bout de la pièce. L'interlettrage remplace les empattements
   du Canva : il donne la même solennité sans changer de police. */
.titre{{
  font-size:9.4mm; font-weight:600; line-height:1;
  letter-spacing:.13em; text-transform:uppercase; color:{OCRE};
}}
.marque{{
  margin-top:2.2mm;
  font-size:3.4mm; font-weight:600; letter-spacing:-.01em; color:{VERT};
}}

/* ---- Les soins ---- */
.soins{{ display:flex; flex-direction:column; gap:4.4mm; }}
.soin{{ display:grid; grid-template-columns:26mm 1fr; gap:6mm; align-items:start; }}
/* Vignette rectangulaire, comme sur le Canva : le disque est la forme du
   site, mais ici les cinq vignettes forment une colonne, et un rectangle
   arrondi la tient mieux qu'un cercle. */
.vignette{{
  width:26mm; height:33mm; border-radius:3.4mm;
  background:var(--fond); display:grid; place-items:center;
}}
.mono{{ width:14mm; height:14.5mm; display:block; background:var(--encre); }}
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
  font-size:2.7mm; font-weight:500; letter-spacing:.13em;
  text-transform:uppercase; color:{DOUX};
}}
.appui{{ margin-top:1mm; font-size:3mm; color:{ENCRE}; }}
.groupes{{ margin-top:2.6mm; display:flex; flex-direction:column; gap:2.4mm; }}
.ligne{{ font-size:3.6mm; color:{DOUX}; }}
.ligne b{{ font-size:4.6mm; font-weight:600; color:{ENCRE};
  font-variant-numeric:tabular-nums; }}
.abo{{
  margin-top:.8mm; font-size:3.2mm; color:{ENCRE};
  display:flex; align-items:baseline; gap:2.5mm;
}}
.abo em{{ font-style:normal; font-size:2.7mm; color:{DOUX}; }}

/* ---- Le pack et l'offre de découverte ----
   Marie trouvait que le pack ressortait trop : il ne s'adresse qu'aux
   habituées. Il reste au niveau d'un soin, et l'aplat plein va à la remise,
   qui est ce qui fait franchir la porte une première fois. */
.extras{{ margin-top:5mm; display:flex; gap:4mm; }}
.pack,.decouverte{{ flex:1; border-radius:4mm; padding:4mm 5.5mm; }}
.pack{{ background:color-mix(in srgb, {OCRE} 12%, {SOCLE}); }}
.pack b{{ display:block; font-size:3.8mm; font-weight:600; color:{titre_pack}; }}
.pack span{{ display:block; margin-top:.8mm; font-size:2.9mm; color:{DOUX}; }}
.decouverte{{
  background:{OCRE}; color:#FFF;
  display:flex; align-items:center; justify-content:center; gap:3.4mm;
}}
.decouverte b{{ font-size:7mm; font-weight:600; line-height:1;
  white-space:nowrap; font-variant-numeric:tabular-nums; }}
.decouverte span{{ font-size:3.1mm; line-height:1.3; }}

/* ---- Pied ---- */
footer{{
  margin-top:auto; padding-top:5mm; text-align:center;
  border-top:.3mm solid rgba(42,35,32,.12);
}}
.tel{{ font-size:4.4mm; font-weight:600; color:{VERT}; }}
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
    <div class="logo"><span></span></div>
    <h1 class="titre">Tarifs massage</h1>
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
