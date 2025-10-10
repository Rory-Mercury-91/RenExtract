# ui/tutorial/content/tab_03.py
"""
Module de contenu pour l'onglet 3 : Interface Principale
"""

import html

def generate_content(generator, language, translations):
    """Génère le contenu de l'onglet Interface Principale
    
    Args:
        generator: Instance du générateur avec méthodes utilitaires
        language: Code langue (fr, en, de)
        translations: Dictionnaire des traductions
    
    Returns:
        str: HTML généré pour l'onglet interface principale
    """
    # Vérification des traductions
    if not isinstance(translations, dict) or 'tabs' not in translations or 'common' not in translations:
        return "<div>Erreur : Traductions manquantes ou mal formées</div>"
    
    # Récupérer les traductions spécifiques à l'interface
    section_t = translations.get('tabs', {}).get('interface', {})
    common_t = translations.get('common', {})
    
    def get_text(key, fallback=""):
        """Récupère une traduction avec sanitisation HTML"""
        value = section_t.get(key) or common_t.get(key) or fallback
        return html.escape(value)
    
    # --- Navigation rapide ---
    quick_nav_title = get_text('quick_nav_title', 'Navigation rapide')
    nav_preparation = get_text('nav_preparation', 'Préparation')
    nav_preparation_desc = get_text('nav_preparation_desc', 'Sélection et validation des fichiers')
    nav_actions = get_text('nav_actions', 'Actions')
    nav_actions_desc = get_text('nav_actions_desc', 'Workflow principal de traduction')
    nav_outils = get_text('nav_outils', 'Outils')
    nav_outils_desc = get_text('nav_outils_desc', 'Accès rapide et intégration système')
    
    # --- Vue d'ensemble ---
    overview_title = get_text('overview_title', 'Interface Principale - Vue d\'ensemble')
    overview_description = get_text('overview_description', 'L\'interface que vous voyez au démarrage de RenExtract. Elle s\'organise autour de 3 onglets principaux qui suivent le workflow de traduction fichier par fichier.')
    overview_organization = get_text('overview_organization', 'Organisation des onglets')
    overview_logic = get_text('overview_logic', 'L\'interface suit une logique linéaire : préparer → agir → utiliser les outils complémentaires.')
    
    # --- Onglet Préparation ---
    preparation_title = get_text('preparation_title', 'Onglet Préparation')
    preparation_features = get_text('preparation_features', 'Fonctionnalités principales :')
    preparation_selection = get_text('preparation_selection', 'Sélection de fichier : Glisser-déposer ou bouton Parcourir pour choisir un fichier .rpy')
    preparation_validation = get_text('preparation_validation', 'Validation automatique : Vérification que le fichier est traitable')
    preparation_quick_access = get_text('preparation_quick_access', 'Accès rapide : Boutons pour ouvrir les dossiers de projet et temporaires')
    preparation_generator = get_text('preparation_generator', 'Générateur Ren\'Py : Accès direct à l\'interface de gestion de projet complet')
    
    # --- Onglet Actions ---
    actions_title = get_text('actions_title', 'Onglet Actions')
    actions_workflow = get_text('actions_workflow', 'Workflow principal :')
    actions_step1_title = get_text('actions_step1_title', '1. Extraire')
    actions_step1_desc = get_text('actions_step1_desc', 'Convertit le fichier .rpy en fichier .txt éditable avec toutes les traductions à faire.')
    actions_step2_title = get_text('actions_step2_title', '2. Traduire')
    actions_step2_desc = get_text('actions_step2_desc', 'Modifiez le fichier .txt généré avec votre éditeur de texte favori.')
    actions_step3_title = get_text('actions_step3_title', '3. Reconstruire')
    actions_step3_desc = get_text('actions_step3_desc', 'Intègre vos traductions dans le fichier .rpy final du jeu.')
    actions_step4_title = get_text('actions_step4_title', '4. Vérifier')
    actions_step4_desc = get_text('actions_step4_desc', 'Analyse la cohérence technique de vos traductions.')
    actions_complementary = get_text('actions_complementary', 'Actions complémentaires :')
    actions_clean_tl = get_text('actions_clean_tl', 'Nettoyer TL : Supprime les blocs de traduction orphelins')
    actions_recheck = get_text('actions_recheck', 'Révérifier : Analyse ciblée du dernier fichier reconstruit')
    actions_batch = get_text('actions_batch', 'Actions en lot : Traitement de plusieurs fichiers simultanément')
    
    # --- Onglet Outils ---
    tools_title = get_text('tools_title', 'Onglet Outils')
    tools_quick_access = get_text('tools_quick_access', 'Accès rapide :')
    tools_folders = get_text('tools_folders', 'Dossiers : Temporaires, Sauvegardes, Rapports, Configs')
    tools_windows = get_text('tools_windows', 'Fenêtres spécialisées : Gestionnaire Sauvegardes, Vérificateur Cohérence')
    tools_configuration = get_text('tools_configuration', 'Configuration : Accès direct aux paramètres de l\'application')
    tools_integration = get_text('tools_integration', 'Intégration système :')
    tools_editors = get_text('tools_editors', 'Éditeurs externes : Ouverture automatique avec VSCode, Notepad++, etc.')
    tools_explorer = get_text('tools_explorer', 'Explorateur : Navigation directe vers les dossiers de travail')
    tools_notifications = get_text('tools_notifications', 'Notifications : Alertes système pour les opérations terminées')
    
    # --- Conseils d'utilisation ---
    tips_title = get_text('tips_title', 'Conseils d\'utilisation')
    tips_workflow_title = get_text('tips_workflow_title', 'Workflow recommandé :')
    tips_workflow_1 = get_text('tips_workflow_1', 'Préparation : Sélectionnez un fichier .rpy dans l\'onglet Préparation')
    tips_workflow_2 = get_text('tips_workflow_2', 'Extraction : Cliquez sur "Extraire" dans l\'onglet Actions')
    tips_workflow_3 = get_text('tips_workflow_3', 'Traduction : Modifiez le fichier .txt généré dans le dossier Temporaires')
    tips_workflow_4 = get_text('tips_workflow_4', 'Reconstruction : Cliquez sur "Reconstruire" pour intégrer vos traductions')
    tips_workflow_5 = get_text('tips_workflow_5', 'Vérification : Utilisez "Vérifier Cohérence" si des erreurs sont détectées')
    tips_practical_title = get_text('tips_practical_title', 'Astuces pratiques :')
    tips_drag_drop = get_text('tips_drag_drop', 'Glisser-déposer : Faites glisser un fichier .rpy n\'importe où dans l\'interface')
    tips_shortcuts = get_text('tips_shortcuts', 'Raccourcis : Les boutons d\'ouverture de dossiers évitent la navigation manuelle')
    tips_backup = get_text('tips_backup', 'Sauvegarde automatique : Chaque reconstruction crée une sauvegarde de sécurité')
    tips_colors = get_text('tips_colors', 'Codes couleur : Les boutons suivent un code couleur logique (bleu=info, vert=action positive, orange=attention)')
    
    # Génération du contenu HTML
    return f"""
        <div class="quick-nav-section" style="background: var(--card-bg); padding: 20px; margin-bottom: 30px; border-radius: 8px; border-left: 4px solid #4a90e2;">
            <h3>🧭 {quick_nav_title}</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin-top: 15px;">
                <a href="#main-preparation" class="nav-card-tab3" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">🔧 {nav_preparation}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_preparation_desc}</div>
                </a>
                <a href="#main-actions" class="nav-card-tab3" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">⚡ {nav_actions}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_actions_desc}</div>
                </a>
                <a href="#main-outils" class="nav-card-tab3" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">🛠️ {nav_outils}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_outils_desc}</div>
                </a>
            </div>
        </div>
        
        <style>
        .nav-card-tab3:hover {{
            box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
            border-color: #4a90e2 !important;
            background: linear-gradient(135deg, var(--button-bg) 0%, rgba(74, 144, 226, 0.1) 100%) !important;
        }}
        </style>
        
        <div class="section" id="main-interface">
            <h2>🖥️ {overview_title}</h2>
            <p>{overview_description}</p>
            
            <h3>📋 {overview_organization}</h3>
            <p>{overview_logic}</p>
        </div>
        
        <div class="section" id="main-preparation">
            <h3>🔧 {preparation_title}</h3>
            {generator._get_image_html("01_interface_principale", "001", language, 
                                       "Interface principale - Onglet Préparation", 
                                       "Zone de glisser-déposer active avec sélection de fichier .rpy")}
            
            <h4>{preparation_features}</h4>
            <ul>
                <li><strong>{preparation_selection}</strong></li>
                <li><strong>{preparation_validation}</strong></li>
                <li><strong>{preparation_quick_access}</strong></li>
                <li><strong>{preparation_generator}</strong></li>
            </ul>
        </div>
        
        <div class="section" id="main-actions">
            <h3>⚡ {actions_title}</h3>
            {generator._get_image_html("01_interface_principale", "002", language,
                                       "Interface principale - Onglet Actions",
                                       "Tous les boutons de traitement avec codes couleur par fonction")}
            
            <h4>{actions_workflow}</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #4a90e2;">
                    <h5>{actions_step1_title}</h5>
                    <p>{actions_step1_desc}</p>
                </div>
                
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #f59e0b;">
                    <h5>{actions_step2_title}</h5>
                    <p>{actions_step2_desc}</p>
                </div>
                
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #10b981;">
                    <h5>{actions_step3_title}</h5>
                    <p>{actions_step3_desc}</p>
                </div>
                
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #8b5cf6;">
                    <h5>{actions_step4_title}</h5>
                    <p>{actions_step4_desc}</p>
                </div>
            </div>
            
            <h4>{actions_complementary}</h4>
            <ul>
                <li><strong>{actions_clean_tl}</strong></li>
                <li><strong>{actions_recheck}</strong></li>
                <li><strong>{actions_batch}</strong></li>
            </ul>
        </div>
        
        <div class="section" id="main-outils">
            <h3>🛠️ {tools_title}</h3>
            {generator._get_image_html("01_interface_principale", "003", language,
                                       "Interface principale - Onglet Outils",
                                       "Accès rapide aux dossiers et fenêtres spécialisées")}
            
            <h4>{tools_quick_access}</h4>
            <ul>
                <li><strong>{tools_folders}</strong></li>
                <li><strong>{tools_windows}</strong></li>
                <li><strong>{tools_configuration}</strong></li>
            </ul>
            
            <h4>{tools_integration}</h4>
            <ul>
                <li><strong>{tools_editors}</strong></li>
                <li><strong>{tools_explorer}</strong></li>
                <li><strong>{tools_notifications}</strong></li>
            </ul>
        </div>
        
        <div class="section">
            <h2>💡 {tips_title}</h2>
            
            <h3>{tips_workflow_title}</h3>
            <ol>
                <li><strong>{tips_workflow_1}</strong></li>
                <li><strong>{tips_workflow_2}</strong></li>
                <li><strong>{tips_workflow_3}</strong></li>
                <li><strong>{tips_workflow_4}</strong></li>
                <li><strong>{tips_workflow_5}</strong></li>
            </ol>
            
            <h3>{tips_practical_title}</h3>
            <ul>
                <li><strong>{tips_drag_drop}</strong></li>
                <li><strong>{tips_shortcuts}</strong></li>
                <li><strong>{tips_backup}</strong></li>
                <li><strong>{tips_colors}</strong></li>
            </ul>
        </div>
    """