# ui/buttons_frame.py
# Buttons Frame Component avec chemin de sortie
# Created for RenExtract 

"""
Composant contenant tous les boutons d'action de l'application organisés par onglets
VERSION AMÉLIORÉE : Drag & Drop + Affichage chemin de sortie
"""

import tkinter as tk
import os
from infrastructure.config.constants import THEMES, FOLDERS
from infrastructure.config.config import config_manager
from ui.themes import theme_manager
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import extract_game_name
from core.services.extraction.extraction import get_file_base_name

class ButtonsFrame(tk.Frame):
    """Frame contenant tous les boutons d'action organisés par onglets + Drag & Drop + Chemin de sortie"""
    
    def __init__(self, parent, app_controller):
        self.app_controller = app_controller
        theme = theme_manager.get_theme()
        super().__init__(parent, bg=theme["bg"])
        
        self.current_tab = "preparation"
        self.buttons = {}
        self.tab_buttons = {}
        
        # Variables pour le chemin de sortie
        self.output_path_var = tk.StringVar()
        self.output_path_label = None
        
        self._create_widgets()
        self._show_tab("preparation")
        self._setup_drag_drop()
    
    def _create_widgets(self):
        """Crée les widgets - AVEC champ de sortie direct"""
        self._create_tab_bar()
        self._create_button_area()
        self._create_conditional_output_field()
        self._setup_drag_drop()
    
    def _create_tab_bar(self):
        """Crée la barre d'onglets - SANS l'onglet ENTRÉE"""
        theme = theme_manager.get_theme()
        
        tab_frame = tk.Frame(self, bg=theme["bg"])
        tab_frame.pack(fill='x', pady=(0, 10))
        
        center_frame = tk.Frame(tab_frame, bg=theme["bg"])
        center_frame.pack(expand=True)
        
        # NOUVEL ORDRE : Préparation, Actions, Outils
        tabs = [
            ("preparation", "🔬 PRÉPARATION", theme["button_secondary_bg"]),  # Secondaire
            ("actions", "⚡ ACTIONS", theme["button_tertiary_bg"]),           # Tertiaire
            ("outils", "🧰 OUTILS", theme["button_tertiary_bg"])             # Tertiaire
        ]

        for tab_id, text, color in tabs:
            btn = tk.Button(
                center_frame, text=text, font=('Segoe UI', 11, 'bold'), 
                bg=color, 
                fg="#000000",  # MODIFIÉ - Texte noir uniforme
                relief='solid', cursor='hand2', command=lambda t=tab_id: self._show_tab(t),
                width=20, pady=10
            )
            btn.pack(side='left', padx=5)
            self.tab_buttons[tab_id] = btn

    def _create_conditional_output_field(self):
        """Crée le champ de sortie conditionnel"""
        # Créer la frame mais ne pas l'afficher tout de suite
        self._create_output_field_widgets()
        # Mettre à jour la visibilité selon le paramètre
        self._update_output_field_visibility()

    def _create_output_field_widgets(self):
        """Crée les widgets du champ de sortie (sans les afficher)"""
        theme = theme_manager.get_theme()
        
        # Ligne directe
        self.output_line = tk.Frame(self, bg=theme["bg"])
        # NE PAS pack ici - sera fait conditionnellement
        
        # Label
        output_label = tk.Label(
            self.output_line,
            text="📁 Dossier de sortie :",
            font=('Segoe UI', 10, 'bold'),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        output_label.pack(side='left', padx=(0, 10))
        
        # Entry (même code que avant)
        self.output_path_entry = tk.Entry(
            self.output_line,
            textvariable=self.output_path_var,
            font=('Segoe UI', 10),
            bg=theme["entry_bg"],
            fg=theme["entry_fg"],
            insertbackground=theme["entry_fg"],
            relief='solid',
            borderwidth=1,
            highlightbackground=theme.get("frame_bg", theme["bg"]),
            highlightcolor=theme.get("accent", "#007acc"),
            selectbackground=theme.get("select_bg", "#0078d4"),
            selectforeground=theme.get("select_fg", "#ffffff"),
        )
        self.output_path_entry.pack(side='left', fill='x', expand=True, padx=(0, 10), ipady=4)
        
        # Événements (même code que avant)
        self.output_path_entry.bind("<Button-1>", self._on_path_click)
        self.output_path_entry.bind("<Control-c>", self._copy_path)
        self.output_path_entry.bind("<Control-a>", self._select_all_path)
        self.output_path_entry.bind("<Button-3>", self._show_context_menu)
        
        # Désactiver l'édition
        self.output_path_entry.bind("<Key>", lambda e: "break")
        self.output_path_entry.bind("<BackSpace>", lambda e: "break")
        self.output_path_entry.bind("<Delete>", lambda e: "break")
        
        # État initial
        self._update_output_path_display()

    def _update_output_field_visibility(self):
        """Met à jour la visibilité du champ de sortie selon le paramètre"""
        try:
            show_field = config_manager.is_output_path_display_enabled()
            
            if show_field:
                # Afficher la frame
                self.output_line.pack(fill='x', padx=10, pady=(8, 5))
            else:
                # Cacher la frame
                self.output_line.pack_forget()
                
        except Exception as e:
            log_message("ERREUR", f"Erreur visibilité champ sortie: {e}", category="ui_buttons")

    def toggle_output_field_display(self, show=None):
        """Méthode publique pour basculer la visibilité du champ"""
        if show is None:
            # Basculer l'état actuel
            config_manager.toggle_output_path_display()
        else:
            # Définir explicitement
            config_manager.set_output_path_display(show)
        
        # Mettre à jour l'affichage
        self._update_output_field_visibility()

    def _select_all_path(self, event):
        """Sélectionne tout le texte (Ctrl+A)"""
        try:
            self.output_path_entry.select_range(0, tk.END)
            self.output_path_entry.icursor(tk.END)
            return "break"  # Empêche le comportement par défaut
        except Exception as e:
            log_message("ATTENTION", f"Erreur Ctrl+A: {e}", category="ui_buttons")

    def _show_context_menu(self, event):
        """Affiche un menu contextuel sur clic droit"""
        try:
            current_path = self.output_path_var.get()
            
            # Créer le menu contextuel
            context_menu = tk.Menu(self, tearoff=0)
            
            if current_path and current_path != "Lancez une extraction pour voir le dossier de sortie":
                context_menu.add_command(
                    label="📋 Copier le chemin",
                    command=self._copy_path
                )
                context_menu.add_command(
                    label="📂 Ouvrir le dossier",
                    command=self._open_output_folder
                )
                context_menu.add_separator()
                context_menu.add_command(
                    label="🔍 Sélectionner tout",
                    command=lambda: self.output_path_entry.select_range(0, tk.END)
                )
            else:
                context_menu.add_command(
                    label="ℹ️ Aucun dossier disponible",
                    state='disabled'
                )
            
            # Afficher le menu à la position du clic
            context_menu.tk_popup(event.x_root, event.y_root)
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur menu contextuel: {e}", category="ui_buttons")
        finally:
            # Nettoyer le menu après utilisation
            try:
                context_menu.grab_release()
            except:
                pass

    def _on_path_click(self, event):
        """Sélectionne tout le texte du chemin au clic"""
        try:
            # Sélectionner tout le texte
            self.output_path_entry.select_range(0, tk.END)
            self.output_path_entry.icursor(tk.END)  # Curseur à la fin
            
            # Donner le focus pour que la sélection soit visible
            self.output_path_entry.focus_set()
            
            log_message("DEBUG", "Chemin sélectionné au clic", category="ui_buttons")
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur sélection chemin: {e}", category="ui_buttons")
    
    def _copy_path(self, event=None):
        """Copie le chemin dans le presse-papier (Ctrl+C)"""
        try:
            current_path = self.output_path_var.get()
            if current_path and current_path != "Lancez une extraction pour voir le dossier de sortie":
                # Copier dans le presse-papier
                self.clipboard_clear()
                self.clipboard_append(current_path)
                
                # Notification de succès
                if hasattr(self.app_controller, 'main_window'):
                    self.app_controller.main_window.show_notification(
                        f"📋 Chemin copié : {os.path.basename(current_path)}", 
                        'TOAST', toast_type='success'
                    )
                
                log_message("INFO", f"Chemin copié: {current_path}", category="ui_buttons")
                
            else:
                # Notification d'avertissement
                if hasattr(self.app_controller, 'main_window'):
                    self.app_controller.main_window.show_notification(
                        "⚠️ Aucun dossier disponible à copier", 
                        'TOAST', toast_type='warning'
                    )
                
            return "break"  # Empêche le comportement par défaut
                
        except Exception as e:
            log_message("ATTENTION", f"Erreur copie chemin: {e}", category="ui_buttons")
    
    def _open_output_folder(self):
        """Ouvre le dossier de sortie dans l'explorateur avec notification si inactif"""
        try:
            current_path = self.output_path_var.get()
            
            # 🆕 TOAST NOTIFICATION au lieu de masquer le bouton
            if not current_path or current_path == "Lancez une extraction pour voir le dossier de sortie":
                self.app_controller.main_window.show_notification(
                    "🚫 Aucun dossier de sortie disponible. Lancez d'abord une extraction.", 
                    'TOAST', toast_type='warning'
                )
                return
            
            # Vérifier que le dossier existe
            if not os.path.exists(current_path):
                self.app_controller.main_window.show_notification(
                    "⚠️ Le dossier de sortie n'existe plus", 'TOAST', toast_type='warning'
                )
                return
            
            # Ouvrir le dossier
            self.app_controller._open_folder(current_path)
            
            # Notification de succès
            self.app_controller.main_window.show_notification(
                f"📂 Dossier ouvert : {os.path.basename(current_path)}", 
                'TOAST', toast_type='success'
            )
            
            log_message("INFO", f"Dossier de sortie ouvert: {current_path}", category="ui_buttons")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur ouverture dossier de sortie: {e}", category="ui_buttons")
            self.app_controller.main_window.show_notification(
                f"❌ Erreur ouverture dossier: {e}", 'TOAST', toast_type='error'
            )
    
    def _update_output_path_display(self, path=None):
        """Met à jour l'affichage du chemin de sortie - SANS readonly"""
        try:
            # ⚠️ On récupère le thème AVANT le if/else
            theme = theme_manager.get_theme()

            # Si l'entry n'est pas encore créée, on sort silencieusement
            if not hasattr(self, 'output_path_entry') or self.output_path_entry is None:
                return

            if path and os.path.exists(path):
                # Chemin valide
                self.output_path_var.set(path)
                # Couleur accentuée pour un chemin réel
                if self.output_path_entry:
                    self.output_path_entry.config(fg=theme["accent"])
            else:
                # Pas de chemin
                self.output_path_var.set("Lancez une extraction pour voir le dossier de sortie")
                # Couleur neutre quand c'est le placeholder
                if self.output_path_entry:
                    self.output_path_entry.config(fg=theme["entry_fg"])

        except Exception as e:
            log_message("ATTENTION", f"Erreur mise à jour affichage chemin: {e}", category="ui_buttons")
    
    def update_output_path_after_extraction(self, original_path):
        """🆕 Met à jour le chemin après une extraction réussie"""
        try:
            if not original_path:
                return
            
            # Construire le chemin avec la nouvelle logique file_base
            game_name = extract_game_name(original_path)
            file_base = get_file_base_name(original_path)
            
            # Nouveau chemin avec sous-dossier fichier
            output_path = os.path.join(
                FOLDERS["temporaires"], 
                game_name, 
                file_base,  # 🆕 NOUVEAU : sous-dossier fichier
                "fichiers_a_traduire"
            )
            
            # Mettre à jour l'affichage
            self._update_output_path_display(output_path)
            
            log_message("INFO", f"Chemin de sortie mis à jour: {output_path}", category="ui_buttons")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur mise à jour chemin après extraction: {e}", category="ui_buttons")
    
    def clear_output_path(self):
        """🆕 Remet le chemin de sortie à l'état initial"""
        self._update_output_path_display()
    
    def _create_button_area(self):
        """Crée la zone des boutons switchable"""
        theme = theme_manager.get_theme()
        self.button_area = tk.Frame(self, bg=theme["bg"])
        self.button_area.pack(fill='x')
        self._create_preparation_buttons()
        self._create_actions_buttons()
        self._create_outils_buttons()
    
    def _create_preparation_buttons(self):
        """Crée les boutons de préparation"""
        theme = theme_manager.get_theme()
        self.preparation_frame = tk.Frame(self.button_area, bg=theme["bg"])
        center_frame = tk.Frame(self.preparation_frame, bg=theme["bg"])
        center_frame.pack(expand=True)
        
        preparation_buttons = [
            ("renpy_generator", "🎮 Générateur Ren'Py", self.app_controller.launch_renpy_generator, theme["button_secondary_bg"])  # MODIFIÉ
        ]

        for btn_id, text, command, color in preparation_buttons:
            btn = tk.Button(center_frame, text=text, font=('Segoe UI', 10), 
                        bg=color, 
                        fg="#000000", # MODIFIÉ - Texte noir uniforme
                        relief='solid', cursor='hand2', command=command, width=25, pady=8)
            btn.pack(side='left', padx=5)
            self.buttons[btn_id] = btn
    
    def _create_actions_buttons(self):
        """Crée les boutons d'actions (SANS le bouton Temporaire supprimé)"""
        theme = theme_manager.get_theme()
        self.actions_frame = tk.Frame(self.button_area, bg=theme["bg"])
        center_frame = tk.Frame(self.actions_frame, bg=theme["bg"])
        center_frame.pack(expand=True)
        
        actions_buttons = [
            ("extract", "⚡Extraire", self.app_controller.extract_texts, theme["button_primary_bg"]),                    # MODIFIÉ - Primaire
            ("reconstruct", "🔧 Reconstruire", self.app_controller.reconstruct_file, theme["button_primary_bg"]),       # MODIFIÉ - Primaire
            ("reload", "🔄 Revérifier", self.app_controller.reload_reconstructed, theme["button_primary_bg"]),          # MODIFIÉ - Primaire
        ]

        for btn_id, text, command, color in actions_buttons:
            btn = tk.Button(center_frame, text=text, font=('Segoe UI', 10), 
                        bg=color, 
                        fg="#000000", # MODIFIÉ - Texte noir uniforme
                        relief='solid', cursor='hand2', command=command, width=25, pady=8)
            btn.pack(side='left', padx=5)
            self.buttons[btn_id] = btn

    def _create_outils_buttons(self):
        """Crée les boutons d'outils"""
        theme = theme_manager.get_theme()
        self.outils_frame = tk.Frame(self.button_area, bg=theme["bg"])
        center_frame = tk.Frame(self.outils_frame, bg=theme["bg"])
        center_frame.pack(expand=True)
        
        # NOUVEAU : Ajout du bouton Outils Maintenance
        outils_buttons = [
            ("warnings", "⚠️ Rapport", self.app_controller.open_warnings, theme["button_tertiary_bg"]),
            ("temporaires", "📂 Temporaires", self.app_controller.open_temporary, theme["button_tertiary_bg"]),
            ("maintenance_tools", "🔧 Outils Spécialisé", self._show_maintenance_tools_interface, theme["button_tertiary_bg"]),  # NOUVEAU
            ("backups", "💾 Sauvegardes", self._show_unified_backup_manager, theme["button_tertiary_bg"])
        ]

        for btn_id, text, command, color in outils_buttons:
            btn = tk.Button(center_frame, text=text, font=('Segoe UI', 10), 
                        bg=color, 
                        fg="#000000",
                        relief='solid', cursor='hand2', command=command, width=25, pady=8)
            btn.pack(side='left', padx=5)
            self.buttons[btn_id] = btn
    
    def _setup_drag_drop(self):
        """Configure le drag & drop sur tout le ButtonsFrame"""
        try:
            # Vérifier si tkinterdnd2 est disponible
            import tkinterdnd2 as dnd2
            
            # Enregistrer le drop target sur le frame principal ET tous ses enfants
            self._register_drop_recursive(self)
            
            
            
        except ImportError:
            log_message("DEBUG", "tkinterdnd2 non disponible - Drag & Drop désactivé sur ButtonsFrame", category="ui_buttons")
        except Exception as e:
            log_message("ATTENTION", f"Erreur configuration D&D ButtonsFrame: {e}", category="ui_buttons")
    
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
            log_message("ATTENTION", f"Erreur enregistrement D&D récursif ButtonsFrame: {e}", category="ui_buttons")
    
    def _on_drop(self, event):
        """Gère le drop de fichiers/dossiers - DÉLÈGUE À l'InfoFrame"""
        try:
            # Déléguer le traitement à l'InfoFrame qui a toute la logique
            info_frame = self.app_controller.main_window.get_component('info')
            if info_frame and hasattr(info_frame, '_on_drop'):
                return info_frame._on_drop(event)
            else:
                log_message("ATTENTION", "InfoFrame non trouvé ou sans méthode _on_drop", category="ui_buttons")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur drop ButtonsFrame: {e}", category="ui_buttons")
        
        return 'copy'
    
    def _on_drag_enter(self, event):
        """Effet visuel à l'entrée du drag"""
        try:
            # Effet subtil - bordure verte sur la zone de boutons
            self.configure(relief='solid', borderwidth=2, highlightbackground='#28a745')
        except Exception:
            pass
        return 'copy'
    
    def _on_drag_leave(self, event):
        """Remet l'apparence normale à la sortie du drag"""
        try:
            theme = theme_manager.get_theme()
            self.configure(relief='flat', borderwidth=0, highlightbackground=theme["bg"])
        except Exception:
            pass
        return 'copy'
    
    def _show_tab(self, tab_id):
        """Affiche l'onglet sélectionné en conservant les couleurs personnalisables"""
        try:
            # Charger le thème actuel
            theme = theme_manager.get_theme()
            
            # Cacher tous les frames
            self.preparation_frame.pack_forget()
            self.actions_frame.pack_forget()
            self.outils_frame.pack_forget()
            
            # Reset des couleurs par défaut pour tous les onglets
            self._reset_tab_colors()
            
            # Afficher le frame correspondant
            # MODIFIÉ : L'onglet actif garde sa couleur personnalisable, pas la couleur accent
            if tab_id == "preparation":
                self.preparation_frame.pack(fill='x')
                # Garde la couleur secondaire personnalisable
                self.tab_buttons["preparation"].config(
                    bg=theme["button_secondary_bg"],
                    fg="#000000"
                )
            elif tab_id == "actions":
                self.actions_frame.pack(fill='x')
                # Garde la couleur primaire personnalisable
                self.tab_buttons["actions"].config(
                    bg=theme["button_primary_bg"],
                    fg="#000000"
                )
            elif tab_id == "outils":
                self.outils_frame.pack(fill='x')
                # Garde la couleur tertiaire personnalisable
                self.tab_buttons["outils"].config(
                    bg=theme["button_tertiary_bg"],
                    fg="#000000"
                )
            
            self.current_tab = tab_id
            
        except Exception as e:
            # Fallback en cas d'erreur avec les couleurs par défaut
            from infrastructure.logging.logging import log_message
            log_message("ERREUR", f"Erreur affichage onglet {tab_id}: {e}", category="ui_buttons")
            
            # Version fallback
            self.preparation_frame.pack_forget()
            self.actions_frame.pack_forget()
            self.outils_frame.pack_forget()
            
            if tab_id == "preparation":
                self.preparation_frame.pack(fill='x')
                self.tab_buttons["preparation"].config(bg="#ADD8E6", fg="#000000")
            elif tab_id == "actions":
                self.actions_frame.pack(fill='x')
                self.tab_buttons["actions"].config(bg="#98FB98", fg="#000000")
            elif tab_id == "outils":
                self.outils_frame.pack(fill='x')
                self.tab_buttons["outils"].config(bg="#EEE8AA", fg="#000000")
            
            self.current_tab = tab_id
    
    def _reset_tab_colors(self):
            """Remet les couleurs par défaut des onglets avec le système de thèmes"""
            try:
                # Charger le thème actuel
                theme = theme_manager.get_theme()
                
                # Mapping des onglets vers leurs couleurs sémantiques
                tab_colors = {
                    "preparation": theme["button_secondary_bg"],  # Bleu - Actions secondaires
                    "actions": theme["button_primary_bg"],       # Vert - Actions principales  
                    "outils": theme["button_tertiary_bg"],       # Jaune - Alternatives
                }
                
                # Appliquer les couleurs aux boutons d'onglets
                for tab_id, bg_color in tab_colors.items():
                    if tab_id in self.tab_buttons:
                        self.tab_buttons[tab_id].config(
                            bg=bg_color,
                            fg="#000000"  # Texte noir uniforme
                        )
                        
            except Exception as e:
                # Fallback en cas d'erreur
                from infrastructure.logging.logging import log_message
                log_message("ERREUR", f"Erreur reset couleurs onglets: {e}", category="ui_buttons")
                
                # Couleurs de secours
                fallback_colors = {
                    "preparation": "#ADD8E6",  # Bleu ciel
                    "actions": "#98FB98",      # Vert pâle
                    "outils": "#EEE8AA",       # Or pâle
                }
                
                for tab_id, bg_color in fallback_colors.items():
                    if tab_id in self.tab_buttons:
                        self.tab_buttons[tab_id].config(
                            bg=bg_color,
                            fg="#000000"
                        )
    
    # =============================================================================
    # MÉTHODES D'INTERFACE DE COMPATIBILITÉ (simplifiées)
    # =============================================================================
    
    def get_button(self, button_id):
        return self.buttons.get(button_id)
    
    # =============================================================================
    # MÉTHODES DE THÈME ET LOCALISATION
    # =============================================================================

    def apply_theme(self):
            """Application du thème - AVEC couleur accent comme InfoFrame"""
            theme = theme_manager.get_theme()
            self.configure(bg=theme["bg"])
            
            # Ligne de sortie
            if hasattr(self, 'output_line'):
                self.output_line.configure(bg=theme["bg"])
                
                for child in self.output_line.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(bg=theme["bg"], fg=theme["fg"])
            
            # ✅ ENTRY - Copie EXACTE de la logique InfoFrame (lignes 717-730)
            if hasattr(self, 'output_path_entry'):
                self.output_path_entry.configure(
                    bg=theme["entry_bg"],
                    fg=theme["entry_fg"],
                    insertbackground=theme["entry_fg"],
                    highlightbackground=theme.get("frame_bg", "#d0d0d0"),
                    highlightcolor=theme.get("accent", "#007acc"),
                    selectbackground=theme.get("select_bg", "#0078d4"),
                    selectforeground=theme.get("select_fg", "#ffffff")
                )
                
                # ✅ COULEUR ACCENT comme InfoFrame - Même logique que lignes 740-754
                current_path = self.output_path_var.get()
                if current_path and current_path != "Lancez une extraction pour voir le dossier de sortie":
                    # Chemin valide = couleur accent (comme InfoFrame)
                    self.output_path_entry.config(fg=theme["accent"])
                else:
                    # Placeholder = couleur grise (comme InfoFrame)
                    self.output_path_entry.config(fg=theme["entry_fg"])
            
            # Zones de boutons (reste identique)
            if hasattr(self, 'button_area'): 
                self.button_area.configure(bg=theme["bg"])
            if hasattr(self, 'preparation_frame'): 
                self.preparation_frame.configure(bg=theme["bg"])
            if hasattr(self, 'actions_frame'): 
                self.actions_frame.configure(bg=theme["bg"])
            if hasattr(self, 'outils_frame'): 
                self.outils_frame.configure(bg=theme["bg"])
            
            # Application récursive (reste identique)
            for widget in self.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.configure(bg=theme["bg"])
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Frame):
                            child.configure(bg=theme["bg"])
                            for grandchild in child.winfo_children():
                                if isinstance(grandchild, tk.Frame):
                                    grandchild.configure(bg=theme["bg"])

    def _show_unified_backup_manager(self):
        from ui.dialogs.unified_backup_interface import show_unified_backup_manager
        root_window = self.app_controller.main_window.get_root()
        show_unified_backup_manager(root_window)

    def _show_maintenance_tools_interface(self):
        """Lance l'interface des outils de maintenance"""
        try:
            from ui.dialogs.maintenance_tools_interface import show_maintenance_tools_interface
            # 🆕 CORRECTION : Passer main_window au lieu de root pour avoir accès à app_controller
            show_maintenance_tools_interface(self.app_controller.main_window)
            
        except Exception as e:
            log_message("ERREUR", f"Erreur lancement interface maintenance: {e}", category="ui_buttons")
            from infrastructure.helpers.unified_functions import show_translated_messagebox
            show_translated_messagebox(
                'error', 
                "Erreur", 
                f"Impossible de lancer l'interface des outils de maintenance:\n\n{e}"
            )

    def update_language(self):
        """Met à jour les textes selon la langue - SANS onglet ENTRÉE"""
        tab_texts = {
            "preparation": "🔬 PRÉPARATION",
            "actions": "⚡ ACTIONS",
            "outils": "🧰 OUTILS",
        }
        
        for tab_id, text in tab_texts.items():
            btn = self.tab_buttons.get(tab_id)
            if btn:
                btn.config(text=text)
        
        # Mettre à jour les boutons de préparation
        preparation_button_texts = {
            "renpy_generator": "🎮 " + "Générateur Ren'Py"
        }
        
        # Mettre à jour les boutons d'action (sans "temporary")
        actions_button_texts = {
            "extract": "⚡ " + "Extraire",
            "reconstruct": "🔧 " + "Reconstruire",
            "reload": "🔄 " + "Revérifier",
        }
        
        # Mettre à jour les boutons d'outils (sans "temporary")
        outils_button_texts = {
            "warnings": "⚠️ Rapport",
            "temporaires": "📂 Temporaires", 
            "maintenance_tools": "🔧 Outils Spécialisé",
            "backups": "💾 Sauvegardes"
        }
        
        # Appliquer tous les textes
        all_texts = {**preparation_button_texts, **actions_button_texts, **outils_button_texts}
        
        for btn_id, text in all_texts.items():
            btn = self.buttons.get(btn_id)
            if btn and text:
                btn.config(text=text)
    
    # =============================================================================
    # MÉTHODES PUBLIQUES POUR INTÉGRATION
    # =============================================================================
    
    def enable_drag_drop_delegation(self, target_info_frame):
        """Active la délégation du drag & drop vers l'InfoFrame"""
        self.target_info_frame = target_info_frame
    
    def get_drop_areas(self):
        """Retourne la liste des zones de drop du ButtonsFrame"""
        drop_areas = [self]
        
        def collect_children(widget):
            areas = [widget]
            for child in widget.winfo_children():
                areas.extend(collect_children(child))
            return areas
        
        return collect_children(self)
