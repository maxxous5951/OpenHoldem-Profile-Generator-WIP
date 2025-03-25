"""
Générateur pour les catégories de mains au turn
"""
from generators.turn.base_generator import BaseTurnGenerator

class HandCategoriesGenerator(BaseTurnGenerator):
    """
    Classe pour générer les fonctions de catégorisation des mains au turn
    """
    
    def generate_code(self, settings):
        """
        Génère les fonctions de catégorisation des mains pour le profil turn
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code généré pour la catégorisation des mains
        """
        code = "//*****************************************************************************\n"
        code += "//\n"
        code += "// HAND CATEGORY HELPER FUNCTIONS FOR TURN\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"

        # Value Hands on Turn
        code += "##f$TurnValueHands##\n"
        code += "// Hands worth value betting on the turn\n"
        code += "WHEN HaveStraightFlush RETURN true FORCE\n"
        code += "WHEN HaveQuads RETURN true FORCE\n"
        code += "WHEN HaveFullHouse RETURN true FORCE\n"
        code += "WHEN HaveFlush RETURN true FORCE\n"
        code += "WHEN HaveStraight RETURN true FORCE\n"
        code += "WHEN HaveTrips RETURN true FORCE\n"
        code += "WHEN HaveTwoPair RETURN true FORCE\n"
        code += "WHEN HaveOverPair RETURN true FORCE\n"
        code += "WHEN HaveTopPair AND f$HaveGoodKicker RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        # Strong Hands on Turn
        code += "##f$TurnStrongHands##\n"
        code += "// Very strong hands that should be played aggressively\n"
        code += "WHEN HaveStraightFlush RETURN true FORCE\n"
        code += "WHEN HaveQuads RETURN true FORCE\n"
        code += "WHEN HaveFullHouse RETURN true FORCE\n"
        code += "WHEN HaveFlush RETURN true FORCE\n"
        code += "WHEN HaveStraight RETURN true FORCE\n"
        code += "WHEN HaveSet RETURN true FORCE\n"
        code += "WHEN HaveTwoPair AND HaveTopPair RETURN true FORCE\n"
        code += "WHEN HaveOverPair AND rankhiplayer >= queen RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        # Strong Draws on Turn
        code += "##f$TurnStrongDraws##\n"
        code += "// Strong drawing hands on the turn\n"
        code += "WHEN HaveFlushDraw AND HaveStraightDraw RETURN true FORCE\n"
        code += "WHEN HaveNutFlushDraw RETURN true FORCE\n"
        code += "WHEN HaveNutStraightDraw RETURN true FORCE\n"
        code += "WHEN HaveFlushDraw AND Overcards >= 1 RETURN true FORCE\n"
        code += "WHEN HaveOpenEndedStraightDraw RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        # Semi-Bluff Hands on Turn
        code += "##f$TurnSemiBluffHands##\n"
        code += "// Hands suitable for semi-bluffing on the turn\n"
        code += "WHEN HaveFlushDraw OR HaveOpenEndedStraightDraw RETURN true FORCE\n"
        code += "WHEN Overcards = 2 AND f$WetBoard RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        # Good kicker helper
        code += "##f$HaveGoodKicker##\n"
        code += "// Determines if we have a good kicker with our pair\n"
        code += "WHEN HaveTopPair AND rankhiplayer >= queen RETURN true FORCE\n"
        code += "WHEN HaveTopPair AND rankloplayer >= ten RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        return code