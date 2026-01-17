import json, os
import re
from .constants import DEFAULT_CONFIG, FILE_NAMES, VERSION, ensure_folders_exist
from infrastructure.logging.logging import log_message, get_logger

class ConfigManager:
    """Gestion de configuration (compacte) avec appli debug immédiate idempotente."""
    def __init__(self):
        ensure_folders_exist()
        self.config_file = FILE_NAMES["config"]
        self.config = DEFAULT_CONFIG.copy()
        self._applying_debug = False  # garde anti-réentrance
        self.load_config()

    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self.config.update(json.load(f))
            else:
                self.save_config()
            # normalisation
            if not self.config.get("debug_mode", False):
                self.config["debug_level"] = 3
        except Exception as e:
            log_message("ATTENTION", f"Impossible de charger la configuration: {e}", category="utils_config")
            self.config = DEFAULT_CONFIG.copy()

    def save_config(self):
        try:
            d = os.path.dirname(self.config_file)
            if d and not os.path.exists(d): os.makedirs(d, exist_ok=True)
            self.config["version"] = VERSION
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            log_message("ATTENTION", f"Impossible de sauvegarder la configuration: {e}", category="utils_config")

    def get_editor_custom_paths(self):
        """Récupère les chemins personnalisés des éditeurs - Version 4 éditeurs"""
        default_paths = {
            'VSCode': '',
            'Sublime Text': '',
            'Notepad++': '',
            'Atom/Pulsar': ''  # ← Unifié
        }
        return self.config.get("editor_custom_paths", default_paths)

    def set_editor_custom_path(self, editor_name, path):
        """Définit le chemin personnalisé pour un éditeur"""
        paths = self.get_editor_custom_paths()
        paths[editor_name] = path
        self.set("editor_custom_paths", paths)

    def get_editor_custom_path(self, editor_name):
        """Récupère le chemin personnalisé d'un éditeur spécifique"""
        paths = self.get_editor_custom_paths()
        
        # Gestion spéciale pour la compatibilité Atom/Pulsar
        if editor_name == 'Atom/Pulsar':
            return paths.get('Atom/Pulsar', '')
        elif editor_name == 'Atom':
            # Compatibilité : si on demande 'Atom', on retourne 'Atom/Pulsar'
            return paths.get('Atom/Pulsar', '')
        elif editor_name == 'Pulsar':
            # Compatibilité : si on demande 'Pulsar', on retourne 'Atom/Pulsar'
            return paths.get('Atom/Pulsar', '')
        else:
            return paths.get(editor_name, '')

    def reset_editor_custom_paths(self):
        """Remet tous les chemins personnalisés à vide - Version 4 éditeurs"""
        self.set("editor_custom_paths", {
            'VSCode': '',
            'Sublime Text': '',
            'Notepad++': '',
            'Atom/Pulsar': ''  # ← Unifié
        })

    # --- getters/setters génériques ---
    def get(self, key, default=None): return self.config.get(key, default)
    def set(self, key, value):
        self.config[key] = value
        self.save_config()
        # Propagation immédiate si on touche au debug
        if key in ("debug_mode", "debug_level"):
            try: self.apply_debug_config_immediately()
            except Exception: pass

    def get_protection_placeholders(self):
        """Récupère la configuration des préfixes de placeholders"""
        default = {
            "code_prefix": "RENPY_CODE_001",
            "asterisk_prefix": "RENPY_ASTERISK_001",
            "tilde_prefix": "RENPY_TILDE_001",
            "empty_prefix": "RENPY_EMPTY"
        }
        return self.get("protection_placeholders", default)

    def set_protection_placeholder(self, placeholder_type, prefix):
        """Définit un préfixe spécifique"""
        if not isinstance(prefix, str) or not prefix.strip():
            log_message("ATTENTION", f"Préfixe invalide pour {placeholder_type}: '{prefix}'", category="utils_config")
            return False
            
        # Validation du préfixe
        allowed_chars = re.match(r'^[a-zA-Z0-9_\-()]+$', prefix)
        if not allowed_chars:
            log_message("ATTENTION", f"Préfixe contient des caractères invalides: '{prefix}'", category="utils_config")
            return False

            
        if len(prefix) > 50:
            log_message("ATTENTION", f"Préfixe trop long (max 50): '{prefix}'", category="utils_config")
            return False
        
        placeholders = self.get_protection_placeholders()
        placeholders[placeholder_type] = prefix.strip()
        self.set("protection_placeholders", placeholders)
        
        return True

    def get_protection_placeholder(self, placeholder_type):
        """Récupère un préfixe spécifique"""
        placeholders = self.get_protection_placeholders()
        default_values = {
            "code_prefix": "RENPY_CODE_001",
            "asterisk_prefix": "RENPY_ASTERISK_001", 
            "tilde_prefix": "RENPY_TILDE_001",
            "empty_prefix": "RENPY_EMPTY"
        }
        return placeholders.get(placeholder_type, default_values.get(placeholder_type, "RENPY_CODE_001"))

    def reset_protection_placeholders(self):
        """Remet tous les préfixes par défaut"""
        default = {
            "code_prefix": "RENPY_CODE_001",
            "asterisk_prefix": "RENPY_ASTERISK_001",
            "tilde_prefix": "RENPY_TILDE_001",
            "empty_prefix": "RENPY_EMPTY"
        }
        self.set("protection_placeholders", default)
        log_message("INFO", "Préfixes de protection remis par défaut", category="utils_config")

    def validate_protection_prefixes(self):
        """Valide que tous les préfixes sont corrects"""
        placeholders = self.get_protection_placeholders()
        errors = []
        
        for prefix_type, prefix_value in placeholders.items():
            if not prefix_value or not isinstance(prefix_value, str):
                errors.append(f"{prefix_type}: Valeur manquante ou invalide")
            elif not re.match(r'^[a-zA-Z0-9_\-()]+$', prefix_value):
                errors.append(f"{prefix_type}: Caractères non autorisés dans '{prefix_value}'")
            elif len(prefix_value) > 50:
                errors.append(f"{prefix_type}: Trop long ('{prefix_value}')")
        
        # Vérifier les doublons
        prefix_values = list(placeholders.values())
        if len(set(prefix_values)) != len(prefix_values):
            errors.append("Doublons détectés entre les préfixes")
        
        if errors:
            log_message("ERREUR", f"Préfixes invalides: {errors}", category="utils_config")
            return False, errors
        else:
            return True, []

    def get_project_progress_tracking(self): 
        return self.config.get("project_progress_tracking", True)

    def set_project_progress_tracking(self, enabled): 
        self.set("project_progress_tracking", enabled)

    def toggle_project_progress_tracking(self): 
        current = self.get_project_progress_tracking()
        new_state = not current
        self.set_project_progress_tracking(new_state)
        return new_state

    # --- last directory ---
    def get_last_directory(self): return self.config.get("last_directory", "")
    def set_last_directory(self, filepath):
        if filepath: self.set("last_directory", os.path.dirname(filepath))

    # --- langue app ---
    def get_language(self): return self.config.get("language", "fr")
    def set_language(self, language_code): self.set("language", language_code)

    # --- intégrations Ren'Py (common/screen) ---
    def set_add_common_integration(self, enabled: bool): self.config["renpy_add_common_integration"] = bool(enabled); self.save_config()
    def is_add_common_integration_enabled(self) -> bool: return self.config.get("renpy_add_common_integration", False)
    def set_add_screen_integration(self, enabled: bool): self.config["renpy_add_screen_integration"] = bool(enabled); self.save_config()
    def is_add_screen_integration_enabled(self) -> bool: return self.config.get("renpy_add_screen_integration", False)

    def get_theme_colors(self):
        from .constants import THEME_COLORS_DEFAULT
        return self.get("theme_colors", THEME_COLORS_DEFAULT)
    def set_theme_color(self, color_key, color_value):
        c = self.get_theme_colors(); c[color_key] = color_value; self.set("theme_colors", c)
    def reset_theme_colors_to_default(self):
        from .constants import THEME_COLORS_DEFAULT
        self.set("theme_colors", THEME_COLORS_DEFAULT.copy())
    def get_theme_color(self, color_key):
        return self.get_theme_colors().get(color_key, "#D3D3D3")
    def apply_color_preset(self, preset_name):
        from .constants import COLOR_PRESETS
        if preset_name in COLOR_PRESETS: self.set("theme_colors", COLOR_PRESETS[preset_name].copy()); return True
        return False
    def get_current_preset_name(self):
        try:
            from .constants import COLOR_PRESETS
            cur = self.get_theme_colors()
            for n, preset in COLOR_PRESETS.items():
                if self._colors_match(cur, preset): return n
            return "Personnalisé"
        except Exception:
            return "Personnalisé"
    def _colors_match(self, c1, c2):
        try:
            for k in ["button_primary_bg","button_secondary_bg","button_tertiary_bg","button_danger_bg","button_feature_bg","button_powerful_bg","button_devtool_bg","button_nav_bg","button_help_bg","button_utility_bg"]:
                if c1.get(k,"").upper()!=c2.get(k,"").upper(): return False
            return True
        except Exception:
            return False
    def get_available_presets(self):
        from .constants import COLOR_PRESETS
        return list(COLOR_PRESETS.keys())

    # --- options diverses ---
    def is_auto_open_enabled(self): return self.config.get("auto_open_files", True)
    def toggle_auto_open(self): v = not self.is_auto_open_enabled(); self.set("auto_open_files", v); return v
    def delete_config_file(self):
        try:
            if os.path.exists(self.config_file): os.remove(self.config_file)
        except Exception as e:
            log_message("ERREUR", f"Erreur suppression config.json: {e}", category="utils_config")
    def is_output_path_display_enabled(self): return self.config.get("show_output_path", False)
    def set_output_path_display(self, enabled): self.set("show_output_path", enabled)
    def toggle_output_path_display(self): v = not self.is_output_path_display_enabled(); self.set_output_path_display(v); return v
    def is_dark_mode_enabled(self): return self.config.get("dark_mode", True)

    # --- Ren'Py: chemins/préférences ---
    def get_renpy_sdk_path(self): return self.config.get("renpy_sdk_path", r"C:\renpy-sdk")
    def set_renpy_sdk_path(self, path): self.set("renpy_sdk_path", path)
    def get_renpy_default_language(self): return self.config.get("renpy_default_language", "french")
    def set_renpy_default_language(self, language): self.set("renpy_default_language", language)
    def is_renpy_auto_open_folder_enabled(self): return self.config.get("renpy_auto_open_folder", True)
    def set_renpy_auto_open_folder(self, enabled): self.set("renpy_auto_open_folder", enabled)

    # --- intégrations UI ---
    def is_language_selector_integration_enabled(self): return self.config.get("language_selector_integration", True)
    def set_language_selector_integration(self, enabled): self.set("language_selector_integration", enabled)
    def toggle_language_selector_integration(self): v = not self.is_language_selector_integration_enabled(); self.set_language_selector_integration(v); return v
    def is_developer_console_integration_enabled(self): return self.config.get("developer_console_integration", False)
    def set_developer_console_integration(self, enabled): self.set("developer_console_integration", bool(enabled))
    def toggle_developer_console_integration(self): v = not self.is_developer_console_integration_enabled(); self.set_developer_console_integration(v); return v

    # --- reset options Génération ---
    def reset_generation_options_to_defaults(self):
        keys = ["renpy_default_language","renpy_auto_open_folder","renpy_show_results_popup","renpy_delete_rpa_after","renpy_delete_source_after_rpa","cleanup_excluded_files","extraction_detection_mode","extraction_excluded_files","language_selector_integration","developer_console_integration","font_preferences"]
        for k in keys:
            if k in DEFAULT_CONFIG: self.config[k] = DEFAULT_CONFIG[k]
        self.save_config()
        return {k: self.config.get(k) for k in keys}

    # --- polices GUI individuelles ---
    def is_fontsize_selector_integration_enabled(self): 
        return self.config.get("fontsize_selector_integration", False)

    def set_fontsize_selector_integration(self, enabled): 
        self.set("fontsize_selector_integration", bool(enabled))

    def toggle_fontsize_selector_integration(self): 
        v = not self.is_fontsize_selector_integration_enabled()
        self.set_fontsize_selector_integration(v)
        return v

    # --- customisation textbox ---
    def get_textbox_customization(self):
        """Récupère les préférences de customisation textbox"""
        default = {
            'opacity': False,
            'offset': False,
            'outline': False
        }
        return self.config.get("textbox_customization", default)
    
    def set_textbox_customization(self, customization_dict):
        """Définit les préférences de customisation textbox"""
        self.set("textbox_customization", customization_dict)
    
    def is_any_textbox_option_enabled(self):
        """Vérifie si au moins une option textbox est activée"""
        prefs = self.get_textbox_customization()
        return any(prefs.values())

    def get_font_preferences(self):
        default = {"is_rtl": False,"apply_system_font": True,"individual_fonts": {
            "text_font":{"enabled": True,"font_name":"","font_path":""},
            "name_text_font":{"enabled": False,"font_name":"","font_path":""},
            "interface_text_font":{"enabled": False,"font_name":"","font_path":""},
            "button_text_font":{"enabled": False,"font_name":"","font_path":""},
            "choice_button_text_font":{"enabled": False,"font_name":"","font_path":""}}}
        return self.config.get("font_preferences", default)
    def set_font_preferences(self, preferences): self.set("font_preferences", preferences)
    def get_individual_font_config(self, font_type):
        prefs = self.get_font_preferences()
        return prefs.get("individual_fonts", {}).get(font_type, {"enabled": False,"font_name":"","font_path":""})
    def set_individual_font_config(self, font_type, config):
        prefs = self.get_font_preferences()
        prefs.setdefault("individual_fonts", {})[font_type] = config
        self.set_font_preferences(prefs)
    def get_font_rtl(self): return self.get_font_preferences().get("is_rtl", False)
    def set_font_rtl(self, is_rtl): p = self.get_font_preferences(); p["is_rtl"] = is_rtl; self.set_font_preferences(p)
    def get_apply_system_font(self): return self.get_font_preferences().get("apply_system_font", True)
    def set_apply_system_font(self, apply): p = self.get_font_preferences(); p["apply_system_font"] = apply; self.set_font_preferences(p)
    def get_enabled_gui_fonts(self):
        fonts = {}
        for t, c in self.get_font_preferences().get("individual_fonts", {}).items():
            if c.get("enabled", False): fonts[t] = c
        return fonts
    def set_gui_font_enabled(self, font_type, enabled): c = self.get_individual_font_config(font_type); c["enabled"] = enabled; self.set_individual_font_config(font_type, c)
    def set_gui_font_selection(self, font_type, font_name, font_path): c = self.get_individual_font_config(font_type); c.update({"font_name": f"{font_name}", "font_path": f"{font_path}"}); self.set_individual_font_config(font_type, c)
    def get_all_gui_font_selections(self):
        out = {}
        for t, c in self.get_font_preferences().get("individual_fonts", {}).items():
            out[t] = {"enabled": c.get("enabled", False), "font_name": c.get("font_name", ""), "font_path": c.get("font_path", "")}
        return out

    # --- mode de sauvegarde ---
    def get_default_save_mode(self): return self.config.get("default_save_mode", "overwrite")
    def set_default_save_mode(self, mode): self.set("default_save_mode", mode if mode in ["overwrite","new_file"] else "overwrite")
    def toggle_default_save_mode(self): m = "new_file" if self.get_default_save_mode()=="overwrite" else "overwrite"; self.set_default_save_mode(m); return m

    # --- rapport de cohérence ---
    def is_coherence_auto_open_report_enabled(self): return self.config.get("coherence_auto_open_report", True)
    def set_coherence_auto_open_report(self, enabled): self.set("coherence_auto_open_report", enabled)
    def toggle_coherence_auto_open_report(self): v = not self.is_coherence_auto_open_report_enabled(); self.set_coherence_auto_open_report(v); return v

    # --- exclusions Ren'Py ---
    def get_renpy_excluded_files_as_string(self):
        default = "common.rpy"
        data = self.config.get("renpy_excluded_files", default)
        return data if isinstance(data, str) else ", ".join(data) if isinstance(data, list) else default
    def get_renpy_excluded_files(self): return [s.strip() for s in self.get_renpy_excluded_files_as_string().split(",") if s.strip()]
    def set_renpy_excluded_files(self, excluded_input):
        if isinstance(excluded_input, str):
            self.set("renpy_excluded_files", ", ".join([x.strip() for x in excluded_input.split(",") if x.strip()]))
        elif isinstance(excluded_input, list):
            self.set("renpy_excluded_files", ", ".join(excluded_input))
    def is_project_sync_enabled(self) -> bool:
        """Vérifie si la synchronisation des projets est activée"""
        return self.get('project_sync_enabled', True)

    def set_project_sync_enabled(self, enabled: bool):
        """Active/désactive la synchronisation des projets"""
        self.set('project_sync_enabled', enabled)

    def toggle_project_sync_enabled(self) -> bool:
        """Bascule la synchronisation des projets"""
        new_state = not self.is_project_sync_enabled()
        self.set_project_sync_enabled(new_state)
        return new_state

    # --- patterns d'extraction personnalisés ---
    def get_custom_extraction_patterns(self):
        """Récupère la configuration des patterns d'extraction personnalisés"""
        default = []
        return self.get("custom_extraction_patterns", default)

    def set_custom_extraction_patterns(self, patterns):
        """Définit la configuration des patterns d'extraction personnalisés"""
        self.set("custom_extraction_patterns", patterns)

    def add_custom_extraction_pattern(self, name, pattern, flags="", description="", enabled=False, test_text=""):
        """Ajoute un nouveau pattern d'extraction personnalisé"""
        patterns = self.get_custom_extraction_patterns()
        new_pattern = {
            "name": name,
            "pattern": pattern,
            "flags": flags,
            "enabled": enabled,
            "description": description,
            "test_text": test_text
        }
        patterns.append(new_pattern)
        self.set_custom_extraction_patterns(patterns)
        return len(patterns) - 1

    def update_custom_extraction_pattern(self, index, name=None, pattern=None, flags=None, description=None, enabled=None, test_text=None):
        """Met à jour un pattern d'extraction personnalisé existant"""
        patterns = self.get_custom_extraction_patterns()
        if 0 <= index < len(patterns):
            if name is not None:
                patterns[index]["name"] = name
            if pattern is not None:
                patterns[index]["pattern"] = pattern
            if flags is not None:
                patterns[index]["flags"] = flags
            if description is not None:
                patterns[index]["description"] = description
            if enabled is not None:
                patterns[index]["enabled"] = enabled
            if test_text is not None:
                patterns[index]["test_text"] = test_text
            self.set_custom_extraction_patterns(patterns)
            return True
        return False

    def remove_custom_extraction_pattern(self, index):
        """Supprime un pattern d'extraction personnalisé"""
        patterns = self.get_custom_extraction_patterns()
        if 0 <= index < len(patterns):
            patterns.pop(index)
            self.set_custom_extraction_patterns(patterns)
            return True
        return False

    def toggle_custom_extraction_pattern(self, index):
        """Active/désactive un pattern d'extraction personnalisé"""
        patterns = self.get_custom_extraction_patterns()
        if 0 <= index < len(patterns):  # ✅ Remplacer pattern_index par index
            patterns[index]["enabled"] = not patterns[index].get("enabled", False)
            self.set_custom_extraction_patterns(patterns)
            return patterns[index]["enabled"]
        return False

    def validate_custom_extraction_pattern(self, pattern, flags=""):
        """Valide un pattern regex personnalisé"""
        try:
            import re
            regex_flags = 0
            if 'i' in flags:
                regex_flags |= re.IGNORECASE
            if 'm' in flags:
                regex_flags |= re.MULTILINE
            if 's' in flags:
                regex_flags |= re.DOTALL
            
            re.compile(pattern, regex_flags)
            return True, None
        except re.error as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erreur inattendue: {e}"

    # --- debug/logging runtime ---
    def apply_debug_config_immediately(self):
        """Applique la configuration debug au logger (idempotent, sans boucle)."""
        if getattr(self, "_applying_debug", False): return
        self._applying_debug = True
        try:
            logger = get_logger()
            want = bool(self.get('debug_mode', False))
            # Niveau strict: 5 si ON, 3 si OFF
            level = 5 if want else 3
            logger.set_debug(want, level)
        finally:
            self._applying_debug = False

    def get_advanced_screen_options(self):
        """Récupère les options avancées de screen preferences"""
        default_options = {
            'language_selector': False,
            'fontsize_control': False,
            'textbox_opacity': False,
            'textbox_offset': False,
            'textbox_outline': False
        }
        return self.config.get("advanced_screen_options", default_options)
    
    def set_advanced_screen_options(self, options):
        """Sauvegarde les options avancées de screen preferences"""
        self.config["advanced_screen_options"] = options
        self.save_config()
    
    # ========== NOUVELLES MÉTHODES: Exclusions de cohérence précises (projet+fichier+ligne) ==========
    
    def get_coherence_exclusions(self, project_path=None):
        """
        Récupère les exclusions de cohérence.
        Si project_path est fourni, retourne les exclusions pour ce projet.
        Sinon, retourne toutes les exclusions (dict par projet).
        
        Source unique de vérité : les exclusions ajoutées via le rapport HTML interactif.
        """
        exclusions = self.config.get('coherence_custom_exclusions', {})
        
        # Garantir que c'est toujours un dictionnaire
        if not isinstance(exclusions, dict):
            log_message("ATTENTION", f"coherence_custom_exclusions n'est pas un dict ({type(exclusions).__name__}), réinitialisation", category="config")
            exclusions = {}
            self.config['coherence_custom_exclusions'] = exclusions
            self.save_config()
        
        # Normaliser la structure pour garantir des clés cohérentes (racine projet)
        normalized_exclusions, changed = self._normalize_coherence_exclusions_structure(exclusions)

        if changed:
            self.config['coherence_custom_exclusions'] = normalized_exclusions
            self.save_config()
            exclusions = normalized_exclusions
        else:
            exclusions = normalized_exclusions
        
        if project_path:
            project_key = self._normalize_project_key(project_path)
            return exclusions.get(project_key, [])
        return exclusions
    
    def add_coherence_exclusion(self, project_path, file_path, line, text):
        """
        Ajoute une exclusion spécifique pour un projet/fichier/ligne.
        
        Args:
            project_path: Chemin du projet Ren'Py
            file_path: Chemin relatif du fichier (ex: story/chapter_01.rpy)
            line: Numéro de ligne
            text: Texte à exclure
        
        Returns:
            True si ajouté, False si déjà présent
        """
        from datetime import datetime
        
        exclusions = self.get_coherence_exclusions()
        project_key = self._normalize_project_key(project_path)
        
        if project_key not in exclusions:
            exclusions[project_key] = []
        
        # Normaliser le chemin du fichier (remplacer les backslashes par des slashes)
        file_path_normalized = file_path.replace('\\', '/')
        
        # Vérifier si déjà présent
        normalized_text = text.strip() if isinstance(text, str) else ""
        for excl in exclusions[project_key]:
            if (excl['file'] == file_path_normalized and 
                excl['line'] == line and 
                excl['text'] == normalized_text):
                return False  # Déjà présent
        
        # Ajouter
        new_entry = {
            'file': file_path_normalized,
            'line': line,
            'text': normalized_text,
            'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        exclusions[project_key].append(new_entry)
        
        self.config['coherence_custom_exclusions'] = exclusions
        self.save_config()
        
        log_message("INFO", f"Exclusion ajoutée: {file_path_normalized}:{line} - {normalized_text[:50]}", category="coherence_exclusion")
        return True
    
    def remove_coherence_exclusion(self, project_path, file_path, line, text):
        """
        Supprime une exclusion spécifique.
        
        Returns:
            True si supprimé, False si non trouvé
        """
        exclusions = self.get_coherence_exclusions()
        project_key = self._normalize_project_key(project_path)
        
        if project_key not in exclusions:
            return False
        
        # Normaliser le chemin
        file_path_normalized = file_path.replace('\\', '/')
        normalized_text = text.strip() if isinstance(text, str) else ""
        
        # Trouver et supprimer
        for i, excl in enumerate(exclusions[project_key]):
            if (excl['file'] == file_path_normalized and 
                excl['line'] == line and 
                excl['text'] == normalized_text):
                exclusions[project_key].pop(i)
                
                # Supprimer le projet si plus d'exclusions
                if not exclusions[project_key]:
                    del exclusions[project_key]
                
                self.config['coherence_custom_exclusions'] = exclusions
                self.save_config()
                
                log_message("INFO", f"Exclusion retirée: {file_path_normalized}:{line}", category="coherence_exclusion")
                return True
        
        return False
    
    def clear_coherence_exclusions(self, project_path):
        """
        Supprime toutes les exclusions pour un projet.
        
        Returns:
            Nombre d'exclusions supprimées
        """
        exclusions = self.get_coherence_exclusions()
        project_key = self._normalize_project_key(project_path)
        
        if project_key not in exclusions:
            return 0
        
        count = len(exclusions[project_key])
        del exclusions[project_key]
        
        self.config['coherence_custom_exclusions'] = exclusions
        self.save_config()
        
        log_message("INFO", f"Toutes les exclusions supprimées pour le projet: {project_key} ({count} exclusions)", category="coherence_exclusion")
        return count
    
    def get_exclusion_count(self, project_path=None):
        """
        Retourne le nombre d'exclusions.
        Si project_path est fourni, compte pour ce projet uniquement.
        """
        if project_path:
            return len(self.get_coherence_exclusions(project_path))
        else:
            exclusions = self.get_coherence_exclusions()
            return sum(len(excl_list) for excl_list in exclusions.values())

    # --- Helpers internes pour les exclusions de cohérence ---
    def _normalize_project_key(self, project_path):
        """Normalise le chemin d'un projet pour unifier les clés d'exclusions."""
        try:
            if not isinstance(project_path, str):
                return ""
            normalized = project_path.strip().replace('\\', '/')
            if not normalized:
                return ""

            # Retirer un éventuel fichier final (.rpy, .json, etc.)
            if '.' in normalized.split('/')[-1]:
                normalized = '/'.join(normalized.split('/')[:-1]) or normalized

            segments = [seg for seg in normalized.split('/') if seg]
            lowered = [seg.lower() for seg in segments]

            # Couper à la racine du projet (avant 'game' ou 'tl')
            for marker in ('game', 'tl'):
                if marker in lowered:
                    idx = lowered.index(marker)
                    segments = segments[:idx]
                    lowered = lowered[:idx]
                    break

            if not segments:
                # Si on a tout supprimé (cas rare), revenir à la version nettoyée initiale
                return normalized.rstrip('/')

            root = '/'.join(segments)

            # Préserver le préfixe absolu si présent (ex: "E:" ou chemin UNC)
            if normalized.startswith('//'):
                root = '//' + root
            elif normalized.startswith('/') and not root.startswith('/'):
                root = '/' + root
            elif len(normalized) >= 2 and normalized[1] == ':' and not root.endswith(':'):
                # Chemins Windows (E:/...)
                drive = normalized[:2]
                if not root.lower().startswith(drive.lower()):
                    root = f"{drive}/{root}"

            return root.rstrip('/')
        except Exception as e:
            log_message("ATTENTION", f"Normalisation chemin projet échouée ({project_path}): {e}", category="config")
            return project_path

    def _normalize_coherence_exclusions_structure(self, exclusions_dict):
        """
        Normalise la structure des exclusions:
        - Clés = racine de projet
        - Chemins fichiers avec /
        - Textes trimés
        Retourne (dict_normalisé, bool_modifié)
        """
        normalized = {}
        modified = False

        if not isinstance(exclusions_dict, dict):
            return {}, True

        for raw_project, entries in exclusions_dict.items():
            project_key = self._normalize_project_key(raw_project)
            if not project_key:
                project_key = raw_project.strip() if isinstance(raw_project, str) else ""
            if not project_key:
                # Impossible d'associer cette entrée => ignorer
                modified = True
                continue

            if not isinstance(entries, list):
                modified = True
                continue

            target_list = normalized.setdefault(project_key, [])
            existing_signature = {(e.get('file'), e.get('line'), e.get('text')) for e in target_list if isinstance(e, dict)}

            for entry in entries:
                if not isinstance(entry, dict):
                    modified = True
                    continue

                file_path = entry.get('file', '')
                text_value = entry.get('text', '')
                line_value = entry.get('line', 0)

                if not isinstance(file_path, str) or not isinstance(text_value, str):
                    modified = True
                    continue

                file_normalized = file_path.replace('\\', '/').strip()
                text_normalized = text_value.strip()

                try:
                    line_int = int(line_value)
                except Exception:
                    line_int = 0

                if not file_normalized or not text_normalized or line_int <= 0:
                    modified = True
                    continue

                signature = (file_normalized, line_int, text_normalized)
                if signature in existing_signature:
                    continue

                normalized_entry = {
                    'file': file_normalized,
                    'line': line_int,
                    'text': text_normalized
                }
                if 'added_date' in entry:
                    normalized_entry['added_date'] = entry['added_date']

                target_list.append(normalized_entry)
                existing_signature.add(signature)

                if (file_normalized != file_path or
                        text_normalized != text_value or
                        line_int != line_value):
                    modified = True

            if project_key != raw_project:
                modified = True

        return normalized, modified


# Instance globale
try:
    config_manager = ConfigManager()
except Exception as e:
    # En cas d'erreur critique, créer une instance par défaut
    print(f"[CONFIG CRITICAL] Erreur création ConfigManager: {e}")
    import traceback
    traceback.print_exc()
    
    # Créer une instance minimale pour éviter les crashs
    class FallbackConfigManager:
        def __init__(self):
            self.config = DEFAULT_CONFIG.copy()
        def get(self, key, default=None):
            return self.config.get(key, default)
        def set(self, key, value):
            self.config[key] = value
        def save_config(self):
            pass
    
    config_manager = FallbackConfigManager()
