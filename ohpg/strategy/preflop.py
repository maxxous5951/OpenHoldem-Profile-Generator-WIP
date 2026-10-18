"""Stratégie préflop : ouverture, isolation, défense vs ouverture, squeeze, vs 3bet/4bet/5bet,
avec ranges polarisées (value + bluffs), tailles en BB et stratégie mixte."""
from __future__ import annotations

from .. import ranges as R
from ..ppl import Profile, fmt
from .common import (HERO, OPENER, ORDER, OPEN_WIDTH, emit_common_helpers, is_ip_vs_opener, join, mix,
                     openers_before, stack_buckets, tiers)

FIRST = "BotsActionsOnThisRoundIncludingChecks = 0"


def open_pct(cfg: dict, pos: str) -> float:
    base = cfg["open_" + {"EP": "ep", "MP": "mp", "CO": "co", "BTN": "btn", "SB": "sb"}[pos]]
    pct = base * cfg["range_scale"] / 100.0
    pct *= 1.0 + cfg["ante_bb"] * 1.2
    return min(100.0, pct)


def open_set(cfg: dict, pos: str) -> list[str]:
    return R.open_range(round(open_pct(cfg, pos), 1))


def _lname(prefix: str, *parts) -> str:
    return "list" + prefix + "".join(str(p).capitalize() if isinstance(p, str) else str(p) for p in parts)


def _rules(prof, f, cfg, cond, value, bluff, call, *, v_action, b_action=None, c_action="Call", tag="X", bluff_freq=1.0):
    """Écrit les règles value > bluff > call pour une condition, avec bas de range à fréquence mixte."""
    b_action = b_action or v_action
    lv = prof.add_list(_lname(tag, "V"), value)
    if lv != "false":
        f.act(join(cond, lv), v_action)
    bf, bp = tiers(bluff, 0.6)
    lb = prof.add_list(_lname(tag, "B"), bf)
    if lb != "false":
        m = mix(cfg, bluff_freq)
        if m is not None:
            f.act(join(cond, lb, m), b_action)
    lbp = prof.add_list(_lname(tag, "Bp"), bp)
    if lbp != "false":
        m = mix(cfg, 0.5 * bluff_freq)
        if m is not None:
            f.act(join(cond, lbp, m), b_action)
    cf, cp = tiers(call, 0.75)
    lc = prof.add_list(_lname(tag, "C"), cf)
    if lc != "false":
        f.act(join(cond, lc), c_action)
    lcp = prof.add_list(_lname(tag, "Cp"), cp)
    if lcp != "false":
        m = mix(cfg, 0.5)
        if m is not None:
            f.act(join(cond, lcp, m), c_action)


def generate(prof: Profile, cfg: dict):
    emit_common_helpers(prof, cfg)
    f = prof.func("f$preflop")
    f.comment("OHPG : fonction préflop. Chaque bloc WHEN sans action est un scénario ; il se termine par un fold/check.")
    agg = cfg["aggression_scale"] / 100.0

    if cfg["pf_max_stack"] > 0:
        from . import pushfold
        pushfold.emit(prof, f, cfg)

    _open(prof, f, cfg)
    _limpers(prof, f, cfg)
    _vs_open(prof, f, cfg, agg)
    _squeeze(prof, f, cfg, agg)
    _facing_3bet(prof, f, cfg, agg)
    _cold_facing_3bet(prof, f, cfg)
    _facing_4bet(prof, f, cfg, agg)
    _cold_facing_4bet(prof, f, cfg)
    _facing_5bet(prof, f, cfg)
    f.group("Others")
    f.act("AmountToCall > 0", "Fold")
    f.others("Check")


# ---------------------------------------------------------------------------------- ouverture
def _open(prof, f, cfg):
    f.comment("=== OUVERTURE (personne n'est entré dans le pot) ===")
    f.group(join(FIRST, "Raises = 0", "Calls = 0"))
    for pos in ("EP", "MP", "CO", "BTN", "SB"):
        hands = open_set(cfg, pos)
        size = cfg["open_size_ep"] if pos in ("EP", "MP") else cfg["open_size_late"] if pos in ("CO", "BTN") else cfg["open_size_sb"]
        if cfg["table_size"] == 2 and pos == "SB":
            size = min(size, 2.5)
        limp_share = cfg["sb_limp_pct"] / 100.0 if pos == "SB" else 0.0
        if limp_share > 0:
            k = int(len(hands) * (1 - limp_share))
            raise_h, limp_h = hands[:k], hands[k:]
        else:
            raise_h, limp_h = hands, []
        full, part = tiers(raise_h, 0.85)
        lf = prof.add_list(f"Open{pos}", full)
        if lf != "false":
            f.act(join(HERO[pos], lf), f"RaiseTo {fmt(size)}")
        lp = prof.add_list(f"Open{pos}Edge", part)
        m = mix(cfg, 0.5)
        if lp != "false" and m is not None:
            f.act(join(HERO[pos], lp, m), f"RaiseTo {fmt(size)}")
        ll = prof.add_list(f"Limp{pos}", limp_h)
        if ll != "false":
            f.act(join(HERO[pos], ll), "Call")
    f.others("Fold")


def _limpers(prof, f, cfg):
    f.comment("=== LIMPERS DEVANT : isolation / overlimp ===")
    f.group(join(FIRST, "Raises = 0", "Calls >= 1"))
    base = cfg["iso_raise_pct"] * cfg["aggression_scale"] / 100.0
    for n, scale in ((1, 1.0), (2, 0.8), (3, 0.6)):
        cond_n = f"Calls = {n}" if n < 3 else "Calls >= 3"
        for pos, pf in (("EP", 0.7), ("MP", 0.8), ("CO", 1.0), ("BTN", 1.3), ("SB", 0.9), ("BB", 1.0)):
            pct = min(60.0, base * scale * pf)
            iso = R.open_range(round(pct, 1))
            full, part = tiers(iso, 0.8)
            size = f"RaiseTo ({fmt(cfg['iso_size'])} + Calls)"
            li = prof.add_list(f"Iso{n}{pos}", full)
            if li != "false":
                f.act(join(cond_n, HERO[pos], li), size)
            lp = prof.add_list(f"Iso{n}{pos}Edge", part)
            m = mix(cfg, 0.5)
            if lp != "false" and m is not None:
                f.act(join(cond_n, HERO[pos], lp, m), size)
    if cfg["overlimp_pct"] > 0:
        over = [h for h in R.open_range(cfg["overlimp_pct"] + base)]
        lo = prof.add_list("Overlimp", over)
        if lo != "false":
            f.act(join(lo, "Calls <= 3", "InBigBlind"), "Check")
            f.act(join(lo, "Calls <= 3"), "Call")
    f.act("InBigBlind", "Check")
    f.others("Fold")


# ---------------------------------------------------------------------------------- vs ouverture
def _vs_open(prof, f, cfg, agg):
    f.comment("=== FACE À UNE OUVERTURE (aucun caller) : 3bet value + bluffs, call, fold ===")
    f.group(join(FIRST, "Raises = 1", "CallsSinceLastRaise = 0"))
    hero_val = {"EP": 0.8, "MP": 0.9, "CO": 1.0, "BTN": 1.1, "SB": 1.2, "BB": 1.0}
    hero_bluff = {"EP": 0.7, "MP": 0.8, "CO": 1.0, "BTN": 1.2, "SB": 1.3, "BB": 1.1}
    for hero in ORDER:
        for opener in (openers_before(hero) if hero != "BB" else ["EP", "MP", "CO", "BTN", "SB"]):
            w = OPEN_WIDTH[opener]
            value_pct = cfg["threebet_value"] * w * hero_val[hero]
            ratio = cfg["threebet_bluff_ratio"] * agg * hero_bluff[hero]
            bluff_pct = value_pct * ratio
            if hero == "BB":
                defend = min(92.0, cfg["bb_defend_pct"] * w / 1.25)
                t = min(defend * 0.9, cfg["bb_threebet_scale"] * defend / 100.0)
                t = max(t, value_pct * (1 + ratio))
                value_pct = t / (1.0 + ratio) if ratio >= 0 else t
                bluff_pct = t - value_pct
                call_pct = max(0.0, defend - t)
            elif hero == "SB":
                call_pct = cfg["call_sb_pct"] * w
            elif hero in ("EP", "MP"):
                call_pct = cfg["call_ip_pct"] * 0.5 * w
            else:
                call_pct = cfg["call_ip_pct"] * (1.0 if hero == "BTN" else 0.8) * w
            value, bluff, call = R.split_range(value_pct, bluff_pct, call_pct)
            ip = is_ip_vs_opener(hero, opener)
            mult = cfg["threebet_size_ip"] if ip else cfg["threebet_size_oop"]
            cond = join(HERO[hero], OPENER[opener])
            tag = f"V{hero}{opener}"
            act = f"RaiseTo (BetSize * {fmt(mult)})"
            shove = cfg["threebet_shove_stack"]
            if shove > 0:
                sh = prof.add_list(_lnm(tag, "SV"), value + bluff[: max(1, len(bluff) // 2)] if bluff else value)
                if sh != "false":
                    f.act(join(cond, f"f$Gen_EffStack <= {shove}", sh), "RaiseMax")
            _rules(prof, f, cfg, cond, value, bluff, call, v_action=act, tag=tag)
    f.others("Fold")


def _lnm(tag, suffix):
    return "list" + tag + suffix


# ---------------------------------------------------------------------------------- squeeze
def _squeeze(prof, f, cfg, agg):
    f.comment("=== SQUEEZE : une ouverture et un ou plusieurs callers ===")
    f.group(join(FIRST, "Raises = 1", "CallsSinceLastRaise >= 1"))
    for callers, cond_c, scale in ((1, "CallsSinceLastRaise = 1", 1.0), (2, "CallsSinceLastRaise >= 2", 0.75)):
        for hero in ORDER:
            val = cfg["squeeze_value"] * scale * (0.85 if hero in ("EP", "MP") else 1.0)
            bl = val * cfg["squeeze_bluff_ratio"] * agg * (0.5 if hero in ("EP", "MP") else 1.0)
            call = cfg["coldcall_squeeze_pct"] * scale * (1.7 if hero == "BB" else 1.2 if hero == "SB" else 0.8 if hero in ("EP", "MP") else 1.0)
            value, bluff, callh = R.split_range(val, bl, call)
            size = f"RaiseTo (BetSize * {fmt(cfg['squeeze_size'])} + BetSize * (CallsSinceLastRaise - 1))"
            cond = join(cond_c, HERO[hero])
            tag = f"Sq{callers}{hero}"
            if cfg["threebet_shove_stack"] > 0:
                sh = prof.add_list(_lnm(tag, "SV"), value)
                if sh != "false":
                    f.act(join(cond, f"f$Gen_EffStack <= {cfg['threebet_shove_stack']}", sh), "RaiseMax")
            _rules(prof, f, cfg, cond, value, bluff, callh, v_action=size, tag=tag)
    f.others("Fold")


# ---------------------------------------------------------------------------------- vs 3bet
def _cont_sets(cfg, hero, agg, tighten=1.0):
    own = open_set(cfg, hero)
    own_pct = R.pct_of(own)
    ip = hero in ("CO", "BTN")
    share = (cfg["call_3bet_ip"] if ip else cfg["call_3bet_oop"]) / 100.0 * tighten
    value_pct = min(cfg["fourbet_value"] * tighten, own_pct * 0.5)
    bluff_pct = value_pct * cfg["fourbet_bluff_ratio"] * agg
    call_pct = own_pct * share
    value, bluff, call = R.split_range(value_pct, bluff_pct, call_pct, pool=R.BLUFF_POOL_4BET, within=own)
    return value, bluff, call, ip


def _facing_3bet(prof, f, cfg, agg):
    f.comment("=== NOUS AVONS OUVERT ET FACE À UN 3BET : 4bet value/bluff, call, fold ===")
    base = "BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 1 AND NumberOfRaisesBeforeFlop = 1 AND RaisesSinceLastPlay = 1"
    for suffix, extra, tighten in (("", "Calls = 0", 1.0), ("Sq", "Calls >= 1", 0.7)):
        f.group(join(base, extra))
        for hero in ("EP", "MP", "CO", "BTN", "SB"):
            value, bluff, call, ip = _cont_sets(cfg, hero, agg, tighten)
            mult = cfg["fourbet_size_ip"] if ip else cfg["fourbet_size_oop"]
            act = f"RaiseTo (BetSize * {fmt(mult)})"
            cond = HERO[hero]
            tag = f"F3{suffix}{hero}"
            if cfg["fourbet_shove_stack"] > 0:
                sh = prof.add_list(_lnm(tag, "SV"), value + bluff)
                if sh != "false":
                    f.act(join(cond, f"f$Gen_EffStack <= {cfg['fourbet_shove_stack']}", sh), "RaiseMax")
            _rules(prof, f, cfg, cond, value, bluff, call, v_action=act, tag=tag)
        f.others("Fold")


def _cold_facing_3bet(prof, f, cfg):
    f.comment("=== OUVERTURE + 3BET DEVANT NOUS (cold) : 4bet très serré ou call ===")
    f.group(join(FIRST, "Raises = 2"))
    value = R.top_equity(round(cfg["fivebet_value"] * 0.9, 2))
    call_h = [h for h in R.top_equity(round(cfg["call_4bet_pct"] + cfg["fivebet_value"], 2)) if h not in value]
    lv = prof.add_list("ColdF3V", value)
    if lv != "false":
        f.act(lv, f"RaiseTo (BetSize * {fmt(cfg['fourbet_size_oop'])})")
    lc = prof.add_list("ColdF3C", call_h)
    if lc != "false":
        f.act(lc, "Call")
    f.others("Fold")


# ---------------------------------------------------------------------------------- vs 4bet / 5bet
def _stack_lists(prof, cfg, tag, value_pct, bluff_pct, call_pct, agg):
    out = []
    for lo, hi, factor in stack_buckets():
        v, b, c = R.split_range(value_pct * factor ** 0.5, bluff_pct * factor ** 0.5, call_pct * factor, pool=R.BLUFF_POOL_4BET)
        out.append((lo, hi, v, b, c))
    return out


def _facing_4bet(prof, f, cfg, agg):
    f.comment("=== NOUS AVONS 3BETÉ ET FACE À UN 4BET : jam value/bluff, call, fold ===")
    f.group("BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 1 AND NumberOfRaisesBeforeFlop = 2 AND RaisesSinceLastPlay = 1")
    for lo, hi, v, b, c in _stack_lists(prof, cfg, "F4", cfg["fivebet_value"], cfg["fivebet_bluff"] * agg, cfg["call_4bet_pct"], agg):
        cond = join(f"f$Gen_EffStack > {lo}", f"f$Gen_EffStack <= {hi}") if hi < 10000 else f"f$Gen_EffStack > {lo}"
        _rules(prof, f, cfg, cond, v, b, c, v_action="RaiseMax", tag=f"F4S{hi}")
    f.others("Fold")


def _cold_facing_4bet(prof, f, cfg):
    f.comment("=== 4BET DEVANT NOUS (cold) : jam premium / call ===")
    f.group(join(FIRST, "Raises = 3"))
    for lo, hi, factor in stack_buckets():
        cond = join(f"f$Gen_EffStack > {lo}", f"f$Gen_EffStack <= {hi}") if hi < 10000 else f"f$Gen_EffStack > {lo}"
        jam = R.top_equity(round(cfg["fivebet_value"] * 0.7 * factor ** 0.5, 2))
        call_h = [h for h in R.top_equity(round((cfg["fivebet_value"] * 0.7 + cfg["call_4bet_pct"] * 0.5) * factor, 2)) if h not in jam]
        lj = prof.add_list(f"ColdF4J{hi}", jam)
        if lj != "false":
            f.act(join(cond, lj), "RaiseMax")
        lc = prof.add_list(f"ColdF4C{hi}", call_h)
        if lc != "false":
            f.act(join(cond, lc), "Call")
    f.others("Fold")


def _facing_5bet(prof, f, cfg):
    f.comment("=== FACE À UN 5BET OU UN ALL-IN PRÉFLOP : call selon la profondeur ===")
    f.group("Raises >= 2")
    for lo, hi, factor in stack_buckets():
        cond = join(f"f$Gen_EffStack > {lo}", f"f$Gen_EffStack <= {hi}") if hi < 10000 else f"f$Gen_EffStack > {lo}"
        pct = min(35.0, cfg["call_allin_pct"] * factor)
        lc = prof.add_list(f"AllinCall{hi}", R.top_equity(round(pct, 2)))
        if lc != "false":
            f.act(join(cond, lc), "Call")
    f.others("Fold")
