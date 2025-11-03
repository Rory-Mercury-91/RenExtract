# core/services/tools/coherence_line_editor.py
"""
Éditeur de lignes pour les corrections depuis le rapport de cohérence
- Modification sécurisée avec backup automatique
- Validation syntaxe Ren'Py
- Remplacement uniquement du contenu entre guillemets
"""

import os
import re
from pathlib import Path
from typing import Tuple, List, Dict, Any
from infrastructure.logging.logging import log_message
from core.models.backup.unified_backup_manager import UnifiedBackupManager, BackupType


def _validate_renpy_syntax(content: str) -> Tuple[bool, str]:
    """
    Valide la syntaxe Ren'Py de base du contenu
    
    Returns:
        (bool, str): (valide, message d'erreur)
    """
    try:
        # Vérifier l'équilibre des guillemets
        double_quotes = content.count('"')
        if double_quotes % 2 != 0:
            return False, "Guillemets non équilibrés"
        
        # Vérifier l'équilibre des crochets [ ]
        open_brackets = content.count('[')
        close_brackets = content.count(']')
        if open_brackets != close_brackets:
            return False, "Crochets [ ] non équilibrés"
        
        # Vérifier l'équilibre des accolades { }
        open_braces = content.count('{')
        close_braces = content.count('}')
        if open_braces != close_braces:
            return False, "Accolades { } non équilibrées"
        
        # Vérifier l'équilibre des parenthèses ( )
        open_parens = content.count('(')
        close_parens = content.count(')')
        if open_parens != close_parens:
            return False, "Parenthèses ( ) non équilibrées"
        
        return True, ""
        
    except Exception as e:
        return False, f"Erreur validation: {str(e)}"


def _find_project_root(file_path: str) -> str:
    """Trouve la racine du projet (dossier contenant 'game/')"""
    try:
        path = Path(file_path).resolve()
        
        # Remonter jusqu'à trouver 'game/' ou 'tl/'
        for parent in path.parents:
            if (parent / 'game').exists() or (parent / 'tl').exists():
                return str(parent)
        
        # Fallback: utiliser le parent du fichier
        return str(path.parent)
        
    except Exception:
        return os.path.dirname(file_path)


def _reconstruct_absolute_path(project_path: str, relative_file: str, language: str = 'french') -> str:
    """
    Reconstruit le chemin absolu depuis le chemin relatif
    
    Args:
        project_path: Racine du projet
        relative_file: Chemin relatif (ex: "script.rpy" ou "subfolder/choices.rpy")
        language: Langue de traduction (ex: 'french', 'english')
    
    Returns:
        Chemin absolu du fichier
    """
    try:
        project = Path(project_path)
        
        # Construire le chemin directement avec la langue spécifiée
        tl_dir = project / 'game' / 'tl' / language
        if not tl_dir.exists():
            tl_dir = project / 'tl' / language
        
        potential_file = tl_dir / relative_file
        if potential_file.exists():
            return str(potential_file)
        
        # Fallback: essayer dans tous les dossiers si pas trouvé
        tl_root = project / 'game' / 'tl'
        if not tl_root.exists():
            tl_root = project / 'tl'
        
        if tl_root.exists():
            for lang_dir in tl_root.iterdir():
                if lang_dir.is_dir():
                    potential_file = lang_dir / relative_file
                    if potential_file.exists():
                        return str(potential_file)
        
        # Fallback final: construire avec la langue spécifiée
        return str(project / 'game' / 'tl' / language / relative_file)
        
    except Exception as e:
        log_message("ERREUR", f"Erreur reconstruction chemin: {e}", category="coherence_editor")
        return os.path.join(project_path, relative_file)


def edit_coherence_line(project_path: str, file_path: str, line_number: int, 
                       new_content: str, language: str = 'french') -> Tuple[bool, str]:
    """
    Modifie une ligne dans un fichier de traduction
    
    Args:
        project_path: Racine du projet OU chemin complet du fichier (auto-détecté)
        file_path: Chemin relatif du fichier
        line_number: Numéro de ligne (1-indexed)
        new_content: Nouveau contenu pour la partie "new"
        language: Langue de traduction (défaut: 'french')
    
    Returns:
        (bool, str): (succès, message)
    """
    try:
        log_message("DEBUG", f"edit_coherence_line - Début: file={file_path}, line={line_number}", category="coherence_editor")
        log_message("DEBUG", f"edit_coherence_line - content: {repr(new_content)[:100]}", category="coherence_editor")
        
        # Valider la syntaxe avant toute modification
        is_valid, error_msg = _validate_renpy_syntax(new_content)
        if not is_valid:
            log_message("ERREUR", f"Validation syntaxe échouée: {error_msg}", category="coherence_editor")
            return False, f"Syntaxe invalide: {error_msg}"
        
        log_message("DEBUG", "Validation syntaxe OK", category="coherence_editor")
        
        # 🔧 CORRECTIF: Détecter si project_path est déjà un chemin de fichier complet
        # Si project_path contient file_path à la fin, c'est qu'on a reçu le chemin complet
        project_path_normalized = project_path.replace('\\', '/')
        file_path_normalized = file_path.replace('\\', '/')
        
        if project_path_normalized.endswith(file_path_normalized):
            # project_path contient déjà le chemin complet du fichier
            absolute_path = project_path
            log_message("DEBUG", f"Chemin complet détecté: {absolute_path}", category="coherence_editor")
        else:
            # Reconstruire le chemin absolu avec la langue
            absolute_path = _reconstruct_absolute_path(project_path, file_path, language)
            log_message("DEBUG", f"Chemin reconstruit: {absolute_path} (langue: {language})", category="coherence_editor")
        
        if not os.path.exists(absolute_path):
            return False, f"Fichier introuvable: {absolute_path}"
        
        # Créer un backup avant modification
        backup_manager = UnifiedBackupManager()
        backup_result = backup_manager.create_backup(
            source_path=absolute_path,
            backup_type=BackupType.COHERENCE_EDIT,
            description=f"Avant modification ligne {line_number}"
        )
        
        if not backup_result['success']:
            log_message("ATTENTION", f"Backup échoué mais poursuite: {backup_result.get('error')}", 
                       category="coherence_editor")
        
        # Lire le fichier
        with open(absolute_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Vérifier que le numéro de ligne est valide (1-indexed)
        if line_number < 1 or line_number > len(lines):
            return False, f"Numéro de ligne invalide: {line_number} (fichier: {len(lines)} lignes)"
        
        # Récupérer la ligne (convertir en 0-indexed)
        line_index = line_number - 1
        original_line = lines[line_index]
        
        # Pattern pour matcher TOUS les types de lignes Ren'Py avec dialogues
        # Formats supportés:
        # - new "contenu"               (strings/menus)
        # - personnage "contenu"        (dialogues avec nom)
        # - i "contenu"                 (dialogues avec préfixe court)
        # - "contenu"                   (dialogues narrateur)
        # - ALE "\"contenu\""           (avec guillemets échappés)
        # 
        # ✅ CORRIGÉ : Pattern pour gérer les guillemets échappés \"
        # Pattern: ^(\s*)([^"]*")((?:\\.|[^\"])*)(")(.*)$
        # Groupe 1: espaces initiaux
        # Groupe 2: tout avant le premier guillemet + guillemet ouvrant
        # Groupe 3: contenu entre guillemets (gère les échappements \")
        # Groupe 4: guillemet fermant
        # Groupe 5: texte après le guillemet fermant (optionnel, ex: "with speechfade.")
        # (?:\\.|[^\"])* = séquence échappée (backslash + char) OU tout sauf guillemet non échappé
        
        dialogue_pattern = r'^(\s*)([^"]*")((?:\\.|[^\"])*)(")(.*)$'
        
        match = re.search(dialogue_pattern, original_line)
        if not match:
            # Log plus détaillé pour debug
            log_message("DEBUG", f"Ligne {line_number} ne matche pas le format dialogue : '{original_line.strip()}'", 
                       category="coherence_editor")
            return False, f"Ligne non conforme au format Ren'Py dialogue (contenu: {original_line.strip()[:50]})"
        
        # Remplacer uniquement le contenu entre guillemets
        indent = match.group(1)      # Espaces initiaux
        prefix = match.group(2)      # Tout avant le premier " + "
        old_content = match.group(3) # Ancien contenu (peut contenir des \")
        suffix = match.group(4)      # " fermant
        after_quote = match.group(5) if len(match.groups()) > 4 else ""  # Texte après " (ex: "with speechfade.")
        
        # ✅ CORRIGÉ : Échapper les guillemets dans le nouveau contenu si nécessaire
        # Si l'ancien contenu avait des guillemets échappés, on doit aussi échapper ceux du nouveau
        # Échapper tous les guillemets qui ne sont pas déjà échappés
        escaped_new_content = re.sub(r'(?<!\\)"', r'\\"', new_content)
        
        # Conserver l'indentation, le texte après guillemets et le retour à la ligne
        modified_line = f"{indent}{prefix}{escaped_new_content}{suffix}{after_quote}\n"
        
        # Appliquer la modification
        lines[line_index] = modified_line
        
        # Écrire le fichier
        with open(absolute_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        log_message("INFO", f"✅ Ligne {line_number} modifiée dans {os.path.basename(absolute_path)}", 
                   category="coherence_editor")
        return True, "Modification appliquée avec succès"
        
    except Exception as e:
        log_message("ERREUR", f"Erreur modification ligne: {e}", category="coherence_editor")
        return False, f"Erreur: {str(e)}"


def save_all_modifications(project_path: str, modifications: List[Dict[str, Any]]) -> Tuple[int, int, List[str]]:
    """
    Applique plusieurs modifications en lot
    
    Args:
        project_path: Racine du projet
        modifications: Liste de dicts avec {file, line, new_content}
    
    Returns:
        (int, int, List[str]): (succès, échecs, messages)
    """
    try:
        success_count = 0
        failed_count = 0
        messages = []
        
        for mod in modifications:
            file_path = mod.get('file', '')
            line = mod.get('line', 0)
            new_content = mod.get('new_content', '')
            
            if not file_path or not new_content or line == 0:
                failed_count += 1
                messages.append(f"❌ {file_path}:{line} - Données incomplètes")
                continue
            
            success, message = edit_coherence_line(project_path, file_path, line, new_content)
            
            if success:
                success_count += 1
                messages.append(f"✅ {file_path}:{line}")
            else:
                failed_count += 1
                messages.append(f"❌ {file_path}:{line} - {message}")
        
        return success_count, failed_count, messages
        
    except Exception as e:
        log_message("ERREUR", f"Erreur enregistrement global: {e}", category="coherence_editor")
        return 0, len(modifications), [f"Erreur critique: {str(e)}"]

