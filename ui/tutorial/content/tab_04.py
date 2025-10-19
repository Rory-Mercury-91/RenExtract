def generate_content(generator, language=None, translations=None):
    """
    Génère le contenu pour l'onglet 4 : Générateur Ren'Py
    
    Args:
        generator: Instance du générateur avec méthodes utilitaires
        language: Code langue (non utilisé, français pur)
        translations: Dictionnaire des traductions (non utilisé, français pur)
    
    Returns:
        str: HTML généré pour l'onglet générateur
    """
    
    return f"""
        <!-- NAVIGATION RAPIDE -->
        <div class="quick-nav-section" style="background: var(--card-bg); padding: 20px; margin-bottom: 30px; border-radius: 8px; border-left: 4px solid var(--accent);">
            <h3 style="margin-top: 0;">🧭 Navigation rapide</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 15px; margin-top: 15px;">
                <a href="#gen-vue-ensemble" class="nav-card" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; cursor: pointer;">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🎮 Vue d'ensemble</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Présentation du Générateur</div>
                </a>
                <a href="#gen-extraction-rpa" class="nav-card" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; cursor: pointer;">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">📦 Extraction & Compilation RPA</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Décompiler les archives du jeu</div>
                </a>
                <a href="#gen-generation-tl" class="nav-card" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; cursor: pointer;">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">⚙️ Génération TL</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Créer l'arborescence de traduction</div>
                </a>
                <a href="#gen-extraction-config" class="nav-card" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; cursor: pointer;">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🔧 Extraction Config</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Trouver les textes oubliés par le SDK</div>
                </a>
                <a href="#gen-combinaison" class="nav-card" style="display: block; padding: 12px 16px; background: var(--button-bg); border-radius: 6px; text-decoration: none; color: var(--text-color); border: 1px solid var(--border-color); transition: all 0.3s ease; cursor: pointer;">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🔄 Combinaison & Division</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Fusionner ou diviser des fichiers</div>
                </a>
            </div>
        </div>
        
        <style>
        .quick-nav-section a:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transform: translateY(-2px);
            border-color: var(--accent);
        }}
        </style>
        
        <!-- VUE D'ENSEMBLE -->
        <div class="section" id="gen-vue-ensemble">
            <h2>🎮 Générateur Ren'Py - Vue d'ensemble</h2>
            
            <p>Le <strong>Générateur Ren'Py</strong> est une interface séparée qui vous permet de gérer l'infrastructure complète de votre projet de traduction. Contrairement à l'<strong>Interface Principale</strong> qui traite les fichiers un par un, le Générateur orchestre les opérations globales.</p>
            
            <h3>📍 Comment accéder au Générateur</h3>
            
            {generator._get_image_html("04_generator", "001", "Accès au Générateur depuis l'interface principale", "Bouton Générateur Ren'Py dans l'onglet PRÉPARATION")}
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--accent); margin: 20px 0;">
                <h4 style="margin-top: 0;">🚀 Accès rapide</h4>
                <ol style="margin-bottom: 0;">
                    <li>Dans l'interface principale, cliquez sur l'onglet <strong>PRÉPARATION</strong> (bleu)</li>
                    <li>Cliquez sur le bouton <strong>🎮 Générateur Ren'Py</strong></li>
                    <li>Une nouvelle fenêtre s'ouvre avec le Générateur</li>
                </ol>
            </div>
            
            <h3>🖥️ Vue d'ensemble de l'interface</h3>
            
            {generator._get_image_html("04_generator/extraction_rpa", "001", "Vue d'ensemble du Générateur", "Fenêtre complète du Générateur avec l'onglet Extraction RPA actif")}
            
            <p>L'interface du Générateur s'organise en <strong>5 onglets principaux</strong> accessibles en haut de la fenêtre. Chaque onglet regroupe des fonctionnalités spécifiques pour gérer différents aspects de votre projet de traduction.</p>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--info); margin: 15px 0;">
                <p style="margin: 0;"><strong>ℹ️ À noter :</strong> L'onglet <strong>📊 Extraction Résultats</strong> n'apparaît que si vous avez effectué une analyse d'extraction Config. Pas d'inquiétude s'il est absent au premier lancement !</p>
            </div>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; margin: 20px 0;">
                <h3 style="margin-top: 0;">📋 Les 5 sous-onglets principaux</h3>
                <ul style="margin-bottom: 0;">
                    <li><strong>📦 Extraction & Compilation RPA</strong> - Décompile les archives .rpa et .rpyc du jeu pour accéder aux scripts source</li>
                    <li><strong>⚙️ Génération TL</strong> - Crée l'arborescence tl/[langue]/ avec modules français (sélecteur de langue, console, polices)</li>
                    <li><strong>🔧 Extraction Config</strong> - Trouve des textes non détectés par le SDK officiel avec patterns intégrés et regex personnalisés</li>
                    <li><strong>📊 Extraction Résultats</strong> - Visualise et sélectionne les textes détectés par catégories (Auto-safe, Textbuttons, Text Elements)</li>
                    <li><strong>🔄 Combinaison & Division</strong> - Fusionne plusieurs fichiers de traduction en un seul, puis redivise le fichier combiné nouvellement traduit</li>
        </ul>
            </div>
            
            <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(74, 144, 226, 0.1) 100%); padding: 15px; border-radius: 8px; border-left: 4px solid var(--success); margin: 20px 0;">
                <h4 style="margin-top: 0;">💡 Bon à savoir</h4>
                <p style="margin-bottom: 0;">Le Générateur nécessite qu'un projet Ren'Py soit sélectionné dans la section <strong>"Configuration du projet"</strong> de l'interface principale. Toutes les opérations s'appliquent directement au projet configuré.</p>
        </div>
    </div>

        <!-- SECTION 1 : EXTRACTION & COMPILATION RPA -->
    <div class="section" id="gen-extraction-rpa">
            <h2>📦 Extraction RPA/RPYC & Compilation RPA</h2>
            
            <h3>🎯 À quoi ça sert ?</h3>
            <p>Cet onglet orchestre l'extraction complète des archives du jeu pour accéder aux fichiers source (.rpy). Il gère deux opérations cruciales :</p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--accent);">
                    <h4 style="margin-top: 0;">📂 Extraction RPA/RPYC</h4>
                    <p style="margin-bottom: 0;">Extrait les archives .rpa et décompile les fichiers .rpyc pour obtenir les scripts source .rpy lisibles et modifiables.</p>
            </div>
            
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--accent);">
                    <h4 style="margin-top: 0;">🛠️ Construction RPA Personnalisée</h4>
                    <p style="margin-bottom: 0;">Recompile vos traductions en archives .rpa optimisées pour distribution ou test dans le jeu original.</p>
            </div>
        </div>
        
            <h3>❓ Aide sur les limitations de chemins</h3>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--error); margin: 20px 0;">
                <h4 style="margin-top: 0;">🚫 Chemins non supportés</h4>
                <p>Les chemins contenant des <strong>crochets [ ]</strong> ne sont pas supportés par les modules Python des outils d'extraction (unrpyc). Cette limitation s'applique à <strong>l'extraction RPA/RPYC</strong> et à la <strong>construction RPA personnalisée</strong>.</p>
                <p><strong>Exemples problématiques :</strong></p>
                <ul>
                    <li>❌ <code>C:/Jeux/Mon Jeu [v1.0]/</code></li>
                    <li>❌ <code>D:/[Backup] Projets/MonProjet/</code></li>
                    <li>❌ <code>/home/user/Jeux [Steam]/MonJeu/</code></li>
        </ul>
                <p style="margin-bottom: 0;"><strong>💡 Solutions :</strong> Renommez le dossier pour retirer les crochets (<code>Mon Jeu v1.0</code>) ou déplacez le projet vers un chemin sans caractères spéciaux (<code>C:/Projets/MonJeu/</code>).</p>
        </div>
        
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--info); margin: 20px 0;">
                <p style="margin: 0;"><strong>ℹ️ Aide intégrée :</strong> Un bouton <strong>"⚠ Aide chemins"</strong> en haut à droite de l'onglet affiche ces limitations directement dans l'application si nécessaire.</p>
            </div>
            
            <h3>📂 Section Extraction RPA/RPYC</h3>
            
            {generator._get_image_html("04_generator/extraction_rpa", "002", "Onglet Extraction RPA - Vue complète", "Interface d'extraction avec projet configuré et options disponibles")}
            
            <h4>🔧 Workflow en 3 phases</h4>
            <ol>
                <li><strong>Préparation automatique :</strong> Téléchargement et configuration des outils (unrpyc v1/v2, rpatool, Python embedded)</li>
                <li><strong>Extraction intelligente :</strong> Détection automatique de la version Ren'Py et choix de la méthode optimale</li>
                <li><strong>Nettoyage et finalisation :</strong> Suppression des outils temporaires et options de post-traitement</li>
        </ol>
        
            <h4>Options principales :</h4>
        <ul>
                <li><strong>☑️ Supprimer les fichiers RPA après extraction :</strong> Économise l'espace disque en supprimant automatiquement les archives sources après extraction réussie</li>
                <li><strong>🚀 Démarrer l'extraction :</strong> Lance le processus complet avec détection automatique des outils nécessaires</li>
        </ul>
        
            <h4>🧠 Détection intelligente automatique</h4>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px;">
                    <h5 style="margin-top: 0; color: var(--accent);">🔍 Version Ren'Py</h5>
                    <p><strong>Méthode :</strong> Analyse de script_version.txt puis fallback sur analyse binaire des .rpyc</p>
                    <p style="margin-bottom: 0;"><strong>Choix automatique :</strong> unrpyc v1 (Ren'Py 6/7) ou v2 (Ren'Py 8+)</p>
            </div>
            
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px;">
                    <h5 style="margin-top: 0; color: var(--accent);">🐍 Python Compatible</h5>
                    <p><strong>v1 :</strong> Python 2.7 embedded pour les anciens jeux</p>
                    <p style="margin-bottom: 0;"><strong>v2 :</strong> Python 3.11 embedded pour les jeux récents</p>
            </div>
            
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px;">
                    <h5 style="margin-top: 0; color: var(--accent);">🔄 Stratégie Fallback</h5>
                    <p style="margin-bottom: 0;">Si la première tentative échoue massivement, essai automatique avec l'autre version d'unrpyc</p>
            </div>
        </div>
        
            <h3>🛠️ Section Construction RPA Personnalisée</h3>
            
            {generator._get_image_html("04_generator/extraction_rpa", "003", "Configuration construction RPA", "Interface de paramétrage pour créer une archive RPA personnalisée")}
            
            <h4>Configuration avancée :</h4>
            
            <h5>🌐 Sélection de langue :</h5>
            <ul>
                <li><strong>🔍 Bouton "Scanner les langues" :</strong> Détecte automatiquement les dossiers tl/ disponibles dans le projet</li>
                <li><strong>⭐ Priorité intelligente :</strong> "french" apparaît en premier s'il existe, sinon tri alphabétique</li>
                <li><strong>✅ Validation :</strong> Seuls les dossiers contenant des fichiers exploitables sont listés</li>
        </ul>
        
            <h5>📦 Types de fichiers inclus automatiquement :</h5>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 12px; border-radius: 6px; text-align: center;">
                    <div style="font-size: 1.5em; margin-bottom: 5px;">📄</div>
                    <strong>Scripts</strong>
                    <div style="font-size: 0.9em; opacity: 0.8;">.rpy, .rpyc</div>
            </div>
                <div style="background: var(--card-bg); padding: 12px; border-radius: 6px; text-align: center;">
                    <div style="font-size: 1.5em; margin-bottom: 5px;">🖼️</div>
                    <strong>Images</strong>
                    <div style="font-size: 0.9em; opacity: 0.8;">.jpg, .png, .webp</div>
            </div>
                <div style="background: var(--card-bg); padding: 12px; border-radius: 6px; text-align: center;">
                    <div style="font-size: 1.5em; margin-bottom: 5px;">🎵</div>
                    <strong>Audio</strong>
                    <div style="font-size: 0.9em; opacity: 0.8;">.ogg, .mp3</div>
            </div>
                <div style="background: var(--card-bg); padding: 12px; border-radius: 6px; text-align: center;">
                    <div style="font-size: 1.5em; margin-bottom: 5px;">🔤</div>
                    <strong>Polices</strong>
                    <div style="font-size: 0.9em; opacity: 0.8;">.ttf, .otf</div>
            </div>
        </div>
        
            <h3>⚡ Déroulement des opérations</h3>
            
            {generator._get_image_html("04_generator/extraction_rpa", "004", "Extraction en cours", "Interface pendant l'extraction avec barre de progression et statut détaillé")}
            
            <h4>Phase d'extraction :</h4>
            <ol>
                <li><strong>Initialisation (0-10%) :</strong> Téléchargement automatique des outils si nécessaire</li>
                <li><strong>Extraction RPA (10-35%) :</strong> Décompression des archives avec rpatool</li>
                <li><strong>Détection version (35-40%) :</strong> Analyse intelligente pour choisir unrpyc v1 ou v2</li>
                <li><strong>Décompilation RPYC (40-85%) :</strong> Conversion des binaires en source avec fallback automatique</li>
                <li><strong>Nettoyage (85-100%) :</strong> Suppression des outils temporaires et finalisation</li>
        </ol>
        
            <h3>📊 Résultats et rapports</h3>
        
            {generator._get_image_html("04_generator/extraction_rpa", "005", "Popup de résultats détaillé", "Fenêtre de résultats après extraction avec statistiques et temps d'exécution")}
            
            <p>Si le mode <strong>"Popup détaillé"</strong> est activé, une fenêtre affiche à la fin de l'opération :</p>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--success);">
                    <h5 style="margin-top: 0;">✅ Extraction réussie</h5>
                    <ul style="margin-bottom: 0;">
                        <li>Nombre d'archives RPA extraites</li>
                        <li>Fichiers RPYC convertis/ignorés/échoués</li>
                        <li>Temps total d'exécution</li>
                        <li>Statistiques de fallback si applicable</li>
                </ul>
            </div>
            
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--error);">
                    <h5 style="margin-top: 0;">❌ Gestion d'échecs</h5>
                    <ul style="margin-bottom: 0;">
                        <li>Lien vers la méthode alternative (UnRen.bat)</li>
                        <li>Détail des erreurs rencontrées</li>
                        <li>Suggestions de résolution</li>
                </ul>
            </div>
        </div>
    </div>

        <!-- SECTION 2 : GÉNÉRATION TL -->
        <div class="section" id="gen-generation-tl">
            <h2>⚙️ Génération TL - Guide Détaillé</h2>
            
            {generator._get_image_html("04_generator/generator_tl", "001", "Onglet Génération - Vue complète", "Interface complète avec configuration langue, options et polices GUI")}
            
            <h3>🎯 À quoi ça sert ?</h3>
            <p>L'onglet <strong>Génération</strong> est votre centre de contrôle pour créer l'arborescence de traduction complète (dossier <code>tl/[langue]/</code>) avec tous les fichiers nécessaires. Il combine la génération de base avec des modules optionnels selon vos besoins.</p>
            
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; text-align: center; border: 2px solid var(--border-color);">
                    <div style="font-size: 2em; margin-bottom: 10px;">⚙️</div>
                    <strong>Configuration de base</strong>
                    <div style="font-size: 0.9em; opacity: 0.8; margin-top: 5px;">Langue cible et options générales</div>
        </div>
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; text-align: center; border: 2px solid var(--border-color);">
                    <div style="font-size: 2em; margin-bottom: 10px;">🎨</div>
                    <strong>Personnalisation avancée</strong>
                    <div style="font-size: 0.9em; opacity: 0.8; margin-top: 5px;">Polices GUI et modules français</div>
                </div>
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; text-align: center; border: 2px solid var(--border-color);">
                    <div style="font-size: 2em; margin-bottom: 10px;">🚀</div>
                    <strong>Génération ciblée</strong>
                    <div style="font-size: 0.9em; opacity: 0.8; margin-top: 5px;">Choix du niveau de traitement selon tes besoins</div>
                </div>
        </div>
        
            <h3>🖥️ Configuration de base</h3>
            
            <h4>🌐 Langue cible avec assistance</h4>
            <ul>
                <li><strong>📝 Champ de saisie :</strong> Tapez le nom de dossier souhaité (ex: "french", "spanish", "german", ou n'importe quel nom personnalisé)</li>
                <li><strong>❓ Bouton d'aide :</strong> Affiche des exemples de noms de dossiers couramment utilisés</li>
                <li><strong>🔄 Auto-complétion intelligente :</strong> Synchronisation automatique avec l'onglet Combinaison</li>
        </ul>
        
            <h4>📋 Options d'intégration</h4>
            
            {generator._get_image_html("04_generator/generator_tl", "002", "Options d'intégration", "Grille avec cases à cocher et boutons d'aide alignés")}
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px;">
                    <h5 style="margin-top: 0; color: var(--accent);">⚙️ Bouton Options Screen Preferences</h5>
                    <p><strong>🎯 Fonction :</strong> Ouvre une fenêtre de configuration avancée</p>
                    <p><strong>💡 Permet de :</strong> Sélecteur de langue, contrôle taille texte, personnalisation textbox</p>
                    <p style="margin-bottom: 0;"><strong>❓ Aide :</strong> Détaille toutes les options configurables (voir section suivante)</p>
            </div>
            
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px;">
                    <h5 style="margin-top: 0; color: var(--accent);">📚 Common.rpy français</h5>
                    <p><strong>☑️ Case :</strong> "Ajouter le common.rpy"</p>
                    <p><strong>💡 Action :</strong> Interface Ren'Py de base en français (disponible uniquement pour "french")</p>
                    <p style="margin-bottom: 0;"><strong>❓ Aide :</strong> Détail du contenu inclus (menus, messages système)</p>
            </div>
            
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px;">
                    <h5 style="margin-top: 0; color: var(--accent);">🖼️ Screen.rpy français</h5>
                    <p><strong>☑️ Case :</strong> "Ajouter le screen.rpy"</p>
                    <p><strong>💡 Action :</strong> Écrans d'interface traduits (disponible uniquement pour "french")</p>
                    <p style="margin-bottom: 0;"><strong>❓ Aide :</strong> Structure et éléments visuels inclus</p>
            </div>
            
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px;">
                    <h5 style="margin-top: 0; color: var(--accent);">🛠️ Console développeur</h5>
                    <p><strong>☑️ Case :</strong> "Activer la console développeur"</p>
                    <p><strong>💡 Action :</strong> Active config.developer et config.console pour la langue</p>
                    <p style="margin-bottom: 0;"><strong>❓ Aide :</strong> Code exact inséré et avantages pour le debug</p>
            </div>
        </div>
        
            <h4>⚙️ Options Screen Preferences (fenêtre modale)</h4>
            
            {generator._get_image_html("04_generator/generator_tl", "005", "Fenêtre modale Options Screen Preferences", "Fenêtre de configuration avancée des fonctionnalités à intégrer au jeu")}
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--info); margin: 20px 0;">
                <p>En cliquant sur le bouton <strong>"Options screen preferences"</strong>, une fenêtre modale s'ouvre pour configurer des fonctionnalités avancées à intégrer dans le menu Préférences du jeu :</p>
                <ul>
                    <li><strong>📺 Sélecteur de langue :</strong> Permet au joueur de changer la langue depuis le menu Préférences</li>
                    <li><strong>📏 Contrôle de taille du texte :</strong> Système intelligent (contrôle précis dialogue ou global selon le screen say)</li>
                    <li><strong>🎨 Personnalisation textbox :</strong> Opacité (0-100%), décalage vertical, épaisseur du contour</li>
        </ul>
                <p><strong>💡 Note :</strong> Le système génère automatiquement le module 99_Z_ScreenPreferences.rpy selon les cases cochées dans cette fenêtre.</p>
                <p style="margin-bottom: 0;"><strong>⚠️ Avertissement :</strong> Ce système est optimisé pour un menu Préférences classique. Le résultat sur un menu personnalisé (custom) est incertain et peut nécessiter des ajustements manuels.</p>
            </div>
        
            <h3>🎨 Section Polices GUI (facultative)</h3>
            
            <h4>👀 Aperçu des polices</h4>
            
            {generator._get_image_html("04_generator/generator_tl", "003", "Aperçu des polices", "Sélecteur avec texte de test français pour prévisualiser les polices")}
            
            <p>Zone de prévisualisation avec le texte test : <em>"Voix ambiguë d'un cœur qui au zéphyr préfère les jattes de kiwis."</em></p>
            <ul>
                    <li><strong>📋 Sélecteur de police :</strong> Liste déroulante avec toutes les polices système compatibles</li>
                    <li><strong>➕ Polices personnalisées :</strong> Vous pouvez ajouter vos propres polices au projet si nécessaire</li>
                    <li><strong>⚡ Aperçu en temps réel :</strong> Le texte change immédiatement selon la police sélectionnée</li>
                    <li><strong>🔤 Test d'accents :</strong> Les polices par défaut supportent les accents français. Pour les polices personnalisées, ce test permet de vérifier leur compatibilité</li>
        </ul>
        
            <h4>🎛️ Configuration individuelle</h4>
            
            {generator._get_image_html("04_generator/generator_tl", "004", "Grille de polices GUI", "Configuration individuelle des 5 éléments GUI avec cases et listes déroulantes alignées")}
            
            <p>Chaque élément GUI peut être configuré séparément :</p>
            
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 12px; border-radius: 6px; border-left: 3px solid var(--accent);">
                    <h5 style="margin: 0 0 8px 0;">💬 Texte principal</h5>
                    <p style="margin: 0; font-size: 0.9em;">Police utilisée pour tous les dialogues des personnages</p>
            </div>
                <div style="background: var(--card-bg); padding: 12px; border-radius: 6px; border-left: 3px solid var(--accent);">
                    <h5 style="margin: 0 0 8px 0;">👤 Noms des personnages</h5>
                    <p style="margin: 0; font-size: 0.9em;">Police pour l'affichage des noms au-dessus des dialogues</p>
            </div>
                <div style="background: var(--card-bg); padding: 12px; border-radius: 6px; border-left: 3px solid var(--accent);">
                    <h5 style="margin: 0 0 8px 0;">🖥️ Interface utilisateur</h5>
                    <p style="margin: 0; font-size: 0.9em;">Police pour les menus, préférences et éléments d'interface</p>
            </div>
                <div style="background: var(--card-bg); padding: 12px; border-radius: 6px; border-left: 3px solid var(--accent);">
                    <h5 style="margin: 0 0 8px 0;">📘 Boutons généraux</h5>
                    <p style="margin: 0; font-size: 0.9em;">Police pour les boutons de navigation et d'action</p>
                </div>
                <div style="background: var(--card-bg); padding: 12px; border-radius: 6px; border-left: 3px solid var(--accent);">
                    <h5 style="margin: 0 0 8px 0;">🎯 Boutons de choix</h5>
                    <p style="margin: 0; font-size: 0.9em;">Police spécifique pour les choix de dialogue du joueur</p>
            </div>
        </div>
        
            <h3>⚡ Boutons d'action</h3>
            
            {generator._get_image_html("04_generator/generator_tl", "006", "Focus sur les boutons d'action", "Boutons de génération avec leurs fonctions spécifiques")}
            
            <p>Les boutons d'action sont organisés en <strong>2 lignes</strong> pour une navigation claire :</p>
            
            <h4>📋 Ligne 1 : Génération complète</h4>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border: 2px solid var(--border-color);">
                    <h5 style="margin-top: 0; color: var(--accent);">⚡ Générer + options cochées</h5>
                    <p><strong>Action :</strong> Génération complète prenant en compte toutes les cases cochées (principales et facultatives)</p>
                    <p style="margin-bottom: 0;"><strong>Usage :</strong> Configuration complète en une fois avec tous les modules sélectionnés</p>
            </div>
            
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border: 2px solid var(--border-color);">
                    <h5 style="margin-top: 0; color: var(--accent);">🔧 Générer les traductions</h5>
                    <p><strong>Action :</strong> Génération classique uniquement (fichiers de base Ren'Py)</p>
                    <p style="margin-bottom: 0;"><strong>Usage :</strong> Première utilisation, génération standard sans modules supplémentaires</p>
            </div>
            </div>
            
            <h4>🛠️ Ligne 2 : Modules spécifiques</h4>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 12px; border-radius: 6px; border: 2px solid var(--border-color);">
                    <h5 style="margin-top: 0; color: var(--accent);">🎨 Appliquer polices</h5>
                    <p style="margin-bottom: 0; font-size: 0.9em;">Applique SEULEMENT les polices GUI sélectionnées</p>
            </div>
            
                <div style="background: var(--card-bg); padding: 12px; border-radius: 6px; border: 2px solid var(--border-color);">
                    <h5 style="margin-top: 0; color: var(--accent);">⚙️ Créer Screen Pref</h5>
                    <p style="margin-bottom: 0; font-size: 0.9em;">Génère 99_Z_ScreenPreferences.rpy</p>
            </div>
            
                <div style="background: var(--card-bg); padding: 12px; border-radius: 6px; border: 2px solid var(--border-color);">
                    <h5 style="margin-top: 0; color: var(--accent);">🛠️ Console dev</h5>
                    <p style="margin-bottom: 0; font-size: 0.9em;">Active la console développeur</p>
            </div>
            
                <div style="background: var(--card-bg); padding: 12px; border-radius: 6px; border: 2px solid var(--border-color);">
                    <h5 style="margin-top: 0; color: var(--accent);">🔄 Réinitialiser</h5>
                    <p style="margin-bottom: 0; font-size: 0.9em;">Réinitialise toutes les options</p>
            </div>
        </div>
        
            <h3>🎬 Démonstration en action</h3>
            
            {generator._get_image_html("04_generator/generator_tl", "007", "Génération en cours", "Animation montrant l'exécution de la génération avec progression")}
            
            <p>Ce GIF animé montre le déroulement complet d'une opération de génération, avec la progression en temps réel et les différentes étapes du processus.</p>
    </div>

        <!-- SECTION 3 : EXTRACTION CONFIG -->
    <div class="section" id="gen-extraction-config">
            <h2>🔧 Extraction des Textes Oubliés - Guide Complet</h2>
            
            {generator._get_image_html("04_generator/extraction_config_results", "001", "Aperçu de l'onglet Extraction Config", "Vue complète de l'interface avec toutes les sections configurables")}
            
            <h3>🎯 À quoi ça sert ?</h3>
            <p>Cette fonctionnalité trouve et extrait <strong>des textes non détectés par le SDK Ren'Py officiel</strong>. Grâce à des patterns de détection personnalisables (textbuttons, input, notify, etc.), elle analyse en profondeur tous les fichiers pour identifier les chaînes traduisibles manquées.</p>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--warning); margin: 20px 0;">
                <h5 style="margin-top: 0;">⚠️ Important à savoir</h5>
                <p style="margin-bottom: 0;">Ce système n'est pas parfait et ne détecte pas tous les textes. Il s'agit d'une aide précieuse mais qui nécessite une vérification manuelle des résultats pour garantir leur pertinence.</p>
        </div>
        
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--info); margin: 20px 0;">
                <h4 style="margin-top: 0;">💡 Pourquoi c'est nécessaire</h4>
                <p style="margin-bottom: 0;">Le SDK officiel ne génère que les traductions des <strong>dialogues principaux, des choix</strong> et des éléments marqués avec <code>_()</code> ou <code>__()</code>. Mais les jeux contiennent aussi de nombreux autres textes (textbuttons, input, notify, variables avec tooltips, etc.) qui ne sont pas automatiquement détectés. Cette fonction comble cette lacune.</p>
        </div>
        
            <h3>🔄 Workflow en 2 étapes</h3>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; text-align: center; border-top: 4px solid var(--accent);">
                    <div style="font-size: 2em; margin-bottom: 10px;">1️⃣</div>
                    <strong>Configuration et Analyse (Onglet Extraction Config)</strong>
                    <div style="font-size: 0.9em; opacity: 0.8; margin-top: 5px;">Paramétrage de l'analyse : langue de référence, patterns de détection (textbutton, input, notify, etc.), patterns personnalisés, exclusions puis lancement</div>
        </div>
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; text-align: center; border-top: 4px solid var(--accent);">
                    <div style="font-size: 2em; margin-bottom: 10px;">2️⃣</div>
                    <strong>Résultats et génération (Onglet Extraction Résultats)</strong>
                    <div style="font-size: 0.9em; opacity: 0.8; margin-top: 5px;">Visualisation par catégories, sélection manuelle et création du fichier final</div>
                </div>
        </div>
        
            <h3>🌐 Sélection de langue</h3>
            
            {generator._get_image_html("04_generator/extraction_config_results", "002", "Sélection de la langue à analyser", "Menu déroulant avec détection automatique des langues disponibles")}
            
            <h4>🔍 Détection automatique des langues</h4>
            <ul>
                <li><strong>🔎 Scan intelligent :</strong> Le bouton "Scanner les langues" détecte automatiquement toutes les langues ayant des fichiers .rpy dans le dossier <code>tl/</code></li>
                <li><strong>⭐ Priorité française :</strong> Si une langue "french" existe, elle apparaît en premier dans la liste</li>
                <li><strong>✅ Validation :</strong> Seules les langues contenant effectivement des fichiers de traduction sont proposées</li>
        </ul>
        
            <h4>🎯 Rôle de la langue sélectionnée</h4>
            <p>La langue sélectionnée sert de <strong>référence anti-doublons</strong>. L'analyse compare les textes détectés avec ceux déjà traduits dans cette langue pour éviter les redondances.</p>
            
            <h3>🎯 Système de détection avancé</h3>
            
            <p>Le système utilise un <strong>ensemble de patterns de détection</strong> pour identifier les textes traduisibles dans votre projet.</p>
            
            <div style="background: linear-gradient(135deg, rgba(74, 144, 226, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); padding: 20px; border-radius: 8px; border: 2px solid var(--success); margin: 20px 0;">
                <h4 style="margin-top: 0; color: var(--success);">🔸 Patterns de détection intégrés</h4>
                <p><strong>✨ Types de patterns détectés :</strong></p>
                <ul>
                    <li><strong>character :</strong> Définitions de personnages (Character(), DynamicCharacter())</li>
                    <li><strong>input :</strong> Saisies utilisateur (renpy.input(), Input())</li>
                    <li><strong>notify :</strong> Notifications à l'écran (notify(), renpy.notify())</li>
                    <li><strong>textbutton :</strong> Boutons d'interface interactifs</li>
                    <li><strong>text :</strong> Éléments texte divers (show text, text parameters)</li>
                    <li><strong>+ Patterns personnalisés :</strong> Tes propres regex pour cas spécifiques</li>
        </ul>
                <p style="margin-bottom: 0;"><strong>📋 Résultat :</strong> Détection complète et classification intelligente en 3 catégories</p>
        </div>
        
            <h4>📊 Classification intelligente des résultats</h4>
            <ul>
                <li><strong>🟢 Auto-safe :</strong> Textes avec confiance 100% (Character(), input(), notify() confirmés) + patterns personnalisés</li>
                <li><strong>🟡 Textbuttons :</strong> Boutons d'interface détectés nécessitant vérification</li>
                <li><strong>🟡 Text elements :</strong> Éléments texte divers à examiner manuellement</li>
        </ul>
        
            <h3>🚫 Système d'exclusions intelligent</h3>
            
            {generator._get_image_html("04_generator/extraction_config_results", "003", "Configuration des fichiers à exclure", "Interface de gestion des exclusions avec liste éditable et exclusions par défaut")}
        
            <h4>🔒 Exclusions automatiques (système)</h4>
            <p>Le système exclut automatiquement ses propres fichiers générés :</p>
        <ul>
                <li><code>99_Z_ScreenPreferences.rpy</code> - Sélecteur de langue et options Screen Preferences générés</li>
                <li><code>99_Z_Console.rpy</code> - Console développeur générée</li>
                <li><code>99_Z_FontSystem.rpy</code> - Système de polices GUI généré</li>
        </ul>
        
            <h4>📋 Exclusions recommandées (configurables)</h4>
            <ul>
                <li><code>common.rpy</code> - Fichier système Ren'Py (exclu par défaut utilisateur)</li>
                <li><code>screens.rpy, gui.rpy, options.rpy</code> - Fichiers de configuration de base</li>
                <li>Fichiers de sauvegarde ou temporaires du projet</li>
        </ul>
        
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--success); margin: 20px 0;">
                <h5 style="margin-top: 0;">💡 Conseil d'utilisation</h5>
                <p style="margin-bottom: 0;">Commencez avec les exclusions par défaut, puis ajustez selon vos besoins. Un fichier exclu ne sera jamais analysé.</p>
        </div>
        
            <h4>🛡️ Exclusions automatiques avancées</h4>
            <p>Le système reconnaît automatiquement et exclut :</p>
            <ul>
                <li><strong>Variables isolées :</strong> <code>[player_name]</code> seul sur une ligne</li>
                <li><strong>Balises techniques :</strong> <code>{{fast}}</code>, <code>{{nw}}</code>, etc.</li>
                <li><strong>Ponctuations expressives :</strong> !!!, ???, ...</li>
                <li><strong>Onomatopées courtes :</strong> Ah!, Oh?, Mmh</li>
            </ul>
            
            <h3>🔧 Patterns Regex Personnalisés - Interface Regex101-like</h3>
            
            {generator._get_image_html("04_generator/extraction_config_results", "004", "Treeview des Regex personnalisés", "Liste des patterns avec état activé/désactivé, boutons d'action et exemple intégré")}
            
            <h4>🎯 À quoi ça sert ?</h4>
            <p>Les <strong>Patterns Regex Personnalisés</strong> vous permettent de définir vos propres expressions régulières pour détecter des textes spécifiques dans vos fichiers Ren'Py. Chaque groupe de capture <code>()</code> crée un bloc old/new séparé dans les résultats.</p>
            
            {generator._get_image_html("04_generator/extraction_config_results", "005", "Fenêtre modale Pattern Regex", "Interface complète avec coloration syntaxique, zone de test et feedback temps réel")}
            
            
            <div style="background: linear-gradient(135deg, rgba(74, 144, 226, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); padding: 20px; border-radius: 8px; border: 2px solid var(--success); margin: 20px 0;">
                <h4 style="margin-top: 0; color: var(--success);">✨ Interface Regex101-like</h4>
                <p><strong>🎨 Coloration syntaxique :</strong> Groupes, métacaractères, quantificateurs colorés en temps réel</p>
                <p><strong>🔍 Surbrillance des correspondances :</strong> Feedback visuel immédiat dans la zone de test</p>
                <p><strong>✅ Validation instantanée :</strong> Vérification de la syntaxe regex pendant la saisie</p>
                <p><strong>📊 Formatage des résultats :</strong> Affichage structuré des groupes capturés avec indentation</p>
                <p style="margin-bottom: 0;"><strong>💾 Sauvegarde persistante :</strong> Patterns et textes de test conservés entre les sessions</p>
            </div>
            
            <h4>🚀 Workflow simplifié</h4>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-top: 4px solid var(--accent);">
                    <h5 style="margin-top: 0;">➕ Ajouter</h5>
                    <p><strong>Action :</strong> Ouvre la fenêtre complètement vierge</p>
                    <p style="margin-bottom: 0;"><strong>Usage :</strong> Créer un nouveau pattern depuis zéro</p>
            </div>
            
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-top: 4px solid var(--success);">
                    <h5 style="margin-top: 0;">📚 Exemple intégré</h5>
                    <p><strong>Action :</strong> "Exemple Regex" toujours présent dans la liste</p>
                    <p style="margin-bottom: 0;"><strong>Usage :</strong> Cliquer sur la regex d'exemple puis sur "Modifier" pour comprendre le fonctionnement</p>
            </div>
        </div>
        
            <h4>🎯 Exemple pratique</h4>
            <p><strong>Pattern :</strong> <code>"QID_[^"]+\"\\s*:\\s*\\[\\s*"([^"]+)",\\s*"([^"]+)".*\\["hint",\\s*"([^"]+)"</code></p>
            <p><strong>Flags :</strong> <code>gms</code> (global, multiligne, dotall)</p>
            <p><strong>Résultat :</strong> 3 groupes → 3 blocs old/new dans les résultats</p>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--info); margin: 20px 0;">
                <h5 style="margin-top: 0;">💡 Conseil d'utilisation</h5>
                <p style="margin-bottom: 0;">Commencez par modifier l'exemple intégré pour comprendre le système, puis créez vos propres patterns selon vos besoins spécifiques.</p>
            </div>
            
            <h3>🚀 Lancement de l'analyse</h3>
            
            {generator._get_image_html("04_generator/extraction_config_results", "007", "Focus zone lancement analyse", "Interface de démarrage de l'analyse avec options et boutons d'action")}
            
            <h3>📊 Onglet Extraction Résultats - Visualisation et Sélection</h3>
            
            {generator._get_image_html("04_generator/extraction_config_results", "008", "Aperçu de l'onglet Extraction Résultats", "Vue complète avec les 3 catégories, statistiques et boutons d'action")}
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--info); margin: 20px 0;">
                <h5 style="margin-top: 0;">ℹ️ À noter</h5>
                <p style="margin-bottom: 0;">Cet onglet n'apparaît qu'après avoir effectué une analyse d'extraction Config. Il regroupe tous les résultats détectés pour une sélection précise avant génération.</p>
            </div>
            
            <h3>📈 Statistiques d'analyse</h3>
            
            {generator._get_image_html("04_generator/extraction_config_results", "009", "Focus sur les statistiques", "Métriques détaillées avec fichiers analysés, textes existants et résultats de détection")}
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--accent);">
                    <h5 style="margin-top: 0;">📊 Analyse de base</h5>
                    <ul style="margin-bottom: 0;">
                        <li>Nombre de fichiers analysés</li>
                        <li>Textes existants dans tl/ (anti-doublon)</li>
                </ul>
            </div>
            
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--success);">
                    <h5 style="margin-top: 0;">🎯 Résultats de détection</h5>
                    <ul style="margin-bottom: 0;">
                        <li>Total de nouveaux textes détectés</li>
                </ul>
            </div>
        </div>
        
            <h4>📐 Organisation visuelle en colonnes</h4>
            
            {generator._get_image_html("04_generator/extraction_config_results", "010", "Focus sur les 3 catégories principales", "Colonnes avec boutons Tout Cocher/Décocher, cases cochées/décochées et barres de scroll")}
            
            <p>L'interface des résultats s'organise en <strong>3 colonnes fixes</strong> avec scroll individuel pour optimiser l'espace et la lisibilité :</p>
            
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-top: 4px solid var(--success);">
                    <h5 style="margin-top: 0; color: var(--success);">🟢 Auto-safe</h5>
                    <p><strong>Contenu :</strong> Textes à confiance 100% + patterns personnalisés</p>
                    <p><strong>Sélection par défaut :</strong> Tous cochés</p>
                    <p style="margin-bottom: 0;"><strong>Action recommandée :</strong> Extraction automatique sans vérification</p>
            </div>
            
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-top: 4px solid var(--warning);">
                    <h5 style="margin-top: 0; color: var(--warning);">🟡 Textbuttons</h5>
                    <p><strong>Contenu :</strong> Boutons d'interface détectés</p>
                    <p><strong>Sélection par défaut :</strong> Non cochés</p>
                    <p style="margin-bottom: 0;"><strong>Action recommandée :</strong> Vérification manuelle conseillée</p>
            </div>
            
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-top: 4px solid var(--warning);">
                    <h5 style="margin-top: 0; color: var(--warning);">🟡 Text Elements</h5>
                    <p><strong>Contenu :</strong> Éléments texte divers</p>
                    <p><strong>Sélection par défaut :</strong> Non cochés</p>
                    <p style="margin-bottom: 0;"><strong>Action recommandée :</strong> Examen individuel nécessaire</p>
            </div>
        </div>
        
            <h4>🎮 Fonctionnalités d'interaction</h4>
            
            <ul>
                <li><strong>✅ Sélection par section :</strong> Bouton "Tout cocher/décocher" dans chaque colonne</li>
                <li><strong>📜 Scroll indépendant :</strong> Chaque colonne a sa propre barre de défilement</li>
                <li><strong>🖱️ Support molette :</strong> Défilement à la molette dans chaque section</li>
                <li><strong>📊 Affichage 2 colonnes :</strong> Textes organisés en 2 colonnes dans chaque section pour optimiser l'espace</li>
        </ul>
        
            <h3>⚡ Boutons d'action</h3>
            
            {generator._get_image_html("04_generator/extraction_config_results", "011", "Focus sur les boutons d'action", "Boutons de génération du fichier final avec options de sélection globale")}
            
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--success);">
                    <h5 style="margin-top: 0;">✅ Tout sélectionner</h5>
                    <p style="margin-bottom: 0;"><strong>Action :</strong> Coche toutes les cases de toutes les catégories</p>
            </div>
                
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--warning);">
                    <h5 style="margin-top: 0;">❌ Tout désélectionner</h5>
                    <p style="margin-bottom: 0;"><strong>Action :</strong> Décoche toutes les cases de toutes les catégories</p>
        </div>
        
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--accent);">
                    <h5 style="margin-top: 0;">💾 Générer le fichier</h5>
                    <p style="margin-bottom: 0;"><strong>Action :</strong> Crée le fichier .rpy avec tous les textes sélectionnés</p>
                </div>
            </div>
            
            <h3>💾 Génération du fichier final</h3>
            
            {generator._get_image_html("04_generator/extraction_config_results", "012", "Dialogue de sauvegarde intelligent", "Fenêtre de sauvegarde avec suggestion automatique du dossier tl/langue")}
            
            <h4>🎯 Suggestions intelligentes</h4>
            <ul>
                <li><strong>📁 Dossier automatique :</strong> Le système propose le dossier <code>tl/[langue]</code> de la langue analysée</li>
                <li><strong>📄 Nom par défaut :</strong> "textes_manquants.rpy" (modifiable selon vos besoins)</li>
                <li><strong>📋 Métadonnées complètes :</strong> Le fichier généré contient des commentaires avec contexte (projet, langue, date)</li>
        </ul>
        
            <h4>📦 Contenu du fichier généré</h4>
            <p>Structure du fichier .rpy créé :</p>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--info); margin: 20px 0;">
                <h5 style="margin-top: 0;">📄 Exemple de fichier généré</h5>
                <pre style="background: rgba(0,0,0,0.1); padding: 12px; border-radius: 6px; overflow-x: auto; font-family: 'Courier New', monospace; font-size: 0.9em;"><code># Date de génération: 12/10/2025 à 14:30:45
# Fichier d'extraction généré par RenExtract
# Projet: Game_Name

translate &lt;Langue&gt; strings:

    old "Hello world"
    new "Hello world"
    
    old "Start game"
    new "Start game"</code></pre>
            </div>
            
            <p><strong>🔄 Paires old/new :</strong> Chaque texte sélectionné génère une paire avec <code>old</code> et <code>new</code> identiques (à traduire manuellement)</p>
            <p><strong>🔡 Tri alphabétique :</strong> Les textes sont organisés par ordre alphabétique pour faciliter l'édition</p>
        
            <h3>💡 Conseils d'utilisation pratique</h3>
            
            <h4>📋 Workflow recommandé</h4>
            <ol>
                <li><strong>Première analyse :</strong> Mode Optimisé avec exclusions par défaut</li>
                <li><strong>Vérification Auto-safe :</strong> Extraire directement les textes verts (confiance 100%)</li>
                <li><strong>Examen manuel :</strong> Parcourir les Textbuttons et Text elements</li>
                <li><strong>Sélection ciblée :</strong> Ne cocher que les textes réellement utiles</li>
                <li><strong>Génération :</strong> Créer le fichier dans le bon dossier tl/</li>
                <li><strong>Test :</strong> Vérifier l'intégration dans le jeu</li>
        </ol>
        
            <h4>⚡ Astuces pour optimiser les résultats</h4>
            <ul>
                <li><strong>🛡️ Anti-doublon efficace :</strong> Assurez-vous d'avoir une langue de référence bien remplie</li>
                <li><strong>🚫 Exclusions personnalisées :</strong> Ajoutez vos fichiers de test ou temporaires</li>
        </ul>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--warning); margin: 20px 0;">
                <h5 style="margin-top: 0;">⚠️ Variables avec fonction de traduction</h5>
                <p>Certains textes détectés peuvent contenir des variables (ex: <code>[tooltip]</code>). Pour qu'ils soient traduits automatiquement, il faut créer un bloc de traduction spécifique :</p>
                <pre style="background: rgba(0,0,0,0.1); padding: 12px; border-radius: 6px; overflow-x: auto; font-family: 'Courier New', monospace; font-size: 0.9em; margin-top: 10px;"><code>old "[tooltip]"
new "[tooltip!t]"</code></pre>
                <p style="margin-bottom: 0;"><strong>💡 Résultat :</strong> La fonction <code>!t</code> active la traduction automatique de la variable lors de l'affichage dans le jeu.</p>
        </div>
    </div>

        <!-- SECTION 4 : COMBINAISON & DIVISION -->
    <div class="section" id="gen-combinaison">
            <h2>🔄 Combinaison & Division - Gestion des Fichiers</h2>
            
            {generator._get_image_html("04_generator/combination", "001", "Générateur - Combinaison", "Interface de combinaison et division de fichiers de traduction")}
            
            <h3>🎯 Objectif</h3>
            <p>Fusionne plusieurs fichiers de traduction en un seul, puis redivise le fichier combiné nouvellement traduit pour le remettre dans sa structure d'origine.</p>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--accent); margin: 20px 0;">
                <h4 style="margin-top: 0;">💡 Cas d'usage typique</h4>
                <p style="margin-bottom: 0;"><strong>🔄 Traduction optimisée :</strong> Combine tous les fichiers en un seul pour faciliter la traduction (avec un logiciel externe ou un traducteur), puis re-divise automatiquement le fichier traduit pour restaurer l'organisation originale.</p>
        </div>
        
            <h3>⚙️ Comment ça fonctionne ?</h3>
            
            <h4>🚫 Exclusion des fichiers</h4>
            <p>Avant de combiner, vous pouvez définir quels fichiers doivent être exclus de l'opération (fichiers système, fichiers spéciaux, etc.).</p>
            
            {generator._get_image_html("04_generator/combination", "002", "Zone d'exclusion des fichiers", "Configuration des fichiers à exclure de la combinaison")}
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; margin: 20px 0;">
                <p style="margin: 0;"><strong>💡 Astuce :</strong> Les fichiers système Ren'Py (common.rpy, screens.rpy, etc.) sont automatiquement exclus pour éviter les problèmes de compatibilité.</p>
            </div>
            
            <h4>🔗 Étape 1 : Combinaison</h4>
            <ol>
                <li><strong>Sélection automatique :</strong> RenExtract prend tous les fichiers du dossier, sauf ceux que vous avez exclus</li>
                <li><strong>Fusion intelligente :</strong> RenExtract combine tous les fichiers en un seul et enregistre les <strong>métadonnées</strong> (informations sur l'origine de chaque fichier)</li>
                <li><strong>Fichier unique :</strong> Vous obtenez un seul fichier à traduire, beaucoup plus simple à gérer</li>
        </ol>
        
            {generator._get_image_html("04_generator/combination", "003", "Interface de combinaison", "Dossier source et fichier de sortie pour la combinaison")}
        
            <h4>✂️ Étape 2 : Division</h4>
            <p><strong>⚠️ Important :</strong> La division <strong>ne fonctionne que sur les fichiers combinés</strong> par RenExtract, grâce aux métadonnées enregistrées lors de la combinaison.</p>
            <ol>
                <li><strong>Traduction :</strong> Une fois le fichier combiné traduit (avec votre outil de traduction préféré)</li>
                <li><strong>Re-division automatique :</strong> RenExtract utilise les métadonnées pour diviser le fichier traduit</li>
                <li><strong>Restauration complète :</strong> Vous retrouvez votre structure originale avec tous les fichiers traduits individuellement dans leurs dossiers d'origine</li>
        </ol>
        
            {generator._get_image_html("04_generator/combination", "004", "Interface de division", "Fichier combiné et dossier de sortie pour la division")}
        
            <h3>🛠️ Fonctionnalités clés</h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin: 20px 0;">
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px;">
                    <h5 style="margin-top: 0; color: var(--accent);">🔗 Combinaison avec métadonnées</h5>
                    <p>Enregistre l'origine de chaque fichier pour permettre la re-division</p>
                    <p style="margin-bottom: 0;"><strong>✅ Avantage :</strong> Aucune perte de structure</p>
        </div>
        
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px;">
                    <h5 style="margin-top: 0; color: var(--accent);">✂️ Re-division intelligente</h5>
                    <p>Restaure automatiquement la structure et les dossiers d'origine</p>
                    <p style="margin-bottom: 0;"><strong>📏 Méthode :</strong> Basée sur les métadonnées du fichier combiné</p>
            </div>
            
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px;">
                    <h5 style="margin-top: 0; color: var(--accent);">🚫 Exclusions personnalisées</h5>
                    <p>Fichiers à ignorer lors de la combinaison</p>
                    <p style="margin-bottom: 0;"><strong>🎛️ Flexibilité :</strong> Contrôle total sur les fichiers à inclure</p>
            </div>
            
                <div style="background: var(--card-bg); padding: 15px; border-radius: 8px;">
                    <h5 style="margin-top: 0; color: var(--accent);">🗑️ Suppression automatique</h5>
                    <p>Les fichiers sources sont supprimés après combinaison</p>
                    <p style="margin-bottom: 0;"><strong>⚠️ Important :</strong> Sauvegarde le projet avant l'opération</p>
            </div>
        </div>
        
            <h3>🎯 Bonnes pratiques</h3>
            
            <div style="background: var(--card-bg); padding: 15px; border-radius: 8px; border-left: 4px solid var(--warning); margin: 20px 0;">
                <h4 style="margin-top: 0;">⚠️ Points importants</h4>
                <ul style="margin-bottom: 0;">
                    <li><strong>💾 Sauvegarde préalable OBLIGATOIRE :</strong> Les fichiers sources sont supprimés après combinaison, faites une sauvegarde avant !</li>
                    <li><strong>📋 Métadonnées essentielles :</strong> Ne supprimez jamais les commentaires de métadonnées dans le fichier combiné</li>
                    <li><strong>✂️ Division uniquement sur fichiers combinés :</strong> La re-division ne fonctionne que sur les fichiers créés par la fonction de combinaison</li>
                    <li><strong>🧪 Test après opération :</strong> Vérifiez que tous les fichiers ont été correctement restaurés dans leurs dossiers</li>
        </ul>
        </div>
        
            <h4>📋 Workflow recommandé</h4>
            <ol>
                <li><strong>💾 Sauvegarde :</strong> Faites une sauvegarde de votre projet avant de commencer</li>
                <li><strong>🔗 Combinaison :</strong> Fusionnez tous vos fichiers de traduction</li>
                <li><strong>⚡ Extraction :</strong> Utilisez l'application principale pour extraire les lignes traduisibles</li>
                <li><strong>📝 Traduction :</strong> Traduisez le fichier unique avec votre outil préféré</li>
                <li><strong>🔄 Reconstruction :</strong> Utilisez l'application principale pour reconstruire le fichier</li>
                <li><strong>✂️ Re-division :</strong> Divisez le fichier traduit pour restaurer la structure</li>
                <li><strong>✅ Validation :</strong> Utilisez le vérificateur de cohérence pour vérifier les traductions</li>
        </ol>
    </div>
    """
