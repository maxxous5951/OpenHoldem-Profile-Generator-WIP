"""
Module de sélection de profils pour OpenHoldem Profile Generator
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QComboBox, QGroupBox, QGridLayout)
from PyQt6.QtCore import Qt

class ProfileSelector(QDialog):
    """
    Dialogue permettant de sélectionner un profil de joueur prédéfini
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Player Profile Selection")
        self.resize(500, 300)
        
        self.selected_profile = None
        self.create_ui()
        
    def create_ui(self):
        """
        Crée l'interface utilisateur du sélecteur de profil
        """
        layout = QVBoxLayout(self)
        
        # Profil actuel
        current_group = QGroupBox("Current profile")
        current_layout = QGridLayout(current_group)
        current_layout.addWidget(QLabel("Current profile:"), 0, 0)
        current_layout.addWidget(QLabel("Custom"), 0, 1)
        layout.addWidget(current_group)
        
        # Sélection de profil
        profile_group = QGroupBox("Profile selection")
        profile_layout = QGridLayout(profile_group)
        
        profile_layout.addWidget(QLabel("Category:"), 0, 0)
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Play Style", "Game Type"])
        self.category_combo.currentIndexChanged.connect(self.update_profiles)
        profile_layout.addWidget(self.category_combo, 0, 1)
        
        profile_layout.addWidget(QLabel("Profil:"), 1, 0)
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(["TAG", "LAG", "Nit", "Fish", "Loose Passive"])
        profile_layout.addWidget(self.profile_combo, 1, 1)
        
        profile_layout.addWidget(QLabel("Description:"), 2, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.description_label = QLabel("Tight-Aggressive - Solid playstyle with tight ranges and an aggressive post-flop approach")
        self.description_label.setWordWrap(True)
        profile_layout.addWidget(self.description_label, 2, 1)
        
        layout.addWidget(profile_group)
        
        # Profil Stack Adjust (pour tournois)
        stack_group = QGroupBox("Stack Adjustments (Tournaments)")
        stack_layout = QGridLayout(stack_group)
        
        stack_layout.addWidget(QLabel("Adaptations according to the stack:"), 0, 0)
        self.stack_adjust_combo = QComboBox()
        self.stack_adjust_combo.addItems(["Standard", "Big Stack (>50BB)", "Medium Stack (25-50BB)", "Small Stack (10-25BB)", "Short Stack (<10BB)"])
        stack_layout.addWidget(self.stack_adjust_combo, 0, 1)
        
        stack_layout.addWidget(QLabel("Aggression adjustment:"), 1, 0)
        self.aggression_combo = QComboBox()
        self.aggression_combo.addItems(["Standard", "More aggressive (+15%)", "Less aggressive (-15%)", "Very aggressive (+30%)", "Very cautious (-30%)"])
        stack_layout.addWidget(self.aggression_combo, 1, 1)
        
        layout.addWidget(stack_group)
        
        # Zone des boutons
        button_layout = QHBoxLayout()
        
        self.info_button = QPushButton("Info")
        self.info_button.clicked.connect(self.show_profile_info)
        button_layout.addWidget(self.info_button)
        
        button_layout.addStretch(1)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_profile)
        button_layout.addWidget(self.apply_button)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept_profile)
        button_layout.addWidget(self.ok_button)
        
        layout.addLayout(button_layout)
        
        # Initialiser l'affichage
        self.update_profiles(0)
        
    def update_profiles(self, index):
        """
        Met à jour la liste des profils en fonction de la catégorie sélectionnée
        
        Args:
            index (int): Index de la catégorie sélectionnée
        """
        self.profile_combo.clear()
        
        if index == 0:  # Style de jeu
            self.profile_combo.addItems(["TAG", "LAG", "Nit", "Fish", "Loose Passive"])
            self.description_label.setText("Tight-Aggressive - Solid playstyle with tight ranges and an aggressive post-flop approach")
            self.stack_adjust_combo.setEnabled(True)
        else:  # Type de partie
            self.profile_combo.addItems(["Cash Game", "Tournament", "SNG", "MTT"])
            self.description_label.setText("Cash Game - Profile suitable for cash games, more patience and exploitation")
            self.stack_adjust_combo.setEnabled(index != 1)  # Désactiver pour Cash Game
        
        self.profile_combo.currentIndexChanged.connect(self.update_description)
        
    def update_description(self, index):
        """
        Updates the description based on the selected profile
        
        Args:
            index (int): Index of the selected profile
        """
        category = self.category_combo.currentIndex()
        profile = self.profile_combo.currentText()
        
        descriptions = {
            "TAG": "Tight-Aggressive - Solid playing style with tight ranges and an aggressive post-flop approach",
            "LAG": "Loose-Aggressive - Very aggressive playing style with wider ranges and lots of pressure on opponents",
            "Nit": "Nit - Extremely tight playing style, only plays the best hands",
            "Fish": "Fish - Beginner player with very wide ranges and inconsistent play",
            "Loose Passive": "Loose-Passive - Player who plays a lot of hands but passively",
            "Cash Game": "Cash Game - Profile adapted for cash games, more patience and exploitation",
            "Tournament": "Tournament - General profile adapted for tournaments, balanced but aggressive",
            "SNG": "SNG - Profile for Sit & Go, adapted to fast blind structures",
            "MTT": "MTT - Profile for multi-table tournaments, adaptable to different phases"
        }
        
        self.description_label.setText(descriptions.get(profile, ""))
        
    def show_profile_info(self):
        """
        Displays detailed information about the selected profile
        """
        from PyQt6.QtWidgets import QMessageBox
        
        profile = self.profile_combo.currentText()
        msg = QMessageBox(self)
        msg.setWindowTitle(f"Information about profile {profile}")
        
        # Detailed information about the profile
        details = {
            "TAG": "The TAG (Tight-Aggressive) style is considered the most profitable playing style in the long run. It is characterized by:\n\n"
                   "- Strict hand selection preflop\n"
                   "- Aggressive play with selected hands\n"
                   "- Frequent and effective c-betting\n"
                   "- Good defense against 3-bets\n"
                   "- Exploits opponents' passivity",
            
            "LAG": "The LAG (Loose-Aggressive) style is difficult to master but potentially very profitable. It is characterized by:\n\n"
                   "- Playing many hands preflop\n"
                   "- Very aggressive in all phases of the game\n"
                   "- Lots of 3-bets and bluffs\n"
                   "- Applies strong pressure on opponents\n"
                   "- Requires a good read on opponents",
            
            "Nit": "The Nit style is an ultra-conservative style. It is characterized by:\n\n"
                   "- Only plays the best hands (AA, KK, QQ, AK)\n"
                   "- Few bluffs, mainly bets with strong hands\n"
                   "- Easy to read for experienced opponents\n"
                   "- Often too tight against 3-bets\n"
                   "- Very cautious approach to bankroll management",
            
            "Fish": "The Fish style represents a beginner or recreational player. It is characterized by:\n\n"
                   "- Plays way too many hands preflop\n"
                   "- Inconsistent bet sizing\n"
                   "- Calls too often with marginal hands\n"
                   "- Few bluffs or poorly designed bluffs\n"
                   "- Rarely 3-bets with medium hands",
            
            "Loose Passive": "The Loose Passive style is typical of intermediate players. It is characterized by:\n\n"
                   "- Plays many hands preflop but passively\n"
                   "- Prefers calling rather than raising\n"
                   "- Frequently limps preflop\n"
                   "- Rarely aggressive with drawing hands\n"
                   "- Generally easy to exploit",
            
            "Cash Game": "Profile optimized for cash games. Main characteristics:\n\n"
                   "- Balanced and profitable approach in the long run\n"
                   "- Well-balanced 3-bet and 4-bet range\n"
                   "- More pronounced position-dependent adaptations\n"
                   "- Exploitative play against weak opponents\n"
                   "- Optimal management of deep stacks",
            
            "Tournament": "Profile for generic tournaments. Main characteristics:\n\n"
                   "- Solid play adapted to standard blind structures\n"
                   "- Gradual increase in aggressiveness with rising blinds\n"
                   "- More selective ranges than in cash games\n"
                   "- Good balance between stack preservation and accumulation\n"
                   "- Adaptations according to tournament stage",
            
            "SNG": "Specific profile for Sit & Go tournaments. Main characteristics:\n\n"
                   "- Adapted to fast blind structures\n"
                   "- Importance of the bubble phase (ICM)\n"
                   "- Increased aggressiveness at the beginning and end of tournament\n"
                   "- Stricter blind defense\n"
                   "- Precise push/fold adaptations",
            
            "MTT": "Profile for Multi-Table Tournaments. Main characteristics:\n\n"
                   "- Phase-based strategy (early, middle, late, final table)\n"
                   "- Chip accumulation in early game\n"
                   "- Adaptation to different stack depths\n"
                   "- ICM considerations for final tables\n"
                   "- Balance between survival and accumulation"
        }
        
        msg.setText(details.get(profile, "No detailed information available"))
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
    
    def apply_profile(self):
        """
        Applies the selected profile without closing the window
        """
        profile_name = self.profile_combo.currentText()
        
        # Process stack and aggressiveness adjustments for tournaments
        stack_adjustment = self.stack_adjust_combo.currentText()
        aggression_adjustment = self.aggression_combo.currentText()
        
        # Return profile information
        self.selected_profile = {
            "profile_name": profile_name,
            "stack_adjustment": stack_adjustment,
            "aggression_adjustment": aggression_adjustment
        }
        
        # Update signal for the main window
        self.parent().update_profile(self.selected_profile)
        
    def accept_profile(self):
        """
        Applies the selected profile and closes the window
        """
        self.apply_profile()
        self.accept()
        
    @staticmethod
    def get_profile(parent=None):
        """
        Static method to open the dialog and retrieve the selected profile
        
        Args:
            parent (QWidget, optional): Parent widget
            
        Returns:
            dict: Information about the selected profile, or None if canceled
        """
        dialog = ProfileSelector(parent)
        result = dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            return dialog.selected_profile
        else:
            return None