# ui/main_window.py
# Main Window Interface - VERSION REFACTORISÉE AVEC SYSTÈME HYBRIDE
# Created for RenExtract 

"""
Fenêtre principale de l'application - Version avec système d'entrée hybride
Drag & Drop : Header + InfoFrame + ButtonsFrame
Ctrl+V : ContentFrame uniquement
"""

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import os
import sys

# Fonction utilitaire pour charger les ressources compatibles PyInstaller
def get_resource_path(relative_path):
    """Retourne le chemin absolu vers une ressource, compatible PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)

# Imports des composants d'interface AMÉLIORÉS
from ui.header_frame import HeaderFrame
from ui.info_frame import InfoFrame
from ui.buttons_frame import ButtonsFrame
from ui.content_frame import ContentFrame
from ui.input_manager import InputManager, setup_hybrid_input_system, get_input_status_message
from ui.notification_manager import NotificationManager

# Imports utilitaires
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message
from infrastructure.config.constants import VERSION, WINDOW_CONFIG
from ui.themes import theme_manager

class MainWindow:
    """Fenêtre principale avec système d'entrée hybride"""
    
    def __init__(self, root, app_controller):
        """Constructeur corrigé avec initialisation en étapes"""
        self.root = root
        self.app_controller = app_controller
        
        # Variables d'état de l'interface
        self.components = {}
        self.text_mode = "empty"
        self.input_system_status = "initializing"
        
        self._setup_window()
        self._create_components()
        self._finalize_initialization()  # NOUVEAU : étape finale

    def _finalize_initialization(self):
        """NOUVELLE FONCTION : Finalise l'initialisation après création des composants"""
        try:
            # Vérifier que tous les composants critiques sont créés
            required_components = ['header', 'info', 'buttons', 'content', 'input']
            missing_components = []
            
            for comp_name in required_components:
                if comp_name not in self.components or self.components[comp_name] is None:
                    missing_components.append(comp_name)
            
            if missing_components:
                log_message("ERREUR", f"Composants manquants: {missing_components}", category="ui_main")
                self.input_system_status = "error"
                return
            
            # Enregistrer cette fenêtre dans le système de thème global
            from ui.themes import theme_manager
            theme_manager.register_window(self)
            
            # MAINTENANT configurer le système hybride (tous les composants existent)
            self._setup_hybrid_input_system()
            self._setup_bindings()
            
            
        except Exception as e:
            self.input_system_status = "error"
            log_message("ERREUR", f"Erreur finalisation initialisation: {e}", category="ui_main")

    def _setup_window(self):
        """Configure la fenêtre principale"""
        self.root.title(f"{VERSION}")
        self.root.geometry(WINDOW_CONFIG["geometry"])
        self.root.minsize(*WINDOW_CONFIG["min_size"])
        
        # Appliquer l'icône personnalisée compatible PyInstaller
        try:
            icon_path = get_resource_path("icone.ico")
            if os.path.exists(icon_path):
                # Sur Windows, utiliser iconbitmap + SetCurrentProcessExplicitAppUserModelID
                if sys.platform == "win32":
                    try:
                        self.root.iconbitmap(icon_path)
                        # ✅ CORRECTION : Définir l'AppUserModelID pour que Windows utilise la bonne icône dans la barre des tâches
                        try:
                            import ctypes
                            # Identifiant unique pour l'application (utilisé par Windows pour l'icône de la barre des tâches)
                            app_id = 'com.renextract.app.1.2.15'
                            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
                            log_message("DEBUG", f"AppUserModelID défini: {app_id}", category="ui_main")
                        except Exception as e_win:
                            log_message("DEBUG", f"Impossible de définir AppUserModelID: {e_win}", category="ui_main")
                    except Exception as e_ico:
                        log_message("DEBUG", f"Icône Windows non chargée: {e_ico}", category="ui_main")
                else:
                    # Sur Linux/macOS, utiliser iconphoto avec une image PhotoImage
                    try:
                        from PIL import Image, ImageTk
                        img = Image.open(icon_path)
                        # Convertir en format compatible (si c'est un ICO, extraire la première image)
                        if hasattr(img, 'n_frames') and img.n_frames > 1:
                            img.seek(0)
                        # Redimensionner si nécessaire (tkinter préfère des tailles standard)
                        img = img.resize((256, 256), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        self.root.iconphoto(True, photo)
                        # Garder une référence pour éviter le garbage collection
                        self._icon_photo = photo
                    except ImportError:
                        # Si PIL n'est pas disponible, essayer iconbitmap quand même
                        self.root.iconbitmap(icon_path)
                    except Exception as e2:
                        log_message("DEBUG", f"Icône PIL non chargée: {e2}", category="ui_main")
                        # Fallback sur iconbitmap
                        try:
                            self.root.iconbitmap(icon_path)
                        except:
                            pass
            else:
                log_message("DEBUG", f"Icône introuvable: {icon_path}", category="ui_main")
        except Exception as e:
            log_message("DEBUG", f"Icône non chargée: {e}", category="ui_main")
        
        # Protocole de fermeture
        self.root.protocol("WM_DELETE_WINDOW", self.app_controller.quit_application)
    
    def _create_components(self):
        """Crée tous les composants de l'interface AMÉLIORÉS"""
        theme = theme_manager.get_theme()
        
        # Header avec Drag & Drop (titre, boutons aide/paramètres/quitter)
        self.components['header'] = HeaderFrame(
            self.root, 
            self.app_controller
        )
        self.components['header'].pack(fill='x', padx=20, pady=(20, 10))
        
        # InfoFrame avec champ intelligent + Drag & Drop
        self.components['info'] = InfoFrame(
            self.root,
            self.app_controller
        )
        self.components['info'].pack(fill='x', padx=20, pady=5)
        
        # ButtonsFrame avec Drag & Drop (sans section ENTRÉE)
        self.components['buttons'] = ButtonsFrame(
            self.root,
            self.app_controller
        )
        self.components['buttons'].pack(fill='x', padx=20, pady=10)
        
        # ContentFrame avec Ctrl+V uniquement
        self.components['content'] = ContentFrame(
            self.root,
            self.app_controller
        )
        self.components['content'].pack(expand=True, fill='both', padx=20, pady=(0, 10))
        
        # InputManager simplifié (coordinateur)
        self.components['input'] = InputManager(
            self.root,
            self.app_controller,
            self.components['content'].get_text_area()
        )
        
        # Gestionnaire de notifications
        self.components['notifications'] = NotificationManager(
            self.root,
            self.app_controller
        )
        
    
    def _setup_hybrid_input_system(self):
        """Configure le système d'entrée hybride - VERSION SÉCURISÉE"""
        try:
            # ✅ CORRECTION : Vérifier que SELF est bien initialisé
            if not hasattr(self, 'components') or not self.components:
                log_message("ERREUR", "self.components non initialisé", category="ui_main")
                self.input_system_status = "error"
                return
            
            # Vérifier que tous les composants existent AVANT d'appeler setup_hybrid_input_system
            required_components = ['header', 'info', 'buttons', 'content', 'input']
            for comp_name in required_components:
                if comp_name not in self.components or self.components[comp_name] is None:
                    log_message("ERREUR", f"Composant {comp_name} manquant pour le système hybride", category="ui_main")
                    self.input_system_status = "error"
                    return
            
            # ✅ CORRECTION : Passer SELF explicitement (pas dans __init__)
            setup_hybrid_input_system(self, self.app_controller)
            
            # Obtenir le statut du système
            input_manager = self.components.get('input')
            if input_manager:
                status_message = get_input_status_message(input_manager)
                self.input_system_status = "active"
            else:
                self.input_system_status = "error"
                log_message("ERREUR", "InputManager non trouvé après création", category="ui_main")
            
            # Configurer les délégations entre composants
            self._setup_component_delegations()
            
        except Exception as e:
            self.input_system_status = "error"
            log_message("ERREUR", f"Erreur configuration système hybride: {e}", category="ui_main")
    
    def _setup_component_delegations(self):
        """Configure les délégations entre composants pour une intégration optimale"""
        try:
            header = self.components.get('header')
            info = self.components.get('info')
            buttons = self.components.get('buttons')
            content = self.components.get('content')
            
            # Délégation Drag & Drop : Header/Buttons -> InfoFrame
            if header and info:
                header.enable_drag_drop_delegation(info)
            
            if buttons and info:
                buttons.enable_drag_drop_delegation(info)
            
            # Forcer le mode Ctrl+V sur ContentFrame
            if content:
                content.force_ctrl_v_mode()
                
            
        except Exception as e:
            log_message("ERREUR", f"Erreur configuration délégations: {e}", category="ui_main")
    
    def _setup_bindings(self):
        """Configure les liaisons d'événements SIMPLIFIÉES"""
        # Raccourcis clavier globaux (gardés pour compatibilité)
        self.root.bind('<Control-o>', lambda e: self._show_file_browser())
        self.root.bind('<Control-d>', lambda e: self._show_folder_browser())
        self.root.bind('<Control-e>', lambda e: self.app_controller.extract_texts())
        self.root.bind('<Control-r>', lambda e: self.app_controller.reconstruct_file())
        self.root.bind('<F1>', lambda e: self.app_controller.show_help())
        self.root.bind('<F5>', lambda e: self.app_controller.refresh())
        
    
    def _show_file_browser(self):
        """Raccourci Ctrl+O -> Utilise le bouton Fichier de l'InfoFrame"""
        try:
            info_frame = self.components.get('info')
            if info_frame and hasattr(info_frame, '_browse_file'):
                info_frame._browse_file()
            else:
                log_message("DEBUG", "Fallback Ctrl+O vers app_controller", category="ui_main")
                self.app_controller.open_file()
        except Exception as e:
            log_message("ERREUR", f"Erreur raccourci Ctrl+O: {e}", category="ui_main")
    
    def _show_folder_browser(self):
        """Raccourci Ctrl+D -> Utilise le bouton Dossier de l'InfoFrame"""
        try:
            info_frame = self.components.get('info')
            if info_frame and hasattr(info_frame, '_browse_folder'):
                info_frame._browse_folder()
            else:
                log_message("DEBUG", "Fallback Ctrl+D vers app_controller", category="ui_main")
                self.app_controller.open_folder()
        except Exception as e:
            log_message("ERREUR", f"Erreur raccourci Ctrl+D: {e}", category="ui_main")
    
    # =============================================================================
    # MÉTHODES D'INTERFACE PUBLIQUES
    # =============================================================================
    
    def get_component(self, name):
        """Récupère un composant par son nom"""
        return self.components.get(name)
    
    def get_text_area(self):
        """Récupère la zone de texte principale"""
        content_frame = self.components.get('content')
        if content_frame:
            return content_frame.get_text_area()
        return None
    
    def get_root(self):
        """Récupère la fenêtre racine (pour les dialogs)"""
        return self.root
    
    # =============================================================================
    # MÉTHODES DE MISE À JOUR DE L'INTERFACE
    # =============================================================================
    
    def update_file_info(self, filepath, line_count, stats=None, execution_time=None):
        """Met à jour les informations du fichier via l'InfoFrame amélioré"""
        try:
            info_frame = self.components.get('info')
            if info_frame:
                info_frame.update_file_info(filepath, line_count, stats, execution_time)
                
                # Mettre à jour le chemin dans le champ intelligent si nécessaire
                if filepath and hasattr(info_frame, 'set_path'):
                    current_path = info_frame.get_current_path()
                    if current_path != filepath:
                        info_frame.set_path(filepath)
                        
                # Rafraîchir l'affichage
                if hasattr(info_frame, 'refresh_display'):
                    info_frame.refresh_display()
                    
            
        except Exception as e:
            log_message("ERREUR", f"Erreur mise à jour infos fichier: {e}", category="ui_main")
    
    def update_status(self, message):
        """Met à jour le statut via l'InfoFrame"""
        info_frame = self.components.get('info')
        if info_frame:
            info_frame.update_status(message)
    
    def show_notification(self, message, notification_type='TOAST', **kwargs):
        """Affiche une notification"""
        notifications = self.components.get('notifications')
        if notifications:
            return notifications.notify(message, notification_type, **kwargs)
        else:
            # Fallback basique
            log_message("INFO", f"Notification: {message}", category="ui_main")
            return True
    
    # =============================================================================
    # MÉTHODES DE THÈME ET CONFIGURATION
    # =============================================================================
    
    def apply_theme(self):
        """Applique le thème à tous les composants"""
        try:
            # Appliquer à la fenêtre principale
            theme = theme_manager.get_theme()
            self.root.configure(bg=theme["bg"])
            
            # Initialiser le style ttk pour les comboboxes
            from tkinter import ttk
            style = ttk.Style()
            theme_manager.apply_uniform_combobox_style(style)
            
            # Appliquer à tous les composants
            for component_name, component in self.components.items():
                if hasattr(component, 'apply_theme'):
                    try:
                        component.apply_theme()
                    except Exception as e:
                        log_message("ATTENTION", f"Erreur thème {component_name}: {e}", category="ui_main")
            
            # Forcer la mise à jour de tous les widgets en cache
            theme_manager.apply_to_all_cached_widgets()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur application thème: {e}", category="ui_main")
    
    def update_language(self):
        """Met à jour la langue de tous les composants"""
        try:
            # Mettre à jour le titre de la fenêtre
            self.root.title(f"{VERSION}")
            
            # Mettre à jour tous les composants
            for component_name, component in self.components.items():
                if hasattr(component, 'update_language'):
                    try:
                        component.update_language()
                        log_message("DEBUG", f"Langue mise à jour pour {component_name}", category="ui_main")
                    except Exception as e:
                        log_message("ATTENTION", f"Erreur langue {component_name}: {e}", category="ui_main")
            
            log_message("INFO", "Langue mise à jour pour tous les composants", category="ui_main")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur mise à jour langue: {e}", category="ui_main")

    def recreate_interface(self):
        """Réinstancie tous les composants après changement de langue"""
        try:
            # Détruire les composants existants
            for comp_name, comp in self.components.items():
                if comp_name != 'notifications':  # Garder les notifications
                    try:
                        if hasattr(comp, 'destroy'):
                            comp.destroy()
                        elif hasattr(comp, 'pack_forget'):
                            comp.pack_forget()
                    except Exception as e:
                        log_message("ATTENTION", f"Erreur destruction {comp_name}: {e}", category="ui_main")
            
            # Nettoyer les références (garder notifications)
            notifications = self.components.get('notifications')
            self.components.clear()
            if notifications:
                self.components['notifications'] = notifications
            
            # Recréer tous les composants
            self._create_components()
            self._setup_hybrid_input_system()
            self._setup_bindings()
            
            # Appliquer le thème
            self.apply_theme()
            
            log_message("INFO", "Interface recréée avec succès", category="ui_main")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur recréation interface: {e}", category="ui_main")
    
    def force_refresh_project_languages(self):
        """Force le refresh des langues du projet (utile après génération)"""
        try:
            info_frame = self.components.get('info')
            if info_frame and hasattr(info_frame, 'force_refresh_languages'):
                info_frame.force_refresh_languages()
                log_message("INFO", "Refresh des langues demandé depuis MainWindow", category="ui_main")
            else:
                log_message("ATTENTION", "InfoFrame non disponible pour refresh des langues", category="ui_main")
        except Exception as e:
            log_message("ERREUR", f"Erreur refresh des langues: {e}", category="ui_main")

    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        try:
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            
            if width < 100 or height < 100:
                width, height = 1200, 800  # Taille par défaut plus grande
            
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            
            self.root.geometry(f"{width}x{height}+{x}+{y}")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur centre fenêtre: {e}", category="ui_main")
    
    # =============================================================================
    # MÉTHODES DE CONTRÔLE DE FENÊTRE
    # =============================================================================
    
    def withdraw(self):
        """Cache la fenêtre"""
        self.root.withdraw()
    
    def deiconify(self):
        """Affiche la fenêtre"""
        self.root.deiconify()
    
    def update(self):
        """Met à jour la fenêtre"""
        self.root.update()
    
    def mainloop(self):
        """Lance la boucle principale"""
        self.root.mainloop()
    
    # =============================================================================
    # MÉTHODES DE DÉBOGAGE ET DIAGNOSTIC
    # =============================================================================
    
    def get_system_status(self):
        """Retourne l'état du système pour diagnostic"""
        try:
            input_manager = self.components.get('input')
            status = {
                "components_loaded": len(self.components),
                "input_system": self.input_system_status,
                "input_manager_available": bool(input_manager),
                "theme": theme_manager.current_theme,
                "dnd_available": input_manager.is_dnd_available() if input_manager else False
            }
            return status
        except Exception as e:
            return {"error": str(e)}
    
    def debug_components_state(self):
        """Affiche l'état de tous les composants pour le débogage"""
        try:
            for name, component in self.components.items():
                if hasattr(component, 'debug_current_state'):
                    component.debug_current_state()
                else:
                    log_message("DEBUG", f"Composant {name}: {type(component).__name__}", category="ui_main")
        except Exception as e:
            log_message("ATTENTION", f"Erreur debug composants: {e}", category="ui_main")
    
    def force_refresh_all(self):
        """Force un rafraîchissement complet de l'interface"""
        try:
            self.apply_theme()
            
            # Rafraîchir l'InfoFrame
            info_frame = self.components.get('info')
            if info_frame and hasattr(info_frame, 'refresh_display'):
                info_frame.refresh_display()
            
            # Forcer la mise à jour du système d'entrée
            input_manager = self.components.get('input')
            if input_manager and hasattr(input_manager, 'force_ctrl_v_only_on_content'):
                input_manager.force_ctrl_v_only_on_content()
            
            self.root.update()
            log_message("INFO", "Rafraîchissement complet effectué", category="ui_main")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur rafraîchissement complet: {e}", category="ui_main")