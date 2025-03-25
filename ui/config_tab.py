"""
Onglet de configuration générale pour l'application OpenHoldem Profile Generator
"""
from PyQt6.QtWidgets import (QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QTextEdit, QGroupBox)
from ui.components import create_scroll_area

def create_config_tab(main_window):
    """
    Crée l'onglet de configuration principale
    
    Args:
        main_window (OpenHoldemProfileGenerator): Instance de la fenêtre principale
    
    Returns:
        QScrollArea: Zone de défilement contenant l'onglet de configuration
    """
    config_frame, config_widget, config_layout = create_scroll_area()
    
    # Game and strategy settings are removed as requested
    
    # Generate and save buttons
    btn_frame = QWidget()
    btn_layout = QHBoxLayout(btn_frame)
    btn_layout.setContentsMargins(0, 0, 0, 0)
    
    generate_btn = QPushButton("Generate Profile")
    generate_btn.clicked.connect(main_window.generate_profile)
    save_btn = QPushButton("Save Profile")
    save_btn.clicked.connect(main_window.save_profile)
    
    btn_layout.addWidget(generate_btn)
    btn_layout.addWidget(save_btn)
    btn_layout.addStretch(1)
    
    config_layout.addWidget(btn_frame)
    
    # Preview frame
    preview_group = QGroupBox("Preview")
    preview_layout = QVBoxLayout(preview_group)
    
    main_window.preview_text = QTextEdit()
    preview_layout.addWidget(main_window.preview_text)
    
    config_layout.addWidget(preview_group)
    
    return config_frame
