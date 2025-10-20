# core/business/rpa_extraction_business.py
# Logique métier complète pour l'extraction RPA/RPYC - Onglet 1
# Migration complète de translation_generator.py

"""
Logique métier complète pour l'extraction et décompilation RPA/RPYC
- Extraction des archives RPA avec rpatool
- Décompilation des fichiers RPYC avec unrpyc (v1/v2)
- Détection automatique de la version Ren'Py
- Construction d'archives RPA personnalisées
- Gestion complète des outils et callbacks
"""

import os
import sys
import subprocess
import threading
import glob
import re
import shutil
import struct
import time
import ctypes
from ctypes import wintypes
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any, Tuple
from datetime import datetime

from infrastructure.logging.logging import log_message
from core.tools.downloader import get_downloader
from core.tools.python_manager import get_python_manager
from core.tools.sdk_manager import get_sdk_manager


class RPAExtractionBusiness:
    """Logique métier complète pour l'extraction RPA/RPYC"""
    
    def __init__(self, tools_dir: str = None):
        """
        Initialise la logique métier d'extraction
        
        Args:
            tools_dir: Répertoire pour stocker les outils
        """
        if tools_dir is None:
            tools_dir = os.path.join(os.path.expanduser("~"), ".renextract_tools")
        
        self.tools_dir = tools_dir
        self.unrpyc_dir = os.path.join(tools_dir, "unrpyc")
        self.rpatool_dir = os.path.join(tools_dir, "rpatool")
        
        # Gestionnaires d'outils
        self.downloader = get_downloader()
        self.python_manager = get_python_manager(tools_dir)
        self.sdk_manager = get_sdk_manager(tools_dir)
        
        # État de l'extraction
        self.rpa_extraction_done = False
        self.operation_cancelled = False
        self.current_project_path = None
        
        # Callbacks pour l'interface
        self.progress_callback: Optional[Callable] = None
        self.status_callback: Optional[Callable] = None
        self.completion_callback: Optional[Callable] = None
        self.error_callback: Optional[Callable] = None
        
        # Assurer que les dossiers existent
        os.makedirs(tools_dir, exist_ok=True)
        
        # Builder RPA
        self.rpa_builder = RPABuilder()
        
        log_message("INFO", "RPAExtractionBusiness initialisé", category="renpy_generator_rpa")
    
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
                log_message("ATTENTION", f"Erreur callback progress: {e}", category="renpy_generator_rpa")
    
    def _update_status(self, message: str):
        """Callback de statut"""
        if self.status_callback:
            try: 
                self.status_callback(message)
            except Exception as e: 
                log_message("ATTENTION", f"Erreur callback status: {e}", category="renpy_generator_rpa")
        log_message("INFO", f"Status: {message}", category="renpy_generator_rpa")
    
    def _notify_completion(self, success: bool, results: Dict):
        """Callback de fin d'opération"""
        if self.completion_callback:
            try: 
                self.completion_callback(success, results)
            except Exception as e: 
                log_message("ATTENTION", f"Erreur callback completion: {e}", category="renpy_generator_rpa")
    
    def _notify_error(self, error_message: str, exception: Optional[Exception] = None):
        """Callback d'erreur"""
        if self.error_callback:
            try: 
                self.error_callback(error_message, exception)
            except Exception as e: 
                log_message("ATTENTION", f"Erreur callback error: {e}", category="renpy_generator_rpa")
        log_message("ERREUR", f"Erreur: {error_message}", category="renpy_generator_rpa")
    
    def setup_extraction_tools(self) -> bool:
        """
        Télécharge et prépare tous les outils nécessaires
        
        Returns:
            True si tous les outils sont prêts
        """
        try:
            log_message("INFO", f"Vérification des outils dans : {self.tools_dir}", category="renpy_generator_rpa")
            
            # Configurer Python embedded pour les outils
            python_3_exe = self.python_manager.setup_python_embedded()
            if not python_3_exe:
                log_message("ERREUR", "Échec configuration Python 3.11 embedded", category="renpy_generator_rpa")
                return False
            
            python_27_exe = self.python_manager.setup_python27_embedded()
            if not python_27_exe:
                log_message("ATTENTION", "Python 2.7 embedded non disponible (optionnel)", category="renpy_generator_rpa")
            
            # Télécharger unrpyc pour Ren'Py 8+ (Python 3)
            unrpyc_v2_result = self.downloader.download_and_extract_zip(
                # url="https://github.com/CensoredUsername/unrpyc/archive/refs/heads/master.zip",
                url="https://github.com/madeddy/unrpyc/archive/refs/heads/renpy_v8.4_code_change_fixes.zip",
                dest_path=os.path.join(self.unrpyc_dir, "v2"),
                # zip_root_dir="unrpyc-master"
                zip_root_dir="unrpyc-renpy_v8.4_code_change_fixes"
            )
            
            if not unrpyc_v2_result['success']:
                log_message("ERREUR", f"Échec téléchargement unrpyc v2: {unrpyc_v2_result['error']}", category="renpy_generator_rpa")
                return False
            
            # Télécharger unrpyc pour Ren'Py 6/7 (Python 2)
            unrpyc_v1_result = self.downloader.download_and_extract_zip(
                url="https://github.com/CensoredUsername/unrpyc/archive/refs/heads/legacy.zip",
                dest_path=os.path.join(self.unrpyc_dir, "v1"),
                zip_root_dir="unrpyc-legacy"
            )
            
            if not unrpyc_v1_result['success']:
                log_message("ATTENTION", f"Échec téléchargement unrpyc v1: {unrpyc_v1_result['error']}", category="renpy_generator_rpa")
            
            # Télécharger rpatool
            rpatool_dest = os.path.join(self.rpatool_dir, "rpatool-master")
            rpatool_result = self.downloader.download_and_extract_zip(
                url="https://github.com/shizmob/rpatool/archive/refs/heads/master.zip",
                dest_path=rpatool_dest,
                zip_root_dir="rpatool-master"
            )
            
            if not rpatool_result['success']:
                log_message("ERREUR", f"Échec téléchargement rpatool: {rpatool_result['error']}", category="renpy_generator_rpa")
                return False
            
            # Renommer le fichier rpatool si nécessaire
            original_rpatool = os.path.join(rpatool_dest, "rpatool")
            renamed_rpatool = os.path.join(rpatool_dest, "rpatool.py")
            if os.path.exists(original_rpatool) and not os.path.exists(renamed_rpatool):
                os.rename(original_rpatool, renamed_rpatool)
            
            log_message("INFO", "Tous les outils sont prêts", category="renpy_generator_rpa")
            return True
            
        except Exception as e:
            log_message("ERREUR", f"Erreur setup_extraction_tools: {e}", category="renpy_generator_rpa")
            return False
    
    def get_project_info(self, project_path: str) -> Dict[str, Any]:
        """Récupère les informations détaillées sur un projet Ren'Py."""
        info = {
            'project_path': project_path,
            'project_name': os.path.basename(project_path),
            'executable_found': False,
            'executable_path': None,
            'game_folder_exists': False,
            'renpy_version': 'Unknown',
            'rpa_files': [],
            'rpyc_files': [],
            'rpy_files': [],
            'translation_folders': [],
            'estimated_size': 0,
            'last_modified': None,
            'errors': []
        }
        
        try:
            if not os.path.exists(project_path):
                info['errors'].append("Le chemin du projet n'existe pas")
                return info
            
            # Vérifier l'exécutable principal
            executable_path = self.detect_game_executable(project_path)
            if executable_path:
                info['executable_found'] = True
                info['executable_path'] = executable_path
            
            # Vérifier le dossier game
            game_dir = os.path.join(project_path, "game")
            info['game_folder_exists'] = os.path.isdir(game_dir)
            
            # Détecter la version Ren'Py
            try:
                version_info = self.detect_renpy_version(project_path)
                info['renpy_version'] = version_info.get('version', 'Unknown')
                info['detection_method'] = version_info.get('detected_via', 'unknown')
            except Exception as e:
                info['errors'].append(f"Erreur détection version: {e}")
            
            # Scanner les fichiers
            search_dirs = [project_path]
            if info['game_folder_exists']:
                search_dirs.append(game_dir)
            
            for search_dir in search_dirs:
                for root, dirs, files in os.walk(search_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        file_lower = file.lower()
                        
                        if file_lower.endswith('.rpa'):
                            info['rpa_files'].append(file_path)
                        elif file_lower.endswith('.rpyc'):
                            info['rpyc_files'].append(file_path)
                        elif file_lower.endswith('.rpy'):
                            info['rpy_files'].append(file_path)
            
            # Scanner les dossiers de traduction
            tl_dir = os.path.join(game_dir, "tl") if info['game_folder_exists'] else None
            if tl_dir and os.path.isdir(tl_dir):
                for item in os.listdir(tl_dir):
                    item_path = os.path.join(tl_dir, item)
                    if os.path.isdir(item_path):
                        info['translation_folders'].append(item)
            
            # Calculer la taille estimée (en MB)
            try:
                total_size = 0
                for file_list in [info['rpa_files'], info['rpyc_files'], info['rpy_files']]:
                    for file_path in file_list:
                        if os.path.exists(file_path):
                            total_size += os.path.getsize(file_path)
                info['estimated_size'] = round(total_size / (1024 * 1024), 2)  # MB
            except Exception as e:
                info['errors'].append(f"Erreur calcul taille: {e}")
            
            # Date de dernière modification
            try:
                if info['executable_path'] and os.path.exists(info['executable_path']):
                    timestamp = os.path.getmtime(info['executable_path'])
                    info['last_modified'] = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
            except Exception as e:
                info['errors'].append(f"Erreur date modification: {e}")
            
            log_message("DEBUG", f"Infos projet collectées: {len(info['rpa_files'])} RPA, {len(info['rpyc_files'])} RPYC, {len(info['rpy_files'])} RPY", category="renpy_generator_rpa")
            
        except Exception as e:
            info['errors'].append(f"Erreur générale: {e}")
            log_message("ERREUR", f"Erreur get_project_info: {e}", category="renpy_generator_rpa")
        
        return info
    
    def detect_game_executable(self, project_path: str) -> Optional[str]:
        """
        Détecte automatiquement l'exécutable principal du jeu Ren'Py
        VERSION CORRIGÉE - Compatible avec les crochets dans les noms
        """
        log_message("INFO", "Détection de l'exécutable principal du jeu...", category="renpy_generator_rpa")
        
        if not os.path.isdir(project_path):
            log_message("ERREUR", f"Le chemin du projet n'existe pas : {project_path}", category="renpy_generator_rpa")
            return None
        
        # Extensions selon la plateforme
        if sys.platform == "win32":  # Windows
            extensions = ['.exe']
            # Patterns spéciaux pour Windows
            special_suffixes = ['-32.exe', '-64.exe']
        elif sys.platform == "darwin":  # macOS
            extensions = ['.app', '.sh']
            special_suffixes = []
        else:  # Linux et autres Unix
            extensions = ['.sh', '.py']
            special_suffixes = []
        
        found_executables = []
        
        try:
            # Utiliser os.listdir() au lieu de glob pour éviter les problèmes avec []
            for filename in os.listdir(project_path):
                filepath = os.path.join(project_path, filename)
                
                if os.path.isfile(filepath):
                    filename_lower = filename.lower()
                    
                    # Vérifier les extensions principales
                    is_executable = any(filename_lower.endswith(ext) for ext in extensions)
                    
                    # Vérifier les suffixes spéciaux (Windows)
                    if not is_executable and special_suffixes:
                        is_executable = any(filename_lower.endswith(suffix) for suffix in special_suffixes)
                    
                    if is_executable:
                        # Exclure certains fichiers système
                        if not any(exclude in filename_lower for exclude in ['uninstall', 'setup', 'installer', 'update']):
                            found_executables.append(filepath)
        
        except Exception as e:
            log_message("ERREUR", f"Erreur lors de la lecture du dossier {project_path}: {e}", category="renpy_generator_rpa")
            return None
        
        # Trier par priorité (nom du dossier parent en premier)
        project_name = os.path.basename(project_path).lower()
        prioritized_executables = []
        other_executables = []
        
        for exe in found_executables:
            exe_name = os.path.basename(exe).lower()
            # Priorité aux exécutables qui contiennent le nom du projet
            if any(word in exe_name for word in project_name.split('-')):
                prioritized_executables.append(exe)
            else:
                other_executables.append(exe)
        
        # Combiner les listes (prioritaires en premier)
        all_executables = prioritized_executables + other_executables
        
        if not all_executables:
            log_message("ERREUR", "Aucun exécutable trouvé dans le dossier du projet", category="renpy_generator_rpa")
            return None
        
        # Prendre le premier exécutable trouvé
        selected_executable = all_executables[0]
        
        log_message("INFO", f"Exécutable détecté : {os.path.basename(selected_executable)}", category="renpy_generator_rpa")
        if len(all_executables) > 1:
            log_message("DEBUG", f"Autres exécutables disponibles : {[os.path.basename(exe) for exe in all_executables[1:]]}", category="renpy_generator_rpa")
        
        return selected_executable
    
    def extract_rpa_files_threaded(self, project_path: str, delete_rpa_after: bool = False, 
                                  progress_callback: Optional[Callable] = None,
                                  status_callback: Optional[Callable] = None,
                                  completion_callback: Optional[Callable] = None) -> threading.Thread:
        """
        Lance la décompilation dans un thread séparé
        
        Args:
            project_path: Chemin vers le projet
            delete_rpa_after: Supprimer les RPA après extraction
            progress_callback: Callback de progression
            status_callback: Callback de statut
            completion_callback: Callback de fin
            
        Returns:
            Thread d'exécution
        """
        def worker():
            start_time = time.time()
            try:
                self.current_project_path = project_path
                log_message("DEBUG", f"Paramètre delete_rpa_after reçu: {delete_rpa_after}", category="renpy_generator_rpa")
                result = self.execute_unren_decompilation(project_path, delete_rpa_after, 
                                                        progress_callback, status_callback)
                
                result['execution_time'] = time.time() - start_time
                
                # Créer le résumé pour le popup
                if result['success']:
                    archives_info = []
                    if result.get('rpa_extracted'):
                        archives_info.append(f"RPA extraites: {len(result['rpa_extracted'])}")
                    if result.get('rpyc_converted', 0) > 0:
                        archives_info.append(f"RPYC converties: {result['rpyc_converted']}")
                    
                    result['summary'] = {
                        'rpa': f"Décompilation terminée avec succès",
                        'details': archives_info,
                        'execution_time': f"Temps d'exécution: {result['execution_time']:.1f}s"
                    }
                else:
                    result['summary'] = {
                        'rpa': "Échec de la décompilation",
                        'alternative_method_url': "https://f95zone.to/threads/unren-bat-v1-0-11d-rpa-extractor-rpyc-decompiler-console-developer-menu-enabler.3083/",
                        'errors': result.get('errors', [])
                    }
                
                if not self.operation_cancelled and completion_callback:
                    completion_callback(result['success'], result)
                elif not self.operation_cancelled and self.completion_callback:
                    self.completion_callback(result['success'], result)
                    
            except Exception as e:
                if not self.operation_cancelled:
                    error_result = {
                        'success': False,
                        'errors': [f"Erreur inattendue dans le thread d'extraction: {e}"],
                        'execution_time': time.time() - start_time,
                        'summary': {
                            'rpa': "Erreur critique lors de la décompilation",
                            'alternative_method_url': "https://f95zone.to/threads/unren-bat-v1-0-11d-rpa-extractor-rpyc-decompiler-console-developer-menu-enabler.3083/",
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
                        'errors': ["Opération annulée."],
                        'execution_time': time.time() - start_time,
                        'summary': {
                            'rpa': "Décompilation annulée par l'utilisateur"
                        }
                    }
                    if completion_callback:
                        completion_callback(False, cancelled_result)
                    elif self.completion_callback:
                        self.completion_callback(False, cancelled_result)
                self.current_project_path = None
        
        self.operation_cancelled = False
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        
        log_message("INFO", f"Extraction RPA/RPYC lancée en thread", category="renpy_generator_rpa")
        return thread
    
    def execute_unren_decompilation(self, project_path: str, delete_rpa_after: bool = False,
                                progress_callback: Optional[Callable] = None,
                                status_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Orchestre la décompilation UnRen avec flag RPA extraction
        VERSION MODIFIÉE : Extraction complète du dossier game (y compris tl/)
        
        Args:
            project_path: Chemin vers le projet
            delete_rpa_after: Supprimer les RPA après extraction
            progress_callback: Callback de progression
            status_callback: Callback de statut
            
        Returns:
            Dict avec les résultats de l'opération
        """
        result = {
            'success': False, 'errors': [], 'warnings': [], 'rpa_extracted': [], 
            'rpyc_converted': 0, 'rpyc_skipped': 0, 'rpyc_failed': 0,
            'rpa_extraction_failed': [], 'rpa_deleted_count': 0,
            'total_files_extracted': 0, 'unrpyc_attempts': [], 'summary': {}
        }
        workflow_start_time = time.time()

        try:
            # Phase 0 : initialisation
            log_message("INFO", "[Phase 0] Initialisation de la décompilation...", category="renpy_generator_rpa")
            if status_callback:
                status_callback("Initialisation de la décompilation...")
            elif self.status_callback:
                self.status_callback("Initialisation de la décompilation...")
            
            if not self.setup_extraction_tools():
                result['errors'].append("Échec configuration des outils")
                return result
            
            self.rpa_extraction_done = False

            # Phase 1 : détection et extraction des .rpa
            log_message("INFO", "[Phase 1] Détection et extraction des .rpa...", category="renpy_generator_rpa")
            if progress_callback:
                progress_callback(10, "Détection des fichiers RPA...")
            elif self.progress_callback:
                self.progress_callback(10, "Détection des fichiers RPA...")
            
            game_dir = os.path.join(project_path, "game") if os.path.isdir(os.path.join(project_path, "game")) else project_path
            rpa_files = [os.path.join(root, f) for root, _, files in os.walk(project_path) for f in files if f.lower().endswith('.rpa')]
            log_message("INFO", f"Fichiers .rpa trouvés : {len(rpa_files)}", category="renpy_generator_rpa")
            
            rpa_success_count = 0
            total_files_extracted = 0
            
            for i, rpa in enumerate(rpa_files, 1):
                if self.operation_cancelled:
                    raise InterruptedError("Opération annulée")
                
                if progress_callback:
                    progress_callback(10 + (i * 25 // max(len(rpa_files), 1)), f"Extraction .rpa ({i}/{len(rpa_files)})")
                elif self.progress_callback:
                    self.progress_callback(10 + (i * 25 // max(len(rpa_files), 1)), f"Extraction .rpa ({i}/{len(rpa_files)})")
                
                log_message("DEBUG", f"Extraction ({i}/{len(rpa_files)}): {os.path.basename(rpa)}", category="renpy_generator_rpa")
                
                files_before = len([f for f in os.listdir(game_dir) if os.path.isfile(os.path.join(game_dir, f))]) if os.path.exists(game_dir) else 0
                
                success = self._extract_single_rpa(rpa, game_dir)
                
                if success:
                    files_after = len([f for f in os.listdir(game_dir) if os.path.isfile(os.path.join(game_dir, f))]) if os.path.exists(game_dir) else 0
                    files_extracted_from_this_rpa = max(0, files_after - files_before)
                    total_files_extracted += files_extracted_from_this_rpa
                    
                    result['rpa_extracted'].append(rpa)
                    rpa_success_count += 1
                    log_message("DEBUG", f"Extraction {os.path.basename(rpa)} réussie ({files_extracted_from_this_rpa} fichiers)", category="renpy_generator_rpa")
                else:
                    result['rpa_extraction_failed'].append(rpa)
                    warn = f"Échec extraction {os.path.basename(rpa)}"
                    result['warnings'].append(warn)
                    log_message("ATTENTION", warn, category="renpy_generator_rpa")
            
            # MARQUER que l'extraction RPA est terminée
            self.rpa_extraction_done = True
            result['total_files_extracted'] = total_files_extracted
            
            if rpa_files:
                log_message("INFO", f"Extraction terminée : {rpa_success_count}/{len(rpa_files)} réussies ({total_files_extracted} fichiers extraits)", category="renpy_generator_rpa")

            # Phase 2 : détection de la version Ren'Py
            log_message("INFO", "[Phase 2] Détection de la version Ren'Py...", category="renpy_generator_rpa")
            info = self.detect_renpy_version(project_path)
            primary_version = info.get('unrpyc_version_needed', 'v2')
            detected_via = info.get('detected_via', 'unknown')
            
            fallback_version = 'v1' if primary_version == 'v2' else 'v2'
            log_message("DEBUG", f"Version primaire : unrpyc {primary_version} (détectée via {detected_via})", category="renpy_generator_rpa")

            # Phase 3-4 : TENTATIVE PRINCIPALE + FALLBACK
            log_message("INFO", "[Phase 3-4] Décompilation des .rpyc...", category="renpy_generator_rpa")
            
            # Collecte des fichiers .rpyc INCLUANT MAINTENANT le dossier tl/
            rpyc_files = []
            for root, dirs, files in os.walk(game_dir):
                # SUPPRESSION DE L'EXCLUSION : plus de if 'tl' in dirs: dirs.remove('tl')
                for f in files:
                    if f.lower().endswith('.rpyc'):
                        rpyc_files.append(os.path.join(root, f))
            
            log_message("INFO", f"Fichiers .rpyc trouvés (dossier game complet) : {len(rpyc_files)}", category="renpy_generator_rpa")
            
            converted_count = 0
            skipped_count = 0
            failed_count = 0
            
            # TENTATIVE 1 : Version primaire
            if rpyc_files:
                log_message("INFO", f"Tentative 1/2 : unrpyc {primary_version}", category="renpy_generator_rpa")
                if progress_callback:
                    progress_callback(40, f"Décompilation RPYC {primary_version}...")
                elif self.progress_callback:
                    self.progress_callback(40, f"Décompilation RPYC {primary_version}...")
                
                converted_count, skipped_count, failed_count = self._attempt_rpyc_decompilation(project_path, rpyc_files, primary_version, progress_callback)
                
                result['unrpyc_attempts'].append({
                    'version': primary_version, 'converted': converted_count,
                    'failed': failed_count, 'skipped': skipped_count
                })
                
                # TENTATIVE 2 : Fallback si échecs
                if failed_count > 0 and failed_count > converted_count:
                    log_message("ATTENTION", f"Nombreux échecs avec {primary_version} ({failed_count}/{len(rpyc_files)}). Tentative fallback...", category="renpy_generator_rpa")
                    
                    self._cleanup_tools_from_game_dir(project_path)
                    
                    log_message("INFO", f"Tentative 2/2 : unrpyc {fallback_version} (fallback)", category="renpy_generator_rpa")
                    if progress_callback:
                        progress_callback(60, f"Décompilation RPYC {fallback_version} (fallback)...")
                    elif self.progress_callback:
                        self.progress_callback(60, f"Décompilation RPYC {fallback_version} (fallback)...")
                    
                    converted_fallback, skipped_fallback, failed_fallback = self._attempt_rpyc_decompilation(project_path, rpyc_files, fallback_version, progress_callback)
                    
                    result['unrpyc_attempts'].append({
                        'version': fallback_version, 'converted': converted_fallback,
                        'failed': failed_fallback, 'skipped': skipped_fallback
                    })
                    
                    # Garder les meilleurs résultats
                    if converted_fallback > converted_count or failed_fallback < failed_count:
                        log_message("INFO", f"Fallback {fallback_version} plus efficace : {converted_fallback} convertis vs {converted_count}", category="renpy_generator_rpa")
                        converted_count = converted_fallback
                        skipped_count = skipped_fallback
                        failed_count = failed_fallback
            
            result['rpyc_converted'] = converted_count
            result['rpyc_skipped'] = skipped_count
            result['rpyc_failed'] = failed_count

            # Phase 5 : nettoyage
            log_message("INFO", "[Phase 5] Nettoyage des outils temporaires...", category="renpy_generator_rpa")
            self._cleanup_tools_from_game_dir(project_path)

            # Phase 6 : Suppression des .rpa extraits avec succès (SI DEMANDÉE)
            rpa_deleted_count = 0
            if delete_rpa_after and result['rpa_extracted']:
                log_message("INFO", "[Phase 6] Suppression des .rpa extraits avec succès...", category="renpy_generator_rpa")
                if progress_callback:
                    progress_callback(90, "Suppression des fichiers RPA...")
                elif self.progress_callback:
                    self.progress_callback(90, "Suppression des fichiers RPA...")
                
                for rpa in result['rpa_extracted']:
                    try:
                        if os.path.exists(rpa):
                            os.remove(rpa)
                            rpa_deleted_count += 1
                            log_message("DEBUG", f"RPA supprimé : {os.path.basename(rpa)}", category="renpy_generator_rpa")
                    except Exception as e:
                        warn = f"Échec suppression {os.path.basename(rpa)}: {e}"
                        result['warnings'].append(warn)
                        log_message("ATTENTION", warn, category="renpy_generator_rpa")
                
                log_message("INFO", f"{rpa_deleted_count} fichiers RPA supprimés", category="renpy_generator_rpa")
            else:
                if not delete_rpa_after:
                    log_message("DEBUG", "Suppression RPA désactivée par l'utilisateur", category="renpy_generator_rpa")
                elif not result['rpa_extracted']:
                    log_message("DEBUG", "Aucun RPA extrait avec succès à supprimer", category="renpy_generator_rpa")

            result['rpa_deleted_count'] = rpa_deleted_count
            
            # Évaluer le succès global
            total_time = time.time() - workflow_start_time
            
            if rpa_success_count > 0 or converted_count > 0 or len(result['rpa_extraction_failed']) == 0:
                result['success'] = True
                log_message("INFO", f"Décompilation terminée avec succès ! RPA: {rpa_success_count} extraites, RPYC: {converted_count} convertis, {skipped_count} ignorés, {failed_count} échecs", category="renpy_generator_rpa")
            else:
                result['success'] = False
                result['errors'].append("Toutes les extractions RPA ont échoué")
                log_message("ERREUR", "Décompilation échouée : aucun RPA extrait avec succès", category="renpy_generator_rpa")
            
            log_message("INFO", f"Temps total d'exécution : {total_time:.2f}s", category="renpy_generator_rpa")
            if progress_callback:
                progress_callback(100, "Décompilation terminée !")
            elif self.progress_callback:
                self.progress_callback(100, "Décompilation terminée !")

        except Exception as e:
            err = f"Erreur critique : {e}"
            result['errors'].append(err)
            log_message("ERREUR", err, category="renpy_generator_rpa")
        finally:
            try:
                self._cleanup_tools_from_game_dir(project_path)
            except Exception as cleanup_error:
                log_message("ATTENTION", f"Erreur lors du nettoyage final : {cleanup_error}", category="renpy_generator_rpa")

        return result
    
    def detect_renpy_version(self, project_path: str) -> Dict[str, str]:
        """
        Détecte la version de Ren'Py SEULEMENT si extraction RPA effectuée
        VERSION MODIFIÉE : Analyse complète du dossier game (y compris tl/)
        
        Args:
            project_path: Chemin vers le projet
            
        Returns:
            Dict avec unrpyc_version_needed, detected_via, version
        """
        # Ne pas détecter si extraction RPA pas encore faite
        if not self.rpa_extraction_done:
            return {'unrpyc_version_needed': 'v2', 'detected_via': 'default_pre_extraction', 'version': 'Unknown'}
        
        log_message("INFO", "Détection de la version de Ren'Py...", category="renpy_generator_rpa")
        
        game_dir = os.path.join(project_path, "game")
        
        # PRIORITÉ 1 : Analyser script_version.txt
        script_version_path = os.path.join(game_dir, "script_version.txt")
        
        if os.path.exists(script_version_path):
            try:
                with open(script_version_path, 'r', encoding='utf-8') as f:
                    version_content = f.read().strip()
                
                # Parsing robuste - Extraire tous les nombres du contenu
                import re
                numbers = re.findall(r'\d+', version_content)
                
                if numbers and len(numbers) >= 1:
                    try:
                        major_version = int(numbers[0])
                        
                        # Reconstruire la version complète pour l'affichage
                        if len(numbers) >= 3:
                            version_display = f"{numbers[0]}.{numbers[1]}.{numbers[2]}"
                        elif len(numbers) >= 2:
                            version_display = f"{numbers[0]}.{numbers[1]}"
                        else:
                            version_display = numbers[0]
                        
                        if major_version >= 8:
                            log_message("INFO", f"DÉTECTION RÉUSSIE: Version Ren'Py {version_display} → unrpyc v2", category="renpy_generator_rpa")
                            return {'unrpyc_version_needed': 'v2', 'detected_via': 'script_version', 'version': version_display}
                        else:
                            log_message("INFO", f"DÉTECTION RÉUSSIE: Version Ren'Py {version_display} → unrpyc v1", category="renpy_generator_rpa")
                            return {'unrpyc_version_needed': 'v1', 'detected_via': 'script_version', 'version': version_display}
                            
                    except ValueError:
                        log_message("ATTENTION", f"Erreur conversion version majeure depuis: {numbers}", category="renpy_generator_rpa")
                else:
                    log_message("ATTENTION", f"Aucun nombre trouvé dans script_version.txt: '{version_content}'", category="renpy_generator_rpa")
                        
            except Exception as e:
                log_message("ERREUR", f"Erreur lecture script_version.txt: {e}", category="renpy_generator_rpa")
        
        # FALLBACK : Analyse binaire des .rpyc
        if not os.path.isdir(game_dir):
            log_message("ATTENTION", "Dossier game/ absent. Utilisation d'unrpyc v2 par défaut.", category="renpy_generator_rpa")
            return {'unrpyc_version_needed': 'v2', 'detected_via': 'default', 'version': 'Unknown'}

        # Collecter les fichiers .rpyc INCLUANT MAINTENANT le dossier tl/
        rpyc_files = []
        for root, dirs, files in os.walk(game_dir):
            # SUPPRESSION DE L'EXCLUSION : plus de if 'tl' in dirs: dirs.remove('tl')
            for f in files:
                if f.lower().endswith('.rpyc'):
                    rpyc_files.append(os.path.join(root, f))
        
        if not rpyc_files:
            log_message("ATTENTION", "Aucun .rpyc trouvé. Utilisation d'unrpyc v2 par défaut.", category="renpy_generator_rpa")
            return {'unrpyc_version_needed': 'v2', 'detected_via': 'default', 'version': 'Unknown'}

        version_votes = {'v1': 0, 'v2': 0}
        files_analyzed = 0
        
        # Analyser jusqu'à 10 fichiers .rpyc pour la détection
        for rpyc_file in rpyc_files[:10]:
            try:
                with open(rpyc_file, 'rb') as f:
                    magic_bytes = f.read(4)
                    
                if len(magic_bytes) < 4:
                    continue
                    
                import struct
                version_int = struct.unpack("<I", magic_bytes)[0]
                
                is_v2 = version_int >= 0x80000000
                version_detected = 'v2' if is_v2 else 'v1'
                version_votes[version_detected] += 1
                files_analyzed += 1
                
            except Exception:
                continue

        if version_votes['v2'] > version_votes['v1']:
            log_message("INFO", "DÉTECTION BINAIRE: Version Ren'Py 8+ détectée → unrpyc v2", category="renpy_generator_rpa")
            return {'unrpyc_version_needed': 'v2', 'detected_via': 'binary_analysis', 'version': 'RenPy8+'}
        else:
            log_message("INFO", "DÉTECTION BINAIRE: Version Ren'Py 6/7 détectée → unrpyc v1", category="renpy_generator_rpa")
            return {'unrpyc_version_needed': 'v1', 'detected_via': 'binary_analysis', 'version': 'RenPy6/7'}
    
    def _extract_single_rpa(self, rpa_path: str, game_dir: str) -> bool:
        """
        Extrait un seul fichier RPA
        
        Args:
            rpa_path: Chemin vers le fichier RPA
            game_dir: Dossier game de destination
            
        Returns:
            True si succès
        """
        try:
            rpatool = os.path.join(self.rpatool_dir, "rpatool-master", "rpatool.py")
            
            if not os.path.exists(rpatool):
                log_message("ERREUR", f"rpatool.py non trouvé: {rpatool}", category="renpy_generator_rpa")
                return False
            
            python_exe = self.python_manager.get_best_python_for_task("rpatool")
            if not python_exe:
                log_message("ERREUR", "Aucun Python disponible pour rpatool", category="renpy_generator_rpa")
                return False
            
            return self._run_command_with_python(
                [rpatool, "-x", rpa_path, "-o", game_dir], 
                python_exe, 
                os.path.dirname(rpatool)
            )
            
        except Exception as e:
            log_message("ERREUR", f"Erreur extraction RPA {os.path.basename(rpa_path)}: {e}", category="renpy_generator_rpa")
            return False
    
    def _attempt_rpyc_decompilation(self, project_path: str, rpyc_files: List[str], unrpyc_version: str, 
                                progress_callback: Optional[Callable] = None) -> Tuple[int, int, int]:
        """
        Tente la décompilation des .rpyc avec une version spécifique d'unrpyc
        
        Args:
            project_path: Chemin vers le projet
            rpyc_files: Liste des fichiers RPYC
            unrpyc_version: Version unrpyc ("v1" ou "v2")
            progress_callback: Callback de progression
            
        Returns:
            Tuple (converted_count, skipped_count, failed_count)
        """
        # Placement des outils
        self._place_tools_in_game_dir(project_path, unrpyc_version)
        
        converted_count = 0
        skipped_count = 0
        failed_count = 0
        
        for i, rpyc in enumerate(rpyc_files, 1):
            if self.operation_cancelled:
                raise InterruptedError("Opération annulée")
            
            # Vérifier si le .rpy correspondant existe déjà    
            rpy_equivalent = rpyc.replace('.rpyc', '.rpy')
            if os.path.exists(rpy_equivalent):
                log_message("DEBUG", f"Skip ({i}/{len(rpyc_files)}): {os.path.basename(rpyc)} - .rpy existe déjà", category="renpy_generator_rpa")
                skipped_count += 1
                continue
            
            if progress_callback:
                progress_base = 40 if unrpyc_version == 'v2' else 50
                progress_callback(progress_base + (i * 20 // max(len(rpyc_files), 1)), 
                                f"Décompilation .rpyc {unrpyc_version} ({i}/{len(rpyc_files)})")
            elif self.progress_callback:
                progress_base = 40 if unrpyc_version == 'v2' else 50
                self.progress_callback(progress_base + (i * 20 // max(len(rpyc_files), 1)), 
                                f"Décompilation .rpyc {unrpyc_version} ({i}/{len(rpyc_files)})")
            
            log_message("DEBUG", f"Décompilation {unrpyc_version} ({i}/{len(rpyc_files)}): {os.path.basename(rpyc)}", category="renpy_generator_rpa")
            
            # Utiliser la version spécifiée pour la sélection Python
            python_exe = self.python_manager.get_best_python_for_task("unrpyc", project_path, unrpyc_version)
            if not python_exe:
                log_message("ERREUR", f"Aucun Python disponible pour unrpyc {unrpyc_version}", category="renpy_generator_rpa")
                failed_count += 1
                continue
            
            success = self._run_command_with_python(["unrpyc.py", rpyc], python_exe, project_path)
            
            if success:
                converted_count += 1
                log_message("DEBUG", f"Décompilation {os.path.basename(rpyc)} réussie", category="renpy_generator_rpa")
            else:
                failed_count += 1
                log_message("ATTENTION", f"Échec décompilation {os.path.basename(rpyc)}", category="renpy_generator_rpa")
        
        log_message("INFO", f"Résultats {unrpyc_version}: {converted_count} convertis, {skipped_count} ignorés, {failed_count} échecs", category="renpy_generator_rpa")
        return converted_count, skipped_count, failed_count
    
    def _place_tools_in_game_dir(self, project_path: str, unrpyc_version: str):
        """Copie le contenu du dossier unrpyc (v1 ou v2) directement dans le dossier racine du jeu"""
        src_dir = os.path.join(self.unrpyc_dir, unrpyc_version)  # v1 ou v2 spécifiquement
        dst_dir = project_path  # directement dans le dossier racine du jeu
        
        log_message("DEBUG", f"Placement des outils unrpyc {unrpyc_version} dans : {dst_dir}", category="renpy_generator_rpa")
        
        # Copier tous les fichiers du dossier v1 ou v2 dans le dossier racine du jeu
        for item in os.listdir(src_dir):
            src_item = os.path.join(src_dir, item)
            dst_item = os.path.join(dst_dir, item)
            
            if os.path.isfile(src_item):
                shutil.copy2(src_item, dst_item)
            elif os.path.isdir(src_item):
                if os.path.exists(dst_item):
                    shutil.rmtree(dst_item)
                shutil.copytree(src_item, dst_item)
        
        log_message("INFO", f"Outils unrpyc {unrpyc_version} copiés dans le dossier racine du jeu.", category="renpy_generator_rpa")
    
    def _cleanup_tools_from_game_dir(self, project_path: str):
        """Supprime TOUS les fichiers/dossiers unrpyc du dossier racine du jeu"""
        log_message("INFO", "Nettoyage des outils temporaires...", category="renpy_generator_rpa")
        
        # Liste des fichiers et dossiers à supprimer
        items_to_remove = [
            "unrpyc.py", "unrpyc.pyo", "unrpyc.pyc",
            "deobfuscate.py", "deobfuscate.pyo", "deobfuscate.pyc",
            "decompiler", "decompiler.py", "decompiler.pyo", "decompiler.pyc",
            "magic.py", "magic.pyo", "magic.pyc", "testcases",
            "un.rpyc", "un.rpy", "LICENSE", "README.md", "MANIFEST.in", "setup.py",
            "bintray-template.json", "make-bintray-json.sh",
            ".github", ".gitignore", ".gitmodules"
        ]
        
        files_removed = 0
        files_failed = 0
        
        for item in items_to_remove:
            item_path = os.path.join(project_path, item)
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                    files_removed += 1
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    files_removed += 1
            except Exception as e:
                # ⬆️ Sévérité ajustée : l’échec de suppression mérite un WARNING
                log_message("ATTENTION", f"Impossible de supprimer {item}: {e}", category="renpy_generator_rpa")
                files_failed += 1
        
        log_message("DEBUG", f"Nettoyage terminé: {files_removed} éléments supprimés, {files_failed} échecs", category="renpy_generator_rpa")
    
    def _run_command_with_python(self, command: List[str], python_exe: str, working_dir: str) -> bool:
        """
        Exécute une commande avec un Python spécifique et un chemin de travail sécurisé.
        """
        process = None
        try:
            final_working_dir = working_dir
            # Si on est sur Windows, on convertit le chemin en sa version "courte" (8.3)
            # pour éviter les problèmes avec les caractères spéciaux comme []
            if sys.platform == "win32":
                try:
                    # Préparation de l'appel à la fonction Windows GetShortPathNameW
                    _GetShortPathNameW = ctypes.windll.kernel32.GetShortPathNameW
                    _GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
                    _GetShortPathNameW.restype = wintypes.DWORD

                    output_buf_size = len(working_dir) + 100  # Buffer suffisant
                    output_buf = ctypes.create_unicode_buffer(output_buf_size)
                    
                    needed = _GetShortPathNameW(working_dir, output_buf, output_buf_size)
                    
                    # Si la conversion réussit, on utilise le nouveau chemin
                    if needed > 0:
                        final_working_dir = output_buf.value
                        log_message("DEBUG", f"Chemin converti en version courte (8.3) pour compatibilité : {final_working_dir}", category="renpy_generator_rpa")

                except Exception as e:
                    log_message("ATTENTION", f"Impossible de convertir le chemin en version courte, utilisation du chemin original. Erreur: {e}", category="renpy_generator_rpa")
                    # En cas d'erreur, on utilise le chemin original par sécurité
                    final_working_dir = working_dir

            # Environnement propre
            env = os.environ.copy()
            env.pop('PYTHONPATH', None)
            env.pop('PYTHONHOME', None)
            env['PYTHONDONTWRITEBYTECODE'] = '1'

            # Configuration Windows pour éviter les fenêtres CMD
            startupinfo = None
            creation_flags = 0
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW | subprocess.STARTF_USESTDHANDLES
                startupinfo.wShowWindow = subprocess.SW_HIDE
                creation_flags = subprocess.CREATE_NO_WINDOW

            # Construction et exécution de la commande
            full_command = [python_exe] + command
            log_message("DEBUG", f"Executing: {' '.join(full_command)} in {final_working_dir}", category="renpy_generator_rpa")

            process = subprocess.Popen(
                full_command, 
                cwd=final_working_dir,  # Utilisation du chemin sécurisé
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                encoding='utf-8', 
                errors='ignore', 
                startupinfo=startupinfo, 
                env=env,
                creationflags=creation_flags
            )
            
            # Attendre avec timeout
            try:
                stdout, stderr = process.communicate(timeout=600)
                return_code = process.returncode
            except subprocess.TimeoutExpired:
                log_message("ATTENTION", "Timeout pour la commande. Terminaison forcée...", category="renpy_generator_rpa")
                process.terminate()
                try:
                    stdout, stderr = process.communicate(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    stdout, stderr = process.communicate(timeout=2)
                return_code = process.returncode
            
            # Vérifier le résultat
            if return_code != 0:
                log_message("ATTENTION", f"La commande a échoué (code {return_code}). Stderr: {stderr[:300] if stderr else 'N/A'}", category="renpy_generator_rpa")
                return False
            else:
                log_message("DEBUG", "Commande réussie", category="renpy_generator_rpa")
                return True
                
        except Exception as e:
            log_message("ERREUR", f"Erreur lors de l'exécution : {e}", category="renpy_generator_rpa")
            return False
        finally:
            # Nettoyage final du processus
            if process and process.poll() is None:
                try:
                    process.terminate()
                    process.wait(timeout=3)
                except (subprocess.TimeoutExpired, Exception):
                    try:
                        process.kill()
                        process.wait(timeout=1)
                    except Exception:
                        log_message("ATTENTION", "Le processus pourrait être orphelin", category="renpy_generator_rpa")
    
    def build_custom_rpa_threaded(self, project_path: str, language: str = "french", archive_name: str = "french.rpa", 
                                output_dir: str = None, delete_source_after: bool = False,  # ✅ NOUVEAU PARAMÈTRE
                                progress_callback: Optional[Callable] = None,
                                status_callback: Optional[Callable] = None,
                                completion_callback: Optional[Callable] = None) -> threading.Thread:
        """
        Lance la construction RPA personnalisée en thread
        
        Args:
            project_path: Chemin vers le projet
            language: Langue source
            archive_name: Nom de l'archive
            output_dir: Dossier de sortie
            delete_source_after: Supprimer le dossier source après création RPA  # ✅ NOUVEAU
            progress_callback: Callback de progression
            status_callback: Callback de statut
            completion_callback: Callback de fin
            
        Returns:
            Thread d'exécution
        """
        def worker():
            start_time = time.time()
            try:
                self.current_project_path = project_path
                if status_callback:
                    status_callback("Préparation de la construction RPA personnalisée...")
                elif self.status_callback:
                    self.status_callback("Préparation de la construction RPA personnalisée...")
                    
                if progress_callback:
                    progress_callback(10, "Préparation de la construction RPA personnalisée...")
                elif self.progress_callback:
                    self.progress_callback(10, "Préparation de la construction RPA personnalisée...")
                
                # S'assurer que le nom a l'extension .rpa
                if not archive_name.endswith('.rpa'):
                    final_archive_name = f"{archive_name}.rpa"
                else:
                    final_archive_name = archive_name
                
                result = self.rpa_builder.build_custom_translation_rpa(
                    project_path, 
                    language, 
                    final_archive_name,
                    output_dir,
                    delete_source_after,  # ✅ TRANSMETTRE le nouveau paramètre
                    progress_callback or self.progress_callback
                )
                result['execution_time'] = time.time() - start_time
                
                # Créer le résumé pour le popup
                if result['success']:
                    archives_info = []
                    for archive in result['archives_created']:
                        archives_info.append(f"Archive {archive['name']}: {archive['files_count']} fichiers")
                    
                    # ✅ AJOUTER info suppression du source dans le résumé
                    if result.get('source_deleted'):
                        archives_info.append(f"Dossier source supprimé: {result['deleted_source_path']}")
                    
                    result['summary'] = {
                        'rpa_build': f"Construction RPA {language} réussie",
                        'archives': archives_info,
                        'execution_time': f"Temps d'exécution: {result['execution_time']:.1f}s"
                    }
                else:
                    result['summary'] = {
                        'rpa_build': f"Échec de la construction RPA {language}",
                        'errors': result.get('errors', [])
                    }
                
                if progress_callback:
                    progress_callback(100, "Construction RPA terminée")
                elif self.progress_callback:
                    self.progress_callback(100, "Construction RPA terminée")
                
                if not self.operation_cancelled and completion_callback:
                    completion_callback(result['success'], result)
                elif not self.operation_cancelled and self.completion_callback:
                    self.completion_callback(result['success'], result)
                    
            except Exception as e:
                if not self.operation_cancelled:
                    error_result = {
                        'success': False,
                        'errors': [f"Erreur inattendue dans le thread RPA: {e}"],
                        'execution_time': time.time() - start_time,
                        'summary': {
                            'rpa_build': "Erreur critique lors de la construction RPA",
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
                        'errors': ["Opération annulée."],
                        'execution_time': time.time() - start_time,
                        'summary': {
                            'rpa_build': "Construction RPA annulée par l'utilisateur"
                        }
                    }
                    if completion_callback:
                        completion_callback(False, cancelled_result)
                    elif self.completion_callback:
                        self.completion_callback(False, cancelled_result)
                self.current_project_path = None
        
        self.operation_cancelled = False
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        
        log_message("INFO", f"Construction RPA personnalisée lancée: {language} -> {archive_name}", category="renpy_generator_rpa")
        return thread
    
    def cancel_operation(self):
        """Annule l'opération en cours"""
        self.operation_cancelled = True
        log_message("INFO", "Annulation demandée par l'utilisateur.", category="renpy_generator_rpa")
    
    def cleanup(self):
        """Nettoie les ressources"""
        try:
            self.python_manager.cleanup()
            self.sdk_manager.cleanup()
            log_message("DEBUG", "RPAExtractionBusiness nettoyé", category="renpy_generator_rpa")
        except Exception as e:
            log_message("ATTENTION", f"Erreur lors du nettoyage: {e}", category="renpy_generator_rpa")


class RPABuilder:
    """
    Constructeur d'archives RPA basé sur la logique Ren'Py
    """
    def __init__(self):
        self.archives_created = []
    
    def build_custom_translation_rpa(self, project_path: str, language: str = "french", archive_name: str = "french.rpa", 
                                    output_dir: str = None, delete_source_after: bool = False,  # ✅ NOUVEAU PARAMÈTRE
                                    progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Construit une archive RPA personnalisée avec backup automatique et suppression optionnelle du source"""
        result = {'success': False, 'errors': [], 'warnings': [], 'archives_created': [], 'backup_info': None,
                'source_deleted': False, 'deleted_source_path': None}  # ✅ NOUVELLES CLÉS
        
        try:
            # Construire les chemins
            tl_folder = os.path.join(project_path, "game", "tl")
            language_folder = os.path.join(tl_folder, language)
            
            if not os.path.exists(language_folder):
                result['errors'].append(f"Dossier de traduction {language} introuvable: game/tl/{language}/")
                return result
            
            # Dossier de sortie par défaut
            if not output_dir:
                output_dir = os.path.join(project_path, "game")
            
            # S'assurer automatiquement que le nom se termine par .rpa
            if not archive_name.endswith('.rpa'):
                archive_name = f"{archive_name}.rpa"
            
            # Chemin de l'archive de sortie
            archive_path = os.path.join(output_dir, archive_name)
            
            log_message("INFO", f"Construction RPA personnalisée: {language} -> {archive_name}", category="renpy_generator_rpa")
            log_message("DEBUG", f"Source: {language_folder}", category="renpy_generator_rpa")
            log_message("DEBUG", f"Archive: {archive_path}", category="renpy_generator_rpa")
            
            # NOUVEAU : Backup des fichiers avant construction RPA
            if progress_callback:
                progress_callback(20, "Sauvegarde des fichiers sources...")
            
            backup_result = self._backup_files_before_rpa_build(language_folder, language)
            
            if backup_result['success']:
                result['backup_info'] = backup_result
                log_message("INFO", f"Backup RPA: {backup_result['backed_up_count']} fichiers sauvegardés", category="renpy_generator_rpa")
            else:
                result['warnings'].extend(backup_result['warnings'])
            
            if progress_callback:
                progress_callback(50, f"Construction de l'archive {archive_name}...")
            
            # Créer l'archive avec la structure préservée
            # archive_result = self.create_custom_rpa_archive(language, language_folder, archive_path)
            archive_result = self.create_custom_rpa_archive(language, language_folder, archive_path,
                                                            pickle_protocol=2)


            if archive_result['success']:
                result['success'] = True
                result['archives_created'].append({
                    'name': archive_name,
                    'path': archive_path,
                    'files_count': archive_result['files_archived']
                })
                log_message("INFO", f"Archive {language} créée: {archive_result['files_archived']} fichiers", category="renpy_generator_rpa")
                
                # ✅ NOUVELLE LOGIQUE : Suppression du dossier source après succès
                if delete_source_after:
                    if progress_callback:
                        progress_callback(80, "Suppression du dossier source...")
                    
                    try:
                        log_message("INFO", f"Suppression du dossier source: {language_folder}", category="renpy_generator_rpa")
                        
                        # Vérifier que l'archive existe bien avant de supprimer le source
                        if os.path.exists(archive_path) and os.path.getsize(archive_path) > 0:
                            import shutil
                            shutil.rmtree(language_folder)
                            
                            result['source_deleted'] = True
                            result['deleted_source_path'] = language_folder
                            log_message("INFO", f"Dossier source supprimé avec succès: {language}", category="renpy_generator_rpa")
                        else:
                            warning = "Archive invalide - suppression du source annulée"
                            result['warnings'].append(warning)
                            log_message("ATTENTION", warning, category="renpy_generator_rpa")
                            
                    except Exception as e:
                        warning = f"Échec suppression dossier source: {e}"
                        result['warnings'].append(warning)
                        log_message("ATTENTION", warning, category="renpy_generator_rpa")
            else:
                result['errors'].extend(archive_result['errors'])
                result['warnings'].extend(archive_result['warnings'])
            
        except Exception as e:
            result['errors'].append(f"Erreur construction RPA {language}: {e}")
            log_message("ERREUR", f"Erreur build custom RPA: {e}", category="renpy_generator_rpa")
        
        return result

    def _backup_files_before_rpa_build(self, source_folder: str, language: str) -> Dict[str, Any]:
        """Sauvegarde tous les fichiers qui seront inclus dans le RPA en utilisant une archive ZIP"""
        result = {'success': True, 'warnings': [], 'backed_up_count': 0, 'backup_paths': []}
        
        try:
            # Import ici pour éviter les dépendances circulaires
            from core.models.backup.unified_backup_manager import UnifiedBackupManager, BackupType
            
            backup_manager = UnifiedBackupManager()
            
            # Patterns basés sur la config build française (identiques à _add_files_to_custom_archive)
            include_patterns = [
                "**.rpy",  # Fichiers source
                "**.rpyc",  # Fichiers binaire source            
                "**.jpg", "**.png", "**.webp",  # Images
                "**.ogg", "**.mp3",  # Sons et musique
                "**.ttf", "**.otf",  # Polices
                "**.webm"  # Vidéos
            ]
            
            exclude_patterns = [
                "**~", "**.bak", "**/.**", "**/#**", "**/thumbs.db",
                "**.psd", "**.txt"  # Sources exclues
            ]
            
            log_message("INFO", f"Début backup ZIP des fichiers pour RPA {language}", category="renpy_generator_rpa")
            
            # Créer une sauvegarde ZIP complète du dossier source
            backup_result = backup_manager.create_zip_backup(
                source_folder,
                BackupType.RPA_BUILD,
                f"Sauvegarde ZIP avant construction RPA {language}",
                include_patterns=include_patterns,
                exclude_patterns=exclude_patterns
            )
            
            if backup_result['success']:
                result['backed_up_count'] = backup_result['files_count']
                result['backup_paths'].append(backup_result['backup_path'])
                result['total_size'] = backup_result['total_size']
                log_message("INFO", f"Backup ZIP créé: {backup_result['files_count']} fichiers dans {backup_result['backup_path']}", category="renpy_generator_rpa")
            else:
                warning = f"Échec backup ZIP: {backup_result.get('error', 'erreur inconnue')}"
                result['warnings'].append(warning)
                log_message("ATTENTION", warning, category="renpy_generator_rpa")
            
            log_message("INFO", f"Backup ZIP RPA terminé: {result['backed_up_count']} fichiers sauvegardés, {len(result['warnings'])} avertissements", category="renpy_generator_rpa")
            
            # Si aucun fichier n'a été sauvegardé, c'est une situation normale possible
            if result['backed_up_count'] == 0:
                log_message("INFO", "Aucun fichier à sauvegarder (dossier vide ou aucun fichier correspondant aux critères)", category="renpy_generator_rpa")
            
        except Exception as e:
            result['success'] = False
            error_msg = f"Erreur backup ZIP RPA: {e}"
            result['warnings'].append(error_msg)
            log_message("ERREUR", error_msg, category="renpy_generator_rpa")
        
        return result

    def create_custom_rpa_archive(self, language: str, source_folder: str, output_path: str,
                                pickle_protocol: int = 2) -> Dict[str, Any]:
        """
        Crée une archive RPA personnalisée (tl/{language}/) avec protocole pickle contrôlé.
        """
        result = {'success': False, 'errors': [], 'warnings': [], 'files_archived': 0, 'archive_path': None}
        try:
            log_message("INFO", f"Création de l'archive RPA personnalisée: {os.path.basename(output_path)}", category="renpy_generator_rpa")

            if not os.path.exists(source_folder):
                result['errors'].append(f"Dossier source introuvable: {source_folder}")
                return result

            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # ⬇️ passer le protocole choisi
            archiver = self._create_simple_archiver(output_path, pickle_protocol)

            files_added = self._add_files_to_custom_archive(archiver, source_folder, language)

            archiver.close()

            if files_added > 0:
                result['success'] = True
                result['files_archived'] = files_added
                result['archive_path'] = output_path
                self.archives_created.append(output_path)
                log_message("INFO", f"Archive RPA créée: {files_added} fichiers archivés", category="renpy_generator_rpa")
            else:
                result['warnings'].append("Aucun fichier trouvé à archiver")
                log_message("ATTENTION", "Aucun fichier trouvé pour l'archive", category="renpy_generator_rpa")

        except Exception as e:
            result['errors'].append(f"Erreur création archive: {e}")
            log_message("ERREUR", f"Erreur création RPA: {e}", category="renpy_generator_rpa")

        return result
    
    def _create_simple_archiver(self, output_path: str, pickle_protocol: int = 2):
        """Crée un archiver RPA-3.0 avec protocole pickle contrôlé (par défaut 2 pour compat Ren'Py 6/7)."""
        import zlib
        from pickle import dumps

        class SimpleRPAArchiver:
            def __init__(self, filename):
                self.f = open(filename, "wb")
                self.index = {}
                self.key = 0x42424242
                self._protocol = pickle_protocol  # <- protocole utilisé pour l'index

                # En-tête RPA-3.0 standard
                padding = b"RPA-3.0 XXXXXXXXXXXXXXXX XXXXXXXX\n"
                self.f.write(padding)

            def add(self, name, path):
                """Ajoute un fichier à l'archive."""
                self.index[name] = []

                with open(path, "rb") as df:
                    data = df.read()
                dlen = len(data)

                # Padding décoratif (optionnel)
                self.f.write(b"Made with RenExtract.")

                offset = self.f.tell()
                self.f.write(data)

                # Entrée d'index chiffrée par XOR (format Ren'Py)
                self.index[name].append((offset ^ self.key, dlen ^ self.key, b""))

            def close(self):
                """Finalise l'archive en écrivant l'index compressé (pickle protocol=2 par défaut)."""
                indexoff = self.f.tell()
                self.f.write(zlib.compress(dumps(self.index, self._protocol)))
                self.f.seek(0)
                self.f.write(b"RPA-3.0 %016x %08x\n" % (indexoff, self.key))
                self.f.close()

        return SimpleRPAArchiver(output_path)

    def _detect_target_pickle_protocol(self, project_path: str) -> int:
        """
        Renvoie 2 pour Ren'Py 6/7 (Py2.7) ; 4 pour Ren'Py 8+ (Py3.x).
        Détection via script_version.txt puis, en fallback, analyse binaire de quelques .rpyc.
        """
        try:
            game_dir = os.path.join(project_path, "game")
            # 1) script_version.txt
            sv = os.path.join(game_dir, "script_version.txt")
            if os.path.exists(sv):
                with open(sv, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                major = content.split(",")[0].strip()
                if major.isdigit() and int(major) < 8:
                    return 2
                return 4

            # 2) Fallback : lecture des 4 octets magiques de quelques .rpyc
            import struct
            for root, _, files in os.walk(game_dir):
                for fn in files:
                    if fn.lower().endswith(".rpyc"):
                        with open(os.path.join(root, fn), "rb") as fh:
                            magic = fh.read(4)
                            if len(magic) >= 4:
                                ver = struct.unpack("<I", magic)[0]
                                return 4 if ver >= 0x80000000 else 2

            # 3) Défaut raisonnable : 4 (compatible Py3.4+)
            return 4
        except Exception:
            return 4

    def _add_files_to_custom_archive(self, archiver, source_folder: str, language: str) -> int:
        """
        Ajoute les fichiers à l'archive personnalisée en préservant la structure tl/{language}/
        """
        files_added = 0
        
        # Patterns basés sur la config build française (adaptés)
        include_patterns = [
            "**.rpy",  # Fichiers source
            "**.rpyc",  # Fichiers binaire source            
            "**.jpg", "**.png", "**.webp",  # Images
            "**.ogg", "**.mp3",  # Sons et musique
            "**.ttf", "**.otf",  # Polices
            "**.webm"  # Vidéos
        ]
        
        exclude_patterns = [
            "**~", "**.bak", "**/.**", "**/#**", "**/thumbs.db",
            "**.psd", "**.txt"  # Sources exclues
        ]
        
        # Parcourir récursivement le dossier source
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Calculer le chemin relatif depuis le dossier source
                relative_path = os.path.relpath(file_path, source_folder)
                
                # Créer le chemin dans l'archive en préservant tl/{language}/
                archive_internal_path = f"tl/{language}/{relative_path}".replace("\\", "/")
                
                # Vérifier les patterns d'inclusion/exclusion
                if self._should_include_file(file, include_patterns, exclude_patterns):
                    try:
                        archiver.add(archive_internal_path, file_path)
                        files_added += 1
                        log_message("DEBUG", f"Ajouté: {archive_internal_path} ← {file}", category="renpy_generator_rpa")
                    except Exception as e:
                        log_message("ATTENTION", f"Erreur ajout {file}: {e}", category="renpy_generator_rpa")
        
        return files_added
    
    def _should_include_file(self, filename: str, include_patterns: list, exclude_patterns: list) -> bool:
        """Vérifie si un fichier doit être inclus selon les patterns"""
        import fnmatch
        
        # Vérifier d'abord les exclusions
        for pattern in exclude_patterns:
            if fnmatch.fnmatch(filename.lower(), pattern.replace("**", "*")):
                return False
        
        # Puis les inclusions
        for pattern in include_patterns:
            if fnmatch.fnmatch(filename.lower(), pattern.replace("**", "*")):
                return True
        
        return False
