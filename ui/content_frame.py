# ui/content_frame.py
# Content Frame Component - VERSION CTRL+V UNIQUEMENT
# Created for RenExtract 

"""
Composant de la zone de contenu principal (zone de texte)
VERSION AMÉLIORÉE : Ctrl+V uniquement, plus de Drag & Drop
"""

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from infrastructure.config.constants import THEMES
from infrastructure.config.config import config_manager
from ui.themes import theme_manager
from infrastructure.logging.logging import log_message

class ContentFrame(tk.Frame):
    """Frame contenant la zone de texte principale - Ctrl+V uniquement"""
    
    def __init__(self, parent, app_controller):
        self.app_controller = app_controller
        
        # Initialiser le Frame avec le thème
        theme = theme_manager.get_theme()
        super().__init__(parent, bg=theme["bg"])
        
        # Zone de texte
        self.text_area = None
        
        self._create_widgets()
        self._setup_ctrl_v_only()
    
    def _create_widgets(self):
        """Crée la zone de texte avec scrollbar"""
        theme = theme_manager.get_theme()
        
        # Zone de texte avec scrollbar intégrée et bordure visible
        self.text_area = ScrolledText(
            self,
            font=('Cascadia Code', 10),
            bg=theme["entry_bg"],
            fg=theme["entry_fg"],
            selectbackground=theme["select_bg"],
            selectforeground=theme["select_fg"],
            insertbackground=theme["entry_fg"],
            relief="solid",
            borderwidth=1,
            wrap=tk.WORD
        )
        self.text_area.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Configuration initiale
        self._setup_text_area()
    
    def _setup_text_area(self):
        """Configure la zone de texte"""
        # État initial normal pour permettre l'édition
        self.text_area.configure(state='normal')
        
        # Message initial
        self._show_welcome_message()
    
    def _setup_ctrl_v_only(self):
        """Configure UNIQUEMENT le Ctrl+V (plus de Drag & Drop)"""
        try:
            # Désactiver explicitement tout Drag & Drop existant
            self._disable_drag_drop()
            
            # Activer UNIQUEMENT Ctrl+V
            self.text_area.bind('<Control-v>', self._handle_paste)
            self.text_area.bind('<Control-V>', self._handle_paste)
            
            # Également sur le frame principal au cas où
            self.bind('<Control-v>', self._handle_paste)
            self.bind('<Control-V>', self._handle_paste)
            
            # Permettre le focus sur la zone de texte
            self.text_area.focus_set()
            
            
            
        except Exception as e:
            log_message("ERREUR", f"Erreur configuration Ctrl+V ContentFrame: {e}", category="ui_content")
    
    def _disable_drag_drop(self):
        """Désactive explicitement le Drag & Drop sur la zone de texte"""
        try:
            # Désactiver tout drop target existant
            if hasattr(self.text_area, 'drop_target_unregister'):
                try:
                    self.text_area.drop_target_unregister()
                except Exception:
                    pass
            
            # Désactiver les événements DnD
            dnd_events = ['<<Drop>>', '<<DragEnter>>', '<<DragLeave>>']
            for event in dnd_events:
                try:
                    self.text_area.unbind(event)
                    self.unbind(event)
                except Exception:
                    pass
            
            
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur désactivation D&D ContentFrame: {e}", category="ui_content")
    
    def _handle_paste(self, event=None):
        """Gère le collage Ctrl+V avec validation intelligente"""
        try:
            # Récupérer le presse-papier
            try:
                clipboard_content = self.text_area.clipboard_get()
            except tk.TclError:
                self._show_notification("Presse-papier vide", 'warning')
                return "break"
            
            if not clipboard_content or not clipboard_content.strip():
                self._show_notification("Presse-papier vide", 'warning')
                return "break"
            
            # NOUVELLE VALIDATION DU CONTENU COLLÉ
            validation_result = self._validate_clipboard_content(clipboard_content)
            
            if not validation_result['is_valid']:
                if validation_result['file_type'] == 'technical_code':
                    # Contenu technique détecté
                    self._show_technical_content_dialog(clipboard_content, validation_result)
                else:
                    # Autre erreur
                    self._show_notification(validation_result['user_message'], 'warning')
                return "break"
            
            # Contenu validé - déléguer au contrôleur principal
            if hasattr(self.app_controller, 'load_from_clipboard'):
                self.app_controller.load_from_clipboard(clipboard_content)
                log_message("INFO", f"Contenu validé délégué à load_from_clipboard: {len(clipboard_content)} caractères", category="ui_content")
            else:
                log_message("ERREUR", "Méthode load_from_clipboard non trouvée dans app_controller", category="ui_content")
                self._show_notification("Erreur: méthode de traitement clipboard non disponible", 'error')
            
            return "break"
            
        except Exception as e:
            log_message("ERREUR", f"Erreur lors du collage: {e}", category="ui_content")
            self._show_notification("Erreur lors de l'accès au presse-papier", 'error')
            return "break"

    def _validate_clipboard_content(self, content):
        """Valide le contenu du presse-papier comme s'il était un fichier"""
        try:
            # Créer un fichier temporaire virtuel pour la validation
            import tempfile
            import os
            
            # Sauvegarder temporairement le contenu
            with tempfile.NamedTemporaryFile(mode='w', suffix='.rpy', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(content)
                temp_path = temp_file.name
            
            try:
                # Utiliser la validation intelligente
                from core.services.extraction.validation import validate_file_for_translation_processing
                validation_result = validate_file_for_translation_processing(temp_path)
                
                # Adapter le message pour le clipboard
                if validation_result['overall_valid']:
                    validation_result['user_message'] = "✅ Contenu de traduction valide détecté"
                else:
                    if validation_result['file_type'] == 'technical_code':
                        validation_result['user_message'] = "⚠️ Contenu technique détecté dans le presse-papiers"
                    else:
                        validation_result['user_message'] = "❌ Contenu invalide dans le presse-papier"
                
                return {
                    'is_valid': validation_result['overall_valid'],
                    'file_type': validation_result['file_type'],
                    'user_message': validation_result['user_message'],
                    'details': validation_result.get('content_validation', {})
                }
                
            finally:
                # Nettoyer le fichier temporaire
                try:
                    os.unlink(temp_path)
                except Exception:
                    pass
                    
        except Exception as e:
            log_message("ERREUR", f"Erreur validation clipboard: {e}", category="ui_content")
            return {
                'is_valid': True,  # En cas d'erreur, on laisse passer
                'file_type': 'unknown',
                'user_message': "⚠️ Validation impossible - contenu traité sans vérification",
                'details': {'error': str(e)}
            }

    def _show_technical_content_dialog(self, content, validation_result):
        """Affiche un dialogue pour le contenu technique dans le presse-papier"""
        try:
            from infrastructure.helpers.unified_functions import show_translated_messagebox
            
            # Analyser le type de contenu
            content_preview = content[:200] + "..." if len(content) > 200 else content
            
            message = f"""⚠️ Contenu technique détecté dans le presse-papier

    Ce contenu semble contenir du code d'interface plutôt que des traductions.

    Aperçu :
    {content_preview}

    Voulez-vous continuer le traitement ?
    (Non recommandé pour du code technique)"""

            result = show_translated_messagebox(
                'askyesno',
                'Contenu technique détecté',
                message,
                parent=self.app_controller.main_window.root if hasattr(self.app_controller, 'main_window') else None
            )
            
            if result:
                # ✅ CORRECTION : L'utilisateur VEUT forcer le traitement
                if hasattr(self.app_controller, 'load_from_clipboard'):
                    self.app_controller.load_from_clipboard(content)
                    self._show_notification("⚠️ Contenu technique traité (à vos risques)", 'warning')
            else:
                # ✅ CORRECT : Utilisateur refuse le traitement - on s'arrête là
                self._show_notification("❌ Traitement annulé - contenu technique rejeté", 'info')
                
        except Exception as e:
            log_message("ERREUR", f"Erreur dialogue contenu technique: {e}", category="ui_content")
            self._show_notification("Erreur lors de la validation du contenu", 'error')
    
    def _show_notification(self, message, toast_type='info'):
        """Affiche une notification via l'app controller"""
        try:
            if hasattr(self.app_controller, 'main_window'):
                self.app_controller.main_window.show_notification(
                    message, 'TOAST', toast_type=toast_type
                )
        except Exception as e:
            log_message("ATTENTION", f"Erreur notification ContentFrame: {e}", category="ui_content")
    
    def _show_welcome_message(self):
        """Affiche le message d'accueil spécialisé Ctrl+V"""
        auto_status = "ON" if config_manager.is_auto_open_enabled() else "OFF"
        
        welcome_text = f"""⌨️ Zone de collage Ctrl+V

Utilisez Ctrl+V pour coller du contenu directement dans cette zone.

Ouverture-Auto: {auto_status}

💡 Astuce : Pour les fichiers et dossiers, utilisez la zone intelligente en haut
   avec les boutons 📄 Fichier et 📂 Dossier, ou glissez-déposez 
   n'importe où dans l'interface SAUF ici.

ℹ️  Cette zone est dédiée exclusivement au collage de texte."""

        self.text_area.delete('1.0', tk.END)
        self.text_area.insert('1.0', welcome_text)
    
    def get_text_area(self):
        """Retourne la zone de texte"""
        return self.text_area
    
    def load_content(self, content):
        """Charge du contenu dans la zone de texte"""
        if self.text_area:
            self.text_area.configure(state='normal')
            self.text_area.delete('1.0', tk.END)
            if isinstance(content, list):
                self.text_area.insert('1.0', ''.join(content))
            else:
                self.text_area.insert('1.0', content)
    
    def clear_content(self):
        """Vide la zone de texte et affiche le message d'accueil"""
        self._show_welcome_message()
    
    def get_content(self):
        """Récupère le contenu de la zone de texte"""
        if self.text_area:
            return self.text_area.get('1.0', tk.END)
        return ""
    
    def apply_theme(self):
        """Applique le thème au composant"""
        theme = theme_manager.get_theme()
        
        # Frame principal
        self.configure(bg=theme["bg"])
        
        # Zone de texte
        if self.text_area:
            self.text_area.configure(
                bg=theme["entry_bg"],
                fg=theme["entry_fg"],
                selectbackground=theme["select_bg"],
                selectforeground=theme["select_fg"],
                insertbackground=theme["entry_fg"],
                highlightbackground=theme["frame_bg"],
                highlightcolor=theme["accent"]
            )
    
    def update_language(self):
        """Met à jour l'affichage selon la langue"""
        # Vérifier si on affiche le message d'accueil
        current_content = self.get_content()
        if any(indicator in current_content for indicator in ["Zone de collage", "Ctrl+V", "Auto-Open"]):
            self._show_welcome_message()
    
    def update_display_for_auto_open(self):
        """Met à jour l'affichage quand Auto-Open change"""
        # Si on affiche le message d'accueil, le mettre à jour
        current_content = self.get_content()
        if "Auto-Open:" in current_content or "Ouverture-Auto:" in current_content:
            self._show_welcome_message()
    
    # =============================================================================
    # MÉTHODES PUBLIQUES POUR INTERACTION EXTERNE
    # =============================================================================
    
    def force_ctrl_v_mode(self):
        """Force le mode Ctrl+V uniquement (pour s'assurer de la configuration)"""
        self._setup_ctrl_v_only()
    
    def is_showing_welcome_message(self):
        """Vérifie si le message d'accueil est affiché"""
        current_content = self.get_content()
        return "Zone de collage Ctrl+V" in current_content
    
    def enable_text_input(self):
        """Active la saisie de texte"""
        if self.text_area:
            self.text_area.configure(state='normal')
    
    def disable_text_input(self):
        """Désactive la saisie de texte"""
        if self.text_area:
            self.text_area.configure(state='disabled')
    
    def get_focus(self):
        """Donne le focus à la zone de texte"""
        if self.text_area:
            self.text_area.focus_set()
    
    # =============================================================================
    # MÉTHODES DE COMPATIBILITÉ (ancien système)
    # =============================================================================
    
    def update_display_for_input_mode(self, input_mode):
        """Compatibilité - plus utilisé car on force Ctrl+V"""
        # Cette méthode n'est plus nécessaire car ContentFrame = toujours Ctrl+V
        # Mais on la garde pour compatibilité
        if self.is_showing_welcome_message():
            self._show_welcome_message()
