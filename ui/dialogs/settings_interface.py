# ui/interfaces/settings_interface_refactored.py - INTERFACE SETTINGS REFACTORISÉE
# Interface principale des paramètres avec onglets modulaires

"""
Interface utilisateur refactorisée pour les paramètres de l'application
- Structure modulaire avec onglets séparés dans ui/tab_settings/
- Interface principale qui orchestre les onglets
- Fonctions partagées centralisées
- Gestion cohérente des thèmes et notifications
"""

import tkinter as tk
from tkinter import ttk, filedialog
import sys
import os
import subprocess
from ui.themes import theme_manager
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import show_translated_messagebox, show_custom_messagebox
from infrastructure.config.constants import VERSION

# Imports des onglets modulaires
from ui.tab_settings.extraction_tab import create_extraction_tab
from ui.tab_settings.paths_tab import create_paths_tab
from ui.tab_settings.application_tab import create_application_tab
from ui.tab_settings.colors_tab import create_colors_tab


class UnifiedSettingsInterface:
    """Interface unifiée des paramètres avec onglets modulaires"""
    
    def __init__(self, parent_window, app_controller=None):
        """Initialise l'interface"""
        self.parent_window = parent_window
        self.app_controller = app_controller
        self.window = None
        self.notebook = None
        
        # Variables Tkinter pour tous les onglets
        self._init_all_variables()
        
        # Widgets de l'interface
        self.status_label = None
        self.operation_buttons = []
        self.cancel_operation_btn = None
        
        # Variables pour les onglets
        self.color_buttons = {}
        self.editor_path_vars = {}
        self.save_mode_combo = None
        self.notification_combo = None
        self.editor_combo = None
        self.preset_var = None
        
        # Aperçus pour les patterns
        self.codes_preview = None
        self.asterisks_preview = None
        self.tildes_preview = None

        self._create_interface()
        # Créer les onglets après l'initialisation complète
        self._create_tabs()
        
        # Enregistrer cette fenêtre dans le système de thème global
        theme_manager.register_window(self)

    def _init_all_variables(self):
        """Initialise toutes les variables Tkinter nécessaires"""
        try:
            # === VARIABLES ONGLET EXTRACTION & PROTECTION ===
            self.detect_duplicates_var = tk.BooleanVar(value=True)
            self.default_save_mode_var = tk.StringVar(value="Écraser l'original")
            self.project_progress_tracking_var = tk.BooleanVar(value=config_manager.get('project_progress_tracking', True))
            
            # Variables pour les contrôles de cohérence
            self.coherence_check_untranslated_var = tk.BooleanVar(value=True)
            self.coherence_check_ellipsis_var = tk.BooleanVar(value=True)
            self.coherence_check_escape_sequences_var = tk.BooleanVar(value=True)
            self.coherence_check_quotations_var = tk.BooleanVar(value=True)
            self.coherence_check_parentheses_var = tk.BooleanVar(value=True)
            self.coherence_check_deepl_ellipsis_var = tk.BooleanVar(value=True)
            self.coherence_check_isolated_percent_var = tk.BooleanVar(value=True)
            
            # Variable limite de lignes d'extraction
            line_limit = config_manager.get('extraction_line_limit')
            self.extraction_line_limit_var = tk.StringVar(value=str(line_limit) if line_limit else "")
            
            # Variables patterns avec valeurs par défaut
            self.code_pattern_var = tk.StringVar(value="RENPY_CODE_001")
            self.asterisk_pattern_var = tk.StringVar(value="RENPY_ASTERISK_001") 
            self.tilde_pattern_var = tk.StringVar(value="RENPY_TILDE_001")
            
            # === VARIABLES ONGLET CHEMINS D'ACCÈS ===
            self.sdk_path_var = tk.StringVar(value="")
            self.custom_editor_var = tk.StringVar(value="")
            
            # === VARIABLES ONGLET INTERFACE & APPLICATION ===
            self.auto_open_files_var = tk.BooleanVar(value=True)
            self.editor_choice_var = tk.StringVar(value="Défaut Windows")
            self.auto_open_folders_var = tk.BooleanVar(value=True)
            self.auto_open_coherence_report_var = tk.BooleanVar(value=True)
            self.dark_mode_var = tk.BooleanVar(value=True)
            self.show_output_path_var = tk.BooleanVar(value=False)
            self.current_language_var = tk.StringVar(value="Français")
            # self.project_sync_var supprimée - synchronisation toujours active via ProjectManager
            self.notification_mode_var = tk.StringVar(value="Statut seulement")
            self.debug_mode_var = tk.BooleanVar(value=False)
            
        except Exception as e:
            log_message("ERREUR", f"Erreur initialisation variables settings: {e}", category="settings")

    def _create_interface(self):
        """Crée l'interface utilisateur avec onglets"""
        # Fenêtre principale
        self.window = tk.Toplevel(self.parent_window)
        self.window.title("⚙️ Paramètres")
        self.window.geometry("1100x850")
        self.window.transient(self.parent_window)
        self.window.grab_set()
        
        # Appliquer le thème
        theme = theme_manager.get_theme()
        self.window.configure(bg=theme["bg"])
        theme_manager.apply_to_widget(self.window)
        
        # Centrer la fenêtre
        self._center_window()
        self.window.lift()
        self.window.focus_force()
        
        # Créer l'interface
        self._create_header()
        self._create_main_content()
        self._create_footer()
        
        # Charger la configuration APRÈS création de l'interface
        self._load_config()
        self.window.after(100, self._cleanup_notifications)
        
        # Appliquer le thème complet après création
        self.window.after(100, self._apply_theme_to_window)
        
        # Gestion de la fermeture
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        self._ensure_single_instance()

    def _center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"+{x}+{y}")

    def _create_header(self):
        """Crée l'en-tête de l'interface"""
        theme = theme_manager.get_theme()
        
        # Frame d'en-tête
        header_frame = tk.Frame(self.window, bg=theme["bg"])
        header_frame.pack(fill='x', padx=20, pady=15)
        
        # Titre principal
        title_label = tk.Label(
            header_frame,
            text="⚙️ Paramètres généraux de l'application",
            font=('Segoe UI Emoji', 16, 'bold'),
            bg=theme["bg"],
            fg=theme["accent"]
        )
        title_label.pack()
        
        # Sous-titre
        subtitle_label = tk.Label(
            header_frame,
            text="Configuration centralisée de l'application",
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        subtitle_label.pack(pady=(5, 0))

    def _create_main_content(self):
        """Crée le contenu principal avec onglets modulaires"""
        theme = theme_manager.get_theme()
        
        # Frame principal
        main_frame = tk.Frame(self.window, bg=theme["bg"])
        main_frame.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        
        # Notebook pour les onglets
        style = ttk.Style()
        
        # Style pour le notebook avec couleurs du thème
        style.configure("Custom.TNotebook", 
                    background=theme["bg"],
                    borderwidth=0)
        style.configure("Custom.TNotebook.Tab", 
                    background=theme["frame_bg"], 
                    foreground='#000000',
                    padding=[15, 6])
        style.map("Custom.TNotebook.Tab",
                background=[('selected', theme["accent"])],
                foreground=[('selected', '#000000')])
        
        self.notebook = ttk.Notebook(main_frame, style="Custom.TNotebook")
        self.notebook.pack(fill='both', expand=True)
        
        # Appliquer le style du notebook
        self._update_notebook_style()
        
        # Les onglets seront créés après l'initialisation complète

    def _create_tabs(self):
        """Crée tous les onglets en utilisant les modules séparés"""
        try:
            # Onglet 1: Interface & Application (première)
            application_tab = create_application_tab(self.notebook, self)
            self.notebook.add(application_tab, text="🎨 Interface & Application")
            
            # Onglet 2: Extraction & Protection (deuxième)
            extraction_tab = create_extraction_tab(self.notebook, self)
            self.notebook.add(extraction_tab, text="Extraction & Protection")
            
            # Onglet 3: Couleurs des boutons (troisième)
            colors_tab = create_colors_tab(self.notebook, self)
            self.notebook.add(colors_tab, text="🎨 Couleurs des boutons")
            
            # Onglet 4: Chemins d'accès (dernière)
            paths_tab = create_paths_tab(self.notebook, self)
            self.notebook.add(paths_tab, text="🛠️ Chemins d'accès")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur création onglets: {e}", category="settings")
            import traceback
            log_message("ERREUR", f"Traceback: {traceback.format_exc()}", category="settings")

    def _create_footer(self):
        """Crée le pied de page avec les boutons"""
        theme = theme_manager.get_theme()
        
        footer_frame = tk.Frame(self.window, bg=theme["bg"])
        footer_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        buttons_frame = tk.Frame(footer_frame, bg=theme["bg"])
        buttons_frame.pack(fill='x')
        
        # Bouton À propos (à gauche)
        about_btn = tk.Button(
            buttons_frame,
            text="ℹ️ À propos",
            command=self._show_about,
            bg=theme["button_help_bg"],
            fg="#000000",
            font=('Segoe UI', 9),
            pady=6,
            width=15
        )
        about_btn.pack(side='left')
        
        # Bouton Fermer (tout à droite)
        close_btn = tk.Button(
            buttons_frame,
            text="❌ Fermer",
            command=self._on_close,
            bg=theme["button_danger_bg"],
            fg="#000000",
            font=('Segoe UI', 9),
            pady=6,
            width=15
        )
        close_btn.pack(side='right')

        reset_btn = tk.Button(
            buttons_frame,
            text="Par défaut",
            command=self._reset_defaults,
            bg=theme["button_tertiary_bg"],
            fg="#000000",
            font=('Segoe UI', 9),
            pady=6,
            width=15
        )
        reset_btn.pack(side='right', padx=(0, 10))

    def _load_config(self):
        """Charge la configuration depuis le fichier"""
        try:
            # Charger les valeurs depuis config_manager
            self.detect_duplicates_var.set(config_manager.get('detect_duplicates', True))
            
            # Mode de sauvegarde - Mapping des valeurs techniques vers libellés
            save_mode_technical = config_manager.get('default_save_mode', "overwrite")
            save_mode_mapping = {
                "overwrite": "Écraser l'original",
                "new_file": "Créer nouveau fichier"
            }
            save_mode_display = save_mode_mapping.get(save_mode_technical, "Écraser l'original")
            self.default_save_mode_var.set(save_mode_display)
            
            # SDK Path
            sdk_path = config_manager.get_renpy_sdk_path()
            if sdk_path:
                self.sdk_path_var.set(sdk_path)
            
            # Custom Editor Path
            custom_editor_path = config_manager.get('custom_editor_path', '')
            if custom_editor_path:
                self.custom_editor_var.set(custom_editor_path)
            
            # Variables d'interface
            self.auto_open_files_var.set(config_manager.get('auto_open_files', True))
            self.auto_open_folders_var.set(config_manager.get('auto_open_folders', True))
            self.auto_open_coherence_report_var.set(config_manager.get('auto_open_coherence_report', True))
            self.show_output_path_var.set(config_manager.get('show_output_path', False))
            # project_sync_var supprimée - synchronisation toujours active
            
            # Mode sombre - Synchroniser avec le ThemeManager
            dark_mode = config_manager.get('dark_mode', True)
            self.dark_mode_var.set(dark_mode)
            
            # S'assurer que le ThemeManager est synchronisé
            current_theme = theme_manager.current_theme
            expected_theme = "sombre" if dark_mode else "clair"
            if current_theme != expected_theme:
                theme_manager.set_theme(expected_theme)
            
            # Mode debug
            debug_mode = config_manager.get('debug_mode', False)
            self.debug_mode_var.set(debug_mode)
            
            # Éditeur de code
            editor_choice = config_manager.get('editor_choice', "Défaut Windows")
            self.editor_choice_var.set(editor_choice)
            
            # Mode de notification - Mapping des valeurs techniques vers libellés
            notification_mode_technical = config_manager.get('notification_mode', "status_only")
            notification_mapping = {
                "status_only": "Statut seulement",
                "detailed_popups": "Popups détaillés"
            }
            notification_mode_display = notification_mapping.get(notification_mode_technical, "Statut seulement")
            self.notification_mode_var.set(notification_mode_display)
            
            # Patterns de protection
            code_prefix = config_manager.get_protection_placeholder('code_prefix')
            asterisk_prefix = config_manager.get_protection_placeholder('asterisk_prefix')
            tilde_prefix = config_manager.get_protection_placeholder('tilde_prefix')
            
            self.code_pattern_var.set(code_prefix)
            self.asterisk_pattern_var.set(asterisk_prefix)
            self.tilde_pattern_var.set(tilde_prefix)
            
            # Chemins d'éditeurs personnalisés
            for editor_name in ['VSCode', 'Sublime Text', 'Notepad++', 'Atom/Pulsar']:
                custom_path = config_manager.get_editor_custom_path(editor_name)
                if editor_name in self.editor_path_vars:
                    self.editor_path_vars[editor_name].set(custom_path or "")
            
            # 🔧 CORRECTIF: Mettre à jour la combobox éditeur après chargement du chemin personnalisé
            # Seulement si editor_combo existe ET n'est pas None
            if hasattr(self, 'editor_combo') and self.editor_combo is not None:
                try:
                    from ui.tab_settings.application_tab import _update_editor_combo_values
                    _update_editor_combo_values(self)
                except Exception as e:
                    log_message("DEBUG", f"Impossible de mettre à jour editor_combo au chargement: {e}", category="settings")
            
            log_message("INFO", "Configuration chargée dans l'interface settings", category="settings")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur chargement configuration: {e}", category="settings")

    def _save_config(self):
        """Sauvegarde la configuration dans le fichier"""
        try:
            # Sauvegarder toutes les variables
            config_manager.set('detect_duplicates', self.detect_duplicates_var.get())
            
            # Mode de sauvegarde - Mapping des libellés vers valeurs techniques
            save_mode_display = self.default_save_mode_var.get()
            save_mode_mapping = {
                "Écraser l'original": "overwrite",
                "Créer nouveau fichier": "new_file"
            }
            save_mode_technical = save_mode_mapping.get(save_mode_display, "overwrite")
            config_manager.set('default_save_mode', save_mode_technical)
            config_manager.set('project_progress_tracking', self.project_progress_tracking_var.get())
            config_manager.set('auto_open_files', self.auto_open_files_var.get())
            config_manager.set('auto_open_folders', self.auto_open_folders_var.get())
            config_manager.set('auto_open_coherence_report', self.auto_open_coherence_report_var.get())
            config_manager.set('show_output_path', self.show_output_path_var.get())
            # project_sync toujours True - géré par ProjectManager
            config_manager.set('dark_mode', self.dark_mode_var.get())
            config_manager.set('debug_mode', self.debug_mode_var.get())
            config_manager.set('editor_choice', self.editor_choice_var.get())
            
            # Mode de notification - Mapping des libellés vers valeurs techniques
            notification_mode_display = self.notification_mode_var.get()
            notification_mapping = {
                "Statut seulement": "status_only",
                "Popups détaillés": "detailed_popups"
            }
            notification_mode_technical = notification_mapping.get(notification_mode_display, "status_only")
            config_manager.set('notification_mode', notification_mode_technical)
            
            # Sauvegarder le SDK path
            sdk_path = self.sdk_path_var.get().strip()
            if sdk_path:
                config_manager.set_renpy_sdk_path(sdk_path)
            
            # Sauvegarder le chemin éditeur personnalisé
            custom_editor_path = self.custom_editor_var.get().strip()
            config_manager.set('custom_editor_path', custom_editor_path)
            
            # Sauvegarder les patterns
            config_manager.set_protection_placeholder('code_prefix', self.code_pattern_var.get())
            config_manager.set_protection_placeholder('asterisk_prefix', self.asterisk_pattern_var.get())
            config_manager.set_protection_placeholder('tilde_prefix', self.tilde_pattern_var.get())
            
            # Sauvegarder les chemins d'éditeurs
            for editor_name, var in self.editor_path_vars.items():
                path = var.get().strip()
                config_manager.set_editor_custom_path(editor_name, path if path else None)
            
            log_message("INFO", "Configuration sauvegardée depuis l'interface settings", category="settings")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur sauvegarde configuration: {e}", category="settings")

    def _apply_theme_to_window(self):
        """Applique le thème à toute la fenêtre"""
        try:
            theme = theme_manager.get_theme()
            theme_manager.apply_to_widget(self.window)
            log_message("DEBUG", "Thème appliqué à la fenêtre settings", category="settings")
        except Exception as e:
            log_message("ERREUR", f"Erreur application thème: {e}", category="settings")

    def _cleanup_notifications(self):
        """Nettoie les notifications temporaires"""
        try:
            # Cette méthode peut être étendue pour nettoyer les notifications
            pass
        except Exception as e:
            log_message("ERREUR", f"Erreur nettoyage notifications: {e}", category="settings")

    def _ensure_single_instance(self):
        """S'assure qu'une seule instance de l'interface est ouverte"""
        try:
            # Vérifier si une autre instance existe déjà
            if hasattr(self.parent_window, '_settings_window_open'):
                self.parent_window._settings_window_open = True
            else:
                self.parent_window._settings_window_open = True
                
            # Nettoyer lors de la fermeture
            self.window.bind('<Destroy>', lambda e: setattr(self.parent_window, '_settings_window_open', False))
            
        except Exception as e:
            log_message("ERREUR", f"Erreur gestion instance unique: {e}", category="settings")

    def _on_close(self):
        """Gère la fermeture de l'interface (cacher pour persistance)"""
        try:
            # Sauvegarder la configuration avant de fermer
            self._save_config()
            
            # Afficher une notification de confirmation
            self._show_toast("✅ Tous les paramètres ont été sauvegardés", "success")
            
            # Libérer le grab modal avant de cacher la fenêtre
            try:
                self.window.grab_release()
            except:
                pass
            
            # Détruire la fenêtre
            self.window.destroy()
            
            log_message("INFO", "Interface settings fermée", category="settings")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur fermeture interface: {e}", category="settings")

    def _reset_defaults(self):
        """Remet tous les paramètres par défaut"""
        try:
            from infrastructure.helpers.unified_functions import show_custom_askyesnocancel
            
            response = show_custom_askyesnocancel(
                "Remettre les paramètres par défaut",
                "Voulez-vous vraiment remettre tous les paramètres par défaut ?",
                parent=self.window
            )
            
            if response:
                # Reset toutes les variables
                self.detect_duplicates_var.set(True)
                self.default_save_mode_var.set("Écraser l'original")
                self.project_progress_tracking_var.set(True)
                self.auto_open_files_var.set(True)
                self.auto_open_folders_var.set(True)
                self.auto_open_coherence_report_var.set(True)
                self.show_output_path_var.set(False)
                # project_sync toujours True par défaut
                self.dark_mode_var.set(True)
                self.debug_mode_var.set(False)
                self.editor_choice_var.set("Défaut Windows")
                self.notification_mode_var.set("Statut seulement")
                
                # Reset SDK path
                self.sdk_path_var.set("")
                
                # Reset custom editor path
                self.custom_editor_var.set("")
                
                # Reset patterns
                self.code_pattern_var.set("RENPY_CODE_001")
                self.asterisk_pattern_var.set("RENPY_ASTERISK_001")
                self.tilde_pattern_var.set("RENPY_TILDE_001")
                
                # Reset éditeurs
                for var in self.editor_path_vars.values():
                    var.set("")
                
                # Sauvegarder
                self._save_config()
                
                # Recharger l'interface
                self._load_config()
                
                self._show_toast("Paramètres remis par défaut")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur reset paramètres: {e}", category="settings")

    def _show_about(self):
        """Affiche la fenêtre À propos"""
        try:
            from datetime import datetime
            current_year = datetime.now().year
            
            about_text = f"""
RenExtract - Générateur de Traductions Ren'Py

Version: {VERSION}

Développé avec ❤️ pour la communauté Ren'Py

Fonctionnalités:
• Extraction automatique de textes
• Génération de traductions
• Outils de maintenance
• Interface moderne et intuitive

© 2024-{current_year} RenExtract Project
            """
            
            show_custom_messagebox(
                'showinfo',
                'À propos de RenExtract',
                [(about_text, "")],
                theme_manager.get_theme(),
                parent=self.window
            )
            
        except Exception as e:
            log_message("ERREUR", f"Erreur affichage À propos: {e}", category="settings")

    def _show_toast(self, message, type="info"):
        """Affiche une notification toast"""
        try:
            # Essayer d'accéder au notification_manager via l'app_controller
            if hasattr(self, 'app_controller') and self.app_controller and hasattr(self.app_controller, 'main_window'):
                main_window = self.app_controller.main_window
                if hasattr(main_window, 'components') and 'notifications' in main_window.components:
                    notification_manager = main_window.components['notifications']
                    
                    # Convertir le type en ToastType
                    toast_type_mapping = {
                        "info": "info",
                        "success": "success", 
                        "warning": "warning",
                        "error": "error"
                    }
                    
                    toast_type = toast_type_mapping.get(type, "info")
                    
                    # Afficher la notification
                    notification_manager.notify(
                        message=message,
                        notification_type='TOAST',
                        toast_type=toast_type,
                        duration=3000
                    )
                    return
            
            # Fallback : utiliser le système global
            from ui.notification_manager import notification_manager
            
            # Convertir le type en ToastType
            toast_type_mapping = {
                "info": "info",
                "success": "success", 
                "warning": "warning",
                "error": "error"
            }
            
            toast_type = toast_type_mapping.get(type, "info")
            
            # Afficher la notification
            notification_manager.notify(
                message=message,
                notification_type='TOAST',
                toast_type=toast_type,
                duration=3000
            )
                
        except Exception as e:
            log_message("ERREUR", f"Erreur affichage toast: {e}", category="settings")
            # Fallback simple
            log_message("INFO", f"Toast: {message}", category="settings")

    # === MÉTHODES PARTAGÉES POUR LES ONGLETS ===
    # Ces méthodes sont appelées depuis les onglets modulaires

    def _on_line_limit_changed(self, event=None):
        """Appelé quand la limite de lignes change"""
        try:
            limit_value = self.extraction_line_limit_var.get().strip()
            
            # Validation
            if limit_value:
                try:
                    limit_int = int(limit_value)
                    if limit_int <= 0:
                        self._show_toast("⚠️ La limite doit être positive", "warning")
                        return
                    elif limit_int > 100000:
                        self._show_toast("⚠️ Limite très élevée (>100k)", "warning")
                except ValueError:
                    self._show_toast("⚠️ Valeur numérique requise", "warning")
                    return
            
            # Sauvegarder
            self._save_line_limit()
            self._show_toast("📄 Limite de lignes mise à jour")
            
        except Exception as e:
            log_message("DEBUG", f"Erreur changement limite lignes: {e}", category="settings")

    def _save_line_limit(self):
        """Sauvegarde la limite de lignes dans la config"""
        try:
            limit_value = self.extraction_line_limit_var.get().strip()
            if limit_value:
                config_manager.set("extraction_line_limit", int(limit_value))
            else:
                config_manager.set("extraction_line_limit", None)
                
        except Exception as e:
            log_message("DEBUG", f"Erreur sauvegarde limite lignes: {e}", category="settings")

    def _on_pattern_changed(self, event=None):
        """Appelé quand un pattern change - validation en temps réel SANS sauvegarde"""
        try:
            # Validation rapide des doublons en temps réel
            patterns = [
                self.code_pattern_var.get().strip(),
                self.asterisk_pattern_var.get().strip(), 
                self.tilde_pattern_var.get().strip()
            ]
            
            # Détection doublons (affichage seulement, pas de sauvegarde)
            if len(set(patterns)) != len(patterns):
                self._show_toast("⚠️ Attention: doublons détectés", "warning")
            else:
                # Mise à jour de l'aperçu seulement (pas de sauvegarde)
                self._update_pattern_previews()
                
        except Exception as e:
            log_message("ERREUR", f"Erreur changement patterns: {e}", category="ui_settings")

    def _update_pattern_previews(self):
        """Met à jour les aperçus en temps réel pour chaque pattern avec vraie incrémentation"""
        try:
            if not self.codes_preview or not self.asterisks_preview or not self.tildes_preview:
                return
            
            # Utiliser le générateur de placeholders pour créer une vraie incrémentation
            from core.services.extraction.placeholder_generator import SimplePlaceholderGenerator
            
            # Aperçu Codes/Variables
            codes_pattern = self.code_pattern_var.get().strip()
            if codes_pattern:
                try:
                    # Créer un générateur et générer 3 exemples consécutifs
                    codes_generator = SimplePlaceholderGenerator(codes_pattern)
                    codes_examples = []
                    for i in range(3):
                        codes_examples.append(codes_generator.next_placeholder())
                    codes_preview_text = f"{codes_pattern} → {', '.join(codes_examples)}"
                except Exception:
                    codes_preview_text = f"{codes_pattern} → Pattern invalide"
            else:
                codes_preview_text = "Pattern vide"
            
            self.codes_preview.config(state='normal')
            self.codes_preview.delete(1.0, tk.END)
            self.codes_preview.insert(1.0, codes_preview_text)
            self.codes_preview.config(state='disabled')
            
            # Aperçu Astérisques
            asterisks_pattern = self.asterisk_pattern_var.get().strip()
            if asterisks_pattern:
                try:
                    # Créer un générateur et générer 3 exemples consécutifs
                    asterisks_generator = SimplePlaceholderGenerator(asterisks_pattern)
                    asterisks_examples = []
                    for i in range(3):
                        asterisks_examples.append(asterisks_generator.next_placeholder())
                    asterisks_preview_text = f"{asterisks_pattern} → {', '.join(asterisks_examples)}"
                except Exception:
                    asterisks_preview_text = f"{asterisks_pattern} → Pattern invalide"
            else:
                asterisks_preview_text = "Pattern vide"
            
            self.asterisks_preview.config(state='normal')
            self.asterisks_preview.delete(1.0, tk.END)
            self.asterisks_preview.insert(1.0, asterisks_preview_text)
            self.asterisks_preview.config(state='disabled')
            
            # Aperçu Tildes
            tildes_pattern = self.tilde_pattern_var.get().strip()
            if tildes_pattern:
                try:
                    # Créer un générateur et générer 3 exemples consécutifs
                    tildes_generator = SimplePlaceholderGenerator(tildes_pattern)
                    tildes_examples = []
                    for i in range(3):
                        tildes_examples.append(tildes_generator.next_placeholder())
                    tildes_preview_text = f"{tildes_pattern} → {', '.join(tildes_examples)}"
                except Exception:
                    tildes_preview_text = f"{tildes_pattern} → Pattern invalide"
            else:
                tildes_preview_text = "Pattern vide"
            
            self.tildes_preview.config(state='normal')
            self.tildes_preview.delete(1.0, tk.END)
            self.tildes_preview.insert(1.0, tildes_preview_text)
            self.tildes_preview.config(state='disabled')
            
        except Exception as e:
            log_message("ERREUR", f"Erreur mise à jour aperçus: {e}", category="ui_settings")

    def _save_simple_patterns(self):
        """Sauvegarde les patterns courts avec validation"""
        try:
            # Validation avant sauvegarde
            patterns = [
                ("code_prefix", self.code_pattern_var.get()),
                ("asterisk_prefix", self.asterisk_pattern_var.get()),
                ("tilde_prefix", self.tilde_pattern_var.get())
            ]
            
            # Vérifier les doublons
            pattern_values = [p[1].strip() for p in patterns]
            if len(set(pattern_values)) != len(pattern_values):
                log_message("ATTENTION", "Tentative de sauvegarde avec doublons - ignorée", category="ui_settings")
                return False
            
            # Sauvegarder si valide
            for key, value in patterns:
                config_manager.set_protection_placeholder(key, value)
            
            log_message("INFO", f"Patterns sauvegardés: CODE='{self.code_pattern_var.get()}', "
                            f"ASTERISK='{self.asterisk_pattern_var.get()}', "
                            f"TILDE='{self.tilde_pattern_var.get()}'", category="ui_settings")
            return True
            
        except Exception as e:
            log_message("ERREUR", f"Erreur sauvegarde patterns: {e}", category="ui_settings")
            return False

    def _reset_simple_patterns(self):
        """Remet les patterns par défaut"""
        try:
            self.code_pattern_var.set("RENPY_CODE_001")
            self.asterisk_pattern_var.set("RENPY_ASTERISK_001")
            self.tilde_pattern_var.set("RENPY_TILDE_001")
            
            self._save_simple_patterns()
            self._update_pattern_previews()
            self._show_toast("Patterns remis par défaut")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur reset patterns: {e}", category="ui_settings")

    def _test_simple_patterns(self):
        """Teste la validité des patterns courts avec détection de doublons"""
        try:
            from core.services.extraction.placeholder_generator import SimplePlaceholderGenerator
            
            patterns = [
                ("Codes", self.code_pattern_var.get()),
                ("Astérisques", self.asterisk_pattern_var.get()),
                ("Tildes", self.tilde_pattern_var.get())
            ]
            
            # VÉRIFICATION DES DOUBLONS EN PREMIER
            pattern_values = [pattern[1].strip() for pattern in patterns]
            duplicates = []
            
            for i, pattern1 in enumerate(pattern_values):
                for j, pattern2 in enumerate(pattern_values):
                    if i != j and pattern1 == pattern2 and pattern1 not in duplicates:
                        duplicates.append(pattern1)
            
            if duplicates:
                self._show_toast(f"❌ Doublons détectés: {', '.join(duplicates)}", "error")
                return  # ARRÊTER LE TEST ICI
            
            # VÉRIFICATION DES PATTERNS VIDES
            empty_patterns = [name for name, pattern in patterns if not pattern.strip()]
            if empty_patterns:
                self._show_toast(f"❌ Patterns vides: {', '.join(empty_patterns)}", "error")
                return
            
            # TESTS DE GÉNÉRATION
            results = []
            all_valid = True
            
            for name, pattern in patterns:
                try:
                    # Validation des caractères interdits
                    forbidden_chars = ['"', "'", '\n', '\r', '\t', '\\', '/', '<', '>', '|', '?', '*']
                    found_forbidden = [char for char in forbidden_chars if char in pattern]
                    
                    if found_forbidden:
                        results.append(f"❌ {name}: Caractères interdits {found_forbidden}")
                        all_valid = False
                        continue
                    
                    # Test de génération
                    generator = SimplePlaceholderGenerator(pattern)
                    info = generator.get_pattern_info()
                    
                    # Générer quelques exemples
                    examples = []
                    for i in range(3):
                        examples.append(generator.next_placeholder())
                    
                    results.append(f"✅ {name}: {pattern} → {', '.join(examples)}")
                    
                except Exception as e:
                    results.append(f"❌ {name}: {pattern} → Erreur: {str(e)}")
                    all_valid = False
            
            # NOTIFICATION TOAST UNIQUEMENT (pas de popup)
            if all_valid:
                self._show_toast("✅ Tous les patterns sont valides", "success")
            else:
                self._show_toast("❌ Certains patterns ont des erreurs", "error")
            
            # Log détaillé pour le débogage
            log_message("INFO", f"Test patterns - Résultats:", category="ui_settings")
            for result in results:
                log_message("INFO", f"  {result}", category="ui_settings")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur test patterns: {e}", category="ui_settings")
            self._show_toast("❌ Erreur lors du test", "error")

    # === MÉTHODES POUR LES ONGLETS CHEMINS D'ACCÈS ===
    
    def _browse_sdk_path(self):
        """Ouvre le dialogue de sélection pour le SDK"""
        try:
            current_path = self.sdk_path_var.get()
            initial_dir = os.path.dirname(current_path) if current_path else "C:\\"
            
            folder_path = tk.filedialog.askdirectory(
                title="🛠️ Sélectionner le dossier SDK Ren'Py",
                initialdir=initial_dir
            )
            
            if folder_path:
                self.sdk_path_var.set(folder_path)
                config_manager.set_sdk_path(folder_path)
                self._show_toast("🛠️ Chemin SDK configuré")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur sélection chemin SDK: {e}", category="ui_settings")

    def _show_sdk_help(self):
        """Affiche l'aide pour le SDK"""
        try:
            help_text = """
🛠️ AIDE - Configuration SDK Ren'Py

Le SDK Ren'Py est nécessaire pour :
• Compiler les projets Ren'Py
• Générer les distributions
• Accéder aux outils de développement

Chemin requis :
• Dossier contenant renpy.exe
• Exemple : C:\\Ren'Py\\renpy-8.1.3-sdk\\
• Ne pas pointer directement sur renpy.exe

Si vous n'avez pas le SDK :
• Téléchargez-le depuis renpy.org
• Installez-le dans un dossier accessible
• Pointez vers le dossier d'installation
            """
            
            show_custom_messagebox(
                'showinfo',
                'Aide - SDK Ren\'Py',
                [(help_text, "")],
                theme_manager.get_theme(),
                parent=self.window
            )
            
        except Exception as e:
            log_message("ERREUR", f"Erreur affichage aide SDK: {e}", category="ui_settings")

    def _browse_editor_path(self, editor_name):
        """Ouvre le dialogue de sélection pour un éditeur"""
        try:
            current_path = self.editor_path_vars[editor_name].get()
            initial_dir = os.path.dirname(current_path) if current_path else "C:\\"
            
            file_path = tk.filedialog.askopenfilename(
                title=f"📝 Sélectionner l'exécutable de {editor_name}",
                initialdir=initial_dir,
                filetypes=[("Exécutables", "*.exe"), ("Tous fichiers", "*.*")]
            )
            
            if file_path:
                self.editor_path_vars[editor_name].set(file_path)
                self._save_editor_path(editor_name, file_path)
                self._show_toast(f"📝 Chemin {editor_name} configuré")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur sélection chemin {editor_name}: {e}", category="ui_settings")

    def _test_editor_path(self, editor_name):
        """Teste si le chemin de l'éditeur est valide"""
        try:
            path = self.editor_path_vars[editor_name].get().strip()
            
            if not path:
                self._show_toast(f"⚠️ Aucun chemin configuré pour {editor_name}", "warning")
                return
            
            if os.path.exists(path) and os.path.isfile(path):
                # Test simple : vérifier que le fichier existe et est exécutable
                try:
                    # Test rapide avec --version (marche pour la plupart des éditeurs)
                    result = subprocess.run([path, "--version"], 
                                        capture_output=True, 
                                        timeout=3, 
                                        text=True)
                    self._show_toast(f"✅ {editor_name} : Chemin valide", "success")
                except subprocess.TimeoutExpired:
                    self._show_toast(f"✅ {editor_name} : Chemin valide (timeout OK)", "success")
                except Exception:
                    # Si --version échoue, on considère que le fichier existe = OK
                    self._show_toast(f"✅ {editor_name} : Chemin valide", "success")
            else:
                self._show_toast(f"❌ {editor_name} : Chemin non valide", "error")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur test chemin {editor_name}: {e}", category="ui_settings")
            self._show_toast(f"❌ Erreur test {editor_name}", "error")

    def _on_editor_path_changed(self, editor_name):
        """Appelé quand un chemin d'éditeur change"""
        try:
            path = self.editor_path_vars[editor_name].get().strip()
            self._save_editor_path(editor_name, path)
        except Exception as e:
            log_message("ERREUR", f"Erreur changement chemin {editor_name}: {e}", category="ui_settings")

    def _save_editor_path(self, editor_name, path):
        """Sauvegarde le chemin d'un éditeur"""
        try:
            config_manager.set_editor_custom_path(editor_name, path)
            log_message("INFO", f"Chemin {editor_name} sauvegardé: {path}", category="ui_settings")
        except Exception as e:
            log_message("ERREUR", f"Erreur sauvegarde chemin {editor_name}: {e}", category="ui_settings")

    def _reset_editor_paths(self):
        """Remet tous les chemins d'éditeurs à vide"""
        try:
            confirmation_message = [
                ("CONFIRMATION REQUISE\n\n", "bold_red"),
                ("Voulez-vous vraiment ", "normal"),
                ("supprimer tous les chemins personnalisés", "bold"),
                (" des éditeurs ?\n\n", "normal"),
                ("Les éditeurs utiliseront à nouveau ", "yellow"),
                ("leurs chemins par défaut", "bold"),
                (".", "normal")
            ]
            
            response = show_custom_messagebox(
                'askyesno',
                'Remettre les chemins par défaut',
                confirmation_message,
                theme_manager.get_theme(),
                yes_text="Oui, remettre par défaut",
                no_text="Non, conserver",
                parent=self.window,
                yes_width=25,
                no_width=25
            )
            
            if response:
                # Reset dans la config
                config_manager.reset_editor_custom_paths()
                
                # Mettre à jour l'interface
                for editor_name in self.editor_path_vars:
                    self.editor_path_vars[editor_name].set("")
                
                self._show_toast("🔄 Chemins d'éditeurs remis par défaut")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur reset chemins éditeurs: {e}", category="ui_settings")

    def _show_editors_help(self):
        """Affiche l'aide pour les éditeurs"""
        try:
            help_text = """
📝 AIDE - Configuration des éditeurs

Les éditeurs personnalisés permettent d'ouvrir :
• Fichiers depuis l'interface temps réel
• Rapports HTML de cohérence
• Fichiers de traduction

Éditeurs supportés :
• VSCode (Visual Studio Code)
• Sublime Text
• Notepad++
• Atom/Pulsar

Configuration :
• Laissez vide pour utiliser les chemins par défaut
• Pointez vers l'exécutable (.exe) de l'éditeur
• Utilisez le bouton "Parcourir" pour sélectionner
• Testez avec le bouton "🧪" pour vérifier
            """
            
            show_custom_messagebox(
                'showinfo',
                'Aide - Éditeurs de code',
                [(help_text, "")],
                theme_manager.get_theme(),
                parent=self.window
            )
            
        except Exception as e:
            log_message("ERREUR", f"Erreur affichage aide éditeurs: {e}", category="ui_settings")

    def _show_paths_help(self):
        """Affiche l'aide pour les chemins d'accès"""
        try:
            help_text = [
                ("🛠️ AIDE - Chemins d'accès\n", "bold"),
                ("\n", ""),
                ("📁 SDK Ren'Py\n", "bold_green"),
                ("• Chemin vers le dossier contenant renpy.exe\n", ""),
                ("• Nécessaire pour la génération et l'extraction\n", ""),
                ("• Exemple : C:\\RenPy\\renpy-8.1.3-sdk\n", "italic"),
                ("\n", ""),
                ("✏️ Éditeur personnalisé\n", "bold_blue"),
                ("• Chemin vers votre éditeur de code préféré\n", ""),
                ("• Optionnel : utilise l'éditeur par défaut si vide\n", ""),
                ("• Le nom de l'éditeur sera détecté automatiquement\n", ""),
                ("• Exemple : C:\\Program Files\\Microsoft VS Code\\Code.exe\n", "italic"),
                ("\n", ""),
                ("🧪 Test des chemins\n", "bold_yellow"),
                ("• Vérifie que les chemins sont valides\n", ""),
                ("• Teste l'existence des fichiers/dossiers\n", ""),
                ("\n", ""),
                ("💡 Conseils\n", "bold"),
                ("• Utilisez le bouton 'Parcourir' pour naviguer facilement\n", ""),
                ("• Les chemins sont sauvegardés automatiquement\n", ""),
                ("• Vous pouvez réinitialiser à tout moment\n", "")
            ]
            
            show_custom_messagebox(
                'info',
                'Aide - Chemins d\'accès',
                help_text,
                theme_manager.get_theme(),
                parent=self.window
            )
                
        except Exception as e:
            log_message("ERREUR", f"Erreur affichage aide chemins: {e}", category="ui_settings")

    def _show_extraction_protection_help(self):
        """Affiche l'aide pour l'extraction et protection"""
        try:
            help_text = [
                ("🛡️ AIDE - Extraction & Protection", "bold"),
                ("\n", ""),
                ("🔧 Options de protection", "bold_green"),
                ("• Détecter et gérer les doublons : Évite les traductions en double\n", ""),
                ("• Suivi de progression : Surveille l'avancement des projets\n", ""),
                ("• Contrôles après extraction : Configuration des vérifications\n", ""),
                ("\n", ""),
                ("📄 Limite par fichier", "bold_blue"),
                ("• Définit le nombre maximum de lignes par fichier\n", ""),
                ("• Évite les fichiers trop volumineux\n", ""),
                ("• Exemple : 1000 lignes maximum\n", "italic"),
                ("\n", ""),
                ("💾 Mode de sauvegarde", "bold_yellow"),
                ("• Écraser l'original : Remplace le fichier existant\n", ""),
                ("• Créer nouveau fichier : Génère un fichier .new\n", ""),
                ("\n", ""),
                ("🔧 Patterns personnalisés", "bold"),
                ("• Codes/Variables : Patterns pour les codes de jeu\n", ""),
                ("• Astérisques : Patterns pour les éléments spéciaux\n", ""),
                ("• Tildes : Patterns pour les séparateurs\n", ""),
                ("\n", ""),
                ("💡 Conseils", "bold"),
                ("• Utilisez 'Tester' pour valider vos patterns\n", ""),
                ("• 'Défaut' restaure les valeurs recommandées\n", ""),
                ("• Les patterns sont sauvegardés automatiquement\n", "")
            ]
            
            show_custom_messagebox(
                'info',
                'Aide - Extraction & Protection',
                help_text,
                theme_manager.get_theme(),
                parent=self.window
            )
                
        except Exception as e:
            log_message("ERREUR", f"Erreur affichage aide extraction: {e}", category="ui_settings")

    # === MÉTHODES POUR L'ONGLET INTERFACE & APPLICATION ===
    
    def _on_interface_option_changed(self):
        """Appelé quand une option d'interface change"""
        try:
            # Sauvegarder automatiquement
            config_manager.set('auto_open_files', self.auto_open_files_var.get())
            config_manager.set('auto_open_folders', self.auto_open_folders_var.get())
            config_manager.set('auto_open_coherence_report', self.auto_open_coherence_report_var.get())
            config_manager.set('show_output_path', self.show_output_path_var.get())
            # project_sync toujours True - géré par ProjectManager
            
            # Mettre à jour l'affichage du champ de sortie dans l'interface principale
            if self.app_controller and hasattr(self.app_controller, 'main_window'):
                main_window = self.app_controller.main_window
                if hasattr(main_window, 'components') and 'buttons' in main_window.components:
                    buttons_frame = main_window.components['buttons']
                    if hasattr(buttons_frame, '_update_output_field_visibility'):
                        buttons_frame._update_output_field_visibility()
            
            self._show_toast("⚙️ Préférences d'interface mises à jour")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur sauvegarde option interface: {e}", category="ui_settings")

    def _on_dark_mode_changed(self):
        """Appelé quand le mode sombre change"""
        try:
            dark_mode = self.dark_mode_var.get()
            config_manager.set('dark_mode', dark_mode)
            
            # Changer le thème dans le ThemeManager
            new_theme = "sombre" if dark_mode else "clair"
            theme_manager.set_theme(new_theme)
            
            # Mettre à jour le style du notebook
            self._update_notebook_style()
            
            self._show_toast("🌙 Mode sombre " + ("activé" if dark_mode else "désactivé"))
            
        except Exception as e:
            log_message("ERREUR", f"Erreur changement mode sombre: {e}", category="ui_settings")
    
    def _update_notebook_style(self):
        """Met à jour le style du notebook avec les couleurs du thème actuel"""
        try:
            theme = theme_manager.get_theme()
            style = ttk.Style()
            
            # Style pour le notebook avec couleurs du thème
            style.configure("Custom.TNotebook", 
                        background=theme["bg"],
                        borderwidth=0)
            style.configure("Custom.TNotebook.Tab", 
                        background=theme["frame_bg"], 
                        foreground='#000000',
                        padding=[15, 6])
            style.map("Custom.TNotebook.Tab",
                    background=[('selected', theme["accent"])],
                    foreground=[('selected', '#000000')])
                    
        except Exception as e:
            log_message("ERREUR", f"Erreur mise à jour style notebook: {e}", category="ui_settings")

    def _on_debug_mode_changed(self):
        """Appelé quand le mode debug change"""
        try:
            debug_mode = self.debug_mode_var.get()
            config_manager.set('debug_mode', debug_mode)
            config_manager.set('debug_level', 5 if debug_mode else 3)  # ✅ AJOUT : Sauvegarder aussi le niveau
            config_manager.save_config()  # ✅ CORRECTION : Sauvegarder la config
            
            # Appliquer le changement au logger immédiatement
            try:
                from infrastructure.logging.logging import get_logger
                logger_instance = get_logger()
                if debug_mode:
                    logger_instance.set_debug(True, 5)
                else:
                    logger_instance.set_debug(False, 3)
            except Exception as logger_error:
                log_message("DEBUG", f"Impossible d'appliquer le mode debug au logger: {logger_error}", category="ui_settings")
            
            self._show_toast("🐛 Mode debug " + ("activé" if debug_mode else "désactivé"))
            log_message("INFO", f"Mode debug {'activé' if debug_mode else 'désactivé'} et sauvegardé", category="ui_settings")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur changement mode debug: {e}", category="ui_settings")

    def _on_editor_choice_changed(self, event=None):
        """Appelé quand le choix d'éditeur change"""
        try:
            editor_choice = self.editor_choice_var.get()
            config_manager.set('editor_choice', editor_choice)
            
            self._show_toast(f"📝 Éditeur configuré : {editor_choice}")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur changement éditeur: {e}", category="ui_settings")

    def _on_notification_mode_changed(self, event=None):
        """Appelé quand le mode de notification change"""
        try:
            notification_mode_display = self.notification_mode_var.get()
            notification_mapping = {
                "Statut seulement": "status_only",
                "Popups détaillés": "detailed_popups"
            }
            notification_mode_technical = notification_mapping.get(notification_mode_display, "status_only")
            config_manager.set('notification_mode', notification_mode_technical)
            
            self._show_toast(f"🔔 Mode notification : {notification_mode_display}")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur changement mode notification: {e}", category="ui_settings")

    def _on_save_mode_changed(self, event=None):
        """Appelé quand le mode de sauvegarde change"""
        try:
            save_mode_display = self.default_save_mode_var.get()
            save_mode_mapping = {
                "Écraser l'original": "overwrite",
                "Créer nouveau fichier": "new_file"
            }
            save_mode_technical = save_mode_mapping.get(save_mode_display, "overwrite")
            config_manager.set('default_save_mode', save_mode_technical)
            
            self._show_toast(f"💾 Mode sauvegarde : {save_mode_display}")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur changement mode sauvegarde: {e}", category="ui_settings")

    def _clean_temp_only(self):
        """Nettoie uniquement les fichiers temporaires"""
        try:
            from infrastructure.helpers.unified_functions import show_custom_askyesnocancel
            
            response = show_custom_askyesnocancel(
                "Nettoyer les fichiers temporaires",
                "Voulez-vous nettoyer tous les fichiers temporaires ?",
                parent=self.window
            )
            
            if response:
                # Logique de nettoyage des fichiers temporaires
                import tempfile
                import shutil
                
                temp_dir = tempfile.gettempdir()
                renpy_temp_files = [f for f in os.listdir(temp_dir) if 'renextract' in f.lower() or 'renpy' in f.lower()]
                
                cleaned_count = 0
                for file_name in renpy_temp_files:
                    try:
                        file_path = os.path.join(temp_dir, file_name)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            cleaned_count += 1
                    except Exception:
                        pass
                
                self._show_toast(f"🧹 {cleaned_count} fichiers temporaires nettoyés")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur nettoyage fichiers temporaires: {e}", category="ui_settings")

    def _reset_application(self):
        """Réinitialise complètement l'application"""
        try:
            from infrastructure.helpers.unified_functions import show_custom_askyesnocancel
            
            response = show_custom_askyesnocancel(
                "Réinitialiser l'application",
                "ATTENTION: Cette action va supprimer TOUS les paramètres, configurations et caches. Êtes-vous sûr ?",
                parent=self.window
            )
            
            if response:
                # Reset complet de la configuration
                config_manager.reset_all_settings()
                
                # Effacer le cache persistant des sauvegardes
                try:
                    from core.models.backup.unified_backup_manager import UnifiedBackupManager
                    backup_manager = UnifiedBackupManager()
                    backup_manager.clear_persistent_cache()
                    log_message("INFO", "Cache persistant des sauvegardes effacé", category="ui_settings")
                except Exception as cache_error:
                    log_message("ATTENTION", f"Erreur suppression cache: {cache_error}", category="ui_settings")
                
                # Détruire toutes les fenêtres cachées ET leurs états persistants
                try:
                    from ui.window_manager import get_window_manager
                    window_manager = get_window_manager()
                    window_manager.clear_all_windows()
                    window_manager.clear_persistent_states()
                    log_message("INFO", "Toutes les fenêtres et états persistants effacés", category="ui_settings")
                except Exception as window_error:
                    log_message("ATTENTION", f"Erreur suppression fenêtres: {window_error}", category="ui_settings")
                
                # Effacer le cache des scans de projets
                try:
                    from core.models.cache.project_scan_cache import get_project_cache
                    project_cache = get_project_cache()
                    project_cache.clear_persistent_cache()
                    log_message("INFO", "Cache persistant des scans de projets effacé", category="ui_settings")
                except Exception as cache_error:
                    log_message("ATTENTION", f"Erreur suppression cache projets: {cache_error}", category="ui_settings")
                
                # Fermer et rouvrir l'interface
                self.window.after(1000, lambda: self.parent_window.after(0, self.parent_window.destroy))
                self._show_toast("🔄 Application réinitialisée - Redémarrage en cours...")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur réinitialisation application: {e}", category="ui_settings")

    # === MÉTHODES POUR L'ONGLET COULEURS ===
    
    def _change_color(self, color_key):
        """Ouvre le sélecteur de couleur avec mise à jour du preset affiché"""
        try:
            from tkinter import colorchooser
            
            current_color = config_manager.get_theme_color(color_key)
            
            new_color = colorchooser.askcolor(
                color=current_color,
                title=f"Choisir la couleur pour {color_key}"
            )[1]
            
            if new_color:
                # Sauvegarder la nouvelle couleur
                config_manager.set_theme_color(color_key, new_color)
                
                # Mettre à jour le bouton dans l'interface
                if color_key in self.color_buttons:
                    self.color_buttons[color_key].configure(bg=new_color)
                
                # Mettre à jour l'affichage du preset
                if self.preset_var:
                    current_preset = config_manager.get_current_preset_name()
                    self.preset_var.set(current_preset)
                
                # Mettre à jour seulement les couleurs des boutons
                theme_manager.apply_to_all_cached_widgets()
                
                # Rafraîchir aussi la fenêtre des paramètres
                self.window.after(100, self._apply_theme_to_window)
                
                self._show_toast(f"Couleur mise à jour : {color_key}")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur changement couleur: {e}", category="ui_settings")

    def _reset_theme_colors(self):
        """Remet toutes les couleurs par défaut avec mise à jour du preset affiché"""
        try:
            confirmation_message = [
                ("CONFIRMATION REQUISE\n\n", "bold_red"),
                ("Voulez-vous vraiment ", "normal"),
                ("remettre toutes les couleurs par défaut", "bold"),
                (" ?\n\n", "normal"),
                ("Cette action est ", "yellow"),
                ("irréversible", "bold_red"),
                (" et supprimera toutes vos personnalisations.", "normal")
            ]
            
            response = show_custom_messagebox(
                'askyesno',
                'Remettre les couleurs par défaut',
                confirmation_message,
                theme_manager.get_theme(),
                yes_text="Oui, remettre par défaut",
                no_text="Non, conserver",
                parent=self.window,
                yes_width=25,
                no_width=25
            )
            
            if response:
                # Reset dans la config
                config_manager.reset_theme_colors_to_default()
                
                # Mettre à jour l'interface des paramètres
                current_colors = config_manager.get_theme_colors()
                for color_key, btn in self.color_buttons.items():
                    btn.configure(bg=current_colors.get(color_key, "#D3D3D3"))
                
                # Mettre à jour l'affichage du preset
                if self.preset_var:
                    current_preset = config_manager.get_current_preset_name()
                    self.preset_var.set(current_preset)
                
                # Mettre à jour seulement les couleurs des boutons
                theme_manager.apply_to_all_cached_widgets()
                
                # Rafraîchir aussi la fenêtre des paramètres
                self.window.after(100, self._apply_theme_to_window)
                
                self._show_toast("Couleurs remises par défaut")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur reset couleurs: {e}", category="ui_settings")

    def _on_preset_selected(self, event=None):
        """Appelé quand un preset est sélectionné"""
        pass  # Optionnel : preview du preset

    def _apply_selected_preset(self):
        """Applique le preset sélectionné avec rafraîchissement complet"""
        try:
            preset_name = self.preset_var.get()
            if preset_name and config_manager.apply_color_preset(preset_name):
                
                # Mettre à jour l'interface des paramètres
                current_colors = config_manager.get_theme_colors()
                for color_key, btn in self.color_buttons.items():
                    btn.configure(bg=current_colors.get(color_key, "#D3D3D3"))
                
                # Mettre à jour seulement les couleurs des boutons
                theme_manager.apply_to_all_cached_widgets()
                
                # Rafraîchir aussi la fenêtre des paramètres
                self.window.after(100, self._apply_theme_to_window)
                
                self._show_toast(f"Preset '{preset_name}' appliqué")
            else:
                self._show_toast("Erreur lors de l'application du preset", "error")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur application preset: {e}", category="ui_settings")


    def _show_coherence_quick_settings(self):
        """Affiche les paramètres rapides de cohérence"""
        try:
            self._create_simple_coherence_settings()
        except Exception as e:
            log_message("ERREUR", f"Erreur paramètres cohérence: {e}", category="ui_settings")
            self._show_toast("❌ Erreur ouverture paramètres cohérence", "error")
    
    def _create_simple_coherence_settings(self):
        """Crée une fenêtre simple de paramètres de cohérence"""
        try:
            from tkinter import Toplevel
            from ui.themes import theme_manager
            
            theme = theme_manager.get_theme()
            
            # Créer la fenêtre
            settings_window = Toplevel(self.window)
            settings_window.title("⚙️ Paramètres de cohérence")
            settings_window.geometry("700x550")
            settings_window.configure(bg=theme["bg"])
            settings_window.resizable(False, False)
            
            # Centrer la fenêtre
            settings_window.transient(self.window)
            settings_window.grab_set()
            
            # Titre
            title_label = tk.Label(
                settings_window,
                text="⚙️ Configuration des vérifications de cohérence",
                font=('Segoe UI', 14, 'bold'),
                bg=theme["bg"],
                fg=theme["accent"]
            )
            title_label.pack(pady=20)
            
            # Description
            desc_label = tk.Label(
                settings_window,
                text="Configurez les types de vérifications à effectuer lors de l'analyse de cohérence.",
                font=('Segoe UI', 10),
                bg=theme["bg"],
                fg=theme["fg"],
                wraplength=550,
                justify='center'
            )
            desc_label.pack(pady=(0, 10))
            
            # Note sur les contrôles obligatoires
            mandatory_note = tk.Label(
                settings_window,
                text="ℹ️ Certains contrôles critiques (Variables [], Balises {}, Séquences \\n, Structure old/new)\nsont toujours actifs pour garantir l'intégrité du jeu.",
                font=('Segoe UI', 9, 'italic'),
                bg=theme["bg"],
                fg=theme.get("fg_secondary", theme["fg"]),
                justify='center'
            )
            mandatory_note.pack(pady=(0, 20))
            
            # Container pour les options avec deux colonnes
            options_frame = tk.Frame(settings_window, bg=theme["bg"])
            options_frame.pack(fill='both', expand=True, padx=20)
            
            # Colonne gauche
            left_column = tk.Frame(options_frame, bg=theme["bg"])
            left_column.pack(side='left', fill='both', expand=True, padx=(0, 10))
            
            # Colonne droite
            right_column = tk.Frame(options_frame, bg=theme["bg"])
            right_column.pack(side='right', fill='both', expand=True, padx=(10, 0))
            
            # ✅ OPTIONS CONFIGURABLES (les 4 options obligatoires ont été retirées)
            # Retirées : coherence_check_variables, coherence_check_tags, coherence_check_escape_sequences, coherence_check_line_structure
            verification_options = [
                ("📝 Lignes non traduites", "coherence_check_untranslated"),
                ("🔖 Contenu balises non traduit ({b}text{/b})", "coherence_check_tags_content"),
                ("… Points de suspension", "coherence_check_ellipsis"),
                ("% Variables %", "coherence_check_percentages"),
                ("💬 Guillemets", "coherence_check_quotations"),
                ("() Parenthèses", "coherence_check_parentheses"),
                ("📐 Syntaxe Ren'Py", "coherence_check_syntax"),
                ("💬 DeepL ellipsis", "coherence_check_deepl_ellipsis"),
                ("% Pourcentage isolé", "coherence_check_isolated_percent"),
                ("📏 Différence de longueur", "coherence_check_length_difference")
            ]
            
            # Variables pour les checkboxes
            check_vars = {}
            
            # Répartir les options sur deux colonnes
            for i, (label_text, config_key) in enumerate(verification_options):
                var = tk.BooleanVar()
                check_vars[config_key] = var
                
                # Charger la valeur actuelle
                current_value = config_manager.get(config_key, True)
                var.set(current_value)
                
                # Alterner entre colonne gauche (pair) et droite (impair)
                target_column = left_column if i % 2 == 0 else right_column
                
                checkbox = tk.Checkbutton(
                    target_column,
                    text=label_text,
                    variable=var,
                    font=('Segoe UI', 10),
                    bg=theme["bg"],
                    fg=theme["fg"],
                    selectcolor=theme["bg"],
                    activebackground=theme["bg"],
                    activeforeground=theme["fg"],
                    anchor='w'
                )
                checkbox.pack(anchor='w', pady=5)
            
            # Boutons
            buttons_frame = tk.Frame(settings_window, bg=theme["bg"])
            buttons_frame.pack(fill='x', pady=20, padx=20)
            
            # Bouton Tout sélectionner
            select_all_btn = tk.Button(
                buttons_frame,
                text="✅ Tout sélectionner",
                command=lambda: [var.set(True) for var in check_vars.values()],
                bg=theme["button_primary_bg"],
                fg="#000000",
                font=('Segoe UI', 10, 'bold'),
                width=18
            )
            select_all_btn.pack(side='left', padx=(0, 10))
            
            # Bouton Tout désélectionner
            select_none_btn = tk.Button(
                buttons_frame,
                text="❌ Tout désélectionner",
                command=lambda: [var.set(False) for var in check_vars.values()],
                bg=theme["button_danger_bg"],
                fg="#000000",
                font=('Segoe UI', 10, 'bold'),
                width=18
            )
            select_none_btn.pack(side='left', padx=(0, 10))
            
            # Bouton Sauvegarder
            save_btn = tk.Button(
                buttons_frame,
                text="💾 Sauvegarder",
                command=lambda: self._save_coherence_settings(check_vars, settings_window),
                bg=theme["button_secondary_bg"],
                fg="#000000",
                font=('Segoe UI', 10, 'bold'),
                width=18
            )
            save_btn.pack(side='right')
                
        except Exception as e:
            log_message("ERREUR", f"Erreur création fenêtre cohérence: {e}", category="ui_settings")
            self._show_toast("❌ Erreur création fenêtre", "error")
    
    def _save_coherence_settings(self, check_vars, window):
        """Sauvegarde les paramètres de cohérence"""
        try:
            for config_key, var in check_vars.items():
                config_manager.set(config_key, var.get())
            
            self._show_toast("✅ Paramètres de cohérence sauvegardés", "success")
            window.destroy()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur sauvegarde cohérence: {e}", category="ui_settings")
            self._show_toast("❌ Erreur sauvegarde", "error")


def show_unified_settings(parent_window, app_controller=None):
    """Fonction principale pour afficher l'interface unifiée des paramètres"""
    try:
        interface = UnifiedSettingsInterface(parent_window, app_controller)
        return interface
        
    except Exception as e:
        log_message("ERREUR", f"Erreur création interface settings: {e}", category="settings")
        show_translated_messagebox(
            'showerror',
            'Erreur',
            f"Impossible d'ouvrir les paramètres :\n{str(e)}",
            parent=parent_window
        )
        return None
