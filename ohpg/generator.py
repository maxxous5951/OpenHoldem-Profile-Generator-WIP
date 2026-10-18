"""Assemblage du profil complet."""
from __future__ import annotations

from datetime import date

from . import __version__
from .params import normalize
from .ppl import Profile
from .strategy import hopper, postflop, preflop
from .validator import Issue, errors, validate

HEADER = """//*****************************************************************************
//  {name}
//  Généré par OpenHoldem Profile Generator (ohpg) v{version} le {today}
//
//  Format : {game}, {table_size} joueurs, ante {ante_bb} BB
//  Prérequis : charger la bibliothèque OpenPPL officielle (OpenPPL_Library) avant ce fichier.
//  Ce profil ne redéfinit AUCUN symbole de la bibliothèque ; ses fonctions auxiliaires sont préfixées f$Gen_.
//  Stratégie mixte : randomhand / randomround (valeurs 0..1 d'OpenHoldem).
//*****************************************************************************
"""


def generate(overrides: dict | None = None) -> str:
    cfg = normalize(overrides)
    prof = Profile()
    prof.header = HEADER.format(version=__version__, today=date.today().isoformat(), **cfg).rstrip().split("\n")
    preflop.generate(prof, cfg)
    postflop.generate(prof, cfg)
    hopper.generate(prof, cfg)
    return prof.render()


def generate_checked(overrides: dict | None = None) -> tuple[str, list[Issue]]:
    text = generate(overrides)
    return text, validate(text)


def generate_strict(overrides: dict | None = None) -> str:
    text, issues = generate_checked(overrides)
    errs = errors(issues)
    if errs:
        raise RuntimeError("profil invalide :\n" + "\n".join(str(e) for e in errs[:30]))
    return text
