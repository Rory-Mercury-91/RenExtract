# ui/notification_manager.py
# Advanced Notification Manager - Completely Refactored
# Created for RenExtract 

"""
Gestionnaire intelligent de notifications complètement refait
- Gestion robuste des toasts avec limite et priorités
- Fallbacks gracieux pour tous les composants
- Thread-safe et optimisé
- Intégration complète avec les thèmes
"""

import tkinter as tk
from tkinter import messagebox
import threading
import time
import queue
from collections import deque
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass
from enum import Enum

from infrastructure.logging.logging import log_message
from infrastructure.config.config import config_manager


class NotificationType(Enum):
    """Types de notifications supportés"""
    TOAST = "toast"
    MODAL = "modal"
    STATUS = "status"
    CONFIRM = "confirm"


class ToastType(Enum):
    """Types de toasts avec couleurs correspondantes"""
    SUCCESS = "success"      # Vert
    WARNING = "warning"      # Orange
    ERROR = "error"         # Rouge
    INFO = "info"           # Gris


@dataclass
class ToastConfig:
    """Configuration d'un toast"""
    message: str
    toast_type: ToastType
    duration: int = 3000
    priority: int = 0  # Plus élevé = plus prioritaire
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class NotificationManager:
    """Gestionnaire intelligent de notifications - Version refaite"""
    
    # Constantes de configuration
    MAX_TOASTS = 4
    TOAST_WIDTH = 380       # Réduit à 380px (compromise entre lisibilité et espace)
    TOAST_HEIGHT = 56        # Légèrement réduit à 56px 
    TOAST_PADDING = 40       # Augmenté pour éviter la scrollbar (16 -> 25px)
    TOAST_SPACING = 10       # Espacement entre toasts
    
    # Couleurs des toasts (fond coloré, texte noir)
    TOAST_COLORS = {
        ToastType.SUCCESS: {'bg': '#28a745', 'fg': '#000000', 'border': '#218838'},
        ToastType.WARNING: {'bg': '#ffc107', 'fg': '#000000', 'border': '#b38600'},
        ToastType.ERROR: {'bg': '#ff8379', 'fg': '#000000', 'border': '#b21f2d'},
        ToastType.INFO: {'bg': '#6c757d', 'fg': '#000000', 'border': '#545b62'},
    }
    
    # Durées par défaut (en millisecondes)
    DEFAULT_DURATIONS = {
        ToastType.SUCCESS: 3000,
        ToastType.WARNING: 5000,
        ToastType.ERROR: 7000,
        ToastType.INFO: 3000,
    }
    
    def __init__(self, root: tk.Tk, app_controller):
        """Initialise le gestionnaire de notifications"""
        self.root = root
        self.app_controller = app_controller
        
        # Thread safety
        self._lock = threading.RLock()
        
        # Gestion des toasts
        self.active_toasts: deque = deque(maxlen=self.MAX_TOASTS)
        self.toast_positions: List[Dict] = []
        
        # Queue pour les toasts en attente
        self.toast_queue: queue.Queue = queue.Queue()
        
        # État du gestionnaire
        self.is_destroyed = False
        
        # Cache des positions pour optimisation
        self._position_cache = {}
        self._last_window_size = None
        
    
    def notify(self, message: str, notification_type: str = 'TOAST', 
               duration: int = None, title: str = None, 
               toast_type: str = 'info', priority: int = 0, **kwargs) -> bool:
        """
        Interface principale pour afficher une notification
        
        Args:
            message: Message à afficher
            notification_type: 'TOAST', 'MODAL', 'STATUS', 'CONFIRM'
            duration: Durée d'affichage (ms) - None = durée par défaut
            title: Titre pour les modales
            toast_type: 'success', 'warning', 'error', 'info'
            priority: Priorité (0-10, plus élevé = plus prioritaire)
            **kwargs: Arguments supplémentaires
            
        Returns:
            bool: True si succès, False sinon (pour CONFIRM, retourne le résultat)
        """
        if self.is_destroyed:
            return False
            
        try:
            # Convertir les types string en enum si nécessaire
            if isinstance(notification_type, str):
                notification_type = notification_type.upper()
            
            if isinstance(toast_type, str):
                toast_type = ToastType(toast_type.lower())
            elif isinstance(toast_type, str):
                # Fallback pour les anciennes valeurs
                toast_type = getattr(ToastType, toast_type.upper(), ToastType.INFO)
            
            # Router selon le type
            if notification_type == 'TOAST':
                return self._handle_toast(message, toast_type, duration, priority)
            elif notification_type == 'MODAL':
                return self._handle_modal(message, title, 'info')
            elif notification_type == 'STATUS':
                return self._handle_status(message)
            elif notification_type == 'CONFIRM':
                return self._handle_confirm(message, title)
            else:
                log_message("ATTENTION", f"Type de notification inconnu: {notification_type}", category="ui_notify")
                return self._handle_toast(message, ToastType.INFO, duration, priority)
                
        except Exception as e:
            log_message("ERREUR", f"Erreur dans notify(): {e}", category="ui_notify")
            # Fallback silent - ne pas échouer l'application
            return False

    def _handle_toast(self, message: str, toast_type: ToastType, 
                    duration: int = None, priority: int = 0) -> bool:
        """Gère l'affichage d'un toast"""
        try:
            # Durée par défaut si non spécifiée
            if duration is None:
                duration = self.DEFAULT_DURATIONS.get(toast_type, 3000)
            
            # Limiter la durée (max 10 secondes comme demandé)
            duration = min(duration, 10000)
            
            # Créer la configuration du toast
            toast_config = ToastConfig(
                message=message,
                toast_type=toast_type,
                duration=duration,
                priority=priority
            )
            
            # Thread-safe - ✅ SIMPLIFIÉ
            with self._lock:
                return self._show_toast_immediate(toast_config)
                
        except Exception as e:
            log_message("ERREUR", f"Erreur _handle_toast(): {e}", category="ui_notify")
            return False
    
    def _show_toast_immediate(self, config: ToastConfig) -> bool:
        """Affiche immédiatement un toast en remplaçant le plus ancien si nécessaire"""
        try:
            # ✅ NOUVEAU : Si on a atteint la limite, supprimer le plus ancien
            if len(self.active_toasts) >= self.MAX_TOASTS:
                # Supprimer le premier toast (le plus ancien)
                if self.active_toasts:
                    oldest_toast = self.active_toasts[0]  # Premier = plus ancien
                    self._remove_toast(oldest_toast['window'])
            
            # Afficher le nouveau toast
            return self._create_toast_window(config)
            
        except Exception as e:
            log_message("ERREUR", f"Erreur _show_toast_immediate(): {e}", category="ui_notify")
            return False
    
    def _create_toast_window(self, config: ToastConfig) -> bool:
        """Crée une fenêtre toast"""
        try:
            # Vérifier que le root existe encore
            if not self.root or not self.root.winfo_exists():
                return False
            
            # Créer la fenêtre toast
            toast_window = tk.Toplevel(self.root)
            toast_window.title("")
            toast_window.resizable(False, False)
            toast_window.attributes('-topmost', True)
            toast_window.overrideredirect(True)
            
            # Configuration visuelle
            colors = self.TOAST_COLORS[config.toast_type]
            
            # Frame principal avec bordure
            main_frame = tk.Frame(
                toast_window,
                bg=colors['bg'],
                highlightbackground=colors['border'],
                highlightthickness=2,
                bd=0
            )
            main_frame.pack(fill='both', expand=True)
            
            # Label du message avec texte noir
            message_label = tk.Label(
                main_frame,
                text=config.message,
                font=('Segoe UI', 10, 'bold'),
                bg=colors['bg'],
                fg=colors['fg'],
                anchor='center',              # Alignement à gauche au lieu de center
                justify='center',          # Justification à gauche
                wraplength=self.TOAST_WIDTH - 36  # Ajusté pour la nouvelle taille (40->36)
            )
            message_label.pack(fill='both', expand=True, padx=12, pady=10)  # Plus de padding
            
            # Calculer la position
            position = self._calculate_toast_position(len(self.active_toasts))
            toast_window.geometry(f"{self.TOAST_WIDTH}x{self.TOAST_HEIGHT}+{position['x']}+{position['y']}")
            
            # Enregistrer le toast
            toast_data = {
                'window': toast_window,
                'config': config,
                'position': position,
                'created_at': time.time()
            }
            
            self.active_toasts.append(toast_data)
            
            # Configuration des événements
            self._setup_toast_events(toast_window, toast_data, main_frame, message_label)
            
            # Programmer la fermeture automatique
            self._schedule_toast_close(toast_window, config.duration)
            
            # Repositionner tous les toasts
            self.root.after(10, self._reposition_all_toasts)
            
            return True
            
        except Exception as e:
            log_message("ERREUR", f"Erreur _create_toast_window(): {e}", category="ui_notify")
            return False
    
    def _setup_toast_events(self, toast_window: tk.Toplevel, toast_data: Dict,
                           main_frame: tk.Frame, message_label: tk.Label):
        """Configure les événements du toast"""
        try:
            # Fermeture au clic
            def on_click(event=None):
                self._remove_toast(toast_window)
            
            # Bind sur tous les widgets
            for widget in [toast_window, main_frame, message_label]:
                widget.bind('<Button-1>', on_click)
                widget.configure(cursor='hand2')
            
            # Gestion de la destruction
            def on_destroy(event=None):
                if toast_data in self.active_toasts:
                    with self._lock:
                        try:
                            self.active_toasts.remove(toast_data)
                        except ValueError:
                            pass  # Déjà supprimé
                    
                    # Repositionner après suppression
                    if self.root and self.root.winfo_exists():
                        self.root.after(10, self._reposition_all_toasts)
            
            toast_window.bind('<Destroy>', on_destroy)
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur _setup_toast_events(): {e}", category="ui_notify")
    
    def _calculate_toast_position(self, toast_index: int) -> Dict[str, int]:
        """Calcule la position d'un toast (optimisé avec cache)"""
        try:
            # Obtenir les dimensions de la fenêtre
            self.root.update_idletasks()
            parent_x = self.root.winfo_x()
            parent_y = self.root.winfo_y()
            parent_width = self.root.winfo_width()
            parent_height = self.root.winfo_height()
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Cache key pour optimisation
            cache_key = (parent_x, parent_y, parent_width, parent_height, toast_index)
            
            if cache_key in self._position_cache:
                return self._position_cache[cache_key]
            
            # Calcul de la position - POSITION AJUSTÉE
            # Plus de marge à droite et en bas pour les toasts plus grands
            x = parent_x + parent_width - self.TOAST_WIDTH - self.TOAST_PADDING
            y = parent_y + parent_height - self.TOAST_HEIGHT - self.TOAST_PADDING - (toast_index * (self.TOAST_HEIGHT + self.TOAST_SPACING))
            
            # Contraintes d'écran - OPTIMISÉES pour éviter les scrollbars
            # Marge minimale de 20px pour éviter les barres de défilement
            min_margin = 20
            scrollbar_margin = 30  # Marge supplémentaire pour les scrollbars
            
            if x < min_margin:
                x = min_margin
            if y < min_margin:
                y = min_margin
            # Prendre en compte l'espace des scrollbars à droite et en bas
            if x + self.TOAST_WIDTH > screen_width - scrollbar_margin:
                x = screen_width - self.TOAST_WIDTH - scrollbar_margin
            if y + self.TOAST_HEIGHT > screen_height - scrollbar_margin:
                y = screen_height - self.TOAST_HEIGHT - scrollbar_margin
            
            position = {'x': x, 'y': y}
            
            # Mettre en cache (limiter la taille du cache)
            if len(self._position_cache) > 50:
                self._position_cache.clear()
            
            self._position_cache[cache_key] = position
            return position
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur _calculate_toast_position(): {e}", category="ui_notify")
            # Position par défaut ajustée
            return {'x': 120, 'y': 120}
    
    def _reposition_all_toasts(self):
        """Repositionne tous les toasts actifs (optimisé)"""
        try:
            if not self.active_toasts:
                return
            
            # Copie thread-safe de la liste
            with self._lock:
                toasts_copy = list(self.active_toasts)
            
            # Repositionner chaque toast
            for index, toast_data in enumerate(reversed(toasts_copy)):
                try:
                    if not toast_data['window'].winfo_exists():
                        continue
                    
                    new_position = self._calculate_toast_position(index)
                    
                    # Ne repositionner que si nécessaire
                    current_geo = toast_data['window'].geometry()
                    new_geo = f"{self.TOAST_WIDTH}x{self.TOAST_HEIGHT}+{new_position['x']}+{new_position['y']}"
                    
                    if current_geo != new_geo:
                        toast_data['window'].geometry(new_geo)
                        toast_data['position'] = new_position
                
                except Exception as e:
                    log_message("ATTENTION", f"Erreur repositionnement toast individuel: {e}", category="ui_notify")
                    
        except Exception as e:
            log_message("ATTENTION", f"Erreur _reposition_all_toasts(): {e}", category="ui_notify")
    
    def _schedule_toast_close(self, toast_window: tk.Toplevel, duration: int):
        """Programme la fermeture automatique d'un toast"""
        def close_toast():
            try:
                time.sleep(duration / 1000.0)  # Convertir ms en secondes
                if toast_window and toast_window.winfo_exists():
                    # Utiliser after pour thread safety
                    self.root.after(0, lambda: self._remove_toast(toast_window))
            except Exception as e:
                log_message("ATTENTION", f"Erreur fermeture automatique toast: {e}", category="ui_notify")
        
        # Lancer dans un thread séparé pour ne pas bloquer l'UI
        close_thread = threading.Thread(target=close_toast, daemon=True)
        close_thread.start()
    
    def _remove_toast(self, toast_window: tk.Toplevel):
        """Supprime un toast spécifique"""
        try:
            if toast_window and toast_window.winfo_exists():
                toast_window.destroy()
        except Exception as e:
            log_message("ATTENTION", f"Erreur _remove_toast(): {e}", category="ui_notify")
    
    def _handle_modal(self, message: str, title: str = None, msg_type: str = 'info') -> bool:
        """Gère l'affichage d'une modal"""
        try:
            # Utiliser les fonctions existantes avec fallback gracieux
            title = title or "Information"
            
            try:
                # Essayer d'abord avec le système unifié
                from infrastructure.helpers.unified_functions import show_translated_messagebox
                show_translated_messagebox(msg_type, title, message)
                return True
            except ImportError:
                # Fallback vers messagebox standard
                if msg_type == 'info':
                    messagebox.showinfo(title, message)
                elif msg_type == 'warning':
                    messagebox.showwarning(title, message)
                elif msg_type == 'error':
                    messagebox.showerror(title, message)
                return True
                
        except Exception as e:
            log_message("ERREUR", f"Erreur _handle_modal(): {e}", category="ui_notify")
            # Fallback ultime
            try:
                messagebox.showinfo("Information", str(message))
                return True
            except Exception:
                return False
    
    def _handle_confirm(self, message: str, title: str = None) -> bool:
        """Gère l'affichage d'une confirmation"""
        try:
            title = title or "Confirmation"
            
            try:
                # Essayer avec le système unifié
                from infrastructure.helpers.unified_functions import show_translated_messagebox
                return show_translated_messagebox("askyesno", title, message)
            except ImportError:
                # Fallback vers messagebox standard
                return messagebox.askyesno(title, message)
                
        except Exception as e:
            log_message("ERREUR", f"Erreur _handle_confirm(): {e}", category="ui_notify")
            # Fallback ultime - retourner False (annulé)
            return False
    
    def _handle_status(self, message: str) -> bool:
        """Gère la mise à jour du statut"""
        try:
            # Essayer plusieurs méthodes de fallback
            
            # Méthode 1: Via app_controller
            if hasattr(self.app_controller, 'update_status'):
                self.app_controller.update_status(message)
                return True
            
            # Méthode 2: Via main_window
            if hasattr(self.app_controller, 'main_window'):
                main_window = self.app_controller.main_window
                if main_window and hasattr(main_window, 'update_status'):
                    main_window.update_status(message)
                    return True
                
                # Méthode 3: Via info_frame
                if hasattr(main_window, 'get_component'):
                    info_frame = main_window.get_component('info')
                    if info_frame and hasattr(info_frame, 'update_status'):
                        info_frame.update_status(message)
                        return True
            
            # Méthode 4: Chercher directement un label de statut
            status_widgets = self._find_status_widgets(self.root)
            if status_widgets:
                for widget in status_widgets:
                    try:
                        widget.config(text=message)
                        return True
                    except Exception:
                        continue
            
            # Aucune méthode n'a fonctionné
            log_message("ATTENTION", f"Impossible de mettre à jour le statut: {message}", category="ui_notify")
            return False
            
        except Exception as e:
            log_message("ERREUR", f"Erreur _handle_status(): {e}", category="ui_notify")
            return False
    
    def _find_status_widgets(self, parent: tk.Widget) -> List[tk.Widget]:
        """Trouve les widgets qui pourraient être des barres de statut"""
        status_widgets = []
        
        try:
            for child in parent.winfo_children():
                # Chercher des labels avec certains noms/propriétés
                if isinstance(child, tk.Label):
                    widget_name = str(child).lower()
                    if any(keyword in widget_name for keyword in ['status', 'statut', 'info']):
                        status_widgets.append(child)
                
                # Recherche récursive
                status_widgets.extend(self._find_status_widgets(child))
        
        except Exception:
            pass  # Ignorer les erreurs de parcours
        
        return status_widgets
    
    # Méthodes de raccourci avec les bonnes couleurs
    def show_success(self, message: str, duration: int = 3000, priority: int = 0) -> bool:
        """Affiche un toast de succès (vert)"""
        return self.notify(message, 'TOAST', duration, toast_type='success', priority=priority)
    
    def show_warning(self, message: str, duration: int = 5000, priority: int = 1) -> bool:
        """Affiche un toast d'avertissement (orange)"""
        return self.notify(message, 'TOAST', duration, toast_type='warning', priority=priority)
    
    def show_error(self, message: str, duration: int = 7000, priority: int = 2) -> bool:
        """Affiche un toast d'erreur (rouge)"""
        return self.notify(message, 'TOAST', duration, toast_type='error', priority=priority)
    
    def show_info(self, message: str, duration: int = 3000, priority: int = 0) -> bool:
        """Affiche un toast d'information (gris)"""
        return self.notify(message, 'TOAST', duration, toast_type='info', priority=priority)
    
    def show_modal_error(self, message: str, title: str = None) -> bool:
        """Affiche une erreur en modal"""
        return self.notify(message, 'MODAL', title=title or "Erreur")
    
    def ask_confirmation(self, message: str, title: str = None) -> bool:
        """Demande une confirmation"""
        return self.notify(message, 'CONFIRM', title=title or "Confirmation")
    
    def update_status(self, message: str) -> bool:
        """Met à jour la barre de statut"""
        return self.notify(message, 'STATUS')
    
    # Méthodes de gestion avancée
    def clear_all_toasts(self):
        """Supprime tous les toasts actifs"""
        with self._lock:
            toasts_to_remove = list(self.active_toasts)
            
        for toast_data in toasts_to_remove:
            try:
                self._remove_toast(toast_data['window'])
            except Exception as e:
                log_message("ATTENTION", f"Erreur suppression toast: {e}", category="ui_notify")
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du gestionnaire"""
        with self._lock:
            return {
                'active_toasts': len(self.active_toasts),
                'max_toasts': self.MAX_TOASTS,
                'cache_size': len(self._position_cache),
                'is_destroyed': self.is_destroyed,
                'toast_types': {
                    toast_type.value: sum(1 for t in self.active_toasts 
                                        if t['config'].toast_type == toast_type)
                    for toast_type in ToastType
                }
            }
    
    def cleanup(self):
        """Nettoie le gestionnaire (à appeler à la fermeture)"""
        try:
            self.is_destroyed = True
            self.clear_all_toasts()
            self._position_cache.clear()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur cleanup NotificationManager: {e}", category="ui_notify")
    
    def __del__(self):
        """Destructeur"""
        try:
            if not self.is_destroyed:
                self.cleanup()
        except Exception:
            pass  # Ignorer les erreurs dans le destructeur