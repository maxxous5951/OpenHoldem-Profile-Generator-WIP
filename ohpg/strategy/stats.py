"""Couche d'exploitation des adversaires (stats PokerTracker exposées par OpenHoldem : pt_*).

Les stats sont lues par « chair » (multiplexeur d'OpenHoldem) :
  - Rs : dernier relanceur (lastraiserchair)        -> préflop (ouvreur / 3beteur)
  - Lm : premier limper (firstcallerchair)          -> isolation des limpers
  - HU : dernier adversaire (headsupchair)          -> postflop heads-up ; sinon Rs
Les valeurs sont normalisées en fraction (0..1) que PokerTracker les renvoie en % ou en fraction.
"""
from __future__ import annotations

from ..ppl import Profile, fmt

CHAIRS = {"HU": "headsupchair", "Rs": "lastraiserchair", "Lm": "firstcallerchair", "Rz": "raischair"}


def _stat_funcs(prof: Profile, chair_tag: str, chair: str):
    f = prof.func(f"f$Gen_Hands{chair_tag}")
    f.ret("", f"pt_hands_{chair}")
    for name, sym in (("VPIP", "vpip"), ("PFR", "pfr")):
        f = prof.func(f"f$Gen_{name}{chair_tag}")
        f.ret(f"pt_{sym}_{chair} > 1", f"pt_{sym}_{chair} / 100")
        f.others_ret(f"pt_{sym}_{chair}")
    f = prof.func(f"f$Gen_AF{chair_tag}")
    if chair_tag == "Rz":  # pas de facteur d'agression global fiable pour raischair : on s'appuie sur le PFR
        f.ret("", "0")
    else:
        f.ret("", f"pt_aggr_factor_{chair}")


def _classify(prof: Profile, cfg: dict, tag: str, src: dict[str, str] | None, nit: bool = True):
    """Crée Known / Maniac / Fish / Nit pour `tag`. `src` = sélection de chair (voir _post_selectors)."""
    h, v, p, a = (f"f$Gen_{n}{tag}" for n in ("Hands", "VPIP", "PFR", "AF"))
    f = prof.func(f"f$Gen_{tag}Known")
    f.ret(f"{h} >= {cfg['stats_min_hands']}", "true")
    f.others_ret("false")
    f = prof.func(f"f$Gen_{tag}Maniac")
    f.ret(f"f$Gen_{tag}Known AND {v} >= 0.25 AND ({p} >= {cfg['opp_maniac_pfr'] / 100:.2f} OR {a} >= {fmt(cfg['opp_maniac_af'])})", "true")
    f.others_ret("false")
    f = prof.func(f"f$Gen_{tag}Fish")
    f.ret(f"f$Gen_{tag}Known AND NOT f$Gen_{tag}Maniac AND {v} >= {cfg['opp_fish_vpip'] / 100:.2f}", "true")
    f.others_ret("false")
    if nit:
        f = prof.func(f"f$Gen_{tag}Nit")
        f.ret(f"f$Gen_{tag}Known AND {v} <= {cfg['opp_nit_vpip'] / 100:.2f}", "true")
        f.others_ret("false")


def emit_preflop(prof: Profile, cfg: dict):
    if not cfg["use_stats"]:
        return
    for tag in ("Rs", "Lm"):
        _stat_funcs(prof, tag, CHAIRS[tag])
        _classify(prof, cfg, tag, None, nit=(tag == "Rs"))


def emit_postflop(prof: Profile, cfg: dict):
    """Fonctions de classification de l'adversaire postflop + facteurs de bluff / value / call."""
    if cfg["use_stats"]:
        _stat_funcs(prof, "HU", CHAIRS["HU"])
        _stat_funcs(prof, "Rz", CHAIRS["Rz"])
        # sélection : face à une mise -> le joueur qui a misé (raischair) ; heads-up -> headsupchair ;
        # sinon (multiway, personne n'a misé) -> dernier relanceur préflop
        for name in ("Hands", "VPIP", "PFR", "AF"):
            f = prof.func(f"f$Gen_{name}Post")
            f.ret("AmountToCall > 0 AND Opponents >= 2", f"f$Gen_{name}Rz")
            f.ret("Opponents = 1", f"f$Gen_{name}HU")
            f.others_ret(f"f$Gen_{name}Rs")
        _classify(prof, cfg, "Post", None)
        f = prof.func("f$Gen_AnyFish")
        f.comment("Multiway, personne n'a misé : un fish dans le pot (dernier relanceur ou premier caller)")
        f.ret("Opponents >= 2 AND AmountToCall = 0 AND (f$Gen_RsFish OR f$Gen_LmFish)", "true")
        f.others_ret("false")
        f = prof.func("f$Gen_OppTol")
        f.comment("Tolérance de call selon l'adversaire (nit : on paye moins, maniaque : on paye plus)")
        f.ret("f$Gen_PostManiac", f"{cfg['exploit_call_maniac'] / 100:.2f}")
        f.ret("f$Gen_PostFish", f"{cfg['exploit_call_fish'] / 100:.2f}")
        f.ret("f$Gen_PostNit", f"{cfg['exploit_call_nit'] / 100:.2f}")
        f.others_ret("1")
        f = prof.func("f$Gen_OppBluff")
        f.comment("Facteur sur la fréquence de bluff selon l'adversaire")
        f.ret("f$Gen_PostManiac", f"{cfg['exploit_bluff_maniac'] / 100:.2f}")
        f.ret("f$Gen_PostFish OR f$Gen_AnyFish", f"{cfg['exploit_bluff_fish'] / 100:.2f}")
        f.ret("f$Gen_PostNit", f"{cfg['exploit_bluff_nit'] / 100:.2f}")
        f.others_ret("1")
        f = prof.func("f$Gen_OppValue")
        f.comment("Facteur sur la value fine : un fish paye trop, on value plus souvent")
        f.ret("f$Gen_PostFish OR f$Gen_AnyFish", f"{cfg['exploit_value_fish'] / 100:.2f}")
        f.others_ret("1")
    # type de pot
    f = prof.func("f$Gen_PotType")
    f.comment("Type de pot préflop : 1 = ouvert/limpé, 2 = 3bet, 3 = 4bet ou plus. "
              "NumberOfRaisesBeforeFlop ne compte que les relances adverses : on ajoute la nôtre.")
    f.ret("BotRaisedBeforeFlop AND NumberOfRaisesBeforeFlop >= 2", 3)
    f.ret("BotRaisedBeforeFlop AND NumberOfRaisesBeforeFlop = 1", 2)
    f.ret("NOT BotRaisedBeforeFlop AND NumberOfRaisesBeforeFlop >= 3", 3)
    f.ret("NOT BotRaisedBeforeFlop AND NumberOfRaisesBeforeFlop = 2", 2)
    f.others_ret("1")
    f = prof.func("f$Gen_WeChecked")
    f.comment("Vrai si nous avons checké dans ce tour d'enchères (donc faisons face à une mise après check)")
    f.ret("BotsActionsOnThisRound = 0 AND BotsActionsOnThisRoundIncludingChecks >= 1", "true")
    f.others_ret("false")
    # cotes brutes / ajustées
    f = prof.func("f$Gen_RawOdds")
    f.comment("Équité nécessaire pour payer : AmountToCall / (PotSize + AmountToCall)")
    f.ret("AmountToCall <= 0", 0)
    f.others_ret("AmountToCall / (PotSize + AmountToCall)")
    tol = cfg["call_3bet_pot_scale"] / 100.0
    k = cfg["tex_dynamic_pct"] / 100.0

    def sc(v):  # intensité de la texture : 1 + (v - 1) * k
        return f"{1.0 + (v - 1.0) * k:.2f}"

    texf = "1"
    if k > 0:
        texf = "f$Gen_TexTol"
        f = prof.func("f$Gen_TexTol")
        f.comment("Tolérance de call selon la texture : plus bas sur board humide (les tirages arrivent)")
        for code, v in ((1, 0.88), (2, 0.90), (4, 0.94), (5, 0.97), (6, 1.03), (7, 1.03)):
            f.ret(f"f$Gen_Tex = {code}", sc(v))
        f.others_ret("1")
        if cfg["randomize"]:
            f = prof.func("f$Gen_TexBluff")
            f.comment("Turn/river : crédibilité des bluffs selon le board (flush/quinte/paire complétés = moins de bluffs)")
            f.ret("betround = flop", "1")
            f.ret("nsuitedcommon >= 4", sc(0.5))
            f.ret("nsuitedcommon >= 3", sc(0.7))
            f.ret("f$Gen_TxConnected", sc(0.8))
            f.ret("PairOnBoard", sc(0.9))
            f.ret("f$Gen_Tex >= 6", sc(1.15))
            f.others_ret("1")
    f = prof.func("f$Gen_CallTol")
    f.comment("Tolérance de call globale : type de pot x adversaire x texture")
    opp = "f$Gen_OppTol" if cfg["use_stats"] else "1"
    base = f"{opp} * {texf}" if texf != "1" else opp
    if tol != 1:
        f.ret("f$Gen_PotType >= 2", f"{tol:.2f} * {base}")
    f.others_ret(base)
    f = prof.func("f$Gen_PotOdds")
    f.comment("Cotes du pot ajustées (plus bas = on paye plus large) : sert aux seuils de call postflop")
    f.ret("AmountToCall <= 0", 0)
    f.others_ret("f$Gen_RawOdds / f$Gen_CallTol")
    if cfg["randomize"] and (cfg["use_stats"] or cfg["cbet_3bet_pot_scale"] != 100 or k > 0):
        ps = cfg["cbet_3bet_pot_scale"] / 100.0
        f = prof.func("f$Gen_BluffMult")
        f.comment("Facteur sur les bluffs : type de pot x adversaire")
        opp = "f$Gen_OppBluff" if cfg["use_stats"] else "1"
        if k > 0:
            opp = f"{opp} * f$Gen_TexBluff" if opp != "1" else "f$Gen_TexBluff"
        if ps != 1:
            f.ret("f$Gen_PotType >= 2", f"{ps:.2f} * {opp}")
        f.others_ret(opp)
        f = prof.func("f$Gen_RRBluff")
        f.comment("randomround divisé par le facteur : fréquence effective = fréquence x facteur")
        f.others_ret("randomround / (f$Gen_BluffMult + 0.0001)")
    if cfg["randomize"] and cfg["use_stats"]:
        f = prof.func("f$Gen_RRValue")
        f.others_ret("randomround / (f$Gen_OppValue + 0.0001)")
