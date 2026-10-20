"""Situations preflop pretes a l'emploi pour tester une decision du profil (sans OpenHoldem).

Chaque scenario fournit les symboles OpenHoldem necessaires ; la position du hero est ajoutee d'apres la taille de table.
Le simulateur couvre le sous-ensemble OpenPPL du profil : le postflop (board, tirages) n'est pas simule.
"""
from __future__ import annotations

from .strategy import common

BASE = dict(BotsActionsOnThisRoundIncludingChecks=0, Raises=0, Calls=0, CallsSinceLastRaise=0, BotRaisedBeforeFlop=False,
            NumberOfRaisesBeforeFlop=0, RaisesSinceLastPlay=0, AmountToCall=1.0, ncurrentbets=0, BetSize=1.0, PotSize=1.5,
            StackSize=100, EffectiveMaxStacksizeOfActiveOpponents=100, MaxStillToActStackSize=100, SmallBlindCalling=False,
            IsBubble=False, Opponents=1)

# nom -> (description, diff d'etat)
SCENARIOS = {
    "Premiere action (ouverture)": ("Personne n'est entre dans le pot", dict(AmountToCall=1.0)),
    "Face a un limp": ("Un joueur a limpe devant nous", dict(Calls=1, AmountToCall=1.0, PotSize=2.5)),
    "Face a une ouverture 2.5 BB": ("Une relance, aucun caller", dict(Raises=1, AmountToCall=2.5, PotSize=4, ncurrentbets=0)),
    "Face a une ouverture + 1 caller (squeeze)": ("Une relance et un call", dict(Raises=1, CallsSinceLastRaise=1, AmountToCall=2.5, PotSize=6.5)),
    "On a ouvert, face a un 3bet a 8 BB": ("Notre ouverture a 2.5, 3bet a 8", dict(
        BotRaisedBeforeFlop=True, BotsActionsOnThisRoundIncludingChecks=1, Raises=1, RaisesSinceLastPlay=1, AmountToCall=5.5,
        ncurrentbets=2.5, PotSize=12)),
    "On a 3bete, face a un 4bet a 20 BB": ("Notre 3bet a 8, 4bet a 20", dict(
        BotRaisedBeforeFlop=True, BotsActionsOnThisRoundIncludingChecks=1, Raises=2, RaisesSinceLastPlay=1, AmountToCall=12,
        ncurrentbets=8, PotSize=30)),
    "Face a un all-in": ("Mise qui nous met all-in", dict(Raises=2, AmountToCall=30, PotSize=45)),
}


def build_state(pos: str, scenario: str, stack: float, table_size: int, hand: str, extra: dict | None = None) -> dict:
    cfg = {"table_size": table_size}
    common.configure(cfg)
    if pos not in common.HERO:
        raise ValueError(f"position {pos} absente d'une table de {table_size} joueurs ({', '.join(common.ORDER)})")
    st = dict(BASE)
    st.update(SCENARIOS[scenario][1])
    st.update(StackSize=stack, EffectiveMaxStacksizeOfActiveOpponents=stack,
              MaxStillToActStackSize=0 if pos == "BB" else stack)
    st["Opponents"] = 1
    hero = common.HERO[pos].strip("()")
    for name in hero.split(" OR "):
        st[name] = True
    if pos == "BB":
        st["AmountToCall"] = 0.0 if st["Raises"] == 0 and st["Calls"] == 0 else st["AmountToCall"]
    st["hand"] = hand
    st.update(extra or {})
    return st


def explain(text: str, pos: str, scenario: str, stack: float, table_size: int, hand: str, extra: dict | None = None,
            fn: str = "f$preflop", opener: str | None = None) -> dict:
    """Decision du profil pour une main et une situation. Retourne action, groupe WHEN et regle declenchee.

    `opener` : position de l'adversaire qui a relance (defaut : la derniere position avant nous).
    """
    import re
    from .sim import Sim
    sim = Sim(text)
    st = build_state(pos, scenario, stack, table_size, hand, extra)
    for name in set(re.findall(r"\b(In[A-Z]\w*|\w+Raising|\w+Calling)\b", text)):  # non fournis = faux
        st.setdefault(name, False)
    if st.get("Raises", 0) >= 1:
        cands = common.openers_before(pos) or common.actives()
        op = opener or cands[-1]
        if op not in common.OPENER:
            raise ValueError(f"ouvreur {op} absent de cette table ({', '.join(common.OPENER)})")
        for name in common.OPENER[op].strip("()").split(" OR "):
            st[name.strip()] = True
    try:
        act = sim.decide(fn, st)
    except (KeyError, NameError) as exc:
        raise RuntimeError(f"situation incomplete pour le simulateur : {exc}") from exc
    return {"action": act, "group": sim.trace["group"], "rule": sim.trace["rule"]}
