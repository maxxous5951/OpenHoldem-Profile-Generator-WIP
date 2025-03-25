"""
Générateur pour les stratégies de probe betting et checking au river
"""
from generators.river.base_generator import BaseRiverGenerator

class ProbeGenerator(BaseRiverGenerator):
    """
    Classe pour générer les sections de code de probe betting au river
    """
    
    def generate_code(self, settings):
        """
        Génère la section de probe betting du profil river
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code généré pour les stratégies de probe betting
        """
        # Extract relevant settings
        river_probe_freq = settings.get("river_probe_freq", 25)
        ip_river_bet_size = settings.get("ip_river_bet_size", "75")
        oop_river_bet_size = settings.get("oop_river_bet_size", "75")
        river_bluff_range = settings.get("river_bluff_range", 15)
        river_check_behind_range = settings.get("river_check_behind_range", 80)
        
        # Global aggression
        aggression = settings.get("aggression", 50)
        aggressive_factor = aggression / 50  # 0-2 range where 1 is neutral
        
        # Calculate thresholds
        river_probe_threshold = self.get_handrank_threshold(river_probe_freq)
        river_bluff_threshold = self.get_handrank_threshold(river_bluff_range)
        river_check_behind_threshold = self.get_handrank_threshold(river_check_behind_range)
        
        # Adjust threshold based on global aggression
        river_probe_threshold = round(river_probe_threshold * (1.2 - 0.4 * aggressive_factor))
        river_bluff_threshold = round(river_bluff_threshold * (1.2 - 0.4 * aggressive_factor))
        
        # Generate the code
        code = "// Probe betting and checking functions\n\n"
        
        # River Probe After Checked Turn
        code += "##f$RiverProbeAfterCheckedTurn##\n"
        code += f"// Probe betting when in position after a checked turn, default size: {ip_river_bet_size}% of pot\n\n"
        
        code += "// Value bet with strong hands\n"
        code += f"WHEN f$RiverValueHands RaiseBy {ip_river_bet_size}% FORCE\n\n"
        
        code += "// Opportunistic betting when checked to twice\n"
        code += f"WHEN f$RiverBluffCandidates AND handrank169 <= {river_probe_threshold} RaiseBy {ip_river_bet_size}% FORCE\n\n"
        
        code += "// Check back with showdown value\n"
        code += f"WHEN handrank169 <= {river_check_behind_threshold} Check FORCE\n\n"
        
        code += "// Default check back\n"
        code += "WHEN Others Check FORCE\n\n"

        # River OOP After Checked Turn
        code += "##f$RiverOOPAfterCheckedTurn##\n"
        code += f"// OOP lead betting after a checked turn, default size: {oop_river_bet_size}% of pot\n\n"
        
        code += "// Only lead with strong hands\n"
        code += f"WHEN f$RiverStrongHands RaiseBy {oop_river_bet_size}% FORCE\n\n"
        
        code += "// Occasionally lead as a bluff\n"
        code += f"WHEN f$RiverBluffCandidates AND handrank169 <= {round(river_probe_threshold * 0.6)} RaiseBy {oop_river_bet_size}% FORCE\n\n"
        
        code += "// Default check\n"
        code += "WHEN Others Check FORCE\n\n"
        
        return code
