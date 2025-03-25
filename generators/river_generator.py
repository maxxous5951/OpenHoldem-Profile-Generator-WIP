class RiverProfileGenerator:
    def __init__(self):
        pass
        
    def get_handrank_threshold(self, percentage):
        """Convert a percentage into a handrank threshold value"""
        # HandRank goes from 1 to 169, where 1 is the best hand (AA)
        # Convert percentage to a hand rank value
        # 0% = only AA (rank 1)
        # 100% = all hands (rank 169)
        return round(1 + (percentage / 100) * 168)
    
    def generate_river_profile(self, settings):
        """Generate the river part of the OpenHoldem profile"""
        # Extract river settings
        third_barrel_freq = settings.get("third_barrel_freq", 40)
        delayed_second_barrel_freq = settings.get("delayed_second_barrel_freq", 30)
        ip_river_bet_size = settings.get("ip_river_bet_size", "75")
        oop_river_bet_size = settings.get("oop_river_bet_size", "75")
        river_checkraise_freq = settings.get("river_checkraise_freq", 15)
        river_float_freq = settings.get("river_float_freq", 20)
        river_probe_freq = settings.get("river_probe_freq", 25)
        river_fold_to_bet_freq = settings.get("river_fold_to_bet_freq", 70)
        river_bluff_raise_freq = settings.get("river_bluff_raise_freq", 10)
        river_value_range = settings.get("river_value_range", 60)
        river_bluff_range = settings.get("river_bluff_range", 15)
        river_check_behind_range = settings.get("river_check_behind_range", 80)
        
        # Global aggression
        aggression = settings.get("aggression", 50)
        aggressive_factor = aggression / 50  # 0-2 range where 1 is neutral
        
        # Calculate thresholds
        third_barrel_threshold = self.get_handrank_threshold(third_barrel_freq)
        delayed_second_barrel_threshold = self.get_handrank_threshold(delayed_second_barrel_freq)
        river_checkraise_threshold = self.get_handrank_threshold(river_checkraise_freq)
        river_float_threshold = self.get_handrank_threshold(river_float_freq)
        river_probe_threshold = self.get_handrank_threshold(river_probe_freq)
        river_bluff_raise_threshold = self.get_handrank_threshold(river_bluff_raise_freq)
        fold_threshold = self.get_handrank_threshold(100 - river_fold_to_bet_freq)
        river_value_threshold = self.get_handrank_threshold(river_value_range)
        river_bluff_threshold = self.get_handrank_threshold(river_bluff_range)
        river_check_behind_threshold = self.get_handrank_threshold(river_check_behind_range)
        
        # Adjust thresholds based on global aggression
        third_barrel_threshold = round(third_barrel_threshold * (1.2 - 0.4 * aggressive_factor))
        delayed_second_barrel_threshold = round(delayed_second_barrel_threshold * (1.2 - 0.4 * aggressive_factor))
        river_checkraise_threshold = round(river_checkraise_threshold * (1.2 - 0.4 * aggressive_factor))
        river_float_threshold = round(river_float_threshold * (1.2 - 0.4 * aggressive_factor))
        river_bluff_threshold = round(river_bluff_threshold * (1.2 - 0.4 * aggressive_factor))
        
        # Generate the profile text
        profile = "//*****************************************************************************\n"
        profile += "//\n"
        profile += "// RIVER STRATEGY\n"
        profile += "//\n"
        profile += "// Generated with the following settings:\n"
        profile += f"// - Third Barrel Frequency: {third_barrel_freq}%\n"
        profile += f"// - Delayed Second Barrel Frequency: {delayed_second_barrel_freq}%\n"
        profile += f"// - IP River Bet Size: {ip_river_bet_size}% of pot\n"
        profile += f"// - OOP River Bet Size: {oop_river_bet_size}% of pot\n"
        profile += f"// - River Check-Raise Frequency: {river_checkraise_freq}%\n"
        profile += f"// - River Float Frequency: {river_float_freq}%\n"
        profile += f"// - River Probe Frequency: {river_probe_freq}%\n"
        profile += f"// - River Fold to Bet Frequency: {river_fold_to_bet_freq}%\n"
        profile += f"// - River Bluff Raise Frequency: {river_bluff_raise_freq}%\n"
        profile += f"// - River Value Range: {river_value_range}%\n"
        profile += f"// - River Bluff Range: {river_bluff_range}%\n"
        profile += f"// - River Check Behind Range: {river_check_behind_range}%\n"
        profile += "//\n"
        profile += "//*****************************************************************************\n\n"

        profile += "##f$river##\n"
        profile += "// Main river decision function\n"
        profile += "// Determines action based on scenario detection\n\n"

        profile += "// Third Barrel and Delayed Second Barrel scenarios\n"
        profile += "WHEN f$ThirdBarrel RETURN f$RiverThirdBarrel FORCE\n"
        profile += "WHEN f$DelayedSecondBarrel RETURN f$RiverDelayedSecondBarrel FORCE\n\n"

        profile += "// Facing bet scenarios\n"
        profile += "WHEN f$FacingThirdBarrel RETURN f$FacingThirdBarrel FORCE\n"
        profile += "WHEN f$FacingDelayedSecondBarrel RETURN f$FacingDelayedSecondBarrel FORCE\n\n"

        profile += "// Facing check scenarios\n"
        profile += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition AND NoBettingOnTurn RETURN f$RiverProbeAfterCheckedTurn FORCE\n"
        profile += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND NOT f$InPosition AND NoBettingOnTurn RETURN f$RiverOOPAfterCheckedTurn FORCE\n\n"

        profile += "// Facing check to our turn bet\n"
        profile += "WHEN BotRaisedBeforeFlop AND BotRaisedOnFlop AND BotRaisedOnTurn AND BotsActionsOnThisRoundIncludingChecks = 0 AND Bets = 0 AND f$InPosition RETURN f$RiverContinuationAfterTurnBet FORCE\n\n"

        profile += "// Check-raise response\n"
        profile += "WHEN f$FacingCheckRaiseToThirdBarrel RETURN f$FacingCheckRaiseToThirdBarrel FORCE\n"
        profile += "WHEN f$FacingRaiseToThirdBarrel RETURN f$FacingRaiseToThirdBarrel FORCE\n\n"

        profile += "// Default action\n"
        profile += "WHEN Others Check FORCE\n\n"

        # Third Barrel
        profile += "##f$RiverThirdBarrel##\n"
        profile += f"// Third barrel after betting flop and turn, default size: {ip_river_bet_size}% of pot\n"
        profile += "// At river, we polarize to value bets and bluffs\n\n"
        
        profile += "// Value betting\n"
        profile += f"WHEN f$RiverValueHands RaiseBy {ip_river_bet_size}% FORCE\n\n"
        
        profile += "// Bluffing with missed draws and blockers\n"
        profile += f"WHEN f$RiverBluffCandidates AND handrank169 <= {river_bluff_threshold} RaiseBy {ip_river_bet_size}% FORCE\n\n"
        
        profile += "// Board texture-based decisions\n"
        profile += f"WHEN f$DrawHeavyBoard AND handrank169 <= {round(third_barrel_threshold * 0.8)} RaiseBy {ip_river_bet_size}% FORCE\n"
        profile += f"WHEN f$PairedBoard AND handrank169 <= {round(third_barrel_threshold * 0.9)} RaiseBy {ip_river_bet_size}% FORCE\n"
        profile += f"WHEN handrank169 <= {third_barrel_threshold} RaiseBy {ip_river_bet_size}% FORCE\n\n"
        
        profile += "// Check back marginal hands\n"
        profile += "WHEN Others Check FORCE\n\n"

        # Delayed Second Barrel on River
        profile += "##f$RiverDelayedSecondBarrel##\n"
        profile += f"// Delayed second barrel after checking turn, default size: {ip_river_bet_size}% of pot\n"
        profile += "// More selective with value betting, less bluffing\n\n"
        
        profile += "// Value betting\n"
        profile += f"WHEN f$RiverStrongHands RaiseBy {ip_river_bet_size}% FORCE\n\n"
        
        profile += "// Occasionally bluff with missed draws\n"
        profile += f"WHEN f$RiverBluffCandidates AND handrank169 <= {round(river_bluff_threshold * 0.7)} RaiseBy {ip_river_bet_size}% FORCE\n\n"
        
        profile += "// Default check\n"
        profile += "WHEN Others Check FORCE\n\n"

        # Facing Third Barrel
        profile += "##f$FacingThirdBarrel##\n"
        profile += "// Response when facing a third barrel on the river\n\n"
        
        profile += "// Call or raise with strong hands\n"
        profile += "WHEN f$RiverNutHands RaisePot FORCE\n"
        profile += "WHEN f$RiverStrongHands Call FORCE\n\n"
        
        profile += "// Hero raise as a bluff with specific holdings\n"
        profile += f"WHEN handrank169 <= {river_bluff_raise_threshold} AND f$RiverBluffRaiseHands RaisePot FORCE\n\n"
        
        profile += "// Call with hands that have showdown value\n"
        profile += f"WHEN handrank169 <= {fold_threshold} Call FORCE\n\n"
        
        profile += "// Default fold\n"
        profile += "WHEN Others Fold FORCE\n\n"

        # Facing Delayed Second Barrel on River
        profile += "##f$FacingDelayedSecondBarrel##\n"
        profile += "// Response when facing a delayed second barrel on the river\n\n"
        
        profile += "// Similar logic to facing third barrel but more calling\n"
        profile += "WHEN f$RiverNutHands RaisePot FORCE\n"
        profile += "WHEN f$RiverStrongHands Call FORCE\n\n"
        
        profile += "// More calling when villain showed weakness on turn\n"
        profile += f"WHEN handrank169 <= {round(fold_threshold * 1.2)} Call FORCE\n\n"
        
        profile += "// More aggressive raising range\n"
        profile += f"WHEN handrank169 <= {round(river_bluff_raise_threshold * 1.3)} AND f$RiverBluffRaiseHands RaisePot FORCE\n\n"
        
        profile += "// Default fold\n"
        profile += "WHEN Others Fold FORCE\n\n"

        # Facing Check-Raise to Third Barrel
        profile += "##f$FacingCheckRaiseToThirdBarrel##\n"
        profile += "// Response when opponent check-raises our third barrel\n\n"
        
        profile += "// Continue with very strong hands\n"
        profile += "WHEN f$RiverNutHands RaisePot FORCE\n"
        profile += "WHEN f$RiverStrongHands Call FORCE\n\n"
        
        profile += "// Defense frequency against check-raises\n"
        profile += f"WHEN handrank169 <= {river_checkraise_threshold} Call FORCE\n\n"
        
        profile += "// Default fold\n"
        profile += "WHEN Others Fold FORCE\n\n"

        # River Probe After Checked Turn
        profile += "##f$RiverProbeAfterCheckedTurn##\n"
        profile += f"// Probe betting when in position after a checked turn, default size: {ip_river_bet_size}% of pot\n\n"
        
        profile += "// Value bet with strong hands\n"
        profile += f"WHEN f$RiverValueHands RaiseBy {ip_river_bet_size}% FORCE\n\n"
        
        profile += "// Opportunistic betting when checked to twice\n"
        profile += f"WHEN f$RiverBluffCandidates AND handrank169 <= {river_probe_threshold} RaiseBy {ip_river_bet_size}% FORCE\n\n"
        
        profile += "// Check back with showdown value\n"
        profile += f"WHEN handrank169 <= {river_check_behind_threshold} Check FORCE\n\n"
        
        profile += "// Default check back\n"
        profile += "WHEN Others Check FORCE\n\n"

        # River OOP After Checked Turn
        profile += "##f$RiverOOPAfterCheckedTurn##\n"
        profile += f"// OOP lead betting after a checked turn, default size: {oop_river_bet_size}% of pot\n\n"
        
        profile += "// Only lead with strong hands\n"
        profile += f"WHEN f$RiverStrongHands RaiseBy {oop_river_bet_size}% FORCE\n\n"
        
        profile += "// Occasionally lead as a bluff\n"
        profile += f"WHEN f$RiverBluffCandidates AND handrank169 <= {round(river_probe_threshold * 0.6)} RaiseBy {oop_river_bet_size}% FORCE\n\n"
        
        profile += "// Default check\n"
        profile += "WHEN Others Check FORCE\n\n"

        # River Continuation After Turn Bet
        profile += "##f$RiverContinuationAfterTurnBet##\n"
        profile += f"// In position facing a check after we bet the turn, default size: {ip_river_bet_size}% of pot\n\n"
        
        profile += "// Value bet with strong hands\n"
        profile += f"WHEN f$RiverValueHands RaiseBy {ip_river_bet_size}% FORCE\n\n"
        
        profile += "// Selective bluffing\n"
        profile += f"WHEN f$RiverBluffCandidates AND handrank169 <= {round(river_bluff_threshold * 0.8)} RaiseBy {ip_river_bet_size}% FORCE\n\n"
        
        profile += "// Check back with showdown value\n"
        profile += f"WHEN handrank169 <= {river_check_behind_threshold} Check FORCE\n\n"
        
        profile += "// Default check back\n"
        profile += "WHEN Others Check FORCE\n\n"

        # Facing Raise to Third Barrel
        profile += "##f$FacingRaiseToThirdBarrel##\n"
        profile += "// Response when opponent raises our third barrel\n\n"
        
        profile += "// Continue only with very strong hands\n"
        profile += "WHEN f$RiverNutHands RaisePot FORCE\n"
        profile += "WHEN f$RiverStrongHands Call FORCE\n\n"
        
        profile += "// Default fold\n"
        profile += "WHEN Others Fold FORCE\n\n"

        # Hand category helper functions
        profile += "//*****************************************************************************\n"
        profile += "//\n"
        profile += "// HAND CATEGORY HELPER FUNCTIONS FOR RIVER\n"
        profile += "//\n"
        profile += "//*****************************************************************************\n\n"

        # Value Hands on River
        profile += "##f$RiverValueHands##\n"
        profile += "// Hands worth value betting on the river\n"
        profile += "WHEN HaveStraightFlush RETURN true FORCE\n"
        profile += "WHEN HaveQuads RETURN true FORCE\n"
        profile += "WHEN HaveFullHouse RETURN true FORCE\n"
        profile += "WHEN HaveFlush RETURN true FORCE\n"
        profile += "WHEN HaveStraight RETURN true FORCE\n"
        profile += "WHEN HaveTrips RETURN true FORCE\n"
        profile += "WHEN HaveTwoPair AND HaveTopPair RETURN true FORCE\n"
        profile += "WHEN HaveOverPair RETURN true FORCE\n"
        profile += "WHEN HaveTopPair AND f$HaveGoodKicker RETURN true FORCE\n"
        profile += "WHEN HaveSecondTopPair AND f$HaveTopKicker RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        # Strong Hands on River
        profile += "##f$RiverStrongHands##\n"
        profile += "// Strong hands that can call a river bet\n"
        profile += "WHEN HaveStraightFlush RETURN true FORCE\n"
        profile += "WHEN HaveQuads RETURN true FORCE\n"
        profile += "WHEN HaveFullHouse RETURN true FORCE\n"
        profile += "WHEN HaveFlush RETURN true FORCE\n"
        profile += "WHEN HaveStraight RETURN true FORCE\n"
        profile += "WHEN HaveTrips RETURN true FORCE\n"
        profile += "WHEN HaveTwoPair RETURN true FORCE\n"
        profile += "WHEN HaveOverPair RETURN true FORCE\n"
        profile += "WHEN HaveTopPair AND rankloplayer >= queen RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        # Nut Hands on River
        profile += "##f$RiverNutHands##\n"
        profile += "// Very strong hands that should be played aggressively\n"
        profile += "WHEN HaveStraightFlush RETURN true FORCE\n"
        profile += "WHEN HaveQuads RETURN true FORCE\n"
        profile += "WHEN HaveFullHouse AND NOT TwoPairOnBoard RETURN true FORCE\n"
        profile += "WHEN HaveNutFlush RETURN true FORCE\n"
        profile += "WHEN HaveNutStraight RETURN true FORCE\n"
        profile += "WHEN HaveSet AND TwoPairOnBoard RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        # Bluff Candidates on River
        profile += "##f$RiverBluffCandidates##\n"
        profile += "// Hands suitable for bluffing on the river\n"
        profile += "// Usually missed draws or blockers to strong hands\n"
        profile += "WHEN f$HadFlushDrawOnTurn AND NOT HaveFlush RETURN true FORCE\n"
        profile += "WHEN f$HadStraightDrawOnTurn AND NOT HaveStraight RETURN true FORCE\n"
        profile += "WHEN TopPairKickerRank >= ace AND FlushPossible RETURN true FORCE\n"
        profile += "WHEN Overcards = 2 AND f$DryBoard RETURN true FORCE\n"
        profile += "WHEN f$HaveBlockersToNuts RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        # Bluff Raise Hands on River
        profile += "##f$RiverBluffRaiseHands##\n"
        profile += "// Hands suitable for bluff-raising on the river\n"
        profile += "// Usually hands with blockers to nuts\n"
        profile += "WHEN f$HaveBlockersToNuts RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        # Board texture helper functions
        profile += "##f$DrawHeavyBoard##\n"
        profile += "// Detects if the board is draw-heavy (many possible draws)\n"
        profile += "WHEN FlushPossible RETURN true FORCE\n"
        profile += "WHEN StraightPossible RETURN true FORCE\n"
        profile += "WHEN f$FourToFlush RETURN true FORCE\n"
        profile += "WHEN f$FourToStraight RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        profile += "##f$PairedBoard##\n"
        profile += "// Detects if the board is paired\n"
        profile += "WHEN PairOnBoard RETURN true FORCE\n"
        profile += "WHEN TripsOnBoard RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"
        
        profile += "##f$HaveBlockersToNuts##\n"
        profile += "// Detects if we have blockers to the nuts\n"
        profile += "// For example holding one flush card when flush is possible\n"
        profile += "WHEN FlushPossible AND ((FirstHoleCardSuit == DominantSuitCommon AND SecondHoleCardSuit != DominantSuitCommon) OR (FirstHoleCardSuit != DominantSuitCommon AND SecondHoleCardSuit == DominantSuitCommon)) RETURN true FORCE\n"
        profile += "WHEN StraightPossible AND ((rankhiplayer == HighCardOfBestPossibleStraight + 1) OR (rankloplayer == HighCardOfBestPossibleStraight + 1)) RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"
        
        profile += "##f$FourToFlush##\n"
        profile += "// Detects if there are four cards of the same suit on board\n"
        profile += "WHEN nsuitedcommon >= 4 RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"
        
        profile += "##f$FourToStraight##\n"
        profile += "// Detects if there are four consecutive cards on board\n"
        profile += "WHEN nstraightcommon >= 4 RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"
        
        profile += "##f$HaveTopKicker##\n"
        profile += "// Checks if we have the top kicker possible\n"
        profile += "WHEN rankhiplayer >= rankhicommon RETURN true FORCE\n"
        profile += "WHEN rankloplayer >= rankhicommon RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"
        
        profile += "##f$HadFlushDrawOnTurn##\n"
        profile += "// Checks if we had a flush draw on the turn\n"
        profile += "WHEN hi_nsuited3 == 4 AND FirstHoleCardSuit == hi_tsuit3 AND SecondHoleCardSuit == hi_tsuit3 RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"
        
        profile += "##f$HadStraightDrawOnTurn##\n"
        profile += "// Checks if we had a straight draw on the turn\n"
        profile += "WHEN hi_nstraightfill3 == 1 RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"
        
        return profile
