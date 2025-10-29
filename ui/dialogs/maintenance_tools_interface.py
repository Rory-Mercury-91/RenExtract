# ui/interfaces/maintenance_tools_interface.py - INTERFACE OUTILS DE MAINTENANCE
# Interface dédiée aux outils de maintenance et analyse
# Created for RenExtract 

"""
Interface utilisateur pour les outils de maintenance Ren'Py
- Onglet 1: Nettoyage TL (migré depuis translation_generator)
- Onglet 2: Éditeur Temps Réel (migré depuis translation_generator)
- Onglet 3: Vérification Cohérence (migré depuis coherence_checker_unified)
- Système de projet bidirectionnel avec l'interface principale
"""

import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog
from typing import Dict, Any, Optional, List

from core.services.tools.realtime_editor_business import RealTimeEditorBusiness
from ui.themes import theme_manager
from ui.notification_manager import NotificationManager
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import show_translated_messagebox, show_custom_askyesnocancel
from ui.widgets.spinner import Spinner

# Support Drag & Drop si disponible
try:
    from tkinterdnd2 import DND_FILES
    HAS_DND = True
except ImportError:
    HAS_DND = False

class MaintenanceToolsInterface:
    """Interface utilisateur unifiée pour les outils de maintenance Ren'Py"""
    
    def __init__(self, parent_window):
        """Initialise l'interface de maintenance"""
        self.parent_window = parent_window
        self.window = None
        self.realtime_editor_business = None
        
        # Gestionnaire de notifications
        try:
            if hasattr(parent_window, 'notification_manager'):
                self.notification_manager = parent_window.notification_manager
            else:
                self.notification_manager = NotificationManager(parent_window, None)
        except Exception as e:
            log_message("ATTENTION", f'Impossible de créer notification_manager: {e}', category="maintenance_tools")
            self.notification_manager = None
        
        # État de l'interface
        self.current_project_path = None
        self.is_operation_running = False
        self._is_updating_from_sync = False  # Protection contre les boucles de synchronisation
        self.project_manager = None  # Référence au ProjectManager pour communication bidirectionnelle
        
        # Initialiser TOUTES les variables dès le début
        self._init_all_variables()
        
        # Variables communes
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

        # Enregistrer dans le ProjectManager (communication bidirectionnelle)
        if hasattr(self.parent_window, 'app_controller'):
            app_controller = self.parent_window.app_controller
            if hasattr(app_controller, 'project_manager'):
                app_controller.project_manager.register_listener(
                    self._on_project_sync_changed,
                    source_name="maintenance_tools"
                )
                # Stocker la référence au ProjectManager pour l'envoi
                self.project_manager = app_controller.project_manager
                        
        
    
    def _init_all_variables(self):
        """Initialise toutes les variables tkinter nécessaires"""
        try:
            # === VARIABLES PRINCIPALES ===
            self.current_project_path = ""
            self.project_var = tk.StringVar(value="")
            self.status_var = tk.StringVar(value="Prêt")
            
            # === VARIABLES ONGLET NETTOYAGE ===
            self.cleanup_excluded_files_var = tk.StringVar(value=config_manager.get('cleanup_excluded_files', 'common.rpy'))
            self.available_languages = []
            self.language_vars = {}
            
            # === VARIABLES ONGLET ÉDITEUR TEMPS RÉEL ===
            self.realtime_language_var = tk.StringVar(value="french")
            self.monitoring_active = False
            self.monitoring_thread = None
            self.last_dialogue_line = 0
            self.current_vo_text = tk.StringVar(value="En attente de dialogue...")
            self.current_vf_text = tk.StringVar(value="")
            self.current_dialogue_info = {}
            self.monitor_status_label = None
            self.vo_text_widget = None
            self.vf_text_widget = None
            self.editor_font_size_var = tk.IntVar()
            default_size = config_manager.get('editor_font_size', 9)
            self.editor_font_size_var.set(default_size)
            self.detached_editor_window = None
            
            # === VARIABLES ONGLET COHÉRENCE ===
            self.coherence_project_path = ""
            self.coherence_language = ""
            self.coherence_selection_info = None
            self.coherence_project_selector = None
            self.analysis_results = None
            self.rapport_path = None
            
            # Variables d'analyse cohérence
            self.check_variables_var = tk.BooleanVar(value=True)
            self.check_tags_var = tk.BooleanVar(value=True)
            self.check_tags_content_var = tk.BooleanVar(value=True)  # 🆕 Vérifier contenu balises
            self.check_special_codes_var = tk.BooleanVar(value=True)
            self.check_untranslated_var = tk.BooleanVar(value=True)
            self.check_ellipsis_var = tk.BooleanVar(value=True)
            self.check_escape_sequences_var = tk.BooleanVar(value=True)
            self.check_percentages_var = tk.BooleanVar(value=True)
            self.check_quotations_var = tk.BooleanVar(value=True)
            self.check_parentheses_var = tk.BooleanVar(value=True)
            self.check_syntax_var = tk.BooleanVar(value=True)
            self.check_deepl_ellipsis_var = tk.BooleanVar(value=True)
            self.check_isolated_percent_var = tk.BooleanVar(value=True)
            self.check_line_structure_var = tk.BooleanVar(value=True)
            self.check_length_difference_var = tk.BooleanVar(value=True)
            self.coherence_excluded_files_var = tk.StringVar(value="common.rpy")
            self.custom_exclusions_var = tk.StringVar(value="")
            
            # Variables communes
            self.operation_buttons = []
            
            
            
        except Exception as e:
            log_message("ERREUR", f"Erreur initialisation variables: {e}", category="maintenance_tools")

    # Nouvelle méthode dans MaintenanceToolsInterface

    def _on_project_sync_changed(self, new_path: str):
        """Appelé quand le projet change depuis une autre interface"""
        try:
            if not new_path or new_path == self.current_project_path:
                return
            
            # Marquer qu'on reçoit une synchronisation pour éviter une boucle
            self._is_updating_from_sync = True
            
            log_message("INFO", f"Outils maintenance reçoivent sync: {os.path.basename(new_path)}", category="project_sync")
            
            # Appeler la fonction centrale qui valide et met à jour
            self._set_current_project(new_path)
            
            # Réinitialiser le flag après mise à jour
            self._is_updating_from_sync = False
            
        except Exception as e:
            self._is_updating_from_sync = False
            log_message("ERREUR", f"Erreur sync projet vers maintenance: {e}", category="project_sync")

    def _create_interface(self):
        """Crée l'interface utilisateur de maintenance"""
        # Fenêtre principale - parent_window est maintenant MainWindow, pas root
        parent_root = self.parent_window.root if hasattr(self.parent_window, 'root') else self.parent_window
        self.window = tk.Toplevel(parent_root)
        self.window.title("🔧 Outils de Maintenance Ren'Py")
        self.window.geometry("1200x900")
        
        # Support Drag & Drop sur toute la fenêtre si disponible
        if HAS_DND:
            try:
                self.window.drop_target_register(DND_FILES)
                self.window.dnd_bind('<<Drop>>', self._on_window_drop)
            except Exception as e:
                log_message("DEBUG", f"Drag & Drop non disponible: {e}", category="maintenance_tools")
        
        # Appliquer le thème
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
        
        # Charger la configuration
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
            text="🔧 Outils de Maintenance Ren'Py",
            font=('Segoe UI Emoji', 16, 'bold'),
            bg=theme["bg"],
            fg=theme["accent"]
        )
        title_label.pack()
        
        # Sous-titre
        subtitle_label = tk.Label(
            header_frame,
            text="Nettoyage • Éditeur Temps Réel • Vérification Cohérence\n🎯 Glissez-déposez un dossier de projet n'importe où dans cette fenêtre !",
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
                text="🎮 Projet:",
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
            bg=theme["button_nav_bg"],
            fg="#000000",
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

            # Notifier le ProjectManager UNIQUEMENT si ce n'est pas une synchronisation entrante
            if not self._is_updating_from_sync and self.project_manager:
                log_message("INFO", f"Outils maintenance notifient changement: {os.path.basename(path)}", category="project_sync")
                self.project_manager.set_project(path, source="maintenance_tools")

            self._trigger_post_project_selection_actions()

            config_manager.set('last_directory', os.path.dirname(path))
            config_manager.set('current_maintenance_project', path)
            

        except Exception as e:
            error_msg = f"Erreur lors de la définition du projet : {e}"
            self.project_info_label.config(text="❌ Erreur critique", fg='#ff8379')
            self._show_notification(error_msg, "error")
            log_message("ERREUR", error_msg, category="maintenance_tools")

    def handle_project_change(self):
        """Vérifie et arrête la surveillance temps réel avant un changement de projet"""
        # Vérifier si la surveillance est active
        if hasattr(self, 'monitoring_active') and self.monitoring_active:
            log_message("INFO", "Changement de projet détecté : Arrêt de la surveillance en cours...", category="maintenance_tools")
            
            # Appeler la fonction d'arrêt de l'onglet temps réel (uniquement onglet 7)
            try:
                from ui.tab_tools.realtime_editor_tab import stop_monitoring
                stop_monitoring(self)
            except Exception as e:
                log_message("ATTENTION", f"Impossible d'arrêter la surveillance: {e}", category="maintenance_tools") 
            
            # Notifier l'utilisateur
            self._show_notification(
                "Surveillance arrêtée en raison du changement de projet.",
                "info"
            )

    def _trigger_post_project_selection_actions(self):
        """Déclenche toutes les mises à jour nécessaires dans les onglets après la sélection d'un projet"""
        try:
            # 1) Cohérence : valide + auto-scan (scan langues + fichiers via le widget)
            if hasattr(self, 'coherence_project_selector') and self.coherence_project_selector:
                try:
                    self.coherence_project_selector._validate_and_set_project(self.current_project_path)
                except Exception as e:
                    log_message("DEBUG", f"Erreur mise à jour sélecteur cohérence : {e}", category="maintenance_tools")

            # 2) Nettoyage TL : hook exposé par l’onglet 5 (auto-scan langues si possible)
            if hasattr(self, "cleaning_resync") and callable(self.cleaning_resync):
                try:
                    self.cleaning_resync()
                except Exception as e:
                    log_message("DEBUG", f"Erreur resync nettoyage TL : {e}", category="maintenance_tools")

            # 3) Éditeur Temps Réel : hook exposé par l’onglet 7 (auto-scan langues combo)
            if hasattr(self, "realtime_resync") and callable(self.realtime_resync):
                try:
                    self.realtime_resync()
                except Exception as e:
                    log_message("DEBUG", f"Erreur resync éditeur temps réel : {e}", category="maintenance_tools")
        except Exception as e:
            log_message("DEBUG", f"Erreur actions post-sélection projet : {e}", category="maintenance_tools")


    def _on_project_path_changed(self, event=None):
        """Appelé lors de la saisie manuelle, appelle la fonction centrale"""
        path = self.project_var.get()
        if path and os.path.isdir(path):
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
            log_message("ATTENTION", f"Erreur validation projet: {e}", category="maintenance_tools")
            return False

    def _update_project_info(self, project_path: str):
        """Met à jour l'info sur le projet détecté"""
        try:
            project_name = os.path.basename(project_path)
            
            # Analyser rapidement le projet
            game_dir = os.path.join(project_path, "game")
            has_game = os.path.isdir(game_dir)
            
            # Chercher des traductions existantes
            tl_dir = os.path.join(game_dir, "tl") if has_game else None
            tl_langs = []
            if tl_dir and os.path.isdir(tl_dir):
                tl_langs = [d for d in os.listdir(tl_dir) if os.path.isdir(os.path.join(tl_dir, d)) and d.lower() != 'none']
            
            # Construire le message d'info
            info_parts = [f"✅ Projet: {project_name}"]
            
            if tl_langs:
                info_parts.append(f"Traductions: {', '.join(tl_langs[:3])}")
                if len(tl_langs) > 3:
                    info_parts.append("...")
            
            info_text = " • ".join(info_parts)
            
            self.project_info_label.config(text=info_text, fg=theme_manager.get_theme()["fg"])
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur mise à jour info projet: {e}", category="maintenance_tools")
            self.project_info_label.config(text="✅ Projet Ren'Py détecté", fg=theme_manager.get_theme()["fg"])

    def _on_window_drop(self, event):
        """Gère le glisser-déposer et appelle la fonction centrale"""
        try:
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
            log_message("ERREUR", error_msg, category="maintenance_tools")

    def _create_main_content(self):
        """Crée le contenu principal avec les 3 onglets"""
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
        
        # Styles uniformes pour les Combobox
        theme_manager.apply_uniform_combobox_style(style)
        
        self.notebook = ttk.Notebook(main_frame, style="Custom.TNotebook")
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        self.notebook.pack(fill='both', expand=True)
        
        # Créer les 3 onglets (imports différés pour éviter les imports lourds au démarrage)
        try:
            from ui.tab_tools.cleaning_tab import create_cleaning_tab
            create_cleaning_tab(self.notebook, self)            # Onglet 1: Nettoyage
        except Exception as e:
            log_message("ERREUR", f"Erreur création onglet nettoyage: {e}", category="maintenance_tools")
        
        try:
            from ui.tab_tools.realtime_editor_tab import create_realtime_editor_tab
            create_realtime_editor_tab(self.notebook, self)     # Onglet 2: Éditeur Temps Réel
        except Exception as e:
            log_message("ERREUR", f"Erreur création onglet éditeur: {e}", category="maintenance_tools")
        
        try:
            from ui.tab_tools.coherence_tab import create_coherence_tab
            create_coherence_tab(self.notebook, self)           # Onglet 3: Cohérence
        except Exception as e:
            log_message("ERREUR", f"Erreur création onglet cohérence: {e}", category="maintenance_tools")

    # =================================================================
    # MÉTHODES UTILITAIRES
    # =================================================================

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
            bg=theme["button_danger_bg"],
            fg="#000000",
            font=('Segoe UI', 9),
            pady=4,
            padx=8
        )
        close_btn.pack(side='right')

        self.cancel_operation_btn = tk.Button(
            single_line_frame,
            text="ℹ️ Annuler l'opération",
            command=self._cancel_operation,
            bg=theme["button_tertiary_bg"],
            fg="#000000",
            font=('Segoe UI', 9),
            pady=4,
            padx=8,
            state='disabled'
        )
        self.cancel_operation_btn.pack(side='right', padx=(0, 10))

    def _load_config(self):
        """Charge la configuration depuis config_manager"""
        try:
            # 🆕 PRIORITÉ : Charger le projet actuel du ProjectManager si disponible
            project_to_load = None
            if hasattr(self, 'parent_window'):
                app_controller = getattr(self.parent_window, 'app_controller', None)
                if app_controller and hasattr(app_controller, 'project_manager'):
                    current_project = app_controller.project_manager.get_current_project()
                    if current_project and os.path.exists(current_project):
                        project_to_load = current_project
                        log_message("INFO", f"Projet chargé depuis ProjectManager: {os.path.basename(current_project)}", category="maintenance_tools")
            
            # Sinon, charger le projet précédent de la config
            if not project_to_load:
                last_project = config_manager.get('current_maintenance_project', '')
                if not last_project:
                    # Migration depuis d'autres modules éventuels
                    last_project = (config_manager.get('current_renpy_project', '') 
                                    or config_manager.get('last_coherence_project_path', ''))
                
                if last_project and os.path.exists(last_project):
                    project_to_load = last_project
            
            # Appliquer le projet trouvé
            if project_to_load:
                self.project_var.set(project_to_load)
                self.current_project_path = project_to_load
                self._update_project_info(project_to_load)
                # ✅ Déclenche les actions post-sélection (cohérence + hooks des autres onglets)
                self._trigger_post_project_selection_actions()

            # Exclusions nettoyage
            if hasattr(self, 'cleanup_excluded_files_var'):
                cleanup_exclusions = config_manager.get('cleanup_excluded_files', 'common.rpy')
                self.cleanup_excluded_files_var.set(cleanup_exclusions)
            
            # Configuration éditeur temps réel
            if hasattr(self, 'realtime_language_var'):
                realtime_lang = config_manager.get('realtime_default_language', 'french')
                self.realtime_language_var.set(realtime_lang)

            # Configuration cohérence
            self.check_variables_var.set(config_manager.get('coherence_check_variables', True))
            self.check_tags_var.set(config_manager.get('coherence_check_tags', True))
            self.check_tags_content_var.set(config_manager.get('coherence_check_tags_content', True))
            self.check_special_codes_var.set(config_manager.get('coherence_check_special_codes', True))
            self.check_untranslated_var.set(config_manager.get('coherence_check_untranslated', True))
            self.check_ellipsis_var.set(config_manager.get('coherence_check_ellipsis', True))
            self.check_escape_sequences_var.set(config_manager.get('coherence_check_escape_sequences', True))
            self.check_percentages_var.set(config_manager.get('coherence_check_percentages', True))
            self.check_quotations_var.set(config_manager.get('coherence_check_quotations', True))
            self.check_parentheses_var.set(config_manager.get('coherence_check_parentheses', True))
            self.check_syntax_var.set(config_manager.get('coherence_check_syntax', True))
            self.check_deepl_ellipsis_var.set(config_manager.get('coherence_check_deepl_ellipsis', True))
            self.check_isolated_percent_var.set(config_manager.get('coherence_check_isolated_percent', True))
            self.check_line_structure_var.set(config_manager.get('coherence_check_line_structure', True))
            
            # Exclusions cohérence
            coherence_exclusions = config_manager.get('coherence_excluded_files', 'common.rpy')
            self.coherence_excluded_files_var.set(coherence_exclusions)
            
            # 🆕 Les exclusions personnalisées sont maintenant gérées via le rapport HTML interactif
            # Ce champ est désactivé pour éviter de corrompre la structure dictionnaire
            self.custom_exclusions_var.set("(Gérées via le rapport HTML interactif)")

        except Exception as e:
            log_message("ERREUR", f"Erreur chargement configuration maintenance: {e}", category="maintenance_tools")

    def _select_project(self):
        """Ouvre une boîte de dialogue pour sélectionner un projet"""
        initial_dir = os.path.dirname(self.current_project_path or '') or config_manager.get('last_directory', os.path.expanduser('~'))
        
        project_path = filedialog.askdirectory(
            title='Sélectionner le dossier du projet Ren\'Py',
            initialdir=initial_dir
        )
        
        if project_path:
            self._set_current_project(project_path)

    def _on_tab_changed(self, event=None):
        try:
            tab_text = self.notebook.tab(self.notebook.select(), "text") or ""
            # Si on revient sur l’onglet Cohérence, on s'assure que tout est bien à jour
            if "Cohérence" in tab_text and hasattr(self, 'coherence_project_selector') and self.coherence_project_selector:
                if self.current_project_path:
                    self.coherence_project_selector._validate_and_set_project(self.current_project_path)
                    self.coherence_project_selector._scan_files()
        except Exception as e:
            log_message("DEBUG", f"TabChanged refresh error: {e}", category="maintenance_tools")


    def _cancel_operation(self):
        """Annule l'opération en cours"""
        try:
            if self.is_operation_running:
                self._update_status('Annulation en cours...')
        except Exception as e:
            log_message("ERREUR", f"Erreur annulation opération: {e}", category="maintenance_tools")

    # =================================================================
    # MÉTHODES UTILITAIRES
    # =================================================================
    def _on_operation_complete(self, success: bool, results: Dict[str, Any]):
        """Callback à la fin d'une opération (compatibilité)"""
        try:
            self._set_operation_running(False)
            
            if success and isinstance(results, dict):
                summary = results.get('summary', {})
                if 'cleaning' in summary:
                    self._update_status(summary['cleaning'], "success")
                else:
                    self._update_status("Opération terminée avec succès", "success")
            else:
                self._update_status("Opération terminée avec des erreurs", "error")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur _on_operation_complete: {e}", category="maintenance_tools")

    def _on_error(self, error_message: str, exception: Exception = None):
        """Callback en cas d'erreur (compatibilité)"""
        try:
            self._set_operation_running(False)
            self._update_status(f"Erreur : {error_message}", "error")
            self._show_notification(error_message, "error")
            
            if exception:
                log_message("ERREUR", f"Erreur opération: {exception}", category="maintenance_tools")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur _on_error: {e}", category="maintenance_tools")

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
        
        if not running:
            self._update_status("Prêt")
    
    def _show_notification(self, message: str, toast_type: str = "info"):
        """Affiche une notification"""
        try:
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
                import tkinter.messagebox as messagebox
                if toast_type == "error":
                    show_translated_messagebox('error', 'Erreur', message)
                elif toast_type == "warning":
                    show_translated_messagebox('warning', 'Avertissement', message)
                else:
                    show_translated_messagebox('info', 'Information', message)
                    
        except Exception as e:
            log_message("ERREUR", f"Erreur show_notification: {e}", category="maintenance_tools")
    
    def _update_status(self, message: str, status_type: str = "normal"):
        """Met à jour le statut - VERSION AVEC SUPPORT TYPE OPTIONNEL"""
        try:
            self.status_var.set(message)
            
            # Couleurs selon le type de message ou le paramètre status_type
            if status_type == "success" or any(word in message.lower() for word in ['terminé', 'succès', 'réussi', 'fini', 'complete']):
                self.status_label.config(fg='#28a745')  # Vert
            elif status_type == "error" or any(word in message.lower() for word in ['erreur', 'échec', 'failed', 'error']):
                self.status_label.config(fg='#ff8379')  # Rouge
            elif status_type == "info" or any(word in message.lower() for word in ['en cours', 'nettoyage', 'édition', 'analyse', 'préparation']):
                self.status_label.config(fg='#2196F3')  # Bleu
            else:
                self.status_label.config(fg=theme_manager.get_theme()["fg"])  # Normal
                
        except Exception as e:
            log_message("ERREUR", f"Erreur update_status: {e}", category="maintenance_tools")

    def _on_progress_update(self, progress: int, message: str = ""):
        """Callback de mise à jour du progrès - COMPATIBILITÉ"""
        try:
            if message:
                self._update_status(message)
        except Exception as e:
            log_message("ERREUR", f"Erreur _on_progress_update: {e}", category="maintenance_tools")

    def _get_realtime_editor_business(self):
        """Obtient l'instance RealTime Editor business en initialisant si nécessaire"""
        if not hasattr(self, 'realtime_editor_business') or self.realtime_editor_business is None:
            self.realtime_editor_business = RealTimeEditorBusiness()
            self.realtime_editor_business.set_callbacks(
                status_callback=self._update_status,
                error_callback=lambda msg: self._show_notification(f"Erreur: {msg}", "error")
            )
        return self.realtime_editor_business
    
    def _on_close(self):
        """Gestion de la fermeture de la fenêtre"""
        try:
            # Vérifier les modifications en attente avant fermeture (éditeur temps réel)
            if hasattr(self, 'realtime_editor_business') and self.realtime_editor_business:
                if self.realtime_editor_business.has_pending_modifications():
                    count = self.realtime_editor_business.get_pending_count()
                    message = f"{count} modification{'s' if count > 1 else ''} n'ont pas été enregistrée{'s' if count > 1 else ''}.\n\nVoulez-vous les sauvegarder ?"
                    
                    from ui.themes import theme_manager
                    theme = theme_manager.get_theme()
                    response = show_custom_askyesnocancel(
                        "Modifications en attente",
                        message,
                        theme,
                        yes_text="Oui",
                        no_text="Non", 
                        cancel_text="Annuler",
                        parent=self.window
                    )
                    
                    if response is None:  # Annuler
                        return
                    elif response is True:  # Oui
                        save_result = self.realtime_editor_business.save_all_pending_modifications(self.current_project_path)
                        if not save_result.get('success'):
                            error_msg = " / ".join(save_result.get('errors', [])) or "Erreur inconnue"
                            show_translated_messagebox(
                                'error',
                                'Erreur sauvegarde',
                                f"Impossible de sauvegarder les modifications:\n{error_msg}\n\nFermeture annulée.",
                                parent=self.window
                            )
                            return

            # Arrêter la surveillance temps réel si active
            if hasattr(self, 'monitoring_active') and self.monitoring_active:
                try:
                    realtime_business = self._get_realtime_editor_business()
                    realtime_business.stop_monitoring()
                    log_message("INFO", "Surveillance temps réel arrêtée à la fermeture", category="maintenance_tools")
                except Exception as e:
                    log_message("ATTENTION", f"Erreur arrêt surveillance: {e}", category="maintenance_tools")

            # Dans _on_close, désenregistrer

            # Désenregistrer du ProjectManager
            if hasattr(self, 'parent_window'):
                app_controller = getattr(self.parent_window, 'app_controller', None)
                if app_controller and hasattr(app_controller, 'project_manager'):
                    app_controller.project_manager.unregister_listener("maintenance_tools")
                    log_message("DEBUG", "Outils maintenance désenregistrés du ProjectManager", category="project_sync")

            # Sauvegarder les paramètres
            try:
                # Projet actuel
                if self.current_project_path:
                    config_manager.set('current_maintenance_project', self.current_project_path)

                # Exclusions nettoyage
                if hasattr(self, 'cleanup_excluded_files_var'):
                    config_manager.set('cleanup_excluded_files', self.cleanup_excluded_files_var.get())

                # Paramètres de l'éditeur temps réel
                if hasattr(self, 'realtime_language_var'):
                    config_manager.set('realtime_default_language', self.realtime_language_var.get())
                
                if hasattr(self, 'monitoring_active'):
                    config_manager.set('realtime_monitoring_was_active', self.monitoring_active)

                # Options cohérence
                config_manager.set('coherence_check_variables', self.check_variables_var.get())
                config_manager.set('coherence_check_tags', self.check_tags_var.get())
                config_manager.set('coherence_check_tags_content', self.check_tags_content_var.get())
                config_manager.set('coherence_check_special_codes', self.check_special_codes_var.get())
                config_manager.set('coherence_check_untranslated', self.check_untranslated_var.get())
                config_manager.set('coherence_excluded_files', self.coherence_excluded_files_var.get())
                
                # 🆕 NE PLUS sauvegarder coherence_custom_exclusions ici
                # Les exclusions sont maintenant gérées exclusivement via le rapport HTML interactif
                # (structure dictionnaire par projet/fichier/ligne, pas une simple liste de textes)

                log_message("INFO", "Paramètres sauvegardés à la fermeture (maintenance)", category="maintenance_tools")
                
            except Exception as e:
                log_message("ERREUR", f"Erreur sauvegarde à la fermeture: {e}", category="maintenance_tools")
            
            # Nettoyer le business
            if hasattr(self, 'realtime_editor_business') and self.realtime_editor_business:
                self.realtime_editor_business.cleanup()
                
            # Détruire la fenêtre
            self.window.destroy()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur fermeture interface maintenance: {e}", category="maintenance_tools")

def show_maintenance_tools_interface(parent_window):
    """Fonction principale pour afficher l'interface des outils de maintenance"""
    try:
        interface = MaintenanceToolsInterface(parent_window)
        log_message("INFO", "🔧 Outils Ren'Py lancée", category="maintenance_tools")
        return interface
        
    except Exception as e:
        log_message("ERREUR", f"Erreur lancement interface maintenance: {e}", category="maintenance_tools")
        
        # Fallback avec messagebox
        try:
            show_translated_messagebox(
                "error",
                "Erreur",
                f"Impossible de lancer l'interface des outils de maintenance:\n\n{e}"
            )
        except Exception:
            pass
        
        return None