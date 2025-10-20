# core/unified_backup_manager.py - VERSION STRUCTURE HIÉRARCHIQUE + CACHE
# Gestionnaire Unifié de Sauvegardes - RenExtract 

"""
Gestionnaire Unifié de Sauvegardes avec structure hiérarchique et cache mémoire

Structure: Game_name/file_name/backup_type/fichiers
- Rotation automatique pour le type "editing" (max 10 fichiers)
- Structure unifiée pour tous les types
- Harmonisation avec les systèmes d'avertissement et nettoyage
- Cache mémoire pour optimiser les performances avec beaucoup de sauvegardes
"""

import os
import shutil
import datetime
import json
import glob
import time
import pickle
import zipfile
import fnmatch
from typing import List, Dict, Optional
from pathlib import Path
from infrastructure.config.constants import FOLDERS, ensure_folders_exist
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import extract_game_name

class BackupType:
    """Énumération des types de sauvegarde"""
    SECURITY = "security"
    CLEANUP = "cleanup"
    RPA_BUILD = "rpa_build"
    REALTIME_EDIT = "realtime_edit"
    BEFORE_COMBINATION = "before_combination"
    COHERENCE_EDIT = "coherence_edit"

class UnifiedBackupManager:
    """Gestionnaire unifié avec structure hiérarchique et cache mémoire (Singleton)"""
    
    _instance = None  # Instance unique du singleton
    
    BACKUP_DESCRIPTIONS = {
        BackupType.SECURITY: "🛡️ Sécurité",
        BackupType.CLEANUP: "🧹 Nettoyage",
        BackupType.RPA_BUILD: "📦 Avant RPA",
        BackupType.REALTIME_EDIT: "⚡ Édition temps réel",
        BackupType.BEFORE_COMBINATION: "🔗 Avant combinaison",
        BackupType.COHERENCE_EDIT: "🔧 Modification cohérence"
    }
    
    # Configuration de rotation par type
    ROTATION_CONFIG = {
        BackupType.REALTIME_EDIT: 10,  # Max 10 fichiers pour editing
        # Autres types: pas de rotation (None)
    }
    
    # Configuration du cache
    CACHE_TTL = 60  # Durée de vie du cache en secondes (60s par défaut)
    
    def __new__(cls):
        """Pattern Singleton : retourne toujours la même instance"""
        if cls._instance is None:
            cls._instance = super(UnifiedBackupManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialise le gestionnaire unifié avec cache (une seule fois pour le singleton)"""
        # Ne s'initialiser qu'une seule fois
        if self._initialized:
            return
        
        ensure_folders_exist()
        self.backup_root = FOLDERS["backup"]
        self.metadata_file = os.path.join(self.backup_root, "backup_metadata.json")
        self.cache_file = os.path.join(self.backup_root, "backup_cache.pkl")
        self._load_metadata()
        
        # Initialisation du cache
        self._cache_data = None
        self._cache_timestamp = 0
        self._cache_enabled = True  # Peut être désactivé pour le débogage
        
        # Index des métadonnées par backup_path pour accès O(1)
        self._metadata_index = {}
        self._rebuild_metadata_index()
        
        # Charger le cache persistant depuis le disque
        self._load_persistent_cache()
        
        self._initialized = True
        log_message("DEBUG", "UnifiedBackupManager initialisé avec système de cache persistant (singleton)", category="backup")
    
    def _load_metadata(self):
        """Charge les métadonnées des sauvegardes"""
        try:
            if os.path.exists(self.metadata_file):
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
            else:
                self.metadata = {}
        except Exception as e:
            log_message("ATTENTION", f"Erreur chargement métadonnées backups: {e}", category="backup_metadata")
            self.metadata = {}
    
    def _save_metadata(self):
        """Sauvegarde les métadonnées"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log_message("ATTENTION", f"Erreur sauvegarde métadonnées backups: {e}", category="backup_metadata")
    
    def _rebuild_metadata_index(self):
        """Reconstruit l'index des métadonnées par backup_path pour accès O(1)"""
        self._metadata_index = {}
        for backup_id, metadata in self.metadata.items():
            backup_path = metadata.get('backup_path')
            if backup_path:
                self._metadata_index[backup_path] = backup_id
        
        log_message("DEBUG", f"Index métadonnées reconstruit : {len(self._metadata_index)} entrées", 
                   category="backup_cache")
    
    def _invalidate_cache(self):
        """Invalide le cache des sauvegardes"""
        self._cache_data = None
        self._cache_timestamp = 0
        log_message("DEBUG", "Cache des sauvegardes invalidé", category="backup_cache")
    
    def _is_cache_valid(self) -> bool:
        """Vérifie si le cache est encore valide"""
        if not self._cache_enabled:
            return False
        
        if self._cache_data is None:
            return False
        
        # Vérifier le TTL
        current_time = time.time()
        age = current_time - self._cache_timestamp
        
        if age > self.CACHE_TTL:
            log_message("DEBUG", f"Cache expiré (âge: {age:.1f}s > TTL: {self.CACHE_TTL}s)", category="backup_cache")
            return False
        
        return True
    
    def clear_cache(self):
        """Méthode publique pour forcer le nettoyage du cache"""
        self._invalidate_cache()
        log_message("INFO", "Cache des sauvegardes nettoyé manuellement", category="backup_cache")
    
    def get_cache_info(self) -> dict:
        """Retourne les informations sur le cache"""
        return {
            'enabled': self._cache_enabled,
            'ttl': self.CACHE_TTL,
            'valid': self._is_cache_valid(),
            'size': len(self._cache_data) if self._cache_data else 0,
            'index_size': len(self._metadata_index),
            'persistent': os.path.exists(self.cache_file)
        }
    
    def _load_persistent_cache(self):
        """Charge le cache persistant depuis le disque"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'rb') as f:
                    cache_data = pickle.load(f)
                    
                # Vérifier que le cache n'est pas trop ancien
                cache_age = time.time() - cache_data.get('timestamp', 0)
                if cache_age < self.CACHE_TTL:
                    self._cache_data = cache_data.get('data')
                    self._cache_timestamp = cache_data.get('timestamp')
                    log_message("DEBUG", 
                        f"Cache persistant chargé : {len(self._cache_data)} entrées (âge: {cache_age:.1f}s)", 
                        category="backup_cache")
                else:
                    log_message("DEBUG", 
                        f"Cache persistant expiré (âge: {cache_age:.1f}s > TTL: {self.CACHE_TTL}s)", 
                        category="backup_cache")
                    # Supprimer le cache expiré
                    os.remove(self.cache_file)
        except Exception as e:
            log_message("ATTENTION", f"Erreur chargement cache persistant: {e}", category="backup_cache")
    
    def _save_persistent_cache(self):
        """Sauvegarde le cache sur disque pour persistance entre sessions"""
        try:
            if self._cache_data is not None:
                cache_data = {
                    'data': self._cache_data,
                    'timestamp': self._cache_timestamp
                }
                with open(self.cache_file, 'wb') as f:
                    pickle.dump(cache_data, f)
                log_message("DEBUG", 
                    f"Cache persistant sauvegardé : {len(self._cache_data)} entrées", 
                    category="backup_cache")
        except Exception as e:
            log_message("ATTENTION", f"Erreur sauvegarde cache persistant: {e}", category="backup_cache")
    
    def clear_persistent_cache(self):
        """Efface le cache persistant (pour réinitialisation)"""
        try:
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)
                log_message("INFO", "Cache persistant effacé", category="backup_cache")
            self._invalidate_cache()
        except Exception as e:
            log_message("ERREUR", f"Erreur suppression cache persistant: {e}", category="backup_cache")
    
    def create_backup(self, source_path: str, backup_type: str = BackupType.SECURITY,
                    description: str = None, override_game_name: str = None, 
                    override_file_name: str = None) -> Dict[str, any]:
        """Crée une sauvegarde avec la nouvelle structure hiérarchique
        
        Args:
            source_path: Chemin du fichier source à sauvegarder
            backup_type: Type de sauvegarde (BackupType.*)
            description: Description optionnelle
            override_game_name: Nom de jeu à utiliser au lieu de l'extraction automatique
            override_file_name: Nom de fichier à utiliser au lieu de l'extraction automatique
        """
        result = {
            'success': False,
            'backup_path': None,
            'backup_id': None,
            'error': None
        }
    
        try:
            if not source_path or not os.path.exists(source_path):
                result['error'] = "Fichier source introuvable"
                return result
        
            if backup_type not in self.BACKUP_DESCRIPTIONS:
                backup_type = BackupType.SECURITY
                log_message("ATTENTION", f"Type de backup invalide, utilisation de SECURITY par défaut", category="backup")
        
            # Gestion des fichiers virtuels
            if source_path.startswith("clipboard_") and not os.path.exists(source_path):
                result['success'] = True
                result['error'] = None
                result['virtual_file'] = True
                result['message'] = "Fichier virtuel - pas de sauvegarde nécessaire"
                return result
        
            # Extraire le nom du jeu et du fichier (avec override si fourni)
            game_name = override_game_name if override_game_name else extract_game_name(source_path)
            file_name = override_file_name if override_file_name else Path(source_path).stem  # Nom sans extension
            
            # Créer la structure hiérarchique: Game_name/file_name/backup_type/
            backup_folder = os.path.join(self.backup_root, game_name, file_name, backup_type)
            os.makedirs(backup_folder, exist_ok=True)
        
            timestamp = datetime.datetime.now()
            timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
            
            # Nom du fichier de sauvegarde (garder l'extension originale)
            original_ext = Path(source_path).suffix
            backup_filename = f"{file_name}_{timestamp_str}{original_ext}"
            backup_path = os.path.join(backup_folder, backup_filename)
        
            # Copier le fichier
            shutil.copy2(source_path, backup_path)
        
            # Appliquer la rotation si nécessaire
            if backup_type in self.ROTATION_CONFIG:
                self._apply_rotation(backup_folder, backup_type)
        
            # Créer les métadonnées
            backup_id = f"{game_name}_{file_name}_{timestamp_str}_{backup_type}"
        
            backup_metadata = {
                'id': backup_id,
                'source_path': source_path,
                'backup_path': backup_path,
                'game_name': game_name,
                'file_name': file_name,
                'type': backup_type,
                'created': timestamp.isoformat(),
                'size': os.path.getsize(backup_path),
                'description': description or f"Sauvegarde {self.BACKUP_DESCRIPTIONS[backup_type]}",
                'source_filename': os.path.basename(source_path),
                'backup_filename': backup_filename
            }
        
            self.metadata[backup_id] = backup_metadata
            self._save_metadata()
        
            result['success'] = True
            result['backup_path'] = backup_path
            result['backup_id'] = backup_id
        
            log_message("DEBUG", f"Backup créé: {game_name}/{file_name}/{backup_type}/{backup_filename}", category="backup")
            
            # Invalider le cache après création d'une sauvegarde
            self._invalidate_cache()
        
        except Exception as e:
            result['error'] = str(e)
            log_message("ERREUR", f"Erreur création backup: {e}", category="backup")
    
        return result
    
    def _apply_rotation(self, backup_folder: str, backup_type: str):
        """Applique la rotation des fichiers pour un type donné"""
        try:
            max_files = self.ROTATION_CONFIG.get(backup_type)
            if max_files is None:
                return  # Pas de rotation pour ce type
            
            # Lister tous les fichiers de sauvegarde dans ce dossier
            backup_files = []
            for file in os.listdir(backup_folder):
                file_path = os.path.join(backup_folder, file)
                if os.path.isfile(file_path):
                    backup_files.append({
                        'path': file_path,
                        'name': file,
                        'mtime': os.path.getmtime(file_path)
                    })
            
            # Trier par date de modification (plus ancien en premier)
            backup_files.sort(key=lambda x: x['mtime'])
            
            # Supprimer les fichiers excédentaires
            while len(backup_files) >= max_files:
                oldest_file = backup_files.pop(0)
                try:
                    os.remove(oldest_file['path'])
                    log_message("DEBUG", f"Rotation: suppression de {oldest_file['name']}", category="backup_rotation")
                    
                    # Supprimer des métadonnées si présent
                    self._remove_from_metadata(oldest_file['path'])
                    
                except Exception as e:
                    log_message("ATTENTION", f"Erreur suppression rotation {oldest_file['name']}: {e}", category="backup_rotation")
            
            if backup_type == BackupType.REALTIME_EDIT:
                log_message("DEBUG", f"Rotation editing: {len(backup_files) + 1}/{max_files} fichiers", category="backup_rotation")
            
            # Invalider le cache si des fichiers ont été supprimés
            if len(backup_files) >= max_files:
                self._invalidate_cache()
                
        except Exception as e:
            log_message("ERREUR", f"Erreur rotation {backup_type}: {e}", category="backup_rotation")
    
    def _remove_from_metadata(self, backup_path: str):
        """Supprime une entrée des métadonnées par chemin (optimisé avec index)"""
        try:
            # Utiliser l'index pour trouver rapidement le backup_id (O(1))
            backup_id = self._metadata_index.get(backup_path)
            
            if backup_id:
                # Supprimer des métadonnées et de l'index
                if backup_id in self.metadata:
                    del self.metadata[backup_id]
                del self._metadata_index[backup_path]
                self._save_metadata()
                log_message("DEBUG", f"Métadonnées supprimées pour {backup_path}", category="backup_metadata")
                
        except Exception as e:
            log_message("ATTENTION", f"Erreur suppression métadonnées: {e}", category="backup_metadata")
    
    def list_all_backups(self, game_filter: str = None, type_filter: str = None) -> List[Dict]:
        """Liste toutes les sauvegardes avec cache mémoire pour optimiser les performances"""
        
        # Vérifier si le cache est valide et qu'on demande toutes les sauvegardes (pas de filtres)
        if self._is_cache_valid() and game_filter is None and type_filter is None:
            log_message("DEBUG", "Utilisation du cache pour list_all_backups", category="backup_cache")
            return self._cache_data.copy()  # Retourner une copie pour éviter les modifications
        
        # Cache invalide ou filtres spécifiques : charger depuis le disque
        start_time = time.time()
        backups = []
        
        try:
            if not os.path.exists(self.backup_root):
                return backups
            
            # Scanner la structure hiérarchique: Game_name/file_name/backup_type/
            for game_name in os.listdir(self.backup_root):
                if game_filter and game_filter != "Tous" and game_name != game_filter:
                    continue
                    
                game_path = os.path.join(self.backup_root, game_name)
                if not os.path.isdir(game_path) or game_name.startswith('.'):
                    continue
                
                # Parcourir les fichiers
                for file_name in os.listdir(game_path):
                    file_path = os.path.join(game_path, file_name)
                    if not os.path.isdir(file_path):
                        continue
                    
                    # Parcourir les types de backup
                    for backup_type in os.listdir(file_path):
                        if type_filter and backup_type != type_filter:
                            continue
                            
                        type_path = os.path.join(file_path, backup_type)
                        if not os.path.isdir(type_path):
                            continue
                        
                        # Scanner les fichiers de sauvegarde
                        for backup_file in os.listdir(type_path):
                            backup_full_path = os.path.join(type_path, backup_file)
                            if not os.path.isfile(backup_full_path):
                                continue
                            
                            backup_info = self._get_or_create_backup_info_hierarchical(
                                backup_full_path, game_name, file_name, backup_type
                            )
                            if backup_info:
                                backups.append(backup_info)
            
            # Trier par date de création (plus récent en premier)
            backups.sort(key=lambda x: x['created'], reverse=True)
            
            # Sauvegarder dans le cache SI pas de filtres (cache complet uniquement)
            if game_filter is None and type_filter is None:
                self._cache_data = backups.copy()
                self._cache_timestamp = time.time()
                elapsed = time.time() - start_time
                log_message("DEBUG", f"Cache mis à jour: {len(backups)} sauvegardes chargées en {elapsed:.2f}s", category="backup_cache")
                
                # Sauvegarder sur disque pour persistance entre sessions
                self._save_persistent_cache()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur listage backups hiérarchiques: {e}", category="backup_listing")
        
        return backups
    
    def _get_or_create_backup_info_hierarchical(self, backup_path: str, game_name: str, 
                                              file_name: str, backup_type: str) -> Optional[Dict]:
        """Crée les infos de backup pour la structure hiérarchique (optimisé avec index)"""
        try:
            backup_filename = os.path.basename(backup_path)
            
            # Chercher dans l'index des métadonnées (O(1) au lieu de O(n))
            backup_id_from_index = self._metadata_index.get(backup_path)
            if backup_id_from_index:
                metadata = self.metadata.get(backup_id_from_index)
                if metadata:
                    return metadata
            
            # Si pas de métadonnées trouvées, chercher par pattern dans les métadonnées existantes
            # pour les sauvegardes récentes qui pourraient ne pas être dans l'index
            for backup_id, metadata in self.metadata.items():
                if (metadata.get('backup_path') == backup_path and 
                    metadata.get('game_name') == game_name and 
                    metadata.get('file_name') == file_name and 
                    metadata.get('type') == backup_type):
                    return metadata
            
            # Créer de nouvelles métadonnées seulement si aucune n'existe
            stats = os.stat(backup_path)
            created_time = datetime.datetime.fromtimestamp(stats.st_ctime)
            backup_id = f"{game_name}_{file_name}_{created_time.strftime('%Y%m%d_%H%M%S')}_{backup_type}"
            
            # Reconstruire le nom de fichier source
            source_filename = self._reconstruct_source_filename(backup_filename, file_name)
            
            backup_info = {
                'id': backup_id,
                'backup_path': backup_path,
                'game_name': game_name,
                'file_name': file_name,
                'type': backup_type,
                'created': created_time.isoformat(),
                'size': stats.st_size,
                'description': f"Sauvegarde {self.BACKUP_DESCRIPTIONS.get(backup_type, backup_type)}",
                'source_filename': source_filename,
                'backup_filename': backup_filename,
                'source_path': None  # À reconstruire à la demande
            }
            
            # Sauvegarder dans les métadonnées ET l'index
            self.metadata[backup_id] = backup_info
            self._metadata_index[backup_path] = backup_id
            return backup_info
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur création info backup hiérarchique {backup_path}: {e}", category="backup_listing")
            return None
    
    def _reconstruct_source_filename(self, backup_filename: str, file_name: str) -> str:
        """Reconstruit le nom de fichier source à partir du backup"""
        try:
            # Format: file_name_YYYYMMDD_HHMMSS.ext
            # Extraire l'extension
            backup_ext = Path(backup_filename).suffix
            
            # Le nom source est généralement le nom du fichier + extension
            if backup_ext:
                return f"{file_name}{backup_ext}"
            else:
                return f"{file_name}.rpy"  # Extension par défaut
                
        except Exception as e:
            log_message("ATTENTION", f"Erreur reconstruction nom source: {e}", category="backup_filename")
            return f"{file_name}.rpy"
    
    def get_backup_statistics(self) -> Dict[str, any]:
        """Calcule les statistiques des sauvegardes avec structure hiérarchique"""
        stats = {
            'total_backups': 0,
            'total_size': 0,
            'by_game': {},
            'by_type': {},
            'by_file': {},
            'oldest': None,
            'newest': None
        }
        
        try:
            all_backups = self.list_all_backups()
            stats['total_backups'] = len(all_backups)
            
            for backup in all_backups:
                # Taille totale
                stats['total_size'] += backup.get('size', 0)
                
                # Par jeu
                game = backup['game_name']
                if game not in stats['by_game']:
                    stats['by_game'][game] = {'count': 0, 'size': 0}
                stats['by_game'][game]['count'] += 1
                stats['by_game'][game]['size'] += backup.get('size', 0)
                
                # Par type
                backup_type = backup['type']
                if backup_type not in stats['by_type']:
                    stats['by_type'][backup_type] = 0
                stats['by_type'][backup_type] += 1
                
                # Par fichier
                file_name = backup.get('file_name', 'unknown')
                if file_name not in stats['by_file']:
                    stats['by_file'][file_name] = 0
                stats['by_file'][file_name] += 1
                
                # Dates
                created_date = backup['created']
                if not stats['oldest'] or created_date < stats['oldest']:
                    stats['oldest'] = created_date
                if not stats['newest'] or created_date > stats['newest']:
                    stats['newest'] = created_date
        
        except Exception as e:
            log_message("ERREUR", f"Erreur calcul statistiques hiérarchiques: {e}", category="backup_stats")
        
        return stats
    
    def cleanup_empty_folders(self):
        """Nettoie les dossiers vides dans la structure hiérarchique"""
        try:
            cleaned_count = 0
            
            # Parcourir tous les jeux
            for game_name in os.listdir(self.backup_root):
                game_path = os.path.join(self.backup_root, game_name)
                if not os.path.isdir(game_path):
                    continue
                
                # Parcourir tous les fichiers
                for file_name in os.listdir(game_path):
                    file_path = os.path.join(game_path, file_name)
                    if not os.path.isdir(file_path):
                        continue
                    
                    # Parcourir tous les types
                    for backup_type in os.listdir(file_path):
                        type_path = os.path.join(file_path, backup_type)
                        if os.path.isdir(type_path) and not os.listdir(type_path):
                            os.rmdir(type_path)
                            cleaned_count += 1
                            log_message("DEBUG", f"Dossier vide supprimé: {game_name}/{file_name}/{backup_type}", category="backup_cleanup")
                    
                    # Supprimer le dossier fichier s'il est vide
                    if os.path.isdir(file_path) and not os.listdir(file_path):
                        os.rmdir(file_path)
                        cleaned_count += 1
                        log_message("DEBUG", f"Dossier fichier vide supprimé: {game_name}/{file_name}", category="backup_cleanup")
                
                # Supprimer le dossier jeu s'il est vide
                if os.path.isdir(game_path) and not os.listdir(game_path):
                    os.rmdir(game_path)
                    cleaned_count += 1
                    log_message("DEBUG", f"Dossier jeu vide supprimé: {game_name}", category="backup_cleanup")
            
            if cleaned_count > 0:
                log_message("INFO", f"Nettoyage: {cleaned_count} dossiers vides supprimés", category="backup_cleanup")
            
            return cleaned_count
            
        except Exception as e:
            log_message("ERREUR", f"Erreur nettoyage dossiers vides: {e}", category="backup_cleanup")
            return 0
    
    def create_zip_backup(self, source_path: str, backup_type: str = BackupType.SECURITY,
                         description: str = None, override_game_name: str = None, 
                         override_file_name: str = None, include_patterns: list = None,
                         exclude_patterns: list = None) -> Dict[str, any]:
        """Crée une sauvegarde ZIP complète d'un dossier ou fichier
        
        Args:
            source_path: Chemin du fichier/dossier source à sauvegarder
            backup_type: Type de sauvegarde (BackupType.*)
            description: Description optionnelle
            override_game_name: Nom de jeu à utiliser au lieu de l'extraction automatique
            override_file_name: Nom de fichier à utiliser au lieu de l'extraction automatique
            include_patterns: Patterns d'inclusion (ex: ["**.rpy", "**.png"])
            exclude_patterns: Patterns d'exclusion (ex: ["**~", "**.bak"])
        """
        result = {
            'success': False,
            'backup_path': None,
            'backup_id': None,
            'error': None,
            'files_count': 0,
            'total_size': 0
        }
        
        try:
            if not source_path or not os.path.exists(source_path):
                result['error'] = "Fichier/dossier source introuvable"
                return result
            
            if backup_type not in self.BACKUP_DESCRIPTIONS:
                backup_type = BackupType.SECURITY
                log_message("ATTENTION", f"Type de backup invalide, utilisation de SECURITY par défaut", category="backup_zip")
            
            # Extraire le nom du jeu et du fichier (avec override si fourni)
            game_name = override_game_name if override_game_name else extract_game_name(source_path)
            file_name = override_file_name if override_file_name else Path(source_path).stem
            
            # Créer la structure hiérarchique: Game_name/file_name/backup_type/
            backup_folder = os.path.join(self.backup_root, game_name, file_name, backup_type)
            os.makedirs(backup_folder, exist_ok=True)
            
            timestamp = datetime.datetime.now()
            timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
            
            # Nom du fichier ZIP de sauvegarde
            zip_filename = f"{file_name}_{timestamp_str}.zip"
            zip_path = os.path.join(backup_folder, zip_filename)
            
            # Patterns par défaut si non fournis
            if include_patterns is None:
                include_patterns = [
                    "**.*"  # Tous les fichiers par défaut
                ]
            
            if exclude_patterns is None:
                exclude_patterns = [
                    "**~", "**.bak", "**/.**", "**/#**", "**/thumbs.db",
                    "**/__pycache__/**", "**/*.pyc"
                ]
            
            # Créer l'archive ZIP
            files_count = 0
            total_size = 0
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if os.path.isfile(source_path):
                    # Fichier unique
                    if self._should_include_file(os.path.basename(source_path), include_patterns, exclude_patterns):
                        zipf.write(source_path, os.path.basename(source_path))
                        files_count = 1
                        total_size = os.path.getsize(source_path)
                else:
                    # Dossier complet
                    for root, dirs, files in os.walk(source_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            
                            # Vérifier les patterns d'inclusion/exclusion
                            if self._should_include_file(file, include_patterns, exclude_patterns):
                                # Chemin relatif dans l'archive
                                arcname = os.path.relpath(file_path, source_path)
                                zipf.write(file_path, arcname)
                                files_count += 1
                                total_size += os.path.getsize(file_path)
            
            # Créer les métadonnées
            backup_id = f"{game_name}_{file_name}_{timestamp_str}_{backup_type}_zip"
            
            backup_metadata = {
                'id': backup_id,
                'source_path': source_path,
                'backup_path': zip_path,
                'game_name': game_name,
                'file_name': file_name,
                'type': backup_type,
                'created': timestamp.isoformat(),
                'size': os.path.getsize(zip_path),
                'description': description or f"Sauvegarde ZIP {self.BACKUP_DESCRIPTIONS[backup_type]}",
                'source_filename': os.path.basename(source_path),
                'backup_filename': zip_filename,
                'files_count': files_count,
                'total_size': total_size,
                'is_zip': True,
                'include_patterns': include_patterns,
                'exclude_patterns': exclude_patterns
            }
            
            self.metadata[backup_id] = backup_metadata
            self._save_metadata()
            
            result['success'] = True
            result['backup_path'] = zip_path
            result['backup_id'] = backup_id
            result['files_count'] = files_count
            result['total_size'] = total_size
            
            log_message("INFO", f"Backup ZIP créé: {game_name}/{file_name}/{backup_type}/{zip_filename} ({files_count} fichiers, {total_size} bytes)", category="backup_zip")
            
            # Invalider le cache après création d'une sauvegarde
            self._invalidate_cache()
            
        except Exception as e:
            result['error'] = str(e)
            log_message("ERREUR", f"Erreur création backup ZIP: {e}", category="backup_zip")
        
        return result
    
    def _should_include_file(self, filename: str, include_patterns: list, exclude_patterns: list) -> bool:
        """Vérifie si un fichier doit être inclus selon les patterns"""
        try:
            # Vérifier les patterns d'exclusion d'abord
            for pattern in exclude_patterns:
                if fnmatch.fnmatch(filename.lower(), pattern.lower()):
                    return False
            
            # Vérifier les patterns d'inclusion
            for pattern in include_patterns:
                if fnmatch.fnmatch(filename.lower(), pattern.lower()):
                    return True
            
            # Si aucun pattern d'inclusion ne correspond, exclure
            return False
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur vérification patterns pour {filename}: {e}", category="backup_zip")
            return True  # Inclure par défaut en cas d'erreur