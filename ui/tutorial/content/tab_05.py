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
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 15px;">
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
            <p>Les <strong>Outils Spécialisés</strong> regroupent trois fonctionnalités avancées pour maintenir et améliorer la qualité de tes traductions Ren'Py. Ils sont accessibles dans une interface dédiée qui partage le projet avec l'interface principale.</p>
            
            <h3>📍 Comment accéder aux outils</h3>
            {generator._get_image_html("05_outils", "001", 
                "Accès aux outils depuis l'interface principale", 
                "Bouton Outils Spécialisé dans l'onglet OUTILS")}
            
            <div class="step-box">
                <h4>🎯 Étapes d'accès</h4>
                <ol>
                    <li>Dans l'interface principale, clique sur l'onglet <strong>OUTILS</strong> (jaune)</li>
                    <li>Clique sur le bouton <strong>🔧 Outils Spécialisé</strong></li>
                    <li>Une nouvelle fenêtre s'ouvre avec les 3 outils disponibles</li>
                </ol>
            </div>
            
            <h3 id="vue-ensemble-outils">🖥️ Vue d'ensemble de l'interface</h3>
            {generator._get_image_html("05_outils", "002", 
                "Fenêtre Outils - Vue d'ensemble", 
                "Interface complète des outils de maintenance vierge")}
            
            <div class="info-box">
                <h4>🔍 Structure de l'interface</h4>
                <p>L'interface des outils se compose de :</p>
                <ul>
                    <li><strong>Header</strong> : Configuration du projet (synchronisé automatiquement avec l'interface principale)</li>
                    <li><strong>3 onglets</strong> : Nettoyage, Éditeur Temps Réel, Vérification Cohérence</li>
                    <li><strong>Footer</strong> : Statut et bouton Fermer</li>
                </ul>
            </div>
            </div>
            
        <!-- Section 1 : Nettoyage Intelligent -->
        <div class="section" id="nettoyage-intelligent">
            <h2>🧹 Nettoyage Intelligent</h2>
            <p>Le <strong>Nettoyage Intelligent</strong> supprime automatiquement les <strong>traductions orphelines</strong> - ces blocs de traduction qui n'ont plus de correspondance dans les fichiers source du jeu après une mise à jour.</p>
            
            <h3>🎯 À quoi ça sert ?</h3>
            <div class="warning-box">
                <h4>⚠️ Problème des traductions orphelines</h4>
                <p>Quand un développeur met à jour son jeu, certains dialogues sont supprimés ou modifiés. Tes anciens fichiers de traduction gardent ces lignes obsolètes qui :</p>
                <ul>
                    <li>Alourdissent les fichiers de traduction (même si négligeable)</li>
                    <li>Rendent la navigation et la maintenance plus difficiles</li>
                </ul>
                <p><strong>Le nettoyage intelligent résout ce problème en un clic !</strong></p>
                </div>
                
            <h3>💪 Double méthode de nettoyage</h3>
            <p>RenExtract utilise deux méthodes complémentaires pour un nettoyage optimal :</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0;">
                <div class="info-box">
                    <h4>🎯 Nettoyage basé sur lint.txt</h4>
                    <p>Utilise l'analyse officielle du SDK Ren'Py pour détecter les IDs de traduction orphelins.</p>
                    <p><strong>Avantage :</strong> Précision maximale basée sur l'analyse officielle</p>
                </div>
                <div class="info-box">
                    <h4>🔍 Nettoyage par correspondance</h4>
                    <p>Vérifie si les textes OLD existent encore dans les fichiers source du jeu.</p>
                    <p><strong>Note :</strong> Comme cette méthode n'est pas précise à 100%, les blocs détectés sont récupérés et fournis dans le rapport pour que tu puisses les vérifier et les reprendre si besoin.</p>
                </div>
            </div>
            
            <h3>🖥️ Interface de nettoyage</h3>
            {generator._get_image_html("05_outils", "003", 
                "Onglet Nettoyage - Vue complète", 
                "Interface complète du nettoyage avec projet sélectionné")}
            
            <div class="step-box">
                <h4>🚀 Workflow en 3 étapes</h4>
                <ol>
                    <li><strong>Sélectionner les langues</strong> : Choisis les langues à nettoyer</li>
                    <li><strong>Configurer les exclusions</strong> : Protège les fichiers importants</li>
                    <li><strong>Lancer le nettoyage</strong> : Clique sur "🧹 Démarrer le nettoyage"</li>
                </ol>
                </div>
                
            <h3 id="selection-langues-nettoyage">🌍 Sélection des langues</h3>
            <p>Les langues sont <strong>détectées automatiquement</strong> dès que tu sélectionnes un projet. Elles s'affichent dans une grille à 3 colonnes pour une lecture optimale.</p>
            
            {generator._get_image_html("05_outils", "005", 
                "Grille de sélection des langues", 
                "Organisation en 3 colonnes avec badges numérotés")}
            
            <div class="info-box">
                <h4>📊 Organisation visuelle</h4>
                <ul>
                    <li><strong>Icônes contextuelles</strong> : 🌐 pour English, 🗣️ pour les autres langues</li>
                    <li><strong>Formatage automatique</strong> : Première lettre en majuscule</li>
                    <li><strong>Grille responsive</strong> : S'adapte à la taille de la fenêtre</li>
                    <li><strong>Détection automatique</strong> : Les langues apparaissent dès la sélection du projet</li>
                </ul>
            </div>
            
            <h3 id="controles-langues">🎮 Contrôles rapides</h3>
            {generator._get_image_html("05_outils", "004", 
                "Boutons de contrôle", 
                "Sélection et désélection rapide des langues")}
            
            <p>Deux boutons te permettent de gérer rapidement la sélection :</p>
            <ul>
                <li><strong>✅ Tout sélectionner</strong> : Coche toutes les langues d'un coup</li>
                <li><strong>❌ Tout désélectionner</strong> : Décoche toutes les langues pour une sélection manuelle précise</li>
            </ul>
            
            <h3 id="exclusions-nettoyage">🚫 Exclusions de fichiers</h3>
            <p>Tu peux protéger certains fichiers du nettoyage en les ajoutant dans le champ <strong>"Fichiers à exclure"</strong>.</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0;">
                <div class="info-box">
                    <h4>📝 Fichiers protégés automatiquement</h4>
                    <p><strong>Exclusions système</strong> (toujours actives) :</p>
                    <ul>
                        <li><code>common.rpy</code> : Fichier système Ren'Py</li>
                        <li><code>99_Z_Console.rpy</code> : Console développeur RenExtract</li>
                        <li><code>99_Z_ScreenPreferences.rpy</code> : Écran préférences RenExtract</li>
                        <li><code>99_Z_FontSystem.rpy</code> : Système de polices RenExtract</li>
                    </ul>
                    <p><strong>Valeur par défaut dans le champ :</strong> <code>common.rpy</code></p>
                    <p>Tu peux ajouter tes propres fichiers (sélecteurs de langue, patches, menus personnalisés) en les séparant par des virgules.</p>
                </div>
                
                <div class="warning-box">
                    <h4>⚙️ Règles importantes</h4>
                    <ul>
                        <li>Les <strong>fichiers système</strong> sont toujours protégés automatiquement (même s'ils ne sont pas dans ta liste)</li>
                        <li>La correspondance est <strong>exacte</strong> mais <strong>insensible à la casse</strong></li>
                        <li>Spécifie toujours l'<strong>extension .rpy</strong></li>
                        <li>Les modifications sont <strong>sauvegardées automatiquement</strong></li>
                    </ul>
                </div>
            </div>
            
            <h3 id="aide-nettoyage">❓ Aide contextuelle</h3>
            {generator._get_image_html("05_outils", "006", 
                "Fenêtre d'aide globale", 
                "Aide complète pour le nettoyage intelligent")}
            
            <p>Le bouton <strong>"À quoi ça sert ?"</strong> ouvre une aide complète qui explique :</p>
            <ul>
                <li>🎯 L'utilité du nettoyage intelligent</li>
                <li>⚡ Le fonctionnement détaillé du processus</li>
                <li>🚫 Les règles d'exclusion des fichiers</li>
                <li>💡 Les conseils et bonnes pratiques</li>
            </ul>
            
            <h3 id="processus-nettoyage">⚙️ Processus de nettoyage</h3>
            {generator._get_image_html("05_outils", "007", 
                "Nettoyage en cours", 
                "Spinner animé pendant la génération du lint")}
            
            <div class="step-box">
                <h4>🔄 Étapes automatiques</h4>
                <ol>
                    <li><strong>Contrôle des prérequis</strong> : Vérification de l'absence de fichiers .rpa (invite à décompiler si détectés) et détection de traceback.txt dans le dossier du jeu (arrêt si présent)</li>
                    <li><strong>Validation du SDK</strong> : Vérification ou téléchargement automatique</li>
                    <li><strong>Génération du lint.txt</strong> : Analyse officielle Ren'Py avec surveillance du traceback.txt (arrêt immédiat si généré pendant l'exécution)</li>
                    <li><strong>Analyse unifiée</strong> : Détection des orphelins avec double méthode</li>
                    <li><strong>Sauvegarde & suppression</strong> : Backup unifié + nettoyage final</li>
            </ol>
                </div>
                
            <div class="tip-box">
                <h4>💡 Pendant le nettoyage</h4>
                <ul>
                    <li>Un <strong>spinner animé</strong> indique que l'opération est en cours</li>
                    <li>Le bouton principal est <strong>désactivé</strong> pour éviter les doublons</li>
                    <li>Un bouton <strong>"⏹️ Annuler"</strong> te permet de stopper l'opération si besoin</li>
                </ul>
                </div>
                
            <h3 id="resultats-nettoyage">📊 Résultats automatiques</h3>
            {generator._get_image_html("05_outils", "008", 
                "Rapport HTML de nettoyage", 
                "Rapport détaillé avec statistiques et résultats")}
            
            <p>À la fin du nettoyage, le <strong>rapport HTML s'ouvre automatiquement</strong> dans ton navigateur.</p>
            
            <div class="info-box">
                <h4>📄 Contenu du rapport</h4>
                <ul>
                    <li><strong>Métadonnées</strong> : Date, projet, langues traitées</li>
                    <li><strong>Statistiques visuelles</strong> : Cartes avec chiffres clés, graphiques</li>
                    <li><strong>Détails par fichier</strong> : Liste des fichiers nettoyés avec nombre de blocs supprimés</li>
                    <li><strong>Thème adaptatif</strong> : Sombre/clair selon tes préférences</li>
                </ul>
                </div>
                
            <h3 id="erreurs-nettoyage">⚠️ Messages d'erreur</h3>
            {generator._get_image_html("05_outils", "009", 
                "Toast notification aucune langue", 
                "Message d'avertissement si aucune langue sélectionnée")}
            
            <p>Si tu oublies de sélectionner des langues avant de lancer le nettoyage, un <strong>toast d'avertissement</strong> (orange) s'affiche en bas de la fenêtre pour te le rappeler.</p>

            <h3>💡 Conseils d'utilisation</h3>
            <div class="tip-box">
                <h4>🎯 Bonnes pratiques</h4>
                <ul>
                    <li><strong>Après chaque mise à jour du jeu</strong> : Lance un nettoyage pour supprimer les anciennes traductions</li>
                    <li><strong>Avant une session de test</strong> : Assure-toi que tes fichiers sont propres</li>
                    <li><strong>Configure les exclusions une fois</strong> : Elles sont sauvegardées automatiquement</li>
                    <li><strong>Vérifie le rapport</strong> : Consulte les statistiques pour voir ce qui a été nettoyé</li>
            </ul>
            </div>
            
            <div class="warning-box">
                <h4>⚠️ Points d'attention</h4>
                <ul>
                    <li>Le système crée des <strong>sauvegardes automatiques</strong>, mais garde tes propres backups importants</li>
                    <li><strong>Teste le jeu</strong> après le nettoyage pour vérifier que tout fonctionne</li>
                    <li><strong>Protège tes fichiers modifiés manuellement</strong> en les ajoutant aux exclusions (comme les fichiers techniques de sélection de langue)</li>
                    <li>Le nettoyage est <strong>global par fichier</strong> (pas de récupération partielle)</li>
                </ul>
            </div>
        </div>

        <!-- Section 2 : Éditeur Temps Réel -->
        <div class="section" id="editeur-temps-reel">
            <h2>⚡ Éditeur Temps Réel</h2>
            <p>L'<strong>Éditeur Temps Réel</strong> te permet de modifier les traductions <strong>pendant que le jeu fonctionne</strong>, sans le redémarrer. Idéal pour peaufiner rapidement des dialogues, ajuster des traductions trop longues, ou corriger des erreurs détectées en cours de jeu.</p>
            
            <h3>🎯 À quoi ça sert ?</h3>
            <div class="success-box">
                <h4>🚀 Révolution du workflow</h4>
                <p><strong>Terminé</strong> le cycle épuisant :</p>
                <ol>
                    <li>Quitter le jeu</li>
                    <li>Modifier le fichier</li>
                    <li>Reconstruire les traductions</li>
                    <li>Relancer le jeu</li>
                </ol>
                <p><strong>Avec l'éditeur temps réel</strong> : Tu modifies directement depuis le jeu et appuies sur <strong>Maj+R</strong> pour voir les changements instantanément !</p>
            </div>
            
            <h3>🖥️ Vue d'ensemble</h3>
            {generator._get_image_html("05_outils", "010", 
                "Onglet Éditeur Temps Réel", 
                "Interface complète de l'éditeur avec installation et surveillance")}
            
            <div class="info-box">
                <h4>🔧 Fonctionnement en 2 temps</h4>
                <ol>
                    <li><strong>Installation du module</strong> : Une seule fois par projet</li>
                    <li><strong>Démarrage de la surveillance</strong> : À chaque session de traduction</li>
                </ol>
            </div>
            
            <h3 id="installation-editeur">⚙️ Installation et configuration</h3>
            {generator._get_image_html("05_outils", "011", 
                "Aide Éditeur Temps Réel", 
                "Fenêtre d'aide complète avec explications détaillées")}
            
            <div class="step-box">
                <h4>🚀 Configuration en 3 étapes</h4>
                <ol>
                    <li><strong>Sélection de langue</strong> : Choisis la langue à surveiller (ex: French, German)</li>
                    <li><strong>Installation du module</strong> : Clique sur "🔧 Installer le module" (une seule fois)</li>
                    <li><strong>Démarrage surveillance</strong> : Clique sur "🚀 Démarrer la surveillance" puis lance ton jeu</li>
                </ol>
            </div>
            
            <div class="tip-box">
                <h4>💡 Installation unique</h4>
                <p>Le module s'installe <strong>une seule fois</strong> dans <code>game/</code> et fonctionne pour <strong>toutes les langues</strong>. Il est automatiquement activé dès le lancement du jeu.</p>
            </div>
            
            <h3>⌨️ Raccourcis clavier essentiels</h3>
            <div class="info-box">
                <h4>🔧 Raccourcis à connaître</h4>
                <ul>
                    <li><strong>F8</strong> : Ouvre l'éditeur si besoin (depuis le jeu quand un dialogue nécessite une correction)</li>
                    <li><strong>Maj+R</strong> : Recharge les traductions (une fois par session, puis le jeu passe en autoreload)</li>
                    <li><strong>F11</strong> : Retour en plein écran (si le jeu est passé en fenêtré avec F8)</li>
            </ul>
                </div>
                
            <div class="info-box">
                <h4>🎯 Fonctionnement du raccourci F8</h4>
                <p><strong>F8</strong> a une double utilité selon le mode de jeu :</p>
                <ul>
                    <li><strong>En plein écran</strong> : Le jeu détecte le plein écran, passe en mode fenêtré, puis met RenExtract au premier plan</li>
                    <li><strong>En mode fenêtré</strong> : Met directement la fenêtre RenExtract au premier plan (focus)</li>
                </ul>
                <p>La <strong>fenêtre principale de RenExtract</strong> (ou la <strong>fenêtre détachée</strong> si le mode détaché est actif) se met au premier plan pour que tu puisses éditer.</p>
                <p><strong>Utilise F11</strong> dans le jeu pour revenir en plein écran après tes modifications.</p>
            </div>
            
            <h3 id="edition-dialogue-simple">💬 Interface d'édition - Dialogues simples</h3>
            {generator._get_image_html("05_outils", "012", 
                "Interface édition simple (mode détaché)", 
                "Édition d'un dialogue classique avec zones VO et VF")}
            
            <p>Pour les <strong>dialogues classiques</strong> avec un seul personnage, l'interface propose deux zones côte à côte :</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0;">
                <div class="info-box">
                    <h4>📖 Zone VO (Version Originale)</h4>
                    <ul>
                        <li>Texte en <strong>lecture seule</strong></li>
                        <li>Même couleur de fond que la zone VF</li>
                        <li>Sert de référence pour la traduction</li>
                    </ul>
                </div>
                <div class="success-box">
                    <h4>🇫🇷 Zone VF (Version Française)</h4>
                    <ul>
                        <li>Texte <strong>éditable</strong></li>
                        <li>Zone d'édition avec texte en <strong>bleu</strong></li>
                        <li>Modifie directement ta traduction ici</li>
                    </ul>
                </div>
                </div>
                
            <div class="tip-box">
                <h4>💡 Boutons utilitaires</h4>
                <p>Chaque zone de texte dispose de boutons pratiques :</p>
                <ul>
                    <li><strong>📋 Copier</strong> : Copie le texte VO dans le presse-papier</li>
                    <li><strong>🌐 Traduire en ligne</strong> : Copie le texte VO et ouvre le traducteur sélectionné avec le texte pré-rempli selon la langue cible choisie</li>
                    <li><strong>📝 Coller</strong> : Colle le contenu du presse-papier dans la zone VF</li>
                </ul>
           <p><strong>Traducteurs supportés :</strong> Google Translate, Yandex Translate, DeepL, Microsoft Translator, Groq AI</p>
           <p><strong>Langues cibles :</strong> Français, Anglais, Espagnol, Allemand, Italien, Portugais, Russe, Japonais, Chinois</p>
           <p><strong>Note :</strong> Le texte est automatiquement pré-rempli dans le traducteur selon la langue sélectionnée dans l'interface. Il est aussi copié dans le presse-papier comme backup.</p>
                </div>
                
            <h3 id="edition-locuteur">🎭 Interface d'édition - Locuteur non défini</h3>
            {generator._get_image_html("05_outils", "013", 
                "Interface locuteur non défini (mode détaché)", 
                "Édition séparée du locuteur et du dialogue")}
            
            <p>Pour les dialogues au format <code>"Nom" "Dialogue"</code>, l'interface se divise en <strong>deux zones distinctes</strong> :</p>
            
            <div class="step-box">
                <h4>📝 Édition en 2 parties</h4>
                <ol>
                    <li><strong>Zone Locuteur</strong> : VO et VF pour le nom du personnage</li>
                    <li><strong>Zone Dialogue</strong> : VO et VF pour le texte du dialogue</li>
                </ol>
                <p><strong>Avantage :</strong> Édition séparée du nom et du dialogue pour plus de précision</p>
            </div>
            
            <h3 id="edition-split">🔀 Interface d'édition - Dialogues divisés</h3>
            {generator._get_image_html("05_outils", "014", 
                "Interface dialogues divisés (mode détaché)", 
                "Division d'un long dialogue en deux parties")}
            
            <p>Pour les <strong>dialogues très longs</strong>, l'éditeur propose un <strong>mode split</strong> qui vous permet de diviser le texte en deux parties :</p>
            
            <div class="info-box">
                <h4>✂️ Division intelligente</h4>
                <ul>
                    <li><strong>Partie 1/2</strong> : Première moitié du dialogue (fond bleu clair)</li>
                    <li><strong>Partie 2/2</strong> : Seconde moitié du dialogue (fond normal)</li>
                    <li><strong>Indicateur visuel</strong> : La partie active est surlignée</li>
                    <li><strong>Bouton Fusionner</strong> : Pour revenir en mode simple</li>
                    <li><strong>Détection voice</strong> : Détecte automatiquement les lignes avec fichiers vocaux (<code>voice "chemin/fichier.ogg"</code>)</li>
                </ul>
                </div>
                
            <div class="tip-box">
                <h4>💡 Quand utiliser le mode split ?</h4>
                <p>Le mode split est particulièrement utile pour :</p>
                <ul>
                    <li>Les dialogues de narration très longs</li>
                    <li>Les descriptions détaillées</li>
                    <li>Les textes qui dépassent la limite d'affichage</li>
                </ul>
                </div>
                
            <h3 id="edition-menu">🎯 Interface d'édition - Choix multiples</h3>
            {generator._get_image_html("05_outils", "015", 
                "Interface choix multiples (mode détaché)", 
                "Édition des options de menu")}
            
            <p>Pour les <strong>menus de choix</strong> du joueur, l'interface affiche une <strong>grille</strong> avec toutes les options :</p>
            
            <div class="info-box">
                <h4>📊 Organisation en grille</h4>
                <ul>
                    <li>Chaque <strong>choix</strong> a sa propre zone VO/VF</li>
                    <li>Les boutons utilitaires sont disponibles pour chaque option</li>
                    <li>Un seul bouton <strong>"💾 Enregistrer tous les choix"</strong> sauvegarde tout d'un coup</li>
                    <li>Adapté pour 2, 3 ou 4 choix selon le menu</li>
            </ul>
                </div>
                
            <div class="warning-box">
                <h4>⚠️ Sauvegarde obligatoire</h4>
                <p><strong>Important :</strong> Pour les menus de choix, c'est le <strong>seul cas où tu dois sauvegarder avant de passer au dialogue suivant</strong>. Si tu ne sauvegardes pas, les modifications des choix seront perdues quand tu passeras à un autre dialogue.</p>
            </div>
            
            <h3 id="edition-multiple">🔢 Interface d'édition - Dialogues multiples</h3>
            {generator._get_image_html("05_outils", "016", 
                "Interface dialogues multiples (mode détaché)", 
                "Édition de dialogues simultanés")}
            
            <p>Pour les <strong>dialogues multiples</strong> (plusieurs personnes qui parlent en même temps), l'interface affiche une <strong>liste verticale</strong> :</p>
            
            <div class="info-box">
                <h4>📝 Liste ordonnée</h4>
                <ul>
                    <li>Chaque dialogue est numéroté et clairement séparé</li>
                    <li>Édition individuelle de chaque ligne</li>
                    <li>Boutons utilitaires pour chaque dialogue</li>
                    <li>Sauvegarde groupée avec un seul bouton</li>
                </ul>
                </div>
                
            <div class="tip-box">
                <h4>💡 Efficacité maximale</h4>
                <p>Le mode dialogues multiples est conçu pour :</p>
                <ul>
                    <li>Les conversations à plusieurs personnages simultanément</li>
                    <li>Les dialogues qui se chevauchent</li>
                    <li>Les scènes de groupe avec plusieurs interlocuteurs</li>
            </ul>
                </div>
                
            <h3 id="mode-detache">🪟 Mode détaché</h3>
            <p>Les captures d'écran précédentes montrent l'éditeur en <strong>mode détaché</strong> - une fenêtre séparée de l'interface principale.</p>
            
            <div class="info-box">
                <h4>📐 Mode détaché vs Mode attaché</h4>
                <ul>
                    <li><strong>Mode attaché</strong> : L'éditeur s'affiche dans l'onglet principal des outils</li>
                    <li><strong>Mode détaché</strong> : L'éditeur s'ouvre dans une fenêtre séparée</li>
                    <li><strong>Avantages du détaché</strong> : Plus d'espace, moins de pollution visuelle, pratique sur plusieurs écrans</li>
                    <li><strong>Basculer</strong> : Bouton "🪟 Détacher" ou "🔗 Rattacher" selon le mode actif</li>
                </ul>
            </div>
            
            <div class="tip-box">
                <h4>💡 Conseil multi-écrans</h4>
                <p>Si tu as <strong>deux écrans</strong>, le mode détaché est idéal :</p>
                <ul>
                    <li>Place le jeu en plein écran sur l'écran principal</li>
                    <li>Détache l'éditeur et place-le sur le second écran</li>
                    <li>Avec le raccourci <strong>F8</strong>, tu peux basculer rapidement entre le jeu et l'éditeur</li>
            </ul>
                </div>
                
            <h3 id="recuperation-crash">💾 Système de récupération anti-perte</h3>
            {generator._get_image_html("05_outils", "017", 
                "Popup récupération après crash", 
                "Dialog de récupération avec statistiques des modifications")}
            
            <p>L'éditeur dispose d'un <strong>système de sécurité anti-perte</strong> qui enregistre toutes tes modifications en temps réel dans un fichier JSON.</p>
            
            <div class="success-box">
                <h4>🛡️ Protection maximale</h4>
                <ul>
                    <li><strong>Sauvegarde temps réel</strong> : Chaque modification est enregistrée instantanément</li>
                    <li><strong>Cache JSON persistant</strong> : Stockage sécurisé sur le disque</li>
                    <li><strong>Récupération intelligente</strong> : Au redémarrage, proposition automatique de récupérer les modifications non sauvées</li>
                    <li><strong>Statistiques détaillées</strong> : Voir combien de modifications sont en attente par type</li>
                </ul>
                </div>
                
            <div class="step-box">
                <h4>🔄 Que faire en cas de crash ?</h4>
                <ol>
                    <li>Relance RenExtract et ouvre les Outils Spécialisés</li>
                    <li>Va dans l'onglet <strong>Éditeur Temps Réel</strong></li>
                    <li>Si des modifications sont en attente, un popup s'affiche automatiquement</li>
                    <li>Choisis <strong>"💾 Récupérer et sauvegarder"</strong> pour restaurer tes modifications</li>
                    <li>Les modifications sont <strong>récupérées dans l'interface</strong> mais tu devras ensuite <strong>les sauvegarder manuellement</strong> avec le bouton "💾 Enregistrer"</li>
                </ol>
                <p><strong>Note :</strong> Les modifications ne sont pas automatiquement sauvegardées dans les fichiers .rpy, tu dois confirmer la sauvegarde après récupération.</p>
                </div>
                
            <h3>💡 Conseils d'utilisation optimale</h3>
            <div class="tip-box">
                <h4>🎯 Workflow recommandé</h4>
                <ol>
                    <li><strong>Installation unique</strong> : Configure le module une fois par projet</li>
                    <li><strong>Session de jeu</strong> : Démarre la surveillance puis lance le jeu</li>
                    <li><strong>Traduction contextuelle</strong> : Joue normalement, appuie sur <strong>F8 si besoin</strong> (seulement si le jeu est en plein écran)</li>
                    <li><strong>Test immédiat</strong> : Utilise <strong>Maj+R une fois au début de la session</strong>, puis le jeu passe en autoreload automatique</li>
                    <li><strong>Sauvegardes régulières</strong> : Sauvegarde régulièrement tes modifications pour éviter les mauvaises surprises, pas seulement en fin de session</li>
            </ol>
            </div>
            
           <div class="tip-box">
               <h4>🚀 Astuces pratiques</h4>
               <ul>
                   <li><strong>Cache de traductions</strong> : La première ouverture peut être lente (construction du cache), puis très rapide</li>
                   <li><strong>Traducteur en ligne</strong> : Choisis ton traducteur préféré dans la liste déroulante (Google, Yandex, DeepL, Microsoft, Groq AI). Le texte est automatiquement pré-rempli selon la langue cible sélectionnée dans l'interface</li>
                   <li><strong>Groq AI (recommandé)</strong> : 🤖 Traduction IA avec remplissage automatique de la zone VF ! 6000 traductions/jour gratuites. Ajoutez une clé API dans les paramètres. ⚠️ Désactivez votre VPN avant utilisation (Groq bloque certains VPN). 🚨 La clé API n'est affichée qu'UNE FOIS : gardez-en une copie de secours !</li>
                   <li><strong>Langues multiples</strong> : Change la langue dans l'interface pour traduire vers d'autres langues (anglais, espagnol, allemand, etc.)</li>
                   <li><strong>Taille de police</strong> : Ajuste la taille pour améliorer la lisibilité de <strong>la zone d'édition uniquement</strong> (n'affecte pas le jeu)</li>
            </ul>
           </div>
            
            <div class="warning-box">
                <h4>⚠️ Limitations à connaître</h4>
                <ul>
                    <li><strong>Un projet à la fois</strong> : La surveillance ne fonctionne que pour un jeu simultanément</li>
                    <li><strong>Arrêt recommandé</strong> : Stoppe la surveillance avant de changer de projet</li>
                    <li><strong>Performance</strong> : Le cache initial peut être plus lent sur de très gros projets</li>
                    <li><strong>Compatibilité</strong> : Nécessite un jeu Ren'Py fonctionnel avec fichiers non corrompus</li>
                    <li><strong>Traducteurs web</strong> : Google, Yandex, DeepL, Microsoft supportent le pré-remplissage automatique. Le texte est aussi copié dans le presse-papier comme backup</li>
                    <li><strong>Groq AI et VPN</strong> : ⚠️ Désactivez votre VPN avant utilisation ! Erreur typique avec VPN actif : <code>"Access denied. Please check your network settings."</code></li>
                </ul>
            </div>
            
            <div class="warning-box" style="border-left: 4px solid #ff6b6b;">
                <h4>🚨 IMPORTANT - Compatibilité versions Ren'Py</h4>
                <p><strong>⚠️ Toutes les versions de Ren'Py ne sont pas encore supportées par l'Éditeur Temps Réel.</strong></p>
                <p>Le support complet de toutes les versions est <strong>en cours de développement</strong> et sera disponible dans une future mise à jour.</p>
                <p>Si l'éditeur ne fonctionne pas avec ton jeu, c'est probablement une question de compatibilité de version. Utilise le mode d'édition classique en attendant.</p>
                </div>
            </div>
            
        <!-- Section 3 : Vérification Cohérence -->
        <div class="section" id="verification-coherence">
            <h2>🧪 Vérification Cohérence</h2>
            <p>Le <strong>Vérificateur de Cohérence</strong> détecte automatiquement les <strong>incohérences techniques</strong> entre les lignes originales (OLD) et traduites (NEW) dans tes fichiers .rpy.</p>
            
            <h3>🎯 À quoi ça sert ?</h3>
            <div class="warning-box">
                <h4>⚠️ Pourquoi c'est essentiel ?</h4>
                <p>Le vérificateur <strong>ne juge pas la qualité de ta traduction</strong>, mais s'assure que tu n'as pas cassé la syntaxe du jeu.</p>
                <p><strong>Une seule balise mal fermée peut faire planter tout le jeu.</strong> Une variable manquante ne causera pas forcément d'erreur technique, mais c'est un manque de respect envers le travail du développeur. Ce vérificateur t'évite des heures de débogage en trouvant ces erreurs avant que tu ne testes le jeu.</p>
            </div>
            
            <h3>🖥️ Vue d'ensemble</h3>
            {generator._get_image_html("05_outils", "018", 
                "Onglet Vérification Cohérence", 
                "Interface complète de vérification avec configuration")}
            
            <div class="info-box">
                <h4>🔧 Structure de l'interface</h4>
                <ol>
                    <li><strong>Sélection langue/fichiers</strong> : Choix de la langue et du mode d'analyse</li>
                    <li><strong>Types de vérifications</strong> : Environ 13 types de contrôles disponibles</li>
                    <li><strong>Exclusions</strong> : Fichiers à ignorer</li>
                </ol>
            </div>
            
            <h3 id="config-coherence">⚙️ Configuration des vérifications</h3>
            {generator._get_image_html("05_outils", "019", 
                "Aide Vérification Cohérence", 
                "Fenêtre d'aide avec explications des types d'erreurs")}
            
            <p>L'interface propose <strong>13 types de vérifications</strong> répartis en 5 colonnes. Voici les principaux :</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0;">
                <div class="warning-box">
                    <h4>🔤 Variables [] incohérentes</h4>
                    <p><strong>Détecte :</strong> Variables Ren'Py manquantes ou ajoutées</p>
                    <p><strong>Exemple :</strong> <code>[player_name]</code> dans OLD mais absent dans NEW (ou inversement)</p>
                    <p><strong>Impact :</strong> Perte de fonctionnalité ou non-respect du travail du développeur</p>
            </div>
            
                <div class="warning-box">
                    <h4>🎨 Balises {{}} incohérentes</h4>
                    <p><strong>Détecte :</strong> Balises de formatage manquantes ou ajoutées</p>
                    <p><strong>Exemple :</strong> <code>{{color=#ff0000}}Texte{{/color}}</code> dans OLD mais mal fermé dans NEW</p>
                    <p><strong>Impact :</strong> Affichage cassé, texte non formaté</p>
                </div>
                
                <div class="warning-box">
                    <h4>💻 Codes spéciaux (\\n, --, %)</h4>
                    <p><strong>Détecte :</strong> Caractères de contrôle manquants ou ajoutés</p>
                    <p><strong>Exemple :</strong> <code>\\n</code> (retour ligne) dans OLD mais absent dans NEW</p>
                    <p><strong>Impact :</strong> Mise en page cassée, dialogues collés</p>
                </div>
                
                <div class="info-box">
                    <h4>📝 Lignes non traduites</h4>
                    <p><strong>Détecte :</strong> Texte identique entre OLD et NEW</p>
                    <p><strong>Exemple :</strong> "Hello" conservé tel quel en français</p>
                    <p><strong>Impact :</strong> Texte non traduit visible pour le joueur</p>
                </div>
            </div>
            
            <div class="tip-box">
                <h4>💡 Nouvelles vérifications</h4>
                <p>L'analyseur inclut aussi des contrôles avancés :</p>
                <ul>
                    <li><strong>() Parenthèses incohérentes</strong> : Vérification du nombre de parenthèses ouvrantes/fermantes</li>
                    <li><strong>« » Guillemets français</strong> : Support des guillemets français et de leurs équivalents &lt;&lt;&gt;&gt;</li>
                    <li><strong>Points de suspension (...)</strong> : Détection des ellipsis mal formatés</li>
                    <li><strong>Structure de ligne</strong> : Vérification de la syntaxe Ren'Py</li>
            </ul>
                </div>
                
            <h3>🎮 Contrôles rapides</h3>
            <p>Deux boutons te permettent de gérer rapidement les vérifications :</p>
            <ul>
                <li><strong>✅ Tout sélectionner</strong> : Active tous les types de vérifications</li>
                <li><strong>❌ Tout désélectionner</strong> : Désactive tout pour une sélection manuelle</li>
                    </ul>
            
            <div class="tip-box">
                <h4>💡 Recommandation pour débuter</h4>
                <p>Lors de ta <strong>première utilisation</strong>, active <strong>tous les types de vérifications</strong> pour avoir une vision complète. Tu pourras ensuite adapter selon tes besoins spécifiques.</p>
                </div>
                
            <h3>🚫 Système d'exclusions</h3>
            <p>Tu peux exclure certains fichiers de l'analyse :</p>
            
            <div class="info-box">
                <h4>📝 Exclusions de fichiers</h4>
                <ul>
                    <li><strong>Par défaut</strong> : <code>common.rpy</code> est exclu (fichier système Ren'Py)</li>
                    <li><strong>Ajout manuel</strong> : Liste séparée par virgules</li>
                    <li><strong>Correspondance</strong> : Partielle dans le nom de fichier, insensible à la casse</li>
                    </ul>
            </div>
            
            <div class="tip-box">
                <h4>💡 Auto-exclusions de lignes</h4>
                <p>Certaines lignes sont <strong>automatiquement exclues</strong> de l'analyse car elles sont considérées comme valides :</p>
                <ul>
                    <li>Points de suspension (...)</li>
                    <li>Variables seules</li>
                    <li>Ellipsis</li>
                    <li>Onomatopées</li>
                </ul>
            </div>
            
            <h3 id="processus-coherence">🚀 Lancement de l'analyse</h3>
            <p>Une fois ta configuration prête, clique sur le bouton <strong>"🧪 Démarrer l'analyse"</strong>.</p>
            
            <div class="step-box">
                <h4>⚡ Processus automatisé</h4>
                <ol>
                    <li><strong>Validation préalable</strong> : Vérification projet/langue/fichiers</li>
                    <li><strong>Configuration automatique</strong> : Application des exclusions sauvegardées</li>
                    <li><strong>Analyse threadée</strong> : Interface responsive pendant le traitement</li>
                    <li><strong>Génération de rapport</strong> : Rapport HTML avec métadonnées complètes</li>
                    <li><strong>Ouverture automatique</strong> : Selon tes paramètres utilisateur</li>
            </ol>
                </div>
                
            <h3 id="rapport-html-coherence">📊 Rapport HTML de cohérence</h3>
            {generator._get_image_html("05_outils", "020", 
                "Rapport HTML de cohérence", 
                "Rapport interactif avec navigation et statistiques")}
            
            <p>Le rapport HTML s'ouvre automatiquement dans ton navigateur et offre une navigation intuitive des résultats.</p>
            
            <div class="info-box">
                <h4>📄 Structure du rapport</h4>
                <ul>
                    <li><strong>Métadonnées</strong> : Date, heure, projet analysé, langue, mode (tous fichiers/spécifique)</li>
                    <li><strong>Statistiques globales</strong> : Fichiers analysés, lignes vérifiées, erreurs détectées</li>
                    <li><strong>Navigation intelligente</strong> : Filtres par type d'erreur, fichier, niveau de criticité</li>
                    <li><strong>Détails des erreurs</strong> : Liste avec Type, Fichier (cliquable), Ligne, VO, VF, Description</li>
                    <li><strong>Thème adaptatif</strong> : Sombre/clair selon tes préférences</li>
                    </ul>
                </div>
                
            <div class="success-box">
                <h4>✨ Nouvelles fonctionnalités du rapport</h4>
                <ul>
                    <li><strong>Métadonnées enrichies</strong> : Contexte complet de l'analyse (traçabilité)</li>
                    <li><strong>Statistiques avancées</strong> : Répartition par types d'erreurs avec vue d'ensemble</li>
                    <li><strong>Navigation intelligente</strong> : Accès direct aux problèmes spécifiques</li>
                    <li><strong>Interface adaptive</strong> : Responsive, s'adapte à toutes les tailles d'écran</li>
                    </ul>
            </div>
            
            <h3>💡 Conseils d'utilisation optimale</h3>
            <div class="tip-box">
                <h4>🎯 Configuration recommandée</h4>
                <ul>
                    <li><strong>Première utilisation</strong> : Active tous les types de vérifications</li>
                    <li><strong>Exclusions fichiers</strong> : <code>common.rpy, screens.rpy</code> au minimum</li>
                    <li><strong>Sauvegarde</strong> : Tes paramètres sont mémorisés automatiquement</li>
            </ul>
                </div>
                
            <div class="tip-box">
                <h4>🚀 Workflow optimal</h4>
                <ol>
                    <li><strong>Projet unique</strong> : Configure une fois dans le header (synchronisation)</li>
                    <li><strong>Vérification systématique</strong> : Après chaque reconstruction importante</li>
                    <li><strong>Analyse complète</strong> : Avant chaque session de test du jeu</li>
                    <li><strong>Rapport permanent</strong> : Garde le rapport HTML ouvert pendant les corrections</li>
            </ol>
            </div>
        </div>
    """
