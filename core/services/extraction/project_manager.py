# core/project_manager.py
# Gestionnaire centralisé de synchronisation des projets
# Created for RenExtract

"""
Gestionnaire de synchronisation des projets entre interfaces
Architecture asymétrique avec option utilisateur
"""

import os
from typing import Optional, Callable, List
from weakref import WeakMethod, ref
from infrastructure.logging.logging import log_message

class ProjectManager:
    """Gestionnaire centralisé de synchronisation des projets"""
    
    def __init__(self):
        self.current_project_path: Optional[str] = None
        self._listeners: List = []  # WeakRef des callbacks
        self._updating = False  # Protection contre boucles
        
        
    
    def is_sync_enabled(self) -> bool:
        """Vérifie si la synchronisation est activée"""
        try:
            from infrastructure.config.config import config_manager
            # ✅ AJOUT : Vérifier que config_manager n'est pas None
            if config_manager is None:
                log_message("ATTENTION", "config_manager est None, synchronisation désactivée", category="project_sync")
                return False
            return config_manager.get('project_sync_enabled', True)
        except Exception as e:
            log_message("ERREUR", f"Impossible d'accéder à config_manager: {e}", category="project_sync")
            return True  # Par défaut, activer la synchronisation
    
    def register_listener(self, callback: Callable[[str], None], source_name: str = "unknown"):
        """
        Enregistre un listener pour les changements de projet
        
        Args:
            callback: Fonction appelée lors d'un changement (new_path)
            source_name: Nom de la source pour le debug
        """
        try:
            # Créer une WeakRef appropriée selon le type
            if hasattr(callback, '__self__'):
                # Méthode liée
                weak_callback = WeakMethod(callback)
            else:
                # Fonction ou lambda
                weak_callback = ref(callback)
            
            self._listeners.append({
                'callback': weak_callback,
                'source': source_name
            })
            
            
        except Exception as e:
            log_message("ERREUR", f"Erreur enregistrement listener {source_name}: {e}", category="project_sync")
    
    def unregister_listener(self, source_name: str):
        """Désenregistre un listener par son nom"""
        try:
            self._listeners = [l for l in self._listeners if l['source'] != source_name]
            log_message("DEBUG", f"Listener désenregistré: {source_name}", category="project_sync")
        except Exception as e:
            log_message("ERREUR", f"Erreur désenregistrement listener: {e}", category="project_sync")
    
    def set_project(self, new_path: str, source: str = "unknown"):
        """
        Définit le projet actuel et notifie tous les listeners
        
        Args:
            new_path: Nouveau chemin du projet
            source: Source du changement (pour éviter notification en boucle)
        """
        try:
            
            
            # Protection contre boucles infinies
            if self._updating:
                log_message("DEBUG", "⚠️  Déjà en mise à jour, ignoré", category="project_sync")
                return
            
            # Vérifier si la synchronisation est activée
            if not self.is_sync_enabled():
                log_message("DEBUG", "❌ Synchronisation désactivée - changement ignoré", category="project_sync")
                return
            
            # Normaliser le chemin
            new_path = os.path.normpath(new_path) if new_path else ""
            
            
            # Ignorer si identique
            if new_path == self.current_project_path:
                log_message("DEBUG", f"✓ Projet identique, ignoré", category="project_sync")
                return
            
            # Valider le projet
            if new_path and not self._validate_project(new_path):
                log_message("ATTENTION", f"❌ Projet invalide ignoré: {new_path}", category="project_sync")
                log_message("DEBUG", f"   Raison: Le dossier n'est pas un projet Ren'Py valide", category="project_sync")
                return
            
            
            
            self._updating = True
            
            try:
                old_path = self.current_project_path
                self.current_project_path = new_path
                
                project_name = os.path.basename(new_path) if new_path else "Aucun"
                
                
                
                # Notifier tous les listeners sauf la source
                self._notify_listeners(new_path, source)
                
            finally:
                self._updating = False
                
        except Exception as e:
            self._updating = False
            log_message("ERREUR", f"Erreur set_project: {e}", category="project_sync")
    
    def _validate_project(self, project_path: str) -> bool:
        """Valide qu'un chemin est un projet Ren'Py valide"""
        try:
            from ui.shared.project_utils import validate_renpy_project
            return validate_renpy_project(project_path)
        except Exception as e:
            log_message("DEBUG", f"Erreur validation projet: {e}", category="project_sync")
            return False
    
    def _notify_listeners(self, new_path: str, source: str):
        """Notifie tous les listeners du changement"""
        # Nettoyer les références mortes
        initial_count = len(self._listeners)
        self._listeners = [l for l in self._listeners if l['callback']() is not None]
        cleaned_count = len(self._listeners)
        
        if initial_count != cleaned_count:
            log_message("DEBUG", f"🧹 {initial_count - cleaned_count} listener(s) mort(s) nettoyé(s)", category="project_sync")
        
        
        notified_count = 0
        for listener in self._listeners:
            # Ne pas notifier la source du changement
            if listener['source'] == source:
                continue
            
            try:
                callback = listener['callback']()
                if callback:
                    log_message("DEBUG", f"   → Notification '{listener['source']}'...", category="project_sync")
                    callback(new_path)
                    notified_count += 1
                    log_message("DEBUG", f"   ✅ '{listener['source']}' notifié", category="project_sync")
                else:
                    log_message("DEBUG", f"   ⚠️  '{listener['source']}' callback None", category="project_sync")
            except Exception as e:
                log_message("ERREUR", f"❌ Erreur notification '{listener['source']}': {e}", category="project_sync")
        
    
    def get_current_project(self) -> Optional[str]:
        """Retourne le projet actuellement sélectionné"""
        return self.current_project_path
    
    def has_project(self) -> bool:
        """Vérifie si un projet est défini"""
        return bool(self.current_project_path)
    
    def clear_project(self, source: str = "unknown"):
        """Efface le projet actuel"""
        self.set_project("", source)
    
    def get_listener_count(self) -> int:
        """Retourne le nombre de listeners actifs"""
        # Nettoyer d'abord les références mortes
        self._listeners = [l for l in self._listeners if l['callback']() is not None]
        return len(self._listeners)
    
    def get_listeners_info(self) -> List[str]:
        """Retourne la liste des noms des listeners actifs"""
        self._listeners = [l for l in self._listeners if l['callback']() is not None]
        return [l['source'] for l in self._listeners]