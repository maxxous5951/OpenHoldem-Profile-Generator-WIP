"""
Classe de base abstraite pour les générateurs river
"""
from abc import ABC, abstractmethod

class BaseRiverGenerator(ABC):
    """
    Classe abstraite fournissant des fonctionnalités communes à tous les générateurs river
    """
    
    def get_handrank_threshold(self, percentage):
        """
        Convertit un pourcentage en une valeur de seuil de handrank
        
        Args:
            percentage (float): Pourcentage de mains à jouer (0-100)
            
        Returns:
            int: Valeur de seuil handrank169 (1-169)
        """
        # HandRank va de 1 à 169, où 1 est la meilleure main (AA)
        # Convertir un pourcentage en une valeur de rang
        # 0% = uniquement AA (rang 1)
        # 100% = toutes les mains (rang 169)
        return round(1 + (percentage / 100) * 168)
    
    @abstractmethod
    def generate_code(self, settings):
        """
        Méthode abstraite pour générer le code de profil
        
        Args:
            settings (dict): Paramètres du générateur
            
        Returns:
            str: Code de profil généré
        """
        pass
