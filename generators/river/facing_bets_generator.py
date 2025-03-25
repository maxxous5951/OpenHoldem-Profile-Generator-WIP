"""
Générateur de stratégies face aux mises au turn
"""
from generators.turn.base_generator import BaseTurnGenerator

class FacingBetsGenerator(BaseTurnGenerator):
    """
    Classe pour générer les sections de code pour répondre aux mises des adversaires au turn
    """
    
    def generate_code(self, settings):
        """
        Génère les sections de réponse aux mises adverses du profil turn
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code généré pour les réponses aux mises
        """
        # Extract relevant settings
        turn_checkraise_freq = settings.get("turn_checkraise_freq", 25)
        turn_float_freq = settings.get("turn_float_freq", 30)
        turn_fold_to_cbet_freq = settings.get("turn_fold_to_cbet_freq", 60)
        turn_bluff_raise_freq = settings.get("turn_bluff_raise_freq", 20)
        
        # Global aggression
        aggression = settings.get("aggression", 50)
        aggressive_factor = aggression / 50  # 0-2 range where 1 is neutral
        
        # Calculate thresholds
        turn_checkraise_threshold = self.get_handrank_threshold(turn_checkraise_freq)
        turn_float_threshold = self.get_handrank_threshold(turn_float_freq)
        turn_bluff_raise_threshold = self.get_handrank_threshold(turn_bluff_raise_freq)
        fold_threshold = self.get_handrank_threshold(100 - turn_fold_to_cbet_freq)
        
        # Adjust thresholds based on global aggression
        turn_checkraise_threshold = round(turn_checkraise_threshold * (1.2 - 0.4 * aggressive_factor))
        turn_float_threshold = round(turn_float_threshold * (1.2 - 0.4 * aggressive_factor))
        
        # Generate the code
        code = "// Facing bets functions\n\n"
        
        # Facing Second Barrel
        code += "##f$FacingSecondBarrel##\n"
        code += "// Response when facing a second barrel on the turn\n\n"
        
        code += "// Always continue with strong hands\n"
        code += "WHEN f$TurnStrongHands RaisePot FORCE\n"
        code += "WHEN f$TurnValueHands Call FORCE\n\n"
        
        code += "// Continue with good draws\n"
        code += f"WHEN f$TurnStrongDraws Call FORCE\n\n"
        
        code += "// Check-raise bluff with specific holdings\n"
        code += f"WHEN handrank169 <= {turn_bluff_raise_threshold} AND f$TurnSemiBluffHands RaisePot FORCE\n\n"
        
        code += "// Float with position\n"
        code += f"WHEN f$InPosition AND handrank169 <= {turn_float_threshold} Call FORCE\n\n"
        
        code += "// Call with hands that have showdown value\n"
        code += f"WHEN handrank169 <= {fold_threshold} Call FORCE\n\n"
        
        code += "// Default fold\n"
        code += "WHEN Others Fold FORCE\n\n"

        # Facing Delayed C-Bet
        code += "##f$FacingDelayedCbet##\n"
        code += "// Response when facing a delayed c-bet on the turn\n\n"
        
        code += "// Similar logic to facing a second barrel\n"
        code += "WHEN f$TurnStrongHands RaisePot FORCE\n"
        code += "WHEN f$TurnValueHands Call FORCE\n\n"
        
        code += "// More inclined to raise with draws when villain showed weakness on flop\n"
        code += f"WHEN f$TurnStrongDraws AND handrank169 <= {round(turn_checkraise_threshold * 1.2)} RaisePot FORCE\n"
        code += f"WHEN f$TurnStrongDraws Call FORCE\n\n"
        
        code += "// More aggressive raising range\n"
        code += f"WHEN handrank169 <= {round(turn_bluff_raise_threshold * 1.2)} RaisePot FORCE\n\n"
        
        code += "// Default fold\n"
        code += "WHEN Others Fold FORCE\n\n"

        # Facing Check-Raise to Second Barrel
        code += "##f$FacingCheckRaiseToSecondBarrel##\n"
        code += "// Response when opponent check-raises our second barrel\n\n"
        
        code += "// Continue with strong hands\n"
        code += "WHEN f$TurnStrongHands RaisePot FORCE\n"
        code += "WHEN f$TurnValueHands Call FORCE\n\n"
        
        code += "// Continue with strong draws\n"
        code += f"WHEN f$TurnStrongDraws AND handrank169 <= {round(turn_checkraise_threshold * 0.8)} Call FORCE\n\n"
        
        code += "// Defense frequency against check-raises\n"
        code += f"WHEN handrank169 <= {turn_checkraise_threshold} Call FORCE\n\n"
        
        code += "// Default fold\n"
        code += "WHEN Others Fold FORCE\n\n"

        # Facing Raise to Second Barrel
        code += "##f$FacingRaiseToSecondBarrel##\n"
        code += "// Response when opponent raises our second barrel\n\n"
        
        code += "// Continue with very strong hands\n"
        code += "WHEN f$TurnStrongHands RaisePot FORCE\n"
        code += "WHEN f$TurnValueHands Call FORCE\n\n"
        
        code += "// Be more cautious with draws\n"
        code += f"WHEN f$TurnStrongDraws AND handrank169 <= {round(turn_checkraise_threshold * 0.7)} Call FORCE\n\n"
        
        code += "// Default fold\n"
        code += "WHEN Others Fold FORCE\n\n"
        
        return code