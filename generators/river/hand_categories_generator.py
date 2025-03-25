"""
Générateur pour les catégories de mains au river
"""
from generators.river.base_generator import BaseRiverGenerator

class HandCategoriesGenerator(BaseRiverGenerator):
    """
    Classe pour générer les fonctions de catégorisation des mains au river
    """
    
    def generate_code(self, settings):
        """
        Génère les fonctions de catégorisation des mains pour le profil river
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code généré pour la catégorisation des mains
        """
        # Extract relevant settings
        river_value_range = settings.get("river_value_range", 60)
        river_bluff_range = settings.get("river_bluff_range", 15)
        
        code = "//*****************************************************************************\n"
        code += "//\n"
        code += "// HAND CATEGORY HELPER FUNCTIONS FOR RIVER\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"

        # Value Hands on River
        code += "##f$RiverValueHands##\n"
        code += "// Hands worth value betting on the river\n"
        code += "WHEN HaveStraightFlush RETURN true FORCE\n"
        code += "WHEN HaveQuads RETURN true FORCE\n"
        code += "WHEN HaveFullHouse RETURN true FORCE\n"
        code += "WHEN HaveFlush RETURN true FORCE\n"
        code += "WHEN HaveStraight RETURN true FORCE\n"
        code += "WHEN HaveTrips RETURN true FORCE\n"
        code += "WHEN HaveTwoPair AND HaveTopPair RETURN true FORCE\n"
        code += "WHEN HaveOverPair RETURN true FORCE\n"
        code += "WHEN HaveTopPair AND f$HaveGoodKicker RETURN true FORCE\n"
        code += "WHEN HaveSecondTopPair AND f$HaveTopKicker RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        # Strong Hands on River
        code += "##f$RiverStrongHands##\n"
        code += "// Strong hands that can call a river bet\n"
        code += "WHEN HaveStraightFlush RETURN true FORCE\n"
        code += "WHEN HaveQuads RETURN true FORCE\n"
        code += "WHEN HaveFullHouse RETURN true FORCE\n"
        code += "WHEN HaveFlush RETURN true FORCE\n"
        code += "WHEN HaveStraight RETURN true FORCE\n"
        code += "WHEN HaveTrips RETURN true FORCE\n"
        code += "WHEN HaveTwoPair RETURN true FORCE\n"
        code += "WHEN HaveOverPair RETURN true FORCE\n"
        code += "WHEN HaveTopPair AND rankloplayer >= queen RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        # Nut Hands on River
        code += "##f$RiverNutHands##\n"
        code += "// Very strong hands that should be played aggressively\n"
        code += "WHEN HaveStraightFlush RETURN true FORCE\n"
        code += "WHEN HaveQuads RETURN true FORCE\n"
        code += "WHEN HaveFullHouse AND NOT TwoPairOnBoard RETURN true FORCE\n"
        code += "WHEN HaveNutFlush RETURN true FORCE\n"
        code += "WHEN HaveNutStraight RETURN true FORCE\n"
        code += "WHEN HaveSet AND TwoPairOnBoard RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        # Bluff Candidates on River
        code += "##f$RiverBluffCandidates##\n"
        code += "// Hands suitable for bluffing on the river\n"
        code += "// Usually missed draws or blockers to strong hands\n"
        code += "WHEN f$HadFlushDrawOnTurn AND NOT HaveFlush RETURN true FORCE\n"
        code += "WHEN f$HadStraightDrawOnTurn AND NOT HaveStraight RETURN true FORCE\n"
        code += "WHEN TopPairKickerRank >= ace AND FlushPossible RETURN true FORCE\n"
        code += "WHEN Overcards = 2 AND f$DryBoard RETURN true FORCE\n"
        code += "WHEN f$HaveBlockersToNuts RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        # Bluff Raise Hands on River
        code += "##f$RiverBluffRaiseHands##\n"
        code += "// Hands suitable for bluff-raising on the river\n"
        code += "// Usually hands with blockers to nuts\n"
        code += "WHEN f$HaveBlockersToNuts RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        # Good kicker helper
        code += "##f$HaveGoodKicker##\n"
        code += "// Determines if we have a good kicker with our pair\n"
        code += "WHEN HaveTopPair AND rankhiplayer >= queen RETURN true FORCE\n"
        code += "WHEN HaveTopPair AND rankloplayer >= ten RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        return code
