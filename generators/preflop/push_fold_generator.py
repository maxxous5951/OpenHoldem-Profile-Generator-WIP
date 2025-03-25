"""
Générateur de stratégies Push/Fold
"""
from generators.preflop.base_generator import BaseProfileGenerator

class PushFoldGenerator(BaseProfileGenerator):
    """
    Classe pour générer les sections de code de Push/Fold
    """
    
    def generate_code(self, settings):
        """
        Génère la section Push/Fold du profil
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code généré pour les stratégies de Push/Fold
        """
        # Extraire le facteur d'agressivité
        aggressive_factor = settings["aggression"] / 50
        
        # Créer les dictionnaires pour les plages de ranges
        push_ranges = self._create_push_ranges_dict(settings, aggressive_factor)
        call_push_ranges = self._create_call_ranges_dict(settings, aggressive_factor)
        
        # Convertir les pourcentages en seuils
        push_thresholds = {}
        call_push_thresholds = {}
        
        for bb_range in push_ranges:
            push_thresholds[bb_range] = {}
            for position in push_ranges[bb_range]:
                push_thresholds[bb_range][position] = self.get_handrank_threshold(push_ranges[bb_range][position])
                
        for bb_range in call_push_ranges:
            call_push_thresholds[bb_range] = {}
            for vs_position in call_push_ranges[bb_range]:
                call_push_thresholds[bb_range][vs_position] = self.get_handrank_threshold(call_push_ranges[bb_range][vs_position])
        
        # Générer le code
        code = "\n//*****************************************************************************\n"
        code += "//\n"
        code += "// PUSH OR FOLD STRATEGY\n"
        code += "//\n"
        code += "// Generated with detailed stack size ranges:\n"
        code += "// - 1BB, 2BB, 3BB, 4BB, 5BB, 6BB, 7BB, 8BB, 9BB, 10BB, 10-15BB, 15-20BB, 20-25BB\n"
        code += "//\n"
        code += "// Aggression Factor applied: " + str(aggressive_factor) + "x\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"
        
        # Function to determine if we're in Push/Fold mode
        code += "##f$InPushFoldMode##\n"
        code += "// Determine if we're in push/fold mode (less than 25 BBs)\n"
        code += "WHEN f$EffectiveStack < 25 AND istournament RETURN true FORCE\n"
        code += "WHEN Others RETURN false FORCE\n\n"
        
        # Main Push/Fold function
        code += "##f$PushFoldPreflop##\n"
        code += "// Main push/fold function based on stack size\n"
        
        # 1BB range
        code += "// 1BB range\n"
        code += "WHEN f$EffectiveStack <= 1 RETURN f$PushFold_1BB FORCE\n\n"
        
        # 2BB range
        code += "// 2BB range\n"
        code += "WHEN f$EffectiveStack > 1 AND f$EffectiveStack <= 2 RETURN f$PushFold_2BB FORCE\n\n"
        
        # 3BB range
        code += "// 3BB range\n"
        code += "WHEN f$EffectiveStack > 2 AND f$EffectiveStack <= 3 RETURN f$PushFold_3BB FORCE\n\n"
        
        # 4BB range
        code += "// 4BB range\n"
        code += "WHEN f$EffectiveStack > 3 AND f$EffectiveStack <= 4 RETURN f$PushFold_4BB FORCE\n\n"
        
        # 5BB range
        code += "// 5BB range\n"
        code += "WHEN f$EffectiveStack > 4 AND f$EffectiveStack <= 5 RETURN f$PushFold_5BB FORCE\n\n"
        
        # 6BB range
        code += "// 6BB range\n"
        code += "WHEN f$EffectiveStack > 5 AND f$EffectiveStack <= 6 RETURN f$PushFold_6BB FORCE\n\n"
        
        # 7BB range
        code += "// 7BB range\n"
        code += "WHEN f$EffectiveStack > 6 AND f$EffectiveStack <= 7 RETURN f$PushFold_7BB FORCE\n\n"
        
        # 8BB range
        code += "// 8BB range\n"
        code += "WHEN f$EffectiveStack > 7 AND f$EffectiveStack <= 8 RETURN f$PushFold_8BB FORCE\n\n"
        
        # 9BB range
        code += "// 9BB range\n"
        code += "WHEN f$EffectiveStack > 8 AND f$EffectiveStack <= 9 RETURN f$PushFold_9BB FORCE\n\n"
        
        # 10BB range
        code += "// 10BB range\n"
        code += "WHEN f$EffectiveStack > 9 AND f$EffectiveStack <= 10 RETURN f$PushFold_10BB FORCE\n\n"
        
        # 10-15BB range
        code += "// 10-15BB range\n"
        code += "WHEN f$EffectiveStack > 10 AND f$EffectiveStack <= 15 RETURN f$PushFold_10_15BB FORCE\n\n"
        
        # 15-20BB range
        code += "// 15-20BB range\n"
        code += "WHEN f$EffectiveStack > 15 AND f$EffectiveStack <= 20 RETURN f$PushFold_15_20BB FORCE\n\n"
        
        # 20-25BB range
        code += "// 20-25BB range\n"
        code += "WHEN f$EffectiveStack > 20 AND f$EffectiveStack <= 25 RETURN f$PushFold_20_25BB FORCE\n\n"
        
        # Default action
        code += "// Default action\n"
        code += "WHEN Others RETURN Fold FORCE\n\n"
        
        # Créer les fonctions individuelles pour chaque taille de stack
        # 1BB range function
        code += self._create_push_fold_function("1", push_thresholds, call_push_thresholds)
        
        # 2BB range function
        code += self._create_push_fold_function("2", push_thresholds, call_push_thresholds)
        
        # 3BB range function
        code += self._create_push_fold_function("3", push_thresholds, call_push_thresholds)
        
        # 4BB range function
        code += self._create_push_fold_function("4", push_thresholds, call_push_thresholds)
        
        # 5BB range function
        code += self._create_push_fold_function("5", push_thresholds, call_push_thresholds)
        
        # 6BB range function
        code += self._create_push_fold_function("6", push_thresholds, call_push_thresholds)
        
        # 7BB range function
        code += self._create_push_fold_function("7", push_thresholds, call_push_thresholds)
        
        # 8BB range function
        code += self._create_push_fold_function("8", push_thresholds, call_push_thresholds)
        
        # 9BB range function
        code += self._create_push_fold_function("9", push_thresholds, call_push_thresholds)
        
        # 10BB range function
        code += self._create_push_fold_function("10", push_thresholds, call_push_thresholds)
        
        # 10-15BB range function
        code += self._create_push_fold_function("10-15", push_thresholds, call_push_thresholds)
        
        # 15-20BB range function
        code += self._create_push_fold_function("15-20", push_thresholds, call_push_thresholds)
        
        # 20-25BB range function
        code += self._create_push_fold_function("20-25", push_thresholds, call_push_thresholds)
        
        return code
    
    def _create_push_ranges_dict(self, settings, aggressive_factor):
        """
        Crée le dictionnaire des ranges Push
        
        Args:
            settings (dict): Paramètres du générateur
            aggressive_factor (float): Facteur d'agressivité
            
        Returns:
            dict: Dictionnaire des ranges Push
        """
        # Format: { BB_range: { position: range_percentage } }
        # Push ranges by stack size (different for each position)
        push_ranges = {
            # 1 BB
            "1": {
                "EP": settings.get("push_1bb_ep", 75),
                "MP": settings.get("push_1bb_mp", 80),
                "CO": settings.get("push_1bb_co", 85),
                "BN": settings.get("push_1bb_btn", 90),
                "SB": settings.get("push_1bb_sb", 92),
                "BB": settings.get("push_1bb_bb", 95)
            },
            # 2 BB
            "2": {
                "EP": settings.get("push_2bb_ep", 60),
                "MP": settings.get("push_2bb_mp", 65),
                "CO": settings.get("push_2bb_co", 70),
                "BN": settings.get("push_2bb_btn", 75),
                "SB": settings.get("push_2bb_sb", 80),
                "BB": settings.get("push_2bb_bb", 85)
            },
            # 3 BB
            "3": {
                "EP": settings.get("push_3bb_ep", 45),
                "MP": settings.get("push_3bb_mp", 50),
                "CO": settings.get("push_3bb_co", 55),
                "BN": settings.get("push_3bb_btn", 60),
                "SB": settings.get("push_3bb_sb", 65),
                "BB": settings.get("push_3bb_bb", 70)
            },
            # 4 BB
            "4": {
                "EP": settings.get("push_4bb_ep", 35),
                "MP": settings.get("push_4bb_mp", 40),
                "CO": settings.get("push_4bb_co", 45),
                "BN": settings.get("push_4bb_btn", 50),
                "SB": settings.get("push_4bb_sb", 55),
                "BB": settings.get("push_4bb_bb", 60)
            },
            # 5 BB
            "5": {
                "EP": settings.get("push_5bb_ep", 28),
                "MP": settings.get("push_5bb_mp", 32),
                "CO": settings.get("push_5bb_co", 36),
                "BN": settings.get("push_5bb_btn", 40),
                "SB": settings.get("push_5bb_sb", 45),
                "BB": settings.get("push_5bb_bb", 50)
            },
            # 6 BB
            "6": {
                "EP": settings.get("push_6bb_ep", 22),
                "MP": settings.get("push_6bb_mp", 26),
                "CO": settings.get("push_6bb_co", 30),
                "BN": settings.get("push_6bb_btn", 35),
                "SB": settings.get("push_6bb_sb", 40),
                "BB": settings.get("push_6bb_bb", 45)
            },
            # 7 BB
            "7": {
                "EP": settings.get("push_7bb_ep", 18),
                "MP": settings.get("push_7bb_mp", 22),
                "CO": settings.get("push_7bb_co", 26),
                "BN": settings.get("push_7bb_btn", 30),
                "SB": settings.get("push_7bb_sb", 35),
                "BB": settings.get("push_7bb_bb", 40)
            },
            # 8 BB
            "8": {
                "EP": settings.get("push_8bb_ep", 15),
                "MP": settings.get("push_8bb_mp", 18),
                "CO": settings.get("push_8bb_co", 22),
                "BN": settings.get("push_8bb_btn", 26),
                "SB": settings.get("push_8bb_sb", 30),
                "BB": settings.get("push_8bb_bb", 35)
            },
            # 9 BB
            "9": {
                "EP": settings.get("push_9bb_ep", 12),
                "MP": settings.get("push_9bb_mp", 15),
                "CO": settings.get("push_9bb_co", 18),
                "BN": settings.get("push_9bb_btn", 22),
                "SB": settings.get("push_9bb_sb", 26),
                "BB": settings.get("push_9bb_bb", 30)
            },
            # 10 BB
            "10": {
                "EP": settings.get("push_10bb_ep", 10),
                "MP": settings.get("push_10bb_mp", 12),
                "CO": settings.get("push_10bb_co", 15),
                "BN": settings.get("push_10bb_btn", 18),
                "SB": settings.get("push_10bb_sb", 22),
                "BB": settings.get("push_10bb_bb", 25)
            },
            # 10-15 BB
            "10-15": {
                "EP": settings.get("push_10_15bb_ep", 8),
                "MP": settings.get("push_10_15bb_mp", 10),
                "CO": settings.get("push_10_15bb_co", 12),
                "BN": settings.get("push_10_15bb_btn", 15),
                "SB": settings.get("push_10_15bb_sb", 18),
                "BB": settings.get("push_10_15bb_bb", 20)
            },
            # 15-20 BB
            "15-20": {
                "EP": settings.get("push_15_20bb_ep", 5),
                "MP": settings.get("push_15_20bb_mp", 8),
                "CO": settings.get("push_15_20bb_co", 10),
                "BN": settings.get("push_15_20bb_btn", 12),
                "SB": settings.get("push_15_20bb_sb", 15),
                "BB": settings.get("push_15_20bb_bb", 18)
            },
            # 20-25 BB
            "20-25": {
                "EP": settings.get("push_20_25bb_ep", 3),
                "MP": settings.get("push_20_25bb_mp", 5),
                "CO": settings.get("push_20_25bb_co", 7),
                "BN": settings.get("push_20_25bb_btn", 10),
                "SB": settings.get("push_20_25bb_sb", 12),
                "BB": settings.get("push_20_25bb_bb", 15)
            }
        }
        
        # Appliquer les ajustements d'agressivité
        for bb_range in push_ranges:
            for position in push_ranges[bb_range]:
                # Ajuster les ranges push en fonction de l'agressivité (plus agressif = plages plus larges)
                push_ranges[bb_range][position] = min(98, round(push_ranges[bb_range][position] * (0.8 + 0.4 * aggressive_factor)))
        
        return push_ranges
    
    def _create_call_ranges_dict(self, settings, aggressive_factor):
        """
        Crée le dictionnaire des ranges d'appel de push
        
        Args:
            settings (dict): Paramètres du générateur
            aggressive_factor (float): Facteur d'agressivité
            
        Returns:
            dict: Dictionnaire des ranges d'appel de push
        """
        # Calling push ranges by stack size (similar structure)
        call_push_ranges = {
            # 1 BB
            "1": {
                "vs_EP": settings.get("call_1bb_vs_ep", 60),
                "vs_MP": settings.get("call_1bb_vs_mp", 65),
                "vs_CO": settings.get("call_1bb_vs_co", 70),
                "vs_BN": settings.get("call_1bb_vs_btn", 75),
                "vs_SB": settings.get("call_1bb_vs_sb", 80)
            },
            # 2 BB
            "2": {
                "vs_EP": settings.get("call_2bb_vs_ep", 50),
                "vs_MP": settings.get("call_2bb_vs_mp", 55),
                "vs_CO": settings.get("call_2bb_vs_co", 60),
                "vs_BN": settings.get("call_2bb_vs_btn", 65),
                "vs_SB": settings.get("call_2bb_vs_sb", 70)
            },
            # 3 BB
            "3": {
                "vs_EP": settings.get("call_3bb_vs_ep", 40),
                "vs_MP": settings.get("call_3bb_vs_mp", 45),
                "vs_CO": settings.get("call_3bb_vs_co", 50),
                "vs_BN": settings.get("call_3bb_vs_btn", 55),
                "vs_SB": settings.get("call_3bb_vs_sb", 60)
            },
            # 4 BB
            "4": {
                "vs_EP": settings.get("call_4bb_vs_ep", 30),
                "vs_MP": settings.get("call_4bb_vs_mp", 35),
                "vs_CO": settings.get("call_4bb_vs_co", 40),
                "vs_BN": settings.get("call_4bb_vs_btn", 45),
                "vs_SB": settings.get("call_4bb_vs_sb", 50)
            },
            # 5 BB
            "5": {
                "vs_EP": settings.get("call_5bb_vs_ep", 25),
                "vs_MP": settings.get("call_5bb_vs_mp", 28),
                "vs_CO": settings.get("call_5bb_vs_co", 32),
                "vs_BN": settings.get("call_5bb_vs_btn", 36),
                "vs_SB": settings.get("call_5bb_vs_sb", 40)
            },
            # 6-10 BB
            "6-10": {
                "vs_EP": settings.get("call_6_10bb_vs_ep", 20),
                "vs_MP": settings.get("call_6_10bb_vs_mp", 22),
                "vs_CO": settings.get("call_6_10bb_vs_co", 25),
                "vs_BN": settings.get("call_6_10bb_vs_btn", 28),
                "vs_SB": settings.get("call_6_10bb_vs_sb", 32)
            },
            # 10-15 BB
            "10-15": {
                "vs_EP": settings.get("call_10_15bb_vs_ep", 15),
                "vs_MP": settings.get("call_10_15bb_vs_mp", 18),
                "vs_CO": settings.get("call_10_15bb_vs_co", 20),
                "vs_BN": settings.get("call_10_15bb_vs_btn", 22),
                "vs_SB": settings.get("call_10_15bb_vs_sb", 25)
            },
            # 15-25 BB
            "15-25": {
                "vs_EP": settings.get("call_15_25bb_vs_ep", 10),
                "vs_MP": settings.get("call_15_25bb_vs_mp", 12),
                "vs_CO": settings.get("call_15_25bb_vs_co", 15),
                "vs_BN": settings.get("call_15_25bb_vs_btn", 18),
                "vs_SB": settings.get("call_15_25bb_vs_sb", 20)
            }
        }
        
        # Appliquer les ajustements d'agressivité
        for bb_range in call_push_ranges:
            for vs_position in call_push_ranges[bb_range]:
                # Ajuster les ranges call en fonction de l'agressivité (plus agressif = plages plus larges)
                call_push_ranges[bb_range][vs_position] = min(95, round(call_push_ranges[bb_range][vs_position] * (0.8 + 0.4 * aggressive_factor)))
        
        return call_push_ranges
    
    def _create_push_fold_function(self, bb_range, push_thresholds, call_push_thresholds):
        """
        Crée une fonction pour une plage spécifique de taille de stack
        
        Args:
            bb_range (str): Plage de taille de stack (ex: "1", "2", "10-15")
            push_thresholds (dict): Seuils de push par position
            call_push_thresholds (dict): Seuils d'appel de push par position
            
        Returns:
            str: Code de la fonction push/fold
        """
        function_name = f"f$PushFold_{bb_range.replace('-', '_')}BB"
        function = f"##" + function_name + "##\n"
        function += f"// Push/Fold strategy for {bb_range}BB stack\n\n"
        
        # Open Push decisions
        function += "// No action before us (first to act)\n"
        
        # Early Position Push Ranges
        function += "// Early Position Push\n"
        function += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 0 AND Calls = 0 AND handrank169 <= {push_thresholds[bb_range]['EP']} RETURN RaiseMax FORCE\n\n"
        
        # Middle Position Push Ranges
        function += "// Middle Position Push\n"
        function += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 0 AND Calls = 0 AND handrank169 <= {push_thresholds[bb_range]['MP']} RETURN RaiseMax FORCE\n\n"
        
        # Late Position Push Ranges
        function += "// CO and Button Push\n"
        function += f"WHEN InCutOff AND BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 0 AND Calls = 0 AND handrank169 <= {push_thresholds[bb_range]['CO']} RETURN RaiseMax FORCE\n"
        function += f"WHEN InButton AND BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 0 AND Calls = 0 AND handrank169 <= {push_thresholds[bb_range]['BN']} RETURN RaiseMax FORCE\n\n"
        
        # Blinds Push Ranges
        function += "// SB Push\n"
        function += f"WHEN InSmallBlind AND BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 0 AND Calls = 0 AND handrank169 <= {push_thresholds[bb_range]['SB']} RETURN RaiseMax FORCE\n\n"
        
        function += "// BB Check or Push over limps\n"
        function += f"WHEN InBigBlind AND BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 0 AND Calls = 0 RETURN Check FORCE\n"
        function += f"WHEN InBigBlind AND BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 0 AND Calls > 0 AND handrank169 <= {push_thresholds[bb_range]['BB']} RETURN RaiseMax FORCE\n\n"
        
        # Push over limpers
        function += "// Push over limpers (from any position)\n"
        function += f"WHEN BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 0 AND Calls > 0 AND handrank169 <= {round(push_thresholds[bb_range]['CO'] * 0.8)} RETURN RaiseMax FORCE\n\n"
        
        # Déterminer quelle plage d'appel utiliser en fonction de la taille du stack
        call_range = bb_range
        if bb_range in ["6", "7", "8", "9", "10"]:
            call_range = "6-10"
        elif bb_range in ["15-20", "20-25"]:
            call_range = "15-25"
            
        # Call all-in from EP
        function += "// Call all-in when EP pushes\n"
        function += f"WHEN BotsActionsOnThisRoundIncludingChecks = 0 AND (RaisesSinceLastPlay = 1) AND (LastRaiserPosition <= 3) AND (AmountToCall >= StackSize * 0.8) AND handrank169 <= {call_push_thresholds[call_range]['vs_EP']} RETURN Call FORCE\n\n"
        
        # Call all-in from MP
        function += "// Call all-in when MP pushes\n"
        function += f"WHEN BotsActionsOnThisRoundIncludingChecks = 0 AND (RaisesSinceLastPlay = 1) AND (LastRaiserPosition > 3 AND LastRaiserPosition <= 6) AND (AmountToCall >= StackSize * 0.8) AND handrank169 <= {call_push_thresholds[call_range]['vs_MP']} RETURN Call FORCE\n\n"
        
        # Call all-in from CO
        function += "// Call all-in when CO pushes\n"
        function += f"WHEN BotsActionsOnThisRoundIncludingChecks = 0 AND (RaisesSinceLastPlay = 1) AND (LastRaiserPosition = nplayersdealt - 2) AND (AmountToCall >= StackSize * 0.8) AND handrank169 <= {call_push_thresholds[call_range]['vs_CO']} RETURN Call FORCE\n\n"
        
        # Call all-in from BN
        function += "// Call all-in when BN pushes\n"
        function += f"WHEN BotsActionsOnThisRoundIncludingChecks = 0 AND (RaisesSinceLastPlay = 1) AND (LastRaiserPosition = nplayersdealt - 1) AND (AmountToCall >= StackSize * 0.8) AND handrank169 <= {call_push_thresholds[call_range]['vs_BN']} RETURN Call FORCE\n\n"
        
        # Call all-in from SB
        function += "// Call all-in when SB pushes\n"
        function += f"WHEN BotsActionsOnThisRoundIncludingChecks = 0 AND (RaisesSinceLastPlay = 1) AND (LastRaiserPosition = nplayersdealt) AND (AmountToCall >= StackSize * 0.8) AND handrank169 <= {call_push_thresholds[call_range]['vs_SB']} RETURN Call FORCE\n\n"
        
        # Face standard raises (not all-in)
        function += "// Face standard raises (push or fold)\n"
        function += f"WHEN BotsActionsOnThisRoundIncludingChecks = 0 AND (RaisesSinceLastPlay = 1) AND (AmountToCall < StackSize * 0.8) AND handrank169 <= {round(call_push_thresholds[call_range]['vs_EP'] * 0.7)} RETURN RaiseMax FORCE\n\n"
        
        # Multiple all-ins
        function += "// Face multiple all-ins\n"
        function += f"WHEN BotsActionsOnThisRoundIncludingChecks = 0 AND Raises >= 2 AND handrank169 <= {round(call_push_thresholds[call_range]['vs_EP'] * 0.4)} RETURN Call FORCE\n\n"
        
        # Default action
        function += "// Default action\n"
        function += "WHEN Others RETURN Fold FORCE\n\n"
        
        return function
