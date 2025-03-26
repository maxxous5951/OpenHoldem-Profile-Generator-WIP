"""
Onglet des paramètres preflop pour l'application OpenHoldem Profile Generator
"""
from PyQt6.QtWidgets import (QGridLayout, QLabel, QSlider, QComboBox, 
                            QGroupBox, QTabWidget, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton)
from PyQt6.QtCore import Qt
from ui.components import create_scroll_area

def create_preflop_tab(main_window):
    """
    Crée l'onglet des paramètres preflop
    
    Args:
        main_window (OpenHoldemProfileGenerator): Instance de la fenêtre principale
    
    Returns:
        QScrollArea: Zone de défilement contenant l'onglet preflop
    """
    preflop_scroll, preflop_widget, preflop_layout = create_scroll_area()
    
    # Bouton de sélection de profil
    profile_frame = QWidget()
    profile_layout = QHBoxLayout(profile_frame)
    profile_layout.setContentsMargins(0, 0, 0, 10)
    
    main_window.profile_label = QLabel("Profil actuel: Personnalisé")
    profile_layout.addWidget(main_window.profile_label)
    
    profile_layout.addStretch(1)
    
    select_profile_button = QPushButton("Select a predefined profile")
    select_profile_button.clicked.connect(lambda: main_window.show_profile_selector())
    profile_layout.addWidget(select_profile_button)
    
    preflop_layout.addWidget(profile_frame)
    
    # Créer un sous-onglet pour organiser les différentes sections
    preflop_tabs = QTabWidget()
    preflop_layout.addWidget(preflop_tabs)
    
    # Onglet des ranges d'ouverture
    open_raise_tab = QWidget()
    open_raise_layout = QVBoxLayout(open_raise_tab)
    
    # Create Open Raise frame
    openraise_group = QGroupBox("Open Raise Ranges")
    openraise_layout = QGridLayout(openraise_group)
    
    # Définir les positions
    positions = [
        ("EP1 (UTG) Range (%)", "ep1_range", 10),
        ("EP2 (UTG+1) Range (%)", "ep2_range", 12),
        ("EP3 (UTG+2) Range (%)", "ep3_range", 14),
        ("MP1 Range (%)", "mp1_range", 16),
        ("MP2 Range (%)", "mp2_range", 18),
        ("MP3 (HJ) Range (%)", "mp3_range", 20),
        ("CO Range (%)", "co_range", 25),
        ("BTN Range (%)", "btn_range", 30),
        ("SB Range (%)", "sb_range", 35),
        ("BB Range (%)", "bb_range", 40)
    ]
    
    # Créer les sliders pour chaque position
    for i, (label_text, attr_name, default_value) in enumerate(positions):
        openraise_layout.addWidget(QLabel(label_text), i, 0)
        
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(default_value)
        
        label = QLabel(str(default_value))
        
        # Connexion personnalisée pour chaque slider
        slider.valueChanged.connect(lambda value, lbl=label: lbl.setText(str(value)))
        
        # Stocker les références dans l'objet main_window
        setattr(main_window, f"{attr_name}_slider", slider)
        setattr(main_window, f"{attr_name}_label", label)
        
        openraise_layout.addWidget(slider, i, 1)
        openraise_layout.addWidget(label, i, 2)
    
    open_raise_layout.addWidget(openraise_group)
    
    # Open Raise sizing
    sizing_group = QGroupBox("Position-Based Sizing")
    sizing_layout = QGridLayout(sizing_group)
    
    # Définir les tailles de raise par position
    sizings = [
        ("EP1 (UTG) Sizing (BB):", "ep1_sizing", ["2.5", "3.0", "3.5", "4.0"], 2),
        ("EP2 (UTG+1) Sizing (BB):", "ep2_sizing", ["2.5", "3.0", "3.5", "4.0"], 2),
        ("EP3 (UTG+2) Sizing (BB):", "ep3_sizing", ["2.5", "3.0", "3.5", "4.0"], 2),
        ("MP1 Sizing (BB):", "mp1_sizing", ["2.2", "2.5", "2.8", "3.0"], 1),
        ("MP2 Sizing (BB):", "mp2_sizing", ["2.2", "2.5", "2.8", "3.0"], 1),
        ("MP3 (HJ) Sizing (BB):", "mp3_sizing", ["2.2", "2.5", "2.8", "3.0"], 1),
        ("CO Sizing (BB):", "co_sizing", ["2.0", "2.2", "2.5", "2.8"], 2),
        ("BTN Sizing (BB):", "btn_sizing", ["2.0", "2.2", "2.5", "2.8"], 2),
        ("SB Sizing (BB):", "sb_sizing", ["2.0", "2.2", "2.5", "2.8"], 2)
    ]
    
    # Créer les combobox pour chaque position
    for i, (label_text, attr_name, options, default_index) in enumerate(sizings):
        sizing_layout.addWidget(QLabel(label_text), i, 0)
        
        combo = QComboBox()
        combo.addItems(options)
        combo.setCurrentIndex(default_index)
        
        # Stocker la référence dans l'objet main_window
        setattr(main_window, f"{attr_name}_combo", combo)
        
        sizing_layout.addWidget(combo, i, 1)
    
    open_raise_layout.addWidget(sizing_group)
    
    # Ajouter l'onglet Open Raise
    preflop_tabs.addTab(open_raise_tab, "Open Raise")
    
    # 3-Bet Defense Tab
    threebet_tab = QWidget()
    threebet_layout = QVBoxLayout(threebet_tab)
    
    # 3-Bet Defense
    threebet_group = QGroupBox("3-Bet Defense")
    threebet_def_layout = QGridLayout(threebet_group)
    
    threebet_def_layout.addWidget(QLabel("Call 3-Bet Range (%):"), 0, 0)
    main_window.call_3bet_range_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.call_3bet_range_slider.setRange(0, 100)
    main_window.call_3bet_range_slider.setValue(15)
    main_window.call_3bet_range_label = QLabel("15")
    main_window.call_3bet_range_slider.valueChanged.connect(lambda v: main_window.call_3bet_range_label.setText(str(v)))
    threebet_def_layout.addWidget(main_window.call_3bet_range_slider, 0, 1)
    threebet_def_layout.addWidget(main_window.call_3bet_range_label, 0, 2)
    
    threebet_def_layout.addWidget(QLabel("4-Bet Range (%):"), 1, 0)
    main_window.fourbet_range_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.fourbet_range_slider.setRange(0, 100)
    main_window.fourbet_range_slider.setValue(8)
    main_window.fourbet_range_label = QLabel("8")
    main_window.fourbet_range_slider.valueChanged.connect(lambda v: main_window.fourbet_range_label.setText(str(v)))
    threebet_def_layout.addWidget(main_window.fourbet_range_slider, 1, 1)
    threebet_def_layout.addWidget(main_window.fourbet_range_label, 1, 2)
    
    threebet_layout.addWidget(threebet_group)
    
    # Position adjustments
    position_adj_group = QGroupBox("Position Adjustments")
    position_adj_layout = QGridLayout(position_adj_group)
    
    position_adj_layout.addWidget(QLabel("In Position 3-Bet Adjust (%):"), 0, 0)
    main_window.ip_3bet_adjust_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.ip_3bet_adjust_slider.setRange(0, 100)
    main_window.ip_3bet_adjust_slider.setValue(20)
    main_window.ip_3bet_adjust_label = QLabel("20")
    main_window.ip_3bet_adjust_slider.valueChanged.connect(lambda v: main_window.ip_3bet_adjust_label.setText(str(v)))
    position_adj_layout.addWidget(main_window.ip_3bet_adjust_slider, 0, 1)
    position_adj_layout.addWidget(main_window.ip_3bet_adjust_label, 0, 2)
    
    position_adj_layout.addWidget(QLabel("vs Late Position 3-Bet Adjust (%):"), 1, 0)
    main_window.vs_lp_3bet_adjust_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.vs_lp_3bet_adjust_slider.setRange(0, 100)
    main_window.vs_lp_3bet_adjust_slider.setValue(15)
    main_window.vs_lp_3bet_adjust_label = QLabel("15")
    main_window.vs_lp_3bet_adjust_slider.valueChanged.connect(lambda v: main_window.vs_lp_3bet_adjust_label.setText(str(v)))
    position_adj_layout.addWidget(main_window.vs_lp_3bet_adjust_slider, 1, 1)
    position_adj_layout.addWidget(main_window.vs_lp_3bet_adjust_label, 1, 2)
    
    threebet_layout.addWidget(position_adj_group)
    
    # 4-Bet defense
    fourbet_group = QGroupBox("4-Bet Defense")
    fourbet_layout = QGridLayout(fourbet_group)
    
    fourbet_layout.addWidget(QLabel("Call 4-Bet Range (%):"), 0, 0)
    main_window.call_4bet_range_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.call_4bet_range_slider.setRange(0, 100)
    main_window.call_4bet_range_slider.setValue(5)
    main_window.call_4bet_range_label = QLabel("5")
    main_window.call_4bet_range_slider.valueChanged.connect(lambda v: main_window.call_4bet_range_label.setText(str(v)))
    fourbet_layout.addWidget(main_window.call_4bet_range_slider, 0, 1)
    fourbet_layout.addWidget(main_window.call_4bet_range_label, 0, 2)
    
    fourbet_layout.addWidget(QLabel("5-Bet Range (%):"), 1, 0)
    main_window.fivebet_range_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.fivebet_range_slider.setRange(0, 100)
    main_window.fivebet_range_slider.setValue(3)
    main_window.fivebet_range_label = QLabel("3")
    main_window.fivebet_range_slider.valueChanged.connect(lambda v: main_window.fivebet_range_label.setText(str(v)))
    fourbet_layout.addWidget(main_window.fivebet_range_slider, 1, 1)
    fourbet_layout.addWidget(main_window.fivebet_range_label, 1, 2)
    
    fourbet_layout.addWidget(QLabel("Short Stack 4-Bet Adjust (%):"), 2, 0)
    main_window.short_stack_4bet_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.short_stack_4bet_slider.setRange(0, 100)
    main_window.short_stack_4bet_slider.setValue(30)
    main_window.short_stack_4bet_label = QLabel("30")
    main_window.short_stack_4bet_slider.valueChanged.connect(lambda v: main_window.short_stack_4bet_label.setText(str(v)))
    fourbet_layout.addWidget(main_window.short_stack_4bet_slider, 2, 1)
    fourbet_layout.addWidget(main_window.short_stack_4bet_label, 2, 2)
    
    threebet_layout.addWidget(fourbet_group)
    
    # Ajouter l'onglet 3-Bet Defense
    preflop_tabs.addTab(threebet_tab, "3-Bet Defense")
    
    # Squeeze settings tab
    squeeze_tab = QWidget()
    squeeze_layout = QVBoxLayout(squeeze_tab)
    
    # Squeeze settings
    squeeze_group = QGroupBox("Squeeze Settings")
    squeeze_settings_layout = QGridLayout(squeeze_group)
    
    squeeze_settings_layout.addWidget(QLabel("Squeeze vs 1 Caller (%):"), 0, 0)
    main_window.squeeze_1caller_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.squeeze_1caller_slider.setRange(0, 100)
    main_window.squeeze_1caller_slider.setValue(12)
    main_window.squeeze_1caller_label = QLabel("12")
    main_window.squeeze_1caller_slider.valueChanged.connect(lambda v: main_window.squeeze_1caller_label.setText(str(v)))
    squeeze_settings_layout.addWidget(main_window.squeeze_1caller_slider, 0, 1)
    squeeze_settings_layout.addWidget(main_window.squeeze_1caller_label, 0, 2)
    
    squeeze_settings_layout.addWidget(QLabel("Squeeze vs Multiple Callers (%):"), 1, 0)
    main_window.squeeze_multi_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.squeeze_multi_slider.setRange(0, 100)
    main_window.squeeze_multi_slider.setValue(8)
    main_window.squeeze_multi_label = QLabel("8")
    main_window.squeeze_multi_slider.valueChanged.connect(lambda v: main_window.squeeze_multi_label.setText(str(v)))
    squeeze_settings_layout.addWidget(main_window.squeeze_multi_slider, 1, 1)
    squeeze_settings_layout.addWidget(main_window.squeeze_multi_label, 1, 2)
    
    squeeze_settings_layout.addWidget(QLabel("Squeeze Sizing (x pot):"), 2, 0)
    main_window.squeeze_sizing_combo = QComboBox()
    main_window.squeeze_sizing_combo.addItems(["2.5", "3.0", "3.5", "4.0"])
    main_window.squeeze_sizing_combo.setCurrentIndex(1)  # Default to 3.0
    squeeze_settings_layout.addWidget(main_window.squeeze_sizing_combo, 2, 1)
    
    squeeze_settings_layout.addWidget(QLabel("Blinds Squeeze Adjust (%):"), 3, 0)
    main_window.blinds_squeeze_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.blinds_squeeze_slider.setRange(0, 100)
    main_window.blinds_squeeze_slider.setValue(25)
    main_window.blinds_squeeze_label = QLabel("25")
    main_window.blinds_squeeze_slider.valueChanged.connect(lambda v: main_window.blinds_squeeze_label.setText(str(v)))
    squeeze_settings_layout.addWidget(main_window.blinds_squeeze_slider, 3, 1)
    squeeze_settings_layout.addWidget(main_window.blinds_squeeze_label, 3, 2)
    
    squeeze_settings_layout.addWidget(QLabel("Button Squeeze Adjust (%):"), 4, 0)
    main_window.btn_squeeze_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.btn_squeeze_slider.setRange(0, 100)
    main_window.btn_squeeze_slider.setValue(20)
    main_window.btn_squeeze_label = QLabel("20")
    main_window.btn_squeeze_slider.valueChanged.connect(lambda v: main_window.btn_squeeze_label.setText(str(v)))
    squeeze_settings_layout.addWidget(main_window.btn_squeeze_slider, 4, 1)
    squeeze_settings_layout.addWidget(main_window.btn_squeeze_label, 4, 2)
    
    squeeze_layout.addWidget(squeeze_group)
    
    # Ajouter l'onglet Squeeze
    preflop_tabs.addTab(squeeze_tab, "Squeeze")
    
    return preflop_scroll
