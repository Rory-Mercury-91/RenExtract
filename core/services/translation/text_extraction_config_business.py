# core/business/text_extraction_config_business.py
# Logique métier pour la configuration d'extraction de textes oubliés
# Refactorisé depuis extract_ui_characters.py - VERSION COMPLÈTE
# AVEC EXCLUSIONS SYSTÈME CODÉES EN DUR

"""
Module métier pour l'onglet 3 - Configuration extraction de textes
- Validation des paramètres d'extraction
- Gestion des langues disponibles
- Configuration des modes de détection
- Gestion des exclusions de fichiers (avec exclusions système automatiques)
- Configuration des patterns d'extraction
- Validation des projets Ren'Py
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Set, Optional, Any, Tuple
from datetime import datetime
from infrastructure.logging.logging import log_message


class TextExtractionConfigBusiness:
    """Logique métier pour la configuration d'extraction de textes"""
    
    def __init__(self):
        """Initialise le module de configuration d'extraction"""
        # Exclusions par défaut (fichiers système Ren'Py)
        self.default_exclusions = [
            'common.rpy'      # Fichier système Ren'Py
        ]
        
        # NOUVEAU: Exclusions système (fichiers générés par ton système)
        # Ces fichiers sont TOUJOURS exclus automatiquement
        self.system_generated_exclusions = [
            '99_Z_Console.rpy',              # Console développeur
            '99_Z_ScreenPreferences.rpy',    # Fichier unifié (sélecteur langue + polices + textbox)
            '99_Z_FontSystem.rpy'            # Polices GUI individuelles
        ]
        
        log_message("INFO", f"TextExtractionConfigBusiness initialisé - {len(self.system_generated_exclusions)} exclusions système", category="extraction_config")
    
    @staticmethod
    def _safe_collect_files(base_dir: str, pattern: str) -> List[str]:
        """
        Retourne la liste des fichiers correspondant au motif en gérant correctement
        les chemins contenant des caractères spéciaux comme [ ] qui perturbent glob().
        """
        try:
            base_path = Path(base_dir)
            if not base_path.exists():
                return []
            return [str(path) for path in base_path.rglob(pattern)]
        except Exception as e:
            log_message("ATTENTION", f"Collecte de fichiers échouée dans {base_dir} ({pattern}) : {e}", category="extraction_config")
            return []

    def get_combined_exclusions(self, user_exclusions: List[str]) -> List[str]:
        """
        Combine les exclusions utilisateur avec les exclusions système obligatoires
        
        Args:
            user_exclusions (List[str]): Exclusions définies par l'utilisateur
            
        Returns:
            List[str]: Liste complète des exclusions (utilisateur + système)
        """
        # Combiner et dédupliquer
        all_exclusions = list(set(user_exclusions + self.system_generated_exclusions))
        
        log_message("DEBUG", f"Exclusions combinées: {len(user_exclusions)} utilisateur + {len(self.system_generated_exclusions)} système = {len(all_exclusions)} total", category="extraction_config")
        
        return sorted(all_exclusions)  # Trier pour cohérence
    
    def detect_available_languages(self, project_path: str) -> Dict[str, Any]:
        """
        Détecte les langues disponibles dans un projet Ren'Py
        
        Args:
            project_path (str): Chemin vers le projet Ren'Py
            
        Returns:
            Dict contenant les langues détectées et leurs informations
        """
        result = {
            'success': False,
            'languages': [],
            'errors': [],
            'project_info': {}
        }
        
        try:
            if not project_path or not os.path.exists(project_path):
                result['errors'].append("Chemin de projet invalide")
                return result
            
            game_dir = os.path.join(project_path, "game")
            tl_dir = os.path.join(game_dir, "tl")
            
            # Informations sur le projet
            result['project_info'] = {
                'project_name': os.path.basename(project_path),
                'has_game_folder': os.path.isdir(game_dir),
                'has_tl_folder': os.path.isdir(tl_dir),
                'game_rpy_count': 0
            }
            
            # Compter les fichiers .rpy dans game
            if result['project_info']['has_game_folder']:
                rpy_files = self._safe_collect_files(game_dir, "*.rpy")
                # Exclure le dossier tl du comptage
                rpy_files = [f for f in rpy_files if 'tl' not in Path(f).parts]
                result['project_info']['game_rpy_count'] = len(rpy_files)
            
            if not result['project_info']['has_tl_folder']:
                result['errors'].append("Aucun dossier tl/ trouvé dans le projet")
                return result
            
            # Scanner les langues disponibles
            for item in os.listdir(tl_dir):
                lang_path = os.path.join(tl_dir, item)
                if os.path.isdir(lang_path) and item.lower() != 'none':
                    
                    # Analyser cette langue
                    lang_info = self._analyze_language_folder(item, lang_path)
                    if lang_info['file_count'] > 0:  # Seulement si il y a des fichiers
                        result['languages'].append(lang_info)
            
            # Trier par nom
            result['languages'].sort(key=lambda x: x['name'])
            result['success'] = True
            
            log_message("INFO", f"Langues détectées: {len(result['languages'])}", category="extraction_config")
            
        except Exception as e:
            error_msg = f"Erreur détection langues: {e}"
            result['errors'].append(error_msg)
            log_message("ERREUR", error_msg, category="extraction_config")
        
        return result
    
    def _analyze_language_folder(self, lang_name: str, lang_path: str) -> Dict[str, Any]:
        """
        Analyse un dossier de langue spécifique
        
        Args:
            lang_name (str): Nom de la langue
            lang_path (str): Chemin vers le dossier de langue
            
        Returns:
            Dict avec les informations de la langue
        """
        lang_info = {
            'name': lang_name,
            'path': lang_path,
            'file_count': 0,
            'total_lines': 0,
            'translation_blocks': 0,
            'last_modified': None,
            'estimated_completeness': 0.0
        }
        
        try:
            # Compter les fichiers .rpy
            rpy_files = self._safe_collect_files(lang_path, "*.rpy")
            lang_info['file_count'] = len(rpy_files)
            
            if rpy_files:
                # Analyser quelques fichiers pour estimer la complétude
                total_lines = 0
                translation_blocks = 0
                last_mod_time = 0
                
                for rpy_file in rpy_files[:10]:  # Limiter à 10 fichiers pour performance
                    try:
                        with open(rpy_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            lines = content.split('\n')
                            total_lines += len(lines)
                            
                            # Compter les blocs translate
                            translation_blocks += len(re.findall(r'translate\s+\w+\s+\w+:', content))
                        
                        # Date de modification
                        mod_time = os.path.getmtime(rpy_file)
                        if mod_time > last_mod_time:
                            last_mod_time = mod_time
                            
                    except Exception:
                        continue
                
                lang_info['total_lines'] = total_lines
                lang_info['translation_blocks'] = translation_blocks
                
                if last_mod_time > 0:
                    lang_info['last_modified'] = datetime.fromtimestamp(last_mod_time).strftime("%Y-%m-%d")
                
                # Estimation de complétude basique
                if translation_blocks > 0:
                    # Plus de blocs = plus complet (estimation grossière)
                    lang_info['estimated_completeness'] = min(100.0, (translation_blocks / 50) * 100)
            
        except Exception as e:
            log_message("DEBUG", f"Erreur analyse langue {lang_name}: {e}", category="extraction_config")
        
        return lang_info
    
    def analyze_existing_translations(self, tl_folder: str) -> Set[str]:
        """
        Analyse le dossier tl pour identifier les textes déjà traduits
        Migré depuis OptimizedTextExtractor._analyze_existing_translations
        
        Args:
            tl_folder (str): Chemin vers le dossier de traductions
            
        Returns:
            Set[str]: Ensemble des textes déjà traduits
        """
        existing_translations = set()
        
        try:
            log_message("INFO", f"Analyse du dossier tl: {tl_folder}", category="extraction_config")
            
            if not tl_folder or not os.path.exists(tl_folder):
                log_message("INFO", "Dossier tl vide ou inexistant", category="extraction_config")
                return existing_translations
            
            # Patterns pour détecter les textes déjà traduits
            tl_old_double_pattern = re.compile(r'old\s+"([^"\\]*(?:\\.[^"\\]*)*)"')
            tl_old_single_pattern = re.compile(r"old\s+'([^'\\]*(?:\\.[^'\\]*)*)'")
            i18n_double_pattern = re.compile(r'__?\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"')
            i18n_single_pattern = re.compile(r"__?\(\s*'([^'\\]*(?:\\.[^'\\]*)*)'")            
            rpy_files = self._safe_collect_files(tl_folder, "*.rpy")
            
            if not rpy_files:
                log_message("INFO", "Dossier tl vide ou inexistant", category="extraction_config")
                return existing_translations
            
            translations_count = 0
            
            for filepath in rpy_files:
                try:
                    with open(filepath, encoding="utf-8") as f:
                        content = f.read()
                        
                        # NOUVEAU
                        for match in tl_old_double_pattern.finditer(content):
                            text = match.group(1).strip()
                            if text:
                                existing_translations.add(text)

                        for match in tl_old_single_pattern.finditer(content):
                            text = match.group(1).strip()
                            if text:
                                existing_translations.add(text)

                        for match in i18n_double_pattern.finditer(content):
                            text = match.group(1).strip()
                            if text:
                                existing_translations.add(text)

                        for match in i18n_single_pattern.finditer(content):
                            text = match.group(1).strip()
                            if text:
                                existing_translations.add(text)
                                
                except Exception as e:
                    log_message("ATTENTION", f"Erreur lecture fichier tl {os.path.basename(filepath)}: {e}", category="extraction_config")
                    continue
            
            log_message("INFO", f"Anti-doublons activé: {len(existing_translations)} textes uniques détectés", category="extraction_config")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur analyse traductions existantes: {e}", category="extraction_config")
        
        return existing_translations
    
    def validate_extraction_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valide une configuration d'extraction
        
        Args:
            config: Configuration à valider contenant:
                - project_path: str
                - selected_language: str  
                - detection_mode: str
                - excluded_files: List[str]
                
        Returns:
            Dict avec résultat de validation
        """
        result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'recommendations': []
        }
        
        try:
            # Validation du projet
            project_path = config.get('project_path')
            if not project_path:
                result['valid'] = False
                result['errors'].append("Chemin de projet manquant")
                return result
            
            if not os.path.exists(project_path):
                result['valid'] = False
                result['errors'].append("Le projet spécifié n'existe pas")
                return result
            
            # Validation du dossier game
            game_folder = os.path.join(project_path, "game")
            if not os.path.exists(game_folder):
                result['valid'] = False
                result['errors'].append("Le projet ne contient pas de dossier 'game'")
                return result
            
            # Vérifier qu'il y a des fichiers .rpy dans game
            rpy_files = self._safe_collect_files(game_folder, "*.rpy")
            rpy_files = [f for f in rpy_files if 'tl' not in Path(f).parts]
            
            if not rpy_files:
                result['warnings'].append("Aucun fichier .rpy trouvé dans le dossier game")
            elif len(rpy_files) < 5:
                result['warnings'].append(f"Peu de fichiers .rpy trouvés ({len(rpy_files)})")
            
            # Validation de la langue sélectionnée
            selected_language = config.get('selected_language')
            if not selected_language:
                result['valid'] = False
                result['errors'].append("Aucune langue de référence sélectionnée")
                return result
            
            # Vérifier que la langue existe
            tl_language_folder = os.path.join(game_folder, "tl", selected_language)
            if not os.path.exists(tl_language_folder):
                result['valid'] = False
                result['errors'].append(f"Le dossier de langue '{selected_language}' n'existe pas")
                return result
            
            # Vérifier qu'il y a des traductions dans cette langue
            lang_rpy_files = self._safe_collect_files(tl_language_folder, "*.rpy")
            if not lang_rpy_files:
                result['warnings'].append(f"Aucun fichier .rpy trouvé dans la langue '{selected_language}'")
            
            # Validation du mode de détection
            detection_mode = config.get('detection_mode', 'optimized')
            if detection_mode not in ['simple', 'optimized']:
                result['warnings'].append(f"Mode de détection '{detection_mode}' non reconnu, utilisation du mode optimisé")
            
            # Validation des exclusions
            excluded_files = config.get('excluded_files', [])
            if excluded_files:
                for excluded_file in excluded_files:
                    if not excluded_file.endswith('.rpy'):
                        result['warnings'].append(f"Fichier d'exclusion '{excluded_file}' sans extension .rpy")
            
            # Recommandations
            if len(rpy_files) > 100:
                result['recommendations'].append("Projet volumineux détecté - l'analyse peut prendre quelques minutes")
            
            if len(lang_rpy_files) > 50:
                result['recommendations'].append("Beaucoup de traductions existantes - l'anti-doublon sera efficace")
            
            # Information sur les exclusions système
            system_exclusions_count = len(self.system_generated_exclusions)
            result['recommendations'].append(f"{system_exclusions_count} fichiers système automatiquement exclus")
            
            log_message("INFO", f"Configuration validée: {len(result['errors'])} erreurs, {len(result['warnings'])} avertissements", category="extraction_config")
            
        except Exception as e:
            result['valid'] = False
            result['errors'].append(f"Erreur validation configuration: {e}")
            log_message("ERREUR", f"Erreur validate_extraction_config: {e}", category="extraction_config")
        
        return result
    
    def prepare_extraction_parameters(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prépare les paramètres finaux pour l'extraction
        AVEC APPLICATION AUTOMATIQUE DES EXCLUSIONS SYSTÈME
        
        Args:
            config: Configuration validée
                        
        Returns:
            Dict avec paramètres prêts pour l'extraction
        """
        params = {
            'game_folder': None,
            'tl_folder': None,
            'detection_mode': 'optimized',
            'extractor_config': {},
            'excluded_files': [],
            'anti_duplicate_active': False,
            'existing_translations': set()
        }
        
        try:
            project_path = config['project_path']
            selected_language = config['selected_language']
            
            # Chemins finaux
            params['game_folder'] = os.path.join(project_path, "game")
            params['tl_folder'] = os.path.join(params['game_folder'], "tl", selected_language)
            
            # Mode de détection
            params['detection_mode'] = config.get('detection_mode', 'optimized')
            
            # Configuration de l'extracteur
            params['extractor_config'] = self._prepare_extractor_config(params['detection_mode'])
            
            # NOUVEAU: Traitement des exclusions avec système automatique
            excluded_files_raw = config.get('excluded_files', [])
            if isinstance(excluded_files_raw, str):
                # Si c'est une string (depuis l'interface), séparer par virgules
                user_exclusions = [f.strip() for f in excluded_files_raw.split(',') if f.strip()]
            else:
                # Si c'est déjà une liste
                user_exclusions = excluded_files_raw
            
            # Combiner avec les exclusions système
            params['excluded_files'] = self.get_combined_exclusions(user_exclusions)
            
            # Anti-duplicate actif si dossier tl existe
            params['anti_duplicate_active'] = os.path.exists(params['tl_folder'])
            
            # Pré-charger les traductions existantes
            if params['anti_duplicate_active']:
                params['existing_translations'] = self.analyze_existing_translations(params['tl_folder'])
            
            log_message("INFO", f"Paramètres d'extraction préparés - Mode: {params['detection_mode']}, Exclusions: {len(params['excluded_files'])}, Anti-duplicate: {params['anti_duplicate_active']}", category="extraction_config")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur prepare_extraction_parameters: {e}", category="extraction_config")
        
        return params
    
    def _prepare_extractor_config(self, detection_mode: str) -> Dict[str, Any]:
        """
        Prépare la configuration de l'extracteur (mode optimisé uniquement)
        
        Args:
            detection_mode (str): Mode de détection (ignoré, toujours optimisé)
            
        Returns:
            Dict avec configuration de l'extracteur
        """
        config = {
            'patterns_enabled': [
                'character_def',
                'input_calls',
                'notify_calls', 
                'show_text',
                'textbutton',
                'textbutton_single',
                'text_element'
            ],
            'confidence_levels': {},
            'auto_safe_patterns': [
                'character_def',
                'input_calls',
                'notify_calls',
                'show_text'
            ],
            'manual_check_patterns': [
                'textbutton',
                'textbutton_single',
                'text_element'
            ]
        }
        
        return config
    
    def get_detection_mode_info(self) -> Dict[str, Dict[str, Any]]:
        """
        Retourne les informations sur le mode de détection (optimisé uniquement)
        
        Returns:
            Dict avec détails du mode
        """
        return {
            'optimized': {
                'name': 'Optimisé',
                'description': 'Tous les patterns ciblés avancés avec classification intelligente',
                'patterns': ['Character', 'input', 'notify', 'textbutton', 'text elements', 'show text'],
                'confidence': 95,
                'speed': 'Modéré',
                'completeness': 'Complète',
                'recommended_for': 'Extraction complète avec classification intelligente'
            }
        }
    
    def get_exclusion_recommendations(self) -> List[str]:
        """
        Retourne les recommandations d'exclusions par défaut
        SANS les exclusions système (car elles sont automatiques)
        
        Returns:
            Liste des fichiers recommandés pour exclusion
        """
        return self.default_exclusions.copy()
    
    def get_system_exclusions(self) -> List[str]:
        """
        Retourne la liste des exclusions système (automatiques)
        
        Returns:
            Liste des fichiers toujours exclus
        """
        return self.system_generated_exclusions.copy()
    
    def get_all_exclusions_info(self) -> Dict[str, List[str]]:
        """
        Retourne toutes les informations sur les exclusions
        
        Returns:
            Dict avec exclusions par catégorie
        """
        return {
            'default_exclusions': self.get_exclusion_recommendations(),
            'system_exclusions': self.get_system_exclusions(),
            'total_automatic_exclusions': len(self.default_exclusions) + len(self.system_generated_exclusions)
        }
    
    def validate_project_structure(self, project_path: str) -> Dict[str, Any]:
        """
        Valide la structure d'un projet Ren'Py pour l'extraction
        
        Args:
            project_path (str): Chemin vers le projet
            
        Returns:
            Dict avec résultat de validation
        """
        result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'project_info': {},
            'structure_analysis': {}
        }
        
        try:
            if not project_path or not os.path.exists(project_path):
                result['valid'] = False
                result['errors'].append("Chemin de projet invalide")
                return result
            
            # Analyse de la structure
            game_folder = os.path.join(project_path, "game")
            tl_folder = os.path.join(game_folder, "tl")
            
            result['project_info'] = {
                'project_name': os.path.basename(project_path),
                'project_path': project_path,
                'has_game_folder': os.path.isdir(game_folder),
                'has_tl_folder': os.path.isdir(tl_folder)
            }
            
            # Validation dossier game
            if not result['project_info']['has_game_folder']:
                result['valid'] = False
                result['errors'].append("Le projet ne contient pas de dossier 'game'")
                return result
            
            # Analyse des fichiers .rpy
            rpy_files = self._safe_collect_files(game_folder, "*.rpy")
            game_rpy_files = [f for f in rpy_files if 'tl' not in Path(f).parts]
            
            result['structure_analysis'] = {
                'total_rpy_files': len(rpy_files),
                'game_rpy_files': len(game_rpy_files),
                'has_translations': result['project_info']['has_tl_folder']
            }
            
            if not game_rpy_files:
                result['warnings'].append("Aucun fichier .rpy trouvé dans le dossier game")
            elif len(game_rpy_files) < 3:
                result['warnings'].append(f"Très peu de fichiers .rpy trouvés ({len(game_rpy_files)})")
            
            # Analyse du dossier tl si présent
            if result['project_info']['has_tl_folder']:
                languages = []
                for item in os.listdir(tl_folder):
                    lang_path = os.path.join(tl_folder, item)
                    if os.path.isdir(lang_path) and item.lower() != 'none':
                        lang_rpy_files = self._safe_collect_files(lang_path, "*.rpy")
                        if lang_rpy_files:
                            languages.append(item)
                
                result['structure_analysis']['available_languages'] = languages
                
                if not languages:
                    result['warnings'].append("Dossier tl présent mais aucune langue avec fichiers .rpy trouvée")
            else:
                result['warnings'].append("Aucun dossier tl trouvé - première extraction")
            
            log_message("INFO", f"Structure projet validée: {result['project_info']['project_name']}", category="extraction_config")
            
        except Exception as e:
            result['valid'] = False
            result['errors'].append(f"Erreur validation structure: {e}")
            log_message("ERREUR", f"Erreur validate_project_structure: {e}", category="extraction_config")
        
        return result


# Fonctions utilitaires pour l'interface et la compatibilité

def validate_project_for_extraction(project_path: str) -> Dict[str, Any]:
    """
    Fonction utilitaire pour valider un projet pour l'extraction
    
    Args:
        project_path (str): Chemin vers le projet
        
    Returns:
        Dict avec résultat de validation
    """
    business = TextExtractionConfigBusiness()
    return business.validate_project_structure(project_path)


def get_exclusion_recommendations() -> List[str]:
    """
    Retourne les recommandations d'exclusions par défaut
    
    Returns:
        Liste des fichiers recommandés pour exclusion
    """
    business = TextExtractionConfigBusiness()
    return business.get_exclusion_recommendations()


def get_system_exclusions() -> List[str]:
    """
    Retourne les exclusions système automatiques
    
    Returns:
        Liste des fichiers système toujours exclus
    """
    business = TextExtractionConfigBusiness()
    return business.get_system_exclusions()


def create_extraction_context(project_path: str, selected_language: str) -> Dict[str, Any]:
    """
    Fonction utilitaire pour créer un contexte d'extraction
    
    Args:
        project_path (str): Chemin vers le projet
        selected_language (str): Langue sélectionnée
        
    Returns:
        Dict avec contexte d'extraction
    """
    context = {
        'project_path': project_path,
        'project_name': os.path.basename(project_path),
        'selected_language': selected_language,
        'game_folder': os.path.join(project_path, "game"),
        'tl_folder': os.path.join(project_path, "game", "tl", selected_language),
        'timestamp': datetime.now().isoformat()
    }
    
    return context


def prepare_extraction_config_from_interface(main_interface) -> Dict[str, Any]:
    """
    Prépare une configuration d'extraction depuis l'interface principale
    VERSION MISE À JOUR pour la nouvelle interface avec combobox
    
    Args:
        main_interface: Instance de l'interface principale
        
    Returns:
        Dict avec configuration d'extraction
    """
    try:
        # NOUVEAU: Récupérer la langue depuis la combobox (nouvelle interface)
        selected_language = None
        if hasattr(main_interface, 'extraction_selected_language_var'):
            # Nouvelle interface avec combobox
            selected_language = main_interface.extraction_selected_language_var.get()
        elif hasattr(main_interface, 'extraction_language_vars'):
            # Ancienne interface avec checkboxes (fallback)
            for lang_name, var in main_interface.extraction_language_vars.items():
                if var.get():
                    selected_language = lang_name
                    break
        
        config = {
            'project_path': getattr(main_interface, 'current_project_path', None),
            'selected_language': selected_language,
            'detection_mode': getattr(main_interface, 'extraction_detection_mode_var', None),
            'excluded_files': getattr(main_interface, 'extraction_excluded_files_var', None)
        }
        
        # Convertir les variables tkinter en valeurs
        if hasattr(config['detection_mode'], 'get'):
            config['detection_mode'] = config['detection_mode'].get()
        if hasattr(config['excluded_files'], 'get'):
            config['excluded_files'] = config['excluded_files'].get()
        
        return config
        
    except Exception as e:
        log_message("ERREUR", f"Erreur préparation config depuis interface: {e}", category="extraction_config")
        return {
            'project_path': None,
            'selected_language': None,
            'detection_mode': 'optimized',
            'excluded_files': []
        }


# Exports pour compatibilité
__all__ = [
    'TextExtractionConfigBusiness',
    'validate_project_for_extraction',
    'get_exclusion_recommendations',
    'get_system_exclusions',
    'create_extraction_context',
    'prepare_extraction_config_from_interface'
]