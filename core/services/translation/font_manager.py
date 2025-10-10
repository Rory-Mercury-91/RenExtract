# core/business/font_manager.py
"""
Gestionnaire centralisé des polices pour RenExtract
Gère les polices système et personnalisées dans .renextract_tools/fonts/
"""

import os
import json
import shutil
import threading
import platform
from pathlib import Path
from typing import Dict, List, Optional, Callable
from infrastructure.logging.logging import log_message

class FontManager:
    """Gestionnaire centralisé des polices système et personnalisées"""
    
    def __init__(self, tools_dir: str):
        self.tools_dir = Path(tools_dir)
        self.fonts_dir = self.tools_dir / "fonts"
        self.system_fonts_dir = self.fonts_dir / "system_fonts"
        self.custom_fonts_dir = self.fonts_dir / "custom_fonts"
        self.cache_file = self.fonts_dir / "font_cache.json"
        
        # Créer les dossiers
        self.fonts_dir.mkdir(parents=True, exist_ok=True)
        self.system_fonts_dir.mkdir(parents=True, exist_ok=True)
        self.custom_fonts_dir.mkdir(parents=True, exist_ok=True)
        
        # État du scan
        self.scan_in_progress = False
        self.scan_callback = None
        
        # Log supprimé : sera affiché seulement après le scan complet
    
    def get_system_font_sources(self) -> List[Dict]:
        """Retourne les sources de polices système selon l'OS"""
        system = platform.system().lower()
        
        if system == "windows":
            return [
                {"name": "Arial", "filename": "arial.ttf", "path": "C:/Windows/Fonts/arial.ttf"},
                {"name": "Calibri", "filename": "calibri.ttf", "path": "C:/Windows/Fonts/calibri.ttf"},
                {"name": "Segoe UI", "filename": "segoeui.ttf", "path": "C:/Windows/Fonts/segoeui.ttf"},
                {"name": "Verdana", "filename": "verdana.ttf", "path": "C:/Windows/Fonts/verdana.ttf"},
                {"name": "Tahoma", "filename": "tahoma.ttf", "path": "C:/Windows/Fonts/tahoma.ttf"},
                {"name": "Times New Roman", "filename": "times.ttf", "path": "C:/Windows/Fonts/times.ttf"},
                {"name": "Georgia", "filename": "georgia.ttf", "path": "C:/Windows/Fonts/georgia.ttf"},
                {"name": "Comic Sans MS", "filename": "comic.ttf", "path": "C:/Windows/Fonts/comic.ttf"},
                {"name": "Impact", "filename": "impact.ttf", "path": "C:/Windows/Fonts/impact.ttf"},
                {"name": "Trebuchet MS", "filename": "trebuc.ttf", "path": "C:/Windows/Fonts/trebuc.ttf"}
            ]
        elif system == "darwin":  # macOS
            return [
                {"name": "Helvetica", "filename": "Helvetica.ttc", "path": "/System/Library/Fonts/Helvetica.ttc"},
                {"name": "Arial", "filename": "Arial.ttf", "path": "/System/Library/Fonts/Arial.ttf"},
                {"name": "Times", "filename": "Times.ttc", "path": "/System/Library/Fonts/Times.ttc"},
                {"name": "Courier", "filename": "Courier.ttc", "path": "/System/Library/Fonts/Courier.ttc"},
                {"name": "Georgia", "filename": "Georgia.ttf", "path": "/System/Library/Fonts/Georgia.ttf"}
            ]
        else:  # Linux
            return [
                {"name": "DejaVu Sans", "filename": "DejaVuSans.ttf", "path": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"},
                {"name": "Liberation Sans", "filename": "LiberationSans-Regular.ttf", "path": "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"},
                {"name": "Ubuntu", "filename": "Ubuntu-R.ttf", "path": "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf"},
                {"name": "Noto Sans", "filename": "NotoSans-Regular.ttf", "path": "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"}
            ]
    
    def scan_and_copy_system_fonts_async(self, callback: Optional[Callable] = None):
        """Lance le scan des polices système en arrière-plan"""
        if self.scan_in_progress:
            return
        
        self.scan_callback = callback
        thread = threading.Thread(target=self._scan_system_fonts_worker, daemon=True)
        thread.start()
    
    def _scan_system_fonts_worker(self):
        """Worker thread pour scanner et copier les polices système"""
        try:
            self.scan_in_progress = True
            # Log supprimé : sera regroupé avec le résultat final
            
            system_sources = self.get_system_font_sources()
            copied_count = 0
            
            for font_info in system_sources:
                source_path = Path(font_info["path"])
                if source_path.exists():
                    target_path = self.system_fonts_dir / font_info["filename"]
                    
                    # Copier seulement si absent ou différent
                    if not target_path.exists() or target_path.stat().st_size != source_path.stat().st_size:
                        try:
                            shutil.copy2(source_path, target_path)
                            copied_count += 1
                            log_message("DEBUG", f"Police copiée : {font_info['name']}", category="font_manager")
                        except Exception as e:
                            log_message("ATTENTION", f"Erreur copie {font_info['name']} : {e}", category="font_manager")
            
            # Mettre à jour le cache
            self._update_font_cache()
            
            log_message("INFO", f"✅ FontManager prêt ({copied_count} polices système)", category="font_manager")
            
            # Notifier l'interface
            if self.scan_callback:
                self.scan_callback(True, f"{copied_count} polices système récupérées")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur scan polices système : {e}", category="font_manager")
            if self.scan_callback:
                self.scan_callback(False, f"Erreur scan : {e}")
        finally:
            self.scan_in_progress = False
    
    def add_custom_font(self, source_font_path: str) -> tuple[bool, str]:
        """Ajoute une police personnalisée au dossier central"""
        try:
            source_path = Path(source_font_path)
            if not source_path.exists():
                return False, "Fichier de police introuvable"
            
            # Vérifier l'extension
            if source_path.suffix.lower() not in ['.ttf', '.otf', '.woff', '.woff2']:
                return False, "Format de police non supporté"
            
            # Copier vers le dossier custom
            target_path = self.custom_fonts_dir / source_path.name
            
            # Éviter les doublons
            if target_path.exists():
                if target_path.stat().st_size == source_path.stat().st_size:
                    return True, f"Police '{source_path.stem}' déjà présente"
            
            shutil.copy2(source_path, target_path)
            
            # Mettre à jour le cache
            self._update_font_cache()
            
            log_message("INFO", f"Police personnalisée ajoutée : {source_path.name}", category="font_manager")
            return True, f"Police '{source_path.stem}' ajoutée avec succès"
            
        except Exception as e:
            log_message("ERREUR", f"Erreur ajout police personnalisée : {e}", category="font_manager")
            return False, str(e)
    
    def get_all_available_fonts(self) -> List[Dict]:
        """Retourne toutes les polices disponibles (système + personnalisées)"""
        fonts = []
        
        # Polices système
        for font_file in self.system_fonts_dir.glob("*"):
            if font_file.suffix.lower() in ['.ttf', '.otf', '.woff', '.woff2']:
                font_name = self._get_font_display_name(font_file.stem)
                fonts.append({
                    'name': font_name,
                    'path': str(font_file),
                    'filename': font_file.name,
                    'type': 'system',
                    'description': f"Police système : {font_name}",
                    'available': True
                })
        
        # Polices personnalisées
        for font_file in self.custom_fonts_dir.glob("*"):
            if font_file.suffix.lower() in ['.ttf', '.otf', '.woff', '.woff2']:
                font_name = font_file.stem
                fonts.append({
                    'name': font_name,
                    'path': str(font_file),
                    'filename': font_file.name,
                    'type': 'custom',
                    'description': f"Police personnalisée : {font_name}",
                    'available': True
                })
        
        # Trier par nom
        fonts.sort(key=lambda x: x['name'].lower())
        return fonts
    
    def _get_font_display_name(self, filename_stem: str) -> str:
        """Convertit un nom de fichier en nom d'affichage"""
        name_mapping = {
            'arial': 'Arial',
            'calibri': 'Calibri',
            'segoeui': 'Segoe UI',
            'verdana': 'Verdana',
            'tahoma': 'Tahoma',
            'times': 'Times New Roman',
            'georgia': 'Georgia',
            'comic': 'Comic Sans MS',
            'impact': 'Impact',
            'trebuc': 'Trebuchet MS'
        }
        return name_mapping.get(filename_stem.lower(), filename_stem.replace('_', ' ').title())
    
    def _update_font_cache(self):
        """Met à jour le cache des polices"""
        try:
            cache_data = {
                'last_updated': str(Path()),
                'system_fonts_count': len(list(self.system_fonts_dir.glob("*"))),
                'custom_fonts_count': len(list(self.custom_fonts_dir.glob("*"))),
                'total_fonts': len(self.get_all_available_fonts())
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
                
        except Exception as e:
            log_message("ATTENTION", f"Erreur mise à jour cache polices : {e}", category="font_manager")
    
    def get_font_for_project(self, font_name: str, font_type: str = None) -> Optional[str]:
        """Retourne le chemin d'une police pour utilisation dans un projet"""
        all_fonts = self.get_all_available_fonts()
        
        for font in all_fonts:
            if font['name'] == font_name:
                return font['path']
        
        return None
    
    def remove_custom_font(self, font_name: str) -> tuple[bool, str]:
        """Supprime une police personnalisée"""
        try:
            for font_file in self.custom_fonts_dir.glob("*"):
                if font_file.stem == font_name:
                    font_file.unlink()
                    self._update_font_cache()
                    log_message("INFO", f"Police personnalisée supprimée : {font_name}", category="font_manager")
                    return True, f"Police '{font_name}' supprimée"
            
            return False, f"Police '{font_name}' introuvable"
            
        except Exception as e:
            log_message("ERREUR", f"Erreur suppression police : {e}", category="font_manager")
            return False, str(e)