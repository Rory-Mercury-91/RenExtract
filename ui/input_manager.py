# ui/input_manager.py
# Input Manager Component - VERSION SIMPLIFIÉE
# Created for RenExtract 

"""
Gestionnaire des modes d'entrée SIMPLIFIÉ
- Drag & Drop : géré par Header/Info/ButtonsFrame
- Ctrl+V : géré uniquement par ContentFrame
"""

import tkinter as tk
import os
from infrastructure.logging.logging import log_message

class InputManager:
    """Gestionnaire simplifié des modes d'entrée"""
    
    def __init__(self, root, app_controller, text_area):
        self.root = root
        self.app_controller = app_controller
        self.text_area = text_area
        
        # Plus de switch de mode - configuration fixe
        self.input_mode = "hybrid"  # Mode hybride fixe
        self.dnd_available = self._check_dnd_availability()
        
        # Configuration immédiate
        self.configure_hybrid_mode()
    
    def _check_dnd_availability(self):
        """Vérifie la disponibilité du Drag & Drop"""
        try:
            import tkinterdnd2
            return True
        except ImportError:
            return False
    
    def configure_hybrid_mode(self):
        """Configure le mode hybride fixe"""
        # Configurer Ctrl+V UNIQUEMENT sur la zone de texte
        self._setup_ctrl_v_on_text_area()
        
        # Le Drag & Drop est géré par les autres composants (Header/Info/Buttons)
        # Plus besoin de le configurer ici
        
        
    
    def _setup_ctrl_v_on_text_area(self):
        """Configure Ctrl+V UNIQUEMENT sur la zone de texte"""
        try:
            if self.text_area:
                # Activer Ctrl+V sur la zone de texte
                self.text_area.bind('<Control-v>', self._handle_paste)
                self.text_area.bind('<Control-V>', self._handle_paste)
                
                # Désactiver tout Drag & Drop existant sur la zone de texte
                self._disable_drag_drop_on_text_area()
                
                
                
        except Exception as e:
            log_message("ATTENTION", f"Erreur configuration Ctrl+V: {e}", category="ui_input")
    
    def _disable_drag_drop_on_text_area(self):
        """Désactive le Drag & Drop sur la zone de texte"""
        try:
            if self.text_area and self.dnd_available:
                # Supprimer tous les bindings DnD existants
                dnd_events = ['<<Drop>>', '<<DragEnter>>', '<<DragLeave>>']
                for event in dnd_events:
                    try:
                        self.text_area.unbind(event)
                    except Exception:
                        pass
                
                # Désenregistrer le drop target si il existe
                try:
                    if hasattr(self.text_area, 'drop_target_unregister'):
                        self.text_area.drop_target_unregister()
                except Exception:
                    pass
                    
                
                
        except Exception as e:
            log_message("ATTENTION", f"Erreur désactivation D&D zone de texte: {e}", category="ui_input")
    
    def _handle_paste(self, event=None):
        """Gère le collage Ctrl+V - DÉLÈGUE au ContentFrame"""
        try:
            # Récupérer le ContentFrame
            content_frame = self.app_controller.main_window.get_component('content')
            if content_frame and hasattr(content_frame, '_handle_paste'):
                # Déléguer au ContentFrame qui a toute la logique
                return content_frame._handle_paste(event)
            else:
                # Fallback : utiliser l'ancienne méthode directe
                return self._handle_paste_fallback(event)
                
        except Exception as e:
            log_message("ERREUR", f"Erreur dans handle_paste InputManager: {e}", category="ui_input")
            return "break"
    
    def _handle_paste_fallback(self, event=None):
        """Méthode de fallback pour le collage"""
        try:
            # Récupérer le presse-papier
            try:
                clipboard_content = self.root.clipboard_get()
            except tk.TclError:
                if hasattr(self.app_controller, 'show_notification'):
                    self.app_controller.show_notification("Presse-papier vide", 'TOAST')
                return "break"
            
            if not clipboard_content or not clipboard_content.strip():
                if hasattr(self.app_controller, 'show_notification'):
                    self.app_controller.show_notification("Presse-papier vide", 'TOAST')
                return "break"
            
            # Déléguer à l'app controller
            if hasattr(self.app_controller, 'load_from_clipboard'):
                self.app_controller.load_from_clipboard(clipboard_content)
            
            return "break"
            
        except Exception as e:
            log_message("ERREUR", f"Erreur lors du collage fallback: {e}", category="ui_input")
            return "break"
    
    # =============================================================================
    # MÉTHODES DE COMPATIBILITÉ (simplifiées)
    # =============================================================================
    
    def toggle_input_mode(self):
        """Compatibilité - plus de toggle, mode fixe"""
        log_message("INFO", "Mode hybride fixe - pas de toggle disponible", category="ui_input")
        # Ne rien faire, le mode est fixe
    
    def get_current_mode(self):
        """Retourne le mode actuel (toujours hybride)"""
        return "hybrid"
    
    def is_dnd_available(self):
        """Retourne si le D&D est disponible"""
        return self.dnd_available
    
    def update_text_area(self, text_area):
        """Met à jour la référence à la zone de texte"""
        self.text_area = text_area
        self.configure_hybrid_mode()
    
    # =============================================================================
    # MÉTHODES PUBLIQUES POUR INTÉGRATION
    # =============================================================================
    
    def setup_global_drag_drop(self, target_components):
        """Configure le drag & drop global sur les composants cibles"""
        try:
            if not self.dnd_available:
                log_message("INFO", "Drag & Drop non disponible - configuration globale ignorée", category="ui_input")
                return
            
            # Déléguer la configuration D&D aux composants eux-mêmes
            for component_name, component in target_components.items():
                if hasattr(component, '_setup_drag_drop'):
                    try:
                        component._setup_drag_drop()
                        
                    except Exception as e:
                        log_message("ATTENTION", f"Erreur D&D {component_name}: {e}", category="ui_input")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur configuration D&D global: {e}", category="ui_input")
    
    def force_ctrl_v_only_on_content(self):
        """Force le mode Ctrl+V uniquement sur la zone de contenu - VERSION CORRIGÉE"""
        try:
            # ✅ CORRECTION : Vérifier que main_window existe avant d'appeler get_component
            if not hasattr(self.app_controller, 'main_window') or self.app_controller.main_window is None:
                log_message("ATTENTION", "main_window non disponible dans force_ctrl_v_only_on_content", category="ui_input")
                return
            
            # ✅ CORRECTION : Vérifier que get_component existe
            main_window = self.app_controller.main_window
            if not hasattr(main_window, 'get_component'):
                log_message("ATTENTION", "get_component non disponible dans force_ctrl_v_only_on_content", category="ui_input")
                return
            
            content_frame = main_window.get_component('content')
            if content_frame and hasattr(content_frame, 'force_ctrl_v_mode'):
                content_frame.force_ctrl_v_mode()
                log_message("DEBUG", "Mode Ctrl+V forcé sur ContentFrame", category="ui_input")
            else:
                log_message("DEBUG", "ContentFrame non trouvé ou sans méthode force_ctrl_v_mode", category="ui_input")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur dans force_ctrl_v_only_on_content: {e}", category="ui_input")
    
    def get_status_info(self):
        """Retourne les informations de statut pour l'interface"""
        return {
            "mode": "hybrid",
            "dnd_available": self.dnd_available,
            "dnd_zones": ["Header", "InfoFrame", "ButtonsFrame"],
            "ctrl_v_zone": "ContentFrame"
        }
    
    def debug_current_state(self):
        """Affiche l'état actuel pour le débogage"""
        try:
            state_info = {
                "input_mode": self.input_mode,
                "dnd_available": self.dnd_available,
                "text_area_exists": bool(self.text_area),
                "app_controller_exists": bool(self.app_controller)
            }
            log_message("DEBUG", f"InputManager state: {state_info}", category="ui_input")
        except Exception as e:
            log_message("ATTENTION", f"Erreur debug state InputManager: {e}", category="ui_input")


# =============================================================================
# FONCTIONS UTILITAIRES POUR L'INTÉGRATION
# =============================================================================

def setup_hybrid_input_system(main_window, app_controller):
    """Configure le système d'entrée hybride complet - VERSION ULTRA-SÉCURISÉE"""
    try:
        # ✅ CORRECTION : Vérifications robustes
        if main_window is None:
            log_message("ERREUR", "main_window est None dans setup_hybrid_input_system", category="ui_input")
            return
            
        if not hasattr(main_window, 'get_component'):
            log_message("ERREUR", "main_window n'a pas de méthode get_component", category="ui_input")
            return
        
        if not hasattr(main_window, 'components'):
            log_message("ERREUR", "main_window n'a pas d'attribut components", category="ui_input")
            return
        
        # Récupérer les composants avec vérification
        components = {}
        component_names = ['header', 'info', 'buttons', 'content', 'input']
        
        for comp_name in component_names:
            try:
                component = main_window.get_component(comp_name)
                if component is not None:
                    components[comp_name] = component
                else:
                    log_message("ATTENTION", f"Composant {comp_name} est None", category="ui_input")
            except Exception as e:
                log_message("ERREUR", f"Erreur récupération composant {comp_name}: {e}", category="ui_input")
                components[comp_name] = None
        
        # Vérifier qu'on a au moins les composants essentiels
        essential_components = ['input', 'content']
        missing_essential = [name for name in essential_components 
                           if components.get(name) is None]
        
        if missing_essential:
            log_message("ERREUR", f"Composants essentiels manquants: {missing_essential}", category="ui_input")
            return
        
        # Configurer le D&D global (délégué aux composants) seulement si les composants existent
        input_manager = components.get('input')
        if input_manager and hasattr(input_manager, 'setup_global_drag_drop'):
            valid_components = {name: comp for name, comp in components.items() 
                              if comp is not None and name in ['header', 'info', 'buttons']}
            
            if valid_components:
                input_manager.setup_global_drag_drop(valid_components)
            else:
                log_message("ATTENTION", "Aucun composant valide pour le D&D global", category="ui_input")
        
        # ✅ CORRECTION : Forcer Ctrl+V directement sur le composant au lieu de passer par main_window
        content_frame = components.get('content')
        if content_frame and hasattr(content_frame, 'force_ctrl_v_mode'):
            content_frame.force_ctrl_v_mode()
            
        elif input_manager and hasattr(input_manager, 'force_ctrl_v_only_on_content'):
            # Fallback : utiliser la méthode de l'input_manager
            input_manager.force_ctrl_v_only_on_content()
        
    except Exception as e:
        log_message("ERREUR", f"Erreur configuration système hybride: {e}", category="ui_input")

def get_input_status_message(input_manager):
    """Génère un message de statut pour l'interface utilisateur"""
    if not input_manager:
        return "Gestionnaire d'entrée non disponible"
    
    status = input_manager.get_status_info()
    
    if status['dnd_available']:
        return f"🎯 Mode D&D et Ctrl+V actif"
    else:
        return f"⌨️ Mode Ctrl+V uniquement - D&D non disponible"