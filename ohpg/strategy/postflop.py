"""Stratégie postflop : catégories de mains réelles (bibliothèque OpenPPL), textures de board,
c-bet / barrels / value fine / bluffs mixtes, défense basée sur les cotes du pot (MDF)."""
from __future__ import annotations

from ..ppl import Profile, fmt
from .common import join, mix_round

CATS = ("Monster", "Strong", "Medium", "StrongDraw", "WeakDraw", "WeakSD", "Air")

# équité approximative de chaque catégorie face à une range qui mise
EQ = {
    "flop": {"Monster": .85, "Strong": .66, "Medium": .45, "WeakSD": .28, "StrongDraw": .42, "WeakDraw": .20, "Air": .04},
    "turn": {"Monster": .86, "Strong": .66, "Medium": .41, "WeakSD": .23, "StrongDraw": .33, "WeakDraw": .12, "Air": .03},
    "river": {"Monster": .88, "Strong": .66, "Medium": .37, "WeakSD": .19, "StrongDraw": .0, "WeakDraw": .0, "Air": .02},
}
TEX = {"mono": 1, "wet": 2, "paired": 3, "high": 4, "low": 5, "dry": 6}


def clamp01(x):
    return max(0.0, min(1.0, x))


# ------------------------------------------------------------------------------ helpers de catégories
def emit_helpers(prof: Profile):
    def boolfunc(name, rules, comment=None):
        f = prof.func(name)
        if comment:
            f.comment(comment)
        for cond in rules:
            f.ret(cond, "true")
        f.others_ret("false")

    boolfunc("f$Gen_Monster", [
        "HaveStraightFlush", "HaveQuads AND NOT QuadsOnBoard", "HaveFullHouse AND NOT FullHouseOnBoard",
        "HaveFlush AND NOT FlushOnBoard", "HaveStraight AND NOT StraightOnBoard", "HaveSet",
        "HaveTrips AND NOT TripsOnBoard"], "Mains monstrueuses (value maximale)")
    boolfunc("f$Gen_Strong", [
        "f$Gen_Monster", "HaveTwoPair", "HaveOverPair",
        "HaveTopPair AND (HaveBestKicker OR HaveSecondBestKicker)"], "Mains fortes")
    boolfunc("f$Gen_Medium", ["HaveTopPair", "HaveSecondTopPair"], "Paires moyennes / top pair kicker faible")
    boolfunc("f$Gen_WeakSD", ["HavePair"], "Petites paires (valeur de showdown)")
    boolfunc("f$Gen_StrongDraw", [
        "(betround < river) AND (HaveFlushDraw OR HaveOpenEndedStraightDraw OR HaveDoubleGutshotDraw)"],
        "Tirages forts (flop/turn)")
    boolfunc("f$Gen_NutDraw", [
        "(betround < river) AND (HaveNutFlushDraw OR HaveNutStraightDraw OR (HaveFlushDraw AND HaveStraightDraw))"],
        "Tirages nuts / combos : candidats au check-raise et au jam")
    boolfunc("f$Gen_WeakDraw", [
        "(betround < river) AND (HaveInsideStraightDraw OR HaveBackdoorFlushDraw OR Overcards = 2)"],
        "Tirages faibles, backdoors, overcards")
    f = prof.func("f$Gen_Air")
    f.comment("Rien : ni main faite ni tirage (exclusif avec les autres catégories)")
    f.ret("f$Gen_Strong OR f$Gen_Medium OR f$Gen_WeakSD OR f$Gen_StrongDraw OR f$Gen_WeakDraw", "false")
    f.others_ret("true")
    boolfunc("f$Gen_Blockers", ["HaveNutFlushCard", "TopHoleCard = ace"], "Blockers des nuts (bonus de bluff river)")
    boolfunc("f$Gen_Scare", [
        "(FlushPossibleOnTurn AND NOT FlushPossibleOnFlop)", "(StraightPossibleOnTurn AND NOT StraightPossibleOnFlop)"],
        "La carte du turn complète un tirage (dangereuse pour les bluffs)")
    boolfunc("f$Gen_GoodBarrelCard", ["TurnCardIsOvercardToBoard AND NOT FlushPossibleOnTurn"],
             "Overcard au turn : bonne carte pour le preneur d'initiative")

    f = prof.func("f$Gen_Tex")
    f.comment("Texture du flop : 1 monotone, 2 humide, 3 pairé, 4 haut sec, 5 bas sec, 6 sec")
    f.ret("nsuitedcommon >= 3", TEX["mono"])
    f.ret("(nsuitedcommon = 2 AND (StraightPossible OR OpenEndedStraightDrawPossibleOnFlop)) OR OpenEndedStraightDrawPossibleOnFlop OR ThreeCardStraightOnBoard", TEX["wet"])
    f.ret("PairOnBoard", TEX["paired"])
    f.ret("BestBoardCard >= 13", TEX["high"])
    f.ret("BestBoardCard <= 9", TEX["low"])
    f.others_ret(TEX["dry"])


def _cat_cond(cat):
    return f"f$Gen_{cat}"


def _act(f, cfg, cond, cat, freq, action):
    """Ajoute `WHEN cond AND cat [AND random] action` (ignorée si la fréquence est nulle)."""
    m = mix_round(cfg, freq)
    if m is None:
        return
    f.act(join(cond, _cat_cond(cat), m), action)


# ------------------------------------------------------------------------------ règles de mise
def bet_rules(f, cfg, cond, size_pct, freq: dict, nuts_size=None):
    """Écrit les règles de mise par catégorie (ordre de priorité), puis check."""
    act = f"RaiseBy {fmt(size_pct)}%"
    if nuts_size:
        f.act(join(cond, "HaveNuts"), f"RaiseBy {fmt(nuts_size)}%")
    for cat in ("Monster", "Strong", "Medium", "StrongDraw", "WeakDraw", "WeakSD", "Air"):
        fr = freq.get(cat, 0.0)
        _act(f, cfg, cond, cat, fr, act)
    f.act(cond, "Check")


def cbet_freqs(cfg, ip: bool, multiway: bool, adj: int):
    agg = cfg["aggression_scale"] / 100.0
    air = clamp01((cfg["cbet_bluff_ip"] if ip else cfg["cbet_bluff_oop"] + 0) / 100.0 + adj / 100.0) * min(1.5, agg)
    med = clamp01((cfg["cbet_medium_ip"] if ip else cfg["cbet_medium_oop"]) / 100.0 + adj / 300.0)
    semi = clamp01(cfg["cbet_semibluff"] / 100.0 + adj / 200.0) * min(1.3, agg)
    fr = {"Monster": 1.0, "Strong": 1.0, "Medium": med, "StrongDraw": semi, "WeakDraw": clamp01(air * 1.1),
          "WeakSD": clamp01(med * 0.5), "Air": air}
    if multiway:
        s = cfg["cbet_multiway_scale"] / 100.0
        fr.update({"Medium": clamp01(med * 0.65), "StrongDraw": clamp01(semi * (0.5 + s)),
                   "WeakDraw": clamp01(air * s), "WeakSD": clamp01(med * 0.25), "Air": clamp01(air * s)})
    return fr


# ------------------------------------------------------------------------------ défense face à une mise
def facing_rules(f, cfg, street: str, base_cond: str, tighten: float = 1.0, raise_size=None):
    """Défense par catégorie contre une mise, d'après les cotes du pot."""
    eq = EQ[street]
    scale = (cfg["river_call_scale"] if street == "river" else cfg["call_scale"]) / 100.0 * tighten
    rsize = raise_size or cfg["size_raise_postflop"]
    raise_act = f"RaiseBy {fmt(rsize)}%"
    rv = clamp01(cfg["raise_vs_bet_value"] / 100.0)
    agg = min(1.5, cfg["aggression_scale"] / 100.0)

    def call_block(cat, thr, extra=""):
        thr = thr * scale
        c1 = join(base_cond, _cat_cond(cat), extra)
        f.act(join(c1, f"f$Gen_PotOdds <= {thr:.3f}"), "Call")
        m = mix_round(cfg, 0.5)
        if m is not None:
            f.act(join(c1, f"f$Gen_PotOdds <= {thr * 1.3:.3f}", m), "Call")

    f.act(join(base_cond, "HaveNuts", "f$Gen_PotOdds < 2"), raise_act)
    # monstres : relance de value à fréquence rv, sinon call
    m = mix_round(cfg, rv)
    if m is not None:
        f.act(join(base_cond, "f$Gen_Monster", m), raise_act)
    f.act(join(base_cond, "f$Gen_Monster"), "Call")
    m = mix_round(cfg, rv * 0.35)
    if m is not None and street != "river":
        f.act(join(base_cond, "f$Gen_Strong", m), raise_act)
    call_block("Strong", eq["Strong"])
    if street != "river":
        m = mix_round(cfg, clamp01(cfg["xr_bluff"] / 100.0 * agg))
        if m is not None:
            f.act(join(base_cond, "f$Gen_NutDraw", m), raise_act)
        call_block("StrongDraw", eq["StrongDraw"] + 0.05)  # cotes implicites
    call_block("Medium", eq["Medium"])
    call_block("WeakSD", eq["WeakSD"])
    if street == "flop":
        m = mix_round(cfg, clamp01(cfg["float_ip"] / 100.0))
        if m is not None:
            f.act(join(base_cond, "f$Gen_WeakDraw", "f$Gen_IP", "f$Gen_PotOdds <= 0.28", m), "Call")
        call_block("WeakDraw", eq["WeakDraw"])
    elif street == "turn":
        call_block("WeakDraw", eq["WeakDraw"])
    if street == "river":
        m = mix_round(cfg, clamp01(cfg["river_raise_bluff"] / 100.0 * agg))
        if m is not None:
            f.act(join(base_cond, "f$Gen_Air", "f$Gen_Blockers", m), raise_act)
    f.act(base_cond, "Fold")


# ------------------------------------------------------------------------------ rues
def generate(prof: Profile, cfg: dict):
    emit_helpers(prof)
    _flop(prof, cfg)
    _turn(prof, cfg)
    _river(prof, cfg)


def _flop(prof, cfg):
    f = prof.func("f$flop")
    f.comment("OHPG : flop. Blocs : c-bet (agresseur préflop), mise du non-agresseur, relance subie, mise subie.")
    adjs = {"mono": cfg["cbet_mono_adj"], "wet": cfg["cbet_wet_adj"], "paired": cfg["cbet_paired_adj"],
            "high": cfg["cbet_high_adj"], "low": cfg["cbet_low_adj"], "dry": cfg["cbet_dry_adj"]}
    sizes = {"mono": cfg["size_cbet_mono"], "wet": cfg["size_cbet_wet"], "paired": cfg["size_cbet_paired"],
             "high": cfg["size_cbet_dry"], "low": cfg["size_cbet_dry"], "dry": cfg["size_cbet_dry"]}

    f.comment("--- C-BET : nous avons relancé préflop et personne n'a misé ---")
    f.group("AmountToCall = 0 AND BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0")
    for mw in (False, True):
        for ip in (True, False):
            for tex, code in TEX.items():
                cond = join("f$Gen_Multiway" if mw else "NOT f$Gen_Multiway", "f$Gen_IP" if ip else "NOT f$Gen_IP", f"f$Gen_Tex = {code}")
                size = cfg["size_cbet_multiway"] if mw else sizes[tex]
                bet_rules(f, cfg, cond, size, cbet_freqs(cfg, ip, mw, adjs[tex]))
    f.others("Check")

    f.comment("--- Nous n'avons pas relancé préflop et personne n'a misé ---")
    f.group("AmountToCall = 0")
    probe = clamp01(cfg["probe_freq"] / 100.0)
    donk = clamp01(cfg["donk_freq"] / 100.0)
    ip_freq = {"Monster": 1, "Strong": 1, "Medium": probe * 0.8, "StrongDraw": probe, "WeakDraw": probe * 0.5,
               "WeakSD": probe * 0.3, "Air": probe * 0.45 * min(1.5, cfg["aggression_scale"] / 100.0)}
    bet_rules(f, cfg, join("f$Gen_IP", "NOT f$Gen_Multiway"), cfg["size_cbet_dry"] + 10, ip_freq)
    for cat in ("Monster", "Strong"):
        _act(f, cfg, "NOT f$Gen_IP", cat, donk, f"RaiseBy {fmt(cfg['size_cbet_wet'])}%")
    f.others("Check")

    f.comment("--- On nous relance après notre mise / check-raise subi ---")
    f.group("AmountToCall > 0 AND RaisesSinceLastPlay >= 1 AND BotsActionsOnThisRoundIncludingChecks >= 1")
    facing_rules(f, cfg, "flop", "", tighten=0.8)

    f.comment("--- On fait face à une mise (c-bet adverse, donk, etc.) ---")
    f.group("AmountToCall > 0")
    facing_rules(f, cfg, "flop", "NOT f$Gen_Multiway")
    facing_rules(f, cfg, "flop", "f$Gen_Multiway", tighten=0.85)


def _turn(prof, cfg):
    f = prof.func("f$turn")
    f.comment("OHPG : turn. Blocs : 2e barrel, c-bet retardé / probe, mise, relance subie, mise subie.")
    agg = min(1.5, cfg["aggression_scale"] / 100.0)
    adj = cfg["barrel_scare_adj"]
    size = cfg["size_turn"]

    f.comment("--- 2e BARREL : nous avons misé au flop ---")
    f.group("AmountToCall = 0 AND BotRaisedOnFlop")
    for mw in (False, True):
        for ip in (True, False):
            for card in ("scare", "good", "neutral"):
                delta = adj / 100.0 if card == "scare" else 0.10 if card == "good" else 0.0
                air = clamp01(cfg["barrel_bluff"] / 100.0 + delta) * agg
                med = clamp01(cfg["barrel_medium_ip"] / 100.0 * (1.0 if ip else 0.6))
                semi = clamp01(cfg["barrel_semibluff"] / 100.0 + delta / 2) * min(1.3, agg)
                fr = {"Monster": cfg["barrel_value"] / 100.0, "Strong": cfg["barrel_value"] / 100.0, "Medium": med,
                      "StrongDraw": semi, "WeakDraw": air * 0.8, "WeakSD": med * 0.3, "Air": air}
                if mw:
                    fr.update({"Medium": med * 0.5, "StrongDraw": semi * 0.6, "WeakDraw": air * 0.3, "WeakSD": 0.0, "Air": air * 0.25})
                ccond = {"scare": "f$Gen_Scare", "good": "NOT f$Gen_Scare AND f$Gen_GoodBarrelCard",
                         "neutral": "NOT f$Gen_Scare AND NOT f$Gen_GoodBarrelCard"}[card]
                cond = join("f$Gen_Multiway" if mw else "NOT f$Gen_Multiway", "f$Gen_IP" if ip else "NOT f$Gen_IP", ccond)
                bet_rules(f, cfg, cond, size, fr)
    f.others("Check")

    f.comment("--- Flop checké : c-bet retardé (agresseur) ou probe ---")
    f.group("AmountToCall = 0 AND NoBettingOnFlop")
    dl = clamp01(cfg["delayed_cbet"] / 100.0)
    pr = clamp01(cfg["turn_probe"] / 100.0)
    for pfr in (True, False):
        fq = dl if pfr else pr
        fr = {"Monster": 1, "Strong": 1, "Medium": fq, "StrongDraw": fq, "WeakDraw": fq * 0.6, "WeakSD": fq * 0.3,
              "Air": fq * 0.5 * agg}
        bet_rules(f, cfg, join("BotRaisedBeforeFlop" if pfr else "NOT BotRaisedBeforeFlop", "NOT f$Gen_Multiway"), size, fr)
    f.others("Check")

    f.comment("--- Autres situations sans mise devant nous ---")
    f.group("AmountToCall = 0")
    pr2 = clamp01(cfg["turn_probe"] / 100.0)
    fr = {"Monster": 1, "Strong": 1, "Medium": pr2 * 0.7, "StrongDraw": pr2 * 0.8, "WeakDraw": pr2 * 0.3,
          "WeakSD": 0.0, "Air": pr2 * 0.3 * agg}
    bet_rules(f, cfg, join("f$Gen_IP", "NOT f$Gen_Multiway"), cfg["size_turn"], fr)
    for cat in ("Monster", "Strong"):
        _act(f, cfg, "NOT f$Gen_IP", cat, 0.8, f"RaiseBy {fmt(cfg['size_turn'])}%")
    f.others("Check")

    f.comment("--- On nous relance après notre mise ---")
    f.group("AmountToCall > 0 AND RaisesSinceLastPlay >= 1 AND BotsActionsOnThisRoundIncludingChecks >= 1")
    facing_rules(f, cfg, "turn", "", tighten=0.75)
    f.comment("--- On fait face à une mise ---")
    f.group("AmountToCall > 0")
    facing_rules(f, cfg, "turn", "NOT f$Gen_Multiway")
    facing_rules(f, cfg, "turn", "f$Gen_Multiway", tighten=0.85)


def _river(prof, cfg):
    f = prof.func("f$river")
    f.comment("OHPG : river. Value fine, bluffs avec blockers, probe, défense par cotes (MDF).")
    agg = min(1.5, cfg["aggression_scale"] / 100.0)
    size = cfg["size_river"]
    bluff = cfg["river_bluff"] / 100.0
    bonus = cfg["river_bluff_blockers"] / 100.0
    thin = clamp01(cfg["river_value_thin"] / 100.0)
    probe = clamp01(cfg["river_probe"] / 100.0)

    f.comment("--- 3e BARREL : nous avons misé au turn ---")
    f.group("AmountToCall = 0 AND BotRaisedOnTurn")
    for mw in (False, True):
        mwc = "f$Gen_Multiway" if mw else "NOT f$Gen_Multiway"
        k = 0.4 if mw else 1.0
        f.act(join(mwc, "HaveNuts", "f$Gen_IP"), f"RaiseBy {fmt(cfg['size_river_nuts'])}%")
        f.act(join(mwc, "f$Gen_Monster"), f"RaiseBy {fmt(size)}%")
        f.act(join(mwc, "f$Gen_Strong"), f"RaiseBy {fmt(size)}%")
        _act(f, cfg, mwc, "Medium", thin * k * (1.0 if True else 0), f"RaiseBy {fmt(cfg['size_thin'])}%")
        _act(f, cfg, join(mwc, "f$Gen_Blockers"), "Air", clamp01((bluff + bonus) * agg) * k, f"RaiseBy {fmt(size)}%")
        _act(f, cfg, mwc, "Air", clamp01(bluff * agg) * k, f"RaiseBy {fmt(size)}%")
        f.act(mwc, "Check")
    f.others("Check")

    f.comment("--- Sans mise devant nous : value / probe / bluff ---")
    f.group("AmountToCall = 0")
    for ip in (True, False):
        ipc = join("f$Gen_IP" if ip else "NOT f$Gen_IP", "NOT f$Gen_Multiway")
        if ip:
            f.act(join(ipc, "HaveNuts"), f"RaiseBy {fmt(cfg['size_river_nuts'])}%")
        f.act(join(ipc, "f$Gen_Monster"), f"RaiseBy {fmt(size)}%")
        f.act(join(ipc, "f$Gen_Strong"), f"RaiseBy {fmt(size)}%")
        _act(f, cfg, ipc, "Medium", thin * (0.9 if ip else 0.35) * probe, f"RaiseBy {fmt(cfg['size_thin'])}%")
        _act(f, cfg, join(ipc, "f$Gen_Blockers"), "Air", clamp01((bluff + bonus) * 0.6 * agg * (probe + 0.3)), f"RaiseBy {fmt(size)}%")
        _act(f, cfg, ipc, "Air", clamp01(bluff * 0.4 * agg * (probe + 0.3)), f"RaiseBy {fmt(size)}%")
        f.act(ipc, "Check")
    f.others("Check")

    f.comment("--- On nous relance ---")
    f.group("AmountToCall > 0 AND RaisesSinceLastPlay >= 1 AND BotsActionsOnThisRoundIncludingChecks >= 1")
    facing_rules(f, cfg, "river", "", tighten=0.8)
    f.comment("--- On fait face à une mise ---")
    f.group("AmountToCall > 0")
    facing_rules(f, cfg, "river", "NOT f$Gen_Multiway")
    facing_rules(f, cfg, "river", "f$Gen_Multiway", tighten=0.85)
