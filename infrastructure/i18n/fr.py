TRANSLATIONS = {
    "window": {
        "title": "{version}",
        "subtitle": "Extraction intelligente de scripts Ren'Py"
    },
    "buttons_frame": {
        "pastilles": {
            "active": "✅",
            "inactive": "❎", 
            "unavailable": "🚫",
            "next_file_active": "▶️"
        }
    },
    "tabs": {
        "entree": "ENTRÉE",
        "actions": "ACTIONS", 
        "outils": "OUTILS",
        "avancee": "AVANCÉE",
        "aide": "AIDE"
    },
    "buttons": {
        "open_file": "Ouvrir Fichier",
        "open_folder": "Ouvrir Dossier",
        "next_file": "Fichier Suivant",
        "next_file_last": "Dernier Fichier",
        "next_file_disabled": "Pas de Fichier Suivant",
        "drag_drop": "Mode Glisser-déposer",
        "ctrl_v": "Mode Ctrl+V",
        "extract_ui_characters": "Oublie du SDK Ren'Py",
        "extract": "Extraire",
        "reconstruct": "Reconstruire", 
        "reload": "Revérifier",
        "warnings": "Avertissements",
        "check_tl_coherence": "Vérifier Cohérence TL",
        "intelligent_cleanup": "Nettoyer TL",
        "auto_open": "Ouverture-Auto : {status}",
        "temporary": "Temporaire",
        "glossary": "Glossaire",
        "backups": "Sauvegardes",
        "ok": "OK",
        "cancel": "Annuler",
        "quit": "Quitter",
        "language": "Langue", 
        "about": "À propos",
        "reset": "Réinitialiser",
        "theme": "Mode Clair",
        "theme_dark": "Mode Sombre",
        "debug_button": "Debug {status}",
        "no": "Non",
        "yes": "Oui",
        "close": "Fermer",
        "renpy_generator": "Générateur Ren'Py",
        "complete_guide": "Guide Complet",
        "express_guide": "Guide Express",
        "execution_process": "Processus d'exécution",
        "sections_guide": "Guide des Sections",
        "faq": "FAQ",
        "select_all": "Tout sélectionner",
        "select_none": "Tout désélectionner",
        "start_cleaning": "Nettoyer",
        "add": "Ajouter",
        "edit": "Modifier",
        "modify": "Modifier", 
        "delete": "Supprimer",
        "new": "Nouveau",
        "export": "Exporter",
        "import": "Importer",
        "validate": "Valider",
        "save": "Sauvegarder",
        "general_settings": "Paramètres"
    },
    "general_settings": {
        "window_title": "Paramètres généraux",
        "main_title": "Paramètres généraux de l'application", 
        "subtitle": "Configurez le comportement global de RenExtract selon vos préférences",
        "protection_types": "Paramètres de traitement",
        "information_title": "Informations",
        "info_text": "Ces paramètres contrôlent le comportement général de l'application. Vous pouvez les ajuster selon vos besoins et votre façon de travailler.",
        "protect_codes": "Protéger les codes et variables Ren'Py",
        "protect_empty": "Protéger les textes vides et guillemets", 
        "protect_glossary": "Utiliser le glossaire automatiquement",
        "protect_asterisk": "Extraire le contenu entre astérisques",
        "detect_duplicates": "Détecter et gérer les doublons",
        "auto_open": "Ouverture automatique des fichiers",
        "coherence_check": "Vérification de cohérence automatique",
        "reset_defaults": "Par défaut",
        "confirm_disable_title": "Confirmation", 
        "confirm_disable_message": "Êtes-vous sûr de vouloir désactiver tous les paramètres ? Cela peut affecter le comportement de l'application et la qualité du traitement.",
        "help_title": "Aide - Paramètres généraux",
        "help_protect_codes": "Protège les variables Ren'Py ([player_name], {b}texte{/b}, etc.) et les codes spéciaux lors du traitement. Recommandé pour éviter la corruption des scripts.",
        "help_protect_empty": "Protège les guillemets vides (\"\"), les espaces (\" \") et les guillemets échappés (\\\") lors du traitement. Essentiel pour la structure du dialogue.",
        "help_protect_glossary": "Applique automatiquement le glossaire lors de l'extraction pour remplacer les termes récurrents. Utile pour les noms propres et termes techniques.",
        "help_protect_asterisk": "Extrait automatiquement le contenu entre astérisques (*action*, *pensée*) dans un fichier séparé. Recommandé pour les descriptions d'actions.",
        "help_detect_duplicates": "Détecte les phrases identiques lors de l'extraction pour éviter de les traduire plusieurs fois. Recommandé pour optimiser le travail de traduction.",
        "help_auto_open": "Ouvre automatiquement les fichiers générés après extraction ou reconstruction dans votre éditeur par défaut.",
        "help_coherence_check": "Lance automatiquement une vérification de cohérence après reconstruction et génère un rapport si des problèmes sont détectés.",
        "help_default": "Aucune aide disponible pour cette option.",
        "auto_open": "Ouverture automatique des fichiers",
        "coherence_check": "Vérification de cohérence automatique", 
        "help_auto_open": "Ouvre automatiquement les fichiers générés après extraction dans votre éditeur par défaut",
        "help_coherence_check": "Vérifie automatiquement la cohérence du fichier après extraction et génère un rapport si des problèmes sont détectés",
        "parameter_changed": "Paramètre modifié",
        "all_enabled": "Tous les paramètres activés",
        "all_disabled": "Tous les paramètres désactivés"
    },
    "renpy_generator": {
        "window_title": "Générateur de Traductions Ren'Py",
        "main_title": "Générateur de Traductions Ren'Py", 
        "subtitle": "Extraction • Génération • Combinaison • Division",
        "tab_extraction": "Extraction RPA/RPYC",
        "tab_generation": "Génération", 
        "tab_combination": "Combinaison/Division",
        "tab_settings": "Paramètres",
        "tab_cleaning": "Nettoyage",
        "btn_start_cleaning": "Démarrer le nettoyage",
        "desc_cleaning": "Nettoyage intelligent des traductions orphelines avec SDK Ren'Py",        
        "label_project": "Projet:",
        "label_sdk": "Ren'Py SDK:",
        "label_target_language": "Langue cible:",
        "label_source_folder": "Dossier source:",
        "label_output_file": "Fichier de sortie:",
        "label_combined_file": "Fichier combiné:",
        "label_output_folder": "Dossier de sortie:",
        "label_general_settings": "Paramètres généraux",
        "label_project_management": "Gestion des projets",
        "label_combination_files": "Combinaison de fichiers",
        "label_file_division": "Division de fichier",
        "label_configuration": "Configuration",
        "label_progress": "Progression:",
        "label_extraction_options": "Options d'extraction",
        "label_excluded_files": "Fichiers exclus de la combinaison:",
        "btn_browse": "Parcourir",
        "btn_launch_extraction": "Lancer l'extraction", 
        "btn_generate_translations": "Générer les traductions",
        "btn_combine_files": "Combiner les fichiers",
        "btn_divide_file": "Diviser le fichier",
        "btn_cancel_operation": "Annuler l'opération",
        "btn_save_settings": "Sauvegarder les paramètres",
        "btn_export_settings": "Exporter les paramètres",
        "btn_import_settings": "Importer les paramètres",
        "desc_extraction": "Extrait et décompile les fichiers RPA et RPYC du projet sélectionné",
        "desc_generation": "Génère les fichiers de traduction via le SDK Ren'Py", 
        "desc_combination": "Combine plusieurs fichiers de traduction en un seul ou divise un fichier combiné",
        "desc_settings": "Configuration du générateur et gestion des paramètres de projet",
        "placeholder_auto_output": "Auto: translations.rpy dans dossier source",
        "placeholder_auto_folder": "Auto: même dossier que le fichier source",
        "option_delete_rpa": "Supprimer les fichiers RPA après extraction",
        "option_auto_open": "Ouvrir automatiquement les dossiers de résultats",
        "option_show_popup": "Afficher les popups de résultats détaillés",
        "option_excluded_help": "Séparez les noms par des virgules (ex: gui, options, screens)",
        "no_project_selected": "Aucun projet sélectionné",
        "no_sdk_selected": "Aucun SDK sélectionné",
        "error_no_project": "Veuillez sélectionner un projet Ren'Py",
        "error_project_not_exists": "Le projet sélectionné n'existe pas",
        "error_no_game_folder": "Le projet ne contient pas de dossier 'game'",
        "error_no_sdk": "Veuillez sélectionner un SDK Ren'Py",
        "error_invalid_sdk": "SDK Ren'Py invalide:\n{errors}",
        "error_no_source_folder": "Veuillez sélectionner un dossier source",
        "error_source_not_exists": "Le dossier source n'existe pas",
        "error_no_source_file": "Veuillez sélectionner un fichier source", 
        "error_source_file_not_exists": "Le fichier source n'existe pas",
        "error_operation_running": "Une opération est en cours.\nVoulez-vous vraiment fermer ?",
        "error_save_settings": "Erreur sauvegarde: {error}",
        "error_export_settings": "Erreur export: {error}",
        "error_import_settings": "Erreur import: {error}",
        "error_start_extraction": "Erreur démarrage extraction: {error}",
        "error_start_generation": "Erreur démarrage génération: {error}",
        "error_start_combination": "Erreur démarrage combinaison: {error}",
        "error_start_division": "Erreur démarrage division: {error}",
        "error_notification_manager": "Impossible de créer notification_manager: {error}",
        "success_settings_saved": "Paramètres sauvegardés",
        "success_operation_complete": "Opération terminée avec succès !",
        "success_sdk_validated": "SDK validé",
        "success_sdk_with_version": "SDK validé (v{version})",
        "success_settings_exported": "Paramètres exportés", 
        "success_settings_imported": "Paramètres importés",
        "status_operation_complete": "Opération terminée avec succès",
        "status_operation_failed": "Opération échouée", 
        "status_cancelling": "Annulation en cours...",
        "status_cancellation_requested": "Annulation demandée",
        "dialog_select_project": "Sélectionner le dossier du projet Ren'Py",
        "dialog_select_sdk": "Sélectionner le dossier du SDK Ren'Py",
        "dialog_select_source_folder": "Sélectionner le dossier contenant les fichiers de traduction",
        "dialog_select_output_file": "Fichier de sortie combiné",
        "dialog_select_source_file": "Sélectionner le fichier combiné à diviser",
        "dialog_select_output_folder": "Sélectionner le dossier de sortie pour les fichiers divisés",
        "dialog_export_settings": "Exporter les paramètres du projet", 
        "dialog_import_settings": "Importer les paramètres de projet",
        "dialog_closing": "Fermeture",
        "file_type_json": "Fichiers JSON",
        "lang_french": "français",
        "lang_english": "anglais",
        "lang_spanish": "espagnol", 
        "lang_german": "allemand",
        "lang_italian": "italien",
        "lang_portuguese": "portugais",
        "lang_russian": "russe",
        "result_extraction_title": "Résultats de l'extraction",
        "result_generation_title": "Résultats de la génération",
        "result_combination_title": "Résultats de la combinaison", 
        "result_division_title": "Résultats de la division",
        "result_extraction_complete": "Extraction terminée avec succès",
        "result_generation_complete": "Génération de traductions terminée",
        "result_combination_complete": "Combinaison de fichiers terminée",
        "result_division_complete": "Division de fichier terminée",
        "result_rpa_processed": "Fichiers RPA traités:",
        "result_total_extracted": "Total de fichiers extraits: {count}",
        "result_rpyc_converted": "Fichiers RPYC convertis: {count}",
        "result_rpa_deleted": "Fichiers RPA supprimés: {count}",
        "result_translation_files": "Fichiers de traduction générés: {count}",
        "result_output_folder": "Dossier de sortie: {folder}",
        "result_target_language": "Langue cible: {language}",
        "result_files_combined": "Fichiers combinés: {count}",
        "result_files_excluded": "Fichiers exclus: {count}",
        "result_created_file": "Fichier créé: {filename}",
        "result_file_path": "Chemin: {path}",
        "result_source_file": "Fichier source: {filename}",
        "result_files_created": "Fichiers créés: {count}",
        "result_warnings_title": "Avertissements:",
        "result_errors_title": "Erreurs:",
        "result_and_others": "... et {count} autres"
    },
    "temporary_folder": {
        "empty": "Aucun fichier chargé pour ouvrir le dossier temporaire",
        "not_found": "Dossier temporaire non trouvé",
        "error_title": "Erreur dossier temporaire",
        "error_message": "Impossible d'ouvrir le dossier temporaire : {error}"
    },
    "next_file": {
        "not_in_folder_mode": "Vous n'êtes pas en mode dossier",
        "success": "Fichier '{filename}' chargé ({current}/{total}, {remaining} restants)",
        "no_more_files": "Aucun fichier suivant disponible",
        "load_error": "Erreur lors du chargement du fichier suivant",
        "error": "Erreur : {error}"
    },
    "warnings_folder": {
        "empty": "Aucun fichier chargé pour ouvrir le dossier d'avertissements",
        "no_warnings_yet": "Aucun avertissement pour le jeu '{game_name}' pour le moment",
        "empty_folder": "Dossier d'avertissements vide pour '{game_name}' - aucun problème détecté !",
        "opened_with_files": "Dossier d'avertissements ouvert : {count} fichier(s) trouvé(s) pour '{game_name}'",
        "read_error": "Impossible de lire le dossier d'avertissements pour '{game_name}'",
        "not_found": "Dossier d'avertissements non trouvé",
        "error_title": "Erreur dossier avertissements", 
        "error_message": "Impossible d'ouvrir le dossier d'avertissements : {error}"
    },
    "drop": {
        "error_message": "Erreur lors du traitement du fichier glissé-déposé : {error}"
    },
    "folder": {
        "no_valid_files": "Aucun fichier .rpy valide trouvé dans ce dossier",
        "error_title": "Erreur dossier",
        "error_message": "Erreur lors de l'ouverture du dossier : {error}",
        "open_error_message": "Impossible d'ouvrir le dossier {folder_path}"
    },
    "status": {
        "texts_extracted": "{count} textes extraits en {time:.2f}s",
        "reconstruction_completed": "Reconstruction terminée en {time:.2f}s",
        "no_file": "Aucun fichier chargé",
        "ready": "Prêt"
    },
    "clipboard": {
        "save_dialog": {
            "title": "Sauvegarder le contenu",
            "main_title": "Sauvegarder le contenu",
            "description": "Contenu du presse-papier détecté.",
            "content_info": "Informations sur le contenu",
            "content_stats": "{lines} ligne(s), {chars} caractère(s)",
            "save_options": "Options de sauvegarde",
            "option_save": "Sauvegarder ce contenu dans un fichier puis continuer",
            "option_continue": "Continuer sans sauvegarder",
            "option_cancel": "Annuler l'opération",
            "save_file_title": "Sauvegarder le contenu",
            "error_title": "Erreur de sauvegarde",
            "error_message": "Impossible de sauvegarder le fichier :\n{error}",
            "empty": "Presse-papier vide",
            "error": "Erreur lors de l'accès au presse-papier"
        }
    },
    "input_manager": {
        "mode_changed": "Mode {mode_name} activé",
        "drag_drop_unavailable": "Glisser-déposer non disponible sur cette plateforme",
        "error_configure_dnd": "Erreur configuration Glisser-déposer",
        "error_configure_ctrl_v": "Erreur configuration Ctrl+V",
        "error_setup_dnd": "Erreur configuration Glisser-déposer",
        "error_disable_dnd": "Erreur désactivation Glisser-déposer",
        "error_paste": "Erreur lors du collage",
        "ctrl_v_only": "Mode Ctrl+V uniquement actif"
    },
    "file": {
        "not_found_title": "Fichier non trouvé",
        "not_found_message": "Le fichier {filepath} n'existe pas",
        "unsupported_title": "Type de fichier non supporté",
        "content_exists_title": "Contenu existant",
        "content_exists_message": "Du contenu est déjà chargé. Voulez-vous le remplacer ?",
        "error_title": "Erreur fichier",
        "error_message": "Erreur lors du traitement du fichier : {error}",
        "open_title": "Ouvrir un fichier Ren'Py",
        "select_folder_title": "Sélectionner un dossier contenant des fichiers .rpy",
        "unsupported": "Type de fichier non supporté. Seuls les fichiers .rpy sont acceptés."
    },
    "progress": {
        "processing": "Traitement en cours...",
        "extracting": "Extraction en cours...",
        "reconstructing": "Reconstruction en cours...",
        "extracting_ui_characters": "Extraction UI/Personnages en cours..."
    },
    "info": {
        "lines_loaded": "lignes chargées",
        "file_count_single": "1 fichier traité / 1 fichier",
        "file_count_multiple": "{current} fichier{current_s} traité{current_s} / {total} fichiers"
    },
    "extraction": {
        "validation": {
            "file_invalid_path": "Chemin de fichier invalide",
            "file_not_found": "Fichier non trouvé : {filepath}",
            "file_not_file": "Le chemin ne pointe pas vers un fichier : {filepath}",
            "file_too_large": "Fichier trop volumineux ({size_mb:.1f} MB, maximum {max_mb} MB)",
            "file_empty": "Fichier vide",
            "file_size_error": "Erreur de lecture de la taille : {error}",
            "permissions_read": "Permissions de lecture insuffisantes",
            "permissions_check_error": "Erreur de vérification des permissions : {error}",
            "unsupported_extension": "Extension de fichier non supportée",
            "wrong_renpy_structure": "Structure Ren'Py incorrecte",
            "missing_language_folder": "Dossier de langue manquant après tl/",
            "renpy_structure_not_detected": "Structure Ren'Py non détectée",
            "file_empty_content": "Fichier sans contenu",
            "suspicious_content": "Contenu suspect détecté",
            "encoding_error": "Erreur d'encodage du fichier",
            "read_error": "Erreur de lecture : {error}",
            "dangerous_filename": "Caractère dangereux '{char}' dans le nom de fichier",
            "unexpected_error": "Erreur inattendue : {error}"
        },
        "errors": {
            "invalid_content": "Contenu de fichier invalide ou manquant",
            "load_file_error": "Erreur lors du chargement du fichier",
            "extraction_error": "Erreur critique pendant l'extraction",
            "save_files_error": "Erreur lors de la sauvegarde des fichiers",
            "duplicate_management_error": "Erreur dans la gestion des doublons",
            "asterix_detection_error": "Erreur lors de la détection des astérisques",
            "glossary_protection_error": "Erreur lors de la protection du glossaire",
            "code_mapping_error": "Erreur lors de la création du mapping",
            "empty_text_protection_error": "Erreur lors de la protection des textes vides",
            "dialogue_extraction_error": "Erreur lors de l'extraction des dialogues",
            "placeholder_application_error": "Erreur lors de l'application des placeholders"
        },
        "error_title": "Erreur d'extraction",
        "error_occurred": "Une erreur s'est produite lors de l'extraction : {error}",
        "error_status": "Erreur lors de l'extraction",
        "fallbacks": {
            "default_name": "fichier_sans_nom"
        }
    },
    "about": {
        "window_title": "À propos de {version}",
        "main_title": "🎮 {version}",
        "subtitle": "Solution professionnelle de traduction pour les jeux Ren'Py",
        "description": "RenExtract est l'outil de référence pour les traducteurs de jeux visuels développés avec le moteur Ren'Py. Conçu par un traducteur pour les traducteurs, il automatise les tâches répétitives tout en préservant l'intégrité du code source. Sa conception modulaire et son interface intuitive en font l'outil idéal pour des traductions de qualité professionnelle.",
        "features_title": "🌟 Fonctionnalités principales :",
        "features_list": [
            "Extraction intelligente avec reconnaissance contextuelle des dialogues",
            "Protection totale du code Python et des structures Ren'Py",
            "Système de glossaire permanent avec gestion des traductions récurrentes",
            "Validation automatique multi-niveaux (syntaxe, cohérence, intégrité)",
            "Interface moderne avec support drag-and-drop et raccourcis clavier",
            "Architecture multilingue complète (FR/EN/DE avec extensibilité)",
            "Gestion avancée des sauvegardes avec historique complet",
            "Mode dossier pour traitement en lot de projets volumineux",
            "Système d'avertissements intelligents pour optimiser la qualité",
            "Outils experts : nettoyage, cohérence, extraction hybride SDK"
        ],
        "workflow_title": "🔄 Workflow optimisé :",
        "workflow_description": "RenExtract suit un processus en 6 étapes qui garantit la qualité :",
        "workflow_steps": [
            "Configuration de l'environnement et chargement des fichiers sources",
            "Extraction automatique avec filtrage intelligent des textes traduisibles", 
            "Édition dans un environnement sécurisé avec protection du code",
            "Reconstruction avec validation syntaxique et contrôles d'intégrité",
            "Vérification post-traitement avec détection d'anomalies",
            "Enrichissement du glossaire pour optimiser les projets futurs"
        ],
        "links_title": "🔗 Ressources et support :",
        "links": {
            "github": "Dépôt GitHub",
            "github_desc": "Code source, releases et documentation technique",
            "documentation": "Guide utilisateur",
            "documentation_desc": "Documentation complète avec exemples pratiques",
            "bug_report": "Signaler un problème",
            "bug_report_desc": "Rapporter des bugs ou suggérer des améliorations",
            "contact": "Contact développeur",
            "contact_desc": "Support technique et assistance (joignez les logs en mode Debug pour un diagnostic précis)"
        },
        "tech_info_title": "⚙️ Informations techniques",
        "tech_info": {
            "version": "Version : {version}",
            "python": "Python : {python_version}",
            "platform": "Plateforme : {platform}",
            "interface": "Interface : Tkinter moderne avec thèmes adaptatifs",
            "architecture": "Architecture : Modulaire avec séparation des responsabilités",
            "encoding": "Encodage : UTF-8 natif avec support international complet"
        },
        "community_title": "👥 Communauté et contribution :",
        "community_description": "RenExtract est développé en collaboration avec la communauté des traducteurs. Vos retours et suggestions sont essentiels pour améliorer l'outil.",
        "community_features": [
            "Développement ouvert avec prise en compte des retours utilisateurs",
            "Support multilingue extensible selon les besoins communautaires", 
            "Documentation collaborative maintenue par les utilisateurs experts",
            "Système de tickets pour un suivi transparent des améliorations"
        ],
        "close_button": "Fermer",
        "url_copied_title": "URL copiée",
        "url_copied_message": "L'URL suivante a été copiée dans le presse-papier :\n{url}"
    },
    "content": {
        "dnd_available": "Mode Glisser-déposer actif\n\nGlissez et déposez votre fichier .rpy ici pour commencer.\n\nOuverture-Auto: {auto_status}\n\nSolutions alternatives :\n• Utilisez les boutons 'Ouvrir Fichier/Dossier'\n• Basculez vers le mode Ctrl+V",
        "dnd_unavailable": "Glisser-déposer non disponible\n\nLe module tkinterdnd2 n'est pas installé.\n\nOuverture-Auto: {auto_status}\n\nSolutions alternatives :\n• Utilisez les boutons 'Ouvrir Fichier/Dossier'\n• Basculez vers le mode Ctrl+V pour coller du contenu",
        "ctrl_v_mode": "Mode Ctrl+V actif\n\nUtilisez Ctrl+V pour coller du contenu directement dans cette zone.\n\nOuverture-Auto: {auto_status}\n\nSolutions alternatives :\n• Utilisez les boutons 'Ouvrir Fichier/Dossier'\n• Basculez vers le mode Glisser-déposer si disponible"
    },
    "extraction_ui_hybrid": {
        "dialogs": {
            "hybrid_mode_question": "Cette méthode analyse ce que le SDK Ren'Py a déjà traduit,\npuis extrait seulement les textes restants.\n\nAvez-vous déjà utilisé 'renpy translate langue' ?\n\nOUI = Sélectionnez le dossier 'tl' pour éviter les doublons\nNON = Extraction complète (peut inclure des doublons)\n\nRecommandé: Utilisez d'abord le SDK, puis cet outil",
            "hybrid_mode_title": "Extraction Hybride",
            "select_tl_folder": "Sélectionnez le dossier 'tl' (créé par SDK Ren'Py)",
            "unusual_structure_title": "Structure inhabituelle",
            "unusual_structure_message": "Structure de dossier inhabituelle :\n{tl_folder}\n\nStructure attendue: 'tl/' ou 'tl/langue/'\nStructure détectée: '{parent_name}/{folder_name}'\n\nL'analyse hybride continuera quand même.",
            "empty_folder_title": "Dossier vide",
            "empty_folder_message": "Aucun fichier .rpy trouvé dans:\n{tl_folder}\n\nLe SDK Ren'Py n'a peut-être pas encore été utilisé.\nL'extraction sera complète (pas hybride).",
            "folder_validated_title": "Dossier tl validé",
            "folder_validated_message": "Dossier tl analysé !\n\nDossieRéponse : {folder_name}\nFichiers .rpy: {rpy_count}\n\nMode hybride ACTIVÉ",
            "complete_extraction_title": "Mode extraction complète",
            "complete_extraction_message": "Aucun dossier tl sélectionné.\n\nMode: Extraction complète\nRisque de doublons avec les traductions SDK existantes",
            "usage_advice_title": "Conseil d'utilisation",
            "usage_advice_message": "Pour de meilleurs résultats :\n\n1️⃣ Utilisez d'abord: 'renpy translate langue'\n2️⃣ Puis utilisez cet outil pour capturer le reste\n\nMode actuel: Extraction complète",
            "extraction_complete_title": "Extraction terminée",
            "extraction_complete_message": "Aucun nouveau texte restant à extraire !\n\nCauses possibles :\nLe SDK Ren'Py a déjà tout traduit\nAucun texte traduisible supplémentaire trouvé\nFiltrage a exclu les textes techniques\n\nVotre projet semble complet pour la traduction !",
            "safe_texts_detected_title": "Textes sûrs détectés",
            "safe_texts_detected_message": "{count} TEXTES SÛRS DÉTECTÉS\n\nCes textes seront ajoutés automatiquement :\n\n{summary}\n\nVous n'aurez à valider que les textes douteux\nInterface simplifiée à venir...",
            "limitation_applied_title": "Limitation appliquée",
            "limitation_applied_message": "LIMITATION POUR PERFORMANCE\n\n{limited_count} textes sélectionnables limités\nLimite: {max_limit} par catégorie\n\nLes textes auto-sélectionnés ne sont PAS limités\nConseil: Traitez par sous-dossiers pour tout capturer",
            "automatic_extraction_title": "Extraction automatique",
            "automatic_extraction_message": "EXCELLENT ! Tous les textes sont sûrs !\n\n{count} textes sélectionnés automatiquement\nAucune validation manuelle nécessaire\n\nGénération du fichier en cours...",
            "interface_error_title": "Erreur d'interface",
            "interface_error_message": "L'interface a échoué.\n\nErreuRéponse : {error}\n\nSOLUTION AUTOMATIQUE :\nIgnorer les {doubtful_count} textes douteux ?\n\nSeuls les {safe_count} textes sûrs seront extraits",
            "hybrid_success_title": "Extraction hybride réussie",
            "hybrid_success_message": "EXTRACTION HYBRIDE TERMINÉE !\n\nFichier généré: {filename}\nTextes complémentaires extraits: {total_count}\n  Auto-sélectionnés (sûrs): {auto_count}\n  Sélectionnés manuellement: {manual_count}\nCommentaires source: {source_count}/{total_count}\nMode: {mode}\nAnti-doublons: {anti_duplicate}\n\nCes textes complètent les traductions du SDK Ren'Py !",
            "save_error_title": "Erreur de sauvegarde",
            "save_error_message": "Erreur lors de la sauvegarde :\n\n{error}\n\nVérifiez les permissions du dossier.",
            "extraction_error_title": "Erreur d'extraction hybride",
            "extraction_error_message": "Erreur lors de l'extraction hybride :\n\n{error}\n\nConsultez les logs pour plus de détails.\nEssayez le mode extraction complète."
        },
        "file_dialog": {
            "save_title": "Où sauvegarder le fichier .rpy généré ?",
            "file_types": {
                "renpy_script": "Ren'Py script (*.rpy)",
                "all_files": "Tous fichiers (*.*)"
            }
        },
        "messages": {
            "cancelled_by_user": "Sauvegarde annulée par l'utilisateur",
            "no_new_texts_found": "Aucun nouveau texte UI trouvé à extraire",
            "smart_extraction_started": "Extraction UI intelligente démarrée",
            "anti_duplicate_enabled": "Vérification anti-doublons activée avec dossier tl",
            "anti_duplicate_disabled": "Vérification anti-doublons désactivée (pas de dossier tl)",
            "smart_extraction_success": "Extraction UI intelligente terminée : {count} nouveaux textes trouvés",
            "no_duplicates_found": "Aucun doublon détecté - extraction optimisée",
            "duplicates_filtered": "{count} doublons filtrés automatiquement",
            "new_patterns_found": "Nouveaux patterns détectés : {types}",
            "file_auto_opened": "Fichier ouvert automatiquement: {save_path}",
            "auto_open_disabled": "Auto-ouverture désactivée dans les paramètres"
        }
    },
    "extraction_selection_simple": {
        "window": {
            "title": "Sélection des textes à extraire"
        },
        "buttons": {
            "select_all": "Tout cocher",
            "deselect_all": "Tout décocher",
            "validate_selection": "Valider la sélection"
        },
        "messages": {
            "no_selection_warning": "Aucune sélection !\n\nVeuillez sélectionner au moins un texte à extraire."
        },
        "separators": {
            "selectable_characters": "Textes de personnages sélectionnables ({count}) :",
            "selectable_general": "Textes sélectionnables ({count}) :",
            "auto_inputs": "Champs de saisie auto-sélectionnés ({count}) :",
            "auto_characters": "Textes auto-sélectionnés ({count}) :"
        }
    },
    "extraction_ui_folder": {
        "select_folder_title": "Sélectionner le dossier 'game' du projet Ren'Py",
        "no_folder_selected": "Aucun dossier sélectionné pour l'extraction UI/Personnages",
        "invalid_folder": "Dossier invalide : veuillez sélectionner un dossier 'game' valide",
        "notification_success": "Extraction UI/Personnages terminée avec succès",
        "notification_error": "Erreur lors de l'extraction UI/Personnages : {error}",
        "folder_validation": {
            "not_game_folder": "Le dossier sélectionné ne semble pas être un dossier 'game' Ren'Py",
            "no_rpy_files": "Aucun fichier .rpy trouvé dans ce dossier",
            "structure_warning": "Structure de projet Ren'Py non détectée"
        },
        "info": {
            "scanning_folder": "Analyse du dossier en cours...",
            "files_found": "{count} fichiers .rpy trouvés",
            "extraction_started": "Démarrage de l'extraction UI/Personnages",
            "extraction_completed": "Extraction terminée"
        },
        "tips": {
            "game_folder_help": "Sélectionnez le dossier 'game' de votre projet Ren'Py",
            "tl_folder_detection": "Le dossier 'tl' sera automatiquement détecté pour l'anti-doublons",
            "backup_recommendation": "Une sauvegarde sera créée automatiquement"
        }
    },
    "extraction_ui_optimized": {
        "dialogs": {
            "antiduplicate_title": "Anti-doublons",
            "antiduplicate_question": "Avez-vous déjà utilisé le SDK Ren'Py pour générer des traductions ?\n\nOUI = Sélectionnez le dossier 'tl' pour éviter les doublons\nNON = Extraction complète",
            "select_tl_folder": "Sélectionnez le dossier 'tl' (créé par SDK Ren'Py)",
            "empty_folder_title": "Dossier vide",
            "empty_folder_message": "Aucun fichier .rpy trouvé dans le dossier tl sélectionné.",
            "folder_validated_title": "Dossier tl validé",
            "folder_validated_message": "Dossier tl analysé ! {rpy_count} fichiers .rpy trouvés.\n\nMode anti-doublons ACTIVÉ",
            "nothing_new_title": "Rien de nouveau",
            "nothing_new_message": "Aucun nouveau texte à extraire.\n\nTous les textes traduisables semblent déjà traités.",
            "interface_error_title": "Erreur d'interface",
            "interface_fallback_message": "Erreur d'interface : {error}\n\nInclure tous les {total_check} textes douteux automatiquement ?",
            "success_title": "Extraction réussie",
            "success_message": "Extraction optimisée terminée !\n\nFichier : {filename}\nTextes extraits : {total_count}\n  Auto-safe : {auto_count}\n  Sélection manuelle : {manual_count}\nMode : {mode}\nAnti-doublons : {antiduplicate}",
            "save_error_title": "Erreur de sauvegarde",
            "save_error_message": "Erreur lors de la sauvegarde :\n{error}",
            "extraction_error_title": "Erreur d'extraction",
            "extraction_error_message": "Erreur lors de l'extraction optimisée :\n{error}"
        },
        "file_dialog": {
            "save_title": "Sauvegarder le fichier d'extraction",
            "file_types": {
                "renpy_script": "Script Ren'Py (*.rpy)",
                "all_files": "Tous fichiers (*.*)"
            }
        }
    },
    "extract_ui_characters": {
        "file_dialog": {
            "save_title": "Où sauvegarder le fichier .rpy généré ?",
            "file_types": {
                "renpy_script": "Ren'Py script (*.rpy)",
                "all_files": "Tous fichiers (*.*)"
            }
        },
        "messages": {
            "cancelled_by_user": "Sauvegarde annulée par l'utilisateur.",
            "file_auto_opened": "Fichier ouvert automatiquement: {save_path}",
            "auto_open_disabled": "Auto-ouverture désactivée dans les paramètres",
            "no_new_texts_found": "Aucun nouveau texte UI trouvé à extraire",
            "smart_extraction_started": "Extraction UI intelligente démarrée",
            "anti_duplicate_enabled": "Vérification anti-doublons activée avec dossier tl",
            "anti_duplicate_disabled": "Vérification anti-doublons désactivée (pas de dossier tl)"
        },
        "notifications": {
            "extraction_started": "Extraction UI/Personnages en cours...",
            "extraction_success": "Extraction UI/Personnages terminée avec succès",
            "extraction_error": "Erreur lors de l'extraction UI/Personnages: {error}",
            "smart_extraction_success": "Extraction UI intelligente terminée : {count} nouveaux textes trouvés",
            "no_duplicates_found": "Aucun doublon détecté - extraction optimisée",
            "duplicates_filtered": "{count} doublons filtrés automatiquement",
            "new_patterns_found": "Nouveaux patterns détectés : {types}"
        },
        "stats": {
            "files_scanned": "{count} fichiers analysés",
            "existing_translations_found": "{count} traductions existantes trouvées",
            "existing_i18n_found": "{count} textes déjà internationalisés trouvés", 
            "new_texts_extracted": "{count} nouveaux textes extraits",
            "filtering_applied": "Filtrage intelligent appliqué",
            "tl_folder_scanned": "Dossier tl scanné : {path}",
            "game_folder_scanned": "Dossier game scanné : {path}"
        }
    },
    "extraction_ui": {
        "window_title": "Sélection des textes à extraire",
        "section_title": "Textes de type : {origine}",
        "separator_characters_selectionables": "Textes de personnages sélectionnables ({count}) :",
        "separator_selectionables": "Textes sélectionnables ({count}) :",
        "separator_auto_inputs": "Champs de saisie auto-sélectionnés ({count}) :",
        "separator_auto_characters": "Textes auto-sélectionnés ({count}) :",
        "validate_button": "Valider la sélection",
        "separator_ui_elements": "Éléments d'interface auto-sélectionnés ({count}) :",
        "separator_notifications": "Notifications auto-sélectionnées ({count}) :",
        "separator_buttons": "Boutons sélectionnables ({count}) :",
        "separator_text_elements": "Éléments de texte sélectionnables ({count}) :",
        "separator_display_texts": "Textes d'affichage auto-sélectionnés ({count}) :",
        "type_descriptions": {
            "show_text": "Textes affichés avec 'show text' (messages, notifications)",
            "renpy_notify": "Notifications Ren'Py (messages système, alertes)",
            "textbutton": "Boutons de texte (interface utilisateur)",
            "text_element": "Éléments de texte (labels, descriptions)"
        },
        "help_messages": {
            "show_text": "Textes d'affichage généralement destinés au joueur",
            "renpy_notify": "Notifications système - souvent traduisibles", 
            "textbutton": "Textes des boutons - vérifiez la pertinence",
            "text_element": "Éléments de texte divers - filtrage strict appliqué"
        },
        "filtering_info": {
            "anti_duplicate_active": "🛡️ Anti-doublons actif (dossier tl scanné)",
            "anti_duplicate_inactive": "⚠️ Anti-doublons inactif (pas de dossier tl)",
            "smart_filtering": "🧠 Filtrage intelligent appliqué",
            "total_found": "Total trouvé : {count} textes",
            "after_filtering": "Après filtrage : {count} textes"
        }
    },
    "cleanup_handler": {
        "module_unavailable": {
            "title": "Modules de nettoyage indisponibles",
            "message": "Les modules de nettoyage ne sont pas disponibles. Veuillez vérifier l'installation."
        },
        "dialogs": {
            "select_game_folder": "Sélectionnez le dossier 'game' de votre projet Ren'Py",
            "select_sdk_folder": "Sélectionnez le dossier du SDK Ren'Py",
            "confirm_unified_cleanup": "Confirmer le nettoyage",
            "cleaning_success": "Nettoyage terminé avec succès",
            "cleaning_error": "Erreur lors du nettoyage"
        },
        "game_detection": {
            "found_game_subfolder_title": "Dossier 'game' détecté",
            "found_game_subfolder_message": "Vous avez sélectionné '{selected_path}', mais un dossier 'game' a été trouvé dans '{game_path}'. Voulez-vous utiliser ce dossier 'game' ?",
            "invalid_game_folder_title": "Dossier 'game' invalide",
            "invalid_game_folder_message": "Le chemin sélectionné '{path}' ne contient pas de dossier 'game' valide. Veuillez sélectionner le dossier 'game' de votre projet Ren'Py."
        },
        "processing": {
            "workflow_starting": "Démarrage du nettoyage...",
            "select_game_folder": "Sélection du dossier game...",
            "validating_game_folder": "Validation du dossier game...",
            "detecting_sdk": "Détection du SDK Ren'Py...",
            "generating_lint": "Génération du fichier lint...",
            "detecting_tl_folder": "Détection du dossier de traductions...",
            "in_progress": "Nettoyage en cours..."
        },
        "sdk_detection": {
            "auto_detected_title": "SDK Ren'Py détecté automatiquement",
            "auto_detected_message": "SDK détecté : {sdk_name}\nChemin : {sdk_path}\n\nVoulez-vous utiliser ce SDK ?",
            "invalid_sdk_title": "SDK Ren'Py invalide",
            "invalid_sdk_message": "Le SDK sélectionné '{path}' n'est pas valide. Veuillez sélectionner un SDK Ren'Py correct."
        },
        "lint_generation": {
            "failed_title": "Génération du lint échouée",
            "failed_message": "La génération du lint.txt a échoué pour le projet '{game_name}' avec le SDK '{sdk_name}'.\n\nVoulez-vous :\n• OUI : Continuer sans lint (nettoyage par correspondance uniquement)\n• NON : Réessayer avec un autre SDK\n• ANNULER : Abandonner le nettoyage",
            "error_title": "Erreur lors de la génération du lint",
            "error_message": "Erreur lors de la génération du lint pour '{game_name}' :\n{error}\n\nVoulez-vous :\n• OUI : Continuer sans lint\n• NON : Réessayer\n• ANNULER : Abandonner"
        },
        "tl_detection": {
            "not_found_title": "Dossier 'tl' introuvable",
            "not_found_message": "Le dossier de traductions 'tl' n'a pas été trouvé dans '{game_folder}'.\nChemin attendu : {tl_path}\n\nVeuillez vérifier que votre projet contient des traductions."
        },
        "language_scan": {
            "scanning_languages": "Recherche des langues disponibles...",
            "scan_error_title": "Erreur lors du scan des langues",
            "scan_error_message": "Impossible de scanner les langues disponibles :\n{error}\n\nDossier : {folder}",
            "no_languages_title": "Aucune langue trouvée",
            "no_languages_message": "Aucune langue de traduction n'a été trouvée dans le dossier '{folder}'.\n\nVeuillez vérifier que vos traductions sont correctement organisées."
        },
        "language_selection": {
            "dialog_title": "Sélection des langues à nettoyer",
            "dialog_subtitle": "Choisissez les langues que vous souhaitez nettoyer",
            "languages_detected": "{count} langue(s) détectée(s)",
            "language_item_info": "Langue de traduction disponible",
            "tip_bottom": "Sélectionnez au moins une langue pour continuer",
            "no_selection_title": "Aucune langue sélectionnée",
            "no_selection_warning": "Vous devez sélectionner au moins une langue pour effectuer le nettoyage."
        },
        "confirmation": {
            "new_workflow_message": "Projet : {game_name}\nLangues : {languages}\n\nDossier game : {game_folder}\nDossier tl : {tl_folder}"
        },
        "results": {
            "new_workflow_success_message": "Nettoyage terminé pour '{game_name}' !\n\n{languages_processed} langue(s) traitée(s)\n{files_processed} fichier(s) analysé(s)\n{blocks_removed} bloc(s) orphelin(s) supprimé(s)\n\nTemps d'exécution : {execution_time}",
            "error_message": "Erreurs rencontrées :\n{errors}"
        },
        "execution_time": {
            "seconds": "{duration:.1f} seconde(s)",
            "minutes_seconds": "{minutes} minute(s) et {seconds} seconde(s)",
            "hours_minutes": "{hours} heure(s) et {minutes} minute(s)"
        },
        "report": {
            "title": "RAPPORT DE NETTOYAGE - RENEXTRACT",
            "fields": {
                "game": "Projet : {game_name}",
                "date": "Date : {date}",
                "execution_time": "Temps d'exécution : {time}",
                "languages_processed": "Langues traitées : {count}",
                "files_processed": "Fichiers traités : {count}",
                "blocks_removed": "Blocs orphelins supprimés : {count}"
            },
            "sections": {
                "method_summary": "RÉSUMÉ PAR MÉTHODE",
                "lint_cleanup": "• Nettoyage par lint : {count} bloc(s)",
                "string_cleanup": "• Nettoyage par correspondance : {count} bloc(s)",
                "total_cleanup": "• Total supprimé : {count} bloc(s)",
                "language_detail": "DÉTAIL PAR LANGUE",
                "language_files": "Fichiers traités : {count}",
                "language_blocks": "Blocs supprimés : {count}",
                "by_lint": "Via lint : {count}",
                "by_correspondence": "Via correspondance : {count}"
            }
        }
    },
    "backup": {
        "window_title": "Gestionnaire de sauvegardes - {filename}",
        "no_file": "Aucun fichier sélectionné",
        "no_file_message": "Veuillez d'abord charger un fichier avant d'accéder aux sauvegardes.",
        "game_label": "Jeu : {game_name}",
        "auto_backup_info": "Sauvegardes automatiques à chaque extraction",
        "searching": "Recherche des sauvegardes...",
        "refreshing": "Actualisation...",
        "no_backups_found": "Aucune sauvegarde trouvée pour le jeu '{game_name}'.\n\nLes sauvegardes sont créées automatiquement lors des extractions.",
        "created_label": "Créée le :",
        "size_label": "Taille :",
        "age_label": "Ancienneté :",
        "restore_button": "Restaurer",
        "delete_button": "Supprimer",
        "most_recent_badge": "Plus récente",
        "safety_badge": "Sauvegarde sécurité",
        "refresh_button": "Actualiser",
        "close_button": "Fermer",
        "restore_confirm_title": "Confirmer la restauration",
        "restore_confirm_message": "Restaurer la sauvegarde :\n'{name}'\n\nJeu : {game}\nCréée le : {created}\n\nCette action remplacera le fichier actuel.",
        "restore_success_title": "Restauration réussie",
        "restore_success_message": "Sauvegarde '{name}' restaurée avec succès.\n\nJeu : {game}\nCréée le : {created}\n\nSouhaitez-vous supprimer cette sauvegarde ?",
        "restore_error_title": "Erreur de restauration",
        "restore_error_message": "Impossible de restaurer '{name}' :\n{error}",
        "restore_critical_error_title": "Erreur critique",
        "restore_critical_error_message": "Erreur critique lors de la restauration :\n{error}",
        "delete_confirm_title": "Confirmer la suppression", 
        "delete_confirm_message": "Supprimer définitivement la sauvegarde :\n'{name}'\n\nJeu : {game}\nCréée le : {created}\nTaille : {size:.2f} MB\n\nCette action est irréversible.",
        "delete_success_title": "Suppression réussie",
        "delete_success_message": "Sauvegarde '{name}' supprimée avec succès.",
        "delete_error_title": "Erreur de suppression",
        "delete_error_message": "Impossible de supprimer '{name}' :\n{error}",
        "errors": {
            "load_error": "Erreur de chargement",
            "load_error_message": "Erreur lors du chargement des sauvegardes pour {filepath} : {error}"
        }
    },
    "single_instance": {
        "already_running_title": "Application déjà lancée",
        "already_running_message": "Une instance de cette application est déjà en cours d'exécution.\n\nVeuillez fermer l'instance existante avant d'en lancer une nouvelle."
    },
    "file_types": {
        "text_files": "Fichier texte (*.txt)",
        "all_files": "Tous fichiers (*.*)"
    },
    "export": {
        "glossary_header": "Glossaire RenExtract - Exporté le",
        "glossary_format": "Format : Original => Traduction"
    },
    "titles": {
        "error_title": "Erreur",
        "warning_title": "Avertissement", 
        "info_title": "Information",
        "success_title": "Succès",
        "confirm_title": "Confirmation",
        "validation_success": "Validation réussie",
        "validation_failed": "Validation échouée"
    },
    "save_mode": {
        "title": "💾 Mode de Sauvegarde",
        "description": "Comment voulez-vous sauvegarder le fichier traduit ?",
        "new_file": {
            "title": "📄 Nouveau Fichier",
            "description": "Crée un nouveau fichier avec le suffixe '_translated'"
        },
        "overwrite": {
            "title": "🔄 Écraser l'Original",
            "description": "Écrase directement le fichier original (sauvegarde automatique)"
        },
        "cancel": "❌ Annuler"
    },
    "reset": {
        "confirm_title": "Confirmer la Réinitialisation",
        "confirm_message": "Êtes-vous sûr de vouloir réinitialiser l'application ?\n\n📄 Fichier actuel : {file_count} lignes\n\n⚠️ Cette action va :\n• Vider la zone de texte\n• Réinitialiser tous les états\n• Conserver les glossaires et les sauvegardes",
        "confirm_complete": "Êtes-vous sûr de vouloir réinitialiser complètement l'application ?\n\n⚠️ Cela supprimera toutes les données (glossaire, configuration, etc.)",
        "complete_success": "Application réinitialisée avec succès !",
        "error_occurred": "Erreur lors de la réinitialisation : {error}",
        "error_title": "Erreur de Réinitialisation"
    },
    "interface": {
        "progress": {
            "title": "Traitement en cours...",
            "processing": "Traitement en cours...",
            "initializing": "Initialisation..."
        },
        "status_bar": {
            "separator": "|"
        },
        "validation": {
            "dialog_title": "Résultats de validation"
        }
    },
    "notification_manager": {
        "fallback": {
            "title": "Information",
            "unknown_type": "Type de notification inconnu",
            "priority_too_low": "Toast ignoré (priorité {priority} trop faible)"
        },
        "errors": {
            "notify_error": "Erreur dans notify()",
            "handle_toast_error": "Erreur _handle_toast()",
            "show_toast_immediate_error": "Erreur _show_toast_immediate()",
            "handle_toast_priority_error": "Erreur _handle_toast_priority()",
            "create_toast_window_error": "Erreur _create_toast_window()",
            "setup_toast_events_error": "Erreur _setup_toast_events()",
            "calculate_toast_position_error": "Erreur _calculate_toast_position()",
            "reposition_all_toasts_error": "Erreur _reposition_all_toasts()",
            "reposition_individual_error": "Erreur repositionnement toast individuel",
            "auto_close_error": "Erreur fermeture automatique toast",
            "remove_toast_error": "Erreur _remove_toast()",
            "handle_modal_error": "Erreur _handle_modal()",
            "handle_confirm_error": "Erreur _handle_confirm()",
            "handle_status_error": "Erreur _handle_status()",
            "cleanup_error": "Erreur cleanup NotificationManager",
            "status_update_impossible": "Impossible de mettre à jour le statut"
        }
    },
    "coherence": {
        "title": "Validation de la Cohérence",
        "report_title": "RAPPORT DE COHÉRENCE RENEXTRACT",
        "folder_name": "tl_folder_coherence",
        "warning_not_tl_subfolder": "Le dossier sélectionné n'est pas un sous-dossier de 'tl'",
        "no_issues_detected": "Aucun problème de cohérence détecté",
        "issues_detected": "{count} problème(s) de cohérence détecté(s)",
        "select_tl_subfolder": "Sélectionnez un sous-dossier 'tl'",
        "error_not_tl_subfolder": "Le dossier sélectionné n'est pas un sous-dossier 'tl'",
        "check_done_with_issues": "Vérification terminée - Problèmes détectés (voir rapport)",
        "check_done_no_issues": "Vérification terminée - Aucun problème détecté",
        "analyzed_folder": "Dossier Analysé : {folder}",
        "date_format": "Date : {date}",
        "variables_section": "Variables incohérentes",
        "balises_section": "Balises incohérentes", 
        "placeholders_section": "Placeholders incohérents",
        "file_line": "Fichier : {file}",
        "line_problem": "Ligne {line} : {type} incohérente : {missing}",
        "old_line": "  ANCIEN (ligne {line}) : {content}",
        "new_line": "  NOUVEAU : {content}",
        "summary_section": "RÉSUMÉ",
        "issues_count": "{count} problème(s) de {type}",
        "issues_count_format": "{count} problème(s) de {type}",
        "log_report_created": "Rapport de cohérence créé : {count} incohérence(s) trouvée(s) - {path}",
        "log_no_issues": "Aucune incohérence trouvée dans le dossier TL",
        "game": "Jeu",
        "analyzed_file": "Fichier Analysé",
        "date": "Date",
        "no_issues_detected": "Aucun problème de cohérence détecté !",
        "detailed_message": "Détails des problèmes détectés :\n{details}",
        "error_title": "Erreur de Validation",
        "error_occurred": "Erreur lors de la validation : {error}",
        "summary": "RÉSUMÉ",
        "warning_note": "⚠️ Note : Ces problèmes peuvent affecter le bon fonctionnement du script.",
        "warning_not_tl_subfolder": "Avertissement : le dossier sélectionné n'est pas un sous-dossier 'tl'. Des incohérences non pertinentes pourraient être détectées.",
        "tip_note": "💡 Astuce : Corrigez ces problèmes avant de reconstruire le fichier.",
        "line_prefix": "Ligne {line}",
        "old_line_prefix": "  ANCIEN (ligne {line})",
        "new_prefix": "  NOUVEAU",
        "analysis": {
            "file_not_found": "Fichier non trouvé : {filepath}",
            "system_error": "Erreur système : {error}"
        },
        "validation": {
            "invalid_folder_title": "Dossier invalide",
            "game_folder_not_allowed": "Le dossier 'game' ne peut pas être analysé directement.\n\nVeuillez sélectionner un sous-dossier de traduction dans 'game/tl/[langue]/'.",
            "must_be_tl_subfolder": "Le dossier sélectionné doit être un dossier de traduction.\n\nVeuillez sélectionner un dossier dans 'game/tl/[langue]/' ou un de ses sous-dossiers.",
            "no_files_title": "Aucun fichier trouvé",
            "no_rpy_files_found": "Aucun fichier .rpy trouvé dans le dossier sélectionné.\n\nVeuillez sélectionner un dossier contenant des fichiers de traduction."
        },
        "issues": {
            "missing_old": "Ligne NEW sans OLD correspondant",
            "analysis_error": "Erreur d'analyse : {error}"
        },
        "warning_file": {
            "unique_file_report": "RAPPORT FICHIER UNIQUE",
            "game": "Jeu",
            "analyzed_file": "Fichier analysé",
            "date": "Date",
            "issues_detected": "Problèmes détectés : {count}",
            "line_prefix": "Ligne {line}",
            "old_prefix": "ANCIEN",
            "new_prefix": "NOUVEAU",
            "summary": "RÉSUMÉ",
            "issues_count_format": "• {count} problème(s) de type {type}",
            "warning_note": "⚠️ Remarque : Ces problèmes peuvent affecter le bon fonctionnement du script.",
            "tip_note": "💡 Astuce : Corrigez ces problèmes avant de reconstruire le fichier."
        },
        "report": {
            "title": "RAPPORT DE COHÉRENCE RENEXTRACT",
            "analyzed_folder": "Dossier analysé",
            "date": "Date",
            "problems_detected": "problèmes détectés",
            "summary_title": "RÉSUMÉ DÉTAILLÉ",
            "total_problems": "Total des problèmes détectés : {total}",
            "technical_note": "Note technique : Les variables avec fonctions de traduction (ex: [TEMP1!t], [VAR!u]) ont été normalisées pour la comparaison.",
            "technical_explanation": "Si vous voyez [TEMP1!t] dans vos fichiers mais que le rapport indique [TEMP1], c'est normal - les fonctions !t, !u, !l, !c sont ignorées."
        },
        "issue_types": {
            "TAG_MISMATCH": "Balises {} incohérentes",
            "VARIABLE_MISMATCH": "Variables [] incohérentes",
            "PLACEHOLDER_MISMATCH": "Placeholders () incohérents",
            "MALFORMED_PLACEHOLDER": "Placeholder malformé",
            "ORPHAN_TAG": "Balise orpheline",
            "SPECIAL_CODE_MISMATCH": "Codes spéciaux incohérents",
            "QUOTE_COUNT_MISMATCH": "Nombre de guillemets différent",
            "MISSING_OLD": "Ligne ANCIENNE manquante",
            "FILE_ERROR": "Erreur de fichier",
            "SYSTEM_ERROR": "Erreur système",
            "ANALYSIS_ERROR": "Erreur d'analyse",
            "UNRESTORED_PLACEHOLDER": "Placeholders non restaurés",
            "variables_inconsistent": "Variables incohérentes",
            "tags_inconsistent": "Balises incohérentes",
            "placeholders_inconsistent": "Placeholders incohérents",
            "quote_problems": "Problèmes de guillemets",
            "other_problems": "Autres problèmes"
        },
        "descriptions": {
            "tag_mismatch": "Balises ouvrantes/fermantes incohérentes : {old_tags} vs {new_tags}",
            "variable_mismatch": "Variables incohérentes : {old_vars} vs {new_vars}",
            "placeholder_mismatch": "Placeholders incohérents : {old_placeholders} vs {new_placeholders}",
            "malformed_placeholder": "Placeholder malformé détecté : {malformed}",
            "orphan_tag": "Balise orpheline : {orphan_open} sans {orphan_close}",
            "special_code_mismatch": "Code spécial incohérent : {old_special} vs {new_special}",
            "unrestored_placeholder": "Placeholder(s) non restauré(s) détecté(s) : {placeholders}",
            "tags_inconsistent": "Balises incohérentes",
            "variables_inconsistent": "Variables incohérentes",
            "placeholders_inconsistent": "Placeholders incohérents",
            "placeholders_not_restored": "Placeholders non restaurés",
            "placeholders_malformed": "Placeholders malformés",
            "orphan_tags": "Balises orphelines",
            "special_codes_inconsistent": "Codes spéciaux incohérents",
            "missing_old": "Ligne OLD manquante",
            "quote_count_different": "Nombre de guillemets différent",
            "expected": "Attendu",
            "present": "Présent",
            "automatic_replacement": "remplacement automatique",
            "format_xx": "format (XX)",
            "closed_tags": "balises fermées complètes",
            "unclosed_tags": "balises non fermées",
            "old_new_pair": "paire OLD/NEW",
            "isolated_new": "NEW isolé",
            "unspecified_problem": "Problème non spécifié",
            "description_error": "Erreur de description"
        },
        "quote_mismatch": {
            "auto_corrected": "Nombre de guillemets différent (ANCIEN : {old_count}, NOUVEAU : {new_count}) - ✅ AUTO-CORRIGÉ",
            "difference_detected": "Nombre de guillemets différent (ANCIEN : {old_count}, NOUVEAU : {new_count}) - ⚠️ Différence détectée"
        }
    },
    "tutorial": {
        "title": "Guide Complet - {version}",
        "subtitle": "Maîtrisez tous les aspects de RenExtract",
        "express_title": "Guide Express - {version}",
        "express_subtitle": "L'essentiel en quelques minutes",
        "non_blocking_notice": "Cette fenêtre est non-bloquante : vous pouvez utiliser l'application en parallèle !",
        "understood_button": "J'ai compris !",
        "collapse_all_button": "Tout Replier",
        "expand_all_button": "Tout Déplier",
        "content": {
            "guide_complet": {
                "workflow": {
                    "title": "Flux de travail recommandé",
                    "overview": "RenExtract suit un processus logique en 6 étapes pour garantir une traduction de qualité :",
                    "step_1": "PRÉPARATION : Configurez votre environnement (langue, thème) et chargez votre fichier",
                    "step_2": "EXTRACTION : Lancez l'extraction pour identifier automatiquement les textes traduisibles",
                    "step_3": "TRADUCTION : Éditez le fichier temporaire généré avec vos traductions",
                    "step_4": "RECONSTRUCTION : Reconstruisez le fichier final intégrant vos modifications",
                    "step_5": "VÉRIFICATION : Revérifier le dernier fichier pour détecter d'éventuelles incohérences oubliée",
                    "step_6": "ENRICHISSEMENT : Ajoutez vos traductions récurrentes au glossaire pour les prochaines fois",
                    "cycle_note": "Ce processus peut être répété pour chaque fichier ou utilisé en mode dossier pour traiter plusieurs fichiers séquentiellement."
                },
                "file_organization": {
                    "title": "Organisation des fichiers et dossiers",
                    "overview": "RenExtract organise automatiquement vos fichiers dans une structure claire :",
                    "temp_folder": "Dossier Temporaires",
                    "temp_structure": "• dialogue.txt : Textes principaux à traduire\n• autre.txt : Expressions entre astérisques\n• empty.txt : Textes vides détectés\n• mapping files : Correspondances techniques",
                    "warnings_folder": "Dossier Avertissements",
                    "warnings_content": "• Erreurs de syntaxe\n• Incohérences de traduction\n• Caractères problématiques\n• Suggestions d'amélioration",
                    "other_folders": "Autres dossiers",
                    "translated_folder": "Fichiers traduits : Dans le même emplacement que l'original",
                    "backups_folder": "Sauvegardes : Organisées automatiquement par jeu",
                    "configs_folder": "Configuration : Glossaire et paramètres permanents",
                    "access_tip": "Utilisez les boutons dédiés pour accéder rapidement à chaque dossier."
                },
                "modes_concepts": {
                    "title": "Modes et concepts avancés",
                    "overview": "Comprenez les différents modes et concepts pour optimiser votre utilisation :",
                    "input_modes": "Modes d'entrée",
                    "drag_drop_mode": "Glisser-déposer : Idéal pour traiter des fichiers depuis l'explorateur",
                    "ctrl_v_mode": "Ctrl+V : Parfait pour coller des extraits de code Ren'Py à analyser",
                    "folder_mode": "Mode dossier",
                    "folder_processing": "Traitement séquentiel : Un fichier à la fois avec sauvegarde automatique",
                    "folder_navigation": "Navigation : Bouton 'Fichier Suivant' pour passer au suivant",
                    "folder_progress": "Suivi : Affichage 'X fichiers traités / Y fichiers'",
                    "validation_system": "Système de validation",
                    "syntax_check": "Vérification syntaxe Ren'Py avant/après traitement",
                    "coherence_check": "Détection des incohérences de variables, balises, placeholders",
                    "quote_correction": "Correction automatique des guillemets mal équilibrés",
                    "glossary_concept": "Concept du glossaire",
                    "glossary_purpose": "Remplace automatiquement les termes récurrents lors de l'extraction",
                    "glossary_protection": "Protège vos traductions avec des placeholders temporaires",
                    "glossary_restoration": "Restaure les traductions lors de la reconstruction"
                },
                "advanced_features": {
                    "title": "Fonctionnalités avancées",
                    "overview": "Exploitez toute la puissance de RenExtract avec ces fonctionnalités expertes :",
                    "auto_backup": "Sauvegardes automatiques",
                    "backup_timing": "Créées automatiquement avant chaque extraction/reconstruction",
                    "backup_organization": "Organisées par jeu et horodatées pour faciliter la gestion",
                    "backup_restoration": "Restauration en un clic depuis le gestionnaire",
                    "coherence_validation": "Validation de cohérence",
                    "folder_analysis": "Analyse complète d'un dossier de traduction",
                    "issue_detection": "Détection des variables/balises/placeholders incohérents",
                    "detailed_reports": "Rapports détaillés avec localisation précise des problèmes",
                    "cleanup_system": "Système de nettoyage",
                    "orphan_removal": "Suppression des blocs de traduction orphelins",
                    "lint_integration": "Intégration avec lint.txt du SDK Ren'Py",
                    "hybrid_extraction": "Extraction hybride (Oublie SDK Ren'Py)",
                    "sdk_complement": "Complète le travail du SDK officiel Ren'Py",
                    "missed_texts": "Capture les textes UI/interface oubliés par le SDK",
                    "anti_duplicate": "Évite les doublons avec les traductions existantes"
                },
                "optimization_tips": {
                    "title": "Conseils d'optimisation",
                    "overview": "Optimisez votre workflow et la qualité de vos traductions :",
                    "workflow_efficiency": "Efficacité du workflow",
                    "batch_processing": "Utilisez le mode dossier pour traiter plusieurs fichiers d'affilée",
                    "glossary_building": "Construisez votre glossaire progressivement pour gagner du temps",
                    "auto_open_usage": "Activez l'auto-ouverture pour un workflow fluide",
                    "quality_assurance": "Assurance qualité",
                    "systematic_verification": "Rechargez systématiquement après reconstruction",
                    "warnings_monitoring": "Consultez régulièrement les avertissements",
                    "coherence_checks": "Validez la cohérence avant finalisation",
                    "debug_usage": "Utilisation du debug",
                    "when_to_enable": "Activez uniquement en cas de problème (ralentit l'exécution)",
                    "log_analysis": "Analysez les logs détaillés pour identifier les causes",
                    "performance_note": "Désactivez après résolution pour retrouver la vitesse normale",
                    "backup_strategy": "Stratégie de sauvegarde",
                    "regular_exports": "Exportez régulièrement votre glossaire",
                    "project_organization": "Organisez vos projets par dossiers séparés",
                    "backup_verification": "Vérifiez occasionnellement l'intégrité de vos sauvegardes"
                },
                "troubleshooting": {
                    "title": "Résolution de problèmes courants",
                    "overview": "Solutions aux problèmes les plus fréquents rencontrés :",
                    "extraction_issues": "Problèmes d'extraction",
                    "no_texts_found": "'Aucun texte trouvé' : Vérifiez que le fichier contient des dialogues",
                    "encoding_errors": "Erreurs d'encodage : Assurez-vous que le fichier est en UTF-8",
                    "large_files": "Fichiers trop volumineux : Divisez en plusieurs parties",
                    "reconstruction_issues": "Problèmes de reconstruction",
                    "validation_failures": "Échec de validation : Consultez les avertissements détaillés",
                    "syntax_errors": "Erreurs de syntaxe : Vérifiez les balises et variables modifiées",
                    "file_corruption": "Fichier corrompu : Restaurez depuis une sauvegarde",
                    "performance_issues": "Problèmes de performance",
                    "slow_processing": "Traitement lent : Désactivez le mode debug",
                    "memory_usage": "Forte utilisation mémoire : Traitez par petits lots",
                    "crash_recovery": "Plantages : Vérifiez les logs et redémarrez l'application",
                    "interface_issues": "Problèmes d'interface",
                    "display_problems": "Problèmes d'affichage : Changez de thème",
                    "language_issues": "Problèmes de langue : Redémarrez après changement",
                    "button_unresponsive": "Boutons non réactifs : Attendez la fin du traitement en cours"
                },
                "best_practices": {
                    "title": "Meilleures pratiques",
                    "overview": "Adoptez les meilleures pratiques pour des traductions professionnelles :",
                    "project_setup": "Organisation de projet",
                    "folder_structure": "Créez une structure de dossiers claire pour chaque jeu",
                    "naming_convention": "Utilisez des noms de fichiers explicites",
                    "version_control": "Gardez une trace des versions de vos traductions",
                    "translation_workflow": "Workflow de traduction",
                    "consistency_check": "Maintenez la cohérence terminologique",
                    "context_preservation": "Préservez le contexte original dans vos traductions",
                    "character_limits": "Respectez les contraintes d'espace de l'interface",
                    "quality_control": "Contrôle qualité",
                    "systematic_testing": "Testez systématiquement vos traductions dans le jeu",
                    "peer_review": "Faites relire vos traductions par d'autres personnes",
                    "iterative_improvement": "Améliorez progressivement vos traductions",
                    "collaboration": "Collaboration",
                    "glossary_sharing": "Partagez vos glossaires avec votre équipe",
                    "standard_procedures": "Établissez des procédures standard",
                    "communication": "Communiquez régulièrement sur l'avancement"
                }
            }
        }
    },
    "sections_guide": {
        "title": "Guide des Sections - RenExtract",
        "subtitle": "Comprendre l'organisation de l'interface par onglets",
        "notice": "Navigation interactive : découvrez les fonctions tout en utilisant l'interface !",
        "header": {
        "title": "En-tête - Contrôles généraux",
        "description": "Zone supérieure contenant les contrôles globaux de l'application et les informations principales.",
        "language": "Langue : Change la langue de l'interface (FR/EN/DE) avec renommage automatique des dossiers",
        "theme": "Thème : Bascule entre le mode clair et le mode sombre",
        "debug": "Debug : Active/désactive le mode débogage pour plus d'informations détaillées",
        "reset": "Réinitialiser : Remet l'application à zéro (efface tous les fichiers temporaires)",
        "about": "À propos : Informations sur l'application, version et crédits",
        "quit": "Quitter : Ferme l'application proprement"
        },
        "entree": {
        "title": "Entrée - Charger vos fichiers",
        "description": "Point de départ : importez vos fichiers Ren'Py pour commencer le travail de traduction.",
        "open_file": "Ouvrir fichier : Sélectionne un fichier .rpy spécifique",
        "open_folder": "Ouvrir dossier : Traite séquentiellement les fichiers d'un dossier",
        "next_file": "Fichier suivant : Passe au fichier suivant en mode dossier",
        "drag_drop": "Glisser-déposer : Mode Glisser-déposer pour importer facilement",
        "ctrl_v": "Ctrl+V : Mode collage rapide depuis une partie d'un fichier .rpy"
        },
        "actions": {
        "title": "Actions - Opérations principales",
        "description": "Les actions essentielles pour extraire et reconstruire vos traductions.",
        "extract": "Extraire : Lance l'extraction des textes depuis les fichiers Ren'Py",
        "reconstruct": "Reconstruire : Reconstruit un fichier .rpy à partir des traductions",
        "reload": "Revérifier : Recharge le dernier fichier traité pour révérifier les incohérences"
        },
        "outils": {
        "title": "Outils - Utilitaires et configuration",
        "description": "Outils pratiques pour gérer vos traductions et configurer l'application.",
        "warnings": "Avertissements : Ouvre le dossier 01_Avertissements si présence d'un fichier",
        "auto_open": "Auto-ouverture : Active/désactive l'ouverture automatique des fichiers",
        "temporary": "Temporaire : Ouvre le dossier 03_Temporaires si présence d'un fichier",
        "glossary": "Glossaire : Gestionnaire de glossaire pour la cohérence",
        "backups": "Sauvegardes : Gère les sauvegardes automatiques"
        },
        "avancee": {
        "title": "Avancée - Fonctions expertes",
        "description": "Outils avancés pour utilisateurs expérimentés. Nécessitent une bonne compréhension de Ren'Py.",
        "check_coherence": "Vérifier cohérence : Analyse les incohérences sur un dossier complet",
        "cleanup": "Nettoyer : Nettoie les fichiers de traduction de leurs lignes orphelines (Ancienne traduction)",
        "extract_ui": "Oublie SDK Ren'Py : Extraction spécialisée des lignes oubliées par le SDK de Ren'Py"
        },
        "aide": {
        "title": "Aide - Documentation et support",
        "description": "Accès complet à la documentation et aux guides d'utilisation.",
        "sections_guide": "Guide des Sections : Ce guide que vous lisez actuellement",
        "complete_guide": "Guide Complet : Documentation détaillée de toutes les fonctionnalités",
        "express_guide": "Guide Express : Guide de démarrage rapide",
        "process": "Processus : Détails techniques sur les processus d'exécution",
        "faq": "FAQ : Questions fréquentes et résolution de problèmes"
        },
        "workflow": {
        "title": "Workflow recommandé",
        "description": "Suivez ce processus optimal pour une traduction efficace :",
        "recommended_steps": "Étapes recommandées",
        "step_1": "EN-TÊTE : Configurez la langue, le thème selon vos préférences",
        "step_2": "ENTRÉE : Chargez vos fichiers (glisser-déposer ou boutons)",
        "step_3": "ACTIONS : Extrayez les textes, modifiez-les, puis reconstruisez",
        "step_4": "OUTILS : Utilisez les utilitaires selon vos besoins",
        "step_5": "AVANCÉE : Fonctions expertes si nécessaire"
        },
        "buttons_available": "Boutons disponibles"
    },
    "express_guide": {
        "title": "Guide Express - RenExtract",
        "subtitle": "L'essentiel en quelques minutes",
        "notice": "Guide rapide non-bloquant : explorez RenExtract en parallèle !",
        
        "workflow": {
            "title": "Processus rapide",
            "description": "Le workflow essentiel en 4 étapes simples :",
            "step_1": "Chargez votre fichier (.rpy ou dossier)",
            "step_2": "Extrayez les textes traduisibles", 
            "step_3": "Traduisez dans le fichier temporaire généré",
            "step_4": "Reconstruisez le fichier final"
        },
        
        "interface_basics": {
            "title": "Interface essentielle",
            "description": "Les éléments clés à connaître :",
            "tabs_organization": "Interface organisée en 5 onglets thématiques",
            "drag_drop_info": "Glissez-déposez vos fichiers .rpy directement",
            "ctrl_v_info": "Utilisez Ctrl+V pour coller du contenu de script",
            "auto_open_tip": "Activez l'auto-ouverture pour un workflow fluide"
        },
        
        "essential_features": {
            "title": "Fonctionnalités essentielles",
            "description": "Ce qu'il faut retenir pour bien commencer :",
            "glossary_brief": "Glossaire permanent pour vos traductions récurrentes",
            "validation_brief": "Validation automatique pour éviter les erreurs",
            "backups_brief": "Sauvegardes automatiques à chaque étape",
            "warnings_brief": "Système d'avertissements pour améliorer vos traductions"
        },
        
        "quick_tips": {
            "title": "Conseils rapides",
            "description": "Les tips essentiels pour bien démarrer :",
            "start_simple": "Commencez par un fichier simple pour vous familiariser",
            "check_warnings": "Consultez toujours les avertissements après extraction",
            "use_reload": "Utilisez 'Revérifier' pour vérifier vos traductions",
            "build_glossary": "Construisez votre glossaire au fur et à mesure",
            "folder_mode": "Utilisez le mode dossier pour traiter plusieurs fichiers"
        },
        
        "next_steps": {
            "title": "Pour aller plus loin",
            "description": "Une fois les bases maîtrisées :",
            "complete_guide": "Consultez le Guide Complet pour les fonctionnalités avancées",
            "sections_guide": "Explorez le Guide des Sections pour comprendre tous les boutons",
            "advanced_features": "Découvrez les fonctions expertes dans l'onglet Avancée"
        }
    },
    "help_specialized": {
        "execution_process": {
            "title": "Processus d'exécution détaillé",
            "subtitle": "Comprendre le fonctionnement interne de RenExtract",
            "notice": "Guide technique non-bloquant : approfondissez vos connaissances en pratiquant !",
            "understood_button": "Processus compris !",
            "sections": {
                "objective": {
                    "title": "Objectif du processus",
                    "content": {
                        "0": "RenExtract automatise l'extraction et la reconstruction de scripts Ren'Py pour la traduction.",
                        "1": "Le processus préserve l'intégrité du code tout en isolant les textes traduisibles.",
                        "2": "Chaque étape est validée pour garantir la compatibilité avec le moteur Ren'Py."
                    }
                },
                "workflow": {
                    "title": "Étapes du traitement",
                    "content": {
                        "0": "• Phase 1 : Analyse syntaxique du fichier source",
                        "1": "• Phase 2 : Identification des patterns traduisibles",
                        "2": "• Phase 3 : Extraction dans un fichier temporaire structuré",
                        "3": "• Phase 4 : Intégration des traductions",
                        "4": "• Phase 5 : Reconstruction avec validation syntaxique",
                        "5": "• Phase 6 : Génération du fichier final et sauvegarde"
                    }
                },
                "protection": {
                    "title": "Protection du code",
                    "content": {
                        "0": "• Les blocs de code Python sont préservés intégralement",
                        "1": "• Les variables, balises, etc... restent intactes",
                        "2": "• Les commentaires techniques sont conservés",
                        "3": "• Seuls les textes destinés au joueur sont extraits"
                    }
                },
                "validation": {
                    "title": "Contrôles qualité",
                    "content": {
                        "0": "• Vérification de la syntaxe Ren'Py avant et après traitement",
                        "1": "• Contrôle de cohérence des structures de dialogue",
                        "2": "• Validation des patterns de substitution",
                        "3": "• Détection des caractères problématiques",
                        "4": "• Rapport d'erreurs détaillé en cas de problème"
                    }
                },
                "tips": {
                    "title": "Conseils d'optimisation",
                    "content": {
                        "0": "• Utilisez le glossaire pour les traductions récurrentes",
                        "1": "• Vérifiez toujours le fichier reconstruit avant utilisation",
                        "2": "• Utilisez la sauvegarde générée lors de l'extractiion si un problème est détecté",
                        "3": "• Activez le mode Debug pour plus de détails sur le processus",
                        "4": "• Consultez le dossier 01_Avertissements pour identifier les améliorations possibles"
                    }
                }
            }
        },
        "faq": {
            "title": "Questions Fréquentes",
            "subtitle": "Réponses aux questions courantes sur RenExtract",
            "notice": "Aide interactive non-bloquante : trouvez vos réponses tout en explorant !",
            "understood_button": "Tout est clair !",
            "sections": {
                "questions": {
                "title": "Questions fréquentes",
                "content": {
                    "0": "Question : Où sont sauvegardés mes fichiers traduits ?",
                    "1": "• Réponse : Dans le dossier d'origine où vous avez chargé le fichier.",
                    "2": "Question : Que faire si la validation échoue ?",
                    "3": "• Réponse : Vérifiez les warnings et corrigez les erreurs de syntaxe signalées.",
                    "4": "Question : Comment sauvegarder mon glossaire ?",
                    "5": "• Réponse : Utilisez les boutons Exporter/Importer dans le gestionnaire de glossaire.",
                    "6": "Question : L'application plante lors du traitement ?",
                    "7": "• Réponse : Activez le mode Debug et consultez les logs pour identifier le problème. Vous pouvez envoyer les logs au Dev à l'aide du contact dans la fenêtre 'A Propos'",
                    "8": "Question : Puis-je traiter plusieurs fichiers en même temps ?",
                    "9": "• Réponse : Non, mais vous pouvez utiliser 'Ouvrir Dossier' pour traiter tous les .rpy d'un répertoire."
                }
            },
                "tips": {
                "title": "Conseils et astuces",
                "content": {
                    "0": "• Sauvegardez régulièrement votre glossaire pour réutiliser vos traductions",
                    "1": "• Le bouton Réinitialiser efface tout - utilisez-le pour repartir à zéro",
                    "2": "• Les sauvegardes automatiques vous permettent de revenir en arrière",
                    "3": "• Consultez le dossier 01_Avertissements pour améliorer vos traductions",
                    "4": "• Le mode Debug affiche plus d'informations mais ralentit l'exécution"
                    }
                }
            }
        }
    },
    "reload": {
        "no_file": "Aucun fichier à revérifier",
        "success": "Aucune nouvelle incohérence détecter"
    },
    "app_controller": {
        "file_operations": {
            "file_loaded_success": "Fichier {filename} chargé avec succès",
            "folder_processing": "Ouverture du dossier en cours...",
            "folder_analysis_complete": "Analyse du dossier terminée",
            "dropped_folder_analysis": "{count} autres fichiers .rpy détectés dans ce dossier",
            "dropped_folder_suggestion_few": "Astuce : {count} autres fichiers .rpy détectés dans ce dossier",
            "dropped_folder_suggestion_many": "Astuce : {count} autres fichiers .rpy détectés (utilisez 'Ouvrir Dossier' pour tous les traiter)",
            "renpy_structure_detected": "Structure Ren'Py détectée",
            "clipboard_content_too_short": "Contenu trop court pour être traité",
            "clipboard_loading_cancelled": "Chargement presse-papier annulé par l'utilisateur",
            "clipboard_content_saved_loaded": "Contenu presse-papier sauvegardé et chargé : {count} lignes",
            "clipboard_unexpected_case": "Cas non prévu dans load_from_clipboard",
        },
        "processing": {
            "extraction_started": "Extraction en cours...",
            "reconstruction_started": "Reconstruction en cours...",
            "post_processing_ellipsis": "Post-traitement : {count} [...] corrigés en ...",
            "coherence_check_started": "Vérification de cohérence en cours...",
            "file_modified_check": "Fichier de traduction non modifié depuis l'extraction (timestamp: {timestamp})",
            "file_modification_detected": "Fichier de traduction modifié depuis l'extraction - reconstruction autorisée",
            "file_dialogue_missing": "Fichier dialogue n'existe plus: {path}",
            "modification_check_conditions_not_met": "Vérification modification fichier - conditions non remplies"
        },
        "language_management": {
            "language_interface_success": "Interface en {language_name}"
        },
        "validation": {
            "validation_with_values": "Validation avec: extracted={extracted}, asterix={asterix}, empty={empty}",
            "extracted_count_zero": "extracted_count est 0, cela semble incorrect",
            "recalculated_from_file": "Recalculé extracted_count depuis le fichieRéponse : {count}",
            "validation_failed_continue": "Validation échouée, continuer quand même ?",
            "validation_error_continue": "Erreur validation avant reconstruction: {error}"
        },
        "errors": {
            "file_open_error": "Erreur ouverture fichier",
            "folder_open_error": "Erreur ouverture dossier",
            "drag_drop_error": "Erreur fichier D&D",
            "clipboard_load_error": "Erreur chargement presse-papier",
            "clipboard_dialog_error": "Erreur dialog sauvegarde: {error}",
            "extraction_error": "Erreur extraction",
            "reconstruction_error": "Erreur reconstruction",
            "reload_error": "Erreur rechargement",
            "theme_toggle_error": "Erreur basculement thème: {error}",
            "auto_open_toggle_error": "Erreur toggle Ouverture-Auto",
            "language_change_error": "Erreur changement langue: {error}",
            "language_menu_error": "Erreur menu langue",
            "interface_recreation_error": "Erreur recréation interface: {error}",
            "theme_application_error": "Erreur application thème: {error}",
            "language_change_critical": "Erreur critique recréation interface: {error}",
            "debug_toggle_error": "Erreur lors du basculement du mode debug: {error}",
            "about_display_error": "Erreur affichage À propos",
            "help_display_error": "Erreur affichage aide",
            "glossary_open_error": "Erreur ouverture glossaire",
            "backup_manager_error": "Erreur gestionnaire sauvegardes",
            "warnings_open_error": "Erreur ouverture avertissements",
            "temporary_open_error": "Erreur ouverture temporaire",
            "reset_error": "Erreur réinitialisation",
            "refresh_error": "Erreur actualisation",
            "app_close_error": "Erreur fermeture",
            "next_file_error": "Erreur passage fichier suivant",
            "folder_open_system_error": "Impossible d'ouvrir le dossier {path}: {error}",
            "ui_extraction_critical": "Exception : {error}",
            "post_processing_error": "Erreur post-traitement: {error}",
            "ellipsis_correction_error": "Erreur correction ellipsis: {error}",
            "old_warnings_cleanup_error": "Erreur nettoyage anciens avertissements: {error}",
            "temp_folders_cleanup_error": "Erreur nettoyage dossiers: {error}",
            "file_load_error": "Erreur chargement fichieRéponse : {error}",
            "dropped_folder_analysis_error": "Erreur analyse dossier D&D: {error}"
        },
        "debug": {
            "debug_mode_enabled": "Mode debug activé",
            "debug_mode_disabled": "Mode debug désactivé",
            "debug_detailed_logs_visible": "Mode debug activé - Les logs détaillés sont maintenant visibles",
            "debug_normal_logs_return": "Mode debug désactivé - Retour aux logs normaux",
            "debug_mode_activated": "Mode debug activé",
            "debug_mode_deactivated": "Mode debug désactivé",
            "debug_toggle_error_message": "Erreur lors du basculement du mode debug"
        },
        "notifications": {
            "language_menu_error_fallback": "Erreur lors de l'affichage du menu de langues",
            "about_fallback": "{version}\nOutil de traduction Ren'Py",
            "success_notification_error": "Erreur notification succès: {error}",
            "theme_change_error_message": "Erreur lors du changement de thème"
        },
        "file_management": {
            "last_directory_updated_dnd": "last_directory mis à jour via D&D: {directory}",
            "folder_dnd_contains_rpy": "Dossier D&D contient {count} autres fichiers .rpy",
            "renpy_structure_detected_dnd": "Structure Ren'Py détectée via D&D: {path}",
            "file_loaded_anonymized": "Fichier chargé: {path} en {time:.2f}s",
            "clipboard_counter_generated": "Compteur presse-papier généré: {counter}",
            "virtual_file_created": "Fichier virtuel créé: {name}",
            "clipboard_content_loaded": "Contenu presse-papier chargé: {path}",
            "folder_files_valid": "Fichier ignoré: {filename} - {error}",
            "backup_failed": "Sauvegarde échouée: {error}",
            "extraction_file_timestamp": "Timestamp fichier extraction stocké: {timestamp}",
            "dialogue_file_path": "Chemin fichier dialogue: {path}",
            "dialogue_file_not_found": "Fichier dialogue non trouvé ou inexistant: {path}",
            "next_file_loaded": "Fichier suivant chargé: {path}",
            "folder_deleted": "Dossier {type} supprimé: {name}"
        }
    },
    "messages": {
        "info": {
            "auto_open_enabled": "Auto-ouverture activée",
            "auto_open_disabled": "Auto-ouverture désactivée"
        },
        "success": {
            "extraction": "Extraction terminée en {time:.2f}s"
        }
    },
    "glossary": {
        "title": "Gestionnaire de Glossaire",
        "search": "Rechercher :",
        "entries_title": "Entrées du glossaire",
        "edit_title": "Édition",
        "original_label": "Texte original",
        "translation_label": "Traduction",
        "labels": {
            "original": "Texte original :",
            "translation": "Traduction :",
            "search": "Rechercher :",
            "entries_count": "{count} entrée(s)",
            "statistics": "Statistiques"
        },
        "messages": {
            "entries_count": "{count} entrée(s)",
            "empty_fields": "Veuillez remplir les deux champs.",
            "add_error": "Cette entrée existe déjà.",
            "no_selection": "Veuillez sélectionner une entrée à modifier.",
            "modify_error": "Erreur lors de la modification.",
            "no_selection_delete": "Veuillez sélectionner une entrée à supprimer.",
            "confirm_delete": "Supprimer l'entrée :\n'{original}' → '{translation}' ?",
            "export_error": "Erreur lors de l'exportation.",
            "import_mode": "Fusionner avec le glossaire existant ?\n\nOui = Fusionner\nNon = Remplacer complètement",
            "import_error": "Erreur lors de l'importation.",
            "validation_success": "Glossaire validé : aucun problème détecté.",
            "validation_issues": "{count} problème(s) détecté(s) dans le glossaire.",
            "validation_issues_text": "Détails des problèmes :\n{issues}",
            "new_entry_added": "Nouvelle entrée ajoutée : '{original}' → '{translation}'",
            "entry_updated": "Entrée mise à jour : '{original}' → '{translation}' (était : '{old_translation}')",
            "entry_removed": "Entrée supprimée : '{original}' → '{translation}'",
            "glossary_loaded": "Glossaire chargé : {count} entrées",
            "new_glossary_created": "Nouveau glossaire créé",
            "glossary_saved": "Glossaire sauvegardé : {count} entrées",
            "glossary_export_success": "Glossaire exporté vers : {filepath}",
            "glossary_import_success": "Glossaire importé : {count} entrées depuis {filepath}",
            "line_ignored_format": "Ligne ignorée (format incorrect) ligne {line_num} : {line}",
            "no_glossary_terms": "Aucun terme dans le glossaire - protection ignorée",
            "exact_protection_start": "Protection du glossaire avec correspondance exacte : {count} termes",
            "term_protected": "Terme protégé (exact) : '{original}' → {placeholder} ({count}x ligne {line})",
            "exact_protection_complete": "Protection glossaire EXACTE terminée : {placeholders} placeholders, {replacements} remplacements",
            "line_modified": "Ligne {line} modifiée par la protection du glossaire"
        },
        "empty_fields_title": "Champs vides",
        "add_error_title": "Entrée existante",
        "no_selection_title": "Aucune sélection",
        "modify_error_title": "Erreur de modification",
        "no_selection_delete_title": "Aucune sélection",
        "confirm_delete_title": "Confirmer la suppression",
        "export_title": "Exporter le glossaire",
        "export_error_title": "Erreur d'exportation",
        "import_title": "Importer un glossaire",
        "import_mode_title": "Mode d'importation",
        "import_error_title": "Erreur d'importation",
        "validation_success_title": "Validation réussie",
        "validation_issues_title": "Problèmes détectés",
        "validation_issues_text_title": "Détails des problèmes",
        "validation": {
            "empty_original": "Terme original vide",
            "empty_translation": "Traduction vide pour '{original}'",
            "duplicate_translation": "Traduction dupliquée '{translation}' pour '{original}' (aussi utilisée par '{duplicates}')",
            "short_term": "Terme très court '{original}' - risque de remplacements non désirés",
            "special_characters": "Terme '{original}' contient des caractères spéciaux - vérifiez le résultat",
            "validation_error": "Erreur de validation : {error}",
            "term_very_short": "Terme très court '{original}' - risque de remplacements non désirés",
            "term_special_chars": "Terme '{original}' contient des caractères spéciaux - vérifiez le résultat",
            "term_substring": "'{original}' est contenu dans '{other_original}' - ordre de traitement important",
            "translation_empty": "Traduction vide pour '{original}'",
            "translation_duplicate": "Traduction '{translation}' utilisée pour plusieurs termes : {terms}"
        },
        "help": {
            "title": "Aide du Glossaire",
            "subtitle": "Guide d'utilisation du système de glossaire",
            "button_tooltip": "Aide sur le glossaire",
            "sections": {
                "principe": "Principe de fonctionnement",
                "principe_content": "Le glossaire permet de remplacer automatiquement des termes récurrents par leur traduction lors de l'extraction. Les termes sont protégés par des placeholders et restaurés automatiquement lors de la reconstruction.",
                "exemple": "Exemple d'utilisation",
                "exemple_content": "Si vous ajoutez 'wish' → 'souhaite', alors 'I wish you well' deviendra automatiquement 'I souhaite you well' après reconstruction, même si le texte original contenait d'autres mots comme 'wishes' ou 'wishful' qui ne seront pas affectés.",
                "ajouter": "Ajouter des termes",
                "ajouter_content": "Utilisez le bouton 'Ajouter' pour créer de nouvelles entrées. Saisissez le terme original en anglais et sa traduction française. La correspondance est exacte (sensible à la casse).",
                "usage": "Utilisation",
                "usage_content": "Le glossaire s'applique automatiquement lors de l'extraction si l'option est activée. Les termes sont remplacés par des placeholders (GLOSS001, GLOSS002...) puis restaurés avec la traduction lors de la reconstruction.",
                "bonnes_pratiques": "Bonnes pratiques",
                "bonnes_pratiques_content": "• Utilisez des termes complets plutôt que des fragments\n• Évitez les termes trop courts (moins de 3 caractères)\n• Vérifiez que vos traductions sont cohérentes\n• Testez sur quelques fichiers avant utilisation massive",
                "import_export": "Import/Export",
                "import_export_content": "Vous pouvez exporter votre glossaire vers un fichier texte pour le partager ou le sauvegarder, et importer des glossaires existants. Format : 'original => traduction' (une entrée par ligne).",
                "validation": "Validation",
                "validation_content": "Utilisez la fonction de validation pour détecter les problèmes potentiels : doublons, termes trop courts, caractères spéciaux, etc. Corrigez les erreurs signalées pour optimiser l'efficacité."
            }
        }
    },
    "reconstruction": {
        "validation": {
            "path_invalid": "Chemin invalide",
            "path_not_renpy_structure": "Chemin ne respectant pas la structure Ren'Py",
            "path_permissions_read": "Permissions de lecture insuffisantes",
            "path_permissions_write": "Permissions d'écriture insuffisantes",
            "path_permissions_dir_read": "Permissions de lecture du dossier insuffisantes",
            "path_permissions_dir_write": "Permissions d'écriture du dossier insuffisantes"
        },
        "errors": {
            "invalid_content": "Contenu de fichier invalide ou manquant",
            "original_path_not_defined": "Le chemin du fichier original n'est pas défini",
            "original_path_not_string": "Le chemin du fichier original n'est pas une chaîne de caractères",
            "original_not_rpy": "Le fichier original n'a pas l'extension .rpy",
            "invalid_save_path": "Chemin de sauvegarde non valide : {error}",
            "invalid_save_content": "Contenu à sauvegarder invalide ou manquant",
            "parent_directory_error": "Impossible de créer le répertoire parent : {error}",
            "save_error": "Erreur lors de la sauvegarde : {error}",
            "missing_mapping_files": "Fichiers manquants dans {folder} :\n• {file1}\n• {file2}",
            "missing_dialogue_file": "Fichier dialogue manquant : {file}",
            "comment_original_error": "Impossible de commenter le fichier original : {error}",
            "content_missing": "Contenu du fichier ou chemin original manquant",
            "critical_error": "Erreur critique : {error}",
            "validation_error": "Erreur de validation : {error}"
        },
        "validation_errors": {
            "mismatch_count": "Nombre de traductions incorrect: {provided} fourni, {expected} attendu",
            "asterix_warning": "{count} expressions entre astérisques détectées - vérifiez autre.txt",
            "empty_warning": "{count} textes vides/espaces détectés - vérifiez empty.txt"
        },
        "no_extraction": "Aucune extraction préalable trouvée. Veuillez d'abord extraire les textes.",
        "error_title": "Erreur de reconstruction",
        "error_occurred": "Une erreur s'est produite lors de la reconstruction : {error}",
        "error_general": "Erreur lors de la reconstruction du fichier",
        "file_modified": {
            "title": "Fichier non modifié",
            "message": "Le fichier de traduction ne semble pas avoir été modifié depuis l'extraction. Voulez-vous continuer quand même ?"
        },
        "clipboard_success_opened": "Fichier {filename} créé et ouvert en {time:.2f}s",
        "clipboard_success_created": "Fichier {filename} créé en {time:.2f}s",
        "file_success_opened": "Fichier {filename} reconstruit et ouvert en {time:.2f}s",
        "file_success_created": "Fichier {filename} reconstruit en {time:.2f}s"
    },
    "theme": {
        "dark_mode": "Mode Sombre", 
        "light_mode": "Mode Clair",
        "changed_to": "Thème changé vers {theme}"
    },
    "drag_drop": {
        "unavailable": "Glisser-déposer non disponible sur cette plateforme"
    },
    "input_modes": {
        "drag_drop_available": "Glissez-déposez vos fichiers ici",
        "ctrl_v_available": "Utilisez Ctrl+V pour coller du contenu"
    },
    "modes": {
        "drag_drop": "Glisser-Déposer",
        "ctrl_v": "Ctrl+V",
        "mode_changed": "Mode {mode_name} activé"
    },
    "sup_lignes_orphelines": {
        "sdk_validation": {
            "invalid_path": "Chemin SDK invalide : {path}",
            "renpy_exe_not_found": "renpy.exe introuvable dans : {path}",
            "sdk_files_missing": "Fichiers SDK manquants dans : {path}",
            "validation_successful": "SDK Ren'Py validé : {path}",
            "validation_failed": "SDK Ren'Py invalide : {path}"
        },
        "lint_generation": {
            "starting": "Génération du lint.txt pour le projet : {project}",
            "sdk_configured": "SDK configuré : {sdk_path}",
            "command_execution": "Exécution de la commande Ren'Py : {command}",
            "lint_found": "Lint trouvé dans fichier log : {file} ({size} octets)",
            "lint_extracted": "Lint extrait vers : {target_path}",
            "all_attempts_failed": "Toutes les tentatives de génération lint ont échoué",
            "exhaustive_search": "Recherche exhaustive du lint...",
            "log_files_found": "Fichiers log trouvés :",
            "creating_minimal_lint": "Création d'un lint minimal...",
            "problematic_files_cleaned": "{count} fichier(s) problématique(s) nettoyé(s)",
            "intelligent_lint_created": "Lint intelligent créé : {orphans} orphelins potentiels détectés",
            "basic_lint_created": "Lint basique créé : {path}",
            "orphan_candidate_found": "Candidat orphelin trouvé : {id}",
            "string_search_in_game": "Chaîne '{text}' trouvée dans {file}",
            "string_not_found_in_game": "Chaîne '{text}' NON trouvée dans le dossier game",
            "search_error": "Erreur lors de la recherche de '{text}'"
        },
        "unified_cleaner": {
            "init_message": "Nettoyeur initialisé",
            "backup_created": "Backup créé : {filename}",
            "backup_already_exists": "Backup déjà créé pour {filename}",
            "backup_failed": "Impossible de créer le backup pour {file}",
            "cleaning_started": "Début du nettoyage pour {count} langue(s) - UN SEUL BACKUP par fichier",
            "language_processing": "Traitement de la langue : {language}",
            "language_completed": "[{language}] Terminé : {files} fichiers, {lint_blocks} blocs lint + {string_blocks} blocs string = {total} blocs total supprimés",
            "cleaning_completed": "Nettoyage terminé : {languages} langues, {files} fichiers, {blocks} blocs supprimés",
            "backups_created": "Nombre de backups créés : {count}",
            "file_ignored_common": "Fichier common.rpy ignoré : {path}",
            "lint_blocks_removed": "[{file}] Lint cleanup: {count} blocs supprimés",
            "string_blocks_removed": "[{file}] String cleanup: {count} blocs supprimés"
        },
        "lint_parsing": {
            "orphan_section_found": "Section 'Orphan Translations' trouvée",
            "orphan_id_found": "ID orphelin trouvé : {id}",
            "orphan_section_end": "Fin de la section orphelins détectée à : {line}",
            "total_orphans_extracted": "Total d'IDs orphelins extraits du lint.txt : {count}",
            "first_orphan_ids": "Premiers IDs orphelins : {ids}",
            "no_orphan_ids": "Aucun ID orphelin, aucun nettoyage lint nécessaire"
        },
        "block_detection": {
            "translate_blocks_detected": "Blocs translate détectés : {count}",
            "new_translate_block": "Nouveau bloc translate détecté : {id} à la ligne {line}",
            "total_translate_blocks": "Total de blocs translate détectés : {count}",
            "orphan_block_to_remove": "Bloc orphelin à supprimer : {id}",
            "blocks_to_remove": "Blocs à supprimer : {remove_count}, à conserver : {keep_count}",
            "empty_translate_block_removed": "Suppression d'un bloc '{block}' vide",
            "orphan_comment_removed": "Suppression commentaire orphelin: {comment}"
        },
        "string_cleaning": {
            "block_removed_old_text": "Bloc supprimé - old_text: '{text}'",
            "string_exists_in_game": "Chaîne '{text}' trouvée dans {file}",
            "string_not_found_in_game": "Chaîne '{text}' NON trouvée dans le dossier game",
            "string_search_error": "Erreur lors de la recherche de '{text}'",
            "file_read_error": "Impossible de lire {file}"
        },
        "folder_scanning": {
            "language_folder_detected": "Dossier de langue détecté : {language}",
            "languages_found": "Dossiers de langue trouvés : {languages}",
            "no_rpy_files": "Aucun fichier .rpy trouvé dans {folder}",
            "rpy_files_found": "{count} fichiers .rpy trouvés dans {language}",
            "folder_scan_error": "Erreur lors du scan des dossiers de langue"
        },
        "sdk_detection": {
            "auto_detection_started": "Auto-détection rapide des SDK...",
            "sdk_found": "SDK trouvé : {folder}",
            "sdk_count_detected": "{count} SDK(s) Ren'Py détecté(s)",
            "auto_detection_failed": "Erreur auto-détection : {error}",
            "sdk_test_started": "Test auto-détecté : {sdk_name}",
            "sdk_suggested_failed": "SDK suggéré a échoué",
            "manual_selection_required": "Sélection manuelle requise...",
            "manual_selection_cancelled": "Sélection manuelle annulée",
            "user_selected_sdk": "Exécutable sélectionné : {exe_path}",
            "fallback_to_minimal": "Création d'un lint minimal...",
            "intelligent_generation_failed": "Erreur génération intelligente : {error}"
        },
        "validation": {
            "renpy_executable_valid": "Exécutable Ren'Py valide : {path}",
            "executable_validation_error": "Erreur validation exécutable : {error}",
            "sdk_file_missing": "Fichier SDK manquant : {file}",
            "executable_selection_info": "Aucun exécutable sélectionné",
            "executable_selected_success": "Exécutable Ren'Py sélectionné : {path}",
            "executable_invalid": "Fichier sélectionné n'est pas un exécutable Ren'Py valide : {path}",
            "executable_selection_error": "Erreur sélection exécutable : {error}"
        },
        "errors": {
            "file_not_found": "Fichier non trouvé : {file_path}",
            "lint_file_not_found": "Fichier lint.txt non trouvé : {lint_file_path}",
            "language_processing_error": "Erreur lors du traitement de la langue {language}: {error}",
            "general_unified_error": "Erreur générale lors du nettoyage : {error}",
            "language_folder_not_found": "Dossier de langue non trouvé : {language_folder}",
            "lint_parsing_error": "Erreur lors du parsing du lint.txt",
            "block_detection_error": "Erreur lors de la détection des blocs",
            "string_cleaning_error": "Erreur lors du nettoyage par chaînes",
            "backup_creation_error": "Erreur lors de la création du backup",
            "file_processing_error": "Erreur lors du traitement du fichier {file}",
            "sdk_validation_error": "Erreur de validation SDK : {error}",
            "lint_generation_error": "Erreur génération lint : {error}",
            "folder_scan_error": "Erreur scan dossier : {error}"
        },
        "statistics": {
            "files_processed": "Fichiers traités : {count}",
            "files_cleaned": "Fichiers nettoyés : {count}",
            "total_orphan_blocks": "Total blocs orphelins supprimés : {count}",
            "lint_blocks": "Blocs supprimés par lint : {count}",
            "string_blocks": "Blocs supprimés par correspondance : {count}",
            "languages_processed": "Langues traitées : {count}",
            "execution_time": "Temps d'exécution : {time}",
            "backup_files": "Fichiers de sauvegarde créés : {count}"
        }
    },
    "unified_backup_manager": {
        "window": {
            "title": "Gestionnaire de Sauvegardes"
        },
        "statistics": {
            "loading": "Chargement en cours...",
            "with_filter": "{count} sauvegardes • {size:.1f} MB • Jeu: {game}",
            "global": "{count} sauvegardes • {size:.1f} MB • {games} jeux"
        },
        "toolbar": {
            "game_filter_label": "Jeu:",
            "all_games": "Tous",
            "refresh_button": "Actualiser",
            "auto_cleanup_button": "Nettoyage Auto"
        },
        "columns": {
            "game": "Jeu",
            "filename": "Fichier",
            "type": "Type",
            "created": "Créé le",
            "size": "Taille"
        },
        "actions": {
            "restore": "Restaurer",
            "restore_to": "Restaurer vers...",
            "delete": "Supprimer",
            "properties": "Propriétés",
            "close": "Fermer"
        },
        "restore": {
            "confirm_title": "Confirmer la Restauration",
            "confirm_message": "Restaurer la sauvegarde ?\n\n• Fichier : {filename}\n• Jeu : {game}\n• Type : {type}\n• Créé le : {created}\n\nLe fichier actuel sera remplacé !",
            "source_not_found_info": "Le chemin source original est introuvable.\nVeuillez sélectionner manuellement le fichier de destination.",
            "success_title": "Restauration Réussie",
            "success_message": "Sauvegarde restaurée avec succès !\n\nFichier restauré : {path}",
            "dialog_title": "Restaurer vers...",
            "to_path_success": "Sauvegarde restaurée vers :\n{path}"
        },
        "delete": {
            "confirm_title": "Confirmer la Suppression",
            "confirm_message": "Supprimer définitivement cette sauvegarde ?\n\n• Fichier : {filename}\n• Jeu : {game}\n• Type : {type}\n• Taille : {size:.1f} MB\n\nCette action est irréversible !",
            "success_title": "Suppression Réussie",
            "success_message": "Sauvegarde supprimée avec succès.",
            "error_title": "Erreur de Suppression",
            "error_message": "Erreur lors de la suppression :\n{error}"
        },
        "properties": {
            "window_title": "Propriétés - {filename}",
            "title": "PROPRIÉTÉS DE LA SAUVEGARDE",
            "file_section": "FICHIER",
            "original_name": "Nom original : {name}",
            "backup_name": "Nom sauvegarde : {name}",
            "size_detail": "Taille : {size_mb:.2f} MB ({size_bytes:,} bytes)",
            "game_section": "JEU",
            "game_name": "Nom : {name}",
            "type_section": "TYPE",
            "type_name": "Type : {type}",
            "type_code": "Code type : {code}",
            "description": "Description : {desc}",
            "dates_section": "DATES",
            "created_date": "Créé le : {date}",
            "paths_section": "CHEMINS",
            "backup_path": "Sauvegarde : {path}",
            "source_path": "Source : {path}",
            "source_exists": "Fichier source existe : {exists}",
            "id_section": "IDENTIFIANT",
            "backup_id": "ID : {id}",
            "system_section": "INFORMATIONS SYSTÈME",
            "backup_exists": "Sauvegarde existe : {exists}",
            "detected_type": "Type détecté : {type}",
            "exists_yes": "Oui",
            "exists_no": "Non",
            "path_unknown": "Inconnu",
            "reconstruct_button": "Reconstruire Chemin Source",
            "reconstruct_success": "Chemin source reconstruit :\n{path}",
            "reconstruct_failed": "Impossible de reconstruire le chemin source automatiquement."
        },
        "auto_cleanup": {
            "confirm_title": "Nettoyage Automatique",
            "confirm_message": "Voulez-vous lancer le nettoyage automatique ?\n\n• Supprime les backups de plus de 30 jours\n• Garde au minimum 5 backups par jeu\n• Préserve les backups de sécurité récents",
            "no_cleanup_title": "Aucun Nettoyage",
            "no_cleanup_message": "Aucune ancienne sauvegarde à nettoyer.",
            "completed_title": "Nettoyage Terminé",
            "completed_message": "Nettoyage terminé !\n\n• {count} sauvegardes supprimées"
        },
        "messages": {
            "selection_required": "Veuillez sélectionner une sauvegarde à restaurer.",
            "selection_required_delete": "Veuillez sélectionner une sauvegarde à supprimer.",
            "selection_required_properties": "Veuillez sélectionner une sauvegarde."
        },
        "errors": {
            "general": "Erreur ouverture gestionnaire : {error}",
            "opening": "Erreur ouverture gestionnaire :\n{error}",
            "loading_data": "Erreur chargement données: {error}",
            "loading_data_message": "Erreur chargement données :\n{error}",
            "game_filter_update": "Erreur mise à jour filtre jeu: {error}",
            "tree_add_error": "Erreur ajout backup à l'arbre: {error}",
            "restore_error": "Erreur durant la restauration :\n{error}",
            "restore_to_error": "Erreur durant la restauration :\n{error}",
            "delete_error": "Erreur durant la suppression :\n{error}",
            "properties_error": "Erreur affichage propriétés :\n{error}",
            "cleanup_error": "Erreur durant le nettoyage :\n{error}",
            "reconstruct_error": "Erreur reconstruction :\n{error}"
        }
    },

    "quick_backup_actions": {
        "window": {
            "title": "Actions Rapides - Sauvegardes"
        },
        "main_title": "Actions Rapides",
        "file_info": "Fichier : {filename}",
        "actions": {
            "create_manual": "Créer Sauvegarde Manuelle",
            "view_all": "Voir Toutes les Sauvegardes",
            "close": "Fermer"
        },
        "manual_backup": {
            "no_file_error": "Aucun fichier valide sélectionné.",
            "success": "Sauvegarde manuelle créée :\n{path}",
            "error": "Erreur création sauvegarde :\n{error}"
        },
        "errors": {
            "menu_error": "Erreur ouverture menu :\n{error}"
        }
    },
    "validation": {
        "success_message": "{file_type} validé avec succès (confiance: {confidence}%). {patterns_count} motif(s) Ren'Py détecté(s).",
        "failed_message": "Validation échouée :\n{errors}",
        "warnings_title": "Avertissements :",
        "errors_title": "Erreurs :",
        "file_not_found": "Fichier non trouvé",
        "non_rpy_extension": "Extension non .rpy détectée",
        "non_utf8_encoding": "Encodage non UTF-8 détecté",
        "read_error": "Erreur de lecture : {error}",
        "file_empty": "Fichier vide",
        "validation_error": "Erreur de validation : {error}",
        "low_confidence": "Niveau de confiance faible pour la validation",
        "backup_success": "Sauvegarde créée avec succès",
        "backup_failed": "Échec de la création de sauvegarde",
        "backup_file_missing": "Fichier source introuvable",
        "backup_file_not_found": "Fichier de sauvegarde introuvable",
        "restore_success": "Fichier restauré avec succès",
        "restore_failed": "Impossible de restaurer",
        "translation_file_missing": "Fichier de traduction manquant : {file}",
        "translation_mismatch": "Nombre de traductions incorrect: {provided} fourni, {expected} attendu",
        "translations_missing": "Traductions manquantes: {missing_count} (attendu: {expected}, trouvé: {found})",
        "translations_extra": "Traductions supplémentaires: {extra_count} (attendu: {expected}, trouvé: {found})",
        "validation_correspondence_error": "Erreur de validation : {error}",
        "main_file_missing": "Fichier principal manquant : {file}",
        "asterix_file_missing": "Fichier astérisques manquant : {file}",
        "empty_file_missing": "Fichier textes vides manquant : {file}",
        "temp_folder_missing": "Dossier temporaire inexistant : {folder}",
        "folder_creation_failed": "Impossible de créer le dossier : {error}",
        "no_game_found": "Aucun projet détecté",
        "start_extraction_suggestion": "Commencez par extraire un fichier .rpy",
        "fix_structure_errors": "Corrigez les erreurs de structure avant de continuer",
        "cleanup_old_files": "Considérez nettoyer les anciens fichiers temporaires",
        "backup_folder_not_found": "Dossier de sauvegarde non trouvé : {folder}",
        "quote_correction_applied": "Correction guillemets appliquée : {count} corrections",
        "quote_correction_error": "Erreur lors de la correction des guillemets : {error}",
        "game_structure_validation": "Validation de la structure du jeu",
        "folders_created": "Dossiers créés avec succès",
        "folders_missing": "Dossiers manquants détectés",
        "insufficient_write_permissions": "Permissions d'écriture insuffisantes : {folder}",
        "extraction_files_validation": "Validation des fichiers d'extraction",
        "required_files_missing": "Fichiers requis manquants pour {file_base}",
        "cleanup_completed": "Nettoyage terminé : {files_removed} supprimés, {files_kept} conservés",
        "cleanup_failed": "Erreur lors du nettoyage : {error}",
        "diagnostic_complete": "Diagnostic terminé",
        "diagnostic_error": "Erreur lors du diagnostic : {error}",
        "application_state_healthy": "État de l'application normal",
        "application_issues_detected": "Problèmes détectés dans l'application"
    }
}