# core/extraction.py
# Extraction Functions Module
# Created for RenExtract 

"""
Module d'extraction des textes depuis les fichiers Ren'Py
"""

import os
import re
import time
import json
from collections import OrderedDict
from infrastructure.config.constants import SPECIAL_CODES, FOLDERS
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import extract_game_name

def validate_file_safely(filepath, max_size_mb=50):
    """
    ✅ VALIDATION SÉCURISÉE ET STRICTE des fichiers Ren'Py avant traitement
    """
    # L'import est déplacé ici pour éviter les dépendances circulaires si nécessaire
    from infrastructure.logging.logging import log_message
    
    try:
        if not filepath or not isinstance(filepath, str):
            return {'valid': False, 'error': "Le chemin du fichier est invalide ou manquant."}
        if not os.path.exists(filepath):
            return {'valid': False, 'error': f"Fichier non trouvé : {filepath}"}
        if not os.path.isfile(filepath):
            return {'valid': False, 'error': f"Le chemin spécifié n'est pas un fichier : {filepath}"}
        
        try:
            file_size = os.path.getsize(filepath)
            max_size_bytes = max_size_mb * 1024 * 1024
            if file_size > max_size_bytes:
                return {'valid': False, 'error': f"Le fichier est trop volumineux ({file_size / (1024*1024):.1f} Mo). La taille maximale est de {max_size_mb} Mo."}
            if file_size == 0:
                return {'valid': False, 'error': "Le fichier est vide."}
        except (OSError, IOError) as e:
            return {'valid': False, 'error': f"Impossible de lire la taille du fichier : {str(e)}"}
        
        if not os.access(filepath, os.R_OK):
            return {'valid': False, 'error': "Permission de lecture refusée."}
        if not filepath.lower().endswith('.rpy'):
            return {'valid': False, 'error': "Type de fichier non supporté. Veuillez sélectionner un fichier .rpy."}
        
        return {'valid': True, 'size': file_size, 'filename': os.path.basename(filepath)}
        
    except Exception as e:
        # L'anonymisation a été retirée, on logue le chemin directement
        log_message("ERREUR", f"Erreur lors de la validation du fichier {filepath}", exception=e, category="file_validation")
        return {'valid': False, 'error': f"Erreur de validation inattendue : {str(e)}"}

def get_file_base_name(filepath):
    """
    Récupère le nom de base du fichier sans extension.
    """
    if not filepath:
        return "fichier_inconnu"
    filename = os.path.basename(filepath)
    base_name = os.path.splitext(filename)[0]
    return re.sub(r'[<>:"/\\|?*]', '_', base_name)

class TrueDuplicateManager:
    """Gestionnaire pour la détection et la gestion des textes dupliqués."""
    def __init__(self):
        self.duplicate_texts_for_translation = []

class TextExtractor:
    """
    Classe principale pour l'extraction, implémentant la logique complète et l'ordre de protection.
    """
    def __init__(self):
        """Initialise l'extracteur avec préfixes personnalisés"""
        self.file_content = []
        self.original_path = None
        self.extraction_time = 0
        
        # Charger les préfixes personnalisés
        self._load_placeholder_prefixes()
        
        # Charger les paramètres d'extraction
        self._load_extraction_settings()
        
        # Initialiser les données d'extraction
        self._reset_extraction_data()
        
        # Métadonnées pour astérisques et tildes
        self.asterix_metadata = {}
        self.tilde_metadata = {}

    def _load_placeholder_prefixes(self):
        """Charge les patterns courts et initialise les générateurs"""
        try:
            from infrastructure.config.config import config_manager
            from core.services.extraction.placeholder_generator import SimplePlaceholderGenerator
            
            # Validation des préfixes
            is_valid, errors = config_manager.validate_protection_prefixes()
            if not is_valid:
                log_message("ATTENTION", f"Patterns invalides détectés, utilisation des valeurs par défaut. Erreurs: {errors}", category="extraction")
                config_manager.reset_protection_placeholders()
            
            # Récupération des patterns courts
            code_pattern = config_manager.get_protection_placeholder("code_prefix")
            asterisk_pattern = config_manager.get_protection_placeholder("asterisk_prefix")
            tilde_pattern = config_manager.get_protection_placeholder("tilde_prefix")
            
            # Initialisation des générateurs pour patterns courts
            self.code_generator = SimplePlaceholderGenerator(code_pattern)
            self.asterisk_generator = SimplePlaceholderGenerator(asterisk_pattern)
            self.tilde_generator = SimplePlaceholderGenerator(tilde_pattern)
            
            # Le prefix empty reste classique car invisible à l'utilisateur
            self.empty_prefix = "RENPY_EMPTY"
            
            log_message("DEBUG", f"Patterns sauvegardés: CODE='{code_pattern}', ASTERISK='{asterisk_pattern}', TILDE='{tilde_pattern}'", category="ui_settings")
                            
        except Exception as e:
            log_message("ERREUR", f"Erreur chargement générateurs, utilisation valeurs par défaut: {e}", category="extraction")
            # Valeurs par défaut en cas d'erreur
            from core.services.extraction.placeholder_generator import SimplePlaceholderGenerator
            self.code_generator = SimplePlaceholderGenerator("(01)")
            self.asterisk_generator = SimplePlaceholderGenerator("(B1)")
            self.tilde_generator = SimplePlaceholderGenerator("(C1)")
            self.empty_prefix = "RENPY_EMPTY"

    def _load_extraction_settings(self):
        """Charge SEULEMENT le paramètre doublons (le reste est obligatoire)"""
        try:
            from infrastructure.config.config import config_manager
            
            # Seul paramètre configurable
            self.detect_duplicates = config_manager.get('extraction_detect_duplicates', True)
            
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur chargement paramètre doublons, utilisation valeur par défaut: {e}", category="extraction_options")
            self.detect_duplicates = True

    def load_file_content(self, file_content, original_path):
        if not file_content or not isinstance(file_content, list):
            raise ValueError("Contenu de fichier invalide ou manquant")
        if original_path and not (original_path.startswith("clipboard_") and not os.path.exists(original_path)):
            validation = validate_file_safely(original_path)
            if not validation['valid']:
                raise ValueError(f"Fichier non valide: {validation['error']}")
        
        self.file_content = file_content[:]
        self.original_path = original_path
        self._reset_extraction_data()
    
    def _reset_extraction_data(self):
        self.mapping = OrderedDict()
        self.asterix_mapping = OrderedDict()
        self.tilde_mapping = OrderedDict()  # NOUVEAU
        self.empty_mapping = OrderedDict()
        self.positions = []
        self.extracted_texts = []
        self.line_quote_counts = []
        self.line_content_prefixes = []
        self.line_content_suffixes = []
        self.line_suffixes = []
        self.asterix_texts = []
        self.tilde_texts = []  # NOUVEAU
        self.empty_texts = []
        self.all_contents_linear = []
        self.line_to_content_indices = {}
        self.original_lines_with_translations = {}
        self.duplicate_manager = TrueDuplicateManager()
        self.extracted_count = 0
        self.asterix_count = 0
        self.tilde_count = 0  # NOUVEAU
        self.empty_count = 0
        self.asterix_metadata = {}
        self.tilde_metadata = {}  # NOUVEAU

    def _extract_tags_as_prefixes_suffixes(self):
        """
        NOUVELLE ÉTAPE : Extrait les {tags} en début/fin de chaque contenu dialogue
        comme préfixes/suffixes AVANT la protection par placeholders.
        Remplace l'ancien système de pelage des placeholders.
        """
        log_message("DEBUG", "NOUVELLE ÉTAPE : Protection des {tags} comme préfixes/suffixes", category="tag_protection")
        
        try:
            for i, line in enumerate(self.file_content):
                stripped = line.strip()
                if not self._should_process_line(stripped):
                    continue
                
                # Extraire tous les contenus entre guillemets de cette ligne
                raw_contents = self._extract_raw_contents_from_line(line)
                if not raw_contents:
                    continue
                
                # Traiter chaque contenu individuellement
                modified_contents = []
                for content in raw_contents:
                    modified_content = self._extract_tags_from_content(content)
                    modified_contents.append(modified_content)
                
                # Reconstruire la ligne avec les contenus modifiés
                self.file_content[i] = self._rebuild_line_with_modified_contents(line, raw_contents, modified_contents)
                
        except Exception as e:
            log_message("ERREUR", "Erreur lors de l'extraction des tags comme préfixes/suffixes", e, category="tag_protection")
            raise

    def _rebuild_line_with_modified_contents(self, original_line, raw_contents, modified_contents):
        """
        Reconstruit la ligne en remplaçant les contenus originaux par les contenus modifiés.
        """
        rebuilt_line = original_line
        
        # Remplacer chaque contenu original par son contenu modifié
        for i, (original, modified) in enumerate(zip(raw_contents, modified_contents)):
            if original != modified['modified']:
                # Remplacer le contenu entre guillemets
                old_quoted = f'"{original}"'
                new_quoted = f'"{modified["modified"]}"'
                rebuilt_line = rebuilt_line.replace(old_quoted, new_quoted, 1)
        
        return rebuilt_line

    def _extract_tags_from_content(self, content):
        """
        Extrait les {tags} en début et fin d'un contenu spécifique.
        Retourne le contenu modifié sans les tags de début/fin.
        """
        original_content = content
        prefix_tags = ""
        suffix_tags = ""
        
        # Extraire les {tags} en début
        while True:
            match = re.match(r'^(\{[^}]*\})', content)
            if match:
                tag = match.group(1)
                prefix_tags += tag
                content = content[len(tag):]
            else:
                break
        
        # Extraire les {tags} en fin
        while True:
            match = re.search(r'(\{[^}]*\})$', content)
            if match:
                tag = match.group(1)
                suffix_tags = tag + suffix_tags
                content = content[:-len(tag)]
            else:
                break
        
        # Log pour debug
        if prefix_tags or suffix_tags:
            log_message("DEBUG", f"Tags extraits - Original: '{original_content}' -> Préfixe: '{prefix_tags}' + Contenu: '{content}' + Suffixe: '{suffix_tags}'", category="tag_protection")
        
        return {
            'original': original_content,
            'prefix': prefix_tags,
            'content': content,
            'suffix': suffix_tags,
            'modified': content  # Le contenu sans les tags début/fin
        }

    def _extract_raw_contents_from_line(self, line):
        """
        Extrait tous les contenus entre guillemets d'une ligne.
        Gère intelligemment les paramètres en fin de ligne.
        """
        raw_contents = []
        
        if "RENPY_NARRATOR" in line:
            match = re.search(r'RENPY_NARRATOR(.*)"(.*)', line)
            if match:
                raw_contents.append(match.group(1))
        elif "RENPY_EMPTY03" in line:
            match = re.search(r'"(.*)RENPY_EMPTY03(.*)"(.*)', line)
            if match:
                raw_contents.append(match.group(1))
                raw_contents.append(match.group(2))
        else:
            # Détecter s'il y a des paramètres en fin de ligne
            # Pattern pour détecter les paramètres : espaces + ( + contenu + )
            param_pattern = r'\s+\([^)]*\)\s*$'
            
            if re.search(param_pattern, line):
                # Il y a des paramètres en fin, les retirer
                line_clean = re.sub(param_pattern, '', line)
            else:
                # Pas de paramètres détectés, garder la ligne entière
                line_clean = line
                
            matches = re.findall(r'"(.*?)"', line_clean)
            if matches:
                raw_contents.extend(matches)
        
        return raw_contents

    def _extract_asterisk_groups_with_stack(self, line):
        """
        Extrait les groupes d'astérisques en utilisant une logique de pile.
        Similaire à _extract_bracketed_tags mais pour les astérisques.
        """
        groups = []
        i = 0
        
        while i < len(line):
            if line[i] == '*':
                # Début d'un groupe potentiel
                asterisk_count = 1
                start_pos = i
                
                # Avancer tant qu'on trouve des astérisques consécutifs
                j = i + 1
                while j < len(line) and line[j] == '*':
                    asterisk_count += 1
                    j += 1
                
                # Maintenant chercher la fermeture avec le même nombre d'astérisques
                content_start = j
                stack_level = asterisk_count
                current_pos = j
                
                while current_pos < len(line) and stack_level > 0:
                    if line[current_pos] == '*':
                        # Compter les astérisques consécutifs
                        consecutive_asterisks = 0
                        temp_pos = current_pos
                        while temp_pos < len(line) and line[temp_pos] == '*':
                            consecutive_asterisks += 1
                            temp_pos += 1
                        
                        # Si on a le même nombre d'astérisques, c'est une fermeture
                        if consecutive_asterisks >= asterisk_count:
                            # Extraire le contenu
                            content = line[content_start:current_pos]
                            full_group = line[start_pos:current_pos + asterisk_count]
                            
                            groups.append({
                                'full_text': full_group,
                                'content': content,
                                'asterisk_count': asterisk_count,
                                'start_pos': start_pos,
                                'end_pos': current_pos + asterisk_count
                            })
                            
                            # Continuer après ce groupe
                            i = current_pos + asterisk_count - 1
                            break
                        else:
                            # Pas assez d'astérisques, continuer
                            current_pos = temp_pos
                    else:
                        current_pos += 1
                else:
                    # Pas de fermeture trouvée, ignorer ce groupe
                    pass
            
            i += 1
        
        return groups

    def _build_asterix_mapping_with_stack(self):
        """Protection des astérisques avec pattern court"""
        try:
            for i, line in enumerate(self.file_content):
                stripped = line.strip()
                if not self._should_process_line(stripped):
                    continue
                
                temp_line = line
                asterisk_groups = self._extract_asterisk_groups_with_stack(temp_line)
                asterisk_groups.sort(key=lambda x: x['start_pos'], reverse=True)
                
                for group in asterisk_groups:
                    full_text = group['full_text']
                    content = group['content']
                    asterisk_count = group['asterisk_count']
                    
                    if full_text not in self.asterix_mapping:
                        placeholder = self.asterisk_generator.next_placeholder()
                        self.asterix_mapping[full_text] = placeholder
                        
                        # Sauvegarder les métadonnées
                        self.asterix_metadata[placeholder] = {
                            'prefix_count': asterisk_count,
                            'suffix_count': asterisk_count,
                            'content': content,
                            'full_text': full_text
                        }
                        
                        self.asterix_texts.append(content + '\n')
                        log_message("DEBUG", f"Astérisque protégé: '{full_text}' -> {placeholder} -> contenu: '{content}'", category="asterisk_protection")
                    
                    temp_line = temp_line.replace(full_text, self.asterix_mapping[full_text], 1)
                
                self.file_content[i] = temp_line
            
            pattern_info = self.asterisk_generator.get_pattern_info()
                
        except Exception as e:
            log_message("ERREUR", "Erreur détection astérisques", e, category="asterisk_protection")
            raise

    def _build_tilde_mapping_two_pass(self):
        """
        Protection des tildes en DEUX PASSES pour sécuriser complètement
        PASSE 1: Système de pile pour les groupes structurés (~~~mot~~~)
        PASSE 2: Protection des tildes multiples orphelins (~~~ seuls)
        """
        
        try:
            # ==================== PASSE 1: GROUPES STRUCTURÉS ====================
            
            structured_count = 0
            for i, line in enumerate(self.file_content):
                stripped = line.strip()
                if not self._should_process_line(stripped):
                    continue
                
                temp_line = line
                tilde_groups = self._extract_tilde_groups_with_stack(temp_line)
                tilde_groups.sort(key=lambda x: x['start_pos'], reverse=True)
                
                for group in tilde_groups:
                    full_text = group['full_text']
                    content = group['content']
                    tilde_count = group['tilde_count']
                    
                    if full_text not in self.tilde_mapping:
                        placeholder = self.tilde_generator.next_placeholder()
                        self.tilde_mapping[full_text] = placeholder
                        
                        # Sauvegarder les métadonnées
                        self.tilde_metadata[placeholder] = {
                            'prefix_count': tilde_count,
                            'suffix_count': tilde_count,
                            'content': content,
                            'full_text': full_text,
                            'protection_pass': 1  # Marquer comme passe 1
                        }
                        
                        self.tilde_texts.append(content + '\n')
                        structured_count += 1
                        log_message("DEBUG", f"Passe 1 - Tilde protégé: '{full_text}' -> {placeholder}", category="tilde_protection")
                    
                    temp_line = temp_line.replace(full_text, self.tilde_mapping[full_text], 1)
                
                self.file_content[i] = temp_line
            
            # ==================== PASSE 2: TILDES ORPHELINS ====================
            
            orphan_count = 0
            for i, line in enumerate(self.file_content):
                stripped = line.strip()
                if not self._should_process_line(stripped):
                    continue
                
                temp_line = line
                orphan_tildes = self._extract_orphan_tildes(temp_line)
                
                # Traiter les orphelins par ordre décroissant de position
                for orphan in sorted(orphan_tildes, key=lambda x: x['start_pos'], reverse=True):
                    orphan_text = orphan['text']
                    
                    if orphan_text not in self.tilde_mapping:
                        placeholder = self.tilde_generator.next_placeholder()
                        self.tilde_mapping[orphan_text] = placeholder
                        
                        # Métadonnées pour orphelins
                        self.tilde_metadata[placeholder] = {
                            'prefix_count': orphan['count'],
                            'suffix_count': 0,  # Pas de suffixe pour les orphelins
                            'content': '',  # Pas de contenu encadré
                            'full_text': orphan_text,
                            'protection_pass': 2,  # Marquer comme passe 2
                            'orphan': True
                        }
                        
                        # Pour les orphelins, on sauvegarde le symbole lui-même
                        self.tilde_texts.append(orphan_text + '\n')
                        orphan_count += 1
                        log_message("DEBUG", f"Passe 2 - Tilde orphelin protégé: '{orphan_text}' -> {placeholder}", category="tilde_protection")
                    
                    temp_line = temp_line.replace(orphan_text, self.tilde_mapping[orphan_text], 1)
                
                self.file_content[i] = temp_line
            
            pattern_info = self.tilde_generator.get_pattern_info()
                    
        except Exception as e:
            log_message("ERREUR", "Erreur protection tildes 2-passes", e, category="tilde_protection")
            raise

    def _extract_tilde_groups_with_stack(self, line):
        """
        Extrait les groupes de tildes en utilisant une logique de pile.
        Similaire à _extract_asterisk_groups_with_stack mais pour les tildes.
        """
        groups = []
        i = 0
        
        while i < len(line):
            if line[i] == '~':
                # Début d'un groupe potentiel
                tilde_count = 1
                start_pos = i
                
                # Avancer tant qu'on trouve des tildes consécutifs
                j = i + 1
                while j < len(line) and line[j] == '~':
                    tilde_count += 1
                    j += 1
                
                # Maintenant chercher la fermeture avec le même nombre de tildes
                content_start = j
                stack_level = tilde_count
                current_pos = j
                
                while current_pos < len(line) and stack_level > 0:
                    if line[current_pos] == '~':
                        # Compter les tildes consécutifs
                        consecutive_tildes = 0
                        temp_pos = current_pos
                        while temp_pos < len(line) and line[temp_pos] == '~':
                            consecutive_tildes += 1
                            temp_pos += 1
                        
                        # Si on a le même nombre de tildes, c'est une fermeture
                        if consecutive_tildes >= tilde_count:
                            # Extraire le contenu
                            content = line[content_start:current_pos]
                            full_group = line[start_pos:current_pos + tilde_count]
                            
                            groups.append({
                                'full_text': full_group,
                                'content': content,
                                'tilde_count': tilde_count,
                                'start_pos': start_pos,
                                'end_pos': current_pos + tilde_count
                            })
                            
                            # Continuer après ce groupe
                            i = current_pos + tilde_count - 1
                            break
                        else:
                            # Pas assez de tildes, continuer
                            current_pos = temp_pos
                    else:
                        current_pos += 1
                else:
                    # Pas de fermeture trouvée, ignorer ce groupe
                    pass
            
            i += 1
        
        return groups

    def _extract_orphan_tildes(self, line):
        """
        Extrait les séquences de tildes orphelins (2+ tildes consécutifs non structurés)
        """
        orphans = []
        i = 0
        
        while i < len(line):
            if line[i] == '~':
                # Compter les tildes consécutifs
                tilde_count = 0
                start_pos = i
                
                while i < len(line) and line[i] == '~':
                    tilde_count += 1
                    i += 1
                
                # Garder seulement les séquences de 2+ tildes
                # (les simples ~ sont probablement des erreurs typo)
                if tilde_count >= 2:
                    tilde_text = '~' * tilde_count
                    orphans.append({
                        'text': tilde_text,
                        'count': tilde_count,
                        'start_pos': start_pos,
                        'end_pos': i
                    })
            else:
                i += 1
        
        return orphans

    def extract_texts(self):
        """
        Exécute le processus d'extraction complet avec protections obligatoires + doublons configurables.
        VERSION MISE À JOUR avec système de tildes.
        """
        start_time = time.time()
        log_message("INFO", f"📤 Début de l'extraction", category="extraction")
        
        self._reset_extraction_data()
        self._load_extraction_settings()
        
        log_message("INFO", f"  - Détection doublons: {'✅ ACTIVÉE' if self.detect_duplicates else '❌ DÉSACTIVÉE'}", category="extraction")
        
        # ÉTAPE 1: Protection des codes/variables 
        self._build_code_mapping()
        
        # ÉTAPE 2: Protection des textes vides 
        self._apply_empty_text_protection()
        
        # ÉTAPE 3: Protection des astérisques avec pile 
        self._build_asterix_mapping_with_stack()
        
        # Étape 3bis: Protection des tildes en 2 passes
        self._build_tilde_mapping_two_pass()
        
        # ÉTAPE 4: Extraction avec doublons (CONFIGURABLE)
        if self.detect_duplicates:
            log_message("DEBUG", "Étape Final: Extraction des dialogues", category="dialogue_extraction")
            self._extract_dialogue_and_handle_duplicates()
        else:
            log_message("DEBUG", "Étape Final: Extraction des dialogues", category="dialogue_extraction")
            self._extract_dialogue_simple()
        
        
        # ÉTAPE 5: Sauvegarde
        self.extraction_time = time.time() - start_time
        result = self._save_extraction_files()
        
        # Mise à jour des compteurs
        self.extracted_count = len(self.extracted_texts)
        self.asterix_count = len(self.asterix_texts)
        self.tilde_count = len(self.tilde_texts)  # NOUVEAU
        self.empty_count = len(self.empty_texts)
        
        result['extracted_count'] = self.extracted_count
        result['asterix_count'] = self.asterix_count
        result['tilde_count'] = self.tilde_count  # NOUVEAU
        result['empty_count'] = self.empty_count
        result['duplicate_count'] = len(self.duplicate_manager.duplicate_texts_for_translation)

        # STATISTIQUES FINALES
        doublons_count = len(self.duplicate_manager.duplicate_texts_for_translation) if self.detect_duplicates else 0
        log_message("INFO", f"  Dialogues: {self.extracted_count} | Astérisques: {self.asterix_count} | Tildes: {self.tilde_count} | Vides: {self.empty_count} | Doublons: {doublons_count}", category="extraction")
        
        return result

    def _should_process_line(self, stripped_line):
        """
        Détermine si une ligne doit être traitée pour les protections.
        Seules les lignes de dialogue pur et les lignes 'new' sont traitées.
        """
        # Ignorer les commentaires
        if stripped_line.startswith('#'):
            return False
        # Ignorer les directives Ren'Py
        if stripped_line.lower().startswith(('translate', 'old', 'voice')):
            return False
        # Traiter les lignes new (pour les choix)
        if stripped_line.startswith('new '):
            return True
        # Traiter les lignes avec guillemets (dialogues)
        if '"' in stripped_line:
            return True
        return False

    def _extract_dialogue_simple(self):
        """
        Version simplifiée sans détection de doublons (quand detect_duplicates=False)
        CONSERVÉ: Garde la logique de désactivation des doublons
        """
        try:
            
            for idx, line in enumerate(self.file_content):
                stripped = line.strip()
                if not self._is_dialogue_line(stripped):
                    continue

                analysis = self._analyze_and_decompose_line(line)
                if analysis['decomposed_parts']:
                    self.line_to_content_indices[idx] = []
                    
                    for part in analysis['decomposed_parts']:
                        # Ignorer uniquement les placeholders vides structurels
                        if part['text'].startswith(f'{self.empty_prefix}_'):
                            continue
                        
                        # IMPORTANT: Même si le texte est vide après pelage, on doit le garder
                        # car il peut correspondre à un astérisque ou autre contenu traduisible
                        # On met un marqueur spécial pour préserver la ligne dans le fichier de traduction
                        text_to_add = part['text'] if part['text'].strip() else "◊"  # Caractère rare pour garder la ligne
                        
                        content_index = len(self.all_contents_linear)
                        self.all_contents_linear.append(text_to_add)
                        self.line_to_content_indices[idx].append(content_index)
                    
                    if self.line_to_content_indices[idx]:
                        self.original_lines_with_translations[idx] = line
                        self.line_suffixes.append(analysis['line_suffix'])
                        self.line_content_prefixes.append([p['prefix'] for p in analysis['decomposed_parts']])
                        self.line_content_suffixes.append([p['suffix'] for p in analysis['decomposed_parts']])
                    else:
                        # Nettoyer si la ligne ne contenait que des placeholders structurels
                        del self.line_to_content_indices[idx]

            # Sans détection de doublons : tous les textes vont dans extracted_texts
            self.extracted_texts = [content + '\n' for content in self.all_contents_linear]
            

        except Exception as e:
            log_message("ERREUR", "Erreur extraction simple", e, category="dialogue_extraction")
            raise

    def _build_code_mapping(self):
        """Protection des codes avec patterns courts - VERSION CORRIGÉE"""
        try:
            all_tags = set()
            
            # Phase 1: Extraire toutes les balises crochétées
            for line in self.file_content:
                stripped = line.strip()
                if not self._should_process_line(stripped):
                    continue
                    
                # Balises crochétées
                for tag in re.findall(r'\[[^\]]+\]', line):
                    all_tags.add(tag)
            
            sorted_tags = sorted(all_tags, key=len, reverse=True)
            
            for tag in sorted_tags:
                if tag not in self.mapping:
                    placeholder = self.code_generator.next_placeholder()
                    self.mapping[tag] = placeholder
                    log_message("DEBUG", f"Étape 1 - Variable protégée: '{tag}' -> {placeholder}", category="code_protection")

            # Phase 2: Protéger les autres codes
            for i, line in enumerate(self.file_content):
                stripped = line.strip()
                if not self._should_process_line(stripped):
                    continue
                    
                temp_line = line

                # Balises HTML
                for tag in re.findall(r'<[^>]+>', line):
                    if tag not in self.mapping:
                        placeholder = self.code_generator.next_placeholder()
                        self.mapping[tag] = placeholder
                        log_message("DEBUG", f"Étape 1 - Balise HTML protégée: '{tag}' -> {placeholder}", category="code_protection")
                        
                # Balises accolades
                for tag in re.findall(r'\{[^}]+\}', line):
                    if tag not in self.mapping:
                        placeholder = self.code_generator.next_placeholder()
                        self.mapping[tag] = placeholder
                        log_message("DEBUG", f"Étape 1 - Balise accolade protégée: '{tag}' -> {placeholder}", category="code_protection")
                        
                # Codes spéciaux - VERSION CORRIGÉE
                for pattern in SPECIAL_CODES:
                    for match in re.finditer(pattern, line):
                        code = match.group(0)
                        
                        # CORRECTION: Ne pas inclure la guillemet dans la protection
                        if code.endswith('"') and not code.startswith('"'):
                            # Cas spécial: %(player_name)s" -> protéger seulement %(player_name)s
                            code_without_quote = code[:-1]
                            if code_without_quote not in self.mapping:
                                placeholder = self.code_generator.next_placeholder()
                                self.mapping[code_without_quote] = placeholder
                                log_message("DEBUG", f"Étape 1 - Code spécial protégé (sans guillemet): '{code_without_quote}' -> {placeholder}", category="code_protection")
                        else:
                            if code not in self.mapping:
                                placeholder = self.code_generator.next_placeholder()
                                self.mapping[code] = placeholder
                                log_message("DEBUG", f"Étape 1 - Code spécial protégé: '{code}' -> {placeholder}", category="code_protection")
                                
                # Guillemets échappés
                for match in re.finditer(r'\\"', line):
                    code = match.group(0)
                    if code not in self.mapping:
                        placeholder = self.code_generator.next_placeholder()
                        self.mapping[code] = placeholder
                        log_message("DEBUG", f"Étape 1 - Guillemet échappé protégé: '{code}' -> {placeholder}", category="code_protection")

            # Phase 3: Appliquer les remplacements
            sorted_map_items = sorted(self.mapping.items(), key=lambda item: len(item[0]), reverse=True)
            for i, line in enumerate(self.file_content):
                stripped = line.strip()
                if not self._should_process_line(stripped):
                    continue
                    
                temp_line = line
                for original, placeholder in sorted_map_items:
                    temp_line = temp_line.replace(original, placeholder)
                self.file_content[i] = temp_line
                
            pattern_info = self.code_generator.get_pattern_info()
            
        except Exception as e:
            log_message("ERREUR", "Erreur lors de la création du mapping de code", e, category="code_protection")
            raise

    def _extract_bracketed_tags(self, line):
        """
        Extrait les variables crochetées en utilisant une logique de pile.
        """
        tags = []
        i = 0
        while i < len(line):
            if line[i] == '[':
                bracket_count = 1
                for j in range(i + 1, len(line)):
                    if line[j] == '[': bracket_count += 1
                    elif line[j] == ']': bracket_count -= 1
                    
                    if bracket_count == 0:
                        tags.append(line[i : j + 1])
                        i = j 
                        break
            i += 1
        return tags

    def _apply_empty_text_protection(self):
        """Protection des textes vides (garde le système classique car invisible)"""
        try:
            # Garder le système classique pour empty car invisible à l'utilisateur
            narrator_placeholder = f"{self.empty_prefix}_NARRATOR"
            separator_placeholder = f"{self.empty_prefix}_SEP03"
            empty_str_placeholder = f"{self.empty_prefix}_01"
            space_str_placeholder = f"{self.empty_prefix}_02"
            
            # Stockage des correspondances
            self.empty_mapping[narrator_placeholder] = '"" "'
            self.empty_mapping[separator_placeholder] = '" "'
            self.empty_mapping[empty_str_placeholder] = '""'
            self.empty_mapping[space_str_placeholder] = '" "'
            
            log_message("DEBUG", f"Étape 2 - Placeholders empty classiques: {list(self.empty_mapping.keys())}", category="empty_protection")

            for i, line in enumerate(self.file_content):
                stripped = line.strip()
                if not self._should_process_line(stripped):
                    continue
                    
                temp_line = line

                # Gérer les cas structurels
                if '"" "' in temp_line:
                    temp_line = re.sub(r'""\s+"([^"]*)"', f'{narrator_placeholder}\\1"', temp_line)
                    log_message("DEBUG", f"Protection narrateur ligne {i+1}: {narrator_placeholder}", category="empty_protection")
                elif re.search(r'"\s+"', temp_line):
                    temp_line = re.sub(r'"([^"]+)"\s+"([^"]*)"', f'"\\1{separator_placeholder}\\2"', temp_line)
                    log_message("DEBUG", f"Protection séparateur ligne {i+1}: {separator_placeholder}", category="empty_protection")
                
                # Cas de contenu vide
                if temp_line == line:
                    if stripped == '""':
                        self.empty_texts.append('""\n')
                        temp_line = line.replace('""', empty_str_placeholder, 1)
                        log_message("DEBUG", f"Protection chaîne vide ligne {i+1}: {empty_str_placeholder}", category="empty_protection")
                    elif stripped == '" "':
                        self.empty_texts.append('" "\n')
                        temp_line = line.replace('" "', space_str_placeholder, 1)
                        log_message("DEBUG", f"Protection espace ligne {i+1}: {space_str_placeholder}", category="empty_protection")

                self.file_content[i] = temp_line


        except Exception as e:
            log_message("ERREUR", f"Erreur protection textes vides: {e}", e, category="empty_protection")
            raise

    def _build_asterix_mapping_selective(self):
        """
        Protège les contenus entre astérisques.
        CORRIGÉ: Ne traite que les lignes de dialogue et new.
        """
        log_message("DEBUG", "Étape 3: Protection des astérisques", category="asterisk_protection")
        try:
            asterix_counter = 1
            for i, line in enumerate(self.file_content):
                stripped = line.strip()
                # Ne traiter que les lignes de dialogue/new
                if not self._should_process_line(stripped):
                    continue
                    
                temp_line = line
                matches = re.findall(r'(\*.*?\*)', temp_line)
                for match in matches:
                    if match not in self.asterix_mapping:
                        placeholder = f"RENPY_ASTERISK_{asterix_counter:03d}"
                        self.asterix_mapping[match] = placeholder
                        self.asterix_texts.append(match[1:-1] + '\n')
                        asterix_counter += 1
                    temp_line = temp_line.replace(match, self.asterix_mapping[match])
                self.file_content[i] = temp_line
        except Exception as e:
            log_message("ERREUR", "Erreur détection astérisques", e, category="asterisk_protection")
            raise

    def _extract_dialogue_and_handle_duplicates(self):
        """
        Étape finale d'extraction qui décompose les lignes, collecte tous les textes,
        et gère les doublons.
        CONSERVÉ: Garde la logique complète de gestion des doublons
        """
        for idx, line in enumerate(self.file_content):
            stripped = line.strip()
            if not self._is_dialogue_line(stripped):
                continue

            analysis = self._analyze_and_decompose_line(line)
            if analysis['decomposed_parts']:
                self.line_to_content_indices[idx] = []
                
                for part in analysis['decomposed_parts']:
                    # Ignorer uniquement les placeholders vides structurels
                    if part['text'].startswith(f'{self.empty_prefix}_'):
                        continue
                    
                    # IMPORTANT: Même si le texte est vide après pelage, on doit le garder
                    # car il peut correspondre à un astérisque ou autre contenu traduisible
                    # On met un marqueur spécial pour préserver la ligne dans le fichier de traduction
                    text_to_add = part['text'] if part['text'].strip() else "◊"  # Caractère rare pour garder la ligne
                    
                    content_index = len(self.all_contents_linear)
                    self.all_contents_linear.append(text_to_add)
                    self.line_to_content_indices[idx].append(content_index)
                
                if self.line_to_content_indices[idx]:
                    self.original_lines_with_translations[idx] = line
                    self.line_suffixes.append(analysis['line_suffix'])
                    self.line_content_prefixes.append([p['prefix'] for p in analysis['decomposed_parts']])
                    self.line_content_suffixes.append([p['suffix'] for p in analysis['decomposed_parts']])
                else:
                    # Nettoyer si la ligne ne contenait que des placeholders structurels
                    del self.line_to_content_indices[idx]

        if self.detect_duplicates:
            # Logique complète de détection des doublons
            content_counts = OrderedDict()
            for content in self.all_contents_linear:
                content_counts[content] = content_counts.get(content, 0) + 1
            
            for content, count in content_counts.items():
                if count > 1:
                    self.duplicate_manager.duplicate_texts_for_translation.append(content + '\n')
                else:
                    self.extracted_texts.append(content + '\n')
                    
            log_message("INFO", f"✅ Extraction terminée: {len(self.extracted_texts)} dialogues", category="dialogue_extraction")
        else:
            # Fallback au cas où (ne devrait pas arriver dans extract_texts)
            self.extracted_texts = [content + '\n' for content in self.all_contents_linear]

    def _is_dialogue_line(self, line):
        # Ignorer les commentaires, directives et old
        if line.startswith('#') or line.lower().startswith(('translate', 'old', 'voice')):
            return False
        
        stripped = line.strip()
        
        # NOUVEAU : Ignorer les lignes qui ne contiennent que des placeholders empty
        if stripped == 'RENPY_EMPTY01' or stripped == 'RENPY_EMPTY02':
            return False
        
        # Traiter seulement les lignes avec guillemets (dialogues) ou new (choix)
        if stripped.startswith('new '):
            return True
        if '"' in line or 'RENPY_NARRATOR' in line or stripped == 'RENPY_EMPTY03':
            return True
        return False

    def _analyze_and_decompose_line(self, line):
        """
        Analyse une ligne pour extraire les textes.
        Maintenant utilise les {tags} comme préfixes/suffixes au lieu des placeholders.
        """
        decomposed_parts = []
        line_suffix = ""
        raw_contents = []

        # Extraction des contenus (logique mise à jour pour gérer les paramètres)
        narrator_placeholder = f"{self.empty_prefix}_NARRATOR"
        narrator_pattern = rf'(?:RENPY_NARRATOR|{re.escape(narrator_placeholder)})'
        narrator_match = re.search(rf'{narrator_pattern}(.*)"(.*)', line)
        
        if narrator_match:
            raw_contents.append(narrator_match.group(1))
            line_suffix = narrator_match.group(2)
        elif "RENPY_EMPTY03" in line:
            match = re.search(r'"(.*)RENPY_EMPTY03(.*)"(.*)', line)
            if match:
                raw_contents.append(match.group(1))
                raw_contents.append(match.group(2))
                line_suffix = match.group(3)
        else:
            # LOGIQUE MISE À JOUR : Détecter et séparer les paramètres
            param_pattern = r'\s+\([^)]*\)\s*$'
            param_match = re.search(param_pattern, line)
            
            if param_match:
                # Il y a des paramètres, les séparer
                line_clean = line[:param_match.start()]  # Partie avant les paramètres
                line_suffix = line[param_match.start():]  # Les paramètres deviennent le suffix
            else:
                # Pas de paramètres
                line_clean = line
                # Calculer line_suffix normalement
                last_quote_pos = line.rfind('"')
                if last_quote_pos != -1:
                    line_suffix = line[last_quote_pos + 1:].rstrip()
            
            matches = re.findall(r'"(.*?)"', line_clean)
            if matches:
                raw_contents.extend(matches)

        # Extraction des {tags} comme préfixes/suffixes (inchangé)
        for content in raw_contents:
            prefix_tags = ""
            suffix_tags = ""
            clean_content = content
            
            # Extraire les {tags} en début
            while True:
                match = re.match(r'^(\{[^}]*\})', clean_content)
                if match:
                    tag = match.group(1)
                    prefix_tags += tag
                    clean_content = clean_content[len(tag):]
                else:
                    break
            
            # Extraire les {tags} en fin
            while True:
                match = re.search(r'(\{[^}]*\})$', clean_content)
                if match:
                    tag = match.group(1)
                    suffix_tags = tag + suffix_tags
                    clean_content = clean_content[:-len(tag)]
                else:
                    break
            
            decomposed_parts.append({
                'prefix': prefix_tags,
                'text': clean_content,
                'suffix': suffix_tags
            })

        return {'decomposed_parts': decomposed_parts, 'line_suffix': line_suffix}

    def _save_extraction_files(self):
        """
        Sauvegarde tous les fichiers générés par l'extraction.
        VERSION UNIFIÉE - tout dans positions.json avec tildes.
        """
        file_base = get_file_base_name(self.original_path)
        game_name = extract_game_name(self.original_path) if self.original_path else "jeu_inconnu"
        
        result = {
            'file_base': file_base, 'files_to_open': [],
            'dialogue_file': None, 'doublons_file': None, 'asterix_file': None, 'tilde_file': None, 'empty_file': None
        }
        
        temp_folder = os.path.join(FOLDERS["temporaires"], game_name, file_base)
        translate_folder = os.path.join(temp_folder, "fichiers_a_traduire")
        reference_folder = os.path.join(temp_folder, "fichiers_a_ne_pas_traduire")
        os.makedirs(translate_folder, exist_ok=True)
        os.makedirs(reference_folder, exist_ok=True)

        # Sauvegarder le fichier avec placeholders
        placeholders_file = os.path.join(reference_folder, f'{file_base}_with_placeholders.rpy')
        with open(placeholders_file, 'w', encoding='utf-8') as f:
            f.writelines(self.file_content)
        log_message("DEBUG", f"Fichier with_placeholders.rpy sauvegardé: {placeholders_file}", category="persistence")

        # Mapping invisible AMÉLIORÉ avec métadonnées (pour lecture humaine)
        invisible_mapping_file = os.path.join(reference_folder, f'{file_base}_invisible_mapping.txt')
        with open(invisible_mapping_file, 'w', encoding='utf-8') as f:
            # Mappings standards
            for tag, ph in self.mapping.items(): 
                f.write(f"{ph} => {tag}\n")
            for tag, ph in self.empty_mapping.items(): 
                f.write(f"{ph} => {tag}\n")
            
            # Mappings astérisques avec métadonnées (pour info)
            f.write("\n# === ASTÉRISQUES AVEC MÉTADONNÉES ===\n")
            for tag, ph in self.asterix_mapping.items():
                if ph in self.asterix_metadata:
                    meta = self.asterix_metadata[ph]
                    f.write(f"{ph} => {tag} [PREFIX:{meta['prefix_count']}*, SUFFIX:{meta['suffix_count']}*, CONTENT:'{meta['content']}']\n")
                else:
                    f.write(f"{ph} => {tag}\n")
            
            # NOUVEAU: Mappings tildes avec métadonnées (pour info)
            f.write("\n# === TILDES AVEC MÉTADONNÉES ===\n")
            for tag, ph in self.tilde_mapping.items():
                if ph in self.tilde_metadata:
                    meta = self.tilde_metadata[ph]
                    f.write(f"{ph} => {tag} [PREFIX:{meta['prefix_count']}~, SUFFIX:{meta['suffix_count']}~, CONTENT:'{meta['content']}']\n")
                else:
                    f.write(f"{ph} => {tag}\n")
        
        # POSITION DATA ENRICHIE - FICHIER UNIQUE AVEC TOUT
        position_data = {
            'line_to_content_indices': {str(k): v for k, v in self.line_to_content_indices.items()},
            'original_lines': {str(k): v for k, v in self.original_lines_with_translations.items()},
            'all_contents_linear': self.all_contents_linear,
            'suffixes': self.line_suffixes,
            'content_prefixes': self.line_content_prefixes,
            'content_suffixes': self.line_content_suffixes,
            
            # MÉTADONNÉES ASTÉRISQUES INTÉGRÉES
            'asterix_metadata': self.asterix_metadata,
            
            # NOUVEAU : MÉTADONNÉES TILDES INTÉGRÉES
            'tilde_metadata': self.tilde_metadata,
            
            # VERSION ET INFO (pour compatibilité future)
            'metadata_version': '2.8.0',
            'extraction_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'has_asterix_metadata': len(self.asterix_metadata) > 0,
            'has_tilde_metadata': len(self.tilde_metadata) > 0  # NOUVEAU
        }
        
        positions_file = os.path.join(reference_folder, f'{file_base}_positions.json')
        with open(positions_file, 'w', encoding='utf-8') as f:
            json.dump(position_data, f, ensure_ascii=False, indent=2)
        
        log_message("DEBUG", f"Positions + métadonnées astérisques + tildes sauvegardées: {positions_file}", category="persistence")

        # Fichiers de traduction avec limite de lignes
        dialogue_files = self._save_texts_with_limit(
            self.extracted_texts, 
            translate_folder, 
            f'{file_base}_dialogue.txt',
            'dialogue'
        )
        result['dialogue_files'] = dialogue_files
        result['files_to_open'].extend(dialogue_files)

        if self.duplicate_manager.duplicate_texts_for_translation:
            doublons_files = self._save_texts_with_limit(
                self.duplicate_manager.duplicate_texts_for_translation,
                translate_folder,
                f'{file_base}_doublons.txt',
                'doublons'
            )
            result['doublons_files'] = doublons_files
            result['files_to_open'].extend(doublons_files)
        
        # Fichier unifié astérisques et tildes avec limite
        if self.asterix_texts or self.tilde_texts:
            combined_texts = []
            if self.asterix_texts:
                combined_texts.extend(self.asterix_texts)
            if self.tilde_texts:
                combined_texts.extend(self.tilde_texts)
            
            asterix_files = self._save_texts_with_limit(
                combined_texts,
                translate_folder,
                f'{file_base}_asterix.txt',
                'asterix'
            )
            result['asterix_files'] = asterix_files
            result['files_to_open'].extend(asterix_files)
            # Supprimer la référence séparée aux tildes
            result['tilde_file'] = None
        
        if self.empty_texts:
            empty_file = os.path.join(reference_folder, f'{file_base}_empty.txt')
            with open(empty_file, 'w', encoding='utf-8') as f:
                f.writelines(self.empty_texts)
            result['empty_file'] = empty_file

        return result

    def _save_texts_with_limit(self, texts, folder, base_filename, file_type):
        """Sauvegarde les textes en respectant la limite de lignes configurée"""
        try:
            from infrastructure.config.config import config_manager
            
            # Récupérer la limite configurée
            line_limit = config_manager.get('extraction_line_limit')
            
            # Si pas de limite ou limite très élevée, sauvegarder en un seul fichier
            if not line_limit or line_limit <= 0 or len(texts) <= line_limit:
                single_file = os.path.join(folder, base_filename)
                with open(single_file, 'w', encoding='utf-8') as f:
                    # S'assurer que chaque ligne se termine par un retour à la ligne
                    for line in texts:
                        if not line.endswith('\n'):
                            line += '\n'
                        f.write(line)
                log_message("INFO", f"Fichier {file_type} créé: {single_file} ({len(texts)} lignes)", category="extraction")
                return [single_file]
            
            # Diviser en plusieurs fichiers
            files_created = []
            file_count = 1
            
            for i in range(0, len(texts), line_limit):
                chunk = texts[i:i + line_limit]
                
                # Nom du fichier avec numéro
                if file_count == 1:
                    filename = base_filename
                else:
                    name, ext = os.path.splitext(base_filename)
                    filename = f"{name}_{file_count}{ext}"
                
                file_path = os.path.join(folder, filename)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    # S'assurer que chaque ligne se termine par un retour à la ligne
                    for line in chunk:
                        if not line.endswith('\n'):
                            line += '\n'
                        f.write(line)
                
                files_created.append(file_path)
                file_count += 1
            
            log_message("INFO", f"Fichiers {file_type} divisés: {len(files_created)} fichiers pour {len(texts)} lignes (limite: {line_limit})", category="extraction")
            return files_created
            
        except Exception as e:
            log_message("ERREUR", f"Erreur sauvegarde avec limite: {e}", category="extraction")
            # Fallback: sauvegarder en un seul fichier
            single_file = os.path.join(folder, base_filename)
            with open(single_file, 'w', encoding='utf-8') as f:
                # S'assurer que chaque ligne se termine par un retour à la ligne
                for line in texts:
                    if not line.endswith('\n'):
                        line += '\n'
                    f.write(line)
            return [single_file]

def extraire_textes_organised(file_content, original_path):
    extractor = TextExtractor
    extractor.load_file_content(file_content, original_path)
    return extractor.extract_texts()
