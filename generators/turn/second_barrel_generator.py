"""
Générateur de stratégies de Second Barrel au turn
"""
from generators.turn.base_generator import BaseTurnGenerator

class SecondBarrelGenerator(BaseTurnGenerator):
    """
    Classe pour générer les sections de code de Second Barrel au turn
    """
    
    def generate_code(self, settings):
        """
        Génère la section Second Barrel du profil turn
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code généré pour les stratégies de Second Barrel
        """
        # Extract relevant settings
        second_barrel_freq = settings.get("second_barrel_freq", 60)
        delayed_cbet_freq = settings.get("delayed_cbet_freq", 40)
        ip_turn_bet_size = settings.get("ip_turn_bet_size", "66")
        oop_turn_bet_size = settings.get("oop_turn_bet_size", "75")
        scare_card_adjust = settings.get("scare_card_adjust", -15) / 100.0  # Convert to decimal
        draw_complete_adjust = settings.get("draw_complete_adjust", 10) / 100.0  # Convert to decimal
        
        # Global aggression
        aggression = settings.get("aggression", 50)
        aggressive_factor = aggression / 50  # 0-2 range where 1 is neutral
        
        # Calculate thresholds
        second_barrel_threshold = self.get_handrank_threshold(second_barrel_freq)
        delayed_cbet_threshold = self.get_handrank_threshold(delayed_cbet_freq)
        
        # Adjust thresholds based on global aggression
        second_barrel_threshold = round(second_barrel_threshold * (1.2 - 0.4 * aggressive_factor))
        delayed_cbet_threshold = round(delayed_cbet_threshold * (1.2 - 0.4 * aggressive_factor))
        
        # Generate the code
        code = "// Second Barrel and Delayed C-bet functions\n\n"
        
        # Second Barrel
        code += "##f$TurnSecondBarrel##\n"
        code += f"// Second barrel after betting the flop, default size: {ip_turn_bet_size}% of pot\n"
        code += "// Adjust based on board texture and previous actions\n\n"
        
        code += "// Always continue with made hands\n"
        code += f"WHEN f$TurnValueHands RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        code += "// Continue with strong draws\n"
        code += f"WHEN f$TurnStrongDraws RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        code += "// Board texture-based adjustments\n"
        code += f"WHEN f$ScareCard AND handrank169 <= {round(second_barrel_threshold * (1 + scare_card_adjust))} RaiseBy {ip_turn_bet_size}% FORCE\n"
        code += f"WHEN f$DrawComplete AND handrank169 <= {round(second_barrel_threshold * (1 + draw_complete_adjust))} RaiseBy {ip_turn_bet_size}% FORCE\n"
        code += f"WHEN f$WetBoard AND handrank169 <= {round(second_barrel_threshold * 0.9)} RaiseBy {ip_turn_bet_size}% FORCE\n"
        code += f"WHEN f$DryBoard AND handrank169 <= {round(second_barrel_threshold * 1.1)} RaiseBy {ip_turn_bet_size}% FORCE\n"
        code += f"WHEN handrank169 <= {second_barrel_threshold} RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        code += "// Default check\n"
        code += "WHEN Others Check FORCE\n\n"

        # Delayed C-Bet
        code += "##f$TurnDelayedCbet##\n"
        code += f"// Delayed c-bet after checking the flop, default size: {ip_turn_bet_size}% of pot\n"
        code += "// Generally more selective than a second barrel\n\n"
        
        code += "// Always bet with made hands\n"
        code += f"WHEN f$TurnValueHands RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        code += "// Continue with strong draws on appropriate boards\n"
        code += f"WHEN f$TurnStrongDraws AND f$WetBoard RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        code += "// Board texture-based adjustments\n"
        code += f"WHEN f$ScareCard AND handrank169 <= {round(delayed_cbet_threshold * (1 + scare_card_adjust * 0.8))} RaiseBy {ip_turn_bet_size}% FORCE\n"
        code += f"WHEN f$DrawComplete AND handrank169 <= {round(delayed_cbet_threshold * (1 + draw_complete_adjust * 0.8))} RaiseBy {ip_turn_bet_size}% FORCE\n"
        code += f"WHEN f$DryBoard AND handrank169 <= {round(delayed_cbet_threshold * 1.1)} RaiseBy {ip_turn_bet_size}% FORCE\n"
        code += f"WHEN handrank169 <= {delayed_cbet_threshold} RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        code += "// Default check\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # Turn Continuation After Flop Bet
        code += "##f$TurnContinuationAfterFlopBet##\n"
        code += f"// In position facing a check after we bet the flop, default size: {ip_turn_bet_size}% of pot\n\n"
        
        code += "// Continue betting with value hands\n"
        code += f"WHEN f$TurnValueHands RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        code += "// Be selective with semi-bluffs\n"
        code += f"WHEN f$TurnStrongDraws AND handrank169 <= {round(second_barrel_threshold * 0.8)} RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        code += "// Board texture-based continuation\n"
        code += f"WHEN f$DryBoard AND handrank169 <= {round(second_barrel_threshold * 0.9)} RaiseBy {ip_turn_bet_size}% FORCE\n"
        code += f"WHEN handrank169 <= {round(second_barrel_threshold * 0.7)} RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        code += "// Default check back\n"
        code += "WHEN Others Check FORCE\n\n"
        
        return code