"""
Générateur principal pour le profil flop OpenHoldem
Coordonne les générateurs spécialisés
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
        
        # Générer la fonction principale flop
        main_flop_function = self._generate_main_flop_function()
        profile += main_flop_function
        
        # Générer chaque section spécialisée
        cbet_code = self.cbet_generator.generate_code(settings)
        facing_bets_code = self.facing_bets_generator.generate_code(settings)
        board_texture_code = self.board_texture_generator.generate_code(settings)
        hand_categories_code = self.hand_categories_generator.generate_code(settings)
        
        # Combiner le tout
        profile += cbet_code + facing_bets_code + board_texture_code + hand_categories_code
        
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
        header += "// FLOP STRATEGY\n"
        header += "//\n"
        header += "// Generated with the following settings:\n"
        header += f"// - IP C-Bet Frequency: {settings.get('ip_cbet_freq', 70)}%\n"
        header += f"// - OOP C-Bet Frequency: {settings.get('oop_cbet_freq', 60)}%\n"
        header += f"// - IP C-Bet Size: {settings.get('ip_cbet_size', '50')}% of pot\n"
        header += f"// - OOP C-Bet Size: {settings.get('oop_cbet_size', '66')}% of pot\n"
        header += f"// - Dry Board Adjustment: {settings.get('dry_board_adjust', 20)}%\n"
        header += f"// - Wet Board Adjustment: {settings.get('wet_board_adjust', -20)}%\n"
        header += f"// - Check-Raise Defense: {settings.get('checkraise_defense', 35)}%\n"
        header += f"// - Donk Bet Response Style: {settings.get('donk_response', 'Call/Raise')}\n"
        header += f"// - Value Hands Aggression: {settings.get('value_aggression', 80)}%\n"
        header += f"// - Draw Hands Aggression: {settings.get('draw_aggression', 60)}%\n"
        header += f"// - Semi-Bluff Frequency: {settings.get('semibluff_freq', 65)}%\n"
        header += f"// - Multiway C-Bet Frequency: {settings.get('multiway_cbet_freq', 40)}%\n"
        header += f"// - Multiway Value Range: {settings.get('multiway_value_range', 25)}%\n"
        header += "//\n"
        header += "//*****************************************************************************\n\n"
        
        return header
    
    def _generate_main_flop_function(self):
        """
        Génère la fonction principale flop qui coordonne les différentes fonctions
        
        Returns:
            str: Code de la fonction principale flop
        """
        code = "##f$flop##\n"
        code += "// Main flop decision function\n"
        code += "// Determines action based on scenario detection\n\n"

        code += "// C-Bet scenarios\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition RETURN f$FlopCbetIP FORCE\n"
        code += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND NOT f$InPosition RETURN f$FlopCbetOOP FORCE\n\n"

        code += "// Facing bet scenarios\n"
        code += "WHEN f$FacingFlopCbet RETURN f$FacingFlopCbet FORCE\n"
        code += "WHEN f$FacingDonkBet RETURN f$FacingDonkBet FORCE\n\n"

        code += "// Facing check scenarios\n"
        code += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition RETURN f$BetAfterCheckIP FORCE\n"
        code += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND Bets = 0 AND NOT f$InPosition RETURN f$DonkBet FORCE\n\n"

        code += "// Check-raise response\n"
        code += "WHEN f$FacingCheckRaiseToCbet RETURN f$FacingCheckRaiseToCbet FORCE\n"
        code += "WHEN f$FacingRaiseToCbet RETURN f$FacingRaiseToCbet FORCE\n\n"

        code += "// Default action\n"
        code += "WHEN Others Check FORCE\n\n"
        
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