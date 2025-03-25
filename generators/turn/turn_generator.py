"""
Générateur principal pour le profil turn OpenHoldem
Coordonne les générateurs spécialisés
"""
from generators.turn.base_generator import BaseTurnGenerator
from generators.turn.second_barrel_generator import SecondBarrelGenerator
from generators.turn.facing_bets_generator import FacingBetsGenerator
from generators.turn.probe_generator import ProbeGenerator
from generators.turn.board_texture_generator import BoardTextureGenerator
from generators.turn.hand_categories_generator import HandCategoriesGenerator

class TurnProfileGenerator(BaseTurnGenerator):
    """
    Classe principale pour générer le profil turn complet
    Coordonne les différents générateurs spécialisés
    """
    
    def __init__(self):
        # Initialiser les générateurs spécialisés
        self.second_barrel_generator = SecondBarrelGenerator()
        self.facing_bets_generator = FacingBetsGenerator()
        self.probe_generator = ProbeGenerator()
        self.board_texture_generator = BoardTextureGenerator()
        self.hand_categories_generator = HandCategoriesGenerator()
    
    def generate_code(self, settings):
        """
        Génère le profil turn complet en coordonnant tous les générateurs spécialisés
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code de profil turn complet
        """
        # Générer l'en-tête du profil
        profile = self._generate_header(settings)
        
        # Générer la fonction principale turn
        main_turn_function = self._generate_main_turn_function()
        profile += main_turn_function
        
        # Générer chaque section spécialisée
        second_barrel_code = self.second_barrel_generator.generate_code(settings)
        facing_bets_code = self.facing_bets_generator.generate_code(settings)
        probe_code = self.probe_generator.generate_code(settings)
        board_texture_code = self.board_texture_generator.generate_code(settings)
        hand_categories_code = self.hand_categories_generator.generate_code(settings)
        
        # Combiner le tout
        profile += second_barrel_code + facing_bets_code + probe_code + board_texture_code + hand_categories_code
        
        # Ajouter le pied de page
        profile += "//*****************************************************************************\n"
        profile += "//\n"
        profile += "// END OF TURN PROFILE\n"
        profile += "//\n"
        profile += "//*****************************************************************************"
        
        return profile
    
    def _generate_header(self, settings):
        """
        Génère l'en-tête du profil turn
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: En-tête du profil
        """
        header = "//*****************************************************************************\n"
        header += "//\n"
        header += "// TURN STRATEGY\n"
        header += "//\n"
        header += "// Generated with the following settings:\n"
        header += f"// - Second Barrel Frequency: {settings.get('second_barrel_freq', 60)}%\n"
        header += f"// - Delayed C-Bet Frequency: {settings.get('delayed_cbet_freq', 40)}%\n"
        header += f"// - IP Turn Bet Size: {settings.get('ip_turn_bet_size', '66')}% of pot\n"
        header += f"// - OOP Turn Bet Size: {settings.get('oop_turn_bet_size', '75')}% of pot\n"
        header += f"// - Turn Check-Raise Frequency: {settings.get('turn_checkraise_freq', 25)}%\n"
        header += f"// - Turn Float Frequency: {settings.get('turn_float_freq', 30)}%\n"
        header += f"// - Turn Probe Frequency: {settings.get('turn_probe_freq', 35)}%\n"
        header += f"// - Turn Fold to C-Bet Frequency: {settings.get('turn_fold_to_cbet_freq', 60)}%\n"
        header += f"// - Turn Bluff Raise Frequency: {settings.get('turn_bluff_raise_freq', 20)}%\n"
        header += f"// - Scare Card Adjustment: {settings.get('scare_card_adjust', -15)}%\n"
        header += f"// - Draw Complete Adjustment: {settings.get('draw_complete_adjust', 10)}%\n"
        header += "//\n"
        header += "//*****************************************************************************\n\n"
        
        return header
    
    def _generate_main_turn_function(self):
        """
        Génère la fonction principale turn qui coordonne les différentes fonctions
        
        Returns:
            str: Code de la fonction principale turn
        """
        code = "##f$turn##\n"
        code += "// Main turn decision function\n"
        code += "// Determines action based on scenario detection\n\n"

        code += "// C-Bet and Second Barrel scenarios\n"
        code += "WHEN f$SecondBarrel RETURN f$TurnSecondBarrel FORCE\n"
        code += "WHEN f$DelayedCbet RETURN f$TurnDelayedCbet FORCE\n\n"

        code += "// Facing bet scenarios\n"
        code += "WHEN f$FacingSecondBarrel RETURN f$FacingSecondBarrel FORCE\n"
        code += "WHEN f$FacingDelayedCbet RETURN f$FacingDelayedCbet FORCE\n\n"

        code += "// Facing check scenarios\n"
        code += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition AND NoBettingOnFlop RETURN f$TurnProbeAfterCheckedFlop FORCE\n"
        code += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND NOT f$InPosition AND NoBettingOnFlop RETURN f$TurnOOPAfterCheckedFlop FORCE\n\n"

        code += "// Facing check to our flop bet\n"
        code += "WHEN BotRaisedBeforeFlop AND BotRaisedOnFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND Bets = 0 AND f$InPosition RETURN f$TurnContinuationAfterFlopBet FORCE\n\n"

        code += "// Check-raise response\n"
        code += "WHEN f$FacingCheckRaiseToSecondBarrel RETURN f$FacingCheckRaiseToSecondBarrel FORCE\n"
        code += "WHEN f$FacingRaiseToSecondBarrel RETURN f$FacingRaiseToSecondBarrel FORCE\n\n"

        code += "// Default action\n"
        code += "WHEN Others Check FORCE\n\n"

        code += "//*****************************************************************************\n"
        code += "// Helper functions for identifying scenarios\n"
        code += "//*****************************************************************************\n\n"

        code += "##f$SecondBarrel##\n"
        code += "// Detect second barrel scenarios\n"
        code += "WHEN BotRaisedBeforeFlop AND BotRaisedOnFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND Bets > 0 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        code += "##f$DelayedCbet##\n"
        code += "// Detect delayed c-bet scenarios\n"
        code += "WHEN BotRaisedBeforeFlop AND NOT BotRaisedOnFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND Bets > 0 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        code += "##f$FacingSecondBarrel##\n"
        code += "// Detect facing second barrel scenarios\n"
        code += "WHEN NOT BotRaisedBeforeFlop AND BotAction_PREFLOP = Call AND BotAction_FLOP = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND Bets > 0 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        code += "##f$FacingDelayedCbet##\n"
        code += "// Detect facing delayed c-bet scenarios\n"
        code += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND NoBettingOnFlop AND BotCalledOnTurn AND Bets = 1 Return true Force\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        code += "##f$FacingCheckRaiseToSecondBarrel##\n"
        code += "// Detect facing check-raise to second barrel scenarios\n"
        code += "WHEN BotRaisedBeforeFlop AND BotRaisedOnFlop AND BotActionsTurn = 1 AND BotsActionsOnThisRound = 1 AND RaisesSinceLastPlay = 1 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        code += "##f$FacingRaiseToSecondBarrel##\n"
        code += "// Detect facing raise to second barrel scenarios\n"
        code += "WHEN BotRaisedBeforeFlop AND BotRaisedOnFlop AND BotRaisedOnTurn AND RaisesSinceLastPlay = 1 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        return code
    
    def generate_turn_profile(self, settings):
        """
        Pour maintenir la compatibilité avec l'API existante
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code de profil turn complet
        """
        return self.generate_code(settings)
