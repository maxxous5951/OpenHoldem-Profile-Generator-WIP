# Tester le profil dans OpenHoldem (checklist)

Le generateur est teste par un simulateur OpenPPL, pas par OpenHoldem lui-meme. Cette checklist verifie le comportement reel.

1. **Chargement** : File > Open le `.ohf`. Aucune erreur de syntaxe ne doit apparaitre (le generateur valide deja le profil).
2. **Symboles PokerTracker** (seulement si `use_stats` est actif) :
   - `python -m ohpg pt-symbols --set use_stats=true` liste les symboles `pt_*` utilises.
   - Dans OpenHoldem, ouvre la fenetre des symboles avec PokerTracker connecte : chacun doit renvoyer une valeur (pas d'erreur).
   - Si l'un manque, desactive `use_stats` ou ouvre un ticket avec le nom du symbole.
3. **Table de test** : joue 200 a 300 mains en jeu fictif / tables a faibles enjeux avec le log d'OpenHoldem active.
4. **Comparer** : pour une main douteuse, note la position, le stack, les actions devant toi, puis lance
   `python -m ohpg explain --hand AKs --pos BB --scenario "Face a une ouverture 2.5 BB" --stack 40` (ou l'onglet *Simulateur* de la GUI).
   L'action du simulateur doit correspondre au log ; sinon note la situation et signale-la.
5. **Points a regarder en priorite** : positions selon la taille de table (3-max sans CO/MP/EP), 3bet/4bet (`Raises`), tailles de relance (`RaiseTo` en BB), zone push/fold et open-jam, limp du SB en 3-max.
6. **Limites du simulateur** : le postflop (board, tirages, texture) n'est pas simule, seul le preflop l'est.
