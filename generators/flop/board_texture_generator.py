"""
Générateur pour l'analyse de texture du board au flop
Implémentation améliorée avec une classification détaillée des textures
"""
from generators.flop.base_generator import BaseFlopGenerator

class BoardTextureGenerator(BaseFlopGenerator):
    """
    Classe pour générer les fonctions d'analyse de texture du board au flop
    Version améliorée avec classifications détaillées des textures de board
    """
    
    def generate_code(self, settings):
        """
        Génère les fonctions de texture du board pour le profil flop
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code généré pour l'analyse de texture du board
        """
        # Extraire les ajustements spécifiques aux textures
        monotone_board_adjust = settings.get("monotone_board_adjust", -25) / 100.0
        paired_board_adjust = settings.get("paired_board_adjust", 15) / 100.0
        connected_board_adjust = settings.get("connected_board_adjust", -20) / 100.0
        high_card_board_adjust = settings.get("high_card_board_adjust", 10) / 100.0
        low_card_board_adjust = settings.get("low_card_board_adjust", 20) / 100.0
        dynamic_board_adjust = settings.get("dynamic_board_adjust", -30) / 100.0
        static_board_adjust = settings.get("static_board_adjust", 25) / 100.0
        
        code = "//*****************************************************************************\n"
        code += "//\n"
        code += "// BOARD TEXTURE ANALYSIS FUNCTIONS\n"
        code += "//\n"
        code += "// Advanced classification of board textures for precise strategy adjustments\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"
        
        # CLASSIFICATION DE BASE : DRY VS WET
        
        # Dry Board Function - inchangée
        code += "##f$DryBoard##\n"
        code += "// A dry board has few draws and is disconnected\n"
        code += "WHEN FlushPossible RETURN false FORCE\n"
        code += "WHEN StraightPossible RETURN false FORCE\n"
        code += "WHEN nsuitedcommon >= 2 RETURN false FORCE\n"
        code += "WHEN (TopFlopCard - LowestFlopCard) <= 4 AND (TopFlopCard - LowestFlopCard) > 1 RETURN false FORCE\n"
        code += "WHEN PairOnBoard RETURN false FORCE\n"
        code += "WHEN Others RETURN true FORCE\n\n"

        # Wet Board Function - inchangée
        code += "##f$WetBoard##\n"
        code += "// A wet board has many draws and connected cards\n"
        code += "WHEN FlushPossible OR FlushDrawPossible RETURN true FORCE\n"
        code += "WHEN StraightPossible RETURN true FORCE\n"
        code += "WHEN OpenEndedStraightDrawPossibleOnFlop RETURN true FORCE\n"
        code += "WHEN (TopFlopCard - LowestFlopCard) <= 4 AND (TopFlopCard - LowestFlopCard) > 1 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # CLASSIFICATION AVANCÉE PAR MOTIF
        
        # Monotone Board (3 cartes de la même couleur)
        code += "##f$MonotoneBoard##\n"
        code += "// Board where all cards are the same suit\n"
        code += "WHEN nsuitedcommon = 3 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Two-tone Board (2 cartes de la même couleur)
        code += "##f$TwoToneBoard##\n"
        code += "// Board where two cards are the same suit\n"
        code += "WHEN nsuitedcommon = 2 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Rainbow Board (3 couleurs différentes)
        code += "##f$RainbowBoard##\n"
        code += "// Board with three different suits\n"
        code += "WHEN nsuitedcommon = 1 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Paired Board (une paire sur le board)
        code += "##f$PairedBoard##\n"
        code += "// Board with a pair\n"
        code += "WHEN PairOnBoard RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Connected Board (3 cartes consécutives)
        code += "##f$ConnectedBoard##\n"
        code += "// Board with connected cards (exactly consecutive)\n"
        code += "WHEN nstraightcommon = 3 RETURN true FORCE\n"
        code += "WHEN (TopFlopCard - f$MiddleFlopCard = 1) AND (f$MiddleFlopCard - LowestFlopCard = 1) RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Semi-Connected Board (cartes avec 1 gap maximum)
        code += "##f$SemiConnectedBoard##\n"
        code += "// Board with semi-connected cards (1 gap max)\n"
        code += "WHEN (TopFlopCard - f$MiddleFlopCard <= 2) AND (f$MiddleFlopCard - LowestFlopCard <= 2) RETURN true FORCE\n"
        code += "WHEN (TopFlopCard - LowestFlopCard <= 4) AND NOT f$ConnectedBoard RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # CLASSIFICATION PAR HAUTEUR DES CARTES
        
        # High Card Board (A, K ou Q sur le flop)
        code += "##f$HighCardBoard##\n"
        code += "// Board with high cards (A, K, Q)\n"
        code += "WHEN rankhicommon >= queen RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Broadway Board (uniquement des cartes T+)
        code += "##f$BroadwayBoard##\n"
        code += "// Board with only Broadway cards (T or higher)\n"
        code += "WHEN LowestFlopCard >= ten RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Low Card Board (uniquement des cartes 9-)
        code += "##f$LowCardBoard##\n"
        code += "// Board with only low cards (9 or lower)\n"
        code += "WHEN TopFlopCard <= 9 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Middle Card Board (uniquement des cartes moyennes T-5)
        code += "##f$MiddleCardBoard##\n"
        code += "// Board with only middle cards (T-5)\n"
        code += "WHEN TopFlopCard <= ten AND LowestFlopCard >= 5 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Fonction auxiliaire pour la carte du milieu
        code += "##f$MiddleFlopCard##\n"
        code += "// Returns the middle ranked card on the flop\n"
        code += "WHEN ($$cr0 > $$cr1 AND $$cr0 < $$cr2) OR ($$cr0 < $$cr1 AND $$cr0 > $$cr2) RETURN $$cr0 FORCE\n"
        code += "WHEN ($$cr1 > $$cr0 AND $$cr1 < $$cr2) OR ($$cr1 < $$cr0 AND $$cr1 > $$cr2) RETURN $$cr1 FORCE\n"
        code += "WHEN Others RETURN $$cr2 FORCE\n\n"
        
        # Fonction auxiliaire pour le rang de la paire sur le board
        code += "##f$PairOnBoardRank##\n"
        code += "// Returns the rank of the paired card on the board, or 0 if no pair\n"
        code += "WHEN $$cr0 = $$cr1 RETURN $$cr0 FORCE\n"
        code += "WHEN $$cr0 = $$cr2 RETURN $$cr0 FORCE\n"
        code += "WHEN $$cr1 = $$cr2 RETURN $$cr1 FORCE\n"
        code += "WHEN PairOnBoard AND $$cr3 = $$cr0 RETURN $$cr0 FORCE\n"
        code += "WHEN PairOnBoard AND $$cr3 = $$cr1 RETURN $$cr1 FORCE\n"
        code += "WHEN PairOnBoard AND $$cr3 = $$cr2 RETURN $$cr2 FORCE\n"
        code += "WHEN PairOnBoard AND $$cr4 = $$cr0 RETURN $$cr0 FORCE\n"
        code += "WHEN PairOnBoard AND $$cr4 = $$cr1 RETURN $$cr1 FORCE\n"
        code += "WHEN PairOnBoard AND $$cr4 = $$cr2 RETURN $$cr2 FORCE\n"
        code += "WHEN PairOnBoard AND $$cr4 = $$cr3 RETURN $$cr3 FORCE\n"
        code += "WHEN Others RETURN 0 FORCE\n\n"
        
        # Fonction pour vérifier si un straight draw est possible
        code += "##f$StraightDrawPossible##\n"
        code += "// Checks if a straight draw is possible on the board\n"
        code += "WHEN nstraightfill <= 2 RETURN true FORCE\n"
        code += "WHEN nstraightfillcommon <= 1 RETURN true FORCE\n"
        code += "WHEN StraightPossible RETURN true FORCE\n"
        code += "WHEN OpenEndedStraightDrawPossibleOnFlop RETURN true FORCE\n"
        code += "WHEN nstraightcommon >= 2 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # CLASSIFICATION PAR POTENTIEL DE DRAW
        
        # Dynamic Board (beaucoup de possibilités de draw)
        code += "##f$DynamicBoard##\n"
        code += "// Board with many possible draws\n"
        code += "WHEN f$WetBoard AND FlushDrawPossible RETURN true FORCE\n"
        code += "WHEN f$WetBoard AND OpenEndedStraightDrawPossibleOnFlop RETURN true FORCE\n"
        code += "WHEN f$SemiConnectedBoard AND f$TwoToneBoard RETURN true FORCE\n"
        code += "WHEN (TopFlopCard - LowestFlopCard) <= 3 AND nsuitedcommon >= 2 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Static Board (peu de possibilités de draw)
        code += "##f$StaticBoard##\n"
        code += "// Board with few possible draws\n"
        code += "WHEN NOT FlushDrawPossible AND NOT f$StraightDrawPossible RETURN true FORCE\n"
        code += "WHEN f$RainbowBoard AND (TopFlopCard - LowestFlopCard) > 4 RETURN true FORCE\n"
        code += "WHEN f$RainbowBoard AND f$PairedBoard RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # EVALUATION DES RISQUES SPÉCIFIQUES
        
        # Board avec des risques de straight draw
        code += "##f$StraightDrawHeavyBoard##\n"
        code += "// Board with significant straight draw potential\n"
        code += "WHEN f$ConnectedBoard RETURN true FORCE\n"
        code += "WHEN f$SemiConnectedBoard AND NOT f$HighCardBoard RETURN true FORCE\n"
        code += "WHEN (TopFlopCard - LowestFlopCard) <= 4 AND TopFlopCard <= jack RETURN true FORCE\n"
        code += "WHEN nstraightfill <= 1 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Board avec des risques de flush draw
        code += "##f$FlushDrawHeavyBoard##\n"
        code += "// Board with significant flush draw potential\n"
        code += "WHEN f$TwoToneBoard RETURN true FORCE\n"
        code += "WHEN nsuitedcommon >= 2 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Board avec position bloquée (difficult to improve or bluff)
        code += "##f$LockedBoard##\n"
        code += "// Board that is difficult to bluff or improve on\n"
        code += "WHEN f$PairedBoard AND f$HighCardBoard RETURN true FORCE\n"
        code += "WHEN f$MonotoneBoard AND NOT f$ConnectedBoard RETURN true FORCE\n"
        code += "WHEN f$BroadwayBoard AND f$RainbowBoard AND NOT f$ConnectedBoard RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # FONCTIONS D'ANALYSE POSITIONNELLE
        
        # Board qui favorise le preflop raiser
        code += "##f$RaiserFavorableBoard##\n"
        code += "// Board that favors the preflop raiser's range\n"
        code += "WHEN f$HighCardBoard AND f$StaticBoard RETURN true FORCE\n"
        code += "WHEN f$BroadwayBoard RETURN true FORCE\n"
        code += "WHEN f$PairedBoard AND rankhicommon >= ten RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Board qui favorise le caller
        code += "##f$CallerFavorableBoard##\n"
        code += "// Board that favors the caller's range\n"
        code += "WHEN f$LowCardBoard AND f$ConnectedBoard RETURN true FORCE\n"
        code += "WHEN f$PairedBoard AND rankhicommon <= 9 RETURN true FORCE\n"
        code += "WHEN f$MiddleCardBoard AND f$ConnectedBoard RETURN true FORCE\n"
        code += "WHEN f$MonotoneBoard AND rankhicommon <= ten RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # FONCTIONS D'ÉVALUATION CONTEXTUELLE DES MAINS
        
        # Évaluation des mains sur board monotone
        code += "##f$HandStrengthOnMonotoneBoard##\n"
        code += "// Evaluates hand strength on monotone boards\n"
        code += "WHEN HaveFlush RETURN 5 FORCE\n"
        code += "WHEN HaveSet RETURN 4 FORCE\n"
        code += "WHEN HaveTwoPair RETURN 3 FORCE\n"
        code += "WHEN HavePair AND (FirstHoleCardSuit = DominantSuitCommon OR SecondHoleCardSuit = DominantSuitCommon) RETURN 2 FORCE\n"
        code += "WHEN FirstHoleCardSuit = DominantSuitCommon AND SecondHoleCardSuit = DominantSuitCommon RETURN 1 FORCE\n"
        code += "WHEN Others RETURN 0 FORCE\n\n"
        
        # Évaluation des mains sur board paired
        code += "##f$HandStrengthOnPairedBoard##\n"
        code += "// Evaluates hand strength on paired boards\n"
        code += "WHEN HaveFullHouse RETURN 5 FORCE\n"
        code += "WHEN HaveTrips RETURN 4 FORCE\n"
        code += "WHEN HaveTwoPair RETURN 3 FORCE\n"
        code += "WHEN HaveOverPair RETURN 2 FORCE\n"
        code += "WHEN HavePair AND rankhiplayer > f$PairOnBoardRank RETURN 1 FORCE\n"
        code += "WHEN Others RETURN 0 FORCE\n\n"
        
        # Évaluation des mains sur board connected
        code += "##f$HandStrengthOnConnectedBoard##\n"
        code += "// Evaluates hand strength on connected boards\n"
        code += "WHEN HaveStraight RETURN 5 FORCE\n"
        code += "WHEN HaveSet RETURN 4 FORCE\n"
        code += "WHEN HaveTwoPair RETURN 3 FORCE\n"
        code += "WHEN HaveOpenEndedStraightDraw AND HaveOverPair RETURN 2 FORCE\n" 
        code += "WHEN HaveOpenEndedStraightDraw OR HaveOverPair RETURN 1 FORCE\n"
        code += "WHEN Others RETURN 0 FORCE\n\n"
        
        # RAPPORTS DE BLUFF VS VALEUR PAR TEXTURE
        
        # Rapport optimal bluff/value sur board monotone
        code += "##f$BluffValueRatioMonotone##\n"
        code += "// Optimal bluff-to-value ratio on monotone boards\n"
        code += f"// Apply {monotone_board_adjust*100:.0f}% adjustment to C-Bet frequencies\n"
        code += "WHEN Others RETURN 0.3 FORCE\n\n"
        
        # Rapport optimal bluff/value sur board paired
        code += "##f$BluffValueRatioPaired##\n"
        code += "// Optimal bluff-to-value ratio on paired boards\n"
        code += f"// Apply {paired_board_adjust*100:.0f}% adjustment to C-Bet frequencies\n"
        code += "WHEN Others RETURN 0.6 FORCE\n\n"
        
        # Rapport optimal bluff/value sur board connected
        code += "##f$BluffValueRatioConnected##\n"
        code += "// Optimal bluff-to-value ratio on connected boards\n"
        code += f"// Apply {connected_board_adjust*100:.0f}% adjustment to C-Bet frequencies\n"
        code += "WHEN Others RETURN 0.4 FORCE\n\n"
        
        # Rapport optimal bluff/value sur board avec cartes hautes
        code += "##f$BluffValueRatioHighCard##\n"
        code += "// Optimal bluff-to-value ratio on high card boards\n"
        code += f"// Apply {high_card_board_adjust*100:.0f}% adjustment to C-Bet frequencies\n"
        code += "WHEN Others RETURN 0.7 FORCE\n\n"
        
        # Rapport optimal bluff/value sur board avec cartes basses
        code += "##f$BluffValueRatioLowCard##\n"
        code += "// Optimal bluff-to-value ratio on low card boards\n"
        code += f"// Apply {low_card_board_adjust*100:.0f}% adjustment to C-Bet frequencies\n"
        code += "WHEN Others RETURN 0.5 FORCE\n\n"
        
        # FONCTIONS DE DETECTION DE CBET FAVORABLE
        
        # Board favorable pour C-bet
        code += "##f$FavorableCBetBoard##\n"
        code += "// Board where c-betting is generally favorable\n"
        code += "WHEN f$StaticBoard AND f$RaiserFavorableBoard RETURN true FORCE\n"
        code += "WHEN f$HighCardBoard AND f$StaticBoard RETURN true FORCE\n"
        code += "WHEN f$PairedBoard AND NOT f$CallerFavorableBoard RETURN true FORCE\n"
        code += "WHEN f$RainbowBoard AND NOT f$ConnectedBoard RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Board défavorable pour C-bet
        code += "##f$UnfavorableCBetBoard##\n"
        code += "// Board where c-betting should be done cautiously\n"
        code += "WHEN f$DynamicBoard AND f$CallerFavorableBoard RETURN true FORCE\n"
        code += "WHEN f$MonotoneBoard AND f$LowCardBoard RETURN true FORCE\n"
        code += "WHEN f$ConnectedBoard AND f$LowCardBoard RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # AJUSTEMENTS DE SIZING PAR TEXTURE
        
        # Sizing recommandé pour c-bet selon texture
        code += "##f$RecommendedCBetSizing##\n"
        code += "// Recommends C-bet sizing based on board texture (in % of pot)\n"
        code += "WHEN f$MonotoneBoard RETURN 75 FORCE\n"
        code += "WHEN f$PairedBoard RETURN 50 FORCE\n"
        code += "WHEN f$StaticBoard AND f$HighCardBoard RETURN 33 FORCE\n"
        code += "WHEN f$DynamicBoard RETURN 66 FORCE\n"
        code += "WHEN f$FavorableCBetBoard RETURN 50 FORCE\n"
        code += "WHEN f$UnfavorableCBetBoard RETURN 33 FORCE\n"
        code += "WHEN Others RETURN 50 FORCE\n\n"
        
        # FONCTIONS D'ÉVALUATION DE CONTINUITÉ
        
        # Indicateur d'équité très polarisée
        code += "##f$PolarizedEquity##\n"
        code += "// Indicates boards where equity is highly polarized\n"
        code += "WHEN f$MonotoneBoard RETURN true FORCE\n"
        code += "WHEN f$ConnectedBoard AND f$HighCardBoard RETURN true FORCE\n"
        code += "WHEN f$PairedBoard AND f$HighCardBoard RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Indicateur d'équité assez linéaire
        code += "##f$LinearEquity##\n"
        code += "// Indicates boards where equity is more linear\n"
        code += "WHEN f$RainbowBoard AND f$StaticBoard RETURN true FORCE\n"
        code += "WHEN f$RainbowBoard AND f$HighCardBoard AND NOT f$ConnectedBoard RETURN true FORCE\n"
        code += "WHEN NOT f$PolarizedEquity RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # CLASSIFICATEURS MULTIWAY
        
        # Board approprié pour multiway c-bet
        code += "##f$GoodMultiwayBoard##\n"
        code += "// Board that is favorable for C-betting in multiway pots\n"
        code += "WHEN f$StaticBoard AND f$HighCardBoard RETURN true FORCE\n"
        code += "WHEN f$PairedBoard AND f$RaiserFavorableBoard RETURN true FORCE\n"
        code += "WHEN f$LockedBoard RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Board risqué pour multiway c-bet
        code += "##f$RiskyMultiwayBoard##\n"
        code += "// Board that is risky for C-betting in multiway pots\n"
        code += "WHEN f$DynamicBoard RETURN true FORCE\n"
        code += "WHEN f$ConnectedBoard RETURN true FORCE\n"
        code += "WHEN f$StraightDrawHeavyBoard RETURN true FORCE\n"
        code += "WHEN f$FlushDrawHeavyBoard RETURN true FORCE\n"
        code += "WHEN f$CallerFavorableBoard RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # CLASSIFICATEURS DE DONK BET
        
        # Board favorable au donk bet
        code += "##f$GoodDonkBetBoard##\n"
        code += "// Board where donk betting can be profitable\n"
        code += "WHEN f$CallerFavorableBoard AND f$DynamicBoard RETURN true FORCE\n"
        code += "WHEN f$MonotoneBoard AND f$LowCardBoard RETURN true FORCE\n"
        code += "WHEN f$ConnectedBoard AND f$LowCardBoard RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Board favorable au check-raise
        code += "##f$GoodCheckRaiseBoard##\n"
        code += "// Board where check-raising can be profitable\n"
        code += "WHEN f$DynamicBoard RETURN true FORCE\n"
        code += "WHEN f$CallerFavorableBoard AND nopponentsplaying <= 2 RETURN true FORCE\n"
        code += "WHEN f$ConnectedBoard AND nopponentsplaying <= 2 RETURN true FORCE\n"
        code += "WHEN f$MonotoneBoard AND f$LowCardBoard RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        return code
