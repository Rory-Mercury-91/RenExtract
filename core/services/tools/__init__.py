"""
Package "Tools Services" - Tools Services - Outils maintenance
Système de monitoring de santé pour RenExtract
"""

import os
from typing import Dict, List, Any

# Import du système de logging
try:
    from infrastructure.logging.logging import log_message
    LOGGING_AVAILABLE = True
except ImportError:
    LOGGING_AVAILABLE = False
    def log_message(level, message, category="init"):
        pass

def discover_modules() -> List[str]:
    """Découverte automatique des modules dans ce package"""
    try:
        package_dir = os.path.dirname(__file__)
        modules = []
        
        # Fichiers Python dans ce dossier
        for item in os.listdir(package_dir):
            item_path = os.path.join(package_dir, item)
            
            # Fichiers .py (sauf __init__)
            if item.endswith('.py') and item != '__init__.py':
                module_name = item[:-3]
                modules.append(module_name)
            
            # Sous-dossiers (packages)
            elif os.path.isdir(item_path) and not item.startswith('__') and not item.startswith('.'):
                if os.path.exists(os.path.join(item_path, '__init__.py')):
                    modules.append(item)
        
        return sorted(modules)
    except Exception as e:
        if LOGGING_AVAILABLE:
            log_message("ERREUR", f"Erreur découverte modules: {e}", "init_tools")
        return []

def load_module_symbols(module_path: str) -> Dict[str, Any]:
    """Charge les symboles publics d'un module"""
    try:
        module = __import__(module_path, fromlist=[''])
        symbols = {}
        
        # Priorité à __all__ si disponible
        if hasattr(module, '__all__'):
            for name in module.__all__:
                if hasattr(module, name):
                    symbols[name] = getattr(module, name)
        else:
            # Sinon, découvrir les symboles publics
            for name in dir(module):
                if not name.startswith('_'):
                    obj = getattr(module, name)
                    if callable(obj) or isinstance(obj, type):
                        symbols[name] = obj
        
        return symbols
    except Exception as e:
        if LOGGING_AVAILABLE:
            log_message("DEBUG", f"Module {module_path}: {e}", "init_tools")
        return {}

# Découverte et chargement
modules_list = discover_modules()
loaded_modules = {}
failed_modules = []

for module_name in modules_list:
    try:
        module_path = "core.services.tools." + module_name
        symbols = load_module_symbols(module_path)
        
        if symbols:
            loaded_modules[module_name] = symbols
            # Export vers globals()
            for symbol_name, symbol_obj in symbols.items():
                globals()[symbol_name] = symbol_obj
        else:
            failed_modules.append(module_name)
            
    except Exception as e:
        failed_modules.append(module_name)
        if LOGGING_AVAILABLE:
            log_message("DEBUG", f"❌ {module_name}: {e}", "init_tools")

# Calcul de la santé
total_modules = len(modules_list)
loaded_count = len(loaded_modules)
failed_count = len(failed_modules)
health_percentage = (loaded_count / total_modules * 100) if total_modules > 0 else 100

# Rapport de santé (simplifié)
if LOGGING_AVAILABLE and total_modules > 0:
    if health_percentage >= 100:
        # Santé parfaite : log en DEBUG uniquement
        log_message("DEBUG", f"✅ Tools Services: {loaded_count}/{total_modules} OK", "tools")
    elif health_percentage >= 90:
        # Santé excellente mais pas 100% : afficher détails
        log_message("INFO", f"🟢 Package Tools Services santé excellente: {health_percentage:.0f}% ({loaded_count}/{total_modules} modules)", "tools")
        if failed_modules:
            log_message("ERREUR", f"Modules non chargés: {', '.join(failed_modules)}", "tools")
    elif health_percentage >= 70:
        log_message("INFO", f"🟡 Package Tools Services santé: {health_percentage:.0f}% ({loaded_count}/{total_modules} modules)", "tools")
        if failed_modules:
            log_message("ERREUR", f"Modules non chargés: {', '.join(failed_modules)}", "tools")
    else:
        log_message("ATTENTION", f"🔴 Package Tools Services santé critique: {health_percentage:.0f}% ({loaded_count}/{total_modules} modules)", "tools")
        if failed_modules:
            log_message("ERREUR", f"Modules non chargés: {', '.join(failed_modules)}", "tools")

# Métadonnées du package
__all__ = list(loaded_modules.keys())
_HEALTH_STATUS = {
    'package': 'Tools Services',
    'health_percentage': health_percentage,
    'loaded_modules': loaded_count,
    'failed_modules': failed_count,
    'total_modules': total_modules
}
