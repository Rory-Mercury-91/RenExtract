# core/project_progress_tracker.py
# Système de suivi de progression pour dossiers de traduction
# Created for RenExtract 

"""
Système simple de suivi des fichiers .rpy traités dans un dossier de traduction
- Analyse les fichiers modifiés récemment
- Indicateurs visuels vert/gris
- Basé sur les timestamps de modification
"""

import os
import json
import datetime
from typing import Dict, List, Optional
from infrastructure.logging.logging import log_message
from infrastructure.config.config import config_manager

class TranslationProgressTracker:
    def __init__(self, project_path: str, language: str):
        """
        Initialise le tracker pour un projet + langue spécifique
        
        Args:
            project_path: Chemin vers le projet Ren'Py  
            language: Langue scannée (ex: "french")
        """
        self.project_path = os.path.normpath(project_path)
        self.language = language
        self.project_name = os.path.basename(self.project_path)
        
        # NOUVEAU: Stockage dans 01_Temporaires comme l'extraction
        from infrastructure.config.constants import FOLDERS

        project_root = os.path.normpath(project_path)
        game_name = os.path.basename(project_root) or "jeu_inconnu"
        
        # Structure: 01_Temporaires/GameName/translation_progress/french.json
        progress_dir = os.path.join(FOLDERS["temporaires"], game_name, "translation_progress")
        os.makedirs(progress_dir, exist_ok=True)
        
        self.progress_file = os.path.join(progress_dir, f"{language}.json")
        if not os.path.exists(self.progress_file):
            initial = self._create_initial_data()
            # Sauvegarde immédiate du fichier
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(initial, f, ensure_ascii=False, indent=2)

        self.data = self._load_or_initialize()
    
    def _safe_folder_name(self) -> str:
        """Génère un nom de fichier sécurisé"""
        safe_name = "".join(c for c in self.folder_name if c.isalnum() or c in ('-', '_'))
        return safe_name[:50] if safe_name else "translation_folder"
    
    def _load_or_initialize(self) -> Dict:
        """Charge ou initialise les données"""
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self._create_initial_data()
        except Exception as e:
            log_message("DEBUG", f"Erreur chargement progression: {e}", category="progress_tracker")
            return self._create_initial_data()
    
    def _create_initial_data(self) -> Dict:
        """Structure initiale autonome et sûre"""
        try:
            # Dossier tl/<langue> par défaut pour ce projet
            default_translation_folder = os.path.join(self.project_path, "game", "tl", self.language)
            folder_name = os.path.basename(default_translation_folder.rstrip(os.sep)) or self.language
        except Exception:
            default_translation_folder = ""
            folder_name = self.language

        return {
            "translation_folder": default_translation_folder,  # clé cohérente avec les usages plus bas
            "folder_name": folder_name,
            "last_scan": None,
            "files_status": {},
            "statistics": {
                "total_files": 0,
                "recently_modified": 0
            }
        }

    
    def _save_data(self):
        """Sauvegarde"""
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            log_message("DEBUG", f"Erreur sauvegarde progression: {e}", category="progress_tracker")
    
    def scan_translation_folder(self, translation_folder: str = None) -> Dict:
        """
        Scanne TOUT le dossier de traduction (incluant sous-dossiers).
        Si translation_folder est None, on prend game/tl/<langue>.
        """
        if not config_manager.get('project_progress_tracking', False):
            return {"tracking_disabled": True}

        try:
            if translation_folder is None:
                translation_folder = os.path.join(self.project_path, "game", "tl", self.language)

            if not os.path.exists(translation_folder):
                return {"error": "Dossier de traduction non trouvé"}
            
            # Scanner RÉCURSIVEMENT tous les .rpy (comme scan_language_files)
            all_rpy_files = []
            for root, dirs, files in os.walk(translation_folder):
                for file in files:
                    if file.lower().endswith('.rpy'):
                        full_path = os.path.join(root, file)
                        # Chemin relatif depuis la racine de la langue
                        relative_path = os.path.relpath(full_path, translation_folder)
                        all_rpy_files.append((relative_path, full_path))
            
            # Analyser tous les fichiers d'un coup
            recently_modified_count = 0
            reconstructed_count = 0
            cutoff_time = datetime.datetime.now() - datetime.timedelta(days=7)
            
            # RÉINITIALISER les données pour ce scan complet
            self.data["files_status"] = {}
            
            for relative_path, full_path in all_rpy_files:
                file_status = self._analyze_file(relative_path, full_path, cutoff_time)
                self.data["files_status"][relative_path] = file_status
                
                if file_status["recently_modified"]:
                    recently_modified_count += 1
                
                # ✅ NOUVEAU : Détecter les fichiers reconstruits
                if file_status.get("reconstructed", False):
                    reconstructed_count += 1
            
            # Stats globales
            old_reconstructed = self.data.get("statistics", {}).get("reconstructed", 0)
            
            self.data["statistics"] = {
                "total_files": len(all_rpy_files),
                "recently_modified": recently_modified_count,
                "reconstructed": reconstructed_count
            }
            self.data["last_scan"] = datetime.datetime.now().isoformat()
            self.data["translation_folder"] = translation_folder
            
            self._save_data()
            
            # Afficher le log seulement si le nombre de fichiers reconstruits a changé
            if reconstructed_count != old_reconstructed:
                log_message("INFO", 
                    f"📊 Progression {self.language}: {reconstructed_count}/{len(all_rpy_files)} fichiers complétés", 
                    category="progress_tracker")
            
            return {
                "total_found": len(all_rpy_files),
                "recently_modified": recently_modified_count,
                "reconstructed": reconstructed_count
            }
            
        except Exception as e:
            log_message("ERREUR", f"Erreur scan {self.language}: {e}", category="progress_tracker")
            return {"error": str(e)}
    
    def _analyze_file(self, filename: str, full_path: str, cutoff_time: datetime.datetime) -> Dict:
        """Analyse un fichier individuel"""
        try:
            stat = os.stat(full_path)
            modified_time = datetime.datetime.fromtimestamp(stat.st_mtime)
            
            # ✅ NOUVEAU : Détecter les fichiers reconstruits
            # Un fichier est considéré comme reconstruit s'il contient le marqueur spécifique
            is_reconstructed = False
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Chercher le marqueur spécifique ajouté lors de la reconstruction
                    if '# Fichier reconstruit après traduction par RenExtract le' in content:
                        is_reconstructed = True
            except Exception:
                # En cas d'erreur de lecture, on assume que ce n'est pas reconstruit
                pass
            
            return {
                "filename": filename,
                "size": stat.st_size,
                "modified": modified_time.isoformat(),
                "recently_modified": modified_time > cutoff_time,
                "reconstructed": is_reconstructed
            }
            
        except Exception as e:
            return {
                "filename": filename,
                "error": str(e),
                "recently_modified": False,
                "reconstructed": False
            }
    
    def get_file_status(self, filepath: str) -> str:
        """
        Obtient le statut d'un fichier (utilise le chemin relatif)
        """
        try:
            # Convertir en chemin relatif si nécessaire
            translation_folder = self.data.get('translation_folder', '')
            
            if os.path.isabs(filepath) and translation_folder:
                # Chemin absolu : convertir en relatif depuis le dossier de traduction
                relative_path = os.path.relpath(filepath, translation_folder)
            else:
                # Chemin déjà relatif ou juste un nom de fichier
                # On cherche d'abord avec le chemin tel quel
                relative_path = filepath
            
            # Normaliser le chemin (\ vers /)
            relative_path = relative_path.replace('\\', '/')
            
            # Chercher le fichier dans files_status
            file_status = self.data["files_status"].get(relative_path, {})
            
            # Si pas trouvé avec le chemin complet, essayer juste avec le nom du fichier
            if not file_status:
                filename_only = os.path.basename(filepath)
                for key, status in self.data["files_status"].items():
                    if os.path.basename(key) == filename_only:
                        file_status = status
                        break
            
            # Priorité 1: Fichier reconstruit (complété)
            if file_status.get("reconstructed", False):
                return "completed"
            # Priorité 2: Fichier récemment modifié
            elif file_status.get("recently_modified", False):
                return "recently_modified"
            # Priorité 3: Fichier plus ancien
            elif "modified" in file_status:
                return "older"
            else:
                return "unknown"
                
        except Exception:
            return "unknown"
    
    def get_statistics(self) -> Dict:
        """Statistiques"""
        return self.data.get("statistics", {
            "total_files": 0,
            "recently_modified": 0,
            "reconstructed": 0
        })

# Instance globale simplifiée
_current_tracker = None
_current_project = None
_current_language = None

def get_translation_tracker(project_path: str, language: str) -> Optional[TranslationProgressTracker]:
    """Obtient UN tracker par projet+langue"""
    global _current_tracker, _current_project, _current_language
    
    if not config_manager.get('project_progress_tracking', False):
        return None
    
    try:
        # Créer un nouveau tracker seulement si projet ou langue change
        if (_current_tracker is None or 
            _current_project != project_path or 
            _current_language != language):
            
            _current_tracker = TranslationProgressTracker(project_path, language)
            _current_project = project_path
            _current_language = language
            
            # Scanner immédiatement le dossier de langue complet
            language_folder = os.path.join(project_path, "game", "tl", language)
            if os.path.exists(language_folder):
                _current_tracker.scan_translation_folder(language_folder)
        
        return _current_tracker
    except Exception as e:
        log_message("DEBUG", f"Erreur création tracker: {e}", category="progress_tracker")
        return None