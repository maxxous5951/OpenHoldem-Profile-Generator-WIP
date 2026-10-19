"""Validateur OpenPPL : vérifie la structure et que chaque symbole existe réellement
(bibliothèque OpenPPL officielle + symboles intégrés d'OpenHoldem)."""
from __future__ import annotations

import re
from dataclasses import dataclass
from importlib import resources

MAIN_FUNCTIONS = ("f$preflop", "f$flop", "f$turn", "f$river")

# fonctions « hook » que l'utilisateur est censé définir (non considérées comme collision)
USER_HOOKS = {"f$sitin", "f$sitout", "f$prefold", "f$leave", "f$close", "f$rebuy", "f$chat", "f$delay", "f$test"}

KEYWORDS = {
    "when", "return", "force", "others", "and", "or", "not", "xor", "true", "false", "bitand", "bitor",
    "bitxor", "set",
}
FIXED_ACTIONS = {
    "fold", "check", "call", "raisemax", "raisepot", "raisemin", "raisehalfpot", "raisethirdpot",
    "raisetwothirdpot", "raisethreefourthpot", "raisefourthpot", "betmax", "betpot", "betmin", "allin",
    "beep", "raiseto", "raiseby", "bet", "raise", "betthreefourthpot", "bettwothirdpot", "bethalfpot",
    "betthirdpot", "betfourthpot",
}
# symboles intégrés d'OpenHoldem/OpenPPL absents de la liste du dumper (constantes, cartes, etc.)
EXTRA_KNOWN = {
    "ace", "king", "queen", "jack", "ten", "nine", "eight", "seven", "six", "five", "four", "three", "two",
    "preflop", "flop", "turn", "river", "isomaha", "isholdem",
}


def _load(name: str) -> set[str]:
    txt = resources.files("ohpg.data").joinpath(name).read_text(encoding="utf-8")
    return {ln.strip() for ln in txt.splitlines() if ln.strip()}


_LIB = None
_OH = None


def library_names() -> set[str]:
    global _LIB
    if _LIB is None:
        _LIB = {n.lower() for n in _load("openppl_library_names.txt")}
    return _LIB


def oh_symbols() -> set[str]:
    global _OH
    if _OH is None:
        _OH = {n.lower() for n in _load("openholdem_symbols.txt")}
    return _OH


@dataclass
class Issue:
    level: str  # "error" | "warning"
    line: int
    message: str

    def __str__(self):
        return f"{self.level.upper():7s} ligne {self.line}: {self.message}"


_SECTION = re.compile(r"^##([A-Za-z0-9_$]+)##\s*$")
_IDENT = re.compile(r"\$\$[a-z]{2}\d|(?:hand|board)\$[A-Za-z0-9]+|[A-Za-z_][A-Za-z0-9_$]*")
_PT_STAT = re.compile(r"^pt_(hands|vpip|pfr|aggr_factor|total_af|rfi|3bet|4bet|fold_to_3bet|fold_to_4bet|steal_attempt|"
                      r"bb_fold_to_steal|sb_fold_to_steal|flop_cbet|flop_fold_to_cbet|flop_checkraise|flop_donkbet|"
                      r"turn_cbet|turn_fold_to_cbet|turn_checkraise|river_fold_to_cbet|river_bet|wtsd|wssd)_"
                      r"(headsupchair|raischair|lastraiserchair|firstraiserchair|firstcallerchair|lastcallerchair|"
                      r"smallblindchair|bigblindchair|dealerchair|cutoffchair)$")
_HAND_TOKEN = re.compile(r"^[AKQJT2-9]{2}[so]?$")


def _strip_comments(text: str) -> list[str]:
    text = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    return [re.sub(r"//.*", "", ln).rstrip() for ln in text.split("\n")]


def validate(text: str, require_main: bool = True) -> list[Issue]:
    issues: list[Issue] = []
    for i, raw in enumerate(text.splitlines(), 1):
        if any(ord(c) > 127 for c in raw):
            issues.append(Issue("error", i, "caractère non-ASCII (accent...) : OpenHoldem ne le supporte pas"))
    lines = _strip_comments(text)

    sections: list[tuple[str, int, list[tuple[int, str]]]] = []
    for i, ln in enumerate(lines, 1):
        m = _SECTION.match(ln.strip())
        if m:
            sections.append((m.group(1), i, []))
        elif ln.strip():
            if not sections:
                issues.append(Issue("error", i, "code en dehors de toute section ##nom##"))
            else:
                sections[-1][2].append((i, ln.strip()))

    names = [s[0] for s in sections]
    for n in {x for x in names if names.count(x) > 1}:
        first = [s[1] for s in sections if s[0] == n]
        issues.append(Issue("error", first[1], f"section définie plusieurs fois : {n}"))

    user_funcs = {n.lower() for n in names if n.lower().startswith("f$")}
    user_lists = {n.lower() for n in names if n.lower().startswith("list")}
    lib = library_names()
    oh = oh_symbols()

    if require_main:
        for mf in MAIN_FUNCTIONS:
            if mf not in user_funcs:
                issues.append(Issue("error", 1, f"fonction principale manquante : {mf}"))

    referenced: set[str] = set()
    for name, start, body in sections:
        low = name.lower()
        bare = low[2:] if low.startswith("f$") else low
        if low.startswith("f$") and bare in lib and low not in USER_HOOKS:
            issues.append(Issue("error", start, f"{name} redéfinit un symbole de la bibliothèque OpenPPL"))
        if low.startswith("list"):
            if not body:
                issues.append(Issue("error", start, f"handlist vide : {name}"))
            for ln_no, ln in body:
                for tok in ln.split():
                    if not _HAND_TOKEN.match(tok):
                        issues.append(Issue("error", ln_no, f"main invalide dans {name} : {tok!r}"))
            continue
        if not body:
            issues.append(Issue("error", start, f"fonction vide : {name}"))
            continue
        is_main = low in MAIN_FUNCTIONS
        group_open_others = False
        for ln_no, ln in body:
            if ln.count("(") != ln.count(")"):
                issues.append(Issue("error", ln_no, "parenthèses non équilibrées"))
            if not re.match(r"(?i)when\b", ln):
                issues.append(Issue("error", ln_no, f"ligne qui ne commence pas par WHEN : {ln[:60]!r}"))
                continue
            has_force = re.search(r"(?i)\bforce\s*$", ln) is not None
            ret = re.search(r"(?i)\breturn\b", ln) is not None
            if ret and is_main:
                issues.append(Issue("error", ln_no, f"RETURN interdit dans {name} (utiliser une action)"))
            cond = ln
            if has_force:
                cond = re.sub(r"(?i)\s*\bforce\s*$", "", cond)
            if not has_force and re.search(r"(?i)\b(raiseto|raiseby|fold|check|call)\b", ln):
                issues.append(Issue("error", ln_no, "action sans FORCE"))
            if not has_force and not ret:
                group_open_others = False  # nouvel en-tête de groupe
            if group_open_others and has_force:
                issues.append(Issue("warning", ln_no, "code inatteignable après WHEN Others"))
            if re.match(r"(?i)when\s+others\b", ln) and has_force and not ln.startswith(" "):
                group_open_others = True
            if has_force and not ret and not is_main:
                issues.append(Issue("warning", ln_no, f"action dans une fonction auxiliaire {name}"))
            for tok in _IDENT.findall(cond):
                t = tok.lower()
                if t.startswith(("hand$", "board$", "$$")):
                    continue
                if t.startswith("f$"):
                    referenced.add(t)
                    if t not in user_funcs and t[2:] not in lib and t[2:] not in oh and t not in {"f$" + x for x in oh}:
                        issues.append(Issue("error", ln_no, f"fonction inconnue : {tok}"))
                    continue
                if t in KEYWORDS or t in FIXED_ACTIONS or t in EXTRA_KNOWN:
                    continue
                if t.startswith("list"):
                    referenced.add(t)
                    if t not in user_lists:
                        issues.append(Issue("error", ln_no, f"handlist inconnue : {tok}"))
                    continue
                if t in lib or t in oh or _PT_STAT.match(t):
                    continue
                issues.append(Issue("error", ln_no, f"symbole inconnu : {tok}"))
    for n in user_funcs - referenced - set(MAIN_FUNCTIONS):
        issues.append(Issue("warning", 1, f"fonction jamais utilisée : {n}"))
    for n in user_lists - referenced:
        issues.append(Issue("warning", 1, f"handlist jamais utilisée : {n}"))
    return issues


def errors(issues):
    return [i for i in issues if i.level == "error"]
