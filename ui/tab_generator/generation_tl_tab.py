# ui/tab_generator/generation_tl_tab.py
# Onglet de génération TL - Générateur de Traductions Ren'Py
# VERSION COMPLÈTE CORRIGÉE AVEC APERÇU FONCTIONNEL

"""
Onglet de génération de traductions Ren'Py
- Interface de génération sans SDK
- Sélecteur de polices GUI individuelles (3x2)
- Génération avec ou sans polices
- Support RTL et caractères français
- Aperçu de polices fonctionnel avec bouton d'ajout dédié
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import platform
from pathlib import Path
from ui.themes import theme_manager
from infrastructure.config.config import config_manager
from core.services.translation.font_manager import FontManager
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import show_translated_messagebox, show_custom_messagebox

# ===== WRAPPERS POUR FONTMANAGER =====

def _get_font_manager():
    """Retourne une instance du FontManager"""
    tools_dir = config_manager.get('tools_directory', os.path.expanduser("~/.renextract_tools"))
    return FontManager(tools_dir)

def cleanup_unused_temporary_fonts_only():
    """Nettoie intelligemment les polices temporaires via FontManager"""
    try:
        prefs = config_manager.get_font_preferences()
        individual_fonts = prefs.get('individual_fonts', {})
        
        used_font_names = set()
        for font_type, font_config in individual_fonts.items():
            if font_config.get('enabled', False):
                used_font_names.add(font_config.get('font_name', ''))
        
        font_manager = _get_font_manager()
        removed_count = font_manager.cleanup_unused_temporary_fonts(used_font_names)
        
        kept_fonts = font_manager.get_temporarily_installed_fonts()
        if kept_fonts:
            log_message("DEBUG", f"Polices conservées: {list(kept_fonts.keys())}", category="renpy_generator_tl")
        
    except Exception as e:
        log_message("ERREUR", f"Erreur nettoyage intelligent polices: {e}", category="renpy_generator_tl")

def get_available_fonts_with_accents():
    """Retourne les polices depuis le FontManager centralisé"""
    try:
        tools_dir = config_manager.get('tools_directory', os.path.expanduser("~/.renextract_tools"))
        font_manager = FontManager(tools_dir)
        
        return font_manager.get_all_available_fonts()
        
    except Exception as e:
        log_message("ERREUR", f"Erreur récupération polices centralisées : {e}", category="renpy_generator_tl")
        
        # Fallback sur l'ancien système
        system = platform.system().lower()
        fonts_info = []
        
        if system == "windows":
            fonts_info = [
                {"name": "Arial", "path": "C:/Windows/Fonts/arial.ttf", "description": "Police standard", "available": True, "type": "system"}
            ]
        
        return fonts_info

def load_font_preferences(main_interface):
    """Charge les préférences de police individuelles sauvegardées"""
    try:
        prefs = config_manager.get_font_preferences()
        
        # Charger les configurations individuelles
        individual_fonts = prefs.get('individual_fonts', {})
        
        # Charger chaque type de police
        for font_type in ['text_font', 'name_text_font', 'interface_text_font', 'button_text_font', 'choice_button_text_font']:
            if font_type not in main_interface.individual_font_vars:
                main_interface.individual_font_vars[font_type] = tk.StringVar()
            
            font_config = individual_fonts.get(font_type, {})
            font_name = font_config.get('font_name', '')
            is_custom = font_config.get('is_custom', False)
            
            # Si c'est une police personnalisée, charger les infos
            if is_custom and font_config.get('font_path'):
                if not hasattr(main_interface, 'custom_fonts'):
                    main_interface.custom_fonts = {}
                main_interface.custom_fonts[font_type] = {
                    'name': font_name,
                    'path': font_config.get('font_path', ''),
                    'is_custom': True
                }
                # Afficher le nom personnalisé
                main_interface.individual_font_vars[font_type].set(f"[Personnalisée] {font_name}")
            else:
                # Police système normale
                main_interface.individual_font_vars[font_type].set(font_name)
            
            # Charger l'état activé/désactivé
            if hasattr(main_interface, 'gui_override_vars') and font_type in main_interface.gui_override_vars:
                main_interface.gui_override_vars[font_type].set(font_config.get('enabled', False))
        
    except Exception as e:
        log_message("ERREUR", f"Erreur chargement préférences police individuelles : {e}", category="renpy_generator_tl")

def save_font_preferences(main_interface):
    """Sauvegarde automatiquement les préférences de police individuelles"""
    try:
        # Récupérer les configurations individuelles
        individual_fonts = {}
        
        for font_type in ['text_font', 'name_text_font', 'interface_text_font', 'button_text_font', 'choice_button_text_font']:
            enabled = False
            font_name = ""
            font_path = ""
            is_custom = False
            
            if hasattr(main_interface, 'gui_override_vars') and font_type in main_interface.gui_override_vars:
                enabled = main_interface.gui_override_vars[font_type].get()
            
            if hasattr(main_interface, 'individual_font_vars') and font_type in main_interface.individual_font_vars:
                font_display = main_interface.individual_font_vars[font_type].get()
                
                # Vérifier si c'est une police personnalisée
                if hasattr(main_interface, 'custom_fonts') and font_type in main_interface.custom_fonts:
                    custom_info = main_interface.custom_fonts[font_type]
                    font_name = custom_info['name']
                    font_path = custom_info['path']
                    is_custom = True
                else:
                    # Police système - chercher le chemin
                    font_name = font_display
                    if font_name and hasattr(main_interface, 'available_fonts'):
                        for font_info in main_interface.available_fonts:
                            if font_info['name'] == font_name:
                                font_path = font_info['path']
                                break
            
            individual_fonts[font_type] = {
                'enabled': enabled,
                'font_name': font_name,
                'font_path': font_path,
                'is_custom': is_custom
            }
        
        preferences = {
            'apply_system_font': True,
            'individual_fonts': individual_fonts
        }
        
        config_manager.set_font_preferences(preferences)
        
    except Exception as e:
        log_message("ERREUR", f"Erreur sauvegarde préférences police individuelles : {e}", category="renpy_generator_tl")

def get_enabled_fonts_info(main_interface):
    """Retourne les informations des polices activées"""
    try:
        enabled_fonts = {}
        
        for font_type in ['text_font', 'name_text_font', 'interface_text_font', 'button_text_font', 'choice_button_text_font']:
            # Vérifier si cette police est activée
            if (hasattr(main_interface, 'gui_override_vars') and 
                font_type in main_interface.gui_override_vars and 
                main_interface.gui_override_vars[font_type].get()):
                
                # Vérifier si c'est une police personnalisée
                if hasattr(main_interface, 'custom_fonts') and font_type in main_interface.custom_fonts:
                    custom_info = main_interface.custom_fonts[font_type]
                    enabled_fonts[font_type] = {
                        'name': custom_info['name'],
                        'path': custom_info['path'],
                        'description': f"Police personnalisée: {custom_info['name']}",
                        'available': os.path.exists(custom_info['path']),
                        'is_custom': True
                    }
                else:
                    # Police système
                    font_name = ""
                    if (hasattr(main_interface, 'individual_font_vars') and 
                        font_type in main_interface.individual_font_vars):
                        font_name = main_interface.individual_font_vars[font_type].get()
                    
                    # Trouver les détails de la police système
                    if font_name and hasattr(main_interface, 'available_fonts'):
                        for font_info in main_interface.available_fonts:
                            if font_info['name'] == font_name:
                                enabled_fonts[font_type] = {
                                    'name': font_info['name'],
                                    'path': font_info['path'],
                                    'description': font_info['description'],
                                    'available': font_info.get('available', True),
                                    'is_custom': False
                                }
                                break
        
        return enabled_fonts
        
    except Exception as e:
        log_message("ERREUR", f"Erreur récupération info polices activées : {e}", category="renpy_generator_tl")
        return {}

def add_custom_font_with_refresh(main_interface):
    """Ajoute une police personnalisée et l'installe temporairement pour l'aperçu"""
    try:
        from tkinter import filedialog
        
        filetypes = [
            ("Fichiers de police", "*.ttf *.otf *.woff *.woff2"),
            ("TrueType Font", "*.ttf"),
            ("OpenType Font", "*.otf"), 
            ("Web Font", "*.woff *.woff2"),
            ("Tous les fichiers", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Sélectionner une police personnalisée",
            filetypes=filetypes,
            parent=main_interface.window
        )
        
        if filename:
            # Ajouter au gestionnaire centralisé
            tools_dir = config_manager.get('tools_directory', os.path.expanduser("~/.renextract_tools"))
            font_manager = FontManager(tools_dir)
            
            success, message = font_manager.add_custom_font(filename)
            if success:
                font_name = Path(filename).stem
                
                # 🆕 INSTALLATION TEMPORAIRE pour l'aperçu (seulement custom fonts)
                install_success = font_manager.install_font_temporarily(filename, font_name)
                # Logs gérés par font_manager
                
                # Mise à jour globale de toutes les listes
                refresh_all_font_lists_globally(main_interface)
                
                # Sélectionner la nouvelle police dans l'aperçu
                if hasattr(main_interface, 'preview_font_combo'):
                    main_interface.preview_font_combo.set(font_name)
                    main_interface.preview_font_var.set(font_name)
                    update_font_preview_fixed(main_interface)
                
                main_interface._show_notification(f"Police '{font_name}' ajoutée avec succès", "info")
                log_message("INFO", f"Police personnalisée ajoutée et aperçu mis à jour : {font_name}", category="renpy_generator_tl")
            else:
                main_interface._show_notification(f"Erreur ajout police : {message}", "error")
                
    except Exception as e:
        main_interface._show_notification(f"Erreur ajout police : {e}", "error")
        log_message("ERREUR", f"Erreur add_custom_font_with_refresh : {e}", category="renpy_generator_tl")

def refresh_all_font_lists_globally(main_interface):
    """Met à jour toutes les listes de polices : aperçu + comboboxes GUI"""
    try:
        # ✅ PROTECTION : Éviter la récursion infinie
        if hasattr(main_interface, '_refreshing_fonts'):
            return
        main_interface._refreshing_fonts = True
        
        # Récupérer les polices mises à jour
        updated_fonts = get_available_fonts_with_accents()
        font_names = [font['name'] for font in updated_fonts]
        
        # 1. Mettre à jour la combobox d'aperçu (sans option parcourir)
        if hasattr(main_interface, 'preview_font_combo'):
            current_preview = main_interface.preview_font_combo.get()
            main_interface.preview_font_combo['values'] = font_names
            if current_preview in font_names:
                # ✅ PROTECTION : Mise à jour silencieuse sans déclencher les callbacks
                main_interface.preview_font_combo.set(current_preview)
            elif font_names:
                # ✅ PROTECTION : Mise à jour silencieuse sans déclencher les callbacks
                main_interface.preview_font_combo.set(font_names[0])
                main_interface.preview_font_var.set(font_names[0])
        
        # 2. Mettre à jour toutes les comboboxes GUI (avec option parcourir)
        gui_font_options = ["[Parcourir police personnalisée...]"] + font_names
        
        # Récupérer toutes les comboboxes GUI stockées
        if hasattr(main_interface, '_all_font_combos'):
            for combo_ref in main_interface._all_font_combos:
                try:
                    current_selection = combo_ref.get()
                    combo_ref['values'] = gui_font_options
                    if current_selection in gui_font_options:
                        combo_ref.set(current_selection)
                except:
                    pass  # Ignorer les comboboxes supprimées
        
        # 3. Mettre à jour la référence globale
        main_interface.available_fonts = updated_fonts
        
        log_message("DEBUG", f"Toutes les listes mises à jour : {len(updated_fonts)} polices", category="renpy_generator_tl")
        
    except Exception as e:
        log_message("ERREUR", f"Erreur refresh_all_font_lists_globally : {e}", category="renpy_generator_tl")
    finally:
        # ✅ PROTECTION : Libérer le verrou de protection
        if hasattr(main_interface, '_refreshing_fonts'):
            delattr(main_interface, '_refreshing_fonts')

def update_font_preview_fixed(main_interface):
    """Version VRAIMENT corrigée de la mise à jour d'aperçu - teste toutes les méthodes possibles"""
    try:
        selected_font = main_interface.preview_font_var.get()
        
        if not selected_font or not hasattr(main_interface, 'preview_text_label') or not main_interface.preview_text_label:
            return
        
        preview_updated = False
        
        # Détecter si c'est une police personnalisée (depuis FontManager)
        is_custom_font = False
        custom_font_path = None
        try:
            tools_dir = config_manager.get('tools_directory', os.path.expanduser("~/.renextract_tools"))
            font_manager = FontManager(tools_dir)
            custom_font_path = font_manager.get_font_for_project(selected_font)
            is_custom_font = custom_font_path and Path(custom_font_path).exists()
            # Log supprimé pour éviter le spam sur les polices système
        except:
            pass
        
        # Méthode 1: Police personnalisée - aperçu avec installation temporaire via FontManager
        if not preview_updated and is_custom_font and custom_font_path:
            try:
                font_manager = _get_font_manager()
                temporarily_installed = font_manager.get_temporarily_installed_fonts()
                
                # Vérifier si la police est déjà installée temporairement
                if selected_font not in temporarily_installed:
                    # Tenter l'installation temporaire (seulement pour custom fonts)
                    font_manager.install_font_temporarily(custom_font_path, selected_font)
                
                # Essayer l'aperçu direct avec la police
                try:
                    preview_text = "Voix ambiguë d'un cœur qui au zéphyr préfère les jattes de kiwis."
                    main_interface.preview_text_label.config(image="", text=preview_text)
                    main_interface.preview_text_label.config(font=(selected_font, 11))
                    preview_updated = True
                    log_message("INFO", f"✅ Aperçu police: {selected_font}", category="renpy_generator_tl")
                except Exception as e_preview:
                    # Fallback vers indication textuelle
                    preview_text = f"📝 Police: {selected_font}\n\nVoix ambiguë d'un cœur qui au zéphyr préfère les jattes de kiwis.\n\n(Sera appliquée dans le jeu)"
                    main_interface.preview_text_label.config(image="", text=preview_text, font=('Arial', 10))
                    preview_updated = True
                    log_message("DEBUG", f"Aperçu textuel pour: {selected_font} ({e_preview})", category="renpy_generator_tl")
                    
            except Exception as e:
                log_message("ERREUR", f"Échec aperçu police pour {selected_font}: {e}", category="renpy_generator_tl")
        
        # Méthode 2: Police système standard par nom
        if not preview_updated:
            try:
                # Restaurer le texte si une image était affichée
                preview_text = "Voix ambiguë d'un cœur qui au zéphyr préfère les jattes de kiwis."
                main_interface.preview_text_label.config(image="", text=preview_text)
                
                # Essayer directement avec le nom de police
                main_interface.preview_text_label.config(font=(selected_font, 11))
                preview_updated = True
                log_message("DEBUG", f"✅ Aperçu mis à jour avec police système: {selected_font}", category="renpy_generator_tl")
            except Exception as e:
                log_message("DEBUG", f"Échec méthode nom système pour {selected_font}: {e}", category="renpy_generator_tl")
        
        # Méthode 3: Polices courantes par nom alternatif
        if not preview_updated:
            try:
                # Restaurer le texte si une image était affichée
                preview_text = "Voix ambiguë d'un cœur qui au zéphyr préfère les jattes de kiwis."
                main_interface.preview_text_label.config(image="", text=preview_text)
                
                # Essayer avec des noms alternatifs courants
                font_alternatives = {
                    'Arial': ['Arial', 'Liberation Sans', 'DejaVu Sans'],
                    'Times New Roman': ['Times New Roman', 'Times', 'Liberation Serif'],
                    'Calibri': ['Calibri', 'Carlito', 'Liberation Sans'],
                    'Verdana': ['Verdana', 'DejaVu Sans'],
                    'Georgia': ['Georgia', 'Liberation Serif'],
                    'Helvetica': ['Helvetica', 'Arial', 'DejaVu Sans']
                }
                
                alternatives = font_alternatives.get(selected_font, [selected_font])
                for alt_font in alternatives:
                    try:
                        main_interface.preview_text_label.config(font=(alt_font, 11))
                        preview_updated = True
                        log_message("DEBUG", f"✅ Aperçu mis à jour avec police alternative {alt_font} pour: {selected_font}", category="renpy_generator_tl")
                        break
                    except:
                        continue
            except Exception as e:
                log_message("DEBUG", f"Échec méthode alternatives pour {selected_font}: {e}", category="renpy_generator_tl")
        
        # Méthode 4: Fallback Arial/Sans-serif
        if not preview_updated:
            try:
                # Restaurer le texte si une image était affichée
                preview_text = "Voix ambiguë d'un cœur qui au zéphyr préfère les jattes de kiwis."
                main_interface.preview_text_label.config(image="", text=preview_text)
                
                fallback_fonts = ['Arial', 'sans-serif', 'DejaVu Sans', 'Liberation Sans', 'Helvetica']
                for fallback in fallback_fonts:
                    try:
                        main_interface.preview_text_label.config(font=(fallback, 11))
                        preview_updated = True
                        log_message("ATTENTION", f"Aperçu fallback {fallback} pour : {selected_font}", category="renpy_generator_tl")
                        break
                    except:
                        continue
            except:
                pass
        
        # Méthode 5: Dernier recours - police par défaut du système
        if not preview_updated:
            try:
                # Restaurer le texte si une image était affichée
                preview_text = "Voix ambiguë d'un cœur qui au zéphyr préfère les jattes de kiwis."
                main_interface.preview_text_label.config(image="", text=preview_text)
                
                main_interface.preview_text_label.config(font=("TkDefaultFont", 11))
                log_message("ATTENTION", f"Aperçu avec police par défaut système pour : {selected_font}", category="renpy_generator_tl")
            except:
                log_message("ERREUR", f"Impossible de mettre à jour l'aperçu pour : {selected_font}", category="renpy_generator_tl")
        
        # Forcer le refresh visuel
        try:
            main_interface.preview_text_label.update_idletasks()
            if hasattr(main_interface.preview_text_label, 'master'):
                main_interface.preview_text_label.master.update_idletasks()
        except:
            pass
        
    except Exception as e:
        log_message("ERREUR", f"Erreur critique update_font_preview_fixed : {e}", category="renpy_generator_tl")
        # Dernier recours absolu
        try:
            if hasattr(main_interface, 'preview_text_label') and main_interface.preview_text_label:
                preview_text = "Voix ambiguë d'un cœur qui au zéphyr préfère les jattes de kiwis."
                main_interface.preview_text_label.config(image="", text=preview_text, font=("TkDefaultFont", 11))
        except:
            pass

def create_font_preview_section(parent_frame, main_interface, theme):
    """Section aperçu des polices avec bouton d'ajout dédié"""
    preview_frame = tk.Frame(parent_frame, bg=theme["bg"])
    preview_frame.pack(fill='x', pady=(0, 10))
    
    # Ligne principale avec bouton à gauche, sélecteur au centre, et aperçu à droite
    main_preview_frame = tk.Frame(preview_frame, bg=theme["bg"])
    main_preview_frame.pack(fill='x', pady=(0, 10))
    
    # Bouton "Ajouter une police" à gauche
    add_font_btn = tk.Button(
        main_preview_frame,
        text="➕ Ajouter une police",
        command=lambda: add_custom_font_with_refresh(main_interface),
        bg=theme["button_feature_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    add_font_btn.pack(side='left', padx=(0, 15))
    
    # Sélecteur de police au centre
    selector_frame = tk.Frame(main_preview_frame, bg=theme["bg"])
    selector_frame.pack(side='left', padx=(0, 15))
    
    tk.Label(selector_frame,
            text="Police :",
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"]).pack(side='left')
    
    # Combobox SANS l'option "Parcourir" 
    preview_font_combo = ttk.Combobox(
        selector_frame,
        textvariable=main_interface.preview_font_var,
        width=20,
        state="readonly",
        font=('Segoe UI', 9)
    )
    preview_font_combo.pack(side='left', padx=(10, 0))
    
    # Stocker la référence pour usage global
    main_interface.preview_font_combo = preview_font_combo
    
    # Zone d'aperçu à droite - s'étend pour prendre l'espace restant
    preview_container = tk.Frame(main_preview_frame, bg='white', relief='solid', borderwidth=1, height=50)
    preview_container.pack(side='right', fill='both', expand=True, padx=(0, 0))
    preview_container.pack_propagate(False)

    preview_text = "Voix ambiguë d'un cœur qui au zéphyr préfère les jattes de kiwis."
    main_interface.preview_text_label = tk.Label(
        preview_container,
        text=preview_text,
        font=('Arial', 11),
        bg='white',
        fg='black',
        padx=10,
        pady=8,
        justify='center',
        wraplength=500
    )
    main_interface.preview_text_label.pack(expand=True)
    
    return preview_font_combo

def setup_preview_combo(preview_font_combo, main_interface):
    """Configuration de la combobox d'aperçu"""
    try:
        # Remplir avec les polices disponibles (SANS option parcourir)
        available_fonts = get_available_fonts_with_accents()
        font_names = [font['name'] for font in available_fonts]
        
        preview_font_combo['values'] = font_names
        
        # Sélection par défaut
        if font_names:
            default_font = font_names[0]
            preview_font_combo.set(default_font)
            main_interface.preview_font_var.set(default_font)
            update_font_preview_fixed(main_interface)
        
        # Callback pour changement de sélection
        def on_preview_selection_changed(event):
            # ✅ PROTECTION : Éviter la récursion si on est en train de rafraîchir
            if hasattr(main_interface, '_refreshing_fonts'):
                return
                
            selected_font = event.widget.get()
            main_interface.preview_font_var.set(selected_font)
            update_font_preview_fixed(main_interface)
        
        preview_font_combo.bind('<<ComboboxSelected>>', on_preview_selection_changed)
        
        
    except Exception as e:
        log_message("ERREUR", f"Erreur setup_preview_combo : {e}", category="renpy_generator_tl")

def register_font_combo_for_updates(main_interface, combo):
    """Enregistre une combobox pour les mises à jour automatiques"""
    if not hasattr(main_interface, '_all_font_combos'):
        main_interface._all_font_combos = []
    
    if combo not in main_interface._all_font_combos:
        main_interface._all_font_combos.append(combo)

def create_font_gui_section_2x3(font_frame, main_interface, theme):
    """Crée la section polices GUI avec grille 2 lignes x 3 colonnes"""
    
    # Interface réorganisée en grille 2x3 avec colonnes fixes
    gui_grid_frame = tk.Frame(font_frame, bg=theme["bg"])
    gui_grid_frame.pack(fill='x', pady=(0, 10))
    
    # Configuration des colonnes avec largeurs fixes pour alignement parfait
    gui_grid_frame.grid_columnconfigure(0, weight=1, uniform="col")
    gui_grid_frame.grid_columnconfigure(1, weight=1, uniform="col") 
    gui_grid_frame.grid_columnconfigure(2, weight=1, uniform="col")
    
    # Stockage des comboboxes pour configuration ultérieure
    font_combos = {}
    
    # LIGNE 1
    # Colonne 1: Texte principal
    col1_frame = tk.Frame(gui_grid_frame, bg=theme["bg"])
    col1_frame.grid(row=0, column=0, sticky='ew', padx=(0, 10), pady=5)
    
    text_check = tk.Checkbutton(
        col1_frame,
        text="Texte principal (dialogues)",
        variable=main_interface.gui_override_vars['text_font'],
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        selectcolor=theme["entry_bg"],
        command=lambda: save_font_preferences(main_interface)
    )
    text_check.pack(anchor='w')
    
    text_font_combo = ttk.Combobox(
        col1_frame,
        textvariable=main_interface.individual_font_vars['text_font'],
        width=18,
        state="readonly",
        font=('Segoe UI', 8)
    )
    text_font_combo.pack(anchor='w', pady=(2, 0), fill='x')
    font_combos['text_font'] = text_font_combo
    register_font_combo_for_updates(main_interface, text_font_combo)
    
    # Colonne 2: Noms des personnages
    col2_frame = tk.Frame(gui_grid_frame, bg=theme["bg"])
    col2_frame.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
    
    name_check = tk.Checkbutton(
        col2_frame,
        text="Noms des personnages",
        variable=main_interface.gui_override_vars['name_text_font'],
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        selectcolor=theme["entry_bg"],
        command=lambda: save_font_preferences(main_interface)
    )
    name_check.pack(anchor='w')
    
    name_font_combo = ttk.Combobox(
        col2_frame,
        textvariable=main_interface.individual_font_vars['name_text_font'],
        width=18,
        state="readonly",
        font=('Segoe UI', 8)
    )
    name_font_combo.pack(anchor='w', pady=(2, 0), fill='x')
    font_combos['name_text_font'] = name_font_combo
    register_font_combo_for_updates(main_interface, name_font_combo)
    
    # Colonne 3: Interface utilisateur
    col3_frame = tk.Frame(gui_grid_frame, bg=theme["bg"])
    col3_frame.grid(row=0, column=2, sticky='ew', padx=(10, 0), pady=5)
    
    interface_check = tk.Checkbutton(
        col3_frame,
        text="Interface utilisateur",
        variable=main_interface.gui_override_vars['interface_text_font'],
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        selectcolor=theme["entry_bg"],
        command=lambda: save_font_preferences(main_interface)
    )
    interface_check.pack(anchor='w')
    
    interface_font_combo = ttk.Combobox(
        col3_frame,
        textvariable=main_interface.individual_font_vars['interface_text_font'],
        width=18,
        state="readonly",
        font=('Segoe UI', 8)
    )
    interface_font_combo.pack(anchor='w', pady=(2, 0), fill='x')
    font_combos['interface_text_font'] = interface_font_combo
    register_font_combo_for_updates(main_interface, interface_font_combo)
    
    # LIGNE 2
    # Colonne 1: Boutons généraux
    col1_frame_l2 = tk.Frame(gui_grid_frame, bg=theme["bg"])
    col1_frame_l2.grid(row=1, column=0, sticky='ew', padx=(0, 10), pady=5)
    
    button_check = tk.Checkbutton(
        col1_frame_l2,
        text="Boutons généraux",
        variable=main_interface.gui_override_vars['button_text_font'],
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        selectcolor=theme["entry_bg"],
        command=lambda: save_font_preferences(main_interface)
    )
    button_check.pack(anchor='w')
    
    button_font_combo = ttk.Combobox(
        col1_frame_l2,
        textvariable=main_interface.individual_font_vars['button_text_font'],
        width=18,
        state="readonly",
        font=('Segoe UI', 8)
    )
    button_font_combo.pack(anchor='w', pady=(2, 0), fill='x')
    font_combos['button_text_font'] = button_font_combo
    register_font_combo_for_updates(main_interface, button_font_combo)
    
    # Colonne 2: Boutons de choix
    col2_frame_l2 = tk.Frame(gui_grid_frame, bg=theme["bg"])
    col2_frame_l2.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
    
    choice_check = tk.Checkbutton(
        col2_frame_l2,
        text="Boutons de choix",
        variable=main_interface.gui_override_vars['choice_button_text_font'],
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        selectcolor=theme["entry_bg"],
        command=lambda: save_font_preferences(main_interface)
    )
    choice_check.pack(anchor='w')
    
    choice_font_combo = ttk.Combobox(
        col2_frame_l2,
        textvariable=main_interface.individual_font_vars['choice_button_text_font'],
        width=18,
        state="readonly",
        font=('Segoe UI', 8)
    )
    choice_font_combo.pack(anchor='w', pady=(2, 0), fill='x')
    font_combos['choice_button_text_font'] = choice_font_combo
    register_font_combo_for_updates(main_interface, choice_font_combo)
    
    # Colonne 3: Aide seulement
    col3_frame_l2 = tk.Frame(gui_grid_frame, bg=theme["bg"])
    col3_frame_l2.grid(row=1, column=2, sticky='ew', padx=(10, 0), pady=5)
    
    # Espacement pour aligner avec les autres colonnes
    spacer_label = tk.Label(
        col3_frame_l2,
        text="",
        bg=theme["bg"],
        font=('Segoe UI', 9)
    )
    spacer_label.pack(anchor='w')
    
    help_fonts_btn = tk.Button(
        col3_frame_l2,
        text="Aide sur les polices GUI",
        command=lambda: show_font_gui_help(main_interface.window),
        bg=theme["button_help_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    help_fonts_btn.pack(anchor='w', pady=(2, 0), fill='x')
    
    # Configurer les comboboxes
    setup_gui_font_combos(main_interface, font_combos)
    
    return font_combos

def setup_gui_font_combos(main_interface, font_combos):
    """Configuration des comboboxes GUI avec synchronisation"""
    try:
        available_fonts = get_available_fonts_with_accents()
        gui_font_options = ["[Parcourir police personnalisée...]"]
        gui_font_options.extend([font['name'] for font in available_fonts])
        
        # Configurer chaque combobox GUI
        for font_type, combo in font_combos.items():
            combo['values'] = gui_font_options
            
            # Callback pour sélection
            def make_gui_callback(ft, combo_widget):
                def on_gui_font_selected(event):
                    selected_font = event.widget.get()
                    
                    if selected_font == "[Parcourir police personnalisée...]":
                        # Rediriger vers le bouton d'ajout principal
                        main_interface._show_notification(
                            "Utilisez le bouton '➕ Ajouter une police' dans la section aperçu", 
                            "info"
                        )
                        # Remettre la sélection précédente
                        combo_widget.set("")
                    else:
                        # Police normale sélectionnée
                        if hasattr(main_interface, 'individual_font_vars') and ft in main_interface.individual_font_vars:
                            main_interface.individual_font_vars[ft].set(selected_font)
                        save_font_preferences(main_interface)
                
                return on_gui_font_selected
            
            combo.bind('<<ComboboxSelected>>', make_gui_callback(font_type, combo))
            
            # Valeur par défaut
            if len(gui_font_options) > 1:
                combo.set(gui_font_options[1])  # Première vraie police
                if hasattr(main_interface, 'individual_font_vars') and font_type in main_interface.individual_font_vars:
                    main_interface.individual_font_vars[font_type].set(available_fonts[0]['name'])
        
        main_interface.available_fonts = available_fonts
        
    except Exception as e:
        log_message("ERREUR", f"Erreur setup_gui_font_combos : {e}", category="renpy_generator_tl")

# REMPLACEMENT pour une grille bien alignée dans create_generation_tab()

def create_generation_tab_aligned(parent_notebook, main_interface):
    """Crée l'onglet de génération avec grille alignée 2x3"""
    theme = theme_manager.get_theme()
    
    # Frame principal
    tab_frame = tk.Frame(parent_notebook, bg=theme["bg"])
    parent_notebook.add(tab_frame, text="Génération")
    
    # Container principal avec espacement optimisé
    main_container = tk.Frame(tab_frame, bg=theme["bg"])
    main_container.pack(fill='both', expand=True, padx=20, pady=15)
    
    # Description simplifiée
    desc_label = tk.Label(
        main_container,
        text="Génération de traductions Ren'Py avec options avancées",
        font=('Segoe UI', 10, 'bold'),
        justify='left',
        bg=theme["bg"],
        fg=theme["accent"]
    )
    desc_label.pack(anchor='w', pady=(0, 20))
    
    # ===== SECTION CONFIGURATION =====
    config_frame = tk.Frame(main_container, bg=theme["bg"])
    config_frame.pack(fill='x', pady=(0, 20))
    
    # Titre de la section configuration
    config_title = tk.Label(
        config_frame,
        text="⚙️ Configuration",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    config_title.pack(anchor='w', pady=(0, 10))
    
    # === SECTION AVEC GRILLE ALIGNÉE ===
    main_config_frame = tk.Frame(config_frame, bg=theme["bg"])
    main_config_frame.pack(fill='x', pady=(0, 10))
    
    # Configuration des colonnes pour une disposition sur une seule ligne
    main_config_frame.grid_columnconfigure(0, weight=0)    # Langue cible:
    main_config_frame.grid_columnconfigure(1, weight=0)    # [french]
    main_config_frame.grid_columnconfigure(2, weight=0)    # [?] aide langue
    main_config_frame.grid_columnconfigure(3, weight=1)    # Espace flexible
    main_config_frame.grid_columnconfigure(4, weight=0)    # ☑ Sélecteur
    main_config_frame.grid_columnconfigure(5, weight=0)    # [?] aide sélecteur
    main_config_frame.grid_columnconfigure(6, weight=1)    # Espace flexible
    main_config_frame.grid_columnconfigure(7, weight=0)    # ☑ Taille
    main_config_frame.grid_columnconfigure(8, weight=0)    # [?] aide taille
    main_config_frame.grid_columnconfigure(9, weight=1)    # Espace flexible
    main_config_frame.grid_columnconfigure(10, weight=0)   # ☑ Common
    main_config_frame.grid_columnconfigure(11, weight=0)   # [?] aide common
    main_config_frame.grid_columnconfigure(12, weight=1)   # Espace flexible
    main_config_frame.grid_columnconfigure(13, weight=0)   # ☑ Screen
    main_config_frame.grid_columnconfigure(14, weight=0)   # [?] aide screen
    main_config_frame.grid_columnconfigure(15, weight=1)   # Espace flexible
    main_config_frame.grid_columnconfigure(16, weight=0)   # ☑ Console
    main_config_frame.grid_columnconfigure(17, weight=0)   # [?] aide console
    
    # === LIGNE UNIQUE : Tous les éléments ===
    
    # Langue cible
    tk.Label(main_config_frame, 
            text="Langue cible:",
            font=('Segoe UI', 10, 'bold'),
            bg=theme["bg"],
            fg=theme["fg"]).grid(row=0, column=0, sticky='w', padx=(0, 10))
    
    lang_entry = tk.Entry(
        main_config_frame,
        textvariable=main_interface.language_var,
        font=('Segoe UI', 10),
        width=12,
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        insertbackground=theme["entry_fg"]
    )
    lang_entry.grid(row=0, column=1, sticky='w', padx=(0, 5))
    lang_entry.bind('<KeyRelease>', lambda event: on_language_changed(main_interface, event))
    lang_entry.bind('<FocusOut>', lambda event: on_language_changed(main_interface, event))

    # Aide langue
    help_lang_btn = tk.Button(
        main_config_frame,
        text="?",
        command=lambda: show_language_help(main_interface.window),
        bg=theme["button_help_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    help_lang_btn.grid(row=0, column=2, padx=(0, 20))
    
    # Options avancées screen preferences (remplace sélecteur langue + taille)
    advanced_options_btn = tk.Button(
        main_config_frame,
        text="⚙️ Options screen preferences",
        command=lambda: open_advanced_screen_options(main_interface),
        bg=theme["button_primary_bg"],
        fg="#000000",
        font=('Segoe UI', 9, 'bold'),
        pady=6,
        padx=12,
        relief='flat',
        cursor='hand2'
    )
    advanced_options_btn.grid(row=0, column=4, sticky='w', padx=(0, 5))

    advanced_options_help_btn = tk.Button(
        main_config_frame,
        text="?",
        command=lambda: show_advanced_screen_options_help(main_interface.window),
        bg=theme["button_help_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    advanced_options_help_btn.grid(row=0, column=5, padx=(0, 20))
    
    # Common.rpy
    common_check = tk.Checkbutton(
        main_config_frame,
        text="Common.rpy",
        variable=main_interface.add_common_var,
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        selectcolor=theme["entry_bg"],
        command=lambda: save_add_common_preference(main_interface)
    )
    common_check.grid(row=0, column=7, sticky='w', padx=(0, 5))

    common_help_btn = tk.Button(
        main_config_frame,
        text="?",
        command=lambda: show_common_help(main_interface.window),
        bg=theme["button_help_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    common_help_btn.grid(row=0, column=8, padx=(0, 20))
    
    # Screen.rpy
    screen_check = tk.Checkbutton(
        main_config_frame,
        text="Screen.rpy",
        variable=main_interface.add_screen_var,
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        selectcolor=theme["entry_bg"],
        command=lambda: save_add_screen_preference(main_interface)
    )
    screen_check.grid(row=0, column=10, sticky='w', padx=(0, 5))

    screen_help_btn = tk.Button(
        main_config_frame,
        text="?",
        command=lambda: show_screen_help(main_interface.window),
        bg=theme["button_help_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    screen_help_btn.grid(row=0, column=11, padx=(0, 20))
    
    # Console développeur
    dev_console_check = tk.Checkbutton(
        main_config_frame,
        text="Console développeur",
        variable=main_interface.developer_console_var,
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        selectcolor=theme["entry_bg"],
        command=lambda: save_developer_console_preference(main_interface)
    )
    dev_console_check.grid(row=0, column=13, sticky='w', padx=(0, 5))

    dev_console_help_btn = tk.Button(
        main_config_frame,
        text="?",
        command=lambda: show_developer_console_help(main_interface.window),
        bg=theme["button_help_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    dev_console_help_btn.grid(row=0, column=14)
    
    # Charger les préférences
    load_font_preferences(main_interface)
    
    # ===== SECTION APERÇU DES POLICES =====
    preview_frame = tk.Frame(main_container, bg=theme["bg"])
    preview_frame.pack(fill='x', pady=(0, 20))
    
    # Titre de la section aperçu
    preview_title = tk.Label(
        preview_frame,
        text="👁️ Aperçu des polices",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    preview_title.pack(anchor='w', pady=(0, 10))
    
    preview_font_combo = create_font_preview_section(preview_frame, main_interface, theme)
    setup_preview_combo(preview_font_combo, main_interface)
    
    # ===== SECTION OPTIONS GUI =====
    font_frame = tk.Frame(main_container, bg=theme["bg"])
    font_frame.pack(fill='x', pady=(0, 10))
    
    # Titre de la section polices GUI
    font_title = tk.Label(
        font_frame,
        text="🎨 Options de Police GUI (facultatif)",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    font_title.pack(anchor='w', pady=(0, 10))
    
    # Créer la section polices GUI
    font_combos = create_font_gui_section_2x3(font_frame, main_interface, theme)
    
    # Configuration finale avec scan en arrière-plan
    if not hasattr(main_interface, '_font_scan_started'):
        main_interface._font_scan_started = True
        
        def on_scan_complete(success, message):
            if success:
                refresh_all_font_lists_globally(main_interface)
                log_message("INFO", f"Scan polices terminé et listes mises à jour : {message}", category="renpy_generator_tl")
        
        try:
            tools_dir = config_manager.get('tools_directory', os.path.expanduser("~/.renextract_tools"))
            font_manager = FontManager(tools_dir)
            font_manager.scan_and_copy_system_fonts_async(callback=on_scan_complete)
        except Exception as e:
            log_message("ERREUR", f"Erreur démarrage scan polices : {e}", category="renpy_generator_tl")
    
    # ===== SECTION BOUTONS D'ACTION =====
    action_frame = tk.Frame(main_container, bg=theme["bg"])
    action_frame.pack(fill='x', pady=(10, 0))
    
    # Première ligne - Frame centré pour les 2 boutons principaux
    first_row_frame = tk.Frame(action_frame, bg=theme["bg"])
    first_row_frame.pack(pady=(0, 10))

    execute_checked_btn = tk.Button(
        first_row_frame,
        text="Générer les traductions + toutes les options cochées",
        command=lambda: start_generation_with_checked_options(main_interface),
        bg=theme["button_powerful_bg"],
        fg="#000000",
        font=('Segoe UI', 10, 'bold'),
        pady=6,
        padx=12,
        relief='flat',
        cursor='hand2'
    )
    execute_checked_btn.pack(side='left', padx=(0, 10))

    generate_simple_btn = tk.Button(
        first_row_frame,
        text="Générer les traductions",
        command=lambda: start_generation_simple(main_interface),
        bg=theme["button_secondary_bg"],
        fg="#000000",
        font=('Segoe UI', 10, 'bold'),
        pady=6,
        padx=12,
        relief='flat',
        cursor='hand2'
    )
    generate_simple_btn.pack(side='left')

    # Deuxième ligne - Frame centré pour les 5 autres boutons
    second_row_frame = tk.Frame(action_frame, bg=theme["bg"])
    second_row_frame.pack(pady=(20, 0))  # 20px d'espace en haut

    generate_with_fonts_btn = tk.Button(
        second_row_frame,
        text="Appliquer les polices",
        command=lambda: apply_fonts_only(main_interface),
        bg=theme["button_primary_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    generate_with_fonts_btn.pack(side='left', padx=(0, 10))

    # Créer screen preferences (sans générer les traductions)
    create_screen_prefs_btn = tk.Button(
        second_row_frame,
        text="⚙️ Créer screen preferences",
        command=lambda: create_screen_preferences_only(main_interface),
        bg=theme["button_feature_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    create_screen_prefs_btn.pack(side='left', padx=(0, 10))

    dev_console_btn = tk.Button(
        second_row_frame,
        text="Console développeur",
        command=lambda: create_developer_console_only(main_interface),
        bg=theme["button_devtool_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    dev_console_btn.pack(side='left', padx=(0, 10))

    reset_btn = tk.Button(
        second_row_frame,
        text="Réinitialiser les options",
        command=lambda: reset_generation_options_ui(main_interface),
        bg=theme["button_danger_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        padx=8,
        relief='flat',
        cursor='hand2'
    )
    reset_btn.pack(side='left')

    # Stocker tous les boutons d'opération pour pouvoir les griser pendant les tâches
    main_interface.operation_buttons.extend([
        generate_simple_btn, 
        generate_with_fonts_btn,
        create_screen_prefs_btn,
        dev_console_btn,
        reset_btn
    ])

def set_operation_buttons_state(main_interface, state):
    """
    Active ou désactive tous les boutons d'opération
    
    Args:
        main_interface: L'interface principale
        state: 'normal' ou 'disabled'
    """
    try:
        for btn in main_interface.operation_buttons:
            btn.config(state=state)
    except Exception as e:
        log_message("ERREUR", f"Erreur changement état boutons: {e}", category="renpy_generator_tl")

def save_add_common_preference(main_interface):
    """Sauvegarde la préférence d'ajout du common.rpy"""
    try:
        enabled = main_interface.add_common_var.get()
        config_manager.set_add_common_integration(enabled)
        log_message("DEBUG", f"Common.rpy: {'activé' if enabled else 'désactivé'}", category="renpy_generator_tl")
    except Exception as e:
        log_message("ERREUR", f"Erreur sauvegarde common.rpy : {e}", category="renpy_generator_tl")

def save_add_screen_preference(main_interface):
    """Sauvegarde la préférence d'ajout du screen.rpy"""
    try:
        enabled = main_interface.add_screen_var.get()
        config_manager.set_add_screen_integration(enabled)
        log_message("DEBUG", f"Screen.rpy: {'activé' if enabled else 'désactivé'}", category="renpy_generator_tl")
    except Exception as e:
        log_message("ERREUR", f"Erreur sauvegarde screen.rpy : {e}", category="renpy_generator_tl")

def save_developer_console_preference(main_interface):
    """Sauvegarde la préférence de la console développeur"""
    try:
        enabled = main_interface.developer_console_var.get()
        config_manager.set_developer_console_integration(enabled)
        log_message("DEBUG", f"Console dev: {'activée' if enabled else 'désactivée'}", category="renpy_generator_tl")
    except Exception as e:
        log_message("ERREUR", f"Erreur sauvegarde console dev : {e}", category="renpy_generator_tl")

def save_language_selector_preference(main_interface):
    """Sauvegarde la préférence du sélecteur de langue"""
    try:
        enabled = main_interface.language_selector_var.get()
        config_manager.set_language_selector_integration(enabled)
        log_message("DEBUG", f"Sélecteur de langue: {'activé' if enabled else 'désactivé'}", category="renpy_generator_tl")
    except Exception as e:
        log_message("ERREUR", f"Erreur sauvegarde sélecteur de langue : {e}", category="renpy_generator_tl")

def on_language_changed(main_interface, event=None):
    """Callback quand la langue change dans l'onglet génération"""
    try:
        # Délai pour éviter trop d'appels
        if hasattr(main_interface, '_language_update_timer'):
            main_interface.window.after_cancel(main_interface._language_update_timer)
        
        # Déclencher auto-fill après un délai
        main_interface._language_update_timer = main_interface.window.after(500, lambda: _trigger_auto_fill(main_interface))
        
    except Exception as e:
        log_message("ERREUR", f"Erreur on_language_changed: {e}", category="renpy_generator_tl")

def _trigger_auto_fill(main_interface):
    """Déclenche la mise à jour automatique des champs de combinaison"""
    try:
        from ui.tab_generator.combination_tab import auto_fill_combination_fields
        auto_fill_combination_fields(main_interface)
    except Exception as e:
        log_message("ERREUR", f"Erreur _trigger_auto_fill: {e}", category="renpy_generator_tl")

def start_generation_simple(main_interface):
    """Lance la génération simple SANS les options cochées"""
    try:
        if not validate_project(main_interface):
            return
        
        language = main_interface.language_var.get().strip().lower()
        if not language:
            main_interface._show_notification("Veuillez spécifier une langue cible.", "warning")
            return
        
        if not language.replace('_', '').replace('-', '').isalnum():
            main_interface._show_notification(
                "Le nom de langue contient des caractères non autorisés.\n" +
                "Utilisez uniquement des lettres, chiffres, tirets et underscores.",
                "warning"
            )
            return
        
        # Options pour génération SIMPLE - sans les cases cochées
        options = {
            'language': language,
            'apply_system_font': False,
            'create_language_selector': False,
            'create_developer_console': False,
            'create_common_file': False,
            'create_screen_file': False,
            'auto_open': getattr(main_interface, 'auto_open_var', tk.BooleanVar(value=False)).get()
        }
        
        translation_business = main_interface._get_translation_business()
        
        translation_business.generate_translations_embedded_threaded(
            main_interface.current_project_path,
            language,
            options,
            progress_callback=main_interface._on_progress_update,
            status_callback=main_interface._update_status,
            completion_callback=main_interface._on_operation_complete
        )
        
        main_interface._set_operation_running(True)
        main_interface._update_status(f"Génération de base pour '{language}'...")
        
        log_message("INFO", f"Génération simple lancée pour : {language}", category="renpy_generator_tl")
        
    except Exception as e:
        main_interface._show_notification(f"Erreur démarrage génération : {e}", "error")
        main_interface._set_operation_running(False)
        log_message("ERREUR", f"Erreur start_generation_simple : {e}", category="renpy_generator_tl")

def start_generation_with_checked_options(main_interface):
    """Lance la génération avec toutes les options cochées"""
    try:
        if not validate_project(main_interface):
            return
        
        language = main_interface.language_var.get().strip().lower()
        if not language:
            main_interface._show_notification("Veuillez spécifier une langue cible.", "warning")
            return
        
        # Récupérer l'état de toutes les checkboxes
        common_checked = main_interface.add_common_var.get()
        screen_checked = main_interface.add_screen_var.get()
        console_checked = main_interface.developer_console_var.get()
        selector_checked = main_interface.language_selector_var.get()
        fontsize_checked = main_interface.fontsize_selector_var.get()
        
        # Récupérer les options avancées de screen preferences sauvegardées
        advanced_options = config_manager.get_advanced_screen_options()
        
        # AJOUTER : Vérifier les polices cochées
        enabled_fonts = get_enabled_fonts_info(main_interface)
        apply_fonts = len(enabled_fonts) > 0
        
        # AJOUTER : Récupérer les préférences de polices si des polices sont cochées
        font_prefs = {}
        if apply_fonts:
            font_prefs = config_manager.get_font_preferences()
        
        # Construire les options (inclure les options avancées)
        options = {
            'language': language,
            'apply_system_font': apply_fonts,
            'individual_fonts': font_prefs.get('individual_fonts', {}),
            'create_language_selector': selector_checked or advanced_options.get('language_selector', False),
            'create_fontsize_selector': fontsize_checked or advanced_options.get('fontsize_control', False),
            'create_developer_console': console_checked,
            'create_common_file': common_checked,
            'create_screen_file': screen_checked,
            'auto_open': getattr(main_interface, 'auto_open_var', tk.BooleanVar(value=False)).get(),
            # Options avancées de screen preferences
            'advanced_screen_options': advanced_options
        }
        
        # Message de statut
        status_parts = [f"Génération pour '{language}'"]
        if common_checked:
            status_parts.append("common français")
        if screen_checked:
            status_parts.append("screens français")
        if console_checked:
            status_parts.append("console dev")
        if apply_fonts:
            status_parts.append("polices GUI")
        
        # Indiquer les options de screen preferences activées
        screen_opts = []
        if selector_checked or advanced_options.get('language_selector'):
            screen_opts.append("sélecteur langue")
        if fontsize_checked or advanced_options.get('fontsize_control'):
            screen_opts.append("contrôle taille")
        if advanced_options.get('textbox_opacity'):
            screen_opts.append("opacité textbox")
        if advanced_options.get('textbox_offset'):
            screen_opts.append("offset textbox")
        if advanced_options.get('textbox_outline'):
            screen_opts.append("contour texte")
        
        if screen_opts:
            status_parts.append(", ".join(screen_opts))
        
        status_msg = " + ".join(status_parts) + "..."
        main_interface._update_status(status_msg)
        
        # Lancer la génération
        translation_business = main_interface._get_translation_business()
        translation_business.generate_translations_embedded_threaded(
            main_interface.current_project_path,
            language,
            options,
            progress_callback=main_interface._on_progress_update,
            status_callback=main_interface._update_status,
            completion_callback=main_interface._on_operation_complete
        )
        
        main_interface._set_operation_running(True)
        log_message("INFO", f"Génération avec options cochées : {status_msg}", category="renpy_generator_tl")

    except Exception as e:
        main_interface._show_notification(f"Erreur génération avec options : {e}", "error")
        main_interface._set_operation_running(False)
        log_message("ERREUR", f"Erreur start_generation_with_checked_options : {e}", category="renpy_generator_tl")

def apply_fonts_only(main_interface):
    """Applique SEULEMENT les polices GUI sans générer de traductions"""
    try:
        if not validate_project(main_interface):
            return
        
        language = main_interface.language_var.get().strip().lower()
        if not language:
            main_interface._update_status("Veuillez spécifier une langue cible.")
            return
        
        # Vérifier qu'au moins une police GUI est sélectionnée
        enabled_fonts = get_enabled_fonts_info(main_interface)
        if not enabled_fonts:
            main_interface._update_status("Veuillez sélectionner au moins une police GUI à appliquer.")
            return
        
        # Vérifier que le dossier de langue existe
        game_dir = os.path.join(main_interface.current_project_path, "game")
        tl_folder = os.path.join(game_dir, "tl", language)
        
        if not os.path.exists(tl_folder):
            main_interface._update_status(f"Le dossier tl/{language} n'existe pas. Générez d'abord les traductions.")
            return
        
        # Griser les boutons pendant l'opération
        set_operation_buttons_state(main_interface, 'disabled')
        main_interface._update_status("Application des polices...")
        
        translation_business = main_interface._get_translation_business()
        
        # Construire les options de police
        prefs = config_manager.get_font_preferences()
        font_options = {
            'individual_fonts': prefs.get('individual_fonts', {})
        }
        
        # Appliquer SEULEMENT les polices
        font_success, font_info = translation_business.create_individual_font_system_file(
            main_interface.current_project_path, 
            language, 
            font_options
        )
        
        if font_success:
            main_interface._update_status(f"✓ Polices appliquées avec succès")
            log_message("INFO", f"Polices appliquées : {font_info}", category="renpy_generator_tl")
            
            # 🆕 NETTOYAGE : Garder seulement les polices utilisées
            try:
                font_manager = _get_font_manager()
                used_font_names = set(info['name'] for info in enabled_fonts.values())
                font_manager.cleanup_unused_temporary_fonts(used_font_names)
            except Exception as e_cleanup:
                log_message("DEBUG", f"Erreur nettoyage après application: {e_cleanup}", category="renpy_generator_tl")
        else:
            main_interface._update_status(f"✗ Échec application polices : {font_info}")
            log_message("ATTENTION", f"Échec polices : {font_info}", category="renpy_generator_tl")
            
    except Exception as e:
        main_interface._update_status(f"✗ Erreur polices : {e}")
        log_message("ERREUR", f"Erreur apply_fonts_only : {e}", category="renpy_generator_tl")
    finally:
        # Toujours réactiver les boutons à la fin
        set_operation_buttons_state(main_interface, 'normal')

def create_screen_preferences_only(main_interface):
    """
    Crée uniquement le fichier screen preferences (99_Z_ScreenPreferences.rpy)
    en utilisant les options configurées, SANS générer les traductions
    """
    try:
        # Vérifications préalables
        if not main_interface.current_project_path:
            main_interface._update_status("Veuillez sélectionner un projet Ren'Py")
            return
        
        language = main_interface.language_var.get().strip().lower()
        if not language:
            main_interface._update_status("Veuillez spécifier une langue cible.")
            return
        
        # Récupérer les options configurées depuis config_manager (nouveau système unifié)
        advanced_options = config_manager.get_advanced_screen_options()
        
        # Vérifier qu'au moins une option est activée
        if not any(advanced_options.values()):
            main_interface._update_status("⚠️ Aucune option screen preferences activée - Configurez d'abord les options via le bouton '⚙️ Options Avancées'")
            log_message("ATTENTION", "Tentative de création screen preferences sans options activées", category="renpy_generator_tl")
            return
        
        # Griser les boutons pendant l'opération
        set_operation_buttons_state(main_interface, 'disabled')
        main_interface._update_status("Création du fichier screen preferences...")
        
        # Obtenir le business
        translation_business = main_interface._get_translation_business()
        
        # Générer le fichier screen preferences
        success, message = translation_business.generate_advanced_screen_preferences(
            main_interface.current_project_path,
            language,
            advanced_options
        )
        
        if success:
            main_interface._update_status(f"✓ Screen preferences créé avec succès")
            log_message("INFO", f"Screen preferences créé : {message}", category="renpy_generator_tl")
        else:
            main_interface._update_status(f"✗ Échec création screen preferences : {message}")
            log_message("ATTENTION", f"Échec screen preferences : {message}", category="renpy_generator_tl")
            
    except Exception as e:
        main_interface._update_status(f"✗ Erreur création screen preferences : {e}")
        log_message("ERREUR", f"Erreur création screen preferences seul : {e}", category="renpy_generator_tl")
        import traceback
        traceback.print_exc()
    finally:
        # Toujours réactiver les boutons à la fin
        set_operation_buttons_state(main_interface, 'normal')

def create_developer_console_only(main_interface):
    """Crée/écrase uniquement la console développeur sans génération"""
    try:
        if not main_interface.current_project_path:
            main_interface._update_status("Veuillez sélectionner un projet Ren'Py")
            return

        language = main_interface.language_var.get().strip().lower()
        if not language:
            main_interface._update_status("Veuillez spécifier une langue cible.")
            return

        # Griser les boutons pendant l'opération
        set_operation_buttons_state(main_interface, 'disabled')
        main_interface._update_status("Création de la console développeur...")

        translation_business = main_interface._get_translation_business()
        success, message = translation_business.create_developer_console_file(
            main_interface.current_project_path,
            language
        )

        if success:
            main_interface._update_status(f"✓ Console développeur créée avec succès")
            log_message("INFO", f"Console : {message}", category="renpy_generator_tl")
        else:
            main_interface._update_status(f"✗ Échec création console : {message}")
            log_message("ATTENTION", f"Console : {message}", category="renpy_generator_tl")

    except Exception as e:
        main_interface._update_status(f"✗ Erreur console : {e}")
        log_message("ERREUR", f"Erreur création console dev seule : {e}", category="renpy_generator_tl")
    finally:
        # Toujours réactiver les boutons à la fin
        set_operation_buttons_state(main_interface, 'normal')

def save_fontsize_selector_preference(main_interface):
    """Sauvegarde la préférence du contrôle de taille de police"""
    try:
        enabled = main_interface.fontsize_selector_var.get()
        config_manager.set_fontsize_selector_integration(enabled)
        log_message("DEBUG", f"Contrôle taille police: {'activé' if enabled else 'désactivé'}", category="renpy_generator_tl")
    except Exception as e:
        log_message("ERREUR", f"Erreur sauvegarde contrôle taille : {e}", category="renpy_generator_tl")

def reset_generation_options_ui(main_interface):
    """Restaure les valeurs par défaut de l'onglet Génération"""
    try:
        defaults = config_manager.reset_generation_options_to_defaults()

        # Langue par défaut
        if "renpy_default_language" in defaults:
            main_interface.language_var.set(defaults["renpy_default_language"])

        # Recharger les préférences de polices (efface les polices personnalisées)
        if hasattr(main_interface, 'custom_fonts'):
            delattr(main_interface, 'custom_fonts')
        
        load_font_preferences(main_interface)

        # Checkboxes - FORCER les valeurs par défaut
        main_interface.language_selector_var.set(False)
        main_interface.developer_console_var.set(False)
        main_interface.add_common_var.set(False)
        main_interface.add_screen_var.set(False)
        main_interface.fontsize_selector_var.set(False)
        
        # Sauvegarder ces nouvelles valeurs
        config_manager.set_language_selector_integration(False)
        config_manager.set_developer_console_integration(False)
        config_manager.set_add_common_integration(False)
        config_manager.set_add_screen_integration(False)
        config_manager.set_fontsize_selector_integration(False)

        # Notification
        main_interface._show_notification("Options réinitialisées aux valeurs par défaut", "info")

    except Exception as e:
        main_interface._show_notification(f"Erreur réinitialisation : {e}", "error")
        log_message("ERREUR", f"Erreur reset_generation_options_ui : {e}", category="renpy_generator_tl")

def validate_project(main_interface):
    """Valide que le projet est sélectionné et valide avec popup d'erreur détaillée"""
    if not main_interface.current_project_path:
        show_translated_messagebox(
            'warning',
            'Projet requis',
            'Veuillez sélectionner un projet Ren\'Py valide avant de continuer.\n\n' +
            'Utilisez le bouton "📁 Parcourir" ou glissez-déposez un dossier de projet.',
            parent=main_interface.window
        )
        return False
    
    if not os.path.exists(main_interface.current_project_path):
        show_translated_messagebox(
            'error',
            'Projet introuvable',
            f'Le projet sélectionné n\'existe plus :\n\n{main_interface.current_project_path}\n\n' +
            'Veuillez sélectionner un projet existant.',
            parent=main_interface.window
        )
        return False
    
    game_folder = os.path.join(main_interface.current_project_path, "game")
    if not os.path.exists(game_folder):
        show_translated_messagebox(
            'error',
            'Structure de projet invalide',
            f'Le projet sélectionné ne contient pas de dossier "game" :\n\n{main_interface.current_project_path}\n\n' +
            'Assurez-vous que c\'est bien un projet Ren\'Py valide.',
            parent=main_interface.window
        )
        return False
    
    # Vérification de l'exécutable avec détails d'erreur
    translation_business = main_interface._get_translation_business()
    executable = translation_business.detect_game_executable(main_interface.current_project_path)
    if not executable:
        show_translated_messagebox(
            'warning',
            'Exécutable non détecté',
            'Aucun exécutable de jeu n\'a été détecté dans le projet.\n\n' +
            'Fichiers recherchés : .exe, .py, .sh, .app\n\n' +
            'Le projet pourrait fonctionner mais vérifiez qu\'il s\'agit bien d\'un projet Ren\'Py complet.\n\n' +
            'Voulez-vous continuer malgré tout ?',
            parent=main_interface.window
        )
        # Retourner True pour permettre de continuer même sans exécutable
        return True
    else:
        log_message("INFO", f"Exécutable détecté : {os.path.basename(executable)}", category="renpy_generator_tl")
    
    return True

def show_language_help(parent_window):
    """Affiche une aide simplifiée pour les codes de langues."""
    
    message_styled = [
        ("LANGUE CIBLE\n\n", "bold_blue"),
        ("Spécifiez le nom de votre langue de traduction.\n\n", "normal"),

        ("Conseils :\n", "bold_green"),
        ("• Utilisez des noms simples en minuscules\n", "normal"),
        ("• Évitez les espaces et caractères spéciaux\n", "normal"),
        ("• Ce nom créera le dossier dans game/tl/\n\n", "normal"),
    ]

    try:
        from ui.themes import theme_manager
        from infrastructure.helpers.unified_functions import show_custom_messagebox
        
        show_custom_messagebox(
            'info',
            'Aide - Langue cible',
            message_styled,
            theme_manager.get_theme(),
            parent=parent_window
        )
    except Exception as e:
        log_message("ERREUR", f"Erreur affichage aide langues : {e}", category="renpy_generator_tl")

def open_advanced_screen_options(main_interface):
    """Ouvre la fenêtre modale des options avancées screen preferences"""
    try:
        from ui.dialogs.advanced_screen_options_dialog import show_advanced_screen_options
        
        # Ouvrir la modale
        result = show_advanced_screen_options(main_interface.window)
        
        if result:
            # Les préférences sont déjà sauvegardées dans la modale
            log_message("INFO", f"Options screen preferences configurées: {result}", category="generation_tl_tab")
            
            # Simple notification de status (pas de popup)
            main_interface._update_status("✓ Options screen preferences configurées avec succès")
        else:
            log_message("DEBUG", "Configuration des options screen preferences annulée", category="generation_tl_tab")
            main_interface._update_status("Configuration des options annulée")
            
    except Exception as e:
        log_message("ERREUR", f"Erreur ouverture options avancées: {e}", category="generation_tl_tab")
        main_interface._update_status(f"✗ Erreur: {e}")


def show_advanced_screen_options_help(parent_window):
    """Affiche l'aide pour les options avancées screen preferences"""
    
    message_styled = [
        ("OPTIONS SCREEN PREFERENCES\n\n", "bold_blue"),
        ("Configure les fonctionnalités avancées du menu Préférences.\n\n", "normal"),
        ("Fonctionnalités disponibles :\n", "bold_green"),
        ("• Sélecteur de langue\n", "normal"),
        ("• Contrôle de taille du texte (intelligent)\n", "normal"),
        ("• Opacité de la boîte de dialogue\n", "normal"),
        ("• Décalage vertical du dialogue\n", "normal"),
        ("• Contour du texte\n\n", "normal"),
        ("Avantages :\n", "bold_green"),
        ("✓ Interface simplifiée (une seule fenêtre)\n", "normal"),
        ("✓ Système modulaire (sélectionnez ce que vous voulez)\n", "normal"),
        ("✓ UN SEUL fichier généré : 99_Z_ScreenPreferences.rpy\n", "normal"),
        ("✓ Téléchargement automatique des images nécessaires\n", "normal"),
        ("✓ Validation intelligente du screen say\n\n", "normal"),
        ("Note : ", "bold_orange"),
        ("Les options textbox nécessitent un screen say standard.", "normal"),
    ]
    
    theme = theme_manager.get_theme()
    show_custom_messagebox('info', 'Aide - Options screen preferences', message_styled, theme, parent=parent_window)


def show_language_selector_help(parent_window):
    """Affiche une aide simplifiée pour le sélecteur de langue."""
    
    message_styled = [
        ("SÉLECTEUR DE LANGUE\n\n", "bold_blue"),
        ("Ajoute votre langue dans le menu Préférences du jeu.\n\n", "normal"),

        ("Fonctionnement :\n", "bold_green"),
        ("• Analyse le menu existant du jeu\n", "normal"),
        ("• Ajoute automatiquement votre langue\n", "normal"),
        ("• Le joueur peut changer de langue facilement\n\n", "normal"),

        ("Avantages :\n", "bold_green"),
        ("• Intégration automatique et transparente\n", "normal"),
        ("• Réversible (supprimez le fichier créé)\n", "normal"),
    ]

    try:
        from ui.themes import theme_manager
        from infrastructure.helpers.unified_functions import show_custom_messagebox
        
        show_custom_messagebox(
            'info',
            'Aide - Sélecteur de langue',
            message_styled,
            theme_manager.get_theme(),
            parent=parent_window
        )
    except Exception as e:
        log_message("ERREUR", f"Erreur affichage aide sélecteur : {e}", category="renpy_generator_tl")

def show_common_help(parent_window):
    """Affiche une aide simplifiée pour common.rpy français."""
    
    message_styled = [
        ("COMMON.RPY FRANÇAIS\n\n", "bold_blue"),
        ("Remplace le common.rpy par défaut par une version française pré-traduite.\n\n", "normal"),
        
        ("⚠️ ", "red"), ("Disponible uniquement pour la langue ", "normal"), ("french", "bold"), (".\n\n", "normal"),
        
        ("Contenu :\n", "bold_green"),
        ("• Menus et boutons de l'interface\n", "normal"),
        ("• Messages système et dialogues\n", "normal"),
        ("• Console développeur et préférences\n\n", "normal"),
        
        ("Fonctionnement :\n", "bold_yellow"),
        ("• Le fichier français est placé AVANT la génération\n", "normal"),
        ("• La génération peut ensuite modifier ce fichier\n", "normal"),
        ("• Remplace complètement le common.rpy par défaut\n\n", "normal"),
        
        ("ℹ️ ", "blue"), ("IMPORTANT : ", "bold_blue"), ("Si décoché, le common.rpy par défaut de Ren'Py sera utilisé.\n", "normal"),
        ("Si coché, le common.rpy français remplace le fichier par défaut.\n", "normal"),
    ]

    try:
        from ui.themes import theme_manager
        from infrastructure.helpers.unified_functions import show_custom_messagebox
        
        show_custom_messagebox(
            'info',
            'Aide - Common.rpy français',
            message_styled,
            theme_manager.get_theme(),
            parent=parent_window
        )
    except Exception as e:
        log_message("ERREUR", f"Erreur affichage aide common : {e}", category="renpy_generator_tl")

def show_screen_help(parent_window):
    """Affiche une aide simplifiée pour screen.rpy français."""
    
    message_styled = [
        ("SCREEN.RPY FRANÇAIS\n\n", "bold_blue"),
        ("Remplace le screens.rpy par défaut par une version française pré-traduite.\n\n", "normal"),
        
        ("⚠️ ", "red"), ("Disponible uniquement pour la langue ", "normal"), ("french", "bold"), (".\n\n", "normal"),
        
        ("Contenu :\n", "bold_green"),
        ("• Écrans principaux (menu, préférences, sauvegarde)\n", "normal"),
        ("• Interface de navigation française\n", "normal"),
        ("• Boutons et labels traduits\n\n", "normal"),
        
        ("Fonctionnement :\n", "bold_yellow"),
        ("• Le fichier français est placé AVANT la génération\n", "normal"),
        ("• La génération peut ensuite modifier ce fichier\n", "normal"),
        ("• Remplace complètement le screens.rpy par défaut\n\n", "normal"),
        
        ("ℹ️ ", "blue"), ("IMPORTANT : ", "bold_blue"), ("Si décoché, le screens.rpy par défaut de Ren'Py sera utilisé.\n", "normal"),
        ("Si coché, le screens.rpy français remplace le fichier par défaut.\n", "normal"),
    ]

    try:
        from ui.themes import theme_manager
        from infrastructure.helpers.unified_functions import show_custom_messagebox
        
        show_custom_messagebox(
            'info',
            'Aide - Screen.rpy français',
            message_styled,
            theme_manager.get_theme(),
            parent=parent_window
        )
    except Exception as e:
        log_message("ERREUR", f"Erreur affichage aide screen : {e}", category="renpy_generator_tl")

def show_developer_console_help(parent_window):
    """Affiche une aide simplifiée pour la console développeur."""
    
    message_styled = [
        ("CONSOLE DÉVELOPPEUR\n\n", "bold_blue"),
        ("Active la console pour exécuter des commandes dans le jeu.\n\n", "normal"),
        
        ("Fonctionnement :\n", "bold_green"),
        ("• Active automatiquement la console Ren'Py\n", "normal"),
        ("• Appuyez sur ", "normal"), ("Maj+D", "bold"), (" dans le jeu pour l'ouvrir\n", "normal"),
        ("• Disponible uniquement avec votre traduction\n", "normal"),
        ("• Désactivation simple en supprimant le fichier\n\n", "normal"),
        
        ("Avantages :\n", "bold_green"),
        ("• Activation rapide sans modifier le code source\n", "normal"),
        ("• Utile pour tester et déboguer\n", "normal"),
    ]

    try:
        from ui.themes import theme_manager
        from infrastructure.helpers.unified_functions import show_custom_messagebox
        
        show_custom_messagebox(
            'info',
            'Aide - Console développeur',
            message_styled,
            theme_manager.get_theme(),
            parent=parent_window
        )
    except Exception as e:
        log_message("ERREUR", f"Erreur affichage aide console dev : {e}", category="renpy_generator_tl")

def show_fontsize_selector_help(parent_window):
    """Affiche une aide simplifiée pour le contrôle de taille de police."""
    
    message_styled = [
        ("CONTRÔLE TAILLE POLICE\n\n", "bold_blue"),
        ("Ajoute un réglage de taille de texte intelligent.\n\n", "normal"),
        
        ("Système automatique :\n", "bold_green"),
        ("• Validation du screen say du projet\n", "normal"),
        ("• Si standard → contrôle précis (dialogue uniquement)\n", "normal"),
        ("• Si personnalisé → contrôle global (tout le texte)\n", "normal"),
        ("• Choix transparent et automatique\n\n", "normal"),
        
        ("Contrôle précis (dialogue) :\n", "bold_yellow"),
        ("• Affecte uniquement les dialogues\n", "normal"),
        ("• Barre de réglage 1-75\n", "normal"),
        ("• Noms de personnages ajustés automatiquement\n", "normal"),
        ("• Bouton de réinitialisation\n\n", "normal"),
        
        ("Contrôle global (fallback) :\n", "bold_yellow"),
        ("• Affecte tous les textes du jeu\n", "normal"),
        ("• Système Ren'Py standard\n", "normal"),
        ("• Barre 50%-150%\n", "normal"),
    ]

    try:
        from ui.themes import theme_manager
        from infrastructure.helpers.unified_functions import show_custom_messagebox
        
        show_custom_messagebox(
            'info',
            'Aide - Contrôle taille police',
            message_styled,
            theme_manager.get_theme(),
            parent=parent_window
        )
    except Exception as e:
        log_message("ERREUR", f"Erreur affichage aide contrôle taille : {e}", category="renpy_generator_tl")

def show_font_gui_help(parent_window):
    """Affiche une aide simplifiée pour les polices GUI."""
    
    message_styled = [
        ("POLICES GUI\n\n", "bold_blue"),
        ("Personnalise les polices des différents éléments du jeu.\n\n", "normal"),

        ("Éléments configurables :\n", "bold_green"),
        ("• Texte principal (dialogues)\n", "normal"),
        ("• Noms des personnages\n", "normal"),
        ("• Interface utilisateur\n", "normal"),
        ("• Boutons et choix\n\n", "normal"),

        ("Fonctionnement :\n", "bold_green"),
        ("• Cochez les éléments à modifier\n", "normal"),
        ("• Sélectionnez une police système ou ajoutez la vôtre\n", "normal"),
        ("• Testez avec l'aperçu avant d'appliquer\n\n", "normal"),

        ("Important :\n", "bold_yellow"),
        ("• Cette fonction est totalement facultative\n", "normal"),
        ("• Le jeu fonctionne parfaitement sans\n", "normal"),
    ]

    try:
        from ui.themes import theme_manager
        from infrastructure.helpers.unified_functions import show_custom_messagebox
        
        show_custom_messagebox(
            'info',
            'Aide - Polices GUI',
            message_styled,
            theme_manager.get_theme(),
            parent=parent_window
        )
    except Exception as e:
        log_message("ERREUR", f"Erreur affichage aide polices GUI : {e}", category="renpy_generator_tl")