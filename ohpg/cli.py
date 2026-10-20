"""Interface en ligne de commande : python -m ohpg ..."""
from __future__ import annotations

import argparse
import json
import sys

from . import __version__, generator, presets, validator
from .params import SCHEMA


def _cfg_from_args(a) -> dict:
    over = {}
    if a.config:
        with open(a.config, encoding="utf-8") as fh:
            over.update(json.load(fh))
    for kv in a.set or []:
        k, _, v = kv.partition("=")
        over[k.strip()] = json.loads(v) if v.strip()[:1] in "[{\"0123456789-" or v.strip() in ("true", "false") else v.strip()
    return presets.build(a.style, a.format, over)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="ohpg", description="Générateur de profils OpenHoldem (OpenPPL)")
    ap.add_argument("--version", action="version", version=__version__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="génère un profil .ohf")
    g.add_argument("-o", "--out", default="profile.ohf")
    g.add_argument("--style", default="Balanced 6-max", choices=list(presets.STYLES))
    g.add_argument("--format", default="Cash 6-max", choices=list(presets.FORMATS))
    g.add_argument("--config", help="fichier JSON d'overrides")
    g.add_argument("--set", action="append", help="clé=valeur (répétable)")
    g.add_argument("--no-validate", action="store_true")

    v = sub.add_parser("validate", help="valide un fichier .ohf")
    v.add_argument("file")
    v.add_argument("--partial", action="store_true", help="ne pas exiger f$preflop/flop/turn/river")

    sub.add_parser("list", help="liste presets et paramètres")
    d = sub.add_parser("dump-config", help="écrit la configuration résultante en JSON")
    d.add_argument("--style", default="Balanced 6-max", choices=list(presets.STYLES))
    d.add_argument("--format", default="Cash 6-max", choices=list(presets.FORMATS))
    d.add_argument("--set", action="append")
    d.add_argument("--config")

    ps = sub.add_parser("pt-symbols", help="liste les symboles PokerTracker (pt_*) utilises par le profil genere")
    ps.add_argument("--style", default="Balanced 6-max", choices=list(presets.STYLES))
    ps.add_argument("--format", default="Cash 6-max", choices=list(presets.FORMATS))
    ps.add_argument("--set", action="append")
    ps.add_argument("--config")

    e = sub.add_parser("explain", help="decision du profil pour une main preflop dans une situation donnee")
    e.add_argument("--style", default="Balanced 6-max", choices=list(presets.STYLES))
    e.add_argument("--format", default="Cash 6-max", choices=list(presets.FORMATS))
    e.add_argument("--set", action="append")
    e.add_argument("--config")
    e.add_argument("--hand", required=True, help="ex. AKs, 77, T9o")
    e.add_argument("--pos", default="BTN", help="EP, MP, CO, BTN, SB, BB")
    e.add_argument("--scenario", default="Premiere action (ouverture)")
    e.add_argument("--stack", type=float, default=100.0)
    e.add_argument("--opener", default=None)

    gui = sub.add_parser("gui", help="lance l'interface graphique")

    a = ap.parse_args(argv)
    if a.cmd == "generate":
        cfg = _cfg_from_args(a)
        text = generator.generate(cfg)
        if not a.no_validate:
            errs = validator.errors(validator.validate(text))
            if errs:
                print("Profil invalide :", file=sys.stderr)
                for e in errs[:30]:
                    print(" ", e, file=sys.stderr)
                return 2
        with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        print(f"{a.out} : {len(text.splitlines())} lignes, validation OK")
        return 0
    if a.cmd == "validate":
        with open(a.file, encoding="utf-8", errors="replace") as fh:
            issues = validator.validate(fh.read(), require_main=not a.partial)
        for i in issues:
            print(i)
        n = len(validator.errors(issues))
        print(f"{n} erreur(s), {len(issues) - n} avertissement(s)")
        return 1 if n else 0
    if a.cmd == "list":
        print("Styles :", ", ".join(presets.STYLES))
        print("Formats :", ", ".join(presets.FORMATS))
        for p in SCHEMA:
            print(f"  {p.key:24s} {p.kind:6s} défaut={p.default!s:10s} {p.label}")
        return 0
    if a.cmd == "dump-config":
        print(json.dumps(_cfg_from_args(a), indent=2, ensure_ascii=False))
        return 0
    if a.cmd == "pt-symbols":
        import re
        cfg = _cfg_from_args(a)
        cfg["use_stats"] = True
        syms = sorted(set(re.findall(r"\bpt_\w+", generator.generate(cfg))))
        print("\n".join(syms))
        print(f"{len(syms)} symboles : verifie qu'ils s'affichent dans la fenetre des symboles d'OpenHoldem (PokerTracker connecte).")
        return 0
    if a.cmd == "explain":
        from .scenarios import SCENARIOS, explain
        if a.scenario not in SCENARIOS:
            print("Scenarios :", *SCENARIOS, sep="\n  ")
            return 2
        cfg = _cfg_from_args(a)
        cfg["randomize"] = False
        r = explain(generator.generate(cfg), a.pos, a.scenario, a.stack, int(cfg["table_size"]), a.hand, opener=a.opener)
        print(f"Action : {r['action']}\nGroupe : {r['group']}\nRegle  : {r['rule']}")
        return 0
    if a.cmd == "gui":
        from .gui.app import run
        return run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
