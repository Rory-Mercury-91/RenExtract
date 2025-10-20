# core/coherence_checker_unified.py
# Unified Coherence Checker System
# Created for RenExtract 

"""
Système unifié de vérification de cohérence
- Une seule logique pour fichier unique ET dossier
- Options configurables par type d'erreur
- Liste d'exclusions personnalisable pour lignes non traduites
- Format de rapport unifié
- 🆕 Ouverture automatique configurable du rapport
"""

import os
import re
import glob
import time
from datetime import datetime
from infrastructure.logging.logging import log_message
from infrastructure.config.config import config_manager
from infrastructure.config.constants import FOLDERS, ensure_folders_exist
from infrastructure.helpers.unified_functions import extract_game_name
from core.services.reporting.coherence_html_report_generator import create_html_coherence_report
from ui.shared.project_widgets import ProjectLanguageSelector

class UnifiedCoherenceChecker:
    """Vérificateur de cohérence unifié avec options configurables"""
    
    def __init__(self):
        """Initialisation nettoyée du checker de cohérence"""
        self.start_time = None
        self.total_issues = 0
        self.files_analyzed = 0
        self.results_by_file = {}
        self.project_path = None  # 🆕 Stocke le chemin du projet pour les exclusions
        
        # Chargement des options depuis la config (avec valeurs par défaut True)
        # Note : Les 4 options critiques (variables, tags, escape_sequences, line_structure) 
        # sont masquées de l'interface mais restent configurables via config.json
        self.check_variables = config_manager.get('coherence_check_variables', True)
        self.check_tags = config_manager.get('coherence_check_tags', True)
        self.check_escape_sequences = config_manager.get('coherence_check_escape_sequences', True)
        self.check_line_structure = config_manager.get('coherence_check_line_structure', True)
        self.check_untranslated = config_manager.get('coherence_check_untranslated', True)
        self.check_ellipsis = config_manager.get('coherence_check_ellipsis', True)
        self.check_percentages = config_manager.get('coherence_check_percentages', True)
        self.check_quotations = config_manager.get('coherence_check_quotations', True)
        self.check_parentheses = config_manager.get('coherence_check_parentheses', True)
        self.check_syntax = config_manager.get('coherence_check_syntax', True)
        self.check_deepl_ellipsis = config_manager.get('coherence_check_deepl_ellipsis', True)
        self.check_isolated_percent = config_manager.get('coherence_check_isolated_percent', True)
        self.check_french_quotes = config_manager.get('coherence_check_french_quotes', True)
        # Placeholders et codes spéciaux désactivés - validation redondante
        self.check_special_codes = False
        self.check_placeholders = False
        
        # Exclusions de fichiers depuis la config
        self.excluded_files = config_manager.get('coherence_excluded_files')
        
        log_message("DEBUG", f"Options cohérence: variables={self.check_variables}, tags={self.check_tags}, codes={self.check_special_codes}, untranslated={self.check_untranslated}, ellipsis={self.check_ellipsis}, escape={self.check_escape_sequences}, percent={self.check_percentages}, quotes={self.check_quotations}, parens={self.check_parentheses}, syntax={self.check_syntax}, deepl={self.check_deepl_ellipsis}, isolated={self.check_isolated_percent}, french={self.check_french_quotes}, structure={self.check_line_structure}", category="coherence_options")
        log_message("DEBUG", f"Fichiers exclus: {config_manager.get('coherence_excluded_files')}", category="coherence_options")
    
    def analyze_path(self, path, return_details=False):
        """
        Analyse un fichier ou un dossier avec la logique unifiée
        
        Args:
            path (str): Chemin du fichier .rpy ou dossier tl
            return_details (bool): Si True, retourne les détails pour l'interface
            
        Returns:
            str ou dict: Chemin du rapport ou détails selon return_details
        """
        # MODIFICATION N°1 : On mémorise le chemin d'origine ici
        self.original_analysis_path = path
        
        # 🆕 Déterminer le chemin du projet pour les exclusions
        self.project_path = _find_project_root(path)
        
        self.start_time = time.time()
        self.total_issues = 0
        self.files_analyzed = 0
        self.results_by_file = {}
        
        try:
            if os.path.isfile(path) and path.endswith('.rpy'):
                # Mode fichier unique
                files_to_analyze = [path]
                analysis_root = os.path.dirname(path)
            else:
                # Mode dossier
                files_to_analyze = self._find_rpy_files(path)
                analysis_root = path
            
            if not files_to_analyze:
                log_message("ATTENTION", f"Aucun fichier .rpy trouvé dans : {path}", category="coherence_analysis")
                return None if not return_details else {'error': 'Aucun fichier trouvé'}
            
            # Analyser tous les fichiers avec la même logique
            excluded_files = []
            for file_path in files_to_analyze:
                if self._should_exclude_file(file_path):
                    excluded_files.append(os.path.basename(file_path))
                    continue
                    
                file_results = self._analyze_single_file(file_path)
                if file_results['issues']:
                    # relative_path = os.path.relpath(file_path, analysis_root)
                    self.results_by_file[file_path] = file_results
                    # self.results_by_file[relative_path] = file_results
                    self.total_issues += len(file_results['issues'])
                
                self.files_analyzed += 1
            
            # Log des fichiers exclus sur une seule ligne
            if excluded_files:
                log_message("DEBUG", f"Fichiers système exclus automatiquement: {', '.join(excluded_files)}", category="file_exclusion")
            
            # Générer le rapport unifié
            execution_time = time.time() - self.start_time
            
            # MODIFICATION N°2 : On retire 'analysis_root' de l'appel
            rapport_path = self._create_unified_report(execution_time)
            
            # Auto-ouverture gérée dans _create_unified_report() pour éviter la duplication
            
            # Retour selon le mode
            if return_details:
                return {
                    'rapport_path': rapport_path,
                    'stats': {
                        'files_analyzed': self.files_analyzed,
                        'total_issues': self.total_issues,
                        'execution_time': execution_time,
                        'issues_by_file': {k: len(v['issues']) for k, v in self.results_by_file.items()}
                    }
                }
            else:
                return rapport_path
                
        except Exception as e:
            log_message("ERREUR", f"Erreur analyse cohérence: {e}", category="coherence_analysis")
            if return_details:
                return {'error': str(e)}
            return None
    
    def _find_rpy_files(self, folder_path):
        """Trouve tous les fichiers .rpy dans un dossier - VERSION CORRIGÉE pour les caractères spéciaux"""
        try:
            if not os.path.exists(folder_path):
                log_message("ERREUR", f"Dossier inexistant: {folder_path}", category="file_search")
                return []
            
            # Utiliser os.walk au lieu de glob pour éviter les problèmes avec les crochets
            rpy_files = []
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith('.rpy'):
                        rpy_files.append(os.path.join(root, file))
            
            # Log des fichiers trouvés sur une seule ligne
            if rpy_files:
                file_names = [os.path.basename(f) for f in rpy_files]
                log_message("DEBUG", f"Fichiers .rpy trouvés dans {folder_path}: {', '.join(file_names)}", category="file_search")
            
            return rpy_files
            
        except Exception as e:
            log_message("ERREUR", f"Erreur recherche fichiers dans '{folder_path}': {e}", category="file_search")
            return []

    def _should_exclude_file(self, file_path):
        """Vérifie si un fichier doit être exclu de l'analyse - VERSION AVEC EXCLUSION AUTOMATIQUE"""
        filename = os.path.basename(file_path).lower()
        
        # ✅ EXCLUSION AUTOMATIQUE : Fichiers système + fichiers générés
        system_generated_files = [
            'common.rpy',
            '99_Z_Console.rpy',
            '99_Z_ScreenPreferences.rpy',
            '99_Z_FontSystem.rpy'
        ]
        
        # Vérifier d'abord les fichiers système
        for system_file in system_generated_files:
            if system_file.lower() in filename:
                return True
        
        # Ensuite vérifier les exclusions utilisateur
        try:
            excluded_files_config = config_manager.get('coherence_excluded_files')
            if excluded_files_config:
                excluded_list = [f.strip().lower() for f in excluded_files_config.split(',') if f.strip()]
                
                for excluded_file in excluded_list:
                    if excluded_file in filename:
                        return True
        
        except Exception as e:
            log_message("ERREUR", f"Erreur vérification exclusions fichiers: {e}", category="file_exclusion")
        
        return False
    
    def _analyze_single_file(self, file_path):
        """Analyse un fichier unique avec gestion correcte des lignes voice"""
        results = {
            'file_path': file_path,
            'issues': [],
            'lines_checked': 0
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            old_line = None
            old_line_num = 0
            
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                
                # Ignorer les commentaires de fichier
                if self._is_file_comment(stripped):
                    continue
                
                # Détecter les lignes OLD (ignorer les voice)
                if self._is_old_line(stripped):
                    if self._is_voice_line(stripped):
                        # Ignorer complètement les lignes voice OLD
                        continue
                    old_line = stripped
                    old_line_num = i
                    continue
                
                # Détecter les lignes NEW (ignorer les voice)
                if self._is_new_line(stripped):
                    if self._is_voice_line(stripped):
                        # Ignorer complètement les lignes voice NEW
                        continue
                        
                    results['lines_checked'] += 1
                    
                    if old_line:
                        # Vérifier la cohérence OLD/NEW
                        issues = self._check_line_coherence(
                            old_line, stripped, old_line_num, i, file_path
                        )
                        results['issues'].extend(issues)
                        
                        # Reset pour la prochaine paire
                        old_line = None
                        old_line_num = 0
                    else:
                        # Ligne NEW sans OLD - vérifier si c'est problématique
                        if self._is_missing_old_problematic(stripped, lines, i):
                            results['issues'].append({
                                'line': i,
                                'type': 'MISSING_OLD',
                                'description': "Ligne NEW sans OLD correspondant",
                                'old_content': "MANQUANT",
                                'new_content': stripped
                            })
            
        except Exception as e:
            log_message("ERREUR", f"Erreur analyse fichier {file_path}: {e}", category="file_analysis")
            results['issues'].append({
                'line': 0,
                'type': 'FILE_ERROR',
                'description': f"Erreur de lecture: {str(e)}",
                'old_content': "",
                'new_content': ""
            })
        
        return results

    def _is_voice_line(self, line):
        """Vérifie si une ligne contient une instruction voice"""
        # Vérifier directement sur la ligne originale (avant extraction)
        stripped_line = line.strip()
        
        # Détecter les lignes voice directement
        is_voice = (stripped_line.startswith('voice ') and '"' in stripped_line)
        
        return is_voice

    def _check_line_coherence(self, old_line, new_line, old_line_num, new_line_num, file_path):
        """Vérifie la cohérence entre une ligne OLD et NEW avec options configurables"""
        issues = []
        
        try:
            # Nettoyer les lignes
            old_content = self._extract_line_content(old_line)
            new_content = self._extract_line_content(new_line)
            
            if not old_content or not new_content:
                return issues
            
            # Extraire les contenus entre guillemets
            old_texts = self._extract_quoted_content(old_content)
            new_texts = self._extract_quoted_content(new_content)
            
            if not old_texts or not new_texts:
                return issues
            
            # Vérifier chaque paire de contenus
            for old_text, new_text in zip(old_texts, new_texts):
                issues.extend(self._check_content_coherence(
                    old_text, new_text, old_line_num, new_line_num, file_path
                ))
            
            # Vérifier le nombre de guillemets
            if len(old_texts) != len(new_texts):
                issues.append({
                    'line': new_line_num,
                    'type': 'QUOTE_COUNT_MISMATCH',
                    'description': f"Nombre de guillemets différent (ANCIEN: {len(old_texts)}, NOUVEAU: {len(new_texts)})",
                    'old_content': old_content,
                    'new_content': new_content
                })
        
        except Exception as e:
            issues.append({
                'line': new_line_num,
                'type': 'ANALYSIS_ERROR',
                'description': f"Erreur d'analyse: {str(e)}",
                'old_content': old_line,
                'new_content': new_line
            })
        
        return issues
    
    def _check_content_coherence(self, old_text, new_text, old_line_num, new_line_num, file_path):
        """
        Vérifie la cohérence entre deux contenus textuels.
        
        LOGIQUE OPTIMISÉE : Une seule erreur par ligne
        - Priorité aux erreurs critiques (balises, variables)
        - Dès qu'une erreur est trouvée, on arrête les autres vérifications
        - Le traducteur corrigera toutes les erreurs en une seule passe
        """
        issues = []
        
        # 🆕 Vérifier si cette ligne est exclue globalement (par old_content)
        if self._is_excluded_by_content(old_text):
            return issues  # Ligne exclue, ignorer toutes les vérifications
        
        # 1. Vérifier les lignes non traduites (si activé) - PRIORITÉ MAXIMALE
        if self.check_untranslated and self._is_untranslated_line(old_text, new_text, file_path, new_line_num):
            issues.append({
                'line': new_line_num,
                'type': 'UNTRANSLATED_LINE',
                'description': "Ligne potentiellement non traduite (contenu identique)",
                'old_content': old_text,
                'new_content': new_text
            })
            return issues  # Arrêt immédiat si non traduit
        
        # 2. Vérifier les balises {} (si activé) - PRIORITÉ HAUTE
        if self.check_tags:
            tag_issues = self._check_tags_coherence(old_text, new_text, old_line_num, new_line_num)
            if tag_issues:
                return tag_issues  # Arrêt dès qu'on trouve une erreur de balise
        
        # 3. Vérifier les variables [] (si activé) - PRIORITÉ HAUTE
        if self.check_variables:
            var_issues = self._check_variables_coherence(old_text, new_text, old_line_num, new_line_num)
            if var_issues:
                return var_issues  # Arrêt dès qu'on trouve une erreur de variable
        
        # 4. Vérifier les placeholders (désactivé - validation redondante)
        if self.check_placeholders:
            placeholder_issues = self._check_placeholders_coherence(old_text, new_text, old_line_num, new_line_num)
            if placeholder_issues:
                return placeholder_issues
        
        # 5. Vérifier les séquences d'échappement (si activé) - PRIORITÉ MOYENNE
        if self.check_escape_sequences:
            escape_issues = self._check_escape_sequences_coherence(old_text, new_text, old_line_num, new_line_num)
            if escape_issues:
                return escape_issues
        
        # 6. Vérifier les pourcentages (si activé) - PRIORITÉ MOYENNE
        if self.check_percentages:
            percent_issues = self._check_percentages_coherence(old_text, new_text, old_line_num, new_line_num)
            if percent_issues:
                return percent_issues
        
        # 7. Vérifier les guillemets (si activé) - PRIORITÉ MOYENNE
        if self.check_quotations:
            quote_issues = self._check_quotations_coherence(old_text, new_text, old_line_num, new_line_num)
            if quote_issues:
                return quote_issues
        
        # 8. Vérifier les parenthèses (si activé) - PRIORITÉ BASSE
        if self.check_parentheses:
            paren_issues = self._check_parentheses_coherence(old_text, new_text, old_line_num, new_line_num)
            if paren_issues:
                return paren_issues
        
        # 9. Vérifier la syntaxe (si activé) - PRIORITÉ BASSE
        if self.check_syntax:
            syntax_issues = self._check_syntax_coherence(old_text, new_text, old_line_num, new_line_num)
            if syntax_issues:
                return syntax_issues
        
        # 10. Vérifier les ellipses DeepL (si activé) - PRIORITÉ BASSE
        if self.check_deepl_ellipsis:
            deepl_issues = self._check_deepl_ellipsis_coherence(old_text, new_text, old_line_num, new_line_num)
            if deepl_issues:
                return deepl_issues
        
        # 11. Vérifier les pourcentages isolés (si activé) - PRIORITÉ BASSE
        if self.check_isolated_percent:
            isolated_issues = self._check_isolated_percent_coherence(old_text, new_text, old_line_num, new_line_num)
            if isolated_issues:
                return isolated_issues
        
        # 12. Vérifier les guillemets français (si activé) - PRIORITÉ BASSE
        if self.check_french_quotes:
            french_issues = self._check_french_quotes_coherence(old_text, new_text, old_line_num, new_line_num)
            if french_issues:
                return french_issues
        
        # 13. Vérifier les codes spéciaux (si activé) - PRIORITÉ BASSE
        if self.check_special_codes:
            special_issues = self._check_special_codes_coherence(old_text, new_text, old_line_num, new_line_num)
            if special_issues:
                return special_issues
        
        # 14. Vérifier la structure des lignes (si activé) - PRIORITÉ TRÈS BASSE
        if self.check_line_structure:
            structure_issues = self._check_line_structure_coherence(old_text, new_text, old_line_num, new_line_num)
            if structure_issues:
                return structure_issues
        
        return issues  # Aucune erreur trouvée
    
    def _is_excluded_by_content(self, old_text):
        """
        Vérifie si une ligne est exclue globalement par son contenu (old_content).
        Utilisé pour les exclusions simples (ellipsis, percentages, quotations, etc.)
        """
        if not old_text or not old_text.strip():
            return False
        
        text = old_text.strip()
        
        # 1. Vérifier les exclusions simples (liste de strings)
        excluded_lines = config_manager.get('coherence_excluded_lines', [])
        if text in excluded_lines:
            return True
        
        # 2. Vérifier les exclusions précises (liste d'objets avec file/line/text)
        if self.project_path:
            exclusions = config_manager.get_coherence_exclusions(self.project_path)
            for excl in exclusions:
                if excl.get('text', '').strip() == text:
                    return True
        
        return False
    
    def _is_untranslated_line(self, old_text, new_text, file_path, line_num):
        """
        Vérifie si une ligne est probablement non traduite.
        🆕 Version avec exclusions précises (projet+fichier+ligne).
        """
        if old_text.strip() != new_text.strip():
            return False
        
        text = old_text.strip()
        
        # Auto-exclusions (patterns techniques)
        if self._is_auto_excluded(text):
            return False
        
        # 🆕 Vérifier les exclusions précises (projet+fichier+ligne)
        if self.project_path:
            exclusions = config_manager.get_coherence_exclusions(self.project_path)
            
            # Extraire le nom relatif du fichier
            file_relative = self._get_relative_file_path(file_path)
            
            for excl in exclusions:
                # Vérifier si cette exclusion correspond
                if (excl['line'] == line_num and 
                    excl['text'] == text and 
                    file_relative.endswith(excl['file'])):
                    return False  # Exclu
        
        # Si le texte est court et contient peu de mots, probablement OK
        if len(text) <= 3 or len(text.split()) <= 1:
            return False
        
        # Sinon, considérer comme non traduit
        return True
    
    def _get_relative_file_path(self, file_path):
        """Retourne le chemin relatif du fichier depuis le dossier tl"""
        try:
            # Trouver la position de 'tl/' dans le chemin
            if '/tl/' in file_path:
                parts = file_path.split('/tl/')
                if len(parts) > 1:
                    # Retourner ce qui est après tl/langue/
                    sub_parts = parts[1].split('/', 1)
                    if len(sub_parts) > 1:
                        return sub_parts[1].replace('\\', '/')
            elif '\\tl\\' in file_path:
                parts = file_path.split('\\tl\\')
                if len(parts) > 1:
                    sub_parts = parts[1].split('\\', 1)
                    if len(sub_parts) > 1:
                        return sub_parts[1].replace('\\', '/')
            
            # Fallback: retourner le nom du fichier
            return os.path.basename(file_path)
        except Exception:
            return os.path.basename(file_path)
    
    def _is_auto_excluded(self, text):
        """Vérifie les auto-exclusions par défaut"""
        # Ellipsis (si activé)
        if self.check_ellipsis and text in ['...', '…', '....', '.....']:
            return True
        
        # Variables seules
        if re.match(r'^\[[^\]]+\]', text):
            return True
        
        # Balises seules
        if re.match(r'^\{[^}]*\}', text):
            return True
        
        # Texte vide ou espaces
        if not text or text.isspace():
            return True
        
        # Ponctuations expressives (sauf ellipsis si désactivé)
        if self.check_ellipsis:
            # Si ellipsis activé, inclure les points dans les ponctuations expressives
            if re.match(r'^[!?…\.]+', text):
                return True
        else:
            # Si ellipsis désactivé, exclure les points des ponctuations expressives
            if re.match(r'^[!?…]+', text):
                return True
        
        # Onomatopées courtes (2-3 caractères)
        if len(text) <= 3 and re.match(r'^[A-Za-z]+[!?]*', text):
            return True
        
        return False
    
    def _check_variables_coherence(self, old_text, new_text, old_line_num, new_line_num):
        """Vérifie la cohérence des variables []"""
        issues = []
        
        try:
            old_vars = re.findall(r'\[[^\]]*\]', old_text)
            new_vars = re.findall(r'\[[^\]]*\]', new_text)
            
            # Normaliser les variables (enlever les fonctions !t, !u, etc.)
            old_vars_norm = [self._normalize_variable(var) for var in old_vars]
            new_vars_norm = [self._normalize_variable(var) for var in new_vars]
            
            if sorted(old_vars_norm) != sorted(new_vars_norm):
                issues.append({
                    'line': new_line_num,
                    'type': 'VARIABLE_MISMATCH',
                    'description': f"Variables incohérentes => Attendu: {old_vars}, Présent: {new_vars}",
                    'old_content': old_text,
                    'new_content': new_text
                })
        
        except Exception:
            pass
        
        return issues
    
    def _check_tags_coherence(self, old_text, new_text, old_line_num, new_line_num):
        """Vérifie la cohérence des balises {}"""
        issues = []
        
        try:
            old_tags = re.findall(r'\{[^}]*\}', old_text)
            new_tags = re.findall(r'\{[^}]*\}', new_text)
            
            if old_tags != new_tags:
                issues.append({
                    'line': new_line_num,
                    'type': 'TAG_MISMATCH',
                    'description': f"Balises incohérentes => Attendu: {old_tags}, Présent: {new_tags}",
                    'old_content': old_text,
                    'new_content': new_text
                })
        
        except Exception:
            pass
        
        return issues
    
    def _check_placeholders_coherence(self, old_text, new_text, old_line_num, new_line_num):
        """Vérifie la cohérence des placeholders RENPY_XX__"""
        issues = []
        
        try:
            old_placeholders = re.findall(r'RENPY_[A-Z_0-9]+', old_text)
            new_placeholders = re.findall(r'RENPY_[A-Z_0-9]+', new_text)
            
            # Placeholders incohérents
            if old_placeholders != new_placeholders:
                issues.append({
                    'line': new_line_num,
                    'type': 'PLACEHOLDER_MISMATCH',
                    'description': f"Placeholders incohérents => Attendu: {old_placeholders}, Présent: {new_placeholders}",
                    'old_content': old_text,
                    'new_content': new_text
                })
            
            # Placeholders non restaurés (présents dans NEW mais pas dans OLD)
            old_set = set(old_placeholders)
            new_set = set(new_placeholders)
            unrestored = new_set - old_set
            
            if unrestored:
                issues.append({
                    'line': new_line_num,
                    'type': 'UNRESTORED_PLACEHOLDER',
                    'description': f"Placeholders non restaurés => Attendu: remplacement automatique, Présent: {list(unrestored)}",
                    'old_content': old_text,
                    'new_content': new_text
                })
            
            # Placeholders malformés
            malformed = re.findall(r'RENPY_[A-Z_0-9]*(?![A-Z_0-9])', new_text)
            if malformed:
                issues.append({
                    'line': new_line_num,
                    'type': 'MALFORMED_PLACEHOLDER',
                    'description': f"Placeholders malformés => Attendu: RENPY_XX__, Présent: {malformed}",
                    'old_content': old_text,
                    'new_content': new_text
                })
        
        except Exception:
            pass
        
        return issues
    
    def _check_special_codes_coherence(self, old_text, new_text, old_line_num, new_line_num):
        """Vérifie la cohérence des codes spéciaux (\\n, --, %, parenthèses, guillemets français)"""
        issues = []
        
        try:
            # Codes spéciaux existants
            old_newlines = old_text.count('\\n')
            new_newlines = new_text.count('\\n')
            
            old_dashes = old_text.count('--')
            new_dashes = new_text.count('--')
            
            old_percent = len(re.findall(r'%[^%]*%', old_text))
            new_percent = len(re.findall(r'%[^%]*%', new_text))
            
            # NOUVEAU: Vérification des parenthèses
            old_open_parens = old_text.count('(')
            new_open_parens = new_text.count('(')
            old_close_parens = old_text.count(')')
            new_close_parens = new_text.count(')')
            
            # NOUVEAU: Vérification des guillemets français
            old_left_guillemets = old_text.count('«') + old_text.count('<<')
            new_left_guillemets = new_text.count('«') + new_text.count('<<')
            old_right_guillemets = old_text.count('»') + old_text.count('>>')
            new_right_guillemets = new_text.count('»') + new_text.count('>>')
            
            # NOUVEAU: Vérification des ellipses (...)
            old_ellipsis = old_text.count('...')
            new_ellipsis = new_text.count('...')
            
            # Vérifications existantes
            if old_newlines != new_newlines:
                issues.append({
                    'line': new_line_num,
                    'type': 'SPECIAL_CODE_MISMATCH',
                    'description': f"Séquences \\n incohérentes => Attendu: {old_newlines}, Présent: {new_newlines}",
                    'old_content': old_text,
                    'new_content': new_text
                })
            
            if old_dashes != new_dashes:
                # Vérification spéciale pour les transformations -- vers ...
                old_ellipsis = old_text.count('...')
                new_ellipsis = new_text.count('...')
                
                # Si les -- ont été transformés en ...
                if old_dashes > 0 and new_dashes < old_dashes and new_ellipsis > old_ellipsis:
                    issues.append({
                        'line': new_line_num,
                        'type': 'DASH_TO_ELLIPSIS_TRANSFORMATION',
                        'description': f"Tirets -- transformés en ... => {old_dashes} -- → {new_ellipsis} ...",
                        'old_content': old_text,
                        'new_content': new_text
                    })
                else:
                    issues.append({
                        'line': new_line_num,
                        'type': 'SPECIAL_CODE_MISMATCH',
                        'description': f"Tirets -- incohérents => Attendu: {old_dashes}, Présent: {new_dashes}",
                        'old_content': old_text,
                        'new_content': new_text
                    })
            
            # Vérification spéciale pour les %%
            if old_percent != new_percent:
                has_percent_word = 'percent' in old_text.lower() or 'pourcent' in old_text.lower()
                has_percent_symbol = '%' in new_text and '%' not in old_text
                
                if has_percent_word and has_percent_symbol:
                    description = f"Variables % ajoutées => Probablement légitime (percent → %) - Vérifiez si intentionnel"
                else:
                    description = f"Variables % incohérentes => Attendu: {old_percent}, Présent: {new_percent}"
                
                issues.append({
                    'line': new_line_num,
                    'type': 'SPECIAL_CODE_MISMATCH',
                    'description': description,
                    'old_content': old_text,
                    'new_content': new_text
                })
            
            # NOUVEAU: Vérifications des parenthèses
            if old_open_parens != new_open_parens:
                issues.append({
                    'line': new_line_num,
                    'type': 'PARENTHESES_MISMATCH',
                    'description': f"Parenthèses ouvrantes ( incohérentes => Attendu: {old_open_parens}, Présent: {new_open_parens}",
                    'old_content': old_text,
                    'new_content': new_text
                })
            
            if old_close_parens != new_close_parens:
                issues.append({
                    'line': new_line_num,
                    'type': 'PARENTHESES_MISMATCH',
                    'description': f"Parenthèses fermantes ) incohérentes => Attendu: {old_close_parens}, Présent: {new_close_parens}",
                    'old_content': old_text,
                    'new_content': new_text
                })
            
            # NOUVEAU: Vérifications des guillemets français
            if old_left_guillemets != new_left_guillemets:
                issues.append({
                    'line': new_line_num,
                    'type': 'FRENCH_QUOTES_MISMATCH',
                    'description': f"Guillemets français ouvrants « ou << incohérents => Attendu: {old_left_guillemets}, Présent: {new_left_guillemets}",
                    'old_content': old_text,
                    'new_content': new_text
                })
            
            if old_right_guillemets != new_right_guillemets:
                issues.append({
                    'line': new_line_num,
                    'type': 'FRENCH_QUOTES_MISMATCH',
                    'description': f"Guillemets français fermants » ou >> incohérents => Attendu: {old_right_guillemets}, Présent: {new_right_guillemets}",
                    'old_content': old_text,
                    'new_content': new_text
                })
            
            # NOUVEAU: Vérification des ellipses (...)
            if old_ellipsis != new_ellipsis:
                # Vérification spéciale pour les transformations ... vers --
                if old_ellipsis > 0 and new_ellipsis < old_ellipsis and new_dashes > old_dashes:
                    issues.append({
                        'line': new_line_num,
                        'type': 'ELLIPSIS_TO_DASH_TRANSFORMATION',
                        'description': f"Ellipses ... transformées en -- => {old_ellipsis} ... → {new_dashes} --",
                        'old_content': old_text,
                        'new_content': new_text
                    })
                else:
                    issues.append({
                        'line': new_line_num,
                        'type': 'SPECIAL_CODE_MISMATCH',
                        'description': f"Ellipses ... incohérentes => Attendu: {old_ellipsis}, Présent: {new_ellipsis}",
                        'old_content': old_text,
                        'new_content': new_text
                    })
        
        except Exception:
            pass
        
        return issues
    
    def _check_escape_sequences_coherence(self, old_text, new_text, old_line_num, new_line_num):
        """Vérifie la cohérence des séquences d'échappement \\n, \\t, \\r, \\\\"""
        issues = []
        
        try:
            # Compter les séquences d'échappement
            escape_patterns = [r'\\n', r'\\t', r'\\r', r'\\\\']
            
            for pattern in escape_patterns:
                old_count = len(re.findall(pattern, old_text))
                new_count = len(re.findall(pattern, new_text))
                
                if old_count != new_count:
                    escape_name = {
                        r'\\n': 'retours à la ligne',
                        r'\\t': 'tabulations',
                        r'\\r': 'retours chariot',
                        r'\\\\': 'backslashes échappés'
                    }.get(pattern, pattern)
                    
                    issues.append({
                        'line': new_line_num,
                        'type': 'ESCAPE_SEQUENCE_MISMATCH',
                        'description': f"Séquences d'échappement {escape_name} incohérentes => Attendu: {old_count}, Présent: {new_count}",
                        'old_content': old_text,
                        'new_content': new_text
                    })
        
        except Exception:
            pass
        
        return issues
    
    def _check_percentages_coherence(self, old_text, new_text, old_line_num, new_line_num):
        """Vérifie la cohérence des pourcentages % et %% (1 seule erreur fusionnée)"""
        issues = []
        
        try:
            # Variables de formatage %[^%]*%
            old_format_vars = len(re.findall(r'%[^%]*%', old_text))
            new_format_vars = len(re.findall(r'%[^%]*%', new_text))
            
            # Double % échappé
            old_double_percent = old_text.count('%%')
            new_double_percent = new_text.count('%%')
            
            # Fusionner les vérifications
            format_mismatch = old_format_vars != new_format_vars
            double_mismatch = old_double_percent != new_double_percent
            
            if format_mismatch or double_mismatch:
                # Construire une description détaillée
                details = []
                if format_mismatch:
                    details.append(f"Variables % (Attendu: {old_format_vars}, Présent: {new_format_vars})")
                if double_mismatch:
                    details.append(f"Échappés %% (Attendu: {old_double_percent}, Présent: {new_double_percent})")
                
                issues.append({
                    'line': new_line_num,
                    'type': 'PERCENTAGE_MISMATCH',
                    'description': f"Pourcentages incohérents => {', '.join(details)}",
                    'old_content': old_text,
                    'new_content': new_text
                })
        
        except Exception:
            pass
        
        return issues
    
    def _check_quotations_coherence(self, old_text, new_text, old_line_num, new_line_num):
        """Vérifie la cohérence des guillemets \" et échappés \\\" (1 seule erreur fusionnée)"""
        issues = []
        
        try:
            # Guillemets échappés \"
            old_escaped_quotes = old_text.count('\\"')
            new_escaped_quotes = new_text.count('\\"')
            
            # Guillemets non échappés (dans le contenu)
            old_unescaped_quotes = len(re.findall(r'(?<!\\)"', old_text))
            new_unescaped_quotes = len(re.findall(r'(?<!\\)"', new_text))
            
            # Fusionner les vérifications
            escaped_mismatch = old_escaped_quotes != new_escaped_quotes
            unescaped_mismatch = old_unescaped_quotes != new_unescaped_quotes
            
            if escaped_mismatch or unescaped_mismatch:
                # Construire une description détaillée
                details = []
                if escaped_mismatch:
                    details.append(f"Échappés \\\" (Attendu: {old_escaped_quotes}, Présent: {new_escaped_quotes})")
                if unescaped_mismatch:
                    details.append(f"Non échappés \" (Attendu: {old_unescaped_quotes}, Présent: {new_unescaped_quotes})")
                
                issues.append({
                    'line': new_line_num,
                    'type': 'QUOTES_MISMATCH',
                    'description': f"Guillemets incohérents => {', '.join(details)}",
                    'old_content': old_text,
                    'new_content': new_text
                })
        
        except Exception:
            pass
        
        return issues
    
    def _check_parentheses_coherence(self, old_text, new_text, old_line_num, new_line_num):
        """Vérifie la cohérence des parenthèses () et crochets [] (1 seule erreur fusionnée)"""
        issues = []
        
        try:
            # Parenthèses
            old_open_parens = old_text.count('(')
            new_open_parens = new_text.count('(')
            old_close_parens = old_text.count(')')
            new_close_parens = new_text.count(')')
            
            # Crochets (ne sont vérifiés que si pas de vérification variables activée)
            # Sinon redondant avec _check_variables_coherence
            old_open_brackets = old_text.count('[')
            new_open_brackets = new_text.count('[')
            old_close_brackets = old_text.count(']')
            new_close_brackets = new_text.count(']')
            
            # Fusionner toutes les vérifications en une seule erreur
            parens_mismatch = (old_open_parens != new_open_parens or 
                               old_close_parens != new_close_parens)
            brackets_mismatch = (old_open_brackets != new_open_brackets or 
                                 old_close_brackets != new_close_brackets)
            
            if parens_mismatch or brackets_mismatch:
                # Construire une description détaillée
                details = []
                if parens_mismatch:
                    details.append(f"( ) (Attendu: {old_open_parens}/{old_close_parens}, Présent: {new_open_parens}/{new_close_parens})")
                if brackets_mismatch:
                    details.append(f"[ ] (Attendu: {old_open_brackets}/{old_close_brackets}, Présent: {new_open_brackets}/{new_close_brackets})")
                
                issues.append({
                    'line': new_line_num,
                    'type': 'PARENTHESES_MISMATCH',
                    'description': f"Parenthèses/Crochets incohérents => {', '.join(details)}",
                    'old_content': old_text,
                    'new_content': new_text
                })
        
        except Exception:
            pass
        
        return issues
    
    def _check_syntax_coherence(self, old_text, new_text, old_line_num, new_line_num):
        """Vérifie la syntaxe Ren'Py et structure des lignes"""
        issues = []
        
        try:
            # Équilibre des guillemets
            old_quotes = old_text.count('"')
            new_quotes = new_text.count('"')
            
            # Ne signaler que si les deux lignes ont un nombre impair différent
            if (old_quotes % 2 != 0) != (new_quotes % 2 != 0):
                issues.append({
                    'line': new_line_num,
                    'type': 'QUOTE_BALANCE_ERROR',
                    'description': f"Guillemets non équilibrés => OLD: {old_quotes}, NEW: {new_quotes}",
                    'old_content': old_text,
                    'new_content': new_text
                })
            
            # Séquences d'échappement malformées
            malformed_escapes = re.findall(r'\\(?![ntr\\"])', new_text)
            if malformed_escapes:
                issues.append({
                    'line': new_line_num,
                    'type': 'MALFORMED_ESCAPE_SEQUENCE',
                    'description': f"Séquences d'échappement malformées détectées: {malformed_escapes}",
                    'old_content': old_text,
                    'new_content': new_text
                })
        
        except Exception:
            pass
        
        return issues
    
    def _check_deepl_ellipsis_coherence(self, old_text, new_text, old_line_num, new_line_num):
        """Vérifie les ellipses DeepL [...] → ..."""
        issues = []
        
        try:
            # Ellipses DeepL [...]
            old_deepl_ellipsis = len(re.findall(r'\[\.\.\.\]', old_text))
            new_deepl_ellipsis = len(re.findall(r'\[\.\.\.\]', new_text))
            
            if old_deepl_ellipsis != new_deepl_ellipsis:
                issues.append({
                    'line': new_line_num,
                    'type': 'DEEPL_ELLIPSIS_MISMATCH',
                    'description': f"Ellipses DeepL [...] incohérentes => Attendu: {old_deepl_ellipsis}, Présent: {new_deepl_ellipsis} (devrait être transformées en ...)",
                    'old_content': old_text,
                    'new_content': new_text
                })
        
        except Exception:
            pass
        
        return issues
    
    def _check_isolated_percent_coherence(self, old_text, new_text, old_line_num, new_line_num):
        """Vérifie les pourcentages isolés % → %%"""
        issues = []
        
        try:
            # Pourcentages isolés (pas dans %% ou %variable)
            old_isolated = len(re.findall(r'(?<!%)%(?!%|[a-zA-Z])', old_text))
            new_isolated = len(re.findall(r'(?<!%)%(?!%|[a-zA-Z])', new_text))
            
            if old_isolated != new_isolated:
                issues.append({
                    'line': new_line_num,
                    'type': 'ISOLATED_PERCENT_MISMATCH',
                    'description': f"Pourcentages isolés % incohérents => Attendu: {old_isolated}, Présent: {new_isolated} (devraient être échappés en %%)",
                    'old_content': old_text,
                    'new_content': new_text
                })
        
        except Exception:
            pass
        
        return issues
    
    def _check_french_quotes_coherence(self, old_text, new_text, old_line_num, new_line_num):
        """Vérifie les guillemets français «» ou << >> → \" (1 seule erreur fusionnée)"""
        issues = []
        
        try:
            # Guillemets français
            old_french_open = old_text.count('«')
            new_french_open = new_text.count('«')
            old_french_close = old_text.count('»')
            new_french_close = new_text.count('»')
            
            # Chevrons
            old_chevron_open = len(re.findall(r'(?<![<>])<<(?![<>])', old_text))
            new_chevron_open = len(re.findall(r'(?<![<>])<<(?![<>])', new_text))
            old_chevron_close = len(re.findall(r'(?<![<>])>>(?![<>])', old_text))
            new_chevron_close = len(re.findall(r'(?<![<>])>>(?![<>])', new_text))
            
            # Fusionner toutes les vérifications en une seule erreur
            french_mismatch = (old_french_open != new_french_open or 
                               old_french_close != new_french_close)
            chevron_mismatch = (old_chevron_open != new_chevron_open or 
                                old_chevron_close != new_chevron_close)
            
            if french_mismatch or chevron_mismatch:
                # Construire une description détaillée
                details = []
                if french_mismatch:
                    details.append(f"« » (Attendu: {old_french_open}/{old_french_close}, Présent: {new_french_open}/{new_french_close})")
                if chevron_mismatch:
                    details.append(f"<< >> (Attendu: {old_chevron_open}/{old_chevron_close}, Présent: {new_chevron_open}/{new_chevron_close})")
                
                issues.append({
                    'line': new_line_num,
                    'type': 'FRENCH_QUOTES_MISMATCH',
                    'description': f"Guillemets français incohérents => {', '.join(details)} (devraient être transformés en \")",
                    'old_content': old_text,
                    'new_content': new_text
                })
        
        except Exception:
            pass
        
        return issues
    
    def _check_line_structure_coherence(self, old_text, new_text, old_line_num, new_line_num):
        """Vérifie la structure des lignes old/new"""
        issues = []
        
        try:
            # Vérifier la cohérence de longueur (approximative)
            old_length = len(old_text.strip())
            new_length = len(new_text.strip())
            
            # Si la différence est très importante (plus de 50% de différence)
            if old_length > 0 and new_length > 0:
                length_ratio = max(old_length, new_length) / min(old_length, new_length)
                if length_ratio > 3.0:  # Plus de 200% de différence (plus tolérant pour EN→FR)
                    issues.append({
                        'line': new_line_num,
                        'type': 'LENGTH_DISCREPANCY',
                        'description': f"Différence de longueur importante => OLD: {old_length} chars, NEW: {new_length} chars (ratio: {length_ratio:.1f})",
                        'old_content': old_text,
                        'new_content': new_text
                    })
            
            # Vérifier les caractères spéciaux non échappés
            special_chars = ['{', '}', '[', ']', '%']
            for char in special_chars:
                old_count = old_text.count(char)
                new_count = new_text.count(char)
                if old_count != new_count:
                    issues.append({
                        'line': new_line_num,
                        'type': 'SPECIAL_CHAR_MISMATCH',
                        'description': f"Caractère spécial '{char}' incohérent => Attendu: {old_count}, Présent: {new_count}",
                        'old_content': old_text,
                        'new_content': new_text
                    })
        
        except Exception:
            pass
        
        return issues
    
    def _normalize_variable(self, variable):
        """Normalise une variable en enlevant les fonctions de traduction"""
        # Enlever les fonctions !t, !u, !l, !c
        normalized = re.sub(r'![tulc]', '', variable)
        return normalized
    
    def _extract_line_content(self, line):
        """Extrait le contenu d'une ligne (enlève # old, etc.)"""
        line = line.strip()
        
        if line.startswith('# old '):
            return line[6:].strip()
        elif line.startswith('old '):
            return line[4:].strip()
        elif line.startswith('new '):
            return line[4:].strip()
        else:
            # Ligne de dialogue normale (enlever le préfixe du personnage)
            # Exemple: n "Bonjour" -> "Bonjour"
            match = re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s+"(.+)"', line)
            if match:
                return f'"{match.group(1)}"'
            return line
    
    def _extract_quoted_content(self, line):
        """Extrait les contenus entre guillemets d'une ligne"""
        try:
            matches = []
            i = 0
            while i < len(line):
                if line[i] == '"':
                    start = i + 1
                    i += 1
                    content = ""
                    
                    while i < len(line):
                        if line[i] == '\\' and i + 1 < len(line):
                            content += line[i:i+2]
                            i += 2
                        elif line[i] == '"':
                            matches.append(content)
                            break
                        else:
                            content += line[i]
                            i += 1
                else:
                    i += 1
            
            return matches
        
        except Exception:
            return re.findall(r'"([^"]*)"', line)
    
    def _is_file_comment(self, line):
        """Vérifie si une ligne est un commentaire de fichier"""
        return (line.startswith('# ') and 
                ('.rpy:' in line or 
                 line.startswith('# game/') or 
                 line.startswith('# renpy/') or 
                 line.startswith('# common/')))
    
    def _is_old_line(self, line):
        """Vérifie si une ligne est une ligne OLD"""
        if line.startswith('old ') and '"' in line:
            return True
        
        if not line.startswith('# '):
            return False
        
        has_quotes = '"' in line
        has_old_keyword = 'old ' in line.lower()
        is_file_comment = self._is_file_comment(line)
        is_todo_comment = 'TODO:' in line or 'Translation updated' in line
        
        return (has_quotes or has_old_keyword) and not is_file_comment and not is_todo_comment
    
    def _is_new_line(self, line):
        """Vérifie si une ligne est une ligne NEW"""
        if line.startswith('#') or line.startswith('old '):
            return False
        
        # Ignorer les lignes voice
        if self._is_voice_line(line):
            return False
        
        if line.startswith('new ') and '"' in line:
            return True
        
        if '"' not in line:
            return False
        
        if line.lower().startswith('translate '):
            return False
        
        if ':' in line and any(keyword in line.lower() for keyword in ['label ', 'menu:', 'if ', 'else:', 'elif ']):
            return False
        
        # Debug temporaire pour les lignes NEW détectées
        return True
    
    def _is_missing_old_problematic(self, new_line, all_lines, line_index):
        """Vérifie si l'absence de ligne OLD est problématique"""
        try:
            # Vérifier si on est dans une section strings
            if self._is_in_strings_section(line_index, all_lines):
                return False
            
            # Vérifier le contexte
            context_range = max(0, line_index - 10)
            previous_lines = all_lines[context_range:line_index-1]
            
            for prev_line in reversed(previous_lines):
                prev_stripped = prev_line.strip()
                
                if prev_stripped.startswith('translate ') and ':' in prev_stripped:
                    return False
                
                if self._is_file_comment(prev_stripped):
                    return False
            
            # Ignorer les lignes très courtes ou principalement du code
            if len(new_line.strip()) <= 5 or self._is_mostly_code(new_line):
                return False
            
            return True
        
        except Exception:
            return False
    
    def _is_in_strings_section(self, line_index, all_lines):
        """Vérifie si on est dans une section translate strings"""
        try:
            search_start = max(0, line_index - 50)
            
            for i in range(search_start, line_index):
                line = all_lines[i].strip()
                
                if line.startswith('translate ') and line.endswith('strings:'):
                    return True
                
                if (line.startswith('translate ') and 
                    not line.endswith('strings:') and 
                    ':' in line and 'strings' not in line):
                    return False
            
            return False
        
        except Exception:
            return False
    
    def _is_mostly_code(self, text):
        """Vérifie si une ligne contient principalement du code"""
        try:
            code_chars = 0
            total_chars = len(text)
            
            if total_chars == 0:
                return True
            
            variables = re.findall(r'\[[^\]]*\]|\{[^}]*\}|%\([^)]*\)|%[a-zA-Z_]|RENPY_[A-Z_0-9]+', text)
            for var in variables:
                code_chars += len(var)
            
            escapes = re.findall(r'\\[a-zA-Z]', text)
            for esc in escapes:
                code_chars += len(esc)
            
            code_ratio = code_chars / total_chars
            return code_ratio > 0.4
        
        except Exception:
            return False
    
    def _calculate_issues_by_type(self):
        """Calcule le nombre d'erreurs par type"""
        issues_by_type = {}
        
        for file_results in self.results_by_file.values():
            for issue in file_results.get('issues', []):
                issue_type = issue['type']
                issues_by_type[issue_type] = issues_by_type.get(issue_type, 0) + 1
        
        return issues_by_type

    def _create_unified_report(self, execution_time, analysis_path=None, selection_info=None):
        """Crée le rapport unifié HTML avec support du mode harmonisé"""
        try:
            ensure_folders_exist()
            
            # Déterminer le chemin d'analyse
            if analysis_path:
                # Mode harmonisé : utiliser le chemin fourni
                report_analysis_path = analysis_path
            elif hasattr(self, 'original_analysis_path') and self.original_analysis_path:
                # Mode traditionnel : utiliser le chemin original
                report_analysis_path = self.original_analysis_path
            else:
                # Fallback : essayer de déduire depuis les fichiers analysés
                if self.results_by_file:
                    first_file = list(self.results_by_file.keys())[0]
                    report_analysis_path = _find_project_root(first_file)
                else:
                    report_analysis_path = "."  # Dernière option
            
            # Préparer les données pour le générateur HTML
            results_data = {
                'stats': {
                    'files_analyzed': self.files_analyzed,
                    'total_issues': self.total_issues,
                    'execution_time': execution_time,
                    'issues_by_type': self._calculate_issues_by_type()
                },
                'results_by_file': self.results_by_file
            }
            
            # 🆕 AJOUT : Inclure selection_info si disponible
            if selection_info:
                results_data['selection_info'] = selection_info
                log_message("DEBUG", f"🎯 selection_info ajouté au rapport: {selection_info}", category="report")
            
            # Générer le rapport HTML
            rapport_path = create_html_coherence_report(
                results_data, 
                report_analysis_path, 
                self._format_execution_time(execution_time)
            )
            
            if rapport_path:
                log_message("INFO", f"Rapport de cohérence HTML créé : {rapport_path}", category="report")
                
                # Auto-ouverture selon la configuration
                if config_manager.is_coherence_auto_open_report_enabled():
                    self._auto_open_report(rapport_path)
            else:
                log_message("INFO", "Aucun rapport généré - aucune erreur détectée", category="report")
            
            return rapport_path
            
        except Exception as e:
            log_message("ERREUR", f"Impossible de créer le rapport de cohérence HTML : {e}", category="report")
            return None

    def _format_execution_time(self, execution_time):
        """Formate le temps d'exécution en format lisible"""
        if execution_time < 60:
            return f"{execution_time:.1f}s"
        else:
            minutes = int(execution_time // 60)
            seconds = int(execution_time % 60)
            return f"{minutes}m {seconds}s"
    
    def _get_issue_type_name(self, issue_type):
        """Retourne le nom lisible d'un type de problème"""
        type_names = {
            "VARIABLE_MISMATCH": "Variables [] incohérentes",
            "TAG_MISMATCH": "Balises {} incohérentes",
            "PLACEHOLDER_MISMATCH": "Placeholders () incohérents",
            "UNRESTORED_PLACEHOLDER": "Placeholders non restaurés",
            "MALFORMED_PLACEHOLDER": "Placeholder malformé",
            "SPECIAL_CODE_MISMATCH": "Codes spéciaux incohérents",
            "PARENTHESES_MISMATCH": "Parenthèses incohérentes",
            "FRENCH_QUOTES_MISMATCH": "Guillemets français incohérents",
            "QUOTE_COUNT_MISMATCH": "Nombre de guillemets différent",
            "UNTRANSLATED_LINE": "Ligne potentiellement non traduite",
            "MISSING_OLD": "Ligne ANCIENNE manquante",
            "CONTENT_PREFIX_MISMATCH": "Préfixe de contenu incohérent",
            "CONTENT_SUFFIX_MISMATCH": "Suffixe de contenu incohérent",
            "FILE_ERROR": "Erreur de fichier",
            "ANALYSIS_ERROR": "Erreur d'analyse",
            "LENGTH_DISCREPANCY": "Différence de longueur",
            # Nouveaux types fusionnés
            "QUOTES_MISMATCH": "Guillemets incohérents",
            "PERCENTAGE_MISMATCH": "Pourcentages incohérents"
        }
        return type_names.get(issue_type, issue_type)
    
    def _auto_open_report(self, rapport_path):
        """Ouvre automatiquement le rapport selon la configuration"""
        try:
            # 🆕 Vérifier la configuration avant d'ouvrir
            if not config_manager.is_coherence_auto_open_report_enabled():
                log_message("DEBUG", "Ouverture automatique du rapport désactivée", category="report_autoopen")
                return
            
            import subprocess
            import platform
            
            if platform.system() == "Windows":
                os.startfile(rapport_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", rapport_path])
            else:  # Linux
                subprocess.run(["xdg-open", rapport_path])
                
        
        except Exception as e:
            log_message("ATTENTION", f"Impossible d'ouvrir automatiquement le rapport : {e}", category="report_autoopen")

# =====================================================================
# FONCTIONS D'INTERFACE PUBLIQUES
# =====================================================================
def check_coherence_unified(target_path, return_details=False, selection_info=None):
    """
    Lance la vérification de cohérence harmonisée - VERSION COMPATIBLE
    
    Args:
        target_path: Chemin vers le fichier ou dossier à analyser
        return_details: Si True, retourne les détails complets
        selection_info: NOUVEAU - Informations sur la sélection (optionnel)
        
    Returns:
        Résultats de l'analyse avec infos de sélection intégrées
    """
    try:
        from datetime import datetime
        
        start_time = datetime.now()
        
        # Log de début avec infos harmonisées
        if selection_info:
            if selection_info.get('is_all_files', True):
                mode_desc = f"dossier {selection_info.get('language', 'unknown')} complet"
            else:
                mode_desc = f"fichier {selection_info.get('selected_option', 'inconnu')}"
        else:
            log_message("INFO", f"🔍 Début vérification cohérence - {target_path}")
        
        # UTILISER VOTRE CLASSE EXISTANTE
        checker = UnifiedCoherenceChecker()
        
        # 🆕 Déterminer le chemin du projet pour les exclusions
        if selection_info and selection_info.get('project_path'):
            checker.project_path = selection_info['project_path']
        else:
            checker.project_path = _find_project_root(target_path)
        
        # Déterminer les fichiers à analyser selon la sélection
        if selection_info and selection_info.get('file_paths'):
            # Mode harmonisé : récupérer tous les fichiers .rpy du dossier (même les techniques)
            if selection_info.get('is_all_files', True):
                # Pour l'analyse de tous les fichiers, récupérer directement tous les .rpy du dossier
                files_to_analyze = checker._find_rpy_files(target_path)
            else:
                # Pour l'analyse de fichiers spécifiques, utiliser la liste fournie
                files_to_analyze = selection_info['file_paths']
                log_message("DEBUG", f"Mode fichiers spécifiques : {len(files_to_analyze)} fichiers sélectionnés", category="coherence_analysis")
            
            # Analyser les fichiers spécifiques avec votre logique existante
            checker.results_by_file = {}
            checker.total_issues = 0
            checker.files_analyzed = 0
            excluded_files = []
            
            for file_path in files_to_analyze:
                if checker._should_exclude_file(file_path):
                    excluded_files.append(os.path.basename(file_path))
                    continue
                    
                file_results = checker._analyze_single_file(file_path)  # VOTRE MÉTHODE EXISTANTE
                if file_results['issues']:
                    checker.results_by_file[file_path] = file_results
                    checker.total_issues += len(file_results['issues'])
                
                checker.files_analyzed += 1
            
            # Log des fichiers exclus sur une seule ligne
            if excluded_files:
                log_message("DEBUG", f"Fichiers système exclus automatiquement: {', '.join(excluded_files)}", category="file_exclusion")
            
            # Générer le rapport avec vos méthodes existantes
            execution_time = (datetime.now() - start_time).total_seconds()
            rapport_path = checker._create_unified_report(execution_time, target_path, selection_info)
            
        else:
            # Mode traditionnel : utiliser votre méthode existante telle quelle
            result = checker.analyze_path(target_path, return_details)
            if not return_details:
                return result
            
            # Convertir le format pour compatibilité
            rapport_path = result.get('rapport_path') if isinstance(result, dict) else result
            execution_time = result.get('stats', {}).get('execution_time', 0) if isinstance(result, dict) else 0
        
        # Construire les résultats harmonisés
        # Créer la liste des fichiers avec erreurs une seule fois
        files_with_issues_paths = [path for path, result in checker.results_by_file.items() if result.get('issues')]

        results = {
            'stats': {
                'files_analyzed': checker.files_analyzed,
                'total_issues': checker.total_issues,
                'issues_by_type': checker._calculate_issues_by_type(),
                # La clé contient maintenant une liste, ce qui corrige l'erreur `len(int)`
                'files_with_issues': files_with_issues_paths,
                # Le code d'affichage peut faire `len(stats['files_with_issues'])` pour avoir le nombre
                'files_clean': checker.files_analyzed - len(files_with_issues_paths)
            },
            'results_by_file': checker.results_by_file,
            'execution_time': execution_time,
            'rapport_path': rapport_path
        }        
        # NOUVEAU : Intégrer les infos de sélection dans les résultats
        if selection_info:
            results['selection_info'] = selection_info.copy()
        
        # Log de fin
        total_issues = results['stats']['total_issues']
        files_analyzed = results['stats']['files_analyzed']
        
        if selection_info:
            pass  # Pas de log pour le mode harmonisé
        else:
            log_message("INFO", f"✅ Vérification cohérence terminée - {files_analyzed} fichier(s), {total_issues} problème(s)")
        
        return results if return_details else results.get('rapport_path')
        
    except Exception as e:
        log_message("ERREUR", f"Erreur critique vérification cohérence harmonisée: {e}")
        return _create_empty_results_compatible(str(e), selection_info) if return_details else None

def _create_empty_results_compatible(error_message, selection_info=None):
    """Crée une structure de résultats vide en cas d'erreur - VERSION COMPATIBLE"""
    results = {
        'stats': {
            'files_analyzed': 0,
            'total_issues': 0,
            'issues_by_type': {},
            'files_with_issues': [],   # ← était 0, doit être une liste
            'files_clean': 0
        },
        'results_by_file': {},
        'execution_time': 0,
        'rapport_path': None,
        'error': error_message
    }
    
    if selection_info:
        results['selection_info'] = selection_info.copy()
    
    return results

# def check_coherence_unified(path, return_details=False):
#     """
#     Fonction principale unifiée pour vérifier la cohérence
    
#     Args:
#         path (str): Chemin du fichier .rpy ou dossier tl
#         return_details (bool): Si True, retourne les détails pour l'interface
        
#     Returns:
#         str ou dict: Chemin du rapport ou détails selon return_details
#     """
#     checker = UnifiedCoherenceChecker()
#     return checker.analyze_path(path, return_details)

def get_coherence_options():
    """Retourne les options actuelles de cohérence"""
    return {
        'check_variables': config_manager.get('coherence_check_variables', True),
        'check_tags': config_manager.get('coherence_check_tags', True),
        'check_special_codes': config_manager.get('coherence_check_special_codes', True),
        'check_untranslated': config_manager.get('coherence_check_untranslated', True),
        'check_ellipsis': config_manager.get('coherence_check_ellipsis', True),
        'check_escape_sequences': config_manager.get('coherence_check_escape_sequences', True),
        'check_percentages': config_manager.get('coherence_check_percentages', True),
        'check_quotations': config_manager.get('coherence_check_quotations', True),
        'check_parentheses': config_manager.get('coherence_check_parentheses', True),
        'check_syntax': config_manager.get('coherence_check_syntax', True),
        'check_deepl_ellipsis': config_manager.get('coherence_check_deepl_ellipsis', True),
        'check_isolated_percent': config_manager.get('coherence_check_isolated_percent', True),
        'check_french_quotes': config_manager.get('coherence_check_french_quotes', True),
        'check_line_structure': config_manager.get('coherence_check_line_structure', True),
        'custom_exclusions': config_manager.get('coherence_custom_exclusions', {}),  # 🆕 Dictionnaire (projet → exclusions)
        'auto_open_report': config_manager.is_coherence_auto_open_report_enabled()
    }

def set_coherence_options(options):
    """
    Sauvegarde les options de cohérence.
    
    NOTE: coherence_custom_exclusions n'est PLUS sauvegardée ici.
    Elle est gérée exclusivement via l'API HTTP du rapport interactif.
    """
    config_manager.set('coherence_check_variables', options.get('check_variables', True))
    config_manager.set('coherence_check_tags', options.get('check_tags', True))
    config_manager.set('coherence_check_special_codes', options.get('check_special_codes', True))
    config_manager.set('coherence_check_untranslated', options.get('check_untranslated', True))
    config_manager.set('coherence_check_ellipsis', options.get('check_ellipsis', True))
    config_manager.set('coherence_check_escape_sequences', options.get('check_escape_sequences', True))
    config_manager.set('coherence_check_percentages', options.get('check_percentages', True))
    config_manager.set('coherence_check_quotations', options.get('check_quotations', True))
    config_manager.set('coherence_check_parentheses', options.get('check_parentheses', True))
    config_manager.set('coherence_check_syntax', options.get('check_syntax', True))
    config_manager.set('coherence_check_deepl_ellipsis', options.get('check_deepl_ellipsis', True))
    config_manager.set('coherence_check_isolated_percent', options.get('check_isolated_percent', True))
    config_manager.set('coherence_check_french_quotes', options.get('check_french_quotes', True))
    config_manager.set('coherence_check_line_structure', options.get('check_line_structure', True))
    # 🆕 NE PLUS sauvegarder coherence_custom_exclusions ici
    # Elle est gérée exclusivement via add_coherence_exclusion() et remove_coherence_exclusion()
    
    # Sauvegarder l'option d'ouverture automatique
    if 'auto_open_report' in options:
        config_manager.set_coherence_auto_open_report(options['auto_open_report'])

def add_custom_exclusion(project_path, file_path, line, text):
    """
    Ajoute une exclusion précise (projet+fichier+ligne).
    🆕 Nouvelle version avec contrôle précis.
    """
    return config_manager.add_coherence_exclusion(project_path, file_path, line, text)

def remove_custom_exclusion(project_path, file_path, line, text):
    """
    Supprime une exclusion précise.
    🆕 Nouvelle version avec contrôle précis.
    """
    return config_manager.remove_coherence_exclusion(project_path, file_path, line, text)

def _find_project_root(target_path):
    """Trouve la racine du projet Ren'Py depuis un chemin"""
    try:
        if os.path.isfile(target_path):
            current_path = os.path.dirname(target_path)
        else:
            current_path = target_path
        
        # Remonter jusqu'à trouver un dossier "game" ou "tl"
        while current_path and current_path != os.path.dirname(current_path):
            if os.path.basename(current_path) == 'tl':
                # On est dans tl/langue, remonter de 2 niveaux
                return os.path.dirname(os.path.dirname(current_path))
            elif os.path.basename(current_path) == 'game':
                # On est dans game, remonter de 1 niveau
                return os.path.dirname(current_path)
            elif os.path.exists(os.path.join(current_path, 'game')):
                # On est à la racine du projet
                return current_path
            
            current_path = os.path.dirname(current_path)
        
        return target_path  # Fallback
        
    except Exception:
        return target_path

# Export des fonctions principales
__all__ = [
    'UnifiedCoherenceChecker',
    'check_coherence_unified',
    'get_coherence_options',
    'set_coherence_options',
    'add_custom_exclusion',
    'remove_custom_exclusion'
]
