"""
Module de gestion des profils pour OpenHoldem Profile Generator
"""
from player_profiles import PlayerProfiles

class ProfileManager:
    """
    Classe qui gère l'application des profils au générateur OpenHoldem
    """
    
    def __init__(self, main_window):
        """
        Initialise le gestionnaire de profils
        
        Args:
            main_window (OpenHoldemProfileGenerator): Référence à la fenêtre principale
        """
        self.main_window = main_window
        self.current_profile = None
        self.aggression_adjustments = {
            "Standard": 0,
            "More aggressive(+15%)": 15,
            "less aggressive (-15%)": -15,
            "Very aggressive(+30%)": 30,
            "Very careful (-30%)": -30
        }
        self.stack_adjustments = {
            "Standard": {
                "ip_3bet_adjust": 0,
                "threebet_frequency": 0,
                "fourbet_frequency": 0,
                "squeeze_frequency": 0,
                "limp_frequency": 0
            },
            "Big Stack (>50BB)": {
                "ip_3bet_adjust": 10,
                "threebet_frequency": 10,
                "fourbet_frequency": 5,
                "squeeze_frequency": 10,
                "limp_frequency": 5
            },
            "Medium Stack (25-50BB)": {
                "ip_3bet_adjust": 5,
                "threebet_frequency": 5,
                "fourbet_frequency": 0,
                "squeeze_frequency": 5,
                "limp_frequency": -5
            },
            "Small Stack (10-25BB)": {
                "ip_3bet_adjust": -5,
                "threebet_frequency": -5,
                "fourbet_frequency": -5,
                "squeeze_frequency": -10,
                "limp_frequency": -10
            },
            "Short Stack (<10BB)": {
                "ip_3bet_adjust": -15,
                "threebet_frequency": -15,
                "fourbet_frequency": -10,
                "squeeze_frequency": -15,
                "limp_frequency": -15
            }
        }
    
    def apply_profile(self, profile_info):
        """
        Applique un profil sélectionné à la fenêtre principale
        
        Args:
            profile_info (dict): Informations sur le profil à appliquer
        """
        if not profile_info:
            return
            
        profile_name = profile_info.get("profile_name")
        stack_adjustment = profile_info.get("stack_adjustment", "Standard")
        aggression_adjustment = profile_info.get("aggression_adjustment", "Standard")
        
        # Obtenir les paramètres de base du profil
        profile_data = PlayerProfiles.get_profile(profile_name)
        if not profile_data:
            return
            
        # Stocker le profil actuel
        self.current_profile = profile_name
        
        # Appliquer les ajustements selon le stack (si applicable)
        if stack_adjustment in self.stack_adjustments:
            for param, adjust in self.stack_adjustments[stack_adjustment].items():
                if param in profile_data:
                    profile_data[param] += adjust
        
        # Appliquer les ajustements d'agressivité
        aggression_adjust = self.aggression_adjustments.get(aggression_adjustment, 0)
        if aggression_adjust != 0:
            # Paramètres liés à l'agressivité
            agg_params = [
                "aggression", "threebet_frequency", "fourbet_frequency", 
                "squeeze_frequency", "ip_3bet_adjust", "vs_lp_3bet_adjust",
                "short_stack_4bet", "blinds_squeeze", "btn_squeeze"
            ]
            
            for param in agg_params:
                if param in profile_data:
                    new_value = profile_data[param] + aggression_adjust
                    # S'assurer que les valeurs restent dans des limites raisonnables
                    profile_data[param] = max(0, min(100, new_value))
        
        # Appliquer tous les paramètres du profil aux contrôles de l'interface
        self._apply_profile_to_ui(profile_data)
        
        # Informer l'utilisateur
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(
            self.main_window, 
            "Applied profile", 
            f"The profile {profile_name} has been successfully applied.\n\n"
            f"Stack adjustment: {stack_adjustment}\n"
            f"Aggression adjustment: {aggression_adjustment}"
        )
    
    def _apply_profile_to_ui(self, profile_data):
        """
        Applique les paramètres du profil à l'interface utilisateur
        
        Args:
            profile_data (dict): Données du profil à appliquer
        """
        # Mise à jour des sliders et combobox de l'interface
        
        # Paramètres généraux preflop
        if hasattr(self.main_window, "aggression_slider"):
            self.main_window.aggression_slider.setValue(profile_data.get("aggression", 50))
        
        if hasattr(self.main_window, "tightness_slider"):
            self.main_window.tightness_slider.setValue(profile_data.get("tightness", 50))
        
        if hasattr(self.main_window, "limp_frequency_slider"):
            self.main_window.limp_frequency_slider.setValue(profile_data.get("limp_frequency", 30))
        
        if hasattr(self.main_window, "threebet_frequency_slider"):
            self.main_window.threebet_frequency_slider.setValue(profile_data.get("threebet_frequency", 40))
        
        if hasattr(self.main_window, "fourbet_frequency_slider"):
            self.main_window.fourbet_frequency_slider.setValue(profile_data.get("fourbet_frequency", 30))
        
        if hasattr(self.main_window, "squeeze_frequency_slider"):
            self.main_window.squeeze_frequency_slider.setValue(profile_data.get("squeeze_frequency", 35))
        
        # Ranges détaillées par position
        self._update_slider_if_exists("ep1_range_slider", profile_data.get("ep1_range", 10))
        self._update_slider_if_exists("ep2_range_slider", profile_data.get("ep2_range", 12))
        self._update_slider_if_exists("ep3_range_slider", profile_data.get("ep3_range", 14))
        self._update_slider_if_exists("mp1_range_slider", profile_data.get("mp1_range", 16))
        self._update_slider_if_exists("mp2_range_slider", profile_data.get("mp2_range", 18))
        self._update_slider_if_exists("mp3_range_slider", profile_data.get("mp3_range", 20))
        self._update_slider_if_exists("co_range_slider", profile_data.get("co_range", 25))
        self._update_slider_if_exists("btn_range_slider", profile_data.get("btn_range", 30))
        self._update_slider_if_exists("sb_range_slider", profile_data.get("sb_range", 35))
        self._update_slider_if_exists("bb_range_slider", profile_data.get("bb_range", 40))
        
        # Sizing preflop par position
        self._update_combo_if_exists("ep1_sizing_combo", profile_data.get("ep1_sizing", "3.0"))
        self._update_combo_if_exists("ep2_sizing_combo", profile_data.get("ep2_sizing", "3.0"))
        self._update_combo_if_exists("ep3_sizing_combo", profile_data.get("ep3_sizing", "3.0"))
        self._update_combo_if_exists("mp1_sizing_combo", profile_data.get("mp1_sizing", "2.5"))
        self._update_combo_if_exists("mp2_sizing_combo", profile_data.get("mp2_sizing", "2.5"))
        self._update_combo_if_exists("mp3_sizing_combo", profile_data.get("mp3_sizing", "2.5"))
        self._update_combo_if_exists("co_sizing_combo", profile_data.get("co_sizing", "2.5"))
        self._update_combo_if_exists("btn_sizing_combo", profile_data.get("btn_sizing", "2.5"))
        self._update_combo_if_exists("sb_sizing_combo", profile_data.get("sb_sizing", "2.5"))
        
        # Autres paramètres preflop
        self._update_slider_if_exists("call_3bet_range_slider", profile_data.get("call_3bet_range", 15))
        self._update_slider_if_exists("fourbet_range_slider", profile_data.get("fourbet_range", 8))
        self._update_slider_if_exists("ip_3bet_adjust_slider", profile_data.get("ip_3bet_adjust", 20))
        self._update_slider_if_exists("vs_lp_3bet_adjust_slider", profile_data.get("vs_lp_3bet_adjust", 15))
        self._update_slider_if_exists("call_4bet_range_slider", profile_data.get("call_4bet_range", 5))
        self._update_slider_if_exists("fivebet_range_slider", profile_data.get("fivebet_range", 3))
        self._update_slider_if_exists("short_stack_4bet_slider", profile_data.get("short_stack_4bet", 30))
        self._update_slider_if_exists("squeeze_1caller_slider", profile_data.get("squeeze_1caller", 12))
        self._update_slider_if_exists("squeeze_multi_slider", profile_data.get("squeeze_multi", 8))
        self._update_combo_if_exists("squeeze_sizing_combo", profile_data.get("squeeze_sizing", "3.0"))
        self._update_slider_if_exists("blinds_squeeze_slider", profile_data.get("blinds_squeeze", 25))
        self._update_slider_if_exists("btn_squeeze_slider", profile_data.get("btn_squeeze", 20))
        
    def _update_slider_if_exists(self, slider_name, value):
        """
        Met à jour un slider s'il existe
        
        Args:
            slider_name (str): Nom du slider
            value (int): Nouvelle valeur
        """
        if hasattr(self.main_window, slider_name):
            slider = getattr(self.main_window, slider_name)
            slider.setValue(value)
    
    def _update_combo_if_exists(self, combo_name, value):
        """
        Met à jour une combobox si elle existe
        
        Args:
            combo_name (str): Nom de la combobox
            value (str): Nouvelle valeur
        """
        if hasattr(self.main_window, combo_name):
            combo = getattr(self.main_window, combo_name)
            index = combo.findText(value)
            if index >= 0:
                combo.setCurrentIndex(index)