"""
Fenêtre principale de l'application OpenHoldem Profile Generator
"""
from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout,
                           QWidget, QPushButton, QTextEdit, QScrollArea, 
                           QFileDialog, QMessageBox, QGroupBox, QComboBox)

from generators.preflop_generator import PreflopProfileGenerator
from generators.flop_generator import FlopProfileGenerator
from generators.turn_generator import TurnProfileGenerator
from generators.river_generator import RiverProfileGenerator

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
        
        # Create the generators
        self.preflop_generator = PreflopProfileGenerator()
        self.flop_generator = FlopProfileGenerator()
        self.turn_generator = TurnProfileGenerator()
        self.river_generator = RiverProfileGenerator()
        
        # Setup the UI
        self.create_ui()
        
    def initialize_variables(self):
        """Initialize all configuration variables with default values"""
        # Configuration variables
        self.num_players = 9
        self.game_type = "Cash Game"
        
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
        
    def collect_preflop_settings(self):
        """Gather all preflop settings from the UI into a dictionary"""
        return {
            "num_players": int(self.num_players_combo.currentText()),
            "game_type": self.game_type_combo.currentText(),
            "aggression": 50,  # Fixed value for now
            "tightness": 50,   # Fixed value for now
            "limp_frequency": 30,  # Fixed value for now
            "threebet_frequency": 40,  # Fixed value for now
            "fourbet_frequency": 30,  # Fixed value for now
            "squeeze_frequency": 35,  # Fixed value for now
            "open_raise_size": "2.5",
            "ep_range": self.ep_range_slider.value(),
            "mp_range": self.mp_range_slider.value(),
            "lp_range": self.lp_range_slider.value(),
            "ep_sizing": self.ep_sizing_combo.currentText(),
            "mp_sizing": self.mp_sizing_combo.currentText(),
            "lp_sizing": self.lp_sizing_combo.currentText(),
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
            "aggression": 50  # Fixed for now
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
            "aggression": 50  # Fixed for now
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
            "aggression": 50  # Fixed for now
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
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.preview_text.toPlainText())
            QMessageBox.information(self, "Save Successful", f"Profile saved to {file_path}")