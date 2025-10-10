# ui/tab_settings/application_tab.py
# Onglet Interface & Application pour l'interface settings

"""
Onglet Interface & Application
- Configuration des ouvertures automatiques
- Options d'apparence et notifications
- Configuration de l'éditeur de code
- Actions système (nettoyage, reset)
"""

import tkinter as tk
from tkinter import ttk
from ui.themes import theme_manager
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message


def create_application_tab(parent, settings_instance):
    """Crée l'onglet Interface & Application"""
    theme = theme_manager.get_theme()
    
    tab_frame = tk.Frame(parent, bg=theme["bg"])
    
    # En-tête moderne avec titre
    header_frame = tk.Frame(tab_frame, bg=theme["bg"])
    header_frame.pack(fill='x', pady=(15, 10), padx=20)
    
    # Titre descriptif
    desc_label = tk.Label(
        header_frame,
        text="Configuration de l'apparence et du comportement de l'application",
        font=('Segoe UI', 10, 'bold'),
        justify='center',
        bg=theme["bg"],
        fg=theme["accent"]
    )
    desc_label.pack(fill='x', anchor='center')
    
    # Container principal
    main_container = tk.Frame(tab_frame, bg=theme["bg"])
    main_container.pack(fill='both', expand=True, padx=20, pady=15)
    
    # === SECTION 1: Ouvertures automatiques ===
    _create_auto_open_section(main_container, settings_instance)
    
    # Séparateur invisible
    _create_separator(main_container)
    
    # === SECTION 2: Apparence et notifications ===
    _create_appearance_section(main_container, settings_instance)
    
    # Séparateur invisible
    _create_separator(main_container)
    
    # === SECTION 3: Éditeur de code ===
    _create_editor_section(main_container, settings_instance)
    
    # Séparateur invisible
    _create_separator(main_container)
    
    # === SECTION 4: Actions système ===
    _create_system_actions_section(main_container, settings_instance)
    
    return tab_frame


def _create_separator(parent):
    """Crée un séparateur invisible"""
    separator = tk.Frame(parent, height=20, bg=parent.cget('bg'))
    separator.pack(fill='x')


def _create_auto_open_section(parent, settings_instance):
    """Crée la section Ouvertures automatiques"""
    theme = theme_manager.get_theme()
    
    # Titre de section
    title_label = tk.Label(
        parent,
        text="🚀 Ouvertures automatiques",
        font=('Segoe UI', 12, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    title_label.pack(anchor='w', pady=(0, 10))
    
    # Container pour les options en grille
    options_container = tk.Frame(parent, bg=theme["bg"])
    options_container.pack(fill='x', pady=(0, 10))
    
    # Colonne gauche
    left_column = tk.Frame(options_container, bg=theme["bg"])
    left_column.pack(side='left', fill='both', expand=True, padx=(0, 20))
    
    # Colonne droite
    right_column = tk.Frame(options_container, bg=theme["bg"])
    right_column.pack(side='right', fill='both', expand=True, padx=(20, 0))
    
    auto_options = [
        (settings_instance.auto_open_files_var, "🚀", "Ouverture automatique des fichiers"),
        (settings_instance.auto_open_folders_var, "📁", "Ouverture automatique des dossiers"),
        (settings_instance.auto_open_coherence_report_var, "📊", "Ouverture automatique du rapport de cohérence"),
        (settings_instance.show_output_path_var, "📂", "Affichage du champ de chemin de sortie"),
        (settings_instance.project_sync_var, "🔄", "Synchronisation centralisée des projets")
    ]
    
    # Répartir les options sur 2 colonnes
    for i, (var, icon, text) in enumerate(auto_options):
        column = left_column if i < 3 else right_column
        
        checkbox = tk.Checkbutton(
            column,
            text=f"{icon} {text}",
            variable=var,
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"],
            selectcolor=theme["bg"],
            activebackground=theme["bg"],
            activeforeground=theme["fg"],
            anchor='w',
            command=settings_instance._on_interface_option_changed
        )
        checkbox.pack(anchor='w', pady=3)
        
        # Ajouter au cache du ThemeManager
        theme_manager._cache_widget(checkbox, 'checkbuttons')


def _update_editor_combo_values(settings_instance):
    """Met à jour les valeurs de la combobox éditeur en fonction de l'éditeur personnalisé"""
    try:
        # Obtenir le chemin de l'éditeur personnalisé depuis la variable directement
        custom_editor_path = ""
        if hasattr(settings_instance, 'custom_editor_var'):
            custom_editor_path = settings_instance.custom_editor_var.get().strip()
        
        # Fallback vers la config si la variable n'existe pas
        if not custom_editor_path:
            custom_editor_path = config_manager.get("custom_editor_path", "")
        
        if custom_editor_path and custom_editor_path.strip():
            # Extraire le nom de l'exécutable
            import os
            editor_name = os.path.basename(custom_editor_path)
            # Enlever l'extension .exe si présente
            if editor_name.lower().endswith('.exe'):
                editor_name = editor_name[:-4]
            
            # Mettre à jour les valeurs de la combobox
            editor_options = ['Défaut Windows', editor_name]
            settings_instance.editor_combo['values'] = editor_options
            
            # Si l'éditeur personnalisé est sélectionné, le garder sélectionné
            if settings_instance.editor_choice_var.get() == editor_name:
                settings_instance.editor_combo.set(editor_name)
            else:
                settings_instance.editor_combo.set("Défaut Windows")
        else:
            # Pas d'éditeur personnalisé, utiliser les valeurs par défaut
            editor_options = ['Défaut Windows']
            settings_instance.editor_combo['values'] = editor_options
            settings_instance.editor_combo.set("Défaut Windows")
            
    except Exception as e:
        log_message("ERREUR", f"Erreur mise à jour combobox éditeur: {e}", category="application_tab")

def _create_appearance_section(parent, settings_instance):
    theme = theme_manager.get_theme()
    
    # Titre de section
    title_label = tk.Label(
        parent,
        text="🎨 Apparence et notifications",
        font=('Segoe UI', 12, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    title_label.pack(anchor='w', pady=(0, 10))
    
    # Container pour les options
    options_container = tk.Frame(parent, bg=theme["bg"])
    options_container.pack(fill='x', pady=(0, 10))
    
    # Mode de notification
    notification_frame = tk.Frame(options_container, bg=theme["bg"])
    notification_frame.pack(fill='x', pady=(0, 10))
    
    notification_label = tk.Label(
        notification_frame,
        text="🔔 Mode de notification des résultats :",
        font=('Segoe UI', 10, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    notification_label.pack(side='left')
    
    settings_instance.notification_combo = ttk.Combobox(
        notification_frame,
        textvariable=settings_instance.notification_mode_var,
        values=['Statut seulement', 'Popups détaillés'],
        state='readonly',
        font=('Segoe UI', 9),
        width=18
    )
    settings_instance.notification_combo.pack(side='left', padx=(10, 0))
    settings_instance.notification_combo.bind('<<ComboboxSelected>>', settings_instance._on_notification_mode_changed)

    # Container pour les checkboxes
    checkboxes_container = tk.Frame(options_container, bg=theme["bg"])
    checkboxes_container.pack(fill='x')
    
    # Mode Sombre
    dark_checkbox = tk.Checkbutton(
        checkboxes_container,
        text="🌙 Mode sombre",
        variable=settings_instance.dark_mode_var,
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        selectcolor=theme["bg"],
        activebackground=theme["bg"],
        activeforeground=theme["fg"],
        anchor='w',
        command=settings_instance._on_dark_mode_changed
    )
    dark_checkbox.pack(anchor='w', pady=3)
    
    # Ajouter au cache du ThemeManager
    theme_manager._cache_widget(dark_checkbox, 'checkbuttons')
    
    # Debug Mode
    debug_checkbox = tk.Checkbutton(
        checkboxes_container,
        text="🐛 Mode debug complet",
        variable=settings_instance.debug_mode_var,
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        selectcolor=theme["bg"],
        activebackground=theme["bg"],
        activeforeground=theme["fg"],
        anchor='w',
        command=settings_instance._on_debug_mode_changed
    )
    debug_checkbox.pack(anchor='w', pady=3)
    
    # Ajouter au cache du ThemeManager
    theme_manager._cache_widget(debug_checkbox, 'checkbuttons')


def _create_editor_section(parent, settings_instance):
    """Crée la section Éditeur de code"""
    theme = theme_manager.get_theme()
    
    # Titre de section
    title_label = tk.Label(
        parent,
        text="📝 Éditeur de code",
        font=('Segoe UI', 12, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    title_label.pack(anchor='w', pady=(0, 10))
    
    # Description
    desc_label = tk.Label(
        parent,
        text="Éditeur pour ouvrir les fichiers depuis l'interface temps réel et les rapports HTML.",
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        wraplength=600,
        justify='left'
    )
    desc_label.pack(anchor='w', pady=(0, 10))
    
    # Sélection d'éditeur
    editor_selection_frame = tk.Frame(parent, bg=theme["bg"])
    editor_selection_frame.pack(fill='x', pady=(0, 10))
    
    editor_label = tk.Label(
        editor_selection_frame,
        text="📝 Éditeur :",
        font=('Segoe UI', 10, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    editor_label.pack(side='left')
    
    editor_options = ['Défaut Windows']  # Valeurs initiales, seront mises à jour
    settings_instance.editor_combo = ttk.Combobox(
        editor_selection_frame,
        textvariable=settings_instance.editor_choice_var,
        values=editor_options,
        state='readonly',
        font=('Segoe UI', 9),
        width=18
    )
    settings_instance.editor_combo.pack(side='left', padx=(10, 0))
    settings_instance.editor_combo.bind('<<ComboboxSelected>>', settings_instance._on_editor_choice_changed)
    
    # Mettre à jour les valeurs de la combobox
    _update_editor_combo_values(settings_instance)


def _create_system_actions_section(parent, settings_instance):
    """Crée la section Actions système"""
    theme = theme_manager.get_theme()
    
    # Titre de section
    title_label = tk.Label(
        parent,
        text="🔧 Actions système",
        font=('Segoe UI', 12, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    title_label.pack(anchor='w', pady=(0, 10))
    
    # Container pour les boutons
    buttons_container = tk.Frame(parent, bg=theme["bg"])
    buttons_container.pack(fill='x')

    clean_temp_btn = tk.Button(
        buttons_container,
        text="🧹 Nettoyer les fichiers temporaires",
        command=settings_instance._clean_temp_only,
        bg=theme["button_powerful_bg"],
        fg="#000000",
        font=('Segoe UI', 11, 'bold'),
        pady=8,
        width=35
    )
    clean_temp_btn.pack(side='left', padx=(0, 10))

    reset_btn = tk.Button(
        buttons_container,
        text="🔄 Réinitialiser l'application",
        command=settings_instance._reset_application,
        bg=theme["button_danger_bg"],
        fg="#000000",
        font=('Segoe UI', 11, 'bold'),
        pady=8,
        width=35
    )
    reset_btn.pack(side='left', padx=(0, 10))