# core/file_manager.py
# File Management Module
# Created for RenExtract 

"""
Module de gestion des fichiers et opérations système
"""

import os
import sys
import subprocess
import glob
import json
import time
import tkinter as tk
from pathlib import Path
from typing import List, Dict, Optional, Any
from tkinter import filedialog, messagebox
from infrastructure.config.config import config_manager
from infrastructure.config.constants import FOLDERS
from infrastructure.logging.logging import log_message

# Fonction show_translated_messagebox déplacée vers utils/unified_functions.py

class FileManager:
    """Gestionnaire de fichiers avec pattern Singleton thread-safe"""
    
    _instance = None
    _lock = None
    
    def __new__(cls):
        if cls._instance is None:
            if cls._lock is None:
                import threading
                cls._lock = threading.Lock()
            
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.is_folder_mode = False
        self.current_file_index = 0
        self.total_files = 0
        self.folder_files = []
        self.folder_path = None
        self.last_directory = ""
        
        self._load_config()
        
        self._initialized = True
    
    def _load_config(self):
        """Charge la configuration depuis le gestionnaire centralisé"""
        self.last_directory = config_manager.get('last_directory', '')

    def has_next_file(self):
        return self.is_folder_mode and self.folder_files and (self.current_file_index + 1) < len(self.folder_files)

    def advance_to_next_file(self):
        if not self.has_next_file():
            return None
        
        self.current_file_index += 1
        if self.current_file_index < len(self.folder_files):
            next_file = self.folder_files[self.current_file_index]
            remaining = len(self.folder_files) - self.current_file_index - 1
            
            log_message("INFO", f"Avancement au fichier suivant: {next_file} (index {self.current_file_index}, {remaining} restants)", category="navigation")
            
            return {
                'file': next_file,
                'remaining': remaining,
                'current_index': self.current_file_index,
                'total_files': len(self.folder_files)
            }
        return None

    def _save_config(self):
        config_manager.set('last_directory', self.last_directory)
        config_manager.save_config()

    def open_single_file(self):
        try:
            self.last_directory = config_manager.get('last_directory', self.last_directory)
            filepath = filedialog.askopenfilename(
                title="Ouvrir un fichier Ren'Py",
                filetypes=[("Fichiers Ren'Py", '*.rpy'), ("Tous les fichiers", '*.*')],
                initialdir=self.last_directory if self.last_directory else None
            )
            if filepath:
                self.last_directory = str(Path(filepath).parent)
                self._save_config()
                self.is_folder_mode = False
                self.current_file_index = 0
                self.total_files = 0
                self.folder_files = []
                self.folder_path = None
                log_message("INFO", f"Fichier unique ouvert: {filepath}", category="file_io")
                return filepath
            return None
        except Exception as e:
            log_message("ERREUR", "Erreur lors de l'ouverture du fichier unique", e, category="file_io")
            return None

    def open_folder(self):
        try:
            self.last_directory = config_manager.get('last_directory', self.last_directory)
            folder_path = filedialog.askdirectory(
                title="Sélectionner un dossier de traductions",
                initialdir=self.last_directory if self.last_directory else None
            )
            if not folder_path:
                return None
            
            self.last_directory = folder_path
            self._save_config()
            rpy_files = self._find_rpy_files_recursive(folder_path)
            if not rpy_files:
                log_message("ATTENTION", f"Aucun fichier .rpy trouvé dans {folder_path} et ses sous-dossiers", category="file_search")
                return None
            
            self.is_folder_mode = True
            self.folder_path = folder_path
            self.folder_files = rpy_files
            self.total_files = len(rpy_files)
            self.current_file_index = 0
            log_message("INFO", f"Mode dossier activé: {len(rpy_files)} fichiers trouvés dans {folder_path} et ses sous-dossiers", category="file_search")
            return {
                'folder_path': folder_path,
                'files': rpy_files,
                'total_files': len(rpy_files),
                'current_file_index': 0,
                'remaining': len(rpy_files) - 1
            }
        except Exception as e:
            log_message("ERREUR", "Erreur lors de l'ouverture du dossier", e, category="file_search")
            return None

    def _find_rpy_files_recursive(self, folder_path):
        try:
            rpy_files = []
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith('.rpy'):
                        rpy_files.append(os.path.join(root, file))
            rpy_files.sort()
            log_message("INFO", f"Recherche récursive: {len(rpy_files)} fichiers .rpy trouvés dans {folder_path}", category="file_search")
            return rpy_files
        except Exception as e:
            log_message("ERREUR", f"Erreur lors de la recherche récursive dans {folder_path}", e, category="file_search")
            return []

    def get_next_file(self):
        if not self.is_folder_mode or not self.folder_files:
            return None
        if self.current_file_index >= len(self.folder_files):
            return None
        next_file = self.folder_files[self.current_file_index]
        remaining = len(self.folder_files) - self.current_file_index - 1
        log_message("INFO", f"Fichier suivant ouvert: {next_file} ({remaining} restants)", category="navigation")
        return {
            'file': next_file,
            'remaining': remaining,
            'current_index': self.current_file_index,
            'total_files': len(self.folder_files)
        }

    def load_file_content(self, filepath):
        import time
        start_time = time.time()
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.readlines()
            elapsed_time = time.time() - start_time
            log_message("INFO", f"Fichier chargé: {len(content)} lignes - {filepath} en {elapsed_time:.2f}s", category="file_io")
            return content
        except UnicodeDecodeError:
            try:
                with open(filepath, 'r', encoding='latin-1') as f:
                    content = f.readlines()
                log_message("ATTENTION", f"Fichier chargé avec encodage latin-1: {filepath}", category="file_io")
                return content
            except Exception as e:
                log_message("ERREUR", f"Impossible de charger le fichier {filepath}", e, category="file_io")
                return None
        except Exception as e:
            log_message("ERREUR", f"Impossible de charger le fichier {filepath}", e, category="file_io")
            return None

    def save_project_info(self, project_key, info):
        try:
            project_file = Path(FOLDERS["configs"]) / f"project_{project_key}.json"
            project_file.parent.mkdir(parents=True, exist_ok=True)
            with open(project_file, 'w', encoding='utf-8') as f:
                json.dump(info, f, ensure_ascii=False, indent=2)
            log_message("INFO", f"Projet enregistré: {project_key}", category="project")
        except Exception as e:
            log_message("ATTENTION", f"Erreur sauvegarde projet: {e}", category="project")

    def load_project_info(self, project_key):
        try:
            project_file = Path(FOLDERS["configs"]) / f"project_{project_key}.json"
            if project_file.exists():
                with open(project_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            log_message("ATTENTION", f"Erreur chargement projet: {e}", category="project")
            return None

    def create_directory(self, directory):
        try:
            os.makedirs(directory, exist_ok=True)
            log_message("INFO", f"Dossier créé: {directory}", category="file_io")
            return True
        except Exception as e:
            log_message("ATTENTION", f"Impossible de créer le dossier {directory}", e, category="file_io")
            return False

    def reset(self):
        self.is_folder_mode = False
        self.current_file_index = 0
        self.total_files = 0
        self.folder_files = []
        self.folder_path = None
        log_message("INFO", "FileManager réinitialisé", category="reset")

class FileOpener:
    @staticmethod
    def open_files(file_list, auto_open_enabled=True):
        if not auto_open_enabled:
            log_message("INFO", "Auto-ouverture désactivée - Fichiers non ouverts automatiquement", category="auto_open")
            return
        if not file_list:
            return
        try:
            for filepath in file_list:
                if filepath and os.path.exists(filepath):
                    FileOpener._open_single_file(filepath)
            log_message("INFO", f"Fichiers ouverts automatiquement: {len(file_list)}", category="auto_open")
        except Exception as e:
            log_message("ATTENTION", "Impossible d'ouvrir automatiquement les fichiers", e, category="auto_open")
    
    @staticmethod
    def _open_single_file(filepath):
        try:
            if os.name == 'nt':
                os.startfile(filepath)
            elif sys.platform == 'darwin':
                subprocess.call(['open', filepath])
            else:
                subprocess.call(['xdg-open', filepath])
        except Exception as e:
            log_message("ATTENTION", f"Impossible d'ouvrir {filepath}", e, category="auto_open")

class ProjectManager:
    def __init__(self):
        self.active_projects = {}
    
    def register_project(self, filepath, project_data):
        project_key = os.path.dirname(filepath)
        self.active_projects[project_key] = {
            'main_file': filepath,
            'data': project_data,
            'timestamp': os.path.getmtime(filepath)
        }
        log_message("INFO", f"Projet enregistré: {project_key}", category="project")
    
    def cleanup_old_projects(self, max_age_hours=24):
        current_time = time.time()
        cutoff_time = current_time - (max_age_hours * 3600)
        to_remove = [k for k, v in self.active_projects.items() if v['timestamp'] < cutoff_time]
        for project_key in to_remove:
            del self.active_projects[project_key]
        if to_remove:
            log_message("INFO", f"Nettoyage: {len(to_remove)} anciens projets supprimés", category="project")

class TempFileManager:
    @staticmethod
    def list_temp_files(pattern="*_mapping.txt"):
        try:
            temp_files = glob.glob(pattern)
            temp_files.extend(glob.glob("*_positions.json"))
            temp_files.extend(glob.glob("*_asterix_mapping.txt"))
            temp_files.extend(glob.glob("*_empty_mapping.txt"))
            return list(set(temp_files))
        except Exception as e:
            log_message("ATTENTION", "Erreur lors de la liste des fichiers temporaires", e, category="cleanup")
            return []
    
    @staticmethod
    def cleanup_temp_files(file_base=None):
        try:
            if file_base:
                patterns = [
                    f"{file_base}_mapping.txt",
                    f"{file_base}_positions.json", 
                    f"{file_base}_asterix_mapping.txt",
                    f"{file_base}_empty_mapping.txt"
                ]
            else:
                patterns = [
                    "*_mapping.txt",
                    "*_positions.json",
                    "*_asterix_mapping.txt", 
                    "*_empty_mapping.txt"
                ]
            cleaned_files = []
            for pattern in patterns:
                for file in glob.glob(pattern):
                    try:
                        os.remove(file)
                        cleaned_files.append(file)
                    except:
                        pass
            if cleaned_files:
                log_message("INFO", f"Fichiers temporaires nettoyés: {len(cleaned_files)}", category="cleanup")
            return cleaned_files
        except Exception as e:
            log_message("ATTENTION", "Erreur lors du nettoyage des fichiers temporaires", e, category="cleanup")
            return []

def get_file_info(filepath):
    try:
        stats = os.stat(filepath)
        return {
            'size': stats.st_size,
            'size_mb': round(stats.st_size / (1024 * 1024), 2),
            'modified': stats.st_mtime,
            'created': stats.st_ctime,
            'exists': True,
            'readable': os.access(filepath, os.R_OK),
            'writable': os.access(filepath, os.W_OK)
        }
    except Exception as e:
        return {'exists': False, 'error': str(e)}

file_manager = FileManager()
project_manager = ProjectManager()
