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
            InMiddlePosition=False, InCutOff=False, InButton=False, InSmallBlind=False, InBigBlind=False,
            EarlyPosition1Raising=False, EarlyPosition2Raising=False, EarlyPosition3Raising=False,
            MiddlePosition1Raising=False, MiddlePosition2Raising=False, MiddlePosition3Raising=False,
            CutOffRaising=False, ButtonRaising=False, SmallBlindRaising=False, BetSize=2.5, AmountToCall=1.5,
            StackSize=100, EffectiveMaxStacksizeOfActiveOpponents=100, BotRaisedBeforeFlop=False,
            NumberOfRaisesBeforeFlop=0, RaisesSinceLastPlay=0)


@pytest.fixture(scope="module")
def sim():
    return Sim(generator.generate({"randomize": False}))


def decide(sim, hand, **kw):
    st = dict(BASE, hand=hand, **kw)
    return sim.decide("f$preflop", st)


def test_open_ranges(sim):
    assert decide(sim, "AA", InEarlyPosition=True).startswith("RaiseTo")
    assert decide(sim, "72o", InEarlyPosition=True) == "Fold"
    assert decide(sim, "T8s", InButton=True).startswith("RaiseTo")
    assert decide(sim, "72o", InButton=True) == "Fold"


def test_premium_3bets_and_trash_folds(sim):
    assert decide(sim, "AKs", InButton=True, Raises=1, CutOffRaising=True).startswith("RaiseTo")
    assert decide(sim, "72o", InButton=True, Raises=1, CutOffRaising=True) == "Fold"
    assert decide(sim, "72o", InBigBlind=True, Calls=1, AmountToCall=0) == "Check"


def test_facing_3bet_and_4bet(sim):
    f3 = dict(InCutOff=True, BotRaisedBeforeFlop=True, BotsActionsOnThisRoundIncludingChecks=1,
              NumberOfRaisesBeforeFlop=1, RaisesSinceLastPlay=1, BetSize=8)
    assert decide(sim, "AA", **f3).startswith("RaiseTo")
    assert decide(sim, "K9s", **f3) == "Fold"
    f4 = dict(InButton=True, BotRaisedBeforeFlop=True, BotsActionsOnThisRoundIncludingChecks=1,
              NumberOfRaisesBeforeFlop=2, RaisesSinceLastPlay=1, BetSize=20)
    assert decide(sim, "KK", **f4) == "RaiseMax"
    assert decide(sim, "J7o", **f4) == "Fold"
