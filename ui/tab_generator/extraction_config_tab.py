# ui/tab_generator/extraction_config_tab.py
# Onglet de configuration extraction textes oubliés - Générateur de Traductions Ren'Py
# VERSION AVEC COMBOBOX pour sélection langue unique

"""
Onglet de configuration pour l'extraction des textes oubliés par le SDK
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

def create_extraction_config_tab(parent, main_interface):
    """Crée l'onglet de configuration d'extraction - parent = frame scrollable (ajout au notebook fait par l'interface)."""
    theme = theme_manager.get_theme()
    
    tab_frame = tk.Frame(parent, bg=theme["bg"])
    tab_frame.pack(fill='both', expand=True)
    
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
            nb = getattr(main_interface, "notebook", None)
            if not nb:
                return
            current = nb.nametowidget(nb.select())
            w = tab_frame
            while w:
                if w == current:
                    _auto_scan_config_if_ready()
                    break
                w = getattr(w, "master", None)
        except Exception:
            pass

    if getattr(main_interface, "notebook", None):
        main_interface.notebook.bind("<<NotebookTabChanged>>", _on_tab_changed_config)
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
        ("• ", "blue"), ("99_Z_ScreenPreferences.rpy", "italic"), (" (sélecteur de langue)\n", "normal"),
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
        
        # Ajouter l'exemple par défaut s'il n'existe pas déjà
        example_exists = any(p.get('name') == "Exemple Regex" for p in patterns)
        if not example_exists:
            example_pattern = {
                'name': 'Exemple Regex',
                'pattern': '"QID_[^"]+"\\s*:\\s*\\[\\s*"([^"]+)"\\s*,\\s*"([^"]+)"\\s*,\\s*[\\s\\S]*?\\["hint",\\s*"([^"]+)"',
                'flags': 'gms',
                'description': 'Ceci est un exemple montrant comme fonctionne le système pour capturer de multiple groupes',
                'enabled': False,
                'test_text': '''"QID_MAIN_WAYHOME1": [
        "Find A Way Home",
        "Make your way to the Jumpgate to start your journey home...",
        "'map talk' in tris.done",
        "'SSIDArellarti' in GAME.mc.done", ["hint", "The Jumpgates might provide a way home eventually. Make sure you are well armed before you enter and explore other Star Systems.", "Q_MAIN"]
    ],''',
                'is_example': True  # Marquer comme exemple
            }
            patterns.insert(0, example_pattern)  # Ajouter en premier
        
        # Afficher tous les patterns
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
    """Ajoute un nouveau pattern personnalisé - ouvre la fenêtre vierge"""
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
    saved_test_text = ''  # Zone vierge par défaut pour nouveaux patterns
    if pattern_index is not None:
        patterns = config_manager.get_custom_extraction_patterns()
        if 0 <= pattern_index < len(patterns):
            pattern = patterns[pattern_index]
            name_var.set(pattern.get('name', ''))
            pattern_var.set(pattern.get('pattern', ''))
            flags_var.set(pattern.get('flags', ''))
            description_var.set(pattern.get('description', ''))
            enabled_var.set(pattern.get('enabled', False))
            saved_test_text = pattern.get('test_text', '')
    else:
        # Nouveaux patterns : zones vierges
        pass
    
    # Interface principale
    main_frame = tk.Frame(dialog, bg=theme["bg"])
    main_frame.pack(fill="both", expand=True, padx=10, pady=15)
    
    # Titre de la fenêtre centré en bleu accent
    title_frame = tk.Frame(main_frame, bg=theme["bg"])
    title_frame.pack(fill='x', pady=(0, 20))
    
    tk.Label(title_frame, text="Pattern Regex Personnalisé", 
             font=('Segoe UI', 14, 'bold'), bg=theme["bg"], fg=theme["accent"]).pack()
    
    # ===== SECTION 1: CONFIGURATION DU PATTERN =====
    config_section = tk.Frame(main_frame, bg=theme["bg"])
    config_section.pack(fill='x', pady=(0, 15))
    
    # Titre de la section
    tk.Label(config_section, text="⚙️ Configuration du Pattern", 
             font=('Segoe UI', 11, 'bold'), bg=theme["bg"], fg=theme["fg"]).pack(anchor='w', pady=(0, 10))
    
    # Grille 2x2 pour les champs
    grid_frame = tk.Frame(config_section, bg=theme["bg"])
    grid_frame.pack(fill='x', pady=(0, 10))
    
    # Ligne 1 : Nom | Description
    # Colonne 1 : Nom
    name_frame = tk.Frame(grid_frame, bg=theme["bg"])
    name_frame.pack(side='left', fill='x', expand=True, padx=(0, 5))
    
    tk.Label(name_frame, text="Nom:", bg=theme["bg"], fg=theme["fg"], 
             font=('Segoe UI', 9, 'bold')).pack(anchor='w')
    name_entry = tk.Entry(name_frame, textvariable=name_var, font=('Segoe UI', 9), 
                          bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["entry_fg"])
    name_entry.pack(fill='x', pady=(2, 0), ipady=3)
    
    # Colonne 2 : Description
    desc_frame = tk.Frame(grid_frame, bg=theme["bg"])
    desc_frame.pack(side='right', fill='x', expand=True, padx=(5, 0))
    
    tk.Label(desc_frame, text="Description:", bg=theme["bg"], fg=theme["fg"], 
             font=('Segoe UI', 9, 'bold')).pack(anchor='w')
    description_text = tk.Text(desc_frame, height=1, font=('Segoe UI', 9), 
                              bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["entry_fg"],
                              wrap=tk.WORD)
    description_text.pack(fill='x', pady=(2, 0), ipady=3, anchor='s')
    description_text.insert('1.0', description_var.get())
    
    # Ligne 2 : Labels Flags | Pattern Regex
    labels_frame = tk.Frame(config_section, bg=theme["bg"])
    labels_frame.pack(fill='x', pady=(0, 5))
    
    tk.Label(labels_frame, text="Flags:", bg=theme["bg"], fg=theme["fg"], 
             font=('Segoe UI', 9, 'bold')).pack(side='left')
    tk.Label(labels_frame, text="Pattern Regex:", bg=theme["bg"], fg=theme["fg"], 
             font=('Segoe UI', 9, 'bold')).pack(side='left', padx=(50, 0))
    
    # Ligne 3 : Champs Flags | Pattern Regex
    fields_frame = tk.Frame(config_section, bg=theme["bg"])
    fields_frame.pack(fill='x', pady=(0, 5))
    
    flags_entry = tk.Entry(fields_frame, textvariable=flags_var, font=('Segoe UI', 10), width=10,
                              bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["entry_fg"])
    flags_entry.pack(side='left', ipady=3)
    
    # Champ Pattern Regex avec coloration syntaxique
    pattern_text = tk.Text(fields_frame, height=1, font=('Consolas', 10),
                          bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["entry_fg"],
                          wrap=tk.NONE, relief='solid', borderwidth=1)
    pattern_text.pack(side='right', fill='x', expand=True, padx=(10, 0), ipady=3)
    pattern_text.insert('1.0', pattern_var.get())
    
    # Ligne 4 : Aide pour les flags
    help_frame = tk.Frame(config_section, bg=theme["bg"])
    help_frame.pack(fill='x')
    
    tk.Label(help_frame, text="i=insensible  m=multiligne  s=dotall  g=global", 
             bg=theme["bg"], fg='#888888', font=('Segoe UI', 8, 'italic')).pack(anchor='w')
    
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
                text="✅ Pattern activé",
                bg="#4ade80" if theme["bg"] == '#1a202c' else "#90EE90",  # Vert adapté au thème
                fg="#000000"   # Texte noir pour contraste
            )
        else:
            enabled_toggle_btn.config(
                text="❌ Pattern désactivé",
                bg="#f87171" if theme["bg"] == '#1a202c' else "#FFB6C1",  # Rouge adapté au thème
                fg="#000000"   # Texte noir pour contraste
            )
    
    # Le bouton sera déplacé dans la section des boutons d'action
    
    # ===== FONCTIONS DE COLORATION SYNTAXIQUE REGEX =====
    def highlight_regex_pattern():
        """Colore la regex en temps réel comme Regex101"""
        try:
            import re
            pattern_content = pattern_text.get('1.0', 'end-1c')
            
            # Supprimer tous les anciens tags
            pattern_text.tag_remove('group1', '1.0', 'end')
            pattern_text.tag_remove('group2', '1.0', 'end')
            pattern_text.tag_remove('group3', '1.0', 'end')
            pattern_text.tag_remove('metachar', '1.0', 'end')
            pattern_text.tag_remove('quantifier', '1.0', 'end')
            pattern_text.tag_remove('character_class', '1.0', 'end')
            pattern_text.tag_remove('escape', '1.0', 'end')
            pattern_text.tag_remove('error', '1.0', 'end')
            
            # Configuration des couleurs des tags
            pattern_text.tag_configure('group1', foreground='#4ade80', font=('Consolas', 10, 'bold'))  # Vert
            pattern_text.tag_configure('group2', foreground='#60a5fa', font=('Consolas', 10, 'bold'))  # Bleu
            pattern_text.tag_configure('group3', foreground='#fbbf24', font=('Consolas', 10, 'bold'))  # Orange
            pattern_text.tag_configure('metachar', foreground='#a78bfa', font=('Consolas', 10, 'bold'))  # Violet
            pattern_text.tag_configure('quantifier', foreground='#fb7185', font=('Consolas', 10, 'bold'))  # Rose
            pattern_text.tag_configure('character_class', foreground='#34d399', font=('Consolas', 10, 'bold'))  # Vert clair
            pattern_text.tag_configure('escape', foreground='#f59e0b', font=('Consolas', 10, 'bold'))  # Ambre
            pattern_text.tag_configure('error', foreground='#ef4444', font=('Consolas', 10, 'bold'))  # Rouge
            
            # Test de validité de la regex
            try:
                re.compile(pattern_content)
                is_valid = True
            except re.error:
                is_valid = False
                # Marquer toute la regex en rouge si invalide
                pattern_text.tag_add('error', '1.0', 'end')
                return
            
            if not pattern_content:
                return
            
            # Détecter les groupes de capture
            group_count = 0
            i = 0
            while i < len(pattern_content):
                char = pattern_content[i]
                
                # Groupes de capture ()
                if char == '(' and (i == 0 or pattern_content[i-1] != '\\'):
                    # Vérifier si c'est un groupe non-capturant (?:)
                    if i + 1 < len(pattern_content) and pattern_content[i+1] == '?':
                        i += 2
                        continue
                    
                    group_count += 1
                    # Trouver la parenthèse fermante correspondante
                    paren_count = 1
                    j = i + 1
                    while j < len(pattern_content) and paren_count > 0:
                        if pattern_content[j] == '(' and (j == 0 or pattern_content[j-1] != '\\'):
                            paren_count += 1
                        elif pattern_content[j] == ')' and (j == 0 or pattern_content[j-1] != '\\'):
                            paren_count -= 1
                        j += 1
                    
                    if paren_count == 0:
                        # Colorer le groupe
                        tag_name = f'group{(group_count % 3) + 1}'
                        pattern_text.tag_add(tag_name, f'1.{i}', f'1.{j}')
                    
                    i = j
                    continue
                
                # Classes de caractères []
                elif char == '[' and (i == 0 or pattern_content[i-1] != '\\'):
                    # Trouver la parenthèse fermante correspondante
                    j = i + 1
                    while j < len(pattern_content):
                        if pattern_content[j] == ']' and (j == 0 or pattern_content[j-1] != '\\'):
                            break
                        j += 1
                    
                    if j < len(pattern_content):
                        pattern_text.tag_add('character_class', f'1.{i}', f'1.{j+1}')
                        i = j + 1
                        continue
                
                # Quantificateurs
                elif char in '*+?{':
                    if char == '{':
                        # Trouver la parenthèse fermante correspondante
                        j = i + 1
                        while j < len(pattern_content) and pattern_content[j] != '}':
                            j += 1
                        if j < len(pattern_content):
                            pattern_text.tag_add('quantifier', f'1.{i}', f'1.{j+1}')
                            i = j + 1
                            continue
                    else:
                        pattern_text.tag_add('quantifier', f'1.{i}', f'1.{i+1}')
                
                # Métacaractères
                elif char in '.^$|':
                    pattern_text.tag_add('metachar', f'1.{i}', f'1.{i+1}')
                
                # Caractères échappés
                elif char == '\\' and i + 1 < len(pattern_content):
                    pattern_text.tag_add('escape', f'1.{i}', f'1.{i+2}')
                    i += 1
                
                i += 1
            
            # Mettre à jour la variable pattern_var
            pattern_var.set(pattern_content)
            
        except Exception as e:
            # En cas d'erreur, ne rien faire pour éviter de casser l'interface
            pass
    
    def on_pattern_change(event):
        """Callback appelé quand le pattern change"""
        # Programmer la coloration après un court délai pour éviter les conflits
        dialog.after(50, highlight_regex_pattern)
    
    def on_pattern_focus_out(event):
        """Callback appelé quand on quitte le champ pattern"""
        highlight_regex_pattern()
    
    # Bindings pour la coloration en temps réel
    pattern_text.bind('<KeyRelease>', on_pattern_change)
    pattern_text.bind('<FocusOut>', on_pattern_focus_out)
    
    # Coloration initiale
    dialog.after(100, highlight_regex_pattern)
    
    # ===== FONCTION DE SURBRILLANCE EN TEMPS RÉEL =====
    def highlight_test_text():
        """Surbrillance en temps réel dans la zone de test comme Regex101"""
        try:
            import re
            pattern_content = pattern_text.get('1.0', 'end-1c').strip()
            test_content = test_text.get('1.0', 'end-1c')
            
            # Supprimer tous les anciens tags de surbrillance
            test_text.tag_remove('match1', '1.0', 'end')
            test_text.tag_remove('match2', '1.0', 'end')
            test_text.tag_remove('match3', '1.0', 'end')
            test_text.tag_remove('full_match', '1.0', 'end')
            
            # Configuration des couleurs de surbrillance - Groupes capturés plus visibles
            test_text.tag_configure('match1', background='#4ade80', foreground='#000000', font=('Consolas', 9, 'bold'))  # Vert vif
            test_text.tag_configure('match2', background='#60a5fa', foreground='#000000', font=('Consolas', 9, 'bold'))  # Bleu vif
            test_text.tag_configure('match3', background='#fbbf24', foreground='#000000', font=('Consolas', 9, 'bold'))  # Orange vif
            test_text.tag_configure('full_match', background='#34d399', foreground='#000000', font=('Consolas', 9, 'bold'))  # Vert clair
            
            if not pattern_content or not test_content:
                return None
            
            # Tester si la regex est valide
            try:
                compiled_pattern = re.compile(pattern_content)
                is_valid = True
            except re.error:
                is_valid = False
                return None
            
            # Trouver toutes les correspondances
            matches = list(compiled_pattern.finditer(test_content))
            
            if not matches:
                return None
            
            # Fonction helper pour convertir position index vers position tkinter
            def index_to_tkinter(index):
                """Convertit un index de caractère en position tkinter (ligne.colonne)"""
                lines = test_content[:index].split('\n')
                line_num = len(lines)
                col_num = len(lines[-1])
                return f"{line_num}.{col_num}"
            
            # Surbrillancer les correspondances - FOCUS sur les groupes capturés
            for i, match in enumerate(matches):
                # Si il y a des groupes capturés, on surbrille seulement les groupes
                if match.groups():
                    for group_num, group in enumerate(match.groups(), 1):
                        if group is not None:
                            group_start = match.start(group_num)
                            group_end = match.end(group_num)
                            if group_start >= 0 and group_end >= 0:
                                group_start_pos = index_to_tkinter(group_start)
                                group_end_pos = index_to_tkinter(group_end)
                                tag_name = f'match{(group_num % 3) + 1}'
                                test_text.tag_add(tag_name, group_start_pos, group_end_pos)
                else:
                    # Si pas de groupes, on surbrille la correspondance complète
                    start_pos = index_to_tkinter(match.start())
                    end_pos = index_to_tkinter(match.end())
                    test_text.tag_add('full_match', start_pos, end_pos)
            
            # Retourner tous les groupes capturés pour le message de statut
            first_match = matches[0]
            if first_match.groups():
                # Afficher tous les groupes capturés avec format amélioré
                groups = [str(g) for g in first_match.groups() if g is not None]
                formatted_groups = []
                for i, group in enumerate(groups, 1):
                    formatted_groups.append(f"                       Groupe {i} => {group}")
                return "\n".join(formatted_groups)
            else:
                # Pas de groupes, retourner la correspondance complète
                return first_match.group(0)
            
        except Exception:
            return None
    
    def update_status_and_highlight():
        """Met à jour le statut et la surbrillance"""
        found_text = highlight_test_text()
        
        if found_text is not None:
            # Regex valide avec correspondance
            update_result_display(f"✅ Regex valide :\n{found_text}", success_color)
        else:
            # Regex invalide ou pas de correspondance
            pattern_content = pattern_text.get('1.0', 'end-1c').strip()
            if pattern_content:
                try:
                    import re
                    re.compile(pattern_content)
                    # Regex valide mais pas de correspondance
                    update_result_display("ℹ️ Regex valide mais aucune correspondance", theme["warning"])
                except re.error:
                    # Regex invalide
                    update_result_display("❌ Regex invalide", error_color)
            else:
                # Pas de regex
                update_result_display("⏳ Tapez une regex pour tester", theme["fg"])
    
    # Bindings pour la surbrillance en temps réel
    def on_pattern_change_with_highlight(event):
        """Callback combiné : coloration regex + surbrillance test"""
        dialog.after(50, lambda: (highlight_regex_pattern(), update_status_and_highlight()))
    
    def on_test_change(event):
        """Callback quand le texte de test change"""
        dialog.after(50, update_status_and_highlight)
    
    # Mise à jour des bindings
    pattern_text.bind('<KeyRelease>', on_pattern_change_with_highlight)
    pattern_text.bind('<FocusOut>', on_pattern_change_with_highlight)
    
    # ===== SECTION 2: ZONE DE TEST =====
    test_section = tk.Frame(main_frame, bg=theme["bg"])
    test_section.pack(fill='both', expand=True, pady=(0, 15))
    
    # Titre de la section
    tk.Label(test_section, text="🧪 Zone de Test en Temps Réel", 
             font=('Segoe UI', 11, 'bold'), bg=theme["bg"], fg=theme["fg"]).pack(anchor='w', pady=(0, 10))
    
    # Texte de test
    test_label_frame = tk.Frame(test_section, bg=theme["bg"])
    test_label_frame.pack(fill='x', pady=(0, 5))
    
    tk.Label(test_label_frame, text="Texte de test (sera sauvegardé):", 
             bg=theme["bg"], fg=theme["fg"], font=('Segoe UI', 9, 'bold')).pack(side='left')
    
    test_text = tk.Text(test_section, height=8, font=('Consolas', 9), 
                       bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["entry_fg"],
                       wrap='word', relief='solid', borderwidth=1)
    test_text.pack(fill='both', expand=True, pady=(0, 10))
    # Zone de test vierge pour nouveaux patterns, ou chargée pour modification
    if pattern_index is not None and saved_test_text:
        test_text.insert('1.0', saved_test_text)
    # Sinon, la zone reste vierge pour les nouveaux patterns
    
    # Binding pour la surbrillance quand le texte de test change
    test_text.bind('<KeyRelease>', on_test_change)
    
    # Plus besoin du bouton tester - feedback en temps réel !
    
    # ===== SECTION 3: RÉSULTATS =====
    result_section = tk.Frame(main_frame, bg=theme["bg"])
    result_section.pack(fill='both', expand=True, pady=(0, 15))
    
    # Titre de la section
    tk.Label(result_section, text="📊 Résultats du Test", 
             font=('Segoe UI', 11, 'bold'), bg=theme["bg"], fg=theme["fg"]).pack(anchor='w', pady=(0, 10))
    
    # Zone de résultats avec widget Text pour un meilleur contrôle de l'affichage
    result_text_widget = tk.Text(
        result_section,
        height=6,
        bg=theme["bg"],
        fg=theme["fg"],
        font=('Segoe UI', 10, 'bold'),
        wrap=tk.WORD,
        relief='flat',
        borderwidth=0,
        state='disabled',
        padx=5,
        pady=5
    )
    result_text_widget.pack(anchor='w', fill='x', pady=(10, 10))
    
    # Fonction pour mettre à jour le texte des résultats
    def update_result_display(text, color=None):
        result_text_widget.config(state='normal')
        result_text_widget.delete('1.0', 'end')
        result_text_widget.insert('1.0', text)
        if color:
            result_text_widget.config(fg=color)
        result_text_widget.config(state='disabled')
    
    # Configuration des couleurs pour le statut
    success_color = '#4ade80' if theme["bg"] == '#1a202c' else '#00aa00'  # Vert adapté au thème
    error_color = '#f87171' if theme["bg"] == '#1a202c' else '#ff0000'    # Rouge adapté au thème
    
    # ===== BOUTON D'AIDE =====
    help_frame = tk.Frame(main_frame, bg=theme["bg"])
    help_frame.pack(fill='x', pady=(0, 15))
    
    def show_pattern_help():
        """Affiche l'aide pour les patterns regex personnalisés"""
        help_dialog = tk.Toplevel(dialog)
        help_dialog.title("Aide - Patterns Regex Personnalisés")
        help_dialog.geometry("600x500")
        help_dialog.configure(bg=theme["bg"])
        help_dialog.resizable(False, False)
        
        # Titre
        title_frame = tk.Frame(help_dialog, bg=theme["bg"])
        title_frame.pack(fill='x', padx=15, pady=(15, 10))
        
        tk.Label(title_frame, text="💡 Aide - Patterns Regex Personnalisés", 
                 font=('Segoe UI', 14, 'bold'), bg=theme["bg"], fg=theme["accent"]).pack()
        
        # Contenu de l'aide
        content_frame = tk.Frame(help_dialog, bg=theme["bg"])
        content_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        help_text = """✨ Approche recommandée :
• Une regex = Un ou plusieurs éléments à capturer
• Support des groupes multiples : chaque groupe () crée un bloc old/new séparé
• Créez des patterns simples et efficaces
• Chaque pattern peut être activé/désactivé indépendamment

📝 Format des patterns :
• Groupes de capture : (contenu) pour capturer du texte
• Classes de caractères : [a-z] pour les lettres, [0-9] pour les chiffres
• Quantificateurs : * (0 ou plus), + (1 ou plus), ? (0 ou 1)
• Métacaractères : . (n'importe quel caractère), ^ (début), $ (fin)

🎨 Surbrillance en temps réel :
• Groupes capturés surlignés avec des couleurs différentes
• Validation immédiate de la syntaxe regex
• Feedback visuel instantané dans la zone de test

🔧 Exemples pratiques :
• Pour capturer du texte entre guillemets : "([^"]+)"
• Pour capturer plusieurs groupes : (\\w+)\\.(\\w+)\\(\"([^\"]+)\", \"([^\"]+)\"\\)
• Pour capturer des chiffres : (\\d+)"""
        
        help_label = tk.Label(content_frame, text=help_text, 
                             bg=theme["bg"], fg=theme["fg"], 
                             font=('Segoe UI', 10),
                             justify='left',
                             wraplength=550)
        help_label.pack(anchor='w', pady=(0, 15))
        
        # Bouton fermer
        close_btn = tk.Button(content_frame, text="✅ Fermer", 
                             command=help_dialog.destroy,
                             bg=theme["button_primary_bg"], fg="#000000",
                             font=('Segoe UI', 10, 'bold'),
                             pady=8, padx=20)
        close_btn.pack(pady=(10, 0))
    
    # Bouton d'aide
    help_btn = tk.Button(help_frame, text="❓ Aide", 
                        command=show_pattern_help,
                        bg=theme["button_help_bg"], fg="#000000",
                        font=('Segoe UI', 9, 'bold'),
                        pady=6, padx=15)
    help_btn.pack(pady=(0, 10))
    
    # Fonction test_pattern supprimée - géré par update_status_and_highlight
    
    # ===== SECTION 4: BOUTONS D'ACTION =====
    buttons_frame = tk.Frame(main_frame, bg=theme["bg"])
    buttons_frame.pack(fill='x', pady=(0, 10))
    
    def save_pattern():
        name = name_var.get().strip()
        pattern = pattern_text.get('1.0', 'end-1c').strip()
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
        font=('Segoe UI', 9),
        pady=4,
        padx=15
    ).pack(side='right', padx=(5, 0))
    
    # Bouton Pattern désactivé au milieu (largeur fixe)
    enabled_toggle_btn = tk.Button(
        buttons_frame,
        command=toggle_enabled,
        font=('Segoe UI', 9, 'bold'),
        relief='raised',
        borderwidth=2,
        pady=4,
        padx=15,
        cursor='hand2',
        width=16  # Largeur fixe adaptée à "Pattern désactivé"
    )
    enabled_toggle_btn.pack(side='right', padx=(5, 5))
    
    # Initialiser l'apparence du bouton
    update_enabled_button()
    
    tk.Button(
        buttons_frame,
        text="❌ Annuler",
        command=dialog.destroy,
        bg=theme["button_tertiary_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=15
    ).pack(side='right')
    
    # Plus besoin de Ctrl+Enter - feedback en temps réel !
    
    # Initialisation de la surbrillance au chargement
    dialog.after(200, update_status_and_highlight)

def _show_custom_patterns_help(main_interface):
    """Affiche l'aide simplifiée pour les patterns personnalisés"""
    message_styled = [
        ("Patterns Regex Personnalisés\n\n", "bold_blue"),
        
        ("Cette fonctionnalité vous permet de définir vos propres patterns regex pour détecter des textes spécifiques dans vos fichiers Ren'Py.\n\n", "normal"),
        
        ("✨ ", "blue"), ("Fonctionnement :\n", "bold"),
        ("• Chaque groupe de capture () crée un bloc old/new séparé\n", "normal"),
        ("• Support des groupes multiples en une seule regex\n", "normal"),
        ("• Chaque pattern peut être activé/désactivé indépendamment\n\n", "normal"),
        
        ("🏷️ ", "yellow"), ("Flags disponibles :\n", "bold"),
        ("• ", "normal"), ("i", "bold"), (" = insensible à la casse\n", "normal"),
        ("• ", "normal"), ("m", "bold"), (" = mode multiligne\n", "normal"),
        ("• ", "normal"), ("s", "bold"), (" = dotall (le . matche les retours à la ligne)\n", "normal"),
        ("• ", "normal"), ("g", "bold"), (" = global (implicite)\n\n", "normal"),
        
        ("💡 ", "green"), ("Exemple pratique :\n", "bold"),
        ("Pattern : ", "normal"), (r'"QID_[^"]+"\s*:\s*\[\s*"([^"]+)",\s*"([^"]+)".*\["hint",\s*"([^"]+)"', "italic"), ("\n", "normal"),
        ("→ Crée 3 blocs : Titre, Description, Hint\n\n", "normal"),
        
        ("🧪 ", "yellow"), ("Comment utiliser :\n", "bold"),
        ("• Cliquez sur ", "normal"), ("➕ Ajouter", "bold"), (" pour créer un nouveau pattern\n", "normal"),
        ("• Utilisez ", "normal"), ("✏️ Modifier", "bold"), (" sur l'exemple pour comprendre le fonctionnement\n", "normal"),
        ("• Testez vos regex directement dans la fenêtre de modification\n\n", "normal"),
        
        ("⚠️ ", "red"), ("Important :", "bold"), ("\n", "normal"),
        ("• Les textes extraits sont classés en ", "normal"), ("auto_safe", "bold"), ("\n", "normal"),
        ("• Les patterns analysent ", "normal"), ("game/", "bold"), (" (hors tl/)\n", "normal"),
        ("• Pour plus de détails, consultez l'aide dans la fenêtre de modification", "normal")
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