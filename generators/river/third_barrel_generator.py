"""
Générateur de stratégies de Third Barrel au river
"""
from generators.river.base_generator import BaseRiverGenerator

class ThirdBarrelGenerator(BaseRiverGenerator):
    """
    Classe pour générer les sections de code de Third Barrel au river
    """
    
    def generate_code(self, settings):
        """
        Génère la section Third Barrel du profil river
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code généré pour les stratégies de Third Barrel
        """
        # Extract relevant settings
        third_barrel_freq = settings.get("third_barrel_freq", 40)
        delayed_second_barrel_freq = settings.get("delayed_second_barrel_freq", 30)
        ip_river_bet_size = settings.get("ip_river_bet_size", "75")
        oop_river_bet_size = settings.get("oop_river_bet_size", "75")
        river_bluff_range = settings.get("river_bluff_range", 15)
        
        # Global aggression
        aggression = settings.get("aggression", 50)
        aggressive_factor = aggression / 50  # 0-2 range where 1 is neutral
        
        # Calculate thresholds
        third_barrel_threshold = self.get_handrank_threshold(third_barrel_freq)
        delayed_second_barrel_threshold = self.get_handrank_threshold(delayed_second_barrel_freq)
        river_bluff_threshold = self.get_handrank_threshold(river_bluff_range)
        
        # Adjust thresholds based on global aggression
        third_barrel_threshold = round(third_barrel_threshold * (1.2 - 0.4 * aggressive_factor))
        delayed_second_barrel_threshold = round(delayed_second_barrel_threshold * (1.2 - 0.4 * aggressive_factor))
        river_bluff_threshold = round(river_bluff_threshold * (1.2 - 0.4 * aggressive_factor))
        
        # Generate the code
        code = "// Third Barrel and Delayed Second Barrel functions\n\n"
        
        # Third Barrel
        code += "##f$RiverThirdBarrel##\n"
        code += f"// Third barrel after betting flop and turn, default size: {ip_river_bet_size}% of pot\n"
        code += "// At river, we polarize to value bets and bluffs\n\n"
        
        code += "// Value betting\n"
        code += f"WHEN f$RiverValueHands RaiseBy {ip_river_bet_size}% FORCE\n\n"
        
        code += "// Bluffing with missed draws and blockers\n"
        code += f"WHEN f$RiverBluffCandidates AND handrank169 <= {river_bluff_threshold} RaiseBy {ip_river_bet_size}% FORCE\n\n"
        
        code += "// Board texture-based decisions\n"
        code += f"WHEN f$DrawHeavyBoard AND handrank169 <= {round(third_barrel_threshold * 0.8)} RaiseBy {ip_river_bet_size}% FORCE\n"
        code += f"WHEN f$PairedBoard AND handrank169 <= {round(third_barrel_threshold * 0.9)} RaiseBy {ip_river_bet_size}% FORCE\n"
        code += f"WHEN handrank169 <= {third_barrel_threshold} RaiseBy {ip_river_bet_size}% FORCE\n\n"
        
        code += "// Check back marginal hands\n"
        code += "WHEN Others Check FORCE\n\n"

        # Delayed Second Barrel on River
        code += "##f$RiverDelayedSecondBarrel##\n"
        code += f"// Delayed second barrel after checking turn, default size: {ip_river_bet_size}% of pot\n"
        code += "// More selective with value betting, less bluffing\n\n"
        
        code += "// Value betting\n"
        code += f"WHEN f$RiverStrongHands RaiseBy {ip_river_bet_size}% FORCE\n\n"
        
        code += "// Occasionally bluff with missed draws\n"
        code += f"WHEN f$RiverBluffCandidates AND handrank169 <= {round(river_bluff_threshold * 0.7)} RaiseBy {ip_river_bet_size}% FORCE\n\n"
        
        code += "// Default check\n"
        code += "WHEN Others Check FORCE\n\n"

        # River Continuation After Turn Bet
        code += "##f$RiverContinuationAfterTurnBet##\n"
        code += f"// In position facing a check after we bet the turn, default size: {ip_river_bet_size}% of pot\n\n"
        
        code += "// Value bet with strong hands\n"
        code += f"WHEN f$RiverValueHands RaiseBy {ip_river_bet_size}% FORCE\n\n"
        
        code += "// Selective bluffing\n"
        code += f"WHEN f$RiverBluffCandidates AND handrank169 <= {round(river_bluff_threshold * 0.8)} RaiseBy {ip_river_bet_size}% FORCE\n\n"
        
        code += "// Check back with showdown value\n"
        code += f"WHEN handrank169 <= {self.get_handrank_threshold(settings.get('river_check_behind_range', 80))} Check FORCE\n\n"
        
        code += "// Default check back\n"
        code += "WHEN Others Check FORCE\n\n"
        
        return code
