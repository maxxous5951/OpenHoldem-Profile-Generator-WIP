"""Balayage exhaustif des situations : aucun trou (pas de None, pas de fold gratuit, pas de premium foldée...)."""
import collections
import itertools

import pytest

from ohpg import generator, presets
from tests import test_generator as T
from tests.sim import Sim

POS = {"UTG": dict(InMiddlePosition2=True), "HJ": dict(InMiddlePosition3=True), "CO": dict(InCutOff=True),
       "BTN": dict(InButton=True), "SB": dict(InSmallBlind=True), "BB": dict(InBigBlind=True)}
OPEN = {"UTG": "MiddlePosition2Raising", "HJ": "MiddlePosition3Raising", "CO": "CutOffRaising",
        "BTN": "ButtonRaising", "SB": "SmallBlindRaising"}
ORDER = list(POS)
CATS = ["Monster", "Strong", "Medium", "StrongDraw", "NutDraw", "WeakDraw", "WeakSD", "Air"]


def _preflop_states():
    for pos in POS:
        i = ORDER.index(pos)
        for stack in (30, 100):
            for r, c in itertools.product(range(0, 5), range(0, 3)):
                for op in ([None] if r == 0 else list(OPEN)):
                    if op and ORDER.index(op) >= i:
                        continue
                    if r == 0 and pos == "BB" and c == 0:
                        continue
                    atc = (0 if pos == "BB" else 1) if r == 0 else 2.5 * 2.5 ** (r - 1)
                    yield dict(kind="first", pos=pos, stack=stack, r=r, c=c, op=op, acted=0, br=False, atc=atc)
            for r, c, op in itertools.product((2, 3, 4), (0, 1), OPEN):
                if ORDER.index(op) < i:
                    yield dict(kind="raised_then_faced", pos=pos, stack=stack, r=r, c=c, op=op, acted=1, br=True, atc=2.5 * 2.5 ** (r - 1))
            for r, c, op in itertools.product((1, 2, 3), (0, 1), OPEN):
                if ORDER.index(op) < i:
                    yield dict(kind="called_then_faced", pos=pos, stack=stack, r=r, c=c, op=op, acted=1, br=False, atc=2.5 * 2.5 ** (r - 1))


@pytest.mark.parametrize("style,fmt", [("Balanced 6-max", "Cash 6-max"), ("Nit", "Cash Full Ring")])
def test_preflop_has_no_holes(style, fmt):
    sim = Sim(generator.generate(presets.build(style, fmt)))
    bad = collections.Counter()
    for s in _preflop_states():
        for hand in ("AA", "KK", "AKs", "99", "72o"):
            st = dict(**POS[s["pos"]], BotsActionsOnThisRoundIncludingChecks=s["acted"], Raises=s["r"], Calls=s["c"],
                      CallsSinceLastRaise=s["c"] if s["r"] else 0, BotRaisedBeforeFlop=s["br"], NumberOfRaisesBeforeFlop=s["r"],
                      RaisesSinceLastPlay=(s["r"] - 1 if s["br"] else s["r"]) if s["acted"] else s["r"], AmountToCall=s["atc"],
                      PotSize=1.5 + s["atc"] * (1 + s["c"]), BetSize=max(s["atc"], 2.5),
                      EffectiveMaxStacksizeOfActiveOpponents=s["stack"], StackSize=s["stack"],
                      **({OPEN[s["op"]]: True} if s["op"] else {}))
            a = T.decide(sim, hand, **st)
            if a is None:
                bad[("none", s["kind"])] += 1
            elif a == "Check" and s["atc"] > 0:
                bad[("check-facing-bet", s["kind"])] += 1
            elif hand in ("AA", "KK") and a == "Fold":
                bad[("premium-fold", hand, s["kind"], s["r"])] += 1
            elif hand == "AA" and a == "Call" and s["r"] >= 3 and s["stack"] >= 30:
                bad[("aa-only-calls", s["kind"], s["r"])] += 1
    assert not bad, dict(bad)


def _post_state(**kw):
    return kw


@pytest.mark.parametrize("over", [{}, {"use_stats": True}])
def test_postflop_has_no_holes(over):
    sim = Sim(generator.generate(presets.build("Balanced 6-max", "Cash 6-max", over)))
    bad = collections.Counter()
    for street in ("flop", "turn", "river"):
        for cat in CATS:
            if street == "river" and cat in ("StrongDraw", "NutDraw", "WeakDraw"):
                continue
            for ip, mw, tex, spr, kind, (acted, rsl), br, (bro, nbf), rr in itertools.product(
                    (True, False), (True, False), (6,), (1.0, 15.0), ("none", "small", "big", "allin"),
                    ((0, 0), (1, 0), (1, 1)), (True, False), ((False, False), (True, False), (False, True)), (0.99,)):
                atc = {"none": 0, "small": 3, "big": 12, "allin": spr * 20}[kind]
                if atc == 0 and rsl or (atc > 0 and acted == 0 and rsl):
                    continue
                pot = 20
                st = {"f$gen_ip": ip, "f$gen_multiway": mw, "f$gen_tex": tex, "f$gen_spr": spr, "f$gen_pottype": 1,
                      "f$gen_potodds": atc / (pot + atc) if atc else 0, "f$gen_rawodds": atc / (pot + atc) if atc else 0,
                      "f$gen_wechecked": acted == 1 and rsl == 0 and atc > 0, "amounttocall": atc, "potsize": pot,
                      "stacksize": spr * pot, "raisessincelastplay": rsl, "botsactionsonthisroundincludingchecks": acted,
                      "botsactionsonthisround": 0 if (acted == 1 and rsl == 0) else acted, "botraisedbeforeflop": br,
                      "botraisedonflop": bro, "nobettingonflop": nbf, "botraisedonturn": bro, "havenuts": False,
                      "hand": "AA", "f$gen_blockers": True, "f$gen_scare": False, "f$gen_goodbarrelcard": True,
                      "betround": 2, "opponents": 2 if mw else 1, "randomround": rr, "randomhand": rr,
                      "f$gen_rrbluff": rr, "f$gen_rrvalue": rr}
                for c in CATS:
                    st["f$gen_" + c.lower()] = (c == cat) or (c == "Strong" and cat == "Monster") or (c == "StrongDraw" and cat == "NutDraw")
                a = sim.decide("f$" + street, st)
                if a is None:
                    bad[("none", street, cat)] += 1
                elif a == "Check" and atc > 0:
                    bad[("check-facing-bet", street, cat)] += 1
                elif a == "Fold" and atc == 0:
                    bad[("fold-free", street, cat)] += 1
                elif cat == "Monster" and a == "Fold":
                    bad[("monster-fold", street, kind)] += 1
                elif cat == "Monster" and atc == 0 and a == "Check" and ip and not mw and street == "river" and rr < 0.5:
                    bad[("monster-checks-river-ip", street)] += 1
    assert not bad, dict(bad)


def _flop_state(**kw):
    st = {"f$gen_ip": False, "f$gen_multiway": False, "f$gen_tex": 6, "f$gen_spr": 15.0, "f$gen_pottype": 1,
          "f$gen_potodds": 0.13, "f$gen_rawodds": 0.13, "f$gen_wechecked": True, "amounttocall": 3, "potsize": 20,
          "stacksize": 300, "raisessincelastplay": 1, "botsactionsonthisroundincludingchecks": 1, "botsactionsonthisround": 0,
          "botraisedbeforeflop": False, "havenuts": False, "hand": "AA", "f$gen_blockers": True, "randomround": 0.01,
          "randomhand": 0.01, "f$gen_rrbluff": 0.01, "f$gen_rrvalue": 0.01, "betround": 2, "opponents": 1}
    for c in CATS:
        st["f$gen_" + c.lower()] = False
    st.update(kw)
    return st


def test_checked_then_bet_plans_check_raise_and_allin_never_raises():
    sim = Sim(generator.generate(presets.build("Balanced 6-max", "Cash 6-max")))
    mon = {"f$gen_monster": True, "f$gen_strong": True}
    assert sim.decide("f$flop", _flop_state(**mon)).startswith("RaiseBy")                       # check-raise value
    assert sim.decide("f$flop", _flop_state(randomround=0.99, **mon)) == "Call"                   # sinon call
    allin = _flop_state(amounttocall=300, f_potodds=0.0, **mon)
    allin["f$gen_potodds"] = allin["f$gen_rawodds"] = 300 / 320
    assert sim.decide("f$flop", allin) == "Call"                                                 # all-in : jamais de relance


def test_stats_make_us_exploit_nits_and_maniacs_preflop():
    sim = Sim(generator.generate(presets.build("Balanced 6-max", "Cash 6-max", {"use_stats": True})))
    from ohpg import ranges as R

    def cont(vpip, pfr, af, hands=300):
        n = 0
        for h in R.EQUITY_ORDER:
            st = dict(T.BASE, hand=h, InButton=True, Raises=1, CutOffRaising=True, NumberOfRaisesBeforeFlop=1,
                      RaisesSinceLastPlay=1, AmountToCall=2.5, PotSize=4, BetSize=2.5, EffectiveMaxStacksizeOfActiveOpponents=100,
                      pt_hands_lastraiserchair=hands, pt_vpip_lastraiserchair=vpip, pt_pfr_lastraiserchair=pfr,
                      pt_aggr_factor_lastraiserchair=af, pt_hands_firstcallerchair=0, pt_vpip_firstcallerchair=0,
                      pt_pfr_firstcallerchair=0, pt_aggr_factor_firstcallerchair=0)
            n += T.decide(sim, h, **{k: v for k, v in st.items() if k not in ("hand",)}) != "Fold"
        return n

    default = cont(0.22, 0.18, 2.0, hands=0)      # pas assez de mains : comportement normal
    nit, maniac, fish = cont(0.12, 0.10, 1.5), cont(0.40, 0.30, 4.5), cont(0.50, 0.08, 1.2)
    assert nit < default < maniac and default < fish, (nit, default, fish, maniac)


def test_big_pot_and_stats_helpers_are_emitted():
    t = generator.generate(presets.build("Balanced 6-max", "Cash 6-max", {"use_stats": True}))
    for name in ("f$Gen_PotType", "f$Gen_WeChecked", "f$Gen_RRBluff", "f$Gen_CallTol", "f$Gen_PostNit", "f$Gen_RsFish"):
        assert f"##{name}##" in t, name
    plain = generator.generate(presets.build("Balanced 6-max", "Cash 6-max", {"cbet_3bet_pot_scale": 100, "call_3bet_pot_scale": 100, "tex_dynamic_pct": 0}))
    assert "##f$Gen_RRBluff##" not in plain and "pt_" not in plain


def test_board_texture_classes():
    sim = Sim(generator.generate(presets.build("Balanced 6-max", "Cash 6-max")))
    base = {"nsuitedcommon": 1, "paironboard": False, "f$gen_txconnected": False, "bestboardcard": 14}
    cases = [(dict(nsuitedcommon=3), 1), (dict(paironboard=True, bestboardcard=13), 3),
             (dict(nsuitedcommon=2, **{"f$gen_txconnected": True}, bestboardcard=9), 2),
             (dict(**{"f$gen_txconnected": True}, bestboardcard=9), 4), (dict(nsuitedcommon=2), 5),
             (dict(bestboardcard=14), 6), (dict(bestboardcard=13), 7), (dict(bestboardcard=10), 8), (dict(bestboardcard=7), 9)]
    for over, code in cases:
        assert sim.call_func("f$Gen_Tex", dict(base, **over)) == code, (over, code)


def test_texture_drives_bluffs_defense_and_stack_bounds_use_ge():
    t = generator.generate(presets.build("Balanced 6-max", "Cash 6-max"))
    for name in ("f$Gen_TexBluff", "f$Gen_TexTol", "f$Gen_TxConnected"):
        assert f"##{name}##" in t, name
    assert "f$Gen_RRBluff < " in t                      # les bluffs river passent par le facteur texture
    off = generator.generate(presets.build("Balanced 6-max", "Cash 6-max", {"tex_dynamic_pct": 0, "cbet_3bet_pot_scale": 100}))
    assert "##f$Gen_TexBluff##" not in off
    import re
    tourney = generator.generate(presets.build("Balanced 6-max", "MTT 9-max (push/fold 15BB)"))
    assert not re.search(r"f\$Gen_EffStack(FirstIn)? > ", t + tourney)
    assert "f$Gen_EffStackFirstIn >= 0" in tourney
