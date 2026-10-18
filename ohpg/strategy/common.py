"""Briques communes : conditions de position, aléatoire, fonctions auxiliaires partagées."""
from __future__ import annotations

from ..ppl import Profile, fmt
from .. import ranges as R

HERO = {
    "EP": "InEarlyPosition", "MP": "InMiddlePosition", "CO": "InCutOff",
    "BTN": "InButton", "SB": "InSmallBlind", "BB": "InBigBlind",
}
OPENER = {
    "EP": "(EarlyPosition1Raising OR EarlyPosition2Raising OR EarlyPosition3Raising)",
    "MP": "(MiddlePosition1Raising OR MiddlePosition2Raising OR MiddlePosition3Raising)",
    "CO": "CutOffRaising",
    "BTN": "ButtonRaising",
    "SB": "SmallBlindRaising",
}
ORDER = ["EP", "MP", "CO", "BTN", "SB", "BB"]  # ordre d'action préflop
OPEN_WIDTH = {"EP": 0.75, "MP": 0.9, "CO": 1.0, "BTN": 1.25, "SB": 1.35}


def openers_before(hero: str) -> list[str]:
    """Positions qui peuvent avoir ouvert avant `hero`."""
    i = ORDER.index(hero)
    out = ORDER[: i + 1] if hero in ("EP", "MP") else ORDER[:i]
    out = [o for o in out if o != "BB"]
    if hero == "EP":
        return ["EP"]
    if hero == "MP":
        return ["EP", "MP"]
    return out


def is_ip_vs_opener(hero: str, opener: str) -> bool:
    """Hero sera-t-il en position postflop face à l'ouvreur ?"""
    if hero == "BTN":
        return True
    if hero == "CO":
        return opener in ("EP", "MP")
    return False


def mix(cfg: dict, freq: float):
    """Condition d'aléatoire. '' = toujours, None = jamais, sinon 'randomhand < x'."""
    freq = max(0.0, min(1.0, freq))
    if freq >= 0.995:
        return ""
    if freq <= 0.005:
        return None
    if not cfg["randomize"]:
        return "" if freq >= 0.5 else None
    return f"randomhand < {freq:.2f}"


def mix_round(cfg: dict, freq: float):
    """Idem mais constant pendant la street (postflop)."""
    freq = max(0.0, min(1.0, freq))
    if freq >= 0.995:
        return ""
    if freq <= 0.005:
        return None
    if not cfg["randomize"]:
        return "" if freq >= 0.5 else None
    return f"randomround < {freq:.2f}"


def tiers(hands, full_share=0.75):
    """Sépare une liste (triée du meilleur au pire) : le bas de liste sera joué à fréquence mixte."""
    hands = list(hands)
    if len(hands) < 4:
        return hands, []
    k = max(1, round(len(hands) * full_share))
    return hands[:k], hands[k:]


def join(*conds: str) -> str:
    return " AND ".join(c for c in conds if c)


def stack_buckets():
    """(borne basse, borne haute, facteur d'élargissement des calls d'all-in) selon la profondeur."""
    return [(0, 8, 3.2), (8, 12, 2.6), (12, 18, 2.0), (18, 25, 1.6), (25, 40, 1.25), (40, 10000, 1.0)]


def emit_common_helpers(prof: Profile, cfg: dict):
    f = prof.func("f$Gen_EffStack")
    f.comment("Stack effectif en BB (petit stack entre nous et le plus gros adversaire encore en jeu)")
    f.ret("", "EffectiveMaxStacksizeOfActiveOpponents")
    if cfg["pf_max_stack"] > 0:
        f = prof.func("f$Gen_EffStackFirstIn")
        f.comment("Stack effectif contre les joueurs derrière nous (première action préflop)")
        f.ret("", "(MaxStillToActStackSize < StackSize ? MaxStillToActStackSize : StackSize)")
    f = prof.func("f$Gen_IP")
    f.comment("Vrai si nous agirons en dernier postflop")
    f.ret("StillToActPostflop = 0", "true")
    f.others_ret("false")
    f = prof.func("f$Gen_PotOdds")
    f.comment("Équité nécessaire pour payer : AmountToCall / (PotSize + AmountToCall)")
    f.ret("AmountToCall <= 0", 0)
    f.others_ret("AmountToCall / (PotSize + AmountToCall)")
    f = prof.func("f$Gen_Multiway")
    f.ret("Opponents >= 2", "true")
    f.others_ret("false")
