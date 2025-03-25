"""
Générateur principal pour le profil river OpenHoldem
Coordonne les générateurs spécialisés
"""
from generators.river.base_generator import BaseRiverGenerator
from generators.river.third_barrel_generator import ThirdBarrelGenerator
from generators.river.facing_bets_generator import FacingBetsGenerator
from generators.river.probe_generator import ProbeGenerator
from generators.river.board_texture_generator import BoardTextureGenerator
from generators.river.hand_categories_generator import HandCategoriesGenerator

class RiverProfileGenerator(BaseRiverGenerator):
    """
    Classe principale pour générer le profil river complet
    Coordonne les différents générateurs spécialisés
    """
    
    def __init__(self):
        # Initialiser les générateurs spécialisés
        self.third_barrel_generator = ThirdBarrelGenerator()
        self.facing_bets_generator = FacingBetsGenerator()
        self.probe_generator = ProbeGenerator()
        self.board_texture_generator = BoardTextureGenerator()
        self.hand_categories_generator = HandCategoriesGenerator()
    
    def generate_code(self, settings):
        """
        Génère le profil river complet en coordonnant tous les générateurs spécialisés
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code de profil river complet
        """
        # Générer l'en-tête du profil
        profile = self._generate_header(settings)
        
        # Générer la fonction principale river
        main_river_function = self._generate_main_river_function()
        profile += main_river_function
        
        # Générer chaque section spécialisée
        third_barrel_code = self.third_barrel_generator.generate_code(settings)
        facing_bets_code = self.facing_bets_generator.generate_code(settings)
        probe_code = self.probe_generator.generate_code(settings)
        board_texture_code = self.board_texture_generator.generate_code(settings)
        hand_categories_code = self.hand_categories_generator.generate_code(settings)
        
        # Combiner le tout
        profile += third_barrel_code + facing_bets_code + probe_code + board_texture_code + hand_categories_code
        
        # Ajouter le pied de page
        profile += "//*****************************************************************************\n"
        profile += "//\n"
        profile += "// END OF RIVER PROFILE\n"
        profile += "//\n"
        profile += "//*****************************************************************************"
        
        return profile
    
    def _generate_header(self, settings):
        """
        Génère l'en-tête du profil river
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: En-tête du profil
        """
        header = "//*****************************************************************************\n"
        header += "//\n"
        header += "// RIVER STRATEGY\n"
        header += "//\n"
        header += "// Generated with the following settings:\n"
        header += f"// - Third Barrel Frequency: {settings.get('third_barrel_freq', 40)}%\n"
        header += f"// - Delayed Second Barrel Frequency: {settings.get('delayed_second_barrel_freq', 30)}%\n"
        header += f"// - IP River Bet Size: {settings.get('ip_river_bet_size', '75')}% of pot\n"
        header += f"// - OOP River Bet Size: {settings.get('oop_river_bet_size', '75')}% of pot\n"
        header += f"// - River Check-Raise Frequency: {settings.get('river_checkraise_freq', 15)}%\n"
        header += f"// - River Float Frequency: {settings.get('river_float_freq', 20)}%\n"
        header += f"// - River Probe Frequency: {settings.get('river_probe_freq', 25)}%\n"
        header += f"// - River Fold to Bet Frequency: {settings.get('river_fold_to_bet_freq', 70)}%\n"
        header += f"// - River Bluff Raise Frequency: {settings.get('river_bluff_raise_freq', 10)}%\n"
        header += f"// - River Value Range: {settings.get('river_value_range', 60)}%\n"
        header += f"// - River Bluff Range: {settings.get('river_bluff_range', 15)}%\n"
        header += f"// - River Check Behind Range: {settings.get('river_check_behind_range', 80)}%\n"
        header += "//\n"
        header += "//*****************************************************************************\n\n"
        
        return header
    
    def _generate_main_river_function(self):
        """
        Génère la fonction principale river qui coordonne les différentes fonctions
        
        Returns:
            str: Code de la fonction principale river
        """
        code = "##f$river##\n"
        code += "// Main river decision function\n"
        code += "// Determines action based on scenario detection\n\n"

        code += "// Third Barrel and Delayed Second Barrel scenarios\n"
        code += "WHEN f$ThirdBarrel RETURN f$RiverThirdBarrel FORCE\n"
        code += "WHEN f$DelayedSecondBarrel RETURN f$RiverDelayedSecondBarrel FORCE\n\n"

        code += "// Facing bet scenarios\n"
        code += "WHEN f$FacingThirdBarrel RETURN f$FacingThirdBarrel FORCE\n"
        code += "WHEN f$FacingDelayedSecondBarrel RETURN f$FacingDelayedSecondBarrel FORCE\n\n"

        code += "// Facing check scenarios\n"
        code += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition AND NoBettingOnTurn RETURN f$RiverProbeAfterCheckedTurn FORCE\n"
        code += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND NOT f$InPosition AND NoBettingOnTurn RETURN f$RiverOOPAfterCheckedTurn FORCE\n\n"

        code += "// Facing check to our turn bet\n"
        code += "WHEN BotRaisedBeforeFlop AND BotRaisedOnFlop AND BotRaisedOnTurn AND BotsActionsOnThisRoundIncludingChecks = 0 AND Bets = 0 AND f$InPosition RETURN f$RiverContinuationAfterTurnBet FORCE\n\n"

        code += "// Check-raise response\n"
        code += "WHEN f$FacingCheckRaiseToThirdBarrel RETURN f$FacingCheckRaiseToThirdBarrel FORCE\n"
        code += "WHEN f$FacingRaiseToThirdBarrel RETURN f$FacingRaiseToThirdBarrel FORCE\n\n"

        code += "// Default action\n"
        code += "WHEN Others Check FORCE\n\n"

        code += "//*****************************************************************************\n"
        code += "// Helper functions for identifying scenarios\n"
        code += "//*****************************************************************************\n\n"

        code += "##f$ThirdBarrel##\n"
        code += "// Detect third barrel scenarios\n"
        code += "WHEN BotRaisedBeforeFlop AND BotRaisedOnFlop AND BotRaisedOnTurn AND BotsActionsOnThisRoundIncludingChecks = 0 AND Bets > 0 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        code += "##f$DelayedSecondBarrel##\n"
        code += "// Detect delayed second barrel scenarios\n"
        code += "WHEN BotRaisedBeforeFlop AND BotRaisedOnFlop AND NOT BotRaisedOnTurn AND BotsActionsOnThisRoundIncludingChecks = 0 AND Bets > 0 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        code += "##f$FacingThirdBarrel##\n"
        code += "// Detect facing third barrel scenarios\n"
        code += "WHEN NOT BotRaisedBeforeFlop AND BotAction_PREFLOP = Call AND BotAction_FLOP = Call AND BotAction_TURN = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND Bets > 0 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        code += "##f$FacingDelayedSecondBarrel##\n"
        code += "// Detect facing delayed second barrel scenarios\n"
        code += "WHEN NOT BotRaisedBeforeFlop AND BotAction_PREFLOP = Call AND BotAction_FLOP = Call AND BotAction_TURN = Check AND BotsActionsOnThisRoundIncludingChecks = 0 AND Bets > 0 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        code += "##f$FacingCheckRaiseToThirdBarrel##\n"
        code += "// Detect facing check-raise to third barrel scenarios\n"
        code += "WHEN BotRaisedBeforeFlop AND BotRaisedOnFlop AND BotRaisedOnTurn AND BotActionsRiver = 1 AND BotsActionsOnThisRound = 1 AND RaisesSinceLastPlay = 1 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        code += "##f$FacingRaiseToThirdBarrel##\n"
        code += "// Detect facing raise to third barrel scenarios\n"
        code += "WHEN BotRaisedBeforeFlop AND BotRaisedOnFlop AND BotRaisedOnTurn AND BotRaisedOnRiver AND RaisesSinceLastPlay = 1 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        return code
    
    def generate_river_profile(self, settings):
        """
        Pour maintenir la compatibilité avec l'API existante
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code de profil river complet
        """
        return self.generate_code(settings)
