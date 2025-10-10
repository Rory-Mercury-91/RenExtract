# ui/tab_generator/combination_tab.py - VERSION REFACTORISÉE
# Onglet de combinaison/division - Générateur de Traductions Ren'Py
# Interface unifiée avec sections séparées par des sous-titres

"""
Onglet de combinaison et division de fichiers de traduction
- Interface unifiée avec sous-sections
- Logique de combinaison et division via business modules
- Auto-remplissage des champs selon le projet et la langue
- Section exclusions de fichiers (déplacée depuis settings)
"""

import tkinter as tk
from tkinter import filedialog
import os
from ui.themes import theme_manager
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import show_translated_messagebox
from ui.shared.common_widgets import PlaceholderEntry
from core.services.translation.combination_business import CombinationBusiness

def create_combination_tab(parent_notebook, main_interface):
    """Crée l'onglet de combinaison/division - VERSION AVEC VARIABLE UNIFIÉE"""
    theme = theme_manager.get_theme()
    
    # Frame avec thème
    tab_frame = tk.Frame(parent_notebook, bg=theme["bg"])
    parent_notebook.add(tab_frame, text="Combinaison & Division")
    
    # Container principal avec espacement optimisé
    main_container = tk.Frame(tab_frame, bg=theme["bg"])
    main_container.pack(fill='both', expand=True, padx=20, pady=15)
    
    # Description simplifiée
    desc_label = tk.Label(
        main_container,
        text="Combine plusieurs fichiers de traduction en un seul ou divise un fichier combiné",
        font=('Segoe UI', 10, 'bold'),
        justify='left',
        bg=theme["bg"],
        fg=theme["accent"]
    )
    desc_label.pack(anchor='w', pady=(0, 20))
    
    # ===== SECTION EXCLUSIONS UNIFIÉE =====
    exclusions_frame = tk.Frame(main_container, bg=theme["bg"])
    exclusions_frame.pack(fill='x', pady=(0, 20))
    
    # Titre des exclusions
    exclusions_title = tk.Label(
        exclusions_frame,
        text="🚫 Fichiers à exclure de la combinaison/division",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    exclusions_title.pack(anchor='w', pady=(0, 10))
    
    # Frame pour input + boutons
    exclusions_input_frame = tk.Frame(exclusions_frame, bg=theme["bg"])
    exclusions_input_frame.pack(fill='x', pady=(0, 10))
    
    # Entry pour les exclusions avec variable unifiée
    exclusions_entry = tk.Entry(
        exclusions_input_frame,
        textvariable=main_interface.unified_excluded_files_var,
        font=('Segoe UI', 10),
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        insertbackground=theme["entry_fg"],
        relief='solid',
        borderwidth=1
    )
    exclusions_entry.pack(side='left', fill='x', expand=True, pady=2)
    exclusions_entry.bind('<KeyRelease>', lambda e: _on_unified_exclusion_changed(main_interface))
    
    # Bouton aide
    exclusions_help_btn = tk.Button(
        exclusions_input_frame,
        text="❓",
        command=lambda: _show_unified_exclusion_help(main_interface),
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
        command=lambda: _reset_unified_exclusions(main_interface),
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
        text="💡 Exemple: common.rpy, Z_LangSelect.rpy, 99_Z_LangSelect.rpy",
        font=('Segoe UI', 8, 'italic'),
        bg=theme["bg"],
        fg='#666666'
    )
    exclusions_note.pack(anchor='w', pady=(5, 0))
    
    # ===== SECTION UNIFIÉE COMBINAISON/DIVISION =====
    operations_frame = tk.Frame(main_container, bg=theme["bg"])
    operations_frame.pack(fill='x', pady=(20, 0))
    
    # === SOUS-SECTION COMBINAISON ===
    # Titre de la section combinaison
    combine_title = tk.Label(
        operations_frame,
        text="🔗 Combinaison de fichiers",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    combine_title.pack(anchor='w', pady=(0, 10))
    
    # Frame pour titre + bouton sur la même ligne
    combine_title_frame = tk.Frame(operations_frame, bg=theme["bg"])
    combine_title_frame.pack(fill='x', pady=(0, 10))
    
    # Bouton de combinaison à droite
    combine_btn = tk.Button(
        combine_title_frame,
        text="Combiner les fichiers",
        command=lambda: start_combination(main_interface),
        bg=theme["button_primary_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    combine_btn.pack(side='right')
    
    # Dossier source combinaison
    combine_source_frame = tk.Frame(operations_frame, bg=theme["bg"])
    combine_source_frame.pack(fill='x', pady=5)
    
    tk.Label(combine_source_frame, 
            text="Dossier source:",
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"]).pack(side='left')
    
    combine_source_entry = tk.Entry(combine_source_frame, 
                                  textvariable=main_interface.combine_source_var, 
                                  font=('Segoe UI', 10), 
                                  bg=theme["entry_bg"],
                                  fg=theme["entry_fg"],
                                  insertbackground=theme["entry_fg"])
    combine_source_entry.pack(side='left', padx=(10, 5), fill='x', expand=True)
    
    combine_source_btn = tk.Button(
        combine_source_frame, 
        text="📁 Parcourir",
        command=lambda: select_combine_source(main_interface),
        bg=theme["button_nav_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    combine_source_btn.pack(side='right')

    # Fichier de sortie combinaison
    combine_output_frame = tk.Frame(operations_frame, bg=theme["bg"])
    combine_output_frame.pack(fill='x', pady=5)
    
    tk.Label(combine_output_frame, 
            text="Fichier de sortie:",
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"]).pack(side='left')
    
    main_interface.combine_output_entry = PlaceholderEntry(
        combine_output_frame, 
        textvariable=main_interface.combine_output_var, 
        placeholder="Auto: traduction.rpy dans dossier source",
        placeholder_color='grey',
        font=('Segoe UI', 9),
        bg=theme["entry_bg"],
        fg=theme["entry_fg"]
    )
    main_interface.combine_output_entry.pack(side='left', fill='x', expand=True, padx=(10, 5))
    
    combine_output_btn = tk.Button(
        combine_output_frame,
        text="📁 Parcourir",
        command=lambda: select_combine_output(main_interface),
        bg=theme["button_nav_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    combine_output_btn.pack(side='right')
    
    # === SOUS-SECTION DIVISION ===
    # Titre de la section division
    divide_title = tk.Label(
        operations_frame,
        text="✂️ Division de fichier",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    divide_title.pack(anchor='w', pady=(20, 10))
    
    # Frame pour titre + bouton sur la même ligne
    divide_title_frame = tk.Frame(operations_frame, bg=theme["bg"])
    divide_title_frame.pack(fill='x', pady=(0, 10))
    
    # Bouton de division à droite
    divide_btn = tk.Button(
        divide_title_frame,
        text="Diviser le fichier",
        command=lambda: start_division(main_interface),
        bg=theme["button_secondary_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    divide_btn.pack(side='right')
    
    # Fichier source division
    divide_source_frame = tk.Frame(operations_frame, bg=theme["bg"])
    divide_source_frame.pack(fill='x', pady=5)
    
    tk.Label(divide_source_frame, 
            text="Fichier combiné:",
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"]).pack(side='left')
    
    divide_source_entry = tk.Entry(divide_source_frame, 
                                 textvariable=main_interface.divide_source_var, 
                                 font=('Segoe UI', 10),
                                 bg=theme["entry_bg"],
                                 fg=theme["entry_fg"],
                                 insertbackground=theme["entry_fg"])
    divide_source_entry.pack(side='left', fill='x', expand=True, padx=(10, 5))
    
    divide_source_btn = tk.Button(
        divide_source_frame,
        text="📁 Parcourir",
        command=lambda: select_divide_source(main_interface),
        bg=theme["button_nav_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    divide_source_btn.pack(side='right')
    
    # Dossier de sortie division
    divide_output_frame = tk.Frame(operations_frame, bg=theme["bg"])
    divide_output_frame.pack(fill='x', pady=5)
    
    tk.Label(divide_output_frame, 
            text="Dossier de sortie:",
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"]).pack(side='left')
    
    main_interface.divide_output_entry = PlaceholderEntry(
        divide_output_frame, 
        textvariable=main_interface.divide_output_var, 
        placeholder="Auto: même dossier que le fichier source",
        placeholder_color='grey',
        font=('Segoe UI', 9),
        bg=theme["entry_bg"],
        fg=theme["entry_fg"]
    )
    main_interface.divide_output_entry.pack(side='left', fill='x', expand=True, padx=(10, 5))
    
    divide_output_btn = tk.Button(
        divide_output_frame,
        text="📁 Parcourir",
        command=lambda: select_divide_output(main_interface),
        bg=theme["button_nav_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    divide_output_btn.pack(side='right')
    
    main_interface.operation_buttons.extend([combine_btn, divide_btn])


# ===== FONCTIONS POUR LES EXCLUSIONS UNIFIÉES =====

def _on_unified_exclusion_changed(main_interface):
    """Appelé quand la liste d'exclusion unifiée change"""
    try:
        exclusions_text = main_interface.unified_excluded_files_var.get()
        
        # Sauvegarder directement dans la config (gère la conversion string->list)
        config_manager.set_renpy_excluded_files(exclusions_text)
        
        log_message("DEBUG", "Liste d'exclusions unifiée mise à jour", category="renpy_generator_combine_tl")
    except Exception as e:
        log_message("ERREUR", f"Erreur sauvegarde exclusions unifiées: {e}", category="renpy_generator_combine_tl")

def _reset_unified_exclusions(main_interface):
    """Remet les exclusions unifiées par défaut"""
    try:
        default_exclusions = "common.rpy, screens.rpy, gui.rpy, options.rpy"
        main_interface.unified_excluded_files_var.set(default_exclusions)
        
        # Sauvegarder dans la config
        config_manager.set_renpy_excluded_files(default_exclusions)
        
        log_message("INFO", "Exclusions unifiées remises par défaut", category="renpy_generator_combine_tl")
    except Exception as e:
        log_message("ERREUR", f"Erreur reset exclusions unifiées: {e}", category="renpy_generator_combine_tl")

def _show_unified_exclusion_help(main_interface):
    """Affiche l'aide stylée pour l'exclusion unifiée."""

    # On crée le message sous forme de liste pour appliquer les styles
    message_styled = [
        ("Exclusion de fichiers de la Combinaison/Division\n\n", "bold_red"),
        ("Cette option permet d'exclure certains fichiers lors des opérations de ", "normal"),
        ("combinaison", "bold"), (" et de ", "normal"), ("division", "bold"), (" des fichiers de traduction.\n\n", "normal"),

        ("Format :\n", "bold_green"),
        ("• Séparez les noms de fichiers par des ", "normal"), ("virgules", "bold"), (" (,).\n", "normal"),
        ("• Utilisez le nom complet du fichier (avec l'extension ", "normal"), (".rpy", "yellow"), (").\n", "normal"),
        ("• La correspondance sur le nom de fichier est ", "normal"), ("exacte", "underline"), (".\n\n", "normal"),

        ("Exemples valides :\n", "bold_green"),
        ("• ", "green"), ("common.rpy, screens.rpy\n", "italic"),
        ("• ", "green"), ("Z_LangSelect.rpy, 99_Z_LangSelect.rpy\n", "italic"),
        ("• ", "green"), ("(... et toute autre combinaison de fichiers)\n\n", "italic"),

        ("Cas d'usage :\n", "bold_yellow"),
        ("• Protéger les fichiers système de Ren'Py.\n", "normal"),
        ("• Isoler les fichiers de sélecteur de langue personnalisés.\n", "normal"),
        ("• Conserver les fichiers de patch ou d'ajouts spécifiques séparés.\n\n", "normal"),

        ("⚠️ ", "red"), ("Note :", "bold"), (" Ces fichiers seront ignorés lors de la combinaison de plusieurs fichiers en un seul ou lors de la division d'un fichier en plusieurs.", "normal"),
    ]

    try:
        # On appelle directement show_custom_messagebox pour utiliser les styles
        from ui.themes import theme_manager
        from infrastructure.helpers.unified_functions import show_custom_messagebox
        
        show_custom_messagebox(
            'info',
            'Aide - Exclusion de fichiers',
            message_styled,
            theme_manager.get_theme(),
            parent=main_interface.window
        )
    except Exception as e:
        log_message("ERREUR", f"Erreur affichage aide exclusion unifiée : {e}", category="renpy_generator_unified")


# ===== FONCTIONS PRINCIPALES MODIFIÉES =====

def select_combine_source(main_interface):
    """Sélectionne le dossier source pour la combinaison avec auto-génération du fichier de sortie"""
    try:
        folder = filedialog.askdirectory(title='Sélectionner le dossier contenant les fichiers de traduction')
        if folder:
            main_interface.combine_source_var.set(folder)
            
            # AUTO-GÉNÉRATION du fichier de sortie
            output_file = os.path.join(folder, "traduction.rpy")
            main_interface.combine_output_var.set(output_file)
            
            log_message("INFO", f"Dossier source sélectionné : {os.path.basename(folder)}", category="renpy_generator_combine_tl")
            log_message("INFO", f"Fichier de sortie auto-généré : traduction.rpy", category="renpy_generator_combine_tl")
            
            # Mise à jour du placeholder si c'est un PlaceholderEntry
            if hasattr(main_interface, 'combine_output_entry'):
                # Forcer la mise à jour de l'affichage
                main_interface.combine_output_entry.delete(0, tk.END)
                main_interface.combine_output_entry.insert(0, output_file)
                main_interface.combine_output_entry.config(fg=main_interface.combine_output_entry.default_fg_color)
            
    except Exception as e:
        main_interface._show_notification(f"Erreur sélection dossier: {e}", "error")
        log_message("ERREUR", f"Erreur select_combine_source: {e}", category="renpy_generator_combine_tl")

def select_combine_output(main_interface):
    """Sélectionne le fichier de sortie pour la combinaison"""
    try:
        file_path = filedialog.asksaveasfilename(
            title='Fichier de sortie combiné',
            defaultextension=".rpy",
            filetypes=[("Fichiers Ren'Py", "*.rpy"), ("Tous les fichiers", "*.*")]
        )
        if file_path:
            main_interface.combine_output_var.set(file_path)
    except Exception as e:
        main_interface._show_notification(f"Erreur sélection fichier: {e}", "error")

def select_divide_source(main_interface):
    """Sélectionne le fichier source pour la division avec auto-génération du dossier de sortie"""
    try:
        file_path = filedialog.askopenfilename(
            title='Sélectionner le fichier combiné à diviser',
            filetypes=[("Fichiers Ren'Py", "*.rpy"), ("Tous les fichiers", "*.*")]
        )
        if file_path:
            main_interface.divide_source_var.set(file_path)
            
            # AUTO-GÉNÉRATION du dossier de sortie (même dossier que le fichier source)
            output_folder = os.path.dirname(file_path)
            main_interface.divide_output_var.set(output_folder)
            
            log_message("INFO", f"Fichier source sélectionné : {os.path.basename(file_path)}", category="renpy_generator_combine_tl")
            log_message("INFO", f"Dossier de sortie auto-généré : {os.path.basename(output_folder)}", category="renpy_generator_combine_tl")
            
            # Mise à jour du placeholder si c'est un PlaceholderEntry
            if hasattr(main_interface, 'divide_output_entry'):
                # Forcer la mise à jour de l'affichage
                main_interface.divide_output_entry.delete(0, tk.END)
                main_interface.divide_output_entry.insert(0, output_folder)
                main_interface.divide_output_entry.config(fg=main_interface.divide_output_entry.default_fg_color)
            
    except Exception as e:
        main_interface._show_notification(f"Erreur sélection fichier: {e}", "error")
        log_message("ERREUR", f"Erreur select_divide_source: {e}", category="renpy_generator_combine_tl")

def select_divide_output(main_interface):
    """Sélectionne le dossier de sortie pour la division"""
    try:
        folder = filedialog.askdirectory(title='Sélectionner le dossier de sortie pour les fichiers divisés')
        if folder:
            main_interface.divide_output_var.set(folder)
    except Exception as e:
        main_interface._show_notification(f"Erreur sélection dossier: {e}", "error")

def start_combination(main_interface):
    """Démarre la combinaison de fichiers - VERSION AVEC VARIABLE UNIFIÉE"""
    try:
        source_folder = main_interface.combine_source_var.get().strip()
        
        # Utiliser get_real_value() pour les placeholders
        if hasattr(main_interface, 'combine_output_entry'):
            output_file = main_interface.combine_output_entry.get_real_value().strip()
        else:
            output_file = main_interface.combine_output_var.get().strip()
        
        if not source_folder:
            main_interface._show_notification('Veuillez sélectionner un dossier source', "warning")
            return
        
        if not os.path.exists(source_folder):
            main_interface._show_notification('Le dossier source n\'existe pas', "error")
            return
        
        # Auto-détection si vide
        if not output_file:
            output_file = os.path.join(source_folder, "traduction.rpy")
            log_message("INFO", f"Fichier de sortie auto-généré: {output_file}", category="renpy_generator_combine_tl")
        
        # Utiliser le getter pattern pour obtenir le business module
        combination_business = main_interface._get_combination_business()
        
        # VARIABLE UNIFIÉE : Récupérer directement depuis la config
        excluded_files = config_manager.get_renpy_excluded_files()
        
        log_message("INFO", f"Fichiers exclus de la combinaison: {excluded_files if excluded_files else 'Aucun'}", category="renpy_generator_combine_tl")
        
        # Lancer la combinaison avec callbacks
        combination_business.combine_translation_files_threaded(
            source_folder,
            output_file,
            excluded_files,
            progress_callback=main_interface._on_progress_update,
            status_callback=main_interface._update_status,
            completion_callback=main_interface._on_operation_complete
        )
        
        main_interface._set_operation_running(True)
        main_interface._update_status("Combinaison en cours...")
        
    except Exception as e:
        main_interface._show_notification(f"Erreur démarrage combinaison: {e}", "error")
        main_interface._set_operation_running(False)
        log_message("ERREUR", f"Erreur start_combination: {e}", category="renpy_generator_combine_tl")

def start_division(main_interface):
    """Démarre la division de fichier - VERSION AVEC VARIABLE UNIFIÉE"""
    try:
        source_file = main_interface.divide_source_var.get().strip()
        
        # Utiliser get_real_value() pour les placeholders
        if hasattr(main_interface, 'divide_output_entry'):
            output_folder = main_interface.divide_output_entry.get_real_value().strip()
        else:
            output_folder = main_interface.divide_output_var.get().strip()
        
        if not source_file:
            main_interface._show_notification('Veuillez sélectionner un fichier source', "warning")
            return
        
        if not os.path.exists(source_file):
            main_interface._show_notification('Le fichier source n\'existe pas', "error")
            return
        
        # Auto-détection si vide
        if not output_folder:
            output_folder = os.path.dirname(source_file)
            log_message("INFO", f"Dossier de sortie auto-généré: {output_folder}", category="renpy_generator_combine_tl")
        
        # Utiliser le getter pattern pour obtenir le business module
        combination_business = main_interface._get_combination_business()
        
        # Lancer la division avec callbacks
        combination_business.divide_translation_file_threaded(
            source_file,
            output_folder,
            progress_callback=main_interface._on_progress_update,
            status_callback=main_interface._update_status,
            completion_callback=main_interface._on_operation_complete
        )
        
        main_interface._set_operation_running(True)
        main_interface._update_status("Division en cours...")
        
    except Exception as e:
        main_interface._show_notification(f"Erreur démarrage division: {e}", "error")
        main_interface._set_operation_running(False)
        log_message("ERREUR", f"Erreur start_division: {e}", category="renpy_generator_combine_tl")

def auto_fill_combination_fields(main_interface, silent=False):
    """Auto-remplit les champs de combinaison/division selon le projet sélectionné et la langue choisie
    
    Args:
        main_interface: Interface principale
        silent: Si True, supprime les logs (utilisé lors du changement d'onglet)
    """
    try:
        if not main_interface.current_project_path:
            return
        
        # Utiliser la langue sélectionnée dans l'onglet Génération
        selected_language = main_interface.language_var.get().strip().lower()
        if not selected_language or selected_language == "":
            selected_language = "french"  # Fallback par défaut
        
        # COMBINAISON : Auto-remplir dossier source avec la langue sélectionnée
        tl_language_folder = os.path.join(main_interface.current_project_path, "game", "tl", selected_language)
        
        # Toujours remplir même si le dossier n'existe pas
        main_interface.combine_source_var.set(tl_language_folder)
        
        # Auto-générer fichier de sortie
        output_file = os.path.join(tl_language_folder, "traduction.rpy")
        main_interface.combine_output_var.set(output_file)
        
        # Mettre à jour le PlaceholderEntry si nécessaire
        if hasattr(main_interface, 'combine_output_entry'):
            main_interface.combine_output_entry.delete(0, tk.END)
            main_interface.combine_output_entry.insert(0, output_file)
            main_interface.combine_output_entry.config(fg=main_interface.combine_output_entry.default_fg_color)
        
        if not silent:
            log_message("INFO", f"🔗 Dossier source : {selected_language}", category="renpy_generator_combine_tl")
        
        # DIVISION : Seulement SI le fichier traduction.rpy existe déjà 
        typical_combined_file = os.path.join(tl_language_folder, "traduction.rpy")
        if os.path.exists(typical_combined_file):
            main_interface.divide_source_var.set(typical_combined_file)
            
            # Auto-générer dossier de sortie (même dossier)
            main_interface.divide_output_var.set(tl_language_folder)
            
            # Mettre à jour le PlaceholderEntry si nécessaire
            if hasattr(main_interface, 'divide_output_entry'):
                main_interface.divide_output_entry.delete(0, tk.END)
                main_interface.divide_output_entry.insert(0, tl_language_folder)
                main_interface.divide_output_entry.config(fg=main_interface.divide_output_entry.default_fg_color)
            
            log_message("INFO", f"Fichier combiné trouvé pour: {selected_language}", category="renpy_generator_combine_tl")
        else:
            # Vider les champs division si pas de fichier
            main_interface.divide_source_var.set("")
            main_interface.divide_output_var.set("")
            
            if hasattr(main_interface, 'divide_output_entry'):
                main_interface.divide_output_entry.delete(0, tk.END)
                main_interface.divide_output_entry._add_placeholder()  # Remettre le placeholder
            
            # Log supprimé : information peu utile si aucun fichier trouvé
        
    except Exception as e:
        log_message("ERREUR", f"Erreur auto_fill_combination_fields: {e}", category="renpy_generator_combine_tl")