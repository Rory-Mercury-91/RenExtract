# core/tools/downloader.py
# Module de téléchargement universel pour RenExtract
# Extrait de translation_generator.py

"""
Module de téléchargement et extraction d'archives
- Téléchargement de fichiers depuis URLs
- Extraction d'archives ZIP
- Gestion des erreurs et timeouts
- Utilisé par l'extraction RPA, le nettoyage, etc.
"""

import os
import zipfile
import requests
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any
from infrastructure.logging.logging import log_message


class UniversalDownloader:
    """Gestionnaire universel de téléchargements et extractions"""
    
    def __init__(self):
        """Initialise le téléchargeur"""
        self.session = requests.Session()
        # Configuration des timeouts et retry
        self.session.timeout = 60
        self.temp_dir = None
    
    def download_and_extract_zip(self, url: str, dest_path: str, zip_root_dir: str, 
                                force_redownload: bool = False) -> Dict[str, Any]:
        """
        Télécharge et extrait une archive ZIP si elle n'existe pas
        
        Args:
            url: URL de l'archive à télécharger
            dest_path: Chemin de destination pour l'extraction
            zip_root_dir: Nom du dossier racine dans l'archive
            force_redownload: Force le re-téléchargement même si le dossier existe
            
        Returns:
            Dict avec success, error, dest_path
        """
        result = {'success': False, 'error': None, 'dest_path': dest_path}
        
        try:
            # Vérifier si le dossier existe déjà
            if os.path.exists(dest_path) and not force_redownload:
                log_message("INFO", f"L'outil '{os.path.basename(dest_path)}' existe déjà.", category="download_zip")
                result['success'] = True
                return result
            
            # Créer le répertoire parent si nécessaire
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            # Préparer les chemins temporaires
            temp_zip_path = os.path.join(tempfile.gettempdir(), "download_temp.zip")
            temp_extract_path = os.path.join(tempfile.gettempdir(), "extract_temp")
            
            try:
                log_message("INFO", f"Téléchargement depuis {url}...", category="download_zip")
                
                # Télécharger le fichier
                response = self.session.get(url, timeout=120)
                response.raise_for_status()
                
                # Sauvegarder temporairement
                with open(temp_zip_path, 'wb') as f:
                    f.write(response.content)
                
                log_message("INFO", f"Extraction de l'archive ({len(response.content)/1024/1024:.1f} MB)...", category="download_zip")
                
                # Extraire l'archive
                with zipfile.ZipFile(temp_zip_path) as z:
                    z.extractall(temp_extract_path)
                
                # Déplacer le contenu vers la destination finale
                source_dir = os.path.join(temp_extract_path, zip_root_dir)
                if os.path.exists(source_dir):
                    # Si le dossier de destination existe, le supprimer d'abord
                    if os.path.exists(dest_path):
                        shutil.rmtree(dest_path)
                    
                    shutil.move(source_dir, dest_path)
                    result['success'] = True
                    log_message("INFO", f"Outil installé avec succès dans : {os.path.basename(dest_path)}", category="download_zip")
                else:
                    result['error'] = f"Le dossier '{zip_root_dir}' n'a pas été trouvé dans l'archive."
                    log_message("ERREUR", result['error'], category="download_zip")
                
            finally:
                # Nettoyer les fichiers temporaires
                self._cleanup_temp_files([temp_zip_path, temp_extract_path])
                
        except requests.exceptions.RequestException as e:
            result['error'] = f"Erreur de téléchargement : {e}"
            log_message("ERREUR", result['error'], category="download_zip")
        except zipfile.BadZipFile as e:
            result['error'] = f"Archive ZIP corrompue : {e}"
            log_message("ERREUR", result['error'], category="download_zip")
        except Exception as e:
            result['error'] = f"Erreur inattendue : {e}"
            log_message("ERREUR", result['error'], category="download_zip")
        
        return result
    
    def download_file(self, url: str, dest_path: str, force_redownload: bool = False) -> Dict[str, Any]:
        """
        Télécharge un fichier simple
        
        Args:
            url: URL du fichier à télécharger
            dest_path: Chemin de destination
            force_redownload: Force le re-téléchargement même si le fichier existe
            
        Returns:
            Dict avec success, error, dest_path, file_size
        """
        result = {'success': False, 'error': None, 'dest_path': dest_path, 'file_size': 0}
        
        try:
            # Vérifier si le fichier existe déjà
            if os.path.exists(dest_path) and not force_redownload:
                result['success'] = True
                result['file_size'] = os.path.getsize(dest_path)
                log_message("INFO", f"Fichier '{os.path.basename(dest_path)}' existe déjà.", category="download_file")
                return result
            
            # Créer le répertoire parent si nécessaire
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            log_message("INFO", f"Téléchargement fichier depuis {url}...", category="download_file")
            
            # Télécharger le fichier
            response = self.session.get(url, timeout=120)
            response.raise_for_status()
            
            # Sauvegarder le fichier
            with open(dest_path, 'wb') as f:
                f.write(response.content)
            
            result['success'] = True
            result['file_size'] = len(response.content)
            log_message("INFO", f"Fichier téléchargé avec succès : {os.path.basename(dest_path)} ({result['file_size']/1024/1024:.1f} MB)", category="download_file")
            
        except requests.exceptions.RequestException as e:
            result['error'] = f"Erreur de téléchargement : {e}"
            log_message("ERREUR", result['error'], category="download_file")
        except Exception as e:
            result['error'] = f"Erreur inattendue : {e}"
            log_message("ERREUR", result['error'], category="download_file")
        
        return result
    
    def get_download_info(self, url: str) -> Dict[str, Any]:
        """
        Récupère les informations sur un fichier distant sans le télécharger
        
        Args:
            url: URL du fichier
            
        Returns:
            Dict avec success, error, content_length, content_type
        """
        result = {'success': False, 'error': None, 'content_length': 0, 'content_type': None}
        
        try:
            # Faire une requête HEAD pour récupérer les métadonnées
            response = self.session.head(url, timeout=30)
            response.raise_for_status()
            
            result['success'] = True
            result['content_length'] = int(response.headers.get('content-length', 0))
            result['content_type'] = response.headers.get('content-type', '')
            
            log_message("DEBUG", f"Info fichier distant : {result['content_length']/1024/1024:.1f} MB, type: {result['content_type']}", category="download_info")
            
        except requests.exceptions.RequestException as e:
            result['error'] = f"Erreur récupération info : {e}"
            log_message("ERREUR", result['error'], category="download_info")
        except Exception as e:
            result['error'] = f"Erreur inattendue : {e}"
            log_message("ERREUR", result['error'], category="download_info")
        
        return result
    
    def _cleanup_temp_files(self, file_paths: list):
        """Nettoie les fichiers temporaires"""
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
            except Exception as e:
                log_message("ATTENTION", f"Impossible de nettoyer {file_path}: {e}", category="cleanup")
    
    def close(self):
        """Ferme la session de téléchargement"""
        try:
            self.session.close()
        except Exception as e:
            log_message("DEBUG", f"Erreur fermeture session : {e}", category="session")


# Instance globale pour réutilisation
_global_downloader = None

def get_downloader() -> UniversalDownloader:
    """Retourne une instance globale du téléchargeur"""
    global _global_downloader
    if _global_downloader is None:
        _global_downloader = UniversalDownloader()
    return _global_downloader
