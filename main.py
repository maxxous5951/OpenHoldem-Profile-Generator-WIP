import sys
from PyQt6.QtWidgets import QApplication, QStyleFactory
from ui.main_window import OpenHoldemProfileGenerator
from utils import load_stylesheet

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        
        # Définir le style Fusion comme base
        app.setStyle("Fusion")
        
        # Appliquer une feuille de style personnalisée avec un thème sombre/violet
        app.setStyleSheet(load_stylesheet())
        
        window = OpenHoldemProfileGenerator()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        import traceback
        print(f"An error occurred: {e}")
        print(traceback.format_exc())
        input("Press Enter to exit...")
