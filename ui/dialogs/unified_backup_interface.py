# ui/unified_backup_interface.py - VERSION HARMONISÉE AVEC COHERENCE CHECKER
# Interface UnifiÃ©e de Gestion des Sauvegardes - Style Coherence Checker
# Created for RenExtract 

"""
Interface graphique unifiÃ©e pour gÃ©rer les sauvegardes de RenExtract
- Style IDENTIQUE au coherence checker
- Même taille de fenêtre (1200x900)
- Thème responsive light/dark mode
- Structure LabelFrame harmonisée
- Filtre par jeu ET par type de backup
"""

import tkinter as tk
from tkinter import ttk, filedialog
import os
import shutil
import datetime
import zipfile
from core.models.backup.unified_backup_manager import UnifiedBackupManager, BackupType
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import show_translated_messagebox
from ui.themes import theme_manager

def show_unified_backup_manager(parent):
    """Affiche l'interface unifiÃ©e de gestion des sauvegardes (persistante)"""
    try:
        # Vérifier si une instance existe déjà
        if hasattr(show_unified_backup_manager, '_current_instance'):
            existing = show_unified_backup_manager._current_instance
            if existing and hasattr(existing, 'window') and existing.window:
                try:
                    if existing.window.winfo_exists():
                        # Fenêtre existe, la réafficher
                        existing.window.deiconify()
                        existing.window.lift()
                        existing.window.focus_force()
                        existing.window.grab_set()
                        existing._load_data()  # Recharger les données
                        log_message("DEBUG", "Fenêtre backup réaffichée", category="ui_backup")
                        return
                except:
                    # Fenêtre détruite, créer une nouvelle
                    pass
        
        # Créer la nouvelle fenêtre
        dialog = UnifiedBackupDialog(parent)
        
    except Exception as e:
        log_message("ERREUR", f"Erreur ouverture gestionnaire unifiÃ©: {e}", category="ui_backup")
        show_translated_messagebox('error', "Erreur", 
                                  "Erreur ouverture gestionnaire :\n{error}", error=str(e))

class UnifiedBackupDialog:
    """Dialogue principal du gestionnaire unifiÃ© - VERSION HARMONISÉE COHERENCE CHECKER"""
    
    def __init__(self, parent):
        self.parent = parent
        self.manager = UnifiedBackupManager()
        self.window = None
        self.current_filter_game = None
        self.current_filter_type = None
        self.backups = []
        self.tree = None
        
        # Enregistrer cette fenêtre dans le système de thème global
        theme_manager.register_window(self)
        
        # Créer et afficher la fenêtre
        self.show()
        
    def show(self):
        """Affiche le dialogue avec style coherence checker (gestion persistance)"""
        # Vérifier si la fenêtre existe déjà
        if self.window is not None:
            try:
                if self.window.winfo_exists():
                    # Fenêtre existe déjà, la réafficher
                    self.window.deiconify()
                    self.window.lift()
                    self.window.focus_force()
                    self.window.grab_set()  # Remettre le grab modal
                    
                    # Recharger les données pour avoir les dernières sauvegardes
                    self._load_data()
                    
                    log_message("DEBUG", "Fenêtre backup réaffichée (réutilisation)", category="ui_backup")
                    return
            except:
                # La fenêtre a été détruite, la recréer
                self.window = None
        
        # Créer la fenêtre pour la première fois
        self.window = tk.Toplevel(self.parent)
        self.window.title("🗂️ " + "Gestionnaire de Sauvegardes")
        self.window.geometry("1200x900")
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Enregistrer la fenêtre dans le window_manager
        from ui.window_manager import window_manager
        window_manager.register_window('backup_manager', self.window)
        
        # ✅ MÊME LOGIQUE DE CENTRAGE que coherence checker
        self._center_window()
        self.window.lift()
        self.window.focus_force()
        
        # ✅ MÊME APPLICATION THÈME
        theme = theme_manager.get_theme()
        self.window.configure(bg=theme["bg"])
        theme_manager.apply_to_widget(self.window)
        
        self._create_interface()
        self._load_data()
        
        log_message("DEBUG", "Fenêtre backup créée (première fois)", category="ui_backup")
        
        # ✅ MÊME LOGIQUE POST-CRÉATION
        self.window.after(100, self._apply_theme_to_window)
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        self._ensure_single_instance()
    
    def _center_window(self):
        """Centre la fenêtre sur l'écran - IDENTIQUE coherence checker"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def _create_interface(self):
        """Crée l'interface utilisateur - STYLE MODERNE SANS LABELFRAME"""
        theme = theme_manager.get_theme()
        
        # ✅ EN-TÊTE IDENTIQUE coherence checker
        self._create_header()
        
        # ✅ CONTENU PRINCIPAL avec structure moderne
        main_frame = tk.Frame(self.window, bg=theme["bg"])
        main_frame.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        
        # Section Statistiques - Style moderne
        stats_title = tk.Label(
            main_frame,
            text="📊 Statistiques des sauvegardes",
            font=('Segoe UI', 11, 'bold'),
            bg=theme["bg"],
            fg=theme["accent"]
        )
        stats_title.pack(anchor='w', pady=(0, 10))
        self._create_statistics_section(main_frame)
        
        # Section Filtres - Style moderne
        filter_title = tk.Label(
            main_frame,
            text="🔍 Filtres et actions",
            font=('Segoe UI', 11, 'bold'),
            bg=theme["bg"],
            fg=theme["accent"]
        )
        filter_title.pack(anchor='w', pady=(20, 10))
        self._create_filter_section(main_frame)
        
        # Section Liste - Style moderne
        list_title = tk.Label(
            main_frame,
            text="📋 Liste des sauvegardes",
            font=('Segoe UI', 11, 'bold'),
            bg=theme["bg"],
            fg=theme["accent"]
        )
        list_title.pack(anchor='w', pady=(20, 10))
        self._create_list_section(main_frame)
        
        # Section Actions - Style moderne
        actions_title = tk.Label(
            main_frame,
            text="⚡ Actions sur les sauvegardes",
            font=('Segoe UI', 11, 'bold'),
            bg=theme["bg"],
            fg=theme["accent"]
        )
        actions_title.pack(anchor='w', pady=(20, 10))
        self._create_actions_section(main_frame)
        
        # ✅ BARRE DE STATUT comme coherence checker
        self._create_footer()
    
    def _create_header(self):
        """Crée l'en-tête - IDENTIQUE coherence checker"""
        theme = theme_manager.get_theme()
        
        # Frame d'en-tête
        header_frame = tk.Frame(self.window, bg=theme["bg"])
        header_frame.pack(fill='x', padx=20, pady=15)
        
        # Titre principal
        title_label = tk.Label(
            header_frame,
            text="🗂️ " + "Gestionnaire de Sauvegardes",
            font=('Segoe UI Emoji', 16, 'bold'),
            bg=theme["bg"],
            fg=theme["accent"]
        )
        title_label.pack()
        
        # Sous-titre
        subtitle_label = tk.Label(
            header_frame,
            text="Gérez, restaurez et organisez toutes vos sauvegardes de fichiers RenExtract",
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        subtitle_label.pack(pady=(5, 0))
    
    def _create_statistics_section(self, parent):
        """Crée la section statistiques en deux colonnes comme coherence checker"""
        theme = theme_manager.get_theme()
        
        # Frame principal pour les stats
        stats_container = tk.Frame(parent, bg=theme["bg"])
        stats_container.pack(fill='x', padx=15, pady=15)
        
        # Colonne gauche
        left_column = tk.Frame(stats_container, bg=theme["bg"])
        left_column.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        # Nombre de sauvegardes (gauche)
        self.total_backups_label = tk.Label(
            left_column,
            text="📊 Sauvegardes totales: - ",
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"],
            anchor='w'
        )
        self.total_backups_label.pack(anchor='w', pady=2, fill='x')
        
        # Nombre de jeux (gauche)
        self.total_games_label = tk.Label(
            left_column,
            text="🎮 Jeux concernés: - ",
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"],
            anchor='w'
        )
        self.total_games_label.pack(anchor='w', pady=2, fill='x')
        
        # Colonne droite
        right_column = tk.Frame(stats_container, bg=theme["bg"])
        right_column.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # Taille totale (droite)
        self.total_size_label = tk.Label(
            right_column,
            text="💾 Taille totale: - ",
            font=('Segoe UI', 10, 'bold'),
            bg=theme["bg"],
            fg=theme["accent"],
            anchor='w'
        )
        self.total_size_label.pack(anchor='w', pady=2, fill='x')
    
    def _create_filter_section(self, parent):
        """Crée la section filtres avec combobox côte à côte"""
        theme = theme_manager.get_theme()
        
        # Container principal
        filter_container = tk.Frame(parent, bg=theme["bg"])
        filter_container.pack(fill='x', padx=15, pady=15)
        
        # ✅ NOUVELLE ORGANISATION : FILTRES EN DEUX COLONNES CÔTE À CÔTE
        filters_main = tk.Frame(filter_container, bg=theme["bg"])
        filters_main.pack(side='left', fill='x', expand=True, padx=(0, 20))
        
        # Colonne gauche - Filtre par jeu
        filter_game_column = tk.Frame(filters_main, bg=theme["bg"])
        filter_game_column.pack(side='left', fill='x', expand=True, padx=(0, 15))
        
        game_filter_label = tk.Label(
            filter_game_column,
            text="🎮 Filtrer par jeu :",
            font=('Segoe UI', 10, 'bold'),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        game_filter_label.pack(anchor='w', pady=(0, 5))
        
        self.game_var = tk.StringVar(value="Tous")
        self.game_combo = ttk.Combobox(
            filter_game_column, 
            textvariable=self.game_var, 
            width=20, 
            state="readonly",
            font=('Segoe UI', 9)
        )
        self.game_combo.pack(anchor='w', fill='x', pady=(0, 5))
        self.game_combo.bind('<<ComboboxSelected>>', self._on_filter_changed)
        
        # Colonne droite - Filtre par type
        filter_type_column = tk.Frame(filters_main, bg=theme["bg"])
        filter_type_column.pack(side='right', fill='x', expand=True, padx=(15, 0))
        
        type_filter_label = tk.Label(
            filter_type_column,
            text="🏷️ Filtrer par type :",
            font=('Segoe UI', 10, 'bold'),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        type_filter_label.pack(anchor='w', pady=(0, 5))
        
        self.type_var = tk.StringVar(value="Tous")
        self.type_combo = ttk.Combobox(
            filter_type_column,
            textvariable=self.type_var,
            width=20,
            state="readonly",
            font=('Segoe UI', 9),
            values=["Tous", "🛡️ Sécurité", "🧹 Nettoyage", "📦 Avant RPA", "🔗 Avant combinaison", "⚡ Édition temps réel", "🔧 Modification cohérence"]
        )
        self.type_combo.pack(anchor='w', fill='x', pady=(0, 5))
        self.type_combo.bind('<<ComboboxSelected>>', self._on_filter_changed)
        
    def _create_list_section(self, parent):
        """Crée la section liste avec TreeView - En-têtes centrés"""
        theme = theme_manager.get_theme()
        
        # Container pour TreeView
        list_container = tk.Frame(parent, bg=theme["bg"])
        list_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Configuration du style TreeView - APPROCHE SIMPLE
        style = ttk.Style()
        
        # Configuration simple du style TreeView
        style.configure("Treeview",
                    background="#2d3748",
                    foreground="#e2e8f0",
                    fieldbackground="#2d3748",
                    borderwidth=1)
        
        # Configuration des en-têtes
        style.configure("Treeview.Heading",
                    background="#1a1f29",
                    foreground="#4a90e2",
                    font=('Segoe UI', 9, 'bold'),
                    relief="flat",
                    anchor='center')
        
        # Configuration des séparateurs
        style.configure("Treeview.Separator",
                    background="#000000",
                    width=1)
        
        # Dictionnaire pour stocker les items sélectionnés
        self.selected_items = {}  # {item_id: True/False}
        self.select_all_var = tk.BooleanVar(value=False)
        
        columns = ('select', 'game', 'filename', 'type', 'created', 'size')
        self.tree = ttk.Treeview(list_container, 
                                columns=columns, 
                                show='headings', 
                                height=12)
        
        # Configuration des colonnes avec en-têtes centrés
        headings_config = [
            ('select', "☐", 40),  # Colonne de sélection (texte fixe pour éviter décalage)
            ('game', "Nom du jeu", 200),
            ('filename', "Nom du fichier/dossier", 150),
            ('type', "Type backup", 120),
            ('created', "Date créé", 130),
            ('size', "Taille", 100)
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
                self.tree.heading(col_id, 
                                text=col_text,
                                command=lambda c=col_id: self._sort_column(c, False),
                                anchor='center')
                self.tree.column(col_id, width=col_width, anchor='w')
        
        # Variables pour le tri
        self.sort_reverse = {}
        for col in columns:
            self.sort_reverse[col] = False
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(list_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Placement
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        list_container.grid_rowconfigure(0, weight=1)
        list_container.grid_columnconfigure(0, weight=1)
        
        # Bind pour cliquer sur une ligne et toggle la checkbox
        self.tree.bind('<Button-1>', self._on_tree_click)
        
        # Menu contextuel
        self._create_context_menu()


    def _create_context_menu(self):
        """Crée le menu contextuel avec style coherence checker"""
        theme = theme_manager.get_theme()
        
        self.context_menu = tk.Menu(self.tree, tearoff=0,
                                   bg=theme["frame_bg"],
                                   fg=theme["fg"],
                                   activebackground=theme["accent"],
                                   activeforeground=theme["bg"])
        
        self.context_menu.add_command(label="💾 Restaurer", 
                                     command=self.restore_selected)
        self.context_menu.add_command(label="📄 Restaurer vers...", 
                                     command=self._restore_to_path)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🗑️ Supprimer", 
                                     command=self._delete_smart)
        
        def show_context_menu(event):
            try:
                item = self.tree.identify_row(event.y)
                if item:
                    self.tree.selection_set(item)
                    self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()
        
        self.tree.bind('<Button-3>', show_context_menu)
    
    def _create_actions_section(self, parent):
        """Crée la section actions avec couleurs fixes pour les boutons"""
        theme = theme_manager.get_theme()
        
        # Disposition : BOUTONS À GAUCHE, FERMER À DROITE
        action_container = tk.Frame(parent, bg=theme["bg"])
        action_container.pack(fill='x', padx=15, pady=15)
        
        # Frame gauche pour les actions principales
        actions_left = tk.Frame(action_container, bg=theme["bg"])
        actions_left.pack(side='left')
        
        # ✅ BOUTONS AVEC COULEURS FIXES (texte toujours noir, couleurs fixes)
        buttons_config = [
            ("💾 Restaurer", self.restore_selected, theme["button_primary_bg"]),     # Primaire
            ("📄 Restaurer vers...", self._restore_to_path, theme["button_secondary_bg"]),   # Secondaire
            ("🗑️ Supprimer", self._delete_smart, theme["button_danger_bg"]),      # Suppression intelligente (sélection ou ligne)
            ("📁 Ouvrir le Dossier", self._open_backup_folder, theme["button_help_bg"])      # Aide/Info
        ]

        for text, command, bg_color in buttons_config:
            btn = tk.Button(
                actions_left,
                text=text,
                command=command,
                bg=bg_color,   # MODIFIÉ
                fg="#000000",  # MODIFIÉ - Texte noir uniforme
                font=('Segoe UI', 9),
                pady=4,
                padx=8,
                width=18
            )
            btn.pack(side='left', padx=(0, 5))

        close_btn = tk.Button(
            action_container,
            text="❌ Fermer",
            command=self._on_close,
            bg=theme["button_danger_bg"],   # MODIFIÉ - Négative/Danger
            fg="#000000",                    # MODIFIÉ - Texte noir uniforme
            font=('Segoe UI', 9),
            pady=4,
            padx=8,
            width=12
        )
        close_btn.pack(side='right')
    
    def _create_footer(self):
        """Crée le pied de page avec barre de statut unique"""
        theme = theme_manager.get_theme()
        
        footer_frame = tk.Frame(self.window, bg=theme["bg"])
        footer_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        # Barre de statut unique (en bas seulement)
        self.status_label = tk.Label(
            footer_frame,
            text="État: Chargement des sauvegardes...",
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"],
            anchor='w'
        )
        self.status_label.pack(fill='x')
    
    def _load_data(self):
        """Charge les données et met à jour l'interface (optimisé avec cache)"""
        try:
            self._update_status("📄 Chargement des sauvegardes en cours...")
            
            # Charger tous les backups - utilise le cache si disponible
            if hasattr(self.manager, 'list_all_backups'):
                # Charger TOUTES les sauvegardes (utilise le cache si valide)
                all_backups = self.manager.list_all_backups()
                
                # Appliquer les filtres en mémoire (très rapide)
                self.backups = all_backups
                
                if self.current_filter_game and self.current_filter_game != "Tous":
                    self.backups = [b for b in self.backups if b['game_name'] == self.current_filter_game]
                
                if self.current_filter_type:
                    self.backups = [b for b in self.backups if b['type'] == self.current_filter_type]
            else:
                # Fallback pour ancien manager
                self.backups = []
            
            # Mettre à jour l'interface
            self._update_statistics()
            self._update_game_filter()
            self._update_tree()
            
            # Mettre à jour le statut final
            filter_info = []
            if self.current_filter_game and self.current_filter_game != "Tous":
                filter_info.append(f"jeu: {self.current_filter_game}")
            if self.current_filter_type:
                # Mapper les types pour l'affichage
                type_display = {
                    BackupType.SECURITY: "Sécurité",
                    BackupType.CLEANUP: "Nettoyage",
                    BackupType.RPA_BUILD: "Avant RPA",
                    BackupType.BEFORE_COMBINATION: "Avant combinaison",
                    BackupType.REALTIME_EDIT: "Édition temps réel",
                    BackupType.COHERENCE_EDIT: "Modification cohérence"
                }.get(self.current_filter_type, str(self.current_filter_type))
                filter_info.append(f"type: {type_display}")
            
            if filter_info:
                filter_text = " (" + ", ".join(filter_info) + ")"
                self._update_status(f"✅ {len(self.backups)} sauvegardes chargées{filter_text}")
            else:
                self._update_status(f"✅ {len(self.backups)} sauvegardes chargées - Prêt")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur chargement données: {e}", category="ui_backup")
            self._update_status("❌ Erreur lors du chargement des données")
            show_translated_messagebox('error', "Erreur", 
                                     "Erreur chargement données :\n{error}", error=str(e))
    
    def _update_statistics(self):
        """Met à jour les statistiques avec structure hiérarchique"""
        try:
            # GESTION DES FILTRES MULTIPLES
            filter_parts = []
            if self.current_filter_game:
                filter_parts.append(f"jeu: {self.current_filter_game}")
            if self.current_filter_type:
                # Mapper seulement les types utilisés
                type_display = {
                    BackupType.SECURITY: "Sécurité",
                    BackupType.CLEANUP: "Nettoyage", 
                    BackupType.RPA_BUILD: "Avant RPA",
                    BackupType.BEFORE_COMBINATION: "Avant combinaison",
                    BackupType.REALTIME_EDIT: "Édition temps réel",
                    BackupType.COHERENCE_EDIT: "Modification cohérence"
                }.get(self.current_filter_type, str(self.current_filter_type))
                filter_parts.append(f"type: {type_display}")
            
            # TOUJOURS utiliser la même source de données pour la cohérence
            if filter_parts:
                # Mode FILTRÉ : utiliser self.backups (données filtrées)
                total_backups = len(self.backups)
                total_size_mb = sum(b.get('size', 0) for b in self.backups) / (1024 * 1024)
                total_games = 1 if self.current_filter_game else len(set(b['game_name'] for b in self.backups))
                total_files = len(set(f"{b['game_name']}/{b.get('file_name', 'unknown')}" for b in self.backups))
            else:
                # Mode NON FILTRÉ : utiliser all_backups (toutes les sauvegardes)
                try:
                    all_backups = self.manager.list_all_backups()
                    total_backups = len(all_backups)
                    total_size_mb = sum(b.get('size', 0) for b in all_backups) / (1024 * 1024)
                    total_games = len(set(b['game_name'] for b in all_backups))
                    total_files = len(set(f"{b['game_name']}/{b.get('file_name', 'unknown')}" for b in all_backups))
                except:
                    # Fallback sur self.backups en cas d'erreur
                    total_backups = len(self.backups)
                    total_size_mb = sum(b.get('size', 0) for b in self.backups) / (1024 * 1024)
                    total_games = len(set(b['game_name'] for b in self.backups))
                    total_files = len(set(f"{b['game_name']}/{b.get('file_name', 'unknown')}" for b in self.backups))
            
            # Affichage des statistiques
            self.total_backups_label.config(text=f"📊 Sauvegardes totales: {total_backups}")
            
            # Afficher jeux ET fichiers si pas de filtre
            if not filter_parts:
                self.total_games_label.config(text=f"🎮 Jeux/Fichiers: {total_games} jeux, {total_files} fichiers")
            else:
                self.total_games_label.config(text=f"🎮 Jeux concernés: {total_games}")
                
            self.total_size_label.config(text=f"💾 Taille totale: {total_size_mb:.1f} MB")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur calcul statistiques hiérarchiques: {e}", category="ui_backup")
            self.total_backups_label.config(text="📊 Sauvegardes totales: Erreur")
    
    def _update_game_filter(self):
        """Met à jour la liste des jeux dans le filtre"""
        try:
            if hasattr(self.manager, 'list_all_backups'):
                all_backups = self.manager.list_all_backups()
                games = ["Tous"] + sorted(set(b['game_name'] for b in all_backups))
                self.game_combo['values'] = games
        except Exception as e:
            log_message("ATTENTION", f"Erreur mise à jour filtre jeu: {e}", category="ui_backup")
    
    def _update_tree(self):
        """Met à jour la TreeView"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Réinitialiser les sélections
        self.selected_items = {}
        self.select_all_var.set(False)
        self.tree.heading('select', text="☐")
        
        for backup in self.backups:
            self._add_backup_to_tree(backup)
    

    def _add_backup_to_tree(self, backup):
        """Ajoute une sauvegarde à la TreeView - Version simplifiée"""
        try:
            game_name = backup['game_name']
            file_name = backup.get('file_name', 'unknown')
            
            # Récupérer la description du type
            if hasattr(self.manager, 'BACKUP_DESCRIPTIONS'):
                backup_type = self.manager.BACKUP_DESCRIPTIONS.get(backup['type'], backup['type'])
            else:
                backup_type = str(backup['type'])
            
            # Formatage de la date
            created_str = backup['created']
            if isinstance(created_str, str):
                try:
                    created_date = datetime.datetime.fromisoformat(created_str)
                    created_display = created_date.strftime("%d/%m/%Y %H:%M")
                except:
                    created_display = created_str
            else:
                created_display = str(created_str)
            
            # Formatage de la taille
            size_bytes = backup.get('size', 0)
            if size_bytes < 1024:
                size_display = f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                size_display = f"{size_bytes / 1024:.1f} KB"
            else:
                size_display = f"{size_bytes / (1024 * 1024):.1f} MB"
            
            backup_id = backup.get('id', '')
            
            # Initialiser la sélection à False
            self.selected_items[backup_id] = False
            
            item = self.tree.insert('', 'end', values=(
                "☐",  # Checkbox non cochée par défaut
                game_name,
                file_name,  # Nom du fichier simple
                backup_type,
                created_display,
                size_display
            ), tags=(backup_id,))
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur ajout backup à l'arbre: {e}", category="ui_backup")
    
    def _on_tree_click(self, event):
        """Gère le clic sur le TreeView pour toggle les checkboxes (clic n'importe où sur la ligne)"""
        try:
            # Identifier la région cliquée
            region = self.tree.identify_region(event.x, event.y)
            if region != "cell":
                return
            
            # Identifier la ligne cliquée
            item = self.tree.identify_row(event.y)
            if not item:
                return
            
            # Récupérer le backup_id depuis les tags
            item_tags = self.tree.item(item, 'tags')
            backup_id = item_tags[0] if item_tags else None
            
            if not backup_id:
                return
            
            # Toggle la sélection
            current_state = self.selected_items.get(backup_id, False)
            new_state = not current_state
            self.selected_items[backup_id] = new_state
            
            # Mettre à jour l'affichage
            current_values = list(self.tree.item(item, 'values'))
            current_values[0] = "☑" if new_state else "☐"
            self.tree.item(item, values=current_values)
            
            # Mettre à jour le compteur de sélection
            self._update_selection_count()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur toggle checkbox: {e}", category="ui_backup")
    
    def _toggle_select_all(self):
        """Sélectionne ou désélectionne tous les items"""
        try:
            # Inverser l'état de sélection globale
            new_state = not self.select_all_var.get()
            self.select_all_var.set(new_state)
            
            # Mettre à jour toutes les checkboxes
            for item in self.tree.get_children():
                item_tags = self.tree.item(item, 'tags')
                backup_id = item_tags[0] if item_tags else None
                
                if backup_id:
                    self.selected_items[backup_id] = new_state
                    
                    # Mettre à jour l'affichage
                    current_values = list(self.tree.item(item, 'values'))
                    current_values[0] = "☑" if new_state else "☐"
                    self.tree.item(item, values=current_values)
            
            # Mettre à jour le compteur
            self._update_selection_count()
            
            # L'en-tête garde toujours "☐" pour éviter le décalage visuel
            # L'état de sélection est visible via les checkboxes individuelles et le compteur
            
        except Exception as e:
            log_message("ERREUR", f"Erreur toggle select all: {e}", category="ui_backup")
    
    def _cleanup_empty_directories(self):
        """Nettoie les dossiers vides après suppression de sauvegardes (inclut les sous-dossiers)"""
        try:
            log_message("DEBUG", "Début nettoyage dossiers vides", category="ui_backup")
            
            if not hasattr(self.manager, 'backup_root'):
                log_message("ATTENTION", "Manager n'a pas d'attribut backup_root", category="ui_backup")
                return
            
            backup_root = self.manager.backup_root
            log_message("DEBUG", f"Racine des sauvegardes: {backup_root}", category="ui_backup")
            
            if not os.path.exists(backup_root):
                log_message("ATTENTION", f"Racine des sauvegardes n'existe pas: {backup_root}", category="ui_backup")
                return
            
            # Nettoyer récursivement TOUS les dossiers vides (y compris les sous-dossiers)
            cleaned_dirs = []
            self._cleanup_empty_dirs_recursive(backup_root, cleaned_dirs)
            
            if cleaned_dirs:
                log_message("INFO", f"Dossiers vides nettoyés: {', '.join(cleaned_dirs)}", category="ui_backup")
            else:
                log_message("INFO", "Aucun dossier vide trouvé", category="ui_backup")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur nettoyage dossiers vides: {e}", category="ui_backup")
    
    def _cleanup_empty_dirs_recursive(self, dir_path, cleaned_dirs):
        """Nettoie récursivement tous les dossiers vides dans un répertoire"""
        try:
            if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
                return
            
            log_message("DEBUG", f"Vérification dossier: {dir_path}", category="ui_backup")
            
            # D'abord, nettoyer récursivement tous les sous-dossiers
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                if os.path.isdir(item_path):
                    self._cleanup_empty_dirs_recursive(item_path, cleaned_dirs)
            
            # Ensuite, vérifier si ce dossier est maintenant vide (après nettoyage des sous-dossiers)
            # Skip les fichiers de métadonnées au niveau racine
            if dir_path == getattr(self.manager, 'backup_root', ''):
                # Au niveau racine, ne JAMAIS supprimer le dossier racine, même s'il est vide
                log_message("DEBUG", f"Dossier racine - jamais supprimé: {dir_path}", category="ui_backup")
                return  # Ne pas supprimer le dossier racine
            
            # Dans les sous-dossiers, vérifier tous les éléments
            items = os.listdir(dir_path)
            log_message("DEBUG", f"Sous-dossier - éléments: {items}", category="ui_backup")
            
            # Si le dossier est vide (ou ne contient que des dossiers vides), le supprimer
            if not items:
                try:
                    relative_path = os.path.relpath(dir_path, getattr(self.manager, 'backup_root', dir_path))
                    log_message("INFO", f"Suppression dossier vide: {relative_path}", category="ui_backup")
                    shutil.rmtree(dir_path)
                    cleaned_dirs.append(relative_path)
                    log_message("INFO", f"Dossier vide supprimé avec succès: {relative_path}", category="ui_backup")
                except Exception as e:
                    log_message("ATTENTION", f"Erreur suppression dossier {dir_path}: {e}", category="ui_backup")
            else:
                log_message("DEBUG", f"Dossier non vide, conservé: {dir_path}", category="ui_backup")
                    
        except Exception as e:
            log_message("ERREUR", f"Erreur nettoyage récursif {dir_path}: {e}", category="ui_backup")
    
    def _is_directory_empty_recursive(self, dir_path):
        """Vérifie récursivement si un dossier est vide (ne contient aucun fichier)"""
        try:
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                if os.path.isfile(item_path):
                    return False  # Il y a au moins un fichier
                elif os.path.isdir(item_path):
                    if not self._is_directory_empty_recursive(item_path):
                        return False  # Un sous-dossier n'est pas vide
            return True  # Le dossier est vide
        except Exception:
            return False  # En cas d'erreur, considérer comme non-vide
    
    def _update_selection_count(self):
        """Met à jour l'affichage du nombre d'éléments sélectionnés"""
        try:
            selected_count = sum(1 for selected in self.selected_items.values() if selected)
            
            if selected_count > 0:
                self._update_status(f"📌 {selected_count} sauvegarde(s) sélectionnée(s)")
            else:
                total = len(self.backups)
                self._update_status(f"✅ {total} sauvegardes chargées - Prêt")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur mise à jour compteur sélection: {e}", category="ui_backup")
    
    def _on_filter_changed(self, event=None):
        """Gestionnaire de changement de filtre - GÈRE LES DEUX FILTRES"""
        # GESTION FILTRE JEU
        selected_game = self.game_var.get()
        if selected_game == "Tous":
            self.current_filter_game = None
        else:
            self.current_filter_game = selected_game
        
        # GESTION FILTRE TYPE
        selected_type = self.type_var.get()
        if selected_type == "Tous":
            self.current_filter_type = None
        else:
            # Mapper tous les types
            type_mapping = {
                "🛡️ Sécurité": BackupType.SECURITY,
                "🧹 Nettoyage": BackupType.CLEANUP,
                "📦 Avant RPA": BackupType.RPA_BUILD,
                "🔗 Avant combinaison": BackupType.BEFORE_COMBINATION,
                "⚡ Édition temps réel": BackupType.REALTIME_EDIT,
                "🔧 Modification cohérence": BackupType.COHERENCE_EDIT
            }
            self.current_filter_type = type_mapping.get(selected_type)
        
        # Recharger les données avec les nouveaux filtres
        self._load_data()
    
    def _get_selected_backup(self):
        """Récupère la sauvegarde sélectionnée"""
        selection = self.tree.selection()
        if not selection:
            return None
        
        item = selection[0]
        item_tags = self.tree.item(item, 'tags')
        backup_id = item_tags[0] if item_tags else None
        
        if not backup_id:
            return None
        
        for backup in self.backups:
            if backup.get('id') == backup_id:
                return backup
        
        return None

    def restore_selected(self):
        """Restaure la sauvegarde sélectionnée"""
        backup = self._get_selected_backup()
        if not backup:
            show_translated_messagebox('warning', "Avertissement",
                                    "Veuillez sélectionner une sauvegarde à restaurer.")
            return
    
        try:
            log_message("DEBUG", f"Backup sélectionné: {backup}", category="ui_backup")
            log_message("DEBUG", f"Source path (logs): {backup.get('source_path', '')}", category="ui_backup")
            
            # Récupérer la description du type
            if hasattr(self.manager, 'BACKUP_DESCRIPTIONS'):
                type_desc = self.manager.BACKUP_DESCRIPTIONS.get(backup['type'], backup['type'])
            else:
                type_desc = str(backup['type'])
            
            result = show_translated_messagebox(
                'askyesno',
                "Confirmer la Restauration",
                "Restaurer la sauvegarde ?\n\n• Fichier : {filename}\n• Jeu : {game}\n• Type : {type}\n• Créé le : {created}\n\nLe fichier actuel sera remplacé !",
                filename=backup.get('source_filename', 'inconnu'),
                game=backup['game_name'],
                type=type_desc,
                created=backup['created']
            )
        
            if not result:
                return
        
            # Gestion différente selon le type de sauvegarde
            backup_path = backup['backup_path']
            backup_type = backup['type']
            
            # Vérifier si c'est un fichier ZIP (sauvegardes de dossier complet)
            if backup_path.endswith('.zip') and backup_type in [BackupType.CLEANUP, BackupType.RPA_BUILD, BackupType.BEFORE_COMBINATION]:
                # Pour les archives ZIP, utiliser le chemin source original
                target_path = backup.get('source_path')
                log_message("DEBUG", f"Target path original pour ZIP: {target_path}", category="ui_backup")
                
                # ✅ CORRECTION : Normaliser le chemin avant de vérifier s'il existe
                if target_path:
                    target_path = os.path.abspath(os.path.normpath(target_path))
                    log_message("DEBUG", f"Target path normalisé pour ZIP: {target_path}", category="ui_backup")
                
                # Si le chemin original n'existe pas, essayer de le reconstruire intelligemment
                if not target_path or not os.path.exists(target_path):
                    target_path = self._get_zip_source_path_smart(backup)
                    log_message("DEBUG", f"Target path reconstruit pour ZIP: {target_path}", category="ui_backup")
                
                # Si toujours pas trouvé, demander à l'utilisateur
                if not target_path:
                    show_translated_messagebox('info', "Information",
                                            "Le chemin source original est introuvable.\nVeuillez sélectionner manuellement le dossier de destination.")
                    self._restore_zip_to_path()
                    return
                
                # Extraire le ZIP vers le dossier cible
                self._extract_zip_backup(backup_path, target_path)
                
            else:
                # Pour les fichiers individuels (SECURITY, REALTIME_EDIT)
                target_path = backup.get('source_path')
                log_message("DEBUG", f"Target path pour fichier (logs): {target_path}", category="ui_backup")
                
                # ✅ CORRECTION : Normaliser le chemin avant de vérifier s'il existe
                if target_path:
                    target_path = os.path.abspath(os.path.normpath(target_path))
                    log_message("DEBUG", f"Target path normalisé pour fichier: {target_path}", category="ui_backup")
                
                if not target_path or not os.path.exists(target_path):
                    if hasattr(self.manager, '_get_source_path_on_demand'):
                        target_path = self.manager._get_source_path_on_demand(backup)
                    
                    if not target_path or target_path == "Chemin source introuvable" or not os.path.exists(target_path):
                        show_translated_messagebox('info', "Information",
                                                "Le chemin source original est introuvable.\nVeuillez sélectionner manuellement le fichier de destination.")
                        self._restore_to_path()
                        return
                
                # Gérer les conflits de noms
                target_path = self._handle_filename_conflict(target_path)
                
                import shutil
                target_dir = os.path.dirname(target_path)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir, exist_ok=True)
                
                log_message("DEBUG", f"Copie fichier: {backup_path} -> {target_path}", category="ui_backup")
                shutil.copy2(backup_path, target_path)
        
            # Supprimer automatiquement la sauvegarde après restauration normale
            try:
                os.remove(backup['backup_path'])
                log_message("INFO", f"Sauvegarde supprimée automatiquement après restauration: {backup['backup_path']}", category="ui_backup")
                
                # Nettoyer les métadonnées
                if hasattr(self.manager, 'metadata') and backup.get('id') in self.manager.metadata:
                    del self.manager.metadata[backup['id']]
                    if hasattr(self.manager, '_save_metadata'):
                        self.manager._save_metadata()
                
                # Invalider le cache après suppression
                if hasattr(self.manager, '_invalidate_cache'):
                    self.manager._invalidate_cache()
                
            except Exception as e:
                log_message("ATTENTION", f"Impossible de supprimer la sauvegarde après restauration: {e}", category="ui_backup")
            
            # Pas de popup de confirmation - juste le statut
            self._update_status("✅ Restauration terminée avec succès - Sauvegarde supprimée automatiquement")
            
            # Recharger les données pour mettre à jour la liste
            self._load_data()
        
        except Exception as e:
            log_message("ERREUR", f"Erreur restauration: {e}", category="ui_backup")
            self._update_status("❌ Erreur lors de la restauration")
            show_translated_messagebox('error', "Erreur",
                                    "Erreur durant la restauration :\n{error}", error=str(e))
    
    def _get_zip_source_path(self, backup):
        """Reconstruit le chemin source pour les sauvegardes ZIP basé sur les métadonnées"""
        try:
            backup_type = backup['type']
            game_name = backup['game_name']
            file_name = backup.get('file_name', '')
            
            # Obtenir le répertoire de travail du projet (pas l'exécutable)
            project_root = self._get_project_root()
            
            # Reconstruire le chemin selon le type de sauvegarde
            if backup_type == BackupType.CLEANUP:
                # Pour CLEANUP, c'est généralement le dossier tl du jeu
                possible_paths = [
                    os.path.join(project_root, game_name, 'tl'),
                    os.path.join(project_root, 'tl'),
                    os.path.join(project_root, game_name, 'translation'),
                    os.path.join(project_root, game_name),  # Fallback
                ]
                
            elif backup_type == BackupType.RPA_BUILD:
                # Pour RPA_BUILD, c'est généralement le dossier du jeu ou un dossier spécifique
                possible_paths = [
                    os.path.join(project_root, game_name),
                    os.path.join(project_root, game_name, 'game'),
                    os.path.join(project_root, game_name, file_name) if file_name else None,
                    os.path.join(project_root, file_name) if file_name else None,
                ]
                
            elif backup_type == BackupType.BEFORE_COMBINATION:
                # Pour BEFORE_COMBINATION, c'est généralement le dossier tl/langue
                possible_paths = [
                    os.path.join(project_root, game_name, 'tl', file_name) if file_name else None,
                    os.path.join(project_root, 'tl', file_name) if file_name else None,
                    os.path.join(project_root, game_name, 'tl'),
                    os.path.join(project_root, 'tl'),
                ]
                
            else:
                return None
            
            # Filtrer les chemins None et tester l'existence
            possible_paths = [p for p in possible_paths if p is not None]
            
            # D'abord, chercher un chemin existant
            for path in possible_paths:
                if os.path.exists(path):
                    log_message("INFO", f"Chemin source ZIP reconstruit (existant): {path}", category="ui_backup")
                    return path
            
            # Si aucun chemin n'existe, proposer le plus logique et le créer
            if possible_paths:
                most_likely = possible_paths[0]
                log_message("INFO", f"Chemin source ZIP suggéré (à créer): {most_likely}", category="ui_backup")
                
                # Créer le dossier s'il n'existe pas
                try:
                    os.makedirs(most_likely, exist_ok=True)
                    log_message("INFO", f"Dossier créé pour restauration ZIP: {most_likely}", category="ui_backup")
                    return most_likely
                except Exception as e:
                    log_message("ATTENTION", f"Impossible de créer le dossier {most_likely}: {e}", category="ui_backup")
                    return most_likely  # Retourner quand même le chemin
                
            return None
            
        except Exception as e:
            log_message("ERREUR", f"Erreur reconstruction chemin source ZIP: {e}", category="ui_backup")
            return None
    
    def _get_zip_source_path_smart(self, backup):
        """Reconstruit intelligemment le chemin source pour les sauvegardes ZIP"""
        try:
            # D'abord, essayer d'utiliser le chemin source original
            original_source_path = backup.get('source_path')
            if original_source_path:
                # ✅ CORRECTION : Normaliser le chemin avant de vérifier s'il existe
                original_source_path = os.path.abspath(os.path.normpath(original_source_path))
                if os.path.exists(original_source_path):
                    log_message("INFO", f"Chemin source original trouvé: {original_source_path}", category="ui_backup")
                    return original_source_path
            
            # Si le chemin original n'existe pas, essayer de le reconstruire
            backup_type = backup['type']
            game_name = backup['game_name']
            file_name = backup.get('file_name', '')
            
            # Extraire le répertoire racine du chemin original
            if original_source_path:
                # Trouver le répertoire racine du projet depuis le chemin original
                project_root = self._extract_project_root_from_source_path(original_source_path)
                if project_root:
                    log_message("INFO", f"Projet racine extrait du chemin source: {project_root}", category="ui_backup")
                else:
                    project_root = self._get_project_root()
            else:
                project_root = self._get_project_root()
            
            # Reconstruire le chemin selon le type de sauvegarde
            if backup_type == BackupType.CLEANUP:
                possible_paths = [
                    os.path.join(project_root, game_name, 'tl'),
                    os.path.join(project_root, 'tl'),
                    os.path.join(project_root, game_name, 'translation'),
                    os.path.join(project_root, game_name),
                ]
                
            elif backup_type == BackupType.RPA_BUILD:
                possible_paths = [
                    os.path.join(project_root, game_name),
                    os.path.join(project_root, game_name, 'game'),
                    os.path.join(project_root, game_name, file_name) if file_name else None,
                    os.path.join(project_root, file_name) if file_name else None,
                ]
                
            elif backup_type == BackupType.BEFORE_COMBINATION:
                possible_paths = [
                    os.path.join(project_root, game_name, 'tl', file_name) if file_name else None,
                    os.path.join(project_root, 'tl', file_name) if file_name else None,
                    os.path.join(project_root, game_name, 'tl'),
                    os.path.join(project_root, 'tl'),
                ]
                
            else:
                return None
            
            # Filtrer les chemins None
            possible_paths = [p for p in possible_paths if p is not None]
            
            # D'abord, chercher un chemin existant
            for path in possible_paths:
                if os.path.exists(path):
                    log_message("INFO", f"Chemin source ZIP reconstruit (existant): {path}", category="ui_backup")
                    return path
            
            # Si aucun chemin n'existe, proposer le plus logique et le créer
            if possible_paths:
                most_likely = possible_paths[0]
                log_message("INFO", f"Chemin source ZIP suggéré (à créer): {most_likely}", category="ui_backup")
                
                # Créer le dossier s'il n'existe pas
                try:
                    os.makedirs(most_likely, exist_ok=True)
                    log_message("INFO", f"Dossier créé pour restauration ZIP: {most_likely}", category="ui_backup")
                    return most_likely
                except Exception as e:
                    log_message("ATTENTION", f"Impossible de créer le dossier {most_likely}: {e}", category="ui_backup")
                    return most_likely  # Retourner quand même le chemin
                
            return None
            
        except Exception as e:
            log_message("ERREUR", f"Erreur reconstruction chemin source ZIP: {e}", category="ui_backup")
            return None
    
    def _extract_project_root_from_source_path(self, source_path):
        """Extrait le répertoire racine du projet depuis le chemin source original"""
        try:
            # ✅ CORRECTION : Normaliser le chemin source avant l'analyse
            source_path = os.path.abspath(os.path.normpath(source_path))
            
            # Analyser le chemin source pour trouver le projet racine
            # Exemple: D:\02 - Jeux VN\02 - A traduire\WastelandGuardians-0.6-pc\game\tl\french
            # → Projet racine: D:\02 - Jeux VN\02 - A traduire\WastelandGuardians-0.6-pc
            
            # Normaliser les séparateurs pour l'analyse
            path_parts = source_path.replace('\\', '/').split('/')
            
            # Chercher les indicateurs de fin de projet
            project_indicators = ['game', 'tl', 'renpy']
            
            for i, part in enumerate(path_parts):
                if part in project_indicators:
                    # Le projet racine est le dossier parent de cet indicateur
                    project_root = '/'.join(path_parts[:i])
                    # ✅ CORRECTION : Normaliser le chemin reconstruit
                    project_root = os.path.normpath(project_root)
                    if os.path.exists(project_root):
                        log_message("INFO", f"Projet racine extrait: {project_root}", category="ui_backup")
                        return project_root
            
            # Si aucun indicateur trouvé, essayer de trouver le dossier contenant le jeu
            for i in range(len(path_parts) - 1, -1, -1):
                test_path = '/'.join(path_parts[:i+1])
                # ✅ CORRECTION : Normaliser le chemin reconstruit
                test_path = os.path.normpath(test_path)
                if os.path.exists(test_path):
                    # Vérifier si ce dossier contient des projets Ren'Py
                    if self._is_project_directory(test_path):
                        log_message("INFO", f"Projet racine trouvé par analyse: {test_path}", category="ui_backup")
                        return test_path
            
            return None
            
        except Exception as e:
            log_message("ERREUR", f"Erreur extraction projet racine depuis {source_path}: {e}", category="ui_backup")
            return None
    
    def _get_project_root(self):
        """Détermine le répertoire racine du projet (pas l'exécutable)"""
        try:
            # Méthode 1: Essayer de trouver le projet via le contrôleur principal
            if hasattr(self, 'manager') and hasattr(self.manager, 'app_controller'):
                app_controller = self.manager.app_controller
                if hasattr(app_controller, 'original_path') and app_controller.original_path:
                    # Utiliser le chemin du projet actuel
                    current_dir = os.path.dirname(app_controller.original_path)
                    project_root = self._find_project_root_from_path(current_dir)
                    if project_root:
                        log_message("INFO", f"Projet racine trouvé via app_controller: {project_root}", category="ui_backup")
                        return project_root
            
            # Méthode 2: Chercher dans le répertoire courant
            current_dir = os.getcwd()
            project_root = self._find_project_root_from_path(current_dir)
            if project_root:
                log_message("INFO", f"Projet racine trouvé via répertoire courant: {project_root}", category="ui_backup")
                return project_root
            
            # Méthode 3: Chercher dans le répertoire parent
            parent_dir = os.path.dirname(current_dir)
            project_root = self._find_project_root_from_path(parent_dir)
            if project_root:
                log_message("INFO", f"Projet racine trouvé via répertoire parent: {project_root}", category="ui_backup")
                return project_root
            
            # Méthode 4: Fallback - utiliser le répertoire courant
            log_message("ATTENTION", f"Aucun projet racine trouvé, utilisation du répertoire courant: {current_dir}", category="ui_backup")
            return current_dir
            
        except Exception as e:
            log_message("ERREUR", f"Erreur détermination projet racine: {e}", category="ui_backup")
            return os.getcwd()
    
    def _get_project_root(self):
        """Détermine le répertoire racine du projet (pas l'exécutable)"""
        try:
            # Méthode 1: Essayer de trouver le projet via le contrôleur principal
            if hasattr(self, 'manager') and hasattr(self.manager, 'app_controller'):
                app_controller = self.manager.app_controller
                if hasattr(app_controller, 'original_path') and app_controller.original_path:
                    # Utiliser le chemin du projet actuel
                    current_dir = os.path.dirname(app_controller.original_path)
                    project_root = self._find_project_root_from_path(current_dir)
                    if project_root:
                        log_message("INFO", f"Projet racine trouvé via app_controller: {project_root}", category="ui_backup")
                        return project_root
            
            # Méthode 2: Utiliser le répertoire de travail de RenExtract
            # Dans la plupart des cas, RenExtract est lancé depuis le dossier du projet
            current_dir = os.getcwd()
            
            # Vérifier si le répertoire courant contient des projets Ren'Py
            if self._is_project_directory(current_dir):
                log_message("INFO", f"Répertoire courant est un projet: {current_dir}", category="ui_backup")
                return current_dir
            
            # Méthode 3: Chercher dans le répertoire parent
            parent_dir = os.path.dirname(current_dir)
            if self._is_project_directory(parent_dir):
                log_message("INFO", f"Projet racine trouvé dans le parent: {parent_dir}", category="ui_backup")
                return parent_dir
            
            # Méthode 4: Fallback - utiliser le répertoire courant
            log_message("ATTENTION", f"Aucun projet racine trouvé, utilisation du répertoire courant: {current_dir}", category="ui_backup")
            return current_dir
            
        except Exception as e:
            log_message("ERREUR", f"Erreur détermination projet racine: {e}", category="ui_backup")
            return os.getcwd()
    
    def _is_project_directory(self, directory):
        """Vérifie si un répertoire contient des projets Ren'Py"""
        try:
            if not os.path.exists(directory):
                return False
            
            # Chercher des indicateurs de projets Ren'Py
            indicators = ["game", "tl", "renpy"]
            
            # Vérifier le répertoire courant
            for indicator in indicators:
                if os.path.exists(os.path.join(directory, indicator)):
                    return True
            
            # Vérifier les sous-répertoires (pour détecter plusieurs projets)
            try:
                for item in os.listdir(directory):
                    item_path = os.path.join(directory, item)
                    if os.path.isdir(item_path):
                        for indicator in indicators:
                            if os.path.exists(os.path.join(item_path, indicator)):
                                return True
            except (PermissionError, OSError):
                pass
            
            return False
            
        except Exception as e:
            log_message("ERREUR", f"Erreur vérification projet dans {directory}: {e}", category="ui_backup")
            return False
    
    def _find_project_root_from_path(self, start_path):
        """Trouve le projet racine en remontant depuis un chemin donné"""
        try:
            test_dir = start_path
            for _ in range(10):  # Max 10 niveaux
                if self._is_project_directory(test_dir):
                    return test_dir
                
                parent = os.path.dirname(test_dir)
                if parent == test_dir:  # Arrivé à la racine
                    break
                test_dir = parent
            
            return None
            
        except Exception as e:
            log_message("ERREUR", f"Erreur recherche projet racine depuis {start_path}: {e}", category="ui_backup")
            return None
    
    def _handle_filename_conflict(self, target_path):
        """Gère les conflits de noms de fichiers en ajoutant un suffixe numérique"""
        if not os.path.exists(target_path):
            return target_path
        
        base_path = os.path.splitext(target_path)[0]
        extension = os.path.splitext(target_path)[1]
        
        counter = 1
        while True:
            new_path = f"{base_path}_restaure_{counter}{extension}"
            if not os.path.exists(new_path):
                log_message("INFO", f"Conflit de nom résolu: {target_path} -> {new_path}", category="ui_backup")
                return new_path
            counter += 1
    
    def _extract_zip_backup(self, zip_path, target_dir):
        """Extrait une sauvegarde ZIP vers le dossier cible"""
        import zipfile
        import shutil
        
        try:
            # ✅ CORRECTION : Normaliser le chemin cible avant l'extraction
            target_dir = os.path.abspath(os.path.normpath(target_dir))
            log_message("DEBUG", f"Chemin cible normalisé pour extraction ZIP: {target_dir}", category="ui_backup")
            
            # Créer le dossier cible s'il n'existe pas
            os.makedirs(target_dir, exist_ok=True)
            
            # Créer un dossier temporaire pour l'extraction
            temp_dir = os.path.join(os.path.dirname(zip_path), f"temp_extract_{os.path.basename(zip_path)}")
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Copier le contenu du dossier temporaire vers la destination
            for item in os.listdir(temp_dir):
                src = os.path.join(temp_dir, item)
                dst = os.path.join(target_dir, item)
                
                if os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    if os.path.exists(dst):
                        os.remove(dst)
                    shutil.copy2(src, dst)
            
            # Nettoyer le dossier temporaire
            shutil.rmtree(temp_dir)
            
            log_message("INFO", f"ZIP extrait avec succès: {zip_path} -> {target_dir}", category="ui_backup")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur extraction ZIP: {e}", category="ui_backup")
            raise e
    
    def _restore_zip_to_path(self):
        """Restaure un ZIP vers un dossier spécifique"""
        backup = self._get_selected_backup()
        if not backup:
            show_translated_messagebox('warning', "Avertissement", 
                                    "Veuillez sélectionner une sauvegarde à restaurer.")
            return
        
        try:
            target_dir = filedialog.askdirectory(
                title="Sélectionner le dossier de destination pour l'archive ZIP"
            )
            
            if not target_dir:
                return
            
            self._extract_zip_backup(backup['backup_path'], target_dir)
            
            # Pas de popup de confirmation - juste le statut
            self._update_status("✅ Restauration ZIP vers dossier personnalisé terminée")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur restauration ZIP vers chemin: {e}", category="ui_backup")
            self._update_status("❌ Erreur lors de la restauration ZIP")
            show_translated_messagebox('error', "Erreur", 
                                    "Erreur durant la restauration ZIP :\n{error}", error=str(e))
    
    def _restore_to_path(self):
        """Restaure vers un chemin spécifique"""
        backup = self._get_selected_backup()
        if not backup:
            show_translated_messagebox('warning', "Avertissement", 
                                    "Veuillez sélectionner une sauvegarde à restaurer.")
            return
        
        try:
            backup_path = backup['backup_path']
            
            # Gestion différente selon le type de fichier
            if backup_path.endswith('.zip'):
                # Pour les ZIP, demander un dossier
                self._restore_zip_to_path()
                return
            
            # Pour les fichiers individuels
            original_filename = backup.get('source_filename', 'fichier_restaure')
            
            if not original_filename.endswith('.rpy'):
                original_filename += '.rpy'
            
            target_path = filedialog.asksaveasfilename(
                title="Restaurer vers...",
                initialfile=original_filename,
                defaultextension=".rpy",
                filetypes=[("Fichiers Ren'Py", "*.rpy"), ("Tous les fichiers", "*.*")]
            )
            
            if not target_path:
                return
            
            import shutil
            
            target_dir = os.path.dirname(target_path)
            if target_dir and not os.path.exists(target_dir):
                os.makedirs(target_dir, exist_ok=True)
            
            shutil.copy2(backup_path, target_path)
            
            # Pas de popup de confirmation - juste le statut
            self._update_status("✅ Restauration vers chemin personnalisé terminée")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur restauration vers chemin: {e}", category="ui_backup")
            self._update_status("❌ Erreur lors de la restauration")
            show_translated_messagebox('error', "Erreur", 
                                    "Erreur durant la restauration :\n{error}", error=str(e))
    
    def _delete_smart(self):
        """Suppression intelligente : sélection multiple si checkboxes cochées, sinon ligne sélectionnée"""
        try:
            # Vérifier s'il y a des checkboxes cochées
            selected_backups = [
                backup for backup in self.backups 
                if self.selected_items.get(backup.get('id'), False)
            ]
            
            if selected_backups:
                # Il y a des checkboxes cochées → suppression par lot
                self._delete_selected_batch()
            else:
                # Pas de checkbox cochée → suppression de la ligne sélectionnée
                self._delete_selected()
                
        except Exception as e:
            log_message("ERREUR", f"Erreur suppression intelligente: {e}", category="ui_backup")
    
    def _delete_selected_batch(self):
        """Supprime toutes les sauvegardes sélectionnées (par lot)"""
        try:
            # Récupérer tous les backups sélectionnés
            selected_backups = [
                backup for backup in self.backups 
                if self.selected_items.get(backup.get('id'), False)
            ]
            
            if not selected_backups:
                self._update_status("⚠️ Aucune sauvegarde sélectionnée")
                return
            
            # Calculer les statistiques pour la confirmation
            total_selected = len(selected_backups)
            total_size = sum(b.get('size', 0) for b in selected_backups) / (1024 * 1024)
            
            # Demander confirmation
            result = show_translated_messagebox(
                'askyesno',
                "Confirmer la Suppression par Lot",
                f"Supprimer {total_selected} sauvegarde(s) ?\n\n• Nombre : {total_selected} sauvegardes\n• Taille totale : {total_size:.1f} MB\n\n⚠️ Cette action est irréversible !"
            )
            
            if not result:
                return
            
            # Supprimer toutes les sauvegardes sélectionnées
            deleted_count = 0
            errors = []
            
            for backup in selected_backups:
                try:
                    os.remove(backup['backup_path'])
                    
                    # Nettoyer les métadonnées
                    if hasattr(self.manager, 'metadata') and backup.get('id') in self.manager.metadata:
                        del self.manager.metadata[backup['id']]
                    
                    deleted_count += 1
                    
                except Exception as e:
                    errors.append(f"{backup.get('source_filename', 'inconnu')}: {e}")
                    log_message("ERREUR", f"Erreur suppression backup {backup.get('id')}: {e}", category="ui_backup")
            
            # Sauvegarder les métadonnées
            if hasattr(self.manager, '_save_metadata'):
                self.manager._save_metadata()
            
            # Invalider le cache
            if hasattr(self.manager, '_invalidate_cache'):
                self.manager._invalidate_cache()
            
            # Nettoyer les dossiers vides
            self._cleanup_empty_directories()
            
            # Afficher le résultat
            if errors:
                self._update_status(f"⚠️ {deleted_count}/{total_selected} sauvegardes supprimées ({len(errors)} erreurs)")
            else:
                self._update_status(f"✅ {deleted_count} sauvegarde(s) supprimée(s) avec succès")
            
            # Recharger les données
            self._load_data()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur suppression par lot: {e}", category="ui_backup")
            self._update_status("❌ Erreur lors de la suppression par lot")
    
    def _delete_selected(self):
        """Supprime la sauvegarde sélectionnée"""
        backup = self._get_selected_backup()
        if not backup:
            show_translated_messagebox('warning', "Avertissement", 
                                     "Veuillez sélectionner une sauvegarde à supprimer.")
            return
        
        try:
            # Récupérer la description du type
            if hasattr(self.manager, 'BACKUP_DESCRIPTIONS'):
                type_desc = self.manager.BACKUP_DESCRIPTIONS.get(backup['type'], backup['type'])
            else:
                type_desc = str(backup['type'])
            
            result = show_translated_messagebox(
                'askyesno',
                "Confirmer la Suppression",
                "Supprimer définitivement cette sauvegarde ?\n\n• Fichier : {filename}\n• Jeu : {game}\n• Type : {type}\n• Taille : {size:.1f} MB\n\nCette action est irréversible !",
                filename=backup.get('source_filename', 'inconnu'),
                game=backup['game_name'],
                type=type_desc,
                size=backup['size'] / (1024*1024)
            )
            
            if not result:
                return
            
            try:
                os.remove(backup['backup_path'])
                
                if hasattr(self.manager, 'metadata') and backup.get('id') in self.manager.metadata:
                    del self.manager.metadata[backup['id']]
                    if hasattr(self.manager, '_save_metadata'):
                        self.manager._save_metadata()
                
                # Invalider le cache après suppression
                if hasattr(self.manager, '_invalidate_cache'):
                    self.manager._invalidate_cache()
                
                # Nettoyer les dossiers vides
                self._cleanup_empty_directories()
                
                # Pas de popup de confirmation - juste le statut
                self._load_data()  # Recharger les données
                self._update_status("✅ Sauvegarde supprimée avec succès")
                
            except Exception as e:
                self._update_status("❌ Erreur lors de la suppression")
                show_translated_messagebox('error', "Erreur de Suppression", 
                                         "Erreur lors de la suppression :\n{error}", error=str(e))
                
        except Exception as e:
            log_message("ERREUR", f"Erreur suppression: {e}", category="ui_backup")
            self._update_status("❌ Erreur lors de la suppression")
            show_translated_messagebox('error', "Erreur", 
                                     "Erreur durant la suppression :\n{error}", error=str(e))

    def _sort_column(self, col, reverse):
        """Tri les colonnes de la TreeView"""
        try:
            # Basculer l'ordre de tri
            self.sort_reverse[col] = not self.sort_reverse[col]
            reverse = self.sort_reverse[col]
            
            # Récupérer tous les éléments
            items = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
            
            # Tri spécial selon la colonne
            if col == 'created':
                # Tri par date
                items.sort(key=lambda x: self._parse_date_for_sort(x[0]), reverse=reverse)
            elif col == 'size':
                # Tri par taille (convertir en bytes)
                items.sort(key=lambda x: self._parse_size_for_sort(x[0]), reverse=reverse)
            else:
                # Tri alphabétique standard
                items.sort(key=lambda x: x[0].lower(), reverse=reverse)
            
            # Réorganiser les éléments
            for index, (val, child) in enumerate(items):
                self.tree.move(child, '', index)
            
            # Mettre à jour les en-têtes pour indiquer le tri
            for column in self.tree['columns']:
                if column == col:
                    direction = " ↓" if reverse else " ↑"
                    current_text = self.tree.heading(column, 'text')
                    # Enlever les anciens indicateurs
                    current_text = current_text.replace(" ↑", "").replace(" ↓", "")
                    self.tree.heading(column, text=current_text + direction)
                else:
                    # Enlever les indicateurs des autres colonnes
                    current_text = self.tree.heading(column, 'text')
                    current_text = current_text.replace(" ↑", "").replace(" ↓", "")
                    self.tree.heading(column, text=current_text)
                    
        except Exception as e:
            log_message("ERREUR", f"Erreur tri colonne {col}: {e}", category="ui_backup")

    def _parse_date_for_sort(self, date_str):
        """Parse une date pour le tri"""
        try:
            return datetime.datetime.strptime(date_str, "%d/%m/%Y %H:%M")
        except:
            return datetime.datetime.min

    def _parse_size_for_sort(self, size_str):
        """Parse une taille pour le tri"""
        try:
            if 'KB' in size_str:
                return float(size_str.replace(' KB', '')) * 1024
            elif 'MB' in size_str:
                return float(size_str.replace(' MB', '')) * 1024 * 1024
            elif 'GB' in size_str:
                return float(size_str.replace(' GB', '')) * 1024 * 1024 * 1024
            else:
                return float(size_str.replace(' B', ''))
        except:
            return 0
    
    def _update_status(self, message):
        """Met à jour le message de statut - IDENTIQUE coherence checker"""
        self.status_label.config(text=f"📊 État: {message}")
    
    def _apply_theme_to_window(self):
        """Applique le thème à toute la fenêtre - IDENTIQUE coherence checker"""
        try:
            theme = theme_manager.get_theme()
            
            self.window.configure(bg=theme["bg"])
            
            def apply_theme_recursive(widget):
                try:
                    if isinstance(widget, tk.Frame):
                        widget.configure(bg=theme["bg"])
                    elif isinstance(widget, tk.Label):
                        widget_text = widget.cget('text')
                        if ('🗂️' in widget_text and 'Gestionnaire' in widget_text):
                            widget.configure(bg=theme["bg"], fg=theme["accent"])
                        else:
                            widget.configure(bg=theme["bg"], fg=theme["fg"])
                    elif isinstance(widget, tk.LabelFrame):
                        widget.configure(bg=theme["bg"], fg=theme["fg"])
                    elif isinstance(widget, tk.Entry):
                        widget.configure(
                            bg=theme["entry_bg"], 
                            fg=theme["entry_fg"],
                            insertbackground=theme["entry_fg"]
                        )
                    elif isinstance(widget, tk.Checkbutton) or isinstance(widget, tk.Radiobutton):
                        widget.configure(
                            bg=theme["bg"], 
                            fg=theme["fg"],
                            selectcolor=theme["bg"],
                            activebackground=theme["bg"],
                            activeforeground=theme["fg"]
                        )
                    elif isinstance(widget, tk.Canvas):
                        widget.configure(bg=theme["bg"])
                    
                    for child in widget.winfo_children():
                        apply_theme_recursive(child)
                        
                except Exception:
                    pass
            
            apply_theme_recursive(self.window)
            
            # Style TTK pour TreeView et Combobox - APPROCHE SIMPLE
            if self.tree:
                style = ttk.Style()
                
                # Configuration simple du style TreeView
                style.configure("Treeview",
                            background="#2d3748",
                            foreground="#e2e8f0",
                            fieldbackground="#2d3748")
                
                style.configure("Treeview.Heading",
                            background="#1a1f29",
                            foreground="#4a90e2",
                            font=('Segoe UI', 9, 'bold'),
                            relief="flat")
                
                style.configure("Treeview.Separator",
                            background="#000000",
                            width=1)
                
                # Styles uniformes pour les Combobox
                theme_manager.apply_uniform_combobox_style(style)
            
            self.window.update()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur application thème backup: {e}", category="ui_backup")

    def _ensure_single_instance(self):
        """S'assure qu'une seule instance du backup manager est ouverte"""
        try:
            # Fermer toute instance précédente
            if hasattr(show_unified_backup_manager, '_current_instance'):
                existing = show_unified_backup_manager._current_instance
                if existing and hasattr(existing, 'window'):
                    try:
                        if existing.window.winfo_exists():
                            existing.window.destroy()
                    except Exception:
                        pass
            
            # Enregistrer cette instance
            show_unified_backup_manager._current_instance = self
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur gestion instance unique backup: {e}", category="ui_backup")

    def _open_backup_folder(self):
        """Ouvre le dossier de sauvegardes dans l'explorateur"""
        try:
            from infrastructure.helpers.file_utils import open_folder_in_explorer, get_backup_folder_path
            
            backup_folder = get_backup_folder_path()
            
            if open_folder_in_explorer(backup_folder):
                log_message("INFO", f"Dossier de sauvegardes ouvert: {backup_folder}", category="ui_backup")
            else:
                from infrastructure.helpers.unified_functions import show_translated_messagebox
                show_translated_messagebox(
                    'warning',
                    "Dossier Inaccessible",
                    f"Impossible d'ouvrir le dossier de sauvegardes.\n\nChemin: {backup_folder}",
                    parent=self.window
                )
                
        except Exception as e:
            log_message("ERREUR", f"Erreur ouverture dossier sauvegardes: {e}", category="ui_backup")
            from infrastructure.helpers.unified_functions import show_translated_messagebox
            show_translated_messagebox(
                'error',
                "Erreur",
                f"Erreur lors de l'ouverture du dossier:\n{e}",
                parent=self.window
            )

    def _on_close(self):
        """Gestion de la fermeture de la fenêtre (cacher pour persistance)"""
        try:
            # Libérer le grab modal avant de cacher la fenêtre
            try:
                self.window.grab_release()
            except:
                pass
            
            # Cacher la fenêtre au lieu de la détruire (persistance)
            self.window.withdraw()
            
            log_message("DEBUG", "Fenêtre backup cachée (persistante)", category="ui_backup")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur fermeture interface backup: {e}", category="ui_backup")

# Export des fonctions principales
__all__ = [
    'show_unified_backup_manager',
    'UnifiedBackupDialog',
    'quick_backup_actions'
]