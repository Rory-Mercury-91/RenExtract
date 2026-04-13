# ui/tab_settings/paths_tab.py
# Onglet Chemins d'accès pour l'interface settings

"""
Onglet Chemins d'accès
- Configuration du SDK Ren'Py
- Configuration des éditeurs de code personnalisés
- Test et validation des chemins
- Reset des configurations
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
from ui.themes import theme_manager
from infrastructure.config.config import config_manager
from infrastructure.config.constants import FOLDERS
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import show_custom_messagebox


def get_editor_name_from_path(editor_path):
    """
    Extrait le nom de l'éditeur à partir du chemin de l'exécutable.
    
    Args:
        editor_path (str): Chemin vers l'exécutable de l'éditeur
        
    Returns:
        str: Nom de l'éditeur ou "Éditeur personnalisé" si non reconnu
    """
    if not editor_path or not os.path.exists(editor_path):
        return "Éditeur par défaut"
    
    # Extraire le nom du fichier sans extension
    exe_name = os.path.basename(editor_path).lower()
    
    # Mapping des noms d'exécutables vers les noms d'éditeurs
    editor_mapping = {
        'code.exe': 'Visual Studio Code',
        'code': 'Visual Studio Code',
        'sublime_text.exe': 'Sublime Text',
        'sublime_text': 'Sublime Text',
        'notepad++.exe': 'Notepad++',
        'notepad++': 'Notepad++',
        'atom.exe': 'Atom',
        'atom': 'Atom',
        'pulsar.exe': 'Pulsar',
        'pulsar': 'Pulsar',
        'pycharm64.exe': 'PyCharm',
        'pycharm.exe': 'PyCharm',
        'pycharm': 'PyCharm',
        'idea64.exe': 'IntelliJ IDEA',
        'idea.exe': 'IntelliJ IDEA',
        'idea': 'IntelliJ IDEA',
        'vim.exe': 'Vim',
        'vim': 'Vim',
        'gvim.exe': 'GVim',
        'gvim': 'GVim',
        'nano.exe': 'Nano',
        'nano': 'Nano'
    }
    
    # Chercher une correspondance exacte
    if exe_name in editor_mapping:
        return editor_mapping[exe_name]
    
    # Chercher une correspondance partielle (pour les cas comme "code.exe" dans "code.exe")
    for exe_key, editor_name in editor_mapping.items():
        if exe_key in exe_name or exe_name in exe_key:
            return editor_name
    
    # Si aucun mapping trouvé, essayer d'extraire un nom lisible du chemin
    try:
        # Prendre le nom du dossier parent si c'est un nom d'éditeur connu
        parent_dir = os.path.basename(os.path.dirname(editor_path)).lower()
        for exe_key, editor_name in editor_mapping.items():
            if exe_key.replace('.exe', '') in parent_dir:
                return editor_name
        
        # Sinon, capitaliser le nom de l'exécutable
        clean_name = os.path.splitext(exe_name)[0].replace('_', ' ').replace('-', ' ')
        return clean_name.title()
    except:
        return "Éditeur personnalisé"


def create_paths_tab(parent, settings_instance):
    """Crée l'onglet Chemins d'accès - parent = frame scrollable (ajout au notebook fait par l'interface)."""
    theme = theme_manager.get_theme()
    
    tab_frame = tk.Frame(parent, bg=theme["bg"])
    tab_frame.pack(fill='both', expand=True)
    
    # Header avec titre centré et bouton d'aide à droite
    header_frame = tk.Frame(tab_frame, bg=theme["bg"])
    header_frame.pack(fill='x', padx=20, pady=(15, 10))
    
    # Titre descriptif centré
    desc_label = tk.Label(
        header_frame,
        text="Configuration des chemins d'accès pour le SDK Ren'Py et l'éditeur de code personnalisé",
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
        command=lambda: _show_paths_help_simple(settings_instance),
        bg=theme["button_secondary_bg"],
        fg="#000000",
        font=('Segoe UI', 10, 'bold'),
        width=15,
        height=1,
        relief='flat',
        cursor='hand2'
    )
    help_btn.pack(side='right', anchor='e')
    
    # Container principal
    main_container = tk.Frame(tab_frame, bg=theme["bg"])
    main_container.pack(fill='both', expand=True, padx=20, pady=(0, 15))
    
    # === SECTION 1: SDK Ren'Py ===
    _create_sdk_section(main_container, settings_instance)
    
    # Séparateur invisible
    _create_separator(main_container)
    
    # === SECTION 2: Éditeur personnalisé ===
    _create_custom_editor_section(main_container, settings_instance)
    
    _create_separator(main_container)


def _create_separator(parent):
    """Crée un séparateur invisible"""
    separator = tk.Frame(parent, height=20, bg=parent.cget('bg'))
    separator.pack(fill='x')


def _create_sdk_section(parent, settings_instance):
    """Crée la section SDK Ren'Py"""
    theme = theme_manager.get_theme()
    
    # Frame de section
    sdk_frame = tk.Frame(parent, bg=theme["bg"])
    sdk_frame.pack(fill='x', pady=(0, 20))
    
    # Titre de section
    title_label = tk.Label(
        sdk_frame,
        text="🛠️ SDK Ren'Py",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["accent"]
    )
    title_label.pack(anchor='w', pady=(0, 10))
    
    # Description
    desc_label = tk.Label(
        sdk_frame,
        text="Chemin vers le SDK Ren'Py (dossier contenant renpy.exe) :",
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    desc_label.pack(anchor='w', pady=(0, 10))
    
    # Container pour le champ et boutons
    input_container = tk.Frame(sdk_frame, bg=theme["bg"])
    input_container.pack(fill='x', pady=(0, 10))
    
    # Champ de saisie
    settings_instance.sdk_path_entry = tk.Entry(
        input_container,
        textvariable=settings_instance.sdk_path_var,
        font=('Segoe UI', 10),
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        insertbackground=theme["entry_fg"],
        relief='solid',
        borderwidth=1
    )
    settings_instance.sdk_path_entry.pack(side='left', fill='x', expand=True, pady=2, ipady=4)
    
    # Bouton Parcourir
    browse_sdk_btn = tk.Button(
        input_container,
        text="📁 Parcourir",
        command=lambda: _browse_sdk_path_simple(settings_instance),
        bg=theme["button_nav_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=6,
        width=15,
        relief='flat',
        cursor='hand2'
    )
    browse_sdk_btn.pack(side='right', padx=(10, 0))


def _create_custom_editor_section(parent, settings_instance):
    """Crée la section Éditeur personnalisé"""
    theme = theme_manager.get_theme()
    
    # Frame de section
    editor_frame = tk.Frame(parent, bg=theme["bg"])
    editor_frame.pack(fill='x', pady=(0, 20))
    
    # Titre de section
    title_label = tk.Label(
        editor_frame,
        text="📝 Éditeur de code personnalisé",
        font=('Segoe UI', 11, 'bold'),
        bg=theme["bg"],
        fg=theme["accent"]
    )
    title_label.pack(anchor='w', pady=(0, 10))
    
    # Description
    desc_label = tk.Label(
        editor_frame,
        text="Chemin vers votre éditeur de code préféré (optionnel) :",
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    desc_label.pack(anchor='w', pady=(0, 10))
    
    # Container pour le champ et boutons
    input_container = tk.Frame(editor_frame, bg=theme["bg"])
    input_container.pack(fill='x', pady=(0, 10))
    
    # 🔧 CORRECTIF: Ne pas écraser custom_editor_var si elle existe déjà (initialisée dans _init_all_variables)
    if not hasattr(settings_instance, 'custom_editor_var') or settings_instance.custom_editor_var is None:
        settings_instance.custom_editor_var = tk.StringVar()
        # Charger la valeur depuis la config si disponible
        custom_editor_path = config_manager.get('custom_editor_path', '')
        if custom_editor_path:
            settings_instance.custom_editor_var.set(custom_editor_path)
    
    # Champ de saisie
    settings_instance.custom_editor_entry = tk.Entry(
        input_container,
        textvariable=settings_instance.custom_editor_var,
        font=('Segoe UI', 10),
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        insertbackground=theme["entry_fg"],
        relief='solid',
        borderwidth=1
    )
    settings_instance.custom_editor_entry.pack(side='left', fill='x', expand=True, pady=2, ipady=4)
    
    # Bouton Test
    test_btn = tk.Button(
        input_container,
        text="🧪",
        command=lambda: _test_custom_editor_path(settings_instance),
        bg=theme["button_utility_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=6,
        width=4,
        relief='flat',
        cursor='hand2'
    )
    test_btn.pack(side='right', padx=(5, 0))
    
    # Bouton Parcourir
    browse_btn = tk.Button(
        input_container,
        text="📁 Parcourir",
        command=lambda: _browse_custom_editor_path(settings_instance),
        bg=theme["button_nav_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=6,
        width=15,
        relief='flat',
        cursor='hand2'
    )
    browse_btn.pack(side='right', padx=(10, 0))
    
    # Container pour les boutons d'action
    actions_container = tk.Frame(editor_frame, bg=theme["bg"])
    actions_container.pack(fill='x', pady=(10, 0))
    
    # Bouton Reset pour tous les chemins
    reset_btn = tk.Button(
        actions_container,
        text="🔄 Réinitialiser tous les chemins",
        command=lambda: _reset_all_paths(settings_instance),
        bg=theme["button_tertiary_bg"],
        fg="#000000",
        font=('Segoe UI', 9),
        pady=4,
        width=30,
        relief='flat',
        cursor='hand2'
    )
    reset_btn.pack(side='left')
    
    # Bind pour sauvegarde automatique
    settings_instance.custom_editor_entry.bind('<KeyRelease>', lambda e: _on_custom_editor_path_changed(settings_instance))


def _test_custom_editor_path(settings_instance):
    """Teste si l'éditeur peut ouvrir un fichier à une ligne spécifique"""
    import tempfile
    from pathlib import Path
    
    try:
        path = settings_instance.custom_editor_var.get().strip()
        
        if not path:
            _show_toast(settings_instance, "⚠️ Aucun chemin configuré pour l'éditeur personnalisé", "warning")
            return
        
        if not (os.path.exists(path) and os.path.isfile(path)):
            _show_toast(settings_instance, "❌ Éditeur personnalisé : Fichier non trouvé", "error")
            return
        
        # Créer le fichier de test dans le dossier 05_ConfigRenExtract de RenExtract
        from infrastructure.config.constants import FOLDERS
        
        config_dir = Path(FOLDERS["configs"])
        config_dir.mkdir(parents=True, exist_ok=True)
        
        test_file = config_dir / "test_editor_compatibility.rpy"
        
        # Contenu du fichier de test
        test_content = """# TEST DE COMPATIBILITÉ

# 05_ConfigRenExtract/test_editor_compatibility.rpy:1
translate test:

    # RenExtract "je veux la ligne 7"
    RenExtract "✅ Le test est passé ! Le curseur devrait être sur cette ligne (ligne 7)"
    
# Si votre curseur est sur la ligne 7 (celle avec le ✅), le test est réussi !
# Vous pouvez fermer ce fichier.
"""
        
        # Écrire le fichier
        test_file.write_text(test_content, encoding='utf-8')
        log_message("INFO", f"Fichier de test créé : {test_file}", category="paths_tab")
        
        # Détecter l'éditeur et construire la commande appropriée
        editor_name = get_editor_name_from_path(path)
        exe_name = os.path.basename(path).lower()
        
        # Commandes selon l'éditeur pour ouvrir à la ligne 7
        if 'code' in exe_name or 'vscode' in editor_name.lower():
            # VSCode: code --goto file.rpy:7
            cmd = [path, "--goto", f"{test_file}:7"]
        elif 'sublime' in exe_name or 'sublime' in editor_name.lower():
            # Sublime Text: sublime_text file.rpy:7
            cmd = [path, f"{test_file}:7"]
        elif 'notepad++' in exe_name:
            # Notepad++: notepad++ -n7 file.rpy
            cmd = [path, f"-n7", str(test_file)]
        elif 'atom' in exe_name or 'pulsar' in exe_name:
            # Atom/Pulsar: atom file.rpy:7
            cmd = [path, f"{test_file}:7"]
        elif 'pycharm' in exe_name or 'idea' in exe_name:
            # PyCharm/IntelliJ: idea --line 7 file.rpy
            cmd = [path, "--line", "7", str(test_file)]
        else:
            # Format générique (espérer que ça marche)
            cmd = [path, f"{test_file}:7"]
        
        # Exécuter la commande
        creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        
        subprocess.Popen(
            cmd,
            creationflags=creationflags,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        log_message("INFO", f"Test éditeur lancé : {' '.join(cmd)}", category="paths_tab")
        
        # Message de confirmation
        _show_toast(
            settings_instance, 
            f"🧪 {editor_name} : Fichier de test ouvert - Vérifiez que le curseur est sur la ligne 7 ✅", 
            "info"
        )
        
    except Exception as e:
        log_message("ERREUR", f"Erreur test ouverture éditeur : {e}", category="paths_tab")
        _show_toast(settings_instance, f"❌ Erreur test : {str(e)[:60]}", "error")


def _browse_custom_editor_path(settings_instance):
    """Ouvre un dialogue pour sélectionner l'éditeur personnalisé"""
    try:
        # Filtres pour les exécutables
        filetypes = [
            ("Exécutables", "*.exe"),
            ("Tous les fichiers", "*.*")
        ]
        
        path = filedialog.askopenfilename(
            title="Sélectionner l'éditeur de code",
            filetypes=filetypes
        )
        
        if path:
            settings_instance.custom_editor_var.set(path)
            _on_custom_editor_path_changed(settings_instance)
            
    except Exception as e:
        log_message("ERREUR", f"Erreur sélection chemin éditeur personnalisé: {e}", category="paths_tab")


def _reset_all_paths(settings_instance):
    """Réinitialise tous les chemins (SDK + Éditeur personnalisé)"""
    try:
        # Réinitialiser le SDK
        settings_instance.sdk_path_var.set("")
        config_manager.set_renpy_sdk_path("")
        
        # Réinitialiser l'éditeur personnalisé
        settings_instance.custom_editor_var.set("")
        config_manager.set("custom_editor_path", "")
        
        _show_toast(settings_instance, "🔄 Tous les chemins ont été réinitialisés", "info")
        log_message("INFO", "Tous les chemins (SDK + Éditeur) ont été réinitialisés", category="paths_tab")
        
        # Mettre à jour la combobox de l'onglet Application
        if hasattr(settings_instance, 'editor_combo'):
            from ui.tab_settings.application_tab import _update_editor_combo_values
            _update_editor_combo_values(settings_instance)
            
    except Exception as e:
        log_message("ERREUR", f"Erreur réinitialisation des chemins: {e}", category="paths_tab")


def _reset_custom_editor_path(settings_instance):
    """Remet le chemin de l'éditeur personnalisé à vide (fonction conservée pour compatibilité)"""
    try:
        settings_instance.custom_editor_var.set("")
        config_manager.set("custom_editor_path", "")
        _show_toast(settings_instance, "🔄 Chemin éditeur personnalisé réinitialisé", "info")
        log_message("INFO", "Chemin éditeur personnalisé réinitialisé", category="paths_tab")
        
        # Mettre à jour la combobox de l'onglet Application
        if hasattr(settings_instance, 'editor_combo'):
            from ui.tab_settings.application_tab import _update_editor_combo_values
            _update_editor_combo_values(settings_instance)
            
    except Exception as e:
        log_message("ERREUR", f"Erreur réinitialisation chemin éditeur personnalisé: {e}", category="paths_tab")


def _on_custom_editor_path_changed(settings_instance):
    """Appelé quand le chemin de l'éditeur personnalisé change"""
    try:
        path = settings_instance.custom_editor_var.get().strip()
        config_manager.set("custom_editor_path", path)
        log_message("INFO", f"Chemin éditeur personnalisé sauvegardé: {path}", category="paths_tab")
        
        # Mettre à jour la combobox de l'onglet Application
        if hasattr(settings_instance, 'editor_combo'):
            from ui.tab_settings.application_tab import _update_editor_combo_values
            _update_editor_combo_values(settings_instance)
            
    except Exception as e:
        log_message("ERREUR", f"Erreur changement chemin éditeur personnalisé: {e}", category="paths_tab")


def _show_toast(settings_instance, message, toast_type="info"):
    """Affiche une notification toast"""
    try:
        if hasattr(settings_instance, '_show_toast'):
            settings_instance._show_toast(message, toast_type)
        else:
            # Fallback si la méthode n'existe pas
            log_message("INFO", message, category="paths_tab")
    except Exception as e:
        log_message("ERREUR", f"Erreur affichage toast: {e}", category="paths_tab")


def _show_paths_help_simple(settings_instance):
    """Affiche l'aide pour les chemins d'accès (version colorée et formatée)"""
    try:
        help_text = [
            ("🛠️ AIDE - Chemins d'accès\n", "bold"),
            ("\n", ""),
            ("📁 SDK Ren'Py\n", "bold_green"),
            ("• Chemin vers le dossier contenant renpy.exe\n", ""),
            ("• Nécessaire pour la génération et l'extraction\n", ""),
            ("• Exemple : C:\\RenPy\\renpy-8.1.3-sdk\n", "italic"),
            ("\n", ""),
            ("✏️ Éditeur personnalisé\n", "bold_blue"),
            ("• Chemin vers votre éditeur de code préféré\n", ""),
            ("• Optionnel : utilise l'éditeur par défaut si vide\n", ""),
            ("• Le nom de l'éditeur sera détecté automatiquement\n", ""),
            ("• Exemple : C:\\Program Files\\Microsoft VS Code\\Code.exe\n", "italic"),
            ("\n", ""),
            ("🧪 Test des chemins\n", "bold_yellow"),
            ("• Vérifie que les chemins sont valides\n", ""),
            ("• Teste l'existence des fichiers/dossiers\n", ""),
            ("\n", ""),
            ("💡 Conseils\n", "bold"),
            ("• Utilisez le bouton 'Parcourir' pour naviguer facilement\n", ""),
            ("• Les chemins sont sauvegardés automatiquement\n", ""),
            ("• Vous pouvez réinitialiser à tout moment\n", "")
        ]
        
        show_custom_messagebox(
            'info',
            'Aide - Chemins d\'accès',
            help_text,
            theme_manager.get_theme(),
            parent=settings_instance.window
        )
    except Exception as e:
        log_message("ERREUR", f"Erreur affichage aide chemins: {e}", category="paths_tab")


def _browse_sdk_path_simple(settings_instance):
    """Ouvre le dialogue de sélection pour le SDK (version simple)"""
    try:
        current_path = settings_instance.sdk_path_var.get()
        initial_dir = os.path.dirname(current_path) if current_path else "C:\\"
        
        folder_path = filedialog.askdirectory(
            title="🛠️ Sélectionner le dossier SDK Ren'Py",
            initialdir=initial_dir
        )
        
        if folder_path:
            settings_instance.sdk_path_var.set(folder_path)
            config_manager.set_renpy_sdk_path(folder_path)
            _show_toast(settings_instance, "🛠️ Chemin SDK configuré", "success")
            
    except Exception as e:
        log_message("ERREUR", f"Erreur sélection chemin SDK: {e}", category="paths_tab")