# ui/tutorial/content/tab_02.py
"""
Module de contenu pour l'onglet 2 : Workflow - Guide du processus de traduction
"""

import html

def generate_content(generator, language=None, translations=None):
    """Génère le contenu de l'onglet Workflow
    
    Args:
        generator: Instance du générateur avec méthodes utilitaires
        language: Code langue (fr, en, de) - optionnel
        translations: Dictionnaire des traductions - optionnel
    
    Returns:
        str: HTML généré pour l'onglet workflow
    """
    # Vérification des traductions
    if translations is None:
        translations = {}
    if not isinstance(translations, dict) or 'tabs' not in translations or 'common' not in translations:
        return "<div>Erreur : Traductions manquantes ou mal formées</div>"
    
    # Récupérer les traductions spécifiques au workflow
    section_t = translations.get('tabs', {}).get('workflow', {})
    common_t = translations.get('common', {})
    
    def get_text(key, fallback=""):
        """Récupère une traduction avec sanitisation HTML"""
        value = section_t.get(key) or common_t.get(key) or fallback
        if isinstance(value, str):
            return html.escape(value)
        elif isinstance(value, list):
            return [html.escape(item) if isinstance(item, str) else item for item in value]
        return value
    
    # --- Navigation rapide ---
    quick_nav_title = get_text('quick_nav_title', 'Navigation rapide')
    nav_overview = get_text('nav_overview', 'Vue d\'ensemble')
    nav_overview_desc = get_text('nav_overview_desc', 'Présentation des 4 composants principaux')
    nav_quickstart = get_text('nav_quickstart', 'Démarrage rapide')
    nav_quickstart_desc = get_text('nav_quickstart_desc', 'Première utilisation et usage quotidien')
    
    # --- Vue d'ensemble ---
    overview_title = get_text('overview_title', 'Vue d\'ensemble de RenExtract')
    overview_description = get_text('overview_description', 'RenExtract est un outil complet de traduction pour les jeux Ren\'Py. Ce guide vous accompagne dans la maîtrise de ses fonctionnalités, de la configuration initiale à l\'utilisation avancée.')
    
    main_interface_card = get_text('main_interface_card', 'Interface Principale')
    main_interface_desc = get_text('main_interface_desc', 'Workflow quotidien : Préparation, Actions et Outils pour traiter vos fichiers un par un.')
    
    generator_card = get_text('generator_card', 'Générateur Ren\'Py')
    generator_desc = get_text('generator_desc', 'Gestion de projet complet : extraction RPA, génération TL, polices GUI, modules français.')
    
    backup_card = get_text('backup_card', 'Gestionnaire Sauvegardes')
    backup_desc = get_text('backup_desc', 'Restauration intelligente des 4 types de sauvegardes automatiques créées par RenExtract.')
    
    tools_card = get_text('tools_card', 'Outils Spécialisés')
    tools_desc = get_text('tools_desc', 'Analyse technique : variables [], balises {{}}, codes spéciaux, lignes non traduites.')
    
    # --- Workflow de traduction ---
    workflow_title = get_text('workflow_title', 'Workflow de traduction en 3 étapes')
    
    step1_title = get_text('step1_title', 'Générateur Ren\'Py')
    step1_desc = get_text('step1_desc', 'Préparation de l\'infrastructure : Extraction des archives (.rpa) et génération de l\'arborescence tl/[langue]/ avec tous les fichiers nécessaires.')
    
    step2_title = get_text('step2_title', 'Interface Principale')
    step2_desc = get_text('step2_desc', 'Traduction fichier par fichier : Cycle Extraire → Traduire → Reconstruire.')
    
    step3_title = get_text('step3_title', 'Vérification')
    step3_desc = get_text('step3_desc', 'Contrôle qualité : Vérificateur de cohérence pour détecter les erreurs techniques avant de tester le jeu.')
    
    # --- Démarrage rapide ---
    quickstart_title = get_text('quickstart_title', 'Démarrage rapide')
    first_use_title = get_text('first_use_title', 'Première utilisation')
    # Gérer la liste des étapes de première utilisation
    first_use_steps_default = [
        'Lancez le Générateur Ren\'Py',
        'Configurez vos Paramètres',
        'Traitez avec l\'Interface Principale',
        'Vérifiez avec le Vérificateur'
    ]
    first_use_steps = get_text('first_use_steps', first_use_steps_default)
    # Extraction des éléments pour l'HTML
    first_step_1 = first_use_steps[0] if len(first_use_steps) > 0 else first_use_steps_default[0]
    first_step_2 = first_use_steps[1] if len(first_use_steps) > 1 else first_use_steps_default[1]
    first_step_3 = first_use_steps[2] if len(first_use_steps) > 2 else first_use_steps_default[2]
    first_step_4 = first_use_steps[3] if len(first_use_steps) > 3 else first_use_steps_default[3]
    
    daily_use_title = get_text('daily_use_title', 'Usage quotidien')
    # Gérer la liste des étapes d'usage quotidien
    daily_use_steps_default = [
        'Extraire un fichier .rpy → Fichier .txt généré',
        'Traduire le .txt avec votre éditeur',
        'Reconstruire → Intégration dans le jeu',
        'Vérifier si des erreurs sont détectées'
    ]
    daily_use_steps = get_text('daily_use_steps', daily_use_steps_default)
    # Extraction des éléments pour l'HTML
    daily_step_1 = daily_use_steps[0] if len(daily_use_steps) > 0 else daily_use_steps_default[0]
    daily_step_2 = daily_use_steps[1] if len(daily_use_steps) > 1 else daily_use_steps_default[1]
    daily_step_3 = daily_use_steps[2] if len(daily_use_steps) > 2 else daily_use_steps_default[2]
    daily_step_4 = daily_use_steps[3] if len(daily_use_steps) > 3 else daily_use_steps_default[3]
    
    # --- Quand utiliser quoi ? ---
    when_to_use_title = get_text('when_to_use_title', 'Quand utiliser quoi ?')
    
    generator_when_title = get_text('generator_when_title', 'Générateur Ren\'Py - Configuration initiale')
    generator_when_desc = get_text('generator_when_desc', 'Utilisez le générateur pour :')
    generator_when_list_default = [
        'Nouveau projet : Extraction complète des archives RPA et génération TL',
        'Infrastructure : Polices GUI, sélecteur de langue, modules français',
        'Textes oubliés : Éléments d\'interface non détectés par le SDK',
        'Maintenance : Nettoyage et combinaison de fichiers'
    ]
    generator_when_list = get_text('generator_when_list', generator_when_list_default)
    # Extraction des éléments pour l'HTML
    gen_item_1 = generator_when_list[0] if len(generator_when_list) > 0 else generator_when_list_default[0]
    gen_item_2 = generator_when_list[1] if len(generator_when_list) > 1 else generator_when_list_default[1]
    gen_item_3 = generator_when_list[2] if len(generator_when_list) > 2 else generator_when_list_default[2]
    gen_item_4 = generator_when_list[3] if len(generator_when_list) > 3 else generator_when_list_default[3]
    
    interface_when_title = get_text('interface_when_title', 'Interface Principale - Travail quotidien')
    interface_when_desc = get_text('interface_when_desc', 'Utilisez l\'interface principale pour :')
    interface_when_list_default = [
        'Traduction fichier par fichier : Cycle Extraire → Traduire → Reconstruire',
        'Modifications ponctuelles : Corrections rapides',
        'Actions en lot : Traitement de plusieurs fichiers similaires',
        'Vérifications : Contrôle qualité après modifications'
    ]
    interface_when_list = get_text('interface_when_list', interface_when_list_default)
    # Extraction des éléments pour l'HTML
    int_item_1 = interface_when_list[0] if len(interface_when_list) > 0 else interface_when_list_default[0]
    int_item_2 = interface_when_list[1] if len(interface_when_list) > 1 else interface_when_list_default[1]
    int_item_3 = interface_when_list[2] if len(interface_when_list) > 2 else interface_when_list_default[2]
    int_item_4 = interface_when_list[3] if len(interface_when_list) > 3 else interface_when_list_default[3]
    
    tools_when_title = get_text('tools_when_title', 'Outils Spécialisés - Maintenance avancée')
    tools_when_desc = get_text('tools_when_desc', 'Utilisez les outils spécialisés pour :')
    tools_when_list_default = [
        'Debugging : Vérificateur de cohérence en cas de problème',
        'Ajustements temps réel : Modifications pendant le jeu',
        'Nettoyage avancé : Suppression des traductions orphelines'
    ]
    tools_when_list = get_text('tools_when_list', tools_when_list_default)
    # Extraction des éléments pour l'HTML
    tool_item_1 = tools_when_list[0] if len(tools_when_list) > 0 else tools_when_list_default[0]
    tool_item_2 = tools_when_list[1] if len(tools_when_list) > 1 else tools_when_list_default[1]
    tool_item_3 = tools_when_list[2] if len(tools_when_list) > 2 else tools_when_list_default[2]
    
    # Génération du contenu HTML
    return f"""
        <div class="quick-nav-section" style="background: var(--card-bg); padding: 20px; margin-bottom: 30px; border-radius: 8px; border-left: 4px solid #4a90e2;">
            <h3>🧭 {quick_nav_title}</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; margin-top: 15px;">
                <a href="#workflow-overview" class="nav-card-tab2" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">🎯 {nav_overview}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_overview_desc}</div>
                </a>
                <a href="#quick-start" class="nav-card-tab2" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">⚡ {nav_quickstart}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_quickstart_desc}</div>
                </a>
            </div>
        </div>
        
        <style>
        .nav-card-tab2:hover {{
            box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
            border-color: #4a90e2 !important;
            background: linear-gradient(135deg, var(--button-bg) 0%, rgba(74, 144, 226, 0.1) 100%) !important;
        }}
        </style>
        
        <div class="section" id="workflow-overview">
            <h2>🎯 {overview_title}</h2>
            <p>{overview_description}</p>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <h4>{main_interface_card}</h4>
                    <p>{main_interface_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>{generator_card}</h4>
                    <p>{generator_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>{backup_card}</h4>
                    <p>{backup_desc}</p>
                </div>
                
                <div class="feature-card">
                    <h4>{tools_card}</h4>
                    <p>{tools_desc}</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🔄 {workflow_title}</h2>
            
            <div class="workflow-step" data-step="1">
                <h3>{step1_title}</h3>
                <p><strong>{step1_desc}</strong></p>
            </div>
            
            <div class="workflow-step" data-step="2">
                <h3>{step2_title}</h3>
                <p><strong>{step2_desc}</strong></p>
            </div>
            
            <div class="workflow-step" data-step="3">
                <h3>{step3_title}</h3>
                <p><strong>{step3_desc}</strong></p>
            </div>
        </div>
        
        <div class="section" id="quick-start">
            <h2>⚡ {quickstart_title}</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid #8b5cf6;">
                    <h4 id="first-use">{first_use_title}</h4>
                    <ol>
                        <li>{first_step_1}</li>
                        <li>{first_step_2}</li>
                        <li>{first_step_3}</li>
                        <li>{first_step_4}</li>
                    </ol>
                </div>
                
                <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid #10b981;">
                    <h4>{daily_use_title}</h4>
                    <ol>
                        <li>{daily_step_1}</li>
                        <li>{daily_step_2}</li>
                        <li>{daily_step_3}</li>
                        <li>{daily_step_4}</li>
                    </ol>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>❓ {when_to_use_title}</h2>
            
            <h3>{generator_when_title}</h3>
            <p>{generator_when_desc}</p>
            <ul>
                <li><strong>{gen_item_1}</strong></li>
                <li><strong>{gen_item_2}</strong></li>
                <li><strong>{gen_item_3}</strong></li>
                <li><strong>{gen_item_4}</strong></li>
            </ul>
            
            <h3>{interface_when_title}</h3>
            <p>{interface_when_desc}</p>
            <ul>
                <li><strong>{int_item_1}</strong></li>
                <li><strong>{int_item_2}</strong></li>
                <li><strong>{int_item_3}</strong></li>
                <li><strong>{int_item_4}</strong></li>
            </ul>
            
            <h3>{tools_when_title}</h3>
            <p>{tools_when_desc}</p>
            <ul>
                <li><strong>{tool_item_1}</strong></li>
                <li><strong>{tool_item_2}</strong></li>
                <li><strong>{tool_item_3}</strong></li>
            </ul>
        </div>
    """