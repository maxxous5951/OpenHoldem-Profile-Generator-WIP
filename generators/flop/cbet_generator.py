"""
Générateur de stratégies de C-Bet au flop
"""
from generators.flop.base_generator import BaseFlopGenerator

class CBetGenerator(BaseFlopGenerator):
    """
    Classe pour générer les sections de code de C-Bet au flop
    """
    
    def generate_code(self, settings):
        """
        Génère la section C-Bet du profil flop
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code généré pour les stratégies de C-Bet
        """
        # Extract relevant settings
        ip_cbet_freq = settings.get("ip_cbet_freq", 70)
        oop_cbet_freq = settings.get("oop_cbet_freq", 60)
        ip_cbet_size = settings.get("ip_cbet_size", "50")
        oop_cbet_size = settings.get("oop_cbet_size", "66")
        dry_board_adjust = settings.get("dry_board_adjust", 20) / 100.0
        wet_board_adjust = settings.get("wet_board_adjust", -20) / 100.0
        multiway_cbet_freq = settings.get("multiway_cbet_freq", 40)
        multiway_value_range = settings.get("multiway_value_range", 25)
        
        # Global aggression
        aggression = settings.get("aggression", 50)
        aggressive_factor = aggression / 50  # 0-2 range where 1 is neutral
        
        # Calculate thresholds
        ip_cbet_threshold = self.get_handrank_threshold(ip_cbet_freq)
        oop_cbet_threshold = self.get_handrank_threshold(oop_cbet_freq)
        multiway_cbet_threshold = self.get_handrank_threshold(multiway_cbet_freq)
        multiway_value_threshold = self.get_handrank_threshold(multiway_value_range)
        
        # Generate the code
        code = "// C-Bet functions\n\n"
        
        # C-Bet In Position
        code += "##f$FlopCbetIP##\n"
        code += f"// C-Bet in position, default size: {ip_cbet_size}% of pot\n"
        code += "// Adjust based on board texture and player count\n\n"
        
        code += "// Multiway pot considerations\n"
        code += f"WHEN nopponentsplaying > 2 AND handrank169 <= {multiway_value_threshold} RaiseBy {ip_cbet_size}% FORCE\n"
        code += f"WHEN nopponentsplaying > 2 Check FORCE\n\n"
        
        code += "// Value hands always c-bet\n"
        code += f"WHEN f$FlopValueHands RaiseBy {ip_cbet_size}% FORCE\n\n"
        
        code += "// Board texture-based adjustments\n"
        code += f"WHEN f$DryBoard AND handrank169 <= {ip_cbet_threshold * (1 + dry_board_adjust)} RaiseBy {ip_cbet_size}% FORCE\n"
        code += f"WHEN f$WetBoard AND handrank169 <= {ip_cbet_threshold * (1 + wet_board_adjust)} RaiseBy {ip_cbet_size}% FORCE\n"
        code += f"WHEN handrank169 <= {ip_cbet_threshold} RaiseBy {ip_cbet_size}% FORCE\n\n"
        
        code += "WHEN Others Check FORCE\n\n"

        # C-Bet Out Of Position
        code += "##f$FlopCbetOOP##\n"
        code += f"// C-Bet out of position, default size: {oop_cbet_size}% of pot\n"
        code += "// Generally more selective when OOP\n\n"
        
        code += "// Multiway pot considerations - even tighter\n"
        code += f"WHEN nopponentsplaying > 2 AND handrank169 <= {round(multiway_value_threshold * 0.8)} RaiseBy {oop_cbet_size}% FORCE\n"
        code += f"WHEN nopponentsplaying > 2 Check FORCE\n\n"
        
        code += "// Value hands always c-bet\n"
        code += f"WHEN f$FlopValueHands RaiseBy {oop_cbet_size}% FORCE\n\n"
        
        code += "// Board texture-based adjustments - more conservative when OOP\n"
        code += f"WHEN f$DryBoard AND handrank169 <= {oop_cbet_threshold * (1 + dry_board_adjust * 0.8)} RaiseBy {oop_cbet_size}% FORCE\n"
        code += f"WHEN f$WetBoard AND handrank169 <= {oop_cbet_threshold * (1 + wet_board_adjust * 0.8)} RaiseBy {oop_cbet_size}% FORCE\n"
        code += f"WHEN handrank169 <= {oop_cbet_threshold} RaiseBy {oop_cbet_size}% FORCE\n\n"
        
        code += "WHEN Others Check FORCE\n\n"
        
        return code