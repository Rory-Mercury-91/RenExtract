# ui/window_manager.py
"""
Gestionnaire de fenêtres pour éviter les ouvertures multiples
"""
import tkinter as tk
from typing import Dict, Any, Optional
from infrastructure.logging.logging import log_message

class WindowManager:
    """Gestionnaire global des fenêtres pour éviter les ouvertures multiples"""
    
    _instance = None
    _active_windows = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WindowManager, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        """Retourne l'instance singleton du gestionnaire"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def register_window(self, window_id: str, window: tk.Toplevel) -> bool:
        """
        Enregistre une fenêtre et vérifie si elle est déjà ouverte
        
        Args:
            window_id: Identifiant unique de la fenêtre
            window: Instance de la fenêtre Tkinter
            
        Returns:
            True si la fenêtre a été enregistrée, False si elle existait déjà
        """
        try:
            # Vérifier si la fenêtre existe déjà et est encore active
            if window_id in self._active_windows:
                existing_window = self._active_windows[window_id]
                
                # Vérifier si la fenêtre est encore valide
                try:
                    if existing_window.winfo_exists():
                        # La fenêtre existe encore, la ramener au premier plan
                        existing_window.lift()
                        existing_window.focus_force()
                        log_message("INFO", f"Fenêtre '{window_id}' déjà ouverte - mise au premier plan", category="window_manager")
                        return False
                except tk.TclError:
                    # La fenêtre n'existe plus, on peut la supprimer de la liste
                    del self._active_windows[window_id]
            
            # Enregistrer la nouvelle fenêtre
            self._active_windows[window_id] = window
            
            # Configurer le callback de fermeture pour nettoyer automatiquement
            def cleanup_on_close():
                if window_id in self._active_windows:
                    del self._active_windows[window_id]
                    log_message("DEBUG", f"Fenêtre '{window_id}' fermée et nettoyée", category="window_manager")
            
            # Intercepter la fermeture de la fenêtre
            original_destroy = window.destroy
            def destroy_with_cleanup():
                cleanup_on_close()
                original_destroy()
            
            window.destroy = destroy_with_cleanup
            
            # Intercepter aussi la fermeture via le bouton X
            window.protocol("WM_DELETE_WINDOW", destroy_with_cleanup)
            
            log_message("DEBUG", f"Fenêtre '{window_id}' enregistrée", category="window_manager")
            return True
            
        except Exception as e:
            log_message("ERREUR", f"Erreur enregistrement fenêtre '{window_id}': {e}", category="window_manager")
            return False
    
    def unregister_window(self, window_id: str) -> bool:
        """
        Désenregistre une fenêtre
        
        Args:
            window_id: Identifiant de la fenêtre
            
        Returns:
            True si la fenêtre a été désenregistrée
        """
        try:
            if window_id in self._active_windows:
                del self._active_windows[window_id]
                log_message("DEBUG", f"Fenêtre '{window_id}' désenregistrée", category="window_manager")
                return True
            return False
        except Exception as e:
            log_message("ERREUR", f"Erreur désenregistrement fenêtre '{window_id}': {e}", category="window_manager")
            return False
    
    def is_window_open(self, window_id: str) -> bool:
        """
        Vérifie si une fenêtre est déjà ouverte
        
        Args:
            window_id: Identifiant de la fenêtre
            
        Returns:
            True si la fenêtre est ouverte et active
        """
        try:
            if window_id in self._active_windows:
                window = self._active_windows[window_id]
                return window.winfo_exists()
            return False
        except tk.TclError:
            # Fenêtre n'existe plus
            if window_id in self._active_windows:
                del self._active_windows[window_id]
            return False
        except Exception:
            return False
    
    def bring_to_front(self, window_id: str) -> bool:
        """
        Ramène une fenêtre au premier plan
        
        Args:
            window_id: Identifiant de la fenêtre
            
        Returns:
            True si la fenêtre a été ramenée au premier plan
        """
        try:
            if window_id in self._active_windows:
                window = self._active_windows[window_id]
                if window.winfo_exists():
                    window.lift()
                    window.focus_force()
                    return True
                else:
                    # Fenêtre n'existe plus, nettoyer
                    del self._active_windows[window_id]
            return False
        except Exception:
            return False
    
    def get_active_windows(self) -> Dict[str, tk.Toplevel]:
        """
        Retourne la liste des fenêtres actives
        
        Returns:
            Dictionnaire des fenêtres actives
        """
        # Nettoyer les fenêtres qui n'existent plus
        active_windows = {}
        for window_id, window in self._active_windows.items():
            try:
                if window.winfo_exists():
                    active_windows[window_id] = window
            except tk.TclError:
                pass  # Fenêtre n'existe plus
        
        self._active_windows = active_windows
        return active_windows.copy()
    
    def close_all_windows(self):
        """Ferme toutes les fenêtres enregistrées"""
        try:
            for window_id, window in list(self._active_windows.items()):
                try:
                    if window.winfo_exists():
                        window.destroy()
                except tk.TclError:
                    pass
            self._active_windows.clear()
            log_message("INFO", "Toutes les fenêtres fermées", category="window_manager")
        except Exception as e:
            log_message("ERREUR", f"Erreur fermeture fenêtres: {e}", category="window_manager")

# Instance globale
window_manager = WindowManager.get_instance()