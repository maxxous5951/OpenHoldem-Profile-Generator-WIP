"""
Générateur pour l'analyse de texture du board au turn
"""
from generators.turn.base_generator import BaseTurnGenerator

class BoardTextureGenerator(BaseTurnGenerator):
    """
    Classe pour générer les fonctions d'analyse de texture du board au turn
    """
    
    def generate_code(self, settings):
        """
        Génère les fonctions de texture du board pour le profil turn
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code généré pour l'analyse de texture du board
        """
        code = "// Board texture helper functions for turn\n\n"
        
        # Scare Card Function
        code += "##f$ScareCard##\n"
        code += "// Detects scare cards that could make betting more effective\n"
        code += "WHEN (TurnCard >= jack) AND (FlopCardPairedOnTurn OR PairOnTurn) RETURN true FORCE\n"
        code += "WHEN FlushDrawPossible AND NOT FlushPossible RETURN true FORCE\n"
        code += "WHEN f$StraightDrawPossible AND NOT StraightPossible RETURN true FORCE\n"
        code += "WHEN TurnCardIsOvercardToBoard RETURN true FORCE\n"
        code += "WHEN TurnCard <= 9 AND FlopCardPairedOnTurn RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        # Draw Complete Function
        code += "##f$DrawComplete##\n"
        code += "// Detects draw completions on the turn\n"
        code += "WHEN FlushPossible RETURN true FORCE\n"
        code += "WHEN StraightPossible RETURN true FORCE\n"
        code += "WHEN FlopCardPairedOnTurn RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Straight Draw Possible Function
        code += "##f$StraightDrawPossible##\n"
        code += "// Detects if a straight draw is possible\n"
        code += "// For example, having 4 consecutive cards or two groups of 3 cards\n"
        code += "WHEN nstraightfill == 1 RETURN true FORCE\n"
        code += "WHEN HaveStraightDraw RETURN true FORCE\n"
        code += "WHEN HaveOpenEndedStraightDraw RETURN true FORCE\n"
        code += "WHEN HaveInsideStraightDraw RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        return code