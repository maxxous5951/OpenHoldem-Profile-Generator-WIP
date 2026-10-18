"""Mini-interpréteur OpenPPL pour tester les décisions du profil généré (sous-ensemble suffisant)."""
from __future__ import annotations

import random
import re

ACTION_RE = re.compile(r"^(RaiseTo\s+.+?|RaiseBy\s+.+?|Fold|Check|Call|RaiseMax|RaisePot|Allin|BetMax)\s*$", re.I)


class Sim:
    def __init__(self, text: str):
        self.sections: dict[str, list[str]] = {}
        cur = None
        for ln in text.split("\n"):
            ln = re.sub(r"//.*", "", ln).rstrip()
            m = re.match(r"^##([A-Za-z0-9_$]+)##$", ln.strip())
            if m:
                cur = m.group(1)
                self.sections[cur] = []
            elif cur and ln.strip():
                self.sections[cur].append(ln.strip())
        self.lists = {n.lower(): set(" ".join(b).split()) for n, b in self.sections.items() if n.startswith("list")}

    # ------------------------------------------------------------------ expressions
    def _py(self, expr: str) -> str:
        e = expr
        e = re.sub(r"^\s*Others\s*$", "True", e, flags=re.I)
        e = re.sub(r"\bAND\b", " and ", e, flags=re.I)
        e = re.sub(r"\bOR\b", " or ", e, flags=re.I)
        e = re.sub(r"\bNOT\b", " not ", e, flags=re.I)
        e = re.sub(r"(?<![<>=!])=(?!=)", "==", e)
        e = re.sub(r"\btrue\b", "True", e, flags=re.I)
        e = re.sub(r"\bfalse\b", "False", e, flags=re.I)
        e = e.replace("$", "_S_")
        return e

    def ev(self, expr: str, st: dict):
        scope = _Scope(self, st)
        return eval(self._py(expr), {"__builtins__": {}}, scope)

    def call_func(self, name: str, st: dict):
        body = self.sections[name]
        for ln in body:
            m = re.match(r"(?i)when\s+(.*?)\s+return\s+(.*?)\s+force$", ln)
            if m and self.ev(m.group(1), st):
                return self.ev(m.group(2), st)
        raise RuntimeError(f"{name}: aucune branche")

    # ------------------------------------------------------------------ décision
    def decide(self, fn: str, st: dict, seed: int = 1):
        st = {k.lower(): v for k, v in st.items()}
        rng = random.Random(seed)
        st.setdefault("randomhand", rng.random())
        st.setdefault("randomround", rng.random())
        active = True
        for ln in self.sections[fn]:
            m = re.match(r"(?i)when\s+(.*)$", ln)
            cond = m.group(1)
            fm = re.match(r"^(.*?)\s+FORCE$", cond, flags=re.I)
            if not fm:  # en-tête de groupe
                active = bool(self.ev(cond.strip(), st))
                continue
            if not active:
                continue
            body = fm.group(1)
            # séparer condition et action : l'action est le plus long suffixe reconnu
            for am in re.finditer(r"\s(RaiseTo\s.+|RaiseBy\s.+|Fold|Check|Call|RaiseMax|RaisePot)$", " " + body):
                pass
            mm = re.match(r"^(?P<c>.*?)(?:\s+(?P<a>RaiseTo\s.+|RaiseBy\s.+|Fold|Check|Call|RaiseMax|RaisePot))$", body, flags=re.I)
            c, a = (mm.group("c"), mm.group("a")) if mm else ("Others", body)
            if c.strip().lower() == "when others" or c.strip().lower() == "others":
                return self._fmt(a, st)
            if self.ev(c, st):
                return self._fmt(a, st)
        return None

    def _fmt(self, action: str, st):
        m = re.match(r"(?i)(RaiseTo|RaiseBy)\s+(.*)$", action)
        if m:
            arg = m.group(2).strip()
            if arg.endswith("%"):
                return f"{m.group(1)} {arg}"
            return f"{m.group(1)} {round(float(self.ev(arg, st)), 2)}"
        return action


class _Scope(dict):
    def __init__(self, sim, st):
        super().__init__()
        self.sim, self.st = sim, st

    def __missing__(self, key):
        raw = key.replace("_S_", "$")
        low = raw.lower()
        if low in self.sim.lists:
            return self.st["hand"] in self.sim.lists[low]
        if low in self.st:
            return self.st[low]
        for n in self.sim.sections:
            if n.lower() == low:
                return self.sim.call_func(n, self.st)
        raise KeyError(f"symbole non fourni au simulateur : {raw}")

    def __getitem__(self, key):
        return self.__missing__(key)
