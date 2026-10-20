"""Stratégie postflop : catégories de mains réelles (bibliothèque OpenPPL), textures de board,
c-bet / barrels / value fine / bluffs mixtes, défense basée sur les cotes du pot (MDF)."""
from __future__ import annotations

from ..ppl import Profile, fmt
from . import stats
from .common import join, mix_round

CATS = ("Monster", "Strong", "Medium", "StrongDraw", "WeakDraw", "WeakSD", "Air")

# équité approximative de chaque catégorie face à une range qui mise
EQ = {
    "flop": {"Monster": .85, "Strong": .66, "Medium": .45, "WeakSD": .28, "StrongDraw": .42, "WeakDraw": .20, "Air": .04},
    "turn": {"Monster": .86, "Strong": .66, "Medium": .41, "WeakSD": .23, "StrongDraw": .33, "WeakDraw": .12, "Air": .03},
    "river": {"Monster": .88, "Strong": .66, "Medium": .37, "WeakSD": .19, "StrongDraw": .0, "WeakDraw": .0, "Air": .02},
}
KIND = {"Air": "bluff", "WeakDraw": "bluff", "StrongDraw": "bluff", "NutDraw": "bluff",
        "Medium": "value", "WeakSD": "value"}
TEX = {"mono": 1, "wet": 2, "paired": 3, "connected": 4, "twotone": 5, "ace": 6, "broad": 7, "mid": 8, "low": 9}
DRY_TEX = ("ace", "broad", "mid", "low")


def clamp01(x):
    return max(0.0, min(1.0, x))


# ------------------------------------------------------------------------------ helpers de catégories
def emit_helpers(prof: Profile):
    f0 = prof.func("f$Gen_SPR")
    f0.comment("SPR : tapis restant / pot (plus bas = plus engage)")
    f0.ret("PotSize <= 0", 99)
    f0.others_ret("StackSize / PotSize")
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
        "f$Gen_Monster", "HaveTwoPair AND NOT PairOnBoard AND nsuitedcommon < 3", "HaveOverPair",
        "HaveTopPair AND (HaveBestKicker OR HaveSecondBestKicker)"], "Mains fortes")
    boolfunc("f$Gen_Medium", ["HaveTwoPair", "HaveTopPair", "HaveSecondTopPair"],
             "Paires moyennes / top pair kicker faible ; double paire sur board paire ou a 3 cartes de couleur (fragile)")
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
    boolfunc("f$Gen_Blockers", ["nsuitedcommon >= 3 AND HaveNutFlushCard", "nsuitedcommon < 3 AND TopHoleCard = ace"],
             "Blockers utiles au bluff : carte du nut flush sur board a 3 couleurs, sinon As (bloque les meilleures paires)")
    boolfunc("f$Gen_Scare", [
        "(FlushPossibleOnTurn AND NOT FlushPossibleOnFlop)", "(StraightPossibleOnTurn AND NOT StraightPossibleOnFlop)"],
        "La carte du turn complète un tirage (dangereuse pour les bluffs)")
    boolfunc("f$Gen_GoodBarrelCard", ["TurnCardIsOvercardToBoard AND NOT FlushPossibleOnTurn"],
             "Overcard au turn : bonne carte pour le preneur d'initiative")

    f = prof.func("f$Gen_TxConnected")
    f.comment("Board connecté (tirages quinte possibles). Flop : tirages ouverts ; turn/river : quinte possible")
    f.ret("betround = flop AND (OpenEndedStraightDrawPossibleOnFlop OR ThreeCardStraightOnBoard)", "true")
    f.ret("betround = turn AND (StraightPossible OR OneCardStraightPossible OR OpenEndedStraightDrawOnBoard)", "true")
    f.ret("betround = river AND (StraightPossible OR OneCardStraightPossible)", "true")
    f.others_ret("false")

    f = prof.func("f$Gen_Tex")
    f.comment("Texture du board (toutes streets) : 1 monotone/flush, 2 humide, 3 pairé, 4 connecté, 5 deux couleurs, "
              "6 As-haut sec, 7 K/Q-haut sec, 8 moyen sec, 9 bas sec")
    f.ret("nsuitedcommon >= 3", TEX["mono"])
    f.ret("PairOnBoard", TEX["paired"])
    f.ret("nsuitedcommon = 2 AND f$Gen_TxConnected", TEX["wet"])
    f.ret("f$Gen_TxConnected", TEX["connected"])
    f.ret("nsuitedcommon = 2", TEX["twotone"])
    f.ret("BestBoardCard = 14", TEX["ace"])
    f.ret("BestBoardCard >= 12", TEX["broad"])
    f.ret("BestBoardCard >= 8", TEX["mid"])
    f.others_ret(TEX["low"])


def RB(cfg, size) -> str:
    """Action RaiseBy en % du pot ; avec les stats, la taille est modulee par f$Gen_SizeMult."""
    if cfg["use_stats"] and (cfg["exploit_size_fish"], cfg["exploit_size_nit"], cfg["exploit_size_maniac"]) != (100, 100, 100):
        return f"RaiseBy ({fmt(size)} * f$Gen_SizeMult)%"
    return f"RaiseBy {fmt(size)}%"


def _cat_cond(cat):
    return f"f$Gen_{cat}"


def _act(f, cfg, cond, cat, freq, action):
    """Ajoute `WHEN cond AND cat [AND random] action` (ignorée si la fréquence est nulle)."""
    m = mix_round(cfg, freq, KIND.get(cat))
    if m is None:
        return
    f.act(join(cond, _cat_cond(cat), m), action)


# ------------------------------------------------------------------------------ engagement du tapis (SPR bas)
def commit_rules(f, cfg, street: str):
    """Quand le SPR est bas, les mains fortes engagent le tapis ; les mains moyennes paient plus large."""
    spr = cfg["commit_spr"]
    if spr <= 0:
        return
    f.comment(f"Engagement : SPR (tapis / pot) <= {fmt(spr)} -> on met le tapis avec les mains fortes")
    f.act(join(f"f$Gen_SPR <= {fmt(spr)}", "f$Gen_Monster"), "RaiseMax")
    if street != "river":
        # main forte : jamais en multiway ; sur board dangereux (monotone / humide / connecte) seulement a SPR demi
        safe = "NOT f$Gen_Multiway AND f$Gen_Tex != 1 AND f$Gen_Tex != 2 AND f$Gen_Tex != 4"
        f.act(join(f"f$Gen_SPR <= {fmt(spr)}", safe, "f$Gen_Strong"), "RaiseMax")
        f.act(join(f"f$Gen_SPR <= {fmt(spr / 2)}", "NOT f$Gen_Multiway", "f$Gen_Strong"), "RaiseMax")
    else:
        f.act(join(f"f$Gen_SPR <= {fmt(spr)}", "NOT f$Gen_Multiway", "f$Gen_Strong"), "RaiseMax")
    if street != "river":
        low = fmt(spr / 2)
        f.act(join(f"f$Gen_SPR <= {low}", "AmountToCall > 0", "f$Gen_StrongDraw", "f$Gen_PotOdds <= 0.45"), "Call")
    f.act(join(f"f$Gen_SPR <= {fmt(spr / 2)}", "AmountToCall > 0", "f$Gen_Medium", "f$Gen_PotOdds <= 0.40"), "Call")


# ------------------------------------------------------------------------------ règles de mise
def bet_rules(f, cfg, cond, size_pct, freq: dict, nuts_size=None):
    """Écrit les règles de mise par catégorie (ordre de priorité), puis check."""
    act = RB(cfg, size_pct)
    if nuts_size:
        f.act(join(cond, "HaveNuts"), RB(cfg, nuts_size))
    for cat in ("Monster", "Strong", "Medium", "StrongDraw", "WeakDraw", "WeakSD", "Air"):
        fr = freq.get(cat, 0.0)
        _act(f, cfg, cond, cat, fr, act)
    f.act(cond, "Check")


def cbet_freqs(cfg, ip: bool, multiway: bool, adj: int, dry: bool = False):
    agg = cfg["aggression_scale"] / 100.0
    air = clamp01((cfg["cbet_bluff_ip"] if ip else cfg["cbet_bluff_oop"] + 0) / 100.0 + adj / 100.0) * min(1.5, agg)
    med = clamp01((cfg["cbet_medium_ip"] if ip else cfg["cbet_medium_oop"]) / 100.0 + adj / 300.0)
    semi = clamp01(cfg["cbet_semibluff"] / 100.0 + adj / 200.0) * min(1.3, agg)
    slow = cfg["slowplay_pct"] / 100.0 if (dry and not multiway) else 0.0
    fr = {"Monster": 1.0 - slow, "Strong": 1.0, "Medium": med, "StrongDraw": semi, "WeakDraw": clamp01(air * 1.1),
          "WeakSD": clamp01(med * 0.5), "Air": air}
    if multiway:
        s = cfg["cbet_multiway_scale"] / 100.0
        fr.update({"Medium": clamp01(med * 0.65), "StrongDraw": clamp01(semi * (0.5 + s)),
                   "WeakDraw": clamp01(air * s), "WeakSD": clamp01(med * 0.25), "Air": clamp01(air * s)})
    return fr


# ------------------------------------------------------------------------------ défense face à une mise
def facing_rules(f, cfg, street: str, base_cond: str, tighten: float = 1.0, raise_size=None, xr: bool = False,
                 allin: bool = False):
    """Défense par catégorie contre une mise, d'après les cotes du pot.

    xr=True  : nous avons checké et faisons face à une mise -> plan de check-raise (xr_value / xr_bluff).
    allin=True : la mise nous met all-in -> aucune relance possible, seulement call / fold.
    """
    eq = EQ[street]
    scale = (cfg["river_call_scale"] if street == "river" else cfg["call_scale"]) / 100.0 * tighten
    rsize = raise_size or cfg["size_raise_postflop"]
    raise_act = "Call" if allin else RB(cfg, rsize)
    rv = clamp01((cfg["xr_value"] if xr else cfg["raise_vs_bet_value"]) / 100.0)
    rv_strong = rv * (0.25 if xr else 0.35)
    agg = min(1.5, cfg["aggression_scale"] / 100.0)
    xr_b = clamp01(cfg["xr_bluff"] / 100.0 * agg)

    def call_block(cat, thr, extra=""):
        thr = thr * scale
        c1 = join(base_cond, _cat_cond(cat), extra)
        f.act(join(c1, f"f$Gen_PotOdds <= {thr:.3f}"), "Call")
        m = mix_round(cfg, 0.5)
        if m is not None:
            f.act(join(c1, f"f$Gen_PotOdds <= {thr * 1.3:.3f}", m), "Call")

    f.act(join(base_cond, "HaveNuts", "f$Gen_PotOdds < 2"), raise_act)
    if not allin:
        # monstres : relance de value à fréquence rv, sinon call
        m = mix_round(cfg, rv)
        if m is not None:
            f.act(join(base_cond, "f$Gen_Monster", m), raise_act)
    f.act(join(base_cond, "f$Gen_Monster"), "Call")
    if not allin and street != "river":
        m = mix_round(cfg, rv_strong)
        if m is not None:
            f.act(join(base_cond, "f$Gen_Strong", m), raise_act)
    call_block("Strong", eq["Strong"])
    if street != "river":
        if not allin:
            m = mix_round(cfg, xr_b, "bluff")
            if m is not None:
                f.act(join(base_cond, "f$Gen_NutDraw", m), raise_act)
            if xr:  # check-raise : aussi une partie des tirages forts (semi-bluff)
                m = mix_round(cfg, xr_b * 0.5, "bluff")
                if m is not None:
                    f.act(join(base_cond, "f$Gen_StrongDraw", m), raise_act)
        call_block("StrongDraw", eq["StrongDraw"] + 0.05)  # cotes implicites
    call_block("Medium", eq["Medium"])
    call_block("WeakSD", eq["WeakSD"])
    if street == "flop":
        m = mix_round(cfg, clamp01(cfg["float_ip"] / 100.0), "bluff")
        if m is not None:
            f.act(join(base_cond, "f$Gen_WeakDraw", "f$Gen_IP", "f$Gen_PotOdds <= 0.28", m), "Call")
        call_block("WeakDraw", eq["WeakDraw"])
    elif street == "turn":
        call_block("WeakDraw", eq["WeakDraw"])
    if street == "river" and not allin:
        m = mix_round(cfg, clamp01(cfg["river_raise_bluff"] / 100.0 * agg), "bluff")
        if m is not None:
            f.act(join(base_cond, "f$Gen_Air", "f$Gen_Blockers", m), raise_act)
    f.act(base_cond, "Fold")


def facing_groups(f, cfg, street: str, t_raised: float, t_mw: float = 0.85):
    """Toutes les situations où nous faisons face à une mise (ordre = priorité)."""
    f.comment("--- On nous met all-in : call ou fold (pas de relance possible) ---")
    f.group("AmountToCall > 0 AND AmountToCall >= StackSize * 0.9")
    facing_rules(f, cfg, street, "NOT f$Gen_Multiway", allin=True)
    facing_rules(f, cfg, street, "f$Gen_Multiway", tighten=t_mw, allin=True)
    f.comment("--- Nous avons checké et on mise devant nous : plan de check-raise ---")
    f.group("AmountToCall > 0 AND f$Gen_WeChecked")
    facing_rules(f, cfg, street, "NOT f$Gen_Multiway", xr=True)
    facing_rules(f, cfg, street, "f$Gen_Multiway", tighten=t_mw, xr=True)
    f.comment("--- On nous relance après notre mise ---")
    f.group("AmountToCall > 0 AND RaisesSinceLastPlay >= 1 AND BotsActionsOnThisRoundIncludingChecks >= 1")
    facing_rules(f, cfg, street, "", tighten=t_raised)
    f.comment("--- On fait face à une mise (c-bet adverse, donk, probe...) ---")
    f.group("AmountToCall > 0")
    facing_rules(f, cfg, street, "NOT f$Gen_Multiway")
    facing_rules(f, cfg, street, "f$Gen_Multiway", tighten=t_mw)


def lead_rules(f, cfg, street: str, size: float, probe: float, donk: float, tex_adj: dict | None = None,
               draw: float = 0.0):
    """Personne n'a misé et nous n'avons pas l'initiative : IP (heads-up ou multiway) et OOP (lead/donk)."""
    agg = min(1.5, cfg["aggression_scale"] / 100.0)
    probe, donk = clamp01(probe), clamp01(donk)
    ip_freq = {"Monster": 1, "Strong": 1, "Medium": probe * 0.8, "StrongDraw": probe, "WeakDraw": probe * 0.5,
               "WeakSD": probe * 0.3, "Air": probe * 0.45 * agg}
    if tex_adj:  # flop : fréquence et taille de la mise selon la texture
        for tex, code in TEX.items():
            k = clamp01(1.0 + tex_adj[tex][0] / 100.0 * 0.6)
            fr = {c: (v if c in ("Monster", "Strong") else clamp01(v * k)) for c, v in ip_freq.items()}
            bet_rules(f, cfg, join("f$Gen_IP", "NOT f$Gen_Multiway", f"f$Gen_Tex = {code}"), tex_adj[tex][1], fr)
    else:
        bet_rules(f, cfg, join("f$Gen_IP", "NOT f$Gen_Multiway"), size, ip_freq)
    mw_freq = {"Monster": 1, "Strong": 1, "Medium": probe * 0.3, "StrongDraw": probe * 0.5, "WeakDraw": 0.0,
               "WeakSD": 0.0, "Air": 0.0}
    bet_rules(f, cfg, join("f$Gen_IP", "f$Gen_Multiway"), size, mw_freq)
    for cat in ("Monster", "Strong"):
        _act(f, cfg, "NOT f$Gen_IP", cat, donk, RB(cfg, size))
    # OOP sans initiative : semi-bluff lead avec les tirages (heads-up), le reste checke puis check-raise / call
    draw = clamp01(draw * min(1.3, agg))
    nm = join("NOT f$Gen_IP", "NOT f$Gen_Multiway")
    _act(f, cfg, nm, "StrongDraw", draw, RB(cfg, size))
    _act(f, cfg, nm, "WeakDraw", draw * 0.3, RB(cfg, size))


# ------------------------------------------------------------------------------ rues
def generate(prof: Profile, cfg: dict):
    stats.emit_postflop(prof, cfg)
    emit_helpers(prof)
    _flop(prof, cfg)
    _turn(prof, cfg)
    _river(prof, cfg)


def _flop(prof, cfg):
    f = prof.func("f$flop")
    f.comment("OHPG : flop. Blocs : c-bet (agresseur préflop), mise du non-agresseur, relance subie, mise subie.")
    commit_rules(f, cfg, "flop")
    adjs = {"mono": cfg["cbet_mono_adj"], "wet": cfg["cbet_wet_adj"], "paired": cfg["cbet_paired_adj"],
            "connected": cfg["cbet_connected_adj"], "twotone": cfg["cbet_twotone_adj"], "ace": cfg["cbet_dry_adj"],
            "broad": cfg["cbet_high_adj"], "mid": cfg["cbet_mid_adj"], "low": cfg["cbet_low_adj"]}
    sizes = {"mono": cfg["size_cbet_mono"], "wet": cfg["size_cbet_wet"], "paired": cfg["size_cbet_paired"],
             "connected": cfg["size_cbet_wet"], "twotone": (cfg["size_cbet_dry"] + cfg["size_cbet_wet"]) // 2,
             "ace": cfg["size_cbet_dry"], "broad": cfg["size_cbet_dry"], "mid": cfg["size_cbet_dry"],
             "low": cfg["size_cbet_dry"]}

    f.comment("--- C-BET : nous avons relancé préflop et personne n'a misé ---")
    f.group("AmountToCall = 0 AND BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0")
    for big_pot in (False, True):  # pot 3bet+ : mises plus petites, bluffs réduits via f$Gen_RRBluff
        pcond = "f$Gen_PotType >= 2" if big_pot else "f$Gen_PotType = 1"
        for mw in (False, True):
            for ip in (True, False):
                for tex, code in TEX.items():
                    cond = join(pcond, "f$Gen_Multiway" if mw else "NOT f$Gen_Multiway", "f$Gen_IP" if ip else "NOT f$Gen_IP",
                                f"f$Gen_Tex = {code}")
                    size = cfg["size_cbet_multiway"] if mw else sizes[tex]
                    if big_pot:
                        size = min(size, cfg["size_cbet_3bet"])
                    dry = tex in DRY_TEX
                    bet_rules(f, cfg, cond, size, cbet_freqs(cfg, ip, mw, adjs[tex], dry))
    f.others("Check")

    f.comment("--- Nous n'avons pas relancé préflop et personne n'a misé ---")
    f.group("AmountToCall = 0")
    tex_adj = {t: (adjs[t], min(150, sizes[t] + 10)) for t in TEX}
    lead_rules(f, cfg, "flop", cfg["size_cbet_dry"] + 10, cfg["probe_freq"] / 100.0, cfg["donk_freq"] / 100.0, tex_adj,
              draw=cfg["donk_semibluff"] / 100.0)
    f.others("Check")

    facing_groups(f, cfg, "flop", 0.8)


def _turn(prof, cfg):
    f = prof.func("f$turn")
    f.comment("OHPG : turn. Blocs : 2e barrel, c-bet retardé / probe, mise, relance subie, mise subie.")
    commit_rules(f, cfg, "turn")
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
    lead_rules(f, cfg, "turn", cfg["size_turn"], cfg["turn_probe"] / 100.0, 0.8, draw=cfg["donk_semibluff"] / 100.0 * 0.7)
    f.others("Check")

    facing_groups(f, cfg, "turn", 0.75)


def _river(prof, cfg):
    f = prof.func("f$river")
    f.comment("OHPG : river. Value fine, bluffs avec blockers, probe, défense par cotes (MDF).")
    commit_rules(f, cfg, "river")
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
        f.act(join(mwc, "HaveNuts", "f$Gen_IP"), RB(cfg, cfg['size_river_nuts']))
        f.act(join(mwc, "f$Gen_Monster"), RB(cfg, size))
        f.act(join(mwc, "f$Gen_Strong"), RB(cfg, size))
        _act(f, cfg, mwc, "Medium", thin * k * (1.0 if True else 0), RB(cfg, cfg['size_thin']))
        _act(f, cfg, join(mwc, "f$Gen_Blockers"), "Air", clamp01((bluff + bonus) * agg) * k, RB(cfg, size))
        _act(f, cfg, mwc, "Air", clamp01(bluff * agg) * k, RB(cfg, size))
        f.act(mwc, "Check")
    f.others("Check")

    f.comment("--- Sans mise devant nous : value / probe / bluff ---")
    f.group("AmountToCall = 0")
    for ip in (True, False):
        ipc = join("f$Gen_IP" if ip else "NOT f$Gen_IP", "NOT f$Gen_Multiway")
        if ip:
            f.act(join(ipc, "HaveNuts"), RB(cfg, cfg['size_river_nuts']))
        f.act(join(ipc, "f$Gen_Monster"), RB(cfg, size))
        f.act(join(ipc, "f$Gen_Strong"), RB(cfg, size))
        _act(f, cfg, ipc, "Medium", thin * (0.9 if ip else 0.35) * probe, RB(cfg, cfg['size_thin']))
        _act(f, cfg, join(ipc, "f$Gen_Blockers"), "Air", clamp01((bluff + bonus) * 0.6 * agg * (probe + 0.3)), RB(cfg, size))
        _act(f, cfg, ipc, "Air", clamp01(bluff * 0.4 * agg * (probe + 0.3)), RB(cfg, size))
        f.act(ipc, "Check")
    mwc = "f$Gen_Multiway"
    f.act(join(mwc, "f$Gen_Monster"), RB(cfg, size))
    f.act(join(mwc, "f$Gen_Strong"), RB(cfg, size))
    _act(f, cfg, join(mwc, "f$Gen_IP"), "Medium", thin * 0.3 * probe, RB(cfg, cfg['size_thin']))
    f.act(mwc, "Check")
    f.others("Check")

    facing_groups(f, cfg, "river", 0.8)
