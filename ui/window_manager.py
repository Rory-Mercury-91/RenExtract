# ui/window_manager.py
"""
Gestionnaire de fenêtres persistantes pour RenExtract
Cache les instances de fenêtres modales pour éviter de les recréer à chaque ouverture
Sauvegarde l'état des fenêtres sur disque pour persistance entre sessions
"""

import os
import json
from infrastructure.logging.logging import log_message
from infrastructure.config.constants import FOLDERS

class WindowManager:
    """Gestionnaire singleton de fenêtres persistantes avec sauvegarde d'état"""
    
    _instance = None
    
    def __new__(cls):
        """Pattern Singleton"""
        if cls._instance is None:
            cls._instance = super(WindowManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialise le gestionnaire (une seule fois)"""
        if self._initialized:
            return
        
        # Cache des fenêtres par nom
        self._windows = {}
        
        # Fichier de sauvegarde de l'état des fenêtres (utiliser "configs" avec 's')
        self._state_file = os.path.join(FOLDERS.get("configs", "."), "windows_state.json")
        
        # Charger l'état sauvegardé
        self._window_states = self._load_window_states()
        
        self._initialized = True
        
        # Log INFO visible
        if self._window_states:
            log_message("INFO", f"🪟 WindowManager initialisé : {len(self._window_states)} fenêtres restaurées", category="ui")
        else:
            log_message("INFO", "🪟 WindowManager initialisé : aucun état à restaurer", category="ui")
    
    def get_or_create_window(self, window_name: str, creator_func, *args, **kwargs):
        """
        Récupère une fenêtre existante ou la crée si nécessaire
        
        Args:
            window_name: Nom unique de la fenêtre (ex: 'backup', 'settings')
            creator_func: Fonction qui crée la fenêtre
            *args, **kwargs: Arguments pour creator_func
        
        Returns:
            Instance de la fenêtre (existante ou nouvelle)
        """
        # Vérifier si la fenêtre existe déjà
        if window_name in self._windows:
            window_instance = self._windows[window_name]
            
            # Vérifier que la fenêtre n'a pas été détruite
            if hasattr(window_instance, 'window') and window_instance.window:
                try:
                    # Tester si la fenêtre existe toujours
                    window_instance.window.winfo_exists()
                    log_message("DEBUG", f"Réutilisation fenêtre existante: {window_name}", category="ui")
                    return window_instance
                except:
                    # La fenêtre a été détruite, la supprimer du cache
                    log_message("DEBUG", f"Fenêtre {window_name} détruite, recréation nécessaire", category="ui")
                    del self._windows[window_name]
        
        # Créer une nouvelle fenêtre
        log_message("DEBUG", f"Création nouvelle fenêtre: {window_name}", category="ui")
        window_instance = creator_func(*args, **kwargs)
        
        # Stocker dans le cache
        self._windows[window_name] = window_instance
        log_message("DEBUG", f"Fenêtre '{window_name}' ajoutée au cache (total: {len(self._windows)})", category="ui")
        
        return window_instance
    
    def show_window(self, window_name: str, creator_func, *args, **kwargs):
        """
        Affiche une fenêtre (réutilise l'existante ou en crée une nouvelle)
        Restaure l'état sauvegardé si c'est la première création
        
        Args:
            window_name: Nom unique de la fenêtre
            creator_func: Fonction qui crée la fenêtre
            *args, **kwargs: Arguments pour creator_func
        """
        # Vérifier si c'est une nouvelle création
        is_new_window = window_name not in self._windows
        
        # Restaurer l'état AVANT de créer la fenêtre si possible
        # Cela évite le flash visuel de repositionnement
        will_restore_state = is_new_window and window_name in self._window_states
        
        window_instance = self.get_or_create_window(window_name, creator_func, *args, **kwargs)
        
        # Si nouvelle fenêtre ET état sauvegardé, restaurer AVANT d'afficher
        if will_restore_state and hasattr(window_instance, 'window'):
            # Restaurer la géométrie AVANT de rendre visible
            self.restore_window_state(window_name, window_instance)
        
        # Afficher la fenêtre
        if hasattr(window_instance, 'show'):
            window_instance.show()
                
        elif hasattr(window_instance, 'window'):
            # Ramener la fenêtre au premier plan si elle existe déjà
            try:
                window_instance.window.deiconify()  # Restaurer si minimisée
                window_instance.window.lift()       # Mettre au premier plan
                window_instance.window.focus_force() # Donner le focus
                log_message("DEBUG", f"Fenêtre {window_name} ramenée au premier plan", category="ui")
            except:
                # Si ça échoue, appeler show() si disponible
                if hasattr(window_instance, 'show'):
                    window_instance.show()
        
        return window_instance
    
    def close_window(self, window_name: str):
        """
        Ferme une fenêtre (la cache au lieu de la détruire)
        
        Args:
            window_name: Nom de la fenêtre à fermer
        """
        if window_name in self._windows:
            window_instance = self._windows[window_name]
            
            if hasattr(window_instance, 'window') and window_instance.window:
                try:
                    # Cacher la fenêtre au lieu de la détruire
                    window_instance.window.withdraw()
                    log_message("DEBUG", f"Fenêtre {window_name} cachée (persistante)", category="ui")
                except:
                    pass
    
    def destroy_window(self, window_name: str):
        """
        Détruit complètement une fenêtre (libère la mémoire)
        
        Args:
            window_name: Nom de la fenêtre à détruire
        """
        if window_name in self._windows:
            window_instance = self._windows[window_name]
            
            if hasattr(window_instance, 'window') and window_instance.window:
                try:
                    window_instance.window.destroy()
                    log_message("DEBUG", f"Fenêtre {window_name} détruite", category="ui")
                except:
                    pass
            
            # Supprimer du cache
            del self._windows[window_name]
    
    def clear_all_windows(self):
        """Détruit toutes les fenêtres cachées (pour réinitialisation)"""
        window_count = len(self._windows)
        log_message("INFO", f"🗑️ Destruction de {window_count} fenêtres en cache", category="ui")
        
        for window_name in list(self._windows.keys()):
            self.destroy_window(window_name)
        
        log_message("INFO", "✅ Toutes les fenêtres détruites", category="ui")
    
    def get_cached_windows_info(self):
        """Retourne des informations sur les fenêtres en cache"""
        return {
            'count': len(self._windows),
            'windows': list(self._windows.keys()),
            'persistent_states': len(self._window_states)
        }
    
    def _load_window_states(self):
        """Charge les états des fenêtres sauvegardés"""
        try:
            if os.path.exists(self._state_file):
                with open(self._state_file, 'r', encoding='utf-8') as f:
                    states = json.load(f)
                    log_message("DEBUG", f"États de fenêtres chargés : {len(states)} fenêtres", category="ui")
                    return states
        except Exception as e:
            log_message("ATTENTION", f"Erreur chargement états fenêtres: {e}", category="ui")
        
        return {}
    
    def _save_window_states(self):
        """Sauvegarde les états des fenêtres sur disque"""
        try:
            # Collecter les états de toutes les fenêtres actives
            log_message("DEBUG", f"Sauvegarde états : {len(self._windows)} fenêtres en cache", category="ui")
            
            states = {}
            for window_name, window_instance in self._windows.items():
                log_message("DEBUG", f"Vérification fenêtre '{window_name}'...", category="ui")
                
                if hasattr(window_instance, 'window') and window_instance.window:
                    try:
                        exists = window_instance.window.winfo_exists()
                        log_message("DEBUG", f"  → window.winfo_exists() = {exists}", category="ui")
                        
                        if exists:
                            # Sauvegarder géométrie et onglet actif
                            geometry = window_instance.window.geometry()
                            active_tab = self._get_active_tab(window_instance)
                            
                            states[window_name] = {
                                'geometry': geometry,
                                'active_tab': active_tab
                            }
                            log_message("DEBUG", f"  → État sauvegardé : {geometry}, onglet {active_tab}", category="ui")
                        else:
                            log_message("DEBUG", f"  → Fenêtre n'existe plus, ignorée", category="ui")
                    except Exception as e:
                        log_message("ATTENTION", f"  → Erreur récupération état: {e}", category="ui")
                else:
                    log_message("DEBUG", f"  → Pas d'attribut 'window' ou window is None", category="ui")
            
            # Sauvegarder sur disque
            os.makedirs(os.path.dirname(self._state_file), exist_ok=True)
            with open(self._state_file, 'w', encoding='utf-8') as f:
                json.dump(states, f, indent=2)
            
            log_message("DEBUG", f"États de {len(states)} fenêtres sauvegardés", category="ui")
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur sauvegarde états fenêtres: {e}", category="ui")
    
    def _get_active_tab(self, window_instance):
        """Récupère l'onglet actif d'une fenêtre (si elle a un notebook)"""
        try:
            if hasattr(window_instance, 'notebook') and window_instance.notebook:
                return window_instance.notebook.index(window_instance.notebook.select())
        except:
            pass
        return 0
    
    def restore_window_state(self, window_name, window_instance):
        """Restaure l'état sauvegardé d'une fenêtre sans flash visuel"""
        try:
            if window_name in self._window_states:
                state = self._window_states[window_name]
                
                if hasattr(window_instance, 'window') and window_instance.window:
                    # Cacher temporairement la fenêtre pour éviter le flash de repositionnement
                    was_visible = window_instance.window.winfo_viewable()
                    if was_visible:
                        window_instance.window.withdraw()
                    
                    # Restaurer géométrie
                    if 'geometry' in state:
                        try:
                            window_instance.window.geometry(state['geometry'])
                            # Force update pour appliquer immédiatement
                            window_instance.window.update_idletasks()
                        except Exception as e:
                            log_message("DEBUG", f"Erreur géométrie: {e}", category="ui")
                    
                    # Restaurer onglet actif
                    if 'active_tab' in state and hasattr(window_instance, 'notebook'):
                        try:
                            window_instance.notebook.select(state['active_tab'])
                        except Exception as e:
                            log_message("DEBUG", f"Erreur onglet: {e}", category="ui")
                    
                    # Réafficher la fenêtre à la bonne position
                    if was_visible:
                        window_instance.window.deiconify()
                        window_instance.window.lift()
                
                log_message("INFO", f"✨ État restauré: {window_name} → {state.get('geometry', 'N/A')}, onglet {state.get('active_tab', 0)}", category="ui")
                
        except Exception as e:
            log_message("ATTENTION", f"Erreur restauration état fenêtre {window_name}: {e}", category="ui")
    
    def save_on_close(self):
        """Sauvegarde les états avant fermeture de l'application"""
        log_message("INFO", f"Début sauvegarde états fenêtres ({len(self._windows)} fenêtres en cache)", category="ui")
        self._save_window_states()
        log_message("INFO", "États des fenêtres sauvegardés pour la prochaine session", category="ui")
    
    def clear_persistent_states(self):
        """Efface les états persistants (réinitialisation)"""
        try:
            if os.path.exists(self._state_file):
                os.remove(self._state_file)
                log_message("INFO", "États persistants des fenêtres effacés", category="ui")
            self._window_states = {}
        except Exception as e:
            log_message("ERREUR", f"Erreur suppression états fenêtres: {e}", category="ui")


# Instance globale
_window_manager = None

def get_window_manager():
    """Retourne l'instance unique du WindowManager"""
    global _window_manager
    if _window_manager is None:
        _window_manager = WindowManager()
    return _window_manager

