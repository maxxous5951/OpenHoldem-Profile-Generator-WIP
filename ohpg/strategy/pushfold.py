"""Push/fold et reshove tournoi. Les pourcentages sont des approximations de ranges Nash (sans ICM),
à ajuster avec pf_scale / pf_call_scale / icm_pressure ; ils sont convertis en handlists triées par équité."""
from __future__ import annotations

from .. import ranges as R
from ..ppl import Profile, fmt
from .common import ORDER, actives, HERO, OPENER, OPEN_WIDTH, join, mix, tiers

BUCKETS = [3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30]
BTN_PUSH = {3: 80, 4: 68, 5: 58, 6: 50, 7: 44, 8: 40, 10: 34, 12: 28, 15: 22, 20: 15, 25: 11, 30: 8}
SB_PUSH = {3: 100, 4: 100, 5: 95, 6: 85, 7: 75, 8: 68, 10: 58, 12: 50, 15: 42, 20: 30, 25: 22, 30: 16}
POS_PUSH_MULT = {"EP": 0.38, "MP": 0.55, "CO": 0.75, "BTN": 1.0}
BB_CALL = {3: 70, 4: 58, 5: 50, 6: 43, 7: 38, 8: 34, 10: 28, 12: 23, 15: 18, 20: 13, 25: 9, 30: 7}
OPENER_CALL_MULT = {"EP": 0.45, "MP": 0.6, "CO": 0.8, "BTN": 1.0, "SB": 1.3}
HERO_CALL_MULT = {"BB": 1.0, "SB": 0.8, "BTN": 0.5, "CO": 0.45, "MP": 0.4, "EP": 0.35}


def _bands(pf_max: int):
    bounds = [b for b in BUCKETS if b < pf_max]
    bounds.append(pf_max)
    out, prev = [], 0
    for b in bounds:
        ref = min((x for x in BUCKETS if x >= b), default=BUCKETS[-1])
        out.append((prev, b, ref))
        prev = b
    return out


def _cond(lo, hi, var="f$Gen_EffStack"):
    return join(f"{var} >= {lo}", f"{var} <= {hi}")


def push_pct(cfg, pos, ref):
    base = SB_PUSH[ref] if pos == "SB" else BTN_PUSH[ref] * POS_PUSH_MULT.get(pos, 1.0)
    return min(100.0, base * cfg["pf_scale"] / 100.0 * (1.0 + cfg["ante_bb"] * 2.0))


def call_pct(cfg, hero, opener, ref, bubble=False):
    pct = BB_CALL[ref] * OPENER_CALL_MULT[opener] * HERO_CALL_MULT[hero] * cfg["pf_call_scale"] / 100.0
    pct *= 1.0 + cfg["ante_bb"] * 1.2
    if bubble:
        pct *= 1.0 - cfg["icm_pressure"] / 100.0 * 0.45
    return min(70.0, pct)


def emit(prof: Profile, f, cfg: dict):
    pf = cfg["pf_max_stack"]
    first = "BotsActionsOnThisRoundIncludingChecks = 0"
    bands = _bands(pf)

    f.comment("=== PUSH/FOLD : première action, stack effectif <= %d BB ===" % pf)
    f.group(join(first, "Raises = 0", "Calls = 0", f"f$Gen_EffStackFirstIn <= {pf}"))
    for lo, hi, ref in bands:
        for pos in actives():
            hands = R.top_equity(round(push_pct(cfg, pos, ref), 1))
            full, part = tiers(hands, 0.9)
            lf = prof.add_list(f"Push{pos}{hi}", full)
            if lf != "false":
                f.act(join(_cond(lo, hi, "f$Gen_EffStackFirstIn"), HERO[pos], lf), "RaiseMax")
            lp = prof.add_list(f"Push{pos}{hi}Edge", part)
            m = mix(cfg, 0.5)
            if lp != "false" and m is not None:
                f.act(join(_cond(lo, hi, "f$Gen_EffStackFirstIn"), HERO[pos], lp, m), "RaiseMax")
    f.others("Fold")

    f.comment("=== PUSH/FOLD : face à des limpers ===")
    f.group(join(first, "Raises = 0", "Calls >= 1", f"f$Gen_EffStackFirstIn <= {pf}"))
    for lo, hi, ref in bands:
        for pos in ORDER:
            base_pos = "CO" if pos == "BB" else pos
            hands = R.top_equity(round(push_pct(cfg, base_pos, ref) * 0.8, 1))
            lh = prof.add_list(f"PushLimp{pos}{hi}", hands)
            if lh != "false":
                f.act(join(_cond(lo, hi, "f$Gen_EffStackFirstIn"), HERO[pos], lh), "RaiseMax")
    f.act("InBigBlind", "Check")
    f.others("Fold")

    f.comment("=== PUSH/FOLD : face à une relance (call d'un jam, reshove sinon) ===")
    f.group(join(first, "Raises = 1", f"f$Gen_EffStack <= {pf}"))
    jam_like = "AmountToCall >= StackSize * 0.6"
    for lo, hi, ref in bands:
        band = _cond(lo, hi)
        for hero in reversed(ORDER):
            from .common import openers_before
            for opener in (openers_before(hero)):
                cond = join(band, HERO[hero], OPENER[opener])
                if cfg["icm_pressure"] > 0:
                    lb = prof.add_list(f"CallJamB{hero}{opener}{hi}", R.top_equity(round(call_pct(cfg, hero, opener, ref, True), 1)))
                    if lb != "false":
                        f.act(join(cond, jam_like, "IsBubble", lb), "Call")
                lc = prof.add_list(f"CallJam{hero}{opener}{hi}", R.top_equity(round(call_pct(cfg, hero, opener, ref), 1)))
                if lc != "false":
                    f.act(join(cond, jam_like, lc), "Call")
                if cfg["reshove_stack"] >= hi or lo < cfg["reshove_stack"]:
                    pct = max(2.0, min(30.0, 0.55 * (27 - ref) + 2.0)) * OPEN_WIDTH[opener] * (1.2 if hero in ("SB", "BB") else 0.8)
                    pct *= cfg["pf_scale"] / 100.0
                    lr = prof.add_list(f"Reshove{hero}{opener}{hi}", R.top_equity(round(pct, 1)))
                    if lr != "false":
                        f.act(join(cond, lr), "RaiseMax")
    f.others("Fold")
