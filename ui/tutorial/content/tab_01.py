# ui/tutorial/content/tab_01.py
"""
Module de contenu pour l'onglet 1 : Sommaire - Table des matières avec navigation
"""

def generate_content(generator, language=None, translations=None):
    """Génère le contenu de l'onglet Sommaire"""
    
    return f"""
        <div class="section">
            <h2>📋 Table des Matières</h2>
            <p>Guide complet de RenExtract organisé par fonctionnalités. Cliquez sur les liens pour naviguer directement vers les sections.</p>
        </div>
        
        <div class="section">
            <h2>🚀 Démarrage</h2>
            <ul style="margin-left: 40px;">
                <li><button class="nav-link-btn" data-target-tab="2" data-target-section="workflow-overview">Vue d'ensemble du workflow</button></li>
                <li><button class="nav-link-btn" data-target-tab="2" data-target-section="quick-start">Démarrage rapide en 4 étapes</button></li>
                <li><button class="nav-link-btn" data-target-tab="2" data-target-section="first-use">Configuration première utilisation</button></li>
            </ul>
        </div>
        
        <div class="section">
            <h2>🖥️ Interface Principale</h2>
            <ul style="margin-left: 40px;">
                <li><button class="nav-link-btn" data-target-tab="3" data-target-section="main-interface">Vue d'ensemble</button></li>
                <li><button class="nav-link-btn" data-target-tab="3" data-target-section="main-preparation">Onglet Préparation</button></li>
                <li><button class="nav-link-btn" data-target-tab="3" data-target-section="main-actions">Onglet Actions</button></li>
                <li><button class="nav-link-btn" data-target-tab="3" data-target-section="main-outils">Onglet Outils</button></li>
            </ul>
        </div>
        
        <div class="section">
            <h2>🎮 Générateur Ren'Py</h2>
            <ul style="margin-left: 40px;">
                <li><button class="nav-link-btn" data-target-tab="4" data-target-section="generator-window">Interface générale</button></li>
                <li><button class="nav-link-btn" data-target-tab="4" data-target-section="gen-extraction-rpa">Extraction & Compilation RPA/RPYC</button></li>
                <li><button class="nav-link-btn" data-target-tab="4" data-target-section="gen-generation">Génération TL et polices GUI</button></li>
                <li><button class="nav-link-btn" data-target-tab="4" data-target-section="gen-extraction-config">Extraction Config (textes oubliés)</button></li>
                <li><button class="nav-link-btn" data-target-tab="4" data-target-section="gen-extraction-resultats">Analyse des résultats</button></li>
                <li><button class="nav-link-btn" data-target-tab="4" data-target-section="gen-combinaison">Combinaison & Division</button></li>
            </ul>
        </div>
        
        <div class="section">
            <h2>💾 Gestionnaire de Sauvegardes</h2>
            <ul style="margin-left: 40px;">
                <li><button class="nav-link-btn" data-target-tab="6" data-target-section="backup-manager">Interface complète</button></li>
                <li><button class="nav-link-btn" data-target-tab="6" data-target-section="backup-statistics">Statistiques et filtres</button></li>
                <li><button class="nav-link-btn" data-target-tab="6" data-target-section="backup-restoration">Processus de restauration</button></li>
                <li><button class="nav-link-btn" data-target-tab="6" data-target-section="backup-cleanup">Nettoyage automatique</button></li>
            </ul>
        </div>
        
        <div class="section">
            <h2>🛠️ Outils Spécialisés</h2>
            <ul style="margin-left: 40px;">
                <li><button class="nav-link-btn" data-target-tab="5" data-target-section="verification-coherence">Vérificateur de Cohérence</button></li>
                <li><button class="nav-link-btn" data-target-tab="5" data-target-section="editeur-temps-reel">Éditeur Temps Réel</button></li>
                <li><button class="nav-link-btn" data-target-tab="5" data-target-section="nettoyage-intelligent">Nettoyage Intelligent</button></li>
            </ul>
        </div>
        
        <div class="section">
            <h2>⚙️ Paramètres</h2>
            <ul style="margin-left: 40px;">
                <li><button class="nav-link-btn" data-target-tab="7" data-target-section="vue-ensemble-parametres">⚙️ Vue d'Ensemble des Paramètres</button></li>
                <li><button class="nav-link-btn" data-target-tab="7" data-target-section="onglet-interface">🎨 Onglet Interface & Application</button></li>
                <li><button class="nav-link-btn" data-target-tab="7" data-target-section="onglet-extraction">🛡️ Onglet Extraction & Protection</button></li>
                <li><button class="nav-link-btn" data-target-tab="7" data-target-section="onglet-couleurs">🎨 Onglet Couleurs des Boutons</button></li>
                <li><button class="nav-link-btn" data-target-tab="7" data-target-section="onglet-chemins">🛠️ Onglet Chemins d'Accès</button></li>
                <li><button class="nav-link-btn" data-target-tab="7" data-target-section="footer-parametres">📋 Footer et Actions Globales</button></li>
            </ul>
        </div>
        
        <div class="section">
            <h2>❓ FAQ et Support</h2>
            <ul style="margin-left: 40px;">
                <li><button class="nav-link-btn" data-target-tab="9" data-target-section="faq-section">❓ Questions Fréquentes</button></li>
                <li><button class="nav-link-btn" data-target-tab="9" data-target-section="troubleshooting">🔧 Dépannage Technique</button></li>
                <li><button class="nav-link-btn" data-target-tab="9" data-target-section="support-contact">📧 Contacter l'équipe de développement</button></li>
                <li><button class="nav-link-btn" data-target-tab="9" data-target-section="credits">🏆 Crédits et remerciements</button></li>
            </ul>
        </div>
    """
