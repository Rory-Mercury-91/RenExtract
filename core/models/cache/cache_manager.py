# core/cache_manager.py
"""
Gestionnaire de cache persistant pour RenExtract
Optimise les performances en évitant les rechargements inutiles
"""

import os
import json
import hashlib
import pickle
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from infrastructure.logging.logging import log_message
from infrastructure.config.constants import FOLDERS

class PersistentCacheManager:
    """Gestionnaire de cache persistant avec invalidation intelligente"""
    
    def __init__(self):
        self.cache_dir = Path(FOLDERS["cache"]) if "cache" in FOLDERS else Path.home() / '.renextract' / 'cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache en mémoire par projet
        self._memory_cache: Dict[str, Dict[str, Any]] = {}
        
        # Métadonnées de cache
        self._cache_metadata = {
            'version': '1.0.0',
            'created': time.time(),
            'last_cleanup': time.time()
        }
        
        # Paramètres
        self.cache_ttl = 86400 * 7  # 7 jours
        self.max_cache_size = 500 * 1024 * 1024  # 500MB
        
        self._load_metadata()
    
    def _load_metadata(self):
        """Charge les métadonnées du cache"""
        metadata_file = self.cache_dir / 'metadata.json'
        try:
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    saved_metadata = json.load(f)
                    self._cache_metadata.update(saved_metadata)
        except Exception as e:
            log_message("ATTENTION", f"Erreur chargement métadonnées cache: {e}", category="cache_manager")
    
    def _save_metadata(self):
        """Sauvegarde les métadonnées du cache"""
        metadata_file = self.cache_dir / 'metadata.json'
        try:
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self._cache_metadata, f, indent=2)
        except Exception as e:
            log_message("ATTENTION", f"Erreur sauvegarde métadonnées cache: {e}", category="cache_manager")
    
    def _get_project_key(self, project_path: str) -> str:
        """Génère une clé unique pour un projet"""
        return hashlib.md5(project_path.encode('utf-8')).hexdigest()[:16]
    
    def _get_cache_file_path(self, project_key: str, cache_type: str) -> Path:
        """Retourne le chemin du fichier de cache"""
        return self.cache_dir / f"{project_key}_{cache_type}.cache"
    
    def _is_cache_valid(self, cache_file: Path, project_path: str) -> bool:
        """Vérifie si le cache est valide"""
        try:
            if not cache_file.exists():
                return False
            
            # Vérifier l'âge du cache
            cache_age = time.time() - cache_file.stat().st_mtime
            if cache_age > self.cache_ttl:
                return False
            
            # Vérifier si les fichiers du projet ont changé
            metadata_file = cache_file.with_suffix('.meta')
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                # Vérifier les timestamps des fichiers clés
                for file_path, timestamp in metadata.get('file_timestamps', {}).items():
                    if os.path.exists(file_path):
                        if os.path.getmtime(file_path) != timestamp:
                            return False
                    else:
                        return False  # Fichier supprimé
            
            return True
            
        except Exception:
            return False
    
    def get_game_files_cache(self, project_path: str) -> Optional[Dict[str, str]]:
        """Récupère le cache des fichiers game/ pour un projet"""
        project_key = self._get_project_key(project_path)
        cache_file = self._get_cache_file_path(project_key, 'game_files')
        
        # Vérifier le cache mémoire d'abord
        if project_key in self._memory_cache and 'game_files' in self._memory_cache[project_key]:
            log_message("DEBUG", f"Cache game files hit (memory): {os.path.basename(project_path)}", category="cache_manager")
            return self._memory_cache[project_key]['game_files']
        
        # Vérifier le cache disque
        if self._is_cache_valid(cache_file, project_path):
            try:
                with open(cache_file, 'rb') as f:
                    cache_data = pickle.load(f)
                
                # Mettre en cache mémoire
                if project_key not in self._memory_cache:
                    self._memory_cache[project_key] = {}
                self._memory_cache[project_key]['game_files'] = cache_data
                
                log_message("INFO", f"Cache game files chargé depuis disque: {os.path.basename(project_path)} ({len(cache_data)} fichiers)", category="cache_manager")
                return cache_data
                
            except Exception as e:
                log_message("ATTENTION", f"Erreur lecture cache game files: {e}", category="cache_manager")
        
        return None
    
    def set_game_files_cache(self, project_path: str, cache_data: Dict[str, str]):
        """Sauvegarde le cache des fichiers game/ pour un projet"""
        project_key = self._get_project_key(project_path)
        cache_file = self._get_cache_file_path(project_key, 'game_files')
        
        try:
            # Sauvegarder le cache
            with open(cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
            
            # Sauvegarder les métadonnées
            metadata = {
                'project_path': project_path,
                'cache_type': 'game_files',
                'file_count': len(cache_data),
                'created': time.time(),
                'file_timestamps': {}
            }
            
            # Enregistrer les timestamps des fichiers
            for file_path in cache_data.keys():
                if os.path.exists(file_path):
                    metadata['file_timestamps'][file_path] = os.path.getmtime(file_path)
            
            metadata_file = cache_file.with_suffix('.meta')
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            # Mettre en cache mémoire
            if project_key not in self._memory_cache:
                self._memory_cache[project_key] = {}
            self._memory_cache[project_key]['game_files'] = cache_data
            
            log_message("INFO", f"Cache game files sauvegardé: {os.path.basename(project_path)} ({len(cache_data)} fichiers)", category="cache_manager")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur sauvegarde cache game files: {e}", category="cache_manager")
    
    def get_string_search_cache(self, project_path: str) -> Optional[Dict[str, bool]]:
        """Récupère le cache de recherche de chaînes pour un projet"""
        project_key = self._get_project_key(project_path)
        cache_file = self._get_cache_file_path(project_key, 'string_search')
        
        # Vérifier le cache mémoire d'abord
        if project_key in self._memory_cache and 'string_search' in self._memory_cache[project_key]:
            return self._memory_cache[project_key]['string_search']
        
        # Vérifier le cache disque
        if self._is_cache_valid(cache_file, project_path):
            try:
                with open(cache_file, 'rb') as f:
                    cache_data = pickle.load(f)
                
                # Mettre en cache mémoire
                if project_key not in self._memory_cache:
                    self._memory_cache[project_key] = {}
                self._memory_cache[project_key]['string_search'] = cache_data
                
                log_message("DEBUG", f"Cache string search chargé: {len(cache_data)} recherches", category="cache_manager")
                return cache_data
                
            except Exception as e:
                log_message("ATTENTION", f"Erreur lecture cache string search: {e}", category="cache_manager")
        
        return None
    
    def set_string_search_cache(self, project_path: str, cache_data: Dict[str, bool]):
        """Sauvegarde le cache de recherche de chaînes pour un projet"""
        project_key = self._get_project_key(project_path)
        cache_file = self._get_cache_file_path(project_key, 'string_search')
        
        try:
            # Sauvegarder le cache
            with open(cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
            
            # Mettre en cache mémoire
            if project_key not in self._memory_cache:
                self._memory_cache[project_key] = {}
            self._memory_cache[project_key]['string_search'] = cache_data
            
            log_message("DEBUG", f"Cache string search sauvegardé: {len(cache_data)} recherches", category="cache_manager")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur sauvegarde cache string search: {e}", category="cache_manager")
    
    def clear_project_cache(self, project_path: str):
        """Efface le cache pour un projet spécifique"""
        project_key = self._get_project_key(project_path)
        
        try:
            # Effacer le cache mémoire
            if project_key in self._memory_cache:
                del self._memory_cache[project_key]
            
            # Effacer les fichiers de cache
            for cache_type in ['game_files', 'string_search']:
                cache_file = self._get_cache_file_path(project_key, cache_type)
                if cache_file.exists():
                    cache_file.unlink()
                
                metadata_file = cache_file.with_suffix('.meta')
                if metadata_file.exists():
                    metadata_file.unlink()
            
            log_message("INFO", f"Cache effacé pour le projet: {os.path.basename(project_path)}", category="cache_manager")
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur effacement cache: {e}", category="cache_manager")
    
    def cleanup_old_caches(self):
        """Nettoie les anciens caches"""
        try:
            current_time = time.time()
            cleaned_count = 0
            
            for cache_file in self.cache_dir.glob("*.cache"):
                if current_time - cache_file.stat().st_mtime > self.cache_ttl:
                    cache_file.unlink()
                    cleaned_count += 1
                    
                    # Effacer aussi le fichier de métadonnées
                    metadata_file = cache_file.with_suffix('.meta')
                    if metadata_file.exists():
                        metadata_file.unlink()
            
            if cleaned_count > 0:
                log_message("INFO", f"🧹 Nettoyage cache: {cleaned_count} anciens fichiers supprimés", category="cache_manager")
            
            self._cache_metadata['last_cleanup'] = current_time
            self._save_metadata()
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur nettoyage cache: {e}", category="cache_manager")

# Instance globale
cache_manager = PersistentCacheManager()
