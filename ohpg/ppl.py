"""Émetteur OpenPPL : handlists, fonctions, conditions WHEN / actions / RETURN."""
from __future__ import annotations

import textwrap
from typing import Iterable

FIXED_ACTIONS = (
    "Fold", "Check", "Call", "RaiseMax", "RaisePot", "RaiseMin", "RaiseHalfPot", "RaiseThirdPot",
    "RaiseTwoThirdPot", "RaiseThreeFourthPot", "RaiseFourthPot", "BetMax", "BetPot", "BetMin", "Allin", "Beep",
)


def raise_to(expr) -> str:
    return f"RaiseTo {expr}"


def raise_by_pct(pct) -> str:
    return f"RaiseBy {fmt(pct)}%"


def fmt(x) -> str:
    """Nombre court et déterministe (pas de 2.0000000001)."""
    if isinstance(x, str):
        return x
    r = round(float(x), 3)
    return str(int(r)) if r == int(r) else f"{r:g}"


def AND(*parts: str) -> str:
    parts = [p for p in parts if p]
    return " AND ".join(parts)


def OR(*parts: str) -> str:
    parts = [p for p in parts if p]
    return parts[0] if len(parts) == 1 else "(" + " OR ".join(parts) + ")"


class Func:
    """Corps d'une fonction OpenPPL, construit ligne par ligne."""

    def __init__(self, name: str):
        self.name = name
        self.lines: list[str] = []
        self._nested = False

    def comment(self, text: str):
        for ln in str(text).splitlines():
            indent = "    " if self._nested and not ln.lstrip().startswith(("===", "---")) else ""
            self.lines.append(indent + "// " + ln)
        return self

    def blank(self):
        self.lines.append("")
        return self

    def group(self, cond: str):
        """Condition « open-ended » : les lignes suivantes ne sont évaluées que si `cond` est vraie."""
        self.lines.append(f"WHEN {cond}")
        self._nested = True
        return self

    def end_group(self):
        self._nested = False
        return self

    def act(self, cond: str, action: str):
        pre = "    " if self._nested else ""
        self.lines.append(f"{pre}WHEN {cond} {action} FORCE" if cond else f"{pre}WHEN Others {action} FORCE")
        return self

    def ret(self, cond: str, value):
        pre = "    " if self._nested else ""
        self.lines.append(f"{pre}WHEN {cond} RETURN {fmt(value)} FORCE" if cond else f"{pre}WHEN Others RETURN {fmt(value)} FORCE")
        return self

    def others(self, action: str):
        pre = "    " if self._nested else ""
        self.lines.append(f"{pre}WHEN Others {action} FORCE")
        return self

    def others_ret(self, value):
        pre = "    " if self._nested else ""
        self.lines.append(f"{pre}WHEN Others RETURN {fmt(value)} FORCE")
        return self

    def render(self) -> str:
        return f"##{self.name}##\n" + "\n".join(self.lines) + "\n"


class Profile:
    def __init__(self):
        self.header: list[str] = []
        self.lists: dict[str, list[str]] = {}
        self._list_by_content: dict[tuple, str] = {}
        self.funcs: dict[str, Func] = {}

    # --- handlists
    def add_list(self, name: str, hands: Iterable[str]) -> str:
        """Ajoute une handlist (nom commençant par 'list'). Réutilise une liste identique existante."""
        hands = list(hands)
        if not hands:
            return "false"  # jamais de handlist vide : l'appelant saute la règle
        key = tuple(sorted(hands))
        if key in self._list_by_content:
            return self._list_by_content[key]
        if not name.startswith("list"):
            name = "list" + name
        if name in self.lists:
            raise ValueError(f"handlist en double : {name}")
        self.lists[name] = hands
        self._list_by_content[key] = name
        return name

    # --- fonctions
    def func(self, name: str) -> Func:
        if name in self.funcs:
            raise ValueError(f"fonction en double : {name}")
        f = Func(name)
        self.funcs[name] = f
        return f

    def render(self) -> str:
        out = ["\n".join(self.header).rstrip() + "\n"] if self.header else []
        for name, hands in self.lists.items():
            body = textwrap.fill(" ".join(hands), width=96, initial_indent="    ", subsequent_indent="    ")
            out.append(f"##{name}##\n{body}\n")
        for f in self.funcs.values():
            out.append(f.render())
        return "\n".join(out).rstrip() + "\n"
