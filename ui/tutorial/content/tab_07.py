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
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-top: 15px;">
                
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
                
                <a href="#notifications-parametres" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🔔 Notifications</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Toasts et messages</div>
                </a>
                
                <a href="#astuces-parametres" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">💡 Astuces</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Bonnes pratiques</div>
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
            
            <p>Cette interface te permet de :</p>
            <ul>
                <li>🎨 <strong>Personnaliser l'apparence</strong> : Mode sombre, couleurs des boutons, thèmes</li>
                <li>🛡️ <strong>Configurer les protections</strong> : Patterns personnalisés, détection doublons</li>
                <li>🛠️ <strong>Définir les chemins</strong> : SDK Ren'Py, éditeurs de code</li>
                <li>⚙️ <strong>Ajuster le comportement</strong> : Ouvertures auto, notifications, modes de sauvegarde</li>
            </ul>
            
            <div class="info-box">
                <h4>🏗️ Structure de l'interface</h4>
                <p>L'interface est organisée en <strong>4 onglets principaux</strong> :</p>
                <ol>
                    <li><strong>🎨 Interface & Application</strong> : Configuration du comportement et de l'apparence</li>
                    <li><strong>🛡️ Extraction & Protection</strong> : Gestion des patterns et options d'extraction</li>
                    <li><strong>🎨 Couleurs des boutons</strong> : Personnalisation complète des couleurs</li>
                    <li><strong>🛠️ Chemins d'accès</strong> : Configuration du SDK et des éditeurs</li>
                </ol>
            </div>
            
            <div class="tip-box">
                <h4>💡 Sauvegarde automatique</h4>
                <p>Tous vos changements sont <strong>sauvegardés automatiquement</strong> lorsque vous fermes la fenêtre. 
                Tu recevras une notification de confirmation "✅ Tous les paramètres ont été sauvegardés".</p>
            </div>
            
            <div class="info-box">
                <h4>🔑 Accès rapide</h4>
                <p>Pour ouvrir les paramètres, cliquez sur le bouton "⚙️ Paramètres" dans le header de RenExtract.</p>
                {generator._get_image_html("07_tab_settings", "001", 
                    "Bouton d'accès aux paramètres", 
                    "Accès aux paramètres depuis l'interface principale")}
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
            
            <div class="info-box">
                <h4>🔧 Configuration des ouvertures</h4>
                <p>Ces options te permettent de choisir ce qui s'ouvre automatiquement après certaines actions :</p>
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
            </div>
            
            <h3>🎨 Apparence et notifications</h3>
            
            {generator._get_image_html("07_tab_settings/applications_tab", "003", 
                "Section apparence et notifications", 
                "Configuration du mode sombre, notifications et debug")}
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="info-box" style="margin: 0;">
                    <h4>🔔 Mode de notification</h4>
                    <p>Choisissez comment RenExtract te notifie des résultats :</p>
                    <ul>
                        <li><strong>Statut seulement</strong> : Notifications discrètes dans la barre de statut</li>
                        <li><strong>Popups détaillés</strong> : Fenêtres de confirmation avec détails complets</li>
                    </ul>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>🌙 Mode sombre</h4>
                    <p>Activez ou désactivez le thème sombre de l'interface.</p>
                    <p>✅ <strong>Recommandé :</strong> Mode sombre activé pour réduire la fatigue oculaire lors de longues sessions de travail.</p>
                </div>
            </div>
            
            <div class="warning-box">
                <h4>🐛 Mode debug</h4>
                <p>Le mode debug affiche des informations techniques détaillées dans les logs. 
                <strong>⚠️ Attention :</strong> Ce mode peut ralentir l'application. Activez-le uniquement si vous rencontres des problèmes ou si un développeur te le demande.</p>
            </div>
            
            <h3>📝 Éditeur de code</h3>
            
            {generator._get_image_html("07_tab_settings/applications_tab", "004", 
                "Section éditeur de code", 
                "Sélection de l'éditeur de code par défaut")}
            
            <div class="info-box">
                <h4>🔧 Choix de l'éditeur</h4>
                <p>Définis quel éditeur de code utiliser pour ouvrir les fichiers (uniquement lié au rapport de nettoyage et à l'éditeur en temps réel) :</p>
                <ul>
                    <li><strong>Défaut Windows</strong> : Utilisez le programme par défaut du système</li>
                    <li><strong>Éditeur détecté</strong> : Si vous as configuré un éditeur personnalisé dans l'onglet "Chemins d'accès", il apparaîtra ici</li>
            </ul>
        </div>
        
            <h3>🤖 Graq AI</h3>
            
            {generator._get_image_html("07_tab_settings/applications_tab", "005", 
                "Section Graq AI", 
                "Configuration de l'intégration Graq AI avec bouton d'aide")}
            
            <div class="info-box">
                <h4>🔧 Configuration Graq AI</h4>
                <p>Cette section te permet de configurer l'intégration avec Graq AI pour l'assistance à la traduction.</p>
                <p><strong>💡 Documentation complète :</strong> Une documentation précise est disponible en appuyant sur le bouton d'aide de cette section.</p>
            </div>
            
            <h3>⚙️ Actions système</h3>
            
            {generator._get_image_html("07_tab_settings/applications_tab", "006", 
                "Section actions système", 
                "Boutons de nettoyage et réinitialisation")}
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="tip-box" style="margin: 0;">
                    <h4>🧹 Nettoyer les fichiers temporaires</h4>
                    <p>Supprime certains fichiers temporaires créés par RenExtract (cache de l'interface, fichiers de session...).</p>
                    <p>💡 <strong>Astuce :</strong> Fais ceci régulièrement pour libérer de l'espace disque.</p>
                </div>
                
                <div class="warning-box" style="margin: 0;">
                    <h4>🔄 Réinitialiser l'application</h4>
                    <p><strong>⚠️ Action irréversible !</strong></p>
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
            
            <p>Cet onglet te permet de configurer finement le <strong>processus d'extraction</strong> et les <strong>protections automatiques</strong> 
            qui préservent vos codes Ren'Py lors de la traduction.</p>
            
            <h3>🛡️ Options de protection + Limite + Mode de sauvegarde</h3>
            
            {generator._get_image_html("07_tab_settings/extraction_tab", "002", 
                "Sections options, limite et mode sauvegarde regroupées", 
                "Options de protection, limite de lignes et mode de sauvegarde")}
            
            <div class="info-box">
                <h4>🔧 Options de protection</h4>
                <ul>
                    <li><strong>🔍 Détecter et gérer les doublons</strong> : Évite les traductions en double (recommandé)</li>
                    <li><strong>📊 Suivi de progression</strong> : Surveille l'avancement de vos projets de traduction</li>
                    <li><strong>⚙️ Paramètres cohérence</strong> : Ouvre une fenêtre pour configurer les vérifications (voir ci-dessous)</li>
                </ul>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="info-box" style="margin: 0;">
                    <h4>📄 Limite de lignes par fichier</h4>
                    <p>Définit le nombre maximum de lignes par fichier extrait.</p>
                    <p><strong>Exemple :</strong> <code>1000</code> = fichiers de max 1000 lignes</p>
                    <p>💡 Laisse vide pour aucune limite.</p>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>💾 Mode de sauvegarde</h4>
                    <p>Choisissez comment les fichiers sont enregistrés :</p>
                    <ul>
                        <li><strong>Écraser l'original</strong> : Remplace le fichier existant</li>
                        <li><strong>Créer nouveau fichier</strong> : Génère un fichier <code>&lt;File_Name&gt;_translated.rpy</code></li>
                    </ul>
                </div>
            </div>
            
            <h3>⚙️ Paramètres de cohérence</h3>
            
            {generator._get_image_html("07_tab_settings/extraction_tab", "004", 
                "Bouton paramètres cohérence", 
                "Accès aux paramètres de vérification de cohérence")}
            
            <div class="info-box">
                <h4>✅ Configuration des vérifications</h4>
                <p>Cette fenêtre te permet de choisir quelles vérifications seront effectuées lors du <strong>contrôle de cohérence après reconstruction</strong>. 
                Ces vérifications sont différentes des cases cochées dans l'onglet Actions de l'interface principale.</p>
                <p><strong>8 types de vérifications disponibles :</strong></p>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1rem 0;">
                    <div>
                        <ul>
                            <li>Variables incohérentes</li>
                            <li>Doublons détectés</li>
                            <li>Traductions manquantes</li>
                            <li>Traductions inutilisées</li>
                        </ul>
                    </div>
                    <div>
                        <ul>
                            <li>Blocs vides</li>
                            <li>Textes non traduits</li>
                            <li>Incohérences de formatage</li>
                            <li>Problèmes d'encodage</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="tip-box">
                <h4>💡 Boutons rapides</h4>
                <ul>
                    <li><strong>✅ Tout sélectionner</strong> : Activez toutes les vérifications (recommandé pour une analyse complète)</li>
                    <li><strong>❌ Tout désélectionner</strong> : Désactivez toutes les vérifications</li>
                    <li><strong>💾 Sauvegarder</strong> : Sauvegarde votre configuration et ferme automatiquement la fenêtre</li>
                </ul>
            </div>
            
            <h3>🔧 Patterns de protection</h3>
            
            {generator._get_image_html("07_tab_settings/extraction_tab", "003", 
                "Patterns avec incrémentation visible", 
                "Exemples de patterns personnalisés montrant clairement l'incrémentation automatique")}
            
            <p>Les patterns sont des <strong>placeholders personnalisés</strong> qui protègent vos codes Ren'Py lors de l'extraction. 
            Ils remplacent temporairement les codes, variables et caractères spéciaux pour éviter au maximum qu'ils soient modifiés par les outils de traduction. 
            N'étant pas fiable à 100%, par sécurité un rapport de cohérence est généré après reconstruction pour signaler les erreurs.</p>
            
            <div class="info-box">
                <h4>🛡️ Les 3 types de patterns</h4>
                <div style="margin-bottom: 15px;">
                    <p><strong>🔧 Pattern Codes/Variables</strong></p>
                    <p>Protège les codes de jeu et variables Ren'Py.</p>
                    <p><strong>Exemple :</strong> <code>RENPY_CODE_001</code></p>
                </div>
                <div style="margin-bottom: 15px;">
                    <p><strong>⭐ Pattern Astérisques & 〰️ Pattern Tildes</strong></p>
                    <p>Ces deux patterns ont <strong>la même utilité</strong> : protéger les mots ou phrases entourés d'astérisques 
                    (<code>*exemple*</code>) et les extraire dans un fichier séparé pour éviter qu'ils soient traduits.</p>
                    <p><strong>Exemples :</strong> <code>RENPY_ASTERISK_001</code>, <code>RENPY_TILDE_001</code></p>
                </div>
            </div>
            
            <div class="tip-box">
                <h4>🎯 Aperçu temps réel et incrémentation</h4>
                <p>Chaque pattern affiche un <strong>aperçu en temps réel</strong> montrant comment les placeholders seront générés. 
                L'image ci-dessus montre des exemples concrets :</p>
                <ul>
                    <li><code>(01)</code> → <code>(01), (02), (03)</code> : Pattern simple avec chiffres</li>
                    <li><code>(B1)-1</code> → <code>(B1)-1, (B1)-2, (B1)-3</code> : Pattern avec lettre, chiffre et tiret</li>
                    <li><code>(C1)1</code> → <code>(C1)1_001, (C1)1_002, (C1)1_003</code> : Pattern avec suffixe numérique</li>
                </ul>
                <p>💡 <strong>L'incrémentation s'adapte intelligemment</strong> à votre pattern ! Elle détecte automatiquement les chiffres et génère 
                la suite logique pour chaque code protégé.</p>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="info-box" style="margin: 0;">
                    <h4>🧪 Tester les patterns</h4>
                    <p>Le bouton <strong>"🧪 Tester"</strong> vérifiez :</p>
                    <ul>
                        <li>✅ <strong>Tous les patterns sont valides</strong></li>
                        <li>❌ <strong>X Doublons détectés :</strong> (placeholders) 
                            <br><small>💡 Une notification signale en direct la détection des doublons avant le test</small></li>
                    </ul>
                </div>
                
                <div class="tip-box" style="margin: 0;">
                    <h4>🔄 Remettre par défaut</h4>
                    <p>Le bouton <strong>"🔄 Défaut"</strong> restaure les patterns recommandés :</p>
                    <ul>
                        <li><code>RENPY_CODE_001</code></li>
                        <li><code>RENPY_ASTERISK_001</code></li>
                        <li><code>RENPY_TILDE_001</code></li>
                    </ul>
                </div>
            </div>
            
            <div class="warning-box">
                <h4>⚠️ Règles importantes</h4>
                <ul>
                    <li><strong>Pas de doublons</strong> : Les 3 patterns doivent être différents</li>
                    <li><strong>Évite les caractères protégés</strong> : N'utilisez pas de caractères que RenExtract tente déjà de protéger comme <code>[ ] {{ }} \\ /</code>, etc. Reste sur des lettres, chiffres et underscore pour éviter les conflits.</li>
                    <li><strong>Suffixe numérique recommandé</strong> : Termine par <code>_001</code> pour faciliter l'incrémentation automatique (voir aperçu temps réel pour comprendre son utilité).</li>
            </ul>
        </div>
        
            <h3>📚 Aide complète - Extraction & Protection</h3>
            
            <div class="tip-box">
                <h4>💡 Besoin d'aide ?</h4>
                <p>Pour accéder à cette fenêtre d'aide directement depuis l'application, cliquez sur le bouton <strong>"À quoi ça sert ?"</strong> 
                présent dans l'onglet Extraction & Protection. Tu y trouveras toutes les explications détaillées sur chaque option.</p>
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
            
            <p>Cet onglet te permet de <strong>personnaliser complètement les couleurs</strong> de tous les boutons de RenExtract. 
            Tu peux utiliser des <strong>presets prédéfinis</strong> ou créer votre propre palette personnalisée !</p>
            
            <h3>🎨 Presets de couleurs</h3>
            
            {generator._get_image_html("07_tab_settings/colors_tab", "002", 
                "Section presets et bouton reset", 
                "Sélection de presets et bouton de réinitialisation")}
            
            <div class="info-box">
                <h4>✨ Utiliser un preset</h4>
                <p>Les presets sont des <strong>combinaisons de couleurs prédéfinies</strong> harmonieuses et testées.</p>
                <ol>
                    <li>Sélectionnez un preset dans la liste déroulante</li>
                    <li>Cliquez sur <strong>"✅ Appliquer le preset"</strong></li>
                    <li>Les couleurs sont appliquées</li>
                </ol>
                <p><strong>💡 Recommandation :</strong> Pour que les changements de couleurs soient parfaitement visibles, 
                il est recommandé de <strong>fermer et rouvrir l'application</strong> après l'application d'un preset.</p>
            </div>
            
            <div class="tip-box">
                <h4>🔄 Remettre par défaut</h4>
                <p>Le bouton <strong>"Par défaut"</strong> restaure les couleurs d'origine de RenExtract. 
                Une confirmation te sera demandée car cette action supprime toutes vos personnalisations.</p>
            </div>
            
            <h3>🖌️ Personnalisation des couleurs</h3>
            
            {generator._get_image_html("07_tab_settings/colors_tab", "003", 
                "Grille des boutons colorés", 
                "8 boutons de couleur personnalisables")}
            
            <p>Tu peux personnaliser <strong>8 types de boutons</strong> différents :</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="info-box" style="margin: 0;">
                    <ul>
                        <li>🔵 <strong>Bouton principal</strong> : Actions principales (Extraire, Reconstruire)</li>
                        <li>🟢 <strong>Bouton secondaire</strong> : Actions secondaires (Sauvegarder)</li>
                        <li>🟣 <strong>Bouton tertiaire</strong> : Actions alternatives</li>
                        <li>🔴 <strong>Bouton danger</strong> : Actions destructives (Supprimer)</li>
                    </ul>
                </div>
                <div class="info-box" style="margin: 0;">
                    <ul>
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
            
            <div class="step-box">
                <h4>📝 Étapes pour changer une couleur</h4>
                <ol>
                    <li>Cliquez sur le bouton de couleur que vous veux modifier</li>
                    <li>Une fenêtre de sélection de couleur s'ouvre</li>
                    <li>Choisissez votre nouvelle couleur (palette, hexadécimal, RGB...)</li>
                    <li>Valide votre sélection</li>
                    <li>La couleur est appliquée</li>
                </ol>
                <p><strong>💡 Recommandation :</strong> Comme pour les presets, il est recommandé de <strong>fermer et rouvrir l'application</strong> 
                pour que les changements de couleurs soient parfaitement appliqués partout.</p>
            </div>
            
            <div class="tip-box">
                <h4>💡 Astuces couleurs</h4>
                <ul>
                    <li><strong>Contraste :</strong> Choisissez des couleurs suffisamment contrastées pour une bonne lisibilité</li>
                    <li><strong>Cohérence :</strong> Utilisez une palette harmonieuse (couleurs complémentaires ou analogues)</li>
                    <li><strong>Accessibilité :</strong> Évite les combinaisons difficiles à lire (ex: jaune sur blanc)</li>
                    <li><strong>Test :</strong> Teste vos couleurs sur différentes parties de l'interface avant de valider</li>
            </ul>
            </div>
            
            <h3>📚 Aide complète - Personnalisation des couleurs</h3>
            
            <div class="tip-box">
                <h4>💡 Besoin d'aide ?</h4>
                <p>Pour accéder à cette fenêtre d'aide directement depuis l'application, cliquez sur le bouton <strong>"À quoi ça sert ?"</strong> 
                présent dans l'onglet Couleurs des boutons. Tu y trouveras le détail complet de chaque catégorie de boutons.</p>
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
            
            <p>Cet onglet te permet de configurer les <strong>chemins vers les outils externes</strong> utilisés par RenExtract.</p>
            
            <h3>🛠️ SDK Ren'Py</h3>
            
            {generator._get_image_html("07_tab_settings/paths_tab", "002", 
                "Section SDK Ren'Py", 
                "Configuration du chemin vers le SDK")}
            
            <div class="info-box">
                <h4>📦 Qu'est-ce que le SDK ?</h4>
                <p>Le <strong>SDK Ren'Py</strong> (Software Development Kit) est l'ensemble d'outils de développement Ren'Py.</p>
                <p>RenExtract intègre un <strong>SDK custom</strong> qui gère la plupart des opérations. Tu ne devrais configurer le SDK officiel 
                <strong>que si l'application échoue</strong> à gérer certaines tâches. ⚠️ Si le SDK externe est configuré, il sera toujours utilisé en priorité.</p>
                <p><strong>Chemin requis :</strong> Le dossier contenant <code>renpy.exe</code></p>
                <p><strong>Exemple :</strong> <code>C:\\Ren'Py\\renpy-8.1.3-sdk\\</code></p>
            </div>
            
            <div class="step-box">
                <h4>📝 Configuration du SDK</h4>
                <ol>
                    <li>Cliquez sur le bouton <strong>"📁 Parcourir"</strong></li>
                    <li>Navigue jusqu'au dossier contenant le SDK Ren'Py</li>
                    <li>Sélectionnez le dossier (pas le fichier <code>renpy.exe</code> directement !)</li>
                    <li>Le chemin est automatiquement sauvegardé</li>
                </ol>
            </div>
            
            <div class="tip-box">
                <h4>💡 Télécharger le SDK</h4>
                <p>Si vous n'as pas encore le SDK Ren'Py, télécharge-le depuis <a href="https://www.renpy.org/release_list.html" target="_blank" style="color: var(--accent); text-decoration: underline;"><strong>renpy.org/release_list</strong></a> et installe-le dans un dossier accessible.</p>
            </div>
            
            <h3>✏️ Éditeur personnalisé</h3>
            
            {generator._get_image_html("07_tab_settings/paths_tab", "003", 
                "Section Éditeur personnalisé", 
                "Configuration d'un éditeur de code personnalisé")}
            
            <div class="info-box">
                <h4>📝 Pourquoi un éditeur personnalisé ?</h4>
                <p>Un éditeur de code dédié (VS Code, Sublime Text, Notepad++...) offre de nombreux avantages :</p>
                <ul>
                    <li>✅ <strong>Coloration syntaxique</strong> : Meilleure lecture du code</li>
                    <li>✅ <strong>Fonctionnalités avancées</strong> : Recherche/remplacement, multi-curseur, etc.</li>
                    <li>✅ <strong>Extensions</strong> : Support Ren'Py, outils de traduction...</li>
            </ul>
        </div>
        
            <div class="step-box">
                <h4>📝 Configuration de l'éditeur</h4>
                <ol>
                    <li>Entre le chemin manuellement dans le champ <strong>Entry</strong> ou cliquez sur <strong>"📁 Parcourir"</strong></li>
                    <li>Sélectionnez l'exécutable de votre éditeur (ex: <code>Code.exe</code> pour VS Code)</li>
                    <li>Utilisez le bouton <strong>"🧪 Test"</strong> pour vérifier que le chemin est valide</li>
                    <li>Le nom de l'éditeur est détecté automatiquement</li>
                    <li>Il apparaîtra dans la liste des éditeurs de l'onglet "Interface & Application"</li>
                </ol>
            </div>
            
            <h3>🔔 Notifications de validation</h3>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="warning-box" style="margin: 0;">
                    <h4>⚠️ Aucun chemin configuré</h4>
                    <p>Si vous testes un éditeur sans avoir configuré de chemin, vous verras un message d'avertissement.</p>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>✅ Chemin valide</h4>
                    <p>Quand le chemin est valide, vous reçois une confirmation.</p>
                </div>
            </div>
            
            <div class="tip-box">
                <h4>🔄 Réinitialiser</h4>
                <p>Le bouton <strong>"Réinitialiser"</strong> efface les chemins personnalisés du SDK et de l'éditeur. 
                Les valeurs par défaut seront restaurées.</p>
            </div>
            
            <h3>📚 Aide complète - Chemins d'accès</h3>
            
            <div class="tip-box">
                <h4>💡 Besoin d'aide ?</h4>
                <p>Pour accéder à cette fenêtre d'aide directement depuis l'application, cliquez sur le bouton <strong>"À quoi ça sert ?"</strong> 
                présent dans l'onglet Chemins d'accès. Tu y trouveras toutes les explications détaillées sur la configuration du SDK et de votre éditeur préféré.</p>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 6 : FOOTER
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_6 = f"""
        <div class="section" id="footer-parametres">
            <h2>📋 Footer et Actions Globales</h2>
            
            <p>En bas de la fenêtre des paramètres, vous trouveras <strong>3 boutons</strong> toujours accessibles, 
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
                    Une confirmation te sera demandée.</p>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>❌ Fermer</h4>
                    <p>Ferme la fenêtre et <strong>sauvegarde automatiquement</strong> tous vos changements.</p>
                </div>
            </div>
            
            <h3>ℹ️ Fenêtre À propos</h3>
            
            <div class="info-box">
                <h4>📊 Informations affichées</h4>
                <ul>
                    <li><strong>Nom</strong> : RenExtract - Générateur de Traductions Ren'Py</li>
                    <li><strong>Version</strong> : Version actuelle de l'application</li>
                    <li><strong>Description</strong> : "Développé avec ❤️ pour la communauté Ren'Py"</li>
                    <li><strong>Technologies</strong> : Application développée en Python avec Tkinter pour l'interface graphique</li>
                    <li><strong>Copyright</strong> : © 2024 RenExtract Project</li>
                </ul>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 7 : NOTIFICATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_7 = f"""
        <div class="section" id="notifications-parametres">
            <h2>🔔 Notifications et Toasts</h2>
            
            <p>RenExtract utilisez des <strong>notifications toast</strong> (petits messages temporaires) pour te tenir informé 
            des actions effectuées et des résultats. Voici les principaux types que vous rencontreras dans les paramètres.</p>
            
            <h3>✅ Toasts de succès</h3>
            
            <div class="info-box">
                <h4>💚 Actions confirmées</h4>
                <p>Les toasts <strong>verts</strong> indiquent qu'une action s'est déroulée avec succès :</p>
                <ul>
                    <li>"✅ Tous les paramètres ont été sauvegardés" (à la fermeture)</li>
                    <li>"✅ [Éditeur] : Chemin valide" (après validation d'un chemin)</li>
                    <li>"✅ Preset appliqué" (après application d'un preset de couleurs)</li>
                    <li>"✅ Paramètres remis par défaut" (après reset)</li>
            </ul>
            </div>
            
            <h3>⚠️ Toasts d'avertissement</h3>
            
            <div class="warning-box">
                <h4>🟠 Attention requise</h4>
                <p>Les toasts <strong>jaune orangé</strong> signalent des problèmes non-bloquants qui nécessitent votre attention :</p>
                <ul>
                    <li>"⚠️ Attention: doublons détectés" (patterns identiques)</li>
                    <li>"⚠️ Aucun chemin configuré pour [Éditeur]" (test d'un chemin vide)</li>
                    <li>"⚠️ Limite très élevée (>100k)" (limite de lignes excessive)</li>
            </ul>
            </div>
            
            <div class="tip-box">
                <h4>💡 Réagir aux avertissements</h4>
                <p>Les avertissements ne bloquent pas l'utilisation de RenExtract, mais il est <strong>recommandé de les corriger</strong> 
                pour éviter des problèmes futurs. Par exemple, des patterns en double peuvent causer des erreurs lors de l'extraction.</p>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 8 : ASTUCES
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_8 = f"""
        <div class="section" id="astuces-parametres">
            <h2>💡 Astuces et Bonnes Pratiques</h2>
            
            <p>Voici quelques conseils pour <strong>optimiser votre configuration</strong> de RenExtract :</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                
                <div class="tip-box" style="margin: 0;">
                    <h4>🎨 Configuration initiale</h4>
                    <ul>
                        <li>Activez le <strong>mode sombre</strong> pour le confort visuel</li>
                        <li>Configurez votre <strong>éditeur préféré</strong> dès le départ</li>
                        <li>Choisissez un <strong>preset de couleurs</strong> qui te plaît</li>
                        <li>Activez les <strong>ouvertures automatiques</strong> selon vos besoins</li>
                    </ul>
                </div>
                
                <div class="tip-box" style="margin: 0;">
                    <h4>🛡️ Protection optimale</h4>
                    <ul>
                        <li><strong>Garde les patterns par défaut</strong> sauf besoin spécifique</li>
                        <li>Activez la <strong>détection des doublons</strong></li>
                        <li>Configurez les <strong>vérifications de cohérence</strong> selon votre workflow</li>
                        <li>Teste vos patterns avant de les utiliser en production</li>
                    </ul>
                </div>
                
                <div class="tip-box" style="margin: 0;">
                    <h4>🎨 Personnalisation</h4>
                    <ul>
                        <li>Utilisez les <strong>presets</strong> comme base avant de personnaliser</li>
                        <li>Teste vos couleurs sur <strong>différentes actions</strong></li>
                        <li>Garde un <strong>bon contraste</strong> pour la lisibilité</li>
                        <li>N'hésite pas à <strong>remettre par défaut</strong> si vous n'es pas satisfait</li>
                    </ul>
                </div>
                
                <div class="tip-box" style="margin: 0;">
                    <h4>🛠️ Chemins et outils</h4>
                    <ul>
                        <li>Configurez le <strong>SDK Ren'Py</strong> si vous fais de la compilation</li>
                        <li>Teste les chemins avec le <strong>bouton Test</strong></li>
                        <li>Utilisez un <strong>éditeur moderne</strong> (VS Code, Sublime...)</li>
                        <li>Garde les chemins à jour après les mises à jour d'outils</li>
            </ul>
                </div>
                
            </div>
            
            <div class="info-box">
                <h4>🔄 Workflow recommandé</h4>
                <ol>
                    <li><strong>Première utilisation</strong> : Configurez les paramètres de base (éditeur, couleurs, SDK)</li>
                    <li><strong>Avant chaque projet</strong> : Vérifiez que vos patterns et vérifications sont adaptés</li>
                    <li><strong>Régulièrement</strong> : Nettoie les fichiers temporaires et vérifiez les chemins</li>
                    <li><strong>En cas de problème</strong> : Activez le mode debug et consulte les logs</li>
                </ol>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 9 : CONCLUSION
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_9 = ""
    
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
        section_7 +
        section_8 +
        section_9
    )
