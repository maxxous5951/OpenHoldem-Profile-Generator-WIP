"""
Fonctions utilitaires pour l'application OpenHoldem Profile Generator
"""
import os

def load_stylesheet():
    """
    Charge la feuille de style CSS pour l'application
    
    Returns:
        str: Contenu de la feuille de style
    """
    # Le style était inclus directement dans main.py, nous le retournons ici
    return """
        QWidget {
            background-color: #14131B;
            color: #FFFFFF;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        QMainWindow, QDialog {
            background-color: #14131B;
        }
        
        QPushButton {
            background-color: #0a522c;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #9632E3;
        }
        
        QPushButton:pressed {
            background-color: #6215A3;
        }
        
        QLineEdit, QTextEdit, QComboBox {
            border: 1px solid #3F3D56;
            border-radius: 4px;
            padding: 6px;
            background-color: #1E1D2A;
            color: white;
        }
        
        QTextEdit {
            background-color: #1E1D2A;
        }
        
        QTabWidget::pane {
            border: 1px solid #3F3D56;
            background-color: #14131B;
        }
        
        QTabBar::tab {
            background-color: #1E1D2A;
            color: white;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected {
            background-color: #0a522c;
        }
        
        QGroupBox {
            border: 1px solid #3F3D56;
            border-radius: 4px;
            margin-top: 16px;
            padding-top: 16px;
            color: white;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 10px;
            background-color: #14131B;
            color: white;
        }
        
        QSlider::groove:horizontal {
            border: none;
            height: 8px;
            background: #1E1D2A;
            margin: 2px 0;
            border-radius: 4px;
        }
        
        QSlider::handle:horizontal {
            background: #0a522c;
            border: none;
            width: 16px;
            height: 16px;
            margin: -4px 0;
            border-radius: 8px;
        }
        
        QScrollArea, QScrollBar {
            background-color: #14131B;
            border: none;
        }
        
        QScrollBar:vertical {
            background-color: #1E1D2A;
            width: 12px;
            margin: 0px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #3F3D56;
            min-height: 20px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #0a522c;
        }
        
        QScrollBar:horizontal {
            background-color: #1E1D2A;
            height: 12px;
            margin: 0px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #3F3D56;
            min-width: 20px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: #0a522c;
        }
        
        QScrollBar::add-line, QScrollBar::sub-line {
            width: 0px;
            height: 0px;
        }
        
        QLabel {
            color: white;
        }
    """

def create_directory_structure():
    """
    Crée la structure de répertoires pour l'application
    """
    # Liste des répertoires à créer
    directories = [
        "generators",
        "ui",
        "resources"
    ]
    
    # Créer les répertoires
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        
    # Créer les fichiers __init__.py
    open(os.path.join("generators", "__init__.py"), "a").close()
    open(os.path.join("ui", "__init__.py"), "a").close()
