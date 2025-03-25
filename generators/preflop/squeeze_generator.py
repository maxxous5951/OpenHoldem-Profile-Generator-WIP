"""
Générateur de stratégies de squeeze
"""
from generators.preflop.base_generator import BaseProfileGenerator

class SqueezeGenerator(BaseProfileGenerator):
    """
    Classe pour générer les sections de code de squeeze
    """
    
    def generate_code(self, settings):
        """
        Génère la section de squeeze du profil
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code généré pour les stratégies de squeeze
        """
        # Extraire les paramètres spécifiques
        squeeze_1caller = settings["squeeze_1caller"]
        squeeze_multi = settings["squeeze_multi"]
        squeeze_sizing = settings["squeeze_sizing"]
        blinds_squeeze = settings["blinds_squeeze"] / 100.0
        btn_squeeze = settings["btn_squeeze"] / 100.0
        squeeze_frequency = settings["squeeze_frequency"]
        tightness = settings["tightness"]
        
        # Facteurs d'ajustement basés sur l'agressivité
        aggressive_factor = settings["aggression"] / 50
        squeeze_adjustment = 1 + (aggressive_factor - 1) * 0.7
        
        # Calculer les seuils
        squeeze_1caller_threshold = self.get_handrank_threshold(squeeze_1caller)
        squeeze_multi_threshold = self.get_handrank_threshold(squeeze_multi)
        tight_threshold = self.get_handrank_threshold(tightness)
        squeeze_threshold = self.get_handrank_threshold(squeeze_frequency * squeeze_adjustment)
        
        # Ajuster taille squeeze
        adjusted_squeeze_size = self.calculate_raise_size(squeeze_sizing, 0, aggressive_factor * 1.2)
        
        # Générer le code
        code = "//*****************************************************************************\n"
        code += "//\n"
        code += "// SQUEEZE STRATEGY\n"
        code += "//\n"
        code += f"// Squeeze Frequency: {squeeze_frequency}% (Adjusted: {squeeze_frequency * squeeze_adjustment:.1f}%)\n"
        code += f"// Squeeze vs 1 Caller: {squeeze_1caller}% (Threshold: {squeeze_1caller_threshold})\n"
        code += f"// Squeeze vs Multiple Callers: {squeeze_multi}% (Threshold: {squeeze_multi_threshold})\n"
        code += f"// Squeeze Sizing: {squeeze_sizing}x (Adjusted: {adjusted_squeeze_size}x)\n"
        code += f"// Button Squeeze Adjust: +{btn_squeeze*100}%\n"
        code += f"// Blinds Squeeze Adjust: +{blinds_squeeze*100}%\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"

        # Squeeze Cold Call
        code += "##f$SqueezeColdCall##\n"
        code += "// 1 Raise before Hero first action and 1 or more villains calls. Hero can Squeeze, ColdCall or Fold\n"
        code += f"WHEN f$SqueezeColdCall_Decision = 2 RETURN {adjusted_squeeze_size} * pot FORCE\n" 
        code += "WHEN f$SqueezeColdCall_Decision = 1 RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"

        code += "##f$SqueezeColdCall_Decision##\n"
        code += "// 0 = Fold, 1 = Call, 2 = Squeeze\n"
        code += "// Tighter squeeze range with more players in the pot\n"
        code += f"WHEN CallsSinceLastRaise = 1 AND handrank169 <= {squeeze_1caller_threshold} RETURN 2 FORCE\n"
        code += f"WHEN CallsSinceLastRaise = 1 AND handrank169 <= {round(tight_threshold * 0.7)} RETURN 1 FORCE\n\n"

        code += f"WHEN CallsSinceLastRaise = 2 AND handrank169 <= {squeeze_multi_threshold} RETURN 2 FORCE\n"
        code += f"WHEN CallsSinceLastRaise = 2 AND handrank169 <= {round(tight_threshold * 0.65)} RETURN 1 FORCE\n\n"

        code += f"WHEN CallsSinceLastRaise >= 3 AND handrank169 <= {round(squeeze_multi_threshold * 0.8)} RETURN 2 FORCE\n"
        code += f"WHEN CallsSinceLastRaise >= 3 AND handrank169 <= {round(tight_threshold * 0.6)} RETURN 1 FORCE\n\n"

        code += "// Position-based adjustments\n"
        code += f"WHEN (InButton) AND handrank169 <= {round(squeeze_1caller_threshold * (1 + btn_squeeze))} RETURN 2 FORCE\n"
        code += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(squeeze_1caller_threshold * (1 + blinds_squeeze))} RETURN 2 FORCE\n\n"

        code += "WHEN Others RETURN 0 FORCE\n\n"
        
        # Facing Squeeze
        code += "##f$FacingSqueeze##\n"
        code += "// Hero is the Original Raiser and Facing Squeeze by an opponent. Hero can 4Bet, Call or Fold\n"
        code += "WHEN f$FacingSqueeze_Decision = 2 RETURN RaisePot FORCE\n"
        code += "WHEN f$FacingSqueeze_Decision = 1 RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"

        code += "##f$FacingSqueeze_Decision##\n"
        code += "// 0 = Fold, 1 = Call, 2 = 4-Bet\n"
        code += "// Generally tighter than regular 3-bet defense\n"
        code += f"WHEN handrank169 <= {round(squeeze_threshold * 0.5)} RETURN 2 FORCE\n"
        code += f"WHEN handrank169 <= {round(tight_threshold * 0.55)} RETURN 1 FORCE\n\n"

        code += "// Adjust based on number of callers between raise and squeeze\n"
        code += f"WHEN CallsSinceLastRaise = 1 AND handrank169 <= {round(squeeze_threshold * 0.55)} RETURN 2 FORCE\n"
        code += f"WHEN CallsSinceLastRaise >= 2 AND handrank169 <= {round(squeeze_threshold * 0.45)} RETURN 2 FORCE\n\n"

        code += "WHEN Others RETURN 0 FORCE\n\n"
        
        return code
