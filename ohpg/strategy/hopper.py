"""Fonctions de gestion de table : f$sitin, f$sitout, f$prefold."""
from __future__ import annotations

from .. import ranges as R
from ..ppl import Profile
from .common import HERO, join


def generate(prof: Profile, cfg: dict):
    if cfg["sitin"]:
        f = prof.func("f$sitin")
        f.comment("Se rasseoir automatiquement")
        f.ret("", "true")
    if cfg["sitout_below_bb"] > 0:
        f = prof.func("f$sitout")
        f.comment("Se lever quand le stack passe sous le seuil")
        f.ret(f"StackSize < {cfg['sitout_below_bb']} AND NOT istournament", "true")
        f.others_ret("false")
    if cfg["prefold_trash"]:
        f = prof.func("f$prefold")
        f.comment("Prefold des pires mains hors BB (évalué hors de notre tour : risque d'état instable)")
        trash = R.PLAY_ORDER[-60:]
        name = prof.add_list("PrefoldTrash", trash)
        f.ret(join("AmountToCall > 0", "NOT InBigBlind", name), "true")
        f.others_ret("false")
