# core/reconstruction.py
# Reconstruction Functions Module
# Created for RenExtract 

"""
Module de reconstruction des fichiers traduits
"""

import os
import re
import time
import json
from collections import OrderedDict
from core.services.extraction.extraction import get_file_base_name
from infrastructure.config.constants import FOLDERS
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import extract_game_name

class FileReconstructor:
    """
    Classe principale pour la reconstruction.
    """
    def __init__(self):
        """
        Classe principale pour la reconstruction.
        MODIFIÉ: Charge les préfixes personnalisés
        """
        self.file_content = []
        self.original_path = None
        self.reconstruction_time = 0
        
        # Charger les préfixes personnalisés
        self._load_placeholder_prefixes()
        
        # Charger les paramètres de reconstruction
        self._load_reconstruction_settings()
        
        # Initialiser les données
        self._reset_reconstruction_data()

    def _load_placeholder_prefixes(self):
        """Charge les patterns personnalisés et initialise les générateurs (même logique que l'extraction)"""
        try:
            from infrastructure.config.config import config_manager
            from core.services.extraction.placeholder_generator import SimplePlaceholderGenerator
            
            # Validation des préfixes
            is_valid, errors = config_manager.validate_protection_prefixes()
            if not is_valid:
                log_message("ATTENTION", f"Patterns invalides détectés pour reconstruction, utilisation des valeurs par défaut. Erreurs: {errors}", category="reconstruction")
                config_manager.reset_protection_placeholders()
            
            # Récupération des patterns (IDENTIQUES à l'extraction)
            code_pattern = config_manager.get_protection_placeholder("code_prefix")
            asterisk_pattern = config_manager.get_protection_placeholder("asterisk_prefix")
            tilde_pattern = config_manager.get_protection_placeholder("tilde_prefix")
            empty_pattern = config_manager.get_protection_placeholder("empty_prefix")
            
            # Créer des générateurs pour comprendre les patterns (même logique que extraction)
            self.code_generator = SimplePlaceholderGenerator(code_pattern)
            self.asterisk_generator = SimplePlaceholderGenerator(asterisk_pattern)
            self.tilde_generator = SimplePlaceholderGenerator(tilde_pattern)
            
            # Pour EMPTY, on garde le système classique car invisible
            self.empty_prefix = "RENPY_EMPTY"
            
            # Extraire les préfixes des générateurs pour la compatibilité
            code_info = self.code_generator.get_pattern_info()
            asterisk_info = self.asterisk_generator.get_pattern_info()
            tilde_info = self.tilde_generator.get_pattern_info()
            
            self.code_prefix_base = code_info.get('prefix', code_pattern)
            self.asterisk_prefix_base = asterisk_info.get('prefix', asterisk_pattern)  
            self.tilde_prefix_base = tilde_info.get('prefix', tilde_pattern)
            
            log_message("DEBUG", f"Patterns sauvegardés: CODE='{code_pattern}', ASTERISK='{asterisk_pattern}', TILDE='{tilde_pattern}'", category="ui_settings")
                            
        except Exception as e:
            log_message("ERREUR", f"Erreur chargement générateurs reconstruction, utilisation valeurs par défaut: {e}", category="reconstruction")
            # Valeurs par défaut en cas d'erreur
            from core.services.extraction.placeholder_generator import SimplePlaceholderGenerator
            self.code_generator = SimplePlaceholderGenerator("RENPY_CODE_001")
            self.asterisk_generator = SimplePlaceholderGenerator("RENPY_ASTERISK_001")
            self.tilde_generator = SimplePlaceholderGenerator("RENPY_TILDE_001")
            self.empty_prefix = "RENPY_EMPTY"
            self.code_prefix_base = "RENPY_CODE"
            self.asterisk_prefix_base = "RENPY_ASTERISK"
            self.tilde_prefix_base = "RENPY_TILDE"

    def load_file_content(self, file_content, original_path):
        if not file_content or not isinstance(file_content, list):
            raise ValueError("Contenu de fichier invalide ou manquant")
        
        file_base = get_file_base_name(original_path)
        game_name = extract_game_name(original_path)
        reference_folder = os.path.join(FOLDERS["temporaires"], game_name, file_base, "fichiers_a_ne_pas_traduire")
        placeholders_path = os.path.join(reference_folder, f'{file_base}_with_placeholders.rpy')
        
        if os.path.exists(placeholders_path):
            with open(placeholders_path, 'r', encoding='utf-8') as f:
                self.file_content = f.readlines()
        else:
            self.file_content = file_content[:]
            log_message("ATTENTION", "Fichier with_placeholders.rpy non trouvé, utilisation du fichier original", category="reconstruction_io")
            
        self.original_path = original_path

    def _reset_reconstruction_data(self):
        self.mapping = OrderedDict()
        self.empty_mapping = OrderedDict()
        self.asterix_mapping = OrderedDict()
        self.tilde_mapping = OrderedDict()  # NOUVEAU
        self.translations = []
        self.duplicate_translations = []
        self.asterix_translations = []
        self.tilde_translations = []  # NOUVEAU
        self.line_to_content_indices = {}
        self.original_lines = {}
        self.all_contents_linear = []
        self.suffixes = []
        self.content_prefixes = []
        self.content_suffixes = []
        self.asterix_metadata = {}
        self.tilde_metadata = {}  # NOUVEAU

    def reconstruct_file(self, save_mode='new_file'):
        start_time = time.time()
        try:
            self._load_data_for_reconstruction()
            reconstructed_content = self._rebuild_content()
            save_path = self._save_reconstructed_file(reconstructed_content, save_mode)
            self.reconstruction_time = time.time() - start_time
            log_message("INFO", f"✅ Reconstruction réussie en {self.reconstruction_time:.2f}s", category="reconstruction")
            return {'save_path': save_path}
        except Exception as e:
            log_message("ERREUR", f"💥 Erreur critique de reconstruction: {e}", category="reconstruction")
            raise

    def _load_data_for_reconstruction(self):
        """
        Charge les données nécessaires à la reconstruction
        CORRIGÉ: Classification intelligente des placeholders sans deviner leur structure
        """
        file_base = get_file_base_name(self.original_path)
        game_name = extract_game_name(self.original_path)
        
        reference_folder = os.path.join(FOLDERS["temporaires"], game_name, file_base, "fichiers_a_ne_pas_traduire")
        translate_folder = os.path.join(FOLDERS["temporaires"], game_name, file_base, "fichiers_a_traduire")

        # Chargement mapping avec CLASSIFICATION INTELLIGENTE
        mapping_file = os.path.join(reference_folder, f'{file_base}_invisible_mapping.txt')
        with open(mapping_file, 'r', encoding='utf-8') as f:
            for line in f:
                if " => " in line and not line.strip().startswith('#'):
                    # Nettoyer la ligne pour gérer les métadonnées
                    clean_line = line.strip()
                    if '[PREFIX:' in clean_line:
                        # Ligne avec métadonnées : "placeholder => tag [PREFIX:2*, SUFFIX:2*, CONTENT:'content']"
                        ph, rest = clean_line.split(" => ", 1)
                        tag = rest.split(" [PREFIX:")[0]  # Récupérer juste la partie tag
                    else:
                        # Ligne simple : "placeholder => tag"
                        ph, tag = clean_line.split(" => ", 1)
                    
                    # NOUVELLE LOGIQUE : Classification par contenu du tag au lieu de structure du placeholder
                    placeholder_type = self._classify_placeholder_by_content(ph, tag)
                    
                    if placeholder_type == 'asterisk':
                        self.asterix_mapping[ph] = tag
                        log_message("DEBUG", f"Asterisk mapping détecté: {ph} => {tag}", category="reconstruction_load")
                    elif placeholder_type == 'tilde':
                        self.tilde_mapping[ph] = tag
                        log_message("DEBUG", f"Tilde mapping détecté: {ph} => {tag}", category="reconstruction_load")
                    elif placeholder_type == 'empty':
                        self.empty_mapping[ph] = tag
                        log_message("DEBUG", f"Empty mapping détecté: {ph} => {tag}", category="reconstruction_load")
                    else:  # 'code' par défaut
                        self.mapping[ph] = tag
                        log_message("DEBUG", f"Code mapping détecté: {ph} => {tag}", category="reconstruction_load")

        # Le reste du chargement reste identique...
        positions_file = os.path.join(reference_folder, f'{file_base}_positions.json')
        with open(positions_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.line_to_content_indices = {int(k): v for k, v in data['line_to_content_indices'].items()}
            self.original_lines = {int(k): v for k, v in data['original_lines'].items()}
            self.all_contents_linear = data['all_contents_linear']
            self.suffixes = data['suffixes']
            self.content_prefixes = data.get('content_prefixes', [])
            self.content_suffixes = data.get('content_suffixes', [])
            
            # Charger les métadonnées
            if 'asterix_metadata' in data:
                self.asterix_metadata = data['asterix_metadata']
            else:
                self.asterix_metadata = {}

            if 'tilde_metadata' in data:
                self.tilde_metadata = data['tilde_metadata']
            else:
                self.tilde_metadata = {}

        # Chargement des traductions avec support multi-fichiers
        raw_translations = self._load_translation_files(translate_folder, f'{file_base}_dialogue.txt')
        self.translations = [line.rstrip('\n\r') for line in raw_translations]
        
        doublons_files = self._find_translation_files(translate_folder, f'{file_base}_doublons.txt')
        if doublons_files:
            raw_duplicates = self._load_translation_files(translate_folder, f'{file_base}_doublons.txt')
            self.duplicate_translations = [line.rstrip('\n\r') for line in raw_duplicates]

        # Chargement unifié astérisques et tildes avec support multi-fichiers
        asterix_files = self._find_translation_files(translate_folder, f'{file_base}_asterix.txt')
        if asterix_files:
            raw_asterix_lines = self._load_translation_files(translate_folder, f'{file_base}_asterix.txt')
            all_lines = [line.rstrip('\n\r') for line in raw_asterix_lines]
            
            # Séparer astérisques et tildes selon les compteurs d'extraction
            asterix_count = len(self.asterix_mapping)
            tilde_count = len(self.tilde_mapping)
            
            if asterix_count > 0:
                self.asterix_translations = all_lines[:asterix_count]
            if tilde_count > 0:
                self.tilde_translations = all_lines[asterix_count:asterix_count + tilde_count]

        # Calculer le total de lignes chargées
        total_dialogue = len(self.translations)
        total_asterix = len(self.asterix_translations)
        total_tilde = len(self.tilde_translations)
        total_lines = total_dialogue + total_asterix + total_tilde
        
        log_message("INFO", f"📂 Chargement : {total_lines} lignes (dialogue:{total_dialogue}, astérisques:{total_asterix}, tildes:{total_tilde})", category="reconstruction")

    def _find_translation_files(self, folder, base_filename):
        """Trouve tous les fichiers de traduction (avec ou sans numérotation)"""
        try:
            import glob
            
            # Chercher tous les fichiers (principal + numérotés)
            name, ext = os.path.splitext(base_filename)
            
            # Pattern pour le fichier principal
            main_file = os.path.join(folder, base_filename)
            
            # Pattern pour les fichiers numérotés
            numbered_pattern = os.path.join(folder, f"{name}_*{ext}")
            numbered_files = glob.glob(numbered_pattern)
            
            # Combiner tous les fichiers trouvés
            all_files = []
            
            # Ajouter le fichier principal s'il existe
            if os.path.exists(main_file):
                all_files.append(main_file)
            
            # Ajouter les fichiers numérotés
            all_files.extend(numbered_files)
            
            if all_files:
                # Trier par numéro pour garantir l'ordre
                all_files.sort(key=lambda x: self._extract_file_number(x, base_filename))
                log_message("DEBUG", f"Fichiers trouvés: {[os.path.basename(f) for f in all_files]}", category="reconstruction")
                return all_files
            
            return []
            
        except Exception as e:
            return []

    def _extract_file_number(self, filepath, base_filename):
        """Extrait le numéro d'un fichier pour le tri"""
        try:
            filename = os.path.basename(filepath)
            name, ext = os.path.splitext(base_filename)
            
            if filename == base_filename:
                return 0  # Fichier principal
            
            # Extraire le numéro du pattern name_1.txt, name_2.txt, etc.
            pattern = f"{name}_"
            if filename.startswith(pattern):
                number_part = filename[len(pattern):-len(ext)]
                return int(number_part)
            
            return 999  # En dernier si pas de numéro
            
        except Exception:
            return 999

    def _load_translation_files(self, folder, base_filename):
        """Charge tous les fichiers de traduction comme un seul contenu"""
        try:
            files = self._find_translation_files(folder, base_filename)
            
            if not files:
                return []
            
            all_lines = []
            for file_path in files:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()  # Garder les retours à la ligne originaux
                    all_lines.extend(lines)
                    log_message("DEBUG", f"Fichier chargé: {file_path} ({len(lines)} lignes)", category="reconstruction")
            
            # Log supprimé : sera regroupé avec le log final de reconstruction
            return all_lines
            
        except Exception as e:
            log_message("ERREUR", f"Erreur chargement fichiers traduction: {e}", category="reconstruction")
            return []

    def _classify_placeholder_by_content(self, placeholder, tag):
        """
        Classifie un placeholder en analysant son CONTENU (tag) plutôt que sa structure.
        Cette méthode est agnostique du pattern utilisé par l'utilisateur.
        """
        try:
            # 1. Classification par analyse du contenu du tag
            if tag.startswith('*') and tag.endswith('*'):
                return 'asterisk'
            elif tag.startswith('~') and tag.endswith('~'):
                return 'tilde'
            elif tag in ['""', '" "', '"" "']:
                return 'empty'
            elif tag.startswith('<') and tag.endswith('>'):
                return 'code'  # Balises HTML
            elif tag.startswith('{') and tag.endswith('}'):
                return 'code'  # Balises Ren'Py
            elif tag.startswith('[') and tag.endswith(']'):
                return 'code'  # Variables
            
            # 2. Classification par mots-clés dans le placeholder (fallback)
            ph_upper = placeholder.upper()
            if "ASTERISK" in ph_upper:
                return 'asterisk'
            elif "TILDE" in ph_upper:
                return 'tilde'
            elif "EMPTY" in ph_upper or "NARRATOR" in ph_upper:
                return 'empty'
            
            # 3. Par défaut : code
            return 'code'
            
        except Exception as e:
            return 'code'  # Fallback sécurisé

    def _is_code_placeholder(self, placeholder):
        """Détermine si un placeholder est un code généré par notre système"""
        try:
            # Test par pattern du générateur
            pattern_info = self.code_generator.get_pattern_info()
            pattern_type = pattern_info.get('type', '')
            
            if pattern_type == 'underscore_numeric':
                # Pattern comme RENPY_CODE_001 ou (01) -> (02)
                prefix = pattern_info.get('prefix', '')
                if prefix and placeholder.startswith(f"{prefix}_"):
                    return True
            elif pattern_type == 'only_paren_numeric':
                # Pattern comme (01) -> (02)
                return re.match(r'^\(\d+\)$', placeholder) is not None
            elif pattern_type == 'alpha_numeric_paren':
                # Pattern comme (B01) -> (B02) mais pour codes (pas normal)
                return re.match(r'^\([A-Z]\d+\)$', placeholder) is not None
            elif pattern_type == 'simple_prefix':
                # Pattern simple comme CODE -> CODE_001
                prefix = pattern_info.get('prefix', '')
                if prefix and placeholder.startswith(f"{prefix}_"):
                    return True
                    
            return False
        except Exception:
            return False

    def _is_asterisk_placeholder(self, placeholder):
        """Détermine si un placeholder est un astérisque généré par notre système"""
        try:
            pattern_info = self.asterisk_generator.get_pattern_info()
            pattern_type = pattern_info.get('type', '')
            
            if pattern_type == 'alpha_numeric_paren':
                # Pattern comme (B01) -> (B02)
                letter = pattern_info.get('format_info', {}).get('letter', 'B')
                return placeholder.startswith(f"({letter}") and placeholder.endswith(')')
            elif pattern_type == 'underscore_numeric':
                # Pattern comme RENPY_ASTERISK_001
                prefix = pattern_info.get('prefix', '')
                if prefix and placeholder.startswith(f"{prefix}_"):
                    return True
            elif pattern_type == 'only_paren_numeric':
                # Si les astérisques utilisent (01) -> (02) (cas rare)
                return re.match(r'^\(\d+\)$', placeholder) is not None
                
            return False
        except Exception:
            return False

    def _is_tilde_placeholder(self, placeholder):
        """Détermine si un placeholder est un tilde généré par notre système"""
        try:
            pattern_info = self.tilde_generator.get_pattern_info()
            pattern_type = pattern_info.get('type', '')
            
            if pattern_type == 'alpha_numeric_paren':
                # Pattern comme (C01) -> (C02)
                letter = pattern_info.get('format_info', {}).get('letter', 'C')
                return placeholder.startswith(f"({letter}") and placeholder.endswith(')')
            elif pattern_type == 'underscore_numeric':
                # Pattern comme RENPY_TILDE_001
                prefix = pattern_info.get('prefix', '')
                if prefix and placeholder.startswith(f"{prefix}_"):
                    return True
            elif pattern_type == 'only_paren_numeric':
                # Si les tildes utilisent (01) -> (02) (cas rare)
                return re.match(r'^\(\d+\)$', placeholder) is not None
                
            return False
        except Exception:
            return False

    def _is_empty_placeholder(self, placeholder):
        """Détermine si un placeholder est un empty (système classique)"""
        return (placeholder.startswith(f"{self.empty_prefix}_") or 
                placeholder == f"{self.empty_prefix}_NARRATOR" or
                "EMPTY" in placeholder.upper() or 
                "NARRATOR" in placeholder.upper())

    def _rebuild_content(self):
        output_lines = self.file_content[:]
        
        translation_map = self._build_translation_map()
        self._restore_asterisks()
        self._restore_tildes_two_pass()
        
        # Logs de restauration pour codes et vides (restaurés automatiquement lors du nettoyage)
        codes_count = len(self.mapping)
        vides_count = len(self.empty_mapping)
        log_message("DEBUG", f"✅ Codes restaurés: {codes_count} placeholders", category="code_restoration")
        log_message("DEBUG", f"✅ Vides restaurés: {vides_count} placeholders", category="empty_restoration")

        # PRÉ-CALCULER TOUS les mappings pour éviter TOUTES les recherches O(n)
        line_idx_to_meta_idx = {line_idx: i for i, line_idx in enumerate(self.original_lines.keys())}

        for line_idx, content_indices in self.line_to_content_indices.items():
            original_line = self.original_lines.get(line_idx)
            if not original_line: continue
            
            # Récupérer les préfixes/suffixes pour cette ligne spécifique
            meta_idx = line_idx_to_meta_idx.get(line_idx)
            prefixes = self.content_prefixes[meta_idx] if meta_idx is not None and meta_idx < len(self.content_prefixes) else [""] * len(content_indices)
            suffixes = self.content_suffixes[meta_idx] if meta_idx is not None and meta_idx < len(self.content_suffixes) else [""] * len(content_indices)
            line_suffix = self.suffixes[meta_idx] if meta_idx is not None and meta_idx < len(self.suffixes) else ""
            
            # Reconstruire les contenus complets (avec préfixes/suffixes)
            full_new_contents = []
            for i, content_idx in enumerate(content_indices):
                original_text = self.all_contents_linear[content_idx]
                
                # Gérer le marqueur spécial ◦
                if original_text == "◦":
                    translated_text = translation_map.get(original_text, "")
                    if translated_text == "◦" or not translated_text:
                        translated_text = ""
                else:
                    translated_text = translation_map.get(original_text, original_text)
                
                prefix = prefixes[i] if i < len(prefixes) else ""
                suffix = suffixes[i] if i < len(suffixes) else ""
                full_new_contents.append(f"{prefix}{translated_text}{suffix}")

            rebuilt_line = self._reassemble_line_optimized(line_idx, original_line, full_new_contents, line_suffix)
            output_lines[line_idx] = rebuilt_line
        
        # NETTOYAGE ITÉRATIF des placeholders pour gérer les imbrications
        all_mappings = {**self.mapping, **self.empty_mapping, **self.asterix_mapping, **self.tilde_mapping}
        sorted_keys = sorted(all_mappings.keys(), key=len, reverse=True)
        
        # Restaurer les placeholders sur TOUTES les lignes avec approche itérative
        # MAIS ignorer les lignes commentées pour éviter de casser leur syntaxe
        max_iterations = 10
        for iteration in range(max_iterations):
            replacements_made = False
            
            for i, line in enumerate(output_lines):
                # NE PAS modifier les lignes commentées (elles ne sont pas extraites donc pas traduites)
                if line.strip().startswith('#'):
                    continue
                
                original_line = line
                
                # Appliquer tous les remplacements sur cette ligne
                for key in sorted_keys:
                    if key in line:
                        line = line.replace(key, all_mappings[key])
                
                # Vérifier si des changements ont été faits
                if line != original_line:
                    replacements_made = True
                    output_lines[i] = line
            
            # Si aucun remplacement n'a été fait, on peut arrêter
            if not replacements_made:
                break
        else:
            log_message("ATTENTION", f"Nettoyage des placeholders interrompu après {max_iterations} itérations", category="placeholder_cleanup")
        
        # POST-TRAITEMENT: Corriger les placeholders empty restants
        output_lines = self._post_process_empty_placeholders(output_lines)
                
        return output_lines

    def _comment_original_file(self):
        """Commente toutes les lignes non-vides du fichier original, même celles déjà commentées"""
        if not isinstance(self.original_path, str) or not self.original_path:
            log_message("ERREUR", "Le chemin du fichier original (original_path) n'est pas défini ou n'est pas une chaîne de caractères.", category="reconstruction_comment")
            return False
        
        try:
            # Lire le fichier original
            with open(self.original_path, 'r', encoding='utf-8') as f:
                original_lines = f.readlines()
            
            commented_lines = []
            commented_count = 0
            
            for line in original_lines:
                # Si la ligne a du contenu (pas juste des espaces)
                if line.strip():
                    # Ajouter # au début, même si déjà commentée
                    commented_line = f"# {line}"
                    commented_lines.append(commented_line)
                    commented_count += 1
                else:
                    # Garder les lignes vides telles quelles
                    commented_lines.append(line)
            
            # Réécrire le fichier avec toutes les lignes commentées
            with open(self.original_path, 'w', encoding='utf-8', newline='') as f:
                f.writelines(commented_lines)
            
            log_message("INFO", f"Fichier original commenté : {commented_count} lignes commentées dans {os.path.basename(self.original_path)}", category="reconstruction_comment")
            return True
            
        except Exception as e:
            log_message("ERREUR", f"Impossible de commenter le fichier original: {str(e)}", e, category="reconstruction_comment")
            return False

    def _reassemble_line_optimized(self, line_idx, original_line, new_contents, line_suffix):
        """
        VERSION OPTIMISÉE : Réassemble une ligne avec line_idx déjà connu.
        Les préfixes/suffixes sont déjà intégrés dans new_contents.
        """
        rebuilt = original_line
        
        # Restaurer les placeholders de structure en premier (inchangé)
        rebuilt = rebuilt.replace("RENPY_NARRATOR", '"" "')
        rebuilt = rebuilt.replace("RENPY_EMPTY03", '" "')
        rebuilt = rebuilt.replace("RENPY_EMPTY01", '""')
        rebuilt = rebuilt.replace("RENPY_EMPTY02", '" "')
        
        # Trouver le préfixe de la ligne (locuteur, indentation)
        first_quote_pos = rebuilt.find('"')
        if first_quote_pos == -1:
            return original_line
        
        line_prefix = rebuilt[:first_quote_pos]
        
        # Les {tags} sont déjà intégrés dans new_contents par _rebuild_content()
        # Plus besoin de récupérer les préfixes/suffixes ici
        
        # Construire la partie dialogue avec les {tags} restaurés
        dialogue_part = ""
        
        if "RENPY_NARRATOR" in original_line:
            # Cas narrateur
            dialogue_part = f'"" "{new_contents[0]}"'
            
        elif "RENPY_EMPTY03" in original_line:
            # Cas contenus multiples
            dialogue_part = f'"{new_contents[0]}" "{new_contents[1]}"'
            
        else:
            # Cas dialogue normal
            parts = []
            for content in new_contents:
                parts.append(f'"{content}"')
            dialogue_part = " ".join(parts)
        
        # Assembler la ligne finale
        final_line = f"{line_prefix}{dialogue_part}{line_suffix}"
        if original_line.endswith('\n') and not final_line.endswith('\n'):
            final_line += '\n'
        
        # Restaurer tous les placeholders de code, empty et astérisques restants
        all_mappings = {**self.mapping, **self.empty_mapping, **self.asterix_mapping}
        sorted_keys = sorted(all_mappings.keys(), key=len, reverse=True)
        for key in sorted_keys:
            final_line = final_line.replace(key, all_mappings[key])
            
        return final_line

    def _build_translation_map(self):
        """Mappe les traductions par INDEX au lieu de par ordre de fichier"""
        translation_map = {}
        
        if self.detect_duplicates:
            # Logique existante pour les doublons
            content_counts = OrderedDict()
            for content in self.all_contents_linear:
                content_counts[content] = content_counts.get(content, 0) + 1
            
            duplicate_originals = [c for c, count in content_counts.items() if count > 1]
            unique_originals = [c for c, count in content_counts.items() if count == 1]

            for i, original in enumerate(duplicate_originals):
                if i < len(self.duplicate_translations):
                    translation_map[original] = self.duplicate_translations[i]
            
            for i, original in enumerate(unique_originals):
                if i < len(self.translations):
                    translation_map[original] = self.translations[i]
        else:
            # Sans doublons, mapper 1:1 par index
            for i, original in enumerate(self.all_contents_linear):
                if i < len(self.translations):
                    translation_map[original] = self.translations[i]
                else:
                    translation_map[original] = original  # Fallback
        
        return translation_map
    
    def _restore_asterisks(self):
        """
        🆕 VERSION AMÉLIORÉE : Restaure les astérisques en utilisant les métadonnées.
        """
        # Créer une liste ordonnée des placeholders (ordre crucial)
        placeholders_ordered = list(self.asterix_mapping.keys())
        num_translations = len(self.asterix_translations)
        
        restored_with_metadata = 0
        restored_fallback = 0
        
        for i, placeholder in enumerate(placeholders_ordered):
            if i < num_translations:
                translated_content = self.asterix_translations[i]
                
                # 🆕 UTILISER LES MÉTADONNÉES si disponibles
                if placeholder in self.asterix_metadata:
                    meta = self.asterix_metadata[placeholder]
                    prefix_asterisks = '*' * meta['prefix_count']
                    suffix_asterisks = '*' * meta['suffix_count']
                    
                    # Reconstruire avec le bon nombre d'astérisques
                    reconstructed_text = f"{prefix_asterisks}{translated_content}{suffix_asterisks}"
                    self.asterix_mapping[placeholder] = reconstructed_text
                    
                    restored_with_metadata += 1
                else:
                    # Fallback: utiliser l'ancien système (simple *)
                    self.asterix_mapping[placeholder] = f"*{translated_content}*"
                    restored_fallback += 1
        
        log_message("DEBUG", f"✅ Astérisques restaurés: {restored_with_metadata} avec métadonnées, {restored_fallback} en fallback", category="asterisk_restoration")

    def _restore_tildes_two_pass(self):
        """
        Restauration des tildes en tenant compte des deux passes
        """
        
        placeholders_ordered = list(self.tilde_mapping.keys())
        num_translations = len(self.tilde_translations)
        
        restored_structured = 0
        restored_orphans = 0
        restored_fallback = 0
        
        for i, placeholder in enumerate(placeholders_ordered):
            if i < num_translations:
                translated_content = self.tilde_translations[i]
                
                if placeholder in self.tilde_metadata:
                    meta = self.tilde_metadata[placeholder]
                    
                    if meta.get('orphan', False):
                        # ORPHELIN: On restaure juste les tildes sans contenu
                        reconstructed_text = '~' * meta['prefix_count']
                        restored_orphans += 1
                    else:
                        # STRUCTURÉ: Encadrer le contenu traduit
                        prefix_tildes = '~' * meta['prefix_count']
                        suffix_tildes = '~' * meta['suffix_count']
                        reconstructed_text = f"{prefix_tildes}{translated_content}{suffix_tildes}"
                        restored_structured += 1
                    
                    self.tilde_mapping[placeholder] = reconstructed_text
                else:
                    # Fallback: ancien système
                    self.tilde_mapping[placeholder] = f"~{translated_content}~"
                    restored_fallback += 1
        
        log_message("DEBUG", f"✅ Tildes restaurés: {restored_structured} structurés, {restored_orphans} orphelins, {restored_fallback} en fallback", category="tilde_restoration")

    def _reassemble_line_optimized(self, line_idx, original_line, new_contents, line_suffix):
        """
        VERSION OPTIMISÉE : Réassemble une ligne avec line_idx déjà connu.
        Évite les recherches O(n) coûteuses. MODIFIÉ pour tildes.
        """
        rebuilt = original_line
        
        # Restaurer les placeholders de structure en premier (inchangé)
        rebuilt = rebuilt.replace("RENPY_NARRATOR", '"" "')
        rebuilt = rebuilt.replace("RENPY_EMPTY03", '" "')
        rebuilt = rebuilt.replace("RENPY_EMPTY01", '""')
        rebuilt = rebuilt.replace("RENPY_EMPTY02", '" "')
        
        # Trouver le préfixe de la ligne (locuteur, indentation)
        first_quote_pos = rebuilt.find('"')
        if first_quote_pos == -1:
            return original_line
        
        line_prefix = rebuilt[:first_quote_pos]
        
        # Les {tags} sont déjà intégrés dans new_contents par _rebuild_content()
        
        # Construire la partie dialogue avec les {tags} restaurés
        dialogue_part = ""
        
        if "RENPY_NARRATOR" in original_line:
            # Cas narrateur
            dialogue_part = f'"" "{new_contents[0]}"'
            
        elif "RENPY_EMPTY03" in original_line:
            # Cas contenus multiples
            dialogue_part = f'"{new_contents[0]}" "{new_contents[1]}"'
            
        else:
            # Cas dialogue normal
            parts = []
            for content in new_contents:
                parts.append(f'"{content}"')
            dialogue_part = " ".join(parts)
        
        # Assembler la ligne finale
        final_line = f"{line_prefix}{dialogue_part}{line_suffix}"
        if original_line.endswith('\n') and not final_line.endswith('\n'):
            final_line += '\n'
        
        # Restaurer tous les placeholders de code, empty, astérisques ET tildes restants
        all_mappings = {**self.mapping, **self.empty_mapping, **self.asterix_mapping, **self.tilde_mapping}
        sorted_keys = sorted(all_mappings.keys(), key=len, reverse=True)
        for key in sorted_keys:
            final_line = final_line.replace(key, all_mappings[key])
            
        return final_line

    def _post_process_empty_placeholders(self, content):
        """
        Post-traitement pour corriger les placeholders EMPTY restants
        MODIFIÉ: Utilise les préfixes personnalisés au lieu des valeurs codées en dur
        """
        processed_content = []
        corrections_made = 0
        
        # Construire les placeholders avec préfixes personnalisés
        empty_01_placeholder = f"{self.empty_prefix}_01"
        empty_02_placeholder = f"{self.empty_prefix}_02"
        narrator_placeholder = f"{self.empty_prefix}_NARRATOR"
        sep_placeholder = f"{self.empty_prefix}_SEP03"
        
        for line in content:
            # NE PAS modifier les lignes commentées
            if line.strip().startswith('#'):
                processed_content.append(line)
                continue
            
            original_line = line
            
            # Corriger les placeholders avec préfixes personnalisés
            if empty_01_placeholder in line:
                line = line.replace(empty_01_placeholder, '""')
                corrections_made += 1
            
            if empty_02_placeholder in line:
                line = line.replace(empty_02_placeholder, '" "')
                corrections_made += 1
                
            if narrator_placeholder in line:
                line = line.replace(narrator_placeholder, '"" "')
                corrections_made += 1
                
            if sep_placeholder in line:
                line = line.replace(sep_placeholder, '" "')
                corrections_made += 1
                
            processed_content.append(line)
        
        if corrections_made > 0:
            log_message("INFO", f"✅ Post-traitement terminé: {corrections_made} corrections appliquées", category="postprocess")
        
        return processed_content

    def _load_reconstruction_settings(self):
        """Charge les paramètres pour la reconstruction"""
        try:
            from infrastructure.config.config import config_manager
            self.detect_duplicates = config_manager.get('extraction_detect_duplicates', True)
        except Exception as e:
            log_message("ATTENTION", f"Erreur chargement paramètre reconstruction: {e}", category="reconstruction_options")
            self.detect_duplicates = True

    def _save_reconstructed_file(self, content, save_mode):
        if save_mode == 'overwrite':
            save_path = self.original_path
        else:
            save_path = self.original_path.replace(".rpy", "_translated.rpy")

        # ✅ NOUVEAU : Ajouter un marqueur de reconstruction
        from datetime import datetime
        reconstruction_marker = f"\n# Fichier reconstruit après traduction par RenExtract le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        content.append(reconstruction_marker)

        with open(save_path, "w", encoding="utf-8", newline='') as wf:
            wf.writelines(content)
        
        # Commenter l'original si nouveau fichier
        if save_mode == 'new_file':
            success = self._comment_original_file()
            if not success:
                log_message("ATTENTION", "Impossible de commenter le fichier original", category="save")
        
        return save_path

def reconstruire_fichier(file_content, original_path, save_mode='new_file'):
    reconstructor = FileReconstructor()
    reconstructor.load_file_content(file_content, original_path)
    return reconstructor.reconstruct_file(save_mode)
