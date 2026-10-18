"""Calcule le classement des 169 mains de départ par équité contre une main aléatoire
(Monte Carlo, eval7) et écrit ohpg/data/hand_ranking.py.

Usage : python tools/compute_hand_ranking.py [itérations_par_main]
"""
import random
import sys
from pathlib import Path

import eval7

RANKS = "AKQJT98765432"
SUITS = "shdc"


def classes():
    out = []
    for i, a in enumerate(RANKS):
        for j, b in enumerate(RANKS):
            if i == j:
                out.append((a + b, a, a, False))
            elif i < j:
                out.append((a + b + "s", a, b, True))
                out.append((a + b + "o", a, b, False))
    return out


def equity(r1, r2, suited, iters, rng):
    if suited:
        c1, c2 = eval7.Card(r1 + "s"), eval7.Card(r2 + "s")
    else:
        c1, c2 = eval7.Card(r1 + "s"), eval7.Card(r2 + "h")
    dead = {str(c1), str(c2)}
    pool = [eval7.Card(r + s) for r in RANKS for s in SUITS if r + s not in dead]
    win = tie = 0
    for _ in range(iters):
        draw = rng.sample(pool, 7)
        board = draw[2:]
        h = eval7.evaluate([c1, c2] + board)
        v = eval7.evaluate(draw[:2] + board)
        if h > v:
            win += 1
        elif h == v:
            tie += 1
    return (win + tie / 2) / iters


def combos(n):
    return 6 if len(n) == 2 else (4 if n.endswith("s") else 12)


def main():
    iters = int(sys.argv[1]) if len(sys.argv) > 1 else 60000
    rng = random.Random(20261018)
    res = []
    for name, r1, r2, s in classes():
        res.append((equity(r1, r2, s, iters, rng), name))
    res.sort(reverse=True)
    lines = ['"""Classement des 169 mains (équité vs main aléatoire). Généré par tools/compute_hand_ranking.py."""',
             "", "# (nom, équité, combos), de la meilleure à la pire main", "HAND_RANKING = ["]
    for eq, n in res:
        lines.append(f'    ("{n}", {eq:.4f}, {combos(n)}),')
    lines.append("]")
    out = Path(__file__).resolve().parent.parent / "ohpg" / "data" / "hand_ranking.py"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("écrit", out, "top10:", [n for _, n in res[:10]], "bottom5:", [n for _, n in res[-5:]])


if __name__ == "__main__":
    main()
