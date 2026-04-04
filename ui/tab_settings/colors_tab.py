# ui/tab_settings/colors_tab.py
# Onglet thème des boutons (presets uniquement) pour l'interface settings

"""
Onglet Couleurs des boutons
- Presets de couleurs (Classique, Océan, Forêt, etc.)
- Remise au thème par défaut
"""

import tkinter as tk
from tkinter import ttk
from ui.themes import theme_manager
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import show_custom_messagebox


def create_colors_tab(parent, settings_instance):
    """Crée l'onglet Couleurs — parent = frame scrollable (ajout au notebook fait par l'interface)."""
    theme = theme_manager.get_theme()

    tab_frame = tk.Frame(parent, bg=theme["bg"])
    tab_frame.pack(fill='both', expand=True)

    header_frame = tk.Frame(tab_frame, bg=theme["bg"])
    header_frame.pack(fill='x', pady=(15, 10), padx=20)

    desc_label = tk.Label(
        header_frame,
        text="Choisissez un thème de couleurs pour les boutons (presets prédéfinis)",
        font=('Segoe UI', 10, 'bold'),
        justify='center',
        bg=theme["bg"],
        fg=theme["accent"]
    )
    desc_label.pack(fill='x', anchor='center')

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

    main_container = tk.Frame(tab_frame, bg=theme["bg"])
    main_container.pack(fill='both', expand=True, padx=20, pady=15)

    _create_presets_section(main_container, settings_instance)


def _create_presets_section(parent, settings_instance):
    """Section : choix d'un preset et application."""
    theme = theme_manager.get_theme()

    title_label = tk.Label(
        parent,
        text="🎨 Presets de couleurs",
        font=('Segoe UI', 12, 'bold'),
        bg=theme["bg"],
        fg=theme["accent"]
    )
    title_label.pack(anchor='w', pady=(0, 10))

    presets_container = tk.Frame(parent, bg=theme["bg"])
    presets_container.pack(fill='x', pady=(0, 10))

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


def _show_colors_help(settings_instance):
    """Aide : presets uniquement."""
    try:
        help_text = [
            ("🎨 AIDE — Couleurs des boutons\n", "bold"),
            ("\n", ""),
            ("Les presets définissent d'un coup les couleurs des catégories de boutons\n", ""),
            ("(actions principales, secondaires, danger, navigation, etc.).\n", ""),
            ("\n", ""),
            ("• Choisissez un nom dans la liste puis « Appliquer le preset ».\n", ""),
            ("• « Remettre les couleurs par défaut » recharge le thème Classique v1.\n", ""),
            ("\n", ""),
            ("Les changements sont enregistrés dans la configuration.\n", "italic"),
        ]

        show_custom_messagebox(
            'info',
            'Aide — Thème des boutons',
            help_text,
            theme_manager.get_theme(),
            parent=settings_instance.window
        )

    except Exception as e:
        log_message("ERREUR", f"Erreur affichage aide couleurs: {e}", category="colors_tab")
