# ui/tutorial/content/tab_09.py
"""
Module de contenu pour l'onglet 9 : FAQ et Support
"""

def generate_content(generator, language, translations):
    """
    Génère le contenu pour l'onglet 9 : FAQ et Support
    
    Args:
        generator: Instance du générateur avec méthodes utilitaires
        language: Code langue (fr, en, de)
        translations: Dictionnaire des traductions
    
    Returns:
        str: HTML généré pour l'onglet FAQ et support
    """
    # Récupération des traductions pour cette section
    section_t = translations.get('tabs', {}).get('faq', {})
    common_t = translations.get('common', {})
   
    def get_text(key, fallback=""):
        return section_t.get(key) or common_t.get(key) or fallback
    
    # Définitions des textes pour la navigation rapide
    quick_nav_title = get_text('quick_nav_title', 'Navigation rapide')
    nav_faq = get_text('nav_faq', 'Questions Fréquentes')
    nav_faq_desc = get_text('nav_faq_desc', 'Réponses aux questions courantes')
    nav_troubleshooting = get_text('nav_troubleshooting', 'Dépannage')
    nav_troubleshooting_desc = get_text('nav_troubleshooting_desc', 'Solutions aux problèmes techniques')
    nav_support = get_text('nav_support', 'Support')
    nav_support_desc = get_text('nav_support_desc', 'Contact et assistance développement')
    nav_credits = get_text('nav_credits', 'Crédits')
    nav_credits_desc = get_text('nav_credits_desc', 'Équipe et remerciements')
    
    # Définitions pour la section FAQ
    faq_title = get_text('faq_title', 'Questions Fréquentes')
    faq_intro = get_text('faq_intro', 'Réponses aux questions les plus courantes sur l\'utilisation de RenExtract.')
    q1_title = get_text('q1_title', 'Interface Principale ou Générateur Ren\'Py ?')
    q1_rule = get_text('q1_rule', 'Règle simple :')
    q1_interface = get_text('q1_interface', 'Interface Principale pour traiter un fichier spécifique (.rpy → .txt → .rpy)')
    q1_generator = get_text('q1_generator', 'Générateur Ren\'Py pour configurer l\'infrastructure complète du projet')
    q2_title = get_text('q2_title', 'Le jeu plante après ma traduction !')
    q2_solution = get_text('q2_solution', 'Solution : Utilisez le Vérificateur de Cohérence. Le rapport HTML vous indiquera exactement la ligne problématique.')
    q3_title = get_text('q3_title', 'Où sont les fichiers à traduire ?')
    q3_answer = get_text('q3_answer', 'Dans le dossier 01_Temporaires après une extraction. Utilisez Interface Principale → Outils → Ouvrir Dossier Temporaires pour y accéder rapidement.')
    q4_title = get_text('q4_title', 'Comment récupérer un fichier cassé ?')
    q4_answer = get_text('q4_answer', 'Utilisez le Gestionnaire de Sauvegardes → Filtrez par le jeu concerné → Type "Sécurité" → Restaurez la dernière version fonctionnelle.')
    q5_title = get_text('q5_title', 'Mes polices ne s\'affichent pas ?')
    q5_answer = get_text('q5_answer', 'Dans le Générateur Ren\'Py → Génération → Testez d\'abord dans l\'aperçu des polices → Sélectionnez uniquement les polices marquées comme "disponibles".')
    q6_title = get_text('q6_title', 'Comment utiliser l\'Éditeur Temps Réel ?')
    q6_answer = get_text('q6_answer', 'Outils Spécialisés → Éditeur Temps Réel → Installez le module → Lancez le jeu → Appuyez sur F8 pour modifier les dialogues en direct.')
    quick_tips_title = get_text('quick_tips_title', 'Conseils rapides')
    tip1 = get_text('tip1', 'Sauvegardez toujours le jeu original avant modification')
    tip2 = get_text('tip2', 'Utilisez le Vérificateur de Cohérence après chaque traduction')
    tip3 = get_text('tip3', 'Consultez les rapports dans 03_Rapports en cas d\'erreur')
    tip4 = get_text('tip4', 'Gardez vos paramètres d\'exclusion pour éviter les faux positifs')
    
    # Définitions pour la section Dépannage
    troubleshooting_title = get_text('troubleshooting_title', 'Dépannage Technique')
    troubleshooting_intro = get_text('troubleshooting_intro', 'Solutions aux problèmes techniques les plus courants rencontrés lors de l\'utilisation.')
    error1_title = get_text('error1_title', '"Aucun texte trouvé"')
    error1_causes = get_text('error1_causes', 'Causes possibles :')
    error1_cause1 = get_text('error1_cause1', 'Fichier .rpyc sélectionné au lieu de .rpy')
    error1_cause2 = get_text('error1_cause2', 'Fichier ne contenant que du code (pas de dialogue)')
    error1_cause3 = get_text('error1_cause3', 'Fichier déjà entièrement traduit')
    error1_solutions = get_text('error1_solutions', 'Solutions :')
    error1_solution1 = get_text('error1_solution1', 'Vérifiez l\'extension : doit être .rpy (pas .rpyc)')
    error1_solution2 = get_text('error1_solution2', 'Utilisez Générateur → Extraction Config pour les textes d\'interface')
    error1_solution3 = get_text('error1_solution3', 'Testez avec un autre fichier du même jeu')
    error2_title = get_text('error2_title', '"Échec de validation"')
    error2_diagnostic = get_text('error2_diagnostic', 'Diagnostic :')
    error2_diag1 = get_text('error2_diag1', 'Consultez le rapport détaillé dans 03_Rapports')
    error2_diag2 = get_text('error2_diag2', 'Utilisez le Vérificateur de Cohérence pour localiser les erreurs')
    error2_corrections = get_text('error2_corrections', 'Corrections courantes :')
    error2_corr1 = get_text('error2_corr1', 'Variables [] : vérifiez que toutes les variables sont conservées')
    error2_corr2 = get_text('error2_corr2', 'Balises {{}} : assurez-vous que toutes les balises sont fermées')
    error2_corr3 = get_text('error2_corr3', 'Codes spéciaux : ne modifiez pas les \\n, --, % etc.')
    error2_fallback = get_text('error2_fallback', 'Solution de secours :')
    error2_fallback_desc = get_text('error2_fallback_desc', 'Restaurez une version valide depuis le Gestionnaire de Sauvegardes')
    error3_title = get_text('error3_title', '"L\'extraction est très lente"')
    perf_antivirus_title = get_text('perf_antivirus_title', 'Antivirus')
    error3_antivirus = get_text('error3_antivirus', 'Ajoutez RenExtract aux exclusions de votre antivirus')
    perf_storage_title = get_text('perf_storage_title', 'Stockage')
    error3_storage = get_text('error3_storage', 'Utilisez un SSD si possible pour améliorer les performances')
    perf_space_title = get_text('perf_space_title', 'Espace disque')
    error3_space = get_text('error3_space', 'Libérez de l\'espace (prévoyez 2-3x la taille du jeu)')
    error4_title = get_text('error4_title', '"Erreur d\'accès fichier"')
    error4_close = get_text('error4_close', 'Fermez le jeu Ren\'Py s\'il est en cours d\'exécution')
    error4_admin = get_text('error4_admin', 'Lancez RenExtract en tant qu\'administrateur')
    error4_editor = get_text('error4_editor', 'Vérifiez que le fichier n\'est pas ouvert dans un éditeur')
    error4_readonly = get_text('error4_readonly', 'Vérifiez que les fichiers ne sont pas en lecture seule')
    error5_title = get_text('error5_title', 'Problèmes de compatibilité')
    compat_renpy_title = get_text('compat_renpy_title', 'Versions Ren\'Py :')
    compat_renpy_old = get_text('compat_renpy_old', 'Ren\'Py 6.x : Support limité, utilisez les fonctions de base')
    compat_renpy_7 = get_text('compat_renpy_7', 'Ren\'Py 7.x : Support complet recommandé')
    compat_renpy_8 = get_text('compat_renpy_8', 'Ren\'Py 8.x : Support complet avec nouvelles fonctionnalités')
    compat_os_title = get_text('compat_os_title', 'Systèmes d\'exploitation :')
    compat_windows = get_text('compat_windows', 'Windows 10/11 : Support optimal')
    compat_older = get_text('compat_older', 'Versions antérieures : Fonctionnalités limitées possibles')
    diagnostic_title = get_text('diagnostic_title', 'Diagnostic avancé')
    diagnostic_desc = get_text('diagnostic_desc', 'Si les problèmes persistent :')
    diagnostic_logs = get_text('diagnostic_logs', 'Consultez les logs :')
    diagnostic_logs_desc = get_text('diagnostic_logs_desc', 'Dossier 03_Rapports contient les logs détaillés')
    diagnostic_version = get_text('diagnostic_version', 'Vérifiez la version :')
    diagnostic_version_desc = get_text('diagnostic_version_desc', 'Assurez-vous d\'avoir la dernière version de RenExtract')
    diagnostic_minimal = get_text('diagnostic_minimal', 'Test minimal :')
    diagnostic_minimal_desc = get_text('diagnostic_minimal_desc', 'Testez avec un petit fichier .rpy simple')
    
    # Définitions pour la section Support
    contact_title = get_text('contact_title', 'Contacter l\'équipe de développement')
    contact_intro = get_text('contact_intro', 'Plusieurs moyens pour obtenir de l\'aide et contacter l\'équipe de développement.')
    support_title = get_text('support_title', 'Support et assistance')
    contact_email_title = get_text('contact_email_title', 'Email')
    contact_email_desc = get_text('contact_email_desc', 'Pour les questions détaillées et le support technique')
    contact_email_note = get_text('contact_email_note', 'Idéal pour les problèmes complexes nécessitant des captures d\'écran')
    contact_discord_title = get_text('contact_discord_title', 'Discord (Recommandé)')
    contact_discord_desc = get_text('contact_discord_desc', 'Communauté active, support rapide et discussions')
    contact_discord_note = get_text('contact_discord_note', 'Réponse la plus rapide, entraide communautaire')
    contact_github_title = get_text('contact_github_title', 'Signaler un bug')
    contact_github_desc = get_text('contact_github_desc', 'Rapportez les bugs et demandez des fonctionnalités')
    contact_github_note = get_text('contact_github_note', 'Uniquement pour les bugs confirmés et reproductibles')
    contact_releases_title = get_text('contact_releases_title', 'Dernière version')
    contact_releases_desc = get_text('contact_releases_desc', 'Toujours avoir la version la plus récente')
    contact_releases_note = get_text('contact_releases_note', 'Vérifiez régulièrement les mises à jour')
    help_tips_title = get_text('help_tips_title', 'Conseils pour obtenir de l\'aide')
    help_tip_1 = get_text('help_tip_1', 'Discord est le moyen le plus rapide pour obtenir de l\'aide')
    help_tip_2 = get_text('help_tip_2', 'Email pour les questions complexes nécessitant des captures d\'écran')
    help_tip_3 = get_text('help_tip_3', 'GitHub Issues uniquement pour les bugs confirmés et reproductibles')
    help_tip_4 = get_text('help_tip_4', 'Précisez toujours votre version de RenExtract et votre système d\'exploitation')
    help_tip_5 = get_text('help_tip_5', 'Joignez les logs du dossier 03_Rapports si possible')
    report_template_title = get_text('report_template_title', 'Template de rapport de bug')
    template_title = get_text('template_title', 'Titre :')
    template_title_example = get_text('template_title_example', 'Description courte du problème')
    template_version = get_text('template_version', 'Version RenExtract :')
    template_os = get_text('template_os', 'Système :')
    template_renpy = get_text('template_renpy', 'Version Ren\'Py :')
    template_steps = get_text('template_steps', 'Étapes pour reproduire :')
    template_step1 = get_text('template_step1', 'Action effectuée')
    template_step2 = get_text('template_step2', 'Résultat obtenu')
    template_step3 = get_text('template_step3', 'Comportement attendu')
    template_files = get_text('template_files', 'Fichiers joints :')
    template_files_note = get_text('template_files_note', 'logs, captures d\'écran si pertinent')
    
    # Définitions pour la section Crédits
    credits_title = get_text('credits_title', 'Crédits et remerciements')
    credits_intro = get_text('credits_intro', 'RenExtract est le fruit d\'un travail collaboratif et de contributions précieuses.')
    team_title = get_text('team_title', 'Équipe de développement')
    dev_main_title = get_text('dev_main_title', 'Développement principal')
    dev_main_name = get_text('dev_main_name', 'Rory-Mercury-91')
    dev_main_desc = get_text('dev_main_desc', 'Concepteur et développeur principal de RenExtract')
    dev_generator_title = get_text('dev_generator_title', 'Générateur Ren\'Py')
    dev_generator_name = get_text('dev_generator_name', 'Virusf')
    dev_generator_desc = get_text('dev_generator_desc', 'Contribution majeure pour une grosse partie du générateur (base du code)')
    dev_editor_title = get_text('dev_editor_title', 'Éditeur Temps Réel')
    dev_editor_name = get_text('dev_editor_name', 'Andric31')
    dev_editor_desc = get_text('dev_editor_desc', 'Idée originale et base de code pour l\'éditeur en temps réel')
    dev_community_title = get_text('dev_community_title', 'Communauté')
    dev_community_name = get_text('dev_community_name', 'Tous les utilisateurs')
    dev_community_desc = get_text('dev_community_desc', 'Retours précieux, tests et suggestions d\'amélioration')
    links_title = get_text('links_title', 'Liens utiles')
    github_repo_title = get_text('github_repo_title', 'Dépôt GitHub')
    documentation_title = get_text('documentation_title', 'Documentation')
    renpy_official_title = get_text('renpy_official_title', 'Ren\'Py Officiel')
    opensource_title = get_text('opensource_title', 'Projet open source')
    opensource_desc = get_text('opensource_desc', 'RenExtract est un projet open source disponible sur GitHub. Les contributions, suggestions et rapports de bugs sont les bienvenus !')
    contribute_title = get_text('contribute_title', 'Comment contribuer :')
    contribute_1 = get_text('contribute_1', 'Signalez les bugs via GitHub Issues')
    contribute_2 = get_text('contribute_2', 'Proposez des améliorations sur Discord')
    contribute_3 = get_text('contribute_3', 'Partagez vos retours d\'expérience')
    contribute_4 = get_text('contribute_4', 'Aidez d\'autres utilisateurs sur la communauté')
    thanks_quote = get_text('thanks_quote', '"Merci à tous ceux qui contribuent à faire de RenExtract un outil toujours meilleur pour la communauté de traduction Ren\'Py !"')
    team_signature = get_text('team_signature', 'L\'équipe RenExtract')
    
    return f"""
        <div class="quick-nav-section" style="background: var(--card-bg); padding: 20px; margin-bottom: 30px; border-radius: 8px; border-left: 4px solid #4a90e2;">
            <h3>🧭 {quick_nav_title}</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin-top: 15px;">
                <a href="#faq-section" class="nav-card-tab9" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">❓ {nav_faq}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_faq_desc}</div>
                </a>
                <a href="#troubleshooting" class="nav-card-tab9" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">🔧 {nav_troubleshooting}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_troubleshooting_desc}</div>
                </a>
                <a href="#support-contact" class="nav-card-tab9" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">📧 {nav_support}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_support_desc}</div>
                </a>
                <a href="#credits" class="nav-card-tab9" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px;">🏆 {nav_credits}</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">{nav_credits_desc}</div>
                </a>
            </div>
        </div>
        
        <style>
        .nav-card-tab9:hover {{
            box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
            border-color: #4a90e2 !important;
            background: linear-gradient(135deg, var(--button-bg) 0%, rgba(74, 144, 226, 0.1) 100%) !important;
        }}
        </style>
        
        <div class="section" id="faq-section">
        <h2>❓ {faq_title}</h2>
        <p>{faq_intro}</p>
        
        <div class="feature-grid">
            <div class="feature-card">
                <h4>{q1_title}</h4>
                <p><strong>{q1_rule}</strong></p>
                <ul>
                    <li><strong>{q1_interface}</strong></li>
                    <li><strong>{q1_generator}</strong></li>
                </ul>
            </div>
            
            <div class="feature-card">
                <h4>{q2_title}</h4>
                <p><strong>{q2_solution}</strong></p>
            </div>
            
            <div class="feature-card">
                <h4>{q3_title}</h4>
                <p>{q3_answer}</p>
            </div>
            
            <div class="feature-card">
                <h4>{q4_title}</h4>
                <p>{q4_answer}</p>
            </div>
            
            <div class="feature-card">
                <h4>{q5_title}</h4>
                <p>{q5_answer}</p>
            </div>
            
            <div class="feature-card">
                <h4>{q6_title}</h4>
                <p>{q6_answer}</p>
            </div>
        </div>
        
        <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #10b981; margin: 20px 0;">
            <h4>💡 {quick_tips_title}</h4>
            <ul>
                <li><strong>{tip1}</strong></li>
                <li><strong>{tip2}</strong></li>
                <li><strong>{tip3}</strong></li>
                <li><strong>{tip4}</strong></li>
            </ul>
        </div>
    </div>
    
    <div class="section" id="troubleshooting">
        <h2>🔧 {troubleshooting_title}</h2>
        <p>{troubleshooting_intro}</p>
        
        <h3>⚠️ {error1_title}</h3>
        <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #f59e0b; margin: 15px 0;">
            <h4>{error1_causes}</h4>
            <ul>
                <li>{error1_cause1}</li>
                <li>{error1_cause2}</li>
                <li>{error1_cause3}</li>
            </ul>
            <h4>{error1_solutions}</h4>
            <ul>
                <li>{error1_solution1}</li>
                <li>{error1_solution2}</li>
                <li>{error1_solution3}</li>
            </ul>
        </div>
        
        <h3>❌ {error2_title}</h3>
        <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #ef4444; margin: 15px 0;">
            <h4>{error2_diagnostic}</h4>
            <ul>
                <li>{error2_diag1}</li>
                <li>{error2_diag2}</li>
            </ul>
            <h4>{error2_corrections}</h4>
            <ul>
                <li>{error2_corr1}</li>
                <li>{error2_corr2}</li>
                <li>{error2_corr3}</li>
            </ul>
            <h4>{error2_fallback}</h4>
            <ul>
                <li>{error2_fallback_desc}</li>
            </ul>
        </div>
        
        <h3>🐌 {error3_title}</h3>
        <div class="feature-grid">
            <div class="feature-card">
                <h5>🛡️ {perf_antivirus_title}</h5>
                <p>{error3_antivirus}</p>
            </div>
            
            <div class="feature-card">
                <h5>💾 {perf_storage_title}</h5>
                <p>{error3_storage}</p>
            </div>
            
            <div class="feature-card">
                <h5>📁 {perf_space_title}</h5>
                <p>{error3_space}</p>
            </div>
        </div>
        
        <h3>🔒 {error4_title}</h3>
        <ul>
            <li>{error4_close}</li>
            <li>{error4_admin}</li>
            <li>{error4_editor}</li>
            <li>{error4_readonly}</li>
        </ul>
        
        <h3>🚨 {error5_title}</h3>
        <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #8b5cf6; margin: 15px 0;">
            <h4>{compat_renpy_title}</h4>
            <ul>
                <li>{compat_renpy_old}</li>
                <li>{compat_renpy_7}</li>
                <li>{compat_renpy_8}</li>
            </ul>
            <h4>{compat_os_title}</h4>
            <ul>
                <li>{compat_windows}</li>
                <li>{compat_older}</li>
            </ul>
        </div>
        
        <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #4a90e2; margin: 20px 0;">
            <h4>🔍 {diagnostic_title}</h4>
            <p>{diagnostic_desc}</p>
            <ul>
                <li><strong>{diagnostic_logs}</strong> {diagnostic_logs_desc}</li>
                <li><strong>{diagnostic_version}</strong> {diagnostic_version_desc}</li>
                <li><strong>{diagnostic_minimal}</strong> {diagnostic_minimal_desc}</li>
            </ul>
        </div>
    </div>
    
    <div class="section" id="support-contact">
        <h2>📧 {contact_title}</h2>
        <p>{contact_intro}</p>
        
        <h3>{support_title}</h3>
        <div class="feature-grid">
            <div class="feature-card">
                <h4>📧 {contact_email_title}</h4>
                <p><strong><a href="mailto:RenExtract@pm.me" style="color: var(--accent);">RenExtract@pm.me</a></strong></p>
                <p>{contact_email_desc}</p>
                <p><em>{contact_email_note}</em></p>
            </div>

            <div class="feature-card">
                <h4>🎮 {contact_discord_title}</h4>
                <p><strong><a href="https://discord.gg/Yp2Hm8JWQ2" target="_blank" style="color: var(--accent);">Rejoindre le serveur</a></strong></p>
                <p>{contact_discord_desc}</p>
                <p><em>{contact_discord_note}</em></p>
            </div>                

            <div class="feature-card">
                <h4>🛠 {contact_github_title}</h4>
                <p><strong><a href="https://github.com/Rory-Mercury-91/RenExtract/issues" target="_blank" style="color: var(--accent);">GitHub Issues</a></strong></p>
                <p>{contact_github_desc}</p>
                <p><em>{contact_github_note}</em></p>
            </div>
            
            <div class="feature-card">
                <h4>📦 {contact_releases_title}</h4>
                <p><strong><a href="https://github.com/Rory-Mercury-91/RenExtract/releases" target="_blank" style="color: var(--accent);">Téléchargements</a></strong></p>
                <p>{contact_releases_desc}</p>
                <p><em>{contact_releases_note}</em></p>
            </div>
        </div>
        
        <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #10b981; margin: 20px 0;">
            <h4>💡 {help_tips_title}</h4>
            <ul>
                <li><strong>{help_tip_1}</strong></li>
                <li><strong>{help_tip_2}</strong></li>
                <li><strong>{help_tip_3}</strong></li>
                <li>{help_tip_4}</li>
                <li>{help_tip_5}</li>
            </ul>
        </div>
        
        <h3>📋 {report_template_title}</h3>
        <div style="background: var(--sep); padding: 15px; border-radius: 8px; font-family: monospace; font-size: 0.9em;">
            <strong>{template_title}</strong> [BUG] {template_title_example}<br>
            <br>
            <strong>{template_version}</strong> [Ex: v2.1.0]<br>
            <strong>{template_os}</strong> [Ex: Windows 11]<br>
            <strong>{template_renpy}</strong> [Ex: 8.1.1]<br>
            <br>
            <strong>{template_steps}</strong><br>
            1. {template_step1}<br>
            2. {template_step2}<br>
            3. {template_step3}<br>
            <br>
            <strong>{template_files}</strong> {template_files_note}
        </div>
    </div>
    
    <div class="section" id="credits">
        <h2>🏆 {credits_title}</h2>
        <p>{credits_intro}</p>
        
        <h3>{team_title}</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin: 20px 0;">
            <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid #8b5cf6;">
                <h4>👨‍💻 {dev_main_title}</h4>
                <p><strong>{dev_main_name}</strong></p>
                <p>{dev_main_desc}</p>
            </div>
            
            <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid #4a90e2;">
                <h4>🎮 {dev_generator_title}</h4>
                <p><strong>{dev_generator_name}</strong></p>
                <p>{dev_generator_desc}</p>
            </div>
            
            <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid #10b981;">
                <h4>⚡ {dev_editor_title}</h4>
                <p><strong>{dev_editor_name}</strong></p>
                <p>{dev_editor_desc}</p>
            </div>
            
            <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid #f59e0b;">
                <h4>🌟 {dev_community_title}</h4>
                <p><strong>{dev_community_name}</strong></p>
                <p>{dev_community_desc}</p>
            </div>
        </div>
        
        <h3>🔗 {links_title}</h3>
        <div class="feature-grid">
            <div class="feature-card">
                <h4>📂 {github_repo_title}</h4>
                <p><a href="https://github.com/Rory-Mercury-91/RenExtract" target="_blank" style="color: var(--accent);">Code source complet</a></p>
            </div>
            
            <div class="feature-card">
                <h4>📋 {documentation_title}</h4>
                <p><a href="https://github.com/Rory-Mercury-91/RenExtract/wiki" target="_blank" style="color: var(--accent);">Wiki et guides</a></p>
            </div>
            
            <div class="feature-card">
                <h4>🎮 {renpy_official_title}</h4>
                <p><a href="https://www.renpy.org/" target="_blank" style="color: var(--accent);">Site officiel Ren\'Py</a></p>
            </div>
        </div>
        
        <h3>{opensource_title}</h3>
        <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid #10b981; margin: 15px 0;">
            <p>{opensource_desc}</p>
            <p><strong>{contribute_title}</strong></p>
            <ul>
                <li>{contribute_1}</li>
                <li>{contribute_2}</li>
                <li>{contribute_3}</li>
                <li>{contribute_4}</li>
            </ul>
        </div>
        
        <div style="text-align: center; margin-top: 30px; padding: 20px; background: var(--hdr); border-radius: 8px;">
            <p style="font-style: italic; opacity: 0.9; font-size: 1.1em;">
                {thanks_quote}
            </p>
            <p style="margin-top: 10px; opacity: 0.7;">
                — {team_signature}
            </p>
        </div>
    </div>
    """