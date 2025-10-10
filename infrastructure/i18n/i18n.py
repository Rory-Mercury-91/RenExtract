# utils/i18n.py - VERSION CORRIGÉE SANS IMPORTS CIRCULAIRES
# Internationalization Module
# Created for RenExtract 

"""
Module d'internationalisation simplifié
Version corrigée sans imports circulaires
Traductions par défaut externalisées dans des modules séparés
"""

import json
import os
import threading
import sys

class I18nManager:
    """Gestionnaire d'internationalisation simplifié"""

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
        if hasattr(self, '_initialized') and self._initialized:
            return

        # Configuration simple
        self.current_language = 'fr'
        self.translations = {}
        
        # Déterminer le dossier de configuration
        self.config_folder = self._get_config_folder()
        self.language_file = os.path.join(self.config_folder, "languages.json")
        
        # Langues supportées (version simple)
        self.supported_languages = {
            'fr': 'Français',
            'en': 'English',
            'de': 'Deutsch'
        }
        
        # Chargement des traductions
        self.load_translations()
        self._initialized = True

    def _get_config_folder(self):
        """Détermine le dossier de configuration sans dépendance externe"""
        try:
            # Tenter d'utiliser le dossier de l'exécutable
            if getattr(sys, 'frozen', False):
                # Exécutable PyInstaller
                base_dir = os.path.dirname(sys.executable)
            else:
                # Script Python
                base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            
            config_folder = os.path.join(base_dir, "04_Configs")
            
            # Créer le dossier s'il n'existe pas
            try:
                os.makedirs(config_folder, exist_ok=True)
            except Exception:
                # Fallback vers le dossier courant
                config_folder = "."
            
            return config_folder
            
        except Exception:
            # Fallback ultime
            return "."

    def _log_message(self, level, message, category="utils_i18n"):
        """Logger simple sans dépendance externe"""
        try:
            # Afficher seulement les messages INFO importants (chargement traductions)
            if level in ["INFO", "ATTENTION", "ERREUR"]:
                print(f"[I18N-{level}] {message}")
        except Exception:
            pass

    def load_translations(self):
        """Charge les traductions depuis le fichier JSON"""
        try:
            if os.path.exists(self.language_file):
                with open(self.language_file, 'r', encoding='utf-8') as f:
                    self.translations = json.load(f)
                self._log_message("INFO", "Traductions chargées depuis languages.json", category="utils_i18n")
            else:
                # Utiliser les traductions par défaut si le fichier n'existe pas
                self.translations = self._get_default_translations()
                self.save_translations()
                self._log_message("INFO", "Traductions par défaut créées", category="utils_i18n")
        except Exception as e:
            self._log_message("ATTENTION", f"Erreur chargement traductions: {e}", category="utils_i18n")
            self.translations = self._get_default_translations()

    def save_translations(self):
        """Sauvegarde les traductions dans le fichier JSON"""
        try:
            os.makedirs(os.path.dirname(self.language_file), exist_ok=True)
            with open(self.language_file, 'w', encoding='utf-8') as f:
                json.dump(self.translations, f, ensure_ascii=False, indent=2)
            self._log_message("INFO", "Traductions sauvegardées", category="utils_i18n")
        except Exception as e:
            self._log_message("ATTENTION", f"Erreur sauvegarde traductions: {e}", category="utils_i18n")

    def get_text(self, key, **kwargs):
        """
        Récupère le texte traduit pour une clé donnée
        
        Args:
            key: Clé de traduction (ex: 'buttons.extract')
            **kwargs: Variables à substituer dans le texte
            
        Returns:
            str: Texte traduit
        """
        try:
            # Navigation dans le dictionnaire par clés séparées par des points
            keys = key.split('.')
            text = self.translations.get(self.current_language, {})
            
            for k in keys:
                if isinstance(text, dict) and k in text:
                    text = text[k]
                else:
                    # Fallback vers le français si clé non trouvée
                    if self.current_language != 'fr':
                        text = self.translations.get('fr', {})
                        for fallback_k in keys:
                            if isinstance(text, dict) and fallback_k in text:
                                text = text[fallback_k]
                            else:
                                text = f"[{key}]"
                                break
                    else:
                        text = f"[{key}]"
                    break

            # S'assurer que c'est une chaîne
            if not isinstance(text, str):
                return f"[{key}]"

            # Remplacer les paramètres
            if kwargs:
                try:
                    text = text.format(**kwargs)
                except (KeyError, ValueError) as e:
                    self._log_message("ATTENTION", f"Erreur formatage '{key}': {e}", category="utils_i18n")

            return text

        except Exception as e:
            self._log_message("ERREUR", f"Erreur récupération texte '{key}': {e}", category="utils_i18n")
            return f"[{key}]"

    def set_language(self, language_code):
        """Change la langue courante"""
        if language_code in self.supported_languages:
            self.current_language = language_code
            self._log_message("INFO", f"Langue changée vers: {self.supported_languages[language_code]}", category="utils_i18n")
            return True
        else:
            self._log_message("ATTENTION", f"Langue non supportée: {language_code}", category="utils_i18n")
            return False

    def get_current_language(self):
        """Retourne la langue courante"""
        return self.current_language

    def get_supported_languages(self):
        """Retourne les langues supportées"""
        return self.supported_languages.copy()

    def is_language_supported(self, language_code):
        """Vérifie si une langue est supportée"""
        return language_code in self.supported_languages

    def get_language_name(self, code=None):
        """Retourne le nom de la langue"""
        if code is None:
            code = self.current_language
        return self.supported_languages.get(code, "Inconnu")

    def map_system_language(self, system_code):
        """Mappe un code système vers nos langues supportées"""
        if not system_code:
            return 'fr'
        
        # Mapping simple
        mapping = {
            'fr': 'fr', 'fr_FR': 'fr', 'fr_CA': 'fr', 'french': 'fr',
            'en': 'en', 'en_US': 'en', 'en_GB': 'en', 'english': 'en',
            'de': 'de', 'de_DE': 'de', 'de_AT': 'de', 'german': 'de'
        }
        
        # Essai direct
        mapped = mapping.get(system_code.lower())
        if mapped and mapped in self.supported_languages:
            return mapped
        
        # Essai code court
        short_code = system_code.split('_')[0].split('-')[0].lower()
        mapped = mapping.get(short_code)
        if mapped and mapped in self.supported_languages:
            return mapped
        
        # Fallback français
        return 'fr'

    def apply_system_language(self):
        """Applique automatiquement la langue du système"""
        try:
            # Import tardif pour éviter les dépendances circulaires
            from .language_manager import SystemLanguageDetector
            system_lang = SystemLanguageDetector.detect_system_language()
            mapped_lang = self.map_system_language(system_lang)
            
            if self.set_language(mapped_lang):
                self._log_message("INFO", f"Langue système appliquée: {self.get_language_name(mapped_lang)}", category="utils_i18n")
                return True
        except ImportError:
            self._log_message("ATTENTION", "Module language_manager non disponible", category="utils_i18n")
        except Exception as e:
            self._log_message("ATTENTION", f"Erreur application langue système: {e}", category="utils_i18n")
        
        return False

    def _get_default_translations(self):
        """
        Retourne les traductions par défaut en chargeant les modules de langue
        Structure simplifiée avec seulement les langues principales
        """
        translations = {}
        
        # Charger chaque langue depuis son module
        for lang_code in self.supported_languages.keys():
            try:
                # Import dynamique du module de langue avec gestion d'erreur
                lang_module = None
                
                # Essayer différentes méthodes d'import
                try:
                    lang_module = __import__(f'utils.{lang_code}', fromlist=[lang_code])
                except ImportError:
                    try:
                        # Import direct si utils n'est pas un package
                        lang_module = __import__(lang_code)
                    except ImportError:
                        self._log_message("ATTENTION", f"Impossible d'importer le module {lang_code}", category="utils_i18n")
                        continue
                
                # Récupérer les traductions depuis le module
                if lang_module and hasattr(lang_module, 'TRANSLATIONS'):
                    translations[lang_code] = lang_module.TRANSLATIONS
                    self._log_message("INFO", f"Traductions {lang_code} chargées depuis le module", category="utils_i18n")
                else:
                    self._log_message("ATTENTION", f"Module {lang_code} sans attribut TRANSLATIONS", category="utils_i18n")
                    translations[lang_code] = self._get_fallback_translation(lang_code)
                    
            except Exception as e:
                self._log_message("ERREUR", f"Erreur lors du chargement de {lang_code}: {e}", category="utils_i18n")
                translations[lang_code] = self._get_fallback_translation(lang_code)
        
        # S'assurer qu'au moins le français est disponible
        if 'fr' not in translations:
            translations['fr'] = self._get_fallback_translation('fr')
        
        return translations

    def _get_fallback_translation(self, lang_code):
        """Retourne une traduction de fallback minimale"""
        fallback_texts = {
            'fr': {
                "window": {"title": "🎮 {version}"},
                "buttons": {"extract": "Extraire", "close": "Fermer", "help": "Aide"},
                "errors": {"general_error": "Erreur: {error}"},
                "status": {"ready": "Prêt", "no_file": "Aucun fichier chargé"}
            },
            'en': {
                "window": {"title": "🎮 {version}"},
                "buttons": {"extract": "Extract", "close": "Close", "help": "Help"},
                "errors": {"general_error": "Error: {error}"},
                "status": {"ready": "Ready", "no_file": "No file loaded"}
            },
            'de': {
                "window": {"title": "🎮 {version}"},
                "buttons": {"extract": "Extrahieren", "close": "Schließen", "help": "Hilfe"},
                "errors": {"general_error": "Fehler: {error}"},
                "status": {"ready": "Bereit", "no_file": "Keine Datei geladen"}
            }
        }
        return fallback_texts.get(lang_code, fallback_texts['fr'])

    def reload_translations(self):
        """Recharge les traductions depuis les modules (utile pour le développement)"""
        try:
            # Recharger les modules de langue
            import importlib
            
            for lang_code in self.supported_languages.keys():
                module_name = f'utils.{lang_code}'
                if module_name in sys.modules:
                    importlib.reload(sys.modules[module_name])
            
            # Recharger les traductions
            self.translations = self._get_default_translations()
            self.save_translations()
            self._log_message("INFO", "Traductions rechargées depuis les modules", category="utils_i18n")
            return True
            
        except Exception as e:
            self._log_message("ERREUR", f"Erreur lors du rechargement des traductions: {e}", category="utils_i18n")
            return False

    def get_language_stats(self):
        """Retourne des statistiques sur les langues"""
        return {
            'current_language': self.current_language,
            'current_language_name': self.get_language_name(),
            'total_languages': len(self.supported_languages),
            'available_languages': self.supported_languages.copy(),
            'loaded_translations': list(self.translations.keys()),
            'config_file': self.language_file
        }


# =====================================================================
# CLASSES UTILITAIRES SIMPLIFIÉES
# =====================================================================

class NotificationManager:
    """Gestionnaire de notifications simplifié"""
    
    def __init__(self):
        self.enabled = True
    
    def notify(self, message, notification_type='TOAST', **kwargs):
        """Affiche une notification simple"""
        try:
            # Pour l'instant, utiliser print comme fallback
            prefix = {
                'TOAST': '💬',
                'INFO': 'ℹ️',
                'WARNING': '⚠️',
                'ERROR': '❌',
                'SUCCESS': '✅'
            }.get(notification_type, '📢')
            
            return True
        except Exception:
            return False


# =====================================================================
# INSTANCES GLOBALES
# =====================================================================

# Instance globale
i18n = I18nManager()

# Instance de notification
notification_manager = NotificationManager()

def _(key, **kwargs):
    """Fonction de traduction simplifiée"""
    return i18n.get_text(key, **kwargs)

def setup_i18n_in_main(main_app):
    """Configure l'i18n dans l'application principale"""
    try:
        main_app.i18n = i18n
        
        def change_language(language_code):
            if i18n.set_language(language_code):
                update_interface_language(main_app)
                return True
            return False
        
        main_app.change_language = change_language
        
    except Exception as e:
        pass

def update_interface_language(app):
    """Met à jour l'interface selon la langue actuelle"""
    try:
        if hasattr(app, 'main_window') and hasattr(app.main_window, 'update_language'):
            app.main_window.update_language()
    except Exception as e:
        pass

# Export des principales fonctions
__all__ = [
    'i18n', '_', 'I18nManager', 'NotificationManager', 'notification_manager',
    'setup_i18n_in_main', 'update_interface_language'
]