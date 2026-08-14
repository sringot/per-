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
SOINS = [
    ('kobido', 'Kobido', 'Lifting japonais du visage',
     '#7E3D49', '#F8E2AF',
     [(('1 h', 60), None)]),
    ('relaxant', 'Relaxant', 'Massage corps complet',
     '#A9AE9D', '#3F422D',
     [(('1 h', 60), (3, 160)), (('1 h 30', 90), (3, 240))]),
    ('madero', 'Madéro', 'Soin corps remodelant',
     '#D15929', '#FDF5E8',
     [(('1 h', 70), (5, 300))]),
    ('drainage', 'Drainage lymphatique', 'Méthode Nathalie Duarte',
     '#E39E99', '#6B3132',
     [(('1 h', 80), (5, 350))]),
]

# ⚠️ Deux valeurs relevées sur la carte de Marie, dont l'export était brouillé
# par des superpositions. À confirmer avec elle avant impression.
PACK = ('Pack combiné', 'Madéro & drainage lymphatique', 6, 390)
DECOUVERTE = ('Massage découverte', 10)

# L'encre secondaire est un cran plus sombre que sur le site (#635D57) :
# les petits textes de l'affiche se posent sur des aplats teintés, et sur le
# forfait du drainage — le plus saturé — la valeur du site tombait à 4,5:1
# tout juste. Relevé sur le rendu : 5,0:1 au pire cas après correction.
SOCLE, ENCRE, DOUX, VERT, OCRE = '#FCF0E2', '#2A2320', '#565049', '#3F4A38', '#AC4B28'

# Groupé par deux, comme on le lit et comme on le dicte.
TEL = '06 31 18 34 81'


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
            gain = prix * lot - px
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

    nom_pack, sous_pack, lot_pack, prix_pack = PACK
    nom_dec, remise_dec = DECOUVERTE

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
header{{ text-align:center; margin-bottom:8mm; }}
.logo{{ width:13mm; margin:0 auto 3mm; display:block; }}
.marque{{
  font-size:7.6mm; font-weight:600; letter-spacing:-.03em;
  line-height:1; color:{VERT};
}}
.sur-titre{{
  margin-top:2.5mm;
  font-size:2.5mm; font-weight:500; letter-spacing:.42em;
  text-transform:uppercase; color:{OCRE};
}}

/* ---- Les soins ---- */
.soins{{ display:flex; flex-direction:column; gap:5mm; }}
.soin{{
  display:grid; grid-template-columns:21mm 1fr auto;
  align-items:center; gap:5mm;
  padding:6.5mm 6mm;
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

/* ---- Le pack et l'offre de découverte ---- */
.extras{{ margin-top:6mm; display:flex; flex-direction:column; gap:3.5mm; }}
.pack{{
  display:grid; grid-template-columns:1fr auto; align-items:center; gap:5mm;
  padding:6.5mm 7mm; border-radius:5.5mm;
  background:{OCRE}; color:#FFF;
}}
.pack h3{{ font-size:4.6mm; font-weight:600; line-height:1.1; }}
.pack p{{ margin-top:1mm; font-size:3mm; opacity:.92; }}
.pack .prix{{ font-size:8mm; color:#FFF; }}
.pack .prix span{{ display:block; font-size:2.8mm; font-weight:500; opacity:.9; }}
.decouverte{{
  text-align:center; padding:4.4mm 5mm; border-radius:4mm;
  border:.4mm dashed color-mix(in srgb, {OCRE} 45%, {SOCLE});
  font-size:3.4mm; color:{ENCRE};
}}
.decouverte b{{ color:{OCRE}; font-weight:600; }}

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
    <img class="logo" src="data:image/png;base64,{b64('assets/img/logo-mark.png')}" alt="">
    <div class="marque">marieemassage</div>
    <p class="sur-titre">Tarifs</p>
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
      <b>{nom_dec}</b> — <b>−{remise_dec}&nbsp;€</b> sur votre premier massage.
    </p>
  </section>

  <footer>
    <p class="tel">Sur rendez-vous · {TEL}</p>
    <p class="mention">Voisins-le-Bretonneux · Les massages proposés sont des soins de bien-être, non thérapeutiques.</p>
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
