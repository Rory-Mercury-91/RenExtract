# core/business/generator/image_manager.py
# Gestionnaire centralisé des images pour la génération de traductions

"""
Gestionnaire d'images pour RenExtract
- Téléchargement d'images depuis GitHub
- Stockage dans le dossier tools
- Copie vers les projets
"""

import os
import shutil
import requests
from pathlib import Path
from typing import Optional, Tuple
from infrastructure.logging.logging import log_message

class ImageManager:
    """Gestionnaire centralisé des images pour la génération"""
    
    # Images disponibles avec leurs URLs
    AVAILABLE_IMAGES = {
        'textboxHigh.png': 'https://github.com/Rory-Mercury-91/Stockage/releases/download/1.0.0/textboxHigh.png'
    }
    
    def __init__(self, tools_dir: str):
        """
        Initialise le gestionnaire d'images
        
        Args:
            tools_dir: Répertoire pour stocker les outils et images
        """
        self.tools_dir = tools_dir
        self.images_dir = os.path.join(tools_dir, "images")
        
        # Créer le dossier images s'il n'existe pas
        os.makedirs(self.images_dir, exist_ok=True)
        
        log_message("DEBUG", f"ImageManager initialisé: {self.images_dir}", category="image_manager")
    
    def get_image_path(self, image_name: str) -> Optional[str]:
        """
        Retourne le chemin local d'une image (télécharge si nécessaire)
        
        Args:
            image_name: Nom de l'image (ex: 'textboxHigh.png')
            
        Returns:
            Chemin vers l'image ou None si erreur
        """
        try:
            if image_name not in self.AVAILABLE_IMAGES:
                log_message("ATTENTION", f"Image inconnue: {image_name}", category="image_manager")
                return None
            
            local_path = os.path.join(self.images_dir, image_name)
            
            # Si l'image existe déjà localement, la retourner
            if os.path.exists(local_path):
                log_message("DEBUG", f"Image trouvée en local: {image_name}", category="image_manager")
                return local_path
            
            # Sinon, télécharger l'image
            success, message = self._download_image(image_name)
            if success:
                return local_path
            else:
                log_message("ERREUR", f"Échec téléchargement image: {message}", category="image_manager")
                return None
                
        except Exception as e:
            log_message("ERREUR", f"Erreur get_image_path pour {image_name}: {e}", category="image_manager")
            return None
    
    def _download_image(self, image_name: str) -> Tuple[bool, str]:
        """
        Télécharge une image depuis GitHub
        
        Args:
            image_name: Nom de l'image
            
        Returns:
            (success, message)
        """
        try:
            url = self.AVAILABLE_IMAGES[image_name]
            local_path = os.path.join(self.images_dir, image_name)
            
            log_message("INFO", f"Téléchargement de {image_name}...", category="image_manager")
            
            # Télécharger l'image
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Sauvegarder l'image
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            file_size = os.path.getsize(local_path) / 1024  # KB
            log_message("INFO", f"Image téléchargée: {image_name} ({file_size:.1f} KB)", category="image_manager")
            
            return True, f"Image {image_name} téléchargée avec succès"
            
        except requests.RequestException as e:
            return False, f"Erreur réseau: {e}"
        except Exception as e:
            return False, f"Erreur: {e}"
    
    def copy_image_to_project(self, image_name: str, project_path: str, 
                             language: str, subfolder: str = "") -> Tuple[bool, str]:
        """
        Copie une image vers un projet Ren'Py
        
        Args:
            image_name: Nom de l'image
            project_path: Chemin vers le projet
            language: Langue cible
            subfolder: Sous-dossier optionnel dans tl/language/
            
        Returns:
            (success, message)
        """
        try:
            # Obtenir l'image (télécharge si nécessaire)
            source_path = self.get_image_path(image_name)
            if not source_path:
                return False, f"Image {image_name} introuvable"
            
            # Créer le dossier de destination
            game_dir = os.path.join(project_path, "game")
            tl_dir = os.path.join(game_dir, "tl", language)
            
            if subfolder:
                dest_dir = os.path.join(tl_dir, subfolder)
            else:
                dest_dir = tl_dir
            
            os.makedirs(dest_dir, exist_ok=True)
            
            # Chemin de destination
            dest_path = os.path.join(dest_dir, image_name)
            
            # Copier l'image
            shutil.copy2(source_path, dest_path)
            
            log_message("INFO", f"Image copiée: {image_name} → tl/{language}/{subfolder}", category="image_manager")
            
            # Retourner le chemin relatif pour Ren'Py
            if subfolder:
                relative_path = f"tl/{language}/{subfolder}/{image_name}"
            else:
                relative_path = f"tl/{language}/{image_name}"
            
            return True, relative_path
            
        except Exception as e:
            log_message("ERREUR", f"Erreur copie image vers projet: {e}", category="image_manager")
            return False, f"Erreur copie: {e}"
    
    def get_available_images(self) -> list:
        """Retourne la liste des images disponibles"""
        return list(self.AVAILABLE_IMAGES.keys())
    
    def clear_cache(self):
        """Supprime toutes les images en cache"""
        try:
            if os.path.exists(self.images_dir):
                shutil.rmtree(self.images_dir)
                os.makedirs(self.images_dir, exist_ok=True)
                log_message("INFO", "Cache images nettoyé", category="image_manager")
                return True
        except Exception as e:
            log_message("ERREUR", f"Erreur nettoyage cache images: {e}", category="image_manager")
            return False

# Export
__all__ = ['ImageManager']

