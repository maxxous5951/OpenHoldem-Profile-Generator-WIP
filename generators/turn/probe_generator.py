"""
Générateur pour les stratégies de probe betting et checking au turn
"""
from generators.turn.base_generator import BaseTurnGenerator

class ProbeGenerator(BaseTurnGenerator):
    """
    Classe pour générer les sections de code de probe betting au turn
    """
    
    def generate_code(self, settings):
        """
        Génère la section de probe betting du profil turn
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code généré pour les stratégies de probe betting
        """
        # Extract relevant settings
        turn_probe_freq = settings.get("turn_probe_freq", 35)
        ip_turn_bet_size = settings.get("ip_turn_bet_size", "66")
        oop_turn_bet_size = settings.get("oop_turn_bet_size", "75")
        
        # Global aggression
        aggression = settings.get("aggression", 50)
        aggressive_factor = aggression / 50  # 0-2 range where 1 is neutral
        
        # Calculate thresholds
        turn_probe_threshold = self.get_handrank_threshold(turn_probe_freq)
        
        # Adjust threshold based on global aggression
        turn_probe_threshold = round(turn_probe_threshold * (1.2 - 0.4 * aggressive_factor))
        
        # Generate the code
        code = "// Probe betting and checking functions\n\n"
        
        # Turn Probe After Checked Flop
        code += "##f$TurnProbeAfterCheckedFlop##\n"
        code += f"// Probe betting when in position after a checked flop, default size: {ip_turn_bet_size}% of pot\n\n"
        
        code += "// Always bet with made hands\n"
        code += f"WHEN f$TurnValueHands RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        code += "// Probe with strong draws\n"
        code += f"WHEN f$TurnStrongDraws RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        code += "// Opportunistic betting when checked to twice\n"
        code += f"WHEN handrank169 <= {turn_probe_threshold} RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        code += "// Default check back\n"
        code += "WHEN Others Check FORCE\n\n"

        # Turn OOP After Checked Flop
        code += "##f$TurnOOPAfterCheckedFlop##\n"
        code += f"// OOP lead betting after a checked flop, default size: {oop_turn_bet_size}% of pot\n\n"
        
        code += "// Only lead with strong hands\n"
        code += f"WHEN f$TurnValueHands RaiseBy {oop_turn_bet_size}% FORCE\n\n"
        
        code += "// Lead with some strong draws\n"
        code += f"WHEN f$TurnStrongDraws AND handrank169 <= {round(turn_probe_threshold * 0.7)} RaiseBy {oop_turn_bet_size}% FORCE\n\n"
        
        code += "// Default check\n"
        code += "WHEN Others Check FORCE\n\n"
        
        return code