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
                    <div style="font-size: 0.9em; opacity: 0.8;">Les 4 types de sauvegardes</div>
                </a>
                
                <a href="#structure" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">📂 Structure</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Organisation des fichiers</div>
                </a>
                
                <a href="#filtres" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🔍 Filtres</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Trouver rapidement</div>
                </a>
                
                <a href="#gestion" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">📋 Gestion</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Tri et navigation</div>
                </a>
                
                <a href="#restauration" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">💾 Restaurer</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Récupérer un fichier</div>
                </a>
                
                <a href="#suppression" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">🗑️ Supprimer</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Nettoyer l'espace</div>
                </a>
                
                <a href="#avancees" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">⚙️ Avancé</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Fonctionnalités techniques</div>
                </a>
                
                <a href="#astuces-sauvegardes" class="nav-card" style="display: block; padding: 12px 16px; background: var(--hdr); border-radius: 6px; text-decoration: none; color: var(--fg); border: 1px solid var(--sep); transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 4px; color: var(--accent);">💡 Astuces</div>
                    <div style="font-size: 0.9em; opacity: 0.8;">Bonnes pratiques</div>
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
            
            {generator._get_image_html("06_sauvegardes", "003", 
                "Interface complète du gestionnaire de sauvegardes", 
                "Vue d'ensemble du gestionnaire avec statistiques, filtres et liste des sauvegardes")}
            
            <h3>Qu'est-ce que c'est ?</h3>
            <p>Le <strong>Gestionnaire de Sauvegardes</strong> est ton centre de contrôle pour toutes les sauvegardes automatiques créées par RenExtract. 
            Chaque fois que tu lances une opération importante (nettoyage, extraction, édition), RenExtract crée automatiquement une sauvegarde de tes fichiers.</p>
            
            <p>Cette interface te permet de :</p>
            <ul>
                <li>📊 <strong>Visualiser</strong> toutes tes sauvegardes en un coup d'œil</li>
                <li>🔍 <strong>Filtrer</strong> par jeu ou par type de sauvegarde</li>
                <li>💾 <strong>Restaurer</strong> un fichier en cas de problème</li>
                <li>🗑️ <strong>Supprimer</strong> les anciennes sauvegardes pour libérer de l'espace</li>
                <li>📈 <strong>Suivre</strong> l'espace disque utilisé</li>
            </ul>
            
            <div class="info-box">
                <h4>🛡️ Sécurité avant tout</h4>
                <p>RenExtract ne supprime <strong>jamais</strong> une sauvegarde sans ta confirmation explicite. Même après restauration, 
                le fichier sauvegardé est automatiquement supprimé uniquement pour éviter les doublons.</p>
            </div>
            
            <h3>Quand l'utiliser ?</h3>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="tip-box" style="margin: 0;">
                    <h4>✅ Situations courantes</h4>
                    <ul>
                        <li>Tu as fait une erreur lors du nettoyage</li>
                        <li>Un fichier a été modifié par erreur</li>
                        <li>Tu veux récupérer une ancienne version</li>
                        <li>Tu veux libérer de l'espace disque</li>
                    </ul>
                </div>
                
                <div class="warning-box" style="margin: 0;">
                    <h4>⚠️ Important à savoir</h4>
                    <ul>
                        <li>Les sauvegardes prennent de l'espace disque</li>
                        <li>Pense à nettoyer régulièrement</li>
                        <li>La suppression est <strong>irréversible</strong></li>
                        <li>Vérifie avant de supprimer !</li>
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
            
            {generator._get_image_html("06_sauvegardes", "001", 
                "Bouton Sauvegardes dans l'onglet OUTILS", 
                "Accès au gestionnaire de sauvegardes depuis l'onglet OUTILS")}
            
            <h3>Comment ouvrir le gestionnaire ?</h3>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                
                <div class="step-box" style="margin: 0;">
                    <h4>📍 Étape par étape</h4>
                    <ol>
                        <li><strong>Clique sur l'onglet OUTILS</strong> (jaune) dans l'interface principale</li>
                        <li><strong>Clique sur le bouton "💾 Sauvegardes"</strong></li>
                        <li>Le gestionnaire s'ouvre dans une nouvelle fenêtre</li>
                    </ol>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>💡 Bon à savoir</h4>
                    <p>Le gestionnaire de sauvegardes est une <strong>fenêtre persistante</strong> : quand tu la fermes, elle se cache simplement.</p>
                    <p>La prochaine fois que tu l'ouvres, elle <strong>réapparaît instantanément</strong> et charge automatiquement les dernières sauvegardes, 
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
            
            <p>RenExtract crée automatiquement <strong>4 types de sauvegardes</strong> différents selon le contexte. Chaque type a son rôle spécifique :</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                
                <div class="info-box" style="margin: 0;">
                    <h4>🛡️ Sécurité</h4>
                    <p><strong>Quand ?</strong> Avant chaque extraction de fichiers</p>
                    <p><strong>Pourquoi ?</strong> Protection maximale de tes fichiers originaux</p>
                    <p><strong>À savoir :</strong> Ces sauvegardes sont précieuses, ne les supprime pas trop vite !</p>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>🧹 Nettoyage</h4>
                    <p><strong>Quand ?</strong> Avant chaque opération de nettoyage de projet</p>
                    <p><strong>Pourquoi ?</strong> Te permet de revenir en arrière si nécessaire</p>
                    <p><strong>À savoir :</strong> Très utile si un nettoyage supprime quelque chose d'important</p>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>📦 Avant RPA</h4>
                    <p><strong>Quand ?</strong> Juste avant la construction d'une archive RPA</p>
                    <p><strong>Pourquoi ?</strong> Garder une trace avant la compression</p>
                    <p><strong>À savoir :</strong> Protection contre la corruption potentielle des données lors de la construction RPA</p>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>⚡ Édition temps réel</h4>
                    <p><strong>Quand ?</strong> À chaque modification dans l'éditeur temps réel</p>
                    <p><strong>Pourquoi ?</strong> Historique de modifications automatique</p>
                    <p><strong>Rotation ?</strong> ✅ <strong>Max 10 fichiers</strong> (les plus anciens sont supprimés automatiquement)</p>
                    <p><strong>À savoir :</strong> Ces sauvegardes tournent automatiquement, pas besoin de les gérer !</p>
                </div>
                
            </div>
            
            <div class="tip-box">
                <h4>💡 Astuce : Libérer de l'espace</h4>
                <p>Les sauvegardes <strong>Édition temps réel</strong> se gèrent toutes seules avec un maximum de 10 fichiers. 
                Pour libérer de l'espace, concentre-toi sur les sauvegardes des types (Sécurité, Nettoyage, Avant RPA) que tu n'utilises plus.</p>
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
            <p>RenExtract organise tes sauvegardes de manière <strong>intelligente et structurée</strong> (arborescence collapsible) :</p>
            
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
02_Sauvegardes/                        ← Dossier racine
├── &lt;Game_Name&gt;/                      ← Nom du jeu
│   ├── &lt;File_name&gt;/                  ← Nom du fichier (sans extension)
│   │   ├── security/                ← Sauvegardes de sécurité
│   │   │   └── file_20250110_143022.rpy
│   │   ├── cleanup/                 ← Sauvegardes de nettoyage
│   │   │   └── file_20250110_150030.rpy
│   │   ├── rpa_build/               ← Sauvegardes avant RPA
│   │   │   └── file_20250110_160045.rpy
│   │   └── realtime_edit/           ← Sauvegardes édition (max 10)
│   │       ├── file_20250110_170001.rpy
│   │       ├── file_20250110_170015.rpy
│   │       └── ... (max 10 fichiers)
├── backup_metadata.json             ← Métadonnées
└── backup_cache.pkl                 ← Cache pour performances
                    </pre>
                </div>
                </div>
                
            <h3>Avantages de cette structure</h3>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="tip-box" style="margin: 0;">
                    <h4>✅ Organisation claire</h4>
                    <ul>
                        <li>Un dossier par jeu</li>
                        <li>Un sous-dossier par fichier</li>
                        <li>Un type par sous-dossier</li>
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
                <p>Le dossier <code>02_Sauvegardes</code> est situé à la racine de ton dossier de travail RenExtract. 
                Tu peux y accéder manuellement si besoin, mais le gestionnaire intégré est beaucoup plus pratique !</p>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 5 : FILTRER LES SAUVEGARDES
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_5 = f"""
        <div class="section" id="filtres">
            <h2>🔍 Filtrer les Sauvegardes</h2>
            
            <p>Quand tu as beaucoup de sauvegardes, les <strong>filtres</strong> sont tes meilleurs amis ! 
            RenExtract te propose deux filtres complémentaires :</p>
            
            <h3>Filtre par jeu</h3>
            
            {generator._get_image_html("06_sauvegardes", "004", 
                "Menu de filtrage par jeu", 
                "Liste déroulante pour filtrer les sauvegardes par jeu")}
            
            <div class="info-box">
                <h4>🎮 Comment ça marche ?</h4>
                <p>Clique sur le menu déroulant <strong>"🎮 Filtrer par jeu"</strong> et choisis :</p>
                <ul>
                    <li><strong>Tous</strong> : Affiche toutes les sauvegardes (tous jeux confondus)</li>
                    <li><strong>Un jeu spécifique</strong> : Affiche uniquement les sauvegardes de ce jeu</li>
                </ul>
                <p>Le tableau et les statistiques s'adaptent automatiquement !</p>
            </div>
            
            <h3>Filtre par type</h3>
            
            {generator._get_image_html("06_sauvegardes", "002", 
                "Menu de filtrage par type", 
                "Liste déroulante pour filtrer les sauvegardes par type (Sécurité, Nettoyage, etc.)")}
            
            <div class="info-box">
                <h4>🏷️ Comment ça marche ?</h4>
                <p>Clique sur le menu déroulant <strong>"🏷️ Filtrer par type"</strong> et choisis :</p>
                <ul>
                    <li><strong>Tous</strong> : Affiche tous les types</li>
                    <li><strong>🛡️ Sécurité</strong> : Uniquement les sauvegardes de sécurité</li>
                    <li><strong>🧹 Nettoyage</strong> : Uniquement les sauvegardes de nettoyage</li>
                    <li><strong>📦 Avant RPA</strong> : Uniquement les sauvegardes avant compilation en RPA</li>
                    <li><strong>⚡ Édition temps réel</strong> : Uniquement les sauvegardes d'édition</li>
            </ul>
            </div>
            
            <h3>Combiner les filtres</h3>
            
            {generator._get_image_html("06_sauvegardes", "008", 
                "Filtres combinés actifs", 
                "Exemple de filtrage par jeu ET par type simultanément")}
            
            <div class="tip-box">
                <h4>🎯 Filtrage puissant</h4>
                <p>Tu peux <strong>combiner les deux filtres</strong> ! Par exemple :</p>
                <ul>
                    <li>Jeu = "Game_Name" + Type = "Sécurité" → Affiche uniquement les sauvegardes de sécurité de ce jeu</li>
                    <li>Les statistiques s'adaptent en temps réel</li>
                    <li>La barre de statut indique les filtres actifs</li>
                </ul>
            </div>
            
            <div class="warning-box">
                <h4>⚠️ Attention au filtre actif</h4>
                <p>Quand un filtre est actif, tu ne vois qu'une <strong>partie</strong> de tes sauvegardes. 
                Vérifie bien la barre de statut en bas pour savoir si un filtre est appliqué !</p>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 6 : GÉRER LES SAUVEGARDES
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_6 = f"""
        <div class="section" id="gestion">
            <h2>📋 Gérer les Sauvegardes</h2>
            
            <h3>Tri des colonnes</h3>
            
            {generator._get_image_html("06_sauvegardes", "006", 
                "Tri par nom de fichier", 
                "Exemple de tri avec indicateur de direction")}
            
            <div class="info-box">
                <h4>🔄 Trier pour mieux s'y retrouver</h4>
                <p>Clique sur <strong>n'importe quel en-tête de colonne</strong> pour trier la liste :</p>
                <ul>
                    <li><strong>Nom du jeu</strong> : Tri alphabétique des jeux</li>
                    <li><strong>Nom du fichier</strong> : Tri alphabétique des fichiers</li>
                    <li><strong>Type backup</strong> : Tri par type de sauvegarde</li>
                    <li><strong>Date créé</strong> : Tri chronologique (plus récent/ancien)</li>
                    <li><strong>Taille</strong> : Tri par taille de fichier</li>
                </ul>
                <p>Un indicateur (<strong>↑</strong> ou <strong>↓</strong>) apparaît pour montrer l'ordre actuel.</p>
            </div>
            
            <h3>Navigation dans le tableau</h3>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                <div class="tip-box" style="margin: 0;">
                    <h4>⌨️ Raccourcis clavier</h4>
                    <ul>
                        <li><strong>Clic</strong> : Sélectionner une sauvegarde</li>
                        <li><strong>Clic droit</strong> : Menu contextuel</li>
                        <li><strong>Flèches ↑↓ ou molette</strong> : Naviguer dans la liste</li>
                    </ul>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>📊 Colonnes affichées</h4>
                    <ul>
                        <li><strong>Nom du jeu</strong> : Jeu concerné</li>
                        <li><strong>Nom du fichier</strong> : Fichier sauvegardé</li>
                        <li><strong>Type backup</strong> : Type de sauvegarde</li>
                        <li><strong>Date créé</strong> : Date et heure</li>
                        <li><strong>Taille</strong> : Espace utilisé</li>
                    </ul>
                </div>
            </div>
            
            <div class="tip-box">
                <h4>💡 Astuce : Scroll infini</h4>
                <p>Le tableau supporte le <strong>scroll vertical et horizontal</strong>. Si tu as beaucoup de sauvegardes, 
                utilise les scrollbars pour naviguer confortablement !</p>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 7 : RESTAURER UNE SAUVEGARDE
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_7 = f"""
        <div class="section" id="restauration">
            <h2>💾 Restaurer une Sauvegarde</h2>
            
            <p>La restauration te permet de <strong>récupérer une version antérieure</strong> de ton fichier. 
            RenExtract propose deux modes de restauration :</p>
            
            <h3>Actions disponibles</h3>
            
            {generator._get_image_html("06_sauvegardes", "005", 
                "Boutons d'action sur les sauvegardes", 
                "Boutons Restaurer, Restaurer vers... et Supprimer")}
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                
                <div class="info-box" style="margin: 0;">
                    <h4>💾 Restaurer (normal)</h4>
                    <p><strong>Ce qui se passe :</strong></p>
                    <ol>
                        <li>Sélectionne une sauvegarde dans la liste</li>
                        <li>Clique sur <strong>"💾 Restaurer"</strong></li>
                        <li>Confirme la restauration</li>
                        <li>Le fichier remplace l'original</li>
                        <li>La sauvegarde est <strong>automatiquement supprimée</strong></li>
                    </ol>
                    <p><strong>Avantage :</strong> Restauration rapide au bon endroit</p>
                </div>
                
                <div class="info-box" style="margin: 0;">
                    <h4>📄 Restaurer vers... (personnalisé)</h4>
                    <p><strong>Ce qui se passe :</strong></p>
                    <ol>
                        <li>Sélectionne une sauvegarde</li>
                        <li>Clique sur <strong>"📄 Restaurer vers..."</strong></li>
                        <li>Choisis le dossier de destination</li>
                        <li>Le fichier est copié là où tu veux</li>
                        <li>La sauvegarde reste disponible</li>
                    </ol>
                    <p><strong>Avantage :</strong> Tu gardes la sauvegarde et l'original</p>
                </div>
                
            </div>
            
            <h3>Confirmation de restauration</h3>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 1.5rem 0; align-items: start;">
                {generator._get_image_html("06_sauvegardes", "007", 
                    "Dialogue de confirmation restauration", 
                    "Fenêtre de confirmation avant restauration d'une sauvegarde")}
                
                <div class="warning-box" style="margin: 0;">
                    <h4>⚠️ Attention : Remplacement du fichier</h4>
                    <p>Lors d'une restauration normale :</p>
                    <ul>
                        <li>Le fichier actuel sera <strong>remplacé</strong> par la sauvegarde</li>
                        <li>Cette action est <strong>irréversible</strong> (sauf si tu as une autre sauvegarde)</li>
                        <li>La sauvegarde est supprimée après restauration pour éviter les doublons</li>
                        <li>Vérifie bien les détails (jeu, fichier, date) avant de confirmer !</li>
                    </ul>
                </div>
            </div>
            
            <div class="tip-box">
                <h4>💡 Astuce : Menu contextuel</h4>
                <p>Tu peux aussi <strong>cliquer droit</strong> sur une sauvegarde pour accéder rapidement aux actions de restauration !</p>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 8 : SUPPRIMER UNE SAUVEGARDE
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_8 = f"""
        <div class="section" id="suppression">
            <h2>🗑️ Supprimer une Sauvegarde</h2>
            
            <p>Pour libérer de l'espace disque, tu peux supprimer les sauvegardes dont tu n'as plus besoin.</p>
            
            <h3>Comment supprimer ?</h3>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 1.5rem 0; align-items: start;">
                <div class="step-box" style="margin: 0;">
                    <h4>📝 Étapes de suppression</h4>
                    <ol>
                        <li>Sélectionne une ou plusieurs sauvegardes dans la liste</li>
                        <li>Clique sur le bouton <strong>"🗑️ Supprimer"</strong> (rouge)</li>
                        <li>Lis attentivement les détails affichés dans la confirmation</li>
                        <li>Confirme en cliquant sur <strong>"Oui"</strong></li>
                        <li>La sauvegarde est définitivement supprimée</li>
            </ol>
                </div>
                
                {generator._get_image_html("06_sauvegardes", "009", 
                    "Dialogue de confirmation suppression", 
                    "Fenêtre de confirmation avant suppression définitive")}
            </div>
            
            <div class="warning-box">
                <h4>⚠️ IMPORTANT : Action irréversible</h4>
                <p><strong>La suppression est DÉFINITIVE</strong> ! Tu ne pourras pas récupérer une sauvegarde supprimée.</p>
                <p>Avant de supprimer, vérifie bien :</p>
                <ul>
                    <li>✅ C'est bien la bonne sauvegarde ?</li>
                    <li>✅ Tu n'en auras plus besoin ?</li>
                    <li>✅ Tu as d'autres sauvegardes si nécessaire ?</li>
                    <li>✅ Le jeu et le fichier correspondent bien ?</li>
                </ul>
            </div>
            
            <h3>Quelles sauvegardes supprimer ?</h3>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                
                <div class="tip-box" style="margin: 0;">
                    <h4>✅ Supprimer sans risque</h4>
                    <ul>
                        <li>Sauvegardes très anciennes (plusieurs semaines/mois)</li>
                        <li>Sauvegardes de jeux terminés</li>
                        <li>Doublons ou versions intermédiaires</li>
                        <li>Sauvegardes de tests ou d'essais</li>
                    </ul>
                </div>
                
                <div class="warning-box" style="margin: 0;">
                    <h4>❌ À conserver</h4>
                    <ul>
                        <li>Sauvegardes de sécurité récentes</li>
                        <li>Dernière sauvegarde avant modification importante</li>
                        <li>Sauvegardes de projets en cours</li>
                        <li>En cas de doute, garde-les !</li>
                    </ul>
                </div>
                
            </div>
            
            <div class="info-box">
                <h4>🧹 Nettoyage automatique des dossiers vides</h4>
                <p>Quand tu supprimes une sauvegarde, RenExtract nettoie automatiquement les dossiers vides. 
                Pas besoin de t'en soucier !</p>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 9 : FONCTIONNALITÉS AVANCÉES
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_9 = f"""
        <div class="section" id="avancees">
            <h2>⚙️ Fonctionnalités Avancées</h2>
            
            <p>Le gestionnaire de sauvegardes intègre plusieurs technologies pour optimiser ton expérience :</p>
            
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
            
            <div class="tip-box">
                <h4>💡 Pour les curieux : Structure technique</h4>
                <p>Si tu veux en savoir plus sur la structure technique :</p>
                <ul>
                    <li><strong>Singleton Pattern</strong> : Une seule instance du gestionnaire</li>
                    <li><strong>Métadonnées JSON</strong> : Stockage léger et lisible</li>
                    <li><strong>Cache Pickle</strong> : Sérialisation Python pour vitesse maximale</li>
                    <li><strong>Scan hiérarchique</strong> : Parcours optimisé de l'arborescence</li>
                </ul>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 10 : ASTUCES ET BONNES PRATIQUES
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_10 = """
        <div class="section" id="astuces-sauvegardes">
            <h2>💡 Astuces et Bonnes Pratiques</h2>
            
            <p>Quelques conseils pour gérer efficacement tes sauvegardes :</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 1.5rem 0;">
                
                <div class="tip-box" style="margin: 0;">
                    <h4>📅 Vérification régulière</h4>
                    <ul>
                        <li>Ouvre le gestionnaire <strong>une fois par semaine</strong></li>
                        <li>Vérifie l'espace disque utilisé</li>
                        <li>Supprime les sauvegardes obsolètes</li>
                        <li>Garde uniquement ce qui est utile</li>
                    </ul>
                </div>
                
                <div class="tip-box" style="margin: 0;">
                    <h4>🎯 Utiliser les filtres</h4>
                    <ul>
                        <li>Filtre par jeu pour les projets terminés</li>
                        <li>Filtre par type pour cibler les sauvegardes lourdes</li>
                        <li>Combine les filtres pour affiner</li>
                        <li>Trie par taille pour voir les plus gros fichiers</li>
                    </ul>
                </div>
                
                <div class="warning-box" style="margin: 0;">
                    <h4>⚠️ Rotation édition temps réel</h4>
                    <ul>
                        <li>Max 10 fichiers : ancien automatiquement supprimé</li>
                        <li>Pas besoin de gérer manuellement</li>
                        <li>Restaure rapidement si modification récente</li>
                        <li>Ne compte pas dessus pour l'archivage long terme</li>
                    </ul>
                </div>
                
                <div class="tip-box" style="margin: 0;">
                    <h4>💾 Sauvegarde externe importante</h4>
                    <ul>
                        <li>Les sauvegardes RenExtract sont <strong>locales</strong></li>
                        <li>Pour les projets importants, fais des sauvegardes externes</li>
                        <li>Utilise Git, cloud, ou disque externe</li>
                        <li>Ne compte pas uniquement sur RenExtract</li>
                    </ul>
                </div>
                
            </div>
            
            <div class="info-box">
                <h4>🔍 Workflow recommandé</h4>
                <ol>
                    <li><strong>Avant une opération importante</strong> : Vérifie qu'une sauvegarde de sécurité est créée</li>
                    <li><strong>Après l'opération</strong> : Si tout va bien, tu peux supprimer l'ancienne sauvegarde</li>
                    <li><strong>En cas de problème</strong> : Restaure la dernière sauvegarde valide</li>
                    <li><strong>Nettoyage mensuel</strong> : Supprime les sauvegardes de plus de 30 jours si inutiles</li>
                </ol>
            </div>
        </div>
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 11 : CONCLUSION
    # ═══════════════════════════════════════════════════════════════════════════
    
    section_11 = ""
    
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
        section_9 +
        section_10 +
        section_11
    )
