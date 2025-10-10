# ui/tutorial/content/tab_01.py
"""
Module de contenu pour l'onglet 1 : Sommaire - Table des matières avec navigation
"""

def generate_content(generator, language, translations):
    """Génère le contenu de l'onglet Sommaire"""
    
    # Récupérer les traductions spécifiques au sommaire
    section_t = translations.get('tabs', {}).get('summary', {})
    
    def get_text(key, fallback=""):
        return section_t.get(key, fallback)
    
    # Libellés traduits
    main_title = get_text('main_title', 'Table des Matières')
    main_description = get_text('main_description', 'Guide complet de RenExtract organisé par fonctionnalités. Cliquez sur les liens pour naviguer directement vers les sections.')
    
    startup_title = get_text('startup_title', 'Démarrage')
    interface_title = get_text('interface_title', 'Interface Principale')
    generator_title = get_text('generator_title', 'Générateur Ren\'Py')
    backup_title = get_text('backup_title', 'Gestionnaire de Sauvegardes')
    tools_title = get_text('tools_title', 'Outils Spécialisés')
    settings_title = get_text('settings_title', 'Configuration')
    technical_title = get_text('technical_title', 'Techniques Avancées')
    help_title = get_text('help_title', 'Aide et Support')
    
    # Liens de navigation
    startup_overview = get_text('startup_overview', 'Vue d\'ensemble du workflow')
    startup_quick = get_text('startup_quick', 'Démarrage rapide en 4 étapes')
    startup_first = get_text('startup_first', 'Configuration première utilisation')
    
    interface_overview = get_text('interface_overview', 'Vue d\'ensemble')
    interface_preparation = get_text('interface_preparation', 'Onglet Préparation')
    interface_actions = get_text('interface_actions', 'Onglet Actions')
    interface_tools = get_text('interface_tools', 'Onglet Outils')
    
    generator_overview = get_text('generator_overview', 'Interface générale')
    generator_extraction = get_text('generator_extraction', 'Extraction & Compilation RPA/RPYC')
    generator_generation = get_text('generator_generation', 'Génération TL et polices GUI')
    generator_config = get_text('generator_config', 'Extraction Config (textes oubliés)')
    generator_results = get_text('generator_results', 'Analyse des résultats')
    generator_combination = get_text('generator_combination', 'Combinaison & Division')
    
    backup_interface = get_text('backup_interface', 'Interface complète')
    backup_statistics = get_text('backup_statistics', 'Statistiques et filtres')
    backup_restoration = get_text('backup_restoration', 'Processus de restauration')
    backup_cleanup = get_text('backup_cleanup', 'Nettoyage automatique')
    
    tools_coherence = get_text('tools_coherence', 'Vérification Cohérence')
    tools_realtime = get_text('tools_realtime', 'Éditeur Temps Réel')
    tools_cleanup = get_text('tools_cleanup', 'Nettoyage Intelligent')
    
    settings_general = get_text('settings_general', 'Paramètres généraux')
    settings_extraction = get_text('settings_extraction', 'Extraction & Protection')
    settings_colors = get_text('settings_colors', 'Personnalisation couleurs')
    settings_interface = get_text('settings_interface', 'Interface & Application')
    settings_paths = get_text('settings_paths', 'Chemins d\'accès')
    
    technical_extraction = get_text('technical_extraction', 'Système d\'extraction/reconstruction')
    technical_architecture = get_text('technical_architecture', 'Architecture des sauvegardes')
    technical_performance = get_text('technical_performance', 'Optimisation et performance')
    technical_integration = get_text('technical_integration', 'Intégration système')
    
    help_faq = get_text('help_faq', 'Questions fréquentes')
    help_troubleshooting = get_text('help_troubleshooting', 'Dépannage technique')
    help_contact = get_text('help_contact', 'Contacter l\'équipe')
    help_credits = get_text('help_credits', 'Crédits et remerciements')
    
    return f"""
        <div class="section">
            <h2>📋 {main_title}</h2>
            <p>{main_description}</p>
        </div>
        
        <div class="section">
            <h2>🚀 {startup_title}</h2>
            <ul>
                <li><button class="nav-link-btn" data-target-tab="2" data-target-section="workflow-overview">{startup_overview}</button></li>
                <li><button class="nav-link-btn" data-target-tab="2" data-target-section="quick-start">{startup_quick}</button></li>
                <li><button class="nav-link-btn" data-target-tab="2" data-target-section="first-use">{startup_first}</button></li>
            </ul>
        </div>
        
        <div class="section">
            <h2>🖥️ {interface_title}</h2>
            <ul>
                <li><button class="nav-link-btn" data-target-tab="3" data-target-section="main-interface">{interface_overview}</button></li>
                <li><button class="nav-link-btn" data-target-tab="3" data-target-section="main-preparation">{interface_preparation}</button></li>
                <li><button class="nav-link-btn" data-target-tab="3" data-target-section="main-actions">{interface_actions}</button></li>
                <li><button class="nav-link-btn" data-target-tab="3" data-target-section="main-outils">{interface_tools}</button></li>
            </ul>
        </div>
        
        <div class="section">
            <h2>🎮 {generator_title}</h2>
            <ul>
                <li><button class="nav-link-btn" data-target-tab="4" data-target-section="generator-window">{generator_overview}</button></li>
                <li><button class="nav-link-btn" data-target-tab="4" data-target-section="gen-extraction-rpa">{generator_extraction}</button></li>
                <li><button class="nav-link-btn" data-target-tab="4" data-target-section="gen-generation">{generator_generation}</button></li>
                <li><button class="nav-link-btn" data-target-tab="4" data-target-section="gen-extraction-config">{generator_config}</button></li>
                <li><button class="nav-link-btn" data-target-tab="4" data-target-section="gen-extraction-resultats">{generator_results}</button></li>
                <li><button class="nav-link-btn" data-target-tab="4" data-target-section="gen-combinaison">{generator_combination}</button></li>
            </ul>
        </div>
        
        <div class="section">
            <h2>💾 {backup_title}</h2>
            <ul>
                <li><button class="nav-link-btn" data-target-tab="6" data-target-section="backup-manager">{backup_interface}</button></li>
                <li><button class="nav-link-btn" data-target-tab="6" data-target-section="backup-statistics">{backup_statistics}</button></li>
                <li><button class="nav-link-btn" data-target-tab="6" data-target-section="backup-restoration">{backup_restoration}</button></li>
                <li><button class="nav-link-btn" data-target-tab="6" data-target-section="backup-cleanup">{backup_cleanup}</button></li>
            </ul>
        </div>
        
        <div class="section">
            <h2>🛠️ {tools_title}</h2>
            <ul>
                <li><button class="nav-link-btn" data-target-tab="5" data-target-section="verification-coherence">{tools_coherence}</button></li>
                <li><button class="nav-link-btn" data-target-tab="5" data-target-section="editeur-temps-reel">{tools_realtime}</button></li>
                <li><button class="nav-link-btn" data-target-tab="5" data-target-section="nettoyage-intelligent">{tools_cleanup}</button></li>
            </ul>
        </div>
        
        <div class="section">
            <h2>⚙️ {settings_title}</h2>
            <ul>
                <li><button class="nav-link-btn" data-target-tab="7" data-target-section="config-details">{settings_general}</button></li>
                <li><button class="nav-link-btn" data-target-tab="7" data-target-section="config-extraction">{settings_extraction}</button></li>
                <li><button class="nav-link-btn" data-target-tab="7" data-target-section="config-colors">{settings_colors}</button></li>
                <li><button class="nav-link-btn" data-target-tab="7" data-target-section="config-interface">{settings_interface}</button></li>
                <li><button class="nav-link-btn" data-target-tab="7" data-target-section="config-paths">{settings_paths}</button></li>
            </ul>
        </div>
        
        <div class="section">
            <h2>🔧 {technical_title}</h2>
            <ul>
                <li><button class="nav-link-btn" data-target-tab="8" data-target-section="tech-extraction">{technical_extraction}</button></li>
                <li><button class="nav-link-btn" data-target-tab="8" data-target-section="tech-architecture">{technical_architecture}</button></li>
                <li><button class="nav-link-btn" data-target-tab="8" data-target-section="tech-performance">{technical_performance}</button></li>
                <li><button class="nav-link-btn" data-target-tab="8" data-target-section="tech-integration">{technical_integration}</button></li>
            </ul>
        </div>
        
        <div class="section">
            <h2>❓ {help_title}</h2>
            <ul>
                <li><button class="nav-link-btn" data-target-tab="9" data-target-section="faq-section">{help_faq}</button></li>
                <li><button class="nav-link-btn" data-target-tab="9" data-target-section="troubleshooting">{help_troubleshooting}</button></li>
                <li><button class="nav-link-btn" data-target-tab="9" data-target-section="support-contact">{help_contact}</button></li>
                <li><button class="nav-link-btn" data-target-tab="9" data-target-section="credits">{help_credits}</button></li>
            </ul>
        </div>
    """