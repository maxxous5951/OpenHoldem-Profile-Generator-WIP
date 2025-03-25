"""
Onglet des paramètres preflop pour l'application OpenHoldem Profile Generator
"""
from PyQt6.QtWidgets import (QGridLayout, QLabel, QSlider, QComboBox, 
                            QGroupBox)
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
    
    # Create Open Raise frame
    openraise_group = QGroupBox("Open Raise Ranges")
    openraise_layout = QGridLayout(openraise_group)
    
    # EP range
    openraise_layout.addWidget(QLabel("Early Position Range (%):"), 0, 0)
    main_window.ep_range_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.ep_range_slider.setRange(0, 100)
    main_window.ep_range_slider.setValue(15)
    main_window.ep_range_label = QLabel("15")
    main_window.ep_range_slider.valueChanged.connect(lambda v: main_window.ep_range_label.setText(str(v)))
    openraise_layout.addWidget(main_window.ep_range_slider, 0, 1)
    openraise_layout.addWidget(main_window.ep_range_label, 0, 2)
    
    # MP range
    openraise_layout.addWidget(QLabel("Middle Position Range (%):"), 1, 0)
    main_window.mp_range_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.mp_range_slider.setRange(0, 100)
    main_window.mp_range_slider.setValue(20)
    main_window.mp_range_label = QLabel("20")
    main_window.mp_range_slider.valueChanged.connect(lambda v: main_window.mp_range_label.setText(str(v)))
    openraise_layout.addWidget(main_window.mp_range_slider, 1, 1)
    openraise_layout.addWidget(main_window.mp_range_label, 1, 2)
    
    # LP range
    openraise_layout.addWidget(QLabel("Late Position Range (%):"), 2, 0)
    main_window.lp_range_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.lp_range_slider.setRange(0, 100)
    main_window.lp_range_slider.setValue(30)
    main_window.lp_range_label = QLabel("30")
    main_window.lp_range_slider.valueChanged.connect(lambda v: main_window.lp_range_label.setText(str(v)))
    openraise_layout.addWidget(main_window.lp_range_slider, 2, 1)
    openraise_layout.addWidget(main_window.lp_range_label, 2, 2)
    
    preflop_layout.addWidget(openraise_group)
    
    # Open Raise sizing
    sizing_group = QGroupBox("Position-Based Sizing")
    sizing_layout = QGridLayout(sizing_group)
    
    sizing_layout.addWidget(QLabel("EP Sizing (BB):"), 0, 0)
    main_window.ep_sizing_combo = QComboBox()
    main_window.ep_sizing_combo.addItems(["2.5", "3.0", "3.5", "4.0"])
    main_window.ep_sizing_combo.setCurrentIndex(1)  # Default to 3.0
    sizing_layout.addWidget(main_window.ep_sizing_combo, 0, 1)
    
    sizing_layout.addWidget(QLabel("MP Sizing (BB):"), 1, 0)
    main_window.mp_sizing_combo = QComboBox()
    main_window.mp_sizing_combo.addItems(["2.2", "2.5", "2.8", "3.0"])
    main_window.mp_sizing_combo.setCurrentIndex(2)  # Default to 2.8
    sizing_layout.addWidget(main_window.mp_sizing_combo, 1, 1)
    
    sizing_layout.addWidget(QLabel("LP Sizing (BB):"), 2, 0)
    main_window.lp_sizing_combo = QComboBox()
    main_window.lp_sizing_combo.addItems(["2.0", "2.2", "2.5", "2.8"])
    main_window.lp_sizing_combo.setCurrentIndex(2)  # Default to 2.5
    sizing_layout.addWidget(main_window.lp_sizing_combo, 2, 1)
    
    preflop_layout.addWidget(sizing_group)
    
    # 3-Bet Defense
    threebet_group = QGroupBox("3-Bet Defense")
    threebet_layout = QGridLayout(threebet_group)
    
    threebet_layout.addWidget(QLabel("Call 3-Bet Range (%):"), 0, 0)
    main_window.call_3bet_range_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.call_3bet_range_slider.setRange(0, 100)
    main_window.call_3bet_range_slider.setValue(15)
    main_window.call_3bet_range_label = QLabel("15")
    main_window.call_3bet_range_slider.valueChanged.connect(lambda v: main_window.call_3bet_range_label.setText(str(v)))
    threebet_layout.addWidget(main_window.call_3bet_range_slider, 0, 1)
    threebet_layout.addWidget(main_window.call_3bet_range_label, 0, 2)
    
    threebet_layout.addWidget(QLabel("4-Bet Range (%):"), 1, 0)
    main_window.fourbet_range_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.fourbet_range_slider.setRange(0, 100)
    main_window.fourbet_range_slider.setValue(8)
    main_window.fourbet_range_label = QLabel("8")
    main_window.fourbet_range_slider.valueChanged.connect(lambda v: main_window.fourbet_range_label.setText(str(v)))
    threebet_layout.addWidget(main_window.fourbet_range_slider, 1, 1)
    threebet_layout.addWidget(main_window.fourbet_range_label, 1, 2)
    
    preflop_layout.addWidget(threebet_group)
    
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
    
    preflop_layout.addWidget(position_adj_group)
    
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
    
    preflop_layout.addWidget(fourbet_group)
    
    # Squeeze settings
    squeeze_group = QGroupBox("Squeeze Settings")
    squeeze_layout = QGridLayout(squeeze_group)
    
    squeeze_layout.addWidget(QLabel("Squeeze vs 1 Caller (%):"), 0, 0)
    main_window.squeeze_1caller_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.squeeze_1caller_slider.setRange(0, 100)
    main_window.squeeze_1caller_slider.setValue(12)
    main_window.squeeze_1caller_label = QLabel("12")
    main_window.squeeze_1caller_slider.valueChanged.connect(lambda v: main_window.squeeze_1caller_label.setText(str(v)))
    squeeze_layout.addWidget(main_window.squeeze_1caller_slider, 0, 1)
    squeeze_layout.addWidget(main_window.squeeze_1caller_label, 0, 2)
    
    squeeze_layout.addWidget(QLabel("Squeeze vs Multiple Callers (%):"), 1, 0)
    main_window.squeeze_multi_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.squeeze_multi_slider.setRange(0, 100)
    main_window.squeeze_multi_slider.setValue(8)
    main_window.squeeze_multi_label = QLabel("8")
    main_window.squeeze_multi_slider.valueChanged.connect(lambda v: main_window.squeeze_multi_label.setText(str(v)))
    squeeze_layout.addWidget(main_window.squeeze_multi_slider, 1, 1)
    squeeze_layout.addWidget(main_window.squeeze_multi_label, 1, 2)
    
    squeeze_layout.addWidget(QLabel("Squeeze Sizing (x pot):"), 2, 0)
    main_window.squeeze_sizing_combo = QComboBox()
    main_window.squeeze_sizing_combo.addItems(["2.5", "3.0", "3.5", "4.0"])
    main_window.squeeze_sizing_combo.setCurrentIndex(1)  # Default to 3.0
    squeeze_layout.addWidget(main_window.squeeze_sizing_combo, 2, 1)
    
    squeeze_layout.addWidget(QLabel("Blinds Squeeze Adjust (%):"), 3, 0)
    main_window.blinds_squeeze_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.blinds_squeeze_slider.setRange(0, 100)
    main_window.blinds_squeeze_slider.setValue(25)
    main_window.blinds_squeeze_label = QLabel("25")
    main_window.blinds_squeeze_slider.valueChanged.connect(lambda v: main_window.blinds_squeeze_label.setText(str(v)))
    squeeze_layout.addWidget(main_window.blinds_squeeze_slider, 3, 1)
    squeeze_layout.addWidget(main_window.blinds_squeeze_label, 3, 2)
    
    squeeze_layout.addWidget(QLabel("Button Squeeze Adjust (%):"), 4, 0)
    main_window.btn_squeeze_slider = QSlider(Qt.Orientation.Horizontal)
    main_window.btn_squeeze_slider.setRange(0, 100)
    main_window.btn_squeeze_slider.setValue(20)
    main_window.btn_squeeze_label = QLabel("20")
    main_window.btn_squeeze_slider.valueChanged.connect(lambda v: main_window.btn_squeeze_label.setText(str(v)))
    squeeze_layout.addWidget(main_window.btn_squeeze_slider, 4, 1)
    squeeze_layout.addWidget(main_window.btn_squeeze_label, 4, 2)
    
    preflop_layout.addWidget(squeeze_group)
    
    return preflop_scroll