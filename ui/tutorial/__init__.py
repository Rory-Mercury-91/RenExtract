"""
Package "tutorial" - Système de guide HTML pour RenExtract
Structure modulaire optimisée en français uniquement
Version 2.0.0 avec système de santé automatique
"""

import os
import sys
import datetime
import webbrowser
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
from infrastructure.config.constants import VERSION, ensure_folders_exist, FILE_NAMES, FOLDERS
from infrastructure.logging.logging import log_message, get_logger
from infrastructure.helpers.unified_functions import show_custom_messagebox
from ui.themes import theme_manager

# Import du système de logging
try:
    LOGGING_AVAILABLE = True
except ImportError:
    LOGGING_AVAILABLE = False
    def log_message(level, message, category="init_tutorial"):
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
            # 2. Découverte automatique des symboles publics (sans underscore)
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
        log_message("DEBUG", f"Erreur découverte exports pour {module_name}: {str(e)}", "init_tutorial")
        return {}

def discover_module_exports_with_retries(module_name: str, max_retries: int = 3) -> Dict[str, Any]:
    # Retry pour dépendances circulaires
    for attempt in range(max_retries + 1):
        try:
            return discover_module_exports(module_name)
        except ImportError as e:
            if "circular import" in str(e).lower() or "partially initialized" in str(e):
                if attempt < max_retries:
                    log_message("DEBUG", f"Tentative {attempt + 1}/{max_retries + 1} - dépendance circulaire: {module_name}", "init_tutorial")
                    import time
                    time.sleep(0.1)
                    continue
                else:
                    log_message("ATTENTION", f"Dépendance circulaire persistante: {module_name}", "init_tutorial")
                    return {}
            else:
                log_message("ERREUR", f"Import impossible: {module_name} - {str(e)}", "init_tutorial")
                return {}
        except Exception as e:
            log_message("ERREUR", f"Erreur découverte: {module_name} - {str(e)}", "init_tutorial")
            return {}
    
    return {}

def discover_modules_in_directory() -> List[str]:
    # Scan automatique du dossier pour trouver les modules
    import os
    import glob
    
    try:
        tutorial_dir = os.path.dirname(__file__)
        python_files = glob.glob(os.path.join(tutorial_dir, "*.py"))
        
        modules_list = []
        excluded_files = {'__init__', '__pycache__', 'test_', 'temp_', 'backup_'}
        
        for file_path in python_files:
            module_name = os.path.basename(file_path)[:-3]  # Enlever .py
            
            # Filtrer les fichiers à exclure
            should_exclude = any(module_name.startswith(exclude) for exclude in excluded_files)
            
            if not should_exclude and module_name not in modules_list:
                modules_list.append(module_name)
        
        # Chercher aussi dans les sous-dossiers
        subdirs = [d for d in os.listdir(tutorial_dir) if os.path.isdir(os.path.join(tutorial_dir, d)) and not d.startswith('__')]
        for subdir in subdirs:
            if subdir not in ['translations', 'content']:  # Exclusions spéciales
                modules_list.append(subdir)
        
        # Trier pour un ordre cohérent
        modules_list.sort()
        
        return modules_list
        
    except Exception as e:
        log_message("ERREUR", f"Impossible de scanner le dossier: {str(e)}", "init_tutorial")
        # Fallback avec la liste connue
        return ['generator', 'cache', 'utils']

def load_tutorial_modules() -> Dict[str, Dict[str, Any]]:
    # Chargement automatique de tous les modules découverts
    modules_list = discover_modules_in_directory()
    
    loaded_modules = {}
    failed_modules = []
    
    
    # Séparer les modules potentiellement problématiques
    problematic_modules = set()  # Aucun module problématique connu pour tutorial
    safe_modules = [m for m in modules_list if m not in problematic_modules]
    risky_modules = [m for m in modules_list if m in problematic_modules]
    
    # Étape 1: Charger les modules "sûrs" d'abord
    for module_name in safe_modules:
        try:
            symbols = discover_module_exports(f'ui.tutorial.{module_name}')
            
            if symbols:
                loaded_modules[module_name] = symbols
            else:
                failed_modules.append(module_name)
                log_message("ATTENTION", f"❌ {module_name}: aucun symbole public trouvé", "init_tutorial")
                
        except Exception as e:
            failed_modules.append(module_name)
            log_message("ERREUR", f"❌ {module_name}: {str(e)}", "init_tutorial")
    
    # Étape 2: Charger les modules "risqués" avec retry
    for module_name in risky_modules:
        try:
            symbols = discover_module_exports_with_retries(f'ui.tutorial.{module_name}', max_retries=3)
            
            if symbols:
                loaded_modules[module_name] = symbols
            else:
                failed_modules.append(module_name)
                log_message("ATTENTION", f"❌ {module_name}: aucun symbole trouvé après retry", "init_tutorial")
                
        except Exception as e:
            failed_modules.append(module_name)
            log_message("ERREUR", f"❌ {module_name}: {str(e)}", "init_tutorial")
    
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
                    logger.enable_debug_mode(['init_tutorial', 'tutorial'])
                else:
                    logger.enable_debug_mode()
                log_message("INFO", "🔧 Mode debug activé automatiquement (santé < 80%)", "init_tutorial")
        elif health_status['health_percentage'] >= 95:
            # Excellente santé - désactiver le debug si activé automatiquement
            if hasattr(logger, 'disable_debug_mode'):
                # Vérifier la signature de la méthode
                import inspect
                sig = inspect.signature(logger.disable_debug_mode)
                if len(sig.parameters) > 0:
                    logger.disable_debug_mode(['init_tutorial'])
                else:
                    logger.disable_debug_mode()
                
    except Exception as e:
        log_message("ATTENTION", f"Impossible de gérer le mode debug: {str(e)}", "init_tutorial")

def export_symbols_to_globals(loaded_modules: Dict[str, Dict[str, Any]], current_globals: Dict) -> None:
    # Export des symboles vers l'espace de noms global
    exported_count = 0
    
    for module_name, symbols in loaded_modules.items():
        for symbol_name, symbol_obj in symbols.items():
            current_globals[symbol_name] = symbol_obj
            exported_count += 1
    

# =============================================================================
# FALLBACKS POUR FONCTIONNALITÉS CRITIQUES (CONSERVÉS)
# =============================================================================

def _fallback_show_tutorial(parent=None, language='fr'):
    # Version fallback pour show_tutorial
    try:
        log_message("ATTENTION", "Utilisation du fallback pour show_tutorial", "init_tutorial")
        theme = theme_manager.get_theme()
        show_custom_messagebox(
            'error',
            'Tutoriel indisponible',
            "Le système de tutoriel HTML n'est pas disponible.\n\n"
            "Le module principal de génération semble manquant ou défaillant.\n\n"
            "Consultez les logs pour plus de détails.",
            theme,
            parent=parent
        )
    except Exception as e:
        log_message("ERREUR", f"Erreur dans fallback show_tutorial: {e}", "init_tutorial")

def _fallback_generator():
    # Générateur fallback minimal
    class FallbackGenerator:
        def __init__(self):
            log_message("ATTENTION", "Générateur fallback utilisé", "init_tutorial")
        
        def generate_tutorial_html(self, version="Unknown", language="fr"):
            log_message("ERREUR", "Générateur principal indisponible", "init_tutorial")
            return None
    
    return FallbackGenerator

# =============================================================================
# FONCTIONS PRINCIPALES (CONSERVÉES)
# =============================================================================

def show_first_launch_popup(parent=None, app_controller=None):
    # Affiche un popup de premier lancement avec choix d'action
    try:
        log_message("DEBUG", "Affichage popup premier lancement", "init_tutorial")
        
        theme = theme_manager.get_theme()

        message_styled = [
            ("🎮 Bienvenue sur ", "normal"), ("RenExtract", "bold_green"), (" !\n\n", "normal"),
            ("Voici un résumé rapide pour bien démarrer :\n\n", "normal"),

            ("🔧 DEUX OUTILS COMPLÉMENTAIRES :\n", "bold"),
            ("• ", "blue"), ("Interface Principale :", "bold"), (" pour traiter les fichiers un par un.\n", "normal"),
            ("• ", "blue"), ("Générateur Ren'Py :", "bold"), (" pour gérer l'infrastructure complète du projet.\n\n", "normal"),

            ("📋 WORKFLOW SIMPLIFIÉ :\n", "bold"),
            ("1. ", "bold"), ("Générateur :", "green"), (" Extrayez les archives (.rpa) et générez l'arborescence.\n", "normal"),
            ("2. ", "bold"), ("Interface Principale :", "green"), (" Traitez chaque fichier (", "normal"), ("Extraire → Traduire → Reconstruire", "italic"), (").\n", "normal"),
            ("3. ", "bold"), ("Éditeur Temps Réel :", "green"), (" Affinez vos traductions en jouant (", "normal"), ("optionnel", "italic"), (").\n\n", "normal"),

            ("💡 PREMIERS PAS :\n", "bold"),
            ("• ", "yellow"), ("Configurez l'application via les Paramètres", "bold"), (" pour un confort optimal.\n", "normal"),
            ("• ", "yellow"), ("Familiarisez-vous", "bold"), (" en traitant un jeu simple (type \"kinetic novel\" court).\n", "normal"),
            ("• ", "yellow"), ("RenExtract gère automatiquement", "bold"), (" les sauvegardes et la validation.\n", "normal"),
            ("• ", "yellow"), ("Après chaque traitement, vérifiez toujours", "bold"), (" les avertissements et rapports générés.\n\n", "normal"),

            ("Pour aller plus loin, que souhaitez-vous faire maintenant ?", "blue")
        ]

        result = show_custom_messagebox(
            'askyesnocancel',
            '🎮 Bienvenue sur RenExtract',
            message_styled,
            theme,
            yes_text='📖 Ouvrir le Guide Complet',
            no_text='⚙️ Configurer les Paramètres',
            cancel_text='🚀 Commencer directement',
            parent=parent,
            yes_width=25,
            no_width=25,
            cancel_width=25
        )

        mark_tutorial_shown()

        if result is True:
            show_tutorial(parent)
        elif result is False:
            if app_controller:
                from ui.dialogs.settings_interface import show_unified_settings
                show_unified_settings(parent, app_controller)
            else:
                log_message("ATTENTION", "AppController non fourni pour les paramètres", "init_tutorial")

    except Exception as e:
        log_message("ERREUR", f"Erreur popup premier démarrage : {e}", "init_tutorial")

def check_first_launch():
    # Vérifie si c'est le premier lancement
    try:
        tutorial_flag_file = FILE_NAMES["tutorial_flag"]
        is_first = not os.path.exists(tutorial_flag_file)
        
        return is_first
    except Exception as e:
        log_message("ERREUR", f"Erreur vérification premier lancement: {e}", "init_tutorial")
        return True  # Par défaut, considérer comme premier lancement

def mark_tutorial_shown():
    # Marque que le tutoriel a été affiché
    try:
        ensure_folders_exist()
        tutorial_flag_file = FILE_NAMES["tutorial_flag"]

        with open(tutorial_flag_file, "w", encoding="utf-8") as f:
            f.write(f"Tutorial shown on: {datetime.datetime.now().isoformat()}\n")
            f.write(f"Version: {VERSION}\n")
            f.write("This file prevents the tutorial from showing again.\n")
            f.write("Delete this file to show the tutorial on next launch.\n")

        log_message("DEBUG", "Tutoriel marqué comme affiché", "init_tutorial")
            
    except Exception as e:
        log_message("ATTENTION", f"Impossible de marquer le tutoriel: {e}", "init_tutorial")

def show_tutorial(parent=None, language='fr'):
    # Fonction principale pour afficher le tutoriel HTML (français uniquement)
    try:
        log_message("DEBUG", f"Demande d'affichage tutoriel", "init_tutorial")
        
        # Essayer d'utiliser le générateur importé automatiquement
        if 'TutorialGenerator' in globals():
            TutorialGenerator = globals()['TutorialGenerator']
            
            if isinstance(TutorialGenerator, type):
                generator = TutorialGenerator()
                html_path = generator.generate_tutorial_html(VERSION)
                
                if html_path and os.path.exists(html_path):
                    try:
                        html_url = f"file:///{html_path.replace(os.sep, '/')}"
                        webbrowser.open(html_url)
                        log_message("INFO", f"Guide complet ouvert dans le navigateur: {html_path}", "init_tutorial")
                        return html_path
                    except Exception as e:
                        log_message("ERREUR", f"Impossible d'ouvrir le navigateur: {e}", "init_tutorial")
                        _show_fallback_message(parent)
                        return html_path
                        
        # Fallback si aucun générateur disponible
        log_message("ERREUR", "Générateur non disponible", "init_tutorial")
        _show_fallback_message(parent)
        return None

    except Exception as e:
        log_message("ERREUR", f"Erreur génération tutoriel HTML: {e}", "init_tutorial")
        _show_fallback_message(parent)
        return None

def _show_fallback_message(parent=None):
    # Affiche un message de fallback si la génération HTML échoue
    try:
        theme = theme_manager.get_theme()
        show_custom_messagebox(
            'error',
            'Erreur Guide',
            "Impossible de générer le guide HTML.\n\n"
            "Vérifiez les logs dans 04_Configs pour plus de détails.\n\n"
            "En attendant, consultez la documentation en ligne ou "
            "les commentaires dans le code source de l'application.",
            theme,
            parent=parent
        )
    except Exception:
        pass

# Classe legacy maintenue pour compatibilité
class UnifiedTutorialInterface:
    def __init__(self, parent_window, app_controller=None):
        log_message("INFO", "Interface Tkinter remplacée par HTML", "init_tutorial")
        show_tutorial(parent_window)

# =============================================================================
# MÉTADONNÉES / VALIDATION ARCHITECTURE - CONSERVÉES
# =============================================================================

CONTENT_MODULES = {
    1: 'tab_01',
    2: 'tab_02',
    3: 'tab_03',
    4: 'tab_04',
    5: 'tab_05',
    6: 'tab_06',
    7: 'tab_07',
    8: 'tab_08',
    9: 'tab_09'
}

def get_version_info():
    # Informations de version enrichies avec santé
    return {
        'version': '2.0.0',
        'architecture': 'modulaire_française',
        'language': 'fr',
        'total_modules': len(CONTENT_MODULES),
        'health_percentage': TUTORIAL_HEALTH_STATUS.get('health_percentage', 0),
        'debug_mode': TUTORIAL_HEALTH_STATUS.get('health_percentage', 100) < 80,
        'features': [
            'Guide français complet',
            'Modules de contenu séparés',
            'Cache optimisé',
            "Gestion d'erreurs robuste",
            "Système de santé automatique",
            "Mode debug adaptatif",
            "Auto-scroll lors du changement d'onglet"
        ]
    }

def validate_architecture():
    # Validation architecture avec santé automatique
    health_percentage = TUTORIAL_HEALTH_STATUS.get('health_percentage', 0)
    
    return {
        'valid': health_percentage >= 70,
        'health_percentage': health_percentage,
        'errors': TUTORIAL_FAILED_MODULES,
        'warnings': [],
        'debug_mode': health_percentage < 80,
        'details': TUTORIAL_HEALTH_STATUS
    }

def get_health_report():
    # Rapport de santé détaillé
    health_data = TUTORIAL_HEALTH_STATUS
    
    if not health_data:
        return "Aucune donnée de santé disponible"
    
    report = [
        f"RAPPORT DE SANTÉ - Package ui.tutorial",
        f"Santé globale: {health_data.get('health_percentage', 0)}%",
        f"Modules chargés: {health_data.get('loaded_modules', 0)}/{health_data.get('total_modules', 0)}",
        f"Symboles exportés: {health_data.get('total_symbols', 0)}",
        f"Mode debug: {'ACTIVÉ' if health_data.get('health_percentage', 100) < 80 else 'DÉSACTIVÉ'}",
        "",
        "MODULES:",
    ]
    
    for module in TUTORIAL_LOADED_MODULES:
        pass
    
    if TUTORIAL_FAILED_MODULES:
        report.append("ÉCHECS:")
        for module in TUTORIAL_FAILED_MODULES:
            report.append(f"  ❌ {module}: FAILED")
    
    return "\n".join(report)

def force_health_check():
    # Force un nouveau check de santé
    global TUTORIAL_HEALTH_STATUS, TUTORIAL_LOADED_MODULES, TUTORIAL_FAILED_MODULES
    loaded_modules, failed_modules, modules_list = load_tutorial_modules()
    health_status = calculate_health_status(loaded_modules, failed_modules, modules_list)
    
    TUTORIAL_HEALTH_STATUS = health_status
    TUTORIAL_LOADED_MODULES = list(loaded_modules.keys())
    TUTORIAL_FAILED_MODULES = failed_modules
    
    return health_status['health_percentage'], health_status

# ===== INITIALISATION DU PACKAGE =====


try:
    # Chargement des modules
    loaded_modules, failed_modules, modules_list = load_tutorial_modules()
    total_modules = len(modules_list)
    
    # Calcul de la santé
    health_status = calculate_health_status(loaded_modules, failed_modules, modules_list)
    
    # Gestion du mode debug automatique
    # ✅ DÉSACTIVÉ : On laisse l'utilisateur gérer le mode debug via les paramètres
    # manage_debug_mode(health_status)
    
    # Export des symboles
    export_symbols_to_globals(loaded_modules, globals())
    
    # Messages de santé (simplifiés)
    if LOGGING_AVAILABLE:
        if health_status['health_percentage'] >= 100:
            # Santé parfaite : log en DEBUG uniquement
            log_message("DEBUG", f"✅ tutorial: {health_status['loaded_modules']}/{health_status['total_modules']} OK", "init_tutorial")
        elif health_status['health_percentage'] >= 90:
            # Santé excellente mais pas 100% : afficher détails
            log_message("INFO", f"🟢 Package tutorial santé excellente: {health_status['health_percentage']:.0f}% ({health_status['loaded_modules']}/{health_status['total_modules']} modules)", "init_tutorial")
            if health_status['failed_modules'] > 0:
                log_message("ERREUR", f"Modules non chargés: {', '.join(health_status['failed_module_names'])}", "init_tutorial")
        elif health_status['health_percentage'] >= 70:
            log_message("ATTENTION", f"🟡 Package tutorial santé: {health_status['health_percentage']:.0f}% ({health_status['loaded_modules']}/{health_status['total_modules']} modules)", "init_tutorial")
            if health_status['failed_modules'] > 0:
                log_message("ERREUR", f"Modules non chargés: {', '.join(health_status['failed_module_names'])}", "init_tutorial")
        else:
            log_message("ERREUR", f"🔴 Package tutorial santé critique: {health_status['health_percentage']:.0f}% ({health_status['loaded_modules']}/{health_status['total_modules']} modules)", "init_tutorial")
            if health_status['failed_modules'] > 0:
                log_message("ERREUR", f"Modules non chargés: {', '.join(health_status['failed_module_names'])}", "init_tutorial")
    
    # Message final de santé
    
    # Définir __all__ dynamiquement
    __all__ = [
        # Fonctions principales conservées
        'show_tutorial',
        'show_first_launch_popup', 
        'check_first_launch',
        'mark_tutorial_shown',
        'UnifiedTutorialInterface',
        'get_version_info',
        'validate_architecture',
        'get_health_report',
        'force_health_check',
        'CONTENT_MODULES',
    ]
    
    for symbols in loaded_modules.values():
        __all__.extend(symbols.keys())
    
    # Variables de statut disponibles pour l'extérieur
    TUTORIAL_HEALTH_STATUS = health_status
    TUTORIAL_LOADED_MODULES = list(loaded_modules.keys())
    TUTORIAL_FAILED_MODULES = failed_modules

except Exception as e:
    log_message("ERREUR", f"💥 Erreur critique lors de l'initialisation du package tutorial: {str(e)}", "init_tutorial")
    # Définir des valeurs de fallback
    __all__ = [
        'show_tutorial',
        'show_first_launch_popup', 
        'check_first_launch',
        'mark_tutorial_shown',
        'UnifiedTutorialInterface'
    ]
    TUTORIAL_HEALTH_STATUS = {
        'health_percentage': 0,
        'loaded_modules': 0,
        'failed_modules': 1,
        'total_modules': 1,
        'total_symbols': 0,
        'failed_module_names': ['init_error'],
        'can_operate': False,
        'is_healthy': False
    }
    TUTORIAL_LOADED_MODULES = []
    TUTORIAL_FAILED_MODULES = ['critical_init_error']

# Version et métadonnées du package (récupération automatique depuis constants)
try:
    from infrastructure.config.constants import VERSION, PROJECT_NAME, AUTHOR, PROJECT_DESCRIPTION
    __version__ = VERSION
    __author__ = AUTHOR
    __project__ = PROJECT_NAME
    __description__ = f"Package tutorial pour {PROJECT_NAME} - Système de guide HTML français avec génération optimisée"
except ImportError:
    # Fallbacks si constants indisponible
    __version__ = "2.0.0"
    __author__ = "Rory Mercury91"
    __project__ = "RenExtract"
    __description__ = "Package tutorial pour RenExtract - Système de guide HTML français avec génération optimisée"