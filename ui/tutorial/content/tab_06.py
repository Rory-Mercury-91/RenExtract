# ui/tutorial/content/tab_06.py
"""
Module de contenu pour l'onglet 6 : Gestionnaire de Sauvegardes
"""

import html

def generate_content(generator, language, translations):
    """
    Génère le contenu pour l'onglet 6 : Gestionnaire de Sauvegardes
    
    Args:
        generator: Instance du générateur avec méthodes utilitaires
        language: Code langue (fr, en, de)
        translations: Dictionnaire des traductions
    
    Returns:
        str: HTML généré pour l'onglet gestionnaire de sauvegardes
    """
    # Vérification des traductions
    if not isinstance(translations, dict) or 'tabs' not in translations or 'common' not in translations:
        return "<div>Erreur : Traductions manquantes ou mal formées</div>"
    
    # Récupération des traductions pour cette section
    section_t = translations.get('tabs', {}).get('backup', {})
    common_t = translations.get('common', {})
    
    def get_text(key, fallback=""):
        """Récupère une traduction avec sanitisation HTML"""
        value = section_t.get(key) or common_t.get(key) or fallback
        return html.escape(value)
    
    # --- Navigation rapide ---
    quick_nav_title = get_text('quick_nav_title', 'Navigation rapide')
    nav_statistics = get_text('nav_statistics', 'Statistiques')
    nav_statistics_desc = get_text('nav_statistics_desc', 'Métriques en temps réel et répartition')
    nav_restoration = get_text('nav_restoration', 'Filtrage & Restauration')
    nav_restoration_desc = get_text('nav_restoration_desc', 'Interface de liste et actions contextuelles')
    nav_cleanup = get_text('nav_cleanup', 'Nettoyage automatique')
    nav_cleanup_desc = get_text('nav_cleanup_desc', 'Critères intelligents et rotation')
    
    # --- Section Gestionnaire de Sauvegardes - Guide Complet ---
    title = get_text('title', 'Gestionnaire de Sauvegardes - Guide Complet')
    description = get_text('description', 'Le Gestionnaire de Sauvegardes centralise la gestion des 4 types de sauvegardes automatiques avec vue unifiée, filtres et restauration en un clic.')
    backup_main_interface_alt = get_text('backup_main_interface_alt', 'Interface principale gestionnaire')
    backup_main_interface_caption = get_text('backup_main_interface_caption', 'Vue d\'ensemble avec filtres et liste des sauvegardes')
    hierarchy_title = get_text('hierarchy_title', 'Architecture hiérarchique')
    hierarchy_desc = get_text('hierarchy_desc', 'Structure organisée : Nom_du_jeu/nom_fichier/type_backup/fichiers')
    advantage_label = get_text('advantage_label', 'Avantage :')
    hierarchy_advantage = get_text('hierarchy_advantage', 'Navigation intuitive et gestion automatique de l\'espace disque')
    purpose_title = get_text('purpose_title', 'À quoi ça sert')
    purpose_intro = get_text('purpose_intro', 'Le gestionnaire unifie l\'accès à tous les types de sauvegardes avec des fonctionnalités avancées :')
    centralized_view_title = get_text('centralized_view_title', 'Vue centralisée')
    centralized_view_desc = get_text('centralized_view_desc', 'Toutes les sauvegardes dans une interface unique')
    smart_filtering_title = get_text('smart_filtering_title', 'Filtrage intelligent')
    smart_filtering_desc = get_text('smart_filtering_desc', 'Par jeu, type, date avec recherche avancée')
    one_click_restore_title = get_text('one_click_restore_title', 'Restauration en 1 clic')
    one_click_restore_desc = get_text('one_click_restore_desc', 'Processus sécurisé avec confirmation')
    auto_cleanup_title = get_text('auto_cleanup_title', 'Nettoyage automatique')
    auto_cleanup_desc = get_text('auto_cleanup_desc', 'Rotation intelligente selon le type de sauvegarde')
    
    # --- Section Statistiques intelligentes ---
    statistics_title = get_text('statistics_title', 'Section Statistiques intelligentes')
    backup_statistics_alt = get_text('backup_statistics_alt', 'Section statistiques')
    backup_statistics_caption = get_text('backup_statistics_caption', 'Métriques en temps réel et répartition par type')
    realtime_metrics_title = get_text('realtime_metrics_title', 'Métriques en temps réel')
    realtime_metrics_intro = get_text('realtime_metrics_intro', 'Informations mises à jour automatiquement à chaque action :')
    general_overview_title = get_text('general_overview_title', 'Vue d\'ensemble générale')
    total_backups_label = get_text('total_backups_label', 'Sauvegardes totales :')
    total_backups_desc = get_text('total_backups_desc', 'Nombre total avec mise à jour automatique')
    cumulative_size_label = get_text('cumulative_size_label', 'Taille cumulée :')
    cumulative_size_desc = get_text('cumulative_size_desc', 'Espace disque utilisé en MB/GB')
    game_distribution_title = get_text('game_distribution_title', 'Répartition par jeu')
    games_concerned_label = get_text('games_concerned_label', 'Jeux concernés :')
    games_concerned_desc = get_text('games_concerned_desc', 'Nombre de projets avec sauvegardes')
    distinct_files_label = get_text('distinct_files_label', 'Fichiers distincts :')
    distinct_files_desc = get_text('distinct_files_desc', 'Granularité par fichier traduit')
    type_breakdown_title = get_text('type_breakdown_title', 'Répartition par type')
    security_count_label = get_text('security_count_label', 'Sécurité :')
    security_count_desc = get_text('security_count_desc', 'Nombre de sauvegardes avant reconstruction')
    cleanup_count_label = get_text('cleanup_count_label', 'Nettoyage :')
    cleanup_count_desc = get_text('cleanup_count_desc', 'Sauvegardes avant nettoyage TL')
    rpa_count_label = get_text('rpa_count_label', 'RPA :')
    rpa_count_desc = get_text('rpa_count_desc', 'Backups pré-compilation')
    realtime_count_label = get_text('realtime_count_label', 'Temps réel :')
    realtime_count_desc = get_text('realtime_count_desc', 'Modifications éditeur direct')
    temporal_analysis_title = get_text('temporal_analysis_title', 'Analyse temporelle')
    newest_backup_label = get_text('newest_backup_label', 'Plus récente :')
    newest_backup_desc = get_text('newest_backup_desc', 'Date de la dernière sauvegarde')
    oldest_backup_label = get_text('oldest_backup_label', 'Plus ancienne :')
    oldest_backup_desc = get_text('oldest_backup_desc', 'Date de la première sauvegarde')
    
    # --- Section Système de filtrage avancé ---
    filtering_title = get_text('filtering_title', 'Système de filtrage avancé')
    backup_filters_alt = get_text('backup_filters_alt', 'Système de filtres')
    backup_filters_caption = get_text('backup_filters_caption', 'Double filtrage par jeu et type avec options avancées')
    double_filtering_title = get_text('double_filtering_title', 'Double filtrage intelligent')
    double_filtering_intro = get_text('double_filtering_intro', 'Système de filtres combinés pour un accès précis aux sauvegardes :')
    game_filter_title = get_text('game_filter_title', 'Filtre par jeu')
    game_filter_desc = get_text('game_filter_desc', 'Liste déroulante avec tous les jeux ayant des sauvegardes')
    type_filter_title = get_text('type_filter_title', 'Filtre par type')
    type_filter_desc = get_text('type_filter_desc', 'Sécurité, Nettoyage, RPA, Temps réel')
    search_bar_title = get_text('search_bar_title', 'Barre de recherche')
    search_bar_desc = get_text('search_bar_desc', 'Recherche par nom de fichier ou date')
    advanced_filters_title = get_text('advanced_filters_title', 'Filtres avancés')
    advanced_filters_desc = get_text('advanced_filters_desc', 'Combinaison jeu + type + date pour précision maximale')
    list_interface_title = get_text('list_interface_title', 'Interface de liste')
    backup_list_alt = get_text('backup_list_alt', 'Liste des sauvegardes')
    backup_list_caption = get_text('backup_list_caption', 'Vue détaillée avec métadonnées et actions')
    list_interface_intro = get_text('list_interface_intro', 'Liste dynamique des sauvegardes avec colonnes riches :')
    game_column_label = get_text('game_column_label', 'Jeu :')
    game_column_desc = get_text('game_column_desc', 'Nom du projet avec icône')
    file_column_label = get_text('file_column_label', 'Fichier :')
    file_column_desc = get_text('file_column_desc', 'Nom du fichier .rpy concerné')
    type_column_label = get_text('type_column_label', 'Type :')
    type_column_desc = get_text('type_column_desc', 'Catégorie de sauvegarde avec code couleur')
    date_column_label = get_text('date_column_label', 'Date :')
    date_column_desc = get_text('date_column_desc', 'Format humain lisible')
    size_column_label = get_text('size_column_label', 'Taille :')
    size_column_desc = get_text('size_column_desc', 'Format KB/MB')
    path_column_label = get_text('path_column_label', 'Chemin :')
    path_column_desc = get_text('path_column_desc', 'Emplacement complet avec icône de copie')
    actions_column_label = get_text('actions_column_label', 'Actions :')
    actions_column_desc = get_text('actions_column_desc', 'Boutons contextuels (Restaurer, Supprimer, Détails)')
    sorting_options_title = get_text('sorting_options_title', 'Options de tri')
    sorting_options_desc = get_text('sorting_options_desc', 'Par date (défaut descendant), taille, nom avec indicateurs visuels')
    pagination_title = get_text('pagination_title', 'Pagination intelligente')
    pagination_desc = get_text('pagination_desc', 'Pour les listes volumineuses avec chargement lazy')
    actions_menu_title = get_text('actions_menu_title', 'Menu contextuel des actions')
    backup_actions_alt = get_text('backup_actions_alt', 'Actions contextuelles')
    backup_actions_caption = get_text('backup_actions_caption', 'Menu déroulant avec options sécurisées')
    restore_action_label = get_text('restore_action_label', 'Restaurer :')
    restore_action_desc = get_text('restore_action_desc', 'Remplacement automatique au chemin original')
    restore_to_action_label = get_text('restore_to_action_label', 'Restaurer vers... :')
    restore_to_action_desc = get_text('restore_to_action_desc', 'Choix manuel du répertoire de destination')
    delete_action_label = get_text('delete_action_label', 'Supprimer :')
    delete_action_desc = get_text('delete_action_desc', 'Avec confirmation et mise à jour des stats')
    details_action_label = get_text('details_action_label', 'Détails :')
    details_action_desc = get_text('details_action_desc', 'Popup avec métadonnées complètes')
    restoration_process_title = get_text('restoration_process_title', 'Processus de restauration')
    restoration_dialog_alt = get_text('restoration_dialog_alt', 'Dialogue de restauration')
    restoration_dialog_caption = get_text('restoration_dialog_caption', 'Processus sécurisé avec confirmation et résumé')
    secure_workflow_title = get_text('secure_workflow_title', 'Workflow de restauration sécurisé')
    selection_step_label = get_text('selection_step_label', 'Sélection :')
    selection_step_desc = get_text('selection_step_desc', 'Choix de la sauvegarde dans la liste')
    confirmation_step_label = get_text('confirmation_step_label', 'Confirmation :')
    confirmation_step_desc = get_text('confirmation_step_desc', 'Dialogue avec résumé complet (fichier, jeu, type, date)')
    path_verification_step_label = get_text('path_verification_step_label', 'Vérification chemin :')
    path_verification_step_desc = get_text('path_verification_step_desc', 'Validation de l\'existence du répertoire cible')
    restoration_step_label = get_text('restoration_step_label', 'Restauration :')
    restoration_step_desc = get_text('restoration_step_desc', 'Copie avec préservation des métadonnées')
    final_confirmation_step_label = get_text('final_confirmation_step_label', 'Confirmation finale :')
    final_confirmation_step_desc = get_text('final_confirmation_step_desc', 'Popup de succès avec chemin restauré')
    special_cases_title = get_text('special_cases_title', 'Gestion des cas particuliers')
    missing_source_title = get_text('missing_source_title', 'Chemin source introuvable')
    auto_detection_label = get_text('auto_detection_label', 'Détection automatique :')
    auto_detection_fallback_desc = get_text('auto_detection_fallback_desc', 'Pour sauvegardes de nettoyage notamment')
    smart_fallback_label = get_text('smart_fallback_label', 'Fallback intelligent :')
    smart_fallback_desc = get_text('smart_fallback_desc', 'Reconstruction du chemin à la demande')
    manual_mode_label = get_text('manual_mode_label', 'Mode manuel :')
    manual_mode_desc = get_text('manual_mode_desc', 'Bascule automatique vers "Restaurer vers..." si échec')
    directory_creation_label = get_text('directory_creation_label', 'Création répertoires :')
    directory_creation_desc = get_text('directory_creation_desc', 'Dossiers créés automatiquement si nécessaire')
    
    # --- Section Nettoyage automatique avancé ---
    auto_cleanup_title = get_text('auto_cleanup_title', 'Nettoyage automatique avancé')
    cleanup_interface_alt = get_text('cleanup_interface_alt', 'Interface de nettoyage')
    cleanup_interface_caption = get_text('cleanup_interface_caption', 'Critères et processus de nettoyage automatique')
    smart_criteria_title = get_text('smart_criteria_title', 'Critères de nettoyage intelligents')
    smart_criteria_intro = get_text('smart_criteria_intro', 'Chaque type de sauvegarde a sa propre stratégie de rétention :')
    security_backups_title = get_text('security_backups_title', 'Sauvegardes Sécurité')
    security_retention_label = get_text('security_retention_label', 'Rétention :')
    security_retention_desc = get_text('security_retention_desc', '30 jours + garde minimum 5 par fichier')
    security_logic_label = get_text('security_logic_label', 'Logique :')
    security_logic_desc = get_text('security_logic_desc', 'Préservation des plus récentes importantes')
    cleanup_backups_title = get_text('cleanup_backups_title', 'Sauvegardes Nettoyage')
    cleanup_retention_label = get_text('cleanup_retention_label', 'Rétention :')
    cleanup_retention_desc = get_text('cleanup_retention_desc', '7 jours (cycle court)')
    cleanup_reason_label = get_text('cleanup_reason_label', 'Raison :')
    cleanup_reason_desc = get_text('cleanup_reason_desc', 'Temporaires, remplacées fréquemment')
    rpa_backups_title = get_text('rpa_backups_title', 'Sauvegardes RPA')
    rpa_retention_label = get_text('rpa_retention_label', 'Rétention :')
    rpa_retention_desc = get_text('rpa_retention_desc', '3 jours (très temporaires)')
    rpa_usage_label = get_text('rpa_usage_label', 'Usage :')
    rpa_usage_desc = get_text('rpa_usage_desc', 'Seulement avant compilation, rotation rapide')
    realtime_backups_title = get_text('realtime_backups_title', 'Sauvegardes Temps Réel')
    realtime_rotation_label = get_text('realtime_rotation_label', 'Rotation automatique :')
    realtime_rotation_desc = get_text('realtime_rotation_desc', '10 fichiers maximum')
    realtime_management_label = get_text('realtime_management_label', 'Gestion :')
    realtime_management_desc = get_text('realtime_management_desc', 'Système de rotation intégré, pas de nettoyage manuel')
    cleanup_process_title = get_text('cleanup_process_title', 'Processus de nettoyage')
    analysis_step_label = get_text('analysis_step_label', 'Analyse :')
    analysis_step_desc = get_text('analysis_step_desc', 'Scan de toutes les sauvegardes avec calcul d\'âge')
    criteria_application_step_label = get_text('criteria_application_step_label', 'Application critères :')
    criteria_application_step_desc = get_text('criteria_application_step_desc', 'Filtrage selon le type et la rétention')
    file_deletion_step_label = get_text('file_deletion_step_label', 'Suppression fichiers :')
    file_deletion_step_desc = get_text('file_deletion_step_desc', 'Suppression physique des fichiers obsolètes')
    metadata_cleanup_step_label = get_text('metadata_cleanup_step_label', 'Nettoyage métadonnées :')
    metadata_cleanup_step_desc = get_text('metadata_cleanup_step_desc', 'Mise à jour des index JSON')
    empty_folders_step_label = get_text('empty_folders_step_label', 'Dossiers vides :')
    empty_folders_step_desc = get_text('empty_folders_step_desc', 'Suppression de l\'arborescence vide')
    final_report_step_label = get_text('final_report_step_label', 'Rapport final :')
    final_report_step_desc = get_text('final_report_step_desc', 'Statistiques détaillées des suppressions')
    use_cases_title = get_text('use_cases_title', 'Cas d\'usage pratiques')
    error_restoration_title = get_text('error_restoration_title', 'Restauration après erreur')
    error_context_label = get_text('error_context_label', 'Contexte :')
    error_context_desc = get_text('error_context_desc', 'Fichier corrompu après modification')
    error_solution_label = get_text('error_solution_label', 'Solution :')
    error_solution_desc = get_text('error_solution_desc', 'Filtre par jeu → Type "Sécurité" → Restaurer dernière version valide')
    disk_audit_title = get_text('disk_audit_title', 'Audit de l\'espace disque')
    disk_context_label = get_text('disk_context_label', 'Contexte :')
    disk_context_desc = get_text('disk_context_desc', 'Vérification utilisation espace')
    disk_usage_label = get_text('disk_usage_label', 'Usage :')
    disk_usage_desc = get_text('disk_usage_desc', 'Statistiques globales + nettoyage automatique ciblé')
    project_change_title = get_text('project_change_title', 'Changement de projet')
    project_context_label = get_text('project_context_label', 'Contexte :')
    project_context_desc = get_text('project_context_desc', 'Travail sur autre jeu')
    project_action_label = get_text('project_action_label', 'Action :')
    project_action_desc = get_text('project_action_desc', 'Filtre par jeu spécifique pour vue dédiée')
    tests_development_title = get_text('tests_development_title', 'Tests et développement')
    tests_context_label = get_text('tests_context_label', 'Contexte :')
    tests_context_desc = get_text('tests_context_desc', 'Expérimentation avec versions multiples')
    tests_workflow_label = get_text('tests_workflow_label', 'Workflow :')
    tests_workflow_desc = get_text('tests_workflow_desc', '"Restaurer vers..." pour tests parallèles')
    best_practices_title = get_text('best_practices_title', 'Bonnes pratiques')
    regular_monitoring_label = get_text('regular_monitoring_label', 'Surveillance régulière :')
    regular_monitoring_desc = get_text('regular_monitoring_desc', 'Vérifiez périodiquement l\'espace utilisé')
    selective_restoration_label = get_text('selective_restoration_label', 'Restauration sélective :')
    selective_restoration_desc = get_text('selective_restoration_desc', 'Utilisez les filtres pour cibler précisément')
    test_before_delete_label = get_text('test_before_delete_label', 'Test avant suppression :')
    test_before_delete_desc = get_text('test_before_delete_desc', 'Vérifiez que vos fichiers principaux sont corrects')
    backup_important_label = get_text('backup_important_label', 'Sauvegarde importante :')
    backup_important_desc = get_text('backup_important_desc', 'Créez vos propres backups avant modifications majeures')
    
    # Génération du contenu HTML
    return f"""
        <div class="quick-nav-section" style="background: var(--card-bg); padding: 20px; margin-bottom: 30px; border-radius: 8px; border-left: 4px solid #4a90e2;">
            <h3>🧭 {quick_nav_title}</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin-top: 15px;">
                <a href="#backup-statistics" class="nav-card-tab6" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">📊 {nav_statistics}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_statistics_desc}</div>
                </a>
                <a href="#backup-restoration" class="nav-card-tab6" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">🔍 {nav_restoration}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_restoration_desc}</div>
                </a>
                <a href="#backup-cleanup" class="nav-card-tab6" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">🧹 {nav_cleanup}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_cleanup_desc}</div>
                </a>
            </div>
        </div>
        
        <style>
        .nav-card-tab6:hover {{
            box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
            border-color: #4a90e2 !important;
            background: linear-gradient(135deg, var(--button-bg) 0%, rgba(74, 144, 226, 0.1) 100%) !important;
        }}
        </style>
        
        <div class="section" id="backup-manager">
            <h2>💾 {title}</h2>
            <p>{description}</p>
            
            {generator._get_image_html("04_interface_sauvegarde", "001", language, backup_main_interface_alt, backup_main_interface_caption)}
    
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #10b981; margin: 15px 0;">
                <h4>🗂️ {hierarchy_title}</h4>
                <p>{hierarchy_desc}</p>
                <p><strong>{advantage_label}</strong> {hierarchy_advantage}</p>
            </div>
            
            <h3>🎯 {purpose_title}</h3>
            <p>{purpose_intro}</p>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <h4>{centralized_view_title}</h4>
                    <p>{centralized_view_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>{smart_filtering_title}</h4>
                    <p>{smart_filtering_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>{one_click_restore_title}</h4>
                    <p>{one_click_restore_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>{auto_cleanup_title}</h4>
                    <p>{auto_cleanup_desc}</p>
                </div>
            </div>
        </div>
    
        <div class="section" id="backup-statistics">
            <h2>📊 {statistics_title}</h2>
            {generator._get_image_html("04_interface_sauvegarde", "002", language, backup_statistics_alt, backup_statistics_caption)}
    
            <h3>{realtime_metrics_title}</h3>
            <p>{realtime_metrics_intro}</p>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <h4>📈 {general_overview_title}</h4>
                    <p><strong>{total_backups_label}</strong> {total_backups_desc}</p>
                    <p><strong>{cumulative_size_label}</strong> {cumulative_size_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>🎮 {game_distribution_title}</h4>
                    <p><strong>{games_concerned_label}</strong> {games_concerned_desc}</p>
                    <p><strong>{distinct_files_label}</strong> {distinct_files_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>🏷️ {type_breakdown_title}</h4>
                    <p><strong>{security_count_label}</strong> {security_count_desc}</p>
                    <p><strong>{cleanup_count_label}</strong> {cleanup_count_desc}</p>
                    <p><strong>{rpa_count_label}</strong> {rpa_count_desc}</p>
                    <p><strong>{realtime_count_label}</strong> {realtime_count_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>⏰ {temporal_analysis_title}</h4>
                    <p><strong>{newest_backup_label}</strong> {newest_backup_desc}</p>
                    <p><strong>{oldest_backup_label}</strong> {oldest_backup_desc}</p>
                </div>
            </div>
        </div>
    
        <div class="section" id="backup-restoration">
            <h2>🔍 {filtering_title}</h2>
            {generator._get_image_html("04_interface_sauvegarde", "003", language, backup_filters_alt, backup_filters_caption)}
    
            <h3>{double_filtering_title}</h3>
            <p>{double_filtering_intro}</p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #4a90e2;">
                    <h4>🎮 {game_filter_title}</h4>
                    <p>{game_filter_desc}</p>
                </div>
                
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #10b981;">
                    <h4>🏷️ {type_filter_title}</h4>
                    <p>{type_filter_desc}</p>
                </div>
                
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #f59e0b;">
                    <h4>🔍 {search_bar_title}</h4>
                    <p>{search_bar_desc}</p>
                </div>
                
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #8b5cf6;">
                    <h4>⚙️ {advanced_filters_title}</h4>
                    <p>{advanced_filters_desc}</p>
                </div>
            </div>
            
            <h3>📋 {list_interface_title}</h3>
            {generator._get_image_html("04_interface_sauvegarde", "004", language, backup_list_alt, backup_list_caption)}
    
            <p>{list_interface_intro}</p>
            
            <ul>
                <li><strong>{game_column_label}</strong> {game_column_desc}</li>
                <li><strong>{file_column_label}</strong> {file_column_desc}</li>
                <li><strong>{type_column_label}</strong> {type_column_desc}</li>
                <li><strong>{date_column_label}</strong> {date_column_desc}</li>
                <li><strong>{size_column_label}</strong> {size_column_desc}</li>
                <li><strong>{path_column_label}</strong> {path_column_desc}</li>
                <li><strong>{actions_column_label}</strong> {actions_column_desc}</li>
            </ul>
            
            <h4>{sorting_options_title}</h4>
            <p>{sorting_options_desc}</p>
            
            <h4>{pagination_title}</h4>
            <p>{pagination_desc}</p>
            
            <h3>⚙️ {actions_menu_title}</h3>
            {generator._get_image_html("04_interface_sauvegarde", "005", language, backup_actions_alt, backup_actions_caption)}
    
            <div class="feature-grid">
                <div class="feature-card">
                    <h4>🔄 {restore_action_label}</h4>
                    <p>{restore_action_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>📂 {restore_to_action_label}</h4>
                    <p>{restore_to_action_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>🗑️ {delete_action_label}</h4>
                    <p>{delete_action_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>ℹ️ {details_action_label}</h4>
                    <p>{details_action_desc}</p>
                </div>
            </div>
            
            <h3>💾 {restoration_process_title}</h3>
            {generator._get_image_html("04_interface_sauvegarde", "007", language, restoration_dialog_alt, restoration_dialog_caption)}
    
            <h4>{secure_workflow_title}</h4>
            <ol>
                <li><strong>{selection_step_label}</strong> {selection_step_desc}</li>
                <li><strong>{confirmation_step_label}</strong> {confirmation_step_desc}</li>
                <li><strong>{path_verification_step_label}</strong> {path_verification_step_desc}</li>
                <li><strong>{restoration_step_label}</strong> {restoration_step_desc}</li>
                <li><strong>{final_confirmation_step_label}</strong> {final_confirmation_step_desc}</li>
            </ol>
    
            <h4>{special_cases_title}</h4>
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #f59e0b; margin: 15px 0;">
                <h5>⚠️ {missing_source_title}</h5>
                <ul>
                    <li><strong>{auto_detection_label}</strong> {auto_detection_fallback_desc}</li>
                    <li><strong>{smart_fallback_label}</strong> {smart_fallback_desc}</li>
                    <li><strong>{manual_mode_label}</strong> {manual_mode_desc}</li>
                    <li><strong>{directory_creation_label}</strong> {directory_creation_desc}</li>
                </ul>
            </div>
        </div>
    
        <div class="section" id="backup-cleanup">
            <h2>🧹 {auto_cleanup_title}</h2>
            {generator._get_image_html("04_interface_sauvegarde", "008", language, cleanup_interface_alt, cleanup_interface_caption)}
    
            <h3>{smart_criteria_title}</h3>
            <p>{smart_criteria_intro}</p>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <h4>🛡️ {security_backups_title}</h4>
                    <p><strong>{security_retention_label}</strong> {security_retention_desc}</p>
                    <p><strong>{security_logic_label}</strong> {security_logic_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>🧹 {cleanup_backups_title}</h4>
                    <p><strong>{cleanup_retention_label}</strong> {cleanup_retention_desc}</p>
                    <p><strong>{cleanup_reason_label}</strong> {cleanup_reason_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>📦 {rpa_backups_title}</h4>
                    <p><strong>{rpa_retention_label}</strong> {rpa_retention_desc}</p>
                    <p><strong>{rpa_usage_label}</strong> {rpa_usage_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>⚡ {realtime_backups_title}</h4>
                    <p><strong>{realtime_rotation_label}</strong> {realtime_rotation_desc}</p>
                    <p><strong>{realtime_management_label}</strong> {realtime_management_desc}</p>
                </div>
            </div>
    
            <h3>{cleanup_process_title}</h3>
            <ol>
                <li><strong>{analysis_step_label}</strong> {analysis_step_desc}</li>
                <li><strong>{criteria_application_step_label}</strong> {criteria_application_step_desc}</li>
                <li><strong>{file_deletion_step_label}</strong> {file_deletion_step_desc}</li>
                <li><strong>{metadata_cleanup_step_label}</strong> {metadata_cleanup_step_desc}</li>
                <li><strong>{empty_folders_step_label}</strong> {empty_folders_step_desc}</li>
                <li><strong>{final_report_step_label}</strong> {final_report_step_desc}</li>
            </ol>
            
            <h3>🎯 {use_cases_title}</h3>
            <div class="feature-grid">
                <div class="feature-card">
                    <h4>🔄 {error_restoration_title}</h4>
                    <p><strong>{error_context_label}</strong> {error_context_desc}</p>
                    <p><strong>{error_solution_label}</strong> {error_solution_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>📊 {disk_audit_title}</h4>
                    <p><strong>{disk_context_label}</strong> {disk_context_desc}</p>
                    <p><strong>{disk_usage_label}</strong> {disk_usage_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>🎮 {project_change_title}</h4>
                    <p><strong>{project_context_label}</strong> {project_context_desc}</p>
                    <p><strong>{project_action_label}</strong> {project_action_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>🧪 {tests_development_title}</h4>
                    <p><strong>{tests_context_label}</strong> {tests_context_desc}</p>
                    <p><strong>{tests_workflow_label}</strong> {tests_workflow_desc}</p>
                </div>
            </div>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #10b981; margin: 20px 0;">
                <h4>💡 {best_practices_title}</h4>
                <ul>
                    <li><strong>{regular_monitoring_label}</strong> {regular_monitoring_desc}</li>
                    <li><strong>{selective_restoration_label}</strong> {selective_restoration_desc}</li>
                    <li><strong>{test_before_delete_label}</strong> {test_before_delete_desc}</li>
                    <li><strong>{backup_important_label}</strong> {backup_important_desc}</li>
                </ul>
            </div>
        </div>
    """