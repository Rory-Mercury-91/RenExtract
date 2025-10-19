# ui/tutorial/content/tab_03.py
"""
Module de contenu pour l'onglet 3 : Interface Principale
Guide complet de l'interface principale de RenExtract
"""

def generate_content(generator, language=None, translations=None):
    """Génère le contenu de l'onglet Interface Principale (français uniquement)
    
    Args:
        generator: Instance du générateur avec méthodes utilitaires (_get_image_html, etc.)
        language: Non utilisé (compatibilité avec ancienne signature)
        translations: Non utilisé (compatibilité avec ancienne signature)
    
    Returns:
        str: HTML généré pour l'onglet interface principale
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # NAVIGATION RAPIDE
    # ═══════════════════════════════════════════════════════════════════════════
    
    navigation = """
        <div class="quick-nav-section" style="background: var(--card-bg); padding: 20px; margin-bottom: 30px; border-radius: 8px; border-left: 4px solid var(--accent);">
            <h3 style="margin-top: 0;">🧭 Navigation Rapide</h3>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-top: 15px;">
                <a href="#vue-ensemble" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🖥️ Vue d'ensemble</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Introduction et présentation</div>
                </a>
                <a href="#header" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">📋 Le Header</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Contrôles principaux</div>
                </a>
                <a href="#selection-projet" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">📂 Sélection Projet</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Choisir projet ou fichier</div>
                </a>
                <a href="#mode-projet" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">📁 Mode Projet</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Projet complet multi-langues</div>
                </a>
                <a href="#mode-fichier" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">📄 Mode Fichier</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Fichier unique rapide</div>
                </a>
                <a href="#onglet-preparation" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🔬 Onglet Préparation</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Générateur Ren'Py</div>
                </a>
                <a href="#onglet-actions" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">⚡ Onglet Actions</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Extraire, Reconstruire, Vérifier</div>
                </a>
                <a href="#onglet-outils" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🧰 Onglet Outils</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Rapports, Temporaires, Sauvegardes</div>
                </a>
                <a href="#zone-contenu" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">📝 Zone de Contenu</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Visualisation et collage</div>
                </a>
                <a href="#champ-sortie" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">📁 Champ de Sortie</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Où vont vos fichiers</div>
                </a>
            </div>
        </div>
        
        <style>
        .nav-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            border-color: var(--accent);
        }
        </style>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 1 : INTRODUCTION - VUE D'ENSEMBLE
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_1 = f"""
        <div class="section" id="vue-ensemble">
            <h2>🖥️ Bienvenue dans RenExtract !</h2>
            
            <h3>Popup de première ouverture</h3>
            {generator._get_image_html("03_main_interface", "001", 
                "Popup de bienvenue première ouverture", 
                "Message d'accueil affiché lors de la première utilisation de RenExtract")}
            
            <p>Lors de votre première utilisation, RenExtract affiche un message de bienvenue pour vous guider dans vos premiers pas.</p>
            
            <h3>Vue d'ensemble de l'interface</h3>
            {generator._get_image_html("03_main_interface", "002", 
                "Vue d'ensemble de l'interface principale", 
                "Capture d'écran complète de l'interface principale de RenExtract")}
            
            <p>Cette interface principale est votre espace de travail pour <strong>préparer vos fichiers de scripts Ren'Py en vue de la traduction</strong>. 
            Elle est conçue pour être intuitive et vous guider à chaque étape : extraction, reconstruction, et vérification.</p>
            
            <div class="warning-box">
                <strong>⚠️ Important</strong> : RenExtract <strong>ne traduit pas</strong> les textes ! Il prépare et structure les fichiers pour que vous puissiez 
                les traduire dans votre éditeur ou outil de traduction préféré (Excel, Notepad++, outils CAT, etc.).
            </div>
            
            <p>L'interface se compose de plusieurs zones clés :</p>
            <ul style="padding-left: 40px;">
                <li>• Le <strong>header en haut</strong> avec les boutons d'accès rapide</li>
                <li>• La <strong>zone de sélection</strong> pour choisir votre projet ou fichier</li>
                <li>• Les <strong>onglets d'actions</strong> pour lancer les différentes opérations</li>
                <li>• La <strong>zone de contenu centrale</strong> pour visualiser le code</li>
            </ul>
            
            <p>Que vous travailliez sur un <strong>projet complet</strong> avec plusieurs langues ou sur un <strong>seul fichier</strong>, 
            RenExtract s'adapte à vos besoins ! 💪</p>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 2 : LE HEADER - CONTRÔLES PRINCIPAUX
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_2 = f"""
        <div class="section" id="header">
            <h2>📋 Le Header - Contrôles Principaux</h2>
            
            {generator._get_image_html("03_main_interface", "003", 
                "Focus sur le header", 
                "Zone du header avec le titre RenExtract et les boutons Guide, Paramètres et Quitter")}
            
            <p>En haut de l'interface, vous trouverez le header avec le titre de l'application et trois boutons essentiels :</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div style="margin: 0;">
                    <h3>🎮 RenExtract [version]</h3>
                    <p>Le titre affiche la version actuelle de l'application. Toujours utile pour vérifier que vous êtes à jour !</p>
                </div>
                
                <div style="margin: 0;">
                    <h3>📖 Guide Complet</h3>
                    <p>Ce bouton ouvre justement ce guide dans votre navigateur. Vous pouvez le consulter à tout moment pour vous rafraîchir la mémoire sur une fonctionnalité.</p>
                </div>
                
                <div style="margin: 0;">
                    <h3>⚙️ Paramètres</h3>
                    <p>Ce bouton vous donne accès aux réglages de l'application : choix de l'éditeur, personnalisation du thème des boutons, 
                    comportements par défaut, etc. C'est ici que vous personnalisez RenExtract selon vos préférences.</p>
                </div>
                
                <div style="margin: 0;">
                    <h3>❌ Quitter</h3>
                    <p>Ce bouton vous permet de fermer proprement l'application. RenExtract sauvegarde automatiquement votre dernier projet ouvert 
                    pour que vous puissiez reprendre là où vous vous êtes arrêté.</p>
                </div>
            </div>
            
            <div class="tip-box">
                <strong>💡 Astuce</strong> : Prenez le temps de configurer l'application via les Paramètres dès le début. 
                Un bon réglage initial vous fera gagner beaucoup de temps par la suite !
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 3 : SÉLECTION DE PROJET
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_3_0 = f"""
        <div class="section" id="selection-projet">
            <h2>📂 Sélection de Projet</h2>
            
            {generator._get_image_html("03_main_interface", "004", 
                "Zone de sélection vide", 
                "Interface sans projet ni fichier sélectionné")}
            
            <p>Lors du premier lancement, la zone de sélection est vide. Vous avez deux options pour charger du contenu :</p>
            <ul style="padding-left: 40px;">
                <li>• <strong>📁 Projet</strong> : Pour gérer un projet Ren'Py avec plusieurs fichiers de traduction</li>
                <li>• <strong>📄 Fichier</strong> : Pour travailler rapidement sur un seul fichier <code>.rpy</code></li>
            </ul>
            
            <p><strong>🔄 Bouton Scanner</strong> : Disponible en mode projet, ce bouton permet de forcer une nouvelle analyse du projet (utile si vous avez modifié la structure manuellement).</p>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 4 : MODE PROJET COMPLET
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_3_1 = f"""
        <div class="section" id="mode-projet">
            <h2>📁 Mode Projet Complet</h2>
            
            {generator._get_image_html("03_main_interface", "005", 
                "Mode Projet avec dossier sélectionné", 
                "Interface en mode projet complet avec langue et fichier sélectionnés")}
            
            <h4>Comment ça marche ?</h4>
            <p>Ce mode est idéal pour gérer un <strong>projet Ren'Py complet</strong> avec potentiellement plusieurs langues et de nombreux fichiers.</p>
            
            <div>
                <h5>1. Sélection du projet 📁</h5>
                <p>Cliquez sur <strong>"📁 Projet"</strong> pour choisir le dossier racine de votre jeu Ren'Py.</p>
                <p><strong>💡 Astuce</strong> : Pas besoin de chercher précisément le dossier racine ! Si vous sélectionnez un sous-dossier (par exemple <code>/game/</code> ou <code>/game/tl/french/</code>), RenExtract remontera intelligemment jusqu'à la racine du projet.</p>
                <p><strong>Scan automatique</strong> : Une fois le projet détecté, RenExtract va automatiquement scanner et détecter les langues disponibles (dossiers dans <code>/game/tl/</code>), les fichiers de traduction (<code>.rpy</code>) et la structure du projet.</p>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div style="margin: 0;">
                    <h5>2. Choix de la langue 🌍</h5>
                    <p>Une fois le projet choisi, sélectionnez la langue sur laquelle vous voulez travailler dans le menu déroulant <strong>"🌍 Langue"</strong>.</p>
                </div>
                
                <div style="margin: 0;">
                    <h5>3. Sélection du fichier 📄</h5>
                    <p>Dans le menu déroulant <strong>"📄 Fichier"</strong>, choisissez le fichier spécifique que vous voulez traiter. Vous pouvez voir le nombre de lignes et votre position dans la liste.</p>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div style="margin: 0;">
                    <h5>4. 📊 Infos affichées</h5>
                    <ul style="padding-left: 40px;">
                        <li>• Le mode actif : <strong>"🔧 Mode : Projet complet"</strong></li>
                        <li>• Les détails du projet : nombre de fichiers RPY, langues disponibles</li>
                        <li>• Les statistiques : nombre de lignes, position dans la liste (ex: "1/108 fichiers")</li>
                    </ul>
                </div>
                
                <div style="margin: 0;">
                    <h5>5. ⏩ Navigation rapide</h5>
                    <p>Quand il y a plusieurs fichiers, deux boutons de navigation apparaissent :</p>
                    <ul style="padding-left: 40px;">
                        <li>• <strong>"◀️ Fichier Précédent"</strong> : retourne au fichier précédent</li>
                        <li>• <strong>"▶️ Fichier Suivant"</strong> : passe au fichier suivant</li>
                    </ul>
                    <p>Ces boutons vous permettent de naviguer rapidement sans repasser par les menus déroulants.</p>
                </div>
            </div>
            
            <div class="tip-box">
                <strong>💡 Bon à savoir</strong> : Vous pouvez scanner à nouveau votre projet avec le bouton <strong>"🔄 Scanner"</strong> 
                si vous avez ajouté des fichiers ou langues manuellement après le scan automatique initial.
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 5 : MODE FICHIER UNIQUE
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_3_2 = f"""
        <div class="section" id="mode-fichier">
            <h2>📄 Mode Fichier Unique</h2>
            
            {generator._get_image_html("03_main_interface", "006", 
                "Mode Fichier unique", 
                "Interface en mode fichier unique avec un fichier chargé")}
            
            <h4>Comment ça marche ?</h4>
            <p>Ce mode est parfait pour travailler rapidement sur un <strong>seul fichier <code>.rpy</code></strong> sans charger tout un projet. Pratique pour des corrections rapides ou des tests !</p>
            
            <div>
                <h5>1. Sélection directe 📄</h5>
                <p>Cliquez sur le bouton <strong>"📄 Fichier"</strong> et choisissez directement un fichier <code>.rpy</code> n'importe où sur votre ordinateur. Les sélections de langue et de fichier sont automatiquement désactivées (grisées) car non applicables.</p>
            </div>
            
            <h5>2. 📊 Infos affichées</h5>
            <ul style="padding-left: 40px;">
                <li>• Le mode actif : <strong>"🔧 Mode : Fichier unique"</strong> (en violet/magenta)</li>
                <li>• Le chemin complet du fichier</li>
                <li>• La langue détectée (si le fichier est dans un dossier <code>/tl/[langue]/</code>)</li>
                <li>• Le nombre de lignes</li>
            </ul>
            
            <div class="warning-box">
                <strong>⚠️ Limitations</strong> : En mode fichier unique, certaines fonctionnalités automatiques du mode projet 
                ne sont pas disponibles (comme la navigation multi-fichiers).
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 6 : ONGLETS D'ACTIONS - VOS OUTILS DE TRAVAIL
    # ═══════════════════════════════════════════════════════════════════════════
    
    # --- 4.1 : ONGLET PRÉPARATION ---
    section_4_1 = f"""
        <div class="section" id="onglet-preparation">
            <h2>🔬 Onglet PRÉPARATION</h2>
            
            {generator._get_image_html("03_main_interface", "007", 
                "Focus sur l'onglet Préparation", 
                "Zone des boutons d'action de l'onglet Préparation avec le Générateur Ren'Py")}
            
            <p>Cet onglet donne accès au <strong>Générateur Ren'Py</strong>, l'outil principal pour gérer l'infrastructure complète de votre projet.</p>
            
            <h4>🎮 Générateur Ren'Py</h4>
            <p>Ouvre l'interface dédiée du Générateur Ren'Py qui vous permet de :</p>
            <ul style="padding-left: 40px;">
                <li>• Extraire les archives <code>.rpa</code> du jeu et décompiler les fichiers <code>.rpyc</code></li>
                <li>• Générer automatiquement l'arborescence de traduction</li>
                <li>• Chercher des textes oubliés lors de la génération</li>
                <li>• Combiner des fichiers en un seul (et le rediviser)</li>
            </ul>
            
            <p><strong>💡 Quand l'utiliser ?</strong> Au tout début d'un nouveau projet pour extraire les RPA et créer l'arborescence de traduction.</p>
        </div>
    """
    
    # --- 4.2 : ONGLET ACTIONS ---
    section_4_2 = f"""
        <div class="section" id="onglet-actions">
            <h2>⚡ Onglet ACTIONS</h2>
            
            {generator._get_image_html("03_main_interface", "008", 
                "Focus sur l'onglet Actions", 
                "Zone des boutons d'action de l'onglet Actions avec Extraire, Reconstruire et Revérifier")}
            
            <p>C'est l'onglet que vous utiliserez le plus ! Il contient les <strong>trois actions principales</strong> du workflow de traduction :</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div style="margin: 0;">
                    <h4>⚡ Extraire</h4>
                    <p>Extrait le texte traduisible depuis le fichier original. Cette opération :</p>
                    <ul style="padding-left: 40px;">
                        <li>• Identifie toutes les chaînes de texte</li>
                        <li>• Crée un fichier structuré avec les balises, variables, etc. protégées</li>
                        <li>• Prépare le fichier pour la traduction</li>
                    </ul>
                </div>
                
                <div style="margin: 0;">
                    <h4>🔄 Reconstruire</h4>
                    <p>Reconstruit le fichier Ren'Py à partir de vos traductions. Cette opération :</p>
                    <ul style="padding-left: 40px;">
                        <li>• Valide la syntaxe de vos traductions</li>
                        <li>• Réintègre le texte traduit dans la structure Ren'Py</li>
                        <li>• Crée le fichier final prêt à être testé</li>
                    </ul>
                </div>
                
                <div style="margin: 0; grid-column: span 2;">
                    <h4>📋 Revérifier</h4>
                    <p>Lance une vérification de cohérence sur votre fichier pour détecter les erreurs courantes :</p>
                    <ul style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.5rem; padding-left: 40px;">
                        <li>• Variables manquantes ou en trop</li>
                        <li>• Tags mal fermés</li>
                        <li>• Placeholders oubliés</li>
                        <li>• Chaînes non traduites</li>
                    </ul>
                </div>
            </div>
            
            <div class="tip-box">
                <strong>💡 Le workflow classique</strong> : <br>
                Extraire → Traduire (à l'extérieur de RenExtract) → Vérification automatique → Corriger → Revérifier
            </div>
        </div>
    """
    
    # --- 4.3 : ONGLET OUTILS ---
    section_4_3 = f"""
        <div class="section" id="onglet-outils">
            <h2>🧰 Onglet OUTILS</h2>
            
            {generator._get_image_html("03_main_interface", "009", 
                "Focus sur l'onglet Outils", 
                "Zone des boutons d'action de l'onglet Outils avec Rapport, Temporaires, Outils Spécialisé et Sauvegardes")}
            
            <p>Cet onglet regroupe les <strong>outils utilitaires</strong> pour gérer vos fichiers, rapports et sauvegardes :</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div style="margin: 0;">
                    <h4>⚠️ Rapport</h4>
                    <p>Accédez rapidement aux rapports générés par RenExtract (cohérence, nettoyage, etc.). 
                    Vous pouvez les consulter, les ouvrir dans votre navigateur ou les supprimer.</p>
                </div>
                
                <div style="margin: 0;">
                    <h4>📁 Temporaires</h4>
                    <p>Gérez les fichiers temporaires créés par l'application. Pratique pour faire du ménage et 
                    libérer de l'espace disque sans risque.</p>
                </div>
                
                <div style="margin: 0;">
                    <h4>🔧 Outils Spécialisé</h4>
                    <p>Accédez aux outils avancés pour améliorer vos fichiers de traductions.</p>
                </div>
                
                <div style="margin: 0;">
                    <h4>💾 Sauvegardes</h4>
                    <p>Consultez et restaurez les sauvegardes automatiques de vos fichiers. RenExtract crée une sauvegarde 
                    avant chaque opération importante pour que vous puissiez toujours revenir en arrière.</p>
                </div>
            </div>
            
            <div>
                <strong>💡 Conseil</strong> : Visitez régulièrement cet onglet pour consulter les rapports d'erreurs 
                et faire le ménage dans les fichiers temporaires.
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 5 : ZONE DE CONTENU - TON ESPACE DE TRAVAIL
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_5 = f"""
        <div class="section" id="zone-contenu">
            <h2>📝 Zone de Contenu - Votre Espace de Travail</h2>
            
            {generator._get_image_html("03_main_interface", "010", 
                "Zone de contenu vide", 
                "Zone de contenu affichant le message de collage Ctrl+V")}
            
            <p>La zone centrale est votre espace de travail principal. C'est ici que s'affiche le contenu de vos fichiers pour vous assurer que vous travaillez sur le bon fichier.</p>
            
            <h3>📋 Affichage du contenu</h3>
            <p>Quand vous sélectionnez un fichier (mode projet) ou que vous en chargez un (mode fichier unique), 
            son contenu s'affiche ici avec une scrollbar pour naviguer dans les fichiers longs.</p>
            
            <div class="warning-box">
                <strong>⚠️ Zone de visualisation uniquement</strong> : Le contenu affiché est en <strong>lecture seule</strong>. 
                Vous ne pouvez pas le modifier directement ici. Pour éditer vos fichiers, utilisez votre éditeur externe préféré 
                (Notepad++, VS Code, etc.).
            </div>
            
            <h3>⌨️ Collage Ctrl+V avec validation intelligente</h3>
            <p>La zone de contenu accepte le collage direct avec <strong>Ctrl+V</strong> <strong>uniquement pour les fichiers de traduction Ren'Py</strong> :</p>
            <ul>
                <li>Structure <code>translate [langue] strings:</code> (traductions de chaînes)</li>
                <li>Structure <code>translate [langue] ID:</code> (traductions de blocs)</li>
            </ul>
            
            <h3>🔍 Processus automatique</h3>
            <p>Quand vous collez du contenu, RenExtract :</p>
            <ul style="padding-left: 40px;">
                <li>• Vérifie que c'est bien une structure de traduction Ren'Py valide</li>
                <li>• Détecte s'il s'agit de code technique non traitable et vous l'indiquera</li>
                <li>• Si c'est valide → vous invite à créer une sauvegarde dans un nouveau fichier</li>
                <li>• Le fichier est ensuite chargé automatiquement dans l'interface</li>
            </ul>
            
            <h3>📝 Message d'accueil</h3>
            <p>Quand aucun fichier n'est chargé, vous verrez un message explicatif :</p>
            <div class="info-box" style="background: rgba(100, 150, 200, 0.1); border-left: 4px solid var(--accent-color); border-radius: 8px;">
                <pre style="margin: 0; font-family: 'Courier New', monospace;">Zone de collage Ctrl+V

Utilisez Ctrl+V pour coller du contenu directement dans cette zone.

Ouverture-Auto: ON

💡 Astuce : Pour les fichiers et dossiers, utilisez la zone intelligente en haut
   avec les boutons 📄 Fichier et 📁 Dossier, ou glissez-déposez
   n'importe où dans l'interface SAUF ici.

ℹ️ Cette zone est dédiée exclusivement au collage de texte.</pre>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 6 : CHAMP DE SORTIE - OÙ VONT VOS FICHIERS
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_6 = """
        <div class="section" id="champ-sortie">
            <h2>📁 Champ de Sortie - Où Vont Vos Fichiers</h2>
            
            <p><em>💡 Cette section est activable via les paramètres de l'application. Par défaut, elle peut être masquée.</em></p>
            
            <h3>📁 Informations de sortie</h3>
            <p>Juste au-dessus de la zone de contenu, une ligne discrète vous indique où RenExtract enregistre les fichiers traités :</p>
            
            <pre style="background: var(--card-bg); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
📁 Dossier de sortie : Lancez une extraction pour voir le dossier de sortie</pre>
            
            <h3>Que voir ici ?</h3>
            <ul style="padding-left: 40px;">
                <li>• <strong>Avant toute opération</strong> : un message explicatif</li>
                <li>• <strong>Après une extraction</strong> : le chemin complet du <strong>dossier</strong> où sont sauvegardés vos fichiers</li>
            </ul>
            
            <p><strong>Exemple</strong> : <code>D:\\02 - Jeux VN\\RenExtract_app\\01_Temporaires\\&lt;Game_Name&gt;\\&lt;File_name&gt;\\fichiers_a_traduire</code></p>
            
            <h3>💡 Copie et accès rapide</h3>
            <p>Le champ n'est pas cliquable directement, mais vous pouvez :</p>
            <ul style="padding-left: 40px;">
                <li>• <strong>Cliquer + Ctrl+C</strong> : Copie automatiquement le chemin</li>
                <li>• <strong>Clic droit</strong> : Accès aux options (Copier le chemin, Ouvrir le dossier, Sélectionner tout)</li>
            </ul>
        
            <div class="warning-box">
                <strong>⚠️ Attention</strong> : Le chemin s'actualise à chaque opération. Si vous changez de projet, le dossier de sortie change aussi !
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ASSEMBLAGE FINAL DU CONTENU
    # ═══════════════════════════════════════════════════════════════════════════
    
    return (
        navigation +
        section_1 +
        section_2 +
        section_3_0 +
        section_3_1 +
        section_3_2 +
        section_4_1 +
        section_4_2 +
        section_4_3 +
        section_5 +
        section_6
    )
