"""
Générateur principal pour le profil flop OpenHoldem
Coordonne les générateurs spécialisés et utilise toutes les fonctions avancées
"""
from generators.flop.base_generator import BaseFlopGenerator
from generators.flop.cbet_generator import CBetGenerator
from generators.flop.facing_bets_generator import FacingBetsGenerator
from generators.flop.board_texture_generator import BoardTextureGenerator
from generators.flop.hand_categories_generator import HandCategoriesGenerator

class FlopProfileGenerator(BaseFlopGenerator):
    """
    Classe principale pour générer le profil flop complet
    Coordonne les différents générateurs spécialisés
    Version améliorée utilisant toutes les fonctions disponibles
    """
    
    def __init__(self):
        # Initialiser les générateurs spécialisés
        self.cbet_generator = CBetGenerator()
        self.facing_bets_generator = FacingBetsGenerator()
        self.board_texture_generator = BoardTextureGenerator()
        self.hand_categories_generator = HandCategoriesGenerator()
    
    def generate_code(self, settings):
        """
        Génère le profil flop complet en coordonnant tous les générateurs spécialisés
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code de profil flop complet
        """
        # Générer l'en-tête du profil
        profile = self._generate_header(settings)
        
        # Générer la fonction principale flop modifiée pour utiliser toutes les fonctions
        main_flop_function = self._generate_enhanced_main_flop_function()
        profile += main_flop_function
        
        # Générer chaque section spécialisée
        cbet_code = self.cbet_generator.generate_code(settings)
        facing_bets_code = self.facing_bets_generator.generate_code(settings)
        board_texture_code = self.board_texture_generator.generate_code(settings)
        hand_categories_code = self.hand_categories_generator.generate_code(settings)
        
        # Ajouter les fonctions utilitaires supplémentaires pour la version améliorée
        utility_functions = self._generate_utility_functions()
        
        # Combiner le tout
        profile += cbet_code + facing_bets_code + board_texture_code + hand_categories_code + utility_functions
        
        # Ajouter le pied de page
        profile += "//*****************************************************************************\n"
        profile += "//\n"
        profile += "// END OF FLOP PROFILE\n"
        profile += "//\n"
        profile += "//*****************************************************************************"
        
        return profile
    
    def _generate_header(self, settings):
        """
        Génère l'en-tête du profil flop
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: En-tête du profil
        """
        header = "//*****************************************************************************\n"
        header += "//\n"
        header += "// FLOP STRATEGY - ENHANCED VERSION\n"
        header += "//\n"
        header += "// Generated with comprehensive texture-based adaptations:\n"
        header += f"// - IP C-Bet Frequency: {settings.get('ip_cbet_freq', 70)}%\n"
        header += f"// - OOP C-Bet Frequency: {settings.get('oop_cbet_freq', 60)}%\n"
        header += f"// - IP C-Bet Size: {settings.get('ip_cbet_size', '50')}% of pot\n"
        header += f"// - OOP C-Bet Size: {settings.get('oop_cbet_size', '66')}% of pot\n"
        header += f"// - Dry Board Adjustment: {settings.get('dry_board_adjust', 20)}%\n"
        header += f"// - Wet Board Adjustment: {settings.get('wet_board_adjust', -20)}%\n"
        header += f"// - Monotone Board Adjustment: {settings.get('monotone_board_adjust', -25)}%\n"
        header += f"// - Paired Board Adjustment: {settings.get('paired_board_adjust', 15)}%\n"
        header += f"// - Connected Board Adjustment: {settings.get('connected_board_adjust', -20)}%\n"
        header += f"// - High Card Board Adjustment: {settings.get('high_card_board_adjust', 10)}%\n"
        header += f"// - Low Card Board Adjustment: {settings.get('low_card_board_adjust', -15)}%\n"
        header += f"// - Dynamic Board Adjustment: {settings.get('dynamic_board_adjust', -30)}%\n"
        header += f"// - Static Board Adjustment: {settings.get('static_board_adjust', 25)}%\n"
        header += f"// - Check-Raise Defense: {settings.get('checkraise_defense', 35)}%\n"
        header += f"// - Donk Bet Response Style: {settings.get('donk_response', 'Call/Raise')}\n"
        header += f"// - Value Hands Aggression: {settings.get('value_aggression', 80)}%\n"
        header += f"// - Draw Hands Aggression: {settings.get('draw_aggression', 60)}%\n"
        header += f"// - Semi-Bluff Frequency: {settings.get('semibluff_freq', 65)}%\n"
        header += f"// - Multiway C-Bet Frequency: {settings.get('multiway_cbet_freq', 40)}%\n"
        header += f"// - Multiway Value Range: {settings.get('multiway_value_range', 25)}%\n"
        header += f"// - Strategy Polarization: {settings.get('polarization', 50)}%\n"
        header += "//\n"
        header += "//*****************************************************************************\n\n"
        
        return header
    
    def _generate_enhanced_main_flop_function(self):
        """
        Génère la fonction principale flop améliorée qui coordonne les différentes fonctions
        et utilise toutes les fonctions de texture avancées disponibles
        
        Returns:
            str: Code de la fonction principale flop améliorée
        """
        code = "##f$flop##\n"
        code += "// Main flop decision function - Enhanced version\n"
        code += "// Utilizes all advanced texture classifications and specialized strategy functions\n\n"

        # DÉTECTION DE SCÉNARIOS MULTIWAY
        code += "// MULTIWAY POT SCENARIOS (3+ PLAYERS)\n"
        code += "WHEN nopponentsplaying > 2 AND BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$GoodMultiwayBoard RETURN f$MultiwayCBetIP FORCE\n"
        code += "WHEN nopponentsplaying > 2 AND BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$RiskyMultiwayBoard RETURN f$MultiwayCBetOOP FORCE\n\n"

        # SCÉNARIOS C-BET AVEC ADAPTATIONS DE TEXTURE
        code += "// C-BET SCENARIOS WITH BOARD TEXTURE ADAPTATIONS\n"
        
        # C-bet en IP (in position) avec adaptations selon texture
        code += "// IP C-bet scenarios with texture adaptations\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition AND f$MonotoneBoard RETURN f$CbetMonotoneBoard FORCE\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition AND f$PairedBoard RETURN f$CbetPairedBoard FORCE\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition AND f$ConnectedBoard RETURN f$CbetConnectedBoard FORCE\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition AND f$HighCardBoard RETURN f$CbetHighCardBoard FORCE\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition AND f$LowCardBoard RETURN f$CbetLowCardBoard FORCE\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition AND f$DynamicBoard RETURN f$CbetDynamicBoard FORCE\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition AND f$StaticBoard RETURN f$CbetStaticBoard FORCE\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition AND f$FavorableCBetBoard RETURN f$CbetFavorableBoard FORCE\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition AND f$UnfavorableCBetBoard RETURN f$CbetUnfavorableBoard FORCE\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition RETURN f$FlopCbetIP FORCE\n\n"
        
        # C-bet OOP (out of position) avec adaptations selon texture
        code += "// OOP C-bet scenarios with texture adaptations\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND NOT f$InPosition AND f$MonotoneBoard RETURN f$CbetMonotoneBoard FORCE\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND NOT f$InPosition AND f$PairedBoard RETURN f$CbetPairedBoard FORCE\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND NOT f$InPosition AND f$ConnectedBoard RETURN f$CbetConnectedBoard FORCE\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND NOT f$InPosition AND f$HighCardBoard RETURN f$CbetHighCardBoard FORCE\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND NOT f$InPosition AND f$LowCardBoard RETURN f$CbetLowCardBoard FORCE\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND NOT f$InPosition AND f$DynamicBoard RETURN f$CbetDynamicBoard FORCE\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND NOT f$InPosition AND f$StaticBoard RETURN f$CbetStaticBoard FORCE\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND NOT f$InPosition AND f$FavorableCBetBoard RETURN f$CbetFavorableBoard FORCE\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND NOT f$InPosition AND f$UnfavorableCBetBoard RETURN f$CbetUnfavorableBoard FORCE\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND NOT f$InPosition RETURN f$FlopCbetOOP FORCE\n\n"

        # SCÉNARIOS FACE AUX MISES
        code += "// FACING BET SCENARIOS WITH TEXTURE ADAPTATIONS\n"
        code += "WHEN BotsActionsOnThisRoundIncludingChecks = 0 AND BotCalledBeforeFlop AND f$FacingCBetFavorableBoard RETURN f$FacingCBetFavorableBoard FORCE\n"
        code += "WHEN BotsActionsOnThisRoundIncludingChecks = 0 AND BotCalledBeforeFlop AND f$FacingCBetUnfavorableBoard RETURN f$FacingCBetUnfavorableBoard FORCE\n"
        code += "WHEN BotsActionsOnThisRoundIncludingChecks = 0 AND BotCalledBeforeFlop AND f$MonotoneBoard RETURN f$FacingCBetMonotoneBoard FORCE\n"
        code += "WHEN BotsActionsOnThisRoundIncludingChecks = 0 AND BotCalledBeforeFlop AND f$PairedBoard RETURN f$FacingCBetPairedBoard FORCE\n"
        code += "WHEN BotsActionsOnThisRoundIncludingChecks = 0 AND BotCalledBeforeFlop AND f$ConnectedBoard RETURN f$FacingCBetConnectedBoard FORCE\n"
        code += "WHEN f$FacingFlopCbet RETURN f$FacingFlopCbet FORCE\n"
        code += "WHEN f$FacingDonkBet RETURN f$FacingDonkBet FORCE\n\n"

        # SCÉNARIOS DE DONK BET 
        code += "// DONK BETTING SCENARIOS WITH TEXTURE ADAPTATIONS\n"
        code += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND Bets = 0 AND NOT f$InPosition AND f$GoodDonkBetBoard RETURN f$DonkBetFavorableBoard FORCE\n"
        code += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND Bets = 0 AND NOT f$InPosition RETURN f$DonkBet FORCE\n\n"

        # SCÉNARIOS DE CHECK-RAISE
        code += "// CHECK-RAISE SCENARIOS WITH TEXTURE ADAPTATIONS\n"
        code += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 1 AND NOT f$InPosition AND f$GoodCheckRaiseBoard RETURN f$CheckRaiseFavorableBoard FORCE\n"
        code += "WHEN f$FacingCheckRaiseToCbet RETURN f$FacingCheckRaiseToCbet FORCE\n"
        code += "WHEN f$FacingRaiseToCbet RETURN f$FacingRaiseToCbet FORCE\n\n"

        # RÉPONSES FACE AUX CHECKS
        code += "// FACING CHECK SCENARIOS WITH TEXTURE ADAPTATIONS\n"
        code += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition AND f$FavorableCBetBoard RETURN f$BetAfterCheckFavorableBoard FORCE\n"
        code += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition AND f$DynamicBoard RETURN f$BetAfterCheckDynamicBoard FORCE\n"
        code += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition AND f$StaticBoard RETURN f$BetAfterCheckStaticBoard FORCE\n"
        code += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition RETURN f$BetAfterCheckIP FORCE\n\n"

        # ACTIONS PAR DÉFAUT
        code += "// Default action\n"
        code += "WHEN Others Check FORCE\n\n"

        # FONCTIONS HELPER POUR DÉTECTION DE POSITION
        code += "//*****************************************************************************\n"
        code += "// Position helper functions\n"
        code += "//*****************************************************************************\n\n"

        code += "##f$InPosition##\n"
        code += "// Helper function to determine if we're in position\n"
        code += "WHEN LastAggressorActsAfterUs RETURN false FORCE\n"
        code += "WHEN Others RETURN true FORCE\n\n"

        return code
    
    def _generate_utility_functions(self):
        """
        Génère les fonctions utilitaires supplémentaires pour la version améliorée
        qui utilisent les classifications avancées de texture
        
        Returns:
            str: Code des fonctions utilitaires
        """
        code = "//*****************************************************************************\n"
        code += "//\n"
        code += "// SPECIALIZED C-BET FUNCTIONS FOR DIFFERENT BOARD TEXTURES\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"
        
        # C-bet sur board monotone
        code += "##f$CbetMonotoneBoard##\n"
        code += "// C-bet strategy for monotone boards (three cards of the same suit)\n"
        code += "WHEN f$FlopStrongHands RaiseBy f$RecommendedCBetSizing% FORCE\n"
        code += "WHEN HaveFlush RaiseBy 75% FORCE\n"
        code += "WHEN HaveFlushDraw RaiseBy 66% FORCE\n"
        code += "WHEN HaveSet RaiseBy 75% FORCE\n"
        code += "WHEN HaveTwoPair RaiseBy 75% FORCE\n"
        code += "WHEN handrank169 <= 25 RaiseBy 66% FORCE\n"
        code += "WHEN f$InPosition AND handrank169 <= 35 RaiseBy 33% FORCE\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # C-bet sur board pairé
        code += "##f$CbetPairedBoard##\n"
        code += "// C-bet strategy for paired boards (pair on board)\n"
        code += "WHEN HaveFullHouse RaiseBy 75% FORCE\n"
        code += "WHEN HaveTrips RaiseBy 75% FORCE\n"
        code += "WHEN HaveOverPair RaiseBy 50% FORCE\n"
        code += "WHEN HaveTopPair AND f$HaveGoodKicker RaiseBy 50% FORCE\n"
        code += "WHEN f$InPosition AND handrank169 <= 40 RaiseBy 33% FORCE\n"
        code += "WHEN NOT f$InPosition AND handrank169 <= 30 RaiseBy 50% FORCE\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # C-bet sur board connecté
        code += "##f$CbetConnectedBoard##\n"
        code += "// C-bet strategy for connected boards (three consecutive cards)\n"
        code += "WHEN HaveStraight RaiseBy 75% FORCE\n"
        code += "WHEN HaveSet RaiseBy 75% FORCE\n"
        code += "WHEN HaveTwoPair RaiseBy 66% FORCE\n"
        code += "WHEN HaveOpenEndedStraightDraw RaiseBy 50% FORCE\n"
        code += "WHEN f$InPosition AND handrank169 <= 35 RaiseBy 33% FORCE\n"
        code += "WHEN NOT f$InPosition AND handrank169 <= 25 RaiseBy 50% FORCE\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # C-bet sur board avec cartes hautes
        code += "##f$CbetHighCardBoard##\n"
        code += "// C-bet strategy for high card boards (A, K, Q on board)\n"
        code += "WHEN HaveTopPair AND rankloplayer >= ten RaiseBy 66% FORCE\n"
        code += "WHEN HaveOverPair RaiseBy 66% FORCE\n"
        code += "WHEN f$InPosition AND handrank169 <= 45 RaiseBy 33% FORCE\n"
        code += "WHEN NOT f$InPosition AND handrank169 <= 35 RaiseBy 50% FORCE\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # C-bet sur board avec cartes basses
        code += "##f$CbetLowCardBoard##\n"
        code += "// C-bet strategy for low card boards (all cards 9 or lower)\n"
        code += "WHEN HaveOverPair RaiseBy 66% FORCE\n"
        code += "WHEN HaveTopPair AND f$HaveGoodKicker RaiseBy 50% FORCE\n"
        code += "WHEN f$InPosition AND handrank169 <= 40 RaiseBy 33% FORCE\n"
        code += "WHEN NOT f$InPosition AND handrank169 <= 30 RaiseBy 50% FORCE\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # C-bet sur board dynamique
        code += "##f$CbetDynamicBoard##\n"
        code += "// C-bet strategy for dynamic boards (many possible draws)\n"
        code += "WHEN f$FlopStrongHands RaiseBy 75% FORCE\n"
        code += "WHEN f$FlopStrongDraws RaiseBy 66% FORCE\n"
        code += "WHEN f$InPosition AND handrank169 <= 30 RaiseBy 50% FORCE\n"
        code += "WHEN NOT f$InPosition AND handrank169 <= 20 RaiseBy 66% FORCE\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # C-bet sur board statique
        code += "##f$CbetStaticBoard##\n"
        code += "// C-bet strategy for static boards (few possible draws)\n"
        code += "WHEN f$FlopValueHands RaiseBy 50% FORCE\n"
        code += "WHEN f$InPosition AND handrank169 <= 60 RaiseBy 33% FORCE\n"
        code += "WHEN NOT f$InPosition AND handrank169 <= 40 RaiseBy 33% FORCE\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # C-bet sur board favorable
        code += "##f$CbetFavorableBoard##\n"
        code += "// C-bet strategy for favorable c-bet boards\n"
        code += "WHEN f$FlopValueHands RaiseBy 50% FORCE\n"
        code += "WHEN f$InPosition AND handrank169 <= 70 RaiseBy 33% FORCE\n"
        code += "WHEN NOT f$InPosition AND handrank169 <= 50 RaiseBy 33% FORCE\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # C-bet sur board défavorable
        code += "##f$CbetUnfavorableBoard##\n"
        code += "// C-bet strategy for unfavorable c-bet boards\n"
        code += "WHEN f$FlopStrongHands RaiseBy 66% FORCE\n"
        code += "WHEN f$InPosition AND handrank169 <= 30 RaiseBy 33% FORCE\n"
        code += "WHEN NOT f$InPosition AND handrank169 <= 20 RaiseBy 50% FORCE\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # Fonctions pour faire face à une mise selon la texture du board
        code += "//*****************************************************************************\n"
        code += "//\n"
        code += "// SPECIALIZED FACING BET FUNCTIONS FOR DIFFERENT BOARD TEXTURES\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"
        
        # Facing C-bet sur board favorable
        code += "##f$FacingCBetFavorableBoard##\n"
        code += "// Strategy when facing a c-bet on a favorable board\n"
        code += "WHEN f$FlopStrongHands RaisePot FORCE\n"
        code += "WHEN f$FlopValueHands Call FORCE\n"
        code += "WHEN f$InPosition AND handrank169 <= 40 Call FORCE\n"
        code += "WHEN NOT f$InPosition AND handrank169 <= 30 Call FORCE\n"
        code += "WHEN Others Fold FORCE\n\n"
        
        # Facing C-bet sur board défavorable
        code += "##f$FacingCBetUnfavorableBoard##\n"
        code += "// Strategy when facing a c-bet on an unfavorable board\n"
        code += "WHEN f$FlopStrongHands RaisePot FORCE\n"
        code += "WHEN f$FlopStrongDraws AND handrank169 <= 35 RaisePot FORCE\n"
        code += "WHEN f$FlopValueHands Call FORCE\n"
        code += "WHEN f$FlopDrawHands Call FORCE\n"
        code += "WHEN Others Fold FORCE\n\n"
        
        # Facing C-bet sur board monotone
        code += "##f$FacingCBetMonotoneBoard##\n"
        code += "// Strategy when facing a c-bet on a monotone board\n"
        code += "WHEN HaveFlush RaisePot FORCE\n"
        code += "WHEN HaveFlushDraw Call FORCE\n"
        code += "WHEN f$FlopStrongHands Call FORCE\n"
        code += "WHEN Others Fold FORCE\n\n"
        
        # Facing C-bet sur board pairé
        code += "##f$FacingCBetPairedBoard##\n"
        code += "// Strategy when facing a c-bet on a paired board\n"
        code += "WHEN HaveFullHouse RaisePot FORCE\n"
        code += "WHEN HaveTrips RaisePot FORCE\n"
        code += "WHEN HaveTwoPair Call FORCE\n"
        code += "WHEN HaveOverPair Call FORCE\n"
        code += "WHEN Others Fold FORCE\n\n"
        
        # Facing C-bet sur board connecté
        code += "##f$FacingCBetConnectedBoard##\n"
        code += "// Strategy when facing a c-bet on a connected board\n"
        code += "WHEN HaveStraight RaisePot FORCE\n"
        code += "WHEN HaveSet RaisePot FORCE\n"
        code += "WHEN HaveOpenEndedStraightDraw AND f$InPosition Call FORCE\n"
        code += "WHEN f$FlopValueHands Call FORCE\n"
        code += "WHEN Others Fold FORCE\n\n"
        
        # Fonctions pour donk bet selon la texture
        code += "//*****************************************************************************\n"
        code += "//\n"
        code += "// SPECIALIZED DONK BET FUNCTIONS FOR DIFFERENT BOARD TEXTURES\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"
        
        # Donk bet sur board favorable
        code += "##f$DonkBetFavorableBoard##\n"
        code += "// Donk betting strategy on favorable boards\n"
        code += "WHEN f$FlopStrongHands RaiseBy 66% FORCE\n"
        code += "WHEN f$FlopValueHands RaiseBy 66% FORCE\n"
        code += "WHEN handrank169 <= 25 RaiseBy 50% FORCE\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # Check-raise sur board favorable
        code += "##f$CheckRaiseFavorableBoard##\n"
        code += "// Check-raise strategy on favorable boards\n"
        code += "WHEN f$FlopStrongHands RaisePot FORCE\n"
        code += "WHEN f$FlopStrongDraws AND handrank169 <= 25 RaisePot FORCE\n" 
        code += "WHEN f$FlopValueHands AND LastRaiserPosition >= (nplayersdealt - 2) RaisePot FORCE\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # Fonctions pour bet after check selon la texture
        code += "//*****************************************************************************\n"
        code += "//\n"
        code += "// SPECIALIZED BET AFTER CHECK FUNCTIONS FOR DIFFERENT BOARD TEXTURES\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"
        
        # Bet after check sur board favorable
        code += "##f$BetAfterCheckFavorableBoard##\n"
        code += "// Betting strategy after villain checks on favorable boards\n"
        code += "WHEN f$FlopStrongHands RaiseBy 66% FORCE\n"
        code += "WHEN f$FlopValueHands RaiseBy 50% FORCE\n"
        code += "WHEN handrank169 <= 70 RaiseBy 33% FORCE\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # Bet after check sur board dynamique
        code += "##f$BetAfterCheckDynamicBoard##\n"
        code += "// Betting strategy after villain checks on dynamic boards\n"
        code += "WHEN f$FlopStrongHands RaiseBy 75% FORCE\n"
        code += "WHEN f$FlopValueHands RaiseBy 66% FORCE\n"
        code += "WHEN f$FlopStrongDraws RaiseBy 50% FORCE\n"
        code += "WHEN handrank169 <= 35 RaiseBy 50% FORCE\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # Bet after check sur board statique
        code += "##f$BetAfterCheckStaticBoard##\n"
        code += "// Betting strategy after villain checks on static boards\n"
        code += "WHEN f$FlopStrongHands RaiseBy 66% FORCE\n"
        code += "WHEN f$FlopValueHands RaiseBy 50% FORCE\n"
        code += "WHEN handrank169 <= 60 RaiseBy 33% FORCE\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # Fonctions pour les scénarios multiway
        code += "//*****************************************************************************\n"
        code += "//\n"
        code += "// SPECIALIZED MULTIWAY POT FUNCTIONS\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"
        
        # Check bluff sur board avec draws
        code += "##f$CheckBluffDrawBoards##\n"
        code += "// Check-bluff strategy for when villain checks to you on draw-heavy boards\n"
        code += "WHEN f$FlopStrongHands RaiseBy 75% FORCE\n"
        code += "WHEN f$FlopValueHands RaiseBy 66% FORCE\n"
        code += "WHEN f$FlopDrawHands RaiseBy 50% FORCE\n"
        code += "WHEN handrank169 <= 30 RaiseBy 33% FORCE\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # Fold equity sur board statique
        code += "##f$MaximizeFoldEquity##\n"
        code += "// Strategy to maximize fold equity on static boards\n"
        code += "WHEN f$FlopStrongHands RaiseBy 50% FORCE\n"
        code += "WHEN handrank169 <= 60 RaiseBy 33% FORCE\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # Fonctions d'équité
        code += "//*****************************************************************************\n"
        code += "//\n"
        code += "// EQUITY FUNCTIONS\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"
        
        # Équité polarisée
        code += "##f$PlayPolarizedEquity##\n"
        code += "// Strategy for playing with polarized equity (strong hands and bluffs)\n"
        code += "WHEN f$PolarizedEquity AND f$FlopStrongHands RaiseBy 75% FORCE\n"
        code += "WHEN f$PolarizedEquity AND handrank169 >= 120 RaiseBy 66% FORCE\n"
        code += "WHEN f$PolarizedEquity AND handrank169 <= 30 RaiseBy 66% FORCE\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # Équité linéaire
        code += "##f$PlayLinearEquity##\n"
        code += "// Strategy for playing with linear equity (bet more hands with decreasing sizing)\n"
        code += "WHEN f$LinearEquity AND f$FlopStrongHands RaiseBy 66% FORCE\n"
        code += "WHEN f$LinearEquity AND f$FlopValueHands RaiseBy 50% FORCE\n"
        code += "WHEN f$LinearEquity AND f$FlopDrawHands RaiseBy 33% FORCE\n"
        code += "WHEN f$LinearEquity AND handrank169 <= 60 RaiseBy 33% FORCE\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # Fonctions de coordination main-board
        code += "//*****************************************************************************\n"
        code += "//\n"
        code += "// HAND-BOARD COORDINATION FUNCTIONS\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"
        
        # Fonction pour les mains bien coordonnées
        code += "##f$WellCoordinatedWithBoard##\n"
        code += "// Determines if our hand is well-coordinated with the board\n"
        code += "WHEN HaveTopPair AND f$HaveGoodKicker RETURN true FORCE\n"
        code += "WHEN HaveOverPair RETURN true FORCE\n"
        code += "WHEN HaveSet RETURN true FORCE\n"
        code += "WHEN HaveTwoPair RETURN true FORCE\n"
        code += "WHEN HaveStraight RETURN true FORCE\n"
        code += "WHEN HaveFlush RETURN true FORCE\n"
        code += "WHEN f$PairedBoard AND HavePair AND rankhiplayer > f$PairOnBoardRank RETURN true FORCE\n"
        code += "WHEN f$MonotoneBoard AND (FirstHoleCardSuit = DominantSuitCommon AND SecondHoleCardSuit = DominantSuitCommon) RETURN true FORCE\n"
        code += "WHEN f$ConnectedBoard AND nstraightfill <= 1 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Fonction pour les mains peu coordonnées
        code += "##f$PoorlyCoordinatedWithBoard##\n"
        code += "// Determines if our hand is poorly coordinated with the board\n"
        code += "WHEN rankhiplayer < 10 AND NOT HavePair AND NOT HaveStraightDraw AND NOT HaveFlushDraw RETURN true FORCE\n"
        code += "WHEN rankhiplayer >= 10 AND LowestFlopCard >= 10 AND NOT HavePair RETURN true FORCE\n"
        code += "WHEN f$MonotoneBoard AND FirstHoleCardSuit != DominantSuitCommon AND SecondHoleCardSuit != DominantSuitCommon RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        return code
    
    def generate_flop_profile(self, settings):
        """
        Pour maintenir la compatibilité avec l'API existante
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code de profil flop complet
        """
        return self.generate_code(settings)
