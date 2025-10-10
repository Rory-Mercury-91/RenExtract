# ui/shared/hotkey_manager.py
"""
Gestionnaire de hotkey globale pour communication Ren'Py ↔ RenExtract
Architecture: Socket local TCP + thread d'écoute
"""

import socket
import threading
import time
import json
from typing import Callable, Optional, Dict, Any
from infrastructure.logging.logging import log_message

class HotkeyManager:
    """Gestionnaire de hotkey globale pour focus/activation à distance"""
    
    def __init__(self, port: int = 8766):
        self.port = port
        self.server_socket: Optional[socket.socket] = None
        self.listen_thread: Optional[threading.Thread] = None
        self.running = False
        self.focus_callback: Optional[Callable] = None
        
    def start_server(self, focus_callback: Callable = None):
        """Démarre le serveur d'écoute pour les hotkeys"""
        try:
            if self.running:
                return True
                
            self.focus_callback = focus_callback
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('127.0.0.1', self.port))
            self.server_socket.listen(1)
            self.server_socket.settimeout(1.0)  # Timeout pour permettre l'arrêt
            
            self.running = True
            self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.listen_thread.start()
            
            log_message("INFO", f"Serveur hotkey démarré sur port {self.port}", category="hotkey")
            return True
            
        except Exception as e:
            log_message("ERREUR", f"Erreur démarrage serveur hotkey: {e}", category="hotkey")
            return False
    
    def stop_server(self):
        """Arrête le serveur d'écoute"""
        try:
            self.running = False
            
            if self.server_socket:
                self.server_socket.close()
                
            if self.listen_thread and self.listen_thread.is_alive():
                self.listen_thread.join(timeout=2.0)
                
            log_message("INFO", "Serveur hotkey arrêté", category="hotkey")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur arrêt serveur hotkey: {e}", category="hotkey")
    
    def _listen_loop(self):
        """Boucle d'écoute des connexions hotkey"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                
                # Traitement dans un thread séparé pour ne pas bloquer
                client_thread = threading.Thread(
                    target=self._handle_client, 
                    args=(client_socket,), 
                    daemon=True
                )
                client_thread.start()
                
            except socket.timeout:
                continue  # Normal - permet de vérifier self.running
            except Exception as e:
                if self.running:  # Éviter les logs d'erreur lors de l'arrêt normal
                    log_message("ATTENTION", f"Erreur écoute hotkey: {e}", category="hotkey")
    
    def _handle_client(self, client_socket: socket.socket):
        """Traite une connexion client hotkey"""
        try:
            # Lire la commande (format JSON)
            data = client_socket.recv(1024).decode('utf-8')
            
            if data:
                command = json.loads(data)
                self._process_hotkey_command(command)
                
                # Répondre que la commande a été reçue
                response = {"status": "success", "command": command.get("action", "unknown")}
                client_socket.send(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur traitement commande hotkey: {e}", category="hotkey")
            try:
                error_response = {"status": "error", "message": str(e)}
                client_socket.send(json.dumps(error_response).encode('utf-8'))
            except:
                pass
        finally:
            try:
                client_socket.close()
            except:
                pass
    
    def _process_hotkey_command(self, command: Dict[str, Any]):
        """Traite une commande hotkey reçue"""
        try:
            action = command.get("action", "")
            
            if action == "focus_renextract":
                if self.focus_callback:
                    # Exécuter dans le thread principal UI
                    import tkinter as tk
                    if hasattr(tk, '_default_root') and tk._default_root:
                        tk._default_root.after(0, self.focus_callback)
                        log_message("INFO", "Commande focus RenExtract exécutée", category="hotkey")
                    else:
                        log_message("ATTENTION", "Interface principale non trouvée", category="hotkey")
                else:
                    log_message("ATTENTION", "Aucun callback focus défini", category="hotkey")
                    
            elif action == "ping":
                log_message("DEBUG", "Ping hotkey reçu", category="hotkey")
                
            else:
                log_message("ATTENTION", f"Commande hotkey inconnue: {action}", category="hotkey")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur traitement commande hotkey: {e}", category="hotkey")


# Fonction utilitaire pour envoyer une commande hotkey (côté Ren'Py)
def send_hotkey_command(command: str, port: int = 8766, timeout: float = 1.0) -> bool:
    """
    Envoie une commande hotkey au serveur RenExtract
    
    Args:
        command: Commande à envoyer ("focus_renextract", "ping", etc.)
        port: Port du serveur hotkey
        timeout: Timeout de connexion
        
    Returns:
        bool: True si la commande a été envoyée avec succès
    """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(timeout)
        client_socket.connect(('127.0.0.1', port))
        
        # Envoyer la commande
        message = json.dumps({"action": command, "timestamp": time.time()})
        client_socket.send(message.encode('utf-8'))
        
        # Attendre la réponse
        response = client_socket.recv(1024).decode('utf-8')
        result = json.loads(response)
        
        client_socket.close()
        
        return result.get("status") == "success"
        
    except Exception as e:
        return False


# Instance globale
hotkey_manager = HotkeyManager()

# Fonctions de commodité pour l'intégration
def start_hotkey_system(focus_callback: Callable = None) -> bool:
    """Démarre le système de hotkey globale"""
    return hotkey_manager.start_server(focus_callback)

def stop_hotkey_system():
    """Arrête le système de hotkey globale"""
    hotkey_manager.stop_server()

def is_hotkey_system_running() -> bool:
    """Vérifie si le système de hotkey est actif"""
    return hotkey_manager.running