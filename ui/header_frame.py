# ui/header_frame.py
# Header Component avec bouton Réinitialiser + DRAG & DROP
# Created for RenExtract 

"""
Composant header avec titre, boutons aide, paramètres et quitter + support Drag & Drop
"""

import tkinter as tk
import os
from infrastructure.config.constants import VERSION, THEMES
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message
from ui.themes import theme_manager

class HeaderFrame(tk.Frame):
    """Frame d'en-tête avec titre et boutons de contrôle + Drag & Drop"""
    
    def __init__(self, parent, app_controller):
        self.app_controller = app_controller
        
        # Initialiser le Frame avec le thème
        theme = theme_manager.get_theme()
        super().__init__(parent, height=60, bg=theme["bg"])
        
        self.pack_propagate(False)
        
        # Références aux widgets pour mise à jour
        self.title_label = None
        self.subtitle_label = None
        self.btn_quit = None
        self.btn_settings = None
        self.btn_help = None
        
        self._create_widgets()
        self._setup_drag_drop()
    
    def _create_widgets(self):
        """Crée les widgets du header - VERSION AVEC AIDE"""
        theme = theme_manager.get_theme()
        
        # Frame pour le titre à gauche
        title_frame = tk.Frame(self, bg=theme["bg"])
        title_frame.pack(side='left', padx=(10, 0))
        
        # Titre principal
        self.title_label = tk.Label(
            title_frame,
            text=f"🎮 RenExtract {VERSION}",
            font=('Segoe UI Emoji', 16, 'bold'),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        self.title_label.pack(anchor='w')
        
        # Sous-titre
        self.subtitle_label = tk.Label(
            title_frame,
            text="Extraction intelligente de scripts Ren'Py",
            font=('Segoe UI Emoji', 10),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        self.subtitle_label.pack(anchor='w')
        
        # Frame pour les boutons à droite
        buttons_frame = tk.Frame(self, bg=theme["bg"])
        buttons_frame.pack(side='right', padx=(0, 10))
        
        # Bouton Quitter (le plus à droite)
        self.btn_quit = tk.Button(
            buttons_frame,
            text="❌ Quitter",
            font=('Segoe UI', 9),
            bg=theme["button_danger_bg"],   # MODIFIÉ - Négative/Danger
            fg="#000000",                    # MODIFIÉ - Texte noir uniforme
            relief='solid',
            cursor='hand2',
            command=self.app_controller.quit_application,
            width=15,
            pady=8
        )
        self.btn_quit.pack(side='right')

        self.btn_settings = tk.Button(
            buttons_frame,
            text="⚙️ Paramètres",
            font=('Segoe UI', 9),
            bg=theme["button_secondary_bg"], # MODIFIÉ - Secondaire
            fg="#000000",                    # MODIFIÉ - Texte noir uniforme
            relief='solid',
            cursor='hand2',
            command=self._show_general_settings,
            width=15,
            pady=8
        )
        self.btn_settings.pack(side='right', padx=(0, 5))

        self.btn_help = tk.Button(
            buttons_frame,
            text="❓ Guide Complet",
            font=('Segoe UI', 9),
            bg=theme["button_help_bg"],      # MODIFIÉ - Aide & Information
            fg="#000000",                    # MODIFIÉ - Texte noir uniforme
            relief='solid',
            cursor='hand2',
            command=self._show_html_tutorial,
            width=15,
            pady=8
        )
        self.btn_help.pack(side='right', padx=(0, 5))
    
    def _setup_drag_drop(self):
        """Configure le drag & drop sur tout le HeaderFrame"""
        try:
            # Vérifier si tkinterdnd2 est disponible
            import tkinterdnd2 as dnd2
            
            # Enregistrer le drop target sur le frame principal ET tous ses enfants
            self._register_drop_recursive(self)
            
            
            
        except ImportError:
            log_message("DEBUG", "tkinterdnd2 non disponible - Drag & Drop désactivé sur HeaderFrame", category="ui_header")
        except Exception as e:
            log_message("ATTENTION", f"Erreur configuration D&D HeaderFrame: {e}", category="ui_header")
    
    def _register_drop_recursive(self, widget):
        """Enregistre le drag & drop récursivement sur un widget et ses enfants"""
        try:
            import tkinterdnd2 as dnd2
            
            # Enregistrer sur le widget actuel
            if hasattr(widget, 'drop_target_register'):
                widget.drop_target_register(dnd2.DND_FILES)
                widget.dnd_bind('<<Drop>>', self._on_drop)
                widget.dnd_bind('<<DragEnter>>', self._on_drag_enter)
                widget.dnd_bind('<<DragLeave>>', self._on_drag_leave)
            
            # Enregistrer récursivement sur tous les enfants
            for child in widget.winfo_children():
                self._register_drop_recursive(child)
                
        except Exception as e:
            # ⚠️ Correction de sévérité: ce n'est pas un simple debug
            log_message("ATTENTION", f"Erreur enregistrement D&D récursif: {e}", category="ui_header")
    
    def _on_drop(self, event):
        """Gère le drop de fichiers/dossiers - DÉLÈGUE à l'InfoFrame"""
        try:
            # Déléguer le traitement à l'InfoFrame qui a toute la logique
            info_frame = self.app_controller.main_window.get_component('info')
            if info_frame and hasattr(info_frame, '_on_drop'):
                return info_frame._on_drop(event)
            else:
                log_message("ATTENTION", "InfoFrame non trouvé ou sans méthode _on_drop", category="ui_header")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur drop HeaderFrame: {e}", category="ui_header")
        
        return 'copy'
    
    def _on_drag_enter(self, event):
        """Effet visuel à l'entrée du drag"""
        try:
            # Effet subtil sur le header
            theme = theme_manager.get_theme()
            self.configure(bg='#2d5016', relief='solid', borderwidth=2)  # Vert foncé
        except Exception:
            pass
        return 'copy'
    
    def _on_drag_leave(self, event):
        """Remet l'apparence normale à la sortie du drag"""
        try:
            theme = theme_manager.get_theme()
            self.configure(bg=theme["bg"], relief='flat', borderwidth=0)
        except Exception:
            pass
        return 'copy'

    def update_language(self):
        """Met à jour les textes (maintenu pour la structure mais textes en dur)"""
        if self.title_label:
            self.title_label.config(text=f"🎮 RenExtract {VERSION}")
        if self.subtitle_label:
            self.subtitle_label.config(text="Extraction intelligente de scripts Ren'Py")
        if self.btn_settings:
            self.btn_settings.config(text="⚙️ Paramètres")
        if self.btn_help:
            self.btn_help.config(text="❓")
        if self.btn_quit:
            self.btn_quit.config(text="❌ Quitter")
    
    def apply_theme(self):
        """Applique le thème au composant"""
        theme = theme_manager.get_theme()
        
        self.configure(bg=theme["bg"])
        
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=theme["bg"])
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(bg=theme["bg"], fg=theme["fg"])
    
    def _show_general_settings(self):
        """Affiche la fenêtre des paramètres généraux"""
        try:
            from ui.dialogs.settings_interface import show_unified_settings
            root_window = self.app_controller.main_window.get_root()
            show_unified_settings(root_window, self.app_controller)
        except Exception as e:
            log_message("ERREUR", f"Erreur ouverture paramètres généraux: {e}", category="ui_header")

    def _show_html_tutorial(self):
        """Affiche le tutoriel HTML au lieu de l'ancienne interface"""
        try:
            from ui.tutorial import show_tutorial
            root_window = self.app_controller.main_window.get_root()
            show_tutorial(root_window)
        except Exception as e:
            log_message("ERREUR", f"Erreur ouverture tutoriel HTML: {e}", category="ui_header")    

    # =============================================================================
    # MÉTHODES PUBLIQUES POUR INTÉGRATION
    # =============================================================================
    
    def enable_drag_drop_delegation(self, target_info_frame):
        """Active la délégation du drag & drop vers l'InfoFrame"""
        self.target_info_frame = target_info_frame
    
    def get_drop_areas(self):
        """Retourne la liste des zones de drop du HeaderFrame"""
        drop_areas = [self]
        
        def collect_children(widget):
            areas = [widget]
            for child in widget.winfo_children():
                areas.extend(collect_children(child))
            return areas
        
        return collect_children(self)
