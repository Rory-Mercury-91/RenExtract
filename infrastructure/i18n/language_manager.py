# utils/language_manager.py - GESTIONNAIRE DE LANGUE UNIFIÉ
"""
Gestionnaire de langue unifié pour RenExtract
Fusionne language_detector.py et language_manager.py
Détection Windows uniquement avec support fr/en/de
"""

import os
import json
import sys
from pathlib import Path
from infrastructure.logging.logging import log_message
from infrastructure.config.config import config_manager

class UnifiedLanguageManager:
    """Gestionnaire de langue unifié avec détection Windows"""
    
    def __init__(self):
        self.supported_languages = {
            'fr': 'Français',
            'en': 'English', 
            'de': 'Deutsch'
        }
        
        try:
            from infrastructure.config.constants import FOLDERS
            self.language_file = Path(FOLDERS["configs"]) / "languages.json"
        except ImportError:
            self.language_file = Path("04_Configs") / "languages.json"
    
    def detect_system_language(self):
        """Détecte la langue Windows via le registre (fr/en/de uniquement)"""
        try:
            import winreg
            
            # Lire le registre Windows
            key_path = r"Control Panel\International"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                locale_name, _ = winreg.QueryValueEx(key, 'LocaleName')
                
                # Mapping des codes Windows vers nos langues supportées
                windows_mapping = {
                    'fr-FR': 'fr', 'fr-CA': 'fr', 'fr-BE': 'fr', 'fr-CH': 'fr',
                    'en-US': 'en', 'en-GB': 'en', 'en-AU': 'en', 'en-CA': 'en',
                    'de-DE': 'de', 'de-AT': 'de', 'de-CH': 'de'
                }
                
                # Vérifier mapping direct
                detected_lang = windows_mapping.get(locale_name)
                if detected_lang:
                    log_message("INFO", f"Langue détectée: {locale_name} → {detected_lang}", category="utils_language")
                    return detected_lang
                
                # Fallback sur le code court (fr, en, de)
                short_code = locale_name.split('-')[0].lower()
                if short_code in ['fr', 'en', 'de']:
                    log_message("INFO", f"Langue détectée (code court): {locale_name} → {short_code}", category="utils_language")
                    return short_code
                
                # Aucune langue supportée
                log_message("INFO", f"Langue non supportée: {locale_name} → fallback français", category="utils_language")
                return 'fr'
                
        except Exception as e:
            log_message("ERREUR", f"Erreur détection langue Windows: {e}", category="utils_language")
            return 'fr'  # Fallback français
    
    def change_language(self, language_code):
        """Change la langue courante"""
        try:
            if language_code not in self.supported_languages:
                log_message("ATTENTION", f"Langue non supportée: {language_code}", category="utils_language")
                return False
            
            # I18n désactivé dans cette version
            # try:
            #     from infrastructure.i18n.i18n import i18n
            #     success = i18n.set_language(language_code)
            #     if not success:
            #         return False
            # except ImportError:
            #     log_message("INFO", "Module i18n non disponible, passage de la mise à jour", category="utils_language")
            
            # Sauvegarder la préférence
            config_manager.set('language', language_code)
            
            log_message("INFO", f"Langue changée vers: {self.supported_languages[language_code]}", category="utils_language")
            return True
                
        except Exception as e:
            log_message("ERREUR", f"Erreur changement langue: {e}", category="utils_language")
            return False
    
    def change_language_with_folders(self, language_code):
        """Change la langue ET met à jour les dossiers"""
        try:
            # Vérifier que la langue est supportée
            if language_code not in self.supported_languages:
                log_message("ATTENTION", f"Langue non supportée: {language_code}", category="utils_language")
                return False
            
            # I18n désactivé dans cette version
            # try:
            #     from infrastructure.i18n.i18n import i18n
            #     i18n.set_language(language_code)
            # except ImportError:
            #     log_message("INFO", "Module i18n non disponible", category="utils_language")
            
            # Changer la langue dans la config
            config_manager.set('language', language_code)
            
            # Mettre à jour les dossiers si disponible
            try:
                from infrastructure.config.constants import set_folder_language
                folder_success = set_folder_language(language_code)
            except ImportError:
                log_message("INFO", "Fonction set_folder_language non disponible", category="utils_language")
                folder_success = True
            
            if folder_success:
                log_message("INFO", f"Langue et dossiers changés vers: {language_code}", category="utils_language")
                return True
            else:
                log_message("ERREUR", f"Erreur mise à jour dossiers pour: {language_code}", category="utils_language")
                return False
                
        except Exception as e:
            log_message("ERREUR", f"Erreur changement langue avec dossiers: {e}", category="utils_language")
            return False
    
    def setup_auto_language_detection(self):
        """Configure la détection automatique au premier lancement AVEC dossiers"""
        try:
            # Vérifier si une langue est déjà configurée
            current_language = config_manager.get('language')
            if current_language and current_language != 'fr':
                log_message("INFO", f"Langue déjà configurée: {current_language}", category="utils_language")
                
                # S'assurer que les dossiers correspondent
                try:
                    from infrastructure.config.constants import set_folder_language
                    set_folder_language(current_language)
                except ImportError:
                    pass
                return current_language
            
            # Détecter la langue système
            detected_language = self.detect_system_language()
            
            # Appliquer avec les dossiers
            success = self.change_language_with_folders(detected_language)
            
            if success:
                log_message("INFO", f"Langue auto-détectée et dossiers configurés: {detected_language}", category="utils_language")
                return detected_language
            else:
                # Fallback
                self.change_language_with_folders('fr')
                return 'fr'
                
        except Exception as e:
            log_message("ERREUR", f"Erreur auto-détection langue: {e}", category="utils_language")
            try:
                self.change_language_with_folders('fr')
            except:
                pass
            return 'fr'


# =====================================================================
# CLASSE DE COMPATIBILITÉ (pour les anciens imports)
# =====================================================================

class SystemLanguageDetector:
    """Classe de compatibilité pour les anciens imports"""
    
    _manager = UnifiedLanguageManager()
    
    @classmethod
    def detect_system_language(cls):
        """Détecte la langue système"""
        return cls._manager.detect_system_language()
    
    @classmethod
    def setup_auto_language_detection(cls):
        """Configure la détection automatique"""
        return cls._manager.setup_auto_language_detection()
    
    @classmethod
    def change_language_with_folders(cls, language_code):
        """Change la langue avec dossiers"""
        return cls._manager.change_language_with_folders(language_code)


class LanguageManager:
    """Classe de compatibilité pour les anciens imports"""
    
    def __init__(self):
        self._manager = UnifiedLanguageManager()
        self.supported_languages = self._manager.supported_languages
    
    def change_language(self, language_code):
        """Change la langue courante"""
        return self._manager.change_language(language_code)
    
    def detect_system_language(self):
        """Détecte la langue système"""
        detected = self._manager.detect_system_language()
        return detected, detected  # Retourne (detected, mapped) pour compatibilité


# =====================================================================
# INSTANCE GLOBALE
# =====================================================================

# Instance globale unifiée
unified_language_manager = UnifiedLanguageManager()

# Export des classes principales
__all__ = [
    'UnifiedLanguageManager',
    'SystemLanguageDetector', 
    'LanguageManager',
    'unified_language_manager'
]