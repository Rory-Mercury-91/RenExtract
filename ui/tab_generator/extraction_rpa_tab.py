# ui/tab_generator/extraction_rpa_tab.py
# Onglet d'extraction RPA/RPYC + Construction RPA - Générateur de Traductions Ren'Py
# Version refactorisée avec modules business + AIDE CHEMINS CROCHETS

"""
Onglet d'extraction des fichiers RPA et RPYC + Construction RPA
- Interface de l'onglet d'extraction et construction
- Logique d'extraction et validation
- Gestion des paramètres de suppression RPA
- Construction d'archives RPA françaises
- NOUVEAU: Aide pour les limitations de chemins avec crochets
"""

import tkinter as tk
import os
from ui.themes import theme_manager
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message
from core.services.translation.rpa_extraction_business import RPAExtractionBusiness

def create_extraction_tab(parent, main_interface):
    """Crée l'onglet d'extraction - parent = frame scrollable (ajout au notebook fait par l'interface)."""
    theme = theme_manager.get_theme()
    
    tab_frame = tk.Frame(parent, bg=theme["bg"])
    tab_frame.pack(fill='both', expand=True)
    
    # Container principal avec espacement optimisé
    main_container = tk.Frame(tab_frame, bg=theme["bg"])
    main_container.pack(fill='both', expand=True, padx=20, pady=15)
    
    # Description principale AVEC bouton d'aide
    desc_frame = tk.Frame(main_container, bg=theme["bg"])
    desc_frame.pack(fill='x', pady=(0, 20))
    
    desc_label = tk.Label(
        desc_frame,
        text='Extraction/décompilation des fichiers RPA/RPYC et compilation d\'archives RPA personnalisées',
        font=('Segoe UI', 10, 'bold'),
        justify='left',
        bg=theme["bg"],
        fg=theme["accent"]
    )
    desc_label.pack(side='left', anchor='w')
    
    # NOUVEAU: Bouton d'aide pour les limitations de chemins
    help_path_btn = tk.Button(
        desc_frame,
        text="⚠ Aide chemins",
        command=lambda: show_path_limitations_help(main_interface.window),
        bg=theme["button_help_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    help_path_btn.pack(side='right')
    
    # ===== SECTION EXTRACTION =====
    extraction_frame = tk.Frame(main_container, bg=theme["bg"])
    extraction_frame.pack(fill='x', pady=(0, 20))
    
    # Titre de la section extraction
    extraction_title = tk.Label(
        extraction_frame,
        text="📂 Extraction RPA/RPYC",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    extraction_title.pack(anchor='w', pady=(0, 10))
    
    # Description extraction
    extraction_desc_label = tk.Label(
        extraction_frame,
        text='Extrait et décompile les fichiers RPA et RPYC du projet sélectionné',
        font=('Segoe UI', 9),
        justify='left',
        bg=theme["bg"],
        fg=theme["fg"]
    )
    extraction_desc_label.pack(anchor='w', pady=(0, 10))
    
    delete_rpa_check = tk.Checkbutton(
        extraction_frame,
        text='Supprimer les fichiers RPA après extraction',
        variable=main_interface.delete_rpa_var,
        command=lambda: save_delete_rpa_setting(main_interface),
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        selectcolor=theme["entry_bg"],
        activebackground=theme["bg"],
        activeforeground=theme["fg"]
    )
    delete_rpa_check.pack(anchor='w', pady=(0, 10))
    
    # Boutons d'extraction
    extraction_buttons_frame = tk.Frame(extraction_frame, bg=theme["bg"])
    extraction_buttons_frame.pack(fill='x', pady=(0, 10))
    
    extract_btn = tk.Button(
        extraction_buttons_frame,
        text="Démarrer l'extraction",
        command=lambda: start_extraction(main_interface),
        bg=theme["button_primary_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    extract_btn.pack(side='left', padx=(0, 10))
    
    # ===== SECTION CONSTRUCTION RPA =====
    rpa_build_frame = tk.Frame(main_container, bg=theme["bg"])
    rpa_build_frame.pack(fill='x', pady=(0, 20))
    
    # Titre de la section construction RPA
    rpa_title = tk.Label(
        rpa_build_frame,
        text="🛠️ Construction RPA personnalisée",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    rpa_title.pack(anchor='w', pady=(0, 10))
    
    # Description RPA
    rpa_desc_label = tk.Label(
        rpa_build_frame,
        text='Construit une archive RPA personnalisée à partir d\'un dossier de traduction',
        font=('Segoe UI', 9),
        justify='left',
        bg=theme["bg"],
        fg=theme["fg"]
    )
    rpa_desc_label.pack(anchor='w', pady=(0, 10))
    
    # === Configuration personnalisée ===
    config_frame = tk.Frame(rpa_build_frame, bg=theme["bg"])
    config_frame.pack(fill='x', pady=(0, 10))
    
    # Ligne 1 : Langue source
    lang_line = tk.Frame(config_frame, bg=theme["bg"])
    lang_line.pack(fill='x', pady=(0, 10))
    
    lang_label = tk.Label(lang_line, text="Langue source :", font=('Segoe UI', 9),
                         bg=theme["bg"], fg=theme["fg"], width=15, anchor='e')
    lang_label.pack(side='left', padx=(0, 10))
    
    # Combobox pour la langue (sera peuplée dynamiquement)
    import tkinter.ttk as ttk
    lang_combo = ttk.Combobox(lang_line, 
                             textvariable=main_interface.rpa_source_language_var,
                             width=20, state='readonly')
    lang_combo.pack(side='left', padx=(0, 10))
    
    # Bouton Scanner langues
    scan_btn = tk.Button(lang_line, text="Scanner les langues", 
                        command=lambda: scan_available_languages(main_interface, lang_combo),
                        bg=theme["button_utility_bg"],
                        fg="#000000",
                        font=('Segoe UI', 9), pady=4, padx=8,
                        relief='flat',
                        cursor='hand2')
    scan_btn.pack(side='left')
    
    # Ligne 2 : Nom de l'archive
    name_line = tk.Frame(config_frame, bg=theme["bg"])
    name_line.pack(fill='x', pady=(0, 10))
    
    name_label = tk.Label(name_line, text="Nom archive :", font=('Segoe UI', 9),
                         bg=theme["bg"], fg=theme["fg"], width=15, anchor='e')
    name_label.pack(side='left', padx=(0, 10))
    
    name_entry = tk.Entry(name_line, textvariable=main_interface.rpa_archive_name_var,
                         font=('Segoe UI', 10), width=25,
                         bg=theme["entry_bg"],
                         fg=theme["entry_fg"],
                         insertbackground=theme["entry_fg"])
    name_entry.pack(side='left', padx=(0, 5))
    
    # Label .rpa fixe
    rpa_extension_label = tk.Label(name_line, text=".rpa", font=('Segoe UI', 9, 'bold'),
                                  bg=theme["bg"], fg='#007bff')
    rpa_extension_label.pack(side='left')
    
    # Fonction de synchronisation
    def sync_archive_name(*args):
        language = main_interface.rpa_source_language_var.get()
        if language:
            # Ne stocker que le nom sans extension
            current_name = main_interface.rpa_archive_name_var.get()
            if current_name.endswith('.rpa'):
                current_name = current_name[:-4]  # Retirer .rpa
            
            # Si le champ est vide ou si c'est un changement de langue, utiliser le nom de la langue
            if not current_name.strip() or current_name == main_interface._previous_language:
                main_interface.rpa_archive_name_var.set(language)
            
            main_interface._previous_language = language
    
    # Initialiser la variable de suivi
    if not hasattr(main_interface, '_previous_language'):
        main_interface._previous_language = ""
    
    main_interface.rpa_source_language_var.trace('w', sync_archive_name)
    
    # Sous-description des types de fichiers
    rpa_subdesc_label = tk.Label(
        rpa_build_frame,
        text='Inclut: .rpy, images (.jpg/.png/.webp), sons (.ogg/.mp3), polices (.ttf/.otf), vidéos (.webm)',
        font=('Segoe UI', 9),
        justify='left',
        bg=theme["bg"],
        fg=theme["fg"],
        wraplength=600
    )
    rpa_subdesc_label.pack(anchor='w', pady=(0, 10))
    
    # Option : Suppression du dossier source après RPA
    delete_source_check = tk.Checkbutton(
        rpa_build_frame,
        text='Supprimer le dossier source après création RPA',
        variable=main_interface.delete_source_after_rpa_var,
        command=lambda: save_delete_source_setting(main_interface),
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        selectcolor=theme["entry_bg"],
        activebackground=theme["bg"],
        activeforeground=theme["fg"]
    )
    delete_source_check.pack(anchor='w', pady=(0, 10))
    
    # Boutons construction RPA
    rpa_buttons_frame = tk.Frame(rpa_build_frame, bg=theme["bg"])
    rpa_buttons_frame.pack(fill='x', pady=(0, 10))
    
    build_rpa_btn = tk.Button(
        rpa_buttons_frame,
        text="🎯 Construire archive RPA",
        command=lambda: start_custom_rpa_build(main_interface),
        bg=theme["button_secondary_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    build_rpa_btn.pack(side='left', padx=(0, 10))
    
    # === SECTION CONTRÔLES ===
    control_frame = tk.Frame(main_container, bg=theme["bg"])
    control_frame.pack(fill='x', pady=(20, 0))
    
    main_interface.operation_buttons.extend([extract_btn, build_rpa_btn])

    # --- AUTO-SCAN LANGUES CORRIGÉ ---
    # PROBLÈME 1: Définir une fonction qui capture lang_combo correctement
    def auto_scan_with_combo():
        """Fonction qui a accès à lang_combo dans sa portée"""
        if (hasattr(main_interface, "current_project_path") and 
            main_interface.current_project_path and
            hasattr(main_interface, 'rpa_source_language_var') and
            not main_interface.rpa_source_language_var.get().strip()):
            
            log_message("DEBUG", "Auto-scan onglet 1: Conditions remplies", category="auto_scan")
            scan_available_languages(main_interface, lang_combo)
        else:
            log_message("DEBUG", "Auto-scan onglet 1: Conditions non remplies", category="auto_scan")

    # PROBLÈME 2: Stocker la fonction dans main_interface pour accès global
    main_interface._auto_scan_extraction = auto_scan_with_combo

    # PROBLÈME 3: Déclenchement initial avec délai pour s'assurer que tout est prêt
    def trigger_initial_scan():
        try:
            log_message("DEBUG", f"Scan initial onglet 1 - Projet: {getattr(main_interface, 'current_project_path', 'None')}", category="auto_scan")
            auto_scan_with_combo()
        except Exception as e:
            log_message("DEBUG", f"Erreur scan initial onglet 1: {e}", category="auto_scan")

    # Déclenchement initial avec délai
    main_interface.window.after(100, trigger_initial_scan)

    # Événement changement d'onglet (onglet = wrapper scrollable, tab_frame est dedans)
    def on_tab_changed_extraction(event=None):
        try:
            nb = getattr(main_interface, "notebook", None)
            if not nb:
                return
            current_tab = nb.nametowidget(nb.select())
            w = tab_frame
            while w:
                if w == current_tab:
                    log_message("DEBUG", "Onglet 1 activé - Déclenchement auto-scan", category="auto_scan")
                    main_interface.window.after(50, auto_scan_with_combo)
                    break
                w = getattr(w, "master", None)
        except Exception as e:
            log_message("DEBUG", f"Erreur événement onglet 1: {e}", category="auto_scan")

    extraction_tab_id = f"extraction_tab_{id(tab_frame)}"
    if not hasattr(main_interface, '_tab_bindings'):
        main_interface._tab_bindings = {}
    if extraction_tab_id not in main_interface._tab_bindings and getattr(main_interface, "notebook", None):
        main_interface.notebook.bind("<<NotebookTabChanged>>", on_tab_changed_extraction, add='+')
        main_interface._tab_bindings[extraction_tab_id] = on_tab_changed_extraction

    # Hook de resync accessible globalement
    main_interface.extraction_rpa_resync = auto_scan_with_combo


def show_path_limitations_help(parent_window):
    """Affiche une popup d'aide stylisée pour les limitations de chemins avec crochets."""
    
    message_styled = [
        ("LIMITATIONS DES CHEMINS D'ACCÈS\n\n", "bold_blue"),
        ("⚠️ ", "red"), ("CHEMINS NON SUPPORTÉS", "bold_red"), ("\n\n", "normal"),
        
        ("Les chemins contenant des ", "normal"), ("crochets [ ]", "bold"), (" ne sont pas supportés.\n\n", "normal"),
        
        ("EXEMPLES PROBLÉMATIQUES :\n", "bold_red"),
        ("❌ ", "red"), ("C:/Jeux/Mon Jeu [v1.0]/\n", "italic"),
        ("❌ ", "red"), ("D:/[Backup] Projets/MonProjet/\n", "italic"),
        ("❌ ", "red"), ("/home/user/Jeux [Steam]/MonJeu/\n\n", "italic"),
        
        ("SOLUTIONS :\n", "bold_green"),
        ("1. ", "green"), ("Renommez le dossier", "bold"), (" pour retirer les crochets :\n", "normal"),
        ("   ", "normal"), ("Mon Jeu [v1.0]", "italic"), (" → ", "normal"), ("Mon Jeu v1.0", "green"), ("\n\n", "normal"),
        
        ("2. ", "green"), ("Déplacez le projet", "bold"), (" vers un chemin sans crochets :\n", "normal"),
        ("   ", "normal"), ("C:/Projets/MonJeu/", "green"), ("\n\n", "normal"),
        
        ("POURQUOI CETTE LIMITATION ?\n", "bold_yellow"),
        ("• Les crochets sont des caractères spéciaux dans certains outils.\n", "normal"),
        ("• Cela peut causer des erreurs lors de l'extraction ou compilation.\n", "normal"),
        ("• Cette limitation garantit la compatibilité maximale.\n\n", "normal"),
        
        ("✅ ", "green"), ("CONSEIL : Utilisez des noms simples sans caractères spéciaux pour vos projets.", "bold_green"),
    ]

    try:
        from ui.themes import theme_manager
        from infrastructure.helpers.unified_functions import show_custom_messagebox
        
        show_custom_messagebox(
            'warning',
            'Aide - Limitations de chemins',
            message_styled,
            theme_manager.get_theme(),
            parent=parent_window
        )
    except Exception as e:
        log_message("ERREUR", f"Erreur affichage aide chemins : {e}", category="renpy_generator_rpa")

def start_extraction(main_interface):
    """Lance l'extraction avec transmission du paramètre delete_rpa"""
    try:
        if not validate_project_for_extraction(main_interface):
            return
        
        delete_rpa_value = main_interface.delete_rpa_var.get() if hasattr(main_interface, 'delete_rpa_var') else False
        
        # Utiliser le getter pattern pour obtenir le business module
        rpa_business = main_interface._get_rpa_business()
        
        # Lancer l'extraction avec callbacks
        rpa_business.extract_rpa_files_threaded(
            main_interface.current_project_path,
            delete_rpa_after=delete_rpa_value,
            progress_callback=main_interface._on_progress_update,
            status_callback=main_interface._update_status,
            completion_callback=main_interface._on_operation_complete
        )
        
        main_interface._set_operation_running(True)
        main_interface._update_status("Extraction en cours...")
        
    except Exception as e:
        log_message("ERREUR", f"Erreur start_extraction: {e}", category="renpy_generator_rpa")
        main_interface._show_notification(f"Erreur démarrage extraction: {e}", "error")

def scan_available_languages(main_interface, lang_combo):
    """Scanne les langues disponibles dans le projet actuel"""
    try:
        if not main_interface.current_project_path:
            main_interface._show_notification('Veuillez sélectionner un projet Ren\'Py', "warning")
            return
        
        tl_path = os.path.join(main_interface.current_project_path, "game", "tl")
        if not os.path.exists(tl_path):
            main_interface._update_status("⚠️ Aucun dossier tl/ trouvé dans le projet")
            return
        
        # Utiliser la logique de scan d'InfoFrame
        languages = []
        for item in os.listdir(tl_path):
            item_path = os.path.join(tl_path, item)
            if os.path.isdir(item_path) and not item.startswith('.') and item.lower() != 'none':
                # Vérifier qu'il y a des fichiers dedans
                has_files = False
                for root, dirs, files in os.walk(item_path):
                    if any(f.endswith(('.rpy', '.jpg', '.png', '.webp', '.ogg', '.mp3', '.ttf', '.otf', '.webm')) for f in files):
                        has_files = True
                        break
                if has_files:
                    languages.append(item)
        
        if not languages:
            main_interface._update_status("⚠️ Aucune langue avec fichiers trouvée")
            return
        
        # Trier avec french en premier
        languages.sort(key=lambda x: (0 if x.lower() == 'french' else 1, x.lower()))
        
        # Peupler la combobox
        lang_combo['values'] = languages
        
        # Sélectionner french par défaut ou le premier
        default_lang = 'french' if 'french' in languages else languages[0]
        main_interface.rpa_source_language_var.set(default_lang)
        
        main_interface._update_status(f"✅ {len(languages)} langues détectées: {', '.join(languages)}")
        log_message("INFO", f"Langues scannées: {languages}", category="renpy_generator_rpa")
        
    except Exception as e:
        log_message("ERREUR", f"Erreur scan langues: {e}", category="renpy_generator_rpa")
        main_interface._show_notification(f"Erreur scan langues: {e}", "error")

def start_custom_rpa_build(main_interface):
    """Lance la construction RPA personnalisée avec option de suppression"""
    try:
        if not validate_project_for_custom_rpa_build(main_interface):
            return
        
        source_language = main_interface.rpa_source_language_var.get()
        archive_name_base = main_interface.rpa_archive_name_var.get().strip()
        
        if not source_language or not archive_name_base:
            main_interface._show_notification('Veuillez spécifier les paramètres', "warning")
            return
        
        archive_name_final = f"{archive_name_base.replace('.rpa', '')}.rpa"
        
        # ✅ RÉCUPÉRER l'option de suppression du source
        delete_source_after = main_interface.delete_source_after_rpa_var.get() if hasattr(main_interface, 'delete_source_after_rpa_var') else False
        
        # Utiliser le getter pattern pour obtenir le business module
        rpa_business = main_interface._get_rpa_business()
        
        # Lancer la construction RPA avec callbacks ET le nouveau paramètre
        rpa_business.build_custom_rpa_threaded(
            main_interface.current_project_path,
            language=source_language,
            archive_name=archive_name_final,
            delete_source_after=delete_source_after,  # ✅ NOUVEAU PARAMÈTRE
            progress_callback=main_interface._on_progress_update,
            status_callback=main_interface._update_status,
            completion_callback=main_interface._on_operation_complete
        )
        
        main_interface._set_operation_running(True)
        main_interface._update_status(f"Construction RPA {archive_name_final} en cours...")
        
    except Exception as e:
        log_message("ERREUR", f"Erreur start_custom_rpa_build: {e}", category="renpy_generator_rpa")
        main_interface._show_notification(f"Erreur démarrage construction RPA: {e}", "error")

def save_delete_source_setting(main_interface):
    """Sauvegarde immédiate du paramètre de suppression du dossier source"""
    try:
        config_manager.set('renpy_delete_source_after_rpa', main_interface.delete_source_after_rpa_var.get())
        log_message("DEBUG", f"Paramètre delete_source_after_rpa sauvegardé: {main_interface.delete_source_after_rpa_var.get()}", category="renpy_generator_rpa")
    except Exception as e:
        log_message("ERREUR", f"Erreur sauvegarde delete_source_after_rpa: {e}", category="renpy_generator_rpa")

def validate_project_for_custom_rpa_build(main_interface):
    """Valide que le projet est prêt pour la construction RPA personnalisée"""
    if not main_interface.current_project_path:
        main_interface._show_notification('Veuillez sélectionner un projet Ren\'Py', "warning")
        return False
    
    if not os.path.exists(main_interface.current_project_path):
        main_interface._show_notification('Le projet sélectionné n\'existe pas', "error")
        return False
    
    tl_folder = os.path.join(main_interface.current_project_path, "game", "tl")
    if not os.path.exists(tl_folder):
        main_interface._show_notification('Aucun dossier tl/ trouvé (game/tl/)', "warning")
        return False
    
    # Vérifier la langue sélectionnée
    source_language = main_interface.rpa_source_language_var.get()
    if source_language:
        language_folder = os.path.join(tl_folder, source_language)
        if not os.path.exists(language_folder):
            main_interface._show_notification(f'Dossier de langue {source_language} introuvable', "warning")
            return False
    
    return True

def validate_project_for_extraction(main_interface):
    """Valide que le projet est sélectionné et valide pour l'extraction"""
    if not main_interface.current_project_path:
        main_interface._show_notification('Veuillez sélectionner un projet Ren\'Py', "warning")
        return False
    
    if not os.path.exists(main_interface.current_project_path):
        main_interface._show_notification('Le projet sélectionné n\'existe pas', "error")
        return False
    
    game_folder = os.path.join(main_interface.current_project_path, "game")
    if not os.path.exists(game_folder):
        main_interface._show_notification('Le projet ne contient pas de dossier \'game\'', "error")
        return False
    
    return True

def save_delete_rpa_setting(main_interface):
    """Sauvegarde immédiate du paramètre de suppression RPA"""
    try:
        config_manager.set('renpy_delete_rpa_after', main_interface.delete_rpa_var.get())
        log_message("DEBUG", f"Paramètre delete_rpa sauvegardé: {main_interface.delete_rpa_var.get()}", category="renpy_generator_rpa")
    except Exception as e:
        log_message("ERREUR", f"Erreur sauvegarde delete_rpa: {e}", category="renpy_generator_rpa")