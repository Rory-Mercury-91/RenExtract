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
import webbrowser
from urllib.parse import quote
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
        
        # === CONTRÔLES STRUCTURELS (critiques) ===
        self.check_variables = config_manager.get('coherence_check_variables', True)              # Variables [] incohérentes
        self.check_tags = config_manager.get('coherence_check_tags', True)                        # Balises {} incohérentes
        self.check_tags_content = config_manager.get('coherence_check_tags_content', True)        # Contenu balises non traduit ({b}text{/b})
        self.check_escape_sequences = config_manager.get('coherence_check_escape_sequences', True)  # Séquences d'échappement (\n, \t, \r, \\)
        self.check_line_structure = config_manager.get('coherence_check_line_structure', True)    # Structure des lignes old/new
        
        # === CONTRÔLES DE TRADUCTION ===
        self.check_untranslated = config_manager.get('coherence_check_untranslated', True)        # Lignes potentiellement non traduites
        # Seuil de similarité (0-100) : alerter si au moins X % de la ligne (en mots) est inchangé (défaut 80)
        self.untranslated_threshold_percent = max(50, min(100, config_manager.get('coherence_untranslated_threshold_percent', 80)))
        
        # === CONTRÔLES DE FORMATAGE ===
        self.check_ellipsis = config_manager.get('coherence_check_ellipsis', True)                # Ellipses (-- → ...)
        self.check_percentages = config_manager.get('coherence_check_percentages', True)          # Variables de formatage (%s, %d, %%)
        self.check_quotations = config_manager.get('coherence_check_quotations', True)            # Guillemets et échappements (" \")
        self.check_parentheses = config_manager.get('coherence_check_parentheses', True)          # Parenthèses et crochets ()
        self.check_syntax = config_manager.get('coherence_check_syntax', True)                    # Syntaxe Ren'Py et structure
        
        # === CONTRÔLES SPÉCIFIQUES ===
        self.check_deepl_ellipsis = config_manager.get('coherence_check_deepl_ellipsis', True)    # Ellipses DeepL ([...] → ...)
        self.check_isolated_percent = config_manager.get('coherence_check_isolated_percent', True)  # Pourcentages isolés (% → %%)
        
        # === AVERTISSEMENTS INDICATIFS ===
        self.check_length_difference = config_manager.get('coherence_check_length_difference', True)  # Différence de longueur importante
        # ⭐ Placeholders TOUJOURS actifs (contrôle obligatoire, non configurable)
        
        # Exclusions de fichiers depuis la config
        self.excluded_files = config_manager.get('coherence_excluded_files')
        
        log_message("DEBUG", f"Options cohérence: variables={self.check_variables}, tags={self.check_tags}, untranslated={self.check_untranslated}, ellipsis={self.check_ellipsis}, escape={self.check_escape_sequences}, percent={self.check_percentages}, quotes={self.check_quotations}, parens={self.check_parentheses}, syntax={self.check_syntax}, deepl={self.check_deepl_ellipsis}, isolated={self.check_isolated_percent}, length={self.check_length_difference}, structure={self.check_line_structure}", category="coherence_options")
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
        
        # 🆕 Vérifier si cette ligne est exclue (par projet + fichier + ligne + texte)
        if self._is_excluded_line(file_path, new_line_num, old_text):
            return issues  # Ligne exclue, ignorer toutes les vérifications
        
        # 1. Vérifier les lignes non traduites (si activé) - PRIORITÉ MAXIMALE
        is_untranslated, percent_unchanged = self._is_untranslated_line(old_text, new_text, file_path, new_line_num)
        if self.check_untranslated and is_untranslated:
            if percent_unchanged is not None:
                desc = f"Ligne partiellement non traduite ({percent_unchanged} % du contenu inchangé)"
            else:
                desc = "Ligne potentiellement non traduite (contenu identique)"
            issues.append({
                'line': new_line_num,
                'type': 'UNTRANSLATED_LINE',
                'description': desc,
                'old_content': old_text,
                'new_content': new_text
            })
            return issues  # Arrêt immédiat si non traduit
        
        # 2. Vérifier les balises {} (si activé) - PRIORITÉ HAUTE
        if self.check_tags:
            tag_issues = self._check_tags_coherence(old_text, new_text, old_line_num, new_line_num)
            if tag_issues:
                return tag_issues  # Arrêt dès qu'on trouve une erreur de balise
        
        # 2bis. Vérifier la traduction du contenu entre balises (si activé)
        if self.check_tags_content:
            tag_content_issues = self._check_tags_content_translation(old_text, new_text, old_line_num, new_line_num)
            if tag_content_issues:
                return tag_content_issues  # Arrêt dès qu'on trouve du contenu non traduit
        
        # 3. Vérifier les variables [] (si activé) - PRIORITÉ HAUTE
        if self.check_variables:
            var_issues = self._check_variables_coherence(old_text, new_text, old_line_num, new_line_num)
            if var_issues:
                return var_issues  # Arrêt dès qu'on trouve une erreur de variable
        
        # 4. Vérifier les séquences d'échappement (si activé) - PRIORITÉ MOYENNE
        if self.check_escape_sequences:
            escape_issues = self._check_escape_sequences_coherence(old_text, new_text, old_line_num, new_line_num)
            if escape_issues:
                return escape_issues
        
        # 5. ⭐ Vérifier les placeholders (OBLIGATOIRE - NON CONFIGURABLE) - PRIORITÉ HAUTE
        placeholder_issues = self._check_placeholders_coherence(old_text, new_text, old_line_num, new_line_num)
        if placeholder_issues:
            return placeholder_issues
        
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
        
        # 12. Vérifier la structure des lignes (si activé) - PRIORITÉ TRÈS BASSE
        if self.check_line_structure:
            structure_issues = self._check_line_structure_coherence(old_text, new_text, old_line_num, new_line_num)
            if structure_issues:
                return structure_issues
        
        # 13. Vérifier la différence de longueur (si activé) - PRIORITÉ INDICATIVE
        if self.check_length_difference:
            length_issues = self._check_length_difference_coherence(old_text, new_text, old_line_num, new_line_num)
            if length_issues:
                return length_issues
        
        return issues  # Aucune erreur trouvée
    
    def _is_excluded_line(self, file_path, line_num, old_text):
        """
        Vérifie si une ligne est exclue de manière PRÉCISE (projet + fichier + ligne + texte).
        
        Cette vérification GLOBALE est appelée AVANT tous les contrôles.
        Les exclusions ajoutées depuis n'importe quel rapport (reconstruction OU maintenance)
        sont prises en compte ici de manière unifiée.
        
        Args:
            file_path: Chemin complet du fichier
            line_num: Numéro de ligne
            old_text: Texte original (OLD)
        
        Returns:
            True si la ligne est exclue, False sinon
        """
        if not old_text or not old_text.strip():
            return False
        
        text = old_text.strip()
        
        # Charger les exclusions pour ce projet
        if not self.project_path:
            return False
        
        exclusions = config_manager.get_coherence_exclusions(self.project_path)
        if not exclusions:
            return False
        
        # Extraire le nom relatif du fichier (normalisé)
        file_relative = self._get_relative_file_path(file_path)
        
        # Vérifier si cette ligne exacte est exclue
        for excl in exclusions:
            excl_file = excl.get('file', '')
            excl_line = excl.get('line', 0)
            excl_text = excl.get('text', '').strip()
            
            # Vérification PRÉCISE : fichier + ligne + texte
            if (excl_line == line_num and 
                excl_text == text and 
                file_relative.endswith(excl_file)):
                log_message("DEBUG", f"Ligne exclue (globale) : {file_relative}:{line_num}", category="coherence")
                return True  # Ligne exclue
        
        return False  # Pas exclue
    
    def _is_untranslated_line(self, old_text, new_text, file_path, line_num):
        """
        Vérifie si une ligne est probablement non traduite (exactement ou partiellement).
        
        Retourne (is_untranslated: bool, percent_unchanged: int|None).
        - Si contenu identique : (True, None) après auto-exclusions.
        - Si contenu différent mais ratio de mots inchangés >= seuil : (True, percent).
        - Sinon : (False, None).
        
        Le seuil est configurable via coherence_untranslated_threshold_percent (ex. 80 = alerter si ≥80 % des mots inchangés).
        """
        old_stripped = old_text.strip()
        new_stripped = new_text.strip()
        text = old_stripped
        
        # Auto-exclusions (patterns techniques : ellipsis, variables, balises seules, etc.)
        if self._is_auto_excluded(text):
            return (False, None)
        
        # Cas 1 : contenu exactement identique
        if old_stripped == new_stripped:
            if len(text) <= 3 or len(text.split()) <= 1:
                return (False, None)
            return (True, None)
        
        # Cas 2 : contenu différent — calcul du pourcentage de mots inchangés (même position)
        old_words = old_stripped.split()
        new_words = new_stripped.split()
        if len(old_words) < 2:
            return (False, None)
        matches = sum(1 for i in range(min(len(old_words), len(new_words))) if old_words[i] == new_words[i])
        percent_unchanged = round(100 * matches / len(old_words)) if old_words else 0
        threshold = self.untranslated_threshold_percent
        if percent_unchanged >= threshold:
            return (True, percent_unchanged)
        return (False, None)
    
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
    
    def _check_tags_content_translation(self, old_text, new_text, old_line_num, new_line_num):
        """
        Vérifie si le contenu entre les balises Ren'Py a bien été traduit.
        
        Exemple:
        OLD: {b}you{/b} are welcome
        NEW: {b}you{/b} êtes les bienvenus  ❌ "you" n'a pas été traduit
        NEW: {b}vous{/b} êtes les bienvenus  ✅ "you" → "vous"
        """
        issues = []
        
        try:
            # Pattern pour extraire les paires de balises avec leur contenu
            # Format: {tag}contenu{/tag}
            tag_pattern = r'\{([a-zA-Z_][a-zA-Z0-9_]*)[^}]*\}(.*?)\{/\1\}'
            
            old_contents = {}  # {tag: [contenus]}
            new_contents = {}  # {tag: [contenus]}
            
            # Extraire tous les contenus entre balises dans OLD
            for match in re.finditer(tag_pattern, old_text):
                tag_name = match.group(1)
                content = match.group(2).strip()
                if content:  # Ignorer les contenus vides
                    if tag_name not in old_contents:
                        old_contents[tag_name] = []
                    old_contents[tag_name].append(content)
            
            # Extraire tous les contenus entre balises dans NEW
            for match in re.finditer(tag_pattern, new_text):
                tag_name = match.group(1)
                content = match.group(2).strip()
                if content:  # Ignorer les contenus vides
                    if tag_name not in new_contents:
                        new_contents[tag_name] = []
                    new_contents[tag_name].append(content)
            
            # Comparer les contenus pour chaque type de balise
            for tag_name in old_contents:
                if tag_name not in new_contents:
                    continue  # Balise absente, sera détecté par _check_tags_coherence
                
                old_tag_contents = old_contents[tag_name]
                new_tag_contents = new_contents[tag_name]
                
                # Comparer chaque occurrence
                for i, old_content in enumerate(old_tag_contents):
                    if i >= len(new_tag_contents):
                        break  # Plus de contenus correspondants dans NEW
                    
                    new_content = new_tag_contents[i]
                    
                    # Vérifier si le contenu est identique (pas traduit)
                    # Ignorer la casse et les espaces pour la comparaison
                    if old_content.lower().strip() == new_content.lower().strip():
                        # Vérifier que ce n'est pas un mot identique en anglais/français
                        # (ex: "ok", "menu", "stop", etc.)
                        common_words = {'ok', 'menu', 'stop', 'start', 'pause', 'no', 'yes', 
                                      'save', 'load', 'auto', 'skip', 'quit', 'back', 'roll'}
                        
                        if old_content.lower().strip() not in common_words:
                            issues.append({
                                'line': new_line_num,
                                'type': 'TAG_CONTENT_UNTRANSLATED',
                                'description': f"Contenu de balise non traduit => {{{tag_name}}} : \"{old_content}\" → \"{new_content}\"",
                                'old_content': old_text,
                                'new_content': new_text
                            })
            
        except Exception as e:
            # Ne pas faire échouer l'analyse entière pour cette vérification
            log_message("DEBUG", f"Erreur vérification contenu balises ligne {new_line_num}: {e}", category="coherence")
            pass
        
        return issues
    
    def _check_placeholders_coherence(self, old_text, new_text, old_line_num, new_line_num):
        """
        Vérifie que les placeholders de protection sont correctement restaurés.
        
        LOGIQUE OBLIGATOIRE (non configurable):
        - Erreur si placeholder détecté dans NEW (peu importe OLD)
        - Les placeholders doivent DISPARAÎTRE après traduction/reconstruction
        - Formats détectés: RENPY_CODE_*, RENPY_ASTERIX_*, RENPY_TILDE_*, RENPY_EMPTY
        
        Types d'erreurs:
        1. Placeholder dans OLD mais supprimé pendant traduction → Erreur
        2. Placeholder dans NEW uniquement (ajouté) → Erreur  
        3. Placeholder dans OLD ET NEW (non restauré) → Erreur
        """
        issues = []
        
        try:
            # Détecter tous les placeholders RENPY dans OLD et NEW
            old_placeholders = re.findall(r'RENPY_[A-Z_]+_?\d*', old_text)
            new_placeholders = re.findall(r'RENPY_[A-Z_]+_?\d*', new_text)
            
            # CAS 1 : Placeholder dans OLD mais pas dans NEW
            # (Supprimé pendant traduction - erreur critique)
            old_set = set(old_placeholders)
            new_set = set(new_placeholders)
            removed_placeholders = old_set - new_set
            
            if removed_placeholders:
                issues.append({
                    'line': new_line_num,
                    'type': 'PLACEHOLDER_REMOVED',
                    'description': f"Placeholder(s) supprimé(s) pendant traduction (critique) : {', '.join(sorted(removed_placeholders))}",
                    'old_content': old_text,
                    'new_content': new_text
                })
                return issues  # Erreur critique, arrêt immédiat
            
            # CAS 2 & 3 : Placeholder dans NEW (ajouté OU non restauré)
            # Dans tous les cas c'est une erreur
            if new_placeholders:
                # Déterminer si c'est un ajout ou une non-restauration
                if old_placeholders:
                    # Placeholders présents dans OLD et NEW = non restauré
                    description = f"Placeholder(s) non restauré(s) après reconstruction : {', '.join(sorted(new_set))}"
                else:
                    # Placeholders seulement dans NEW = ajouté par erreur
                    description = f"Placeholder(s) ajouté(s) par erreur : {', '.join(sorted(new_set))}"
                
                issues.append({
                    'line': new_line_num,
                    'type': 'UNRESTORED_PLACEHOLDER',
                    'description': description,
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
            def count_isolated_percents(text):
                """Compte les pourcentages isolés en excluant les variables Ren'Py %(lettres)s et les %% échappés"""
                # 1. Remplacer toutes les variables Ren'Py %(nom)s, %(nom)d, etc. par un placeholder
                # Pattern: %(lettres ou chiffres ou underscore)lettre (s, d, i, f, etc.)
                text_no_vars = re.sub(r'%\([a-zA-Z0-9_]+\)[a-zA-Z]', '__RENPY_VAR__', text)
                
                # 2. Remplacer tous les %% échappés par un placeholder
                text_no_escaped = text_no_vars.replace('%%', '__DOUBLE_PERCENT__')
                
                # 3. Compter les % restants (pourcentages isolés)
                isolated_count = text_no_escaped.count('%')
                
                return isolated_count
            
            # Compter les pourcentages isolés (hors variables Ren'Py et %% échappés)
            old_isolated = count_isolated_percents(old_text)
            new_isolated = count_isolated_percents(new_text)
            
            # Double % échappé
            old_double_percent = old_text.count('%%')
            new_double_percent = new_text.count('%%')
            
            # Fusionner les vérifications
            isolated_mismatch = old_isolated != new_isolated
            double_mismatch = old_double_percent != new_double_percent
            
            if isolated_mismatch or double_mismatch:
                # Construire une description détaillée
                details = []
                if isolated_mismatch:
                    details.append(f"Variables % (Attendu: {old_isolated}, Présent: {new_isolated})")
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
        """
        Vérifie la cohérence du NOMBRE TOTAL de guillemets (tous types confondus).
        
        Types de guillemets comptés :
        - Guillemets droits : " (échappés \" et non échappés)
        - Guillemets simples : ' (sauf élisions françaises : l', d', c', etc.)
        - Guillemets français : « »
        - Guillemets typographiques anglais : " " (curly quotes)
        - Apostrophes typographiques : ' (curly apostrophe)
        - Chevrons ASCII : << >>
        
        Accepte les substitutions de style (ex: 'simple' → \"échappé\" ou → « français »).
        """
        issues = []
        
        try:
            # Compter TOUS les types de guillemets dans OLD
            old_total = 0
            old_total += old_text.count('\\"')  # Guillemets échappés \"
            old_total += len(re.findall(r'(?<!\\)"', old_text))  # Guillemets droits non échappés "
            # Guillemets simples ' : TOUS sauf élisions françaises (lettre'lettre comme c'est, l'eau)
            # Compte 'texte' mais ignore c'est, l'eau, d'accord
            old_single_quotes = old_text.count("'")
            # Soustraire les élisions (lettre ' lettre)
            old_elisions = len(re.findall(r"[a-zA-ZÀ-ÿ]'[a-zA-ZÀ-ÿ]", old_text))
            old_total += (old_single_quotes - old_elisions)
            old_total += old_text.count('«')  # Guillemets français (chevrons) ouvrants «
            old_total += old_text.count('»')  # Guillemets français (chevrons) fermants »
            old_total += old_text.count('"')  # Guillemets typographiques anglais ouvrants " (curly quotes)
            old_total += old_text.count('"')  # Guillemets typographiques anglais fermants " (curly quotes)
            old_total += old_text.count(''')  # Apostrophes typographiques ' (curly apostrophe)
            old_total += len(re.findall(r'(?<![<>])<<(?![<>])', old_text))  # Chevrons ASCII ouvrants <<
            old_total += len(re.findall(r'(?<![<>])>>(?![<>])', old_text))  # Chevrons ASCII fermants >>
            
            # Compter TOUS les types de guillemets dans NEW
            new_total = 0
            new_total += new_text.count('\\"')  # Guillemets échappés \"
            new_total += len(re.findall(r'(?<!\\)"', new_text))  # Guillemets droits non échappés "
            # Guillemets simples ' : TOUS sauf élisions françaises (lettre'lettre comme c'est, l'eau)
            # Compte 'texte' mais ignore c'est, l'eau, d'accord
            new_single_quotes = new_text.count("'")
            # Soustraire les élisions (lettre ' lettre)
            new_elisions = len(re.findall(r"[a-zA-ZÀ-ÿ]'[a-zA-ZÀ-ÿ]", new_text))
            new_total += (new_single_quotes - new_elisions)
            new_total += new_text.count('«')  # Guillemets français (chevrons) ouvrants «
            new_total += new_text.count('»')  # Guillemets français (chevrons) fermants »
            new_total += new_text.count('"')  # Guillemets typographiques anglais ouvrants " (curly quotes)
            new_total += new_text.count('"')  # Guillemets typographiques anglais fermants " (curly quotes)
            new_total += new_text.count(''')  # Apostrophes typographiques ' (curly apostrophe)
            new_total += len(re.findall(r'(?<![<>])<<(?![<>])', new_text))  # Chevrons ASCII ouvrants <<
            new_total += len(re.findall(r'(?<![<>])>>(?![<>])', new_text))  # Chevrons ASCII fermants >>
            
            # Vérifier que le nombre TOTAL de guillemets est cohérent
            if old_total != new_total:
                issues.append({
                    'line': new_line_num,
                    'type': 'QUOTES_MISMATCH',
                    'description': f"Nombre de guillemets incohérent => Attendu: {old_total}, Présent: {new_total}",
                    'old_content': old_text,
                    'new_content': new_text
                })
        
        except Exception:
            pass
        
        return issues
    
    def _check_parentheses_coherence(self, old_text, new_text, old_line_num, new_line_num):
        """
        Vérifie la cohérence des parenthèses () UNIQUEMENT (1 seule erreur fusionnée).
        
        Note : Les crochets [] et accolades {} sont déjà vérifiés par :
        - check_variables (pour [variable])
        - check_tags (pour {balise})
        """
        issues = []
        
        try:
            # Vérifier SEULEMENT les parenthèses ()
            old_open_parens = old_text.count('(')
            new_open_parens = new_text.count('(')
            old_close_parens = old_text.count(')')
            new_close_parens = new_text.count(')')
            
            # Fusionner les vérifications en 1 seule erreur
            open_mismatch = old_open_parens != new_open_parens
            close_mismatch = old_close_parens != new_close_parens
            
            if open_mismatch or close_mismatch:
                # Construire une description détaillée
                details = []
                if open_mismatch:
                    details.append(f"Ouvrantes ( (Attendu: {old_open_parens}, Présent: {new_open_parens})")
                if close_mismatch:
                    details.append(f"Fermantes ) (Attendu: {old_close_parens}, Présent: {new_close_parens})")
                
                issues.append({
                    'line': new_line_num,
                    'type': 'PARENTHESES_MISMATCH',
                    'description': f"Parenthèses () incohérentes => {', '.join(details)}",
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
    
    
    def _check_length_difference_coherence(self, old_text, new_text, old_line_num, new_line_num):
        """
        Vérifie la différence de longueur entre OLD et NEW (indicatif, non critique).
        
        Signale si la traduction est significativement plus courte ou plus longue que l'original.
        Seuil : 250% de différence de longueur (ratio > 2.5).
        """
        issues = []
        
        try:
            old_length = len(old_text.strip())
            new_length = len(new_text.strip())
            
            # Ignorer les lignes OLD trop courtes (moins de 10 caractères)
            if old_length < 10:
                return issues
            
            # Calculer le ratio de différence
            if old_length > 0 and new_length > 0:
                length_ratio = max(old_length, new_length) / min(old_length, new_length)
                
                # Seuil : 250% de différence (ratio > 2.5)
                if length_ratio > 2.5:
                    length_diff_percent = abs((new_length - old_length) / old_length) * 100
                    
                    if new_length > old_length:
                        status = f"⬆️ +{length_diff_percent:.0f}% plus longue"
                    else:
                        status = f"⬇️ -{length_diff_percent:.0f}% plus courte"
                    
                    issues.append({
                        'line': new_line_num,
                        'type': 'LENGTH_DIFFERENCE_WARNING',
                        'description': f"Différence de longueur importante {status} => ANCIEN: {old_length} caractères, NOUVEAU: {new_length} caractères (ratio: {length_ratio:.1f})",
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
            "TAG_CONTENT_UNTRANSLATED": "Contenu de balise non traduit",
            "PLACEHOLDER_MISMATCH": "Placeholders () incohérents",
            "UNRESTORED_PLACEHOLDER": "Placeholders non restaurés",
            "MALFORMED_PLACEHOLDER": "Placeholder malformé",
            "SPECIAL_CODE_MISMATCH": "Codes spéciaux incohérents",
            "PARENTHESES_MISMATCH": "Parenthèses incohérentes",
            "QUOTE_COUNT_MISMATCH": "Nombre de guillemets différent",
            "UNTRANSLATED_LINE": "Ligne potentiellement non traduite",
            "MISSING_OLD": "Ligne ANCIENNE manquante",
            "CONTENT_PREFIX_MISMATCH": "Préfixe de contenu incohérent",
            "CONTENT_SUFFIX_MISMATCH": "Suffixe de contenu incohérent",
            "FILE_ERROR": "Erreur de fichier",
            "ANALYSIS_ERROR": "Erreur d'analyse",
            # Nouveaux types fusionnés
            "QUOTES_MISMATCH": "Guillemets incohérents",
            "PERCENTAGE_MISMATCH": "Pourcentages incohérents",
            # Avertissements indicatifs
            "LENGTH_DIFFERENCE_WARNING": "Différence de longueur importante"
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
            
            # Essayer d'abord via le serveur local sur localhost
            server_host = config_manager.get('editor_server_host', '127.0.0.1') or '127.0.0.1'
            try:
                server_port = int(config_manager.get('editor_server_port', 8765))
            except Exception:
                server_port = 8765
            
            browser_host = '127.0.0.1' if server_host in ('0.0.0.0', '::') else server_host
            report_param = quote(os.path.abspath(rapport_path), safe='')
            report_url = f"http://{browser_host}:{server_port}/coherence/report?path={report_param}"
            
            log_message("DEBUG", f"Ouverture rapport via serveur local: {report_url}", category="report_autoopen")
            opened_via_server = False
            try:
                opened_via_server = webbrowser.open(report_url)
            except Exception as e:
                log_message("ATTENTION", f"Ouverture via serveur local impossible: {e}", category="report_autoopen")
                opened_via_server = False
            
            if opened_via_server:
                return
            
            # Fallback: ouverture directe du fichier
            log_message("ATTENTION", "Fallback ouverture rapport via fichier local", category="report_autoopen")
            if platform.system() == "Windows":
                os.startfile(rapport_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", rapport_path], check=False)
            else:  # Linux
                subprocess.run(["xdg-open", rapport_path], check=False)
            
        
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
        'check_line_structure': config_manager.get('coherence_check_line_structure', True),
        'untranslated_threshold_percent': config_manager.get('coherence_untranslated_threshold_percent', 80),
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
    config_manager.set('coherence_untranslated_threshold_percent', max(50, min(100, options.get('untranslated_threshold_percent', 80))))
    config_manager.set('coherence_check_ellipsis', options.get('check_ellipsis', True))
    config_manager.set('coherence_check_escape_sequences', options.get('check_escape_sequences', True))
    config_manager.set('coherence_check_percentages', options.get('check_percentages', True))
    config_manager.set('coherence_check_quotations', options.get('check_quotations', True))
    config_manager.set('coherence_check_parentheses', options.get('check_parentheses', True))
    config_manager.set('coherence_check_syntax', options.get('check_syntax', True))
    config_manager.set('coherence_check_deepl_ellipsis', options.get('check_deepl_ellipsis', True))
    config_manager.set('coherence_check_isolated_percent', options.get('check_isolated_percent', True))
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
