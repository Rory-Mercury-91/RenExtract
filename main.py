# main.py
# RenExtract - Point d'entrée

"""
RenExtract
Outil de traduction avancé pour les scripts Ren'Py
Version allégée : pont de logging, imports via __init__, i18n et UI.
"""

import sys
import logging
import tkinter as tk
import threading
import subprocess
import os
import platform

# Charger charset_normalizer avant tout import de requests pour éviter l'avertissement
# "Unable to find acceptable character detection dependency" dans la CMD
try:
    import charset_normalizer  # noqa: F401
except ImportError:
    pass


def _early_single_instance_win():
    """
    Vérification instance unique sous Windows AVANT tout log.
    Si une instance tourne déjà, affiche la messagebox et quitte sans toucher au fichier de log.
    Retourne True si on peut continuer, False si on doit quitter (2e instance).
    """
    if sys.platform != "win32":
        return True
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        ERROR_ALREADY_EXISTS = 0x000000B7
        mutex = kernel32.CreateMutexW(None, True, "RenExtract_SingleInstance_Mutex")
        if mutex is None or mutex == 0:
            return True
        if kernel32.GetLastError() == ERROR_ALREADY_EXISTS:
            kernel32.CloseHandle(mutex)
            return False
        return True
    except Exception:
        return True


# Vérification instance unique dès le chargement (avant initialize_log) pour ne pas régénérer le log
if __name__ == "__main__":
    if not _early_single_instance_win():
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning(
            "Instance Multiple",
            "RenExtract est déjà en cours d'exécution.\n\nFermez l'autre instance avant de relancer l'application."
        )
        root.destroy()
        root.quit()
        os._exit(1)  # terminaison immédiate (sys.exit peut laisser le processus vivant avec Tk)


from infrastructure.config.constants import VERSION, FILE_NAMES

# ✅ CORRECTION CRITIQUE : Charger le mode debug AVANT d'initialiser le logger
import json
import os as os_temp
_DEBUG_MODE = False
_DEBUG_LEVEL = 3
try:
    _config_path = FILE_NAMES["config"]
    if os_temp.path.exists(_config_path):
        with open(_config_path, 'r', encoding='utf-8') as f:
            _config = json.load(f)
        _DEBUG_MODE = bool(_config.get("debug_mode", False))
        _DEBUG_LEVEL = int(_config.get("debug_level", 5))
except Exception:
    pass

from infrastructure.logging.logging import log_message, initialize_log, get_logger

initialize_log(app_version=VERSION)
log_message("INFO", "Processus démarré (avant chargement de l'interface)", category="main")

# Forcer le mode debug si activé dans la config
if _DEBUG_MODE:
    logger = get_logger()
    logger.debug_enabled = True
    logger.log_level = _DEBUG_LEVEL
    # ✅ CORRECTION : Logger immédiatement que le mode debug est activé
    log_message("INFO", f"🐛 Mode debug forcé au démarrage (niveau {_DEBUG_LEVEL})", category="main")

class _StdToUnified(logging.Handler):
    def emit(self, record):
        level_map = {
            logging.DEBUG: "DEBUG",
            logging.INFO: "INFO",
            logging.WARNING: "ATTENTION",
            logging.ERROR: "ERREUR",
            logging.CRITICAL: "ERREUR",
        }
        level = level_map.get(record.levelno, "INFO")
        category = record.name if record.name and record.name != "root" else "system"
        msg = record.getMessage()
        try:
            log_message(level, msg, category=category)
        except Exception:
            pass

_root_logger = logging.getLogger()
_root_logger.setLevel(logging.DEBUG)
if _root_logger.hasHandlers():
    _root_logger.handlers.clear()
_root_logger.addHandler(_StdToUnified())

def _trigger_health_imports() -> None:
    """
    Effectue des imports 'à blanc' pour déclencher les contrôles de santé
    définis dans les __init__.py de chaque package.
    L'ordre limite les imports circulaires.
    """
    # Désactivé temporairement pour éviter les problèmes en sandbox
    # Ces imports peuvent causer des boucles dans certains environnements
    pass

# _trigger_health_imports()  # Commenté pour éviter les problèmes en sandbox

# Résumé de santé des packages
def _log_health_summary():
    """Affiche un résumé de la santé de tous les packages"""
    try:
        import infrastructure
        import core
        import ui
        
        packages_status = []
        total_packages = 0
        healthy_packages = 0
        
        # Collecter les statuts
        if hasattr(infrastructure, 'INFRASTRUCTURE_HEALTH_STATUS'):
            status = infrastructure.INFRASTRUCTURE_HEALTH_STATUS
            total_packages += 1
            if status['health_percentage'] >= 100:
                healthy_packages += 1
            else:
                packages_status.append(('infrastructure', status))
        
        if hasattr(core, '_HEALTH_STATUS'):
            status = core._HEALTH_STATUS
            total_packages += 1
            if status['health_percentage'] >= 100:
                healthy_packages += 1
            else:
                packages_status.append(('core', status))
        
        if hasattr(ui, 'UI_HEALTH_STATUS'):
            status = ui.UI_HEALTH_STATUS
            total_packages += 1
            if status['health_percentage'] >= 100:
                healthy_packages += 1
            else:
                packages_status.append(('ui', status))
        
        # Afficher le résumé
        if healthy_packages == total_packages and total_packages > 0:
            # Tout est parfait : une seule ligne
            log_message("INFO", f"✅ Système opérationnel : {total_packages}/{total_packages} packages OK", category="main")
        elif total_packages > 0:
            # Il y a des problèmes : afficher les détails
            log_message("ATTENTION", f"⚠️  Système partiellement opérationnel : {healthy_packages}/{total_packages} packages OK", category="main")
            for pkg_name, status in packages_status:
                log_message("ERREUR", f"   └─ {pkg_name}: {status['health_percentage']:.0f}% ({status['loaded_modules']}/{status['total_modules']} modules)", category="main")
    except Exception as e:
        log_message("DEBUG", f"Impossible de générer le résumé de santé: {e}", category="main")

# _log_health_summary()  # Commenté pour éviter les problèmes en sandbox

log_message("INFO", "=== Démarrage de {version} ===", version=VERSION, category="main")

# --- Fenêtre console de chargement (Windows) : s'ouvre au démarrage, se ferme quand l'app est prête ---
_loading_console_active = False
_loading_console_stdout = None
_loading_console_stderr = None

def _show_loading_console():
    """Ouvre une fenêtre CMD affichant un message de chargement (Windows uniquement). N'affecte pas Tk."""
    global _loading_console_active, _loading_console_stdout, _loading_console_stderr
    if sys.platform != "win32":
        return
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        if not kernel32.AllocConsole():
            return
        _loading_console_active = True
        kernel32.SetConsoleTitleW("RenExtract - Chargement...")
        # Réattacher stdout/stderr pour que print() aille dans la console
        _loading_console_stdout = sys.stdout
        _loading_console_stderr = sys.stderr
        sys.stdout = open("CONOUT$", "w", encoding="utf-8")
        sys.stderr = sys.stdout
        print("RenExtract - Chargement en cours...")
        print("(Cette fenêtre se fermera lorsque l'application sera prête.)")
    except Exception:
        _loading_console_active = False

def _hide_loading_console():
    """Ferme la fenêtre console de chargement (Windows). À appeler juste avant d'afficher la fenêtre principale."""
    global _loading_console_active, _loading_console_stdout, _loading_console_stderr
    if not _loading_console_active or sys.platform != "win32":
        return
    try:
        import ctypes
        if sys.stdout and getattr(sys.stdout, "name", "") == "CONOUT$":
            try:
                sys.stdout.close()
            except Exception:
                pass
        sys.stdout = _loading_console_stdout if _loading_console_stdout is not None else sys.__stdout__
        sys.stderr = _loading_console_stderr if _loading_console_stderr is not None else sys.__stderr__
        ctypes.windll.kernel32.FreeConsole()
        _loading_console_active = False
    except Exception:
        _loading_console_active = False

# Imports légers uniquement ; core / ui chargés plus tard pour accélérer l'affichage
from infrastructure import get_config_manager
from infrastructure.config.constants import BASE_DIR, CONFIG_DIR_NAME, ensure_folders_exist
from infrastructure.helpers.unified_functions import show_translated_messagebox

try:
    import tkinterdnd2 as dnd2
    _DND = True
except Exception:
    _DND = False
    log_message("ATTENTION", "TkinterDnD2 non disponible - mode fallback", category="main")

class RenExtractApp:
    def __init__(self):
        # Dernier état connu des outils (réappliqué quand l'UI devient disponible)
        self._tools_status_message = "en cours d'initialisation..."
        self._tools_status_ready = False
        self._init_base()
        self._create_root()
        self._create_ui()
        self._finalize()

    def _init_base(self):
        try:
            ensure_folders_exist()
            self._cleanup_legacy_app_tools_dirs()
            
            # Lancer le pré-chargement des images du tutoriel en arrière-plan
            self._preload_tutorial_images()
            # Préparer Python embedded au démarrage pour éviter le délai au clic d'extraction
            self._preload_python_embedded()
            
        except Exception as e:
            log_message("ATTENTION", f"Impossible de vérifier/Créer les dossiers: {e}", category="main")

    def _cleanup_legacy_app_tools_dirs(self):
        """Supprime les anciens dossiers locaux inutilisés (05_ConfigRenExtract/tools,temp)."""
        try:
            import shutil
            config_root = os.path.join(BASE_DIR, CONFIG_DIR_NAME)
            legacy_dirs = [
                os.path.join(config_root, "tools"),
                os.path.join(config_root, "temp"),
            ]
            for d in legacy_dirs:
                if os.path.isdir(d):
                    try:
                        shutil.rmtree(d)
                        log_message("INFO", f"Ancien dossier supprimé: {d}", category="main")
                    except Exception as e:
                        log_message("ATTENTION", f"Impossible de supprimer le dossier {d}: {e}", category="main")
        except Exception as e:
            log_message("DEBUG", f"Nettoyage legacy tools/temp ignoré: {e}", category="main")
    
    def _preload_tutorial_images(self):
        """Lance le téléchargement des images du tutoriel en arrière-plan au démarrage"""
        try:
            from ui.tutorial import TutorialGenerator
            
            # Créer une instance du générateur en arrière-plan
            # Le téléchargement se lance automatiquement dans __init__
            def preload_task():
                try:
                    log_message("DEBUG", "🖼️  Pré-chargement des images tutoriel en arrière-plan...", category="main")
                    generator = TutorialGenerator()
                    # Pas besoin de générer le HTML maintenant, juste lancer le téléchargement
                    # Le générateur lance automatiquement _start_background_download() dans __init__
                except Exception as e:
                    log_message("DEBUG", f"Erreur pré-chargement images tutoriel: {e}", category="main")
            
            # Lancer dans un thread séparé pour ne pas bloquer le démarrage
            preload_thread = threading.Thread(target=preload_task, daemon=True, name="TutorialImagePreload")
            preload_thread.start()
            
        except Exception as e:
            log_message("DEBUG", f"Impossible de pré-charger les images du tutoriel: {e}", category="main")

    def _preload_python_embedded(self):
        """Précharge Python embedded (3.11 + 2.7) au démarrage (thread non bloquant)."""
        try:
            def preload_task():
                try:
                    log_message("INFO", "🐍 Préchargement Python embedded (3.11/2.7) démarré en arrière-plan...", category="main")
                    self._post_startup_status("en cours...", ready=False)

                    from core.tools.python_manager import get_python_manager
                    manager = get_python_manager()

                    py3 = manager.setup_python_embedded()
                    py2 = manager.setup_python27_embedded()

                    py3_ok = bool(py3)
                    py2_ok = bool(py2)

                    if py3_ok:
                        log_message("INFO", f"🐍 Python 3.11 embedded prêt : {py3}", category="main")
                    else:
                        log_message("ATTENTION", "Python 3.11 embedded non prêt au démarrage (retry au besoin).", category="main")

                    if py2_ok:
                        log_message("INFO", f"🐍 Python 2.7 embedded prêt : {py2}", category="main")
                    else:
                        log_message("ATTENTION", "Python 2.7 embedded non prêt au démarrage (retry au besoin).", category="main")

                    if py3_ok and py2_ok:
                        self._post_startup_status("prêts (3.11 + 2.7)", ready=True)
                    elif py3_ok:
                        self._post_startup_status("partiels (3.11 prêt, 2.7 à la demande)", ready=False)
                    else:
                        self._post_startup_status("non prêts (téléchargement à la demande)", ready=False)
                except Exception as e:
                    log_message("DEBUG", f"Erreur préchargement Python embedded: {e}", category="main")
                    self._post_startup_status("échec du préchargement (fallback à la demande)", ready=False)

            preload_thread = threading.Thread(target=preload_task, daemon=True, name="PythonEmbeddedPreload")
            preload_thread.start()
        except Exception as e:
            log_message("DEBUG", f"Impossible de lancer le préchargement Python embedded: {e}", category="main")

    def _post_startup_status(self, message: str, ready: bool = False):
        """Affiche un statut de démarrage dans l'UI si elle est disponible."""
        try:
            # Toujours mémoriser le dernier état, même si l'UI n'est pas encore prête.
            self._tools_status_message = message
            self._tools_status_ready = ready

            if not hasattr(self, "root"):
                return

            def _apply():
                try:
                    if not hasattr(self, "window"):
                        return
                    info_frame = self.window.get_component('info') if hasattr(self.window, 'get_component') else None
                    if info_frame and hasattr(info_frame, 'update_tools_status'):
                        info_frame.update_tools_status(message, ready=ready)
                except Exception:
                    pass

            self.root.after(0, _apply)
        except Exception:
            pass

    def _apply_pending_tools_status(self):
        """Réapplique le dernier statut outils quand l'interface est disponible."""
        try:
            if not hasattr(self, "window"):
                return
            info_frame = self.window.get_component('info') if hasattr(self.window, 'get_component') else None
            if info_frame and hasattr(info_frame, 'update_tools_status'):
                info_frame.update_tools_status(
                    getattr(self, "_tools_status_message", "en cours d'initialisation..."),
                    ready=getattr(self, "_tools_status_ready", False)
                )
        except Exception:
            pass

    def _create_root(self):
        try:
            self.root = dnd2.Tk() if _DND else tk.Tk()
            self.root.withdraw()
        except Exception as e:
            log_message("ERREUR", f"Erreur création fenêtre: {e}", category="main")
            self.root = tk.Tk()
            self.root.withdraw()

    def _create_ui(self):
        try:
            log_message("DEBUG", "Chargement de l'interface (core + ui)...", category="main")
            from core.app_controller import AppController
            from ui.main_window import MainWindow
            self.controller = AppController(None)
            self.window = MainWindow(self.root, self.controller)
            self.controller.main_window = self.window
        except Exception as e:
            log_message("ERREUR", f"Erreur création UI: {e}", category="main")
            raise

    def _check_server_running(self, port: int = 8765) -> bool:
        """Vérifie si le serveur tourne déjà sur le port donné"""
        import socket
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex(('127.0.0.1', port))
                return result == 0  # 0 = connexion réussie = serveur actif
        except Exception:
            return False
    
    def _start_editor_server_if_enabled(self) -> bool:
        """
        Démarre le serveur d'édition intégré dans un thread.
        Le serveur s'arrêtera automatiquement quand l'application se ferme.
        """
        try:
            config_manager = get_config_manager()
            if not config_manager:
                log_message("ATTENTION", "Config manager non disponible pour le serveur d'édition", category="main")
                return False
                
            enabled = config_manager.get('editor_server_enabled', True)  # Activé par défaut maintenant qu'il est intégré
            if not enabled:
                log_message("INFO", "Serveur d'édition désactivé par la configuration", category="main")
                return False

            # Détection automatique de l'environnement pour le développement WSL
            system = platform.system()
            release = platform.release().lower()
            log_message("DEBUG", f"🔍 Détection OS: system={system}, release={release}", category="main")
            
            default_host = '127.0.0.1'
            if system == 'Linux' and 'microsoft' in release:
                # WSL détecté : utiliser 0.0.0.0 pour permettre l'accès depuis Windows
                default_host = '0.0.0.0'
                log_message("INFO", "🐧 WSL détecté : serveur accessible depuis Windows", category="main")
            else:
                log_message("DEBUG", f"❌ WSL non détecté (Linux={system == 'Linux'}, microsoft in release={'microsoft' in release})", category="main")
            
            host = config_manager.get('editor_server_host', default_host)
            try:
                port = int(config_manager.get('editor_server_port', 8765))
            except Exception:
                port = 8765
            
            log_message("DEBUG", f"Configuration serveur: host={host} (défaut: {default_host}), port={port}", category="main")

            # Vérifier si le serveur tourne déjà
            if self._check_server_running(port):
                log_message("INFO", f"Serveur d'édition déjà actif sur http://{host}:{port}", category="main")
                return True

            # Démarrer le serveur dans un thread daemon
            from ui.shared.editor_manager_server import run_server
            
            def server_thread_func():
                try:
                    log_message("INFO", f"🚀 Démarrage serveur d'édition sur http://{host}:{port}", category="main")
                    run_server(host=host, port=port)
                except Exception as e:
                    log_message("ATTENTION", f"Erreur serveur d'édition: {e}", category="main")
            
            server_thread = threading.Thread(target=server_thread_func, daemon=True, name="EditorServer")
            server_thread.start()
            
            # Attendre un peu que le serveur démarre
            import time
            time.sleep(0.5)
            
            # Vérifier que le serveur est bien démarré
            if self._check_server_running(port):
                log_message("INFO", f"✅ Serveur d'édition intégré démarré sur http://{host}:{port}", category="main")
                self.editor_server_thread = server_thread
                return True
            else:
                log_message("ATTENTION", f"Serveur d'édition non joignable sur le port {port}", category="main")
                return False

        except Exception as e:
            log_message("ATTENTION", f"Impossible de démarrer le serveur d'édition: {e}", category="main")
            import traceback
            log_message("DEBUG", f"Traceback: {traceback.format_exc()}", category="main")
            return False

    def _setup_realtime_editor_callbacks(self):
        """Configure les callbacks pour l'éditeur temps réel si disponible"""
        try:
            from ui.shared import editor_manager_server as ems
            
            # Fonction callback pour recevoir les dialogues depuis Ren'Py
            def dialogue_http_callback(dialogue_data):
                """Callback appelé quand un dialogue arrive via HTTP"""
                try:
                    # Vérifier qu'on a une interface principale
                    if hasattr(self, 'window') and hasattr(self.window, 'realtime_dialogue_callback'):
                        # Utiliser le thread principal de Tkinter
                        self.root.after(0, self.window.realtime_dialogue_callback, dialogue_data)
                    elif hasattr(self, 'controller') and hasattr(self.controller, 'handle_realtime_dialogue'):
                        self.root.after(0, self.controller.handle_realtime_dialogue, dialogue_data)
                    else:
                        log_message("DEBUG", f"Dialogue reçu mais pas d'handler: {dialogue_data.get('displayed_text', '')[:50]}...", category="main")
                except Exception as e:
                    log_message("ERREUR", f"Erreur callback dialogue HTTP: {e}", category="main")
            
            # Configurer le callback dans le serveur
            ems.set_focus_callback(dialogue_http_callback)
            log_message("INFO", "Callbacks éditeur temps réel configurés", category="main")
            return True
            
        except Exception as e:
            log_message("ATTENTION", f"Impossible de configurer les callbacks temps réel: {e}", category="main")
            return False

    def _finalize(self):
        """
        Ordre avant affichage fenêtre (tout se fait avant deiconify) :
        - _init_base : ensure_folders_exist() (dossiers), _preload_tutorial_images() (thread, non bloquant)
        - _create_root : Tk() puis withdraw()
        - _create_ui : AppController + MainWindow (construction UI = partie la plus longue)
        - _finalize : fermeture console de chargement (Windows), apply_theme, center_window, puis deiconify().
        """
        try:
            _hide_loading_console()
            from ui.themes import theme_manager
            from ui.tutorial import show_first_launch_popup, check_first_launch
            # Thème et centrage avant affichage pour éviter que la fenêtre "saute" après apparition
            if hasattr(self.window, "apply_theme") and theme_manager is not None:
                self.window.apply_theme()
            if hasattr(self.window, "center_window"):
                self.window.center_window()
            if hasattr(self.window, "deiconify"):
                self.window.deiconify()
            else:
                self.root.deiconify()
            # Réappliquer l'état des outils (utile si le thread a fini avant la création de l'UI)
            self._apply_pending_tools_status()
            try:
                if check_first_launch():
                    self.root.after(500, lambda: show_first_launch_popup(self.root, self.controller))
            except Exception as e:
                log_message("ATTENTION", f"Tutoriel premier lancement indisponible: {e}", category="main")
            
            # Démarrer le serveur HTTP étendu
            server_started = self._start_editor_server_if_enabled()
            
            # Configurer les callbacks temps réel si le serveur est démarré
            if server_started:
                self._setup_realtime_editor_callbacks()
            
        except Exception as e:
            log_message("ERREUR", f"Erreur finalisation UI: {e}", category="main")

    def run(self):
        try:
            if hasattr(self.window, "mainloop"):
                self.window.mainloop()
            else:
                self.root.mainloop()
        except KeyboardInterrupt:
            self.quit()
        except Exception as e:
            log_message("ERREUR", f"Erreur dans la boucle principale: {e}", category="main")
            self.quit()

    def quit(self):
        try:
            log_message("INFO", "Fermeture de l'application", category="main")
            
            # Le serveur d'édition est dans un thread daemon, il s'arrêtera automatiquement
            
            # Nettoyer l'éditeur temps réel si actif
            try:
                if hasattr(self, 'controller') and hasattr(self.controller, 'cleanup_realtime_editor'):
                    self.controller.cleanup_realtime_editor()
            except Exception as e:
                log_message("ATTENTION", f"Erreur nettoyage éditeur temps réel: {e}", category="main")
            
            # Nettoyage normal
            if hasattr(self, "controller") and hasattr(self.controller, "quit_application"):
                self.controller.quit_application()
            elif hasattr(self, "root"):
                self.root.quit()
                self.root.destroy()
        finally:
            sys.exit(0)

def _is_renextract_process(proc_name: str, cmdline: str) -> bool:
    """Détermine si un processus identifié par son nom et sa ligne de commande semble appartenir à RenExtract.

    Cette détection est volontairement stricte : on vérifie la présence de 'renextract' dans le nom
    du processus ou la ligne de commande, ou on compare le nom de l'exécutable courant
    (ex: python.exe / renextract.exe) et le nom du script (`main.py`).
    """
    try:
        lower_proc = (proc_name or '').lower()
        lower_cmd = (cmdline or '').lower()
        exe_basename = os.path.basename(sys.executable).lower()
        script_basename = os.path.basename(__file__).lower()

        if 'renextract' in lower_proc or 'renextract' in lower_cmd:
            return True
        if exe_basename and exe_basename in lower_proc:
            return True
        if script_basename and script_basename in lower_cmd:
            return True
        return False
    except Exception:
        return False


def cleanup_orphaned_ports():
    """Nettoie les ports orphelins avant le démarrage de l'application"""
    import socket
    
    # Lire la configuration des ports si disponible
    cleaned_ports = []
    try:
        from infrastructure.config.config import config_manager
        cfg_ports = config_manager.get('orphaned_ports', [8765, 45000, 8767]) or [8765, 45000, 8767]
        # Normaliser en int et garder l'ordre sans doublons
        normalized = []
        for p in cfg_ports:
            try:
                ip = int(p)
                if ip not in normalized:
                    normalized.append(ip)
            except Exception:
                pass
        # S'assurer que editor & hotkey sont présents
        try:
            editor_p = int(config_manager.get('editor_server_port', 8765))
        except Exception:
            editor_p = 8765
        try:
            hotkey_p = int(config_manager.get('hotkey_server_port', 45000))
        except Exception:
            hotkey_p = 45000
        if editor_p not in normalized:
            normalized.insert(0, editor_p)
        if hotkey_p not in normalized:
            # insérer après l'éditeur si possible
            if editor_p in normalized:
                idx = normalized.index(editor_p) + 1
                normalized.insert(idx, hotkey_p)
            else:
                normalized.insert(0, hotkey_p)
        ports_to_check = normalized
    except Exception:
        ports_to_check = [8765, 45000, 8767]

    # Timeout court : sur localhost un port libre = refus immédiat ; 0.15s évite ~1.5s cumulés (3 ports × 0.5s)
    socket_timeout = 0.15
    for port in ports_to_check:
        try:
            # Vérifier si le port est utilisé
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(socket_timeout)
            result = test_socket.connect_ex(('127.0.0.1', port))
            test_socket.close()
            
            if result == 0:
                # Port utilisé, tenter de trouver et tuer le processus
                try:
                    if sys.platform.startswith('win'):
                        # Windows: utiliser netstat et taskkill, mais vérifier le processus avant de le tuer
                        import subprocess
                        # ✅ CORRECTION : Masquer la fenêtre console sur Windows
                        creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

                        netstat_output = subprocess.check_output(
                            f'netstat -ano | findstr :{port}',
                            shell=True,
                            text=True,
                            creationflags=creationflags
                        )
                        lines = netstat_output.strip().split('\n')
                        for line in lines:
                            if f':{port}' in line and 'LISTENING' in line:
                                parts = line.split()
                                pid = parts[-1]

                                # Récupérer la ligne de commande associée au PID (wmic peut renvoyer vide)
                                try:
                                    cmd_output = subprocess.check_output(
                                        f'wmic process where ProcessId={pid} get CommandLine',
                                        shell=True,
                                        text=True,
                                        creationflags=creationflags,
                                        stderr=subprocess.DEVNULL
                                    ).strip().replace('\r', '')
                                    cmdlines = [l.strip() for l in cmd_output.splitlines() if l.strip()]
                                    cmdline_text = " ".join(cmdlines) if cmdlines else ""
                                except Exception:
                                    cmdline_text = ""

                                # Récupérer le nom du processus (tasklist)
                                try:
                                    tasklist_out = subprocess.check_output(
                                        f'tasklist /FI "PID eq {pid}" /FO CSV /NH',
                                        shell=True,
                                        text=True,
                                        creationflags=creationflags,
                                        stderr=subprocess.DEVNULL
                                    ).strip()
                                    # Format attendu: "process.exe","<pid>",...
                                    proc_name = tasklist_out.split('\",\"')[0].strip('"') if tasklist_out else ''
                                except Exception:
                                    proc_name = ''

                                lower_cmd = cmdline_text.lower()
                                lower_proc = proc_name.lower()

                                # N'éliminer que si on reconnaît un processus RenExtract (par nom ou par cmdline)
                                if _is_renextract_process(proc_name, cmdline_text):
                                    subprocess.run(f'taskkill /F /PID {pid}', shell=True, capture_output=True, creationflags=creationflags)
                                    cleaned_ports.append(port)
                                    log_message("DEBUG", f"Port {port} nettoye9 (PID: {pid}, proc: {proc_name}, cmd: {cmdline_text})", category="main")
                                else:
                                    log_message("DEBUG", f"Saut nettoyage port {port} (PID {pid}, proc: {proc_name}, cmd: {cmdline_text})", category="main")
                                break
                    else:
                        # Linux/Mac: utiliser ss ou netstat
                        import subprocess
                        try:
                            # Essayer avec ss (plus moderne)
                            ss_output = subprocess.check_output(
                                f'ss -tulpn | grep :{port}',
                                shell=True,
                                text=True,
                                stderr=subprocess.DEVNULL
                            )
                            # Format: tcp LISTEN 0 5 127.0.0.1:8765 0.0.0.0:* users:(("python",pid=12345,fd=5))
                            import re
                            pid_match = re.search(r'pid=(\d+)', ss_output)
                            if pid_match:
                                pid = pid_match.group(1)
                                # Vérifier la commande associée au PID avant de tuer
                                try:
                                    proc_cmd = subprocess.check_output(
                                        ['ps', '-p', pid, '-o', 'args='],
                                        text=True,
                                        stderr=subprocess.DEVNULL
                                    ).strip()
                                except Exception:
                                    proc_cmd = ''

                                if _is_renextract_process('', proc_cmd):
                                    subprocess.run(['kill', '-9', pid], capture_output=True)
                                    cleaned_ports.append(port)
                                    log_message("DEBUG", f"Port {port} nettoye9 (PID: {pid}, cmd: {proc_cmd})", category="main")
                                else:
                                    log_message("DEBUG", f"Saut nettoyage port {port} (PID {pid}, cmd: {proc_cmd})", category="main")
                        except subprocess.CalledProcessError:
                            # Fallback: essayer avec lsof si disponible
                            try:
                                lsof_output = subprocess.check_output(
                                    f'lsof -ti:{port}',
                                    shell=True,
                                    text=True,
                                    stderr=subprocess.DEVNULL
                                )
                                pids = lsof_output.strip().split('\n')
                                for pid in pids:
                                    if pid:
                                        try:
                                            proc_cmd = subprocess.check_output(
                                                ['ps', '-p', pid, '-o', 'args='],
                                                text=True,
                                                stderr=subprocess.DEVNULL
                                            ).strip()
                                        except Exception:
                                            proc_cmd = ''

                                        if _is_renextract_process('', proc_cmd):
                                            subprocess.run(['kill', '-9', pid], capture_output=True)
                                            cleaned_ports.append(port)
                                            log_message("DEBUG", f"Port {port} nettoye9 (PID: {pid}, cmd: {proc_cmd})", category="main")
                                        else:
                                            log_message("DEBUG", f"Saut nettoyage port {port} (PID {pid}, cmd: {proc_cmd})", category="main")
                            except subprocess.CalledProcessError:
                                pass
                except Exception as e:
                    log_message("DEBUG", f"Impossible de nettoyer le port {port}: {e}", category="main")
        except Exception:
            pass
    
    if cleaned_ports:
        log_message("DEBUG", f"{len(cleaned_ports)} port(s) orphelin(s) nettoyé(s)", category="main")
    
    return len(cleaned_ports)


def main():
    # Détection du mode sandbox
    is_sandbox = (
        os.environ.get('SANDBOX', '').lower() == 'true' or
        'sandbox' in os.path.basename(sys.executable).lower() or
        os.environ.get('USERNAME', '').lower() in ['sandbox', 'user'] or
        os.path.exists('C:\\Windows\\Sandbox') or
        'sandbox' in os.getcwd().lower()
    )
    
    if is_sandbox:
        log_message("DEBUG", "Mode sandbox détecté - fonctionnalités limitées", category="main")
    
    lock_file_path = None  # utilisé par le finally si verrou fichier (non-Windows)
    # Instance unique : sous Windows déjà vérifiée au chargement du module (_early_single_instance_win)
    if sys.platform != "win32" or is_sandbox:
        # Fallback : verrou fichier (Linux, sandbox)
        import tempfile
        if is_sandbox:
            lock_file_path = "renextract_app.lock"
        else:
            appdata = os.environ.get("APPDATA") or tempfile.gettempdir()
            lock_dir = os.path.join(appdata, "RenExtract")
            try:
                os.makedirs(lock_dir, exist_ok=True)
            except Exception:
                lock_dir = tempfile.gettempdir()
            lock_file_path = os.path.join(lock_dir, "renextract_app.lock")
        
        if os.path.exists(lock_file_path):
            try:
                with open(lock_file_path, 'r') as f:
                    old_pid = int(f.read().strip())
                try:
                    os.kill(old_pid, 0)
                    try:
                        root = tk.Tk()
                        root.withdraw()
                        tk.messagebox.showwarning(
                            "Instance Multiple",
                            "RenExtract est déjà en cours d'exécution.\n\nFermez l'autre instance avant de relancer l'application."
                        )
                        root.destroy()
                    except Exception:
                        pass
                    sys.exit(1)
                except (OSError, ProcessLookupError, SystemError):
                    try:
                        os.remove(lock_file_path)
                    except Exception:
                        pass
            except (ValueError, FileNotFoundError):
                try:
                    if os.path.exists(lock_file_path):
                        os.remove(lock_file_path)
                except Exception:
                    pass
        
        try:
            with open(lock_file_path, 'w') as f:
                f.write(str(os.getpid()))
        except Exception as e:
            log_message("ERREUR", f"Erreur création verrou: {e}", category="main")
            sys.exit(1)
    
    # Fenêtre console de chargement (Windows) : affichage immédiat avant tout chargement lourd
    _show_loading_console()
    
    # Nettoyer d'éventuels ports orphelins (crash précédent)
    log_message("DEBUG", "Vérification des ports orphelins...", category="main")
    cleanup_orphaned_ports()
    
    try:
        log_message("DEBUG", "Instance unique vérifiée - démarrage autorisé", category="main")
        
        app = RenExtractApp()
        app.run()
        
    except Exception as e:
        _hide_loading_console()
        try:
            root = tk.Tk(); root.withdraw()
            tk.messagebox.showerror(
                "Erreur Critique",
                f"Une erreur critique a empêché le démarrage de l'application.\n\n{e}\n\nConsulte le log pour plus de détails."
            )
            root.destroy()
        except Exception:
            pass
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Nettoyer le verrou fichier (uniquement si on l'a utilisé, pas sous Windows mutex)
        try:
            if lock_file_path and os.path.exists(lock_file_path):
                os.remove(lock_file_path)
        except Exception:
            pass
        
        # 🆕 NETTOYAGE INTELLIGENT : Garder les polices utilisées, supprimer les autres
        try:
            from core.services.translation.font_manager import FontManager
            from infrastructure.config.config import config_manager
            
            tools_dir = config_manager.get_tools_directory()
            font_manager = FontManager(tools_dir)
            
            # Récupérer les polices utilisées
            prefs = config_manager.get_font_preferences()
            individual_fonts = prefs.get('individual_fonts', {})
            used_font_names = set()
            for font_type, font_config in individual_fonts.items():
                if font_config.get('enabled', False):
                    used_font_names.add(font_config.get('font_name', ''))
            
            # Nettoyage intelligent
            font_manager.cleanup_unused_temporary_fonts(used_font_names)
        except Exception as e:
            log_message("DEBUG", f"Erreur nettoyage intelligent polices temporaires: {e}", category="main")

if __name__ == "__main__":
    main()