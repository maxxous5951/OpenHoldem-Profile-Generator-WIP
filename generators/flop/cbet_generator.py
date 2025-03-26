"""
Générateur de stratégies de C-Bet au flop
Version améliorée avec intégration des classifications avancées de textures de board
"""
from generators.flop.base_generator import BaseFlopGenerator

class CBetGenerator(BaseFlopGenerator):
    """
    Classe pour générer les sections de code de C-Bet au flop
    Implémentation avancée avec stratégies adaptées aux textures de board
    """
    
    def generate_code(self, settings):
        """
        Génère la section C-Bet du profil flop
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code généré pour les stratégies de C-Bet
        """
        # Extraction des paramètres de base
        ip_cbet_freq = settings.get("ip_cbet_freq", 70)
        oop_cbet_freq = settings.get("oop_cbet_freq", 60)
        ip_cbet_size = settings.get("ip_cbet_size", "50")
        oop_cbet_size = settings.get("oop_cbet_size", "66")
        
        # Extraire paramètres d'ajustement pour chaque texture
        dry_board_adjust = settings.get("dry_board_adjust", 20) / 100.0
        wet_board_adjust = settings.get("wet_board_adjust", -20) / 100.0
        monotone_board_adjust = settings.get("monotone_board_adjust", -25) / 100.0
        paired_board_adjust = settings.get("paired_board_adjust", 15) / 100.0
        connected_board_adjust = settings.get("connected_board_adjust", -20) / 100.0
        high_card_board_adjust = settings.get("high_card_board_adjust", 10) / 100.0
        low_card_board_adjust = settings.get("low_card_board_adjust", -15) / 100.0
        dynamic_board_adjust = settings.get("dynamic_board_adjust", -30) / 100.0
        static_board_adjust = settings.get("static_board_adjust", 25) / 100.0
        
        # Ajustements multiway
        multiway_cbet_freq = settings.get("multiway_cbet_freq", 40)
        multiway_value_range = settings.get("multiway_value_range", 25)
        
        # Tailles spéciales
        small_cbet_size = settings.get("small_cbet_size", "33")
        large_cbet_size = settings.get("large_cbet_size", "75")
        overbet_cbet_size = settings.get("overbet_cbet_size", "125")
        
        # Paramètres d'agressivité et de polarisation
        aggression = settings.get("aggression", 50)
        polarization = settings.get("polarization", 50)  # Niveau de polarisation (0-100)
        aggressive_factor = aggression / 50  # 0-2 range where 1 is neutral
        polar_factor = polarization / 50  # 0-2 range where 1 is neutral
        
        # Calcul des seuils de base
        ip_cbet_threshold = self.get_handrank_threshold(ip_cbet_freq)
        oop_cbet_threshold = self.get_handrank_threshold(oop_cbet_freq)
        multiway_cbet_threshold = self.get_handrank_threshold(multiway_cbet_freq)
        multiway_value_threshold = self.get_handrank_threshold(multiway_value_range)
        
        # Génération du code
        code = "//*****************************************************************************\n"
        code += "//\n"
        code += "// C-BET FUNCTIONS\n"
        code += "//\n"
        code += "// Advanced C-Bet strategy with texture-specific adaptations\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"
        
        #
        # C-Bet En Position (IP)
        #
        code += "##f$FlopCbetIP##\n"
        code += f"// C-Bet in position, default size: {ip_cbet_size}% of pot\n"
        code += "// Advanced strategy with specific adapations for each board texture\n\n"
        
        # Considérations pour les pots multiway
        code += "// MULTIWAY POT CONSIDERATIONS (3+ PLAYERS)\n"
        code += f"WHEN nopponentsplaying > 2 AND f$GoodMultiwayBoard AND handrank169 <= {multiway_value_threshold} RaiseBy f$RecommendedCBetSizing% FORCE\n"
        code += f"WHEN nopponentsplaying > 2 AND f$RiskyMultiwayBoard AND handrank169 <= {round(multiway_value_threshold * 0.7)} RaiseBy f$RecommendedCBetSizing% FORCE\n"
        code += f"WHEN nopponentsplaying > 2 Check FORCE\n\n"
        
        # Value betting en IP
        code += "// VALUE BETTING HANDS\n"
        code += f"WHEN f$FlopValueHands RaiseBy f$RecommendedCBetSizing% FORCE\n\n"
        
        # Stratégie basée sur les textures spécifiques
        code += "// TEXTURE-SPECIFIC C-BET STRATEGIES (HEADS-UP)\n"
        
        # Board monotone
        code += "// Monotone board strategy (three same suit)\n"
        code += f"WHEN f$MonotoneBoard AND HaveFlush RaiseBy {large_cbet_size}% FORCE\n"
        code += f"WHEN f$MonotoneBoard AND HaveFlushDraw RaiseBy {ip_cbet_size}% FORCE\n" 
        code += f"WHEN f$MonotoneBoard AND handrank169 <= {round(ip_cbet_threshold * (1 + monotone_board_adjust))} RaiseBy {ip_cbet_size}% FORCE\n\n"
        
        # Board paired
        code += "// Paired board strategy (pair on board)\n"
        code += f"WHEN f$PairedBoard AND HaveFullHouse RaiseBy {large_cbet_size}% FORCE\n"
        code += f"WHEN f$PairedBoard AND HaveTrips RaiseBy {large_cbet_size}% FORCE\n"
        code += f"WHEN f$PairedBoard AND HaveOverPair RaiseBy {ip_cbet_size}% FORCE\n"
        code += f"WHEN f$PairedBoard AND handrank169 <= {round(ip_cbet_threshold * (1 + paired_board_adjust))} RaiseBy {ip_cbet_size}% FORCE\n\n"
        
        # Board connected
        code += "// Connected board strategy (three connected cards)\n"
        code += f"WHEN f$ConnectedBoard AND HaveStraight RaiseBy {large_cbet_size}% FORCE\n"
        code += f"WHEN f$ConnectedBoard AND (HaveSet OR HaveTwoPair) RaiseBy {large_cbet_size}% FORCE\n"
        code += f"WHEN f$ConnectedBoard AND HaveOpenEndedStraightDraw RaiseBy {ip_cbet_size}% FORCE\n"
        code += f"WHEN f$ConnectedBoard AND handrank169 <= {round(ip_cbet_threshold * (1 + connected_board_adjust))} RaiseBy {ip_cbet_size}% FORCE\n\n"
        
        # Board avec cartes hautes
        code += "// High card board strategy (A, K, Q on board)\n"
        code += f"WHEN f$HighCardBoard AND handrank169 <= {round(ip_cbet_threshold * (1 + high_card_board_adjust))} RaiseBy {ip_cbet_size}% FORCE\n"
        code += f"WHEN f$HighCardBoard AND f$RaiserFavorableBoard AND handrank169 <= {round(ip_cbet_threshold * 1.1)} RaiseBy {small_cbet_size}% FORCE\n\n"
        
        # Board avec cartes basses
        code += "// Low card board strategy (all cards 9 or lower)\n"
        code += f"WHEN f$LowCardBoard AND HaveOverPair RaiseBy {ip_cbet_size}% FORCE\n"
        code += f"WHEN f$LowCardBoard AND HaveTopPair AND f$HaveGoodKicker RaiseBy {ip_cbet_size}% FORCE\n"
        code += f"WHEN f$LowCardBoard AND handrank169 <= {round(ip_cbet_threshold * (1 + low_card_board_adjust))} RaiseBy {ip_cbet_size}% FORCE\n\n"
        
        # Board dynamique / statique
        code += "// Dynamic vs Static board strategies\n"
        code += f"WHEN f$DynamicBoard AND handrank169 <= {round(ip_cbet_threshold * (1 + dynamic_board_adjust))} RaiseBy {ip_cbet_size}% FORCE\n"
        code += f"WHEN f$StaticBoard AND handrank169 <= {round(ip_cbet_threshold * (1 + static_board_adjust))} RaiseBy {small_cbet_size}% FORCE\n\n"
        
        # Stratégies spécifiques d'exploitabilité 
        code += "// EXPLOITATIVE ADJUSTMENTS\n"
        code += f"WHEN f$FavorableCBetBoard AND handrank169 <= {round(ip_cbet_threshold * 1.1)} RaiseBy {small_cbet_size}% FORCE\n"
        code += f"WHEN f$UnfavorableCBetBoard AND handrank169 <= {round(ip_cbet_threshold * 0.7)} RaiseBy {ip_cbet_size}% FORCE\n\n"
        
        # Stratégies par défaut basées sur les catégories de base (pour compatibilité)
        code += "// FALLBACK TO BASIC TEXTURE CLASSIFICATIONS\n"
        code += f"WHEN f$DryBoard AND handrank169 <= {round(ip_cbet_threshold * (1 + dry_board_adjust))} RaiseBy {small_cbet_size}% FORCE\n"
        code += f"WHEN f$WetBoard AND handrank169 <= {round(ip_cbet_threshold * (1 + wet_board_adjust))} RaiseBy {ip_cbet_size}% FORCE\n"
        code += f"WHEN handrank169 <= {ip_cbet_threshold} RaiseBy {ip_cbet_size}% FORCE\n\n"
        
        # Action par défaut
        code += "// Default action\n"
        code += "WHEN Others Check FORCE\n\n"

        #
        # C-Bet Hors Position (OOP)
        #
        code += "##f$FlopCbetOOP##\n"
        code += f"// C-Bet out of position, default size: {oop_cbet_size}% of pot\n"
        code += "// Generally more selective strategy with position disadvantage\n\n"
        
        # Considérations pour les pots multiway
        code += "// MULTIWAY POT CONSIDERATIONS - TIGHTER RANGES\n"
        code += f"WHEN nopponentsplaying > 2 AND f$GoodMultiwayBoard AND handrank169 <= {round(multiway_value_threshold * 0.8)} RaiseBy f$RecommendedCBetSizing% FORCE\n"
        code += f"WHEN nopponentsplaying > 2 AND f$RiskyMultiwayBoard AND handrank169 <= {round(multiway_value_threshold * 0.5)} RaiseBy f$RecommendedCBetSizing% FORCE\n"
        code += f"WHEN nopponentsplaying > 2 Check FORCE\n\n"
        
        # Value betting en OOP
        code += "// VALUE BETTING HANDS\n"
        code += f"WHEN f$FlopValueHands RaiseBy f$RecommendedCBetSizing% FORCE\n\n"
        
        # Stratégie basée sur les textures spécifiques
        code += "// TEXTURE-SPECIFIC C-BET STRATEGIES (HEADS-UP)\n"
        
        # Board monotone
        code += "// Monotone board strategy (three same suit)\n"
        code += f"WHEN f$MonotoneBoard AND HaveFlush RaiseBy {large_cbet_size}% FORCE\n"
        code += f"WHEN f$MonotoneBoard AND HaveSet RaiseBy {large_cbet_size}% FORCE\n"
        code += f"WHEN f$MonotoneBoard AND handrank169 <= {round(oop_cbet_threshold * (1 + monotone_board_adjust * 0.7))} RaiseBy {oop_cbet_size}% FORCE\n\n"
        
        # Board paired
        code += "// Paired board strategy (pair on board)\n"
        code += f"WHEN f$PairedBoard AND HaveFullHouse RaiseBy {large_cbet_size}% FORCE\n"
        code += f"WHEN f$PairedBoard AND HaveTrips RaiseBy {large_cbet_size}% FORCE\n"
        code += f"WHEN f$PairedBoard AND handrank169 <= {round(oop_cbet_threshold * (1 + paired_board_adjust * 0.7))} RaiseBy {oop_cbet_size}% FORCE\n\n"
        
        # Board connected
        code += "// Connected board strategy (three connected cards)\n"
        code += f"WHEN f$ConnectedBoard AND HaveStraight RaiseBy {large_cbet_size}% FORCE\n"
        code += f"WHEN f$ConnectedBoard AND (HaveSet OR HaveTwoPair) RaiseBy {large_cbet_size}% FORCE\n"
        code += f"WHEN f$ConnectedBoard AND handrank169 <= {round(oop_cbet_threshold * (1 + connected_board_adjust * 0.7))} RaiseBy {oop_cbet_size}% FORCE\n\n"
        
        # Board avec cartes hautes
        code += "// High card board strategy (A, K, Q on board)\n"
        code += f"WHEN f$HighCardBoard AND handrank169 <= {round(oop_cbet_threshold * (1 + high_card_board_adjust * 0.8))} RaiseBy {oop_cbet_size}% FORCE\n\n"
        
        # Board dynamique / statique
        code += "// Dynamic vs Static board strategies\n"
        code += f"WHEN f$DynamicBoard AND handrank169 <= {round(oop_cbet_threshold * (1 + dynamic_board_adjust * 0.7))} RaiseBy {oop_cbet_size}% FORCE\n"
        code += f"WHEN f$StaticBoard AND handrank169 <= {round(oop_cbet_threshold * (1 + static_board_adjust * 0.7))} RaiseBy {small_cbet_size}% FORCE\n\n"
        
        # Stratégies spécifiques d'exploitabilité 
        code += "// EXPLOITATIVE ADJUSTMENTS\n"
        code += f"WHEN f$FavorableCBetBoard AND handrank169 <= {round(oop_cbet_threshold * 0.9)} RaiseBy {oop_cbet_size}% FORCE\n"
        code += f"WHEN f$UnfavorableCBetBoard AND handrank169 <= {round(oop_cbet_threshold * 0.6)} RaiseBy {oop_cbet_size}% FORCE\n\n"
        
        # Stratégies par défaut basées sur les catégories de base (pour compatibilité)
        code += "// FALLBACK TO BASIC TEXTURE CLASSIFICATIONS\n"
        code += f"WHEN f$DryBoard AND handrank169 <= {round(oop_cbet_threshold * (1 + dry_board_adjust * 0.8))} RaiseBy {oop_cbet_size}% FORCE\n"
        code += f"WHEN f$WetBoard AND handrank169 <= {round(oop_cbet_threshold * (1 + wet_board_adjust * 0.8))} RaiseBy {oop_cbet_size}% FORCE\n"
        code += f"WHEN handrank169 <= {oop_cbet_threshold} RaiseBy {oop_cbet_size}% FORCE\n\n"
        
        # Action par défaut
        code += "// Default action\n"
        code += "WHEN Others Check FORCE\n\n"
        
        #
        # C-Bet Sizes Variables
        #
        code += "//*****************************************************************************\n"
        code += "//\n"
        code += "// C-BET SIZING HELPER FUNCTIONS\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"
        
        # C-Bet sizing basé sur la polarisation
        code += "##f$PolarizedCBetSize##\n"
        code += "// Determines polarized C-bet sizing based on hand strength\n"
        code += "// Strong hands and bluffs get larger sizing, medium hands get smaller sizing\n"
        code += f"WHEN f$FlopStrongHands OR handrank169 >= {round(ip_cbet_threshold * 1.5)} RETURN {large_cbet_size} FORCE\n"
        code += f"WHEN handrank169 <= {round(ip_cbet_threshold * 0.5)} RETURN {large_cbet_size} FORCE\n"
        code += f"WHEN Others RETURN {small_cbet_size} FORCE\n\n"
        
        # C-Bet sizing basé sur la texture
        code += "##f$TextureBasedCBetSize##\n"
        code += "// Recommends C-bet sizing based on board texture\n"
        code += f"WHEN f$MonotoneBoard RETURN {large_cbet_size} FORCE\n"
        code += f"WHEN f$PairedBoard RETURN {ip_cbet_size} FORCE\n"
        code += f"WHEN f$ConnectedBoard RETURN {large_cbet_size} FORCE\n"
        code += f"WHEN f$DynamicBoard RETURN {ip_cbet_size} FORCE\n"
        code += f"WHEN f$StaticBoard AND f$HighCardBoard RETURN {small_cbet_size} FORCE\n"
        code += f"WHEN f$StaticBoard RETURN {small_cbet_size} FORCE\n"
        code += f"WHEN f$LowCardBoard RETURN {ip_cbet_size} FORCE\n"
        code += f"WHEN Others RETURN {ip_cbet_size} FORCE\n\n"
        
        #
        # Stratégies Avancées Multiway
        #
        code += "//*****************************************************************************\n"
        code += "//\n"
        code += "// ADVANCED MULTIWAY C-BET STRATEGIES\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"
        
        # C-Bet en pots multiway en IP
        code += "##f$MultiwayCBetIP##\n"
        code += "// C-bet strategy for multiway pots when in position\n"
        code += f"// More selective approach adjusting for 3+ players in the pot\n\n"
        
        code += "// Very strong hands always c-bet\n"
        code += f"WHEN f$FlopStrongHands RaiseBy {large_cbet_size}% FORCE\n\n"
        
        code += "// Texture-specific multiway strategy\n"
        code += f"WHEN f$GoodMultiwayBoard AND handrank169 <= {multiway_value_threshold} RaiseBy {ip_cbet_size}% FORCE\n"
        code += f"WHEN f$PairedBoard AND handrank169 <= {round(multiway_value_threshold * 1.1)} RaiseBy {ip_cbet_size}% FORCE\n"
        code += f"WHEN f$HighCardBoard AND f$StaticBoard AND handrank169 <= {round(multiway_value_threshold * 1.2)} RaiseBy {small_cbet_size}% FORCE\n\n"
        
        code += "// Avoid c-betting on dangerous boards\n"
        code += f"WHEN f$RiskyMultiwayBoard AND NOT f$FlopValueHands Check FORCE\n\n"
        
        code += "// Default action\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # C-Bet en pots multiway en OOP
        code += "##f$MultiwayCBetOOP##\n"
        code += "// C-bet strategy for multiway pots when out of position\n"
        code += f"// Very selective approach adjusting for 3+ players with position disadvantage\n\n"
        
        code += "// Only c-bet with very strong hands\n"
        code += f"WHEN f$FlopStrongHands RaiseBy {large_cbet_size}% FORCE\n\n"
        
        code += "// Texture-specific strategy - only c-bet on favorable boards\n"
        code += f"WHEN f$GoodMultiwayBoard AND handrank169 <= {round(multiway_value_threshold * 0.7)} RaiseBy {oop_cbet_size}% FORCE\n"
        code += f"WHEN f$HighCardBoard AND f$StaticBoard AND handrank169 <= {round(multiway_value_threshold * 0.8)} RaiseBy {small_cbet_size}% FORCE\n\n"
        
        code += "// Default action\n"
        code += "WHEN Others Check FORCE\n\n"
        
        #
        # Delayed C-Bet (après avoir check au flop)
        # 
        code += "//*****************************************************************************\n"
        code += "//\n"
        code += "// DELAYED C-BET STRATEGIES\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"
        
        # Delayed C-Bet en IP
        code += "##f$DelayedCBetIP##\n"
        code += "// Delayed c-bet strategy on turn after checking flop when in position\n"
        code += f"// Used typically after trap-checking strong hands or giving up on weak boards\n\n"
        
        code += "// Always bet with strong hands after trap-checking\n"
        code += f"WHEN f$FlopStrongHands RaiseBy {large_cbet_size}% FORCE\n"
        code += f"WHEN f$FlopValueHands RaiseBy {ip_cbet_size}% FORCE\n\n"
        
        code += "// Texture-based delayed c-bet\n"
        code += f"WHEN f$StaticBoard AND handrank169 <= {round(ip_cbet_threshold * 0.8)} RaiseBy {ip_cbet_size}% FORCE\n"
        code += f"WHEN f$DynamicBoard AND f$FlopDrawHands RaiseBy {ip_cbet_size}% FORCE\n\n"
        
        code += "// Attack perceived weakness after flop check-check\n"
        code += f"WHEN f$FavorableCBetBoard AND handrank169 <= {round(ip_cbet_threshold * 0.7)} RaiseBy {ip_cbet_size}% FORCE\n\n"
        
        code += "// Default action\n"
        code += "WHEN Others Check FORCE\n\n"
        
        # Delayed C-Bet en OOP
        code += "##f$DelayedCBetOOP##\n"
        code += "// Delayed c-bet strategy on turn after checking flop when out of position\n"
        code += f"// Used typically as a probe bet or after opponent shows weakness\n\n"
        
        code += "// Only lead with strong hands\n"
        code += f"WHEN f$FlopStrongHands RaiseBy {large_cbet_size}% FORCE\n"
        code += f"WHEN f$FlopValueHands RaiseBy {oop_cbet_size}% FORCE\n\n"
        
        code += "// Limited bluffing with draws\n"
        code += f"WHEN f$FlopStrongDraws AND handrank169 <= {round(oop_cbet_threshold * 0.6)} RaiseBy {oop_cbet_size}% FORCE\n\n"
        
        code += "// Default action\n"
        code += "WHEN Others Check FORCE\n\n"
        
        #
        # Probe Betting au flop (en tant que caller preflop)
        #
        code += "//*****************************************************************************\n"
        code += "//\n"
        code += "// PROBE BETTING STRATEGIES\n"
        code += "//\n"
        code += "//*****************************************************************************\n\n"
        
        # Probe bet OOP
        code += "##f$ProbeOOP##\n"
        code += "// Probe betting strategy as preflop caller when out of position\n"
        code += f"// Used when villain has position but checked back preflop as BTN, CO, etc.\n\n"
        
        code += "// Only lead on favorable boards\n"
        code += f"WHEN f$GoodDonkBetBoard AND f$FlopValueHands RaiseBy {oop_cbet_size}% FORCE\n"
        code += f"WHEN f$GoodDonkBetBoard AND handrank169 <= {round(oop_cbet_threshold * 0.5)} RaiseBy {oop_cbet_size}% FORCE\n\n"
        
        code += "// Default action\n"
        code += "WHEN Others Check FORCE\n\n"
        
        return code