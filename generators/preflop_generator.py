class PreflopProfileGenerator:
    def __init__(self):
        pass
        
    def get_handrank_threshold(self, percentage):
        """Convert a percentage into a handrank threshold value"""
        # HandRank goes from 1 to 169, where 1 is the best hand (AA)
        # Convert percentage to a hand rank value
        # 0% = only AA (rank 1)
        # 100% = all hands (rank 169)
        return round(1 + (percentage / 100) * 168)
        
    def calculate_raise_size(self, base_size, num_limpers=0, aggressive_factor=1.0):
        """Calculate raise size based on base size, number of limpers and aggression"""
        # Add 1BB for each limper
        size = float(base_size)
        if num_limpers > 0:
            size += num_limpers
        
        # Adjust size based on aggression
        # More aggressive = larger sizing (±20%)
        size *= (0.8 + (aggressive_factor * 0.4))
        
        return round(size, 1)
        
    def get_position_map(self, num_players):
        """Returns a map of which positions exist based on number of players"""
        positions = {
            "EP1": False,
            "EP2": False,
            "EP3": False,
            "MP1": False,
            "MP2": False,
            "MP3": False,
            "CO": False,
            "BTN": False,
            "SB": True,   # Always exists
            "BB": True    # Always exists
        }
        
        # Activate positions based on number of players
        if num_players >= 3:
            positions["BTN"] = True
        
        if num_players >= 4:
            positions["CO"] = True
            
        if num_players >= 5:
            positions["MP3"] = True
            
        if num_players >= 6:
            positions["MP2"] = True
            
        if num_players >= 7:
            positions["MP1"] = True
            
        if num_players >= 8:
            positions["EP3"] = True
            
        if num_players >= 9:
            positions["EP2"] = True
            positions["EP1"] = True
            
        return positions
    
    def generate_preflop_profile(self, settings):
        """Generate the preflop part of the OpenHoldem profile"""
        # Extract basic settings
        num_players = settings["num_players"]
        game_type = settings["game_type"]
        aggression = settings["aggression"]
        tightness = settings["tightness"]
        limp_frequency = settings["limp_frequency"]
        threebet_frequency = settings["threebet_frequency"]
        fourbet_frequency = settings["fourbet_frequency"]
        squeeze_frequency = settings["squeeze_frequency"]
        open_raise_size = settings["open_raise_size"]
        
        # Extract specific settings from tabs
        # Open Raise tab
        ep_range = settings["ep_range"]
        mp_range = settings["mp_range"]
        lp_range = settings["lp_range"] 
        ep_sizing = settings["ep_sizing"]
        mp_sizing = settings["mp_sizing"]
        lp_sizing = settings["lp_sizing"]
        
        # Facing 3-Bet tab
        call_3bet_range = settings["call_3bet_range"]
        fourbet_vs_3bet_range = settings["fourbet_range"]
        ip_3bet_adjust = settings["ip_3bet_adjust"] / 100.0  # Convert to decimal
        vs_lp_3bet_adjust = settings["vs_lp_3bet_adjust"] / 100.0  # Convert to decimal
        
        # Facing 4-Bet tab
        call_4bet_range = settings["call_4bet_range"]
        fivebet_range = settings["fivebet_range"]
        short_stack_4bet = settings["short_stack_4bet"] / 100.0  # Convert to decimal
        
        # Squeeze tab
        squeeze_1caller = settings["squeeze_1caller"]
        squeeze_multi = settings["squeeze_multi"]
        squeeze_sizing = settings["squeeze_sizing"]
        blinds_squeeze = settings["blinds_squeeze"] / 100.0  # Convert to decimal
        btn_squeeze = settings["btn_squeeze"] / 100.0  # Convert to decimal
        
        # Convert slider values to thresholds
        tight_threshold = self.get_handrank_threshold(tightness)
        aggressive_factor = aggression / 50  # 0-2 range where 1 is neutral
        limp_factor = limp_frequency / 50  # 0-2 range where 1 is default frequency
        
        # Specific thresholds for position-based ranges
        ep_raise_threshold = self.get_handrank_threshold(ep_range)
        mp_raise_threshold = self.get_handrank_threshold(mp_range)
        lp_raise_threshold = self.get_handrank_threshold(lp_range)
        
        # Specific thresholds for 3-bet/4-bet/squeeze reactions
        call_3bet_threshold = self.get_handrank_threshold(call_3bet_range)
        fourbet_vs_3bet_threshold = self.get_handrank_threshold(fourbet_vs_3bet_range)
        call_4bet_threshold = self.get_handrank_threshold(call_4bet_range)
        fivebet_threshold = self.get_handrank_threshold(fivebet_range)
        squeeze_1caller_threshold = self.get_handrank_threshold(squeeze_1caller)
        squeeze_multi_threshold = self.get_handrank_threshold(squeeze_multi)
        
        # Adjust 3bet/4bet/squeeze frequencies based on aggression
        # Higher aggression = higher 3bet/4bet frequencies
        threebet_adjustment = 1 + (aggressive_factor - 1) * 0.5  # 0.75-1.25 range
        fourbet_adjustment = 1 + (aggressive_factor - 1) * 0.6   # 0.7-1.3 range
        squeeze_adjustment = 1 + (aggressive_factor - 1) * 0.7   # 0.65-1.35 range
        
        # Apply aggression adjustments
        threebet_threshold = self.get_handrank_threshold(threebet_frequency * threebet_adjustment)
        fourbet_threshold = self.get_handrank_threshold(fourbet_frequency * fourbet_adjustment)
        squeeze_threshold = self.get_handrank_threshold(squeeze_frequency * squeeze_adjustment)
        
        # Determine which positions exist based on number of players
        position_map = self.get_position_map(num_players)
        
        # Adjust raise sizes based on aggression and position
        adjusted_open_raise = self.calculate_raise_size(open_raise_size, 0, aggressive_factor)
        ep_open_raise = self.calculate_raise_size(ep_sizing, 0, aggressive_factor)
        mp_open_raise = self.calculate_raise_size(mp_sizing, 0, aggressive_factor)
        lp_open_raise = self.calculate_raise_size(lp_sizing, 0, aggressive_factor)
        
        # Calculate squeeze size
        squeeze_bet_size = float(squeeze_sizing)
        adjusted_squeeze_size = self.calculate_raise_size(squeeze_sizing, 0, aggressive_factor * 1.2)  # More aggressive for squeezes
        
        # Generate the profile text using string concatenation instead of a single f-string
        # to avoid issues with very long strings
        profile = "//*****************************************************************************\n"
        profile += "//\n"
        profile += f"// OpenHoldem Profile Generator - Preflop Profile\n"
        profile += f"// Generated for {num_players}-player {game_type}\n"
        profile += "// \n"
        profile += f"// Strategy Settings:\n"
        profile += f"// - Aggression: {aggression}% (Factor: {aggressive_factor:.2f}x)\n"
        profile += f"// - Tightness: {tightness}%\n"
        profile += f"// - Limp Frequency: {limp_frequency}%\n"
        profile += f"// - 3-Bet Frequency: {threebet_frequency}% (Adjusted: {threebet_frequency * threebet_adjustment:.1f}%)\n"
        profile += f"// - 4-Bet Frequency: {fourbet_frequency}% (Adjusted: {fourbet_frequency * fourbet_adjustment:.1f}%)\n"
        profile += f"// - Squeeze Frequency: {squeeze_frequency}% (Adjusted: {squeeze_frequency * squeeze_adjustment:.1f}%)\n"
        profile += f"// - Open Raise Size: {open_raise_size}x (Adjusted: {adjusted_open_raise}x)\n"
        profile += "//\n"
        profile += "// Position-Based Settings:\n"
        profile += f"// - Early Position Range: {ep_range}% (Threshold: {ep_raise_threshold})\n"
        profile += f"// - Middle Position Range: {mp_range}% (Threshold: {mp_raise_threshold})\n"
        profile += f"// - Late Position Range: {lp_range}% (Threshold: {lp_raise_threshold})\n"
        profile += f"// - Squeeze vs 1 Caller: {squeeze_1caller}% (Threshold: {squeeze_1caller_threshold})\n"
        profile += f"// - Squeeze vs 2+ Callers: {squeeze_multi}% (Threshold: {squeeze_multi_threshold})\n"
        profile += "//\n"
        profile += "// Position Map for Table Size:\n"
        
        # Add position information
        for pos, exists in position_map.items():
            profile += f"// - {pos}: {'Active' if exists else 'Inactive'}\n"
            
        profile += "//\n"
        profile += "//*****************************************************************************\n\n"

        profile += "//*****************************************************************************\n"
        profile += "//\n"
        profile += "// PREFLOP SCENARIOS\n"
        profile += "//\n"
        profile += "//*****************************************************************************\n\n"

        # Open Raise or Open Limp
        profile += "##f$OpenRaiseOrOpenLimp##\n"
        profile += "// No action (limp or raise) before us. Hero can Open the game by Raising or Limping\n"
        profile += "WHEN InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3 RETURN f$OpenRaise_EarlyPosition FORCE\n"
        profile += "WHEN InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3 RETURN f$OpenRaise_MiddlePosition FORCE\n"
        profile += "WHEN InCutOff OR InButton RETURN f$OpenRaise_LatePosition FORCE\n"
        profile += "WHEN InSmallBlind RETURN f$OpenRaise_SB FORCE\n"
        profile += "WHEN InBigBlind RETURN Check FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        # Early Position Open Raising
        profile += "##f$OpenRaise_EarlyPosition##\n"
        profile += f"WHEN handrank169 <= {ep_raise_threshold} RETURN {ep_open_raise} FORCE\n"
        profile += f"WHEN handrank169 <= {round(tight_threshold * 0.7 * limp_factor)} RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"
        
        # Middle Position Open Raising
        profile += "##f$OpenRaise_MiddlePosition##\n"
        profile += f"WHEN handrank169 <= {mp_raise_threshold} RETURN {mp_open_raise} FORCE\n"
        profile += f"WHEN handrank169 <= {round(tight_threshold * 0.85 * limp_factor)} RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"
        
        # Late Position Open Raising
        profile += "##f$OpenRaise_LatePosition##\n"
        profile += f"WHEN handrank169 <= {lp_raise_threshold} RETURN {lp_open_raise} FORCE\n"
        profile += f"WHEN handrank169 <= {round(tight_threshold * limp_factor)} RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"
        
        # Small Blind Open Raising
        profile += "##f$OpenRaise_SB##\n"
        profile += f"WHEN handrank169 <= {round(lp_raise_threshold * 0.9)} RETURN {lp_open_raise} FORCE\n"
        profile += f"WHEN handrank169 <= {round(tight_threshold * 0.9 * limp_factor)} RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        # Limp Or Isolate Limpers
        profile += "##f$LimpOrIsolateLimpers##\n"
        profile += "// 1 or more limps before us. Hero can Limp too or Raise to isolate the limpers\n"
        profile += "WHEN f$LimpOrIsolateLimpers_Decision = 2 RETURN f$IsolateSize FORCE\n"
        profile += "WHEN f$LimpOrIsolateLimpers_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        # Isolate sizing calculation based on number of limpers
        profile += "##f$IsolateSize##\n"
        profile += f"// Base open size: {open_raise_size}BB plus 1BB per limper\n"
        profile += f"Calls * 1 + {adjusted_open_raise}\n\n"

        profile += "##f$LimpOrIsolateLimpers_Decision##\n"
        profile += "// 0 = Fold, 1 = Limp, 2 = Raise\n"
        profile += "// More aggressive with fewer limpers, tighter with more\n"
        profile += f"WHEN Calls = 1 AND handrank169 <= {round(tight_threshold * 0.7)} RETURN 2 FORCE\n"
        profile += f"WHEN Calls = 1 AND handrank169 <= {round(tight_threshold * 0.9 * limp_factor)} RETURN 1 FORCE\n\n"

        profile += f"WHEN Calls = 2 AND handrank169 <= {round(tight_threshold * 0.6)} RETURN 2 FORCE\n"
        profile += f"WHEN Calls = 2 AND handrank169 <= {round(tight_threshold * 0.85 * limp_factor)} RETURN 1 FORCE\n\n"

        profile += f"WHEN Calls >= 3 AND handrank169 <= {round(tight_threshold * 0.5)} RETURN 2 FORCE\n"
        profile += f"WHEN Calls >= 3 AND handrank169 <= {round(tight_threshold * 0.8 * limp_factor)} RETURN 1 FORCE\n\n"

        profile += "// Position based adjustments - more aggressive in position\n"
        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(tight_threshold * 0.75)} RETURN 2 FORCE\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(tight_threshold * 0.65)} RETURN 2 FORCE\n\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Three Bet Cold Call
        profile += "##f$ThreeBetColdCall##\n"
        profile += "// 1 Raise before Hero first action and No villains call. Hero can 3Bet, ColdCall or Fold\n"
        profile += "WHEN f$ThreeBetColdCall_Decision = 2 RETURN RaisePot FORCE\n"
        profile += "WHEN f$ThreeBetColdCall_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        profile += "##f$ThreeBetColdCall_Decision##\n"
        profile += "// 0 = Fold, 1 = Call, 2 = 3-Bet\n"
        profile += "// Early Position 3-bet\n"
        profile += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(threebet_threshold * 0.5)} RETURN 2 FORCE\n"
        profile += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(call_3bet_threshold * 0.6)} RETURN 1 FORCE\n\n"

        profile += "// Middle Position 3-bet\n"
        profile += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(threebet_threshold * 0.65)} RETURN 2 FORCE\n"
        profile += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(call_3bet_threshold * 0.7)} RETURN 1 FORCE\n\n"

        profile += "// Late Position 3-bet\n"
        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(threebet_threshold * 0.8)} RETURN 2 FORCE\n"
        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(call_3bet_threshold * 0.8)} RETURN 1 FORCE\n\n"

        profile += "// Blinds 3-bet\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(threebet_threshold * 0.7)} RETURN 2 FORCE\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(call_3bet_threshold * 0.75)} RETURN 1 FORCE\n\n"

        profile += "// Against specific positions - 3-bet looser against late position raises\n"
        profile += f"WHEN (DealPositionLastRaiser >= nplayersdealt - 2) AND handrank169 <= {round(threebet_threshold * (1 + vs_lp_3bet_adjust))} RETURN 2 FORCE\n"
        profile += f"WHEN (DealPositionLastRaiser >= nplayersdealt - 2) AND handrank169 <= {round(call_3bet_threshold * (1 + vs_lp_3bet_adjust))} RETURN 1 FORCE\n\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Squeeze Cold Call
        profile += "##f$SqueezeColdCall##\n"
        profile += "// 1 Raise before Hero first action and 1 or more villains calls. Hero can Squeeze, ColdCall or Fold\n"
        profile += f"WHEN f$SqueezeColdCall_Decision = 2 RETURN {adjusted_squeeze_size} * pot FORCE\n" 
        profile += "WHEN f$SqueezeColdCall_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        profile += "##f$SqueezeColdCall_Decision##\n"
        profile += "// 0 = Fold, 1 = Call, 2 = Squeeze\n"
        profile += "// Tighter squeeze range with more players in the pot\n"
        profile += f"WHEN CallsSinceLastRaise = 1 AND handrank169 <= {squeeze_1caller_threshold} RETURN 2 FORCE\n"
        profile += f"WHEN CallsSinceLastRaise = 1 AND handrank169 <= {round(tight_threshold * 0.7)} RETURN 1 FORCE\n\n"

        profile += f"WHEN CallsSinceLastRaise = 2 AND handrank169 <= {squeeze_multi_threshold} RETURN 2 FORCE\n"
        profile += f"WHEN CallsSinceLastRaise = 2 AND handrank169 <= {round(tight_threshold * 0.65)} RETURN 1 FORCE\n\n"

        profile += f"WHEN CallsSinceLastRaise >= 3 AND handrank169 <= {round(squeeze_multi_threshold * 0.8)} RETURN 2 FORCE\n"
        profile += f"WHEN CallsSinceLastRaise >= 3 AND handrank169 <= {round(tight_threshold * 0.6)} RETURN 1 FORCE\n\n"

        profile += "// Position-based adjustments\n"
        profile += f"WHEN (InButton) AND handrank169 <= {round(squeeze_1caller_threshold * (1 + btn_squeeze))} RETURN 2 FORCE\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(squeeze_1caller_threshold * (1 + blinds_squeeze))} RETURN 2 FORCE\n\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing 3Bet Before First Action
        profile += "##f$Facing3BetBeforeFirstAction##\n"
        profile += "// 3bet or squeeze before Hero first action. Hero can 4Bet, ColdCall or Fold\n"
        profile += "WHEN f$Facing3BetBeforeFirstAction_Decision = 2 RETURN RaisePot FORCE\n"
        profile += "WHEN f$Facing3BetBeforeFirstAction_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        profile += "##f$Facing3BetBeforeFirstAction_Decision##\n"
        profile += "// 0 = Fold, 1 = Call, 2 = 4-Bet\n"
        profile += "// Very tight 4-betting range from early position\n"
        profile += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.4)} RETURN 2 FORCE\n"
        profile += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(call_3bet_threshold * 0.5)} RETURN 1 FORCE\n\n"

        profile += "// Middle position\n"
        profile += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.5)} RETURN 2 FORCE\n"
        profile += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(call_3bet_threshold * 0.55)} RETURN 1 FORCE\n\n"

        profile += "// Late position\n"
        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.6)} RETURN 2 FORCE\n"
        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(call_3bet_threshold * 0.6)} RETURN 1 FORCE\n\n"

        profile += "// Blinds\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.55)} RETURN 2 FORCE\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(call_3bet_threshold * 0.55)} RETURN 1 FORCE\n\n"

        profile += "// Stack depth considerations\n"
        profile += f"WHEN StackSize < 50 AND handrank169 <= {round(fourbet_vs_3bet_threshold * (1 + short_stack_4bet))} RETURN 2 FORCE\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing 4Bet Before First Action
        profile += "##f$Facing4BetBeforeFirstAction##\n"
        profile += "// 4bet before Hero first action. Hero can 5Bet, ColdCall or Fold\n"
        profile += "WHEN f$Facing4BetBeforeFirstAction_Decision = 2 RETURN RaiseMax FORCE\n"
        profile += "WHEN f$Facing4BetBeforeFirstAction_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        profile += "##f$Facing4BetBeforeFirstAction_Decision##\n"
        profile += "// 0 = Fold, 1 = Call, 2 = 5-Bet (All-In)\n"
        profile += f"WHEN handrank169 <= {fivebet_threshold} RETURN 2 FORCE\n"
        profile += f"WHEN handrank169 <= {call_4bet_threshold} RETURN 1 FORCE\n"
        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing 5Bet Before First Action
        profile += "##f$Facing5BetBeforeFirstAction##\n"
        profile += "// 5bet before Hero first action. Hero can Push, ColdCall or Fold\n"
        profile += f"WHEN handrank169 <= {round(fivebet_threshold * 0.8)} RETURN RaiseMax FORCE\n"
        profile += f"WHEN handrank169 <= {round(call_4bet_threshold * 0.8)} RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        # Facing 3Bet
        profile += "##f$Facing3Bet##\n"
        profile += "// Hero is the Original Raiser and Facing 3Bet. Hero can 4Bet, Call or Fold\n"
        profile += "WHEN f$Facing3Bet_Decision = 2 RETURN RaisePot FORCE\n"
        profile += "WHEN f$Facing3Bet_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        profile += "##f$Facing3Bet_Decision##\n"
        profile += "// 0 = Fold, 1 = Call, 2 = 4-Bet\n"
        profile += "// Adjust based on position\n"
        profile += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.45)} RETURN 2 FORCE\n"
        profile += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(call_3bet_threshold * 0.55)} RETURN 1 FORCE\n\n"

        profile += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.55)} RETURN 2 FORCE\n"
        profile += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(call_3bet_threshold * 0.6)} RETURN 1 FORCE\n\n"

        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.65)} RETURN 2 FORCE\n"
        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(call_3bet_threshold * 0.7)} RETURN 1 FORCE\n\n"

        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.6)} RETURN 2 FORCE\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(call_3bet_threshold * 0.65)} RETURN 1 FORCE\n\n"

        profile += "// Position adjustment - more aggressive in position\n"
        profile += f"WHEN f$InPosition AND handrank169 <= {round(fourbet_vs_3bet_threshold * (1 + ip_3bet_adjust))} RETURN 2 FORCE\n"
        profile += f"WHEN f$InPosition AND handrank169 <= {round(call_3bet_threshold * (1 + ip_3bet_adjust))} RETURN 1 FORCE\n\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # In Position helper function
        profile += "##f$InPosition##\n"
        profile += "// Helper function to determine if we're in position vs the 3bettor\n"
        profile += "WHEN LastAggressorActsAfterUs RETURN false FORCE\n"
        profile += "WHEN Others RETURN true FORCE\n\n"

        # Facing Squeeze
        profile += "##f$FacingSqueeze##\n"
        profile += "// Hero is the Original Raiser and Facing Squeeze by an opponent. Hero can 4Bet, Call or Fold\n"
        profile += "WHEN f$FacingSqueeze_Decision = 2 RETURN RaisePot FORCE\n"
        profile += "WHEN f$FacingSqueeze_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        profile += "##f$FacingSqueeze_Decision##\n"
        profile += "// 0 = Fold, 1 = Call, 2 = 4-Bet\n"
        profile += "// Generally tighter than regular 3-bet defense\n"
        profile += f"WHEN handrank169 <= {round(fourbet_vs_3bet_threshold * 0.5)} RETURN 2 FORCE\n"
        profile += f"WHEN handrank169 <= {round(call_3bet_threshold * 0.55)} RETURN 1 FORCE\n\n"

        profile += "// Adjust based on number of callers between raise and squeeze\n"
        profile += f"WHEN CallsSinceLastRaise = 1 AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.55)} RETURN 2 FORCE\n"
        profile += f"WHEN CallsSinceLastRaise >= 2 AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.45)} RETURN 2 FORCE\n\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing 4Bet
        profile += "##f$Facing4Bet##\n"
        profile += "// Hero 3bet and facing 4bet. Hero can 5bet, Call or Fold\n"
        profile += "WHEN f$Facing4Bet_Decision = 2 RETURN RaiseMax FORCE\n"
        profile += "WHEN f$Facing4Bet_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        profile += "##f$Facing4Bet_Decision##\n"
        profile += "// 0 = Fold, 1 = Call, 2 = 5-Bet (All-In)\n"
        profile += f"WHEN handrank169 <= {fivebet_threshold} RETURN 2 FORCE\n"
        profile += f"WHEN handrank169 <= {call_4bet_threshold} RETURN 1 FORCE\n"
        profile += "// Stack depth considerations\n"
        profile += f"WHEN StackSize < 50 AND handrank169 <= {round(fivebet_threshold * (1 + short_stack_4bet))} RETURN 2 FORCE\n\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing 5Bet
        profile += "##f$Facing5Bet##\n"
        profile += "// Hero 4bet and facing 5bet. Hero can Push, Call or Fold\n"
        profile += f"WHEN handrank169 <= {round(fivebet_threshold * 0.8)} RETURN RaiseMax FORCE\n"
        profile += f"WHEN handrank169 <= {round(call_4bet_threshold * 0.6)} RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        # Additional functions
        profile += "//*****************************************************************************\n"
        profile += "//\n"
        profile += "// ADDITIONAL FUNCTIONS\n"
        profile += "//\n"
        profile += "//*****************************************************************************\n\n"

        # Main preflop function
        profile += "##f$preflop##\n"
        profile += "// Main preflop decision function that uses OpenPPL library functions\n"
        profile += "// to detect scenarios and then calls our decision functions\n\n"

        profile += "// Check for Push/Fold mode first\n"
        profile += "WHEN f$InPushFoldMode RETURN f$PushFoldPreflop FORCE\n\n"

        profile += "// Open Raise or Open Limp\n"
        profile += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 0 AND Calls = 0) RETURN f$OpenRaiseOrOpenLimp FORCE\n\n"

        profile += "// Limp or Isolate Limpers\n"
        profile += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 0 AND Calls >= 1) RETURN f$LimpOrIsolateLimpers FORCE\n\n"

        profile += "// Three Bet or Cold Call\n"
        profile += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 1 AND CallsSinceLastRaise = 0) RETURN f$ThreeBetColdCall FORCE\n\n"

        profile += "// Squeeze or Cold Call\n"
        profile += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 1 AND CallsSinceLastRaise >= 1) RETURN f$SqueezeColdCall FORCE\n\n"

        profile += "// Facing 3-Bet Before First Action\n"
        profile += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 2) RETURN f$Facing3BetBeforeFirstAction FORCE\n\n"

        profile += "// Facing 4-Bet Before First Action\n"
        profile += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 3) RETURN f$Facing4BetBeforeFirstAction FORCE\n\n"

        profile += "// Facing 5-Bet Before First Action\n"
        profile += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 4) RETURN f$Facing5BetBeforeFirstAction FORCE\n\n"

        profile += "// Facing 3-Bet\n"
        profile += "WHEN (BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 1 AND NumberOfRaisesBeforeFlop = 1 AND Calls = 0 AND RaisesSinceLastPlay = 1) RETURN f$Facing3Bet FORCE\n\n"

        profile += "// Facing Squeeze\n"
        profile += "WHEN (BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 1 AND NumberOfRaisesBeforeFlop = 1 AND Calls >= 1 AND RaisesSinceLastPlay = 1) RETURN f$FacingSqueeze FORCE\n\n"

        profile += "// Facing 4-Bet\n"
        profile += "WHEN (BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 1 AND NumberOfRaisesBeforeFlop = 2 AND RaisesSinceLastPlay = 1) RETURN f$Facing4Bet FORCE\n\n"

        profile += "// Facing 5-Bet\n"
        profile += "WHEN (BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 2 AND NumberOfRaisesBeforeFlop = 2 AND RaisesSinceLastPlay = 1) RETURN f$Facing5Bet FORCE\n\n"

        profile += "// Default action if no scenario is matched\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        # Post-flop placeholders (to be expanded later)
        profile += "//*****************************************************************************\n"
        profile += "//\n"
        profile += "// POST-FLOP PLACEHOLDERS\n"
        profile += "// These are basic placeholders that would need to be expanded\n"
        profile += "//\n"
        profile += "//*****************************************************************************\n\n"

        profile += "##f$flop##\n"
        profile += "// Basic C-bet strategy\n"
        profile += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition RETURN BetHalfPot FORCE\n"
        profile += "WHEN HaveTopPair OR HaveOverPair OR HaveStrongDraws RETURN BetHalfPot FORCE\n"
        profile += "WHEN Others RETURN Check FORCE\n\n"

        profile += "##f$HaveStrongDraws##\n"
        profile += "// Strong draws worth betting\n"
        profile += "WHEN HaveFlushDraw OR HaveStraightDraw RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        profile += "##f$turn##\n"
        profile += "// Basic turn strategy\n"
        profile += "WHEN BotRaisedBeforeFlop AND BotRaisedOnFlop AND f$InPosition RETURN BetHalfPot FORCE\n"
        profile += "WHEN HaveTopPair RETURN BetHalfPot FORCE\n"
        profile += "WHEN Others RETURN Check FORCE\n\n"

        profile += "##f$HaveTopPairOrBetterOrStrongDraw##\n"
        profile += "// Hand strong enough to bet on turn\n"
        profile += "WHEN HaveTopPair OR HaveOverPair OR HaveFlushDraw OR HaveStraightDraw OR HaveTwoPair OR HaveTrips OR HaveStraight OR HaveFlush OR HaveFullHouse OR HaveQuads OR HaveStraightFlush RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        profile += "##f$river##\n"
        profile += "// Basic river strategy\n"
        profile += "WHEN HaveTwoPair  RETURN BetPot FORCE\n"
        profile += "WHEN Others RETURN Check FORCE\n\n"

        # Add Push/Fold strategy
        profile += self.add_push_fold_strategy(settings)

        profile += "//*****************************************************************************\n"
        profile += "//\n"
        profile += "// END OF PROFILE\n"
        profile += "//\n"
        profile += "//*****************************************************************************"
        
        return profile
        
    def add_push_fold_strategy(self, settings):
        """
        Add Push or Fold strategy to the preflop profile
        
        Args:
            settings (dict): Settings dictionary containing push/fold parameters
            
        Returns:
            str: Push/fold strategy text to be added to the profile
        """
        # Extract general aggressive factor from settings
        aggression = settings.get("aggression", 50)
        aggressive_factor = aggression / 50  # 0-2 range where 1 is neutral
        
        # Create ranges based on stack size
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
        
        # Apply aggression adjustments
        for bb_range in push_ranges:
            for position in push_ranges[bb_range]:
                # Adjust push ranges based on aggression (more aggressive = wider pushing range)
                push_ranges[bb_range][position] = min(98, round(push_ranges[bb_range][position] * (0.8 + 0.4 * aggressive_factor)))
                
        for bb_range in call_push_ranges:
            for vs_position in call_push_ranges[bb_range]:
                # Adjust call ranges based on aggression (more aggressive = wider calling range)
                call_push_ranges[bb_range][vs_position] = min(95, round(call_push_ranges[bb_range][vs_position] * (0.8 + 0.4 * aggressive_factor)))
        
        # Convert percentages to thresholds
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
        
        # Generate the push/fold section
        push_fold = "\n//*****************************************************************************\n"
        push_fold += "//\n"
        push_fold += "// PUSH OR FOLD STRATEGY\n"
        push_fold += "//\n"
        push_fold += "// Generated with detailed stack size ranges:\n"
        push_fold += "// - 1BB, 2BB, 3BB, 4BB, 5BB, 6BB, 7BB, 8BB, 9BB, 10BB, 10-15BB, 15-20BB, 20-25BB\n"
        push_fold += "//\n"
        push_fold += "// Aggression Factor applied: " + str(aggressive_factor) + "x\n"
        push_fold += "//\n"
        push_fold += "//*****************************************************************************\n\n"
        
        # Function to determine if we're in Push/Fold mode
        push_fold += "##f$InPushFoldMode##\n"
        push_fold += "// Determine if we're in push/fold mode (less than 25 BBs)\n"
        push_fold += "WHEN f$EffectiveStack < 25 AND istournament RETURN true FORCE\n"
        push_fold += "WHEN Others RETURN false FORCE\n\n"
        
        # Main Push/Fold function
        push_fold += "##f$PushFoldPreflop##\n"
        push_fold += "// Main push/fold function based on stack size\n"
        
        # 1BB range
        push_fold += "// 1BB range\n"
        push_fold += "WHEN f$EffectiveStack <= 1 RETURN f$PushFold_1BB FORCE\n\n"
        
        # 2BB range
        push_fold += "// 2BB range\n"
        push_fold += "WHEN f$EffectiveStack > 1 AND f$EffectiveStack <= 2 RETURN f$PushFold_2BB FORCE\n\n"
        
        # 3BB range
        push_fold += "// 3BB range\n"
        push_fold += "WHEN f$EffectiveStack > 2 AND f$EffectiveStack <= 3 RETURN f$PushFold_3BB FORCE\n\n"
        
        # 4BB range
        push_fold += "// 4BB range\n"
        push_fold += "WHEN f$EffectiveStack > 3 AND f$EffectiveStack <= 4 RETURN f$PushFold_4BB FORCE\n\n"
        
        # 5BB range
        push_fold += "// 5BB range\n"
        push_fold += "WHEN f$EffectiveStack > 4 AND f$EffectiveStack <= 5 RETURN f$PushFold_5BB FORCE\n\n"
        
        # 6BB range
        push_fold += "// 6BB range\n"
        push_fold += "WHEN f$EffectiveStack > 5 AND f$EffectiveStack <= 6 RETURN f$PushFold_6BB FORCE\n\n"
        
        # 7BB range
        push_fold += "// 7BB range\n"
        push_fold += "WHEN f$EffectiveStack > 6 AND f$EffectiveStack <= 7 RETURN f$PushFold_7BB FORCE\n\n"
        
        # 8BB range
        push_fold += "// 8BB range\n"
        push_fold += "WHEN f$EffectiveStack > 7 AND f$EffectiveStack <= 8 RETURN f$PushFold_8BB FORCE\n\n"
        
        # 9BB range
        push_fold += "// 9BB range\n"
        push_fold += "WHEN f$EffectiveStack > 8 AND f$EffectiveStack <= 9 RETURN f$PushFold_9BB FORCE\n\n"
        
        # 10BB range
        push_fold += "// 10BB range\n"
        push_fold += "WHEN f$EffectiveStack > 9 AND f$EffectiveStack <= 10 RETURN f$PushFold_10BB FORCE\n\n"
        
        # 10-15BB range
        push_fold += "// 10-15BB range\n"
        push_fold += "WHEN f$EffectiveStack > 10 AND f$EffectiveStack <= 15 RETURN f$PushFold_10_15BB FORCE\n\n"
        
        # 15-20BB range
        push_fold += "// 15-20BB range\n"
        push_fold += "WHEN f$EffectiveStack > 15 AND f$EffectiveStack <= 20 RETURN f$PushFold_15_20BB FORCE\n\n"
        
        # 20-25BB range
        push_fold += "// 20-25BB range\n"
        push_fold += "WHEN f$EffectiveStack > 20 AND f$EffectiveStack <= 25 RETURN f$PushFold_20_25BB FORCE\n\n"
        
        # Default action
        push_fold += "// Default action\n"
        push_fold += "WHEN Others RETURN Fold FORCE\n\n"
        
        # Create individual functions for each stack size range
        # 1BB range function
        push_fold += self.create_push_fold_function("1", push_thresholds, call_push_thresholds)
        
        # 2BB range function
        push_fold += self.create_push_fold_function("2", push_thresholds, call_push_thresholds)
        
        # 3BB range function
        push_fold += self.create_push_fold_function("3", push_thresholds, call_push_thresholds)
        
        # 4BB range function
        push_fold += self.create_push_fold_function("4", push_thresholds, call_push_thresholds)
        
        # 5BB range function
        push_fold += self.create_push_fold_function("5", push_thresholds, call_push_thresholds)
        
        # 6BB range function
        push_fold += self.create_push_fold_function("6", push_thresholds, call_push_thresholds)
        
        # 7BB range function
        push_fold += self.create_push_fold_function("7", push_thresholds, call_push_thresholds)
        
        # 8BB range function
        push_fold += self.create_push_fold_function("8", push_thresholds, call_push_thresholds)
        
        # 9BB range function
        push_fold += self.create_push_fold_function("9", push_thresholds, call_push_thresholds)
        
        # 10BB range function
        push_fold += self.create_push_fold_function("10", push_thresholds, call_push_thresholds)
        
        # 10-15BB range function
        push_fold += self.create_push_fold_function("10-15", push_thresholds, call_push_thresholds)
        
        # 15-20BB range function
        push_fold += self.create_push_fold_function("15-20", push_thresholds, call_push_thresholds)
        
        # 20-25BB range function
        push_fold += self.create_push_fold_function("20-25", push_thresholds, call_push_thresholds)
        
        return push_fold
        
    def create_push_fold_function(self, bb_range, push_thresholds, call_push_thresholds):
        """Create a function for a specific stack size range"""
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
        
        # Determine which call range to use based on stack size
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

    def collect_push_fold_settings(self):
        """Gather push/fold settings from the UI"""
        # This method would be called by the UI to gather push/fold settings
        # Implement the actual UI collection in main.py
        # Return default values for now
        return {
            # 1BB stack ranges
            "push_1bb_ep": 75,
            "push_1bb_mp": 80,
            "push_1bb_co": 85,
            "push_1bb_btn": 90,
            "push_1bb_sb": 92,
            "push_1bb_bb": 95,
            "call_1bb_vs_ep": 60,
            "call_1bb_vs_mp": 65,
            "call_1bb_vs_co": 70,
            "call_1bb_vs_btn": 75,
            "call_1bb_vs_sb": 80,
            
            # 2BB stack ranges
            "push_2bb_ep": 60,
            "push_2bb_mp": 65,
            "push_2bb_co": 70,
            "push_2bb_btn": 75,
            "push_2bb_sb": 80,
            "push_2bb_bb": 85,
            "call_2bb_vs_ep": 50,
            "call_2bb_vs_mp": 55,
            "call_2bb_vs_co": 60,
            "call_2bb_vs_btn": 65,
            "call_2bb_vs_sb": 70,
            
            # 3BB stack ranges
            "push_3bb_ep": 45,
            "push_3bb_mp": 50,
            "push_3bb_co": 55,
            "push_3bb_btn": 60,
            "push_3bb_sb": 65,
            "push_3bb_bb": 70,
            "call_3bb_vs_ep": 40,
            "call_3bb_vs_mp": 45,
            "call_3bb_vs_co": 50,
            "call_3bb_vs_btn": 55,
            "call_3bb_vs_sb": 60,
            
            # 4BB stack ranges
            "push_4bb_ep": 35,
            "push_4bb_mp": 40,
            "push_4bb_co": 45,
            "push_4bb_btn": 50,
            "push_4bb_sb": 55,
            "push_4bb_bb": 60,
            "call_4bb_vs_ep": 30,
            "call_4bb_vs_mp": 35,
            "call_4bb_vs_co": 40,
            "call_4bb_vs_btn": 45,
            "call_4bb_vs_sb": 50,
            
            # 5BB stack ranges
            "push_5bb_ep": 28,
            "push_5bb_mp": 32,
            "push_5bb_co": 36,
            "push_5bb_btn": 40,
            "push_5bb_sb": 45,
            "push_5bb_bb": 50,
            "call_5bb_vs_ep": 25,
            "call_5bb_vs_mp": 28,
            "call_5bb_vs_co": 32,
            "call_5bb_vs_btn": 36,
            "call_5bb_vs_sb": 40,
            
            # 6BB stack ranges
            "push_6bb_ep": 22,
            "push_6bb_mp": 26,
            "push_6bb_co": 30,
            "push_6bb_btn": 35,
            "push_6bb_sb": 40,
            "push_6bb_bb": 45,
            
            # 7BB stack ranges
            "push_7bb_ep": 18,
            "push_7bb_mp": 22,
            "push_7bb_co": 26,
            "push_7bb_btn": 30,
            "push_7bb_sb": 35,
            "push_7bb_bb": 40,
            
            # 8BB stack ranges
            "push_8bb_ep": 15,
            "push_8bb_mp": 18,
            "push_8bb_co": 22,
            "push_8bb_btn": 26,
            "push_8bb_sb": 30,
            "push_8bb_bb": 35,
            
            # 9BB stack ranges
            "push_9bb_ep": 12,
            "push_9bb_mp": 15,
            "push_9bb_co": 18,
            "push_9bb_btn": 22,
            "push_9bb_sb": 26,
            "push_9bb_bb": 30,
            
            # 10BB stack ranges
            "push_10bb_ep": 10,
            "push_10bb_mp": 12,
            "push_10bb_co": 15,
            "push_10bb_btn": 18,
            "push_10bb_sb": 22,
            "push_10bb_bb": 25,
            
            # 6-10BB call ranges
            "call_6_10bb_vs_ep": 20,
            "call_6_10bb_vs_mp": 22,
            "call_6_10bb_vs_co": 25,
            "call_6_10bb_vs_btn": 28,
            "call_6_10bb_vs_sb": 32,
            
            # 10-15BB stack ranges
            "push_10_15bb_ep": 8,
            "push_10_15bb_mp": 10,
            "push_10_15bb_co": 12,
            "push_10_15bb_btn": 15,
            "push_10_15bb_sb": 18,
            "push_10_15bb_bb": 20,
            "call_10_15bb_vs_ep": 15,
            "call_10_15bb_vs_mp": 18,
            "call_10_15bb_vs_co": 20,
            "call_10_15bb_vs_btn": 22,
            "call_10_15bb_vs_sb": 25,
            
            # 15-20BB stack ranges
            "push_15_20bb_ep": 5,
            "push_15_20bb_mp": 8,
            "push_15_20bb_co": 10,
            "push_15_20bb_btn": 12,
            "push_15_20bb_sb": 15,
            "push_15_20bb_bb": 18,
            
            # 20-25BB stack ranges
            "push_20_25bb_ep": 3,
            "push_20_25bb_mp": 5,
            "push_20_25bb_co": 7,
            "push_20_25bb_btn": 10,
            "push_20_25bb_sb": 12,
            "push_20_25bb_bb": 15,
            
            # 15-25BB call ranges
            "call_15_25bb_vs_ep": 10,
            "call_15_25bb_vs_mp": 12,
            "call_15_25bb_vs_co": 15,
            "call_15_25bb_vs_btn": 18,
            "call_15_25bb_vs_sb": 20
        }
