"""
Onglet des paramètres turn pour l'application OpenHoldem Profile Generator
"""
from PyQt6.QtWidgets import (QGridLayout, QLabel, QSlider, QComboBox, 
                            QGroupBox)
from PyQt6.QtCore import Qt
from ui.components import create_scroll_area

def create_turn_tab(main_window):
    """
    Crée l'onglet des paramètres turn
    
    Args:
        main_window (OpenHoldemProfileGenerator): Instance de la fenêtre principale
    
    Returns:
        QScrollArea: Zone de défilement contenant l'onglet turn
    """
    turn_scroll, turn_widget, turn_layout = create_scroll_area()
    
    # Second Barrel settings
    second_barrel_group = QGroupBox("Second Barrel Settings")
    second_barrel_layout = QGridLayout(second_barrel_group)
    
    second_barrel_layout.addWidget(QLabel("Second Barrel Frequency (%):"), 0, 0)
    main_window.second_barrel_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.second_barrel_freq_slider.setRange(0, 100)
    main_window.second_barrel_freq_slider.setValue(60)
    main_window.second_barrel_freq_label = QLabel("60")
    main_window.second_barrel_freq_slider.valueChanged.connect(lambda v: main_window.second_barrel_freq_label.setText(str(v)))
    second_barrel_layout.addWidget(main_window.second_barrel_freq_slider, 0, 1)
    second_barrel_layout.addWidget(main_window.second_barrel_freq_label, 0, 2)
    
    second_barrel_layout.addWidget(QLabel("Delayed C-Bet Frequency (%):"), 1, 0)
    main_window.delayed_cbet_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.delayed_cbet_freq_slider.setRange(0, 100)
    main_window.delayed_cbet_freq_slider.setValue(40)
    main_window.delayed_cbet_freq_label = QLabel("40")
    main_window.delayed_cbet_freq_slider.valueChanged.connect(lambda v: main_window.delayed_cbet_freq_label.setText(str(v)))
    second_barrel_layout.addWidget(main_window.delayed_cbet_freq_slider, 1, 1)
    second_barrel_layout.addWidget(main_window.delayed_cbet_freq_label, 1, 2)
    
    second_barrel_layout.addWidget(QLabel("IP Turn Bet Size (% of pot):"), 2, 0)
    main_window.ip_turn_bet_size_combo = QComboBox()
    main_window.ip_turn_bet_size_combo.addItems(["50", "66", "75", "100"])
    main_window.ip_turn_bet_size_combo.setCurrentIndex(1)  # Default to 66
    second_barrel_layout.addWidget(main_window.ip_turn_bet_size_combo, 2, 1)
    
    second_barrel_layout.addWidget(QLabel("OOP Turn Bet Size (% of pot):"), 3, 0)
    main_window.oop_turn_bet_size_combo = QComboBox()
    main_window.oop_turn_bet_size_combo.addItems(["50", "66", "75", "100"])
    main_window.oop_turn_bet_size_combo.setCurrentIndex(2)  # Default to 75
    second_barrel_layout.addWidget(main_window.oop_turn_bet_size_combo, 3, 1)
    
    turn_layout.addWidget(second_barrel_group)
    
    # Turn Card adjustments
    turn_card_group = QGroupBox("Turn Card Adjustments")
    turn_card_layout = QGridLayout(turn_card_group)
    
    turn_card_layout.addWidget(QLabel("Scare Card Adjustment (%):"), 0, 0)
    main_window.scare_card_adjust_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.scare_card_adjust_slider.setRange(-50, 50)
    main_window.scare_card_adjust_slider.setValue(-15)
    main_window.scare_card_adjust_label = QLabel("-15")
    main_window.scare_card_adjust_slider.valueChanged.connect(lambda v: main_window.scare_card_adjust_label.setText(str(v)))
    turn_card_layout.addWidget(main_window.scare_card_adjust_slider, 0, 1)
    turn_card_layout.addWidget(main_window.scare_card_adjust_label, 0, 2)
    
    turn_card_layout.addWidget(QLabel("Draw Complete Adjustment (%):"), 1, 0)
    main_window.draw_complete_adjust_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.draw_complete_adjust_slider.setRange(-50, 50)
    main_window.draw_complete_adjust_slider.setValue(10)
    main_window.draw_complete_adjust_label = QLabel("10")
    main_window.draw_complete_adjust_slider.valueChanged.connect(lambda v: main_window.draw_complete_adjust_label.setText(str(v)))
    turn_card_layout.addWidget(main_window.draw_complete_adjust_slider, 1, 1)
    turn_card_layout.addWidget(main_window.draw_complete_adjust_label, 1, 2)
    
    turn_layout.addWidget(turn_card_group)
    
    # Facing Turn bets
    facing_turn_group = QGroupBox("Facing Turn Bets")
    facing_turn_layout = QGridLayout(facing_turn_group)
    
    facing_turn_layout.addWidget(QLabel("Turn Check-Raise Frequency (%):"), 0, 0)
    main_window.turn_checkraise_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.turn_checkraise_freq_slider.setRange(0, 100)
    main_window.turn_checkraise_freq_slider.setValue(25)
    main_window.turn_checkraise_freq_label = QLabel("25")
    main_window.turn_checkraise_freq_slider.valueChanged.connect(lambda v: main_window.turn_checkraise_freq_label.setText(str(v)))
    facing_turn_layout.addWidget(main_window.turn_checkraise_freq_slider, 0, 1)
    facing_turn_layout.addWidget(main_window.turn_checkraise_freq_label, 0, 2)
    
    facing_turn_layout.addWidget(QLabel("Turn Float Frequency (%):"), 1, 0)
    main_window.turn_float_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.turn_float_freq_slider.setRange(0, 100)
    main_window.turn_float_freq_slider.setValue(30)
    main_window.turn_float_freq_label = QLabel("30")
    main_window.turn_float_freq_slider.valueChanged.connect(lambda v: main_window.turn_float_freq_label.setText(str(v)))
    facing_turn_layout.addWidget(main_window.turn_float_freq_slider, 1, 1)
    facing_turn_layout.addWidget(main_window.turn_float_freq_label, 1, 2)
    
    facing_turn_layout.addWidget(QLabel("Turn Fold to C-Bet Frequency (%):"), 2, 0)
    main_window.turn_fold_to_cbet_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.turn_fold_to_cbet_freq_slider.setRange(0, 100)
    main_window.turn_fold_to_cbet_freq_slider.setValue(60)
    main_window.turn_fold_to_cbet_freq_label = QLabel("60")
    main_window.turn_fold_to_cbet_freq_slider.valueChanged.connect(lambda v: main_window.turn_fold_to_cbet_freq_label.setText(str(v)))
    facing_turn_layout.addWidget(main_window.turn_fold_to_cbet_freq_slider, 2, 1)
    facing_turn_layout.addWidget(main_window.turn_fold_to_cbet_freq_label, 2, 2)
    
    turn_layout.addWidget(facing_turn_group)
    
    # Probe betting
    probe_group = QGroupBox("Probe Betting")
    probe_layout = QGridLayout(probe_group)
    
    probe_layout.addWidget(QLabel("Turn Probe Frequency (%):"), 0, 0)
    main_window.turn_probe_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.turn_probe_freq_slider.setRange(0, 100)
    main_window.turn_probe_freq_slider.setValue(35)
    main_window.turn_probe_freq_label = QLabel("35")
    main_window.turn_probe_freq_slider.valueChanged.connect(lambda v: main_window.turn_probe_freq_label.setText(str(v)))
    probe_layout.addWidget(main_window.turn_probe_freq_slider, 0, 1)
    probe_layout.addWidget(main_window.turn_probe_freq_label, 0, 2)
    
    probe_layout.addWidget(QLabel("Turn Bluff Raise Frequency (%):"), 1, 0)
    main_window.turn_bluff_raise_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.turn_bluff_raise_freq_slider.setRange(0, 100)
    main_window.turn_bluff_raise_freq_slider.setValue(20)
    main_window.turn_bluff_raise_freq_label = QLabel("20")
    main_window.turn_bluff_raise_freq_slider.valueChanged.connect(lambda v: main_window.turn_bluff_raise_freq_label.setText(str(v)))
    probe_layout.addWidget(main_window.turn_bluff_raise_freq_slider, 1, 1)
    probe_layout.addWidget(main_window.turn_bluff_raise_freq_label, 1, 2)
    
    turn_layout.addWidget(probe_group)
    
    return turn_scroll
