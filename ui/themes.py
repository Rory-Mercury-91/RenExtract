# ui/themes.py - SYSTÈME DE THÈMES CORRIGÉ ET FRANCISÉ
"""
Gestionnaire de thèmes corrigé pour RenExtract
🆕 Version francisée : "sombre" et "clair" au lieu de "dark" et "light"
"""

import tkinter as tk
from tkinter import ttk
import threading
from infrastructure.config.constants import THEMES

class ThemeManager:
    """Gestionnaire de thèmes avec pattern Singleton thread-safe"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # Configuration manager importé localement pour éviter les imports circulaires
        from infrastructure.config.config import config_manager
        
        # Initialisation unique - FRANCISÉ
        self.current_theme = "sombre" if config_manager.is_dark_mode_enabled() else "clair"
        self.style = None
        self._initialized = True
        self.config_manager = config_manager
        
        # Cache des widgets pour performance
        self.widget_cache = {
            'frames': [],
            'labels': [],
            'buttons': [],
            'text_widgets': [],
            'windows': [],
            'entries': [],
            'checkbuttons': [],
            'labelframes': []
        }
        
        # Système de gestion globale des fenêtres
        self.registered_windows = []
        self.theme_change_callbacks = []

    def set_theme(self, theme_name):
        """Définit le thème actuel et applique les changements - VERSION FRANCISÉE"""
        # Conversion automatique anglais -> français
        theme_mapping = {
            "dark": "sombre",
            "light": "clair",
            "sombre": "sombre",
            "clair": "clair"
        }
        
        normalized_theme = theme_mapping.get(theme_name, theme_name)
        
        if self._theme_exists(normalized_theme):
            self.current_theme = normalized_theme
            # Sauvegarder dans la config (toujours en mode booléen)
            self.config_manager.set("dark_mode", normalized_theme == "sombre")
            # Appliquer immédiatement à tous les widgets et fenêtres
            self.apply_to_all_cached_widgets()
            self.apply_theme_to_all_windows()
            self.notify_theme_change()
    
    def _theme_exists(self, theme_name):
        """Vérifie si un thème existe - VERSION FRANCISÉE"""
        # Mapping français -> anglais pour THEMES
        french_to_english = {
            "sombre": "dark",
            "clair": "light"
        }
        
        english_theme = french_to_english.get(theme_name)
        return english_theme and english_theme in THEMES
    
    def get_theme(self, theme_name=None):
        """
        Récupère le thème complet en fusionnant les couleurs de base (clair/sombre)
        avec les couleurs des boutons personnalisables depuis la configuration.
        """
        # Mapping français -> anglais pour accéder aux THEMES
        french_to_english = {
            "sombre": "dark",
            "clair": "light"
        }
        
        if theme_name:
            # Conversion automatique
            theme_mapping = {
                "dark": "sombre",
                "light": "clair",
                "sombre": "sombre", 
                "clair": "clair"
            }
            normalized_theme = theme_mapping.get(theme_name, theme_name)
            english_theme = french_to_english.get(normalized_theme, "dark")
            base_colors = THEMES.get(english_theme, THEMES["dark"]).copy()
        else:
            # Thème actuel
            english_theme = french_to_english.get(self.current_theme, "dark")
            base_colors = THEMES[english_theme].copy()
        
        # 2. Récupère les couleurs des boutons depuis config.json
        # C'est ici que la personnalisation par l'utilisateur prend effet.
        button_colors = self.config_manager.get_theme_colors()

        # 3. Fusionne les deux dictionnaires. Les couleurs des boutons 
        #    s'ajoutent aux couleurs de base du thème.
        full_theme = {**base_colors, **button_colors}
        
        return full_theme
    
    def toggle_theme(self):
        """Bascule entre les thèmes clair et sombre - VERSION FRANCISÉE"""
        new_theme = "clair" if self.current_theme == "sombre" else "sombre"
        self.set_theme(new_theme)
        return new_theme
    
    def get_current_theme_name(self):
        """Retourne le nom du thème actuel en français"""
        return self.current_theme
    
    def is_dark_mode(self):
        """Vérifie si le mode sombre est actif"""
        return self.current_theme == "sombre"
    
    def is_light_mode(self):
        """Vérifie si le mode clair est actif"""
        return self.current_theme == "clair"
    
    def apply_to_widget(self, widget, widget_type="default"):
        """Applique le thème à un widget spécifique"""
        if not widget:
            return
        
        theme = self.get_theme()
        
        try:
            # Catégoriser le widget
            if isinstance(widget, tk.Frame):
                self._apply_to_frame(widget, theme)
                self._cache_widget(widget, 'frames')
                
            elif isinstance(widget, tk.Label):
                self._apply_to_label(widget, widget_type, theme)
                self._cache_widget(widget, 'labels')
                
            elif isinstance(widget, tk.Text):
                self._apply_to_text(widget, theme)
                self._cache_widget(widget, 'text_widgets')
                
            elif isinstance(widget, tk.Entry):
                self._apply_to_entry(widget, theme)
                self._cache_widget(widget, 'entries')
                
            elif isinstance(widget, tk.Button):
                self._apply_to_button(widget, theme)
                self._cache_widget(widget, 'buttons')
                
            elif isinstance(widget, (tk.Tk, tk.Toplevel)):
                widget.configure(bg=theme["bg"])
                self._cache_widget(widget, 'windows')
                
        except Exception as e:
            pass
    
    def _apply_to_frame(self, widget, theme):
        """Applique le thème aux frames"""
        widget.configure(bg=theme["frame_bg"])

    def apply_current_theme(self):
        """✅ NOUVELLE MÉTHODE : Applique le thème actuel à tous les widgets"""
        try:
            # Méthode 1 : Utiliser apply_to_all_cached_widgets (déjà existante)
            self.apply_to_all_cached_widgets()
            
            # Méthode 2 : Forcer la mise à jour du thème actuel
            current_theme_name = self.current_theme
            theme = self.get_theme(current_theme_name)
            
            return True
            
        except Exception as e:
            from infrastructure.logging.logging import log_message
            log_message("ATTENTION", f"Erreur apply_current_theme: {e}", category="ui_theme")
            return False

    def refresh_all_themes(self):
        """✅ NOUVELLE MÉTHODE : Rafraîchit complètement tous les thèmes - VERSION FRANCISÉE"""
        try:
            # Recalculer le thème actuel
            self.current_theme = "sombre" if self.config_manager.is_dark_mode_enabled() else "clair"
            
            # Appliquer le thème
            self.apply_current_theme()
            
            return True
            
        except Exception as e:
            from infrastructure.logging.logging import log_message
            log_message("ATTENTION", f"Erreur refresh_all_themes: {e}", category="ui_theme")
            return False

    def _apply_to_label(self, widget, widget_type, theme):
        """Applique le thème aux labels"""
        if widget_type == "title":
            widget.configure(bg=theme["bg"], fg=theme["fg"])
        elif widget_type == "subtitle":
            widget.configure(bg=theme["bg"], fg=theme["fg"])
        elif widget_type == "path_label":
            widget.configure(bg=theme["frame_bg"], fg=theme["accent"])
        elif widget_type == "stats_label":
            widget.configure(bg=theme["frame_bg"], fg=theme["fg"])
        else:
            widget.configure(bg=theme["frame_bg"], fg=theme["fg"])
    
    def _apply_to_text(self, widget, theme):
        """Applique le thème aux widgets Text - VERSION AMÉLIORÉE"""
        widget.configure(
            bg=theme["entry_bg"],
            fg=theme["accent"],                # CHANGÉ : Texte vert au lieu de entry_fg
            selectbackground=theme["select_bg"],
            selectforeground=theme["select_fg"],
            insertbackground='#1976d2',        # CHANGÉ : Curseur bleu au lieu de entry_fg
            highlightbackground=theme["accent"],
            highlightcolor=theme["accent"],
            highlightthickness=2,
            relief="solid",
            borderwidth=1
        )

    def _apply_to_entry(self, widget, theme):
        """Applique le thème aux Entry - VERSION AMÉLIORÉE"""
        widget.configure(
            bg=theme["entry_bg"],
            fg=theme["accent"],                # CHANGÉ : Texte vert au lieu de entry_fg  
            selectbackground=theme["select_bg"],
            selectforeground=theme["select_fg"],
            insertbackground='#1976d2',        # CHANGÉ : Curseur bleu au lieu de entry_fg
            highlightbackground=theme["accent"],
            highlightcolor=theme["accent"],
            highlightthickness=1
        )

    def apply_uniform_combobox_style(self, style_obj):
        """Applique un style uniforme aux Combobox - adapté au thème sombre avec texte noir"""
        theme = self.get_theme()
        
        style_obj.configure("TCombobox",
                        fieldbackground=theme["entry_bg"],
                        background=theme["entry_bg"],
                        foreground="#000000",  # Texte noir pour lisibilité
                        arrowcolor="#000000",  # Flèche noire
                        borderwidth=1,
                        relief="solid")
        
        style_obj.map("TCombobox",
                    fieldbackground=[("readonly", theme["entry_bg"]), ("focus", theme["entry_bg"])],
                    background=[("readonly", theme["entry_bg"]), ("focus", theme["entry_bg"])],
                    foreground=[("readonly", "#000000"), ("focus", "#000000")],  # Texte noir même en readonly
                    bordercolor=[("focus", theme["accent"])])

    def _apply_to_button(self, widget, theme):
        """Applique le thème aux boutons avec détection intelligente du type"""
        try:
            # Détecter le type de bouton et appliquer la bonne couleur
            button_bg = self._detect_button_color(widget, theme)
            widget.configure(bg=button_bg, fg=theme["button_fg"])
        except:
            pass
    
    def _cache_widget(self, widget, category):
        """Met en cache un widget par catégorie"""
        if widget not in self.widget_cache[category]:
            self.widget_cache[category].append(widget)

    def force_refresh_all_windows(self):
        """Force le rafraîchissement de toutes les fenêtres de l'application"""
        try:
            import tkinter as tk
            
            # Obtenir toutes les fenêtres Tk ouvertes
            root_windows = []
            
            # Méthode 1 : Via tkinter._default_root si disponible
            try:
                if hasattr(tk, '_default_root') and tk._default_root:
                    root_windows.append(tk._default_root)
            except:
                pass
            
            # Méthode 2 : Chercher toutes les fenêtres via l'app_controller
            try:
                # Si on a accès à l'app_controller
                if hasattr(self, 'app_controller') and self.app_controller:
                    if hasattr(self.app_controller, 'main_window'):
                        root_windows.append(self.app_controller.main_window)
                    if hasattr(self.app_controller, 'get_all_windows'):
                        root_windows.extend(self.app_controller.get_all_windows())
            except:
                pass
            
            # Méthode 3 : Utiliser une référence globale (à implémenter)
            try:
                from main import app_instance  # Adapter selon votre structure
                if app_instance and hasattr(app_instance, 'main_window'):
                    root_windows.append(app_instance.main_window)
            except:
                pass
            
            # Rafraîchir toutes les fenêtres trouvées
            for window in root_windows:
                if window and hasattr(window, 'winfo_exists'):
                    try:
                        if window.winfo_exists():
                            self._refresh_window_recursively(window)
                    except:
                        continue
            
            return True
            
        except Exception as e:
            from infrastructure.logging.logging import log_message
            log_message("ERREUR", f"Erreur force_refresh_all_windows: {e}", category="ui_theme")
            return False

    def _refresh_window_recursively(self, widget):
        """Rafraîchit récursivement tous les widgets d'une fenêtre"""
        try:
            theme = self.get_theme()
            
            # Mettre à jour le widget actuel selon son type
            if isinstance(widget, tk.Button):
                self._refresh_button(widget, theme)
            elif isinstance(widget, tk.Frame):
                widget.configure(bg=theme.get("frame_bg", theme["bg"]))
            elif isinstance(widget, tk.Label):
                widget.configure(bg=theme.get("frame_bg", theme["bg"]), fg=theme["fg"])
            elif isinstance(widget, (tk.Tk, tk.Toplevel)):
                widget.configure(bg=theme["bg"])
            
            # Récursion sur les enfants
            try:
                for child in widget.winfo_children():
                    self._refresh_window_recursively(child)
            except:
                pass
                
        except Exception as e:
            # Ignorer les erreurs sur les widgets individuels
            pass

    def _refresh_button(self, button, theme):
        """Rafraîchit un bouton en détectant sa catégorie par sa couleur actuelle"""
        try:
            current_bg = button.cget("bg")
            
            # Mapping des anciennes couleurs vers les nouvelles clés
            color_mapping = {
                # Couleurs par défaut vers clés sémantiques
                "#98FB98": "button_primary_bg",      # Vert pâle -> Primaire
                "#ADD8E6": "button_secondary_bg",    # Bleu ciel -> Secondaire  
                "#EEE8AA": "button_tertiary_bg",     # Or pâle -> Tertiaire
                "#F08080": "button_danger_bg",       # Corail -> Danger
                "#E6E6FA": "button_feature_bg",      # Lavande -> Feature
                "#FFA07A": "button_powerful_bg",     # Saumon -> Puissant
                "#DCDCDC": "button_devtool_bg",      # Gainsboro -> Dev
                "#AFEEEE": "button_nav_bg",          # Turquoise -> Navigation
                "#7FFFD4": "button_help_bg",         # Aquamarine -> Aide
                "#D3D3D3": "button_utility_bg",      # Gris -> Utilitaires
            }
            
            # Si on trouve une correspondance, utiliser la nouvelle couleur
            if current_bg in color_mapping:
                new_color_key = color_mapping[current_bg]
                button.configure(
                    bg=theme.get(new_color_key, current_bg),
                    fg="#000000"
                )
            # Sinon, vérifier si c'est déjà une couleur du thème actuel
            else:
                # Chercher si la couleur actuelle correspond à une valeur du thème
                for key, value in theme.items():
                    if key.startswith("button_") and key.endswith("_bg") and current_bg == value:
                        # C'est déjà à jour
                        button.configure(fg="#000000")  # S'assurer que le texte est noir
                        break
                        
        except Exception:
            pass

    def apply_to_all_cached_widgets(self):
        """Applique le thème à tous les widgets en cache"""
        theme = self.get_theme()
        
        # Frames
        for widget in self.widget_cache['frames']:
            try:
                self._apply_to_frame(widget, theme)
            except:
                pass
        
        # Labels
        for widget in self.widget_cache['labels']:
            try:
                self._apply_to_label(widget, "default", theme)
            except:
                pass
        
        # Text widgets
        for widget in self.widget_cache['text_widgets']:
            try:
                self._apply_to_text(widget, theme)
            except:
                pass
        
        # Entry widgets
        for widget in self.widget_cache['entries']:
            try:
                self._apply_to_entry(widget, theme)
            except:
                pass
        
        # Buttons
        for widget in self.widget_cache['buttons']:
            try:
                self._apply_to_button(widget, theme)
            except:
                pass
        
        # Checkbuttons
        for widget in self.widget_cache['checkbuttons']:
            try:
                widget.configure(
                    bg=theme["bg"],
                    fg=theme["fg"],
                    selectcolor=theme["entry_bg"],
                    activebackground=theme["bg"],
                    activeforeground=theme["fg"]
                )
            except:
                pass
        
        # LabelFrames
        for widget in self.widget_cache['labelframes']:
            try:
                widget.configure(
                    bg=theme["bg"],
                    fg=theme["fg"],
                    relief="flat",
                    borderwidth=1
                )
            except:
                pass
        
        # Windows
        for widget in self.widget_cache['windows']:
            try:
                widget.configure(bg=theme["bg"])
            except:
                pass
    
    def get_dialog_theme(self):
        """Récupère la configuration de thème pour les dialogues"""
        theme = self.get_theme()
        return {
            'bg': theme["bg"],
            'fg': theme["fg"],
            'frame_bg': theme["frame_bg"],
            'button_bg': theme["button_bg"],
            'button_fg': theme["button_fg"],
            'accent': theme["accent"],
            'warning': theme["warning"],
            'danger': theme["danger"],
        }
    
    def register_window(self, window):
        """Enregistre une fenêtre pour recevoir les changements de thème"""
        if window not in self.registered_windows:
            self.registered_windows.append(window)
    
    def unregister_window(self, window):
        """Désenregistre une fenêtre"""
        if window in self.registered_windows:
            self.registered_windows.remove(window)
    
    def register_theme_change_callback(self, callback):
        """Enregistre une fonction de callback pour les changements de thème"""
        if callback not in self.theme_change_callbacks:
            self.theme_change_callbacks.append(callback)
    
    def unregister_theme_change_callback(self, callback):
        """Désenregistre une fonction de callback"""
        if callback in self.theme_change_callbacks:
            self.theme_change_callbacks.remove(callback)
    
    def apply_theme_to_all_windows(self):
        """Applique le thème à toutes les fenêtres enregistrées"""
        theme = self.get_theme()
        
        for window in self.registered_windows[:]:  # Copie pour éviter les modifications pendant l'itération
            try:
                if hasattr(window, 'apply_theme'):
                    # Si la fenêtre a sa propre méthode apply_theme
                    window.apply_theme()
                elif hasattr(window, 'window') and hasattr(window.window, 'configure'):
                    # Si c'est un objet avec une propriété window
                    window.window.configure(bg=theme["bg"])
                    self._apply_theme_recursive(window.window, theme)
                elif hasattr(window, 'configure'):
                    # Si c'est directement une fenêtre Tkinter
                    window.configure(bg=theme["bg"])
                    self._apply_theme_recursive(window, theme)
            except Exception as e:
                from infrastructure.logging.logging import log_message
                log_message("ATTENTION", f"Erreur application thème fenêtre: {e}", category="ui_theme")
                # Retirer la fenêtre problématique de la liste
                if window in self.registered_windows:
                    self.registered_windows.remove(window)
    
    def notify_theme_change(self):
        """Notifie tous les callbacks enregistrés du changement de thème"""
        for callback in self.theme_change_callbacks[:]:  # Copie pour éviter les modifications
            try:
                callback(self.current_theme)
            except Exception as e:
                from infrastructure.logging.logging import log_message
                log_message("ATTENTION", f"Erreur callback changement thème: {e}", category="ui_theme")
    
    def _apply_theme_recursive(self, widget, theme):
        """Applique le thème récursivement à tous les widgets enfants"""
        try:
            # Appliquer le thème au widget actuel
            if isinstance(widget, tk.Frame):
                widget.configure(bg=theme["bg"])
            elif isinstance(widget, tk.Label):
                widget.configure(bg=theme["bg"], fg=theme["fg"])
            elif isinstance(widget, tk.Button):
                # Détecter le type de bouton et appliquer la bonne couleur
                button_bg = self._detect_button_color(widget, theme)
                widget.configure(bg=button_bg, fg=theme["button_fg"])
            elif isinstance(widget, tk.Checkbutton):
                # Appliquer le thème aux checkboxes
                widget.configure(
                    bg=theme["bg"],
                    fg=theme["fg"],
                    selectcolor=theme["entry_bg"],
                    activebackground=theme["bg"],
                    activeforeground=theme["fg"]
                )
            elif isinstance(widget, tk.LabelFrame):
                # Appliquer le thème aux sections (LabelFrame)
                widget.configure(
                    bg=theme["bg"],
                    fg=theme["fg"],
                    relief="flat",
                    borderwidth=1
                )
            elif isinstance(widget, tk.Entry):
                widget.configure(bg=theme["entry_bg"], fg=theme["entry_fg"])
            elif isinstance(widget, tk.Text):
                widget.configure(bg=theme["entry_bg"], fg=theme["entry_fg"])
            
            # Appliquer récursivement aux enfants
            for child in widget.winfo_children():
                self._apply_theme_recursive(child, theme)
                
        except Exception:
            pass  # Ignorer les erreurs sur les widgets qui ne supportent pas certaines options
    
    def _detect_button_color(self, button, theme):
        """Détecte la couleur appropriée pour un bouton selon son texte ou ses propriétés"""
        try:
            button_text = button.cget("text").lower()
            
            # Mots-clés pour détecter le type de bouton
            if any(word in button_text for word in ["fermer", "close", "supprimer", "delete", "réinitialiser", "reset"]):
                return theme.get("button_danger_bg", theme["button_bg"])
            elif any(word in button_text for word in ["nettoyer", "clean", "extraire", "extract", "démarrer", "start"]):
                return theme.get("button_powerful_bg", theme["button_bg"])
            elif any(word in button_text for word in ["à propos", "about", "aide", "help"]):
                return theme.get("button_help_bg", theme["button_bg"])
            elif any(word in button_text for word in ["par défaut", "default", "sauvegarder", "save"]):
                return theme.get("button_secondary_bg", theme["button_bg"])
            elif any(word in button_text for word in ["paramètres", "settings", "configuration"]):
                return theme.get("button_tertiary_bg", theme["button_bg"])
            else:
                # Bouton par défaut
                return theme.get("button_primary_bg", theme["button_bg"])
                
        except Exception:
            # En cas d'erreur, utiliser la couleur par défaut
            return theme.get("button_primary_bg", theme["button_bg"])

# Instance globale du gestionnaire de thèmes
theme_manager = ThemeManager()