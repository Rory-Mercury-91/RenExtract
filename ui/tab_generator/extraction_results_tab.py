# ui/tab_generator/extraction_results_tab.py
# Onglet de résultats extraction textes oubliés - Générateur de Traductions Ren'Py

"""
Onglet de résultats pour l'extraction des textes oubliés par le SDK
- Affichage des statistiques d'analyse
- Visualisation des textes par catégorie (3 colonnes)
- Sélection interactive des textes à extraire
- Génération du fichier .rpy final
"""

import tkinter as tk
from tkinter import ttk, filedialog
import os
from ui.themes import theme_manager
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import show_translated_messagebox
from core.models.files.file_manager import FileOpener
from core.services.translation.text_extraction_results_business import TextExtractionResultsBusiness

def create_extraction_results_tab(parent, main_interface):
    """Crée l'onglet de résultats d'extraction - parent = frame scrollable (ajout au notebook fait par l'interface)."""
    theme = theme_manager.get_theme()
    
    tab_frame = tk.Frame(parent, bg=theme["bg"])
    tab_frame.pack(fill='both', expand=True)
    
    # Container principal avec espacement optimisé
    main_container = tk.Frame(tab_frame, bg=theme["bg"])
    main_container.pack(fill='both', expand=True, padx=20, pady=15)
    
    # Description
    desc_label = tk.Label(
        main_container,
        text="Résultats de l'analyse des textes oubliés par le SDK Ren'Py.\n" +
             "Sélectionnez les textes à extraire et générez le fichier .rpy final.",
        font=('Segoe UI', 10, 'bold'),
        justify='left',
        bg=theme["bg"],
        fg=theme["accent"]
    )
    desc_label.pack(anchor='w', pady=(0, 20))
    
    # ===== SECTION STATISTIQUES =====
    stats_frame = tk.Frame(main_container, bg=theme["bg"])
    stats_frame.pack(fill='x', pady=(0, 20))
    
    # Titre de la section statistiques
    stats_title = tk.Label(
        stats_frame,
        text="📈 Statistiques de l'analyse",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    stats_title.pack(anchor='w', pady=(0, 10))
    
    _create_statistics_section_2_columns(stats_frame, main_interface)
    
    # ===== SECTION RÉSULTATS =====
    results_frame = tk.Frame(main_container, bg=theme["bg"])
    results_frame.pack(fill='both', expand=True, pady=(0, 20))
    
    # Titre de la section résultats
    results_title = tk.Label(
        results_frame,
        text="🎯 Textes détectés par catégorie",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    results_title.pack(anchor='w', pady=(0, 10))
    
    _create_results_section(results_frame, main_interface)
    
    # ===== SECTION ACTIONS =====
    actions_frame = tk.Frame(main_container, bg=theme["bg"])
    actions_frame.pack(fill='x', pady=(10, 0))
    
    # Titre de la section actions
    actions_title = tk.Label(
        actions_frame,
        text="⚡ Actions sur la sélection",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    actions_title.pack(anchor='w', pady=(0, 10))
    
    _create_results_actions_section_horizontal(actions_frame, main_interface)

def _create_statistics_section_2_columns(parent, main_interface):
    """Crée la section des statistiques en 2 colonnes"""
    theme = theme_manager.get_theme()
    
    # Container pour 2 colonnes
    stats_container = tk.Frame(parent, bg=theme["bg"])
    stats_container.pack(fill='x', pady=(0, 10))
    
    # Colonne 1 (gauche)
    col1 = tk.Frame(stats_container, bg=theme["bg"])
    col1.pack(side='left', fill='x', expand=True, padx=(0, 10))
    
    # Colonne 2 (droite)
    col2 = tk.Frame(stats_container, bg=theme["bg"])
    col2.pack(side='right', fill='x', expand=True, padx=(10, 0))
    
    # Labels de statistiques en 2 colonnes
    main_interface.extraction_files_stat_label = tk.Label(
        col1,
        text="📊 Fichiers analysés: - ",
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        anchor='w'
    )
    main_interface.extraction_files_stat_label.pack(anchor='w', pady=2, fill='x')
    
    main_interface.extraction_existing_stat_label = tk.Label(
        col1,
        text="📊 Textes existants dans tl/: - ",
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        anchor='w'
    )
    main_interface.extraction_existing_stat_label.pack(anchor='w', pady=2, fill='x')
    
    main_interface.extraction_detected_stat_label = tk.Label(
        col2,
        text="🎯 Nouveaux textes détectés: - ",
        font=('Segoe UI', 10, 'bold'),
        bg=theme["bg"],
        fg=theme["accent"],
        anchor='w'
    )
    main_interface.extraction_detected_stat_label.pack(anchor='w', pady=2, fill='x')
    
    main_interface.extraction_mode_stat_label = tk.Label(
        col2,
        text="🔧 Mode utilisé: - ",
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        anchor='w'
    )
    main_interface.extraction_mode_stat_label.pack(anchor='w', pady=2, fill='x')

def _create_results_section(parent, main_interface):
    """Crée la section des résultats avec hauteur fixe"""
    theme = theme_manager.get_theme()
    
    # Frame avec hauteur fixe
    scroll_container = tk.Frame(parent, bg=theme["bg"])
    scroll_container.pack(fill='both', expand=True, pady=(0, 10))
    
    scroll_container.configure(height=200)
    scroll_container.pack_propagate(False)  # Empêche le redimensionnement automatique
    
    # Canvas SANS scrollbar globale
    main_interface.extraction_results_canvas = tk.Canvas(scroll_container, bg=theme["bg"], highlightthickness=0)
    main_interface.extraction_results_scrollable_frame = tk.Frame(main_interface.extraction_results_canvas, bg=theme["bg"])
    
    main_interface.extraction_results_scrollable_frame.bind(
        "<Configure>",
        lambda e: main_interface.extraction_results_canvas.configure(scrollregion=main_interface.extraction_results_canvas.bbox("all"))
    )
    
    main_interface.extraction_results_canvas.create_window((0, 0), window=main_interface.extraction_results_scrollable_frame, anchor="nw")
    
    # Canvas prend tout l'espace (pas de scrollbar à droite)
    main_interface.extraction_results_canvas.pack(fill="both", expand=True)
    
    # Message initial
    main_interface.extraction_no_results_label = tk.Label(
        main_interface.extraction_results_scrollable_frame,
        text="📋 Aucune analyse effectuée.\nUtilisez l'onglet Configuration pour lancer une analyse.",
        font=('Segoe UI', 11),
        bg=theme["bg"],
        fg=theme["fg"],
        justify='center'
    )
    main_interface.extraction_no_results_label.pack(expand=True, pady=50)

def _create_results_actions_section_horizontal(parent, main_interface):
    """Crée la section des actions en 3 boutons horizontaux"""
    theme = theme_manager.get_theme()
    
    # Frame pour les boutons horizontaux
    buttons_frame = tk.Frame(parent, bg=theme["bg"])
    buttons_frame.pack(fill='x', pady=(0, 10))
    
    select_all_btn = tk.Button(
        buttons_frame,
        text="✅ Tout sélectionner",
        command=lambda: _select_all_extraction_results(main_interface),
        bg=theme["button_primary_bg"],   # MODIFIÉ - Primaire
        fg="#000000",                    # MODIFIÉ - Texte noir uniforme
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2',
        width=18  # Largeur fixe pour tous les boutons
    )
    select_all_btn.pack(side='left', padx=(0, 5))

    select_none_btn = tk.Button(
        buttons_frame,
        text="❌ Tout désélectionner", 
        command=lambda: _select_none_extraction_results(main_interface),
        bg=theme["button_danger_bg"],    # MODIFIÉ - Négative/Danger
        fg="#000000",                    # MODIFIÉ - Texte noir uniforme
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2',
        width=18  # Largeur fixe pour tous les boutons
    )
    select_none_btn.pack(side='left', padx=(5, 5))

    main_interface.extraction_generate_btn = tk.Button(
        buttons_frame,
        text="📄 Générer .rpy",
        command=lambda: _generate_extraction_file(main_interface),
        bg=theme["button_utility_bg"],   # MODIFIÉ - Utilitaires
        fg="#000000",                    # MODIFIÉ - Texte noir uniforme
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        state='disabled',
        relief='flat',
        cursor='hand2',
        width=18  # Largeur fixe pour tous les boutons
    )
    main_interface.extraction_generate_btn.pack(side='left', padx=(5, 0))

def display_extraction_results(main_interface):
    """Affiche les résultats de l'analyse d'extraction - VERSION REFACTORISÉE"""
    try:
        if not hasattr(main_interface, 'extraction_analysis_results') or not main_interface.extraction_analysis_results:
            _extraction_display_error(main_interface, "Aucun résultat d'analyse disponible")
            return
        
        results = main_interface.extraction_analysis_results
        
        # NOUVEAU : Initialiser le module métier si nécessaire
        if not hasattr(main_interface, 'extraction_results_business'):
            main_interface.extraction_results_business = TextExtractionResultsBusiness()
        
        # NOUVEAU : Calculer les statistiques détaillées via le module métier
        detailed_stats = main_interface.extraction_results_business.calculate_detailed_statistics(
            results, 
            _get_project_context(main_interface)
        )
        
        # Le reste du code reste identique...
        stats = results.get('statistics', {})
        total_detected = stats.get('total_detected', 0)
        
        # Mettre à jour les statistiques
        main_interface.extraction_files_stat_label.config(text=f"📊 Fichiers analysés: {_count_analyzed_files(main_interface)}")
        main_interface.extraction_existing_stat_label.config(text=f"📊 Textes existants dans tl/: {_count_existing_translations(main_interface)}")
        main_interface.extraction_detected_stat_label.config(text=f"🎯 Nouveaux textes détectés: {total_detected}")
        
        metadata = results.get('metadata', {})
        mode_text = "Simple" if metadata.get('detection_mode') == "simple" else "Optimisé"
        main_interface.extraction_mode_stat_label.config(text=f"🔧 Mode utilisé: {mode_text}")
        
        # Effacer le contenu précédent
        for widget in main_interface.extraction_results_scrollable_frame.winfo_children():
            widget.destroy()
        
        if total_detected == 0:
            # Aucun résultat
            no_results = tk.Label(
                main_interface.extraction_results_scrollable_frame,
                text="✅ Aucun nouveau texte détecté !\n\nTous les textes traduisibles semblent déjà être présents dans le dossier tl.",
                font=('Segoe UI', 11),
                bg=theme_manager.get_theme()["frame_bg"],
                fg=theme_manager.get_theme()["fg"],
                justify='center'
            )
            no_results.pack(expand=True, pady=50)
            main_interface.extraction_generate_btn.config(state='disabled')
        else:
            # NOUVEAU : Préparer les sélections via le module métier
            main_interface.extraction_selections = main_interface.extraction_results_business.prepare_text_selections(results)
            
            # Afficher les résultats par catégorie
            _create_extraction_results_categories(main_interface, results)
            main_interface.extraction_generate_btn.config(state='normal')
        
        log_message("INFO", f"✅ Résultats d'extraction affichés - {total_detected} textes détectés", category="extraction_results")
        
    except Exception as e:
        log_message("ERREUR", f"Erreur affichage résultats extraction: {e}", category="extraction_results")
        _extraction_display_error(main_interface, f"Erreur lors de l'affichage des résultats: {e}")

def _get_project_context(main_interface):
    """Récupère le contexte du projet pour les statistiques détaillées"""
    try:
        context = {}
        if main_interface.current_project_path:
            game_folder = os.path.join(main_interface.current_project_path, "game")
            if os.path.exists(game_folder):
                import glob
                rpy_files = list(glob.glob(os.path.join(game_folder, "**/*.rpy"), recursive=True))
                # Exclure le dossier tl
                rpy_files = [f for f in rpy_files if '/tl/' not in f.replace('\\', '/')]
                context['game_rpy_count'] = len(rpy_files)
        return context
    except Exception:
        return {}

def _create_extraction_results_categories(main_interface, results):
    """Crée 3 sections fixes côte à côte avec scroll individuel - VERSION REFACTORISÉE"""
    theme = theme_manager.get_theme()
    
    # Réinitialiser les sélections
    main_interface.extraction_selections.clear()
    main_interface.extraction_buttons.clear()
    
    # Container principal pour les 3 sections qui remplissent toute la largeur
    main_container = tk.Frame(main_interface.extraction_results_scrollable_frame, bg=theme["bg"])
    main_container.pack(fill='both', expand=True, padx=5, pady=5)
    
    # NOUVEAU : Utiliser les résultats catégorisés du module métier
    categorized_results = results.get('categorized_results', {})
    
    if not categorized_results:
        # Fallback vers l'ancienne structure si pas de catégorisation
        auto_safe_texts = results.get('raw_results', {}).get('auto_safe', set())
        textbutton_texts = results.get('raw_results', {}).get('textbutton_check', set())
        text_check_texts = results.get('raw_results', {}).get('text_check', set())
    else:
        # Utiliser les nouvelles catégories
        auto_safe_texts = categorized_results.get('high_confidence', {}).get('texts', set())
        textbutton_texts = categorized_results.get('textbuttons', {}).get('texts', set())
        text_check_texts = categorized_results.get('text_elements', {}).get('texts', set())
    
    # === SECTION 1: AUTO-SAFE (à gauche) ===
    auto_safe_frame = tk.LabelFrame(
        main_container,
        text=f"🟢 Auto-safe ({len(auto_safe_texts)} textes)",
        font=('Segoe UI Emoji', 10, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    auto_safe_frame.pack(side='left', fill='both', expand=True, padx=(0, 3))
    
    _create_extraction_section_content(auto_safe_frame, auto_safe_texts, True, "auto_safe", main_interface)
    
    # === SECTION 2: TEXTBUTTONS (au centre) ===
    textbutton_frame = tk.LabelFrame(
        main_container,
        text=f"🟡 Textbuttons ({len(textbutton_texts)} textes)",
        font=('Segoe UI Emoji', 10, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    textbutton_frame.pack(side='left', fill='both', expand=True, padx=(3, 3))
    
    _create_extraction_section_content(textbutton_frame, textbutton_texts, False, "textbuttons", main_interface)
    
    # === SECTION 3: TEXT ELEMENTS (à droite) ===
    text_elements_frame = tk.LabelFrame(
        main_container,
        text=f"🟡 Text elements ({len(text_check_texts)} textes)",
        font=('Segoe UI Emoji', 10, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    text_elements_frame.pack(side='left', fill='both', expand=True, padx=(3, 0))
    
    _create_extraction_section_content(text_elements_frame, text_check_texts, False, "text_elements", main_interface)

def _create_extraction_section_content(parent_frame, texts, default_selected, section_id, main_interface):
    """Crée le contenu d'une section avec taille fixe, 2 colonnes, ET scroll + molette"""
    theme = theme_manager.get_theme()
    
    # Description selon la section
    descriptions = {
        "auto_safe": "Confiance 100% - Extraction automatique recommandée (Zone scrollable)",
        "textbuttons": "Boutons d'interface détectés - Vérification recommandée (Zone scrollable)", 
        "text_elements": "Éléments texte détectés - Vérification recommandée (Zone scrollable)"
    }
    
    # Description
    desc_label = tk.Label(
        parent_frame,
        text=descriptions.get(section_id, ""),
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        wraplength=250,
        justify='left'
    )
    desc_label.pack(anchor='w', padx=8, pady=(5, 3))
    
    # Bouton pour tout cocher/décocher cette section
    def toggle_section():
        section_texts = [t for t in texts if t in main_interface.extraction_selections]
        if section_texts:
            all_selected = all(main_interface.extraction_selections.get(t, False) for t in section_texts)
            new_state = not all_selected
        else:
            new_state = True
        
        for text in texts:
            if text in main_interface.extraction_selections:
                main_interface.extraction_selections[text] = new_state
                if text in main_interface.extraction_buttons:
                    icon = "☑️" if new_state else "☐"
                    main_interface.extraction_buttons[text].config(text=f"{icon} {text}")
    
    toggle_btn = tk.Button(
        parent_frame,
        text="☑️ Tout cocher/décocher",
        command=toggle_section,
        bg=theme["button_utility_bg"],   # MODIFIÉ - Utilitaires
        fg="#000000",                    # MODIFIÉ - Texte noir uniforme
        font=('Segoe UI', 9),
        pady=2,
        relief='flat',
        cursor='hand2'
    )
    toggle_btn.pack(anchor='w', padx=8, pady=(0, 5))
    
    # Zone scrollable pour cette section - TAILLE FIXE
    scroll_container = tk.Frame(parent_frame, bg=theme["bg"])
    scroll_container.pack(fill='both', expand=True, padx=5, pady=(0, 8))
    
    scroll_container.configure(height=120, width=340)
    scroll_container.pack_propagate(False)
    
    # Canvas à gauche (prend l'espace restant)
    canvas = tk.Canvas(scroll_container, bg=theme["bg"], highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    
    # Frame pour la scrollbar : pas de pack_propagate(False) pour que fill="y" donne toute la hauteur (barre visible jusqu'en bas)
    scrollbar_frame = tk.Frame(scroll_container, bg=theme["bg"], width=16)
    scrollbar_frame.pack(side="right", fill="y")
    
    scrollbar = ttk.Scrollbar(
        scrollbar_frame,
        orient="vertical",
        command=canvas.yview
    )
    scrollbar.pack(fill="both", expand=True, padx=1, pady=1)
    
    scrollable_frame = tk.Frame(canvas, bg=theme["bg"])
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Support molette sur TOUS les widgets de cette section (return "break" pour ne pas
    # laisser l'onglet scrollable parent capturer l'événement et empêcher le scroll interne)
    def on_mousewheel(event):
        delta = getattr(event, "delta", 0)
        if not delta:
            num = getattr(event, "num", None)
            delta = 120 if num == 4 else (-120 if num == 5 else 0)
        if delta:
            canvas.yview_scroll(int(-1 * (delta / 120)), "units")
        return "break"
    
    # Lier molette au canvas (Windows/Mac + Linux Button-4/5)
    canvas.bind("<MouseWheel>", on_mousewheel)
    canvas.bind("<Button-4>", on_mousewheel)
    canvas.bind("<Button-5>", on_mousewheel)
    
    # Fonction pour lier la molette récursivement à tous les enfants
    def bind_mousewheel_recursive(widget):
        widget.bind("<MouseWheel>", on_mousewheel, add="+")
        widget.bind("<Button-4>", on_mousewheel, add="+")
        widget.bind("<Button-5>", on_mousewheel, add="+")
        for child in widget.winfo_children():
            bind_mousewheel_recursive(child)
    
    # LIER LA MOLETTE AU FRAME SCROLLABLE ET TOUS SES ENFANTS
    bind_mousewheel_recursive(scrollable_frame)
    
    # Ajouter les textes en 2 COLONNES ou message si vide
    if not texts:
        no_text_label = tk.Label(
            scrollable_frame,
            text="Aucun texte\ndétecté",
            font=('Segoe UI', 10, 'italic'),
            bg=theme["bg"],
            fg='#666666',
            justify='center'
        )
        no_text_label.pack(expand=True, pady=20)
        # Lier molette au message vide aussi
        no_text_label.bind("<MouseWheel>", on_mousewheel, add="+")
    else:
        # Container pour 2 colonnes dans chaque section
        columns_frame = tk.Frame(scrollable_frame, bg=theme["bg"])
        columns_frame.pack(fill='x', padx=2, pady=2)
        
        # 2 colonnes par section
        col1 = tk.Frame(columns_frame, bg=theme["bg"])
        col1.pack(side='left', fill='both', expand=True, padx=(0, 2))
        
        col2 = tk.Frame(columns_frame, bg=theme["bg"])
        col2.pack(side='right', fill='both', expand=True, padx=(2, 0))
        
        columns = [col1, col2]
        
        # Distribuer les textes sur 2 colonnes
        for i, text in enumerate(sorted(texts)):
            column = columns[i % 2]
            
            # Initialiser la sélection
            main_interface.extraction_selections[text] = default_selected
            
            # Créer le bouton case à cocher
            icon = "☑️" if default_selected else "☐"
            
            btn = tk.Button(
                column,
                text=f"{icon} {text}",
                command=lambda t=text: _toggle_extraction_text_selection(main_interface, t),
                font=('Segoe UI', 9),  # Police plus petite pour 2 colonnes
                bg=theme["bg"],
                fg=theme["fg"],
                anchor='w',
                relief='flat',
                bd=1,
                padx=2,
                pady=1,
                wraplength=120  # Plus étroit pour 2 colonnes
            )
            btn.pack(fill='x', pady=1)
            
            # LIER LA MOLETTE À CHAQUE BOUTON
            btn.bind("<MouseWheel>", on_mousewheel, add="+")
            
            # Stocker la référence
            main_interface.extraction_buttons[text] = btn
        
        # LIER LA MOLETTE AUX FRAMES COLONNES
        columns_frame.bind("<MouseWheel>", on_mousewheel, add="+")
        col1.bind("<MouseWheel>", on_mousewheel, add="+")
        col2.bind("<MouseWheel>", on_mousewheel, add="+")
    
    # Forcer la mise à jour du scrollregion après création du contenu (évite contenu coupé)
    def _update_scroll_region():
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
    parent_frame.after(100, _update_scroll_region)
    parent_frame.after(300, _update_scroll_region)


def _toggle_extraction_text_selection(main_interface, text):
    """Bascule la sélection d'un texte d'extraction"""
    try:
        if text in main_interface.extraction_selections:
            main_interface.extraction_selections[text] = not main_interface.extraction_selections[text]
            icon = "☑️" if main_interface.extraction_selections[text] else "☐"
            
            if text in main_interface.extraction_buttons:
                main_interface.extraction_buttons[text].config(text=f"{icon} {text}")
                
            log_message("DEBUG", f"Toggle sélection extraction: '{text[:30]}...' -> {main_interface.extraction_selections[text]}", category="extraction_results")
    except Exception as e:
        log_message("ERREUR", f"Erreur toggle sélection extraction: {e}", category="extraction_results")

def _select_all_extraction_results(main_interface):
    """Sélectionne tous les textes d'extraction"""
    try:
        for text in main_interface.extraction_selections:
            main_interface.extraction_selections[text] = True
            if text in main_interface.extraction_buttons:
                main_interface.extraction_buttons[text].config(text=f"☑️ {text}")
        
        log_message("INFO", f"Tous les textes d'extraction sélectionnés ({len(main_interface.extraction_selections)})", category="extraction_results")
    except Exception as e:
        log_message("ERREUR", f"Erreur sélection totale extraction: {e}", category="extraction_results")

def _select_none_extraction_results(main_interface):
    """Désélectionne tous les textes d'extraction"""
    try:
        for text in main_interface.extraction_selections:
            main_interface.extraction_selections[text] = False
            if text in main_interface.extraction_buttons:
                main_interface.extraction_buttons[text].config(text=f"☐ {text}")
        
        log_message("INFO", "Tous les textes d'extraction désélectionnés", category="extraction_results")
    except Exception as e:
        log_message("ERREUR", f"Erreur désélection totale extraction: {e}", category="extraction_results")

def _generate_extraction_file(main_interface):
    """Génère le fichier .rpy d'extraction - VERSION AVEC RESPECT DU MODE NOTIFICATION"""
    try:
        # Collecter les textes sélectionnés
        selected_texts = {text for text, selected in main_interface.extraction_selections.items() if selected}
        
        if not selected_texts:
            main_interface._show_notification("Veuillez sélectionner au moins un texte à extraire.", "warning")
            return
        
        # Construction du chemin intelligent (code existant inchangé)
        suggested_folder = None
        suggested_filename = "textes_manquants.rpy"
        
        try:
            from ui.tab_generator.extraction_config_tab import get_selected_extraction_language_path, get_selected_extraction_language
            
            selected_language = get_selected_extraction_language(main_interface)
            tl_language_folder = get_selected_extraction_language_path(main_interface)
            
            if selected_language and tl_language_folder and os.path.exists(tl_language_folder):
                suggested_folder = tl_language_folder
                log_message("INFO", f"🎯 Dossier intelligent proposé: {suggested_folder}", category="extraction_results")
            else:
                if main_interface.current_project_path:
                    game_folder = os.path.join(main_interface.current_project_path, "game")
                    if os.path.exists(game_folder):
                        suggested_folder = game_folder
                        log_message("INFO", f"🎯 Fallback vers dossier game: {suggested_folder}", category="extraction_results")
        except Exception as e:
            log_message("DEBUG", f"Erreur construction chemin intelligent: {e}", category="extraction_results")
            suggested_folder = None
        
        # Dialogue de sauvegarde
        # IMPORTANT: disable the native "replace existing file" confirmation so our app
        # can handle existing files (propose fusion) itself. On Windows this prevents the
        # OS dialog from showing its own "replace" prompt.
        save_path = filedialog.asksaveasfilename(
            defaultextension=".rpy",
            filetypes=[("Fichiers Ren'Py", "*.rpy"), ("Tous les fichiers", "*.*")],
            initialfile=suggested_filename,
            initialdir=suggested_folder,
            title="💾 Sauvegarder le fichier d'extraction",
            parent=main_interface.window,
            confirmoverwrite=False
        )
        
        if not save_path:
            return
        
        # NOUVEAU : Utiliser le module métier pour la génération
        if not hasattr(main_interface, 'extraction_results_business'):
            main_interface.extraction_results_business = TextExtractionResultsBusiness()
        
        # Préparer les métadonnées
        project_name = os.path.basename(main_interface.current_project_path) if main_interface.current_project_path else "Projet inconnu"
        analyzed_language = get_selected_extraction_language(main_interface) if 'get_selected_extraction_language' in locals() else "Langue inconnue"
        
        metadata = main_interface.extraction_analysis_results.get('metadata', {})
        detection_mode = metadata.get('detection_mode', 'optimized')
        
        extraction_metadata = {
            'Projet': project_name,
            'Langue analysée': analyzed_language,
            'Mode de détection': detection_mode,
            'Nombre de textes': len(selected_texts)
        }
        
        # NOUVEAU : Générer via le module métier
        generation_result = main_interface.extraction_results_business.generate_extraction_file(
            selected_texts, 
            save_path, 
            extraction_metadata
        )
        
        if generation_result['success']:
            # MODIFIÉ : Respecter le mode de notification
            notification_mode = config_manager.get('notification_mode', 'status_only')
            
            if notification_mode == 'status_only':
                # Mode discret : juste mettre à jour le statut
                main_interface._update_status(f"✅ Fichier d'extraction généré ({len(selected_texts)} textes)")
            else:
                # Mode popup détaillé (comportement original)
                context_info = ""
                if suggested_folder and save_path.startswith(suggested_folder):
                    context_info = f"\n🎯 Sauvegardé dans le dossier de langue analysé !"
                
                main_interface._show_notification(
                    f'Fichier d\'extraction généré avec succès !{context_info}\n\n'
                    f'📄 Fichier: {os.path.basename(save_path)}\n'
                    f'📊 Nombre de textes: {len(selected_texts)}\n'
                    f'🎮 Projet: {project_name}\n'
                    f'🌐 Langue: {analyzed_language}\n'
                    f'📂 Emplacement: {os.path.dirname(save_path)}',
                    "success"
                )
            
            # Auto-ouverture si configurée (commun aux deux modes)
            try:
                if config_manager.get('auto_open_folders', True):
                    FileOpener.open_files([save_path], True)
                    log_message("INFO", "Fichier d'extraction ouvert automatiquement", category="extraction_results")
            except Exception as e:
                log_message("ATTENTION", f"Erreur auto-ouverture extraction: {e}", category="extraction_results")
            
            log_message("INFO", f"Fichier d'extraction généré: {save_path} ({len(selected_texts)} textes)", category="extraction_results")
            log_message("INFO", f"Contexte: Projet={project_name}, Langue={analyzed_language}", category="extraction_results")
        else:
            # NOUVEAU : Afficher les erreurs du module métier (toujours affiché même en mode discret)
            error_messages = "\n".join(generation_result.get('errors', ['Erreur inconnue']))
            main_interface._show_notification(f"Erreur lors de la génération du fichier:\n\n{error_messages}", "error")
        
    except Exception as e:
        log_message("ERREUR", f"Erreur génération fichier extraction: {e}", category="extraction_results")
        main_interface._show_notification(f"Erreur lors de la génération du fichier:\n\n{e}", "error")

def _extraction_display_error(main_interface, error_message):
    """Gère les erreurs d'affichage des résultats d'extraction"""
    log_message("ERREUR", f"Erreur affichage résultats extraction: {error_message}", category="extraction_results")
    
    # Effacer le contenu et afficher l'erreur
    for widget in main_interface.extraction_results_scrollable_frame.winfo_children():
        widget.destroy()
    
    theme = theme_manager.get_theme()
    error_label = tk.Label(
        main_interface.extraction_results_scrollable_frame,
        text=f"❌ Erreur d'affichage\n\n{error_message}",
        font=('Segoe UI', 11),
        bg=theme["bg"],
        fg='#ff8379',
        justify='center'
    )
    error_label.pack(expand=True, pady=50)
    
    # Désactiver le bouton de génération
    main_interface.extraction_generate_btn.config(state='disabled')

def _count_analyzed_files(main_interface):
    """Compte le nombre de fichiers analysés"""
    try:
        if not main_interface.current_project_path:
            return "❓"
        game_folder = os.path.join(main_interface.current_project_path, "game")
        if os.path.exists(game_folder):
            import glob
            return len(list(glob.glob(os.path.join(game_folder, "**/*.rpy"), recursive=True)))
    except:
        pass
    return "❓"

def _count_existing_translations(main_interface):
    """Compte le nombre de traductions existantes"""
    try:
        from ui.tab_generator.extraction_config_tab import get_selected_extraction_language_path
        tl_folder = get_selected_extraction_language_path(main_interface)
        if tl_folder and os.path.exists(tl_folder):
            import glob
            return len(list(glob.glob(os.path.join(tl_folder, "**/*.rpy"), recursive=True)))
    except:
        pass
    return "❓"
