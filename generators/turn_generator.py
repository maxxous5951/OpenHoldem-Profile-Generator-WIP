class TurnProfileGenerator:
    def __init__(self):
        pass
        
    def get_handrank_threshold(self, percentage):
        """Convert a percentage into a handrank threshold value"""
        # HandRank goes from 1 to 169, where 1 is the best hand (AA)
        # Convert percentage to a hand rank value
        # 0% = only AA (rank 1)
        # 100% = all hands (rank 169)
        return round(1 + (percentage / 100) * 168)
    
    def generate_turn_profile(self, settings):
        """Generate the turn part of the OpenHoldem profile"""
        # Extract turn settings
        second_barrel_freq = settings.get("second_barrel_freq", 60)
        delayed_cbet_freq = settings.get("delayed_cbet_freq", 40)
        ip_turn_bet_size = settings.get("ip_turn_bet_size", "66")
        oop_turn_bet_size = settings.get("oop_turn_bet_size", "75")
        turn_checkraise_freq = settings.get("turn_checkraise_freq", 25)
        turn_float_freq = settings.get("turn_float_freq", 30)
        turn_probe_freq = settings.get("turn_probe_freq", 35)
        turn_fold_to_cbet_freq = settings.get("turn_fold_to_cbet_freq", 60)
        turn_bluff_raise_freq = settings.get("turn_bluff_raise_freq", 20)
        scare_card_adjust = settings.get("scare_card_adjust", -15) / 100.0  # Convert to decimal
        draw_complete_adjust = settings.get("draw_complete_adjust", 10) / 100.0  # Convert to decimal
        
        # Global aggression
        aggression = settings.get("aggression", 50)
        aggressive_factor = aggression / 50  # 0-2 range where 1 is neutral
        
        # Calculate thresholds
        second_barrel_threshold = self.get_handrank_threshold(second_barrel_freq)
        delayed_cbet_threshold = self.get_handrank_threshold(delayed_cbet_freq)
        turn_checkraise_threshold = self.get_handrank_threshold(turn_checkraise_freq)
        turn_float_threshold = self.get_handrank_threshold(turn_float_freq)
        turn_probe_threshold = self.get_handrank_threshold(turn_probe_freq)
        turn_bluff_raise_threshold = self.get_handrank_threshold(turn_bluff_raise_freq)
        fold_threshold = self.get_handrank_threshold(100 - turn_fold_to_cbet_freq)
        
        # Adjust thresholds based on global aggression
        second_barrel_threshold = round(second_barrel_threshold * (1.2 - 0.4 * aggressive_factor))
        delayed_cbet_threshold = round(delayed_cbet_threshold * (1.2 - 0.4 * aggressive_factor))
        turn_checkraise_threshold = round(turn_checkraise_threshold * (1.2 - 0.4 * aggressive_factor))
        turn_float_threshold = round(turn_float_threshold * (1.2 - 0.4 * aggressive_factor))
        
        # Generate the profile text
        profile = "//*****************************************************************************\n"
        profile += "//\n"
        profile += "// TURN STRATEGY\n"
        profile += "//\n"
        profile += "// Generated with the following settings:\n"
        profile += f"// - Second Barrel Frequency: {second_barrel_freq}%\n"
        profile += f"// - Delayed C-Bet Frequency: {delayed_cbet_freq}%\n"
        profile += f"// - IP Turn Bet Size: {ip_turn_bet_size}% of pot\n"
        profile += f"// - OOP Turn Bet Size: {oop_turn_bet_size}% of pot\n"
        profile += f"// - Turn Check-Raise Frequency: {turn_checkraise_freq}%\n"
        profile += f"// - Turn Float Frequency: {turn_float_freq}%\n"
        profile += f"// - Turn Probe Frequency: {turn_probe_freq}%\n"
        profile += f"// - Turn Fold to C-Bet Frequency: {turn_fold_to_cbet_freq}%\n"
        profile += f"// - Turn Bluff Raise Frequency: {turn_bluff_raise_freq}%\n"
        profile += f"// - Scare Card Adjustment: {settings.get('scare_card_adjust', -15)}%\n"
        profile += f"// - Draw Complete Adjustment: {settings.get('draw_complete_adjust', 10)}%\n"
        profile += "//\n"
        profile += "//*****************************************************************************\n\n"

        profile += "##f$turn##\n"
        profile += "// Main turn decision function\n"
        profile += "// Determines action based on scenario detection\n\n"

        profile += "// C-Bet and Second Barrel scenarios\n"
        profile += "WHEN f$SecondBarrel RETURN f$TurnSecondBarrel FORCE\n"
        profile += "WHEN f$DelayedCbet RETURN f$TurnDelayedCbet FORCE\n\n"

        profile += "// Facing bet scenarios\n"
        profile += "WHEN f$FacingSecondBarrel RETURN f$FacingSecondBarrel FORCE\n"
        profile += "WHEN f$FacingDelayedCbet RETURN f$FacingDelayedCbet FORCE\n\n"

        profile += "// Facing check scenarios\n"
        profile += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition AND NoBettingOnFlop RETURN f$TurnProbeAfterCheckedFlop FORCE\n"
        profile += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND NOT f$InPosition AND NoBettingOnFlop RETURN f$TurnOOPAfterCheckedFlop FORCE\n\n"

        profile += "// Facing check to our flop bet\n"
        profile += "WHEN BotRaisedBeforeFlop AND BotRaisedOnFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND Bets = 0 AND f$InPosition RETURN f$TurnContinuationAfterFlopBet FORCE\n\n"

        profile += "// Check-raise response\n"
        profile += "WHEN f$FacingCheckRaiseToSecondBarrel RETURN f$FacingCheckRaiseToSecondBarrel FORCE\n"
        profile += "WHEN f$FacingRaiseToSecondBarrel RETURN f$FacingRaiseToSecondBarrel FORCE\n\n"

        profile += "// Default action\n"
        profile += "WHEN Others Check FORCE\n\n"

        # Second Barrel
        profile += "##f$TurnSecondBarrel##\n"
        profile += f"// Second barrel after betting the flop, default size: {ip_turn_bet_size}% of pot\n"
        profile += "// Adjust based on board texture and previous actions\n\n"
        
        profile += "// Always continue with made hands\n"
        profile += f"WHEN f$TurnValueHands RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        profile += "// Continue with strong draws\n"
        profile += f"WHEN f$TurnStrongDraws RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        profile += "// Board texture-based adjustments\n"
        profile += f"WHEN f$ScareCard AND handrank169 <= {round(second_barrel_threshold * (1 + scare_card_adjust))} RaiseBy {ip_turn_bet_size}% FORCE\n"
        profile += f"WHEN f$DrawComplete AND handrank169 <= {round(second_barrel_threshold * (1 + draw_complete_adjust))} RaiseBy {ip_turn_bet_size}% FORCE\n"
        profile += f"WHEN f$WetBoard AND handrank169 <= {round(second_barrel_threshold * 0.9)} RaiseBy {ip_turn_bet_size}% FORCE\n"
        profile += f"WHEN f$DryBoard AND handrank169 <= {round(second_barrel_threshold * 1.1)} RaiseBy {ip_turn_bet_size}% FORCE\n"
        profile += f"WHEN handrank169 <= {second_barrel_threshold} RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        profile += "// Default check\n"
        profile += "WHEN Others Check FORCE\n\n"

        # Delayed C-Bet
        profile += "##f$TurnDelayedCbet##\n"
        profile += f"// Delayed c-bet after checking the flop, default size: {ip_turn_bet_size}% of pot\n"
        profile += "// Generally more selective than a second barrel\n\n"
        
        profile += "// Always bet with made hands\n"
        profile += f"WHEN f$TurnValueHands RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        profile += "// Continue with strong draws on appropriate boards\n"
        profile += f"WHEN f$TurnStrongDraws AND f$WetBoard RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        profile += "// Board texture-based adjustments\n"
        profile += f"WHEN f$ScareCard AND handrank169 <= {round(delayed_cbet_threshold * (1 + scare_card_adjust * 0.8))} RaiseBy {ip_turn_bet_size}% FORCE\n"
        profile += f"WHEN f$DrawComplete AND handrank169 <= {round(delayed_cbet_threshold * (1 + draw_complete_adjust * 0.8))} RaiseBy {ip_turn_bet_size}% FORCE\n"
        profile += f"WHEN f$DryBoard AND handrank169 <= {round(delayed_cbet_threshold * 1.1)} RaiseBy {ip_turn_bet_size}% FORCE\n"
        profile += f"WHEN handrank169 <= {delayed_cbet_threshold} RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        profile += "// Default check\n"
        profile += "WHEN Others Check FORCE\n\n"

        # Facing Second Barrel
        profile += "##f$FacingSecondBarrel##\n"
        profile += "// Response when facing a second barrel on the turn\n\n"
        
        profile += "// Always continue with strong hands\n"
        profile += "WHEN f$TurnStrongHands RaisePot FORCE\n"
        profile += "WHEN f$TurnValueHands Call FORCE\n\n"
        
        profile += "// Continue with good draws\n"
        profile += f"WHEN f$TurnStrongDraws Call FORCE\n\n"
        
        profile += "// Check-raise bluff with specific holdings\n"
        profile += f"WHEN handrank169 <= {turn_bluff_raise_threshold} AND f$TurnSemiBluffHands RaisePot FORCE\n\n"
        
        profile += "// Float with position\n"
        profile += f"WHEN f$InPosition AND handrank169 <= {turn_float_threshold} Call FORCE\n\n"
        
        profile += "// Call with hands that have showdown value\n"
        profile += f"WHEN handrank169 <= {fold_threshold} Call FORCE\n\n"
        
        profile += "// Default fold\n"
        profile += "WHEN Others Fold FORCE\n\n"

        # Facing Delayed C-Bet
        profile += "##f$FacingDelayedCbet##\n"
        profile += "// Response when facing a delayed c-bet on the turn\n\n"
        
        profile += "// Similar logic to facing a second barrel\n"
        profile += "WHEN f$TurnStrongHands RaisePot FORCE\n"
        profile += "WHEN f$TurnValueHands Call FORCE\n\n"
        
        profile += "// More inclined to raise with draws when villain showed weakness on flop\n"
        profile += f"WHEN f$TurnStrongDraws AND handrank169 <= {round(turn_checkraise_threshold * 1.2)} RaisePot FORCE\n"
        profile += f"WHEN f$TurnStrongDraws Call FORCE\n\n"
        
        profile += "// More aggressive raising range\n"
        profile += f"WHEN handrank169 <= {round(turn_bluff_raise_threshold * 1.2)} RaisePot FORCE\n\n"
        
        profile += "// Default fold\n"
        profile += "WHEN Others Fold FORCE\n\n"

        # Facing Check-Raise to Second Barrel
        profile += "##f$FacingCheckRaiseToSecondBarrel##\n"
        profile += "// Response when opponent check-raises our second barrel\n\n"
        
        profile += "// Continue with strong hands\n"
        profile += "WHEN f$TurnStrongHands RaisePot FORCE\n"
        profile += "WHEN f$TurnValueHands Call FORCE\n\n"
        
        profile += "// Continue with strong draws\n"
        profile += f"WHEN f$TurnStrongDraws AND handrank169 <= {round(turn_checkraise_threshold * 0.8)} Call FORCE\n\n"
        
        profile += "// Defense frequency against check-raises\n"
        profile += f"WHEN handrank169 <= {turn_checkraise_threshold} Call FORCE\n\n"
        
        profile += "// Default fold\n"
        profile += "WHEN Others Fold FORCE\n\n"

        # Turn Probe After Checked Flop
        profile += "##f$TurnProbeAfterCheckedFlop##\n"
        profile += f"// Probe betting when in position after a checked flop, default size: {ip_turn_bet_size}% of pot\n\n"
        
        profile += "// Always bet with made hands\n"
        profile += f"WHEN f$TurnValueHands RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        profile += "// Probe with strong draws\n"
        profile += f"WHEN f$TurnStrongDraws RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        profile += "// Opportunistic betting when checked to twice\n"
        profile += f"WHEN handrank169 <= {turn_probe_threshold} RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        profile += "// Default check back\n"
        profile += "WHEN Others Check FORCE\n\n"

        # Turn OOP After Checked Flop
        profile += "##f$TurnOOPAfterCheckedFlop##\n"
        profile += f"// OOP lead betting after a checked flop, default size: {oop_turn_bet_size}% of pot\n\n"
        
        profile += "// Only lead with strong hands\n"
        profile += f"WHEN f$TurnValueHands RaiseBy {oop_turn_bet_size}% FORCE\n\n"
        
        profile += "// Lead with some strong draws\n"
        profile += f"WHEN f$TurnStrongDraws AND handrank169 <= {round(turn_probe_threshold * 0.7)} RaiseBy {oop_turn_bet_size}% FORCE\n\n"
        
        profile += "// Default check\n"
        profile += "WHEN Others Check FORCE\n\n"

        # Turn Continuation After Flop Bet
        profile += "##f$TurnContinuationAfterFlopBet##\n"
        profile += f"// In position facing a check after we bet the flop, default size: {ip_turn_bet_size}% of pot\n\n"
        
        profile += "// Continue betting with value hands\n"
        profile += f"WHEN f$TurnValueHands RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        profile += "// Be selective with semi-bluffs\n"
        profile += f"WHEN f$TurnStrongDraws AND handrank169 <= {round(second_barrel_threshold * 0.8)} RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        profile += "// Board texture-based continuation\n"
        profile += f"WHEN f$DryBoard AND handrank169 <= {round(second_barrel_threshold * 0.9)} RaiseBy {ip_turn_bet_size}% FORCE\n"
        profile += f"WHEN handrank169 <= {round(second_barrel_threshold * 0.7)} RaiseBy {ip_turn_bet_size}% FORCE\n\n"
        
        profile += "// Default check back\n"
        profile += "WHEN Others Check FORCE\n\n"

        # Facing Raise to Second Barrel
        profile += "##f$FacingRaiseToSecondBarrel##\n"
        profile += "// Response when opponent raises our second barrel\n\n"
        
        profile += "// Continue with very strong hands\n"
        profile += "WHEN f$TurnStrongHands RaisePot FORCE\n"
        profile += "WHEN f$TurnValueHands Call FORCE\n\n"
        
        profile += "// Be more cautious with draws\n"
        profile += f"WHEN f$TurnStrongDraws AND handrank169 <= {round(turn_checkraise_threshold * 0.7)} Call FORCE\n\n"
        
        profile += "// Default fold\n"
        profile += "WHEN Others Fold FORCE\n\n"

        # Hand category helper functions
        profile += "//*****************************************************************************\n"
        profile += "//\n"
        profile += "// HAND CATEGORY HELPER FUNCTIONS FOR TURN\n"
        profile += "//\n"
        profile += "//*****************************************************************************\n\n"

        # Value Hands on Turn
        profile += "##f$TurnValueHands##\n"
        profile += "// Hands worth value betting on the turn\n"
        profile += "WHEN HaveStraightFlush RETURN true FORCE\n"
        profile += "WHEN HaveQuads RETURN true FORCE\n"
        profile += "WHEN HaveFullHouse RETURN true FORCE\n"
        profile += "WHEN HaveFlush RETURN true FORCE\n"
        profile += "WHEN HaveStraight RETURN true FORCE\n"
        profile += "WHEN HaveTrips RETURN true FORCE\n"
        profile += "WHEN HaveTwoPair RETURN true FORCE\n"
        profile += "WHEN HaveOverPair RETURN true FORCE\n"
        profile += "WHEN HaveTopPair AND f$HaveGoodKicker RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        # Strong Hands on Turn
        profile += "##f$TurnStrongHands##\n"
        profile += "// Very strong hands that should be played aggressively\n"
        profile += "WHEN HaveStraightFlush RETURN true FORCE\n"
        profile += "WHEN HaveQuads RETURN true FORCE\n"
        profile += "WHEN HaveFullHouse RETURN true FORCE\n"
        profile += "WHEN HaveFlush RETURN true FORCE\n"
        profile += "WHEN HaveStraight RETURN true FORCE\n"
        profile += "WHEN HaveSet RETURN true FORCE\n"
        profile += "WHEN HaveTwoPair AND HaveTopPair RETURN true FORCE\n"
        profile += "WHEN HaveOverPair AND rankhiplayer >= queen RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        # Strong Draws on Turn
        profile += "##f$TurnStrongDraws##\n"
        profile += "// Strong drawing hands on the turn\n"
        profile += "WHEN HaveFlushDraw AND HaveStraightDraw RETURN true FORCE\n"
        profile += "WHEN HaveNutFlushDraw RETURN true FORCE\n"
        profile += "WHEN HaveNutStraightDraw RETURN true FORCE\n"
        profile += "WHEN HaveFlushDraw AND Overcards >= 1 RETURN true FORCE\n"
        profile += "WHEN HaveOpenEndedStraightDraw RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        # Semi-Bluff Hands on Turn
        profile += "##f$TurnSemiBluffHands##\n"
        profile += "// Hands suitable for semi-bluffing on the turn\n"
        profile += "WHEN HaveFlushDraw OR HaveOpenEndedStraightDraw RETURN true FORCE\n"
        profile += "WHEN Overcards = 2 AND f$WetBoard RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        # Board texture helper functions
        profile += "##f$ScareCard##\n"
        profile += "// Detects scare cards that could make betting more effective\n"
        profile += "WHEN (TurnCard >= jack) AND (FlopCardPairedOnTurn OR PairOnTurn) RETURN true FORCE\n"
        profile += "WHEN FlushDrawPossible AND NOT FlushPossible RETURN true FORCE\n"
        profile += "WHEN f$StraightDrawPossible AND NOT StraightPossible RETURN true FORCE\n"
        profile += "WHEN TurnCardIsOvercardToBoard RETURN true FORCE\n"
        profile += "WHEN TurnCard <= 9 AND FlopCardPairedOnTurn RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        profile += "##f$DrawComplete##\n"
        profile += "// Detects draw completions on the turn\n"
        profile += "WHEN FlushPossible RETURN true FORCE\n"
        profile += "WHEN StraightPossible RETURN true FORCE\n"
        profile += "WHEN FlopCardPairedOnTurn RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"
        
        profile += "##f$StraightDrawPossible##\n"
        profile += "// Detects if a straight draw is possible\n"
        profile += "// For example, having 4 consecutive cards or two groups of 3 cards\n"
        profile += "WHEN nstraightfill == 1 RETURN true FORCE\n"
        profile += "WHEN HaveStraightDraw RETURN true FORCE\n"
        profile += "WHEN HaveOpenEndedStraightDraw RETURN true FORCE\n"
        profile += "WHEN HaveInsideStraightDraw RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"
        
        return profile
