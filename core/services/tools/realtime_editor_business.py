# core/business/realtime_editor_business.py
# Logique métier pour l'éditeur de traduction temps réel
# Created for RenExtract v2.8.0

"""
Logique métier pour l'édition de traductions en temps réel
- Génération du module de surveillance Ren'Py
- Monitoring des fichiers log
- Gestion des modifications de traductions
- Sauvegarde avec backup REALTIME_EDIT
"""

import os
import threading
import time
import re
import json
from typing import Dict, List, Optional, Callable, Any
from pathlib import Path

from infrastructure.logging.logging import log_message
from infrastructure.config.config import config_manager
from core.models.backup.unified_backup_manager import UnifiedBackupManager, BackupType


class RealTimeEditorBusiness:
    """Logique métier pour l'éditeur temps réel"""
    
    # Dictionnaire de compatibilité Ren'Py → Module
    MODULE_COMPATIBILITY = {
        (8, 1, 1): "v1",  # Compatible avec le module v1
        (8, 1, 2): "v1",  # Testé sur Nudist Olivia
        (8, 2, 1): "v1",  # Testé sur FamilyIsland
        (8, 3, 2): "v1",  # Compatible avec le module v1
        (8, 3, 7): "v1",  # Compatible avec le module v1
        (7, 3, 5): "v2",  # ✅ Ren'Py 7.3.5 validé (dialogues + choix)
        (7, 6, 3): "v2",  # En attente de traitement, utilise le module v2
        (7, 6, 1): "v2",  # ✅ Ren'Py 7.6.1 validé sur Girl Scout Island (reload + choix OK)
        # Ajoutez ici les futures versions et modules
    }
    
    def __init__(self):
        """Initialise la logique métier"""
        self.backup_manager = UnifiedBackupManager()
        self.monitoring_active = False
        self.current_project_path = None
        self.current_language = None
        self.pending_modifications_file = None
        self.last_dialogue_line = 0
        self.pending_modifications = {}
        
        # Callbacks pour l'interface
        self.dialogue_callback: Optional[Callable] = None
        self.status_callback: Optional[Callable] = None
        self.error_callback: Optional[Callable] = None
        self.string_translation_cache: Optional[Dict[str, Any]] = None        
        log_message("INFO", "RealTimeEditorBusiness initialisé", category="realtime_editor")
    
    def set_callbacks(self, dialogue_callback: Callable = None, 
                     status_callback: Callable = None,
                     error_callback: Callable = None):
        """Configure les callbacks pour l'interface"""
        self.dialogue_callback = dialogue_callback
        self.status_callback = status_callback
        self.error_callback = error_callback
    
    def _update_status(self, message: str):
        """Met à jour le statut"""
        if self.status_callback:
            try:
                self.status_callback(message)
            except Exception as e:
                log_message("ATTENTION", f"Erreur callback status: {e}", category="realtime_editor")
        log_message("INFO", f"Status: {message}", category="realtime_editor")

    def _build_string_translation_cache(self):
        """Scanne tous les fichiers de traduction une fois et construit un cache en mémoire."""
        self._update_status("Création du cache de traductions...")
        log_message("INFO", "Début de la construction du cache de traductions.", "realtime_editor")
        cache: Dict[str, Any] = {}
        
        try:
            game_dir = os.path.join(self.current_project_path, "game")
            target_path_segment = os.path.join("tl", self.current_language)

            for root, _, files in os.walk(game_dir):
                if target_path_segment in root:
                    for filename in files:
                        if filename.endswith('.rpy'):
                            filepath = os.path.join(root, filename)
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                lines = f.readlines()

                            for i, line in enumerate(lines):
                                if line.strip().startswith('old '):
                                    old_match = re.search(r'old\s+"((?:\\.|[^"])*)"', line)
                                    if old_match:
                                        old_text = old_match.group(1)
                                        if i + 1 < len(lines):
                                            next_line = lines[i + 1]
                                            new_match = re.search(r'new\s+"((?:\\.|[^"])*)"', next_line)
                                            if new_match:
                                                translated_text = new_match.group(1)
                                                rel_path = os.path.relpath(filepath, self.current_project_path)
                                                cache[old_text] = {
                                                    'translated_text': translated_text,
                                                    'tl_file': rel_path,
                                                    'tl_line': i + 2
                                                }
        except Exception as e:
            log_message("ERREUR", f"Erreur lors de la création du cache: {e}", "realtime_editor")

        self.string_translation_cache = cache
        self._update_status(f"Cache créé ({len(cache)} entrées). Surveillance prête.")
        log_message("INFO", f"Cache de traductions construit avec {len(cache)} entrées.", "realtime_editor")

    def _find_string_translation_in_project(self, original_text: str) -> Dict[str, Any]:
        """Recherche la traduction d'un string en utilisant le cache en mémoire."""
        # Si le cache n'est pas encore prêt, on attend un tout petit peu.
        if self.string_translation_cache is None:
            time.sleep(0.5) # Petite attente pour que le cache finisse de se construire

        # Si toujours pas prêt (très gros projet), on fait une recherche normale en fallback
        if self.string_translation_cache is None:
            log_message("ATTENTION", "Cache non disponible, recherche en temps réel effectuée.", "realtime_editor")
            # Ici on pourrait appeler l'ancienne fonction de recherche si on voulait un fallback
            return {'translated_text': original_text, 'tl_file': None, 'tl_line': 0}

        # On cherche dans le cache. C'est quasi-instantané.
        default_value = {'translated_text': original_text, 'tl_file': None, 'tl_line': 0}
        return self.string_translation_cache.get(original_text, default_value)

    def save_choice_translation(self, choice_info: Dict, new_translation: str, project_path: str = None) -> Dict[str, Any]:
        """Sauvegarde la traduction d'un choix (string)"""
        result = {'success': False, 'errors': [], 'backup_created': False}
        
        try:
            base_project = project_path or self.current_project_path
            if not base_project:
                result['errors'].append("Projet non défini")
                return result
            
            tl_file = choice_info.get('tl_file')
            tl_line = choice_info.get('tl_line', 0)
            
            if not tl_file or tl_line <= 0:
                result['errors'].append("Informations de fichier incomplètes")
                return result
            
            # Construire le chemin complet
            tl_file_path = os.path.join(base_project, tl_file)
            if not os.path.exists(tl_file_path):
                tl_file_path = os.path.join(base_project, "game", tl_file)
                if not os.path.exists(tl_file_path):
                    result['errors'].append("Fichier de traduction non trouvé")
                    return result
            
            # Créer un backup
            backup_result = self.backup_manager.create_backup(
                tl_file_path,
                BackupType.REALTIME_EDIT,
                "Sauvegarde avant modification choix temps réel"
            )
            if backup_result.get('success'):
                result['backup_created'] = True
            
            # Charger et modifier le fichier
            with open(tl_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            target_index = tl_line - 1
            if target_index < 0 or target_index >= len(lines):
                result['errors'].append("Ligne hors limites")
                return result
            
            # Remplacer la ligne "new"
            line = lines[target_index]
            if 'new ' in line:
                escaped_text = self._escape_quotes_properly(new_translation)
                new_line = re.sub(
                    r'(new\s+")([^"]*)(.*")',
                    r'\1' + escaped_text + r'\3',
                    line
                )
                lines[target_index] = new_line
            
            # Écrire le fichier
            with open(tl_file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            result['success'] = True
            result['modified_file'] = tl_file_path
            result['modified_line'] = tl_line
            
            log_message("INFO", f"Choix sauvegardé: {os.path.basename(tl_file_path)}:{tl_line}", category="realtime_editor")
            
        except Exception as e:
            result['errors'].append(f"Erreur sauvegarde choix: {e}")
            log_message("ERREUR", f"Erreur sauvegarde choix: {e}", category="realtime_editor")
        
        return result

    # ===================================================================
    # NOUVELLE FONCTION AJOUTÉE
    # ===================================================================
    def detect_multiple_dialogue_group(self, lines: List[str], target_line: int) -> Dict[str, Any]:
        """
        Version 3 - Robuste et définitive - Testée avec le fichier fourni.
        Cette version identifie tous les blocs 'multiple', les partitionne en groupes
        de la bonne taille, puis localise le groupe auquel appartient le dialogue actuel.
        """
        log_message("DEBUG", f"=== DÉBUT DÉTECTION MULTIPLE (v3 - DÉFINITIVE) - Ligne {target_line} ===", category="realtime_editor")

        if not (0 <= target_line < len(lines)):
            return {'is_multiple': False}

        # Étape 1: Extraire le numéro 'multiple' de la ligne actuelle pour savoir quoi chercher.
        current_line_text = lines[target_line]
        multiple_match = re.search(r'\(multiple=(\d+)\)\s*$', current_line_text)
        if not multiple_match:
            log_message("DEBUG", "Pas de tag (multiple=X) sur la ligne cible.", category="realtime_editor")
            return {'is_multiple': False}
        
        target_multiple_number = int(multiple_match.group(1))
        tag_to_find = f"(multiple={target_multiple_number})"

        # --- Fonctions utilitaires internes ---
        def get_block_starts(file_lines: List[str]) -> List[int]:
            """Retourne les indices de début de tous les blocs 'translate'."""
            return [i for i, line in enumerate(file_lines) if line.strip().startswith('translate ')]

        def extract_from_block(start_idx: int, end_idx: int) -> Optional[Dict[str, Any]]:
            """Extrait les infos d'un bloc s'il contient le tag recherché."""
            vo_text = None
            vf_text = None
            vf_line_index = -1
            
            vf_candidates = []
            for i in range(start_idx, end_idx):
                line = lines[i].strip()
                if tag_to_find in line and not line.startswith('#'):
                    dialogue_match = re.search(r'"(.*?)"', line)
                    if dialogue_match:
                        vf_candidates.append({'text': dialogue_match.group(1), 'index': i})

            if not vf_candidates:
                return None
            
            vf_line_index = vf_candidates[-1]['index']
            vf_text = vf_candidates[-1]['text']
            
            for j in range(vf_line_index - 1, start_idx -1, -1):
                prev_line = lines[j].strip()
                if prev_line.startswith('#'):
                    vo_match = re.search(r'"(.*?)"', prev_line)
                    if vo_match:
                        vo_text = vo_match.group(1)
                        break
            
            # CORRECTION : Ajouter 'original_text' pour l'interface VO
            vo_dialogue_text = vo_text or ""
            return {
                'vo_dialogue': {
                    'line_index': -1, 
                    'dialogue_text': vo_dialogue_text,
                    'original_text': vo_dialogue_text  # ✅ Pour l'affichage VO dans l'interface
                }, 
                'vf_dialogue': {'line_index': vf_line_index, 'dialogue_text': vf_text},
                'start_line': start_idx
            }

        # --- Logique principale ---
        all_block_starts = get_block_starts(lines)
        tagged_blocks = []
        for i, start_line in enumerate(all_block_starts):
            end_line = all_block_starts[i + 1] if i + 1 < len(all_block_starts) else len(lines)
            block_data = extract_from_block(start_line, end_line)
            if block_data:
                tagged_blocks.append(block_data)
        
        if not tagged_blocks:
            return {'is_multiple': False}

        all_groups = [tagged_blocks[i:i + target_multiple_number] for i in range(0, len(tagged_blocks), target_multiple_number) if len(tagged_blocks[i:i + target_multiple_number]) == target_multiple_number]

        target_group = None
        for group in all_groups:
            if any(block['vf_dialogue']['line_index'] == target_line for block in group):
                target_group = group
                break
        
        if not target_group:
            return {'is_multiple': False}

        vo_dialogues = [block['vo_dialogue'] for block in target_group]
        vf_dialogues = [block['vf_dialogue'] for block in target_group]
        
        dialogue_count = len(target_group)
        grid_rows, grid_cols = (1, 2) if dialogue_count <= 2 else (2, 2)

        return {
            'is_multiple': True,
            'multiple_number': dialogue_count,
            'group_size': dialogue_count,
            'vo_dialogues': vo_dialogues,
            'vf_dialogues': vf_dialogues,
            'dialogues': vf_dialogues,
            'grid_rows': grid_rows,
            'grid_cols': grid_cols
        }

    # ===================================================================
    # FONCTION MODIFIÉE pour appeler la nouvelle détection
    # ===================================================================
    def _check_for_multiple_dialogues(self, dialogue_info):
        """
        Version "aiguillage" qui utilise la nouvelle fonction de détection robuste.
        """
        try:
            tl_file_path = dialogue_info.get('tl_file')
            tl_line = dialogue_info.get('tl_line', 0)
            
            if not tl_file_path or not self.current_project_path:
                return {'is_multiple': False}
            
            full_tl_path = os.path.join(self.current_project_path, tl_file_path)
            if not os.path.exists(full_tl_path):
                # Essayer avec le préfixe "game/"
                full_tl_path = os.path.join(self.current_project_path, "game", tl_file_path)
                if not os.path.exists(full_tl_path):
                    return {'is_multiple': False}
            
            with open(full_tl_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            target_line_index = tl_line - 1
            
            # Appel de votre nouvelle fonction de détection
            multiple_result = self.detect_multiple_dialogue_group(lines, target_line_index)
            
            if not multiple_result['is_multiple']:
                return {'is_multiple': False}
            
            # Enrichir le résultat pour l'interface
            multiple_result.update({
                'is_multiple_group': True,
                'tl_file': tl_file_path,
                'displayed_text': dialogue_info.get('displayed_text', ''),
                'original_text': dialogue_info.get('original_text', ''),
                'source_file': dialogue_info.get('source_file', ''),
                'source_line': dialogue_info.get('source_line', 0)
            })
            
            return multiple_result
            
        except Exception as e:
            log_message("ERREUR", f"Erreur vérification dialogues multiples: {e}", category="realtime_editor")
            return {'is_multiple': False}

    def _notify_dialogue(self, dialogue_info: Dict):
        """Notifie un nouveau dialogue"""
        if self.dialogue_callback:
            try:
                self.dialogue_callback(dialogue_info)
            except Exception as e:
                log_message("ATTENTION", f"Erreur callback dialogue: {e}", category="realtime_editor")


    def _init_pending_modifications_file(self, project_path: str):
        """
        Version améliorée qui gère la migration automatique des anciens formats
        """
        self.pending_modifications_file = os.path.join(project_path, "renextract_pending_modifications.json")
        
        # VÉRIFIER s'il reste des données d'une session précédente (= crash détecté)
        if os.path.exists(self.pending_modifications_file):
            try:
                # Tenter la migration si nécessaire
                self._migrate_legacy_pending_file(self.pending_modifications_file)
                
                with open(self.pending_modifications_file, 'r', encoding='utf-8') as f:
                    previous_data = json.load(f)
                
                if previous_data:  # Il y avait des modifications non sauvées
                    # CRÉER le fichier de récupération
                    recovery_file = self.pending_modifications_file.replace('.json', '_recovery.json')
                    with open(recovery_file, 'w', encoding='utf-8') as f:
                        json.dump(previous_data, f, indent=2, ensure_ascii=False)
                    
                    log_message("INFO", f"Crash détecté: {len(previous_data)} modifications sauvées pour récupération", category="realtime_editor")
            except Exception as e:
                log_message("ATTENTION", f"Erreur détection crash: {e}", category="realtime_editor")
        
        # Réinitialiser pour la nouvelle session
        self.pending_modifications = {}
        with open(self.pending_modifications_file, 'w', encoding='utf-8') as f:
            json.dump({}, f)

    def save_speaker_dialogue_translation(self, dialogue_info: Dict, speaker_text: str, dialogue_text: str, project_path: str = None) -> Dict[str, Any]:
        """
        Sauvegarde une traduction avec locuteur non défini en modifiant les deux parties.
        Structure : "nouveau_locuteur" "nouveau_dialogue"
        """
        result: Dict[str, Any] = {'success': False, 'errors': [], 'backup_created': False}

        try:
            # 1) Résolution du chemin (même logique que save_translation)
            base_project = project_path or self.current_project_path
            if not base_project:
                result['errors'].append("Projet non défini")
                return result

            tl_rel = dialogue_info.get('tl_file')
            tl_line_no = int(dialogue_info.get('tl_line', 0))
            if not tl_rel or tl_line_no <= 0:
                result['errors'].append("Informations dialogue incomplètes")
                return result

            # Résoudre le chemin complet
            candidates = []
            if os.path.isabs(tl_rel):
                candidates.append(tl_rel)
            else:
                candidates.append(os.path.join(base_project, tl_rel))
                candidates.append(os.path.join(base_project, "game", tl_rel))

            tl_file_path = None
            for cand in candidates:
                if os.path.exists(cand):
                    tl_file_path = cand
                    break

            if not tl_file_path:
                result['errors'].append("Fichier de traduction non trouvé")
                return result

            # 2) Créer un backup
            backup_result = self.backup_manager.create_backup(
                tl_file_path,
                BackupType.REALTIME_EDIT,
                "Sauvegarde avant modification locuteur + dialogue"
            )
            if backup_result.get('success'):
                result['backup_created'] = True

            # 3) Charger le fichier
            with open(tl_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            target_index = tl_line_no - 1
            if target_index < 0 or target_index >= len(lines):
                result['errors'].append("Ligne de traduction hors limites")
                return result

            # 4) Modifier la ligne en remplaçant les deux segments
            original_line = lines[target_index]
            new_line = self._rebuild_speaker_dialogue_line(original_line, speaker_text, dialogue_text)
            
            if new_line is None:
                result['errors'].append("Impossible de reconstruire la ligne")
                return result
                
            lines[target_index] = new_line

            # 5) Écrire le fichier
            with open(tl_file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            # 6) Vider le fichier log
            log_file_path = os.path.join(base_project, "renextract_dialogue_log.txt")
            if os.path.exists(log_file_path):
                try:
                    with open(log_file_path, 'w', encoding='utf-8') as f:
                        f.write("")
                    self.last_dialogue_line = 0
                except Exception as e:
                    log_message("ATTENTION", f"Erreur vidage fichier log: {e}", category="realtime_editor")
            
            # ✅ Mettre à jour le cache de traductions avec la nouvelle valeur
            original_text = dialogue_info.get('original_text', '')
            if original_text and self.string_translation_cache is not None:
                rel_path = os.path.relpath(tl_file_path, base_project)
                # Pour les dialogues locuteur + dialogue, on stocke les deux parties séparées par un espace
                combined_translation = f'"{speaker_text}" "{dialogue_text}"'
                self.string_translation_cache[original_text] = {
                    'translated_text': combined_translation,
                    'tl_file': rel_path,
                    'tl_line': target_index + 1
                }
                log_message("DEBUG", f"Cache mis à jour pour locuteur + dialogue: {original_text[:50]}...", category="realtime_editor")
            
            result['success'] = True
            result['modified_file'] = tl_file_path
            result['modified_line'] = target_index + 1
            
            log_message("INFO", f"Locuteur + dialogue sauvegardés: {os.path.basename(tl_file_path)}", category="realtime_editor")
            return result

        except Exception as e:
            result['errors'].append(f"Erreur sauvegarde locuteur + dialogue: {e}")
            log_message("ERREUR", f"Erreur sauvegarde locuteur + dialogue: {e}", category="realtime_editor")
            return result

    def _escape_quotes_properly(self, text: str) -> str:
        """
        Échappe correctement les guillemets en évitant le double échappement.
        Ne modifie que les guillemets qui ne sont pas déjà échappés.
        """
        # Remplacer seulement les guillemets qui ne sont PAS précédés d'un backslash
        # Pattern : guillemet qui n'est pas précédé par un backslash
        result = re.sub(r'(?<!\\)"', r'\\"', text)
        
        return result

    def _rebuild_speaker_dialogue_line(self, original_line: str, speaker_text: str, dialogue_text: str) -> str:
        """
        Reconstruit une ligne en remplaçant les deux segments entre guillemets.
        Préserve la structure et l'indentation de la ligne originale.
        """
        # Échapper les guillemets correctement (sans double échappement)
        escaped_speaker = self._escape_quotes_properly(speaker_text)
        escaped_dialogue = self._escape_quotes_properly(dialogue_text)
        
        # Chercher tous les segments entre guillemets
        quote_pattern = r'\"((?:\\.|[^\"])*)\"'
        matches = list(re.finditer(quote_pattern, original_line))
        
        if len(matches) >= 2:
            # Remplacer les deux premiers segments
            result = original_line
            
            # Remplacer en ordre inverse pour préserver les indices
            # D'abord le deuxième segment (dialogue)
            second_match = matches[1]
            result = (result[:second_match.start(1)] + 
                    escaped_dialogue + 
                    result[second_match.end(1):])
            
            # Puis le premier segment (locuteur)
            first_match = matches[0]
            result = (result[:first_match.start(1)] + 
                    escaped_speaker + 
                    result[first_match.end(1):])
            
            return result
        
        return None

    def save_split_translation(self, dialogue_info: Dict, part1_text: str, part2_text: str, project_path: str = None) -> Dict[str, Any]:
        """Sauvegarde une traduction divisée en deux parties consécutives"""
        result: Dict[str, Any] = {'success': False, 'errors': [], 'backup_created': False}

        try:
            # 1) Résoudre le chemin du fichier cible
            base_project = project_path or self.current_project_path
            if not base_project:
                result['errors'].append("Projet non défini")
                return result

            tl_rel = dialogue_info.get('tl_file')
            tl_line_no = int(dialogue_info.get('tl_line', 0))
            if not tl_rel or tl_line_no <= 0:
                result['errors'].append("Informations dialogue incomplètes")
                return result

            # Résoudre le chemin complet
            candidates = []
            if os.path.isabs(tl_rel):
                candidates.append(tl_rel)
            else:
                candidates.append(os.path.join(base_project, tl_rel))
                candidates.append(os.path.join(base_project, "game", tl_rel))

            tl_file_path = None
            for cand in candidates:
                if os.path.exists(cand):
                    tl_file_path = cand
                    break

            if not tl_file_path:
                result['errors'].append("Fichier de traduction non trouvé")
                return result

            # 2) Créer un backup
            backup_result = self.backup_manager.create_backup(
                tl_file_path,
                BackupType.REALTIME_EDIT,
                "Sauvegarde avant modification split temps réel"
            )
            if backup_result.get('success'):
                result['backup_created'] = True

            # 3) Charger le fichier
            with open(tl_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            target_index = tl_line_no - 1
            if target_index < 0 or target_index >= len(lines):
                result['errors'].append("Ligne de traduction hors limites")
                return result

            # 4) Analyser la situation actuelle
            current_line = lines[target_index].strip()
            has_next_new = (target_index + 1 < len(lines) and 
                        lines[target_index + 1].strip().startswith('new '))

            if has_next_new:
                # Cas: Déjà split, on met à jour les deux parties
                self._update_split_lines(lines, target_index, part1_text, part2_text)
            else:
                # Cas: Ligne simple, on la divise en deux
                self._create_split_lines(lines, target_index, part1_text, part2_text)

            # 5) Écrire le fichier
            with open(tl_file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            # 6) Vider le fichier log pour forcer la recapture
            log_file_path = os.path.join(base_project, "renextract_dialogue_log.txt")
            if os.path.exists(log_file_path):
                try:
                    with open(log_file_path, 'w', encoding='utf-8') as f:
                        f.write("")
                    self.last_dialogue_line = 0
                except Exception as e:
                    log_message("ATTENTION", f"Erreur vidage fichier log: {e}", category="realtime_editor")
            
            # ✅ Mettre à jour le cache de traductions avec la nouvelle valeur combinée
            original_text = dialogue_info.get('original_text', '')
            if original_text and self.string_translation_cache is not None:
                rel_path = os.path.relpath(tl_file_path, base_project)
                # Pour les dialogues split, on stocke les deux parties concaténées avec un espace
                combined_translation = f"{part1_text} {part2_text}"
                self.string_translation_cache[original_text] = {
                    'translated_text': combined_translation,
                    'tl_file': rel_path,
                    'tl_line': target_index + 1
                }
                log_message("DEBUG", f"Cache mis à jour pour dialogue split: {original_text[:50]}...", category="realtime_editor")
            
            result['success'] = True
            result['modified_file'] = tl_file_path
            result['modified_lines'] = [target_index + 1, target_index + 2]
            
            log_message("INFO", f"Traduction split sauvegardée: {os.path.basename(tl_file_path)}", category="realtime_editor")
            return result

        except Exception as e:
            result['errors'].append(f"Erreur sauvegarde split: {e}")
            log_message("ERREUR", f"Erreur sauvegarde split: {e}", category="realtime_editor")
            return result

    def _update_split_lines(self, lines: list, target_index: int, part1_text: str, part2_text: str):
        """Met à jour deux lignes de dialogue existantes"""
        # Échapper les guillemets correctement (sans double échappement)
        part1_escaped = self._escape_quotes_properly(part1_text)
        part2_escaped = self._escape_quotes_properly(part2_text)
        
        # Conserver la structure originale de la ligne (personnage, indentation, etc.)
        original_line1 = lines[target_index]
        original_line2 = lines[target_index + 1] if target_index + 1 < len(lines) else original_line1
        
        # Extraire le préfixe (tout avant les guillemets)
        prefix1_match = re.match(r'^(.*?)(".*?)$', original_line1.rstrip())
        prefix2_match = re.match(r'^(.*?)(".*?)$', original_line2.rstrip())
        
        if prefix1_match and prefix2_match:
            prefix1 = prefix1_match.group(1)
            prefix2 = prefix2_match.group(1)
            
            # Reconstruire les lignes avec les nouveaux textes
            lines[target_index] = f'{prefix1}"{part1_escaped}"\n'
            if target_index + 1 < len(lines):
                lines[target_index + 1] = f'{prefix2}"{part2_escaped}"\n'
        else:
            # Fallback si le pattern ne correspond pas
            lines[target_index] = f'    n "{part1_escaped}"\n'
            if target_index + 1 < len(lines):
                lines[target_index + 1] = f'    n "{part2_escaped}"\n'

    def _create_split_lines(self, lines: list, target_index: int, part1_text: str, part2_text: str):
        """Divise une ligne de dialogue simple en deux lignes"""
        # Échapper les guillemets correctement (sans double échappement)
        part1_escaped = self._escape_quotes_properly(part1_text)
        part2_escaped = self._escape_quotes_properly(part2_text)
        
        # Conserver la structure originale de la ligne
        original_line = lines[target_index]
        
        # Extraire le préfixe (tout avant les guillemets)
        prefix_match = re.match(r'^(.*?)(".*?)$', original_line.rstrip())
        
        if prefix_match:
            prefix = prefix_match.group(1)
            
            # Remplacer la ligne actuelle par la première partie
            lines[target_index] = f'{prefix}"{part1_escaped}"\n'
            
            # Insérer la seconde partie juste après avec le même préfixe
            lines.insert(target_index + 1, f'{prefix}"{part2_escaped}"\n')
        else:
            # Fallback si le pattern ne correspond pas
            lines[target_index] = f'    n "{part1_escaped}"\n'
            lines.insert(target_index + 1, f'    n "{part2_escaped}"\n')

    def _find_merge_dialogue_block(self, lines: List[str], target_line: int) -> List[int]:
        """
        Trouve toutes les lignes de dialogue consécutives qui appartiennent au même bloc de traduction
        pour la fusion. Retourne les indices des lignes à fusionner.
        """
        dialogue_block = []
        
        # Commencer par la ligne cible
        if self._is_dialogue_line(lines[target_line]):
            dialogue_block.append(target_line)
        
        # Chercher vers le bas pour les lignes consécutives de dialogue
        for i in range(target_line + 1, len(lines)):
            line = lines[i].strip()
            
            # Arrêter si on trouve une ligne vide, un commentaire, ou un nouveau bloc translate
            if (not line or 
                line.startswith('#') or 
                line.startswith('translate ') or
                line.startswith('label ')):
                break
            
            # Ajouter si c'est une ligne de dialogue
            if self._is_dialogue_line(line):
                dialogue_block.append(i)
            else:
                # Si ce n'est pas un dialogue, arrêter la recherche
                break
        
        # AUSSI chercher vers le haut si la ligne cible n'était pas la première du bloc
        for i in range(target_line - 1, -1, -1):
            line = lines[i].strip()
            
            # Arrêter si on trouve une ligne vide, un commentaire, ou un nouveau bloc
            if (not line or 
                line.startswith('#') or 
                line.startswith('translate ') or
                line.startswith('label ')):
                break
            
            # Ajouter si c'est une ligne de dialogue (insérer au début)
            if self._is_dialogue_line(line):
                dialogue_block.insert(0, i)
            else:
                break
        
        return dialogue_block

    def save_merge_translation(self, dialogue_info: Dict, merged_text: str, project_path: str = None) -> Dict[str, Any]:
        """
        Fusionne deux lignes consécutives en une seule ligne en préservant le locuteur
        VERSION CORRIGÉE - gère mieux la suppression de ligne
        """
        result: Dict[str, Any] = {'success': False, 'errors': [], 'backup_created': False}
        
        try:
            # Logique de résolution du chemin (identique)
            base_project = project_path or self.current_project_path
            if not base_project:
                result['errors'].append("Projet non défini")
                return result
            
            tl_rel = dialogue_info.get('tl_file')
            tl_line_no = int(dialogue_info.get('tl_line', 0))
            
            # Résoudre le chemin et charger le fichier
            candidates = []
            if os.path.isabs(tl_rel):
                candidates.append(tl_rel)
            else:
                candidates.append(os.path.join(base_project, tl_rel))
                candidates.append(os.path.join(base_project, "game", tl_rel))
            
            tl_file_path = next((p for p in candidates if os.path.exists(p)), None)
            if not tl_file_path:
                result['errors'].append("Fichier de traduction non trouvé")
                return result
            
            # Backup
            backup_result = self.backup_manager.create_backup(
                tl_file_path, BackupType.REALTIME_EDIT, "Sauvegarde avant fusion temps réel"
            )
            if backup_result.get('success'):
                result['backup_created'] = True
            
            # Charger et analyser
            with open(tl_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            target_index = tl_line_no - 1
            
            if target_index < 0 or target_index >= len(lines):
                result['errors'].append("Ligne cible hors limites")
                return result
            
            # LOGIQUE CORRIGÉE : Identifier le bloc de dialogue complet à fusionner
            dialogue_block = self._find_merge_dialogue_block(lines, target_index)
            
            if len(dialogue_block) < 2:
                # C'est une modification simple, pas une fusion
                # On utilise la logique de save_translation pour ce cas
                return self.save_translation(dialogue_info, merged_text, project_path)

            # Extraire le locuteur de la première ligne du bloc
            first_line_index = dialogue_block[0]
            speaker = self._extract_speaker_from_line(lines[first_line_index].strip())
            
            # CORRECTION : Échapper correctement le texte fusionné
            escaped_text = self._escape_quotes_properly(merged_text)
            
            # Construire la nouvelle ligne avec le bon locuteur
            if speaker:
                new_line = f'    {speaker} "{escaped_text}"\n'
            else:
                new_line = f'    "{escaped_text}"\n'
            
            # CORRECTION PRINCIPALE : Remplacer la première ligne et supprimer les suivantes
            lines[first_line_index] = new_line
            
            # Supprimer toutes les lignes suivantes du bloc (en ordre inverse pour préserver les indices)
            for line_index in sorted(dialogue_block[1:], reverse=True):
                if line_index < len(lines):
                    lines.pop(line_index)
            
            # Sauvegarder
            with open(tl_file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            # Vider le log
            log_file_path = os.path.join(base_project, "renextract_dialogue_log.txt")
            if os.path.exists(log_file_path):
                with open(log_file_path, 'w', encoding='utf-8') as f:
                    f.write("")
                self.last_dialogue_line = 0
            
            # ✅ Mettre à jour le cache de traductions avec la nouvelle valeur fusionnée
            original_text = dialogue_info.get('original_text', '')
            if original_text and self.string_translation_cache is not None:
                rel_path = os.path.relpath(tl_file_path, base_project)
                self.string_translation_cache[original_text] = {
                    'translated_text': merged_text,
                    'tl_file': rel_path,
                    'tl_line': first_line_index + 1
                }
                log_message("DEBUG", f"Cache mis à jour pour dialogue fusionné: {original_text[:50]}...", category="realtime_editor")
            
            result['success'] = True
            result['modified_file'] = tl_file_path
            result['removed_lines'] = dialogue_block[1:]  # Lignes supprimées
            log_message("INFO", f"Traduction fusionnée: {len(dialogue_block)} lignes → 1 ligne", category="realtime_editor")
            
        except Exception as e:
            result['errors'].append(f"Erreur fusion: {e}")
            log_message("ERREUR", f"Erreur fusion traduction: {e}", category="realtime_editor")
        
        return result

    def _is_dialogue_line(self, line: str) -> bool:
        """
        Version améliorée pour vérifier si une ligne contient un dialogue
        """
        line_stripped = line.strip()
        
        # Ignorer les commentaires et lignes vides
        if not line_stripped or line_stripped.startswith('#'):
            return False
        
        # Ignorer les directives Ren'Py
        if (line_stripped.startswith('translate ') or 
            line_stripped.startswith('label ') or
            line_stripped.startswith('return') or
            line_stripped.startswith('jump ') or
            line_stripped.startswith('call ')):
            return False
        
        # Vérifier les patterns de dialogue
        dialogue_patterns = [
            r'^\s*\w+\s+"',          # Locuteur + dialogue (ex: p "...")
            r'^\s*new\s+"',          # new "dialogue"
            r'^\s*old\s+"',          # old "dialogue"  
            r'^\s*"',                # Dialogue sans locuteur
        ]
        
        return any(re.search(pattern, line) for pattern in dialogue_patterns)

    def _extract_speaker_from_line(self, line: str) -> Optional[str]:
        """Extrait le locuteur d'une ligne de dialogue"""
        # Patterns courants pour les lignes de dialogue
        patterns = [
            r'^\s*(\w+)\s+"',        # "    p "dialogue""
            r'^\s*new\s+"',          # "    new "dialogue"" (pas de locuteur)
            r'^\s*old\s+"',          # "    old "dialogue"" (pas de locuteur)
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                speaker = match.group(1) if match.lastindex else None
                # Exclure les mots-clés qui ne sont pas des locuteurs
                if speaker and speaker not in ['new', 'old']:
                    return speaker
                elif pattern.startswith(r'^\s*(new|old)'):
                    return None  # Ligne new/old sans locuteur
        
        return None

    def load_recovery_data(self, recovery_file_path: str) -> Dict[str, Any]:
        """
        Charge les données de récupération avec gestion de compatibilité entre versions
        """
        result = {'success': False, 'recovered_count': 0, 'errors': [], 'legacy_converted': 0}
        
        try:
            with open(recovery_file_path, 'r', encoding='utf-8') as f:
                recovery_data = json.load(f)
            
            converted_data = {}
            legacy_count = 0
            
            for key, mod_entry in recovery_data.items():
                # Vérifier si c'est l'ancien format ou le nouveau
                if isinstance(mod_entry, dict) and 'version' in mod_entry:
                    # Nouveau format, utiliser tel quel
                    converted_data[key] = mod_entry
                elif isinstance(mod_entry, dict) and 'new_translation' in mod_entry:
                    # Ancien format, convertir
                    dialogue_info = mod_entry.get('dialogue_info', {})
                    new_translation = mod_entry.get('new_translation', '')
                    timestamp = mod_entry.get('timestamp', time.time())
                    
                    # Analyser le contenu pour déterminer le type
                    if '|||' in new_translation:
                        # C'était un split dans l'ancien format
                        parts = new_translation.split('|||')
                        modification_data = {
                            'type': 'split',
                            'content': {
                                'part1': parts[0] if len(parts) > 0 else '',
                                'part2': parts[1] if len(parts) > 1 else ''
                            },
                            'original_structure': {
                                'was_split': False,
                                'split_type': 'multiline'
                            }
                        }
                    else:
                        # C'était une modification simple
                        modification_data = {
                            'type': 'simple',
                            'content': new_translation,
                            'original_structure': {
                                'was_split': False,
                                'split_type': 'normal'
                            }
                        }
                    
                    converted_data[key] = {
                        'dialogue_info': dialogue_info,
                        'modification_data': modification_data,
                        'timestamp': timestamp,
                        'version': '2.0',
                        'converted_from_legacy': True
                    }
                    legacy_count += 1
                else:
                    # Format inconnu, ignorer
                    log_message("ATTENTION", f"Format de récupération inconnu pour {key}", category="realtime_editor")
                    continue
            
            # Charger les modifications converties dans le cache actuel
            self.pending_modifications = converted_data
            result['recovered_count'] = len(converted_data)
            result['legacy_converted'] = legacy_count
            result['success'] = True
            
            # Sauvegarder dans le fichier actuel avec le nouveau format
            if self.pending_modifications_file:
                with open(self.pending_modifications_file, 'w', encoding='utf-8') as f:
                    json.dump(self.pending_modifications, f, indent=2, ensure_ascii=False)
            
            log_message("INFO", f"Récupération: {result['recovered_count']} modifications rechargées ({legacy_count} converties)", category="realtime_editor")
            
        except Exception as e:
            result['errors'].append(f"Erreur chargement récupération: {e}")
            log_message("ERREUR", f"Erreur chargement récupération: {e}", category="realtime_editor")
        
        return result

    def _migrate_legacy_pending_file(self, file_path: str) -> bool:
        """
        Migre un fichier de modifications en attente de l'ancien format vers le nouveau
        """
        try:
            if not os.path.exists(file_path):
                return True
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not data:
                return True
            
            # Vérifier si c'est déjà le nouveau format
            first_entry = next(iter(data.values()), {})
            if 'version' in first_entry:
                return True  # Déjà au nouveau format
            
            # Migrer vers le nouveau format
            migrated_data = {}
            for key, mod_entry in data.items():
                if 'new_translation' in mod_entry:
                    dialogue_info = mod_entry.get('dialogue_info', {})
                    new_translation = mod_entry.get('new_translation', '')
                    timestamp = mod_entry.get('timestamp', time.time())
                    
                    # Déterminer le type selon le contenu
                    if '|||' in new_translation:
                        parts = new_translation.split('|||')
                        modification_data = {
                            'type': 'split',
                            'content': {
                                'part1': parts[0],
                                'part2': parts[1] if len(parts) > 1 else ''
                            },
                            'original_structure': {'was_split': False, 'split_type': 'multiline'}
                        }
                    else:
                        modification_data = {
                            'type': 'simple',
                            'content': new_translation,
                            'original_structure': {'was_split': False, 'split_type': 'normal'}
                        }
                    
                    migrated_data[key] = {
                        'dialogue_info': dialogue_info,
                        'modification_data': modification_data,
                        'timestamp': timestamp,
                        'version': '2.0',
                        'migrated_from_legacy': True
                    }
            
            # Sauvegarder le format migré
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(migrated_data, f, indent=2, ensure_ascii=False)
            
            log_message("INFO", f"Migration réussie: {len(migrated_data)} modifications migrées", category="realtime_editor")
            return True
            
        except Exception as e:
            log_message("ERREUR", f"Erreur migration fichier legacy: {e}", category="realtime_editor")
            return False

    def check_recovery_available(self, project_path: str) -> Dict[str, Any]:
        """Vérifie si un fichier de récupération est disponible"""
        result = {'available': False, 'count': 0, 'recovery_file': None}
        
        try:
            recovery_file = os.path.join(project_path, "renextract_pending_modifications_recovery.json")
            
            if os.path.exists(recovery_file):
                with open(recovery_file, 'r', encoding='utf-8') as f:
                    recovery_data = json.load(f)
                
                result['available'] = True
                result['count'] = len(recovery_data)
                result['recovery_file'] = recovery_file
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur vérification récupération: {e}", category="realtime_editor")
        
        return result

    def add_pending_modification(self, dialogue_info: Dict, modification_data: Dict) -> bool:
        """
        Ajoute une modification au cache JSON avec structure complète
        
        Args:
            dialogue_info: Informations du dialogue
            modification_data: Dict contenant:
                - type: 'simple', 'split', 'speaker_dialogue', 'merge'
                - content: Le contenu selon le type
                - original_structure: Structure originale détectée
        """
        try:
            key = f"{dialogue_info['tl_file']}|{dialogue_info['tl_line']}"
            
            self.pending_modifications[key] = {
                'dialogue_info': dialogue_info,
                'modification_data': modification_data,
                'timestamp': time.time(),
                'version': '2.0'  # Version pour la compatibilité
            }
            
            # Sauvegarder dans le fichier
            if self.pending_modifications_file:
                with open(self.pending_modifications_file, 'w', encoding='utf-8') as f:
                    json.dump(self.pending_modifications, f, indent=2, ensure_ascii=False)
            
            log_message("DEBUG", f"Modification en attente ajoutée: {key} (type: {modification_data['type']})", category="realtime_editor")
            return True
            
        except Exception as e:
            log_message("ERREUR", f"Erreur ajout modification en attente: {e}", category="realtime_editor")
            return False

    def get_pending_count(self) -> int:
        """Retourne le nombre de modifications en attente"""
        return len(self.pending_modifications)

    def has_pending_modifications(self) -> bool:
        """Vérifie s'il y a des modifications en attente"""
        return len(self.pending_modifications) > 0

    def generate_monitoring_module(self, project_path: str, language: str, manual_version: Optional[str] = None) -> Dict[str, Any]:
        """
        Génère et installe le module de surveillance dans le projet
        
        Args:
            project_path: Chemin vers le projet Ren'Py
            language: Langue cible (ex: "french")
            manual_version: Version Ren'Py manuelle au format "8.2.1" (optionnel)
            
        Returns:
            Dict avec les résultats de l'opération
        """
        result = {'success': False, 'module_path': None, 'module_version': None, 'renpy_version_detected': None, 'errors': [], 'warnings': []}
        
        try:
            if not os.path.exists(project_path):
                result['errors'].append("Projet non trouvé")
                return result
            
            game_dir = os.path.join(project_path, "game")
            if not os.path.exists(game_dir):
                result['errors'].append("Dossier 'game' non trouvé")
                return result
            
            module_path = os.path.join(game_dir, "renextract_realtime_monitor.rpy")
            
            # Sélectionner la version du module
            selected_module = self._select_module_version(project_path, manual_version)
            
            # Si la version est None, c'est une version inconnue
            if selected_module is None:
                detected_version = self._get_renpy_version_from_project(project_path)
                result['renpy_version_detected'] = detected_version
                result['warnings'].append(f"Version Ren'Py {detected_version} inconnue, utilisation du module v1 par défaut")
                selected_module = "v1"
            
            result['module_version'] = selected_module
            log_message("INFO", f"Module {selected_module} sélectionné pour le projet", category="realtime_editor")
            
            # Générer le contenu du module
            module_content = self._generate_module_content(language, selected_module)
            
            # Sauvegarder le fichier existant si présent
            if os.path.exists(module_path):
                backup_result = self.backup_manager.create_backup(
                    module_path,
                    BackupType.SECURITY,
                    "Sauvegarde avant mise à jour du module de surveillance"
                )
                if backup_result['success']:
                    log_message("DEBUG", f"Backup module existant créé", category="realtime_editor")
            
            # Écrire le nouveau module
            with open(module_path, 'w', encoding='utf-8') as f:
                f.write(module_content)
            
            result['success'] = True
            result['module_path'] = module_path
            
            log_message("INFO", f"Module de surveillance créé: {os.path.basename(module_path)}", category="realtime_editor")
            
        except Exception as e:
            result['errors'].append(f"Erreur génération module: {e}")
            log_message("ERREUR", f"Erreur génération module surveillance: {e}", category="realtime_editor")
        
        return result

    def _get_renpy_version_from_project(self, project_path: str) -> Optional[tuple]:
        """
        Détecte la version Ren'Py du projet directement (sans dépendre de l'extraction RPA)
        
        Returns:
            Tuple (major, minor, patch) ou None si non détecté
        """
        try:
            game_dir = os.path.join(project_path, "game")
            
            # PRIORITÉ 1 : Analyser script_version.txt
            script_version_path = os.path.join(game_dir, "script_version.txt")
            
            if os.path.exists(script_version_path):
                try:
                    with open(script_version_path, 'r', encoding='utf-8') as f:
                        version_content = f.read().strip()
                    
                    log_message("DEBUG", f"Contenu script_version.txt: {version_content}", category="realtime_editor")
                    
                    # Parsing robuste - Extraire tous les nombres du contenu
                    import re
                    numbers = re.findall(r'\d+', version_content)
                    
                    if numbers and len(numbers) >= 1:
                        major_version = int(numbers[0])
                        
                        if len(numbers) >= 3:
                            version_tuple = (int(numbers[0]), int(numbers[1]), int(numbers[2]))
                        elif len(numbers) >= 2:
                            version_tuple = (int(numbers[0]), int(numbers[1]), 0)
                        else:
                            version_tuple = (int(numbers[0]), 0, 0)
                        
                        log_message("INFO", f"Version Ren'Py détectée: {version_tuple}", category="realtime_editor")
                        return version_tuple
                        
                except Exception as e:
                    log_message("ATTENTION", f"Erreur lecture script_version.txt: {e}", category="realtime_editor")
            
            # PRIORITÉ 2 : Analyser les fichiers .rpyc
            rpyc_files = []
            for root, dirs, files in os.walk(game_dir):
                for file in files:
                    if file.endswith('.rpyc'):
                        rpyc_files.append(os.path.join(root, file))
                        if len(rpyc_files) >= 3:  # Limiter pour éviter de lire trop de fichiers
                            break
                if len(rpyc_files) >= 3:
                    break
            
            if rpyc_files:
                try:
                    # Lire le premier fichier .rpyc pour détecter la version
                    with open(rpyc_files[0], 'rb') as f:
                        header = f.read(16)
                        
                    # Ren'Py 8 commence par b'RENPY RPC2'
                    if header.startswith(b'RENPY RPC2'):
                        log_message("INFO", "Version Ren'Py détectée via .rpyc: 8.x.x", category="realtime_editor")
                        return (8, 0, 0)
                    # Ren'Py 7 commence par b'RENPY RPC'
                    elif header.startswith(b'RENPY RPC'):
                        log_message("INFO", "Version Ren'Py détectée via .rpyc: 7.x.x", category="realtime_editor")
                        return (7, 0, 0)
                        
                except Exception as e:
                    log_message("ATTENTION", f"Erreur lecture .rpyc: {e}", category="realtime_editor")
            
            log_message("ATTENTION", "Aucune version Ren'Py détectée", category="realtime_editor")
            return None
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur détection version Ren'Py: {e}", category="realtime_editor")
            return None
    
    def _select_module_version(self, project_path: str, manual_override: Optional[str] = None) -> str:
        """
        Sélectionne la version du module à utiliser
        
        Args:
            project_path: Chemin vers le projet
            manual_override: Version manuelle au format "8.2.1" (optionnel)
            
        Returns:
            Nom de la version du module ("v1", "v2", etc.)
        """
        # 1. Si override manuel fourni, l'utiliser
        if manual_override:
            try:
                import re
                numbers = re.findall(r'\d+', manual_override)
                if len(numbers) >= 3:
                    version_tuple = (int(numbers[0]), int(numbers[1]), int(numbers[2]))
                elif len(numbers) >= 2:
                    version_tuple = (int(numbers[0]), int(numbers[1]), 0)
                else:
                    version_tuple = (int(numbers[0]), 0, 0)
                
                if version_tuple in self.MODULE_COMPATIBILITY:
                    log_message("INFO", f"Version manuelle {manual_override} → module {self.MODULE_COMPATIBILITY[version_tuple]}", category="realtime_editor")
                    return self.MODULE_COMPATIBILITY[version_tuple]
                else:
                    log_message("ATTENTION", f"Version manuelle {manual_override} inconnue, utilisation de v1 par défaut", category="realtime_editor")
                    return "v1"
            except Exception as e:
                log_message("ATTENTION", f"Erreur parsing version manuelle: {e}, utilisation de v1", category="realtime_editor")
                return "v1"
        
        # 2. Détection automatique
        detected_version = self._get_renpy_version_from_project(project_path)
        
        if detected_version:
            if detected_version in self.MODULE_COMPATIBILITY:
                module_version = self.MODULE_COMPATIBILITY[detected_version]
                log_message("INFO", f"Version Ren'Py {detected_version} détectée → module {module_version}", category="realtime_editor")
                return module_version
            else:
                log_message("ATTENTION", f"Version Ren'Py {detected_version} inconnue, utilisation de v1 par défaut", category="realtime_editor")
                # Retourner None pour signaler une version inconnue (pour le feedback utilisateur)
                return None
        
        # 3. Fallback par défaut
        log_message("INFO", "Version Ren'Py non détectée, utilisation de v1 par défaut", category="realtime_editor")
        return "v1"
    
    def _load_module_template(self, module_version: str) -> str:
        """
        Charge le template du module depuis le fichier correspondant
        
        Args:
            module_version: Version du module ("v1", "v2", etc.)
            
        Returns:
            Contenu du template
        """
        try:
            # Chemin vers le module
            module_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "renpy_modules",
                f"{module_version}.rpy"
            )
            
            if not os.path.exists(module_path):
                log_message("ERREUR", f"Module {module_version} introuvable: {module_path}", category="realtime_editor")
                # Fallback vers v1
                module_path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "renpy_modules",
                    "v1.rpy"
                )
            
            with open(module_path, 'r', encoding='utf-8') as f:
                template = f.read()
            
            log_message("INFO", f"Module {module_version} chargé depuis {module_path}", category="realtime_editor")
            return template
            
        except Exception as e:
            log_message("ERREUR", f"Erreur chargement module {module_version}: {e}", category="realtime_editor")
            raise
    
    def _generate_module_content(self, language: str, module_version: str = "v1") -> str:
        """Génère le contenu complet du module de surveillance avec la logique de menu SIMPLIFIÉE."""
        # Charger le template
        template = self._load_module_template(module_version)
        
        # Remplacer uniquement le placeholder {language} pour éviter les conflits
        # avec les chaînes .format présentes dans le template.
        return template.replace("{language}", language)

    def start_monitoring(self, project_path: str, language: str) -> Dict[str, Any]:
        """
        Démarre la surveillance des dialogues - VERSION CORRIGÉE AVEC CACHE ET SANS ERREUR
        """
        result = {'success': False, 'errors': []}
        
        try:
            if self.monitoring_active:
                result['errors'].append("Surveillance déjà active")
                return result
            
            self._init_pending_modifications_file(project_path)
            self.current_project_path = project_path
            self.current_language = language
            
            log_file_path = os.path.join(project_path, "renextract_dialogue_log.txt")
            
            # ✅ Toujours remettre à zéro le fichier log au démarrage pour une session propre
            try:
                with open(log_file_path, 'w', encoding='utf-8') as f:
                    f.write("")
                log_message("INFO", "Fichier log remis à zéro pour nouvelle session.", "realtime_editor")
            except Exception as e:
                log_message("ERREUR", f"Impossible de créer/vider le fichier log : {e}", "realtime_editor")
                result['errors'].append("Impossible de créer/vider le fichier log.")
                return result

            # Toujours reprendre à zéro pour une détection propre
            # Cela évite les problèmes de synchronisation avec d'anciens logs
            self.last_dialogue_line = 0
            log_message("INFO", "Surveillance démarrée - lecture depuis le début du fichier log", category="realtime_editor")

            self.monitoring_active = True

            # On lance la création du cache dans un thread séparé
            self.string_translation_cache = None
            cache_thread = threading.Thread(target=self._build_string_translation_cache, daemon=True)
            cache_thread.start()
            
            # --- LA PARTIE CORRIGÉE ---
            
            # Le worker pour la surveillance des dialogues
            def monitor_worker():
                log_message("DEBUG", "Thread de surveillance démarré", category="realtime_editor")
                while self.monitoring_active:
                    try:
                        self._check_for_dialogues(log_file_path)
                        time.sleep(0.2)
                    except Exception as e:
                        log_message("ERREUR", f"Erreur dans le thread de surveillance: {e}", category="realtime_editor")
                        break
                log_message("DEBUG", "Thread de surveillance arrêté", category="realtime_editor")
            
            # LA LIGNE MANQUANTE : On doit créer l'attribut .monitoring_thread ici
            self.monitoring_thread = threading.Thread(target=monitor_worker, daemon=True)
            self.monitoring_thread.start()
            
            # --- FIN DE LA CORRECTION ---
            
            result['success'] = True
            self._update_status("Surveillance démarrée, création du cache en cours...")
            
            log_message("INFO", "Surveillance des dialogues démarrée", category="realtime_editor")
            
        except Exception as e:
            result['errors'].append(f"Erreur démarrage surveillance: {e}")
            log_message("ERREUR", f"Erreur critique démarrage surveillance: {e}", category="realtime_editor")
        
        return result
    
    def stop_monitoring(self) -> Dict[str, Any]:
        """Arrête la surveillance des dialogues et nettoie les fichiers temporaires"""
        result = {'success': False, 'errors': [], 'cleaned_files': []}
        
        try:
            self.monitoring_active = False
            
            # Attendre que le thread se termine
            if hasattr(self, 'monitoring_thread') and self.monitoring_thread.is_alive():
                self.monitoring_thread.join(timeout=2.0)
            
            # Nettoyer les fichiers temporaires
            self._cleanup_temporary_files(result)
            
            result['success'] = True
            self._update_status("Surveillance arrêtée")
            
            log_message("INFO", "Surveillance des dialogues arrêtée", category="realtime_editor")
            
        except Exception as e:
            result['errors'].append(f"Erreur arrêt surveillance: {e}")
            log_message("ERREUR", f"Erreur arrêt surveillance: {e}", category="realtime_editor")
        
        return result

    def _cleanup_temporary_files(self, result: Dict[str, Any]):
        """
        Nettoie les fichiers temporaires lors de l'arrêt de la surveillance
        - Supprime le fichier JSON s'il est vide
        - Supprime le fichier de log
        """
        try:
            # 1. Nettoyer le fichier JSON des modifications en attente
            if self.pending_modifications_file and os.path.exists(self.pending_modifications_file):
                try:
                    # Vérifier si le fichier est vide ou ne contient que {}
                    with open(self.pending_modifications_file, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                    
                    if not content or content == '{}':
                        os.remove(self.pending_modifications_file)
                        result['cleaned_files'].append(os.path.basename(self.pending_modifications_file))
                        log_message("INFO", f"Fichier JSON vide supprimé: {os.path.basename(self.pending_modifications_file)}", category="realtime_editor")
                    else:
                        log_message("DEBUG", f"Fichier JSON conservé (contient des modifications): {os.path.basename(self.pending_modifications_file)}", category="realtime_editor")
                        
                except Exception as e:
                    log_message("ATTENTION", f"Erreur nettoyage fichier JSON: {e}", category="realtime_editor")
            
            # 2. Nettoyer le fichier de log
            if self.current_project_path:
                log_file_path = os.path.join(self.current_project_path, "renextract_dialogue_log.txt")
                if os.path.exists(log_file_path):
                    try:
                        os.remove(log_file_path)
                        result['cleaned_files'].append(os.path.basename(log_file_path))
                        log_message("INFO", f"Fichier de log supprimé: {os.path.basename(log_file_path)}", category="realtime_editor")
                    except Exception as e:
                        log_message("ATTENTION", f"Erreur suppression fichier de log: {e}", category="realtime_editor")
            
            # 3. Réinitialiser les variables
            self.pending_modifications = {}
            self.last_dialogue_line = 0
            
            if result['cleaned_files']:
                log_message("INFO", f"Nettoyage terminé: {len(result['cleaned_files'])} fichier(s) supprimé(s)", category="realtime_editor")
            
        except Exception as e:
            result['errors'].append(f"Erreur nettoyage fichiers temporaires: {e}")
            log_message("ERREUR", f"Erreur nettoyage fichiers temporaires: {e}", category="realtime_editor")

    def save_all_pending_modifications(self, project_path: str = None) -> Dict[str, Any]:
        """
        Sauvegarde toutes les modifications en attente avec gestion des différents types
        """
        result = {'success': False, 'saved_count': 0, 'errors': [], 'details': []}
        
        try:
            if not self.pending_modifications:
                result['success'] = True
                return result
            
            base_project = project_path or self.current_project_path
            saved_count = 0
            
            # Itérer sur une copie pour pouvoir supprimer des éléments
            for key, mod_entry in list(self.pending_modifications.items()):
                try:
                    dialogue_info = mod_entry['dialogue_info']
                    modification_data = mod_entry['modification_data']
                    mod_type = modification_data['type']
                    
                    # Dispatcher selon le type de modification
                    if mod_type == 'simple':
                        save_result = self.save_translation(
                            dialogue_info, 
                            modification_data['content'], 
                            base_project
                        )
                    elif mod_type == 'split':
                        save_result = self.save_split_translation(
                            dialogue_info,
                            modification_data['content']['part1'],
                            modification_data['content']['part2'],
                            base_project
                        )
                    elif mod_type == 'speaker_dialogue':
                        save_result = self.save_speaker_dialogue_translation(
                            dialogue_info,
                            modification_data['content']['speaker'],
                            modification_data['content']['dialogue'],
                            base_project
                        )
                    elif mod_type == 'merge':
                        save_result = self.save_merge_translation(
                            dialogue_info,
                            modification_data['content'],
                            base_project
                        )
                    else:
                        content = modification_data.get('content', '')
                        if isinstance(content, dict):
                            content = str(content)
                        save_result = self.save_translation(dialogue_info, content, base_project)
                    
                    if save_result['success']:
                        saved_count += 1
                        result['details'].append({
                            'key': key,
                            'type': mod_type,
                            'status': 'success'
                        })
                        # Supprimer la modification du cache
                        if key in self.pending_modifications:
                            del self.pending_modifications[key]
                    else:
                        result['errors'].extend([f"{key}: {err}" for err in save_result['errors']])
                        result['details'].append({
                            'key': key,
                            'type': mod_type,
                            'status': 'failed',
                            'errors': save_result['errors']
                        })
                        
                except Exception as e:
                    error_msg = f"Erreur sauvegarde {key}: {e}"
                    result['errors'].append(error_msg)
                    result['details'].append({
                        'key': key,
                        'status': 'error',
                        'error': str(e)
                    })
                    log_message("ERREUR", error_msg, category="realtime_editor")
            
            # Réécrire le fichier JSON avec les modifications restantes (celles qui ont échoué)
            # Si toutes les modifications ont été sauvegardées avec succès, vider complètement le fichier
            if self.pending_modifications_file:
                if len(self.pending_modifications) == 0:
                    # Toutes les modifications ont été sauvegardées avec succès, vider le fichier
                    with open(self.pending_modifications_file, 'w', encoding='utf-8') as f:
                        f.write('{}')  # Fichier JSON vide
                    log_message("INFO", "Fichier de modifications en attente vidé après sauvegarde complète", category="realtime_editor")
                else:
                    # Il reste des modifications qui ont échoué, les garder dans le fichier
                    with open(self.pending_modifications_file, 'w', encoding='utf-8') as f:
                        json.dump(self.pending_modifications, f, indent=2, ensure_ascii=False)
            
            result['success'] = True
            result['saved_count'] = saved_count
            
            log_message("INFO", f"Sauvegarde en lot: {saved_count} modifications, {len(result['errors'])} erreurs", category="realtime_editor")
            
        except Exception as e:
            result['errors'].append(f"Erreur générale sauvegarde en lot: {e}")
            log_message("ERREUR", f"Erreur générale sauvegarde en lot: {e}", category="realtime_editor")
        
        return result

    def _check_for_dialogues(self, log_file_path: str):
        """Version finale qui gère le nouveau format de log pour les menus."""
        try:
            if not os.path.exists(log_file_path): return
            
            with open(log_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if len(lines) <= self.last_dialogue_line: return
            
            in_menu, menu_choices, current_line_index = False, [], self.last_dialogue_line
            
            while current_line_index < len(lines):
                line = lines[current_line_index].strip()
                if not line:
                    current_line_index += 1
                    continue
                
                if line == "MENU_START":
                    in_menu, menu_choices = True, []
                elif line == "MENU_END" and in_menu:
                    in_menu = False
                    if menu_choices:
                        self._notify_dialogue({
                            'is_menu': True, 'choices': menu_choices,
                            'choice_count': len(menu_choices),
                            'grid_rows': (len(menu_choices) + 1) // 2, 'grid_cols': 2
                        })
                    menu_choices = []
                # Dans la section menu de _check_for_dialogues
                elif in_menu and line.startswith("CHOICE|"):
                    original_text = line[7:]
                    
                    # Recherche de la traduction
                    translation_info = self._find_string_translation_in_project(original_text)
                    
                    choice_info = {
                        'original_text': original_text,
                        'translated_text': translation_info['translated_text'],
                        'tl_file': translation_info['tl_file'],
                        'tl_line': translation_info['tl_line']
                    }
                    menu_choices.append(choice_info)
                    # <-- FIN DE LA MODIFICATION -->
                elif not in_menu and '|' in line:
                    dialogue_info = self._parse_dialogue_line(line)
                    if dialogue_info:
                        dialogue_info['original_text'] = self._get_original_text(dialogue_info)
                        dialogue_info['is_menu'] = False
                        multiple_group = self._check_for_multiple_dialogues(dialogue_info)
                        if multiple_group['is_multiple']:
                            multiple_group['is_menu'] = False
                            self._notify_dialogue(multiple_group)
                        else:
                            self._notify_dialogue(dialogue_info)
                
                current_line_index += 1
            
            self.last_dialogue_line = len(lines)
                            
        except Exception as e:
            log_message("ERREUR", f"Erreur vérification dialogues: {e}", category="realtime_editor")

    def get_pending_modifications_summary(self) -> Dict[str, Any]:
        """
        Retourne un résumé détaillé des modifications en attente
        """
        summary = {
            'total_count': len(self.pending_modifications),
            'by_type': {},
            'by_file': {},
            'modifications': []
        }
        
        try:
            for key, mod_entry in self.pending_modifications.items():
                mod_data = mod_entry['modification_data']
                mod_type = mod_data['type']
                dialogue_info = mod_entry['dialogue_info']
                
                # Compter par type
                summary['by_type'][mod_type] = summary['by_type'].get(mod_type, 0) + 1
                
                # Compter par fichier
                file_name = os.path.basename(dialogue_info['tl_file'])
                summary['by_file'][file_name] = summary['by_file'].get(file_name, 0) + 1
                
                # Ajouter les détails
                summary['modifications'].append({
                    'key': key,
                    'type': mod_type,
                    'file': file_name,
                    'line': dialogue_info['tl_line'],
                    'timestamp': mod_entry['timestamp']
                })
        
        except Exception as e:
            log_message("ERREUR", f"Erreur génération résumé modifications: {e}", category="realtime_editor")
        
        return summary

    def clear_all_pending_modifications(self) -> bool:
        """
        Vide complètement toutes les modifications en attente et le fichier associé
        
        Returns:
            bool: True si l'opération a réussi, False sinon
        """
        try:
            # Vider le cache en mémoire
            self.pending_modifications = {}
            
            # Vider le fichier JSON
            if self.pending_modifications_file:
                with open(self.pending_modifications_file, 'w', encoding='utf-8') as f:
                    f.write('{}')  # Fichier JSON vide
                log_message("INFO", "Toutes les modifications en attente ont été vidées", category="realtime_editor")
            
            return True
            
        except Exception as e:
            log_message("ERREUR", f"Erreur lors du vidage des modifications en attente: {e}", category="realtime_editor")
            return False

    def _parse_dialogue_line(self, line: str) -> Optional[Dict]:
        """Parse une ligne du log de dialogue et récupère les textes VO/VF"""
        try:
            # Format: texte_affiché|fichier|ligne|fichier_tl|ligne_tl
            parts = line.split('|')
            if len(parts) == 5:
                displayed_text = parts[0]  # Texte affiché (traduit)
                source_file = parts[1]
                source_line = int(parts[2])
                tl_file = parts[3]
                tl_line = int(parts[4])
                
                # 🔧 RÉCUPÉRER LE VRAI TEXTE ORIGINAL depuis le fichier de traduction
                original_text, translated_text = self._get_vo_vf_texts(tl_file, tl_line, displayed_text)
                
                return {
                    'displayed_text': displayed_text,
                    'original_text': original_text,
                    'translated_text': translated_text,
                    'source_file': source_file,
                    'source_line': source_line,
                    'tl_file': tl_file,
                    'tl_line': tl_line
                }
        except Exception as e:
            log_message("ATTENTION", f"Erreur parsing ligne dialogue: {e}", category="realtime_editor")
        
        return None

    def _get_vo_vf_texts(self, tl_file: str, tl_line: int, displayed_text: str) -> tuple:
        """
        Récupère le texte original (VO) et traduit (VF) depuis le fichier de traduction
        en scannant autour de la ligne ciblée
        """
        try:
            if not self.current_project_path or not tl_file:
                return displayed_text, displayed_text
            
            # Construire le chemin du fichier de traduction
            tl_file_path = os.path.join(self.current_project_path, tl_file)
            if not os.path.exists(tl_file_path):
                tl_file_path = os.path.join(self.current_project_path, "game", tl_file)
                if not os.path.exists(tl_file_path):
                    return displayed_text, displayed_text
            
            with open(tl_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            target_index = tl_line - 1
            if target_index < 0 or target_index >= len(lines):
                return displayed_text, displayed_text
            
            # Analyser la ligne ciblée et son contexte
            current_line = lines[target_index].strip()
            
            # Cas 1: Ligne "new" - chercher la ligne "old" précédente
            if 'new ' in current_line:
                new_text = self._extract_text_from_line(current_line)
                
                # Chercher la ligne "old" correspondante (généralement juste au-dessus)
                for i in range(target_index - 1, max(0, target_index - 5), -1):
                    prev_line = lines[i].strip()
                    if 'old ' in prev_line:
                        old_text = self._extract_text_from_line(prev_line)
                        return old_text, new_text
                
                # Si pas de ligne "old" trouvée, utiliser le texte affiché
                return displayed_text, new_text
            
            # Cas 2: Ligne "old" - chercher la ligne "new" suivante
            elif 'old ' in current_line:
                old_text = self._extract_text_from_line(current_line)
                
                # Chercher la ligne "new" correspondante (généralement juste en dessous)
                for i in range(target_index + 1, min(len(lines), target_index + 5)):
                    next_line = lines[i].strip()
                    if 'new ' in next_line:
                        new_text = self._extract_text_from_line(next_line)
                        return old_text, new_text
                
                # Si pas de ligne "new" trouvée, utiliser le texte original
                return old_text, old_text
            
            # Cas 3: Ligne de dialogue direct (sans old/new)
            else:
                dialogue_text = self._extract_text_from_line(current_line)
                
                # Chercher un commentaire avec le texte original dans les lignes précédentes
                for i in range(target_index - 1, max(0, target_index - 8), -1):
                    prev_line = lines[i].strip()
                    if prev_line.startswith('#') and not prev_line.startswith('# game/'):
                        # Extraire le texte du commentaire (texte original)
                        comment_text = self._extract_text_from_comment(prev_line)
                        if comment_text and len(comment_text) > 5:  # Filtrer les commentaires trop courts
                            return comment_text, dialogue_text
                
                # Fallback: utiliser le texte affiché comme original
                return displayed_text, dialogue_text
            
        except Exception as e:
            log_message("ERREUR", f"Erreur récupération VO/VF: {e}", category="realtime_editor")
            return displayed_text, displayed_text

    def _extract_text_from_line(self, line: str) -> str:
        """Extrait le texte entre guillemets d'une ligne"""
        try:
            import re
            # Chercher le texte entre guillemets
            quote_match = re.search(r'"((?:\\.|[^"])*)"', line)
            if quote_match:
                return quote_match.group(1)
            return ""
        except Exception:
            return ""

    def _extract_text_from_comment(self, comment_line: str) -> str:
        """Extrait le texte d'un commentaire (ligne #)"""
        try:
            import re
            # Supprimer le # et espaces de début
            content = comment_line.lstrip('#').strip()
            
            # Supprimer le préfixe de locuteur s'il existe (ex: "p " -> "")
            content = re.sub(r'^\w+\s+', '', content)
            
            # Extraire le texte entre guillemets
            quote_matches = re.findall(r'"((?:\\.|[^"\\])*)"', content)
            
            if quote_matches:
                if len(quote_matches) == 1:
                    return quote_matches[0]
                elif len(quote_matches) == 2:
                    # Cas locuteur non défini : "locuteur" "dialogue"
                    return f'"{quote_matches[0]}" "{quote_matches[1]}"'
                else:
                    # Prendre le plus long segment
                    return max(quote_matches, key=len)
            
            # Si pas de guillemets, retourner le contenu brut (filtré)
            if content and len(content) > 3:
                return content
            
            return ""
        except Exception:
            return ""
    
    def get_previous_dialogue(self, dialogue_info: Dict) -> Optional[Dict[str, str]]:
        """
        Récupère le dialogue précédent dans le fichier de traduction
        pour fournir un contexte conversationnel
        
        Args:
            dialogue_info: Infos du dialogue actuel
            
        Returns:
            Dict avec 'speaker' et 'text' du dialogue précédent, ou None
        """
        try:
            if not self.current_project_path or not dialogue_info.get('tl_file'):
                return None
            
            tl_file_path = os.path.join(self.current_project_path, dialogue_info['tl_file'])
            if not os.path.exists(tl_file_path):
                tl_file_path = os.path.join(self.current_project_path, "game", dialogue_info['tl_file'])
                if not os.path.exists(tl_file_path):
                    return None
            
            with open(tl_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            target_line = dialogue_info.get('tl_line', 0) - 1
            if target_line < 0 or target_line >= len(lines):
                return None
            
            # Chercher le bloc translate précédent
            for i in range(target_line - 1, max(0, target_line - 50), -1):
                line = lines[i].strip()
                
                # Ignorer les lignes vides et commentaires
                if not line or line.startswith('#'):
                    continue
                
                # Si on trouve un nouveau bloc translate, on arrête
                if line.startswith('translate '):
                    # Le dialogue précédent devrait être juste après
                    for j in range(i + 1, min(len(lines), i + 20)):
                        dialogue_line = lines[j].strip()
                        if not dialogue_line or dialogue_line.startswith('#') or dialogue_line.startswith('translate '):
                            continue
                        
                        # Extraire locuteur et texte
                        speaker = self._extract_speaker_from_line(dialogue_line)
                        text = self._extract_text_from_line(dialogue_line)
                        
                        if text:
                            return {
                                'speaker': speaker or '',
                                'text': text
                            }
                    break
                
                # Sinon, essayer d'extraire directement
                speaker = self._extract_speaker_from_line(line)
                text = self._extract_text_from_line(line)
                
                if text and len(text) > 3:  # Texte valide trouvé
                    return {
                        'speaker': speaker or '',
                        'text': text
                    }
            
            return None
            
        except Exception as e:
            log_message("ERREUR", f"Erreur récupération dialogue précédent: {e}", category="realtime_editor")
            return None
    
    def _get_original_text(self, dialogue_info: Dict) -> str:
        """
        Récupère le texte original - Version simplifiée utilisant les données déjà parsées
        """
        try:
            # Si on a déjà le texte original parsé, l'utiliser
            original_text = dialogue_info.get('original_text', '')
            if original_text and original_text != dialogue_info.get('displayed_text', ''):
                return original_text
            
            # Sinon, fallback sur l'ancienne méthode
            displayed_text = dialogue_info.get('displayed_text', '')
            return displayed_text
            
        except Exception as e:
            log_message("ERREUR", f"Erreur récupération texte original: {e}", category="realtime_editor")
            return dialogue_info.get('displayed_text', 'Erreur récupération')
    
    def save_translation(self, dialogue_info: Dict, new_translation: str, project_path: str = None) -> Dict[str, Any]:
        """
        Sauvegarde une traduction modifiée (compatible blocs strings old/new ET blocs translate dialogue).
        - Crée un backup de type REALTIME_EDIT avant écriture.
        - Remplace uniquement le premier texte entre guillemets sur la ligne ciblée.
        - Vide le fichier log pour forcer la recapture des nouveaux dialogues.
        """
        result: Dict[str, Any] = {'success': False, 'errors': [], 'backup_created': False}

        try:
            # 1) Résoudre le chemin du fichier cible
            base_project = project_path or self.current_project_path
            if not base_project:
                result['errors'].append("Projet non défini")
                return result

            tl_rel = dialogue_info.get('tl_file')
            tl_line_no = int(dialogue_info.get('tl_line', 0))
            if not tl_rel or tl_line_no <= 0:
                result['errors'].append("Informations dialogue incomplètes")
                return result

            # Normaliser le chemin
            candidates = []
            if os.path.isabs(tl_rel):
                candidates.append(tl_rel)
            else:
                candidates.append(os.path.join(base_project, tl_rel))
                candidates.append(os.path.join(base_project, "game", tl_rel))

            tl_file_path = None
            for cand in candidates:
                if os.path.exists(cand):
                    tl_file_path = cand
                    break

            if not tl_file_path:
                result['errors'].append("Fichier de traduction non trouvé")
                return result

            # 2) Créer un backup REALTIME_EDIT
            backup_result = self.backup_manager.create_backup(
                tl_file_path,
                BackupType.REALTIME_EDIT,
                "Sauvegarde avant modification temps réel"
            )
            if backup_result.get('success'):
                result['backup_created'] = True
                log_message("DEBUG", "Backup créé pour édition temps réel", category="realtime_editor")
            else:
                log_message("ATTENTION", f"Échec backup: {backup_result.get('error')}", category="realtime_editor")

            # 3) Charger le fichier
            with open(tl_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            target_index = tl_line_no - 1  # index 0-based
            if target_index < 0 or target_index >= len(lines):
                result['errors'].append("Ligne de traduction hors limites")
                return result

            line = lines[target_index]

            def _replace_first_quoted_text(s: str, replacement: str) -> str | None:
                """Remplace le segment entre guillemets approprié par replacement avec échappement correct."""
                
                # Échapper correctement le remplacement
                escaped_replacement = self._escape_quotes_properly(replacement)
                
                # Triples guillemets en priorité
                matches_triple = list(re.finditer(r'\"\"\"(.*?)\"\"\"', s))
                if matches_triple:
                    # Prendre le dernier match pour les triples guillemets
                    last_match = matches_triple[-1]
                    start, end = last_match.span(1)
                    return s[:start] + escaped_replacement.replace('\"\"\"', '\\\"\\\"\\\"') + s[end:]
                
                # Simples guillemets - chercher tous les matches
                matches_simple = list(re.finditer(r'\"((?:\\.|[^\"])*)\"', s))
                if matches_simple:
                    if len(matches_simple) == 1:
                        # Un seul segment, le remplacer
                        match = matches_simple[0]
                        start, end = match.span(1)
                        return s[:start] + escaped_replacement + s[end:]
                    else:
                        # Plusieurs segments - prendre le dernier (le dialogue)
                        last_match = matches_simple[-1]
                        start, end = last_match.span(1)
                        return s[:start] + escaped_replacement + s[end:]
                
                return None

            # 4) Choisir la stratégie selon le format
            # Cas A : bloc strings (ligne avec 'new ')
            if 'new ' in line:
                if '\"\"\"' in line:
                    # Remplacement entre triples guillemets après 'new'
                    def repl(m):
                        escaped_replacement = self._escape_quotes_properly(new_translation)
                        return m.group(1) + escaped_replacement.replace('\"\"\"', '\\\"\\\"\\\"') + m.group(3)
                    new_line = re.sub(r'(new\s+\"\"\")(.+?)(\"\"\"\s*)', repl, line, count=1, flags=re.DOTALL)
                else:
                    # Remplacement entre guillemets simples
                    escaped_replacement = self._escape_quotes_properly(new_translation)
                    new_line = re.sub(r'(new\s+\")((?:\\.|[^\"])*)(\"\s*)', r'\1' + escaped_replacement + r'\3', line, count=1)
                lines[target_index] = new_line
                modified_index = target_index
            else:
                # Cas B : bloc translate dialogue
                edit_index = target_index

                # Si la ligne cible est commentée (souvent la VO), avancer à la 1re ligne utile
                if line.strip().startswith('#'):
                    for j in range(target_index + 1, min(len(lines), target_index + 8)):
                        sj = lines[j].strip()
                        if sj and not sj.startswith('#') and ('"' in sj):
                            edit_index = j
                            break

                edit_line = lines[edit_index]
                replaced = _replace_first_quoted_text(edit_line, new_translation)
                
                if replaced is None:
                    result['errors'].append("Format de ligne non reconnu")
                    return result

                lines[edit_index] = replaced
                modified_index = edit_index

            # 5) Écrire le fichier
            with open(tl_file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            # 6) Vider le fichier log pour forcer la recapture des nouveaux dialogues
            log_file_path = os.path.join(base_project, "renextract_dialogue_log.txt")
            if os.path.exists(log_file_path):
                try:
                    with open(log_file_path, 'w', encoding='utf-8') as f:
                        f.write("")
                    # Réinitialiser le compteur de lignes pour le monitoring
                    self.last_dialogue_line = 0
                    log_message("DEBUG", "Fichier log vidé après sauvegarde pour forcer recapture", category="realtime_editor")
                except Exception as e:
                    log_message("ATTENTION", f"Erreur vidage fichier log: {e}", category="realtime_editor")
                    # Ne pas faire échouer la sauvegarde à cause de cela
            
            # ✅ Mettre à jour le cache de traductions avec la nouvelle valeur
            original_text = dialogue_info.get('original_text', '')
            if original_text and self.string_translation_cache is not None:
                rel_path = os.path.relpath(tl_file_path, base_project)
                self.string_translation_cache[original_text] = {
                    'translated_text': new_translation,
                    'tl_file': rel_path,
                    'tl_line': modified_index + 1
                }
                log_message("DEBUG", f"Cache mis à jour pour: {original_text[:50]}...", category="realtime_editor")
            
            result['success'] = True
            result['modified_file'] = tl_file_path
            result['modified_line'] = modified_index + 1
            log_message("INFO", f"Traduction sauvegardée: {os.path.basename(tl_file_path)}:{modified_index+1}", category="realtime_editor")
            return result

        except Exception as e:
            result['errors'].append(f"Erreur sauvegarde: {e}")
            log_message("ERREUR", f"Erreur sauvegarde traduction: {e}", category="realtime_editor")
            return result
    
    def get_translation_statistics(self, project_path: str) -> Dict[str, Any]:
        """Récupère les statistiques des traductions temps réel"""
        stats = {
            'total_backups': 0,
            'recent_modifications': [],
            'monitoring_status': 'stopped',
            'log_file_size': 0,
            'last_dialogue_time': None
        }
        
        try:
            # Statistiques des backups temps réel
            all_backups = self.backup_manager.list_all_backups(type_filter=BackupType.REALTIME_EDIT)
            stats['total_backups'] = len(all_backups)
            
            # Dernières modifications (5 plus récentes)
            recent_backups = sorted(all_backups, key=lambda x: x['created'], reverse=True)[:5]
            stats['recent_modifications'] = [
                {
                    'filename': backup['source_filename'],
                    'date': backup['created'],
                    'size': backup['size']
                }
                for backup in recent_backups
            ]
            
            # État du monitoring
            stats['monitoring_status'] = 'active' if self.monitoring_active else 'stopped'
            
            # Taille du fichier log
            log_file_path = os.path.join(project_path, "renextract_dialogue_log.txt")
            if os.path.exists(log_file_path):
                stats['log_file_size'] = os.path.getsize(log_file_path)
                
                # Dernière entrée du log
                try:
                    with open(log_file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    if lines:
                        stats['last_dialogue_time'] = os.path.getmtime(log_file_path)
                except Exception:
                    pass
            
        except Exception as e:
            log_message("ERREUR", f"Erreur statistiques édition temps réel: {e}", category="realtime_editor")
        
        return stats
    
    def cleanup_old_logs(self, project_path: str, days_old: int = 7) -> Dict[str, Any]:
        """Nettoie les anciens fichiers de log"""
        result = {'success': False, 'cleaned_files': [], 'errors': []}
        
        try:
            import time
            import glob
            
            current_time = time.time()
            cutoff_time = current_time - (days_old * 24 * 60 * 60)
            
            # Chercher les fichiers de log
            log_pattern = os.path.join(project_path, "*dialogue_log*.txt")
            log_files = glob.glob(log_pattern)
            
            for log_file in log_files:
                try:
                    file_time = os.path.getmtime(log_file)
                    if file_time < cutoff_time:
                        # Créer un backup avant suppression
                        backup_result = self.backup_manager.create_backup(
                            log_file,
                            BackupType.SECURITY,
                            f"Backup avant nettoyage log ancien ({days_old} jours)"
                        )
                        
                        if backup_result['success']:
                            os.remove(log_file)
                            result['cleaned_files'].append(os.path.basename(log_file))
                            log_message("INFO", f"Log ancien nettoyé: {os.path.basename(log_file)}", category="realtime_editor")
                        
                except Exception as e:
                    result['errors'].append(f"Erreur nettoyage {os.path.basename(log_file)}: {e}")
            
            result['success'] = True
            
        except Exception as e:
            result['errors'].append(f"Erreur nettoyage logs: {e}")
            log_message("ERREUR", f"Erreur nettoyage logs: {e}", category="realtime_editor")
        
        return result
    
    def validate_project_compatibility(self, project_path: str) -> Dict[str, Any]:
        """Valide la compatibilité d'un projet avec l'éditeur temps réel"""
        validation = {
            'compatible': False,
            'issues': [],
            'recommendations': [],
            'project_info': {}
        }
        
        try:
            # Vérifications de base
            game_dir = os.path.join(project_path, "game")
            if not os.path.exists(game_dir):
                validation['issues'].append("Dossier 'game' non trouvé")
                return validation
            
            # Chercher des fichiers .rpy
            rpy_files = []
            for root, dirs, files in os.walk(game_dir):
                for file in files:
                    if file.endswith('.rpy'):
                        rpy_files.append(os.path.join(root, file))
            
            validation['project_info']['rpy_count'] = len(rpy_files)
            
            if len(rpy_files) == 0:
                validation['issues'].append("Aucun fichier .rpy trouvé")
                return validation
            
            # Vérifier la présence de dossier tl
            tl_dir = os.path.join(game_dir, "tl")
            if os.path.exists(tl_dir):
                languages = [d for d in os.listdir(tl_dir) if os.path.isdir(os.path.join(tl_dir, d))]
                validation['project_info']['existing_languages'] = languages
                
                if not languages:
                    validation['recommendations'].append("Générez d'abord des traductions avec l'onglet Génération")
            else:
                validation['recommendations'].append("Créez d'abord des fichiers de traduction")
            
            # Vérifier les permissions d'écriture
            test_file = os.path.join(game_dir, "test_write_permissions.tmp")
            try:
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                validation['project_info']['write_permissions'] = True
            except Exception:
                validation['issues'].append("Permissions d'écriture insuffisantes")
                validation['project_info']['write_permissions'] = False
            
            # Si pas d'issues majeures, le projet est compatible
            if not validation['issues']:
                validation['compatible'] = True
            
        except Exception as e:
            validation['issues'].append(f"Erreur validation: {e}")
            log_message("ERREUR", f"Erreur validation projet: {e}", category="realtime_editor")
        
        return validation
    
    def cleanup(self):
        """Nettoie les ressources"""
        try:
            if self.monitoring_active:
                self.stop_monitoring()
            
            # NOUVEAU: Nettoyer le fichier JSON temporaire
            if self.pending_modifications_file and os.path.exists(self.pending_modifications_file):
                try:
                    os.remove(self.pending_modifications_file)
                    log_message("DEBUG", "Fichier JSON temporaire supprimé", category="realtime_editor")
                except Exception as e:
                    log_message("ATTENTION", f"Erreur suppression fichier JSON: {e}", category="realtime_editor")
            
            log_message("DEBUG", "RealTimeEditorBusiness nettoyé", category="realtime_editor")
        except Exception as e:
            log_message("ATTENTION", f"Erreur nettoyage RealTimeEditorBusiness: {e}", category="realtime_editor")