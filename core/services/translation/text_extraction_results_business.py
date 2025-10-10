# core/business/text_extraction_results_business.py
# Logique métier pour les résultats d'extraction de textes oubliés
# Refactorisé depuis extract_ui_characters.py - VERSION COMPLÈTE

"""
Module métier pour l'onglet 4 - Résultats extraction de textes
- Classe OptimizedTextExtractor complète avec tous les patterns
- Traitement des résultats d'analyse
- Calcul des statistiques
- Génération de fichiers .rpy
- Gestion des sélections utilisateur
"""

import os
import re
import glob
import threading
from typing import Dict, Set, List, Any, Optional, Pattern
from datetime import datetime
from infrastructure.logging.logging import log_message


class OptimizedTextExtractor:
    """
    Extracteur optimisé avec patterns ciblés pour éviter la sur-détection
    Analyse le dossier tl pour éviter les doublons avec le SDK
    Version améliorée avec nouveaux patterns et gestion des apostrophes
    """
    
    def __init__(self):
        """Initialise l'extracteur optimisé"""
        self.existing_translations = set()  # Textes déjà dans tl/
        self.patterns = self._init_targeted_patterns()
        self.custom_patterns = self._init_custom_patterns()
        
    def _init_targeted_patterns(self) -> Dict[str, Pattern]:
        """Patterns regex corrigés avec gestion séparée des guillemets simples et doubles"""
        return {
            # Pattern pour Character() avec gestion séparée des guillemets
            'character_def_double': re.compile(r'Character\s*\(\s*"(?!persistent\.|store\.|config\.|renpy\.)([^"\\]*(?:\\.[^"\\]*)*)"', re.IGNORECASE),
            'character_def_single': re.compile(r"Character\s*\(\s*'(?!persistent\.|store\.|config\.|renpy\.)([^'\\]*(?:\\.[^'\\]*)*)'", re.IGNORECASE),
            
            # show text avec gestion séparée
            'show_text_double': re.compile(r'show\s+text\s+"([^"\\]*(?:\\.[^"\\]*)*)"', re.IGNORECASE | re.DOTALL),
            'show_text_single': re.compile(r"show\s+text\s+'([^'\\]*(?:\\.[^'\\]*)*)'", re.IGNORECASE | re.DOTALL),
            
            # text elements avec attributs - gestion séparée
            'text_element_with_attrs_double': re.compile(r'text\s+"([^"\\]*(?:\\.[^"\\]*)*)"(?:\s+style|\s+color|\s+xalign|\s+text_align|\s+ypos)', re.IGNORECASE | re.DOTALL),
            'text_element_with_attrs_single': re.compile(r"text\s+'([^'\\]*(?:\\.[^'\\]*)*)'(?:\s+style|\s+color|\s+xalign|\s+text_align|\s+ypos)", re.IGNORECASE | re.DOTALL),
            
            # text simple avec gestion séparée
            'text_element_double': re.compile(r'(?<!#)\btext\s+"([^"\\]*(?:\\.[^"\\]*)*)"(?!\s*=)', re.IGNORECASE | re.DOTALL),
            'text_element_single': re.compile(r"(?<!#)\btext\s+'([^'\\]*(?:\\.[^'\\]*)*)'(?!\s*=)", re.IGNORECASE | re.DOTALL),
            
            # renpy.input avec gestion séparée
            'input_calls_double': re.compile(r'renpy\.input\s*\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"', re.IGNORECASE | re.DOTALL),
            'input_calls_single': re.compile(r"renpy\.input\s*\(\s*'([^'\\]*(?:\\.[^'\\]*)*)'", re.IGNORECASE | re.DOTALL),
            
            # Lignes commentées avec gestion séparée
            'commented_input_double': re.compile(r'#.*renpy\.input\s*\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"', re.IGNORECASE | re.DOTALL),
            'commented_input_single': re.compile(r"#.*renpy\.input\s*\(\s*'([^'\\]*(?:\\.[^'\\]*)*)'", re.IGNORECASE | re.DOTALL),
            
            # notify avec gestion séparée
            'notify_calls_double': re.compile(r'\.notify\s*\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"', re.IGNORECASE | re.DOTALL),
            'notify_calls_single': re.compile(r"\.notify\s*\(\s*'([^'\\]*(?:\\.[^'\\]*)*)'", re.IGNORECASE | re.DOTALL),
            
            # text parameter avec gestion séparée
            'text_param_double': re.compile(r'\btext\s*=\s*"([^"\\]*(?:\\.[^"\\]*)*)"', re.IGNORECASE | re.DOTALL),
            'text_param_single': re.compile(r"\btext\s*=\s*'([^'\\]*(?:\\.[^'\\]*)*)'", re.IGNORECASE | re.DOTALL),
            
            # renpy.notify avec gestion séparée
            'renpy_notify_double': re.compile(r'renpy\.notify\s*\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"', re.IGNORECASE | re.DOTALL),
            'renpy_notify_single': re.compile(r"renpy\.notify\s*\(\s*'([^'\\]*(?:\\.[^'\\]*)*)'", re.IGNORECASE | re.DOTALL),
            
            # activity title avec gestion séparée
            'activity_title_double': re.compile(r'Activity\s*\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"', re.IGNORECASE | re.DOTALL),
            'activity_title_single': re.compile(r"Activity\s*\(\s*'([^'\\]*(?:\\.[^'\\]*)*)'", re.IGNORECASE | re.DOTALL),
            
            # textbutton avec gestion séparée
            'textbutton_double': re.compile(r'textbutton\s+"([^"\\]*(?:\\.[^"\\]*)*)"', re.IGNORECASE | re.DOTALL),
            'textbutton_single': re.compile(r"textbutton\s+'([^'\\]*(?:\\.[^'\\]*)*)'", re.IGNORECASE | re.DOTALL),
            
            # Patterns plus complexes - gardés avec gestion mixte car plus rares
            'activity_description': re.compile(r'Activity\s*\(\s*"[^"\\]*(?:\\.[^"\\]*)*"\s*,\s*"[^"\\]*(?:\\.[^"\\]*)*"\s*,\s*"([^"\\]*(?:\\.[^"\\]*)*)"', re.IGNORECASE),
            'character_age_double': re.compile(r'\w+\.age\s*=\s*"([^"\\]*(?:\\.[^"\\]*)*)"', re.IGNORECASE),
            'character_age_single': re.compile(r"\w+\.age\s*=\s*'([^'\\]*(?:\\.[^'\\]*)*)'", re.IGNORECASE),
            'character_connection_double': re.compile(r'\w+\.connection\s*=\s*"([^"\\]*(?:\\.[^"\\]*)*)"', re.IGNORECASE),
            'character_connection_single': re.compile(r"\w+\.connection\s*=\s*'([^'\\]*(?:\\.[^'\\]*)*)'", re.IGNORECASE),
            'character_info_double': re.compile(r'\w+\.info\s*=\s*"([^"\\]*(?:\\.[^"\\]*)*)"', re.IGNORECASE),
            'character_info_single': re.compile(r"\w+\.info\s*=\s*'([^'\\]*(?:\\.[^'\\]*)*)'", re.IGNORECASE),
            'character_relationship_double': re.compile(r'\w+\.relationship\s*=\s*"([^"\\]*(?:\\.[^"\\]*)*)"', re.IGNORECASE),
            'character_relationship_single': re.compile(r"\w+\.relationship\s*=\s*'([^'\\]*(?:\\.[^'\\]*)*)'", re.IGNORECASE),
            'method_calls_text_double': re.compile(r'\.(remove|add|append|insert)\s*\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"', re.IGNORECASE),
            'method_calls_text_single': re.compile(r"\.(remove|add|append|insert)\s*\(\s*'([^'\\]*(?:\\.[^'\\]*)*)'", re.IGNORECASE),
            'custom_dialogue_double': re.compile(r'\w+\.say\s*\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"', re.IGNORECASE),
            'custom_dialogue_single': re.compile(r"\w+\.say\s*\(\s*'([^'\\]*(?:\\.[^'\\]*)*)'", re.IGNORECASE),
            

            # NOUVEAU - AVEC GESTION DES ÉCHAPPEMENTS
            'tl_old_double': re.compile(r'old\s+"([^"\\]*(?:\\.[^"\\]*)*)"'),
            'tl_old_single': re.compile(r"old\s+'([^'\\]*(?:\\.[^'\\]*)*)'"),
            'i18n_existing_double': re.compile(r'__?\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"'),
            'i18n_existing_single': re.compile(r"__?\(\s*'([^'\\]*(?:\\.[^'\\]*)*)'"),

        }

    def _init_custom_patterns(self) -> Dict[str, Pattern]:
        """Initialise les patterns regex personnalisés depuis la configuration"""
        from infrastructure.config.config import config_manager
        
        custom_patterns = {}
        config_patterns = config_manager.get('custom_extraction_patterns', [])
        
        for i, pattern_config in enumerate(config_patterns):
            if pattern_config.get('enabled', False):
                try:
                    flags = 0
                    pattern_flags = pattern_config.get('flags', '')
                    
                    if 'i' in pattern_flags:
                        flags |= re.IGNORECASE
                    if 'm' in pattern_flags:
                        flags |= re.MULTILINE
                    if 's' in pattern_flags:
                        flags |= re.DOTALL
                    if 'g' in pattern_flags:
                        # 'g' est implicite avec findall, pas besoin de flag
                        pass
                    
                    # Nettoyer le nom (remplacer espaces et tirets par underscores)
                    clean_name = pattern_config.get('name', 'unnamed').replace(' ', '_').replace('-', '_')
                    pattern_name = f"custom_{i}_{clean_name}"
                    custom_patterns[pattern_name] = re.compile(pattern_config['pattern'], flags)
                    
                    log_message("DEBUG", f"Pattern personnalisé chargé: {pattern_config.get('name', 'unnamed')}", category="extraction")
                    
                except re.error as e:
                    log_message("ERREUR", f"Pattern personnalisé invalide '{pattern_config.get('name', 'unnamed')}': {e}", category="extraction")
                except Exception as e:
                    log_message("ERREUR", f"Erreur chargement pattern personnalisé: {e}", category="extraction")
        
        return custom_patterns

    def _is_variable_pattern(self, text: str) -> bool:
        """Vérifie si un texte ressemble à une variable plutôt qu'à du texte traduisible"""
        text = text.strip()
        
        # Variables Ren'Py communes
        if text.startswith(('persistent.', 'store.', 'config.', 'preferences.')):
            return True
        
        # Variables avec underscores sans espaces
        if '_' in text and ' ' not in text and len(text.split('.')) <= 3:
            return True
        
        # Noms de variables snake_case
        if re.match(r'^[a-z_][a-z0-9_]*$', text) and '_' in text:
            return True
        
        # Variables avec points (namespaces)
        if '.' in text and ' ' not in text and not any(char.isupper() for char in text.split('.')[0]):
            return True
        
        return False

    def _extract_text_from_match(self, match, pattern_name: str) -> str:
        """Version mise à jour pour extraire le texte selon le pattern (guillemets séparés)"""
        try:
            # Tous les nouveaux patterns ont le texte dans group(1)
            if pattern_name.endswith('_double') or pattern_name.endswith('_single'):
                text = match.group(1) or ""
            elif pattern_name in ['method_calls_text_double', 'method_calls_text_single']:
                text = match.group(2) or ""  # Le texte est dans le groupe 2 pour ces patterns
            else:
                # Patterns legacy
                text = match.group(1) or ""
            
            # Filtrer les variables pour les patterns character_def
            if pattern_name.startswith('character_def') and self._is_variable_pattern(text):
                return ""
                
            return text
        except (IndexError, AttributeError):
            return ""
    
    def _extract_all_groups_from_match(self, match, pattern_name: str) -> List[str]:
        """Extrait tous les groupes capturés d'un match pour les patterns personnalisés"""
        try:
            groups = []
            # Extraire tous les groupes capturés (group(1), group(2), etc.)
            for i in range(1, len(match.groups()) + 1):
                group_text = match.group(i)
                if group_text and group_text.strip():
                    groups.append(group_text.strip())
            return groups
        except (IndexError, AttributeError):
            return []
    
    def _process_custom_pattern_matches(self, pattern_name: str, matches, all_detected: list, 
                            seen_texts: set, duplicate_counts: dict, results: dict, 
                            stats: dict) -> None:
        """Nouvelle fonction pour traiter les patterns personnalisés avec support des groupes multiples"""
        for match in matches:
            # ✅ NOUVELLE LOGIQUE : Extraire tous les groupes capturés
            all_groups = self._extract_all_groups_from_match(match, pattern_name)
            
            if not all_groups:
                continue
            
            # ✅ NOUVELLE LOGIQUE : Traiter chaque groupe comme un texte séparé
            for group_text in all_groups:
                if not group_text or not group_text.strip():
                    continue
                    
                text = group_text.strip()
                all_detected.append(text)
                
                if text in seen_texts:
                    # Gérer le cas où le pattern n'est pas dans duplicate_counts
                    if pattern_name in duplicate_counts:
                        duplicate_counts[pattern_name] += 1
                    log_message("DEBUG", f"🔄 DOUBLON {pattern_name}: '{text[:30]}...'", category="extraction_results")
                else:
                    seen_texts.add(text)
                
                if self._is_valid_and_new_with_stats(text, stats):
                    # Les patterns personnalisés sont toujours classés en auto_safe
                    self._assign_text('auto_safe', text, results)
                    log_message("DEBUG", f"✅ {pattern_name} (custom) auto-safe: '{text[:30]}...'", category="extraction_results")
                
                # Mettre à jour les stats pour les patterns personnalisés
                if pattern_name not in stats['patterns_found']:
                    stats['patterns_found'][pattern_name] = 0
                stats['patterns_found'][pattern_name] += 1

    def _get_all_pattern_names(self) -> List[str]:
        """Retourne la liste complète des noms de patterns à traiter"""
        return [
            'character_def_double', 'character_def_single',
            'show_text_double', 'show_text_single',
            'text_element_with_attrs_double', 'text_element_with_attrs_single',
            'text_element_double', 'text_element_single',
            'input_calls_double', 'input_calls_single',
            'commented_input_double', 'commented_input_single',
            'notify_calls_double', 'notify_calls_single',
            'text_param_double', 'text_param_single',
            'renpy_notify_double', 'renpy_notify_single',
            'activity_title_double', 'activity_title_single',
            'textbutton_double', 'textbutton_single',
            'activity_description',
            'character_age_double', 'character_age_single',
            'character_connection_double', 'character_connection_single',
            'character_info_double', 'character_info_single',
            'character_relationship_double', 'character_relationship_single',
            'method_calls_text_double', 'method_calls_text_single',
            'custom_dialogue_double', 'custom_dialogue_single'
        ]

    def _process_pattern_matches(self, pattern_name: str, matches, all_detected: list, 
                            seen_texts: set, duplicate_counts: dict, results: dict, 
                            stats: dict) -> None:
        """Version mise à jour pour traiter tous les patterns avec guillemets séparés"""
        for match in matches:
            text = self._extract_text_from_match(match, pattern_name)
            if not text:
                continue
                
            text = text.strip()
            all_detected.append(text)
            
            if text in seen_texts:
                # Gérer le cas où le pattern n'est pas dans duplicate_counts
                if pattern_name in duplicate_counts:
                    duplicate_counts[pattern_name] += 1
                log_message("DEBUG", f"🔄 DOUBLON {pattern_name}: '{text[:30]}...'", category="extraction_results")
            else:
                seen_texts.add(text)
            
            if self._is_valid_and_new_with_stats(text, stats):
                # Classification selon le type de pattern
                base_pattern_name = self._get_base_pattern_name(pattern_name)
                
                if base_pattern_name in ['character_def', 'input_calls', 'notify_calls', 'show_text', 
                                    'text_param', 'renpy_notify', 'activity_title', 'activity_description', 
                                    'character_info', 'text_element_with_attrs', 'commented_input']:
                    self._assign_text('auto_safe', text, results)
                    log_message("DEBUG", f"✅ {pattern_name} auto-safe: '{text[:30]}...'", category="extraction_results")
                    
                elif base_pattern_name in ['character_age', 'character_connection', 'character_relationship']:
                    if self._is_character_attribute_auto_safe(text):
                        self._assign_text('auto_safe', text, results)
                        log_message("DEBUG", f"✅ {pattern_name} auto-safe: '{text[:30]}...'", category="extraction_results")
                    else:
                        self._assign_text('text_check', text, results)
                        log_message("DEBUG", f"🟡 {pattern_name} à vérifier: '{text[:30]}...'", category="extraction_results")
                        
                elif base_pattern_name in ['textbutton']:
                    if self._is_textbutton_auto_safe(text):
                        self._assign_text('auto_safe', text, results)
                        log_message("DEBUG", f"✅ {pattern_name} auto-safe: '{text[:30]}...'", category="extraction_results")
                    else:
                        self._assign_text('textbutton_check', text, results)
                        log_message("DEBUG", f"🟡 {pattern_name} à vérifier: '{text[:30]}...'", category="extraction_results")
                        
                elif base_pattern_name in ['text_element']:
                    if self._is_text_auto_safe(text):
                        self._assign_text('auto_safe', text, results)
                        log_message("DEBUG", f"✅ {pattern_name} auto-safe: '{text[:30]}...'", category="extraction_results")
                    else:
                        self._assign_text('text_check', text, results)
                        log_message("DEBUG", f"🟡 {pattern_name} à vérifier: '{text[:30]}...'", category="extraction_results")
                        
                elif base_pattern_name in ['method_calls_text', 'custom_dialogue']:
                    if self._is_method_call_auto_safe(text):
                        self._assign_text('auto_safe', text, results)
                        log_message("DEBUG", f"✅ {pattern_name} auto-safe: '{text[:30]}...'", category="extraction_results")
                    else:
                        self._assign_text('text_check', text, results)
                        log_message("DEBUG", f"🟡 {pattern_name} à vérifier: '{text[:30]}...'", category="extraction_results")
                
                # Gestion des patterns personnalisés
                elif base_pattern_name.startswith('custom_'):
                    # Les patterns personnalisés sont toujours classés en auto_safe
                    self._assign_text('auto_safe', text, results)
                    log_message("DEBUG", f"✅ {pattern_name} (custom) auto-safe: '{text[:30]}...'", category="extraction_results")
                
                # Mettre à jour les stats seulement si la clé existe
                if base_pattern_name in stats['patterns_found']:
                    stats['patterns_found'][base_pattern_name] += 1
                elif base_pattern_name.startswith('custom_'):
                    # Créer la clé pour les patterns personnalisés si elle n'existe pas
                    if base_pattern_name not in stats['patterns_found']:
                        stats['patterns_found'][base_pattern_name] = 0
                    stats['patterns_found'][base_pattern_name] += 1

    def _get_base_pattern_name(self, pattern_name: str) -> str:
        """Extrait le nom de pattern de base (sans _double/_single)"""
        if pattern_name.endswith('_double') or pattern_name.endswith('_single'):
            return pattern_name.rsplit('_', 1)[0]
        return pattern_name

    def _initialize_stats_patterns(self) -> Dict[str, int]:
        """Initialise le dictionnaire des statistiques pour tous les patterns de base"""
        return {
            'character_def': 0, 'show_text': 0, 'text_element_with_attrs': 0, 'text_element': 0,
            'input_calls': 0, 'commented_input': 0, 'notify_calls': 0, 'text_param': 0,
            'renpy_notify': 0, 'activity_title': 0, 'activity_description': 0,
            'character_age': 0, 'character_connection': 0, 'character_info': 0, 'character_relationship': 0,
            'textbutton': 0, 'method_calls_text': 0, 'custom_dialogue': 0
        }

    def _is_character_attribute_auto_safe(self, text: str) -> bool:
        """Détermine si un attribut de personnage est auto-safe"""
        text_lower = text.lower().strip()
        if len(text) < 3:
            return False
        if re.match(r'^\d+[\+\-]?$', text) or text_lower in ['young', 'old', 'adult', 'teen']:
            return True
        relationship_terms = ['friend', 'lover', 'enemy', 'family', 'co-worker', 'agent', 'thief', 'boss', 'colleague', 'partner']
        if any(term in text_lower for term in relationship_terms):
            return True
        if ' ' in text and len(text) > 8:
            return True
        if text.isupper() or '_' in text:
            return False
        if len(text) <= 10 and ' ' not in text:
            return False
        return len(text) >= 8

    def _is_method_call_auto_safe(self, text: str) -> bool:
        """Détermine si un appel de méthode est auto-safe"""
        text_lower = text.lower().strip()
        if len(text) < 8:
            return False
        if re.match(r'^[a-z]+_[a-z0-9_]+$', text) and len(text) <= 20:
            return False
        if re.match(r'^[a-zA-Z0-9_-]+$', text) and len(text) <= 12 and '_' in text:
            return False
        if ' ' in text and len(text) >= 15:
            words = text.split()
            if len(words) >= 3:
                return True
        user_indicators = ['message', 'task', 'todo', 'note', 'reminder', 'quest', 'notification', 'check', 'discuss', 'connect', 'read', 'open']
        if any(indicator in text_lower for indicator in user_indicators):
            if ' ' in text:
                return True
        if self._is_complete_sentence(text):
            return True
        if text.isupper() or (text.islower() and '_' in text):
            return False
        if '.' in text and not text.endswith('.') and not text.endswith(' - OPTIONAL.'):
            return False
        return False
   
    def extract_targeted_texts(self, game_folder: str, tl_folder: str = None, 
                              existing_translations: Set[str] = None,
                              excluded_files: List[str] = None) -> Dict[str, Set[str]]:
        """
        Extraction ciblée avec patterns spécialisés et gestion séparée des guillemets
        """
        log_message("INFO", f"Début extraction CIBLÉE dans: {game_folder}", category="extraction_results")
        
        # Étape 1: anti-doublons
        if existing_translations is not None:
            self.existing_translations = existing_translations
            log_message("INFO", f"Anti-doublons: {len(self.existing_translations)} textes pré-chargés", category="extraction_results")
        elif tl_folder and os.path.exists(tl_folder):
            self._analyze_existing_translations(tl_folder)
            log_message("INFO", f"Anti-doublons: {len(self.existing_translations)} textes existants", category="extraction_results")
        else:
            log_message("INFO", "Aucun dossier tl - extraction complète", category="extraction_results")
        
        results = {
            'auto_safe': set(),
            'textbutton_check': set(),
            'text_check': set(),
        }
        
        stats = {
            'files_processed': 0,
            'files_excluded': 0,
            'files_error': 0,
            'patterns_found': self._initialize_stats_patterns(),
            'rejection_reasons': {'too_short': 0, 'duplicate': 0, 'technical': 0}
        }
        
        default_excluded = {'options.rpy', 'gui.rpy', 'screens.rpy'}
        if excluded_files:
            excluded_files_set = set(excluded_files)
            excluded_files_set.update(default_excluded)
        else:
            excluded_files_set = default_excluded
        
        log_message("INFO", f"Scan récursif des fichiers .rpy...", category="extraction_results")
        all_files = list(glob.glob(os.path.join(game_folder, "**/*.rpy"), recursive=True))
        log_message("INFO", f"{len(all_files)} fichiers .rpy trouvés", category="extraction_results")

        all_detected = []
        seen_texts = set()
        # Initialiser duplicate_counts avec tous les patterns standards ET personnalisés
        duplicate_counts = {pattern: 0 for pattern in self._get_all_pattern_names()}
        # Ajouter les patterns personnalisés
        for custom_pattern_name in self.custom_patterns.keys():
            duplicate_counts[custom_pattern_name] = 0

        for filepath in all_files:
            if '/tl/' in filepath.replace('\\', '/') or '\\tl\\' in filepath:
                continue
            
            filename = os.path.basename(filepath)
            if filename in excluded_files_set:
                stats['files_excluded'] += 1
                log_message("DEBUG", f"Fichier exclu: {filename}", category="extraction_results")
                continue
                
            try:
                with open(filepath, encoding="utf-8") as f:
                    content = f.read()
                    stats['files_processed'] += 1
                    log_message("DEBUG", f"Traitement: {filename} ({len(content)} caractères)", category="extraction_results")
                    
                    # Traiter tous les patterns avec gestion séparée des guillemets
                    for pattern_name in self._get_all_pattern_names():
                        if pattern_name in self.patterns:
                            matches = self.patterns[pattern_name].finditer(content)
                            self._process_pattern_matches(
                                pattern_name, matches, all_detected, seen_texts, 
                                duplicate_counts, results, stats
                            )
                    
                    # Traiter les patterns personnalisés avec support des groupes multiples
                    for pattern_name, pattern in self.custom_patterns.items():
                        matches = pattern.finditer(content)
                        self._process_custom_pattern_matches(
                            pattern_name, matches, all_detected, seen_texts, 
                            duplicate_counts, results, stats
                        )
                            
            except Exception as e:
                stats['files_error'] += 1
                log_message("ATTENTION", f"Erreur lecture {filename}: {e}", category="extraction_results")
                continue
        
        total_found = len(all_detected)
        total_unique = len(seen_texts)
        total_duplicates = sum(duplicate_counts.values())
        total_rejected = sum(stats['rejection_reasons'].values())
        total_accepted = len(results['auto_safe']) + len(results['textbutton_check']) + len(results['text_check'])
        
        # Log simplifié en une ligne
        log_message("INFO", f"✅ Extraction : {total_accepted} textes (auto-safe:{len(results['auto_safe'])}, textbutton:{len(results['textbutton_check'])}, text:{len(results['text_check'])})", category="extraction_results")
        # Normalisation finale (exclusivité stricte)
        unique_map = {}
        for cat in ('auto_safe', 'textbutton_check', 'text_check'):
            for t in list(results[cat]):
                best = min(
                    [cat] + [c for c in ('auto_safe','textbutton_check','text_check') if t in results[c]],
                    key=self._get_category_priority
                )
                if best != cat:
                    results[cat].discard(t)
                results[best].add(t)
        
        return results

    def apply_simple_mode_filter(self):
        """
        DÉPRÉCIÉ: Le mode simple a été supprimé, cette méthode ne fait rien
        """
        log_message("INFO", "Mode simple supprimé - utilisation du mode optimisé uniquement", category="extraction_results")

    def _get_simple_pattern_names(self) -> List[str]:
        """
        DÉPRÉCIÉ: Le mode simple a été supprimé
        """
        return []

    def _analyze_existing_translations(self, tl_folder: str) -> None:
        """Analyse le dossier tl pour identifier les textes déjà traduits"""
        log_message("INFO", f"🔍 Analyse du dossier tl: {tl_folder}", category="extraction_results")
        
        rpy_files = list(glob.glob(os.path.join(tl_folder, "**/*.rpy"), recursive=True))
        
        if not rpy_files:
            log_message("INFO", f"📂 Dossier tl vide ou inexistant", category="extraction_results")
            return
        
        translations_count = 0
        
        for filepath in rpy_files:
            try:
                with open(filepath, encoding="utf-8") as f:
                    content = f.read()
                    
                # NOUVEAU - 4 patterns avec échappements
                for match in self.patterns['tl_old_double'].finditer(content):
                    text = match.group(1).strip()
                    if text:
                        self.existing_translations.add(text)
                        translations_count += 1

                for match in self.patterns['tl_old_single'].finditer(content):
                    text = match.group(1).strip()
                    if text:
                        self.existing_translations.add(text)
                        translations_count += 1

                for match in self.patterns['i18n_existing_double'].finditer(content):
                    text = match.group(1).strip()
                    if text:
                        self.existing_translations.add(text)

                for match in self.patterns['i18n_existing_single'].finditer(content):
                    text = match.group(1).strip()
                    if text:
                        self.existing_translations.add(text)
                            
            except Exception as e:
                log_message("ATTENTION", f"Erreur lecture fichier tl {os.path.basename(filepath)}: {e}", category="extraction_results")
                continue
        
        log_message("INFO", f"📊 Anti-doublons activé: {len(self.existing_translations)} textes uniques détectés", category="extraction_results")

    def _is_valid_and_new_with_stats(self, text: str, stats: dict) -> bool:
        """Version avec stats pour identifier les textes perdus"""
        if not text or len(text.strip()) < 2:
            stats['rejection_reasons']['too_short'] += 1
            log_message("DEBUG", f"⚠ REJET trop court: '{text}' (longueur: {len(text)})", category="extraction_results")
            return False
        
        if text in self.existing_translations:
            stats['rejection_reasons']['duplicate'] += 1
            log_message("DEBUG", f"⚠ REJET doublon: '{text[:30]}...'", category="extraction_results")
            return False
        
        if self._is_purely_technical(text):
            stats['rejection_reasons']['technical'] += 1
            log_message("DEBUG", f"⚠ REJET technique: '{text[:30]}...'", category="extraction_results")
            return False
        
        log_message("DEBUG", f"✅ ACCEPTÉ: '{text[:30]}...'", category="extraction_results")
        return True

    def _is_purely_technical(self, text: str) -> bool:
        """Vérifie si un texte est purement technique"""
        if re.match(r'^\[.*\]$', text):
            return True
        if re.match(r'^.*\.(png|jpg|jpeg|gif|webp|mp3|ogg|wav|avi|mp4|webm|rpy|txt|json)$', text.lower()):
            return True
        if text.lower().startswith(('http://', 'https://', 'www.')):
            return True
        if re.match(r'^([A-Z]:\\|/)', text):
            return True
        if re.match(r'^#[0-9a-fA-F]{3,8}$', text):
            return True
        if re.match(r'^[0-9\s\-_\.,:;!?]+$', text):
            return True
        if re.match(r'^[a-z_][a-z0-9_]*$', text) and '_' in text and len(text) > 8:
            return True
        if re.match(r'^[A-Z_][A-Z0-9_]*$', text) and len(text) > 4:
            return True
        if re.match(r'^[a-z]+[0-9]*_[a-z0-9_]+$', text) and len(text) <= 25:
            return True
        return False
    
    def _is_textbutton_auto_safe(self, text: str) -> bool:
        """Détermine si un textbutton est auto-safe (confiance 100%)"""
        text_lower = text.lower().strip()
        common_ui_words = {
            'save', 'load', 'new', 'open', 'edit', 'delete', 'copy', 'paste',
            'start', 'stop', 'play', 'pause', 'reset', 'clear', 'refresh',
            'menu', 'back', 'next', 'home', 'exit', 'quit', 'close',
            'yes', 'no', 'ok', 'cancel', 'done', 'finish',
            'help', 'about', 'info', 'settings', 'options', 'preferences',
            'continue', 'skip', 'auto', 'history', 'rollback'
        }
        if text_lower in common_ui_words:
            return True
        words = re.findall(r'[a-zA-Z]+', text_lower)
        for word in words:
            if word in common_ui_words:
                return True
        if len(text) >= 15:
            return True
        return False
    
    def _is_text_auto_safe(self, text: str) -> bool:
        """Détermine si un élément text est auto-safe (confiance 100%)"""
        return self._is_complete_sentence(text)
    
    def _is_complete_sentence(self, text: str) -> bool:
        """Vérifie si un texte ressemble à une phrase complète"""
        text = text.strip()
        if len(text) < 15:
            return False
        words = text.split()
        if len(words) < 3:
            return False
        if text.endswith(('.', '!', '?', ':', ';')) or text[0].isupper():
            return True
        letters = re.findall(r'[a-zA-ZÀ-ÿ]', text)
        if len(letters) >= 10:
            vowels = len(re.findall(r'[aeiouáéíóúàèìòùâêîôûäëïöüyAEIOU]', text))
            vowel_ratio = vowels / len(letters)
            if 0.2 <= vowel_ratio <= 0.6:
                return True
        return False

    def _get_category_priority(self, cat: str) -> int:
        """Plus petit nombre = plus prioritaire"""
        priorities = {'auto_safe': 0, 'textbutton_check': 1, 'text_check': 2}
        return priorities.get(cat, 99)

    def _assign_text(self, target_cat: str, text: str, results: dict) -> None:
        """
        Ajoute `text` dans `target_cat` en garantissant l'exclusivité entre catégories
        et en respectant la priorité (auto_safe > textbutton_check > text_check).
        """
        # Si déjà présent dans la cible, rien à faire
        if text in results[target_cat]:
            return

        # Vérifier si présent ailleurs
        present_in = [
            cat for cat in ('auto_safe', 'textbutton_check', 'text_check')
            if text in results[cat]
        ]
        if not present_in:
            results[target_cat].add(text)
            return

        # S'il existe déjà, ne garder que la catégorie la plus prioritaire
        best_cat = min([target_cat] + present_in, key=self._get_category_priority)

        # Retirer des catégories moins prioritaires
        for cat in ('auto_safe', 'textbutton_check', 'text_check'):
            if cat != best_cat:
                results[cat].discard(text)

        # Assurer la présence dans la meilleure catégorie
        results[best_cat].add(text)


class TextExtractionResultsBusiness:
    """Logique métier pour les résultats d'extraction de textes"""
    
    def __init__(self):
        """Initialise le module de résultats d'extraction"""
        self.current_operation = None
        self.operation_cancelled = False
        log_message("INFO", "TextExtractionResultsBusiness initialisé", category="extraction_results")
    
    def run_extraction_analysis(self, extraction_params: Dict[str, Any], 
                               progress_callback=None, status_callback=None, 
                               completion_callback=None) -> None:
        """
        CORRIGÉ: Lance l'analyse d'extraction dans un thread
        """
        def worker():
            try:
                self.operation_cancelled = False
                
                if status_callback:
                    status_callback("Initialisation de l'analyse...")
                
                extractor = OptimizedTextExtractor()
                
                detection_mode = extraction_params.get('detection_mode', 'optimized')
                if detection_mode == "simple":
                    # CORRIGÉ: Utiliser la nouvelle méthode de filtrage
                    extractor.apply_simple_mode_filter()
                    log_message("INFO", "Mode Simple activé - patterns basiques uniquement", category="extraction_results")
                else:
                    log_message("INFO", "Mode Optimisé activé - tous les patterns ciblés", category="extraction_results")
                
                if status_callback:
                    status_callback("Analyse du dossier tl...")
                if progress_callback:
                    progress_callback(30, "Analyse en cours...")
                
                game_folder = extraction_params['game_folder']
                tl_folder = extraction_params['tl_folder']
                existing_translations = extraction_params.get('existing_translations', None)
                excluded_files = extraction_params.get('excluded_files', [])
                
                # CORRIGÉ: Appeler la méthode avec le bon nom
                results = extractor.extract_targeted_texts(
                    game_folder, 
                    tl_folder, 
                    existing_translations,
                    excluded_files
                )
                
                if progress_callback:
                    progress_callback(70, "Traitement des résultats...")
                
                enriched_results = self._enrich_extraction_results(results, extraction_params)
                
                if status_callback:
                    status_callback("Analyse terminée - Préparation des résultats...")
                if progress_callback:
                    progress_callback(100, "Terminé")
                
                if completion_callback and not self.operation_cancelled:
                    completion_callback(True, enriched_results)
                    
            except Exception as e:
                if not self.operation_cancelled:
                    error_msg = f"Erreur pendant l'analyse d'extraction: {e}"
                    log_message("ERREUR", error_msg, category="extraction_results")
                    if completion_callback:
                        completion_callback(False, {'error': error_msg, 'exception': e})
        
        self.current_operation = threading.Thread(target=worker, daemon=True)
        self.current_operation.start()
    
    def cancel_operation(self):
        """Annule l'opération en cours"""
        self.operation_cancelled = True
        log_message("INFO", "Annulation de l'analyse d'extraction demandée", category="extraction_results")
    
    def _enrich_extraction_results(self, results: Dict[str, Set[str]], 
                                  extraction_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrichit les résultats d'extraction avec des métadonnées
        """
        enriched = {
            'raw_results': results,
            'statistics': {},
            'metadata': {},
            'categorized_results': {}
        }
        
        try:
            auto_safe_count = len(results.get('auto_safe', set()))
            textbutton_count = len(results.get('textbutton_check', set()))
            text_check_count = len(results.get('text_check', set()))
            total_detected = auto_safe_count + textbutton_count + text_check_count
            
            enriched['statistics'] = {
                'total_detected': total_detected,
                'auto_safe_count': auto_safe_count,
                'textbutton_count': textbutton_count,
                'text_check_count': text_check_count,
                'confidence_ratio': (auto_safe_count / total_detected * 100) if total_detected > 0 else 0.0,
                'manual_review_needed': textbutton_count + text_check_count
            }
            
            enriched['metadata'] = {
                'extraction_date': datetime.now().isoformat(),
                'detection_mode': extraction_params.get('detection_mode', 'optimized'),
                'anti_duplicate_active': extraction_params.get('anti_duplicate_active', False),
                'game_folder': extraction_params.get('game_folder'),
                'tl_folder': extraction_params.get('tl_folder'),
                'excluded_files': extraction_params.get('excluded_files', [])
            }
            
            enriched['categorized_results'] = {
                'high_confidence': {
                    'texts': results.get('auto_safe', set()),
                    'description': 'Confiance 100% - Extraction automatique recommandée',
                    'default_selected': True,
                    'category_color': 'green'
                },
                'textbuttons': {
                    'texts': results.get('textbutton_check', set()),
                    'description': 'Boutons d\'interface détectés - Vérification recommandée',
                    'default_selected': False,
                    'category_color': 'orange'
                },
                'text_elements': {
                    'texts': results.get('text_check', set()),
                    'description': 'Éléments texte détectés - Vérification recommandée',
                    'default_selected': False,
                    'category_color': 'orange'
                }
            }
            
            log_message("INFO", f"Résultats enrichis: {total_detected} textes détectés", category="extraction_results")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur enrichissement résultats: {e}", category="extraction_results")
        
        return enriched
    
    def calculate_detailed_statistics(self, results: Dict[str, Any], 
                                    project_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Calcule des statistiques détaillées sur les résultats
        """
        stats = {
            'extraction_summary': {},
            'quality_metrics': {},
            'recommendations': [],
            'comparison_data': {}
        }
        
        try:
            basic_stats = results.get('statistics', {})
            
            stats['extraction_summary'] = {
                'total_texts_found': basic_stats.get('total_detected', 0),
                'auto_safe_texts': basic_stats.get('auto_safe_count', 0),
                'manual_review_texts': basic_stats.get('manual_review_needed', 0),
                'confidence_percentage': round(basic_stats.get('confidence_ratio', 0), 1)
            }
            
            total = basic_stats.get('total_detected', 0)
            if total > 0:
                stats['quality_metrics'] = {
                    'extraction_efficiency': 'Élevée' if total > 20 else 'Moyenne' if total > 5 else 'Faible',
                    'confidence_level': 'Élevé' if basic_stats.get('confidence_ratio', 0) > 70 else 'Moyen',
                    'review_workload': 'Léger' if basic_stats.get('manual_review_needed', 0) < 10 else 'Modéré'
                }
            
            if basic_stats.get('auto_safe_count', 0) > 0:
                stats['recommendations'].append("Extraire automatiquement les textes à confiance élevée")
            
            if basic_stats.get('manual_review_needed', 0) > 0:
                stats['recommendations'].append("Examiner manuellement les textes d'interface détectés")
            
            if total == 0:
                stats['recommendations'].append("Aucun nouveau texte détecté - toutes les traductions semblent complètes")
            elif total > 50:
                stats['recommendations'].append("Grand nombre de textes détectés - vérifier la configuration d'exclusion")
            
            if project_context:
                self._add_comparison_data(stats, results, project_context)
            
        except Exception as e:
            log_message("ERREUR", f"Erreur calcul statistiques détaillées: {e}", category="extraction_results")
        
        return stats
    
    def _add_comparison_data(self, stats: Dict[str, Any], results: Dict[str, Any], 
                           project_context: Dict[str, Any]) -> None:
        """
        Ajoute des données de comparaison basées sur le contexte du projet
        """
        try:
            game_rpy_count = project_context.get('game_rpy_count', 0)
            total_detected = results.get('statistics', {}).get('total_detected', 0)
            
            if game_rpy_count > 0:
                detection_ratio = (total_detected / game_rpy_count) * 100
                
                stats['comparison_data'] = {
                    'game_files_count': game_rpy_count,
                    'detection_ratio_percent': round(detection_ratio, 1),
                    'detection_efficiency': (
                        'Très efficace' if detection_ratio > 20 else
                        'Efficace' if detection_ratio > 10 else
                        'Normale' if detection_ratio > 5 else
                        'Faible'
                    )
                }
        except Exception as e:
            log_message("DEBUG", f"Erreur données de comparaison: {e}", category="extraction_results")
    
    def prepare_text_selections(self, results: Dict[str, Any]) -> Dict[str, bool]:
        """
        Prépare les sélections par défaut des textes selon leur catégorie
        """
        selections = {}
        
        try:
            categorized = results.get('categorized_results', {})
            
            for category_name, category_data in categorized.items():
                texts = category_data.get('texts', set())
                default_selected = category_data.get('default_selected', False)
                
                for text in texts:
                    selections[text] = default_selected
            
            log_message("INFO", f"Sélections préparées: {len(selections)} textes", category="extraction_results")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur préparation sélections: {e}", category="extraction_results")
        
        return selections
    
    def generate_extraction_file(self, selected_texts: Set[str], output_path: str, 
                            metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Génère un fichier .rpy d'extraction à partir des textes sélectionnés
        """
        result = {
            'success': False,
            'file_path': output_path,
            'texts_count': 0,
            'errors': [],
            'warnings': []
        }
        
        try:
            if not selected_texts:
                result['errors'].append("Aucun texte sélectionné pour la génération")
                return result
            
            log_message("INFO", f"Génération du fichier: {os.path.basename(output_path)}", category="extraction_results")
            log_message("INFO", f"Nombre de textes: {len(selected_texts)}", category="extraction_results")
            
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                current_time = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")
                project_name = metadata.get('Projet', 'Projet inconnu') if metadata else 'Projet inconnu'
                
                f.write(f'# Date de génération: {current_time}\n')
                f.write('# Fichier d\'extraction généré par RenExtract\n')
                f.write(f'# Projet: {project_name}\n\n')
                
                f.write('translate french strings:\n\n')
                
                sorted_texts = sorted(selected_texts)
                for text in sorted_texts:
                    # On utilise directement le texte sans le ré-échapper
                    f.write(f'    old "{text}"\n    new "{text}"\n\n')
            
            result['success'] = True
            result['texts_count'] = len(selected_texts)
            
            log_message("INFO", f"Fichier généré avec succès: {output_path}", category="extraction_results")
            
        except Exception as e:
            error_msg = f"Erreur génération fichier: {e}"
            result['errors'].append(error_msg)
            log_message("ERREUR", error_msg, category="extraction_results")
        
        return result
    
    def export_analysis_report(self, results: Dict[str, Any], detailed_stats: Dict[str, Any],
                             export_path: str) -> Dict[str, Any]:
        """
        Exporte un rapport d'analyse détaillé
        """
        export_result = {
            'success': False,
            'report_path': export_path,
            'errors': []
        }
        
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("RAPPORT D'ANALYSE D'EXTRACTION - RENEXTRACT\n")
                f.write("=" * 60 + "\n")
                
                metadata = results.get('metadata', {})
                f.write(f"Date d'analyse: {metadata.get('extraction_date', 'Inconnue')}\n")
                f.write(f"Mode de détection: {metadata.get('detection_mode', 'Non spécifié')}\n")
                f.write(f"Anti-doublon actif: {'Oui' if metadata.get('anti_duplicate_active') else 'Non'}\n")
                f.write(f"Dossier analysé: {metadata.get('game_folder', 'Non spécifié')}\n")
                f.write(f"Langue de référence: {os.path.basename(metadata.get('tl_folder', ''))}\n")
                f.write("\n")
                
                summary = detailed_stats.get('extraction_summary', {})
                f.write("RÉSUMÉ D'EXTRACTION\n")
                f.write("-" * 30 + "\n")
                f.write(f"Total de textes détectés: {summary.get('total_texts_found', 0)}\n")
                f.write(f"Textes auto-safe: {summary.get('auto_safe_texts', 0)}\n")
                f.write(f"Textes à réviser: {summary.get('manual_review_texts', 0)}\n")
                f.write(f"Niveau de confiance: {summary.get('confidence_percentage', 0)}%\n")
                f.write("\n")
                
                quality = detailed_stats.get('quality_metrics', {})
                if quality:
                    f.write("MÉTRIQUES DE QUALITÉ\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"Efficacité d'extraction: {quality.get('extraction_efficiency', 'Non évaluée')}\n")
                    f.write(f"Niveau de confiance: {quality.get('confidence_level', 'Non évalué')}\n")
                    f.write(f"Charge de révision: {quality.get('review_workload', 'Non évaluée')}\n")
                    f.write("\n")
                
                categorized = results.get('categorized_results', {})
                if categorized:
                    f.write("DÉTAIL PAR CATÉGORIE\n")
                    f.write("-" * 30 + "\n")
                    
                    for category_name, category_data in categorized.items():
                        texts = category_data.get('texts', set())
                        if texts:
                            f.write(f"\n{category_name.upper()} ({len(texts)} textes)\n")
                            f.write(f"Description: {category_data.get('description', '')}\n")
                            f.write("Textes détectés:\n")
                            
                            for i, text in enumerate(sorted(texts), 1):
                                display_text = text[:80] + "..." if len(text) > 80 else text
                                f.write(f"  {i}. {display_text}\n")
                            f.write("\n")
                
                recommendations = detailed_stats.get('recommendations', [])
                if recommendations:
                    f.write("RECOMMANDATIONS\n")
                    f.write("-" * 30 + "\n")
                    for i, rec in enumerate(recommendations, 1):
                        f.write(f"{i}. {rec}\n")
                    f.write("\n")
                
                comparison = detailed_stats.get('comparison_data', {})
                if comparison:
                    f.write("DONNÉES DE COMPARAISON\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"Fichiers du jeu analysés: {comparison.get('game_files_count', 0)}\n")
                    f.write(f"Ratio de détection: {comparison.get('detection_ratio_percent', 0)}%\n")
                    f.write(f"Efficacité de détection: {comparison.get('detection_efficiency', 'Non évaluée')}\n")
                    f.write("\n")
                
                f.write("=" * 60 + "\n")
                f.write("Fin du rapport\n")
            
            export_result['success'] = True
            log_message("INFO", f"Rapport d'analyse exporté: {export_path}", category="extraction_results")
            
        except Exception as e:
            error_msg = f"Erreur export rapport: {e}"
            export_result['errors'].append(error_msg)
            log_message("ERREUR", error_msg, category="extraction_results")
        
        return export_result

def extract_texts_simple_mode(game_folder, tl_folder=None, detection_mode="optimized", 
                             excluded_files=None, existing_translations=None):
    """
    CORRIGÉ: Mode d'extraction pour l'interface - migré depuis extract_ui_characters.py
    """
    log_message("INFO", f"Extraction mode interface: {detection_mode}", category="extraction_results")
    log_message("INFO", f"   Dossier game: {game_folder}", category="extraction_results")
    log_message("INFO", f"   Dossier tl: {tl_folder or 'Aucun'}", category="extraction_results")
    
    try:
        if not os.path.exists(game_folder):
            raise FileNotFoundError(f"Dossier game inexistant: {game_folder}")
        
        extractor = OptimizedTextExtractor()
        
        if detection_mode == "simple":
            # CORRIGÉ: Utiliser la nouvelle méthode
            extractor.apply_simple_mode_filter()
            log_message("INFO", "Mode Simple activé - patterns de base uniquement", category="extraction_results")
        else:
            log_message("INFO", "Mode Optimisé activé - tous les patterns ciblés", category="extraction_results")
        
        # CORRIGÉ: Appeler la méthode avec le bon nom
        results = extractor.extract_targeted_texts(
            game_folder, 
            tl_folder, 
            existing_translations,
            excluded_files
        )
        
        auto_safe_count = len(results.get('auto_safe', set()))
        textbutton_count = len(results.get('textbutton_check', set()))
        text_check_count = len(results.get('text_check', set()))
        total_detected = auto_safe_count + textbutton_count + text_check_count
        
        extraction_stats = {
            'total_detected': total_detected,
            'auto_safe': auto_safe_count,
            'textbutton_check': textbutton_count,
            'text_check': text_check_count,
            'detection_mode': detection_mode,
            'antiduplicate_active': tl_folder is not None,
            'game_folder': game_folder,
            'tl_folder': tl_folder
        }
        
        log_message("INFO", f"Extraction interface terminée:", category="extraction_results")
        log_message("INFO", f"   Total détecté: {total_detected}", category="extraction_results")
        log_message("INFO", f"   Auto-safe: {auto_safe_count}", category="extraction_results")
        log_message("INFO", f"   À vérifier: {textbutton_count + text_check_count}", category="extraction_results")
        
        return {
            'success': True,
            'results': results,
            'stats': extraction_stats
        }
        
    except Exception as e:
        log_message("ERREUR", f"Erreur extraction interface: {e}", category="extraction_results")
        return {
            'success': False,
            'error': str(e),
            'results': None,
            'stats': None
        }

def generate_rpy_file(selected_texts, output_path, metadata=None):
    """
    Génère un fichier .rpy à partir d'une sélection de textes - migré depuis extract_ui_characters.py
    """
    try:
        business = TextExtractionResultsBusiness()
        result = business.generate_extraction_file(selected_texts, output_path, metadata)
        return result['success']
    except Exception as e:
        log_message("ERREUR", f"Erreur génération fichier: {e}", category="extraction_results")
        return False


def get_extraction_statistics(results):
    """
    Calcule les statistiques détaillées d'extraction - migré depuis extract_ui_characters.py
    """
    if not results:
        return {
            'total_detected': 0,
            'auto_safe': 0,
            'textbutton_check': 0,
            'text_check': 0,
            'confidence_ratio': 0.0
        }
    
    auto_safe_count = len(results.get('auto_safe', set()))
    textbutton_count = len(results.get('textbutton_check', set()))
    text_check_count = len(results.get('text_check', set()))
    total_detected = auto_safe_count + textbutton_count + text_check_count
    
    confidence_ratio = (auto_safe_count / total_detected * 100) if total_detected > 0 else 0.0
    
    return {
        'total_detected': total_detected,
        'auto_safe': auto_safe_count,
        'textbutton_check': textbutton_count,
        'text_check': text_check_count,
        'confidence_ratio': round(confidence_ratio, 1)
    }


def create_extraction_context(project_path: str, selected_language: str) -> Dict[str, Any]:
    """
    Fonction utilitaire pour créer un contexte d'extraction
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


def get_default_extraction_filters() -> Dict[str, Any]:
    """
    Retourne les filtres par défaut pour l'extraction
    """
    return {
        'min_length': 2,
        'max_length': 500,
        'exclude_patterns': [
            r'^\[.*\]',        # Variables Ren'Py [variable]
            r'^#[0-9a-fA-F]+', # Codes hexadécimaux
            r'^\d+',           # Nombres seuls
            r'^[_\-\.]+'       # Symboles seuls
        ],
        'include_only_patterns': []
    }


def format_extraction_statistics(stats: Dict[str, Any]) -> str:
    """
    Formate les statistiques d'extraction pour affichage
    """
    try:
        total = stats.get('total_detected', 0)
        auto_safe = stats.get('auto_safe_count', 0)
        manual_review = stats.get('manual_review_needed', 0)
        confidence = stats.get('confidence_ratio', 0)
        
        lines = []
        lines.append(f"Total détecté: {total} textes")
        if auto_safe > 0:
            lines.append(f"Auto-safe: {auto_safe}")
        if manual_review > 0:
            lines.append(f"À réviser: {manual_review}")
        lines.append(f"Confiance: {confidence:.1f}%")
        return " • ".join(lines)
    except Exception:
        return "Statistiques non disponibles"

# Exports
__all__ = [
    'OptimizedTextExtractor',
    'TextExtractionResultsBusiness', 
    'extract_texts_simple_mode',
    'generate_rpy_file',
    'get_extraction_statistics',
    'create_extraction_context',
    'get_default_extraction_filters',
    'format_extraction_statistics'
]
