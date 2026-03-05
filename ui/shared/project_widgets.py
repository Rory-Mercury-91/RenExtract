# ui/shared/project_widgets.py
# Widgets partagés pour la sélection de projets et langues
# VERSION AVEC MODE DUAL : Support fichier unique + projet complet

import tkinter as tk
import os
from tkinter import ttk
from ui.themes import theme_manager
from ui.shared.project_utils import (
    validate_renpy_project, 
    scan_project_languages, 
    scan_language_files,
    get_project_info_summary,
    parse_exclusions_string
)
from infrastructure.logging.logging import log_message

class ProjectLanguageSelector:
    """Widget composé pour sélection projet + langue + fichiers avec mode dual"""
    
    def __init__(self, parent_frame, initial_project_path="", 
                on_project_changed=None, on_language_changed=None, on_files_changed=None,
                show_project_input=True):
        """
        Initialise le sélecteur avec support dual mode
        
        Args:
            parent_frame: Frame parent
            initial_project_path: Chemin initial du projet
            on_project_changed: Callback(project_path) quand le projet change
            on_language_changed: Callback(language_name) quand la langue change  
            on_files_changed: Callback(selected_files_info) quand la sélection change
            show_project_input: Booléen pour afficher ou non la sélection de projet
        """
        self.parent_frame = parent_frame
        self.current_project_path = initial_project_path
        self.show_project_input = show_project_input
        
        # NOUVEAU : Mode de fonctionnement
        self.current_mode = "project"  # "project" ou "single_file"
        self.single_file_path = ""
        
        # Callbacks
        self.on_project_changed = on_project_changed
        self.on_language_changed = on_language_changed  
        self.on_files_changed = on_files_changed
        
        # Variables Tkinter
        self.project_var = tk.StringVar(value=initial_project_path)
        self.selected_language_var = tk.StringVar()
        self.selected_file_var = tk.StringVar()
        
        # Widgets (seront créés par create_widgets)
        self.project_entry = None
        self.project_info_label = None
        self.language_combo = None
        self.language_status_label = None
        self.file_combo = None
        self.file_status_label = None
        self.mode_indicator_label = None  # NOUVEAU
        
        # Données
        self.available_languages = []
        self.available_files = []
        self.exclusions = []
        
        # Créer l'interface
        self.create_widgets()
        
        # Initialiser si projet fourni
        if initial_project_path:
            self._validate_and_set_project(initial_project_path)

    def _set_project_info(self, text, fg=None):
        """Met à jour le label projet uniquement s'il existe (show_project_input=True)."""
        try:
            if hasattr(self, "project_info_label") and self.project_info_label is not None:
                kwargs = {"text": text}
                if fg is not None:
                    kwargs["fg"] = fg
                self.project_info_label.config(**kwargs)
        except Exception:
            pass

    def create_widgets(self):
        """Crée tous les widgets du sélecteur avec layout amélioré et mode dual"""
        theme = theme_manager.get_theme()
        
        # === SÉLECTION DU PROJET (CONDITIONNELLE) ===
        if self.show_project_input:
            project_frame = tk.Frame(self.parent_frame, bg=theme["bg"])
            project_frame.pack(fill='x', padx=15, pady=(10, 5))
            
            project_label = tk.Label(
                project_frame,
                text="🎮 Projet :",
                font=('Segoe UI', 10, 'bold'),
                bg=theme["bg"],
                fg=theme["fg"],
                width=12,
                anchor='e'
            )
            project_label.pack(side='left')
            
            # Entry avec événements intelligents
            self.project_entry = tk.Entry(
                project_frame,
                textvariable=self.project_var,
                font=('Segoe UI', 10),
                bg=theme["bg"],
                fg=theme["fg"],
                insertbackground=theme["fg"]
            )
            self.project_entry.pack(side='left', padx=(10, 5), fill='x', expand=True)
            
            # Événements pour saisie intelligente
            self.project_entry.bind('<KeyRelease>', self._on_project_path_changed)
            self.project_entry.bind('<FocusOut>', self._on_project_path_changed)
            
            # NOUVEAU : Bouton Scanner unique
            refresh_btn = tk.Button(
                project_frame,
                text="🔄 Scanner",
                command=self._refresh_all,
                bg=theme["button_utility_bg"],
                fg="#000000",
                font=('Segoe UI', 9),
                pady=4,
                padx=8,
                width=10
            )
            refresh_btn.pack(side='right', padx=(5, 5))
            
            # NOUVEAU : Bouton Fichier unique
            file_btn = tk.Button(
                project_frame,
                text="📄 Fichier",
                command=self._browse_single_file,
                bg=theme["button_nav_bg"],
                fg="#000000",
                font=('Segoe UI', 9),
                pady=4,
                padx=8,
                width=8
            )
            file_btn.pack(side='right', padx=(2, 2))
            
            # Bouton Parcourir projet (existant)
            project_btn = tk.Button(
                project_frame,
                text="📁 Projet",
                command=self._browse_project,
                bg=theme["button_nav_bg"],
                fg="#000000",
                font=('Segoe UI', 9),
                pady=4,
                padx=8,
                width=8
            )
            project_btn.pack(side='right')
            
            # NOUVEAU : Indicateur de mode
            mode_frame = tk.Frame(self.parent_frame, bg=theme["bg"])
            mode_frame.pack(fill='x', padx=15, pady=(2, 5))
            
            self.mode_indicator_label = tk.Label(
                mode_frame,
                text="🔧 Mode : Projet complet",
                font=('Segoe UI', 9, 'bold'),
                bg=theme["bg"],
                fg='#3498db'
            )
            self.mode_indicator_label.pack(anchor='w')
            
            # Info projet (modifié pour inclure info fichier unique)
            self.project_info_label = tk.Label(
                self.parent_frame,
                text="📊 Aucun projet sélectionné",
                font=('Segoe UI', 9, 'italic'),
                bg=theme["bg"],
                fg='#2980B9'
            )
            self.project_info_label.pack(anchor='w', padx=15, pady=(2, 10))
        
        # === SÉLECTION LANGUE ET FICHIER CÔTE À CÔTE ===
        selection_frame = tk.Frame(self.parent_frame, bg=theme["bg"])
        selection_frame.pack(fill='x', padx=15, pady=5)
        
        # Colonne gauche - Langue
        lang_column = tk.Frame(selection_frame, bg=theme["bg"])
        lang_column.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        lang_row = tk.Frame(lang_column, bg=theme["bg"])
        lang_row.pack(fill='x', pady=2)
        
        language_label = tk.Label(
            lang_row,
            text="🌍 Langue :",
            font=('Segoe UI', 10, 'bold'),
            bg=theme["bg"],
            fg=theme["fg"],
            width=12,
            anchor='e'
        )
        language_label.pack(side='left')
        
        self.language_combo = ttk.Combobox(
            lang_row,
            textvariable=self.selected_language_var,
            width=20,
            state='readonly'
        )
        self.language_combo.pack(side='left', padx=(10, 5), fill='x', expand=True)
        self.language_combo.bind('<<ComboboxSelected>>', self._on_language_selected)
        
        # Colonne droite - Fichier
        file_column = tk.Frame(selection_frame, bg=theme["bg"])
        file_column.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        file_row = tk.Frame(file_column, bg=theme["bg"])
        file_row.pack(fill='x', pady=2)
        
        files_label = tk.Label(
            file_row,
            text="📄 Fichier :",
            font=('Segoe UI', 10, 'bold'),
            bg=theme["bg"],
            fg=theme["fg"],
            width=12,
            anchor='e'
        )
        files_label.pack(side='left')
        
        self.file_combo = ttk.Combobox(
            file_row,
            textvariable=self.selected_file_var,
            width=20,
            state='readonly'
        )
        self.file_combo.pack(side='left', padx=(10, 5), fill='x', expand=True)
        self.file_combo.bind('<<ComboboxSelected>>', self._on_file_selected)
        
        # === STATUTS CÔTE À CÔTE ===
        status_frame = tk.Frame(self.parent_frame, bg=theme["bg"])
        status_frame.pack(fill='x', padx=15, pady=(2, 10))
        
        # Statut langues (gauche)
        lang_status_column = tk.Frame(status_frame, bg=theme["bg"])
        lang_status_column.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        self.language_status_label = tk.Label(
            lang_status_column,
            text="📋 Projet non configuré - Cliquez sur 'Scanner'",
            font=('Segoe UI', 9, 'italic'),
            bg=theme["bg"],
            fg='#666666'
        )
        self.language_status_label.pack(anchor='w')
        
        # Statut fichiers (droite)
        file_status_column = tk.Frame(status_frame, bg=theme["bg"])
        file_status_column.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        self.file_status_label = tk.Label(
            file_status_column,
            text="📋 Sélectionnez une langue pour voir les fichiers",
            font=('Segoe UI', 9, 'italic'),
            bg=theme["bg"],
            fg='#666666'
        )
        self.file_status_label.pack(anchor='w')

    # ============================================================================
    # NOUVELLES MÉTHODES POUR MODE DUAL
    # ============================================================================
    
    def _browse_single_file(self):
        """Ouvre la boîte de dialogue pour sélectionner UN fichier unique"""
        from tkinter import filedialog
        from infrastructure.config.config import config_manager
        
        initial_dir = config_manager.get('last_directory', '.')
        
        file_path = filedialog.askopenfilename(
            title='Sélectionner un fichier .rpy',
            initialdir=initial_dir,
            filetypes=[
                ('Fichiers Ren\'Py', '*.rpy'),
                ('Tous les fichiers', '*.*')
            ]
        )
        
        if file_path:
            self._set_single_file_mode(file_path)
    
    def _set_single_file_mode(self, file_path):
        """Bascule en mode fichier unique avec le fichier spécifié"""
        try:
            if not os.path.exists(file_path):
                self._set_project_info("❌ Fichier inexistant", fg="#ff8379")
                return
            
            # NOUVEAU : Validation du contenu du fichier
            from core.services.extraction.validation import validate_file_for_translation_processing
            validation_result = validate_file_for_translation_processing(file_path)
            
            if not validation_result['overall_valid']:
                # Fichier refusé : afficher le détail (ce qui a coincé) dans un popup
                filename = os.path.basename(file_path)
                self._set_project_info(
                    f"❌ Fichier refusé : {filename}",
                    fg="#ff8379"
                )
                self.language_status_label.config(
                    text="❌ Ce fichier ne contient pas de traductions valides",
                    fg='#ff8379'
                )
                self.file_status_label.config(
                    text="💡 Fichier .rpy avec blocs 'translate <langue> <id>:' ou 'translate <langue> strings:'",
                    fg='#ff8379'
                )
                details = validation_result.get('rejection_details') or []
                details_text = "\n• ".join(details) if details else "Aucun détail."
                try:
                    from infrastructure.helpers.unified_functions import show_translated_messagebox
                    parent_win = self.parent_frame.winfo_toplevel() if self.parent_frame else None
                    show_translated_messagebox(
                        'info',
                        f"Fichier refusé : {filename}",
                        f"Ce qui a coincé :\n\n• {details_text}",
                        parent=parent_win
                    )
                except Exception as e:
                    log_message("ATTENTION", f"Popup détail rejet: {e}", category="project_widgets")
                log_message("INFO", f"Fichier refusé en mode unique : {filename}", category="project_widgets")
                return
            
            # Basculer en mode fichier unique (code existant)
            self.current_mode = "single_file"
            self.single_file_path = file_path
            
            # Mettre à jour l'indicateur de mode
            if self.mode_indicator_label:
                self.mode_indicator_label.config(
                    text="🔧 Mode : Fichier unique",
                    fg='#9b59b6'
                )
            
            # Mettre à jour l'entry avec le chemin du fichier
            self.project_var.set(file_path)
            
            # Mettre à jour les informations
            filename = os.path.basename(file_path)
            file_dir = os.path.dirname(file_path)
            self._set_project_info(f"📄 Fichier de traduction : {filename} (dans {os.path.basename(file_dir)})", fg="#9b59b6")
            
            # Désactiver les combos langue/fichier en mode fichier unique
            self.language_combo.configure(state='disabled')
            self.file_combo.configure(state='disabled')
            self.selected_language_var.set("N/A (fichier unique)")
            self.selected_file_var.set(filename)
            
            # Mettre à jour les statuts
            self.language_status_label.config(
                text="📄 Mode fichier unique - Sélection de langue non applicable",
                fg='#9b59b6'
            )
            self.file_status_label.config(
                text="📄 Fichier unique sélectionné",
                fg='#9b59b6'
            )
            
            # Sauvegarder le répertoire
            from infrastructure.config.config import config_manager
            try:
                config_manager.set('last_directory', os.path.dirname(file_path))
            except Exception:
                pass
            
            # Déclencher les callbacks
            if self.on_project_changed:
                try:
                    self.on_project_changed(file_path)  # Envoyer le fichier comme "projet"
                except Exception:
                    pass
            
            if self.on_language_changed:
                try:
                    self.on_language_changed("single_file")
                except Exception:
                    pass
            
            # Créer une sélection de fichiers pour le mode unique
            if self.on_files_changed:
                try:
                    selection_info = {
                        'project_path': file_path,
                        'language': 'single_file',
                        'selected_option': filename,
                        'is_all_files': False,
                        'is_single_file_mode': True,  # NOUVEAU FLAG
                        'available_files': [{
                            'name': filename,
                            'path': file_path,
                            'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0
                        }],
                        'target_files': [{
                            'name': filename,
                            'path': file_path,
                            'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0
                        }],
                        'file_paths': [file_path]
                    }
                    self.on_files_changed(selection_info)
                except Exception:
                    pass
            
            log_message("INFO", f"Mode fichier unique activé : {filename}", category="project_widgets")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur mode fichier unique: {e}", category="project_widgets")
            self._set_project_info("❌ Erreur lors de la sélection du fichier", fg="#ff8379")

    def _find_project_root_from_subdir(self, path):
        """Remonte dans l'arborescence pour trouver la racine du projet Ren'Py"""
        try:
            current_dir = path
            max_levels = 5  # Limite pour éviter de remonter trop haut
            
            for _ in range(max_levels):
                # Vérifier si le dossier actuel est un projet Ren'Py valide
                if validate_renpy_project(current_dir):
                    return current_dir
                
                # Remonter d'un niveau
                parent_dir = os.path.dirname(current_dir)
                
                # Si on atteint la racine du système, arrêter
                if parent_dir == current_dir:
                    break
                    
                current_dir = parent_dir
            
            return None
            
        except Exception as e:
            log_message("DEBUG", f"Erreur recherche racine projet: {e}", category="project_widgets")
            return None

    def _switch_to_project_mode(self):
        """Bascule vers le mode projet (réactive les fonctionnalités normales)"""
        try:
            self.current_mode = "project"
            self.single_file_path = ""
            
            # Mettre à jour l'indicateur de mode
            if self.mode_indicator_label:
                self.mode_indicator_label.config(
                    text="🔧 Mode : Projet complet",
                    fg='#3498db'
                )
            
            # Réactiver les combos
            self.language_combo.configure(state='readonly')
            self.file_combo.configure(state='readonly')
            
            # Remettre les statuts par défaut
            self.language_status_label.config(
                text="📋 Projet non configuré - Cliquez sur 'Scanner'",
                fg='#666666'
            )
            self.file_status_label.config(
                text="📋 Sélectionnez une langue pour voir les fichiers",
                fg='#666666'
            )
            
            # Vider les sélections
            self.selected_language_var.set("")
            self.selected_file_var.set("")
            self.language_combo['values'] = []
            self.file_combo['values'] = []
            
            log_message("INFO", "Mode projet réactivé", category="project_widgets")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur retour mode projet: {e}", category="project_widgets")

    # ============================================================================
    # MÉTHODES MODIFIÉES POUR GÉRER LE MODE DUAL
    # ============================================================================

    def _refresh_all(self):
        """Actualise langues ET fichiers (uniquement en mode projet)"""
        try:
            if self.current_mode == "single_file":
                # En mode fichier unique, le refresh bascule vers le mode projet
                self._switch_to_project_mode()
                self._set_project_info("📊 Mode projet activé - Spécifiez un dossier projet", fg="#2980B9")
                return
            
            # CORRECTION: Forcer le rafraîchissement pour détecter les changements manuels
            self._scan_languages(force_refresh=True)
            self._scan_files()
            
            log_message("INFO", "Scan manuel déclenché", category="project_widgets")
        except Exception as e:
            log_message("ERREUR", f"Erreur scan manuel: {e}", category="project_widgets")
    
    def _browse_project(self):
        """Ouvre la boîte de dialogue pour sélectionner un projet (bascule en mode projet)"""
        from tkinter import filedialog
        from infrastructure.config.config import config_manager
        
        # Forcer le passage en mode projet
        if self.current_mode == "single_file":
            self._switch_to_project_mode()
        
        initial_dir = config_manager.get('last_directory', '.')
        
        project_path = filedialog.askdirectory(
            title='Sélectionner le dossier du projet Ren\'Py',
            initialdir=initial_dir
        )
        
        if project_path:
            self._validate_and_set_project(project_path)
    
    def _on_project_path_changed(self, event=None):
        """Appelé lors de la saisie manuelle du chemin"""
        path = self.project_var.get().strip()
        
        if not path:
            return
        
        if os.path.exists(path):
            if os.path.isfile(path):
                # C'est un fichier - basculer en mode fichier unique
                self._set_single_file_mode(path)
            elif os.path.isdir(path):
                # C'est un dossier - basculer en mode projet
                if self.current_mode == "single_file":
                    self._switch_to_project_mode()
                self._validate_and_set_project(path)
    
    def _validate_and_set_project(self, project_path, force_refresh=False):
        """Valide et définit le projet actuel avec remontée intelligente"""
        try:
            if hasattr(self, '_updating_project') and self._updating_project:
                return
            
            self._updating_project = True
            
            try:
                # Forcer le mode projet
                if self.current_mode == "single_file":
                    self._switch_to_project_mode()
                
                # Vérifier d'abord si c'est directement un projet valide
                if validate_renpy_project(project_path):
                    actual_project_path = project_path
                else:
                    # Essayer de remonter pour trouver la racine du projet
                    actual_project_path = self._find_project_root_from_subdir(project_path)
                    
                    if actual_project_path:
                        log_message("INFO", f"Projet parent trouvé: {actual_project_path} (depuis {project_path})", category="project_widgets")
                    else:
                        self._set_project_info("❌ Dossier invalide - Aucun projet Ren'Py trouvé dans l'arborescence", fg="#ff8379")
                        return

                # Projet valide trouvé
                self.current_project_path = actual_project_path
                self.project_var.set(actual_project_path)

                # Info projet avec indication si remontée effectuée
                info_text = get_project_info_summary(actual_project_path)
                if actual_project_path != project_path:
                    info_prefix = "🔍 Projet parent détecté: "
                else:
                    info_prefix = "✅ "
                
                self._set_project_info(f"{info_prefix}{info_text}", fg=theme_manager.get_theme().get("fg", "#ffffff"))

                # Reste du code existant...
                from infrastructure.config.config import config_manager
                try:
                    config_manager.set('last_directory', os.path.dirname(actual_project_path))
                except Exception:
                    pass

                if self.on_project_changed:
                    try:
                        self.on_project_changed(actual_project_path)
                    except Exception:
                        pass

                self._scan_languages(force_refresh=force_refresh)
                self._scan_files()

                log_message("INFO", f"Projet défini: {os.path.basename(actual_project_path)}", category="project_widgets")
                
            finally:
                self._updating_project = False
                
        except Exception as e:
            self._updating_project = False
            log_message("ERREUR", f"Erreur validation projet: {e}", category="project_widgets")
            self._set_project_info("❌ Erreur lors de la validation", fg="#ff8379")

    # ============================================================================
    # GESTION DU DRAG & DROP MODIFIÉE
    # ============================================================================
    
    def handle_dropped_path(self, dropped_path):
        """Gère le drag & drop avec validation pour les fichiers uniques"""
        try:
            if not os.path.exists(dropped_path):
                log_message("ATTENTION", f"Chemin droppé inexistant: {dropped_path}", category="project_widgets")
                return False
            
            if os.path.isfile(dropped_path):
                if dropped_path.endswith('.rpy'):
                    # Valider le fichier avant de l'accepter
                    from core.services.extraction.validation import validate_file_for_translation_processing
                    validation_result = validate_file_for_translation_processing(dropped_path)
                    
                    if validation_result['overall_valid']:
                        self._set_single_file_mode(dropped_path)
                        return True
                    else:
                        # Fichier refusé : popup avec détail (ce qui a coincé)
                        filename = os.path.basename(dropped_path)
                        self._set_project_info(
                            f"❌ Fichier refusé : {filename}",
                            fg="#ff8379"
                        )
                        details = validation_result.get('rejection_details') or []
                        details_text = "\n• ".join(details) if details else "Aucun détail."
                        try:
                            from infrastructure.helpers.unified_functions import show_translated_messagebox
                            parent_win = self.parent_frame.winfo_toplevel() if self.parent_frame else None
                            show_translated_messagebox(
                                'info',
                                f"Fichier refusé : {filename}",
                                f"Ce qui a coincé :\n\n• {details_text}",
                                parent=parent_win
                            )
                        except Exception as e:
                            log_message("ATTENTION", f"Popup détail rejet: {e}", category="project_widgets")
                        log_message("INFO", f"Fichier refusé via drag & drop : {filename}", category="project_widgets")
                        return False
                else:
                    log_message("ATTENTION", f"Type de fichier non supporté: {dropped_path}", category="project_widgets")
                    return False
            
            elif os.path.isdir(dropped_path):
                # Essayer de traiter comme un projet (avec remontée intelligente)
                self._validate_and_set_project(dropped_path)
                return True
            
            return False
            
        except Exception as e:
            log_message("ERREUR", f"Erreur traitement drop: {e}", category="project_widgets")
            return False

    # ============================================================================
    # MÉTHODES EXISTANTES (Scan langues/fichiers, etc.) - MODE PROJET UNIQUEMENT
    # ============================================================================
    
    def _scan_languages(self, force_refresh=False):
        """Scanne les langues disponibles (mode projet uniquement)"""
        if self.current_mode == "single_file":
            return  # Pas de scan en mode fichier unique
            
        try:
            if not self.current_project_path:
                if getattr(self, "language_status_label", None):
                    self.language_status_label.config(text="❌ Aucun projet sélectionné", fg="#ff8379")
                return

            self.available_languages = scan_project_languages(self.current_project_path, force_refresh=force_refresh)

            if not self.available_languages:
                if getattr(self, "language_status_label", None):
                    self.language_status_label.config(text="ℹ️ Aucune langue avec fichiers .rpy trouvée", fg="#666666")
                if getattr(self, "language_combo", None):
                    self.language_combo['values'] = []
                if getattr(self, "selected_language_var", None):
                    self.selected_language_var.set("")
                return

            lang_names = [lang['name'] for lang in self.available_languages]
            if getattr(self, "language_combo", None):
                self.language_combo['values'] = lang_names

            # Sélection : 'french' si dispo, sinon 1ère
            default_lang = 'french' if 'french' in lang_names else lang_names[0]
            if getattr(self, "selected_language_var", None):
                self.selected_language_var.set(default_lang)

            total_files = sum(lang['file_count'] for lang in self.available_languages)
            if getattr(self, "language_status_label", None):
                self.language_status_label.config(
                    text=f"✅ {len(self.available_languages)} langue(s) trouvée(s) - {total_files} fichiers .rpy au total",
                    fg=theme_manager.get_theme().get("fg", "#ffffff")
                )

            # Callback langue, puis scan fichiers
            if self.on_language_changed:
                try: self.on_language_changed(default_lang)
                except Exception: pass

            self._scan_files()

        except Exception as e:
            log_message("ERREUR", f"Erreur scan langues: {e}", category="project_widgets")
            if getattr(self, "language_status_label", None):
                self.language_status_label.config(text="❌ Erreur lors du scan des langues", fg="#ff8379")
    
    def _on_language_selected(self, event=None):
        """Appelé quand une langue est sélectionnée (mode projet uniquement)"""
        if self.current_mode == "single_file":
            return
            
        selected_language = self.selected_language_var.get()
        if selected_language:
            if self.on_language_changed:
                self.on_language_changed(selected_language)
            self._scan_files()
    
    def _scan_files(self):
        """Scanne les fichiers de la langue sélectionnée (mode projet uniquement)"""
        if self.current_mode == "single_file":
            return
            
        try:
            selected_language = self.selected_language_var.get()
            if not self.current_project_path or not selected_language:
                # CORRECTION: Nettoyer la liste des fichiers quand pas de langue sélectionnée
                self.available_files = []
                self.file_combo['values'] = []
                self.selected_file_var.set("")
                self.file_status_label.config(
                    text="📋 Sélectionnez une langue pour voir les fichiers",
                    fg='#666666'
                )
                return
            
            self.available_files = scan_language_files(
                self.current_project_path,
                selected_language,
                self.exclusions,
                force_refresh=True  # ✅ AJOUT : Forcer le refresh pour détecter les nouveaux fichiers
            )
            
            if not self.available_files:
                self.file_status_label.config(
                    text="ℹ️ Aucun fichier .rpy trouvé dans cette langue",
                    fg='#666666'
                )
                self.file_combo['values'] = []
                self.selected_file_var.set("")
                return
            
            # Construire les options: "Tous" + fichiers individuels
            file_options = ["Tous les fichiers"]
            file_options.extend([f['name'] for f in self.available_files])
            
            self.file_combo['values'] = file_options
            
            # ✅ CORRECTION : Sélectionner "Tous les fichiers" par défaut pour activer la navigation
            if len(self.available_files) > 0:
                # Sélectionner "Tous les fichiers" pour permettre la navigation entre fichiers
                self.selected_file_var.set("Tous les fichiers")
            else:
                # Fallback vers "Tous les fichiers" si aucun fichier individuel
                self.selected_file_var.set("Tous les fichiers")
            
            # Mettre à jour le statut
            self.file_status_label.config(
                text=f"✅ {len(self.available_files)} fichier(s) disponible(s) (exclusions appliquées)",
                fg=theme_manager.get_theme()["fg"]
            )
            
            # Déclencher le callback
            self._on_file_selected()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur scan fichiers: {e}", category="project_widgets")
            self.file_status_label.config(
                text="❌ Erreur lors du scan des fichiers",
                fg='#ff8379'
            )
    
    def _on_file_selected(self, event=None):
        """Appelé quand une sélection de fichier change (mode projet uniquement)"""
        if self.current_mode == "single_file":
            return
            
        try:
            selected_file = self.selected_file_var.get()
            if not selected_file:
                return
            
            # Préparer les infos de sélection
            selection_info = {
                'project_path': self.current_project_path,
                'language': self.selected_language_var.get(),
                'selected_option': selected_file,
                'is_all_files': (selected_file == "Tous les fichiers"),
                'is_single_file_mode': False,
                'available_files': self.available_files.copy()
            }
            
            if selection_info['is_all_files']:
                selection_info['target_files'] = self.available_files.copy()
                selection_info['file_paths'] = [f['path'] for f in self.available_files]
            else:
                # Fichier spécifique
                target_file = next((f for f in self.available_files if f['name'] == selected_file), None)
                if target_file:
                    selection_info['target_files'] = [target_file]
                    selection_info['file_paths'] = [target_file['path']]
                else:
                    selection_info['target_files'] = []
                    selection_info['file_paths'] = []
            
            # Callback
            if self.on_files_changed:
                self.on_files_changed(selection_info)
                
        except Exception as e:
            log_message("ERREUR", f"Erreur sélection fichier: {e}", category="project_widgets")
    
    # ============================================================================
    # MÉTHODES D'ACCÈS POUR COMPATIBILITÉ
    # ============================================================================
    
    def get_current_selection(self) -> dict:
        """Retourne la sélection actuelle selon le mode"""
        if self.current_mode == "single_file":
            # Mode fichier unique
            filename = os.path.basename(self.single_file_path)
            return {
                'project_path': self.single_file_path,
                'language': 'single_file',
                'selected_option': filename,
                'is_all_files': False,
                'is_single_file_mode': True,
                'available_files': [{
                    'name': filename,
                    'path': self.single_file_path,
                    'size': os.path.getsize(self.single_file_path) if os.path.exists(self.single_file_path) else 0
                }],
                'target_files': [{
                    'name': filename,
                    'path': self.single_file_path,
                    'size': os.path.getsize(self.single_file_path) if os.path.exists(self.single_file_path) else 0
                }],
                'file_paths': [self.single_file_path]
            }
        else:
            # Mode projet (code existant)
            selection_info = {
                'project_path': self.current_project_path,
                'language': self.selected_language_var.get(),
                'selected_option': self.selected_file_var.get(),
                'is_all_files': (self.selected_file_var.get() == "Tous les fichiers"),
                'is_single_file_mode': False,
                'available_files': self.available_files.copy()
            }
            
            if selection_info['is_all_files']:
                selection_info['target_files'] = self.available_files.copy()
                selection_info['file_paths'] = [f['path'] for f in self.available_files]
            else:
                target_file = next((f for f in self.available_files if f['name'] == self.selected_file_var.get()), None)
                if target_file:
                    selection_info['target_files'] = [target_file]
                    selection_info['file_paths'] = [target_file['path']]
                else:
                    selection_info['target_files'] = []
                    selection_info['file_paths'] = []
            
            return selection_info

    # ============================================================================
    # MÉTHODES UTILITAIRES ET COMPATIBILITÉ
    # ============================================================================
    
    def set_exclusions(self, exclusions_str: str):
        """Définit les exclusions à appliquer (mode projet uniquement)"""
        if self.current_mode == "single_file":
            return  # Pas d'exclusions en mode fichier unique
            
        self.exclusions = parse_exclusions_string(exclusions_str)
        
        # Re-scanner les fichiers si une langue est sélectionnée
        if self.selected_language_var.get():
            self._scan_files()
    
    def refresh_languages(self, force_refresh=True):
        """Rafraîchit la liste des langues disponibles (mode projet uniquement)"""
        if self.current_mode == "single_file":
            return  # Pas de refresh en mode fichier unique
        
        if self.current_project_path:
            self._scan_languages(force_refresh=force_refresh)
            self._scan_files()
    
    def get_selection_summary(self) -> str:
        """Retourne un résumé de la sélection actuelle selon le mode"""
        try:
            if self.current_mode == "single_file":
                filename = os.path.basename(self.single_file_path)
                file_dir = os.path.basename(os.path.dirname(self.single_file_path))
                return f"Fichier unique: {filename} (dans {file_dir})"
            
            # Mode projet (code existant)
            if not self.current_project_path:
                return "Aucune sélection"
            
            project_name = os.path.basename(self.current_project_path)
            language = self.selected_language_var.get()
            file_selection = self.selected_file_var.get()
            
            if not language:
                return f"Projet: {project_name} (aucune langue)"
            
            if not file_selection:
                return f"Projet: {project_name} • Langue: {language} (aucun fichier)"
            
            if file_selection == "Tous les fichiers":
                return f"Projet: {project_name} • Langue: {language} • Tous les fichiers ({len(self.available_files)})"
            else:
                return f"Projet: {project_name} • Langue: {language} • Fichier: {file_selection}"
                
        except Exception:
            return "Sélection incomplète"
    
    def get_current_mode(self) -> str:
        """Retourne le mode actuel ('project' ou 'single_file')"""
        return self.current_mode
    
    def is_single_file_mode(self) -> bool:
        """Retourne True si en mode fichier unique"""
        return self.current_mode == "single_file"
    
    def get_single_file_path(self) -> str:
        """Retourne le chemin du fichier unique (si en mode fichier unique)"""
        return self.single_file_path if self.current_mode == "single_file" else ""
    
    def apply_theme(self):
        """Applique le thème au ProjectLanguageSelector"""
        try:
            theme = theme_manager.get_theme()
            
            # Frame parent principal
            if hasattr(self, 'parent_frame'):
                self.parent_frame.configure(bg=theme["bg"])
            
            # Tous les frames enfants
            if hasattr(self, 'parent_frame'):
                for child in self.parent_frame.winfo_children():
                    if isinstance(child, tk.Frame):
                        child.configure(bg=theme["bg"])
                        
                        # Frames petits-enfants
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Frame):
                                grandchild.configure(bg=theme["bg"])
            
            # Tous les labels
            for child in self.parent_frame.winfo_children():
                self._apply_theme_recursive(child, theme)
            
            # Entry du projet (si show_project_input=True)
            if hasattr(self, 'project_entry') and self.project_entry:
                self.project_entry.configure(
                    bg=theme["bg"],
                    fg=theme["fg"],
                    insertbackground=theme["fg"]
                )
            
            # Labels d'info projet et mode
            for label_attr in ['project_info_label', 'mode_indicator_label']:
                if hasattr(self, label_attr):
                    label = getattr(self, label_attr)
                    if label:
                        label.configure(bg=theme["bg"], fg=theme["fg"])
            
            # Labels de statut
            for label_attr in ['language_status_label', 'file_status_label']:
                if hasattr(self, label_attr):
                    label = getattr(self, label_attr)
                    if label:
                        label.configure(bg=theme["bg"], fg='#666666')
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur apply_theme ProjectLanguageSelector: {e}", category="ui_theme")

    def _apply_theme_recursive(self, widget, theme):
        """Applique le thème récursivement"""
        try:
            if isinstance(widget, tk.Label):
                widget.configure(bg=theme["bg"], fg=theme["fg"])
            elif isinstance(widget, tk.Frame):
                widget.configure(bg=theme["bg"])
            elif isinstance(widget, tk.Button):
                # Garder les couleurs des boutons personnalisés
                pass
            
            # Récursion sur les enfants
            for child in widget.winfo_children():
                self._apply_theme_recursive(child, theme)
        except Exception:
            pass