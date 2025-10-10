# ui/tutorial/utils.py
"""
Utilitaires pour validation et gestion d'erreurs du système multilingue
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from infrastructure.logging.logging import log_message

class TranslationValidator:
    """Validateur pour les traductions et l'intégrité du système"""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.required_ui_keys = [
            'main_title', 'version', 'tab_summary', 'tab_workflow', 'tab_interface',
            'tab_generator', 'tab_backup', 'tab_tools', 'tab_settings', 'tab_technical',
            'tab_faq', 'click_to_see', 'place_image', 'language', 'french', 'english', 'german'
        ]
        
    def validate_translation_file(self, language: str) -> List[str]:
        """Valide un fichier de traduction spécifique"""
        errors = []
        
        try:
            module_path = self.base_path / 'translations' / f'{language}.py'
            if not module_path.exists():
                errors.append(f"Fichier de traduction manquant: {module_path}")
                return errors
            
            # Import dynamique pour validation
            spec = importlib.util.spec_from_file_location(f"translations_{language}", module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if not hasattr(module, 'TRANSLATIONS'):
                errors.append(f"Dictionnaire TRANSLATIONS manquant dans {language}.py")
                return errors
            
            translations = module.TRANSLATIONS
            
            # Vérifier la structure de base
            if not isinstance(translations, dict):
                errors.append(f"TRANSLATIONS doit être un dictionnaire dans {language}.py")
                return errors
            
            # Vérifier les sections requises
            required_sections = ['ui', 'images', 'tabs', 'meta']
            for section in required_sections:
                if section not in translations:
                    errors.append(f"Section '{section}' manquante dans {language}.py")
            
            # Vérifier les clés UI essentielles
            ui_section = translations.get('ui', {})
            for key in self.required_ui_keys:
                if key not in ui_section:
                    errors.append(f"Clé UI manquante '{key}' dans {language}.py")
            
            # Vérifier les métadonnées
            meta_section = translations.get('meta', {})
            required_meta = ['language_name', 'language_code', 'translation_complete']
            for key in required_meta:
                if key not in meta_section:
                    errors.append(f"Métadonnée manquante '{key}' dans {language}.py")
            
            # Vérifier la cohérence du code langue
            if meta_section.get('language_code') != language:
                errors.append(f"Code langue incohérent dans {language}.py: attendu '{language}', trouvé '{meta_section.get('language_code')}'")
                
        except Exception as e:
            errors.append(f"Erreur lors de la validation de {language}.py: {e}")
        
        return errors
    
    def validate_content_modules(self) -> List[str]:
        """Valide tous les modules de contenu"""
        errors = []
        content_path = self.base_path / 'content'
        
        for tab_num in range(1, 10):
            module_file = content_path / f'tab_{tab_num:02d}.py'
            if not module_file.exists():
                errors.append(f"Module de contenu manquant: {module_file}")
                continue
            
            try:
                # Vérifier que le module a une fonction generate_content
                spec = importlib.util.spec_from_file_location(f"tab_{tab_num:02d}", module_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if not hasattr(module, 'generate_content'):
                    errors.append(f"Fonction 'generate_content' manquante dans {module_file}")
                elif not callable(getattr(module, 'generate_content')):
                    errors.append(f"'generate_content' n'est pas callable dans {module_file}")
                    
            except Exception as e:
                errors.append(f"Erreur lors de la validation de {module_file}: {e}")
        
        return errors
    
    def validate_image_structure(self, images_dir: str) -> List[str]:
        """Valide la structure des images multilingues"""
        errors = []
        
        if not os.path.exists(images_dir):
            errors.append(f"Dossier d'images introuvable: {images_dir}")
            return errors
        
        # Vérifier la structure multilingue
        supported_languages = ['fr', 'en', 'de']
        expected_sections = [
            '01_interface_principale',
            '02_interface_generateur', 
            '03_interface_outils',
            '04_interface_sauvegarde',
            '05_interface_parametres',
            '06_logos'
        ]
        
        for lang in supported_languages:
            lang_dir = os.path.join(images_dir, lang)
            if not os.path.exists(lang_dir):
                errors.append(f"Dossier langue manquant: {lang_dir}")
                continue
            
            for section in expected_sections:
                section_dir = os.path.join(lang_dir, section)
                if not os.path.exists(section_dir):
                    errors.append(f"Section d'images manquante: {section_dir}")
                else:
                    # Compter les images dans cette section
                    images = [f for f in os.listdir(section_dir) 
                             if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
                    if not images:
                        errors.append(f"Aucune image trouvée dans: {section_dir}")
        
        return errors

class PerformanceMonitor:
    """Moniteur de performance pour le système multilingue"""
    
    def __init__(self):
        self.metrics = {}
        self.cache_stats = {
            'translations_loaded': 0,
            'images_cached': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }
    
    def record_translation_load(self, language: str, load_time: float, size: int):
        """Enregistre les métriques de chargement de traduction"""
        self.metrics[f'translation_load_{language}'] = {
            'load_time': load_time,
            'size_bytes': size,
            'timestamp': time.time()
        }
        self.cache_stats['translations_loaded'] += 1
        log_message("DEBUG", f"Traduction {language} chargée en {load_time:.3f}s ({size} bytes)", 
                   category="tutorial_performance")
    
    def record_image_cache(self, cache_key: str, encode_time: float, size: int):
        """Enregistre les métriques de cache d'images"""
        self.metrics[f'image_cache_{cache_key}'] = {
            'encode_time': encode_time,
            'size_bytes': size,
            'timestamp': time.time()
        }
        self.cache_stats['images_cached'] += 1
        log_message("DEBUG", f"Image {cache_key} cachée en {encode_time:.3f}s ({size} bytes)",
                   category="tutorial_performance")
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Génère un rapport de performance"""
        return {
            'cache_stats': self.cache_stats,
            'metrics_count': len(self.metrics),
            'average_translation_load_time': self._calculate_average_load_time(),
            'total_cache_size': self._calculate_total_cache_size()
        }
    
    def _calculate_average_load_time(self) -> float:
        """Calcule le temps moyen de chargement des traductions"""
        translation_metrics = [m for k, m in self.metrics.items() if k.startswith('translation_load_')]
        if not translation_metrics:
            return 0.0
        return sum(m['load_time'] for m in translation_metrics) / len(translation_metrics)
    
    def _calculate_total_cache_size(self) -> int:
        """Calcule la taille totale du cache"""
        return sum(m['size_bytes'] for m in self.metrics.values())

def validate_tutorial_architecture(base_path: Optional[Path] = None) -> Dict[str, Any]:
    """Fonction principale de validation de l'architecture"""
    if base_path is None:
        base_path = Path(__file__).parent
    
    validator = TranslationValidator(base_path)
    validation_report = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'stats': {}
    }
    
    # Validation des traductions
    supported_languages = ['fr', 'en', 'de']
    for lang in supported_languages:
        errors = validator.validate_translation_file(lang)
        if errors:
            validation_report['errors'].extend(errors)
            validation_report['valid'] = False
    
    # Validation des modules de contenu
    content_errors = validator.validate_content_modules()
    if content_errors:
        validation_report['errors'].extend(content_errors)
        validation_report['valid'] = False
    
    # Validation de la structure d'images
    try:
        images_dir = os.path.join(str(base_path.parent.parent.parent), "tutorial_images")
        image_errors = validator.validate_image_structure(images_dir)
        if image_errors:
            validation_report['warnings'].extend(image_errors)  # Images en warning, pas erreur critique
    except Exception as e:
        validation_report['warnings'].append(f"Impossible de valider les images: {e}")
    
    # Statistiques
    validation_report['stats'] = {
        'languages_supported': len(supported_languages),
        'content_modules': 9,
        'total_errors': len(validation_report['errors']),
        'total_warnings': len(validation_report['warnings'])
    }
    
    # Log du résultat
    if validation_report['valid']:
        log_message("INFO", "Architecture tutoriel validée avec succès", category="tutorial_validation")
    else:
        log_message("ERREUR", f"Validation échouée: {len(validation_report['errors'])} erreurs", 
                   category="tutorial_validation")
    
    return validation_report

# Imports nécessaires (ajoutés ici pour éviter les erreurs)
import importlib.util
import time