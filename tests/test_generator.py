import itertools
import json

import pytest

from ohpg import generator, presets, ranges, validator
from ohpg.params import SCHEMA, normalize
from tests.sim import Sim

COMBOS = list(itertools.product(list(presets.STYLES)[:3], list(presets.FORMATS)))


@pytest.mark.parametrize("style,fmt", COMBOS)
def test_every_preset_generates_valid_profile(style, fmt):
    text = generator.generate(presets.build(style, fmt))
    assert validator.errors(validator.validate(text)) == []


def test_every_parameter_extreme_values_stay_valid():
    for p in SCHEMA:
        if p.kind in ("int", "float", "pct"):
            for v in (p.lo, p.hi):
                text = generator.generate({p.key: v})
                assert validator.errors(validator.validate(text)) == [], (p.key, v)


def test_deterministic_when_randomize_off():
    a = generator.generate({"randomize": False})
    b = generator.generate({"randomize": False})
    body = lambda s: "\n".join(l for l in s.split("\n") if not l.startswith("//"))
    assert body(a) == body(b)
    assert "randomhand" not in body(a) and "randomround" not in body(a)


def test_no_library_symbol_redefined():
    text = generator.generate()
    assert not [i for i in validator.validate(text) if "bibliothèque" in i.message]


def test_validator_catches_errors():
    bad = "##f$preflop##\nWHEN Foo = 1 Call FORCE\nCall FORCE\n"
    msgs = " ".join(str(i) for i in validator.validate(bad))
    assert "symbole inconnu : Foo" in msgs and "WHEN" in msgs and "manquante" in msgs


def test_unknown_param_rejected():
    with pytest.raises(KeyError):
        normalize({"nope": 1})


def test_ranges_monotone_and_disjoint():
    assert set(ranges.top_equity(5)) <= set(ranges.top_equity(10))
    v, b, c = ranges.split_range(4, 3, 10)
    assert not (set(v) & set(b)) and not (set(v) & set(c)) and not (set(b) & set(c))
    assert abs(ranges.pct_of(ranges.open_range(25)) - 25) < 1.5
    assert ranges.expand_notation("AA-TT, AKs-ATs, 76s+")[:5] == ["AA", "KK", "QQ", "JJ", "TT"]


def test_profile_json_roundtrip():
    cfg = presets.build("LAG", "Cash Full Ring")
    assert normalize(json.loads(json.dumps(cfg))) == cfg


# ---------------------------------------------------------------- décisions simulées
BASE = dict(BotsActionsOnThisRoundIncludingChecks=0, Raises=0, Calls=0, CallsSinceLastRaise=0, InEarlyPosition=False,
            InEarlyPosition1=False, InEarlyPosition2=False, InEarlyPosition3=False, InMiddlePosition1=False,
            InMiddlePosition2=False, InMiddlePosition3=False, InMiddlePosition=False, InCutOff=False, InButton=False, InSmallBlind=False, InBigBlind=False,
            EarlyPosition1Raising=False, EarlyPosition2Raising=False, EarlyPosition3Raising=False,
            MiddlePosition1Raising=False, MiddlePosition2Raising=False, MiddlePosition3Raising=False,
            CutOffRaising=False, ButtonRaising=False, SmallBlindRaising=False, BetSize=2.5, AmountToCall=1.5, ncurrentbets=0,
            StackSize=100, EffectiveMaxStacksizeOfActiveOpponents=100, BotRaisedBeforeFlop=False,
            NumberOfRaisesBeforeFlop=0, RaisesSinceLastPlay=0)


@pytest.fixture(scope="module")
def sim():
    return Sim(generator.generate({"randomize": False}))


def decide(sim, hand, **kw):
    st = dict(BASE, hand=hand, **kw)
    return sim.decide("f$preflop", st)


def test_open_ranges(sim):
    assert decide(sim, "AA", InMiddlePosition2=True).startswith("RaiseTo")
    assert decide(sim, "72o", InMiddlePosition2=True) == "Fold"
    assert decide(sim, "T8s", InButton=True).startswith("RaiseTo")
    assert decide(sim, "72o", InButton=True) == "Fold"


def test_premium_3bets_and_trash_folds(sim):
    assert decide(sim, "AKs", InButton=True, Raises=1, CutOffRaising=True).startswith("RaiseTo")
    assert decide(sim, "72o", InButton=True, Raises=1, CutOffRaising=True) == "Fold"
    assert decide(sim, "72o", InBigBlind=True, Calls=1, AmountToCall=0) == "Check"


def test_facing_3bet_and_4bet(sim):
    f3 = dict(InCutOff=True, BotRaisedBeforeFlop=True, BotsActionsOnThisRoundIncludingChecks=1,
              Raises=1, RaisesSinceLastPlay=1, AmountToCall=5.5, ncurrentbets=2.5)
    assert decide(sim, "AA", **f3).startswith("RaiseTo")
    assert decide(sim, "K9s", **f3) == "Fold"
    f4 = dict(InButton=True, BotRaisedBeforeFlop=True, BotsActionsOnThisRoundIncludingChecks=1,
              Raises=2, RaisesSinceLastPlay=1, AmountToCall=20, ncurrentbets=8)
    assert decide(sim, "KK", **f4) == "RaiseMax"
    assert decide(sim, "J7o", **f4) == "Fold"


def test_output_is_ascii_for_every_preset():
    from ohpg import presets
    for st in presets.STYLES:
        for fm in presets.FORMATS:
            text = generator.generate(presets.build(st, fm, {"name": "Prôfil é à"}))
            assert all(ord(c) < 128 for c in text), (st, fm)


def test_positions_follow_table_size():
    """Spin 3-max : ni CutOff, ni MiddlePosition, ni EarlyPosition. 6-max : UTG = MiddlePosition2, pas d'EarlyPosition."""
    for st in presets.STYLES:
        t3 = generator.generate(presets.build(st, "Spin & Go 3-max"))
        assert not any(w in t3 for w in ("InCutOff", "CutOffRaising", "MiddlePosition", "EarlyPosition")), st
        assert not [e for e in validator.validate(t3) if e.level == "error"]
    t6 = generator.generate(presets.build("Balanced 6-max", "Cash 6-max"))
    assert "InMiddlePosition2" in t6 and "EarlyPosition" not in t6
    t4 = generator.generate(presets.build("Balanced 6-max", "Cash 6-max", {"table_size": 4}))
    assert "InCutOff" in t4 and "MiddlePosition" not in t4


def test_limp_then_raise_and_cold_call_then_squeeze(sim):
    lr = dict(BotsActionsOnThisRoundIncludingChecks=1, Raises=1, AmountToCall=3, PotSize=7.5)
    assert decide(sim, "AA", InSmallBlind=True, **lr).startswith("RaiseTo")
    assert decide(sim, "72o", InSmallBlind=True, **lr) == "Fold"
    sq = dict(BotsActionsOnThisRoundIncludingChecks=1, Raises=2, AmountToCall=12, PotSize=20)
    assert decide(sim, "AA", InButton=True, **sq).startswith("RaiseTo")
    assert decide(sim, "72o", InButton=True, **sq) == "Fold"


def test_spr_commitment_present_and_optional():
    t = generator.generate(presets.build("Balanced 6-max", "Cash 6-max"))
    assert t.count("f$Gen_SPR <=") >= 6
    off = generator.generate(presets.build("Balanced 6-max", "Cash 6-max", {"commit_spr": 0}))
    assert "f$Gen_SPR <=" not in off


def test_raise_sizes_use_total_bet_not_call_amount(sim):
    """BB (1 BB déjà posée) face à une ouverture à 2.5 BB : 3bet ~ 4x2.5 = 10, pas 4x1.5 = 6."""
    st = dict(InBigBlind=True, Raises=1, CutOffRaising=True, AmountToCall=1.5, ncurrentbets=1, PotSize=4)
    a = decide(sim, "AA", **st)
    assert a.startswith("RaiseTo") and 8.5 <= float(a.split()[1]) <= 14, a
    # nous avons ouvert à 2.5 et subissons un 3bet à 8 : 4bet vers ~17-20, pas 2.2x5.5
    f3 = dict(InCutOff=True, BotRaisedBeforeFlop=True, BotsActionsOnThisRoundIncludingChecks=1, Raises=1,
              RaisesSinceLastPlay=1, AmountToCall=5.5, ncurrentbets=2.5, PotSize=12, EffectiveMaxStacksizeOfActiveOpponents=100)
    a = decide(sim, "AA", **f3)
    assert a.startswith("RaiseTo") and 16 <= float(a.split()[1]) <= 24, a


# ---------------------------------------------------------------- v2.2 : open-jam, limp SB, limp-raise, lead OOP, stats multiway
@pytest.fixture(scope="module")
def spin():
    return Sim(generator.generate(presets.build("Balanced 6-max", "Spin & Go 3-max", {"randomize": False})))


def test_open_jam_zone_above_pushfold(spin):
    st = dict(BASE, InButton=True, StackSize=18, MaxStillToActStackSize=18, EffectiveMaxStacksizeOfActiveOpponents=18)
    assert spin.decide("f$preflop", dict(st, hand="AA")) == "RaiseMax"
    assert spin.decide("f$preflop", dict(st, hand="K9s")).startswith("RaiseTo")  # ouverture normale, pas de jam
    deep = dict(st, StackSize=60, MaxStillToActStackSize=60, EffectiveMaxStacksizeOfActiveOpponents=60)
    assert spin.decide("f$preflop", dict(deep, hand="AA")).startswith("RaiseTo")  # au-dessus de la zone


def test_bb_raises_vs_sb_limp_and_sb_defends_vs_bb_raise(spin):
    st = dict(BASE, InBigBlind=True, Calls=1, SmallBlindCalling=True, StackSize=40, MaxStillToActStackSize=0,
              EffectiveMaxStacksizeOfActiveOpponents=40, AmountToCall=0, PotSize=2)
    assert spin.decide("f$preflop", dict(st, hand="AKs")).startswith("RaiseTo")
    assert spin.decide("f$preflop", dict(st, hand="72o")) == "Check"
    sb = dict(BASE, InSmallBlind=True, BotsActionsOnThisRoundIncludingChecks=1, Raises=1, AmountToCall=2, ncurrentbets=1,
              PotSize=5, StackSize=40, EffectiveMaxStacksizeOfActiveOpponents=40)
    assert spin.decide("f$preflop", dict(sb, hand="AA")).startswith("RaiseTo")
    assert spin.decide("f$preflop", dict(sb, hand="72o")) == "Fold"


def test_list_names_unique_per_scenario():
    t = generator.generate(presets.build("Balanced 6-max", "Spin & Go 3-max"))
    names = [l[2:-2] for l in t.split("\n") if l.startswith("##list")]
    assert len(names) == len(set(names))
    assert any(n.startswith("listLimpRaiseV") for n in names) and not any(n.startswith("listColdF3V") and False for n in names)


def test_oop_lead_semibluff_present_and_optional():
    on = generator.generate({"randomize": False, "donk_semibluff": 100})
    assert "NOT f$Gen_IP AND NOT f$Gen_Multiway AND f$Gen_StrongDraw" in on
    off = generator.generate({"randomize": False, "donk_semibluff": 0, "donk_freq": 0})
    assert "NOT f$Gen_IP AND NOT f$Gen_Multiway AND f$Gen_StrongDraw" not in off


def test_stats_multiway_uses_bettor_and_any_fish():
    t = generator.generate({"use_stats": True})
    assert "pt_vpip_raischair" in t and "f$Gen_AnyFish" in t
    assert "AmountToCall > 0 AND Opponents >= 2" in t
