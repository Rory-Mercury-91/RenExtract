# infrastructure/helpers/server_utils.py
"""
Utilitaires pour gérer le serveur HTTP persistant
"""

import socket
import subprocess
import sys
import os
from typing import Optional
from infrastructure.logging.logging import log_message


def is_server_running(port: int = 8765, host: str = '127.0.0.1') -> bool:
    """Vérifie si le serveur tourne sur le port donné"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((host, port))
            return result == 0
    except Exception:
        return False


def find_server_pid(port: int = 8765) -> Optional[int]:
    """Trouve le PID du processus qui écoute sur le port donné"""
    try:
        if sys.platform.startswith('win'):
            # Windows: utiliser netstat
            result = subprocess.run(
                ['netstat', '-ano'],
                capture_output=True,
                text=True,
                timeout=5
            )
            for line in result.stdout.splitlines():
                if f':{port}' in line and 'LISTENING' in line:
                    parts = line.split()
                    if parts:
                        try:
                            return int(parts[-1])
                        except (ValueError, IndexError):
                            continue
        else:
            # Linux/Mac: utiliser lsof
            result = subprocess.run(
                ['lsof', '-ti', f':{port}'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.stdout.strip():
                return int(result.stdout.strip().split()[0])
    except Exception as e:
        log_message("DEBUG", f"Erreur recherche PID serveur: {e}", category="server_utils")
    
    return None


def stop_server(port: int = 8765) -> bool:
    """Arrête le serveur qui écoute sur le port donné"""
    try:
        pid = find_server_pid(port)
        if not pid:
            log_message("INFO", f"Aucun serveur actif trouvé sur le port {port}", category="server_utils")
            return False
        
        if sys.platform.startswith('win'):
            # Windows: utiliser taskkill
            subprocess.run(
                ['taskkill', '/F', '/PID', str(pid)],
                capture_output=True,
                timeout=5
            )
        else:
            # Linux/Mac: utiliser kill
            subprocess.run(
                ['kill', str(pid)],
                capture_output=True,
                timeout=5
            )
        
        log_message("INFO", f"Serveur arrêté (PID: {pid})", category="server_utils")
        return True
        
    except Exception as e:
        log_message("ERREUR", f"Erreur arrêt serveur: {e}", category="server_utils")
        return False


def get_server_info(port: int = 8765) -> dict:
    """Retourne les informations sur le serveur"""
    running = is_server_running(port)
    pid = find_server_pid(port) if running else None
    
    return {
        'running': running,
        'port': port,
        'pid': pid,
        'url': f'http://127.0.0.1:{port}' if running else None
    }

