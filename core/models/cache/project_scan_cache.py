# core/project_scan_cache.py
"""
Cache intelligent pour les scans de projets Ren'Py
Invalidation granulaire par langue pour optimiser les performances
"""

import os
import pickle
import time
from typing import Dict, List, Optional, Any
from infrastructure.logging.logging import log_message
from infrastructure.config.constants import FOLDERS

class ProjectScanCache:
    """
    Cache singleton pour les scans de projets avec invalidation granulaire
    
    Stratégie d'invalidation :
    - Par langue : Seulement la langue modifiée est rescannée
    - Par mtime : Compare le timestamp du dossier langue
    - Fichier unique : Cache tous les projets dans un seul fichier
    """
    
    _instance = None
    
    def __new__(cls):
        """Pattern Singleton"""
        if cls._instance is None:
            cls._instance = super(ProjectScanCache, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialise le cache (une seule fois)"""
        if self._initialized:
            return
        
        # Fichier de cache persistant (utiliser "configs" avec 's')
        config_dir = FOLDERS.get("configs", ".")
        self.cache_file = os.path.join(config_dir, "project_scan_cache.pkl")
        
        # Cache en mémoire : {project_path: {languages: {...}}}
        self._cache = self._load_cache()
        
        self._initialized = True
        log_message("DEBUG", f"ProjectScanCache initialisé avec {len(self._cache)} projets en cache", category="cache")
    
    def _load_cache(self) -> Dict[str, Any]:
        """Charge le cache depuis le disque"""
        try:
            if os.path.exists(self.cache_file):
                file_size = os.path.getsize(self.cache_file)
                log_message("INFO", f"📂 Chargement cache projet ({file_size} octets)...", category="cache")
                
                with open(self.cache_file, 'rb') as f:
                    cache = pickle.load(f)
                
                total_langs = sum(len(p.get('languages', {})) for p in cache.values())
                log_message("INFO", f"✅ Cache chargé: {len(cache)} projets, {total_langs} langues", category="cache")
                return cache
            else:
                log_message("INFO", "⚠️  Aucun cache projet trouvé (première utilisation)", category="cache")
        except Exception as e:
            log_message("ERREUR", f"❌ Erreur chargement cache projet: {e}", category="cache")
            import traceback
            log_message("DEBUG", traceback.format_exc(), category="cache")
        
        return {}
    
    def _save_cache(self):
        """Sauvegarde le cache sur le disque"""
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self._cache, f)
            
            file_size = os.path.getsize(self.cache_file)
            total_langs = sum(len(p.get('languages', {})) for p in self._cache.values())
            log_message("INFO", f"💾 Cache sauvegardé: {len(self._cache)} projets, {total_langs} langues ({file_size} octets)", category="cache")
        except Exception as e:
            log_message("ERREUR", f"❌ Erreur sauvegarde cache projet: {e}", category="cache")
            import traceback
            log_message("DEBUG", traceback.format_exc(), category="cache")
    
    def get_project_languages(self, project_path: str) -> Optional[List[Dict[str, Any]]]:
        """
        Récupère les langues d'un projet depuis le cache
        
        Args:
            project_path: Chemin du projet
            
        Returns:
            Liste des langues ou None si cache invalide
        """
        if not project_path or project_path not in self._cache:
            return None
        
        project_cache = self._cache[project_path]
        
        # Vérifier si le dossier tl/ existe toujours
        tl_path = os.path.join(project_path, "game", "tl")
        if not os.path.exists(tl_path):
            # Projet n'existe plus, supprimer du cache
            del self._cache[project_path]
            self._save_cache()
            return None
        
        # Retourner la liste des langues
        languages = []
        for lang_name, lang_data in project_cache.get('languages', {}).items():
            languages.append({
                'name': lang_name,
                'file_count': lang_data.get('file_count', 0)
            })
        
        log_message("DEBUG", f"Cache HIT: {len(languages)} langues pour {os.path.basename(project_path)}", category="cache")
        return languages
    
    def get_language_files(self, project_path: str, language: str, 
                          exclusions: List[str] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Récupère les fichiers d'une langue depuis le cache avec invalidation granulaire
        
        Args:
            project_path: Chemin du projet
            language: Nom de la langue
            exclusions: Fichiers à exclure
            
        Returns:
            Liste des fichiers ou None si cache invalide pour cette langue
        """
        if not project_path or project_path not in self._cache:
            log_message("DEBUG", f"Cache MISS: projet {os.path.basename(project_path)} non trouvé", category="cache")
            return None
        
        project_cache = self._cache[project_path]
        
        if 'languages' not in project_cache or language not in project_cache['languages']:
            log_message("DEBUG", f"Cache MISS: langue {language} non trouvée", category="cache")
            return None
        
        lang_cache = project_cache['languages'][language]
        
        # Vérifier si le dossier de la langue a été modifié (invalidation granulaire)
        lang_path = os.path.join(project_path, "game", "tl", language)
        if not os.path.exists(lang_path):
            # Langue supprimée
            del project_cache['languages'][language]
            self._save_cache()
            log_message("DEBUG", f"Cache INVALIDATED: langue {language} supprimée", category="cache")
            return None
        
        # Comparer le mtime du dossier
        try:
            current_mtime = os.path.getmtime(lang_path)
            cached_mtime = lang_cache.get('directory_mtime', 0)
            
            if current_mtime > cached_mtime:
                # Dossier modifié, cache invalide pour cette langue
                log_message("DEBUG", f"Cache INVALIDATED: langue {language} modifiée (mtime: {current_mtime} > {cached_mtime})", category="cache")
                return None
        except Exception as e:
            log_message("ATTENTION", f"Erreur vérification mtime: {e}", category="cache")
            return None
        
        # Cache valide, filtrer les exclusions
        files = lang_cache.get('files', [])
        
        if exclusions:
            files = [f for f in files if f['name'] not in exclusions]
        
        log_message("DEBUG", f"Cache HIT: {len(files)} fichiers pour {language} (après exclusions)", category="cache")
        return files
    
    def cache_project_languages(self, project_path: str, languages: List[Dict[str, Any]]):
        """
        Met en cache la liste des langues d'un projet
        
        Args:
            project_path: Chemin du projet
            languages: Liste des langues avec file_count
        """
        if project_path not in self._cache:
            self._cache[project_path] = {'languages': {}}
        
        # Mettre à jour les infos de langue (sans écraser les fichiers déjà cachés)
        for lang in languages:
            lang_name = lang['name']
            if lang_name not in self._cache[project_path]['languages']:
                self._cache[project_path]['languages'][lang_name] = {}
            
            self._cache[project_path]['languages'][lang_name]['file_count'] = lang['file_count']
        
        self._save_cache()
        log_message("DEBUG", f"Cache UPDATE: {len(languages)} langues pour {os.path.basename(project_path)}", category="cache")
    
    def cache_language_files(self, project_path: str, language: str, files: List[Dict[str, Any]]):
        """
        Met en cache les fichiers d'une langue avec invalidation granulaire
        
        Args:
            project_path: Chemin du projet
            language: Nom de la langue
            files: Liste des fichiers
        """
        if project_path not in self._cache:
            self._cache[project_path] = {'languages': {}}
        
        if language not in self._cache[project_path]['languages']:
            self._cache[project_path]['languages'][language] = {}
        
        # Stocker les fichiers avec le mtime du dossier pour invalidation
        lang_path = os.path.join(project_path, "game", "tl", language)
        try:
            directory_mtime = os.path.getmtime(lang_path)
        except:
            directory_mtime = time.time()
        
        self._cache[project_path]['languages'][language].update({
            'files': files,
            'file_count': len(files),
            'directory_mtime': directory_mtime,
            'last_scan': time.strftime("%Y-%m-%d %H:%M:%S")
        })
        
        self._save_cache()
        log_message("DEBUG", f"Cache UPDATE: {len(files)} fichiers pour {language} (mtime: {directory_mtime})", category="cache")
    
    def invalidate_language(self, project_path: str, language: str):
        """
        Invalide le cache d'une langue spécifique
        
        Args:
            project_path: Chemin du projet
            language: Nom de la langue à invalider
        """
        if project_path in self._cache and language in self._cache[project_path].get('languages', {}):
            del self._cache[project_path]['languages'][language]
            self._save_cache()
            log_message("DEBUG", f"Cache INVALIDATED: langue {language} manuellement", category="cache")
    
    def invalidate_project(self, project_path: str):
        """
        Invalide tout le cache d'un projet
        
        Args:
            project_path: Chemin du projet
        """
        if project_path in self._cache:
            del self._cache[project_path]
            self._save_cache()
            log_message("DEBUG", f"Cache INVALIDATED: projet {os.path.basename(project_path)} manuellement", category="cache")
    
    def clear_cache(self):
        """Efface tout le cache (réinitialisation)"""
        self._cache = {}
        self._save_cache()
        log_message("INFO", "Cache projet complètement effacé", category="cache")
    
    def clear_persistent_cache(self):
        """Efface le cache persistant (fichier .pkl)"""
        try:
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)
                log_message("INFO", "Cache persistant projet supprimé", category="cache")
            self._cache = {}
        except Exception as e:
            log_message("ERREUR", f"Erreur suppression cache projet: {e}", category="cache")
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Retourne des informations sur le cache"""
        total_languages = 0
        total_files = 0
        
        for project_cache in self._cache.values():
            for lang_cache in project_cache.get('languages', {}).values():
                total_languages += 1
                total_files += lang_cache.get('file_count', 0)
        
        return {
            'projects': len(self._cache),
            'languages': total_languages,
            'files': total_files,
            'cache_file': self.cache_file,
            'size_bytes': os.path.getsize(self.cache_file) if os.path.exists(self.cache_file) else 0
        }


# Instance globale
_project_cache = None

def get_project_cache() -> ProjectScanCache:
    """Retourne l'instance singleton du cache projet"""
    global _project_cache
    if _project_cache is None:
        _project_cache = ProjectScanCache()
    return _project_cache

