# infrastructure/helpers/file_utils.py
# Utilitaires pour la gestion des fichiers et dossiers
# Created for RenExtract

"""
Utilitaires pour la gestion des fichiers et dossiers
- Ouverture de dossiers dans l'explorateur
- Gestion des chemins
- Fonctions transverses
"""

import os
import subprocess
import platform
from infrastructure.logging.logging import log_message

def open_folder_in_explorer(folder_path):
    """
    Ouvre un dossier dans l'explorateur de fichiers du système
    
    Args:
        folder_path (str): Chemin vers le dossier à ouvrir
        
    Returns:
        bool: True si l'ouverture a réussi, False sinon
    """
    try:
        if not os.path.exists(folder_path):
            log_message("ATTENTION", f"Dossier inexistant: {folder_path}", category="file_utils")
            return False
        
        # Normaliser le chemin
        normalized_path = os.path.normpath(folder_path)
        
        system = platform.system()
        
        if system == "Windows":
            # Windows
            subprocess.Popen(['explorer', normalized_path], shell=True)
        elif system == "Darwin":
            # macOS
            subprocess.Popen(['open', normalized_path])
        else:
            # Linux et autres
            subprocess.Popen(['xdg-open', normalized_path])
        
        log_message("INFO", f"Dossier ouvert dans l'explorateur: {normalized_path}", category="file_utils")
        return True
        
    except Exception as e:
        log_message("ERREUR", f"Erreur ouverture dossier {folder_path}: {e}", category="file_utils")
        return False

def open_file_in_explorer(file_path):
    """
    Ouvre un fichier dans l'explorateur de fichiers du système
    (sélectionne le fichier et ouvre son dossier parent)
    
    Args:
        file_path (str): Chemin vers le fichier
        
    Returns:
        bool: True si l'ouverture a réussi, False sinon
    """
    try:
        if not os.path.exists(file_path):
            log_message("ATTENTION", f"Fichier inexistant: {file_path}", category="file_utils")
            return False
        
        # Normaliser le chemin
        normalized_path = os.path.normpath(file_path)
        
        system = platform.system()
        
        if system == "Windows":
            # Windows - sélectionne le fichier
            subprocess.Popen(['explorer', '/select,', normalized_path], shell=True)
        elif system == "Darwin":
            # macOS - révèle le fichier dans le Finder
            subprocess.Popen(['open', '-R', normalized_path])
        else:
            # Linux - ouvre le dossier parent
            parent_dir = os.path.dirname(normalized_path)
            subprocess.Popen(['xdg-open', parent_dir])
        
        log_message("INFO", f"Fichier révélé dans l'explorateur: {normalized_path}", category="file_utils")
        return True
        
    except Exception as e:
        log_message("ERREUR", f"Erreur révélation fichier {file_path}: {e}", category="file_utils")
        return False

def get_backup_folder_path():
    """
    Retourne le chemin vers le dossier de sauvegardes
    
    Returns:
        str: Chemin vers le dossier de sauvegardes
    """
    from infrastructure.config.constants import FOLDERS
    
    backup_folder = FOLDERS.get("backup")
    if backup_folder and os.path.exists(backup_folder):
        return backup_folder
    
    # Fallback : dossier par défaut
    from infrastructure.config.constants import get_executable_dir
    default_backup = os.path.join(get_executable_dir(), ".renextract_tools", "backups")
    return default_backup
