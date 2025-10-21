# ui/tutorial/content/tab_07.py
"""
Module de contenu pour l'onglet 7 : Paramètres
Guide complet de l'interface des paramètres de RenExtract
"""

def generate_content(generator, language=None, translations=None):
    """Génère le contenu de l'onglet Paramètres (français uniquement)
    
    Args:
        generator: Instance du générateur avec méthodes utilitaires
        language: Non utilisé (compatibilité)
        translations: Non utilisé (compatibilité)
    
    Returns:
        str: HTML généré pour l'onglet
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # NAVIGATION RAPIDE
    # ═══════════════════════════════════════════════════════════════════════════
    
    navigation = """
        <div class="quick-nav-section" style="background: var(--card-bg); padding: 20px; margin-bottom: 30px; border-radius: 8px; border-left: 4px solid var(--accent);">
            <h3 style="margin-top: 0;">🧭 Navigation Rapide</h3>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 15px;">
                
                <a href="#vue-ensemble-parametres" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">⚙️ Vue d'ensemble</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Présentation générale</div>
                </a>
                
                <a href="#onglet-interface" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🎨 Interface & Appli</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Apparence et comportement</div>
                </a>
                
                <a href="#onglet-extraction" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🛡️ Extraction</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Protection et patterns</div>
                </a>
                
                <a href="#onglet-couleurs" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🎨 Couleurs</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Personnalisation visuelle</div>
                </a>
                
                <a href="#onglet-chemins" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🛠️ Chemins</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">SDK et éditeurs</div>
                </a>
                
                <a href="#footer-parametres" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">📋 Footer</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Actions globales</div>
                </a>
                
            </div>
        </div>
        
        <style>
        .nav-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            border-color: var(--accent);
        }}
        </style>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 1 : VUE D'ENSEMBLE
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_1 = f"""
        <div class="section" id="vue-ensemble-parametres">
            <h2>⚙️ Vue d'Ensemble des Paramètres</h2>
            
            <h3>Qu'est-ce que c'est ?</h3>
            <p>L'interface des <strong>Paramètres</strong> est votre centre de configuration pour personnaliser RenExtract selon vos besoins. 
            Elle regroupe <strong>tous les réglages de l'application</strong> dans une interface claire et organisée.</p>
            
            <h4>🔑 Accès rapide</h4>
            <p>Pour ouvrir les paramètres, cliquez sur le bouton "⚙️ Paramètres" dans le header de RenExtract.</p>
            {generator._get_image_html("07_tab_settings", "001", 
                "Bouton d'accès aux paramètres", 
                "Accès aux paramètres depuis l'interface principale")}
            
            <p>Cette interface vous permet de :</p>
            <ul style="margin-left: 40px;">
                <li>🎨 <strong>Personnaliser l'apparence</strong> : Mode sombre, couleurs des boutons</li>
                <li>🛡️ <strong>Configurer les protections</strong> : Patterns personnalisés, détection doublons</li>
                <li>🛠️ <strong>Définir les chemins</strong> : SDK Ren'Py, éditeurs de code</li>
                <li>⚙️ <strong>Ajuster le comportement</strong> : Ouvertures auto, notifications, modes de sauvegarde</li>
            </ul>
            
            <h4>🏗️ Structure de l'interface</h4>
            <p>L'interface est organisée en <strong>4 onglets principaux</strong> :</p>
            <ol style="margin-left: 40px;">
                <li><strong>🎨 Interface & Application</strong> : Configuration du comportement et de l'apparence</li>
                <li><strong>🛡️ Extraction & Protection</strong> : Gestion des patterns et options d'extraction</li>
                <li><strong>🎨 Couleurs des boutons</strong> : Personnalisation complète des couleurs</li>
                <li><strong>🛠️ Chemins d'accès</strong> : Configuration du SDK et des éditeurs</li>
            </ol>
            
            <div class="tip-box">
                <h4>💡 Sauvegarde automatique</h4>
                <p>Tous vos changements sont <strong>sauvegardés automatiquement</strong> lorsque vous fermez la fenêtre. 
                Vous recevrez une notification de confirmation "✅ Tous les paramètres ont été sauvegardés".</p>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 2 : ONGLET INTERFACE & APPLICATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_2 = f"""
        <div class="section" id="onglet-interface">
            <h2>🎨 Onglet Interface & Application</h2>
            
            {generator._get_image_html("07_tab_settings/applications_tab", "001", 
                "Fenêtre principale de l'onglet Applications", 
                "Vue d'ensemble de l'onglet Interface & Application")}
            
            <p>Cet onglet regroupe tous les paramètres liés au <strong>comportement et à l'apparence</strong> de RenExtract. 
            Il est divisé en <strong>4 sections</strong> principales.</p>
            
            <h3>🚀 Ouvertures automatiques</h3>
            
            {generator._get_image_html("07_tab_settings/applications_tab", "002", 
                "Section ouvertures automatiques", 
                "Checkboxes pour configurer les ouvertures automatiques")}
            
            <h4>🔧 Configuration des ouvertures</h4>
            <p>Ces options vous permettent de choisir ce qui s'ouvre automatiquement après certaines actions :</p>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div style="margin: 0;">
                    <ul>
                        <li><strong>🚀 Fichiers</strong> : Ouvre les fichiers générés après extraction/reconstruction</li>
                        <li><strong>📁 Dossiers</strong> : Ouvre le dossier de sortie après certaines opérations</li>
                    </ul>
                </div>
                <div style="margin: 0;">
                    <ul>
                        <li><strong>📊 Rapport cohérence</strong> : Ouvre automatiquement le rapport HTML après vérification</li>
                        <li><strong>📂 Champ de sortie</strong> : Affiche le chemin de sortie dans l'interface principale</li>
                    </ul>
                </div>
            </div>
            
            <h3>🎨 Apparence et notifications</h3>
            
            {generator._get_image_html("07_tab_settings/applications_tab", "003", 
                "Section apparence et notifications", 
                "Configuration du mode sombre, notifications et debug")}
            
            <h4>🔔 Mode de notification</h4>
            <p>Choisissez comment RenExtract vous notifie des résultats :</p>
            <ul style="margin-left: 40px;">
                <li><strong>Statut seulement</strong> : Notifications discrètes dans la barre de statut</li>
                <li><strong>Popups détaillés</strong> : Fenêtres de confirmation avec détails complets</li>
            </ul>
            
            <h4>🌙 Mode sombre</h4>
            <p>Activez ou désactivez le thème sombre de l'interface.</p>
            <p>✅ <strong>Recommandé :</strong> Mode sombre activé pour réduire la fatigue oculaire lors de longues sessions de travail.</p>
            
            <h4>🐛 Mode debug</h4>
            <p>Le mode debug affiche des informations techniques détaillées dans les logs.</p>
            <p><strong style="color: #ef4444;">⚠️ Attention :</strong> Ce mode peut ralentir l'application. Activez-le uniquement si vous rencontrez des problèmes ou si un développeur vous le demande.</p>
            
            <h3>📝 Éditeur de code</h3>
            
            {generator._get_image_html("07_tab_settings/applications_tab", "004", 
                "Section éditeur de code", 
                "Sélection de l'éditeur de code par défaut")}
            
            <h4>🔧 Choix de l'éditeur</h4>
            <p>Définissez quel éditeur de code utiliser pour ouvrir les fichiers (uniquement lié au rapport HTML et à l'éditeur en temps réel) :</p>
            <ul style="margin-left: 40px;">
                <li><strong>Défaut Windows</strong> : Utilisez le programme par défaut du système</li>
                <li><strong>Éditeur détecté</strong> : Si vous avez configuré un éditeur personnalisé dans l'onglet "Chemins d'accès", il apparaîtra ici</li>
            </ul>
        
            <h3>🤖 Graq AI</h3>
            
            {generator._get_image_html("07_tab_settings/applications_tab", "005", 
                "Section Graq AI", 
                "Configuration de l'intégration Graq AI avec bouton d'aide")}
            
            <h4>🔧 Configuration Graq AI</h4>
            <p>Cette section vous permet de configurer l'intégration avec Graq AI pour l'assistance à la traduction.</p>
            <p><strong>💡 Documentation complète :</strong> Une documentation précise est disponible en appuyant sur le bouton d'aide de cette section.</p>
            
            <h3>⚙️ Actions système</h3>
            
            {generator._get_image_html("07_tab_settings/applications_tab", "006", 
                "Section actions système", 
                "Boutons de nettoyage et réinitialisation")}
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div style="margin: 0;">
                    <h4>🧹 Nettoyer les fichiers temporaires</h4>
                    <p>Supprime certains fichiers temporaires créés par RenExtract (cache de l'interface, fichiers de session...).</p>
                    <p>💡 <strong>Astuce :</strong> Faites ceci régulièrement pour libérer de l'espace disque.</p>
                </div>
                
                <div style="margin: 0;">
                    <h4>🔄 Réinitialiser l'application</h4>
                    <p><strong style="color: #ef4444;">⚠️ Action irréversible !</strong></p>
                    <p>Remet tous les paramètres à leurs valeurs par défaut, efface le cache <strong>et nettoie les fichiers temporaires</strong>. Utilisez ceci uniquement en cas de problème grave.</p>
                </div>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 3 : ONGLET EXTRACTION & PROTECTION
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_3 = f"""
        <div class="section" id="onglet-extraction">
            <h2>🛡️ Onglet Extraction & Protection</h2>
            
            {generator._get_image_html("07_tab_settings/extraction_tab", "001", 
                "Vue d'ensemble onglet Extraction & Protection", 
                "Interface complète avec options de protection et patterns")}
            
            <p>Cet onglet vous permet de configurer finement le <strong>processus d'extraction</strong> et les <strong>protections automatiques</strong> 
            qui préservent vos codes Ren'Py lors de la traduction.</p>
            
            <h3>🛡️ Configuration de la protection et sauvegarde</h3>
            
            {generator._get_image_html("07_tab_settings/extraction_tab", "002", 
                "Sections options, limite et mode sauvegarde regroupées", 
                "Options de protection, limite de lignes et mode de sauvegarde")}
            
            <h4>🔧 Options de protection</h4>
            <ul style="margin-left: 40px;">
                <li><strong>🔍 Détecter et gérer les doublons</strong> : Évite de traduire deux fois la même ligne (recommandé)</li>
                <li><strong>📊 Suivi de progression</strong> : Surveille l'avancement de vos projets de traduction</li>
                <li><strong>⚙️ Paramètres cohérence</strong> : Ouvre une fenêtre pour configurer les vérifications (voir ci-dessous)</li>
            </ul>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div style="margin: 0;">
                    <h4>📄 Limite de lignes par fichier</h4>
                    <p>Définit le nombre maximum de lignes par fichier extrait.</p>
                    <p><strong>Exemple :</strong> <code>1000</code> = fichiers de 1000 lignes maximum</p>
                    <p>💡 Laissez vide pour aucune limite.</p>
                </div>
                
                <div style="margin: 0;">
                    <h4>💾 Mode de sauvegarde</h4>
                    <p>Choisissez comment les fichiers sont enregistrés :</p>
                    <ul style="margin-left: 40px;">
                        <li><strong>Écraser l'original</strong> : Remplace le fichier existant</li>
                        <li><strong>Créer nouveau fichier</strong> : Génère un fichier <code>&lt;File_Name&gt;_translated.rpy</code></li>
                    </ul>
                </div>
            </div>
            
            <h3>⚙️ Paramètres de cohérence</h3>
            
            {generator._get_image_html("07_tab_settings/extraction_tab", "004", 
                "Bouton paramètres cohérence", 
                "Accès aux paramètres de vérification de cohérence")}
            
            <h4>✅ Configuration des vérifications</h4>
            <p>Cette fenêtre vous permet de choisir quelles vérifications seront effectuées lors du <strong>contrôle de cohérence après reconstruction</strong>. 
            Ces vérifications sont différentes des cases cochées dans l'onglet Actions de l'interface principale.</p>
            
            <div style="background: linear-gradient(135deg, rgba(74, 144, 226, 0.1) 0%, rgba(74, 144, 226, 0.05) 100%); padding: 20px; border-radius: 8px; border-left: 4px solid var(--accent); margin: 1.5rem 0;">
                <h4 style="margin-top: 0; color: var(--accent);">🔍 9 types de vérifications disponibles :</h4>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
                    <div>
                        <ul style="margin-left: 40px;">
                            <li>📝 Lignes non traduites</li>
                            <li>… Points de suspension</li>
                            <li>% Variables %</li>
                            <li>💬 Guillemets</li>
                            <li>() Parenthèses</li>
                        </ul>
                    </div>
                    <div>
                        <ul style="margin-left: 40px;">
                            <li>📐 Syntaxe Ren'Py</li>
                            <li>💬 DeepL ellipsis</li>
                            <li>% Pourcentage isolé</li>
                            <li>🇫🇷 Guillemets français «»</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <h4>💡 Boutons rapides</h4>
            <ul style="margin-left: 40px;">
                <li><strong>✅ Tout sélectionner</strong> : Activez toutes les vérifications (recommandé pour une analyse complète)</li>
                <li><strong>❌ Tout désélectionner</strong> : Désactivez toutes les vérifications</li>
                <li><strong>💾 Sauvegarder</strong> : Sauvegarde votre configuration et ferme automatiquement la fenêtre</li>
            </ul>
            
            <h3>🔧 Patterns de protection</h3>
            
            {generator._get_image_html("07_tab_settings/extraction_tab", "003", 
                "Patterns avec incrémentation visible", 
                "Exemples de patterns personnalisés montrant clairement l'incrémentation automatique")}
            
            <p>Les patterns sont des <strong>placeholders personnalisés</strong> qui protègent vos codes Ren'Py lors de l'extraction. 
            Ils remplacent temporairement les codes, variables et caractères spéciaux pour éviter au maximum qu'ils soient modifiés par les outils de traduction. 
            N'étant pas fiable à 100%, par sécurité un rapport de cohérence est généré après reconstruction pour signaler les erreurs.</p>
            
            <h4>🛡️ Les 3 types de patterns</h4>
            <div style="margin-bottom: 15px; margin-left: 40px;">
                <p><strong>🔧 Pattern Codes/Variables</strong></p>
                <p>Protège les codes de jeu et variables Ren'Py.</p>
                <p><strong>Exemple :</strong> <code>RENPY_CODE_001</code></p>
            </div>
            <div style="margin-bottom: 15px; margin-left: 40px;">
                <p><strong>⭐ Pattern Astérisques & 〰️ Pattern Tildes</strong></p>
                <p>Ces deux patterns ont <strong>la même utilité</strong> : protéger les mots ou phrases entourés d'astérisques ou de tilde 
                (<code>*exemple*</code> et <code>~exemple~</code>) et les extraire dans un fichier séparé pour faciliter leur traduction en préservant les caractères spéciaux.</p>
                <p><strong>Exemples :</strong> <code>RENPY_ASTERISK_001</code>, <code>RENPY_TILDE_001</code></p>
            </div>
            
            <h4>🎯 Aperçu temps réel et incrémentation</h4>
            <p>Chaque pattern affiche un <strong>aperçu en temps réel</strong> montrant comment les placeholders seront générés. 
            L'image ci-dessus montre des exemples concrets :</p>
            <ul style="margin-left: 40px;">
                <li><code>(01)</code> → <code>(01), (02), (03)</code> : Pattern simple avec chiffres</li>
                <li><code>(B1)-1</code> → <code>(B1)-1, (B1)-2, (B1)-3</code> : Pattern avec lettre, chiffre et tiret</li>
                <li><code>(C1)1</code> → <code>(C1)1_001, (C1)1_002, (C1)1_003</code> : Pattern avec suffixe numérique</li>
            </ul>
            <p>💡 <strong>L'incrémentation s'adapte intelligemment</strong> à votre pattern ! Elle détecte automatiquement les chiffres et génère 
            la suite logique pour chaque code protégé.</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div style="margin: 0;">
                    <h4>🧪 Tester les patterns</h4>
                    <p>Le bouton <strong>"🧪 Tester"</strong> vérifie :</p>
                    <ul style="margin-left: 40px;">
                        <li>✅ <strong>Tous les patterns sont valides</strong></li>
                        <li>❌ <strong>X Doublons détectés :</strong> (placeholders) 
                            <br><small>💡 Une notification signale en direct la détection des doublons avant le test</small></li>
                    </ul>
                </div>
                
                <div style="margin: 0;">
                    <h4>🔄 Remettre par défaut</h4>
                    <p>Le bouton <strong>"🔄 Défaut"</strong> restaure les patterns recommandés :</p>
                    <ul style="margin-left: 40px;">
                        <li><code>RENPY_CODE_001</code></li>
                        <li><code>RENPY_ASTERISK_001</code></li>
                        <li><code>RENPY_TILDE_001</code></li>
                    </ul>
                </div>
            </div>
            
            <h4 style="color: #ef4444;">⚠️ Règles importantes</h4>
            <ul style="margin-left: 40px;">
                <li><strong>Pas de doublons</strong> : Les 3 patterns doivent être différents</li>
                <li><strong>Évitez les caractères protégés</strong> : N'utilisez pas de caractères que RenExtract tente déjà de protéger comme <code>[ ] {{ }} \\ /</code>, etc. Restez sur des lettres, chiffres et underscore pour éviter les conflits.</li>
            </ul>
            
            <div class="tip-box">
                <h4>💡 Besoin d'aide ?</h4>
                <p>Pour accéder à cette fenêtre d'aide directement depuis l'application, cliquez sur le bouton <strong>"À quoi ça sert ?"</strong> 
                présent dans l'onglet Extraction & Protection. Vous y trouverez toutes les explications détaillées sur chaque option.</p>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 4 : ONGLET COULEURS
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_4 = f"""
        <div class="section" id="onglet-couleurs">
            <h2>🎨 Onglet Couleurs des Boutons</h2>
            
            {generator._get_image_html("07_tab_settings/colors_tab", "001", 
                "Vue d'ensemble onglet Couleurs", 
                "Interface complète de personnalisation des couleurs")}
            
            <p>Cet onglet vous permet de <strong>personnaliser complètement les couleurs</strong> de tous les boutons de RenExtract. 
            Vous pouvez utiliser des <strong>presets prédéfinis</strong> ou créer votre propre palette personnalisée !</p>
            
            <h3>🎨 Presets de couleurs</h3>
            
            {generator._get_image_html("07_tab_settings/colors_tab", "002", 
                "Section presets et bouton reset", 
                "Sélection de presets et bouton de réinitialisation")}
            
            <h4>✨ Utiliser un preset</h4>
            <p>Les presets sont des <strong>combinaisons de couleurs prédéfinies</strong> harmonieuses et testées.</p>
            <ol style="margin-left: 40px;">
                <li>Sélectionnez un preset dans la liste déroulante</li>
                <li>Cliquez sur <strong>"✅ Appliquer le preset"</strong></li>
                <li>Les couleurs sont appliquées</li>
            </ol>
            <p><strong>💡 Recommandation :</strong> Pour que les changements de couleurs soient parfaitement visibles, 
            il est recommandé de <strong>fermer et rouvrir l'application</strong> après l'application d'un preset.</p>
            
            <h4>🔄 Remettre par défaut</h4>
            <p>Le bouton <strong>"Par défaut"</strong> restaure les couleurs d'origine de RenExtract. 
            Une confirmation vous sera demandée car cette action supprime toutes vos personnalisations.</p>
            
            <h3>🖌️ Personnalisation des couleurs</h3>
            
            {generator._get_image_html("07_tab_settings/colors_tab", "003", 
                "Grille des boutons colorés", 
                "8 boutons de couleur personnalisables")}
            
            <p>Vous pouvez personnaliser <strong>8 types de boutons</strong> différents :</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div style="margin: 0;">
                    <ul style="margin-left: 40px;">
                        <li>🔵 <strong>Bouton principal</strong> : Actions principales (Extraire, Reconstruire)</li>
                        <li>🟢 <strong>Bouton secondaire</strong> : Actions secondaires (Sauvegarder)</li>
                        <li>🟣 <strong>Bouton tertiaire</strong> : Actions alternatives</li>
                        <li>🔴 <strong>Bouton danger</strong> : Actions destructives (Supprimer)</li>
                    </ul>
                </div>
                <div style="margin: 0;">
                    <ul style="margin-left: 40px;">
                        <li>✅ <strong>Bouton succès</strong> : Actions de confirmation</li>
                        <li>ℹ️ <strong>Bouton aide</strong> : Accès à l'aide et documentation</li>
                        <li>⚠️ <strong>Bouton avertissement</strong> : Actions nécessitant attention</li>
                        <li>🛠️ <strong>Bouton utilitaire</strong> : Outils spécialisés</li>
                    </ul>
                </div>
            </div>
            
            <h3>🎨 Utiliser le color picker</h3>
            
            {generator._get_image_html("07_tab_settings/colors_tab", "004", 
                "Color picker", 
                "Interface du sélecteur de couleurs")}
            
            <h4>📝 Étapes pour changer une couleur</h4>
            <ol style="margin-left: 40px;">
                <li>Cliquez sur le bouton de couleur que vous voulez modifier</li>
                <li>Une fenêtre de sélection de couleur s'ouvre</li>
                <li>Choisissez votre nouvelle couleur (palette, hexadécimal, RGB...)</li>
                <li>Validez votre sélection</li>
                <li>La couleur est appliquée</li>
            </ol>
            <p><strong>💡 Recommandation :</strong> Comme pour les presets, il est recommandé de <strong>fermer et rouvrir l'application</strong> 
            pour que les changements de couleurs soient parfaitement appliqués partout.</p>
            
            <h4>💡 Astuces couleurs</h4>
            <ul style="margin-left: 40px;">
                <li><strong>Contraste :</strong> Choisissez des couleurs suffisamment contrastées pour une bonne lisibilité</li>
                <li><strong>Cohérence :</strong> Utilisez une palette harmonieuse (couleurs complémentaires ou analogues)</li>
                <li><strong>Accessibilité :</strong> Évitez les combinaisons difficiles à lire (ex: jaune sur blanc)</li>
                <li><strong>Test :</strong> Testez vos couleurs sur différentes parties de l'interface avant de valider</li>
            </ul>
            
            <div class="tip-box">
                <h4>💡 Besoin d'aide ?</h4>
                <p>Pour accéder à cette fenêtre d'aide directement depuis l'application, cliquez sur le bouton <strong>"À quoi ça sert ?"</strong> 
                présent dans l'onglet Couleurs des boutons. Vous y trouverez le détail complet de chaque catégorie de boutons.</p>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 5 : ONGLET CHEMINS D'ACCÈS
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_5 = f"""
        <div class="section" id="onglet-chemins">
            <h2>🛠️ Onglet Chemins d'Accès</h2>
            
            {generator._get_image_html("07_tab_settings/paths_tab", "001", 
                "Vue d'ensemble onglet Chemins d'accès", 
                "Configuration du SDK et des éditeurs")}
            
            <p>Cet onglet vous permet de configurer les <strong>chemins vers les outils externes</strong> utilisés par RenExtract.</p>
            
            <h3>🛠️ SDK Ren'Py</h3>
            
            {generator._get_image_html("07_tab_settings/paths_tab", "002", 
                "Section SDK Ren'Py", 
                "Configuration du chemin vers le SDK")}
            
            <h4>📦 Qu'est-ce que le SDK ?</h4>
            <p>Le <strong>SDK Ren'Py</strong> (Software Development Kit) est l'ensemble d'outils de développement Ren'Py.</p>
            <p>RenExtract intègre un <strong>SDK custom</strong> qui gère la plupart des opérations. Vous ne devriez configurer le SDK officiel 
            <strong>que si l'application échoue</strong> à gérer certaines tâches. ⚠️ Si le SDK externe est configuré, il sera toujours utilisé en priorité.</p>
            <p><strong>Chemin requis :</strong> Le dossier contenant <code>renpy.exe</code></p>
            <p><strong>Exemple :</strong> <code>C:\\Ren'Py\\renpy-8.1.3-sdk\\</code></p>
            
            <h4>📝 Configuration du SDK</h4>
            <ol style="margin-left: 40px;">
                <li>Cliquez sur le bouton <strong>"📁 Parcourir"</strong></li>
                <li>Naviguez jusqu'au dossier contenant le SDK Ren'Py</li>
                <li>Sélectionnez le dossier (pas le fichier <code>renpy.exe</code> directement !)</li>
                <li>Le chemin est automatiquement sauvegardé</li>
            </ol>
            
            <h4>💡 Télécharger le SDK</h4>
            <p>Si vous n'avez pas encore le SDK Ren'Py, téléchargez-le depuis <a href="https://www.renpy.org/release_list.html" target="_blank" style="color: var(--accent); text-decoration: underline;"><strong>renpy.org/release_list</strong></a> et installez-le dans un dossier accessible.</p>
            
            <h3>✏️ Éditeur personnalisé</h3>
            
            {generator._get_image_html("07_tab_settings/paths_tab", "003", 
                "Section Éditeur personnalisé", 
                "Configuration d'un éditeur de code personnalisé")}
            
            <h4>📝 Pourquoi un éditeur personnalisé ?</h4>
            <p>Un éditeur de code dédié (VS Code, Sublime Text, Notepad++...) offre de nombreux avantages :</p>
            <ul style="margin-left: 40px;">
                <li>✅ <strong>Coloration syntaxique</strong> : Meilleure lecture du code</li>
                <li>✅ <strong>Fonctionnalités avancées</strong> : Recherche/remplacement, multi-curseur, etc.</li>
                <li>✅ <strong>Extensions</strong> : Support Ren'Py, outils de traduction...</li>
            </ul>
            
            <h4>📝 Configuration de l'éditeur</h4>
            <ol style="margin-left: 40px;">
                <li>Entrez le chemin manuellement dans le champ <strong>Entry</strong> ou cliquez sur <strong>"📁 Parcourir"</strong></li>
                <li>Sélectionnez l'exécutable de votre éditeur (ex: <code>Code.exe</code> pour VS Code)</li>
                <li>Utilisez le bouton <strong>"🧪 Test"</strong> pour vérifier que le chemin est valide</li>
                <li>Le nom de l'éditeur est détecté automatiquement</li>
                <li>Il apparaîtra dans la liste des éditeurs de l'onglet "Interface & Application"</li>
            </ol>
            
            <h4>🔄 Réinitialiser</h4>
            <p>Le bouton <strong>"Réinitialiser"</strong> efface les chemins personnalisés du SDK et de l'éditeur. 
            Les valeurs par défaut seront restaurées.</p>
            
            <div class="tip-box">
                <h4>💡 Besoin d'aide ?</h4>
                <p>Pour accéder à cette fenêtre d'aide directement depuis l'application, cliquez sur le bouton <strong>"À quoi ça sert ?"</strong> 
                présent dans l'onglet Chemins d'accès. Vous y trouverez toutes les explications détaillées sur la configuration du SDK et de votre éditeur préféré.</p>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 6 : FOOTER
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_6 = f"""
        <div class="section" id="footer-parametres">
            <h2>📋 Footer et Actions Globales</h2>
            
            <p>En bas de la fenêtre des paramètres, vous trouverez <strong>3 boutons</strong> toujours accessibles, 
            quel que soit l'onglet actif.</p>
            
            {generator._get_image_html("07_tab_settings", "002", 
                "Footer avec boutons", 
                "Barre de footer avec À propos, Par défaut et Fermer")}
            
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="info-box" style="margin: 0;">
                    <h4>ℹ️ À propos</h4>
                    <p>Affiche les informations sur RenExtract : version, fonctionnalités, et copyright.</p>
                </div>
                
                <div class="tip-box" style="margin: 0;">
                    <h4>🔄 Par défaut</h4>
                    <p>Remet <strong>tous les paramètres</strong> de tous les onglets à leurs valeurs par défaut. 
                    Une confirmation vous sera demandée.</p>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>❌ Fermer</h4>
                    <p>Ferme la fenêtre et <strong>sauvegarde automatiquement</strong> tous vos changements.</p>
                </div>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 7 : CONCLUSION
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_7 = ""
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ASSEMBLAGE FINAL
    # ═══════════════════════════════════════════════════════════════════════════
    
    return (
        navigation +
        section_1 +
        section_2 +
        section_3 +
        section_4 +
        section_5 +
        section_6 +
        section_7
    )
