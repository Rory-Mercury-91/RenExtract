# ui/tab_tools/cleaning_tab.py - REFACTORISÉ avec exclusions déplacées
# Onglet de nettoyage TL - Générateur de Traductions Ren'Py

"""
Onglet de nettoyage des traductions Ren'Py
- Interface de nettoyage avec sélection des langues
- Section exclusions de fichiers (déplacée depuis settings)
- Logique de nettoyage intelligent avec SDK intégré
- Génération de rapports détaillés
"""

import tkinter as tk
from tkinter import ttk
import os
import threading
from ui.themes import theme_manager
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message
from core.services.tools.cleaning_business import UnifiedCleaner, unified_clean_all_translations

def create_cleaning_tab(parent, main_interface):
    """Crée l'onglet de nettoyage TL - parent = frame scrollable (ajout au notebook fait par l'interface)."""
    theme = theme_manager.get_theme()
    
    tab_frame = tk.Frame(parent, bg=theme["bg"])
    tab_frame.pack(fill='both', expand=True)
    
    # Header : phrase et bouton d'aide sur la même ligne
    header_frame = tk.Frame(tab_frame, bg=theme["bg"])
    header_frame.pack(fill='x', padx=20, pady=(15, 10))
    help_btn = tk.Button(
        header_frame,
        text="À quoi ça sert ?",
        command=lambda: _show_cleaning_help(main_interface),
        bg=theme["button_secondary_bg"],
        fg="#000000",
        font=('Segoe UI', 10, 'bold'),
        width=15,
        height=1,
        relief='flat',
        cursor='hand2'
    )
    help_btn.pack(side='right')
    desc_label = tk.Label(
        header_frame,
        text="Nettoyage intelligent des traductions orphelines avec SDK Ren'Py intégré",
        font=('Segoe UI', 10, 'bold'),
        justify='center',
        bg=theme["bg"],
        fg=theme["accent"]
    )
    desc_label.pack(side='left', fill='x', expand=True, anchor='center')
    
    # Container principal avec espacement optimisé
    main_container = tk.Frame(tab_frame, bg=theme["bg"])
    main_container.pack(fill='both', expand=True, padx=20, pady=(0, 15))
    
    # === SECTION 1: SÉLECTION DES LANGUES ===
    languages_frame = tk.Frame(main_container, bg=theme["bg"])
    languages_frame.pack(fill='x', pady=(0, 20))
    
    # Titre des langues
    lang_title = tk.Label(
        languages_frame,
        text="🌍 Langues à nettoyer",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["accent"]
    )
    lang_title.pack(anchor='w', pady=(0, 10))
    
    # Zone scrollable pour les langues
    scroll_frame = tk.Frame(languages_frame, bg=theme["bg"])
    scroll_frame.pack(fill='x', pady=(0, 10))
    
    # Zone fixe pour les langues (sans scroll)
    lang_checkboxes_frame = tk.Frame(scroll_frame, bg=theme["bg"], height=200)
    lang_checkboxes_frame.pack(fill='x', pady=5)
    lang_checkboxes_frame.pack_propagate(False)  # Fixe la hauteur
    
    # Stocker la référence dans main_interface
    main_interface.lang_checkboxes_frame = lang_checkboxes_frame
    
    # Boutons de contrôle des langues
    buttons_controls_frame = tk.Frame(languages_frame, bg=theme["bg"])
    buttons_controls_frame.pack(fill='x', pady=(0, 10))

    # Frame horizontal pour les boutons
    all_buttons_frame = tk.Frame(buttons_controls_frame, bg=theme["bg"])
    all_buttons_frame.pack()

    select_all_btn = tk.Button(
        all_buttons_frame,
        text="✅ Tout sélectionner",
        command=lambda: select_all_languages(main_interface),
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
        command=lambda: select_no_languages(main_interface),
        bg=theme["button_danger_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    select_none_btn.pack(side='left')
    
    # === SECTION 2: EXCLUSIONS DE FICHIERS ===
    exclusions_frame = tk.Frame(main_container, bg=theme["bg"])
    exclusions_frame.pack(fill='x', pady=(0, 20))
    
    # Titre des exclusions
    exclusions_title = tk.Label(
        exclusions_frame,
        text="🚫 Fichiers à exclure du nettoyage",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["accent"]
    )
    exclusions_title.pack(anchor='w', pady=(0, 10))
    
    # Frame pour input + boutons
    exclusions_input_frame = tk.Frame(exclusions_frame, bg=theme["bg"])
    exclusions_input_frame.pack(fill='x', pady=(0, 10))
    
    # Entry pour les exclusions
    exclusions_entry = tk.Entry(
        exclusions_input_frame,
        textvariable=main_interface.cleanup_excluded_files_var,
        font=('Segoe UI', 10),
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        insertbackground=theme["entry_fg"],
        relief='solid',
        borderwidth=1
    )
    exclusions_entry.pack(side='left', fill='x', expand=True, pady=2, ipady=4)
    exclusions_entry.bind('<KeyRelease>', lambda e: _on_cleanup_exclusion_changed(main_interface))
    

    exclusions_reset_btn = tk.Button(
        exclusions_input_frame,
        text="Par défaut",
        command=lambda: _reset_cleanup_exclusions(main_interface),
        bg=theme["button_tertiary_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    exclusions_reset_btn.pack(side='right', padx=(5, 0))
    
    # Note d'exemple
    exclusions_note = tk.Label(
        exclusions_frame,
        text="💡 Exemple: common.rpy, menu.rpy, mon_fichier.rpy",
        font=('Segoe UI', 8, 'italic'),
        bg=theme["bg"],
        fg='#666666'
    )
    exclusions_note.pack(anchor='w', pady=(5, 0))
    
    # Bouton d'action principal
    clean_btn = tk.Button(
        exclusions_frame,
        text="🧹 Démarrer le nettoyage",
        command=lambda: start_cleaning(main_interface),
        bg=theme["button_primary_bg"],
        fg="#000000",
        font=('Segoe UI', 10, 'bold'),
        pady=8,
        padx=20,
        relief='flat',
        cursor='hand2'
    )
    clean_btn.pack(anchor='e', pady=(20, 0))

    main_interface.operation_buttons.append(clean_btn)
    # --- AUTO-SCAN LANGUES (création + re-sélection de l'onglet) ---
    def _auto_scan_cleaning_if_ready(*_):
        # Scanner si on a un projet (même si des langues sont déjà listées)
        if getattr(main_interface, "current_project_path", ""):
            log_message("DEBUG", f"Auto-scan déclenché pour projet: {main_interface.current_project_path}", category="renpy_generator_clean_tl")
            scan_available_languages(main_interface)

    # 1) au moment de la création (si un projet est déjà restauré)
    _auto_scan_cleaning_if_ready()

    # 2) quand l'onglet devient actif (onglet = wrapper scrollable, tab_frame est dedans)
    def _on_tab_changed_cleaning(event=None):
        nb = getattr(main_interface, "notebook", None)
        if not nb:
            return
        current = nb.nametowidget(nb.select())
        w = tab_frame
        while w:
            if w == current:
                _auto_scan_cleaning_if_ready()
                break
            w = getattr(w, "master", None)

    if getattr(main_interface, "notebook", None):
        main_interface.notebook.bind("<<NotebookTabChanged>>", _on_tab_changed_cleaning)

    # 3) Expose un hook pour que la fenêtre principale puisse forcer un resync
    main_interface.cleaning_resync = _auto_scan_cleaning_if_ready
    
    # 4) Hook pour déclencher le scan quand le projet change
    def _on_project_changed_cleaning():
        if getattr(main_interface, "current_project_path", ""):
            log_message("DEBUG", f"Projet changé, scan déclenché: {main_interface.current_project_path}", category="renpy_generator_clean_tl")
            scan_available_languages(main_interface)
    
    # Stocker la fonction pour qu'elle puisse être appelée depuis l'extérieur
    main_interface.cleaning_project_changed = _on_project_changed_cleaning

# ===== FONCTIONS POUR LES EXCLUSIONS =====

def _on_cleanup_exclusion_changed(main_interface):
    """Appelé quand la liste d'exclusion du nettoyage change"""
    try:
        exclusions_text = main_interface.cleanup_excluded_files_var.get()
        config_manager.set('cleanup_excluded_files', exclusions_text)
        config_manager.save_config()  # ✅ CORRIGÉ : Sauvegarder immédiatement
        log_message("DEBUG", "Liste d'exclusions nettoyage mise à jour", category="renpy_generator_clean_tl")
    except Exception as e:
        log_message("ERREUR", f"Erreur sauvegarde exclusions nettoyage: {e}", category="renpy_generator_clean_tl")

def _reset_cleanup_exclusions(main_interface):
    """Remet les exclusions de nettoyage par défaut"""
    try:
        default_exclusions = "common.rpy"
        main_interface.cleanup_excluded_files_var.set(default_exclusions)
        config_manager.set('cleanup_excluded_files', default_exclusions)
        log_message("INFO", "Exclusions nettoyage remises par défaut", category="renpy_generator_clean_tl")
    except Exception as e:
        log_message("ERREUR", f"Erreur reset exclusions: {e}", category="renpy_generator_clean_tl")

def _show_cleaning_help(main_interface):
    """Affiche l'aide complète pour l'onglet de nettoyage"""
    from infrastructure.helpers.unified_functions import show_custom_messagebox
    from ui.themes import theme_manager
    
    theme = theme_manager.get_theme()
    
    # Message avec couleurs et styles
    help_message = [
        ("🧹 ", "bold_green"),
        ("Nettoyage Intelligent des Traductions", "bold"),
        ("\n\n", "normal"),
        ("Cet outil nettoie automatiquement les traductions orphelines dans vos projets Ren'Py.", "normal"),
        ("\n\n", "normal"),
        ("📋 ", "bold_blue"),
        ("Fonctionnalités principales :", "bold"),
        ("\n", "normal"),
        ("• ", "green"),
        ("SDK Ren'Py intégré", "bold_green"),
        (" (téléchargement automatique si nécessaire)", "normal"),
        ("\n", "normal"),
        ("• ", "green"),
        ("Suppression des lignes orphelines", "bold_green"),
        (" détectées par lint", "normal"),
        ("\n", "normal"),
        ("• ", "green"),
        ("Nettoyage des correspondances", "bold_green"),
        (" de chaînes obsolètes", "normal"),
        ("\n", "normal"),
        ("• ", "green"),
        ("Sauvegardes automatiques", "bold_green"),
        (" avant modification", "normal"),
        ("\n\n", "normal"),
        ("🌍 ", "bold_blue"),
        ("Sélection des Langues :", "bold"),
        ("\n", "normal"),
        ("• ", "blue"),
        ("Choisissez les langues", "bold_blue"),
        (" à nettoyer dans la liste", "normal"),
        ("\n", "normal"),
        ("• ", "blue"),
        ("Boutons de contrôle rapide", "bold_blue"),
        (" : \"Tout sélectionner\" / \"Tout désélectionner\"", "normal"),
        ("\n", "normal"),
        ("• ", "blue"),
        ("Affichage automatique", "bold_blue"),
        (" des langues avec fichiers .rpy", "normal"),
        ("\n", "normal"),
        ("• ", "blue"),
        ("Compteur de fichiers", "bold_blue"),
        (" par langue", "normal"),
        ("\n\n", "normal"),
        ("🚫 ", "bold_yellow"),
        ("Exclusions de Fichiers :", "bold"),
        ("\n", "normal"),
        ("• ", "yellow"),
        ("Protection des fichiers", "bold_yellow"),
        (" modifiés manuellement", "normal"),
        ("\n", "normal"),
        ("• ", "yellow"),
        ("Format :", "bold_yellow"),
        (" nom_fichier.rpy, autre_fichier.rpy", "normal"),
        ("\n", "normal"),
        ("• ", "yellow"),
        ("Exemples :", "bold_yellow"),
        (" common.rpy, menu.rpy, mon_fichier.rpy", "normal"),
        ("\n\n", "normal"),
        ("🎯 ", "bold"),
        ("Guide d'utilisation :", "bold"),
        ("\n", "normal"),
        ("1. ", "bold"),
        ("Sélectionnez un projet Ren'Py", "bold"),
        ("\n", "normal"),
        ("2. ", "bold"),
        ("Choisissez les langues à nettoyer", "bold"),
        ("\n", "normal"),
        ("3. ", "bold"),
        ("Configurez les exclusions si nécessaire", "bold"),
        ("\n", "normal"),
        ("4. ", "bold"),
        ("Cliquez sur \"Démarrer le nettoyage\"", "bold"),
        ("\n\n", "normal"),
        ("📊 ", "bold_blue"),
        ("Résultats et Rapports :", "bold"),
        ("\n", "normal"),
        ("• ", "blue"),
        ("Rapport détaillé", "bold_blue"),
        (" généré automatiquement", "normal"),
        ("\n", "normal"),
        ("• ", "blue"),
        ("Statistiques des blocs", "bold_blue"),
        (" orphelins supprimés", "normal"),
        ("\n", "normal"),
        ("• ", "blue"),
        ("Sauvegardes créées", "bold_blue"),
        (" avant modification", "normal"),
        ("\n", "normal"),
        ("• ", "blue"),
        ("Ouverture automatique", "bold_blue"),
        (" du dossier de résultats", "normal")
    ]
    
    show_custom_messagebox(
        'info',
        '🧹 Aide - Nettoyage Intelligent',
        help_message,
        theme,
        parent=main_interface.window
    )

# ===== FONCTIONS DE NOTIFICATIONS TOAST =====

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
                kwargs = {}
                if toast_type == "success":
                    kwargs['toast_type'] = 'success'
                elif toast_type == "warning":
                    kwargs['toast_type'] = 'warning'
                elif toast_type == "error":
                    kwargs['toast_type'] = 'error'
                else:
                    kwargs['toast_type'] = 'info'

                # Utiliser la méthode publique show_notification
                main_window.show_notification(message, **kwargs)
                
        else:
            # Fallback vers la méthode _show_notification si disponible
            if hasattr(main_interface, '_show_notification'):
                main_interface._show_notification(message, toast_type)
            else:
                log_message("ATTENTION", f"Impossible d'afficher le toast: {message}", category="renpy_generator_clean_tl")
                
    except Exception as e:
        log_message("ERREUR", f"Erreur _show_toast: {e}", category="renpy_generator_clean_tl")

def _on_language_selection_changed(main_interface, language, is_selected):
    """Gère les notifications toast lors du changement de sélection de langue"""
    try:
        # Éviter les notifications pendant l'initialisation
        if not hasattr(main_interface, '_cleaning_initialization_complete') or not main_interface._cleaning_initialization_complete:
            return
        
        # Traductions des noms de langues
        language_translations = {
            'english': 'Anglais',
            'french': 'Français', 
            'spanish': 'Espagnol',
            'german': 'Allemand',
            'italian': 'Italien',
            'portuguese': 'Portugais',
            'russian': 'Russe',
            'japanese': 'Japonais',
            'chinese': 'Chinois',
            'korean': 'Coréen',
            'arabic': 'Arabe',
            'dutch': 'Néerlandais',
            'polish': 'Polonais',
            'swedish': 'Suédois',
            'norwegian': 'Norvégien',
            'danish': 'Danois',
            'finnish': 'Finnois',
            'turkish': 'Turc',
            'greek': 'Grec',
            'hebrew': 'Hébreu'
        }
        
        language_name = language_translations.get(language.lower(), language.title())
        
        if is_selected:
            _show_toast(main_interface, f"✅ {language_name} sélectionné pour le nettoyage", "success")
        else:
            _show_toast(main_interface, f"⚠️ {language_name} désélectionné du nettoyage", "warning")
            
    except Exception as e:
        log_message("ERREUR", f"Erreur notification langue {language}: {e}", category="renpy_generator_clean_tl")

# ===== FONCTIONS EXISTANTES (inchangées) =====

def scan_available_languages(main_interface):
    """Scanne les langues disponibles dans le projet"""
    try:
        if not main_interface.current_project_path:
            _show_toast(main_interface, "⚠️ Veuillez sélectionner un projet d'abord", "warning")
            return
        
        # Vérifier le dossier tl
        tl_folder = os.path.join(main_interface.current_project_path, "game", "tl")
        if not os.path.exists(tl_folder):
            _show_toast(main_interface, "⚠️ Aucun dossier tl/ trouvé dans le projet", "warning")
            return
        
        # Scanner les dossiers de langue
        languages = []
        for item in os.listdir(tl_folder):
            item_path = os.path.join(tl_folder, item)
            if os.path.isdir(item_path) and item.lower() != 'none':
                # Vérifier qu'il contient des fichiers .rpy (recherche récursive)
                has_rpy = False
                for root, dirs, files in os.walk(item_path):
                    if any(f.endswith('.rpy') for f in files):
                        has_rpy = True
                        break
                if has_rpy:
                    languages.append(item)
        
        if not languages:
            main_interface._update_status("⚠️ Aucune langue avec fichiers trouvée");
            return
        
        main_interface.available_languages = sorted(languages)
        create_language_checkboxes(main_interface)
        
        
    except Exception as e:
        _show_toast(main_interface, f"❌ Erreur lors du scan : {e}", "error")
        log_message("ERREUR", f"Erreur scan_available_languages : {e}", category="renpy_generator_clean_tl")

def create_language_checkboxes(main_interface):
    """Crée les checkboxes améliorés avec drapeaux et statistiques"""
    try:
        theme = theme_manager.get_theme()
        
        # Marquer que l'initialisation est en cours pour éviter les notifications
        main_interface._cleaning_initialization_complete = False
        
        # Nettoyer les anciens checkboxes
        for widget in main_interface.lang_checkboxes_frame.winfo_children():
            widget.destroy()
        
        main_interface.language_vars.clear()
        
        # Créer 3 colonnes pour optimiser l'espace
        languages_container = tk.Frame(main_interface.lang_checkboxes_frame, bg=theme["bg"])
        languages_container.pack(fill='x', padx=5, pady=5)
        
        # Créer 3 frames pour les colonnes
        col1_frame = tk.Frame(languages_container, bg=theme["bg"])
        col1_frame.pack(side='left', fill='both', expand=True, padx=2)
        
        col2_frame = tk.Frame(languages_container, bg=theme["bg"])
        col2_frame.pack(side='left', fill='both', expand=True, padx=2)
        
        col3_frame = tk.Frame(languages_container, bg=theme["bg"])
        col3_frame.pack(side='left', fill='both', expand=True, padx=2)
        
        # Distribuer les langues dans les 3 colonnes
        columns = [col1_frame, col2_frame, col3_frame]
        
        # Fonction pour obtenir l'icône d'une langue
        def get_language_icon(lang):
            icons = {
                'english': '🌐', 'french': '🗣️', 'spanish': '🗣️', 'german': '🗣️',
                'italian': '🗣️', 'portuguese': '🗣️', 'russian': '🗣️', 'japanese': '🗣️',
                'chinese': '🗣️', 'korean': '🗣️', 'arabic': '🗣️', 'dutch': '🗣️',
                'polish': '🗣️', 'swedish': '🗣️', 'norwegian': '🗣️', 'danish': '🗣️',
                'finnish': '🗣️', 'turkish': '🗣️', 'greek': '🗣️', 'hebrew': '🗣️'
            }
            return icons.get(lang.lower(), '🗣️')
        
        # Fonction pour compter les fichiers d'une langue (récursif)
        def count_language_files(lang):
            try:
                tl_folder = os.path.join(main_interface.current_project_path, "game", "tl", lang)
                if os.path.exists(tl_folder):
                    # Parcourir récursivement tous les sous-dossiers
                    count = 0
                    for root, dirs, files in os.walk(tl_folder):
                        count += sum(1 for f in files if f.endswith('.rpy'))
                    return count
                return 0
            except:
                return 0
        
        for i, language in enumerate(main_interface.available_languages):
            var = tk.BooleanVar(value=True)
            main_interface.language_vars[language] = var
            
            # Ajouter une trace pour les notifications toast
            var.trace('w', lambda *args, lang=language, v=var: _on_language_selection_changed(main_interface, lang, v.get()))
            
            # Déterminer la colonne (distribution équilibrée)
            col_index = i % 3
            parent_frame = columns[col_index]
            
            # Frame principal pour cette langue
            lang_frame = tk.Frame(parent_frame, bg=theme["bg"])
            lang_frame.pack(fill='x', pady=2)
            
            # Checkbox avec style amélioré
            checkbox = tk.Checkbutton(
                lang_frame,
                text="",  # Texte vide, on va ajouter les éléments séparément
                variable=var,
                font=('Segoe UI', 9),
                bg=theme["bg"],
                fg=theme["fg"],
                selectcolor=theme["bg"],
                activebackground=theme["bg"],
                activeforeground=theme["fg"],
                width=2,
                height=1
            )
            checkbox.pack(side='left', padx=(0, 8))
            
            # Icône de la langue
            icon_label = tk.Label(
                lang_frame,
                text=get_language_icon(language),
                font=('Segoe UI Emoji', 12),
                bg=theme["bg"],
                fg=theme["fg"]
            )
            icon_label.pack(side='left', padx=(0, 8))
            
            # Nom de la langue
            name_label = tk.Label(
                lang_frame,
                text=language.title(),
                font=('Segoe UI', 10, 'bold'),
                bg=theme["bg"],
                fg=theme["fg"]
            )
            name_label.pack(side='left', padx=(0, 8))
            
            # Compteur de fichiers
            file_count = count_language_files(language)
            count_label = tk.Label(
                lang_frame,
                text=f"({file_count} fichiers)",
                font=('Segoe UI', 8),
                bg=theme["bg"],
                fg='#666666'
            )
            count_label.pack(side='left')
            
            # Rendre toute la ligne cliquable (correction du problème de closure)
            for widget in [lang_frame, icon_label, name_label, count_label]:
                widget.bind('<Button-1>', lambda e, v=var: v.set(not v.get()))
            
        
        # Mise à jour de l'affichage
        main_interface.lang_checkboxes_frame.update_idletasks()
        # Relier la molette aux nouveaux widgets (zone scrollable de l'onglet)
        getattr(main_interface, 'refresh_tab_mousewheel', lambda: None)()
        
        # Activer les notifications après un court délai pour éviter les notifications pendant l'initialisation
        def enable_notifications():
            main_interface._cleaning_initialization_complete = True
        
        # Programmer l'activation des notifications après un court délai
        main_interface.window.after(1000, enable_notifications)  # 1 seconde de délai
        
    except Exception as e:
        log_message("ERREUR", f"Erreur create_language_checkboxes : {e}", category="renpy_generator_clean_tl")

def select_all_languages(main_interface):
    """Sélectionne toutes les langues"""
    try:
        # Temporairement désactiver les notifications pour éviter le spam
        main_interface._cleaning_initialization_complete = False
        
        for var in main_interface.language_vars.values():
            var.set(True)
        
        # Réactiver les notifications après un court délai
        def re_enable_notifications():
            main_interface._cleaning_initialization_complete = True
        
        main_interface.window.after(100, re_enable_notifications)
        
        # Notification globale
        _show_toast(main_interface, "✅ Toutes les langues sélectionnées", "success")
        
    except Exception as e:
        log_message("ERREUR", f"Erreur select_all_languages: {e}", category="renpy_generator_clean_tl")

def select_no_languages(main_interface):
    """Désélectionne toutes les langues"""
    try:
        # Temporairement désactiver les notifications pour éviter le spam
        main_interface._cleaning_initialization_complete = False
        
        for var in main_interface.language_vars.values():
            var.set(False)
        
        # Réactiver les notifications après un court délai
        def re_enable_notifications():
            main_interface._cleaning_initialization_complete = True
        
        main_interface.window.after(100, re_enable_notifications)
        
        # Notification globale
        _show_toast(main_interface, "⚠️ Toutes les langues désélectionnées", "warning")
        
    except Exception as e:
        log_message("ERREUR", f"Erreur select_no_languages: {e}", category="renpy_generator_clean_tl")

def start_cleaning(main_interface):
    """Démarre le nettoyage avec SDK intégré"""
    try:
        if not main_interface.current_project_path:
            _show_toast(main_interface, '⚠️ Veuillez sélectionner un projet Ren\'Py', "warning")
            return
        
        # Vérifier la présence de fichiers .rpa (archives non décompilées)
        rpa_files = []
        for root, dirs, files in os.walk(main_interface.current_project_path):
            for file in files:
                if file.endswith('.rpa'):
                    rpa_files.append(os.path.join(root, file))
            
            # Limiter à 5 fichiers pour le message
            if len(rpa_files) >= 5:
                break
        
        if rpa_files:
            # Formater la liste des fichiers pour l'affichage
            file_list = "\n".join([f"  • {os.path.relpath(f, main_interface.current_project_path)}" for f in rpa_files[:5]])
            if len(rpa_files) > 5:
                file_list += f"\n  ... et {len(rpa_files) - 5} autres fichiers"
            
            from infrastructure.helpers.unified_functions import show_custom_messagebox
            theme = theme_manager.get_theme()
            show_custom_messagebox(
                'error',
                'Archives .rpa détectées',
                [
                    ("❌ Impossible de nettoyer : archives .rpa détectées\n\n", "bold_red"),
                    ("Le projet contient encore des archives .rpa non décompilées.\n", "normal"),
                    ("Le nettoyage nécessite des fichiers sources décompilés (.rpy).\n\n", "normal"),
                    ("Archives détectées :\n", "bold_orange"),
                    (f"{file_list}\n\n", "normal"),
                    ("🔧 Solution :\n", "bold_green"),
                    ("1. Allez dans l'onglet ", "normal"),
                    ("Extraction & Compilation RPA / RPYC\n", "bold_blue"),
                    ("2. Extrayez les archives .rpa du projet\n", "normal"),
                    ("3. Revenez ici pour effectuer le nettoyage\n\n", "normal"),
                    ("💡 Note : ", "bold_blue"),
                    ("Le nettoyage compare les fichiers sources (.rpy) avec les traductions.", "normal"),
                ],
                theme,
                parent=main_interface.window
            )
            
            log_message("ATTENTION", 
                f"Nettoyage bloqué : {len(rpa_files)} archives .rpa détectées - Extraction requise", 
                category="renpy_generator_clean_tl")
            return
        
        # Vérifier SDK avec SDKManager
        log_message("INFO", "🧹 Début du processus de nettoyage...", category="renpy_generator_clean_tl")
        
        from core.tools.sdk_manager import get_sdk_manager
        sdk_manager = get_sdk_manager()
        sdk_path = sdk_manager.get_sdk_for_cleaning()
        
        if not sdk_path:
            _show_toast(main_interface, 
                "❌ Impossible d'obtenir un SDK Ren'Py - Vérifiez votre connexion ou configurez un SDK", 
                "error")
            return
        
        # Vérifier langues sélectionnées
        selected_languages = [lang for lang, var in main_interface.language_vars.items() if var.get()]
        if not selected_languages:
            _show_toast(main_interface, "⚠️ Veuillez sélectionner au moins une langue", "warning")
            return
        
        log_message("INFO", f"🌐 Langues à nettoyer: {', '.join(selected_languages)}", category="renpy_generator_clean_tl")
        
        main_interface._set_operation_running(True)
        
        # Lancer dans un thread
        run_cleanup_thread(main_interface, sdk_path, selected_languages)
        
    except Exception as e:
        _show_toast(main_interface, f"❌ Erreur : {e}", "error")
        main_interface._set_operation_running(False)
        log_message("ERREUR", f"Erreur start_cleaning: {e}", category="renpy_generator_clean_tl")


def run_cleanup_thread(main_interface, sdk_path, selected_languages):
    """Lance le nettoyage dans un thread avec SDK intégré"""
    
    def cleanup_worker():
        try:
            import time
            start_time = time.time()
            
            main_interface._update_status("🔍 Préparation du nettoyage...")
            main_interface._on_progress_update(10, "Initialisation...")
            
            # Construire les chemins
            game_folder_path = os.path.join(main_interface.current_project_path, "game")
            tl_folder_path = os.path.join(game_folder_path, "tl")
            
            main_interface._update_status("🛠️ Génération du lint.txt...")
            main_interface._on_progress_update(30, "Génération lint...")
            
            # Générer le lint avec le SDK (intégré ou configuré)
            from core.services.tools.cleaning_business import UnifiedCleaner
            cleaner = UnifiedCleaner()
            
            log_message("INFO", f"🛠️ Génération lint.txt avec SDK: {os.path.basename(sdk_path)}", category="renpy_generator_clean_tl")
            lint_file_path = cleaner.generate_lint_file(sdk_path, main_interface.current_project_path)
            
            # ✅ NOUVEAU : Vérifier si la génération lint a échoué à cause d'un traceback
            if lint_file_path is None:
                main_interface._update_status("❌ Nettoyage annulé - Erreur Ren'Py détectée (traceback.txt)")
                main_interface._on_progress_update(100, "Nettoyage annulé")
                log_message("ERREUR", "Nettoyage annulé - traceback.txt détecté lors de la génération lint", category="renpy_generator_clean_tl")
                
                # ✅ NOUVEAU : Notification toast d'alerte pour l'utilisateur
                _show_toast(main_interface, 
                    "❌ Erreur Ren'Py détectée - Consultez traceback.txt dans le dossier du jeu", 
                    "error")
                return
            
            main_interface._update_status("🧹 Nettoyage en cours...")
            main_interface._on_progress_update(60, "Suppression des orphelins...")
            
            # ✅ CORRIGÉ : Récupérer et sauvegarder les exclusions avant le nettoyage
            excluded_files = []
            if hasattr(main_interface, 'cleanup_excluded_files_var'):
                excluded_text = main_interface.cleanup_excluded_files_var.get().strip()
                if excluded_text:
                    excluded_files = [item.strip() for item in excluded_text.split(',') if item.strip()]
                    # Sauvegarder dans la configuration pour que _get_excluded_files() puisse les lire
                    from infrastructure.config.config import config_manager
                    config_manager.set('cleanup_excluded_files', excluded_text)
                    config_manager.save_config()
            
            log_message("INFO", f"Fichiers exclus du nettoyage: {excluded_files if excluded_files else 'Aucun'}", category="renpy_generator_clean_tl")
            
            # UTILISER la fonction existante avec exclusions
            from core.services.tools.cleaning_business import unified_clean_all_translations
            results = unified_clean_all_translations(
                lint_file_path, 
                game_folder_path, 
                tl_folder_path, 
                selected_languages
            )
            
            main_interface._on_progress_update(100, "Terminé")
            
            # Calculer le temps d'exécution
            end_time = time.time()
            execution_duration = end_time - start_time
            execution_time = format_execution_time(execution_duration)
            
            # Générer le rapport
            report_path = None
            try:
                report_path = create_unified_cleanup_report(results, main_interface.current_project_path, execution_time)
            except Exception as e:
                log_message("ERREUR", f"Erreur création rapport: {e}", category="renpy_generator_clean_tl")
         
            # Formater pour l'interface avec summary
            final_results = {
                'success': results['success'],
                'operation_type': 'cleaning',
                'languages_processed': results['total_languages_processed'],
                'files_processed': results['total_files_processed'],
                'orphan_blocks_removed': results['total_orphan_blocks_removed'],
                'errors': results.get('errors', []),
                'execution_time': execution_duration,
                'report_path': report_path,
                'summary': {
                    'cleaning': f"Nettoyage: {results['total_orphan_blocks_removed']} blocs orphelins supprimés dans {results['total_files_processed']} fichiers ({len(selected_languages)} langues)",
                    'execution_time': f"Temps d'exécution: {execution_time}",
                    'report_path': report_path,
                    'lint_cleanup': results['summary']['lint_cleanup'],
                    'string_cleanup': results['summary']['string_cleanup']
                }
            }                
            
            # Callback de fin
            main_interface._on_operation_complete(True, final_results)
            
        except Exception as e:
            error_msg = f"Erreur nettoyage : {str(e)}"
            log_message("ERREUR", error_msg, category="renpy_generator_clean_tl")
            main_interface._on_error(error_msg, e)
    
    # Lancer le thread
    thread = threading.Thread(target=cleanup_worker, daemon=True)
    thread.start()


def format_execution_time(duration):
    """Formate le temps d'exécution selon la durée"""
    if duration < 60:
        return f"{duration:.1f} secondes"
    elif duration < 3600:
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        return f"{minutes}m {seconds}s"
    else:
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        return f"{hours}h {minutes}m"

def create_unified_cleanup_report(results, game_folder_path, execution_time):
    """Crée un rapport de nettoyage unifié avec la nouvelle structure hiérarchique + version HTML."""
    try:
        # Si aucun bloc n'a été supprimé, on ne crée pas de rapport.
        if results.get('total_orphan_blocks_removed', 0) == 0:
            log_message("INFO", "Aucun bloc orphelin supprimé, les rapports de nettoyage n'ont pas été créés.", category="renpy_generator_clean_tl")
            return None
            
        from datetime import datetime
        import os
        
        try:
            from infrastructure.config.constants import FOLDERS, ensure_folders_exist
            from infrastructure.helpers.unified_functions import extract_game_name
            from infrastructure.config.config import config_manager
            from core.services.reporting.html_report_generator import create_html_cleanup_report
            
            ensure_folders_exist()
            
            game_name = os.path.basename(game_folder_path)
            warnings_root = FOLDERS["warnings"]
            
            # Construire la nouvelle arborescence avec le sous-dossier "nettoyage"
            report_type_folder = os.path.join(warnings_root, game_name, "nettoyage")
            os.makedirs(report_type_folder, exist_ok=True)
            
            # Génération du rapport HTML interactif
            html_report_path = None
            try:
                html_report_path = create_html_cleanup_report(results, game_folder_path, execution_time)
                if html_report_path:
                    log_message("INFO", f"Rapport HTML interactif créé : {os.path.basename(html_report_path)}", category="renpy_generator_clean_tl")
                else:
                    log_message("ATTENTION", "Échec de la génération du rapport HTML", category="renpy_generator_clean_tl")
                    
            except Exception as e:
                log_message("ERREUR", f"Erreur génération rapport HTML: {e}", category="renpy_generator_clean_tl")
            
            # Ouverture automatique du rapport HTML
            try:
                from infrastructure.config.config import config_manager
                if config_manager.is_auto_open_enabled() and html_report_path:
                    try:
                        import subprocess
                        import platform
                        
                        if platform.system() == "Windows":
                            os.startfile(html_report_path)
                        elif platform.system() == "Darwin":
                            subprocess.run(["open", html_report_path])
                        else:
                            subprocess.run(["xdg-open", html_report_path])
                        log_message("DEBUG", f"Rapport HTML auto-ouvert : {html_report_path}", category="renpy_generator_clean_tl")
                    except Exception as e:
                        log_message("ATTENTION", f"Impossible d'ouvrir automatiquement le rapport HTML : {str(e)}", category="renpy_generator_clean_tl")
            except ImportError:
                pass
            
            return html_report_path
            
        except ImportError:
            # Fallback si les modules utils ne sont pas disponibles
            game_name = os.path.basename(game_folder_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            txt_report_path = f"{game_name}_nettoyage_{timestamp}.txt"
            
            return txt_report_path
        
    except Exception as e:
        log_message("ERREUR", f"Impossible de créer le rapport de nettoyage: {e}", category="renpy_generator_clean_tl")
        return None