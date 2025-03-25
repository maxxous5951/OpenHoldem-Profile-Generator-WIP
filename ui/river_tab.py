"""
Onglet des paramètres river pour l'application OpenHoldem Profile Generator
"""
from PyQt6.QtWidgets import (QGridLayout, QLabel, QSlider, QComboBox, 
                            QGroupBox)
from PyQt6.QtCore import Qt
from ui.components import create_scroll_area

def create_river_tab(main_window):
    """
    Crée l'onglet des paramètres river
    
    Args:
        main_window (OpenHoldemProfileGenerator): Instance de la fenêtre principale
    
    Returns:
        QScrollArea: Zone de défilement contenant l'onglet river
    """
    river_scroll, river_widget, river_layout = create_scroll_area()
    
    # Third Barrel settings
    barrel_group = QGroupBox("Third Barrel Settings")
    barrel_layout = QGridLayout(barrel_group)
    
    barrel_layout.addWidget(QLabel("Third Barrel Frequency (%):"), 0, 0)
    main_window.third_barrel_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.third_barrel_freq_slider.setRange(0, 100)
    main_window.third_barrel_freq_slider.setValue(40)
    main_window.third_barrel_freq_label = QLabel("40")
    main_window.third_barrel_freq_slider.valueChanged.connect(lambda v: main_window.third_barrel_freq_label.setText(str(v)))
    barrel_layout.addWidget(main_window.third_barrel_freq_slider, 0, 1)
    barrel_layout.addWidget(main_window.third_barrel_freq_label, 0, 2)
    
    barrel_layout.addWidget(QLabel("Delayed Second Barrel Frequency (%):"), 1, 0)
    main_window.delayed_second_barrel_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.delayed_second_barrel_freq_slider.setRange(0, 100)
    main_window.delayed_second_barrel_freq_slider.setValue(30)
    main_window.delayed_second_barrel_freq_label = QLabel("30")
    main_window.delayed_second_barrel_freq_slider.valueChanged.connect(lambda v: main_window.delayed_second_barrel_freq_label.setText(str(v)))
    barrel_layout.addWidget(main_window.delayed_second_barrel_freq_slider, 1, 1)
    barrel_layout.addWidget(main_window.delayed_second_barrel_freq_label, 1, 2)
    
    barrel_layout.addWidget(QLabel("IP River Bet Size (% of pot):"), 2, 0)
    main_window.ip_river_bet_size_combo = QComboBox()
    main_window.ip_river_bet_size_combo.addItems(["50", "66", "75", "100"])
    main_window.ip_river_bet_size_combo.setCurrentIndex(2)  # Default to 75
    barrel_layout.addWidget(main_window.ip_river_bet_size_combo, 2, 1)
    
    barrel_layout.addWidget(QLabel("OOP River Bet Size (% of pot):"), 3, 0)
    main_window.oop_river_bet_size_combo = QComboBox()
    main_window.oop_river_bet_size_combo.addItems(["50", "66", "75", "100"])
    main_window.oop_river_bet_size_combo.setCurrentIndex(2)  # Default to 75
    barrel_layout.addWidget(main_window.oop_river_bet_size_combo, 3, 1)
    
    river_layout.addWidget(barrel_group)
    
    # Facing River bets
    facing_river_group = QGroupBox("Facing River Bets")
    facing_river_layout = QGridLayout(facing_river_group)
    
    facing_river_layout.addWidget(QLabel("River Check-Raise Frequency (%):"), 0, 0)
    main_window.river_checkraise_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.river_checkraise_freq_slider.setRange(0, 100)
    main_window.river_checkraise_freq_slider.setValue(15)
    main_window.river_checkraise_freq_label = QLabel("15")
    main_window.river_checkraise_freq_slider.valueChanged.connect(lambda v: main_window.river_checkraise_freq_label.setText(str(v)))
    facing_river_layout.addWidget(main_window.river_checkraise_freq_slider, 0, 1)
    facing_river_layout.addWidget(main_window.river_checkraise_freq_label, 0, 2)
    
    facing_river_layout.addWidget(QLabel("River Float Frequency (%):"), 1, 0)
    main_window.river_float_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.river_float_freq_slider.setRange(0, 100)
    main_window.river_float_freq_slider.setValue(20)
    main_window.river_float_freq_label = QLabel("20")
    main_window.river_float_freq_slider.valueChanged.connect(lambda v: main_window.river_float_freq_label.setText(str(v)))
    facing_river_layout.addWidget(main_window.river_float_freq_slider, 1, 1)
    facing_river_layout.addWidget(main_window.river_float_freq_label, 1, 2)
    
    facing_river_layout.addWidget(QLabel("River Fold to Bet Frequency (%):"), 2, 0)
    main_window.river_fold_to_bet_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.river_fold_to_bet_freq_slider.setRange(0, 100)
    main_window.river_fold_to_bet_freq_slider.setValue(70)
    main_window.river_fold_to_bet_freq_label = QLabel("70")
    main_window.river_fold_to_bet_freq_slider.valueChanged.connect(lambda v: main_window.river_fold_to_bet_freq_label.setText(str(v)))
    facing_river_layout.addWidget(main_window.river_fold_to_bet_freq_slider, 2, 1)
    facing_river_layout.addWidget(main_window.river_fold_to_bet_freq_label, 2, 2)
    
    facing_river_layout.addWidget(QLabel("River Bluff Raise Frequency (%):"), 3, 0)
    main_window.river_bluff_raise_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.river_bluff_raise_freq_slider.setRange(0, 100)
    main_window.river_bluff_raise_freq_slider.setValue(10)
    main_window.river_bluff_raise_freq_label = QLabel("10")
    main_window.river_bluff_raise_freq_slider.valueChanged.connect(lambda v: main_window.river_bluff_raise_freq_label.setText(str(v)))
    facing_river_layout.addWidget(main_window.river_bluff_raise_freq_slider, 3, 1)
    facing_river_layout.addWidget(main_window.river_bluff_raise_freq_label, 3, 2)
    
    river_layout.addWidget(facing_river_group)
    
    # River Hand Ranges
    river_ranges_group = QGroupBox("River Hand Ranges")
    river_ranges_layout = QGridLayout(river_ranges_group)
    
    river_ranges_layout.addWidget(QLabel("River Value Range (%):"), 0, 0)
    main_window.river_value_range_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.river_value_range_slider.setRange(0, 100)
    main_window.river_value_range_slider.setValue(60)
    main_window.river_value_range_label = QLabel("60")
    main_window.river_value_range_slider.valueChanged.connect(lambda v: main_window.river_value_range_label.setText(str(v)))
    river_ranges_layout.addWidget(main_window.river_value_range_slider, 0, 1)
    river_ranges_layout.addWidget(main_window.river_value_range_label, 0, 2)
    
    river_ranges_layout.addWidget(QLabel("River Bluff Range (%):"), 1, 0)
    main_window.river_bluff_range_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.river_bluff_range_slider.setRange(0, 100)
    main_window.river_bluff_range_slider.setValue(15)
    main_window.river_bluff_range_label = QLabel("15")
    main_window.river_bluff_range_slider.valueChanged.connect(lambda v: main_window.river_bluff_range_label.setText(str(v)))
    river_ranges_layout.addWidget(main_window.river_bluff_range_slider, 1, 1)
    river_ranges_layout.addWidget(main_window.river_bluff_range_label, 1, 2)
    
    river_ranges_layout.addWidget(QLabel("River Check Behind Range (%):"), 2, 0)
    main_window.river_check_behind_range_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.river_check_behind_range_slider.setRange(0, 100)
    main_window.river_check_behind_range_slider.setValue(80)
    main_window.river_check_behind_range_label = QLabel("80")
    main_window.river_check_behind_range_slider.valueChanged.connect(lambda v: main_window.river_check_behind_range_label.setText(str(v)))
    river_ranges_layout.addWidget(main_window.river_check_behind_range_slider, 2, 1)
    river_ranges_layout.addWidget(main_window.river_check_behind_range_label, 2, 2)
    
    river_layout.addWidget(river_ranges_group)
    
    # Probe betting (River)
    river_probe_group = QGroupBox("River Probe Betting")
    river_probe_layout = QGridLayout(river_probe_group)
    
    river_probe_layout.addWidget(QLabel("River Probe Frequency (%):"), 0, 0)
    main_window.river_probe_freq_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.river_probe_freq_slider.setRange(0, 100)
    main_window.river_probe_freq_slider.setValue(25)
    main_window.river_probe_freq_label = QLabel("25")
    main_window.river_probe_freq_slider.valueChanged.connect(lambda v: main_window.river_probe_freq_label.setText(str(v)))
    river_probe_layout.addWidget(main_window.river_probe_freq_slider, 0, 1)
    river_probe_layout.addWidget(main_window.river_probe_freq_label, 0, 2)
    
    river_layout.addWidget(river_probe_group)
    
    return river_scroll
