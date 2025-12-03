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
from ui.shared.editor_manager_server import set_focus_callback

# Constantes pour les dimensions fixes des zones de texte
TEXT_WIDGET_HEIGHT = 120  # Hauteur fixe en pixels
TEXT_WIDGET_WIDTH = 400   # Largeur fixe en pixels

def update_status_with_pending_count(main_interface):
    """Met à jour le statut avec le nombre de modifications en attente."""
    try:
        biz = main_interface._get_realtime_editor_business()
        summary = biz.get_pending_modifications_summary()
        pending_count = summary['total_count']
        
        # Mettre à jour la barre de statut générale
        if pending_count > 0:
            status_parts = [f"{pending_count} modification(s) en attente"]
            by_type = summary['by_type']
            if len(by_type) > 1:
                type_details = []
                for mod_type, count in by_type.items():
                    type_name = {'simple': 'simple', 'split': 'division', 'speaker_dialogue': 'locuteur+dialogue', 'merge': 'fusion', 'menu_choice': 'choix', 'multiple_dialogue': 'multiple'}.get(mod_type, mod_type)
                    type_details.append(f"{count} {type_name}")
                status_parts.append(f"({', '.join(type_details)})")
            main_interface._update_status(" ".join(status_parts))
        
        # Mettre à jour le label de surveillance spécifique
        if hasattr(main_interface, 'monitor_status_label'):
            current_text = main_interface.monitor_status_label.cget("text")
            current_fg = main_interface.monitor_status_label.cget("fg")
            
            # Déterminer le statut de base selon la couleur
            if current_fg == '#28a745':  # Vert = Surveillance active
                base_status = "🟢 Surveillance active"
            elif current_fg == '#dc3545':  # Rouge = Surveillance arrêtée
                base_status = "⭕ Surveillance arrêtée"
            else:
                base_status = current_text
            
            # Ajouter le nombre de modifications en attente
            if pending_count > 0:
                status_text = f"{base_status} ({pending_count} modification{'s' if pending_count > 1 else ''} en attente)"
            else:
                status_text = base_status
            
            main_interface.monitor_status_label.config(text=status_text)
            
    except Exception as e:
        log_message("ERREUR", f"Erreur mise à jour statut pending: {e}", category="realtime_editor")

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
        default_size = config_manager.get('editor_font_size', 12)
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
    
    # --- AUTO-SCAN LANGUE (création + re-sélection de l'onglet + changement de projet) ---
    _last_scanned_project = [None]  # Liste pour mutation dans closure
    
    def _manual_scan():
        """Scan manuel avec mise à jour du dernier projet scanné"""
        scan_available_languages(main_interface, lang_combo)
        _last_scanned_project[0] = getattr(main_interface, "current_project_path", "")
    
    scan_btn = tk.Button(config_frame, text="Scanner les langues", command=_manual_scan, bg=theme["button_utility_bg"], fg="#000000", font=('Segoe UI', 9, 'normal'), pady=4, padx=8, relief='flat', cursor='hand2')
    scan_btn.pack(side='left', padx=(0, 10))

    install_btn = tk.Button(config_frame, text="Installer le module", command=lambda: install_monitoring_module(main_interface), bg=theme["button_feature_bg"], fg="#000000", font=('Segoe UI', 9, 'normal'), pady=4, padx=8, relief='flat', cursor='hand2')
    install_btn.pack(side='left', padx=(0, 5))
    
    # ✅ NOUVEAU : Bouton pour forcer l'installation du module v2 (test de compatibilité)
    install_v2_btn = tk.Button(config_frame, text="Tester module v2", command=lambda: install_monitoring_module(main_interface, force_v2=True), bg=theme["button_utility_bg"], fg="#000000", font=('Segoe UI', 9, 'normal'), pady=4, padx=8, relief='flat', cursor='hand2')
    install_v2_btn.pack(side='left')
    
    def _auto_scan_realtime_if_ready(*_):
        # Scanner si on a un projet et (combo vide OU projet différent du dernier scan)
        current_project = getattr(main_interface, "current_project_path", "")
        has_project = bool(current_project)
        combo_empty = not lang_combo['values']
        project_changed = (_last_scanned_project[0] != current_project)
        
        if has_project and (combo_empty or project_changed):
            try:
                scan_available_languages(main_interface, lang_combo)
                _last_scanned_project[0] = current_project  # Mémoriser le projet scanné
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

    # 3) Hook pour resync forcé depuis la fenêtre principale
    main_interface.realtime_resync = _auto_scan_realtime_if_ready
    
    # 4) NOUVEAU : Surveiller les changements de projet
    def _on_project_changed_realtime(*_):
        _auto_scan_realtime_if_ready()
    
    # Attacher un observer si current_project_path est une StringVar
    if hasattr(main_interface, 'current_project_var') and hasattr(main_interface.current_project_var, 'trace'):
        main_interface.current_project_var.trace('w', _on_project_changed_realtime)
    
    # Fallback : Vérifier périodiquement les changements de projet (polling léger)
    def _check_project_change():
        current_project = getattr(main_interface, "current_project_path", "")
        if current_project and current_project != _last_scanned_project[0]:
            _auto_scan_realtime_if_ready()
        # Re-vérifier dans 2 secondes
        tab_frame.after(2000, _check_project_change)
    
    _check_project_change()  # Démarrer la vérification périodique


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
    
    # === AJOUT: Sélecteur de traducteur ===
    from ui.shared.translator_utils import get_default_translator, set_default_translator
    
    # Initialiser le traducteur par défaut si pas déjà fait
    if not hasattr(main_interface, 'current_translator'):
        main_interface.current_translator = get_default_translator()
    
    # Sélecteur de traducteur
    translator_var = tk.StringVar(value=main_interface.current_translator)
    translator_combo = ttk.Combobox(
        interface_controls_frame,
        textvariable=translator_var,
        values=["Google", "Yandex", "DeepL", "Microsoft", "Groq AI"],
        state="readonly",
        width=10,
        font=('Segoe UI', 9)
    )
    translator_combo.pack(side='right', padx=(0, 10))
    def on_translator_changed(event=None):
        new_translator = translator_var.get()
        set_default_translator(new_translator)
        main_interface.current_translator = new_translator
        log_message("INFO", f"Traducteur changé vers: {new_translator}", category="realtime_editor")
    
    translator_combo.bind('<<ComboboxSelected>>', on_translator_changed)
    
    tk.Label(
        interface_controls_frame, 
        text="Traducteur :", 
        font=('Segoe UI', 9, 'normal'),
        bg=theme["bg"], 
        fg=theme["fg"]
    ).pack(side='right', padx=(0, 5))
    
    # === AJOUT: Sélecteur de ton (pour Groq AI) ===
    # Initialiser le ton par défaut si pas déjà fait
    if not hasattr(main_interface, 'translation_tone'):
        main_interface.translation_tone = "informel"  # Par défaut informel (tutoiement)
    
    # Sélecteur de ton
    tone_var = tk.StringVar(value=main_interface.translation_tone.capitalize())
    tone_combo = ttk.Combobox(
        interface_controls_frame,
        textvariable=tone_var,
        values=["Informel", "Formel", "Neutre"],
        state="readonly",
        width=8,
        font=('Segoe UI', 9)
    )
    tone_combo.pack(side='right', padx=(0, 10))
    
    def on_tone_changed(event=None):
        new_tone = tone_var.get().lower()
        main_interface.translation_tone = new_tone
        log_message("INFO", f"Ton de traduction changé vers: {new_tone}", category="realtime_editor")
    
    tone_combo.bind('<<ComboboxSelected>>', on_tone_changed)
    
    tk.Label(
        interface_controls_frame, 
        text="Ton :", 
        font=('Segoe UI', 9, 'normal'),
        bg=theme["bg"], 
        fg=theme["fg"]
    ).pack(side='right', padx=(0, 5))
    
    # === AJOUT: Bouton paramétrage Groq AI ===
    groq_settings_btn = tk.Button(
        interface_controls_frame,
        text="⚙️ Paramétrer Groq AI",
        command=lambda: _show_groq_prompt_customizer(main_interface),
        bg=theme["button_feature_bg"],
        fg="#000000",
        font=('Segoe UI', 9, 'bold'),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    groq_settings_btn.pack(side='right', padx=(0, 15))


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
    """Met à jour la taille de police de tous les widgets de texte et sauvegarde le choix."""
    try:
        new_size = main_interface.editor_font_size_var.get()
        new_font = ('Segoe UI', new_size)

        # ✅ Mettre à jour les widgets principaux (simple)
        if hasattr(main_interface, 'vo_text_widget') and main_interface.vo_text_widget and main_interface.vo_text_widget.winfo_exists():
            main_interface.vo_text_widget.config(font=new_font)
        
        if hasattr(main_interface, 'vf_text_widget') and main_interface.vf_text_widget and main_interface.vf_text_widget.winfo_exists():
            main_interface.vf_text_widget.config(font=new_font)
        
        # ✅ Mettre à jour les widgets split (partie 1 et 2)
        if hasattr(main_interface, 'vf_text_widget_2') and main_interface.vf_text_widget_2 and main_interface.vf_text_widget_2.winfo_exists():
            main_interface.vf_text_widget_2.config(font=new_font)
        
        # ✅ Mettre à jour les widgets speaker/dialogue divisé (VO)
        if hasattr(main_interface, 'vo_speaker_widget') and main_interface.vo_speaker_widget and main_interface.vo_speaker_widget.winfo_exists():
            main_interface.vo_speaker_widget.config(font=new_font)
        
        # ✅ Mettre à jour les widgets de dialogues multiples (ce sont des widgets Text directs)
        if hasattr(main_interface, 'multiple_vo_widgets'):
            for text_widget in main_interface.multiple_vo_widgets:
                if text_widget and text_widget.winfo_exists():
                    text_widget.config(font=new_font)
        
        if hasattr(main_interface, 'multiple_vf_widgets'):
            for text_widget in main_interface.multiple_vf_widgets:
                if text_widget and text_widget.winfo_exists():
                    text_widget.config(font=new_font)
        
        # ✅ Mettre à jour les widgets de menus (ce sont des widgets Text directs)
        if hasattr(main_interface, 'menu_vo_widgets'):
            for text_widget in main_interface.menu_vo_widgets:
                if text_widget and text_widget.winfo_exists():
                    text_widget.config(font=new_font)
        
        if hasattr(main_interface, 'menu_vf_widgets'):
            for text_widget in main_interface.menu_vf_widgets:
                if text_widget and text_widget.winfo_exists():
                    text_widget.config(font=new_font)

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
        # Ajusté pour être cohérent avec les dimensions fixes des widgets Text (8 lignes ≈ 160px)
        TEXT_AREA_HEIGHT = 160

        edit_main = tk.Frame(parent_container, bg=theme["bg"])

        # Configuration de la grille principale
        if is_detached:
            edit_main.grid_rowconfigure(0, weight=0)  # Header
            edit_main.grid_rowconfigure(1, weight=1)  # Zones de texte
            edit_main.grid_rowconfigure(2, weight=0)  # Boutons globaux
        else:
            edit_main.grid_rowconfigure(0, weight=1)  # Zones de texte
            edit_main.grid_rowconfigure(1, weight=0)  # Boutons globaux

        # Proportions : VO 50% / VF 50%
        edit_main.grid_columnconfigure(0, weight=1, minsize=200)
        edit_main.grid_columnconfigure(1, weight=1, minsize=300)

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
            # ✅ Petit padding horizontal pour ne pas coller aux bords
            text_areas_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=8)
        else:
            text_areas_frame.grid(row=0, column=0, columnspan=2, sticky='ew')

        text_areas_frame.grid_columnconfigure(0, weight=1)
        text_areas_frame.grid_columnconfigure(1, weight=1)
        text_areas_frame.grid_rowconfigure(0, weight=1)

        # --- COLONNE VO avec Grid ---
        main_interface.vo_main_container = tk.Frame(text_areas_frame, bg=theme["bg"])
        # ✅ Réduire l'espace horizontal entre VO et VF en mode détaché
        padding_between = 3 if is_detached else 5
        main_interface.vo_main_container.grid(row=0, column=0, sticky='nsew', padx=(0, padding_between))
        
        main_interface.vo_main_container.grid_rowconfigure(0, weight=0)
        main_interface.vo_main_container.grid_rowconfigure(1, weight=1)
        main_interface.vo_main_container.grid_columnconfigure(0, weight=1)

        vo_label = tk.Label(main_interface.vo_main_container, text="Texte Original (VO)", font=('Segoe UI', 10, 'bold'), bg=theme["bg"], fg=theme["fg"])
        vo_label.grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        main_interface.vo_content_container = tk.Frame(main_interface.vo_main_container, bg=theme["bg"], height=TEXT_AREA_HEIGHT)
        main_interface.vo_content_container.grid(row=1, column=0, sticky='ew')
        
        main_interface.vo_content_container.grid_propagate(False)
        # ✅ MODIFIÉ : Configuration pour inclure le champ locuteur (3 lignes au lieu de 2)
        main_interface.vo_content_container.grid_rowconfigure(0, weight=0)  # Locuteur (fixe)
        main_interface.vo_content_container.grid_rowconfigure(1, weight=1)  # Zone texte (expandable)
        main_interface.vo_content_container.grid_rowconfigure(2, weight=0)  # Boutons (fixe)
        main_interface.vo_content_container.grid_columnconfigure(0, weight=1)

        _create_normal_vo_interface_with_grid(main_interface)

        # --- COLONNE VF avec Grid ---
        main_interface.vf_main_container = tk.Frame(text_areas_frame, bg=theme["bg"])
        # ✅ Réduire l'espace horizontal entre VO et VF en mode détaché
        main_interface.vf_main_container.grid(row=0, column=1, sticky='nsew', padx=(padding_between, 0))
        
        main_interface.vf_main_container.grid_rowconfigure(0, weight=0)
        main_interface.vf_main_container.grid_rowconfigure(1, weight=1)
        main_interface.vf_main_container.grid_columnconfigure(0, weight=1)

        main_interface.vf_label = tk.Label(main_interface.vf_main_container, text=f"Traduction ({main_interface.realtime_language_var.get().title()})", font=('Segoe UI', 10, 'bold'), bg=theme["bg"], fg=theme["fg"])
        main_interface.vf_label.grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        main_interface.vf_content_container = tk.Frame(main_interface.vf_main_container, bg=theme["bg"], height=TEXT_AREA_HEIGHT)
        main_interface.vf_content_container.grid(row=1, column=0, sticky='ew')
        
        main_interface.vf_content_container.grid_propagate(False)
        # ✅ MODIFIÉ : Configuration pour inclure le champ locuteur (3 lignes au lieu de 2)
        main_interface.vf_content_container.grid_rowconfigure(0, weight=0)  # Locuteur (fixe)
        main_interface.vf_content_container.grid_rowconfigure(1, weight=1)  # Zone texte (expandable)
        main_interface.vf_content_container.grid_rowconfigure(2, weight=0)  # Boutons (fixe)
        main_interface.vf_content_container.grid_columnconfigure(0, weight=1)
        
        _create_normal_vf_interface_with_grid_and_buttons(main_interface)

        # BOUTONS GLOBAUX
        buttons_frame = tk.Frame(edit_main, bg=theme["bg"])
        if is_detached:
            # ✅ Ajouter un petit espace en bas et à droite en mode détaché
            buttons_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10, 8), padx=(0, 8))
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

def _get_character_display_name(speaker_key, main_interface):
    """Récupère le nom d'affichage d'un personnage depuis sa lettre de définition"""
    if not speaker_key:
        return "Narrateur"
    
    from infrastructure.config.config import config_manager
    characters_def = config_manager.get('groq_characters_definitions', {})
    
    if speaker_key in characters_def:
        char_info = characters_def[speaker_key]
        prenom = char_info.get('prenom', '')
        if prenom:
            return f"{speaker_key} ({prenom})"
        # Fallback : utiliser la lettre si pas de prénom défini
        return speaker_key.upper()
    
    # Si pas dans les définitions, retourner la lettre
    return speaker_key.upper()

def _scan_all_speakers_from_game(main_interface):
    """Scanne tous les fichiers .rpy du jeu pour trouver tous les locuteurs utilisés (avec cache)"""
    # ✅ Cache pour éviter de scanner à chaque fois
    if not hasattr(main_interface, '_scanned_speakers_cache'):
        main_interface._scanned_speakers_cache = {}
    
    cache_key = main_interface.current_project_path if hasattr(main_interface, 'current_project_path') else None
    if cache_key and cache_key in main_interface._scanned_speakers_cache:
        return main_interface._scanned_speakers_cache[cache_key]
    
    speakers_found = set()
    
    try:
        if not hasattr(main_interface, 'current_project_path') or not main_interface.current_project_path:
            return speakers_found
        
        game_folder = os.path.join(main_interface.current_project_path, "game")
        if not os.path.exists(game_folder):
            return speakers_found
        
        # Scanner tous les fichiers .rpy (hors tl/)
        import glob
        rpy_files = glob.glob(os.path.join(game_folder, "**/*.rpy"), recursive=True)
        rpy_files = [f for f in rpy_files if '/tl/' not in f.replace('\\', '/')]
        
        # Mots-clés Ren'Py à exclure (liste complète)
        renpy_keywords = {
            'define', 'label', 'menu', 'if', 'elif', 'else', 'while', 'for', 'return', 
            'call', 'jump', 'scene', 'show', 'hide', 'play', 'stop', 'pause', 'window', 
            'nvl', 'centered', 'extend', 'with', 'at', 'as', 'onlayer', 'zorder', 'transform', 
            'function', 'class', 'init', 'python', 'screen', 'image', 'default', 'persistent',
            'old', 'new', 'translate', 'renpy', 'config', 'store'
        }
        
        # Pattern pour détecter les locuteurs : lettre "texte" ou nom "texte"
        speaker_pattern = re.compile(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s+"')
        
        for filepath in rpy_files:
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        # Ignorer les commentaires et lignes spéciales
                        stripped = line.strip()
                        if not stripped or stripped.startswith('#') or stripped.startswith('translate ') or 'old ' in stripped.lower() or 'new ' in stripped.lower():
                            continue
                        
                        # Chercher un locuteur
                        match = speaker_pattern.match(line)
                        if match:
                            speaker_key = match.group(1).lower()
                            # Exclure les mots-clés Ren'Py
                            if speaker_key not in renpy_keywords:
                                speakers_found.add(speaker_key)
            except Exception:
                continue
        
        # Mettre en cache
        if cache_key:
            main_interface._scanned_speakers_cache[cache_key] = speakers_found
        
        log_message("INFO", f"Scan locuteurs: {len(speakers_found)} locuteurs trouvés dans le jeu", category="realtime_editor")
        return speakers_found
        
    except Exception as e:
        log_message("ERREUR", f"Erreur scan locuteurs: {e}", category="realtime_editor")
        return speakers_found

def _get_characters_list_for_combobox(main_interface):
    """Récupère la liste des personnages formatée pour une Combobox (inclut tous les locuteurs du jeu)"""
    from infrastructure.config.config import config_manager
    characters_def = config_manager.get('groq_characters_definitions', {})
    
    # Créer une liste avec "Narrateur" en premier
    characters_list = ["Narrateur (aucun locuteur)"]
    
    # ✅ NOUVEAU : Scanner tous les locuteurs du jeu
    all_speakers = _scan_all_speakers_from_game(main_interface)
    
    # Combiner les locuteurs scannés avec les définitions
    all_char_keys = set(all_speakers)
    for char_key in characters_def.keys():
        all_char_keys.add(char_key)
    
    # Ajouter tous les locuteurs avec leur nom d'affichage
    for char_key in sorted(all_char_keys):
        # Chercher dans les définitions pour le nom
        if char_key in characters_def:
            char_info = characters_def[char_key]
            if isinstance(char_info, dict):
                prenom = char_info.get('prenom', '')
                if prenom:
                    display_name = f"{char_key} ({prenom})"
                else:
                    display_name = char_key.upper()
            else:
                display_name = char_key.upper()
        else:
            # Si pas dans les définitions, utiliser juste la lettre
            display_name = char_key.upper()
        
        characters_list.append(display_name)
    
    return characters_list

def _get_speaker_key_from_display_name(display_name):
    """Extrait la lettre du locuteur depuis le nom d'affichage de la combobox"""
    if not display_name or display_name == "Narrateur (aucun locuteur)":
        return None
    
    # Extraire la lettre (premier mot avant l'espace ou parenthèse)
    import re
    match = re.match(r'^(\w+)', display_name)
    if match:
        return match.group(1).lower()
    
    return None

def _create_normal_vo_interface_with_grid(main_interface):
    """Crée l'interface VO normale avec le thème sombre."""
    theme = theme_manager.get_theme()
    editor_font = ('Segoe UI', main_interface.editor_font_size_var.get())

    for widget in main_interface.vo_content_container.winfo_children():
        widget.destroy()

    # ✅ NOUVEAU : Réorganiser la grille pour inclure le champ locuteur
    main_interface.vo_content_container.grid_rowconfigure(0, weight=0)  # Locuteur (fixe)
    main_interface.vo_content_container.grid_rowconfigure(1, weight=1)  # Zone texte (expandable)
    main_interface.vo_content_container.grid_rowconfigure(2, weight=0)  # Boutons (fixe)

    # ✅ NOUVEAU : Frame pour le locuteur au-dessus
    speaker_frame = tk.Frame(main_interface.vo_content_container, bg=theme["bg"])
    speaker_frame.grid(row=0, column=0, sticky='ew', pady=(0, 5))
    speaker_frame.grid_columnconfigure(1, weight=1)

    tk.Label(
        speaker_frame,
        text="Locuteur:",
        font=('Segoe UI', 9, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    ).grid(row=0, column=0, padx=(0, 5), sticky='w')

    # Combobox pour sélectionner le locuteur
    if not hasattr(main_interface, 'vo_speaker_combo_var'):
        main_interface.vo_speaker_combo_var = tk.StringVar()
    
    characters_list = _get_characters_list_for_combobox(main_interface)
    main_interface.vo_speaker_combo = ttk.Combobox(
        speaker_frame,
        textvariable=main_interface.vo_speaker_combo_var,
        values=characters_list,
        state='readonly',
        font=('Segoe UI', 9),
        width=25
    )
    main_interface.vo_speaker_combo.grid(row=0, column=1, sticky='ew', padx=(0, 5))
    
    # Callback pour sauvegarder la modification
    def on_speaker_changed(event=None):
        selected_display = main_interface.vo_speaker_combo_var.get()
        new_speaker_key = _get_speaker_key_from_display_name(selected_display)
        if new_speaker_key is not None or selected_display == "Narrateur (aucun locuteur)":
            _save_speaker_key_modification(main_interface, new_speaker_key)
    
    main_interface.vo_speaker_combo.bind('<<ComboboxSelected>>', on_speaker_changed)
    
    # Mettre à jour la liste des personnages dans la combobox
    main_interface.vo_speaker_combo['values'] = characters_list

    # ✅ MODIFIÉ : Application du thème sombre sans dimensions fixes (pour permettre le word wrap)
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
    vo_text.grid(row=1, column=0, sticky='nsew', pady=(0, 5))
    main_interface.vo_text_widget = vo_text

    vo_buttons_frame = tk.Frame(main_interface.vo_content_container, bg=theme["bg"])
    vo_buttons_frame.grid(row=2, column=0, pady=8)

    tk.Button(
        vo_buttons_frame, text="Copier",
        command=lambda: copy_vo_text_simple(main_interface),
        bg=theme["button_utility_bg"], fg="#000000",
        font=('Segoe UI', 9, 'normal'), pady=4, padx=8
    ).pack(side='left', padx=(0, 5))

    tk.Button(
        vo_buttons_frame, text="Traduire en ligne",
        command=lambda: copy_and_open_translator(main_interface, main_interface.vo_text_widget.get('1.0', tk.END).strip(), "VO simple"),
        bg=theme["button_tertiary_bg"], fg="#000000",
        font=('Segoe UI', 9, 'normal'), pady=4, padx=8
    ).pack(side='left', padx=(0, 5))


    main_interface.vo_split_mode = False


def _create_normal_vf_interface_with_grid_and_buttons(main_interface):
    """Crée l'interface VF normale avec le thème sombre."""
    theme = theme_manager.get_theme()
    editor_font = ('Segoe UI', main_interface.editor_font_size_var.get())

    for widget in main_interface.vf_content_container.winfo_children():
        widget.destroy()

    # ✅ NOUVEAU : Réorganiser la grille pour inclure le champ locuteur
    main_interface.vf_content_container.grid_rowconfigure(0, weight=0)  # Locuteur (fixe)
    main_interface.vf_content_container.grid_rowconfigure(1, weight=1)  # Zone texte (expandable)
    main_interface.vf_content_container.grid_rowconfigure(2, weight=0)  # Boutons (fixe)

    # ✅ NOUVEAU : Frame pour le locuteur au-dessus
    speaker_frame = tk.Frame(main_interface.vf_content_container, bg=theme["bg"])
    speaker_frame.grid(row=0, column=0, sticky='ew', pady=(0, 5))
    speaker_frame.grid_columnconfigure(1, weight=1)

    tk.Label(
        speaker_frame,
        text="Locuteur:",
        font=('Segoe UI', 9, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    ).grid(row=0, column=0, padx=(0, 5), sticky='w')

    # Combobox pour sélectionner le locuteur
    if not hasattr(main_interface, 'vf_speaker_combo_var'):
        main_interface.vf_speaker_combo_var = tk.StringVar()
    
    characters_list = _get_characters_list_for_combobox(main_interface)
    main_interface.vf_speaker_combo = ttk.Combobox(
        speaker_frame,
        textvariable=main_interface.vf_speaker_combo_var,
        values=characters_list,
        state='readonly',
        font=('Segoe UI', 9),
        width=25
    )
    main_interface.vf_speaker_combo.grid(row=0, column=1, sticky='ew', padx=(0, 5))
    
    # Callback pour sauvegarder la modification
    def on_speaker_changed(event=None):
        selected_display = main_interface.vf_speaker_combo_var.get()
        new_speaker_key = _get_speaker_key_from_display_name(selected_display)
        if new_speaker_key is not None or selected_display == "Narrateur (aucun locuteur)":
            _save_speaker_key_modification(main_interface, new_speaker_key)
    
    main_interface.vf_speaker_combo.bind('<<ComboboxSelected>>', on_speaker_changed)

    # ✅ MODIFIÉ : Application du thème sombre sans dimensions fixes (pour permettre le word wrap)
    vf_text = tk.Text(main_interface.vf_content_container, wrap='word', font=editor_font,
                     bg=theme["entry_bg"], fg=theme["accent"], relief='solid', borderwidth=1,
                     insertbackground='#1976d2', highlightbackground='#666666'
                     )
    vf_text.grid(row=1, column=0, sticky='nsew', pady=(0, 5))
    main_interface.vf_text_widget = vf_text
    main_interface.vf_text_widget_2 = None

    vf_buttons_frame = tk.Frame(main_interface.vf_content_container, bg=theme["bg"])
    vf_buttons_frame.grid(row=2, column=0, pady=8)

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
        # ✅ MODIFIÉ : Application du thème sombre sans dimensions fixes (pour permettre le word wrap)
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
            speaker_buttons_frame, text="Traduire en ligne",
            command=lambda: copy_and_open_translator(main_interface, speaker_widget.get('1.0', tk.END).strip(), "locuteur VO"),
            bg=theme["button_tertiary_bg"], fg="#000000", font=('Segoe UI', 9), pady=4, padx=8
        ).pack(side='left', padx=(0, 5))


        # --- Widget Dialogue (VO) ---
        dialogue_container = tk.Frame(main_interface.vo_content_container, bg=theme["bg"]); dialogue_container.grid(row=0, column=1, sticky='nsew', padx=(2, 0))
        dialogue_container.grid_rowconfigure(0, weight=0); dialogue_container.grid_rowconfigure(1, weight=1); dialogue_container.grid_rowconfigure(2, weight=0); dialogue_container.grid_columnconfigure(0, weight=1)
        tk.Label(dialogue_container, text="Dialogue Original", font=('Segoe UI', 9, 'bold'), bg=theme["bg"], fg=theme["fg"]).grid(row=0, column=0, sticky='w', pady=(0, 2))
        # ✅ MODIFIÉ : Application du thème sombre sans dimensions fixes (pour permettre le word wrap)
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
            dialogue_buttons_frame, text="Traduire en ligne",
            command=lambda: copy_and_open_translator(main_interface, dialogue_widget.get('1.0', tk.END).strip(), "dialogue VO"),
            bg=theme["button_tertiary_bg"], fg="#000000", font=('Segoe UI', 9), pady=4, padx=8
        ).pack(side='left', padx=(0, 5))


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
        copy_and_open_translator(main_interface, vo_text, "VO simple")
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
            copy_and_open_translator(main_interface, speaker_text, "locuteur VO")
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
        copy_and_open_translator(main_interface, vo_text, "dialogue VO")
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

    # ✅ Ajout du header pour la fenêtre détachée
    if is_detached:
        edit_main.grid_rowconfigure(0, weight=0)  # Header
        edit_main.grid_rowconfigure(1, weight=1)  # Zones de texte
        edit_main.grid_rowconfigure(2, weight=0)  # Boutons globaux
    else:
        edit_main.grid_rowconfigure(0, weight=0)  # Zones de texte
        edit_main.grid_rowconfigure(1, weight=1)
        edit_main.grid_rowconfigure(2, weight=0)  # Boutons globaux

    edit_main.grid_columnconfigure(0, weight=1, minsize=200); edit_main.grid_columnconfigure(1, weight=1, minsize=300)

    # ✅ HEADER SEULEMENT POUR LA FENÊTRE DÉTACHÉE
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

        _build_editor_controls(header_frame, main_interface, is_detached=True)

    text_areas_frame = tk.Frame(edit_main, bg=theme["bg"])
    text_areas_frame.grid(row=1 if is_detached else 0, column=0, columnspan=2, sticky='nsew' if is_detached else 'ew')
    text_areas_frame.grid_columnconfigure(0, weight=1); text_areas_frame.grid_columnconfigure(1, weight=1)

    vo_grid_frame = tk.Frame(text_areas_frame, bg=theme["bg"]); vo_grid_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
    # ✅ Fixer une hauteur pour empêcher les textes de pousser les boutons (augmentée pour laisser place aux boutons)
    vo_grid_frame.configure(height=280)
    tk.Label(vo_grid_frame, text="Textes Originaux", font=('Segoe UI', 10, 'bold'), bg=theme["bg"], fg=theme["fg"]).pack(anchor='w', pady=(0, 5))
    vo_grid_container = tk.Frame(vo_grid_frame, bg=theme["bg"]); vo_grid_container.pack(fill='both', expand=True)
    vo_grid_frame.grid_propagate(False)  # Empêcher le container de s'étendre
    
    grid_rows, grid_cols = dialogue_group['grid_rows'], dialogue_group['grid_cols']
    for r in range(grid_rows): vo_grid_container.grid_rowconfigure(r, weight=1)
    for c in range(grid_cols): vo_grid_container.grid_columnconfigure(c, weight=1)
    
    main_interface.multiple_vo_widgets = []
    vo_dialogues = dialogue_group.get('vo_dialogues', [])
    for i in range(min(len(vo_dialogues), grid_rows * grid_cols)):
        row, col = i // grid_cols, i % grid_cols
        vo_dialogue_container = tk.Frame(vo_grid_container, bg=theme["bg"]); vo_dialogue_container.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        # ✅ Configuration des rangées pour garantir l'espace des boutons
        vo_dialogue_container.grid_rowconfigure(0, weight=0, minsize=25)  # Label
        vo_dialogue_container.grid_rowconfigure(1, weight=1, minsize=60)   # Text widget - weight=1 pour occuper l'espace
        vo_dialogue_container.grid_rowconfigure(2, weight=0, minsize=40)   # Boutons
        vo_dialogue_container.grid_columnconfigure(0, weight=1)
        tk.Label(vo_dialogue_container, text=f"Original {i+1}", font=('Segoe UI', 9, 'bold'), bg=theme["bg"], fg=theme["fg"]).grid(row=0, column=0, sticky='w', padx=3, pady=(3, 2))
        # ✅ MODIFIÉ : Hauteur minimale (1 ligne) qui s'adapte à l'espace du container
        vo_widget = tk.Text(
            vo_dialogue_container,
            wrap='word',
            font=editor_font,
            bg=theme["entry_bg"],
            fg=theme["fg"],
            relief='solid',
            borderwidth=1,
            height=1,
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
            vo_buttons_multiple_frame, text="Traduire en ligne",
            command=lambda idx=i: copy_and_open_translator(main_interface, main_interface.multiple_vo_widgets[idx].get('1.0', tk.END).strip(), f"original {idx + 1}"),
            bg=theme["button_tertiary_bg"], fg="#000000", font=('Segoe UI', 9), pady=4, padx=8
        ).pack(side='left', padx=(0, 5))
        vo_widget.dialogue_info = vo_dialogues[i] if i < len(vo_dialogues) else {}; vo_widget.dialogue_index = i
        main_interface.multiple_vo_widgets.append(vo_widget)

    vf_grid_frame = tk.Frame(text_areas_frame, bg=theme["bg"]); vf_grid_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
    # ✅ Fixer une hauteur pour empêcher les textes de pousser les boutons (augmentée pour laisser place aux boutons)
    vf_grid_frame.configure(height=280)
    tk.Label(vf_grid_frame, text=f"Traductions ({dialogue_group['group_size']} dialogues)", font=('Segoe UI', 10, 'bold'), bg=theme["bg"], fg=theme["fg"]).pack(anchor='w', pady=(0, 5))
    vf_grid_container = tk.Frame(vf_grid_frame, bg=theme["bg"]); vf_grid_container.pack(fill='both', expand=True)
    vf_grid_frame.grid_propagate(False)  # Empêcher le container de s'étendre
    
    for r in range(grid_rows): vf_grid_container.grid_rowconfigure(r, weight=1)
    for c in range(grid_cols): vf_grid_container.grid_columnconfigure(c, weight=1)
    
    main_interface.multiple_vf_widgets = []
    dialogues = dialogue_group['dialogues']
    for i, dialogue in enumerate(dialogues):
        if i >= grid_rows * grid_cols: break
        row, col = i // grid_cols, i % grid_cols
        vf_dialogue_container = tk.Frame(vf_grid_container, bg=theme["bg"]); vf_dialogue_container.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        # ✅ Configuration des rangées pour garantir l'espace des boutons
        vf_dialogue_container.grid_rowconfigure(0, weight=0, minsize=25)  # Label
        vf_dialogue_container.grid_rowconfigure(1, weight=1, minsize=60)   # Text widget - weight=1 pour occuper l'espace
        vf_dialogue_container.grid_rowconfigure(2, weight=0, minsize=40)   # Bouton
        vf_dialogue_container.grid_columnconfigure(0, weight=1)
        tk.Label(vf_dialogue_container, text=f"Traduction {i+1}", font=('Segoe UI', 9, 'bold'), bg=theme["bg"], fg=theme["fg"]).grid(row=0, column=0, sticky='w', padx=3, pady=(3, 2))
        # ✅ MODIFIÉ : Hauteur minimale (1 ligne) qui s'adapte à l'espace du container
        vf_widget = tk.Text(
            vf_dialogue_container,
            wrap='word',
            font=editor_font,
            bg=theme["entry_bg"],
            fg=theme["accent"],
            relief='solid',
            borderwidth=1,
            height=1,
            insertbackground='#1976d2',
            highlightbackground='#666666'
        )
        vf_widget.grid(row=1, column=0, sticky='nsew', padx=3, pady=2)
        tk.Button(vf_dialogue_container, text="Coller", command=lambda idx=i: paste_to_multiple_vf_text(main_interface, idx), bg=theme["button_primary_bg"], fg="#000000", font=('Segoe UI', 9, 'normal'), pady=4, padx=8).grid(row=2, column=0, padx=3, pady=(2, 3))
        vf_widget.dialogue_info = dialogue; vf_widget.dialogue_index = i
        main_interface.multiple_vf_widgets.append(vf_widget)
    # --- Boutons globaux ---
    buttons_frame = tk.Frame(edit_main, bg=theme["bg"])
    # ✅ Placer les boutons globaux SOUS les dialogues (row 2 en mode détaché)
    if is_detached:
        buttons_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10, 8), padx=(0, 8))
    else:
        buttons_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10, 0))

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
                copy_and_open_translator(main_interface, vo_text, f"original {widget_index + 1}")
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

def _calculate_detached_window_size(dialogue_info: Dict) -> str:
    """
    Calcule la taille optimale de la fenêtre détachée en fonction du contenu.
    
    Args:
        dialogue_info: Informations sur le dialogue/menu actuel
        
    Returns:
        Géométrie au format "WIDTHxHEIGHT" (ex: "1200x450")
    """
    # Constantes de dimensionnement
    BASE_HEIGHT = 120        # Hauteur pour les contrôles (header + boutons)
    CELL_HEIGHT = 150        # Hauteur d'une cellule de grille (widget + label + boutons)
    MIN_HEIGHT = 300         # Hauteur minimale
    MAX_HEIGHT = 900         # Hauteur maximale (ne pas dépasser l'écran)
    DEFAULT_WIDTH = 1200
    
    try:
        if dialogue_info.get('is_menu'):
            # Menu de choix : calculer selon le nombre de choix
            nb_choices = len(dialogue_info.get('choices', []))
            grid_cols = 2  # Grille sur 2 colonnes
            grid_rows = (nb_choices + grid_cols - 1) // grid_cols  # Arrondi supérieur
            height = BASE_HEIGHT + (grid_rows * CELL_HEIGHT)
            
        elif dialogue_info.get('is_multiple_group'):
            # Dialogues multiples : utiliser grid_rows déjà calculé
            grid_rows = dialogue_info.get('grid_rows', 1)
            height = BASE_HEIGHT + (grid_rows * CELL_HEIGHT)
            
        else:
            # Dialogue simple : taille par défaut
            height = MIN_HEIGHT
        
        # Limiter entre min et max
        height = max(MIN_HEIGHT, min(height, MAX_HEIGHT))
        
        return f"{DEFAULT_WIDTH}x{height}"
        
    except Exception as e:
        log_message("ATTENTION", f"Erreur calcul taille fenêtre: {e}", category="realtime_editor")
        return f"{DEFAULT_WIDTH}x{MIN_HEIGHT}"


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

    # Construire la fenêtre détachée avec taille adaptative
    theme = theme_manager.get_theme()
    window = tk.Toplevel(main_interface.window)
    window.title("Éditeur Temps Réel")
    
    # ✅ Appliquer le thème à la fenêtre Toplevel
    window.configure(bg=theme["bg"])
    
    # ✅ Calculer la taille optimale selon le contenu actuel
    if hasattr(main_interface, 'current_dialogue_info') and main_interface.current_dialogue_info:
        geometry = _calculate_detached_window_size(main_interface.current_dialogue_info)
    else:
        geometry = "1200x300"
    
    window.geometry(geometry)
    window.minsize(500, 200)
    main_interface.detached_editor_window = window

    main_interface.realtime_edit_main = _build_editor_panel(window, main_interface, is_detached=True)
    # ✅ Réduire les paddings pour éviter les zones blanches
    main_interface.realtime_edit_main.pack(fill='both', expand=True, padx=0, pady=0)

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


def install_monitoring_module(main_interface, force_v2=False):
    """Installe le module de surveillance dans le projet Ren'Py."""
    try:
        if not main_interface.current_project_path:
            main_interface._show_notification("Veuillez sélectionner un projet Ren'Py", "warning"); return
        language = main_interface.realtime_language_var.get().strip().lower()
        if not language:
            main_interface._show_notification("Veuillez spécifier une langue cible", "warning"); return
        
        # Version manuelle désactivée - utilisation de la détection automatique uniquement
        manual_version = None
        
        # ✅ NOUVEAU : Forcer le module v2 si demandé
        force_module_version = "v2" if force_v2 else None
        
        main_interface._update_status("Installation du module de surveillance...")
        biz = main_interface._get_realtime_editor_business()
        result = biz.generate_monitoring_module(
            project_path=main_interface.current_project_path, 
            language=language,
            manual_version=manual_version,
            force_module_version=force_module_version
        )
        
        if result.get('success'):
            module_path = result.get('module_path', '')
            module_version = result.get('module_version', 'v1')
            
            # Message de succès avec infos sur la version
            if force_v2:
                success_msg = f"Module {module_version} installé (test de compatibilité) pour '{language}'"
            else:
                success_msg = f"Module {module_version} installé avec succès pour '{language}'"
            main_interface._update_status(success_msg)
            log_message("INFO", f"Module de surveillance installé: {module_path} (version {module_version})", category="realtime_editor")
            
            # Feedback si version inconnue ou module forcé
            if result.get('warnings') or force_v2:
                from infrastructure.helpers.unified_functions import show_custom_messagebox
                from ui.themes import theme_manager
                
                detected_version = result.get('renpy_version_detected')
                module_version = result.get('module_version', 'v1')
                
                if force_v2:
                    # Message spécial pour test de compatibilité v2
                    warning_message = [
                        ("🧪 Test de compatibilité - Module v2\n\n", "bold_green"),
                        (f"Version Ren'Py détectée : ", "normal"),
                        (f"{detected_version or 'Inconnue'}\n\n", "bold_blue"),
                        ("Le module v2 a été installé manuellement pour test.\n\n", "normal"),
                        ("📋 Instructions de test :\n", "bold"),
                        ("1. Lancez votre jeu Ren'Py\n", "normal"),
                        ("2. Testez l'éditeur temps réel (surveillance + traduction)\n", "normal"),
                        ("3. Vérifiez que tout fonctionne correctement\n\n", "normal"),
                        ("💡 Si le module v2 fonctionne :\n", "bold_green"),
                        ("   → Utilisez le bouton 'Tester module v2' pour continuer à l'utiliser\n\n", "normal"),
                        ("⚠️ Si le module v2 ne fonctionne pas :\n", "bold_yellow"),
                        ("   → Réinstallez avec 'Installer le module' pour revenir au module recommandé\n\n", "normal"),
                        ("📧 Important : ", "bold"),
                        ("Merci de signaler le résultat du test (version Ren'Py + module testé + résultat) pour mettre à jour le tableau de compatibilité !\n\n", "normal"),
                        ("Rapportez sur GitHub ou par email.", "italic")
                    ]
                    
                    show_custom_messagebox(
                        "info",
                        "Test de compatibilité - Module v2",
                        warning_message,
                        theme_manager.get_theme(),
                        parent=main_interface.window
                    )
                else:
                    # Message pour version inconnue (comportement normal)
                    warning_message = [
                        ("⚠️ Version Ren'Py inconnue détectée\n\n", "bold"),
                        (f"Version détectée : ", "normal"),
                        (f"{detected_version}\n\n", "bold_blue"),
                        (f"Le module {module_version} sera utilisé par défaut.\n\n", "normal"),
                        ("🧪 Test de compatibilité disponible :\n", "bold_green"),
                        ("Si vous rencontrez des problèmes, vous pouvez tester le module v2 avec le bouton ", "normal"),
                        ("'Tester module v2'", "bold_yellow"),
                        (" pour vérifier la compatibilité.\n\n", "normal"),
                        ("📋 Après test, merci de signaler :\n", "bold"),
                        ("• La version Ren'Py testée\n", "normal"),
                        ("• Le module utilisé (v1 ou v2)\n", "normal"),
                        ("• Le résultat (fonctionne / ne fonctionne pas)\n\n", "normal"),
                        ("📧 Contact : ", "bold"),
                        ("Rapportez sur GitHub ou par email pour mettre à jour le tableau de compatibilité.", "normal")
                    ]
                    
                    show_custom_messagebox(
                        "warning",
                        "Version Ren'Py inconnue",
                        warning_message,
                        theme_manager.get_theme(),
                        parent=main_interface.window
                    )
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
                    # Enregistrer le callback de focus
                    set_focus_callback(_focus_cb)
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
            
            # Mettre à jour le statut avec le nombre de modifications en attente
            update_status_with_pending_count(main_interface)
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
           
           # Mettre à jour le statut avec le nombre de modifications en attente
           update_status_with_pending_count(main_interface)
           
           # Afficher les informations de nettoyage
           cleaned_files = result.get('cleaned_files', [])
           if cleaned_files:
               cleanup_msg = f"Surveillance arrêtée\n\nFichiers temporaires nettoyés:\n• " + "\n• ".join(cleaned_files)
               main_interface._show_notification(cleanup_msg, "info")
           else:
               log_message("INFO", "Arrêt surveillance - aucun fichier temporaire à nettoyer", category="realtime_editor")
           
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
            type_name = {'simple': 'Modifications simples', 'split': 'Divisions', 'speaker_dialogue': 'Locuteur + dialogue', 'merge': 'Fusions', 'menu_choice': 'Choix de menu', 'multiple_dialogue': 'Dialogues multiples'}.get(mod_type, f'Type {mod_type}')
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
            # ✅ Maintenant on gère aussi les menus dans _save_current_modification_if_changed
            _save_current_modification_if_changed(main_interface)

        # --- DÉBUT DE LA LOGIQUE DE TRANSITION CORRIGÉE ---
        was_in_menu = getattr(main_interface, 'is_in_menu_mode', False)
        was_in_multiple = getattr(main_interface, 'is_in_multiple_mode', False)
        was_in_split = getattr(main_interface, 'is_in_split_mode', False)

        is_currently_menu = dialogue_info.get('is_menu', False)
        is_currently_multiple = dialogue_info.get('is_multiple_group', False)
        
        # Déterminer si on est actuellement en mode split (speaker_dialogue ou multiline)
        dialogue_structure = _analyze_dialogue_structure(main_interface, dialogue_info) if not (is_currently_menu or is_currently_multiple) else {'is_split': False}
        is_currently_split = dialogue_structure.get('is_split', False) and dialogue_structure.get('split_type') in ['speaker_dialogue', 'multiline']

        main_interface.is_in_menu_mode = is_currently_menu
        main_interface.is_in_multiple_mode = is_currently_multiple
        main_interface.is_in_split_mode = is_currently_split

        # On reconstruit l'interface si on sort d'un mode spécial (Menu OU Multiple OU Split)
        if (was_in_menu and not is_currently_menu) or (was_in_multiple and not is_currently_multiple) or (was_in_split and not is_currently_split):
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
            
            # ✅ Ajuster la taille de la fenêtre détachée lors de la reconstruction
            if is_detached:
                geometry = _calculate_detached_window_size(dialogue_info)
                main_interface.detached_editor_window.geometry(geometry)
            
            main_interface.realtime_edit_main = _build_editor_panel(parent, main_interface, is_detached)
            # ✅ Réduire les paddings pour éviter les zones blanches en mode détaché
            padding = 0 if is_detached else 15
            main_interface.realtime_edit_main.pack(fill='both', expand=True, padx=padding, pady=padding)
        # --- FIN DE LA LOGIQUE DE TRANSITION ---

        # Aiguillage principal (inchangé)
        if is_currently_menu:
            _update_for_menu_choices(main_interface, dialogue_info)
        elif is_currently_multiple:
            _update_for_multiple_dialogue(main_interface, dialogue_info)
        else:
            original_text = dialogue_info.get('original_text', "")
            
            # ✅ Ajuster la taille de la fenêtre détachée pour les dialogues simples
            is_detached = bool(main_interface.detached_editor_window and main_interface.detached_editor_window.winfo_exists())
            if is_detached:
                geometry = _calculate_detached_window_size(dialogue_info)
                main_interface.detached_editor_window.geometry(geometry)
            
            if dialogue_structure.get('split_type') == 'speaker_dialogue':
                vo_type_analysis = _analyze_original_text_type(original_text, dialogue_structure)
                _handle_unnamed_speaker_update(main_interface, vo_type_analysis, dialogue_structure, dialogue_info)
            elif dialogue_structure.get('is_split') and dialogue_structure.get('split_type') == 'multiline':
                vo_type_analysis = {'type': 'multiline', 'dialogue': original_text}
                _handle_multiline_update(main_interface, vo_type_analysis, dialogue_structure, original_text, dialogue_info)
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
    
    # ✅ Si fenêtre détachée, ajuster sa taille selon le nombre de choix
    if is_detached:
        geometry = _calculate_detached_window_size(menu_info)
        main_interface.detached_editor_window.geometry(geometry)
    
    main_interface.realtime_edit_main = _build_menu_choices_interface(parent, main_interface, menu_info, is_detached)
    # ✅ Réduire les paddings pour éviter les zones blanches en mode détaché
    padding = 0 if is_detached else 15
    main_interface.realtime_edit_main.pack(fill='both', expand=True, padx=padding, pady=padding)

def _build_menu_choices_interface(parent_container, main_interface, menu_info, is_detached=False):
    """
    Construit l'interface pour les choix de menu en utilisant une grille harmonisée
    avec l'affichage des dialogues multiples.
    """
    theme = theme_manager.get_theme()
    editor_font = ('Segoe UI', main_interface.editor_font_size_var.get())
    
    edit_main = tk.Frame(parent_container, bg=theme["bg"])

    # === Conteneur scrollable (Canvas + Scrollbar) pour gérer >10 choix ===
    # Le header et tout le contenu sont placés dans un inner_frame scrolable.
    scroll_container = tk.Frame(edit_main, bg=theme["bg"])
    scroll_container.pack(fill='both', expand=True)
    canvas = tk.Canvas(scroll_container, bg=theme["bg"], highlightthickness=0)
    canvas.pack(side='left', fill='both', expand=True)
    v_scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
    v_scrollbar.pack(side='right', fill='y')
    canvas.configure(yscrollcommand=v_scrollbar.set)
    inner_frame = tk.Frame(canvas, bg=theme["bg"])
    inner_window = canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    def _update_scroll_region(event=None):
        try:
            canvas.configure(scrollregion=canvas.bbox("all"))
        except Exception:
            pass
    inner_frame.bind("<Configure>", _update_scroll_region)

    def _on_canvas_configure(event):
        """Ajuste la largeur de l'inner_frame pour éviter les débordements horizontaux."""
        try:
            canvas.itemconfig(inner_window, width=event.width)
        except Exception:
            pass
    canvas.bind("<Configure>", _on_canvas_configure)

    # Support molette (Windows/Linux)
    def _on_mousewheel(event):
        try:
            delta = event.delta
            if delta == 0 and hasattr(event, 'num'):
                # Compat X11: Button-4/5
                if event.num == 4:
                    delta = 120
                elif event.num == 5:
                    delta = -120
            canvas.yview_scroll(int(-1 * (delta / 120)), "units")
        except Exception:
            pass
    # Binder sur le conteneur et ses enfants
    inner_frame.bind_all("<MouseWheel>", _on_mousewheel)
    inner_frame.bind_all("<Button-4>", _on_mousewheel)
    inner_frame.bind_all("<Button-5>", _on_mousewheel)

    # ✅ HEADER SEULEMENT POUR LA FENÊTRE DÉTACHÉE
    if is_detached:
        header_frame = tk.Frame(inner_frame, bg=theme["bg"])
        header_frame.pack(fill='x', padx=15, pady=(5, 10))

        if hasattr(main_interface, 'monitor_status_label'):
            current_text = main_interface.monitor_status_label.cget("text")
            current_fg = main_interface.monitor_status_label.cget("fg")
        else:
            current_text = "⭕ Surveillance arrêtée"
            current_fg = '#dc3545'
        
        status_label = tk.Label(header_frame, text=current_text, font=('Segoe UI', 9, 'bold'), bg=theme["bg"], fg=current_fg)
        status_label.pack(side='left')

        _build_editor_controls(header_frame, main_interface, is_detached=True)

    # --- Titre principal ---
    title_frame = tk.Frame(inner_frame, bg=theme["bg"])
    title_frame.pack(fill='x', pady=(0, 5), padx=5)
    choices = menu_info.get('choices', [])
    tk.Label(
        title_frame,
        text=f"📋 Menu de choix ({len(choices)} options)",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"], fg=theme["fg"]
    ).pack(side='left')

    # --- Conteneur principal pour les grilles VO et VF ---
    text_areas_frame = tk.Frame(inner_frame, bg=theme["bg"])
    text_areas_frame.pack(fill='both', expand=True)
    text_areas_frame.grid_columnconfigure(0, weight=1)
    text_areas_frame.grid_columnconfigure(1, weight=1)

    # --- Colonne gauche : VO ---
    vo_grid_frame = tk.Frame(text_areas_frame, bg=theme["bg"])
    vo_grid_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
    vo_grid_frame.configure(height=280)  # Hauteur fixe pour empêcher les textes de pousser les boutons (augmentée)
    vo_grid_frame.grid_propagate(False)
    tk.Label(vo_grid_frame, text="Choix Originaux (VO)", font=('Segoe UI', 10, 'bold'),
             bg=theme["bg"], fg=theme["fg"]).pack(anchor='w', pady=(0, 5))
    vo_grid_container = tk.Frame(vo_grid_frame, bg=theme["bg"])
    vo_grid_container.pack(fill='both', expand=True)

    # --- Colonne droite : VF ---
    vf_grid_frame = tk.Frame(text_areas_frame, bg=theme["bg"])
    vf_grid_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
    vf_grid_frame.configure(height=280)  # Hauteur fixe pour empêcher les textes de pousser les boutons (augmentée)
    vf_grid_frame.grid_propagate(False)
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
        vo_container.grid_rowconfigure(0, weight=0, minsize=25)  # Label
        vo_container.grid_rowconfigure(1, weight=1, minsize=50)  # Text widget
        vo_container.grid_rowconfigure(2, weight=0, minsize=40)  # Boutons
        vo_container.grid_columnconfigure(0, weight=1)

        tk.Label(vo_container, text=f"Choix {i+1}", font=('Segoe UI', 9, 'normal'),
                 bg=theme["bg"], fg=theme["fg"]).grid(row=0, column=0, sticky='w', padx=3, pady=(3, 2))

        vo_text = tk.Text(
            vo_container, wrap='word', font=editor_font,
            bg=theme["entry_bg"], fg=theme["fg"],
            relief='solid', borderwidth=1, height=1, state='disabled',
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
            vo_buttons, text="Traduire en ligne",
            command=lambda idx=i: copy_and_open_translator(main_interface, main_interface.menu_vo_widgets[idx].get('1.0', tk.END).strip(), f"choix {idx + 1}"),
            bg=theme["button_tertiary_bg"], fg="#000000", font=('Segoe UI', 9), pady=4, padx=8
        ).pack(side='left', padx=(0, 5))

        # VF
        vf_container = tk.Frame(vf_grid_container, bg=theme["bg"])
        vf_container.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        vf_container.grid_rowconfigure(0, weight=0, minsize=25)  # Label
        vf_container.grid_rowconfigure(1, weight=1, minsize=50)  # Text widget
        vf_container.grid_rowconfigure(2, weight=0, minsize=40)  # Bouton
        vf_container.grid_columnconfigure(0, weight=1)

        tk.Label(vf_container, text=f"Traduction {i+1}", font=('Segoe UI', 9, 'normal'),
                 bg=theme["bg"], fg=theme["fg"]).grid(row=0, column=0, sticky='w', padx=3, pady=(3, 2))

        vf_text = tk.Text(
            vf_container, wrap='word', font=editor_font,
            bg=theme["entry_bg"], fg=theme["accent"],
            relief='solid', borderwidth=1, height=1,
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
    buttons_frame = tk.Frame(inner_frame, bg=theme["bg"])
    # ✅ Ajouter un petit espace en bas et à droite en mode détaché
    if is_detached:
        buttons_frame.pack(fill='x', pady=(10, 8), padx=(0, 8))
    else:
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
            copy_and_open_translator(main_interface, vo_text, f"choix {index + 1}")
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
    
    # ✅ Si fenêtre détachée, ajuster sa taille selon le nombre de dialogues
    if is_detached:
        geometry = _calculate_detached_window_size(dialogue_info)
        main_interface.detached_editor_window.geometry(geometry)
            
    main_interface.realtime_edit_main = _build_editor_panel(parent, main_interface, is_detached)
    # ✅ Réduire les paddings pour éviter les zones blanches en mode détaché
    padding = 0 if is_detached else 15
    main_interface.realtime_edit_main.pack(fill='both', expand=True, padx=padding, pady=padding)
    
    _populate_multiple_widgets_separated(main_interface, dialogue_info)

# ### REFACTORISATION ###: Fonction spécialisée pour le cas "Locuteur non défini"
def _handle_unnamed_speaker_update(main_interface, dialogue_type, dialogue_structure, dialogue_info):
    """Met à jour l'UI pour un dialogue de type 'locuteur' 'dialogue'."""
    # ✅ CORRECTION : Utiliser dialogue_info passé en paramètre au lieu de current_dialogue_info
    # (car current_dialogue_info contient encore l'ancien dialogue)
    original_full_text = dialogue_info.get('original_text', '')
    
    # ✅ NOUVEAU : Afficher le nom du locuteur (pour référence, même en mode split)
    speaker_key = dialogue_info.get('speaker_key')
    modified_speaker_key = dialogue_info.get('modified_speaker_key')
    
    current_speaker_key = modified_speaker_key if modified_speaker_key is not None else speaker_key
    
    characters_list = _get_characters_list_for_combobox(main_interface)
    display_name = "Narrateur (aucun locuteur)"
    
    if current_speaker_key:
        for item in characters_list:
            if item.startswith(f"{current_speaker_key} "):
                display_name = item
                break
        else:
            display_name = _get_character_display_name(current_speaker_key, main_interface)
    
    if hasattr(main_interface, 'vo_speaker_combo_var'):
        main_interface.vo_speaker_combo_var.set(display_name)
    if hasattr(main_interface, 'vf_speaker_combo_var'):
        main_interface.vf_speaker_combo_var.set(display_name)
    
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
def _handle_multiline_update(main_interface, dialogue_type, dialogue_structure, original_text, dialogue_info):
    """Met à jour l'UI pour un dialogue divisé sur plusieurs lignes."""
    if getattr(main_interface, 'vo_split_mode', False):
        _create_normal_vo_interface_with_grid(main_interface)
    
    # ✅ NOUVEAU : Afficher le nom du locuteur
    speaker_key = dialogue_info.get('speaker_key')
    modified_speaker_key = dialogue_info.get('modified_speaker_key')
    
    current_speaker_key = modified_speaker_key if modified_speaker_key is not None else speaker_key
    
    characters_list = _get_characters_list_for_combobox(main_interface)
    display_name = "Narrateur (aucun locuteur)"
    
    if current_speaker_key:
        for item in characters_list:
            if item.startswith(f"{current_speaker_key} "):
                display_name = item
                break
        else:
            display_name = _get_character_display_name(current_speaker_key, main_interface)
    
    if hasattr(main_interface, 'vo_speaker_combo_var'):
        main_interface.vo_speaker_combo_var.set(display_name)
    if hasattr(main_interface, 'vf_speaker_combo_var'):
        main_interface.vf_speaker_combo_var.set(display_name)
    
    # ✅ CORRECTION : Utiliser dialogue_info passé en paramètre au lieu de current_dialogue_info
    # (car current_dialogue_info contient encore l'ancien dialogue)
    vo_display_text = dialogue_info.get('original_text', original_text)
    if not vo_display_text or vo_display_text == dialogue_info.get('displayed_text', ''):
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
    # ✅ CORRECTION : Toujours recréer l'interface VO normale pour un dialogue simple
    # (même logique que pour l'interface VF, sans condition)
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
    
    # ✅ NOUVEAU : Afficher le nom du locuteur (après création des interfaces)
    speaker_key = dialogue_info.get('speaker_key')
    modified_speaker_key = dialogue_info.get('modified_speaker_key')
    
    # Utiliser la clé modifiée si disponible, sinon la clé originale
    current_speaker_key = modified_speaker_key if modified_speaker_key is not None else speaker_key
    
    # Trouver le nom d'affichage dans la liste
    characters_list = _get_characters_list_for_combobox(main_interface)
    display_name = "Narrateur (aucun locuteur)"
    
    if current_speaker_key:
        for item in characters_list:
            if item.startswith(f"{current_speaker_key} "):
                display_name = item
                break
        else:
            # Si pas trouvé, créer un nom d'affichage simple
            display_name = _get_character_display_name(current_speaker_key, main_interface)
    
    if hasattr(main_interface, 'vo_speaker_combo_var'):
        main_interface.vo_speaker_combo_var.set(display_name)
    if hasattr(main_interface, 'vf_speaker_combo_var'):
        main_interface.vf_speaker_combo_var.set(display_name)
    
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
                    
                    # CORRECTION : Pour la VO, toujours utiliser 'original_text' en priorité
                    # Si original_text n'existe pas, fallback sur dialogue_text
                    original_text = vo_dialogue_data.get('original_text', '')
                    if not original_text:
                        # Fallback : utiliser dialogue_text si original_text n'est pas renseigné
                        original_text = vo_dialogue_data.get('dialogue_text', '')
                    
                    # Formater le texte pour l'affichage
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

def _save_speaker_key_modification(main_interface, new_speaker_key):
    """Sauvegarde la modification de la lettre du locuteur et modifie le fichier source Ren'Py"""
    try:
        if not hasattr(main_interface, 'current_dialogue_info') or not main_interface.current_dialogue_info:
            return
        
        dialogue_info = main_interface.current_dialogue_info
        biz = main_interface._get_realtime_editor_business()
        
        # Récupérer le speaker_key original
        original_speaker_key = dialogue_info.get('speaker_key')
        
        # ✅ NOUVEAU : Modifier le fichier source Ren'Py
        source_file = dialogue_info.get('source_file')
        source_line = dialogue_info.get('source_line', 0)
        
        if source_file and source_line > 0 and main_interface.current_project_path:
            try:
                # Construire le chemin du fichier source
                source_file_path = os.path.join(main_interface.current_project_path, "game", source_file)
                if not os.path.exists(source_file_path):
                    source_file_path = os.path.join(main_interface.current_project_path, source_file)
                
                if os.path.exists(source_file_path):
                    # Créer un backup
                    from core.models.backup.unified_backup_manager import UnifiedBackupManager, BackupType
                    backup_manager = UnifiedBackupManager()
                    backup_result = backup_manager.create_backup(
                        source_file_path,
                        BackupType.REALTIME_EDIT,
                        f"Modification locuteur: {original_speaker_key} → {new_speaker_key}"
                    )
                    
                    # Lire le fichier
                    with open(source_file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    # Modifier la ligne source
                    target_index = source_line - 1
                    if 0 <= target_index < len(lines):
                        original_line = lines[target_index]
                        original_line_stripped = original_line.rstrip('\n\r')
                        
                        # ✅ DEBUG : Logger la ligne originale
                        log_message("DEBUG", f"Ligne originale: '{original_line_stripped}'", category="realtime_editor")
                        log_message("DEBUG", f"Locuteur original: '{original_speaker_key}' → Nouveau: '{new_speaker_key}'", category="realtime_editor")
                        
                        # ✅ APPROCHE SIMPLIFIÉE ET ROBUSTE : Extraire manuellement le contenu
                        # Extraire l'indentation
                        indent_match = re.match(r'^(\s*)', original_line_stripped)
                        indent = indent_match.group(1) if indent_match else ''
                        
                        # Trouver la position du premier guillemet ouvrant après le locuteur
                        # Chercher le pattern : espaces + locuteur + espaces + guillemet
                        speaker_pattern = re.compile(
                            r'^\s*' + re.escape(original_speaker_key) + r'\s+"',
                            re.IGNORECASE
                        )
                        
                        match = speaker_pattern.search(original_line_stripped)
                        
                        if match:
                            # Le locuteur a été trouvé
                            quote_start = match.end() - 1  # Position du guillemet ouvrant
                            
                            # Extraire le contenu entre guillemets en gérant les échappements
                            content_start = quote_start + 1
                            content = ""
                            i = content_start
                            while i < len(original_line_stripped):
                                if original_line_stripped[i] == '\\' and i + 1 < len(original_line_stripped):
                                    # Échappement : préserver \"
                                    content += original_line_stripped[i:i+2]
                                    i += 2
                                elif original_line_stripped[i] == '"':
                                    # Fin du contenu
                                    break
                                else:
                                    content += original_line_stripped[i]
                                    i += 1
                            
                            # Récupérer le reste de la ligne après le guillemet fermant
                            if i < len(original_line_stripped):
                                rest_of_line = original_line_stripped[i+1:]  # +1 pour sauter le guillemet fermant
                            else:
                                rest_of_line = ""
                            
                            # ✅ DEBUG : Logger le contenu extrait
                            log_message("DEBUG", f"Contenu extrait: '{content}'", category="realtime_editor")
                            log_message("DEBUG", f"Reste de la ligne: '{rest_of_line}'", category="realtime_editor")
                            
                            # Reconstruire la ligne avec le nouveau locuteur
                            if new_speaker_key:
                                new_line = f'{indent}{new_speaker_key} "{content}"{rest_of_line}'
                            else:
                                # Pas de locuteur (narrateur)
                                new_line = f'{indent}"{content}"{rest_of_line}'
                            
                            log_message("DEBUG", f"Nouvelle ligne: '{new_line}'", category="realtime_editor")
                        else:
                            # Le locuteur n'a pas été trouvé dans la ligne
                            log_message("ATTENTION", f"Locuteur '{original_speaker_key}' non trouvé dans: '{original_line_stripped}'", category="realtime_editor")
                            new_line = original_line_stripped
                        
                        # Préserver le saut de ligne original
                        if not new_line.endswith('\n') and original_line.endswith('\n'):
                            new_line += '\n'
                        elif new_line.endswith('\n') and not original_line.endswith('\n'):
                            new_line = new_line.rstrip('\n')
                        
                        if new_line != original_line:
                            lines[target_index] = new_line
                            
                            # Écrire le fichier modifié
                            with open(source_file_path, 'w', encoding='utf-8') as f:
                                f.writelines(lines)
                            
                            log_message("INFO", f"Fichier source modifié: {source_file}:{source_line} ({original_speaker_key} → {new_speaker_key})", category="realtime_editor")
                        else:
                            log_message("ATTENTION", f"Aucune modification détectée dans la ligne source", category="realtime_editor")
                    else:
                        log_message("ATTENTION", f"Ligne source hors limites: {source_line}", category="realtime_editor")
                else:
                    log_message("ATTENTION", f"Fichier source introuvable: {source_file_path}", category="realtime_editor")
            except Exception as e:
                log_message("ERREUR", f"Erreur modification fichier source: {e}", category="realtime_editor")
        
        # Créer une clé unique pour cette modification
        key = f"{dialogue_info.get('tl_file', '')}|{dialogue_info.get('tl_line', 0)}"
        
        # Vérifier si une modification existe déjà
        if hasattr(biz, 'pending_modifications') and key in biz.pending_modifications:
            mod_entry = biz.pending_modifications[key]
            mod_data = mod_entry.get('modification_data', {})
        else:
            mod_data = {'type': 'simple', 'content': ''}
        
        # Ajouter la modification de la lettre du locuteur dans les métadonnées
        mod_data['speaker_modification'] = {
            'original_speaker_key': original_speaker_key,
            'modified_speaker_key': new_speaker_key,
            'source_file': source_file,
            'source_line': source_line
        }
        
        # Sauvegarder dans pending_modifications
        if not hasattr(biz, 'pending_modifications'):
            biz.pending_modifications = {}
        
        biz.pending_modifications[key] = {
            'dialogue_info': dialogue_info,
            'modification_data': mod_data,
            'timestamp': time.time()
        }
        
        # Sauvegarder dans le fichier JSON si disponible
        if hasattr(biz, 'pending_modifications_file') and biz.pending_modifications_file:
            try:
                import json
                with open(biz.pending_modifications_file, 'w', encoding='utf-8') as f:
                    json.dump(biz.pending_modifications, f, indent=2, ensure_ascii=False, default=str)
            except Exception as e:
                log_message("ATTENTION", f"Erreur sauvegarde JSON modification locuteur: {e}", category="realtime_editor")
        
        # Mettre à jour le dialogue_info pour refléter la modification
        dialogue_info['modified_speaker_key'] = new_speaker_key
        dialogue_info['speaker_key'] = new_speaker_key  # Mettre à jour aussi la clé originale
        
        # Mettre à jour les deux combobox (VO et VF) pour synchronisation
        characters_list = _get_characters_list_for_combobox(main_interface)
        new_display_name = "Narrateur (aucun locuteur)"
        
        if new_speaker_key:
            # Trouver le nom d'affichage complet depuis la liste
            for item in characters_list:
                if item.startswith(f"{new_speaker_key} ") or item == f"{new_speaker_key.upper()}":
                    new_display_name = item
                    break
            else:
                # Si pas trouvé, créer un nom d'affichage simple
                new_display_name = _get_character_display_name(new_speaker_key, main_interface)
        
        if hasattr(main_interface, 'vo_speaker_combo_var'):
            main_interface.vo_speaker_combo_var.set(new_display_name)
        if hasattr(main_interface, 'vf_speaker_combo_var'):
            main_interface.vf_speaker_combo_var.set(new_display_name)
        
        display_name = _get_character_display_name(new_speaker_key, main_interface) if new_speaker_key else "Narrateur"
        main_interface._update_status(f"Locuteur modifié: {display_name}")
        log_message("INFO", f"Modification locuteur sauvegardée: {original_speaker_key} → {new_speaker_key}", category="realtime_editor")
        
    except Exception as e:
        log_message("ERREUR", f"Erreur sauvegarde modification locuteur: {e}", category="realtime_editor")
        main_interface._update_status("Erreur lors de la sauvegarde du locuteur")

def _save_current_modification_if_changed(main_interface):
    """Sauvegarde la modification actuelle en attente si elle a changé."""
    try:
        if not hasattr(main_interface, 'current_dialogue_info') or not main_interface.current_dialogue_info: return
        
        biz = main_interface._get_realtime_editor_business()
        
        # ✅ NOUVEAU : Gérer les menus de choix
        if main_interface.current_dialogue_info.get('is_menu', False):
            if not hasattr(main_interface, 'menu_vf_widgets'):
                return
            
            for i, vf_widget in enumerate(main_interface.menu_vf_widgets):
                if not (vf_widget and vf_widget.winfo_exists()):
                    continue
                
                try:
                    current_text = vf_widget.get('1.0', tk.END).strip()
                    choice_info = vf_widget.choice_info
                    original_text = choice_info.get('translated_text', '').strip()
                    
                    # Vérifier si le texte a changé
                    if current_text != original_text:
                        # Chaque choix a son propre tl_file et tl_line
                        single_choice_info = {
                            'tl_file': choice_info.get('tl_file'),
                            'tl_line': choice_info.get('tl_line'),
                            'original_text': choice_info.get('original_text'),
                            'displayed_text': original_text,
                            'is_menu': False  # Pour la sauvegarde, traiter comme dialogue simple
                        }
                        
                        mod_data = {
                            'type': 'menu_choice',
                            'content': current_text,
                            'original_structure': {
                                'was_split': False,
                                'original_text': original_text
                            }
                        }
                        
                        biz.add_pending_modification(single_choice_info, mod_data)
                        
                except Exception as e:
                    log_message("ERREUR", f"Erreur sauvegarde choix {i+1} en attente: {e}", category="realtime_editor")
            
            # Mettre à jour le statut avec le nombre de modifications en attente
            update_status_with_pending_count(main_interface)
            return
        
        if main_interface.current_multiple_group:
            vf_dialogues = main_interface.current_multiple_group.get('vf_dialogues', [])
            for i, widget in enumerate(main_interface.multiple_vf_widgets):
                if not (widget and widget.winfo_exists() and i < len(vf_dialogues)): continue
                current_text, original_info = widget.get('1.0', tk.END).strip(), vf_dialogues[i]
                if current_text != original_info.get('dialogue_text', '').strip():
                    single_dialogue_info = {**main_interface.current_multiple_group, **original_info, 'tl_line': original_info['line_index'] + 1}
                    mod_data = {'type': 'multiple_dialogue', 'content': current_text, 'original_structure': {'was_split': False, 'original_text': original_info.get('dialogue_text', '')}}
                    biz.add_pending_modification(single_dialogue_info, mod_data)
            # Mettre à jour le statut avec le nombre de modifications en attente
            update_status_with_pending_count(main_interface)
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
            # Mettre à jour le statut avec le nombre de modifications en attente
            update_status_with_pending_count(main_interface)
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
                    # ✅ CORRECTION : Mettre à jour le compteur après la récupération
                    update_status_with_pending_count(main_interface)
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
                    type_name = {'simple': 'simple', 'split': 'division', 'speaker_dialogue': 'locuteur+dialogue', 'merge': 'fusion', 'menu_choice': 'choix', 'multiple_dialogue': 'multiple'}.get(mod_type, mod_type)
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
            
            # Mettre à jour le statut avec le nombre de modifications en attente
            update_status_with_pending_count(main_interface)
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
        
        # Réinitialiser complètement la combobox
        lang_combo['values'] = []  # Vider d'abord
        main_interface.realtime_language_var.set('')  # Réinitialiser la variable
        lang_combo['values'] = languages  # Puis remplir avec les nouvelles valeurs
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
    Ouvre Google Translate avec le texte fourni (avec encodage correct des balises Ren'Py).
    Cible la langue de l'interface temps réel si disponible.
    """
    try:
        import webbrowser, urllib.parse
        
        # Nettoyer le texte
        clean_text = (text or "").strip()
        if not clean_text:
            main_interface._show_notification("Aucun texte à traduire", "warning")
            return False
        
        # Langue cible d'après ton sélecteur d'onglet (fallback 'fr')
        tl = 'fr'
        try:
            tl = (main_interface.realtime_language_var.get() or 'fr').lower()
        except Exception:
            pass

        # Limiter la longueur pour éviter les URLs trop longues
        max_length = 400
        if len(clean_text) > max_length:
            clean_text = clean_text[:max_length] + "..."
            main_interface._show_notification(f"Texte tronqué à {max_length} caractères", "info")

        # Encoder TOUS les caractères spéciaux (y compris {, }, [, ], \, etc.)
        # urllib.parse.quote avec safe='' encode TOUT sauf les caractères alphanumériques
        encoded_text = urllib.parse.quote(clean_text, safe='')

        url = "https://translate.google.com/?sl=auto&tl={}&text={}&op=translate".format(
            urllib.parse.quote(tl, safe=''), encoded_text
        )
        webbrowser.open(url)
        main_interface._update_status("Google Translate ouvert")
        return True
    except Exception as e:
        log_message("ATTENTION", f"Impossible d'ouvrir Google Translate: {e}", category="realtime_editor")
        return False

def _fill_translation_area(main_interface, translation_text, context=""):
    """
    Remplit automatiquement la zone de traduction avec le texte traduit
    """
    import tkinter as tk  # ✅ CORRECTION : Import au début de la fonction
    try:
        # ✅ AMÉLIORATION : Chercher toutes les zones de traduction possibles
        vf_widgets = []
        
        # Zones VF de l'éditeur temps réel (noms corrects)
        if hasattr(main_interface, 'vf_text_widget') and main_interface.vf_text_widget:
            vf_widgets.append(('vf_text_widget', main_interface.vf_text_widget))
        
        # Zone VF split (deuxième widget)
        if hasattr(main_interface, 'vf_text_widget_2') and main_interface.vf_text_widget_2:
            vf_widgets.append(('vf_text_widget_2', main_interface.vf_text_widget_2))
        
        # Zones VF avec noms alternatifs (pour compatibilité)
        if hasattr(main_interface, 'vf_text') and main_interface.vf_text:
            vf_widgets.append(('vf_text', main_interface.vf_text))
        
        if hasattr(main_interface, 'txt2') and main_interface.txt2:
            vf_widgets.append(('txt2', main_interface.txt2))
        
        if hasattr(main_interface, 'vf_dialogue_widget') and main_interface.vf_dialogue_widget:
            vf_widgets.append(('vf_dialogue_widget', main_interface.vf_dialogue_widget))
        
        if hasattr(main_interface, 'vf_multiple_widget') and main_interface.vf_multiple_widget:
            vf_widgets.append(('vf_multiple_widget', main_interface.vf_multiple_widget))
        
        if hasattr(main_interface, 'vf_choice_widget') and main_interface.vf_choice_widget:
            vf_widgets.append(('vf_choice_widget', main_interface.vf_choice_widget))
        
        # ✅ AJOUT : Recherche dynamique dans tous les widgets Text de l'interface
        if not vf_widgets:
            log_message("DEBUG", "Recherche dynamique des zones VF...", category="realtime_editor")
            
            # Essayer d'abord avec main_interface
            vf_widgets = _find_vf_widgets_recursively(main_interface)
            
            # Si pas de widgets trouvés et main_interface a une fenêtre, chercher dans la fenêtre
            if not vf_widgets and hasattr(main_interface, 'window') and main_interface.window:
                log_message("DEBUG", "Recherche dans la fenêtre principale...", category="realtime_editor")
                vf_widgets = _find_vf_widgets_recursively(main_interface.window)
            
            # Si toujours pas de widgets trouvés, chercher dans toutes les fenêtres Tkinter
            if not vf_widgets:
                log_message("DEBUG", "Recherche dans toutes les fenêtres Tkinter...", category="realtime_editor")
                for window in tk._default_root.winfo_children() if tk._default_root else []:
                    window_widgets = _find_vf_widgets_recursively(window)
                    vf_widgets.extend(window_widgets)
                    if vf_widgets:  # Arrêter dès qu'on trouve des widgets
                        break
        
        # Remplir la première zone VF trouvée
        for widget_name, widget in vf_widgets:
            try:
                widget.delete('1.0', tk.END)
                widget.insert('1.0', translation_text)
                log_message("INFO", f"Zone de traduction remplie ({widget_name}){' (' + context + ')' if context else ''}", category="realtime_editor")
                return True
            except Exception as e:
                log_message("ATTENTION", f"Erreur remplissage {widget_name}: {e}", category="realtime_editor")
                continue
        
        # Aucune zone trouvée
        log_message("ATTENTION", f"Aucune zone de traduction trouvée. Zones disponibles: {[name for name, _ in vf_widgets]}", category="realtime_editor")
        return False
        
    except Exception as e:
        log_message("ERREUR", f"Erreur remplissage zone traduction: {e}", category="realtime_editor")
        return False


def _find_vf_widgets_recursively(parent_widget, depth=0):
    """
    Recherche récursive de tous les widgets Text qui pourraient être des zones VF
    """
    vf_widgets = []
    
    if depth > 10:  # Limiter la profondeur pour éviter les boucles infinies
        return vf_widgets
    
    try:
        # ✅ CORRECTION : Vérifier que l'objet parent est un widget Tkinter
        if not hasattr(parent_widget, 'winfo_children'):
            log_message("DEBUG", f"Objet parent n'est pas un widget Tkinter: {type(parent_widget)}", category="realtime_editor")
            return vf_widgets
        
        # Parcourir tous les enfants du widget
        for child in parent_widget.winfo_children():
            try:
                # Vérifier si c'est un widget Text
                if isinstance(child, tk.Text):
                    # Vérifier si le widget semble être une zone VF
                    widget_info = child.winfo_class()
                    widget_name = getattr(child, '_name', f"Text_{id(child)}")
                    
                    # Critères pour identifier une zone VF :
                    # - Widget Text existant
                    # - Pas de contenu ou contenu court (zone de traduction vide)
                    current_content = child.get('1.0', tk.END).strip()
                    
                    if len(current_content) < 100:  # Zone probablement vide ou avec peu de contenu
                        vf_widgets.append((f"dynamic_{widget_name}", child))
                        log_message("DEBUG", f"Zone VF potentielle trouvée: {widget_name} (contenu: {len(current_content)} chars)", category="realtime_editor")
                
                # Rechercher récursivement dans les enfants
                child_vf_widgets = _find_vf_widgets_recursively(child, depth + 1)
                vf_widgets.extend(child_vf_widgets)
                
            except Exception as e:
                # Ignorer les erreurs sur les widgets spécifiques
                continue
                
    except Exception as e:
        log_message("DEBUG", f"Erreur recherche récursive: {e}", category="realtime_editor")
    
    return vf_widgets

# Exporter la fonction pour qu'elle soit accessible depuis translator_utils
def fill_translation_area(main_interface, translation_text, context=""):
    return _fill_translation_area(main_interface, translation_text, context)

def copy_and_open_translator(main_interface, text, context=""):
    """
    Ouvre le traducteur sélectionné avec le texte pré-rempli.
    
    Args:
        main_interface: Interface principale pour accéder au clipboard et aux notifications
        text: Texte à copier (avec balises Ren'Py préservées)
        context: Contexte pour les logs (optionnel)
    """
    try:
        from ui.shared.translator_utils import open_translator, get_default_translator
        
        # Utiliser le traducteur sélectionné ou le défaut
        translator = getattr(main_interface, 'current_translator', get_default_translator())
        
        # Nettoyer le texte
        clean_text = (text or "").strip()
        if not clean_text:
            main_interface._show_notification("Aucun texte à traduire", "warning")
            return
        
        # Récupérer la langue cible depuis l'interface
        target_lang = "fr"  # Par défaut français
        if hasattr(main_interface, 'realtime_language_var'):
            language_var = main_interface.realtime_language_var.get()
            # Convertir "french" -> "fr", "english" -> "en", etc.
            lang_map = {
                "french": "fr",
                "english": "en", 
                "spanish": "es",
                "german": "de",
                "italian": "it",
                "portuguese": "pt",
                "russian": "ru",
                "japanese": "ja",
                "chinese": "zh"
            }
            target_lang = lang_map.get(language_var, "fr")
        
        # Récupérer le ton de traduction
        tone = getattr(main_interface, 'translation_tone', 'informel')
        
        # ✅ NOUVEAU : Récupérer le contexte enrichi pour Groq AI
        speaker = None
        previous_dialogue = None
        characters_def = None
        
        # Uniquement pour Groq AI
        if translator == "Groq AI":
            # Extraire le locuteur du dialogue actuel
            if hasattr(main_interface, 'current_dialogue_info') and main_interface.current_dialogue_info:
                dialogue_info = main_interface.current_dialogue_info
                
                # Récupérer le business pour extraire le locuteur
                try:
                    biz = main_interface._get_realtime_editor_business()
                    
                    # Essayer d'extraire le locuteur depuis le fichier de traduction
                    tl_file = dialogue_info.get('tl_file')
                    tl_line = dialogue_info.get('tl_line', 0)
                    
                    if tl_file and tl_line > 0:
                        import os
                        tl_file_path = os.path.join(main_interface.current_project_path, tl_file)
                        if not os.path.exists(tl_file_path):
                            tl_file_path = os.path.join(main_interface.current_project_path, "game", tl_file)
                        
                        if os.path.exists(tl_file_path):
                            with open(tl_file_path, 'r', encoding='utf-8') as f:
                                lines = f.readlines()
                            
                            target_index = tl_line - 1
                            if 0 <= target_index < len(lines):
                                current_line = lines[target_index].strip()
                                speaker = biz._extract_speaker_from_line(current_line)
                    
                    # Récupérer le dialogue précédent
                    previous_dialogue = biz.get_previous_dialogue(dialogue_info)
                    
                except Exception as e:
                    log_message("ATTENTION", f"Erreur extraction contexte: {e}", category="realtime_editor")
            
            # Récupérer les définitions de personnages
            from infrastructure.config.config import config_manager
            characters_def = config_manager.get('groq_characters_definitions', {})
        
        # Ouvrir le traducteur sélectionné avec contexte enrichi
        success = open_translator(
            translator, clean_text, context, main_interface, 
            target_lang=target_lang, tone=tone,
            speaker=speaker, previous_dialogue=previous_dialogue, characters_def=characters_def
        )
        
        if success:
            # Message de statut
            status_msg = f"{translator} ouvert{' avec ' + context if context else ''}"
            main_interface._update_status(status_msg)
            
            log_message("INFO", f"Texte envoyé à {translator}{' (' + context + ')' if context else ''}: {len(clean_text)} caractères", category="realtime_editor")
        
    except Exception as e:
        error_msg = f"Erreur ouverture traducteur: {e}"
        main_interface._show_notification(error_msg, "error")
        log_message("ERREUR", f"Erreur traducteur{' (' + context + ')' if context else ''}: {e}", category="realtime_editor")

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


def _show_groq_prompt_customizer(main_interface):
    """Affiche la fenêtre de personnalisation complète du prompt Groq AI"""
    from ui.window_manager import window_manager
    
    # Vérifier si la fenêtre est déjà ouverte
    window_id = "groq_prompt_customizer"
    if window_manager.is_window_open(window_id):
        window_manager.bring_to_front(window_id)
        return
    
    theme = theme_manager.get_theme()
    
    # Déterminer la fenêtre parente (détachée si elle existe, sinon principale)
    parent_window = main_interface.window  # Par défaut, fenêtre principale
    if hasattr(main_interface, 'detached_editor_window') and main_interface.detached_editor_window and main_interface.detached_editor_window.winfo_exists():
        parent_window = main_interface.detached_editor_window
    
    # Créer la fenêtre (agrandie pour inclure personnages et profils)
    dialog = tk.Toplevel(parent_window)
    dialog.title("⚙️ Personnalisation Groq AI")
    dialog.geometry("950x750")
    dialog.configure(bg=theme["bg"])
    dialog.transient(parent_window)
    # Ne PAS utiliser grab_set() pour ne pas bloquer toute l'application
    
    # Enregistrer la fenêtre dans le gestionnaire
    window_manager.register_window(window_id, dialog)
    
    # Centrer la fenêtre
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (950 // 2)
    y = (dialog.winfo_screenheight() // 2) - (750 // 2)
    dialog.geometry(f"950x750+{x}+{y}")
    
    # Frame principal avec scrollbar
    main_frame = tk.Frame(dialog, bg=theme["bg"])
    main_frame.pack(fill="both", expand=True, padx=15, pady=15)
    
    # Titre centré
    title_frame = tk.Frame(main_frame, bg=theme["bg"])
    title_frame.pack(fill='x', pady=(0, 20))
    
    tk.Label(title_frame, text="🤖 Personnalisation Complète de Groq AI", 
             font=('Segoe UI', 14, 'bold'), bg=theme["bg"], fg=theme["accent"]).pack()
    
    tk.Label(title_frame, text="Configurez le comportement de la traduction IA selon vos besoins", 
             font=('Segoe UI', 9, 'italic'), bg=theme["bg"], fg=theme["fg"]).pack(pady=(5, 0))
    
    # ===== NOUVEAU : SYSTÈME DE PROFILS =====
    profiles_frame = tk.Frame(main_frame, bg=theme["bg"], relief='solid', borderwidth=1)
    profiles_frame.pack(fill='x', pady=(0, 15))
    
    # Header profils
    profiles_header = tk.Frame(profiles_frame, bg=theme["accent"])
    profiles_header.pack(fill='x')
    tk.Label(profiles_header, text="📁 Profils de prompts", font=('Segoe UI', 10, 'bold'), 
             bg=theme["accent"], fg="#FFFFFF", padx=10, pady=5).pack(side='left')
    
    # Contenu profils
    profiles_content = tk.Frame(profiles_frame, bg=theme["bg"])
    profiles_content.pack(fill='x', padx=10, pady=10)
    
    # Charger les profils existants
    saved_profiles = config_manager.get('groq_prompt_profiles', {})
    profile_names = list(saved_profiles.keys()) if saved_profiles else []
    
    tk.Label(profiles_content, text="Profil actif :", font=('Segoe UI', 9, 'bold'),
             bg=theme["bg"], fg=theme["fg"]).pack(side='left', padx=(0, 5))
    
    current_profile_var = tk.StringVar(value=config_manager.get('groq_current_profile', 'Par défaut'))
    profile_combo = ttk.Combobox(profiles_content, textvariable=current_profile_var,
                                values=['Par défaut'] + profile_names, state="readonly", width=25,
                                font=('Segoe UI', 9))
    profile_combo.pack(side='left', padx=(0, 10))
    
    # Charger automatiquement quand on sélectionne un profil
    profile_combo.bind('<<ComboboxSelected>>', lambda e: load_profile())
    
    def load_profile():
        """Charge un profil sauvegardé"""
        profile_name = current_profile_var.get()
        
        if profile_name == 'Par défaut':
            # Réinitialiser aux valeurs par défaut
            instructions_text.delete('1.0', 'end')
            tone_var.set('Informel')
            style_var.set('Naturel')
            context_var.set('Général')
            creativity_var.set(0.3)
            
            # Vider la liste des personnages
            if hasattr(dialog, 'character_frames'):
                for frame in dialog.character_frames:
                    frame.destroy()
                dialog.character_frames = []
                dialog.characters_list_data = {}
            
            config_manager.set('groq_current_profile', 'Par défaut')
            log_message("INFO", "Profil réinitialisé aux valeurs par défaut", category="realtime_editor")
            
            # Mettre à jour l'aperçu
            if hasattr(dialog, 'update_prompt_preview_func'):
                dialog.update_prompt_preview_func()
            return
        
        if profile_name in saved_profiles:
            profile_data = saved_profiles[profile_name]
            
            # Charger les données dans l'interface
            instructions_text.delete('1.0', 'end')
            instructions_text.insert('1.0', profile_data.get('custom_instructions', ''))
            
            tone_var.set(profile_data.get('tone', 'Informel'))
            style_var.set(profile_data.get('style', 'Naturel'))
            context_var.set(profile_data.get('game_context', 'Général'))
            creativity_var.set(profile_data.get('temperature', 0.3))
            
            # Charger les personnages (fonction sera créée plus tard dans le code)
            characters_data = profile_data.get('characters', {})
            # Stocker temporairement pour charger après création de l'interface personnages
            if hasattr(dialog, 'load_characters_func'):
                dialog.load_characters_func(characters_data)
            else:
                # Pas encore créé, on stocke pour plus tard
                dialog.characters_to_load = characters_data
            
            config_manager.set('groq_current_profile', profile_name)
            log_message("INFO", f"Profil '{profile_name}' chargé", category="realtime_editor")
            
            # Mettre à jour l'aperçu
            if hasattr(dialog, 'update_prompt_preview_func'):
                dialog.update_prompt_preview_func()
            else:
                # Fonction pas encore créée, on l'appellera plus tard
                pass
    
    def save_profile():
        """Sauvegarde le profil actuel"""
        # Toujours demander le nom (permet de créer des variantes)
        from infrastructure.helpers.unified_functions import show_custom_input_dialog
        from ui.themes import theme_manager
        
        current_name = current_profile_var.get()
        initial_value = current_name if current_name != 'Par défaut' else ""
        
        profile_name = show_custom_input_dialog(
            "💾 Sauvegarder le profil",
            "Nom du profil à sauvegarder :",
            theme_manager.get_theme(),
            parent=dialog,
            initial_value=initial_value
        )
        if not profile_name:
            return
        
        # Collecter toutes les données actuelles
        profile_data = {
            'custom_instructions': instructions_text.get('1.0', 'end-1c').strip(),
            'tone': tone_var.get(),
            'style': style_var.get(),
            'game_context': context_var.get(),
            'temperature': creativity_var.get(),
            'characters': dialog.characters_list_data  # Les données des personnages
        }
        
        saved_profiles[profile_name] = profile_data
        config_manager.set('groq_prompt_profiles', saved_profiles)
        config_manager.set('groq_current_profile', profile_name)
        config_manager.save_config()
        
        # Mettre à jour la combo
        profile_combo['values'] = ['Par défaut'] + list(saved_profiles.keys())
        current_profile_var.set(profile_name)
        
        log_message("INFO", f"Profil '{profile_name}' sauvegardé", category="realtime_editor")
    
    def delete_profile():
        """Supprime le profil actuel"""
        profile_name = current_profile_var.get()
        if profile_name == 'Par défaut':
            return
        
        if profile_name in saved_profiles:
            from infrastructure.helpers.unified_functions import show_custom_askyesno
            confirm = show_custom_askyesno(
                "Supprimer le profil",
                f"Êtes-vous sûr de vouloir supprimer le profil '{profile_name}' ?",
                theme_manager.get_theme(),
                parent=dialog
            )
            
            if confirm:
                del saved_profiles[profile_name]
                config_manager.set('groq_prompt_profiles', saved_profiles)
                config_manager.set('groq_current_profile', 'Par défaut')
                config_manager.save_config()
                
                profile_combo['values'] = ['Par défaut'] + list(saved_profiles.keys())
                current_profile_var.set('Par défaut')
                
                log_message("INFO", f"Profil '{profile_name}' supprimé", category="realtime_editor")
    
    tk.Button(profiles_content, text="💾 Sauvegarder", command=save_profile,
             bg=theme["button_primary_bg"], fg="#000000", font=('Segoe UI', 8, 'bold'),
             pady=2, padx=8, relief='flat', cursor='hand2').pack(side='left', padx=(0, 5))
    
    tk.Button(profiles_content, text="🗑️ Supprimer", command=delete_profile,
             bg=theme["button_danger_bg"], fg="#000000", font=('Segoe UI', 8, 'bold'),
             pady=2, padx=8, relief='flat', cursor='hand2').pack(side='left')
    
    # ===== SECTION 1: INSTRUCTIONS PERSONNALISÉES =====
    instructions_section = tk.Frame(main_frame, bg=theme["bg"])
    instructions_section.pack(fill='x', pady=(0, 15))
    
    # Header avec titre et bouton d'aide
    instructions_header = tk.Frame(instructions_section, bg=theme["bg"])
    instructions_header.pack(fill='x', pady=(0, 5))
    
    tk.Label(instructions_header, text="📝 Instructions personnalisées", 
             font=('Segoe UI', 11, 'bold'), bg=theme["bg"], fg=theme["fg"]).pack(side='left')
    
    # Bouton d'aide
    def show_groq_help():
        """Affiche l'aide complète pour la personnalisation Groq AI"""
        help_title = "🤖 Aide - Personnalisation Groq AI"
        help_message = [
            ("Guide Complet de Personnalisation Groq AI\n\n", "bold"),
            ("📁 PROFILS DE PROMPTS\n\n", "bold_green"),
            ("Les profils permettent de sauvegarder et recharger des configurations complètes pour différents jeux.\n\n", "normal"),
            ("• 📂 Charger : Recharge un profil sauvegardé (instructions, style, personnages, etc.)\n", "normal"),
            ("• 💾 Sauvegarder : Crée un nouveau profil ou met à jour l'existant\n", "normal"),
            ("• 🗑️ Supprimer : Supprime le profil actuel (sauf 'Par défaut')\n\n", "normal"),
            ("📝 INSTRUCTIONS PERSONNALISÉES\n\n", "bold_green"),
            ("Ajoutez vos propres consignes pour guider la traduction. Exemples :\n\n", "normal"),
            ("• Expressions idiomatiques : Adapte les expressions au contexte francophone\n", "normal"),
            ("• Style humoristique : Conserve le style humoristique et les jeux de mots\n", "normal"),
            ("• Registre soutenu : Utilise un vocabulaire soutenu adapté au contexte médiéval\n", "normal"),
            ("• Traduction littérale : Traduit de manière très littérale pour garder la précision\n\n", "normal"),
            ("🎨 STYLE DE TRADUCTION\n\n", "bold_green"),
            ("• Ton : Informel (tutoiement), Formel (vouvoiement), ou Neutre\n", "normal"),
            ("• Style : Littéral (structure originale), Naturel (équilibre), ou Créatif (adaptation culturelle)\n", "normal"),
            ("• Contexte : Général, Romance, Aventure, Horreur, Comédie, Fantaisie, Science-Fiction\n", "normal"),
            ("• Créativité : 0.0 = Précis (fidèle), 1.0 = Créatif (adaptatif)\n\n", "normal"),
            ("👥 DÉFINITION DES PERSONNAGES\n\n", "bold_green"),
            ("Cette fonctionnalité enrichit automatiquement le prompt avec le contexte des personnages :\n\n", "normal"),
            ("• Locuteur : 1-3 caractères (ex: p, a, n, mc, al)\n", "normal"),
            ("• Genre : Fille, Garçon, Adolescent, Adolescente, Homme, Femme\n", "normal"),
            ("• Prénom : Nom du personnage pour un contexte plus précis\n\n", "normal"),
            ("💡 EXEMPLE D'UTILISATION\n\n", "bold_green"),
            ("Si vous définissez :\n", "normal"),
            ("• [p] = Homme, Alex\n", "blue"),
            ("• [a] = Fille, Andrea\n\n", "blue"),
            ("Et que le dialogue actuel est :\n", "normal"),
            ("p \"Noch viel trauriger.\"\n\n", "blue"),
            ("Le prompt sera enrichi automatiquement avec :\n", "normal"),
            ("CONTEXTE DES PERSONNAGES :\n", "bold"),
            ("[p] est un Homme du nom de Alex\n", "blue"),
            ("[a] est une Fille du nom de Andrea\n\n", "blue"),
            ("CONTEXTE DE CONVERSATION (dialogue précédent) :\n", "bold"),
            ("a \"Warst du wirklich so traurig, wie du ausgesehen hast?\"\n\n", "blue"),
            ("Cela permet à Groq AI de :\n", "normal"),
            ("• Faire les bons accords grammaticaux (il/elle)\n", "normal"),
            ("• Adapter le ton selon la relation entre personnages\n", "normal"),
            ("• Comprendre le contexte émotionnel de la conversation\n", "normal"),
            ("• Traduire de manière plus cohérente et naturelle\n\n", "normal"),
            ("👀 APERÇU DU PROMPT\n\n", "bold_green"),
            ("L'aperçu se met à jour automatiquement et montre le prompt complet qui sera envoyé à Groq AI.\n", "normal"),
            ("C'est un excellent moyen de vérifier que votre configuration est correcte avant de traduire.\n\n", "normal"),
            ("🚀 UTILISATION PRATIQUE\n\n", "bold_green"),
            ("1. Configurez vos personnages une fois par jeu\n", "normal"),
            ("2. Ajustez le style selon vos préférences\n", "normal"),
            ("3. Sauvegardez votre profil (ex: 'DasTrio v0.01a')\n", "normal"),
            ("4. Utilisez Groq AI dans l'éditeur temps réel\n", "normal"),
            ("5. Le système enrichit automatiquement chaque traduction !\n\n", "normal"),
            ("Les sections Style et Personnages sont collapsibles (▶/▼) pour une interface plus épurée.", "italic")
        ]
        
        from infrastructure.helpers.unified_functions import show_custom_messagebox
        from ui.themes import theme_manager
        show_custom_messagebox(
            'info',
            help_title,
            help_message,
            theme_manager.get_theme(),
            parent=dialog
        )
    
    help_btn = tk.Button(instructions_header, text="❓ Aide", 
                        command=show_groq_help,
                        bg=theme["button_help_bg"], fg="#000000",
                        font=('Segoe UI', 9, 'bold'), pady=2, padx=8,
                        relief='flat', cursor='hand2')
    help_btn.pack(side='right')
    
    tk.Label(instructions_section, text="Ajoutez vos propres consignes pour guider la traduction :", 
             font=('Segoe UI', 9), bg=theme["bg"], fg=theme["fg"]).pack(anchor='w', pady=(0, 5))
    
    # Container pour le texte et sa scrollbar
    instructions_text_container = tk.Frame(instructions_section, bg=theme["bg"])
    instructions_text_container.pack(fill='x', pady=(0, 5))
    
    instructions_text = tk.Text(
        instructions_text_container,
        height=4,
        font=('Segoe UI', 9),
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        insertbackground=theme["entry_fg"],
        wrap='word',
        relief='solid',
        borderwidth=1
    )
    instructions_text.pack(side='left', fill='both', expand=True)
    
    # Ajouter scrollbar pour instructions
    instructions_scrollbar = tk.Scrollbar(instructions_text_container, orient="vertical", command=instructions_text.yview)
    instructions_text.configure(yscrollcommand=instructions_scrollbar.set)
    instructions_scrollbar.pack(side='right', fill='y')
    
    # Charger les instructions sauvegardées
    current_instructions = config_manager.get('groq_custom_instructions', '')
    if current_instructions:
        instructions_text.insert('1.0', current_instructions)
    
    # Exemples cliquables
    examples_frame = tk.Frame(instructions_section, bg=theme["bg"])
    examples_frame.pack(fill='x', pady=(5, 0))
    
    tk.Label(examples_frame, text="💡 Exemples :", 
             font=('Segoe UI', 8, 'bold'), bg=theme["bg"], fg=theme["fg"]).pack(side='left', padx=(0, 5))
    
    def insert_example(text):
        current = instructions_text.get('1.0', 'end-1c').strip()
        if current:
            instructions_text.insert('end', f'\n{text}')
        else:
            instructions_text.insert('1.0', text)
    
    examples = [
        ("Expressions idiomatiques", "Adapte les expressions idiomatiques au contexte francophone"),
        ("Style humoristique", "Conserve le style humoristique et les jeux de mots"),
        ("Registre soutenu", "Utilise un vocabulaire soutenu adapté à un contexte médiéval"),
        ("Traduction littérale", "Traduis de manière très littérale pour garder la précision"),
    ]
    
    for label, text in examples:
        btn = tk.Button(
            examples_frame,
            text=label,
            command=lambda t=text: insert_example(t),
            bg=theme["button_utility_bg"],
            fg="#000000",
            font=('Segoe UI', 7),
            pady=2,
            padx=4,
            relief='flat',
            cursor='hand2'
        )
        btn.pack(side='left', padx=2)
    
    # ===== SECTION 2: OPTIONS DE STYLE (COLLAPSIBLE) =====
    style_section = tk.Frame(main_frame, bg=theme["bg"])
    style_section.pack(fill='x', pady=(0, 15))
    
    # Variable pour tracker l'état (ouvert/fermé) - FERMÉ par défaut
    style_collapsed = tk.BooleanVar(value=True)
    
    # Header cliquable
    style_header = tk.Frame(style_section, bg=theme["bg"], cursor='hand2')
    style_header.pack(fill='x')
    
    style_collapse_icon = tk.Label(style_header, text="▶", font=('Segoe UI', 10, 'bold'),
                                  bg=theme["bg"], fg=theme["fg"], cursor='hand2')
    style_collapse_icon.pack(side='left', padx=(0, 5))
    
    style_label = tk.Label(style_header, text="🎨 Style de traduction", 
                          font=('Segoe UI', 11, 'bold'), bg=theme["bg"], fg=theme["fg"],
                          cursor='hand2')
    style_label.pack(side='left')
    
    # Container pour le contenu des options de style (FERMÉ par défaut)
    style_content = tk.Frame(style_section, bg=theme["bg"])
    # style_content.pack(fill='x', pady=(10, 0))  # Pas d'affichage initial
    
    # Une seule ligne pour les 4 contrôles
    options_row = tk.Frame(style_content, bg=theme["bg"])
    options_row.pack(fill='x', pady=(0, 10))
    
    # Ton
    tone_frame = tk.Frame(options_row, bg=theme["bg"])
    tone_frame.pack(side='left', fill='x', expand=True, padx=(0, 15))
    tk.Label(tone_frame, text="Ton :", font=('Segoe UI', 9, 'bold'), 
             bg=theme["bg"], fg=theme["fg"]).pack(anchor='w')
    tone_var = tk.StringVar(value=getattr(main_interface, 'translation_tone', 'informel').capitalize())
    tone_combo_dialog = ttk.Combobox(tone_frame, textvariable=tone_var,
                                    values=["Informel", "Formel", "Neutre"], state="readonly", width=15)
    tone_combo_dialog.pack(anchor='w', pady=(2, 0))
    
    # Style
    style_frame = tk.Frame(options_row, bg=theme["bg"])
    style_frame.pack(side='left', fill='x', expand=True, padx=(0, 15))
    tk.Label(style_frame, text="Style :", font=('Segoe UI', 9, 'bold'), 
             bg=theme["bg"], fg=theme["fg"]).pack(anchor='w')
    style_var = tk.StringVar(value=config_manager.get('groq_translation_style', 'Naturel'))
    style_combo = ttk.Combobox(style_frame, textvariable=style_var,
                              values=["Littéral", "Naturel", "Créatif"], state="readonly", width=15)
    style_combo.pack(anchor='w', pady=(2, 0))
    
    # Contexte du jeu
    context_frame = tk.Frame(options_row, bg=theme["bg"])
    context_frame.pack(side='left', fill='x', expand=True, padx=(0, 15))
    tk.Label(context_frame, text="Contexte :", font=('Segoe UI', 9, 'bold'), 
             bg=theme["bg"], fg=theme["fg"]).pack(anchor='w')
    context_var = tk.StringVar(value=config_manager.get('groq_game_context', 'Général'))
    context_combo = ttk.Combobox(context_frame, textvariable=context_var,
                                values=["Général", "Romance", "Aventure", "Horreur", "Comédie", "Fantaisie", "Science-Fiction"], 
                                state="readonly", width=15)
    context_combo.pack(anchor='w', pady=(2, 0))
    
    # Créativité (température)
    creativity_frame = tk.Frame(style_content, bg=theme["bg"])
    creativity_frame.pack(fill='x', pady=(0, 10))
    tk.Label(creativity_frame, text="Créativité :", font=('Segoe UI', 9, 'bold'), 
             bg=theme["bg"], fg=theme["fg"]).pack(anchor='w')
    
    creativity_var = tk.DoubleVar(value=float(config_manager.get('groq_temperature', 0.3)))
    creativity_scale = tk.Scale(
        creativity_frame,
        from_=0.0,
        to=1.0,
        resolution=0.1,
        orient='horizontal',
        variable=creativity_var,
        bg=theme["bg"],
        fg=theme["fg"],
        highlightbackground=theme["bg"],
        troughcolor=theme["entry_bg"],
        length=120
    )
    creativity_scale.pack(anchor='w', pady=(2, 0))
    
    tk.Label(creativity_frame, text="0.0 = Précis | 1.0 = Créatif", 
             font=('Segoe UI', 7, 'italic'), bg=theme["bg"], fg='#888888').pack(anchor='w')
    
    # Fonction pour toggle le collapse de la section style
    def toggle_style_section():
        if style_collapsed.get():
            # Afficher
            style_content.pack(fill='x', pady=(10, 0))
            style_collapse_icon.config(text="▼")
            style_collapsed.set(False)
        else:
            # Cacher
            style_content.pack_forget()
            style_collapse_icon.config(text="▶")
            style_collapsed.set(True)
    
    # Bind du clic sur le header style (tous les éléments)
    style_header.bind('<Button-1>', lambda e: toggle_style_section())
    style_collapse_icon.bind('<Button-1>', lambda e: toggle_style_section())
    style_label.bind('<Button-1>', lambda e: toggle_style_section())
    
    # ===== NOUVEAU : SECTION 3: PERSONNAGES (COLLAPSIBLE) =====
    characters_section = tk.Frame(main_frame, bg=theme["bg"])
    characters_section.pack(fill='x', pady=(15, 15))
    
    # Variable pour tracker l'état (ouvert/fermé) - FERMÉ par défaut
    characters_collapsed = tk.BooleanVar(value=True)
    
    # Header cliquable
    characters_header = tk.Frame(characters_section, bg=theme["bg"], cursor='hand2')
    characters_header.pack(fill='x')
    
    collapse_icon = tk.Label(characters_header, text="▶", font=('Segoe UI', 10, 'bold'),
                            bg=theme["bg"], fg=theme["fg"], cursor='hand2')
    collapse_icon.pack(side='left', padx=(0, 5))
    
    characters_label = tk.Label(characters_header, text="👥 Définition des personnages (pour contexte enrichi)", 
                               font=('Segoe UI', 11, 'bold'), bg=theme["bg"], fg=theme["fg"],
                               cursor='hand2')
    characters_label.pack(side='left')
    
    # Bouton Scanner à droite
    def scan_characters():
        """Scanne les fichiers .rpy du projet pour détecter les personnages"""
        try:
            from infrastructure.helpers.unified_functions import show_custom_messagebox
            from ui.themes import theme_manager
            import re
            import os
            
            # Récupérer le chemin du projet actuel depuis main_interface
            if not hasattr(main_interface, 'current_project_path') or not main_interface.current_project_path:
                show_custom_messagebox(
                    'warning',
                    '⚠️ Aucun projet ouvert',
                    'Veuillez d\'abord ouvrir un projet Ren\'Py.\n\nUtilisez le bouton "📂 Ouvrir Projet" dans la section Installation & Surveillance.',
                    theme_manager.get_theme(),
                    parent=dialog
                )
                return
            
            game_directory = main_interface.current_project_path
            if not os.path.exists(game_directory):
                show_custom_messagebox(
                    'warning',
                    '⚠️ Projet introuvable',
                    f'Le dossier du projet est introuvable :\n{game_directory}',
                    theme_manager.get_theme(),
                    parent=dialog
                )
                return
            
            # Rechercher tous les fichiers .rpy
            characters_found = {}
            pattern = re.compile(r'define\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*Character\s*\(\s*[_]*\(\s*["\']([^"\']+)["\']\s*\)|define\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*Character\s*\(\s*["\']([^"\']+)["\']\s*\)')
            
            for root, dirs, files in os.walk(game_directory):
                for file in files:
                    if file.endswith('.rpy'):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                content = f.read()
                                # Chercher les définitions de personnages
                                matches = re.finditer(
                                    r'define\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*Character\s*\(\s*(?:_+\()?\s*["\']([^"\']+)["\']',
                                    content
                                )
                                for match in matches:
                                    char_key = match.group(1)
                                    char_name = match.group(2)
                                    if char_key and char_name:
                                        characters_found[char_key] = char_name
                        except Exception:
                            continue
            
            if not characters_found:
                show_custom_messagebox(
                    'info',
                    'ℹ️ Aucun personnage trouvé',
                    'Aucune définition de personnage trouvée dans les fichiers .rpy du projet.',
                    theme_manager.get_theme(),
                    parent=dialog
                )
                return
            
            # Afficher les résultats et demander confirmation
            result_message = f"Personnages détectés : {len(characters_found)}\n\n"
            
            # Organiser en colonnes (3 colonnes)
            char_items = list(characters_found.items())
            max_items = min(15, len(char_items))  # Afficher max 15 personnages
            
            # Calculer le nombre de lignes nécessaires
            cols = 3
            rows = (max_items + cols - 1) // cols
            
            # Créer les colonnes
            for row in range(rows):
                line = ""
                for col in range(cols):
                    idx = row * cols + col
                    if idx < max_items:
                        key, name = char_items[idx]
                        line += f"[{key}] = {name:<15}"
                        if col < cols - 1 and idx < max_items - 1:
                            line += " | "
                result_message += line + "\n"
            
            if len(characters_found) > max_items:
                result_message += f"\n... et {len(characters_found) - max_items} autres personnages"
            
            confirm = show_custom_messagebox(
                'askyesno',
                '🔍 Personnages détectés',
                result_message + "\n\nVoulez-vous importer ces personnages ?",
                theme_manager.get_theme(),
                parent=dialog
            )
            
            if confirm:
                # Vider la liste actuelle
                for frame in dialog.character_frames:
                    frame.destroy()
                dialog.character_frames = []
                dialog.characters_list_data = {}
                
                # Ajouter les personnages trouvés
                for char_key, char_name in characters_found.items():
                    add_character_row(char_key, 'Homme', char_name)
                
                # Ouvrir la section si elle est fermée
                if characters_collapsed.get():
                    toggle_characters_section()
                
                log_message("INFO", f"{len(characters_found)} personnages importés", category="groq_customizer")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur scan personnages: {e}", category="groq_customizer")
    
    scan_btn = tk.Button(characters_header, text="🔍 Scanner", 
                        command=scan_characters,
                        bg=theme["button_utility_bg"], fg="#000000",
                        font=('Segoe UI', 9, 'bold'), pady=2, padx=8,
                        relief='flat', cursor='hand2')
    scan_btn.pack(side='right')
    
    # Container pour le contenu (liste de personnages) - FERMÉ par défaut
    characters_content = tk.Frame(characters_section, bg=theme["bg"])
    # characters_content.pack(fill='x', pady=(10, 0))  # Pas d'affichage initial
    
    # Initialiser la liste des personnages
    dialog.characters_list_data = config_manager.get('groq_characters_definitions', {})
    
    # Frame scrollable pour les personnages (2 colonnes)
    characters_list_container = tk.Frame(characters_content, bg=theme["bg"])
    characters_list_container.pack(fill='both', expand=True, pady=(0, 10))
    
    # Canvas pour le scroll
    characters_canvas = tk.Canvas(characters_list_container, bg=theme["bg"], height=200)
    characters_canvas.pack(side='left', fill='both', expand=True)
    
    # Scrollbar
    characters_scrollbar = tk.Scrollbar(characters_list_container, orient="vertical", command=characters_canvas.yview)
    characters_scrollbar.pack(side='right', fill='y')
    characters_canvas.configure(yscrollcommand=characters_scrollbar.set)
    
    # Frame pour le contenu des personnages (2 colonnes)
    characters_inner_frame = tk.Frame(characters_canvas, bg=theme["bg"])
    characters_canvas.create_window((0, 0), window=characters_inner_frame, anchor="nw")
    
    # Colonnes pour les personnages
    characters_col1 = tk.Frame(characters_inner_frame, bg=theme["bg"])
    characters_col2 = tk.Frame(characters_inner_frame, bg=theme["bg"])
    
    characters_col1.pack(side='left', fill='both', expand=True, padx=(0, 5))
    characters_col2.pack(side='right', fill='both', expand=True, padx=(5, 0))
    
    # Stocker les frames de personnages pour pouvoir les supprimer
    dialog.character_frames = []
    
    def add_character_row(char_key='', genre='Homme', prenom=''):
        """Ajoute une ligne de personnage"""
        # Choisir la colonne (alternance ou basée sur le nombre actuel)
        target_col = characters_col1 if len(dialog.character_frames) % 2 == 0 else characters_col2
        
        char_row = tk.Frame(target_col, bg=theme["bg"])
        char_row.pack(fill='x', pady=2)
        
        # Locuteur
        tk.Label(char_row, text="[", font=('Segoe UI', 9), bg=theme["bg"], fg=theme["fg"]).pack(side='left')
        
        locuteur_entry = tk.Entry(char_row, width=3, font=('Segoe UI', 9), 
                                  bg=theme["entry_bg"], fg=theme["entry_fg"],
                                  insertbackground=theme["entry_fg"])
        locuteur_entry.pack(side='left')
        locuteur_entry.insert(0, char_key)
        
        tk.Label(char_row, text="]", font=('Segoe UI', 9), bg=theme["bg"], fg=theme["fg"]).pack(side='left', padx=(0, 10))
        
        # Genre
        tk.Label(char_row, text="Genre :", font=('Segoe UI', 9), bg=theme["bg"], fg=theme["fg"]).pack(side='left', padx=(0, 5))
        
        genre_var = tk.StringVar(value=genre)
        genre_combo = ttk.Combobox(char_row, textvariable=genre_var,
                                   values=["Fille", "Garçon", "Adolescent", "Adolescente", "Homme", "Femme"],
                                   state="readonly", width=12, font=('Segoe UI', 9))
        genre_combo.pack(side='left', padx=(0, 10))
        
        # Prénom
        tk.Label(char_row, text="Prénom :", font=('Segoe UI', 9), bg=theme["bg"], fg=theme["fg"]).pack(side='left', padx=(0, 5))
        
        prenom_entry = tk.Entry(char_row, width=20, font=('Segoe UI', 9),
                               bg=theme["entry_bg"], fg=theme["entry_fg"],
                               insertbackground=theme["entry_fg"])
        prenom_entry.pack(side='left', padx=(0, 10))
        prenom_entry.insert(0, prenom)
        
        # Bouton supprimer
        def remove_this_row():
            char_row.destroy()
            if char_row in dialog.character_frames:
                dialog.character_frames.remove(char_row)
            update_characters_data()
            update_scroll_region()
        
        tk.Button(char_row, text="✖", command=remove_this_row,
                 bg=theme["button_danger_bg"], fg="#000000", font=('Segoe UI', 7, 'bold'),
                 width=2, pady=1, relief='flat', cursor='hand2').pack(side='left')
        
        # Stocker les widgets
        char_row.locuteur_entry = locuteur_entry
        char_row.genre_var = genre_var
        char_row.prenom_entry = prenom_entry
        
        dialog.character_frames.append(char_row)
        
        # Mise à jour auto lors de changements
        def on_change(*args):
            update_characters_data()
            update_scroll_region()
        
        locuteur_entry.bind('<KeyRelease>', on_change)
        prenom_entry.bind('<KeyRelease>', on_change)
        genre_combo.bind('<<ComboboxSelected>>', on_change)
        
        # Mettre à jour la région de scroll
        update_scroll_region()
        
        # Re-lier la molette aux nouveaux widgets
        _bind_mousewheel_to_children(char_row)
    
    def update_scroll_region():
        """Met à jour la région de scroll du canvas"""
        characters_canvas.update_idletasks()
        characters_canvas.configure(scrollregion=characters_canvas.bbox("all"))
    
    # Support de la molette de la souris sur toute la zone
    def _on_mousewheel(event):
        characters_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _bind_mousewheel_to_children(widget):
        """Lie la molette de la souris à un widget et tous ses enfants"""
        widget.bind("<MouseWheel>", _on_mousewheel)
        for child in widget.winfo_children():
            _bind_mousewheel_to_children(child)
    
    # Lier la molette à toute la zone des personnages
    _bind_mousewheel_to_children(characters_list_container)
    
    def load_characters_from_dict(characters_dict):
        """Charge les personnages depuis un dictionnaire"""
        # Vider la liste actuelle
        for frame in dialog.character_frames:
            frame.destroy()
        dialog.character_frames = []
        
        # Charger les nouveaux personnages
        for char_key, char_data in characters_dict.items():
            if isinstance(char_data, dict):
                genre = char_data.get('genre', 'Homme')
                prenom = char_data.get('prenom', '')
            else:
                # Format ancien : juste le prénom
                genre = 'Homme'
                prenom = char_data
            
            add_character_row(char_key, genre, prenom)
        
        update_characters_data()
        update_scroll_region()
        
        # Re-lier la molette à tous les nouveaux personnages
        for frame in dialog.character_frames:
            _bind_mousewheel_to_children(frame)
    
    # Enregistrer la fonction de chargement
    dialog.load_characters_func = load_characters_from_dict
    
    # Charger les personnages en attente si présents
    if hasattr(dialog, 'characters_to_load'):
        load_characters_from_dict(dialog.characters_to_load)
        delattr(dialog, 'characters_to_load')
    
    def update_characters_data():
        """Met à jour les données des personnages dans dialog.characters_list_data"""
        characters_dict = {}
        for char_frame in dialog.character_frames:
            if char_frame.winfo_exists():
                locuteur = char_frame.locuteur_entry.get().strip()
                if locuteur:  # Seulement si le locuteur n'est pas vide
                    characters_dict[locuteur] = {
                        'genre': char_frame.genre_var.get(),
                        'prenom': char_frame.prenom_entry.get().strip()
                    }
        dialog.characters_list_data = characters_dict
        config_manager.set('groq_characters_definitions', characters_dict)
        # Mettre à jour l'aperçu du prompt
        update_prompt_preview()
    
    # Fonction pour charger les personnages (utilisée aussi par load_profile)
    def load_characters_into_interface(characters_data):
        """Charge les personnages dans l'interface"""
        # Supprimer tous les personnages existants
        for char_frame in list(dialog.character_frames):
            try:
                char_frame.destroy()
            except:
                pass
        dialog.character_frames.clear()
        
        # Charger les nouveaux personnages
        for char_key, char_data in characters_data.items():
            add_character_row(char_key, char_data.get('genre', 'Homme'), char_data.get('prenom', ''))
        
        # Mettre à jour les données
        dialog.characters_list_data = characters_data
    
    # Charger les personnages existants
    for char_key, char_data in dialog.characters_list_data.items():
        add_character_row(char_key, char_data.get('genre', 'Homme'), char_data.get('prenom', ''))
    
    # Stocker la fonction pour l'utiliser dans load_profile
    dialog.load_characters_func = load_characters_into_interface
    
    # Vérifier s'il y a des personnages en attente de chargement (depuis load_profile)
    if hasattr(dialog, 'characters_to_load') and dialog.characters_to_load:
        load_characters_into_interface(dialog.characters_to_load)
        delattr(dialog, 'characters_to_load')
    
    # Bouton ajouter
    add_char_btn = tk.Button(characters_content, text="➕ Ajouter un personnage",
                            command=lambda: add_character_row(),
                            bg=theme["button_feature_bg"], fg="#000000",
                            font=('Segoe UI', 9, 'bold'), pady=4, padx=12,
                            relief='flat', cursor='hand2')
    add_char_btn.pack(anchor='w')
    
    # Fonction pour toggle le collapse
    def toggle_characters_section():
        if characters_collapsed.get():
            # Afficher
            characters_content.pack(fill='x', pady=(10, 0))
            collapse_icon.config(text="▼")
            characters_collapsed.set(False)
        else:
            # Cacher
            characters_content.pack_forget()
            collapse_icon.config(text="▶")
            characters_collapsed.set(True)
    
    # Bind du clic sur le header (tous les éléments)
    characters_header.bind('<Button-1>', lambda e: toggle_characters_section())
    collapse_icon.bind('<Button-1>', lambda e: toggle_characters_section())
    characters_label.bind('<Button-1>', lambda e: toggle_characters_section())
    
    # ===== SECTION 4: APERÇU DU PROMPT =====
    preview_section = tk.Frame(main_frame, bg=theme["bg"])
    preview_section.pack(fill='both', expand=True, pady=(0, 15))
    
    tk.Label(preview_section, text="👀 Aperçu du prompt (généré automatiquement)", 
             font=('Segoe UI', 11, 'bold'), bg=theme["bg"], fg=theme["fg"]).pack(anchor='w', pady=(0, 10))
    
    # Container pour le texte et sa scrollbar
    preview_text_container = tk.Frame(preview_section, bg=theme["bg"])
    preview_text_container.pack(fill='both', expand=True)
    
    preview_text = tk.Text(
        preview_text_container,
        height=4,
        font=('Segoe UI', 9),
        bg=theme["entry_bg"],
        fg=theme["fg"],
        wrap='word',
        relief='solid',
        borderwidth=1,
        state='disabled'
    )
    preview_text.pack(side='left', fill='both', expand=True)
    
    # Ajouter scrollbar pour aperçu
    preview_scrollbar = tk.Scrollbar(preview_text_container, orient="vertical", command=preview_text.yview)
    preview_text.configure(yscrollcommand=preview_scrollbar.set)
    preview_scrollbar.pack(side='right', fill='y')
    
    def update_prompt_preview():
        """Met à jour l'aperçu du prompt en temps réel"""
        try:
            # Récupérer toutes les valeurs
            custom_instr = instructions_text.get('1.0', 'end-1c').strip()
            tone = tone_var.get().lower()
            style = style_var.get()
            context = context_var.get()
            temperature = creativity_var.get()
            
            # Construire le prompt
            tone_instruction = ""
            if tone == "formel":
                tone_instruction = "\n4. Utilise un ton FORMEL (vouvoiement, registre soutenu)"
            elif tone == "neutre":
                tone_instruction = "\n4. Utilise un ton NEUTRE (ni tutoiement ni vouvoiement)"
            else:
                tone_instruction = "\n4. Utilise un ton INFORMEL (tutoiement, registre courant)"
            
            style_instruction = ""
            if style == "Littéral":
                style_instruction = "\n5. Traduis de manière LITTÉRALE en respectant au maximum la structure originale"
            elif style == "Créatif":
                style_instruction = "\n5. Traduis de manière CRÉATIVE en adaptant idiomes et expressions culturelles"
            else:
                style_instruction = "\n5. Traduis de manière NATURELLE en équilibrant fidélité et fluidité"
            
            context_instruction = ""
            if context != "Général":
                context_instruction = f"\n6. Contexte du jeu : {context.upper()} - adapte le vocabulaire en conséquence"
            
            custom_instruction = ""
            if custom_instr:
                custom_instruction = f"\n7. Instructions supplémentaires : {custom_instr}"
            
            # ✅ NOUVEAU : Contexte des personnages
            characters_context = ""
            if dialog.characters_list_data and len(dialog.characters_list_data) > 0:
                chars_lines = []
                for char_key, char_info in dialog.characters_list_data.items():
                    genre = char_info.get('genre', 'Neutre')
                    prenom = char_info.get('prenom', '')
                    if prenom:
                        chars_lines.append(f"[{char_key}] est un(e) {genre} du nom de {prenom}")
                    else:
                        chars_lines.append(f"[{char_key}] est un(e) {genre}")
                
                if chars_lines:
                    characters_context = "\n\nCONTEXTE DES PERSONNAGES :\n" + "\n".join(chars_lines)
                    characters_context += "\nNote : Ces lettres entre crochets peuvent aussi apparaître comme variables dans le texte."
            
            # ✅ NOUVEAU : Exemple de contexte conversationnel
            conversation_example = ""
            if dialog.characters_list_data and len(dialog.characters_list_data) > 0:
                # Prendre le premier personnage comme exemple
                first_char = list(dialog.characters_list_data.keys())[0] if dialog.characters_list_data else None
                if first_char:
                    conversation_example = f"\n\nCONTEXTE DE CONVERSATION (dialogue précédent - EXEMPLE) :\n{first_char} \"[Dialogue précédent inséré automatiquement]\""
            
            # Prompt final enrichi
            prompt = f"""Tu es un traducteur professionnel pour jeux vidéo Ren'Py. Traduis ce texte du [LANGUE_SOURCE] vers le [LANGUE_CIBLE].

RÈGLES STRICTES :
1. Préserve TOUTES les balises Ren'Py : {{i}}, {{/i}}, [p], [tooltip], \\", etc.
2. Retourne UNIQUEMENT la traduction finale, SANS notes, SANS explications, SANS commentaires
3. Ne modifie que le texte visible, jamais les balises ou la structure{tone_instruction}{style_instruction}{context_instruction}{custom_instruction}{characters_context}{conversation_example}

Texte à traduire :
[LOCUTEUR] "[TEXTE_A_TRADUIRE]"

Traduction (UNIQUEMENT le texte traduit, sans le locuteur) :"""
            
            # Afficher dans l'aperçu
            preview_text.config(state='normal')
            preview_text.delete('1.0', 'end')
            preview_text.insert('1.0', prompt)
            preview_text.config(state='disabled')
            
            # Afficher la température en bas
            temp_info = f"\n\n💡 Température (créativité) : {temperature:.1f}"
            preview_text.config(state='normal')
            preview_text.insert('end', temp_info)
            preview_text.config(state='disabled')
            
        except Exception as e:
            log_message("ERREUR", f"Erreur mise à jour aperçu prompt: {e}", category="realtime_editor")
    
    # Stocker la fonction pour l'utiliser dans load_profile
    dialog.update_prompt_preview_func = update_prompt_preview
    
    # Bindings pour mise à jour en temps réel
    instructions_text.bind('<KeyRelease>', lambda e: dialog.after(300, update_prompt_preview))
    tone_combo_dialog.bind('<<ComboboxSelected>>', lambda e: update_prompt_preview())
    style_combo.bind('<<ComboboxSelected>>', lambda e: update_prompt_preview())
    context_combo.bind('<<ComboboxSelected>>', lambda e: update_prompt_preview())
    creativity_scale.config(command=lambda v: update_prompt_preview())
    
    # ===== SECTION 4: BOUTONS D'ACTION =====
    buttons_frame = tk.Frame(main_frame, bg=theme["bg"])
    buttons_frame.pack(fill='x', pady=(15, 0))
    
    def save_settings():
        """Sauvegarde toutes les configurations"""
        try:
            # Sauvegarder dans config_manager
            config_manager.set('groq_custom_instructions', instructions_text.get('1.0', 'end-1c').strip())
            config_manager.set('groq_translation_style', style_var.get())
            config_manager.set('groq_game_context', context_var.get())
            config_manager.set('groq_temperature', creativity_var.get())
            config_manager.save_config()
            
            # Mettre à jour le ton dans l'interface principale
            main_interface.translation_tone = tone_var.get().lower()
            
            main_interface._update_status("✅ Configuration Groq AI sauvegardée")
            log_message("INFO", f"Configuration Groq AI sauvegardée", category="realtime_editor")
            dialog.destroy()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur sauvegarde config Groq: {e}", category="realtime_editor")
            main_interface._update_status("❌ Erreur sauvegarde configuration")
    
    def reset_to_default():
        """Réinitialise aux valeurs par défaut"""
        instructions_text.delete('1.0', 'end')
        tone_var.set('Informel')
        style_var.set('Naturel')
        context_var.set('Général')
        creativity_var.set(0.3)
        update_prompt_preview()
    
    # Boutons
    tk.Button(
        buttons_frame,
        text="💾 Sauvegarder",
        command=save_settings,
        bg=theme["button_primary_bg"],
        fg="#000000",
        font=('Segoe UI', 10, 'bold'),
        pady=6,
        padx=20,
        relief='flat',
        cursor='hand2'
    ).pack(side='right', padx=(5, 0))
    
    tk.Button(
        buttons_frame,
        text="🔄 Réinitialiser",
        command=reset_to_default,
        bg=theme["button_tertiary_bg"],
        fg="#000000",
        font=('Segoe UI', 10),
        pady=6,
        padx=15,
        relief='flat',
        cursor='hand2'
    ).pack(side='right', padx=(5, 0))
    
    tk.Button(
        buttons_frame,
        text="❌ Annuler",
        command=dialog.destroy,
        bg=theme["button_secondary_bg"],
        fg="#000000",
        font=('Segoe UI', 10),
        pady=6,
        padx=15,
        relief='flat',
        cursor='hand2'
    ).pack(side='right')
    
    # Aperçu initial
    dialog.after(200, update_prompt_preview)
    
    # Si un profil est déjà actif, le charger
    current_active_profile = config_manager.get('groq_current_profile', 'Par défaut')
    if current_active_profile != 'Par défaut' and current_active_profile in saved_profiles:
        current_profile_var.set(current_active_profile)
        dialog.after(300, load_profile)


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
        ("    ", "normal"), ("Version Ren'Py :", "bold"), (" La version Ren'Py est détectée automatiquement. ", "normal"),
        ("Si votre version n'est pas dans le tableau de compatibilité, vous pouvez utiliser le bouton ", "normal"),
        ("'Tester module v2'", "bold_yellow"), (" pour tester manuellement la compatibilité du module v2.\n", "normal"),
        ("    ", "normal"), ("💡 ", "bold_green"), ("Après test, merci de signaler le résultat (version + module testé + résultat) pour mettre à jour le tableau de compatibilité !\n\n", "normal"),
        
        ("2.  ", "bold"), ("Installation (une seule fois) :", "italic"), (" Cliquez sur ", "normal"), 
        ("\"Installer le module\"", "yellow"), (" pour installer le module recommandé, ou ", "normal"),
        ("\"Tester module v2\"", "bold_yellow"), (" pour tester manuellement le module v2 si votre version Ren'Py n'est pas dans le tableau de compatibilité.\n", "normal"),
        ("    ", "normal"), ("Un fichier sera ajouté au dossier ", "normal"), ("game/", "italic"), (" de votre projet.\n", "normal"),
        ("    ", "normal"), ("Note :", "bold_yellow"), (" Si vous mettez à jour RenExtract, il est conseillé de réinstaller le module pour bénéficier des derniers correctifs.\n\n", "yellow"),

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