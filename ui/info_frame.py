# ui/info_frame.py
# Info Frame Component - VERSION UNIFIÉE AVEC ProjectLanguageSelector + MODE DUAL
# Created for RenExtract 

"""
Composant d'affichage des informations de fichier et statut
VERSION UNIFIÉE + MODE DUAL : Utilise ProjectLanguageSelector avec support fichier unique
"""

import tkinter as tk
import os
from infrastructure.config.constants import THEMES
from infrastructure.config.config import config_manager
from ui.themes import theme_manager
from core.models.files.file_manager import file_manager
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import get_last_directory, set_last_directory
from ui.shared.project_widgets import ProjectLanguageSelector

class InfoFrame(tk.Frame):
    """Frame d'informations avec ProjectLanguageSelector unifié et mode dual"""
    
    def __init__(self, parent, app_controller):
        self.app_controller = app_controller
        
        # Initialiser le Frame avec le thème
        theme = theme_manager.get_theme()
        super().__init__(
            parent,
            bg=theme["bg"],
            relief='flat',
            bd=1,
            padx=8,
            pady=10
        )
        
        # Widgets principaux
        self.main_frame = None
        self.project_selector = None
        self.info_line = None
        self.label_info_left = None
        self.label_info_right = None
        self.next_file_btn = None
        self.processing_label = None
        
        # État
        self.is_processing = False
        self.current_project_path = ""
        self.current_language = ""
        self.current_files = []
        self.current_file_index = 0
        
        # NOUVEAU : État pour mode dual
        self.current_mode = "project"  # "project" ou "single_file"
        self.single_file_path = ""
        
        self._create_widgets()
        self._setup_drag_drop()
        self._load_initial_project()
    
    def _create_widgets(self):
        """Crée les widgets du frame d'information"""
        theme = theme_manager.get_theme()
        
        # Frame principal
        self.main_frame = tk.Frame(self, bg=theme["bg"], relief='solid', borderwidth=1)
        self.main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # === SÉLECTEUR DE PROJET UNIFIÉ AVEC MODE DUAL ===
        self.project_selector = ProjectLanguageSelector(
            self.main_frame,
            initial_project_path=config_manager.get('current_project', ''),
            on_project_changed=self._on_project_changed,
            on_language_changed=self._on_language_changed,
            on_files_changed=self._on_files_changed,
            show_project_input=True
        )
        
        # === LIGNE D'INFORMATIONS ET NAVIGATION ===
        self.info_line = tk.Frame(self.main_frame, bg=theme["bg"])
        self.info_line.pack(fill='x', padx=10, pady=(5, 8))
        
        # Label gauche (informations générales)
        self.label_info_left = tk.Label(
            self.info_line,
            text="Sélectionnez un projet ou un fichier pour commencer",
            font=('Consolas', 11, 'bold'),
            bg=theme["bg"],
            fg=theme["accent"],
            anchor='w',
            justify='left'
        )
        self.label_info_left.pack(side='left', fill='x', expand=True)
        
        # Bouton Fichier Suivant (masqué initialement)
        self.next_file_btn = tk.Button(
            self.info_line,
            text="▶️ Fichier Suivant",
            command=self._next_file,
            bg=theme["button_secondary_bg"],
            fg="#000000",
            font=('Segoe UI', 9),
            relief='solid',
            cursor='hand2',
            width=15,
            pady=8
        )
        # Ne pas pack encore - sera affiché quand nécessaire
        
        # Label droite (statistiques)
        self.label_info_right = tk.Label(
            self.info_line,
            text="",
            font=('Consolas', 11, 'bold'),
            bg=theme["bg"],
            fg=theme["accent"],
            anchor='e',
            justify='right'
        )
        self.label_info_right.pack(side='right', fill='x')
        
        # Label de traitement (caché par défaut)
        self.processing_label = tk.Label(
            self.info_line,
            text="",
            font=('Consolas', 11, 'bold'),
            bg=theme["bg"],
            fg="#ffc107",
            anchor='center',
            justify='center'
        )
        self.processing_label.pack_forget()
    
    def _setup_drag_drop(self):
        """Configure le drag & drop sur le frame principal"""
        try:
            import tkinterdnd2 as dnd2
            
            # Enregistrer le drop target sur le frame principal
            self.main_frame.drop_target_register(dnd2.DND_FILES)
            self.main_frame.dnd_bind('<<Drop>>', self._on_drop)
            self.main_frame.dnd_bind('<<DragEnter>>', self._on_drag_enter)
            self.main_frame.dnd_bind('<<DragLeave>>', self._on_drag_leave)
            
            
            
        except ImportError:
            log_message("DEBUG", "tkinterdnd2 non disponible - Drag & Drop désactivé", category="ui_info")
        except Exception as e:
            log_message("ATTENTION", f"Erreur configuration D&D InfoFrame: {e}", category="ui_info")
    
    def _load_initial_project(self):
        """Charge le projet initial depuis la configuration"""
        try:
            initial_project = config_manager.get('current_project', '')
            if initial_project and os.path.exists(initial_project):
                self.after(200, self._force_initial_sync)
            else:
                pass  # Aucun projet initial à charger
        except Exception as e:
            log_message("ATTENTION", f"Erreur chargement projet initial: {e}", category="ui_info")

    def _force_initial_sync(self):
        """Force la synchronisation initiale après le chargement automatique"""
        try:
            # Attendre que l'interface soit complètement initialisée
            self.after(100, self._delayed_initial_sync)
        except Exception as e:
            log_message("ERREUR", f"Erreur synchronisation forcée: {e}", category="ui_info")
    
    def _delayed_initial_sync(self):
        """Synchronisation initiale avec délai pour l'interface"""
        try:
            if self.project_selector:
                current_selection = self.project_selector.get_current_selection()
                
                if (current_selection and 
                    current_selection.get('project_path') and 
                    current_selection.get('file_paths')):
                    
                    log_message("DEBUG", "Déclenchement forcé de la synchronisation initiale", category="ui_info")
                    self._on_files_changed(current_selection)
                else:
                    log_message("DEBUG", "Pas de sélection valide pour la sync initiale", category="ui_info")
        except Exception as e:
            log_message("ERREUR", f"Erreur synchronisation forcée: {e}", category="ui_info")
    
    # =============================================================================
    # CALLBACKS DU ProjectLanguageSelector
    # =============================================================================
    
    def _on_project_changed(self, project_path):
        """Appelé quand le projet change"""
        try:
            if os.path.isfile(project_path):
                # Mode fichier unique
                self.current_mode = "single_file"
                self.single_file_path = project_path
                self.current_project_path = os.path.dirname(project_path)
                config_manager.set('current_project', os.path.dirname(project_path))
                log_message("INFO", f"Mode fichier unique: {os.path.basename(project_path)}", category="ui_info")
            else:
                # Mode projet
                self.current_mode = "project"
                self.current_project_path = project_path
                self.single_file_path = ""
                config_manager.set('current_project', project_path)
                log_message("INFO", f"Mode projet: {os.path.basename(project_path)}", category="ui_info")
            
            # ✅ AJOUT : Notifier le ProjectManager via AppController
            if hasattr(self, 'app_controller') and self.app_controller:
                if hasattr(self.app_controller, 'project_manager'):
                    actual_path = project_path if self.current_mode == "project" else self.current_project_path
                    self.app_controller.project_manager.set_project(actual_path, source="main_window")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur changement projet: {e}", category="ui_info")
    
    def _on_language_changed(self, language_name):
        """Appelé quand la langue change"""
        try:
            self.current_language = language_name
        except Exception as e:
            log_message("ERREUR", f"Erreur changement langue: {e}", category="ui_info")
    
    def _on_files_changed(self, selection_info):
        """Appelé quand la sélection de fichiers change"""
        try:
            if not selection_info or not selection_info.get('file_paths'):
                self._clear_file_selection()
                return
            
            is_single_file_mode = selection_info.get('is_single_file_mode', False)
            
            if is_single_file_mode:
                # Mode fichier unique
                self.current_mode = "single_file"
                self.single_file_path = selection_info['file_paths'][0]
                self.current_files = [self.single_file_path]
                self.current_file_index = 0
                
                # Configurer le file_manager
                file_manager.is_folder_mode = False
                file_manager.folder_files = []
                file_manager.total_files = 1
                file_manager.current_file_index = 0
                file_manager.folder_path = os.path.dirname(self.single_file_path)
                
                self._hide_next_file_button()
                
                if self.current_files:
                    self._load_current_file()
                
                log_message("INFO", f"Fichier unique chargé: {os.path.basename(self.single_file_path)}", category="ui_info")
                
            else:
                # Mode projet
                self.current_mode = "project"
                self.single_file_path = ""
                self.current_files = selection_info['file_paths']
                self.current_file_index = 0
                
                if len(self.current_files) > 1:
                    file_manager.is_folder_mode = True
                    file_manager.folder_files = self.current_files
                    file_manager.total_files = len(self.current_files)
                    file_manager.current_file_index = 0
                    file_manager.folder_path = os.path.dirname(self.current_files[0])
                    self._show_next_file_button()
                else:
                    file_manager.is_folder_mode = False
                    file_manager.folder_files = []
                    file_manager.total_files = 0
                    file_manager.current_file_index = 0
                    self._hide_next_file_button()
                
                if self.current_files:
                    # Attendre que l'interface soit prête avant de charger le fichier
                    self.after(150, self._load_current_file)
            
        except Exception as e:
            log_message("ERREUR", f"Erreur changement fichiers: {e}", category="ui_info")
    
    def _load_current_file(self):
        """Charge le fichier actuel"""
        try:
            if not self.current_files or self.current_file_index >= len(self.current_files):
                return
            
            current_file = self.current_files[self.current_file_index]
            
            if hasattr(self.app_controller, '_validate_and_load_file'):
                success = self.app_controller._validate_and_load_file(current_file)
                if success:
                    self._update_display_for_loaded_file(current_file)
                    return True
            
            return False
            
        except Exception as e:
            log_message("ERREUR", f"Erreur chargement fichier: {e}", category="ui_info")
            return False
    
    def _update_display_for_loaded_file(self, filepath):
        """Met à jour l'affichage pour le fichier chargé"""
        try:
            filename = os.path.basename(filepath)
            progress_indicator = self._get_progress_indicator(filepath)
            
            if self.current_mode == "single_file":
                # Affichage mode fichier unique
                file_dir = os.path.basename(os.path.dirname(filepath))
                
                if self.label_info_left:
                    self.label_info_left.config(
                        text=f"{progress_indicator} 📄 Fichier unique • {file_dir} • {filename}",
                        fg="#9b59b6"
                    )
                
                line_count = 0
                if hasattr(self.app_controller, 'file_content') and self.app_controller.file_content:
                    line_count = len(self.app_controller.file_content)
                
                if self.label_info_right:
                    self.label_info_right.config(
                        text=f"{line_count} lignes",
                        fg="#9b59b6"
                    )
                
            else:
                # Affichage mode projet
                project_name = os.path.basename(self.current_project_path) if self.current_project_path else "Projet"
                
                if len(self.current_files) > 1:
                    current_num = self.current_file_index + 1
                    total = len(self.current_files)
                    
                    if self.label_info_left:
                        self.label_info_left.config(
                            text=f"{progress_indicator} {project_name} • {self.current_language} • {filename}",
                            fg=theme_manager.get_theme()["fg"]
                        )
                    
                    line_count = 0
                    if hasattr(self.app_controller, 'file_content') and self.app_controller.file_content:
                        line_count = len(self.app_controller.file_content)
                    
                    progress_stats = self._get_files_progress_stats()
                    
                    if self.label_info_right:
                        self.label_info_right.config(
                            text=f"{line_count} lignes | {current_num}/{total} fichiers {progress_stats}",
                            fg=theme_manager.get_theme()["fg"]
                        )
                else:
                    if self.label_info_left:
                        self.label_info_left.config(
                            text=f"{progress_indicator} {project_name} • {self.current_language} • {filename}",
                            fg=theme_manager.get_theme()["fg"]
                        )
                    
                    line_count = 0
                    if hasattr(self.app_controller, 'file_content') and self.app_controller.file_content:
                        line_count = len(self.app_controller.file_content)
                    
                    if self.label_info_right:
                        self.label_info_right.config(
                            text=f"{line_count} lignes",
                            fg=theme_manager.get_theme()["fg"]
                        )
            
            if self.current_mode == "project" and len(self.current_files) > 1:
                self._update_next_file_button_state()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur mise à jour affichage: {e}", category="ui_info")

    def _get_progress_indicator(self, filepath: str) -> str:
        """Indicateur de progression basé sur modification récente"""
        try:
            if not config_manager.get('project_progress_tracking', False):
                return "🔳"
            
            if hasattr(self.app_controller, '_get_translation_progress_tracker'):
                tracker = self.app_controller._get_translation_progress_tracker()
                if tracker:
                    filename = os.path.basename(filepath)
                    status = tracker.get_file_status(filename)
                    
                    # ✅ NOUVEAU : Gérer le statut "completed" (fichier reconstruit)
                    if status == "completed":
                        return "✅"
                    elif status == "recently_modified":
                        return "✅"
                    else:
                        return "⬜"
            
            return "🔳"
            
        except Exception as e:
            log_message("DEBUG", f"Erreur indicateur: {e}", category="ui_info")
            return "🔳"

    def _get_files_progress_stats(self) -> str:
        """Retourne les stats de progression pour la série de fichiers"""
        try:
            if (self.current_mode == "single_file" or 
                not config_manager.get('project_progress_tracking', False) or 
                not hasattr(self.app_controller, '_get_progress_tracker')):
                return ""
            
            tracker = self.app_controller._get_progress_tracker()
            if not tracker:
                return ""
            
            completed = 0
            skipped = 0
            
            for file_info in self.current_files:
                if isinstance(file_info, dict):
                    filepath = file_info.get('path')
                else:
                    filepath = file_info
                
                if filepath:
                    status = tracker.get_file_status(filepath)
                    if status == "completed":
                        completed += 1
                    elif status == "skipped_technical":
                        skipped += 1
            
            if completed > 0 or skipped > 0:
                return f"(✅{completed} ⚙️{skipped})"
            
            return ""
            
        except Exception as e:
            log_message("DEBUG", f"Erreur stats progression: {e}", category="ui_info")
            return ""
    
    def _clear_file_selection(self):
        """Remet l'affichage à l'état initial"""
        self.current_files = []
        self.current_file_index = 0
        self.current_mode = "project"
        self.single_file_path = ""
        
        self.label_info_left.config(
            text="Sélectionnez un projet/fichier et une langue",
            fg=theme_manager.get_theme()["fg"]
        )
        self.label_info_right.config(text="")
        
        self._hide_next_file_button()
        
        file_manager.is_folder_mode = False
        file_manager.folder_files = []
        file_manager.total_files = 0
        file_manager.current_file_index = 0
    
    # =============================================================================
    # NAVIGATION FICHIERS
    # =============================================================================
    
    def _next_file(self):
        """Passe au fichier suivant"""
        try:
            if self.current_mode == "single_file":
                self.app_controller.main_window.show_notification(
                    "Navigation non disponible en mode fichier unique.", 
                    'TOAST', toast_type='info'
                )
                return
            
            if not self.current_files or self.current_file_index >= len(self.current_files) - 1:
                self.app_controller.main_window.show_notification(
                    "C'était le dernier fichier de la sélection.", 
                    'TOAST', toast_type='info'
                )
                return
            
            self.current_file_index += 1
            file_manager.current_file_index = self.current_file_index
            
            if self._load_current_file():
                current_filename = os.path.basename(self.current_files[self.current_file_index])
                remaining = len(self.current_files) - self.current_file_index - 1
                
                self.app_controller.main_window.show_notification(
                    f"Fichier suivant: {current_filename} ({remaining} restants)",
                    'TOAST', toast_type='success'
                )
            
        except Exception as e:
            log_message("ERREUR", f"Erreur fichier suivant: {e}", category="ui_info")
            self.app_controller.main_window.show_notification(
                "Erreur lors du passage au fichier suivant",
                'TOAST', toast_type='error'
            )
    
    def _show_next_file_button(self):
        """Affiche le bouton Fichier Suivant"""
        if self.next_file_btn and self.current_mode == "project":
            self.next_file_btn.pack(side='right', padx=(5, 10), before=self.label_info_right)
            self._update_next_file_button_state()
    
    def _hide_next_file_button(self):
        """Cache le bouton Fichier Suivant"""
        if self.next_file_btn:
            self.next_file_btn.pack_forget()
    
    def _update_next_file_button_state(self):
        """Met à jour l'état du bouton Fichier Suivant"""
        if not self.next_file_btn or self.current_mode == "single_file":
            return
        
        try:
            has_next = (self.current_files and 
                       self.current_file_index < len(self.current_files) - 1)
            
            if has_next:
                remaining = len(self.current_files) - self.current_file_index - 1
                self.next_file_btn.config(
                    text=f"▶️ Suivant ({remaining})",
                    bg=theme_manager.get_theme()["button_secondary_bg"],
                    fg='#000000',
                    state='normal'
                )
            else:
                self.next_file_btn.config(
                    text="⏹ Dernier fichier",
                    bg='#6c757d',
                    fg='#000000',
                    state='disabled'
                )
                
        except Exception as e:
            log_message("ATTENTION", f"Erreur MAJ bouton suivant: {e}", category="ui_info")
    
    # =============================================================================
    # DRAG & DROP
    # =============================================================================
    
    def _on_drop(self, event):
        """Gère le drop de fichiers/dossiers"""
        try:
            raw_data = event.data
            log_message("DEBUG", f"Drop InfoFrame dual - données: {repr(raw_data)}", category="ui_info")
            
            dropped_path = self._parse_dropped_path(raw_data)
            
            if dropped_path and os.path.exists(dropped_path):
                if self.project_selector and hasattr(self.project_selector, 'handle_dropped_path'):
                    success = self.project_selector.handle_dropped_path(dropped_path)
                    if success:
                        log_message("INFO", f"Drag & drop traité: {os.path.basename(dropped_path)}", category="ui_info")
                    else:
                        log_message("ATTENTION", f"Échec traitement drop: {dropped_path}", category="ui_info")
            else:
                log_message("ATTENTION", f"Chemin droppé invalide: {dropped_path}", category="ui_info")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur drop InfoFrame dual: {e}", category="ui_info")
        
        return 'copy'
    
    def _parse_dropped_path(self, raw_data):
        """Parse le chemin droppé selon les différents formats possibles"""
        try:
            if raw_data.startswith('{') and raw_data.endswith('}'):
                return raw_data.strip('{}')
            elif '"' in raw_data:
                import re
                paths = re.findall(r'"([^"]*)"', raw_data)
                if paths:
                    return paths[0]
            else:
                parts = raw_data.split()
                if parts:
                    return parts[0]
            
            return raw_data.strip()
        except Exception:
            return raw_data.strip()
    
    def _on_drag_enter(self, event):
        """Effet visuel à l'entrée du drag"""
        try:
            self.main_frame.configure(relief='solid', borderwidth=2, highlightbackground='#28a745')
        except Exception:
            pass
        return 'copy'
    
    def _on_drag_leave(self, event):
        """Remet l'apparence normale à la sortie du drag"""
        try:
            theme = theme_manager.get_theme()
            self.main_frame.configure(relief='solid', borderwidth=1, highlightbackground=theme["bg"])
        except Exception:
            pass
        return 'copy'
    
    # =============================================================================
    # MÉTHODES DE COMPATIBILITÉ
    # =============================================================================
    
    def update_file_info(self, filepath, line_count, stats=None, execution_time=None):
        """Compatibilité avec l'ancien système"""
        try:
            if filepath:
                if self.current_mode == "single_file":
                    if filepath != self.single_file_path:
                        if os.path.exists(filepath) and os.path.isfile(filepath):
                            self.single_file_path = filepath
                            self.current_files = [filepath]
                            self.current_file_index = 0
                else:
                    if filepath not in self.current_files:
                        self.current_files = [filepath]
                        self.current_file_index = 0
                
                self._update_display_for_loaded_file(filepath)
                
                if execution_time is not None:
                    current_text = self.label_info_right.cget("text")
                    time_str = f"({execution_time:.1f}s)"
                    self.label_info_right.config(text=f"{current_text} {time_str}")
            else:
                self._clear_file_selection()
                
        except Exception as e:
            log_message("ERREUR", f"Erreur update_file_info: {e}", category="ui_info")
    
    def update_status(self, message):
        """Compatibilité - mise à jour du statut"""
        if self.label_info_left:
            self.label_info_left.config(text=message)
        if self.label_info_right:
            self.label_info_right.config(text="")
    
    def update_execution_time(self, execution_time):
        """Compatibilité - mise à jour du temps d'exécution"""
        if self.label_info_right and execution_time is not None:
            current_text = self.label_info_right.cget("text")
            if "(" in current_text and "s)" in current_text:
                current_text = current_text.split(" (")[0]
            
            time_str = f"({execution_time:.1f}s)"
            self.label_info_right.config(text=f"{current_text} {time_str}")
    
    def show_processing(self, message=None):
        """Affiche l'indicateur de traitement"""
        if not self.is_processing:
            self.is_processing = True
            if self.label_info_left:
                self.label_info_left.pack_forget()
            if self.label_info_right:
                self.label_info_right.pack_forget()
            if self.next_file_btn:
                self.next_file_btn.pack_forget()
            
            if self.processing_label:
                if message:
                    self.processing_label.config(text=message)
                else:
                    self.processing_label.config(text="🔄 Traitement en cours...")
                self.processing_label.pack(side='left', fill='x', expand=True)
            
            self.update()
    
    def hide_processing(self):
        """Cache l'indicateur de traitement"""
        if self.is_processing:
            self.is_processing = False
            if self.processing_label:
                self.processing_label.pack_forget()
            
            if self.label_info_left:
                self.label_info_left.pack(side='left', fill='x', expand=True)
            if self.label_info_right:
                self.label_info_right.pack(side='right', fill='x')
            
            if self.current_mode == "project" and len(self.current_files) > 1:
                self._show_next_file_button()
            
            self.update()
    
    # =============================================================================
    # MÉTHODES DE THÈME ET CONFIGURATION
    # =============================================================================
    
    def apply_theme(self):
        """Applique le thème au composant"""
        theme = theme_manager.get_theme()
        
        self.configure(bg=theme["bg"])
        if self.main_frame:
            self.main_frame.configure(bg=theme["bg"])
            
        if self.project_selector and hasattr(self.project_selector, 'apply_theme'):
            self.project_selector.apply_theme()
            
        fg_color = theme["fg"]
        
        if self.label_info_left:
            self.label_info_left.configure(bg=theme["bg"], fg=fg_color)
        if self.label_info_right:
            self.label_info_right.configure(bg=theme["bg"], fg=fg_color)
        if self.processing_label:
            self.processing_label.configure(bg=theme["bg"], fg="#ffc107")
        
        if self.next_file_btn:
            self.next_file_btn.configure(
                bg=theme["button_secondary_bg"],
                activebackground=theme.get("button_secondary_bg", "#007bff"),
                fg='#000000'
            )
    
    def update_language(self):
        """Met à jour les textes selon la langue"""
        pass
    
    # =============================================================================
    # MÉTHODES PUBLIQUES POUR INTÉGRATION
    # =============================================================================
    
    def set_path(self, path):
        """Définit le chemin depuis l'extérieur"""
        if path and os.path.exists(path):
            if self.project_selector and hasattr(self.project_selector, 'handle_dropped_path'):
                success = self.project_selector.handle_dropped_path(path)
                
                # 🆕 NOUVEAU : Notifier le ProjectManager si succès
                if success and hasattr(self, 'app_controller'):
                    app_controller = self.app_controller
                    if hasattr(app_controller, 'project_manager'):
                        # Déterminer le chemin réel selon le mode
                        actual_path = path
                        if self.project_selector.is_single_file_mode():
                            actual_path = os.path.dirname(path)
                        
                        app_controller.project_manager.set_project(actual_path, source="main_window")
                
                if not success:
                    self._clear_file_selection()
        else:
            self._clear_file_selection()
    
    def get_current_path(self):
        """Retourne le chemin actuellement sélectionné"""
        if self.current_mode == "single_file":
            return self.single_file_path
        elif self.current_files and self.current_file_index < len(self.current_files):
            return self.current_files[self.current_file_index]
        return ""
    
    def get_current_mode(self):
        """Retourne le mode actuel"""
        return self.current_mode
    
    def is_single_file_mode(self):
        """Retourne True si en mode fichier unique"""
        return self.current_mode == "single_file"
    
    def clear_path(self):
        """Efface la sélection et remet l'état initial"""
        self._clear_file_selection()
    
    def refresh_display(self):
        """Rafraîchit l'affichage selon l'état actuel et le mode"""
        try:
            if self.current_mode == "single_file" and self.single_file_path:
                self._update_display_for_loaded_file(self.single_file_path)
            elif self.current_mode == "project" and self.current_files and self.current_file_index < len(self.current_files):
                current_file = self.current_files[self.current_file_index]
                self._update_display_for_loaded_file(current_file)
            else:
                self._clear_file_selection()
                
        except Exception as e:
            log_message("ERREUR", f"Erreur refresh_display: {e}", category="ui_info")