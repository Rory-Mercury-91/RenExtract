# ui/interfaces/advanced_screen_options_dialog.py
# Fenêtre modale pour les options avancées de screen preferences

"""
Fenêtre modale pour configurer les options screen preferences
- Sélecteur de langue
- Contrôle de taille du texte
- Personnalisation textbox (opacité, décalage, contour)
"""

import tkinter as tk
from tkinter import ttk
from ui.themes import theme_manager
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import show_custom_messagebox

class AdvancedScreenOptionsDialog:
    """Dialogue modal pour les options screen preferences"""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = None
        self.result = None
        
        # Variables pour les checkboxes
        self.language_selector_var = tk.BooleanVar()
        self.fontsize_control_var = tk.BooleanVar()
        self.textbox_opacity_var = tk.BooleanVar()
        self.textbox_offset_var = tk.BooleanVar()
        self.textbox_outline_var = tk.BooleanVar()
        
        # Charger les préférences sauvegardées
        self._load_preferences()
    
    def _load_preferences(self):
        """Charge les préférences sauvegardées"""
        try:
            options = config_manager.get_advanced_screen_options()
            self.language_selector_var.set(options.get('language_selector', False))
            self.fontsize_control_var.set(options.get('fontsize_control', False))
            self.textbox_opacity_var.set(options.get('textbox_opacity', False))
            self.textbox_offset_var.set(options.get('textbox_offset', False))
            self.textbox_outline_var.set(options.get('textbox_outline', False))
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur chargement préférences screen options: {e}", category="screen_options")
    
    def _save_preferences(self):
        """Sauvegarde les préférences"""
        try:
            options = {
                'language_selector': self.language_selector_var.get(),
                'fontsize_control': self.fontsize_control_var.get(),
                'textbox_opacity': self.textbox_opacity_var.get(),
                'textbox_offset': self.textbox_offset_var.get(),
                'textbox_outline': self.textbox_outline_var.get()
            }
            config_manager.set_advanced_screen_options(options)
            log_message("DEBUG", "Préférences screen options sauvegardées", category="screen_options")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur sauvegarde préférences screen options: {e}", category="screen_options")
    
    def show(self) -> dict:
        """
        Affiche le dialogue modal et retourne les options sélectionnées
        
        Returns:
            dict avec les options sélectionnées ou None si annulé
        """
        self.window = tk.Toplevel(self.parent)
        self.window.title("⚙️ Options avancées - Screen Preferences")
        self.window.geometry("650x550")
        self.window.transient(self.parent)
        self.window.grab_set()
        
        theme = theme_manager.get_theme()
        self.window.configure(bg=theme["bg"])
        
        self._center_window()
        self._create_interface()
        
        # Attendre la fermeture
        self.window.wait_window()
        
        return self.result
    
    def _center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def _create_interface(self):
        """Crée l'interface du dialogue"""
        theme = theme_manager.get_theme()
        
        # En-tête
        header_frame = tk.Frame(self.window, bg=theme["bg"])
        header_frame.pack(fill='x', padx=20, pady=15)
        
        title_label = tk.Label(
            header_frame,
            text="⚙️ Options avancées - Screen Preferences",
            font=('Segoe UI', 14, 'bold'),
            bg=theme["bg"],
            fg=theme["accent"]
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Sélectionnez les fonctionnalités à intégrer dans le menu Préférences du jeu",
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Contenu principal avec scroll
        main_container = tk.Frame(self.window, bg=theme["bg"])
        main_container.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        
        # Canvas avec scrollbar
        canvas = tk.Canvas(main_container, bg=theme["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=theme["bg"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Sections d'options
        self._create_language_section(scrollable_frame, theme)
        self._create_fontsize_section(scrollable_frame, theme)
        self._create_textbox_section(scrollable_frame, theme)
        
        # Résumé
        self._create_summary_section(scrollable_frame, theme)
        
        # Boutons d'action
        self._create_action_buttons(theme)
    
    def _create_language_section(self, parent, theme):
        """Section sélecteur de langue"""
        section_frame = tk.LabelFrame(
            parent,
            text="📋 Sélecteur de langue",
            font=('Segoe UI', 10, 'bold'),
            bg=theme["bg"],
            fg=theme["fg"],
            padx=15,
            pady=10
        )
        section_frame.pack(fill='x', pady=(0, 15))
        
        option_frame = tk.Frame(section_frame, bg=theme["bg"])
        option_frame.pack(fill='x')
        
        help_btn = tk.Button(
            option_frame,
            text="?",
            command=lambda: self._show_help("language_selector"),
            bg=theme["button_help_bg"],
            fg="#000000",
            font=('Segoe UI', 9),
            pady=2,
            padx=6,
            relief='flat',
            cursor='hand2'
        )
        help_btn.pack(side='right')
        
        check = tk.Checkbutton(
            option_frame,
            text="Ajouter le sélecteur de langue dans le menu",
            variable=self.language_selector_var,
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"],
            selectcolor=theme["entry_bg"],
            command=self._update_summary
        )
        check.pack(side='left')
        
        desc_label = tk.Label(
            section_frame,
            text="Permet au joueur de changer la langue depuis le menu Préférences",
            font=('Segoe UI', 8),
            bg=theme["bg"],
            fg=theme["fg"],
            wraplength=550,
            justify='left'
        )
        desc_label.pack(anchor='w', pady=(5, 0))
    
    def _create_fontsize_section(self, parent, theme):
        """Section contrôle de taille"""
        section_frame = tk.LabelFrame(
            parent,
            text="📏 Contrôle de taille du texte",
            font=('Segoe UI', 10, 'bold'),
            bg=theme["bg"],
            fg=theme["fg"],
            padx=15,
            pady=10
        )
        section_frame.pack(fill='x', pady=(0, 15))
        
        option_frame = tk.Frame(section_frame, bg=theme["bg"])
        option_frame.pack(fill='x')
        
        help_btn = tk.Button(
            option_frame,
            text="?",
            command=lambda: self._show_help("fontsize_control"),
            bg=theme["button_help_bg"],
            fg="#000000",
            font=('Segoe UI', 9),
            pady=2,
            padx=6,
            relief='flat',
            cursor='hand2'
        )
        help_btn.pack(side='right')
        
        check = tk.Checkbutton(
            option_frame,
            text="Ajouter une barre de réglage de la taille du texte",
            variable=self.fontsize_control_var,
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"],
            selectcolor=theme["entry_bg"],
            command=self._update_summary
        )
        check.pack(side='left')
        
        desc_label = tk.Label(
            section_frame,
            text="Système intelligent : contrôle précis (dialogue) ou global selon le screen say",
            font=('Segoe UI', 8),
            bg=theme["bg"],
            fg=theme["fg"],
            wraplength=550,
            justify='left'
        )
        desc_label.pack(anchor='w', pady=(5, 0))
    
    def _create_textbox_section(self, parent, theme):
        """Section personnalisation textbox"""
        section_frame = tk.LabelFrame(
            parent,
            text="🎨 Personnalisation de la textbox",
            font=('Segoe UI', 10, 'bold'),
            bg=theme["bg"],
            fg=theme["fg"],
            padx=15,
            pady=10
        )
        section_frame.pack(fill='x', pady=(0, 15))
        
        # Option 1: Opacité
        opacity_frame = tk.Frame(section_frame, bg=theme["bg"])
        opacity_frame.pack(fill='x', pady=(0, 8))
        
        opacity_help_btn = tk.Button(
            opacity_frame,
            text="?",
            command=lambda: self._show_help("textbox_opacity"),
            bg=theme["button_help_bg"],
            fg="#000000",
            font=('Segoe UI', 9),
            pady=2,
            padx=6,
            relief='flat',
            cursor='hand2'
        )
        opacity_help_btn.pack(side='right')
        
        opacity_check = tk.Checkbutton(
            opacity_frame,
            text="Contrôle d'opacité de la boîte de dialogue (0-100%)",
            variable=self.textbox_opacity_var,
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"],
            selectcolor=theme["entry_bg"],
            command=self._update_summary
        )
        opacity_check.pack(side='left')
        
        # Option 2: Décalage vertical
        offset_frame = tk.Frame(section_frame, bg=theme["bg"])
        offset_frame.pack(fill='x', pady=(0, 8))
        
        offset_help_btn = tk.Button(
            offset_frame,
            text="?",
            command=lambda: self._show_help("textbox_offset"),
            bg=theme["button_help_bg"],
            fg="#000000",
            font=('Segoe UI', 9),
            pady=2,
            padx=6,
            relief='flat',
            cursor='hand2'
        )
        offset_help_btn.pack(side='right')
        
        offset_check = tk.Checkbutton(
            offset_frame,
            text="Contrôle du décalage vertical du dialogue",
            variable=self.textbox_offset_var,
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"],
            selectcolor=theme["entry_bg"],
            command=self._update_summary
        )
        offset_check.pack(side='left')
        
        # Option 3: Contour du texte
        outline_frame = tk.Frame(section_frame, bg=theme["bg"])
        outline_frame.pack(fill='x', pady=(0, 8))
        
        outline_help_btn = tk.Button(
            outline_frame,
            text="?",
            command=lambda: self._show_help("textbox_outline"),
            bg=theme["button_help_bg"],
            fg="#000000",
            font=('Segoe UI', 9),
            pady=2,
            padx=6,
            relief='flat',
            cursor='hand2'
        )
        outline_help_btn.pack(side='right')
        
        outline_check = tk.Checkbutton(
            outline_frame,
            text="Contrôle de l'épaisseur du contour du texte",
            variable=self.textbox_outline_var,
            font=('Segoe UI', 9),
            bg=theme["bg"],
            fg=theme["fg"],
            selectcolor=theme["entry_bg"],
            command=self._update_summary
        )
        outline_check.pack(side='left')
        
        # Info textbox
        info_label = tk.Label(
            section_frame,
            text="⚠️ Les options textbox nécessitent un screen say standard et l'image textboxHigh.png",
            font=('Segoe UI', 8),
            bg=theme["bg"],
            fg=theme["accent"],
            wraplength=550,
            justify='left'
        )
        info_label.pack(anchor='w', pady=(10, 0))
    
    def _create_summary_section(self, parent, theme):
        """Section résumé"""
        self.summary_frame = tk.Frame(parent, bg=theme["frame_bg"], relief='solid', borderwidth=1)
        self.summary_frame.pack(fill='x', pady=(15, 0), padx=5)
        
        self.summary_label = tk.Label(
            self.summary_frame,
            text="",
            font=('Segoe UI', 9, 'bold'),
            bg=theme["frame_bg"],
            fg=theme["accent"],
            padx=15,
            pady=10,
            justify='left'
        )
        self.summary_label.pack()
        
        self._update_summary()
    
    def _create_action_buttons(self, theme):
        """Boutons d'action"""
        button_frame = tk.Frame(self.window, bg=theme["bg"])
        button_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        cancel_btn = tk.Button(
            button_frame,
            text="❌ Annuler",
            command=self._on_cancel,
            bg=theme["button_danger_bg"],
            fg="#000000",
            font=('Segoe UI', 10),
            pady=6,
            padx=15,
            relief='flat',
            cursor='hand2'
        )
        cancel_btn.pack(side='left')
        
        validate_btn = tk.Button(
            button_frame,
            text="✅ Valider",
            command=self._on_validate,
            bg=theme["button_primary_bg"],
            fg="#000000",
            font=('Segoe UI', 10, 'bold'),
            pady=6,
            padx=15,
            relief='flat',
            cursor='hand2'
        )
        validate_btn.pack(side='right')
    
    def _update_summary(self):
        """Met à jour le résumé des options sélectionnées"""
        selected = []
        
        if self.language_selector_var.get():
            selected.append("Sélecteur de langue")
        if self.fontsize_control_var.get():
            selected.append("Contrôle taille")
        if self.textbox_opacity_var.get():
            selected.append("Opacité textbox")
        if self.textbox_offset_var.get():
            selected.append("Décalage vertical")
        if self.textbox_outline_var.get():
            selected.append("Contour texte")
        
        count = len(selected)
        
        if count == 0:
            summary_text = "ℹ️ Aucune option sélectionnée\nAucun fichier ne sera créé"
        else:
            summary_text = f"ℹ️ Options sélectionnées : {count}/5\n"
            summary_text += "Un fichier 99_Z_ScreenPreferences.rpy sera créé avec :\n"
            summary_text += " • " + "\n • ".join(selected)
        
        self.summary_label.config(text=summary_text)
    
    def _show_help(self, topic):
        """Affiche l'aide pour un sujet"""
        help_messages = {
            'language_selector': [
                ("SÉLECTEUR DE LANGUE\n\n", "bold_blue"),
                ("Ajoute un bouton dans le menu Préférences pour changer de langue.\n\n", "normal"),
                ("Fonctionnement :\n", "bold_green"),
                ("• Détecte automatiquement le screen preferences existant\n", "normal"),
                ("• Ajoute une vbox avec les langues disponibles\n", "normal"),
                ("• Le joueur peut basculer entre English et votre langue\n", "normal"),
            ],
            'fontsize_control': [
                ("CONTRÔLE DE TAILLE\n\n", "bold_blue"),
                ("Ajoute une barre pour régler la taille du texte.\n\n", "normal"),
                ("Système intelligent :\n", "bold_green"),
                ("• Détecte si le screen say est standard\n", "normal"),
                ("• Si standard → Contrôle précis (dialogue uniquement)\n", "normal"),
                ("• Sinon → Contrôle global (tous les textes)\n", "normal"),
            ],
            'textbox_opacity': [
                ("OPACITÉ TEXTBOX\n\n", "bold_blue"),
                ("Permet de régler la transparence de la boîte de dialogue.\n\n", "normal"),
                ("Fonctionnement :\n", "bold_green"),
                ("• Barre de 0% (invisible) à 100% (opaque)\n", "normal"),
                ("• Modifie le screen say pour utiliser l'image textboxHigh.png\n", "normal"),
                ("• L'image est téléchargée automatiquement si nécessaire\n", "normal"),
            ],
            'textbox_offset': [
                ("DÉCALAGE VERTICAL\n\n", "bold_blue"),
                ("Permet d'ajuster la position verticale du dialogue.\n\n", "normal"),
                ("Utilisation :\n", "bold_green"),
                ("• Barre de -200 à +200 pixels\n", "normal"),
                ("• Utile pour adapter à différentes résolutions\n", "normal"),
                ("• Fonctionne avec le système RenExtract\n", "normal"),
            ],
            'textbox_outline': [
                ("CONTOUR DU TEXTE\n\n", "bold_blue"),
                ("Ajoute un contour noir autour du texte pour améliorer la lisibilité.\n\n", "normal"),
                ("Paramètres :\n", "bold_green"),
                ("• Épaisseur de 0 à 10 pixels\n", "normal"),
                ("• Améliore la visibilité sur fonds clairs\n", "normal"),
                ("• Basé sur le système RenExtract\n", "normal"),
            ],
        }
        
        if topic in help_messages:
            show_custom_messagebox(
                'info',
                'Aide - Options avancées',
                help_messages[topic],
                theme_manager.get_theme(),
                parent=self.window
            )
    
    def _on_validate(self):
        """Validation des options"""
        # Sauvegarder les préférences
        self._save_preferences()
        
        # Préparer le résultat
        self.result = {
            'language_selector': self.language_selector_var.get(),
            'fontsize_control': self.fontsize_control_var.get(),
            'textbox_opacity': self.textbox_opacity_var.get(),
            'textbox_offset': self.textbox_offset_var.get(),
            'textbox_outline': self.textbox_outline_var.get()
        }
        
        self.window.destroy()
    
    def _on_cancel(self):
        """Annulation"""
        self.result = None
        self.window.destroy()


def show_advanced_screen_options(parent):
    """Fonction helper pour afficher le dialogue"""
    dialog = AdvancedScreenOptionsDialog(parent)
    return dialog.show()


# Export
__all__ = ['AdvancedScreenOptionsDialog', 'show_advanced_screen_options']

