# ui/shared/editor_manager_server.py
"""
Petit serveur HTTP local pour recevoir les clics depuis le rapport HTML
et ouvrir un fichier à une ligne donnée dans l'éditeur choisi.
- Démarrage:  python -m ui.shared.editor_manager_server
- Endpoints:
    GET http://127.0.0.1:8765/open?file=ABSOLUTE_PATH&line=NUMBER
    GET http://127.0.0.1:8765/focus              
    POST http://127.0.0.1:8765/api/coherence/exclude   (gestion exclusions)
    DELETE http://127.0.0.1:8765/api/coherence/exclude (gestion exclusions)
    GET http://127.0.0.1:8765/api/coherence/exclusions (liste exclusions)
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
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()
    
    def _read_request_body(self):
        """Lit le corps de la requête JSON"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.rfile.read(content_length)
                return json.loads(body.decode('utf-8'))
            return {}
        except Exception as e:
            log_message("ERREUR", f"Erreur lecture body requête: {e}", category="editor_opener")
            return {}
    
    def _send_json_response(self, data, status_code=200):
        """Envoie une réponse JSON"""
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self._cors()
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

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
        
        # ===== Endpoint: /api/coherence/exclusions (GET) =====
        if parsed.path == "/api/coherence/exclusions":
            try:
                from infrastructure.config.config import config_manager
                
                # 🆕 Récupérer le projet depuis les query params
                qs = parse_qs(parsed.query)
                project_path = (qs.get("project", [""])[0] or "").strip()
                
                if project_path:
                    # Récupérer les exclusions pour ce projet uniquement
                    exclusions = config_manager.get_coherence_exclusions(project_path)
                else:
                    # Récupérer toutes les exclusions (dict par projet)
                    exclusions = config_manager.get_coherence_exclusions()
                
                self._send_json_response({'ok': True, 'exclusions': exclusions})
            except Exception as e:
                log_message("ERREUR", f"Erreur récupération exclusions: {e}", category="coherence_api")
                self._send_json_response({'ok': False, 'error': str(e)}, 500)
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

    def do_POST(self):
        """Gère les requêtes POST (ajout d'exclusions, modifications, traductions)"""
        parsed = urlparse(self.path)
        
        # ===== Endpoint: /api/coherence/exclude (POST) =====
        if parsed.path == "/api/coherence/exclude":
            try:
                from core.services.tools.coherence_checker_business import add_custom_exclusion
                
                data = self._read_request_body()
                exclusion_text = data.get('text', '').strip()
                file_path = data.get('file', '').strip()  # 🆕
                line = data.get('line', 0)  # 🆕
                project_path = data.get('project', '').strip()  # 🆕
                
                # 🆕 LOG DE DÉBOGAGE
                log_message("DEBUG", f"POST /exclude - Données reçues: text={bool(exclusion_text)}, file={repr(file_path)}, line={line}, project={repr(project_path)}", category="coherence_api")
                
                if not exclusion_text or not file_path or not project_path or line == 0:
                    log_message("ERREUR", f"Données incomplètes: text={bool(exclusion_text)}, file={bool(file_path)}, project={bool(project_path)}, line={line}", category="coherence_api")
                    self._send_json_response({'ok': False, 'error': 'Données incomplètes'}, 400)
                    return
                
                # Ajouter l'exclusion
                success = add_custom_exclusion(project_path, file_path, line, exclusion_text)
                
                if success:
                    log_message("INFO", f"✅ Exclusion ajoutée: {file_path}:{line}", category="coherence_exclusion")
                    self._send_json_response({'ok': True, 'message': 'Exclusion ajoutée'})
                else:
                    # Déjà présente
                    self._send_json_response({'ok': True, 'message': 'Exclusion déjà présente'})
                
            except Exception as e:
                log_message("ERREUR", f"Erreur ajout exclusion: {e}", category="coherence_api")
                self._send_json_response({'ok': False, 'error': str(e)}, 500)
            return
        
        # ===== Endpoint: /api/coherence/edit (POST) =====
        if parsed.path == "/api/coherence/edit":
            try:
                from core.services.tools.coherence_line_editor import edit_coherence_line
                import traceback
                
                data = self._read_request_body()
                file_path = data.get('file', '').strip()
                line = data.get('line', 0)
                # Ne pas strip new_content pour conserver les espaces intentionnels
                new_content = data.get('new_content', '')
                project_path = data.get('project', '').strip()
                language = data.get('language', 'french').strip()
                
                log_message("DEBUG", f"POST /edit - file={file_path}, line={line}, project={project_path}, language={language}", category="coherence_api")
                log_message("DEBUG", f"POST /edit - new_content: {repr(new_content)[:200]}", category="coherence_api")
                
                # Vérifier uniquement file_path, project_path et line (new_content peut être vide)
                if not file_path or not project_path or line == 0:
                    self._send_json_response({'ok': False, 'error': 'Données incomplètes (fichier, projet ou ligne manquant)'}, 400)
                    return
                
                # Effectuer la modification
                success, message = edit_coherence_line(project_path, file_path, line, new_content, language)
                
                if success:
                    log_message("INFO", f"✅ Ligne modifiée: {file_path}:{line}", category="coherence_edit")
                    self._send_json_response({'ok': True, 'message': message})
                else:
                    log_message("ERREUR", f"❌ Échec modification: {message}", category="coherence_edit")
                    self._send_json_response({'ok': False, 'error': message}, 500)
                
            except Exception as e:
                error_trace = traceback.format_exc()
                log_message("ERREUR", f"Exception modification ligne: {e}", category="coherence_api")
                log_message("DEBUG", f"Traceback complet:\n{error_trace}", category="coherence_api")
                self._send_json_response({'ok': False, 'error': str(e)}, 500)
            return
        
        # ===== Endpoint: /api/coherence/translate (POST) =====
        if parsed.path == "/api/coherence/translate":
            try:
                from ui.shared.translator_utils import translate_with_groq_api, get_translator_url
                
                data = self._read_request_body()
                text = data.get('text', '').strip()
                translator = data.get('translator', 'Google').strip()
                target_lang = data.get('target_lang', 'fr').strip()
                
                log_message("DEBUG", f"POST /translate - translator={translator}, target_lang={target_lang}", category="coherence_api")
                
                if not text:
                    self._send_json_response({'ok': False, 'error': 'Texte manquant'}, 400)
                    return
                
                # Traduction selon le service
                translation = None
                if translator == "Groq AI":
                    # Utiliser l'API Groq si disponible
                    translation = translate_with_groq_api(text, target_lang=target_lang)
                
                if translation:
                    log_message("INFO", f"✅ Traduction réussie: {translator}", category="coherence_translate")
                    self._send_json_response({'ok': True, 'translation': translation, 'service': translator})
                else:
                    # Fallback: retourner l'URL du traducteur web
                    url = get_translator_url(translator, text, target_lang=target_lang)
                    if url:
                        log_message("INFO", f"ℹ️ URL traducteur générée: {translator}", category="coherence_translate")
                        self._send_json_response({'ok': True, 'url': url, 'service': translator})
                    else:
                        self._send_json_response({'ok': False, 'error': 'Traduction non disponible'}, 500)
                
            except Exception as e:
                log_message("ERREUR", f"Erreur traduction: {e}", category="coherence_api")
                self._send_json_response({'ok': False, 'error': str(e)}, 500)
            return
        
        # ===== Endpoint: /api/coherence/save_all (POST) =====
        if parsed.path == "/api/coherence/save_all":
            try:
                from core.services.tools.coherence_line_editor import save_all_modifications
                
                data = self._read_request_body()
                modifications = data.get('modifications', [])
                project_path = data.get('project', '').strip()
                
                log_message("DEBUG", f"POST /save_all - {len(modifications)} modifications", category="coherence_api")
                
                if not modifications or not project_path:
                    self._send_json_response({'ok': False, 'error': 'Données incomplètes'}, 400)
                    return
                
                # Sauvegarder toutes les modifications
                success_count, failed_count, messages = save_all_modifications(project_path, modifications)
                
                log_message("INFO", f"✅ Enregistrement global: {success_count} succès, {failed_count} échecs", category="coherence_edit")
                self._send_json_response({
                    'ok': True,
                    'success_count': success_count,
                    'failed_count': failed_count,
                    'messages': messages
                })
                
            except Exception as e:
                log_message("ERREUR", f"Erreur enregistrement global: {e}", category="coherence_api")
                self._send_json_response({'ok': False, 'error': str(e)}, 500)
            return
        
        # Endpoint non trouvé
        self.send_response(404)
        self._cors()
        self.end_headers()
    
    def do_DELETE(self):
        """Gère les requêtes DELETE (suppression d'exclusions)"""
        parsed = urlparse(self.path)
        
        # ===== Endpoint: /api/coherence/exclude (DELETE) =====
        if parsed.path == "/api/coherence/exclude":
            try:
                from core.services.tools.coherence_checker_business import remove_custom_exclusion
                
                data = self._read_request_body()
                exclusion_text = data.get('text', '').strip()
                file_path = data.get('file', '').strip()  # 🆕
                line = data.get('line', 0)  # 🆕
                project_path = data.get('project', '').strip()  # 🆕
                
                if not exclusion_text or not file_path or not project_path or line == 0:
                    self._send_json_response({'ok': False, 'error': 'Données incomplètes'}, 400)
                    return
                
                # Supprimer l'exclusion
                success = remove_custom_exclusion(project_path, file_path, line, exclusion_text)
                
                if success:
                    log_message("INFO", f"🗑️ Exclusion retirée: {file_path}:{line}", category="coherence_exclusion")
                    self._send_json_response({'ok': True, 'message': 'Exclusion retirée'})
                else:
                    self._send_json_response({'ok': False, 'error': 'Exclusion non trouvée'}, 404)
                
            except Exception as e:
                log_message("ERREUR", f"Erreur suppression exclusion: {e}", category="coherence_api")
                self._send_json_response({'ok': False, 'error': str(e)}, 500)
            return
        
        # Endpoint non trouvé
        self.send_response(404)
        self._cors()
        self.end_headers()

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
