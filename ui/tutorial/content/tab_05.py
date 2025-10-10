# ui/tutorial/content/tab_05.py
"""
Module de contenu pour l'onglet 5 : Outils Spécialisés
"""

def generate_content(generator, language, translations):
    """
    Génère le contenu pour l'onglet 5 : Outils Spécialisés
    
    Args:
        generator: Instance du générateur avec méthodes utilitaires
        language: Code langue (fr, en, de)
        translations: Dictionnaire des traductions
    
    Returns:
        str: HTML généré pour l'onglet outils spécialisés
    """
    # Récupération des traductions pour cette section
    section_t = translations.get('tabs', {}).get('outils', {})
    common_t = translations.get('common', {})
   
    def get_text(key, fallback=""):
        return section_t.get(key) or common_t.get(key) or fallback

    # Navigation rapide
    quick_nav_title = get_text('quick_nav_title', 'Navigation rapide')
    nav_coherence_checker = get_text('nav_coherence_checker', 'Vérificateur de Cohérence')
    nav_coherence_desc = get_text('nav_coherence_desc', 'Détection d\'erreurs techniques dans les traductions')
    nav_realtime_editor = get_text('nav_realtime_editor', 'Éditeur Temps Réel')
    nav_realtime_desc = get_text('nav_realtime_desc', 'Modification en direct pendant le jeu')
    nav_smart_cleanup = get_text('nav_smart_cleanup', 'Nettoyage Intelligent')
    nav_cleanup_desc = get_text('nav_cleanup_desc', 'Suppression des blocs orphelins')

    # Vue d'ensemble générale
    title = get_text('title', 'Outils spécialisés')
    intro = get_text('intro', 'Ensemble d\'outils spécialisés pour maintenir la qualité et la cohérence de vos traductions.')
    overview_title = get_text('overview_title', 'Vue d\'ensemble des 3 outils')
    coherence_checker_title = get_text('coherence_checker_title', 'Vérificateur de Cohérence TL')
    coherence_checker_desc = get_text('coherence_checker_desc', 'Détection d\'erreurs techniques')
    realtime_editor_title = get_text('realtime_editor_title', 'Éditeur Temps Réel')
    realtime_editor_desc = get_text('realtime_editor_desc', 'Modification en direct pendant le jeu')
    smart_cleanup_title = get_text('smart_cleanup_title', 'Nettoyage Intelligent')
    smart_cleanup_desc = get_text('smart_cleanup_desc', 'Suppression des blocs orphelins')

    # Section Vérificateur de Cohérence
    coherence_detailed_title = get_text('coherence_detailed_title', 'Vérificateur de Cohérence TL - Guide Détaillé')
    coherence_interface_alt = get_text('coherence_interface_alt', 'Vérificateur de Cohérence - Interface complète')
    coherence_interface_caption = get_text('coherence_interface_caption', 'Vue d\'ensemble de l\'interface avec projet configuré et options sélectionnées')
    coherence_purpose_title = get_text('coherence_purpose_title', 'À quoi ça sert')
    coherence_purpose_intro = get_text('coherence_purpose_intro', 'Le Vérificateur de Cohérence détecte automatiquement les incohérences techniques entre les lignes originales (OLD) et traduites (NEW) dans vos fichiers .rpy. Il ne juge pas la qualité de votre traduction, mais s\'assure que vous n\'avez pas cassé la syntaxe du jeu.')
    why_essential_title = get_text('why_essential_title', 'Pourquoi c\'est essentiel')
    why_essential_desc = get_text('why_essential_desc', 'Une seule variable manquante ou une balise mal fermée peut faire planter tout le jeu. Ce vérificateur vous évite des heures de débogage en trouvant ces erreurs avant que vous ne testiez le jeu.')

    # Interface nouvelle
    new_interface_title = get_text('new_interface_title', 'Nouvelle interface intégrée aux Outils Spécialisés')
    new_interface_intro = get_text('new_interface_intro', 'Le vérificateur fait désormais partie des Outils de Maintenance Ren\'Py, accessible via l\'interface principale avec une approche harmonisée. L\'interface se structure autour de 3 sections principales :')
    centralized_config_step = get_text('centralized_config_step', 'Configuration centralisée')
    centralized_config_desc = get_text('centralized_config_desc', 'Projet piloté par l\'en-tête, sélection langue/fichiers unifiée')
    customizable_options_step = get_text('customizable_options_step', 'Options personnalisables')
    customizable_options_desc = get_text('customizable_options_desc', 'Types de vérifications et exclusions configurables')
    unified_analysis_step = get_text('unified_analysis_step', 'Analyse et rapport unifiés')
    unified_analysis_desc = get_text('unified_analysis_desc', 'Lancement intelligent avec résultats harmonisés')

    # Configuration unifiée
    unified_project_config_title = get_text('unified_project_config_title', 'Configuration unifiée du projet')
    project_selector_alt = get_text('project_selector_alt', 'Sélecteur de projet harmonisé')
    project_selector_caption = get_text('project_selector_caption', 'Widget unifié pour sélection langue et fichiers avec scan automatique')
    smart_selection_title = get_text('smart_selection_title', 'Sélection intelligente :')
    smart_selection_intro = get_text('smart_selection_intro', 'Le nouveau système utilise le widget ProjectLanguageSelector unifié qui offre :')
    header_driven_title = get_text('header_driven_title', 'Pilotage par l\'en-tête')
    header_driven_desc = get_text('header_driven_desc', 'Le projet est défini une fois dans l\'en-tête, puis partagé avec tous les outils')
    advantage_label = get_text('advantage_label', 'Avantage :')
    header_driven_advantage = get_text('header_driven_advantage', 'Cohérence entre tous les outils de maintenance')
    auto_language_scan_title = get_text('auto_language_scan_title', 'Scan automatique des langues')
    auto_language_scan_desc = get_text('auto_language_scan_desc', 'Détection automatique des dossiers tl/ avec priorité française')
    intelligence_label = get_text('intelligence_label', 'Intelligence :')
    auto_language_scan_intelligence = get_text('auto_language_scan_intelligence', 'Seules les langues avec fichiers .rpy sont proposées')
    flexible_selection_title = get_text('flexible_selection_title', 'Modes de sélection flexibles')
    flexible_selection_desc = get_text('flexible_selection_desc', 'Tous les fichiers de la langue OU fichier spécifique')
    granularity_label = get_text('granularity_label', 'Granularité :')
    flexible_selection_granularity = get_text('flexible_selection_granularity', 'Analyse complète ou ciblée selon les besoins')
    integrated_exclusions_title = get_text('integrated_exclusions_title', 'Exclusions intégrées')
    integrated_exclusions_desc = get_text('integrated_exclusions_desc', 'Les exclusions de fichiers sont appliquées automatiquement')
    efficiency_label = get_text('efficiency_label', 'Efficacité :')
    integrated_exclusions_efficiency = get_text('integrated_exclusions_efficiency', 'Pas de vérification sur les fichiers système')

    # Types de vérifications
    configurable_checks_title = get_text('configurable_checks_title', 'Types de vérifications configurables')
    check_options_alt = get_text('check_options_alt', 'Options de vérification détaillées')
    check_options_caption = get_text('check_options_caption', 'Configuration des types de vérifications et exclusions personnalisées')
    inconsistent_variables_title = get_text('inconsistent_variables_title', 'Variables [] incohérentes')
    detects_label = get_text('detects_label', 'Détecte :')
    inconsistent_variables_detects = get_text('inconsistent_variables_detects', 'Variables Ren\'Py manquantes, ajoutées ou mal écrites')
    example_label = get_text('example_label', 'Exemple :')
    inconsistent_variables_example = get_text('inconsistent_variables_example', '[player_name] dans OLD mais absent dans NEW')
    impact_label = get_text('impact_label', 'Impact :')
    inconsistent_variables_impact = get_text('inconsistent_variables_impact', 'Plantage du jeu avec erreur de variable')
    inconsistent_tags_title = get_text('inconsistent_tags_title', 'Balises {} incohérentes')
    inconsistent_tags_detects = get_text('inconsistent_tags_detects', 'Balises de formatage manquantes ou incorrectes')
    inconsistent_tags_example = get_text('inconsistent_tags_example', '{color=#ff0000}Texte{/color} mal fermé')
    inconsistent_tags_impact = get_text('inconsistent_tags_impact', 'Affichage cassé, texte non formaté')
    special_codes_title = get_text('special_codes_title', 'Codes spéciaux (\\\\n, --, %)')
    special_codes_detects = get_text('special_codes_detects', 'Caractères de contrôle modifiés par erreur')
    special_codes_example = get_text('special_codes_example', '\\\\n (retour ligne) supprimé ou mal échappé')
    special_codes_impact = get_text('special_codes_impact', 'Mise en page cassée, dialogues collés')
    untranslated_lines_title = get_text('untranslated_lines_title', 'Lignes non traduites')
    untranslated_lines_detects = get_text('untranslated_lines_detects', 'Texte identique entre OLD et NEW')
    untranslated_lines_example = get_text('untranslated_lines_example', '"Hello" conservé tel quel en français')
    untranslated_lines_impact = get_text('untranslated_lines_impact', 'Texte non traduit visible pour le joueur')

    # Nouvelles vérifications
    new_checks_title = get_text('new_checks_title', 'Nouvelles vérifications ajoutées :')
    inconsistent_parentheses_title = get_text('inconsistent_parentheses_title', '() Parenthèses incohérentes')
    new_label = get_text('new_label', 'Nouveau :')
    inconsistent_parentheses_new = get_text('inconsistent_parentheses_new', 'Vérification du nombre de parenthèses ouvrantes/fermantes')
    usage_label = get_text('usage_label', 'Usage :')
    inconsistent_parentheses_usage = get_text('inconsistent_parentheses_usage', 'Expressions mathématiques, conditions Ren\'Py')
    french_quotes_title = get_text('french_quotes_title', '« » Guillemets français')
    french_quotes_new = get_text('french_quotes_new', 'Support des guillemets français et de leurs équivalents <<>>')
    localization_label = get_text('localization_label', 'Localisation :')
    french_quotes_localization = get_text('french_quotes_localization', 'Respect de la typographie française')

    # Système d'exclusions
    smart_exclusions_title = get_text('smart_exclusions_title', 'Système d\'exclusions intelligent')
    files_to_exclude_title = get_text('files_to_exclude_title', 'Fichiers à exclure')
    configuration_label = get_text('configuration_label', 'Configuration :')
    files_to_exclude_config = get_text('files_to_exclude_config', 'common.rpy, Z_LangSelect.rpy, screens.rpy')
    functioning_label = get_text('functioning_label', 'Fonctionnement :')
    files_to_exclude_functioning = get_text('files_to_exclude_functioning', 'Correspondance partielle dans le nom de fichier')
    synchronization_label = get_text('synchronization_label', 'Synchronisation :')
    files_to_exclude_sync = get_text('files_to_exclude_sync', 'Partagé avec le sélecteur de projet')
    smart_line_exclusions_title = get_text('smart_line_exclusions_title', 'Exclusions lignes intelligentes')
    auto_exclusions_label = get_text('auto_exclusions_label', 'Auto-exclusions :')
    smart_line_exclusions_auto = get_text('smart_line_exclusions_auto', '..., variables seules, ellipsis, onomatopées')
    custom_label = get_text('custom_label', 'Personnalisées :')
    smart_line_exclusions_custom = get_text('smart_line_exclusions_custom', 'OK, Menu, Continue, Level, HP, MP')
    saving_label = get_text('saving_label', 'Sauvegarde :')
    smart_line_exclusions_saving = get_text('smart_line_exclusions_saving', 'Mémorisées entre les sessions')

    # Lancement et analyse
    launch_analysis_title = get_text('launch_analysis_title', 'Lancement et analyse harmonisés')
    centralized_control_title = get_text('centralized_control_title', 'Interface de contrôle centralisée :')
    centralized_control_intro = get_text('centralized_control_intro', 'La nouvelle interface unifie le lancement et l\'affichage des résultats :')
    realtime_status_label = get_text('realtime_status_label', 'État en temps réel :')
    realtime_status_desc = get_text('realtime_status_desc', 'Suivi du projet configuré et de la sélection active')
    smart_validation_label = get_text('smart_validation_label', 'Validation intelligente :')
    smart_validation_desc = get_text('smart_validation_desc', 'Vérification automatique avant lancement')
    contextual_info_label = get_text('contextual_info_label', 'Informations contextuelles :')
    contextual_info_desc = get_text('contextual_info_desc', 'Affichage du mode (tous fichiers vs spécifique)')
    post_analysis_actions_label = get_text('post_analysis_actions_label', 'Actions post-analyse :')
    post_analysis_actions_desc = get_text('post_analysis_actions_desc', 'Accès direct au rapport et au dossier')

    # Processus d'analyse optimisé
    optimized_analysis_process_title = get_text('optimized_analysis_process_title', 'Processus d\'analyse optimisé :')
    preliminary_validation_step = get_text('preliminary_validation_step', 'Validation préalable :')
    preliminary_validation_desc = get_text('preliminary_validation_desc', 'Vérification projet/langue/fichiers')
    auto_configuration_step = get_text('auto_configuration_step', 'Configuration automatique :')
    auto_configuration_desc = get_text('auto_configuration_desc', 'Application des exclusions sauvegardées')
    threaded_analysis_step = get_text('threaded_analysis_step', 'Analyse threadée :')
    threaded_analysis_desc = get_text('threaded_analysis_desc', 'Interface responsive pendant le traitement')
    report_generation_step = get_text('report_generation_step', 'Génération de rapport :')
    report_generation_desc = get_text('report_generation_desc', 'Rapport HTML avec métadonnées complètes')
    conditional_opening_step = get_text('conditional_opening_step', 'Ouverture conditionnelle :')
    conditional_opening_desc = get_text('conditional_opening_desc', 'Selon les paramètres utilisateur')

    # Rapport HTML modernisé
    modern_html_report_title = get_text('modern_html_report_title', 'Rapport HTML modernisé')
    html_report_alt = get_text('html_report_alt', 'Rapport HTML interactif')
    html_report_caption = get_text('html_report_caption', 'Rapport de cohérence ouvert dans le navigateur avec navigation par types d\'erreurs et statistiques détaillées')
    new_report_features_title = get_text('new_report_features_title', 'Nouvelles fonctionnalités du rapport :')
    enriched_metadata_title = get_text('enriched_metadata_title', 'Métadonnées enrichies')
    enriched_metadata_desc = get_text('enriched_metadata_desc', 'Informations sur le projet, langue analysée, mode de sélection')
    traceability_label = get_text('traceability_label', 'Traçabilité :')
    enriched_metadata_traceability = get_text('enriched_metadata_traceability', 'Contexte complet de l\'analyse')
    advanced_statistics_title = get_text('advanced_statistics_title', 'Statistiques avancées')
    advanced_statistics_desc = get_text('advanced_statistics_desc', 'Répartition par types d\'erreurs avec graphiques visuels')
    overview_label = get_text('overview_label', 'Vue d\'ensemble :')
    advanced_statistics_overview = get_text('advanced_statistics_overview', 'Problèmes prioritaires identifiés')
    smart_navigation_title = get_text('smart_navigation_title', 'Navigation intelligente')
    smart_navigation_desc = get_text('smart_navigation_desc', 'Filtrage par fichier, type d\'erreur, niveau de criticité')
    smart_navigation_efficiency = get_text('smart_navigation_efficiency', 'Accès direct aux problèmes spécifiques')
    adaptive_interface_title = get_text('adaptive_interface_title', 'Interface adaptive')
    adaptive_interface_desc = get_text('adaptive_interface_desc', 'Thème sombre/clair, responsive mobile, export PDF')
    comfort_label = get_text('comfort_label', 'Confort :')
    adaptive_interface_comfort = get_text('adaptive_interface_comfort', 'Consultation optimisée sur tous supports')

    # Cas d'usage nouvelle architecture
    use_cases_new_architecture_title = get_text('use_cases_new_architecture_title', 'Cas d\'usage avec la nouvelle architecture')
    integrated_daily_workflow_title = get_text('integrated_daily_workflow_title', 'Workflow quotidien intégré')
    context_label = get_text('context_label', 'Contexte :')
    integrated_daily_workflow_context = get_text('integrated_daily_workflow_context', 'Utilisation avec l\'Interface Principale')
    method_label = get_text('method_label', 'Méthode :')
    integrated_daily_workflow_method = get_text('integrated_daily_workflow_method', 'Projet partagé, vérification post-reconstruction automatique')
    integrated_daily_workflow_advantage = get_text('integrated_daily_workflow_advantage', 'Cohérence totale entre les outils')
    complete_project_verification_title = get_text('complete_project_verification_title', 'Vérification projet complet')
    complete_project_verification_context = get_text('complete_project_verification_context', 'Contrôle qualité avant publication')
    complete_project_verification_method = get_text('complete_project_verification_method', 'Mode "Tous les fichiers" avec exclusions personnalisées')
    result_label = get_text('result_label', 'Résultat :')
    complete_project_verification_result = get_text('complete_project_verification_result', 'Analyse exhaustive de toute la traduction')
    targeted_debugging_title = get_text('targeted_debugging_title', 'Débogage ciblé')
    targeted_debugging_context = get_text('targeted_debugging_context', 'Le jeu plante sur un dialogue spécifique')
    targeted_debugging_method = get_text('targeted_debugging_method', 'Mode "Fichier spécifique" pour analyse rapide')
    targeted_debugging_efficiency = get_text('targeted_debugging_efficiency', 'Identification immédiate du problème')
    automated_verification_title = get_text('automated_verification_title', 'Vérification automatisée')
    automated_verification_context = get_text('automated_verification_context', 'Intégration dans un processus de build')
    automated_verification_method = get_text('automated_verification_method', 'API harmonisée avec paramètres prédéfinis')
    evolution_label = get_text('evolution_label', 'Évolution :')
    automated_verification_evolution = get_text('automated_verification_evolution', 'Vers l\'automatisation complète')

    # Conseils d'utilisation optimale
    optimal_usage_tips_title = get_text('optimal_usage_tips_title', 'Conseils d\'utilisation optimale')
    recommended_config_title = get_text('recommended_config_title', 'Configuration recommandée :')
    first_use_label = get_text('first_use_label', 'Première utilisation :')
    first_use_desc = get_text('first_use_desc', 'Activez tous les types de vérifications')
    file_exclusions_label = get_text('file_exclusions_label', 'Exclusions fichiers :')
    file_exclusions_desc = get_text('file_exclusions_desc', 'common.rpy, screens.rpy au minimum')
    line_exclusions_label = get_text('line_exclusions_label', 'Exclusions lignes :')
    line_exclusions_desc = get_text('line_exclusions_desc', 'Ajoutez les termes récurrents de votre jeu')
    save_all_label = get_text('save_all_label', 'Sauvegarde :')
    save_all_desc = get_text('save_all_desc', 'Utilisez "💾 Sauvegarder tout" pour mémoriser vos paramètres')
    optimal_workflow_title = get_text('optimal_workflow_title', 'Workflow optimal avec les outils intégrés :')
    unique_project_step = get_text('unique_project_step', 'Projet unique :')
    unique_project_desc = get_text('unique_project_desc', 'Configurez une fois dans l\'en-tête')
    systematic_verification_step = get_text('systematic_verification_step', 'Vérification systématique :')
    systematic_verification_desc = get_text('systematic_verification_desc', 'Après chaque reconstruction')
    complete_analysis_step = get_text('complete_analysis_step', 'Analyse complète :')
    complete_analysis_desc = get_text('complete_analysis_desc', 'Avant chaque session de test')
    permanent_report_step = get_text('permanent_report_step', 'Rapport permanent :')
    permanent_report_desc = get_text('permanent_report_desc', 'Gardez le rapport ouvert pendant la correction')

    # Intégration autres outils
    integration_other_tools_title = get_text('integration_other_tools_title', 'Intégration avec les autres outils')
    integration_other_tools_intro = get_text('integration_other_tools_intro', 'Le vérificateur s\'intègre parfaitement avec :')
    realtime_editor_integration_label = get_text('realtime_editor_integration_label', 'Éditeur Temps Réel :')
    realtime_editor_integration_desc = get_text('realtime_editor_integration_desc', 'Vérification automatique après modification')
    smart_cleanup_integration_label = get_text('smart_cleanup_integration_label', 'Nettoyage Intelligent :')
    smart_cleanup_integration_desc = get_text('smart_cleanup_integration_desc', 'Analyse post-nettoyage')
    backup_manager_integration_label = get_text('backup_manager_integration_label', 'Gestionnaire Sauvegardes :')
    backup_manager_integration_desc = get_text('backup_manager_integration_desc', 'Sauvegarde avant corrections importantes')

    # Section Éditeur Temps Réel
    realtime_editor_detailed_title = get_text('realtime_editor_detailed_title', 'Éditeur Temps Réel - Guide Complet')
    realtime_editor_interface_alt = get_text('realtime_editor_interface_alt', 'Interface complète Éditeur Temps Réel')
    realtime_editor_interface_caption = get_text('realtime_editor_interface_caption', 'Vue d\'ensemble avec projet sélectionné et surveillance active')
    realtime_editor_purpose_title = get_text('realtime_editor_purpose_title', 'À quoi ça sert')
    realtime_editor_purpose_intro = get_text('realtime_editor_purpose_intro', 'L\'Éditeur Temps Réel permet de modifier les traductions pendant que le jeu fonctionne, sans redémarrage. Idéal pour peaufiner rapidement des dialogues, ajuster des traductions trop longues, ou corriger des erreurs détectées en cours de jeu.')
    workflow_revolution_title = get_text('workflow_revolution_title', 'Révolution du workflow')
    workflow_revolution_desc = get_text('workflow_revolution_desc', 'Terminé le cycle : Quitter le jeu → Modifier → Reconstruire → Relancer. Avec l\'éditeur temps réel, vous modifiez directement depuis le jeu avec Maj+R pour voir les changements instantanément.')

    # Installation et surveillance
    installation_monitoring_title = get_text('installation_monitoring_title', 'Installation et surveillance')
    installation_config_alt = get_text('installation_config_alt', 'Configuration installation et surveillance')
    installation_config_caption = get_text('installation_config_caption', 'Interface fusionnée avec options de langue, installation du module et contrôles de surveillance')
    config_3_steps_title = get_text('config_3_steps_title', 'Configuration en 3 étapes :')
    language_selection_step = get_text('language_selection_step', 'Sélection de langue')
    scan_languages_label = get_text('scan_languages_label', 'Scanner les langues :')
    language_selection_scan = get_text('language_selection_scan', 'Détection automatique des dossiers tl/ disponibles avec priorité française')
    validation_label = get_text('validation_label', 'Validation :')
    language_selection_validation = get_text('language_selection_validation', 'Seules les langues contenant des fichiers .rpy sont proposées')
    module_installation_step = get_text('module_installation_step', 'Installation du module')
    renpy_module_label = get_text('renpy_module_label', 'Module Ren\'Py :')
    module_installation_module = get_text('module_installation_module', 'Installe un fichier .rpy dans game/ qui surveille les dialogues')
    smart_update_label = get_text('smart_update_label', 'Mise à jour intelligente :')
    module_installation_update = get_text('module_installation_update', 'Réinstallation automatique recommandée après chaque update de RenExtract')
    monitoring_start_step = get_text('monitoring_start_step', 'Démarrage surveillance')
    translation_cache_label = get_text('translation_cache_label', 'Cache de traductions :')
    monitoring_start_cache = get_text('monitoring_start_cache', 'Construction automatique d\'un index en mémoire pour performances optimales')
    active_monitoring_label = get_text('active_monitoring_label', 'Monitoring actif :')
    monitoring_start_monitoring = get_text('monitoring_start_monitoring', 'Surveillance du fichier log_dialogues.txt en temps réel')
    unique_installation_title = get_text('unique_installation_title', 'Installation unique par projet')
    unique_installation_desc = get_text('unique_installation_desc', 'Le module s\'installe une seule fois par projet et fonctionne pour toutes les langues. Il est automatiquement activé dès le lancement du jeu.')

    # Raccourci F8
    f8_shortcut_title = get_text('f8_shortcut_title', 'Raccourci F8 et gestion plein écran')
    f8_guide_alt = get_text('f8_guide_alt', 'Guide installation et utilisation')
    f8_guide_caption = get_text('f8_guide_caption', 'Popup d\'aide complète avec workflow F8 et instructions plein écran')
    f8_functioning_title = get_text('f8_functioning_title', 'Fonctionnement du raccourci F8 :')
    smart_detection_label = get_text('smart_detection_label', 'Détection intelligente :')
    f8_functioning_detection = get_text('f8_functioning_detection', 'Le module détecte automatiquement si le jeu est en plein écran')
    auto_exit_label = get_text('auto_exit_label', 'Sortie automatique :')
    f8_functioning_exit = get_text('f8_functioning_exit', 'Passe en mode fenêtré si nécessaire pour permettre le focus')
    renextract_focus_label = get_text('renextract_focus_label', 'Focus RenExtract :')
    f8_functioning_focus = get_text('f8_functioning_focus', 'Met l\'éditeur au premier plan via une requête HTTP locale')
    f11_return_label = get_text('f11_return_label', 'Retour F11 :')
    f8_functioning_return = get_text('f8_functioning_return', 'Utilisez F11 dans le jeu pour revenir en plein écran')

    # Architecture technique
    technical_architecture_title = get_text('technical_architecture_title', 'Architecture technique :')
    integrated_local_server_title = get_text('integrated_local_server_title', 'Serveur local intégré')
    integrated_local_server_desc = get_text('integrated_local_server_desc', 'RenExtract démarre un serveur HTTP sur le port 8765 pour recevoir les requêtes F8')
    security_label = get_text('security_label', 'Sécurité :')
    integrated_local_server_security = get_text('integrated_local_server_security', 'Accessible uniquement en local (127.0.0.1)')
    multi_version_compatibility_title = get_text('multi_version_compatibility_title', 'Compatibilité multi-version')
    multi_version_compatibility_desc = get_text('multi_version_compatibility_desc', 'Support Ren\'Py 7 (Python 2) et Ren\'Py 8 (Python 3) avec détection automatique')
    robustness_label = get_text('robustness_label', 'Robustesse :')
    multi_version_compatibility_robustness = get_text('multi_version_compatibility_robustness', 'Fallback gracieux si la requête échoue')

    # Interface d'édition adaptative
    adaptive_editing_interface_title = get_text('adaptive_editing_interface_title', 'Interface d\'édition adaptative')
    supported_dialogue_types_title = get_text('supported_dialogue_types_title', '5 types de dialogues supportés :')
    simple_dialogues_title = get_text('simple_dialogues_title', 'Dialogues simples')
    simple_dialogues_alt = get_text('simple_dialogues_alt', 'Fenêtre détachée dialogues simples')
    simple_dialogues_caption = get_text('simple_dialogues_caption', 'Interface VO/VF côte à côte avec boutons d\'action')
    simple_dialogues_usage = get_text('simple_dialogues_usage', 'Dialogues classiques avec un seul personnage')
    interface_label = get_text('interface_label', 'Interface :')
    simple_dialogues_interface = get_text('simple_dialogues_interface', 'Zone VO (lecture seule) + Zone VF (éditable) + boutons utilitaires')
    undefined_speaker_title = get_text('undefined_speaker_title', 'Locuteur non défini')
    undefined_speaker_alt = get_text('undefined_speaker_alt', 'Interface locuteur non défini')
    undefined_speaker_caption = get_text('undefined_speaker_caption', 'Division VO et VF en locuteur/dialogue avec boutons individuels')
    undefined_speaker_usage = get_text('undefined_speaker_usage', 'Format "Nom" "Dialogue" avec deux segments distincts')
    undefined_speaker_advantage = get_text('undefined_speaker_advantage', 'Édition séparée du nom et du dialogue pour plus de précision')
    split_dialogues_title = get_text('split_dialogues_title', 'Dialogues divisés')
    split_dialogues_alt = get_text('split_dialogues_alt', 'Interface dialogues divisés')
    split_dialogues_caption = get_text('split_dialogues_caption', 'Mode split avec parties 1/2 et indicateurs visuels d\'état actif')
    split_dialogues_usage = get_text('split_dialogues_usage', 'Dialogues longs répartis sur plusieurs lignes')
    split_dialogues_interface = get_text('split_dialogues_interface', 'Division intelligente avec surbrillance de la partie active')
    multiple_choices_title = get_text('multiple_choices_title', 'Choix multiples')
    multiple_choices_alt = get_text('multiple_choices_alt', 'Interface choix multiples')
    multiple_choices_caption = get_text('multiple_choices_caption', 'Grille d\'options de menu avec traductions VO/VF alignées')
    multiple_choices_usage = get_text('multiple_choices_usage', 'Menus de choix du joueur avec plusieurs options')
    organization_label = get_text('organization_label', 'Organisation :')
    multiple_choices_organization = get_text('multiple_choices_organization', 'Grille 2x2 pour optimiser l\'espace d\'affichage')
    multiple_dialogues_title = get_text('multiple_dialogues_title', 'Dialogues multiples')
    multiple_dialogues_alt = get_text('multiple_dialogues_alt', 'Interface dialogues multiples')
    multiple_dialogues_caption = get_text('multiple_dialogues_caption', 'Grille de dialogues consécutifs avec boutons individuels')
    multiple_dialogues_usage = get_text('multiple_dialogues_usage', 'Séquences de dialogues rapides (combats, animations)')
    multiple_dialogues_efficiency = get_text('multiple_dialogues_efficiency', 'Traitement en lot avec sauvegarde groupée')

    # Boutons utilitaires intégrés
    integrated_utility_buttons_title = get_text('integrated_utility_buttons_title', 'Boutons utilitaires intégrés')
    utility_buttons_alt = get_text('utility_buttons_alt', 'Boutons utilitaires')
    utility_buttons_caption = get_text('utility_buttons_caption', 'Zoom sur les boutons Copier, DeepL et Google avec leurs fonctions')
    translation_assistance_tools_title = get_text('translation_assistance_tools_title', 'Outils d\'assistance à la traduction :')
    copy_button_title = get_text('copy_button_title', 'Copier')
    function_label = get_text('function_label', 'Fonction :')
    copy_button_function = get_text('copy_button_function', 'Copie le texte VO dans le presse-papier')
    copy_button_usage = get_text('copy_button_usage', 'Pour coller dans un traducteur externe ou référence')
    deepl_button_title = get_text('deepl_button_title', 'DeepL')
    deepl_button_function = get_text('deepl_button_function', 'Copie + ouvre DeepL avec le texte pré-rempli')
    deepl_button_advantage = get_text('deepl_button_advantage', 'Traduction contextuelle immédiate')
    google_button_title = get_text('google_button_title', 'Google')
    google_button_function = get_text('google_button_function', 'Ouvre Google Translate avec détection auto de la langue')
    complementary_label = get_text('complementary_label', 'Complémentaire :')
    google_button_complementary = get_text('google_button_complementary', 'Alternative ou vérification croisée')
    paste_button_title = get_text('paste_button_title', 'Coller')
    paste_button_function = get_text('paste_button_function', 'Colle le contenu du presse-papier dans la zone VF')
    workflow_label = get_text('workflow_label', 'Workflow :')
    paste_button_workflow = get_text('paste_button_workflow', 'Récupération depuis traducteur externe')
    detach_button_title = get_text('detach_button_title', 'Détacher/Rattacher')
    detach_button_function = get_text('detach_button_function', 'Ouvre l\'éditeur dans une fenêtre séparée')
    detach_button_advantage = get_text('detach_button_advantage', 'Réduit la pollution visuelle du module principal')
    font_size_selector_title = get_text('font_size_selector_title', 'Sélecteur de taille police')
    font_size_selector_function = get_text('font_size_selector_function', 'Agrandit la police d\'écriture dans les zones de texte')
    scope_label = get_text('scope_label', 'Portée :')
    font_size_selector_scope = get_text('font_size_selector_scope', 'Améliore la lisibilité des traductions (pas celle du jeu)')

    # Boutons de mode avancé
    advanced_mode_buttons_title = get_text('advanced_mode_buttons_title', 'Boutons de mode avancé :')
    split_merge_label = get_text('split_merge_label', 'Diviser/Fusionner :')
    split_merge_desc = get_text('split_merge_desc', 'Bascule entre mode simple et mode split pour les longs dialogues')
    detach_attach_label = get_text('detach_attach_label', 'Détacher/Rattacher :')
    detach_attach_desc = get_text('detach_attach_desc', 'Ouvre l\'éditeur dans une fenêtre séparée pour plus de confort')
    open_label = get_text('open_label', 'Ouvrir :')
    open_desc = get_text('open_desc', 'Accès direct au fichier .rpy dans votre éditeur de code')

    # Système de modifications en attente
    pending_modifications_system_title = get_text('pending_modifications_system_title', 'Système de modifications en attente')
    crash_recovery_alt = get_text('crash_recovery_alt', 'Récupération après crash')
    crash_recovery_caption = get_text('crash_recovery_caption', 'Dialog de récupération avec statistiques des modifications en attente')
    anti_loss_security_title = get_text('anti_loss_security_title', 'Sécurité anti-perte :')
    persistent_json_cache_title = get_text('persistent_json_cache_title', 'Cache JSON persistant')
    persistent_json_cache_desc = get_text('persistent_json_cache_desc', 'Toutes les modifications sont stockées en temps réel dans un fichier JSON')
    protection_label = get_text('protection_label', 'Protection :')
    persistent_json_cache_protection = get_text('persistent_json_cache_protection', 'Aucune perte même en cas de crash')
    smart_recovery_title = get_text('smart_recovery_title', 'Récupération intelligente')
    smart_recovery_desc = get_text('smart_recovery_desc', 'Au redémarrage, proposition automatique de récupérer les modifications non sauvées')
    detail_label = get_text('detail_label', 'Détail :')
    smart_recovery_detail = get_text('smart_recovery_detail', 'Statistiques par type de modification')
    grouped_save_title = get_text('grouped_save_title', 'Sauvegarde groupée')
    grouped_save_desc = get_text('grouped_save_desc', 'Un seul bouton "Enregistrer" traite toutes les modifications en attente')
    grouped_save_efficiency = get_text('grouped_save_efficiency', 'Backup automatique avant chaque sauvegarde')

    # Types de modifications supportées
    supported_modification_types_title = get_text('supported_modification_types_title', 'Types de modifications supportées :')
    simple_mod_label = get_text('simple_mod_label', 'Simple :')
    simple_mod_desc = get_text('simple_mod_desc', 'Remplacement direct du texte VF')
    split_mod_label = get_text('split_mod_label', 'Split :')
    split_mod_desc = get_text('split_mod_desc', 'Division en deux parties avec textes distincts')
    speaker_dialogue_mod_label = get_text('speaker_dialogue_mod_label', 'Speaker_dialogue :')
    speaker_dialogue_mod_desc = get_text('speaker_dialogue_mod_desc', 'Modification séparée locuteur + dialogue')
    merge_mod_label = get_text('merge_mod_label', 'Merge :')
    merge_mod_desc = get_text('merge_mod_desc', 'Fusion de plusieurs lignes en une seule')

    # Cas d'usage pratiques
    practical_use_cases_title = get_text('practical_use_cases_title', 'Cas d\'usage pratiques')
    length_adjustments_title = get_text('length_adjustments_title', 'Ajustements de longueur')
    problem_label = get_text('problem_label', 'Problème :')
    length_adjustments_problem = get_text('length_adjustments_problem', 'Texte qui dépasse de l\'écran du jeu')
    solution_label = get_text('solution_label', 'Solution :')
    length_adjustments_solution = get_text('length_adjustments_solution', 'Modification immédiate + Maj+R pour vérifier l\'affichage')
    contextual_corrections_title = get_text('contextual_corrections_title', 'Corrections en contexte')
    contextual_corrections_problem = get_text('contextual_corrections_problem', 'Traduction incohérente détectée en jouant')
    contextual_corrections_solution = get_text('contextual_corrections_solution', 'F8 → Correction → Sauvegarde → Retour au jeu')
    style_adaptation_title = get_text('style_adaptation_title', 'Adaptation de style')
    style_adaptation_problem = get_text('style_adaptation_problem', 'Ton de personnage à ajuster')
    style_adaptation_solution = get_text('style_adaptation_solution', 'Tests multiples en temps réel avec feedback immédiat')
    collaborative_review_title = get_text('collaborative_review_title', 'Révision collaborative')
    collaborative_review_context = get_text('collaborative_review_context', 'Relecture avec retours en direct')
    collaborative_review_advantage = get_text('collaborative_review_advantage', 'Corrections immédiates pendant la session de test')

    # Conseils d'utilisation optimale éditeur temps réel
    optimal_usage_tips_realtime_title = get_text('optimal_usage_tips_realtime_title', 'Conseils d\'utilisation optimale')
    recommended_workflow_realtime_title = get_text('recommended_workflow_realtime_title', 'Workflow recommandé :')
    unique_installation_step = get_text('unique_installation_step', 'Installation unique :')
    unique_installation_step_desc = get_text('unique_installation_step_desc', 'Configurez une fois par projet')
    game_session_step = get_text('game_session_step', 'Session de jeu :')
    game_session_step_desc = get_text('game_session_step_desc', 'Démarrez la surveillance puis lancez le jeu')
    contextual_translation_step = get_text('contextual_translation_step', 'Traduction contextuelle :')
    contextual_translation_step_desc = get_text('contextual_translation_step_desc', 'Jouez normalement, F8 pour modifier')
    immediate_test_step = get_text('immediate_test_step', 'Test immédiat :')
    immediate_test_step_desc = get_text('immediate_test_step_desc', 'Maj+R dans le jeu pour voir les changements')
    grouped_save_step = get_text('grouped_save_step', 'Sauvegarde groupée :')
    grouped_save_step_desc = get_text('grouped_save_step_desc', 'En fin de session pour valider toutes les modifications')
    practical_tips_title = get_text('practical_tips_title', 'Astuces pratiques :')
    detached_mode_label = get_text('detached_mode_label', 'Mode détaché :')
    detached_mode_desc = get_text('detached_mode_desc', 'Plus confortable sur plusieurs écrans')
    translation_cache_tip_label = get_text('translation_cache_tip_label', 'Cache de traductions :')
    translation_cache_tip_desc = get_text('translation_cache_tip_desc', 'Première ouverture plus lente, puis très rapide')
    external_buttons_label = get_text('external_buttons_label', 'Boutons externes :')
    external_buttons_desc = get_text('external_buttons_desc', 'DeepL et Google s\'ouvrent dans le navigateur par défaut')
    ctrl_s_shortcut_label = get_text('ctrl_s_shortcut_label', 'Raccourci Ctrl+S :')
    ctrl_s_shortcut_desc = get_text('ctrl_s_shortcut_desc', 'Sauvegarde rapide depuis l\'interface')

    # Limitations importantes éditeur temps réel
    important_limitations_realtime_title = get_text('important_limitations_realtime_title', 'Limitations importantes')
    one_project_at_time_label = get_text('one_project_at_time_label', 'Un projet à la fois :')
    one_project_at_time_desc = get_text('one_project_at_time_desc', 'La surveillance ne fonctionne que pour un jeu simultanément')
    recommended_stop_label = get_text('recommended_stop_label', 'Arrêt recommandé :')
    recommended_stop_desc = get_text('recommended_stop_desc', 'Stoppez la surveillance avant de changer de projet')
    performance_label = get_text('performance_label', 'Performance :')
    performance_desc = get_text('performance_desc', 'Cache initial plus lent sur de très gros projets')
    compatibility_label = get_text('compatibility_label', 'Compatibilité :')
    compatibility_desc = get_text('compatibility_desc', 'Nécessite un jeu Ren\'Py fonctionnel avec fichiers non corrompus')

    # Section Nettoyage Intelligent
    smart_cleanup_detailed_title = get_text('smart_cleanup_detailed_title', 'Nettoyage Intelligent - Guide Détaillé')
    smart_cleanup_interface_alt = get_text('smart_cleanup_interface_alt', 'Interface complète Nettoyage TL')
    smart_cleanup_interface_caption = get_text('smart_cleanup_interface_caption', 'Vue d\'ensemble avec projet configuré, sélection de langues et exclusions')
    smart_cleanup_purpose_title = get_text('smart_cleanup_purpose_title', 'À quoi ça sert')
    smart_cleanup_purpose_intro = get_text('smart_cleanup_purpose_intro', 'Le Nettoyage Intelligent supprime automatiquement les blocs de traduction orphelins - ces lignes de traduction qui n\'ont plus de correspondance dans les fichiers source du jeu. Il combine deux méthodes complémentaires pour un nettoyage optimal :')
    lint_based_cleanup_title = get_text('lint_based_cleanup_title', 'Nettoyage basé sur lint.txt')
    lint_based_cleanup_desc = get_text('lint_based_cleanup_desc', 'Utilise l\'analyse officielle du SDK Ren\'Py pour détecter les IDs de traduction orphelins')
    lint_based_cleanup_advantage = get_text('lint_based_cleanup_advantage', 'Précision maximale basée sur l\'analyse officielle')
    correspondence_cleanup_title = get_text('correspondence_cleanup_title', 'Nettoyage par correspondance')
    correspondence_cleanup_desc = get_text('correspondence_cleanup_desc', 'Vérifie si les textes OLD existent encore dans les fichiers source du jeu')
    complement_label = get_text('complement_label', 'Complément :')
    correspondence_cleanup_complement = get_text('correspondence_cleanup_complement', 'Détecte les orphelins manqués par lint')
    why_necessary_cleanup_title = get_text('why_necessary_cleanup_title', 'Pourquoi c\'est nécessaire')
    why_necessary_cleanup_desc = get_text('why_necessary_cleanup_desc', 'Lors des mises à jour de jeux, certains dialogues sont supprimés ou modifiés. Vos anciens fichiers de traduction gardent ces lignes obsolètes qui encombrent l\'interface et peuvent parfois causer des dysfonctionnements.')

    # Workflow nettoyage
    cleanup_workflow_title = get_text('cleanup_workflow_title', 'Workflow en 3 étapes')
    smart_configuration_step = get_text('smart_configuration_step', 'Configuration intelligente')
    smart_configuration_desc = get_text('smart_configuration_desc', 'Sélection du projet, scan automatique des langues, personnalisation des exclusions')
    auto_lint_generation_step = get_text('auto_lint_generation_step', 'Génération lint automatique')
    auto_lint_generation_desc = get_text('auto_lint_generation_desc', 'Téléchargement SDK si nécessaire, génération lint.txt, analyse des orphelins')
    unified_cleanup_step = get_text('unified_cleanup_step', 'Nettoyage unifié')
    unified_cleanup_desc = get_text('unified_cleanup_desc', 'Sauvegarde automatique + suppression intelligente avec un seul backup par fichier')

    # Sélection des langues optimisée
    language_selection_optimized_title = get_text('language_selection_optimized_title', 'Sélection des langues avec interface optimisée')
    column_organization_title_3 = get_text('column_organization_title_3', 'Organisation en 3 colonnes :')
    column_organization_intro_3 = get_text('column_organization_intro_3', 'Le système affiche les langues détectées dans une grille équilibrée à 3 colonnes pour optimiser l\'espace et la lisibilité :')
    contextual_icons_label = get_text('contextual_icons_label', 'Icônes contextuelles :')
    contextual_icons_desc = get_text('contextual_icons_desc', '🗣️ pour les langues génériques, 🌐 pour English')
    numbered_badges_label = get_text('numbered_badges_label', 'Badges numérotés :')
    numbered_badges_desc = get_text('numbered_badges_desc', 'Chaque langue a un numéro pour faciliter le suivi')
    formatted_title_label = get_text('formatted_title_label', 'Titre formaté :')
    formatted_title_desc = get_text('formatted_title_desc', 'Première lettre en majuscule automatiquement')
    default_selection_label = get_text('default_selection_label', 'Sélection par défaut :')
    default_selection_desc = get_text('default_selection_desc', 'Toutes les langues cochées initialement')

    # Contrôles rapides nettoyage
    quick_controls_title = get_text('quick_controls_title', 'Contrôles rapides :')
    scan_languages_title = get_text('scan_languages_title', 'Scanner les langues')
    scan_languages_desc = get_text('scan_languages_desc', 'Détection automatique des dossiers tl/ contenant des fichiers .rpy exploitables')
    select_all_title = get_text('select_all_title', 'Tout sélectionner')
    select_all_desc = get_text('select_all_desc', 'Cocher toutes les langues d\'un coup pour traitement global')
    deselect_all_title = get_text('deselect_all_title', 'Tout désélectionner')
    deselect_all_desc = get_text('deselect_all_desc', 'Décocher toutes les langues pour sélection manuelle précise')

    # Système d'exclusions avancé nettoyage
    advanced_exclusions_system_title = get_text('advanced_exclusions_system_title', 'Système d\'exclusions avancé')
    custom_exclusions_help_alt = get_text('custom_exclusions_help_alt', 'Aide exclusions personnalisées')
    custom_exclusions_help_caption = get_text('custom_exclusions_help_caption', 'Popup d\'aide avec exemples pratiques et formatage stylé')
    configurable_exclusions_title = get_text('configurable_exclusions_title', 'Exclusions configurables :')
    configurable_exclusions_intro = get_text('configurable_exclusions_intro', 'Section intégrée directement dans l\'onglet pour personnaliser les fichiers à ignorer lors du nettoyage :')
    flexible_configuration_title = get_text('flexible_configuration_title', 'Configuration flexible')
    flexible_configuration_1 = get_text('flexible_configuration_1', 'Saisie libre séparée par virgules')
    flexible_configuration_2 = get_text('flexible_configuration_2', 'Bouton "Par défaut" pour reset rapide')
    flexible_configuration_3 = get_text('flexible_configuration_3', 'Aide contextuelle avec exemples')
    auto_protection_title = get_text('auto_protection_title', 'Protection automatique')
    auto_protection_1 = get_text('auto_protection_1', 'common.rpy : Fichier système Ren\'Py')
    auto_protection_2 = get_text('auto_protection_2', 'Z_LangSelect.rpy : Sélecteur de langue généré')
    auto_protection_3 = get_text('auto_protection_3', 'Vos fichiers personnalisés')

    # Logique d'exclusion nettoyage
    exclusion_logic_title = get_text('exclusion_logic_title', 'Logique d\'exclusion')
    exact_match_label = get_text('exact_match_label', 'Correspondance exacte :')
    exact_match_desc = get_text('exact_match_desc', 'Le nom de fichier doit correspondre exactement')
    case_insensitive_label = get_text('case_insensitive_label', 'Insensible à la casse :')
    case_insensitive_desc = get_text('case_insensitive_desc', 'common.rpy = Common.rpy = COMMON.rpy')
    extension_required_label = get_text('extension_required_label', 'Extension requise :')
    extension_required_desc = get_text('extension_required_desc', 'Spécifiez toujours l\'extension .rpy')
    auto_save_label = get_text('auto_save_label', 'Sauvegarde automatique :')
    auto_save_desc = get_text('auto_save_desc', 'Modifications enregistrées instantanément')

    # Processus de nettoyage automatisé
    automated_cleanup_process_title = get_text('automated_cleanup_process_title', 'Processus de nettoyage automatisé')
    cleanup_progress_alt = get_text('cleanup_progress_alt', 'Nettoyage en progression')
    cleanup_progress_caption = get_text('cleanup_progress_caption', 'Interface pendant le nettoyage avec étapes détaillées et barre de progression')
    integrated_sdk_title = get_text('integrated_sdk_title', 'SDK intégré et téléchargement automatique :')
    sdk_validation_step = get_text('sdk_validation_step', 'Validation du SDK (0-10%) :')
    sdk_validation_desc = get_text('sdk_validation_desc', 'Vérification SDK configuré ou téléchargement automatique')
    preliminary_cleanup_step = get_text('preliminary_cleanup_step', 'Nettoyage préliminaire (10-20%) :')
    preliminary_cleanup_desc = get_text('preliminary_cleanup_desc', 'Suppression des fichiers problématiques temporaires')
    lint_generation_step = get_text('lint_generation_step', 'Génération lint (20-60%) :')
    lint_generation_desc = get_text('lint_generation_desc', 'Exécution renpy.exe avec gestion des timeouts')
    unified_analysis_step_cleanup = get_text('unified_analysis_step_cleanup', 'Analyse unifiée (60-90%) :')
    unified_analysis_desc_cleanup = get_text('unified_analysis_desc_cleanup', 'Détection des orphelins avec double méthode')
    backup_deletion_step = get_text('backup_deletion_step', 'Sauvegarde & suppression (90-100%) :')
    backup_deletion_desc = get_text('backup_deletion_desc', 'Backup unifié + nettoyage final')

    # Gestion des échecs et optimisations nettoyage
    sdk_failure_management_title = get_text('sdk_failure_management_title', 'Gestion des échecs SDK')
    smart_fallback_label = get_text('smart_fallback_label', 'Fallback intelligent :')
    sdk_failure_management_desc = get_text('sdk_failure_management_desc', 'Si le SDK échoue, création d\'un lint minimal basé sur l\'analyse des fichiers de traduction')
    single_backup_title = get_text('single_backup_title', 'Un seul backup par fichier')
    optimization_label = get_text('optimization_label', 'Optimisation :')
    single_backup_desc = get_text('single_backup_desc', 'Sauvegarde unifiée avant toute modification, évite les doublons de backups')
    timeout_management_title = get_text('timeout_management_title', 'Gestion des timeouts')
    timeout_management_desc = get_text('timeout_management_desc', 'Limitation à 3 minutes par tentative SDK, plusieurs stratégies de commandes')

    # Résultats et rapports détaillés nettoyage
    detailed_results_reports_title = get_text('detailed_results_reports_title', 'Résultats et rapports détaillés')
    cleanup_results_alt = get_text('cleanup_results_alt', 'Résultats de nettoyage')
    cleanup_results_caption = get_text('cleanup_results_caption', 'Popup avec statistiques complètes et actions post-nettoyage')
    interactive_results_popup_title = get_text('interactive_results_popup_title', 'Popup de résultats interactif :')
    interactive_results_popup_intro = get_text('interactive_results_popup_intro', 'À la fin du nettoyage, présentation des résultats avec statistiques détaillées :')
    cleanup_metrics_title = get_text('cleanup_metrics_title', 'Métriques de nettoyage')
    cleanup_metrics_1 = get_text('cleanup_metrics_1', 'Nombre de langues traitées')
    cleanup_metrics_2 = get_text('cleanup_metrics_2', 'Total de fichiers analysés')
    cleanup_metrics_3 = get_text('cleanup_metrics_3', 'Blocs orphelins supprimés (lint + chaînes)')
    cleanup_metrics_4 = get_text('cleanup_metrics_4', 'Temps d\'exécution formaté')
    interactive_html_report_title = get_text('interactive_html_report_title', 'Rapport HTML interactif')
    interactive_html_report_1 = get_text('interactive_html_report_1', 'Structure hiérarchique par jeu/type')
    interactive_html_report_2 = get_text('interactive_html_report_2', 'Navigation par catégories d\'erreurs')
    interactive_html_report_3 = get_text('interactive_html_report_3', 'Thème sombre/clair adaptatif')
    interactive_html_report_4 = get_text('interactive_html_report_4', 'Export et partage facilités')

    # Actions post-nettoyage
    post_cleanup_actions_title = get_text('post_cleanup_actions_title', 'Actions post-nettoyage :')
    auto_opening_label = get_text('auto_opening_label', 'Ouverture automatique :')
    auto_opening_desc = get_text('auto_opening_desc', 'Rapport HTML prioritaire si disponible, sinon rapport texte')
    direct_folder_access_label = get_text('direct_folder_access_label', 'Accès direct dossiers :')
    direct_folder_access_desc = get_text('direct_folder_access_desc', 'Boutons vers dossiers de rapports et sauvegardes')
    recommended_validation_label = get_text('recommended_validation_label', 'Validation recommandée :')
    recommended_validation_desc = get_text('recommended_validation_desc', 'Lancement du vérificateur de cohérence suggéré')

    # Cas d'usage et bonnes pratiques nettoyage
    practical_use_cases_cleanup_title = get_text('practical_use_cases_cleanup_title', 'Cas d\'usage et bonnes pratiques')
    new_translation_project_title = get_text('new_translation_project_title', 'Nouveau projet de traduction')
    new_translation_project_context = get_text('new_translation_project_context', 'Première traduction d\'un jeu récent')
    new_translation_project_usage = get_text('new_translation_project_usage', 'Nettoyage initial après génération TL pour partir sur des bases saines')
    game_update_title = get_text('game_update_title', 'Mise à jour de jeu')
    game_update_context = get_text('game_update_context', 'Le jeu a été mis à jour avec nouveaux dialogues')
    game_update_usage = get_text('game_update_usage', 'Nettoyage après re-génération pour supprimer les anciens textes')
    periodic_maintenance_title = get_text('periodic_maintenance_title', 'Maintenance périodique')
    periodic_maintenance_context = get_text('periodic_maintenance_context', 'Nettoyage de routine d\'un projet existant')
    periodic_maintenance_usage = get_text('periodic_maintenance_usage', 'Optimisation de l\'espace et suppression des accumulations')
    problem_resolution_title = get_text('problem_resolution_title', 'Résolution de problèmes')
    problem_resolution_context = get_text('problem_resolution_context', 'Dysfonctionnements ou erreurs dans le jeu')
    problem_resolution_usage = get_text('problem_resolution_usage', 'Nettoyage ciblé pour éliminer les traductions problématiques')

    # Conseils d'utilisation optimale nettoyage
    optimal_usage_tips_cleanup_title = get_text('optimal_usage_tips_cleanup_title', 'Conseils d\'utilisation optimale')
    recommended_workflow_cleanup_title = get_text('recommended_workflow_cleanup_title', 'Workflow recommandé :')
    unique_config_step = get_text('unique_config_step', 'Configuration unique :')
    unique_config_desc = get_text('unique_config_desc', 'Définissez vos exclusions une fois pour toutes')
    systematic_cleanup_step = get_text('systematic_cleanup_step', 'Nettoyage systématique :')
    systematic_cleanup_desc = get_text('systematic_cleanup_desc', 'Après chaque re-génération TL importante')
    post_cleanup_verification_step = get_text('post_cleanup_verification_step', 'Vérification post-nettoyage :')
    post_cleanup_verification_desc = get_text('post_cleanup_verification_desc', 'Utilisez le vérificateur de cohérence')
    game_test_step = get_text('game_test_step', 'Test du jeu :')
    game_test_desc = get_text('game_test_desc', 'Validation fonctionnelle après modification')

    # Précautions importantes nettoyage
    important_precautions_cleanup_title = get_text('important_precautions_cleanup_title', 'Précautions importantes :')
    attention_points_title = get_text('attention_points_title', 'Points d\'attention')
    auto_backup_label = get_text('auto_backup_label', 'Sauvegarde automatique :')
    auto_backup_desc = get_text('auto_backup_desc', 'Le système crée des backups, mais gardez vos propres sauvegardes importantes')
    mandatory_test_label = get_text('mandatory_test_label', 'Test obligatoire :')
    mandatory_test_desc = get_text('mandatory_test_desc', 'Vérifiez que le jeu fonctionne correctement après nettoyage')
    custom_exclusions_label = get_text('custom_exclusions_label', 'Exclusions personnalisées :')
    custom_exclusions_desc = get_text('custom_exclusions_desc', 'Protégez vos fichiers modifiés manuellement')
    no_partial_recovery_label = get_text('no_partial_recovery_label', 'Pas de récupération partielle :')
    no_partial_recovery_desc = get_text('no_partial_recovery_desc', 'Le nettoyage est global par fichier')

    # Astuces d'efficacité nettoyage
    efficiency_tips_title = get_text('efficiency_tips_title', 'Astuces d\'efficacité :')
    tool_combination_label = get_text('tool_combination_label', 'Combinaison d\'outils :')
    tool_combination_desc = get_text('tool_combination_desc', 'Utilisez avec l\'Éditeur Temps Réel pour voir les modifications en direct')
    planning_label = get_text('planning_label', 'Planification :')
    planning_desc = get_text('planning_desc', 'Nettoyage en fin de session de traduction')
    log_monitoring_label = get_text('log_monitoring_label', 'Surveillance logs :')
    log_monitoring_desc = get_text('log_monitoring_desc', 'Consultez les messages dans l\'interface pour comprendre les actions')
    permanent_report_label = get_text('permanent_report_label', 'Rapport permanent :')
    permanent_report_desc = get_text('permanent_report_desc', 'Gardez le rapport HTML ouvert pendant les vérifications')
    return f"""
        <div class="quick-nav-section" style="background: var(--card-bg); padding: 20px; margin-bottom: 30px; border-radius: 8px; border-left: 4px solid #4a90e2;">
            <h3>🧭 {quick_nav_title}</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; margin-top: 15px;">
                <a href="#verification-coherence" class="nav-card" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; transform: translateY(0); box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">🔍 {nav_coherence_checker}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_coherence_desc}</div>
                </a>
                <a href="#editeur-temps-reel" class="nav-card" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; transform: translateY(0); box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">⚡ {nav_realtime_editor}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_realtime_desc}</div>
                </a>
                <a href="#nettoyage-intelligent" class="nav-card" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; transform: translateY(0); box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">🧹 {nav_smart_cleanup}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_cleanup_desc}</div>
                </a>
            </div>
            <style>
                .nav-card:hover {{
                    transform: translateY(-3px) !important;
                    box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
                    border-color: #4a90e2 !important;
                    background: linear-gradient(135deg, var(--button-bg) 0%, rgba(74, 144, 226, 0.1) 100%) !important;
                }}
                
                .nav-card:active {{
                    transform: translateY(-1px) !important;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.12) !important;
                }}
            </style>
        </div>
        
        <div class="section" id="verification-coherence">
            <h2>🧪 {title}</h2>
            <p>{intro}</p>
            
            <h3>🎯 {overview_title}</h3>
            <ul>
                <li><strong>🔍 {coherence_checker_title}</strong> - {coherence_checker_desc}</li>
                <li><strong>⚡ {realtime_editor_title}</strong> - {realtime_editor_desc}</li>
                <li><strong>🧹 {smart_cleanup_title}</strong> - {smart_cleanup_desc}</li>
            </ul>        
            <h2>🔍 {coherence_detailed_title}</h2>
            {generator._get_image_html("03_interface_outils", "001", language, coherence_interface_alt, coherence_interface_caption)}
            
            <h3>🎯 {coherence_purpose_title}</h3>
            <p>{coherence_purpose_intro}</p>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #f59e0b; margin: 15px 0;">
                <h4>🚨 {why_essential_title}</h4>
                <p>{why_essential_desc}</p>
            </div>
            
            <h3>🖥️ {new_interface_title}</h3>
            <p>{new_interface_intro}</p>
            
            <div class="workflow-step" data-step="1">
                <h4>{centralized_config_step}</h4>
                <p>{centralized_config_desc}</p>
            </div>
            
            <div class="workflow-step" data-step="2">
                <h4>{customizable_options_step}</h4>
                <p>{customizable_options_desc}</p>
            </div>
            
            <div class="workflow-step" data-step="3">
                <h4>{unified_analysis_step}</h4>
                <p>{unified_analysis_desc}</p>
            </div>
            
            <h3>📂 {unified_project_config_title}</h3>
            {generator._get_image_html("03_interface_outils", "003", language, project_selector_alt, project_selector_caption)}
            
            <h4>{smart_selection_title}</h4>
            <p>{smart_selection_intro}</p>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <h5>🎯 {header_driven_title}</h5>
                    <p>{header_driven_desc}</p>
                    <p><strong>{advantage_label}</strong> {header_driven_advantage}</p>
                </div>
                
                <div class="feature-card">
                    <h5>🌐 {auto_language_scan_title}</h5>
                    <p>{auto_language_scan_desc}</p>
                    <p><strong>{intelligence_label}</strong> {auto_language_scan_intelligence}</p>
                </div>
                
                <div class="feature-card">
                    <h5>📋 {flexible_selection_title}</h5>
                    <p>{flexible_selection_desc}</p>
                    <p><strong>{granularity_label}</strong> {flexible_selection_granularity}</p>
                </div>
                
                <div class="feature-card">
                    <h5>🚫 {integrated_exclusions_title}</h5>
                    <p>{integrated_exclusions_desc}</p>
                    <p><strong>{efficiency_label}</strong> {integrated_exclusions_efficiency}</p>
                </div>
            </div>
            
            <h3>⚙️ {configurable_checks_title}</h3>
            {generator._get_image_html("03_interface_outils", "002", language, check_options_alt, check_options_caption)}

            <div class="feature-grid">
                <div class="feature-card">
                    <h5>🔤 {inconsistent_variables_title}</h5>
                    <p><strong>{detects_label}</strong> {inconsistent_variables_detects}</p>
                    <p><strong>{example_label}</strong> {inconsistent_variables_example}</p>
                    <p><strong>{impact_label}</strong> {inconsistent_variables_impact}</p>
                </div>
                
                <div class="feature-card">
                    <h5>🎨 {inconsistent_tags_title}</h5>
                    <p><strong>{detects_label}</strong> {inconsistent_tags_detects}</p>
                    <p><strong>{example_label}</strong> {inconsistent_tags_example}</p>
                    <p><strong>{impact_label}</strong> {inconsistent_tags_impact}</p>
                </div>
                
                <div class="feature-card">
                    <h5>💻 {special_codes_title}</h5>
                    <p><strong>{detects_label}</strong> {special_codes_detects}</p>
                    <p><strong>{example_label}</strong> {special_codes_example}</p>
                    <p><strong>{impact_label}</strong> {special_codes_impact}</p>
                </div>
                
                <div class="feature-card">
                    <h5>📝 {untranslated_lines_title}</h5>
                    <p><strong>{detects_label}</strong> {untranslated_lines_detects}</p>
                    <p><strong>{example_label}</strong> {untranslated_lines_example}</p>
                    <p><strong>{impact_label}</strong> {untranslated_lines_impact}</p>
                </div>
            </div>
            
            <h4>🆕 {new_checks_title}</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #8b5cf6;">
                    <h5>{inconsistent_parentheses_title}</h5>
                    <p><strong>{new_label}</strong> {inconsistent_parentheses_new}</p>
                    <p><strong>{usage_label}</strong> {inconsistent_parentheses_usage}</p>
                </div>
                
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #10b981;">
                    <h5>{french_quotes_title}</h5>
                    <p><strong>{new_label}</strong> {french_quotes_new}</p>
                    <p><strong>{localization_label}</strong> {french_quotes_localization}</p>
                </div>
            </div>
            
            <h3>🚫 {smart_exclusions_title}</h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #e74c3c;">
                    <h5>🚫 {files_to_exclude_title}</h5>
                    <p><strong>{configuration_label}</strong> {files_to_exclude_config}</p>
                    <p><strong>{functioning_label}</strong> {files_to_exclude_functioning}</p>
                    <p><strong>{synchronization_label}</strong> {files_to_exclude_sync}</p>
                </div>
                
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #f39c12;">
                    <h5>🔍 {smart_line_exclusions_title}</h5>
                    <p><strong>{auto_exclusions_label}</strong> {smart_line_exclusions_auto}</p>
                    <p><strong>{custom_label}</strong> {smart_line_exclusions_custom}</p>
                    <p><strong>{saving_label}</strong> {smart_line_exclusions_saving}</p>
                </div>
            </div>
            
            <h3>🚀 {launch_analysis_title}</h3>
            
            <h4>{centralized_control_title}</h4>
            <p>{centralized_control_intro}</p>
            
            <ul>
                <li><strong>{realtime_status_label}</strong> {realtime_status_desc}</li>
                <li><strong>{smart_validation_label}</strong> {smart_validation_desc}</li>
                <li><strong>{contextual_info_label}</strong> {contextual_info_desc}</li>
                <li><strong>{post_analysis_actions_label}</strong> {post_analysis_actions_desc}</li>
            </ul>
            
            <h4>{optimized_analysis_process_title}</h4>
            <ol>
                <li><strong>{preliminary_validation_step}</strong> {preliminary_validation_desc}</li>
                <li><strong>{auto_configuration_step}</strong> {auto_configuration_desc}</li>
                <li><strong>{threaded_analysis_step}</strong> {threaded_analysis_desc}</li>
                <li><strong>{report_generation_step}</strong> {report_generation_desc}</li>
                <li><strong>{conditional_opening_step}</strong> {conditional_opening_desc}</li>
            </ol>
            
            <h3>📊 {modern_html_report_title}</h3>
            {generator._get_image_html("03_interface_outils", "004", language, html_report_alt, html_report_caption)}
            
            <h4>{new_report_features_title}</h4>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <h5>🎯 {enriched_metadata_title}</h5>
                    <p>{enriched_metadata_desc}</p>
                    <p><strong>{traceability_label}</strong> {enriched_metadata_traceability}</p>
                </div>
                
                <div class="feature-card">
                    <h5>📈 {advanced_statistics_title}</h5>
                    <p>{advanced_statistics_desc}</p>
                    <p><strong>{overview_label}</strong> {advanced_statistics_overview}</p>
                </div>
                
                <div class="feature-card">
                    <h5>🔗 {smart_navigation_title}</h5>
                    <p>{smart_navigation_desc}</p>
                    <p><strong>{efficiency_label}</strong> {smart_navigation_efficiency}</p>
                </div>
                
                <div class="feature-card">
                    <h5>🎨 {adaptive_interface_title}</h5>
                    <p>{adaptive_interface_desc}</p>
                    <p><strong>{comfort_label}</strong> {adaptive_interface_comfort}</p>
                </div>
            </div>
            
            <h3>🎯 {use_cases_new_architecture_title}</h3>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <h5>📄 {integrated_daily_workflow_title}</h5>
                    <p><strong>{context_label}</strong> {integrated_daily_workflow_context}</p>
                    <p><strong>{method_label}</strong> {integrated_daily_workflow_method}</p>
                    <p><strong>{advantage_label}</strong> {integrated_daily_workflow_advantage}</p>
                </div>
                
                <div class="feature-card">
                    <h5>🎮 {complete_project_verification_title}</h5>
                    <p><strong>{context_label}</strong> {complete_project_verification_context}</p>
                    <p><strong>{method_label}</strong> {complete_project_verification_method}</p>
                    <p><strong>{result_label}</strong> {complete_project_verification_result}</p>
                </div>
                
                <div class="feature-card">
                    <h5>🚨 {targeted_debugging_title}</h5>
                    <p><strong>{context_label}</strong> {targeted_debugging_context}</p>
                    <p><strong>{method_label}</strong> {targeted_debugging_method}</p>
                    <p><strong>{efficiency_label}</strong> {targeted_debugging_efficiency}</p>
                </div>
                
                <div class="feature-card">
                    <h5>⚡ {automated_verification_title}</h5>
                    <p><strong>{context_label}</strong> {automated_verification_context}</p>
                    <p><strong>{method_label}</strong> {automated_verification_method}</p>
                    <p><strong>{evolution_label}</strong> {automated_verification_evolution}</p>
                </div>
            </div>
            
            <h3>💡 {optimal_usage_tips_title}</h3>
            
            <h4>{recommended_config_title}</h4>
            <ul>
                <li><strong>{first_use_label}</strong> {first_use_desc}</li>
                <li><strong>{file_exclusions_label}</strong> {file_exclusions_desc}</li>
                <li><strong>{line_exclusions_label}</strong> {line_exclusions_desc}</li>
                <li><strong>{save_all_label}</strong> {save_all_desc}</li>
            </ul>
            
            <h4>{optimal_workflow_title}</h4>
            <ol>
                <li><strong>{unique_project_step}</strong> {unique_project_desc}</li>
                <li><strong>{systematic_verification_step}</strong> {systematic_verification_desc}</li>
                <li><strong>{complete_analysis_step}</strong> {complete_analysis_desc}</li>
                <li><strong>{permanent_report_step}</strong> {permanent_report_desc}</li>
            </ol>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #4a90e2; margin: 15px 0;">
                <h4>📄 {integration_other_tools_title}</h4>
                <p>{integration_other_tools_intro}</p>
                <ul>
                    <li><strong>{realtime_editor_integration_label}</strong> {realtime_editor_integration_desc}</li>
                    <li><strong>{smart_cleanup_integration_label}</strong> {smart_cleanup_integration_desc}</li>
                    <li><strong>{backup_manager_integration_label}</strong> {backup_manager_integration_desc}</li>
                </ul>
            </div>
        </div>
        <div class="section" id="editeur-temps-reel">
            <h2>⚡ {realtime_editor_detailed_title}</h2>
            {generator._get_image_html("03_interface_outils", "009", language, realtime_editor_interface_alt, realtime_editor_interface_caption)}
            
            <h3>🎯 {realtime_editor_purpose_title}</h3>
            <p>{realtime_editor_purpose_intro}</p>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #10b981; margin: 15px 0;">
                <h4>🚀 {workflow_revolution_title}</h4>
                <p>{workflow_revolution_desc}</p>
            </div>
            
            <h3>🔧 {installation_monitoring_title}</h3>
            {generator._get_image_html("03_interface_outils", "015", language, installation_config_alt, installation_config_caption)}
            
            <h4>{config_3_steps_title}</h4>
            
            <div class="workflow-step" data-step="1">
                <h4>{language_selection_step}</h4>
                <p><strong>{scan_languages_label}</strong> {language_selection_scan}</p>
                <p><strong>{validation_label}</strong> {language_selection_validation}</p>
            </div>
            
            <div class="workflow-step" data-step="2">
                <h4>{module_installation_step}</h4>
                <p><strong>{renpy_module_label}</strong> {module_installation_module}</p>
                <p><strong>{smart_update_label}</strong> {module_installation_update}</p>
            </div>
            
            <div class="workflow-step" data-step="3">
                <h4>{monitoring_start_step}</h4>
                <p><strong>{translation_cache_label}</strong> {monitoring_start_cache}</p>
                <p><strong>{active_monitoring_label}</strong> {monitoring_start_monitoring}</p>
            </div>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #4a90e2; margin: 15px 0;">
                <h4>💡 {unique_installation_title}</h4>
                <p>{unique_installation_desc}</p>
            </div>
            
            <h3>⌨️ {f8_shortcut_title}</h3>
            {generator._get_image_html("03_interface_outils", "016", language, f8_guide_alt, f8_guide_caption)}
            
            <h4>{f8_functioning_title}</h4>
            <ul>
                <li><strong>{smart_detection_label}</strong> {f8_functioning_detection}</li>
                <li><strong>{auto_exit_label}</strong> {f8_functioning_exit}</li>
                <li><strong>{renextract_focus_label}</strong> {f8_functioning_focus}</li>
                <li><strong>{f11_return_label}</strong> {f8_functioning_return}</li>
            </ul>
            
            <h4>{technical_architecture_title}</h4>
            <div class="feature-grid">
                <div class="feature-card">
                    <h5>🌐 {integrated_local_server_title}</h5>
                    <p>{integrated_local_server_desc}</p>
                    <p><strong>{security_label}</strong> {integrated_local_server_security}</p>
                </div>
                
                <div class="feature-card">
                    <h5>📱 {multi_version_compatibility_title}</h5>
                    <p>{multi_version_compatibility_desc}</p>
                    <p><strong>{robustness_label}</strong> {multi_version_compatibility_robustness}</p>
                </div>
            </div>
            
            <h3>💬 {adaptive_editing_interface_title}</h3>
            
            <h4>{supported_dialogue_types_title}</h4>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <h5>📝 {simple_dialogues_title}</h5>
                    {generator._get_image_html("03_interface_outils", "010", language, simple_dialogues_alt, simple_dialogues_caption)}
                    <p><strong>{usage_label}</strong> {simple_dialogues_usage}</p>
                    <p><strong>{interface_label}</strong> {simple_dialogues_interface}</p>
                </div>
                
                <div class="feature-card">
                    <h5>🎭 {undefined_speaker_title}</h5>
                    {generator._get_image_html("03_interface_outils", "012", language, undefined_speaker_alt, undefined_speaker_caption)}
                    <p><strong>{usage_label}</strong> {undefined_speaker_usage}</p>
                    <p><strong>{advantage_label}</strong> {undefined_speaker_advantage}</p>
                </div>
                
                <div class="feature-card">
                    <h5>🔀 {split_dialogues_title}</h5>
                    {generator._get_image_html("03_interface_outils", "013", language, split_dialogues_alt, split_dialogues_caption)}
                    <p><strong>{usage_label}</strong> {split_dialogues_usage}</p>
                    <p><strong>{interface_label}</strong> {split_dialogues_interface}</p>
                </div>
                
                <div class="feature-card">
                    <h5>🎯 {multiple_choices_title}</h5>
                    {generator._get_image_html("03_interface_outils", "011", language, multiple_choices_alt, multiple_choices_caption)}
                    <p><strong>{usage_label}</strong> {multiple_choices_usage}</p>
                    <p><strong>{organization_label}</strong> {multiple_choices_organization}</p>
                </div>
                
                <div class="feature-card">
                    <h5>🔢 {multiple_dialogues_title}</h5>
                    {generator._get_image_html("03_interface_outils", "014", language, multiple_dialogues_alt, multiple_dialogues_caption)}
                    <p><strong>{usage_label}</strong> {multiple_dialogues_usage}</p>
                    <p><strong>{efficiency_label}</strong> {multiple_dialogues_efficiency}</p>
                </div>
            </div>
            
            <h3>🛠️ {integrated_utility_buttons_title}</h3>
            {generator._get_image_html("03_interface_outils", "017", language, utility_buttons_alt, utility_buttons_caption)}
            
            <h4>{translation_assistance_tools_title}</h4>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #4a90e2;">
                    <h5>📋 {copy_button_title}</h5>
                    <p><strong>{function_label}</strong> {copy_button_function}</p>
                    <p><strong>{usage_label}</strong> {copy_button_usage}</p>
                </div>
                
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #10b981;">
                    <h5>🔄 {deepl_button_title}</h5>
                    <p><strong>{function_label}</strong> {deepl_button_function}</p>
                    <p><strong>{advantage_label}</strong> {deepl_button_advantage}</p>
                </div>
                
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #f59e0b;">
                    <h5>🌐 {google_button_title}</h5>
                    <p><strong>{function_label}</strong> {google_button_function}</p>
                    <p><strong>{complementary_label}</strong> {google_button_complementary}</p>
                </div>
                
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #8b5cf6;">
                    <h5>📝 {paste_button_title}</h5>
                    <p><strong>{function_label}</strong> {paste_button_function}</p>
                    <p><strong>{workflow_label}</strong> {paste_button_workflow}</p>
                </div>

                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #e74c3c;">
                    <h5>🪟 {detach_button_title}</h5>
                    <p><strong>{function_label}</strong> {detach_button_function}</p>
                    <p><strong>{advantage_label}</strong> {detach_button_advantage}</p>
                </div>
                
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #9333ea;">
                    <h5>🔤 {font_size_selector_title}</h5>
                    <p><strong>{function_label}</strong> {font_size_selector_function}</p>
                    <p><strong>{scope_label}</strong> {font_size_selector_scope}</p>
                </div>            
            </div>
            
            <h4>{advanced_mode_buttons_title}</h4>
            <ul>
                <li><strong>{split_merge_label}</strong> {split_merge_desc}</li>
                <li><strong>{detach_attach_label}</strong> {detach_attach_desc}</li>
                <li><strong>{open_label}</strong> {open_desc}</li>
            </ul>
            
            <h3>💾 {pending_modifications_system_title}</h3>
            {generator._get_image_html("03_interface_outils", "018", language, crash_recovery_alt, crash_recovery_caption)}
            
            <h4>{anti_loss_security_title}</h4>
            <div class="feature-grid">
                <div class="feature-card">
                    <h5>📊 {persistent_json_cache_title}</h5>
                    <p>{persistent_json_cache_desc}</p>
                    <p><strong>{protection_label}</strong> {persistent_json_cache_protection}</p>
                </div>
                
                <div class="feature-card">
                    <h5>🔄 {smart_recovery_title}</h5>
                    <p>{smart_recovery_desc}</p>
                    <p><strong>{detail_label}</strong> {smart_recovery_detail}</p>
                </div>
                
                <div class="feature-card">
                    <h5>💾 {grouped_save_title}</h5>
                    <p>{grouped_save_desc}</p>
                    <p><strong>{efficiency_label}</strong> {grouped_save_efficiency}</p>
                </div>
            </div>
            
            <h4>{supported_modification_types_title}</h4>
            <ul>
                <li><strong>{simple_mod_label}</strong> {simple_mod_desc}</li>
                <li><strong>{split_mod_label}</strong> {split_mod_desc}</li>
                <li><strong>{speaker_dialogue_mod_label}</strong> {speaker_dialogue_mod_desc}</li>
                <li><strong>{merge_mod_label}</strong> {merge_mod_desc}</li>
            </ul>
            
            <h3>🎯 {practical_use_cases_title}</h3>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <h5>🔧 {length_adjustments_title}</h5>
                    <p><strong>{problem_label}</strong> {length_adjustments_problem}</p>
                    <p><strong>{solution_label}</strong> {length_adjustments_solution}</p>
                </div>
                
                <div class="feature-card">
                    <h5>✏️ {contextual_corrections_title}</h5>
                    <p><strong>{problem_label}</strong> {contextual_corrections_problem}</p>
                    <p><strong>{solution_label}</strong> {contextual_corrections_solution}</p>
                </div>
                
                <div class="feature-card">
                    <h5>🎭 {style_adaptation_title}</h5>
                    <p><strong>{problem_label}</strong> {style_adaptation_problem}</p>
                    <p><strong>{solution_label}</strong> {style_adaptation_solution}</p>
                </div>
                
                <div class="feature-card">
                    <h5>🎯 {collaborative_review_title}</h5>
                    <p><strong>{context_label}</strong> {collaborative_review_context}</p>
                    <p><strong>{advantage_label}</strong> {collaborative_review_advantage}</p>
                </div>
            </div>
            
            <h3>💡 {optimal_usage_tips_realtime_title}</h3>
            
            <h4>{recommended_workflow_realtime_title}</h4>
            <ol>
                <li><strong>{unique_installation_step}</strong> {unique_installation_step_desc}</li>
                <li><strong>{game_session_step}</strong> {game_session_step_desc}</li>
                <li><strong>{contextual_translation_step}</strong> {contextual_translation_step_desc}</li>
                <li><strong>{immediate_test_step}</strong> {immediate_test_step_desc}</li>
                <li><strong>{grouped_save_step}</strong> {grouped_save_step_desc}</li>
            </ol>
            
            <h4>{practical_tips_title}</h4>
            <ul>
                <li><strong>{detached_mode_label}</strong> {detached_mode_desc}</li>
                <li><strong>{translation_cache_tip_label}</strong> {translation_cache_tip_desc}</li>
                <li><strong>{external_buttons_label}</strong> {external_buttons_desc}</li>
                <li><strong>{ctrl_s_shortcut_label}</strong> {ctrl_s_shortcut_desc}</li>
            </ul>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #f59e0b; margin: 15px 0;">
                <h4>⚠️ {important_limitations_realtime_title}</h4>
                <ul>
                    <li><strong>{one_project_at_time_label}</strong> {one_project_at_time_desc}</li>
                    <li><strong>{recommended_stop_label}</strong> {recommended_stop_desc}</li>
                    <li><strong>{performance_label}</strong> {performance_desc}</li>
                    <li><strong>{compatibility_label}</strong> {compatibility_desc}</li>
                </ul>
            </div>
        </div>
        <div class="section" id="nettoyage-intelligent">
            <h2>🧹 {smart_cleanup_detailed_title}</h2>
            {generator._get_image_html("03_interface_outils", "005", language, smart_cleanup_interface_alt, smart_cleanup_interface_caption)}
            
            <h3>🎯 {smart_cleanup_purpose_title}</h3>
            <p>{smart_cleanup_purpose_intro}</p>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <h5>🎯 {lint_based_cleanup_title}</h5>
                    <p>{lint_based_cleanup_desc}</p>
                    <p><strong>{advantage_label}</strong> {lint_based_cleanup_advantage}</p>
                </div>
                
                <div class="feature-card">
                    <h5>🔍 {correspondence_cleanup_title}</h5>
                    <p>{correspondence_cleanup_desc}</p>
                    <p><strong>{complement_label}</strong> {correspondence_cleanup_complement}</p>
                </div>
            </div>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #f39c12; margin: 15px 0;">
                <h4>💡 {why_necessary_cleanup_title}</h4>
                <p>{why_necessary_cleanup_desc}</p>
            </div>
            
            <h3>🖥️ {cleanup_workflow_title}</h3>
            
            <div class="workflow-step" data-step="1">
                <h4>{smart_configuration_step}</h4>
                <p>{smart_configuration_desc}</p>
            </div>
            
            <div class="workflow-step" data-step="2">
                <h4>{auto_lint_generation_step}</h4>
                <p>{auto_lint_generation_desc}</p>
            </div>
            
            <div class="workflow-step" data-step="3">
                <h4>{unified_cleanup_step}</h4>
                <p>{unified_cleanup_desc}</p>
            </div>
            
            <h3>🌐 {language_selection_optimized_title}</h3>
            
            <h4>{column_organization_title_3}</h4>
            <p>{column_organization_intro_3}</p>
            
            <ul>
                <li><strong>{contextual_icons_label}</strong> {contextual_icons_desc}</li>
                <li><strong>{numbered_badges_label}</strong> {numbered_badges_desc}</li>
                <li><strong>{formatted_title_label}</strong> {formatted_title_desc}</li>
                <li><strong>{default_selection_label}</strong> {default_selection_desc}</li>
            </ul>
            
            <h4>{quick_controls_title}</h4>
            <div class="feature-grid">
                <div class="feature-card">
                    <h5>📡 {scan_languages_title}</h5>
                    <p>{scan_languages_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h5>✅ {select_all_title}</h5>
                    <p>{select_all_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h5>❌ {deselect_all_title}</h5>
                    <p>{deselect_all_desc}</p>
                </div>
            </div>
            
            <h3>🚫 {advanced_exclusions_system_title}</h3>
            {generator._get_image_html("03_interface_outils", "006", language, custom_exclusions_help_alt, custom_exclusions_help_caption)}
            
            <h4>{configurable_exclusions_title}</h4>
            <p>{configurable_exclusions_intro}</p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #4a90e2;">
                    <h5>🔧 {flexible_configuration_title}</h5>
                    <ul>
                        <li>{flexible_configuration_1}</li>
                        <li>{flexible_configuration_2}</li>
                        <li>{flexible_configuration_3}</li>
                    </ul>
                </div>
                
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #10b981;">
                    <h5>🛡️ {auto_protection_title}</h5>
                    <ul>
                        <li>{auto_protection_1}</li>
                        <li>{auto_protection_2}</li>
                        <li>{auto_protection_3}</li>
                    </ul>
                </div>
            </div>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #f59e0b; margin: 15px 0;">
                <h4>⚙️ {exclusion_logic_title}</h4>
                <ul>
                    <li><strong>{exact_match_label}</strong> {exact_match_desc}</li>
                    <li><strong>{case_insensitive_label}</strong> {case_insensitive_desc}</li>
                    <li><strong>{extension_required_label}</strong> {extension_required_desc}</li>
                    <li><strong>{auto_save_label}</strong> {auto_save_desc}</li>
                </ul>
            </div>
            
            <h3>⚡ {automated_cleanup_process_title}</h3>
            {generator._get_image_html("03_interface_outils", "007", language, cleanup_progress_alt, cleanup_progress_caption)}
            
            <h4>{integrated_sdk_title}</h4>
            
            <ol>
                <li><strong>{sdk_validation_step}</strong> {sdk_validation_desc}</li>
                <li><strong>{preliminary_cleanup_step}</strong> {preliminary_cleanup_desc}</li>
                <li><strong>{lint_generation_step}</strong> {lint_generation_desc}</li>
                <li><strong>{unified_analysis_step_cleanup}</strong> {unified_analysis_desc_cleanup}</li>
                <li><strong>{backup_deletion_step}</strong> {backup_deletion_desc}</li>
            </ol>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <h5>🔄 {sdk_failure_management_title}</h5>
                    <p><strong>{smart_fallback_label}</strong> {sdk_failure_management_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h5>💾 {single_backup_title}</h5>
                    <p><strong>{optimization_label}</strong> {single_backup_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h5>⏱️ {timeout_management_title}</h5>
                    <p><strong>{robustness_label}</strong> {timeout_management_desc}</p>
                </div>
            </div>
            
            <h3>📊 {detailed_results_reports_title}</h3>
            {generator._get_image_html("03_interface_outils", "008", language, cleanup_results_alt, cleanup_results_caption)}
            
            <h4>{interactive_results_popup_title}</h4>
            <p>{interactive_results_popup_intro}</p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #10b981;">
                    <h5>📈 {cleanup_metrics_title}</h5>
                    <ul>
                        <li>{cleanup_metrics_1}</li>
                        <li>{cleanup_metrics_2}</li>
                        <li>{cleanup_metrics_3}</li>
                        <li>{cleanup_metrics_4}</li>
                    </ul>
                </div>
                
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #4a90e2;">
                    <h5>📄 {interactive_html_report_title}</h5>
                    <ul>
                        <li>{interactive_html_report_1}</li>
                        <li>{interactive_html_report_2}</li>
                        <li>{interactive_html_report_3}</li>
                        <li>{interactive_html_report_4}</li>
                    </ul>
                </div>
            </div>
            
            <h4>{post_cleanup_actions_title}</h4>
            <ul>
                <li><strong>{auto_opening_label}</strong> {auto_opening_desc}</li>
                <li><strong>{direct_folder_access_label}</strong> {direct_folder_access_desc}</li>
                <li><strong>{recommended_validation_label}</strong> {recommended_validation_desc}</li>
            </ul>
            
            <h3>🎯 {practical_use_cases_cleanup_title}</h3>
            <div class="feature-grid">
                <div class="feature-card">
                    <h4>🆕 {new_translation_project_title}</h4>
                    <p><strong>{context_label}</strong> {new_translation_project_context}</p>
                    <p><strong>{usage_label}</strong> {new_translation_project_usage}</p>
                </div>
                
                <div class="feature-card">
                    <h4>🔄 {game_update_title}</h4>
                    <p><strong>{context_label}</strong> {game_update_context}</p>
                    <p><strong>{usage_label}</strong> {game_update_usage}</p>
                </div>
                
                <div class="feature-card">
                    <h4>🧹 {periodic_maintenance_title}</h4>
                    <p><strong>{context_label}</strong> {periodic_maintenance_context}</p>
                    <p><strong>{usage_label}</strong> {periodic_maintenance_usage}</p>
                </div>
                
                <div class="feature-card">
                    <h4>🚨 {problem_resolution_title}</h4>
                    <p><strong>{context_label}</strong> {problem_resolution_context}</p>
                    <p><strong>{usage_label}</strong> {problem_resolution_usage}</p>
                </div>
            </div>
            
            <h3>💡 {optimal_usage_tips_cleanup_title}</h3>
            
            <h4>{recommended_workflow_cleanup_title}</h4>
            <ol>
                <li><strong>{unique_config_step}</strong> {unique_config_desc}</li>
                <li><strong>{systematic_cleanup_step}</strong> {systematic_cleanup_desc}</li>
                <li><strong>{post_cleanup_verification_step}</strong> {post_cleanup_verification_desc}</li>
                <li><strong>{game_test_step}</strong> {game_test_desc}</li>
            </ol>
            
            <h4>{important_precautions_cleanup_title}</h4>
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #ef4444; margin: 15px 0;">
                <h4>⚠️ {attention_points_title}</h4>
                <ul>
                    <li><strong>{auto_backup_label}</strong> {auto_backup_desc}</li>
                    <li><strong>{mandatory_test_label}</strong> {mandatory_test_desc}</li>
                    <li><strong>{custom_exclusions_label}</strong> {custom_exclusions_desc}</li>
                    <li><strong>{no_partial_recovery_label}</strong> {no_partial_recovery_desc}</li>
                </ul>
            </div>
            
            <h4>{efficiency_tips_title}</h4>
            <ul>
                <li><strong>{tool_combination_label}</strong> {tool_combination_desc}</li>
                <li><strong>{planning_label}</strong> {planning_desc}</li>
                <li><strong>{log_monitoring_label}</strong> {log_monitoring_desc}</li>
                <li><strong>{permanent_report_label}</strong> {permanent_report_desc}</li>
            </ul>
        </div>
    """