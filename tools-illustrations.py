#!/usr/bin/env python3
"""Génère le jeu d'illustrations plates de Marie Massage.

Toutes les scènes partagent la même palette et les mêmes primitives
(tête, main, feuille, bougie, flacon) pour rester cohérentes entre elles.
"""
import pathlib

OUT = pathlib.Path('/home/user/per-/assets/img/illus')
OUT.mkdir(parents=True, exist_ok=True)

# ---- Palette ----
TERRA   = '#D9643C'
TERRA_L = '#E5825A'
OCHRE   = '#C15A32'
SAGE    = '#A7AE9B'
SAGE_D  = '#7C8873'
OLIVE   = '#9A8B5F'
YELLOW  = '#F2E7B3'
YELLOW_D= '#E3D18C'
CREAM   = '#FBF3E4'
SKIN    = '#F2B98F'
SKIN_D  = '#DFA173'
HAIR    = '#3E3228'
WOOD    = '#5C4A38'
INK     = '#40382C'


def head(cx, cy, r, hair=HAIR, skin=SKIN, bun=True):
    """Tête de profil trois-quarts, yeux clos."""
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{skin}"/>'
    s += (f'<path d="M{cx-r} {cy-2}a{r} {r} 0 0 1 {2*r} -{r*0.3}'
          f'c-{r*0.25} {r*0.42} -{r*0.75} {r*0.55} -{r*1.2} {r*0.4}'
          f'c-{r*0.35} -{r*0.1} -{r*0.65} 0 -{r*0.8} {r*0.05}Z" fill="{hair}"/>')
    if bun:
        s += f'<circle cx="{cx+r*0.05}" cy="{cy-r*1.13}" r="{r*0.41}" fill="{hair}"/>'
    s += (f'<path d="M{cx-r*0.42} {cy+r*0.34}q{r*0.17} {r*0.15} {r*0.34} 0" '
          f'stroke="{SKIN_D}" stroke-width="{max(2,r*0.075)}" fill="none" stroke-linecap="round"/>')
    return s


def arm(x, y, w, h, skin=SKIN):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w/2}" fill="{skin}"/>'


def hand(x, y, w=54, h=44, skin=SKIN, fingers=4, rot=0):
    """Main vue de dessus, doigts vers le bas."""
    s = (f'<path d="M{x} {y}h{w}a{w*0.26} {w*0.26} 0 0 1 {w*0.26} {w*0.26}'
         f'v{h*0.5}a{h*0.55} {h*0.55} 0 0 1 -{h*0.55} {h*0.55}'
         f'h-{w*0.72}a{h*0.55} {h*0.55} 0 0 1 -{h*0.55} -{h*0.55}'
         f'v-{h*0.5}a{w*0.26} {w*0.26} 0 0 1 {w*0.26} -{w*0.26}Z" fill="{skin}"/>')
    step = w / (fingers + 1)
    for i in range(fingers):
        fx = x + step * (i + 1)
        ln = h * 0.46 if i in (0, fingers - 1) else h * 0.56
        s += (f'<path d="M{fx:.1f} {y+h*0.85:.1f}v{ln:.1f}" stroke="{SKIN_D}" '
              f'stroke-width="{w*0.075:.1f}" stroke-linecap="round"/>')
    if rot:
        s = f'<g transform="rotate({rot} {x+w/2} {y+h/2})">{s}</g>'
    return s


def leaf(cx, cy, size, fill=SAGE_D, rot=0):
    return (f'<g transform="translate({cx} {cy}) rotate({rot})">'
            f'<path d="M0 0C0 -{size*0.9} {size*0.62} -{size*1.5} {size*0.95} -{size*1.5}'
            f'C{size*0.95} -{size*0.6} {size*0.42} 0 0 0Z" fill="{fill}"/></g>')


def plant(cx, base, scale=1.0, fill=SAGE_D, pot=OLIVE):
    s = ''
    for dx, rot, sz in ((-4, -26, 30), (4, 16, 34), (0, -4, 26)):
        s += leaf(cx + dx * scale, base - 6 * scale, sz * scale, fill, rot)
    s += (f'<path d="M{cx-19*scale} {base-4*scale}h{38*scale}l-{5*scale} {26*scale}'
          f'h-{28*scale}Z" fill="{pot}"/>')
    return s


def candle(x, base, h, w=17, body=CREAM):
    return (f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" rx="{w*0.32}" fill="{body}"/>'
            f'<ellipse cx="{x+w/2}" cy="{base-h-9}" rx="{w*0.27}" ry="{w*0.46}" fill="{YELLOW_D}"/>'
            f'<ellipse cx="{x+w/2}" cy="{base-h-7}" rx="{w*0.13}" ry="{w*0.25}" fill="{CREAM}"/>')


def bottle(x, base, h=64, w=32, fill=OLIVE):
    return (f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" rx="{w*0.28}" fill="{fill}"/>'
            f'<rect x="{x+w*0.31}" y="{base-h-13}" width="{w*0.38}" height="14" rx="3" fill="{WOOD}"/>'
            f'<rect x="{x+w*0.17}" y="{base-h*0.62}" width="{w*0.66}" height="{h*0.3}" rx="4" fill="{CREAM}" opacity=".75"/>')


def table(y, x0=-30, x1=430, top=WOOD, side=INK):
    return (f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="26" rx="13" fill="{top}"/>'
            f'<rect x="{x0}" y="{y+18}" width="{x1-x0}" height="30" rx="12" fill="{side}"/>')


def wrap(w, h, bg, body, label, arc=None):
    a = ''
    if arc:
        cx, cy, r, col, op = arc
        a = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" opacity="{op}"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'preserveAspectRatio="xMidYMid slice" role="img" aria-label="{label}">'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>{a}{body}</svg>\n')


S = {}

# ---------- 1. Héros : mains sur le dos ----------
b = (arm(232, -40, 34, 168) + arm(300, -40, 34, 168)
     + hand(224, 118, 58, 48) + hand(292, 118, 58, 48)
     + table(352)
     + f'<path d="M96 352c46-52 128-64 208-46 52 12 122 20 122 20v26H96Z" fill="{SKIN}"/>'
     + f'<path d="M232 292c74 8 134 26 194 34v26H232Z" fill="{CREAM}"/>'
     + f'<rect x="188" y="306" width="250" height="40" rx="19" fill="{CREAM}"/>'
     + f'<rect x="18" y="292" width="126" height="54" rx="26" fill="{CREAM}"/>'
     + head(112, 268, 46))
S['hero.svg'] = wrap(400, 448, TERRA, b, "Marie masse le dos d'une cliente",
                     arc=(320, 96, 130, TERRA_L, '.6'))

# ---------- 2. À propos : Marie de face ----------
b = (plant(52, 452, 1.15, SAGE_D, OLIVE)
     + f'<rect x="150" y="300" width="150" height="210" rx="70" fill="{CREAM}"/>'
     + head(225, 250, 74, HAIR, SKIN)
     + arm(140, 330, 40, 150) + arm(272, 330, 40, 150))
S['marie.svg'] = wrap(400, 500, YELLOW, b, "Portrait de Marie",
                      arc=(225, 232, 128, YELLOW_D, '.75'))

# ---------- 3. Détail : mains ----------
b = (hand(52, 104, 92, 74, rot=-14) + hand(232, 122, 92, 74, rot=12)
     + leaf(352, 274, 34, SAGE_D, 24) + leaf(44, 268, 28, SAGE_D, -30))
S['mains.svg'] = wrap(400, 300, SAGE, b, 'Gros plan sur des mains', arc=(210, 130, 118, CREAM, '.4'))

# ---------- 4. Cabinet : la table ----------
b = (plant(58, 250, 1.0, SAGE_D, OCHRE)
     + f'<rect x="118" y="150" width="234" height="34" rx="16" fill="{CREAM}"/>'
     + table(176, 108, 362)
     + f'<rect x="128" y="122" width="66" height="30" rx="14" fill="{CREAM}"/>'
     + f'<rect x="146" y="230" width="16" height="52" rx="7" fill="{WOOD}"/>'
     + f'<rect x="310" y="230" width="16" height="52" rx="7" fill="{WOOD}"/>')
S['table.svg'] = wrap(400, 300, YELLOW, b, 'La table de massage', arc=(300, 80, 116, YELLOW_D, '.8'))

# ---------- 5. Cabinet : bougies ----------
b = (candle(116, 234, 96) + candle(178, 234, 132) + candle(240, 234, 76)
     + f'<rect x="80" y="232" width="230" height="18" rx="9" fill="{WOOD}"/>')
S['bougies.svg'] = wrap(400, 300, TERRA, b, 'Bougies allumées', arc=(196, 130, 108, TERRA_L, '.55'))

# ---------- 6. Cabinet : huiles & serviettes ----------
b = (bottle(112, 244, 78, 36, OLIVE) + bottle(168, 244, 60, 30, WOOD)
     + f'<circle cx="256" cy="212" r="34" fill="{CREAM}"/>'
     + f'<circle cx="256" cy="212" r="13" fill="{SAGE}"/>'
     + f'<circle cx="304" cy="228" r="24" fill="{CREAM}"/>'
     + f'<circle cx="304" cy="228" r="9" fill="{SAGE}"/>'
     + f'<rect x="86" y="244" width="240" height="16" rx="8" fill="{WOOD}"/>')
S['huiles.svg'] = wrap(400, 300, SAGE, b, 'Huiles et serviettes roulées', arc=(150, 120, 96, CREAM, '.35'))

# ---------- 7. Cabinet : coin détente ----------
b = (plant(316, 262, 1.35, SAGE_D, OCHRE)
     + f'<rect x="74" y="120" width="132" height="96" rx="30" fill="{OLIVE}"/>'
     + f'<rect x="62" y="196" width="156" height="52" rx="22" fill="{CREAM}"/>'
     + f'<rect x="58" y="176" width="22" height="62" rx="11" fill="{SAGE_D}"/>'
     + f'<rect x="200" y="176" width="22" height="62" rx="11" fill="{SAGE_D}"/>'
     + f'<rect x="84" y="244" width="14" height="30" rx="7" fill="{WOOD}"/>'
     + f'<rect x="182" y="244" width="14" height="30" rx="7" fill="{WOOD}"/>')
S['detente.svg'] = wrap(400, 300, CREAM, b, 'Coin détente', arc=(120, 120, 92, YELLOW, '.85'))

# ---------- 8. Cabinet : vue d'ensemble (bandeau) ----------
b = (f'<rect x="36" y="34" width="84" height="66" rx="10" fill="{YELLOW}"/>'
     + f'<path d="M78 34v66M36 67h84" stroke="{CREAM}" stroke-width="6"/>'
     + plant(342, 128, 0.62, SAGE_D, OCHRE)
     + f'<rect x="150" y="84" width="170" height="20" rx="10" fill="{CREAM}"/>'
     + table(100, 142, 328)
     + candle(126, 128, 30, 12))
S['piece.svg'] = wrap(400, 150, SAGE, b, "Vue d'ensemble de la pièce")

# ---------- 9-14. Soins ----------
def soin(bg, arc_col, body, label):
    return wrap(400, 275, bg, body, label, arc=(300, 60, 108, arc_col, '.55'))

# Kobido — visage
b = (head(200, 168, 76, HAIR, SKIN)
     + hand(76, 128, 54, 44) + hand(268, 128, 54, 44)
     + f'<rect x="150" y="240" width="100" height="60" rx="30" fill="{CREAM}"/>')
S['kobido.svg'] = soin(TERRA, TERRA_L, b, 'Massage du visage Kobido')

# Madérothérapie — outils en bois
b = (f'<rect x="74" y="118" width="150" height="52" rx="26" fill="{WOOD}"/>'
     + ''.join(f'<rect x="{x}" y="118" width="7" height="52" fill="{CREAM}" opacity=".22"/>'
               for x in (104, 134, 164, 194))
     + f'<rect x="46" y="132" width="34" height="24" rx="12" fill="{CREAM}"/>'
     + f'<rect x="218" y="132" width="34" height="24" rx="12" fill="{CREAM}"/>'
     + f'<path d="M262 214a44 44 0 0 1 88 0Z" fill="{WOOD}"/>'
     + f'<rect x="256" y="208" width="100" height="16" rx="8" fill="{CREAM}"/>'
     + f'<rect x="70" y="212" width="150" height="14" rx="7" fill="{CREAM}" opacity=".55"/>')
S['madero.svg'] = soin(OLIVE, YELLOW_D, b, 'Outils de madérothérapie')

# Relaxation — corps allongé
b = (table(212, -20, 420)
     + f'<path d="M60 212c40-40 116-50 186-36 46 10 108 16 108 16v20H60Z" fill="{SKIN}"/>'
     + f'<rect x="150" y="176" width="212" height="34" rx="16" fill="{CREAM}"/>'
     + head(76, 158, 38)
     + hand(178, 118, 52, 44, rot=-8) + hand(240, 126, 52, 44, rot=8))
S['relaxation.svg'] = soin(TERRA_L, TERRA, b, 'Massage relaxation du corps')

# Drainage — jambes
b = (table(222, -20, 420)
     + f'<rect x="60" y="168" width="300" height="42" rx="21" fill="{SKIN}"/>'
     + f'<circle cx="66" cy="189" r="27" fill="{SKIN}"/>'
     + f'<rect x="252" y="160" width="120" height="30" rx="15" fill="{CREAM}"/>'
     + hand(112, 104, 54, 44, rot=-10) + hand(176, 112, 54, 44, rot=10)
     + leaf(348, 132, 28, SAGE_D, 22))
S['drainage.svg'] = soin(SAGE, CREAM, b, 'Drainage lymphatique des jambes')

# Bébé
b = (f'<rect x="88" y="176" width="230" height="46" rx="23" fill="{CREAM}"/>'
     + f'<circle cx="236" cy="164" r="34" fill="{SKIN}"/>'
     + f'<path d="M202 158a34 34 0 0 1 68-8c-10 10-24 14-40 11-12-2-22 0-28-3Z" fill="{HAIR}"/>'
     + f'<path d="M222 172q7 6 14 0" stroke="{SKIN_D}" stroke-width="3" fill="none" stroke-linecap="round"/>'
     + f'<rect x="132" y="164" width="86" height="34" rx="17" fill="{SKIN}"/>'
     + hand(96, 66, 46, 38, rot=-12) + hand(158, 74, 46, 38, rot=10))
S['bebe.svg'] = soin(YELLOW, YELLOW_D, b, 'Massage bébé')

# Dos & nuque
b = (f'<path d="M112 275c0-70 40-116 92-116s92 46 92 116Z" fill="{SKIN}"/>'
     + head(204, 138, 52)
     + hand(126, 168, 52, 42) + hand(230, 168, 52, 42))
S['dos.svg'] = soin(OCHRE, TERRA_L, b, 'Massage du dos et de la nuque')

# ---------- 15. Avatars ----------
AV = ((YELLOW, HAIR), (SAGE, '#4A3B2A'), (TERRA_L, '#2F2721'), (OLIVE, '#4C3A2C'), (CREAM, '#3E3228'))
for i, (bg, hr) in enumerate(AV, 1):
    b = (f'<circle cx="50" cy="96" r="30" fill="{CREAM}"/>' + head(50, 46, 20, hr, SKIN))
    S[f'avatar-{i}.svg'] = wrap(100, 100, bg, b, 'Portrait de cliente')

for name, svg in S.items():
    (OUT / name).write_text(svg, encoding='utf-8')
print(f'{len(S)} illustrations générées dans {OUT}')
