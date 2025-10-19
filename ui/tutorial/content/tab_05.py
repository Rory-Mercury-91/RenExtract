# ui/tutorial/content/tab_05.py
"""
Module de contenu pour l'onglet 5 : Outils Spécialisés
Version française uniquement
"""

def generate_content(generator):
    """
    Génère le contenu pour l'onglet 5 : Outils Spécialisés
    
    Args:
        generator: Instance du générateur avec méthodes utilitaires
    
    Returns:
        str: HTML généré pour l'onglet outils spécialisés
    """
    
    return f"""
        <!-- Navigation rapide -->
        <div class="quick-nav-section" style="background: var(--card-bg); padding: 20px; margin-bottom: 30px; border-radius: 8px; border-left: 4px solid var(--accent);">
            <h3>🧭 Navigation rapide</h3>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-top: 15px;">
                <a href="#introduction-outils" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🔧 Introduction</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Présentation des outils</div>
                </a>
                <a href="#nettoyage-intelligent" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🧹 Nettoyage Intelligent</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Suppression des traductions orphelines</div>
                </a>
                <a href="#editeur-temps-reel" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">⚡ Éditeur Temps Réel</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Modification en direct pendant le jeu</div>
                </a>
                <a href="#verification-coherence" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🧪 Vérification Cohérence</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Détection d'erreurs techniques</div>
                </a>
            </div>
            <style>
                .nav-card:hover {{
                    transform: translateY(-3px) !important;
                    box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
                    border-color: var(--accent) !important;
                    background: linear-gradient(135deg, var(--hdr) 0%, rgba(74, 144, 226, 0.1) 100%) !important;
                }}
                .nav-card:active {{
                    transform: translateY(-1px) !important;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.12) !important;
                }}
            </style>
        </div>
        
        <!-- Section Introduction -->
        <div class="section" id="introduction-outils">
            <h2>🔧 Outils Spécialisés</h2>
            <p>Les <strong>Outils Spécialisés</strong> regroupent trois fonctionnalités avancées pour maintenir et améliorer la qualité de vos traductions Ren'Py. Ils sont accessibles dans une interface dédiée qui partage le projet avec l'interface principale.</p>
            
            <h3>📍 Comment accéder aux outils</h3>
            {generator._get_image_html("05_tools", "001", 
                "Accès aux outils depuis l'interface principale", 
                "Bouton Outils Spécialisé dans l'onglet OUTILS")}
            
            <h4>🎯 Étapes d'accès</h4>
            <ol style="padding-left: 40px;">
                <li>Dans l'interface principale, cliquez sur l'onglet <strong>OUTILS</strong> (jaune)</li>
                <li>Cliquez sur le bouton <strong>🔧 Outils Spécialisé</strong></li>
                <li>Une nouvelle fenêtre s'ouvre avec les 3 outils disponibles</li>
            </ol>
            
            <h3 id="vue-ensemble-outils">📋 Configuration du projet</h3>
            {generator._get_image_html("05_tools", "002", 
                "Configuration du projet", 
                "Zone de sélection du projet commune à tous les onglets")}
            
            <p>La configuration du projet est <strong>synchronisée automatiquement</strong> avec l'interface principale. Vous n'avez pas besoin de resélectionner votre projet à chaque ouverture.</p>
            </div>
            
        <!-- Section 1 : Nettoyage Intelligent -->
        <div class="section" id="nettoyage-intelligent">
            <h2>🧹 Nettoyage Intelligent</h2>
            <p>Le <strong>Nettoyage Intelligent</strong> supprime automatiquement les <strong>traductions orphelines</strong> - ces blocs de traduction qui n'ont plus de correspondance dans les fichiers source du jeu après une mise à jour.</p>
            
            <h3>🖥️ Interface de nettoyage</h3>
            {generator._get_image_html("05_tools/clean", "001", 
                "Onglet Nettoyage - Vue complète", 
                "Interface complète du nettoyage avec projet sélectionné")}
            
            <h3>🎯 À quoi ça sert ?</h3>
            <div class="warning-box">
                <h4>⚠️ Problème des traductions orphelines</h4>
                <p>Quand un développeur met à jour son jeu, certains dialogues sont supprimés ou modifiés. Vos anciens fichiers de traduction gardent ces lignes obsolètes qui :</p>
                <ul>
                    <li>Alourdissent les fichiers de traduction (même si négligeable)</li>
                    <li>Rendent la navigation et la maintenance plus difficiles</li>
                </ul>
                <p><strong>Le nettoyage intelligent résout ce problème en un clic !</strong></p>
                </div>
            
            <h3>🚀 Workflow en 3 étapes</h3>
            <ol style="padding-left: 40px;">
                <li><strong>Sélectionner les langues</strong> : Choisissez les langues à nettoyer</li>
                <li><strong>Configurer les exclusions</strong> : Protégez les fichiers importants</li>
                <li><strong>Lancer le nettoyage</strong> : Cliquez sur "🧹 Démarrer le nettoyage"</li>
            </ol>
                
            <h3>💪 Double méthode de nettoyage</h3>
            <p>RenExtract utilise deux méthodes complémentaires pour un nettoyage optimal :</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 20px 0;">
                <div>
                    <h4>🎯 Nettoyage basé sur lint.txt</h4>
                    <p>Utilise l'analyse officielle du SDK Ren'Py pour détecter les IDs de traduction orphelins.</p>
                    <p><strong>Avantage :</strong> Précision maximale basée sur l'analyse officielle</p>
                </div>
                <div>
                    <h4>🔍 Nettoyage par correspondance</h4>
                    <p>Vérifie si les textes OLD existent encore dans les fichiers source du jeu.</p>
                    <p><strong>Note :</strong> Comme cette méthode n'est pas précise à 100%, les blocs détectés sont récupérés et fournis dans le rapport pour que vous puissiez les vérifier et les reprendre si besoin.</p>
                </div>
            </div>
                
            <h3 id="selection-langues-nettoyage">🌍 Sélection des langues</h3>
            <p>Les langues sont <strong>détectées automatiquement</strong> dès que vous sélectionnez un projet. Elles s'affichent dans une grille à 3 colonnes pour une lecture optimale.</p>
            
            {generator._get_image_html("05_tools/clean", "002", 
                "Grille de sélection des langues", 
                "Focus sur la zone : Langues à nettoyer")}
            
            <h4>📊 Organisation visuelle</h4>
            <ul>
                <li><strong>Icônes contextuelles</strong> : 🌐 pour English, 🗣️ pour les autres langues</li>
                <li><strong>Formatage automatique</strong> : Première lettre en majuscule</li>
                <li><strong>Détection automatique</strong> : Les langues apparaissent dès la sélection du projet</li>
                <li><strong>🎮 Contrôles rapides</strong> :
                    <ul style="padding-left: 40px;">
                        <li>• <strong>✅ Tout sélectionner</strong> : Coche toutes les langues d'un coup</li>
                        <li>• <strong>❌ Tout désélectionner</strong> : Décoche toutes les langues pour une sélection manuelle précise</li>
                    </ul>
                </li>
            </ul>
            
            <h3 id="exclusions-nettoyage">🚫 Exclusions de fichiers</h3>
            <p>Vous pouvez protéger certains fichiers du nettoyage en les ajoutant dans le champ <strong>"Fichiers à exclure"</strong>.</p>
            
            {generator._get_image_html("05_tools/clean", "003", 
                "Fichiers à exclure du nettoyage", 
                "Focus sur la zone : Fichiers à exclure du nettoyage")}
            
            <h4>📝 Fichiers protégés automatiquement</h4>
            <p><strong>Exclusions système</strong> (toujours actives) :</p>
            <ul style="padding-left: 40px;">
                <li>• <code>common.rpy</code> : Fichier système Ren'Py</li>
                <li>• <code>99_Z_Console.rpy</code> : Console développeur RenExtract</li>
                <li>• <code>99_Z_ScreenPreferences.rpy</code> : Écran préférences RenExtract</li>
                <li>• <code>99_Z_FontSystem.rpy</code> : Système de polices RenExtract</li>
            </ul>
            <p><strong>Valeur par défaut dans le champ :</strong> <code>common.rpy</code></p>
            <p>Vous pouvez ajouter vos propres fichiers (sélecteurs de langue, patches, menus personnalisés) en les séparant par des virgules.</p>
                
            <div class="warning-box">
                <h4>⚙️ Règles importantes</h4>
                <ul>
                    <li>Les <strong>fichiers système</strong> sont toujours protégés automatiquement (même s'ils ne sont pas dans votre liste)</li>
                    <li>La correspondance est <strong>exacte</strong> mais <strong>insensible à la casse</strong></li>
                    <li>Spécifiez toujours l'<strong>extension .rpy</strong></li>
                    <li>Les modifications sont <strong>sauvegardées automatiquement</strong></li>
                </ul>
            </div>
            
            <h3 id="processus-nettoyage">⚙️ Processus de nettoyage</h3>
            
            <h4>🔄 Étapes automatiques</h4>
            <ol style="padding-left: 40px;">
                <li><strong>Contrôle des prérequis</strong> : Vérification de l'absence de fichiers .rpa (invite à décompiler si détectés) et détection de traceback.txt dans le dossier du jeu (arrêt si présent)</li>
                <li><strong>Validation du SDK</strong> : Vérification ou téléchargement automatique</li>
                <li><strong>Génération du lint.txt</strong> : Analyse officielle Ren'Py avec surveillance du traceback.txt (arrêt immédiat si généré pendant l'exécution)</li>
                <li><strong>Analyse unifiée</strong> : Détection des orphelins avec double méthode</li>
                <li><strong>Sauvegarde & suppression</strong> : Backup unifié + nettoyage final</li>
            </ol>
                
            <h4>💡 Pendant le nettoyage</h4>
            <ul>
                <li>Un <strong>spinner animé</strong> indique que l'opération est en cours</li>
                <li>Le bouton principal est <strong>désactivé</strong> pour éviter les doublons</li>
                <li>Un bouton <strong>"ℹ️ Annuler l'opération"</strong> vous permet de stopper l'opération si besoin</li>
            </ul>
                
            <h3 id="resultats-nettoyage">📊 Résultats automatiques</h3>
            
            <p>À la fin du nettoyage, le <strong>rapport HTML s'ouvre automatiquement</strong> dans votre navigateur.</p>
            
            <h4>📄 Contenu du rapport</h4>
            <ul style="padding-left: 40px;">
                <li>• <strong>Métadonnées</strong> : Date, projet, langues traitées</li>
                <li>• <strong>Statistiques visuelles</strong> : Cartes avec chiffres clés, graphiques</li>
                <li>• <strong>Détails par fichier</strong> : Liste des fichiers nettoyés avec nombre de blocs supprimés</li>
                <li>• <strong>Thème adaptatif</strong> : Sombre/clair selon vos préférences</li>
            </ul>
                
            <h3 id="erreurs-nettoyage">⚠️ Messages d'erreur</h3>
            
            <p>Si vous oubliez de sélectionner des langues avant de lancer le nettoyage, un <strong>toast d'avertissement</strong> (orange) s'affiche en bas de la fenêtre pour vous le rappeler.</p>

            <div class="warning-box">
                <h4>⚠️ Points d'attention</h4>
                <ul>
                    <li>Le système crée une <strong>sauvegarde automatique du dossier de traduction complet</strong>, mais gardez vos propres backups importants</li>
                    <li><strong>Testez le jeu</strong> après le nettoyage pour vérifier que tout fonctionne</li>
                    <li><strong>Protégez vos fichiers modifiés manuellement</strong> en les ajoutant aux exclusions (comme les fichiers techniques de sélection de langue)</li>
                    <li>Le nettoyage est <strong>global par fichier</strong> (pas de récupération partielle)</li>
                </ul>
            </div>
            
            <h3 id="aide-nettoyage">❓ Aide contextuelle</h3>
            <p>Un bouton <strong>"À quoi ça sert ?"</strong> est disponible dans l'interface pour ouvrir une aide détaillée sur le nettoyage intelligent.</p>
        </div>

        <!-- Section 2 : Éditeur Temps Réel -->
        <div class="section" id="editeur-temps-reel">
            <h2>⚡ Éditeur Temps Réel</h2>
            <p>L'<strong>Éditeur Temps Réel</strong> vous permet de modifier les traductions <strong>pendant que le jeu fonctionne</strong>, sans le redémarrer. Idéal pour peaufiner rapidement des dialogues, ajuster des traductions trop longues, ou corriger des erreurs détectées en cours de jeu.</p>
            
            <h3>🎯 À quoi ça sert ?</h3>
            <div class="success-box">
                <h4>🚀 Révolution du workflow</h4>
                <p><strong>Terminé</strong> le cycle épuisant :</p>
                <ol style="padding-left: 40px;">
                    <li>Quitter le jeu</li>
                    <li>Modifier le fichier</li>
                    <li>Reconstruire les traductions</li>
                    <li>Relancer le jeu</li>
                </ol>
                <p><strong>Avec l'éditeur temps réel</strong> : Vous modifiez directement depuis le jeu et appuyez sur <strong>Maj+R</strong> pour voir les changements instantanément !</p>
            </div>
            
            <h3>🖥️ Vue d'ensemble</h3>
            {generator._get_image_html("05_tools/editor", "001", 
                "Onglet Éditeur Temps Réel", 
                "Interface complète de l'éditeur avec installation et surveillance")}
            
            <h4>🔧 Fonctionnement en 2 temps</h4>
            <ol style="padding-left: 40px;">
                <li><strong>Installation du module</strong> : Une seule fois par projet</li>
                <li><strong>Démarrage de la surveillance</strong> : À chaque session de traduction</li>
            </ol>
            
            <h3 id="installation-editeur">⚙️ Installation et configuration</h3>
            {generator._get_image_html("05_tools/editor", "002", 
                "Installation et surveillance", 
                "Focus sur la zone : Installation et surveillance")}
            
            <h4>🚀 Configuration en 3 étapes</h4>
            <ol style="padding-left: 40px;">
                <li><strong>Sélection de langue</strong> : Choisissez la langue à surveiller (ex: French, German)</li>
                <li><strong>Installation du module</strong> : Cliquez sur "🔧 Installer le module" (une seule fois)</li>
                <li><strong>Démarrage surveillance</strong> : Cliquez sur "🚀 Démarrer la surveillance" puis lancez votre jeu</li>
            </ol>
            
            <div class="tip-box">
                <h4>💡 Installation unique</h4>
                <p>Le module s'installe <strong>une seule fois</strong> dans <code>game/</code> et fonctionne pour <strong>toutes les langues</strong>. Il est automatiquement activé dès le lancement du jeu.</p>
            </div>
            
            <h3>⌨️ Raccourcis clavier essentiels</h3>
            <ul>
                <li><strong>Maj+R</strong> : Recharge les traductions (une fois par session, puis le jeu passe en autoreload)</li>
                <li><strong>F11</strong> : Retour en plein écran (si le jeu est passé en fenêtré avec F8)</li>
                <li><strong>F8</strong> : Ouvre l'éditeur si besoin (depuis le jeu quand un dialogue nécessite une correction)</li>
            </ul>

            <p><strong>Fonctionnement du raccourci F8 :</strong> Il a une double utilité selon le mode de jeu :</p>
            <ul style="padding-left: 40px;">
                <li>• <strong>En plein écran</strong> : Le jeu détecte le plein écran, passe en mode fenêtré, puis met RenExtract au premier plan</li>
                <li>• <strong>En mode fenêtré</strong> : Met directement la fenêtre RenExtract au premier plan (focus)</li>
            </ul>
            <p>La <strong>fenêtre principale de RenExtract</strong> (ou la <strong>fenêtre détachée</strong> si le mode détaché est actif) se met au premier plan pour que vous puissiez éditer. <strong>Utilisez F11</strong> dans le jeu pour revenir en plein écran après vos modifications.</p>
            
            <h3 id="edition-dialogue-simple">💬 Interface d'édition - Dialogues simples</h3>
            {generator._get_image_html("05_tools/editor", "004", 
                "Interface édition simple (mode détaché)", 
                "Vue de l'affichage : Dialogue simple")}
            
            <p>Pour les <strong>dialogues classiques</strong> avec un seul personnage, l'interface propose deux zones côte à côte :</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 20px 0;">
                <div>
                    <h4>📖 Zone VO (Version Originale)</h4>
                    <ul>
                        <li>Texte en <strong>lecture seule</strong></li>
                        <li>Sert de référence pour la traduction</li>
                    </ul>
                </div>
                <div>
                    <h4>🇫🇷 Zone VF (Version Française)</h4>
                    <ul>
                        <li>Texte <strong>éditable</strong></li>
                        <li>Zone d'édition avec texte en <strong>bleu</strong></li>
                        <li>Modifiez directement votre traduction ici</li>
                    </ul>
                </div>
            </div>
                
            <h3 id="edition-locuteur">🎭 Interface d'édition - Locuteur non défini</h3>
            {generator._get_image_html("05_tools/editor", "006", 
                "Interface locuteur non défini (mode détaché)", 
                "Vue de l'affichage : Locuteur + Dialogue")}
            
            <p>Pour les dialogues au format <code>"Nom" "Dialogue"</code>, l'interface se divise en <strong>deux zones distinctes</strong> :</p>
            
            <h4>📝 Édition en 2 parties</h4>
            <ol style="padding-left: 40px;">
                <li><strong>Zone Locuteur</strong> : VO et VF pour le nom du personnage</li>
                <li><strong>Zone Dialogue</strong> : VO et VF pour le texte du dialogue</li>
            </ol>
            <p><strong>Avantage :</strong> Édition séparée du nom et du dialogue pour plus de précision</p>
            
            <h3 id="edition-split">🔀 Interface d'édition - Dialogues divisés</h3>
            {generator._get_image_html("05_tools/editor", "005", 
                "Interface dialogues divisés (mode détaché)", 
                "Vue de l'affichage : Dialogue divisé")}
            
            <p>Pour les <strong>dialogues très longs</strong>, l'éditeur propose un <strong>mode divisé</strong> qui vous permet de diviser le texte en deux parties :</p>
            
            <h4>✂️ Division intelligente</h4>
            <ul>
                <li><strong>Partie 1/2</strong> : Première moitié du dialogue (fond bleu clair)</li>
                <li><strong>Partie 2/2</strong> : Seconde moitié du dialogue (fond normal)</li>
                <li><strong>Indicateur visuel</strong> : La partie active est surlignée</li>
                <li><strong>Bouton Fusionner</strong> : Pour revenir en mode simple</li>
                <li><strong>Détection voice</strong> : Détecte automatiquement les lignes avec fichiers vocaux (<code>voice "chemin/fichier.ogg"</code>)</li>
            </ul>
                
            <h4>💡 Quand utiliser le mode divisé ?</h4>
            <p>Le mode divisé est particulièrement utile pour :</p>
            <ul style="padding-left: 40px;">
                <li>• Les dialogues de narration très longs</li>
                <li>• Les descriptions détaillées</li>
                <li>• Les textes qui dépassent la limite d'affichage</li>
            </ul>
                
            <h3 id="edition-menu">🎯 Interface d'édition - Choix multiples</h3>
            {generator._get_image_html("05_tools/editor", "008", 
                "Interface choix multiples (mode détaché)", 
                "Vue de l'affichage : Choix")}
            
            <p>Pour les <strong>menus de choix</strong> du joueur, l'interface affiche une <strong>grille</strong> avec toutes les options :</p>
            
            <h4>📊 Organisation en grille</h4>
            <ul>
                <li>Chaque <strong>choix</strong> a sa propre zone VO/VF</li>
                <li>Un seul bouton <strong>"💾 Enregistrer tous les choix"</strong> sauvegarde tout d'un coup</li>
                <li>Théoriquement adapté pour plusieurs choix, mais vous devrez probablement agrandir la fenêtre selon le nombre de choix affichés</li>
            </ul>
            
            <h3 id="edition-multiple">🔢 Interface d'édition - Dialogues multiples</h3>
            {generator._get_image_html("05_tools/editor", "007", 
                "Interface dialogues multiples (mode détaché)", 
                "Vue de l'affichage : Dialogue multiple locuteur")}
            
            <p>Pour les <strong>dialogues multiples</strong> (plusieurs personnes qui parlent en même temps), l'interface affiche une <strong>liste verticale</strong> :</p>
            
            <h4>📝 Liste ordonnée</h4>
            <ul>
                <li>Chaque dialogue est numéroté et clairement séparé</li>
                <li>Édition individuelle de chaque ligne</li>
                <li>Un seul bouton <strong>"💾 Enregistrer tous"</strong> sauvegarde tout d'un coup</li>
            </ul>
                
            <h4>💡 Efficacité maximale</h4>
            <p>Le mode dialogues multiples est conçu pour :</p>
            <ul style="padding-left: 40px;">
                <li>• Les conversations à plusieurs personnages simultanément</li>
                <li>• Les dialogues qui se chevauchent</li>
                <li>• Les scènes de groupe avec plusieurs interlocuteurs</li>
            </ul>
                
            <h3 id="boutons-utilitaires">💡 Boutons utilitaires</h3>
            <p>Chaque zone de texte dans toutes les interfaces d'édition dispose de boutons pratiques :</p>
            <ul style="padding-left: 40px;">
                <li>• <strong>📋 Copier</strong> : Copie le texte VO dans le presse-papier</li>
                <li>• <strong>🌐 Traduire en ligne</strong> : Copie le texte VO et ouvre le traducteur sélectionné avec le texte pré-rempli selon la langue cible choisie (Note : DeepL ne supporte pas les textes avec des balises Ren'Py comme <code>{{/i}}</code>)</li>
                <li>• <strong>📝 Coller</strong> : Colle le contenu du presse-papier dans la zone VF</li>
            </ul>
            <p><strong>Traducteurs supportés :</strong> Google Translate, Yandex Translate, DeepL, Microsoft Translator, Groq AI</p>
            <p><strong>Langues cibles :</strong> Français, Anglais, Espagnol, Allemand, Italien, Portugais, Russe, Japonais, Chinois</p>
            <p><strong>Note :</strong> Le texte est automatiquement pré-rempli dans le traducteur selon la langue sélectionnée dans l'interface. Il est aussi copié dans le presse-papier comme backup.</p>
                
            <h3 id="mode-detache">🪟 Mode détaché</h3>
            <p>Les captures d'écran précédentes montrent l'éditeur en <strong>mode détaché</strong> - une fenêtre séparée de l'interface principale.</p>
            
            <h4>📐 Mode détaché vs Mode attaché</h4>
            <ul>
                <li><strong>Mode attaché</strong> : L'éditeur s'affiche dans l'onglet principal des outils</li>
                <li><strong>Mode détaché</strong> : L'éditeur s'ouvre dans une fenêtre séparée</li>
                <li><strong>Avantages du détaché</strong> : Plus d'espace, moins de pollution visuelle, pratique sur plusieurs écrans</li>
                <li><strong>Basculer</strong> : Bouton "🪟 Détacher" ou "🔗 Rattacher" selon le mode actif</li>
            </ul>
                
            <h3 id="recuperation-crash">💾 Système de récupération anti-perte</h3>
            {generator._get_image_html("05_tools/editor", "009", 
                "Popup récupération après crash", 
                "Vue de la popup de confirmation de récupération après crash")}
            
            <p>L'éditeur dispose d'un <strong>système de sécurité anti-perte</strong> qui enregistre toutes vos modifications en temps réel dans un fichier JSON.</p>
            
            <h4>🛡️ Protection maximale</h4>
            <ul style="padding-left: 40px;">
                <li>• <strong>Sauvegarde temps réel</strong> : Chaque modification est enregistrée instantanément</li>
                <li>• <strong>Cache JSON persistant</strong> : Stockage sécurisé sur le disque</li>
                <li>• <strong>Récupération intelligente</strong> : Au redémarrage, proposition automatique de récupérer les modifications non sauvées</li>
                <li>• <strong>Statistiques détaillées</strong> : Voir combien de modifications sont en attente par type</li>
            </ul>
                
            <div class="step-box">
                <h4>🔄 Que faire en cas de crash ?</h4>
                <ol style="padding-left: 40px;">
                    <li>Relancez RenExtract et ouvrez les Outils Spécialisés</li>
                    <li>Allez dans l'onglet <strong>Éditeur Temps Réel</strong></li>
                    <li>Si des modifications sont en attente, un popup s'affiche automatiquement</li>
                    <li>Choisissez <strong>"💾 Récupérer et sauvegarder"</strong> pour restaurer vos modifications</li>
                    <li>Les modifications sont <strong>récupérées dans l'interface</strong> mais vous devrez ensuite <strong>les sauvegarder manuellement</strong> avec le bouton "💾 Enregistrer"</li>
                </ol>
                <p><strong>Note :</strong> Les modifications ne sont pas automatiquement sauvegardées dans les fichiers .rpy, vous devez confirmer la sauvegarde après récupération.</p>
            </div>
                
            <div class="warning-box" style="border-left: 4px solid #ff6b6b;">
                <h4>⚠️ Limitations et compatibilité</h4>
                <ul>
                    <li><strong>🚨 Compatibilité Ren'Py</strong> : Toutes les versions de Ren'Py ne sont pas encore supportées. Le support complet est en cours de développement. Si l'éditeur ne fonctionne pas avec votre jeu, utilisez le mode d'édition classique en attendant</li>
                    <li><strong>Un projet à la fois</strong> : La surveillance ne fonctionne que pour un jeu simultanément</li>
                    <li><strong>Arrêt recommandé</strong> : Stoppez la surveillance avant de changer de projet</li>
                    <li><strong>Performance</strong> : Le cache initial peut être plus lent sur de très gros projets</li>
                    <li><strong>Compatibilité fichiers</strong> : Nécessite un jeu Ren'Py fonctionnel avec fichiers non corrompus</li>
                    <li><strong>Groq AI et VPN</strong> : ⚠️ Désactivez votre VPN avant utilisation ! Erreur typique avec VPN actif : <code>"Access denied. Please check your network settings."</code></li>
                </ul>
            </div>
                
            <h3 id="aide-editeur">❓ Aide contextuelle</h3>
            <p>Un bouton <strong>"À quoi ça sert ?"</strong> est disponible dans l'interface pour ouvrir une aide détaillée sur l'éditeur temps réel.</p>
            </div>
            
        <!-- Section 3 : Vérification Cohérence -->
        <div class="section" id="verification-coherence">
            <h2>🧪 Vérification Cohérence</h2>
            <p>Le <strong>Vérificateur de Cohérence</strong> détecte automatiquement les <strong>incohérences techniques</strong> entre les lignes originales (OLD) et traduites (NEW) dans vos fichiers .rpy.</p>
            
            <h3>🎯 À quoi ça sert ?</h3>
            <p>Le vérificateur <strong>ne juge pas la qualité de votre traduction</strong>, mais s'assure que vous n'avez pas cassé la syntaxe du jeu.</p>
            <p><strong>Une seule balise mal fermée peut faire planter tout le jeu.</strong> Une variable manquante ne causera pas forcément d'erreur technique, mais c'est un manque de respect envers le travail du développeur. Ce vérificateur vous évite des heures de débogage en trouvant ces erreurs avant que vous ne testiez le jeu.</p>
            
            <h3>🖥️ Vue d'ensemble</h3>
            {generator._get_image_html("05_tools/coherence", "001", 
                "Onglet Vérification Cohérence", 
                "Vue d'ensemble de l'onglet")}
            
            <h4>🔧 Structure de l'interface</h4>
            <ol style="padding-left: 40px;">
                <li><strong>Sélection langue/fichiers</strong> : Choix de la langue et du mode d'analyse</li>
                <li><strong>Types de vérifications</strong> : Environ 13 types de contrôles disponibles</li>
                <li><strong>Exclusions</strong> : Fichiers à ignorer</li>
            </ol>
            
            <h3 id="config-coherence">⚙️ Configuration des vérifications</h3>
            {generator._get_image_html("05_tools/coherence", "002", 
                "Langue et Fichier à sélectionner", 
                "Focus sur la zone : Langue et Fichier à sélectionner")}
            
            <p>Cette section vous permet de <strong>sélectionner la langue de traduction</strong> à vérifier et de choisir le <strong>mode d'analyse</strong> :</p>
            <ul style="padding-left: 40px;">
                <li>• <strong>Tous les fichiers</strong> : Analyse complète de tous les fichiers .rpy de la langue sélectionnée (sauf exclusions)</li>
                <li>• <strong>Un fichier spécifique</strong> : Analyse ciblée sur un seul fichier .rpy</li>
            </ul>
            
            {generator._get_image_html("05_tools/coherence", "003", 
                "Types de vérifications à effectuer", 
                "Focus sur la zone : Types de vérifications à effectuer")}
            
            <p>L'interface propose <strong>13 types de vérifications</strong> répartis en 5 colonnes :</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0;">
                <div>
                    <h4>🔤 Variables [] incohérentes</h4>
                    <p>Détecte les variables Ren'Py manquantes ou ajoutées (ex: <code>[player_name]</code>)</p>
                </div>
            
                <div>
                    <h4>🎨 Balises {{}} incohérentes</h4>
                    <p>Détecte les balises de formatage manquantes ou mal fermées (ex: <code>{{color=#ff0000}}{{/color}}</code>)</p>
                </div>
                
                <div>
                    <h4>💻 Codes spéciaux (\\n, --, %)</h4>
                    <p>Détecte les caractères de contrôle manquants (ex: <code>\\n</code> pour les retours à la ligne)</p>
                </div>
                
                <div>
                    <h4>📝 Lignes non traduites</h4>
                    <p>Détecte les textes identiques entre OLD et NEW (traduction oubliée)</p>
                </div>
                
                <div>
                    <h4>() Parenthèses incohérentes</h4>
                    <p>Vérification du nombre de parenthèses ouvrantes/fermantes</p>
                </div>
                
                <div>
                    <h4>« » Guillemets français</h4>
                    <p>Support des guillemets français et de leurs équivalents &lt;&lt;&gt;&gt;</p>
                </div>
                
                <div>
                    <h4>... Points de suspension</h4>
                    <p>Détection des ellipsis mal formatés</p>
                </div>
                
                <div>
                    <h4>🔧 Structure de ligne</h4>
                    <p>Vérification de la syntaxe Ren'Py</p>
                </div>
            </div>
                
            <h3>🎮 Contrôles rapides</h3>
            <p>Deux boutons vous permettent de gérer rapidement les vérifications :</p>
            <ul style="padding-left: 40px;">
                <li>• <strong>✅ Tout sélectionner</strong> : Active tous les types de vérifications</li>
                <li>• <strong>❌ Tout désélectionner</strong> : Désactive tout pour une sélection manuelle</li>
            </ul>
                
            <h3>🚫 Système d'exclusions</h3>
            <p>Vous pouvez exclure certains fichiers de l'analyse :</p>
            
            {generator._get_image_html("05_tools/coherence", "004", 
                "Fichiers à exclure", 
                "Focus sur la zone : Fichier à exclure")}
            
            <h4>📝 Exclusions de fichiers</h4>
            <ul>
                <li><strong>Par défaut</strong> : <code>common.rpy</code> est exclu (fichier système Ren'Py)</li>
                <li><strong>Ajout manuel</strong> : Liste séparée par virgules</li>
                <li><strong>Correspondance</strong> : Partielle dans le nom de fichier, insensible à la casse</li>
            </ul>
            
            <h3 id="processus-coherence">🚀 Lancement de l'analyse</h3>
            <p>Une fois votre configuration prête, cliquez sur le bouton <strong>"🧪 Démarrer l'analyse"</strong>.</p>
            
            {generator._get_image_html("05_tools/coherence", "005", 
                "Boutons d'actions", 
                "Focus sur la zone : Bouton d'actions")}
            
            <h4>⚡ Processus automatisé</h4>
            <ol style="padding-left: 40px;">
                <li><strong>Validation préalable</strong> : Vérification projet/langue/fichiers</li>
                <li><strong>Configuration automatique</strong> : Application des exclusions sauvegardées</li>
                <li><strong>Analyse threadée</strong> : Interface responsive pendant le traitement</li>
                <li><strong>Génération de rapport</strong> : Rapport HTML avec métadonnées complètes</li>
                <li><strong>Ouverture automatique</strong> : Selon vos paramètres utilisateur</li>
            </ol>
                
            <h3 id="rapport-html-coherence">📊 Rapport HTML de cohérence</h3>
            
            <p>Le rapport HTML s'ouvre automatiquement dans votre navigateur et offre une navigation intuitive des résultats.</p>
            
            {generator._get_image_html("05_tools/coherence", "006", 
                "Rapport HTML de cohérence", 
                "Vue d'ensemble du rapport de cohérence")}
            
            <h4>📄 Structure du rapport</h4>
            <ul>
                <li><strong>Métadonnées</strong> : Date, heure, projet analysé, langue, mode (tous fichiers/spécifique)</li>
                <li><strong>Statistiques globales</strong> : Fichiers analysés, lignes vérifiées, erreurs détectées</li>
                <li><strong>Navigation intelligente</strong> : Filtres par type d'erreur, fichier, niveau de criticité</li>
                <li><strong>Détails des erreurs</strong> : Liste avec Type, Fichier (cliquable), Ligne, VO, VF, Description</li>
                <li><strong>Thème adaptatif</strong> : Sombre/clair selon vos préférences</li>
            </ul>
        </div>
    """
