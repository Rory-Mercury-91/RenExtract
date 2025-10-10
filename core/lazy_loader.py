# core/lazy_loader.py
"""
Système de chargement paresseux (lazy loading) pour optimiser le démarrage
"""

import sys
import time
from typing import Dict, Any, Optional, Callable
from infrastructure.logging.logging import log_message

class LazyModuleLoader:
    """Gestionnaire de chargement paresseux pour optimiser les performances"""
    
    def __init__(self):
        self._loaded_modules: Dict[str, Any] = {}
        self._loading_functions: Dict[str, Callable] = {}
        self._loading_times: Dict[str, float] = {}
        
    def register_lazy_module(self, module_name: str, loader_function: Callable):
        """Enregistre un module pour chargement paresseux"""
        self._loading_functions[module_name] = loader_function
        
    def get_module(self, module_name: str) -> Any:
        """Récupère un module (le charge si nécessaire)"""
        if module_name in self._loaded_modules:
            return self._loaded_modules[module_name]
            
        if module_name in self._loading_functions:
            start_time = time.time()
            try:
                module = self._loading_functions[module_name]()
                self._loaded_modules[module_name] = module
                self._loading_times[module_name] = time.time() - start_time
                
                log_message("DEBUG", f"Module chargé paresseusement: {module_name} ({self._loading_times[module_name]:.3f}s)", category="lazy_loader")
                return module
                
            except Exception as e:
                log_message("ERREUR", f"Erreur chargement module {module_name}: {e}", category="lazy_loader")
                return None
                
        log_message("ATTENTION", f"Module {module_name} non enregistré pour chargement paresseux", category="lazy_loader")
        return None
    
    def is_loaded(self, module_name: str) -> bool:
        """Vérifie si un module est déjà chargé"""
        return module_name in self._loaded_modules
    
    def get_loading_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de chargement"""
        return {
            'loaded_modules': list(self._loaded_modules.keys()),
            'loading_times': self._loading_times.copy(),
            'total_loaded': len(self._loaded_modules),
            'total_time': sum(self._loading_times.values())
        }
    
    def preload_critical_modules(self):
        """Précharge les modules critiques pour le démarrage"""
        critical_modules = [
            'utils.logging',
            'utils.config',
            'core.app_controller',
            'ui.main_window'
        ]
        
        log_message("INFO", f"🚀 Préchargement de {len(critical_modules)} modules critiques...", category="lazy_loader")
        
        for module_name in critical_modules:
            if module_name in self._loading_functions:
                self.get_module(module_name)
        
        stats = self.get_loading_stats()
        log_message("INFO", f"✅ Préchargement terminé: {stats['total_loaded']} modules en {stats['total_time']:.3f}s", category="lazy_loader")

# Instance globale
lazy_loader = LazyModuleLoader()

def register_ui_module(module_name: str, loader_function: Callable):
    """Enregistre un module UI pour chargement paresseux"""
    lazy_loader.register_lazy_module(f"ui.{module_name}", loader_function)

def register_core_module(module_name: str, loader_function: Callable):
    """Enregistre un module Core pour chargement paresseux"""
    lazy_loader.register_lazy_module(f"core.{module_name}", loader_function)

def get_ui_module(module_name: str) -> Any:
    """Récupère un module UI"""
    return lazy_loader.get_module(f"ui.{module_name}")

def get_core_module(module_name: str) -> Any:
    """Récupère un module Core"""
    return lazy_loader.get_module(f"core.{module_name}")
