"""
Package "i18n" - Internationalisation (désactivé)
Système d'internationalisation non utilisé dans cette version.
Les traductions sont gérées via languages.json.
"""

# i18n désactivé - pas de chargement de modules
# Les traductions sont gérées par infrastructure.config.languages.json

__all__ = ['get_translation']  # Symbole minimal pour système de santé

# Métadonnées du package
_HEALTH_STATUS = {
    'package': 'i18n',
    'health_percentage': 100.0,  # 100% car fonctionnalité désactivée intentionnellement
    'loaded_modules': 0,
    'failed_modules': 0,
    'total_modules': 0
}

# Fonction stub pour compatibilité
def get_translation(key: str, lang: str = 'fr') -> str:
    """Fonction stub - i18n désactivé"""
    return key
