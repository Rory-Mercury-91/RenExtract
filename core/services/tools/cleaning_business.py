# core/business/tools/cleaning_business.py
# Logique métier pour le nettoyage des lignes orphelines - RenExtract 

"""
Logique métier de suppression des lignes orphelines

Ce module contient la logique pure de nettoyage des fichiers de traduction :
- Détection automatique des lignes orphelines
- Sauvegarde de sécurité avant suppression
- Rapport détaillé des suppressions
- Validation avant suppression

Utilise les modules tools pour SDK et Python.
"""

import os
import re
import tempfile
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from infrastructure.logging.logging import log_message
from infrastructure.config.constants import FOLDERS, ensure_folders_exist
from infrastructure.helpers.unified_functions import get_last_game_directory, set_last_game_directory
from core.models.backup.unified_backup_manager import UnifiedBackupManager, BackupType
from core.tools.sdk_manager import get_sdk_manager
from core.tools.python_manager import get_python_manager

class UnifiedCleaner:
    """
    Classe unifiée pour nettoyer les traductions avec les deux méthodes :
    1. Nettoyage basé sur lint.txt (IDs orphelins)
    2. Nettoyage basé sur correspondance de chaînes
    AVEC UN SEUL BACKUP PAR FICHIER
    """

    def __init__(self):
        """Initialise le nettoyeur unifié"""
        self.backup_suffix = ".backup_unified_cleanup"
        self.cleaned_files = []
        self.total_orphan_blocks = 0
        self.total_files_processed = 0
        self.backed_up_files = {}  # Cache des fichiers déjà sauvegardés
        
        # Cache pour optimiser les recherches de chaînes
        self.game_files_cache = {}  # Cache des fichiers game/
        self.string_search_cache = {}  # Cache des résultats de recherche
        self.last_game_folder_path = None  # Pour détecter les changements de projet

    def generate_lint_file(self, renpy_sdk_path: str, project_path: str) -> Optional[str]:
        """
        Génère le fichier lint.txt en utilisant le SDK
        
        Args:
            renpy_sdk_path: Chemin vers le SDK Ren'Py
            project_path: Chemin vers le projet
            
        Returns:
            Chemin vers lint.txt généré ou None
        """
        try:
            sdk_manager = get_sdk_manager()
            
            # Valider le SDK fourni
            if not sdk_manager.validate_sdk_path(renpy_sdk_path):
                log_message("ERREUR", f"SDK fourni invalide : {renpy_sdk_path}", category="renpy_generator_clean_tl")
                return None
            
            # Obtenir l'exécutable Ren'Py
            renpy_exe = sdk_manager.get_renpy_executable(renpy_sdk_path)
            if not renpy_exe:
                log_message("ERREUR", f"Exécutable Ren'Py introuvable dans le SDK", category="renpy_generator_clean_tl")
                return None
            
            return self._generate_lint_with_executable(renpy_exe, project_path)
            
        except Exception as e:
            log_message("ERREUR", f"Erreur génération lint : {e}", category="renpy_generator_clean_tl")
            return self._create_minimal_lint(project_path)

    def _generate_lint_with_executable(self, renpy_exe: str, project_path: str) -> Optional[str]:
        """Génère le lint avec un exécutable spécifique"""
        try:
            # Valider le projet
            game_folder = os.path.join(project_path, "game")
            if not os.path.exists(game_folder):
                log_message("ERREUR", f"Dossier 'game' manquant : {game_folder}", category="renpy_generator_clean_tl")
                return self._create_minimal_lint(project_path)
            
            
            
            # Nettoyer les fichiers problématiques avant génération
            self._clean_problematic_files(project_path)
            
            # ✅ NOUVEAU : Supprimer traceback.txt s'il existe
            traceback_path = os.path.join(project_path, "traceback.txt")
            if os.path.exists(traceback_path):
                try:
                    os.remove(traceback_path)
                except Exception as e:
                    log_message("ATTENTION", f"Impossible de supprimer traceback.txt : {e}", category="renpy_generator_clean_tl")
            
            # Fichiers log possibles contenant le lint
            possible_log_files = [
                os.path.join(project_path, "log.txt"),
                os.path.join(project_path, "renpy.log"),
                os.path.join(project_path, "lint.txt"),
                os.path.join(game_folder, "log.txt"),
                os.path.join(game_folder, "renpy.log")
            ]
            
            # Nettoyer les anciens fichiers
            for log_file in possible_log_files:
                if os.path.exists(log_file) and "lint" in os.path.basename(log_file).lower():
                    try:
                        os.remove(log_file)
                    except:
                        pass
            
            # Commandes à essayer
            commands_to_try = [
                [renpy_exe, project_path, "lint"],
                [renpy_exe, ".", "lint"]
            ]
            
            # Environnement
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            
            import subprocess
            
            for cmd_index, cmd in enumerate(commands_to_try, 1):
                log_message("INFO", f"Tentative {cmd_index}/{len(commands_to_try)}", category="renpy_generator_clean_tl")
                
                try:
                    work_dir = project_path if cmd_index == 2 else os.path.dirname(renpy_exe)
                    
                    # ✅ NOUVEAU : Lancer Ren'Py en arrière-plan pour surveiller traceback.txt
                    import threading
                    import time
                    
                    traceback_detected = False
                    
                    def monitor_traceback():
                        nonlocal traceback_detected
                        while True:
                            if os.path.exists(traceback_path):
                                traceback_detected = True
                                log_message("ERREUR", f"traceback.txt détecté pendant l'exécution Ren'Py", category="renpy_generator_clean_tl")
                                break
                            time.sleep(0.5)  # Vérifier toutes les 500ms
                    
                    # Démarrer la surveillance
                    monitor_thread = threading.Thread(target=monitor_traceback, daemon=True)
                    monitor_thread.start()
                    
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        cwd=work_dir,
                        timeout=180,
                        env=env
                    )
                    
                    # Log du résultat de la commande
                    # ✅ Vérifier si traceback.txt a été généré pendant l'exécution
                    if traceback_detected or os.path.exists(traceback_path):
                        log_message("ERREUR", f"traceback.txt détecté - Erreur Ren'Py lors de la génération lint", category="renpy_generator_clean_tl")
                        log_message("ERREUR", f"Le nettoyage est annulé pour éviter des suppressions incorrectes", category="renpy_generator_clean_tl")
                        return None
                    
                    # Chercher le lint dans les fichiers log
                    for log_file in possible_log_files:
                        if os.path.exists(log_file):
                            file_size = os.path.getsize(log_file)
                            if file_size > 0:
                                try:
                                    with open(log_file, 'r', encoding='utf-8') as f:
                                        content = f.read()
                                    
                                    if any(pattern in content for pattern in ['Orphan Translations:', 'lint.txt', 'Statistics:']):
                                        target_lint_path = os.path.join(project_path, "lint.txt")
                                        
                                        if "lint.txt" in os.path.basename(log_file):
                                            import shutil
                                            shutil.copy2(log_file, target_lint_path)
                                        else:
                                            with open(target_lint_path, 'w', encoding='utf-8') as f:
                                                f.write(content)
                                        
                                        
                                        self._validate_and_convert_lint(target_lint_path)
                                        return target_lint_path
                                        
                                except Exception:
                                    continue
                    
                except subprocess.TimeoutExpired:
                    log_message("ATTENTION", f"Tentative {cmd_index} : Timeout", category="renpy_generator_clean_tl")
                    continue
                except Exception as e:
                    log_message("ERREUR", f"Tentative {cmd_index} échouée : {e}", category="renpy_generator_clean_tl")
                    continue
            
            # Si toutes les tentatives échouent
            log_message("ERREUR", "Toutes les tentatives de génération lint ont échoué", category="renpy_generator_clean_tl")
            return self._create_minimal_lint(project_path)
            
        except Exception as e:
            log_message("ERREUR", f"Erreur génération lint : {e}", category="renpy_generator_clean_tl")
            return self._create_minimal_lint(project_path)

    def _clean_problematic_files(self, project_path: str):
        """Nettoie les fichiers problématiques qui empêchent la génération du lint"""
        try:
                        
            game_folder = os.path.join(project_path, "game")
            tl_folder = os.path.join(game_folder, "tl")
            
            if not os.path.exists(tl_folder):
                return
            
            files_removed = 0
            problematic_patterns = [
                "clipboard_*.rpy",
                "temp_*.rpy", 
                "tmp_*.rpy",
                "*_backup.rpy"
            ]
            
            import glob
            
            for lang_folder in os.listdir(tl_folder):
                lang_path = os.path.join(tl_folder, lang_folder)
                if os.path.isdir(lang_path):
                    for pattern in problematic_patterns:
                        search_pattern = os.path.join(lang_path, pattern)
                        for file_path in glob.glob(search_pattern):
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                
                                if (len(content.strip()) == 0 or
                                    'old "' in content and 'new "' not in content or
                                    content.count('old "') != content.count('new "') or
                                    'translate' not in content):
                                    
                                    backup_path = file_path + f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                                    import shutil
                                    shutil.copy2(file_path, backup_path)
                                    os.remove(file_path)
                                    files_removed += 1

                            except Exception:
                                continue
            
            if files_removed > 0:
                log_message("INFO", f"{files_removed} fichier(s) problématique(s) nettoyé(s)", category="renpy_generator_clean_tl")
                
        except Exception as e:
            # Sévérité ajustée : le nettoyage préliminaire qui échoue doit être visible
            log_message("ATTENTION", f"Erreur nettoyage fichiers problématiques : {e}", category="renpy_generator_clean_tl")

    def _validate_and_convert_lint(self, lint_file_path: str):
        """Valide et convertit le fichier lint en UTF-8 si nécessaire"""
        try:
            with open(lint_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            encodings = ['cp1252', 'latin1', 'iso-8859-1']
            for encoding in encodings:
                try:
                    with open(lint_file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    
                    with open(lint_file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    break
                except UnicodeDecodeError:
                    continue

    def _create_minimal_lint(self, project_path: str) -> Optional[str]:
        """Crée un fichier lint minimal en analysant les traductions"""
        try:
            lint_file_path = os.path.join(project_path, "lint.txt")
            
            log_message("INFO", "Analyse des traductions pour lint intelligent...", category="renpy_generator_clean_tl")
            
            tl_folder = os.path.join(project_path, "game", "tl")
            game_folder = os.path.join(project_path, "game")
            
            orphan_candidates = []
            total_translations = 0
            
            if os.path.exists(tl_folder):
                for lang_folder in os.listdir(tl_folder):
                    lang_path = os.path.join(tl_folder, lang_folder)
                    if os.path.isdir(lang_path) and lang_folder.lower() != 'none':
                        
                        for root, dirs, files in os.walk(lang_path):
                            for file in files:
                                if file.endswith('.rpy'):
                                    file_path = os.path.join(root, file)
                                    
                                    try:
                                        with open(file_path, 'r', encoding='utf-8') as f:
                                            content = f.read()
                                        
                                        translate_pattern = r'translate\s+\w+\s+(\w+):'
                                        matches = re.findall(translate_pattern, content)
                                        total_translations += len(matches)
                                        
                                        old_pattern = r'old\s+"([^"]*)"'
                                        old_texts = re.findall(old_pattern, content)
                                        
                                        for old_text in old_texts:
                                            if old_text and len(old_text.strip()) > 0:
                                                if not self._quick_search_in_game(old_text, game_folder):
                                                    escaped_text = re.escape(old_text)
                                                    id_pattern = r'translate\s+\w+\s+(\w+):[^}]*?old\s+"' + escaped_text + r'"'
                                                    id_match = re.search(id_pattern, content, re.DOTALL)
                                                    if id_match:
                                                        orphan_id = id_match.group(1)
                                                        if orphan_id not in orphan_candidates:
                                                            orphan_candidates.append(orphan_id)
                                        
                                    except Exception:
                                        continue
            
            # Créer le contenu du lint
            lint_content = f"""# Fichier lint généré automatiquement - RenExtract
# Projet : {os.path.basename(project_path)}
# Généré le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Lint Status: Generated automatically due to Ren'Py SDK execution failure
Analysis completed successfully.

"""
            
            if orphan_candidates:
                lint_content += f"""Orphan Translations:
    
"""
                for i, orphan_id in enumerate(orphan_candidates[:20], 1):
                    lint_content += f"* line {i} of translation {orphan_id} (id {orphan_id}) is an orphan (missing from the original files)\n"
                
                lint_content += f"""
Total orphans detected: {len(orphan_candidates)}
"""
            else:
                lint_content += """Orphan Translations:
    
    No orphan translations detected.
    
"""
            
            lint_content += f"""
Statistics:
    The project contains {total_translations} translation blocks analyzed.
    Automatic analysis completed with {len(orphan_candidates)} potential orphans found.
    
    Note: This lint file was generated automatically due to Ren'Py SDK execution issues.
    Some orphan detections may be false positives. Manual verification recommended.
"""
            
            with open(lint_file_path, 'w', encoding='utf-8') as f:
                f.write(lint_content)
            
            log_message("INFO", f"Lint intelligent créé : {len(orphan_candidates)} orphelins potentiels détectés", category="renpy_generator_clean_tl")
            
            return lint_file_path
            
        except Exception as e:
            log_message("ERREUR", f"Erreur création lint intelligent : {e}", category="renpy_generator_clean_tl")
            
            # Fallback vers un lint très basique
            try:
                lint_file_path = os.path.join(project_path, "lint.txt")
                basic_content = f"""# Fichier lint basique - RenExtract
# Généré le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Lint Status: Basic lint file due to generation errors
No orphan analysis available.

Orphan Translations:
    
    No orphan translations detected (basic mode).

Statistics:
    Basic lint file generated.
    Manual review recommended.
"""
                
                with open(lint_file_path, 'w', encoding='utf-8') as f:
                    f.write(basic_content)
                
                log_message("INFO", f"Lint basique créé : {lint_file_path}", category="renpy_generator_clean_tl")
                return lint_file_path
                
            except Exception as e2:
                log_message("ERREUR", f"Erreur création lint basique : {e2}", category="renpy_generator_clean_tl")
                return None

    def _quick_search_in_game(self, search_text: str, game_folder_path: str) -> bool:
        """Recherche rapide d'une chaîne dans le dossier game"""
        try:
            for root, dirs, files in os.walk(game_folder_path):
                if 'tl' in dirs:
                    dirs.remove('tl')
                
                for file in files:
                    if file.endswith('.rpy'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            if f'"{search_text}"' in content or f"'{search_text}'" in content:
                                return True
                                
                        except Exception:
                            continue
            
            return False
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur lors de la recherche de '{search_text}' : {e}", category="renpy_generator_clean_tl")
            return True  # En cas d'erreur, considérer comme trouvé pour éviter les faux positifs

    def scan_translation_folders(self, tl_folder_path: str) -> List[str]:
        """
        Scanne le dossier tl et retourne la liste des dossiers de langue
        
        Args:
            tl_folder_path: Chemin vers le dossier tl racine
            
        Returns:
            Liste des noms de dossiers de langue trouvés
        """
        language_folders = []
        
        try:
            if not os.path.exists(tl_folder_path):
                log_message("ERREUR", f"Dossier tl non trouvé : {tl_folder_path}", category="renpy_generator_clean_tl")
                return []
            
            for item in os.listdir(tl_folder_path):
                item_path = os.path.join(tl_folder_path, item)
                
                if os.path.isdir(item_path):
                    if item.lower() != 'none':
                        has_rpy_files = any(f.endswith('.rpy') for f in os.listdir(item_path) 
                                          if os.path.isfile(os.path.join(item_path, f)))
                        
                        if has_rpy_files:
                            language_folders.append(item)
            
            log_message("INFO", f"Dossiers de langue trouvés : {language_folders}", category="renpy_generator_clean_tl")
            return sorted(language_folders)
            
        except Exception as e:
            log_message("ERREUR", f"Erreur lors du scan des dossiers de langue : {e}", category="renpy_generator_clean_tl")
            return []

    def unified_clean(self, lint_file_path: str, game_folder_path: str, tl_folder_path: str, 
                     selected_languages: List[str]) -> Dict[str, any]:
        """
        Nettoyage unifié avec UN SEUL BACKUP par fichier
        
        Args:
            lint_file_path: Chemin vers le fichier lint.txt
            game_folder_path: Chemin vers le dossier game
            tl_folder_path: Chemin vers le dossier tl racine
            selected_languages: Liste des langues sélectionnées à traiter
            
        Returns:
            Dict avec les résultats consolidés du nettoyage
        """
        # Réinitialiser le cache des backups pour chaque nettoyage
        self.backed_up_files.clear()
        
        # Sauvegarder le dossier utilisé
        set_last_game_directory(game_folder_path)
        
        results = {
            'success': True,
            'total_languages_processed': 0,
            'total_files_processed': 0,
            'total_orphan_blocks_removed': 0,
            'errors': [],
            'language_results': {},
            'summary': {
                'lint_cleanup': {'files': 0, 'blocks_removed': 0},
                'string_cleanup': {'files': 0, 'blocks_removed': 0}
            }
        }
        
        try:
            
            
            for language in selected_languages:
                language_folder = os.path.join(tl_folder_path, language)
                
                if not os.path.exists(language_folder):
                    error_msg = f"Dossier de langue introuvable : {language_folder}"
                    log_message("ERREUR", error_msg, category="renpy_generator_clean_tl")
                    results['errors'].append(error_msg)
                    continue
                
                log_message("INFO", f"Traitement de la langue : {language}", category="renpy_generator_clean_tl")
                
                # Résultats pour cette langue
                lang_result = {
                    'language': language,
                    'success': True,
                    'lint_cleanup': None,
                    'string_cleanup': None,
                    'total_blocks_removed': 0,
                    'files_processed': 0,
                    'file_results': []
                }
                
                try:
                    # Nettoyer le dossier de langue avec backup unifié
                    cleanup_result = self._clean_language_folder_unified(language_folder, lint_file_path, game_folder_path)
                    
                    # Convertir le résultat au format attendu
                    lang_result['lint_cleanup'] = {
                        'success': cleanup_result['success'],
                        'files_cleaned': cleanup_result['files_cleaned'],
                        'total_orphan_blocks_removed': cleanup_result['lint_blocks_removed']
                    }
                    
                    lang_result['string_cleanup'] = {
                        'success': cleanup_result['success'],
                        'files_cleaned': cleanup_result['files_cleaned'],
                        'total_orphan_blocks_removed': cleanup_result['string_blocks_removed']
                    }
                    
                    lang_result['orphan_comments_cleanup'] = {
                        'success': cleanup_result['success'],
                        'files_cleaned': cleanup_result['files_cleaned'],
                        'total_orphan_blocks_removed': cleanup_result.get('orphan_comments_removed', 0)
                    }
                    
                    lang_result['file_results'] = cleanup_result['file_results']

                    if cleanup_result['success']:
                        results['summary']['lint_cleanup']['files'] += cleanup_result['files_cleaned']
                        results['summary']['lint_cleanup']['blocks_removed'] += cleanup_result['lint_blocks_removed']
                        results['summary']['string_cleanup']['files'] += cleanup_result['files_cleaned']
                        results['summary']['string_cleanup']['blocks_removed'] += cleanup_result['string_blocks_removed']
                        
                        orphan_comments_count = cleanup_result.get('orphan_comments_removed', 0)
                        log_message("INFO", f"[{language}] Terminé : {cleanup_result['files_cleaned']} fichiers, "
                                  f"{cleanup_result['lint_blocks_removed']} blocs lint + {cleanup_result['string_blocks_removed']} blocs string + {orphan_comments_count} commentaires orphelins = "
                                  f"{cleanup_result['total_orphan_blocks_removed']} éléments total supprimés", category="renpy_generator_clean_tl")
                    
                    # Calculer les totaux pour cette langue
                    lang_result['total_blocks_removed'] = cleanup_result['total_orphan_blocks_removed']
                    lang_result['files_processed'] = cleanup_result['files_processed']
                    
                    results['total_languages_processed'] += 1
                    results['total_files_processed'] += lang_result['files_processed']
                    results['total_orphan_blocks_removed'] += lang_result['total_blocks_removed']
                    
                except Exception as e:
                    error_msg = f"Erreur lors du traitement de la langue '{language}': {str(e)}"
                    log_message("ERREUR", f"{error_msg} | {e}", category="renpy_generator_clean_tl")
                    lang_result['success'] = False
                    lang_result['error'] = error_msg
                    results['errors'].append(error_msg)
                
                results['language_results'][language] = lang_result
            
            # Nettoyer le cache pour libérer la mémoire
            self._clear_cache()
            
            # Rapport final
            log_message("INFO", f"Nettoyage unifié terminé : {results['total_languages_processed']} langues, "
                      f"{results['total_files_processed']} fichiers, {results['total_orphan_blocks_removed']} blocs supprimés", category="renpy_generator_clean_tl")
            log_message("INFO", f"Nombre de backups créés : {len(self.backed_up_files)}", category="renpy_generator_clean_tl")
            
            return results
            
        except Exception as e:
            # Nettoyer le cache même en cas d'erreur
            self._clear_cache()
            
            error_msg = f"Erreur générale lors du nettoyage unifié : {str(e)}"
            log_message("ERREUR", f"{error_msg} | {e}", category="renpy_generator_clean_tl")
            results['success'] = False
            results['errors'].append(error_msg)
            return results

    def _clean_language_folder_unified(self, language_folder: str, lint_file_path: str, game_folder_path: str) -> Dict[str, any]:
        """Nettoie tous les fichiers d'un dossier de langue avec un seul backup par fichier"""
        results = {
            'success': True,
            'files_processed': 0,
            'files_cleaned': 0,
            'total_orphan_blocks_removed': 0,
            'lint_blocks_removed': 0,
            'string_blocks_removed': 0,
            'errors': [],
            'file_results': []
        }
        
        try:
            # Récupérer les fichiers à exclure de la configuration
            excluded_files = self._get_excluded_files()
            
            for root, dirs, files in os.walk(language_folder):
                for file in files:
                    if file.endswith('.rpy'):
                        # Vérifier si le fichier doit être exclu
                        if self._should_exclude_file(file, excluded_files):
                                                        continue
                        
                        file_path = os.path.join(root, file)
                        result = self._clean_file_unified(file_path, lint_file_path, game_folder_path)
                        
                        results['files_processed'] += 1
                        results['file_results'].append(result)
                        
                        if result['success']:
                            results['files_cleaned'] += 1
                            results['total_orphan_blocks_removed'] += result['total_blocks_removed']
                            results['lint_blocks_removed'] += result.get('lint_blocks_removed', 0)
                            results['string_blocks_removed'] += result.get('string_blocks_removed', 0)
                        else:
                            results['errors'].append(result['error'])
            
            return results
            
        except Exception as e:
            log_message("ERREUR", f"Erreur lors du nettoyage du dossier {language_folder} : {e}", category="renpy_generator_clean_tl")
            results['success'] = False
            results['errors'].append(str(e))
            return results

    def _get_excluded_files(self) -> List[str]:
        """Récupère la liste des fichiers à exclure depuis la configuration"""
        try:
            from infrastructure.config.config import config_manager
            
            excluded_files_str = config_manager.get('cleanup_excluded_files')
            
            excluded_files = []
            if excluded_files_str:
                for file_name in excluded_files_str.split(','):
                    cleaned_name = file_name.strip()
                    if cleaned_name:
                        excluded_files.append(cleaned_name)
            
                        return excluded_files
            
        except Exception as e:
                        return []

    def _should_exclude_file(self, file_name: str, excluded_files: List[str]) -> bool:
        """Vérifie si un fichier doit être exclu du nettoyage"""
        try:
            # ✅ EXCLUSION AUTOMATIQUE : Fichiers générés par le système
            system_generated_files = [
                '99_Z_Console.rpy',
                '99_Z_ScreenPreferences.rpy', 
                '99_Z_FontSystem.rpy',
                'common.rpy'
            ]
            
            # Vérifier d'abord les fichiers système
            file_name_lower = file_name.lower()
            for system_file in system_generated_files:
                if system_file.lower() == file_name_lower:
                                        return True
            
            # Ensuite vérifier les exclusions utilisateur
            if file_name in excluded_files:
                return True
            
            # Vérification insensible à la casse pour les exclusions utilisateur
            for excluded_file in excluded_files:
                if excluded_file.lower() == file_name_lower:
                    return True
            
            return False
            
        except Exception as e:
                        return False

    def _create_unified_backup(self, file_path: str) -> Optional[str]:
        """Crée une sauvegarde unifiée du fichier avant tout traitement"""
        # Vérifier si ce fichier a déjà été sauvegardé
        if file_path in self.backed_up_files:
                        return self.backed_up_files[file_path]
        
        try:
            # Utiliser le gestionnaire unifié
            manager = UnifiedBackupManager()
            result = manager.create_backup(
                file_path, 
                BackupType.CLEANUP, 
                "Sauvegarde avant nettoyage automatique"
            )
            
            if result['success']:
                # Enregistrer le backup créé
                self.backed_up_files[file_path] = result['backup_path']
                return result['backup_path']
            else:
                log_message("ATTENTION", f"Échec backup unifié: {result['error']}", category="renpy_generator_clean_tl")
                return None
                
        except Exception as e:
            log_message("ERREUR", f"Erreur backup unifié pour {file_path} : {e}", category="renpy_generator_clean_tl")
            return None

    def _clean_file_unified(self, file_path: str, lint_file_path: str, game_folder_path: str) -> Dict[str, any]:
        """
        Nettoie un fichier avec les deux méthodes en créant un seul backup
        VERSION CORRIGÉE - Sans modification des chemins comme dans le système de cohérence
        
        Args:
            file_path: Chemin du fichier à nettoyer (utilisé tel quel)
            lint_file_path: Chemin vers lint.txt
            game_folder_path: Chemin vers le dossier game
            
        Returns:
            Dict avec les résultats consolidés du nettoyage
        """
        try:
            # Utiliser le chemin tel quel - PAS de normalisation
            if not os.path.exists(file_path):
                return {
                    'success': False,
                    'error': f'Fichier non trouvé : {file_path}',
                    'lint_blocks_removed': 0,
                    'string_blocks_removed': 0,
                    'total_blocks_removed': 0,
                    'file_path': file_path  # Chemin original inchangé
                }
            
            # Créer un seul backup au début
            backup_path = self._create_unified_backup(file_path)
            
            # Lire le fichier original
            with open(file_path, 'r', encoding='utf-8') as f:
                original_lines = f.readlines()
            
            current_lines = original_lines.copy()
            total_blocks_removed = 0
            lint_blocks_removed = 0
            string_blocks_removed = 0
            
            # Étape 1: Nettoyage basé sur lint.txt
            if os.path.exists(lint_file_path):
                try:
                    orphan_ids = self._parse_lint_file(lint_file_path)
                    if orphan_ids:
                        current_lines, removed_blocks = self._clean_blocks_with_lint(current_lines, orphan_ids)
                        lint_blocks_removed = len(removed_blocks)
                        total_blocks_removed += lint_blocks_removed
                except Exception as e:
                    log_message("ATTENTION", f"Erreur lors du nettoyage lint de {file_path} : {e}", category="renpy_generator_clean_tl")
            
            # Étape 2: Nettoyage basé sur les chaînes
            string_blocks_details = []
            try:
                current_lines, removed_blocks_details = self._clean_blocks_by_strings(current_lines, game_folder_path)
                string_blocks_removed = len(removed_blocks_details)
                string_blocks_details = removed_blocks_details
                total_blocks_removed += string_blocks_removed
            except Exception as e:
                log_message("ATTENTION", f"Erreur lors du nettoyage par chaînes de {file_path} : {e}", category="renpy_generator_clean_tl")
            
            # Étape 3: Nettoyage des blocs vides
            empty_blocks_removed = 0
            try:
                # Compter les blocs avant nettoyage
                blocks_before = len([line for line in current_lines if line.strip().startswith('translate ')])
                
                # Nettoyer les blocs translate strings vides
                current_lines = self._fix_empty_translate_blocks(current_lines)
                
                # Nettoyer les blocs translate ID vides
                current_lines = self._fix_empty_translate_id_blocks(current_lines)
                
                # Compter les blocs après nettoyage
                blocks_after = len([line for line in current_lines if line.strip().startswith('translate ')])
                empty_blocks_removed = blocks_before - blocks_after
                
                if empty_blocks_removed > 0:
                    total_blocks_removed += empty_blocks_removed
                
            except Exception as e:
                log_message("ATTENTION", f"Erreur lors du nettoyage des blocs vides de {file_path} : {e}", category="renpy_generator_clean_tl")
            
            # Étape 4: Nettoyage des commentaires orphelins
            orphan_comments_removed = 0
            try:
                lines_before = len(current_lines)
                current_lines = self._clean_orphan_comments_and_spacing(current_lines)
                lines_after = len(current_lines)
                orphan_comments_removed = lines_before - lines_after
                
                if orphan_comments_removed > 0:
                    log_message("INFO", f"Supprimé {orphan_comments_removed} commentaires orphelins dans {os.path.basename(file_path)}", category="renpy_generator_clean_tl")
                    
            except Exception as e:
                log_message("ATTENTION", f"Erreur lors du nettoyage des commentaires orphelins de {file_path} : {e}", category="renpy_generator_clean_tl")
            
            # Mettre à jour le total avec les commentaires orphelins
            total_blocks_removed += orphan_comments_removed
            
            # Écrire le fichier final nettoyé
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(current_lines)
            
            return {
                'success': True,
                'file_path': file_path,  # IMPORTANT: Chemin original préservé
                'backup_path': backup_path,
                'original_lines': len(original_lines),
                'cleaned_lines': len(current_lines),
                'lint_blocks_removed': lint_blocks_removed,
                'string_blocks_removed': string_blocks_removed,
                'empty_blocks_removed': empty_blocks_removed,
                'orphan_comments_removed': orphan_comments_removed,
                'string_blocks_details': string_blocks_details,
                'total_blocks_removed': total_blocks_removed,
                'backup_created': backup_path is not None
            }
        except Exception as e:
            log_message("ERREUR", f"Erreur lors du nettoyage unifié de {file_path} : {e}", category="renpy_generator_clean_tl")
            return {
                'success': False,
                'error': str(e),
                'file_path': file_path,  # Chemin original même en cas d'erreur
                'total_blocks_removed': 0
            }

    # ===== MÉTHODES POUR LE NETTOYAGE LINT =====
    
    def _parse_lint_file(self, lint_file_path: str) -> List[str]:
        """Parse le fichier lint.txt et extrait les IDs orphelins"""
        orphan_ids = []
        
        try:
            with open(lint_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Chercher la section "Orphan Translations:"
            lines = content.split('\n')
            in_orphan_section = False
            
            for line in lines:
                line = line.strip()
                
                # Détecter le début de la section orphelins
                if 'Orphan Translations:' in line:
                    in_orphan_section = True
                    continue
                
                # Si on est dans la section orphelins
                if in_orphan_section:
                    # Chercher les lignes avec des IDs orphelins
                    if line.startswith('* line') and '(id ' in line:
                        match = re.search(r'\(id\s+(\w+)\)', line)
                        if match:
                            orphan_id = match.group(1)
                            orphan_ids.append(orphan_id)
                                                
                    # Fin de la section orphelins
                    elif line and not line.startswith('*') and not line.startswith('game/'):
                        if any(keyword in line for keyword in ['Statistics:', 'Lint is not', 'The game contains']):
                            break
            
            # log_message("INFO", f"Total d'IDs orphelins extraits du lint.txt : {len(orphan_ids)}", category="renpy_generator_clean_tl")  # Désactivé pour éviter la répétition
            return orphan_ids
            
        except Exception as e:
            log_message("ERREUR", f"Erreur lors du parsing du lint.txt : {e}", category="renpy_generator_clean_tl")
            return []
    
    def _clean_blocks_with_lint(self, lines: List[str], orphan_ids: List[str]) -> Tuple[List[str], List[Dict]]:
        """Nettoie les blocs basés sur les IDs du lint.txt"""
        if not orphan_ids:
            return lines, []
        
        # Détecter tous les blocs translate
        blocks = self._detect_translate_blocks_for_lint(lines)
                
        # Séparer les blocs à supprimer et à conserver
        blocks_to_remove = []
        blocks_to_keep = []
        
        for block in blocks:
            if block['id'] in orphan_ids:
                blocks_to_remove.append(block)
            else:
                blocks_to_keep.append(block)
                        
        
        # Reconstruire le fichier avec les blocs conservés
        cleaned_lines = []
        
        # Créer un set des indices de lignes qui appartiennent aux blocs translate
        translate_line_indices = set()
        for block in blocks:
            translate_line_indices.update(block['line_indices'])
        
        # Créer un set des indices de lignes des blocs à supprimer
        remove_line_indices = set()
        for block in blocks_to_remove:
            remove_line_indices.update(block['line_indices'])
        
        # Reconstruire ligne par ligne
        for i, line in enumerate(lines):
            if i in translate_line_indices:
                # Cette ligne appartient à un bloc translate
                if i not in remove_line_indices:
                    # Bloc à conserver
                    cleaned_lines.append(line)
                # Sinon, bloc à supprimer, on ne l'ajoute pas
            else:
                # Ligne qui n'appartient à aucun bloc translate, on la garde
                cleaned_lines.append(line)
        
        return cleaned_lines, blocks_to_remove
    
    def _detect_translate_blocks_for_lint(self, lines: List[str]) -> List[Dict]:
        """Détecte tous les blocs translate dans le fichier"""
        blocks = []
        current_block = None
        
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            
            # Détecter le début d'un bloc translate
            if self._is_block_start(stripped_line):
                # Finir le bloc précédent s'il existe
                if current_block:
                    blocks.append(current_block)
                
                # Commencer un nouveau bloc
                block_id = self._extract_block_id(stripped_line)
                current_block = {
                    'start_line': i + 1,
                    'translate_line': line,
                    'id': block_id,
                    'lines': [line],
                    'line_indices': [i],
                    'reference_line': None
                }
            else:
                # Ajouter la ligne au bloc courant s'il existe
                if current_block:
                    current_block['lines'].append(line)
                    current_block['line_indices'].append(i)
                    
                    # Détecter la ligne de référence
                    if stripped_line.startswith('# game/') and current_block['reference_line'] is None:
                        current_block['reference_line'] = line
        
        # Ajouter le dernier bloc
        if current_block:
            blocks.append(current_block)
        
        return blocks
    
    def _is_block_start(self, line: str) -> bool:
        """Vérifie si une ligne est le début d'un bloc translate"""
        return re.match(r'^translate\s+\w+\s+\w+:', line) is not None
    
    def _extract_block_id(self, line: str) -> str:
        """Extrait l'ID d'un bloc translate"""
        match = re.match(r'^translate\s+\w+\s+(\w+):', line)
        return match.group(1) if match else ""
    
    # ===== MÉTHODES POUR LE NETTOYAGE PAR CHAÎNES =====
    
    def _clean_blocks_by_strings(self, lines: List[str], game_folder_path: str) -> Tuple[List[str], List[Dict]]:
        """Nettoie les blocs en vérifiant la correspondance des chaînes - VERSION CORRIGÉE"""
        log_message("INFO", f"🔍 Début nettoyage par chaînes - {len(lines)} lignes à analyser", category="renpy_generator_clean_tl")
        
        # ✅ NOUVELLE APPROCHE : Parcourir ligne par ligne au lieu d'utiliser _detect_translation_blocks
        cleaned_lines = []
        removed_blocks_details = []
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Si c'est une ligne old, analyser le bloc complet
            if line.startswith('old '):
                # Extraire le texte entre guillemets
                old_text = self._extract_text_from_quotes(line)
                
                if old_text:
                    # Vérifier si le texte existe dans le jeu
                    exists_in_game = self._string_exists_in_game(old_text, game_folder_path)
                    
                    if exists_in_game:
                        # ✅ CONSERVER le bloc complet (old + new + commentaire si présent)
                                                
                        # Ajouter le commentaire précédent s'il existe et n'a pas déjà été ajouté
                        if (i > 0 and 
                            lines[i-1].strip().startswith('# game/') and 
                            (not cleaned_lines or cleaned_lines[-1].strip() != lines[i-1].strip())):
                            cleaned_lines.append(lines[i-1])
                        
                        # Ajouter la ligne old
                        cleaned_lines.append(lines[i])
                        
                        # Ajouter la ligne new suivante si elle existe
                        if i + 1 < len(lines) and lines[i+1].strip().startswith('new '):
                            cleaned_lines.append(lines[i+1])
                            i += 2  # Passer old et new
                        else:
                            i += 1  # Passer seulement old
                    else:
                        # ❌ SUPPRIMER le bloc (texte introuvable dans le jeu)
                                                
                        # Enregistrer les détails du bloc supprimé
                        new_text = ""
                        if i + 1 < len(lines) and lines[i+1].strip().startswith('new '):
                            new_text = self._extract_text_from_quotes(lines[i+1].strip())
                            i += 2  # Passer old et new
                        else:
                            i += 1  # Passer seulement old
                        
                        removed_blocks_details.append({
                            'old_text': old_text,
                            'new_text': new_text,
                            'line_number': i,
                            'block_lines': [lines[i-1] if i > 0 and lines[i-1].strip().startswith('# game/') else '', lines[i-1], lines[i] if i < len(lines) else '']
                        })
                else:
                    # Pas de texte extrait, conserver la ligne
                    cleaned_lines.append(lines[i])
                    i += 1
            else:
                # Ligne normale, la conserver
                cleaned_lines.append(lines[i])
                i += 1
        
        log_message("INFO", f"📊 Nettoyage terminé: {len(cleaned_lines)} lignes conservées, {len(removed_blocks_details)} blocs supprimés", category="renpy_generator_clean_tl")
        
        return cleaned_lines, removed_blocks_details
    
    def _extract_text_from_quotes(self, line: str) -> str:
        """Extrait le texte entre guillemets d'une ligne old/new"""
        import re
        
        # Chercher le texte entre guillemets doubles
        match = re.search(r'"([^"\\]*(?:\\.[^"\\]*)*)"', line)
        if match:
            return match.group(1)
        
        # Chercher le texte entre guillemets simples
        match = re.search(r"'([^'\\]*(?:\\.[^'\\]*)*)'", line)
        if match:
            return match.group(1)
        
        return ""
    
    def _detect_translation_blocks(self, lines: List[str]) -> List[Dict]:
        """Détecte tous les blocs de traduction (commentaire + old + new)"""
        blocks = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            if self._is_old_line(stripped):
                old_text = self._extract_text_from_old(stripped)
                
                if old_text:
                    block = {
                        'old_text': old_text,
                        'lines': [],
                        'start_index': i
                    }
                    
                    comment_index = None
                    if i > 0 and lines[i - 1].strip().startswith('# game/'):
                        comment_index = i - 1
                    
                    if comment_index is not None:
                        block['lines'].append(lines[comment_index])
                    
                    block['lines'].append(lines[i])
                    
                    if i + 1 < len(lines) and self._is_new_line(lines[i + 1].strip()):
                        block['lines'].append(lines[i + 1])
                        i += 1
                    
                    blocks.append(block)
            
            i += 1
        
        return blocks

    def _extract_new_text_from_block(self, block: Dict, lines: List[str]) -> str:
        """Extrait le texte new d'un bloc de traduction"""
        start_idx = block['start_index']
        
        # Chercher la ligne new après la ligne old
        for i in range(start_idx + 1, min(start_idx + 3, len(lines))):
            if i < len(lines):
                line = lines[i].strip()
                if self._is_new_line(line):
                    return self._extract_text_from_new(line)
        
        return "(pas de traduction new trouvée)"

    def _extract_text_from_new(self, line: str) -> str:
        """Extrait le texte entre guillemets d'une ligne new"""
        new_match = re.search(r'new\s+"', line)
        if not new_match:
            new_match = re.search(r"new\s+'", line)
            if not new_match:
                return ""
            quote_char = "'"
        else:
            quote_char = '"'
        
        start_pos = new_match.end()
        
        i = start_pos
        while i < len(line):
            if line[i] == '\\':
                i += 2
            elif line[i] == quote_char:
                return line[start_pos:i]
            else:
                i += 1
        
        return ""

    def _is_old_line(self, line: str) -> bool:
        """Vérifie si une ligne est une ligne old avec du texte"""
        return line.startswith('old ') and '"' in line
    
    def _is_new_line(self, line: str) -> bool:
        """Vérifie si une ligne est une ligne new avec du texte"""
        return line.startswith('new ') and '"' in line
    
    def _extract_text_from_old(self, line: str) -> str:
        """Extrait le texte entre guillemets d'une ligne old"""
        old_match = re.search(r'old\s+"', line)
        if not old_match:
            old_match = re.search(r"old\s+'", line)
            if not old_match:
                return ""
            quote_char = "'"
        else:
            quote_char = '"'
        
        start_pos = old_match.end()
        
        i = start_pos
        while i < len(line):
            if line[i] == '\\':
                i += 2
            elif line[i] == quote_char:
                return line[start_pos:i]
            else:
                i += 1
        
        return ""
    
    def _string_exists_in_game(self, search_text: str, game_folder_path: str) -> bool:
        """Vérifie si une chaîne existe quelque part dans le dossier game - VERSION OPTIMISÉE"""
        try:
            # Vérifier le cache d'abord
            if search_text in self.string_search_cache:
                return self.string_search_cache[search_text]
            
            # Charger le cache des fichiers si nécessaire
            if (self.last_game_folder_path != game_folder_path or 
                not self.game_files_cache):
                self._load_game_files_cache(game_folder_path)
            
            # Recherche optimisée dans le cache
            for file_path, file_content in self.game_files_cache.items():
                if search_text in file_content:
                    self.string_search_cache[search_text] = True
                    return True
            
            self.string_search_cache[search_text] = False
            return False
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur lors de la recherche de '{search_text[:50]}...' : {e}", category="renpy_generator_clean_tl")
            return True  # En cas d'erreur, on conserve le bloc par sécurité
    
    def _load_game_files_cache(self, game_folder_path: str):
        """Charge tous les fichiers .rpy du dossier game/ en mémoire pour des recherches rapides"""
        try:
            from core.models.cache.cache_manager import cache_manager
            
            # Essayer de charger depuis le cache persistant
            project_path = os.path.dirname(game_folder_path)  # Remonter au dossier projet
            cached_data = cache_manager.get_game_files_cache(project_path)
            
            if cached_data:
                # Cache persistant trouvé, l'utiliser
                self.game_files_cache = cached_data
                self.string_search_cache = cache_manager.get_string_search_cache(project_path) or {}
                self.last_game_folder_path = game_folder_path
                log_message("INFO", f"🚀 Cache persistant chargé: {len(cached_data)} fichiers .rpy", category="renpy_generator_clean_tl")
                return
            
            # Pas de cache persistant, charger depuis le disque
            log_message("INFO", f"🔄 Chargement du cache des fichiers game/ ({game_folder_path})", category="renpy_generator_clean_tl")
            
            self.game_files_cache.clear()
            self.string_search_cache.clear()
            self.last_game_folder_path = game_folder_path
            
            files_loaded = 0
            for root, dirs, files in os.walk(game_folder_path):
                if 'tl' in dirs:
                    dirs.remove('tl')
                
                for file in files:
                    if file.endswith('.rpy'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                self.game_files_cache[file_path] = content
                                files_loaded += 1
                        except Exception as e:
                            log_message("ATTENTION", f"Impossible de lire {file_path}: {e}", category="renpy_generator_clean_tl")
            
            # Sauvegarder dans le cache persistant
            cache_manager.set_game_files_cache(project_path, self.game_files_cache)
            
            log_message("INFO", f"✅ Cache chargé: {files_loaded} fichiers .rpy en mémoire", category="renpy_generator_clean_tl")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur lors du chargement du cache: {e}", category="renpy_generator_clean_tl")
            self.game_files_cache.clear()
    
    def _clear_cache(self):
        """Nettoie le cache pour libérer la mémoire"""
        try:
            from core.models.cache.cache_manager import cache_manager
            
            cache_size = len(self.game_files_cache)
            search_cache_size = len(self.string_search_cache)
            
            # Sauvegarder le cache de recherche de chaînes avant de le vider
            if self.last_game_folder_path and self.string_search_cache:
                project_path = os.path.dirname(self.last_game_folder_path)
                cache_manager.set_string_search_cache(project_path, self.string_search_cache)
            
            self.game_files_cache.clear()
            self.string_search_cache.clear()
            self.last_game_folder_path = None
            
            log_message("DEBUG", f"🧹 Cache nettoyé: {cache_size} fichiers, {search_cache_size} recherches", category="renpy_generator_clean_tl")

        except Exception as e:
            log_message("ATTENTION", f"Erreur lors du nettoyage du cache: {e}", category="renpy_generator_clean_tl")
    
    def _search_in_file(self, search_text: str, file_path: str) -> bool:
        """Cherche une chaîne dans un fichier avec gestion robuste des échappements"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                return False
            
            # MÉTHODE 1 : Recherche exacte (la plus rapide)
            if search_text in content:
                                return True
            
            # MÉTHODE 2 : Extraire toutes les chaînes et comparer avec normalisation
            patterns = [
                (r'"([^"\\]*(?:\\.[^"\\]*)*)"', '"'),  # Guillemets doubles
                (r"'([^'\\]*(?:\\.[^'\\]*)*)'", "'"),  # Guillemets simples
            ]
            
            for pattern, quote_type in patterns:
                for match in re.finditer(pattern, content, re.DOTALL):
                    found_text = match.group(1)
                    
                    if self._strings_match(search_text, found_text):
                        return True
            
            # MÉTHODE 3 : Recherche floue (ignorer différences d'échappement)
            normalized_search = self._deep_normalize(search_text)
            normalized_content = self._deep_normalize(content)
            
            if normalized_search in normalized_content:
                return True
            
            return False
            
        except Exception as e:
            log_message("ATTENTION", f"Impossible de lire {os.path.basename(file_path)} : {e}", category="renpy_generator_clean_tl")
            return True  # En cas d'erreur, on conserve le bloc par sécurité
    
    def _strings_match(self, str1: str, str2: str) -> bool:
        """Compare deux chaînes avec normalisation des échappements"""
        # Comparaison directe d'abord
        if str1 == str2:
            return True
        
        # Normaliser et comparer
        norm1 = self._normalize_escapes(str1)
        norm2 = self._normalize_escapes(str2)
        
        return norm1 == norm2
    
    def _normalize_escapes(self, text: str) -> str:
        """Normalise les échappements d'une chaîne"""
        text = text.replace(r'\"', '"')
        text = text.replace(r"\'", "'")
        text = text.replace(r'\\', '\\')
        text = text.replace(r'\n', '\n')
        text = text.replace(r'\r', '\r')
        text = text.replace(r'\t', '\t')
        return text.strip()
    
    def _deep_normalize(self, text: str) -> str:
        """Normalisation profonde pour comparaison floue"""
        text = text.replace('\\', '')
        text = ' '.join(text.split())
        text = text.replace('"', '').replace("'", "")
        return text.lower().strip()
    
    def _normalize_string_for_comparison(self, text: str) -> str:
        """Normalise une chaîne pour la comparaison"""
        normalized = re.sub(r'"\s*"', '', text)
        normalized = re.sub(r"'\s*'", '', normalized)
        return normalized
    
    def _fix_empty_translate_blocks(self, lines: List[str]) -> List[str]:
        """Supprime les blocs translate vides"""
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            if self._is_translate_strings_line(stripped):
                has_content = False
                content_start = i + 1
                content_end = len(lines)

                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    
                    if self._is_translate_strings_line(next_line) or next_line.startswith('# TODO:'):
                        content_end = j
                        break
                    
                    if next_line.startswith('old ') or next_line.startswith('new '):
                        has_content = True
                                            
                    j += 1

                if has_content:
                    for k in range(i, content_end):
                        if k < len(lines):
                            fixed_lines.append(lines[k])
                else:
                    # ✅ DEBUG : Afficher le contenu du bloc avant suppression
                    block_content = []
                    for k in range(i, content_end):
                        if k < len(lines):
                            block_content.append(lines[k].strip())
                                                            
                    # ✅ CORRECTION : Ne garder AUCUNE ligne du bloc translate strings vide
                    # Toutes les lignes du bloc (y compris translate strings: et les commentaires) sont supprimées
                    pass  # Le bloc entier est ignoré/supprimé
                
                i = content_end - 1
            else:
                fixed_lines.append(line)
            
            i += 1
        
        return fixed_lines
    
    def _is_translate_strings_line(self, line: str) -> bool:
        """Vérifie si une ligne est un bloc translate strings"""
        pattern = r'^translate\s+\w+\s+strings:\s*'
        return bool(re.match(pattern, line))
    
    def _is_translate_id_line(self, line: str) -> bool:
        """Vérifie si une ligne est un bloc translate ID (pas strings)"""
        pattern = r'^translate\s+\w+\s+\w+:\s*$'
        return bool(re.match(pattern, line))
    
    def _fix_empty_translate_id_blocks(self, lines: List[str]) -> List[str]:
        """Supprime les blocs translate ID vides (ex: translate french foot_ca733686:)"""
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            if self._is_translate_id_line(stripped):
                has_content = False
                content_end = len(lines)

                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    
                    # Arrêter si on trouve un autre bloc translate ou un commentaire TODO
                    if (self._is_translate_id_line(next_line) or 
                        self._is_translate_strings_line(next_line) or 
                        next_line.startswith('# TODO:')):
                        content_end = j
                        break
                    
                    # Vérifier s'il y a du contenu réel (pas juste des commentaires ou lignes vides)
                    if (next_line and 
                        not next_line.startswith('#') and 
                        not next_line.startswith('    #') and
                        next_line.strip() != ''):
                        has_content = True
                                            
                    j += 1

                if has_content:
                    # Garder tout le bloc
                    for k in range(i, content_end):
                        if k < len(lines):
                            fixed_lines.append(lines[k])
                else:
                    # Supprimer complètement le bloc vide
                    block_content = []
                    for k in range(i, content_end):
                        if k < len(lines):
                            block_content.append(lines[k].strip())
                    # Rien n'est ajouté - le bloc entier est supprimé
                
                i = content_end - 1
            else:
                fixed_lines.append(line)
            
            i += 1
        
        return fixed_lines
    
    def _clean_orphan_comments_and_spacing(self, lines: List[str]) -> List[str]:
        """Nettoie les commentaires orphelins et gère l'espacement"""
        cleaned_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Détecter les commentaires de fichier et TODO
            if stripped.startswith('# game/') or stripped.startswith('# TODO:'):
                has_content_after = False
                empty_lines_after = 0
                
                # Rechercher du contenu valide après le commentaire
                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    
                    # Compter et ignorer les lignes vides (jusqu'à 3 lignes vides max)
                    if not next_line:
                        empty_lines_after += 1
                        if empty_lines_after <= 3:  # Autoriser jusqu'à 3 lignes vides
                            j += 1
                            continue
                        else:
                            # Trop de lignes vides, considérer comme orphelin
                            break
                    
                    # Vérifier s'il y a un bloc translate valide après le commentaire
                    if (next_line.startswith('old ') or 
                        next_line.startswith('new ') or
                        self._is_translate_strings_line(next_line) or
                        re.match(r'^translate\s+\w+\s+\w+:', next_line)):
                        has_content_after = True
                        break
                    
                    # Si on trouve un autre commentaire, arrêter la recherche
                    if (next_line.startswith('# game/') or 
                        next_line.startswith('# TODO:')):
                        break
                    
                    j += 1
                
                # Garder le commentaire seulement s'il y a du contenu après
                if has_content_after:
                    cleaned_lines.append(line)
                else:
                    # Commentaire orphelin - ne pas l'ajouter (suppression)
                    pass
            else:
                cleaned_lines.append(line)
            
            i += 1
        
        return self._normalize_line_spacing(cleaned_lines)
    
    def _normalize_line_spacing(self, lines: List[str]) -> List[str]:
        """Normalise l'espacement"""
        normalized_lines = []
        empty_line_count = 0
        
        for line in lines:
            if line.strip() == '':
                empty_line_count += 1
                # Autoriser maximum 2 lignes vides consécutives
                if empty_line_count <= 2:
                    normalized_lines.append(line)
            else:
                empty_line_count = 0
                normalized_lines.append(line)
        
        return normalized_lines

# ===== FONCTIONS UTILITAIRES SIMPLIFIÉES =====

def unified_clean_all_translations(lint_file_path: str, game_folder_path: str, tl_folder_path: str, 
                                  selected_languages: List[str]) -> Dict[str, any]:
    """
    Fonction utilitaire pour le nettoyage unifié de toutes les traductions
    
    Args:
        lint_file_path: Chemin vers le fichier lint.txt
        game_folder_path: Chemin vers le dossier game
        tl_folder_path: Chemin vers le dossier tl racine
        selected_languages: Liste des langues sélectionnées à traiter
        
    Returns:
        Dict avec les résultats consolidés du nettoyage
    """
    cleaner = UnifiedCleaner()
    return cleaner.unified_clean(lint_file_path, game_folder_path, tl_folder_path, selected_languages)

def scan_available_languages(tl_folder_path: str) -> List[str]:
    """
    Fonction utilitaire pour scanner les langues disponibles dans le dossier tl
    
    Args:
        tl_folder_path: Chemin vers le dossier tl racine
        
    Returns:
        Liste des langues disponibles
    """
    cleaner = UnifiedCleaner()
    return cleaner.scan_translation_folders(tl_folder_path)
