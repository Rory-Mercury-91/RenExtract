# ui/dialogs/exclusions_manager_dialog.py
# Gestionnaire d'exclusions de lignes pour la cohérence

"""
Fenêtre modale pour gérer les exclusions de lignes de cohérence.
Permet de voir, filtrer et supprimer les exclusions ajoutées via le rapport HTML interactif.
"""

import tkinter as tk
from tkinter import ttk
import os

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
        self.current_project_filter = tk.StringVar(value="all")
        self.current_file_filter = tk.StringVar(value="all")  # Nouveau filtre par fichier
        self.exclusions_data = {}  # {project_path: [exclusions]}
        self.tree_items = {}  # {item_id: (project, index)}
        
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
            
            # Ajouter "Tous les projets" en premier
            values = ["Tous les projets"] + [os.path.basename(p) for p in projects]
            
            self.project_filter_combo['values'] = values
            
            # Sélectionner "Tous les projets" par défaut
            if self.current_project_filter.get() == "all" or not self.current_project_filter.get():
                self.project_filter_combo.current(0)
            
            # Mettre à jour le filtre de fichiers
            self._update_file_filter()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur mise à jour filtre projets: {e}", category="exclusions_manager")
    
    def _update_file_filter(self):
        """Met à jour la liste des fichiers dans le filtre selon le projet sélectionné"""
        try:
            selected_project = self.current_project_filter.get()
            
            # Récupérer les fichiers selon le projet sélectionné
            files = set()
            
            if selected_project == "Tous les projets":
                # Tous les fichiers de tous les projets
                for project_path, exclusions in self.exclusions_data.items():
                    for exclusion in exclusions:
                        files.add(exclusion.get('file', ''))
            else:
                # Fichiers du projet sélectionné uniquement
                for project_path, exclusions in self.exclusions_data.items():
                    if os.path.basename(project_path) == selected_project:
                        for exclusion in exclusions:
                            files.add(exclusion.get('file', ''))
                        break
            
            # Supprimer les fichiers vides
            files.discard('')
            
            # Créer la liste avec "Tous les fichiers" en premier
            values = ["Tous les fichiers"] + sorted(list(files))
            
            self.file_filter_combo['values'] = values
            
            # Réinitialiser à "Tous les fichiers" quand on change de projet
            if not hasattr(self, '_file_filter_initialized') or not self._file_filter_initialized:
                self.file_filter_combo.current(0)
                self._file_filter_initialized = True
            
        except Exception as e:
            log_message("ERREUR", f"Erreur mise à jour filtre fichiers: {e}", category="exclusions_manager")
    
    def _on_project_filter_changed(self):
        """Callback quand le filtre de projet change"""
        try:
            # Mettre à jour le filtre de fichiers selon le nouveau projet
            self._update_file_filter()
            
            # Réinitialiser le filtre de fichiers à "Tous les fichiers"
            self.current_file_filter.set("all")
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
            
            total_exclusions = 0
            visible_exclusions = 0
            
            for project_path, exclusions in self.exclusions_data.items():
                project_name = os.path.basename(project_path)
                
                # Vérifier le filtre par projet
                if selected_project_filter != "Tous les projets" and project_name != selected_project_filter:
                    continue
                
                for idx, exclusion in enumerate(exclusions):
                    total_exclusions += 1
                    
                    # Extraire les données
                    file_path = exclusion.get('file', 'N/A')
                    line = exclusion.get('line', 0)
                    text = exclusion.get('text', '')
                    date = exclusion.get('added_date', 'N/A')
                    
                    # Vérifier le filtre par fichier
                    if selected_file_filter != "Tous les fichiers" and file_path != selected_file_filter:
                        continue
                    
                    visible_exclusions += 1
                    
                    # Tronquer le texte si trop long
                    if len(text) > 80:
                        text = text[:77] + "..."
                    
                    # Créer un ID unique pour cette exclusion
                    item_unique_id = f"{project_path}|{file_path}|{line}"
                    
                    # Initialiser la sélection à False
                    self.selected_items[item_unique_id] = False
                    
                    # Ajouter à la Treeview avec checkbox
                    item_id = self.tree.insert(
                        '',
                        'end',
                        values=("☐", project_name, file_path, line, text, date),
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

