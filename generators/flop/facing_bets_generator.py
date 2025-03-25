"""
Générateur de stratégies face aux mises au flop
"""
from generators.flop.base_generator import BaseFlopGenerator

class FacingBetsGenerator(BaseFlopGenerator):
    """
    Classe pour générer les sections de code pour répondre aux mises des adversaires au flop
    """
    
    def generate_code(self, settings):
        """
        Génère les sections de réponse aux mises adverses du profil flop
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code généré pour les réponses aux mises
        """
        # Extract relevant settings
        checkraise_defense = settings.get("checkraise_defense", 35)
        donk_response = settings.get("donk_response", "Call/Raise")
        draw_aggression = settings.get("draw_aggression", 60)
        semibluff_freq = settings.get("semibluff_freq", 65)
        
        # Calculate thresholds
        checkraise_defense_threshold = self.get_handrank_threshold(checkraise_defense)
        draw_hands_threshold = self.get_handrank_threshold(draw_aggression)
        semibluff_threshold = self.get_handrank_threshold(semibluff_freq)
        
        # Generate the code
        code = "// Facing bets functions\n\n"
        
        # Facing Flop C-Bet
        code += "##f$FacingFlopCbet##\n"
        code += "// Response when facing a c-bet on the flop\n\n"
        
        code += "// Always continue with strong hands\n"
        code += "WHEN f$FlopStrongHands RaisePot FORCE\n"
        code += "WHEN f$FlopValueHands Call FORCE\n\n"
        
        code += "// Continue with good draws\n"
        code += f"WHEN f$FlopDrawHands AND handrank169 <= {draw_hands_threshold} Call FORCE\n\n"
        
        code += "// Check-raise with strong draws in position\n"
        code += f"WHEN f$InPosition AND f$FlopStrongDraws AND handrank169 <= {semibluff_threshold} RaisePot FORCE\n\n"
        
        code += "// Default fold\n"
        code += "WHEN Others Fold FORCE\n\n"

        # Facing Donk Bet
        code += "##f$FacingDonkBet##\n"
        code += "// Response when a non-preflop-raiser bets into the preflop raiser\n\n"
        
        code += "// Aggressive response to donk bets with strong hands\n"
        code += "WHEN f$FlopStrongHands RaisePot FORCE\n"
        code += "WHEN f$FlopValueHands Call FORCE\n\n"
        
        # Different responses based on settings
        if donk_response == "Fold/Call":
            code += "// Conservative approach to donk bets\n"
            code += f"WHEN f$FlopDrawHands AND handrank169 <= {round(draw_hands_threshold * 0.8)} Call FORCE\n"
        elif donk_response == "Call/Raise":
            code += "// Balanced approach to donk bets\n"
            code += f"WHEN f$FlopDrawHands AND handrank169 <= {draw_hands_threshold} Call FORCE\n"
            code += f"WHEN f$FlopStrongDraws AND handrank169 <= {semibluff_threshold} RaisePot FORCE\n"
        else:  # Aggressive
            code += "// Aggressive approach to donk bets\n"
            code += f"WHEN f$FlopDrawHands Call FORCE\n"
            code += f"WHEN handrank169 <= {round(semibluff_threshold * 0.8)} RaisePot FORCE\n"
        
        code += "\nWHEN Others Fold FORCE\n\n"

        # Facing Check-Raise to C-Bet
        code += "##f$FacingCheckRaiseToCbet##\n"
        code += "// Response when opponent check-raises our c-bet\n\n"
        
        code += "// Continue with strong hands\n"
        code += "WHEN f$FlopStrongHands RaisePot FORCE\n"
        code += "WHEN f$FlopValueHands Call FORCE\n\n"
        
        code += f"// Defense frequency against check-raises\n"
        code += f"WHEN handrank169 <= {checkraise_defense_threshold} Call FORCE\n\n"
        
        code += "// Default fold\n"
        code += "WHEN Others Fold FORCE\n\n"

        # Facing Raise to C-Bet
        code += "##f$FacingRaiseToCbet##\n"
        code += "// Response when opponent raises our c-bet\n\n"
        
        code += "// Continue with strong hands\n"
        code += "WHEN f$FlopStrongHands RaisePot FORCE\n"
        code += "WHEN f$FlopValueHands Call FORCE\n\n"
        
        code += f"// Defense frequency against raises - slightly tighter than vs check-raises\n"
        code += f"WHEN handrank169 <= {round(checkraise_defense_threshold * 0.9)} Call FORCE\n\n"
        
        code += "// Default fold\n"
        code += "WHEN Others Fold FORCE\n\n"

        # Donk Bet
        code += "##f$DonkBet##\n"
        code += "// Donk betting as non-preflop-raiser\n\n"
        
        code += "// Only donk with very strong hands or draws\n"
        code += "WHEN f$FlopStrongHands RaisePot FORCE\n"
        code += f"WHEN f$FlopStrongDraws AND handrank169 <= {round(semibluff_threshold * 0.7)} RaiseBy 50% FORCE\n\n"
        
        code += "// Default check\n"
        code += "WHEN Others Check FORCE\n\n"

        # Betting after opponent checks in position
        code += "##f$BetAfterCheckIP##\n"
        code += "// Betting when checked to in position\n\n"
        
        code += "// Always bet value hands\n"
        code += "WHEN f$FlopValueHands RaiseBy 50% FORCE\n\n"
        
        code += "// Bet draws on wet boards\n"
        code += f"WHEN f$FlopDrawHands AND f$WetBoard AND handrank169 <= {draw_hands_threshold} RaiseBy 50% FORCE\n\n"
        
        code += "// Opportunistic betting when checked to\n"
        code += f"WHEN f$DryBoard AND handrank169 <= {semibluff_threshold} RaiseBy 50% FORCE\n"
        code += f"WHEN handrank169 <= {round(semibluff_threshold * 0.8)} RaiseBy 50% FORCE\n\n"
        
        code += "// Default check back\n"
        code += "WHEN Others Check FORCE\n\n"
        
        return code