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
                <a href="#mode-projet" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">📂 Mode Projet</div>
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
                    <div style="font-size: 0.9em; opacity: 0.8;">Où vont tes fichiers</div>
                </a>
                <a href="#astuces" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🎯 Raccourcis</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Raccourcis clavier et actions</div>
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
            
            {generator._get_image_html("03_interface_principale", "001", 
                "Vue d'ensemble de l'interface", 
                "Capture d'écran complète de l'interface principale de RenExtract")}
            
            <p>Cette interface principale est ton espace de travail pour <strong>préparer tes fichiers de scripts Ren'Py en vue de la traduction</strong>. 
            Elle est conçue pour être intuitive et te guider à chaque étape : extraction, reconstruction, et vérification.</p>
            
            <div class="warning-box">
                <strong>⚠️ Important</strong> : RenExtract <strong>ne traduit pas</strong> les textes ! Il prépare et structure les fichiers pour que tu puisses 
                les traduire dans ton éditeur ou outil de traduction préféré (Excel, Notepad++, outils CAT, etc.).
        </div>
            
            <p>L'interface se compose de plusieurs zones clés :</p>
            <ul>
                <li>Le <strong>header en haut</strong> avec les boutons d'accès rapide</li>
                <li>La <strong>zone de sélection</strong> pour choisir ton projet ou fichier</li>
                <li>Les <strong>onglets d'actions</strong> pour lancer les différentes opérations</li>
                <li>La <strong>zone de contenu centrale</strong> pour visualiser le code</li>
            </ul>
            
            <p>Que tu travailles sur un <strong>projet complet</strong> avec plusieurs langues ou sur un <strong>seul fichier</strong>, 
            RenExtract s'adapte à tes besoins ! 💪</p>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 2 : LE HEADER - CONTRÔLES PRINCIPAUX
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_2 = """
        <div class="section" id="header">
            <h2>📋 Le Header - Contrôles Principaux</h2>
            
            <p>En haut de l'interface, tu trouveras le header avec le titre de l'application et quatre boutons essentiels :</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="info-box" style="margin: 0;">
                    <h3>🎮 RenExtract [version]</h3>
                    <p>Le titre affiche la version actuelle de l'application. Toujours utile pour vérifier que tu es à jour !</p>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h3>📖 Guide Complet</h3>
                    <p>Ce bouton ouvre justement ce guide dans ton navigateur. Tu peux le consulter à tout moment pour te rafraîchir la mémoire sur une fonctionnalité.</p>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h3>⚙️ Paramètres</h3>
                    <p>Ce bouton te donne accès aux réglages de l'application : choix de l'éditeur, personnalisation du thème des boutons, 
                    comportements par défaut, etc. C'est ici que tu personnalises RenExtract selon tes préférences.</p>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h3>❌ Quitter</h3>
                    <p>Ce bouton te permet de fermer proprement l'application. RenExtract sauvegarde automatiquement ton dernier projet ouvert 
                    pour que tu puisses reprendre là où tu t'es arrêté.</p>
                </div>
            </div>
            
            <div class="tip-box">
                <strong>💡 Astuce</strong> : Prends le temps de configurer l'application via les Paramètres dès le début. 
                Un bon réglage initial te fera gagner beaucoup de temps par la suite !
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 3 : MODE PROJET COMPLET
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_3_1 = f"""
        <div class="section" id="mode-projet">
            <h2>📂 Mode Projet Complet</h2>
            
            {generator._get_image_html("03_interface_principale", "002", 
                "Mode Projet avec fichier sélectionné", 
                "Interface en mode projet avec un fichier chargé")}
            
            <h4>Quand l'utiliser ?</h4>
            <p>Ce mode est idéal quand tu veux gérer un <strong>projet Ren'Py complet</strong> avec potentiellement 
            plusieurs langues et de nombreux fichiers.</p>
            
            <h4>Comment ça marche ?</h4>
            
            <div class="step-box">
                <h5>1. Sélection du projet 📁</h5>
                <p>Clique sur <strong>"📁 Projet"</strong> pour choisir le dossier racine de ton jeu Ren'Py.</p>
                <p><strong>💡 Astuce</strong> : Pas besoin de chercher précisément le dossier racine ! Si tu sélectionnes un sous-dossier (par exemple <code>/game/</code> ou <code>/game/tl/french/</code>), RenExtract remontera intelligemment jusqu'à la racine du projet.</p>
                <p><strong>Scan automatique</strong> : Une fois le projet détecté, RenExtract va automatiquement scanner et détecter les langues disponibles (dossiers dans <code>/game/tl/</code>), les fichiers de traduction (<code>.rpy</code>) et la structure du projet.</p>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="step-box" style="margin: 0;">
                    <h5>2. Choix de la langue 🌍</h5>
                    <p>Une fois le projet scanné, sélectionne la langue sur laquelle tu veux travailler dans le menu déroulant <strong>"🌍 Langue"</strong>. Tu verras le nombre de fichiers disponibles pour cette langue.</p>
                </div>
                
                <div class="step-box" style="margin: 0;">
                    <h5>3. Sélection du fichier 📄</h5>
                    <p>Dans le menu <strong>"📄 Fichier"</strong>, choisis le fichier spécifique que tu veux traiter. Tu peux voir le nombre de lignes et ta position dans la liste.</p>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="info-box" style="margin: 0;">
                    <h4>📊 4. Infos affichées</h4>
                    <ul>
                        <li>Le mode actif : <strong>"🔧 Mode : Projet complet"</strong></li>
                        <li>Les détails du projet : nombre de fichiers RPY, langues disponibles</li>
                        <li>Les statistiques : nombre de lignes, position dans la liste (ex: "1/108 fichiers")</li>
                    </ul>
                </div>
                
                <div class="step-box" style="margin: 0;">
                    <h5>5. Navigation rapide ⏩</h5>
                    <p>Quand il y a plusieurs fichiers, deux boutons de navigation apparaissent :</p>
                    <ul>
                        <li><strong>"◀️ Fichier Précédent"</strong> : retourne au fichier précédent</li>
                        <li><strong>"▶️ Fichier Suivant"</strong> : passe au fichier suivant</li>
                    </ul>
                    <p>Ces boutons te permettent de naviguer rapidement sans repasser par les menus déroulants.</p>
                </div>
            </div>
            
            <div class="tip-box">
                <strong>💡 Bon à savoir</strong> : Tu peux scanner à nouveau ton projet avec le bouton <strong>"🔄 Scanner"</strong> 
                si tu as ajouté des fichiers ou langues manuellement.
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 4 : MODE FICHIER UNIQUE
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_3_2 = f"""
        <div class="section" id="mode-fichier">
            <h2>📄 Mode Fichier Unique</h2>
            
            {generator._get_image_html("03_interface_principale", "003", 
                "Mode Fichier unique", 
                "Interface en mode fichier unique")}
            
            <h4>Quand l'utiliser ?</h4>
            <p>Ce mode est parfait pour travailler rapidement sur un <strong>seul fichier <code>.rpy</code></strong> sans charger tout un projet. 
            Pratique pour des corrections rapides ou des tests !</p>
            
            <h4>Comment ça marche ?</h4>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="step-box" style="margin: 0;">
                    <h5>1. Sélection directe 📄</h5>
                    <p>Clique sur le bouton <strong>"📄 Fichier"</strong> et choisis directement un fichier <code>.rpy</code> 
                    n'importe où sur ton ordinateur.</p>
                </div>
                
                <div class="step-box" style="margin: 0;">
                    <h5>2. Chargement automatique ⚡</h5>
                    <p>RenExtract charge immédiatement le fichier et l'affiche dans la zone de contenu. 
                    Les sélections de langue et de fichier sont automatiquement désactivées (grisées) car non applicables.</p>
                </div>
            </div>
            
            <div class="info-box">
                <h4>📊 Infos affichées</h4>
                <ul>
                    <li>Le mode actif : <strong>"🔧 Mode : Fichier unique"</strong> (en violet/magenta)</li>
                    <li>Le chemin complet du fichier</li>
                    <li>La langue détectée (si le fichier est dans un dossier <code>/tl/[langue]/</code>)</li>
                    <li>Le nombre de lignes</li>
                </ul>
            </div>
            
            <div class="warning-box">
                <strong>⚠️ Limitations</strong> : En mode fichier unique, certaines fonctionnalités automatiques du mode projet 
                ne sont pas disponibles (comme la navigation multi-fichiers).
            </div>
            
            <div class="tip-box">
                <strong>💡 Astuce</strong> : Ce mode est idéal pour tester rapidement un fichier de rapport de cohérence 
                ou pour faire une correction urgente sur un seul fichier.
            </div>
        </div>
    """
    
    # --- 3.3 : BOUTON SCANNER ---
    section_3_3 = """
        <div class="section">
            <h2>🔄 Bouton Scanner</h2>
            
            <p>Le bouton <strong>"🔄 Scanner"</strong> te permet de forcer une nouvelle analyse du projet. Utilise-le dans ces cas :</p>
            <ul>
                <li>Tu as ajouté manuellement un dossier de langue</li>
                <li>Tu as modifié la structure du projet</li>
                <li>Les fichiers ne s'affichent pas correctement</li>
            </ul>
            
            <p>Le scanner va <strong>ignorer le cache</strong> et tout réanalyser à zéro. C'est comme un "rafraîchir" pour ton projet !</p>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 4 : ONGLETS D'ACTIONS - TES OUTILS DE TRAVAIL
    # ═══════════════════════════════════════════════════════════════════════════
    
    # --- 4.1 : ONGLET PRÉPARATION ---
    section_4_1 = f"""
        <div class="section" id="onglet-preparation">
            <h2>🔬 Onglet PRÉPARATION</h2>
            
            {generator._get_image_html("03_interface_principale", "004-1", 
                "Onglet Préparation", 
                "Onglet Préparation avec le bouton Générateur Ren'Py")}
            
            <p>Cet onglet donne accès au <strong>Générateur Ren'Py</strong>, l'outil principal pour gérer l'infrastructure complète de ton projet :</p>
            
            <div class="info-box">
                <h4>🎮 Générateur Ren'Py</h4>
                <p>Ouvre l'interface dédiée du Générateur Ren'Py qui te permet de :</p>
                <ul>
                    <li>Extraire les archives <code>.rpa</code> du jeu</li>
                    <li>Générer automatiquement l'arborescence de traduction</li>
                    <li>Gérer la structure des fichiers du projet</li>
                    <li>Configurer les paramètres avancés du projet</li>
                </ul>
                
                <p>Le Générateur est <strong>complémentaire</strong> à l'Interface Principale :</p>
                <ul>
                    <li><strong>Interface Principale</strong> → Pour travailler fichier par fichier (Extraire, Traduire, Reconstruire)</li>
                    <li><strong>Générateur Ren'Py</strong> → Pour gérer la structure globale du projet (Setup, RPA, Arborescence)</li>
                </ul>
            </div>
            
            <div class="tip-box">
                <strong>💡 Quand utiliser le Générateur ?</strong>
                <ul>
                    <li>Au tout début d'un nouveau projet pour extraire les RPA et créer l'arborescence de traduction</li>
                    <li>Pour ajouter ou gérer plusieurs langues en parallèle</li>
                    <li>Pour des opérations en masse sur l'ensemble du projet</li>
                </ul>
            </div>
        </div>
    """
    
    # --- 4.2 : ONGLET ACTIONS ---
    section_4_2 = f"""
        <div class="section" id="onglet-actions">
            <h2>⚡ Onglet ACTIONS</h2>
            
            {generator._get_image_html("03_interface_principale", "004-2", 
                "Onglet Actions", 
                "Onglet Actions avec les trois boutons principaux")}
            
            <p>C'est l'onglet que tu utiliseras le plus ! Il contient les <strong>trois actions principales</strong> du workflow de traduction :</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="info-box" style="margin: 0;">
                    <h4>⚡ Extraire</h4>
                    <p>Extrait le texte traduisible depuis le fichier original. Cette opération :</p>
                    <ul>
                        <li>Identifie toutes les chaînes de texte</li>
                        <li>Crée un fichier structuré avec les balises, variables, etc. protégées</li>
                        <li>Prépare le fichier pour la traduction</li>
                    </ul>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>🔄 Reconstruire</h4>
                    <p>Reconstruit le fichier Ren'Py à partir de tes traductions. Cette opération :</p>
                    <ul>
                        <li>Valide la syntaxe de tes traductions</li>
                        <li>Réintègre le texte traduit dans la structure Ren'Py</li>
                        <li>Crée le fichier final prêt à être testé</li>
                    </ul>
                </div>
                
                <div class="info-box" style="margin: 0; grid-column: span 2;">
                    <h4>📋 Revérifier</h4>
                    <p>Lance une vérification de cohérence sur ton fichier pour détecter les erreurs courantes :</p>
                    <ul style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.5rem;">
                        <li>Variables manquantes ou en trop</li>
                        <li>Tags mal fermés</li>
                        <li>Placeholders oubliés</li>
                        <li>Chaînes non traduites</li>
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
            
            {generator._get_image_html("03_interface_principale", "004-3", 
                "Onglet Outils", 
                "Onglet Outils avec les quatre boutons utilitaires")}
            
            <p>Cet onglet regroupe les <strong>outils utilitaires</strong> pour gérer tes fichiers, rapports et sauvegardes :</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="info-box" style="margin: 0;">
                    <h4>⚠️ Rapport</h4>
                    <p>Accède rapidement aux rapports générés par RenExtract (cohérence, nettoyage, etc.). 
                    Tu peux les consulter, les ouvrir dans ton navigateur ou les supprimer.</p>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>📁 Temporaires</h4>
                    <p>Gère les fichiers temporaires créés par l'application. Pratique pour faire du ménage et 
                    libérer de l'espace disque sans risque.</p>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>🔧 Outils Spécialisé</h4>
                    <p>Accès aux outils avancés pour gérer les aspects techniques de tes fichiers de traduction.</p>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>💾 Sauvegardes</h4>
                    <p>Consulte et restaure les sauvegardes automatiques de tes fichiers. RenExtract crée une sauvegarde 
                    avant chaque opération importante pour que tu puisses toujours revenir en arrière.</p>
                </div>
            </div>
            
            <div class="tip-box">
                <strong>💡 Conseil</strong> : Visite régulièrement cet onglet pour consulter les rapports d'erreurs 
                et faire le ménage dans les fichiers temporaires.
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 5 : ZONE DE CONTENU - TON ESPACE DE TRAVAIL
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_5 = f"""
        <div class="section" id="zone-contenu">
            <h2>📝 Zone de Contenu - Ton Espace de Travail</h2>
            
            {generator._get_image_html("03_interface_principale", "005", 
                "Zone de contenu avec code", 
                "Zone de contenu affichant du code Ren'Py")}
            
            <p>La zone centrale est ton espace de travail principal. C'est ici que tu visualises et manipules le contenu de tes fichiers.</p>
            
            <h3>📋 Affichage du contenu</h3>
            <p>Quand tu sélectionnes un fichier (mode projet) ou que tu en charges un (mode fichier unique), 
            son contenu s'affiche ici avec une scrollbar pour naviguer dans les fichiers longs.</p>
            
            <div class="warning-box">
                <strong>⚠️ Zone de visualisation uniquement</strong> : Le contenu affiché est en <strong>lecture seule</strong>. 
                Tu ne peux pas le modifier directement ici. Pour éditer tes fichiers, utilise ton éditeur externe préféré 
                (Notepad++, VS Code, etc.).
            </div>
            
            <h3>⌨️ Collage Ctrl+V avec validation intelligente</h3>
            <p>La zone de contenu accepte le collage direct avec <strong>Ctrl+V</strong> <strong>uniquement pour les fichiers de traduction Ren'Py</strong> :</p>
            <ul>
                <li>Structure <code>translate [langue] strings:</code> (traductions de chaînes)</li>
                <li>Structure <code>translate [langue] ID:</code> (traductions de blocs)</li>
            </ul>
            
            <div class="info-box">
                <h4>🔍 Processus automatique :</h4>
                <p>Quand tu colles du contenu, RenExtract :</p>
                <ul>
                    <li>Vérifie que c'est bien une structure de traduction Ren'Py valide</li>
                    <li>Détecte s'il s'agit de code technique non traitable et te l'indiquera</li>
                    <li>Si c'est valide → crée automatiquement une sauvegarde dans un nouveau fichier</li>
                    <li>Le fichier est ensuite chargé automatiquement dans l'interface</li>
                </ul>
            </div>
            
            <h3>📝 Message d'accueil</h3>
            <p>Quand aucun fichier n'est chargé, tu verras un message explicatif :</p>
            <pre style="background: var(--card-bg); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
Zone de collage Ctrl+V

Utilisez Ctrl+V pour coller du contenu directement dans cette zone.

Ouverture-Auto: ON

💡 Astuce : Pour les fichiers et dossiers, utilisez la zone intelligente en haut
   avec les boutons 📄 Fichier et 📁 Dossier, ou glissez-déposez
   n'importe où dans l'interface SAUF ici.

ℹ️ Cette zone est dédiée exclusivement au collage de texte.</pre>
            
            <div class="tip-box">
                <strong>💡 Astuce d'organisation</strong> : L'ouverture automatique (Ouverture-Auto: ON) charge immédiatement 
                le fichier sélectionné. Tu peux la désactiver dans les paramètres si tu préfères charger manuellement.
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 6 : CHAMP DE SORTIE - OÙ VONT TES FICHIERS
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_6 = f"""
        <div class="section" id="champ-sortie">
            <h2>📁 Champ de Sortie - Où Vont Tes Fichiers</h2>
            
            {generator._get_image_html("03_interface_principale", "006", 
                "Champ de sortie", 
                "Champ affichant le dossier de sortie")}
            
            <h3>📁 Informations de sortie</h3>
            <p>Juste au-dessus de la zone de contenu, une ligne discrète t'indique où RenExtract enregistre les fichiers traités :</p>
            
            <pre style="background: var(--card-bg); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
📁 Dossier de sortie : Lancez une extraction pour voir le dossier de sortie</pre>
            
            <h3>Que voir ici ?</h3>
            <ul>
                <li><strong>Avant toute opération</strong> : un message explicatif</li>
                <li><strong>Après une extraction</strong> : le chemin complet du <strong>dossier</strong> où sont sauvegardés tes fichiers</li>
            </ul>
            
            <p><strong>Exemple</strong> : <code>D:\\02 - Jeux VN\\RenExtract_app\\01_Temporaires\\&lt;Game_Name&gt;\\&lt;File_name&gt;\\fichiers_a_traduire</code></p>
            
            <div class="info-box">
                <h4>💡 Copie et accès rapide</h4>
                <p>Le champ n'est pas cliquable directement, mais tu peux :</p>
                <ul>
                    <li><strong>Cliquer + Ctrl+C</strong> : Copie automatiquement le chemin</li>
                    <li><strong>Clic droit</strong> : Accès aux options (Copier le chemin, Ouvrir le dossier, Sélectionner tout)</li>
            </ul>
        </div>
        
            <div class="warning-box">
                <strong>⚠️ Attention</strong> : Le chemin s'actualise à chaque opération. Si tu changes de projet, le dossier de sortie change aussi !
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 7 : RACCOURCIS UTILES (simplifié - bonnes pratiques dans Workflow)
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_7 = """
        <div class="section" id="astuces">
            <h2>🎯 Raccourcis Utiles</h2>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="info-box" style="margin: 0;">
                    <h4>⌨️ Collage et Navigation</h4>
                    <ul>
                        <li><strong>Ctrl+V</strong> : Coller du contenu Ren'Py</li>
                        <li><strong>Drag & Drop</strong> : Glisser projet/fichier</li>
                    </ul>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>📋 Copie et Accès</h4>
                    <ul>
                        <li><strong>Clic + Ctrl+C</strong> : Copier chemin de sortie</li>
                        <li><strong>Clic droit</strong> : Menu contextuel (copier, ouvrir)</li>
            </ul>
                </div>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 8 : POUR ALLER PLUS LOIN (Conclusion simplifiée) - SUPPRIMÉE
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_8 = ""
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ASSEMBLAGE FINAL DU CONTENU
    # ═══════════════════════════════════════════════════════════════════════════
    
    return (
        navigation +
        section_1 +
        section_2 +
        section_3_1 +
        section_3_2 +
        section_3_3 +
        section_4_1 +
        section_4_2 +
        section_4_3 +
        section_5 +
        section_6 +
        section_7 +
        section_8
    )
