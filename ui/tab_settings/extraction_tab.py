# ui/tab_settings/extraction_tab.py
# Onglet Extraction & Protection pour l'interface settings

"""
Onglet Extraction & Protection
- Configuration de la protection automatique du contenu
- Options de détection des doublons
- Patterns de protection personnalisés
- Limite de lignes par fichier
- Mode de sauvegarde par défaut
"""

import tkinter as tk
from tkinter import ttk
from ui.themes import theme_manager
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message


def create_extraction_tab(parent, settings_instance):
    """Crée l'onglet Extraction & Protection"""
    theme = theme_manager.get_theme()
    
    tab_frame = tk.Frame(parent, bg=theme["bg"])
    
    # En-tête moderne avec titre et bouton d'aide
    header_frame = tk.Frame(tab_frame, bg=theme["bg"])
    header_frame.pack(fill='x', pady=(15, 10), padx=20)
    
    # Titre descriptif centré
    desc_label = tk.Label(
        header_frame,
        text="Configuration de la protection automatique du contenu lors de l'extraction",
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
        command=settings_instance._show_extraction_protection_help,
        bg=theme["button_secondary_bg"],
        fg="#000000",
        font=('Segoe UI', 10, 'bold'),
        width=15,
        height=1,
        relief='flat',
        cursor='hand2'
    )
    help_button.pack(side='right', anchor='e')
    
    # Contenu principal sans sections
    _create_protection_options(tab_frame, settings_instance)
    
    return tab_frame


def _create_protection_options(parent, settings_instance):
    """Crée les options de protection avec disposition en 6 lignes"""
    theme = theme_manager.get_theme()
    
    # Container principal
    main_container = tk.Frame(parent, bg=theme["bg"])
    main_container.pack(fill='x', padx=20, pady=15)
    
    # Variables pour les patterns courts
    settings_instance.code_pattern_var = tk.StringVar(value="RENPY_CODE_001")
    settings_instance.asterisk_pattern_var = tk.StringVar(value="RENPY_ASTERIX_001") 
    settings_instance.tilde_pattern_var = tk.StringVar(value="RENPY_TILDE_001")
    
    # === LIGNE 1: Checkboxes côte à côte ===
    line1_frame = tk.Frame(main_container, bg=theme["bg"])
    line1_frame.pack(fill='x', pady=(0, 15))
    
    # Titre des options de protection
    protection_title = tk.Label(
        line1_frame,
        text="🔧 Options de protection",
        font=('Segoe UI', 10, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    protection_title.pack(anchor='w', pady=(0, 5))
    
    # Container pour les checkboxes
    checkboxes_container = tk.Frame(line1_frame, bg=theme["bg"])
    checkboxes_container.pack(fill='x')
    
    # Checkbox 1
    checkbox1 = tk.Checkbutton(
        checkboxes_container,
        text="Détecter et gérer les doublons",
        variable=settings_instance.detect_duplicates_var,
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        selectcolor=theme["bg"],
        activebackground=theme["bg"],
        activeforeground=theme["fg"],
        anchor='w'
    )
    checkbox1.pack(side='left', padx=(0, 20))
    
    # Checkbox 2
    checkbox2 = tk.Checkbutton(
        checkboxes_container,
        text="📊 Suivi de progression des projets",
        variable=settings_instance.project_progress_tracking_var,
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        selectcolor=theme["bg"],
        activebackground=theme["bg"],
        activeforeground=theme["fg"],
        anchor='w'
    )
    checkbox2.pack(side='left')
    
    # === LIGNE 2: Bouton cohérence + limite de lignes ===
    line2_frame = tk.Frame(main_container, bg=theme["bg"])
    line2_frame.pack(fill='x', pady=(0, 15))
    
    # Bouton cohérence
    coherence_btn = tk.Button(
        line2_frame,
        text="⚙️ Configurer les contrôles après extraction",
        command=settings_instance._show_coherence_quick_settings,
        bg=theme["button_secondary_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    coherence_btn.pack(side='left', padx=(0, 20))
    
    # Limite de lignes
    limit_label = tk.Label(
        line2_frame,
        text="📄 Limite par fichier :",
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    limit_label.pack(side='left', padx=(0, 5))
    
    limit_entry = tk.Entry(
        line2_frame,
        textvariable=settings_instance.extraction_line_limit_var,
        font=('Segoe UI', 10),
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        width=8,
        justify='center'
    )
    limit_entry.pack(side='left', padx=(0, 5), ipady=4)
    limit_entry.bind('<KeyRelease>', settings_instance._on_line_limit_changed)
    
    unit_label = tk.Label(
        line2_frame,
        text="lignes",
        font=('Segoe UI', 8),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    unit_label.pack(side='left')
    
    # === LIGNE 3: Mode de sauvegarde (pleine largeur) ===
    line3_frame = tk.Frame(main_container, bg=theme["bg"])
    line3_frame.pack(fill='x', pady=(0, 15))
    
    save_mode_label = tk.Label(
        line3_frame,
        text="💾 Mode de sauvegarde par défaut :",
        font=('Segoe UI', 10, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    save_mode_label.pack(side='left')

    settings_instance.save_mode_combo = ttk.Combobox(
        line3_frame,
        textvariable=settings_instance.default_save_mode_var,
        values=["Écraser l'original", "Créer nouveau fichier"],
        state='readonly',
        font=('Segoe UI', 9),
        width=25
    )
    settings_instance.save_mode_combo.pack(side='left', padx=(10, 5))
    settings_instance.save_mode_combo.bind('<<ComboboxSelected>>', settings_instance._on_save_mode_changed)
    
    # === LIGNE 4: Codes/Variables + aperçu ===
    # Titre de la section patterns
    patterns_section_title = tk.Label(
        main_container,
        text="🔧 Patterns de protection personnalisés",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    patterns_section_title.pack(anchor='w', pady=(20, 10))
    
    line4_frame = tk.Frame(main_container, bg=theme["bg"])
    line4_frame.pack(fill='x', pady=(0, 10))
    
    # Titre Codes/Variables
    codes_title = tk.Label(
        line4_frame,
        text="🔤 Codes/Variables",
        font=('Segoe UI', 10, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    codes_title.pack(anchor='w', pady=(0, 5))
    
    # Container pour le champ et l'aperçu
    codes_container = tk.Frame(line4_frame, bg=theme["bg"])
    codes_container.pack(fill='x')
    
    # Entry Codes/Variables
    codes_entry = tk.Entry(
        codes_container,
        textvariable=settings_instance.code_pattern_var,
        font=('Segoe UI', 10, 'bold'),
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        insertbackground=theme["entry_fg"],
        relief='solid',
        borderwidth=2,
        width=22,
        justify='center'
    )
    codes_entry.pack(side='left', padx=(0, 15), ipady=4)
    codes_entry.bind('<KeyRelease>', settings_instance._on_pattern_changed)
    
    # Aperçu Codes/Variables
    settings_instance.codes_preview = tk.Text(
        codes_container,
        height=1,
        font=('Consolas', 11),
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        relief='solid',
        borderwidth=1,
        state='disabled',
        wrap='word'
    )
    settings_instance.codes_preview.tag_configure("center", justify='center')
    settings_instance.codes_preview.pack(side='left', fill='x', expand=True)
    
    # === LIGNE 5: Astérisques + aperçu ===
    line5_frame = tk.Frame(main_container, bg=theme["bg"])
    line5_frame.pack(fill='x', pady=(0, 10))
    
    # Titre Astérisques
    asterisks_title = tk.Label(
        line5_frame,
        text="⭐ Astérisques",
        font=('Segoe UI', 10, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    asterisks_title.pack(anchor='w', pady=(0, 5))
    
    # Container pour le champ et l'aperçu
    asterisks_container = tk.Frame(line5_frame, bg=theme["bg"])
    asterisks_container.pack(fill='x')
    
    # Entry Astérisques
    asterisks_entry = tk.Entry(
        asterisks_container,
        textvariable=settings_instance.asterisk_pattern_var,
        font=('Segoe UI', 10, 'bold'),
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        insertbackground=theme["entry_fg"],
        relief='solid',
        borderwidth=2,
        width=22,
        justify='center'
    )
    asterisks_entry.pack(side='left', padx=(0, 15), ipady=4)
    asterisks_entry.bind('<KeyRelease>', settings_instance._on_pattern_changed)
    
    # Aperçu Astérisques
    settings_instance.asterisks_preview = tk.Text(
        asterisks_container,
        height=1,
        font=('Consolas', 11),
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        relief='solid',
        borderwidth=1,
        state='disabled',
        wrap='word'
    )
    settings_instance.asterisks_preview.tag_configure("center", justify='center')
    settings_instance.asterisks_preview.pack(side='left', fill='x', expand=True)
    
    # === LIGNE 6: Tildes + aperçu ===
    line6_frame = tk.Frame(main_container, bg=theme["bg"])
    line6_frame.pack(fill='x', pady=(0, 15))
    
    # Titre Tildes
    tildes_title = tk.Label(
        line6_frame,
        text="〰️ Tildes",
        font=('Segoe UI', 10, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    tildes_title.pack(anchor='w', pady=(0, 5))
    
    # Container pour le champ et l'aperçu
    tildes_container = tk.Frame(line6_frame, bg=theme["bg"])
    tildes_container.pack(fill='x')
    
    # Entry Tildes
    tildes_entry = tk.Entry(
        tildes_container,
        textvariable=settings_instance.tilde_pattern_var,
        font=('Segoe UI', 10, 'bold'),
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        insertbackground=theme["entry_fg"],
        relief='solid',
        borderwidth=2,
        width=22,
        justify='center'
    )
    tildes_entry.pack(side='left', padx=(0, 15), ipady=4)
    tildes_entry.bind('<KeyRelease>', settings_instance._on_pattern_changed)
    
    # Aperçu Tildes
    settings_instance.tildes_preview = tk.Text(
        tildes_container,
        height=1,
        font=('Consolas', 11),
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        relief='solid',
        borderwidth=1,
        state='disabled',
        wrap='word'
    )
    settings_instance.tildes_preview.tag_configure("center", justify='center')
    settings_instance.tildes_preview.pack(side='left', fill='x', expand=True)
    
    # Boutons d'action pour patterns
    buttons_frame = tk.Frame(main_container, bg=theme["bg"])
    buttons_frame.pack(fill='x', pady=(10, 0))

    # Bouton Reset
    reset_btn = tk.Button(
        buttons_frame,
        text="🔄 Défaut",
        command=settings_instance._reset_simple_patterns,
        bg=theme["button_tertiary_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        width=12
    )
    reset_btn.pack(side='left')

    # Bouton Test
    test_btn = tk.Button(
        buttons_frame,
        text="🧪 Tester",
        command=settings_instance._test_simple_patterns,
        bg=theme["button_utility_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        width=12
    )
    test_btn.pack(side='left', padx=(10, 0))
    
    # Initialiser les aperçus
    settings_instance._update_pattern_previews()
