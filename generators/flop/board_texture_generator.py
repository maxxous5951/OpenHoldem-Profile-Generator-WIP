"""
Générateur pour l'analyse de texture du board au flop
"""
from generators.flop.base_generator import BaseFlopGenerator

class BoardTextureGenerator(BaseFlopGenerator):
    """
    Classe pour générer les fonctions d'analyse de texture du board au flop
    """
    
    def generate_code(self, settings):
        """
        Génère les fonctions de texture du board pour le profil flop
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code généré pour l'analyse de texture du board
        """
        code = "// Board texture helper functions\n\n"
        
        # Dry Board Function
        code += "##f$DryBoard##\n"
        code += "// A dry board has few draws and is disconnected\n"
        code += "WHEN FlushPossible RETURN false FORCE\n"
        code += "WHEN StraightPossible RETURN false FORCE\n"
        code += "WHEN nsuitedcommon >= 2 RETURN false FORCE\n"
        code += "WHEN (TopFlopCard - LowestFlopCard) <= 4 AND (TopFlopCard - LowestFlopCard) > 1 RETURN false FORCE\n"
        code += "WHEN PairOnBoard RETURN false FORCE\n"
        code += "WHEN Others RETURN true FORCE\n\n"

        # Wet Board Function
        code += "##f$WetBoard##\n"
        code += "// A wet board has many draws and connected cards\n"
        code += "WHEN FlushPossible OR FlushDrawPossible RETURN true FORCE\n"
        code += "WHEN StraightPossible RETURN true FORCE\n"
        code += "WHEN OpenEndedStraightDrawPossibleOnFlop RETURN true FORCE\n"
        code += "WHEN (TopFlopCard - LowestFlopCard) <= 4 AND (TopFlopCard - LowestFlopCard) > 1 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        return code