# ui/tutorial/content/tab_09.py
"""
Module de contenu pour l'onglet 9 : FAQ et Support
Contenu en français pur, sans système multilingue.
"""

def generate_content(generator, language=None, translations=None):
    """
    Génère le contenu pour l'onglet 9 : FAQ et Support
    
    Args:
        generator: Instance du générateur avec méthodes utilitaires
        language: Code langue (non utilisé - français uniquement)
        translations: Dictionnaire des traductions (non utilisé - français uniquement)
    
    Returns:
        str: HTML généré pour l'onglet FAQ et support
    """
    
    return f"""
        <!-- Navigation rapide -->
        <div class="quick-nav-section" style="background: var(--card-bg); padding: 20px; margin-bottom: 30px; border-radius: 8px; border-left: 4px solid var(--accent);">
            <h3>🧭 Navigation rapide</h3>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-top: 15px;">
                <a href="#faq-section" class="nav-card-tab9" style="display: block; padding: 15px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease;">
                    <div style="font-weight: bold; margin-bottom: 4px; font-size: 1.1em;">❓ Questions Fréquentes</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Réponses aux questions courantes</div>
                </a>
                <a href="#troubleshooting" class="nav-card-tab9" style="display: block; padding: 15px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease;">
                    <div style="font-weight: bold; margin-bottom: 4px; font-size: 1.1em;">🔧 Dépannage</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Solutions aux problèmes techniques</div>
                </a>
                <a href="#support-contact" class="nav-card-tab9" style="display: block; padding: 15px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease;">
                    <div style="font-weight: bold; margin-bottom: 4px; font-size: 1.1em;">📧 Support</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Contact et assistance</div>
                </a>
                <a href="#credits" class="nav-card-tab9" style="display: block; padding: 15px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease;">
                    <div style="font-weight: bold; margin-bottom: 4px; font-size: 1.1em;">🏆 Crédits</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Équipe et remerciements</div>
                </a>
            </div>
        </div>
        
        <style>
        .nav-card-tab9:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
            border-color: var(--accent) !important;
            background: linear-gradient(135deg, var(--button-bg) 0%, rgba(74, 144, 226, 0.1) 100%) !important;
        }}
        </style>
        
        <!-- ============================================================ -->
        <!-- SECTION 1 : QUESTIONS FRÉQUENTES -->
        <!-- ============================================================ -->
        
        <div class="section" id="faq-section">
            <h2>❓ Questions Fréquentes</h2>
            <p>Réponses aux questions les plus courantes sur l'utilisation de RenExtract.</p>
            
            <div style="margin-top: 20px;">
                
                <!-- Question 1 -->
                <h4>🎯 Quelle différence entre les différentes interfaces ?</h4>
                <ul style="margin-left: 40px;">
                    <li><strong>Générateur Ren'Py</strong> : pour configurer l'infrastructure complète du projet</li>
                    <li><strong>Interface Principale</strong> : pour traduire les fichiers (.rpy → .txt → .rpy)</li>
                    <li><strong>Outils spécialisés</strong> : pour améliorer les fichiers de traduction</li>
                </ul>
                
                <!-- Question 2 -->
                <h4>💥 Le jeu plante après ma traduction !</h4>
                <p><strong>Solutions :</strong> Analysez le fichier <code>traceback.txt</code> ou <code>error.txt</code> présent dans le répertoire racine du jeu pour comprendre le problème. Vous pouvez aussi utiliser le <strong>Vérificateur de Cohérence</strong> dans Outils Spécialisés.</p>
                <p>Le rapport HTML pourra vous montrer peut-être la ligne problématique et le type d'erreur (variable manquante, balise mal fermée, etc.).</p>
                
                <!-- Question 3 -->
                <h4>📁 Où sont mes fichiers à traduire ?</h4>
                <p>Dans le dossier <code>01_Temporaires</code> après une extraction.</p>
                <p><strong>Accès rapide :</strong> Interface Principale → Onglet <strong>OUTILS</strong> → <strong>📂 Temporaires</strong>.</p>
                
                <!-- Question 4 -->
                <h4>🔄 Comment récupérer un fichier cassé ?</h4>
                <p><strong>Gestionnaire de Sauvegardes</strong> :</p>
                <ol style="margin-left: 40px;">
                    <li>Ouvrez le gestionnaire (Interface Principale → OUTILS)</li>
                    <li>Filtrez par le jeu concerné</li>
                    <li>Sélectionnez le <strong>Type</strong></li>
                    <li>Restaurez la dernière version fonctionnelle</li>
                </ol>
                
                <!-- Question 5 -->
                <h4>🔤 Les caractères français accentués ne s'affichent pas en jeu ?</h4>
                <p>Dans <strong>Générateur Ren'Py</strong> :</p>
                <ol style="margin-left: 40px;">
                    <li>Allez dans l'onglet <strong>Génération</strong></li>
                    <li>Testez d'abord dans l'<strong>aperçu des polices</strong></li>
                    <li>Sélectionnez <strong>uniquement</strong> les polices marquées comme "disponibles"</li>
                </ol>
                
                <!-- Question 6 -->
                <h4>⚡ Comment utiliser l'Éditeur Temps Réel ?</h4>
                <p><strong>Étapes :</strong></p>
                <ol style="margin-left: 40px;">
                    <li>Outils Spécialisés → <strong>Éditeur Temps Réel</strong></li>
                    <li>Installez le module dans votre jeu</li>
                    <li>Lancez le jeu</li>
                    <li>Consultez le <strong>tutoriel complet</strong> (Onglet Outils) pour toutes les fonctionnalités</li>
                </ol>
                
                <!-- Question 7 -->
                <h4>🛡️ Pourquoi certains fichiers sont automatiquement exclus ?</h4>
                <p><strong>Fichiers système protégés :</strong></p>
                <ul style="margin-left: 40px;">
                    <li><code>common.rpy</code> (Ren'Py)</li>
                    <li><code>99_Z_Console.rpy</code> (RenExtract)</li>
                    <li><code>99_Z_ScreenPreferences.rpy</code> (RenExtract)</li>
                    <li><code>99_Z_FontSystem.rpy</code> (RenExtract)</li>
                </ul>
                <p>Protection contre la suppression accidentelle lors du nettoyage.</p>
                
                <!-- Question 8 -->
                <h4>🧹 Comment nettoyer un gros projet avec plusieurs langues ?</h4>
                <p><strong>Nettoyage Intelligent</strong> :</p>
                <ol style="margin-left: 40px;">
                    <li>Outils Spécialisés → <strong>Nettoyage Intelligent</strong></li>
                    <li>Sélectionnez votre projet multi-langues</li>
                    <li>Choisissez les langues à nettoyer (sélection multiple)</li>
                    <li>Lancez le nettoyage → rapport HTML détaillé automatique</li>
                </ol>
                
                <!-- Question 9 -->
                <h4>💾 Quelle est la différence entre les 6 types de sauvegardes ?</h4>
                <ul style="margin-left: 40px;">
                    <li><strong>Sécurité</strong> : avant extraction (conservée indéfiniment)</li>
                    <li><strong>Nettoyage</strong> : avant nettoyage projet (conservée indéfiniment)</li>
                    <li><strong>Avant RPA</strong> : avant compilation RPA (conservée indéfiniment)</li>
                    <li><strong>Avant combinaison</strong> : avant fusion de fichiers (conservée indéfiniment)</li>
                    <li><strong>Modification cohérence</strong> : avant modification depuis le rapport de cohérence HTML (conservée indéfiniment)</li>
                    <li><strong>Édition temps réel</strong> : modifications en direct (max 10 fichiers, rotation automatique)</li>
                </ul>
                
                <!-- Question 10 -->
                <h4>🎨 Comment personnaliser les patterns de protection ?</h4>
                <p><strong>Paramètres → Patterns de protection</strong> :</p>
                <ol style="margin-left: 40px;">
                    <li>Configurez vos patterns personnalisés (Astérisques, Tildes)</li>
                    <li>Testez-les avec le <strong>générateur de placeholders</strong></li>
                    <li>Utilisez le <strong>suffixe numérique</strong> recommandé pour éviter les conflits</li>
                </ol>
                
            </div>
            
            <!-- Conseils rapides -->
            <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%); padding: 20px; border-radius: 8px; border-left: 4px solid #10b981; margin-top: 30px;">
                <h4>💡 Conseils rapides</h4>
                <ul style="margin: 10px 0; padding-left: 40px;">
                    <li><strong>Sauvegardez toujours le jeu original</strong> avant toute modification</li>
                    <li><strong>Consultez les logs</strong> dans le dossier <code>05_ConfigRenExtract</code> en cas d'erreur</li>
                    <li><strong>Gardez vos paramètres d'exclusion</strong> pour éviter les faux positifs lors des vérifications</li>
                </ul>
            </div>
        </div>
        
        <!-- ============================================================ -->
        <!-- SECTION 2 : DÉPANNAGE TECHNIQUE -->
        <!-- ============================================================ -->
        
        <div class="section" id="troubleshooting">
            <h2>🔧 Dépannage Technique</h2>
            <p>Solutions aux problèmes techniques les plus courants rencontrés lors de l'utilisation de RenExtract.</p>
            
            <!-- Problème 1 -->
            <h3>⚠️ "Aucun texte trouvé"</h3>
            <h4>Causes possibles :</h4>
            <ul style="margin-left: 40px;">
                <li>Archives <code>.rpa</code> ou <code>.rpyc</code> non décompilées</li>
                <li>Fichier ne contenant que du code (pas de dialogue)</li>
            </ul>
            <h4>Solutions :</h4>
            <ul style="margin-left: 40px;">
                <li><strong>Décompiler :</strong> Les archives <code>.rpa</code> et <code>.rpyc</code> doivent être décompilées</li>
                <li><strong>Utiliser Générateur → Extraction Config</strong> pour les textes oubliés</li>
                <li><strong>Tenter avec le SDK officiel</strong> (Paramètres → SDK Ren'Py)</li>
                <li><strong>Tester avec un autre fichier</strong> du même jeu</li>
            </ul>
            
            <!-- Problème 2 -->
            <h3>🐌 "L'extraction est très lente"</h3>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 15px 0;">
                <div>
                    <h5>🛡️ Antivirus</h5>
                    <p>Ajoutez RenExtract aux <strong>exclusions de votre antivirus</strong>. L'analyse en temps réel peut considérablement ralentir le traitement.</p>
                </div>
                
                <div>
                    <h5>💾 Stockage</h5>
                    <p>Utilisez un <strong>SSD</strong> si possible pour améliorer les performances d'écriture/lecture.</p>
                </div>
                
                <div>
                    <h5>📁 Espace disque</h5>
                    <p>Assurez-vous que votre <strong>disque n'est pas plein</strong> et dispose d'espace suffisant.</p>
                </div>
            </div>
            
            <!-- Problème 3 -->
            <h3>🔒 "Erreur d'accès fichier"</h3>
            <ul style="margin-left: 40px;">
                <li><strong>Fermez le jeu Ren'Py</strong> s'il est en cours d'exécution</li>
                <li><strong>Lancez RenExtract en administrateur</strong> (clic droit → Exécuter en tant qu'administrateur)</li>
                <li><strong>Vérifiez que le fichier n'est pas ouvert</strong> dans un éditeur de texte</li>
                <li><strong>Vérifiez les propriétés du fichier</strong> : il ne doit pas être en lecture seule</li>
            </ul>
            
            <!-- Problème 4 et diagnostic côte à côte -->
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 20px 0;">
                <!-- Problème 4 -->
                <div>
                    <h3>🚨 Problèmes de compatibilité</h3>
                    <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid #8b5cf6;">
                        <h4>Versions Ren'Py :</h4>
                        <ul>
                            <li><strong>Ren'Py 6.x :</strong> Support limité, utilisez les fonctions de base</li>
                            <li><strong>Ren'Py 7.x :</strong> Support complet recommandé ✅</li>
                            <li><strong>Ren'Py 8.x :</strong> Support complet avec nouvelles fonctionnalités ✅</li>
                        </ul>
                        <h4>Systèmes d'exploitation :</h4>
                        <ul>
                            <li><strong>Windows 10/11 :</strong> Support optimal ✅</li>
                            <li><strong>Versions antérieures :</strong> Fonctionnalités limitées possibles</li>
                        </ul>
                    </div>
                </div>
                
                <!-- Diagnostic avancé -->
                <div>
                    <h3>🔍 Diagnostic avancé</h3>
                    <div style="background: linear-gradient(135deg, rgba(74, 144, 226, 0.1) 0%, rgba(74, 144, 226, 0.05) 100%); padding: 20px; border-radius: 8px; border-left: 4px solid var(--accent);">
                        <p>Si les problèmes persistent :</p>
                        <ul>
                            <li><strong>Vérifier la source :</strong> Assurez-vous que le problème vient de RenExtract et pas d'un outil de traduction externe</li>
                            <li><strong>Consulter les logs :</strong> Le dossier <code>05_ConfigRenExtract</code> contient les logs détaillés (mode debug recommandé)</li>
                            <li><strong>Vérifier la version :</strong> Assurez-vous d'avoir la dernière version de RenExtract</li>
                            <li><strong>Test minimal :</strong> Testez avec un petit fichier <code>.rpy</code> simple pour isoler le problème</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- ============================================================ -->
        <!-- SECTION 3 : SUPPORT ET CONTACT -->
        <!-- ============================================================ -->
        
        <div class="section" id="support-contact">
            <h2>📧 Contacter l'équipe de développement</h2>
            <p>Plusieurs moyens pour obtenir de l'aide et contacter l'équipe de développement.</p>
            
            <h3>💬 Support et assistance</h3>
            
            <style>
            .contact-card {{
                background: var(--card-bg);
                padding: 20px;
                border-radius: 8px;
                transition: all 0.3s ease;
            }}
            .contact-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(0,0,0,0.2);
            }}
            .contact-link {{
                color: var(--accent);
                text-decoration: none;
                transition: color 0.2s ease;
            }}
            .contact-link:hover {{
                color: #60a5fa;
                text-decoration: underline;
            }}
            </style>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 20px;">
                
                <!-- Email -->
                <div class="contact-card" style="border-left: 4px solid #f59e0b;">
                    <h4>📧 Email</h4>
                    <p style="font-size: 1.2em; margin: 10px 0;">
                        <strong><a href="mailto:RenExtract@pm.me" class="contact-link">RenExtract@pm.me</a></strong>
                    </p>
                    <p>Pour les questions détaillées et le support technique.</p>
                    <p style="opacity: 0.8; font-style: italic;">Idéal pour les problèmes complexes nécessitant des captures d'écran.</p>
                </div>
                
                <!-- Discord -->
                <div class="contact-card" style="border-left: 4px solid #5865f2;">
                    <h4>🎮 Discord (Recommandé)</h4>
                    <p style="font-size: 1.2em; margin: 10px 0;">
                        <strong><a href="https://discord.gg/Yp2Hm8JWQ2" target="_blank" class="contact-link">Rejoindre le serveur</a></strong>
                    </p>
                    <p>Communauté active, support rapide et discussions.</p>
                    <p style="opacity: 0.8; font-style: italic;">Réponse la plus rapide, entraide communautaire.</p>
                </div>
                
                <!-- GitHub Issues -->
                <div class="contact-card" style="border-left: 4px solid #333;">
                    <h4>🛠 Signaler un bug</h4>
                    <p style="font-size: 1.2em; margin: 10px 0;">
                        <strong><a href="https://github.com/Rory-Mercury-91/RenExtract/issues" target="_blank" class="contact-link">GitHub Issues</a></strong> ou bien le <strong><a href="https://discord.gg/Yp2Hm8JWQ2" target="_blank" class="contact-link">Discord</a></strong>
                    </p>
                    <p>Rapportez les bugs et demandez des fonctionnalités.</p>
                    <p style="opacity: 0.8; font-style: italic;">GitHub pour bugs confirmés, Discord pour diagnostic rapide.</p>
                </div>
                
                <!-- Releases -->
                <div class="contact-card" style="border-left: 4px solid #10b981;">
                    <h4>📦 Dernière version</h4>
                    <p style="font-size: 1.2em; margin: 10px 0;">
                        <strong><a href="https://github.com/Rory-Mercury-91/RenExtract/releases" target="_blank" class="contact-link">Téléchargements</a></strong>
                    </p>
                    <p>Toujours avoir la version la plus récente.</p>
                    <p style="opacity: 0.8; font-style: italic;">Vérifiez régulièrement les mises à jour.</p>
                </div>
                
            </div>
            
            <!-- Conseils pour obtenir de l'aide -->
            <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%); padding: 20px; border-radius: 8px; border-left: 4px solid #10b981; margin-top: 30px;">
                <h4>💡 Conseils pour obtenir de l'aide</h4>
                <ul style="margin: 10px 0; padding-left: 40px;">
                    <li><strong>Discord</strong> est le moyen le plus rapide pour obtenir de l'aide (réponse rapide)</li>
                    <li><strong>Email</strong> pour les questions complexes nécessitant des captures d'écran ou des logs</li>
                    <li><strong>GitHub Issues</strong> uniquement pour les bugs liés au code lui-même</li>
                    <li>Précisez toujours votre <strong>version de RenExtract</strong> et votre <strong>système d'exploitation</strong></li>
                    <li>Joignez les <strong>logs du dossier <code>05_ConfigRenExtract</code></strong> si vous êtes en mode debug</li>
                </ul>
            </div>
        </div>
        
        <!-- ============================================================ -->
        <!-- SECTION 4 : CRÉDITS ET REMERCIEMENTS -->
        <!-- ============================================================ -->
        
        <div class="section" id="credits">
            <h2>🏆 Crédits et remerciements</h2>
            <p>RenExtract est le fruit d'un travail collaboratif et de contributions précieuses.</p>
            
            <h3>👥 Équipe de développement</h3>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 20px 0;">
                
                <!-- Développeur principal -->
                <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%); padding: 25px; border-radius: 8px; border-left: 4px solid #8b5cf6;">
                    <h4>👨‍💻 Développement principal</h4>
                    <p style="font-size: 1.2em; margin: 10px 0;">
                        <strong>Rory-Mercury-91</strong>
                    </p>
                    <p>Concepteur et développeur principal de RenExtract.</p>
                </div>
                
                <!-- Générateur -->
                <div style="background: linear-gradient(135deg, rgba(74, 144, 226, 0.1) 0%, rgba(74, 144, 226, 0.05) 100%); padding: 25px; border-radius: 8px; border-left: 4px solid var(--accent);">
                    <h4>🎮 Générateur Ren'Py</h4>
                    <p style="font-size: 1.2em; margin: 10px 0;">
                        <strong>Virusf</strong>
                    </p>
                    <p>Contribution majeure pour une grosse partie du générateur (base du code).</p>
                </div>
                
                <!-- Éditeur temps réel -->
                <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%); padding: 25px; border-radius: 8px; border-left: 4px solid #10b981;">
                    <h4>⚡ Éditeur Temps Réel</h4>
                    <p style="font-size: 1.2em; margin: 10px 0;">
                        <strong>Andric31</strong>
                    </p>
                    <p>Idée originale et base de code pour l'éditeur en temps réel.</p>
                </div>
                
                <!-- Communauté -->
                <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%); padding: 25px; border-radius: 8px; border-left: 4px solid #f59e0b;">
                    <h4>🌟 Communauté</h4>
                    <p style="font-size: 1.2em; margin: 10px 0;">
                        <strong>Principalement DxSnake</strong>
                    </p>
                    <p>Retours précieux, tests et suggestions d'amélioration.</p>
                </div>
                
            </div>
            
            <!-- Liens utiles -->
            <h3>🔗 Liens utiles</h3>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0;">
                
                <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; text-align: center;">
                    <h4>📂 Dépôt GitHub</h4>
                    <p>
                        <a href="https://github.com/Rory-Mercury-91/RenExtract" target="_blank" style="color: var(--accent); text-decoration: none; font-weight: bold;">
                            Code source complet
                        </a>
                    </p>
                </div>
                
                
                <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; text-align: center;">
                    <h4>🎮 Ren'Py Officiel</h4>
                    <p>
                        <a href="https://www.renpy.org/" target="_blank" style="color: var(--accent); text-decoration: none; font-weight: bold;">
                            Site officiel Ren'Py
                        </a>
                    </p>
                </div>
                
            </div>
            
            <!-- Projet open source -->
            <h3>🌐 Projet open source</h3>
            <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%); padding: 20px; border-radius: 8px; border-left: 4px solid #10b981; margin: 15px 0;">
                <p>RenExtract est un projet open source disponible sur GitHub. Les contributions, suggestions et rapports de bugs sont les bienvenus !</p>
                <p style="margin-top: 15px;"><strong>Comment contribuer :</strong></p>
                <ul style="margin: 10px 0; padding-left: 40px;">
                    <li>Signalez les bugs via <strong>GitHub Issues</strong></li>
                    <li>Proposez des améliorations sur <strong>Discord</strong></li>
                    <li>Partagez vos retours d'expérience</li>
                    <li>Aidez d'autres utilisateurs sur la communauté</li>
                </ul>
            </div>
            
            <!-- Citation finale -->
            <div style="text-align: center; margin-top: 40px; padding: 30px; background: linear-gradient(135deg, var(--hdr) 0%, rgba(74, 144, 226, 0.05) 100%); border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <p style="font-style: italic; opacity: 0.9; font-size: 1.2em; line-height: 1.6; margin-bottom: 15px;">
                    "Merci à tous pour votre contribution à RenExtract !"
                </p>
                <p style="opacity: 0.7; font-size: 1em;">
                    Rory-Mercury-91
                </p>
            </div>
        </div>
    """
