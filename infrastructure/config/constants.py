# utils/constants.py - VERSION AUTO-INCREMENTEE
# Constants and Configuration Module
# Created for RenExtract - Intégré avec le système de santé des packages
"""
Module contenant toutes les constantes de l'application — VERSION ADAPTÉE : Architecture portable moderne + monitoring de santé
"""
import sys, os, re, datetime
from pathlib import Path

# ========================================
# SYSTEME DE VERSION AUTO-INCREMENTEE
# ========================================

def get_executable_dir():
    """Retourne le dossier de l'exécutable (ou main.py)."""
    return os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(sys.argv[0]))

def get_version():
    """
    Retourne la version depuis le tag Git ou un fichier VERSION.txt
    Format: v1.2.11 ou valeur par défaut si pas de tag
    """
    import subprocess
    
    base_dir = get_executable_dir()
    
    # PRIORITÉ 1 : Lire depuis VERSION.txt (créé lors du build GitHub Actions)
    version_file = os.path.join(base_dir, "VERSION.txt")
    if os.path.exists(version_file):
        try:
            with open(version_file, "r", encoding="utf-8") as f:
                version = f.read().strip()
                if version:
                    return version
        except Exception:
            pass
    
    # PRIORITÉ 2 : Essayer de lire depuis Git (si disponible en développement)
    try:
        # Essayer de récupérer le dernier tag Git
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=base_dir,
            capture_output=True,
            text=True,
            timeout=2,
            check=False
        )
        if result.returncode == 0 and result.stdout.strip():
            tag = result.stdout.strip()
            # Enlever le 'v' si présent pour uniformiser
            if tag.startswith('v'):
                return tag
            return f"v{tag}"
    except Exception:
        pass
    
    # PRIORITÉ 3 : Essayer de lire depuis Git sans tag (commit hash)
    try:
        result = subprocess.run(
            ["git", "describe", "--always", "--dirty"],
            cwd=base_dir,
            capture_output=True,
            text=True,
            timeout=2,
            check=False
        )
        if result.returncode == 0 and result.stdout.strip():
            return f"dev-{result.stdout.strip()}"
    except Exception:
        pass
    
    # FALLBACK : Utiliser la date si rien d'autre n'est disponible
    return "RenExtract v1.2.13"

def increment_build_number():
    """
    Fonction obsolète - conservée pour compatibilité
    Retourne simplement la version actuelle depuis Git/VERSION.txt
    """
    return get_version()

# Version actuelle (lecture seule)
VERSION = get_version()
__version__ = VERSION  # Alias pour compatibilité avec les imports standards

# Métadonnées du projet
PROJECT_NAME = "RenExtract"
AUTHOR = "Rory Mercury91"
PROJECT_DESCRIPTION = "Outil d'extraction et de préparation à la traduction pour les jeux Ren'Py"

# Dossiers/fichiers
BASE_DIR = get_executable_dir()
FOLDERS = {"configs": os.path.join(BASE_DIR, "04_Configs"),
           "backup": os.path.join(BASE_DIR, "02_Sauvegardes"),
           "temporaires": os.path.join(BASE_DIR, "01_Temporaires"),
           "warnings": os.path.join(BASE_DIR, "03_Rapports")}
FILE_NAMES = {"config": os.path.join(FOLDERS["configs"], "config.json"),
              "log": os.path.join(FOLDERS["configs"], "log.txt"),
              "tutorial_flag": os.path.join(FOLDERS["configs"], "tutorial_shown.flag"),
              "languages": os.path.join(FOLDERS["configs"], "languages.json")}

def ensure_folders_exist():
    """Crée les dossiers nécessaires s'ils n'existent pas."""
    try:
        for p in FOLDERS.values(): os.makedirs(p, exist_ok=True)
    except Exception:
        pass

def ensure_game_structure(game_name: str):
    """Crée la structure de dossiers pour un jeu spécifique."""
    try:
        if not validate_game_name(game_name): return False
        for p in [os.path.join(FOLDERS["temporaires"], game_name),
                  os.path.join(FOLDERS["backup"], game_name),
                  os.path.join(FOLDERS["warnings"], game_name)]:
            os.makedirs(p, exist_ok=True)
        return True
    except Exception:
        return False

def validate_game_name(game_name: str) -> bool:
    """Valide un nom de jeu (dossier)."""
    try:
        if not game_name or not isinstance(game_name, str): return False
        if len(game_name) > 255 or len(game_name) < 1: return False
        if any(c in game_name for c in ['<','>',':','"','|','?','*','/','\\']): return False
        if game_name.upper() in ['CON','PRN','AUX','NUL','COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9','LPT1','LPT2','LPT3','LPT4','LPT5','LPT6','LPT7','LPT8','LPT9']: return False
        if game_name.startswith((' ','.')) or game_name.endswith((' ','.')): return False
        return True
    except Exception:
        return False

# Thèmes - Style moderne aligné avec le tutoriel HTML
THEMES = {
    "dark": {
        "bg": "#1a1f29",           # Fond principal (comme --bg du tutoriel)
        "fg": "#e2e8f0",           # Texte principal (comme --fg du tutoriel)
        "frame_bg": "#2d3748",     # Fond des frames (comme --card-bg du tutoriel)
        "button_bg": "#2d3748",    # Fond des boutons (comme --card-bg du tutoriel)
        "entry_bg": "#2d3748",      # Fond des entrées (comme --card-bg du tutoriel)
        "entry_fg": "#e2e8f0",     # Texte des entrées (comme --fg du tutoriel)
        "select_bg": "#4a90e2",    # Sélection (comme --accent du tutoriel)
        "select_fg": "#ffffff",    # Texte sélectionné
        "accent": "#4a90e2",       # Couleur d'accent (comme --accent du tutoriel)
        "warning": "#ed8936",      # Warning (comme --warning du tutoriel)
        "danger": "#f56565",       # Danger (comme --danger du tutoriel)
        "button_fg": "#000000",    # Texte des boutons (noir pour contraste)
        "button_help_fg": "#000000", # Texte des boutons d'aide (noir pour contraste)
        "nav_bg": "#1a202c",       # Navigation (comme --nav-bg du tutoriel)
        "sep": "#4a5568"           # Séparateurs (comme --sep du tutoriel)
    },
    "light": {
        "bg": "#f7fafc",           # Fond principal clair (comme --bg du tutoriel)
        "fg": "#2d3748",           # Texte principal clair (comme --fg du tutoriel)
        "frame_bg": "#ffffff",     # Fond des frames clair (comme --card-bg du tutoriel)
        "button_bg": "#ffffff",    # Fond des boutons clair (comme --card-bg du tutoriel)
        "entry_bg": "#ffffff",     # Fond des entrées clair (comme --card-bg du tutoriel)
        "entry_fg": "#2d3748",     # Texte des entrées clair (comme --fg du tutoriel)
        "select_bg": "#3182ce",    # Sélection claire (comme --accent du tutoriel)
        "select_fg": "#ffffff",    # Texte sélectionné
        "accent": "#3182ce",       # Couleur d'accent claire (comme --accent du tutoriel)
        "warning": "#d69e2e",      # Warning clair (comme --warning du tutoriel)
        "danger": "#e53e3e",       # Danger clair (comme --danger du tutoriel)
        "button_fg": "#000000",    # Texte des boutons (noir pour contraste)
        "button_help_fg": "#000000", # Texte des boutons d'aide (noir pour contraste)
        "nav_bg": "#f7fafc",       # Navigation claire (comme --nav-bg du tutoriel)
        "sep": "#e2e8f0"           # Séparateurs clairs (comme --sep du tutoriel)
    }
}

# Fenêtre
WINDOW_CONFIG = {"title": f"{VERSION}", "geometry": "1400x900", "min_size": (200, 100)}

# Logging
LOGGING_CONFIG = {
    "max_log_files": 5, "max_file_size_mb": 50, "log_encoding": "utf-8",
    "default_log_level": 3, "debug_log_level": 5,
    "available_categories": [
        "core","main","renextract",
        "extraction","reconstruction","coherence_check","renpy_generator","renpy_decompiler","renpy_sdk","renpy_tools",
        "ui","onglets","shared","ui_buttons","ui_content","ui_header","ui_info","ui_input","ui_main","ui_notify","ui_settings","ui_theme","ui_tutorial","ui_backup",
        "utils","performance","validation","file_io","cleanup","backup","utils_unified","utils_language","utils_i18n","utils_config","utils_logging",
        "diagnostic","system"
    ]
}

# Santé
HEALTH_CONFIG = {
    "expected_packages": ["utils","core","ui","main"],
    "critical_packages": ["utils","core","ui"],
    "health_thresholds": {"excellent":95,"good":80,"warning":60,"critical":40},
    "health_colors": {
        "excellent": "#198754",  # vert succès (aligné INFO)
        "good":      "#20C997",  # vert/teal succès-alt (plus doux que excellent)
        "warning":   "#FFC107",  # jaune alerte
        "critical":  "#DC3545",  # rouge danger
        "failed":    "#842029"   # rouge foncé (échec)
    }
}

# utils/constants.py
SPECIAL_CODES = [
    # === ÉCHAPPEMENTS DE BASE (dans les dialogues traduits) ===
    r'%%',                              # Double % échappé
    r'\\%',                             # % échappé avec backslash
    r'\\n', r'\\t', r'\\r', r'\\\\',    # Échappements dans les chaînes
    r'\\"',                             # Guillemets échappés dans les dialogues
    
    # NOTE: Antislash simple \ retiré car il peut être un caractère d'échappement légitime
    # et ne doit pas être protégé isolément pour éviter de casser la syntaxe Ren'Py
    
    # === FORMATAGE PYTHON DANS LES DIALOGUES ===
    r'%[sdioxXeEfFgGcr%]',              # Formatage simple %s, %d, %f dans le texte
    r'%[-+0 #]*\*?[0-9]*\.?\*?[0-9]*[sdioxXeEfFgGcr%]',  # Formatage avec options %05d, %.2f
    
    # CORRIGÉ: Formatage nommé %(nom)s - VERSION SIMPLIFIÉE
    r'%\([^)]+\)[sdioxXeEfFgGcr%]',     # %(player_name)s, %(score)d, etc.
    
    # === VARIABLES REN'PY DANS LE TEXTE ===
    r'%[a-zA-Z_][a-zA-Z0-9_]*',        # Variables %nom_personnage, %score
    r'%\[[^\]]+\]',                     # Variables avec crochets %[variable]
    r'%\{[^}]+\}',                      # Expressions %{code_python}
    
    # === CODES SPÉCIAUX REN'PY ===
    r'\[[^\]]+\]',                      # Balises crochétées [nom], [color=#ff0000]
    r'<[^>]+>',                         # Balises HTML <b>, <i>, <color=#ff0000>
    r'\{[^}]+\}',                       # Balises accolades {nom}, {color=#ff0000}
    
    # === CODES DE FORMATAGE AVANCÉ ===
    r'\{[^}]*color[^}]*\}',            # Codes couleur {color=#ff0000}
    r'\{[^}]*size[^}]*\}',             # Codes taille {size=24}
    r'\{[^}]*font[^}]*\}',             # Codes police {font=arial}
    
    # === CODES DE CONTRÔLE ===
    r'\{[^}]*w[^}]*\}',                # Codes attente {w=1.0}
    r'\{[^}]*cps[^}]*\}',              # Codes vitesse {cps=20}
    r'\{[^}]*pause[^}]*\}',            # Codes pause {pause=2.0}
]
PROTECTION_ORDER = [(r'\"','Guillemets échappés'),('""','Chaînes vides'),('" "','Un espace'),('"  "','Deux espaces'),('"   "','Trois espaces')]
SUPPORTED_FILES = {"renpy":[("Ren'Py script","*.rpy")], "text":[("Texte","*.txt")], "all":[("Tous fichiers","*.*")]}

# Messages
MESSAGES = {
    "extraction_success":"✅ Extraction terminée en {time:.2f}s !",
    "reconstruction_success":"✅ Fichier traduit créé en {time:.2f}s",
    "no_file_loaded":"⚠️ Erreur: Chargez d'abord un fichier .rpy",
    "files_missing":"⚠️ Erreur: Fichiers manquants",
    "extraction_in_progress":"⚙️ Extraction en cours...",
    "reconstruction_in_progress":"🔧 Reconstruction en cours...",
    "health_excellent":"🎉 Santé du système: Excellente ({health}%)",
    "health_good":"✅ Santé du système: Bonne ({health}%)",
    "health_warning":"⚠️ Santé du système: Attention ({health}%)",
    "health_critical":"🚨 Santé du système: Critique ({health}%)",
    "health_failed":"❌ Santé du système: Défaillance ({health}%)",
    "package_loaded":"📦 Package {package} chargé - Santé: {health}%",
    "package_failed":"❌ Package {package} non disponible: {error}",
    "debug_mode_changed":"🔧 Mode debug: {mode} ({categories})",
    "system_ready":"🚀 RenExtract prêt - Santé globale: {health}%"
}
NOTIFICATION_CONFIG = {"toast_duration":3000,"reduce_popups":True,"smart_notifications":True,"log_notifications":True,"health_notifications":True}
CRITICAL_POPUPS = ["fermer_application","reinitialiser","nettoyer_page","validation_errors","file_corruption","backup_restore","health_critical","package_failure"]
MESSAGE_PRIORITIES = {
    "STATUS_ONLY":["extraction_progress","reconstruction_progress","file_loading","ready_state","health_updates"],
    "TOAST":["auto_open_toggle","validation_toggle","language_change","theme_change","operation_success","minor_warnings","debug_mode_change","health_good"],
    "MODAL":["quit_confirmation","reset_with_data","clean_with_data","critical_errors","file_conflicts","health_critical","package_failures"]
}

# Thème par défaut & presets (Classique v1)
THEME_COLORS_DEFAULT = {
    "button_fg_dark":"#000000","button_fg_light":"#000000",
    "button_primary_bg":"#28a745","button_secondary_bg":"#007bff","button_tertiary_bg":"#ffc107","button_danger_bg":"#dc3545",
    "button_feature_bg":"#6f42c1","button_powerful_bg":"#fd7e14","button_devtool_bg":"#6c757d","button_nav_bg":"#17a2b8",
    "button_help_bg":"#20c997","button_utility_bg":"#6c757d"
}
COLOR_PRESETS = {
    "Classique v1 (Fond Bleu)":{"button_primary_bg":"#28a745","button_secondary_bg":"#007bff","button_tertiary_bg":"#ffc107","button_danger_bg":"#dc3545","button_feature_bg":"#6f42c1","button_powerful_bg":"#fd7e14","button_devtool_bg":"#6c757d","button_nav_bg":"#17a2b8","button_help_bg":"#20c997","button_utility_bg":"#6c757d"},
    "Océan Profond (Fond Bleu)":{"button_primary_bg":"#20B2AA","button_secondary_bg":"#4682B4","button_tertiary_bg":"#5F9EA0","button_danger_bg":"#DC143C","button_feature_bg":"#9370DB","button_powerful_bg":"#FF6347","button_devtool_bg":"#708090","button_nav_bg":"#48D1CC","button_help_bg":"#40E0D0","button_utility_bg":"#B0C4DE"},
    "Forêt d'Automne (Fond Bleu)":{"button_primary_bg":"#228B22","button_secondary_bg":"#CD853F","button_tertiary_bg":"#DAA520","button_danger_bg":"#B22222","button_feature_bg":"#9932CC","button_powerful_bg":"#FF8C00","button_devtool_bg":"#A0522D","button_nav_bg":"#2E8B57","button_help_bg":"#32CD32","button_utility_bg":"#BC8F8F"},
    "Coucher de Soleil (Fond Bleu)":{"button_primary_bg":"#FF7F50","button_secondary_bg":"#FFA500","button_tertiary_bg":"#FFD700","button_danger_bg":"#FF4500","button_feature_bg":"#DA70D6","button_powerful_bg":"#FF1493","button_devtool_bg":"#CD5C5C","button_nav_bg":"#FF6347","button_help_bg":"#FFA07A","button_utility_bg":"#F0E68C"},
    "Minimaliste Moderne (Fond Bleu)":{"button_primary_bg":"#00CED1","button_secondary_bg":"#87CEEB","button_tertiary_bg":"#F5F5DC","button_danger_bg":"#FF6B6B","button_feature_bg":"#DDA0DD","button_powerful_bg":"#FFA500","button_devtool_bg":"#C0C0C0","button_nav_bg":"#20B2AA","button_help_bg":"#98FB98","button_utility_bg":"#D3D3D3"},
    "Ancien (Fond Noir)":{"button_primary_bg":"#98FB98","button_secondary_bg":"#ADD8E6","button_tertiary_bg":"#EEE8AA","button_danger_bg":"#F08080","button_feature_bg":"#E6E6FA","button_powerful_bg":"#FFA07A","button_devtool_bg":"#DCDCDC","button_nav_bg":"#AFEEEE","button_help_bg":"#7FFFD4","button_utility_bg":"#D3D3D3"}
}

DEFAULT_CONFIG_PLACEHOLDERS = {
    "protection_placeholders": {
        "code_prefix": "RENPY_CODE_001",
        "asterisk_prefix": "RENPY_ASTERISK_001",
        "tilde_prefix": "RENPY_TILDE_001",
        "empty_prefix": "RENPY_EMPTY"
    }
}

# Config par défaut
DEFAULT_CONFIG = {
    "html_reports_enabled": True,
    "editor_custom_paths": {
        'VSCode': '',
        'Sublime Text': '',
        'Notepad++': '',
        'Atom/Pulsar': ''
    },
    "protection_placeholders": {
        "code_prefix": "RENPY_CODE_001",
        "asterisk_prefix": "RENPY_ASTERISK_001",
        "tilde_prefix": "RENPY_TILDE_001",
        "empty_prefix": "RENPY_EMPTY"
    },
    "project_sync_enabled": True,
    "notification_mode": "status_only",
    "project_progress_tracking": True,
    "html_reports_priority": True,
    "log_format": "html",
    "html_reports_theme": "dark",
    "auto_enable_debug_on_init_errors": True,
    "last_directory":"","auto_open_files":True,"auto_open_folders":True,"language":"fr","theme_colors":THEME_COLORS_DEFAULT,
    "debug_mode":False,"debug_level":3,
    "html_auto_refresh": True,
    "html_auto_refresh_seconds": 30,
    "extraction_detect_duplicates":True,"default_save_mode":"overwrite",
    "extraction_excluded_files":"",
    "cleanup_excluded_files":"common.rpy",
    "coherence_check_variables":True,"coherence_check_tags":True,"coherence_check_special_codes":True,"coherence_check_untranslated":True,"coherence_check_ellipsis":True,
    "coherence_check_escape_sequences":True,"coherence_check_percentages":True,"coherence_check_quotations":True,"coherence_check_parentheses":True,
    "coherence_check_syntax":True,"coherence_check_deepl_ellipsis":True,"coherence_check_isolated_percent":True,"coherence_check_line_structure":True,"coherence_check_length_difference":True,
    "coherence_custom_exclusions":{},
    "coherence_excluded_files":"",
    "coherence_auto_open_report":True,
    "realtime_editor_enabled":True,"realtime_monitoring_interval":200,"realtime_auto_backup":True,"realtime_default_language":"french",
    "editor_font_size":9,"realtime_log_retention_days":7,"realtime_max_log_size_mb":10,"default_online_translator":"Google","groq_api_key":"","groq_custom_instructions":"","groq_translation_style":"Naturel","groq_game_context":"Général","groq_temperature":0.3,
    "current_renpy_project":"","renpy_sdk_path":"","renpy_default_language":"french","renpy_auto_open_folder":True,"renpy_show_results_popup":True,
    "renpy_delete_rpa_after":False,"renpy_delete_source_after_rpa":False,
    "renpy_excluded_files":"common.rpy",
    "language_selector_integration":False,"developer_console_integration":False,
    "dark_mode":True,"show_output_path_display":False,
    "last_game_directory":"",
    "font_preferences":{"is_rtl":False,"apply_system_font":True,"individual_fonts":{
        "text_font":{"enabled":False,"font_name":"","font_path":""},
        "name_text_font":{"enabled":False,"font_name":"","font_path":""},
        "interface_text_font":{"enabled":False,"font_name":"","font_path":""},
        "button_text_font":{"enabled":False,"font_name":"","font_path":""},
        "choice_button_text_font":{"enabled":False,"font_name":"","font_path":""}}},
    "custom_extraction_patterns":[]
}
# Note: Les catégories de logs sont maintenant extraites dynamiquement depuis le fichier HTML
# Voir utils/logging.py → _extract_categories_from_log_file()

# Utilitaires santé
def get_health_color(health_percentage: float) -> str:
    """Retourne la couleur correspondant au pourcentage de santé."""
    try:
        h, t, c = health_percentage, HEALTH_CONFIG["health_thresholds"], HEALTH_CONFIG["health_colors"]
        return c["excellent"] if h>=t["excellent"] else c["good"] if h>=t["good"] else c["warning"] if h>=t["warning"] else c["critical"] if h>=t["critical"] else c["failed"]
    except Exception:
        return HEALTH_CONFIG["health_colors"]["warning"]

def get_health_message(health_percentage: float) -> str:
    """Retourne le message correspondant au pourcentage de santé."""
    try:
        h, t, m = health_percentage, HEALTH_CONFIG["health_thresholds"], MESSAGES
        return m["health_excellent"].format(health=h) if h>=t["excellent"] else m["health_good"].format(health=h) if h>=t["good"] else m["health_warning"].format(health=h) if h>=t["warning"] else m["health_critical"].format(health=h) if h>=t["critical"] else m["health_failed"].format(health=h)
    except Exception:
        return f"Santé du système: {health_percentage}%"

__all__ = [
    'VERSION','__version__','PROJECT_NAME','AUTHOR','PROJECT_DESCRIPTION','BASE_DIR','FOLDERS','FILE_NAMES','THEMES','WINDOW_CONFIG','SPECIAL_CODES','PROTECTION_ORDER','SUPPORTED_FILES',
    'MESSAGES','NOTIFICATION_CONFIG','CRITICAL_POPUPS','MESSAGE_PRIORITIES','DEFAULT_CONFIG','LOGGING_CONFIG','HEALTH_CONFIG',
    'get_executable_dir','ensure_folders_exist','ensure_game_structure','validate_game_name','get_health_color','get_health_message'
]
