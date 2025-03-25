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
        # Extraire les paramètres pour chaque position
        ep1_range = settings["ep1_range"]
        ep2_range = settings["ep2_range"]
        ep3_range = settings["ep3_range"]
        mp1_range = settings["mp1_range"]
        mp2_range = settings["mp2_range"]
        mp3_range = settings["mp3_range"]
        co_range = settings["co_range"]
        btn_range = settings["btn_range"]
        sb_range = settings["sb_range"]
        bb_range = settings["bb_range"]
        
        # Extraire les paramètres pour le sizing
        ep1_sizing = settings["ep1_sizing"]
        ep2_sizing = settings["ep2_sizing"]
        ep3_sizing = settings["ep3_sizing"]
        mp1_sizing = settings["mp1_sizing"]
        mp2_sizing = settings["mp2_sizing"]
        mp3_sizing = settings["mp3_sizing"]
        co_sizing = settings["co_sizing"]
        btn_sizing = settings["btn_sizing"]
        sb_sizing = settings["sb_sizing"]
        
        limp_frequency = settings["limp_frequency"]
        tightness = settings["tightness"]
        aggressive_factor = settings["aggression"] / 50  # 0-2 range where 1 is neutral
        limp_factor = limp_frequency / 50
        
        # Calculer les seuils pour chaque position
        ep1_raise_threshold = self.get_handrank_threshold(ep1_range)
        ep2_raise_threshold = self.get_handrank_threshold(ep2_range)
        ep3_raise_threshold = self.get_handrank_threshold(ep3_range)
        mp1_raise_threshold = self.get_handrank_threshold(mp1_range)
        mp2_raise_threshold = self.get_handrank_threshold(mp2_range)
        mp3_raise_threshold = self.get_handrank_threshold(mp3_range)
        co_raise_threshold = self.get_handrank_threshold(co_range)
        btn_raise_threshold = self.get_handrank_threshold(btn_range)
        sb_raise_threshold = self.get_handrank_threshold(sb_range)
        bb_raise_threshold = self.get_handrank_threshold(bb_range)
        tight_threshold = self.get_handrank_threshold(tightness)
        
        # Ajuster les tailles de relance
        ep1_open_raise = self.calculate_raise_size(ep1_sizing, 0, aggressive_factor)
        ep2_open_raise = self.calculate_raise_size(ep2_sizing, 0, aggressive_factor)
        ep3_open_raise = self.calculate_raise_size(ep3_sizing, 0, aggressive_factor)
        mp1_open_raise = self.calculate_raise_size(mp1_sizing, 0, aggressive_factor)
        mp2_open_raise = self.calculate_raise_size(mp2_sizing, 0, aggressive_factor)
        mp3_open_raise = self.calculate_raise_size(mp3_sizing, 0, aggressive_factor)
        co_open_raise = self.calculate_raise_size(co_sizing, 0, aggressive_factor)
        btn_open_raise = self.calculate_raise_size(btn_sizing, 0, aggressive_factor)
        sb_open_raise = self.calculate_raise_size(sb_sizing, 0, aggressive_factor)
        
        # Générer le code
        code = "//*****************************************************************************\n"
        code += "//\n"
        code += "// OPEN RAISE STRATEGY\n"
        code += "//\n"
        code += f"// EP1 (UTG) Range: {ep1_range}% (Threshold: {ep1_raise_threshold})\n"
        code += f"// EP2 (UTG+1) Range: {ep2_range}% (Threshold: {ep2_raise_threshold})\n"
        code += f"// EP3 (UTG+2) Range: {ep3_range}% (Threshold: {ep3_raise_threshold})\n"
        code += f"// MP1 Range: {mp1_range}% (Threshold: {mp1_raise_threshold})\n"
        code += f"// MP2 Range: {mp2_range}% (Threshold: {mp2_raise_threshold})\n"
        code += f"// MP3 (HJ) Range: {mp3_range}% (Threshold: {mp3_raise_threshold})\n"
        code += f"// CO Range: {co_range}% (Threshold: {co_raise_threshold})\n"
        code += f"// BTN Range: {btn_range}% (Threshold: {btn_raise_threshold})\n"
        code += f"// SB Range: {sb_range}% (Threshold: {sb_raise_threshold})\n"
        code += f"// BB Range: {bb_range}% (Threshold: {bb_raise_threshold})\n"
        code += f"// EP1 Sizing: {ep1_open_raise}BB\n"
        code += f"// EP2 Sizing: {ep2_open_raise}BB\n"
        code += f"// EP3 Sizing: {ep3_open_raise}BB\n"
        code += f"// MP1 Sizing: {mp1_open_raise}BB\n"
        code += f"// MP2 Sizing: {mp2_open_raise}BB\n"
        code += f"// MP3 Sizing: {mp3_open_raise}BB\n"
        code += f"// CO Sizing: {co_open_raise}BB\n"
        code += f"// BTN Sizing: {btn_open_raise}BB\n"
        code += f"// SB Sizing: {sb_open_raise}BB\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"

        # Open Raise ou Open Limp
        code += "##f$OpenRaiseOrOpenLimp##\n"
        code += "// No action (limp or raise) before us. Hero can Open the game by Raising or Limping\n"
        code += "WHEN InEarlyPosition1 RETURN f$OpenRaise_EarlyPosition1 FORCE\n"
        code += "WHEN InEarlyPosition2 RETURN f$OpenRaise_EarlyPosition2 FORCE\n"
        code += "WHEN InEarlyPosition3 RETURN f$OpenRaise_EarlyPosition3 FORCE\n"
        code += "WHEN InMiddlePosition1 RETURN f$OpenRaise_MiddlePosition1 FORCE\n"
        code += "WHEN InMiddlePosition2 RETURN f$OpenRaise_MiddlePosition2 FORCE\n"
        code += "WHEN InMiddlePosition3 RETURN f$OpenRaise_MiddlePosition3 FORCE\n"
        code += "WHEN InCutOff RETURN f$OpenRaise_CutOff FORCE\n"
        code += "WHEN InButton RETURN f$OpenRaise_Button FORCE\n"
        code += "WHEN InSmallBlind RETURN f$OpenRaise_SB FORCE\n"
        code += "WHEN InBigBlind RETURN Check FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"

        # Early Position 1 (UTG) Open Raising
        code += "##f$OpenRaise_EarlyPosition1##\n"
        code += f"WHEN handrank169 <= {ep1_raise_threshold} RETURN {ep1_open_raise} FORCE\n"
        code += f"WHEN handrank169 <= {round(tight_threshold * 0.5 * limp_factor)} RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"
        
        # Early Position 2 (UTG+1) Open Raising
        code += "##f$OpenRaise_EarlyPosition2##\n"
        code += f"WHEN handrank169 <= {ep2_raise_threshold} RETURN {ep2_open_raise} FORCE\n"
        code += f"WHEN handrank169 <= {round(tight_threshold * 0.55 * limp_factor)} RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"
        
        # Early Position 3 (UTG+2) Open Raising
        code += "##f$OpenRaise_EarlyPosition3##\n"
        code += f"WHEN handrank169 <= {ep3_raise_threshold} RETURN {ep3_open_raise} FORCE\n"
        code += f"WHEN handrank169 <= {round(tight_threshold * 0.6 * limp_factor)} RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"
        
        # Middle Position 1 Open Raising
        code += "##f$OpenRaise_MiddlePosition1##\n"
        code += f"WHEN handrank169 <= {mp1_raise_threshold} RETURN {mp1_open_raise} FORCE\n"
        code += f"WHEN handrank169 <= {round(tight_threshold * 0.65 * limp_factor)} RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"
        
        # Middle Position 2 Open Raising
        code += "##f$OpenRaise_MiddlePosition2##\n"
        code += f"WHEN handrank169 <= {mp2_raise_threshold} RETURN {mp2_open_raise} FORCE\n"
        code += f"WHEN handrank169 <= {round(tight_threshold * 0.7 * limp_factor)} RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"
        
        # Middle Position 3 (Hijack) Open Raising
        code += "##f$OpenRaise_MiddlePosition3##\n"
        code += f"WHEN handrank169 <= {mp3_raise_threshold} RETURN {mp3_open_raise} FORCE\n"
        code += f"WHEN handrank169 <= {round(tight_threshold * 0.75 * limp_factor)} RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"
        
        # Cut Off Open Raising
        code += "##f$OpenRaise_CutOff##\n"
        code += f"WHEN handrank169 <= {co_raise_threshold} RETURN {co_open_raise} FORCE\n"
        code += f"WHEN handrank169 <= {round(tight_threshold * 0.8 * limp_factor)} RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"
        
        # Button Open Raising
        code += "##f$OpenRaise_Button##\n"
        code += f"WHEN handrank169 <= {btn_raise_threshold} RETURN {btn_open_raise} FORCE\n"
        code += f"WHEN handrank169 <= {round(tight_threshold * 0.85 * limp_factor)} RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"
        
        # Small Blind Open Raising
        code += "##f$OpenRaise_SB##\n"
        code += f"WHEN handrank169 <= {sb_raise_threshold} RETURN {sb_open_raise} FORCE\n"
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
