"""
Générateur pour l'analyse de texture du board au river
"""
from generators.river.base_generator import BaseRiverGenerator

class BoardTextureGenerator(BaseRiverGenerator):
    """
    Classe pour générer les fonctions d'analyse de texture du board au river
    """
    
    def generate_code(self, settings):
        """
        Génère les fonctions de texture du board pour le profil river
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code généré pour l'analyse de texture du board
        """
        code = "// Board texture helper functions for river\n\n"
        
        # Détection des boards avec beaucoup de draws
        code += "##f$DrawHeavyBoard##\n"
        code += "// Detects if the board is draw-heavy (many possible draws)\n"
        code += "WHEN FlushPossible RETURN true FORCE\n"
        code += "WHEN StraightPossible RETURN true FORCE\n"
        code += "WHEN f$FourToFlush RETURN true FORCE\n"
        code += "WHEN f$FourToStraight RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"

        # Détection des boards avec paires
        code += "##f$PairedBoard##\n"
        code += "// Detects if the board is paired\n"
        code += "WHEN PairOnBoard RETURN true FORCE\n"
        code += "WHEN TripsOnBoard RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Détection des bloqueurs pour les nuts
        code += "##f$HaveBlockersToNuts##\n"
        code += "// Detects if we have blockers to the nuts\n"
        code += "// For example holding one flush card when flush is possible\n"
        code += "WHEN FlushPossible AND ((FirstHoleCardSuit == DominantSuitCommon AND SecondHoleCardSuit != DominantSuitCommon) OR (FirstHoleCardSuit != DominantSuitCommon AND SecondHoleCardSuit == DominantSuitCommon)) RETURN true FORCE\n"
        code += "WHEN StraightPossible AND ((rankhiplayer == HighCardOfBestPossibleStraight + 1) OR (rankloplayer == HighCardOfBestPossibleStraight + 1)) RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Détection des quatre cartes de même couleur sur le board
        code += "##f$FourToFlush##\n"
        code += "// Detects if there are four cards of the same suit on board\n"
        code += "WHEN nsuitedcommon >= 4 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Détection des quatre cartes consécutives sur le board
        code += "##f$FourToStraight##\n"
        code += "// Detects if there are four consecutive cards on board\n"
        code += "WHEN nstraightcommon >= 4 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Vérification du kicker
        code += "##f$HaveTopKicker##\n"
        code += "// Checks if we have the top kicker possible\n"
        code += "WHEN rankhiplayer >= rankhicommon RETURN true FORCE\n"
        code += "WHEN rankloplayer >= rankhicommon RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Détection des draws au turn
        code += "##f$HadFlushDrawOnTurn##\n"
        code += "// Checks if we had a flush draw on the turn\n"
        code += "WHEN hi_nsuited3 == 4 AND FirstHoleCardSuit == hi_tsuit3 AND SecondHoleCardSuit == hi_tsuit3 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        code += "##f$HadStraightDrawOnTurn##\n"
        code += "// Checks if we had a straight draw on the turn\n"
        code += "WHEN hi_nstraightfill3 == 1 RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        return code
