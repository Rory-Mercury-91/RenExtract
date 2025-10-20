# ui/tab_tools/coherence_tab.py
# Onglet de vérification de cohérence - Outils de Maintenance Ren'Py

"""
Onglet de vérification de cohérence des traductions Ren'Py
- Interface de sélection langue/fichiers avec ProjectLanguageSelector
- Options de vérification personnalisables
- Exclusions de fichiers et lignes
- Génération de rapports détaillés
- TOUTE la logique métier incluse
"""

import os
import threading
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional

from ui.themes import theme_manager
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import show_translated_messagebox

def create_coherence_tab(parent_notebook, main_interface):
    """Crée l'onglet de vérification de cohérence"""
    theme = theme_manager.get_theme()
    
    # Frame principal de l'onglet
    tab_frame = tk.Frame(parent_notebook, bg=theme["bg"])
    parent_notebook.add(tab_frame, text="🧪 Vérification Cohérence")
    
    # Header avec titre centré et bouton d'aide à droite
    help_frame = tk.Frame(tab_frame, bg=theme["bg"])
    help_frame.pack(fill='x', padx=20, pady=(15, 10))
    
    # Titre descriptif centré
    desc_label = tk.Label(
        help_frame,
        text="Vérification de cohérence des traductions avec détection d'incohérences",
        font=('Segoe UI', 10, 'bold'),
        justify='center',
        bg=theme["bg"],
        fg=theme["accent"]
    )
    desc_label.pack(fill='x', anchor='center')
    
    # Bouton d'aide aligné à droite
    help_btn = tk.Button(
        help_frame,
        text="À quoi ça sert ?",
        command=lambda: _show_coherence_help(main_interface),
        bg=theme["button_secondary_bg"],
        fg="#000000",
        font=('Segoe UI', 10, 'bold'),
        width=15,
        height=1,
        relief='flat',
        cursor='hand2'
    )
    help_btn.pack(anchor='e', pady=(10, 0))
    
    # Contenu principal
    _create_coherence_content(tab_frame, main_interface)

def _create_coherence_content(parent, main_interface):
    """Crée le contenu de l'onglet cohérence"""
    theme = theme_manager.get_theme()
    
    # === 1. SÉLECTION DE PROJET ===
    # Sélecteur harmonisé (on verrouille la partie 'projet')
    from ui.shared.project_widgets import ProjectLanguageSelector

    # On instancie le widget SANS sa propre barre de sélection de projet
    main_interface.coherence_project_selector = ProjectLanguageSelector(
        parent,
        initial_project_path=main_interface.current_project_path,
        on_language_changed=lambda lang: _on_coherence_language_changed(main_interface, lang),
        on_files_changed=lambda info: _on_coherence_files_changed(main_interface, info),
        show_project_input=False
    )

    # Appliquer les exclusions initiales
    exclusions_str = main_interface.coherence_excluded_files_var.get()
    if exclusions_str:
        main_interface.coherence_project_selector.set_exclusions(exclusions_str)

    # S'assurer que le widget pointe bien sur le projet du header
    try:
        if main_interface.current_project_path:
            main_interface.coherence_project_selector._validate_and_set_project(main_interface.current_project_path)
    except Exception:
        pass
    
    # === 2. TYPES DE CONTRÔLES ===
    # Options d'analyse
    options_title = tk.Label(
        parent,
        text="🔧 Types de vérifications à effectuer :",
        font=('Segoe UI', 10, 'bold'),
        bg=theme["bg"],
        fg=theme["accent"]
    )
    options_title.pack(anchor='w', padx=20, pady=(20, 10))
    
    # Frame pour les options en grille 5x3
    options_container = tk.Frame(parent, bg=theme["bg"])
    options_container.pack(fill='x', padx=20, pady=(0, 10))
    
    # Configuration de la grille 5x3 (5 colonnes, 3 lignes)
    grid_columns = 5
    
    # Liste des options avec leurs variables et textes
    options_data = [
        (main_interface.check_variables_var, "Variables [] incohérentes"),
        (main_interface.check_tags_var, "Balises {} incohérentes"),
        (main_interface.check_untranslated_var, "Lignes non traduites"),
        (main_interface.check_ellipsis_var, "… Ellipsis (-- → ...)"),
        (main_interface.check_escape_sequences_var, "\\ Séquences d'échappement (\\n, \\t, \\r, \\\\)"),
        (main_interface.check_percentages_var, "% Variables de formatage (%s, %d, %%)"),
        (main_interface.check_quotations_var, "\" Guillemets et échappements"),
        (main_interface.check_parentheses_var, "() Parenthèses et crochets"),
        (main_interface.check_syntax_var, "Syntaxe Ren'Py et structure"),
        (main_interface.check_deepl_ellipsis_var, "[…] Ellipses DeepL [...] → ..."),
        (main_interface.check_isolated_percent_var, "% Pourcentages isolés (% → %%)"),
        (main_interface.check_french_quotes_var, "«» Guillemets français «» → \""),
        (main_interface.check_line_structure_var, "Structure des lignes old/new")
    ]
    
    # Créer les cases à cocher en grille
    for i, (var, text) in enumerate(options_data):
        row = i // grid_columns
        col = i % grid_columns
        
        checkbox = tk.Checkbutton(
            options_container,
            text=text,
            variable=var,
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"],
            selectcolor=theme["bg"],
            activebackground=theme["bg"],
            activeforeground=theme["fg"],
            anchor='w'
        )
        checkbox.grid(row=row, column=col, sticky='w', padx=5, pady=2)
    
    # Configurer les colonnes pour qu'elles s'étendent
    for col in range(grid_columns):
        options_container.grid_columnconfigure(col, weight=1)
    
    # Boutons de contrôle des options
    buttons_controls_frame = tk.Frame(parent, bg=theme["bg"])
    buttons_controls_frame.pack(fill='x', padx=20, pady=(10, 20))
    
    # Frame horizontal pour les boutons
    all_buttons_frame = tk.Frame(buttons_controls_frame, bg=theme["bg"])
    all_buttons_frame.pack()
    
    select_all_btn = tk.Button(
        all_buttons_frame,
        text="✅ Tout sélectionner",
        command=lambda: _select_all_coherence_options(main_interface),
        bg=theme["button_primary_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    select_all_btn.pack(side='left', padx=(0, 10))
    
    select_none_btn = tk.Button(
        all_buttons_frame,
        text="❌ Tout désélectionner", 
        command=lambda: _select_no_coherence_options(main_interface),
        bg=theme["button_danger_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    select_none_btn.pack(side='left')
    
    # === 3. EXCLUSIONS DE FICHIERS ===
    exclusions_frame = tk.Frame(parent, bg=theme["bg"])
    exclusions_frame.pack(fill='x', padx=20, pady=(20, 10))
    
    # Header avec titre et bouton de gestion des exclusions de lignes
    exclusions_header = tk.Frame(exclusions_frame, bg=theme["bg"])
    exclusions_header.pack(fill='x', pady=(0, 5))
    
    tk.Label(
        exclusions_header,
        text="🚫 Fichiers à exclure :",
        font=('Segoe UI', 10, 'bold'),
        bg=theme["bg"],
        fg=theme["accent"]
    ).pack(side='left')
    
    # Bouton pour gérer les exclusions de lignes (à droite)
    manage_exclusions_btn = tk.Button(
        exclusions_header,
        text="⚙️ Gérer les exclusions de lignes",
        command=lambda: _open_exclusions_manager(main_interface),
        bg=theme["button_nav_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=2,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    manage_exclusions_btn.pack(side='right')
    
    main_interface.coherence_excluded_files_entry = tk.Entry(
        exclusions_frame,
        textvariable=main_interface.coherence_excluded_files_var,
        font=('Segoe UI', 10),
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        insertbackground=theme["entry_fg"],
        relief='solid',
        borderwidth=1
    )
    main_interface.coherence_excluded_files_entry.pack(fill='x', pady=(0, 5), ipady=4)
    
    tk.Label(
        exclusions_frame,
        text="💡 Ex: z_lang.rpy, common.rpy",
        font=('Segoe UI', 8, 'italic'),
        bg=theme["bg"],
        fg='#2980B9'
    ).pack(anchor='w')
    
    # === 4. BOUTONS D'ACTION ===
    # Container horizontal pour les boutons
    buttons_frame = tk.Frame(parent, bg=theme["bg"])
    buttons_frame.pack(fill='x', padx=20, pady=(30, 20))
    
    # Boutons à droite
    buttons_right_frame = tk.Frame(buttons_frame, bg=theme["bg"])
    buttons_right_frame.pack(side='right')
    
    main_interface.coherence_detailed_report_btn = tk.Button(
        buttons_right_frame,
        text="📄 Rapport détaillé",
        command=lambda: _open_coherence_detailed_report(main_interface),
        bg=theme["button_secondary_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    main_interface.coherence_detailed_report_btn.pack(side='left', padx=(0, 5))
    
    main_interface.coherence_open_folder_btn = tk.Button(
        buttons_right_frame,
        text="📁 Ouvrir dossier",
        command=lambda: _open_coherence_analysis_folder(main_interface),
        bg=theme["button_nav_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    main_interface.coherence_open_folder_btn.pack(side='left', padx=(0, 10))
    
    main_interface.coherence_analyze_btn = tk.Button(
        buttons_right_frame,
        text="🚀 Démarrer l'analyse",
        command=lambda: start_coherence_analysis(main_interface),
        bg=theme["button_primary_bg"],
        fg="#000000",
        font=('Segoe UI', 9, 'bold'),
        pady=6,
        padx=12
    )
    main_interface.coherence_analyze_btn.pack(side='left')
    
    # Note: Le bouton d'analyse de cohérence n'est PAS ajouté à operation_buttons
    # car c'est un outil indépendant qui ne doit pas être bloqué par les opérations principales
    # (extraction, reconstruction, génération TL, etc.)
    
    # Configurer la sauvegarde automatique des options avec délai pour éviter les notifications au démarrage
    _setup_auto_save_coherence_options(main_interface)

# ===== FONCTIONS DE CONTRÔLE DES OPTIONS =====

def _select_all_coherence_options(main_interface):
    """Sélectionne toutes les options de vérification"""
    try:
        # Temporairement désactiver les notifications pour éviter le spam
        main_interface._coherence_initialization_complete = False
        
        # Liste de toutes les variables de vérification
        coherence_vars = [
            main_interface.check_variables_var,
            main_interface.check_tags_var,
            main_interface.check_untranslated_var,
            main_interface.check_ellipsis_var,
            main_interface.check_escape_sequences_var,
            main_interface.check_percentages_var,
            main_interface.check_quotations_var,
            main_interface.check_parentheses_var,
            main_interface.check_syntax_var,
            main_interface.check_deepl_ellipsis_var,
            main_interface.check_isolated_percent_var,
            main_interface.check_french_quotes_var,
            main_interface.check_line_structure_var
        ]
        
        # Sélectionner toutes les options
        for var in coherence_vars:
            var.set(True)
        
        # Réactiver les notifications après un court délai
        def re_enable_notifications():
            main_interface._coherence_initialization_complete = True
        
        main_interface.window.after(100, re_enable_notifications)
        
        # Notification globale
        _show_toast(main_interface, "✅ Toutes les vérifications sélectionnées", "success")
        
        log_message("INFO", "Toutes les options de vérification sélectionnées", category="coherence_tab")
        
    except Exception as e:
        log_message("ERREUR", f"Erreur sélection toutes options: {e}", category="coherence_tab")

def _select_no_coherence_options(main_interface):
    """Désélectionne toutes les options de vérification"""
    try:
        # Temporairement désactiver les notifications pour éviter le spam
        main_interface._coherence_initialization_complete = False
        
        # Liste de toutes les variables de vérification
        coherence_vars = [
            main_interface.check_variables_var,
            main_interface.check_tags_var,
            main_interface.check_untranslated_var,
            main_interface.check_ellipsis_var,
            main_interface.check_escape_sequences_var,
            main_interface.check_percentages_var,
            main_interface.check_quotations_var,
            main_interface.check_parentheses_var,
            main_interface.check_syntax_var,
            main_interface.check_deepl_ellipsis_var,
            main_interface.check_isolated_percent_var,
            main_interface.check_french_quotes_var,
            main_interface.check_line_structure_var
        ]
        
        # Désélectionner toutes les options
        for var in coherence_vars:
            var.set(False)
        
        # Réactiver les notifications après un court délai
        def re_enable_notifications():
            main_interface._coherence_initialization_complete = True
        
        main_interface.window.after(100, re_enable_notifications)
        
        # Notification globale
        _show_toast(main_interface, "⚠️ Toutes les vérifications désélectionnées", "warning")
        
        log_message("INFO", "Toutes les options de vérification désélectionnées", category="coherence_tab")
        
    except Exception as e:
        log_message("ERREUR", f"Erreur désélection toutes options: {e}", category="coherence_tab")

# ===== FONCTIONS DE CALLBACKS =====

def _on_coherence_language_changed(main_interface, language_name):
    """Callback quand la langue cohérence change"""
    try:
        main_interface.coherence_language = language_name
        _update_coherence_status(main_interface, f"🌐 Langue sélectionnée: {language_name}")
    except Exception as e:
        log_message("ERREUR", f"Erreur callback langue cohérence: {e}", category="coherence_tab")

def _on_coherence_files_changed(main_interface, selection_info):
    """Callback quand la sélection de fichiers cohérence change"""
    try:
        main_interface.coherence_selection_info = selection_info
        
        if selection_info['is_all_files']:
            file_count = len(selection_info['target_files'])
            _update_coherence_status(main_interface, f"Prêt à analyser {file_count} fichiers de {selection_info['language']}")
        else:
            file_name = selection_info['selected_option']
            _update_coherence_status(main_interface, f"Prêt à analyser le fichier {file_name}")
            
    except Exception as e:
        log_message("ERREUR", f"Erreur callback fichiers cohérence: {e}", category="coherence_tab")

# ===== FONCTIONS D'ANALYSE =====

def start_coherence_analysis(main_interface):
    """Lance l'analyse de cohérence"""
    try:
        # Validation de la sélection
        if not hasattr(main_interface, 'coherence_selection_info') or not main_interface.coherence_selection_info:
            _update_coherence_status(main_interface, "❌ Aucune sélection configurée")
            show_translated_messagebox(
                'warning',
                'Configuration incomplète',
                'Veuillez configurer un projet, une langue et une sélection de fichiers avant de lancer l\'analyse.',
                parent=main_interface.window
            )
            return
        
        selection = main_interface.coherence_selection_info
        
        # Vérifications de validité
        if not selection['project_path'] or not os.path.exists(selection['project_path']):
            _update_coherence_status(main_interface, "❌ Projet invalide")
            return
        
        if not selection['language']:
            _update_coherence_status(main_interface, "❌ Aucune langue sélectionnée")
            return
        
        if not selection['file_paths']:
            _update_coherence_status(main_interface, "❌ Aucun fichier à analyser")
            return
        
        # Préparer les informations d'analyse
        if selection['is_all_files']:
            mode_text = f"dossier {selection['language']} ({len(selection['file_paths'])} fichiers)"
            analysis_target = os.path.join(selection['project_path'], "game", "tl", selection['language'])
        else:
            mode_text = f"fichier {selection['selected_option']}"
            analysis_target = selection['file_paths'][0]
        
        log_message("INFO", f"🚀 Début de l'analyse de cohérence ({mode_text})", category="coherence_tab")
        
        # Désactiver le bouton et lancer l'analyse
        main_interface.coherence_analyze_btn.config(state='disabled', text="⏳ Analyse en cours...")
        run_coherence_analysis_thread(main_interface, analysis_target, selection)
        
    except Exception as e:
        log_message("ERREUR", f"Erreur lors du démarrage de l'analyse : {e}", category="coherence_tab")
        _update_coherence_status(main_interface, "❌ Erreur lors du démarrage")
        main_interface.coherence_analyze_btn.config(state='normal', text="🚀 Démarrer l'analyse")

def run_coherence_analysis_thread(main_interface, analysis_target, selection_info):
    """Exécute l'analyse cohérence dans un thread"""
    def analysis_worker():
        try:
            # Import du vérificateur de cohérence unifié
            from core.services.tools.coherence_checker_business import check_coherence_unified, set_coherence_options
            
            # Configurer les options d'analyse
            analysis_options = _get_coherence_analysis_options(main_interface)
            set_coherence_options(analysis_options)
            
            # Lancer l'analyse
            results = check_coherence_unified(
                analysis_target, 
                return_details=True,
                selection_info=selection_info
            )
            
            # Stocker les résultats
            main_interface.analysis_results = results
            if isinstance(results, dict):
                results['selection_info'] = selection_info
                main_interface.rapport_path = results.get('rapport_path')
            else:
                main_interface.rapport_path = results
                main_interface.analysis_results = {
                    'rapport_path': results,
                    'selection_info': selection_info
                }
            
            # Mettre à jour l'interface
            main_interface.window.after(100, lambda: _display_coherence_results(main_interface))
            
        except Exception as e:
            log_message("ERREUR", f"Erreur pendant l'analyse : {e}", category="coherence_tab")
            error_message = str(e)
            main_interface.window.after(100, lambda: _coherence_analysis_error(main_interface, error_message))
    
    # Lancer le thread
    thread = threading.Thread(target=analysis_worker, daemon=True)
    thread.start()

def _display_coherence_results(main_interface):
    """Affiche les résultats de cohérence"""
    try:
        if not main_interface.analysis_results:
            _coherence_analysis_error(main_interface, "Aucun résultat d'analyse disponible")
            return
    
        # Calculer les statistiques
        if isinstance(main_interface.analysis_results, dict) and 'stats' in main_interface.analysis_results:
            stats = main_interface.analysis_results['stats']
            files_analyzed = stats.get('files_analyzed', 0)
            total_issues = stats.get('total_issues', 0)
            issues_by_type = stats.get('issues_by_type', {})
        else:
            files_analyzed = 0
            total_issues = 0
            issues_by_type = {}
    
        # Assurer des valeurs valides
        if not isinstance(files_analyzed, int):
            files_analyzed = 0
        if not isinstance(total_issues, int):
            total_issues = 0
    
        # Compter les types de problèmes distincts
        distinct_types = 0
        if isinstance(issues_by_type, dict):
            distinct_types = sum(1 for count in issues_by_type.values() if _get_issue_count(count) > 0)
        
        # Activer les boutons d'action
        main_interface.coherence_detailed_report_btn.config(state='normal')
        main_interface.coherence_open_folder_btn.config(state='normal')
    
        # Remettre le bouton d'analyse normal
        main_interface.coherence_analyze_btn.config(state='normal', text="🚀 Nouvelle analyse")
    
        # Mettre à jour l'état avec un résumé compact
        if total_issues == 0:
            status_message = "✅ Analyse terminée - Aucun problème détecté"
        else:
            if distinct_types > 0:
                status_message = f"⚠️ Analyse terminée - {total_issues} erreur(s) sur {distinct_types} type(s)"
            else:
                status_message = f"⚠️ Analyse terminée - {total_issues} erreur(s) détectée(s)"
        
        _update_coherence_status(main_interface, status_message)
    
        # Log du résultat
        log_message("INFO", f"✅ Analyse terminée - {files_analyzed} fichiers, {total_issues} problèmes, {distinct_types} types", category="coherence_tab")
    
    except Exception as e:
        error_msg = f"Erreur lors de l'affichage des résultats: {str(e)}"
        log_message("ERREUR", f"Erreur affichage résultats : {e}", category="coherence_tab")
        _coherence_analysis_error(main_interface, error_msg)

def _get_issue_count(issues_value):
    """Utilitaire pour obtenir le nombre de problèmes"""
    if isinstance(issues_value, int):
        return issues_value
    elif isinstance(issues_value, list):
        return len(issues_value)
    else:
        return 0

def _coherence_analysis_error(main_interface, error_message):
    """Gère les erreurs d'analyse cohérence"""
    main_interface.coherence_analyze_btn.config(state='normal', text="🚀 Lancer l'analyse")
    _update_coherence_status(main_interface, f"❌ Erreur: {error_message}")
    
    show_translated_messagebox(
        'error',
        '❌ Erreur d\'analyse',
        f'Une erreur est survenue pendant l\'analyse:\n\n{error_message}',
        parent=main_interface.window
    )

def _get_coherence_analysis_options(main_interface):
    """Retourne les options d'analyse actuelles pour l'analyseur"""
    return {
        'check_variables': main_interface.check_variables_var.get(),
        'check_tags': main_interface.check_tags_var.get(),
        'check_special_codes': main_interface.check_special_codes_var.get(),
        'check_untranslated': main_interface.check_untranslated_var.get(),
        'check_ellipsis': main_interface.check_ellipsis_var.get(),
        'check_escape_sequences': main_interface.check_escape_sequences_var.get(),
        'check_percentages': main_interface.check_percentages_var.get(),
        'check_quotations': main_interface.check_quotations_var.get(),
        'check_parentheses': main_interface.check_parentheses_var.get(),
        'check_syntax': main_interface.check_syntax_var.get(),
        'check_deepl_ellipsis': main_interface.check_deepl_ellipsis_var.get(),
        'check_isolated_percent': main_interface.check_isolated_percent_var.get(),
        'check_french_quotes': main_interface.check_french_quotes_var.get(),
        'check_line_structure': main_interface.check_line_structure_var.get(),
        'custom_exclusions': ['OK', 'Menu', 'Continue', 'Level']  # Valeurs par défaut
    }

# ===== FONCTIONS D'AIDE =====

def _show_coherence_help(main_interface):
    """Affiche l'aide pour l'outil de cohérence"""
    from infrastructure.helpers.unified_functions import show_custom_messagebox
    from ui.themes import theme_manager
    
    theme = theme_manager.get_theme()
    
    # Message avec couleurs et styles
    help_message = [
        ("🧪 ", "bold_green"),
        ("Vérification de Cohérence des Traductions", "bold"),
        ("\n\n", "normal"),
        ("Cet outil détecte les incohérences entre les lignes OLD et NEW dans vos fichiers de traduction Ren'Py.", "normal"),
        ("\n\n", "normal"),
        ("🔧 ", "bold_blue"),
        ("Types de Vérifications Disponibles :", "bold"),
        ("\n", "normal"),
        ("• ", "green"),
        ("Variables [] incohérentes", "bold_green"),
        (" - Détection des variables manquantes ou mal formatées", "normal"),
        ("\n", "normal"),
        ("• ", "green"),
        ("Balises {} incohérentes", "bold_green"),
        (" - Vérification des balises de formatage", "normal"),
        ("\n", "normal"),
        ("• ", "green"),
        ("Lignes non traduites", "bold_green"),
        (" - Identification des textes encore en anglais", "normal"),
        ("\n", "normal"),
        ("• ", "green"),
        ("Ellipses (-- → ...)", "bold_green"),
        (" - Conversion automatique des ellipses", "normal"),
        ("\n", "normal"),
        ("• ", "green"),
        ("Séquences d'échappement", "bold_green"),
        (" (\\n, \\t, \\r, \\\\) - Validation des caractères spéciaux", "normal"),
        ("\n", "normal"),
        ("• ", "green"),
        ("Variables de formatage", "bold_green"),
        (" (%s, %d, %%) - Cohérence des formats", "normal"),
        ("\n", "normal"),
        ("• ", "green"),
        ("Guillemets et échappements", "bold_green"),
        (" - Vérification des guillemets corrects", "normal"),
        ("\n", "normal"),
        ("• ", "green"),
        ("Parenthèses et crochets", "bold_green"),
        (" - Équilibrage des délimiteurs", "normal"),
        ("\n", "normal"),
        ("• ", "green"),
        ("Syntaxe Ren'Py", "bold_green"),
        (" - Validation de la structure du code", "normal"),
        ("\n", "normal"),
        ("• ", "green"),
        ("Ellipses DeepL", "bold_green"),
        (" ([…] → ...) - Correction des ellipses de traduction", "normal"),
        ("\n", "normal"),
        ("• ", "green"),
        ("Pourcentages isolés", "bold_green"),
        (" (% → %%) - Échappement des pourcentages", "normal"),
        ("\n", "normal"),
        ("• ", "green"),
        ("Guillemets français", "bold_green"),
        (" («» → \") - Conversion vers guillemets standards", "normal"),
        ("\n", "normal"),
        ("• ", "green"),
        ("Structure des lignes", "bold_green"),
        (" - Cohérence old/new", "normal"),
        ("\n\n", "normal"),
        ("🎯 ", "bold"),
        ("Guide d'utilisation :", "bold"),
        ("\n", "normal"),
        ("1. ", "bold"),
        ("Sélectionnez la langue et les fichiers", "bold"),
        ("\n", "normal"),
        ("2. ", "bold"),
        ("Choisissez les types de vérifications", "bold"),
        (" (utilisez les boutons \"Tout sélectionner\" / \"Tout désélectionner\")", "normal"),
        ("\n", "normal"),
        ("3. ", "bold"),
        ("Configurez les exclusions de fichiers", "bold"),
        (" si nécessaire", "normal"),
        ("\n", "normal"),
        ("4. ", "bold"),
        ("Cliquez sur \"Démarrer l'analyse\"", "bold"),
        ("\n\n", "normal"),
        ("📊 ", "bold_blue"),
        ("Résultats et Rapports :", "bold"),
        ("\n", "normal"),
        ("• ", "blue"),
        ("Rapport détaillé", "bold_blue"),
        (" généré automatiquement", "normal"),
        ("\n", "normal"),
        ("• ", "blue"),
        ("Statistiques par type d'erreur", "bold_blue"),
        (" avec compteurs", "normal"),
        ("\n", "normal"),
        ("• ", "blue"),
        ("Localisation précise", "bold_blue"),
        (" des problèmes (fichier + ligne)", "normal"),
        ("\n", "normal"),
        ("• ", "blue"),
        ("Ouverture automatique", "bold_blue"),
        (" du dossier de résultats", "normal"),
        ("\n\n", "normal"),
        ("💡 ", "bold_yellow"),
        ("Conseils d'utilisation :", "bold"),
        ("\n", "normal"),
        ("• ", "yellow"),
        ("Commencez par sélectionner", "bold_yellow"),
        (" toutes les vérifications", "normal"),
        ("\n", "normal"),
        ("• ", "yellow"),
        ("Excluez les fichiers", "bold_yellow"),
        (" modifiés manuellement", "normal"),
        ("\n", "normal"),
        ("• ", "yellow"),
        ("Vérifiez les résultats", "bold_yellow"),
        (" avant de corriger automatiquement", "normal")
    ]
    
    show_custom_messagebox(
        'info',
        '🧪 Aide - Vérification de Cohérence',
        help_message,
        theme,
        parent=main_interface.window
    )

# ===== FONCTIONS D'ACCÈS AUX RAPPORTS =====

def _open_coherence_detailed_report(main_interface):
    """Ouvre le rapport détaillé de cohérence"""
    try:
        if not main_interface.rapport_path or not os.path.exists(main_interface.rapport_path):
            show_translated_messagebox(
                'warning',
                'Rapport non disponible',
                'Le rapport détaillé n\'est pas disponible ou a été supprimé.',
                parent=main_interface.window
            )
            return
        
        # Ouvrir le fichier avec l'application par défaut
        from core.models.files.file_manager import FileOpener
        FileOpener.open_files([main_interface.rapport_path], True)
        
        log_message("INFO", f"Rapport détaillé ouvert : {main_interface.rapport_path}", category="coherence_tab")
        
    except Exception as e:
        log_message("ERREUR", f"Erreur ouverture rapport : {e}", category="coherence_tab")
        show_translated_messagebox(
            'error',
            'Erreur',
            f'Impossible d\'ouvrir le rapport détaillé:\n\n{e}',
            parent=main_interface.window
        )

def _open_coherence_analysis_folder(main_interface):
    """Ouvre le dossier contenant les rapports de cohérence"""
    try:
        if not main_interface.rapport_path:
            from infrastructure.config.constants import FOLDERS
            folder_path = FOLDERS.get("warnings", "")
        else:
            folder_path = os.path.dirname(main_interface.rapport_path)
        
        if not os.path.exists(folder_path):
            show_translated_messagebox(
                'warning',
                'Dossier non trouvé',
                'Le dossier des rapports n\'existe pas encore.',
                parent=main_interface.window
            )
            return
        
        # Ouvrir le dossier
        import subprocess
        import platform
        
        if platform.system() == "Windows":
            os.startfile(folder_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", folder_path])
        else:  # Linux
            subprocess.run(["xdg-open", folder_path])
        
        log_message("INFO", f"Dossier des rapports ouvert : {folder_path}", category="coherence_tab")
        
    except Exception as e:
        log_message("ERREUR", f"Erreur ouverture dossier : {e}", category="coherence_tab")
        show_translated_messagebox(
            'error',
            'Erreur',
            f'Impossible d\'ouvrir le dossier:\n\n{e}',
            parent=main_interface.window
        )

def _update_coherence_status(main_interface, message):
    """Met à jour le statut cohérence"""
    try:
        # Utiliser la méthode de mise à jour de statut de l'interface principale
        if hasattr(main_interface, '_update_status'):
            main_interface._update_status(message)
        else:
            log_message("INFO", message, category="coherence_tab")
            
    except Exception as e:
        log_message("ERREUR", f"Erreur update_coherence_status: {e}", category="coherence_tab")

# ===== FONCTIONS DE SAUVEGARDE AUTOMATIQUE =====

def _save_coherence_options(main_interface):
    """Sauvegarde les options de cohérence"""
    try:
        # Sauvegarder les options d'analyse
        config_manager.set('coherence_check_variables', main_interface.check_variables_var.get())
        config_manager.set('coherence_check_tags', main_interface.check_tags_var.get())
        config_manager.set('coherence_check_special_codes', main_interface.check_special_codes_var.get())
        config_manager.set('coherence_check_untranslated', main_interface.check_untranslated_var.get())
        config_manager.set('coherence_check_ellipsis', main_interface.check_ellipsis_var.get())
        config_manager.set('coherence_check_escape_sequences', main_interface.check_escape_sequences_var.get())
        config_manager.set('coherence_check_percentages', main_interface.check_percentages_var.get())
        config_manager.set('coherence_check_quotations', main_interface.check_quotations_var.get())
        config_manager.set('coherence_check_parentheses', main_interface.check_parentheses_var.get())
        config_manager.set('coherence_check_syntax', main_interface.check_syntax_var.get())
        config_manager.set('coherence_check_deepl_ellipsis', main_interface.check_deepl_ellipsis_var.get())
        config_manager.set('coherence_check_isolated_percent', main_interface.check_isolated_percent_var.get())
        config_manager.set('coherence_check_french_quotes', main_interface.check_french_quotes_var.get())
        config_manager.set('coherence_check_line_structure', main_interface.check_line_structure_var.get())
        
        # Sauvegarder les exclusions de fichiers
        config_manager.set('coherence_excluded_files', main_interface.coherence_excluded_files_var.get())
        
        # Appliquer les exclusions au sélecteur de projet
        if hasattr(main_interface, 'coherence_project_selector') and main_interface.coherence_project_selector:
            exclusions_str = main_interface.coherence_excluded_files_var.get()
            main_interface.coherence_project_selector.set_exclusions(exclusions_str)
        
        # 🆕 NE PLUS sauvegarder coherence_custom_exclusions depuis cette interface
        # Les exclusions sont maintenant gérées exclusivement via le rapport HTML interactif
        # (structure dictionnaire par projet/fichier/ligne, pas une simple liste de textes)
        
        # Compter les options activées
        enabled_count = sum([
            main_interface.check_variables_var.get(),
            main_interface.check_tags_var.get(), 
            main_interface.check_special_codes_var.get(),
            main_interface.check_untranslated_var.get(),
            main_interface.check_ellipsis_var.get(),
            main_interface.check_escape_sequences_var.get(),
            main_interface.check_percentages_var.get(),
            main_interface.check_quotations_var.get(),
            main_interface.check_parentheses_var.get(),
            main_interface.check_syntax_var.get(),
            main_interface.check_deepl_ellipsis_var.get(),
            main_interface.check_isolated_percent_var.get(),
            main_interface.check_french_quotes_var.get(),
            main_interface.check_line_structure_var.get()
        ])
        
        _update_coherence_status(main_interface, f"💾 Options sauvegardées - {enabled_count} vérifications, {len(exclusions_list)} exclusions")
        
        log_message("INFO", f"Options cohérence sauvegardées - {enabled_count} vérifications, exclusions: {exclusions_list}", category="coherence_tab")
        
    except Exception as e:
        log_message("ERREUR", f"Erreur sauvegarde options cohérence: {e}", category="coherence_tab")
        _update_coherence_status(main_interface, "❌ Erreur lors de la sauvegarde des options")

def _setup_auto_save_coherence_options(main_interface):
    """Configure la sauvegarde automatique des options de cohérence"""
    # Marquer immédiatement que l'initialisation est en cours
    main_interface._coherence_initialization_complete = False
    
    # Variables de cohérence avec leurs clés de configuration
    coherence_vars = [
        (main_interface.check_variables_var, 'coherence_check_variables'),
        (main_interface.check_tags_var, 'coherence_check_tags'),
        (main_interface.check_special_codes_var, 'coherence_check_special_codes'),
        (main_interface.check_untranslated_var, 'coherence_check_untranslated'),
        (main_interface.check_ellipsis_var, 'coherence_check_ellipsis'),
        (main_interface.check_escape_sequences_var, 'coherence_check_escape_sequences'),
        (main_interface.check_percentages_var, 'coherence_check_percentages'),
        (main_interface.check_quotations_var, 'coherence_check_quotations'),
        (main_interface.check_parentheses_var, 'coherence_check_parentheses'),
        (main_interface.check_syntax_var, 'coherence_check_syntax'),
        (main_interface.check_deepl_ellipsis_var, 'coherence_check_deepl_ellipsis'),
        (main_interface.check_isolated_percent_var, 'coherence_check_isolated_percent'),
        (main_interface.check_french_quotes_var, 'coherence_check_french_quotes'),
        (main_interface.check_line_structure_var, 'coherence_check_line_structure')
    ]
    
    # Configurer la sauvegarde automatique pour chaque variable
    for var, config_key in coherence_vars:
        var.trace('w', lambda *args, key=config_key, v=var: _auto_save_coherence_option(main_interface, key, v.get()))
    
    # Configurer la sauvegarde automatique pour les exclusions de fichiers
    if hasattr(main_interface, 'coherence_excluded_files_var'):
        main_interface.coherence_excluded_files_var.trace('w', lambda *args: _auto_save_file_exclusions(main_interface))
    
    # Délai pour permettre l'initialisation complète avant d'activer les notifications
    def enable_notifications():
        main_interface._coherence_initialization_complete = True
    
    # Programmer l'activation des notifications après un court délai
    main_interface.window.after(1000, enable_notifications)  # 1 seconde de délai

def _auto_save_coherence_option(main_interface, config_key, value):
    """Sauvegarde automatique d'une option de cohérence"""
    try:
        # Sauvegarder dans la config
        config_manager.set(config_key, value)
        
        # Vérifier si c'est une vraie modification utilisateur (pas un chargement initial)
        if not hasattr(main_interface, '_coherence_initialization_complete') or not main_interface._coherence_initialization_complete:
            return
        
        # Afficher une notification toast spécifique selon l'état avec traduction française
        option_translations = {
            'coherence_check_variables': 'Variables [] incohérentes',
            'coherence_check_tags': 'Balises {} incohérentes',
            'coherence_check_special_codes': 'Codes spéciaux',
            'coherence_check_untranslated': 'Lignes non traduites',
            'coherence_check_ellipsis': 'Ellipses (-- → ...)',
            'coherence_check_escape_sequences': 'Séquences d\'échappement',
            'coherence_check_percentages': 'Variables de formatage',
            'coherence_check_quotations': 'Guillemets et échappements',
            'coherence_check_parentheses': 'Parenthèses et crochets',
            'coherence_check_syntax': 'Syntaxe Ren\'Py',
            'coherence_check_deepl_ellipsis': 'Ellipses DeepL',
            'coherence_check_isolated_percent': 'Pourcentages isolés',
            'coherence_check_french_quotes': 'Guillemets français',
            'coherence_check_line_structure': 'Structure des lignes'
        }
        
        option_name = option_translations.get(config_key, config_key.replace('coherence_check_', '').replace('_', ' ').title())
        if value:
            _show_toast(main_interface, f"✅ {option_name} activé", "success")
        else:
            _show_toast(main_interface, f"⚠️ {option_name} désactivé", "warning")
            
    except Exception as e:
        log_message("ERREUR", f"Erreur sauvegarde automatique {config_key}: {e}", category="coherence_tab")

def _auto_save_file_exclusions(main_interface):
    """Sauvegarde automatique des exclusions de fichiers"""
    try:
        # Sauvegarder les exclusions de fichiers
        if hasattr(main_interface, 'coherence_excluded_files_var'):
            config_manager.set('coherence_excluded_files', main_interface.coherence_excluded_files_var.get())
            
            # Appliquer les exclusions au sélecteur de projet
            if hasattr(main_interface, 'coherence_project_selector') and main_interface.coherence_project_selector:
                exclusions_str = main_interface.coherence_excluded_files_var.get()
                main_interface.coherence_project_selector.set_exclusions(exclusions_str)
        
        # Vérifier si c'est une vraie modification utilisateur
        if not hasattr(main_interface, '_coherence_initialization_complete') or not main_interface._coherence_initialization_complete:
            return
        
        # Notification toast pour les exclusions
        _show_toast(main_interface, "📝 Exclusions de fichiers mises à jour", "info")
    except Exception as e:
        log_message("ERREUR", f"Erreur sauvegarde automatique exclusions: {e}", category="coherence_tab")

def _show_toast(main_interface, message, toast_type="info"):
    """Affiche une notification toast"""
    try:
        # Vérifier si le contrôleur et la fenêtre principale existent
        if (hasattr(main_interface, 'parent_window') and main_interface.parent_window and
            hasattr(main_interface.parent_window, 'app_controller')):
            
            app_controller = main_interface.parent_window.app_controller
            if hasattr(app_controller, 'main_window'):
                main_window = app_controller.main_window
                
                # Accéder au gestionnaire de notifications via la méthode publique
                notifications = main_window.get_component('notifications')
                
                if notifications:
                    # Logique pour nettoyer les toasts précédents lors du changement de thème
                    if "Thème changé" in message or "Mode sombre" in message or "Mode clair" in message:
                        notifications.clear_all_toasts()

                # Mapper notre 'toast_type' simple aux kwargs attendus par show_notification
                kwargs = {'toast_type': 'info'} # Par défaut
                if toast_type == 'success' or 'activé' in message or '✅' in message:
                    kwargs['toast_type'] = 'success'
                elif toast_type == 'warning' or 'désactivé' in message:
                    kwargs['toast_type'] = 'warning'
                elif toast_type == 'error' or '❌' in message:
                    kwargs['toast_type'] = 'error'

                # Utiliser la méthode publique de la fenêtre principale pour afficher la notification
                return main_window.show_notification(message, 'TOAST', **kwargs)
        
        # Fallback si la fenêtre n'est pas accessible
        log_message("INFO", f"Toast Maintenance (Fallback): {message}", category="coherence_tab")
        return True
            
    except Exception as e:
        log_message("ERREUR", f"Erreur _show_toast: {e}", category="coherence_tab")
        return False

# ===== GESTIONNAIRE D'EXCLUSIONS DE LIGNES =====

def _open_exclusions_manager(main_interface):
    """Ouvre la fenêtre de gestion des exclusions de lignes"""
    try:
        from ui.dialogs.exclusions_manager_dialog import ExclusionsManagerDialog
        
        # Créer et afficher la fenêtre
        dialog = ExclusionsManagerDialog(main_interface.window)
        
        log_message("INFO", "Fenêtre de gestion des exclusions ouverte", category="coherence_tab")
        
    except Exception as e:
        log_message("ERREUR", f"Erreur ouverture gestionnaire exclusions: {e}", category="coherence_tab")
        show_translated_messagebox(
            'error',
            'Erreur',
            f'Impossible d\'ouvrir le gestionnaire d\'exclusions:\n\n{e}',
            parent=main_interface.window
        )