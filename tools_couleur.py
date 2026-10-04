"""Contraste et lisibilité — partagé par les outils du projet.

Ces trois fonctions décidaient déjà des couleurs des cartes de soins ; elles
servent maintenant aussi à l'affiche imprimée. Les garder à un seul endroit
évite qu'un des deux outils dérive et produise une teinte qui « passe » d'un
côté et pas de l'autre.

Pur Python, sans dépendance : le calcul de contraste du WCAG tient en dix
lignes, et l'importer depuis un script qui charge numpy pour autre chose ne
justifierait pas la dépendance.
"""

Couleur = tuple


def hexa(c):
    """(r, g, b) → '#RRGGBB'."""
    return '#%02X%02X%02X' % tuple(int(round(x)) for x in c)


def rgb(s):
    """'#RRGGBB' → (r, g, b)."""
    s = s.lstrip('#')
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def luminance(c):
    """Luminance relative, au sens du WCAG."""
    v = []
    for x in c:
        x /= 255
        v.append(x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4)
    return .2126 * v[0] + .7152 * v[1] + .0722 * v[2]


def contraste(a, b):
    """Rapport de contraste entre deux couleurs, de 1:1 à 21:1."""
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + .05) / (min(la, lb) + .05)


def melange(a, b, part):
    """`color-mix(in srgb, a part%, b)` — le même calcul, côté Python.

    Sert à connaître le fond réel d'un bloc avant d'y poser du texte : les
    aplats de l'affiche sont des mélanges, et vérifier le contraste sur la
    couleur pure du soin donnerait une réponse fausse.
    """
    return tuple(x * part + y * (1 - part) for x, y in zip(a, b))


def encre_lisible(teinte, fond, vise=4.5):
    """Pousse `teinte` vers le noir ou le blanc jusqu'à atteindre `vise`.

    On garde la teinte — c'est elle qui identifie le soin — et l'on ne joue
    que sur sa clarté. Les deux directions sont essayées parce qu'aucune ne
    marche partout : sur un orange vif, éclaircir plafonne sous le seuil même
    en blanc pur, alors qu'assombrir passe. On retient celle qui atteint la
    cible en s'écartant le moins de la couleur d'origine.
    """
    if contraste(teinte, fond) >= vise:
        return tuple(teinte)

    candidats = []
    for vers in ((0, 0, 0), (255, 255, 255)):
        for k in range(1, 101):
            essai = tuple(t + (v - t) * k / 100 for t, v in zip(teinte, vers))
            if contraste(essai, fond) >= vise:
                candidats.append((k, essai))
                break
    if not candidats:
        raise ValueError(f'aucune encre à {vise}:1 sur {hexa(fond)}')
    return min(candidats)[1]
