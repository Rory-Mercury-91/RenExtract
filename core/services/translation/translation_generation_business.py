# core/business/translation_generation_business.py
# Logique métier complète pour la génération de traductions - Onglet 2
# VERSION COMPLÈTE avec support des polices GUI individuelles

"""
Logique métier complète pour la génération de traductions Ren'Py
- Génération via l'exécutable du jeu (méthode embedded)
- Génération via SDK Ren'Py
- Détection automatique de l'exécutable
- Création de fichiers de commande temporaires
- Monitoring en temps réel avec timeout
- Gestion complète des callbacks et interface
- Gestion des polices systèmes individuelles par élément GUI
"""

import os
import sys
import subprocess
import threading
import glob
import re
import time
import tempfile
import platform
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any, Tuple
from datetime import datetime

from infrastructure.logging.logging import log_message
from infrastructure.config.config import config_manager
from core.tools.sdk_manager import get_sdk_manager
from core.services.translation.font_manager import FontManager
from core.models.backup.unified_backup_manager import UnifiedBackupManager
from core.services.common.common import get_french_common_translations


class TranslationGenerationBusiness:
    """Logique métier complète pour la génération de traductions"""
    
    def __init__(self, tools_dir: str = None):
        """
        Initialise la logique métier de génération
        
        Args:
            tools_dir: Répertoire pour stocker les outils
        """
        if tools_dir is None:
            tools_dir = os.path.join(os.path.expanduser("~"), ".renextract_tools")
        
        self.tools_dir = tools_dir
        self.operation_cancelled = False
        self.current_project_path = None
        self.current_sdk_path = None
        
        # Gestionnaires d'outils
        self.sdk_manager = get_sdk_manager(tools_dir)
        self.backup_manager = UnifiedBackupManager()
        
        # Callbacks pour l'interface
        self.progress_callback: Optional[Callable] = None
        self.status_callback: Optional[Callable] = None
        self.completion_callback: Optional[Callable] = None
        self.error_callback: Optional[Callable] = None
        
        log_message("INFO", "TranslationGenerationBusiness initialisé", category="renpy_generator_tl")
    
    def set_callbacks(self, progress_callback: Callable = None, status_callback: Callable = None,
                     completion_callback: Callable = None, error_callback: Callable = None):
        """Configure les callbacks pour l'interface utilisateur"""
        self.progress_callback = progress_callback
        self.status_callback = status_callback
        self.completion_callback = completion_callback
        self.error_callback = error_callback
    
    def _on_progress_update(self, progress: int, message: str = ""):
        """Callback de progression"""
        if self.progress_callback:
            try: 
                self.progress_callback(progress, message)
            except Exception as e: 
                log_message("ATTENTION", f"Erreur callback progress: {e}", category="renpy_generator_tl")
    
    def _update_status(self, message: str):
        """Callback de statut"""
        if self.status_callback:
            try: 
                self.status_callback(message)
            except Exception as e: 
                log_message("ATTENTION", f"Erreur callback status: {e}", category="renpy_generator_tl")
        log_message("INFO", f"Status: {message}", category="renpy_generator_tl")
    
    def _notify_completion(self, success: bool, results: Dict):
        """Callback de fin d'opération"""
        if self.completion_callback:
            try: 
                self.completion_callback(success, results)
            except Exception as e: 
                log_message("ATTENTION", f"Erreur callback completion: {e}", category="renpy_generator_tl")
    
    def _notify_error(self, error_message: str, exception: Optional[Exception] = None):
        """Callback d'erreur"""
        if self.error_callback:
            try: 
                self.error_callback(error_message, exception)
            except Exception as e: 
                log_message("ATTENTION", f"Erreur callback error: {e}", category="renpy_generator_tl")
        log_message("ERREUR", f"Erreur: {error_message}", category="renpy_generator_tl")
    
    def get_available_fonts_with_accents(self):
        """Retourne la liste des polices système supportant les accents français"""
        system = platform.system().lower()
        
        fonts_info = []
        
        if system == "windows":
            fonts_info = [
                {"name": "Arial", "path": "C:/Windows/Fonts/arial.ttf", "description": "Police standard, très lisible"},
                {"name": "Calibri", "path": "C:/Windows/Fonts/calibri.ttf", "description": "Police moderne Office"},
                {"name": "Segoe UI", "path": "C:/Windows/Fonts/segoeui.ttf", "description": "Police système Windows"},
                {"name": "Verdana", "path": "C:/Windows/Fonts/verdana.ttf", "description": "Optimisée pour écran"},
                {"name": "Tahoma", "path": "C:/Windows/Fonts/tahoma.ttf", "description": "Compacte et claire"},
                {"name": "Times New Roman", "path": "C:/Windows/Fonts/times.ttf", "description": "Police serif classique"},
                {"name": "Georgia", "path": "C:/Windows/Fonts/georgia.ttf", "description": "Serif moderne pour écran"}
            ]
        elif system == "darwin":  # macOS
            fonts_info = [
                {"name": "Helvetica", "path": "/System/Library/Fonts/Helvetica.ttc", "description": "Police système Mac"},
                {"name": "Arial", "path": "/System/Library/Fonts/Arial.ttf", "description": "Sans-serif standard"},
                {"name": "San Francisco", "path": "/System/Library/Fonts/SFNS.ttf", "description": "Police moderne macOS"},
                {"name": "Lucida Grande", "path": "/System/Library/Fonts/LucidaGrande.ttc", "description": "Interface utilisateur"},
                {"name": "Times", "path": "/System/Library/Fonts/Times.ttc", "description": "Serif traditionnel"}
            ]
        else:  # Linux
            fonts_info = [
                {"name": "DejaVu Sans", "path": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "description": "Police libre standard"},
                {"name": "Liberation Sans", "path": "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", "description": "Alternative libre d'Arial"},
                {"name": "Ubuntu", "path": "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf", "description": "Police Ubuntu"},
                {"name": "Noto Sans", "path": "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf", "description": "Police Google"},
                {"name": "Source Sans Pro", "path": "/usr/share/fonts/truetype/source-sans-pro/SourceSansPro-Regular.ttf", "description": "Police Adobe"}
            ]
        
        # Filtrer les polices existantes
        available_fonts = []
        for font in fonts_info:
            if Path(font["path"]).exists():
                font["available"] = True
                available_fonts.append(font)
            else:
                font["description"] += " (fichier non trouvé)"
                font["available"] = False
                available_fonts.append(font)
        
        return available_fonts
    
    def get_system_font_for_french(self):
        """Retourne la meilleure police système pour les caractères français selon l'OS"""
        available_fonts = self.get_available_fonts_with_accents()
        
        # Prendre la première police disponible
        for font in available_fonts:
            if font.get("available", True):
                return Path(font["path"]), font["name"]
        
        # Fallback sur la première police même si non trouvée
        if available_fonts:
            return None, available_fonts[0]["name"]
        
        # Fallback ultime
        return None, "Arial"

    def _check_if_fontsize_exists(self, screen_lines: list) -> bool:
        """
        Vérifie si un contrôle de taille de police existe déjà dans le screen.
        """
        try:
            screen_content = '\n'.join(screen_lines)
            
            # Patterns pour détecter les contrôles de taille existants
            fontsize_patterns = [
                r'Preference\s*\(\s*["\']font\s+size["\']',  # Preference("font size", ...)
                r'label\s+_\(["\']Text\s+Size["\']\)',        # label _("Text Size")
                r'label\s+_\(["\']Taille\s+du\s+texte["\']', # label _("Taille du texte")
                r'bar.*font.*size',                           # bar avec font size
                r'slider.*font.*size',                        # slider avec font size
                r'textbutton.*font.*size',                    # textbutton pour font size
            ]
            
            for pattern in fontsize_patterns:
                if re.search(pattern, screen_content, re.IGNORECASE):
                    return True
                    
            return False
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur vérification taille police existante : {e}", category="renpy_generator_tl")
            return False

    def _find_screens_file(self, game_dir: str) -> str:
        """
        Cherche screens.rpy dans game/ et tous ses sous-dossiers, SAUF le dossier tl/
        
        Args:
            game_dir: Chemin vers le dossier game/
            
        Returns:
            str: Chemin complet vers screens.rpy ou None si introuvable
        """
        import os
        
        # D'abord, chercher à la racine de game/
        root_screens = os.path.join(game_dir, "screens.rpy")
        if os.path.exists(root_screens):
            return root_screens
        
        # Ensuite, chercher récursivement dans les sous-dossiers (sauf tl/)
        for root, dirs, files in os.walk(game_dir):
            # Exclure le dossier tl/ et tous ses sous-dossiers
            if 'tl' in dirs:
                dirs.remove('tl')
            
            # Chercher screens.rpy dans ce dossier
            if 'screens.rpy' in files:
                return os.path.join(root, 'screens.rpy')
        
        # Rien trouvé
        return None

    def _validate_say_screen_structure(self, project_path: str) -> tuple:
        """
        Vérifie si le screen say est compatible avec le contrôle de taille précis.
        Retourne (is_valid: bool, reason: str)
        """
        try:
            game_dir = os.path.join(project_path, "game")
            screens_file = os.path.join(game_dir, "screens.rpy")
            
            if not os.path.exists(screens_file):
                return False, "screens.rpy introuvable"
            
            with open(screens_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Marqueurs de validation
            required_markers = [
                r'screen\s+say\s*\(\s*who\s*,\s*what\s*\)',  # screen say(who, what):
                r'text\s+who\s+id\s+["\']who["\']',           # text who id "who"
                r'text\s+what\s+id\s+["\']what["\']'          # text what id "what"
            ]
            
            for marker in required_markers:
                if not re.search(marker, content, re.IGNORECASE):
                    return False, "Structure screen say non standard"
            
            return True, "Screen say standard détecté"
            
        except Exception as e:
            return False, f"Erreur validation: {e}"

    def create_individual_font_system_file(self, project_path: str, language: str, font_options: dict):
        """Version modifiée pour utiliser le gestionnaire centralisé de polices"""
        try:
            game_dir = os.path.join(project_path, "game")
            tl_lang_dir = Path(game_dir) / "tl" / language
            fonts_dir = tl_lang_dir / "fonts"
            
            tl_lang_dir.mkdir(parents=True, exist_ok=True)
            fonts_dir.mkdir(parents=True, exist_ok=True)
            
            individual_fonts = font_options.get('individual_fonts', {})
            enabled_fonts = {k: v for k, v in individual_fonts.items() if v.get('enabled', False)}
            
            if not enabled_fonts:
                return True, "Aucune police appliquée"
            
            tools_dir = config_manager.get('tools_directory', os.path.expanduser("~/.renextract_tools"))
            font_manager = FontManager(tools_dir)
            
            processed_fonts = {}
            copied_fonts = []
            
            for font_type, font_config in enabled_fonts.items():
                font_name = font_config.get('font_name', '')
                if not font_name:
                    continue
                
                # Rechercher la police dans le gestionnaire centralisé
                central_font_path = font_manager.get_font_for_project(font_name)
                
                if central_font_path and Path(central_font_path).exists():
                    source_font_path = Path(central_font_path)
                    target_font_path = fonts_dir / source_font_path.name
                    
                    # Copier depuis le gestionnaire centralisé vers le projet
                    if not target_font_path.exists() or target_font_path.stat().st_size != source_font_path.stat().st_size:
                        shutil.copy2(source_font_path, target_font_path)
                        if source_font_path.name not in copied_fonts:
                            copied_fonts.append(source_font_path.name)
                    
                    relative_font_path = f"tl/{language}/fonts/{source_font_path.name}"
                    
                    # Déterminer le type (système ou personnalisée)
                    is_custom = 'custom_fonts' in str(source_font_path)
                    
                    processed_fonts[font_type] = {
                        'font_name': font_name,
                        'relative_path': relative_font_path,
                        'use_relative': True,
                        'is_custom': is_custom
                    }
                else:
                    log_message("ATTENTION", f"Police non trouvée dans le gestionnaire centralisé : {font_name}", category="renpy_generator_tl")
                    continue
            
            if not processed_fonts:
                return False, "Aucune police valide trouvée"
            
            # Créer le fichier de configuration
            font_rpy = tl_lang_dir / "99_Z_FontSystem.rpy"
            self._write_individual_font_system_rpy_no_rtl(font_rpy, processed_fonts, language)
            
            # Construire le résumé
            applied_fonts = []
            for font_type, config in processed_fonts.items():
                font_desc = f"{font_type}: {config['font_name']}"
                if config.get('is_custom', False):
                    font_desc += " (personnalisée)"
                applied_fonts.append(font_desc)
            
            summary = f"Polices appliquées - {', '.join(applied_fonts)}"
            return True, summary
            
        except Exception as e:
            log_message("ERREUR", f"Erreur application polices centralisées : {e}", category="renpy_generator_tl")
            return False, str(e)

    def _write_individual_font_system_rpy_no_rtl(self, rpy_path: Path, processed_fonts: dict, lang: str):
        """Écrit le fichier de configuration avec polices individuelles - SANS RTL"""
        
        # Construire la configuration des polices
        font_configs = []
        for font_type, config in processed_fonts.items():
            if config['use_relative']:
                font_ref = f'"{config["relative_path"]}"'
                font_source = "personnalisée" if config.get('is_custom', False) else "fichier copié"
                comment = f"# {font_type}: {config['font_name']} ({font_source})"
            else:
                font_ref = f'"{config["font_name"]}"'
                comment = f"# {font_type}: {config['font_name']} (police système)"
            
            font_configs.append(f'        "{font_type}": {font_ref},  {comment}')
        
        font_config_str = '\n'.join(font_configs)
        
        content = f"""# Auto-generated - Polices GUI individuelles pour caractères français
# Supporte les caractères accentués français : é è à ç ù etc.
# Configuration avec polices individuelles par élément (système + personnalisées)

init python early hide:
    from renpy import exports as renpy
    import os
    
    if 'tl_font_cfg' not in globals():
        global tl_font_cfg
        tl_font_cfg = dict()
        global old_load_face
        old_load_face = renpy.text.font.load_face
        
        def _resolve_font_path(path):
            # Si c'est un chemin relatif, essayer de le résoudre via le loader
            if not os.path.isabs(path):
                try:
                    # Essayer via le loader Ren'Py
                    import renpy as _renpy_mod
                    if hasattr(_renpy_mod, 'loader') and _renpy_mod.loader.loadable(path):
                        resolved = _renpy_mod.loader.transfn(path)
                        if resolved:
                            return resolved.replace(chr(92), '/')
                        return path
                except Exception:
                    pass
                
                # Essayer relatif au gamedir
                try:
                    game_path = os.path.join(renpy.config.gamedir, path)
                    if os.path.exists(game_path):
                        return game_path.replace(chr(92), '/')
                except Exception:
                    pass
            
            # Retourner tel quel (nom de police système) ou convertir les backslashes
            if os.path.isabs(path):
                return path.replace(chr(92), '/')
            return path
        
        def my_load_face(fn, *args, **kwargs):
            # Vérifier si on est dans la langue cible
            lang = getattr(renpy.game.preferences, 'language', None)
            cfg = tl_font_cfg.get(lang)
            
            if cfg:
                # Déterminer le type de police GUI à partir du contexte
                gui_font_type = None
                
                # Correspondances GUI -> types de police
                gui_mappings = {{
                    'gui.text_font': 'text_font',
                    'gui.name_text_font': 'name_text_font', 
                    'gui.interface_text_font': 'interface_text_font',
                    'gui.button_text_font': 'button_text_font',
                    'gui.choice_button_text_font': 'choice_button_text_font'
                }}
                
                # Chercher si fn correspond à une police GUI connue
                for gui_var, font_type in gui_mappings.items():
                    try:
                        if hasattr(renpy.store, 'gui') and hasattr(renpy.store.gui, gui_var.split('.')[1]):
                            gui_font = getattr(renpy.store.gui, gui_var.split('.')[1])
                            if fn == gui_font and font_type in cfg.get('font_overrides', {{}}):
                                gui_font_type = font_type
                                break
                    except Exception:
                        pass
                
                # Appliquer le remplacement de police si trouvé
                if gui_font_type and gui_font_type in cfg.get('font_overrides', {{}}):
                    font_path = _resolve_font_path(cfg['font_overrides'][gui_font_type])
                    fn = font_path
            
            return old_load_face(fn, *args, **kwargs)
        
        renpy.text.font.load_face = my_load_face
        
        # Restaurer lors du reload
        old_reload_all = renpy.reload_all
        def my_reload_all():
            renpy.text.font.free_memory()
            renpy.text.font.load_face = old_load_face
            ret = old_reload_all()
            # ✅ CORRECTION : Restaurer la fonction originale pour éviter la récursion
            renpy.reload_all = old_reload_all
            return ret
        renpy.reload_all = my_reload_all
    
    # Configuration pour cette langue avec polices individuelles (SANS RTL)
    tl_font_cfg["{lang}"] = dict(
        font_overrides = {{
{font_config_str}
        }}
    )
"""
        rpy_path.write_text(content, encoding="utf-8")

    def create_french_common_file_pre_generation(self, project_path: str, language: str):
        """
        Crée le fichier common.rpy français AVANT la génération des traductions
        Utilise le module common.py pour récupérer le contenu complet
        SANS backup - écrasement direct avec vérification de contenu identique
        
        Args:
            project_path: Chemin vers le projet
            language: Langue cible
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Ne s'applique que pour le français
            if language.lower() != "french":
                return True, "Fichier common non applicable pour cette langue"
            
            game_dir = os.path.join(project_path, "game")
            tl_lang_dir = Path(game_dir) / "tl" / language
            
            # Créer les dossiers nécessaires
            tl_lang_dir.mkdir(parents=True, exist_ok=True)
            
            # Chemin de destination
            common_file = tl_lang_dir / "common.rpy"
            
            # Récupérer le nouveau contenu depuis le module common
            try:
                from core.services.common.common import get_french_common_translations
                new_common_content = get_french_common_translations()
            except Exception as e:
                log_message("ERREUR", f"Erreur import contenu common français : {e}", category="renpy_generator_tl")
                return False, f"Impossible de charger le contenu des traductions : {e}"
            
            # Vérifier si le fichier existe déjà et comparer les lignes de commentaires spécifiques
            if common_file.exists():
                try:
                    # Lire le fichier existant
                    existing_content = common_file.read_text(encoding="utf-8")
                    
                    # Extraire les premières lignes des deux contenus
                    existing_lines = existing_content.split('\n')
                    new_lines = new_common_content.split('\n')
                    
                    # Vérifier les lignes de commentaires spécifiques du fichier généré automatiquement
                    # On cherche les marqueurs caractéristiques du fichier common de RenExtract
                    signature_markers = [
                        "# TODO: Translation updated at",
                        "# Fichier common français - Créé avant génération TL par RenExtract", 
                        "# Traductions des éléments communs de l'interface Ren'Py"
                    ]
                    
                    # Vérifier si les 3 premières lignes de l'existant correspondent aux marqueurs
                    matches = 0
                    for i, marker in enumerate(signature_markers):
                        if i < len(existing_lines):
                            existing_line = existing_lines[i].strip()
                            if marker in existing_line or existing_line.startswith(marker.split()[0]):
                                matches += 1
                    
                    # Si au moins 2 des 3 marqueurs correspondent, c'est déjà notre fichier
                    if matches >= 2:
                        log_message("INFO", "Fichier common français RenExtract déjà présent (marqueurs détectés)", category="renpy_generator_tl")
                        return True, "Fichier common.rpy RenExtract déjà installé"
                        
                except Exception as e:
                    log_message("ATTENTION", f"Erreur lors de la vérification du fichier existant : {e}", category="renpy_generator_tl")
                    # Continuer avec l'écriture en cas d'erreur de lecture
            
            # Écrire le fichier directement (pas de backup)
            common_file.write_text(new_common_content, encoding="utf-8", newline="\n")
            
            # LOG SEULEMENT - PAS DE CALLBACK NOTIFICATION
            log_message("INFO", f"Fichier common français créé/écrasé depuis module : {common_file.name}", category="renpy_generator_tl")
            return True, f"Fichier common.rpy généré avec traductions françaises"
            
        except Exception as e:
            log_message("ERREUR", f"Erreur création fichier common français depuis module : {e}", category="renpy_generator_tl")
            return False, f"Erreur lors de la création : {e}"

    def generate_translations_embedded_threaded(self, project_path: str, language: str = "french", options: Optional[Dict] = None,
                                              progress_callback: Optional[Callable] = None,
                                              status_callback: Optional[Callable] = None,
                                              completion_callback: Optional[Callable] = None) -> threading.Thread:
        """
        Lance la génération de traductions embarquée dans un thread
        
        Args:
            project_path: Chemin vers le projet
            language: Langue cible
            options: Options de génération
            progress_callback: Callback de progression
            status_callback: Callback de statut
            completion_callback: Callback de fin
            
        Returns:
            Thread d'exécution
        """
        def worker():
            start_time = time.time()
            try:
                self.current_project_path = project_path
                result = self.generate_translations_embedded(
                    project_path, language, options, 
                    progress_callback, status_callback
                )
                result['execution_time'] = time.time() - start_time
                
                # Ajouter un résumé synthétique pour le popup
                if result['success']:
                    files_count = len(result.get('translation_files', []))
                    summary_text = f"Génération réussie pour '{language}': {files_count} fichiers créés"
                    if result.get('font_applied'):
                        summary_text += f" ({result.get('font_summary', 'polices GUI appliquées')})"
                    
                    result['summary'] = {
                        'generation': summary_text,
                        'output_folder': result.get('output_folder', ''),
                        'execution_time': f"Temps d'exécution: {result['execution_time']:.1f}s"
                    }
                else:
                    result['summary'] = {
                        'generation': f"Échec de la génération pour '{language}'",
                        'alternative_method_url': "https://f95zone.to/threads/unren-bat-v1-0-11d-rpa-extractor-rpyc-decompiler-console-developer-menu-enabler.3083/",
                        'errors': result.get('errors', [])
                    }
                
                if not self.operation_cancelled and completion_callback:
                    completion_callback(result['success'], result)
                elif not self.operation_cancelled and self.completion_callback:
                    self.completion_callback(result['success'], result)
                    
            except Exception as e:
                if not self.operation_cancelled:
                    error_result = {
                        'success': False,
                        'errors': [f"Erreur inattendue dans le thread de génération: {e}"],
                        'execution_time': time.time() - start_time,
                        'summary': {
                            'generation': f"Erreur critique lors de la génération pour '{language}'",
                            'alternative_method_url': "https://f95zone.to/threads/unren-bat-v1-0-11d-rpa-extractor-rpyc-decompiler-console-developer-menu-enabler.3083/",
                            'errors': [str(e)]
                        }
                    }
                    if completion_callback:
                        completion_callback(False, error_result)
                    elif self.completion_callback:
                        self.completion_callback(False, error_result)
                log_message("ERREUR", f"Erreur dans le thread de génération : {e}", category="renpy_generator_tl")
            finally:
                if self.operation_cancelled:
                    cancelled_result = {
                        'success': False,
                        'cancelled': True,
                        'errors': ["Opération annulée par l'utilisateur."],
                        'execution_time': time.time() - start_time,
                        'summary': {
                            'generation': f"Génération annulée pour '{language}'"
                        }
                    }
                    if completion_callback:
                        completion_callback(False, cancelled_result)
                    elif self.completion_callback:
                        self.completion_callback(False, cancelled_result)
                self.current_project_path = None
        
        self.operation_cancelled = False
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        
        log_message("INFO", f"Génération de traductions lancée en arrière-plan pour la langue : {language}", category="renpy_generator_tl")
        return thread
    
    def generate_translations_embedded(self, project_path: str, language: str = "french", options: Optional[Dict] = None,
                                    progress_callback: Optional[Callable] = None,
                                    status_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Génère les fichiers de traduction via l'exécutable du jeu avec monitoring temps réel
        ORDRE: common.rpy et screen.rpy AVANT la génération TL
        MODIFIÉ: Support polices personnalisées sans RTL
        
        Args:
            project_path: Chemin vers le projet
            language: Langue cible
            options: Options de génération
            progress_callback: Callback de progression
            status_callback: Callback de statut
            
        Returns:
            Dict avec les résultats de l'opération
        """
        result = {'success': False, 'errors': [], 'warnings': [], 'translation_files': [], 'output_folder': None, 'language': language}
        start_time = time.time()
        command_filepath = None
        
        if options is None:
            options = {}
        
        try:
            if self.operation_cancelled:
                raise InterruptedError("Opération annulée.")
            
            # === VALIDATION DU PROJET ===
            if progress_callback:
                progress_callback(5, "Validation du projet...")
            if status_callback:
                status_callback("Validation du projet...")
            
            if not os.path.isdir(project_path):
                result['errors'].append("Le chemin du projet n'existe pas.")
                return result
            
            game_dir = os.path.join(project_path, "game")
            if not os.path.isdir(game_dir):
                result['errors'].append("Le dossier 'game' n'existe pas dans le projet.")
                return result

            # === PRÉPARATION FICHIERS FRANÇAIS AVANT GÉNÉRATION ===
            # Common.rpy français si demandé
            if options.get('create_common_file', False) and language.lower() == "french":
                if progress_callback:
                    progress_callback(6, "Préparation du fichier common français...")
                if status_callback:
                    status_callback("Préparation du fichier common français...")
                
                try:
                    common_success, common_message = self.create_french_common_file_pre_generation(project_path, language)
                    if common_success:
                        result['french_common_prepared'] = True
                        result['french_common_message'] = common_message
                    else:
                        result['warnings'].append(f"Common français : {common_message}")
                except Exception as common_error:
                    result['warnings'].append(f"Erreur common français : {common_error}")

            # Screen.rpy français si demandé
            screen_option = options.get('create_screen_file', False)
            is_french = language.lower() == "french"
            
            if screen_option and is_french:
                if progress_callback:
                    progress_callback(8, "Préparation du fichier screens français...")
                if status_callback:
                    status_callback("Préparation du fichier screens français...")
                
                try:
                    screens_success, screens_message = self.create_french_screen_file_pre_generation(project_path, language)
                    if screens_success:
                        result['french_screens_prepared'] = True
                        result['french_screens_message'] = screens_message
                    else:
                        result['warnings'].append(f"Screens français : {screens_message}")
                except Exception as screens_error:
                    result['warnings'].append(f"Erreur screens français : {screens_error}")

            # === DÉTECTION EXÉCUTABLE ET PRÉPARATION ===
            if progress_callback:
                progress_callback(10, "Détection de l'exécutable du jeu...")
            if status_callback:
                status_callback("Détection de l'exécutable du jeu...")
            
            executable_path = self.detect_game_executable(project_path)
            if not executable_path:
                result['errors'].append("Aucun exécutable de jeu trouvé dans le projet.")
                return result
            
            if progress_callback:
                progress_callback(20, "Initialisation de Ren'Py...")
            if status_callback:
                status_callback("Initialisation de Ren'Py...")
            
            command_filepath = self.create_translation_command_file(project_path, language)
            
            if progress_callback:
                progress_callback(30, "Analyse des fichiers sources...")
            
            cmd = self._build_execution_command(executable_path)
            
            env = os.environ.copy()
            env['RENPY_PLATFORM'] = 'all'
            
            startupinfo = None
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
            
            if progress_callback:
                progress_callback(40, "Génération des traductions...")
            if status_callback:
                status_callback("Génération des traductions...")
            
            # ✅ NOUVEAU : Supprimer traceback.txt s'il existe
            traceback_path = os.path.join(project_path, "traceback.txt")
            if os.path.exists(traceback_path):
                try:
                    os.remove(traceback_path)
                    log_message("INFO", "traceback.txt supprimé avant génération", category="renpy_generator_tl")
                except Exception as e:
                    log_message("ATTENTION", f"Impossible de supprimer traceback.txt : {e}", category="renpy_generator_tl")
            
            # === GÉNÉRATION TRADUCTIONS REN'PY ===
            # ✅ CORRECTION : Masquer la fenêtre console sur Windows
            creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            
            process = subprocess.Popen(
                cmd,
                cwd=project_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='ignore',
                startupinfo=startupinfo,
                env=env,
                creationflags=creationflags
            )
            
            # ✅ NOUVEAU : Surveillance traceback.txt en temps réel
            traceback_detected = False
            
            def monitor_traceback():
                nonlocal traceback_detected
                while process.poll() is None:
                    if os.path.exists(traceback_path):
                        traceback_detected = True
                        log_message("ERREUR", f"traceback.txt détecté pendant la génération Ren'Py", category="renpy_generator_tl")
                        # Arrêter le processus si traceback détecté
                        try:
                            process.terminate()
                        except Exception:
                            pass
                        break
                    time.sleep(0.5)  # Vérifier toutes les 500ms
            
            # Démarrer la surveillance
            monitor_thread = threading.Thread(target=monitor_traceback, daemon=True)
            monitor_thread.start()
            
            # Monitoring en temps réel avec timeout adaptatif
            tl_folder = os.path.join(game_dir, "tl", language)
            generation_start_time = time.time()
            timeout_seconds = 600  # 10 minutes d'inactivité (pas de nouveaux fichiers)
            initial_timeout = 300  # 5 minutes avant le premier fichier
            last_file_count = 0
            last_activity_time = time.time()  # Dernière fois qu'un nouveau fichier a été détecté
            first_file_detected = False  # Indique si au moins un fichier a été généré
            
            while process.poll() is None:
                # Vérifier si traceback a été détecté
                if traceback_detected:
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
                    
                    result['errors'].append(
                        "Erreur Ren'Py détectée (traceback.txt généré). "
                        "Le problème vient du jeu, pas de RenExtract. "
                        "Consultez traceback.txt dans le dossier du projet pour plus de détails."
                    )
                    log_message("ERREUR", "Génération annulée - traceback.txt détecté lors de la génération", category="renpy_generator_tl")
                    return result
                
                elapsed_time = time.time() - generation_start_time
                
                # Progression basée sur les fichiers générés
                current_files = 0
                if os.path.isdir(tl_folder):
                    current_files = len([f for f in os.listdir(tl_folder) if f.endswith('.rpy')])
                
                # ✅ NOUVEAU : Détecter si de nouveaux fichiers sont générés
                if current_files > last_file_count:
                    # Nouveaux fichiers détectés - réinitialiser le timer d'inactivité
                    last_activity_time = time.time()
                    last_file_count = current_files
                    if not first_file_detected:
                        first_file_detected = True
                        log_message("INFO", f"Premier fichier généré après {int(elapsed_time)}s", category="renpy_generator_tl")
                    else:
                        log_message("DEBUG", f"Progression détectée : {current_files} fichiers générés", category="renpy_generator_tl")
                
                # ✅ NOUVEAU : Timeout adaptatif basé sur l'inactivité
                if first_file_detected:
                    # Une fois qu'au moins un fichier a été généré, utiliser le timeout d'inactivité
                    inactivity_time = time.time() - last_activity_time
                    if inactivity_time > timeout_seconds:
                        # Aucun nouveau fichier depuis 2 minutes - probablement bloqué
                        log_message("ATTENTION", f"Timeout adaptatif : Aucun nouveau fichier depuis {int(inactivity_time)}s ({current_files} fichiers au total)", category="renpy_generator_tl")
                        process.terminate()
                        try:
                            process.wait(timeout=5)
                        except subprocess.TimeoutExpired:
                            process.kill()
                            process.wait()
                        
                        result['errors'].append(
                            f"La génération semble bloquée (aucun nouveau fichier depuis {int(inactivity_time)}s). "
                            f"{current_files} fichier(s) généré(s) avant l'arrêt. "
                            "Le projet pourrait être trop volumineux ou il y a un problème avec Ren'Py."
                        )
                        return result
                else:
                    # Aucun fichier généré encore - utiliser le timeout initial
                    if elapsed_time > initial_timeout:
                        log_message("ATTENTION", f"Timeout initial : Aucun fichier généré après {int(elapsed_time)}s", category="renpy_generator_tl")
                        process.terminate()
                        try:
                            process.wait(timeout=5)
                        except subprocess.TimeoutExpired:
                            process.kill()
                            process.wait()
                        
                        result['errors'].append(
                            f"La génération n'a pas démarré correctement (aucun fichier généré après {int(elapsed_time)}s). "
                            "Vérifiez que Ren'Py fonctionne correctement avec ce projet."
                        )
                        return result
                
                estimated_progress = min(30, (current_files * 30) // max(20, 1))
                total_progress = 40 + estimated_progress
                
                minutes = int(elapsed_time // 60)
                seconds = int(elapsed_time % 60)
                time_str = f"{minutes}m {seconds:02d}s" if minutes > 0 else f"{seconds}s"
                
                status_message = f"Génération des traductions... ({time_str})"
                if current_files > 0:
                    status_message += f" - {current_files} fichiers générés"
                
                if progress_callback:
                    progress_callback(total_progress, status_message)
                
                time.sleep(0.5)
            
            stdout, stderr = process.communicate()
            
            # ✅ Vérifier si traceback.txt a été généré pendant l'exécution
            if traceback_detected or os.path.exists(traceback_path):
                result['errors'].append(
                    "Erreur Ren'Py détectée (traceback.txt généré). "
                    "Le problème vient du jeu, pas de RenExtract. "
                    "Consultez traceback.txt dans le dossier du projet pour plus de détails."
                )
                log_message("ERREUR", f"traceback.txt détecté - Erreur Ren'Py lors de la génération", category="renpy_generator_tl")
                return result
            
            # === VÉRIFICATION RÉSULTATS GÉNÉRATION ===
            if os.path.isdir(tl_folder):
                result['output_folder'] = tl_folder
                
                translation_files = []
                for root, _, files in os.walk(tl_folder):
                    if self.operation_cancelled:
                        raise InterruptedError("Opération annulée.")
                    for file in files:
                        if self.operation_cancelled:
                            raise InterruptedError("Opération annulée.")
                        if file.endswith('.rpy'):
                            translation_files.append(os.path.join(root, file))
                
                result['translation_files'] = translation_files
                result['success'] = True
                
                # === MODULES COMPLÉMENTAIRES ===
                # Application des polices GUI si demandées
                if options.get('apply_system_font', False):
                    if progress_callback:
                        progress_callback(85, "Application des polices GUI...")
                    if status_callback:
                        status_callback("Application des polices GUI...")
                    
                    try:
                        font_options = {
                            'individual_fonts': options.get('individual_fonts', {})
                        }
                        
                        font_success, font_info = self.create_individual_font_system_file(project_path, language, font_options)
                        
                        if font_success:
                            result['font_applied'] = True
                            result['font_summary'] = font_info
                        else:
                            result['warnings'].append(f"Impossible d'appliquer les polices GUI : {font_info}")
                            
                    except Exception as font_error:
                        result['warnings'].append(f"Erreur lors de l'application des polices GUI : {font_error}")
                
                # Console développeur si demandée (indépendant)
                if options.get('create_developer_console', False):
                    if progress_callback:
                        progress_callback(94, "Création de la console développeur...")
                    if status_callback:
                        status_callback("Création de la console développeur...")
                    
                    try:
                        cons_success, cons_message = self.create_developer_console_file(project_path, language)
                        
                        if cons_success:
                            result['developer_console_created'] = True
                            result['developer_console_message'] = cons_message
                        else:
                            result['warnings'].append(f"Console développeur : {cons_message}")
                            
                    except Exception as cons_error:
                        result['warnings'].append(f"Erreur console développeur : {cons_error}")

                # Options screen preferences avancées - Nouveau système modulaire unifié
                # Vérifier si les options avancées sont passées explicitement
                if options and 'advanced_screen_options' in options:
                    advanced_options = options['advanced_screen_options']
                else:
                    # Sinon, charger depuis la config
                    advanced_options = config_manager.get_advanced_screen_options()
                
                # Si au moins une option est activée
                if any(advanced_options.values()):
                    if progress_callback:
                        progress_callback(96, "Création des options screen preferences...")
                    if status_callback:
                        status_callback("Création des options screen preferences...")
                    
                    try:
                        adv_success, adv_message = self.generate_advanced_screen_preferences(
                            project_path,
                            language,
                            advanced_options
                        )
                        
                        if adv_success:
                            result['screen_preferences_created'] = True
                            result['screen_preferences_message'] = adv_message
                        else:
                            result['warnings'].append(f"Options screen preferences : {adv_message}")
                            
                    except Exception as adv_error:
                        result['warnings'].append(f"Erreur options screen preferences : {adv_error}")
                        
                if progress_callback:
                    progress_callback(98, "Finalisation...")
            else:
                # Échec de la génération
                error_msg = "La génération a échoué. "
                
                if process.returncode != 0:
                    error_msg += f"Code de sortie : {process.returncode}. "
                
                if stderr:
                    error_msg += f"Erreur : {stderr[:200]}"
                elif stdout:
                    if "error" in stdout.lower() or "traceback" in stdout.lower():
                        error_msg += f"Sortie : {stdout[:200]}"
                
                result['errors'].append(error_msg)
                    
        except InterruptedError as ie:
            result['errors'].append(str(ie))
        except Exception as e:
            result['errors'].append(f"Erreur inattendue : {e}")
        finally:
            # === NETTOYAGE ===
            temp_files_to_clean = []
            
            if command_filepath:
                temp_files_to_clean.append(command_filepath)
                rpyc_filepath = command_filepath.replace('.rpy', '.rpyc')
                temp_files_to_clean.append(rpyc_filepath)
            
            for temp_file in temp_files_to_clean:
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except Exception as e:
                        result['warnings'].append(f"Impossible de supprimer {os.path.basename(temp_file)}: {e}")
            
            # === RÉSUMÉ FINAL - SECTION À MODIFIER ===
            if result['success']:
                files_count = len(result.get('translation_files', []))
                summary_parts = [f"Génération réussie pour '{language}': {files_count} fichiers créés"]
                
                # VOICI LA PARTIE additional_features À REMPLACER :
                additional_features = []
                if result.get('french_common_prepared'):
                    additional_features.append("fichier common français")
                if result.get('french_screens_prepared'):
                    additional_features.append("fichier screens français")
                if result.get('font_applied'):
                    additional_features.append("polices GUI appliquées")
                if result.get('developer_console_created'):
                    additional_features.append("console développeur activée")
                if result.get('combined_selectors_created'):
                    additional_features.append("sélecteur langue + contrôle taille")
                elif result.get('language_selector_created'):
                    additional_features.append("sélecteur de langue intégré")
                elif result.get('fontsize_selector_created'):
                    additional_features.append("contrôle taille police")
                
                if additional_features:
                    final_message = summary_parts[0] + " (" + ", ".join(additional_features) + ")"
                else:
                    final_message = summary_parts[0]
                
                if status_callback:
                    status_callback(final_message)
            else:
                if status_callback:
                    status_callback("Échec de la génération")
        
        result['execution_time'] = time.time() - start_time
        return result
    
    def generate_translations_with_sdk_threaded(self, project_path: str, language: str = "french", options: Optional[Dict] = None,
                                              progress_callback: Optional[Callable] = None,
                                              status_callback: Optional[Callable] = None,
                                              completion_callback: Optional[Callable] = None) -> threading.Thread:
        """
        Lance la génération de traductions via SDK dans un thread
        
        Args:
            project_path: Chemin vers le projet
            language: Langue cible
            options: Options de génération
            progress_callback: Callback de progression
            status_callback: Callback de statut
            completion_callback: Callback de fin
            
        Returns:
            Thread d'exécution
        """
        def worker():
            start_time = time.time()
            try:
                self.current_project_path = project_path
                result = self.generate_translations_with_sdk(
                    project_path, language, options, 
                    progress_callback, status_callback
                )
                result['execution_time'] = time.time() - start_time
                
                # Ajouter un résumé synthétique pour le popup
                if result['success']:
                    files_count = len(result.get('translation_files', []))
                    result['summary'] = {
                        'generation': f"Génération SDK réussie pour '{language}': {files_count} fichiers créés",
                        'output_folder': result.get('output_folder', ''),
                        'execution_time': f"Temps d'exécution: {result['execution_time']:.1f}s"
                    }
                else:
                    result['summary'] = {
                        'generation': f"Échec de la génération SDK pour '{language}'",
                        'alternative_method_url': "https://f95zone.to/threads/unren-bat-v1-0-11d-rpa-extractor-rpyc-decompiler-console-developer-menu-enabler.3083/",
                        'errors': result.get('errors', [])
                    }
                
                if not self.operation_cancelled and completion_callback:
                    completion_callback(result['success'], result)
                elif not self.operation_cancelled and self.completion_callback:
                    self.completion_callback(result['success'], result)
                    
            except Exception as e:
                if not self.operation_cancelled:
                    error_result = {
                        'success': False,
                        'errors': [f"Erreur inattendue dans le thread SDK: {e}"],
                        'execution_time': time.time() - start_time,
                        'summary': {
                            'generation': f"Erreur critique lors de la génération SDK pour '{language}'",
                            'alternative_method_url': "https://f95zone.to/threads/unren-bat-v1-0-11d-rpa-extractor-rpyc-decompiler-console-developer-menu-enabler.3083/",
                            'errors': [str(e)]
                        }
                    }
                    if completion_callback:
                        completion_callback(False, error_result)
                    elif self.completion_callback:
                        self.completion_callback(False, error_result)
            finally:
                if self.operation_cancelled:
                    cancelled_result = {
                        'success': False,
                        'cancelled': True,
                        'errors': ["Opération annulée par l'utilisateur."],
                        'execution_time': time.time() - start_time,
                        'summary': {
                            'generation': f"Génération SDK annulée pour '{language}'"
                        }
                    }
                    if completion_callback:
                        completion_callback(False, cancelled_result)
                    elif self.completion_callback:
                        self.completion_callback(False, cancelled_result)
                self.current_project_path = None
        
        self.operation_cancelled = False
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        
        log_message("INFO", f"Génération SDK lancée en arrière-plan pour la langue : {language}", category="renpy_generator_tl")
        return thread
    
    def generate_translations_with_sdk(self, project_path: str, language: str = "french", options: Optional[Dict] = None,
                                     progress_callback: Optional[Callable] = None,
                                     status_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Génère les fichiers de traduction via le SDK Ren'Py
        
        Args:
            project_path: Chemin vers le projet
            language: Langue cible
            options: Options de génération
            progress_callback: Callback de progression
            status_callback: Callback de statut
            
        Returns:
            Dict avec les résultats de l'opération
        """
        result = {'success': False, 'errors': [], 'warnings': [], 'translation_files': [], 'output_folder': None, 'language': language}
        start_time = time.time()
        
        try:
            if self.operation_cancelled:
                raise InterruptedError("Opération annulée.")
            
            if progress_callback:
                progress_callback(5, "Validation du projet...")
            elif self.progress_callback:
                self.progress_callback(5, "Validation du projet...")
                
            if status_callback:
                status_callback("Validation du projet...")
            elif self.status_callback:
                self.status_callback("Validation du projet...")
            
            log_message("INFO", f"Début de la génération SDK pour la langue : {language}", category="renpy_generator_tl")
            
            # Validation du projet
            if not os.path.isdir(project_path):
                result['errors'].append("Le chemin du projet n'existe pas.")
                return result
            
            game_dir = os.path.join(project_path, "game")
            if not os.path.isdir(game_dir):
                result['errors'].append("Le dossier 'game' n'existe pas dans le projet.")
                return result
            
            if progress_callback:
                progress_callback(15, "Recherche du SDK Ren'Py...")
            elif self.progress_callback:
                self.progress_callback(15, "Recherche du SDK Ren'Py...")
                
            if status_callback:
                status_callback("Recherche du SDK Ren'Py...")
            elif self.status_callback:
                self.status_callback("Recherche du SDK Ren'Py...")
            
            # Obtenir le SDK optimal
            sdk_path = self.sdk_manager.get_sdk_for_cleaning()
            if not sdk_path:
                result['errors'].append("Aucun SDK Ren'Py trouvé ou téléchargeable.")
                return result
            
            self.current_sdk_path = sdk_path
            renpy_exe = self.sdk_manager.get_renpy_executable(sdk_path)
            if not renpy_exe:
                result['errors'].append("Exécutable Ren'Py non trouvé dans le SDK.")
                return result
            
            if progress_callback:
                progress_callback(30, "Génération via SDK...")
            elif self.progress_callback:
                self.progress_callback(30, "Génération via SDK...")
                
            if status_callback:
                status_callback("Génération via SDK...")
            elif self.status_callback:
                self.status_callback("Génération via SDK...")
            
            # Commande de génération
            cmd = [renpy_exe, project_path, "translate", language]
            
            log_message("INFO", f"Commande SDK : {' '.join(cmd)}", category="renpy_generator_tl")
            
            # Environnement propre
            env = os.environ.copy()
            env['RENPY_PLATFORM'] = 'all'
            
            startupinfo = None
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
            
            # ✅ NOUVEAU : Supprimer traceback.txt s'il existe
            traceback_path = os.path.join(project_path, "traceback.txt")
            if os.path.exists(traceback_path):
                try:
                    os.remove(traceback_path)
                    log_message("INFO", "traceback.txt supprimé avant génération SDK", category="renpy_generator_tl")
                except Exception as e:
                    log_message("ATTENTION", f"Impossible de supprimer traceback.txt : {e}", category="renpy_generator_tl")
            
            # Lancer le processus avec monitoring
            # ✅ CORRECTION : Masquer la fenêtre console sur Windows
            creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='ignore',
                startupinfo=startupinfo,
                env=env,
                creationflags=creationflags
            )
            
            # ✅ NOUVEAU : Surveillance traceback.txt en temps réel
            traceback_detected = False
            
            def monitor_traceback():
                nonlocal traceback_detected
                while process.poll() is None:
                    if os.path.exists(traceback_path):
                        traceback_detected = True
                        log_message("ERREUR", f"traceback.txt détecté pendant la génération SDK Ren'Py", category="renpy_generator_tl")
                        # Arrêter le processus si traceback détecté
                        try:
                            process.terminate()
                        except Exception:
                            pass
                        break
                    time.sleep(0.5)  # Vérifier toutes les 500ms
            
            # Démarrer la surveillance
            monitor_thread = threading.Thread(target=monitor_traceback, daemon=True)
            monitor_thread.start()
            
            # Monitoring avec timeout
            tl_folder = os.path.join(game_dir, "tl", language)
            generation_start_time = time.time()
            timeout_seconds = 180  # 3 minutes pour SDK
            
            while process.poll() is None:
                # Vérifier si traceback a été détecté
                if traceback_detected:
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
                    
                    result['errors'].append(
                        "Erreur Ren'Py détectée (traceback.txt généré). "
                        "Le problème vient du jeu, pas de RenExtract. "
                        "Consultez traceback.txt dans le dossier du projet pour plus de détails."
                    )
                    log_message("ERREUR", "Génération SDK annulée - traceback.txt détecté", category="renpy_generator_tl")
                    return result
                elapsed_time = time.time() - generation_start_time
                
                if elapsed_time > timeout_seconds:
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
                    
                    result['errors'].append(f"La génération SDK a dépassé le temps limite (3 minutes).")
                    log_message("ERREUR", "Timeout lors de la génération SDK", category="renpy_generator_tl")
                    return result
                
                # Progression basée sur le temps
                progress_percent = min(70, 30 + int((elapsed_time / timeout_seconds) * 40))
                
                minutes = int(elapsed_time // 60)
                seconds = int(elapsed_time % 60)
                time_str = f"{minutes}m {seconds:02d}s" if minutes > 0 else f"{seconds}s"
                
                if progress_callback:
                    progress_callback(progress_percent, f"Génération SDK en cours... ({time_str})")
                elif self.progress_callback:
                    self.progress_callback(progress_percent, f"Génération SDK en cours... ({time_str})")
                
                time.sleep(1)
            
            # Récupérer la sortie
            stdout, stderr = process.communicate()
            
            # ✅ Vérifier si traceback.txt a été généré pendant l'exécution
            if traceback_detected or os.path.exists(traceback_path):
                result['errors'].append(
                    "Erreur Ren'Py détectée (traceback.txt généré). "
                    "Le problème vient du jeu, pas de RenExtract. "
                    "Consultez traceback.txt dans le dossier du projet pour plus de détails."
                )
                log_message("ERREUR", f"traceback.txt détecté - Erreur Ren'Py lors de la génération SDK", category="renpy_generator_tl")
                return result
            
            if progress_callback:
                progress_callback(80, "Vérification des résultats SDK...")
            elif self.progress_callback:
                self.progress_callback(80, "Vérification des résultats SDK...")
            
            # Vérifier les résultats
            if os.path.isdir(tl_folder):
                result['output_folder'] = tl_folder
                
                translation_files = []
                for root, _, files in os.walk(tl_folder):
                    if self.operation_cancelled:
                        raise InterruptedError("Opération annulée.")
                    for file in files:
                        if self.operation_cancelled:
                            raise InterruptedError("Opération annulée.")
                        if file.endswith('.rpy'):
                            translation_files.append(os.path.join(root, file))
                
                result['translation_files'] = translation_files
                result['success'] = True
                
                log_message("INFO", f"Génération SDK réussie ! {len(translation_files)} fichiers créés", category="renpy_generator_tl")
            else:
                error_msg = f"Génération SDK échouée. Code: {process.returncode}"
                if stderr:
                    error_msg += f" Erreur: {stderr[:200]}"
                result['errors'].append(error_msg)
                log_message("ERREUR", error_msg, category="renpy_generator_tl")
                
        except InterruptedError as ie:
            result['errors'].append(str(ie))
            log_message("INFO", str(ie), category="renpy_generator_tl")
        except Exception as e:
            result['errors'].append(f"Erreur inattendue SDK : {e}")
            log_message("ERREUR", f"Erreur génération SDK : {e}", category="renpy_generator_tl")
        finally:
            # Finaliser le statut
            if result['success']:
                if progress_callback:
                    progress_callback(100, f"Traductions SDK générées pour '{language}'")
                elif self.progress_callback:
                    self.progress_callback(100, f"Traductions SDK générées pour '{language}'")
            else:
                if progress_callback:
                    progress_callback(0, "Échec de la génération SDK")
                elif self.progress_callback:
                    self.progress_callback(0, "Échec de la génération SDK")
        
        result['execution_time'] = time.time() - start_time
        return result
    
    def detect_game_executable(self, project_path: str) -> Optional[str]:
        """
        Détecte automatiquement l'exécutable principal du jeu Ren'Py
        VERSION CORRIGÉE - Compatible avec les crochets dans les noms + évite les versions 32-bits
        
        Args:
            project_path: Chemin vers le projet
            
        Returns:
            Chemin vers l'exécutable ou None
        """
        # Cache pour éviter les doublons de logs lors des appels multiples
        cache_key = f"_last_detected_exe_{project_path}"
        if hasattr(self, cache_key):
            return getattr(self, cache_key)
        
        # Log supprimé : sera affiché seulement quand l'exécutable est trouvé
        
        if not os.path.isdir(project_path):
            log_message("ERREUR", f"Le chemin du projet n'existe pas : {project_path}", category="renpy_generator_tl")
            return None
        
        # Extensions selon la plateforme
        if sys.platform == "win32":  # Windows
            extensions = ['.exe']
            # Patterns spéciaux pour Windows
            special_suffixes = ['-32.exe', '-64.exe']
        elif sys.platform == "darwin":  # macOS
            extensions = ['.app', '.sh']
            special_suffixes = []
        else:  # Linux et autres Unix
            extensions = ['.sh', '.py']
            special_suffixes = []
        
        found_executables = []
        
        try:
            # Utiliser os.listdir() au lieu de glob pour éviter les problèmes avec []
            for filename in os.listdir(project_path):
                filepath = os.path.join(project_path, filename)
                
                if os.path.isfile(filepath):
                    filename_lower = filename.lower()
                    
                    # Vérifier les extensions principales
                    is_executable = any(filename_lower.endswith(ext) for ext in extensions)
                    
                    # Vérifier les suffixes spéciaux (Windows)
                    if not is_executable and special_suffixes:
                        is_executable = any(filename_lower.endswith(suffix) for suffix in special_suffixes)
                    
                    if is_executable:
                        # Exclure certains fichiers système
                        if not any(exclude in filename_lower for exclude in ['uninstall', 'setup', 'installer', 'update']):
                            found_executables.append(filepath)
        
        except Exception as e:
            log_message("ERREUR", f"Erreur lors de la lecture du dossier {project_path}: {e}", category="renpy_generator_tl")
            return None
        
        # Filtrer et trier par priorité (éviter les versions 32-bits)
        project_name = os.path.basename(project_path).lower()
        prioritized_executables = []
        standard_executables = []
        fallback_32bit = []
        
        for exe in found_executables:
            exe_name = os.path.basename(exe).lower()
            
            # Détecter les versions 32-bits à éviter
            is_32bit = any(marker in exe_name for marker in ['-32', '_32', '32bit', '32-bit'])
            
            # Détecter les versions 64-bits préférées
            is_64bit = any(marker in exe_name for marker in ['-64', '_64', '64bit', '64-bit'])
            
            # Priorité 1: Exécutables 64-bits avec nom du projet
            if is_64bit and any(word in exe_name for word in project_name.split('-')):
                prioritized_executables.insert(0, exe)
            # Priorité 2: Exécutables standard (ni 32 ni 64) avec nom du projet
            elif not is_32bit and not is_64bit and any(word in exe_name for word in project_name.split('-')):
                prioritized_executables.append(exe)
            # Priorité 3: Exécutables 64-bits sans nom du projet
            elif is_64bit:
                standard_executables.insert(0, exe)
            # Priorité 4: Exécutables standard sans nom du projet
            elif not is_32bit:
                standard_executables.append(exe)
            # Dernière option: versions 32-bits (à éviter)
            else:
                fallback_32bit.append(exe)
        
        # Combiner les listes par ordre de priorité
        all_executables = prioritized_executables + standard_executables + fallback_32bit
        
        if not all_executables:
            log_message("ERREUR", "Aucun exécutable trouvé dans le dossier du projet", category="renpy_generator_tl")
            return None
        
        # Prendre le premier exécutable trouvé (priorité la plus haute)
        selected_executable = all_executables[0]
        
        # Avertir si on utilise une version 32-bits
        selected_name = os.path.basename(selected_executable).lower()
        if any(marker in selected_name for marker in ['-32', '_32', '32bit', '32-bit']):
            log_message("ATTENTION", f"Version 32-bits sélectionnée par défaut : {os.path.basename(selected_executable)}", category="renpy_generator_tl")
        
        log_message("INFO", f"🎮 Exécutable détecté : {os.path.basename(selected_executable)}", category="renpy_generator_tl")
        if len(all_executables) > 1:
            log_message("DEBUG", f"Autres exécutables disponibles : {[os.path.basename(exe) for exe in all_executables[1:]]}", category="renpy_generator_tl")
        
        # Mettre en cache pour éviter les doublons de logs
        setattr(self, cache_key, selected_executable)
        
        return selected_executable
    
    def create_translation_command_file(self, project_path: str, language: str) -> str:
        """
        Crée le fichier temporaire .rpy pour déclencher la génération de traductions avec tous les paramètres nécessaires
        
        Args:
            project_path: Chemin vers le projet
            language: Langue cible
            
        Returns:
            Chemin vers le fichier de commande créé
        """
        log_message("INFO", f"Création du fichier de commande pour la langue : {language}", category="renpy_generator_tl")
        
        game_dir = os.path.join(project_path, "game")
        if not os.path.isdir(game_dir):
            raise FileNotFoundError("Le dossier 'game' n'existe pas dans le projet")
        
        # Nom du fichier temporaire
        command_filename = "00_translate_command_temp.rpy"
        command_filepath = os.path.join(game_dir, command_filename)
        
        # Contenu du fichier de commande avec TOUS les paramètres pour extraire dialogues ET strings
        command_content = f'''# Fichier temporaire généré par RenExtract
# Ce fichier sera automatiquement supprimé après génération

init python early hide:
    # La langue cible pour la traduction avec paramètres complets
    command = "translate {language} --min-priority 0 --max-priority 500"
    # Ces lignes préparent la commande pour Ren'Py
    renpy.game.args.command = command.split()[0]
    sys.argv.extend([""] + command.split())
    # GARDER TOUS LES COMMENTAIRES ET LIGNES ORIGINALES
    # --min-priority 0 et --max-priority 500 : inclut TOUTES les strings _() et __()
    # Pas de --no-todo : garde les commentaires TODO
    # Pas de --strings-only : extrait dialogues ET strings
'''
        
        try:
            # Écrire le fichier
            with open(command_filepath, 'w', encoding='utf-8') as f:
                f.write(command_content)
            
            log_message("INFO", f"Fichier de commande créé avec paramètres complets : {command_filename}", category="renpy_generator_tl")
            return command_filepath
            
        except Exception as e:
            log_message("ERREUR", f"Erreur création fichier de commande : {e}", category="renpy_generator_tl")
            raise
    
    def _build_execution_command(self, executable_path: str) -> List[str]:
        """
        Construit la commande d'exécution selon le type d'exécutable
        
        Args:
            executable_path: Chemin vers l'exécutable
            
        Returns:
            Liste des arguments de commande
        """
        if sys.platform == "win32":
            cmd = [executable_path]
        elif executable_path.endswith('.sh'):
            cmd = ['/bin/bash', executable_path]
        elif executable_path.endswith('.py'):
            python_exe = sys.executable
            cmd = [python_exe, executable_path]
        elif executable_path.endswith('.app'):
            cmd = ['open', executable_path, '--wait-apps']
        else:
            cmd = [executable_path]
        
        return cmd

    def _language_already_exists(self, screen_lines: list, language: str) -> bool:
        """
        Vérifie si la langue existe déjà dans le screen preferences parsé.
        
        Args:
            screen_lines: Lignes du screen preferences
            language: Langue à rechercher
            
        Returns:
            bool: True si la langue existe déjà
        """
        try:
            # Pattern pour chercher Language("french") ou Language('french')
            language_pattern = rf'Language\s*\(\s*["\']?\s*{re.escape(language)}\s*["\']?\s*\)'
            
            screen_content = '\n'.join(screen_lines)
            return bool(re.search(language_pattern, screen_content, re.IGNORECASE))
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur vérification langue existante : {e}", category="renpy_generator_tl")
            return False

    def _parse_preferences_screen(self, screens_content: str) -> dict:
        """
        Parse intelligemment le screen preferences du fichier screens.rpy.
        Extrait tout le contenu jusqu'à la fin du screen (indentation zéro).
        
        Args:
            screens_content: Contenu complet du fichier screens.rpy
            
        Returns:
            dict: {'found': bool, 'content': list, 'start_line': int} ou None
        """
        try:
            lines = screens_content.split('\n')
            screen_start = None
            screen_lines = []
            
            # Chercher le début du screen preferences (DOIT être au niveau 0, tab 0)
            for i, line in enumerate(lines):
                # Vérifier que la ligne commence directement par "screen" (pas d'indentation)
                if re.match(r'^screen\s+preferences\s*\(\s*\):', line):
                    screen_start = i
                    screen_lines.append(line)
                    break
            
            if screen_start is None:
                return None
            
            # Extraire tout le contenu du screen jusqu'à indentation zéro
            for i in range(screen_start + 1, len(lines)):
                line = lines[i]
                
                # Fin du screen si ligne avec indentation zéro (sauf ligne vide)
                if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                    break
                
                screen_lines.append(line)
            
            return {
                'found': True,
                'content': screen_lines,
                'start_line': screen_start
            }
            
        except Exception as e:
            log_message("ERREUR", f"Erreur parsing screen preferences : {e}", category="renpy_generator_tl")
            return None

    def create_french_screen_file_pre_generation(self, project_path: str, language: str):
        """
        Crée le fichier screens.rpy français AVANT la génération des traductions
        Utilise le module screens.py pour récupérer le contenu complet
        SANS backup - écrasement direct
        
        Args:
            project_path: Chemin vers le projet
            language: Langue cible
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Ne s'applique que pour le français
            if language.lower() != "french":
                return True, "Fichier screens non applicable pour cette langue"
            
            game_dir = os.path.join(project_path, "game")
            tl_lang_dir = Path(game_dir) / "tl" / language
            
            # Créer les dossiers nécessaires
            tl_lang_dir.mkdir(parents=True, exist_ok=True)
            
            # Chemin de destination - CORRIGER LE NOM : screens.rpy (avec S)
            screens_file = tl_lang_dir / "screens.rpy"  # ✅ CORRIGÉ
            
            # Récupérer le nouveau contenu depuis le module screens
            try:
                from core.services.common.screens import get_french_screen_content  # ✅ CORRIGÉ
                new_screens_content = get_french_screen_content()
            except Exception as e:
                log_message("ERREUR", f"Erreur import contenu screens français : {e}", category="renpy_generator_tl")
                return False, f"Impossible de charger le contenu des screens : {e}"
            
            # Écrire le fichier directement (pas de backup)
            screens_file.write_text(new_screens_content, encoding="utf-8", newline="\n")
            
            log_message("INFO", f"Fichier screens français créé/écrasé depuis module : {screens_file.name}", category="renpy_generator_tl")
            return True, f"Fichier screens.rpy généré avec interface française"
            
        except Exception as e:
            log_message("ERREUR", f"Erreur création fichier screens français depuis module : {e}", category="renpy_generator_tl")
            return False, f"Erreur lors de la création : {e}"

    def _write_parsed_screen_to_file(self, file_path: Path, parsed_screen: dict, language: str):
        """
        Écrit le screen 'preferences' modifié (avec vbox Language injectée) puis,
        si la langue cible est le français, ajoute le bloc de traduction du label "Language".
        """
        try:
            # Entête du fichier
            content = (
                "# Auto-generated language selector\n"
                "# Screen preferences parsé intelligemment avec injection de langue\n"
                f"# Langue ajoutée : {language}\n\n"
            )

            # 1) Contenu du screen modifié
            screen_lines = parsed_screen.get("content", [])
            if isinstance(screen_lines, list):
                content += "\n".join(screen_lines)
            else:
                # Sécurité : si déjà string
                content += str(screen_lines)

            # 2) Bloc translate pour le libellé "Language" si langue = french
            lang_norm = str(language).strip().lower()
            translated_label = self.get_language_word_translation(lang_norm)
            if translated_label:
                content += (
                    f'\n\ntranslate {lang_norm} strings:\n'
                    '\n'
                    '    old "Language"\n'
                    f'    new "{translated_label}"\n'
                )
            # Écriture disque
            file_path.write_text(content, encoding="utf-8", newline="\n")
            log_message("INFO", f"Screen preferences modifié sauvegardé : {file_path.name}", category="renpy_generator_tl")

        except Exception as e:
            log_message("ERREUR", f"Erreur écriture fichier sélecteur langue : {e}", category="renpy_generator_tl")
            raise

    def create_developer_console_file(self, project_path: str, language: str):
        """
        Crée/écrase tl/<lang>/99_Z_Console.rpy pour activer la console développeur Ren'Py.
        SANS popup individuel - seulement logs.

        Args:
            project_path: Chemin du projet Ren'Py
            language: Code langue (ex: "french")

        Returns:
            (success: bool, message: str)
        """
        try:
            game_dir = os.path.join(project_path, "game")
            if not os.path.isdir(game_dir):
                return False, "Dossier 'game' introuvable dans le projet"

            tl_lang_dir = Path(game_dir) / "tl" / language
            tl_lang_dir.mkdir(parents=True, exist_ok=True)

            target_file = tl_lang_dir / "99_Z_Console.rpy"

            content = (
                "## Active la console développeur\n"
                "init +1:\n"
                "    python hide:\n"
                "        ## Active le mode développeur\n"
                "        config.developer = True\n"
                "        config.console = True\n"
            )

            # ÉCRASER SYSTÉMATIQUEMENT (pas de recherche/compare)
            target_file.write_text(content, encoding="utf-8", newline="\n")

            # LOG SEULEMENT - PAS DE CALLBACK NOTIFICATION
            log_message("INFO", f"Console dev: {target_file.name} écrit (écrasement)", category="renpy_generator_tl")
            return True, f"Console développeur activée"
            
        except Exception as e:
            log_message("ERREUR", f"Erreur création console dev : {e}", category="renpy_generator_tl")
            return False, f"Erreur création console dev : {e}"

    def get_language_word_translation(self, language_code: str) -> str | None:
        """
        Retourne la traduction du mot 'Language' dans la langue cible.
        Sert au bloc `translate <lang> strings:` pour le label _("Language").
        """
        m = {
            'french': 'Langue',
            'spanish': 'Idioma',
            'german': 'Sprache',
            'italian': 'Lingua',
            'portuguese': 'Idioma',
            'polish': 'Język',
            'czech': 'Jazyk',
            'hungarian': 'Nyelv',
            'turkish': 'Dil',
            'russian': 'Язык',
            'arabic': 'اللغة',
            'japanese': '言語',
            'korean': '언어',
            'chinese': '语言',
            'dutch': 'Taal',
            'swedish': 'Språk',
            'norwegian': 'Språk',
            'danish': 'Sprog',
            'finnish': 'Kieli',
            'greek': 'Γλώσσα',
            'hebrew': 'שפה',
            'thai': 'ภาษา',
            'vietnamese': 'Ngôn ngữ',
            'indonesian': 'Bahasa',
            'malay': 'Bahasa',
            # 'english': None  # pas de traduction nécessaire
        }
        return m.get(language_code.lower())

    def get_language_display_name(self, language_code: str) -> str:
        """
        Retourne le nom d'affichage pour un code de langue.
        
        Args:
            language_code: Code de langue (ex: "french", "spanish") 
            
        Returns:
            str: Nom d'affichage de la langue
        """
        language_names = {
            'french': 'Français',
            'english': 'English',
            'spanish': 'Español', 
            'german': 'Deutsch',
            'italian': 'Italiano',
            'portuguese': 'Português',
            'russian': 'Русский',
            'chinese': '中文',
            'japanese': '日本語',
            'korean': '한국어',
            'arabic': 'العربية',
            'dutch': 'Nederlands',
            'swedish': 'Svenska',
            'norwegian': 'Norsk',
            'danish': 'Dansk',
            'finnish': 'Suomi',
            'polish': 'Polski',
            'czech': 'Čeština',
            'hungarian': 'Magyar',
            'turkish': 'Türkçe',
            'greek': 'Ελληνικά',
            'hebrew': 'עברית',
            'thai': 'ไทย',
            'vietnamese': 'Tiếng Việt',
            'indonesian': 'Bahasa Indonesia',
            'malay': 'Bahasa Melayu'
        }
        
        return language_names.get(language_code.lower(), language_code.capitalize())

    def get_project_info(self, project_path: str) -> Dict[str, Any]:
        """Récupère les informations détaillées sur un projet Ren'Py."""
        info = {
            'project_path': project_path,
            'project_name': os.path.basename(project_path),
            'executable_found': False,
            'executable_path': None,
            'game_folder_exists': False,
            'renpy_version': 'Unknown',
            'rpa_files': [],
            'rpyc_files': [],
            'rpy_files': [],
            'translation_folders': [],
            'estimated_size': 0,
            'last_modified': None,
            'errors': []
        }
        
        try:
            if not os.path.exists(project_path):
                info['errors'].append("Le chemin du projet n'existe pas")
                return info
            
            # Vérifier l'exécutable principal
            executable_path = self.detect_game_executable(project_path)
            if executable_path:
                info['executable_found'] = True
                info['executable_path'] = executable_path
            
            # Vérifier le dossier game
            game_dir = os.path.join(project_path, "game")
            info['game_folder_exists'] = os.path.isdir(game_dir)
            
            # Scanner les fichiers
            search_dirs = [project_path]
            if info['game_folder_exists']:
                search_dirs.append(game_dir)
            
            for search_dir in search_dirs:
                for root, dirs, files in os.walk(search_dir):
                    if self.operation_cancelled:
                        raise InterruptedError("Opération annulée.")
                    for file in files:
                        if self.operation_cancelled:
                            raise InterruptedError("Opération annulée.")
                        file_path = os.path.join(root, file)
                        file_lower = file.lower()
                        
                        if file_lower.endswith('.rpa'):
                            info['rpa_files'].append(file_path)
                        elif file_lower.endswith('.rpyc'):
                            info['rpyc_files'].append(file_path)
                        elif file_lower.endswith('.rpy'):
                            info['rpy_files'].append(file_path)
            
            # Scanner les dossiers de traduction
            tl_dir = os.path.join(game_dir, "tl") if info['game_folder_exists'] else None
            if tl_dir and os.path.isdir(tl_dir):
                for item in os.listdir(tl_dir):
                    item_path = os.path.join(tl_dir, item)
                    if os.path.isdir(item_path):
                        info['translation_folders'].append(item)
            
            # Calculer la taille estimée (en MB)
            try:
                total_size = 0
                for file_list in [info['rpa_files'], info['rpyc_files'], info['rpy_files']]:
                    for file_path in file_list:
                        if os.path.exists(file_path):
                            total_size += os.path.getsize(file_path)
                info['estimated_size'] = round(total_size / (1024 * 1024), 2)  # MB
            except Exception as e:
                info['errors'].append(f"Erreur calcul taille: {e}")
            
            # Date de dernière modification
            try:
                if info['executable_path'] and os.path.exists(info['executable_path']):
                    timestamp = os.path.getmtime(info['executable_path'])
                    info['last_modified'] = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
            except Exception as e:
                info['errors'].append(f"Erreur date modification: {e}")
            
            log_message("DEBUG", f"Infos projet collectées: {len(info['rpa_files'])} RPA, {len(info['rpyc_files'])} RPYC, {len(info['rpy_files'])} RPY", category="renpy_generator_tl")
            
        except Exception as e:
            info['errors'].append(f"Erreur générale: {e}")
            log_message("ERREUR", f"Erreur get_project_info: {e}", category="renpy_generator_tl")
        
        return info
    
    def generate_advanced_screen_preferences(self, project_path: str, language: str, 
                                            options: Dict[str, bool]) -> Tuple[bool, str]:
        """
        Génère UN SEUL fichier 99_Z_ScreenPreferences.rpy avec les options sélectionnées
        
        Options possibles:
        - language_selector: Sélecteur de langue
        - fontsize_control: Contrôle de taille
        - textbox_opacity: Opacité de la textbox
        - textbox_offset: Décalage vertical
        - textbox_outline: Contour du texte
        
        Args:
            project_path: Chemin vers le projet
            language: Langue cible
            options: Dict des options activées
            
        Returns:
            (success: bool, message: str)
        """
        try:
            # Définir le projet courant pour que les sous-fonctions l'utilisent
            self.current_project_path = project_path
            
            # Vérifier qu'au moins une option est activée
            if not any(options.values()):
                return True, "Aucune option screen preferences sélectionnée"
            
            game_dir = os.path.join(project_path, "game")
            tl_lang_dir = Path(game_dir) / "tl" / language
            tl_lang_dir.mkdir(parents=True, exist_ok=True)
            
            # Fichier de destination
            target_file = tl_lang_dir / "99_Z_ScreenPreferences.rpy"
            
            # Déterminer les sections nécessaires
            need_textbox = options.get('textbox_opacity', False) or \
                          options.get('textbox_offset', False) or \
                          options.get('textbox_outline', False)
            
            need_language = options.get('language_selector', False)
            need_fontsize = options.get('fontsize_control', False)
            
            # Le screen say doit être modifié si on a fontsize OU textbox
            need_say_modification = need_fontsize or need_textbox
            
            # Validation du screen say si modification demandée
            use_textbox_system = False
            if need_say_modification:
                is_valid, validation_msg = self._validate_say_screen_structure(project_path)
                if is_valid:
                    use_textbox_system = True
                    log_message("INFO", "Screen say standard - système de customisation activé", category="renpy_generator_tl")
                else:
                    log_message("ATTENTION", f"Screen say non standard ({validation_msg}) - modification screen say impossible", category="renpy_generator_tl")
                    # Si le screen say n'est pas modifiable, désactiver toutes les options qui en dépendent
                    need_fontsize = False
                    need_textbox = False
            
            # Télécharger l'image si nécessaire (seulement pour les options textbox, pas fontsize seul)
            image_path_relative = None
            if use_textbox_system and need_textbox:
                from core.services.translation.image_manager import ImageManager
                tools_dir = config_manager.get('tools_directory', os.path.expanduser("~/.renextract_tools"))
                image_manager = ImageManager(tools_dir)
                
                success, result = image_manager.copy_image_to_project(
                    'textboxHigh.png', 
                    project_path, 
                    language,
                    subfolder='images'
                )
                
                if success:
                    image_path_relative = result
                    log_message("INFO", f"Image textbox copiée: {image_path_relative}", category="renpy_generator_tl")
                else:
                    log_message("ATTENTION", f"Impossible de copier l'image textbox: {result}", category="renpy_generator_tl")
                    # Si l'image échoue, désactiver seulement les options textbox, pas fontsize
                    need_textbox = False
            
            # Générer le contenu
            content = self._generate_screen_preferences_content(
                language,
                need_language,
                need_fontsize,
                need_textbox,
                options,
                image_path_relative
            )
            
            # Écrire le fichier
            target_file.write_text(content, encoding="utf-8", newline="\n")
            
            # Construire le message de résultat
            features = []
            if need_language:
                features.append("sélecteur langue")
            if need_fontsize:
                features.append("contrôle taille")
            if options.get('textbox_opacity', False):
                features.append("opacité textbox")
            if options.get('textbox_offset', False):
                features.append("décalage vertical")
            if options.get('textbox_outline', False):
                features.append("contour texte")
            
            message = f"Options screen preferences créées: {', '.join(features)}"
            log_message("INFO", message, category="renpy_generator_tl")
            
            return True, message
            
        except FileNotFoundError as e:
            log_message("ERREUR", f"Fichier screens.rpy manquant: {e}", category="renpy_generator_tl")
            return False, str(e)
        except ValueError as e:
            log_message("ERREUR", f"Validation screen preferences échouée: {e}", category="renpy_generator_tl")
            return False, str(e)
        except Exception as e:
            log_message("ERREUR", f"Erreur génération screen preferences avancées: {e}", category="renpy_generator_tl")
            return False, f"Erreur: {e}"
    
    def _generate_screen_preferences_content(self, language: str, need_language: bool, 
                                            need_fontsize: bool, need_textbox: bool,
                                            options: Dict[str, bool], 
                                            image_path: Optional[str]) -> str:
        """
        Génère le contenu complet du fichier screen preferences modulaire
        """
        # En-tête
        content = "# Auto-generated Advanced Screen Preferences\n"
        content += "# Options screen preferences avec customisation avancée\n"
        content += f"# Langue cible: {language}\n\n"
        
        # Section 1: Définitions des variables selon options
        if need_fontsize or need_textbox:
            content += self._generate_textbox_variables(options, need_fontsize, need_textbox)
            content += "\n"
        
        # Section 2: Screen say modifié si fontsize OU textbox
        if need_fontsize or need_textbox:
            content += self._generate_textbox_screen_say(image_path, options, need_fontsize, need_textbox)
            content += "\n"
        
        # Section 3: Screen preferences modifié
        content += self._generate_preferences_screen(language, need_language, need_fontsize, need_textbox, options)
        content += "\n"
        
        # Section 4: Traductions
        lang_norm = language.strip().lower()
        if lang_norm == "french":
            content += self._generate_french_translations(need_language, need_fontsize, need_textbox, options)
        
        return content
    
    def _generate_textbox_variables(self, options: Dict[str, bool], need_fontsize: bool, need_textbox: bool) -> str:
        """
        Génère les variables nécessaires selon les options cochées
        
        Args:
            options: Options activées
            need_fontsize: Si True, génère les variables de taille
            need_textbox: Si True, génère les variables textbox
        """
        content = "## Variables pour la customisation\n\n"
        
        # Valeurs par défaut
        defaults = []
        persistents = []
        
        # Variables fontsize
        if need_fontsize:
            defaults.append("define pref_text_sizedefault = 34")
            persistents.append("default persistent.pref_text_size = pref_text_sizedefault")
            persistents.append("default persistent.pref_text_size2 = 44")
        
        # Variables textbox opacity
        if options.get('textbox_opacity', False):
            defaults.append("define RenExtractTextboxOpacitydefault = 1.0")
            persistents.append("default persistent.RenExtractTextboxOpacity = RenExtractTextboxOpacitydefault")
        
        # Variables textbox offset
        if options.get('textbox_offset', False):
            defaults.append("define RenExtractyposOffsetdefault = 0")
            persistents.append("default persistent.RenExtractyposOffset = RenExtractyposOffsetdefault")
        
        # Variables textbox outline
        if options.get('textbox_outline', False):
            defaults.extend([
                "define RenExtractTextOutline1default = 3",
                "define RenExtractTextOutline2default = 0",
                "define RenExtractTextOutline3default = 0"
            ])
            persistents.extend([
                "default persistent.RenExtractTextOutline1 = RenExtractTextOutline1default",
                "default persistent.RenExtractTextOutline2 = RenExtractTextOutline2default",
                "default persistent.RenExtractTextOutline3 = RenExtractTextOutline3default"
            ])
        
        # Générer le contenu
        if defaults:
            content += "# Valeurs par défaut\n"
            content += "\n".join(defaults) + "\n\n"
        
        if persistents:
            content += "# Variables persistantes\n"
            content += "\n".join(persistents) + "\n\n"
        
        return content
    
    def _generate_textbox_screen_say(self, image_path: Optional[str], options: Dict[str, bool], 
                                     need_fontsize: bool, need_textbox: bool) -> str:
        """
        Génère le screen say modifié pour fontsize et/ou textbox
        
        Args:
            image_path: Chemin vers l'image textbox (peut être None si juste fontsize)
            options: Options activées
            need_fontsize: Si True, applique pref_text_size
            need_textbox: Si True, applique les options textbox complètes
        """
        content = "## Screen say modifié pour la customisation\n\n"
        content += "screen say(who, what):\n"
        content += "    style_prefix \"say\"\n\n"
        content += "    window:\n"
        content += "        id \"window\"\n"
        
        # Background avec image si textbox, sinon garder le style par défaut
        if need_textbox and image_path:
            content += f"        background Transform(Image(\"{image_path}\",xalign=0.5), alpha=persistent.RenExtractTextboxOpacity)\n"
        
        # Calcul de la taille si fontsize activé
        if need_fontsize:
            content += "        $ persistent.pref_text_size2 = persistent.pref_text_size + 10\n"
        
        # Calculs de position si offset activé
        if options.get('textbox_offset', False):
            if need_fontsize:
                # Calculs dynamiques avec pref_text_size
                content += "        if persistent.pref_text_size > 20:\n"
                content += "            $ RenExtractypos1 = 195 - (6 * persistent.pref_text_size + persistent.RenExtractyposOffset)\n"
                content += "            $ RenExtractypos2 = 210 - (6 * persistent.pref_text_size + persistent.RenExtractyposOffset)\n"
                content += "            $ RenExtractypos3 = 240 - (5 * persistent.pref_text_size + persistent.RenExtractyposOffset)\n"
                content += "        else:\n"
                content += "            $ RenExtractypos1 = 195 - (6 * 20 + persistent.RenExtractyposOffset)\n"
                content += "            $ RenExtractypos2 = 210 - (6 * 20 + persistent.RenExtractyposOffset)\n"
                content += "            $ RenExtractypos3 = 240 - (5 * 20 + persistent.RenExtractyposOffset)\n"
            else:
                # Calculs fixes sans pref_text_size
                content += "        $ RenExtractypos1 = 195 - (6 * 20 + persistent.RenExtractyposOffset)\n"
                content += "        $ RenExtractypos2 = 210 - (6 * 20 + persistent.RenExtractyposOffset)\n"
                content += "        $ RenExtractypos3 = 240 - (5 * 20 + persistent.RenExtractyposOffset)\n"
        
        # Namebox (who)
        content += "        if who is not None:\n"
        content += "            window:\n"
        content += "                id \"namebox\"\n"
        content += "                style \"namebox\"\n"
        
        if options.get('textbox_offset', False):
            content += "                ypos RenExtractypos2\n"
        
        # Texte du nom avec taille et outline si configurés
        who_attrs = []
        if need_fontsize:
            who_attrs.append("size persistent.pref_text_size2")
        if options.get('textbox_outline', False):
            who_attrs.append("outlines [ (absolute(persistent.RenExtractTextOutline1), \"#000\", absolute(persistent.RenExtractTextOutline2), absolute(persistent.RenExtractTextOutline3)) ]")
        
        who_line = "                text who id \"who\""
        if who_attrs:
            who_line += " " + " ".join(who_attrs)
        content += who_line + "\n"
        
        # Texte du dialogue avec taille et outline si configurés
        what_attrs = []
        if options.get('textbox_offset', False):
            what_attrs.append("ypos RenExtractypos3")
        if need_fontsize:
            what_attrs.append("size persistent.pref_text_size")
        if options.get('textbox_outline', False):
            what_attrs.append("outlines [ (absolute(persistent.RenExtractTextOutline1), \"#000\", absolute(persistent.RenExtractTextOutline2), absolute(persistent.RenExtractTextOutline3)) ]")
        
        what_line = "        text what id \"what\""
        if what_attrs:
            what_line += " " + " ".join(what_attrs)
        content += what_line + "\n\n"
        
        content += "    if not renpy.variant(\"small\"):\n"
        content += "        add SideImage() xalign 0.0 yalign 1.0\n\n"
        
        return content
    
    def _detect_translation_style(self, screens_content: str) -> tuple:
        """
        Détecte le style de traduction utilisé dans screens.rpy
        
        Args:
            screens_content: Contenu du fichier screens.rpy
            
        Returns:
            (use_underscore: bool, tag_type: str) où tag_type est 'label', 'text' ou 'textbutton'
        """
        import re
        
        # Chercher dans les vbox de sliders pour identifier le tag utilisé
        # Pattern pour trouver les labels dans les sliders
        patterns_to_check = [
            (r'label\s+_\(["\']', 'label', True),      # label _("...")
            (r'label\s+["\']', 'label', False),        # label "..."
            (r'text\s+_\(["\']', 'text', True),        # text _("...")
            (r'text\s+["\'](?![\[])', 'text', False),  # text "..." (mais pas text "[...")
        ]
        
        # Compter les occurrences de chaque pattern
        results = {}
        for pattern, tag, has_underscore in patterns_to_check:
            count = len(re.findall(pattern, screens_content))
            if count > 0:
                key = (tag, has_underscore)
                results[key] = results.get(key, 0) + count
        
        # Trouver le pattern le plus utilisé
        if results:
            most_common = max(results.items(), key=lambda x: x[1])
            tag_type, use_underscore = most_common[0]
            return use_underscore, tag_type
        
        # Par défaut : label avec _()
        return True, 'label'
    
    def _generate_preferences_screen(self, language: str, need_language: bool, 
                                    need_fontsize: bool, need_textbox: bool,
                                    options: Dict[str, bool]) -> str:
        """Génère le screen preferences avec les vbox nécessaires"""
        
        # Lire le screen preferences existant depuis game/ (JAMAIS depuis tl/)
        game_dir = os.path.join(self.current_project_path or "", "game")
        
        # Chercher screens.rpy dans game/ et ses sous-dossiers (SAUF tl/)
        screens_file = self._find_screens_file(game_dir)
        
        if not screens_file:
            raise FileNotFoundError(
                f"Le fichier screens.rpy est introuvable dans le dossier game/ (hors traductions).\n"
                f"Recherché dans : {game_dir} et tous ses sous-dossiers (sauf tl/)\n"
                f"Assurez-vous que le projet Ren'Py est décompilé."
            )
        
        log_message("INFO", f"Utilisation de screens.rpy depuis : {os.path.relpath(screens_file, self.current_project_path)}", category="renpy_generator_tl")
        
        # Lire et parser le screen preferences
        try:
            with open(screens_file, 'r', encoding='utf-8', errors='ignore') as f:
                screens_content = f.read()
            parsed_screen = self._parse_preferences_screen(screens_content)
            
            # Détecter le style de traduction utilisé (tag et _())
            use_translation_markers, label_tag = self._detect_translation_style(screens_content)
            log_message("DEBUG", f"Style détecté: tag='{label_tag}', underscore={use_translation_markers}", category="renpy_generator_tl")
        except Exception as e:
            raise ValueError(f"Erreur lors de la lecture de screens.rpy: {e}")
        
        # VALIDATION STRICTE : Le screen preferences DOIT exister
        if not parsed_screen:
            raise ValueError(
                "Structure 'screen preferences():' introuvable dans screens.rpy. "
                "Le fichier doit contenir un screen preferences() au niveau 0 (tab 0) pour pouvoir être modifié."
            )
        
        # Utiliser le screen parsé
        content = "\n".join(parsed_screen['content'])
        
        # Helper pour wrapper les strings (juste le quote, pas le tag)
        def quote_text(text):
            return f'_("{text}")' if use_translation_markers else f'"{text}"'
        
        # Trouver le point d'injection
        injection_lines = []
        
        # Ajouter vbox langue si demandé
        if need_language:
            display_name = self.get_language_display_name(language)
            lang_label = f"{label_tag} {quote_text('Language')}"
            eng_btn = quote_text("English")
            display_btn = quote_text(display_name)
            injection_lines.extend([
                "",
                "                vbox:",
                "                    style_prefix \"radio\"",
                f"                    {lang_label}",
                f"                    textbutton {eng_btn} action Language(None)",
                f"                    textbutton {display_btn} action Language(\"{language}\")",
                ""
            ])
        
        # Ajouter vbox taille si demandé (version avancée cohérente)
        if need_fontsize and not need_textbox:
            size_label = f"{label_tag} {quote_text('Dialogue text size  ([persistent.pref_text_size]/75)')}"
            reset_text = quote_text('reset')
            injection_lines.extend([
                "",
                "                vbox:",
                "                    style_prefix \"slider\"",
                "                    spacing -2",
                "                    hbox:",
                "                        xpos 5",
                f"                        {size_label}",
                "                    hbox:",
                "                        xpos 15",
                "                        ypos 5",
                "                        bar:",
                "                            value FieldValue(object=persistent, field='pref_text_size', range=75, max_is_zero=False, style=u'slider', offset=0, step=1)",
                "",
                "                    null height (1 * gui.pref_spacing)",
                "                    if persistent.pref_text_size != pref_text_sizedefault:",
                "                        hbox:",
                "                            xpos -5",
                f"                            textbutton {reset_text}:",
                "                                selected False",
                "                                action SetVariable(\"persistent.pref_text_size\", pref_text_sizedefault)",
                ""
            ])
        
        # Ajouter vbox textbox si demandé
        if need_textbox:
            injection_lines.extend(self._generate_textbox_vbox(options, use_translation_markers, label_tag))
        
        # Injecter dans le screen
        if injection_lines:
            # Trouver où injecter (après Transitions/After Choices pour ne pas déplacer ces éléments)
            lines = content.split('\n')
            injection_point = None
            
            # Chercher d'abord après "Transitions" (qui doit rester sous "After Choices")
            for i, line in enumerate(lines):
                if 'Preference("transitions"' in line or 'Preference("after choices"' in line:
                    # Trouver la fin de cette vbox (ligne vide suivante ou prochaine vbox)
                    for j in range(i + 1, len(lines)):
                        if lines[j].strip() == '' or (lines[j].strip().startswith('vbox:') and 'style_prefix' in lines[j+1] if j+1 < len(lines) else False):
                            injection_point = j
                            break
                    if injection_point:
                        break
            
            # Fallback: chercher après Skip
            if not injection_point:
                for i, line in enumerate(lines):
                    if '"Skip"' in line or '"Passer"' in line:
                        injection_point = i + 3
                        break
            
            if injection_point:
                lines[injection_point:injection_point] = injection_lines
            else:
                # Fallback: ajouter à la fin
                lines.extend(injection_lines)
            
            content = '\n'.join(lines)
        
        return content
    
    def _generate_textbox_vbox(self, options: Dict[str, bool], use_translation_markers: bool = True, label_tag: str = 'text') -> List[str]:
        """
        Génère les vbox pour les contrôles textbox en layout 2x2
        
        Args:
            options: Options activées
            use_translation_markers: Si True, utilise _() pour les strings
            label_tag: Tag à utiliser pour les labels ('label', 'text', etc.)
        """
        lines = []
        
        # Helper pour wrapper les strings (juste le quote, pas le tag)
        def quote_text(text):
            return f'_("{text}")' if use_translation_markers else f'"{text}"'
        
        # Calculer le pourcentage pour l'opacité si nécessaire
        if options.get('textbox_opacity', False):
            lines.append("")
            lines.append("            # Calcul du pourcentage pour l'affichage")
            lines.append("            $ RenExtractTextboxOpacityPercent = int(persistent.RenExtractTextboxOpacity * 100)")
            lines.append("")
        
        # Espacement initial unique
        lines.append("            null height (4 * gui.pref_spacing)")
        
        # PREMIÈRE LIGNE : Taille du dialogue + Opacité (si au moins une activée)
        has_fontsize = options.get('fontsize_control', False)
        has_opacity = options.get('textbox_opacity', False)
        has_first_line = has_fontsize or has_opacity
        
        if has_first_line:
            lines.append("            hbox:")
            lines.append("                spacing 20")
            
            # Taille du dialogue (colonne 1) - seulement si cochée
            if has_fontsize:
                lines.extend([
                    "                vbox:",
                    "                    style_prefix \"slider\"",
                    "                    spacing -2",
                    "                    hbox:",
                    "                        xpos 5",
                    f"                        {label_tag} {quote_text('Dialogue text size  ([persistent.pref_text_size]/75)')}",
                    "                    hbox:",
                    "                        xpos 15",
                    "                        ypos 5",
                    "                        bar:",
                    "                            value FieldValue(object=persistent, field='pref_text_size', range=75, max_is_zero=False, style=u'slider', offset=0, step=1)"
                ])
            
            # Opacité (colonne 2) - seulement si cochée
            if has_opacity:
                lines.extend([
                    "                vbox:",
                    "                    style_prefix \"slider\"",
                    "                    spacing -2",
                    "                    hbox:",
                    "                        xpos 5",
                    f"                        {label_tag} {quote_text('Dialogue box opacity ([RenExtractTextboxOpacityPercent]%)')}",
                    "                    hbox:",
                    "                        xpos 15",
                    "                        ypos 5",
                    "                        bar:",
                    "                            value FieldValue(persistent, \"RenExtractTextboxOpacity\", range=1.0, style=\"slider\")"
                ])
            
            lines.append("")
        
        # DEUXIÈME LIGNE : Décalage vertical + Contour (si au moins une activée)
        has_second_line = options.get('textbox_offset', False) or options.get('textbox_outline', False)
        
        if has_second_line:
            # Espacement entre les lignes uniquement s'il y a une première ligne
            if has_first_line:
                lines.append("            null height (2 * gui.pref_spacing)")
            lines.append("            hbox:")
            lines.append("                spacing 20")
            
            # Décalage vertical si demandé (colonne 1)
            if options.get('textbox_offset', False):
                lines.extend([
                    "                vbox:",
                    "                    style_prefix \"slider\"",
                    "                    spacing -2",
                    "                    hbox:",
                    "                        xpos 5",
                    f"                        {label_tag} {quote_text('Dialogue vert. offset ([persistent.RenExtractyposOffset])')}",
                    "                    hbox:",
                    "                        xpos 15",
                    "                        ypos 5",
                    "                        bar:",
                    "                            value FieldValue(object=persistent, field='RenExtractyposOffset', range=400, max_is_zero=False, style=u'slider', offset=-200, step=1)"
                ])
            
            # Contour si demandé (colonne 2)
            if options.get('textbox_outline', False):
                lines.extend([
                    "                vbox:",
                    "                    style_prefix \"slider\"",
                    "                    spacing -2",
                    "                    hbox:",
                    "                        xpos 5",
                    f"                        {label_tag} {quote_text('Text outline ([persistent.RenExtractTextOutline1]/10)')}",
                    "                    hbox:",
                    "                        xpos 15",
                    "                        ypos 5",
                    "                        bar:",
                    "                            value FieldValue(persistent, \"RenExtractTextOutline1\", range=10, style=\"slider\")"
                ])
            
            lines.append("")
        
        # Bouton de reset (seulement pour les options cochées)
        reset_conditions = []
        reset_actions = []
        
        if has_fontsize:
            reset_conditions.append("persistent.pref_text_size != pref_text_sizedefault")
            reset_actions.append("SetVariable(\"persistent.pref_text_size\", pref_text_sizedefault)")
        
        if has_opacity:
            reset_conditions.append("persistent.RenExtractTextboxOpacity != RenExtractTextboxOpacitydefault")
            reset_actions.append("SetVariable(\"persistent.RenExtractTextboxOpacity\", RenExtractTextboxOpacitydefault)")
        
        if options.get('textbox_offset', False):
            reset_conditions.append("persistent.RenExtractyposOffset != RenExtractyposOffsetdefault")
            reset_actions.append("SetVariable(\"persistent.RenExtractyposOffset\", RenExtractyposOffsetdefault)")
        
        if options.get('textbox_outline', False):
            reset_conditions.append("persistent.RenExtractTextOutline1 != RenExtractTextOutline1default")
            reset_actions.extend([
                "SetVariable(\"persistent.RenExtractTextOutline1\", RenExtractTextOutline1default)",
                "SetVariable(\"persistent.RenExtractTextOutline2\", RenExtractTextOutline2default)",
                "SetVariable(\"persistent.RenExtractTextOutline3\", RenExtractTextOutline3default)"
            ])
        
        if reset_conditions:
            reset_text = quote_text('reset')
            condition = " or ".join(reset_conditions)
            actions = ",\n                            ".join(reset_actions)
            
            lines.extend([
                "            null height (1 * gui.pref_spacing)",
                f"            if {condition}:",
                "                hbox:",
                "                    xpos -5",
                f"                    textbutton {reset_text}:",
                "                        selected False",
                "                        action [",
                f"                            {actions}]",
                ""
            ])
        
        return lines
    
    def _generate_french_translations(self, need_language: bool, need_fontsize: bool, 
                                     need_textbox: bool, options: Dict[str, bool]) -> str:
        """Génère les traductions françaises"""
        content = "\ntranslate french strings:\n\n"
        
        if need_language:
            content += '    old "Language"\n'
            content += '    new "Langue"\n\n'
        
        if need_fontsize and not need_textbox:
            content += '    old "Text Size"\n'
            content += '    new "Taille du texte"\n\n'
        
        if need_textbox:
            content += '    old "Dialogue text size  ([persistent.pref_text_size]/75)"\n'
            content += '    new "Taille du texte du dialogue ([persistent.pref_text_size]/75)"\n\n'
            
            if options.get('textbox_opacity', False):
                content += '    old "Dialogue box opacity ([RenExtractTextboxOpacityPercent]%)"\n'
                content += '    new "Opacité de la boîte de dialogue ([RenExtractTextboxOpacityPercent]%)"\n\n'
            
            if options.get('textbox_offset', False):
                content += '    old "Dialogue vert. offset ([persistent.RenExtractyposOffset])"\n'
                content += '    new "Décalage vertical du dialogue ([persistent.RenExtractyposOffset])"\n\n'
            
            if options.get('textbox_outline', False):
                content += '    old "Text outline ([persistent.RenExtractTextOutline1]/10)"\n'
                content += '    new "Contour du texte ([persistent.RenExtractTextOutline1]/10)"\n\n'
       
        return content
    
    def cancel_operation(self):
        """Annule l'opération en cours"""
        self.operation_cancelled = True
        log_message("INFO", "Annulation demandée par l'utilisateur.", category="renpy_generator_tl")
    
    def cleanup(self):
        """Nettoie les ressources"""
        try:
            self.sdk_manager.cleanup()
            log_message("DEBUG", "TranslationGenerationBusiness nettoyé", category="renpy_generator_tl")
        except Exception as e:
            log_message("ATTENTION", f"Erreur lors du nettoyage: {e}", category="renpy_generator_tl")

# Export des symboles publics
__all__ = ['TranslationGenerationBusiness']