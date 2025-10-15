# ui/shared/editor_manager_server.py
"""
Petit serveur HTTP local pour recevoir les clics depuis le rapport HTML
et ouvrir un fichier à une ligne donnée dans l'éditeur choisi.
- Démarrage:  python -m ui.shared.editor_manager_server
- Endpoints:
    GET http://127.0.0.1:8765/open?file=ABSOLUTE_PATH&line=NUMBER
    GET http://127.0.0.1:8765/focus              (nouveau)
"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import sys
import os
import time  # <-- ajouté pour le debounce
from infrastructure.logging.logging import log_message

# Importe votre gestionnaire existant
try:
    # Adapter si votre arborescence diffère
    from ui.shared.editor_manager import open_file_with_editor
except Exception:
    # Fallback si lancé en standalone pour test dans le même dossier
    from editor_manager import open_file_with_editor  # type: ignore

# ====== NOUVEAU : gestion du focus via callback + debounce F8 ======
_focus_callback = None
_last_focus_ts = 0.0
_focus_min_interval = 0.35  # secondes (~350 ms)
_SERVER_RUNNING = False

def set_focus_callback(cb):
    """
    Enregistre la fonction appelée quand /focus est reçu.
    La callback ne prend pas d'arguments et fait le 'bring to front' côté UI.
    """
    global _focus_callback
    _focus_callback = cb
    

# Compat ancien nom si ton code l'utilisait :
def set_dialogue_callback(cb):
    return set_focus_callback(cb)

def _call_focus_with_debounce():
    """Appelle la callback focus si présente, avec anti-rebond."""
    global _last_focus_ts
    now = time.monotonic()
    if (now - _last_focus_ts) < _focus_min_interval:
        return {"ok": True, "debounced": True}
    _last_focus_ts = now

    if _focus_callback:
        try:
            _focus_callback()
            return {"ok": True}
        except Exception as e:
            log_message("ATTENTION", f"Erreur focus_callback: {e}", category="editor_opener")
            return {"ok": False, "error": "callback_error"}
    else:
        return {"ok": False, "error": "no_callback"}
# ================================================================

class _Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        # Log supprimé : redondant avec le log d'ouverture simplifié

        # ===== Nouvel endpoint: /focus (F8 depuis Ren'Py) =====
        if parsed.path == "/focus":
            # Log supprimé : action interne peu utile
            payload = json.dumps(_call_focus_with_debounce()).encode("utf-8")
            self.send_response(200)
            self._cors()
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        # ======================================================

        if parsed.path != "/open":
            self.send_response(404)
            self._cors()
            self.end_headers()
            return

        qs = parse_qs(parsed.query)
        file_path = (qs.get("file", [""])[0] or "").strip().strip('"')
        line_str = (qs.get("line", ["0"])[0] or "0").strip()

        # Log supprimé : redondant avec le log d'ouverture simplifié

        try:
            line = int(line_str)
            if line <= 0:
                line = 1
        except ValueError:
            line = 1

        ok = False
        message = ""
        if not file_path:
            message = "Paramètre 'file' manquant."
        elif not os.path.isfile(file_path):
            message = f"Fichier introuvable: {file_path}"
        else:
            # Log déplacé vers editor_manager.py pour éviter les doublons
            ok = bool(open_file_with_editor(file_path, line))
            message = "Ouvert dans l'éditeur." if ok else "Impossible d'ouvrir dans l'éditeur."

        payload = json.dumps({"ok": ok, "message": message}).encode("utf-8")
        self.send_response(200 if ok else 400)
        self._cors()
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    # Silence default logging
    def log_message(self, format, *args):
        pass

def is_server_running():
    return _SERVER_RUNNING

def run_server(host="127.0.0.1", port=8765):
    global _SERVER_RUNNING
    httpd = HTTPServer((host, port), _Handler)
    _SERVER_RUNNING = True
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        log_message("ATTENTION", "Serveur éditeur arrêté (Ctrl+C).", category="editor_opener")
    finally:
        _SERVER_RUNNING = False

if __name__ == "__main__":
    # Démarre en frontal si exécuté en script
    try:
        run_server()
    except KeyboardInterrupt:
        print("Serveur arrêté par l'utilisateur")
    except Exception as e:
        print(f"Erreur serveur: {e}")
    finally:
        print("Nettoyage du serveur terminé")
