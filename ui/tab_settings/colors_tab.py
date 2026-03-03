# ui/tab_settings/colors_tab.py
# Onglet Couleurs des boutons pour l'interface settings

"""
Onglet Couleurs des boutons
- Presets de couleurs
- Personnalisation des couleurs par catégorie
- Aperçu en temps réel
- Reset des couleurs par défaut
"""

import tkinter as tk
from tkinter import ttk, colorchooser
from ui.themes import theme_manager
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import show_custom_messagebox


def create_colors_tab(parent, settings_instance):
    """Crée l'onglet Couleurs - parent = frame scrollable (ajout au notebook fait par l'interface)."""
    theme = theme_manager.get_theme()
    
    tab_frame = tk.Frame(parent, bg=theme["bg"])
    tab_frame.pack(fill='both', expand=True)
    
    # En-tête moderne avec titre et bouton d'aide
    header_frame = tk.Frame(tab_frame, bg=theme["bg"])
    header_frame.pack(fill='x', pady=(15, 10), padx=20)
    
    # Titre descriptif centré
    desc_label = tk.Label(
        header_frame,
        text="Personnalisez les couleurs des boutons ou choisissez un preset",
        font=('Segoe UI', 10, 'bold'),
        justify='center',
        bg=theme["bg"],
        fg=theme["accent"]
    )
    desc_label.pack(fill='x', anchor='center')
    
    # Bouton d'aide moderne à droite
    help_button = tk.Button(
        header_frame,
        text="À quoi ça sert ?",
        command=lambda: _show_colors_help(settings_instance),
        bg=theme["button_secondary_bg"],
        fg="#000000",
        font=('Segoe UI', 10, 'bold'),
        width=15,
        height=1,
        relief='flat',
        cursor='hand2'
    )
    help_button.pack(side='right', anchor='e')
    
    # Container principal
    main_container = tk.Frame(tab_frame, bg=theme["bg"])
    main_container.pack(fill='both', expand=True, padx=20, pady=15)
    
    # === SECTION 1: Presets de couleurs ===
    _create_presets_section(main_container, settings_instance)
    
    # Séparateur invisible
    _create_separator(main_container)
    
    # === SECTION 2: Personnalisation des couleurs ===
    _create_color_customization_section(main_container, settings_instance)


def _create_separator(parent):
    """Crée un séparateur invisible"""
    separator = tk.Frame(parent, height=20, bg=parent.cget('bg'))
    separator.pack(fill='x')


def _create_presets_section(parent, settings_instance):
    """Crée la section Presets de couleurs"""
    theme = theme_manager.get_theme()
    
    # Titre de section
    title_label = tk.Label(
        parent,
        text="🎨 Presets de couleurs",
        font=('Segoe UI', 12, 'bold'),
        bg=theme["bg"],
        fg=theme["accent"]
    )
    title_label.pack(anchor='w', pady=(0, 10))
    
    # Container pour la sélection de preset
    presets_container = tk.Frame(parent, bg=theme["bg"])
    presets_container.pack(fill='x', pady=(0, 10))
    
    # Label et combobox pour les presets
    preset_label = tk.Label(
        presets_container,
        text="Choisir un preset :",
        font=('Segoe UI', 10),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    preset_label.pack(side='left')
    
    settings_instance.preset_var = tk.StringVar()
    preset_combo = ttk.Combobox(
        presets_container,
        textvariable=settings_instance.preset_var,
        values=config_manager.get_available_presets(),
        state='readonly',
        font=('Segoe UI', 9),
        width=30
    )
    preset_combo.pack(side='left', padx=(10, 10))
    preset_combo.bind('<<ComboboxSelected>>', settings_instance._on_preset_selected)
    
    # Détecter et afficher le preset actuel
    current_preset = config_manager.get_current_preset_name()
    settings_instance.preset_var.set(current_preset)
    
    apply_preset_btn = tk.Button(
        presets_container,
        text="Appliquer le preset",
        command=settings_instance._apply_selected_preset,
        bg=theme.get("button_secondary_bg", "#ADD8E6"),
        fg="#000000",
        font=('Segoe UI', 9, 'bold'),
        pady=4,
        width=18
    )
    apply_preset_btn.pack(side='left', padx=(5, 10))

    # Ajouter le bouton de reset à droite
    reset_colors_btn = tk.Button(
        presets_container,
        text="🔄 Remettre les couleurs par défaut",
        command=settings_instance._reset_theme_colors,
        bg=theme.get("button_danger_bg", "#F08080"),
        fg="#000000",
        font=('Segoe UI', 9, 'bold'),
        pady=4,
        width=35
    )
    reset_colors_btn.pack(side='left', padx=(5, 0))


def _create_color_customization_section(parent, settings_instance):
    """Crée la section Personnalisation des couleurs"""
    theme = theme_manager.get_theme()
    current_colors = config_manager.get_theme_colors()
    
    # Titre de section
    title_label = tk.Label(
        parent,
        text="🎨 Personnalisation des couleurs",
        font=('Segoe UI', 12, 'bold'),
        bg=theme["bg"],
        fg=theme["accent"]
    )
    title_label.pack(anchor='w', pady=(0, 10))
    
    # Définition des catégories avec leurs couleurs
    color_categories = [
        ("🟢 Actions Principales", [
            ("button_primary_bg", "Actions positives (Extraire, Démarrer, Sélectionner tout)")
        ]),
        ("🔵 Actions Secondaires", [
            ("button_secondary_bg", "Actions standards (Générer, Paramètres, Construire)")
        ]),
        ("🟡 Actions Alternatives", [
            ("button_tertiary_bg", "Réinitialisation et alternatives (Par défaut, Annuler)")
        ]),
        ("🔴 Actions de Danger", [
            ("button_danger_bg", "Fermer, Quitter, Supprimer, Désélectionner")
        ]),
        ("🟣 Modules et Fonctionnalités", [
            ("button_feature_bg", "Ajouter modules, nouvelles fonctions")
        ]),
        ("🟠 Actions Puissantes", [
            ("button_powerful_bg", "Nettoyage, actions combinées importantes")
        ]),
        ("⚫ Outils Développeur", [
            ("button_devtool_bg", "Console développeur et outils avancés")
        ]),
        ("🔵 Navigation Fichiers", [
            ("button_nav_bg", "Parcourir, Ouvrir dossiers et fichiers")
        ]),
        ("⚪ Aide et Information", [
            ("button_help_bg", "Aide, À propos, Instructions et support")
        ]),
        ("⚫ Utilitaires Divers", [
            ("button_utility_bg", "Scanner, Coller, actions diverses")
        ])
    ]
    
    # Container pour les deux colonnes avec hauteur fixe
    columns_container = tk.Frame(parent, bg=theme["bg"], height=400)
    columns_container.pack(fill='both', expand=True)
    columns_container.pack_propagate(False)
    
    # Colonnes gauche et droite avec largeur fixe
    left_column = tk.Frame(columns_container, bg=theme["bg"], width=380)
    left_column.pack(side='left', fill='y', padx=(0, 10))
    left_column.pack_propagate(False)
    
    right_column = tk.Frame(columns_container, bg=theme["bg"], width=380)
    right_column.pack(side='right', fill='y', padx=(10, 0))
    right_column.pack_propagate(False)
    
    settings_instance.color_buttons = {}
    
    # Répartition sur deux colonnes
    for i, (category_name, colors) in enumerate(color_categories):
        # Alterner entre colonne gauche (pair) et droite (impair)
        target_column = left_column if i % 2 == 0 else right_column
        
        # Frame de catégorie avec hauteur fixe
        category_frame = tk.LabelFrame(
            target_column,
            text=category_name,
            font=('Segoe UI', 10, 'bold'),
            bg=theme["bg"],
            fg=theme["fg"],
            height=70
        )
        category_frame.pack(fill='x', pady=2)
        category_frame.pack_propagate(False)
        
        # Ajouter au cache du ThemeManager
        theme_manager._cache_widget(category_frame, 'labelframes')
        
        for color_key, description in colors:
            color_frame = tk.Frame(category_frame, bg=theme["bg"])
            color_frame.pack(fill='both', expand=True, padx=10, pady=8)
            
            # Label description avec wraplength pour éviter débordement
            desc_label = tk.Label(
                color_frame,
                text=description,
                font=('Segoe UI', 8),
                bg=theme["bg"],
                fg=theme["fg"],
                anchor='w',
                wraplength=280,
                justify='left'
            )
            desc_label.pack(side='left', fill='both', expand=True)
            
            # Bouton d'exemple avec texte représentatif
            example_text = _get_example_button_text(color_key)
            color_btn = tk.Button(
                color_frame,
                text=example_text,
                bg=current_colors.get(color_key, "#D3D3D3"),
                fg="#000000",
                font=('Segoe UI', 8, 'bold'),
                width=12,
                height=1,
                relief='solid',
                borderwidth=2,
                cursor='hand2',
                command=lambda key=color_key: settings_instance._change_color(key)
            )
            color_btn.pack(side='right', padx=(5, 0))
            
            # Ajouter effet hover pour montrer que c'est cliquable
            _add_hover_effect(color_btn)
            
            settings_instance.color_buttons[color_key] = color_btn
    
def _add_hover_effect(button):
    """Ajoute un effet hover au bouton pour montrer qu'il est cliquable"""
    original_config = {
        'borderwidth': button.cget('borderwidth'),
        'relief': button.cget('relief')
    }
    
    def on_enter(event):
        """Au survol : bordure plus épaisse et relief raised"""
        button.config(borderwidth=3, relief='raised')
    
    def on_leave(event):
        """En sortie : retour à l'état normal"""
        button.config(
            borderwidth=original_config['borderwidth'],
            relief=original_config['relief']
        )
    
    button.bind('<Enter>', on_enter)
    button.bind('<Leave>', on_leave)


def _get_example_button_text(color_key):
    """Retourne un texte d'exemple pour chaque type de bouton"""
    examples = {
        "button_primary_bg": "Extraire",
        "button_secondary_bg": "Paramètres", 
        "button_tertiary_bg": "Annuler",
        "button_danger_bg": "Fermer",
        "button_feature_bg": "Ajouter",
        "button_powerful_bg": "Nettoyer",
        "button_devtool_bg": "Console",
        "button_nav_bg": "Parcourir",
        "button_help_bg": "Aide",
        "button_utility_bg": "Scanner"
    }
    return examples.get(color_key, "Exemple")


def _show_colors_help(settings_instance):
    """Affiche l'aide pour la personnalisation des couleurs"""
    try:
        help_text = [
            ("🎨 AIDE - Personnalisation des couleurs\n", "bold"),
            ("\n", ""),
            ("🎨 Presets de couleurs\n", "bold_green"),
            ("• Choisissez un preset prédéfini pour des couleurs harmonieuses\n", ""),
            ("• Les presets sont optimisés pour l'accessibilité et la lisibilité\n", ""),
            ("• 'Défaut (Accessible)' : Couleurs équilibrées et accessibles\n", "italic"),
            ("\n", ""),
            ("🔧 Personnalisation manuelle\n", "bold_blue"),
            ("• Cliquez sur chaque bouton d'exemple pour changer sa couleur\n", ""),
            ("• Les changements sont appliqués immédiatement\n", ""),
            ("• Chaque catégorie a une fonction spécifique dans l'interface\n", ""),
            ("\n", ""),
            ("📋 Catégories de boutons\n", "bold_yellow"),
            ("• Actions Principales : Actions positives (Extraire, Démarrer)\n", ""),
            ("• Actions Secondaires : Actions standards (Paramètres, Générer)\n", ""),
            ("• Actions de Danger : Fermer, Quitter, Supprimer\n", ""),
            ("• Actions Puissantes : Nettoyage, actions importantes\n", ""),
            ("• Navigation : Parcourir, Ouvrir fichiers et dossiers\n", ""),
            ("\n", ""),
            ("💡 Conseils\n", "bold"),
            ("• Utilisez des couleurs contrastées pour une meilleure lisibilité\n", ""),
            ("• Les couleurs sont sauvegardées automatiquement\n", ""),
            ("• Vous pouvez réinitialiser à tout moment avec 'Par défaut'\n", "")
        ]
        
        show_custom_messagebox(
            'info',
            'Aide - Personnalisation des couleurs',
            help_text,
            theme_manager.get_theme(),
            parent=settings_instance.window
        )
        
    except Exception as e:
        log_message("ERREUR", f"Erreur affichage aide couleurs: {e}", category="colors_tab")