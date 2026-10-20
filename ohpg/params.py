"""Schéma unique de tous les paramètres : sert à la CLI, aux presets, à la validation et à la GUI."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class P:
    key: str
    label: str
    group: str
    kind: str  # pct | int | float | bool | choice
    default: Any
    lo: float = 0
    hi: float = 100
    step: float = 1
    choices: tuple = field(default_factory=tuple)
    help: str = ""


G_GEN = "Général"
G_OPEN = "Preflop · Ouverture"
G_DEF = "Preflop · Défense / 3bet"
G_BIG = "Preflop · 4bet / 5bet / squeeze"
G_SHORT = "Push/Fold"
G_FLOP = "Flop"
G_TURN = "Turn"
G_RIVER = "River"
G_SIZE = "Tailles de mise"
G_HOP = "Gestion de table"
G_STATS = "Stats adversaires"

SCHEMA: list[P] = [
    # ------------------------------------------------------------------ général
    P("name", "Nom du profil", G_GEN, "str", "OHPG Profile"),
    P("game", "Type de jeu", G_GEN, "choice", "cash", choices=("cash", "tournament"),
      help="tournament active le push/fold et l'ajustement ICM"),
    P("table_size", "Joueurs à table", G_GEN, "int", 6, 2, 10, 1, help="2 = heads-up, 6 = 6-max, 9 = full ring"),
    P("ante_bb", "Ante (en BB)", G_GEN, "float", 0.0, 0, 0.5, 0.01, help="élargit les ranges de push/ouverture"),
    P("range_scale", "Échelle des ranges (%)", G_GEN, "int", 100, 40, 160, 1, help="multiplie toutes les ranges d'ouverture"),
    P("aggression_scale", "Agressivité globale (%)", G_GEN, "int", 100, 20, 200, 1,
      help="multiplie les fréquences de bluff et de relance"),
    P("randomize", "Stratégie mixte (aléatoire)", G_GEN, "bool", True,
      help="mélange les actions limites avec randomhand/randomround au lieu d'être déterministe"),
    # ------------------------------------------------------------------ ouverture
    P("open_ep", "Ouverture UTG/EP (% mains)", G_OPEN, "pct", 14, 0, 60),
    P("open_mp", "Ouverture MP/HJ (%)", G_OPEN, "pct", 19, 0, 70),
    P("open_co", "Ouverture CO (%)", G_OPEN, "pct", 27, 0, 80),
    P("open_btn", "Ouverture BTN (%)", G_OPEN, "pct", 45, 0, 100),
    P("open_sb", "Ouverture SB (%)", G_OPEN, "pct", 42, 0, 100),
    P("open_size_ep", "Taille ouverture EP/MP (x BB)", G_OPEN, "float", 2.5, 2, 5, 0.1),
    P("open_size_late", "Taille ouverture CO/BTN (x BB)", G_OPEN, "float", 2.3, 2, 5, 0.1),
    P("open_size_sb", "Taille ouverture SB (x BB)", G_OPEN, "float", 3.0, 2, 5, 0.1),
    P("sb_limp_pct", "SB : part de la range complétée (%)", G_OPEN, "pct", 0, 0, 100,
      help="mains ouvertes en limp au lieu d'un raise (SB)"),
    P("bb_iso_vs_sblimp", "BB : relance vs limp du SB (% mains)", G_OPEN, "pct", 40, 0, 100,
      help="3-max / heads-up : le SB complete, le BB relance cette part de range (sinon check)"),
    P("size_iso_sblimp", "BB : taille de la relance vs limp du SB (BB)", G_OPEN, "float", 3.0, 2, 6, 0.1),
    P("iso_raise_pct", "Isolation des limpers (% mains)", G_OPEN, "pct", 14, 0, 60),
    P("iso_size", "Taille d'isolation (x BB + 1/limper)", G_OPEN, "float", 3.5, 2, 8, 0.1),
    P("overlimp_pct", "Overlimp derrière limpers (% mains)", G_OPEN, "pct", 0, 0, 60),
    # ------------------------------------------------------------------ défense / 3bet
    P("threebet_value", "3bet value (% mains vs CO)", G_DEF, "pct", 3.5, 0, 20, 0.1),
    P("threebet_bluff_ratio", "Ratio bluffs/value 3bet", G_DEF, "float", 0.6, 0, 2, 0.05),
    P("call_ip_pct", "Cold-call IP (% mains vs CO)", G_DEF, "pct", 8, 0, 40, 0.5),
    P("call_sb_pct", "SB : flat vs ouverture (%)", G_DEF, "pct", 3, 0, 30, 0.5),
    P("bb_defend_pct", "BB : défense vs BTN (% mains)", G_DEF, "pct", 36, 0, 100),
    P("bb_threebet_scale", "BB : part de 3bet dans la défense (%)", G_DEF, "pct", 12, 0, 60),
    P("threebet_size_ip", "Taille 3bet IP (x ouverture)", G_DEF, "float", 3.0, 2, 6, 0.1),
    P("threebet_size_oop", "Taille 3bet OOP (x ouverture)", G_DEF, "float", 4.0, 2, 8, 0.1),
    P("threebet_shove_stack", "3bet all-in sous (BB)", G_DEF, "int", 20, 0, 60, 1),
    # ------------------------------------------------------------------ 4bet etc.
    P("fourbet_value", "4bet value (% mains)", G_BIG, "pct", 1.8, 0, 10, 0.1),
    P("fourbet_bluff_ratio", "Ratio bluffs/value 4bet", G_BIG, "float", 0.5, 0, 2, 0.05),
    P("call_3bet_ip", "Continuer vs 3bet IP (% de sa range)", G_BIG, "pct", 38, 0, 80),
    P("call_3bet_oop", "Continuer vs 3bet OOP (% de sa range)", G_BIG, "pct", 28, 0, 80),
    P("fourbet_size_ip", "Taille 4bet IP (x 3bet)", G_BIG, "float", 2.2, 1.8, 4, 0.1),
    P("fourbet_size_oop", "Taille 4bet OOP (x 3bet)", G_BIG, "float", 2.5, 1.8, 4, 0.1),
    P("fourbet_shove_stack", "4bet all-in sous (BB)", G_BIG, "int", 30, 0, 100, 1),
    P("fivebet_value", "5bet all-in value (%)", G_BIG, "pct", 1.2, 0, 8, 0.1),
    P("fivebet_bluff", "5bet bluff (A5s…, %)", G_BIG, "pct", 0.4, 0, 3, 0.1),
    P("call_4bet_pct", "Call vs 4bet (%)", G_BIG, "pct", 2.5, 0, 12, 0.1),
    P("call_allin_pct", "Call d'un all-in préflop 100BB (%)", G_BIG, "pct", 3.0, 0, 20, 0.1),
    P("squeeze_value", "Squeeze value (%)", G_BIG, "pct", 3.2, 0, 15, 0.1),
    P("squeeze_bluff_ratio", "Ratio bluffs/value squeeze", G_BIG, "float", 0.6, 0, 2, 0.05),
    P("squeeze_size", "Taille squeeze (x ouverture + 1/caller)", G_BIG, "float", 3.8, 2.5, 8, 0.1),
    P("coldcall_squeeze_pct", "Call multiway derrière un call (%)", G_BIG, "pct", 5, 0, 30, 0.5),
    # ------------------------------------------------------------------ push/fold
    P("pf_max_stack", "Push/fold sous (BB, 0 = off)", G_SHORT, "int", 0, 0, 30, 1),
    P("openjam_max", "Zone open-jam : tapis premium jusqu'a (BB, 0 = off)", G_SHORT, "int", 0, 0, 40, 1,
      help="au-dessus du push/fold : les mains premium ouvrent all-in (premiere action) jusqu'a cette profondeur"),
    P("openjam_pct", "Zone open-jam : range de tapis (% mains, BTN)", G_SHORT, "pct", 6, 1, 25, 0.5),
    P("icm_postflop", "ICM postflop a la bulle (0-100)", G_SHORT, "int", 0, 0, 100, 1,
      help="a la bulle (IsBubble) : moins de calls marginaux et moins de bluffs apres le flop"),
    P("pf_scale", "Échelle des ranges de push (%)", G_SHORT, "int", 100, 50, 150, 1),
    P("pf_call_scale", "Échelle des calls de push (%)", G_SHORT, "int", 100, 40, 160, 1),
    P("reshove_stack", "Reshove vs ouverture sous (BB)", G_SHORT, "int", 22, 0, 40, 1),
    P("payout", "Structure des gains (module l'ICM)", G_SHORT, "choice", "standard",
      choices=("standard", "top2", "wta"),
      help="standard = plusieurs places payees (ICM plein) ; top2 = deux payes (ICM x0.6) ; "
           "wta = le gagnant prend tout (Spin & Go : chip EV, ICM desactive)"),
    P("icm_pressure", "Pression ICM (0-100)", G_SHORT, "int", 0, 0, 100, 1,
      help="resserre les calls de push à la bulle (IsBubble)"),
    # ------------------------------------------------------------------ flop
    P("cbet_bluff_ip", "C-bet bluff IP (% des mains vides)", G_FLOP, "pct", 55, 0, 100),
    P("cbet_bluff_oop", "C-bet bluff OOP (%)", G_FLOP, "pct", 35, 0, 100),
    P("commit_spr", "SPR d'engagement du tapis (0 = off)", G_FLOP, "float", 2.5, 0, 10, 0.5,
      help="SPR = tapis / pot. En dessous, Monster/Strong mettent le tapis (valable flop, turn, river)"),
    P("slowplay_pct", "Slowplay des monstres, board sec heads-up (%)", G_FLOP, "pct", 10, 0, 60,
      help="% de fois où un monstre check au lieu de miser (piège)"),
    P("cbet_3bet_pot_scale", "Pots 3bet+ : facteur sur les bluffs (%)", G_FLOP, "pct", 80, 20, 150,
      help="agit sur tous les bluffs/semi-bluffs postflop quand le pot préflop est 3bet ou plus"),
    P("call_3bet_pot_scale", "Pots 3bet+ : tolérance de call (%)", G_FLOP, "int", 110, 60, 160, 1,
      help="engagement plus large dans les pots 3bet/4bet"),
    P("cbet_semibluff", "Semi-bluff des tirages (%)", G_FLOP, "pct", 85, 0, 100),
    P("cbet_medium_ip", "C-bet des mains moyennes IP (%)", G_FLOP, "pct", 55, 0, 100),
    P("cbet_medium_oop", "C-bet des mains moyennes OOP (%)", G_FLOP, "pct", 35, 0, 100),
    P("cbet_multiway_scale", "Multiway : facteur sur les bluffs (%)", G_FLOP, "pct", 25, 0, 100),
    P("cbet_dry_adj", "Board As-haut sec : ajustement bluff (pts)", G_FLOP, "int", 15, -50, 50),
    P("cbet_wet_adj", "Texture humide : ajustement (pts)", G_FLOP, "int", -20, -50, 50),
    P("cbet_paired_adj", "Board pairé : ajustement (pts)", G_FLOP, "int", 10, -50, 50),
    P("cbet_mono_adj", "Board monotone : ajustement (pts)", G_FLOP, "int", -30, -60, 50),
    P("cbet_high_adj", "Board K/Q-haut sec : ajustement (pts)", G_FLOP, "int", 10, -50, 50),
    P("cbet_low_adj", "Board bas sec (<= 7) : ajustement (pts)", G_FLOP, "int", -10, -50, 50),
    P("cbet_mid_adj", "Board moyen sec (8-J haut) : ajustement (pts)", G_FLOP, "int", 0, -50, 50),
    P("cbet_connected_adj", "Board connecté : ajustement (pts)", G_FLOP, "int", -10, -50, 50),
    P("cbet_twotone_adj", "Board deux couleurs : ajustement (pts)", G_FLOP, "int", -5, -50, 50),
    P("tex_dynamic_pct", "Texture turn/river + défense : intensité (%, 0 = off)", G_FLOP, "pct", 100, 0, 200,
      help="turn/river : bluffs réduits quand flush/quinte/paire sont sur le board, accrus sur board sec ; "
           "défense : moins de calls sur board humide"),
    P("donk_freq", "Lead OOP des mains fortes, flop (%)", G_FLOP, "pct", 25, 0, 100,
      help="sans initiative et hors position : % de fois où Monster/Strong misent (sinon check, puis check-raise)"),
    P("donk_semibluff", "Lead OOP des tirages forts, semi-bluff (%)", G_FLOP, "pct", 30, 0, 100,
      help="flop et turn (x0.7), heads-up seulement ; les tirages faibles le font a 30% de cette frequence"),
    P("probe_freq", "Probe quand checké (%)", G_FLOP, "pct", 55, 0, 100),
    P("xr_value", "Check-raise value (%)", G_FLOP, "pct", 65, 0, 100),
    P("xr_bluff", "Check-raise bluff (tirages nuts, %)", G_FLOP, "pct", 15, 0, 100),
    P("raise_vs_bet_value", "Relance value face à une mise (%)", G_FLOP, "pct", 55, 0, 100),
    P("float_ip", "Float IP (vide avec backdoors, %)", G_FLOP, "pct", 30, 0, 100),
    P("call_scale", "Tolérance de call vs cotes (%)", G_FLOP, "int", 100, 50, 150, 1,
      help=">100 = paie plus large, <100 = fold plus"),
    # ------------------------------------------------------------------ turn
    P("barrel_value", "2e barrel value (%)", G_TURN, "pct", 90, 0, 100),
    P("barrel_semibluff", "2e barrel semi-bluff (%)", G_TURN, "pct", 70, 0, 100),
    P("barrel_bluff", "2e barrel bluff (mains vides, %)", G_TURN, "pct", 30, 0, 100),
    P("barrel_medium_ip", "Barrel des mains moyennes IP (%)", G_TURN, "pct", 40, 0, 100),
    P("barrel_scare_adj", "Carte dangereuse : ajustement bluff (pts)", G_TURN, "int", -15, -60, 40),
    P("delayed_cbet", "C-bet retardé IP (%)", G_TURN, "pct", 60, 0, 100),
    P("turn_probe", "Probe turn OOP (%)", G_TURN, "pct", 45, 0, 100),
    # ------------------------------------------------------------------ river
    P("river_value_thin", "Value fine (paire forte) IP (%)", G_RIVER, "pct", 60, 0, 100),
    P("river_bluff", "Bluff river (mains vides, %)", G_RIVER, "pct", 28, 0, 100),
    P("river_bluff_blockers", "Bonus bluff avec blockers (pts)", G_RIVER, "int", 25, 0, 60),
    P("river_probe", "Probe river (%)", G_RIVER, "pct", 40, 0, 100),
    P("river_raise_bluff", "Bluff-raise river (%)", G_RIVER, "pct", 3, 0, 30),
    P("river_call_scale", "Tolérance de call river (%)", G_RIVER, "int", 100, 50, 150, 1),
    # ------------------------------------------------------------------ tailles
    P("size_cbet_dry", "C-bet board sec (% pot)", G_SIZE, "int", 33, 20, 150, 1),
    P("size_cbet_wet", "C-bet board humide (% pot)", G_SIZE, "int", 66, 20, 150, 1),
    P("size_cbet_paired", "C-bet board pairé (% pot)", G_SIZE, "int", 33, 20, 150, 1),
    P("size_cbet_mono", "C-bet board monotone (% pot)", G_SIZE, "int", 40, 20, 150, 1),
    P("size_cbet_multiway", "C-bet multiway (% pot)", G_SIZE, "int", 66, 20, 150, 1),
    P("size_cbet_3bet", "C-bet pots 3bet+ (% pot)", G_SIZE, "int", 33, 20, 150, 1),
    P("size_turn", "Mise turn (% pot)", G_SIZE, "int", 66, 20, 200, 1),
    P("size_river", "Mise river value/bluff (% pot)", G_SIZE, "int", 70, 20, 200, 1),
    P("size_river_nuts", "Mise river avec les nuts IP (% pot)", G_SIZE, "int", 110, 20, 300, 1),
    P("size_thin", "Mise value fine (% pot)", G_SIZE, "int", 45, 20, 150, 1),
    P("size_raise_postflop", "Relance postflop (% pot)", G_SIZE, "int", 100, 50, 250, 1),
    # ------------------------------------------------------------------ stats adversaires
    P("use_stats", "Exploiter les stats PokerTracker (OpenHoldem pt_*)", G_STATS, "bool", False,
      help="nécessite PokerTracker configuré dans OpenHoldem ; sans base, le profil reste neutre"),
    P("stats_min_hands", "Mains minimum avant de se fier aux stats", G_STATS, "int", 60, 10, 500, 5),
    P("opp_nit_vpip", "Nit : VPIP <= (%)", G_STATS, "pct", 17, 5, 30),
    P("opp_fish_vpip", "Fish / station : VPIP >= (%)", G_STATS, "pct", 40, 25, 80),
    P("opp_maniac_pfr", "Maniaque : PFR >= (%)", G_STATS, "pct", 25, 10, 60),
    P("opp_maniac_af", "Maniaque : agression (AF) >=", G_STATS, "float", 3.5, 1.5, 10, 0.1),
    P("exploit_vs_nit", "Préflop vs nit : continuer (% de nos ranges)", G_STATS, "int", 70, 30, 150, 1),
    P("exploit_vs_fish", "Préflop vs fish : continuer (%)", G_STATS, "int", 125, 50, 200, 1),
    P("exploit_vs_maniac", "Préflop vs maniaque : continuer (%)", G_STATS, "int", 140, 50, 250, 1),
    P("exploit_size_fish", "Taille des mises vs fish / fish dans le pot (%)", G_STATS, "int", 125, 60, 200, 1,
      help="un fish paie trop : on mise plus gros pour la value"),
    P("exploit_size_nit", "Taille des mises vs nit (%)", G_STATS, "int", 85, 60, 200, 1,
      help="un nit se couche aux grosses mises : on mise plus petit"),
    P("exploit_size_maniac", "Taille des mises vs maniaque (%)", G_STATS, "int", 100, 60, 200, 1),
    P("opp_sticky_fold", "Adversaire collant : fold to c-bet flop <= (%)", G_STATS, "int", 35, 10, 60, 1),
    P("opp_folder_fold", "Adversaire foldeur : fold to c-bet flop >= (%)", G_STATS, "int", 65, 40, 90, 1),
    P("exploit_bluff_sticky", "Bluffs vs adversaire collant (% de la frequence)", G_STATS, "int", 40, 0, 150, 1,
      help="il ne se couche presque jamais au flop : on bluffe beaucoup moins (tous tours)"),
    P("exploit_bluff_folder", "Bluffs vs adversaire foldeur (% de la frequence)", G_STATS, "int", 130, 50, 250, 1),
    P("exploit_iso_fish", "Isoler un limper fish (% de la fréquence normale)", G_STATS, "int", 150, 50, 300, 1),
    P("exploit_bluff_nit", "Postflop vs nit : fréquence de bluff (%)", G_STATS, "int", 130, 20, 250, 1),
    P("exploit_bluff_fish", "Postflop vs fish : fréquence de bluff (%)", G_STATS, "int", 30, 0, 200, 1),
    P("exploit_bluff_maniac", "Postflop vs maniaque : fréquence de bluff (%)", G_STATS, "int", 60, 0, 200, 1),
    P("exploit_value_fish", "Postflop vs fish : value fine (% de la fréquence)", G_STATS, "int", 130, 50, 250, 1),
    P("exploit_call_nit", "Postflop vs nit : tolérance de call (%)", G_STATS, "int", 80, 40, 160, 1),
    P("exploit_call_fish", "Postflop vs fish : tolérance de call (%)", G_STATS, "int", 90, 40, 160, 1),
    P("exploit_call_maniac", "Postflop vs maniaque : tolérance de call (%)", G_STATS, "int", 130, 40, 220, 1),
    # ------------------------------------------------------------------ gestion de table
    P("sitin", "Se rasseoir automatiquement (f$sitin)", G_HOP, "bool", False),
    P("sitout_below_bb", "Se lever sous (BB, 0 = off)", G_HOP, "int", 0, 0, 100, 1),
    P("prefold_trash", "Prefold des mains poubelles (hors BB)", G_HOP, "bool", False,
      help="attention : prefold est évalué hors de ton tour"),
]

SCHEMA_BY_KEY = {p.key: p for p in SCHEMA}
GROUPS = list(dict.fromkeys(p.group for p in SCHEMA))


def defaults() -> dict:
    return {p.key: p.default for p in SCHEMA}


def coerce(key: str, value):
    p = SCHEMA_BY_KEY[key]
    if p.kind == "bool":
        return bool(value)
    if p.kind == "str":
        return str(value)
    if p.kind == "choice":
        if value not in p.choices:
            raise ValueError(f"{key}: {value!r} n'est pas dans {p.choices}")
        return value
    v = float(value)
    v = min(max(v, p.lo), p.hi)
    return int(round(v)) if p.kind == "int" else v


def normalize(overrides: dict | None = None, strict: bool = True) -> dict:
    """defaults + overrides, valeurs bornées. strict=True refuse les clés inconnues."""
    out = defaults()
    for k, v in (overrides or {}).items():
        if k not in SCHEMA_BY_KEY:
            if strict:
                raise KeyError(f"paramètre inconnu : {k}")
            continue
        out[k] = coerce(k, v)
    return out
