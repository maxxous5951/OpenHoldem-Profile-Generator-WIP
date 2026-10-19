"""Presets : styles de jeu et formats de table (overrides appliqués sur les valeurs par défaut)."""
from __future__ import annotations

from .params import normalize

STYLES = {
    "Balanced 6-max": {},
    "TAG": {"open_ep": 13, "open_mp": 17, "open_co": 25, "open_btn": 42, "open_sb": 38, "threebet_bluff_ratio": 0.5,
            "cbet_bluff_ip": 50, "river_bluff": 25, "aggression_scale": 100},
    "LAG": {"open_ep": 18, "open_mp": 24, "open_co": 34, "open_btn": 58, "open_sb": 50, "threebet_value": 4.5,
            "threebet_bluff_ratio": 0.9, "bb_defend_pct": 44, "call_ip_pct": 11, "iso_raise_pct": 16,
            "cbet_bluff_ip": 68, "cbet_bluff_oop": 48, "barrel_bluff": 42, "river_bluff": 36, "aggression_scale": 135,
            "xr_bluff": 22, "float_ip": 40},
    "Nit": {"open_ep": 9, "open_mp": 12, "open_co": 18, "open_btn": 30, "open_sb": 26, "threebet_value": 2.6,
            "threebet_bluff_ratio": 0.15, "bb_defend_pct": 26, "call_ip_pct": 5, "iso_raise_pct": 7,
            "fourbet_value": 1.4, "fourbet_bluff_ratio": 0.1, "cbet_bluff_ip": 30, "cbet_bluff_oop": 12,
            "barrel_bluff": 12, "river_bluff": 10, "aggression_scale": 60, "float_ip": 10, "xr_bluff": 4,
            "call_scale": 85, "river_call_scale": 85},
    "Maniac": {"open_ep": 26, "open_mp": 34, "open_co": 46, "open_btn": 72, "open_sb": 65, "threebet_value": 6,
               "threebet_bluff_ratio": 1.4, "bb_defend_pct": 55, "call_ip_pct": 14, "iso_raise_pct": 24,
               "cbet_bluff_ip": 85, "cbet_bluff_oop": 65, "barrel_bluff": 60, "river_bluff": 50,
               "aggression_scale": 180, "xr_bluff": 35, "float_ip": 55, "call_scale": 115},
    "Calling Station (fish)": {"open_ep": 22, "open_mp": 26, "open_co": 32, "open_btn": 45, "open_sb": 40,
                               "threebet_value": 2.2, "threebet_bluff_ratio": 0.0, "call_ip_pct": 18, "call_sb_pct": 10,
                               "bb_defend_pct": 55, "iso_raise_pct": 8, "overlimp_pct": 20, "cbet_bluff_ip": 30,
                               "cbet_bluff_oop": 10, "barrel_bluff": 8, "river_bluff": 6, "call_scale": 125,
                               "river_call_scale": 120, "aggression_scale": 50},
    "Exploit vs Passive": {"open_ep": 15, "open_mp": 21, "open_co": 30, "open_btn": 50, "open_sb": 44,
                           "cbet_bluff_ip": 35, "barrel_bluff": 18, "river_bluff": 12, "barrel_value": 100,
                           "river_value_thin": 85, "size_thin": 55, "call_scale": 90},
}

FORMATS = {
    "Cash 6-max": {"game": "cash", "table_size": 6},
    "Cash Full Ring": {"game": "cash", "table_size": 9, "open_ep": 10, "open_mp": 15, "open_co": 22, "open_btn": 38,
                       "open_sb": 34, "threebet_value": 3.0},
    "Cash Heads-Up": {"game": "cash", "table_size": 2, "open_sb": 85, "open_btn": 85, "bb_defend_pct": 62,
                      "threebet_value": 7, "threebet_bluff_ratio": 1.0, "open_size_sb": 2.3, "call_ip_pct": 20},
    "MTT 9-max (push/fold 15BB)": {"game": "tournament", "table_size": 9, "pf_max_stack": 15, "ante_bb": 0.12,
                                   "open_ep": 11, "open_mp": 16, "open_co": 24, "open_btn": 42, "open_sb": 36,
                                   "icm_pressure": 25, "openjam_max": 22, "threebet_shove_stack": 24, "fourbet_shove_stack": 34},
    "SNG bubble": {"game": "tournament", "table_size": 6, "pf_max_stack": 14, "icm_pressure": 70, "ante_bb": 0.0,
                   "pf_call_scale": 90},
    "Spin & Go 3-max": {"game": "tournament", "table_size": 3, "pf_max_stack": 12, "open_ep": 40, "open_mp": 40,
                        "open_co": 40, "open_btn": 55, "open_sb": 60, "bb_defend_pct": 50, "icm_pressure": 40,
                        "sb_limp_pct": 30, "openjam_max": 20, "openjam_pct": 8},
}


def build(style: str = "Balanced 6-max", fmt: str = "Cash 6-max", overrides: dict | None = None) -> dict:
    """defaults ← style ← format ← overrides."""
    cfg = {}
    cfg.update(STYLES[style])
    cfg.update(FORMATS[fmt])
    cfg.update(overrides or {})
    cfg.setdefault("name", f"OHPG {style} / {fmt}")
    return normalize(cfg)
