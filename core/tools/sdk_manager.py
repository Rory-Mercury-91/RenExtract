# core/tools/sdk_manager.py
# Gestionnaire SDK Ren'Py pour RenExtract
# Extrait de translation_generator.py et sup_lignes_orphelines.py

"""
Gestionnaire du SDK Ren'Py
- Téléchargement automatique du SDK intégré
- Validation des SDK existants
- Détection automatique des installations
- Sélection manuelle via interface
"""

import os
import sys
import glob
import subprocess
import tempfile
from typing import Optional, List, Dict, Any
from infrastructure.logging.logging import log_message
from infrastructure.config.config import config_manager
from .downloader import get_downloader


class SDKManager:
    """Gestionnaire du SDK Ren'Py"""
    
    def __init__(self, tools_dir: str = None):
        """
        Initialise le gestionnaire SDK
        
        Args:
            tools_dir: Répertoire pour stocker le SDK intégré
        """
        if tools_dir is None:
            from infrastructure.config.config import config_manager
            tools_dir = config_manager.get_tools_directory()
        
        self.tools_dir = tools_dir
        self.embedded_sdk_dir = os.path.join(tools_dir, "renpy_sdk_embedded")
        
        # Assurer que le dossier tools existe
        os.makedirs(tools_dir, exist_ok=True)
    
    def get_embedded_sdk_path(self) -> Optional[str]:
        """Retourne le chemin vers le SDK Ren'Py intégré s'il existe"""
        try:
            if os.path.exists(self.embedded_sdk_dir):
                for item in os.listdir(self.embedded_sdk_dir):
                    if item.startswith("renpy-") and item.endswith("-sdk"):
                        sdk_path = os.path.join(self.embedded_sdk_dir, item)
                        if os.path.isdir(sdk_path):
                            if self.validate_sdk_path(sdk_path):
                                return sdk_path
            
            return None
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur recherche SDK intégré: {e}", category="sdk_manager")
            return None
    
    def download_renpy_sdk(self, version: str = "8.3.7") -> Optional[str]:
        """
        Télécharge et installe le SDK Ren'Py intégré
        
        Args:
            version: Version du SDK à télécharger
            
        Returns:
            Chemin vers le SDK installé ou None si échec
        """
        try:
            sdk_folder_name = f"renpy-{version}-sdk"
            final_sdk_path = os.path.join(self.embedded_sdk_dir, sdk_folder_name)
            
            # Si déjà présent, le valider
            if os.path.exists(final_sdk_path):
                if self.validate_sdk_path(final_sdk_path):
                    log_message("INFO", f"SDK intégré {version} déjà installé et validé", category="sdk_manager")
                    return final_sdk_path
                else:
                    log_message("ATTENTION", f"SDK intégré corrompu, re-téléchargement...", category="sdk_manager")
                    self._cleanup_sdk_dir(final_sdk_path)
            
            log_message("INFO", f"Début téléchargement SDK Ren'Py {version} intégré", category="sdk_manager")
            
            # URL fixe pour la version spécifiée
            sdk_url = f"https://www.renpy.org/dl/{version}/renpy-{version}-sdk.zip"
            
            downloader = get_downloader()
            
            # Vérifier d'abord les informations du fichier distant
            info_result = downloader.get_download_info(sdk_url)
            if info_result['success']:
                size_mb = info_result['content_length'] / 1024 / 1024
                log_message("INFO", f"SDK distant détecté: {size_mb:.1f} MB", category="sdk_manager")
            
            # Télécharger le SDK (dossier temp selon config : app ou système)
            app_temp = config_manager.get_download_temp_dir()
            temp_zip_path = os.path.join(app_temp, "renpy_sdk_temp.zip")
            
            download_result = downloader.download_file(sdk_url, temp_zip_path, force_redownload=True)
            
            if not download_result['success']:
                raise Exception(f"Échec téléchargement SDK: {download_result['error']}")
            
            log_message("INFO", f"SDK téléchargé: {download_result['file_size']/1024/1024:.1f} MB", category="sdk_manager")
            
            log_message("INFO", "Extraction du SDK Ren'Py...", category="sdk_manager")
            
            # Créer le dossier de destination
            os.makedirs(self.embedded_sdk_dir, exist_ok=True)
            
            # Extraire le ZIP
            import zipfile
            with zipfile.ZipFile(temp_zip_path) as z:
                z.extractall(self.embedded_sdk_dir)
            
            # Valider l'installation
            if self.validate_sdk_path(final_sdk_path):
                log_message("INFO", f"SDK Ren'Py {version} installé et validé avec succès", category="sdk_manager")
                return final_sdk_path
            else:
                raise RuntimeError("SDK téléchargé mais validation échouée")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur téléchargement SDK intégré: {e}", category="sdk_manager")
            return None
        finally:
            # Nettoyer le fichier temporaire
            if 'temp_zip_path' in locals() and os.path.exists(temp_zip_path):
                try:
                    os.remove(temp_zip_path)
                except Exception:
                    pass
    
    def validate_sdk_path(self, sdk_path: str) -> bool:
        """
        Valide qu'un chemin contient un SDK Ren'Py fonctionnel
        
        Args:
            sdk_path: Chemin à valider
            
        Returns:
            True si le SDK est valide
        """
        try:
            if not os.path.isdir(sdk_path):
                return False
            
            # Chercher renpy.exe ou renpy.sh
            renpy_exe = os.path.join(sdk_path, "renpy.exe")
            renpy_sh = os.path.join(sdk_path, "renpy.sh")
            
            if os.path.exists(renpy_exe):
                return True
            elif os.path.exists(renpy_sh):
                return True
            else:
                return False
                
        except Exception as e:
            log_message("ATTENTION", f"Erreur validation SDK '{sdk_path}': {e}", category="sdk_manager")
            return False
    
    def detect_installed_sdks(self) -> List[str]:
        """
        Détecte automatiquement les installations Ren'Py sur le système
        
        Returns:
            Liste des chemins SDK trouvés
        """
        found_sdks = []
        
        try:
            # Chemins de recherche courants
            search_paths = [
                "C:/",
                "D:/",
                "C:/Program Files/",
                "C:/Program Files (x86)/",
                os.path.expanduser("~/Downloads/"),
                os.path.expanduser("~/Desktop/"),
                "E:/", "F:/", "G:/"  # Autres disques possibles
            ]
            
            # Patterns de noms de dossiers Ren'Py
            renpy_patterns = [
                "renpy*sdk*",
                "renpy-*",
                "*renpy*",
                "RenPy*"
            ]
            
            for base_path in search_paths:
                if not os.path.exists(base_path):
                    continue
                    
                for pattern in renpy_patterns:
                    search_pattern = os.path.join(base_path, pattern)
                    
                    try:
                        for folder in glob.glob(search_pattern):
                            if os.path.isdir(folder):
                                if self.validate_sdk_path(folder):
                                    found_sdks.append(folder)
                    except Exception:
                        continue
            
            # Retirer les doublons et trier
            found_sdks = list(set(found_sdks))
            found_sdks.sort()
            
            log_message("INFO", f"{len(found_sdks)} SDK(s) Ren'Py détecté(s)", category="sdk_manager")
            return found_sdks
                        
        except Exception as e:
            log_message("ATTENTION", f"Erreur auto-détection SDK : {e}", category="sdk_manager")
            return []
    
    def select_renpy_executable(self) -> Optional[str]:
        """
        Interface graphique pour sélectionner l'exécutable Ren'Py
        
        Returns:
            Chemin vers l'exécutable sélectionné ou None
        """
        try:
            import tkinter as tk
            from tkinter import filedialog, messagebox
            
            # Créer une fenêtre temporaire
            root = tk.Tk()
            root.withdraw()  # Cacher la fenêtre principale
            
            # Dialog de sélection de fichier
            exe_path = filedialog.askopenfilename(
                title="Sélectionner l'exécutable Ren'Py",
                filetypes=[
                    ("Exécutables Ren'Py", "renpy.exe"),
                    ("Tous les exécutables", "*.exe"),
                    ("Tous les fichiers", "*.*")
                ],
                initialdir="C:/",
            )
            
            root.destroy()
            
            if exe_path:
                # Valider que c'est bien un exécutable Ren'Py
                sdk_path = os.path.dirname(exe_path)
                if self.validate_sdk_path(sdk_path):
                    log_message("INFO", f"Exécutable Ren'Py sélectionné : {exe_path}", category="sdk_manager")
                    return exe_path
                else:
                    # ⚠️ Sévérité ajustée: ce n'est pas une erreur système, mais une mauvaise sélection utilisateur
                    log_message("ATTENTION", f"Fichier sélectionné non valide pour Ren'Py : {exe_path}", category="sdk_manager")
                    return None
            else:
                log_message("INFO", "Aucun exécutable sélectionné", category="sdk_manager")
                return None
                
        except Exception as e:
            log_message("ERREUR", f"Erreur sélection exécutable : {e}", category="sdk_manager")
            return None
    
    def get_sdk_for_cleaning(self) -> Optional[str]:
        """
        Retourne le SDK à utiliser pour le nettoyage avec priorité intégrée
        
        Returns:
            Chemin vers le SDK optimal ou None
        """
        
        
        # 1️⃣ PRIORITÉ 1: Essayer le SDK intégré existant
        embedded_sdk = self.get_embedded_sdk_path()
        if embedded_sdk:
            log_message("DEBUG", "SDK intégré", category="sdk_manager")
            return embedded_sdk
        
        # 2️⃣ PRIORITÉ 2: Essayer le SDK configuré dans settings
        try:
            from infrastructure.config.config import config_manager
            configured_sdk = config_manager.get('renpy_sdk_path', '')
            if configured_sdk and self.validate_sdk_path(configured_sdk):
                log_message("INFO", "Utilisation du SDK configuré dans settings", category="sdk_manager")
                return configured_sdk
            else:
                if configured_sdk:
                    log_message("ATTENTION", f"SDK configuré invalide: {configured_sdk}", category="sdk_manager")
        except Exception as e:
            pass
        
        # 3️⃣ DERNIER RECOURS: Télécharger le SDK intégré
        log_message("INFO", "Aucun SDK disponible → téléchargement automatique", category="sdk_manager")
        
        downloaded_sdk = self.download_renpy_sdk()
        if downloaded_sdk:
            log_message("INFO", "SDK intégré téléchargé et prêt à utiliser", category="sdk_manager")
            return downloaded_sdk
        else:
            log_message("ERREUR", "Échec complet: aucun SDK disponible pour le nettoyage", category="sdk_manager")
            return None
    
    def smart_sdk_selection(self, project_path: str, sdk_hint: str = None) -> Optional[str]:
        """
        Sélection intelligente de SDK avec fallback manuel
        
        Args:
            project_path: Chemin vers le projet
            sdk_hint: Suggestion de SDK à essayer d'abord
            
        Returns:
            Chemin vers le SDK sélectionné ou None
        """
        try:
            log_message("INFO", "Sélection intelligente du SDK...", category="sdk_manager")
            
            # 1️⃣ ESSAYER LE SDK SUGGÉRÉ D'ABORD
            if sdk_hint and os.path.exists(sdk_hint):
                if self.validate_sdk_path(sdk_hint):
                    log_message("INFO", f"Utilisation du SDK suggéré : {os.path.basename(sdk_hint)}", category="sdk_manager")
                    return sdk_hint
                else:
                    log_message("ATTENTION", "SDK suggéré invalide", category="sdk_manager")
            
            # 2️⃣ AUTO-DÉTECTION RAPIDE
            log_message("INFO", "Auto-détection rapide des SDK...", category="sdk_manager")
            auto_detected = self.detect_installed_sdks()
            
            if auto_detected:
                # Prendre le premier SDK valide trouvé
                selected_sdk = auto_detected[0]
                log_message("INFO", f"Utilisation du SDK auto-détecté : {os.path.basename(selected_sdk)}", category="sdk_manager")
                return selected_sdk
            
            # 3️⃣ DEMANDER À L'UTILISATEUR DE SÉLECTIONNER
            log_message("INFO", "Sélection manuelle requise...", category="sdk_manager")
            
            # Afficher une boîte de dialogue d'information
            try:
                import tkinter as tk
                from tkinter import messagebox
                
                root = tk.Tk()
                root.withdraw()
                
                message = """Auto-détection SDK échouée !
                
🎯 Veuillez sélectionner manuellement l'exécutable Ren'Py :
• Cherchez 'renpy.exe' dans votre installation Ren'Py
• Généralement dans un dossier comme 'renpy-X.X.X-sdk'

💡 Exemple : C:/renpy-8.3.2-sdk/renpy.exe"""
                
                messagebox.showinfo("Sélection SDK Ren'Py", message)
                root.destroy()
            except:
                pass
            
            # Lancer la sélection manuelle
            selected_exe = self.select_renpy_executable()
            
            if selected_exe:
                log_message("INFO", f"Exécutable sélectionné : {selected_exe}", category="sdk_manager")
                return os.path.dirname(selected_exe)  # Retourner le dossier SDK
            
            # 4️⃣ DERNIER RECOURS : SDK INTÉGRÉ
            log_message("INFO", "Téléchargement du SDK intégré...", category="sdk_manager")
            return self.download_renpy_sdk()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur sélection intelligente SDK : {e}", category="sdk_manager")
            return self.download_renpy_sdk()
    
    def get_renpy_executable(self, sdk_path: str) -> Optional[str]:
        """
        Retourne le chemin vers l'exécutable Ren'Py dans un SDK
        
        Args:
            sdk_path: Chemin vers le SDK
            
        Returns:
            Chemin vers renpy.exe/renpy.sh ou None
        """
        if not sdk_path or not os.path.exists(sdk_path):
            return None
        
        # Windows
        renpy_exe = os.path.join(sdk_path, "renpy.exe")
        if os.path.exists(renpy_exe):
            return renpy_exe
        
        # Linux/macOS
        renpy_sh = os.path.join(sdk_path, "renpy.sh")
        if os.path.exists(renpy_sh):
            return renpy_sh
        
        return None
    
    def _cleanup_sdk_dir(self, sdk_dir: str):
        """Nettoie un répertoire SDK"""
        try:
            if os.path.exists(sdk_dir):
                import shutil
                shutil.rmtree(sdk_dir)
        except Exception as e:
            # ⚠️ Sévérité ajustée: on signale le problème de nettoyage
            log_message("ATTENTION", f"Erreur nettoyage répertoire SDK : {e}", category="sdk_manager")
    
    def cleanup(self):
        """Nettoie les ressources du gestionnaire"""
        try:
            # Rien de spécifique à nettoyer pour l'instant
            pass
        except Exception as e:
            pass


# Instance globale pour réutilisation
_global_sdk_manager = None

def get_sdk_manager(tools_dir: str = None) -> SDKManager:
    """Retourne une instance globale du gestionnaire SDK"""
    global _global_sdk_manager
    if _global_sdk_manager is None:
        _global_sdk_manager = SDKManager(tools_dir)
    elif tools_dir:
        requested = os.path.normpath(tools_dir)
        current = os.path.normpath(_global_sdk_manager.tools_dir)
        if requested != current:
            _global_sdk_manager = SDKManager(tools_dir)
    return _global_sdk_manager
