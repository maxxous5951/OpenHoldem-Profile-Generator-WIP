"""
Module de profils de joueurs prédéfinis pour OpenHoldem Profile Generator
"""

# Définition des profils de joueurs communs
# Chaque profil contient tous les paramètres nécessaires pour le générateur preflop

class PlayerProfiles:
    """
    Classe contenant les profils de joueurs prédéfinis pour
    différents styles de jeu
    """
    
    @staticmethod
    def get_profile(profile_name):
        """
        Renvoie un profil de joueur prédéfini en fonction du nom
        
        Args:
            profile_name (str): Nom du profil (TAG, LAG, Nit, etc.)
            
        Returns:
            dict: Dictionnaire de paramètres pour le profil sélectionné
        """
        profiles = {
            "TAG": PlayerProfiles.tag_profile(),
            "LAG": PlayerProfiles.lag_profile(),
            "Nit": PlayerProfiles.nit_profile(),
            "Fish": PlayerProfiles.fish_profile(),
            "Loose Passive": PlayerProfiles.loose_passive_profile(),
            "Tournament": PlayerProfiles.tournament_profile(),
            "Cash Game": PlayerProfiles.cash_game_profile(),
            "SNG": PlayerProfiles.sng_profile(),
            "MTT": PlayerProfiles.mtt_profile(),
        }
        
        return profiles.get(profile_name, PlayerProfiles.tag_profile())
    
    @staticmethod
    def tag_profile():
        """
        Tight-Aggressive - Style de jeu solide avec des ranges serrées
        et une approche agressive post-flop
        """
        return {
            # Paramètres généraux preflop
            "aggression": 65,      # Plus agressif que la moyenne
            "tightness": 70,       # Assez serré
            "limp_frequency": 15,  # Limpe rarement
            "threebet_frequency": 50,  # Utilise le 3-bet de manière équilibrée
            "fourbet_frequency": 40,  # 4-bet avec une range solide
            "squeeze_frequency": 45,  # Squeeze opportuniste
            "open_raise_size": "2.5",  # Taille standard
            
            # Ranges preflop détaillées par position
            "ep1_range": 12,    # UTG - Très sélectif
            "ep2_range": 14,    # UTG+1
            "ep3_range": 16,    # UTG+2
            "mp1_range": 18,
            "mp2_range": 20,
            "mp3_range": 24,    # HJ
            "co_range": 30,     # CO
            "btn_range": 40,    # BTN
            "sb_range": 26,     # SB
            "bb_range": 32,     # BB
            
            # Sizing preflop par position
            "ep1_sizing": "3.0",  # UTG
            "ep2_sizing": "3.0",  # UTG+1
            "ep3_sizing": "3.0",  # UTG+2
            "mp1_sizing": "2.5",
            "mp2_sizing": "2.5",
            "mp3_sizing": "2.5",  # HJ
            "co_sizing": "2.5",   # CO
            "btn_sizing": "2.5",  # BTN
            "sb_sizing": "3.0",   # SB
            
            # Autres paramètres preflop
            "call_3bet_range": 20,
            "fourbet_range": 12,
            "ip_3bet_adjust": 25,
            "vs_lp_3bet_adjust": 20,
            "call_4bet_range": 7,
            "fivebet_range": 4,
            "short_stack_4bet": 35,
            "squeeze_1caller": 15,
            "squeeze_multi": 10,
            "squeeze_sizing": "3.0",
            "blinds_squeeze": 20,
            "btn_squeeze": 25,
        }
    
    @staticmethod
    def lag_profile():
        """
        Loose-Aggressive - Style de jeu très agressif avec des ranges plus larges 
        et beaucoup de pression sur les adversaires
        """
        return {
            # Paramètres généraux preflop
            "aggression": 85,      # Très agressif
            "tightness": 40,       # Loose
            "limp_frequency": 5,   # Ne limpe presque jamais
            "threebet_frequency": 65,  # 3-bet beaucoup
            "fourbet_frequency": 55,  # 4-bet large
            "squeeze_frequency": 60,  # Squeeze très souvent
            "open_raise_size": "3.0",  # Taille plus grande
            
            # Ranges preflop détaillées par position
            "ep1_range": 18,    # UTG - Plus large que TAG
            "ep2_range": 20,    # UTG+1
            "ep3_range": 25,    # UTG+2
            "mp1_range": 30,
            "mp2_range": 35,
            "mp3_range": 40,    # HJ
            "co_range": 50,     # CO
            "btn_range": 65,    # BTN
            "sb_range": 45,     # SB
            "bb_range": 50,     # BB
            
            # Sizing preflop par position
            "ep1_sizing": "3.0",  # UTG
            "ep2_sizing": "3.0",  # UTG+1
            "ep3_sizing": "3.0",  # UTG+2
            "mp1_sizing": "3.0",
            "mp2_sizing": "3.0",
            "mp3_sizing": "2.5",  # HJ
            "co_sizing": "2.5",   # CO
            "btn_sizing": "2.5",  # BTN
            "sb_sizing": "3.5",   # SB
            
            # Autres paramètres preflop
            "call_3bet_range": 25,
            "fourbet_range": 20,
            "ip_3bet_adjust": 30,
            "vs_lp_3bet_adjust": 35,
            "call_4bet_range": 10,
            "fivebet_range": 6,
            "short_stack_4bet": 45,
            "squeeze_1caller": 25,
            "squeeze_multi": 18,
            "squeeze_sizing": "3.5",
            "blinds_squeeze": 35,
            "btn_squeeze": 40,
        }
    
    @staticmethod
    def nit_profile():
        """
        Nit - Style de jeu extrêmement serré, ne joue que les meilleures mains
        """
        return {
            # Paramètres généraux preflop
            "aggression": 45,      # Peu agressif
            "tightness": 90,       # Extrêmement serré
            "limp_frequency": 10,  # Limpe peu
            "threebet_frequency": 25,  # 3-bet uniquement avec les meilleures mains
            "fourbet_frequency": 15,  # 4-bet très premium
            "squeeze_frequency": 20,  # Squeeze rarement
            "open_raise_size": "2.5",  # Taille standard
            
            # Ranges preflop détaillées par position
            "ep1_range": 6,     # UTG - Ultra premium
            "ep2_range": 7,     # UTG+1
            "ep3_range": 8,     # UTG+2
            "mp1_range": 9,
            "mp2_range": 10,
            "mp3_range": 12,    # HJ
            "co_range": 15,     # CO
            "btn_range": 20,    # BTN
            "sb_range": 12,     # SB
            "bb_range": 15,     # BB
            
            # Sizing preflop par position
            "ep1_sizing": "3.0",  # UTG
            "ep2_sizing": "3.0",  # UTG+1
            "ep3_sizing": "3.0",  # UTG+2
            "mp1_sizing": "2.5",
            "mp2_sizing": "2.5",
            "mp3_sizing": "2.5",  # HJ
            "co_sizing": "2.5",   # CO
            "btn_sizing": "2.5",  # BTN
            "sb_sizing": "3.0",   # SB
            
            # Autres paramètres preflop
            "call_3bet_range": 8,
            "fourbet_range": 5,
            "ip_3bet_adjust": 10,
            "vs_lp_3bet_adjust": 15,
            "call_4bet_range": 2,
            "fivebet_range": 1,
            "short_stack_4bet": 15,
            "squeeze_1caller": 7,
            "squeeze_multi": 4,
            "squeeze_sizing": "3.0",
            "blinds_squeeze": 10,
            "btn_squeeze": 12,
        }
    
    @staticmethod
    def fish_profile():
        """
        Fish - Joueur débutant avec des ranges très larges et un jeu peu cohérent
        """
        return {
            # Paramètres généraux preflop
            "aggression": 35,      # Pas très agressif
            "tightness": 30,       # Très loose
            "limp_frequency": 70,  # Limpe beaucoup
            "threebet_frequency": 15,  # 3-bet rarement
            "fourbet_frequency": 10,  # 4-bet encore plus rarement
            "squeeze_frequency": 5,   # Presque jamais de squeeze
            "open_raise_size": "4.0",  # Taille trop grande
            
            # Ranges preflop détaillées par position
            "ep1_range": 35,    # UTG - Joue beaucoup trop de mains
            "ep2_range": 35,    # UTG+1
            "ep3_range": 35,    # UTG+2
            "mp1_range": 40,
            "mp2_range": 40,
            "mp3_range": 45,    # HJ
            "co_range": 50,     # CO
            "btn_range": 60,    # BTN
            "sb_range": 55,     # SB
            "bb_range": 60,     # BB
            
            # Sizing preflop par position
            "ep1_sizing": "4.0",  # UTG
            "ep2_sizing": "4.0",  # UTG+1
            "ep3_sizing": "4.0",  # UTG+2
            "mp1_sizing": "4.0",
            "mp2_sizing": "4.0",
            "mp3_sizing": "4.0",  # HJ
            "co_sizing": "3.5",   # CO
            "btn_sizing": "3.5",  # BTN
            "sb_sizing": "3.0",   # SB
            
            # Autres paramètres preflop
            "call_3bet_range": 40,
            "fourbet_range": 5,
            "ip_3bet_adjust": 5,
            "vs_lp_3bet_adjust": 5,
            "call_4bet_range": 4,
            "fivebet_range": 2,
            "short_stack_4bet": 5,
            "squeeze_1caller": 3,
            "squeeze_multi": 2,
            "squeeze_sizing": "4.0",
            "blinds_squeeze": 4,
            "btn_squeeze": 6,
        }
    
    @staticmethod
    def loose_passive_profile():
        """
        Loose-Passive - Joueur qui joue beaucoup de mains mais passivement
        """
        return {
            # Paramètres généraux preflop
            "aggression": 25,      # Pas agressif
            "tightness": 35,       # Loose
            "limp_frequency": 80,  # Limpe énormément
            "threebet_frequency": 10,  # 3-bet très peu
            "fourbet_frequency": 5,   # 4-bet presque jamais
            "squeeze_frequency": 8,   # Squeeze très rarement
            "open_raise_size": "2.0",  # Taille minimale
            
            # Ranges preflop détaillées par position
            "ep1_range": 25,    # UTG - Large
            "ep2_range": 28,    # UTG+1
            "ep3_range": 30,    # UTG+2
            "mp1_range": 35,
            "mp2_range": 40,
            "mp3_range": 45,    # HJ
            "co_range": 50,     # CO
            "btn_range": 60,    # BTN
            "sb_range": 55,     # SB
            "bb_range": 65,     # BB
            
            # Sizing preflop par position
            "ep1_sizing": "2.0",  # UTG
            "ep2_sizing": "2.0",  # UTG+1
            "ep3_sizing": "2.0",  # UTG+2
            "mp1_sizing": "2.0",
            "mp2_sizing": "2.0",
            "mp3_sizing": "2.0",  # HJ
            "co_sizing": "2.0",   # CO
            "btn_sizing": "2.0",  # BTN
            "sb_sizing": "2.5",   # SB
            
            # Autres paramètres preflop
            "call_3bet_range": 45,
            "fourbet_range": 3,
            "ip_3bet_adjust": 3,
            "vs_lp_3bet_adjust": 3,
            "call_4bet_range": 2,
            "fivebet_range": 1,
            "short_stack_4bet": 2,
            "squeeze_1caller": 5,
            "squeeze_multi": 2,
            "squeeze_sizing": "2.5",
            "blinds_squeeze": 4,
            "btn_squeeze": 6,
        }
    
    @staticmethod
    def tournament_profile():
        """
        Tournament - Profil général adapté aux tournois, équilibré mais agressif
        """
        return {
            # Paramètres généraux preflop
            "aggression": 70,      # Assez agressif
            "tightness": 60,       # Modérément serré
            "limp_frequency": 10,  # Limpe peu
            "threebet_frequency": 45,  # 3-bet équilibré
            "fourbet_frequency": 35,  # 4-bet sélectif
            "squeeze_frequency": 40,  # Squeeze dans les bonnes situations
            "open_raise_size": "2.5",  # Taille standard
            
            # Ranges preflop détaillées par position
           "ep1_range": 10,    # UTG - Sélectif
           "ep2_range": 12,    # UTG+1
           "ep3_range": 15,    # UTG+2
           "mp1_range": 18,
           "mp2_range": 22,
           "mp3_range": 26,    # HJ
           "co_range": 32,     # CO
           "btn_range": 45,    # BTN
           "sb_range": 30,     # SB
           "bb_range": 35,     # BB
           
           # Sizing preflop par position
           "ep1_sizing": "2.5",  # UTG
           "ep2_sizing": "2.5",  # UTG+1
           "ep3_sizing": "2.5",  # UTG+2
           "mp1_sizing": "2.5",
           "mp2_sizing": "2.5",
           "mp3_sizing": "2.5",  # HJ
           "co_sizing": "2.5",   # CO
           "btn_sizing": "2.5",  # BTN
           "sb_sizing": "3.0",   # SB
           
           # Autres paramètres preflop
           "call_3bet_range": 18,
           "fourbet_range": 10,
           "ip_3bet_adjust": 20,
           "vs_lp_3bet_adjust": 25,
           "call_4bet_range": 6,
           "fivebet_range": 3,
           "short_stack_4bet": 40,
           "squeeze_1caller": 14,
           "squeeze_multi": 9,
           "squeeze_sizing": "3.0",
           "blinds_squeeze": 18,
           "btn_squeeze": 22,
       }
       
    @staticmethod
    def cash_game_profile():
        """
        Cash Game - Profil adapté aux parties d'argent, plus de patience et exploitation
        """
        return {
            # Paramètres généraux preflop
            "aggression": 60,      # Modérément agressif
            "tightness": 65,       # Assez serré
            "limp_frequency": 15,  # Limpe peu
            "threebet_frequency": 40,  # 3-bet sélectif
            "fourbet_frequency": 30,  # 4-bet value-oriented
            "squeeze_frequency": 35,  # Squeeze opportuniste
            "open_raise_size": "3.0",  # Taille standard pour cash game
            
            # Ranges preflop détaillées par position
            "ep1_range": 12,    # UTG - Serré
            "ep2_range": 14,    # UTG+1
            "ep3_range": 16,    # UTG+2
            "mp1_range": 20,
            "mp2_range": 24,
            "mp3_range": 28,    # HJ
            "co_range": 35,     # CO
            "btn_range": 45,    # BTN
            "sb_range": 32,     # SB
            "bb_range": 35,     # BB
            
            # Sizing preflop par position
            "ep1_sizing": "3.0",  # UTG
            "ep2_sizing": "3.0",  # UTG+1
            "ep3_sizing": "3.0",  # UTG+2
            "mp1_sizing": "3.0",
            "mp2_sizing": "3.0",
            "mp3_sizing": "2.5",  # HJ
            "co_sizing": "2.5",   # CO
            "btn_sizing": "2.5",  # BTN
            "sb_sizing": "3.0",   # SB
            
            # Autres paramètres preflop
            "call_3bet_range": 16,
            "fourbet_range": 12,
            "ip_3bet_adjust": 22,
            "vs_lp_3bet_adjust": 18,
            "call_4bet_range": 7,
            "fivebet_range": 3,
            "short_stack_4bet": 30,
            "squeeze_1caller": 15,
            "squeeze_multi": 10,
            "squeeze_sizing": "3.0",
            "blinds_squeeze": 18,
            "btn_squeeze": 25,
        }
        
    @staticmethod
    def sng_profile():
        """
        SNG - Profil pour Sit & Go, adapté aux structures de blind rapides
        """
        return {
            # Paramètres généraux preflop
            "aggression": 75,      # Très agressif
            "tightness": 55,       # Modérément serré
            "limp_frequency": 5,   # Presque jamais de limp
            "threebet_frequency": 50,  # 3-bet fréquent
            "fourbet_frequency": 40,  # 4-bet agressif
            "squeeze_frequency": 45,  # Squeeze fréquent
            "open_raise_size": "2.5",  # Taille standard
            
            # Ranges preflop détaillées par position
            "ep1_range": 14,    # UTG - Un peu plus large que tournoi
            "ep2_range": 16,    # UTG+1
            "ep3_range": 18,    # UTG+2
            "mp1_range": 22,
            "mp2_range": 26,
            "mp3_range": 30,    # HJ
            "co_range": 38,     # CO
            "btn_range": 50,    # BTN
            "sb_range": 35,     # SB
            "bb_range": 40,     # BB
            
            # Sizing preflop par position
            "ep1_sizing": "2.5",  # UTG
            "ep2_sizing": "2.5",  # UTG+1
            "ep3_sizing": "2.5",  # UTG+2
            "mp1_sizing": "2.5",
            "mp2_sizing": "2.5",
            "mp3_sizing": "2.5",  # HJ
            "co_sizing": "2.5",   # CO
            "btn_sizing": "2.5",  # BTN
            "sb_sizing": "3.0",   # SB
            
            # Autres paramètres preflop
            "call_3bet_range": 15,
            "fourbet_range": 12,
            "ip_3bet_adjust": 20,
            "vs_lp_3bet_adjust": 25,
            "call_4bet_range": 6,
            "fivebet_range": 3,
            "short_stack_4bet": 45,
            "squeeze_1caller": 18,
            "squeeze_multi": 12,
            "squeeze_sizing": "3.0",
            "blinds_squeeze": 20,
            "btn_squeeze": 25,
        }
    
    @staticmethod
    def mtt_profile():
        """
        MTT - Profil pour tournois multi-tables, adaptable aux différentes phases
        """
        return {
            # Paramètres généraux preflop
            "aggression": 65,      # Assez agressif
            "tightness": 60,       # Modérément serré
            "limp_frequency": 8,   # Limite le limping
            "threebet_frequency": 45,  # 3-bet équilibré
            "fourbet_frequency": 35,  # 4-bet sélectif
            "squeeze_frequency": 40,  # Squeeze dans les bonnes situations
            "open_raise_size": "2.2",  # Taille un peu plus petite pour MTT
            
            # Ranges preflop détaillées par position
            "ep1_range": 11,    # UTG - Sélectif
            "ep2_range": 13,    # UTG+1
            "ep3_range": 15,    # UTG+2
            "mp1_range": 18,
            "mp2_range": 22,
            "mp3_range": 25,    # HJ
            "co_range": 32,     # CO
            "btn_range": 42,    # BTN
            "sb_range": 30,     # SB
            "bb_range": 35,     # BB
            
            # Sizing preflop par position
            "ep1_sizing": "2.2",  # UTG
            "ep2_sizing": "2.2",  # UTG+1
            "ep3_sizing": "2.2",  # UTG+2
            "mp1_sizing": "2.2",
            "mp2_sizing": "2.2",
            "mp3_sizing": "2.2",  # HJ
            "co_sizing": "2.2",   # CO
            "btn_sizing": "2.2",  # BTN
            "sb_sizing": "2.5",   # SB
            
            # Autres paramètres preflop
            "call_3bet_range": 18,
            "fourbet_range": 10,
            "ip_3bet_adjust": 20,
            "vs_lp_3bet_adjust": 20,
            "call_4bet_range": 5,
            "fivebet_range": 3,
            "short_stack_4bet": 40,
            "squeeze_1caller": 15,
            "squeeze_multi": 10,
            "squeeze_sizing": "2.7",
            "blinds_squeeze": 18,
            "btn_squeeze": 22,
        }