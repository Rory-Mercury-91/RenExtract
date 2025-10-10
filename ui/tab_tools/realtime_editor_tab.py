# ui/tab_tools/realtime_editor_tab.py
# Onglet Éditeur Temps Réel - Traduction en temps réel pour jeux Ren'Py
# Created for RenExtract v2.8.0

"""
Onglet d'édition temps réel des traductions
- Installation du module de surveillance Ren'Py
- Interface d'édition VO/VF côte à côte
- Sauvegarde avec BackupType.REALTIME_EDIT
- Monitoring du fichier log_dialogues.txt
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog
import threading
import re
import time
import urllib.parse
import webbrowser
from typing import Dict, Any
from pathlib import Path
from ui.themes import theme_manager
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import show_custom_askyesnocancel, show_custom_messagebox
from core.models.backup.unified_backup_manager import BackupType
from ui.shared.editor_manager import open_file_with_editor as _open_with_editor
try:
    from ui.shared.editor_manager_server import set_dialogue_callback
except Exception:
    from ui.shared.editor_manager_server import set_focus_callback as set_dialogue_callback

def create_realtime_editor_tab(parent_notebook, main_interface):
    """Crée l'onglet d'édition temps réel avec interface optimisée."""
    theme = theme_manager.get_theme()
    
    # Frame principal
    tab_frame = tk.Frame(parent_notebook, bg=theme["bg"])
    parent_notebook.add(tab_frame, text="⚡ Éditeur Temps Réel")
    
    # Header avec titre centré et bouton d'aide à droite
    header_frame = tk.Frame(tab_frame, bg=theme["bg"])
    header_frame.pack(fill='x', padx=20, pady=(15, 10))
    
    # Titre descriptif centré
    desc_label = tk.Label(
        header_frame,
        text="Édition temps réel des traductions avec surveillance automatique et SDK Ren'Py intégré",
        font=('Segoe UI', 10, 'bold'),
        justify='center',
        bg=theme["bg"],
        fg=theme["accent"]
    )
    desc_label.pack(fill='x', anchor='center')
    
    # Bouton d'aide aligné à droite
    help_btn = tk.Button(
        header_frame,
        text="À quoi ça sert ?",
        command=lambda: show_installation_help(main_interface.window),
        bg=theme["button_secondary_bg"],
        fg="#000000",
        font=('Segoe UI', 10, 'bold'),
        width=15,
        height=1,
        relief='flat',
        cursor='hand2'
    )
    help_btn.pack(anchor='e', pady=(10, 0))

    # Variables de fenêtre détachée et police (inchangées)
    if not hasattr(main_interface, 'detached_editor_window'):
        main_interface.detached_editor_window = None

    if not hasattr(main_interface, 'editor_font_size_var'):
        main_interface.editor_font_size_var = tk.IntVar()
        default_size = config_manager.get('editor_font_size', 9)
        main_interface.editor_font_size_var.set(default_size)

    if not hasattr(main_interface, 'vf_split_mode'):
        main_interface.vf_split_mode = False
        main_interface.vf_text_widget_2 = None
        main_interface.vf_split_container = None
        main_interface.split_separator = None
    
    init_multiple_support(main_interface)
    main_interface.is_in_menu_mode = False # Vous devriez déjà avoir celle-ci
    main_interface.is_in_multiple_mode = False # <-- AJOUTEZ CETTE LIGNE
    # === SECTION MODERNISÉE: INSTALLATION & SURVEILLANCE ===
    install_monitor_frame = tk.Frame(tab_frame, bg=theme["bg"])
    install_monitor_frame.pack(fill='x', padx=20, pady=(15, 10))
    
    # Titre de section avec icône
    install_title = tk.Label(
        install_monitor_frame,
        text="🔧 Installation & Surveillance",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["accent"]
    )
    install_title.pack(anchor='w', pady=(0, 10))
    
    # Sous-section Configuration
    config_frame = tk.Frame(install_monitor_frame, bg=theme["bg"])
    config_frame.pack(fill='x', pady=(0, 10))
    
    tk.Label(config_frame, text="Configuration :", font=('Segoe UI', 9, 'bold'), bg=theme["bg"], fg=theme["fg"]).pack(side='left')
    
    tk.Label(config_frame, text=" Langue :", font=('Segoe UI', 9, 'normal'), bg=theme["bg"], fg=theme["fg"]).pack(side='left', padx=(15, 5))
    
    if not hasattr(main_interface, 'realtime_language_var'):
        main_interface.realtime_language_var = tk.StringVar(value="french")
    
    lang_combo = ttk.Combobox(
        config_frame,
        textvariable=main_interface.realtime_language_var,
        width=15,
        state="readonly",
        font=('Segoe UI', 9)
    )
    lang_combo.pack(side='left', padx=(0, 10))
    
    def on_language_changed(*args):
        update_vf_label_text(main_interface)
    main_interface.realtime_language_var.trace('w', on_language_changed)
    
    scan_btn = tk.Button(config_frame, text="Scanner les langues", command=lambda: scan_available_languages(main_interface, lang_combo), bg=theme["button_utility_bg"], fg="#000000", font=('Segoe UI', 9, 'normal'), pady=4, padx=8, relief='flat', cursor='hand2')
    scan_btn.pack(side='left', padx=(0, 10))

    install_btn = tk.Button(config_frame, text="Installer le module", command=lambda: install_monitoring_module(main_interface), bg=theme["button_feature_bg"], fg="#000000", font=('Segoe UI', 9, 'normal'), pady=4, padx=8, relief='flat', cursor='hand2')
    install_btn.pack(side='left')

    # --- AUTO-SCAN LANGUE (création + re-sélection de l'onglet) ---
    def _auto_scan_realtime_if_ready(*_):
        # On n'essaie que si on a un projet et si la combo n'a pas encore été remplie
        has_project = bool(getattr(main_interface, "current_project_path", ""))
        combo_empty = not lang_combo['values']
        if has_project and combo_empty:
            try:
                # ta fonction existante de scan dans cet onglet
                scan_available_languages(main_interface, lang_combo)
            except Exception as e:
                log_message("DEBUG", f"Auto-scan realtime échoué: {e}", category="realtime_editor")

    # 1) au moment de la création (si un projet est déjà restauré)
    _auto_scan_realtime_if_ready()

    # 2) quand l'onglet devient actif
    def _on_tab_changed_realtime(event=None):
        current = parent_notebook.nametowidget(parent_notebook.select())
        if current is tab_frame:
            _auto_scan_realtime_if_ready()

    parent_notebook.bind("<<NotebookTabChanged>>", _on_tab_changed_realtime)

    # 3) (optionnel) expose un hook pour resync forcé depuis la fenêtre principale
    main_interface.realtime_resync = _auto_scan_realtime_if_ready


    controls_frame = tk.Frame(install_monitor_frame, bg=theme["bg"])
    controls_frame.pack(fill='x', pady=(0, 10))
    
    tk.Label(controls_frame, text="Contrôles :", font=('Segoe UI', 9, 'bold'), bg=theme["bg"], fg=theme["fg"]).pack(side='left')
    
    if not hasattr(main_interface, 'monitoring_active'):
        main_interface.monitoring_active = False
    
    main_interface.start_monitor_btn = tk.Button(controls_frame, text="▶️ Démarrer la surveillance", command=lambda: start_monitoring(main_interface), bg=theme["button_primary_bg"], fg="#000000", font=('Segoe UI', 9, 'normal'), pady=4, padx=8, relief='flat', cursor='hand2')
    main_interface.start_monitor_btn.pack(side='left', padx=(15, 10))

    main_interface.stop_monitor_btn = tk.Button(controls_frame, text="⏹️ Arrêter la surveillance", command=lambda: stop_monitoring(main_interface), bg=theme["button_danger_bg"], fg="#000000", font=('Segoe UI', 9, 'normal'), pady=4, padx=8, relief='flat', cursor='hand2', state='disabled')
    main_interface.stop_monitor_btn.pack(side='left')
    
    # === SECTION MODERNISÉE: ÉDITION DES TRADUCTIONS ===
    edit_frame = tk.Frame(tab_frame, bg=theme["bg"])
    edit_frame.pack(fill='both', expand=True, padx=20, pady=(0, 15))
    main_interface.realtime_edit_frame = edit_frame
    
    # Titre de section avec icône
    edit_title = tk.Label(
        edit_frame,
        text="✏️ Édition des traductions",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["accent"]
    )
    edit_title.pack(anchor='w', pady=(0, 10))
    
    header_frame = tk.Frame(edit_frame, bg=theme["bg"])
    header_frame.pack(fill='x', pady=(0, 10))

    main_interface.monitor_status_label = tk.Label(header_frame, text="⭕ Surveillance arrêtée", font=('Segoe UI', 9, 'bold'), bg=theme["bg"], fg='#dc3545')
    main_interface.monitor_status_label.pack(side='left')

    _build_editor_controls(header_frame, main_interface, is_detached=False)

    main_interface.realtime_edit_main = _build_editor_panel(edit_frame, main_interface)
    main_interface.realtime_edit_main.pack(fill='both', expand=True, pady=(0, 10))
    
    def on_ctrl_s(event):
        try:
            current_tab = main_interface.notebook.tab(main_interface.notebook.select(), "text")
            if "Temps Réel" in current_tab or "⚡" in current_tab:
                save_translation(main_interface)
            return 'break'
        except Exception:
            return 'break'
    tab_frame.bind_all('<Control-s>', on_ctrl_s)
    tab_frame.bind_all('<Control-S>', on_ctrl_s)
    
    def on_escape(event):
        if main_interface.current_dialogue_info:
            main_interface.current_dialogue_info = {}
            main_interface.vo_text_widget.config(state='normal')
            main_interface.vo_text_widget.delete('1.0', tk.END)
            main_interface.vo_text_widget.insert('1.0', "En attente de dialogue...")
            main_interface.vo_text_widget.config(state='disabled')
            main_interface.vf_text_widget.delete('1.0', tk.END)
            main_interface._update_status("Interface réinitialisée")
    tab_frame.bind_all('<Escape>', on_escape)

    if not hasattr(main_interface, 'current_dialogue_info'):
        main_interface.current_dialogue_info = {}
    
    update_vf_label_text(main_interface)
    
    buttons_to_extend = [
        install_btn, 
        main_interface.start_monitor_btn, 
        main_interface.stop_monitor_btn
    ]
    main_interface.operation_buttons.extend(buttons_to_extend)

def _build_editor_controls(parent_container, main_interface, is_detached=False):
    """
    ### REFACTORISATION ###
    Nouvelle fonction qui centralise la création des contrôles de l'éditeur (DRY).
    Elle gère les variations entre la vue attachée et détachée.
    """
    theme = theme_manager.get_theme()
    
    controls_right_frame = tk.Frame(parent_container, bg=theme["bg"])
    controls_right_frame.pack(side='right')

    # Contrôles d'interface
    interface_controls_frame = tk.Frame(controls_right_frame, bg=theme["bg"])
    interface_controls_frame.pack(side='right')

    # Le bouton change en fonction du contexte (détaché ou non)
    if is_detached:
        attach_button = tk.Button(
            interface_controls_frame, text="↙️ Rattacher", font=('Segoe UI', 9, 'normal'),
            command=lambda: on_editor_close(main_interface),
            bg=theme["button_utility_bg"], fg="#000000", pady=4, padx=8
        )
        attach_button.pack(side='right')
    else:
        detach_button = tk.Button(
            interface_controls_frame, text="↗️ Détacher", font=('Segoe UI', 9, 'normal'),
            command=lambda: detach_editor(main_interface),
            bg=theme["button_utility_bg"], fg="#000000", pady=4, padx=8
        )
        detach_button.pack(side='right')

    default_font_btn = tk.Button(
        interface_controls_frame, text="Par défaut", font=('Segoe UI', 9, 'normal'),
        command=lambda: reset_font_size_to_default(main_interface),
        bg=theme["button_tertiary_bg"], fg="#000000", pady=4, padx=8
    )
    default_font_btn.pack(side='right', padx=(0, 10))

    font_size_spinbox = tk.Spinbox(
        interface_controls_frame, from_=8, to=24, width=4,
        textvariable=main_interface.editor_font_size_var,
        command=lambda: update_editor_font_size(main_interface)
    )
    font_size_spinbox.pack(side='right', padx=(0, 10))

    font_size_label = tk.Label(
        interface_controls_frame, text="Taille police :", font=('Segoe UI', 9, 'normal'),
        bg=theme["bg"], fg=theme["fg"]
    )
    font_size_label.pack(side='right')


def open_deepl_website(main_interface):
    """Ouvre DeepL sans pré-remplir le texte"""
    try:
        import webbrowser
        webbrowser.open("https://www.deepl.com/translator")
        main_interface._update_status("DeepL ouvert")
    except Exception as e:
        log_message("ERREUR", f"Erreur ouverture DeepL: {e}", category="realtime_editor")

def open_google_translate_website(main_interface):
    """Ouvre Google Translate sans pré-remplir le texte"""
    try:
        import webbrowser
        webbrowser.open("https://translate.google.com/")
        main_interface._update_status("Google Translate ouvert")
    except Exception as e:
        log_message("ERREUR", f"Erreur ouverture Google Translate: {e}", category="realtime_editor")

def update_editor_font_size(main_interface):
    """Met à jour la taille de police des zones de texte et sauvegarde le choix."""
    try:
        new_size = main_interface.editor_font_size_var.get()
        new_font = ('Segoe UI', new_size)

        # Mettre à jour les widgets s'ils existent
        if hasattr(main_interface, 'vo_text_widget') and main_interface.vo_text_widget.winfo_exists():
            main_interface.vo_text_widget.config(font=new_font)
        
        if hasattr(main_interface, 'vf_text_widget') and main_interface.vf_text_widget.winfo_exists():
            main_interface.vf_text_widget.config(font=new_font)

        # Sauvegarder la nouvelle taille dans la configuration
        config_manager.set('editor_font_size', new_size)
        log_message("INFO", f"Taille de police de l'éditeur changée à {new_size}pt", category="realtime_editor")

    except Exception as e:
        log_message("ERREUR", f"Erreur lors de la mise à jour de la police: {e}", category="realtime_editor")

def _build_editor_panel(parent_container, main_interface, is_detached=False):
    """
    Version complète utilisant Grid pour un meilleur contrôle de la hauteur
    """
    # Vérifier si on a un groupe multiple
    multiple_group = getattr(main_interface, 'current_multiple_group', None)
    
    if multiple_group and multiple_group.get('is_multiple'):
        return _build_multiple_dialogue_interface_with_individual_buttons(parent_container, main_interface, multiple_group, is_detached)
    else:
        theme = theme_manager.get_theme()
        current_font_size = main_interface.editor_font_size_var.get()
        editor_font = ('Segoe UI', current_font_size)
        
        # Hauteurs adaptées selon le mode (réduite pour compenser le header)
        TEXT_AREA_HEIGHT = 200

        edit_main = tk.Frame(parent_container, bg=theme["bg"])

        # Configuration de la grille principale
        if is_detached:
            edit_main.grid_rowconfigure(0, weight=0)  # Header
            edit_main.grid_rowconfigure(1, weight=1)  # Zones de texte
            edit_main.grid_rowconfigure(2, weight=0)  # Boutons globaux
        else:
            edit_main.grid_rowconfigure(0, weight=1)  # Zones de texte
            edit_main.grid_rowconfigure(1, weight=0)  # Boutons globaux

        # Proportions : VO 40% / VF 60%
        edit_main.grid_columnconfigure(0, weight=40, minsize=200)
        edit_main.grid_columnconfigure(1, weight=60, minsize=300)

        # HEADER SEULEMENT POUR LA FENÊTRE DÉTACHÉE
        if is_detached:
            header_frame = tk.Frame(edit_main, bg=theme["bg"])
            header_frame.grid(row=0, column=0, columnspan=2, sticky='ew', padx=15, pady=(5, 10))

            if hasattr(main_interface, 'monitor_status_label'):
                current_text = main_interface.monitor_status_label.cget("text")
                current_fg = main_interface.monitor_status_label.cget("fg")
            else:
                current_text = "⭕ Surveillance arrêtée"
                current_fg = '#dc3545'
            
            status_label = tk.Label(header_frame, text=current_text, font=('Segoe UI', 9, 'bold'), bg=theme["bg"], fg=current_fg)
            status_label.pack(side='left')

            # ### REFACTORISATION ### : Appel à la nouvelle fonction centralisée
            _build_editor_controls(header_frame, main_interface, is_detached=True)

        # ZONES DE TEXTE avec Grid
        text_areas_frame = tk.Frame(edit_main, bg=theme["bg"])
        if is_detached:
            text_areas_frame.grid(row=1, column=0, columnspan=2, sticky='nsew')
        else:
            text_areas_frame.grid(row=0, column=0, columnspan=2, sticky='ew')

        text_areas_frame.grid_columnconfigure(0, weight=40)
        text_areas_frame.grid_columnconfigure(1, weight=60)
        text_areas_frame.grid_rowconfigure(0, weight=1)

        # --- COLONNE VO avec Grid ---
        main_interface.vo_main_container = tk.Frame(text_areas_frame, bg=theme["bg"])
        main_interface.vo_main_container.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        
        main_interface.vo_main_container.grid_rowconfigure(0, weight=0)
        main_interface.vo_main_container.grid_rowconfigure(1, weight=1)
        main_interface.vo_main_container.grid_columnconfigure(0, weight=1)

        vo_label = tk.Label(main_interface.vo_main_container, text="Texte Original (VO)", font=('Segoe UI', 10, 'bold'), bg=theme["bg"], fg=theme["fg"])
        vo_label.grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        main_interface.vo_content_container = tk.Frame(main_interface.vo_main_container, bg=theme["bg"], height=TEXT_AREA_HEIGHT)
        main_interface.vo_content_container.grid(row=1, column=0, sticky='ew')
        
        main_interface.vo_content_container.grid_propagate(False)
        main_interface.vo_content_container.grid_rowconfigure(0, weight=1)
        main_interface.vo_content_container.grid_rowconfigure(1, weight=0)
        main_interface.vo_content_container.grid_columnconfigure(0, weight=1)

        _create_normal_vo_interface_with_grid(main_interface)

        # --- COLONNE VF avec Grid ---
        main_interface.vf_main_container = tk.Frame(text_areas_frame, bg=theme["bg"])
        main_interface.vf_main_container.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
        
        main_interface.vf_main_container.grid_rowconfigure(0, weight=0)
        main_interface.vf_main_container.grid_rowconfigure(1, weight=1)
        main_interface.vf_main_container.grid_columnconfigure(0, weight=1)

        main_interface.vf_label = tk.Label(main_interface.vf_main_container, text=f"Traduction ({main_interface.realtime_language_var.get().title()})", font=('Segoe UI', 10, 'bold'), bg=theme["bg"], fg=theme["fg"])
        main_interface.vf_label.grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        main_interface.vf_content_container = tk.Frame(main_interface.vf_main_container, bg=theme["bg"], height=TEXT_AREA_HEIGHT)
        main_interface.vf_content_container.grid(row=1, column=0, sticky='ew')
        
        main_interface.vf_content_container.grid_propagate(False)
        main_interface.vf_content_container.grid_rowconfigure(0, weight=1)
        main_interface.vf_content_container.grid_rowconfigure(1, weight=0)
        main_interface.vf_content_container.grid_columnconfigure(0, weight=1)
        
        _create_normal_vf_interface_with_grid_and_buttons(main_interface)

        # BOUTONS GLOBAUX
        buttons_frame = tk.Frame(edit_main, bg=theme["bg"])
        if is_detached:
            buttons_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        else:
            buttons_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        
        buttons_frame.grid_columnconfigure(1, weight=1)

        global_buttons_group = tk.Frame(buttons_frame, bg=theme["bg"])
        global_buttons_group.grid(row=0, column=1, sticky='e')
        
        tk.Button(global_buttons_group, text="Ouvrir", command=lambda: open_modified_file(main_interface), bg=theme["button_nav_bg"], fg="#000000", font=('Segoe UI', 9, 'normal'), pady=4, padx=8).pack(side='left', padx=(0, 5))
        
        save_btn = tk.Button(global_buttons_group, text="Enregistrer", command=lambda: save_translation(main_interface), bg=theme["button_secondary_bg"], fg="#000000", font=('Segoe UI', 9, 'normal'), pady=4, padx=8)
        save_btn.pack(side='left')
        
        if hasattr(main_interface, 'operation_buttons'):
            main_interface.operation_buttons.append(save_btn)

        return edit_main

def _create_normal_vo_interface_with_grid(main_interface):
    """Crée l'interface VO normale avec le thème sombre."""
    theme = theme_manager.get_theme()
    editor_font = ('Segoe UI', main_interface.editor_font_size_var.get())

    for widget in main_interface.vo_content_container.winfo_children():
        widget.destroy()

    # ✅ MODIFIÉ : Application du thème sombre
    vo_text = tk.Text(
        main_interface.vo_content_container,
        wrap='word',
        font=editor_font,
        bg=theme["entry_bg"],
        fg=theme["fg"],
        state='disabled',
        relief='solid',
        borderwidth=1,
        highlightbackground='#666666'
    )
    vo_text.grid(row=0, column=0, sticky='nsew', pady=(0, 5))
    main_interface.vo_text_widget = vo_text

    vo_buttons_frame = tk.Frame(main_interface.vo_content_container, bg=theme["bg"])
    vo_buttons_frame.grid(row=1, column=0, pady=8)

    tk.Button(
        vo_buttons_frame, text="Copier",
        command=lambda: copy_vo_text_simple(main_interface),
        bg=theme["button_utility_bg"], fg="#000000",
        font=('Segoe UI', 9, 'normal'), pady=4, padx=8
    ).pack(side='left', padx=(0, 5))

    tk.Button(
        vo_buttons_frame, text="DeepL",
        command=lambda: deepl_vo_text_simple(main_interface),
        bg=theme["button_tertiary_bg"], fg="#000000",
        font=('Segoe UI', 9, 'normal'), pady=4, padx=8
    ).pack(side='left', padx=(0, 5))

    # 👉 NOUVEAU : bouton Google, à côté de DeepL (utilise le texte VO affiché)
    tk.Button(
        vo_buttons_frame, text="Google",
        command=lambda: _open_google_with_text(main_interface, main_interface.vo_text_widget.get('1.0', tk.END)),
        bg=theme.get("button_google_bg", theme["button_tertiary_bg"]), fg="#000000",
        font=('Segoe UI', 9, 'normal'), pady=4, padx=8
    ).pack(side='left')

    main_interface.vo_split_mode = False


def _create_normal_vf_interface_with_grid_and_buttons(main_interface):
    """Crée l'interface VF normale avec le thème sombre."""
    theme = theme_manager.get_theme()
    editor_font = ('Segoe UI', main_interface.editor_font_size_var.get())

    for widget in main_interface.vf_content_container.winfo_children():
        widget.destroy()

    # ✅ MODIFIÉ : Application du thème sombre
    vf_text = tk.Text(main_interface.vf_content_container, wrap='word', font=editor_font,
                     bg=theme["entry_bg"], fg=theme["accent"], relief='solid', borderwidth=1,
                     insertbackground='#1976d2', highlightbackground='#666666')
    vf_text.grid(row=0, column=0, sticky='nsew', pady=(0, 5))
    main_interface.vf_text_widget = vf_text
    main_interface.vf_text_widget_2 = None

    vf_buttons_frame = tk.Frame(main_interface.vf_content_container, bg=theme["bg"])
    vf_buttons_frame.grid(row=1, column=0, pady=8)

    tk.Button(vf_buttons_frame, text="Coller", command=lambda: paste_vf_text_simple(main_interface),
              bg=theme["button_primary_bg"], fg="#000000", font=('Segoe UI', 9, 'normal'), pady=4, padx=8).pack(side='left', padx=(0, 5))
    main_interface.split_button = tk.Button(vf_buttons_frame, text="Diviser", command=lambda: toggle_split_mode(main_interface),
                                             bg=theme["button_feature_bg"], fg="#000000", font=('Segoe UI', 9, 'normal'), pady=4, padx=8)
    main_interface.split_button.pack(side='left')

    main_interface.vf_split_mode = False


def _create_split_vf_interface_with_grid_and_buttons(main_interface, part1_text="", part2_text="", part_number=1, total_parts=2, split_type="multiline"):
    """Interface VF split avec thème sombre — état actif adouci (gris) et switch visuel fiable."""
    theme = theme_manager.get_theme()
    editor_font = ('Segoe UI', main_interface.editor_font_size_var.get())

    # Couleurs "douces" pour l'état actif (fallback si le thème n'en fournit pas)
    soft_active_bg     = theme.get("soft_active_bg", '#2f3338')   # gris bleuté très doux (sur fond sombre)
    soft_active_border = theme.get("soft_active_border", '#8a9099')
    active_label_fg    = theme.get("active_label_fg", theme["fg"])
    normal_bg, normal_border = theme["entry_bg"], '#666666'

    for w in main_interface.vf_content_container.winfo_children():
        w.destroy()

    main_interface.vf_content_container.grid_rowconfigure(0, weight=1)
    main_interface.vf_content_container.grid_rowconfigure(1, weight=0)
    main_interface.vf_content_container.grid_columnconfigure(0, weight=1)
    main_interface.vf_content_container.grid_columnconfigure(1, weight=1)

    if split_type == "speaker_dialogue":
        part1_label_text, part2_label_text = "Locuteur", "Dialogue"
        is_part1_active, is_part2_active = False, True
    else:
        part1_label_text, part2_label_text = f"Partie 1/{total_parts}", f"Partie 2/{total_parts}"
        is_part1_active, is_part2_active = (part_number == 1), (part_number == 2)

    # --- PARTIE 1 ---
    p1 = tk.Frame(main_interface.vf_content_container, bg=theme["bg"])
    p1.grid(row=0, column=0, sticky='nsew', padx=(0, 2))
    p1.grid_rowconfigure(0, weight=0); p1.grid_rowconfigure(1, weight=1); p1.grid_rowconfigure(2, weight=0)
    p1.grid_columnconfigure(0, weight=1)

    lbl1 = tk.Label(
        p1, text=part1_label_text,
        font=('Segoe UI', 9, 'bold' if is_part1_active else 'normal'),
        bg=soft_active_bg if is_part1_active else theme["bg"],
        fg=active_label_fg if is_part1_active else theme["fg"]
    )
    lbl1.grid(row=0, column=0, sticky='w', pady=(0, 2))

    txt1 = tk.Text(
        p1, wrap='word', font=editor_font,
        bg=soft_active_bg if is_part1_active else normal_bg,
        fg=theme["accent"], relief='solid',
        borderwidth=2 if is_part1_active else 1,
        highlightbackground=soft_active_border if is_part1_active else normal_border,
        highlightcolor=soft_active_border if is_part1_active else normal_border,
        insertbackground='#1976d2'
    )
    txt1.grid(row=1, column=0, sticky='nsew', pady=(0, 5))
    txt1.insert('1.0', part1_text)
    tk.Button(p1, text="Coller", command=lambda: paste_to_split_part1(main_interface),
              bg=theme["button_primary_bg"], fg="#000000", font=('Segoe UI', 9), pady=4, padx=8).grid(row=2, column=0, pady=5)

    # --- PARTIE 2 ---
    p2 = tk.Frame(main_interface.vf_content_container, bg=theme["bg"])
    p2.grid(row=0, column=1, sticky='nsew', padx=(2, 0))
    p2.grid_rowconfigure(0, weight=0); p2.grid_rowconfigure(1, weight=1); p2.grid_rowconfigure(2, weight=0)
    p2.grid_columnconfigure(0, weight=1)

    lbl2 = tk.Label(
        p2, text=part2_label_text,
        font=('Segoe UI', 9, 'bold' if is_part2_active else 'normal'),
        bg=soft_active_bg if is_part2_active else theme["bg"],
        fg=active_label_fg if is_part2_active else theme["fg"]
    )
    lbl2.grid(row=0, column=0, sticky='w', pady=(0, 2))

    txt2 = tk.Text(
        p2, wrap='word', font=editor_font,
        bg=soft_active_bg if is_part2_active else normal_bg,
        fg=theme["accent"], relief='solid',
        borderwidth=2 if is_part2_active else 1,
        highlightbackground=soft_active_border if is_part2_active else normal_border,
        highlightcolor=soft_active_border if is_part2_active else normal_border,
        insertbackground='#1976d2'
    )
    txt2.grid(row=1, column=0, sticky='nsew', pady=(0, 5))
    txt2.insert('1.0', part2_text)
    tk.Button(p2, text="Coller", command=lambda: paste_to_split_part2(main_interface),
              bg=theme["button_primary_bg"], fg="#000000", font=('Segoe UI', 9), pady=4, padx=8).grid(row=2, column=0, pady=5)

    if split_type != "speaker_dialogue":
        btns = tk.Frame(main_interface.vf_content_container, bg=theme["bg"])
        btns.grid(row=1, column=0, columnspan=2, pady=(5, 0))
        main_interface.split_button = tk.Button(btns, text="Fusionner",
                                                command=lambda: toggle_split_mode(main_interface),
                                                bg=theme["button_feature_bg"], fg="#000000",
                                                font=('Segoe UI', 9), pady=4, padx=8)
        main_interface.split_button.pack()

    # Expose les widgets pour le switch visuel
    main_interface.vf_part1_widgets = {'label': lbl1, 'text': txt1}
    main_interface.vf_part2_widgets = {'label': lbl2, 'text': txt2}
    main_interface.vf_text_widget = txt1
    main_interface.vf_text_widget_2 = txt2
    main_interface.vf_split_mode = True
    main_interface.current_split_type = split_type

def _create_split_vo_interface_for_unnamed_speaker_with_grid_and_buttons(main_interface, speaker_text, dialogue_text):
    """Interface VO split pour locuteur non défini avec Grid et boutons Copier"""
    try:
        theme = theme_manager.get_theme()
        editor_font = ('Segoe UI', main_interface.editor_font_size_var.get())
        
        for widget in main_interface.vo_content_container.winfo_children():
            widget.destroy()
        
        main_interface.vo_content_container.grid_columnconfigure(0, weight=1); main_interface.vo_content_container.grid_columnconfigure(1, weight=1); main_interface.vo_content_container.grid_rowconfigure(0, weight=1)
        
        # --- Widget Locuteur (VO) ---
        speaker_container = tk.Frame(main_interface.vo_content_container, bg=theme["bg"]); speaker_container.grid(row=0, column=0, sticky='nsew', padx=(0, 2))
        speaker_container.grid_rowconfigure(0, weight=0); speaker_container.grid_rowconfigure(1, weight=1); speaker_container.grid_rowconfigure(2, weight=0); speaker_container.grid_columnconfigure(0, weight=1)
        tk.Label(speaker_container, text="Locuteur Original", font=('Segoe UI', 9, 'bold'), bg=theme["bg"], fg=theme["fg"]).grid(row=0, column=0, sticky='w', pady=(0, 2))
        # ✅ MODIFIÉ : Application du thème sombre
        speaker_widget = tk.Text(
            speaker_container,
            wrap='word',
            font=editor_font,
            bg=theme["entry_bg"],
            fg=theme["fg"],
            relief='solid',
            borderwidth=1,
            state='disabled',
            highlightbackground='#666666'
        )
        speaker_widget.grid(row=1, column=0, sticky='nsew', pady=(0, 5))
        speaker_widget.config(state='normal'); speaker_widget.insert('1.0', speaker_text); speaker_widget.config(state='disabled')
        speaker_buttons_frame = tk.Frame(speaker_container, bg=theme["bg"])
        speaker_buttons_frame.grid(row=2, column=0, pady=5)

        tk.Button(
            speaker_buttons_frame, text="Copier",
            command=lambda: copy_vo_speaker_text(main_interface),
            bg=theme["button_utility_bg"], fg="#000000", font=('Segoe UI', 9), pady=4, padx=8
        ).pack(side='left', padx=(0, 5))

        tk.Button(
            speaker_buttons_frame, text="DeepL",
            command=lambda: deepl_vo_speaker_text(main_interface),
            bg=theme["button_tertiary_bg"], fg="#000000", font=('Segoe UI', 9), pady=4, padx=8
        ).pack(side='left', padx=(0, 5))

        # 👉 NOUVEAU
        tk.Button(
            speaker_buttons_frame, text="Google",
            command=lambda: _open_google_with_text(main_interface, speaker_widget.get('1.0', tk.END)),
            bg=theme.get("button_google_bg", theme["button_tertiary_bg"]), fg="#000000",
            font=('Segoe UI', 9), pady=4, padx=8
        ).pack(side='left')


        # --- Widget Dialogue (VO) ---
        dialogue_container = tk.Frame(main_interface.vo_content_container, bg=theme["bg"]); dialogue_container.grid(row=0, column=1, sticky='nsew', padx=(2, 0))
        dialogue_container.grid_rowconfigure(0, weight=0); dialogue_container.grid_rowconfigure(1, weight=1); dialogue_container.grid_rowconfigure(2, weight=0); dialogue_container.grid_columnconfigure(0, weight=1)
        tk.Label(dialogue_container, text="Dialogue Original", font=('Segoe UI', 9, 'bold'), bg=theme["bg"], fg=theme["fg"]).grid(row=0, column=0, sticky='w', pady=(0, 2))
        # ✅ MODIFIÉ : Application du thème sombre
        dialogue_widget = tk.Text(
            dialogue_container,
            wrap='word',
            font=editor_font,
            bg=theme["entry_bg"],
            fg=theme["fg"],
            relief='solid',
            borderwidth=1,
            state='disabled',
            highlightbackground='#666666'
        )
        dialogue_widget.grid(row=1, column=0, sticky='nsew', pady=(0, 5))
        dialogue_widget.config(state='normal'); dialogue_widget.insert('1.0', dialogue_text); dialogue_widget.config(state='disabled')
        dialogue_buttons_frame = tk.Frame(dialogue_container, bg=theme["bg"])
        dialogue_buttons_frame.grid(row=2, column=0, pady=5)

        tk.Button(
            dialogue_buttons_frame, text="Copier",
            command=lambda: copy_vo_dialogue_text(main_interface),
            bg=theme["button_utility_bg"], fg="#000000", font=('Segoe UI', 9), pady=4, padx=8
        ).pack(side='left', padx=(0, 5))

        tk.Button(
            dialogue_buttons_frame, text="DeepL",
            command=lambda: deepl_vo_dialogue_text(main_interface),
            bg=theme["button_tertiary_bg"], fg="#000000", font=('Segoe UI', 9), pady=4, padx=8
        ).pack(side='left', padx=(0, 5))

        # 👉 NOUVEAU
        tk.Button(
            dialogue_buttons_frame, text="Google",
            command=lambda: _open_google_with_text(main_interface, dialogue_widget.get('1.0', tk.END)),
            bg=theme.get("button_google_bg", theme["button_tertiary_bg"]), fg="#000000",
            font=('Segoe UI', 9), pady=4, padx=8
        ).pack(side='left')


        # Pointeurs conservés à l’identique
        main_interface.vo_text_widget = dialogue_widget
        main_interface.vo_speaker_widget = speaker_widget
        main_interface.vo_split_mode = True
    except Exception as e:
        log_message("ERREUR", f"Erreur création interface VO split avec Grid: {e}", category="realtime_editor")


def _create_split_vf_interface_for_unnamed_speaker_with_grid_and_buttons(main_interface, part1_text="", part2_text=""):
    """Interface VF pour locuteur + dialogue avec thème sombre, état actif doux (gris) et switch visuel correct."""
    theme = theme_manager.get_theme()
    editor_font = ('Segoe UI', main_interface.editor_font_size_var.get())

    # Couleurs "douces" pour l'état actif (fallback si non présentes dans le thème)
    soft_active_bg     = theme.get("soft_active_bg", '#2f3338')   # gris doux visible sur fond sombre
    soft_active_border = theme.get("soft_active_border", '#8a9099')
    active_label_fg    = theme.get("active_label_fg", theme["fg"])
    normal_bg          = theme["entry_bg"]
    normal_border      = '#666666'

    # Reset du container
    for widget in main_interface.vf_content_container.winfo_children():
        widget.destroy()

    # Layout principal
    main_interface.vf_content_container.grid_rowconfigure(0, weight=1)
    main_interface.vf_content_container.grid_columnconfigure(0, weight=1)
    main_interface.vf_content_container.grid_columnconfigure(1, weight=1)

    # --- Locuteur (inactif par défaut) ---
    speaker_container = tk.Frame(main_interface.vf_content_container, bg=theme["bg"])
    speaker_container.grid(row=0, column=0, sticky='nsew', padx=(0, 2))
    speaker_container.grid_rowconfigure(0, weight=0)
    speaker_container.grid_rowconfigure(1, weight=1)
    speaker_container.grid_rowconfigure(2, weight=0)
    speaker_container.grid_columnconfigure(0, weight=1)

    label_speaker = tk.Label(
        speaker_container,
        text="Locuteur",
        font=('Segoe UI', 9, 'normal'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    label_speaker.grid(row=0, column=0, sticky='w', pady=(0, 2))

    vf_speaker_widget = tk.Text(
        speaker_container,
        wrap='word',
        font=editor_font,
        bg=normal_bg,
        fg=theme["accent"],
        relief='solid',
        borderwidth=1,
        insertbackground='#1976d2',
        highlightbackground=normal_border,
        highlightcolor=normal_border
    )
    vf_speaker_widget.grid(row=1, column=0, sticky='nsew', pady=(0, 5))
    vf_speaker_widget.insert('1.0', part1_text)

    tk.Button(
        speaker_container,
        text="Coller",
        command=lambda: paste_to_vf_speaker(main_interface),
        bg=theme["button_primary_bg"],
        fg="#000000",
        font=('Segoe UI', 9, 'normal'),
        pady=4, padx=8
    ).grid(row=2, column=0, pady=5)

    # --- Dialogue (actif par défaut) ---
    dialogue_container = tk.Frame(main_interface.vf_content_container, bg=theme["bg"])
    dialogue_container.grid(row=0, column=1, sticky='nsew', padx=(2, 0))
    dialogue_container.grid_rowconfigure(0, weight=0)
    dialogue_container.grid_rowconfigure(1, weight=1)
    dialogue_container.grid_rowconfigure(2, weight=0)
    dialogue_container.grid_columnconfigure(0, weight=1)

    label_dialogue = tk.Label(
        dialogue_container,
        text="Dialogue",
        font=('Segoe UI', 9, 'bold'),
        bg=soft_active_bg,
        fg=active_label_fg
    )
    label_dialogue.grid(row=0, column=0, sticky='w', pady=(0, 2))

    vf_dialogue_widget = tk.Text(
        dialogue_container,
        wrap='word',
        font=editor_font,
        bg=soft_active_bg,
        fg=theme["accent"],
        relief='solid',
        borderwidth=2,
        insertbackground='#1976d2',
        highlightbackground=soft_active_border,
        highlightcolor=soft_active_border
    )
    vf_dialogue_widget.grid(row=1, column=0, sticky='nsew', pady=(0, 5))
    vf_dialogue_widget.insert('1.0', part2_text)

    tk.Button(
        dialogue_container,
        text="Coller",
        command=lambda: paste_to_vf_dialogue(main_interface),
        bg=theme["button_primary_bg"],
        fg="#000000",
        font=('Segoe UI', 9, 'normal'),
        pady=4, padx=8
    ).grid(row=2, column=0, pady=5)

    # Pointeurs et mapping pour le switch visuel
    main_interface.vf_text_widget   = vf_speaker_widget
    main_interface.vf_text_widget_2 = vf_dialogue_widget
    main_interface.vf_part1_widgets = {'label': label_speaker,  'text': vf_speaker_widget}
    main_interface.vf_part2_widgets = {'label': label_dialogue, 'text': vf_dialogue_widget}
    main_interface.vf_split_mode = True
    main_interface.current_split_type = 'speaker_dialogue'

def copy_vo_text_simple(main_interface):
    """Copie le texte VO simple dans le presse-papier"""
    try:
        vo_text = main_interface.vo_text_widget.get('1.0', tk.END).strip()
        main_interface.window.clipboard_clear()
        main_interface.window.clipboard_append(vo_text)
        main_interface._update_status("Texte VO copié")
    except Exception as e:
        log_message("ERREUR", f"Erreur copie VO simple: {e}", category="realtime_editor")

def deepl_vo_text_simple(main_interface):
    """Copie le texte VO simple et ouvre DeepL"""
    try:
        vo_text = main_interface.vo_text_widget.get('1.0', tk.END).strip()
        copy_and_open_deepl(main_interface, vo_text, "VO simple")
    except Exception as e:
        log_message("ERREUR", f"Erreur DeepL VO simple: {e}", category="realtime_editor")

def paste_vf_text_simple(main_interface):
    """Colle le texte du presse-papier dans la zone VF simple"""
    try:
        clipboard_text = main_interface.window.clipboard_get()
        main_interface.vf_text_widget.delete('1.0', tk.END)
        main_interface.vf_text_widget.insert('1.0', clipboard_text)
        main_interface._update_status("Texte collé en VF")
    except Exception as e:
        log_message("ERREUR", f"Erreur collage VF simple: {e}", category="realtime_editor")

def paste_to_split_part1(main_interface):
    """Colle le texte du presse-papier dans la partie 1 du split"""
    try:
        clipboard_text = main_interface.window.clipboard_get()
        main_interface.vf_text_widget.delete('1.0', tk.END)
        main_interface.vf_text_widget.insert('1.0', clipboard_text)
        main_interface._update_status("Texte collé en partie 1")
    except Exception as e:
        log_message("ERREUR", f"Erreur collage split partie 1: {e}", category="realtime_editor")

def paste_to_split_part2(main_interface):
    """Colle le texte du presse-papier dans la partie 2 du split"""
    try:
        clipboard_text = main_interface.window.clipboard_get()
        if main_interface.vf_text_widget_2:
            main_interface.vf_text_widget_2.delete('1.0', tk.END)
            main_interface.vf_text_widget_2.insert('1.0', clipboard_text)
            main_interface._update_status("Texte collé en partie 2")
    except Exception as e:
        log_message("ERREUR", f"Erreur collage split partie 2: {e}", category="realtime_editor")

# Fonctions pour l'interface VO split (locuteur + dialogue séparés)

def copy_vo_speaker_text(main_interface):
    """Copie le texte du locuteur VO dans le presse-papier"""
    try:
        if hasattr(main_interface, 'vo_speaker_widget') and main_interface.vo_speaker_widget:
            speaker_text = main_interface.vo_speaker_widget.get('1.0', tk.END).strip()
            main_interface.window.clipboard_clear()
            main_interface.window.clipboard_append(speaker_text)
            main_interface._update_status("Locuteur VO copié")
    except Exception as e:
        log_message("ERREUR", f"Erreur copie locuteur VO: {e}", category="realtime_editor")

def deepl_vo_speaker_text(main_interface):
    """Copie le texte du locuteur VO et ouvre DeepL"""
    try:
        if hasattr(main_interface, 'vo_speaker_widget') and main_interface.vo_speaker_widget:
            speaker_text = main_interface.vo_speaker_widget.get('1.0', tk.END).strip()
            copy_and_open_deepl(main_interface, speaker_text, "locuteur VO")
    except Exception as e:
        log_message("ERREUR", f"Erreur DeepL locuteur VO: {e}", category="realtime_editor")

def copy_vo_dialogue_text(main_interface):
    """Copie le texte du dialogue VO dans le presse-papier"""
    try:
        vo_text = main_interface.vo_text_widget.get('1.0', tk.END).strip()
        main_interface.window.clipboard_clear()
        main_interface.window.clipboard_append(vo_text)
        main_interface._update_status("Dialogue VO copié")
    except Exception as e:
        log_message("ERREUR", f"Erreur copie dialogue VO: {e}", category="realtime_editor")

def deepl_vo_dialogue_text(main_interface):
    """Copie le texte du dialogue VO et ouvre DeepL"""
    try:
        vo_text = main_interface.vo_text_widget.get('1.0', tk.END).strip()
        copy_and_open_deepl(main_interface, vo_text, "dialogue VO")
    except Exception as e:
        log_message("ERREUR", f"Erreur DeepL dialogue VO: {e}", category="realtime_editor")

def paste_to_vf_speaker(main_interface):
    """Colle le texte du presse-papier dans la zone locuteur VF"""
    try:
        clipboard_text = main_interface.window.clipboard_get()
        main_interface.vf_text_widget.delete('1.0', tk.END)
        main_interface.vf_text_widget.insert('1.0', clipboard_text)
        main_interface._update_status("Texte collé en locuteur VF")
    except Exception as e:
        log_message("ERREUR", f"Erreur collage locuteur VF: {e}", category="realtime_editor")

def paste_to_vf_dialogue(main_interface):
    """Colle le texte du presse-papier dans la zone dialogue VF"""
    try:
        clipboard_text = main_interface.window.clipboard_get()
        if main_interface.vf_text_widget_2:
            main_interface.vf_text_widget_2.delete('1.0', tk.END)
            main_interface.vf_text_widget_2.insert('1.0', clipboard_text)
            main_interface._update_status("Texte collé en dialogue VF")
    except Exception as e:
        log_message("ERREUR", f"Erreur collage dialogue VF: {e}", category="realtime_editor")

def _build_multiple_dialogue_interface_with_individual_buttons(parent_container, main_interface, dialogue_group, is_detached=False):
    """Interface grille pour dialogues multiples avec boutons Copier/Coller sous chaque widget."""
    theme = theme_manager.get_theme()
    editor_font = ('Segoe UI', main_interface.editor_font_size_var.get())
    TEXT_AREA_HEIGHT = 200

    edit_main = tk.Frame(parent_container, bg=theme["bg"])

    if is_detached:
        edit_main.grid_rowconfigure(0, weight=1); edit_main.grid_rowconfigure(1, weight=0)
    else:
        edit_main.grid_rowconfigure(0, weight=0); edit_main.grid_rowconfigure(1, weight=1); edit_main.grid_rowconfigure(2, weight=0)

    edit_main.grid_columnconfigure(0, weight=40, minsize=200); edit_main.grid_columnconfigure(1, weight=60, minsize=300)

    text_areas_frame = tk.Frame(edit_main, bg=theme["bg"])
    text_areas_frame.grid(row=0, column=0, columnspan=2, sticky='nsew' if is_detached else 'ew')
    text_areas_frame.grid_columnconfigure(0, weight=40); text_areas_frame.grid_columnconfigure(1, weight=60)

    vo_grid_frame = tk.Frame(text_areas_frame, bg=theme["bg"]); vo_grid_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
    if not is_detached: vo_grid_frame.configure(height=TEXT_AREA_HEIGHT)
    tk.Label(vo_grid_frame, text="Textes Originaux", font=('Segoe UI', 10, 'bold'), bg=theme["bg"], fg=theme["fg"]).pack(anchor='w', pady=(0, 5))
    vo_grid_container = tk.Frame(vo_grid_frame, bg=theme["bg"]); vo_grid_container.pack(fill='both', expand=True)
    
    grid_rows, grid_cols = dialogue_group['grid_rows'], dialogue_group['grid_cols']
    for r in range(grid_rows): vo_grid_container.grid_rowconfigure(r, weight=1)
    for c in range(grid_cols): vo_grid_container.grid_columnconfigure(c, weight=1)
    
    main_interface.multiple_vo_widgets = []
    vo_dialogues = dialogue_group.get('vo_dialogues', [])
    for i in range(min(len(vo_dialogues), grid_rows * grid_cols)):
        row, col = i // grid_cols, i % grid_cols
        vo_dialogue_container = tk.Frame(vo_grid_container, bg=theme["bg"]); vo_dialogue_container.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        vo_dialogue_container.grid_rowconfigure(0, weight=0); vo_dialogue_container.grid_rowconfigure(1, weight=1); vo_dialogue_container.grid_rowconfigure(2, weight=0); vo_dialogue_container.grid_columnconfigure(0, weight=1)
        tk.Label(vo_dialogue_container, text=f"Original {i+1}", font=('Segoe UI', 9, 'bold'), bg=theme["bg"], fg=theme["fg"]).grid(row=0, column=0, sticky='w', padx=3, pady=(3, 2))
        # ✅ MODIFIÉ : Application du thème sombre au widget VO
        vo_widget = tk.Text(
            vo_dialogue_container,
            wrap='word',
            font=editor_font,
            bg=theme["entry_bg"],
            fg=theme["fg"],
            relief='solid',
            borderwidth=1,
            height=3,
            state='disabled',
            highlightbackground='#666666'
        )
        vo_widget.grid(row=1, column=0, sticky='nsew', padx=3, pady=2)
        vo_buttons_multiple_frame = tk.Frame(vo_dialogue_container, bg=theme["bg"])
        vo_buttons_multiple_frame.grid(row=2, column=0, padx=3, pady=(2, 3))

        tk.Button(
            vo_buttons_multiple_frame, text="Copier",
            command=lambda idx=i: copy_multiple_vo_text(main_interface, idx),
            bg=theme["button_utility_bg"], fg="#000000", font=('Segoe UI', 9), pady=4, padx=8
        ).pack(side='left', padx=(0, 5))

        tk.Button(
            vo_buttons_multiple_frame, text="DeepL",
            command=lambda idx=i: deepl_multiple_vo_text(main_interface, idx),
            bg=theme["button_tertiary_bg"], fg="#000000", font=('Segoe UI', 9), pady=4, padx=8
        ).pack(side='left', padx=(0, 5))

        # 👉 NOUVEAU : Google à côté de DeepL
        tk.Button(
            vo_buttons_multiple_frame, text="Google",
            command=lambda idx=i: _open_google_with_text(main_interface, main_interface.multiple_vo_widgets[idx].get('1.0', tk.END)),
            bg=theme.get("button_google_bg", theme["button_tertiary_bg"]), fg="#000000",
            font=('Segoe UI', 9), pady=4, padx=8
        ).pack(side='left')
        vo_widget.dialogue_info = vo_dialogues[i] if i < len(vo_dialogues) else {}; vo_widget.dialogue_index = i
        main_interface.multiple_vo_widgets.append(vo_widget)

    vf_grid_frame = tk.Frame(text_areas_frame, bg=theme["bg"]); vf_grid_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
    if not is_detached: vf_grid_frame.configure(height=TEXT_AREA_HEIGHT)
    tk.Label(vf_grid_frame, text=f"Traductions ({dialogue_group['group_size']} dialogues)", font=('Segoe UI', 10, 'bold'), bg=theme["bg"], fg=theme["fg"]).pack(anchor='w', pady=(0, 5))
    vf_grid_container = tk.Frame(vf_grid_frame, bg=theme["bg"]); vf_grid_container.pack(fill='both', expand=True)
    
    for r in range(grid_rows): vf_grid_container.grid_rowconfigure(r, weight=1)
    for c in range(grid_cols): vf_grid_container.grid_columnconfigure(c, weight=1)
    
    main_interface.multiple_vf_widgets = []
    dialogues = dialogue_group['dialogues']
    for i, dialogue in enumerate(dialogues):
        if i >= grid_rows * grid_cols: break
        row, col = i // grid_cols, i % grid_cols
        vf_dialogue_container = tk.Frame(vf_grid_container, bg=theme["bg"]); vf_dialogue_container.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        vf_dialogue_container.grid_rowconfigure(0, weight=0); vf_dialogue_container.grid_rowconfigure(1, weight=1); vf_dialogue_container.grid_rowconfigure(2, weight=0); vf_dialogue_container.grid_columnconfigure(0, weight=1)
        tk.Label(vf_dialogue_container, text=f"Traduction {i+1}", font=('Segoe UI', 9, 'bold'), bg=theme["bg"], fg=theme["fg"]).grid(row=0, column=0, sticky='w', padx=3, pady=(3, 2))
        # ✅ MODIFIÉ : Application du thème sombre au widget VF
        vf_widget = tk.Text(
            vf_dialogue_container,
            wrap='word',
            font=editor_font,
            bg=theme["entry_bg"],
            fg=theme["accent"],
            relief='solid',
            borderwidth=1,
            height=3,
            insertbackground='#1976d2',
            highlightbackground='#666666'
        )
        vf_widget.grid(row=1, column=0, sticky='nsew', padx=3, pady=2)
        tk.Button(vf_dialogue_container, text="Coller", command=lambda idx=i: paste_to_multiple_vf_text(main_interface, idx), bg=theme["button_primary_bg"], fg="#000000", font=('Segoe UI', 9, 'normal'), pady=4, padx=8).grid(row=2, column=0, padx=3, pady=(2, 3))
        vf_widget.dialogue_info = dialogue; vf_widget.dialogue_index = i
        main_interface.multiple_vf_widgets.append(vf_widget)
    # --- Boutons globaux ---
    buttons_frame = tk.Frame(edit_main, bg=theme["bg"])
    buttons_frame.grid(row=2 if not is_detached else 1, column=0, columnspan=2, sticky='ew', pady=(10, 0))

    # Frame pour aligner les boutons à droite
    right_buttons_frame = tk.Frame(buttons_frame, bg=theme["bg"])
    right_buttons_frame.pack(side='right')

    # Le bouton "Ouvrir" qui appelle maintenant la bonne fonction
    tk.Button(right_buttons_frame, text="Ouvrir", command=lambda: open_modified_file_for_multiple(main_interface), bg=theme["button_nav_bg"], fg="#000000", font=('Segoe UI', 9, 'normal'), pady=4, padx=8).pack(side='left', padx=(0, 5))

    # Le bouton "Enregistrer Tout"
    tk.Button(right_buttons_frame, text="Enregistrer Tout", command=lambda: save_multiple_translations(main_interface), bg=theme["button_secondary_bg"], fg="#000000", font=('Segoe UI', 9, 'normal'), pady=4, padx=8).pack(side='left')

    return edit_main

def copy_multiple_vo_text(main_interface, widget_index):
    """Copie le texte d'un widget VO spécifique dans la grille multiple"""
    try:
        if (hasattr(main_interface, 'multiple_vo_widgets') and widget_index < len(main_interface.multiple_vo_widgets)):
            vo_widget = main_interface.multiple_vo_widgets[widget_index]
            if vo_widget and vo_widget.winfo_exists():
                vo_text = vo_widget.get('1.0', tk.END).strip()
                main_interface.window.clipboard_clear()
                main_interface.window.clipboard_append(vo_text)
                main_interface._update_status(f"Original {widget_index + 1} copié")
    except Exception as e:
        log_message("ERREUR", f"Erreur copie VO multiple {widget_index}: {e}", category="realtime_editor")

def deepl_multiple_vo_text(main_interface, widget_index):
    """Copie le texte d'un widget VO spécifique et ouvre DeepL"""
    try:
        if (hasattr(main_interface, 'multiple_vo_widgets') and widget_index < len(main_interface.multiple_vo_widgets)):
            vo_widget = main_interface.multiple_vo_widgets[widget_index]
            if vo_widget and vo_widget.winfo_exists():
                vo_text = vo_widget.get('1.0', tk.END).strip()
                copy_and_open_deepl(main_interface, vo_text, f"original {widget_index + 1}")
    except Exception as e:
        log_message("ERREUR", f"Erreur DeepL VO multiple {widget_index}: {e}", category="realtime_editor")

def paste_to_multiple_vf_text(main_interface, widget_index):
    """Colle le texte du presse-papier dans un widget VF spécifique de la grille multiple"""
    try:
        if (hasattr(main_interface, 'multiple_vf_widgets') and widget_index < len(main_interface.multiple_vf_widgets)):
            vf_widget = main_interface.multiple_vf_widgets[widget_index]
            if vf_widget and vf_widget.winfo_exists():
                clipboard_text = main_interface.window.clipboard_get()
                vf_widget.delete('1.0', tk.END)
                vf_widget.insert('1.0', clipboard_text)
                main_interface._update_status(f"Texte collé en traduction {widget_index + 1}")
    except Exception as e:
        log_message("ERREUR", f"Erreur collage VF multiple {widget_index}: {e}", category="realtime_editor")

def toggle_split_mode(main_interface):
    """Bascule entre le mode d'édition simple et divisé."""
    try:
        _save_current_modification_if_changed(main_interface)
        if not main_interface.vf_split_mode:
            enable_split_mode(main_interface)
        else:
            disable_split_mode(main_interface)
    except Exception as e:
        log_message("ERREUR", f"Erreur toggle split mode: {e}", category="realtime_editor")

def enable_split_mode(main_interface):
    """Active le mode split avec Grid"""
    current_text = main_interface.vf_text_widget.get('1.0', tk.END).strip()
    mid_point = len(current_text) // 2
    for i in range(mid_point, min(len(current_text), mid_point + 20)):
        if current_text[i] == ' ':
            mid_point = i; break
    part1, part2 = current_text[:mid_point].strip(), current_text[mid_point:].strip()
    _create_split_vf_interface_with_grid_and_buttons(main_interface, part1, part2)
    main_interface.vf_split_mode = True
    main_interface.split_button.config(text="Fusionner")

def disable_split_mode(main_interface):
    """Désactive le mode split avec Grid"""
    part1 = main_interface.vf_text_widget.get('1.0', tk.END).strip()
    part2 = main_interface.vf_text_widget_2.get('1.0', tk.END).strip() if main_interface.vf_text_widget_2 else ""
    combined_text = f"{part1} {part2}".strip()
    _create_normal_vf_interface_with_grid_and_buttons(main_interface)
    main_interface.vf_text_widget.insert('1.0', combined_text)
    main_interface.vf_split_mode = False
    main_interface.split_button.config(text="Diviser")

def reset_font_size_to_default(main_interface):
    """Réinitialise la taille de la police de l'éditeur à 10pt."""
    main_interface.editor_font_size_var.set(10)
    update_editor_font_size(main_interface)

def detach_editor(main_interface):
    """Détache l'éditeur dans une fenêtre Toplevel en conservant l'affichage visible."""
    # Si déjà détaché : on met au premier plan
    if main_interface.detached_editor_window and main_interface.detached_editor_window.winfo_exists():
        main_interface.detached_editor_window.lift()
        main_interface.detached_editor_window.focus_force()
        return

    # --- SNAPSHOT de l'état visuel courant ---
    main_interface._editor_state_snapshot = _snapshot_editor_visible_state(main_interface)

    # Détruire le panneau intégré et masquer le frame
    if hasattr(main_interface, 'realtime_edit_main') and main_interface.realtime_edit_main.winfo_exists():
        main_interface.realtime_edit_main.destroy()
    main_interface.realtime_edit_frame.pack_forget()

    # Construire la fenêtre détachée
    window = tk.Toplevel(main_interface.window)
    window.title("Éditeur Temps Réel")
    window.geometry("1200x300")
    window.minsize(500, 200)
    main_interface.detached_editor_window = window

    main_interface.realtime_edit_main = _build_editor_panel(window, main_interface, is_detached=True)
    main_interface.realtime_edit_main.pack(fill='both', expand=True, padx=10, pady=10)

    # --- RESTORE de l'état visuel ---
    _restore_editor_visible_state(main_interface, getattr(main_interface, "_editor_state_snapshot", None))

    window.protocol("WM_DELETE_WINDOW", lambda: on_editor_close(main_interface))


def on_editor_close(main_interface):
    """Ré-attache l'éditeur à l'onglet principal en conservant l'affichage visible."""
    window = main_interface.detached_editor_window
    if not window or not window.winfo_exists():
        return

    # --- SNAPSHOT avant destruction de la fenêtre détachée ---
    main_interface._editor_state_snapshot = _snapshot_editor_visible_state(main_interface)

    # Détruire le contenu de la fenêtre détachée
    if hasattr(main_interface, 'realtime_edit_main') and main_interface.realtime_edit_main.winfo_exists():
        main_interface.realtime_edit_main.destroy()

    # Recréer l'UI intégrée
    main_interface.realtime_edit_frame.pack(fill='both', expand=True, padx=20, pady=10)
    main_interface.realtime_edit_main = _build_editor_panel(main_interface.realtime_edit_frame, main_interface, is_detached=False)
    main_interface.realtime_edit_main.pack(fill='both', expand=True, padx=15, pady=15)

    # --- RESTORE de l'état visuel ---
    _restore_editor_visible_state(main_interface, getattr(main_interface, "_editor_state_snapshot", None))

    # Nettoyage
    window.destroy()
    main_interface.detached_editor_window = None


def install_monitoring_module(main_interface):
    """Installe le module de surveillance dans le projet Ren'Py."""
    try:
        if not main_interface.current_project_path:
            main_interface._show_notification("Veuillez sélectionner un projet Ren'Py", "warning"); return
        language = main_interface.realtime_language_var.get().strip().lower()
        if not language:
            main_interface._show_notification("Veuillez spécifier une langue cible", "warning"); return
        
        main_interface._update_status("Installation du module de surveillance...")
        biz = main_interface._get_realtime_editor_business()
        result = biz.generate_monitoring_module(project_path=main_interface.current_project_path, language=language)
        
        if result.get('success'):
            module_path = result.get('module_path', '')
            main_interface._update_status(f"Module installé avec succès pour '{language}'")
            log_message("INFO", f"Module de surveillance installé: {module_path}", category="realtime_editor")
        else:
            error_message = " / ".join(result.get('errors', ["Erreur inconnue"]))
            main_interface._update_status("Erreur installation module")
            main_interface._show_notification(f"Erreur installation: {error_message}", "error")
            log_message("ERREUR", f"Erreur installation module surveillance: {error_message}", category="realtime_editor")
    except Exception as e:
        main_interface._update_status("Erreur installation module")
        main_interface._show_notification(f"Erreur critique installation: {e}", "error")
        log_message("ERREUR", f"Erreur critique installation module: {e}", category="realtime_editor")

def start_monitoring(main_interface):
    """Démarre la surveillance des dialogues du jeu."""
    try:
        if not main_interface.current_project_path:
            main_interface._show_notification("Aucun projet sélectionné", "warning"); return
        
        language = main_interface.realtime_language_var.get().strip().lower()
        biz = main_interface._get_realtime_editor_business()
        biz.set_callbacks(
            dialogue_callback=lambda info: main_interface.window.after(0, update_dialogue_interface, main_interface, info),
            status_callback=main_interface._update_status,
            error_callback=main_interface._show_notification
        )
        result = biz.start_monitoring(main_interface.current_project_path, language)

        if result.get('success'):
            # --- NOUVEAU : enregistrer le callback de focus (compat: alias set_dialogue_callback) ---
            try:
                if not getattr(main_interface, "_focus_cb_registered", False):
                    # Le callback s’exécute TOUJOURS sur le thread Tk via after(0)
                    def _focus_cb():
                        try:
                            main_interface.window.after(0, lambda: _bring_realtime_editor_to_front(main_interface))
                        except Exception:
                            pass
                    # Alias conservé (ne change pas votre code ailleurs)
                    set_dialogue_callback(_focus_cb)
                    main_interface._focus_cb_registered = True
                    log_message("INFO", "Callback de focus (F8) enregistré.", category="realtime_editor")
            except Exception as e_cb:
                log_message("ATTENTION", f"Impossible d'enregistrer le callback de focus: {e_cb}", category="realtime_editor")
            # -----------------------------------------------------------------------------------------

            main_interface.monitor_status_label.config(text="🟢 Surveillance active", fg='#28a745')
            main_interface.monitoring_active = True
            main_interface.start_monitor_btn.config(state='disabled')
            main_interface.stop_monitor_btn.config(state='normal')
            main_interface.window.after(1000, lambda: check_and_offer_recovery(main_interface))
            log_message("INFO", "Appel de démarrage surveillance UI réussi", category="realtime_editor")
        else:
            main_interface._show_notification(" / ".join(result.get('errors', ["Erreur inconnue"])), "error")
    except Exception as e:
        main_interface._show_notification(f"Erreur démarrage: {e}", "error")
        log_message("ERREUR", f"Erreur critique démarrage surveillance: {e}", category="realtime_editor")

def stop_monitoring(main_interface):
   """Arrête la surveillance et gère les modifications en attente."""
   try:
       biz = main_interface._get_realtime_editor_business()
       if biz.has_pending_modifications():
           response = _ask_save_pending_modifications(main_interface)
           if response == 'cancel': return
           elif response == 'yes':
               save_result = biz.save_all_pending_modifications(main_interface.current_project_path)
               if not save_result.get('success'):
                   main_interface._show_notification("Erreur sauvegarde, arrêt annulé", "error"); return

       result = biz.stop_monitoring()
       if result.get('success'):
           main_interface.monitor_status_label.config(text="⭕ Surveillance arrêtée", fg='#dc3545')
           main_interface.monitoring_active = False
           main_interface.start_monitor_btn.config(state='normal')
           main_interface.stop_monitor_btn.config(state='disabled')
           log_message("INFO", "Appel d'arrêt surveillance UI réussi", category="realtime_editor")
       else:
           main_interface._show_notification(" / ".join(result.get('errors', ["Erreur inconnue"])), "error")
   except Exception as e:
       main_interface._show_notification(f"Erreur arrêt: {e}", "error")
       log_message("ERREUR", f"Erreur critique arrêt surveillance: {e}", category="realtime_editor")

def _ask_save_pending_modifications(main_interface):
    """Affiche une boîte de dialogue pour sauvegarder les modifications en attente."""
    try:
        biz = main_interface._get_realtime_editor_business()
        summary = biz.get_pending_modifications_summary()
        count = summary['total_count']
        if count == 0: return 'no'
        
        message_parts = [f"{count} modification{'s' if count > 1 else ''} en attente :"]
        by_type = summary['by_type']
        for mod_type, type_count in by_type.items():
            type_name = {'simple': 'Modifications simples', 'split': 'Divisions', 'speaker_dialogue': 'Locuteur + dialogue', 'merge': 'Fusions'}.get(mod_type, f'Type {mod_type}')
            message_parts.append(f"  • {type_count} {type_name}")
        message_parts.append("\nVoulez-vous les sauvegarder ?")
        
        result = show_custom_askyesnocancel("Modifications en attente", "\n".join(message_parts), theme_manager.get_theme(), parent=main_interface.window)
        if result is True: return 'yes'
        elif result is False: return 'no'
        else: return 'cancel'
    except Exception as e:
        log_message("ERREUR", f"Erreur dialog sauvegarde: {e}", category="realtime_editor"); return 'no'

def _update_highlight_for_split_dialogue(main_interface, new_part_number):
    """Met à jour la surbrillance de l'interface VF split (labels + zones) en mode doux (gris)."""
    try:
        if not getattr(main_interface, 'vf_split_mode', False):
            return
        if not hasattr(main_interface, 'vf_part1_widgets') or not hasattr(main_interface, 'vf_part2_widgets'):
            return

        theme = theme_manager.get_theme()
        soft_active_bg     = theme.get("soft_active_bg", '#2f3338')
        soft_active_border = theme.get("soft_active_border", '#8a9099')
        active_label_fg    = theme.get("active_label_fg", theme["fg"])

        normal_bg_label = theme["bg"]
        normal_fg_label = theme["fg"]
        normal_bg_text  = theme["entry_bg"]
        normal_border   = '#666666'

        def apply(target, active: bool):
            target['label'].config(
                font=('Segoe UI', 9, 'bold' if active else 'normal'),
                bg=soft_active_bg if active else normal_bg_label,
                fg=active_label_fg if active else normal_fg_label
            )
            target['text'].config(
                bg=soft_active_bg if active else normal_bg_text,
                fg=theme["accent"],
                relief='solid',
                borderwidth=2 if active else 1,
                highlightbackground=soft_active_border if active else normal_border,
                highlightcolor=soft_active_border if active else normal_border,
                insertbackground='#1976d2'
            )

        apply(main_interface.vf_part1_widgets, new_part_number == 1)
        apply(main_interface.vf_part2_widgets, new_part_number == 2)

    except Exception as e:
        log_message("ATTENTION", f"Erreur mise à jour surbrillance: {e}", category="realtime_editor")

def update_dialogue_interface(main_interface, dialogue_info: Dict):
    """
    *** VERSION FINALE AVEC TRANSITION BIDIRECTIONNELLE ***
    Gère tous les cas : dialogues simples, complexes, menus, multiples et les transitions entre eux.
    """
    try:
        # Bloc de contrôle pour ignorer les lignes consécutives (inchangé)
        if (hasattr(main_interface, 'current_dialogue_info') and
                main_interface.current_dialogue_info and
                not main_interface.current_dialogue_info.get('is_menu') and
                not dialogue_info.get('is_menu')):
            prev_info = main_interface.current_dialogue_info
            if prev_info.get('tl_file') == dialogue_info.get('tl_file') and \
               dialogue_info.get('tl_line') == prev_info.get('tl_line', 0) + 1:
                main_interface.current_dialogue_info = dialogue_info
                dialogue_structure = _analyze_dialogue_structure(main_interface, dialogue_info)
                new_part_number = dialogue_structure.get('part_number', 1)
                _update_highlight_for_split_dialogue(main_interface, new_part_number)
                return

        if hasattr(main_interface, 'current_dialogue_info') and main_interface.current_dialogue_info:
            if not main_interface.current_dialogue_info.get('is_menu', False):
                _save_current_modification_if_changed(main_interface)

        # --- DÉBUT DE LA LOGIQUE DE TRANSITION CORRIGÉE ---
        was_in_menu = getattr(main_interface, 'is_in_menu_mode', False)
        was_in_multiple = getattr(main_interface, 'is_in_multiple_mode', False)

        is_currently_menu = dialogue_info.get('is_menu', False)
        is_currently_multiple = dialogue_info.get('is_multiple_group', False)

        main_interface.is_in_menu_mode = is_currently_menu
        main_interface.is_in_multiple_mode = is_currently_multiple

        # On reconstruit l'interface si on sort d'un mode spécial (Menu OU Multiple)
        if (was_in_menu and not is_currently_menu) or (was_in_multiple and not is_currently_multiple):
            if hasattr(main_interface, 'realtime_edit_main') and main_interface.realtime_edit_main.winfo_exists():
                main_interface.realtime_edit_main.destroy()

            # <-- LA LIGNE CRUCIALE À AJOUTER EST ICI -->
            main_interface.current_multiple_group = None # On réinitialise l'état du groupe multiple

            # Réinitialisation des listes de widgets spécifiques
            if hasattr(main_interface, 'menu_vo_widgets'): main_interface.menu_vo_widgets = []
            if hasattr(main_interface, 'menu_vf_widgets'): main_interface.menu_vf_widgets = []
            if hasattr(main_interface, 'multiple_vo_widgets'): main_interface.multiple_vo_widgets = []
            if hasattr(main_interface, 'multiple_vf_widgets'): main_interface.multiple_vf_widgets = []
            
            is_detached = bool(main_interface.detached_editor_window and main_interface.detached_editor_window.winfo_exists())
            parent = main_interface.detached_editor_window or main_interface.realtime_edit_frame
            main_interface.realtime_edit_main = _build_editor_panel(parent, main_interface, is_detached)
            main_interface.realtime_edit_main.pack(fill='both', expand=True, padx=15, pady=15)
        # --- FIN DE LA LOGIQUE DE TRANSITION ---

        # Aiguillage principal (inchangé)
        if is_currently_menu:
            _update_for_menu_choices(main_interface, dialogue_info)
        elif is_currently_multiple:
            _update_for_multiple_dialogue(main_interface, dialogue_info)
        else:
            dialogue_structure = _analyze_dialogue_structure(main_interface, dialogue_info)
            original_text = dialogue_info.get('original_text', "")
            if dialogue_structure.get('split_type') == 'speaker_dialogue':
                vo_type_analysis = _analyze_original_text_type(original_text, dialogue_structure)
                _handle_unnamed_speaker_update(main_interface, vo_type_analysis, dialogue_structure)
            elif dialogue_structure.get('is_split') and dialogue_structure.get('split_type') == 'multiline':
                vo_type_analysis = {'type': 'multiline', 'dialogue': original_text}
                _handle_multiline_update(main_interface, vo_type_analysis, dialogue_structure, original_text)
            else:
                vo_type_analysis = _analyze_original_text_type(original_text, {})
                _handle_simple_dialogue_update(main_interface, vo_type_analysis, original_text, dialogue_info)

        main_interface.current_dialogue_info = dialogue_info
        _update_pending_status(main_interface)

    except Exception as e:
        log_message("ERREUR", f"Erreur mise à jour interface: {e}", category="realtime_editor")

def _update_for_menu_choices(main_interface, menu_info: Dict):
    """Gère l'affichage des choix de menu"""
    main_interface.current_menu_choices = menu_info
    
    # Détruire l'interface actuelle
    if hasattr(main_interface, 'realtime_edit_main') and main_interface.realtime_edit_main.winfo_exists():
        main_interface.realtime_edit_main.destroy()
    
    # Créer la nouvelle interface pour les choix
    is_detached = bool(main_interface.detached_editor_window and main_interface.detached_editor_window.winfo_exists())
    parent = main_interface.detached_editor_window or main_interface.realtime_edit_frame
    main_interface.realtime_edit_main = _build_menu_choices_interface(parent, main_interface, menu_info, is_detached)
    main_interface.realtime_edit_main.pack(fill='both', expand=True, padx=15, pady=15)

def _build_menu_choices_interface(parent_container, main_interface, menu_info, is_detached=False):
    """
    Construit l'interface pour les choix de menu en utilisant une grille harmonisée
    avec l'affichage des dialogues multiples.
    """
    theme = theme_manager.get_theme()
    editor_font = ('Segoe UI', main_interface.editor_font_size_var.get())
    
    edit_main = tk.Frame(parent_container, bg=theme["bg"])

    # --- Titre principal ---
    title_frame = tk.Frame(edit_main, bg=theme["bg"])
    title_frame.pack(fill='x', pady=(0, 5), padx=5)
    choices = menu_info.get('choices', [])
    tk.Label(
        title_frame,
        text=f"📋 Menu de choix ({len(choices)} options)",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"], fg=theme["fg"]
    ).pack(side='left')

    # --- Conteneur principal pour les grilles VO et VF ---
    text_areas_frame = tk.Frame(edit_main, bg=theme["bg"])
    text_areas_frame.pack(fill='both', expand=True)
    text_areas_frame.grid_columnconfigure(0, weight=1)
    text_areas_frame.grid_columnconfigure(1, weight=1)

    # --- Colonne gauche : VO ---
    vo_grid_frame = tk.Frame(text_areas_frame, bg=theme["bg"])
    vo_grid_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
    tk.Label(vo_grid_frame, text="Choix Originaux (VO)", font=('Segoe UI', 10, 'bold'),
             bg=theme["bg"], fg=theme["fg"]).pack(anchor='w', pady=(0, 5))
    vo_grid_container = tk.Frame(vo_grid_frame, bg=theme["bg"])
    vo_grid_container.pack(fill='both', expand=True)

    # --- Colonne droite : VF ---
    vf_grid_frame = tk.Frame(text_areas_frame, bg=theme["bg"])
    vf_grid_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
    lang_name = main_interface.realtime_language_var.get().title()
    tk.Label(vf_grid_frame, text=f"Traductions ({lang_name})", font=('Segoe UI', 10, 'bold'),
             bg=theme["bg"], fg=theme["fg"]).pack(anchor='w', pady=(0, 5))
    vf_grid_container = tk.Frame(vf_grid_frame, bg=theme["bg"])
    vf_grid_container.pack(fill='both', expand=True)

    # --- Grille 2 colonnes ---
    grid_cols = 2
    grid_rows = (len(choices) + 1) // grid_cols
    for r in range(grid_rows):
        vo_grid_container.grid_rowconfigure(r, weight=1)
        vf_grid_container.grid_rowconfigure(r, weight=1)
    for c in range(grid_cols):
        vo_grid_container.grid_columnconfigure(c, weight=1)
        vf_grid_container.grid_columnconfigure(c, weight=1)

    main_interface.menu_vo_widgets, main_interface.menu_vf_widgets = [], []

    # --- Items ---
    for i, choice in enumerate(choices):
        row, col = i // grid_cols, i % grid_cols

        # VO
        vo_container = tk.Frame(vo_grid_container, bg=theme["bg"])
        vo_container.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        vo_container.grid_rowconfigure(1, weight=1)
        vo_container.grid_columnconfigure(0, weight=1)

        tk.Label(vo_container, text=f"Choix {i+1}", font=('Segoe UI', 9, 'normal'),
                 bg=theme["bg"], fg=theme["fg"]).grid(row=0, column=0, sticky='w', padx=3, pady=(3, 2))

        vo_text = tk.Text(
            vo_container, wrap='word', font=editor_font,
            bg=theme["entry_bg"], fg=theme["fg"],
            relief='solid', borderwidth=1, height=3, state='disabled',
            highlightbackground='#666666'
        )
        vo_text.grid(row=1, column=0, sticky='nsew', padx=3, pady=2)
        vo_text.config(state='normal'); vo_text.insert('1.0', choice.get('original_text', '')); vo_text.config(state='disabled')
        main_interface.menu_vo_widgets.append(vo_text)

        vo_buttons = tk.Frame(vo_container, bg=theme["bg"])
        vo_buttons.grid(row=2, column=0, padx=3, pady=(2, 3))

        tk.Button(
            vo_buttons, text="Copier",
            command=lambda idx=i: copy_menu_choice_vo(main_interface, idx),
            bg=theme["button_utility_bg"], fg="#000000", font=('Segoe UI', 9), pady=4, padx=8
        ).pack(side='left', padx=(0, 5))

        tk.Button(
            vo_buttons, text="DeepL",
            command=lambda idx=i: deepl_menu_choice_vo(main_interface, idx),
            bg=theme["button_tertiary_bg"], fg="#000000", font=('Segoe UI', 9), pady=4, padx=8
        ).pack(side='left', padx=(0, 5))

        # 👉 NOUVEAU : Google à côté de DeepL
        tk.Button(
            vo_buttons, text="Google",
            command=lambda idx=i: _open_google_with_text(main_interface, main_interface.menu_vo_widgets[idx].get('1.0', tk.END)),
            bg=theme.get("button_google_bg", theme["button_tertiary_bg"]), fg="#000000",
            font=('Segoe UI', 9), pady=4, padx=8
        ).pack(side='left')

        # VF
        vf_container = tk.Frame(vf_grid_container, bg=theme["bg"])
        vf_container.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        vf_container.grid_rowconfigure(1, weight=1)
        vf_container.grid_columnconfigure(0, weight=1)

        tk.Label(vf_container, text=f"Traduction {i+1}", font=('Segoe UI', 9, 'normal'),
                 bg=theme["bg"], fg=theme["fg"]).grid(row=0, column=0, sticky='w', padx=3, pady=(3, 2))

        vf_text = tk.Text(
            vf_container, wrap='word', font=editor_font,
            bg=theme["entry_bg"], fg=theme["accent"],
            relief='solid', borderwidth=1, height=3,
            insertbackground='#1976d2', highlightbackground='#666666'
        )
        vf_text.grid(row=1, column=0, sticky='nsew', padx=3, pady=2)
        translated_text = choice.get('translated_text', '')
        vf_text.insert('1.0', '' if translated_text == choice.get('original_text') else translated_text)
        vf_text.choice_info = choice
        main_interface.menu_vf_widgets.append(vf_text)

        tk.Button(vf_container, text="Coller", command=lambda idx=i: paste_menu_choice_vf(main_interface, idx),
                  bg=theme["button_primary_bg"], fg="#000000", font=('Segoe UI', 9), pady=4, padx=8).grid(row=2, column=0, padx=3, pady=(2, 3))

    # --- Boutons globaux ---
    buttons_frame = tk.Frame(edit_main, bg=theme["bg"])
    buttons_frame.pack(fill='x', pady=(10, 0))

    right_buttons_frame = tk.Frame(buttons_frame, bg=theme["bg"])
    right_buttons_frame.pack(side='right')

    tk.Button(right_buttons_frame, text="Ouvrir", command=lambda: open_modified_file_for_menu(main_interface),
              bg=theme["button_nav_bg"], fg="#000000", font=('Segoe UI', 9), pady=4, padx=8).pack(side='left', padx=(0, 5))

    tk.Button(right_buttons_frame, text="Enregistrer Tous les Choix", command=lambda: save_all_menu_choices(main_interface),
              bg=theme["button_secondary_bg"], fg="#000000", font=('Segoe UI', 9), pady=4, padx=8).pack(side='left')

    main_interface.is_in_menu_mode = True
    return edit_main

def deepl_menu_choice_vo(main_interface, index):
    """Copie et ouvre DeepL pour un choix"""
    try:
        if index < len(main_interface.menu_vo_widgets):
            vo_text = main_interface.menu_vo_widgets[index].get('1.0', tk.END).strip()
            copy_and_open_deepl(main_interface, vo_text, f"choix {index + 1}")
    except Exception as e:
        log_message("ERREUR", f"Erreur DeepL choix: {e}", category="realtime_editor")

# Fonctions helper pour les choix de menu
def copy_menu_choice_vo(main_interface, index):
    """Copie le texte VO d'un choix"""
    try:
        if index < len(main_interface.menu_vo_widgets):
            vo_text = main_interface.menu_vo_widgets[index].get('1.0', tk.END).strip()
            main_interface.window.clipboard_clear()
            main_interface.window.clipboard_append(vo_text)
            main_interface._update_status(f"Choix {index + 1} VO copié")
    except Exception as e:
        log_message("ERREUR", f"Erreur copie choix VO: {e}", category="realtime_editor")

def paste_menu_choice_vf(main_interface, index):
    """Colle le texte dans un choix VF"""
    try:
        if index < len(main_interface.menu_vf_widgets):
            clipboard_text = main_interface.window.clipboard_get()
            vf_widget = main_interface.menu_vf_widgets[index]
            vf_widget.delete('1.0', tk.END)
            vf_widget.insert('1.0', clipboard_text)
            main_interface._update_status(f"Texte collé dans choix {index + 1}")
    except Exception as e:
        log_message("ERREUR", f"Erreur collage choix VF: {e}", category="realtime_editor")

def save_all_menu_choices(main_interface):
    """Sauvegarde tous les choix modifiés"""
    try:
        if not hasattr(main_interface, 'menu_vf_widgets'):
            main_interface._show_notification("Aucun choix à sauvegarder", "warning")
            return
        
        biz = main_interface._get_realtime_editor_business()
        saved_count = 0
        error_count = 0
        
        for i, vf_widget in enumerate(main_interface.menu_vf_widgets):
            if vf_widget and vf_widget.winfo_exists():
                try:
                    new_text = vf_widget.get('1.0', tk.END).strip()
                    choice_info = vf_widget.choice_info
                    
                    # Vérifier s'il y a eu une modification
                    if new_text != choice_info.get('translated_text', ''):
                        result = biz.save_choice_translation(
                            choice_info,
                            new_text,
                            main_interface.current_project_path
                        )
                        
                        if result.get('success'):
                            saved_count += 1
                            # Mettre à jour le texte original dans les infos
                            choice_info['translated_text'] = new_text
                        else:
                            error_count += 1
                            
                except Exception as e:
                    error_count += 1
                    log_message("ERREUR", f"Erreur sauvegarde choix {i+1}: {e}", category="realtime_editor")
        
        if saved_count > 0:
            main_interface._update_status(f"{saved_count} choix sauvegardés")
            main_interface._show_notification(
                f"{saved_count} choix sauvegardés !\nAppuyez sur Maj+R dans le jeu pour voir les changements.",
                "success"
            )
        elif error_count > 0:
            main_interface._show_notification(f"Erreurs lors de la sauvegarde", "error")
        else:
            main_interface._show_notification("Aucune modification détectée", "info")
            
    except Exception as e:
        log_message("ERREUR", f"Erreur sauvegarde choix: {e}", category="realtime_editor")
        main_interface._show_notification(f"Erreur: {e}", "error")

# ### REFACTORISATION ###: Nouvelle fonction pour gérer les dialogues multiples
def _update_for_multiple_dialogue(main_interface, dialogue_info):
    """Gère la mise à jour de l'UI pour un groupe de dialogues multiples."""
    main_interface.current_multiple_group = dialogue_info
    
    if hasattr(main_interface, 'realtime_edit_main') and main_interface.realtime_edit_main.winfo_exists():
        main_interface.realtime_edit_main.destroy()
    
    is_detached = main_interface.detached_editor_window and main_interface.detached_editor_window.winfo_exists()
    parent = main_interface.detached_editor_window if is_detached else main_interface.realtime_edit_frame
            
    main_interface.realtime_edit_main = _build_editor_panel(parent, main_interface, is_detached)
    main_interface.realtime_edit_main.pack(fill='both', expand=True, padx=15, pady=15)
    
    _populate_multiple_widgets_separated(main_interface, dialogue_info)

# ### REFACTORISATION ###: Fonction spécialisée pour le cas "Locuteur non défini"
def _handle_unnamed_speaker_update(main_interface, dialogue_type, dialogue_structure):
    """Met à jour l'UI pour un dialogue de type 'locuteur' 'dialogue'."""
    # Récupérer les textes originaux (VO)
    original_full_text = main_interface.current_dialogue_info.get('original_text', '')
    
    # Si on a le texte original complet, l'analyser pour séparer locuteur/dialogue
    if original_full_text and '"' in original_full_text:
        import re
        quote_matches = re.findall(r'"((?:\\.|[^"])*)"', original_full_text)
        if len(quote_matches) >= 2:
            vo_speaker = quote_matches[0]
            vo_dialogue = quote_matches[1]
        else:
            vo_speaker = dialogue_type.get('speaker', 'Locuteur')
            vo_dialogue = dialogue_type.get('dialogue', original_full_text.strip('"'))
    else:
        vo_speaker = dialogue_type.get('speaker', 'Locuteur')
        vo_dialogue = dialogue_type.get('dialogue', '')
    
    # Créer l'interface VO split
    _create_split_vo_interface_for_unnamed_speaker_with_grid_and_buttons(
        main_interface, 
        vo_speaker, 
        vo_dialogue
    )
    
    # Créer l'interface VF split avec les traductions
    _create_split_vf_interface_for_unnamed_speaker_with_grid_and_buttons(
        main_interface, 
        dialogue_structure.get('part1_text', ''),  # Traduction du locuteur
        dialogue_structure.get('part2_text', '')   # Traduction du dialogue
    )

# ### REFACTORISATION ###: Fonction spécialisée pour le cas "Dialogue multi-lignes"
def _handle_multiline_update(main_interface, dialogue_type, dialogue_structure, original_text):
    """Met à jour l'UI pour un dialogue divisé sur plusieurs lignes."""
    if getattr(main_interface, 'vo_split_mode', False):
        _create_normal_vo_interface_with_grid(main_interface)
    
    # Récupérer le vrai texte original (VO)
    vo_display_text = main_interface.current_dialogue_info.get('original_text', original_text)
    if not vo_display_text or vo_display_text == main_interface.current_dialogue_info.get('displayed_text', ''):
        vo_display_text = _get_clean_vo_display_text(dialogue_type, original_text)
    
    # Afficher le texte VO
    if hasattr(main_interface, 'vo_text_widget') and main_interface.vo_text_widget.winfo_exists():
        main_interface.vo_text_widget.config(state='normal')
        main_interface.vo_text_widget.delete('1.0', tk.END)
        main_interface.vo_text_widget.insert('1.0', vo_display_text)
        main_interface.vo_text_widget.config(state='disabled')
    
    # Créer l'interface VF split avec les parties traduites
    _create_split_vf_interface_with_grid_and_buttons(
        main_interface,
        dialogue_structure.get('part1_text', ''),
        dialogue_structure.get('part2_text', ''),
        dialogue_structure.get('part_number', 1),
        dialogue_structure.get('total_parts', 2),
        'multiline'
    )

# ### REFACTORISATION ###: Fonction spécialisée pour le cas "Dialogue simple"
def _handle_simple_dialogue_update(main_interface, dialogue_type, original_text, dialogue_info):
    """Met à jour l'UI pour un dialogue simple avec VO/VF distincts."""
    if getattr(main_interface, 'vo_split_mode', False):
        _create_normal_vo_interface_with_grid(main_interface)
    
    # Récupérer le vrai texte original (VO) depuis dialogue_info
    vo_display_text = dialogue_info.get('original_text', original_text)
    if not vo_display_text or vo_display_text == dialogue_info.get('displayed_text', ''):
        vo_display_text = _get_clean_vo_display_text(dialogue_type, original_text)
    
    # Afficher le texte VO
    if hasattr(main_interface, 'vo_text_widget') and main_interface.vo_text_widget.winfo_exists():
        main_interface.vo_text_widget.config(state='normal')
        main_interface.vo_text_widget.delete('1.0', tk.END)
        main_interface.vo_text_widget.insert('1.0', vo_display_text)
        main_interface.vo_text_widget.config(state='disabled')
    
    _create_normal_vf_interface_with_grid_and_buttons(main_interface)
    
    # Afficher le texte VF (traduit)
    if hasattr(main_interface, 'vf_text_widget') and main_interface.vf_text_widget.winfo_exists():
        main_interface.vf_text_widget.delete('1.0', tk.END)
        # Utiliser le texte traduit réel
        translated_text = dialogue_info.get('translated_text', dialogue_info.get('displayed_text', ''))
        main_interface.vf_text_widget.insert('1.0', translated_text)

def _get_clean_vo_display_text(dialogue_type, original_text):
    """Génère le texte VO propre pour l'affichage"""
    if dialogue_type['type'] == 'named_speaker':
        return f"{dialogue_type['speaker']}: {dialogue_type['dialogue']}"
    elif dialogue_type['type'] in ['split_multiline', 'simple']:
        return dialogue_type['dialogue']
    else:
        return original_text.strip('"')

def _analyze_original_text_type(original_text: str, dialogue_structure: Dict) -> Dict[str, Any]:
    """Analyse le type de dialogue original en ignorant les guillemets échappés."""
    try:
        import re
        if dialogue_structure.get('is_split', False):
            split_type = dialogue_structure.get('split_type', 'normal')
            if split_type == 'speaker_dialogue':
                quote_matches = re.findall(r'(?<!\\)"([^"]*?)(?<!\\)"', original_text)
                if len(quote_matches) >= 2: return {'type': 'unnamed_speaker', 'speaker': quote_matches[0], 'dialogue': quote_matches[1]}
                else: return {'type': 'unnamed_speaker', 'speaker': 'Non défini', 'dialogue': original_text.strip('"')}
            elif split_type == 'multiline':
                return {'type': 'split_multiline', 'dialogue': original_text.strip('"')}
        
        temp_text = original_text.replace('\\"', '§ESCAPED_QUOTE§')
        quote_matches = [match.replace('§ESCAPED_QUOTE§', '\\"') for match in re.findall(r'"([^"]*)"', temp_text)]
        
        if len(quote_matches) == 2:
            first_quote_end = temp_text.find('"' + quote_matches[0].replace('\\"', '§ESCAPED_QUOTE§') + '"') + len(quote_matches[0]) + 2
            second_quote_start = temp_text.find('"' + quote_matches[1].replace('\\"', '§ESCAPED_QUOTE§') + '"', first_quote_end)
            if second_quote_start - first_quote_end > 0:
                return {'type': 'unnamed_speaker', 'speaker': quote_matches[0], 'dialogue': quote_matches[1]}
        
        if len(quote_matches) == 1:
            dialogue_text = quote_matches[0]
            before_quotes = re.sub(r'"[^"]*"', '', temp_text).strip()
            if before_quotes and not before_quotes.startswith('#'):
                return {'type': 'named_speaker', 'speaker': before_quotes, 'dialogue': dialogue_text}
            else: return {'type': 'simple', 'dialogue': dialogue_text}
        else: return {'type': 'simple', 'dialogue': original_text.strip('"')}
    except Exception as e:
        log_message("ERREUR", f"Erreur analyse type: {e}", category="realtime_editor")
        return {'type': 'simple', 'dialogue': original_text.strip('"')}

def init_multiple_support(main_interface):
    """Initialise le support des dialogues multiples"""
    if not hasattr(main_interface, 'current_multiple_group'): main_interface.current_multiple_group = None
    if not hasattr(main_interface, 'multiple_vf_widgets'): main_interface.multiple_vf_widgets = []
    if not hasattr(main_interface, 'multiple_vo_widgets'): main_interface.multiple_vo_widgets = []

def _populate_multiple_widgets_separated(main_interface, dialogue_info):
    """Remplit les widgets multiples VO et VF avec leurs contenus respectifs"""
    try:
        vo_dialogues = dialogue_info.get('vo_dialogues', [])
        vf_dialogues = dialogue_info.get('vf_dialogues', [])
        
        # Widgets VO - Afficher les textes originaux
        if hasattr(main_interface, 'multiple_vo_widgets'):
            for i, vo_widget in enumerate(main_interface.multiple_vo_widgets):
                if i < len(vo_dialogues) and vo_widget and vo_widget.winfo_exists():
                    # Récupérer le texte original depuis vo_dialogues
                    vo_dialogue_data = vo_dialogues[i]
                    original_text = vo_dialogue_data.get('original_text', vo_dialogue_data.get('dialogue_text', ''))
                    
                    # Si pas de texte original distinct, utiliser le système de formatage
                    if not original_text or original_text == vo_dialogue_data.get('dialogue_text', ''):
                        formatted_text = _format_vo_text_for_display(vo_dialogue_data.get('dialogue_text', ''))
                    else:
                        formatted_text = _format_vo_text_for_display(original_text)
                    
                    vo_widget.config(state='normal')
                    vo_widget.delete('1.0', tk.END)
                    vo_widget.insert('1.0', formatted_text)
                    vo_widget.config(state='disabled')
                    vo_widget.dialogue_info = vo_dialogue_data
                    vo_widget.dialogue_index = i
        
        # Widgets VF - Afficher les textes traduits
        if hasattr(main_interface, 'multiple_vf_widgets'):
            for i, vf_widget in enumerate(main_interface.multiple_vf_widgets):
                if i < len(vf_dialogues) and vf_widget and vf_widget.winfo_exists():
                    vf_dialogue = vf_dialogues[i]
                    # Utiliser le texte traduit (dialogue_text dans vf_dialogues)
                    translated_text = vf_dialogue.get('dialogue_text', '')
                    
                    vf_widget.delete('1.0', tk.END)
                    vf_widget.insert('1.0', translated_text)
                    vf_widget.dialogue_info = vf_dialogue
                    vf_widget.dialogue_index = i
                    
    except Exception as e:
        log_message("ERREUR", f"Erreur population widgets séparés: {e}", category="realtime_editor")

def _format_vo_text_for_display(original_text):
    """Formate un texte VO pour un affichage optimisé dans les petits widgets"""
    try:
        import re
        named_match = re.match(r'^(\w+)\s+"(.+)"$', original_text.strip())
        if named_match: return f"{named_match.group(1)}:\n\"{named_match.group(2)}\""
        
        quote_matches = re.findall(r'"([^"]*)"', original_text)
        if len(quote_matches) == 2: return f"\"{quote_matches[0]}\":\n\"{quote_matches[1]}\""
        
        simple_match = re.match(r'^"(.+)"$', original_text.strip())
        if simple_match: return f"\"{simple_match.group(1)}\""
        
        return original_text[:47] + "..." if len(original_text) > 50 else original_text
    except Exception as e:
        log_message("ERREUR", f"Erreur formatage texte VO: {e}", category="realtime_editor"); return original_text

def _analyze_dialogue_structure(main_interface, dialogue_info):
    """Détecte les dialogues split et récupère les vrais textes VO/VF."""
    try:
        if not main_interface.current_project_path or not dialogue_info.get('tl_file'): 
            return {'is_split': False}
        
        tl_file_path = os.path.join(main_interface.current_project_path, dialogue_info['tl_file'])
        if not os.path.exists(tl_file_path): 
            return {'is_split': False}
        
        with open(tl_file_path, 'r', encoding='utf-8') as f: 
            lines = f.readlines()
        
        target_line = dialogue_info.get('tl_line', 0) - 1
        if not (0 <= target_line < len(lines)): 
            return {'is_split': False}
        
        dialogue_block = _find_translation_block(lines, target_line)
        if len(dialogue_block) > 1:
            current_part_index = next((i for i, (line_idx, _) in enumerate(dialogue_block) if line_idx == target_line), -1)
            
            # Récupérer les textes traduits réels des parties
            part1_translated = dialogue_block[0][1] if len(dialogue_block) > 0 else ''
            part2_translated = dialogue_block[1][1] if len(dialogue_block) > 1 else ''
            
            if current_part_index == 0 and len(dialogue_block) >= 2:
                return {
                    'is_split': True, 
                    'split_type': 'multiline', 
                    'part1_text': part1_translated, 
                    'part2_text': part2_translated, 
                    'part_number': 1, 
                    'total_parts': len(dialogue_block)
                }
            elif current_part_index == 1 and len(dialogue_block) >= 2:
                return {
                    'is_split': True, 
                    'split_type': 'multiline', 
                    'part1_text': part1_translated, 
                    'part2_text': part2_translated, 
                    'part_number': 2, 
                    'total_parts': len(dialogue_block)
                }
        
        # Cas locuteur non défini - analyser la ligne actuelle
        import re
        current_line = lines[target_line].strip()
        temp_line = current_line.replace('\\"', '§ESCAPED_QUOTE§')
        quote_matches = list(re.finditer(r'"([^"]*)"', temp_line))
        
        if len(quote_matches) == 2 and quote_matches[1].start() - quote_matches[0].end() > 0:
            # Récupérer les textes traduits des deux parties
            speaker_translated = quote_matches[0].group(1).replace('§ESCAPED_QUOTE§', '\\"')
            dialogue_translated = quote_matches[1].group(1).replace('§ESCAPED_QUOTE§', '\\"')
            
            return {
                'is_split': True, 
                'split_type': 'speaker_dialogue', 
                'part1_text': speaker_translated, 
                'part2_text': dialogue_translated, 
                'part_number': 1, 
                'total_parts': 2
            }
        
        # Cas simple
        if len(quote_matches) == 1:
            dialogue_translated = quote_matches[0].group(1).replace('§ESCAPED_QUOTE§', '\\"')
            return {
                'is_split': False, 
                'split_type': 'normal', 
                'part1_text': dialogue_translated, 
                'part2_text': '', 
                'part_number': 1, 
                'total_parts': 1
            }
        
        return {'is_split': False, 'split_type': 'normal', 'part1_text': '', 'part2_text': '', 'part_number': 1, 'total_parts': 1}
        
    except Exception as e:
        log_message("ERREUR", f"Erreur analyse structure dialogue: {e}", category="realtime_editor")
        return {'is_split': False}

def _find_translation_block(lines, target_line):
    """Trouve tous les dialogues appartenant au même bloc de traduction"""
    dialogue_block, block_start = [], target_line
    for i in range(target_line - 1, -1, -1):
        line = lines[i].strip()
        if (line.startswith('#') and not line.startswith('# game/')) or line.startswith('translate ') or line == '':
            block_start = i + 1; break
    
    import re
    for i in range(block_start, len(lines)):
        line = lines[i].strip()
        if line.startswith('translate ') or line.startswith('# game/'): break
        if not line.startswith('#') and line:
            dialogue_match = re.search(r'"((?:\\.|[^"])*)"', line)
            if dialogue_match: dialogue_block.append((i, dialogue_match.group(1)))
    return dialogue_block

def _save_current_modification_if_changed(main_interface):
    """Sauvegarde la modification actuelle en attente si elle a changé."""
    try:
        if not hasattr(main_interface, 'current_dialogue_info') or not main_interface.current_dialogue_info: return
        
        biz = main_interface._get_realtime_editor_business()
        if main_interface.current_multiple_group:
            vf_dialogues = main_interface.current_multiple_group.get('vf_dialogues', [])
            for i, widget in enumerate(main_interface.multiple_vf_widgets):
                if not (widget and widget.winfo_exists() and i < len(vf_dialogues)): continue
                current_text, original_info = widget.get('1.0', tk.END).strip(), vf_dialogues[i]
                if current_text != original_info.get('dialogue_text', '').strip():
                    single_dialogue_info = {**main_interface.current_multiple_group, **original_info, 'tl_line': original_info['line_index'] + 1}
                    mod_data = {'type': 'simple', 'content': current_text, 'original_structure': {'was_split': False, 'original_text': original_info.get('dialogue_text', '')}}
                    biz.add_pending_modification(single_dialogue_info, mod_data)
            return

        dialogue_structure = _analyze_dialogue_structure(main_interface, main_interface.current_dialogue_info)
        was_split, original_type = dialogue_structure['is_split'], dialogue_structure.get('split_type', 'normal')
        
        modification_data = None
        if main_interface.vf_split_mode:
            part1, part2 = main_interface.vf_text_widget.get('1.0', tk.END).strip(), (main_interface.vf_text_widget_2.get('1.0', tk.END).strip() if main_interface.vf_text_widget_2 else "")
            orig_p1, orig_p2 = dialogue_structure.get('part1_text', '').strip(), dialogue_structure.get('part2_text', '').strip()
            if part1 != orig_p1 or part2 != orig_p2:
                if original_type == 'speaker_dialogue':
                    modification_data = {'type': 'speaker_dialogue', 'content': {'speaker': part1, 'dialogue': part2}, 'original_structure': {'was_split': was_split, 'split_type': original_type, 'original_speaker': orig_p1, 'original_dialogue': orig_p2}}
                else:
                    modification_data = {'type': 'split', 'content': {'part1': part1, 'part2': part2}, 'original_structure': {'was_split': was_split, 'split_type': original_type, 'original_part1': orig_p1, 'original_part2': orig_p2}}
        else:
            current_vf_text = main_interface.vf_text_widget.get('1.0', tk.END).strip()
            original_displayed = main_interface.current_dialogue_info.get('displayed_text', '').strip()
            if current_vf_text != original_displayed:
                if was_split:
                    modification_data = {'type': 'merge', 'content': current_vf_text, 'original_structure': {'was_split': was_split, 'split_type': original_type, 'original_part1': dialogue_structure.get('part1_text', ''), 'original_part2': dialogue_structure.get('part2_text', '')}}
                else:
                    modification_data = {'type': 'simple', 'content': current_vf_text, 'original_structure': {'was_split': False, 'split_type': 'normal', 'original_text': original_displayed}}
        
        if modification_data:
            biz.add_pending_modification(main_interface.current_dialogue_info, modification_data)
    except Exception as e:
        log_message("ERREUR", f"Erreur sauvegarde modification actuelle: {e}", category="realtime_editor")

def check_and_offer_recovery(main_interface):
    """Vérifie et propose la récupération des modifications non sauvegardées."""
    try:
        if not main_interface.current_project_path: return False
        biz = main_interface._get_realtime_editor_business()
        recovery_info = biz.check_recovery_available(main_interface.current_project_path)
        
        if recovery_info['available']:
            count = recovery_info['count']; s = 's' if count > 1 else ''
            message_styled = [
                ("Récupération disponible !\n\n", "bold_green"), (f"Un total de {count} modification{s}", "bold"),
                (" de la session précédente a été trouvé.\n\nVoulez-vous les récupérer ?\n\n", "normal"),
                ("💡 ", "yellow"), ("Attention : ", "bold"), ("Ignorer impliquera la ", "yellow"), ("perte définitive", "underline"),
                (" de ce travail non sauvegardé.\n\n", "yellow"), ("⚠️ Un choix est requis pour continuer.", "bold_red")]

            response = show_custom_messagebox('askyesno', "Récupération après crash", message_styled, theme_manager.get_theme(), parent=main_interface.window)
            
            if response is True:
                result = biz.load_recovery_data(recovery_info['recovery_file'])
                if result.get('success'):
                    main_interface._show_notification(f"{result.get('recovered_count', 0)} modifications récupérées !", "success")
                else:
                    # ### CORRECTION FINALE ###
                    # On prépare la variable avant pour éviter les conflits de guillemets.
                    error_msg = " / ".join(result.get('errors', [])) or "Inconnue"
                    main_interface._show_notification(f"Erreur récupération: {error_msg}", "error")

            elif response is False:
                main_interface._show_notification("Fichier de récupération ignoré", "info")
            
            if os.path.exists(recovery_info['recovery_file']): os.remove(recovery_info['recovery_file'])
            return True
    except Exception as e:
        log_message("ERREUR", f"Erreur vérification récupération: {e}", category="realtime_editor")
    return False

def _update_pending_status(main_interface):
    """Met à jour le statut avec le nombre de modifications en attente."""
    try:
        biz = main_interface._get_realtime_editor_business()
        summary = biz.get_pending_modifications_summary()
        pending_count = summary['total_count']
        if pending_count > 0:
            status_parts = [f"{pending_count} modification(s) en attente"]
            by_type = summary['by_type']
            if len(by_type) > 1:
                type_details = []
                for mod_type, count in by_type.items():
                    type_name = {'simple': 'simple', 'split': 'division', 'speaker_dialogue': 'locuteur+dialogue', 'merge': 'fusion'}.get(mod_type, mod_type)
                    type_details.append(f"{count} {type_name}")
                status_parts.append(f"({', '.join(type_details)})")
            main_interface._update_status(" ".join(status_parts))
    except Exception as e:
        log_message("ERREUR", f"Erreur mise à jour statut pending: {e}", category="realtime_editor")

def save_translation(main_interface):
    """Sauvegarde la modification actuelle puis toutes les modifications en attente."""
    try:
        if not main_interface.current_dialogue_info:
            main_interface._show_notification("Aucun dialogue à sauvegarder", "warning"); return
        
        _save_current_modification_if_changed(main_interface)
        biz = main_interface._get_realtime_editor_business()
        result = biz.save_all_pending_modifications(main_interface.current_project_path)
        
        if result.get('success'):
            saved_count = result.get('saved_count', 0)
            errors_count = len(result.get('errors', []))
            if saved_count > 0:
                main_interface._update_status(f"{saved_count} traduction(s) sauvegardée(s)")
                if not getattr(main_interface, 'realtime_first_save_notified', False):
                    success_msg = f"{saved_count} modification(s) sauvegardée(s) !\n\nAppuyez sur Maj+R dans le jeu pour voir les modifications."
                    main_interface._show_notification(success_msg, "success")
                    main_interface.realtime_first_save_notified = True
            else: main_interface._show_notification("Aucune modification à sauvegarder", "info")
            if errors_count > 0:
                error_summary = f"{errors_count} erreur(s) lors de la sauvegarde:\n" + "\n".join(result['errors'][:5])
                main_interface._show_notification(error_summary, "warning")
        else:
            # ### CORRECTION FINALE ###
            # On prépare la variable avant pour éviter les conflits de guillemets.
            err_details = " / ".join(result.get('errors', [])) or "Échec inconnu"
            main_interface._show_notification(f"Erreur sauvegarde: {err_details}", "error")
            
    except Exception as e:
        main_interface._show_notification(f"Erreur sauvegarde: {e}", "error")
        log_message("ERREUR", f"Erreur sauvegarde: {e}", category="realtime_editor")

def scan_available_languages(main_interface, lang_combo):
    """Scanne les langues disponibles dans le projet actuel."""
    try:
        if not main_interface.current_project_path:
            main_interface._show_notification('Veuillez sélectionner un projet Ren\'Py', "warning"); return
        tl_path = os.path.join(main_interface.current_project_path, "game", "tl")
        if not os.path.exists(tl_path):
            main_interface._update_status("⚠️ Aucun dossier tl/ trouvé dans le projet"); return
        
        languages = [item for item in os.listdir(tl_path) if os.path.isdir(os.path.join(tl_path, item)) and any(f.endswith('.rpy') for _, _, files in os.walk(os.path.join(tl_path, item)) for f in files)]
        if not languages:
            main_interface._update_status("⚠️ Aucune langue avec fichiers trouvée"); return
        
        languages.sort(key=lambda x: (0 if x.lower() == 'french' else 1, x.lower()))
        lang_combo['values'] = languages
        main_interface.realtime_language_var.set('french' if 'french' in languages else languages[0])
        update_vf_label_text(main_interface)
        main_interface._update_status(f"✅ {len(languages)} langues détectées: {', '.join(languages)}")
    except Exception as e:
        log_message("ERREUR", f"Erreur scan langues: {e}", category="realtime_editor")
        main_interface._show_notification(f"Erreur scan langues: {e}", "error")

def update_vf_label_text(main_interface):
    """Met à jour le texte du label VF selon la langue sélectionnée"""
    try:
        lang = main_interface.realtime_language_var.get()
        new_text = f"🌐 Traduction ({lang.title()})" if lang else "🌐 Traduction (VF)"
        if hasattr(main_interface, 'vf_label'): main_interface.vf_label.config(text=new_text)
    except Exception as e:
        log_message("ATTENTION", f"Erreur mise à jour label VF: {e}", category="realtime_editor")

def _open_google_with_text(main_interface, text: str):
    """
    Ouvre Google Translate avec le texte fourni.
    Cible la langue de l'interface temps réel si disponible.
    """
    try:
        import webbrowser, urllib.parse
        # Langue cible d'après ton sélecteur d'onglet (fallback 'fr')
        tl = 'fr'
        try:
            tl = (main_interface.realtime_language_var.get() or 'fr').lower()
        except Exception:
            pass

        url = "https://translate.google.com/?sl=auto&tl={}&text={}&op=translate".format(
            urllib.parse.quote(tl), urllib.parse.quote(text or "")
        )
        webbrowser.open(url)
        return True
    except Exception as e:
        log_message("ATTENTION", f"Impossible d'ouvrir Google Translate: {e}", category="realtime_editor")
        return False

def copy_and_open_deepl(main_interface, text, context=""):
    """
    Copie le texte dans le presse-papier et ouvre DeepL avec le texte pré-rempli.
    
    Args:
        main_interface: Interface principale pour accéder au clipboard et aux notifications
        text: Texte à copier et envoyer à DeepL
        context: Contexte pour les logs (optionnel)
    """
    try:
        # Nettoyer et limiter le texte
        clean_text = text.strip()
        if not clean_text:
            main_interface._show_notification("Aucun texte à traduire", "warning")
            return
        
        # Limiter la longueur pour éviter les URLs trop longues
        max_length = 500
        if len(clean_text) > max_length:
            clean_text = clean_text[:max_length] + "..."
            main_interface._show_notification(f"Texte tronqué à {max_length} caractères", "info")
        
        # Copier dans le presse-papier
        main_interface.window.clipboard_clear()
        main_interface.window.clipboard_append(clean_text)
        
        # Encoder le texte pour l'URL en préservant les antislashs
        encoded_text = urllib.parse.quote(clean_text, safe='\\')
        
        # Construire l'URL DeepL (anglais vers français par défaut)
        # Format: https://www.deepl.com/translator#en/fr/texte
        deepl_url = f"https://www.deepl.com/translator#en/fr/{encoded_text}"
        
        # Ouvrir DeepL
        webbrowser.open(deepl_url)
        
        # Message de statut
        status_msg = f"DeepL ouvert avec le texte{' ' + context if context else ''}"
        main_interface._update_status(status_msg)
        
        log_message("INFO", f"Texte envoyé à DeepL{' (' + context + ')' if context else ''}: {len(clean_text)} caractères", category="realtime_editor")
        
    except Exception as e:
        error_msg = f"Erreur ouverture DeepL: {e}"
        main_interface._show_notification(error_msg, "error")
        log_message("ERREUR", f"Erreur DeepL{' (' + context + ')' if context else ''}: {e}", category="realtime_editor")

def open_modified_file(main_interface):
    """Ouvre le fichier modifié dans l'éditeur par défaut à la ligne correspondante"""
    try:
        if not main_interface.current_dialogue_info:
            main_interface._show_notification("Aucun fichier à ouvrir", "warning"); return
        if not config_manager.get('auto_open_files', True):
            main_interface._show_notification("Ouverture auto désactivée", "info"); return
        
        tl_file, tl_line = main_interface.current_dialogue_info.get('tl_file'), main_interface.current_dialogue_info.get('tl_line', 1)
        if not tl_file:
            main_interface._show_notification("Infos de fichier manquantes", "warning"); return
        
        file_path = tl_file if os.path.isabs(tl_file) else os.path.join(main_interface.current_project_path, tl_file)
        if not os.path.exists(file_path):
            main_interface._show_notification("Fichier de traduction non trouvé", "error"); return
        
        if _open_file_with_editor(file_path, tl_line):
            main_interface._update_status(f"Fichier ouvert: {os.path.basename(file_path)}:{tl_line}")
        else: main_interface._show_notification("Impossible d'ouvrir le fichier ou éditeur non trouvé", "error")
            
    except Exception as e:
        log_message("ERREUR", f"Erreur ouverture fichier: {e}", category="realtime_editor")
        main_interface._show_notification(f"Erreur ouverture: {e}", category="realtime_editor")

def open_modified_file_for_menu(main_interface):
    """Ouvre le fichier de traduction correspondant au premier choix du menu."""
    try:
        if not hasattr(main_interface, 'current_menu_choices'):
            main_interface._show_notification("Aucun menu actuellement affiché.", "warning")
            return

        choices = main_interface.current_menu_choices.get('choices', [])
        if not choices:
            main_interface._show_notification("Aucun choix dans le menu à ouvrir.", "warning")
            return

        # On prend les informations du PREMIER choix
        first_choice = choices[0]
        tl_file = first_choice.get('tl_file')
        tl_line = first_choice.get('tl_line', 1)

        if not tl_file or not main_interface.current_project_path:
            main_interface._show_notification("Impossible de trouver le fichier pour le premier choix.", "error")
            return
            
        file_path = tl_file if os.path.isabs(tl_file) else os.path.join(main_interface.current_project_path, tl_file)
        if not os.path.exists(file_path):
            main_interface._show_notification(f"Fichier non trouvé : {file_path}", "error")
            return

        if _open_file_with_editor(file_path, tl_line):
            main_interface._update_status(f"Fichier ouvert : {os.path.basename(file_path)}:{tl_line}")
        else:
            main_interface._show_notification("Impossible d'ouvrir le fichier.", "error")

    except Exception as e:
        log_message("ERREUR", f"Erreur ouverture fichier menu: {e}", "realtime_editor")
        main_interface._show_notification(f"Erreur à l'ouverture: {e}", "error")

def open_modified_file_for_multiple(main_interface):
    """Ouvre le fichier de traduction correspondant au premier dialogue du groupe multiple."""
    try:
        if not hasattr(main_interface, 'current_multiple_group') or not main_interface.current_multiple_group:
            main_interface._show_notification("Aucun groupe multiple actuellement affiché.", "warning")
            return

        # Le nom du fichier est stocké au niveau du groupe
        tl_file = main_interface.current_multiple_group.get('tl_file')
        
        # Les détails de la ligne sont dans le premier dialogue de la liste
        dialogues = main_interface.current_multiple_group.get('dialogues', [])
        if not dialogues:
            main_interface._show_notification("Aucun dialogue dans le groupe à ouvrir.", "warning")
            return
        
        first_dialogue = dialogues[0]
        # L'index de ligne est 0-based, on ajoute 1 pour l'éditeur
        tl_line = first_dialogue.get('line_index', -1) + 1

        if not tl_file or tl_line == 0 or not main_interface.current_project_path:
            main_interface._show_notification("Impossible de trouver les infos de fichier pour le premier dialogue.", "error")
            return
            
        # Le chemin est relatif, on le combine avec le chemin du projet
        file_path = os.path.join(main_interface.current_project_path, tl_file)
        if not os.path.exists(file_path):
             main_interface._show_notification(f"Fichier non trouvé : {file_path}", "error")
             return

        if _open_file_with_editor(file_path, tl_line):
            main_interface._update_status(f"Fichier ouvert : {os.path.basename(file_path)}:{tl_line}")
        else:
            main_interface._show_notification("Impossible d'ouvrir le fichier.", "error")

    except Exception as e:
        log_message("ERREUR", f"Erreur ouverture fichier multiple: {e}", "realtime_editor")
        main_interface._show_notification(f"Erreur à l'ouverture: {e}", "error")

def _open_file_with_editor(file_path, line_number):
    """Wrapper vers editor_manager.open_file_with_editor pour éviter toute divergence."""
    return _open_with_editor(file_path, line_number)

def _snapshot_editor_visible_state(main_interface):
    """
    Capture l'état VISUEL courant pour le réappliquer après detach/attach.
    On ne touche pas aux données métier, seulement aux contenus affichés.
    """
    snap = {
        "font_size": main_interface.editor_font_size_var.get(),
        "mode": "normal",
        "vf": {},
        "vo": {}
    }

    # --- VO ---
    # Menus/Multiples
    if getattr(main_interface, "is_in_menu_mode", False) and hasattr(main_interface, "multiple_vo_widgets"):
        snap["vo"]["items"] = []
        for w in getattr(main_interface, "multiple_vo_widgets", []):
            if w and w.winfo_exists():
                try:
                    w.config(state='normal'); snap["vo"]["items"].append(w.get('1.0', tk.END)); w.config(state='disabled')
                except Exception:
                    snap["vo"]["items"].append("")
            else:
                snap["vo"]["items"].append("")
    else:
        # VO simple / split locuteur+dialogue
        if hasattr(main_interface, "vo_speaker_widget") and main_interface.vo_speaker_widget and main_interface.vo_speaker_widget.winfo_exists():
            try:
                main_interface.vo_speaker_widget.config(state='normal')
                snap["vo"]["speaker"] = main_interface.vo_speaker_widget.get('1.0', tk.END)
                main_interface.vo_speaker_widget.config(state='disabled')
            except Exception:
                pass
        if hasattr(main_interface, "vo_text_widget") and main_interface.vo_text_widget and main_interface.vo_text_widget.winfo_exists():
            try:
                main_interface.vo_text_widget.config(state='normal')
                snap["vo"]["text"] = main_interface.vo_text_widget.get('1.0', tk.END)
                main_interface.vo_text_widget.config(state='disabled')
            except Exception:
                pass

    # --- VF ---
    if getattr(main_interface, "is_in_menu_mode", False) and hasattr(main_interface, "multiple_vf_widgets"):
        snap["mode"] = "menu_multiple"
        snap["vf"]["items"] = []
        for w in getattr(main_interface, "multiple_vf_widgets", []):
            if w and w.winfo_exists():
                snap["vf"]["items"].append(w.get('1.0', tk.END))
            else:
                snap["vf"]["items"].append("")
    elif getattr(main_interface, "vf_split_mode", False):
        split_type = getattr(main_interface, "current_split_type", "multiline")
        snap["mode"] = f"split::{split_type}"
        p1 = main_interface.vf_text_widget.get('1.0', tk.END) if hasattr(main_interface, "vf_text_widget") and main_interface.vf_text_widget and main_interface.vf_text_widget.winfo_exists() else ""
        p2 = main_interface.vf_text_widget_2.get('1.0', tk.END) if hasattr(main_interface, "vf_text_widget_2") and main_interface.vf_text_widget_2 and main_interface.vf_text_widget_2.winfo_exists() else ""
        snap["vf"]["part1"] = p1
        snap["vf"]["part2"] = p2
    else:
        snap["mode"] = "normal"
        txt = main_interface.vf_text_widget.get('1.0', tk.END) if hasattr(main_interface, "vf_text_widget") and main_interface.vf_text_widget and main_interface.vf_text_widget.winfo_exists() else ""
        snap["vf"]["text"] = txt

    return snap

def _restore_editor_visible_state(main_interface, snap):
    """
    Réapplique l'état visuel capturé par _snapshot_editor_visible_state.
    Si l’interface créée ne correspond pas au mode snapshot, on force la bonne
    interface avant d’injecter les textes (VF et VO).
    """
    if not snap:
        return

    # Police
    try:
        main_interface.editor_font_size_var.set(snap.get("font_size", main_interface.editor_font_size_var.get()))
        update_editor_font_size(main_interface)
    except Exception:
        pass

    mode = snap.get("mode", "normal")

    # --- S'assurer que l'UI correspond au mode du snapshot (côté VF) ---
    if mode == "menu_multiple":
        # UI déjà (re)créée par _build_editor_panel ; rien à forcer ici.
        pass
    elif mode.startswith("split::"):
        split_type = mode.split("::", 1)[1]
        part1 = snap["vf"].get("part1", "")
        part2 = snap["vf"].get("part2", "")
        if not getattr(main_interface, "vf_split_mode", False) or getattr(main_interface, "current_split_type", None) != split_type:
            if split_type == "speaker_dialogue":
                _create_split_vf_interface_for_unnamed_speaker_with_grid_and_buttons(main_interface, part1, part2)
            else:
                _create_split_vf_interface_with_grid_and_buttons(main_interface, part1, part2, split_type="multiline")
    else:
        if getattr(main_interface, "vf_split_mode", False):
            _create_normal_vf_interface_with_grid_and_buttons(main_interface)

    # --- Réinjection VF ---
    if mode == "menu_multiple" and hasattr(main_interface, "multiple_vf_widgets"):
        items = snap["vf"].get("items", [])
        for i, w in enumerate(getattr(main_interface, "multiple_vf_widgets", [])):
            if i < len(items) and w and w.winfo_exists():
                w.delete('1.0', tk.END); w.insert('1.0', items[i])
    elif mode.startswith("split::"):
        if hasattr(main_interface, "vf_text_widget") and main_interface.vf_text_widget:
            main_interface.vf_text_widget.delete('1.0', tk.END)
            main_interface.vf_text_widget.insert('1.0', snap["vf"].get("part1", ""))
        if hasattr(main_interface, "vf_text_widget_2") and main_interface.vf_text_widget_2:
            main_interface.vf_text_widget_2.delete('1.0', tk.END)
            main_interface.vf_text_widget_2.insert('1.0', snap["vf"].get("part2", ""))
    else:
        if hasattr(main_interface, "vf_text_widget") and main_interface.vf_text_widget:
            main_interface.vf_text_widget.delete('1.0', tk.END)
            main_interface.vf_text_widget.insert('1.0', snap["vf"].get("text", ""))

    # --- Réinjection VO (tous modes) ---
    # Menus/Multiples
    if hasattr(main_interface, "multiple_vo_widgets") and "items" in snap.get("vo", {}):
        vo_items = snap["vo"].get("items", [])
        for i, w in enumerate(getattr(main_interface, "multiple_vo_widgets", [])):
            if i < len(vo_items) and w and w.winfo_exists():
                try:
                    w.config(state='normal'); w.delete('1.0', tk.END); w.insert('1.0', vo_items[i]); w.config(state='disabled')
                except Exception:
                    pass
    else:
        # VO simple
        if "speaker" in snap.get("vo", {}) and hasattr(main_interface, "vo_speaker_widget") and main_interface.vo_speaker_widget:
            try:
                main_interface.vo_speaker_widget.config(state='normal')
                main_interface.vo_speaker_widget.delete('1.0', tk.END)
                main_interface.vo_speaker_widget.insert('1.0', snap["vo"]["speaker"])
                main_interface.vo_speaker_widget.config(state='disabled')
            except Exception:
                pass
        if "text" in snap.get("vo", {}) and hasattr(main_interface, "vo_text_widget") and main_interface.vo_text_widget:
            try:
                main_interface.vo_text_widget.config(state='normal')
                main_interface.vo_text_widget.delete('1.0', tk.END)
                main_interface.vo_text_widget.insert('1.0', snap["vo"]["text"])
                main_interface.vo_text_widget.config(state='disabled')
            except Exception:
                pass

def save_multiple_translations(main_interface):
    """Sauvegarde toutes les traductions des widgets multiples."""
    try:
        if not (hasattr(main_interface, 'multiple_vf_widgets') and main_interface.multiple_vf_widgets and main_interface.current_multiple_group):
            main_interface._show_notification("Informations de groupe manquantes", "warning"); return False
        
        biz = main_interface._get_realtime_editor_business()
        save_count, error_count = 0, 0
        dialogues = main_interface.current_multiple_group.get('dialogues', [])
        
        for i, widget in enumerate(main_interface.multiple_vf_widgets):
            if widget and widget.winfo_exists() and i < len(dialogues):
                try:
                    vf_text, dialogue = widget.get('1.0', tk.END).strip(), dialogues[i]
                    if vf_text and dialogue:
                        dialogue_info = {
                            'tl_file': main_interface.current_multiple_group.get('tl_file', ''),
                            'tl_line': dialogue['line_index'] + 1,
                            'original_text': dialogue.get('dialogue_text', ''),
                            'displayed_text': vf_text
                        }
                        result = biz.save_translation(dialogue_info, vf_text, main_interface.current_project_path)
                        if result.get('success'): save_count += 1
                        else: error_count += 1
                except Exception as e:
                    error_count += 1; log_message("ERREUR", f"Erreur widget {i+1}: {e}", category="realtime_editor")
        
        if save_count > 0:
            main_interface._update_status(f"{save_count}/{len(main_interface.multiple_vf_widgets)} traductions sauvegardées")
            main_interface._show_notification(f"{save_count} sauvegardées, {error_count} erreurs" if error_count > 0 else f"Toutes les traductions sauvegardées ! ({save_count})", "warning" if error_count > 0 else "success")
            return True
        else: main_interface._show_notification("Aucune traduction sauvegardée", "warning"); return False
    except Exception as e:
        log_message("ERREUR", f"Erreur sauvegarde multiple: {e}", category="realtime_editor")
        main_interface._show_notification(f"Erreur sauvegarde: {e}", "error"); return False

def _bring_realtime_editor_to_front(main_interface):
    """
    Met au premier plan la fenêtre d'édition :
    - si détachée: restaure si minimisée, topmost bref, focus
    - sinon: sélectionne l'onglet, restaure la fenêtre principale, topmost bref, focus
    """
    try:
        # Fenêtre détachée ?
        if getattr(main_interface, "detached_editor_window", None) and main_interface.detached_editor_window.winfo_exists():
            win = main_interface.detached_editor_window
            try:
                win.state("normal")   # restaure si iconifiée
            except Exception:
                pass
            try:
                win.attributes("-topmost", True)
                win.lift()
                win.focus_force()
                # Retirer topmost après un court délai pour ne pas gêner l'utilisateur
                win.after(250, lambda: win.attributes("-topmost", False))
            except Exception:
                pass
            return

        # Sinon, fenêtre principale
        root = main_interface.window  # ta Tk root
        try:
            root.state("normal")
        except Exception:
            pass

        # Sélectionne l’onglet “Éditeur Temps Réel” si Notebook
        try:
            if hasattr(main_interface, "notebook") and main_interface.notebook:
                # adapte 'editor_tab' à l’identifiant réel si besoin
                main_interface.notebook.select(main_interface.editor_tab)
        except Exception:
            pass

        try:
            root.attributes("-topmost", True)
            root.lift()
            root.focus_force()
            root.after(250, lambda: root.attributes("-topmost", False))
        except Exception:
            pass
    except Exception as e:
        log_message("ATTENTION", f"Focus editor fail: {e}", category="realtime_editor")


def show_installation_help(parent_window):
    """Affiche l'aide mise à jour et stylée pour l'Éditeur Temps Réel."""
    
    # On importe les dépendances ici pour éviter une importation circulaire si ce fichier est appelé ailleurs
    from ui.themes import theme_manager
    from infrastructure.helpers.unified_functions import show_custom_messagebox

    help_content_styled = [
        ("GUIDE D'UTILISATION - ÉDITEUR TEMPS RÉEL\n\n", "bold"),
        ("Cette fonctionnalité vous permet de traduire votre jeu en temps réel.\n", "normal"),
        ("Suivez ce guide pour une utilisation optimale.\n\n", "normal"),

        ("📋 WORKFLOW COMPLET (DE A à Z)\n", "bold_green"),
        ("--------------------------------------------------\n", "normal"),
        ("1.  ", "bold"), ("Pré-requis :", "italic"), (" Sélectionnez votre projet Ren'Py, la langue de traduction et votre ", "normal"),
        ("éditeur de code préféré", "bold"), (" dans les menus de configuration.\n\n", "normal"),
        
        ("2.  ", "bold"), ("Installation (une seule fois) :", "italic"), (" Cliquez sur ", "normal"), 
        ("\"Installer le module\"", "yellow"), (". Un fichier sera ajouté au dossier ", "normal"), 
        ("game/", "italic"), (" de votre projet. \n    ", "normal"),
        ("Note :", "bold_yellow"), (" Si vous mettez à jour RenExtract, il est conseillé de réinstaller le module pour bénéficier des derniers correctifs.\n\n", "yellow"),

        ("3.  ", "bold"), ("Lancement :", "italic"), (" Démarrez la surveillance dans RenExtract ", "normal"), 
        ("PUIS", "bold_red"), (" lancez votre jeu Ren'Py. L'application va alors créer un cache de vos traductions pour être ultra-rapide.\n\n", "normal"),

        ("4.  ", "bold"), ("Jeu & Détection :", "italic"), (" Jouez normalement. Chaque ", "normal"),
        ("dialogue et menu de choix", "bold_green"),
        (" s'affichera instantanément dans l'éditeur.\n\n", "normal"),

        ("5.  ", "bold"), ("Édition & Sauvegarde :", "italic"), (" Modifiez la traduction.\n", "normal"),
        ("    • ", "normal"), ("Sauvegarde :", "bold"), (" Appuyez sur ", "normal"), 
        ("le bouton d'enregistrement", "yellow"), (" (ex: 'Enregistrer Tout') ou le raccourci ", "normal"), ("Ctrl+S", "yellow"), (".\n", "normal"),
        ("    • ", "normal"), ("Modifications en attente :", "bold"), (" Si vous ne sauvegardez pas, votre travail est mis en attente. Tout sera sauvegardé au prochain enregistrement.\n\n", "normal"),

        ("6.  ", "bold"), ("Mise à jour en jeu :", "italic"), (" Une fois sauvegardé, retournez dans le jeu et appuyez sur ", "normal"),
        ("Maj+R (Shift+R)", "bold_green"), (" pour voir les changements.\n\n\n", "normal"),

        ("⌨️ RACCOURCIS CLAVIER (FOCUS & PLEIN ÉCRAN)\n", "bold_purple"),
        ("--------------------------------------------------\n", "normal"),
        ("• ", "purple"), ("F8 :", "bold"), (" met l'éditeur au premier plan.\n", "normal"),
        ("    ", "normal"), ("Si le jeu est en plein écran exclusif, le module quitte le plein écran pour permettre le focus automatique.\n", "normal"),
        ("• ", "purple"), ("F11 (Ren'Py natif) :", "bold"), (" pour repasser en plein écran quand vous revenez jouer.\n\n\n", "normal"),

        ("✨ PERSONNALISATION DE L'INTERFACE\n", "bold_purple"),
        ("--------------------------------------------------\n", "normal"),
        ("• ", "purple"), ("Harmonie visuelle :", "bold"), (" Toutes les interfaces d'édition (dialogue simple, split, multiple, choix) ont été harmonisées pour une expérience cohérente.\n\n", "normal"),
        ("• ", "purple"), ("Fenêtre détachable :", "bold"), (" Pour plus de confort, cliquez sur ", "normal"),
        ("↗️ Détacher", "yellow"), 
        (" pour ouvrir l'éditeur dans une fenêtre séparée.\n\n", "normal"),
        
        ("• ", "purple"), ("Taille de la police :", "bold"), (" Utilisez le sélecteur ", "normal"),
        ("Taille police", "yellow"),
        (" pour ajuster la lisibilité. Votre choix est sauvegardé.\n\n\n", "normal"),
        
        ("🛡️ SÉCURITÉ & FIABILITÉ\n", "bold_blue"),
        ("--------------------------------------------------\n", "normal"),
        ("• ", "blue"), ("Performance :", "bold"), (" Un système de cache intelligent a été mis en place pour que l'affichage des menus de choix soit instantané, même dans les gros projets.\n\n", "normal"),
        ("• ", "blue"), ("Récupération après crash :", "bold"), (" En cas de fermeture inattendue, vos modifications en attente sont conservées et proposées à la restauration au redémarrage.\n\n", "normal"),
        ("• ", "blue"), ("Serveur local :", "bold"), (" l'appel F8 utilise l'URL locale ", "normal"),
        ("http://127.0.0.1:8765/focus", "italic"),
        (" (aucune dépendance externe). Autorisez l'accès local si un pare-feu interrompt la requête.\n\n\n", "normal"),

        ("💡 NOTES IMPORTANTES\n", "bold_yellow"),
        ("--------------------------------------------------\n", "normal"),
        ("• L'éditeur gère à la fois les ", "normal"),
        ("dialogues parlés", "bold"), (" (simples, multiples, splits, etc.) et les ", "normal"),
        ("textes des menus de choix", "bold"), (".\n", "normal"),
        ("• Les traductions sont sauvegardées directement dans les fichiers ", "normal"),
        (".rpy", "italic"), (" de vos dossiers de traduction (ex: `game/tl/french` ou `game/bonus/tl/french`).\n\n", "normal"),

        ("🧰 DÉPANNAGE RAPIDE (F8)\n", "bold_green"),
        ("--------------------------------------------------\n", "normal"),
        ("• ", "normal"), ("Si F8 ne fait rien :", "bold"), (" vérifiez que le module a bien été installé et que la screen d'overlay des hotkeys est active.\n", "normal"),
        ("• ", "normal"), ("Si vous êtes en plein écran et que l'éditeur ne prend pas le dessus :", "bold"), (" repassez en fenêtré, puis réessayez F8. Utilisez ", "normal"),
        ("F11", "yellow"), (" pour revenir en plein écran.\n", "normal"),
        ("• ", "normal"), ("Si un antivirus/Pare-feu bloque :", "bold"), (" autorisez les connexions locales sur le port ", "normal"),
        ("8765", "yellow"), (".\n", "normal"),
    ]

    try:
        show_custom_messagebox(
            'info',
            'Instructions - Éditeur Temps Réel',
            help_content_styled,
            theme_manager.get_theme(),
            parent=parent_window
        )
    except Exception as e:
        log_message("ERREUR", f"Erreur affichage aide installation : {e}", category="realtime_editor")