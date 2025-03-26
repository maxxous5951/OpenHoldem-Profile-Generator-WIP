"""
Fenêtre principale de l'application OpenHoldem Profile Generator
"""
from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout,
                           QWidget, QPushButton, QTextEdit, QScrollArea, 
                           QFileDialog, QMessageBox, QGroupBox, QComboBox, QLabel)
from PyQt6.QtCore import Qt

from generators.preflop import PreflopProfileGenerator
from generators.flop import FlopProfileGenerator
from generators.turn import TurnProfileGenerator
from generators.river import RiverProfileGenerator

from ui.config_tab import create_config_tab
from ui.preflop_tab import create_preflop_tab
from ui.flop_tab import create_flop_tab
from ui.turn_tab import create_turn_tab
from ui.river_tab import create_river_tab
from ui.push_fold_tab import create_push_fold_tab

class OpenHoldemProfileGenerator(QMainWindow):
    """
    Classe principale de l'application, gère la fenêtre principale et ses onglets
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenHoldem Profile Generator")
        self.setMinimumSize(1000, 800)
        
        # Configuration variables
        self.initialize_variables()
        
        # Initialiser le gestionnaire de profils
        from profile_manager import ProfileManager
        self.profile_manager = ProfileManager(self)
        self.current_profile = "Personnalisé"
        
        # Create the generators
        self.preflop_generator = PreflopProfileGenerator()
        self.flop_generator = FlopProfileGenerator()
        self.turn_generator = TurnProfileGenerator()
        self.river_generator = RiverProfileGenerator()
        
        # Setup the UI
        self.create_ui()
        
    def show_profile_selector(self):
        """Affiche le dialogue de sélection de profil"""
        from profile_selector import ProfileSelector
        selected_profile = ProfileSelector.get_profile(self)
        if selected_profile:
            self.update_profile(selected_profile)
    
    def update_profile(self, profile_info):
        """Met à jour l'interface avec le profil sélectionné"""
        # Créer le gestionnaire de profils s'il n'existe pas encore
        if not hasattr(self, 'profile_manager'):
            from profile_manager import ProfileManager
            self.profile_manager = ProfileManager(self)
        
        # Appliquer le profil
        self.profile_manager.apply_profile(profile_info)
        self.current_profile = profile_info.get("profile_name", "Personnalisé")
        
        # Mettre à jour le label
        if hasattr(self, "profile_label"):
            self.profile_label.setText(f"Profil actuel: {self.current_profile}")
                
    def initialize_variables(self):
        """Initialize all configuration variables with default values"""
        # Configuration variables
        self.num_players = 9
        self.game_type = "Cash Game"
        
        # Paramètres généraux preflop
        self.aggression = 50      # 0-100
        self.tightness = 50       # 0-100
        self.limp_frequency = 30  # 0-100
        self.threebet_frequency = 40  # 0-100
        self.fourbet_frequency = 30  # 0-100
        self.squeeze_frequency = 35  # 0-100
        self.open_raise_size = "2.5"  # BB
        
        # Ranges preflop détaillées par position
        self.ep1_range = 10    # UTG
        self.ep2_range = 12    # UTG+1
        self.ep3_range = 14    # UTG+2
        self.mp1_range = 16
        self.mp2_range = 18
        self.mp3_range = 20    # HJ
        self.co_range = 25     # CO
        self.btn_range = 30    # BTN
        self.sb_range = 35     # SB
        self.bb_range = 40     # BB
        
        # Sizing preflop par position
        self.ep1_sizing = "3.0"  # UTG
        self.ep2_sizing = "3.0"  # UTG+1
        self.ep3_sizing = "3.0"  # UTG+2
        self.mp1_sizing = "2.5"
        self.mp2_sizing = "2.5"
        self.mp3_sizing = "2.5"  # HJ
        self.co_sizing = "2.5"   # CO
        self.btn_sizing = "2.5"  # BTN
        self.sb_sizing = "2.5"   # SB
        
        # Autres paramètres preflop
        self.call_3bet_range = 15
        self.fourbet_range = 8
        self.ip_3bet_adjust = 20
        self.vs_lp_3bet_adjust = 15
        self.call_4bet_range = 5
        self.fivebet_range = 3
        self.short_stack_4bet = 30
        self.squeeze_1caller = 12
        self.squeeze_multi = 8
        self.squeeze_sizing = "3.0"
        self.blinds_squeeze = 25
        self.btn_squeeze = 20
        
        # Flop variables
        self.ip_cbet_freq = 70
        self.oop_cbet_freq = 60
        self.ip_cbet_size = "50"
        self.oop_cbet_size = "66"
        self.dry_board_adjust = 20
        self.wet_board_adjust = -20
        self.checkraise_defense = 35
        self.donk_response = "Call/Raise"
        self.value_aggression = 80
        self.draw_aggression = 60
        self.semibluff_freq = 65
        self.multiway_cbet_freq = 40
        self.multiway_value_range = 25
        
        # Texture de board avancées
        self.monotone_board_adjust = -25
        self.paired_board_adjust = 15
        self.connected_board_adjust = -20
        self.high_card_board_adjust = 10
        self.low_card_board_adjust = -15
        self.dynamic_board_adjust = -30
        self.static_board_adjust = 25
        self.small_cbet_size = "33"
        self.large_cbet_size = "75"
        self.overbet_cbet_size = "125"
        self.polarization = 50
        
        # Turn variables
        self.second_barrel_freq = 60
        self.delayed_cbet_freq = 40
        self.ip_turn_bet_size = "66"
        self.oop_turn_bet_size = "75"
        self.turn_checkraise_freq = 25
        self.turn_float_freq = 30
        self.turn_probe_freq = 35
        self.turn_fold_to_cbet_freq = 60
        self.turn_bluff_raise_freq = 20
        self.scare_card_adjust = -15
        self.draw_complete_adjust = 10
        
        # River variables
        self.third_barrel_freq = 40
        self.delayed_second_barrel_freq = 30
        self.ip_river_bet_size = "75"
        self.oop_river_bet_size = "75"
        self.river_checkraise_freq = 15
        self.river_float_freq = 20
        self.river_probe_freq = 25
        self.river_fold_to_bet_freq = 70
        self.river_bluff_raise_freq = 10
        self.river_value_range = 60
        self.river_bluff_range = 15
        self.river_check_behind_range = 80
        
        # Push/Fold variables
        self.initialize_push_fold_variables()
        
    def initialize_push_fold_variables(self):
        """Initialize all Push/Fold variables with default values"""
        # 1BB stack ranges
        self.push_1bb_ep = 75
        self.push_1bb_mp = 80
        self.push_1bb_co = 85
        self.push_1bb_btn = 90
        self.push_1bb_sb = 92
        self.push_1bb_bb = 95
        self.call_1bb_vs_ep = 60
        self.call_1bb_vs_mp = 65
        self.call_1bb_vs_co = 70
        self.call_1bb_vs_btn = 75
        self.call_1bb_vs_sb = 80
        
        # 2BB-5BB stack ranges
        self.push_2bb_ep = 60
        self.push_2bb_mp = 65
        self.push_2bb_co = 70
        self.push_2bb_btn = 75
        self.push_2bb_sb = 80
        self.push_2bb_bb = 85
        
        self.push_3bb_ep = 45
        self.push_3bb_mp = 50
        self.push_3bb_co = 55
        self.push_3bb_btn = 60
        self.push_3bb_sb = 65
        self.push_3bb_bb = 70
        
        self.push_4bb_ep = 35
        self.push_4bb_mp = 40
        self.push_4bb_co = 45
        self.push_4bb_btn = 50
        self.push_4bb_sb = 55
        self.push_4bb_bb = 60
        
        self.push_5bb_ep = 28
        self.push_5bb_mp = 32
        self.push_5bb_co = 36
        self.push_5bb_btn = 40
        self.push_5bb_sb = 45
        self.push_5bb_bb = 50
        
        # 6BB-10BB stack ranges
        self.push_6bb_ep = 22
        self.push_6bb_mp = 26
        self.push_6bb_co = 30
        self.push_6bb_btn = 35
        self.push_6bb_sb = 40
        self.push_6bb_bb = 45
        
        self.push_7bb_ep = 18
        self.push_7bb_mp = 22
        self.push_7bb_co = 26
        self.push_7bb_btn = 30
        self.push_7bb_sb = 35
        self.push_7bb_bb = 40
        
        self.push_8bb_ep = 15
        self.push_8bb_mp = 18
        self.push_8bb_co = 22
        self.push_8bb_btn = 26
        self.push_8bb_sb = 30
        self.push_8bb_bb = 35
        
        self.push_9bb_ep = 12
        self.push_9bb_mp = 15
        self.push_9bb_co = 18
        self.push_9bb_btn = 22
        self.push_9bb_sb = 26
        self.push_9bb_bb = 30
        
        self.push_10bb_ep = 10
        self.push_10bb_mp = 12
        self.push_10bb_co = 15
        self.push_10bb_btn = 18
        self.push_10bb_sb = 22
        self.push_10bb_bb = 25
        
        # 2BB-10BB call ranges
        self.call_2bb_vs_ep = 50
        self.call_2bb_vs_mp = 55
        self.call_2bb_vs_co = 60
        self.call_2bb_vs_btn = 65
        self.call_2bb_vs_sb = 70
        
        self.call_3bb_vs_ep = 40
        self.call_3bb_vs_mp = 45
        self.call_3bb_vs_co = 50
        self.call_3bb_vs_btn = 55
        self.call_3bb_vs_sb = 60
        
        self.call_4bb_vs_ep = 30
        self.call_4bb_vs_mp = 35
        self.call_4bb_vs_co = 40
        self.call_4bb_vs_btn = 45
        self.call_4bb_vs_sb = 50
        
        self.call_5bb_vs_ep = 25
        self.call_5bb_vs_mp = 28
        self.call_5bb_vs_co = 32
        self.call_5bb_vs_btn = 36
        self.call_5bb_vs_sb = 40
        
        self.call_6_10bb_vs_ep = 20
        self.call_6_10bb_vs_mp = 22
        self.call_6_10bb_vs_co = 25
        self.call_6_10bb_vs_btn = 28
        self.call_6_10bb_vs_sb = 32
        
        # 10BB+ stack ranges
        self.push_10_15bb_ep = 8
        self.push_10_15bb_mp = 10
        self.push_10_15bb_co = 12
        self.push_10_15bb_btn = 15
        self.push_10_15bb_sb = 18
        self.push_10_15bb_bb = 20
        
        self.push_15_20bb_ep = 5
        self.push_15_20bb_mp = 8
        self.push_15_20bb_co = 10
        self.push_15_20bb_btn = 12
        self.push_15_20bb_sb = 15
        self.push_15_20bb_bb = 18
        
        self.push_20_25bb_ep = 3
        self.push_20_25bb_mp = 5
        self.push_20_25bb_co = 7
        self.push_20_25bb_btn = 10
        self.push_20_25bb_sb = 12
        self.push_20_25bb_bb = 15
        
        # 10BB+ call ranges
        self.call_10_15bb_vs_ep = 15
        self.call_10_15bb_vs_mp = 18
        self.call_10_15bb_vs_co = 20
        self.call_10_15bb_vs_btn = 22
        self.call_10_15bb_vs_sb = 25
        
        self.call_15_25bb_vs_ep = 10
        self.call_15_25bb_vs_mp = 12
        self.call_15_25bb_vs_co = 15
        self.call_15_25bb_vs_btn = 18
        self.call_15_25bb_vs_sb = 20
        
    def create_ui(self):
        """Crée l'interface utilisateur principale"""
        # Create central widget with its layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)
        
        # Titre et informations
        title_widget = QWidget()
        title_layout = QHBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel("OpenHoldem Profile Generator")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_layout.addWidget(title_label)
        
        title_layout.addStretch(1)
        
        # Bouton pour accéder au sélecteur de profil
        select_profile_btn = QPushButton("Charger un profil")
        select_profile_btn.clicked.connect(self.show_profile_selector)
        title_layout.addWidget(select_profile_btn)
        
        main_layout.addWidget(title_widget)
        
        # Create a notebook (tabbed interface)
        notebook = QTabWidget()
        main_layout.addWidget(notebook)
        
        # Create main configuration tab
        config_tab = create_config_tab(self)
        notebook.addTab(config_tab, "Configuration")
        
        # Create other tabs for specific scenarios
        preflop_tab = create_preflop_tab(self)
        notebook.addTab(preflop_tab, "Preflop Settings")
        
        flop_tab = create_flop_tab(self)
        notebook.addTab(flop_tab, "Flop Settings")
        
        turn_tab = create_turn_tab(self)
        notebook.addTab(turn_tab, "Turn Settings")
        
        river_tab = create_river_tab(self)
        notebook.addTab(river_tab, "River Settings")
        
        push_fold_tab = create_push_fold_tab(self)
        notebook.addTab(push_fold_tab, "Push/Fold")
        
        # Hidden config values for internal use (they won't be shown in the UI)
        self.num_players_combo = QComboBox()
        self.num_players_combo.addItems([str(i) for i in range(2, 10)])
        self.num_players_combo.setCurrentIndex(7)  # Default to 9 players
        
        self.game_type_combo = QComboBox()
        self.game_type_combo.addItems(["Cash Game", "Tournament"])
        
        # Add status bar with current profile info
        self.statusBar().showMessage(f"Current profile: {self.current_profile}")
        
    def collect_preflop_settings(self):
        """Gather all preflop settings from the UI into a dictionary"""
        return {
            "num_players": int(self.num_players_combo.currentText()),
            "game_type": self.game_type_combo.currentText(),
            "aggression": self.aggression,
            "tightness": self.tightness,
            "limp_frequency": self.limp_frequency,
            "threebet_frequency": self.threebet_frequency,
            "fourbet_frequency": self.fourbet_frequency,
            "squeeze_frequency": self.squeeze_frequency,
            "open_raise_size": self.open_raise_size,
            
            # Ranges détaillées par position
            "ep1_range": self.ep1_range_slider.value(),
            "ep2_range": self.ep2_range_slider.value(),
            "ep3_range": self.ep3_range_slider.value(),
            "mp1_range": self.mp1_range_slider.value(),
            "mp2_range": self.mp2_range_slider.value(),
            "mp3_range": self.mp3_range_slider.value(),
            "co_range": self.co_range_slider.value(),
            "btn_range": self.btn_range_slider.value(),
            "sb_range": self.sb_range_slider.value(),
            "bb_range": self.bb_range_slider.value(),
            
            # Sizing par position
            "ep1_sizing": self.ep1_sizing_combo.currentText(),
            "ep2_sizing": self.ep2_sizing_combo.currentText(),
            "ep3_sizing": self.ep3_sizing_combo.currentText(),
            "mp1_sizing": self.mp1_sizing_combo.currentText(),
            "mp2_sizing": self.mp2_sizing_combo.currentText(),
            "mp3_sizing": self.mp3_sizing_combo.currentText(),
            "co_sizing": self.co_sizing_combo.currentText(),
            "btn_sizing": self.btn_sizing_combo.currentText(),
            "sb_sizing": self.sb_sizing_combo.currentText(),
            
            # Autres paramètres preflop
            "call_3bet_range": self.call_3bet_range_slider.value(),
            "fourbet_range": self.fourbet_range_slider.value(),
            "ip_3bet_adjust": self.ip_3bet_adjust_slider.value(),
            "vs_lp_3bet_adjust": self.vs_lp_3bet_adjust_slider.value(),
            "call_4bet_range": self.call_4bet_range_slider.value(),
            "fivebet_range": self.fivebet_range_slider.value(),
            "short_stack_4bet": self.short_stack_4bet_slider.value(),
            "squeeze_1caller": self.squeeze_1caller_slider.value(),
            "squeeze_multi": self.squeeze_multi_slider.value(),
            "squeeze_sizing": self.squeeze_sizing_combo.currentText(),
            "blinds_squeeze": self.blinds_squeeze_slider.value(),
            "btn_squeeze": self.btn_squeeze_slider.value(),
            
            # Ajouter toutes les variables push/fold
            "push_1bb_ep": self.push_1bb_ep,
            "push_1bb_mp": self.push_1bb_mp,
            "push_1bb_co": self.push_1bb_co,
            "push_1bb_btn": self.push_1bb_btn,
            "push_1bb_sb": self.push_1bb_sb,
            "push_1bb_bb": self.push_1bb_bb,
            "call_1bb_vs_ep": self.call_1bb_vs_ep,
            "call_1bb_vs_mp": self.call_1bb_vs_mp,
            "call_1bb_vs_co": self.call_1bb_vs_co,
            "call_1bb_vs_btn": self.call_1bb_vs_btn,
            "call_1bb_vs_sb": self.call_1bb_vs_sb,
            
            # 2BB-5BB stack ranges
            "push_2bb_ep": self.push_2bb_ep,
            "push_2bb_mp": self.push_2bb_mp,
            "push_2bb_co": self.push_2bb_co,
            "push_2bb_btn": self.push_2bb_btn,
            "push_2bb_sb": self.push_2bb_sb,
            "push_2bb_bb": self.push_2bb_bb,
            
            "push_3bb_ep": self.push_3bb_ep,
            "push_3bb_mp": self.push_3bb_mp,
            "push_3bb_co": self.push_3bb_co,
            "push_3bb_btn": self.push_3bb_btn,
            "push_3bb_sb": self.push_3bb_sb,
            "push_3bb_bb": self.push_3bb_bb,
            
            "push_4bb_ep": self.push_4bb_ep,
            "push_4bb_mp": self.push_4bb_mp,
            "push_4bb_co": self.push_4bb_co,
            "push_4bb_btn": self.push_4bb_btn,
            "push_4bb_sb": self.push_4bb_sb,
            "push_4bb_bb": self.push_4bb_bb,
            
            "push_5bb_ep": self.push_5bb_ep,
            "push_5bb_mp": self.push_5bb_mp,
            "push_5bb_co": self.push_5bb_co,
            "push_5bb_btn": self.push_5bb_btn,
            "push_5bb_sb": self.push_5bb_sb,
            "push_5bb_bb": self.push_5bb_bb,
            
            # 6BB-10BB stack ranges
            "push_6bb_ep": self.push_6bb_ep,
            "push_6bb_mp": self.push_6bb_mp,
            "push_6bb_co": self.push_6bb_co,
            "push_6bb_btn": self.push_6bb_btn,
            "push_6bb_sb": self.push_6bb_sb,
            "push_6bb_bb": self.push_6bb_bb,
            
            "push_7bb_ep": self.push_7bb_ep,
            "push_7bb_mp": self.push_7bb_mp,
            "push_7bb_co": self.push_7bb_co,
            "push_7bb_btn": self.push_7bb_btn,
            "push_7bb_sb": self.push_7bb_sb,
            "push_7bb_bb": self.push_7bb_bb,
            
            "push_8bb_ep": self.push_8bb_ep,
            "push_8bb_mp": self.push_8bb_mp,
            "push_8bb_co": self.push_8bb_co,
            "push_8bb_btn": self.push_8bb_btn,
            "push_8bb_sb": self.push_8bb_sb,
            "push_8bb_bb": self.push_8bb_bb,
            
            "push_9bb_ep": self.push_9bb_ep,
            "push_9bb_mp": self.push_9bb_mp,
            "push_9bb_co": self.push_9bb_co,
            "push_9bb_btn": self.push_9bb_btn,
            "push_9bb_sb": self.push_9bb_sb,
            "push_9bb_bb": self.push_9bb_bb,
            
            "push_10bb_ep": self.push_10bb_ep,
            "push_10bb_mp": self.push_10bb_mp,
            "push_10bb_co": self.push_10bb_co,
            "push_10bb_btn": self.push_10bb_btn,
            "push_10bb_sb": self.push_10bb_sb,
            "push_10bb_bb": self.push_10bb_bb,
            
            # Call ranges
            "call_2bb_vs_ep": self.call_2bb_vs_ep,
            "call_2bb_vs_mp": self.call_2bb_vs_mp,
            "call_2bb_vs_co": self.call_2bb_vs_co,
            "call_2bb_vs_btn": self.call_2bb_vs_btn,
            "call_2bb_vs_sb": self.call_2bb_vs_sb,
            
            "call_3bb_vs_ep": self.call_3bb_vs_ep,
            "call_3bb_vs_mp": self.call_3bb_vs_mp,
            "call_3bb_vs_co": self.call_3bb_vs_co,
            "call_3bb_vs_btn": self.call_3bb_vs_btn,
            "call_3bb_vs_sb": self.call_3bb_vs_sb,
            
            "call_4bb_vs_ep": self.call_4bb_vs_ep,
            "call_4bb_vs_mp": self.call_4bb_vs_mp,
            "call_4bb_vs_co": self.call_4bb_vs_co,
            "call_4bb_vs_btn": self.call_4bb_vs_btn,
            "call_4bb_vs_sb": self.call_4bb_vs_sb,
            
            "call_5bb_vs_ep": self.call_5bb_vs_ep,
            "call_5bb_vs_mp": self.call_5bb_vs_mp,
            "call_5bb_vs_co": self.call_5bb_vs_co,
            "call_5bb_vs_btn": self.call_5bb_vs_btn,
            "call_5bb_vs_sb": self.call_5bb_vs_sb,
            
            "call_6_10bb_vs_ep": self.call_6_10bb_vs_ep,
            "call_6_10bb_vs_mp": self.call_6_10bb_vs_mp,
            "call_6_10bb_vs_co": self.call_6_10bb_vs_co,
            "call_6_10bb_vs_btn": self.call_6_10bb_vs_btn,
            "call_6_10bb_vs_sb": self.call_6_10bb_vs_sb,
            
            # 10BB+ stack ranges
            "push_10_15bb_ep": self.push_10_15bb_ep,
            "push_10_15bb_mp": self.push_10_15bb_mp,
            "push_10_15bb_co": self.push_10_15bb_co,
            "push_10_15bb_btn": self.push_10_15bb_btn,
            "push_10_15bb_sb": self.push_10_15bb_sb,
            "push_10_15bb_bb": self.push_10_15bb_bb,
            
            "push_15_20bb_ep": self.push_15_20bb_ep,
            "push_15_20bb_mp": self.push_15_20bb_mp,
            "push_15_20bb_co": self.push_15_20bb_co,
            "push_15_20bb_btn": self.push_15_20bb_btn,
            "push_15_20bb_sb": self.push_15_20bb_sb,
            "push_15_20bb_bb": self.push_15_20bb_bb,
            
            "push_20_25bb_ep": self.push_20_25bb_ep,
            "push_20_25bb_mp": self.push_20_25bb_mp,
            "push_20_25bb_co": self.push_20_25bb_co,
            "push_20_25bb_btn": self.push_20_25bb_btn,
            "push_20_25bb_sb": self.push_20_25bb_sb,
            "push_20_25bb_bb": self.push_20_25bb_bb,
            
            "call_10_15bb_vs_ep": self.call_10_15bb_vs_ep,
            "call_10_15bb_vs_mp": self.call_10_15bb_vs_mp,
            "call_10_15bb_vs_co": self.call_10_15bb_vs_co,
            "call_10_15bb_vs_btn": self.call_10_15bb_vs_btn,
            "call_10_15bb_vs_sb": self.call_10_15bb_vs_sb,
            
            "call_15_25bb_vs_ep": self.call_15_25bb_vs_ep,
            "call_15_25bb_vs_mp": self.call_15_25bb_vs_mp,
            "call_15_25bb_vs_co": self.call_15_25bb_vs_co,
            "call_15_25bb_vs_btn": self.call_15_25bb_vs_btn,
            "call_15_25bb_vs_sb": self.call_15_25bb_vs_sb
        }
    
    def collect_flop_settings(self):
        """Gather all flop settings from the UI into a dictionary"""
        return {
            "ip_cbet_freq": self.ip_cbet_freq_slider.value(),
            "oop_cbet_freq": self.oop_cbet_freq_slider.value(),
            "ip_cbet_size": self.ip_cbet_size_combo.currentText(),
            "oop_cbet_size": self.oop_cbet_size_combo.currentText(),
            "dry_board_adjust": self.dry_board_adjust_slider.value(),
            "wet_board_adjust": self.wet_board_adjust_slider.value(),
            "checkraise_defense": self.checkraise_defense_slider.value(),
            "donk_response": self.donk_response_combo.currentText(),
            "value_aggression": self.value_aggression_slider.value(),
            "draw_aggression": self.draw_aggression_slider.value(),
            "semibluff_freq": self.semibluff_freq_slider.value(),
            "multiway_cbet_freq": self.multiway_cbet_freq_slider.value(),
            "multiway_value_range": self.multiway_value_range_slider.value(),
            "aggression": self.aggression,
            
            # Nouvelles textures de board avancées
            "monotone_board_adjust": self.monotone_board_adjust_slider.value(),
            "paired_board_adjust": self.paired_board_adjust_slider.value(),
            "connected_board_adjust": self.connected_board_adjust_slider.value(),
            "high_card_board_adjust": self.high_card_board_adjust_slider.value(),
            "low_card_board_adjust": self.low_card_board_adjust_slider.value(),
            "dynamic_board_adjust": self.dynamic_board_adjust_slider.value(),
            "static_board_adjust": self.static_board_adjust_slider.value(), 
            "small_cbet_size": self.small_cbet_size_combo.currentText(),
            "large_cbet_size": self.large_cbet_size_combo.currentText(),
            "overbet_cbet_size": self.overbet_cbet_size_combo.currentText(),
            "polarization": self.polarization_slider.value()
        }
    
    def collect_turn_settings(self):
        """Gather all turn settings from the UI into a dictionary"""
        return {
            "second_barrel_freq": self.second_barrel_freq_slider.value(),
            "delayed_cbet_freq": self.delayed_cbet_freq_slider.value(),
            "ip_turn_bet_size": self.ip_turn_bet_size_combo.currentText(),
            "oop_turn_bet_size": self.oop_turn_bet_size_combo.currentText(),
            "turn_checkraise_freq": self.turn_checkraise_freq_slider.value(),
            "turn_float_freq": self.turn_float_freq_slider.value(),
            "turn_probe_freq": self.turn_probe_freq_slider.value(),
            "turn_fold_to_cbet_freq": self.turn_fold_to_cbet_freq_slider.value(),
            "turn_bluff_raise_freq": self.turn_bluff_raise_freq_slider.value(),
            "scare_card_adjust": self.scare_card_adjust_slider.value(),
            "draw_complete_adjust": self.draw_complete_adjust_slider.value(),
            "aggression": self.aggression
        }
    
    def collect_river_settings(self):
        """Gather all river settings from the UI into a dictionary"""
        return {
            "third_barrel_freq": self.third_barrel_freq_slider.value(),
            "delayed_second_barrel_freq": self.delayed_second_barrel_freq_slider.value(),
            "ip_river_bet_size": self.ip_river_bet_size_combo.currentText(),
            "oop_river_bet_size": self.oop_river_bet_size_combo.currentText(),
            "river_checkraise_freq": self.river_checkraise_freq_slider.value(),
            "river_float_freq": self.river_float_freq_slider.value(),
            "river_probe_freq": self.river_probe_freq_slider.value(),
            "river_fold_to_bet_freq": self.river_fold_to_bet_freq_slider.value(),
            "river_bluff_raise_freq": self.river_bluff_raise_freq_slider.value(),
            "river_value_range": self.river_value_range_slider.value(),
            "river_bluff_range": self.river_bluff_range_slider.value(),
            "river_check_behind_range": self.river_check_behind_range_slider.value(),
            "aggression": self.aggression
        }
    
    def generate_profile(self):
        """Generate the OpenHoldem profile based on current settings"""
        # Get all settings from UI
        preflop_settings = self.collect_preflop_settings()
        flop_settings = self.collect_flop_settings()
        turn_settings = self.collect_turn_settings()
        river_settings = self.collect_river_settings()
        
        # Generate profile using the generators
        preflop_profile = self.preflop_generator.generate_preflop_profile(preflop_settings)
        flop_profile = self.flop_generator.generate_flop_profile(flop_settings)
        turn_profile = self.turn_generator.generate_turn_profile(turn_settings)
        river_profile = self.river_generator.generate_river_profile(river_settings)
        
        # Combine the profiles
        full_profile = preflop_profile + "\n\n" + flop_profile + "\n\n" + turn_profile + "\n\n" + river_profile
        
        # Display in preview
        self.preview_text.setText(full_profile)
        
        # Update status bar
        self.statusBar().showMessage("Profile generated successfully")
        
        QMessageBox.information(self, "Profile Generated", "OpenHoldem profile has been generated and is ready to save.")
        
    def save_profile(self):
        """Save the generated profile to a file"""
        if not self.preview_text.toPlainText().strip():
            QMessageBox.warning(self, "Empty Profile", "Please generate a profile first.")
            return
            
        # Ask for save location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Profile",
            "",
            "OpenHoldem Files (*.ohf);;Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.preview_text.toPlainText())
                QMessageBox.information(self, "Save Successful", f"Profile saved to {file_path}")
                self.statusBar().showMessage(f"Profile saved to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Could not save profile: {str(e)}")
                
    def export_settings(self):
        """Export current settings to a JSON file for future use"""
        import json
        
        # Collect all settings
        settings = {
            "preflop": self.collect_preflop_settings(),
            "flop": self.collect_flop_settings(),
            "turn": self.collect_turn_settings(),
            "river": self.collect_river_settings(),
        }
        
        # Ask for save location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Settings",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(settings, file, indent=4)
                QMessageBox.information(self, "Export Successful", f"Settings exported to {file_path}")
                self.statusBar().showMessage(f"Settings exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Could not export settings: {str(e)}")
                
    def import_settings(self):
        """Import settings from a JSON file"""
        import json
        
        # Ask for file to import
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Settings",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    settings = json.load(file)
                
                # Apply settings to UI
                self.apply_settings(settings)
                QMessageBox.information(self, "Import Successful", f"Settings imported from {file_path}")
                self.statusBar().showMessage(f"Settings imported from {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"Could not import settings: {str(e)}")
                
    def apply_settings(self, settings):
        """Apply imported settings to the UI components"""
        # This method would need to update all UI components based on the imported settings
        # For sliders, combo boxes, etc.
        
        # Example implementation for a few components:
        if "preflop" in settings:
            preflop = settings["preflop"]
            
            # Update range sliders if they exist
            for pos in ["ep1", "ep2", "ep3", "mp1", "mp2", "mp3", "co", "btn", "sb", "bb"]:
                slider_name = f"{pos}_range_slider"
                if hasattr(self, slider_name) and f"{pos}_range" in preflop:
                    slider = getattr(self, slider_name)
                    slider.setValue(preflop[f"{pos}_range"])
            
            # Update sizing combos
            for pos in ["ep1", "ep2", "ep3", "mp1", "mp2", "mp3", "co", "btn", "sb"]:
                combo_name = f"{pos}_sizing_combo"
                if hasattr(self, combo_name) and f"{pos}_sizing" in preflop:
                    combo = getattr(self, combo_name)
                    index = combo.findText(preflop[f"{pos}_sizing"])
                    if index >= 0:
                        combo.setCurrentIndex(index)
            
            # Update other preflop sliders
            slider_mappings = [
                ("call_3bet_range", "call_3bet_range_slider"),
                ("fourbet_range", "fourbet_range_slider"),
                ("ip_3bet_adjust", "ip_3bet_adjust_slider"),
                ("vs_lp_3bet_adjust", "vs_lp_3bet_adjust_slider"),
                ("call_4bet_range", "call_4bet_range_slider"),
                ("fivebet_range", "fivebet_range_slider"),
                ("short_stack_4bet", "short_stack_4bet_slider"),
                ("squeeze_1caller", "squeeze_1caller_slider"),
                ("squeeze_multi", "squeeze_multi_slider"),
                ("blinds_squeeze", "blinds_squeeze_slider"),
                ("btn_squeeze", "btn_squeeze_slider")
            ]
            
            for setting_name, slider_name in slider_mappings:
                if hasattr(self, slider_name) and setting_name in preflop:
                    slider = getattr(self, slider_name)
                    slider.setValue(preflop[setting_name])
        
        # Process flop settings
        if "flop" in settings:
            flop = settings["flop"]
            
            # Update flop sliders
            slider_mappings = [
                ("ip_cbet_freq", "ip_cbet_freq_slider"),
                ("oop_cbet_freq", "oop_cbet_freq_slider"),
                ("dry_board_adjust", "dry_board_adjust_slider"),
                ("wet_board_adjust", "wet_board_adjust_slider"),
                ("checkraise_defense", "checkraise_defense_slider"),
                ("value_aggression", "value_aggression_slider"),
                ("draw_aggression", "draw_aggression_slider"),
                ("semibluff_freq", "semibluff_freq_slider"),
                ("multiway_cbet_freq", "multiway_cbet_freq_slider"),
                ("multiway_value_range", "multiway_value_range_slider"),
                # Nouveaux sliders pour les textures avancées
                ("monotone_board_adjust", "monotone_board_adjust_slider"),
                ("paired_board_adjust", "paired_board_adjust_slider"),
                ("connected_board_adjust", "connected_board_adjust_slider"),
                ("high_card_board_adjust", "high_card_board_adjust_slider"),
                ("low_card_board_adjust", "low_card_board_adjust_slider"),
                ("dynamic_board_adjust", "dynamic_board_adjust_slider"),
                ("static_board_adjust", "static_board_adjust_slider"),
                ("polarization", "polarization_slider")
            ]
            
            for setting_name, slider_name in slider_mappings:
                if hasattr(self, slider_name) and setting_name in flop:
                    slider = getattr(self, slider_name)
                    slider.setValue(flop[setting_name])
            
            # Update flop combos
            combo_mappings = [
                ("ip_cbet_size", "ip_cbet_size_combo"),
                ("oop_cbet_size", "oop_cbet_size_combo"),
                ("donk_response", "donk_response_combo"),
                ("small_cbet_size", "small_cbet_size_combo"),
                ("large_cbet_size", "large_cbet_size_combo"),
                ("overbet_cbet_size", "overbet_cbet_size_combo")
            ]
            
            for setting_name, combo_name in combo_mappings:
                if hasattr(self, combo_name) and setting_name in flop:
                    combo = getattr(self, combo_name)
                    index = combo.findText(flop[setting_name])
                    if index >= 0:
                        combo.setCurrentIndex(index)
        
        # Process turn settings
        if "turn" in settings:
            turn = settings["turn"]
            
            # Update turn sliders
            slider_mappings = [
                ("second_barrel_freq", "second_barrel_freq_slider"),
                ("delayed_cbet_freq", "delayed_cbet_freq_slider"),
                ("turn_checkraise_freq", "turn_checkraise_freq_slider"),
                ("turn_float_freq", "turn_float_freq_slider"),
                ("turn_probe_freq", "turn_probe_freq_slider"),
                ("turn_fold_to_cbet_freq", "turn_fold_to_cbet_freq_slider"),
                ("turn_bluff_raise_freq", "turn_bluff_raise_freq_slider"),
                ("scare_card_adjust", "scare_card_adjust_slider"),
                ("draw_complete_adjust", "draw_complete_adjust_slider")
            ]
            
            for setting_name, slider_name in slider_mappings:
                if hasattr(self, slider_name) and setting_name in turn:
                    slider = getattr(self, slider_name)
                    slider.setValue(turn[setting_name])
            
            # Update turn combos
            combo_mappings = [
                ("ip_turn_bet_size", "ip_turn_bet_size_combo"),
                ("oop_turn_bet_size", "oop_turn_bet_size_combo")
            ]
            
            for setting_name, combo_name in combo_mappings:
                if hasattr(self, combo_name) and setting_name in turn:
                    combo = getattr(self, combo_name)
                    index = combo.findText(turn[setting_name])
                    if index >= 0:
                        combo.setCurrentIndex(index)
        
        # Process river settings
        if "river" in settings:
            river = settings["river"]
            
            # Update river sliders
            slider_mappings = [
                ("third_barrel_freq", "third_barrel_freq_slider"),
                ("delayed_second_barrel_freq", "delayed_second_barrel_freq_slider"),
                ("river_checkraise_freq", "river_checkraise_freq_slider"),
                ("river_float_freq", "river_float_freq_slider"),
                ("river_probe_freq", "river_probe_freq_slider"),
                ("river_fold_to_bet_freq", "river_fold_to_bet_freq_slider"),
                ("river_bluff_raise_freq", "river_bluff_raise_freq_slider"),
                ("river_value_range", "river_value_range_slider"),
                ("river_bluff_range", "river_bluff_range_slider"),
                ("river_check_behind_range", "river_check_behind_range_slider")
            ]
            
            for setting_name, slider_name in slider_mappings:
                if hasattr(self, slider_name) and setting_name in river:
                    slider = getattr(self, slider_name)
                    slider.setValue(river[setting_name])
            
            # Update river combos
            combo_mappings = [
                ("ip_river_bet_size", "ip_river_bet_size_combo"),
                ("oop_river_bet_size", "oop_river_bet_size_combo")
            ]
            
            for setting_name, combo_name in combo_mappings:
                if hasattr(self, combo_name) and setting_name in river:
                    combo = getattr(self, combo_name)
                    index = combo.findText(river[setting_name])
                    if index >= 0:
                        combo.setCurrentIndex(index)
                        
    def connect_ui_events(self):
        """Connect UI event handlers to their respective slots"""
        # Connect preflop sliders to their variable updaters
        # This would be done for each slider and combobox in the UI
        # Example:
        if hasattr(self, "ep1_range_slider"):
            self.ep1_range_slider.valueChanged.connect(lambda v: setattr(self, 'ep1_range', v))
        
        # Similar for flop, turn, and river controls
        
        # Connect flop texture sliders
        slider_mappings = [
            ('ip_cbet_freq_slider', 'ip_cbet_freq'),
            ('oop_cbet_freq_slider', 'oop_cbet_freq'),
            ('dry_board_adjust_slider', 'dry_board_adjust'),
            ('wet_board_adjust_slider', 'wet_board_adjust'),
            ('checkraise_defense_slider', 'checkraise_defense'),
            ('value_aggression_slider', 'value_aggression'),
            ('draw_aggression_slider', 'draw_aggression'),
            ('semibluff_freq_slider', 'semibluff_freq'),
            ('multiway_cbet_freq_slider', 'multiway_cbet_freq'),
            ('multiway_value_range_slider', 'multiway_value_range'),
            # Nouveaux sliders pour les textures avancées
            ('monotone_board_adjust_slider', 'monotone_board_adjust'),
            ('paired_board_adjust_slider', 'paired_board_adjust'),
            ('connected_board_adjust_slider', 'connected_board_adjust'),
            ('high_card_board_adjust_slider', 'high_card_board_adjust'),
            ('low_card_board_adjust_slider', 'low_card_board_adjust'),
            ('dynamic_board_adjust_slider', 'dynamic_board_adjust'),
            ('static_board_adjust_slider', 'static_board_adjust'),
            ('polarization_slider', 'polarization')
        ]
        
        for slider_name, attr_name in slider_mappings:
            if hasattr(self, slider_name):
                slider = getattr(self, slider_name)
                slider.valueChanged.connect(lambda v, attr=attr_name: setattr(self, attr, v))
    
    def reset_settings(self):
        """Reset all settings to their default values"""
        # Re-initialize all variables
        self.initialize_variables()
        
        # Update all UI components to reflect the reset values
        self.update_ui_from_settings()
        
        # Show confirmation message
        QMessageBox.information(self, "Settings Reset", "All settings have been reset to their default values.")
        
    def update_ui_from_settings(self):
        """Update all UI components to reflect the current settings values"""
        # This method would update all sliders, combos, etc.
        # based on the current values in the instance variables
        
        # Example for a slider
        if hasattr(self, "ep1_range_slider"):
            self.ep1_range_slider.setValue(self.ep1_range)
        
        # Example for a combo
        if hasattr(self, "ep1_sizing_combo"):
            index = self.ep1_sizing_combo.findText(self.ep1_sizing)
            if index >= 0:
                self.ep1_sizing_combo.setCurrentIndex(index)
        
        # Similarly for all other UI components
    
    def add_import_export_buttons(self, config_layout):
        """Add import/export buttons to the config tab"""
        button_frame = QWidget()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        import_btn = QPushButton("Import Settings")
        import_btn.clicked.connect(self.import_settings)
        
        export_btn = QPushButton("Export Settings")
        export_btn.clicked.connect(self.export_settings)
        
        reset_btn = QPushButton("Reset All Settings")
        reset_btn.clicked.connect(self.reset_settings)
        
        button_layout.addWidget(import_btn)
        button_layout.addWidget(export_btn)
        button_layout.addWidget(reset_btn)
        button_layout.addStretch(1)
        
        config_layout.addWidget(button_frame)
    
    def closeEvent(self, event):
        """Handle the window close event"""
        # Ask for confirmation if there are unsaved changes
        if hasattr(self, "preview_text") and self.preview_text.toPlainText().strip():
            reply = QMessageBox.question(
                self, 
                "Confirm Exit",
                "There might be unsaved changes. Do you want to exit anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
        
        # Accept the event and close the window
        event.accept()                    