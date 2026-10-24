#!/usr/bin/env python3
"""Optimisation évolutive d'un profil OpenHoldem contre un pool de bots (pokersim + ohpg).

Chaque génération :
  1. des enfants sont créés (croisement + mutation des survivants) ;
  2. étape 1 : chaque enfant joue quelques tables courtes (adversaires tirés dans les bots d'ENTRAÎNEMENT) ;
  3. étape 2 : les meilleurs enfants reçoivent un gros volume de mains ;
  4. survivants = meilleurs scores, score = moyenne - k x erreur-type (borne basse : évite les gagnants par chance).

Paramètres optimisés : --groups (jeux de paramètres) ou --stages (plusieurs étapes enchaînées : chaque étape ne fait varier que
ses groupes et repart du meilleur de l'étape précédente). Groupes : base, open, defense, big, flop, turn, river, sizes, global, exploit, all.
Voir --list-groups. Exemple (recommandé pour un profil complet) :
    --stages "open,defense,big;flop,turn,river;sizes,global" --gens 15

Tout est sauvegardé à chaque génération (state.json) : Ctrl+C puis --resume pour reprendre.
Le pool de VALIDATION n'est jamais utilisé ici : voir validate.py.
"""
from __future__ import annotations

import argparse
import json
import random
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import simlib
from simlib import Acc, Ctx

STYLE, FORMAT = "Balanced 6-max", "Cash 6-max"
HERO = "HERO"

CORE_GENES = [
    "open_ep", "open_mp", "open_co", "open_btn", "open_sb",
    "threebet_value", "threebet_bluff_ratio", "bb_defend_pct", "call_ip_pct", "fourbet_value", "call_3bet_ip",
    "cbet_bluff_ip", "cbet_bluff_oop", "cbet_semibluff", "barrel_bluff", "river_bluff",
    "call_scale", "river_call_scale", "aggression_scale",
    "size_cbet_dry", "size_cbet_wet", "size_turn", "size_river",
]
EXPLOIT_GENES = [
    "exploit_vs_nit", "exploit_vs_fish", "exploit_vs_maniac", "exploit_size_fish", "exploit_size_nit", "exploit_size_maniac",
    "exploit_bluff_sticky", "exploit_bluff_folder", "exploit_bluff_nit", "exploit_bluff_fish", "exploit_bluff_maniac",
    "exploit_value_fish", "exploit_call_nit", "exploit_call_fish", "exploit_call_maniac", "exploit_iso_fish",
]
SEED_STYLES = ["Balanced 6-max", "TAG", "LAG", "Nit", "Maniac", "Calling Station (fish)"]

GROUP_NAMES = ["base", "open", "defense", "big", "flop", "turn", "river", "sizes", "global", "exploit", "all"]
GROUP_HELP = {
    "base": "jeu réduit de 23 paramètres (ouvertures, 3bet, défense, c-bet, barrels, bluffs, tolérance de call, 4 tailles postflop)",
    "open": "ouverture par position, isolation, overlimp (largeur des ranges et fréquences)",
    "defense": "3bet, cold-call, défense de la BB, continuer face au 3bet, 4bet value",
    "big": "4bet / 5bet / squeeze : bluffs, calls, face à un all-in",
    "flop": "flop : c-bet, semi-bluffs, check-raise, probe, donk, textures de board, engagement du tapis",
    "turn": "turn : barrels, c-bet retardé, probe",
    "river": "river : value fine, bluffs, blockers, tolérance de call",
    "sizes": "toutes les tailles de mise (préflop : ouverture, isolation, 3bet, 4bet, squeeze ; postflop : % du pot)",
    "global": "réglages globaux : échelle de toutes les ranges d'ouverture, agressivité globale (bluffs et relances)",
    "exploit": "16 paramètres d'exploitation selon les stats adversaires (impose use_stats)",
    "all": "tous les paramètres de style hors exploitation (open + defense + big + flop + turn + river + sizes + global)",
}
# paramètres sans effet à 100 BB en cash (seuils de tapis) ou liés au limp du SB : exclus de la recherche
SKIP_GENES = {"table_size", "ante_bb", "sb_limp_pct", "payout", "threebet_shove_stack", "fourbet_shove_stack",
              "bb_iso_vs_sblimp", "size_iso_sblimp"}


def group_genes(params, name: str) -> list[str]:
    num = ("pct", "int", "float")

    def keys(group, sizes=None):
        ks = [p.key for p in params.SCHEMA if p.group == group and p.kind in num and p.key not in SKIP_GENES]
        if sizes is None:
            return ks
        return [k for k in ks if ("size" in k) == sizes]

    preflop_sizes = keys(params.G_OPEN, True) + keys(params.G_DEF, True) + keys(params.G_BIG, True)
    table = {
        "base": CORE_GENES,
        "open": keys(params.G_OPEN, False),
        "defense": keys(params.G_DEF, False),
        "big": keys(params.G_BIG, False),
        "flop": keys(params.G_FLOP),
        "turn": keys(params.G_TURN),
        "river": keys(params.G_RIVER),
        "sizes": keys(params.G_SIZE) + preflop_sizes,
        "global": ["range_scale", "aggression_scale"],
        "exploit": [p.key for p in params.SCHEMA if p.group == params.G_STATS and p.key.startswith("exploit_")],
    }
    if name == "all":
        out = []
        for g in ("open", "defense", "big", "flop", "turn", "river", "sizes", "global"):
            out += table[g]
        return out
    if name not in table:
        raise SystemExit(f"groupe inconnu : {name} (groupes : {', '.join(GROUP_NAMES)})")
    return list(table[name])


def parse_stages(args) -> list[list[str]]:
    """--stages "a,b;c" -> [["a","b"],["c"]] ; sinon --groups (une seule étape)."""
    if args.stages:
        stages = [[g.strip() for g in st.split(",") if g.strip()] for st in args.stages.split(";") if st.strip()]
    else:
        stages = [[g.strip() for g in args.groups.split(",") if g.strip()]]
    if not stages or not all(stages):
        raise SystemExit("--stages / --groups vide")
    return stages


# ---------------------------------------------------------------------------------------------- génome
class Space:
    def __init__(self, genes: list[str], use_stats: bool):
        from ohpg import params, presets
        self.params, self.presets = params, presets
        self.genes = genes
        self.use_stats = use_stats
        self.base = presets.build(STYLE, FORMAT)

    def bounds(self, g):
        p = self.params.SCHEMA_BY_KEY[g]
        return p.lo, p.hi

    def clamp(self, g, v):
        v = self.params.coerce(g, v)
        return v if self.params.SCHEMA_BY_KEY[g].kind == "int" else round(v, 3)

    def from_style(self, style):
        full = self.presets.build(style, FORMAT)
        return {g: full[g] for g in self.genes}

    def mutate(self, genome, rng, sigma, p_gene, active=None):
        """Mute des gènes de `active` (par défaut tous). p_gene est plafonné pour qu'un enfant ne change qu'une poignée de gènes."""
        active = active or self.genes
        out = dict(genome)
        p = min(p_gene, 7.0 / len(active))
        picked = [g for g in active if rng.random() < p] or [rng.choice(active)]
        for g in picked:
            lo, hi = self.bounds(g)
            out[g] = self.clamp(g, out[g] + rng.gauss(0, sigma) * (hi - lo))
        return out

    def cross(self, a, b, rng, active=None):
        act = set(active or self.genes)
        return {g: (a[g] if (g not in act or rng.random() < 0.5) else b[g]) for g in self.genes}

    def overrides(self, genome):
        o = dict(genome)
        if self.use_stats:
            o["use_stats"] = True
        return o


# ---------------------------------------------------------------------------------------------- boucle
class Cand:
    _next = 0

    def __init__(self, genome, acc=None, cid=None, origin=""):
        if cid is None:
            Cand._next += 1
            cid = Cand._next
        self.id, self.genome, self.acc, self.origin = cid, genome, acc or Acc(), origin

    def score(self, k):
        return self.acc.mean - k * self.acc.se if self.acc.n >= 2 else float("-inf")

    def to_json(self):
        return {"id": self.id, "genome": self.genome, "acc": self.acc.to_json(), "origin": self.origin}

    @classmethod
    def from_json(cls, d):
        return cls(d["genome"], Acc.from_json(d["acc"]), d["id"], d.get("origin", ""))


def eval_batch(ctx, ex, space, cands, tables, games, hands, seed, tmp: Path):
    """Fait jouer tous les candidats sur les mêmes tables, en parallèle ; ajoute les résultats à leur accumulateur."""
    futs = []
    for c in cands:
        f = simlib.write_profile(space.overrides(c.genome), STYLE, FORMAT, HERO, tmp / f"c{c.id}.ohf")
        for i, opp in enumerate(tables):
            futs.append((c, ex.submit(simlib.run_table, ctx, str(f), HERO, opp, games, hands, seed + i)))
    for c, fut in futs:
        c.acc.merge(fut.result())


def save_state(run: Path, stage, gen, pop, args):
    (run / "state.json").write_text(json.dumps({"stage": stage, "gen": gen, "next_id": Cand._next, "pop": [c.to_json() for c in pop],
                                                "args": vars(args)}, indent=1), encoding="utf-8")


def save_best(run: Path, space, best: Cand, gen_global, stage, nstages, gen_in_stage, active, gens_per_stage):
    d = {"generation": gen_global, "stage": stage + 1, "stages": nstages, "gen_in_stage": gen_in_stage, "gens_per_stage": gens_per_stage,
         "active_genes": active, "mean_bb100": best.acc.mean, "ci95": best.acc.ci95, "hands": best.acc.hands,
         "genome": best.genome, "use_stats": space.use_stats, "style": STYLE, "format": FORMAT}
    (run / "best.json").write_text(json.dumps(d, indent=1), encoding="utf-8")
    simlib.write_profile(space.overrides(best.genome), STYLE, FORMAT, "OPT_BEST", run / "best.ohf")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pokersim", help="exécutable pokersim (avec le patch --json)")
    ap.add_argument("--oh-root", help="dossier OH15-by-nolog (contient OpenPPL/OpenPPL_Library)")
    ap.add_argument("--ohpg", help="dossier OpenHoldem-Profile-Generator-WIP")
    ap.add_argument("--pool", default="pool", help="dossier créé par make_pool.py")
    ap.add_argument("--run", default="runs/run1", help="dossier de sortie de cette optimisation")
    ap.add_argument("--gens", type=int, default=30, help="générations (par étape si --stages)")
    ap.add_argument("--mu", type=int, default=8, help="survivants")
    ap.add_argument("--lam", type=int, default=8, help="enfants par génération")
    ap.add_argument("--refine", type=int, default=3, help="nombre d'enfants qui passent à l'étape 2")
    ap.add_argument("--t1", type=int, default=4, help="évaluation courte : nombre de tables")
    ap.add_argument("--t2", type=int, default=10, help="évaluation longue : nombre de tables")
    ap.add_argument("--games", type=int, default=2, help="sessions par table à l'évaluation courte (x2 à la longue)")
    ap.add_argument("--hands", type=int, default=1000, help="mains par session")
    ap.add_argument("--k", type=float, default=1.0, help="score = moyenne - k x erreur-type")
    ap.add_argument("--sigma", type=float, default=0.10, help="mutation initiale (fraction de la plage du paramètre)")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--jobs", type=int, default=0, help="simulations en parallèle (0 = nb de coeurs)")
    ap.add_argument("--prwin-max", type=int, default=10000)
    ap.add_argument("--rake", type=float, default=0.0, help="rake en %% (défaut 0 : somme nulle)")
    ap.add_argument("--rake-cap", type=int, default=0, help="plafond du rake en jetons (BB = 10 jetons)")
    ap.add_argument("--use-stats", action="store_true", help="active use_stats et optimise aussi les paramètres d'exploitation")
    ap.add_argument("--groups", default="base", help="groupes de paramètres optimisés en une étape, séparés par des virgules (défaut : base)")
    ap.add_argument("--stages", help='étapes enchaînées : groupes séparés par des virgules, étapes séparées par des ";" (remplace --groups)')
    ap.add_argument("--genes", help="liste explicite de paramètres (une étape ; remplace --groups et --stages)")
    ap.add_argument("--list-groups", action="store_true", help="affiche les groupes et leurs paramètres (JSON) puis quitte")
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    simlib.load_ohpg(args.ohpg)
    from ohpg import params as ohparams
    if args.list_groups:
        print(json.dumps({n: {"help": GROUP_HELP[n], "genes": group_genes(ohparams, n)} for n in GROUP_NAMES}, ensure_ascii=False, indent=1))
        return
    if not args.pokersim or not args.oh_root:
        ap.error("--pokersim et --oh-root sont obligatoires")

    # ---- étapes : liste de listes de gènes
    if args.genes:
        stage_names, stage_genes = [["genes"]], [args.genes.split(",")]
    else:
        stage_names = parse_stages(args)
        if args.use_stats and not any("exploit" in st for st in stage_names):
            if len(stage_names) == 1:
                stage_names[0] = stage_names[0] + ["exploit"]
            else:
                stage_names.append(["exploit"])
        stage_genes = []
        for st in stage_names:
            gl = []
            for g in st:
                gl += [x for x in group_genes(ohparams, g) if x not in gl]
            stage_genes.append(gl)
    for gl in stage_genes:
        for g in gl:
            if g not in ohparams.SCHEMA_BY_KEY:
                raise SystemExit(f"paramètre inconnu : {g}")
    use_stats = args.use_stats or any("exploit" in st for st in stage_names)
    union = []
    for gl in stage_genes:
        union += [g for g in gl if g not in union]
    nst = len(stage_genes)

    pool = simlib.load_pool(args.pool)
    ctx = Ctx(args.pokersim, args.oh_root, args.pool, jobs=args.jobs, prwin_max=args.prwin_max,
              rake_pct=args.rake, rake_cap=args.rake_cap)
    space = Space(union, use_stats)
    run = Path(args.run)
    run.mkdir(parents=True, exist_ok=True)
    tmp = run / "tmp"

    si0, gen0, pop = 0, 0, []
    if args.resume and (run / "state.json").exists():
        st = json.loads((run / "state.json").read_text(encoding="utf-8"))
        si0, gen0, pop = st.get("stage", 0), st["gen"], [Cand.from_json(c) for c in st["pop"]]
        Cand._next = st["next_id"]
        print(f"reprise : étape {si0 + 1}/{nst}, génération {gen0}/{args.gens} ({len(pop)} survivants)")
    else:   # nouveau run : on repart d'un dossier propre (sinon la courbe et la validation d'un ancien run se mélangent)
        for name in ("state.json", "history.jsonl", "validation.json"):
            (run / name).unlink(missing_ok=True)

    t_start = time.time()
    with ThreadPoolExecutor(ctx.n_jobs()) as ex:
        for si in range(si0, nst):
            active = stage_genes[si]
            label = "+".join(stage_names[si])
            print(f"=== étape {si + 1}/{nst} : {label} ({len(active)} paramètres) ===", flush=True)
            if si == si0 and pop:
                gstart = gen0
            else:
                gstart = 0
                if not pop:   # tout début : presets + copies bruitées (mutation sur les gènes de l'étape)
                    rng = random.Random(args.seed)
                    seeds = [Cand(space.from_style(s), origin=f"preset {s}") for s in SEED_STYLES]
                    while len(seeds) < args.mu + args.lam:
                        parent = rng.choice(seeds[:len(SEED_STYLES)])
                        seeds.append(Cand(space.mutate(parent.genome, rng, args.sigma * 2, 0.4, active), origin="preset muté"))
                    tables = simlib.draw_tables(pool, "train", args.t1, args.seed * 7919)
                    eval_batch(ctx, ex, space, seeds, tables, args.games, args.hands, args.seed * 104729, tmp)
                    seeds.sort(key=lambda c: -c.acc.mean)
                    top = seeds[:max(args.mu, args.refine + 2)]       # seuls les candidats mesurés longuement peuvent survivre
                    tables2 = simlib.draw_tables(pool, "train", args.t2, args.seed * 7919 + 777)
                    eval_batch(ctx, ex, space, top, tables2, args.games * 2, args.hands, args.seed * 104729 + 5000, tmp)
                    pop = sorted(top, key=lambda c: -c.score(args.k))[:args.mu]
                else:         # étape suivante : on repart des survivants, réévalués sur de nouvelles tables (scores comparables)
                    for c in pop:
                        c.acc = Acc()
                    tables2 = simlib.draw_tables(pool, "train", args.t2, args.seed * 7919 + 777 + 31 * si)
                    eval_batch(ctx, ex, space, pop, tables2, args.games * 2, args.hands, args.seed * 104729 + 5000 + 977 * si, tmp)
                    pop = sorted(pop, key=lambda c: -c.score(args.k))
                save_state(run, si, 0, pop, args)
                save_best(run, space, pop[0], si * args.gens, si, nst, 0, label, args.gens)
                print(f"étape {si + 1} : départ | meilleur : {pop[0].origin} {pop[0].acc}", flush=True)

            for gen in range(gstart + 1, args.gens + 1):
                rng = random.Random(args.seed * 1000 + si * 100003 + gen)
                sigma = args.sigma * (1 - 0.7 * (gen - 1) / max(1, args.gens - 1))   # mutation décroissante : 100 % -> 30 %
                kids = []
                for _ in range(args.lam):
                    a = min(rng.sample(pop, min(2, len(pop))), key=lambda c: -c.score(args.k))
                    b = min(rng.sample(pop, min(2, len(pop))), key=lambda c: -c.score(args.k))
                    g = space.cross(a.genome, b.genome, rng, active) if rng.random() < 0.6 else dict(a.genome)
                    kids.append(Cand(space.mutate(g, rng, sigma, 0.3, active), origin=f"s{si + 1}g{gen}"))
                gseed = args.seed * 104729 + si * 7000003 + gen * 10000
                tables = simlib.draw_tables(pool, "train", args.t1, gseed)
                eval_batch(ctx, ex, space, kids, tables, args.games, args.hands, gseed, tmp)
                kids.sort(key=lambda c: -c.acc.mean)
                tables2 = simlib.draw_tables(pool, "train", args.t2, gseed + 777)
                eval_batch(ctx, ex, space, kids[:args.refine], tables2, args.games * 2, args.hands, gseed + 5000, tmp)
                # successive halving : seuls les enfants qui ont reçu l'évaluation longue concourent (un enfant mesuré sur peu de mains
                # peut avoir un score flatteur par hasard)
                pop = sorted(pop + kids[:args.refine], key=lambda c: -c.score(args.k))[:args.mu]
                gglobal = si * args.gens + gen
                save_state(run, si, gen, pop, args)
                save_best(run, space, pop[0], gglobal, si, nst, gen, label, args.gens)
                with open(run / "history.jsonl", "a", encoding="utf-8") as fh:
                    fh.write(json.dumps({"gen": gglobal, "stage": si + 1, "gen_in_stage": gen, "best": pop[0].to_json(),
                                         "survivors": [(c.id, round(c.acc.mean, 2), c.acc.n) for c in pop]}) + "\n")
                entered = sum(1 for c in pop if c.origin == f"s{si + 1}g{gen}")
                el = (time.time() - t_start) / 60
                print(f"gen {gglobal}/{nst * args.gens} (étape {si + 1}/{nst}, {gen}/{args.gens}) | meilleur : {pop[0].acc} | "
                      f"{entered} nouveau(x) dans les survivants | {el:.1f} min", flush=True)
            if si + 1 < nst:
                pop = sorted(pop, key=lambda c: -c.score(args.k))
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"terminé. Meilleur profil : {run / 'best.ohf'} (paramètres : {run / 'best.json'})\nÀ valider avec : python validate.py --run {run} ...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\ninterrompu : relance avec --resume pour reprendre à la dernière génération sauvegardée")
