"""Nash push/fold a 3 joueurs (BTN / SB / BB), chip EV (Spin & Go gagnant-prend-tout), par profondeur.

Meme matrice d'equite 169x169 que nash_pushfold.py. Les equites a 3 joueurs sont approchees par produit normalise des
equites deux a deux (pas d'enumeration exacte) ; effacement des cartes ignore ; stacks egaux. Ecrit ohpg/data/nash_3max.py.

Strategies : BTN push ; SB call-jam vs BTN ; SB push si BTN fold ; BB call vs BTN seul / vs BTN + SB / vs SB seul.
Usage : python tools/nash_3max.py
"""
from pathlib import Path

import numpy as np

from nash_pushfold import names, weights

ROOT = Path(__file__).resolve().parent
STACKS = [3, 4, 5, 6, 7, 8, 10, 12, 15]


def tensor(M):
    pa = M[:, :, None]  # eq(h, a)
    pb = M[:, None, :]  # eq(h, b)
    pab = M[None, :, :]  # eq(a, b)
    wh = pa * pb
    wa = (1 - pa) * pab
    wb = (1 - pb) * (1 - pab)
    return (wh / (wh + wa + wb + 1e-12)).astype(np.float32)


def solve(M, T, w, S, iters=500):
    n = len(w)
    tot = w.sum()
    T2 = T.reshape(n, n * n)
    b = np.full(n, 0.5)       # BTN push
    sc = np.full(n, 0.3)      # SB call vs BTN push
    sp = np.full(n, 0.5)      # SB push (BTN fold)
    k1 = np.full(n, 0.3)      # BB call vs BTN (SB fold)
    k2 = np.full(n, 0.2)      # BB call vs BTN + SB call
    k3 = np.full(n, 0.3)      # BB call vs SB push

    def dist(freq):
        x = w * freq
        s = x.sum()
        return x / s if s > 0 else np.full(n, 1.0 / n), s / tot

    def eq3(da, db):
        return T2 @ np.outer(da, db).ravel()

    for t in range(1, iters + 1):
        step = 1.0 / (t + 1)
        dB, _ = dist(b)
        dSc, pSc = dist(sc)
        dSp, _ = dist(sp)
        dK1, pk1 = dist(k1)
        dK2, pk2 = dist(k2)
        dK3, pk3 = dist(k3)
        # --- BB
        e1 = M @ dB
        br_k1 = (e1 * (2 * S + 0.5) - S > -1.0)
        e2 = eq3(dB, dSc)
        br_k2 = (3 * S * e2 - S > -1.0)
        e3 = M @ dSp
        br_k3 = (S * (2 * e3 - 1) > -1.0)
        # --- SB : call vs BTN push (BB repond ensuite avec k2)
        hu = (M @ dB) * (2 * S + 1) - S
        tw = 3 * S * eq3(dB, dK2) - S
        ev_call = (1 - pk2) * hu + pk2 * tw
        br_sc = ev_call > -0.5
        # --- SB : push quand BTN fold (BB repond avec k3)
        ev_sp = (1 - pk3) * 1.0 + pk3 * S * (2 * (M @ dK3) - 1)
        br_sp = ev_sp > -0.5
        # --- BTN push
        hu_bb = (M @ dK1) * (2 * S + 0.5) - S
        hu_sb = (M @ dSc) * (2 * S + 1) - S
        tw3 = 3 * S * eq3(dSc, dK2) - S
        ev_b = ((1 - pSc) * ((1 - pk1) * 1.5 + pk1 * hu_bb)
                + pSc * ((1 - pk2) * hu_sb + pk2 * tw3))
        br_b = ev_b > 0
        for arr, br in ((b, br_b), (sc, br_sc), (sp, br_sp), (k1, br_k1), (k2, br_k2), (k3, br_k3)):
            arr *= (1 - step)
            arr += step * br
    pct = lambda x: round(float(100 * (w * x).sum() / tot), 1)
    return dict(BTN_PUSH=pct(b), SB_CALL=pct(sc), SB_PUSH=pct(sp), BB_CALL_BTN=pct(k1), BB_CALL_BTN_SB=pct(k2),
                BB_CALL_SB=pct(k3))


def main():
    M = np.loadtxt(ROOT / "data" / "equity169.txt")
    M = (M + (1 - M.T)) / 2
    w = weights(names())
    T = tensor(M)
    res = {}
    for s in STACKS:
        res[s] = solve(M, T, w, float(s))
        print(s, res[s], flush=True)
    keys = ["BTN_PUSH", "SB_CALL", "SB_PUSH", "BB_CALL_BTN", "BB_CALL_BTN_SB", "BB_CALL_SB"]
    out = '"""Nash push/fold 3 joueurs chip EV (genere par tools/nash_3max.py) : % de combos par profondeur (BB)."""\n'
    for k in keys:
        out += f"{k} = {{{', '.join(f'{s}: {res[s][k]}' for s in STACKS)}}}\n"
    (ROOT.parent / "ohpg" / "data" / "nash_3max.py").write_text(out, encoding="ascii")


if __name__ == "__main__":
    main()
