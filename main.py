"""
Version mise à jour du fichier main.py avec l'intégration
des fonctionnalités de profils prédéfinis
"""
import sys
from PyQt6.QtWidgets import QApplication, QStyleFactory, QScrollArea
from ui.main_window import OpenHoldemProfileGenerator
from utils import load_stylesheet

# Patch de la classe OpenHoldemProfileGenerator pour ajouter les fonctionnalités de profil
from ui.main_window import OpenHoldemProfileGenerator as OriginalGenerator

# Importer les nouvelles fonctionnalités
from profile_selector import ProfileSelector
from profile_manager import ProfileManager

# Appliquer le patch à la classe OpenHoldemProfileGenerator
def apply_profile_patch():
    """
    Ajoute les fonctionnalités de profil à la classe OpenHoldemProfileGenerator
    """
    # Ajouter les nouvelles méthodes à la classe
    OriginalGenerator.initialize_profile_manager = initialize_profile_manager
    OriginalGenerator.show_profile_selector = show_profile_selector
    OriginalGenerator.update_profile = update_profile
    
    # Sauvegarder la méthode create_ui originale
    original_create_ui = OriginalGenerator.create_ui
    
    # Redéfinir la méthode create_ui
    def new_create_ui(self):
        # Appeler la méthode originale
        original_create_ui(self)
        
        # Initialiser le gestionnaire de profils
        self.initialize_profile_manager()
        
        # Définir les méthodes à ajouter à la classe
def initialize_profile_manager(self):
    """
    Initialise le gestionnaire de profils
    """
    self.profile_manager = ProfileManager(self)
    self.current_profile = "Personnalisé"

def show_profile_selector(self):
    """
    Affiche le sélecteur de profils
    """
    selected_profile = ProfileSelector.get_profile(self)
    if selected_profile:
        self.update_profile(selected_profile)

def update_profile(self, profile_info):
    """
    Met à jour l'interface avec les paramètres du profil sélectionné
    
    Args:
        profile_info (dict): Informations sur le profil à appliquer
    """
    if profile_info:
        self.profile_manager.apply_profile(profile_info)
        self.current_profile = profile_info.get("profile_name", "Personnalisé")
        
        # Mettre à jour le label du profil actuel
        if hasattr(self, "profile_label"):
            self.profile_label.setText(f"Profil actuel: {self.current_profile}")

if __name__ == "__main__":
    try:
        # Appliquer le patch avant de créer l'application
        apply_profile_patch()
        
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
