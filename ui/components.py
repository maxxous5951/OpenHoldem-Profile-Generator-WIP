"""
Composants d'interface utilisateur réutilisables pour l'application
"""
from PyQt6.QtWidgets import (QGroupBox, QGridLayout, QSlider, QLabel, 
                          QScrollArea, QWidget, QVBoxLayout)
from PyQt6.QtCore import Qt

def create_slider_with_label(min_val, max_val, default_val, callback=None):
    """
    Crée un slider avec une étiquette affichant sa valeur
    
    Args:
        min_val (int): Valeur minimale
        max_val (int): Valeur maximale
        default_val (int): Valeur par défaut
        callback (function, optional): Fonction à appeler lorsque la valeur change
    
    Returns:
        tuple: (QSlider, QLabel, QLabel) - Le slider, son label de valeur, et son label de description
    """
    slider = QSlider(Qt.Orientation.Horizontal)
    slider.setRange(min_val, max_val)
    slider.setValue(default_val)
    
    label = QLabel(str(default_val))
    
    desc_label = QLabel("")
    
    if callback:
        slider.valueChanged.connect(lambda v: (label.setText(str(v)), callback(v)))
    else:
        slider.valueChanged.connect(lambda v: label.setText(str(v)))
    
    return slider, label, desc_label

def create_scroll_area():
    """
    Crée une zone de défilement standard
    
    Returns:
        tuple: (QScrollArea, QWidget, QVBoxLayout) - La zone de défilement, son widget et son layout
    """
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    scroll_area.setWidget(widget)
    
    return scroll_area, widget, layout

def create_push_fold_position_frame(title, position_vars):
    """
    Crée un cadre avec des sliders pour chaque position dans le jeu push/fold
    
    Args:
        title (str): Titre du cadre
        position_vars (dict): Dictionnaire de variables de position {position: (valeur, fonction setter)}
    
    Returns:
        QGroupBox: Cadre avec les sliders pour chaque position
    """
    frame = QGroupBox(title)
    layout = QGridLayout(frame)
    
    row = 0
    position_names = {
        "EP": "Early Position", 
        "MP": "Middle Position", 
        "CO": "Cutoff", 
        "BTN": "Button", 
        "SB": "Small Blind", 
        "BB": "Big Blind"
    }
    
    for pos, (value, setter) in position_vars.items():
        layout.addWidget(QLabel(f"{position_names.get(pos, pos)} (%):"), row, 0)
        
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(value)
        label = QLabel(str(value))
        
        # Connecter le changement de valeur pour mettre à jour à la fois l'étiquette et l'attribut
        slider.valueChanged.connect(lambda v, lbl=label, set_fn=setter: (lbl.setText(str(v)), set_fn(v)))
        
        layout.addWidget(slider, row, 1)
        layout.addWidget(label, row, 2)
        row += 1
    
    return frame

def create_push_fold_call_frame(title, position_vars):
    """
    Crée un cadre avec des sliders pour l'appel de chaque position dans le jeu push/fold
    
    Args:
        title (str): Titre du cadre
        position_vars (dict): Dictionnaire de variables de position {position: (valeur, fonction setter)}
    
    Returns:
        QGroupBox: Cadre avec les sliders pour chaque position
    """
    frame = QGroupBox(title)
    layout = QGridLayout(frame)
    
    row = 0
    position_names = {
        "vs_EP": "vs Early Position", 
        "vs_MP": "vs Middle Position", 
        "vs_CO": "vs Cutoff", 
        "vs_BTN": "vs Button", 
        "vs_SB": "vs Small Blind"
    }
    
    for pos, (value, setter) in position_vars.items():
        layout.addWidget(QLabel(f"{position_names.get(pos, pos)} (%):"), row, 0)
        
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(value)
        label = QLabel(str(value))
        
        # Connecter le changement de valeur pour mettre à jour à la fois l'étiquette et l'attribut
        slider.valueChanged.connect(lambda v, lbl=label, set_fn=setter: (lbl.setText(str(v)), set_fn(v)))
        
        layout.addWidget(slider, row, 1)
        layout.addWidget(label, row, 2)
        row += 1
    
    return frame
