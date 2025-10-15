# ui/interfaces/translation_generator_interface.py - INTERFACE UNIFIÉE COMPLÈTE
# Interface principale du générateur de traductions Ren'Py - AVEC 6 ONGLETS INTÉGRÉS

"""
Interface utilisateur principale pour le générateur de traductions Ren'Py
- Saisie intelligente du projet (comme coherence_checker_unified)
- Taille de fenêtre harmonisée (1200x900)
- 6 onglets intégrés : RPA → Génération → Extraction Config → Extraction Résultats → Nettoyage → Combinaison
- Orchestration complète des workflows
"""

import os
import threading
import tkinter as tk
from typing import Dict, Any, Optional, List
from core.services.translation.translation_generation_business import TranslationGenerationBusiness
from core.services.translation.rpa_extraction_business import RPAExtractionBusiness
from core.services.translation.combination_business import CombinationBusiness
from core.services.tools.realtime_editor_business import RealTimeEditorBusiness
from tkinter import ttk, filedialog
from ui.themes import theme_manager
from ui.notification_manager import NotificationManager
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import show_translated_messagebox, show_custom_askyesnocancel

# Imports des 5 onglets du générateur
from ui.tab_generator.extraction_rpa_tab import create_extraction_tab
from ui.tab_generator.generation_tl_tab import create_generation_tab_aligned
from ui.tab_generator.extraction_config_tab import create_extraction_config_tab
from ui.tab_generator.extraction_results_tab import create_extraction_results_tab
from ui.tab_generator.combination_tab import create_combination_tab

# Import du widget spinner
from ui.widgets.spinner import Spinner

# Support Drag & Drop si disponible
try:
    from tkinterdnd2 import DND_FILES
    HAS_DND = True
except ImportError:
    HAS_DND = False

class TranslationGeneratorInterface:
    """Interface utilisateur unifiée pour le générateur de traductions Ren'Py"""
    
    def __init__(self, parent_window):
        """Initialise l'interface unifiée"""
        self.parent_window = parent_window
        self.window = None
        self.rpa_business = None
        self.translation_business = None
        self.combination_business = None
        self.realtime_editor_business = None
        # Gérer le notification_manager
        try:
            if hasattr(parent_window, 'notification_manager'):
                self.notification_manager = parent_window.notification_manager
            else:
                self.notification_manager = NotificationManager(parent_window, None)
        except Exception as e:
            log_message("ATTENTION", f'Impossible de créer notification_manager: {e}', category="renpy_generator")
            self.notification_manager = None
        
        # État de l'interface
        self.current_project_path = None
        self.current_sdk_path = None
        self.is_operation_running = False
        
        # Initialiser TOUTES les variables dès le début
        self._init_all_variables()
        
        # Variables pour les onglets communs
        self.available_languages = []
        self.language_vars = {}
        self.lang_canvas = None
        self.lang_scrollable_frame = None
        self.lang_checkboxes_frame = None
        
        # Widgets de l'interface
        self.status_label = None
        self.notebook = None
        self.operation_buttons = []
        self.cancel_operation_btn = None
        
        self._create_interface()
        # Enregistrer dans le ProjectManager
        if hasattr(self.parent_window, 'app_controller'):
            app_controller = self.parent_window.app_controller
            if hasattr(app_controller, 'project_manager'):
                app_controller.project_manager.register_listener(
                    self._on_project_sync_changed,
                    source_name="renpy_generator"
                )
                log_message("DEBUG", "Générateur enregistré dans ProjectManager", category="project_sync")        
        log_message("INFO", "Interface TranslationGenerator unifiée initialisée", category="renpy_generator")
    
    def _init_all_variables(self):
        """Initialise toutes les variables tkinter nécessaires pour l'interface"""
        try:
            # === VARIABLES PRINCIPALES ===
            self.current_project_path = ""
            self.project_var = tk.StringVar(value="")
            self.status_var = tk.StringVar(value="Prêt")
            self.auto_open_var = tk.BooleanVar(value=config_manager.is_auto_open_enabled())
            self._updating_project = False
            
            # === VARIABLES ONGLET 1 : EXTRACTION/COMPILATION RPA ===
            self.delete_rpa_var = tk.BooleanVar(value=config_manager.get('renpy_delete_rpa_after', False))
            self.rpa_source_language_var = tk.StringVar(value="")
            self.rpa_translation_folder_var = tk.StringVar(value="")
            self.rpa_output_name_var = tk.StringVar(value="")
            self.rpa_archive_name_var = tk.StringVar(value="")
            self.delete_source_after_rpa_var = tk.BooleanVar(value=config_manager.get('renpy_delete_source_after_rpa', False))
            
            # === VARIABLES ONGLET 2 : GENERATION TL ===
            self.language_var = tk.StringVar(value=config_manager.get_renpy_default_language())
            self.language_selector_var = tk.BooleanVar(value=config_manager.is_language_selector_integration_enabled())
            self.developer_console_var = tk.BooleanVar(value=config_manager.is_developer_console_integration_enabled())
            self.add_common_var = tk.BooleanVar(value=config_manager.is_add_common_integration_enabled())
            self.add_screen_var = tk.BooleanVar(value=config_manager.is_add_screen_integration_enabled())
            self.fontsize_selector_var = tk.BooleanVar(value=config_manager.is_fontsize_selector_integration_enabled())
            
            # Variables polices GUI
            self.is_rtl_var = tk.BooleanVar(value=False)
            self.gui_override_vars = {
                'text_font': tk.BooleanVar(value=True),
                'name_text_font': tk.BooleanVar(value=False),
                'interface_text_font': tk.BooleanVar(value=False),
                'button_text_font': tk.BooleanVar(value=False),
                'choice_button_text_font': tk.BooleanVar(value=False)
            }
            self.individual_font_vars = {
                'text_font': tk.StringVar(),
                'name_text_font': tk.StringVar(),
                'interface_text_font': tk.StringVar(),
                'button_text_font': tk.StringVar(),
                'choice_button_text_font': tk.StringVar()
            }
            self.preview_font_var = tk.StringVar()
            self.preview_text_label = None
            
            # === VARIABLES ONGLET 3 : EXTRACTION CONFIG ===
            self.extraction_excluded_files_var = tk.StringVar(value="common.rpy, screens.rpy")
            self.extraction_available_languages = []
            self.extraction_language_vars = {}
            self.extraction_status_label = None
            self.extraction_analyze_btn = None
            
            # === VARIABLES ONGLET 4 : EXTRACTION RESULTS ===
            self.extraction_selections = {}
            self.extraction_buttons = {}
            self.extraction_files_stat_label = None
            self.extraction_existing_stat_label = None
            self.extraction_detected_stat_label = None
            self.extraction_mode_stat_label = None
            self.extraction_results_canvas = None
            self.extraction_results_scrollable_frame = None
            self.extraction_no_results_label = None
            self.extraction_generate_btn = None
            
            # === VARIABLES ONGLET 6 : COMBINAISON/DIVISION (maintenant 5e onglet) ===
            excluded_string = config_manager.get_renpy_excluded_files_as_string()
            self.unified_excluded_files_var = tk.StringVar(value=excluded_string)
            self.combine_source_var = tk.StringVar(value="")
            self.combine_output_var = tk.StringVar(value="")
            self.divide_source_var = tk.StringVar(value="")
            self.divide_output_var = tk.StringVar(value="")

            # SUPPRIMÉ: Variables onglets 5 (nettoyage) et 7 (éditeur temps réel)
            
            # === VARIABLES COMMUNES ===
            self.operation_buttons = []
            
            
        except Exception as e:
            log_message("ERREUR", f"Erreur initialisation variables: {e}", category="ui")
    
    def _create_interface(self):
        """Crée l'interface utilisateur unifiée"""
        # Fenêtre principale - parent_window est maintenant MainWindow, pas root
        parent_root = self.parent_window.root if hasattr(self.parent_window, 'root') else self.parent_window
        self.window = tk.Toplevel(parent_root)
        self.window.title("🎮 " + 'Générateur de Traductions Ren\'Py')
        self.window.geometry("1200x900")
        
        # Support Drag & Drop sur toute la fenêtre si disponible
        if HAS_DND:
            try:
                self.window.drop_target_register(DND_FILES)
                self.window.dnd_bind('<<Drop>>', self._on_window_drop)
            except Exception as e:
                log_message("DEBUG", f"Drag & Drop non disponible: {e}", category="renpy_generator")
        
        # Appliquer le thème à la fenêtre ET récupérer le thème
        theme = theme_manager.get_theme()
        self.window.configure(bg=theme["bg"])
        theme_manager.apply_to_widget(self.window)
        
        # Centrer la fenêtre et la mettre au premier plan
        self._center_window()
        self.window.lift()
        self.window.focus_force()
        
        # Créer l'interface
        self._create_header()
        self._create_main_content()
        self._create_footer()
        
        # Charger la configuration (maintenant que les variables existent)
        self._load_config()
        
        # Gestion de la fermeture
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def _create_header(self):
        """Crée l'en-tête avec saisie intelligente du projet"""
        theme = theme_manager.get_theme()
        
        # Frame d'en-tête
        header_frame = tk.Frame(self.window, bg=theme["bg"])
        header_frame.pack(fill='x', padx=20, pady=15)
        
        # Titre principal
        title_label = tk.Label(
            header_frame,
            text="🎮 " + 'Générateur de Traductions Ren\'Py Unifié',
            font=('Segoe UI Emoji', 16, 'bold'),
            bg=theme["bg"],
            fg=theme["accent"]
        )
        title_label.pack()
        
        # Sous-titre
        subtitle_label = tk.Label(
            header_frame,
            text="Workflow complet : RPA → Génération → Extraction → Nettoyage → Combinaison\n🎯 Glissez-déposez un dossier de projet n'importe où dans cette fenêtre !",
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Configuration principale
        config_frame = tk.Frame(header_frame, bg=theme["bg"])
        config_frame.pack(fill='x', pady=(20, 0))
        
        # Sélection du projet avec SAISIE INTELLIGENTE
        project_frame = tk.Frame(config_frame, bg=theme["bg"])
        project_frame.pack(fill='x', pady=5)
        
        tk.Label(project_frame, 
                text="🎮 " + 'Projet:',
                font=('Segoe UI', 10, 'bold'),
                bg=theme["bg"],
                fg=theme["fg"]).pack(side='left')
        
        # Entry avec événements intelligents
        self.project_entry = tk.Entry(
            project_frame, 
            textvariable=self.project_var, 
            font=('Segoe UI', 10), 
            width=70,
            bg=theme["entry_bg"],
            fg=theme["entry_fg"],
            insertbackground=theme["entry_fg"]
        )
        self.project_entry.pack(side='left', padx=(10, 5), fill='x', expand=True)
        
        # Événements pour saisie intelligente
        self.project_entry.bind('<KeyRelease>', self._on_project_path_changed)
        self.project_entry.bind('<FocusOut>', self._on_project_path_changed)
        
        project_btn = tk.Button(
            project_frame, 
            text="📁 Parcourir",
            command=self._select_project,
            bg=theme["button_nav_bg"],       # MODIFIÉ - Navigation Fichiers
            fg="#000000",                    # MODIFIÉ - Texte noir uniforme
            font=('Segoe UI', 9),
            pady=4,
            padx=8
        )
        project_btn.pack(side='right')
        
        # Info dynamique sur le projet
        self.project_info_label = tk.Label(
            config_frame,
            text="📊 Aucun projet sélectionné",
            font=('Segoe UI', 9, 'italic'),
            bg=theme["bg"],
            fg='#2980B9'
        )
        self.project_info_label.pack(anchor='w', pady=(5, 0))

    def _on_project_sync_changed(self, new_path: str):
        """Appelé quand le projet change depuis une autre interface (récepteur)"""
        try:
            if not new_path or new_path == self.current_project_path:
                return
            
            log_message("INFO", f"Générateur Ren'Py reçoit sync: {os.path.basename(new_path)}", category="project_sync")
            
            # Mettre à jour sans re-notifier pour éviter les boucles
            path = os.path.normpath(new_path.strip())
            self.current_project_path = path
            self.project_var.set(path)
            self._update_project_info(path)
            self._trigger_all_auto_scans()
            self._trigger_post_project_selection_actions()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur sync projet vers générateur: {e}", category="project_sync")

    # Modifier _set_current_project pour notifier le ProjectManager

    def _set_current_project(self, new_path: str):
        """Fonction centrale pour définir, valider et mettre à jour le projet"""
        try:
            path = os.path.normpath(new_path.strip())
            
            if not path or path == self.current_project_path:
                return

            if not self._validate_renpy_project(path):
                self.project_info_label.config(text="❌ Dossier invalide", fg='#ff8379')
                return

            if hasattr(self, 'handle_project_change'):
                self.handle_project_change()

            self.current_project_path = path
            self.project_var.set(path)
            self._update_project_info(path)

            # 🆕 NOUVEAU : Notifier le ProjectManager
            if hasattr(self, 'parent_window'):
                app_controller = getattr(self.parent_window, 'app_controller', None)
                if app_controller and hasattr(app_controller, 'project_manager'):
                    app_controller.project_manager.set_project(path, source="renpy_generator")

            self._trigger_all_auto_scans()
            self._trigger_post_project_selection_actions()

            config_manager.set('last_directory', os.path.dirname(path))
            config_manager.set('current_renpy_project', path)
            
            log_message("INFO", f"Projet changé avec succès : {os.path.basename(path)}", category="renpy_generator")

        except Exception as e:
            error_msg = f"Erreur lors de la définition du projet : {e}"
            self.project_info_label.config(text="❌ Erreur critique", fg='#ff8379')
            self._show_notification(error_msg, "error")
            log_message("ERREUR", error_msg, category="renpy_generator")

    def handle_project_change(self):
        """Vérifie et arrête les opérations en cours avant un changement de projet"""
        try:
            # Arrêter les opérations en cours si nécessaire
            if self.is_operation_running:
                log_message("INFO", "Changement de projet détecté : Arrêt des opérations en cours...", category="renpy_generator")
                
                # Annuler les opérations business
                if self.rpa_business:
                    self.rpa_business.cancel_operation()
                if self.translation_business:
                    self.translation_business.cancel_operation()
                if self.combination_business:
                    self.combination_business.cancel_operation()
                
                self._set_operation_running(False)
                
                # Notifier l'utilisateur
                self._show_notification(
                    "Opérations arrêtées en raison du changement de projet.",
                    "info"
                )
                
        except Exception as e:
            log_message("ERREUR", f"Erreur handle_project_change: {e}", category="renpy_generator")

    def _trigger_auto_scan_in_main_interface(self):
        """Déclenche un scan automatique dans l'interface principale à la fermeture"""
        try:
            if hasattr(self, 'parent_window') and self.parent_window:
                # Accéder à l'app_controller via parent_window
                app_controller = getattr(self.parent_window, 'app_controller', None)
                
                if app_controller and hasattr(app_controller, 'project_manager'):
                    project_path = app_controller.project_manager.get_current_project()
                    
                    if project_path:
                        log_message("INFO", "🔄 Déclenchement scan automatique dans l'interface principale", category="renpy_generator")
                        
                        # Utiliser un thread pour ne pas bloquer la fermeture
                        import threading
                        def auto_scan_thread():
                            try:
                                # Délai réduit pour laisser le temps à la fenêtre de se fermer
                                import time
                                time.sleep(0.2)
                                
                                # Déclencher le scan via ProjectLanguageSelector dans l'interface principale
                                scans_triggered = 0
                                
                                # Accéder au ProjectLanguageSelector via InfoFrame
                                if hasattr(self.parent_window, 'components'):
                                    components = self.parent_window.components
                                    if 'info' in components:
                                        info_frame = components['info']
                                        if hasattr(info_frame, 'project_selector'):
                                            project_selector = info_frame.project_selector
                                            
                                            try:
                                                # Déclencher le scan des langues
                                                if hasattr(project_selector, '_scan_languages'):
                                                    project_selector._scan_languages()
                                                    scans_triggered += 1
                                                
                                                # Déclencher le scan des fichiers
                                                if hasattr(project_selector, '_scan_files'):
                                                    project_selector._scan_files()
                                                    scans_triggered += 1
                                                
                                            except Exception as e:
                                                log_message("DEBUG", f"Erreur scan ProjectLanguageSelector: {e}", category="renpy_generator")
                                
                                log_message("INFO", f"✅ Scan automatique terminé - {scans_triggered} scans déclenchés", category="renpy_generator")
                                
                            except Exception as e:
                                log_message("DEBUG", f"Erreur scan automatique: {e}", category="renpy_generator")
                        
                        # Lancer le scan en arrière-plan
                        scan_thread = threading.Thread(target=auto_scan_thread, daemon=True)
                        scan_thread.start()
                        
        except Exception as e:
            log_message("DEBUG", f"Erreur déclenchement scan automatique: {e}", category="renpy_generator")

    def _trigger_all_auto_scans(self):
        """Déclenche tous les auto-scans des onglets après changement de projet"""
        try:
            # Délai progressif pour éviter les conflits
            
            # Onglet 1: Extraction RPA (100ms)
            if hasattr(self, '_auto_scan_extraction'):
                self.window.after(100, self._auto_scan_extraction)
            
            # Onglet 3: Extraction Config (200ms)  
            if hasattr(self, 'extraction_config_resync'):
                self.window.after(200, self.extraction_config_resync)
            
            
        except Exception as e:
            log_message("ERREUR", f"Erreur déclenchement auto-scans: {e}", category="auto_scan")

    def _trigger_post_project_selection_actions(self):
        """Déclenche toutes les mises à jour nécessaires dans les onglets après la sélection d'un projet."""
        try:
            # Onglet 3: Extraction Config - Rafraîchir les langues
            from ui.tab_generator.extraction_config_tab import detect_extraction_languages
            detect_extraction_languages(self)
        except Exception as e:
            log_message("DEBUG", f"Échec de la détection des langues pour l'extraction : {e}", category="renpy_generator")
            
        try:
            # Onglet 6: Combinaison - Remplissage automatique (silencieux)
            from ui.tab_generator.combination_tab import auto_fill_combination_fields
            auto_fill_combination_fields(self, silent=True)
        except Exception as e:
            log_message("DEBUG", f"Échec du remplissage automatique pour la combinaison : {e}", category="renpy_generator")

    def _on_project_path_changed(self, event=None):
        """Appelé lors de la saisie manuelle, appelle la fonction centrale."""
        path = self.project_var.get()
        if path and os.path.isdir(path): # On ne vérifie que si le dossier existe pour ne pas être trop agressif
            self._set_current_project(path)

    def _validate_renpy_project(self, project_path: str) -> bool:
        """Valide qu'un chemin est un projet Ren'Py valide"""
        try:
            if not os.path.isdir(project_path):
                return False
            
            # Vérifier la présence d'au moins un indicateur Ren'Py
            game_dir = os.path.join(project_path, "game")
            has_game_folder = os.path.isdir(game_dir)
            
            # Chercher des fichiers Ren'Py caractéristiques
            has_exe = any(f.endswith('.exe') for f in os.listdir(project_path) if os.path.isfile(os.path.join(project_path, f)))
            
            # Chercher des fichiers .rpy ou .rpyc
            has_rpy_files = False
            if has_game_folder:
                for root, dirs, files in os.walk(game_dir):
                    if any(f.endswith(('.rpy', '.rpyc', '.rpa')) for f in files):
                        has_rpy_files = True
                        break
                    # Limiter la recherche à 2 niveaux
                    if root.count(os.sep) - game_dir.count(os.sep) >= 2:
                        break
            
            return has_game_folder or has_exe or has_rpy_files
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur validation projet: {e}", category="renpy_generator")
            return False

    def _update_project_info(self, project_path: str):
        """Met à jour l'info sur le projet détecté"""
        try:
            project_name = os.path.basename(project_path)
            
            # Analyser rapidement le projet
            game_dir = os.path.join(project_path, "game")
            has_game = os.path.isdir(game_dir)
            
            # Compter les fichiers rapidement
            rpa_count = 0
            rpy_count = 0
            
            if has_game:
                for f in os.listdir(game_dir):
                    if f.endswith('.rpa'):
                        rpa_count += 1
                    elif f.endswith('.rpy'):
                        rpy_count += 1
            
            # Chercher des traductions existantes
            tl_dir = os.path.join(game_dir, "tl") if has_game else None
            tl_langs = []
            if tl_dir and os.path.isdir(tl_dir):
                tl_langs = [d for d in os.listdir(tl_dir) if os.path.isdir(os.path.join(tl_dir, d)) and d.lower() != 'none']
            
            # Construire le message d'info
            info_parts = [f"✅ Projet: {project_name}"]
            
            if rpa_count > 0:
                info_parts.append(f"{rpa_count} RPA")
            if rpy_count > 0:
                info_parts.append(f"{rpy_count} RPY")
            if tl_langs:
                info_parts.append(f"Traductions: {', '.join(tl_langs[:3])}")
                if len(tl_langs) > 3:
                    info_parts.append("...")
            
            info_text = " • ".join(info_parts)
            
            self.project_info_label.config(text=info_text, fg=theme_manager.get_theme()["fg"])
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur mise à jour info projet: {e}", category="renpy_generator")
            self.project_info_label.config(text="✅ Projet Ren'Py détecté", fg=theme_manager.get_theme()["fg"])

    def _get_rpa_business(self):
        """Obtient l'instance RPA business en initialisant si nécessaire"""
        if self.rpa_business is None:
            self.rpa_business = RPAExtractionBusiness()
            self.rpa_business.set_callbacks(
                progress_callback=self._on_progress_update,
                status_callback=self._on_status_update,
                completion_callback=self._on_operation_complete,
                error_callback=self._on_error
            )
        return self.rpa_business

    def _get_translation_business(self):
        """Obtient l'instance Translation business en initialisant si nécessaire"""
        if self.translation_business is None:
            self.translation_business = TranslationGenerationBusiness()
            self.translation_business.set_callbacks(
                progress_callback=self._on_progress_update,
                status_callback=self._on_status_update,
                completion_callback=self._on_operation_complete,
                error_callback=self._on_error
            )
        return self.translation_business

    def _get_combination_business(self):
        """Obtient l'instance Combination business en initialisant si nécessaire"""
        if self.combination_business is None:
            self.combination_business = CombinationBusiness()
            self.combination_business.set_callbacks(
                progress_callback=self._on_progress_update,
                status_callback=self._on_status_update,
                completion_callback=self._on_operation_complete,
                error_callback=self._on_error
            )
        return self.combination_business

    def _on_window_drop(self, event):
        """Gère le glisser-déposer et appelle la fonction centrale."""
        try:
            # Votre logique de parsing du chemin reste la même
            raw_data = event.data
            if raw_data.startswith('{') and raw_data.endswith('}'):
                dropped_path = raw_data.strip('{}')
            else:
                dropped_path = raw_data.split('\n')[0].strip()

            if dropped_path:
                self._set_current_project(dropped_path)
                
        except Exception as e:
            error_msg = f"Erreur lors du glisser-déposer : {e}"
            self.project_info_label.config(text="❌ Erreur Drag & Drop", fg='#ff8379')
            log_message("ERREUR", error_msg, category="renpy_generator")

    def _create_main_content(self):
        """Crée le contenu principal avec les 7 onglets"""
        theme = theme_manager.get_theme()
        
        # Frame principal
        main_frame = tk.Frame(self.window, bg=theme["bg"])
        main_frame.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        
        # Notebook pour les onglets
        style = ttk.Style()
        
        # Style pour le notebook avec onglets gris
        style.configure("Custom.TNotebook",
                    background=theme["bg"],
                    borderwidth=0)
        style.configure("Custom.TNotebook.Tab",
                    background='#6c757d',
                    foreground='#000000',
                    padding=[15, 6])
        style.map("Custom.TNotebook.Tab",
                background=[('selected', theme["accent"])],
                foreground=[('selected', '#000000')])
        
        # Styles uniformes pour les Combobox - APRÈS avoir créé style
        theme_manager.apply_uniform_combobox_style(style)
        
        self.notebook = ttk.Notebook(main_frame, style="Custom.TNotebook")
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        self.notebook.pack(fill='both', expand=True)
        
        # Créer les onglets dans l'ordre (avec gestion d'erreur pour chacun)
        try:
            create_extraction_tab(self.notebook, self)          # Onglet 1: RPA/RPYC
        except Exception as e:
            log_message("ERREUR", f"Erreur création onglet 1: {e}", category="ui")
        
        try:
            create_generation_tab_aligned(self.notebook, self)          # Onglet 2: Génération SDK
        except Exception as e:
            log_message("ERREUR", f"Erreur création onglet 2: {e}", category="ui")
        
        try:
            create_extraction_config_tab(self.notebook, self)   # Onglet 3: Config extraction
        except Exception as e:
            log_message("ERREUR", f"Erreur création onglet 3: {e}", category="ui")
        
        try:
            create_extraction_results_tab(self.notebook, self)  # Onglet 4: Résultats extraction
        except Exception as e:
            log_message("ERREUR", f"Erreur création onglet 4: {e}", category="ui")
        
        try:
            create_combination_tab(self.notebook, self)         # Onglet 5: Combinaison
        except Exception as e:
            log_message("ERREUR", f"Erreur création onglet 6: {e}", category="ui")
    
    def _create_footer(self):
        """Crée le pied de page simplifié"""
        theme = theme_manager.get_theme()
        
        # Frame de pied de page
        footer_frame = tk.Frame(self.window, bg=theme["bg"])
        footer_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        # Tout sur une seule ligne
        single_line_frame = tk.Frame(footer_frame, bg=theme["bg"])
        single_line_frame.pack(fill='x')

        # Label "État:" à gauche
        tk.Label(single_line_frame, 
                text='État:',
                font=('Segoe UI', 9, 'bold'),
                bg=theme["bg"],
                fg=theme["fg"]).pack(side='left')

        # Label de statut au centre
        self.status_label = tk.Label(
            single_line_frame,
            textvariable=self.status_var,
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"],
            anchor='w'
        )
        self.status_label.pack(side='left', padx=(10, 0), fill='x', expand=True)
        
        # Spinner animé (masqué par défaut)
        self.spinner = Spinner(single_line_frame, size=18, bg=theme["bg"])
        # Ne pas afficher par défaut, sera géré par _set_operation_running
        
        # Bouton Fermer tout à droite
        close_btn = tk.Button(
            single_line_frame,
            text="❌ Fermer",
            command=self._on_close,
            bg=theme["button_danger_bg"],   # MODIFIÉ - Négative/Danger
            fg="#000000",                    # MODIFIÉ - Texte noir uniforme
            font=('Segoe UI', 9),
            pady=4,
            padx=8
        )
        close_btn.pack(side='right')

        self.cancel_operation_btn = tk.Button(
            single_line_frame,
            text="ℹ️ Annuler l'opération",
            command=self._cancel_operation,
            bg=theme["button_tertiary_bg"], # MODIFIÉ - Tertiaire
            fg="#000000",                    # MODIFIÉ - Texte noir uniforme
            font=('Segoe UI', 9),
            pady=4,
            padx=8,
            state='disabled'
        )
        self.cancel_operation_btn.pack(side='right', padx=(0, 10))

    def _load_config(self):
        """Charge la configuration depuis config_manager - VERSION CORRIGÉE"""
        try:
            # Langue par défaut
            default_lang = config_manager.get_renpy_default_language()
            self.language_var.set(default_lang)
            
            # Auto-ouverture
            self.auto_open_var.set(config_manager.is_auto_open_enabled())

            # 🆕 PRIORITÉ : Charger le projet actuel du ProjectManager si disponible
            project_to_load = None
            if hasattr(self, 'parent_window'):
                app_controller = getattr(self.parent_window, 'app_controller', None)
                if app_controller and hasattr(app_controller, 'project_manager'):
                    current_project = app_controller.project_manager.get_current_project()
                    if current_project and os.path.exists(current_project):
                        project_to_load = current_project
                        log_message("INFO", f"Projet chargé depuis ProjectManager: {os.path.basename(current_project)}", category="renpy_generator")
            
            # Sinon, charger le projet précédent de la config
            if not project_to_load:
                last_project = config_manager.get('current_renpy_project', '')
                if last_project and os.path.exists(last_project):
                    project_to_load = last_project
            
            # Appliquer le projet trouvé
            if project_to_load:
                self.project_var.set(project_to_load)
                self.current_project_path = project_to_load
                self._update_project_info(project_to_load)
                self._trigger_all_auto_scans()
                self._trigger_post_project_selection_actions()

            # Variables manquantes - les créer si elles n'existent pas
            if not hasattr(self, 'excluded_files_var'):
                self.excluded_files_var = tk.StringVar()
                excluded_files = config_manager.get_renpy_excluded_files()
                self.excluded_files_var.set(", ".join(excluded_files))
            
            if not hasattr(self, 'show_results_popup_var'):
                self.show_results_popup_var = tk.BooleanVar(value=True)
                self.show_results_popup_var.set(config_manager.get('renpy_show_results_popup', True))
            
            # Suppression RPA
            if hasattr(self, 'delete_rpa_var'):
                self.delete_rpa_var.set(config_manager.get('renpy_delete_rpa_after', False))
            
            # Exclusions nettoyage
            if hasattr(self, 'cleanup_excluded_files_var'):
                cleanup_exclusions = config_manager.get('cleanup_excluded_files', 'common.rpy')
                self.cleanup_excluded_files_var.set(cleanup_exclusions)
            
            # Configuration extraction
            if hasattr(self, 'extraction_excluded_files_var'):
                extraction_exclusions = config_manager.get('extraction_excluded_files', 'common.rpy, screens.rpy')
                self.extraction_excluded_files_var.set(extraction_exclusions)
            
        except Exception as e:
            log_message("ERREUR", f"Erreur chargement configuration: {e}", category="renpy_generator")

    def _select_project(self):
        """Ouvre une boîte de dialogue pour sélectionner un projet et appelle la fonction centrale."""
        initial_dir = os.path.dirname(self.current_project_path or '') or config_manager.get('last_directory', os.path.expanduser('~'))
        
        project_path = filedialog.askdirectory(
            title='Sélectionner le dossier du projet Ren\'Py',
            initialdir=initial_dir
        )
        
        if project_path:
            self._set_current_project(project_path)

    def _on_tab_changed(self, event=None):
        """Callback quand l'utilisateur change d'onglet"""
        try:
            current_tab = self.notebook.tab(self.notebook.select(), "text")
            
            # Onglet Combinaison/Division
            if "Combinaison" in current_tab or "🔗" in current_tab:
                try:
                    from ui.tab_generator.combination_tab import auto_fill_combination_fields
                    auto_fill_combination_fields(self, silent=False)  # Logs activés dans l'onglet Combinaison
                except Exception:
                    pass
            
            # Onglet Extraction Config - rafraîchir les langues
            elif "Extraction - Config" in current_tab or "🔍" in current_tab:
                try:
                    from ui.tab_generator.extraction_config_tab import detect_extraction_languages
                    detect_extraction_languages(self)
                except Exception:
                    pass
                
        except Exception as e:
            log_message("ERREUR", f"Erreur _on_tab_changed: {e}", category="renpy_generator")

    def _cancel_operation(self):
        """Annule l'opération en cours"""
        try:
            if self.is_operation_running:
                # Annuler tous les modules business
                if self.rpa_business:
                    self.rpa_business.cancel_operation()
                
                if self.translation_business:
                    self.translation_business.cancel_operation()
                
                if self.combination_business:
                    self.combination_business.cancel_operation()
                
                self._update_status('Annulation en cours...')
        except Exception as e:
            log_message("ERREUR", f"Erreur annulation opération: {e}", category="renpy_generator")

    # =================================================================
    # MÉTHODES DE CALLBACKS ET ÉVÉNEMENTS - SIMPLIFIÉES
    # =================================================================
    
    def _on_progress_update(self, progress: int, message: str = ""):
        """Callback de mise à jour du progrès - SIMPLIFIÉ"""
        try:
            if message:
                self.window.after(0, lambda: self._update_status(message))
        except Exception as e:
            log_message("ERREUR", f"Erreur callback progress: {e}", category="renpy_generator")
    
    def _on_status_update(self, message: str):
        """Callback de mise à jour du statut"""
        try:
            self.window.after(0, lambda: self._update_status(message))
        except Exception as e:
            log_message("ERREUR", f"Erreur callback status: {e}", category="renpy_generator")
    
    def _update_status(self, message: str, status_type: str = "normal"):
        """Met à jour le statut - VERSION AVEC SUPPORT TYPE OPTIONNEL"""
        try:
            self.status_var.set(message)
            
            # Couleurs selon le type de message ou le paramètre status_type
            if status_type == "success" or any(word in message.lower() for word in ['terminé', 'succès', 'réussi', 'fini', 'complete']):
                self.status_label.config(fg='#28a745')  # Vert
            elif status_type == "error" or any(word in message.lower() for word in ['erreur', 'échec', 'failed', 'error']):
                self.status_label.config(fg='#ff8379')  # Rouge
            elif status_type == "info" or any(word in message.lower() for word in ['en cours', 'extraction', 'génération', 'nettoyage', 'préparation']):
                self.status_label.config(fg='#2196F3')  # Bleu
            else:
                self.status_label.config(fg=theme_manager.get_theme()["fg"])  # Normal
                
        except Exception as e:
            log_message("ERREUR", f"Erreur update_status: {e}", category="renpy_generator")
    
    def _on_operation_complete(self, success: bool, results: Dict[str, Any]):
        """Callback de fin d'opération"""
        try:
            self.window.after(0, lambda: self._handle_operation_complete_safe(success, results))
        except Exception as e:
            log_message("ERREUR", f"Erreur callback completion: {e}", category="renpy_generator")
    
    def _handle_operation_complete_safe(self, success: bool, results: Dict[str, Any]):
        """Gestion thread-safe de la fin d'opération avec notifications d'erreur détaillées"""
        try:
            self._set_operation_running(False)
            
            notification_mode = config_manager.get('notification_mode', 'status_only')
            
            # Détecter les erreurs
            has_errors = bool(
                results.get('errors') or 
                results.get('generation_errors') or 
                results.get('failed_files') or
                results.get('partial_errors')
            )
            
            # Détecter les warnings critiques (échecs déguisés)
            has_critical_warnings = False
            if results.get('warnings'):
                critical_keywords = ['non trouvé', 'non supportée', 'échec', 'erreur', 'impossible', 'failed', 'error', 'not found', 'not supported']
                for warning in results['warnings']:
                    if any(keyword in str(warning).lower() for keyword in critical_keywords):
                        has_critical_warnings = True
                        break
            
            has_problems = has_errors or has_critical_warnings
            
            if success:
                operation_type = self._detect_operation_type(results)
                
                # Afficher popup si mode détaillé OU si problèmes détectés
                if (notification_mode == 'detailed_popups') or has_problems:
                    self._show_detailed_results_popup(results)
                
                # Statut
                if has_problems:
                    self._update_status(f'⚠️ {operation_type} terminée avec problèmes', "warning")
                else:
                    self._update_status(f'✅ {operation_type} terminée avec succès', "success")
                
                # Auto-ouverture
                if hasattr(self, 'auto_open_var') and self.auto_open_var.get():
                    self._auto_open_results(results)
                
                # ✅ AJOUT : Invalider le cache des langues après génération
                self._invalidate_language_cache_after_generation(results)
                    
            else:
                self._handle_complete_failure(results)
        
        except Exception as e:
            log_message("ERREUR", f"Erreur handle_operation_complete_safe: {e}", category="renpy_generator")

    def _invalidate_language_cache_after_generation(self, results: Dict[str, Any]):
        """Invalide le cache des langues après génération de nouveaux fichiers"""
        try:
            log_message("DEBUG", f"Invalidation cache - Début avec résultats: {results}", category="renpy_generator")
            
            if not hasattr(self, 'current_project_path') or not self.current_project_path:
                log_message("DEBUG", "Pas de projet actuel pour invalidation cache", category="renpy_generator")
                return
            
            # Détecter quelle langue a été générée
            language = None
            
            # Méthode 1: Chercher dans les résultats
            if 'language' in results:
                language = results['language']
                log_message("DEBUG", f"Langue trouvée dans résultats: {language}", category="renpy_generator")
            elif 'generated_files' in results:
                # Extraire la langue du chemin des fichiers générés
                generated_files = results.get('generated_files', [])
                log_message("DEBUG", f"Fichiers générés: {generated_files}", category="renpy_generator")
                if generated_files:
                    # Le premier fichier devrait contenir le chemin vers la langue
                    first_file = generated_files[0] if isinstance(generated_files, list) else str(generated_files)
                    if 'tl/' in first_file:
                        parts = first_file.split('tl/')
                        if len(parts) > 1:
                            language = parts[1].split('/')[0]
                            log_message("DEBUG", f"Langue extraite du chemin: {language}", category="renpy_generator")
            
            # Méthode 2: Chercher dans le statut actuel
            if not language and hasattr(self, 'current_language'):
                language = self.current_language
                log_message("DEBUG", f"Langue trouvée dans statut actuel: {language}", category="renpy_generator")
            
            if language:
                # Invalider le cache pour cette langue
                from core.models.cache.project_scan_cache import get_project_cache
                cache = get_project_cache()
                cache.invalidate_language(self.current_project_path, language)
                
                log_message("INFO", f"Cache invalidé pour la langue '{language}' après génération", category="renpy_generator")
                
                # ✅ AJOUT : Notifier l'interface principale pour refresh
                self._notify_main_window_refresh()
                
                # ✅ AJOUT : Forcer l'invalidation complète du cache comme solution de contournement
                self._force_clear_all_cache()
            else:
                # Si on ne peut pas déterminer la langue, invalider tout le projet
                from core.models.cache.project_scan_cache import get_project_cache
                cache = get_project_cache()
                cache.invalidate_project(self.current_project_path)
                
                log_message("INFO", f"Cache invalidé pour tout le projet après génération", category="renpy_generator")
                
                # ✅ AJOUT : Notifier l'interface principale pour refresh
                self._notify_main_window_refresh()
                
                # ✅ AJOUT : Forcer l'invalidation complète du cache comme solution de contournement
                self._force_clear_all_cache()
                
        except Exception as e:
            log_message("ERREUR", f"Erreur invalidation cache après génération: {e}", category="renpy_generator")

    def _notify_main_window_refresh(self):
        """Notifie l'interface principale pour qu'elle refresh les langues"""
        try:
            # Méthode 1: Via l'app_controller si disponible
            if hasattr(self, 'app_controller') and self.app_controller:
                self.app_controller.force_refresh_project_languages()
                return
            
            # Méthode 2: Via une référence globale si disponible
            try:
                from main import app_instance
                if app_instance and hasattr(app_instance, 'controller'):
                    app_instance.controller.force_refresh_project_languages()
                    return
            except:
                pass
            
            log_message("INFO", "Notification de refresh envoyée à l'interface principale", category="renpy_generator")
            
        except Exception as e:
            log_message("ATTENTION", f"Impossible de notifier l'interface principale: {e}", category="renpy_generator")

    def _force_clear_all_cache(self):
        """Force l'invalidation complète du cache comme solution de contournement"""
        try:
            from core.models.cache.project_scan_cache import get_project_cache
            cache = get_project_cache()
            
            # Méthode 1: Invalider le projet actuel
            if hasattr(self, 'current_project_path') and self.current_project_path:
                cache.invalidate_project(self.current_project_path)
                log_message("INFO", f"Cache invalidé pour le projet: {self.current_project_path}", category="renpy_generator")
            
            # Méthode 2: Vider complètement le cache (solution radicale)
            cache.clear_cache()
            log_message("INFO", "Cache complètement vidé comme solution de contournement", category="renpy_generator")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur lors du vidage forcé du cache: {e}", category="renpy_generator")

    def _get_error_resolution_suggestions(self, errors: List[str], results: Dict[str, Any]) -> str:
        """Génère des suggestions de résolution basées sur les types d'erreurs"""
        try:
            suggestions = []
            error_text = " ".join(errors).lower()
            
            if "fichier introuvable" in error_text or "file not found" in error_text:
                suggestions.append("• Vérifiez que tous les fichiers source sont présents")
                suggestions.append("• Assurez-vous que le projet n'a pas été modifié pendant l'opération")
            
            if "permission" in error_text or "accès" in error_text:
                suggestions.append("• Fermez le jeu s'il est en cours d'exécution")
                suggestions.append("• Vérifiez les permissions du dossier")
                suggestions.append("• Exécutez en tant qu'administrateur si nécessaire")
            
            if "encoding" in error_text or "encodage" in error_text:
                suggestions.append("• Certains fichiers contiennent des caractères spéciaux")
                suggestions.append("• Essayez de régénérer les fichiers source")
            
            if "rpyc" in error_text or "decompile" in error_text:
                suggestions.append("• Utilisez la méthode alternative UnRen.bat")
                suggestions.append("• Certains fichiers peuvent être protégés")
            
            if not suggestions:
                operation_type = self._detect_operation_type(results).lower()
                suggestions.append("• Vérifiez les logs pour plus de détails")
                suggestions.append(f"• Essayez de relancer la {operation_type}")
                
                if "génération" in operation_type:
                    suggestions.append("• Vérifiez que le projet est correctement décompilé")
            
            return "\n".join(suggestions) if suggestions else ""
            
        except Exception as e:
            log_message("DEBUG", f"Erreur génération suggestions: {e}", category="renpy_generator")
            return ""

    def _get_status_suffix_for_errors(self, results: Dict[str, Any]) -> str:
        """Génère un suffixe pour le statut en cas d'erreurs partielles"""
        try:
            error_count = 0
            warning_count = 0
            
            if results.get('errors'):
                error_count += len(results['errors'])
            if results.get('failed_files'):
                error_count += len(results['failed_files'])
            if results.get('generation_errors'):
                error_count += len(results['generation_errors'])
            
            if results.get('warnings'):
                warning_count = len(results['warnings'])
            
            if error_count > 0:
                return f" avec {error_count} erreur{'s' if error_count > 1 else ''}"
            elif warning_count > 0:
                return f" avec {warning_count} avertissement{'s' if warning_count > 1 else ''}"
            
            return " avec succès"
            
        except Exception:
            return ""

    def _handle_complete_failure(self, results: Dict[str, Any]):
        """Gère les échecs complets d'opération"""
        try:
            self._update_status('❌ Opération échouée')
            
            operation_type = self._detect_operation_type(results)
            title = f"❌ Échec de la {operation_type.lower()}"
            
            # Collecter toutes les erreurs
            all_errors = []
            if results.get('errors'):
                all_errors.extend(results['errors'])
            if results.get('generation_errors'):
                all_errors.extend(results['generation_errors'])
            
            # Construire le message
            if all_errors:
                message = "L'opération a échoué pour les raisons suivantes:\n\n"
                displayed_errors = all_errors[:5]
                message += "\n".join([f"• {error}" for error in displayed_errors])
                
                if len(all_errors) > 5:
                    remaining = len(all_errors) - 5
                    message += f"\n\n... et {remaining} autre{'s' if remaining > 1 else ''} erreur{'s' if remaining > 1 else ''}"
            else:
                message = f"La {operation_type.lower()} a échoué pour une raison inconnue.\n\nConsultez les logs pour plus de détails."
            
            # Ajouter des suggestions
            suggestions = self._get_error_resolution_suggestions(all_errors, results)
            if suggestions:
                message += f"\n\n💡 Suggestions:\n{suggestions}"
            
            show_translated_messagebox(
                'error',
                title,
                message,
                parent=self.window
            )
            
        except Exception as e:
            log_message("ERREUR", f"Erreur handle_complete_failure: {e}", category="renpy_generator")
            self._show_notification('Opération échouée', "error")

    def _detect_operation_type(self, results: Dict[str, Any]) -> str:
        """Détecte le type d'opération à partir des résultats pour l'affichage de statut"""
        try:
            # Vérifier d'abord le summary (format le plus récent)
            summary = results.get('summary', {})
            if 'cleaning' in summary:
                return "Nettoyage"
            elif 'rpa' in summary:
                return "Décompilation"
            elif 'generation' in summary:
                return "Génération"
            elif 'combination' in summary:
                return "Combinaison"
            elif 'division' in summary:
                return "Division"
            
            # Fallback vers l'ancien format
            if 'rpa_extracted' in results or 'rpyc_converted' in results:
                return "Décompilation"
            elif 'translation_files' in results:
                return "Génération"
            elif 'files_combined' in results:
                return "Combinaison"
            elif 'divided_files' in results:
                return "Division"
            elif 'orphan_blocks_removed' in results:
                return "Nettoyage"
            else:
                return "Opération"
                
        except Exception as e:
            log_message("DEBUG", f"Erreur détection type opération: {e}", category="renpy_generator")
            return "Opération"
    
    def _on_error(self, error_message: str, exception: Exception = None):
        """Callback d'erreur"""
        try:
            self.window.after(0, lambda: self._handle_error_safe(error_message, exception))
        except Exception as e:
            log_message("ERREUR", f"Erreur callback error: {e}", category="renpy_generator")
    
    def _handle_error_safe(self, error_message: str, exception: Exception = None):
        """Gestion thread-safe des erreurs"""
        try:
            self._set_operation_running(False)
            self._update_status('Erreur')
            self._show_notification(f"Erreur: {error_message}", "error")
        except Exception as e:
            log_message("ERREUR", f"Erreur handle_error_safe: {e}", category="renpy_generator")

    # =================================================================
    # MÉTHODES DE GESTION DES RÉSULTATS ET POPUPS
    # =================================================================

    def _show_detailed_results_popup(self, results: Dict[str, Any]):
        """Affiche une popup avec les résultats détaillés"""
        try:
            # Déterminer le format du message
            if 'summary' in results and results['summary']:
                title, message = self._format_summary_results(results)
            else:
                # Fallback vers l'ancien système
                if 'rpa_extracted' in results or 'rpyc_converted' in results:
                    title = "Résultats de l'extraction"
                    message = self._format_extraction_results_improved(results)
                elif 'translation_files' in results:
                    title = "Résultats de la génération" 
                    message = self._format_generation_results_complete(results)
                elif 'files_combined' in results:
                    title = "Résultats de la combinaison"
                    message = self._format_combination_results(results)
                elif 'divided_files' in results:
                    title = "Résultats de la division"
                    message = self._format_division_results(results)
                else:
                    title = "Résultats de l'opération"
                    message = self._format_generic_results(results)
            
            # Déterminer le type selon les erreurs
            message_type = 'info'
            if results.get('errors') or results.get('generation_errors') or results.get('failed_files'):
                message_type = 'warning'
            
            show_translated_messagebox(message_type, title, message, parent=self.window)
            
        except Exception as e:
            log_message("ERREUR", f"Erreur affichage résultats: {e}", category="renpy_generator")

    def _format_generation_results_complete(self, results: Dict[str, Any]) -> str:
        """Formate les résultats de génération COMPLETS"""
        lines = []
        
        # En-tête
        if results.get('success', True):
            lines.append("✅ GÉNÉRATION de traductions terminée avec succès !")
        else:
            lines.append("❌ ÉCHEC de la génération de traductions")
        
        lines.append("")
        lines.append("📸 RÉSUMÉ DE LA GÉNÉRATION")
        lines.append("-" * 40)
        
        # Langue cible
        if results.get('language'):
            lines.append(f"🌍 Langue cible: {results['language']}")
        
        # Fichiers générés
        if results.get('translation_files'):
            file_count = len(results['translation_files'])
            lines.append(f"📄 {file_count} fichiers de traduction créés")
        
        # Dossier de sortie
        if results.get('output_folder'):
            lines.append(f"📂 Dossier: {results['output_folder']}")
        
        # Éléments supplémentaires créés
        additional_features = []
        
        if results.get('french_common_prepared'):
            additional_features.append("fichier common français")
        
        if results.get('font_applied'):
            font_summary = results.get('font_summary', 'polices GUI appliquées')
            additional_features.append(font_summary)
        
        if results.get('developer_console_created'):
            console_msg = results.get('developer_console_message', 'console développeur activée')
            additional_features.append(console_msg)
        
        if results.get('language_selector_created'):
            selector_msg = results.get('language_selector_message', 'sélecteur de langue intégré')
            additional_features.append(selector_msg)
        
        # Afficher les éléments supplémentaires
        if additional_features:
            lines.append("")
            lines.append("🎯 ÉLÉMENTS SUPPLÉMENTAIRES:")
            for feature in additional_features:
                lines.append(f"   • {feature}")
        
        # Temps d'exécution
        if results.get('execution_time'):
            lines.append("")
            lines.append(f"⏱️ Temps d'exécution: {results['execution_time']:.1f}s")
        
        # Avertissements
        if results.get('warnings'):
            lines.append("")
            lines.append("⚠️ AVERTISSEMENTS:")
            for warning in results['warnings']:
                lines.append(f"   • {warning}")
        
        # Erreurs de génération
        if results.get('generation_errors'):
            lines.append("")
            lines.append("❌ ERREURS DE GÉNÉRATION:")
            for error in results['generation_errors']:
                lines.append(f"   • {error}")
        
        # Erreurs générales
        if results.get('errors'):
            lines.append("")
            lines.append("❌ ERREURS:")
            for error in results['errors']:
                lines.append(f"   • {error}")
        
        # Fichiers échoués
        if results.get('failed_files'):
            lines.append("")
            lines.append("❌ FICHIERS ÉCHOUÉS:")
            for failed_file in results['failed_files']:
                if isinstance(failed_file, dict):
                    file_name = failed_file.get('path', 'Fichier inconnu')
                    reason = failed_file.get('reason', 'Raison inconnue')
                    lines.append(f"   • {file_name}: {reason}")
                else:
                    lines.append(f"   • {failed_file}")
        
        # Opération annulée
        if results.get('cancelled'):
            lines.append("")
            lines.append("ℹ️ Opération annulée par l'utilisateur")
        
        return "\n".join(lines)

    def _format_summary_results(self, results: Dict[str, Any]) -> tuple:
        """Formate les résultats basés sur le nouveau format summary - VERSION COMPLÈTE"""
        summary = results.get('summary', {})
        lines = []
        
        # Déterminer le titre selon le type d'opération
        if 'cleaning' in summary:
            title = "Résultats du nettoyage"
        elif 'rpa' in summary:
            title = "Résultats de la décompilation"
        elif 'generation' in summary:
            title = "Résultats de la génération"
        elif 'combination' in summary:
            title = "Résultats de la combinaison"
        elif 'division' in summary:
            title = "Résultats de la division"
        else:
            title = "Résultats de l'opération"
        
        # NETTOYAGE - Format rapport détaillé
        if 'cleaning' in summary:
            lines.append("RÉSUMÉ PAR MÉTHODE")
            lines.append("-" * 40)

            lint_blocks = results.get('summary', {}).get('lint_cleanup', {}).get('blocks_removed', 0)
            string_blocks = results.get('summary', {}).get('string_cleanup', {}).get('blocks_removed', 0)
            total_blocks = results.get('orphan_blocks_removed', 0)

            lines.append(f"Nettoyage par LINT: {lint_blocks} blocs")
            lines.append(f"Nettoyage par CORRESPONDANCE: {string_blocks} blocs") 
            lines.append(f"TOTAL: {total_blocks} blocs supprimés")          
        
        # DÉCOMPILATION - Format rapport détaillé AMÉLIORÉ
        elif 'rpa' in summary:
            lines.append("RÉSUMÉ DE LA DÉCOMPILATION")
            lines.append("-" * 40)
            lines.append(f"{summary['rpa']}")
            
            # Détails des archives RPA
            rpa_extracted = results.get('rpa_extracted', [])
            if rpa_extracted:
                lines.append(f"Archives RPA: {len(rpa_extracted)} extraites")
            
            total_files_extracted = results.get('total_files_extracted', 0)
            if total_files_extracted > 0:
                lines.append(f"Fichiers extraits: {total_files_extracted}")
            
            # Détails de la décompilation RPYC
            rpyc_converted = results.get('rpyc_converted', 0)
            rpyc_skipped = results.get('rpyc_skipped', 0)
            rpyc_failed = results.get('rpyc_failed', 0)
            
            if rpyc_converted > 0 or rpyc_skipped > 0 or rpyc_failed > 0:
                lines.append("")
                lines.append("DÉCOMPILATION RPYC:")
                lines.append(f"• Convertis: {rpyc_converted}")
                if rpyc_skipped > 0:
                    lines.append(f"• Ignorés (.rpy existe): {rpyc_skipped}")
                if rpyc_failed > 0:
                    lines.append(f"• Échecs: {rpyc_failed}")
            
            # Informations sur les tentatives unrpyc
            unrpyc_attempts = results.get('unrpyc_attempts', [])
            if len(unrpyc_attempts) > 1:
                lines.append("")
                lines.append("TENTATIVES UNRPYC:")
                for attempt in unrpyc_attempts:
                    version = attempt.get('version', 'unknown')
                    converted = attempt.get('converted', 0)
                    failed = attempt.get('failed', 0)
                    lines.append(f"• {version}: {converted} convertis, {failed} échecs")
            
            # Suppression des RPA (si activée)
            rpa_deleted_count = results.get('rpa_deleted_count', 0)
            if rpa_deleted_count > 0:
                lines.append(f"Archives RPA supprimées: {rpa_deleted_count}")
            
            # Lien vers méthode alternative si nécessaire
            if rpyc_failed > 0 and 'alternative_method_url' in summary:
                lines.append("")
                lines.append("→ Cliquez sur 'Méthode alternative' ci-dessous")
        
        # GÉNÉRATION - Format rapport détaillé COMPLET
        elif 'generation' in summary:
            lines.append("RÉSUMÉ DE LA GÉNÉRATION")
            lines.append("-" * 40)
            lines.append(f"{summary['generation']}")
            
            if results.get('translation_files'):
                lines.append(f"{len(results['translation_files'])} fichiers créés")
            if results.get('language'):
                lines.append(f"Langue: {results['language']}")
            
            # ÉLÉMENTS SUPPLÉMENTAIRES DÉTAILLÉS
            additional_features = []
            
            if results.get('french_common_prepared'):
                common_msg = results.get('french_common_message', 'fichier common français préparé')
                additional_features.append(common_msg)
            
            if results.get('font_applied'):
                font_summary = results.get('font_summary', 'polices GUI appliquées')
                additional_features.append(font_summary)
            
            if results.get('developer_console_created'):
                console_msg = results.get('developer_console_message', 'console développeur activée')
                additional_features.append(console_msg)
            
            if results.get('language_selector_created'):
                selector_msg = results.get('language_selector_message', 'sélecteur de langue intégré')
                additional_features.append(selector_msg)
            
            # Afficher les éléments supplémentaires
            if additional_features:
                lines.append("")
                lines.append("ÉLÉMENTS SUPPLÉMENTAIRES:")
                for feature in additional_features:
                    lines.append(f"• {feature}")
        
        # COMBINAISON - Format rapport détaillé
        elif 'combination' in summary:
            lines.append("RÉSUMÉ DE LA COMBINAISON")
            lines.append("-" * 40)
            lines.append(f"{summary['combination']}")
            
            if results.get('files_combined'):
                lines.append(f"{len(results['files_combined'])} fichiers combinés")
            if results.get('combined_file'):
                lines.append(f"Fichier: {os.path.basename(results['combined_file'])}")
        
        # DIVISION - Format rapport détaillé
        elif 'division' in summary:
            lines.append("RÉSUMÉ DE LA DIVISION")
            lines.append("-" * 40)
            lines.append(f"{summary['division']}")
            
            if results.get('divided_files'):
                lines.append(f"{len(results['divided_files'])} fichiers créés")
            if results.get('source_file'):
                lines.append(f"Source: {os.path.basename(results['source_file'])}")
        
        # Temps d'exécution (COMMUN À TOUS)
        lines.append("")
        if 'execution_time' in summary:
            lines.append(f"{summary['execution_time']}")
        elif results.get('execution_time'):
            lines.append(f"Temps d'exécution: {results['execution_time']:.1f}s")
        
        # Dossier de sortie (SI PERTINENT)
        if 'output_folder' in summary:
            lines.append(f"Dossier: {summary['output_folder']}")
        
        # Rapport détaillé (SI DISPONIBLE)
        if 'report_path' in summary and summary['report_path']:
            lines.append("")
            lines.append("Rapport détaillé créé")
            lines.append(f"   → {os.path.basename(summary['report_path'])}")
        
        # Erreurs et avertissements (COMMUN À TOUS)
        if results.get('errors'):
            lines.append("")
            lines.append("Erreurs rencontrées:")
            for error in results['errors']:
                lines.append(f"   • {error}")
        
        if results.get('warnings'):
            lines.append("")
            lines.append("Avertissements:")
            for warning in results['warnings']:
                lines.append(f"   • {warning}")
        
        return title, "\n".join(lines)

    def _format_extraction_results_improved(self, results: Dict[str, Any]) -> str:
        """Formate les résultats d'extraction avec le nouveau format amélioré"""
        lines = []
        
        lines.append("✅ Décompilation terminée avec succès !")
        lines.append("")
        
        # Résultats RPA
        rpa_count = len(results.get('rpa_extracted', []))
        total_extracted = results.get('total_files_extracted', 0)
        if rpa_count > 0:
            lines.append(f"📦 {rpa_count} fichiers RPA traités → {total_extracted} fichiers extraits")
            
            # RPA supprimés
            rpa_deleted = results.get('rpa_deleted_count', 0)
            if rpa_deleted > 0:
                lines.append(f"🗑️ {rpa_deleted} fichiers RPA supprimés")
        
        # Résultats RPYC
        rpyc_converted = results.get('rpyc_converted', 0)
        rpyc_skipped = results.get('rpyc_skipped', 0)
        rpyc_failed = results.get('rpyc_failed', 0)
        
        if rpyc_converted > 0 or rpyc_skipped > 0 or rpyc_failed > 0:
            lines.append("")
            rpyc_text = f"🔧 {rpyc_converted} fichiers .rpyc convertis"
            if rpyc_skipped > 0:
                rpyc_text += f", {rpyc_skipped} ignorés (fichier .rpy existant)"
            lines.append(rpyc_text)
            
            if rpyc_failed > 0:
                lines.append(f"⚠️ {rpyc_failed} échecs de conversion")
                lines.append("   → Utilisez la méthode alternative UnRen.bat")
        
        # Temps d'exécution
        if results.get('execution_time'):
            lines.append("")
            lines.append(f"⏱️ Temps d'exécution: {results['execution_time']:.1f}s")
        
        # Erreurs et avertissements
        if results.get('warnings'):
            lines.append("")
            lines.append("⚠️ Avertissements:")
            for warning in results['warnings']:
                lines.append(f"   • {warning}")
        
        if results.get('errors'):
            lines.append("")
            lines.append("❌ Erreurs:")
            for error in results['errors']:
                lines.append(f"   • {error}")
        
        return "\n".join(lines)

    def _format_generation_results_improved(self, results: Dict[str, Any]) -> str:
        """Formate les résultats de génération avec le nouveau format amélioré"""
        lines = []
        
        # En-tête
        if results.get('success', True):
            lines.append("✅ Génération de traductions terminée avec succès !")
        else:
            lines.append("❌ Échec de la génération de traductions")
        
        lines.append("")
        
        # Langue cible
        if results.get('language'):
            lines.append(f"🌍 Langue cible: {results['language']}")
        
        # Fichiers générés
        if results.get('translation_files'):
            file_count = len(results['translation_files'])
            lines.append(f"📝 {file_count} fichiers de traduction créés")
        
        # Dossier de sortie
        if results.get('output_folder'):
            lines.append(f"📁 Dossier: {results['output_folder']}")
        
        # Temps d'exécution
        if results.get('execution_time'):
            lines.append("")
            lines.append(f"⏱️ Temps d'exécution: {results['execution_time']:.1f}s")
        
        # Erreurs et avertissements
        if results.get('warnings'):
            lines.append("")
            lines.append("⚠️ Avertissements:")
            for warning in results['warnings']:
                lines.append(f"   • {warning}")
        
        if results.get('errors'):
            lines.append("")
            lines.append("❌ Erreurs:")
            for error in results['errors']:
                lines.append(f"   • {error}")
        
        return "\n".join(lines)

    def _format_combination_results(self, results: Dict[str, Any]) -> str:
        """Formate les résultats de combinaison pour l'affichage"""
        text = "✅ " + 'Combinaison de fichiers terminée' + "\n\n"
        
        if results.get('combined_file'):
            text += 'Fichier créé: {filename}'.format(filename=os.path.basename(results['combined_file'])) + "\n"
            text += 'Chemin: {path}'.format(path=results['combined_file']) + "\n\n"
        
        if results.get('files_combined'):
            text += 'Fichiers combinés: {count}'.format(count=len(results['files_combined'])) + "\n"
            for file_path in results['files_combined']:
                text += f"  • {os.path.basename(file_path)}\n"
            text += "\n"
        
        if results.get('files_excluded'):
            text += 'Fichiers exclus: {count}'.format(count=len(results['files_excluded'])) + "\n"
            for file_path in results['files_excluded']:
                text += f"  • {os.path.basename(file_path)}\n"
            text += "\n"
        
        if results.get('warnings'):
            text += 'Avertissements:' + "\n"
            for warning in results['warnings']:
                text += f"  • {warning}\n"
            text += "\n"
        
        if results.get('errors'):
            text += 'Erreurs:' + "\n"
            for error in results['errors']:
                text += f"  • {error}\n"
        
        return text

    def _format_division_results(self, results: Dict[str, Any]) -> str:
        """Formate les résultats de division pour l'affichage"""
        text = "✅ " + 'Division de fichier terminée' + "\n\n"
        
        if results.get('source_file'):
            text += 'Fichier source: {filename}'.format(filename=os.path.basename(results['source_file'])) + "\n\n"
        
        if results.get('divided_files'):
            text += 'Fichiers créés: {count}'.format(count=len(results['divided_files'])) + "\n"
            for file_path in results['divided_files']:
                text += f"  • {os.path.basename(file_path)}\n"
            text += "\n"
        
        if results.get('output_folder'):
            text += 'Dossier de sortie: {folder}'.format(folder=results['output_folder']) + "\n\n"
        
        if results.get('warnings'):
            text += 'Avertissements:' + "\n"
            for warning in results['warnings']:
                text += f"  • {warning}\n"
            text += "\n"
        
        if results.get('errors'):
            text += 'Erreurs:' + "\n"
            for error in results['errors']:
                text += f"  • {error}\n"
        
        return text

    def _format_generic_results(self, results: Dict[str, Any]) -> str:
        """Formate des résultats génériques quand le type n'est pas reconnu"""
        lines = []
        
        if results.get('success', False):
            lines.append("✅ Opération terminée avec succès !")
        else:
            lines.append("❌ L'opération a échoué")
        
        lines.append("")
        
        # Temps d'exécution
        if results.get('execution_time'):
            lines.append(f"⏱️ Temps d'exécution: {results['execution_time']:.1f}s")
        
        # Erreurs et avertissements
        if results.get('warnings'):
            lines.append("")
            lines.append("⚠️ Avertissements:")
            for warning in results['warnings']:
                lines.append(f"   • {warning}")
        
        if results.get('errors'):
            lines.append("")
            lines.append("❌ Erreurs:")
            for error in results['errors']:
                lines.append(f"   • {error}")
        
        # Opération annulée
        if results.get('cancelled'):
            lines.append("")
            lines.append("ℹ️ Opération annulée par l'utilisateur")
        
        return "\n".join(lines)

    def _open_report(self, report_path: str):
        """Ouvre le rapport de nettoyage"""
        try:
            if os.path.exists(report_path):
                import subprocess
                import platform
                if platform.system() == "Windows":
                    os.startfile(report_path)
                elif platform.system() == "Darwin":
                    subprocess.run(["open", report_path])
                else:
                    subprocess.run(["xdg-open", report_path])
                log_message("INFO", f"Rapport ouvert: {os.path.basename(report_path)}", category="renpy_generator")
            else:
                self._show_notification("Le rapport n'existe plus.", "warning")
        except Exception as e:
            log_message("ERREUR", f"Erreur ouverture rapport: {e}", category="renpy_generator")
            self._show_notification(f"Impossible d'ouvrir le rapport: {e}", "error")

    def _open_alternative_method(self, url: str):
        """Ouvre l'URL de la méthode alternative dans le navigateur"""
        try:
            import webbrowser
            webbrowser.open(url)
            log_message("INFO", f"Ouverture de la méthode alternative: {url}", category="renpy_generator")
        except Exception as e:
            log_message("ERREUR", f"Erreur ouverture URL: {e}", category="renpy_generator")

    def _auto_open_results(self, results: Dict[str, Any]):
        """Ouvre automatiquement les dossiers de résultats"""
        try:
            log_message("DEBUG", "Début auto_open_results", category="renpy_generator")
            
            folders_to_open = []
            
            # Extraction: ouvrir le dossier du projet
            if results.get('rpa_extracted') or results.get('rpyc_converted', 0) > 0:
                if self.current_project_path:
                    game_folder = os.path.join(self.current_project_path, "game")
                    if os.path.exists(game_folder):
                        folders_to_open.append(game_folder)
                    else:
                        folders_to_open.append(self.current_project_path)
            
            # Génération: ouvrir le dossier tl
            if results.get('output_folder'):
                folders_to_open.append(results['output_folder'])
            
            # Combinaison: ouvrir le dossier du fichier combiné
            if results.get('combined_file'):
                folders_to_open.append(os.path.dirname(results['combined_file']))
            
            # Division: ouvrir le dossier de sortie
            if results.get('divided_files') and results['divided_files']:
                folders_to_open.append(os.path.dirname(results['divided_files'][0]))
            
            # Ouvrir les dossiers (sans doublons)
            opened_folders = set()
            for folder in folders_to_open:
                if folder and folder not in opened_folders:
                    log_message("DEBUG", f"Ouverture dossier: {os.path.basename(folder)}", category="renpy_generator")
                    self._open_folder(folder)
                    opened_folders.add(folder)
            
            if not folders_to_open:
                log_message("DEBUG", "Aucun dossier à ouvrir", category="renpy_generator")
                        
        except Exception as e:
            log_message("ERREUR", f"Erreur auto_open_results: {e}", category="renpy_generator")
    
    def _open_folder(self, folder_path: str):
        """Ouvre un dossier avec l'explorateur système"""
        try:
            import subprocess
            import sys
            
            if os.name == 'nt':  # Windows
                os.startfile(folder_path)
                log_message("DEBUG", f"Dossier ouvert (Windows): {os.path.basename(folder_path)}", category="renpy_generator")
            elif sys.platform == 'darwin':  # macOS
                subprocess.call(['open', folder_path])
                log_message("DEBUG", f"Dossier ouvert (macOS): {os.path.basename(folder_path)}", category="renpy_generator")
            else:  # Linux
                subprocess.call(['xdg-open', folder_path])
                log_message("DEBUG", f"Dossier ouvert (Linux): {os.path.basename(folder_path)}", category="renpy_generator")
                    
        except Exception as e:
            log_message("ATTENTION", f"Impossible d'ouvrir le dossier {os.path.basename(folder_path)}: {e}", category="renpy_generator")

    # =================================================================
    # MÉTHODES UTILITAIRES
    # =================================================================

    def _set_operation_running(self, running: bool):
        """Définit l'état d'opération en cours"""
        self.is_operation_running = running
        
        # Activer/désactiver les boutons d'opération
        state = 'disabled' if running else 'normal'
        for button in self.operation_buttons:
            button.config(state=state)
        
        # Bouton d'annulation
        if hasattr(self, 'cancel_operation_btn'):
            self.cancel_operation_btn.config(state='normal' if running else 'disabled')
        
        # Gestion du spinner
        if hasattr(self, 'spinner'):
            if running:
                # Afficher et démarrer le spinner
                self.spinner.pack(side='right', padx=(0, 10))
                self.spinner.start()
            else:
                # Arrêter et masquer le spinner
                self.spinner.stop()
                self.spinner.pack_forget()
        
        # Plus de gestion de barre de progression
        if not running:
            self._update_status("Prêt")
    
    def _show_notification(self, message: str, toast_type: str = "info"):
        """Affiche une notification"""
        try:
            # Essayer d'utiliser le NotificationManager du parent
            if hasattr(self.parent_window, 'notification_manager'):
                notification_manager = self.parent_window.notification_manager
                if toast_type == "success":
                    notification_manager.show_success(message)
                elif toast_type == "warning":
                    notification_manager.show_warning(message)
                elif toast_type == "error":
                    notification_manager.show_error(message)
                else:
                    notification_manager.show_info(message)
            else:
                # Fallback vers messagebox
                import tkinter.messagebox as messagebox
                if toast_type == "error":
                    show_translated_messagebox('error', 'Erreur', message)
                elif toast_type == "warning":
                    show_translated_messagebox('warning', 'Avertissement', message)
                else:
                    show_translated_messagebox('info', 'Information', message)
                    
        except Exception as e:
            log_message("ERREUR", f"Erreur show_notification: {e}", category="renpy_generator")
    
    def _on_close(self):
        """Gestion de la fermeture de la fenêtre"""
        try:
            
            # Annuler les opérations en cours
            if self.is_operation_running:
                confirm = show_translated_messagebox(
                    'askyesno', 
                    'Fermeture', 
                    'Une opération est en cours.\nVoulez-vous vraiment fermer ?', 
                    parent=self.window
                )

                if not confirm:
                    return
                
                # Annuler toutes les opérations
                if self.rpa_business:
                    self.rpa_business.cancel_operation()
                if self.translation_business:
                    self.translation_business.cancel_operation()
                if self.combination_business:
                    self.combination_business.cancel_operation()
            # Dans _on_close, désenregistrer AVANT le transfer

            # Désenregistrer du ProjectManager
            if hasattr(self, 'parent_window'):
                app_controller = getattr(self.parent_window, 'app_controller', None)
                if app_controller and hasattr(app_controller, 'project_manager'):
                    app_controller.project_manager.unregister_listener("renpy_generator")
                    log_message("DEBUG", "Générateur désenregistré du ProjectManager", category="project_sync")

            # Sauvegarder les paramètres (SUPPRIMER variables onglets 5 et 7)
            try:
                # Langue par défaut
                config_manager.set_renpy_default_language(self.language_var.get())
                
                # Fichiers exclus si la variable existe
                if hasattr(self, 'excluded_files_var'):
                    excluded_text = self.excluded_files_var.get().strip()
                    if excluded_text:
                        excluded_list = [item.strip() for item in excluded_text.split(',') if item.strip()]
                        config_manager.set_renpy_excluded_files(excluded_list)
                
                # Auto-ouverture si activée
                if hasattr(self, 'auto_open_var'):
                    config_manager.set_renpy_auto_open_folder(self.auto_open_var.get())

                # Suppression RPA
                if hasattr(self, 'delete_rpa_var'):
                    config_manager.set('renpy_delete_rpa_after', self.delete_rpa_var.get())

                # Suppression du dossier source après RPA
                if hasattr(self, 'delete_source_after_rpa_var'):
                    config_manager.set('renpy_delete_source_after_rpa', self.delete_source_after_rpa_var.get())

                # Configuration extraction
                if hasattr(self, 'extraction_excluded_files_var'):
                    config_manager.set('extraction_excluded_files', self.extraction_excluded_files_var.get())

                # SUPPRIMÉ: Sauvegarde paramètres onglets 5 et 7

                # Sauvegarder le projet actuel dans la config
                if self.current_project_path:
                    config_manager.set('current_renpy_project', self.current_project_path)

                log_message("INFO", "Paramètres sauvegardés à la fermeture (interface unifiée)", category="renpy_generator")
                
            except Exception as e:
                log_message("ERREUR", f"Erreur sauvegarde à la fermeture: {e}", category="renpy_generator")
            
            if self.rpa_business:
                self.rpa_business.cleanup()
            if self.translation_business:
                self.translation_business.cleanup()
            if self.combination_business:
                self.combination_business.cleanup()
                
            # ✅ NOUVEAU : Déclencher un scan automatique dans l'interface principale
            self._trigger_auto_scan_in_main_interface()
            
            # Détruire la fenêtre
            self.window.destroy()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur fermeture interface: {e}", category="renpy_generator")


    def _get_realtime_editor_business(self):
        """Obtient l'instance RealTime Editor business en initialisant si nécessaire"""
        if not hasattr(self, 'realtime_editor_business') or self.realtime_editor_business is None:
            from core.services.tools.realtime_editor_business import RealTimeEditorBusiness
            self.realtime_editor_business = RealTimeEditorBusiness()
            self.realtime_editor_business.set_callbacks(
                status_callback=self._update_status,
                error_callback=self._on_error
            )
        return self.realtime_editor_business



def show_translation_generator(parent_window):
    """Fonction principale pour afficher le générateur de traductions unifié"""
    try:
        interface = TranslationGeneratorInterface(parent_window)
        log_message("INFO", "Générateur de traductions Ren'Py unifié lancé", category="renpy_generator")
        return interface
        
    except Exception as e:
        log_message("ERREUR", f"Erreur lancement générateur unifié: {e}", category="renpy_generator")
        
        # Fallback avec messagebox
        try:
            import tkinter.messagebox as messagebox
            show_translated_messagebox(
                "error",
                "Erreur",
                f"Impossible de lancer le générateur de traductions Ren'Py:\n\n{e}"
            )
        except Exception:
            pass
        
        return None

# Export des symboles publics
__all__ = ['TranslationGeneratorInterface', 'show_translation_generator']