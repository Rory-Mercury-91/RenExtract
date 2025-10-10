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

from infrastructure.config.constants import VERSION

from infrastructure.logging.logging import log_message, initialize_log

initialize_log(app_version=VERSION)

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
    try:
        import utils
    except Exception:
        pass
    try:
        import core.tools
    except Exception:
        pass
    try:
        import core.business
    except Exception:
        pass
    try:
        import ui.shared
    except Exception:
        pass
    try:
        import ui.tab_generator
    except Exception:
        pass
    try:
        import ui
    except Exception:
        pass
    try:
        import core
    except Exception:
        pass

_trigger_health_imports()

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

_log_health_summary()

log_message("INFO", "=== Démarrage de {version} ===", version=VERSION, category="main")

# IMPORTS CORRIGÉS - utilisation des nouvelles fonctions d'accès
from infrastructure import get_config_manager
from infrastructure.config.constants import ensure_folders_exist
from infrastructure.helpers.unified_functions import show_translated_messagebox

from core.app_controller import AppController
from ui.tutorial import show_first_launch_popup, check_first_launch
from ui.themes import theme_manager
from ui.main_window import MainWindow

try:
    import tkinterdnd2 as dnd2
    _DND = True
except Exception:
    _DND = False
    log_message("ATTENTION", "TkinterDnD2 non disponible - mode fallback", category="main")

class RenExtractApp:
    def __init__(self):
        self._init_base()
        self._create_root()
        self._create_ui()
        self._finalize()

    def _init_base(self):
        try:
            ensure_folders_exist()
        except Exception as e:
            log_message("ATTENTION", f"Impossible de vérifier/Créer les dossiers: {e}", category="main")

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
            self.controller = AppController(None)
            self.window = MainWindow(self.root, self.controller)
            self.controller.main_window = self.window
        except Exception as e:
            log_message("ERREUR", f"Erreur création UI: {e}", category="main")
            raise

    def _start_editor_server_if_enabled(self) -> bool:
        """
        Démarre le serveur d'édition étendu (HTML → Éditeur + HTTP dialogue/choix)
        en arrière-plan si activé dans la configuration.
        """
        try:
            config_manager = get_config_manager()
            if not config_manager:
                log_message("ATTENTION", "Config manager non disponible pour le serveur d'édition", category="main")
                return False
                
            enabled = config_manager.get('editor_server_enabled', True)
            if not enabled:
                log_message("INFO", "Serveur d'édition désactivé par la configuration", category="main")
                return False

            # Déjà lancé ? on ne relance pas
            if getattr(self, "_editor_server_thread", None) and self._editor_server_thread.is_alive():
                return True

            # Import du serveur étendu
            from ui.shared import editor_manager_server as ems

            host = config_manager.get('editor_server_host', '127.0.0.1')
            try:
                port = int(config_manager.get('editor_server_port', 8765))
            except Exception:
                port = 8765

            # Thread daemon → se termine avec l'app
            self._editor_server_thread = threading.Thread(
                target=lambda: ems.run_server(host=host, port=port),
                name="EditorServerThread",
                daemon=True
            )
            self._editor_server_thread.start()

            # Attendre un peu que le serveur démarre
            import time
            time.sleep(0.5)
            
            # Vérifier que le serveur est bien démarré
            if hasattr(ems, 'is_server_running') and ems.is_server_running():
                log_message("INFO", f"Serveur d'édition HTTP démarré sur http://{host}:{port}", category="main")
                return True
            else:
                log_message("ATTENTION", f"Serveur d'édition démarré mais statut incertain sur http://{host}:{port}", category="main")
                return True  # On assume que ça marche

        except Exception as e:
            log_message("ATTENTION", f"Impossible de démarrer le serveur d'édition HTTP: {e}", category="main")
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
            ems.set_dialogue_callback(dialogue_http_callback)
            log_message("INFO", "Callbacks éditeur temps réel configurés", category="main")
            return True
            
        except Exception as e:
            log_message("ATTENTION", f"Impossible de configurer les callbacks temps réel: {e}", category="main")
            return False

    def _finalize(self):
        try:
            if hasattr(self.window, "apply_theme") and theme_manager is not None:
                self.window.apply_theme()
            if hasattr(self.window, "center_window"):
                self.window.center_window()
            if hasattr(self.window, "deiconify"):
                self.window.deiconify()
            else:
                self.root.deiconify()
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

def main():
    app = RenExtractApp()
    app.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        try:
            root = tk.Tk(); root.withdraw()
            show_translated_messagebox(
                "error",
                "Erreur Critique",
                f"Une erreur critique a empêché le démarrage de l'application.\n\n{e}\n\nConsulte le log pour plus de détails."
            )
            root.destroy()
        except Exception:
            pass
        import traceback
        traceback.print_exc()
        sys.exit(1)