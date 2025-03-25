class FlopProfileGenerator:
    def __init__(self):
        pass
        
    def get_handrank_threshold(self, percentage):
        """Convert a percentage into a handrank threshold value"""
        # HandRank goes from 1 to 169, where 1 is the best hand (AA)
        # Convert percentage to a hand rank value
        # 0% = only AA (rank 1)
        # 100% = all hands (rank 169)
        return round(1 + (percentage / 100) * 168)
    
    def generate_flop_profile(self, settings):
        """Generate the flop part of the OpenHoldem profile"""
        # Extract flop settings
        ip_cbet_freq = settings.get("ip_cbet_freq", 70)
        oop_cbet_freq = settings.get("oop_cbet_freq", 60)
        ip_cbet_size = settings.get("ip_cbet_size", "50")
        oop_cbet_size = settings.get("oop_cbet_size", "66")
        dry_board_adjust = settings.get("dry_board_adjust", 20) / 100.0  # Convert to decimal
        wet_board_adjust = settings.get("wet_board_adjust", -20) / 100.0  # Convert to decimal
        checkraise_defense = settings.get("checkraise_defense", 35)
        donk_response = settings.get("donk_response", "Call/Raise")
        value_aggression = settings.get("value_aggression", 80)
        draw_aggression = settings.get("draw_aggression", 60)
        semibluff_freq = settings.get("semibluff_freq", 65)
        multiway_cbet_freq = settings.get("multiway_cbet_freq", 40)
        multiway_value_range = settings.get("multiway_value_range", 25)
        
        # Global aggression
        aggression = settings.get("aggression", 50)
        aggressive_factor = aggression / 50  # 0-2 range where 1 is neutral
        
        # Calculate thresholds
        ip_cbet_threshold = self.get_handrank_threshold(ip_cbet_freq)
        oop_cbet_threshold = self.get_handrank_threshold(oop_cbet_freq)
        checkraise_defense_threshold = self.get_handrank_threshold(checkraise_defense)
        multiway_cbet_threshold = self.get_handrank_threshold(multiway_cbet_freq)
        value_hands_threshold = self.get_handrank_threshold(value_aggression)
        draw_hands_threshold = self.get_handrank_threshold(draw_aggression)
        semibluff_threshold = self.get_handrank_threshold(semibluff_freq)
        multiway_value_threshold = self.get_handrank_threshold(multiway_value_range)
        
        # Adjust thresholds based on global aggression
        ip_cbet_threshold = round(ip_cbet_threshold * (1.2 - 0.4 * aggressive_factor))
        oop_cbet_threshold = round(oop_cbet_threshold * (1.2 - 0.4 * aggressive_factor))
        
        # Generate the profile text
        profile = "//*****************************************************************************\n"
        profile += "//\n"
        profile += "// FLOP STRATEGY\n"
        profile += "//\n"
        profile += "// Generated with the following settings:\n"
        profile += f"// - IP C-Bet Frequency: {ip_cbet_freq}%\n"
        profile += f"// - OOP C-Bet Frequency: {oop_cbet_freq}%\n"
        profile += f"// - IP C-Bet Size: {ip_cbet_size}% of pot\n"
        profile += f"// - OOP C-Bet Size: {oop_cbet_size}% of pot\n"
        profile += f"// - Dry Board Adjustment: {settings.get('dry_board_adjust', 20)}%\n"
        profile += f"// - Wet Board Adjustment: {settings.get('wet_board_adjust', -20)}%\n"
        profile += f"// - Check-Raise Defense: {checkraise_defense}%\n"
        profile += f"// - Donk Bet Response Style: {donk_response}\n"
        profile += f"// - Value Hands Aggression: {value_aggression}%\n"
        profile += f"// - Draw Hands Aggression: {draw_aggression}%\n"
        profile += f"// - Semi-Bluff Frequency: {semibluff_freq}%\n"
        profile += f"// - Multiway C-Bet Frequency: {multiway_cbet_freq}%\n"
        profile += f"// - Multiway Value Range: {multiway_value_range}%\n"
        profile += "//\n"
        profile += "//*****************************************************************************\n\n"

        profile += "##f$flop##\n"
        profile += "// Main flop decision function\n"
        profile += "// Determines action based on scenario detection\n\n"

        profile += "// C-Bet scenarios\n"
        profile += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition RETURN f$FlopCbetIP FORCE\n"
        profile += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND NOT f$InPosition RETURN f$FlopCbetOOP FORCE\n\n"

        profile += "// Facing bet scenarios\n"
        profile += "WHEN f$FacingFlopCbet RETURN f$FacingFlopCbet FORCE\n"
        profile += "WHEN f$FacingDonkBet RETURN f$FacingDonkBet FORCE\n\n"

        profile += "// Facing check scenarios\n"
        profile += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition RETURN f$BetAfterCheckIP FORCE\n"
        profile += "WHEN BotsLastPreflopAction = Call AND BotsActionsOnThisRoundIncludingChecks = 0 AND Bets = 0 AND NOT f$InPosition RETURN f$DonkBet FORCE\n\n"

        profile += "// Check-raise response\n"
        profile += "WHEN f$FacingCheckRaiseToCbet RETURN f$FacingCheckRaiseToCbet FORCE\n"
        profile += "WHEN f$FacingRaiseToCbet RETURN f$FacingRaiseToCbet FORCE\n\n"

        profile += "// Default action\n"
        profile += "WHEN Others Check FORCE\n\n"

        # C-Bet In Position
        profile += "##f$FlopCbetIP##\n"
        profile += f"// C-Bet in position, default size: {ip_cbet_size}% of pot\n"
        profile += "// Adjust based on board texture and player count\n\n"
        
        profile += "// Multiway pot considerations\n"
        profile += f"WHEN nopponentsplaying > 2 AND handrank169 <= {multiway_value_threshold} RaiseBy {ip_cbet_size}% FORCE\n"
        profile += f"WHEN nopponentsplaying > 2 Check FORCE\n\n"
        
        profile += "// Value hands always c-bet\n"
        profile += f"WHEN f$FlopValueHands RaiseBy {ip_cbet_size}% FORCE\n\n"
        
        profile += "// Semi-bluffs on draw-heavy boards\n"
        profile += f"WHEN f$FlopDrawHands AND f$WetBoard AND handrank169 <= {draw_hands_threshold} RaiseBy {ip_cbet_size}% FORCE\n\n"
        
        profile += "// Board texture-based adjustments\n"
        profile += f"WHEN f$DryBoard AND handrank169 <= {ip_cbet_threshold * (1 + dry_board_adjust)} RaiseBy {ip_cbet_size}% FORCE\n"
        profile += f"WHEN f$WetBoard AND handrank169 <= {ip_cbet_threshold * (1 + wet_board_adjust)} RaiseBy {ip_cbet_size}% FORCE\n"
        profile += f"WHEN handrank169 <= {ip_cbet_threshold} RaiseBy {ip_cbet_size}% FORCE\n\n"
        
        profile += "WHEN Others Check FORCE\n\n"

        # C-Bet Out Of Position
        profile += "##f$FlopCbetOOP##\n"
        profile += f"// C-Bet out of position, default size: {oop_cbet_size}% of pot\n"
        profile += "// Generally more selective when OOP\n\n"
        
        profile += "// Multiway pot considerations - even tighter\n"
        profile += f"WHEN nopponentsplaying > 2 AND handrank169 <= {round(multiway_value_threshold * 0.8)} RaiseBy {oop_cbet_size}% FORCE\n"
        profile += f"WHEN nopponentsplaying > 2 Check FORCE\n\n"
        
        profile += "// Value hands always c-bet\n"
        profile += f"WHEN f$FlopValueHands RaiseBy {oop_cbet_size}% FORCE\n\n"
        
        profile += "// Semi-bluffs on draw-heavy boards\n"
        profile += f"WHEN f$FlopDrawHands AND f$WetBoard AND handrank169 <= {round(draw_hands_threshold * 0.9)} RaiseBy {oop_cbet_size}% FORCE\n\n"
        
        profile += "// Board texture-based adjustments - more conservative when OOP\n"
        profile += f"WHEN f$DryBoard AND handrank169 <= {oop_cbet_threshold * (1 + dry_board_adjust * 0.8)} RaiseBy {oop_cbet_size}% FORCE\n"
        profile += f"WHEN f$WetBoard AND handrank169 <= {oop_cbet_threshold * (1 + wet_board_adjust * 0.8)} RaiseBy {oop_cbet_size}% FORCE\n"
        profile += f"WHEN handrank169 <= {oop_cbet_threshold} RaiseBy {oop_cbet_size}% FORCE\n\n"
        
        profile += "WHEN Others Check FORCE\n\n"

        # Facing Flop C-Bet
        profile += "##f$FacingFlopCbet##\n"
        profile += "// Response when facing a c-bet on the flop\n\n"
        
        profile += "// Always continue with strong hands\n"
        profile += "WHEN f$FlopStrongHands RaisePot FORCE\n"
        profile += "WHEN f$FlopValueHands Call FORCE\n\n"
        
        profile += "// Continue with good draws\n"
        profile += f"WHEN f$FlopDrawHands AND handrank169 <= {draw_hands_threshold} Call FORCE\n\n"
        
        profile += "// Check-raise with strong draws in position\n"
        profile += f"WHEN f$InPosition AND f$FlopStrongDraws AND handrank169 <= {semibluff_threshold} RaisePot FORCE\n\n"
        
        profile += "// Default fold\n"
        profile += "WHEN Others Fold FORCE\n\n"

        # Facing Donk Bet
        profile += "##f$FacingDonkBet##\n"
        profile += "// Response when a non-preflop-raiser bets into the preflop raiser\n\n"
        
        profile += "// Aggressive response to donk bets with strong hands\n"
        profile += "WHEN f$FlopStrongHands RaisePot FORCE\n"
        profile += "WHEN f$FlopValueHands Call FORCE\n\n"
        
        # Different responses based on settings
        if donk_response == "Fold/Call":
            profile += "// Conservative approach to donk bets\n"
            profile += f"WHEN f$FlopDrawHands AND handrank169 <= {round(draw_hands_threshold * 0.8)} Call FORCE\n"
        elif donk_response == "Call/Raise":
            profile += "// Balanced approach to donk bets\n"
            profile += f"WHEN f$FlopDrawHands AND handrank169 <= {draw_hands_threshold} Call FORCE\n"
            profile += f"WHEN f$FlopStrongDraws AND handrank169 <= {semibluff_threshold} RaisePot FORCE\n"
        else:  # Aggressive
            profile += "// Aggressive approach to donk bets\n"
            profile += f"WHEN f$FlopDrawHands Call FORCE\n"
            profile += f"WHEN handrank169 <= {round(ip_cbet_threshold * 0.8)} RaisePot FORCE\n"
        
        profile += "\nWHEN Others Fold FORCE\n\n"

        # Facing Check-Raise to C-Bet
        profile += "##f$FacingCheckRaiseToCbet##\n"
        profile += "// Response when opponent check-raises our c-bet\n\n"
        
        profile += "// Continue with strong hands\n"
        profile += "WHEN f$FlopStrongHands RaisePot FORCE\n"
        profile += "WHEN f$FlopValueHands Call FORCE\n\n"
        
        profile += f"// Defense frequency against check-raises\n"
        profile += f"WHEN handrank169 <= {checkraise_defense_threshold} Call FORCE\n\n"
        
        profile += "// Default fold\n"
        profile += "WHEN Others Fold FORCE\n\n"

        # Facing Raise to C-Bet
        profile += "##f$FacingRaiseToCbet##\n"
        profile += "// Response when opponent raises our c-bet\n\n"
        
        profile += "// Continue with strong hands\n"
        profile += "WHEN f$FlopStrongHands RaisePot FORCE\n"
        profile += "WHEN f$FlopValueHands Call FORCE\n\n"
        
        profile += f"// Defense frequency against raises - slightly tighter than vs check-raises\n"
        profile += f"WHEN handrank169 <= {round(checkraise_defense_threshold * 0.9)} Call FORCE\n\n"
        
        profile += "// Default fold\n"
        profile += "WHEN Others Fold FORCE\n\n"

        # Donk Bet
        profile += "##f$DonkBet##\n"
        profile += "// Donk betting as non-preflop-raiser\n\n"
        
        profile += "// Only donk with very strong hands or draws\n"
        profile += "WHEN f$FlopStrongHands RaisePot FORCE\n"
        profile += f"WHEN f$FlopStrongDraws AND handrank169 <= {round(semibluff_threshold * 0.7)} RaiseBy 50% FORCE\n\n"
        
        profile += "// Default check\n"
        profile += "WHEN Others Check FORCE\n\n"

        # Betting after opponent checks in position
        profile += "##f$BetAfterCheckIP##\n"
        profile += "// Betting when checked to in position\n\n"
        
        profile += "// Always bet value hands\n"
        profile += "WHEN f$FlopValueHands RaiseBy 50% FORCE\n\n"
        
        profile += "// Bet draws on wet boards\n"
        profile += f"WHEN f$FlopDrawHands AND f$WetBoard AND handrank169 <= {draw_hands_threshold} RaiseBy 50% FORCE\n\n"
        
        profile += "// Opportunistic betting when checked to\n"
        profile += f"WHEN f$DryBoard AND handrank169 <= {ip_cbet_threshold} RaiseBy 50% FORCE\n"
        profile += f"WHEN handrank169 <= {round(ip_cbet_threshold * 0.8)} RaiseBy 50% FORCE\n\n"
        
        profile += "// Default check back\n"
        profile += "WHEN Others Check FORCE\n\n"

        # Hand category helper functions
        profile += "//*****************************************************************************\n"
        profile += "//\n"
        profile += "// HAND CATEGORY HELPER FUNCTIONS\n"
        profile += "//\n"
        profile += "//*****************************************************************************\n\n"

        # Value Hands
        profile += "##f$FlopValueHands##\n"
        profile += "// Hands worth value betting on the flop\n"
        profile += "WHEN HaveQuads RETURN true FORCE\n"
        profile += "WHEN HaveFullHouse RETURN true FORCE\n"
        profile += "WHEN HaveFlush RETURN true FORCE\n"
        profile += "WHEN HaveStraight RETURN true FORCE\n"
        profile += "WHEN HaveTrips RETURN true FORCE\n"
        profile += "WHEN HaveTwoPair RETURN true FORCE\n"
        profile += "WHEN HaveOverPair RETURN true FORCE\n"
        profile += "WHEN HaveTopPair AND f$HaveGoodKicker RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        # Strong Hands
        profile += "##f$FlopStrongHands##\n"
        profile += "// Very strong hands that should be played aggressively\n"
        profile += "WHEN HaveQuads RETURN true FORCE\n"
        profile += "WHEN HaveFullHouse RETURN true FORCE\n"
        profile += "WHEN HaveFlush RETURN true FORCE\n"
        profile += "WHEN HaveStraight RETURN true FORCE\n"
        profile += "WHEN HaveSet RETURN true FORCE\n"
        profile += "WHEN HaveTwoPair AND HaveTopPair RETURN true FORCE\n"
        profile += "WHEN HaveOverPair AND rankhiplayer >= queen RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        # Draw Hands
        profile += "##f$FlopDrawHands##\n"
        profile += "// Hands with significant drawing potential\n"
        profile += "WHEN HaveFlushDraw RETURN true FORCE\n"
        profile += "WHEN HaveStraightDraw RETURN true FORCE\n"
        profile += "WHEN HaveOpenEndedStraightDraw RETURN true FORCE\n"
        profile += "WHEN HaveInsideStraightDraw AND Overcards >= 1 RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        # Strong Draw Hands
        profile += "##f$FlopStrongDraws##\n"
        profile += "// Strong drawing hands worth semi-bluffing\n"
        profile += "WHEN HaveFlushDraw AND Overcards >= 1 RETURN true FORCE\n"
        profile += "WHEN HaveOpenEndedStraightDraw AND Overcards >= 1 RETURN true FORCE\n"
        profile += "WHEN HaveFlushDraw AND HaveStraightDraw RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        # Good kicker helper
        profile += "##f$HaveGoodKicker##\n"
        profile += "// Determines if we have a good kicker with our pair\n"
        profile += "WHEN HaveTopPair AND rankhiplayer >= queen RETURN true FORCE\n"
        profile += "WHEN HaveTopPair AND rankloplayer >= ten RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        # Board texture helper functions
        profile += "##f$DryBoard##\n"
        profile += "// A dry board has few draws and is disconnected\n"
        profile += "WHEN FlushPossible RETURN false FORCE\n"
        profile += "WHEN StraightPossible RETURN false FORCE\n"
        profile += "WHEN nsuitedcommon >= 2 RETURN false FORCE\n"
        profile += "WHEN (TopFlopCard - LowestFlopCard) <= 4 AND (TopFlopCard - LowestFlopCard) > 1 RETURN false FORCE\n"
        profile += "WHEN PairOnBoard RETURN false FORCE\n"
        profile += "WHEN Others RETURN true FORCE\n\n"

        profile += "##f$WetBoard##\n"
        profile += "// A wet board has many draws and connected cards\n"
        profile += "WHEN FlushPossible OR FlushDrawPossible RETURN true FORCE\n"
        profile += "WHEN StraightPossible RETURN true FORCE\n"
        profile += "WHEN OpenEndedStraightDrawPossibleOnFlop RETURN true FORCE\n"
        profile += "WHEN (TopFlopCard - LowestFlopCard) <= 4 AND (TopFlopCard - LowestFlopCard) > 1 RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"
        
        return profile
