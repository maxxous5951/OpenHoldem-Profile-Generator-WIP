"""
Onglet des paramètres flop pour l'application OpenHoldem Profile Generator
"""
from PyQt6.QtWidgets import (QGridLayout, QLabel, QSlider, QComboBox, 
                            QGroupBox)
from PyQt6.QtCore import Qt
from ui.components import create_scroll_area

def create_flop_tab(main_window):
    """
    Crée l'onglet des paramètres flop
    
    Args:
        main_window (OpenHoldemProfileGenerator): Instance de la fenêtre principale
    
    Returns:
        QScrollArea: Zone de défilement contenant l'onglet flop
    """
    flop_scroll, flop_widget, flop_layout = create_scroll_area()
    
    # C-Bet settings
    cbet_group = QGroupBox("C-Bet Settings")
    cbet_layout = QGridLayout(cbet_group)
    
    cbet_layout.addWidget(QLabel("IP C-Bet Frequency (%):"), 0, 0)
    main_window.ip_cbet_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.ip_cbet_freq_slider.setRange(0, 100)
    main_window.ip_cbet_freq_slider.setValue(70)
    main_window.ip_cbet_freq_label = QLabel("70")
    main_window.ip_cbet_freq_slider.valueChanged.connect(lambda v: main_window.ip_cbet_freq_label.setText(str(v)))
    cbet_layout.addWidget(main_window.ip_cbet_freq_slider, 0, 1)
    cbet_layout.addWidget(main_window.ip_cbet_freq_label, 0, 2)
    
    cbet_layout.addWidget(QLabel("OOP C-Bet Frequency (%):"), 1, 0)
    main_window.oop_cbet_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.oop_cbet_freq_slider.setRange(0, 100)
    main_window.oop_cbet_freq_slider.setValue(60)
    main_window.oop_cbet_freq_label = QLabel("60")
    main_window.oop_cbet_freq_slider.valueChanged.connect(lambda v: main_window.oop_cbet_freq_label.setText(str(v)))
    cbet_layout.addWidget(main_window.oop_cbet_freq_slider, 1, 1)
    cbet_layout.addWidget(main_window.oop_cbet_freq_label, 1, 2)
    
    cbet_layout.addWidget(QLabel("IP C-Bet Size (% of pot):"), 2, 0)
    main_window.ip_cbet_size_combo = QComboBox()
    main_window.ip_cbet_size_combo.addItems(["33", "50", "66", "75", "100"])
    main_window.ip_cbet_size_combo.setCurrentIndex(1)  # Default to 50
    cbet_layout.addWidget(main_window.ip_cbet_size_combo, 2, 1)
    
    cbet_layout.addWidget(QLabel("OOP C-Bet Size (% of pot):"), 3, 0)
    main_window.oop_cbet_size_combo = QComboBox()
    main_window.oop_cbet_size_combo.addItems(["33", "50", "66", "75", "100"])
    main_window.oop_cbet_size_combo.setCurrentIndex(2)  # Default to 66
    cbet_layout.addWidget(main_window.oop_cbet_size_combo, 3, 1)
    
    flop_layout.addWidget(cbet_group)
    
    # Board texture adjustments
    texture_group = QGroupBox("Board Texture Adjustments")
    texture_layout = QGridLayout(texture_group)
    
    texture_layout.addWidget(QLabel("Dry Board Adjustment (%):"), 0, 0)
    main_window.dry_board_adjust_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.dry_board_adjust_slider.setRange(-50, 50)
    main_window.dry_board_adjust_slider.setValue(20)
    main_window.dry_board_adjust_label = QLabel("20")
    main_window.dry_board_adjust_slider.valueChanged.connect(lambda v: main_window.dry_board_adjust_label.setText(str(v)))
    texture_layout.addWidget(main_window.dry_board_adjust_slider, 0, 1)
    texture_layout.addWidget(main_window.dry_board_adjust_label, 0, 2)
    
    texture_layout.addWidget(QLabel("Wet Board Adjustment (%):"), 1, 0)
    main_window.wet_board_adjust_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.wet_board_adjust_slider.setRange(-50, 50)
    main_window.wet_board_adjust_slider.setValue(-20)
    main_window.wet_board_adjust_label = QLabel("-20")
    main_window.wet_board_adjust_slider.valueChanged.connect(lambda v: main_window.wet_board_adjust_label.setText(str(v)))
    texture_layout.addWidget(main_window.wet_board_adjust_slider, 1, 1)
    texture_layout.addWidget(main_window.wet_board_adjust_label, 1, 2)
    
    flop_layout.addWidget(texture_group)
    
    # Facing bets
    facing_group = QGroupBox("Facing Bets")
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
    
    flop_layout.addWidget(facing_group)
    
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
    
    flop_layout.addWidget(ranges_group)
    
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
    
    flop_layout.addWidget(multiway_group)
    
    return flop_scroll
