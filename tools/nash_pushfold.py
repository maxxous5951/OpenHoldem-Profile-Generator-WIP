"""Calcule le Nash push/fold heads-up (SB all-in ou fold, BB call ou fold) par profondeur, a partir de la matrice
d'equite 169x169 (tools/equity.c -> tools/data/equity169.txt). Ecrit ohpg/data/nash_hu.py.

Usage : python tools/nash_pushfold.py
Hypotheses : EV en jetons, sans ante, effacement des cartes (card removal) ignore. Les ranges sont donnees en % de combos.
"""
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
RANKS = "AKQJT98765432"
STACKS = [3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30]


def names():
    out = []
    for i, a in enumerate(RANKS):
        for j, b in enumerate(RANKS):
            if i == j:
                out.append(a + b)
            elif i < j:
                out += [a + b + "s", a + b + "o"]
    return out


def weights(ns):
    return np.array([6 if len(n) == 2 else 4 if n[2] == "s" else 12 for n in ns], dtype=float)


def solve(M, w, S, iters=4000):
    n = len(w)
    sb = np.ones(n)
    bb = np.zeros(n)
    tot = w.sum()
    for t in range(1, iters + 1):
        step = 1.0 / (t + 1)
        # meilleure reponse du BB : paie si S*(2*eq-1) > -1
        sbw = w * sb
        if sbw.sum() > 0:
            eq_bb = (M @ sbw) / sbw.sum()  # eq_bb[j] = equite du BB j contre la range SB
            br_bb = (S * (2 * eq_bb - 1) > -1.0).astype(float)
        else:
            br_bb = np.ones(n)
        bb = (1 - step) * bb + step * br_bb
        # meilleure reponse du SB : push si EV > -0.5
        bbw = w * bb
        pc = bbw.sum() / tot
        ev_called = (M @ bbw) / max(bbw.sum(), 1e-9)  # equite de chaque main SB quand BB paie
        ev_push = (1 - pc) * 1.0 + pc * S * (2 * ev_called - 1)
        br_sb = (ev_push > -0.5).astype(float)
        sb = (1 - step) * sb + step * br_sb
    return 100 * (w * sb).sum() / tot, 100 * (w * bb).sum() / tot


def main():
    M = np.loadtxt(ROOT / "data" / "equity169.txt")
    M = (M + (1 - M.T)) / 2  # lisse le bruit Monte Carlo
    ns = names()
    w = weights(ns)
    push, call = {}, {}
    for s in STACKS:
        p, c = solve(M, w, float(s))
        push[s], call[s] = round(float(p), 1), round(float(c), 1)
        print(s, push[s], call[s])
    out = Path(ROOT.parent / "ohpg" / "data" / "nash_hu.py")
    out.write_text('"""Nash push/fold heads-up (genere par tools/nash_pushfold.py) : % de combos par profondeur (BB)."""\n'
                   f"SB_PUSH = {push}\nBB_CALL = {call}\n", encoding="ascii")


if __name__ == "__main__":
    main()
