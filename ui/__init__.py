"""
Package "ui" - Interface utilisateur de RenExtract
Système de logging configuré pour le monitoring de santé du package.
Gestion améliorée des dépendances circulaires.
"""

import sys
import os
from typing import Dict, List, Any, Optional, Set

# Import du système de logging
try:
    from infrastructure.logging.logging import log_message, get_logger
    LOGGING_AVAILABLE = True
except ImportError:
    LOGGING_AVAILABLE = False
    def log_message(level, message, category="init_ui"):
        pass  # Fallback silencieux

def discover_module_exports(module_name: str) -> Dict[str, Any]:
    # Découverte automatique des exports publics
    try:
        module = __import__(module_name, fromlist=[''])
        exported_symbols = {}
        
        # 1. Chercher __all__ en priorité
        if hasattr(module, '__all__'):
            for name in module.__all__:
                if hasattr(module, name):
                    exported_symbols[name] = getattr(module, name)
        else:
            # 2. Découverte automatique des symboles publics
            for name in dir(module):
                if not name.startswith('_'):  # Exclure les privés
                    obj = getattr(module, name)
                    # Inclure seulement les classes, fonctions et constantes
                    if (callable(obj) or 
                        isinstance(obj, type) or 
                        (isinstance(obj, (str, int, float, bool, list, dict, tuple)) and name.isupper())):
                        exported_symbols[name] = obj
        
        return exported_symbols
        
    except Exception as e:
        log_message("DEBUG", f"Erreur découverte exports pour {module_name}: {str(e)}", "init_ui")
        return {}

def discover_module_exports_with_retries(module_name: str, max_retries: int = 3) -> Dict[str, Any]:
    # Retry pour dépendances circulaires
    for attempt in range(max_retries + 1):
        try:
            return discover_module_exports(module_name)
        except ImportError as e:
            if "circular import" in str(e).lower() or "partially initialized" in str(e):
                if attempt < max_retries:
                    log_message("DEBUG", f"Tentative {attempt + 1}/{max_retries + 1} - dépendance circulaire: {module_name}", "init_ui")
                    import time
                    time.sleep(0.1)
                    continue
                else:
                    log_message("ATTENTION", f"Dépendance circulaire persistante: {module_name}", "init_ui")
                    return {}
            else:
                log_message("ERREUR", f"Import impossible: {module_name} - {str(e)}", "init_ui")
                return {}
        except Exception as e:
            log_message("ERREUR", f"Erreur découverte: {module_name} - {str(e)}", "init_ui")
            return {}
    
    return {}

def discover_modules_in_directory() -> List[str]:
    # Scan automatique du dossier pour trouver les modules
    import os
    import glob
    
    try:
        ui_dir = os.path.dirname(__file__)
        python_files = glob.glob(os.path.join(ui_dir, "*.py"))
        
        modules_list = []
        excluded_files = {'__init__', '__pycache__', 'test_', 'temp_', 'backup_'}
        
        for file_path in python_files:
            module_name = os.path.basename(file_path)[:-3]  # Enlever .py
            
            # Filtrer les fichiers à exclure
            should_exclude = any(module_name.startswith(exclude) for exclude in excluded_files)
            
            if not should_exclude and module_name not in modules_list:
                modules_list.append(module_name)
        
        # Chercher aussi dans les sous-dossiers
        subdirs = [d for d in os.listdir(ui_dir) if os.path.isdir(os.path.join(ui_dir, d)) and not d.startswith('__')]
        for subdir in subdirs:
            modules_list.append(subdir)
        
        # Trier pour un ordre cohérent
        modules_list.sort()
        
        return modules_list
        
    except Exception as e:
        log_message("ERREUR", f"Impossible de scanner le dossier: {str(e)}", "init_ui")
        # Fallback avec modules
        return [
        'buttons_frame',
        'content_frame',
        'header_frame',
        'info_frame',
        'input_manager',
        'main_window',
        'maintenance_tools_interface',
        'notification_manager',
        'settings_interface',
        'themes',
        'translation_generator_interface',
        'unified_backup_interface',
    ]

def load_ui_modules() -> Dict[str, Dict[str, Any]]:
    # Chargement automatique de tous les modules découverts
    modules_list = discover_modules_in_directory()
    
    loaded_modules = {}
    failed_modules = []
    
    
    # Séparer les modules potentiellement problématiques
    problematic_modules = set()
    safe_modules = [m for m in modules_list if m not in problematic_modules]
    risky_modules = [m for m in modules_list if m in problematic_modules]
    
    # Étape 1: Charger les modules "sûrs" d'abord
    for module_name in safe_modules:
        try:
            symbols = discover_module_exports(f'ui.{module_name}')
            
            if symbols:
                loaded_modules[module_name] = symbols
            else:
                failed_modules.append(module_name)
                log_message("ATTENTION", f"❌ {module_name}: aucun symbole public trouvé", "init_ui")
                
        except Exception as e:
            failed_modules.append(module_name)
            log_message("ERREUR", f"❌ {module_name}: {str(e)}", "init_ui")
    
    # Étape 2: Charger les modules "risqués" avec retry
    for module_name in risky_modules:
        try:
            symbols = discover_module_exports_with_retries(f'ui.{module_name}', max_retries=3)
            
            if symbols:
                loaded_modules[module_name] = symbols
            else:
                failed_modules.append(module_name)
                log_message("ATTENTION", f"❌ {module_name}: aucun symbole trouvé après retry", "init_ui")
                
        except Exception as e:
            failed_modules.append(module_name)
            log_message("ERREUR", f"❌ {module_name}: {str(e)}", "init_ui")
    
    return loaded_modules, failed_modules, modules_list

def calculate_health_status(loaded_modules: Dict, failed_modules: List, modules_list: List) -> Dict[str, Any]:
    # Calcul du statut de santé du package
    total_modules = len(modules_list)
    loaded_count = len(loaded_modules)
    failed_count = len(failed_modules)
    health_percentage = (loaded_count / total_modules) * 100 if total_modules > 0 else 0
    
    total_symbols = sum(len(symbols) for symbols in loaded_modules.values())
    
    status = {
        'health_percentage': health_percentage,
        'loaded_modules': loaded_count,
        'failed_modules': failed_count,
        'total_modules': total_modules,
        'total_symbols': total_symbols,
        'failed_module_names': failed_modules,
        'can_operate': health_percentage >= 50,
        'is_healthy': health_percentage >= 80
    }
    
    return status

def manage_debug_mode(health_status: Dict[str, Any]) -> None:
    # Gestion automatique du mode debug selon la santé
    if not LOGGING_AVAILABLE:
        return
    
    try:
        logger = get_logger()
        
        if health_status['health_percentage'] < 80:
            # Santé faible - activer le debug
            if hasattr(logger, 'enable_debug_mode'):
                # Vérifier la signature de la méthode
                import inspect
                sig = inspect.signature(logger.enable_debug_mode)
                if len(sig.parameters) > 0:
                    logger.enable_debug_mode(['init_ui', 'ui'])
                else:
                    logger.enable_debug_mode()
                log_message("INFO", "🔧 Mode debug activé automatiquement (santé < 80%)", "init_ui")
        elif health_status['health_percentage'] >= 95:
            # Excellente santé - désactiver le debug seulement s'il n'a pas été activé par l'utilisateur
            try:
                from infrastructure.config.config import config_manager
                user_debug_enabled = config_manager.get('debug_mode', False)
                if not user_debug_enabled and hasattr(logger, 'disable_debug_mode'):
                    # Vérifier la signature de la méthode
                    import inspect
                    sig = inspect.signature(logger.disable_debug_mode)
                    if len(sig.parameters) > 0:
                        logger.disable_debug_mode(['init_ui'])
                    else:
                        logger.disable_debug_mode()
                elif user_debug_enabled:
                    pass  # Mode debug conservé (choix utilisateur)
            except ImportError:
                # Fallback si config_manager n'est pas disponible
                # Vérifier directement si le logger a le mode debug activé
                if hasattr(logger, 'debug_enabled') and logger.debug_enabled:
                    pass  # Mode debug déjà activé par l'utilisateur, ne pas le désactiver
                elif hasattr(logger, 'disable_debug_mode'):
                    import inspect
                    sig = inspect.signature(logger.disable_debug_mode)
                    if len(sig.parameters) > 0:
                        logger.disable_debug_mode(['init_ui'])
                    else:
                        logger.disable_debug_mode()
                
    except Exception as e:
        log_message("ATTENTION", f"Impossible de gérer le mode debug: {str(e)}", "init_ui")

def export_symbols_to_globals(loaded_modules: Dict[str, Dict[str, Any]], current_globals: Dict) -> None:
    # Export des symboles vers l'espace de noms global
    exported_count = 0
    
    for module_name, symbols in loaded_modules.items():
        for symbol_name, symbol_obj in symbols.items():
            current_globals[symbol_name] = symbol_obj
            exported_count += 1
    

# ===== INITIALISATION DU PACKAGE =====


try:
    # Chargement des modules
    loaded_modules, failed_modules, modules_list = load_ui_modules()
    total_modules = len(modules_list)
    
    # Calcul de la santé
    health_status = calculate_health_status(loaded_modules, failed_modules, modules_list)
    
    # Gestion du mode debug automatique
    manage_debug_mode(health_status)
    
    # Export des symboles
    export_symbols_to_globals(loaded_modules, globals())
    
    # Messages de santé (simplifiés)
    if LOGGING_AVAILABLE:
        if health_status['health_percentage'] >= 100:
            # Santé parfaite : log en DEBUG uniquement
            log_message("DEBUG", f"✅ ui: {health_status['loaded_modules']}/{health_status['total_modules']} OK", "init_ui")
        elif health_status['health_percentage'] >= 90:
            # Santé excellente mais pas 100% : afficher détails
            log_message("INFO", f"🟢 Package ui santé excellente: {health_status['health_percentage']:.0f}% ({health_status['loaded_modules']}/{health_status['total_modules']} modules)", "init_ui")
            if health_status['failed_modules'] > 0:
                log_message("ERREUR", f"Modules non chargés: {', '.join(health_status['failed_module_names'])}", "init_ui")
        elif health_status['health_percentage'] >= 70:
            log_message("ATTENTION", f"🟡 Package ui santé: {health_status['health_percentage']:.0f}% ({health_status['loaded_modules']}/{health_status['total_modules']} modules)", "init_ui")
            if health_status['failed_modules'] > 0:
                log_message("ERREUR", f"Modules non chargés: {', '.join(health_status['failed_module_names'])}", "init_ui")
        else:
            log_message("ERREUR", f"🔴 Package ui santé critique: {health_status['health_percentage']:.0f}% ({health_status['loaded_modules']}/{health_status['total_modules']} modules)", "init_ui")
            if health_status['failed_modules'] > 0:
                log_message("ERREUR", f"Modules non chargés: {', '.join(health_status['failed_module_names'])}", "init_ui")
    
    # Message final de santé
    
    # Définir __all__ dynamiquement
    __all__ = []
    for symbols in loaded_modules.values():
        __all__.extend(symbols.keys())
    
    # Variables de statut disponibles pour l'extérieur
    UI_HEALTH_STATUS = health_status
    UI_LOADED_MODULES = list(loaded_modules.keys())
    UI_FAILED_MODULES = failed_modules

except Exception as e:
    log_message("ERREUR", f"💥 Erreur critique lors de l'initialisation du package ui: {str(e)}", "init_ui")
    # Définir des valeurs de fallback
    __all__ = []
    UI_HEALTH_STATUS = {
        'health_percentage': 0,
        'loaded_modules': 0,
        'failed_modules': 1,
        'total_modules': 1,
        'total_symbols': 0,
        'failed_module_names': ['init_error'],
        'can_operate': False,
        'is_healthy': False
    }
    UI_LOADED_MODULES = []
    UI_FAILED_MODULES = ['critical_init_error']

# Version et métadonnées du package (récupération automatique depuis constants)
try:
    from infrastructure.config.constants import VERSION, PROJECT_NAME, AUTHOR, PROJECT_DESCRIPTION
    __version__ = VERSION
    __author__ = AUTHOR
    __project__ = PROJECT_NAME
    __description__ = f"Package ui pour {PROJECT_NAME}"
except ImportError:
    # Fallbacks si constants indisponible
    __version__ = "2.0.0"
    __author__ = "Rory Mercury91"
    __project__ = "RenExtract"
    __description__ = "Package ui pour RenExtract"