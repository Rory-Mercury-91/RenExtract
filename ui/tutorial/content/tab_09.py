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
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 20px;">
                
                <!-- Question 1 -->
                <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid var(--accent);">
                    <h4>🎯 Quelle différence entre Interface Principale et Générateur Ren'Py ?</h4>
                    <p><strong>Règle simple :</strong></p>
                    <ul>
                        <li><strong>Interface Principale</strong> : pour traiter un fichier spécifique (.rpy → .txt → .rpy)</li>
                        <li><strong>Générateur Ren'Py</strong> : pour configurer l'infrastructure complète du projet</li>
                    </ul>
                </div>
                
                <!-- Question 2 -->
                <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid #ef4444;">
                    <h4>💥 Le jeu plante après ma traduction !</h4>
                    <p><strong>Solution :</strong> Utilise le <strong>Vérificateur de Cohérence</strong> dans Outils Spécialisés.</p>
                    <p>Le rapport HTML pourra te montrer la ligne problématique et le type d'erreur (variable manquante, balise mal fermée, etc.).</p>
                </div>
                
                <!-- Question 3 -->
                <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid var(--accent);">
                    <h4>📁 Où sont mes fichiers à traduire ?</h4>
                    <p>Dans le dossier <code>01_Temporaires</code> après une extraction.</p>
                    <p><strong>Accès rapide :</strong> Interface Principale → Onglet <strong>OUTILS</strong> → <strong>📂 Temporaires</strong>.</p>
                </div>
                
                <!-- Question 4 -->
                <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid #10b981;">
                    <h4>🔄 Comment récupérer un fichier cassé ?</h4>
                    <p><strong>Gestionnaire de Sauvegardes</strong> :</p>
                    <ol>
                        <li>Ouvre le gestionnaire (Interface Principale → OUTILS)</li>
                        <li>Filtre par le jeu concerné</li>
                        <li>Sélectionne le <strong>Type</strong></li>
                        <li>Restaure la dernière version fonctionnelle</li>
                    </ol>
                </div>
                
                <!-- Question 5 -->
                <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid var(--accent);">
                    <h4>🔤 Les caractères français accentués ne s'affichent pas ?</h4>
                    <p>Dans <strong>Générateur Ren'Py</strong> :</p>
                    <ol>
                        <li>Va dans l'onglet <strong>Génération</strong></li>
                        <li>Teste d'abord dans l'<strong>aperçu des polices</strong></li>
                        <li>Sélectionne <strong>uniquement</strong> les polices marquées comme "disponibles"</li>
                    </ol>
                </div>
                
                <!-- Question 6 -->
                <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid #8b5cf6;">
                    <h4>⚡ Comment utiliser l'Éditeur Temps Réel ?</h4>
                    <p><strong>Étapes :</strong></p>
                    <ol>
                        <li>Outils Spécialisés → <strong>Éditeur Temps Réel</strong></li>
                        <li>Installe le module dans ton jeu</li>
                        <li>Lance le jeu</li>
                        <li>Consulte le <strong>tutoriel complet</strong> (Onglet Outils) pour toutes les fonctionnalités</li>
                    </ol>
                </div>
                
                <!-- Question 7 (NOUVELLE) -->
                <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid #f59e0b;">
                    <h4>🛡️ Pourquoi certains fichiers sont automatiquement exclus ?</h4>
                    <p><strong>Fichiers système protégés :</strong></p>
                    <ul>
                        <li><code>common.rpy</code> (Ren'Py)</li>
                        <li><code>99_Z_Console.rpy</code> (RenExtract)</li>
                        <li><code>99_Z_ScreenPreferences.rpy</code> (RenExtract)</li>
                        <li><code>99_Z_FontSystem.rpy</code> (RenExtract)</li>
                    </ul>
                    <p>Protection contre la suppression accidentelle lors du nettoyage.</p>
                </div>
                
                <!-- Question 8 (NOUVELLE) -->
                <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid var(--accent);">
                    <h4>🧹 Comment nettoyer un gros projet avec plusieurs langues ?</h4>
                    <p><strong>Nettoyage Intelligent</strong> :</p>
                    <ol>
                        <li>Outils Spécialisés → <strong>Nettoyage Intelligent</strong></li>
                        <li>Sélectionne ton projet multi-langues</li>
                        <li>Choisis les langues à nettoyer (sélection multiple)</li>
                        <li>Lance le nettoyage → rapport HTML détaillé automatique</li>
                    </ol>
                </div>
                
                <!-- Question 9 (NOUVELLE) -->
                <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid var(--accent);">
                    <h4>💾 Quelle est la différence entre les 4 types de sauvegardes ?</h4>
                    <ul>
                        <li><strong>Sécurité</strong> : avant extraction (conservée indéfiniment)</li>
                        <li><strong>Nettoyage</strong> : avant nettoyage projet (conservée indéfiniment)</li>
                        <li><strong>Avant RPA</strong> : avant compilation RPA (conservée indéfiniment)</li>
                        <li><strong>Édition temps réel</strong> : modifications en direct (max 10 fichiers, rotation automatique)</li>
                    </ul>
                </div>
                
                <!-- Question 10 (NOUVELLE) -->
                <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid var(--accent);">
                    <h4>🎨 Comment personnaliser les patterns de protection ?</h4>
                    <p><strong>Paramètres → Patterns de protection</strong> :</p>
                    <ol>
                        <li>Configure tes patterns personnalisés (Astérisques, Tildes)</li>
                        <li>Teste-les avec le <strong>générateur de placeholders</strong></li>
                        <li>Utilise le <strong>suffixe numérique</strong> recommandé pour éviter les conflits</li>
                    </ol>
                </div>
                
            </div>
            
            <!-- Conseils rapides -->
            <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%); padding: 20px; border-radius: 8px; border-left: 4px solid #10b981; margin-top: 30px;">
                <h4>💡 Conseils rapides</h4>
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li><strong>Sauvegarde toujours le jeu original</strong> avant toute modification</li>
                    <li><strong>Consulte les rapports</strong> dans le dossier <code>03_Rapports</code> en cas d'erreur</li>
                    <li><strong>Garde tes paramètres d'exclusion</strong> pour éviter les faux positifs lors des vérifications</li>
                </ul>
            </div>
        </div>
        
        <!-- ============================================================ -->
        <!-- SECTION 2 : DÉPANNAGE TECHNIQUE -->
        <!-- ============================================================ -->
        
        <div class="section" id="troubleshooting">
            <h2>🔧 Dépannage Technique</h2>
            <p>Solutions aux problèmes techniques les plus courants rencontrés lors de l'utilisation de RenExtract.</p>
            
            <!-- Problèmes 1 et 2 côte à côte -->
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 20px 0;">
                <!-- Problème 1 -->
                <div>
                    <h3>⚠️ "Aucun texte trouvé"</h3>
                    <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid #f59e0b;">
                        <h4>Causes possibles :</h4>
                        <ul>
                            <li>Archives <code>.rpa</code> ou <code>.rpyc</code> non décompilées</li>
                            <li>Fichier ne contenant que du code (pas de dialogue)</li>
                        </ul>
                        <h4>Solutions :</h4>
                        <ul>
                            <li><strong>Décompiler :</strong> Les archives <code>.rpa</code> et <code>.rpyc</code> doivent être décompilées</li>
                            <li><strong>Utiliser Générateur → Extraction Config</strong> pour les textes d'interface</li>
                            <li><strong>Tenter avec le SDK officiel</strong> (Paramètres → SDK Ren'Py)</li>
                            <li><strong>Tester avec un autre fichier</strong> du même jeu</li>
                        </ul>
                    </div>
                </div>
                
                <!-- Problème 2 -->
                <div>
                    <h3>❌ "Échec de validation"</h3>
                    <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid #ef4444;">
                        <h4>Diagnostic :</h4>
                        <ul>
                            <li>Consulte le <strong>rapport détaillé</strong> dans le dossier <code>03_Rapports</code></li>
                            <li>Utilise le <strong>Vérificateur de Cohérence</strong> pour localiser précisément les erreurs</li>
                        </ul>
                        <h4>Corrections courantes :</h4>
                        <ul>
                            <li><strong>Variables <code>[]</code> :</strong> vérifie que toutes les variables sont conservées intactes</li>
                            <li><strong>Balises <code>{{}}</code> :</strong> assure-toi que toutes les balises sont bien fermées</li>
                            <li><strong>Codes spéciaux :</strong> ne modifie pas les <code>\\n</code>, <code>%</code>, etc.</li>
                        </ul>
                        <h4>Solution de secours :</h4>
                        <p>Restaure une version valide depuis le <strong>Gestionnaire de Sauvegardes</strong>.</p>
                    </div>
                </div>
            </div>
            
            <!-- Problème 3 -->
            <h3>🐌 "L'extraction est très lente"</h3>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 15px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--accent);">
                    <h5>🛡️ Antivirus</h5>
                    <p>Ajoute RenExtract aux <strong>exclusions de ton antivirus</strong>. L'analyse en temps réel peut considérablement ralentir le traitement.</p>
                </div>
                
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--accent);">
                    <h5>💾 Stockage</h5>
                    <p>Utilise un <strong>SSD</strong> si possible pour améliorer les performances d'écriture/lecture.</p>
                </div>
                
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--accent);">
                    <h5>📁 Espace disque</h5>
                    <p>Assure-toi que ton <strong>disque n'est pas plein</strong> et dispose d'espace suffisant.</p>
                </div>
            </div>
            
            <!-- Problème 4 -->
            <h3>🔒 "Erreur d'accès fichier"</h3>
            <ul>
                <li><strong>Ferme le jeu Ren'Py</strong> s'il est en cours d'exécution</li>
                <li><strong>Lance RenExtract en administrateur</strong> (clic droit → Exécuter en tant qu'administrateur)</li>
                <li><strong>Vérifie que le fichier n'est pas ouvert</strong> dans un éditeur de texte</li>
                <li><strong>Vérifie les propriétés du fichier</strong> : il ne doit pas être en lecture seule</li>
            </ul>
            
            <!-- Problèmes 5 et diagnostic côte à côte -->
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 20px 0;">
                <!-- Problème 5 -->
                <div>
                    <h3>🚨 Problèmes de compatibilité</h3>
                    <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid #8b5cf6;">
                        <h4>Versions Ren'Py :</h4>
                        <ul>
                            <li><strong>Ren'Py 6.x :</strong> Support limité, utilise les fonctions de base</li>
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
                            <li><strong>Vérifier la source :</strong> Assure-toi que le problème vient de RenExtract et pas d'un outil de traduction externe</li>
                            <li><strong>Consulter les logs :</strong> Le dossier <code>04_Configs</code> contient les logs détaillés (mode debug recommandé)</li>
                            <li><strong>Vérifier la version :</strong> Assure-toi d'avoir la dernière version de RenExtract</li>
                            <li><strong>Test minimal :</strong> Teste avec un petit fichier <code>.rpy</code> simple pour isoler le problème</li>
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
                    <p>Rapporte les bugs et demande des fonctionnalités.</p>
                    <p style="opacity: 0.8; font-style: italic;">GitHub pour bugs confirmés, Discord pour diagnostic rapide.</p>
                </div>
                
                <!-- Releases -->
                <div class="contact-card" style="border-left: 4px solid #10b981;">
                    <h4>📦 Dernière version</h4>
                    <p style="font-size: 1.2em; margin: 10px 0;">
                        <strong><a href="https://github.com/Rory-Mercury-91/RenExtract/releases" target="_blank" class="contact-link">Téléchargements</a></strong>
                    </p>
                    <p>Toujours avoir la version la plus récente.</p>
                    <p style="opacity: 0.8; font-style: italic;">Vérifie régulièrement les mises à jour.</p>
                </div>
                
            </div>
            
            <!-- Conseils pour obtenir de l'aide -->
            <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%); padding: 20px; border-radius: 8px; border-left: 4px solid #10b981; margin-top: 30px;">
                <h4>💡 Conseils pour obtenir de l'aide</h4>
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li><strong>Discord</strong> est le moyen le plus rapide pour obtenir de l'aide (réponse en quelques minutes)</li>
                    <li><strong>Email</strong> pour les questions complexes nécessitant des captures d'écran ou des logs</li>
                    <li><strong>GitHub Issues</strong> uniquement pour les bugs confirmés et reproductibles</li>
                    <li>Précise toujours ta <strong>version de RenExtract</strong> et ton <strong>système d'exploitation</strong></li>
                    <li>Joins les <strong>logs du dossier <code>04_Configs</code></strong> si tu es en mode debug</li>
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
                        <strong>Tous les utilisateurs</strong>
                    </p>
                    <p>Retours précieux, tests et suggestions d'amélioration.</p>
                </div>
                
            </div>
            
            <!-- Liens utiles -->
            <h3>🔗 Liens utiles</h3>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0;">
                
                <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; text-align: center;">
                    <h4>📂 Dépôt GitHub</h4>
                    <p>
                        <a href="https://github.com/Rory-Mercury-91/RenExtract" target="_blank" style="color: var(--accent); text-decoration: none; font-weight: bold;">
                            Code source complet
                        </a>
                    </p>
                </div>
                
                <div style="background: var(--card-bg); padding: 20px; border-radius: 8px; text-align: center;">
                    <h4>📋 Documentation</h4>
                    <p>
                        <a href="https://github.com/Rory-Mercury-91/RenExtract/wiki" target="_blank" style="color: var(--accent); text-decoration: none; font-weight: bold;">
                            Wiki et guides
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
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li>Signale les bugs via <strong>GitHub Issues</strong></li>
                    <li>Propose des améliorations sur <strong>Discord</strong></li>
                    <li>Partage tes retours d'expérience</li>
                    <li>Aide d'autres utilisateurs sur la communauté</li>
                </ul>
            </div>
            
            <!-- Citation finale -->
            <div style="text-align: center; margin-top: 40px; padding: 30px; background: linear-gradient(135deg, var(--hdr) 0%, rgba(74, 144, 226, 0.05) 100%); border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <p style="font-style: italic; opacity: 0.9; font-size: 1.2em; line-height: 1.6; margin-bottom: 15px;">
                    "Merci à tous ceux qui contribuent à faire de RenExtract un outil toujours meilleur pour la communauté de traduction Ren'Py !"
                </p>
                <p style="opacity: 0.7; font-size: 1em;">
                    — L'équipe RenExtract
                </p>
            </div>
        </div>
    """
