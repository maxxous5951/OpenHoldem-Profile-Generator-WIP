"""
Onglet des paramètres flop pour l'application OpenHoldem Profile Generator
Version améliorée avec support pour les classifications avancées de textures de board
"""
from PyQt6.QtWidgets import (QGridLayout, QLabel, QSlider, QComboBox, 
                           QGroupBox, QVBoxLayout, QHBoxLayout, QTabWidget,
                           QWidget, QPushButton)
from PyQt6.QtCore import Qt
from ui.components import create_scroll_area

def create_flop_tab(main_window):
    """
    Crée l'onglet des paramètres flop avec support pour la classification avancée des textures de board
    
    Args:
        main_window (OpenHoldemProfileGenerator): Instance de la fenêtre principale
    
    Returns:
        QScrollArea: Zone de défilement contenant l'onglet flop
    """
    flop_scroll, flop_widget, flop_layout = create_scroll_area()
    
    # Titre de l'onglet
    title_widget = QWidget()
    title_layout = QHBoxLayout(title_widget)
    title_layout.setContentsMargins(0, 0, 0, 0)
    
    title_label = QLabel("Paramètres de stratégie au flop")
    title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
    title_layout.addWidget(title_label)
    
    title_layout.addStretch(1)
    
    # Bouton de réinitialisation
    reset_btn = QPushButton("Réinitialiser les paramètres")
    reset_btn.clicked.connect(lambda: reset_flop_settings(main_window))
    title_layout.addWidget(reset_btn)
    
    flop_layout.addWidget(title_widget)
    
    # Créer des onglets pour mieux organiser les paramètres
    flop_tabs = QTabWidget()
    flop_layout.addWidget(flop_tabs)
	
	# Onglet des paramètres de C-Bet
    cbet_tab = QWidget()
    cbet_layout = QVBoxLayout(cbet_tab)
    
    # C-Bet settings
    cbet_group = QGroupBox("Paramètres C-Bet")
    cbet_layout_grid = QGridLayout(cbet_group)
    
    cbet_layout_grid.addWidget(QLabel("IP C-Bet Frequency (%):"), 0, 0)
    main_window.ip_cbet_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.ip_cbet_freq_slider.setRange(0, 100)
    main_window.ip_cbet_freq_slider.setValue(70)
    main_window.ip_cbet_freq_label = QLabel("70")
    main_window.ip_cbet_freq_slider.valueChanged.connect(lambda v: main_window.ip_cbet_freq_label.setText(str(v)))
    cbet_layout_grid.addWidget(main_window.ip_cbet_freq_slider, 0, 1)
    cbet_layout_grid.addWidget(main_window.ip_cbet_freq_label, 0, 2)
    
    cbet_layout_grid.addWidget(QLabel("OOP C-Bet Frequency (%):"), 1, 0)
    main_window.oop_cbet_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.oop_cbet_freq_slider.setRange(0, 100)
    main_window.oop_cbet_freq_slider.setValue(60)
    main_window.oop_cbet_freq_label = QLabel("60")
    main_window.oop_cbet_freq_slider.valueChanged.connect(lambda v: main_window.oop_cbet_freq_label.setText(str(v)))
    cbet_layout_grid.addWidget(main_window.oop_cbet_freq_slider, 1, 1)
    cbet_layout_grid.addWidget(main_window.oop_cbet_freq_label, 1, 2)
    
    cbet_layout_grid.addWidget(QLabel("IP C-Bet Size (% of pot):"), 2, 0)
    main_window.ip_cbet_size_combo = QComboBox()
    main_window.ip_cbet_size_combo.addItems(["33", "50", "66", "75", "100"])
    main_window.ip_cbet_size_combo.setCurrentIndex(1)  # Default to 50
    cbet_layout_grid.addWidget(main_window.ip_cbet_size_combo, 2, 1)
    
    cbet_layout_grid.addWidget(QLabel("OOP C-Bet Size (% of pot):"), 3, 0)
    main_window.oop_cbet_size_combo = QComboBox()
    main_window.oop_cbet_size_combo.addItems(["33", "50", "66", "75", "100"])
    main_window.oop_cbet_size_combo.setCurrentIndex(2)  # Default to 66
    cbet_layout_grid.addWidget(main_window.oop_cbet_size_combo, 3, 1)
    
    # Nouveaux paramètres de sizing
    cbet_layout_grid.addWidget(QLabel("Small C-Bet Size (% of pot):"), 4, 0)
    main_window.small_cbet_size_combo = QComboBox()
    main_window.small_cbet_size_combo.addItems(["25", "33", "40", "50"])
    main_window.small_cbet_size_combo.setCurrentIndex(1)  # Default to 33
    cbet_layout_grid.addWidget(main_window.small_cbet_size_combo, 4, 1)
    
    cbet_layout_grid.addWidget(QLabel("Large C-Bet Size (% of pot):"), 5, 0)
    main_window.large_cbet_size_combo = QComboBox()
    main_window.large_cbet_size_combo.addItems(["66", "75", "85", "100"])
    main_window.large_cbet_size_combo.setCurrentIndex(1)  # Default to 75
    cbet_layout_grid.addWidget(main_window.large_cbet_size_combo, 5, 1)
    
    cbet_layout_grid.addWidget(QLabel("Overbet Size (% of pot):"), 6, 0)
    main_window.overbet_cbet_size_combo = QComboBox()
    main_window.overbet_cbet_size_combo.addItems(["110", "125", "150", "200"])
    main_window.overbet_cbet_size_combo.setCurrentIndex(1)  # Default to 125
    cbet_layout_grid.addWidget(main_window.overbet_cbet_size_combo, 6, 1)
    
    cbet_layout.addWidget(cbet_group)
    
    # Multiway pots
    multiway_group = QGroupBox("Multiway Pots")
    multiway_layout = QGridLayout(multiway_group)
    
    multiway_layout.addWidget(QLabel("Multiway C-Bet Frequency (%):"), 0, 0)
    main_window.multiway_cbet_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.multiway_cbet_freq_slider.setRange(0, 100)
    main_window.multiway_cbet_freq_slider.setValue(40)
    main_window.multiway_cbet_freq_label = QLabel("40")
    main_window.multiway_cbet_freq_slider.valueChanged.connect(lambda v: main_window.multiway_cbet_freq_label.setText(str(v)))
    multiway_layout.addWidget(main_window.multiway_cbet_freq_slider, 0, 1)
    multiway_layout.addWidget(main_window.multiway_cbet_freq_label, 0, 2)
    
    multiway_layout.addWidget(QLabel("Multiway Value Range (%):"), 1, 0)
    main_window.multiway_value_range_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.multiway_value_range_slider.setRange(0, 100)
    main_window.multiway_value_range_slider.setValue(25)
    main_window.multiway_value_range_label = QLabel("25")
    main_window.multiway_value_range_slider.valueChanged.connect(lambda v: main_window.multiway_value_range_label.setText(str(v)))
    multiway_layout.addWidget(main_window.multiway_value_range_slider, 1, 1)
    multiway_layout.addWidget(main_window.multiway_value_range_label, 1, 2)
    
    # Paramètre de polarisation
    multiway_layout.addWidget(QLabel("Polarisation (0-100):"), 2, 0)
    main_window.polarization_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.polarization_slider.setRange(0, 100)
    main_window.polarization_slider.setValue(50)
    main_window.polarization_label = QLabel("50")
    main_window.polarization_slider.valueChanged.connect(lambda v: main_window.polarization_label.setText(str(v)))
    multiway_layout.addWidget(main_window.polarization_slider, 2, 1)
    multiway_layout.addWidget(main_window.polarization_label, 2, 2)
    
    cbet_layout.addWidget(multiway_group)
    
    # Ajouter l'onglet C-Bet
    flop_tabs.addTab(cbet_tab, "C-Bet")
	
	# Onglet des textures de board
    texture_tab = QWidget()
    texture_layout = QVBoxLayout(texture_tab)
    
    # Textures de board de base
    base_texture_group = QGroupBox("Textures de Board Basiques")
    base_texture_layout = QGridLayout(base_texture_group)
    
    base_texture_layout.addWidget(QLabel("Dry Board Adjustment (%):"), 0, 0)
    main_window.dry_board_adjust_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.dry_board_adjust_slider.setRange(-50, 50)
    main_window.dry_board_adjust_slider.setValue(20)
    main_window.dry_board_adjust_label = QLabel("20")
    main_window.dry_board_adjust_slider.valueChanged.connect(lambda v: main_window.dry_board_adjust_label.setText(str(v)))
    base_texture_layout.addWidget(main_window.dry_board_adjust_slider, 0, 1)
    base_texture_layout.addWidget(main_window.dry_board_adjust_label, 0, 2)
    
    base_texture_layout.addWidget(QLabel("Wet Board Adjustment (%):"), 1, 0)
    main_window.wet_board_adjust_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.wet_board_adjust_slider.setRange(-50, 50)
    main_window.wet_board_adjust_slider.setValue(-20)
    main_window.wet_board_adjust_label = QLabel("-20")
    main_window.wet_board_adjust_slider.valueChanged.connect(lambda v: main_window.wet_board_adjust_label.setText(str(v)))
    base_texture_layout.addWidget(main_window.wet_board_adjust_slider, 1, 1)
    base_texture_layout.addWidget(main_window.wet_board_adjust_label, 1, 2)
    
    texture_layout.addWidget(base_texture_group)
    
    # Textures avancées - Distribution des couleurs
    color_texture_group = QGroupBox("Distribution des Couleurs")
    color_texture_layout = QGridLayout(color_texture_group)
    
    color_texture_layout.addWidget(QLabel("Monotone Board Adjustment (%):"), 0, 0)
    main_window.monotone_board_adjust_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.monotone_board_adjust_slider.setRange(-50, 50)
    main_window.monotone_board_adjust_slider.setValue(-25)
    main_window.monotone_board_adjust_label = QLabel("-25")
    main_window.monotone_board_adjust_slider.valueChanged.connect(lambda v: main_window.monotone_board_adjust_label.setText(str(v)))
    color_texture_layout.addWidget(main_window.monotone_board_adjust_slider, 0, 1)
    color_texture_layout.addWidget(main_window.monotone_board_adjust_label, 0, 2)
    
    texture_layout.addWidget(color_texture_group)
    
    # Textures avancées - Structure du board
    structure_texture_group = QGroupBox("Structure du Board")
    structure_texture_layout = QGridLayout(structure_texture_group)
    
    structure_texture_layout.addWidget(QLabel("Paired Board Adjustment (%):"), 0, 0)
    main_window.paired_board_adjust_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.paired_board_adjust_slider.setRange(-50, 50)
    main_window.paired_board_adjust_slider.setValue(15)
    main_window.paired_board_adjust_label = QLabel("15")
    main_window.paired_board_adjust_slider.valueChanged.connect(lambda v: main_window.paired_board_adjust_label.setText(str(v)))
    structure_texture_layout.addWidget(main_window.paired_board_adjust_slider, 0, 1)
    structure_texture_layout.addWidget(main_window.paired_board_adjust_label, 0, 2)
    
    structure_texture_layout.addWidget(QLabel("Connected Board Adjustment (%):"), 1, 0)
    main_window.connected_board_adjust_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.connected_board_adjust_slider.setRange(-50, 50)
    main_window.connected_board_adjust_slider.setValue(-20)
    main_window.connected_board_adjust_label = QLabel("-20")
    main_window.connected_board_adjust_slider.valueChanged.connect(lambda v: main_window.connected_board_adjust_label.setText(str(v)))
    structure_texture_layout.addWidget(main_window.connected_board_adjust_slider, 1, 1)
    structure_texture_layout.addWidget(main_window.connected_board_adjust_label, 1, 2)
    
    texture_layout.addWidget(structure_texture_group)
	
	# Textures avancées - Hauteur des cartes
    height_texture_group = QGroupBox("Hauteur des Cartes")
    height_texture_layout = QGridLayout(height_texture_group)
    
    height_texture_layout.addWidget(QLabel("High Card Board Adjustment (%):"), 0, 0)
    main_window.high_card_board_adjust_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.high_card_board_adjust_slider.setRange(-50, 50)
    main_window.high_card_board_adjust_slider.setValue(10)
    main_window.high_card_board_adjust_label = QLabel("10")
    main_window.high_card_board_adjust_slider.valueChanged.connect(lambda v: main_window.high_card_board_adjust_label.setText(str(v)))
    height_texture_layout.addWidget(main_window.high_card_board_adjust_slider, 0, 1)
    height_texture_layout.addWidget(main_window.high_card_board_adjust_label, 0, 2)
    
    height_texture_layout.addWidget(QLabel("Low Card Board Adjustment (%):"), 1, 0)
    main_window.low_card_board_adjust_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.low_card_board_adjust_slider.setRange(-50, 50)
    main_window.low_card_board_adjust_slider.setValue(-15)
    main_window.low_card_board_adjust_label = QLabel("-15")
    main_window.low_card_board_adjust_slider.valueChanged.connect(lambda v: main_window.low_card_board_adjust_label.setText(str(v)))
    height_texture_layout.addWidget(main_window.low_card_board_adjust_slider, 1, 1)
    height_texture_layout.addWidget(main_window.low_card_board_adjust_label, 1, 2)
    
    texture_layout.addWidget(height_texture_group)
    
    # Textures avancées - Potentiel de Draw
    draw_texture_group = QGroupBox("Potentiel de Draw")
    draw_texture_layout = QGridLayout(draw_texture_group)
    
    draw_texture_layout.addWidget(QLabel("Dynamic Board Adjustment (%):"), 0, 0)
    main_window.dynamic_board_adjust_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.dynamic_board_adjust_slider.setRange(-50, 50)
    main_window.dynamic_board_adjust_slider.setValue(-30)
    main_window.dynamic_board_adjust_label = QLabel("-30")
    main_window.dynamic_board_adjust_slider.valueChanged.connect(lambda v: main_window.dynamic_board_adjust_label.setText(str(v)))
    draw_texture_layout.addWidget(main_window.dynamic_board_adjust_slider, 0, 1)
    draw_texture_layout.addWidget(main_window.dynamic_board_adjust_label, 0, 2)
    
    draw_texture_layout.addWidget(QLabel("Static Board Adjustment (%):"), 1, 0)
    main_window.static_board_adjust_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.static_board_adjust_slider.setRange(-50, 50)
    main_window.static_board_adjust_slider.setValue(25)
    main_window.static_board_adjust_label = QLabel("25")
    main_window.static_board_adjust_slider.valueChanged.connect(lambda v: main_window.static_board_adjust_label.setText(str(v)))
    draw_texture_layout.addWidget(main_window.static_board_adjust_slider, 1, 1)
    draw_texture_layout.addWidget(main_window.static_board_adjust_label, 1, 2)
    
    texture_layout.addWidget(draw_texture_group)
    
    # Ajouter l'onglet Textures
    flop_tabs.addTab(texture_tab, "Textures de Board")
    
    # Onglet des réponses face aux mises
    facing_bets_tab = QWidget()
    facing_bets_layout = QVBoxLayout(facing_bets_tab)
    
    # Facing bets
    facing_group = QGroupBox("Responding to Bets")
    facing_layout = QGridLayout(facing_group)
    
    facing_layout.addWidget(QLabel("Check-Raise Defense (%):"), 0, 0)
    main_window.checkraise_defense_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.checkraise_defense_slider.setRange(0, 100)
    main_window.checkraise_defense_slider.setValue(35)
    main_window.checkraise_defense_label = QLabel("35")
    main_window.checkraise_defense_slider.valueChanged.connect(lambda v: main_window.checkraise_defense_label.setText(str(v)))
    facing_layout.addWidget(main_window.checkraise_defense_slider, 0, 1)
    facing_layout.addWidget(main_window.checkraise_defense_label, 0, 2)
    
    facing_layout.addWidget(QLabel("Donk Bet Response Style:"), 1, 0)
    main_window.donk_response_combo = QComboBox()
    main_window.donk_response_combo.addItems(["Fold/Call", "Call/Raise", "Aggressive"])
    main_window.donk_response_combo.setCurrentIndex(1)  # Default to Call/Raise
    facing_layout.addWidget(main_window.donk_response_combo, 1, 1)
    
    facing_bets_layout.addWidget(facing_group)
	
	# Hand ranges
    ranges_group = QGroupBox("Hand Ranges")
    ranges_layout = QGridLayout(ranges_group)
    
    ranges_layout.addWidget(QLabel("Value Hands Aggression (%):"), 0, 0)
    main_window.value_aggression_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.value_aggression_slider.setRange(0, 100)
    main_window.value_aggression_slider.setValue(80)
    main_window.value_aggression_label = QLabel("80")
    main_window.value_aggression_slider.valueChanged.connect(lambda v: main_window.value_aggression_label.setText(str(v)))
    ranges_layout.addWidget(main_window.value_aggression_slider, 0, 1)
    ranges_layout.addWidget(main_window.value_aggression_label, 0, 2)
    
    ranges_layout.addWidget(QLabel("Draw Hands Aggression (%):"), 1, 0)
    main_window.draw_aggression_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.draw_aggression_slider.setRange(0, 100)
    main_window.draw_aggression_slider.setValue(60)
    main_window.draw_aggression_label = QLabel("60")
    main_window.draw_aggression_slider.valueChanged.connect(lambda v: main_window.draw_aggression_label.setText(str(v)))
    ranges_layout.addWidget(main_window.draw_aggression_slider, 1, 1)
    ranges_layout.addWidget(main_window.draw_aggression_label, 1, 2)
    
    ranges_layout.addWidget(QLabel("Semi-Bluff Frequency (%):"), 2, 0)
    main_window.semibluff_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.semibluff_freq_slider.setRange(0, 100)
    main_window.semibluff_freq_slider.setValue(65)
    main_window.semibluff_freq_label = QLabel("65")
    main_window.semibluff_freq_slider.valueChanged.connect(lambda v: main_window.semibluff_freq_label.setText(str(v)))
    ranges_layout.addWidget(main_window.semibluff_freq_slider, 2, 1)
    ranges_layout.addWidget(main_window.semibluff_freq_label, 2, 2)
    
    facing_bets_layout.addWidget(ranges_group)
    
    # Ajouter l'onglet Facing Bets
    flop_tabs.addTab(facing_bets_tab, "Face aux Mises")
    
    # Description de l'onglet
    description_group = QGroupBox("Aide sur les textures de board")
    description_layout = QVBoxLayout(description_group)
    
    description_text = QLabel(
        "Les ajustements de texture déterminent comment la stratégie s'adapte aux différents types de flop:\n\n"
        "- Valeurs positives: augmentent la fréquence de c-bet sur ce type de board\n"
        "- Valeurs négatives: réduisent la fréquence de c-bet sur ce type de board\n\n"
        "Board monotone: trois cartes de la même couleur (ex: ♣8♣5♣2)\n"
        "Board pairé: contient une paire (ex: A♠A♥7♦)\n"
        "Board connecté: trois cartes consécutives (ex: 9♠8♥7♦)\n"
        "Board dynamique: beaucoup de tirages possibles\n"
        "Board statique: peu de possibilités d'amélioration"
    )
    description_text.setWordWrap(True)
    description_layout.addWidget(description_text)
    
    flop_layout.addWidget(description_group)
    
    # Set up connections
    connect_flop_ui_events(main_window)
    
    return flop_scroll
	
def connect_flop_ui_events(main_window):
    """
    Configure les événements de l'interface utilisateur pour l'onglet flop
    
    Args:
        main_window (OpenHoldemProfileGenerator): Instance de la fenêtre principale
    """
    # Update variables when sliders change
    main_window.ip_cbet_freq_slider.valueChanged.connect(lambda v: setattr(main_window, 'ip_cbet_freq', v))
    main_window.oop_cbet_freq_slider.valueChanged.connect(lambda v: setattr(main_window, 'oop_cbet_freq', v))
    main_window.dry_board_adjust_slider.valueChanged.connect(lambda v: setattr(main_window, 'dry_board_adjust', v))
    main_window.wet_board_adjust_slider.valueChanged.connect(lambda v: setattr(main_window, 'wet_board_adjust', v))
    main_window.checkraise_defense_slider.valueChanged.connect(lambda v: setattr(main_window, 'checkraise_defense', v))
    main_window.value_aggression_slider.valueChanged.connect(lambda v: setattr(main_window, 'value_aggression', v))
    main_window.draw_aggression_slider.valueChanged.connect(lambda v: setattr(main_window, 'draw_aggression', v))
    main_window.semibluff_freq_slider.valueChanged.connect(lambda v: setattr(main_window, 'semibluff_freq', v))
    main_window.multiway_cbet_freq_slider.valueChanged.connect(lambda v: setattr(main_window, 'multiway_cbet_freq', v))
    main_window.multiway_value_range_slider.valueChanged.connect(lambda v: setattr(main_window, 'multiway_value_range', v))
    
    # Nouvelles textures avancées
    main_window.monotone_board_adjust_slider.valueChanged.connect(lambda v: setattr(main_window, 'monotone_board_adjust', v))
    main_window.paired_board_adjust_slider.valueChanged.connect(lambda v: setattr(main_window, 'paired_board_adjust', v))
    main_window.connected_board_adjust_slider.valueChanged.connect(lambda v: setattr(main_window, 'connected_board_adjust', v))
    main_window.high_card_board_adjust_slider.valueChanged.connect(lambda v: setattr(main_window, 'high_card_board_adjust', v))
    main_window.low_card_board_adjust_slider.valueChanged.connect(lambda v: setattr(main_window, 'low_card_board_adjust', v))
    main_window.dynamic_board_adjust_slider.valueChanged.connect(lambda v: setattr(main_window, 'dynamic_board_adjust', v))
    main_window.static_board_adjust_slider.valueChanged.connect(lambda v: setattr(main_window, 'static_board_adjust', v))
    main_window.polarization_slider.valueChanged.connect(lambda v: setattr(main_window, 'polarization', v))
    
    # Combobox updates
    main_window.ip_cbet_size_combo.currentTextChanged.connect(lambda v: setattr(main_window, 'ip_cbet_size', v))
    main_window.oop_cbet_size_combo.currentTextChanged.connect(lambda v: setattr(main_window, 'oop_cbet_size', v))
    main_window.donk_response_combo.currentTextChanged.connect(lambda v: setattr(main_window, 'donk_response', v))
    main_window.small_cbet_size_combo.currentTextChanged.connect(lambda v: setattr(main_window, 'small_cbet_size', v))
    main_window.large_cbet_size_combo.currentTextChanged.connect(lambda v: setattr(main_window, 'large_cbet_size', v))
    main_window.overbet_cbet_size_combo.currentTextChanged.connect(lambda v: setattr(main_window, 'overbet_cbet_size', v))

def reset_flop_settings(main_window):
    """
    Réinitialise tous les paramètres de l'onglet flop aux valeurs par défaut
    
    Args:
        main_window (OpenHoldemProfileGenerator): Instance de la fenêtre principale
    """
    # Réinitialiser les sliders de base
    main_window.ip_cbet_freq_slider.setValue(70)
    main_window.oop_cbet_freq_slider.setValue(60)
    main_window.dry_board_adjust_slider.setValue(20)
    main_window.wet_board_adjust_slider.setValue(-20)
    main_window.checkraise_defense_slider.setValue(35)
    main_window.value_aggression_slider.setValue(80)
    main_window.draw_aggression_slider.setValue(60)
    main_window.semibluff_freq_slider.setValue(65)
    main_window.multiway_cbet_freq_slider.setValue(40)
    main_window.multiway_value_range_slider.setValue(25)
    
    # Réinitialiser les sliders avancés
    main_window.monotone_board_adjust_slider.setValue(-25)
    main_window.paired_board_adjust_slider.setValue(15)
    main_window.connected_board_adjust_slider.setValue(-20)
    main_window.high_card_board_adjust_slider.setValue(10)
    main_window.low_card_board_adjust_slider.setValue(-15)
    main_window.dynamic_board_adjust_slider.setValue(-30)
    main_window.static_board_adjust_slider.setValue(25)
    main_window.polarization_slider.setValue(50)
    
    # Réinitialiser les combo boxes
    main_window.ip_cbet_size_combo.setCurrentIndex(1)  # "50"
    main_window.oop_cbet_size_combo.setCurrentIndex(2)  # "66"
    main_window.donk_response_combo.setCurrentIndex(1)  # "Call/Raise"
    main_window.small_cbet_size_combo.setCurrentIndex(1)  # "33"
    main_window.large_cbet_size_combo.setCurrentIndex(1)  # "75"
    main_window.overbet_cbet_size_combo.setCurrentIndex(1)  # "125"	