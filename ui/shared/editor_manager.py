# ========================================
# UI/SHARED/EDITOR_MANAGER.PY - VERSION SIMPLIFIÉE
# ========================================

import os
import sys
import subprocess

# Import conditionnel pour Windows uniquement
if sys.platform == "win32":
    import winreg
else:
    winreg = None

from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message

def _get_default_editor_for_rpy():
    """Détecte l'éditeur par défaut pour les fichiers .rpy et retourne la commande appropriée"""
    if sys.platform != "win32" or winreg is None:
        log_message("ATTENTION", "Détection d'éditeur par défaut non supportée sur cette plateforme", category="editor_opener")
        return ("unknown", None)
        
    try:
        # Windows 10/11 : Essayer d'abord HKEY_CURRENT_USER (priorité utilisateur)
        file_type = None
        command = None
        
        try:
            # Essayer UserChoice (Windows 10+)
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.rpy\UserChoice") as key:
                prog_id = winreg.QueryValueEx(key, "ProgId")[0]
                
                # Récupérer la commande depuis le ProgId
                with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, f"{prog_id}\\shell\\open\\command") as cmd_key:
                    command = winreg.QueryValue(cmd_key, "")
                    file_type = prog_id
        except (FileNotFoundError, OSError):
            # Fallback sur l'ancien système (HKEY_CLASSES_ROOT)
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, ".rpy") as key:
                file_type = winreg.QueryValue(key, "")
            
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, f"{file_type}\\shell\\open\\command") as key:
                command = winreg.QueryValue(key, "")
        
        if not command:
            log_message("ATTENTION", "Aucune commande trouvée pour .rpy", category="editor_opener")
            return ("unknown", None)
        
        command_lower = command.lower()
        
        # Détecter les éditeurs supportés
        if "sublime_text.exe" in command_lower or "subl.exe" in command_lower:
            # Extraire le chemin de l'exécutable depuis la commande
            import re
            match = re.search(r'"([^"]+sublime[^"]*\.exe)"', command, re.IGNORECASE)
            if match:
                detected_path = match.group(1)
                # Si c'est sublime_text.exe, remplacer par subl.exe dans le même dossier
                if "sublime_text.exe" in detected_path.lower():
                    subl_path = detected_path.replace("sublime_text.exe", "subl.exe").replace("sublime_text.EXE", "subl.exe")
                    if os.path.exists(subl_path):
                        return ("sublime", subl_path)
                # Si c'est déjà subl.exe, l'utiliser directement
                elif "subl.exe" in detected_path.lower():
                    if os.path.exists(detected_path):
                        return ("sublime", detected_path)
            
            # Fallback : chercher dans les emplacements standards
            possible_paths = [
                r"C:\Program Files\Sublime Text\subl.exe",
                r"C:\Program Files\Sublime Text 4\subl.exe",
                r"C:\Program Files\Sublime Text 3\subl.exe",
                r"C:\Program Files (x86)\Sublime Text\subl.exe",
                r"C:\Program Files (x86)\Sublime Text 4\subl.exe",
                r"C:\Program Files (x86)\Sublime Text 3\subl.exe",
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    return ("sublime", path)
        
        if "code.exe" in command_lower:
            # Extraire le chemin de l'exécutable depuis la commande
            import re
            match = re.search(r'"([^"]+code[^"]*\.exe)"', command, re.IGNORECASE)
            if match:
                detected_path = match.group(1)
                if os.path.exists(detected_path):
                    return ("vscode", detected_path)
            
            # Fallback : chercher dans les emplacements standards
            possible_paths = [
                r"C:\Program Files\Microsoft VS Code\Code.exe",
                r"C:\Program Files (x86)\Microsoft VS Code\Code.exe",
                os.path.expanduser(r"~\AppData\Local\Programs\Microsoft VS Code\Code.exe"),
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    return ("vscode", path)
        
        if "notepad++.exe" in command_lower:
            # Extraire le chemin de l'exécutable depuis la commande
            import re
            match = re.search(r'"([^"]+notepad\+\+[^"]*\.exe)"', command, re.IGNORECASE)
            if match:
                detected_path = match.group(1)
                if os.path.exists(detected_path):
                    return ("notepadpp", detected_path)
            
            # Fallback : chercher dans les emplacements standards
            possible_paths = [
                r"C:\Program Files\Notepad++\notepad++.exe",
                r"C:\Program Files (x86)\Notepad++\notepad++.exe",
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    return ("notepadpp", path)
        
        if "atom.exe" in command_lower or "pulsar.exe" in command_lower:
            # Vérifier Pulsar en priorité (plus récent)
            pulsar_path = os.path.expanduser(r"~\AppData\Local\Programs\Pulsar\Pulsar.exe")
            if os.path.exists(pulsar_path):
                return ("atom_pulsar", pulsar_path)
            
            atom_path = os.path.expanduser(r"~\AppData\Local\atom\atom.exe")
            if os.path.exists(atom_path):
                return ("atom_pulsar", atom_path)
            
        return ("unknown", None)
        
    except Exception as e:
        log_message("ATTENTION", f"Impossible de détecter l'éditeur par défaut: {e}", category="editor_opener")
        return ("unknown", None)

def _try_open_with_default_smart(file_path, line_number):
    """Tente d'ouvrir avec l'éditeur par défaut en détectant le bon format de commande"""
    editor_type, editor_path = _get_default_editor_for_rpy()
    
    # Flags pour masquer la fenêtre console sur Windows + handles sécurisés
    from infrastructure.helpers.subprocess_helper import run_silent
    
    try:
        if editor_type == "sublime" and editor_path:
            cmd = [editor_path, f"{file_path}:{line_number}"]
            filename = os.path.basename(file_path)
            log_message("INFO", f"📝 Ouverture : {filename}:{line_number}", category="editor_opener")
            run_silent(cmd, check=False, timeout=10)
            return True
        
        elif editor_type == "vscode" and editor_path:
            cmd = [editor_path, "--goto", f"{file_path}:{line_number}"]
            filename = os.path.basename(file_path)
            log_message("INFO", f"📝 Ouverture : {filename}:{line_number}", category="editor_opener")
            run_silent(cmd, check=False, timeout=10)
            return True
        
        elif editor_type == "notepadpp" and editor_path:
            cmd = [editor_path, f"-n{line_number}", file_path]
            filename = os.path.basename(file_path)
            log_message("INFO", f"📝 Ouverture : {filename}:{line_number}", category="editor_opener")
            run_silent(cmd, check=False, timeout=10)
            return True
        
        elif editor_type == "atom_pulsar" and editor_path:
            cmd = [editor_path, f"{file_path}:{line_number}"]
            filename = os.path.basename(file_path)
            log_message("INFO", f"📝 Ouverture : {filename}:{line_number}", category="editor_opener")
            run_silent(cmd, check=False, timeout=10)
            return True
        
        else:
            log_message("INFO", f"Éditeur par défaut non reconnu: {editor_type}", category="editor_opener")
            return False
            
    except Exception as e:
        log_message("ATTENTION", f"Erreur avec éditeur détecté ({editor_type}): {e}", category="editor_opener")
        return False

def open_file_with_editor(file_path, line_number):
    """
    Ouvre un fichier en utilisant l'éditeur choisi par l'utilisateur 
    ou l'éditeur par défaut de Windows en cas d'échec.
    """
    if sys.platform != "win32":
        log_message("ATTENTION", "L'ouverture de l'éditeur est supportée uniquement sur Windows.", category="editor_opener")
        return False

    editor_choice = config_manager.get('editor_choice', 'Défaut Windows')
    # Log simplifié : suppression des logs intermédiaires redondants

    opened = False
    try:
        if editor_choice == 'Défaut Windows':
            # Utiliser la détection intelligente de l'éditeur par défaut
            opened = _try_open_with_default_smart(file_path, line_number)
        else:
            # Utiliser l'éditeur personnalisé sélectionné
            custom_editor_path = config_manager.get("custom_editor_path", "")
            if custom_editor_path and os.path.exists(custom_editor_path):
                opened = _try_open_with_custom_editor(custom_editor_path, file_path, line_number)
            else:
                log_message("ATTENTION", f"Chemin de l'éditeur personnalisé '{editor_choice}' introuvable: {custom_editor_path}", category="editor_opener")
        
        # Fallback si échec
        if not opened:
            filename = os.path.basename(file_path)
            log_message("ATTENTION", f"⚠️ Fallback Windows : {filename} (perte ligne {line_number})", category="editor_opener")
            os.startfile(file_path)
            opened = True

    except Exception as e:
        log_message("ERREUR", f"Erreur critique lors de l'ouverture de l'éditeur : {e}", category="editor_opener")
        return False
        
    return opened

def _try_open_with_custom_editor(editor_path, file_path, line_number):
    """Tente d'ouvrir avec un éditeur personnalisé en détectant automatiquement la syntaxe"""
    from infrastructure.helpers.subprocess_helper import run_silent
    
    try:
        editor_name = os.path.basename(editor_path).lower()
        
        # Détecter le type d'éditeur par le nom de l'exécutable
        filename = os.path.basename(file_path)
        
        if "code.exe" in editor_name or "code" in editor_name:
            # VSCode
            cmd = [editor_path, "--goto", f"{file_path}:{line_number}"]
            log_message("INFO", f"📝 Ouverture : {filename}:{line_number}", category="editor_opener")
            run_silent(cmd, check=False, timeout=10)
            return True
            
        elif "subl.exe" in editor_name or "sublime" in editor_name:
            # Sublime Text
            cmd = [editor_path, f"{file_path}:{line_number}"]
            log_message("INFO", f"📝 Ouverture : {filename}:{line_number}", category="editor_opener")
            run_silent(cmd, check=False, timeout=10)
            return True
            
        elif "notepad++.exe" in editor_name or "notepad" in editor_name:
            # Notepad++
            cmd = [editor_path, f"-n{line_number}", file_path]
            log_message("INFO", f"📝 Ouverture : {filename}:{line_number}", category="editor_opener")
            run_silent(cmd, check=False, timeout=10)
            return True
            
        elif "atom.exe" in editor_name or "pulsar.exe" in editor_name or "atom" in editor_name or "pulsar" in editor_name:
            # Atom/Pulsar
            cmd = [editor_path, f"{file_path}:{line_number}"]
            log_message("INFO", f"📝 Ouverture : {filename}:{line_number}", category="editor_opener")
            run_silent(cmd, check=False, timeout=10)
            return True
            
        else:
            # Éditeur inconnu - essayer la syntaxe générique
            log_message("INFO", f"📝 Ouverture : {filename}:{line_number} (éditeur inconnu)", category="editor_opener")
            cmd = [editor_path, f"{file_path}:{line_number}"]
            run_silent(cmd, check=False, timeout=10)
            return True
            
    except Exception as e:
        log_message("ATTENTION", f"Erreur avec éditeur personnalisé '{editor_path}': {e}", category="editor_opener")
        return False