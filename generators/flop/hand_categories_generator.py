"""
Générateur pour les catégories de mains au flop
"""
from generators.flop.base_generator import BaseFlopGenerator

class HandCategoriesGenerator(BaseFlopGenerator):
    """
    Classe pour générer les fonctions de catégorisation des mains au flop
    """
    
    def generate_code(self, settings):
        """
        Génère les fonctions de catégorisation des mains pour le profil flop
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code généré pour la catégorisation des mains
        """
        # Extract relevant settings
        value_aggression = settings.get("value_aggression", 80)
        draw_aggression = settings.get("draw_aggression", 60)
        
        # Calculate thresholds
        value_hands_threshold = self.get_handrank_threshold(value_aggression)
        draw_hands_threshold = self.get_handrank_threshold(draw_aggression)
        
        code = "//*****************************************************************************\n"
        code += "//\n"
        code += "// HAND CATEGORY HELPER FUNCTIONS\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"

        # Value Hands
        code += "##f$FlopValueHands##\n"
        code += "// Hands worth value betting on the flop\n"
        code += "WHEN HaveQuads RETURN true FORCE\n"
        code += "WHEN HaveFullHouse RETURN true FORCE\n"
        code += "WHEN HaveFlush RETURN true FORCE\n"
        code += "WHEN HaveStraight RETURN true FORCE\n"
        code += "WHEN HaveTrips RETURN true FORCE\n"
        code += "WHEN HaveTwoPair RETURN true FORCE\n"
        code += "WHEN HaveOverPair RETURN true FORCE\n"
        code += "WHEN HaveTopPair AND f$HaveGoodKicker RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        # Strong Hands
        code += "##f$FlopStrongHands##\n"
        code += "// Very strong hands that should be played aggressively\n"
        code += "WHEN HaveQuads RETURN true FORCE\n"
        code += "WHEN HaveFullHouse RETURN true FORCE\n"
        code += "WHEN HaveFlush RETURN true FORCE\n"
        code += "WHEN HaveStraight RETURN true FORCE\n"
        code += "WHEN HaveSet RETURN true FORCE\n"
        code += "WHEN HaveTwoPair AND HaveTopPair RETURN true FORCE\n"
        code += "WHEN HaveOverPair AND rankhiplayer >= queen RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        # Draw Hands
        code += "##f$FlopDrawHands##\n"
        code += "// Hands with significant drawing potential\n"
        code += "WHEN HaveFlushDraw RETURN true FORCE\n"
        code += "WHEN HaveStraightDraw RETURN true FORCE\n"
        code += "WHEN HaveOpenEndedStraightDraw RETURN true FORCE\n"
        code += "WHEN HaveInsideStraightDraw AND Overcards >= 1 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        # Strong Draw Hands
        code += "##f$FlopStrongDraws##\n"
        code += "// Strong drawing hands worth semi-bluffing\n"
        code += "WHEN HaveFlushDraw AND Overcards >= 1 RETURN true FORCE\n"
        code += "WHEN HaveOpenEndedStraightDraw AND Overcards >= 1 RETURN true FORCE\n"
        code += "WHEN HaveFlushDraw AND HaveStraightDraw RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        # Good kicker helper
        code += "##f$HaveGoodKicker##\n"
        code += "// Determines if we have a good kicker with our pair\n"
        code += "WHEN HaveTopPair AND rankhiplayer >= queen RETURN true FORCE\n"
        code += "WHEN HaveTopPair AND rankloplayer >= ten RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        return code