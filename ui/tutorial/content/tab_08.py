# ui/tutorial/content/tab_08.py
"""
Module de contenu pour l'onglet 8 : Détail technique
"""

import html

def generate_content(generator, language, translations):
    """
    Génère le contenu pour l'onglet 8 : Détails Techniques
    
    Args:
        generator: Instance du générateur avec méthodes utilitaires
        language: Code langue (fr, en, de)
        translations: Dictionnaire des traductions
    
    Returns:
        str: HTML généré pour l'onglet détails techniques
    """
    # Vérification des traductions
    if not isinstance(translations, dict) or 'tabs' not in translations or 'common' not in translations:
        return "<div>Erreur : Traductions manquantes ou mal formées</div>"
    
    # Récupération des traductions pour cette section
    section_t = translations.get('tabs', {}).get('technique', {})
    common_t = translations.get('common', {})
    
    def get_text(key, fallback=""):
        """Récupère une traduction avec sanitisation HTML"""
        value = section_t.get(key) or common_t.get(key) or fallback
        return html.escape(value)
    
    # --- Navigation rapide ---
    quick_nav_title = get_text('quick_nav_title', 'Navigation rapide')
    nav_extraction_system = get_text('nav_extraction_system', 'Système Extraction')
    nav_extraction_system_desc = get_text('nav_extraction_system_desc', 'Patterns et architecture temporaire')
    nav_backup_architecture = get_text('nav_backup_architecture', 'Architecture Sauvegardes')
    nav_backup_architecture_desc = get_text('nav_backup_architecture_desc', 'Structure hiérarchique et rotation')
    nav_performance = get_text('nav_performance', 'Performance')
    nav_performance_desc = get_text('nav_performance_desc', 'Optimisation et gestion mémoire')
    nav_integration = get_text('nav_integration', 'Intégration Système')
    nav_integration_desc = get_text('nav_integration_desc', 'État partagé et extensibilité')
    
    # --- Section Système d'Extraction/Reconstruction ---
    extraction_title = get_text('extraction_title', 'Système d\'Extraction/Reconstruction')
    extraction_intro = get_text('extraction_intro', 'Vue technique du processus qui transforme un fichier Ren\'Py en fichiers de traduction, puis reconstruit le résultat final.')
    config_protections_title = get_text('config_protections_title', 'Configuration des protections')
    config_protections_alt = get_text('config_protections_alt', 'Configuration patterns')
    config_protections_caption = get_text('config_protections_caption', 'Paramètres d\'extraction avec patterns personnalisables')
    patterns_intro = get_text('patterns_intro', 'RenExtract utilise des patterns personnalisables pour protéger différents types d\'éléments :')
    variables_title = get_text('variables_title', 'Variables et codes (01)')
    variables_desc = get_text('variables_desc', 'Protège [player_name], {{color=#ff0000}}, {{/color}}')
    asterix_title = get_text('asterix_title', 'Astérisques (B01)')
    asterix_desc = get_text('asterix_desc', 'Protège *sigh*, **emphasis**, actions narratives')
    tildes_title = get_text('tildes_title', 'Tildes (C01)')
    tildes_desc = get_text('tildes_desc', 'Protège ~~whisper~~, ~~~secret~~~, chuchotements')
    empty_elements_title = get_text('empty_elements_title', 'Éléments vides')
    empty_elements_desc = get_text('empty_elements_desc', 'Gère les chaînes vides, narrateur, séparateurs structurels')
    preparation_interface_title = get_text('preparation_interface_title', 'Interface de préparation')
    preparation_interface_alt = get_text('preparation_interface_alt', 'Interface préparation')
    preparation_interface_caption = get_text('preparation_interface_caption', 'Zone d\'information avec fichier chargé et prêt pour extraction')
    concrete_example_title = get_text('concrete_example_title', 'Exemple concret : suivi d\'une ligne complexe')
    concrete_example_intro = get_text('concrete_example_intro', 'Prenons cette ligne Ren\'Py qui contient tous les éléments problématiques :')
    step1_title = get_text('step1_title', 'Étape 1 : Ligne originale')
    step2_title = get_text('step2_title', 'Étape 2 : Après protection (fichier with_placeholders.rpy)')
    transformations_applied = get_text('transformations_applied', 'Transformations appliquées :')
    step3_title = get_text('step3_title', 'Étape 3 : Contenu extrait (fichier _dialogue.txt)')
    step3_desc = get_text('step3_desc', 'Le traducteur voit cette ligne avec les placeholders pour comprendre le contexte, mais ne traduit que le texte en gardant les codes intacts.')
    step4_title = get_text('step4_title', 'Étape 4 : Après traduction')
    step4_desc = get_text('step4_desc', 'Le traducteur a conservé tous les placeholders et traduit uniquement le texte visible.')
    step5_title = get_text('step5_title', 'Étape 5 : Résultat final reconstruit')
    restorations_applied = get_text('restorations_applied', 'Restaurations appliquées :')
    content_translated = get_text('content_translated', '(contenu traduit)')
    metadata_files_title = get_text('metadata_files_title', 'Fichiers de métadonnées')
    metadata_files_intro = get_text('metadata_files_intro', 'Le processus génère des fichiers techniques pour assurer la cohérence :')
    placeholder_mapping_title = get_text('placeholder_mapping_title', 'Mapping des placeholders (invisible_mapping.txt)')
    asterix_metadata_title = get_text('asterix_metadata_title', 'ASTÉRISQUES AVEC MÉTADONNÉES')
    tildes_metadata_title = get_text('tildes_metadata_title', 'TILDES AVEC MÉTADONNÉES')
    position_data_title = get_text('position_data_title', 'Données de position (positions.json)')
    position_data_desc = get_text('position_data_desc', 'Structure JSON qui stocke l\'emplacement de chaque élément et ses métadonnées :')
    temp_architecture_title = get_text('temp_architecture_title', 'Architecture des fichiers temporaires')
    temp_architecture_alt = get_text('temp_architecture_alt', 'Arborescence fichiers')
    temp_architecture_caption = get_text('temp_architecture_caption', 'Structure des dossiers temporaires avec organisation logique')
    temp_architecture_intro = get_text('temp_architecture_intro', 'Organisation des fichiers générés lors de l\'extraction :')
    main_text_file = get_text('main_text_file', 'Texte principal à traduire')
    duplicates_file = get_text('duplicates_file', 'Textes en double (optionnel)')
    actions_file = get_text('actions_file', 'Actions (*sigh*) et murmures (~~whisper~~)')
    protected_version_file = get_text('protected_version_file', 'Version avec codes protégés')
    reconstruction_metadata_file = get_text('reconstruction_metadata_file', 'Métadonnées de reconstruction')
    placeholder_correspondences_file = get_text('placeholder_correspondences_file', 'Correspondances placeholders')
    empty_strings_file = get_text('empty_strings_file', 'Chaînes vides (référence)')
    separation_logic_title = get_text('separation_logic_title', 'Logique de séparation')
    to_translate_folder = get_text('to_translate_folder', 'fichiers_a_traduire/ :')
    to_translate_desc = get_text('to_translate_desc', 'Ce que le traducteur doit modifier')
    not_to_translate_folder = get_text('not_to_translate_folder', 'fichiers_a_ne_pas_traduire/ :')
    not_to_translate_desc = get_text('not_to_translate_desc', 'Métadonnées techniques pour la reconstruction')
    
    # --- Section Architecture des Sauvegardes ---
    backup_architecture_title = get_text('backup_architecture_title', 'Architecture des Sauvegardes')
    backup_architecture_intro = get_text('backup_architecture_intro', 'Système de protection automatique avec 4 types de sauvegardes et rotation intelligente.')
    hierarchical_structure_title = get_text('hierarchical_structure_title', 'Structure hiérarchique')
    before_reconstruction = get_text('before_reconstruction', 'Avant reconstruction')
    before_tl_cleanup = get_text('before_tl_cleanup', 'Avant nettoyage TL')
    before_rpa_compilation = get_text('before_rpa_compilation', 'Avant compilation RPA')
    realtime_editor = get_text('realtime_editor', 'Éditeur temps réel')
    global_backup_index = get_text('global_backup_index', 'Index global des sauvegardes')
    md5_hashes_anti_duplicates = get_text('md5_hashes_anti_duplicates', 'Hachages MD5 anti-doublons')
    automatic_rotation_title = get_text('automatic_rotation_title', 'Rotation automatique')
    security_rotation_title = get_text('security_rotation_title', 'Sécurité (30 jours)')
    security_rotation_desc = get_text('security_rotation_desc', 'Avant chaque reconstruction, minimum 5 par fichier')
    cleanup_rotation_title = get_text('cleanup_rotation_title', 'Nettoyage (7 jours)')
    cleanup_rotation_desc = get_text('cleanup_rotation_desc', 'Avant suppression de traductions orphelines')
    rpa_rotation_title = get_text('rpa_rotation_title', 'RPA Build (3 jours)')
    rpa_rotation_desc = get_text('rpa_rotation_desc', 'Avant compilation d\'archives personnalisées')
    realtime_rotation_title = get_text('realtime_rotation_title', 'Temps réel (10 fichiers)')
    realtime_rotation_desc = get_text('realtime_rotation_desc', 'Rotation par nombre pour l\'éditeur en direct')
    
    # --- Section Optimisation et Performance ---
    optimization_title = get_text('optimization_title', 'Optimisation et Performance')
    optimization_intro = get_text('optimization_intro', 'Mécanismes pour traiter efficacement les gros projets de traduction.')
    smart_cache_title = get_text('smart_cache_title', 'Cache intelligent')
    ast_analysis_label = get_text('ast_analysis_label', 'Analyse AST :')
    ast_analysis_desc = get_text('ast_analysis_desc', 'Mise en cache des structures syntaxiques analysées')
    validation_patterns_label = get_text('validation_patterns_label', 'Patterns de validation :')
    validation_patterns_desc = get_text('validation_patterns_desc', 'Résultats de détection mis en mémoire')
    metadata_cache_label = get_text('metadata_cache_label', 'Métadonnées :')
    metadata_cache_desc = get_text('metadata_cache_desc', 'Index des correspondances placeholders → contenu')
    threading_title = get_text('threading_title', 'Threading et parallélisation')
    extraction_threading_label = get_text('extraction_threading_label', 'Extraction :')
    extraction_threading_desc = get_text('extraction_threading_desc', 'Traitement parallèle des protections par type')
    validation_threading_label = get_text('validation_threading_label', 'Validation :')
    validation_threading_desc = get_text('validation_threading_desc', 'Analyse multi-thread des gros fichiers')
    reconstruction_threading_label = get_text('reconstruction_threading_label', 'Reconstruction :')
    reconstruction_threading_desc = get_text('reconstruction_threading_desc', 'Restauration simultanée des placeholders')
    memory_management_title = get_text('memory_management_title', 'Gestion mémoire')
    streaming_label = get_text('streaming_label', 'Streaming :')
    streaming_desc = get_text('streaming_desc', 'Lecture par chunks pour les fichiers > 50 MB')
    compression_label = get_text('compression_label', 'Compression :')
    compression_desc = get_text('compression_desc', 'Métadonnées JSON compressées automatiquement')
    cleanup_memory_label = get_text('cleanup_memory_label', 'Cleanup :')
    cleanup_memory_desc = get_text('cleanup_memory_desc', 'Libération immédiate des objets temporaires')
    
    # --- Section Intégration Système ---
    system_integration_title = get_text('system_integration_title', 'Intégration Système')
    system_integration_intro = get_text('system_integration_intro', 'Communication entre les composants et extensibilité de RenExtract.')
    shared_state_title = get_text('shared_state_title', 'État partagé')
    active_project_label = get_text('active_project_label', 'Projet actif :')
    active_project_desc = get_text('active_project_desc', 'Configuration synchronisée entre tous les outils')
    distributed_cache_label = get_text('distributed_cache_label', 'Cache distribué :')
    distributed_cache_desc = get_text('distributed_cache_desc', 'Métadonnées partagées Interface ↔ Générateur ↔ Outils')
    events_label = get_text('events_label', 'Événements :')
    events_desc = get_text('events_desc', 'Notifications automatiques entre fenêtres')
    centralized_config_title = get_text('centralized_config_title', 'Configuration centralisée')
    custom_patterns_label = get_text('custom_patterns_label', 'Patterns personnalisés :')
    custom_patterns_desc = get_text('custom_patterns_desc', 'Un changement appliqué partout')
    extraction_settings_label = get_text('extraction_settings_label', 'Paramètres extraction :')
    extraction_settings_desc = get_text('extraction_settings_desc', 'Cohérence totale du workflow')
    user_profiles_label = get_text('user_profiles_label', 'Profils utilisateur :')
    user_profiles_desc = get_text('user_profiles_desc', 'Sauvegarde des préférences')
    hooks_extensibility_title = get_text('hooks_extensibility_title', 'Hooks et extensibilité')
    internal_api_label = get_text('internal_api_label', 'API interne :')
    internal_api_desc = get_text('internal_api_desc', 'Points d\'entrée pour scripts personnalisés')
    potential_plugins_label = get_text('potential_plugins_label', 'Plugins potentiels :')
    potential_plugins_desc = get_text('potential_plugins_desc', 'Système d\'extensions prévu')
    automation_label = get_text('automation_label', 'Automation :')
    automation_desc = get_text('automation_desc', 'Intégration possible dans des workflows CI/CD')
    technical_vision_title = get_text('technical_vision_title', 'Vision technique')
    technical_vision_desc = get_text('technical_vision_desc', 'RenExtract combine robustesse (protection des données), performance (traitement rapide) et flexibilité (adaptation aux besoins) pour offrir un outil de traduction professionnel adapté aux projets Ren\'Py de toute taille.')
    
    # Génération du contenu HTML
    return f"""
        <div class="quick-nav-section" style="background: var(--card-bg); padding: 20px; margin-bottom: 30px; border-radius: 8px; border-left: 4px solid #4a90e2;">
            <h3>🧭 {quick_nav_title}</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin-top: 15px;">
                <a href="#tech-extraction" class="nav-card-tab8" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">🔧 {nav_extraction_system}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_extraction_system_desc}</div>
                </a>
                <a href="#tech-architecture" class="nav-card-tab8" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">🗃️ {nav_backup_architecture}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_backup_architecture_desc}</div>
                </a>
                <a href="#tech-performance" class="nav-card-tab8" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">⚡ {nav_performance}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_performance_desc}</div>
                </a>
                <a href="#tech-integration" class="nav-card-tab8" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">🔗 {nav_integration}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_integration_desc}</div>
                </a>
            </div>
        </div>
        
        <style>
        .nav-card-tab8:hover {{
            box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
            border-color: #4a90e2 !important;
            background: linear-gradient(135deg, var(--button-bg) 0%, rgba(74, 144, 226, 0.1) 100%) !important;
        }}
        </style>
        
        <div class="section" id="tech-extraction">
            <h2>🔧 {extraction_title}</h2>
            <p>{extraction_intro}</p>
            
            <h3>📋 {config_protections_title}</h3>
            {generator._get_image_html("01_interface_principale", "004", language, config_protections_alt, config_protections_caption)}
            
            <p>{patterns_intro}</p>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <h4>{variables_title}</h4>
                    <p>{variables_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>{asterix_title}</h4>
                    <p>{asterix_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>{tildes_title}</h4>
                    <p>{tildes_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>{empty_elements_title}</h4>
                    <p>{empty_elements_desc}</p>
                </div>
            </div>
            
            <h3>⚡ {preparation_interface_title}</h3>
            {generator._get_image_html("01_interface_principale", "005", language, preparation_interface_alt, preparation_interface_caption)}
            
            <h3>📖 {concrete_example_title}</h3>
            <p>{concrete_example_intro}</p>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4>{step1_title}</h4>
                <pre style="background: var(--sep); padding: 10px; border-radius: 4px; overflow-x: auto;">alice "Hello [player_name]! {{color=#ff0000}}How are you?{{/color}} *sigh* ~~whisper~~" with dissolve</pre>
            </div>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4>{step2_title}</h4>
                <pre style="background: var(--sep); padding: 10px; border-radius: 4px; overflow-x: auto;">alice "Hello (01)! (02)How are you?(03) (B01) (C01)" with dissolve</pre>
                <p><strong>{transformations_applied}</strong></p>
                <ul>
                    <li><code>[player_name]</code> → <code>(01)</code></li>
                    <li><code>{{color=#ff0000}}</code> → <code>(02)</code></li>
                    <li><code>{{/color}}</code> → <code>(03)</code></li>
                    <li><code>*sigh*</code> → <code>(B01)</code></li>
                    <li><code>~~whisper~~</code> → <code>(C01)</code></li>
                </ul>
            </div>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4>{step3_title}</h4>
                <pre style="background: var(--sep); padding: 10px; border-radius: 4px; overflow-x: auto;">Hello (01)! (02)How are you?(03) (B01) (C01)</pre>
                <p>{step3_desc}</p>
            </div>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4>{step4_title}</h4>
                <pre style="background: var(--sep); padding: 10px; border-radius: 4px; overflow-x: auto;">Bonjour (01)! (02)Comment allez-vous ?(03) (B01) (C01)</pre>
                <p>{step4_desc}</p>
            </div>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4>{step5_title}</h4>
                <pre style="background: var(--sep); padding: 10px; border-radius: 4px; overflow-x: auto;">alice "Bonjour [player_name]! {{color=#ff0000}}Comment allez-vous ?{{/color}} *soupir* ~~murmure~~" with dissolve</pre>
                <p><strong>{restorations_applied}</strong></p>
                <ul>
                    <li><code>(01)</code> → <code>[player_name]</code></li>
                    <li><code>(02)</code> → <code>{{color=#ff0000}}</code></li>
                    <li><code>(03)</code> → <code>{{/color}}</code></li>
                    <li><code>(B01)</code> → <code>*soupir*</code> {content_translated}</li>
                    <li><code>(C01)</code> → <code>~~murmure~~</code> {content_translated}</li>
                </ul>
            </div>
            
            <h3>📊 {metadata_files_title}</h3>
            <p>{metadata_files_intro}</p>
            
            <h4>{placeholder_mapping_title}</h4>
            <pre style="background: var(--sep); padding: 10px; border-radius: 4px; overflow-x: auto; font-size: 0.9em;">
(01) => [player_name]
(02) => {{color=#ff0000}}
(03) => {{/color}}

# === {asterix_metadata_title} ===
(B01) => *sigh* [PREFIX:1*, SUFFIX:1*, CONTENT:'sigh']

# === {tildes_metadata_title} ===
(C01) => ~~whisper~~ [PREFIX:2~, SUFFIX:2~, CONTENT:'whisper']
            </pre>
            
            <h4>{position_data_title}</h4>
            <p>{position_data_desc}</p>
            <pre style="background: var(--sep); padding: 10px; border-radius: 4px; overflow-x: auto; font-size: 0.9em;">{{
    "line_to_content_indices": {{"4": [0]}},
    "original_lines": {{"4": "alice \\"Hello (01)! ...\\" with dissolve"}},
    "suffixes": [" with dissolve"],
    "asterix_metadata": {{
        "(B01)": {{"prefix_count": 1, "content": "sigh"}}
    }},
    "tilde_metadata": {{
        "(C01)": {{"prefix_count": 2, "content": "whisper"}}
    }}
}}</pre>
            
            <h3>🗂 {temp_architecture_title}</h3>
            {generator._get_image_html("01_interface_principale", "006", language, temp_architecture_alt, temp_architecture_caption)}
            
            <p>{temp_architecture_intro}</p>
            
            <pre style="background: var(--sep); padding: 15px; border-radius: 4px; font-family: monospace; font-size: 0.9em;">01_Temporaires/
    ├── NomDuJeu/
    │   └── script/
    │       ├── fichiers_a_traduire/
    │       │   ├── script_dialogue.txt       # {main_text_file}
    │       │   ├── script_doublons.txt       # {duplicates_file}
    │       │   └── script_asterix.txt        # {actions_file}
    │       └── fichiers_a_ne_pas_traduire/
    │           ├── script_with_placeholders.rpy     # {protected_version_file}
    │           ├── script_positions.json            # {reconstruction_metadata_file}
    │           ├── script_invisible_mapping.txt     # {placeholder_correspondences_file}
    │           └── script_empty.txt                 # {empty_strings_file}</pre>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--accent); margin: 15px 0;">
                <h4>{separation_logic_title}</h4>
                <ul>
                    <li><strong>{to_translate_folder}</strong> {to_translate_desc}</li>
                    <li><strong>{not_to_translate_folder}</strong> {not_to_translate_desc}</li>
                </ul>
            </div>
        </div>
        
        <div class="section" id="tech-architecture">
            <h2>🗃️ {backup_architecture_title}</h2>
            <p>{backup_architecture_intro}</p>
            
            <h3>📂 {hierarchical_structure_title}</h3>
            <pre style="background: var(--sep); padding: 15px; border-radius: 4px; font-family: monospace; font-size: 0.9em;">02_Sauvegarde/
    ├── NomDuJeu/
    │   ├── script/
    │   │   ├── security/
    │   │   │   ├── script_20240920_143022.backup          # {before_reconstruction}
    │   │   │   └── script_20240920_143125.backup
    │   │   ├── cleanup/
    │   │   │   └── script_20240920_142830.backup          # {before_tl_cleanup}
    │   │   ├── rpa_build/
    │   │   │   └── script_20240920_141205.backup          # {before_rpa_compilation}
    │   │   └── realtime/
    │   │       ├── script_modification_001.backup         # {realtime_editor}
    │   │       └── script_modification_002.backup
    │   └── metadata/
    │       ├── index.json                                # {global_backup_index}
    │       └── checksums.json                            # {md5_hashes_anti_duplicates}</pre>
            
            <h3>🔄 {automatic_rotation_title}</h3>
            <div class="feature-grid">
                <div class="feature-card">
                    <h4>{security_rotation_title}</h4>
                    <p>{security_rotation_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>{cleanup_rotation_title}</h4>
                    <p>{cleanup_rotation_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>{rpa_rotation_title}</h4>
                    <p>{rpa_rotation_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>{realtime_rotation_title}</h4>
                    <p>{realtime_rotation_desc}</p>
                </div>
            </div>
        </div>
        
        <div class="section" id="tech-performance">
            <h2>⚡ {optimization_title}</h2>
            <p>{optimization_intro}</p>
            
            <h3>🧠 {smart_cache_title}</h3>
            <ul>
                <li><strong>{ast_analysis_label}</strong> {ast_analysis_desc}</li>
                <li><strong>{validation_patterns_label}</strong> {validation_patterns_desc}</li>
                <li><strong>{metadata_cache_label}</strong> {metadata_cache_desc}</li>
            </ul>
            
            <h3>🔀 {threading_title}</h3>
            <ul>
                <li><strong>{extraction_threading_label}</strong> {extraction_threading_desc}</li>
                <li><strong>{validation_threading_label}</strong> {validation_threading_desc}</li>
                <li><strong>{reconstruction_threading_label}</strong> {reconstruction_threading_desc}</li>
            </ul>
            
            <h3>💾 {memory_management_title}</h3>
            <ul>
                <li><strong>{streaming_label}</strong> {streaming_desc}</li>
                <li><strong>{compression_label}</strong> {compression_desc}</li>
                <li><strong>{cleanup_memory_label}</strong> {cleanup_memory_desc}</li>
            </ul>
        </div>
        
        <div class="section" id="tech-integration">
            <h2>🔗 {system_integration_title}</h2>
            <p>{system_integration_intro}</p>
            
            <h3>📡 {shared_state_title}</h3>
            <ul>
                <li><strong>{active_project_label}</strong> {active_project_desc}</li>
                <li><strong>{distributed_cache_label}</strong> {distributed_cache_desc}</li>
                <li><strong>{events_label}</strong> {events_desc}</li>
            </ul>
            
            <h3>⚙️ {centralized_config_title}</h3>
            <ul>
                <li><strong>{custom_patterns_label}</strong> {custom_patterns_desc}</li>
                <li><strong>{extraction_settings_label}</strong> {extraction_settings_desc}</li>
                <li><strong>{user_profiles_label}</strong> {user_profiles_desc}</li>
            </ul>
            
            <h3>🔌 {hooks_extensibility_title}</h3>
            <ul>
                <li><strong>{internal_api_label}</strong> {internal_api_desc}</li>
                <li><strong>{potential_plugins_label}</strong> {potential_plugins_desc}</li>
                <li><strong>{automation_label}</strong> {automation_desc}</li>
            </ul>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--success); margin: 20px 0;">
                <h4>{technical_vision_title}</h4>
                <p>{technical_vision_desc}</p>
            </div>
        </div>
    """