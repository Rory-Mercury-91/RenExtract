# ui/tutorial/content/tab_07.py
"""
Module de contenu pour l'onglet 7 : Paramètres
"""

import html

def generate_content(generator, language, translations):
    """
    Génère le contenu pour l'onglet 7 : Paramètres et Configuration
    
    Args:
        generator: Instance du générateur avec méthodes utilitaires
        language: Code langue (fr, en, de)
        translations: Dictionnaire des traductions
    
    Returns:
        str: HTML généré pour l'onglet paramètres
    """
    # Vérification des traductions
    if not isinstance(translations, dict) or 'tabs' not in translations or 'common' not in translations:
        return "<div>Erreur : Traductions manquantes ou mal formées</div>"
    
    # Récupération des traductions pour cette section
    section_t = translations.get('tabs', {}).get('parametres', {})
    common_t = translations.get('common', {})
    
    def get_text(key, fallback=""):
        """Récupère une traduction avec sanitisation HTML"""
        value = section_t.get(key) or common_t.get(key) or fallback
        return html.escape(value)
    
    # --- Navigation rapide ---
    quick_nav_title = get_text('quick_nav_title', 'Navigation rapide')
    nav_extraction_protection = get_text('nav_extraction_protection', 'Extraction & Protection')
    nav_extraction_protection_desc = get_text('nav_extraction_protection_desc', 'Sauvegardes et détection doublons')
    nav_colors = get_text('nav_colors', 'Couleurs')
    nav_colors_desc = get_text('nav_colors_desc', 'Personnalisation des boutons par catégorie')
    nav_interface_config = get_text('nav_interface_config', 'Interface')
    nav_interface_config_desc = get_text('nav_interface_config_desc', 'Apparence et notifications')
    nav_paths = get_text('nav_paths', 'Chemins d\'accès')
    nav_paths_desc = get_text('nav_paths_desc', 'SDK Ren\'Py et éditeurs de texte')
    
    # --- Section Paramètres de l'application ---
    title = get_text('title', 'Paramètres de l\'application')
    intro = get_text('intro', 'Configuration centralisée accessible via le bouton "⚙️ Paramètres" dans l\'en-tête de l\'interface principale.')
    organization_title = get_text('organization_title', 'Organisation des paramètres')
    organization_desc = get_text('organization_desc', 'Les paramètres sont organisés en 4 catégories principales selon leur fonction.')
    
    # --- Section Extraction & Protection ---
    extraction_title = get_text('extraction_title', 'Extraction & Protection')
    extraction_alt = get_text('extraction_alt', 'Configuration extraction et protection')
    extraction_caption = get_text('extraction_caption', 'Paramètres de protection automatique et gestion des sauvegardes')
    backup_auto_title = get_text('backup_auto_title', 'Sauvegardes automatiques :')
    backup_types_label = get_text('backup_types_label', 'Types de sauvegarde :')
    backup_types_desc = get_text('backup_types_desc', 'Configuration des 4 types (Sécurité, Nettoyage, Avant RPA, Temps réel)')
    backup_rotation_label = get_text('backup_rotation_label', 'Rotation intelligente :')
    backup_rotation_desc = get_text('backup_rotation_desc', 'Nombre maximum de sauvegardes à conserver par type')
    backup_location_label = get_text('backup_location_label', 'Emplacement :')
    backup_location_desc = get_text('backup_location_desc', 'Dossier de stockage des sauvegardes')
    duplicate_detection_title = get_text('duplicate_detection_title', 'Détection de doublons :')
    md5_analysis_label = get_text('md5_analysis_label', 'Analyse MD5 :')
    md5_analysis_desc = get_text('md5_analysis_desc', 'Évite les sauvegardes redondantes')
    space_optimization_label = get_text('space_optimization_label', 'Optimisation espace :')
    space_optimization_desc = get_text('space_optimization_desc', 'Suppression automatique des doublons exacts')
    
    # --- Section Couleurs des boutons ---
    colors_title = get_text('colors_title', 'Couleurs des boutons')
    colors_alt = get_text('colors_alt', 'Personnalisation des couleurs')
    colors_caption = get_text('colors_caption', 'Configuration complète des couleurs par catégorie d\'action')
    color_categories_title = get_text('color_categories_title', 'Catégories de couleurs :')
    primary_actions_title = get_text('primary_actions_title', 'Actions Primaires')
    primary_actions_desc = get_text('primary_actions_desc', 'Extraire, Reconstruire, actions principales du workflow')
    secondary_actions_title = get_text('secondary_actions_title', 'Actions Secondaires')
    secondary_actions_desc = get_text('secondary_actions_desc', 'Actions complémentaires, outils d\'assistance')
    help_actions_title = get_text('help_actions_title', 'Aide & Information')
    help_actions_desc = get_text('help_actions_desc', 'Boutons d\'aide, informations, documentation')
    negative_actions_title = get_text('negative_actions_title', 'Actions Négatives')
    negative_actions_desc = get_text('negative_actions_desc', 'Suppression, nettoyage, actions irréversibles')
    customization_title = get_text('customization_title', 'Personnalisation :')
    presets_label = get_text('presets_label', 'Presets :')
    presets_desc = get_text('presets_desc', 'Thèmes prédéfinis (Classique, Moderne, Contrasté)')
    custom_colors_label = get_text('custom_colors_label', 'Couleurs custom :')
    custom_colors_desc = get_text('custom_colors_desc', 'Sélecteur de couleur pour chaque catégorie')
    realtime_preview_label = get_text('realtime_preview_label', 'Aperçu temps réel :')
    realtime_preview_desc = get_text('realtime_preview_desc', 'Visualisation immédiate des changements')
    
    # --- Section Interface & Application ---
    interface_title = get_text('interface_title', 'Interface & Application')
    interface_alt = get_text('interface_alt', 'Configuration interface utilisateur')
    interface_caption = get_text('interface_caption', 'Paramètres d\'apparence, notifications et actions système')
    appearance_title = get_text('appearance_title', 'Apparence :')
    theme_label = get_text('theme_label', 'Thème :')
    theme_desc = get_text('theme_desc', 'Sombre, clair ou automatique selon le système')
    font_size_label = get_text('font_size_label', 'Taille des polices :')
    font_size_desc = get_text('font_size_desc', 'Ajustement pour la lisibilité')
    animations_label = get_text('animations_label', 'Animations :')
    animations_desc = get_text('animations_desc', 'Activation/désactivation des transitions')
    notifications_title = get_text('notifications_title', 'Notifications :')
    system_notifications_label = get_text('system_notifications_label', 'Notifications système :')
    system_notifications_desc = get_text('system_notifications_desc', 'Alertes Windows pour les opérations terminées')
    sounds_label = get_text('sounds_label', 'Sons :')
    sounds_desc = get_text('sounds_desc', 'Signaux sonores pour les événements importants')
    popups_label = get_text('popups_label', 'Popups :')
    popups_desc = get_text('popups_desc', 'Fenêtres d\'information pour les résultats')
    behavior_title = get_text('behavior_title', 'Comportement :')
    auto_open_label = get_text('auto_open_label', 'Ouvertures automatiques :')
    auto_open_desc = get_text('auto_open_desc', 'Dossiers et éditeurs après les opérations')
    confirmations_label = get_text('confirmations_label', 'Confirmations :')
    confirmations_desc = get_text('confirmations_desc', 'Demandes de confirmation pour les actions sensibles')
    memorization_label = get_text('memorization_label', 'Mémorisation :')
    memorization_desc = get_text('memorization_desc', 'Sauvegarde de la dernière configuration utilisée')
    
    # --- Section Chemins d'accès ---
    paths_title = get_text('paths_title', 'Chemins d\'accès')
    paths_alt = get_text('paths_alt', 'Configuration chemins et éditeurs')
    paths_caption = get_text('paths_caption', 'Paramétrage du SDK Ren\'Py et éditeurs de code')
    renpy_sdk_title = get_text('renpy_sdk_title', 'SDK Ren\'Py :')
    auto_detection_label = get_text('auto_detection_label', 'Détection automatique :')
    auto_detection_desc = get_text('auto_detection_desc', 'Recherche des installations SDK sur le système')
    manual_path_label = get_text('manual_path_label', 'Chemin manuel :')
    manual_path_desc = get_text('manual_path_desc', 'Spécification d\'un SDK personnalisé')
    integrated_download_label = get_text('integrated_download_label', 'Téléchargement intégré :')
    integrated_download_desc = get_text('integrated_download_desc', 'Installation automatique si aucun SDK trouvé')
    text_editors_title = get_text('text_editors_title', 'Éditeurs de texte :')
    detected_editors_label = get_text('detected_editors_label', 'Éditeurs détectés :')
    detected_editors_desc = get_text('detected_editors_desc', 'VSCode, Notepad++, Sublime Text, etc.')
    default_editor_label = get_text('default_editor_label', 'Éditeur par défaut :')
    default_editor_desc = get_text('default_editor_desc', 'Choix de l\'éditeur principal')
    custom_args_label = get_text('custom_args_label', 'Arguments personnalisés :')
    custom_args_desc = get_text('custom_args_desc', 'Paramètres de lancement spécifiques')
    work_folders_title = get_text('work_folders_title', 'Dossiers de travail :')
    temp_folder_label = get_text('temp_folder_label', 'Dossier temporaire :')
    temp_folder_desc = get_text('temp_folder_desc', 'Emplacement des fichiers .txt à traduire')
    backup_folder_label = get_text('backup_folder_label', 'Dossier sauvegardes :')
    backup_folder_desc = get_text('backup_folder_desc', 'Stockage des copies de sécurité')
    reports_folder_label = get_text('reports_folder_label', 'Dossier rapports :')
    reports_folder_desc = get_text('reports_folder_desc', 'Emplacement des rapports de cohérence')
    
    # Génération du contenu HTML
    return f"""
        <div class="quick-nav-section" style="background: var(--card-bg); padding: 20px; margin-bottom: 30px; border-radius: 8px; border-left: 4px solid #4a90e2;">
            <h3>🧭 {quick_nav_title}</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin-top: 15px;">
                <a href="#config-extraction" class="nav-card-tab7" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">🛡️ {nav_extraction_protection}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_extraction_protection_desc}</div>
                </a>
                <a href="#config-colors" class="nav-card-tab7" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">🎨 {nav_colors}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_colors_desc}</div>
                </a>
                <a href="#config-interface" class="nav-card-tab7" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">🖥️ {nav_interface_config}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_interface_config_desc}</div>
                </a>
                <a href="#config-paths" class="nav-card-tab7" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">🛠️ {nav_paths}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_paths_desc}</div>
                </a>
            </div>
        </div>
        
        <style>
        .nav-card-tab7:hover {{
            box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
            border-color: #4a90e2 !important;
            background: linear-gradient(135deg, var(--button-bg) 0%, rgba(74, 144, 226, 0.1) 100%) !important;
        }}
        </style>
        
        <div class="section" id="config-details">
            <h2>⚙️ {title}</h2>
            <p>{intro}</p>
            
            <h3>🗂️ {organization_title}</h3>
            <p>{organization_desc}</p>
        </div>
        
        <div class="section" id="config-extraction">
            <h3>🛡️ {extraction_title}</h3>
            {generator._get_image_html("05_interface_parametres", "001", language, extraction_alt, extraction_caption)}
            
            <h4>{backup_auto_title}</h4>
            <ul>
                <li><strong>{backup_types_label}</strong> {backup_types_desc}</li>
                <li><strong>{backup_rotation_label}</strong> {backup_rotation_desc}</li>
                <li><strong>{backup_location_label}</strong> {backup_location_desc}</li>
            </ul>
            
            <h4>{duplicate_detection_title}</h4>
            <ul>
                <li><strong>{md5_analysis_label}</strong> {md5_analysis_desc}</li>
                <li><strong>{space_optimization_label}</strong> {space_optimization_desc}</li>
            </ul>
        </div>
        
        <div class="section" id="config-colors">
            <h3>🎨 {colors_title}</h3>
            {generator._get_image_html("05_interface_parametres", "002", language, colors_alt, colors_caption)}
            
            <h4>{color_categories_title}</h4>
            <div class="feature-grid">
                <div class="feature-card">
                    <h5>🔵 {primary_actions_title}</h5>
                    <p>{primary_actions_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h5>🟢 {secondary_actions_title}</h5>
                    <p>{secondary_actions_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h5>🟡 {help_actions_title}</h5>
                    <p>{help_actions_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h5>🔴 {negative_actions_title}</h5>
                    <p>{negative_actions_desc}</p>
                </div>
            </div>
            
            <h4>{customization_title}</h4>
            <ul>
                <li><strong>{presets_label}</strong> {presets_desc}</li>
                <li><strong>{custom_colors_label}</strong> {custom_colors_desc}</li>
                <li><strong>{realtime_preview_label}</strong> {realtime_preview_desc}</li>
            </ul>
        </div>
        
        <div class="section" id="config-interface">
            <h3>🖥️ {interface_title}</h3>
            {generator._get_image_html("05_interface_parametres", "003", language, interface_alt, interface_caption)}
            
            <h4>{appearance_title}</h4>
            <ul>
                <li><strong>{theme_label}</strong> {theme_desc}</li>
                <li><strong>{font_size_label}</strong> {font_size_desc}</li>
                <li><strong>{animations_label}</strong> {animations_desc}</li>
            </ul>
            
            <h4>{notifications_title}</h4>
            <ul>
                <li><strong>{system_notifications_label}</strong> {system_notifications_desc}</li>
                <li><strong>{sounds_label}</strong> {sounds_desc}</li>
                <li><strong>{popups_label}</strong> {popups_desc}</li>
            </ul>
            
            <h4>{behavior_title}</h4>
            <ul>
                <li><strong>{auto_open_label}</strong> {auto_open_desc}</li>
                <li><strong>{confirmations_label}</strong> {confirmations_desc}</li>
                <li><strong>{memorization_label}</strong> {memorization_desc}</li>
            </ul>
        </div>
        
        <div class="section" id="config-paths">
            <h3>🛠️ {paths_title}</h3>
            {generator._get_image_html("05_interface_parametres", "004", language, paths_alt, paths_caption)}
            
            <h4>{renpy_sdk_title}</h4>
            <ul>
                <li><strong>{auto_detection_label}</strong> {auto_detection_desc}</li>
                <li><strong>{manual_path_label}</strong> {manual_path_desc}</li>
                <li><strong>{integrated_download_label}</strong> {integrated_download_desc}</li>
            </ul>
            
            <h4>{text_editors_title}</h4>
            <ul>
                <li><strong>{detected_editors_label}</strong> {detected_editors_desc}</li>
                <li><strong>{default_editor_label}</strong> {default_editor_desc}</li>
                <li><strong>{custom_args_label}</strong> {custom_args_desc}</li>
            </ul>
            
            <h4>{work_folders_title}</h4>
            <ul>
                <li><strong>{temp_folder_label}</strong> {temp_folder_desc}</li>
                <li><strong>{backup_folder_label}</strong> {backup_folder_desc}</li>
                <li><strong>{reports_folder_label}</strong> {reports_folder_desc}</li>
            </ul>
        </div>
    """