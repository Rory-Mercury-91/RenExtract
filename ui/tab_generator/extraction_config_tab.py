# ui/tab_generator/extraction_config_tab.py
# Onglet de configuration extraction textes oubliés - Générateur de Traductions Ren'Py
# VERSION AVEC COMBOBOX pour sélection langue unique

"""
Onglet de configuration pour l'extraction des textes oubliés par le SDK
- Sélection du mode de détection (Simple/Optimisé)
- Configuration des exclusions de fichiers
- Sélection de la langue de référence via COMBOBOX
- Validation et lancement de l'analyse
"""

import tkinter as tk
from tkinter import ttk
import os
import glob
from ui.themes import theme_manager
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import show_translated_messagebox

def create_extraction_config_tab(parent_notebook, main_interface):
    """Crée l'onglet de configuration d'extraction des textes oubliés"""
    theme = theme_manager.get_theme()
    
    # Frame avec thème
    tab_frame = tk.Frame(parent_notebook, bg=theme["bg"])
    parent_notebook.add(tab_frame, text="📁 Extraction - Config")
    
    # Container principal avec espacement optimisé
    main_container = tk.Frame(tab_frame, bg=theme["bg"])
    main_container.pack(fill='both', expand=True, padx=20, pady=15)
    
    # Description simplifiée
    desc_label = tk.Label(
        main_container,
        text="Configuration pour l'extraction des textes oubliés par le SDK Ren'Py",
        font=('Segoe UI', 10, 'bold'),
        justify='left',
        bg=theme["bg"],
        fg=theme["accent"]
    )
    desc_label.pack(anchor='w', pady=(0, 20))
    
    # ===== SECTION SÉLECTION DE LA LANGUE =====
    language_frame = tk.Frame(main_container, bg=theme["bg"])
    language_frame.pack(fill='x', pady=(0, 20))
    
    # Titre de la section langue
    language_title = tk.Label(
        language_frame,
        text="🌍 Langue de référence à analyser",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    language_title.pack(anchor='w', pady=(0, 10))
    
    _create_language_selection_section(language_frame, main_interface)
    
    # ===== SECTION EXCLUSIONS =====
    exclusions_frame = tk.Frame(main_container, bg=theme["bg"])
    exclusions_frame.pack(fill='x', pady=(0, 10))
    
    # Titre de la section exclusions
    exclusions_title = tk.Label(
        exclusions_frame,
        text="🚫 Fichiers à exclure",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    exclusions_title.pack(anchor='w', pady=(0, 10))
    
    _create_exclusions_section(exclusions_frame, main_interface)
    
    # ===== SECTION PATTERNS PERSONNALISÉS =====
    custom_patterns_frame = tk.Frame(main_container, bg=theme["bg"])
    custom_patterns_frame.pack(fill='x', pady=(0, 10))
    
    # Titre de la section patterns
    patterns_title = tk.Label(
        custom_patterns_frame,
        text="🔧 Patterns Regex Personnalisés",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    patterns_title.pack(anchor='w', pady=(0, 10))
    
    _create_custom_patterns_section(custom_patterns_frame, main_interface)
    
    # ===== SECTION ACTION =====
    action_frame = tk.Frame(main_container, bg=theme["bg"])
    action_frame.pack(fill='x', pady=(10, 0))
    
    # Titre de la section action
    action_title = tk.Label(
        action_frame,
        text="🚀 Lancement de l'analyse",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    action_title.pack(anchor='w', pady=(0, 10))
    
    _create_action_section(action_frame, main_interface)
    # --- PLACEZ ICI, AVANT LA FERMETURE DE LA FONCTION ---
    def _auto_scan_config_if_ready(*_):
        if (getattr(main_interface, "current_project_path", "") and 
            hasattr(main_interface, 'extraction_lang_combo') and
            not main_interface.extraction_selected_language_var.get()):
            scan_extraction_languages(main_interface)

    _auto_scan_config_if_ready()

    def _on_tab_changed_config(event=None):
        try:
            current = parent_notebook.nametowidget(parent_notebook.select())
            if current is tab_frame:
                _auto_scan_config_if_ready()
        except Exception:
            pass

    parent_notebook.bind("<<NotebookTabChanged>>", _on_tab_changed_config)
    main_interface.extraction_config_resync = _auto_scan_config_if_ready
    # FIN DE LA FONCTION create_extraction_config_tab

def _create_language_selection_section(parent, main_interface):
    """Crée la section de sélection des langues avec COMBOBOX"""
    theme = theme_manager.get_theme()
    
    # Frame pour la combobox et le bouton scanner
    lang_line = tk.Frame(parent, bg=theme["bg"])
    lang_line.pack(fill='x', pady=(0, 10))
    
    lang_label = tk.Label(lang_line, text="Langue :", font=('Segoe UI', 9),
                         bg=theme["bg"], fg=theme["fg"], width=15, anchor='e')
    lang_label.pack(side='left', padx=(0, 10))
    
    # Variable pour stocker la langue sélectionnée
    if not hasattr(main_interface, 'extraction_selected_language_var'):
        main_interface.extraction_selected_language_var = tk.StringVar()
    
    # Combobox pour la langue (sera peuplée dynamiquement)
    main_interface.extraction_lang_combo = ttk.Combobox(
        lang_line, 
        textvariable=main_interface.extraction_selected_language_var,
        width=25, 
        state='readonly'
    )
    main_interface.extraction_lang_combo.pack(side='left', padx=(0, 10))
    main_interface.extraction_lang_combo.bind('<<ComboboxSelected>>', lambda event: _on_language_selected(main_interface))
    
    # Bouton Scanner langues
    scan_btn = tk.Button(lang_line, text="Scanner les langues", 
                        command=lambda: scan_extraction_languages(main_interface),
                        bg=theme["button_utility_bg"],
                        fg="#000000",
                        font=('Segoe UI', 9), 
                        pady=4, 
                        padx=8,
                        relief='flat',
                        cursor='hand2')
    scan_btn.pack(side='left')
    
    # Label d'état de détection
    main_interface.extraction_lang_status_label = tk.Label(
        parent,
        text="📊 Projet non configuré - Cliquez sur 'Scanner les langues'",
        font=('Segoe UI', 9, 'italic'),
        bg=theme["bg"],
        fg='#666666'
    )
    main_interface.extraction_lang_status_label.pack(anchor='w', pady=(5, 0))

def _create_exclusions_section(parent, main_interface):
    """Crée la section des exclusions"""
    theme = theme_manager.get_theme()
    
    exclusions_label = tk.Label(
        parent,
        text="📋 Fichiers à ignorer lors de l'analyse (séparés par des virgules) :",
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    exclusions_label.pack(anchor='w', pady=(0, 10))
    
    # Frame pour input + boutons
    exclusions_input_frame = tk.Frame(parent, bg=theme["bg"])
    exclusions_input_frame.pack(fill='x', pady=(0, 10))
    
    exclusions_entry = tk.Entry(
        exclusions_input_frame,
        textvariable=main_interface.extraction_excluded_files_var,
        font=('Segoe UI', 10),
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        insertbackground=theme["entry_fg"],
        relief='solid',
        borderwidth=1
    )
    exclusions_entry.pack(side='left', fill='x', expand=True, pady=2)
    
    # Bouton aide
    exclusions_help_btn = tk.Button(
        exclusions_input_frame,
        text="❓",
        command=lambda: _show_exclusions_help(main_interface),
        bg=theme["button_help_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    exclusions_help_btn.pack(side='right', padx=(10, 0))

    exclusions_reset_btn = tk.Button(
        exclusions_input_frame,
        text="Par défaut",
        command=lambda: _reset_exclusions(main_interface),
        bg=theme["button_tertiary_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    exclusions_reset_btn.pack(side='right', padx=(5, 0))

def _create_action_section(parent, main_interface):
    """Crée la section d'action"""
    theme = theme_manager.get_theme()
    
    # DISPOSITION : STATUT À GAUCHE, BOUTON À DROITE
    action_container = tk.Frame(parent, bg=theme["bg"])
    action_container.pack(fill='x', pady=(0, 10))
    
    # Frame gauche pour le statut
    status_frame = tk.Frame(action_container, bg=theme["bg"])
    status_frame.pack(side='left', fill='x', expand=True, pady=2)
    
    main_interface.extraction_status_label = tk.Label(
        status_frame,
        text="📊 État: Prêt - Sélectionnez une langue pour commencer",
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        anchor='w'
    )
    main_interface.extraction_status_label.pack(anchor='w', fill='x')

    main_interface.extraction_analyze_btn = tk.Button(
        action_container,
        text="🚀 Démarrer l'analyse",
        command=lambda: start_extraction_analysis(main_interface),
        bg=theme["button_primary_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    main_interface.extraction_analyze_btn.pack(side='right', padx=(10, 0))

    main_interface.operation_buttons.append(main_interface.extraction_analyze_btn)

def scan_extraction_languages(main_interface):
    """Scanne les langues disponibles dans le projet actuel pour l'extraction"""
    try:
        if not main_interface.current_project_path:
            main_interface._show_notification('Veuillez sélectionner un projet Ren\'Py', "warning")
            return
       
        tl_path = os.path.join(main_interface.current_project_path, "game", "tl")
        if not os.path.exists(tl_path):
            main_interface._update_status("⚠️ Aucun dossier tl/ trouvé dans le projet")
            main_interface.extraction_lang_status_label.config(
                text="❌ Aucun dossier tl/ trouvé dans le projet", fg='#ff8379'
            )
            return
       
        # Utiliser la même logique que l'onglet 1
        languages = []
        for item in os.listdir(tl_path):
            item_path = os.path.join(tl_path, item)
            if os.path.isdir(item_path) and not item.startswith('.') and item.lower() != 'none':
                # Vérifier qu'il y a des fichiers .rpy dedans
                rpy_files = list(glob.glob(os.path.join(item_path, "**/*.rpy"), recursive=True))
                if rpy_files:
                    languages.append({
                        'name': item,
                        'file_count': len(rpy_files)
                    })
       
        if not languages:
            main_interface._update_status("⚠️ Aucune langue avec fichiers .rpy trouvée")
            main_interface.extraction_lang_status_label.config(
                text="ℹ️ Aucune langue avec fichiers .rpy trouvée", fg='#666666'
            )
            return
       
        # Trier avec french en premier
        languages.sort(key=lambda x: (0 if x['name'].lower() == 'french' else 1, x['name'].lower()))
       
        # Peupler la combobox
        lang_names = [lang['name'] for lang in languages]
        main_interface.extraction_lang_combo['values'] = lang_names
       
        # Sélectionner french par défaut ou le premier
        default_lang = 'french' if 'french' in lang_names else lang_names[0]
        main_interface.extraction_selected_language_var.set(default_lang)
       
        # Mettre à jour le statut
        total_files = sum(lang['file_count'] for lang in languages)
        main_interface.extraction_lang_status_label.config(
            text=f"✅ {len(languages)} langue(s) trouvée(s) - {total_files} fichiers .rpy au total",
            fg=theme_manager.get_theme()["fg"]
        )
       
        # Déclencher la mise à jour du statut principal
        _on_language_selected(main_interface)
       
        main_interface._update_status(f'{len(languages)} langues trouvées: {", ".join(lang_names)}', "success")
        log_message("INFO", f"Langues d'extraction scannées: {lang_names}", category="extraction_config")
       
    except Exception as e:
        log_message("ERREUR", f"Erreur scan langues extraction: {e}", category="extraction_config")
        main_interface._show_notification(f"Erreur scan langues: {e}", "error")
        main_interface.extraction_lang_status_label.config(
            text="❌ Erreur lors du scan des langues", fg='#ff8379'
        )

def _on_language_selected(main_interface):
    """Callback quand une langue est sélectionnée dans la combobox"""
    try:
        selected_language = main_interface.extraction_selected_language_var.get()
        if selected_language:
            main_interface.extraction_status_label.config(
                text=f"📊 État: Langue sélectionnée: {selected_language} - Prêt pour l'analyse"
            )
            log_message("DEBUG", f"Langue d'extraction sélectionnée: {selected_language}", category="extraction_config")
        else:
            main_interface.extraction_status_label.config(
                text="📊 État: Prêt - Sélectionnez une langue pour commencer"
            )
    except Exception as e:
        log_message("ERREUR", f"Erreur sélection langue extraction: {e}", category="extraction_config")

def detect_extraction_languages(main_interface):
    """Détecte automatiquement les langues quand le projet change"""
    try:
        # Auto-scanner les langues quand un projet est sélectionné
        scan_extraction_languages(main_interface)
    except Exception as e:
        log_message("ERREUR", f"Erreur détection automatique langues extraction: {e}", category="extraction_config")

def get_selected_extraction_language(main_interface):
    """Retourne la langue actuellement sélectionnée pour l'extraction"""
    return main_interface.extraction_selected_language_var.get()

def get_selected_extraction_language_path(main_interface):
    """Retourne le chemin complet vers le dossier tl de la langue sélectionnée"""
    selected_lang = get_selected_extraction_language(main_interface)
    if not selected_lang or not main_interface.current_project_path:
        return None
    
    return os.path.join(main_interface.current_project_path, "game", "tl", selected_lang)

def start_extraction_analysis(main_interface):
    """Lance l'analyse d'extraction des textes oubliés"""
    try:
        # Validation minimale des prérequis
        if not main_interface.current_project_path:
            main_interface.extraction_status_label.config(text="📊 État: ❌ Veuillez sélectionner un projet Ren'Py")
            main_interface._show_notification("Veuillez sélectionner un projet Ren'Py avant de lancer l'analyse.", "warning")
            return
        
        selected_language = get_selected_extraction_language(main_interface)
        if not selected_language:
            main_interface.extraction_status_label.config(text="📊 État: ❌ Veuillez sélectionner une langue")
            main_interface._show_notification("Veuillez sélectionner une langue de référence à analyser.", "warning")
            return

        # IMPORTS NÉCESSAIRES
        from core.services.translation.text_extraction_results_business import TextExtractionResultsBusiness
        from core.services.translation.text_extraction_config_business import TextExtractionConfigBusiness, prepare_extraction_config_from_interface
        
        # Initialiser les modules métier
        if not hasattr(main_interface, 'extraction_results_business'):
            main_interface.extraction_results_business = TextExtractionResultsBusiness()
        
        if not hasattr(main_interface, 'extraction_config_business'):
            main_interface.extraction_config_business = TextExtractionConfigBusiness()
        
        # Préparer et valider la configuration via le module métier
        config = prepare_extraction_config_from_interface(main_interface)
        validation_result = main_interface.extraction_config_business.validate_extraction_config(config)
        
        if not validation_result['valid']:
            error_msg = "; ".join(validation_result['errors'])
            main_interface.extraction_status_label.config(text="📊 État: ❌ Configuration invalide")
            main_interface._show_notification(f"Configuration invalide:\n{error_msg}", "error")
            return
        
        # Préparer les paramètres d'extraction
        extraction_params = main_interface.extraction_config_business.prepare_extraction_parameters(config)
        
        # Désactiver le bouton et mettre à jour l'état
        main_interface.extraction_analyze_btn.config(state='disabled', text="⏳ Analyse en cours...")
        main_interface.extraction_status_label.config(text=f"📊 État: 🔍 Analyse en cours ({selected_language})...")
        main_interface._set_operation_running(True)
        
        # Lancer l'analyse avec callbacks
        main_interface.extraction_results_business.run_extraction_analysis(
            extraction_params,
            progress_callback=main_interface._on_progress_update,
            status_callback=lambda msg: main_interface.extraction_status_label.config(text=f"📊 État: {msg}"),
            completion_callback=lambda success, results: _handle_extraction_completion(main_interface, success, results)
        )
        
    except Exception as e:
        log_message("ERREUR", f"Erreur lors du démarrage de l'analyse d'extraction: {e}", category="extraction_config")
        main_interface.extraction_status_label.config(text="📊 État: ❌ Erreur lors du démarrage")
        main_interface._set_operation_running(False)

def _handle_extraction_completion(main_interface, success, results):
    """Gère la fin de l'analyse d'extraction"""
    try:
        if success:
            # Stocker les résultats
            main_interface.extraction_analysis_results = results
            
            # Basculer vers l'onglet résultats
            main_interface.notebook.tab(3, state='normal')
            main_interface.notebook.select(3)
            
            # Déclencher l'affichage des résultats
            from ui.tab_generator.extraction_results_tab import display_extraction_results
            display_extraction_results(main_interface)
            
            # Calculer le total pour le statut
            stats = results.get('statistics', {})
            total_detected = stats.get('total_detected', 0)
            
            main_interface.extraction_status_label.config(
                text=f"📊 État: ✅ Analyse terminée - {total_detected} nouveaux textes détectés"
            )
        else:
            error_msg = results.get('error', 'Erreur inconnue')
            main_interface.extraction_status_label.config(text=f"📊 État: ❌ Erreur: {error_msg}")
            main_interface._show_notification(f"Une erreur est survenue pendant l'analyse:\n\n{error_msg}", "error")
        
        # Remettre le bouton en état normal
        main_interface.extraction_analyze_btn.config(state='normal', text="🚀 Lancer l'analyse")
        main_interface._set_operation_running(False)
        
    except Exception as e:
        log_message("ERREUR", f"Erreur gestion fin analyse: {e}", category="extraction_config")

def _show_exclusions_help(main_interface):
    """Affiche l'aide stylisée pour les exclusions avec mention des exclusions système."""
    
    message_styled = [
        ("Exclusion de fichiers de l'extraction\n\n", "bold_red"),
        ("Cette option permet d'ignorer certains fichiers lors de l'analyse pour trouver les textes oubliés.\n\n", "normal"),

        ("📁 Format :\n", "bold_green"),
        ("• Séparez les noms de fichiers par des ", "normal"), ("virgules", "bold"), (" (,).\n", "normal"),
        ("• Utilisez uniquement le nom du fichier (ex: ", "normal"), ("screens.rpy", "italic"), (").\n\n", "normal"),

        ("✅ Exemples valides :\n", "bold_green"),
        ("• ", "green"), ("common.rpy, screens.rpy\n", "yellow"),
        ("• ", "green"), ("backup.rpy, old_file.rpy\n\n", "yellow"),

        ("💡 Cas d'usage :\n", "bold_yellow"),
        ("• Fichiers de sauvegarde ou temporaires.\n", "normal"),
        ("• Modèles ou fichiers de test que vous ne souhaitez pas traduire.\n", "normal"),
        ("• Fichiers système importants que vous ne voulez pas modifier.\n\n", "normal"),
        
        ("🔧 ", "blue"), ("Exclusions automatiques :", "bold"), ("\n", "normal"),
        ("Le système exclut automatiquement ses propres fichiers générés :\n", "normal"),
        ("• ", "blue"), ("99_Z_LangSelect.rpy", "italic"), (" (sélecteur de langue)\n", "normal"),
        ("• ", "blue"), ("99_Z_Console.rpy", "italic"), (" (console développeur)\n", "normal"),
        ("Ces fichiers n'apparaîtront jamais dans les résultats d'extraction.\n\n", "normal"),

        ("⚠️ ", "red"), ("Note :", "bold"), (" Les fichiers listés ci-dessus seront totalement ignorés par l'outil d'extraction des textes oubliés.", "normal"),
    ]

    try:
        from ui.themes import theme_manager
        from infrastructure.helpers.unified_functions import show_custom_messagebox
        
        show_custom_messagebox(
            'info',
            '🚫 Aide - Exclusion de fichiers',
            message_styled,
            theme_manager.get_theme(),
            parent=main_interface.window
        )
    except Exception as e:
        log_message("ERREUR", f"Erreur affichage aide exclusions : {e}", category="renpy_generator_extraction")

def _reset_exclusions(main_interface):
    """Remet les exclusions par défaut"""
    try:
        default_exclusions = "common.rpy, screens.rpy"
        main_interface.extraction_excluded_files_var.set(default_exclusions)
        log_message("INFO", "Exclusions extraction remises par défaut", category="extraction_config")
    except Exception as e:
        log_message("ERREUR", f"Erreur reset exclusions extraction: {e}", category="extraction_config")

def _create_custom_patterns_section(parent, main_interface):
    """Crée la section pour les patterns regex personnalisés"""
    theme = theme_manager.get_theme()
    
    # Frame pour la liste des patterns
    patterns_list_frame = tk.Frame(parent, bg=theme["bg"])
    patterns_list_frame.pack(fill='both', expand=True, pady=(0, 10))
    
    # Liste des patterns avec scrollbar
    list_frame = tk.Frame(patterns_list_frame, bg=theme["bg"])
    list_frame.pack(side='left', fill='both', expand=True)
    
    # Treeview pour afficher les patterns
    columns = ('name', 'pattern', 'flags', 'enabled')
    main_interface.custom_patterns_tree = ttk.Treeview(
        list_frame,
        columns=columns,
        show='headings',
        height=4
    )
    
    # Configuration des colonnes
    main_interface.custom_patterns_tree.heading('name', text='Nom')
    main_interface.custom_patterns_tree.heading('pattern', text='Pattern Regex')
    main_interface.custom_patterns_tree.heading('flags', text='Flags')
    main_interface.custom_patterns_tree.heading('enabled', text='Activé')
    
    main_interface.custom_patterns_tree.column('name', width=120)
    main_interface.custom_patterns_tree.column('pattern', width=200)
    main_interface.custom_patterns_tree.column('flags', width=60)
    main_interface.custom_patterns_tree.column('enabled', width=60)
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=main_interface.custom_patterns_tree.yview)
    main_interface.custom_patterns_tree.configure(yscrollcommand=scrollbar.set)
    
    main_interface.custom_patterns_tree.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    
    # Frame pour les boutons
    buttons_frame = tk.Frame(parent, bg=theme["bg"])
    buttons_frame.pack(fill='x', pady=(0, 10))
    
    # Boutons d'action
    add_btn = tk.Button(
        buttons_frame,
        text="➕ Ajouter",
        command=lambda: _add_custom_pattern(main_interface),
        bg=theme["button_primary_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    add_btn.pack(side='left', padx=(0, 5))
    
    edit_btn = tk.Button(
        buttons_frame,
        text="✏️ Modifier",
        command=lambda: _edit_custom_pattern(main_interface),
        bg=theme["button_secondary_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    edit_btn.pack(side='left', padx=(0, 5))
    
    toggle_btn = tk.Button(
        buttons_frame,
        text="🔄 Activer/Désactiver",
        command=lambda: _toggle_custom_pattern(main_interface),
        bg=theme["button_tertiary_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    toggle_btn.pack(side='left', padx=(0, 5))
    
    delete_btn = tk.Button(
        buttons_frame,
        text="🗑️ Supprimer",
        command=lambda: _delete_custom_pattern(main_interface),
        bg=theme["button_danger_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    delete_btn.pack(side='left', padx=(0, 5))
    
    help_btn = tk.Button(
        buttons_frame,
        text="❓",
        command=lambda: _show_custom_patterns_help(main_interface),
        bg=theme["button_help_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    help_btn.pack(side='right')
    
    # Charger les patterns existants
    _load_custom_patterns(main_interface)

def _load_custom_patterns(main_interface):
    """Charge les patterns personnalisés dans la liste"""
    try:
        # Vider la liste
        for item in main_interface.custom_patterns_tree.get_children():
            main_interface.custom_patterns_tree.delete(item)
        
        # Charger depuis la configuration
        patterns = config_manager.get_custom_extraction_patterns()
        for i, pattern in enumerate(patterns):
            enabled_text = "✅" if pattern.get('enabled', False) else "❌"
            main_interface.custom_patterns_tree.insert('', 'end', values=(
                pattern.get('name', 'Sans nom'),
                pattern.get('pattern', ''),
                pattern.get('flags', ''),
                enabled_text
            ), tags=(str(i),))
        
        # Forcer la mise à jour de l'affichage
        main_interface.custom_patterns_tree.update_idletasks()
        
    except Exception as e:
        log_message("ERREUR", f"Erreur chargement patterns personnalisés: {e}", category="extraction_config")

def _add_custom_pattern(main_interface):
    """Ajoute un nouveau pattern personnalisé"""
    _show_pattern_dialog(main_interface, None)

def _edit_custom_pattern(main_interface):
    """Modifie un pattern personnalisé existant"""
    selection = main_interface.custom_patterns_tree.selection()
    if not selection:
        main_interface._update_status("⚠️ Veuillez sélectionner un pattern à modifier")
        return
    
    item = main_interface.custom_patterns_tree.item(selection[0])
    pattern_index = int(item['tags'][0])
    _show_pattern_dialog(main_interface, pattern_index)

def _test_custom_pattern(main_interface):
    """Teste un pattern personnalisé"""
    selection = main_interface.custom_patterns_tree.selection()
    if not selection:
        main_interface._update_status("⚠️ Veuillez sélectionner un pattern à tester")
        return
    
    item = main_interface.custom_patterns_tree.item(selection[0])
    pattern_index = int(item['tags'][0])
    
    # Ouvrir directement le dialogue unifié en mode modification
    _show_pattern_dialog(main_interface, pattern_index)

def _toggle_custom_pattern(main_interface):
    """Active/désactive un pattern personnalisé"""
    selection = main_interface.custom_patterns_tree.selection()
    if not selection:
        main_interface._update_status("⚠️ Veuillez sélectionner un pattern")
        return
    
    item = main_interface.custom_patterns_tree.item(selection[0])
    pattern_index = int(item['tags'][0])
    
    new_state = config_manager.toggle_custom_extraction_pattern(pattern_index)
    _load_custom_patterns(main_interface)
    
    status = "activé" if new_state else "désactivé"
    main_interface._update_status(f"✅ Pattern {status} avec succès")

def _delete_custom_pattern(main_interface):
    """Supprime un pattern personnalisé"""
    selection = main_interface.custom_patterns_tree.selection()
    if not selection:
        main_interface._update_status("⚠️ Veuillez sélectionner un pattern à supprimer")
        return
    
    item = main_interface.custom_patterns_tree.item(selection[0])
    pattern_name = item['values'][0]
    pattern_index = int(item['tags'][0])
    
    # Confirmation avec Oui/Non (type 'askyesno')
    from infrastructure.helpers.unified_functions import show_translated_messagebox
    result = show_translated_messagebox(
        'askyesno',
        '❓ Confirmation de suppression',
        f'Voulez-vous vraiment supprimer le pattern "{pattern_name}" ?\n\nCette action est irréversible.',
        parent=main_interface.window
    )
    
    if result:  # Si l'utilisateur clique sur "Oui"
        if config_manager.remove_custom_extraction_pattern(pattern_index):
            _load_custom_patterns(main_interface)
            main_interface._update_status(f"✅ Pattern '{pattern_name}' supprimé avec succès")
        else:
            main_interface._update_status("❌ Erreur lors de la suppression du pattern")
    else:  # Si l'utilisateur clique sur "Non" ou ferme
        main_interface._update_status(f"ℹ️ Suppression du pattern '{pattern_name}' annulée")

def _show_pattern_dialog(main_interface, pattern_index=None):
    """Affiche la boîte de dialogue unifiée pour ajouter/modifier/tester un pattern"""
    theme = theme_manager.get_theme()
    
    # Créer la fenêtre plus grande pour tout inclure
    dialog = tk.Toplevel(main_interface.window)
    dialog.title("Pattern Regex Personnalisé" if pattern_index is None else "Modifier Pattern")
    dialog.geometry("1100x750")
    dialog.configure(bg=theme["bg"])
    dialog.transient(main_interface.window)
    dialog.grab_set()
    
    # Centrer la fenêtre
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (1100 // 2)
    y = (dialog.winfo_screenheight() // 2) - (700 // 2)
    dialog.geometry(f"1100x750+{x}+{y}")
    
    # Variables
    name_var = tk.StringVar()
    pattern_var = tk.StringVar()
    flags_var = tk.StringVar()
    description_var = tk.StringVar()
    enabled_var = tk.BooleanVar()
    
    # Charger les données si modification
    saved_test_text = '$ sms.msg("[V]", "[mc.name]... That was incredibly dangerous.", False)'
    if pattern_index is not None:
        patterns = config_manager.get_custom_extraction_patterns()
        if 0 <= pattern_index < len(patterns):
            pattern = patterns[pattern_index]
            name_var.set(pattern.get('name', ''))
            pattern_var.set(pattern.get('pattern', ''))
            flags_var.set(pattern.get('flags', ''))
            description_var.set(pattern.get('description', ''))
            enabled_var.set(pattern.get('enabled', False))
            saved_test_text = pattern.get('test_text', saved_test_text)
    
    # Interface principale avec Canvas et Scrollbar
    main_canvas = tk.Canvas(dialog, bg=theme["bg"], highlightthickness=0)
    scrollbar = tk.Scrollbar(dialog, orient="vertical", command=main_canvas.yview)
    main_frame = tk.Frame(main_canvas, bg=theme["bg"])
    
    main_frame.bind(
        "<Configure>",
        lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
    )
    
    canvas_window = main_canvas.create_window((0, 0), window=main_frame, anchor="nw")
    main_canvas.configure(yscrollcommand=scrollbar.set)
    
    # Faire en sorte que le main_frame prenne toute la largeur du canvas
    def on_canvas_configure(event):
        main_canvas.itemconfig(canvas_window, width=event.width)
    main_canvas.bind('<Configure>', on_canvas_configure)
    
    main_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=15)
    scrollbar.pack(side="right", fill="y")
    
    # ===== SECTION 1: CONFIGURATION DU PATTERN =====
    config_section = tk.LabelFrame(
        main_frame,
        text="⚙️ Configuration du Pattern",
        font=('Segoe UI', 10, 'bold'),
        bg=theme["frame_bg"],
        fg=theme["fg"],
        padx=15,
        pady=10
    )
    config_section.pack(fill='x', pady=(0, 15))
    
    # Nom
    tk.Label(config_section, text="Nom:", bg=theme["frame_bg"], fg=theme["fg"], 
             font=('Segoe UI', 9, 'bold')).pack(anchor='w')
    name_entry = tk.Entry(config_section, textvariable=name_var, font=('Segoe UI', 10), 
                          bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["entry_fg"])
    name_entry.pack(fill='x', pady=(2, 10))
    
    # Pattern
    tk.Label(config_section, text="Pattern Regex:", bg=theme["frame_bg"], fg=theme["fg"], 
             font=('Segoe UI', 9, 'bold')).pack(anchor='w')
    pattern_entry = tk.Entry(config_section, textvariable=pattern_var, font=('Consolas', 10),
                            bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["entry_fg"])
    pattern_entry.pack(fill='x', pady=(2, 10))
    
    # Flags avec exemples
    flags_frame = tk.Frame(config_section, bg=theme["frame_bg"])
    flags_frame.pack(fill='x', pady=(0, 10))
    
    tk.Label(flags_frame, text="Flags:", bg=theme["frame_bg"], fg=theme["fg"], 
             font=('Segoe UI', 9, 'bold')).pack(side='left')
    flags_entry = tk.Entry(flags_frame, textvariable=flags_var, font=('Segoe UI', 10), width=10,
                          bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["entry_fg"])
    flags_entry.pack(side='left', padx=(5, 10))
    tk.Label(flags_frame, text="i=insensible  m=multiligne  s=dotall  g=global", 
             bg=theme["frame_bg"], fg='#888888', font=('Segoe UI', 8, 'italic')).pack(side='left')
    
    # Description
    tk.Label(config_section, text="Description:", bg=theme["frame_bg"], fg=theme["fg"], 
             font=('Segoe UI', 9, 'bold')).pack(anchor='w')
    description_text = tk.Text(config_section, height=3, font=('Segoe UI', 9), 
                              bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["entry_fg"])
    description_text.pack(fill='x', pady=(2, 10))
    description_text.insert('1.0', description_var.get())
    
    # Bouton d'activation avec émote (au lieu de checkbox)
    def toggle_enabled():
        """Toggle l'état activé/désactivé et met à jour l'interface principale"""
        current = enabled_var.get()
        enabled_var.set(not current)
        update_enabled_button()
        
        # Si on modifie un pattern existant, sauvegarder l'état et mettre à jour l'interface
        if pattern_index is not None:
            new_state = not current
            config_manager.update_custom_extraction_pattern(
                pattern_index, 
                enabled=new_state
            )
            # Mettre à jour l'affichage dans l'interface principale
            _load_custom_patterns(main_interface)
            log_message("INFO", f"Pattern {'activé' if new_state else 'désactivé'}", category="extraction_config")
    
    def update_enabled_button():
        """Met à jour l'apparence du bouton selon l'état"""
        if enabled_var.get():
            enabled_toggle_btn.config(
                text="✅ Pattern activé pour l'extraction",
                bg="#90EE90",  # Vert clair
                fg="#006400"   # Vert foncé
            )
        else:
            enabled_toggle_btn.config(
                text="❌ Pattern désactivé",
                bg="#FFB6C1",  # Rouge clair
                fg="#8B0000"   # Rouge foncé
            )
    
    enabled_toggle_btn = tk.Button(
        config_section,
        command=toggle_enabled,
        font=('Segoe UI', 9, 'bold'),
        relief='raised',
        borderwidth=2,
        pady=5,
        cursor='hand2'
    )
    enabled_toggle_btn.pack(fill='x', pady=(5, 0))
    
    # Initialiser l'apparence du bouton
    update_enabled_button()
    
    # ===== SECTION 2: ZONE DE TEST =====
    test_section = tk.LabelFrame(
        main_frame,
        text="🧪 Zone de Test en Temps Réel",
        font=('Segoe UI', 10, 'bold'),
        bg=theme["frame_bg"],
        fg=theme["fg"],
        padx=15,
        pady=10
    )
    test_section.pack(fill='both', expand=True, pady=(0, 15))
    
    # Texte de test
    test_label_frame = tk.Frame(test_section, bg=theme["frame_bg"])
    test_label_frame.pack(fill='x', pady=(0, 5))
    
    tk.Label(test_label_frame, text="Texte de test (sera sauvegardé):", 
             bg=theme["frame_bg"], fg=theme["fg"], font=('Segoe UI', 9, 'bold')).pack(side='left')
    
    test_text = tk.Text(test_section, height=8, font=('Consolas', 9), 
                       bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["entry_fg"],
                       wrap='word')
    test_text.pack(fill='both', expand=True, pady=(0, 10))
    test_text.insert('1.0', saved_test_text)
    
    # Scrollbar pour le texte de test
    test_scroll = tk.Scrollbar(test_text)
    test_scroll.pack(side='right', fill='y')
    test_text.config(yscrollcommand=test_scroll.set)
    test_scroll.config(command=test_text.yview)
    
    # Bouton Tester
    test_btn_frame = tk.Frame(test_section, bg=theme["frame_bg"])
    test_btn_frame.pack(fill='x', pady=(0, 10))
    
    test_button = tk.Button(
        test_btn_frame,
        text="🔍 Tester le pattern",
        command=lambda: test_pattern(),
        bg=theme["button_utility_bg"],
        fg="#000000",
        font=('Segoe UI', 10, 'bold'),
        pady=8
    )
    test_button.pack(fill='x')
    
    # ===== SECTION 3: RÉSULTATS =====
    result_section = tk.LabelFrame(
        main_frame,
        text="📊 Résultats du Test",
        font=('Segoe UI', 10, 'bold'),
        bg=theme["frame_bg"],
        fg=theme["fg"],
        padx=15,
        pady=10
    )
    result_section.pack(fill='both', expand=True, pady=(0, 15))
    
    # Label de statut
    result_status_label = tk.Label(
        result_section,
        text="⏳ Cliquez sur 'Tester le pattern' pour voir les résultats",
        bg=theme["frame_bg"],
        fg='#888888',
        font=('Segoe UI', 9, 'italic')
    )
    result_status_label.pack(anchor='w', pady=(0, 5))
    
    # Zone de résultats
    result_text = tk.Text(result_section, height=8, font=('Consolas', 9), 
                         bg='#f0f0f0', fg='#000000', wrap='word', state='disabled')
    result_text.pack(fill='both', expand=True)
    
    # Scrollbar pour les résultats
    result_scroll = tk.Scrollbar(result_text)
    result_scroll.pack(side='right', fill='y')
    result_text.config(yscrollcommand=result_scroll.set)
    result_scroll.config(command=result_text.yview)
    
    # Configuration des tags pour coloration
    result_text.tag_configure('success', foreground='#00aa00', font=('Consolas', 9, 'bold'))
    result_text.tag_configure('error', foreground='#ff0000', font=('Consolas', 9, 'bold'))
    result_text.tag_configure('match', foreground='#0066cc', font=('Consolas', 9))
    
    def test_pattern():
        """Teste le pattern avec le texte fourni"""
        try:
            import re
            pattern_str = pattern_var.get().strip()
            flags_str = flags_var.get().strip()
            test_content = test_text.get('1.0', 'end-1c')
            
            if not pattern_str:
                result_status_label.config(text="⚠️ Veuillez entrer un pattern regex", fg='#ff8800')
                return
            
            # Convertir les flags
            regex_flags = 0
            if 'i' in flags_str:
                regex_flags |= re.IGNORECASE
            if 'm' in flags_str:
                regex_flags |= re.MULTILINE
            if 's' in flags_str:
                regex_flags |= re.DOTALL
            
            # Tester le pattern
            compiled_pattern = re.compile(pattern_str, regex_flags)
            matches = compiled_pattern.findall(test_content)
            
            # Afficher les résultats
            result_text.config(state='normal')
            result_text.delete('1.0', 'end')
            
            if matches:
                result_status_label.config(
                    text=f"✅ {len(matches)} correspondance(s) trouvée(s)",
                    fg='#00aa00'
                )
                result_text.insert('1.0', f"✅ {len(matches)} correspondance(s) trouvée(s):\n\n", 'success')
                for i, match in enumerate(matches, 1):
                    if isinstance(match, tuple):
                        match_str = " | ".join(str(m) for m in match)
                    else:
                        match_str = str(match)
                    result_text.insert('end', f"{i}. ", 'success')
                    result_text.insert('end', f"{match_str}\n", 'match')
            else:
                result_status_label.config(text="ℹ️ Aucune correspondance trouvée", fg='#ff8800')
                result_text.insert('1.0', "ℹ️ Aucune correspondance trouvée.\n\n", 'error')
                result_text.insert('end', "Vérifiez que:\n")
                result_text.insert('end', "• Le pattern est correct\n")
                result_text.insert('end', "• Le texte de test contient des éléments correspondants\n")
                result_text.insert('end', "• Les flags sont appropriés\n")
            
            result_text.config(state='disabled')
                
        except re.error as e:
            result_status_label.config(text="❌ Erreur regex", fg='#ff0000')
            result_text.config(state='normal')
            result_text.delete('1.0', 'end')
            result_text.insert('1.0', f"❌ Erreur regex:\n\n{e}\n\n", 'error')
            result_text.insert('end', "Vérifiez la syntaxe de votre expression régulière.")
            result_text.config(state='disabled')
        except Exception as e:
            result_status_label.config(text="❌ Erreur", fg='#ff0000')
            result_text.config(state='normal')
            result_text.delete('1.0', 'end')
            result_text.insert('1.0', f"❌ Erreur:\n\n{e}", 'error')
            result_text.config(state='disabled')
    
    # ===== SECTION 4: BOUTONS D'ACTION =====
    buttons_frame = tk.Frame(main_frame, bg=theme["bg"])
    buttons_frame.pack(fill='x', pady=(0, 10))
    
    def save_pattern():
        name = name_var.get().strip()
        pattern = pattern_var.get().strip()
        flags = flags_var.get().strip()
        description = description_text.get('1.0', 'end-1c').strip()
        enabled = enabled_var.get()
        test_content = test_text.get('1.0', 'end-1c')
        
        if not name or not pattern:
            main_interface._update_status("⚠️ Le nom et le pattern sont obligatoires")
            return
        
        # Valider le pattern
        is_valid, error = config_manager.validate_custom_extraction_pattern(pattern, flags)
        if not is_valid:
            main_interface._update_status(f"❌ Pattern invalide: {error}")
            return
        
        # Sauvegarder (avec le texte de test)
        if pattern_index is None:
            # Ajouter
            config_manager.add_custom_extraction_pattern(name, pattern, flags, description, enabled, test_content)
            main_interface._update_status(f"✅ Pattern '{name}' ajouté avec succès")
        else:
            # Modifier
            config_manager.update_custom_extraction_pattern(
                pattern_index, name, pattern, flags, description, enabled, test_content
            )
            main_interface._update_status(f"✅ Pattern '{name}' modifié avec succès")
        
        _load_custom_patterns(main_interface)
        dialog.destroy()
    
    tk.Button(
        buttons_frame,
        text="💾 Sauvegarder",
        command=save_pattern,
        bg=theme["button_primary_bg"],
        fg="#000000",
        font=('Segoe UI', 10, 'bold'),
        pady=8,
        padx=20
    ).pack(side='right', padx=(5, 0))
    
    tk.Button(
        buttons_frame,
        text="❌ Annuler",
        command=dialog.destroy,
        bg=theme["button_tertiary_bg"],
        fg="#000000",
        font=('Segoe UI', 10),
        pady=8,
        padx=20
    ).pack(side='right')
    
    # Bind pour tester avec Ctrl+Enter
    def test_on_ctrl_enter(event):
        test_pattern()
        return "break"
    
    pattern_entry.bind('<Control-Return>', test_on_ctrl_enter)
    test_text.bind('<Control-Return>', test_on_ctrl_enter)
    
    # Test automatique au chargement si pattern existe
    if pattern_var.get():
        dialog.after(200, test_pattern)

def _show_custom_patterns_help(main_interface):
    """Affiche l'aide pour les patterns personnalisés"""
    message_styled = [
        ("Patterns Regex Personnalisés\n\n", "bold_blue"),
        
        ("Cette fonctionnalité vous permet de définir vos propres patterns regex pour détecter des textes spécifiques dans vos fichiers Ren'Py.\n\n", "normal"),
        
        ("✨ ", "blue"), ("Approche recommandée :\n", "bold"),
        ("• ", "green"), ("Une regex = Un ou plusieurs éléments à capturer\n", "bold"),
        ("• Support des groupes multiples : chaque groupe () crée un bloc old/new séparé\n", "normal"),
        ("• Créez des patterns simples et efficaces\n", "normal"),
        ("• Chaque pattern peut être activé/désactivé indépendamment\n\n", "normal"),
        
        ("📝 ", "blue"), ("Format des patterns :\n", "bold"),
        ("• Utilisez la syntaxe regex standard de Python\n", "normal"),
        ("• Les ", "normal"), ("groupes de capture ()", "bold"), (" extraient le texte souhaité\n", "normal"),
        ("• ", "green"), ("NOUVEAU : ", "bold"), ("Chaque groupe () crée un bloc old/new séparé\n", "normal"),
        ("• Exemple : ", "normal"), ("(groupe1).*(groupe2)", "italic"), (" → 2 blocs old/new\n\n", "normal"),
        
        ("🏷️ ", "yellow"), ("Flags disponibles :\n", "bold"),
        ("• ", "normal"), ("i", "bold"), (" = insensible à la casse (ignore majuscules/minuscules)\n", "normal"),
        ("• ", "normal"), ("m", "bold"), (" = mode multiligne (^ et $ fonctionnent sur chaque ligne)\n", "normal"),
        ("• ", "normal"), ("s", "bold"), (" = dotall (le point . correspond aux retours à la ligne)\n", "normal"),
        ("• ", "normal"), ("g", "bold"), (" = global (trouve toutes les occurrences - implicite)\n\n", "normal"),
        
        ("💡 ", "green"), ("Exemples pratiques :\n", "bold"),
        
        ("Cas d'usage : Extraire les titres de quêtes\n", "bold_yellow"),
        ("Pattern : ", "normal"), (r'"QID_[^"]+"\s*:\s*\[\s*"([^"]+)"', "italic"), ("\n", "normal"),
        ("Capture : ", "normal"), ("Find A Way Home", "green"), ("\n\n", "normal"),
        
        ("Cas d'usage : Extraire les descriptions de quêtes\n", "bold_yellow"),
        ("Pattern : ", "normal"), (r'"QID_[^"]+"\s*:\s*\[\s*"[^"]+",\s*"([^"]+)"', "italic"), ("\n", "normal"),
        ("Capture : ", "normal"), ("Make your way to the Jumpgate...", "green"), ("\n\n", "normal"),
        
        ("Cas d'usage : Extraire les indices (hints)\n", "bold_yellow"),
        ("Pattern : ", "normal"), (r'\["hint",\s*"([^"]+)"', "italic"), ("\n", "normal"),
        ("Capture : ", "normal"), ("The Jumpgates might provide a way home...", "green"), ("\n\n", "normal"),
        
        ("Cas d'usage : Messages de notification\n", "bold_yellow"),
        ("Pattern : ", "normal"), (r'\.msg\s*\(\s*"([^"]+)"', "italic"), ("\n", "normal"),
        ("Flags : ", "normal"), ("gm", "yellow"), ("\n\n", "normal"),
        
        ("Cas d'usage : Dialogues personnalisés\n", "bold_yellow"),
        ("Pattern : ", "normal"), (r'\.say\s*\(\s*"([^"]+)"', "italic"), ("\n", "normal"),
        ("Flags : ", "normal"), ("gm", "yellow"), ("\n\n", "normal"),
        
        ("🎯 ", "blue"), ("Nouvelles possibilités avec groupes multiples :\n", "bold"),
        ("Maintenant vous pouvez capturer plusieurs éléments en une seule regex :\n", "normal"),
        ("✅ ", "green"), (r'"QID_[^"]+"\s*:\s*\[\s*"([^"]+)",\s*"([^"]+)".*\["hint",\s*"([^"]+)"', "italic"), ("\n", "normal"),
        ("→ Crée 3 blocs old/new : Titre, Description, Hint\n\n", "normal"),
        
        ("💡 ", "yellow"), ("Ou garder l'approche simple :\n", "bold"),
        ("✅ Pattern 1 : ", "green"), (r'"QID_[^"]+"\s*:\s*\[\s*"([^"]+)"', "italic"), (" → Titre\n", "normal"),
        ("✅ Pattern 2 : ", "green"), (r'"QID_[^"]+"\s*:\s*\[\s*"[^"]+",\s*"([^"]+)"', "italic"), (" → Description\n", "normal"),
        ("✅ Pattern 3 : ", "green"), (r'\["hint",\s*"([^"]+)"', "italic"), (" → Hint\n\n", "normal"),
        
        ("🧪 ", "yellow"), ("Astuce :\n", "bold"),
        ("Utilisez le bouton ", "normal"), ("🔍 Tester le pattern", "bold"), (" pour vérifier vos regex avant de les activer.\n", "normal"),
        ("Collez un extrait de votre code dans la zone de test et ajustez jusqu'à obtenir le bon résultat !\n\n", "normal"),
        
        ("⚠️ ", "red"), ("Important :", "bold"), ("\n", "normal"),
        ("• Les textes extraits sont automatiquement classés en ", "normal"), ("auto_safe", "bold"), ("\n", "normal"),
        ("• Testez toujours vos patterns avant de les activer\n", "normal"),
        ("• Les patterns personnalisés analysent ", "normal"), ("game/", "bold"), (" (hors tl/) et vérifient les doublons\n", "normal"),
        ("• Sauvegardez votre texte de test pour le réutiliser plus tard", "normal")
    ]
    
    try:
        from ui.themes import theme_manager
        from infrastructure.helpers.unified_functions import show_custom_messagebox
        
        show_custom_messagebox(
            'info',
            '❓ Aide - Patterns Regex Personnalisés',
            message_styled,
            theme_manager.get_theme(),
            parent=main_interface.window
        )
    except Exception as e:
        log_message("ERREUR", f"Erreur affichage aide patterns: {e}", category="extraction_config")