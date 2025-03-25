"""
Générateur de stratégies d'open raise
"""
from generators.preflop.base_generator import BaseProfileGenerator

class OpenRaiseGenerator(BaseProfileGenerator):
    """
    Classe pour générer les sections de code d'open raise
    """
    
    def generate_code(self, settings):
        """
        Génère la section d'open raise du profil
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code généré pour l'open raise
        """
        # Extraire les paramètres pertinents
        ep_range = settings["ep_range"]
        mp_range = settings["mp_range"]
        lp_range = settings["lp_range"]
        ep_sizing = settings["ep_sizing"]
        mp_sizing = settings["mp_sizing"]
        lp_sizing = settings["lp_sizing"]
        limp_frequency = settings["limp_frequency"]
        tightness = settings["tightness"]
        aggressive_factor = settings["aggression"] / 50  # 0-2 range where 1 is neutral
        limp_factor = limp_frequency / 50
        
        # Calculer les seuils
        ep_raise_threshold = self.get_handrank_threshold(ep_range)
        mp_raise_threshold = self.get_handrank_threshold(mp_range)
        lp_raise_threshold = self.get_handrank_threshold(lp_range)
        tight_threshold = self.get_handrank_threshold(tightness)
        
        # Ajuster les tailles de relance
        ep_open_raise = self.calculate_raise_size(ep_sizing, 0, aggressive_factor)
        mp_open_raise = self.calculate_raise_size(mp_sizing, 0, aggressive_factor)
        lp_open_raise = self.calculate_raise_size(lp_sizing, 0, aggressive_factor)
        
        # Générer le code
        code = "//*****************************************************************************\n"
        code += "//\n"
        code += "// OPEN RAISE STRATEGY\n"
        code += "//\n"
        code += f"// Early Position Range: {ep_range}% (Threshold: {ep_raise_threshold})\n"
        code += f"// Middle Position Range: {mp_range}% (Threshold: {mp_raise_threshold})\n"
        code += f"// Late Position Range: {lp_range}% (Threshold: {lp_raise_threshold})\n"
        code += f"// Early Position Sizing: {ep_open_raise}BB\n"
        code += f"// Middle Position Sizing: {mp_open_raise}BB\n"
        code += f"// Late Position Sizing: {lp_open_raise}BB\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"

        # Open Raise ou Open Limp
        code += "##f$OpenRaiseOrOpenLimp##\n"
        code += "// No action (limp or raise) before us. Hero can Open the game by Raising or Limping\n"
        code += "WHEN InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3 RETURN f$OpenRaise_EarlyPosition FORCE\n"
        code += "WHEN InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3 RETURN f$OpenRaise_MiddlePosition FORCE\n"
        code += "WHEN InCutOff OR InButton RETURN f$OpenRaise_LatePosition FORCE\n"
        code += "WHEN InSmallBlind RETURN f$OpenRaise_SB FORCE\n"
        code += "WHEN InBigBlind RETURN Check FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"

        # Early Position Open Raising
        code += "##f$OpenRaise_EarlyPosition##\n"
        code += f"WHEN handrank169 <= {ep_raise_threshold} RETURN {ep_open_raise} FORCE\n"
        code += f"WHEN handrank169 <= {round(tight_threshold * 0.7 * limp_factor)} RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"
        
        # Middle Position Open Raising
        code += "##f$OpenRaise_MiddlePosition##\n"
        code += f"WHEN handrank169 <= {mp_raise_threshold} RETURN {mp_open_raise} FORCE\n"
        code += f"WHEN handrank169 <= {round(tight_threshold * 0.85 * limp_factor)} RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"
        
        # Late Position Open Raising
        code += "##f$OpenRaise_LatePosition##\n"
        code += f"WHEN handrank169 <= {lp_raise_threshold} RETURN {lp_open_raise} FORCE\n"
        code += f"WHEN handrank169 <= {round(tight_threshold * limp_factor)} RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"
        
        # Small Blind Open Raising
        code += "##f$OpenRaise_SB##\n"
        code += f"WHEN handrank169 <= {round(lp_raise_threshold * 0.9)} RETURN {lp_open_raise} FORCE\n"
        code += f"WHEN handrank169 <= {round(tight_threshold * 0.9 * limp_factor)} RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"

        # Limp Or Isolate Limpers
        code += "##f$LimpOrIsolateLimpers##\n"
        code += "// 1 or more limps before us. Hero can Limp too or Raise to isolate the limpers\n"
        code += "WHEN f$LimpOrIsolateLimpers_Decision = 2 RETURN f$IsolateSize FORCE\n"
        code += "WHEN f$LimpOrIsolateLimpers_Decision = 1 RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"

        # Isolate sizing calculation based on number of limpers
        code += "##f$IsolateSize##\n"
        code += f"// Base open size plus 1BB per limper\n"
        code += f"Calls * 1 + {self.calculate_raise_size(settings['open_raise_size'], 0, aggressive_factor)}\n\n"

        code += "##f$LimpOrIsolateLimpers_Decision##\n"
        code += "// 0 = Fold, 1 = Limp, 2 = Raise\n"
        code += "// More aggressive with fewer limpers, tighter with more\n"
        code += f"WHEN Calls = 1 AND handrank169 <= {round(tight_threshold * 0.7)} RETURN 2 FORCE\n"
        code += f"WHEN Calls = 1 AND handrank169 <= {round(tight_threshold * 0.9 * limp_factor)} RETURN 1 FORCE\n\n"

        code += f"WHEN Calls = 2 AND handrank169 <= {round(tight_threshold * 0.6)} RETURN 2 FORCE\n"
        code += f"WHEN Calls = 2 AND handrank169 <= {round(tight_threshold * 0.85 * limp_factor)} RETURN 1 FORCE\n\n"

        code += f"WHEN Calls >= 3 AND handrank169 <= {round(tight_threshold * 0.5)} RETURN 2 FORCE\n"
        code += f"WHEN Calls >= 3 AND handrank169 <= {round(tight_threshold * 0.8 * limp_factor)} RETURN 1 FORCE\n\n"

        code += "// Position based adjustments - more aggressive in position\n"
        code += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(tight_threshold * 0.75)} RETURN 2 FORCE\n"
        code += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(tight_threshold * 0.65)} RETURN 2 FORCE\n\n"

        code += "WHEN Others RETURN 0 FORCE\n\n"
        
        return code
