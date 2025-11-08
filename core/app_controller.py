# core/app_controller.py
# Application Controller - Refactored
# Created for RenExtract 

"""
Contrôleur principal de l'application - Logique métier séparée de l'interface
"""

import os
import time
from typing import Optional, Dict, Any

# Imports métier
from core.services.extraction.extraction import TextExtractor, get_file_base_name
from core.services.extraction.reconstruction import FileReconstructor
from core.services.extraction.validation import validate_before_reconstruction, fix_unescaped_quotes_in_txt
from core.models.backup.unified_backup_manager import UnifiedBackupManager, BackupType
from core.models.files.file_manager import file_manager, FileOpener

# Imports utilitaires
from infrastructure.config.config import config_manager
from infrastructure.logging.logging import log_message, get_logger
from infrastructure.config.constants import VERSION, FOLDERS, ensure_game_structure
from infrastructure.helpers.unified_functions import extract_game_name
from ui.themes import theme_manager

class AppController:
    """Contrôleur principal gérant la logique métier"""

    def __init__(self, main_window):
        self.main_window = main_window
        # Gestionnaire centralisé de projets
        from core.services.extraction.project_manager import ProjectManager
        self.project_manager = ProjectManager()

        # Enregistrer InfoFrame comme listener
        self.project_manager.register_listener(
            self._on_project_sync_changed,
            source_name="main_window"  # Utiliser source_name et non source
        )
        # État de l'application
        self.file_content = []
        self.original_path = None
        self.extraction_results = None
        self.text_mode = "empty"
        self.source_info = None
        self.clipboard_counter = 0

        # Temps d'exécution
        self.last_extraction_time = 0
        self.last_reconstruction_time = 0
        self.last_reconstructed_file = None

    # =============================================================================
    # MÉTHODES DE GESTION DES FICHIERS
    # =============================================================================

    def load_from_clipboard(self, content):
        """Charge du contenu depuis le presse-papier"""
        try:
            start_time = time.time()

            lines = content.splitlines(keepends=True)

            if not lines or len(''.join(lines).strip()) < 10:
                self.main_window.show_notification(
                    "Le contenu du presse-papiers est trop court.",
                    'TOAST', toast_type='warning'
                )
                return

            self.clipboard_counter += 1
            timestamp = int(time.time())

            save_result = self._offer_clipboard_save_simple(content, f"clipboard_{timestamp}")

            if save_result["action"] == "cancel":
                log_message("INFO", "Chargement presse-papier annulé par l'utilisateur", category="clipboard")
                return

            if save_result["action"] == "save_and_continue" and save_result["saved_path"]:
                actual_path = save_result["saved_path"]
                self.text_mode = "file"
                success_message = f"✅ Contenu du presse-papiers ({len(lines)} lignes) sauvegardé et chargé."
                log_message("INFO", f"Contenu presse-papier sauvegardé et chargé: {actual_path}", category="clipboard")
            else:
                log_message("ERREUR", "Cas non prévu dans load_from_clipboard après la sauvegarde.", category="clipboard")
                return

            self.file_content = lines
            self.original_path = actual_path
            self.source_info = {
                'type': self.text_mode,
                'length': len(content),
                'lines': len(lines),
                'timestamp': timestamp,
                'saved_path': save_result.get("saved_path"),
                'virtual': False
            }

            load_time = time.time() - start_time
            self._update_interface_for_content(load_time)
            self.main_window.show_notification(success_message, 'TOAST', toast_type='success')

        except Exception as e:
            log_message("ERREUR", "Erreur chargement presse-papier", e, category="clipboard")
            self.main_window.show_notification(
                f"❌ Erreur : {str(e)}", 'TOAST', toast_type='error'
            )

    def _offer_clipboard_save_simple(self, content, suggested_name):
        """
        Propose de sauvegarder le contenu du presse-papier - VERSION INTELLIGENTE
        Force la sauvegarde dans une structure TL
        """
        try:
            import tkinter.filedialog as filedialog
            from pathlib import Path
            from infrastructure.helpers.unified_functions import show_translated_messagebox, get_last_directory, set_last_directory
            
            lines_count = len(content.splitlines())
            message = f"""Le presse-papiers contient du texte.
    {lines_count} lignes détectées

    Voulez-vous le sauvegarder dans un fichier .rpy ?"""
            
            # Proposition de sauvegarde
            want_to_save = show_translated_messagebox(
                'askyesno', 'Sauvegarder le presse-papiers ?', message,
                parent=self.main_window.root
            )
            
            if not want_to_save:
                return {"action": "cancel", "saved_path": None}
            
            # === SAUVEGARDE INTELLIGENTE ===
            
            # Étape 1: Sélectionner le dossier de langue
            initial_dir = get_last_directory() or str(Path.home())
            
            language_folder = filedialog.askdirectory(
                parent=self.main_window.root,
                title="Sélectionner un dossier de langue (tl/french, tl/english, etc.)",
                initialdir=initial_dir
            )
            
            if not language_folder:
                return {"action": "cancel", "saved_path": None}
            
            # Étape 2: Valider la structure TL
            if not self._validate_language_folder_clipboard(language_folder):
                show_translated_messagebox(
                    'error',
                    "❌ Dossier invalide",
                    "Le dossier sélectionné ne semble pas être un dossier de langue Ren'Py.\n\n"
                    "Veuillez sélectionner un dossier dans une structure tl/ (ex: game/tl/french/)",
                    parent=self.main_window.root
                )
                return {"action": "cancel", "saved_path": None}
            
            # Étape 3: Construire le chemin du fichier
            suggested_filename = f"{suggested_name}.rpy"
            file_path = os.path.join(language_folder, suggested_filename)
            
            # Étape 4: Vérifier si le fichier existe
            if os.path.exists(file_path):
                overwrite = show_translated_messagebox(
                    'askyesno',
                    "📄 Fichier existant",
                    f"Le fichier '{suggested_filename}' existe déjà.\n\n"
                    f"Voulez-vous le remplacer ?",
                    parent=self.main_window.root
                )
                if not overwrite:
                    return {"action": "cancel", "saved_path": None}
            
            # Étape 5: Sauvegarder
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Étape 6: Mettre à jour la config
            set_last_directory(language_folder)
            
            # Étape 7: Message de succès
            show_translated_messagebox(
                'info',
                "✅ Sauvegarde réussie",
                f"Fichier sauvegardé avec succès :\n{os.path.basename(file_path)}\n\n"
                f"Le fichier va maintenant être chargé automatiquement.",
                parent=self.main_window.root
            )
            
            log_message("INFO", f"Clipboard sauvegardé intelligemment: {file_path}", category="clipboard")
            return {"action": "save_and_continue", "saved_path": file_path}
            
        except Exception as e:
            log_message("ERREUR", f"Erreur dialog sauvegarde intelligente: {e}", category="clipboard")
            return {"action": "cancel", "saved_path": None}

    def _validate_language_folder_clipboard(self, folder_path):
        """
        Valide que le dossier sélectionné est un dossier de langue
        Version pour le clipboard
        """
        try:
            if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
                return False
            
            normalized_path = os.path.normpath(os.path.abspath(folder_path))
            path_parts = normalized_path.split(os.sep)
            
            # Chercher 'tl' dans la hiérarchie
            tl_found = False
            tl_index = -1
            
            for i, part in enumerate(path_parts):
                if part.lower() == 'tl':
                    tl_found = True
                    tl_index = i
                    break
            
            if not tl_found:
                return False
            
            # Vérifier qu'on est dans un dossier de langue (pas tl/ lui-même)
            if tl_index + 1 >= len(path_parts):
                return False
            
            # Exclure "None"
            language_name = path_parts[tl_index + 1]
            if language_name.lower() == 'none':
                return False
            
            # Vérifier 'game' avant 'tl'
            if tl_index > 0 and path_parts[tl_index - 1].lower() == 'game':
                return True
            
            return False
            
        except Exception as e:
            log_message("DEBUG", f"Erreur validation dossier langue clipboard: {e}", category="clipboard")
            return False

    # =============================================================================
    # MÉTHODES DE TRAITEMENT
    # =============================================================================

    def _on_project_sync_changed(self, new_path: str):
        """Appelé quand le projet change depuis une autre interface"""
        try:
            if not new_path:
                log_message("DEBUG", "Projet effacé par sync", category="project_sync")
                return
            
            # Mettre à jour InfoFrame
            info_frame = self.main_window.get_component('info')
            if info_frame and hasattr(info_frame, 'set_path'):
                # ✅ IMPORTANT : Ne pas créer de boucle
                # set_path() va déclencher _on_project_changed() qui notifie le ProjectManager
                # Mais le ProjectManager a un flag _updating qui empêche la boucle
                info_frame.set_path(new_path)
                log_message("INFO", f"InfoFrame synchronisé: {os.path.basename(new_path)}", category="project_sync")
                
        except Exception as e:
            log_message("ERREUR", f"Erreur sync projet vers main: {e}", category="project_sync")

    def set_current_project(self, project_path: str, source: str = "main_window"):
        """
        Définit le projet actuel et propage aux autres interfaces
        
        Args:
            project_path: Chemin du projet
            source: Source du changement
        """
        try:
            if hasattr(self, 'project_manager'):
                self.project_manager.set_project(project_path, source)
        except Exception as e:
            log_message("ERREUR", f"Erreur set_current_project: {e}", category="project_sync")

    def force_refresh_project_languages(self):
        """Force le refresh des langues du projet (utile après génération)"""
        try:
            if hasattr(self, 'main_window') and self.main_window:
                self.main_window.force_refresh_project_languages()
                log_message("INFO", "Refresh des langues demandé depuis AppController", category="project_sync")
            else:
                log_message("ATTENTION", "MainWindow non disponible pour refresh des langues", category="project_sync")
        except Exception as e:
            log_message("ERREUR", f"Erreur refresh des langues: {e}", category="project_sync")

    def update_output_field_visibility(self):
        """Met à jour la visibilité du champ de sortie dans tous les composants"""
        if hasattr(self, 'main_window') and self.main_window:
            buttons_frame = self.main_window.get_component('buttons')
            if buttons_frame and hasattr(buttons_frame, '_update_output_field_visibility'):
                buttons_frame._update_output_field_visibility()

    def _get_translation_progress_tracker(self):
        """Obtient le tracker pour le projet+langue actuel"""
        if not self.original_path:
            return None
        
        try:
            # Extraire projet et langue depuis le chemin
            from infrastructure.helpers.unified_functions import extract_game_name
            
            # Trouver le projet racine
            current_dir = os.path.dirname(self.original_path)
            project_root = None
            
            # Remonter jusqu'à trouver le dossier avec /game/
            test_dir = current_dir
            for _ in range(10):  # Max 10 niveaux
                if os.path.exists(os.path.join(test_dir, "game")):
                    project_root = test_dir
                    break
                parent = os.path.dirname(test_dir)
                if parent == test_dir:
                    break
                test_dir = parent
            
            if not project_root:
                return None
            
            # Extraire la langue depuis le chemin (ex: /tl/french/)
            path_parts = self.original_path.replace('\\', '/').split('/')
            tl_index = None
            for i, part in enumerate(path_parts):
                if part == "tl" and i + 1 < len(path_parts):
                    language = path_parts[i + 1]
                    break
            else:
                language = "unknown"
            
            from core.services.extraction.project_progress_tracker import get_translation_tracker
            return get_translation_tracker(project_root, language)
        
        except Exception as e:
            log_message("DEBUG", f"Erreur tracker: {e}", category="progress_tracker")
            return None

    def extract_texts(self):
        """Extrait les textes à traduire"""
        if not self.file_content:
            self.main_window.show_notification('Aucun fichier n\'est chargé.', 'TOAST')
            return

        info_frame = self.main_window.get_component('info')
        if info_frame:
            info_frame.show_processing('Extraction en cours...')

        try:
            self.main_window.show_notification('Lancement de l\'extraction...', 'STATUS')

            if self.original_path:
                backup_manager = UnifiedBackupManager()
                backup_result = backup_manager.create_backup(self.original_path, BackupType.SECURITY, "Sauvegarde avant extraction")
                if not backup_result['success']:
                    log_message("ATTENTION", f"Sauvegarde échouée: {backup_result['error']}", category="extraction")

            extractor = TextExtractor()
            extractor.load_file_content(self.file_content, self.original_path)
            results = extractor.extract_texts()

            self.extraction_results = results
            self.last_extraction_time = getattr(extractor, 'extraction_time', 0)

            # Gérer le timestamp pour les fichiers multiples
            if results.get('dialogue_files') and results['dialogue_files']:
                # Prendre le timestamp du premier fichier
                first_dialogue_file = results['dialogue_files'][0]
                if os.path.exists(first_dialogue_file):
                    self.extraction_file_timestamp = os.path.getmtime(first_dialogue_file)
                    log_message("DEBUG", f"Timestamp fichier extraction stocké: {self.extraction_file_timestamp}", category="extraction")
            elif results.get('dialogue_file') and os.path.exists(results['dialogue_file']):
                self.extraction_file_timestamp = os.path.getmtime(results['dialogue_file'])
                log_message("DEBUG", f"Timestamp fichier extraction stocké: {self.extraction_file_timestamp}", category="extraction")
            else:
                log_message("DEBUG", f"Fichier dialogue non trouvé ou inexistant", category="extraction")

            # Collecter tous les fichiers à ouvrir (support multi-fichiers)
            files_to_open = []
            
            # Fichiers de dialogue (peuvent être multiples)
            if results.get('dialogue_files'):
                files_to_open.extend(results['dialogue_files'])
            elif results.get('dialogue_file'):
                files_to_open.append(results['dialogue_file'])
            
            # Fichiers de doublons (peuvent être multiples)
            if results.get('doublons_files'):
                files_to_open.extend(results['doublons_files'])
            elif results.get('doublons_file'):
                files_to_open.append(results['doublons_file'])
            
            # Fichiers d'astérisques (peuvent être multiples)
            if results.get('asterix_files'):
                files_to_open.extend(results['asterix_files'])
            elif results.get('asterix_file'):
                files_to_open.append(results['asterix_file'])

            auto_open_enabled = config_manager.is_auto_open_enabled()
            if auto_open_enabled and files_to_open:
                FileOpener.open_files(files_to_open, True)

            status_msg = f"{extractor.extracted_count} textes extraits en {self.last_extraction_time:.2f}s"
            self.update_status(status_msg)

            if info_frame and self.original_path:
                info_frame.update_execution_time(self.last_extraction_time)

            # 🆕 NOUVEAU : Mettre à jour le chemin de sortie après extraction réussie
            buttons_frame = self.main_window.get_component('buttons')
            if buttons_frame and hasattr(buttons_frame, 'update_output_path_after_extraction'):
                buttons_frame.update_output_path_after_extraction(self.original_path)

            toast_msg = f"✅ Extraction terminée en {self.last_extraction_time:.2f} secondes."
            self.main_window.show_notification(toast_msg, 'TOAST', duration=5000, toast_type='success')

            # À la fin, si succès
            if results:
                tracker = self._get_translation_progress_tracker()
                if tracker:
                    tracker.scan_translation_folder()
        except Exception as e:
            log_message("ERREUR", "Erreur extraction", e, category="extraction")
            self.main_window.show_notification(
                f"Une erreur est survenue lors de l'extraction :\n{str(e)}", 'MODAL',
                title='Erreur d\'extraction', toast_type='error'
            )
            self.update_status("❌ Erreur lors de l'extraction")
        finally:
            if info_frame:
                info_frame.hide_processing()

    def reconstruct_file(self):
        """Reconstruit le fichier traduit"""
        if not self.file_content or not self.original_path:
            self.main_window.show_notification('Aucun fichier n\'est chargé.', 'TOAST')
            return

        info_frame = self.main_window.get_component('info')
        if info_frame:
            info_frame.show_processing('Reconstruction en cours...')

        try:
            file_base = get_file_base_name(self.original_path)
            
            game_name = extract_game_name(self.original_path)
            translate_folder = os.path.join(FOLDERS["temporaires"], game_name, file_base, "fichiers_a_traduire")

            files_to_clean = [
                os.path.join(translate_folder, f"{file_base}_dialogue.txt"),
                os.path.join(translate_folder, f"{file_base}_doublons.txt"),
                os.path.join(translate_folder, f"{file_base}_asterix.txt")
            ]

            for file_path in files_to_clean:
                if os.path.exists(file_path):
                    corrections = fix_unescaped_quotes_in_txt(file_path)
                    if corrections > 0:
                        log_message("INFO", f"{corrections} correction(s) auto appliquée(s) à {os.path.basename(file_path)}", category="reconstruction")

            if not self.extraction_results:
                self.main_window.show_notification("Vous devez d'abord extraire les textes.", 'TOAST')
                return

            if hasattr(self, 'extraction_file_timestamp') and self.extraction_results.get('dialogue_file'):
                dialogue_file_path = self.extraction_results['dialogue_file']
                if os.path.exists(dialogue_file_path):
                    current_timestamp = os.path.getmtime(dialogue_file_path)
                    if current_timestamp == self.extraction_file_timestamp:
                        log_message("INFO", f"Fichier de traduction non modifié depuis l'extraction (timestamp: {self.extraction_file_timestamp})", category="reconstruction")
                        from infrastructure.helpers.unified_functions import show_translated_messagebox
                        response = show_translated_messagebox(
                            'askyesno', "Fichier de traduction non modifié",
                            "Le fichier de traduction ne semble pas avoir été modifié depuis la dernière extraction.\n\nVoulez-vous continuer la reconstruction quand même ?", parent=self.main_window.root
                        )
                        if not response:
                            log_message("INFO", "Reconstruction annulée par l'utilisateur", category="reconstruction")
                            return

            # Validation automatique avant reconstruction
            if not self._validate_before_reconstruction():
                return

            save_mode = self._determine_save_mode()
            if not save_mode:
                return

            self.main_window.show_notification('Lancement de la reconstruction...', 'STATUS')

            start_time = time.time()
            reconstructor = FileReconstructor()
            reconstructor.load_file_content(self.file_content, self.original_path)
            result = reconstructor.reconstruct_file(save_mode)
            self.last_reconstruction_time = time.time() - start_time

            if result:
                self.last_reconstructed_file = result['save_path']
                self._post_process_reconstructed_file(result['save_path'])
                status_msg = f"Reconstruction terminée en {self.last_reconstruction_time:.2f}s"
                self.update_status(status_msg)

                if info_frame and self.original_path:
                    info_frame.update_execution_time(self.last_reconstruction_time)

                auto_open_enabled = config_manager.is_auto_open_enabled()
                FileOpener.open_files([result['save_path']], auto_open_enabled)
                self._show_reconstruction_success_message(result['save_path'])
            else:
                self.main_window.show_notification(
                    "La reconstruction a échoué pour une raison inconnue.", 'MODAL',
                    title='Erreur de reconstruction', toast_type='error'
                )
            # À la fin, si succès
            if result:
                tracker = self._get_translation_progress_tracker()
                if tracker:
                    tracker.scan_translation_folder()
        except Exception as e:
            log_message("ERREUR", "Erreur reconstruction", e, category="reconstruction")
            self.main_window.show_notification(
                f"Une erreur est survenue lors de la reconstruction :\n{str(e)}", 'MODAL',
                title='Erreur de reconstruction', toast_type='error'
            )            
        finally:
            if info_frame:
                info_frame.hide_processing()

    def reload_reconstructed(self):
        """Recharge et vérifie le fichier reconstruit"""
        if not self.last_reconstructed_file or not os.path.exists(self.last_reconstructed_file):
            self.main_window.show_notification("Aucun fichier récemment reconstruit à recharger.", 'TOAST')
            return

        try:
            file_base = get_file_base_name(self.last_reconstructed_file)
            
            game_name = extract_game_name(self.last_reconstructed_file)
            translate_folder = os.path.join(FOLDERS["temporaires"], game_name, file_base, "fichiers_a_traduire")
            main_txt_path = os.path.join(translate_folder, f"{file_base}_dialogue.txt")
            if os.path.exists(main_txt_path):
                fix_unescaped_quotes_in_txt(main_txt_path)

            with open(self.last_reconstructed_file, 'r', encoding='utf-8') as f:
                self.file_content = f.readlines()

            self.original_path = self.last_reconstructed_file
            self._update_interface_for_content()

            # Vérification de cohérence avec les options configurées par l'utilisateur
            from core.services.tools.coherence_checker_business import check_coherence_unified
            coherence_result = check_coherence_unified(self.last_reconstructed_file, return_details=False)
            
            # Le reste du traitement reste identique
            if coherence_result is None:
                self.main_window.show_notification("Aucune incohérence détectée dans le fichier.", 'TOAST', toast_type='success')
            elif isinstance(coherence_result, str) and os.path.exists(coherence_result):
                try:
                    with open(coherence_result, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    import re
                    match = re.search(r'(\d+) problèmes? détectés?', content)
                    if match:
                        issues_count = int(match.group(1))
                        self.main_window.show_notification(
                            f"{issues_count} problèmes de cohérence détectés.",
                            'TOAST', toast_type='warning'
                        )
                    else:
                        self.main_window.show_notification(
                            "Des problèmes de cohérence ont été détectés.",
                            'TOAST', toast_type='warning'
                        )
                except Exception:
                    self.main_window.show_notification(
                        "Des problèmes de cohérence ont été détectés.",
                        'TOAST', toast_type='warning'
                    )
            else:
                log_message("DEBUG", f"Format coherence_result inattendu: {type(coherence_result)}", category="coherence_check")
                self.main_window.show_notification("Vérification de cohérence terminée.", 'TOAST', toast_type='info')

            self.main_window.show_notification("Fichier reconstruit rechargé avec succès.", 'TOAST', toast_type='success')

        except Exception as e:
            log_message("ERREUR", f"Erreur rechargement | Exception: {e}", category="reconstruction")
            self.main_window.show_notification(
                f"Erreur lors du rechargement : {str(e)}", 'TOAST', toast_type='error'
            )

    # =============================================================================
    # MÉTHODES D'INTERFACE
    # =============================================================================

    def toggle_theme(self):
        """Bascule le thème sombre/clair avec application immédiate"""
        try:
            new_theme = theme_manager.toggle_theme()
            self.main_window.apply_theme()
            log_message("INFO", f"Thème changé vers: {new_theme}", category="theme")
        except Exception as e:
            log_message("ERREUR", f"Erreur basculement thème: {e}", category="theme")
            self.main_window.show_notification("Erreur lors du changement de thème", 'TOAST')

    def toggle_auto_open(self):
        """Bascule l'auto-ouverture"""
        try:
            new_state = config_manager.toggle_auto_open()

            buttons_frame = self.main_window.get_component('buttons')
            if buttons_frame:
                    buttons_frame.update_output_path_after_extraction(self.original_path)

            content_frame = self.main_window.get_component('content')
            if content_frame:
                content_frame.update_display_for_auto_open()
            
            message = "Ouverture automatique des fichiers activée." if new_state else "Ouverture automatique des fichiers désactivée."
            self.main_window.show_notification(message, 'TOAST')
        except Exception as e:
            log_message("ERREUR", "Erreur toggle auto-open", e, category="auto_open")

    def show_help(self):
        """Affiche la fenêtre d'aide principale et unifiée."""
        try:
            from ui.tutorial import show_tutorial
            show_tutorial(self.main_window.root)
        except Exception as e:
            log_message("ERREUR", "Erreur lors de l'affichage de l'aide unifiée", e, category="help")
            self.main_window.show_notification(
                f"Impossible d'ouvrir le module d'aide.\nErreur : {e}",
                'MODAL',
                title="Erreur Aide"
            )

    def open_warnings(self):
        """Ouvre le dossier d'avertissements pour le jeu en cours, s'il n'est pas vide."""
        try:
            # Étape 1 : Vérifier qu'un fichier est chargé (logique identique)
            if not self.original_path:
                self.main_window.show_notification("Chargez un fichier d'abord.", 'TOAST')
                return

            
            from infrastructure.helpers.unified_functions import extract_game_name
            import os

            # Étape 2 : Extraire le nom du jeu et construire le chemin du sous-dossier (logique identique)
            game_name = extract_game_name(self.original_path)
            warnings_folder = os.path.join(FOLDERS["warnings"], game_name)

            # Étape 3 : Vérifier si ce dossier spécifique existe et s'il contient des fichiers/dossiers
            if not os.path.exists(warnings_folder) or not os.listdir(warnings_folder):
                self.main_window.show_notification(f"Aucun avertissement trouvé pour le jeu '{game_name}'.", 'TOAST', toast_type='info')
                return

            # Étape 4 : Si tout est bon, ouvrir le dossier spécifique au jeu
            self._open_folder(warnings_folder)
            self.main_window.show_notification(
                f"Ouverture du dossier d'avertissements pour '{game_name}'.",
                'TOAST', toast_type='success'
            )
                
        except Exception as e:
            log_message("ERREUR", "Erreur ouverture avertissements", e, category="warnings")
            self.main_window.show_notification("Erreur lors de l'ouverture du dossier d'avertissements.", 'TOAST', toast_type='error')

    def open_temporary(self):
        """Ouvre le dossier temporaire"""
        try:
            if not self.original_path:
                self.main_window.show_notification("Chargez un fichier d'abord.", 'TOAST')
                return

            game_name = extract_game_name(self.original_path)
            temp_folder = os.path.join(FOLDERS["temporaires"], game_name)

            if not os.path.exists(temp_folder):
                ensure_game_structure(game_name)

            self._open_folder(temp_folder)
        except Exception as e:
            log_message("ERREUR", "Erreur ouverture temporaire", e, category="temporary")

    def reset_application(self):
        """Réinitialise l'application"""
        try:
            file_count = len(self.file_content) if self.file_content else 0
            confirm_msg = f"Ceci réinitialisera l'application et effacera le contenu actuel ({file_count} lignes).\n\nCela supprimera aussi les configurations utilisateur et outils téléchargés.\n\nÊtes-vous sûr de vouloir continuer ?"
            result = self.main_window.show_notification(confirm_msg, 'CONFIRM', title="Confirmer la réinitialisation")
            if not result:
                return
            self._reset_application_state()
            self._clean_temp_folders()
            self._clean_user_config_folders()  # Nouvelle fonction
            self._update_interface_for_reset()
            # Remettre le chemin de sortie à l'état initial
            buttons_frame = self.main_window.get_component('buttons')
            if buttons_frame and hasattr(buttons_frame, 'clear_output_path'):
                buttons_frame.clear_output_path()
            self.main_window.show_notification("Réinitialisation complète de l'application terminée.", 'TOAST', toast_type='success')
        except Exception as e:
            log_message("ERREUR", "Erreur réinitialisation", e, category="reset")

    def _clean_user_config_folders(self):
        """Nettoie les dossiers de configuration utilisateur"""
        import os
        import shutil
        from pathlib import Path
        
        try:
            # Obtenir le dossier utilisateur
            user_home = Path.home()
            
            # Dossier à nettoyer
            folders_to_clean = [
                user_home / ".renextract_tools"
            ]
            
            for folder_path in folders_to_clean:
                if folder_path.exists():
                    try:
                        shutil.rmtree(folder_path)
                        log_message("INFO", f"Dossier supprimé: {folder_path}", category="reset")
                    except Exception as e:
                        log_message("ATTENTION", f"Impossible de supprimer {folder_path}: {e}", category="reset")
                        
        except Exception as e:
            log_message("ERREUR", f"Erreur nettoyage dossiers utilisateur: {e}", category="reset")

    def refresh(self):
        """Actualise l'affichage"""
        try:
            if self.original_path and os.path.exists(self.original_path):
                self._load_file_content(self.original_path)
                self.main_window.show_notification("Affichage actualisé.", 'TOAST', toast_type='success')
            else:
                self.main_window.show_notification("Aucun fichier à actualiser.", 'TOAST')
        except Exception as e:
            log_message("ERREUR", "Erreur actualisation", e, category="refresh")

    def quit_application(self):
        """Ferme l'application"""
        try:
            # Sauvegarder les états des fenêtres pour la prochaine session
            try:
                from ui.window_manager import get_window_manager
                window_manager = get_window_manager()
                window_manager.save_on_close()
                log_message("INFO", "États des fenêtres sauvegardés", category="quit")
            except Exception as save_error:
                log_message("ATTENTION", f"Erreur sauvegarde états fenêtres: {save_error}", category="quit")
            
            self.main_window.root.quit()
            self.main_window.root.destroy()
            log_message("INFO", "Application fermée proprement", category="quit")
        except Exception as e:
            log_message("ERREUR", "Erreur fermeture", e, category="quit")
        finally:
            import sys
            sys.exit(0)

    def toggle_debug_mode(self):
        """Bascule le mode debug pour afficher plus de logs"""
        try:
            current_debug = config_manager.get('debug_mode', False)
            new_state = not current_debug
            config_manager.set('debug_mode', new_state)

            logger = get_logger()
            logger._load_debug_config()

            log_message("INFO", "✅ Mode debug activé" if new_state else "❌ Mode debug désactivé", category="debug_mode")

            header_frame = self.main_window.get_component('header')
            if header_frame and hasattr(header_frame, 'update_debug_button'):
                header_frame.update_debug_button()

            message = "✅ Mode debug activé." if new_state else "❌ Mode debug désactivé."
            self.main_window.show_notification(message, 'TOAST', toast_type='info')
        except Exception as e:
            log_message("ERREUR", f"Erreur lors du basculement du mode debug: {e}", category="debug_mode")
            self.main_window.show_notification("Erreur lors du changement du mode debug.", 'TOAST', toast_type='error')

    # =============================================================================
    # MÉTHODES UTILITAIRES
    # =============================================================================

    def update_status(self, message):
        """Met à jour le statut"""
        info_frame = self.main_window.get_component('info')
        if info_frame:
            info_frame.update_status(message)

    def _validate_and_load_file(self, filepath):
        """Valide et charge un fichier"""
        if not os.path.exists(filepath):
            self.main_window.show_notification(f"Le fichier spécifié n'a pas été trouvé :\n{filepath}", 'MODAL', title="Fichier non trouvé")
            return False

        if not filepath.lower().endswith('.rpy'):
            self.main_window.show_notification("Type de fichier non supporté. Veuillez sélectionner un fichier .rpy.", 'MODAL', title="Fichier non supporté")
            return False

        from core.services.extraction.extraction import validate_file_safely
        validation = validate_file_safely(filepath)
        if not validation['valid']:
            self.main_window.show_notification(f"Erreur de structure Ren'Py: {validation['error']}", 'MODAL', title="Structure invalide")
            return False

        return self._load_file_content(filepath)

    def _load_file_content(self, filepath):
        """Charge le contenu d'un fichier"""
        try:
            # Éviter les chargements multiples du même fichier
            if (hasattr(self, 'original_path') and 
                self.original_path == filepath and 
                hasattr(self, 'file_content') and 
                self.file_content is not None):
                return True
                
            start_time = time.time()
            self.file_content = file_manager.load_file_content(filepath)
            if not self.file_content:
                return False

            load_time = time.time() - start_time
            self.original_path = filepath
            self.text_mode = "file"
            self.source_info = {
                'type': 'file', 'path': filepath,
                'lines': len(self.file_content),
                'size': os.path.getsize(filepath) if os.path.exists(filepath) else 0
            }

            self._update_interface_for_content(load_time)
            return True
        except Exception as e:
            log_message("ERREUR", f"Erreur chargement fichier: {e}", category="file_io")
            return False

    def _update_interface_for_content(self, load_time=None):
        """Met à jour l'interface après chargement de contenu"""
        if not self.main_window:
            log_message("DEBUG", "main_window non disponible, skip mise à jour interface", category="file_io")
            return
        
        # Vérifier que l'interface est complètement initialisée
        if not hasattr(self.main_window, 'get_component') or not self.main_window.get_component('content'):
            log_message("DEBUG", "Interface pas encore prête, retry dans 50ms", category="file_io")
            if hasattr(self.main_window, 'after'):
                self.main_window.after(50, lambda: self._update_interface_for_content(load_time))
            return
            
        self.main_window.update_file_info(self.original_path, len(self.file_content))

        content_frame = self.main_window.get_component('content')
        if content_frame:
            content_frame.load_content(self.file_content)

        if load_time is not None:
            info_frame = self.main_window.get_component('info')
            if info_frame and hasattr(info_frame, 'update_execution_time'):
                info_frame.update_execution_time(load_time)

    def _update_interface_for_reset(self):
        """Met à jour l'interface après réinitialisation"""
        if not self.main_window:
            log_message("DEBUG", "main_window non disponible, skip reset interface", category="file_io")
            return
            
        content_frame = self.main_window.get_component('content')
        if content_frame:
            content_frame.clear_content()

        self.main_window.update_file_info(None, 0)
        self.main_window.root.title(f'{VERSION}')

    def _validate_folder_files(self, files):
        """Valide les fichiers d'un dossier"""
        from core.services.extraction.extraction import validate_file_safely
        valid_files = []
        for filepath in files:
            validation = validate_file_safely(filepath)
            if validation['valid']:
                valid_files.append(filepath)
            else:
                log_message("ATTENTION", f"Fichier ignoré: {os.path.basename(filepath)} - {validation['error']}", category="file_io")
        return valid_files

    def _validate_before_reconstruction(self):
        """Validation avant reconstruction avec les valeurs correctes - CHEMIN CORRIGÉ"""
        try:
            if not self.extraction_results:
                log_message("ATTENTION", "Aucun résultat d'extraction disponible pour la validation", category="validation")
                return True
                
            extracted_count = self.extraction_results.get('extracted_count', 0)
            asterix_count = self.extraction_results.get('asterix_count', 0)
            tilde_count = self.extraction_results.get('tilde_count', 0)
            empty_count = self.extraction_results.get('empty_count', 0)
            
            # Le fichier asterix.txt contient à la fois les astérisques ET les tildes
            combined_asterix_count = asterix_count + tilde_count
            
            log_message("DEBUG", f"Validation avec: extracted={extracted_count}, asterix={asterix_count}, tildes={tilde_count}, combined_asterix={combined_asterix_count}, empty={empty_count}", category="validation")
            
            if extracted_count == 0:
                log_message("ATTENTION", "extracted_count est 0, tentative de recalcul.", category="validation")
                
                # ✅ UTILISER LA MÊME LOGIQUE que update_output_path_after_extraction
                file_base = get_file_base_name(self.original_path)
                game_name = extract_game_name(self.original_path)
                
                # ✅ CONSTRUIRE LE CHEMIN comme dans ButtonsFrame
                
                output_path = os.path.join(
                    FOLDERS["temporaires"], 
                    game_name, 
                    file_base,  # Sous-dossier fichier
                    "fichiers_a_traduire"
                )
                
                dialogue_file = os.path.join(output_path, f"{file_base}_dialogue.txt")
                
                # ✅ DEBUG: Afficher le chemin construit
                log_message("DEBUG", f"Chemin dialogue construit: {dialogue_file}", category="validation")
                log_message("DEBUG", f"Le fichier existe: {os.path.exists(dialogue_file)}", category="validation")
                
                # ✅ VÉRIFICATION D'EXISTENCE plus robuste
                if os.path.exists(dialogue_file):
                    try:
                        with open(dialogue_file, 'r', encoding='utf-8') as f:
                            extracted_count = sum(1 for line in f if line.strip())
                        log_message("DEBUG", f"Recalculé extracted_count depuis le fichier: {extracted_count}", category="validation")
                    except Exception as e:
                        log_message("ERREUR", f"Erreur lecture fichier dialogue: {e}", category="validation")
                else:
                    # ✅ RECHERCHE ALTERNATIVE si le chemin exact échoue
                    log_message("DEBUG", "Fichier dialogue non trouvé, recherche alternative...", category="validation")
                    
                    # Chercher dans tous les sous-dossiers possibles
                    base_dir = os.path.join(FOLDERS["temporaires"], game_name)
                    if os.path.exists(base_dir):
                        for root, dirs, files in os.walk(base_dir):
                            for file in files:
                                if file == f"{file_base}_dialogue.txt":
                                    found_file = os.path.join(root, file)
                                    log_message("DEBUG", f"Fichier dialogue trouvé à: {found_file}", category="validation")
                                    try:
                                        with open(found_file, 'r', encoding='utf-8') as f:
                                            extracted_count = sum(1 for line in f if line.strip())
                                        log_message("DEBUG", f"Recalculé extracted_count (recherche): {extracted_count}", category="validation")
                                        break
                                    except Exception as e:
                                        log_message("ERREUR", f"Erreur lecture fichier trouvé: {e}", category="validation")
                    
            # ✅ VALIDATION avec le chemin corrigé
            file_base = get_file_base_name(self.original_path)
            
            # ✅ VALIDATION - Plus claire et fiable
            # Utiliser combined_asterix_count car le fichier asterix.txt contient astérisques + tildes
            # ✅ CORRIGÉ : Passer original_path pour utiliser le bon game_name
            validation_result = validate_before_reconstruction(
                file_base, 
                extracted_count, 
                combined_asterix_count,  # Utiliser le compteur combiné
                empty_count,
                original_path=self.original_path  # ✅ NOUVEAU : Passer le chemin original
            )
            
            if not validation_result['overall_valid']:
                # Utiliser les erreurs du nouveau système de validation
                errors = validation_result['summary']['errors']
                
                error_summary = "\n".join(f"• {error}" for error in errors[:3])
                if len(errors) > 3:
                    error_summary += f"\n... et {len(errors) - 3} autres erreurs."
                
                full_message = f"La validation avant reconstruction a échoué. Erreurs détectées :\n{error_summary}\n\nVoulez-vous forcer la reconstruction ?"
                
                # Demander confirmation pour forcer la reconstruction
                user_choice = self.main_window.show_notification(
                    full_message, 
                    'CONFIRM', 
                    title="Échec de la validation"
                )
                
                # Si l'utilisateur refuse, arrêter la reconstruction
                if not user_choice:
                    log_message("INFO", "Reconstruction annulée par l'utilisateur suite à l'échec de validation", category="validation")
                    return False
                
                # Si l'utilisateur accepte de forcer, continuer avec un avertissement
                log_message("ATTENTION", "Reconstruction forcée par l'utilisateur malgré les erreurs de validation", category="validation")
                return True
            
            return True
        
        except Exception as e:
            log_message("ERREUR", f"Erreur validation avant reconstruction: {e}", category="validation")
            return False

    def _determine_save_mode(self):
        """Détermine le mode de sauvegarde - BASÉ SUR LA CONFIGURATION"""
        return config_manager.get('default_save_mode', 'overwrite')

    def _post_process_reconstructed_file(self, file_path):
        """Post-traitement du fichier reconstruit"""
        try:
            # Contrôle de cohérence automatique
            self._clean_old_warning_files(file_path)
        
            # Vérification de cohérence avec les options configurées par l'utilisateur
            from core.services.tools.coherence_checker_business import check_coherence_unified
            coherence_result = check_coherence_unified(file_path, return_details=False)
        
            # Le reste du traitement reste identique
            if coherence_result is None:
                # Aucun problème détecté
                self.main_window.show_notification(
                    "Aucune incohérence détectée.", 'TOAST', toast_type='success'
                )
            elif isinstance(coherence_result, str) and os.path.exists(coherence_result):
                # Rapport créé = des problèmes ont été détectés
                try:
                    # Compter les problèmes dans le rapport
                    with open(coherence_result, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extraire le nombre de problèmes du rapport
                    import re
                    match = re.search(r'(\d+) problèmes? détectés?', content)
                    if match:
                        issues_count = int(match.group(1))
                        self.main_window.show_notification(
                            f"{issues_count} problèmes de cohérence détectés.",
                            'TOAST', toast_type='warning'
                        )
                    else:
                        self.main_window.show_notification(
                            "Des problèmes de cohérence ont été détectés.",
                            'TOAST', toast_type='warning'
                        )
                except Exception:
                    self.main_window.show_notification(
                        "Des problèmes de cohérence ont été détectés.",
                        'TOAST', toast_type='warning'
                    )
            else:
                # Format inattendu mais pas None
                log_message("DEBUG", f"Format coherence_result inattendu: {type(coherence_result)}", category="coherence_check")
                self.main_window.show_notification(
                    "Vérification de cohérence terminée.", 'TOAST', toast_type='info'
                )
            
        except Exception as e:
            log_message("ATTENTION", f"Erreur post-traitement: {e}", category="coherence_check")

    def _show_reconstruction_success_message(self, file_path):
        """Affiche le message de succès de reconstruction"""
        filename = os.path.basename(file_path)
        auto_open_enabled = config_manager.is_auto_open_enabled()
        
        if auto_open_enabled:
            message = f"✅ Fichier '{filename}' reconstruit et ouvert en {self.last_reconstruction_time:.2f}s."
        else:
            message = f"✅ Fichier '{filename}' reconstruit en {self.last_reconstruction_time:.2f}s."
            
        self.main_window.show_notification(message, 'TOAST', duration=5000, toast_type='success')

    def _clean_old_warning_files(self, file_path):
        """Nettoie les anciens fichiers d'avertissement"""
        try:
            

            game_name = extract_game_name(file_path)
            warnings_folder = os.path.join(FOLDERS["warnings"], game_name)

            if os.path.exists(warnings_folder):
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                old_warning_file = os.path.join(warnings_folder, f"{base_name}_avertissement.txt")
                if os.path.exists(old_warning_file):
                    os.remove(old_warning_file)
                    log_message("INFO", "Ancien fichier d'avertissement supprimé", category="warnings")
        except Exception as e:
            log_message("ATTENTION", f"Erreur nettoyage anciens avertissements: {e}", category="warnings")

    def clean_temp_only(self):
        """Nettoie les dossiers temporaires sans toucher à l'application"""
        try:
            self._clean_temp_folders()
            self.main_window.show_notification("Nettoyage terminé ✅", 'TOAST', toast_type='success')
        except Exception as e:
            log_message("ERREUR", "Erreur nettoyage", e, category="cleanup")

    def _reset_application_state(self):
        """Remet à zéro l'état de l'application"""
        self.file_content = []
        self.original_path = None
        self.extraction_results = None
        self.text_mode = "empty"
        self.source_info = None
        self.last_extraction_time = 0
        self.last_reconstruction_time = 0
        self.last_reconstructed_file = None
        file_manager.reset()

    def _reset_configuration(self):
        """Remet la configuration aux valeurs par défaut et supprime config.json"""
        try:
            config_manager.delete_config_file()
            config_manager.save_config()
            self.main_window.apply_theme()
            log_message("INFO", "Configuration ET fichier config.json réinitialisés", category="reset")
        except Exception as e:
            log_message("ERREUR", f"Erreur reset configuration complète: {e}", category="reset")

    def _clean_temp_folders(self):
        """Nettoie tous les dossiers temporaires"""
        try:
            
            import shutil

            for folder_type in ["temporaires", "backup", "warnings"]:
                root_folder = FOLDERS.get(folder_type)
                if root_folder and os.path.exists(root_folder):
                    # Supprimer TOUT le contenu du dossier
                    for item in os.listdir(root_folder):
                        item_path = os.path.join(root_folder, item)
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                            log_message("INFO", f"Dossier {folder_type}/{item} supprimé", category="cleanup")
                        elif os.path.isfile(item_path):
                            os.remove(item_path)
                            log_message("INFO", f"Fichier {folder_type}/{item} supprimé", category="cleanup")
                            
        except Exception as e:
            log_message("ATTENTION", f"Erreur nettoyage dossiers: {e}", category="cleanup")

    def _update_window_title(self, remaining_files=None):
        """Met à jour le titre de la fenêtre"""
        base_title = f'{VERSION}'
        if file_manager.is_folder_mode and remaining_files is not None:
            title = f"{base_title} - Mode Dossier ({remaining_files} fichiers restants)"
        else:
            title = base_title
        self.main_window.root.title(title)

    def next_file(self):
        """Passe au fichier suivant en mode dossier"""
        try:
            if not file_manager.is_folder_mode:
                self.main_window.show_notification("Vous n'êtes pas en mode dossier.", 'TOAST', toast_type='info')
                return

            if not file_manager.has_next_file():
                self.main_window.show_notification("C'était le dernier fichier du dossier.", 'TOAST', toast_type='info')
                return

            next_file_info = file_manager.advance_to_next_file()

            if next_file_info and self._load_file_content(next_file_info['file']):
                self._update_window_title(next_file_info['remaining'])
                self._update_next_file_button()
                filename = os.path.basename(next_file_info['file'])
                self.main_window.show_notification(
                    f"Fichier suivant : {filename} ({next_file_info['current_index'] + 1}/{next_file_info['total_files']})",
                    'TOAST', toast_type='success'
                )
                log_message("INFO", f"Fichier suivant chargé: {next_file_info['file']}", category="navigation")
            elif next_file_info:
                self.main_window.show_notification("Erreur lors du chargement du fichier suivant.", 'TOAST', toast_type='error')
            else:
                 self.main_window.show_notification("Il n'y a plus de fichiers à traiter.", 'TOAST', toast_type='info')
        except Exception as e:
            log_message("ERREUR", "Erreur passage fichier suivant", e, category="navigation")
            self.main_window.show_notification(f"Erreur lors du passage au fichier suivant : {str(e)}", 'TOAST', toast_type='error')

    def is_in_folder_mode(self):
        """Retourne si l'application est en mode dossier"""
        return file_manager.is_folder_mode

    def has_next_file(self):
        """Retourne s'il y a un fichier suivant disponible"""
        return file_manager.has_next_file()

    def _update_next_file_button(self):
        """Met à jour l'état du bouton fichier suivant"""
        buttons_frame = self.main_window.get_component('buttons')
        if buttons_frame and hasattr(buttons_frame, 'update_next_file_button'):
            buttons_frame.update_next_file_button(self.is_in_folder_mode(), self.has_next_file())

    def _open_folder(self, folder_path):
        """Ouvre un dossier avec l'explorateur de fichiers natif"""
        try:
            import sys
            import subprocess

            if os.name == 'nt':  # Windows
                os.startfile(os.path.normpath(folder_path))
            elif sys.platform == 'darwin':  # macOS
                subprocess.call(['open', folder_path])
            else:  # Linux
                subprocess.call(['xdg-open', folder_path])
        except Exception as e:
            log_message("ATTENTION", f"Impossible d'ouvrir le dossier {folder_path}: {e}", category="navigation")
            self.main_window.show_notification(f"Impossible d'ouvrir le dossier : {folder_path}", 'TOAST')

    def launch_renpy_generator(self):
        """Lance le générateur de traduction Ren'Py intégré."""
        try:
            from ui.dialogs.translation_generator_interface import show_translation_generator
            # 🆕 CORRECTION : Passer main_window au lieu de root pour avoir accès à app_controller
            generator_interface = show_translation_generator(self.main_window)
            if generator_interface:
                log_message("INFO", "🎮 Générateur Ren'Py ouvert !", category="renpy_generator")
            else:
                log_message("ATTENTION", "La fenêtre du générateur Ren'Py n'a pas été créée ou a été annulée.", category="renpy_generator")
        except ImportError as ie:
            log_message("CRITICAL", f"Échec de l'importation pour le générateur intégré: {ie}", category="renpy_generator")
        except Exception as e:
            log_message("ERREUR", f"Erreur lors du lancement du générateur Ren'Py: {e}", category="renpy_generator")
