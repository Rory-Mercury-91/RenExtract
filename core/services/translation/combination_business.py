# core/business/combination_business.py
# Logique métier pour la combinaison et division de fichiers de traduction
# Migration complète de translation_generator.py

"""
Logique métier pour la combinaison et division de fichiers de traduction
- Combinaison de plusieurs fichiers .rpy en un seul
- Division d'un fichier combiné en fichiers séparés
- Gestion des exclusions et filtres
- Support des callbacks et threading
"""

import os
import re
import threading
import time
from typing import Dict, List, Optional, Callable, Any

from infrastructure.logging.logging import log_message
from infrastructure.config.config import config_manager


class CombinationBusiness:
    """Logique métier pour la combinaison et division de fichiers"""
    
    def __init__(self):
        """Initialise la logique métier de combinaison"""
        self.operation_cancelled = False
        self.current_project_path = None
        
        # Callbacks pour l'interface
        self.progress_callback: Optional[Callable] = None
        self.status_callback: Optional[Callable] = None
        self.completion_callback: Optional[Callable] = None
        self.error_callback: Optional[Callable] = None
        
        log_message("INFO", "CombinationBusiness initialisé", category="renpy_generator_combine_tl")
    
    def set_callbacks(self, progress_callback: Callable = None, status_callback: Callable = None,
                     completion_callback: Callable = None, error_callback: Callable = None):
        """Configure les callbacks pour l'interface utilisateur"""
        self.progress_callback = progress_callback
        self.status_callback = status_callback
        self.completion_callback = completion_callback
        self.error_callback = error_callback
    
    def _on_progress_update(self, progress: int, message: str = ""):
        """Callback de progression"""
        if self.progress_callback:
            try: 
                self.progress_callback(progress, message)
            except Exception as e: 
                log_message("ATTENTION", f"Erreur callback progress: {e}", category="renpy_generator_combine_tl")
    
    def _update_status(self, message: str):
        """Callback de statut"""
        if self.status_callback:
            try: 
                self.status_callback(message)
            except Exception as e: 
                log_message("ATTENTION", f"Erreur callback status: {e}", category="renpy_generator_combine_tl")
        log_message("INFO", f"Status: {message}", category="renpy_generator_combine_tl")
    
    def _notify_completion(self, success: bool, results: Dict):
        """Callback de fin d'opération"""
        if self.completion_callback:
            try: 
                self.completion_callback(success, results)
            except Exception as e: 
                log_message("ATTENTION", f"Erreur callback completion: {e}", category="renpy_generator_combine_tl")
    
    def _notify_error(self, error_message: str, exception: Optional[Exception] = None):
        """Callback d'erreur"""
        if self.error_callback:
            try: 
                self.error_callback(error_message, exception)
            except Exception as e: 
                log_message("ATTENTION", f"Erreur callback error: {e}", category="renpy_generator_combine_tl")
        log_message("ERREUR", f"Erreur: {error_message}", category="renpy_generator_combine_tl")
    
    def combine_translation_files_threaded(self, translation_folder: str, output_file: str,
                                         excluded_files: Optional[List[str]] = None,
                                         progress_callback: Optional[Callable] = None,
                                         status_callback: Optional[Callable] = None,
                                         completion_callback: Optional[Callable] = None) -> threading.Thread:
        """
        Lance la combinaison de fichiers en thread
        
        Args:
            translation_folder: Dossier contenant les fichiers de traduction
            output_file: Fichier de sortie combiné
            excluded_files: Liste des fichiers à exclure
            progress_callback: Callback de progression
            status_callback: Callback de statut
            completion_callback: Callback de fin
            
        Returns:
            Thread d'exécution
        """
        def worker():
            start_time = time.time()
            try:
                result = self.combine_translation_files(
                    translation_folder, output_file, excluded_files,
                    progress_callback, status_callback
                )
                result['execution_time'] = time.time() - start_time
                result['operation_type'] = 'combination'
                
                # Créer le résumé pour le popup
                if result['success']:
                    result['summary'] = {
                        'combination': f"Combinaison réussie: {len(result['files_combined'])} fichiers combinés",
                        'output_folder': os.path.dirname(output_file),
                        'execution_time': f"Temps d'exécution: {result['execution_time']:.1f}s"
                    }
                    if result.get('files_excluded'):
                        result['summary']['files_excluded'] = f"{len(result['files_excluded'])} fichiers exclus"
                else:
                    result['summary'] = {
                        'combination': "Échec de la combinaison",
                        'errors': result.get('errors', [])
                    }
                
                # Ajouter le fichier combiné aux résultats
                result['combined_file'] = output_file
                
                if not self.operation_cancelled and completion_callback:
                    completion_callback(result['success'], result)
                elif not self.operation_cancelled and self.completion_callback:
                    self.completion_callback(result['success'], result)
                    
            except Exception as e:
                if not self.operation_cancelled:
                    error_result = {
                        'success': False,
                        'operation_type': 'combination',
                        'errors': [f"Erreur inattendue dans le thread de combinaison: {e}"],
                        'execution_time': time.time() - start_time,
                        'summary': {
                            'combination': "Erreur critique lors de la combinaison",
                            'errors': [str(e)]
                        }
                    }
                    if completion_callback:
                        completion_callback(False, error_result)
                    elif self.completion_callback:
                        self.completion_callback(False, error_result)
            finally:
                if self.operation_cancelled:
                    cancelled_result = {
                        'success': False,
                        'cancelled': True,
                        'operation_type': 'combination',
                        'errors': ["Opération annulée."],
                        'execution_time': time.time() - start_time,
                        'summary': {
                            'combination': "Combinaison annulée par l'utilisateur"
                        }
                    }
                    if completion_callback:
                        completion_callback(False, cancelled_result)
                    elif self.completion_callback:
                        self.completion_callback(False, cancelled_result)
        
        self.operation_cancelled = False
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        
        log_message("INFO", f"Combinaison de fichiers lancée en thread", category="renpy_generator_combine_tl")
        return thread
    
    def combine_translation_files(self, translation_folder: str, output_file: str, 
                                excluded_files: Optional[List[str]] = None,
                                progress_callback: Optional[Callable] = None,
                                status_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Combine plusieurs fichiers de traduction en un seul - VERSION AVEC CORRESPONDANCE EXACTE
        
        Args:
            translation_folder: Dossier contenant les fichiers de traduction
            output_file: Fichier de sortie combiné
            excluded_files: Liste des fichiers à exclure
            progress_callback: Callback de progression
            status_callback: Callback de statut
            
        Returns:
            Dict avec les résultats de l'opération
        """
        result = {'success': False, 'errors': [], 'warnings': [], 'files_combined': [], 'output_folder': None}
        
        try:
            if self.operation_cancelled:
                raise InterruptedError("Opération annulée.")
            
            if progress_callback:
                progress_callback(5, "Initialisation de la combinaison...")
            elif self.progress_callback:
                self.progress_callback(5, "Initialisation de la combinaison...")
                
            if status_callback:
                status_callback("Initialisation de la combinaison...")
            elif self.status_callback:
                self.status_callback("Initialisation de la combinaison...")
            
            # ✅ EXCLUSION AUTOMATIQUE : Fichiers système + fichiers générés
            system_generated_files = [
                'common.rpy',
                'screens.rpy', 
                'options.rpy',
                '99_Z_Console.rpy',
                '99_Z_LangSelect.rpy',
                '99_Z_LangSelect_FontSize.rpy',
                '99_Z_FontSize.rpy',
                '0-font-system.rpy',
                'traduction.rpy'
            ]

            # Combiner les exclusions système avec les exclusions utilisateur
            if excluded_files is None:
                user_excluded_files = config_manager.get_renpy_excluded_files()
            else:
                user_excluded_files = excluded_files

            # Fusionner les listes (éviter les doublons)
            excluded_files = list(set(system_generated_files + user_excluded_files))            
            log_message("INFO", f"Début de la combinaison des fichiers de traduction", category="renpy_generator_combine_tl")
            log_message("DEBUG", f"Dossier source: {translation_folder}", category="renpy_generator_combine_tl")
            log_message("DEBUG", f"Fichier de sortie: {output_file}", category="renpy_generator_combine_tl")
            log_message("DEBUG", f"Fichiers exclus: {excluded_files}", category="renpy_generator_combine_tl")
            
            # Validation des paramètres
            if not os.path.isdir(translation_folder):
                result['errors'].append("Le dossier de traduction n'existe pas.")
                return result
            
            if progress_callback:
                progress_callback(10, "Scan des fichiers à combiner...")
            elif self.progress_callback:
                self.progress_callback(10, "Scan des fichiers à combiner...")
            
            # Collecter tous les fichiers .rpy à traiter avec CORRESPONDANCE EXACTE
            files_to_process = []
            files_excluded = []
            
            for root, _, files in os.walk(translation_folder):
                if self.operation_cancelled:
                    raise InterruptedError("Opération annulée.")
                for f in files:
                    if self.operation_cancelled:
                        raise InterruptedError("Opération annulée.")
                    if f.endswith('.rpy'):
                        # NOUVELLE LOGIQUE : Correspondance exacte du nom de fichier
                        if f in excluded_files:
                            files_excluded.append(os.path.join(root, f))
                            log_message("DEBUG", f"Fichier exclu (correspondance exacte): {f}", category="renpy_generator_combine_tl")
                        else:
                            files_to_process.append(os.path.join(root, f))
            
            if not files_to_process:
                if files_excluded:
                    result['errors'].append(f"Aucun fichier .rpy à combiner trouvé. {len(files_excluded)} fichiers exclus.")
                else:
                    result['errors'].append("Aucun fichier .rpy à combiner trouvé.")
                return result
            
            log_message("INFO", f"{len(files_to_process)} fichiers à combiner, {len(files_excluded)} exclus", category="renpy_generator_combine_tl")
            
            if progress_callback:
                progress_callback(20, "Création du fichier de sortie...")
            elif self.progress_callback:
                self.progress_callback(20, "Création du fichier de sortie...")
            
            # Créer le dossier de sortie si nécessaire
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Combiner les fichiers
            with open(output_file, 'w', encoding='utf-8') as outfile:
                # Écrire un en-tête détaillé
                outfile.write(f"# Fichier combiné généré par RenExtract\n")
                outfile.write(f"# Créé le: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                outfile.write(f"# Nombre de fichiers combinés: {len(files_to_process)}\n")
                if files_excluded:
                    outfile.write(f"# Fichiers exclus: {len(files_excluded)}\n")
                outfile.write(f"\n")
                
                for i, rpy_file in enumerate(files_to_process, 1):
                    if self.operation_cancelled:
                        raise InterruptedError("Opération annulée")
                    
                    progress_percent = 20 + (i * 60 // len(files_to_process))
                    if progress_callback:
                        progress_callback(progress_percent, f"Combinaison fichier {i}/{len(files_to_process)}")
                    elif self.progress_callback:
                        self.progress_callback(progress_percent, f"Combinaison fichier {i}/{len(files_to_process)}")
                    
                    # Calculer le chemin relatif pour l'en-tête
                    relative_path = os.path.relpath(rpy_file, translation_folder)
                    
                    # Écrire l'en-tête de séparation
                    outfile.write(f"\n# ===== {relative_path.replace(os.sep, '/')} =====\n")
                    
                    try:
                        # Lire et écrire le contenu du fichier
                        with open(rpy_file, 'r', encoding='utf-8-sig') as infile:
                            content = infile.read()
                            outfile.write(content)
                            
                            # S'assurer qu'il y a une ligne vide à la fin
                            if not content.endswith('\n'):
                                outfile.write('\n')
                        
                        result['files_combined'].append(rpy_file)
                        log_message("DEBUG", f"Fichier combiné: {os.path.basename(rpy_file)}", category="renpy_generator_combine_tl")
                        
                    except Exception as e:
                        error_msg = f"Erreur lecture {os.path.basename(rpy_file)}: {e}"
                        result['errors'].append(error_msg)
                        log_message("ERREUR", error_msg, category="renpy_generator_combine_tl")
            
            # Ajouter les exclusions aux résultats pour le rapport
            result['files_excluded'] = files_excluded
            
            if progress_callback:
                progress_callback(85, "Suppression des fichiers sources...")
            elif self.progress_callback:
                self.progress_callback(85, "Suppression des fichiers sources...")
            
            # Supprimer les fichiers sources combinés
            files_deleted = 0
            for rpy_file in result['files_combined']:
                try:
                    if os.path.exists(rpy_file):
                        os.remove(rpy_file)
                        files_deleted += 1
                except Exception as e:
                    warn_msg = f"Impossible de supprimer {os.path.basename(rpy_file)}: {e}"
                    result['warnings'].append(warn_msg)
                    log_message("ATTENTION", warn_msg, category="renpy_generator_combine_tl")
            
            if progress_callback:
                progress_callback(95, "Nettoyage des dossiers vides...")
            elif self.progress_callback:
                self.progress_callback(95, "Nettoyage des dossiers vides...")
            
            # Supprimer les dossiers vides
            self._cleanup_empty_directories(translation_folder)
            
            # Marquer comme réussi si au moins un fichier a été combiné
            if result['files_combined']:
                result['success'] = True
                result['output_folder'] = os.path.dirname(output_file)
                result['combined_file'] = output_file  # Ajouter le fichier de sortie aux résultats
                log_message("INFO", f"Combinaison réussie: {len(result['files_combined'])} fichiers combinés, {files_deleted} supprimés, {len(files_excluded)} exclus", category="renpy_generator_combine_tl")
            else:
                result['errors'].append("Aucun fichier n'a pu être combiné")
                
        except InterruptedError as ie:
            result['errors'].append(str(ie))
            log_message("INFO", str(ie), category="renpy_generator_combine_tl")
        except Exception as e:
            result['errors'].append(f"Erreur inattendue: {e}")
            log_message("ERREUR", f"Erreur combinaison: {e}", category="renpy_generator_combine_tl")
        finally:
            if result['success']:
                if progress_callback:
                    progress_callback(100, "Combinaison terminée")
                elif self.progress_callback:
                    self.progress_callback(100, "Combinaison terminée")
            else:
                if progress_callback:
                    progress_callback(0, "Échec de la combinaison")
                elif self.progress_callback:
                    self.progress_callback(0, "Échec de la combinaison")
        
        return result
    
    def divide_translation_file_threaded(self, combined_file: str, output_folder: str,
                                       progress_callback: Optional[Callable] = None,
                                       status_callback: Optional[Callable] = None,
                                       completion_callback: Optional[Callable] = None) -> threading.Thread:
        """
        Lance la division de fichier en thread
        
        Args:
            combined_file: Fichier combiné à diviser
            output_folder: Dossier de sortie pour les fichiers divisés
            progress_callback: Callback de progression
            status_callback: Callback de statut
            completion_callback: Callback de fin
            
        Returns:
            Thread d'exécution
        """
        def worker():
            start_time = time.time()
            try:
                result = self.divide_translation_file(
                    combined_file, output_folder,
                    progress_callback, status_callback
                )
                result['execution_time'] = time.time() - start_time
                result['operation_type'] = 'division'
                
                # Créer le résumé pour le popup
                if result['success']:
                    result['summary'] = {
                        'division': f"Division réussie: {len(result['divided_files'])} fichiers créés",
                        'output_folder': output_folder,
                        'execution_time': f"Temps d'exécution: {result['execution_time']:.1f}s"
                    }
                else:
                    result['summary'] = {
                        'division': "Échec de la division",
                        'errors': result.get('errors', [])
                    }
                
                # Ajouter le fichier source aux résultats
                result['source_file'] = combined_file
                
                if not self.operation_cancelled and completion_callback:
                    completion_callback(result['success'], result)
                elif not self.operation_cancelled and self.completion_callback:
                    self.completion_callback(result['success'], result)
                    
            except Exception as e:
                if not self.operation_cancelled:
                    error_result = {
                        'success': False,
                        'operation_type': 'division',
                        'errors': [f"Erreur inattendue dans le thread de division: {e}"],
                        'execution_time': time.time() - start_time,
                        'summary': {
                            'division': "Erreur critique lors de la division",
                            'errors': [str(e)]
                        }
                    }
                    if completion_callback:
                        completion_callback(False, error_result)
                    elif self.completion_callback:
                        self.completion_callback(False, error_result)
            finally:
                if self.operation_cancelled:
                    cancelled_result = {
                        'success': False,
                        'cancelled': True,
                        'operation_type': 'division',
                        'errors': ["Opération annulée."],
                        'execution_time': time.time() - start_time,
                        'summary': {
                            'division': "Division annulée par l'utilisateur"
                        }
                    }
                    if completion_callback:
                        completion_callback(False, cancelled_result)
                    elif self.completion_callback:
                        self.completion_callback(False, cancelled_result)
        
        self.operation_cancelled = False
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        
        log_message("INFO", f"Division de fichier lancée en thread", category="renpy_generator_combine_tl")
        return thread
    
    def divide_translation_file(self, combined_file: str, output_folder: str,
                              progress_callback: Optional[Callable] = None,
                              status_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Divise un fichier de traduction combiné en fichiers séparés
        
        Args:
            combined_file: Fichier combiné à diviser
            output_folder: Dossier de sortie pour les fichiers divisés
            progress_callback: Callback de progression
            status_callback: Callback de statut
            
        Returns:
            Dict avec les résultats de l'opération
        """
        result = {'success': False, 'errors': [], 'warnings': [], 'divided_files': [], 'output_folder': output_folder}
        
        try:
            if self.operation_cancelled:
                raise InterruptedError("Opération annulée.")
            
            if progress_callback:
                progress_callback(5, "Initialisation de la division...")
            elif self.progress_callback:
                self.progress_callback(5, "Initialisation de la division...")
                
            if status_callback:
                status_callback("Initialisation de la division...")
            elif self.status_callback:
                self.status_callback("Initialisation de la division...")
            
            log_message("INFO", f"Début de la division du fichier combiné", category="renpy_generator_combine_tl")
            log_message("DEBUG", f"Fichier source: {combined_file}", category="renpy_generator_combine_tl")
            log_message("DEBUG", f"Dossier de sortie: {output_folder}", category="renpy_generator_combine_tl")
            
            # Validation des paramètres
            if not os.path.isfile(combined_file):
                result['errors'].append("Le fichier combiné n'existe pas.")
                return result
            
            if progress_callback:
                progress_callback(10, "Lecture du fichier combiné...")
            elif self.progress_callback:
                self.progress_callback(10, "Lecture du fichier combiné...")
            
            # Lire le contenu du fichier combiné
            with open(combined_file, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            
            if progress_callback:
                progress_callback(20, "Analyse des sections...")
            elif self.progress_callback:
                self.progress_callback(20, "Analyse des sections...")
            
            # Diviser le contenu en sections basées sur les séparateurs
            sections = re.split(r'\n# ===== (.+?) =====\n', content)
            
            # Le premier élément est généralement l'en-tête avant la première section
            if len(sections) < 3:
                result['errors'].append("Aucun séparateur de fichier trouvé dans le fichier combiné.")
                return result
            
            # Créer le dossier de sortie
            os.makedirs(output_folder, exist_ok=True)
            
            # Traiter les sections (par paires: nom_fichier, contenu)
            sections_count = (len(sections) - 1) // 2
            log_message("INFO", f"{sections_count} sections détectées pour division", category="renpy_generator_combine_tl")
            
            for i in range(1, len(sections), 2):
                if self.operation_cancelled:
                    raise InterruptedError("Opération annulée")
                
                section_num = (i + 1) // 2
                progress_percent = 20 + (section_num * 60 // sections_count)
                if progress_callback:
                    progress_callback(progress_percent, f"Division section {section_num}/{sections_count}")
                elif self.progress_callback:
                    self.progress_callback(progress_percent, f"Division section {section_num}/{sections_count}")
                
                # Nom du fichier (converti en chemin du système)
                file_relative_path = sections[i].replace('/', os.sep)
                file_path = os.path.join(output_folder, file_relative_path)
                
                # Contenu du fichier
                file_content = sections[i + 1].strip() if i + 1 < len(sections) else ""
                
                try:
                    # Créer les dossiers parents si nécessaire
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    # Écrire le fichier
                    with open(file_path, 'w', encoding='utf-8') as outfile:
                        outfile.write(file_content)
                        if not file_content.endswith('\n'):
                            outfile.write('\n')
                    
                    result['divided_files'].append(file_path)
                    log_message("DEBUG", f"Fichier créé: {file_relative_path}", category="renpy_generator_combine_tl")
                    
                except Exception as e:
                    error_msg = f"Erreur création {file_relative_path}: {e}"
                    result['errors'].append(error_msg)
                    log_message("ERREUR", error_msg, category="renpy_generator_combine_tl")
            
            if progress_callback:
                progress_callback(90, "Suppression du fichier combiné...")
            elif self.progress_callback:
                self.progress_callback(90, "Suppression du fichier combiné...")
            
            # Supprimer le fichier combiné original
            try:
                os.remove(combined_file)
                log_message("DEBUG", f"Fichier combiné supprimé: {os.path.basename(combined_file)}", category="renpy_generator_combine_tl")
            except Exception as e:
                warn_msg = f"Impossible de supprimer le fichier combiné: {e}"
                result['warnings'].append(warn_msg)
                log_message("ATTENTION", warn_msg, category="renpy_generator_combine_tl")
            
            # Marquer comme réussi si au moins un fichier a été créé
            if result['divided_files']:
                result['success'] = True
                log_message("INFO", f"Division réussie: {len(result['divided_files'])} fichiers créés", category="renpy_generator_combine_tl")
            else:
                result['errors'].append("Aucun fichier n'a pu être créé")
                
        except InterruptedError as ie:
            result['errors'].append(str(ie))
            log_message("INFO", str(ie), category="renpy_generator_combine_tl")
        except Exception as e:
            result['errors'].append(f"Erreur inattendue: {e}")
            log_message("ERREUR", f"Erreur division: {e}", category="renpy_generator_combine_tl")
        finally:
            if result['success']:
                if progress_callback:
                    progress_callback(100, "Division terminée")
                elif self.progress_callback:
                    self.progress_callback(100, "Division terminée")
            else:
                if progress_callback:
                    progress_callback(0, "Échec de la division")
                elif self.progress_callback:
                    self.progress_callback(0, "Échec de la division")
        
        return result
    
    def _cleanup_empty_directories(self, root_path: str):
        """
        Supprime récursivement les dossiers vides
        
        Args:
            root_path: Chemin racine à partir duquel nettoyer
        """
        try:
            # Parcourir de bas en haut pour supprimer les dossiers vides
            for root, dirs, files in os.walk(root_path, topdown=False):
                for directory in dirs:
                    dir_path = os.path.join(root, directory)
                    try:
                        # Tenter de supprimer le dossier (ne fonctionne que s'il est vide)
                        os.rmdir(dir_path)
                        log_message("DEBUG", f"Dossier vide supprimé: {directory}", category="renpy_generator_combine_tl")
                    except OSError:
                        # Le dossier n'est pas vide, c'est normal
                        pass
        except Exception as e:
            log_message("ATTENTION", f"Erreur nettoyage dossiers vides: {e}", category="renpy_generator_combine_tl")
    
    def cancel_operation(self):
        """Annule l'opération en cours"""
        self.operation_cancelled = True
        log_message("INFO", "Annulation demandée par l'utilisateur.", category="renpy_generator_combine_tl")
    
    def cleanup(self):
        """Nettoie les ressources"""
        try:
            log_message("DEBUG", "CombinationBusiness nettoyé", category="renpy_generator_combine_tl")
        except Exception as e:
            log_message("ATTENTION", f"Erreur lors du nettoyage: {e}", category="renpy_generator_combine_tl")
