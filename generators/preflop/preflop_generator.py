"""
Générateur principal pour le profil preflop OpenHoldem
Coordonne les générateurs spécialisés
"""
from generators.preflop.base_generator import BaseProfileGenerator
from generators.preflop.open_raise_generator import OpenRaiseGenerator
from generators.preflop.three_bet_generator import ThreeBetGenerator
from generators.preflop.squeeze_generator import SqueezeGenerator
from generators.preflop.push_fold_generator import PushFoldGenerator

class PreflopProfileGenerator(BaseProfileGenerator):
    """
    Classe principale pour générer le profil preflop complet
    Coordonne les différents générateurs spécialisés
    """
    
    def __init__(self):
        # Initialiser les générateurs spécialisés
        self.open_raise_generator = OpenRaiseGenerator()
        self.three_bet_generator = ThreeBetGenerator()
        self.squeeze_generator = SqueezeGenerator()
        self.push_fold_generator = PushFoldGenerator()
    
    def generate_code(self, settings):
        """
        Génère le profil preflop complet en coordonnant tous les générateurs spécialisés
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code de profil preflop complet
        """
        # Générer l'en-tête du profil
        profile = self._generate_header(settings)
        
        # Générer chaque section spécialisée
        open_raise_code = self.open_raise_generator.generate_code(settings)
        three_bet_code = self.three_bet_generator.generate_code(settings)
        squeeze_code = self.squeeze_generator.generate_code(settings)
        push_fold_code = self.push_fold_generator.generate_code(settings)
        
        # Générer la fonction principale preflop
        main_preflop_function = self._generate_main_preflop_function()
        
        # Combiner le tout
        profile += open_raise_code + three_bet_code + squeeze_code + main_preflop_function + push_fold_code
        
        # Ajouter le pied de page
        profile += "//*****************************************************************************\n"
        profile += "//\n"
        profile += "// END OF PREFLOP PROFILE\n"
        profile += "//\n"
        profile += "//*****************************************************************************"
        
        return profile
    
    def _generate_header(self, settings):
        """
        Génère l'en-tête du profil preflop
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: En-tête du profil
        """
        num_players = settings["num_players"]
        game_type = settings["game_type"]
        aggression = settings["aggression"]
        tightness = settings["tightness"]
        limp_frequency = settings["limp_frequency"]
        threebet_frequency = settings["threebet_frequency"]
        fourbet_frequency = settings["fourbet_frequency"]
        squeeze_frequency = settings["squeeze_frequency"]
        open_raise_size = settings["open_raise_size"]
        
        # Facteurs d'ajustement
        aggressive_factor = aggression / 50  # 0-2 range where 1 is neutral
        threebet_adjustment = 1 + (aggressive_factor - 1) * 0.5  # 0.75-1.25 range
        fourbet_adjustment = 1 + (aggressive_factor - 1) * 0.6   # 0.7-1.3 range
        squeeze_adjustment = 1 + (aggressive_factor - 1) * 0.7   # 0.65-1.35 range
        
        # Obtenir la carte des positions
        position_map = self.get_position_map(num_players)
        
        header = "//*****************************************************************************\n"
        header += "//\n"
        header += f"// OpenHoldem Profile Generator - Preflop Profile\n"
        header += f"// Generated for {num_players}-player {game_type}\n"
        header += "// \n"
        header += f"// Strategy Settings:\n"
        header += f"// - Aggression: {aggression}% (Factor: {aggressive_factor:.2f}x)\n"
        header += f"// - Tightness: {tightness}%\n"
        header += f"// - Limp Frequency: {limp_frequency}%\n"
        header += f"// - 3-Bet Frequency: {threebet_frequency}% (Adjusted: {threebet_frequency * threebet_adjustment:.1f}%)\n"
        header += f"// - 4-Bet Frequency: {fourbet_frequency}% (Adjusted: {fourbet_frequency * fourbet_adjustment:.1f}%)\n"
        header += f"// - Squeeze Frequency: {squeeze_frequency}% (Adjusted: {squeeze_frequency * squeeze_adjustment:.1f}%)\n"
        header += f"// - Open Raise Size: {open_raise_size}x (Adjusted: {self.calculate_raise_size(open_raise_size, 0, aggressive_factor)}x)\n"
        header += "//\n"
        header += "// Position-Based Settings:\n"
        header += f"// - EP1 (UTG) Range: {settings['ep1_range']}% (Threshold: {self.get_handrank_threshold(settings['ep1_range'])})\n"
        header += f"// - EP2 (UTG+1) Range: {settings['ep2_range']}% (Threshold: {self.get_handrank_threshold(settings['ep2_range'])})\n"
        header += f"// - EP3 (UTG+2) Range: {settings['ep3_range']}% (Threshold: {self.get_handrank_threshold(settings['ep3_range'])})\n"
        header += f"// - MP1 Range: {settings['mp1_range']}% (Threshold: {self.get_handrank_threshold(settings['mp1_range'])})\n"
        header += f"// - MP2 Range: {settings['mp2_range']}% (Threshold: {self.get_handrank_threshold(settings['mp2_range'])})\n"
        header += f"// - MP3 (HJ) Range: {settings['mp3_range']}% (Threshold: {self.get_handrank_threshold(settings['mp3_range'])})\n"
        header += f"// - CO Range: {settings['co_range']}% (Threshold: {self.get_handrank_threshold(settings['co_range'])})\n"
        header += f"// - BTN Range: {settings['btn_range']}% (Threshold: {self.get_handrank_threshold(settings['btn_range'])})\n"
        header += f"// - SB Range: {settings['sb_range']}% (Threshold: {self.get_handrank_threshold(settings['sb_range'])})\n"
        header += f"// - Squeeze vs 1 Caller: {settings['squeeze_1caller']}% (Threshold: {self.get_handrank_threshold(settings['squeeze_1caller'])})\n"
        header += f"// - Squeeze vs 2+ Callers: {settings['squeeze_multi']}% (Threshold: {self.get_handrank_threshold(settings['squeeze_multi'])})\n"
        header += "//\n"
        header += "// Position Map for Table Size:\n"
        
        # Add position information
        for pos, exists in position_map.items():
            header += f"// - {pos}: {'Active' if exists else 'Inactive'}\n"
            
        header += "//\n"
        header += "//*****************************************************************************\n\n"

        header += "//*****************************************************************************\n"
        header += "//\n"
        header += "// PREFLOP SCENARIOS\n"
        header += "//\n"
        header += "//*****************************************************************************\n\n"
        
        return header
    
    def _generate_main_preflop_function(self):
        """
        Génère la fonction principale preflop qui coordonne les différentes fonctions
        
        Returns:
            str: Code de la fonction principale preflop
        """
        code = "//*****************************************************************************\n"
        code += "//\n"
        code += "// MAIN PREFLOP FUNCTION\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"
        
        code += "##f$preflop##\n"
        code += "// Main preflop decision function that uses OpenPPL library functions\n"
        code += "// to detect scenarios and then calls our decision functions\n\n"

        code += "// Check for Push/Fold mode first\n"
        code += "WHEN f$InPushFoldMode RETURN f$PushFoldPreflop FORCE\n\n"

        code += "// Open Raise or Open Limp\n"
        code += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 0 AND Calls = 0) RETURN f$OpenRaiseOrOpenLimp FORCE\n\n"

        code += "// Limp or Isolate Limpers\n"
        code += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 0 AND Calls >= 1) RETURN f$LimpOrIsolateLimpers FORCE\n\n"

        code += "// Three Bet or Cold Call\n"
        code += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 1 AND CallsSinceLastRaise = 0) RETURN f$ThreeBetColdCall FORCE\n\n"

        code += "// Squeeze or Cold Call\n"
        code += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 1 AND CallsSinceLastRaise >= 1) RETURN f$SqueezeColdCall FORCE\n\n"

        code += "// Facing 3-Bet Before First Action\n"
        code += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 2) RETURN f$Facing3BetBeforeFirstAction FORCE\n\n"

        code += "// Facing 4-Bet Before First Action\n"
        code += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 3) RETURN f$Facing4BetBeforeFirstAction FORCE\n\n"

        code += "// Facing 5-Bet Before First Action\n"
        code += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 4) RETURN f$Facing5BetBeforeFirstAction FORCE\n\n"

        code += "// Facing 3-Bet\n"
        code += "WHEN (BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 1 AND NumberOfRaisesBeforeFlop = 1 AND Calls = 0 AND RaisesSinceLastPlay = 1) RETURN f$Facing3Bet FORCE\n\n"

        code += "// Facing Squeeze\n"
        code += "WHEN (BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 1 AND NumberOfRaisesBeforeFlop = 1 AND Calls >= 1 AND RaisesSinceLastPlay = 1) RETURN f$FacingSqueeze FORCE\n\n"

        code += "// Facing 4-Bet\n"
        code += "WHEN (BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 1 AND NumberOfRaisesBeforeFlop = 2 AND RaisesSinceLastPlay = 1) RETURN f$Facing4Bet FORCE\n\n"

        code += "// Facing 5-Bet\n"
        code += "WHEN (BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 2 AND NumberOfRaisesBeforeFlop = 2 AND RaisesSinceLastPlay = 1) RETURN f$Facing5Bet FORCE\n\n"

        code += "// Default action if no scenario is matched\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"
        
        return code
    
    def generate_preflop_profile(self, settings):
        """
        Pour maintenir la compatibilité avec l'API existante
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code de profil preflop complet
        """
        return self.generate_code(settings)
