# core/tools/python_manager.py
# Gestionnaire Python embedded pour RenExtract
# Extrait de translation_generator.py

"""
Gestionnaire des environnements Python embedded
- Configuration Python 2.7 et 3.11 embedded
- Sélection automatique du Python optimal selon la tâche
- Tests de compatibilité
- Détection des Python intégrés aux jeux Ren'Py
"""

import os
import sys
import subprocess
import tempfile
from typing import Optional, Dict, Any
from infrastructure.logging.logging import log_message
from .downloader import get_downloader


class PythonManager:
    """Gestionnaire des environnements Python embedded"""
    
    def __init__(self, tools_dir: str = None):
        """
        Initialise le gestionnaire Python
        
        Args:
            tools_dir: Répertoire pour stocker les Python embedded
        """
        if tools_dir is None:
            tools_dir = os.path.join(os.path.expanduser("~"), ".renextract_tools")
        
        self.tools_dir = tools_dir
        self.python_embed_dir = os.path.join(tools_dir, "python_embed_3")
        self.python27_embed_dir = os.path.join(tools_dir, "python_embed_2")
        
        # Chemins vers les exécutables
        self.universal_python_exe = None
        self.python27_embedded_exe = None
        
        # Assurer que le dossier tools existe
        os.makedirs(tools_dir, exist_ok=True)
    
    def setup_python_embedded(self) -> Optional[str]:
        """
        Télécharge et configure Python Embedded 3.11 pour compatibilité universelle
        
        Returns:
            Chemin vers python.exe ou None si échec
        """
        python_exe = os.path.join(self.python_embed_dir, "python.exe")
        
        # Si Python Embedded existe déjà, vérifier qu'il fonctionne
        if os.path.exists(python_exe):
            if self._test_python_executable(python_exe):
                log_message("INFO", "Python Embedded 3.11 trouvé et fonctionnel", category="python_setup_3")
                self.universal_python_exe = python_exe
                return python_exe
            else:
                log_message("ATTENTION", "Python Embedded 3.11 défaillant, re-téléchargement...", category="python_setup_3")
                self._cleanup_python_dir(self.python_embed_dir)
        
        # Télécharger Python Embedded 3.11
        log_message("INFO", "Téléchargement de Python Embedded 3.11 pour compatibilité universelle...", category="python_setup_3")
        
        # URL pour Python 3.11.9 Embedded (x64)
        python_url = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip"
        
        try:
            downloader = get_downloader()
            
            # Télécharger et extraire directement dans le dossier python_embed_3
            temp_zip_path = os.path.join(tempfile.gettempdir(), "python_embed_3.zip")
            
            # Télécharger le fichier
            download_result = downloader.download_file(python_url, temp_zip_path, force_redownload=True)
            
            if not download_result['success']:
                raise Exception(f"Échec téléchargement Python 3.11: {download_result['error']}")
            
            log_message("INFO", "Extraction de Python Embedded 3.11...", category="python_setup_3")
            
            # Extraire directement dans le dossier python_embed_3
            os.makedirs(self.python_embed_dir, exist_ok=True)
            import zipfile
            with zipfile.ZipFile(temp_zip_path) as z:
                z.extractall(self.python_embed_dir)
            
            # Configurer Python Embedded pour les imports
            self._configure_python_embedded(self.python_embed_dir)
            
            # Vérifier que Python fonctionne
            if self._test_python_executable(python_exe):
                log_message("INFO", "Python Embedded 3.11 installé avec succès", category="python_setup_3")
                self.universal_python_exe = python_exe
                
                # Installer pip si nécessaire
                self._setup_embedded_pip(python_exe)
                
                return python_exe
            else:
                raise RuntimeError("Python Embedded 3.11 ne fonctionne pas après installation")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur installation Python Embedded 3.11 : {e}", category="python_setup_3")
            self._cleanup_python_dir(self.python_embed_dir)
            return None
        finally:
            # Nettoyer le fichier temporaire
            if 'temp_zip_path' in locals() and os.path.exists(temp_zip_path):
                try:
                    os.remove(temp_zip_path)
                except Exception:
                    pass
    
    def setup_python27_embedded(self) -> Optional[str]:
        """
        Télécharge et configure Python 2.7 Embedded pour unrpyc v1 (Ren'Py 6/7)
        
        Returns:
            Chemin vers python.exe ou None si échec
        """
        python27_exe = os.path.join(self.python27_embed_dir, "App", "Python", "python.exe")
        
        # Si Python 2.7 Embedded existe déjà, vérifier qu'il fonctionne
        if os.path.exists(python27_exe):
            if self._test_python_executable(python27_exe, expected_version="2.7"):
                log_message("DEBUG", "Python Embedded 2.7 trouvé et fonctionnel", category="python_setup_2")
                self.python27_embedded_exe = python27_exe
                return python27_exe
            else:
                log_message("ATTENTION", "Python Embedded 2.7 défaillant, re-téléchargement...", category="python_setup_2")
                self._cleanup_python_dir(self.python27_embed_dir)
        
        # Télécharger Python 2.7 Embedded
        log_message("INFO", "Téléchargement de Python Embedded 2.7...", category="python_setup_2")
        
        python27_url = "https://github.com/Rory-Mercury-91/python/releases/download/0.1/Python2.7.zip"
        
        try:
            downloader = get_downloader()
            
            # Télécharger et extraire
            temp_zip_path = os.path.join(tempfile.gettempdir(), "python27_embed.zip")
            
            download_result = downloader.download_file(python27_url, temp_zip_path, force_redownload=True)
            
            if not download_result['success']:
                raise Exception(f"Échec téléchargement Python 2.7: {download_result['error']}")
            
            # Extraire dans le dossier python_embed_2
            os.makedirs(self.python27_embed_dir, exist_ok=True)
            import zipfile
            with zipfile.ZipFile(temp_zip_path) as z:
                z.extractall(self.python27_embed_dir)
            
            # Vérifier que Python 2.7 fonctionne
            if self._test_python_executable(python27_exe, expected_version="2.7"):
                log_message("INFO", "Python Embedded 2.7 installé avec succès", category="python_setup_2")
                self.python27_embedded_exe = python27_exe
                return python27_exe
            else:
                raise RuntimeError("Python Embedded 2.7 ne fonctionne pas")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur installation Python Embedded 2.7 : {e}", category="python_setup_2")
            self._cleanup_python_dir(self.python27_embed_dir)
            return None
        finally:
            if 'temp_zip_path' in locals() and os.path.exists(temp_zip_path):
                try:
                    os.remove(temp_zip_path)
                except Exception:
                    pass
    
    def get_best_python_for_task(self, task: str, project_path: str = None, unrpyc_version: str = None) -> Optional[str]:
        """
        Détermine le meilleur Python à utiliser selon la tâche
        
        Args:
            task: Type de tâche ("rpatool", "unrpyc", etc.)
            project_path: Chemin vers le projet (pour détecter Python embarqué)
            unrpyc_version: Version unrpyc si spécifiée ("v1" ou "v2")
            
        Returns:
            Chemin vers l'exécutable Python optimal ou None
        """
        log_message("DEBUG", f"Sélection Python pour tâche: {task}", category="python_selection")
        
        if task == "rpatool":
            # RPATOOL : Toujours utiliser Python 3.11 Embedded
            if not self.universal_python_exe:
                self.universal_python_exe = self.setup_python_embedded()
            
            if self.universal_python_exe:
                log_message("INFO", "Utilisation de Python 3.11 Embedded pour rpatool", category="python_selection")
                return self.universal_python_exe
            
        elif task == "unrpyc":
            # UNRPYC : Utiliser les versions embedded en priorité
            
            # Si version fournie directement, l'utiliser
            if unrpyc_version:
                target_version = unrpyc_version
            else:
                # Sinon détecter la version (nécessite une logique externe)
                target_version = 'v2'  # Par défaut v2
            
            if target_version == 'v1':
                # Ren'Py 6/7 -> Python 2.7 Embedded
                if not self.python27_embedded_exe:
                    self.python27_embedded_exe = self.setup_python27_embedded()
                
                if self.python27_embedded_exe:
                    log_message("INFO", "Utilisation de Python 2.7 Embedded pour unrpyc v1", category="python_selection")
                    return self.python27_embedded_exe
                else:
                    log_message("ATTENTION", "Python 2.7 Embedded non disponible, fallback vers Python 3.11", category="python_selection")
                    # Fallback vers Python 3.11
                    if not self.universal_python_exe:
                        self.universal_python_exe = self.setup_python_embedded()
                    return self.universal_python_exe
            else:
                # Ren'Py 8+ -> Priorité Python du jeu, sinon Python 3.11 Embedded
                if project_path:
                    embedded_python = self.detect_embedded_python(project_path)
                    if embedded_python and self._test_python_compatibility(embedded_python, task):
                        log_message("INFO", "Utilisation du Python embarqué du jeu pour unrpyc v2", category="python_selection")
                        return embedded_python
                
                # Fallback vers Python 3.11 Embedded
                if not self.universal_python_exe:
                    self.universal_python_exe = self.setup_python_embedded()
                
                if self.universal_python_exe:
                    log_message("INFO", "Utilisation de Python 3.11 Embedded pour unrpyc v2", category="python_selection")
                    return self.universal_python_exe
        
        # Par défaut : Python 3.11 Embedded
        if not self.universal_python_exe:
            self.universal_python_exe = self.setup_python_embedded()
        
        return self.universal_python_exe
    
    def detect_embedded_python(self, project_path: str) -> Optional[str]:
        """
        Détecte l'exécutable Python embarqué dans le dossier 'lib' du jeu
        
        Args:
            project_path: Chemin vers le projet Ren'Py
            
        Returns:
            Chemin vers python.exe ou None
        """
        log_message("DEBUG", "Recherche du Python embarqué dans le dossier 'lib' du jeu...", category="embedded_detect")
        lib_path = os.path.join(project_path, "lib")
        
        if not os.path.isdir(lib_path):
            log_message("DEBUG", "Dossier 'lib' non trouvé.", category="embedded_detect")
            return None

        possible_paths = [
            os.path.join(lib_path, "py3-windows-x86_64", "python.exe"),
            os.path.join(lib_path, "py2-windows-x86_64", "python.exe"),
            os.path.join(lib_path, "windows-x86_64", "python.exe"),
            os.path.join(lib_path, "py3-windows-i686", "python.exe"),
            os.path.join(lib_path, "py2-windows-i686", "python.exe"),
            os.path.join(lib_path, "windows-i686", "python.exe"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                if self._test_python_executable(path):
                    log_message("DEBUG", f"Python embarqué fonctionnel trouvé : {os.path.basename(os.path.dirname(path))}", category="embedded_detect")
                    return path
                else:
                    log_message("DEBUG", f"Python embarqué non fonctionnel : {path}", category="embedded_detect")

        log_message("DEBUG", "Aucun Python embarqué fonctionnel trouvé.", category="embedded_detect")
        return None
    
    def _test_python_executable(self, python_exe: str, expected_version: str = None) -> bool:
        """
        Teste si un exécutable Python fonctionne
        
        Args:
            python_exe: Chemin vers l'exécutable Python
            expected_version: Version attendue ("2.7" ou "3.11")
            
        Returns:
            True si l'exécutable fonctionne
        """
        try:
            # ✅ CORRECTION : Masquer la fenêtre console sur Windows
            creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            
            result = subprocess.run(
                [python_exe, "--version"], 
                capture_output=True, 
                text=True, 
                timeout=5,
                creationflags=creationflags
            )
            
            if result.returncode == 0:
                # Python 2.7 affiche la version sur stderr, Python 3+ sur stdout
                version_output = result.stdout or result.stderr
                
                if expected_version:
                    if expected_version in version_output:
                        log_message("DEBUG", f"Python testé avec succès : {version_output.strip()}", category="python_test")
                        return True
                    else:
                        log_message("DEBUG", f"Version Python incorrecte : attendu {expected_version}, trouvé {version_output.strip()}", category="python_test")
                        return False
                else:
                    log_message("DEBUG", f"Python testé avec succès : {version_output.strip()}", category="python_test")
                    return True
            else:
                log_message("DEBUG", f"Échec test Python : code {result.returncode}", category="python_test")
                return False
                
        except subprocess.TimeoutExpired:
            log_message("DEBUG", "Timeout test Python", category="python_test")
            return False
        except Exception as e:
            log_message("DEBUG", f"Erreur test Python: {e}", category="python_test")
            return False
    
    def _test_python_compatibility(self, python_exe: str, task: str) -> bool:
        """
        Teste si un Python est vraiment compatible pour une tâche donnée
        
        Args:
            python_exe: Chemin vers l'exécutable Python
            task: Type de tâche
            
        Returns:
            True si compatible
        """
        try:
            log_message("DEBUG", f"Test de compatibilité Python pour {task}...", category="python_compat")
            
            if task == "unrpyc":
                # Test spécifique pour unrpyc : essayer d'importer les modules critiques
                test_script = """
import sys
try:
    import argparse
    import ast
    import codecs
    print("COMPAT_OK")
except Exception as e:
    print("COMPAT_FAIL:" + str(e))
    sys.exit(1)
"""
            else:
                # Test générique
                test_script = 'print("COMPAT_OK")'
            
            # Environnement ultra-propre pour le test
            clean_env = {
                'PATH': os.environ.get('PATH', ''),
                'SYSTEMROOT': os.environ.get('SYSTEMROOT', ''),
                'PYTHONDONTWRITEBYTECODE': '1',
                'PYTHONNOUSERSITE': '1'  # Ignorer les packages utilisateur
            }
            
            # Retirer explicitement les variables Python problématiques
            for key in ['PYTHONPATH', 'PYTHONHOME', 'PYTHON', 'PYTHONSTARTUP']:
                clean_env.pop(key, None)
            
            startupinfo = None
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
            
            # Test rapide (2 secondes max)
            # ✅ CORRECTION : Masquer la fenêtre console sur Windows
            creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            
            result = subprocess.run(
                [python_exe, "-c", test_script],
                capture_output=True,
                text=True,
                timeout=2,
                env=clean_env,
                startupinfo=startupinfo,
                creationflags=creationflags
            )
            
            if result.returncode == 0 and "COMPAT_OK" in result.stdout:
                log_message("DEBUG", f"Python compatible pour {task}", category="python_compat")
                return True
            else:
                log_message("DEBUG", f"Python incompatible pour {task}: {result.stderr[:100]}", category="python_compat")
                return False
                
        except subprocess.TimeoutExpired:
            log_message("DEBUG", f"Timeout test Python pour {task}", category="python_compat")
            return False
        except Exception as e:
            log_message("DEBUG", f"Erreur test Python pour {task}: {e}", category="python_compat")
            return False
    
    def _configure_python_embedded(self, python_dir: str):
        """Configure Python Embedded pour les imports"""
        try:
            pth_file = os.path.join(python_dir, "python311._pth")
            if os.path.exists(pth_file):
                # Modifier le .pth pour permettre l'importation des modules
                with open(pth_file, 'r') as f:
                    content = f.read()
                
                # Ajouter les chemins nécessaires
                if "#import site" in content:
                    content = content.replace("#import site", "import site")
                    with open(pth_file, 'w') as f:
                        f.write(content)
                    log_message("DEBUG", "Python Embedded configuré pour les imports", category="python_config")
        except Exception as e:
            log_message("DEBUG", f"Erreur configuration Python Embedded : {e}", category="python_config")
    
    def _setup_embedded_pip(self, python_exe: str):
        """Configure pip dans Python Embedded (optionnel)"""
        try:
            log_message("DEBUG", "Configuration de pip dans Python Embedded...", category="pip_setup")
            
            # Télécharger get-pip.py
            get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
            get_pip_path = os.path.join(os.path.dirname(python_exe), "get-pip.py")
            
            downloader = get_downloader()
            download_result = downloader.download_file(get_pip_url, get_pip_path)
            
            if download_result['success']:
                # Installer pip (sans fenêtre console)
                creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
                subprocess.run([python_exe, get_pip_path], 
                             capture_output=True, timeout=120, cwd=os.path.dirname(python_exe),
                             creationflags=creationflags)
                
                # Nettoyer
                if os.path.exists(get_pip_path):
                    os.remove(get_pip_path)
                    
                log_message("DEBUG", "Pip configuré avec succès", category="pip_setup")
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur configuration pip : {e} (non critique)", category="pip_setup")
    
    def _cleanup_python_dir(self, python_dir: str):
        """Nettoie un répertoire Python"""
        try:
            if os.path.exists(python_dir):
                import shutil
                shutil.rmtree(python_dir)
                log_message("DEBUG", f"Répertoire Python nettoyé : {os.path.basename(python_dir)}", category="cleanup")
        except Exception as e:
            log_message("DEBUG", f"Erreur nettoyage répertoire Python : {e}", category="cleanup")
    
    def cleanup(self):
        """Nettoie les ressources du gestionnaire"""
        try:
            # Rien de spécifique à nettoyer pour l'instant
            log_message("DEBUG", "PythonManager nettoyé", category="cleanup")
        except Exception as e:
            log_message("DEBUG", f"Erreur nettoyage PythonManager : {e}", category="cleanup")


# Instance globale pour réutilisation
_global_python_manager = None

def get_python_manager(tools_dir: str = None) -> PythonManager:
    """Retourne une instance globale du gestionnaire Python"""
    global _global_python_manager
    if _global_python_manager is None:
        _global_python_manager = PythonManager(tools_dir)
    return _global_python_manager
