# Optimiseur de profils

Cherche automatiquement un profil `ohpg` qui bat un pool de bots, en le faisant jouer dans le simulateur
[PokerSim](https://github.com/maxxous5951/OH15-by-nolog) (branche `gui-optimizer`, qui ajoute aussi un onglet « Optimisation » pilotant ces scripts).

1. Un jeu de paramètres `ohpg` donne un profil candidat (`.ohf`).
2. `pokersim` le fait jouer contre 5 bots tirés dans le pool d'entraînement.
3. Sélection selon le bb/100 et son intervalle de confiance, croisement, mutation, génération suivante.
4. Validation finale sur des bots **jamais vus** pendant la recherche, comparée aux 6 presets d'`ohpg`.

## Prérequis

- Python 3.10+ (aucune dépendance : bibliothèque standard seulement).
- `pokersim` avec l'option `--json` : branche `gui-optimizer` de `OH15-by-nolog` (ou `git apply patches/0001-pokersim-cli-json.patch` sur `pokersim-cpp`, puis recompiler).
- Le dépôt `OH15-by-nolog` (racine OpenHoldem : `OpenPPL/OpenPPL_Library`).
- `ohpg` est trouvé automatiquement (le dossier parent de `optimizer/`) ; sinon `--ohpg DOSSIER` ou la variable `OHPG_PATH`.

## Utilisation

```
cd optimizer
python make_pool.py --out pool --seed 1        # 15 bots reproductibles (10 entraînement, 5 validation)
python optimize.py --pokersim /chemin/pokersim --oh-root /chemin/OH15-by-nolog --pool pool --run runs/run1 --gens 30
                                               # Ctrl+C puis --resume pour reprendre
python validate.py --pokersim /chemin/pokersim --oh-root /chemin/OH15-by-nolog --pool pool --run runs/run1 --tables 30 --games 10 --hands 2000
```

- **Pool** : Balanced (2), TAG (3), LAG (3), Nit (2), Maniac (2), Calling Station (3). Chaque variante perturbe ~85 paramètres de style de ±15 à ±35 %. Validation : BAL_2, TAG_3, LAG_3, NIT_2, FISH_3 (jamais utilisés par `optimize.py`). Détail : `pool/pool.json`.
- **Boucle** : génération 0 = les 6 presets + copies mutées ; ensuite croisement + mutation, étape 1 (tables courtes) sur tous les enfants, étape 2 (gros volume) sur les `--refine` meilleurs. Score = moyenne - k x erreur-type (`--k`, défaut 1).
- **Gènes** : `--groups base` (23 paramètres, défaut), `all` (87) ou une liste de groupes : `open, defense, big, flop, turn, river, sizes, global, exploit` (`--list-groups` les affiche). `--stages "open,defense,big;flop,turn,river;sizes,global"` optimise par étapes : `--gens` générations par étape, chaque étape repart des meilleurs de la précédente (ré-évalués sur de nouvelles tables). `--genes a,b,c` choisit à la main ; `--use-stats` active `use_stats` et ajoute les 16 paramètres `exploit` (une étape de plus en mode par étapes).
- **Sélection** : élimination successive (un enfant n'est classé que s'il a été affiné sur beaucoup de mains). Un nouveau run efface l'ancien `history.jsonl` et `validation.json`.
- **Rake** : 0 par défaut (somme nulle : bb/100 > 0 = bat le champ). `--rake 5 --rake-cap 30` pour un rake réaliste.
- **Sorties** (dans `--run`) : `best.ohf` (meilleur profil), `best.json` (ses paramètres), `history.jsonl`, `state.json` (reprise), `validation.json`.

## Vitesse et précision

~3 200 mains/s sur 2 coeurs (cash 6-max, PokerTracker simulé actif) ; les profils générés n'appellent pas `prwin`, donc son plafond est sans effet. Sur 8 000 mains l'intervalle de confiance est d'environ ±30 bb/100 ;
il faut de l'ordre de 2 millions de mains pour descendre vers ±2 bb/100.

## Limites

- Un profil qui bat le pool ne bat pas forcément de vrais joueurs : seule la validation sur les bots jamais vus a un sens, et elle reste un champ simulé.
- Les variantes ne couvrent que ce que permettent les paramètres d'`ohpg` (tailles de mise en pourcentages fixes, `use_stats` limité à nit / fish / maniaque).
- Pas encore de mains dupliquées (mêmes cartes, places permutées) pour réduire la variance.
- Les sites de poker en ligne interdisent généralement les bots : usage hors-ligne, recherche et tests uniquement.
