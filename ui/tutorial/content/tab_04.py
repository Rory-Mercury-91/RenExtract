def generate_content(generator, language, translations):
    """
    Génère le contenu pour l'onglet 4 : Générateur Ren'Py
    
    Args:
        generator: Instance du générateur avec méthodes utilitaires
        language: Code langue (fr, en, de)
        translations: Dictionnaire des traductions
    
    Returns:
        str: HTML généré pour l'onglet générateur
    """
    # Récupération des traductions pour cette section
    section_t = translations.get('tabs', {}).get('generateur', {})
    common_t = translations.get('common', {})
   
    def get_text(key, fallback=""):
        return section_t.get(key) or common_t.get(key) or fallback

    # Navigation rapide
    quick_nav_title = get_text('quick_nav_title', 'Navigation rapide')
    nav_extraction_rpa = get_text('nav_extraction_rpa', 'Extraction RPA')
    nav_extraction_rpa_desc = get_text('nav_extraction_rpa_desc', 'Extraction des archives du jeu')
    nav_generation = get_text('nav_generation', 'Génération TL')
    nav_generation_desc = get_text('nav_generation_desc', 'Création arborescence et modules français')
    nav_extraction_config = get_text('nav_extraction_config', 'Extraction Config')
    nav_extraction_config_desc = get_text('nav_extraction_config_desc', 'Textes oubliés par le SDK')
    nav_combinaison = get_text('nav_combinaison', 'Combinaison')
    nav_combinaison_desc = get_text('nav_combinaison_desc', 'Fusion et division de fichiers')

    # Vue d'ensemble générale
    title = get_text('title', 'Générateur Ren\'Py - Guide Complet')
    intro = get_text('intro', 'Interface séparée accessible via Préparation → Générateur Ren\'Py pour la gestion complète du projet. Contrairement à l\'Interface Principale qui traite fichier par fichier, le Générateur gère l\'infrastructure complète du projet.')
    overview_title = get_text('overview_title', 'Vue d\'ensemble des 4 onglets principaux')
    extraction_compilation_tab = get_text('extraction_compilation_tab', 'Extraction & Compilation RPA/RPYC')
    extraction_compilation_desc = get_text('extraction_compilation_desc', 'Gestion des archives du jeu')
    generation_tab = get_text('generation_tab', 'Génération')
    generation_desc = get_text('generation_desc', 'Création de l\'arborescence tl/[langue]/ avec modules français')
    extraction_config_tab = get_text('extraction_config_tab', 'Extraction Config')
    extraction_config_desc = get_text('extraction_config_desc', 'Textes oubliés par le SDK')
    extraction_results_tab = get_text('extraction_results_tab', 'Extraction Résultats')
    extraction_results_desc = get_text('extraction_results_desc', 'Analyse des textes détectés')
    combination_tab = get_text('combination_tab', 'Combinaison & Division')
    combination_desc = get_text('combination_desc', 'Fusion/division de fichiers')
    reorganization_title = get_text('reorganization_title', 'Réorganisation des outils')
    reorganization_desc = get_text('reorganization_desc', 'Les outils Nettoyage Intelligent et Éditeur Temps Réel ont été déplacés vers l\'onglet Outils de Cohérence pour une meilleure organisation thématique.')

    # Section Extraction RPA
    extraction_rpa_title = get_text('extraction_rpa_title', 'Extraction & Compilation RPA/RPYC - Guide Complet')
    extraction_interface_alt = get_text('extraction_interface_alt', 'Générateur - Interface Extraction & Compilation')
    extraction_interface_caption = get_text('extraction_interface_caption', 'Vue complète avec projet configuré et toutes les options disponibles')
    extraction_purpose_title = get_text('extraction_purpose_title', 'À quoi ça sert')
    extraction_purpose_intro = get_text('extraction_purpose_intro', 'Cet onglet orchestre l\'extraction complète des archives du jeu pour accéder aux fichiers source (.rpy). Il gère deux opérations cruciales :')
    extraction_rpa_rpyc_title = get_text('extraction_rpa_rpyc_title', 'Extraction RPA/RPYC')
    extraction_rpa_rpyc_desc = get_text('extraction_rpa_rpyc_desc', 'Extrait les archives .rpa et décompile les fichiers .rpyc pour obtenir les scripts source .rpy lisibles et modifiables.')
    custom_rpa_build_title = get_text('custom_rpa_build_title', 'Construction RPA Personnalisée')
    custom_rpa_build_desc = get_text('custom_rpa_build_desc', 'Recompile vos traductions en archives .rpa optimisées pour distribution ou test dans le jeu original.')
    prerequisite_title = get_text('prerequisite_title', 'Prérequis important')
    prerequisite_desc = get_text('prerequisite_desc', 'Un projet Ren\'Py doit être sélectionné dans la section "Configuration du projet" avant d\'utiliser cet onglet. Les opérations agissent directement sur le dossier du jeu choisi.')

    # Workflow
    workflow_title = get_text('workflow_title', 'Workflow en 3 phases')
    auto_preparation_label = get_text('auto_preparation_label', 'Préparation automatique :')
    auto_preparation_desc = get_text('auto_preparation_desc', 'Téléchargement et configuration des outils (unrpyc v1/v2, rpatool, Python embedded)')
    smart_extraction_label = get_text('smart_extraction_label', 'Extraction intelligente :')
    smart_extraction_desc = get_text('smart_extraction_desc', 'Détection automatique de la version Ren\'Py et choix de la méthode optimale')
    cleanup_finalization_label = get_text('cleanup_finalization_label', 'Nettoyage et finalisation :')
    cleanup_finalization_desc = get_text('cleanup_finalization_desc', 'Suppression des outils temporaires et options de post-traitement')

    # Section Extraction
    extraction_section_title = get_text('extraction_section_title', 'Section Extraction RPA/RPYC')
    advanced_extraction_alt = get_text('advanced_extraction_alt', 'Paramètres d\'extraction avancés')
    advanced_extraction_caption = get_text('advanced_extraction_caption', 'Configuration des options d\'extraction avec cases à cocher et explications')
    main_options_title = get_text('main_options_title', 'Options principales :')
    delete_rpa_option = get_text('delete_rpa_option', 'Case "Supprimer les fichiers RPA après extraction" :')
    delete_rpa_desc = get_text('delete_rpa_desc', 'Économise l\'espace disque en supprimant automatiquement les archives sources après extraction réussie')
    start_extraction_button = get_text('start_extraction_button', 'Bouton "Démarrer l\'extraction" :')
    start_extraction_desc = get_text('start_extraction_desc', 'Lance le processus complet avec détection automatique des outils nécessaires')
    path_help_button = get_text('path_help_button', 'Aide chemins ⚠️ :')
    path_help_desc = get_text('path_help_desc', 'Popup d\'information sur les limitations des chemins contenant des crochets [ ]')

    # Détection intelligente
    smart_detection_title = get_text('smart_detection_title', 'Détection intelligente automatique :')
    renpy_version_title = get_text('renpy_version_title', 'Version Ren\'Py')
    method_label = get_text('method_label', 'Méthode :')
    renpy_version_method = get_text('renpy_version_method', 'Analyse de script_version.txt puis fallback sur analyse binaire des .rpyc')
    auto_choice_label = get_text('auto_choice_label', 'Choix automatique :')
    renpy_version_choice = get_text('renpy_version_choice', 'unrpyc v1 (Ren\'Py 6/7) ou v2 (Ren\'Py 8+)')
    compatible_python_title = get_text('compatible_python_title', 'Python Compatible')
    v1_label = get_text('v1_label', 'v1 :')
    python_v1_desc = get_text('python_v1_desc', 'Python 2.7 embedded pour les anciens jeux')
    v2_label = get_text('v2_label', 'v2 :')
    python_v2_desc = get_text('python_v2_desc', 'Python 3.11 embedded pour les jeux récents')
    fallback_strategy_title = get_text('fallback_strategy_title', 'Stratégie Fallback')
    fallback_strategy_desc = get_text('fallback_strategy_desc', 'Si la première tentative échoue massivement, essai automatique avec l\'autre version d\'unrpyc')

    # Limitations
    important_limitations_title = get_text('important_limitations_title', 'Limitations importantes :')
    path_limitations_alt = get_text('path_limitations_alt', 'Aide sur les limitations de chemins')
    path_limitations_caption = get_text('path_limitations_caption', 'Popup explicatif sur les problèmes avec les crochets dans les noms de dossiers')
    unsupported_paths_title = get_text('unsupported_paths_title', 'Chemins non supportés')
    unsupported_paths_desc = get_text('unsupported_paths_desc', 'Les chemins contenant des crochets [ ] ne sont pas supportés par les outils d\'extraction.')
    problematic_examples_label = get_text('problematic_examples_label', 'Exemples problématiques :')
    solutions_label = get_text('solutions_label', 'Solutions :')
    solutions_desc = get_text('solutions_desc', 'Renommez le dossier ou déplacez le projet vers un chemin sans caractères spéciaux.')

    # Construction RPA
    custom_rpa_section_title = get_text('custom_rpa_section_title', 'Section Construction RPA Personnalisée')
    rpa_build_config_alt = get_text('rpa_build_config_alt', 'Configuration construction RPA')
    rpa_build_config_caption = get_text('rpa_build_config_caption', 'Interface de paramétrage pour créer une archive RPA personnalisée')
    advanced_config_title = get_text('advanced_config_title', 'Configuration avancée :')
    language_selection_title = get_text('language_selection_title', 'Sélection de langue :')
    scan_languages_button = get_text('scan_languages_button', 'Bouton "Scanner les langues" :')
    scan_languages_desc = get_text('scan_languages_desc', 'Détecte automatiquement les dossiers tl/ disponibles dans le projet')
    smart_priority_label = get_text('smart_priority_label', 'Priorité intelligente :')
    smart_priority_desc = get_text('smart_priority_desc', '"french" apparaît en premier s\'il existe, sinon tri alphabétique')
    validation_label = get_text('validation_label', 'Validation :')
    validation_desc = get_text('validation_desc', 'Seuls les dossiers contenant des fichiers exploitables sont listés')

    # Types de fichiers
    file_types_title = get_text('file_types_title', 'Types de fichiers inclus automatiquement :')
    scripts_type_title = get_text('scripts_type_title', 'Scripts')
    scripts_type_desc = get_text('scripts_type_desc', '.rpy (source), .rpyc (binaire)')
    images_type_title = get_text('images_type_title', 'Images')
    images_type_desc = get_text('images_type_desc', '.jpg, .png, .webp')
    audio_type_title = get_text('audio_type_title', 'Audio')
    audio_type_desc = get_text('audio_type_desc', '.ogg, .mp3')
    fonts_type_title = get_text('fonts_type_title', 'Polices')
    fonts_type_desc = get_text('fonts_type_desc', '.ttf, .otf')

    # Déroulement des opérations
    operations_flow_title = get_text('operations_flow_title', 'Déroulement des opérations')
    extraction_in_progress_alt = get_text('extraction_in_progress_alt', 'Extraction en cours')
    extraction_in_progress_caption = get_text('extraction_in_progress_caption', 'Interface pendant l\'extraction avec barre de progression et statut détaillé')
    extraction_phase_title = get_text('extraction_phase_title', 'Phase d\'extraction :')
    initialization_step = get_text('initialization_step', 'Initialisation (0-10%) :')
    initialization_desc = get_text('initialization_desc', 'Téléchargement automatique des outils si nécessaire')
    rpa_extraction_step = get_text('rpa_extraction_step', 'Extraction RPA (10-35%) :')
    rpa_extraction_desc = get_text('rpa_extraction_desc', 'Décompression des archives avec rpatool')
    version_detection_step = get_text('version_detection_step', 'Détection version (35-40%) :')
    version_detection_desc = get_text('version_detection_desc', 'Analyse intelligente pour choisir unrpyc v1 ou v2')
    rpyc_decompilation_step = get_text('rpyc_decompilation_step', 'Décompilation RPYC (40-85%) :')
    rpyc_decompilation_desc = get_text('rpyc_decompilation_desc', 'Conversion des binaires en source avec fallback automatique')
    cleanup_step = get_text('cleanup_step', 'Nettoyage (85-100%) :')
    cleanup_desc = get_text('cleanup_desc', 'Suppression des outils temporaires et finalisation')

    # Résultats et rapports
    results_reports_title = get_text('results_reports_title', 'Résultats et rapports')
    detailed_results_alt = get_text('detailed_results_alt', 'Popup de résultats détaillé')
    detailed_results_caption = get_text('detailed_results_caption', 'Fenêtre de résultats après extraction avec statistiques et temps d\'exécution')
    interactive_results_title = get_text('interactive_results_title', 'Popup de résultats interactif :')
    interactive_results_intro = get_text('interactive_results_intro', 'À la fin de chaque opération, une fenêtre détaillée affiche :')
    successful_extraction_title = get_text('successful_extraction_title', 'Extraction réussie')
    successful_extraction_1 = get_text('successful_extraction_1', 'Nombre d\'archives RPA extraites')
    successful_extraction_2 = get_text('successful_extraction_2', 'Fichiers RPYC convertis/ignorés/échoués')
    successful_extraction_3 = get_text('successful_extraction_3', 'Temps total d\'exécution')
    successful_extraction_4 = get_text('successful_extraction_4', 'Statistiques de fallback si applicable')
    failure_management_title = get_text('failure_management_title', 'Gestion d\'échecs')
    failure_management_1 = get_text('failure_management_1', 'Lien vers la méthode alternative (UnRen.bat)')
    failure_management_2 = get_text('failure_management_2', 'Détail des erreurs rencontrées')
    failure_management_3 = get_text('failure_management_3', 'Suggestions de résolution')

    # Section Génération TL
    generation_tl_title = get_text('generation_tl_title', 'Génération TL - Guide Détaillé')
    generation_overview_alt = get_text('generation_overview_alt', 'Onglet Génération - Vue complète')
    generation_overview_caption = get_text('generation_overview_caption', 'Interface complète avec configuration langue, options et polices GUI')
    generation_purpose_title = get_text('generation_purpose_title', 'À quoi ça sert')
    generation_purpose_intro = get_text('generation_purpose_intro', 'L\'onglet Génération est votre centre de contrôle pour créer l\'arborescence de traduction complète (dossier tl/[langue]/) avec tous les fichiers nécessaires. Il combine la génération de base avec des modules optionnels pour une expérience française optimisée.')
    basic_config_step = get_text('basic_config_step', 'Configuration de base')
    basic_config_desc = get_text('basic_config_desc', 'Langue cible et options générales')
    advanced_customization_step = get_text('advanced_customization_step', 'Personnalisation avancée')
    advanced_customization_desc = get_text('advanced_customization_desc', 'Polices GUI et modules français')
    targeted_generation_step = get_text('targeted_generation_step', 'Génération ciblée')
    targeted_generation_desc = get_text('targeted_generation_desc', 'Choix du niveau de traitement selon vos besoins')

    # Interface utilisateur génération
    user_interface_title = get_text('user_interface_title', 'Ce que voit l\'utilisateur')
    basic_config_section_title = get_text('basic_config_section_title', 'Section Configuration de base :')
    target_language_title = get_text('target_language_title', 'Langue cible avec assistance :')
    input_field_label = get_text('input_field_label', 'Champ de saisie :')
    input_field_desc = get_text('input_field_desc', 'Tapez le code de langue souhaité (ex: "french", "spanish")')
    help_button_label = get_text('help_button_label', 'Bouton d\'aide "?" :')
    help_button_desc = get_text('help_button_desc', 'Popup avec exemples de codes de langues supportés')
    smart_autocomplete_label = get_text('smart_autocomplete_label', 'Auto-complétion intelligente :')
    smart_autocomplete_desc = get_text('smart_autocomplete_desc', 'Synchronisation automatique avec l\'onglet Combinaison')

    # Options grille
    options_grid_title = get_text('options_grid_title', 'Grille d\'options 2x4 :')
    integration_options_alt = get_text('integration_options_alt', 'Options d\'intégration')
    integration_options_caption = get_text('integration_options_caption', 'Grille avec cases à cocher et boutons d\'aide alignés')
    language_selector_option_title = get_text('language_selector_option_title', 'Sélecteur de langue')
    checkbox_label = get_text('checkbox_label', 'Case :')
    language_selector_checkbox = get_text('language_selector_checkbox', '"Ajouter sélecteur de langue"')
    action_label = get_text('action_label', 'Action :')
    language_selector_action = get_text('language_selector_action', 'Intègre automatiquement votre langue dans le menu Preferences du jeu')
    help_label = get_text('help_label', 'Aide :')
    language_selector_help = get_text('language_selector_help', 'Explique l\'injection intelligente dans screens.rpy')
    common_rpy_option_title = get_text('common_rpy_option_title', 'Common.rpy français')
    common_rpy_checkbox = get_text('common_rpy_checkbox', '"Ajouter le common.rpy"')
    common_rpy_action = get_text('common_rpy_action', 'Interface Ren\'Py de base en français (disponible uniquement pour "french")')
    common_rpy_help = get_text('common_rpy_help', 'Détail du contenu inclus (menus, messages système)')
    dev_console_option_title = get_text('dev_console_option_title', 'Console développeur')
    dev_console_checkbox = get_text('dev_console_checkbox', '"Activer la console développeur"')
    dev_console_action = get_text('dev_console_action', 'Active config.developer et config.console pour la langue')
    dev_console_help = get_text('dev_console_help', 'Code exact inséré et avantages pour le debug')
    screen_rpy_option_title = get_text('screen_rpy_option_title', 'Screen.rpy français')
    screen_rpy_checkbox = get_text('screen_rpy_checkbox', '"Ajouter le screen.rpy"')
    screen_rpy_action = get_text('screen_rpy_action', 'Écrans d\'interface traduits (disponible uniquement pour "french")')
    screen_rpy_help = get_text('screen_rpy_help', 'Structure et éléments visuels inclus')

    # Section polices GUI
    gui_fonts_section_title = get_text('gui_fonts_section_title', 'Section Polices GUI (facultative) :')
    font_preview_title = get_text('font_preview_title', 'Aperçu des polices :')
    font_preview_alt = get_text('font_preview_alt', 'Aperçu des polices')
    font_preview_caption = get_text('font_preview_caption', 'Sélecteur avec texte de test français pour prévisualiser les polices')
    preview_zone_desc = get_text('preview_zone_desc', 'Zone de prévisualisation avec le texte test : "Voix ambiguë d\'un cœur qui au zéphyr préfère les jattes de kiwis."')
    font_selector_label = get_text('font_selector_label', 'Sélecteur de police :')
    font_selector_desc = get_text('font_selector_desc', 'Dropdown avec toutes les polices système compatibles')
    realtime_preview_label = get_text('realtime_preview_label', 'Aperçu en temps réel :')
    realtime_preview_desc = get_text('realtime_preview_desc', 'Le texte change immédiatement selon la police sélectionnée')
    accent_test_label = get_text('accent_test_label', 'Test d\'accents :')
    accent_test_desc = get_text('accent_test_desc', 'Vérifie la compatibilité avec les caractères français')

    # Configuration individuelle
    individual_config_title = get_text('individual_config_title', 'Configuration individuelle (Grille 2x3) :')
    gui_fonts_grid_alt = get_text('gui_fonts_grid_alt', 'Grille de polices GUI')
    gui_fonts_grid_caption = get_text('gui_fonts_grid_caption', 'Configuration individuelle des 5 éléments GUI avec cases et dropdowns alignés')
    individual_config_intro = get_text('individual_config_intro', 'Chaque élément GUI peut être configuré séparément :')
    main_text_title = get_text('main_text_title', 'Texte principal (dialogues)')
    main_text_desc = get_text('main_text_desc', 'Police utilisée pour tous les dialogues des personnages')
    character_names_title = get_text('character_names_title', 'Noms des personnages')
    character_names_desc = get_text('character_names_desc', 'Police pour l\'affichage des noms au-dessus des dialogues')
    user_interface_element_title = get_text('user_interface_element_title', 'Interface utilisateur')
    user_interface_element_desc = get_text('user_interface_element_desc', 'Police pour les menus, préférences et éléments d\'interface')
    general_buttons_title = get_text('general_buttons_title', 'Boutons généraux')
    general_buttons_desc = get_text('general_buttons_desc', 'Police pour les boutons de navigation et d\'action')
    choice_buttons_title = get_text('choice_buttons_title', 'Boutons de choix')
    choice_buttons_desc = get_text('choice_buttons_desc', 'Police spécifique pour les choix de dialogue du joueur')
    rtl_option_title = get_text('rtl_option_title', 'Option RTL :')
    rtl_option_desc = get_text('rtl_option_desc', 'Case "RTL (Lecture droite à gauche)" pour les langues comme l\'arabe, l\'hébreu, le persan.')

    # Boutons d'action
    action_buttons_title = get_text('action_buttons_title', 'Boutons d\'action')
    generate_translations_title = get_text('generate_translations_title', 'Générer les traductions')
    generate_translations_action = get_text('generate_translations_action', 'Génération de base + common.rpy/screen.rpy si cochés')
    usage_label = get_text('usage_label', 'Usage :')
    generate_translations_usage = get_text('generate_translations_usage', 'Première utilisation, génération standard')
    apply_fonts_title = get_text('apply_fonts_title', 'Appliquer les polices')
    apply_fonts_action = get_text('apply_fonts_action', 'Applique SEULEMENT les polices GUI sélectionnées')
    apply_fonts_usage = get_text('apply_fonts_usage', 'Modification des polices sur un projet existant')
    add_selector_title = get_text('add_selector_title', 'Ajouter le sélecteur')
    add_selector_action = get_text('add_selector_action', 'Crée UNIQUEMENT le sélecteur de langue')
    add_selector_usage = get_text('add_selector_usage', 'Ajout ponctuel sans regénération')
    generate_all_title = get_text('generate_all_title', 'Générer + options cochées')
    generate_all_action = get_text('generate_all_action', 'Génération complète avec TOUTES les cases cochées')
    generate_all_usage = get_text('generate_all_usage', 'Configuration complète en une fois')

    # Section Extraction Config
    extraction_config_title = get_text('extraction_config_title', 'Extraction des Textes Oubliés - Guide Complet')
    config_extraction_complete_alt = get_text('config_extraction_complete_alt', 'Configuration d\'extraction complète')
    config_extraction_complete_caption = get_text('config_extraction_complete_caption', 'Interface avec sélection langue, modes de détection et exclusions configurées')
    config_extraction_purpose_title = get_text('config_extraction_purpose_title', 'À quoi ça sert')
    config_extraction_purpose_intro = get_text('config_extraction_purpose_intro', 'Cette fonctionnalité trouve et extrait les textes d\'interface oubliés par le SDK Ren\'Py officiel : boutons de menu, messages d\'erreur, éléments GUI, etc. Contrairement à la génération normale qui ne traite que les dialogues, l\'extraction Config analyse en profondeur tous les fichiers pour détecter les chaînes traduisibles manquées.')
    why_necessary_title = get_text('why_necessary_title', 'Pourquoi c\'est nécessaire')
    why_necessary_desc = get_text('why_necessary_desc', 'Le SDK officiel ne génère que les traductions des dialogues principaux. Mais les jeux contiennent aussi des textes d\'interface (menus, boutons, notifications) qui ne sont pas automatiquement détectés. Cette fonction comble cette lacune.')

    # Workflow Config
    config_workflow_title = get_text('config_workflow_title', 'Workflow en 3 étapes')
    config_step1_title = get_text('config_step1_title', 'Configuration (Onglet 3)')
    config_step1_desc = get_text('config_step1_desc', 'Paramétrage de l\'analyse : langue de référence, mode de détection, exclusions')
    config_step2_title = get_text('config_step2_title', 'Analyse automatique')
    config_step2_desc = get_text('config_step2_desc', 'Le système scanne tous les fichiers .rpy avec patterns intelligents')
    config_step3_title = get_text('config_step3_title', 'Résultats et génération (Onglet 4)')
    config_step3_desc = get_text('config_step3_desc', 'Visualisation par catégories, sélection manuelle et création du fichier final')

    # Sélection de langue config
    auto_language_detection_title = get_text('auto_language_detection_title', 'Détection automatique des langues :')
    smart_scan_label = get_text('smart_scan_label', 'Scan intelligent :')
    smart_scan_desc = get_text('smart_scan_desc', 'Le bouton "Scanner les langues" détecte automatiquement toutes les langues ayant des fichiers .rpy dans le dossier tl/')
    french_priority_label = get_text('french_priority_label', 'Priorité française :')
    french_priority_desc = get_text('french_priority_desc', 'Si une langue "french" existe, elle apparaît en premier dans la liste')
    language_validation_label = get_text('language_validation_label', 'Validation :')
    language_validation_desc = get_text('language_validation_desc', 'Seules les langues contenant effectivement des fichiers de traduction sont proposées')
    language_role_title = get_text('language_role_title', 'Rôle de la langue sélectionnée :')
    language_role_desc = get_text('language_role_desc', 'La langue sélectionnée sert de référence anti-doublons. L\'analyse compare les textes détectés avec ceux déjà traduits dans cette langue pour éviter les redondances.')

    # Modes de détection
    detection_modes_title = get_text('detection_modes_title', 'Modes de détection - Simple vs Optimisé')
    detection_modes_help_alt = get_text('detection_modes_help_alt', 'Aide sur les modes de détection')
    detection_modes_help_caption = get_text('detection_modes_help_caption', 'Popup explicatif comparant les modes Simple et Optimisé')
    simple_mode_title = get_text('simple_mode_title', 'Mode Simple')
    basic_patterns_label = get_text('basic_patterns_label', 'Patterns basiques uniquement :')
    basic_patterns_desc = get_text('basic_patterns_desc', 'Character(), input(), notify()')
    simple_advantages_label = get_text('simple_advantages_label', 'Avantages :')
    simple_advantages_desc = get_text('simple_advantages_desc', 'Très rapide, confiance 100%, pas de faux positifs')
    simple_disadvantages_label = get_text('simple_disadvantages_label', 'Inconvénients :')
    simple_disadvantages_desc = get_text('simple_disadvantages_desc', 'Détection limitée, peut manquer des textes d\'interface')
    simple_usage_label = get_text('simple_usage_label', 'Usage :')
    simple_usage_desc = get_text('simple_usage_desc', 'Premier essai rapide, projets avec peu de textes d\'interface')
    optimized_mode_title = get_text('optimized_mode_title', 'Mode Optimisé (Recommandé)')
    advanced_patterns_label = get_text('advanced_patterns_label', 'Patterns avancés :')
    advanced_patterns_desc = get_text('advanced_patterns_desc', 'Character, input, notify, textbutton, text, show text')
    optimized_advantages_label = get_text('optimized_advantages_label', 'Avantages :')
    optimized_advantages_desc = get_text('optimized_advantages_desc', 'Détection complète, classification intelligente')
    optimized_disadvantages_label = get_text('optimized_disadvantages_label', 'Inconvénients :')
    optimized_disadvantages_desc = get_text('optimized_disadvantages_desc', 'Plus lent, nécessite vérification manuelle')
    optimized_usage_label = get_text('optimized_usage_label', 'Usage :')
    optimized_usage_desc = get_text('optimized_usage_desc', 'Extraction exhaustive, projets avec interface complexe')

    # Classification intelligente
    smart_classification_title = get_text('smart_classification_title', 'Classification intelligente (Mode Optimisé) :')
    auto_safe_label = get_text('auto_safe_label', 'Auto-safe :')
    auto_safe_desc = get_text('auto_safe_desc', 'Textes avec confiance 100% (Character(), input(), notify() confirmés)')
    textbuttons_label = get_text('textbuttons_label', 'Textbuttons :')
    textbuttons_desc = get_text('textbuttons_desc', 'Boutons d\'interface détectés nécessitant vérification')
    text_elements_label = get_text('text_elements_label', 'Text elements :')
    text_elements_desc = get_text('text_elements_desc', 'Éléments texte divers à examiner manuellement')

    # Système d'exclusions
    exclusions_system_title = get_text('exclusions_system_title', 'Système d\'exclusions intelligent')
    auto_exclusions_title = get_text('auto_exclusions_title', 'Exclusions automatiques (système) :')
    auto_exclusions_intro = get_text('auto_exclusions_intro', 'Le système exclut automatiquement ses propres fichiers générés :')
    lang_select_file_desc = get_text('lang_select_file_desc', 'Sélecteur de langue généré')
    console_file_desc = get_text('console_file_desc', 'Console développeur générée')
    recommended_exclusions_title = get_text('recommended_exclusions_title', 'Exclusions recommandées (configurables) :')
    system_files_desc = get_text('system_files_desc', 'Fichiers système Ren\'Py')
    base_config_desc = get_text('base_config_desc', 'Configuration de base')
    backup_temp_files_desc = get_text('backup_temp_files_desc', 'Fichiers de sauvegarde ou temporaires du projet')
    usage_tip_title = get_text('usage_tip_title', 'Conseil d\'utilisation')
    usage_tip_desc = get_text('usage_tip_desc', 'Commencez avec les exclusions par défaut, puis ajustez selon vos besoins. Un fichier exclu ne sera jamais analysé, ce qui accélère le processus.')

    # Exclusions automatiques avancées
    advanced_auto_exclusions_title = get_text('advanced_auto_exclusions_title', 'Exclusions automatiques avancées')
    advanced_auto_exclusions_intro = get_text('advanced_auto_exclusions_intro', 'Le système reconnaît automatiquement et exclut :')
    isolated_variables_label = get_text('isolated_variables_label', 'Variables isolées :')
    isolated_variables_desc = get_text('isolated_variables_desc', '[player_name] seul sur une ligne')
    technical_tags_label = get_text('technical_tags_label', 'Balises techniques :')
    technical_tags_desc = get_text('technical_tags_desc', '{fast}, {nw}, etc.')
    expressive_punctuation_label = get_text('expressive_punctuation_label', 'Ponctuations expressives :')
    expressive_punctuation_desc = get_text('expressive_punctuation_desc', '!!!, ???, ...')
    short_onomatopoeia_label = get_text('short_onomatopoeia_label', 'Onomatopées courtes :')
    short_onomatopoeia_desc = get_text('short_onomatopoeia_desc', 'Ah!, Oh?, Mmh')

    # Interface des résultats
    results_interface_title = get_text('results_interface_title', 'Interface des résultats - 3 catégories')
    results_categories_alt = get_text('results_categories_alt', 'Interface des résultats par catégories')
    results_categories_caption = get_text('results_categories_caption', 'Affichage en 3 colonnes avec scrollbars individuelles et statistiques détaillées')
    visual_organization_title = get_text('visual_organization_title', 'Organisation visuelle :')
    visual_organization_intro = get_text('visual_organization_intro', 'L\'interface des résultats s\'organise en 3 colonnes fixes avec scroll individuel pour optimiser l\'espace et la lisibilité :')
    auto_safe_column_title = get_text('auto_safe_column_title', 'Auto-safe (Gauche)')
    content_label = get_text('content_label', 'Contenu :')
    auto_safe_content = get_text('auto_safe_content', 'Textes à confiance 100%')
    default_selection_label = get_text('default_selection_label', 'Sélection par défaut :')
    auto_safe_selection = get_text('auto_safe_selection', 'Tous cochés')
    recommended_action_label = get_text('recommended_action_label', 'Action recommandée :')
    auto_safe_action = get_text('auto_safe_action', 'Extraction automatique sans vérification')
    textbuttons_column_title = get_text('textbuttons_column_title', 'Textbuttons (Centre)')
    textbuttons_content = get_text('textbuttons_content', 'Boutons d\'interface détectés')
    textbuttons_selection = get_text('textbuttons_selection', 'Non cochés')
    textbuttons_action = get_text('textbuttons_action', 'Vérification manuelle conseillée')
    text_elements_column_title = get_text('text_elements_column_title', 'Text Elements (Droite)')
    text_elements_content = get_text('text_elements_content', 'Éléments texte divers')
    text_elements_selection = get_text('text_elements_selection', 'Non cochés')
    text_elements_action = get_text('text_elements_action', 'Examen individuel nécessaire')

    # Fonctionnalités d'interaction
    interaction_features_title = get_text('interaction_features_title', 'Fonctionnalités d\'interaction :')
    selection_workflow_alt = get_text('selection_workflow_alt', 'Workflow de sélection')
    selection_workflow_caption = get_text('selection_workflow_caption', 'Démonstration des cases à cocher et boutons de sélection par section')
    section_selection_label = get_text('section_selection_label', 'Sélection par section :')
    section_selection_desc = get_text('section_selection_desc', 'Bouton "Tout cocher/décocher" dans chaque colonne')
    global_selection_label = get_text('global_selection_label', 'Sélection globale :')
    global_selection_desc = get_text('global_selection_desc', 'Boutons "Tout sélectionner" et "Tout désélectionner"')
    independent_scroll_label = get_text('independent_scroll_label', 'Scroll indépendant :')
    independent_scroll_desc = get_text('independent_scroll_desc', 'Chaque colonne a sa propre barre de défilement')
    wheel_support_label = get_text('wheel_support_label', 'Support molette :')
    wheel_support_desc = get_text('wheel_support_desc', 'Défilement à la molette dans chaque section')
    two_column_display_label = get_text('two_column_display_label', 'Affichage 2 colonnes :')
    two_column_display_desc = get_text('two_column_display_desc', 'Textes organisés en 2 colonnes dans chaque section pour optimiser l\'espace')

    # Statistiques d'analyse
    analysis_statistics_title = get_text('analysis_statistics_title', 'Statistiques d\'analyse')
    complete_statistics_alt = get_text('complete_statistics_alt', 'Statistiques complètes')
    complete_statistics_caption = get_text('complete_statistics_caption', 'Section statistiques avec métriques détaillées et indicateurs de performance')
    displayed_metrics_title = get_text('displayed_metrics_title', 'Métriques affichées :')
    basic_analysis_title = get_text('basic_analysis_title', 'Analyse de base')
    analyzed_files_count = get_text('analyzed_files_count', 'Nombre de fichiers analysés')
    existing_texts_count = get_text('existing_texts_count', 'Textes existants dans tl/ (anti-doublon)')
    detection_mode_used = get_text('detection_mode_used', 'Mode de détection utilisé')
    detection_results_title = get_text('detection_results_title', 'Résultats de détection')
    new_texts_total = get_text('new_texts_total', 'Total de nouveaux textes détectés')
    category_distribution = get_text('category_distribution', 'Répartition par catégorie')
    global_confidence_level = get_text('global_confidence_level', 'Niveau de confiance global')

    # Génération du fichier final
    final_file_generation_title = get_text('final_file_generation_title', 'Génération du fichier final')
    smart_save_dialog_alt = get_text('smart_save_dialog_alt', 'Dialogue de sauvegarde intelligent')
    smart_save_dialog_caption = get_text('smart_save_dialog_caption', 'Fenêtre de sauvegarde avec suggestion automatique du dossier tl/langue')
    smart_suggestions_title = get_text('smart_suggestions_title', 'Suggestions intelligentes :')
    auto_folder_label = get_text('auto_folder_label', 'Dossier automatique :')
    auto_folder_desc = get_text('auto_folder_desc', 'Le système propose le dossier tl/[langue] de la langue analysée')
    default_name_label = get_text('default_name_label', 'Nom par défaut :')
    default_name_desc = get_text('default_name_desc', '"textes_manquants.rpy" pour éviter les conflits')
    complete_metadata_label = get_text('complete_metadata_label', 'Métadonnées complètes :')
    complete_metadata_desc = get_text('complete_metadata_desc', 'Le fichier généré contient des commentaires avec contexte (projet, langue, mode, date)')

    # Contenu du fichier généré
    generated_file_content_title = get_text('generated_file_content_title', 'Contenu du fichier généré :')
    generated_file_structure_intro = get_text('generated_file_structure_intro', 'Structure du fichier .rpy créé :')
    informative_header_label = get_text('informative_header_label', 'En-tête informatif :')
    informative_header_desc = get_text('informative_header_desc', 'Date, projet, langue analysée, mode de détection')
    translate_block_label = get_text('translate_block_label', 'Bloc translate :')
    old_new_pairs_label = get_text('old_new_pairs_label', 'Paires old/new :')
    old_new_pairs_desc = get_text('old_new_pairs_desc', 'Chaque texte sélectionné avec structure old "texte"\\nnew "texte"')
    alphabetical_sort_label = get_text('alphabetical_sort_label', 'Tri alphabétique :')
    alphabetical_sort_desc = get_text('alphabetical_sort_desc', 'Textes organisés par ordre alphabétique pour faciliter l\'édition')

    # Conseils d'utilisation pratique
    practical_usage_tips_title = get_text('practical_usage_tips_title', 'Conseils d\'utilisation pratique')
    recommended_workflow_title = get_text('recommended_workflow_title', 'Workflow recommandé :')
    first_analysis_step = get_text('first_analysis_step', 'Première analyse :')
    first_analysis_desc = get_text('first_analysis_desc', 'Mode Optimisé avec exclusions par défaut')
    auto_safe_verification_step = get_text('auto_safe_verification_step', 'Vérification Auto-safe :')
    auto_safe_verification_desc = get_text('auto_safe_verification_desc', 'Extraire directement les textes verts (confiance 100%)')
    manual_examination_step = get_text('manual_examination_step', 'Examen manuel :')
    manual_examination_desc = get_text('manual_examination_desc', 'Parcourir les Textbuttons et Text elements')
    targeted_selection_step = get_text('targeted_selection_step', 'Sélection ciblée :')
    targeted_selection_desc = get_text('targeted_selection_desc', 'Ne cocher que les textes réellement utiles')
    generation_step = get_text('generation_step', 'Génération :')
    generation_desc = get_text('generation_desc', 'Créer le fichier dans le bon dossier tl/')
    testing_step = get_text('testing_step', 'Test :')
    testing_desc = get_text('testing_desc', 'Vérifier l\'intégration dans le jeu')

    # Astuces pour optimiser
    optimization_tips_title = get_text('optimization_tips_title', 'Astuces pour optimiser les résultats :')
    efficient_anti_duplicate_label = get_text('efficient_anti_duplicate_label', 'Anti-doublon efficace :')
    efficient_anti_duplicate_desc = get_text('efficient_anti_duplicate_desc', 'Assurez-vous d\'avoir une langue de référence bien remplie')
    custom_exclusions_label = get_text('custom_exclusions_label', 'Exclusions personnalisées :')
    custom_exclusions_desc = get_text('custom_exclusions_desc', 'Ajoutez vos fichiers de test ou temporaires')
    progressive_mode_label = get_text('progressive_mode_label', 'Mode progressif :')
    progressive_mode_desc = get_text('progressive_mode_desc', 'Commencez par Simple, puis Optimisé si pas assez de résultats')
    contextual_verification_label = get_text('contextual_verification_label', 'Vérification contextuelle :')
    contextual_verification_desc = get_text('contextual_verification_desc', 'Les textes détectés peuvent nécessiter un contexte pour être traduits correctement')

    # Section Combinaison
    combination_division_title = get_text('combination_division_title', 'Combinaison & Division')
    combination_interface_alt = get_text('combination_interface_alt', 'Générateur - Combinaison')
    combination_interface_caption = get_text('combination_interface_caption', 'Interface de combinaison et division de fichiers')
    combination_objective_title = get_text('combination_objective_title', 'Objectif')
    combination_objective_desc = get_text('combination_objective_desc', 'Fusionne plusieurs fichiers de traduction en un seul ou divise un fichier volumineux pour faciliter la traduction collaborative.')
    typical_use_cases_title = get_text('typical_use_cases_title', 'Cas d\'usage typiques')
    collaborative_translation_label = get_text('collaborative_translation_label', 'Traduction collaborative :')
    collaborative_translation_desc = get_text('collaborative_translation_desc', 'Divisez un gros fichier pour plusieurs traducteurs')
    optimization_label = get_text('optimization_label', 'Optimisation :')
    optimization_desc = get_text('optimization_desc', 'Combinez de petits fichiers en un seul pour simplifier')
    organization_label = get_text('organization_label', 'Organisation :')
    organization_desc = get_text('organization_desc', 'Restructurez vos fichiers selon vos préférences')

    # Fonctionnalités combinaison
    combination_features_title = get_text('combination_features_title', 'Fonctionnalités')
    smart_combination_title = get_text('smart_combination_title', 'Combinaison intelligente')
    smart_combination_desc = get_text('smart_combination_desc', 'Fusionne en préservant la structure des traductions')
    advantage_label = get_text('advantage_label', 'Avantage :')
    smart_combination_advantage = get_text('smart_combination_advantage', 'Aucune perte de données ou de formatage')
    balanced_division_title = get_text('balanced_division_title', 'Division équilibrée')
    balanced_division_desc = get_text('balanced_division_desc', 'Répartit les traductions de manière logique')
    balanced_division_method = get_text('balanced_division_method', 'Par nombre de lignes ou par sections')
    custom_exclusions_title = get_text('custom_exclusions_title', 'Exclusions personnalisées')
    flexibility_label = get_text('flexibility_label', 'Flexibilité :')
    custom_exclusions_flexibility = get_text('custom_exclusions_flexibility', 'Contrôle total sur le processus')
    preview_title = get_text('preview_title', 'Prévisualisation')
    preview_desc = get_text('preview_desc', 'Aperçu du résultat avant exécution')
    security_label = get_text('security_label', 'Sécurité :')
    preview_security = get_text('preview_security', 'Validation avant traitement')

    # Modes de fonctionnement
    operation_modes_title = get_text('operation_modes_title', 'Modes de fonctionnement')
    combination_mode_title = get_text('combination_mode_title', 'Mode Combinaison :')
    selection_step = get_text('selection_step', 'Sélection :')
    combination_selection_desc = get_text('combination_selection_desc', 'Choisissez les fichiers à fusionner')
    order_step = get_text('order_step', 'Ordre :')
    combination_order_desc = get_text('combination_order_desc', 'Définissez l\'ordre de fusion')
    output_name_step = get_text('output_name_step', 'Nom de sortie :')
    combination_output_name_desc = get_text('combination_output_name_desc', 'Spécifiez le nom du fichier résultat')
    validation_step = get_text('validation_step', 'Validation :')
    combination_validation_desc = get_text('combination_validation_desc', 'Vérifiez la prévisualisation')
    execution_step = get_text('execution_step', 'Exécution :')
    combination_execution_desc = get_text('combination_execution_desc', 'Lancez la combinaison')

    division_mode_title = get_text('division_mode_title', 'Mode Division :')
    source_file_step = get_text('source_file_step', 'Fichier source :')
    division_source_file_desc = get_text('division_source_file_desc', 'Sélectionnez le fichier à diviser')
    division_criteria_step = get_text('division_criteria_step', 'Critère de division :')
    division_criteria_desc = get_text('division_criteria_desc', 'Par taille, nombre de blocs, ou sections')
    prefix_step = get_text('prefix_step', 'Préfixe :')
    division_prefix_desc = get_text('division_prefix_desc', 'Nom de base pour les fichiers résultants')
    preview_step = get_text('preview_step', 'Aperçu :')
    division_preview_desc = get_text('division_preview_desc', 'Visualisez la répartition')
    division_step = get_text('division_step', 'Division :')
    division_execution_desc = get_text('division_execution_desc', 'Créez les fichiers')

    # Bonnes pratiques
    best_practices_title = get_text('best_practices_title', 'Bonnes pratiques')
    important_precautions_title = get_text('important_precautions_title', 'Précautions importantes')
    auto_backup_label = get_text('auto_backup_label', 'Sauvegarde automatique :')
    auto_backup_desc = get_text('auto_backup_desc', 'Les fichiers originaux sont sauvegardés')
    test_after_operation_label = get_text('test_after_operation_label', 'Test après opération :')
    test_after_operation_desc = get_text('test_after_operation_desc', 'Vérifiez que le jeu fonctionne toujours')
    naming_consistency_label = get_text('naming_consistency_label', 'Cohérence des noms :')
    naming_consistency_desc = get_text('naming_consistency_desc', 'Utilisez une convention de nommage claire')
    documentation_label = get_text('documentation_label', 'Documentation :')
    documentation_desc = get_text('documentation_desc', 'Notez les changements effectués')
    no_partial_recovery_label = get_text('no_partial_recovery_label', 'Pas de récupération partielle :')
    no_partial_recovery_desc = get_text('no_partial_recovery_desc', 'Le nettoyage est global par fichier')

    recommended_workflow_combination_title = get_text('recommended_workflow_combination_title', 'Workflow recommandé :')
    planning_label = get_text('planning_label', 'Planification :')
    planning_desc = get_text('planning_desc', 'Réfléchissez à l\'organisation souhaitée')
    copy_tests_label = get_text('copy_tests_label', 'Tests sur copies :')
    copy_tests_desc = get_text('copy_tests_desc', 'Essayez d\'abord sur des fichiers de test')
    validation_coherence_label = get_text('validation_coherence_label', 'Validation :')
    validation_coherence_desc = get_text('validation_coherence_desc', 'Utilisez le vérificateur de cohérence après')
    change_documentation_label = get_text('change_documentation_label', 'Documentation :')
    change_documentation_desc = get_text('change_documentation_desc', 'Gardez une trace des modifications')
# Navigation rapide - maintenir l'indentation
    return f"""
        <div class="quick-nav-section" style="background: var(--card-bg); padding: 20px; margin-bottom: 30px; border-radius: 8px; border-left: 4px solid #4a90e2;">
            <h3>🧭 {quick_nav_title}</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin-top: 15px;">
                <a href="#gen-extraction-rpa" class="nav-card-tab4" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">📦 {nav_extraction_rpa}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_extraction_rpa_desc}</div>
                </a>
                <a href="#gen-generation" class="nav-card-tab4" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">⚙️ {nav_generation}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_generation_desc}</div>
                </a>
                <a href="#gen-extraction-config" class="nav-card-tab4" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">🔧 {nav_extraction_config}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_extraction_config_desc}</div>
                </a>
                <a href="#gen-combinaison" class="nav-card-tab4" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">🔄 {nav_combinaison}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_combinaison_desc}</div>
                </a>
            </div>
        </div>
        
        <style>
        .nav-card-tab4:hover {{
            box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
            border-color: #4a90e2 !important;
            background: linear-gradient(135deg, var(--button-bg) 0%, rgba(74, 144, 226, 0.1) 100%) !important;
        }}
        </style>
        
        <div class="section" id="generator-window">
        <h2>🎮 {title}</h2>
        <p>{intro}</p>
        
        <h3>📋 {overview_title}</h3>
        <ul>
            <li><strong>📦 {extraction_compilation_tab}</strong> - {extraction_compilation_desc}</li>
            <li><strong>⚙️ {generation_tab}</strong> - {generation_desc}</li>
            <li><strong>🔧 {extraction_config_tab}</strong> - {extraction_config_desc}</li>
            <li><strong>📊 {extraction_results_tab}</strong> - {extraction_results_desc}</li>
            <li><strong>🔄 {combination_tab}</strong> - {combination_desc}</li>
        </ul>
        
        <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #10b981; margin: 15px 0;">
            <h4>📄 {reorganization_title}</h4>
            <p>{reorganization_desc}</p>
        </div>
    </div>

    <div class="section" id="gen-extraction-rpa">
        <h2>📦 {extraction_rpa_title}</h2>
        {generator._get_image_html("02_interface_generateur", "001", language, extraction_interface_alt, extraction_interface_caption)}
        
        <h3>🎯 {extraction_purpose_title}</h3>
        <p>{extraction_purpose_intro}</p>
        
        <div class="feature-grid">
            <div class="feature-card">
                <h5>📂 {extraction_rpa_rpyc_title}</h5>
                <p>{extraction_rpa_rpyc_desc}</p>
            </div>
            
            <div class="feature-card">
                <h5>🛠️ {custom_rpa_build_title}</h5>
                <p>{custom_rpa_build_desc}</p>
            </div>
        </div>
        
        <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #f59e0b; margin: 15px 0;">
            <h4>⚠️ {prerequisite_title}</h4>
            <p>{prerequisite_desc}</p>
        </div>
        
        <h3>🔧 {workflow_title}</h3>
        <ol>
            <li><strong>{auto_preparation_label}</strong> {auto_preparation_desc}</li>
            <li><strong>{smart_extraction_label}</strong> {smart_extraction_desc}</li>
            <li><strong>{cleanup_finalization_label}</strong> {cleanup_finalization_desc}</li>
        </ol>
        
        <h3>📂 {extraction_section_title}</h3>
        {generator._get_image_html("02_interface_generateur", "002", language, advanced_extraction_alt, advanced_extraction_caption)}
        
        <h4>{main_options_title}</h4>
        <ul>
            <li><strong>{delete_rpa_option}</strong> {delete_rpa_desc}</li>
            <li><strong>{start_extraction_button}</strong> {start_extraction_desc}</li>
            <li><strong>{path_help_button}</strong> {path_help_desc}</li>
        </ul>
        
        <h4>{smart_detection_title}</h4>
        <div class="feature-grid">
            <div class="feature-card">
                <h5>🔍 {renpy_version_title}</h5>
                <p><strong>{method_label}</strong> {renpy_version_method}</p>
                <p><strong>{auto_choice_label}</strong> {renpy_version_choice}</p>
            </div>
            
            <div class="feature-card">
                <h5>🐍 {compatible_python_title}</h5>
                <p><strong>{v1_label}</strong> {python_v1_desc}</p>
                <p><strong>{v2_label}</strong> {python_v2_desc}</p>
            </div>
            
            <div class="feature-card">
                <h5>🔄 {fallback_strategy_title}</h5>
                <p>{fallback_strategy_desc}</p>
            </div>
        </div>
        
        <h4>{important_limitations_title}</h4>
        {generator._get_image_html("02_interface_generateur", "003", language, path_limitations_alt, path_limitations_caption)}
        
        <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #ef4444; margin: 15px 0;">
            <h4>⚠️ {unsupported_paths_title}</h4>
            <p>{unsupported_paths_desc}</p>
            <p><strong>{problematic_examples_label}</strong></p>
            <ul>
                <li>❌ C:/Jeux/Mon Jeu [v1.0]/</li>
                <li>❌ D:/[Backup] Projets/MonProjet/</li>
            </ul>
            <p><strong>{solutions_label}</strong> {solutions_desc}</p>
        </div>
        
        <h3>🛠️ {custom_rpa_section_title}</h3>
        {generator._get_image_html("02_interface_generateur", "005", language, rpa_build_config_alt, rpa_build_config_caption)}
        
        <h4>{advanced_config_title}</h4>
        
        <h5>{language_selection_title}</h5>
        <ul>
            <li><strong>{scan_languages_button}</strong> {scan_languages_desc}</li>
            <li><strong>{smart_priority_label}</strong> {smart_priority_desc}</li>
            <li><strong>{validation_label}</strong> {validation_desc}</li>
        </ul>
        
        <h5>{file_types_title}</h5>
        <div class="feature-grid">
            <div class="feature-card">
                <h5>📄 {scripts_type_title}</h5>
                <p>{scripts_type_desc}</p>
            </div>
            
            <div class="feature-card">
                <h5>🖼️ {images_type_title}</h5>
                <p>{images_type_desc}</p>
            </div>
            
            <div class="feature-card">
                <h5>📊 {audio_type_title}</h5>
                <p>{audio_type_desc}</p>
            </div>
            
            <div class="feature-card">
                <h5>🔤 {fonts_type_title}</h5>
                <p>{fonts_type_desc}</p>
            </div>
        </div>
        
        <h3>⚡ {operations_flow_title}</h3>
        {generator._get_image_html("02_interface_generateur", "004", language, extraction_in_progress_alt, extraction_in_progress_caption)}
        
        <h4>{extraction_phase_title}</h4>
        <ol>
            <li><strong>{initialization_step}</strong> {initialization_desc}</li>
            <li><strong>{rpa_extraction_step}</strong> {rpa_extraction_desc}</li>
            <li><strong>{version_detection_step}</strong> {version_detection_desc}</li>
            <li><strong>{rpyc_decompilation_step}</strong> {rpyc_decompilation_desc}</li>
            <li><strong>{cleanup_step}</strong> {cleanup_desc}</li>
        </ol>
        
        <h3>📊 {results_reports_title}</h3>
        {generator._get_image_html("02_interface_generateur", "006", language, detailed_results_alt, detailed_results_caption)}
        
        <h4>{interactive_results_title}</h4>
        <p>{interactive_results_intro}</p>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; margin: 20px 0;">
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #10b981;">
                <h5>✅ {successful_extraction_title}</h5>
                <ul>
                    <li>{successful_extraction_1}</li>
                    <li>{successful_extraction_2}</li>
                    <li>{successful_extraction_3}</li>
                    <li>{successful_extraction_4}</li>
                </ul>
            </div>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #ef4444;">
                <h5>❌ {failure_management_title}</h5>
                <ul>
                    <li>{failure_management_1}</li>
                    <li>{failure_management_2}</li>
                    <li>{failure_management_3}</li>
                </ul>
            </div>
        </div>
    </div>

    <div class="section" id="gen-generation">
        <h2>⚙️ {generation_tl_title}</h2>
        {generator._get_image_html("02_interface_generateur", "007", language, generation_overview_alt, generation_overview_caption)}
        
        <h3>🎯 {generation_purpose_title}</h3>
        <p>{generation_purpose_intro}</p>
        
        <div class="workflow-step" data-step="1">
            <h4>{basic_config_step}</h4>
            <p>{basic_config_desc}</p>
        </div>
        
        <div class="workflow-step" data-step="2">
            <h4>{advanced_customization_step}</h4>
            <p>{advanced_customization_desc}</p>
        </div>
        
        <div class="workflow-step" data-step="3">
            <h4>{targeted_generation_step}</h4>
            <p>{targeted_generation_desc}</p>
        </div>
        
        <h3>🖥️ {user_interface_title}</h3>
        
        <h4>{basic_config_section_title}</h4>
        
        <h5>🌐 {target_language_title}</h5>
        <ul>
            <li><strong>{input_field_label}</strong> {input_field_desc}</li>
            <li><strong>{help_button_label}</strong> {help_button_desc}</li>
            <li><strong>{smart_autocomplete_label}</strong> {smart_autocomplete_desc}</li>
        </ul>
        
        <h5>📋 {options_grid_title}</h5>
        {generator._get_image_html("02_interface_generateur", "010", language, integration_options_alt, integration_options_caption)}
        
        <div class="feature-grid">
            <div class="feature-card">
                <h5>🔧 {language_selector_option_title}</h5>
                <p><strong>{checkbox_label}</strong> {language_selector_checkbox}</p>
                <p><strong>{action_label}</strong> {language_selector_action}</p>
                <p><strong>{help_label}</strong> {language_selector_help}</p>
            </div>
            
            <div class="feature-card">
                <h5>📚 {common_rpy_option_title}</h5>
                <p><strong>{checkbox_label}</strong> {common_rpy_checkbox}</p>
                <p><strong>{action_label}</strong> {common_rpy_action}</p>
                <p><strong>{help_label}</strong> {common_rpy_help}</p>
            </div>
            
            <div class="feature-card">
                <h5>🛠 {dev_console_option_title}</h5>
                <p><strong>{checkbox_label}</strong> {dev_console_checkbox}</p>
                <p><strong>{action_label}</strong> {dev_console_action}</p>
                <p><strong>{help_label}</strong> {dev_console_help}</p>
            </div>
            
            <div class="feature-card">
                <h5>🖼 {screen_rpy_option_title}</h5>
                <p><strong>{checkbox_label}</strong> {screen_rpy_checkbox}</p>
                <p><strong>{action_label}</strong> {screen_rpy_action}</p>
                <p><strong>{help_label}</strong> {screen_rpy_help}</p>
            </div>
        </div>
        
        <h4>{gui_fonts_section_title}</h4>
        
        <h5>👀 {font_preview_title}</h5>
        {generator._get_image_html("02_interface_generateur", "009", language, font_preview_alt, font_preview_caption)}
        
        <p>{preview_zone_desc}</p>
        <ul>
            <li><strong>{font_selector_label}</strong> {font_selector_desc}</li>
            <li><strong>{realtime_preview_label}</strong> {realtime_preview_desc}</li>
            <li><strong>{accent_test_label}</strong> {accent_test_desc}</li>
        </ul>
        
        <h5>🎛 {individual_config_title}</h5>
        {generator._get_image_html("02_interface_generateur", "008", language, gui_fonts_grid_alt, gui_fonts_grid_caption)}
        
        <p>{individual_config_intro}</p>
        
        <div class="feature-grid">
            <div class="feature-card">
                <h5>💬 {main_text_title}</h5>
                <p>{main_text_desc}</p>
            </div>
            
            <div class="feature-card">
                <h5>👤 {character_names_title}</h5>
                <p>{character_names_desc}</p>
            </div>
            
            <div class="feature-card">
                <h5>🖥 {user_interface_element_title}</h5>
                <p>{user_interface_element_desc}</p>
            </div>
            
            <div class="feature-card">
                <h5>📘 {general_buttons_title}</h5>
                <p>{general_buttons_desc}</p>
            </div>
            
            <div class="feature-card">
                <h5>🎯 {choice_buttons_title}</h5>
                <p>{choice_buttons_desc}</p>
            </div>
        </div>
        
        <h5>🔄 {rtl_option_title}</h5>
        <p>{rtl_option_desc}</p>
        
        <h3>⚡ {action_buttons_title}</h3>
        
        <div class="feature-grid">
            <div class="feature-card">
                <h5>🔧 {generate_translations_title}</h5>
                <p><strong>{action_label}</strong> {generate_translations_action}</p>
                <p><strong>{usage_label}</strong> {generate_translations_usage}</p>
            </div>
            
            <div class="feature-card">
                <h5>🎨 {apply_fonts_title}</h5>
                <p><strong>{action_label}</strong> {apply_fonts_action}</p>
                <p><strong>{usage_label}</strong> {apply_fonts_usage}</p>
            </div>
            
            <div class="feature-card">
                <h5>🔗 {add_selector_title}</h5>
                <p><strong>{action_label}</strong> {add_selector_action}</p>
                <p><strong>{usage_label}</strong> {add_selector_usage}</p>
            </div>
            
            <div class="feature-card">
                <h5>⚡ {generate_all_title}</h5>
                <p><strong>{action_label}</strong> {generate_all_action}</p>
                <p><strong>{usage_label}</strong> {generate_all_usage}</p>
            </div>
        </div>
    </div>

    <div class="section" id="gen-extraction-config">
        <h2>🔧 {extraction_config_title}</h2>
        {generator._get_image_html("02_interface_generateur", "012", language, config_extraction_complete_alt, config_extraction_complete_caption)}
        
        <h3>🎯 {config_extraction_purpose_title}</h3>
        <p>{config_extraction_purpose_intro}</p>
        
        <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #f39c12; margin: 15px 0;">
            <h4>💡 {why_necessary_title}</h4>
            <p>{why_necessary_desc}</p>
        </div>
        
        <h3>🖥️ {config_workflow_title}</h3>
        
        <div class="workflow-step" data-step="1">
            <h4>{config_step1_title}</h4>
            <p>{config_step1_desc}</p>
        </div>
        
        <div class="workflow-step" data-step="2">
            <h4>{config_step2_title}</h4>
            <p>{config_step2_desc}</p>
        </div>
        
        <div class="workflow-step" data-step="3">
            <h4>{config_step3_title}</h4>
            <p>{config_step3_desc}</p>
        </div>
        
        <h3>🌐 {language_selection_title}</h3>
        
        <h4>{auto_language_detection_title}</h4>
        <ul>
            <li><strong>{smart_scan_label}</strong> {smart_scan_desc}</li>
            <li><strong>{french_priority_label}</strong> {french_priority_desc}</li>
            <li><strong>{language_validation_label}</strong> {language_validation_desc}</li>
        </ul>
        
        <h4>{language_role_title}</h4>
        <p>{language_role_desc}</p>
        
        <h3>🎯 {detection_modes_title}</h3>
        {generator._get_image_html("02_interface_generateur", "014", language, detection_modes_help_alt, detection_modes_help_caption)}
        
        <div class="feature-grid">
            <div class="feature-card">
                <h5>🔹 {simple_mode_title}</h5>
                <p><strong>{basic_patterns_label}</strong> {basic_patterns_desc}</p>
                <p><strong>{simple_advantages_label}</strong> {simple_advantages_desc}</p>
                <p><strong>{simple_disadvantages_label}</strong> {simple_disadvantages_desc}</p>
                <p><strong>{simple_usage_label}</strong> {simple_usage_desc}</p>
            </div>
            
            <div class="feature-card">
                <h5>🔸 {optimized_mode_title}</h5>
                <p><strong>{advanced_patterns_label}</strong> {advanced_patterns_desc}</p>
                <p><strong>{optimized_advantages_label}</strong> {optimized_advantages_desc}</p>
                <p><strong>{optimized_disadvantages_label}</strong> {optimized_disadvantages_desc}</p>
                <p><strong>{optimized_usage_label}</strong> {optimized_usage_desc}</p>
            </div>
        </div>
        
        <h4>{smart_classification_title}</h4>
        <ul>
            <li><strong>{auto_safe_label}</strong> {auto_safe_desc}</li>
            <li><strong>{textbuttons_label}</strong> {textbuttons_desc}</li>
            <li><strong>{text_elements_label}</strong> {text_elements_desc}</li>
        </ul>
        
        <h3>🚫 {exclusions_system_title}</h3>
        
        <h4>{auto_exclusions_title}</h4>
        <p>{auto_exclusions_intro}</p>
        <ul>
            <li><code>99_Z_LangSelect.rpy</code> - {lang_select_file_desc}</li>
            <li><code>99_Z_Console.rpy</code> - {console_file_desc}</li>
        </ul>
        
        <h4>{recommended_exclusions_title}</h4>
        <ul>
            <li><code>common.rpy, screens.rpy</code> - {system_files_desc}</li>
            <li><code>gui.rpy, options.rpy</code> - {base_config_desc}</li>
            <li>{backup_temp_files_desc}</li>
        </ul>
        
        <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #10b981; margin: 15px 0;">
            <h4>💡 {usage_tip_title}</h4>
            <p>{usage_tip_desc}</p>
        </div>
        
        <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #4a90e2; margin: 15px 0;">
            <h4>💡 {advanced_auto_exclusions_title}</h4>
            <p>{advanced_auto_exclusions_intro}</p>
            <ul>
                <li><strong>{isolated_variables_label}</strong> {isolated_variables_desc}</li>
                <li><strong>{technical_tags_label}</strong> {technical_tags_desc}</li>
                <li><strong>{expressive_punctuation_label}</strong> {expressive_punctuation_desc}</li>
                <li><strong>{short_onomatopoeia_label}</strong> {short_onomatopoeia_desc}</li>
            </ul>
        </div>
    </div>

    <div class="section" id="gen-extraction-resultats">
        <h3>📊 {results_interface_title}</h3>
        {generator._get_image_html("02_interface_generateur", "013", language, results_categories_alt, results_categories_caption)}
        
        <h4>{visual_organization_title}</h4>
        <p>{visual_organization_intro}</p>
        
        <div class="feature-grid">
            <div class="feature-card">
                <h5>🟢 {auto_safe_column_title}</h5>
                <p><strong>{content_label}</strong> {auto_safe_content}</p>
                <p><strong>{default_selection_label}</strong> {auto_safe_selection}</p>
                <p><strong>{recommended_action_label}</strong> {auto_safe_action}</p>
            </div>
            
            <div class="feature-card">
                <h5>🟡 {textbuttons_column_title}</h5>
                <p><strong>{content_label}</strong> {textbuttons_content}</p>
                <p><strong>{default_selection_label}</strong> {textbuttons_selection}</p>
                <p><strong>{recommended_action_label}</strong> {textbuttons_action}</p>
            </div>
            
            <div class="feature-card">
                <h5>🟡 {text_elements_column_title}</h5>
                <p><strong>{content_label}</strong> {text_elements_content}</p>
                <p><strong>{default_selection_label}</strong> {text_elements_selection}</p>
                <p><strong>{recommended_action_label}</strong> {text_elements_action}</p>
            </div>
        </div>
        
        <h4>{interaction_features_title}</h4>
        {generator._get_image_html("02_interface_generateur", "015", language, selection_workflow_alt, selection_workflow_caption)}
        
        <ul>
            <li><strong>{section_selection_label}</strong> {section_selection_desc}</li>
            <li><strong>{global_selection_label}</strong> {global_selection_desc}</li>
            <li><strong>{independent_scroll_label}</strong> {independent_scroll_desc}</li>
            <li><strong>{wheel_support_label}</strong> {wheel_support_desc}</li>
            <li><strong>{two_column_display_label}</strong> {two_column_display_desc}</li>
        </ul>
        
        <h3>📈 {analysis_statistics_title}</h3>
        {generator._get_image_html("02_interface_generateur", "016", language, complete_statistics_alt, complete_statistics_caption)}
        
        <h4>{displayed_metrics_title}</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin: 20px 0;">
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #4a90e2;">
                <h5>📊 {basic_analysis_title}</h5>
                <ul>
                    <li>{analyzed_files_count}</li>
                    <li>{existing_texts_count}</li>
                    <li>{detection_mode_used}</li>
                </ul>
            </div>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #10b981;">
                <h5>🎯 {detection_results_title}</h5>
                <ul>
                    <li>{new_texts_total}</li>
                    <li>{category_distribution}</li>
                    <li>{global_confidence_level}</li>
                </ul>
            </div>
        </div>
        
        <h3>💾 {final_file_generation_title}</h3>
        {generator._get_image_html("02_interface_generateur", "017", language, smart_save_dialog_alt, smart_save_dialog_caption)}
        
        <h4>{smart_suggestions_title}</h4>
        <ul>
            <li><strong>{auto_folder_label}</strong> {auto_folder_desc}</li>
            <li><strong>{default_name_label}</strong> {default_name_desc}</li>
            <li><strong>{complete_metadata_label}</strong> {complete_metadata_desc}</li>
        </ul>
        
        <h4>{generated_file_content_title}</h4>
        <p>{generated_file_structure_intro}</p>
        <ul>
            <li><strong>{informative_header_label}</strong> {informative_header_desc}</li>
            <li><strong>{translate_block_label}</strong> <code>translate french strings:</code></li>
            <li><strong>{old_new_pairs_label}</strong> {old_new_pairs_desc}</li>
            <li><strong>{alphabetical_sort_label}</strong> {alphabetical_sort_desc}</li>
        </ul>
        
        <h3>💡 {practical_usage_tips_title}</h3>
        
        <h4>{recommended_workflow_title}</h4>
        <ol>
            <li><strong>{first_analysis_step}</strong> {first_analysis_desc}</li>
            <li><strong>{auto_safe_verification_step}</strong> {auto_safe_verification_desc}</li>
            <li><strong>{manual_examination_step}</strong> {manual_examination_desc}</li>
            <li><strong>{targeted_selection_step}</strong> {targeted_selection_desc}</li>
            <li><strong>{generation_step}</strong> {generation_desc}</li>
            <li><strong>{testing_step}</strong> {testing_desc}</li>
        </ol>
        
        <h4>{optimization_tips_title}</h4>
        <ul>
            <li><strong>{efficient_anti_duplicate_label}</strong> {efficient_anti_duplicate_desc}</li>
            <li><strong>{custom_exclusions_label}</strong> {custom_exclusions_desc}</li>
            <li><strong>{progressive_mode_label}</strong> {progressive_mode_desc}</li>
            <li><strong>{contextual_verification_label}</strong> {contextual_verification_desc}</li>
        </ul>
    </div>

    <div class="section" id="gen-combinaison">
        <h2>🔄 {combination_division_title}</h2>
        {generator._get_image_html("02_interface_generateur", "018", language, combination_interface_alt, combination_interface_caption)}
        
        <h3>🎯 {combination_objective_title}</h3>
        <p>{combination_objective_desc}</p>
        
        <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #4a90e2; margin: 15px 0;">
            <h4>💡 {typical_use_cases_title}</h4>
            <ul>
                <li><strong>{collaborative_translation_label}</strong> {collaborative_translation_desc}</li>
                <li><strong>{optimization_label}</strong> {optimization_desc}</li>
                <li><strong>{organization_label}</strong> {organization_desc}</li>
            </ul>
        </div>
        
        <h3>🛠️ {combination_features_title}</h3>
        
        <div class="feature-grid">
            <div class="feature-card">
                <h5>🔗 {smart_combination_title}</h5>
                <p>{smart_combination_desc}</p>
                <p><strong>{advantage_label}</strong> {smart_combination_advantage}</p>
            </div>
            
            <div class="feature-card">
                <h5>✂️ {balanced_division_title}</h5>
                <p>{balanced_division_desc}</p>
                <p><strong>{method_label}</strong> {balanced_division_method}</p>
            </div>
            
            <div class="feature-card">
                <h5>🚫 {custom_exclusions_title}</h5>
                <p>{custom_exclusions_desc}</p>
                <p><strong>{flexibility_label}</strong> {custom_exclusions_flexibility}</p>
            </div>
            
            <div class="feature-card">
                <h5>📊 {preview_title}</h5>
                <p>{preview_desc}</p>
                <p><strong>{security_label}</strong> {preview_security}</p>
            </div>
        </div>
        
        <h3>⚙️ {operation_modes_title}</h3>
        
        <h4>{combination_mode_title}</h4>
        <ol>
            <li><strong>{selection_step}</strong> {combination_selection_desc}</li>
            <li><strong>{order_step}</strong> {combination_order_desc}</li>
            <li><strong>{output_name_step}</strong> {combination_output_name_desc}</li>
            <li><strong>{validation_step}</strong> {combination_validation_desc}</li>
            <li><strong>{execution_step}</strong> {combination_execution_desc}</li>
        </ol>
        
        <h4>{division_mode_title}</h4>
        <ol>
            <li><strong>{source_file_step}</strong> {division_source_file_desc}</li>
            <li><strong>{division_criteria_step}</strong> {division_criteria_desc}</li>
            <li><strong>{prefix_step}</strong> {division_prefix_desc}</li>
            <li><strong>{preview_step}</strong> {division_preview_desc}</li>
            <li><strong>{division_step}</strong> {division_execution_desc}</li>
        </ol>
        
        <h3>🎯 {best_practices_title}</h3>
        
        <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #f59e0b; margin: 15px 0;">
            <h4>⚠️ {important_precautions_title}</h4>
            <ul>
                <li><strong>{auto_backup_label}</strong> {auto_backup_desc}</li>
                <li><strong>{test_after_operation_label}</strong> {test_after_operation_desc}</li>
                <li><strong>{naming_consistency_label}</strong> {naming_consistency_desc}</li>
                <li><strong>{documentation_label}</strong> {documentation_desc}</li>
            </ul>
        </div>
        
        <h4>{recommended_workflow_combination_title}</h4>
        <ul>
            <li><strong>{planning_label}</strong> {planning_desc}</li>
            <li><strong>{copy_tests_label}</strong> {copy_tests_desc}</li>
            <li><strong>{validation_coherence_label}</strong> {validation_coherence_desc}</li>
            <li><strong>{change_documentation_label}</strong> {change_documentation_desc}</li>
        </ul>
    </div>
    """