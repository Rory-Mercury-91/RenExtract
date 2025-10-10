# ui/tutorial/cache.py
"""
Système de cache optimisé pour le tutoriel multilingue
Gestion intelligente de la mémoire et persistence
"""

import os
import json
import hashlib
import pickle
import time
from typing import Dict, Any, Optional, Union
from pathlib import Path
from infrastructure.logging.logging import log_message

class TutorialCache:
    """Cache intelligent pour traductions et images avec persistence"""
    
    def __init__(self, cache_dir: Optional[str] = None):
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / '.renextract' / 'tutorial_cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Caches en mémoire
        self._translation_cache: Dict[str, Dict] = {}
        self._image_cache: Dict[str, str] = {}
        self._content_cache: Dict[str, str] = {}
        
        # Métadonnées du cache
        self._cache_metadata = {
            'created': time.time(),
            'last_cleanup': time.time(),
            'version': '2.0.0'
        }
        
        # Paramètres de cache
        self.max_memory_size = 50 * 1024 * 1024  # 50MB en mémoire
        self.max_disk_size = 200 * 1024 * 1024   # 200MB sur disque
        self.cache_ttl = 86400 * 7  # 7 jours
        
        # Charger les métadonnées existantes
        self._load_metadata()
        
    def _load_metadata(self):
        """Charge les métadonnées du cache depuis le disque"""
        metadata_file = self.cache_dir / 'metadata.json'
        try:
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    saved_metadata = json.load(f)
                    self._cache_metadata.update(saved_metadata)
        except Exception as e:
            log_message("ATTENTION", f"Erreur chargement métadonnées cache: {e}", 
                       category="tutorial_cache")
    
    def _save_metadata(self):
        """Sauvegarde les métadonnées du cache"""
        metadata_file = self.cache_dir / 'metadata.json'
        try:
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self._cache_metadata, f, indent=2)
        except Exception as e:
            log_message("ATTENTION", f"Erreur sauvegarde métadonnées cache: {e}",
                       category="tutorial_cache")
    
    def _generate_cache_key(self, category: str, identifier: str, **kwargs) -> str:
        """Génère une clé de cache unique"""
        key_data = f"{category}:{identifier}:{json.dumps(kwargs, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_cache_file_path(self, cache_key: str, category: str) -> Path:
        """Retourne le chemin du fichier de cache"""
        category_dir = self.cache_dir / category
        category_dir.mkdir(exist_ok=True)
        return category_dir / f"{cache_key}.cache"
    
    def _is_cache_valid(self, cache_file: Path) -> bool:
        """Vérifie si un fichier de cache est encore valide"""
        if not cache_file.exists():
            return False
        
        try:
            file_age = time.time() - cache_file.stat().st_mtime
            return file_age < self.cache_ttl
        except Exception:
            return False
    
    def get_translation(self, language: str) -> Optional[Dict]:
        """Récupère une traduction depuis le cache"""
        # Vérifier le cache mémoire d'abord
        if language in self._translation_cache:
            log_message("DEBUG", f"Translation cache hit (memory): {language}", 
                       category="tutorial_cache")
            return self._translation_cache[language]
        
        # Vérifier le cache disque
        cache_key = self._generate_cache_key('translation', language)
        cache_file = self._get_cache_file_path(cache_key, 'translations')
        
        if self._is_cache_valid(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    translation_data = pickle.load(f)
                    
                # Mettre en cache mémoire
                self._translation_cache[language] = translation_data
                log_message("DEBUG", f"Translation cache hit (disk): {language}",
                           category="tutorial_cache")
                return translation_data
                
            except Exception as e:
                log_message("ATTENTION", f"Erreur lecture cache traduction {language}: {e}",
                           category="tutorial_cache")
        
        return None
    
    def set_translation(self, language: str, translation_data: Dict):
        """Sauvegarde une traduction dans le cache"""
        # Cache mémoire
        self._translation_cache[language] = translation_data
        
        # Cache disque
        cache_key = self._generate_cache_key('translation', language)
        cache_file = self._get_cache_file_path(cache_key, 'translations')
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(translation_data, f)
                
            log_message("DEBUG", f"Translation cached: {language} ({len(str(translation_data))} chars)",
                       category="tutorial_cache")
        except Exception as e:
            log_message("ATTENTION", f"Erreur sauvegarde cache traduction {language}: {e}",
                       category="tutorial_cache")
    
    def get_image(self, image_key: str) -> Optional[str]:
        """Récupère une image encodée depuis le cache"""
        # Cache mémoire
        if image_key in self._image_cache:
            log_message("DEBUG", f"Image cache hit (memory): {image_key}",
                       category="tutorial_cache")
            return self._image_cache[image_key]
        
        # Cache disque
        cache_key = self._generate_cache_key('image', image_key)
        cache_file = self._get_cache_file_path(cache_key, 'images')
        
        if self._is_cache_valid(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    image_data = f.read()
                    
                # Mettre en cache mémoire si pas trop gros
                if len(image_data) < 1024 * 1024:  # < 1MB
                    self._image_cache[image_key] = image_data
                    
                log_message("DEBUG", f"Image cache hit (disk): {image_key}",
                           category="tutorial_cache")
                return image_data
                
            except Exception as e:
                log_message("ATTENTION", f"Erreur lecture cache image {image_key}: {e}",
                           category="tutorial_cache")
        
        return None
    
    def set_image(self, image_key: str, image_data: str):
        """Sauvegarde une image encodée dans le cache"""
        # Cache mémoire (seulement si pas trop gros)
        if len(image_data) < 1024 * 1024:  # < 1MB
            self._image_cache[image_key] = image_data
        
        # Cache disque
        cache_key = self._generate_cache_key('image', image_key)
        cache_file = self._get_cache_file_path(cache_key, 'images')
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(image_data)
                
            log_message("DEBUG", f"Image cached: {image_key} ({len(image_data)} chars)",
                       category="tutorial_cache")
        except Exception as e:
            log_message("ATTENTION", f"Erreur sauvegarde cache image {image_key}: {e}",
                       category="tutorial_cache")
    
    def get_content(self, content_key: str) -> Optional[str]:
        """Récupère du contenu généré depuis le cache"""
        return self._content_cache.get(content_key)
    
    def set_content(self, content_key: str, content_data: str):
        """Sauvegarde du contenu généré dans le cache"""
        self._content_cache[content_key] = content_data
        log_message("DEBUG", f"Content cached: {content_key} ({len(content_data)} chars)",
                   category="tutorial_cache")
    
    def get_memory_usage(self) -> Dict[str, int]:
        """Retourne l'usage mémoire du cache"""
        translations_size = sum(len(str(data)) for data in self._translation_cache.values())
        images_size = sum(len(data) for data in self._image_cache.values())
        content_size = sum(len(data) for data in self._content_cache.values())
        
        return {
            'translations': translations_size,
            'images': images_size, 
            'content': content_size,
            'total': translations_size + images_size + content_size
        }
    
    def get_disk_usage(self) -> int:
        """Retourne l'usage disque du cache"""
        total_size = 0
        try:
            for path in self.cache_dir.rglob('*.cache'):
                total_size += path.stat().st_size
        except Exception as e:
            log_message("ATTENTION", f"Erreur calcul usage disque: {e}", 
                       category="tutorial_cache")
        return total_size
    
    def cleanup_old_cache(self):
        """Nettoie les anciens fichiers de cache"""
        cleaned_count = 0
        cleaned_size = 0
        
        try:
            current_time = time.time()
            for cache_file in self.cache_dir.rglob('*.cache'):
                if current_time - cache_file.stat().st_mtime > self.cache_ttl:
                    file_size = cache_file.stat().st_size
                    cache_file.unlink()
                    cleaned_count += 1
                    cleaned_size += file_size
            
            self._cache_metadata['last_cleanup'] = current_time
            self._save_metadata()
            
            if cleaned_count > 0:
                log_message("INFO", 
                           f"Cache nettoyé: {cleaned_count} fichiers supprimés ({cleaned_size} bytes)",
                           category="tutorial_cache")
                           
        except Exception as e:
            log_message("ATTENTION", f"Erreur nettoyage cache: {e}",
                       category="tutorial_cache")
    
    def clear_memory_cache(self):
        """Vide le cache mémoire"""
        memory_usage = self.get_memory_usage()
        self._translation_cache.clear()
        self._image_cache.clear()
        self._content_cache.clear()
        
        log_message("INFO", f"Cache mémoire vidé: {memory_usage['total']} bytes libérés",
                   category="tutorial_cache")
    
    def clear_all_cache(self):
        """Vide complètement le cache (mémoire + disque)"""
        # Vider la mémoire
        self.clear_memory_cache()
        
        # Vider le disque
        try:
            import shutil
            if self.cache_dir.exists():
                shutil.rmtree(self.cache_dir)
                self.cache_dir.mkdir(parents=True, exist_ok=True)
                
            log_message("INFO", "Cache complètement vidé (mémoire + disque)",
                       category="tutorial_cache")
        except Exception as e:
            log_message("ERREUR", f"Erreur vidage cache disque: {e}",
                       category="tutorial_cache")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du cache"""
        memory_usage = self.get_memory_usage()
        disk_usage = self.get_disk_usage()
        
        return {
            'memory_usage_bytes': memory_usage['total'],
            'disk_usage_bytes': disk_usage,
            'memory_items': {
                'translations': len(self._translation_cache),
                'images': len(self._image_cache),
                'content': len(self._content_cache)
            },
            'cache_dir': str(self.cache_dir),
            'metadata': self._cache_metadata.copy(),
            'limits': {
                'max_memory_size': self.max_memory_size,
                'max_disk_size': self.max_disk_size,
                'cache_ttl_hours': self.cache_ttl / 3600
            }
        }

# Instance globale du cache (singleton pattern)
_global_cache = None

def get_tutorial_cache() -> TutorialCache:
    """Retourne l'instance globale du cache"""
    global _global_cache
    if _global_cache is None:
        _global_cache = TutorialCache()
    return _global_cache

def clear_tutorial_cache():
    """Vide le cache global"""
    global _global_cache
    if _global_cache is not None:
        _global_cache.clear_all_cache()
        _global_cache = None