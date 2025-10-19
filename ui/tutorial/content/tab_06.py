# ui/tutorial/content/tab_06.py
"""
Module de contenu pour l'onglet 6 : Sauvegardes
Gestionnaire de sauvegardes - Restauration et organisation
"""

def generate_content(generator, language=None, translations=None):
    """Génère le contenu de l'onglet Sauvegardes (français uniquement)
    
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
                
                <a href="#vue-ensemble-sauvegardes" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">💾 Vue d'ensemble</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Qu'est-ce que c'est ?</div>
                </a>
                
                <a href="#acces" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🔓 Accès</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Ouvrir le gestionnaire</div>
                </a>
                
                <a href="#types-sauvegardes" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">📊 Types</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Les 5 types de sauvegardes</div>
                </a>
                
                <a href="#structure" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">📂 Structure</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Organisation des fichiers</div>
                </a>
                
                <a href="#statistiques" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">📈 Statistiques</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Aperçu en temps réel</div>
                </a>
                
                <a href="#filtres" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🔍 Filtres</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Trouver rapidement</div>
                </a>
                
                <a href="#treeview" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🌳 Tree View</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Vue hiérarchique</div>
                </a>
                
                <a href="#actions" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🎯 Actions</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Restaurer, supprimer</div>
                </a>
                
                <a href="#avancees" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">⚙️ Avancé</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Fonctionnalités techniques</div>
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
    # SECTION 1 : VUE D'ENSEMBLE
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_1 = f"""
        <div class="section" id="vue-ensemble-sauvegardes">
            <h2>💾 Vue d'Ensemble du Gestionnaire de Sauvegardes</h2>
            
            {generator._get_image_html("06_backup", "002", 
                "Vue d'ensemble du gestionnaire de sauvegardes", 
                "Interface complète du gestionnaire avec statistiques, filtres et liste des sauvegardes")}
            
            <h3>Qu'est-ce que c'est ?</h3>
            <p>Le <strong>Gestionnaire de Sauvegardes</strong> est votre centre de contrôle pour toutes les sauvegardes automatiques créées par RenExtract. 
            Chaque fois que vous lancez une opération importante, RenExtract crée automatiquement une sauvegarde de vos fichiers.</p>
            
            <p>Cette interface vous permet de :</p>
            <ul>
                <li>📊 <strong>Visualiser</strong> toutes vos sauvegardes en un coup d'œil</li>
                <li>🔍 <strong>Filtrer</strong> par jeu ou par type de sauvegarde</li>
                <li>💾 <strong>Restaurer</strong> un fichier en cas de problème</li>
                <li>🗑️ <strong>Supprimer</strong> les anciennes sauvegardes pour libérer de l'espace</li>
                <li>📈 <strong>Suivre</strong> l'espace disque utilisé</li>
            </ul>
            
            <div class="info-box">
                <h4>🛡️ Sécurité avant tout</h4>
                <p>RenExtract ne supprime <strong>jamais</strong> une sauvegarde sans votre confirmation explicite. 
                La seule exception : lors d'une restauration normale, le fichier sauvegardé est automatiquement supprimé pour éviter les doublons, mais cette action est clairement expliquée avant confirmation.</p>
            </div>
            
            <h3>Quand l'utiliser ?</h3>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="tip-box" style="margin: 0;">
                    <h4>✅ Situations courantes</h4>
                    <ul>
                        <li>Vous avez fait une erreur lors du nettoyage</li>
                        <li>Un fichier a été modifié par erreur</li>
                        <li>Vous voulez récupérer une ancienne version</li>
                        <li>Vous voulez libérer de l'espace disque</li>
                    </ul>
                </div>
                
                <div class="warning-box" style="margin: 0;">
                    <h4>⚠️ Important à savoir</h4>
                    <ul>
                        <li>Les sauvegardes prennent de l'espace disque</li>
                        <li>Pensez à nettoyer régulièrement</li>
                        <li>La suppression est <strong>irréversible</strong></li>
                        <li>Vérifiez avant de supprimer !</li>
                    </ul>
                </div>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 2 : ACCÈS AU GESTIONNAIRE
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_2 = f"""
        <div class="section" id="acces">
            <h2>🔓 Accès au Gestionnaire</h2>
            
            {generator._get_image_html("06_backup", "001", 
                "Bouton Sauvegardes dans l'onglet OUTILS", 
                "Accès au gestionnaire de sauvegardes depuis l'onglet OUTILS")}
            
            <h3>Comment ouvrir le gestionnaire ?</h3>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                
                <div class="step-box" style="margin: 0;">
                    <h4>📍 Étape par étape</h4>
                    <ol>
                        <li><strong>Cliquez sur l'onglet OUTILS</strong> (jaune) dans l'interface principale</li>
                        <li><strong>Cliquez sur le bouton "💾 Sauvegardes"</strong></li>
                        <li>Le gestionnaire s'ouvre dans une nouvelle fenêtre</li>
                    </ol>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>💡 Bon à savoir</h4>
                    <p>Le gestionnaire de sauvegardes est une <strong>fenêtre persistante</strong> : quand vous la fermez, elle se cache simplement.</p>
                    <p>La prochaine fois que vous l'ouvrez, elle <strong>réapparaît instantanément</strong> et charge automatiquement les dernières sauvegardes, 
                    y compris celles créées entre temps !</p>
                </div>
                
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 3 : TYPES DE SAUVEGARDES
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_3 = f"""
        <div class="section" id="types-sauvegardes">
            <h2>📊 Comprendre les Types de Sauvegardes</h2>
            
            <p>RenExtract crée automatiquement <strong>5 types de sauvegardes</strong> différents selon le contexte. Chaque type a son rôle spécifique :</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                
                <div class="info-box" style="margin: 0;">
                    <h4>🛡️ Sécurité</h4>
                    <p><strong>Quand ?</strong> Avant chaque extraction de fichiers</p>
                    <p><strong>Pourquoi ?</strong> Protection maximale de vos fichiers originaux</p>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>🧹 Nettoyage</h4>
                    <p><strong>Quand ?</strong> Avant chaque opération de nettoyage</p>
                    <p><strong>Pourquoi ?</strong> Protection contre la perte de données lors du nettoyage</p>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>📦 Avant RPA</h4>
                    <p><strong>Quand ?</strong> Avant chaque construction d'archive RPA</p>
                    <p><strong>Pourquoi ?</strong> Protection contre la corruption potentielle des données lors de la construction RPA</p>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>🔗 Avant combinaison</h4>
                    <p><strong>Quand ?</strong> Avant chaque opération de combinaison</p>
                    <p><strong>Pourquoi ?</strong> Protection contre la perte de données lors de la fusion</p>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>⚡ Édition temps réel</h4>
                    <p><strong>Quand ?</strong> Avant chaque modification dans l'éditeur</p>
                    <p><strong>Pourquoi ?</strong> Historique de modifications automatique</p>
                    <p><strong>Rotation :</strong> ✅ <strong>Max 10 fichiers</strong> (les plus anciens sont supprimés automatiquement)</p>
                </div>
                
            </div>
            
            <div class="info-box">
                <h4>📁 Types de sauvegarde : Fichier vs Dossier</h4>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 15px;">
                    <div>
                        <p><strong>Sauvegardes par fichier :</strong></p>
                        <ul>
                            <li><strong>🛡️ Sécurité</strong> : Sauvegarde individuelle de chaque fichier</li>
                            <li><strong>⚡ Édition temps réel</strong> : Sauvegarde individuelle à chaque modification</li>
                        </ul>
                    </div>
                    <div>
                        <p><strong>Sauvegardes par dossier complet :</strong></p>
                        <ul>
                            <li><strong>🧹 Nettoyage</strong> : Archive ZIP complète du dossier avant nettoyage</li>
                            <li><strong>📦 Avant RPA</strong> : Archive ZIP complète du dossier avant construction</li>
                            <li><strong>🔗 Avant combinaison</strong> : Archive ZIP complète du dossier avant fusion</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 4 : STRUCTURE DE STOCKAGE
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_4 = f"""
        <div class="section" id="structure">
            <h2>📂 Structure de Stockage</h2>
            
            <h3>Organisation hiérarchique</h3>
            <p>RenExtract organise vos sauvegardes de manière <strong>intelligente et structurée</strong> (arborescence collapsible) :</p>
            
            <div style="margin: 1.5rem 0; background: var(--nav-bg); border-radius: 8px; border-left: 4px solid var(--accent);">
                <div class="arbo-toggle" style="padding: 18px 24px; cursor: pointer; user-select: none; display: flex; align-items: center; gap: 12px; transition: all 0.2s; border-bottom: 1px solid var(--sep);" onclick="window.toggleArborescence()" id="arborescence-title">
                    <span id="arborescence-toggle" style="font-size: 1.3rem; color: var(--accent); font-weight: bold; transition: all 0.3s;">▶</span>
                    <span style="font-weight: 600; color: var(--fg);">📁 Cliquez pour voir l'arborescence des sauvegardes</span>
                </div>
                <style>
                .arbo-toggle:hover {{ background: rgba(74, 144, 226, 0.1); padding-left: 30px !important; }}
                </style>
                <div id="arborescence-content" style="display: none; margin-top: 15px;">
                    <pre style="background: var(--bg); padding: 15px; border-radius: 6px; overflow-x: auto; font-family: 'Consolas', 'Monaco', monospace; font-size: 0.9em;">
02_Sauvegardes/                            ← Dossier racine
├── backup_metadata.json                   ← Métadonnées globales
├── backup_cache.pkl                       ← Cache pour performances
├── &lt;Game_Name&gt;/                           ← Nom du jeu
│   ├── &lt;File_Name&gt;/                       ← Nom du fichier (sans extension)
│   │   ├── security/                      ← Sauvegardes de sécurité (fichiers individuels)
│   │   │   └── script_20251015_143124.rpy
│   │   └── realtime_edit/                 ← Sauvegardes édition (max 10 fichiers)
│   │       ├── script_20251015_144235.rpy
│   │       └── ... (max 10 fichiers)
│   ├── &lt;Langue_Name&gt;/                     ← Nom de la langue (pour archives ZIP)
│   │   ├── before_combination/            ← Sauvegardes avant combinaison (ZIP)
│   │   │   └── french_20251015_143111.zip
│   │   └── rpa_build/                     ← Sauvegardes avant RPA (ZIP)
│   │       └── french_20251015_143816.zip
│   └── tl/                                ← Dossier de traductions
│       └── cleanup/                       ← Sauvegardes de nettoyage (ZIP)
│           └── tl_20251015_143155.zip
                    </pre>
                </div>
                </div>
                
            <h3>Avantages de cette structure</h3>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="tip-box" style="margin: 0;">
                    <h4>✅ Organisation claire</h4>
                    <ul>
                        <li>Un dossier par jeu</li>
                        <li>Séparation par contexte : fichiers individuels vs archives ZIP</li>
                        <li>Fichiers individuels : security/ et realtime_edit/</li>
                        <li>Archives ZIP : before_combination/, rpa_build/, cleanup/</li>
                        <li>Facile à retrouver manuellement</li>
                    </ul>
                </div>
                
                <div class="tip-box" style="margin: 0;">
                    <h4>🚀 Performance optimisée</h4>
                    <ul>
                        <li>Cache intelligent (TTL: 60s)</li>
                        <li>Chargement ultra-rapide</li>
                        <li>Index des métadonnées</li>
                        <li>Scan hiérarchique efficace</li>
                    </ul>
                </div>
            </div>
            
            <div class="info-box">
                <h4>📍 Où se trouve ce dossier ?</h4>
                <p>Le dossier <code>02_Sauvegardes</code> est situé à la racine de votre dossier de travail RenExtract. 
                Vous pouvez y accéder par le bouton <strong>"Ouvrir le Dossier"</strong> depuis l'interface du gestionnaire !</p>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 5 : STATISTIQUES DES SAUVEGARDES
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_5 = f"""
        <div class="section" id="statistiques">
            <h2>📊 Statistiques des Sauvegardes</h2>
            
            <p>Le gestionnaire affiche des <strong>statistiques en temps réel</strong> pour vous donner un aperçu complet de vos sauvegardes :</p>
            
            {generator._get_image_html("06_backup", "003", 
                "Statistiques des sauvegardes", 
                "Zone de statistiques montrant le nombre total de sauvegardes, jeux et fichiers")}
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="info-box" style="margin: 0;">
                    <h4>📊 Informations affichées</h4>
                    <p>Les statistiques vous donnent un aperçu rapide de vos sauvegardes :</p>
                    <ul>
                        <li><strong>Nombre total de sauvegardes</strong> : Toutes les sauvegardes confondues</li>
                        <li><strong>Nombre de jeux</strong> : Jeux différents ayant des sauvegardes</li>
                        <li><strong>Nombre de fichiers</strong> : Fichiers différents sauvegardés</li>
                        <li><strong>Taille totale</strong> : Espace disque utilisé par toutes les sauvegardes</li>
                    </ul>
                    <p>Ces statistiques se mettent à jour automatiquement selon les filtres actifs !</p>
                </div>
                
                <div class="tip-box" style="margin: 0;">
                    <h4>💡 Utilisation pratique</h4>
                    <p>Les statistiques sont particulièrement utiles pour :</p>
                    <ul>
                        <li><strong>Surveiller l'espace disque</strong> utilisé par les sauvegardes</li>
                        <li><strong>Identifier les jeux</strong> avec le plus de sauvegardes</li>
                        <li><strong>Décider quelles sauvegardes</strong> supprimer pour libérer de l'espace</li>
                        <li><strong>Vérifier l'impact</strong> des filtres sur les données affichées</li>
                    </ul>
                </div>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 6 : FILTRER LES SAUVEGARDES
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_6 = f"""
        <div class="section" id="filtres">
            <h2>🔍 Filtrer les Sauvegardes</h2>
            
            <p>Quand vous avez beaucoup de sauvegardes, les <strong>filtres</strong> sont vos meilleurs amis ! 
            RenExtract vous propose deux filtres complémentaires :</p>
            
            <h3>Filtres et actions</h3>
            
            {generator._get_image_html("06_backup", "004", 
                "Filtres et actions", 
                "Zone des filtres et boutons d'action du gestionnaire")}
            
            <div class="info-box">
                <h4>🔍 Filtres disponibles</h4>
                <p>Le gestionnaire propose deux types de filtres :</p>
                <ul>
                    <li><strong>🎮 Filtre par jeu</strong> : Affiche les sauvegardes d'un jeu spécifique</li>
                    <li><strong>🏷️ Filtre par type</strong> : Affiche un type de sauvegarde spécifique</li>
                </ul>
                <p>Vous pouvez combiner les deux filtres pour affiner votre recherche !</p>
            </div>
            
            <h3>Filtre par jeu</h3>
            
            {generator._get_image_html("06_backup", "005", 
                "Filtre par jeu", 
                "Menu déroulant pour filtrer les sauvegardes par jeu")}
            
            <div class="info-box">
                <h4>🎮 Comment ça marche ?</h4>
                <p>Cliquez sur le menu déroulant <strong>"🎮 Filtrer par jeu"</strong> et choisissez :</p>
                <ul>
                    <li><strong>Tous</strong> : Affiche toutes les sauvegardes (tous jeux confondus)</li>
                    <li><strong>Un jeu spécifique</strong> : Affiche uniquement les sauvegardes de ce jeu</li>
                </ul>
                <p>Le tableau et les statistiques s'adaptent automatiquement !</p>
            </div>
            
            <h3>Filtre par type</h3>
            
            {generator._get_image_html("06_backup", "006", 
                "Filtre par type", 
                "Menu déroulant pour filtrer les sauvegardes par type")}
            
            <div class="info-box">
                <h4>🏷️ Comment ça marche ?</h4>
                <p>Cliquez sur le menu déroulant <strong>"🏷️ Filtrer par type"</strong> et choisissez :</p>
                <ul>
                    <li><strong>Tous</strong> : Affiche tous les types</li>
                    <li><strong>🛡️ Sécurité</strong> : Uniquement les sauvegardes de sécurité</li>
                    <li><strong>🧹 Nettoyage</strong> : Uniquement les sauvegardes de nettoyage</li>
                    <li><strong>📦 Avant RPA</strong> : Uniquement les sauvegardes avant compilation en RPA</li>
                    <li><strong>🔗 Avant combinaison</strong> : Uniquement les sauvegardes avant combinaison</li>
                    <li><strong>⚡ Édition temps réel</strong> : Uniquement les sauvegardes d'édition</li>
            </ul>
            </div>
            
            <div class="tip-box">
                <h4>🎯 Filtrage puissant</h4>
                <p>Vous pouvez <strong>combiner les deux filtres</strong> ! Par exemple :</p>
                <ul>
                    <li>Jeu = "Game_Name" + Type = "Sécurité" → Affiche uniquement les sauvegardes de sécurité de ce jeu</li>
                    <li>Les statistiques s'adaptent en temps réel</li>
                    <li>La barre de statut indique les filtres actifs</li>
                </ul>
            </div>
            
            <div class="warning-box">
                <h4>⚠️ Attention au filtre actif</h4>
                <p>Quand un filtre est actif, vous ne voyez qu'une <strong>partie</strong> de vos sauvegardes. 
                Vérifiez bien la barre de statut en bas pour savoir si un filtre est appliqué !</p>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 7 : TREE VIEW DES SAUVEGARDES
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_7 = f"""
        <div class="section" id="treeview">
            <h2>🌳 Tree View des Sauvegardes</h2>
            
            <p>Le <strong>Tree View</strong> vous donne une <strong>vue hiérarchique</strong> de toutes vos sauvegardes, 
            organisées de manière logique et intuitive.</p>
            
            {generator._get_image_html("06_backup", "007", 
                "Tree view des sauvegardes", 
                "Vue hiérarchique montrant tous les types de sauvegardes organisés")}
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="info-box" style="margin: 0;">
                    <h4>🌳 Structure hiérarchique</h4>
                    <p>Le Tree View organise vos sauvegardes selon cette logique :</p>
                    <ul>
                        <li><strong>Niveau 1</strong> : Checkbox</li>
                        <li><strong>Niveau 2</strong> : Nom du jeu</li>
                        <li><strong>Niveau 3</strong> : Nom du fichier/dossier</li>
                        <li><strong>Niveau 4</strong> : Type de sauvegarde</li>
                        <li><strong>Niveau 5</strong> : Date de création</li>
                        <li><strong>Niveau 6</strong> : Taille</li>
                    </ul>
                </div>
                
                <div class="tip-box" style="margin: 0;">
                    <h4>🎯 Avantages du Tree View</h4>
                    <ul>
                        <li><strong>Navigation intuitive</strong> : Structure claire et logique</li>
                        <li><strong>Vue d'ensemble</strong> : Toutes les sauvegardes en un coup d'œil</li>
                        <li><strong>Organisation par jeu</strong> : Facile de trouver ce qui vous intéresse</li>
                        <li><strong>Types visibles</strong> : Distinction claire entre les types</li>
                    </ul>
                </div>
            </div>
            
            <div class="info-box">
                <h4>🎮 Interactions avec le Tree View</h4>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 1rem 0;">
                    <div>
                        <h5>🔍 Navigation de base</h5>
                        <ul>
                            <li><strong>Clic sur le nom</strong> : Sélectionner l'élément</li>
                            <li><strong>Clic droit</strong> : Menu contextuel</li>
                            <li><strong>Scroll</strong> : Naviguer dans la liste</li>
                        </ul>
                    </div>
                    <div>
                        <h5>⌨️ Raccourcis clavier</h5>
                        <ul>
                            <li><strong>Flèches ↑↓</strong> : Navigation clavier</li>
                            <li><strong>Molette</strong> : Scroll fluide</li>
                        </ul>
                    </div>
                    <div>
                        <h5>💡 Sélection multiple</h5>
                        <ul>
                            <li><strong>Clic + Ctrl</strong> : Ajouter à la sélection</li>
                            <li><strong>Clic + Shift</strong> : Sélectionner une plage</li>
                            <li><strong>Checkbox</strong> : Sélection visuelle</li>
                        </ul>
                    </div>
                </div>
                <p><strong>💡 Astuce :</strong> Le Tree View est particulièrement utile pour comprendre l'organisation de vos sauvegardes, identifier rapidement les sauvegardes d'un jeu spécifique, et naviguer facilement dans une grande quantité de données.</p>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 8 : ACTIONS SUR LES SAUVEGARDES
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_8 = f"""
        <div class="section" id="actions">
            <h2>🎯 Actions sur les Sauvegardes</h2>
            
            <p>Cette section couvre toutes les <strong>actions disponibles</strong> dans le gestionnaire de sauvegardes : 
            restaurer, supprimer et accéder aux dossiers. Chaque action est adaptée selon le type de sauvegarde sélectionnée.</p>
            
            <h3>Actions disponibles</h3>
            
            {generator._get_image_html("06_backup", "008", 
                "Actions sur les sauvegardes", 
                "Boutons d'action disponibles pour les sauvegardes sélectionnées")}
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="info-box" style="margin: 0;">
                    <h4>🔧 Actions disponibles</h4>
                    <p>Selon la sauvegarde sélectionnée, vous pouvez :</p>
                    <ul>
                        <li><strong>💾 Restaurer</strong> : Restauration intelligente (ZIP → extraction, Fichier → remplacement)</li>
                        <li><strong>📄 Restaurer vers...</strong> : Copier la sauvegarde à un emplacement choisi</li>
                        <li><strong>🗑️ Supprimer</strong> : Supprimer définitivement la sauvegarde (une ou plusieurs sélectionnées)</li>
                        <li><strong>📁 Ouvrir le Dossier</strong> : Accéder au dossier mère des sauvegardes (02_Sauvegardes)</li>
                    </ul>
                    <p>Les boutons s'activent automatiquement selon la sélection et le type de sauvegarde !</p>
                </div>
                
                <div class="tip-box" style="margin: 0;">
                    <h4>🎯 Workflow recommandé</h4>
                    <p>Pour une gestion efficace de vos sauvegardes :</p>
                    <ol>
                        <li><strong>Sélectionnez</strong> les sauvegardes à traiter (une ou plusieurs)</li>
                        <li><strong>Choisissez l'action</strong> appropriée selon vos besoins</li>
                        <li><strong>Confirmez</strong> les dialogues de sécurité</li>
                        <li><strong>Vérifiez</strong> le résultat dans la barre de statut</li>
                    </ol>
                </div>
            </div>
            
            <h3>💾 Restaurer une Sauvegarde</h3>
            
            <p>La restauration vous permet de <strong>récupérer une version antérieure</strong> de vos fichiers. 
            RenExtract adapte automatiquement le processus selon le type de sauvegarde :</p>
            
            <div class="info-box">
                <h4>🎯 Types de Restauration Intelligente</h4>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1rem 0;">
                    <div>
                        <h5>📁 Archives ZIP (Nettoyage, RPA, Combinaison)</h5>
                        <ul>
                            <li><strong>Extraction automatique</strong> vers le dossier original</li>
                            <li><strong>Détection intelligente</strong> du chemin source</li>
                            <li><strong>Restauration complète</strong> du dossier</li>
                            <li>Gestion des conflits de fichiers</li>
                        </ul>
                    </div>
                    <div>
                        <h5>📄 Fichiers individuels (Sécurité, Édition)</h5>
                        <ul>
                            <li><strong>Remplacement direct</strong> du fichier original</li>
                            <li><strong>Gestion des conflits</strong> avec renommage automatique</li>
                            <li><strong>Suppression automatique</strong> après restauration</li>
                            <li>Protection contre l'écrasement</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="info-box" style="margin: 0;">
                    <h4>💾 Restaurer (normal)</h4>
                    <p><strong>Ce qui se passe :</strong></p>
                    <ol>
                        <li>Sélectionne une sauvegarde dans la liste</li>
                        <li>Clique sur <strong>"💾 Restaurer"</strong></li>
                        <li>Confirme la restauration</li>
                        <li><strong>ZIP :</strong> Extraction vers le dossier original</li>
                        <li><strong>Fichier :</strong> Remplacement du fichier original</li>
                        <li>La sauvegarde est <strong>automatiquement supprimée</strong></li>
                    </ol>
                    <p><strong>Avantage :</strong> Restauration intelligente au bon endroit</p>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>📄 Restaurer vers... (personnalisé)</h4>
                    <p><strong>Ce qui se passe :</strong></p>
                    <ol>
                        <li>Sélectionne une sauvegarde</li>
                        <li>Clique sur <strong>"📄 Restaurer vers..."</strong></li>
                        <li><strong>ZIP :</strong> Choisissez le dossier de destination</li>
                        <li><strong>Fichier :</strong> Choisissez l'emplacement et le nom</li>
                        <li>Le contenu est copié là où vous voulez</li>
                        <li>La sauvegarde reste disponible</li>
                    </ol>
                    <p><strong>Avantage :</strong> Vous gardez la sauvegarde et l'original</p>
                </div>
            </div>
            
            <div class="info-box">
                <h4>🧠 Détection Intelligente du Chemin Source</h4>
                <p>RenExtract utilise une <strong>logique avancée</strong> pour retrouver automatiquement le bon emplacement :</p>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1rem 0;">
                    <div>
                        <h5>🎯 Pour les Archives ZIP</h5>
                        <ol>
                            <li><strong>Métadonnées</strong> : Utilise le chemin stocké lors de la sauvegarde</li>
                            <li><strong>Reconstruction</strong> : Reconstitue le chemin basé sur le projet</li>
                            <li><strong>Détection projet</strong> : Trouve automatiquement le dossier racine</li>
                            <li><strong>Fallback</strong> : Demande à l'utilisateur si nécessaire</li>
                        </ol>
                    </div>
                    <div>
                        <h5>📄 Pour les Fichiers Individuels</h5>
                        <ol>
                            <li><strong>Chemin original</strong> : Utilise le chemin exact du fichier</li>
                            <li><strong>Vérification</strong> : S'assure que le fichier existe</li>
                            <li><strong>Conflit</strong> : Renomme automatiquement si nécessaire</li>
                            <li><strong>Sécurité</strong> : Évite l'écrasement accidentel</li>
                        </ol>
                    </div>
                </div>
                <p><strong>💡 Résultat :</strong> Dans 99% des cas, la restauration se fait automatiquement au bon endroit !</p>
            </div>
            
            <div class="warning-box">
                <h4>⚠️ Attention : Remplacement du fichier</h4>
                <p>Lors d'une restauration normale :</p>
                <ul>
                    <li>Le fichier actuel sera <strong>remplacé</strong> par la sauvegarde</li>
                    <li>Cette action est <strong>irréversible</strong> (sauf si vous avez une autre sauvegarde)</li>
                    <li>La sauvegarde est supprimée après restauration pour éviter les doublons</li>
                    <li>Vérifiez bien les détails (jeu, fichier, date) avant de confirmer !</li>
                </ul>
            </div>
            
            <h3>🗑️ Supprimer des Sauvegardes</h3>
            
            <p>Pour libérer de l'espace disque, vous pouvez supprimer les sauvegardes dont vous n'avez plus besoin. 
            Vous pouvez supprimer <strong>une sauvegarde unique</strong> ou <strong>plusieurs sauvegardes en une fois</strong>.</p>
            
            {generator._get_image_html("06_backup", "009", 
                "Dialogue de confirmation suppression", 
                "Fenêtre de confirmation avant suppression définitive")}
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="step-box" style="margin: 0;">
                    <h4>📝 Étapes de suppression</h4>
                    <ol>
                        <li>Sélectionne une ou plusieurs sauvegardes dans la liste</li>
                        <li>Clique sur le bouton <strong>"🗑️ Supprimer"</strong> (rouge)</li>
                        <li>Lis attentivement les détails affichés dans la confirmation</li>
                        <li>Confirme en cliquant sur <strong>"Oui"</strong></li>
                        <li>La ou les sauvegardes sont définitivement supprimées</li>
                    </ol>
                </div>
                
                <div class="tip-box" style="margin: 0;">
                    <h4>✅ Supprimer sans risque</h4>
                    <ul>
                        <li>Sauvegardes très anciennes (plusieurs semaines/mois)</li>
                        <li>Sauvegardes de jeux terminés</li>
                        <li>Doublons ou versions intermédiaires</li>
                        <li>Sauvegardes de tests ou d'essais</li>
                    </ul>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="warning-box" style="margin: 0;">
                    <h4>❌ À conserver</h4>
                    <ul>
                        <li>Sauvegardes de sécurité récentes</li>
                        <li>Dernière sauvegarde avant modification importante</li>
                        <li>Sauvegardes de projets en cours</li>
                        <li>Dernière sauvegarde de chaque jeu</li>
                    </ul>
                </div>
                
                <div class="warning-box" style="margin: 0;">
                    <h4>⚠️ IMPORTANT : Action irréversible</h4>
                    <p><strong>La suppression est DÉFINITIVE</strong> ! Vous ne pourrez pas récupérer une sauvegarde supprimée.</p>
                    <p>Avant de supprimer, vérifiez bien :</p>
                    <ul>
                        <li>✅ C'est bien la bonne sauvegarde ?</li>
                        <li>✅ Vous n'en aurez plus besoin ?</li>
                        <li>✅ Vous avez d'autres sauvegardes si nécessaire ?</li>
                        <li>✅ Le jeu et le fichier correspondent bien ?</li>
                    </ul>
                </div>
            </div>
            
            <div class="info-box">
                <h4>🎯 Cas d'Usage par Type de Sauvegarde</h4>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1rem 0;">
                    <div>
                        <h5>📁 Archives ZIP - Quand les utiliser ?</h5>
                        <ul>
                            <li><strong>Nettoyage</strong> : Restaurer tout le dossier `tl` après erreur</li>
                            <li><strong>Avant RPA</strong> : Revenir à l'état avant compilation</li>
                            <li><strong>Avant combinaison</strong> : Annuler une fusion problématique</li>
                            <li><strong>Avantage</strong> : Restauration complète en une action</li>
                        </ul>
                    </div>
                    <div>
                        <h5>📄 Fichiers individuels - Quand les utiliser ?</h5>
                        <ul>
                            <li><strong>Sécurité</strong> : Restaurer un fichier spécifique</li>
                            <li><strong>Édition temps réel</strong> : Annuler une modification récente</li>
                            <li><strong>Avantage</strong> : Restauration précise et rapide</li>
                            <li><strong>Rotation</strong> : Gestion automatique (max 10 fichiers) - Édition temps réel uniquement</li>
                        </ul>
                    </div>
                </div>
            </div>
            
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 9 : FONCTIONNALITÉS AVANCÉES
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_9 = f"""
        <div class="section" id="avancees">
            <h2>⚙️ Fonctionnalités Avancées</h2>
            
            <p>Le gestionnaire de sauvegardes intègre plusieurs technologies pour optimiser votre expérience :</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                
                <div class="info-box" style="margin: 0;">
                    <h4>🚀 Cache intelligent</h4>
                    <p><strong>Problème résolu :</strong> Chargement lent avec beaucoup de sauvegardes</p>
                    <p><strong>Solution :</strong></p>
                    <ul>
                        <li>Cache mémoire avec TTL de 60 secondes</li>
                        <li>Cache persistant sur disque (entre sessions)</li>
                        <li>Invalidation automatique lors de modifications</li>
                        <li>Chargement ultra-rapide (même avec 1000+ sauvegardes)</li>
                    </ul>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>🪟 Fenêtre persistante</h4>
                    <p><strong>Avantage :</strong> Réactivité maximale</p>
                    <p><strong>Comment ça marche :</strong></p>
                    <ul>
                        <li>La fenêtre se cache au lieu de se fermer</li>
                        <li>Réouverture instantanée (pas de rechargement)</li>
                        <li>Données toujours à jour</li>
                        <li>Économie de ressources</li>
                    </ul>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>📊 Index des métadonnées</h4>
                    <p><strong>Optimisation :</strong> Accès O(1) aux infos</p>
                    <p><strong>Bénéfices :</strong></p>
                    <ul>
                        <li>Recherche ultra-rapide par chemin</li>
                        <li>Pas de scan complet nécessaire</li>
                        <li>Métadonnées toujours synchronisées</li>
                        <li>Performance constante quelle que soit la quantité</li>
                    </ul>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>🔄 Rotation automatique</h4>
                    <p><strong>Type concerné :</strong> Édition temps réel uniquement</p>
                    <p><strong>Fonctionnement :</strong></p>
                    <ul>
                        <li>Maximum : 10 fichiers conservés</li>
                        <li>Suppression automatique des plus anciens</li>
                        <li>Aucune intervention manuelle nécessaire</li>
                        <li>Gestion optimale de l'espace disque</li>
                    </ul>
                </div>
                
            </div>
            
        </div>
    """
    
    
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
