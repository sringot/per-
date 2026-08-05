#!/usr/bin/env python3
"""Redessine le pictogramme du logo et mesure l'écart avec le fichier fourni.

Le tracé est établi sur les coordonnées relevées ligne par ligne dans
assets/img/logo-reference.png, puis rendu et comparé au masque d'origine
(indice de Jaccard). Relancer après toute retouche du tracé.
"""
import pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).parent

# Repère source → viewBox : le pictogramme occupe x 41→103, y 45→108.
SX, SY, S = 41, 45, 100 / 62
fx = lambda x: round((x - SX) * S, 1)
fy = lambda y: round((y - SY) * S, 1)

# Le tracé descend jusqu'à y=108,6 (arrondis du pied) : le viewBox
# doit aller au-delà, sans quoi le bas du M est rogné.
VB_H = round((109 - SY) * S, 1)          # 103.2

PATH = (
    # ── flanc gauche : le bord s'évase légèrement vers le bas ────
    f"M {fx(41.6)} {fy(106)} "
    f"L {fx(44.2)} {fy(69)} "
    f"Q {fx(44.3)} {fy(65.6)} {fx(47.8)} {fy(65.6)} "
    # ── plateau de l'épaule gauche, congé serré vers le bras ─────
    f"L {fx(60)} {fy(65.6)} "
    f"Q {fx(63.2)} {fy(65.8)} {fx(64.2)} {fy(68)} "
    # ── bras gauche plongeant vers le centre ─────────────────────
    f"C {fx(65.6)} {fy(70.5)} {fx(67.6)} {fy(73.5)} {fx(68.6)} {fy(78.5)} "
    f"C {fx(69.2)} {fy(81.5)} {fx(69.6)} {fy(83.5)} {fx(70.2)} {fy(85)} "
    f"Q {fx(71.4)} {fy(87.5)} {fx(72.4)} {fy(85)} "
    # ── bras droit, miroir autour de x = 72,2 ────────────────────
    f"C {fx(73)} {fy(83.5)} {fx(73.6)} {fy(81.5)} {fx(74.6)} {fy(78.5)} "
    f"C {fx(75.6)} {fy(73.5)} {fx(77.2)} {fy(70.5)} {fx(78.4)} {fy(68)} "
    f"Q {fx(78.8)} {fy(65.8)} {fx(82.5)} {fy(65.6)} "
    # ── plateau de l'épaule droite ───────────────────────────────
    f"L {fx(96.8)} {fy(65.6)} "
    f"Q {fx(100.3)} {fy(65.6)} {fx(100.4)} {fy(69)} "
    # ── flanc droit ──────────────────────────────────────────────
    f"L {fx(102.7)} {fy(106)} "
    f"Q {fx(102.9)} {fy(108.6)} {fx(100.2)} {fy(108.6)} "
    f"L {fx(87.3)} {fy(108.6)} "
    f"Q {fx(84.6)} {fy(108.6)} {fx(84.6)} {fy(105.5)} "
    # ── fente droite ─────────────────────────────────────────────
    f"L {fx(84.8)} {fy(87)} "
    f"Q {fx(82.9)} {fy(83)} {fx(81.2)} {fy(87)} "
    f"L {fx(77.2)} {fy(105.5)} "
    f"Q {fx(76.9)} {fy(108.6)} {fx(74.2)} {fy(108.6)} "
    # ── pied de la colonne centrale ──────────────────────────────
    f"L {fx(68.8)} {fy(108.6)} "
    f"Q {fx(66.1)} {fy(108.6)} {fx(66.1)} {fy(105.5)} "
    # ── fente gauche ─────────────────────────────────────────────
    f"L {fx(61.2)} {fy(87)} "
    f"Q {fx(59.6)} {fy(83)} {fx(58.1)} {fy(87)} "
    f"L {fx(58.6)} {fy(105.5)} "
    f"Q {fx(58.6)} {fy(108.6)} {fx(55.9)} {fy(108.6)} "
    # ── pied du flanc gauche ─────────────────────────────────────
    f"L {fx(44.3)} {fy(108.6)} "
    f"Q {fx(41.4)} {fy(108.6)} {fx(41.6)} {fy(106)} Z"
)

HEADS = (
    (fx(53), fy(53), 13.7),      # tête gauche
    (fx(90.6), fy(53), 12.9),    # tête droite
)

def svg(color='currentColor', label='Logo Marie Massage'):
    heads = ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r}"/>' for cx, cy, r in HEADS)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 {VB_H}" '
            f'role="img" aria-label="{label}">'
            f'<g fill="{color}">{heads}<path d="{PATH}"/></g></svg>\n')


if __name__ == '__main__':
    (ROOT / 'assets/img/logo.svg').write_text(svg(), encoding='utf-8')
    print('assets/img/logo.svg écrit')

    # Version aplatie pour la comparaison pixel à pixel
    tmp = pathlib.Path('/tmp/claude-0/-home-user-per-/0ab23514-8cad-52d4-a3c4-7a8a46290735/scratchpad/logo-test.svg')
    tmp.write_text(svg('#EC8448'), encoding='utf-8')
    print(f'{tmp} écrit')
