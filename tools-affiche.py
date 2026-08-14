#!/usr/bin/env python3
"""Compose l'affiche des tarifs à afficher dans la pièce de massage.

Un A4 autonome : polices, monogrammes et couleurs y sont embarqués, donc le
fichier s'ouvre et s'imprime partout, sans dépendre du dépôt ni d'une
connexion. C'est un document imprimable, pas une page du site — il n'est ni
listé dans le plan du site, ni indexable.

Les tarifs et les couleurs ne sont pas ressaisis : ils viennent d'ici, et
d'ici seulement, à côté de ceux du site. Une teinte se change dans `SOINS`
et l'affiche suit.

    python3 tools-affiche.py          # écrit affiche-tarifs.html
    python3 tools-affiche.py --pdf    # et le PDF, via le navigateur

Marie n'a pas de « Deep Tissus » sur sa carte : elle l'a mis de côté pour
le moment. L'affiche s'en tient donc à quatre soins, là où le site en
présente cinq.
"""
import base64
import os
import pathlib
import sys

from tools_couleur import contraste, encre_lisible, hexa, melange, rgb

ROOT = pathlib.Path(__file__).parent
DEST = ROOT / 'affiche-tarifs.html'

# clé, nom, sous-titre, fond, encre du monogramme, offres
# Une offre : (durée, prix) et, s'il existe, (nombre de séances, prix du lot)
#
# L'ordre est celui voulu par Marie, et il n'est pas alphabétique : le
# relaxant ouvre parce que c'est le soin d'appel, le drainage ferme parce
# que c'est le plus cher. Ne pas retrier.
SOINS = [
    ('relaxant', 'Relaxant', 'Massage corps complet',
     '#A9AE9D', '#3F422D',
     [(('1 h', 60), (3, 150)), (('1 h 30', 90), (3, 240))]),
    ('kobido', 'Kobido', 'Lifting japonais du visage',
     '#7E3D49', '#F8E2AF',
     [(('1 h', 60), None)]),
    ('madero', 'Madéro', 'Soin corps remodelant',
     '#D15929', '#FDF5E8',
     [(('1 h', 70), (5, 300))]),
    ('drainage', 'Drainage lymphatique', 'Méthode Nathalie Duarte',
     '#E39E99', '#6B3132',
     [(('1 h', 80), (5, 350))]),
]

PACK = ('Pack combiné', '3 Madéro & 3 drainages lymphatiques', 6, 390)
DECOUVERTE = 10

# L'encre secondaire est un cran plus sombre que sur le site (#635D57) :
# les petits textes de l'affiche se posent sur des aplats teintés, et sur le
# forfait du drainage — le plus saturé — la valeur du site tombait à 4,5:1
# tout juste. Relevé sur le rendu : 5,0:1 au pire cas après correction.
SOCLE, ENCRE, DOUX, VERT, OCRE = '#FCF0E2', '#2A2320', '#565049', '#3F4A38', '#AC4B28'

# Groupé par deux, comme on le lit et comme on le dicte.
TEL = '06 31 18 34 81'
VILLE = 'Montigny-le-Bretonneux'

# Le monogramme du logo, posé dans un disque comme les pastilles des soins.
# Marie a proposé deux accords ; celui-ci tient à l'impression (3,6:1 entre
# le M et son disque, 7:1 entre le disque et le papier). L'autre — M jaune
# sur disque rose — tombe à 1,7:1 et s'efface une fois imprimé.
LOGO_FOND, LOGO_ENCRE = '#7E3D49', '#E39E99'


def b64(chemin):
    return base64.b64encode((ROOT / chemin).read_bytes()).decode()


# Ligne supplémentaire sous le sous-titre, pour les soins qui en ont besoin.
APPUIS = {'drainage': 'De nombreux effets 🪄'}

# Part de la teinte du soin dans le fond de son bloc, et dans celui de ses
# forfaits. Ces valeurs sont aussi celles du CSS plus bas : les changer ici
# suffit, le contraste des titres est recalculé dessus.
PART_BLOC, PART_FORFAIT = .12, .19


def bloc(cle, nom, sous, fond, encre, offres):
    lignes = []
    for (duree, prix), forfait in offres:
        lignes.append(
            f'<div class="ligne">'
            f'<span class="duree">{duree}</span>'
            f'<span class="prix">{prix}&nbsp;€</span></div>')
        if forfait:
            lot, px = forfait
            # L'économie est calculée, jamais saisie : un tarif qui change la
            # met à jour, et une addition fausse devient impossible.
            lignes.append(
                f'<div class="ligne ligne--forfait">'
                f'<span class="duree">Forfait {lot} séances de {duree}</span>'
                f'<span class="prix">{px}&nbsp;€'
                f'<em>au lieu de {prix * lot}&nbsp;€</em></span></div>')
    # Le titre prend la couleur du soin — mais pas sa couleur brute : posée
    # sur le fond de son propre bloc, la sauge tomberait à 1,7:1 et le rose
    # à 1,5:1. On la pousse jusqu'à 4,5:1 en gardant la teinte, par le même
    # calcul que celui des cartes du site.
    fond_bloc = melange(rgb(fond), rgb(SOCLE), PART_BLOC)
    titre = hexa(encre_lisible(rgb(fond), fond_bloc))

    appui = APPUIS.get(cle)
    appui = f'<p class="appui">{appui}</p>' if appui else ''

    return f'''
    <article class="soin" style="--fond:{fond}; --encre:{encre}; --titre:{titre}">
      <div class="pastille"><span class="mono mono--{cle}"></span></div>
      <div class="titres">
        <h2>{nom}</h2>
        <p>{sous}</p>
        {appui}
      </div>
      <div class="offres">{''.join(lignes)}</div>
    </article>'''


def main():
    monos = {cle: b64(f'assets/img/soins/{cle}.svg') for cle, *_ in SOINS}
    masques = '\n'.join(
        f'.mono--{cle}{{ -webkit-mask-image:url(data:image/svg+xml;base64,{d});'
        f' mask-image:url(data:image/svg+xml;base64,{d}); }}'
        for cle, d in monos.items())
    logo_svg = b64('assets/img/logo.svg')

    nom_pack, sous_pack, lot_pack, prix_pack = PACK
    # Même correction que pour les titres de soins : l'ocre pur tombait à
    # 4,2:1 sur le fond dilué de son propre bloc.
    titre_pack = hexa(encre_lisible(rgb(OCRE),
                                    melange(rgb(OCRE), rgb(SOCLE), PART_BLOC)))

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
  padding:16mm 15mm 12mm;
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
.feuille > *{{ position:relative; }}

/* ---- En-tête ---- */
header{{ text-align:center; margin-bottom:5.5mm; }}
/* Le logo reprend la forme des pastilles des soins : même disque, même
   monogramme détouré. L'affiche n'a ainsi qu'un seul motif, décliné. */
.logo{{
  width:16mm; height:16mm; border-radius:50%;
  background:{LOGO_FOND};
  margin:0 auto 3.5mm; display:grid; place-items:center;
}}
.logo span{{
  width:8.7mm; height:9mm; display:block;
  background:{LOGO_ENCRE};
  -webkit-mask:url(data:image/svg+xml;base64,{logo_svg}) center/contain no-repeat;
          mask:url(data:image/svg+xml;base64,{logo_svg}) center/contain no-repeat;
}}
.marque{{
  font-size:5.2mm; font-weight:600; letter-spacing:-.02em;
  line-height:1; color:{VERT};
}}
/* « Tarifs » est le titre de la feuille — c'est ce qu'on doit lire depuis
   l'autre bout de la pièce, avant même le nom. */
.titre{{
  margin-top:2.6mm;
  font-size:11mm; font-weight:600; line-height:1;
  letter-spacing:.06em; text-transform:uppercase; color:{OCRE};
}}

/* ---- Les soins ---- */
.soins{{ display:flex; flex-direction:column; gap:4.4mm; }}
.soin{{
  display:grid; grid-template-columns:21mm 1fr auto;
  align-items:center; gap:5mm;
  padding:5.8mm 6mm;
  border-radius:5.5mm;
  background:color-mix(in srgb, var(--fond) 12%, {SOCLE});
}}
.pastille{{
  width:21mm; height:21mm; border-radius:50%;
  background:var(--fond);
  display:grid; place-items:center;
}}
.mono{{
  width:11.6mm; height:11.6mm; display:block;
  background:var(--encre);
  -webkit-mask-repeat:no-repeat; mask-repeat:no-repeat;
  -webkit-mask-position:center;  mask-position:center;
  -webkit-mask-size:contain;     mask-size:contain;
}}
{masques}
.titres h2{{
  font-size:5mm; font-weight:600; line-height:1.1; color:var(--titre);
  letter-spacing:-.01em;
}}
.titres p{{
  margin-top:.8mm;
  font-size:2.8mm; font-weight:500; letter-spacing:.14em;
  text-transform:uppercase; color:{DOUX};
}}
.titres .appui{{
  margin-top:1.2mm;
  font-size:3.1mm; font-weight:400; letter-spacing:0;
  text-transform:none; color:{ENCRE};
}}
.offres{{ display:flex; flex-direction:column; gap:1.6mm; min-width:62mm; }}
.ligne{{
  display:flex; align-items:baseline; justify-content:space-between;
  gap:4mm;
}}
.duree{{ font-size:3.3mm; color:{DOUX}; }}
.prix{{
  font-size:5.4mm; font-weight:600; white-space:nowrap;
  text-align:right; line-height:1.1;
  font-variant-numeric:tabular-nums;
}}
/* Le forfait est une option de la durée au-dessus : plus petit, en retrait,
   et sur un fond creusé pour qu'on voie qu'il forme un bloc avec elle. */
.ligne--forfait{{
  margin-top:-.4mm; padding:1.6mm 2.6mm;
  border-radius:2.4mm;
  background:color-mix(in srgb, var(--fond) 19%, {SOCLE});
}}
.ligne--forfait .duree{{ font-size:2.9mm; color:{ENCRE}; }}
.ligne--forfait .prix{{ font-size:4mm; }}
.prix em{{
  display:block; font-style:normal; font-weight:500;
  font-size:2.5mm; color:{DOUX};
}}

/* ---- Le pack et l'offre de découverte ----
   Les deux blocs ont échangé leur poids. Le pack ne s'adresse qu'aux
   habituées et criait plus fort que les tarifs eux-mêmes : il redescend au
   même niveau qu'un soin. La remise, elle, est ce qui fait franchir la
   porte une première fois — c'est elle qui mérite l'aplat. */
.extras{{ margin-top:5.5mm; display:flex; flex-direction:column; gap:3.5mm; }}
.pack{{
  display:grid; grid-template-columns:1fr auto; align-items:center; gap:5mm;
  padding:5mm 6mm; border-radius:5.5mm;
  background:color-mix(in srgb, {OCRE} 12%, {SOCLE});
}}
.pack h3{{ font-size:4.2mm; font-weight:600; line-height:1.1; color:{titre_pack}; }}
.pack p{{ margin-top:.9mm; font-size:3mm; color:{DOUX}; }}
.pack .prix{{ font-size:6mm; color:{ENCRE}; }}
.pack .prix span{{
  display:block; font-size:2.7mm; font-weight:500; color:{DOUX};
}}
.decouverte{{
  display:flex; align-items:center; justify-content:center; gap:4mm;
  padding:5mm; border-radius:5.5mm;
  background:{OCRE}; color:#FFF; text-align:left;
}}
.decouverte b{{
  font-size:9mm; font-weight:600; line-height:1;
  white-space:nowrap; font-variant-numeric:tabular-nums;
}}
.decouverte span{{ font-size:3.6mm; line-height:1.3; }}

/* ---- Pied ---- */
footer{{
  margin-top:auto; padding-top:6mm; text-align:center;
  border-top:.3mm solid rgba(42,35,32,.12);
}}
.tel{{ font-size:4.6mm; font-weight:600; color:{VERT}; letter-spacing:.01em; }}
.mention{{ margin-top:1.6mm; font-size:2.7mm; color:{DOUX}; }}

@media print{{
  html{{ background:#FFF; }}
  body{{ padding:0; display:block; }}
  .feuille{{ box-shadow:none; }}
}}
</style>
</head>
<body>
<div class="feuille">

  <header>
    <div class="logo"><span></span></div>
    <div class="marque">marieemassage</div>
    <h1 class="titre">Tarifs</h1>
  </header>

  <section class="soins">{''.join(bloc(*s) for s in SOINS)}
  </section>

  <section class="extras">
    <div class="pack">
      <div>
        <h3>{nom_pack}</h3>
        <p>{sous_pack}</p>
      </div>
      <div class="prix">{prix_pack}&nbsp;€<span>{lot_pack} séances</span></div>
    </div>
    <p class="decouverte">
      <b>−{DECOUVERTE}&nbsp;€</b>
      <span>sur votre massage inédit</span>
    </p>
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
