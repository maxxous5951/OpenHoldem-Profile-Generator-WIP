"""Briques communes : conditions de position, aléatoire, fonctions auxiliaires partagées."""
from __future__ import annotations

from ..ppl import Profile, fmt
from .. import ranges as R

HERO: dict[str, str] = {}
OPENER: dict[str, str] = {}
ORDER: list[str] = []  # positions actives, dans l'ordre d'action préflop
SEATS: dict[str, int] = {}  # nombre de sièges regroupés sous EP / MP
_SEAT_NAMES = ["EarlyPosition1", "EarlyPosition2", "EarlyPosition3",
               "MiddlePosition1", "MiddlePosition2", "MiddlePosition3"]


def configure(cfg: dict) -> None:
    """Fixe les positions réellement jouées selon la taille de table.

    OpenHoldem attribue les rôles en partant du bouton : BTN, CO, puis MP3, MP2, MP1, EP3, EP2, EP1.
    Ex. à 6 joueurs UTG = MiddlePosition2 (il n'y a pas d'EarlyPosition) ; à 3 joueurs il n'y a ni CO ni MP/EP.
    """
    n = int(cfg["table_size"])
    k = max(0, min(6, n - 4))  # sièges devant le CO
    seats = _SEAT_NAMES[len(_SEAT_NAMES) - k:] if k else []
    mp = k // 2
    groups = {"EP": seats[: k - mp], "MP": seats[k - mp:]}
    HERO.clear()
    OPENER.clear()
    ORDER.clear()
    SEATS.clear()
    for g, names in groups.items():
        if names:
            ORDER.append(g)
            SEATS[g] = len(names)
            HERO[g] = "(" + " OR ".join("In" + x for x in names) + ")" if len(names) > 1 else "In" + names[0]
            OPENER[g] = "(" + " OR ".join(x + "Raising" for x in names) + ")" if len(names) > 1 else names[0] + "Raising"
    if n >= 4:
        ORDER.append("CO")
        HERO["CO"], OPENER["CO"] = "InCutOff", "CutOffRaising"
    ORDER.extend(["BTN", "SB", "BB"])
    HERO.update({"BTN": "InButton", "SB": "InSmallBlind", "BB": "InBigBlind"})
    OPENER.update({"BTN": "ButtonRaising", "SB": "SmallBlindRaising"})


def actives(with_bb: bool = False) -> list[str]:
    return [p for p in ORDER if with_bb or p != "BB"]


OPEN_WIDTH = {"EP": 0.75, "MP": 0.9, "CO": 1.0, "BTN": 1.25, "SB": 1.35}


def openers_before(hero: str) -> list[str]:
    """Positions qui peuvent avoir ouvert avant `hero`."""
    if hero == "BB":
        return actives()
    i = ORDER.index(hero)
    out = ORDER[:i]
    if hero in ("EP", "MP") and SEATS.get(hero, 0) > 1:
        out = ORDER[: i + 1]  # un autre siège du même groupe a pu ouvrir
    return [o for o in out if o != "BB"]


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


ICM_K = {"standard": 1.0, "top2": 0.6, "wta": 0.0}


def icm(cfg: dict, key: str) -> float:
    """Valeur effective (0-100) d'un reglage ICM apres prise en compte de la structure des gains."""
    return cfg[key] * ICM_K[cfg["payout"]]


def bluff_scaled(cfg: dict) -> bool:
    """Vrai si la frequence de bluff postflop est modulee (stats, pot 3bet, texture, ICM) -> f$Gen_RRBluff existe."""
    return bool(cfg["use_stats"] or cfg["cbet_3bet_pot_scale"] != 100 or cfg["tex_dynamic_pct"] > 0
                or icm(cfg, "icm_postflop") > 0)


def rr_symbol(cfg: dict, kind: str | None) -> str:
    """Symbole d'aléatoire constant pendant la street. 'bluff' / 'value' passent par un facteur d'exploitation."""
    if kind == "bluff" and bluff_scaled(cfg):
        return "f$Gen_RRBluff"
    if kind == "value" and cfg["use_stats"]:
        return "f$Gen_RRValue"
    return "randomround"


def mix_round(cfg: dict, freq: float, kind: str | None = None):
    """Idem mais constant pendant la street (postflop)."""
    freq = max(0.0, min(1.0, freq))
    if freq >= 0.995:
        return ""
    if freq <= 0.005:
        return None
    if not cfg["randomize"]:
        return "" if freq >= 0.5 else None
    return f"{rr_symbol(cfg, kind)} < {freq:.2f}"


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
    if cfg["pf_max_stack"] > 0 or cfg["openjam_max"] > 0:
        f = prof.func("f$Gen_EffStackFirstIn")
        f.comment("Stack effectif contre les joueurs derrière nous (première action préflop)")
        f.ret("", "(MaxStillToActStackSize < StackSize ? MaxStillToActStackSize : StackSize)")
    f = prof.func("f$Gen_IP")
    f.comment("Vrai si nous agirons en dernier postflop")
    f.ret("StillToActPostflop = 0", "true")
    f.others_ret("false")
    f = prof.func("f$Gen_Facing")
    f.comment("Taille totale (en BB) de la mise adverse : ce qu'il reste à payer + ce que nous avons déjà mis (blinde, ouverture)."
              " BetSize (= ncallbets) ne donne que le complément, d'où RaiseTo faux pour les blindes et après notre relance")
    f.ret("", "AmountToCall + ncurrentbets")
    f = prof.func("f$Gen_Multiway")
    f.ret("Opponents >= 2", "true")
    f.others_ret("false")
