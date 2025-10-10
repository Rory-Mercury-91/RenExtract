# utils/unified_functions.py - VERSION CORRIGÉE AVEC IMPORTS LOCAUX
# Unified Functions Module - With Selectable Text MessageBox
# Created for RenExtract 

import os
import re
import shutil
import time
import datetime
import getpass
import tkinter as tk
from tkinter import ttk, font
from pathlib import Path
from typing import Union, List, Tuple, Optional, Dict, Any


# =====================================================================
# MESSAGEBOX CUSTOM AVEC SÉLECTION DE TEXTE
# =====================================================================

def show_custom_messagebox(
    type_: str, 
    title: str, 
    message: Union[str, List[Tuple[str, str]]],
    theme: dict, 
    yes_text: str = None, 
    no_text: str = None, 
    cancel_text: str = None, 
    parent: tk.Widget = None, 
    adaptive_size: bool = True, 
    yes_width: int = 10, 
    no_width: int = 10, 
    cancel_width: int = 10
):
    """Popup custom stylée avec support du texte multi-styles (couleur, gras, etc.)."""
    from infrastructure.logging.logging import log_message
    import tkinter as tk
    from tkinter import font
   
    result = {'value': None}
    popup = tk.Toplevel(parent) if parent else tk.Toplevel()
    popup.title(title)
    popup.configure(bg=theme["bg"])
    popup.resizable(True, True)
    
    # --- Début de la logique de taille adaptative ---
    if adaptive_size:
        # On a besoin d'un texte brut pour le calcul, même si le message est stylé
        if isinstance(message, list):
            message_text_for_size_calc = "".join(chunk[0] for chunk in message)
        else:
            message_text_for_size_calc = str(message)
            
        total_chars = len(message_text_for_size_calc)
        line_count = len(message_text_for_size_calc.split('\n'))
        
        if total_chars < 100:
            adaptive_width = min(max(500, total_chars * 10), 700)
            adaptive_height = 350
        elif line_count > 6 and total_chars > 300:
            adaptive_width = 800
            adaptive_height = min(700, 300 + line_count * 25)
        else:
            target_chars_per_line = 80
            optimal_width = min(max(600, target_chars_per_line * 10), 900)
            estimated_lines = max(4, total_chars // target_chars_per_line)
            adaptive_height = min(max(400, 300 + estimated_lines * 25), 800)
            adaptive_width = optimal_width
        
        popup.geometry(f"{adaptive_width}x{adaptive_height}")
    else:
        popup.geometry("800x650")
    
    popup.grab_set()
    popup.update_idletasks()

    if parent:
        parent_x, parent_y = parent.winfo_rootx(), parent.winfo_rooty()
        parent_w, parent_h = parent.winfo_width(), parent.winfo_height()
        popup_w, popup_h = popup.winfo_width(), popup.winfo_height()
        x = parent_x + (parent_w // 2) - (popup_w // 2)
        y = parent_y + (parent_h // 2) - (popup_h // 2)
    else:
        x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
        y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
    popup.geometry(f"+{x}+{y}")
    
    main_frame = tk.Frame(popup, bg=theme["bg"])
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    message_frame = tk.Frame(main_frame, bg=theme["bg"])
    message_frame.pack(fill='both', expand=True, padx=10, pady=(10, 10))
    
    # Fonctions internes pour la sélection et copie (elles restent inchangées)
    def create_selectable_text_widget_fixed(parent_widget, text_content, font_tuple, bg_color, fg_color):
        text_container = tk.Frame(parent_widget, bg=bg_color)
        temp_font = font.Font(font=font_tuple)
        char_width = temp_font.measure('M')
        parent_widget.update_idletasks()
        available_width = parent_widget.winfo_width()
        if available_width <= 1: available_width = 600
        text_width = available_width - 60
        width_chars = max(40, text_width // char_width)
        
        text_widget = tk.Text(text_container, font=font_tuple, bg=bg_color, fg=fg_color, wrap='word', width=width_chars, state='normal', relief='flat', borderwidth=0, highlightthickness=0, cursor='arrow', selectbackground='#0078d4', selectforeground='white', padx=10, pady=10)
        text_widget.insert('1.0', text_content)
        lines = text_content.split('\n')
        actual_lines = 0
        for line in lines:
            if len(line) == 0: actual_lines += 1
            else: actual_lines += max(1, (temp_font.measure(line) // text_width) + 1)
        
        max_visible_lines = 20
        needs_scrollbar = actual_lines > max_visible_lines
        
        if needs_scrollbar:
            scrollbar = tk.Scrollbar(text_container, orient="vertical", command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            text_widget.config(height=max_visible_lines)
            text_widget.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        else:
            text_widget.config(height=max(3, min(actual_lines, max_visible_lines)))
            text_widget.pack(fill="both", expand=True)
        
        text_widget.config(state='disabled')
        
        def on_enter(event):
            if text_widget.cget('state') == 'disabled': text_widget.config(cursor='xterm')
        def on_leave(event):
            text_widget.config(cursor='arrow')
        
        text_widget.bind('<Enter>', on_enter)
        text_widget.bind('<Leave>', on_leave)
        
        def show_context_menu(event):
            context_menu = tk.Menu(popup, tearoff=0, bg=bg_color, fg=fg_color)
            try:
                if text_widget.get(tk.SEL_FIRST, tk.SEL_LAST): context_menu.add_command(label="Copier la sélection", command=lambda: copy_selected_text(text_widget))
                else: context_menu.add_command(label="Copier tout le texte", command=lambda: copy_all_text(text_widget))
            except tk.TclError:
                context_menu.add_command(label="Copier tout le texte", command=lambda: copy_all_text(text_widget))
            
            context_menu.add_separator()
            context_menu.add_command(label="Sélectionner tout", command=lambda: select_all_text(text_widget))
            
            try: context_menu.tk_popup(event.x_root, event.y_root)
            finally: context_menu.grab_release()
        
        text_widget.bind('<Button-3>', show_context_menu)
        
        def _on_mousewheel(event):
            if needs_scrollbar: text_widget.yview_scroll(int(-1*(event.delta/120)), "units")
        
        text_widget.bind("<MouseWheel>", _on_mousewheel)
        
        return text_container, text_widget
    
    def copy_selected_text(text_widget):
        try:
            popup.clipboard_clear()
            popup.clipboard_append(text_widget.get(tk.SEL_FIRST, tk.SEL_LAST))
            log_message("INFO", "Texte sélectionné copié", category="ui_messagebox")
        except tk.TclError:
            copy_all_text(text_widget)
    
    def copy_all_text(text_widget):
        try:
            popup.clipboard_clear()
            popup.clipboard_append(text_widget.get('1.0', 'end-1c'))
            log_message("INFO", "Tout le texte copié", category="ui_messagebox")
        except Exception as e:
            log_message("ERREUR", f"Erreur copie texte: {e}", category="ui_messagebox")
    
    def select_all_text(text_widget):
        try:
            text_widget.tag_add(tk.SEL, '1.0', 'end')
            text_widget.mark_set(tk.INSERT, '1.0')
            text_widget.see(tk.INSERT)
        except Exception as e:
            log_message("ERREUR", f"Erreur sélection texte: {e}", category="ui_messagebox")
    
    def on_ctrl_a(event):
        focused_widget = popup.focus_get()
        if isinstance(focused_widget, tk.Text):
            select_all_text(focused_widget)
            return 'break'
    
    def on_ctrl_c(event):
        focused_widget = popup.focus_get()
        if isinstance(focused_widget, tk.Text):
            copy_selected_text(focused_widget)
            return 'break'
    
    popup.bind_all('<Control-a>', on_ctrl_a)
    popup.bind_all('<Control-A>', on_ctrl_a)
    popup.bind_all('<Control-c>', on_ctrl_c)
    popup.bind_all('<Control-C>', on_ctrl_c)
    
    # --- DÉBUT DE LA NOUVELLE LOGIQUE POUR LE TEXTE STYLÉ ---

    # On prépare le texte brut pour la création initiale du widget (essentiel pour la scrollbar)
    message_text_plain = "".join(chunk[0] for chunk in message) if isinstance(message, list) else str(message)
    
    # On appelle votre fonction interne une seule fois avec ce texte brut
    text_container, text_widget = create_selectable_text_widget_fixed(message_frame, message_text_plain, ('Segoe UI Emoji', 11), theme["bg"], theme["fg"])
    text_container.pack(fill='both', expand=True, padx=10, pady=10)
    
    # On applique les styles seulement si le message est une liste structurée
    if isinstance(message, list):
        text_widget.config(state='normal')
        
        # Définition de tous les styles (tags)
        font_bold = ('Segoe UI Emoji', 11, 'bold')
        font_italic = ('Segoe UI Emoji', 11, 'italic')
        text_widget.tag_configure("bold", font=font_bold)
        text_widget.tag_configure("italic", font=font_italic)
        text_widget.tag_configure("underline", underline=True)
        text_widget.tag_configure("strikethrough", overstrike=True)
        text_widget.tag_configure("green", foreground="#38d66b")
        text_widget.tag_configure("red", foreground="#ff8379")
        text_widget.tag_configure("yellow", foreground="#ffc107")
        text_widget.tag_configure("blue", foreground="#5ab0ff")
        text_widget.tag_configure("bold_green", font=font_bold, foreground="#38d66b")
        text_widget.tag_configure("bold_red", font=font_bold, foreground="#ff8379")

        # On efface le texte brut et on le remplace par le texte stylé
        text_widget.delete('1.0', 'end')
        for text_chunk, tag_name in message:
            # On utilise le tag 'normal' comme fallback
            tag_to_apply = tag_name if tag_name != "normal" else ()
            text_widget.insert('end', text_chunk, tag_to_apply)
        
        text_widget.config(state='disabled')
    
    # --- FIN DE LA NOUVELLE LOGIQUE POUR LE TEXTE STYLÉ ---

    # Le bloc final pour les boutons et l'astuce, tel que nous l'avons finalisé
    bottom_frame = tk.Frame(main_frame, bg=theme["bg"])
    bottom_frame.pack(pady=(15, 0), fill='x', padx=10)
    
    btn_container = tk.Frame(bottom_frame, bg=theme["bg"])
    btn_container.pack() 
    
    def close(val=None):
        result['value'] = val
        popup.destroy()

    if type_ == 'askyesno':
        popup.protocol("WM_DELETE_WINDOW", lambda: None)
    elif type_ == 'askyesnocancel':
        popup.protocol("WM_DELETE_WINDOW", lambda: close(None))
    else:
        popup.protocol("WM_DELETE_WINDOW", lambda: close(True))

    if type_ in ('info', 'warning', 'error'):
        btn_ok = tk.Button(btn_container, text=yes_text or 'OK', font=('Segoe UI', 10, 'bold'), 
                           bg='#38d66b', fg='#000000',
                           width=yes_width, command=lambda: close(True))
        btn_ok.pack()
        btn_ok.focus_set()
        
    elif type_ == 'askyesno':
        btn_yes = tk.Button(btn_container, text=yes_text or 'Oui', font=('Segoe UI', 10, 'bold'),
                            bg='#38d66b', fg='#000000',
                            width=yes_width, command=lambda: close(True))
        btn_no = tk.Button(btn_container, text=no_text or 'Non', font=('Segoe UI', 10, 'bold'),
                           bg='#ff8379', fg='#000000',
                           width=no_width, command=lambda: close(False))
        btn_yes.pack(side='left', padx=8)
        btn_no.pack(side='left', padx=8)
        btn_yes.focus_set()
        
    elif type_ == 'askyesnocancel':
        btn_yes = tk.Button(btn_container, text=yes_text or 'Oui', font=('Segoe UI', 10, 'bold'),
                            bg='#38d66b', fg='#000000',
                            width=yes_width, command=lambda: close(True))
        btn_no = tk.Button(btn_container, text=no_text or 'Non', font=('Segoe UI', 10, 'bold'),
                           bg='#ff8379', fg='#000000',
                           width=no_width, command=lambda: close(False))
        btn_cancel = tk.Button(btn_container, text=cancel_text or 'Annuler', font=('Segoe UI', 10, 'bold'),
                               bg='#ffc107', fg='#000000',
                               width=cancel_width, command=lambda: close(None))
        btn_yes.pack(side='left', padx=8)
        btn_no.pack(side='left', padx=8)
        btn_cancel.pack(side='left', padx=8)
        btn_yes.focus_set()
    
    help_frame = tk.Frame(main_frame, bg=theme["bg"])
    help_frame.pack(pady=(10, 0), fill='x', padx=10)
    
    icon_emoji = {'info': 'ℹ️', 'warning': '⚠️', 'error': '❌', 'askyesno': '❓', 'askyesnocancel': '❓'}.get(type_, 'ℹ️')
    hint_text = "Astuce: Clic droit pour copier • Ctrl+A pour tout sélectionner • Ctrl+C pour copier"
    
    hint_container = tk.Frame(help_frame, bg=theme["bg"])
    hint_container.pack()

    tk.Label(hint_container, text=icon_emoji, font=('Segoe UI Emoji', 14), 
             bg=theme["bg"], fg=theme.get("secondary_fg", theme["fg"])).pack(side='left', padx=(0, 10))
    tk.Label(hint_container, text=hint_text, font=('Segoe UI', 9), 
             bg=theme["bg"], fg=theme.get("secondary_fg", theme["fg"])).pack(side='left')
    tk.Label(hint_container, text=icon_emoji, font=('Segoe UI Emoji', 14), 
             bg=theme["bg"], fg=theme.get("secondary_fg", theme["fg"])).pack(side='left', padx=(10, 0))

    popup.wait_window()
    return result['value']

def show_custom_askyesnocancel(title, message, theme, yes_text, no_text, cancel_text, parent=None):
    return show_custom_messagebox('askyesnocancel', title, message, theme, yes_text, no_text, cancel_text, parent=parent)


# =====================================================================
# EXTRACTION ET ANALYSE DE FICHIERS
# =====================================================================

def extract_game_name(filepath: str) -> str:
    from infrastructure.logging.logging import log_message # <-- IMPORT LOCAL
    try:
        if not filepath: return "Projet_Inconnu"
        if filepath.startswith("clipboard_"):
            parts = filepath.split("_")
            return f"Clipboard_{parts[2].replace('.rpy', '')}" if len(parts) >= 3 else "Projet_Clipboard"
        
        normalized_path = filepath.replace('\\', '/')
        path_parts = [part for part in normalized_path.split('/') if part]
        
        game_indices = [i for i, part in enumerate(path_parts) if part.lower() == 'game']
        for game_index in reversed(game_indices):
            if game_index > 0:
                game_name = path_parts[game_index - 1]
                
                return game_name
        
        if len(path_parts) > 1:
             parent_folder = path_parts[-2]
             if ":" not in parent_folder:
                 log_message("INFO", f"Nom de jeu extrait (fallback, parent): {parent_folder}", category="extraction_game_name")
                 return parent_folder
        return "Projet_Inconnu"
    except Exception as e:
        log_message("ERREUR", f"Erreur extraction nom de jeu pour {filepath}: {e}", category="extraction_game_name")
        return "Projet_Inconnu"

def get_file_base_name(filepath: str) -> str:
    if not filepath: return "fichier_inconnu"
    try: return os.path.splitext(os.path.basename(filepath))[0]
    except Exception: return "fichier_inconnu"

def sanitize_folder_name(name: str) -> str:
    """Version modifiée pour accepter [], -, _ dans les noms de dossiers"""
    if not name: return "dossier_vide"
    try:
        cleaned = name
        
        cleaned = cleaned.strip()
        # MODIFIÉ : Conserver les espaces normaux au lieu de les remplacer par des _
        cleaned = re.sub(r'\s{2,}', ' ', cleaned)  # Réduire seulement les espaces multiples
        
        # Supprimer uniquement les caractères de contrôle
        cleaned = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', cleaned)
        
        if len(cleaned) > 100:  # Augmenter la limite
            cleaned = cleaned[:100]
        
        if not cleaned or len(cleaned) < 1:  # Réduire le minimum
            return "dossier_nettoye"
        
        # Vérification des noms réservés Windows (inchangé)
        if cleaned.upper() in ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']: 
            return f"{cleaned}_Game"
        
        return cleaned
    except Exception: 
        return "dossier_erreur"

# =====================================================================
# VALIDATION DE FICHIERS ET CHEMINS
# =====================================================================

def validate_file_path(filepath: str) -> Dict[str, Any]:
    """Valide un chemin de fichier de manière complète"""
    result = {
        'valid': False,
        'exists': False,
        'is_file': False,
        'is_rpy': False,
        'readable': False,
        'size_mb': 0,
        'errors': [],
        'warnings': []
    }
    
    try:
        # Vérification de base
        if not filepath or not isinstance(filepath, str):
            result['errors'].append("Chemin invalide ou vide")
            return result
        
        # Existence
        if os.path.exists(filepath):
            result['exists'] = True
            
            # Type de fichier
            if os.path.isfile(filepath):
                result['is_file'] = True
                
                # Extension .rpy
                if filepath.lower().endswith('.rpy'):
                    result['is_rpy'] = True
                else:
                    result['errors'].append("Extension non .rpy")
                
                # Taille
                try:
                    size_bytes = os.path.getsize(filepath)
                    result['size_mb'] = size_bytes / (1024 * 1024)
                    
                    if result['size_mb'] > 50:
                        result['warnings'].append(f"Fichier volumineux: {result['size_mb']:.1f} MB")
                except Exception as e:
                    result['warnings'].append(f"Impossible de lire la taille: {e}")
                
                # Lisibilité
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        f.read(100)  # Test de lecture
                    result['readable'] = True
                except UnicodeDecodeError:
                    result['errors'].append("Fichier non encodé en UTF-8")
                except PermissionError:
                    result['errors'].append("Permissions de lecture insuffisantes")
                except Exception as e:
                    result['errors'].append(f"Erreur lecture: {e}")
            else:
                result['errors'].append("Le chemin ne pointe pas vers un fichier")
        else:
            result['errors'].append("Fichier introuvable")
        
        # Validation globale
        result['valid'] = (result['exists'] and result['is_file'] and 
                          result['is_rpy'] and result['readable'] and 
                          len(result['errors']) == 0)
        
        return result
        
    except Exception as e:
        result['errors'].append(f"Erreur inattendue: {e}")
        return result


def get_file_info(filepath: str) -> Dict[str, Any]:
    from infrastructure.logging.logging import log_message
    info = {'path': filepath, 'exists': False, 'name': '', 'base_name': '', 'extension': '', 'size_bytes': 0, 'size_mb': 0, 'created': None, 'modified': None, 'game_name': '', 'lines': 0, 'encoding': 'unknown'}
    try:
        if not os.path.exists(filepath): return info
        info['exists'] = True
        info['name'] = os.path.basename(filepath)
        info['base_name'] = get_file_base_name(filepath)
        info['extension'] = os.path.splitext(filepath)[1]
        info['game_name'] = extract_game_name(filepath)
        stat = os.stat(filepath)
        info['size_bytes'] = stat.st_size
        info['size_mb'] = stat.st_size / (1024 * 1024)
        info['created'] = datetime.datetime.fromtimestamp(stat.st_ctime)
        info['modified'] = datetime.datetime.fromtimestamp(stat.st_mtime)
        if filepath.lower().endswith(('.rpy', '.txt')):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    info['lines'] = len(f.readlines())
                    info['encoding'] = 'utf-8'
            except UnicodeDecodeError:
                try:
                    with open(filepath, 'r', encoding='latin1') as f:
                        info['lines'] = len(f.readlines())
                        info['encoding'] = 'latin1'
                except Exception: info['encoding'] = 'unknown'
            except Exception: pass
        return info
    except Exception as e:
        log_message("ATTENTION", f"Erreur get_file_info pour {filepath}: {e}", category="utils_unified")
        return info

# =====================================================================
# INTERFACE UTILISATEUR ET MESSAGES - VERSION AVEC SÉLECTION
# =====================================================================

def show_translated_messagebox(box_type: str, title_key: str, message_key: str, **kwargs):
    from infrastructure.logging.logging import log_message
    try:
        from infrastructure.config.config import config_manager
        parent = kwargs.pop('parent', None)
        title, message = str(title_key), str(message_key)
        try:
            format_kwargs = {k: v for k, v in kwargs.items() if k != 'parent'}
            if '{' in title: title = title.format(**format_kwargs)
            if '{' in message: message = message.format(**format_kwargs)
        except Exception as e:
            log_message("ATTENTION", f"Erreur remplacement placeholders: {e}", category="utils_unified")
            for key, value in kwargs.items():
                if key != 'parent':
                    placeholder = '{' + key + '}'
                    title = title.replace(placeholder, str(value))
                    message = message.replace(placeholder, str(value))
        
        message, title = clean_translation_artifacts(message), clean_translation_artifacts(title)
        
        try:
            from ui.themes import theme_manager
            theme = theme_manager.get_theme()
            if box_type.lower() in ['info', 'warning', 'error']:
                show_custom_messagebox(box_type.lower(), title, message, theme, parent=parent)
                return True
            elif box_type.lower() == 'askyesno':
                return show_custom_messagebox('askyesno', title, message, theme, yes_text='Oui', no_text='Non', parent=parent)
            else:
                show_custom_messagebox('info', title, message, theme, parent=parent)
                return True
        except Exception as e:
            log_message("ATTENTION", f"Erreur messagebox custom: {e}", category="utils_unified")
            import tkinter.messagebox as messagebox
            if 'askyesno' in box_type.lower(): return messagebox.askyesno(title, message)
            elif 'warning' in box_type.lower(): messagebox.showwarning(title, message)
            elif 'error' in box_type.lower(): messagebox.showerror(title, message)
            else: messagebox.showinfo(title, message)
            return True
    except Exception as e:
        try:
            import tkinter.messagebox as messagebox
            fallback_title = str(title_key)
            fallback_message = str(message_key)
            fallback_title, fallback_message = clean_translation_artifacts(fallback_title), clean_translation_artifacts(fallback_message)
            if 'askyesno' in box_type.lower(): return messagebox.askyesno(fallback_title, fallback_message)
            else: messagebox.showinfo(fallback_title, fallback_message)
            return True
        except Exception:
            log_message("ERREUR", f"Erreur critique show_translated_messagebox: {e}", category="utils_unified")
            return False

def clean_translation_artifacts(text: str) -> str:
    if not isinstance(text, str): return str(text)
    try:
        text = re.sub(r'^\[([^\]]+)\]', r'\1', text)
        text = text.replace('\\n\\n', '\n\n').replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r').replace('\\\\"', '"').replace('\\\\', '\\')
        text = re.sub(r'\n\s*\n', '\n\n', text).strip()
        return text
    except Exception:
        return str(text)
# =====================================================================
# GESTION DES DERNIERS DOSSIERS UTILISÉS
# =====================================================================

def get_last_directory() -> str:
    """
    Récupère le dernier dossier utilisé
    
    Returns:
        str: Chemin du dernier dossier utilisé
    """
    try:
        from .config import config_manager
        return config_manager.get('last_directory', '')
    except ImportError:
        return ''

def set_last_directory(directory_path: str) -> bool:
    """
    Sauvegarde le dernier dossier utilisé
    
    Args:
        directory_path (str): Chemin du dossier à sauvegarder
        
    Returns:
        bool: True si sauvegardé avec succès
    """
    try:
        from .config import config_manager
        config_manager.set('last_directory', directory_path)
        return True
    except ImportError:
        return False

def get_last_game_directory() -> str:
    """
    Récupère le dernier dossier game utilisé
    
    Returns:
        str: Chemin du dernier dossier game utilisé
    """
    try:
        from .config import config_manager
        return config_manager.get('last_game_directory', '')
    except ImportError:
        return ''

def set_last_game_directory(directory_path: str) -> bool:
    """
    Sauvegarde le dernier dossier game utilisé
    
    Args:
        directory_path (str): Chemin du dossier game à sauvegarder
        
    Returns:
        bool: True si sauvegardé avec succès
    """
    try:
        from .config import config_manager
        config_manager.set('last_game_directory', directory_path)
        return True
    except ImportError:
        return False

# Export des fonctions principales
__all__ = [
    'extract_game_name', 'get_file_base_name', 'sanitize_folder_name',
    'validate_file_path', 'get_file_info', 'show_translated_messagebox',
    'show_custom_messagebox', 'show_custom_askyesnocancel',
    'clean_translation_artifacts', 'get_last_directory', 'set_last_directory', 'get_last_game_directory', 'set_last_game_directory'
]