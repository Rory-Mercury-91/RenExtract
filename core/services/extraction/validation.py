# core/validation.py - VERSION COMPLÈTE CORRIGÉE
# Validation and Security Module
# Created for RenExtract 

"""
Module de validation des fichiers et de sécurité
VERSION AVEC VALIDATION INTELLIGENTE DE TRADUCTION
"""

import os
import re
import shutil
import datetime
from infrastructure.config.constants import FOLDERS
from infrastructure.logging.logging import log_message
from core.models.backup.unified_backup_manager import UnifiedBackupManager, BackupType

class FileValidator:
    """Classe pour la validation des fichiers Ren'Py"""
    
    # Patterns typiques des fichiers Ren'Py
    RENPY_PATTERNS = [
        r'label\s+\w+:',                    # Labels Ren'Py
        r'menu:',                           # Menus
        r'scene\s+\w+',                     # Changements de scène
        r'show\s+\w+',                      # Affichage de personnages
        r'hide\s+\w+',                      # Masquage de personnages
        r'\w+\s+".*"',                      # Dialogues (personnage + texte)
        r'translate\s+\w+\s+\w+:',          # Blocs de traduction
        r'old\s+".*"',                      # Anciennes traductions
        r'new\s+".*"',                      # Nouvelles traductions
        r'\$\s+.*',                         # Code Python intégré
        r'if\s+.*:',                        # Conditions
        r'jump\s+\w+',                      # Sauts
        r'call\s+\w+',                      # Appels
        r'return',                          # Retours
        r'with\s+\w+',                      # Transitions
        r'pause\s*\d*\.?\d*',               # Pauses
    ]
    
    @classmethod
    def is_renpy_file(cls, filepath):
        """
        Vérifie si un fichier est un vrai fichier Ren'Py
        
        Args:
            filepath (str): Chemin du fichier à valider
            
        Returns:
            dict: Résultat de la validation avec détails
        """
        result = {
            'is_valid': False,
            'confidence': 0,
            'patterns_found': [],
            'file_info': {},
            'warnings': [],
            'errors': []
        }
        
        try:
            # Vérifications de base
            if not os.path.exists(filepath):
                result['errors'].append("Fichier non trouvé")
                return result
            
            if not filepath.lower().endswith('.rpy'):
                result['warnings'].append("L'extension du fichier n'est pas .rpy")
            
            # Informations sur le fichier
            file_stats = os.stat(filepath)
            result['file_info'] = {
                'size': file_stats.st_size,
                'modified': datetime.datetime.fromtimestamp(file_stats.st_mtime),
                'encoding': 'unknown'
            }
            
            # Lecture et analyse du contenu
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                result['file_info']['encoding'] = 'utf-8'
            except UnicodeDecodeError:
                try:
                    with open(filepath, 'r', encoding='latin-1') as f:
                        content = f.read()
                    result['file_info']['encoding'] = 'latin-1'
                    result['warnings'].append("Fichier encodé en non-UTF8 (tentative avec latin-1)")
                except Exception as e:
                    result['errors'].append(f"Erreur de lecture du fichier : {str(e)}")
                    return result
            
            if not content.strip():
                result['errors'].append("Le fichier est vide.")
                return result
            
            # Analyse des patterns Ren'Py
            lines = content.split('\n')
            pattern_matches = 0
            dialogue_lines = 0
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Vérifier chaque pattern
                for pattern in cls.RENPY_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        if pattern not in result['patterns_found']:
                            result['patterns_found'].append(pattern)
                        pattern_matches += 1
                        break
                
                # Compter les lignes de dialogue potentielles
                if re.search(r'\w+\s+".*"', line) or re.search(r'".*"', line):
                    dialogue_lines += 1
            
            # Calcul de la confiance
            total_lines = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
            if total_lines > 0:
                confidence = min(100, (pattern_matches / total_lines) * 100)
                dialogue_ratio = (dialogue_lines / total_lines) * 100
                
                # Bonus pour les dialogues
                if dialogue_ratio > 10:
                    confidence += min(20, dialogue_ratio / 2)
                
                result['confidence'] = round(confidence, 1)
            
            # Déterminer la validité
            result['is_valid'] = (
                result['confidence'] > 15 and  # Au moins 15% de confiance
                len(result['patterns_found']) >= 2 and  # Au moins 2 patterns différents
                dialogue_lines > 0  # Au moins quelques dialogues
            )
            
            # Messages informatifs
            result['file_info']['total_lines'] = total_lines
            result['file_info']['dialogue_lines'] = dialogue_lines
            result['file_info']['patterns_count'] = len(result['patterns_found'])
            
            if result['confidence'] < 50:
                result['warnings'].append("Confiance faible, le fichier n'est peut-être pas un script Ren'Py.")

            log_message("INFO", f"Validation fichier: {os.path.basename(filepath)} - Confiance: {result['confidence']}%", category="validation")

        except Exception as e:
            result['errors'].append(f"Erreur inattendue lors de la validation : {str(e)}")
            log_message("ERREUR", f"Erreur validation fichier {filepath}", e, category="validation")
        
        return result


class TranslationContentValidator:
    """
    Validateur pour distinguer les fichiers de traduction (dialogues/strings) du code technique.
    RÈGLE: Seuls les fichiers contenant au moins un bloc reconnu sont acceptés :
      - translate <langue> <ID>:  (dialogues)
      - translate <langue> strings:  (choix / strings)
    Tout le reste est considéré comme technique.

    Structure typique d'un fichier de traduction accepté :
      Ligne 1 : # TODO: Translation updated at YYYY-MM-DD ...
      Ligne 2 : (vide)
      Ligne 3 : # game/script.rpy:164  (localisation)
      Ligne 4 : translate <langue> <id>:  ou  translate <langue> strings:
    Les lignes # ne sont pas considérées comme "technique" ; seuls init/define/screen en début de ligne le sont.
    """
    
    # Blocs de traduction acceptés : uniquement en DÉBUT DE LIGNE (évite faux positifs dans commentaires/chaînes)
    # Ex. ligne 4 typique : "translate french splashscreen_4aafa53c:" ou "translate french strings:"
    PATTERN_TRANSLATE_DIALOGUE = re.compile(
        r'^\s*translate\s+\w+\s+\S+:',
        re.IGNORECASE | re.MULTILINE
    )
    PATTERN_TRANSLATE_STRINGS = re.compile(
        r'^\s*translate\s+\w+\s+strings\s*:',
        re.IGNORECASE | re.MULTILINE
    )
    
    # Patterns techniques : UNIQUEMENT en début de ligne (^\s*), pour comparer position avec premier translate
    # init +1:, init 999:, init python:, define, default, screen
    TECHNICAL_PATTERNS_DETECT = [
        (r'^\s*init\s+python\s*:', 'init python:'),
        (r'^\s*init\s+[\+]?\d+\s*:', 'init N: ou init +1:'),
        (r'^\s*define\s+\w+\s*=', 'define config/var'),
        (r'^\s*default\s+\w+\s*=', 'default persistent/var'),
        (r'^\s*screen\s+\w+\s*\(', 'screen name():'),
    ]
    
    def validate_translation_content(self, filepath):
        """
        Validation stricte : accepte uniquement si le fichier contient
        translate <langue> <ID>: (dialogues) ou translate <langue> strings: (strings).
        
        Returns:
            dict: is_translation, file_type, reason, rejection_details (liste pour le popup)
        """
        try:
            if not filepath.lower().endswith('.rpy'):
                return {
                    'is_translation': False,
                    'file_type': 'invalid',
                    'confidence': 0.0,
                    'reason': 'Extension non .rpy',
                    'rejection_details': ['Seuls les fichiers .rpy sont acceptés.']
                }
            
            analysis = self._fast_content_analysis(filepath)
            
            if analysis.get('error'):
                return {
                    'is_translation': False,
                    'file_type': 'invalid',
                    'confidence': 0.0,
                    'reason': analysis['error'],
                    'rejection_details': [f"Erreur à l'analyse : {analysis['error']}"]
                }
            
            if analysis['translation_detected']:
                return {
                    'is_translation': True,
                    'file_type': 'translation',
                    'confidence': analysis['confidence'],
                    'reason': analysis.get('reason', 'Bloc(s) de traduction reconnu(s).'),
                    'rejection_details': []
                }
            
            # Rejet : détail pour le popup
            return {
                'is_translation': False,
                'file_type': 'technical_code',
                'confidence': 70.0,
                'reason': analysis.get('reason', 'Contenu non reconnu comme traduction.'),
                'rejection_details': analysis.get('rejection_details', [])
            }
                
        except Exception as e:
            return {
                'is_translation': False,
                'file_type': 'invalid',
                'confidence': 0.0,
                'reason': str(e),
                'rejection_details': [f'Erreur : {e}']
            }
    
    def _fast_content_analysis(self, filepath):
        """
        Analyse un échantillon du fichier.
        Accepte uniquement si présence de :
          - translate <lang> <id>:  (dialogues)
          - translate <lang> strings:  (strings)
        Retourne rejection_details pour affichage dans le popup (ce qui a coincé).
        """
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content_sample = f.read(12000)  # ~300–400 lignes typiques
            
            if not content_sample.strip():
                return {
                    'translation_detected': False,
                    'reason': 'Fichier vide ou sans contenu lisible.',
                    'rejection_details': ['Fichier vide ou sans contenu lisible.'],
                    'technical_found': [],
                    'confidence': 0,
                }
            
            # Nettoyer BOM
            if content_sample.startswith('\ufeff'):
                content_sample = content_sample[1:]
            
            # Position du premier "translate" en début de ligne (dialogues ou strings)
            first_translate_pos = None
            for m in self.PATTERN_TRANSLATE_DIALOGUE.finditer(content_sample):
                first_translate_pos = m.start()
                break
            if first_translate_pos is None:
                for m in self.PATTERN_TRANSLATE_STRINGS.finditer(content_sample):
                    first_translate_pos = m.start()
                    break
            
            # Position du premier bloc technique en début de ligne (init, define, screen)
            first_technical_pos = None
            for pattern_re, label in self.TECHNICAL_PATTERNS_DETECT:
                m = re.search(pattern_re, content_sample, re.MULTILINE | re.IGNORECASE)
                if m and (first_technical_pos is None or m.start() < first_technical_pos):
                    first_technical_pos = m.start()
            
            has_translate = first_translate_pos is not None
            has_technical_before = (
                first_technical_pos is not None
                and (first_translate_pos is None or first_technical_pos < first_translate_pos)
            )
            # Accepter seulement si on a un bloc translate ET pas de code technique avant le premier translate
            translation_detected = has_translate and not has_technical_before
            
            # Détail des patterns techniques trouvés (pour le retour visuel)
            technical_found = []
            for pattern_re, label in self.TECHNICAL_PATTERNS_DETECT:
                if re.search(pattern_re, content_sample, re.MULTILINE | re.IGNORECASE):
                    technical_found.append(label)
            
            rejection_details = []
            if not translation_detected:
                if not has_translate:
                    rejection_details.append(
                        "Aucun bloc 'translate <langue> <id>:' (dialogues) ni 'translate <langue> strings:' (choix/strings) trouvé."
                    )
                else:
                    rejection_details.append(
                        "Le fichier commence par du code technique (init, define, screen) avant tout bloc 'translate'."
                    )
                rejection_details.append(
                    "Seuls les fichiers dont le contenu principal est de la traduction sont acceptés."
                )
            if technical_found:
                rejection_details.append("Éléments de type code détectés : " + ", ".join(technical_found))
            
            return {
                'translation_detected': translation_detected,
                'reason': 'Bloc(s) de traduction reconnu(s).' if translation_detected else (
                    'Aucun bloc dialogue/strings reconnu.' + (
                        f" Code détecté : {', '.join(technical_found)}" if technical_found else ''
                    )
                ),
                'rejection_details': rejection_details,
                'technical_found': technical_found,
                'confidence': 95.0 if translation_detected else 0.0,
            }
            
        except Exception as e:
            return {
                'translation_detected': False,
                'reason': str(e),
                'rejection_details': [f"Erreur à la lecture : {e}"],
                'technical_found': [],
                'confidence': 0,
                'error': str(e),
            }

# ✅ FONCTION PRINCIPALE SIMPLIFIÉE - REMPLACE L'ANCIENNE
def validate_file_for_translation_processing(filepath):
    """
    Validation RAPIDE et STRICTE - VERSION PRINCIPALE
    RÈGLE: Seuls les fichiers avec patterns de traduction sont acceptés
    """
    try:
        # ✅ Vérification extension de base
        if not filepath.lower().endswith('.rpy'):
            return {
                'overall_valid': False,
                'file_type': 'invalid',
                'processing_recommended': False,
                'user_message': "❌ Seuls les fichiers .rpy sont acceptés",
                'rejection_details': ['Seuls les fichiers .rpy sont acceptés.'],
                'fast_validation': True
            }
        
        # ✅ Validation stricte du contenu
        validator = TranslationContentValidator()
        content_validation = validator.validate_translation_content(filepath)
        
        # ✅ Résultat unifié
        filename = os.path.basename(filepath)
        result = {
            'overall_valid': content_validation['is_translation'],
            'file_type': content_validation['file_type'],
            'processing_recommended': content_validation['is_translation'],
            'content_validation': content_validation,
            'fast_validation': True
        }
        
        # ✅ Messages selon le type + détail du rejet pour le popup
        if content_validation['file_type'] == 'translation':
            result['user_message'] = f"✅ Fichier de traduction détecté: {filename}"
        else:
            result['user_message'] = f"⚠️ Fichier non autorisé: {filename}"
            result['warnings'] = ['Ajoutez ce fichier aux exemptions si nécessaire']
            result['rejection_details'] = content_validation.get('rejection_details', [])
        
        return result
        
    except Exception as e:
        log_message("ERREUR", f"Erreur validation rapide: {e}", category="validation")
        return {
            'overall_valid': False,
            'file_type': 'invalid',
            'processing_recommended': False,
            'user_message': f"❌ Erreur de validation: {os.path.basename(filepath)}",
            'warnings': ['Fichier refusé par sécurité - erreur de validation'],
            'rejection_details': [f'Erreur : {e}'],
            'fast_validation': True
        }
    

class TranslationValidator:
    @staticmethod
    def validate_file_correspondence(extracted_count, translation_file_path):
        """Validation d'un fichier avec support des fichiers multiples"""
        result = {'valid': True, 'translation_count': 0, 'missing_count': 0, 'extra_count': 0, 'empty_lines': 0, 'warnings': [], 'errors': []}
        try:
            if not os.path.exists(translation_file_path):
                result['valid'] = False
                result['errors'].append(f"Fichier de traduction manquant: {translation_file_path}")
                return result
            
            filename = os.path.basename(translation_file_path)
            folder = os.path.dirname(translation_file_path)
            
            # Charger tous les fichiers (principal + numérotés) comme un seul contenu
            all_lines = TranslationValidator._load_translation_files(folder, filename)
            
            if not all_lines:
                result['valid'] = False
                result['errors'].append(f"Aucun contenu trouvé dans les fichiers: {filename}")
                return result
            
            # Compter les lignes selon le type de fichier (même logique que l'ancienne méthode)
            if filename.endswith('_dialogue.txt'):
                content_lines = []
                empty_lines = 0
                for i, line in enumerate(all_lines):
                    content = line.rstrip('\n\r')
                    if content.strip():
                        content_lines.append((i + 1, content))
                    else:
                        empty_lines += 1
                result['translation_count'] = len(content_lines)
                result['empty_lines'] = empty_lines
                log_message("DEBUG", f"Fichier dialogue - Total lignes: {len(all_lines)}, Non vides: {len(content_lines)}, Vides: {empty_lines}", category="validation")
            elif filename.endswith('_empty.txt'):
                result['translation_count'] = len(all_lines)
                log_message("DEBUG", f"Fichier empty - Total lignes: {len(all_lines)}", category="validation")
            else:
                non_empty_lines = []
                empty_lines = 0
                for i, line in enumerate(all_lines):
                    content = line.rstrip('\n\r')
                    if content.strip():
                        non_empty_lines.append((i + 1, content))
                    else:
                        empty_lines += 1
                result['translation_count'] = len(non_empty_lines)
                result['empty_lines'] = empty_lines
                log_message("DEBUG", f"Fichier {filename} - Total lignes: {len(all_lines)}, Non vides: {len(non_empty_lines)}, Vides: {empty_lines}", category="validation")
            
            # Comparer avec le nombre attendu
            if result['translation_count'] != extracted_count:
                result['valid'] = False
                if result['translation_count'] < extracted_count:
                    result['missing_count'] = extracted_count - result['translation_count']
                    result['errors'].append(f"Traductions manquantes: {result['missing_count']} (attendu: {extracted_count}, trouvé: {result['translation_count']})")
                else:
                    result['extra_count'] = result['translation_count'] - extracted_count
                    result['warnings'].append(f"Traductions supplémentaires: {result['extra_count']} (attendu: {extracted_count}, trouvé: {result['translation_count']})")
            return result
        except Exception as e:
            result['valid'] = False
            result['errors'].append(f"Erreur de validation: {str(e)}")
            log_message("ERREUR", f"Erreur validation traduction {translation_file_path}", e, category="translation_validation")
        return result
    
    @staticmethod
    def _find_translation_files(folder, base_filename):
        """Trouve tous les fichiers de traduction (avec ou sans numérotation) - Version validation"""
        try:
            import glob
            
            # Chercher tous les fichiers (principal + numérotés)
            name, ext = os.path.splitext(base_filename)
            
            # Pattern pour le fichier principal
            main_file = os.path.join(folder, base_filename)
            
            # Pattern pour les fichiers numérotés
            pattern = os.path.join(folder, f"{name}_*{ext}")
            numbered_files = glob.glob(pattern)
            
            # Combiner et trier
            all_files = []
            if os.path.exists(main_file):
                all_files.append(main_file)
            
            # Trier les fichiers numérotés par numéro
            numbered_files.sort(key=lambda f: TranslationValidator._extract_file_number(f, base_filename))
            all_files.extend(numbered_files)
            
            return all_files
            
        except Exception as e:
            log_message("ERREUR", f"Erreur recherche fichiers multiples: {e}", category="validation")
            return []
    
    @staticmethod
    def _extract_file_number(filepath, base_filename):
        """Extrait le numéro d'un fichier pour le tri - Version validation"""
        try:
            filename = os.path.basename(filepath)
            name, ext = os.path.splitext(base_filename)
            
            if filename == base_filename:
                return 0  # Fichier principal
            
            # Extraire le numéro du pattern name_1.txt, name_2.txt, etc.
            if filename.startswith(f"{name}_") and filename.endswith(ext):
                number_part = filename[len(f"{name}_"):-len(ext)]
                try:
                    return int(number_part)
                except ValueError:
                    return 999
            return 999
        except Exception:
            return 999
    
    @staticmethod
    def _load_translation_files(folder, base_filename):
        """Charge tous les fichiers de traduction comme un seul contenu - Version validation"""
        try:
            files = TranslationValidator._find_translation_files(folder, base_filename)
            
            # DEBUG: Log les fichiers trouvés
            log_message("DEBUG", f"_load_translation_files - Fichiers trouvés pour {base_filename}: {len(files)}", category="validation")
            for f in files:
                log_message("DEBUG", f"  - {os.path.basename(f)}", category="validation")
            
            if not files:
                log_message("WARNING", f"Aucun fichier trouvé pour {base_filename} dans {folder}", category="validation")
                return []
            
            all_lines = []
            for file_path in files:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        all_lines.extend(lines)
                        log_message("DEBUG", f"  - {os.path.basename(file_path)}: {len(lines)} lignes", category="validation")
            
            log_message("DEBUG", f"Total lignes chargées pour {base_filename}: {len(all_lines)}", category="validation")
            return all_lines
            
        except Exception as e:
            log_message("ERREUR", f"Erreur chargement fichiers multiples: {e}", category="validation")
            return []
    
    @staticmethod
    def validate_multiple_files_correspondence(extracted_count, folder, base_filename):
        """Validation des fichiers multiples (principal + numérotés)"""
        result = {'valid': True, 'translation_count': 0, 'missing_count': 0, 'extra_count': 0, 'empty_lines': 0, 'warnings': [], 'errors': []}
        try:
            # Charger tous les fichiers comme un seul contenu
            all_lines = TranslationValidator._load_translation_files(folder, base_filename)
            
            if not all_lines:
                result['valid'] = False
                result['errors'].append(f"Aucun fichier de traduction trouvé: {base_filename}")
                return result
            
            # Compter les lignes selon le type de fichier
            if base_filename.endswith('_dialogue.txt'):
                content_lines = []
                empty_lines = 0
                for i, line in enumerate(all_lines):
                    content = line.rstrip('\n\r')
                    if content.strip():
                        content_lines.append((i + 1, content))
                    else:
                        empty_lines += 1
                result['translation_count'] = len(content_lines)
                result['empty_lines'] = empty_lines
            elif base_filename.endswith('_empty.txt'):
                result['translation_count'] = len(all_lines)
            else:
                non_empty_lines = []
                empty_lines = 0
                for i, line in enumerate(all_lines):
                    content = line.rstrip('\n\r')
                    if content.strip():
                        non_empty_lines.append((i + 1, content))
                    else:
                        empty_lines += 1
                result['translation_count'] = len(non_empty_lines)
                result['empty_lines'] = empty_lines
            
            # Comparer avec le nombre attendu
            if result['translation_count'] != extracted_count:
                result['valid'] = False
                if result['translation_count'] < extracted_count:
                    result['missing_count'] = extracted_count - result['translation_count']
                    result['errors'].append(f"Lignes manquantes: {result['missing_count']} (attendu: {extracted_count}, trouvé: {result['translation_count']})")
                else:
                    result['extra_count'] = result['translation_count'] - extracted_count
                    result['warnings'].append(f"Lignes supplémentaires: {result['extra_count']} (attendu: {extracted_count}, trouvé: {result['translation_count']})")
                    
        except Exception as e:
            result['valid'] = False
            result['errors'].append(f"Erreur lors de la validation des fichiers multiples: {str(e)}")
        return result
    
    @staticmethod
    def validate_all_files(game_name, file_base, extracted_count, asterix_count=0, empty_count=0, detect_duplicates=False):
        validation_results = {
            'overall_valid': True, 'main_file': None, 'asterix_file': None, 'empty_file': None,
            'summary': {'total_expected': extracted_count + asterix_count + empty_count, 'total_found': 0, 'files_validated': 0, 'validation_success': True}
        }
        try:
            # Vérifier d'abord le fichier principal
            main_file = os.path.join(FOLDERS["temporaires"], game_name, file_base, "fichiers_a_traduire", f"{file_base}_dialogue.txt")
            
            if os.path.exists(main_file):
                # Utiliser l'ancienne méthode qui fonctionnait
                validation_results['main_file'] = TranslationValidator.validate_file_correspondence(extracted_count, main_file)
                validation_results['summary']['files_validated'] += 1
                validation_results['summary']['total_found'] += validation_results['main_file']['translation_count']
                if not validation_results['main_file']['valid']:
                    validation_results['overall_valid'] = False
                    validation_results['summary']['validation_success'] = False
            else:
                validation_results['overall_valid'] = False
                validation_results['summary']['validation_success'] = False
                validation_results['main_file'] = {'valid': False, 'translation_count': 0, 'errors': [f"Fichier principal manquant: {main_file}"]}
            if asterix_count > 0:
                asterix_file = os.path.join(FOLDERS["temporaires"], game_name, file_base, "fichiers_a_traduire", f"{file_base}_asterix.txt")
                if os.path.exists(asterix_file):
                    validation_results['asterix_file'] = TranslationValidator.validate_file_correspondence(asterix_count, asterix_file)
                    validation_results['summary']['files_validated'] += 1
                    validation_results['summary']['total_found'] += validation_results['asterix_file']['translation_count']
                    if not validation_results['asterix_file']['valid']:
                        validation_results['overall_valid'] = False
                        validation_results['summary']['validation_success'] = False
                else:
                    validation_results['asterix_file'] = {'valid': False, 'translation_count': 0, 'errors': [f"Fichier astérisques manquant: {asterix_file}"]}
                    validation_results['overall_valid'] = False
                    validation_results['summary']['validation_success'] = False
            
            # Validation du fichier doublons (si détection doublons activée)
            if detect_duplicates:
                doublons_file = os.path.join(FOLDERS["temporaires"], game_name, file_base, "fichiers_a_traduire", f"{file_base}_doublons.txt")
                if os.path.exists(doublons_file):
                    doublons_count = len([line for line in open(doublons_file, 'r', encoding='utf-8').readlines() if line.strip()])
                    validation_results['doublons_file'] = {'valid': True, 'translation_count': doublons_count, 'errors': []}
                    validation_results['summary']['files_validated'] += 1
                    log_message("INFO", f"   ✅ Fichier doublons: {doublons_count} doublons trouvés", category="validation")
                else:
                    validation_results['doublons_file'] = {'valid': False, 'translation_count': 0, 'errors': [f"Fichier doublons manquant: {doublons_file}"]}
                    validation_results['overall_valid'] = False
                    validation_results['summary']['validation_success'] = False
                    log_message("ATTENTION", f"   ⚠️ Fichier doublons manquant: {os.path.basename(doublons_file)}", category="validation")
            
            if empty_count > 0:
                empty_file = os.path.join(FOLDERS["temporaires"], game_name, file_base, "fichiers_a_ne_pas_traduire", f"{file_base}_empty.txt")
                if not os.path.exists(empty_file):
                    empty_file_alt = os.path.join(FOLDERS["temporaires"], game_name, file_base, "fichiers_a_traduire", f"{file_base}_empty.txt")
                    if os.path.exists(empty_file_alt):
                        empty_file = empty_file_alt
                if os.path.exists(empty_file):
                    validation_results['empty_file'] = TranslationValidator.validate_file_correspondence(empty_count, empty_file)
                    validation_results['summary']['files_validated'] += 1
                    validation_results['summary']['total_found'] += validation_results['empty_file']['translation_count']
                    if not validation_results['empty_file']['valid']:
                        validation_results['overall_valid'] = False
                        validation_results['summary']['validation_success'] = False
                else:
                    validation_results['empty_file'] = {'valid': False, 'translation_count': 0, 'errors': [f"Fichier textes vides manquant: {empty_file}"]}
                    validation_results['overall_valid'] = False
                    validation_results['summary']['validation_success'] = False
        except Exception as e:
            log_message("ERREUR", f"Erreur lors de la validation des fichiers pour {file_base}", e, category="validation_summary")
            validation_results['overall_valid'] = False
            validation_results['summary']['validation_success'] = False
            if not validation_results.get('main_file'):
                validation_results['main_file'] = {'valid': False, 'translation_count': 0, 'errors': [f"Erreur de validation: {str(e)}"]}
        return validation_results

def create_safety_backup(filepath):
    try:
        if not filepath:
            return {'success': False, 'backup_path': None, 'error': "Chemin de fichier non fourni"}
        is_virtual_file = (filepath.startswith("clipboard_") and not os.path.exists(filepath))
        if is_virtual_file:
            log_message("INFO", f"Fichier virtuel détecté - pas de sauvegarde nécessaire: {filepath}", category="safety_backup")
            return {'success': True, 'backup_path': None, 'error': None, 'virtual_file': True, 'message': "Fichier virtuel - pas de sauvegarde nécessaire"}
        if not os.path.exists(filepath):
            return {'success': False, 'backup_path': None, 'error': "Fichier source introuvable"}
        backup_manager = UnifiedBackupManager()
        result = backup_manager.create_backup(filepath, BackupType.SECURITY, "Sauvegarde de sécurité automatique")
        if result['success']:
            log_message("INFO", f"Sauvegarde de sécurité créée: {result['backup_path']}", category="safety_backup")
        else:
            log_message("ATTENTION", f"Échec de la sauvegarde: {result['error']}", category="safety_backup")
        return result
    except Exception as e:
        log_message("ERREUR", f"Erreur lors de la création de la sauvegarde de sécurité pour {filepath}", e, category="safety_backup")
        return {'success': False, 'backup_path': None, 'error': str(e)}

def find_actual_game_folder(file_base):
    try:
        from infrastructure.config.constants import FOLDERS
        temp_root = FOLDERS["temporaires"]
        if not os.path.exists(temp_root):
            log_message("DEBUG", f"Dossier temporaire inexistant: {temp_root}", category="validation")
            return None
        
        
        for game_folder in os.listdir(temp_root):
            game_path = os.path.join(temp_root, game_folder)
            if os.path.isdir(game_path):
                # Structure 1: game_folder/fichiers_a_traduire/file_base_dialogue.txt
                translate_folder = os.path.join(game_path, "fichiers_a_traduire")
                if os.path.exists(translate_folder):
                    main_file = os.path.join(translate_folder, f"{file_base}_dialogue.txt")
                    if os.path.exists(main_file):
                        log_message("DEBUG", f"Dossier trouvé: {game_folder} pour {file_base}", category="validation")
                        return game_folder
                
                # Structure 2: game_folder/file_base/fichiers_a_traduire/file_base_dialogue.txt
                file_folder = os.path.join(game_path, file_base)
                if os.path.isdir(file_folder):
                    translate_folder = os.path.join(file_folder, "fichiers_a_traduire")
                    if os.path.exists(translate_folder):
                        main_file = os.path.join(translate_folder, f"{file_base}_dialogue.txt")
                        if os.path.exists(main_file):
                            log_message("DEBUG", f"Dossier trouvé: {game_folder}/{file_base} pour {file_base}", category="validation")
                            return game_folder
        
        log_message("ATTENTION", f"Aucun dossier trouvé pour file_base: {file_base}", category="validation")
        return None
    except Exception as e:
        log_message("ERREUR", f"Erreur find_actual_game_folder: {e}", category="validation")
        return None

class ValidationSystem:
    """
    Système de validation refait de A à Z
    - Plus clair et plus robuste
    - Logs détaillés pour le débogage
    - Gestion d'erreurs améliorée
    """
    
    def __init__(self):
        self.validation_results = {
            'overall_valid': True,
            'files_validated': {},
            'summary': {
                'total_expected': 0,
                'total_found': 0,
                'files_checked': 0,
                'errors': [],
                'warnings': []
            }
        }
    
    def validate_reconstruction_files(self, game_name: str, file_base: str, 
                                    extracted_count: int, asterix_count: int = 0, empty_count: int = 0) -> dict:
        """
        Valide tous les fichiers nécessaires pour la reconstruction
        
        Args:
            game_name: Nom du jeu (ex: "CoaSG-v0.6.1-pc")
            file_base: Nom de base du fichier (ex: "main")
            extracted_count: Nombre de dialogues extraits
            asterix_count: Nombre d'astérisques extraits
            empty_count: Nombre de lignes vides extraites
            
        Returns:
            dict: Résultats complets de la validation
        """
        # Logs de début supprimés : seront regroupés avec le résultat final
        
        # Réinitialiser les résultats
        self.validation_results = {
            'overall_valid': True,
            'files_validated': {},
            'summary': {
                'total_expected': extracted_count + asterix_count,
                'total_found': 0,
                'files_checked': 0,
                'errors': [],
                'warnings': []
            }
        }
        
        try:
            # 1. Valider le fichier dialogue principal
            if extracted_count > 0:
                self._validate_dialogue_file(game_name, file_base, extracted_count)
            
            # 2. Valider le fichier astérisques (si nécessaire)
            if asterix_count > 0:
                self._validate_asterix_file(game_name, file_base, asterix_count)
            
            # 3. Calculer le résultat final
            self._calculate_final_result()
            
            # 4. Logger le résultat
            self._log_validation_result()
            
            return self.validation_results
            
        except Exception as e:
            log_message("ERREUR", f"Erreur critique lors de la validation: {e}", category="validation")
            self.validation_results['overall_valid'] = False
            self.validation_results['summary']['errors'].append(f"Erreur critique: {str(e)}")
            return self.validation_results
    
    def _validate_dialogue_file(self, game_name: str, file_base: str, expected_count: int):
        """Valide le fichier dialogue principal avec support des fichiers multiples"""
        file_path = os.path.join(FOLDERS["temporaires"], game_name, file_base, "fichiers_a_traduire", f"{file_base}_dialogue.txt")
        
        log_message("DEBUG", f"📄 Validation fichier dialogue: {os.path.basename(file_path)}", category="validation")
        
        if not os.path.exists(file_path):
            error_msg = f"Fichier dialogue manquant: {file_path}"
            log_message("ERREUR", error_msg, category="validation")
            self._add_file_error('dialogue', error_msg)
            return
        
        try:
            # Charger tous les fichiers (principal + numérotés)
            folder = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            lines = TranslationValidator._load_translation_files(folder, filename)
            
            if not lines:
                error_msg = f"Aucun contenu trouvé dans les fichiers dialogue"
                log_message("ERREUR", error_msg, category="validation")
                self._add_file_error('dialogue', error_msg)
                return
            
            # Compter TOUTES les lignes (y compris les vides)
            total_lines = len(lines)
            non_empty_lines = sum(1 for line in lines if line.strip())
            empty_lines = total_lines - non_empty_lines
            
            log_message("DEBUG", f"   📊 Analyse: {total_lines} lignes total ({non_empty_lines} non-vides, {empty_lines} vides)", category="validation")
            
            # Pour les fichiers dialogue, on compte SEULEMENT les lignes non vides
            # (car l'extraction compte les lignes extraites, pas les lignes vides de séparation)
            actual_count = non_empty_lines
            
            # Comparer avec le nombre attendu
            if actual_count == expected_count:
                # Log individuel supprimé : sera regroupé dans le log final
                self._add_file_success('dialogue', actual_count, expected_count)
            else:
                diff = actual_count - expected_count
                if diff > 0:
                    error_msg = f"Fichier dialogue: {actual_count} lignes trouvées, {expected_count} attendues (+{diff} en trop)"
                    log_message("ERREUR", f"   ❌ {error_msg}", category="validation")
                    self._add_file_error('dialogue', error_msg, actual_count, expected_count)
                else:
                    error_msg = f"Fichier dialogue: {actual_count} lignes trouvées, {expected_count} attendues ({diff} manquantes)"
                    log_message("ERREUR", f"   ❌ {error_msg}", category="validation")
                    self._add_file_error('dialogue', error_msg, actual_count, expected_count)
                    
        except Exception as e:
            error_msg = f"Erreur lecture fichier dialogue: {str(e)}"
            log_message("ERREUR", error_msg, category="validation")
            self._add_file_error('dialogue', error_msg)
    
    def _validate_asterix_file(self, game_name: str, file_base: str, expected_count: int):
        """Valide le fichier astérisques avec support des fichiers multiples"""
        file_path = os.path.join(FOLDERS["temporaires"], game_name, file_base, "fichiers_a_traduire", f"{file_base}_asterix.txt")
        
        log_message("DEBUG", f"⭐ Validation fichier astérisques: {os.path.basename(file_path)}", category="validation")
        
        if not os.path.exists(file_path):
            error_msg = f"Fichier astérisques manquant: {file_path}"
            log_message("ERREUR", error_msg, category="validation")
            self._add_file_error('asterix', error_msg)
            return
        
        try:
            # Charger tous les fichiers (principal + numérotés)
            folder = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            lines = TranslationValidator._load_translation_files(folder, filename)
            
            if not lines:
                error_msg = f"Aucun contenu trouvé dans les fichiers astérisques"
                log_message("ERREUR", error_msg, category="validation")
                self._add_file_error('asterix', error_msg)
                return
            
            # Compter TOUTES les lignes (y compris les vides)
            total_lines = len(lines)
            non_empty_lines = sum(1 for line in lines if line.strip())
            empty_lines = total_lines - non_empty_lines
            
            log_message("DEBUG", f"   📊 Analyse: {total_lines} lignes total ({non_empty_lines} non-vides, {empty_lines} vides)", category="validation")
            
            # Pour les fichiers astérisques, on compte SEULEMENT les lignes non vides
            # (car l'extraction compte les astérisques extraits, pas les lignes vides)
            actual_count = non_empty_lines
            
            # Comparer avec le nombre attendu
            if actual_count == expected_count:
                # Log individuel supprimé : sera regroupé dans le log final
                self._add_file_success('asterix', actual_count, expected_count)
            else:
                diff = actual_count - expected_count
                if diff > 0:
                    error_msg = f"Fichier astérisques: {actual_count} lignes trouvées, {expected_count} attendues (+{diff} en trop)"
                    log_message("ERREUR", f"   ❌ {error_msg}", category="validation")
                    self._add_file_error('asterix', error_msg, actual_count, expected_count)
                else:
                    error_msg = f"Fichier astérisques: {actual_count} lignes trouvées, {expected_count} attendues ({diff} manquantes)"
                    log_message("ERREUR", f"   ❌ {error_msg}", category="validation")
                    self._add_file_error('asterix', error_msg, actual_count, expected_count)
                    
        except Exception as e:
            error_msg = f"Erreur lecture fichier astérisques: {str(e)}"
            log_message("ERREUR", error_msg, category="validation")
            self._add_file_error('asterix', error_msg)
    
    def _add_file_success(self, file_type: str, actual_count: int, expected_count: int):
        """Ajoute un fichier validé avec succès"""
        self.validation_results['files_validated'][file_type] = {
            'valid': True,
            'actual_count': actual_count,
            'expected_count': expected_count,
            'errors': [],
            'warnings': []
        }
        self.validation_results['summary']['total_found'] += actual_count
        self.validation_results['summary']['files_checked'] += 1
    
    def _add_file_error(self, file_type: str, error_msg: str, actual_count: int = 0, expected_count: int = 0):
        """Ajoute un fichier avec erreur"""
        self.validation_results['files_validated'][file_type] = {
            'valid': False,
            'actual_count': actual_count,
            'expected_count': expected_count,
            'errors': [error_msg],
            'warnings': []
        }
        self.validation_results['summary']['total_found'] += actual_count
        self.validation_results['summary']['files_checked'] += 1
        self.validation_results['summary']['errors'].append(error_msg)
        self.validation_results['overall_valid'] = False
    
    def _calculate_final_result(self):
        """Calcule le résultat final de la validation"""
        expected = self.validation_results['summary']['total_expected']
        found = self.validation_results['summary']['total_found']
        
        if found == expected:
            pass  # Pas de log ici, le log de succès est dans _log_validation_result()
        else:
            diff = found - expected
            if diff > 0:
                log_message("ERREUR", f"🎯 VALIDATION ÉCHOUÉE: {found}/{expected} éléments (+{diff} en trop)", category="validation")
            else:
                log_message("ERREUR", f"🎯 VALIDATION ÉCHOUÉE: {found}/{expected} éléments ({diff} manquants)", category="validation")
    
    def _log_validation_result(self):
        """Log le résultat final de la validation"""
        file_base = self.validation_results.get('file_base', 'fichier')
        if self.validation_results['overall_valid']:
            log_message("INFO", f"✅ VALIDATION {file_base} : {self.validation_results['summary']['total_found']}/{self.validation_results['summary']['total_expected']} éléments validés", category="validation")
        else:
            log_message("ERREUR", f"❌ VALIDATION {file_base} ÉCHOUÉE : {self.validation_results['summary']['total_found']}/{self.validation_results['summary']['total_expected']} éléments validés", category="validation")
            log_message("ERREUR", f"   Erreurs: {len(self.validation_results['summary']['errors'])}", category="validation")
            for error in self.validation_results['summary']['errors']:
                log_message("ERREUR", f"   - {error}", category="validation")


def validate_before_reconstruction(file_base: str, extracted_count: int, asterix_count: int = 0, empty_count: int = 0, original_path: str = None) -> dict:
    """
    Fonction de validation avant reconstruction - Version refaite
    
    Args:
        file_base: Nom de base du fichier (ex: "main")
        extracted_count: Nombre de dialogues extraits
        asterix_count: Nombre d'astérisques extraits  
        empty_count: Nombre de lignes vides extraites (ignoré dans la validation)
        original_path: Chemin du fichier original (utilisé pour déterminer le game_name correct)
        
    Returns:
        dict: Résultats de la validation
    """
    # Log simplifié : suppression du log de démarrage
    
    # ✅ CORRIGÉ : Utiliser original_path pour déterminer le game_name correct
    # Au lieu de chercher dans tous les dossiers (qui peut trouver le mauvais)
    if original_path:
        from infrastructure.helpers.unified_functions import extract_game_name
        game_name = extract_game_name(original_path)
        log_message("DEBUG", f"Game name déterminé depuis original_path: {game_name}", category="validation")
    else:
        # Fallback : chercher dans tous les dossiers (ancien comportement)
        game_name = find_actual_game_folder(file_base)
        if not game_name:
            log_message("ERREUR", f"Impossible de trouver le dossier pour {file_base}", category="validation")
            return {
                'overall_valid': False,
                'summary': {
                    'total_expected': extracted_count + asterix_count,
                    'total_found': 0,
                    'files_checked': 0,
                    'errors': [f"Dossier non trouvé pour {file_base}"],
                    'warnings': []
                }
            }
        log_message("ATTENTION", f"Game name trouvé par recherche (fallback): {game_name}", category="validation")
    
    log_message("INFO", f"Dossier trouvé: {game_name}", category="validation")
    
    # Créer et utiliser le système de validation
    validator = ValidationSystem()
    return validator.validate_reconstruction_files(
        game_name, file_base, extracted_count, asterix_count, empty_count
    )

def fix_unescaped_quotes_in_txt(file_path):
    try:
        if not os.path.exists(file_path):
            return 0
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        corrections_made = 0
        lines = content.split('\n')
        corrected_lines = []
        for i, line in enumerate(lines):
            corrected_line = line
           
            # Correction des guillemets non échappés
            unescaped_quotes = re.findall(r'(?<!\\)"', line)
            if unescaped_quotes:
                corrected_line = re.sub(r'(?<!\\)"', r'\\"', corrected_line)
                corrections_made += len(unescaped_quotes)
           
            # Correction des guillemets français ouvrants
            french_quotes_open = re.findall(r'[«]|(?<![<>])<<(?![<>])', corrected_line)
            if french_quotes_open:
                # Remplacer « par \"
                corrected_line = re.sub(r'«', r'\\"', corrected_line)
                # Remplacer << par \" (seulement si pas entouré par < ou >)
                corrected_line = re.sub(r'(?<![<>])<<(?![<>])', r'\\"', corrected_line)
                corrections_made += len(french_quotes_open)
            
            # Correction des guillemets français fermants
            french_quotes_close = re.findall(r'[»]|(?<![<>])>>(?![<>])', corrected_line)
            if french_quotes_close:
                # Remplacer » par \"
                corrected_line = re.sub(r'»', r'\\"', corrected_line)
                # Remplacer >> par \" (seulement si pas entouré par < ou >)
                corrected_line = re.sub(r'(?<![<>])>>(?![<>])', r'\\"', corrected_line)
                corrections_made += len(french_quotes_close)

            # NOUVEAU: Correction des points de suspension DeepL [...] → ...
            deepl_ellipsis = re.findall(r'\[\.\.\.\]', corrected_line)
            if deepl_ellipsis:
                corrected_line = re.sub(r'\[\.\.\.\]', '...', corrected_line)
                corrections_made += len(deepl_ellipsis)
           
            # Correction des pourcentages isolés - VERSION CORRIGÉE
            # Éviter les % qui sont déjà dans %% ou qui sont suivis de lettres/autres %
            isolated_percent = re.findall(r'(?<!%)%(?!%|[a-zA-Z])', corrected_line)
            if isolated_percent:
                corrected_line = re.sub(r'(?<!%)%(?!%|[a-zA-Z])', r'%%', corrected_line)
                corrections_made += len(isolated_percent)
           
            corrected_lines.append(corrected_line)
       
        if corrections_made > 0:
            corrected_content = '\n'.join(corrected_lines)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(corrected_content)
       
        return corrections_made
    except Exception as e:
        log_message("ATTENTION", f"Erreur lors de la correction des guillemets/pourcentages/ellipses: {e}", category="fix_quotes")
        return 0
