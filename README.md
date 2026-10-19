# OpenHoldem Profile Generator (ohpg) v2

Générateur de profils **OpenHoldem / OpenPPL** : tu règles des paramètres de stratégie (ranges, fréquences, tailles, push/fold…), il produit un fichier `.ohf` **validé symbole par symbole** contre la bibliothèque OpenPPL officielle.

## Pourquoi cette v2
- **Syntaxe vérifiée** : le validateur contrôle chaque symbole (≈1 100 fonctions de la bibliothèque OpenPPL + symboles intégrés d'OpenHoldem), la structure `WHEN … FORCE`, les doublons, les handlists. Un profil invalide n'est jamais écrit.
- **Aucune redéfinition de la bibliothèque** : les fonctions auxiliaires sont préfixées `f$Gen_`.
- **Ranges réelles** : classement des 169 mains par équité (Monte Carlo, `tools/compute_hand_ranking.py`) + ordre de jouabilité ; ranges exportées en **handlists** (`##listXxx##`).
- **Stratégie mixte** : `randomhand` / `randomround` (0..1) pour jouer les mains limites à fréquence partielle, bluffs polarisés (A5s…, blockers), ratio value/bluff réglable.
- **Postflop par catégories de mains** (monstre, forte, moyenne, tirage fort/faible, paire faible, rien) × texture du board × IP/OOP × multiway, défense basée sur les **cotes du pot** (MDF).
- **Préflop complet** : ouverture par poste, isolation, défense vs ouverture selon le poste de l'ouvreur, BB defense, squeeze, 4bet/5bet, calls d'all-in selon la profondeur.
- **Tournoi** : push/fold par profondeur et poste, reshove, ante, pression ICM à la bulle (`IsBubble`).
- **Situations couvertes, vérifiées par balayage exhaustif** (`tests/test_coverage.py`) : ouverture, limpers, vs ouverture, squeeze, vs 3bet/4bet/5bet/all-in, limp/call puis relance, pots ouverts/3bet/4bet (SPR et engagement du tapis), c-bet / 2e et 3e barrel / probe / donk, check-raise planifié, face à un all-in, multiway, heads-up. Positions adaptées à la taille de table (2 à 10 joueurs).
- **Exploitation des adversaires** (option `use_stats`) : classification nit / fish / maniaque via les stats PokerTracker d'OpenHoldem (`pt_*`) et ajustement des ranges préflop, des bluffs et de la tolérance de call.
- **120 paramètres** décrits dans un schéma unique (`ohpg/params.py`) qui alimente la CLI, les presets et la GUI.

## Installation
```bash
pip install -e .            # noyau, sans dépendance
pip install -e ".[gui]"     # + interface PyQt6
```

## Utilisation
```bash
python -m ohpg generate --style LAG --format "Cash 6-max" -o lag.ohf
python -m ohpg generate --style TAG --format "MTT 9-max (push/fold 15BB)" --set icm_pressure=60 --set ante_bb=0.12 -o mtt.ohf
python -m ohpg validate mon_profil.ohf --partial     # valide n'importe quel .ohf
python -m ohpg list                                   # presets et paramètres
python -m ohpg dump-config --style Nit > config.json  # puis --config config.json
python -m ohpg gui   # ou double-clic sur lancer.bat                                    # interface graphique
```
Presets de style : Balanced 6-max, TAG, LAG, Nit, Maniac, Calling Station, Exploit vs Passive.
Formats : Cash 6-max, Full Ring, Heads-Up, MTT 9-max, SNG bubble, Spin & Go 3-max.

Dans OpenHoldem : charger la **bibliothèque OpenPPL officielle**, puis le `.ohf` généré (il définit `f$preflop`, `f$flop`, `f$turn`, `f$river` et les hooks optionnels).

## Architecture
```
ohpg/params.py        schéma des paramètres (source de vérité)
ohpg/presets.py       styles + formats
ohpg/ranges.py        classement des mains, ranges %, value/bluff/call disjoints, notation "AA-TT,AKs+"
ohpg/ppl.py           émetteur OpenPPL (Profile, Func, handlists dédupliquées)
ohpg/strategy/        preflop, pushfold, postflop, hopper, common
ohpg/validator.py     validation structure + symboles
ohpg/generator.py     assemblage
ohpg/gui/app.py       GUI auto-générée depuis le schéma
tests/                pytest + mini-simulateur OpenPPL (tests/sim.py) pour tester les décisions
examples/             profils générés prêts à charger
```

## Limites connues (honnêteté)
- Non testé **dans OpenHoldem lui-même** (Windows) : la validation garantit que les symboles existent dans la bibliothèque officielle, pas leur comportement exact sur chaque table. Charge le profil et utilise le vérificateur de syntaxe d'OpenHoldem.
- Les ranges de push/fold sont des **approximations** de Nash sans ICM complet, pas des solutions solveur. Règle-les avec `pf_scale`, `pf_call_scale`, `icm_pressure`.
- Le classement des mains est basé sur l'équité contre une main aléatoire + jouabilité, pas sur des ranges solveur.
- L'exploitation `use_stats` exige PokerTracker configuré dans OpenHoldem (HEM non géré) ; les noms `pt_*` viennent de la documentation officielle mais n'ont pas pu être exécutés ici. Sans base ou avec trop peu de mains, le profil reste neutre.
- Les tailles de mise ne varient pas selon l'adversaire (non implémenté : les tailles sont des pourcentages fixes).
- Les sites de poker en ligne interdisent généralement les bots : utilise ce projet uniquement là où c'est légal et autorisé (jeu hors-ligne, tests, recherche).

## Développement
```bash
pip install -e ".[dev]" && pytest
python tools/compute_hand_ranking.py 60000   # recalcule le classement des 169 mains
```
Licence : MIT.
