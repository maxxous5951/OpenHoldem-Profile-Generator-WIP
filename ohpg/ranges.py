"""Gestion des ranges : classement des 169 mains, construction de ranges en % de combos,
ranges value / bluff / call disjointes, export en handlists OpenPPL."""
from __future__ import annotations

import re
from functools import lru_cache

from .data.hand_ranking import HAND_RANKING

RANKS = "AKQJT98765432"
TOTAL_COMBOS = 1326
COMBOS = {n: c for n, _, c in HAND_RANKING}
EQUITY = {n: e for n, e, _ in HAND_RANKING}
EQUITY_ORDER = [n for n, _, _ in HAND_RANKING]


def _play_score(name: str) -> float:
    """Équité corrigée par la jouabilité postflop (suited, connecté, paires basses, domination)."""
    eq = EQUITY[name]
    if len(name) == 2:  # paire
        return eq + (0.075 if RANKS.index(name[0]) >= 6 else 0.0)
    hi, lo = RANKS.index(name[0]), RANKS.index(name[1])
    gap = lo - hi - 1
    suited = name.endswith("s")
    s = eq
    if suited:
        s += 0.034
        s += {0: 0.046, 1: 0.032, 2: 0.018, 3: 0.007}.get(gap, 0.0)
        if name[0] == "A" and lo >= 9:  # A5s-A2s : blockers + nut flush draw + roue
            s += 0.022
    else:
        s -= 0.012
        s += {0: 0.012, 1: 0.006}.get(gap, 0.0)
        if name[0] == "A" and lo >= 5:  # Ax faible hors couleur : très dominé
            s -= 0.030
        elif name[0] == "K" and lo >= 7:
            s -= 0.020
        elif name[0] in "QJ" and lo >= 7:
            s -= 0.012
    return s


# Ordre de jeu curaté (ouverture 6-max/9-max : du plus tight au plus large), complété par le score de jouabilité.
_CURATED = (
    "AA KK QQ JJ AKs TT AQs AKo 99 AJs KQs 88 ATs AQo KJs 77 KTs QJs A9s AJo JTs 66 A5s QTs KQo A8s A4s "
    "A7s A3s 55 K9s A2s A6s J9s T9s ATo Q9s 44 KJo 98s 87s K8s A9o 33 J8s T8s KTo K7s QJo 76s K6s Q8s 22 "
    "K5s 65s 97s 54s QTo Q7s K4s A8o K3s T7s K2s 86s JTo J7s Q6s 75s A7o Q5s 64s K9o J6s Q4s T6s A5o 96s "
    "Q3s 53s A6o Q9o J5s Q2s 85s A4o K8o J4s 43s A3o T9o J9o 95s A2o"
).split()
assert len(set(_CURATED)) == len(_CURATED) and all(h in EQUITY for h in _CURATED), "ordre curaté invalide"
_rest = sorted((h for h in EQUITY_ORDER if h not in set(_CURATED)), key=_play_score, reverse=True)
PLAY_ORDER = _CURATED + _rest

# Pool de bluffs de 3bet/4bet : blockers d'As, puis mains suited à bon potentiel.
BLUFF_POOL = [
    "A5s", "A4s", "A3s", "A2s", "A6s", "A7s", "K9s", "K8s", "K7s", "K6s", "Q9s", "J9s", "T9s", "98s",
    "87s", "76s", "65s", "54s", "J8s", "T8s", "97s", "86s", "75s", "KJo", "QJo", "A9s", "A8s", "K5s",
    "Q8s", "64s", "53s",
]
BLUFF_POOL_4BET = ["A5s", "A4s", "A3s", "A2s", "KQo", "K9s", "A9s", "A8s", "76s", "65s"]


def combos_of(hands) -> int:
    return sum(COMBOS[h] for h in hands)


def pct_of(hands) -> float:
    return 100.0 * combos_of(hands) / TOTAL_COMBOS


def _take(order, pct: float, exclude=frozenset()) -> list[str]:
    """Prend des mains dans `order` jusqu'à atteindre pct % des combos."""
    pct = max(0.0, min(100.0, float(pct)))
    target = TOTAL_COMBOS * pct / 100.0
    out, acc = [], 0
    for h in order:
        if h in exclude:
            continue
        c = COMBOS[h]
        if acc + c / 2.0 > target + 1e-9:
            continue
        out.append(h)
        acc += c
        if acc >= target:
            break
    return out


@lru_cache(maxsize=None)
def top_equity(pct: float) -> tuple[str, ...]:
    return tuple(_take(EQUITY_ORDER, pct))


@lru_cache(maxsize=None)
def top_play(pct: float) -> tuple[str, ...]:
    return tuple(_take(PLAY_ORDER, pct))


def split_range(value_pct: float, bluff_pct: float, call_pct: float, *, pool=None, within=None):
    """Retourne (value, bluff, call) disjoints.

    value : meilleures mains (équité) ; bluff : pool de bluffs hors value ;
    call  : meilleures mains restantes selon la jouabilité.
    `within` limite toutes les catégories à un ensemble de mains (ex. range d'ouverture)."""
    pool = BLUFF_POOL if pool is None else pool
    allowed = set(within) if within is not None else None
    eq_order = [h for h in EQUITY_ORDER if allowed is None or h in allowed]
    play_order = [h for h in PLAY_ORDER if allowed is None or h in allowed]
    value = _take(eq_order, value_pct)
    used = set(value)
    bluff = _take([h for h in pool if allowed is None or h in allowed], bluff_pct, exclude=used)
    used |= set(bluff)
    call = _take(play_order, call_pct, exclude=used)
    return value, bluff, call


def open_range(pct: float) -> list[str]:
    return list(top_play(round(float(pct), 2)))


# ----------------------------------------------------------------------------- notation

def expand_notation(text: str) -> list[str]:
    """Parse 'AA-TT, AKs-ATs, KQo, 76s+' en liste de mains."""
    hands: list[str] = []
    for tok in re.split(r"[\s,;]+", text.strip()):
        if not tok:
            continue
        hands.extend(_expand_token(tok))
    seen, out = set(), []
    for h in hands:
        if h not in seen:
            seen.add(h)
            out.append(h)
    return out


def _expand_token(tok: str) -> list[str]:
    m = re.fullmatch(r"([AKQJT2-9])([AKQJT2-9])([so]?)(\+|-([AKQJT2-9])([AKQJT2-9])([so]?))?", tok)
    if not m:
        raise ValueError(f"notation de main invalide : {tok!r}")
    a, b, suf, ext, ea, eb, _ = m.groups()
    ia, ib = RANKS.index(a), RANKS.index(b)
    if ia == ib:  # paire
        if not ext:
            return [a + a]
        if ext == "+":
            return [RANKS[i] * 2 for i in range(ia, -1, -1)]
        ie = RANKS.index(ea)
        lo, hi = sorted((ia, ie))
        return [RANKS[i] * 2 for i in range(lo, hi + 1)]
    if ia > ib:
        a, b, ia, ib = b, a, ib, ia
    if not suf:
        return _expand_token(f"{a}{b}s{ext or ''}") + _expand_token(f"{a}{b}o{ext or ''}")
    if not ext:
        return [a + b + suf]
    if ext == "+":
        return [a + RANKS[i] + suf for i in range(ib, ia, -1)]
    ie = RANKS.index(eb)
    lo, hi = sorted((ib, ie))
    return [a + RANKS[i] + suf for i in range(lo, hi + 1)]


def to_notation(hands) -> str:
    return " ".join(sorted(hands, key=lambda h: EQUITY_ORDER.index(h)))
