"""
Classe de base abstraite pour les générateurs preflop
"""
from abc import ABC, abstractmethod

class BaseProfileGenerator(ABC):
    """
    Classe abstraite fournissant des fonctionnalités communes à tous les générateurs preflop
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
    
    def calculate_raise_size(self, base_size, num_limpers=0, aggressive_factor=1.0):
        """
        Calcule la taille d'une relance en fonction de la taille de base 
        et du nombre de limpers, sans appliquer le facteur d'agressivité
        
        Args:
            base_size (str): Taille de base en BB
            num_limpers (int): Nombre de limpers
            aggressive_factor (float): Paramètre ignoré, gardé pour compatibilité
            
        Returns:
            float: Taille de la relance calculée
        """
        # Ajouter 1BB pour chaque limper
        size = float(base_size)
        if num_limpers > 0:
            size += num_limpers
        
        # Pas d'ajustement basé sur l'agressivité
        
        return round(size, 1)
        
    def get_position_map(self, num_players):
        """
        Renvoie une carte des positions qui existent en fonction du nombre de joueurs
        
        Args:
            num_players (int): Nombre de joueurs à la table
            
        Returns:
            dict: Dictionnaire des positions actives
        """
        positions = {
            "EP1": False,
            "EP2": False,
            "EP3": False,
            "MP1": False,
            "MP2": False,
            "MP3": False,
            "CO": False,
            "BTN": False,
            "SB": True,   # Toujours présent
            "BB": True    # Toujours présent
        }
        
        # Activer les positions en fonction du nombre de joueurs
        if num_players >= 3:
            positions["BTN"] = True
        
        if num_players >= 4:
            positions["CO"] = True
            
        if num_players >= 5:
            positions["MP3"] = True
            
        if num_players >= 6:
            positions["MP2"] = True
            
        if num_players >= 7:
            positions["MP1"] = True
            
        if num_players >= 8:
            positions["EP3"] = True
            
        if num_players >= 9:
            positions["EP2"] = True
            positions["EP1"] = True
            
        return positions
    
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
