# ui/dialogs/exclusions_manager_dialog.py
# Gestionnaire d'exclusions de lignes pour la cohérence

"""
Fenêtre modale pour gérer les exclusions de lignes de cohérence.
Permet de voir, filtrer et supprimer les exclusions ajoutées via le rapport HTML interactif.
"""

import tkinter as tk
from tkinter import ttk
import os
from pathlib import Path

from ui.themes import theme_manager
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import show_custom_messagebox


class ExclusionsManagerDialog:
    """Fenêtre modale de gestion des exclusions"""
    
    def __init__(self, parent):
        """
        Initialise la fenêtre de gestion des exclusions
        
        Args:
            parent: Fenêtre parent (tk.Tk ou tk.Toplevel)
        """
        self.parent = parent
        self.theme = theme_manager.get_theme()
        
        # Créer la fenêtre modale
        self.window = tk.Toplevel(parent)
        self.window.title("⚙️ Gestion des Exclusions de Cohérence")
        self.window.geometry("1000x600")
        self.window.minsize(800, 500)
        self.window.configure(bg=self.theme["bg"])
        
        # Rendre la fenêtre modale
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centrer la fenêtre
        self._center_window()
        
        # Variables
        self.current_project_filter = tk.StringVar(value="Tous les projets")
        self.current_file_filter = tk.StringVar(value="Tous les fichiers")  # Nouveau filtre par fichier
        self.exclusions_data = {}  # {project_path: [exclusions]}
        self.tree_items = {}  # {item_id: (project, index)}
        self.project_filter_map = {}  # {display_name: set(project_paths)}
        self.file_filter_map = {}  # {display_name: set(file_paths)}
        self.project_display_names = {}  # Cache le nom affiché par projet
        
        # Système de sélection multiple par checkbox
        self.selected_items = {}  # {item_id: True/False}
        self.select_all_var = tk.BooleanVar(value=False)
        
        # Créer l'interface
        self._create_ui()
        
        # Charger les exclusions
        self._load_exclusions()
        
        # Gestion de la fermeture
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        log_message("INFO", "Gestionnaire d'exclusions initialisé", category="exclusions_manager")
    
    def _center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def _normalize_path(self, path):
        """Normalise un chemin (séparateurs)."""
        if not isinstance(path, str):
            return ""
        return path.replace('\\', '/').strip()
    
    def _get_project_display_name(self, project_path):
        """Retourne le nom du projet à afficher, quelle que soit la source."""
        normalized = self._normalize_path(project_path)
        if not normalized:
            return "Projet inconnu"
        
        normalized = normalized.rstrip('/')
        normalized_lower = normalized.lower()

        # Cas direct : le chemin existe et contient un dossier game → racine de projet probable
        try:
            path_obj = Path(normalized)
            if path_obj.exists() and (path_obj / "game").exists():
                direct_name = path_obj.name
                if direct_name:
                    return direct_name
        except Exception:
            pass

        # Fallback basé sur les projets actifs mémorisés en configuration
        candidate_paths = [
            config_manager.get('current_renpy_project', ''),
            config_manager.get('current_project', ''),
            config_manager.get('current_maintenance_project', '')
        ]

        seen = set()
        for candidate in candidate_paths:
            if not candidate or candidate in seen:
                continue
            seen.add(candidate)

            candidate_norm = self._normalize_path(candidate).rstrip('/')
            if not candidate_norm:
                continue

            candidate_norm_lower = candidate_norm.lower()
            try:
                candidate_key = config_manager._normalize_project_key(candidate_norm)
            except Exception:
                candidate_key = candidate_norm

            candidate_key = self._normalize_path(candidate_key).rstrip('/')
            candidate_key_lower = candidate_key.lower()

            if candidate_key_lower == normalized_lower:
                name = os.path.basename(candidate_norm)
                if name:
                    return name

            if candidate_norm_lower.startswith(normalized_lower + '/'):
                name = os.path.basename(candidate_norm)
                if name:
                    return name

            if normalized_lower.startswith(candidate_norm_lower + '/'):
                name = os.path.basename(candidate_norm)
                if name:
                    return name
        
        # Si la clé correspond à un fichier (contient une extension .rpy)
        if normalized.endswith('.rpy'):
            # Rechercher un segment 'game' pour identifier la racine Ren'Py
            segments = normalized.split('/')
            try:
                game_index = next(i for i, seg in enumerate(segments) if seg.lower() == 'game')
                if game_index > 0:
                    return segments[game_index - 1]
            except StopIteration:
                pass
            # Fallback : prendre le deuxième élément (game_name/file.rpy)
            if len(segments) >= 2:
                return segments[-2]
            return segments[-1].replace('.rpy', '') or "Projet inconnu"
        
        # Tentative supplémentaire : extraire le nom via helper global
        try:
            from infrastructure.helpers.unified_functions import extract_game_name
            guessed_name = extract_game_name(normalized)
            if guessed_name and guessed_name != "Projet_Inconnu":
                return guessed_name
        except Exception:
            pass

        # Cas où la clé est un dossier complet
        base_name = os.path.basename(normalized.rstrip('/'))
        if base_name.lower() in ('game', 'tl'):
            parent = os.path.basename(os.path.dirname(normalized))
            return parent or base_name
        return base_name or "Projet inconnu"
    
    def _get_file_display_name(self, file_path):
        """Retourne un nom de fichier simplifié à afficher."""
        normalized = self._normalize_path(file_path)
        if not normalized:
            return "N/A"
        return os.path.basename(normalized)
    
    def _create_ui(self):
        """Crée l'interface de la fenêtre"""
        # === HEADER ===
        header_frame = tk.Frame(self.window, bg=self.theme["bg"])
        header_frame.pack(fill='x', padx=20, pady=15)
        
        tk.Label(
            header_frame,
            text="⚙️ Gestion des Exclusions de Lignes",
            font=('Segoe UI', 14, 'bold'),
            bg=self.theme["bg"],
            fg=self.theme["accent"]
        ).pack()
        
        tk.Label(
            header_frame,
            text="Gérez les lignes ignorées dans les rapports de cohérence",
            font=('Segoe UI', 9),
            bg=self.theme["bg"],
            fg=self.theme["fg"]
        ).pack(pady=(5, 0))
        
        # === FILTRES (2 COLONNES CÔTE À CÔTE) ===
        filters_frame = tk.Frame(self.window, bg=self.theme["bg"])
        filters_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        # Colonne gauche - Filtre par projet
        filter_project_column = tk.Frame(filters_frame, bg=self.theme["bg"])
        filter_project_column.pack(side='left', fill='x', expand=True, padx=(0, 15))
        
        tk.Label(
            filter_project_column,
            text="🎮 Filtrer par projet :",
            font=('Segoe UI', 9, 'bold'),
            bg=self.theme["bg"],
            fg=self.theme["fg"]
        ).pack(anchor='w', pady=(0, 5))
        
        self.project_filter_combo = ttk.Combobox(
            filter_project_column,
            textvariable=self.current_project_filter,
            state='readonly',
            font=('Segoe UI', 9),
            width=30
        )
        self.project_filter_combo.pack(anchor='w', fill='x', pady=(0, 5))
        self.project_filter_combo.bind('<<ComboboxSelected>>', lambda e: self._on_project_filter_changed())
        
        # Colonne droite - Filtre par fichier
        filter_file_column = tk.Frame(filters_frame, bg=self.theme["bg"])
        filter_file_column.pack(side='right', fill='x', expand=True, padx=(15, 0))
        
        tk.Label(
            filter_file_column,
            text="📄 Filtrer par fichier :",
            font=('Segoe UI', 9, 'bold'),
            bg=self.theme["bg"],
            fg=self.theme["fg"]
        ).pack(anchor='w', pady=(0, 5))
        
        self.file_filter_combo = ttk.Combobox(
            filter_file_column,
            textvariable=self.current_file_filter,
            state='readonly',
            font=('Segoe UI', 9),
            width=30
        )
        self.file_filter_combo.pack(anchor='w', fill='x', pady=(0, 5))
        self.file_filter_combo.bind('<<ComboboxSelected>>', lambda e: self._apply_filter())
        
        # === LISTE DES EXCLUSIONS (TREEVIEW) ===
        tree_frame = tk.Frame(self.window, bg=self.theme["bg"])
        tree_frame.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        
        # Scrollbars
        tree_scroll_y = tk.Scrollbar(tree_frame, orient='vertical')
        tree_scroll_y.pack(side='right', fill='y')
        
        tree_scroll_x = tk.Scrollbar(tree_frame, orient='horizontal')
        tree_scroll_x.pack(side='bottom', fill='x')
        
        # Treeview avec colonnes (ajout de 'select' pour checkbox)
        columns = ('select', 'project', 'file', 'line', 'text', 'date')
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            selectmode='extended'
        )
        
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        # Configuration des colonnes avec en-têtes centrés
        headings_config = [
            ('select', "☐", 40),  # Colonne de sélection
            ('project', "Projet", 180),
            ('file', "Fichier", 200),
            ('line', "Ligne", 60),
            ('text', "Texte exclu", 300),
            ('date', "Date d'ajout", 140)
        ]
        
        for col_id, col_text, col_width in headings_config:
            if col_id == 'select':
                # En-tête cliquable pour tout sélectionner/désélectionner
                self.tree.heading(col_id, 
                                text=col_text,
                                command=self._toggle_select_all,
                                anchor='center')
                self.tree.column(col_id, width=col_width, anchor='center', stretch=False)
            else:
                self.tree.heading(col_id, text=col_text, anchor='center')
                if col_id == 'line':
                    self.tree.column(col_id, width=col_width, minwidth=50, anchor='center', stretch=False)
                else:
                    self.tree.column(col_id, width=col_width, minwidth=100, anchor='w')
        
        self.tree.pack(fill='both', expand=True)
        
        # Bind pour cliquer sur une ligne et toggle la checkbox
        self.tree.bind('<Button-1>', self._on_tree_click)
        
        # === STATISTIQUES ===
        stats_frame = tk.Frame(self.window, bg=self.theme["bg"])
        stats_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        self.stats_label = tk.Label(
            stats_frame,
            text="",
            font=('Segoe UI', 9, 'italic'),
            bg=self.theme["bg"],
            fg=self.theme["fg"]
        )
        self.stats_label.pack(side='left')
        
        # === BOUTONS D'ACTION ===
        buttons_frame = tk.Frame(self.window, bg=self.theme["bg"])
        buttons_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # Boutons à gauche
        left_buttons = tk.Frame(buttons_frame, bg=self.theme["bg"])
        left_buttons.pack(side='left')
        
        tk.Button(
            left_buttons,
            text="🔄 Actualiser",
            command=self._refresh,
            bg=self.theme["button_secondary_bg"],
            fg="#000000",
            font=('Segoe UI', 9),
            padx=12,
            pady=6,
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=(0, 5))
        
        tk.Button(
            left_buttons,
            text="🗑️ Supprimer la sélection",
            command=self._delete_selected,
            bg=self.theme["button_danger_bg"],
            fg="#000000",
            font=('Segoe UI', 9),
            padx=12,
            pady=6,
            relief='flat',
            cursor='hand2'
        ).pack(side='left')
        
        # Bouton à droite
        tk.Button(
            buttons_frame,
            text="✅ Fermer",
            command=self._on_close,
            bg=self.theme["button_primary_bg"],
            fg="#000000",
            font=('Segoe UI', 9, 'bold'),
            padx=20,
            pady=6,
            relief='flat',
            cursor='hand2'
        ).pack(side='right')
    
    def _load_exclusions(self):
        """Charge toutes les exclusions depuis la config"""
        try:
            # Récupérer toutes les exclusions (dict par projet)
            self.exclusions_data = config_manager.get_coherence_exclusions()
            
            if not isinstance(self.exclusions_data, dict):
                self.exclusions_data = {}
                log_message("ATTENTION", "Exclusions mal formatées, réinitialisation", category="exclusions_manager")
            
            # Mettre à jour le filtre de projets
            self._update_project_filter()
            
            # Afficher les exclusions
            self._display_exclusions()
            
            log_message("INFO", f"Exclusions chargées: {len(self.exclusions_data)} projet(s)", category="exclusions_manager")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur chargement exclusions: {e}", category="exclusions_manager")
            show_custom_messagebox(
                'error',
                "❌ Erreur de chargement",
                f"Impossible de charger les exclusions:\n\n{e}",
                self.theme,
                parent=self.window
            )
    
    def _update_project_filter(self):
        """Met à jour la liste des projets dans le filtre"""
        try:
            projects = list(self.exclusions_data.keys())
            self.project_filter_map = {}
            self.project_display_names = {}
            
            for project_key in projects:
                display_name = self._get_project_display_name(project_key)
                self.project_display_names[project_key] = display_name
                if display_name not in self.project_filter_map:
                    self.project_filter_map[display_name] = set()
                self.project_filter_map[display_name].add(project_key)
            
            # Ajouter "Tous les projets" en premier
            project_values = ["Tous les projets"] + sorted(self.project_filter_map.keys(), key=str.lower)
            
            self.project_filter_combo['values'] = project_values
            
            # Sélectionner "Tous les projets" par défaut
            current_value = self.current_project_filter.get()
            if not current_value or current_value not in project_values:
                self.current_project_filter.set("Tous les projets")
                self.project_filter_combo.current(0)
            else:
                self.project_filter_combo.current(project_values.index(current_value))
            
            # Mettre à jour le filtre de fichiers
            self._update_file_filter()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur mise à jour filtre projets: {e}", category="exclusions_manager")
    
    def _update_file_filter(self):
        """Met à jour la liste des fichiers dans le filtre selon le projet sélectionné"""
        try:
            selected_project = self.current_project_filter.get()
            
            # Récupérer les fichiers selon le projet sélectionné
            self.file_filter_map = {}
            
            if selected_project == "Tous les projets":
                project_keys = self.exclusions_data.keys()
            else:
                project_keys = self.project_filter_map.get(selected_project, set())
            
            for project_path in project_keys:
                exclusions = self.exclusions_data.get(project_path, [])
                for exclusion in exclusions:
                    file_path = exclusion.get('file', '')
                    normalized_file_path = self._normalize_path(file_path)
                    if not normalized_file_path:
                        continue
                    display_name = self._get_file_display_name(normalized_file_path)
                    if display_name not in self.file_filter_map:
                        self.file_filter_map[display_name] = set()
                    self.file_filter_map[display_name].add(normalized_file_path)
            
            file_values = ["Tous les fichiers"] + sorted(self.file_filter_map.keys(), key=str.lower)
            
            self.file_filter_combo['values'] = file_values
            
            # Réinitialiser à "Tous les fichiers" quand on change de projet
            current_file_value = self.current_file_filter.get()
            if current_file_value not in file_values:
                self.current_file_filter.set("Tous les fichiers")
                self.file_filter_combo.current(0)
            else:
                self.file_filter_combo.current(file_values.index(current_file_value))
            
        except Exception as e:
            log_message("ERREUR", f"Erreur mise à jour filtre fichiers: {e}", category="exclusions_manager")
    
    def _on_project_filter_changed(self):
        """Callback quand le filtre de projet change"""
        try:
            # Mettre à jour le filtre de fichiers selon le nouveau projet
            self._update_file_filter()
            
            # Réinitialiser le filtre de fichiers à "Tous les fichiers"
            self.current_file_filter.set("Tous les fichiers")
            self.file_filter_combo.current(0)
            
            # Appliquer les filtres
            self._apply_filter()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur changement filtre projet: {e}", category="exclusions_manager")
    
    def _display_exclusions(self):
        """Affiche les exclusions dans le Treeview"""
        try:
            # Vider le Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            self.tree_items.clear()
            
            # Réinitialiser les sélections
            self.selected_items = {}
            self.select_all_var.set(False)
            self.tree.heading('select', text="☐")
            
            # Filtrer selon le projet et le fichier sélectionnés
            selected_project_filter = self.current_project_filter.get()
            selected_file_filter = self.current_file_filter.get()
            
            allowed_projects = None
            if selected_project_filter != "Tous les projets":
                allowed_projects = self.project_filter_map.get(selected_project_filter, set())
            
            allowed_files = None
            if selected_file_filter != "Tous les fichiers":
                allowed_files = self.file_filter_map.get(selected_file_filter, set())
            
            total_exclusions = 0
            visible_exclusions = 0
            
            for project_path, exclusions in self.exclusions_data.items():
                if allowed_projects is not None and project_path not in allowed_projects:
                    continue
                
                project_name = self.project_display_names.get(project_path) or self._get_project_display_name(project_path)
                self.project_display_names[project_path] = project_name
                
                for idx, exclusion in enumerate(exclusions):
                    total_exclusions += 1
                    
                    # Extraire les données
                    file_path = exclusion.get('file', 'N/A')
                    normalized_file_path = self._normalize_path(file_path)
                    file_display_name = self._get_file_display_name(normalized_file_path or file_path)
                    line = exclusion.get('line', 0)
                    text = exclusion.get('text', '')
                    date = exclusion.get('added_date', 'N/A')
                    
                    # Vérifier le filtre par fichier
                    if allowed_files is not None:
                        if not normalized_file_path or normalized_file_path not in allowed_files:
                            continue
                    
                    visible_exclusions += 1
                    
                    # Tronquer le texte si trop long
                    if len(text) > 80:
                        text = text[:77] + "..."
                    
                    # Créer un ID unique pour cette exclusion
                    normalized_project_key = project_path
                    normalized_file_for_id = normalized_file_path or file_path
                    item_unique_id = f"{normalized_project_key}|{normalized_file_for_id}|{line}"
                    
                    # Initialiser la sélection à False
                    self.selected_items[item_unique_id] = False
                    
                    # Ajouter à la Treeview avec checkbox
                    item_id = self.tree.insert(
                        '',
                        'end',
                        values=("☐", project_name, file_display_name, line, text, date),
                        tags=(item_unique_id,)
                    )
                    
                    # Stocker la référence
                    self.tree_items[item_id] = (project_path, idx)
            
            # Mettre à jour les statistiques
            filter_info = []
            if selected_project_filter != "Tous les projets":
                filter_info.append(f"projet: {selected_project_filter}")
            if selected_file_filter != "Tous les fichiers":
                filter_info.append(f"fichier: {selected_file_filter}")
            
            if filter_info:
                stats_text = f"📊 {visible_exclusions} exclusion(s) ({', '.join(filter_info)})"
            elif selected_project_filter == "Tous les projets":
                stats_text = f"📊 Total: {visible_exclusions} exclusion(s) dans {len(self.exclusions_data)} projet(s)"
            else:
                stats_text = f"📊 {visible_exclusions} exclusion(s)"
            
            self.stats_label.config(text=stats_text)
            
            log_message("INFO", f"Affichage: {visible_exclusions} exclusions", category="exclusions_manager")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur affichage exclusions: {e}", category="exclusions_manager")
            show_custom_messagebox(
                'error',
                "❌ Erreur d'affichage",
                f"Impossible d'afficher les exclusions:\n\n{e}",
                self.theme,
                parent=self.window
            )
    
    def _apply_filter(self):
        """Applique le filtre de projet"""
        self._display_exclusions()
    
    def _on_tree_click(self, event):
        """Gère le clic sur le TreeView pour toggle les checkboxes"""
        try:
            # Identifier la région cliquée
            region = self.tree.identify_region(event.x, event.y)
            if region != "cell":
                return
            
            # Identifier la ligne cliquée
            item = self.tree.identify_row(event.y)
            if not item:
                return
            
            # Récupérer l'ID unique depuis les tags
            item_tags = self.tree.item(item, 'tags')
            item_unique_id = item_tags[0] if item_tags else None
            
            if not item_unique_id:
                return
            
            # Toggle la sélection
            current_state = self.selected_items.get(item_unique_id, False)
            new_state = not current_state
            self.selected_items[item_unique_id] = new_state
            
            # Mettre à jour l'affichage
            current_values = list(self.tree.item(item, 'values'))
            current_values[0] = "☑" if new_state else "☐"
            self.tree.item(item, values=current_values)
            
            # Mettre à jour le compteur de sélection
            self._update_selection_count()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur toggle checkbox: {e}", category="exclusions_manager")
    
    def _toggle_select_all(self):
        """Sélectionne ou désélectionne tous les items"""
        try:
            # Inverser l'état de sélection globale
            new_state = not self.select_all_var.get()
            self.select_all_var.set(new_state)
            
            # Mettre à jour toutes les checkboxes
            for item in self.tree.get_children():
                item_tags = self.tree.item(item, 'tags')
                item_unique_id = item_tags[0] if item_tags else None
                
                if item_unique_id:
                    self.selected_items[item_unique_id] = new_state
                    
                    # Mettre à jour l'affichage
                    current_values = list(self.tree.item(item, 'values'))
                    current_values[0] = "☑" if new_state else "☐"
                    self.tree.item(item, values=current_values)
            
            # Mettre à jour le compteur
            self._update_selection_count()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur toggle select all: {e}", category="exclusions_manager")
    
    def _update_selection_count(self):
        """Met à jour l'affichage du nombre d'éléments sélectionnés"""
        try:
            selected_count = sum(1 for selected in self.selected_items.values() if selected)
            
            if selected_count > 0:
                self.stats_label.config(text=f"📌 {selected_count} exclusion(s) sélectionnée(s)")
            else:
                # Afficher les stats normales
                selected_project_filter = self.current_project_filter.get()
                selected_file_filter = self.current_file_filter.get()
                visible_exclusions = len([item for item in self.tree.get_children()])
                
                # Construire le texte des filtres actifs
                filter_info = []
                if selected_project_filter != "Tous les projets":
                    filter_info.append(f"projet: {selected_project_filter}")
                if selected_file_filter != "Tous les fichiers":
                    filter_info.append(f"fichier: {selected_file_filter}")
                
                if filter_info:
                    stats_text = f"📊 {visible_exclusions} exclusion(s) ({', '.join(filter_info)})"
                elif selected_project_filter == "Tous les projets":
                    stats_text = f"📊 Total: {visible_exclusions} exclusion(s) dans {len(self.exclusions_data)} projet(s)"
                else:
                    stats_text = f"📊 {visible_exclusions} exclusion(s)"
                
                self.stats_label.config(text=stats_text)
                
        except Exception as e:
            log_message("ERREUR", f"Erreur mise à jour compteur sélection: {e}", category="exclusions_manager")
    
    def _refresh(self):
        """Recharge les exclusions"""
        self._load_exclusions()
        show_custom_messagebox(
            'info',
            "🔄 Actualisation",
            "Les exclusions ont été actualisées avec succès.",
            self.theme,
            parent=self.window
        )
    
    def _delete_selected(self):
        """Supprime les exclusions sélectionnées (via checkboxes)"""
        try:
            # Récupérer toutes les exclusions cochées
            selected_exclusions = []
            
            for item_unique_id, is_selected in self.selected_items.items():
                if is_selected:
                    # Parser l'ID unique pour extraire les infos
                    parts = item_unique_id.split('|')
                    if len(parts) == 3:
                        project_path, file_path, line = parts
                        selected_exclusions.append({
                            'project_path': project_path,
                            'file_path': file_path,
                            'line': int(line)
                        })
            
            if not selected_exclusions:
                show_custom_messagebox(
                    'warning',
                    "⚠️ Aucune sélection",
                    "Veuillez cocher au moins une exclusion à supprimer.",
                    self.theme,
                    parent=self.window
                )
                return
            
            # Confirmer la suppression
            count = len(selected_exclusions)
            confirm = show_custom_messagebox(
                'askyesno',
                "❓ Confirmer la suppression",
                f"Voulez-vous vraiment supprimer {count} exclusion(s) ?\n\n"
                "Cette action est irréversible.",
                self.theme,
                yes_text="Oui, supprimer",
                no_text="Annuler",
                parent=self.window
            )
            
            if not confirm:
                return
            
            # Supprimer les exclusions
            deleted_count = 0
            errors = []
            
            for excl_info in selected_exclusions:
                try:
                    # Trouver l'exclusion complète pour avoir le texte
                    project_path = excl_info['project_path']
                    file_path = excl_info['file_path']
                    line = excl_info['line']
                    
                    if project_path in self.exclusions_data:
                        for exclusion in self.exclusions_data[project_path]:
                            if (exclusion['file'] == file_path and 
                                exclusion['line'] == line):
                                # Supprimer via config_manager
                                config_manager.remove_coherence_exclusion(
                                    project_path,
                                    exclusion['file'],
                                    exclusion['line'],
                                    exclusion['text']
                                )
                                deleted_count += 1
                                break
                    
                except Exception as e:
                    errors.append(f"{file_path}:{line}: {e}")
                    log_message("ERREUR", f"Erreur suppression exclusion {file_path}:{line}: {e}", category="exclusions_manager")
            
            # Recharger les exclusions
            self._load_exclusions()
            
            # Afficher le résultat
            if errors:
                show_custom_messagebox(
                    'warning',
                    "⚠️ Suppression partielle",
                    f"{deleted_count}/{count} exclusion(s) supprimée(s)\n\n"
                    f"{len(errors)} erreur(s) rencontrée(s).",
                    self.theme,
                    parent=self.window
                )
            else:
                show_custom_messagebox(
                    'info',
                    "✅ Suppression réussie",
                    f"{deleted_count} exclusion(s) supprimée(s) avec succès.",
                    self.theme,
                    parent=self.window
                )
            
            log_message("INFO", f"{deleted_count} exclusions supprimées", category="exclusions_manager")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur suppression exclusions: {e}", category="exclusions_manager")
            show_custom_messagebox(
                'error',
                "❌ Erreur de suppression",
                f"Impossible de supprimer les exclusions:\n\n{e}",
                self.theme,
                parent=self.window
            )
    
    def _on_close(self):
        """Ferme la fenêtre"""
        try:
            self.window.grab_release()
            self.window.destroy()
            log_message("INFO", "Gestionnaire d'exclusions fermé", category="exclusions_manager")
        except Exception as e:
            log_message("ERREUR", f"Erreur fermeture gestionnaire: {e}", category="exclusions_manager")

