"""
Générateur de stratégies de 3-bet et 4-bet
"""
from generators.preflop.base_generator import BaseProfileGenerator

class ThreeBetGenerator(BaseProfileGenerator):
    """
    Classe pour générer les sections de code de 3-bet et 4-bet
    """
    
    def generate_code(self, settings):
        """
        Génère la section de 3-bet et 4-bet du profil
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code généré pour les stratégies de 3-bet et 4-bet
        """
        # Extraire les paramètres spécifiques
        call_3bet_range = settings["call_3bet_range"]
        fourbet_vs_3bet_range = settings["fourbet_range"]
        ip_3bet_adjust = settings["ip_3bet_adjust"] / 100.0  # Convert to decimal
        vs_lp_3bet_adjust = settings["vs_lp_3bet_adjust"] / 100.0  # Convert to decimal
        call_4bet_range = settings["call_4bet_range"]
        fivebet_range = settings["fivebet_range"]
        short_stack_4bet = settings["short_stack_4bet"] / 100.0  # Convert to decimal
        threebet_frequency = settings["threebet_frequency"]
        fourbet_frequency = settings["fourbet_frequency"]
        
        # Facteurs d'ajustement basés sur l'agressivité
        aggressive_factor = settings["aggression"] / 50  # 0-2 range where 1 is neutral
        threebet_adjustment = 1 + (aggressive_factor - 1) * 0.5  # 0.75-1.25 range
        fourbet_adjustment = 1 + (aggressive_factor - 1) * 0.6   # 0.7-1.3 range
        
        # Calculer les seuils
        call_3bet_threshold = self.get_handrank_threshold(call_3bet_range)
        fourbet_vs_3bet_threshold = self.get_handrank_threshold(fourbet_vs_3bet_range)
        call_4bet_threshold = self.get_handrank_threshold(call_4bet_range)
        fivebet_threshold = self.get_handrank_threshold(fivebet_range)
        threebet_threshold = self.get_handrank_threshold(threebet_frequency * threebet_adjustment)
        fourbet_threshold = self.get_handrank_threshold(fourbet_frequency * fourbet_adjustment)
        
        # Générer le code
        code = "//*****************************************************************************\n"
        code += "//\n"
        code += "// 3-BET AND 4-BET STRATEGY\n"
        code += "//\n"
        code += f"// 3-Bet Frequency: {threebet_frequency}% (Adjusted: {threebet_frequency * threebet_adjustment:.1f}%)\n"
        code += f"// 4-Bet Frequency: {fourbet_frequency}% (Adjusted: {fourbet_frequency * fourbet_adjustment:.1f}%)\n"
        code += f"// Call 3-Bet Range: {call_3bet_range}% (Threshold: {call_3bet_threshold})\n" 
        code += f"// 4-Bet vs 3-Bet Range: {fourbet_vs_3bet_range}% (Threshold: {fourbet_vs_3bet_threshold})\n"
        code += f"// Call 4-Bet Range: {call_4bet_range}% (Threshold: {call_4bet_threshold})\n"
        code += f"// 5-Bet Range: {fivebet_range}% (Threshold: {fivebet_threshold})\n"
        code += f"// Position Adjustments: In Position +{ip_3bet_adjust*100}%, vs Late Position +{vs_lp_3bet_adjust*100}%\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"

        # Three Bet Cold Call
        code += "##f$ThreeBetColdCall##\n"
        code += "// 1 Raise before Hero first action and No villains call. Hero can 3Bet, ColdCall or Fold\n"
        code += "WHEN f$ThreeBetColdCall_Decision = 2 RETURN RaisePot FORCE\n"
        code += "WHEN f$ThreeBetColdCall_Decision = 1 RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"

        code += "##f$ThreeBetColdCall_Decision##\n"
        code += "// 0 = Fold, 1 = Call, 2 = 3-Bet\n"
        code += "// Early Position 3-bet\n"
        code += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(threebet_threshold * 0.5)} RETURN 2 FORCE\n"
        code += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(call_3bet_threshold * 0.6)} RETURN 1 FORCE\n\n"

        code += "// Middle Position 3-bet\n"
        code += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(threebet_threshold * 0.65)} RETURN 2 FORCE\n"
        code += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(call_3bet_threshold * 0.7)} RETURN 1 FORCE\n\n"

        code += "// Late Position 3-bet\n"
        code += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(threebet_threshold * 0.8)} RETURN 2 FORCE\n"
        code += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(call_3bet_threshold * 0.8)} RETURN 1 FORCE\n\n"

        code += "// Blinds 3-bet\n"
        code += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(threebet_threshold * 0.7)} RETURN 2 FORCE\n"
        code += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(call_3bet_threshold * 0.75)} RETURN 1 FORCE\n\n"

        code += "// Against specific positions - 3-bet looser against late position raises\n"
        code += f"WHEN (DealPositionLastRaiser >= nplayersdealt - 2) AND handrank169 <= {round(threebet_threshold * (1 + vs_lp_3bet_adjust))} RETURN 2 FORCE\n"
        code += f"WHEN (DealPositionLastRaiser >= nplayersdealt - 2) AND handrank169 <= {round(call_3bet_threshold * (1 + vs_lp_3bet_adjust))} RETURN 1 FORCE\n\n"

        code += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing 3Bet Before First Action
        code += "##f$Facing3BetBeforeFirstAction##\n"
        code += "// 3bet or squeeze before Hero first action. Hero can 4Bet, ColdCall or Fold\n"
        code += "WHEN f$Facing3BetBeforeFirstAction_Decision = 2 RETURN RaisePot FORCE\n"
        code += "WHEN f$Facing3BetBeforeFirstAction_Decision = 1 RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"

        code += "##f$Facing3BetBeforeFirstAction_Decision##\n"
        code += "// 0 = Fold, 1 = Call, 2 = 4-Bet\n"
        code += "// Very tight 4-betting range from early position\n"
        code += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.4)} RETURN 2 FORCE\n"
        code += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(call_3bet_threshold * 0.5)} RETURN 1 FORCE\n\n"

        code += "// Middle position\n"
        code += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.5)} RETURN 2 FORCE\n"
        code += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(call_3bet_threshold * 0.55)} RETURN 1 FORCE\n\n"

        code += "// Late position\n"
        code += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.6)} RETURN 2 FORCE\n"
        code += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(call_3bet_threshold * 0.6)} RETURN 1 FORCE\n\n"

        code += "// Blinds\n"
        code += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.55)} RETURN 2 FORCE\n"
        code += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(call_3bet_threshold * 0.55)} RETURN 1 FORCE\n\n"

        code += "// Stack depth considerations\n"
        code += f"WHEN StackSize < 50 AND handrank169 <= {round(fourbet_vs_3bet_threshold * (1 + short_stack_4bet))} RETURN 2 FORCE\n"

        code += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing 4Bet Before First Action
        code += "##f$Facing4BetBeforeFirstAction##\n"
        code += "// 4bet before Hero first action. Hero can 5Bet, ColdCall or Fold\n"
        code += "WHEN f$Facing4BetBeforeFirstAction_Decision = 2 RETURN RaiseMax FORCE\n"
        code += "WHEN f$Facing4BetBeforeFirstAction_Decision = 1 RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"

        code += "##f$Facing4BetBeforeFirstAction_Decision##\n"
        code += "// 0 = Fold, 1 = Call, 2 = 5-Bet (All-In)\n"
        code += f"WHEN handrank169 <= {fivebet_threshold} RETURN 2 FORCE\n"
        code += f"WHEN handrank169 <= {call_4bet_threshold} RETURN 1 FORCE\n"
        code += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing 5Bet Before First Action
        code += "##f$Facing5BetBeforeFirstAction##\n"
        code += "// 5bet before Hero first action. Hero can Push, ColdCall or Fold\n"
        code += f"WHEN handrank169 <= {round(fivebet_threshold * 0.8)} RETURN RaiseMax FORCE\n"
        code += f"WHEN handrank169 <= {round(call_4bet_threshold * 0.8)} RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"

        # Facing 3Bet
        code += "##f$Facing3Bet##\n"
        code += "// Hero is the Original Raiser and Facing 3Bet. Hero can 4Bet, Call or Fold\n"
        code += "WHEN f$Facing3Bet_Decision = 2 RETURN RaisePot FORCE\n"
        code += "WHEN f$Facing3Bet_Decision = 1 RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"

        code += "##f$Facing3Bet_Decision##\n"
        code += "// 0 = Fold, 1 = Call, 2 = 4-Bet\n"
        code += "// Adjust based on position\n"
        code += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.45)} RETURN 2 FORCE\n"
        code += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(call_3bet_threshold * 0.55)} RETURN 1 FORCE\n\n"

        code += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.55)} RETURN 2 FORCE\n"
        code += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(call_3bet_threshold * 0.6)} RETURN 1 FORCE\n\n"

        code += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.65)} RETURN 2 FORCE\n"
        code += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(call_3bet_threshold * 0.7)} RETURN 1 FORCE\n\n"

        code += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.6)} RETURN 2 FORCE\n"
        code += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(call_3bet_threshold * 0.65)} RETURN 1 FORCE\n\n"

        code += "// Position adjustment - more aggressive in position\n"
        code += f"WHEN f$InPosition AND handrank169 <= {round(fourbet_vs_3bet_threshold * (1 + ip_3bet_adjust))} RETURN 2 FORCE\n"
        code += f"WHEN f$InPosition AND handrank169 <= {round(call_3bet_threshold * (1 + ip_3bet_adjust))} RETURN 1 FORCE\n\n"

        code += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing 4Bet
        code += "##f$Facing4Bet##\n"
        code += "// Hero 3bet and facing 4bet. Hero can 5bet, Call or Fold\n"
        code += "WHEN f$Facing4Bet_Decision = 2 RETURN RaiseMax FORCE\n"
        code += "WHEN f$Facing4Bet_Decision = 1 RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"

        code += "##f$Facing4Bet_Decision##\n"
        code += "// 0 = Fold, 1 = Call, 2 = 5-Bet (All-In)\n"
        code += f"WHEN handrank169 <= {fivebet_threshold} RETURN 2 FORCE\n"
        code += f"WHEN handrank169 <= {call_4bet_threshold} RETURN 1 FORCE\n"
        code += "// Stack depth considerations\n"
        code += f"WHEN StackSize < 50 AND handrank169 <= {round(fivebet_threshold * (1 + short_stack_4bet))} RETURN 2 FORCE\n\n"

        code += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing 5Bet
        code += "##f$Facing5Bet##\n"
        code += "// Hero 4bet and facing 5bet. Hero can Push, Call or Fold\n"
        code += f"WHEN handrank169 <= {round(fivebet_threshold * 0.8)} RETURN RaiseMax FORCE\n"
        code += f"WHEN handrank169 <= {round(call_4bet_threshold * 0.6)} RETURN Call FORCE\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"

        # In Position helper function
        code += "##f$InPosition##\n"
        code += "// Helper function to determine if we're in position vs the 3bettor\n"
        code += "WHEN LastAggressorActsAfterUs RETURN false FORCE\n"
        code += "WHEN Others RETURN true FORCE\n\n"
        
        return code
