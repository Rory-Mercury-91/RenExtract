# ui/tab_settings/application_tab.py
# Onglet Interface & Application pour l'interface settings

"""
Onglet Interface & Application
- Configuration des ouvertures automatiques
- Options d'apparence et notifications
- Configuration de l'éditeur de code
- Actions système (nettoyage, reset)
"""

import tkinter as tk
from tkinter import ttk
from ui.themes import theme_manager
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message


def create_application_tab(parent, settings_instance):
    """Crée l'onglet Interface & Application"""
    theme = theme_manager.get_theme()
    
    tab_frame = tk.Frame(parent, bg=theme["bg"])
    
    # En-tête moderne avec titre
    header_frame = tk.Frame(tab_frame, bg=theme["bg"])
    header_frame.pack(fill='x', pady=(15, 10), padx=20)
    
    # Titre descriptif
    desc_label = tk.Label(
        header_frame,
        text="Configuration de l'apparence et du comportement de l'application",
        font=('Segoe UI', 10, 'bold'),
        justify='center',
        bg=theme["bg"],
        fg=theme["accent"]
    )
    desc_label.pack(fill='x', anchor='center')
    
    # Container principal
    main_container = tk.Frame(tab_frame, bg=theme["bg"])
    main_container.pack(fill='both', expand=True, padx=20, pady=15)
    
    # === SECTION 1: Ouvertures automatiques ===
    _create_auto_open_section(main_container, settings_instance)
    
    # Séparateur invisible
    _create_separator(main_container)
    
    # === SECTION 2: Apparence et Éditeur (2 colonnes) ===
    _create_appearance_and_editor_section(main_container, settings_instance)
    
    # Séparateur invisible
    _create_separator(main_container)
    
    # === SECTION 3: Groq AI ===
    _create_groq_section(main_container, settings_instance)
    
    # Séparateur invisible
    _create_separator(main_container)
    
    # === SECTION 4: Actions système ===
    _create_system_actions_section(main_container, settings_instance)
    
    return tab_frame


def _create_separator(parent):
    """Crée un séparateur invisible"""
    separator = tk.Frame(parent, height=20, bg=parent.cget('bg'))
    separator.pack(fill='x')


def _create_auto_open_section(parent, settings_instance):
    """Crée la section Ouvertures automatiques"""
    theme = theme_manager.get_theme()
    
    # Titre de section
    title_label = tk.Label(
        parent,
        text="🚀 Ouvertures automatiques",
        font=('Segoe UI', 12, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    title_label.pack(anchor='w', pady=(0, 10))
    
    # Container pour les options en grille
    options_container = tk.Frame(parent, bg=theme["bg"])
    options_container.pack(fill='x', pady=(0, 10))
    
    # Colonne gauche
    left_column = tk.Frame(options_container, bg=theme["bg"])
    left_column.pack(side='left', fill='both', expand=True, padx=(0, 20))
    
    # Colonne droite
    right_column = tk.Frame(options_container, bg=theme["bg"])
    right_column.pack(side='right', fill='both', expand=True, padx=(20, 0))
    
    auto_options = [
        (settings_instance.auto_open_files_var, "🚀", "Ouverture automatique des fichiers"),
        (settings_instance.auto_open_folders_var, "📁", "Ouverture automatique des dossiers"),
        (settings_instance.auto_open_coherence_report_var, "📊", "Ouverture automatique du rapport de cohérence"),
        (settings_instance.show_output_path_var, "📂", "Affichage du champ de chemin de sortie")
    ]
    
    # Répartir les options sur 2 colonnes (2 par colonne)
    for i, (var, icon, text) in enumerate(auto_options):
        column = left_column if i < 2 else right_column
        
        checkbox = tk.Checkbutton(
            column,
            text=f"{icon} {text}",
            variable=var,
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"],
            selectcolor=theme["bg"],
            activebackground=theme["bg"],
            activeforeground=theme["fg"],
            anchor='w',
            command=settings_instance._on_interface_option_changed
        )
        checkbox.pack(anchor='w', pady=3)
        
        # Ajouter au cache du ThemeManager
        theme_manager._cache_widget(checkbox, 'checkbuttons')


def _update_editor_combo_values(settings_instance):
    """Met à jour les valeurs de la combobox éditeur en fonction de l'éditeur personnalisé"""
    try:
        # Obtenir le chemin de l'éditeur personnalisé depuis la variable directement
        custom_editor_path = ""
        if hasattr(settings_instance, 'custom_editor_var'):
            custom_editor_path = settings_instance.custom_editor_var.get().strip()
        
        # Fallback vers la config si la variable n'existe pas
        if not custom_editor_path:
            custom_editor_path = config_manager.get("custom_editor_path", "")
        
        if custom_editor_path and custom_editor_path.strip():
            # Extraire le nom de l'exécutable
            import os
            from ui.tab_settings.paths_tab import get_editor_name_from_path
            editor_name = get_editor_name_from_path(custom_editor_path)
            
            # Mettre à jour les valeurs de la combobox
            editor_options = ['Défaut Windows', editor_name]
            settings_instance.editor_combo['values'] = editor_options
            
            # 🔧 CORRECTIF: Vérifier si l'éditeur personnalisé est configuré ET si editor_choice_var 
            # correspond soit au nom de l'éditeur, soit s'il n'est pas "Défaut Windows"
            current_choice = settings_instance.editor_choice_var.get()
            
            # Si l'utilisateur a sélectionné l'éditeur personnalisé OU si la config dit d'utiliser un éditeur personnalisé
            if current_choice == editor_name or (current_choice != "Défaut Windows" and current_choice not in ['Défaut Windows']):
                settings_instance.editor_combo.set(editor_name)
                settings_instance.editor_choice_var.set(editor_name)
            else:
                # Par défaut, sélectionner "Défaut Windows" mais garder l'éditeur personnalisé dans la liste
                settings_instance.editor_combo.set("Défaut Windows")
        else:
            # Pas d'éditeur personnalisé, utiliser les valeurs par défaut
            editor_options = ['Défaut Windows']
            settings_instance.editor_combo['values'] = editor_options
            settings_instance.editor_combo.set("Défaut Windows")
            
    except Exception as e:
        log_message("ERREUR", f"Erreur mise à jour combobox éditeur: {e}", category="application_tab")

def _create_appearance_section(parent, settings_instance):
    theme = theme_manager.get_theme()
    
    # Titre de section
    title_label = tk.Label(
        parent,
        text="🎨 Apparence et notifications",
        font=('Segoe UI', 12, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    title_label.pack(anchor='w', pady=(0, 10))
    
    # Container pour les options
    options_container = tk.Frame(parent, bg=theme["bg"])
    options_container.pack(fill='x', pady=(0, 10))
    
    # Mode de notification
    notification_frame = tk.Frame(options_container, bg=theme["bg"])
    notification_frame.pack(fill='x', pady=(0, 10))
    
    notification_label = tk.Label(
        notification_frame,
        text="🔔 Mode de notification des résultats :",
        font=('Segoe UI', 10, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    notification_label.pack(side='left')
    
    settings_instance.notification_combo = ttk.Combobox(
        notification_frame,
        textvariable=settings_instance.notification_mode_var,
        values=['Statut seulement', 'Popups détaillés'],
        state='readonly',
        font=('Segoe UI', 9),
        width=18
    )
    settings_instance.notification_combo.pack(side='left', padx=(10, 0))
    settings_instance.notification_combo.bind('<<ComboboxSelected>>', settings_instance._on_notification_mode_changed)

    # Container pour les checkboxes
    checkboxes_container = tk.Frame(options_container, bg=theme["bg"])
    checkboxes_container.pack(fill='x')
    
    # Mode Sombre
    dark_checkbox = tk.Checkbutton(
        checkboxes_container,
        text="🌙 Mode sombre",
        variable=settings_instance.dark_mode_var,
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        selectcolor=theme["bg"],
        activebackground=theme["bg"],
        activeforeground=theme["fg"],
        anchor='w',
        command=settings_instance._on_dark_mode_changed
    )
    dark_checkbox.pack(anchor='w', pady=3)
    
    # Ajouter au cache du ThemeManager
    theme_manager._cache_widget(dark_checkbox, 'checkbuttons')
    
    # Debug Mode
    debug_checkbox = tk.Checkbutton(
        checkboxes_container,
        text="🐛 Mode debug complet",
        variable=settings_instance.debug_mode_var,
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        selectcolor=theme["bg"],
        activebackground=theme["bg"],
        activeforeground=theme["fg"],
        anchor='w',
        command=settings_instance._on_debug_mode_changed
    )
    debug_checkbox.pack(anchor='w', pady=3)
    
    # Ajouter au cache du ThemeManager
    theme_manager._cache_widget(debug_checkbox, 'checkbuttons')


def _create_editor_section(parent, settings_instance):
    """Crée la section Éditeur de code"""
    theme = theme_manager.get_theme()
    
    # Titre de section
    title_label = tk.Label(
        parent,
        text="📝 Éditeur de code",
        font=('Segoe UI', 12, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    title_label.pack(anchor='w', pady=(0, 10))
    
    # Description
    desc_label = tk.Label(
        parent,
        text="Éditeur pour ouvrir les fichiers depuis l'interface temps réel et les rapports HTML.",
        font=('Segoe UI', 9),
        bg=theme["bg"],
        fg=theme["fg"],
        wraplength=600,
        justify='left'
    )
    desc_label.pack(anchor='w', pady=(0, 10))
    
    # Sélection d'éditeur
    editor_selection_frame = tk.Frame(parent, bg=theme["bg"])
    editor_selection_frame.pack(fill='x', pady=(0, 10))
    
    editor_label = tk.Label(
        editor_selection_frame,
        text="📝 Éditeur :",
        font=('Segoe UI', 10, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    editor_label.pack(side='left')
    
    editor_options = ['Défaut Windows']  # Valeurs initiales, seront mises à jour
    settings_instance.editor_combo = ttk.Combobox(
        editor_selection_frame,
        textvariable=settings_instance.editor_choice_var,
        values=editor_options,
        state='readonly',
        font=('Segoe UI', 9),
        width=18
    )
    settings_instance.editor_combo.pack(side='left', padx=(10, 0))
    settings_instance.editor_combo.bind('<<ComboboxSelected>>', settings_instance._on_editor_choice_changed)
    
    # Bouton de test de l'éditeur
    def test_current_editor():
        """Teste l'éditeur actuellement sélectionné"""
        from pathlib import Path
        
        try:
            # Créer le fichier de test dans le dossier 04_Configs
            from infrastructure.config.constants import FOLDERS
            
            config_dir = Path(FOLDERS["configs"])
            config_dir.mkdir(parents=True, exist_ok=True)
            
            test_file = config_dir / "test_editor_compatibility.rpy"
            
            # Contenu du fichier de test
            test_content = """# TEST DE COMPATIBILITÉ

# 04_Configs/test_editor_compatibility.rpy:1
translate test:

    # RenExtract "je veux la ligne 7"
    RenExtract "✅ Le test est passé ! Le curseur devrait être sur cette ligne (ligne 7)"
    
# Si votre curseur est sur la ligne 7 (celle avec le ✅), le test est réussi !
# Vous pouvez fermer ce fichier.
"""
            
            # Écrire le fichier
            test_file.write_text(test_content, encoding='utf-8')
            
            # Utiliser la fonction d'ouverture existante (la même que pour les rapports de cohérence)
            from ui.shared.editor_manager import open_file_with_editor
            
            success = open_file_with_editor(str(test_file), 7)
            
            if success:
                if hasattr(settings_instance, '_show_toast'):
                    settings_instance._show_toast(
                        "🧪 Fichier de test ouvert - Le curseur est-il ligne 7 avec ✅ ?",
                        type="info"
                    )
            else:
                if hasattr(settings_instance, '_show_toast'):
                    settings_instance._show_toast(
                        "⚠️ Fichier ouvert, mais l'éditeur ne supporte peut-être pas l'ouverture à une ligne spécifique",
                        type="warning"
                    )
                
        except Exception as e:
            log_message("ERREUR", f"Erreur test éditeur : {e}", category="application_tab")
            if hasattr(settings_instance, '_show_toast'):
                settings_instance._show_toast(f"❌ Erreur test : {str(e)[:60]}", type="error")
    
    test_editor_btn = tk.Button(
        editor_selection_frame,
        text="🧪",
        font=('Segoe UI', 9),
        bg=theme["button_utility_bg"],
        fg="#000000",
        command=test_current_editor,
        width=4,
        cursor='hand2'
    )
    test_editor_btn.pack(side='left', padx=(5, 0))
    
    # Mettre à jour les valeurs de la combobox
    _update_editor_combo_values(settings_instance)


def _create_appearance_and_editor_section(parent, settings_instance):
    """Crée une section avec Apparence & notifications et Éditeur de code côte à côte"""
    theme = theme_manager.get_theme()
    
    # Container principal pour les 2 colonnes
    two_column_frame = tk.Frame(parent, bg=theme["bg"])
    two_column_frame.pack(fill='x', pady=(0, 10))
    
    # Colonne gauche : Apparence et notifications
    left_column = tk.Frame(two_column_frame, bg=theme["bg"])
    left_column.pack(side='left', fill='both', expand=True, padx=(0, 10))
    
    # Colonne droite : Éditeur de code
    right_column = tk.Frame(two_column_frame, bg=theme["bg"])
    right_column.pack(side='right', fill='both', expand=True, padx=(10, 0))
    
    # Créer les sections dans leurs colonnes respectives
    _create_appearance_section(left_column, settings_instance)
    _create_editor_section(right_column, settings_instance)


def _create_groq_section(parent, settings_instance):
    """Crée la section Configuration Groq AI"""
    theme = theme_manager.get_theme()
    
    # Titre de section
    title_label = tk.Label(
        parent,
        text="🤖 Groq AI (Traducteur IA Gratuit)",
        font=('Segoe UI', 12, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    title_label.pack(anchor='w', pady=(0, 10))
    
    # Container pour les contrôles Groq
    groq_frame = tk.Frame(parent, bg=theme["bg"])
    groq_frame.pack(fill='x', pady=(0, 10))
    
    # Label et champ pour la clé API
    api_key_frame = tk.Frame(groq_frame, bg=theme["bg"])
    api_key_frame.pack(fill='x', pady=(0, 10))
    
    api_key_label = tk.Label(
        api_key_frame,
        text="Clé API Groq :",
        font=('Segoe UI', 10),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    api_key_label.pack(side='left')
    
    settings_instance.groq_api_key_entry = tk.Entry(
        api_key_frame,
        font=('Segoe UI', 10),
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        insertbackground=theme["entry_fg"],
        width=40,
        show="*"  # Masquer la clé API pour la sécurité
    )
    settings_instance.groq_api_key_entry.pack(side='left', padx=(10, 0))
    
    # Bouton pour afficher/masquer la clé
    def toggle_api_key_visibility():
        if settings_instance.groq_api_key_entry['show'] == "*":
            settings_instance.groq_api_key_entry['show'] = ""
            toggle_btn['text'] = "👁️"
        else:
            settings_instance.groq_api_key_entry['show'] = "*"
            toggle_btn['text'] = "👁️‍🗨️"
    
    toggle_btn = tk.Button(
        api_key_frame,
        text="👁️‍🗨️",
        font=('Segoe UI', 9),
        bg=theme["button_bg"],
        fg=theme["button_fg"],
        activebackground=theme["button_secondary_bg"],
        activeforeground=theme["button_fg"],
        command=toggle_api_key_visibility,
        width=3
    )
    toggle_btn.pack(side='left', padx=(5, 0))
    
    # Bouton de test de la clé API
    def test_groq_api_key():
        """Teste la validité de la clé API Groq avec un prompt simple"""
        import threading
        
        api_key = settings_instance.groq_api_key_entry.get().strip()
        
        if not api_key:
            # Utiliser la méthode _show_toast de settings_instance
            if hasattr(settings_instance, '_show_toast'):
                settings_instance._show_toast("⚠️ Veuillez entrer une clé API Groq avant de tester.", type="warning")
            return
        
        # Désactiver le bouton pendant le test
        test_btn['state'] = 'disabled'
        test_btn['text'] = "⏳ Test..."
        test_btn.update_idletasks()
        
        def run_test():
            try:
                from groq import Groq
                
                # Initialiser le client Groq avec la clé fournie
                client = Groq(api_key=api_key)
                
                # Envoyer un prompt de test simple
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Tu es un assistant de test. Réponds uniquement 'OK' si tu reçois ce message."},
                        {"role": "user", "content": "Test de connexion"}
                    ],
                    temperature=0.1,
                    max_tokens=10
                )
                
                # Vérifier la réponse
                if response and response.choices:
                    result_text = response.choices[0].message.content.strip()
                    
                    # Réactiver le bouton et afficher le succès
                    def show_success():
                        test_btn.config(state='normal', text="🔍 Tester")
                        if hasattr(settings_instance, '_show_toast'):
                            settings_instance._show_toast(
                                f"✅ Groq AI opérationnel - Réponse : {result_text}",
                                type="success"
                            )
                    
                    test_btn.after(0, show_success)
                    log_message("INFO", f"Test API Groq réussi - Réponse: {result_text}", category="settings")
                else:
                    raise Exception("Réponse vide du serveur")
                    
            except ImportError:
                def show_import_error():
                    test_btn.config(state='normal', text="🔍 Tester")
                    if hasattr(settings_instance, '_show_toast'):
                        settings_instance._show_toast(
                            "❌ Module 'groq' non installé - Utilisez : pip install groq",
                            type="error"
                        )
                
                test_btn.after(0, show_import_error)
                log_message("ERREUR", "Module groq non installé", category="settings")
                
            except Exception as e:
                error_msg = str(e)
                
                # Messages d'erreur personnalisés selon le type
                if "401" in error_msg or "invalid" in error_msg.lower():
                    toast_msg = "❌ Clé API invalide ou expirée - Vérifiez sur console.groq.com"
                elif "403" in error_msg or "denied" in error_msg.lower():
                    toast_msg = "❌ Accès refusé - Désactivez votre VPN et réessayez"
                elif "429" in error_msg or "rate" in error_msg.lower():
                    toast_msg = "⚠️ Limite de requêtes atteinte - Réessayez dans quelques instants"
                elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                    toast_msg = "❌ Erreur réseau - Vérifiez votre connexion Internet"
                else:
                    toast_msg = f"❌ Test échoué : {error_msg[:80]}"
                
                def show_error():
                    test_btn.config(state='normal', text="🔍 Tester")
                    if hasattr(settings_instance, '_show_toast'):
                        settings_instance._show_toast(toast_msg, type="error")
                
                test_btn.after(0, show_error)
                log_message("ERREUR", f"Test API Groq échoué : {error_msg}", category="settings")
        
        # Lancer le test dans un thread séparé pour ne pas bloquer l'interface
        threading.Thread(target=run_test, daemon=True).start()
    
    test_btn = tk.Button(
        api_key_frame,
        text="🔍 Tester",
        font=('Segoe UI', 9),
        bg=theme["accent"],
        fg=theme["button_fg"],
        activebackground=theme["select_bg"],
        activeforeground=theme["button_fg"],
        command=test_groq_api_key,
        width=8
    )
    test_btn.pack(side='left', padx=(5, 0))
    
    # Avertissement clé API
    warning_frame = tk.Frame(groq_frame, bg=theme["bg"])
    warning_frame.pack(fill='x', pady=(5, 0))
    
    warning_label = tk.Label(
        warning_frame,
        text="⚠️ La clé API n'est affichée qu'UNE FOIS lors de sa création. Gardez-en une copie de secours !",
        font=('Segoe UI', 8, 'bold'),
        bg=theme["bg"],
        fg="#ff6b6b",
        justify='left',
        wraplength=500
    )
    warning_label.pack(anchor='w')
    
    # Bouton d'aide
    def show_groq_help():
        from infrastructure.helpers.unified_functions import show_custom_messagebox
        
        help_title = "🤖 Comment obtenir une clé API Groq"
        
        # Contenu d'aide avec formatage
        help_content = [
            ("🔑 Étapes pour obtenir votre clé API Groq :\n\n", "bold"),
            ("1. 🌐 Allez sur ", "normal"),
            ("https://console.groq.com", "bold_blue"),
            ("\n2. 📝 Créez un compte gratuit (email + mot de passe)\n3. ✅ Vérifiez votre email si demandé\n4. 🔑 Allez dans ", "normal"),
            ("\"API Keys\"", "bold"),
            (" dans le menu\n5. ➕ Cliquez sur ", "normal"),
            ("\"Create API Key\"", "bold"),
            ("\n6. 📋 Copiez votre clé API (commence par ", "normal"),
            ("gsk_...", "bold_green"),
            (")\n\n", "normal"),
            ("🚨 ATTENTION CRITIQUE :\n", "bold_red"),
            ("• ", "normal"),
            ("La clé API n'est affichée qu'UNE SEULE FOIS lors de sa création\n", "bold_red"),
            ("• ", "normal"),
            ("Groq ne la réaffichera JAMAIS, même si vous la perdez\n", "bold_red"),
            ("• ", "normal"),
            ("Sauvegardez-la IMMÉDIATEMENT dans un gestionnaire de mots de passe\n", "bold_red"),
            ("• Si vous perdez votre clé : créez-en une nouvelle (supprimez l'ancienne)\n\n", "normal"),
            ("7. 🔒 Collez votre clé dans le champ ci-dessus\n8. 💾 Gardez une copie de secours de votre clé dans un endroit sûr\n\n", "normal"),
            ("✨ Fonctionnement de Groq AI :\n", "bold_green"),
            ("• Modèle utilisé : ", "normal"),
            ("llama-3.3-70b-versatile\n", "bold_blue"),
            ("• Qualité IA supérieure pour la contextualisation\n", "normal"),
            ("• Préservation automatique des balises Ren'Py ({i}, [p], etc.)\n", "normal"),
            ("• Remplissage automatique de la zone VF (pas de copier-coller)\n", "normal"),
            ("• Suppression automatique des notes explicatives de l'IA\n", "normal"),
            ("• Parfait pour améliorer des traductions existantes\n\n", "normal"),
            ("📊 Limites quotidiennes (gratuites) :\n", "bold_green"),
            ("• ", "normal"),
            ("30 requêtes par minute", "bold"),
            (" (RPM)\n", "normal"),
            ("• ", "normal"),
            ("14,400 requêtes par jour", "bold"),
            (" (RPD)\n", "normal"),
            ("• ", "normal"),
            ("75,000 mots par jour", "bold"),
            (" ≈ 1 roman Harry Potter\n", "normal"),
            ("• 💡 Ces limites sont ", "normal"),
            ("largement suffisantes", "bold_green"),
            (" pour la relecture/amélioration\n\n", "normal"),
            ("⚠️ Recommandations importantes :\n", "bold_yellow"),
            ("• ", "normal"),
            ("Désactivez votre VPN avant d'utiliser Groq AI\n", "bold_red"),
            ("• Si VPN actif : erreur \"Access denied. Please check your network settings.\"\n", "normal"),
            ("• Groq bloque certains VPN/proxies pour des raisons de sécurité\n\n", "normal"),
            ("🔒 Sécurité :\n", "bold_blue"),
            ("• Votre clé API est stockée localement en clair\n", "normal"),
            ("• Elle n'est jamais envoyée à d'autres services que Groq\n", "normal"),
            ("• Vous pouvez la masquer/afficher avec l'icône œil\n\n", "normal"),
            ("🔄 Fallback automatique :\n", "bold_blue"),
            ("• Si pas de clé API : ouvre le playground web Groq\n", "normal"),
            ("• Si erreur API : retour automatique au playground", "normal")
        ]
        
        show_custom_messagebox(
            type_="info",
            title=help_title,
            message=help_content,
            theme=theme,
            parent=settings_instance.winfo_toplevel() if hasattr(settings_instance, 'winfo_toplevel') else None
        )
    
    help_btn = tk.Button(
        groq_frame,
        text="❓ Comment obtenir une clé API ?",
        font=('Segoe UI', 9),
        bg=theme["button_help_bg"],
        fg=theme["button_help_fg"],
        activebackground=theme["button_help_bg"],
        activeforeground=theme["button_fg"],
        command=show_groq_help,
        cursor="hand2"
    )
    help_btn.pack(anchor='e', pady=(10, 0))
    
    # Charger la valeur actuelle
    current_api_key = config_manager.get('groq_api_key', '')
    log_message("DEBUG", f"Chargement clé API Groq: {'***' + current_api_key[-4:] if current_api_key else 'VIDE'} (longueur: {len(current_api_key)})", category="settings")
    settings_instance.groq_api_key_entry.insert(0, current_api_key)
    log_message("DEBUG", f"Clé API Groq insérée dans l'Entry (visible: {settings_instance.groq_api_key_entry.get()})", category="settings")
    
    # Bind pour sauvegarder automatiquement
    def on_api_key_changed(event=None):
        api_key = settings_instance.groq_api_key_entry.get().strip()
        log_message("DEBUG", f"on_api_key_changed appelé - Nouvelle valeur: {'***' + api_key[-4:] if api_key else 'VIDE'} (longueur: {len(api_key)})", category="settings")
        config_manager.set('groq_api_key', api_key)
        config_manager.save_config()
        log_message("INFO", f"Clé API Groq mise à jour: {'***' + api_key[-4:] if api_key else 'Vide'}", category="settings")
    
    settings_instance.groq_api_key_entry.bind('<KeyRelease>', on_api_key_changed)
    settings_instance.groq_api_key_entry.bind('<FocusOut>', on_api_key_changed)


def _create_system_actions_section(parent, settings_instance):
    """Crée la section Actions système"""
    theme = theme_manager.get_theme()
    
    # Titre de section
    title_label = tk.Label(
        parent,
        text="🔧 Actions système",
        font=('Segoe UI', 12, 'bold'),
        bg=theme["bg"],
        fg=theme["fg"]
    )
    title_label.pack(anchor='w', pady=(0, 10))
    
    # Container pour les boutons
    buttons_container = tk.Frame(parent, bg=theme["bg"])
    buttons_container.pack(fill='x')

    clean_temp_btn = tk.Button(
        buttons_container,
        text="🧹 Nettoyer les fichiers temporaires",
        command=settings_instance._clean_temp_only,
        bg=theme["button_powerful_bg"],
        fg="#000000",
        font=('Segoe UI', 11, 'bold'),
        pady=8,
        width=35
    )
    clean_temp_btn.pack(side='left', padx=(0, 10))

    reset_btn = tk.Button(
        buttons_container,
        text="🔄 Réinitialiser l'application",
        command=settings_instance._reset_application,
        bg=theme["button_danger_bg"],
        fg="#000000",
        font=('Segoe UI', 11, 'bold'),
        pady=8,
        width=35
    )
    reset_btn.pack(side='left', padx=(0, 10))