# utils/coherence_html_report_generator.py
# Générateur de rapports HTML interactifs pour la cohérence

import os
import json
import html as _html
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from infrastructure.helpers.unified_functions import extract_game_name

class HtmlCoherenceReportGenerator:
    """Générateur de rapports HTML interactifs pour la vérification de cohérence"""
    
    def __init__(self):
        self.report_dir = self._get_report_directory()
        self._ensure_report_directory()
    
    def _get_report_directory(self) -> str:
        """Détermine le répertoire de rapports de cohérence"""
        try:
            from infrastructure.config.constants import FOLDERS
            return FOLDERS["warnings"]  # Retourne 03_Rapports/
        except Exception:
            return os.path.join(".", "03_Rapports")
    
    def _ensure_report_directory(self):
        """Assure l'existence du répertoire de rapports"""
        try:
            Path(self.report_dir).mkdir(parents=True, exist_ok=True)
        except Exception:
            self.report_dir = "."
    
    def _get_css_styles(self) -> str:
        """Retourne les styles CSS pour le rapport de cohérence"""
        return """
        <style>
          :root {
            --bg: #1a1f29; --fg: #e2e8f0; --hdr: #2d3748; --sep: #4a5568;
            --success: #48bb78; --warning: #ed8936; --danger: #f56565; --info: #4a90e2;
            --card-bg: #2d3748; --hover-bg: rgba(255,255,255,0.06); --nav-bg: #1a202c;
            --error-variable: #ff6b9d; --error-tag: #ffa726; --error-placeholder: #ab47bc;
            --error-special: #ef5350; --error-untranslated: #ffcc02; --error-other: #78909c;
          }
          .light {
            --bg: #fafafa; --fg: #222; --hdr: #fff; --sep: #ddd;
            --card-bg: #f8f9fa; --hover-bg: rgba(0,0,0,0.04);
          }
          
          body { 
            font-family: ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, Arial; 
            background: var(--bg); color: var(--fg); margin: 0; line-height: 1.6;
          }
          
          .header {
            background: var(--hdr); padding: 20px; border-bottom: 2px solid var(--sep);
            position: sticky; top: 0; z-index: 1000; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-radius: 0 0 12px 12px;
            margin: 0 15px 0 15px;
          }
          
          .header select {
            position: relative;
            z-index: 1001;
            color: #000;
            background: #fff;
          }
          
          .header select option {
            color: #000;
            background: #fff;
          }
          
          .header select option:hover {
            background: #0d6efd;
            color: #fff;
          }
          
          .header h1 { margin: 0 0 10px 0; font-size: 1.8rem; }
          .header-meta { display: flex; gap: 20px; flex-wrap: wrap; align-items: center; }
          .header-meta span { opacity: 0.9; font-size: 0.95rem; }
          
          .controls { 
            display: flex; gap: 12px; align-items: center; margin-left: auto;
          }
          
          .btn {
            cursor: pointer; padding: 8px 12px; border-radius: 8px; 
            border: 1px solid var(--sep); background: transparent; color: var(--fg);
            transition: all 0.2s; font-size: 0.9rem;
          }
          .btn:hover { background: var(--hover-bg); transform: translateY(-1px); }
          
          .summary-cards {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px; padding: 20px; margin-bottom: 0px;
            background: var(--bg); 
            border-bottom: 1px solid var(--sep);
          }
          
          .card {
            background: var(--card-bg); border: 1px solid var(--sep); 
            border-radius: 12px; padding: 20px; 
            transition: transform 0.2s ease;
          }
          .card:hover { transform: translateY(-2px); }
          
          .card h3 { margin-top: 0; font-size: 1.1rem; }
          
          .stat { display: flex; justify-content: space-between; margin: 8px 0; }
          .stat-value { font-weight: bold; color: var(--info); }
          
          .progress-bar {
            background: var(--sep); height: 8px; border-radius: 4px; overflow: hidden;
            margin: 10px 0;
          }
          .progress-fill { 
            height: 100%; background: var(--danger); 
            transition: width 0.3s ease;
          }
          
          .error-type-section {
            margin: 20px; background: var(--card-bg); border-radius: 12px;
            border: 1px solid var(--sep); overflow: hidden; transition: all 0.2s;
          }
          .error-type-section:hover { transform: translateY(-1px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
          
          .error-type-header {
            background: var(--hdr); padding: 15px 20px; font-weight: bold;
            cursor: pointer; user-select: none;
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid var(--sep);
          }
          
          .error-type-content { padding: 20px; display: none; }
          .error-type-content.expanded { display: block; }
          .issue-header{display:flex;align-items:center;gap:10px;justify-content:space-between;flex-wrap:wrap}
          .issue-line{font-weight:bold;color:var(--warning);margin:0}
          
          .error-type-badge {
            padding: 4px 12px; border-radius: 16px; font-size: 0.8rem; 
            font-weight: bold; color: white;
          }
          
          .badge-variable { background: var(--error-variable); }
          .badge-tag { background: var(--error-tag); }
          .badge-placeholder { background: var(--error-placeholder); }
          .badge-special { background: var(--error-special); }
          .badge-untranslated { background: var(--error-untranslated); color: #000; }
          .badge-other { background: var(--error-other); }
          
          .file-section {
            background: var(--bg); border: 1px solid var(--sep); 
            border-radius: 8px; margin: 15px 0; overflow: hidden;
          }
          
          .file-header {
            background: rgba(255,255,255,0.02); padding: 12px 15px;
            font-weight: 600; color: var(--info); border-bottom: 1px solid var(--sep);
          }
          
          .issue-item {
            padding: 15px; border-bottom: 1px solid var(--sep);
            transition: background 0.2s, opacity 0.3s;
          }
          .issue-item:hover { background: var(--hover-bg); }
          .issue-item:last-child { border-bottom: none; }
          .issue-item.excluded {
            opacity: 0.5;
            background: rgba(72, 187, 120, 0.1);
            border-left: 4px solid var(--success);
          }
          
          .exclude-checkbox-container {
            display: flex; align-items: center; gap: 8px;
            padding: 8px; margin-top: 10px;
            background: rgba(255,255,255,0.03);
            border-radius: 6px;
          }
          .exclude-checkbox {
            width: 18px; height: 18px; cursor: pointer;
            accent-color: var(--success); flex-shrink: 0;
          }
          .exclude-label {
            cursor: pointer; user-select: none; font-size: 0.9rem;
            flex: 1; display: flex; align-items: center;
            padding: 4px 8px; border-radius: 4px;
            transition: background 0.2s, color 0.2s;
          }
          .exclude-label:hover { 
            color: var(--success); 
            background: rgba(100, 200, 100, 0.08);
          }
          .exclusion-text {
            font-size: 0.85rem; opacity: 0.7;
          }
          .exclusion-status {
            font-size: 0.85rem; opacity: 0.9; font-style: italic;
            color: var(--success); font-weight: 500;
            display: none;
          }
          .exclude-checkbox:checked ~ .exclude-label .exclusion-text {
            display: none;
          }
          .exclude-checkbox:checked ~ .exclude-label .exclusion-status {
            display: inline;
          }
          
          .open-in-editor {
              display: inline-flex; align-items: center; gap: 6px;
              font-size: 12px; padding: 6px 10px; border-radius: 6px;
              border: 1px solid var(--sep); background: rgba(13,110,253,0.12);
              cursor: pointer; user-select: none;
              color: var(--fg); /* Utilise la couleur de texte du thème */
              order: 3;
          }
          .open-in-editor:hover { 
              background: rgba(13,110,253,0.18); 
              color: var(--fg); /* Maintient la couleur au survol */
          }
          .open-in-editor svg { 
              width: 14px; height: 14px; opacity: 0.9; 
              color: inherit; /* L'icône hérite de la couleur du texte */
          }
          .issue-line { font-weight: bold; color: var(--warning); margin: 0; order: 1; }
          .issue-description { margin-bottom: 12px; color: var(--fg); }
          
          /* Style pour les lignes enregistrées (état persistant) */
          .issue-item.saved {
            border-left: 4px solid #51cf66;
            background: rgba(81, 207, 102, 0.08);
          }
          
          .issue-item.saved .edit-interface {
            background: rgba(81, 207, 102, 0.12) !important;
            border-color: rgba(81, 207, 102, 0.5) !important;
          }
          
          .saved-badge {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 4px 10px;
            background: #51cf66;
            color: white;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-left: 10px;
            margin-right: auto;
            order: 2;
          }
          
          .content-comparison {
            display: grid; grid-template-columns: 1fr 1fr; gap: 15px;
            margin-top: 10px;
          }
          
          .content-block {
            background: rgba(0,0,0,0.2); border-radius: 6px; padding: 12px;
            font-family: 'Consolas', 'Monaco', monospace; font-size: 0.9rem;
          }
          
          .old-content { 
            border-left: 4px solid #ff6b6b;
            background: rgba(255, 107, 107, 0.1);
          }
          .new-content { 
            border-left: 4px solid #51cf66;
            background: rgba(81, 207, 102, 0.1);
          }
          
          .content-label {
            font-size: 0.8rem; font-weight: bold; opacity: 0.8;
            margin-bottom: 6px; text-transform: uppercase;
          }
          
          .filters {
            padding: 15px 20px; background: var(--hdr); 
            border: 1px solid var(--sep); border-radius: 12px;
            display: flex; gap: 15px; align-items: center; flex-wrap: wrap;
            position: sticky; top: var(--header-height, 120px); z-index: 900;
            margin: 0 20px 20px 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
          }
          
          .filter-group { display: flex; gap: 8px; align-items: center; }
          .filter-group label { font-size: 0.9rem; font-weight: 500; }
          
          select, input {
            background: var(--bg); color: var(--fg); border: 1px solid var(--sep);
            padding: 6px 10px; border-radius: 6px; outline: none; transition: border-color 0.2s;
          }
          select:focus, input:focus { border-color: var(--info); }
          
          .collapsible-toggle {
            font-size: 1rem;
            display: inline-block;
            width: 20px;
            transition: transform 0.2s ease;
            cursor: pointer;
            user-select: none;
          }
          
          .stats-overview {
            display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px;
          }
          
          .mini-stat {
            padding: 4px 8px; background: rgba(255,255,255,0.1);
            border-radius: 4px; font-size: 0.8rem;
          }
          
          @media (max-width: 768px) {
            .summary-cards { grid-template-columns: 1fr; }
            .header-meta { flex-direction: column; align-items: flex-start; }
            .controls { margin-left: 0; }
            .content-comparison { grid-template-columns: 1fr; }
          }
          
          .no-issues {
            text-align: center; padding: 60px 20px; opacity: 0.7;
          }
          .no-issues h2 { color: var(--success); margin-bottom: 15px; }
          
          .info-banner {
            background: rgba(74, 144, 226, 0.15);
            border-left: 4px solid var(--info);
            padding: 12px 15px;
            margin: 10px 0;
            border-radius: 6px;
            font-size: 0.9rem;
          }
          .info-banner strong { color: var(--info); }
        </style>
        """
    
    def _get_javascript_harmonized(self, selection_info: Dict[str, Any]) -> str:
        """JavaScript harmonisé SANS recherche textuelle + avec bouton reset"""
        
        # Préparer les données de sélection pour JavaScript
        is_all_files = selection_info.get('is_all_files', True)
        language = selection_info.get('language', '')
        selected_file = selection_info.get('selected_option', '')
        total_files = len(selection_info.get('target_files', []))
        project_path = selection_info.get('project_path', '').replace('\\', '\\\\')  # 🆕 Échapper les backslashes
        
        # Obtenir l'hôte et le port du serveur depuis la config
        from infrastructure.config.config import config_manager
        from infrastructure.logging.logging import log_message
        server_host = config_manager.get('editor_server_host', '127.0.0.1')
        server_port = config_manager.get('editor_server_port', 8765)
        server_url = f"http://{server_host}:{server_port}"
        log_message("DEBUG", f"🎯 Génération JavaScript rapport : server_url={server_url}", category="report")
        
        return f"""
        <script>
        (function() {{
            // URL du serveur d'édition (configurable pour support WSL)
            window.RENEXTRACT_SERVER_URL = '{server_url}';
            
            // Informations sur la sélection harmonisée
            window.coherenceSelectionInfo = {{
                isAllFiles: {str(is_all_files).lower()},
                language: '{language}',
                selectedFile: '{selected_file}',
                totalFiles: {total_files},
                project_path: '{project_path}'  // 🆕
            }};
            
            // 🆕 Calculer dynamiquement la hauteur du header au chargement
            function updateHeaderHeight() {{
                const header = document.querySelector('.header');
                if (header) {{
                    const headerHeight = header.offsetHeight;
                    document.documentElement.style.setProperty('--header-height', headerHeight + 'px');
                }}
            }}
            
            // Mettre à jour au chargement et au redimensionnement
            window.addEventListener('load', updateHeaderHeight);
            window.addEventListener('resize', updateHeaderHeight);
            
            // Gestion du thème
            const savedTheme = localStorage.getItem('renextract_coherence_theme') || 'dark';
            if (savedTheme === 'light') document.body.classList.add('light');

            function toggleTheme() {{
                const isLight = document.body.classList.toggle('light');
                localStorage.setItem('renextract_coherence_theme', isLight ? 'light' : 'dark');
                const themeBtn = document.getElementById('themeBtn');
                if (themeBtn) {{
                    themeBtn.textContent = 'Thème: ' + (isLight ? 'Clair' : 'Sombre');
                }}
            }}

            // Fonction pour ouvrir dans l'éditeur
            window.openInEditor = function(filePath, lineNumber) {{
                const url = `${{window.RENEXTRACT_SERVER_URL}}/open?file=${{encodeURIComponent(filePath)}}&line=${{encodeURIComponent(lineNumber)}}`;

                fetch(url, {{ method: 'GET' }})
                    .then(async (res) => {{
                        if (!res.ok) throw new Error('HTTP ' + res.status);
                        const data = await res.json().catch(() => ({{}}));
                        const msg = data && (data.message || (data.ok ? "Ouvert dans l'éditeur." : 'Requête envoyée.'));
                        if (msg) {{
                            console.log(msg);
                        }} else {{
                            console.log('Ouverture demandée au gestionnaire local.');
                        }}
                    }})
                    .catch(() => {{
                        const textToCopy = `${{filePath}}:${{lineNumber}}`;
                        if (navigator.clipboard && navigator.clipboard.writeText) {{
                            navigator.clipboard.writeText(textToCopy).then(() => {{
                                alert(`Le serveur local n'est pas joignable.\\nJ'ai copié: ${{textToCopy}}\\nOuvre ton éditeur et fais "Go to Line".\\n• VSCode: Ctrl+G\\n• Notepad++: Ctrl+G\\n• Sublime: Ctrl+G`);
                            }}).catch(() => {{
                                prompt('Copiez ce chemin manuellement:', textToCopy);
                            }});
                        }} else {{
                            prompt('Copiez ce chemin manuellement:', textToCopy);
                        }}
                    }});
            }};
            
            // ===== NOUVEAU : Gestion des exclusions =====
            window.exclusionsCache = new Set();
            
            // Charger les exclusions existantes depuis le serveur
            async function loadExclusions() {{
                try {{
                    const project = window.coherenceSelectionInfo.project_path;
                    const response = await fetch(`${{window.RENEXTRACT_SERVER_URL}}/api/coherence/exclusions?project=${{encodeURIComponent(project)}}`);
                    if (response.ok) {{
                        const data = await response.json();
                        if (data.ok && Array.isArray(data.exclusions)) {{
                            // Créer les clés pour le cache (project|file|line|text)
                            window.exclusionsCache = new Set(
                                data.exclusions.map(excl => `${{project}}|${{excl.file}}|${{excl.line}}|${{excl.text}}`)
                            );
                            console.log(`✅ ${{data.exclusions.length}} exclusion(s) chargée(s) pour ce projet`);
                            updateCheckboxStates();
                            // Masquer l'avertissement si présent
                            const warningBanner = document.getElementById('server-warning-banner');
                            if (warningBanner) warningBanner.style.display = 'none';
                            return true;
                        }}
                    }}
                    return false;
                }} catch (error) {{
                    console.log('⚠️ Impossible de charger les exclusions (serveur non accessible)');
                    showServerWarning();
                    return false;
                }}
            }}
            
            // Afficher un avertissement si RenExtract n'est pas ouvert
            function showServerWarning() {{
                let warningBanner = document.getElementById('server-warning-banner');
                if (!warningBanner) {{
                    warningBanner = document.createElement('div');
                    warningBanner.id = 'server-warning-banner';
                    warningBanner.style.cssText = `
                        background: rgba(237, 137, 54, 0.2);
                        border-left: 4px solid #ed8936;
                        padding: 12px 15px;
                        margin: 10px 0;
                        border-radius: 6px;
                        font-size: 0.9rem;
                    `;
                    warningBanner.innerHTML = `
                        <strong style="color: #ed8936;">⚠️ Fonctionnalité d'exclusion inactive</strong>
                        <br>
                        <em>RenExtract doit être ouvert pour ignorer des lignes. Relancez l'application puis rechargez ce rapport.</em>
                    `;
                    
                    // Insérer après le titre du rapport
                    const header = document.querySelector('.header');
                    if (header && header.nextSibling) {{
                        header.parentNode.insertBefore(warningBanner, header.nextSibling);
                    }} else {{
                        document.body.insertBefore(warningBanner, document.body.firstChild);
                    }}
                }}
            }}
            
            // Afficher un message global dans le header
            function showGlobalMessage(message, type = 'info', duration = 3000) {{
                const msgDiv = document.getElementById('globalMessage');
                if (!msgDiv) return;
                
                // Définir le style selon le type
                let bgColor, borderColor;
                if (type === 'success') {{
                    bgColor = 'rgba(40, 167, 69, 0.15)';
                    borderColor = '#28a745';
                }} else if (type === 'error') {{
                    bgColor = 'rgba(220, 53, 69, 0.15)';
                    borderColor = '#dc3545';
                }} else if (type === 'warning') {{
                    bgColor = 'rgba(255, 193, 7, 0.15)';
                    borderColor = '#ffc107';
                }} else {{
                    bgColor = 'rgba(13, 110, 253, 0.15)';
                    borderColor = '#0d6efd';
                }}
                
                msgDiv.style.background = bgColor;
                msgDiv.style.borderLeft = `4px solid ${{borderColor}}`;
                msgDiv.textContent = message;
                msgDiv.style.display = 'block';
                
                // Auto-masquer après durée spécifiée
                if (duration > 0) {{
                    setTimeout(() => {{
                        msgDiv.style.display = 'none';
                    }}, duration);
                }}
            }}
            
            // Mettre à jour l'état des checkboxes selon les exclusions
            function updateCheckboxStates() {{
                const project = window.coherenceSelectionInfo.project_path;
                
                document.querySelectorAll('.exclude-checkbox').forEach(checkbox => {{
                    const text = checkbox.getAttribute('data-exclusion-text');
                    const file = checkbox.getAttribute('data-exclusion-file');
                    const line = parseInt(checkbox.getAttribute('data-exclusion-line'));
                    
                    // Construire la clé complète
                    const cacheKey = `${{project}}|${{file}}|${{line}}|${{text}}`;
                    const isExcluded = window.exclusionsCache.has(cacheKey);
                    
                    checkbox.checked = isExcluded;
                    
                    // Marquer visuellement la ligne comme exclue
                    const issueItem = checkbox.closest('.issue-item');
                    const statusSpan = checkbox.closest('.exclude-checkbox-container').querySelector('.exclusion-status');
                    
                    if (isExcluded) {{
                        issueItem.classList.add('excluded');
                        statusSpan.textContent = '✓ Ignoré';
                    }} else {{
                        issueItem.classList.remove('excluded');
                        statusSpan.textContent = '';
                    }}
                }});
            }}
            
            // Ajouter une exclusion
            async function addExclusion(text, file, line, project) {{
                console.log('📤 POST /exclude:', {{ text: text.substring(0, 50), file, line, project: project.substring(0, 50) }});
                try {{
                    const response = await fetch(`${{window.RENEXTRACT_SERVER_URL}}/api/coherence/exclude`, {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ text, file, line, project }})  // 🆕 Envoyer toutes les données
                    }});
                    
                    if (response.ok) {{
                        const data = await response.json();
                        if (data.ok) {{
                            // Stocker la clé complète dans le cache
                            const cacheKey = `${{project}}|${{file}}|${{line}}|${{text}}`;
                            window.exclusionsCache.add(cacheKey);
                            console.log('✅ Exclusion ajoutée:', file, 'ligne', line);
                            return true;
                        }}
                    }}
                    return false;
                }} catch (error) {{
                    console.error('❌ Erreur ajout exclusion:', error);
                    showServerWarning();
                    alert('⚠️ RenExtract doit être ouvert pour enregistrer les exclusions');
                    return false;
                }}
            }}
            
            // Retirer une exclusion
            async function removeExclusion(text, file, line, project) {{
                try {{
                    const response = await fetch(`${{window.RENEXTRACT_SERVER_URL}}/api/coherence/exclude`, {{
                        method: 'DELETE',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ text, file, line, project }})  // 🆕 Envoyer toutes les données
                    }});
                    
                    if (response.ok) {{
                        const data = await response.json();
                        if (data.ok) {{
                            // Retirer la clé complète du cache
                            const cacheKey = `${{project}}|${{file}}|${{line}}|${{text}}`;
                            window.exclusionsCache.delete(cacheKey);
                            console.log('🗑️ Exclusion retirée:', file, 'ligne', line);
                            return true;
                        }}
                    }}
                    return false;
                }} catch (error) {{
                    console.error('❌ Erreur suppression exclusion:', error);
                    alert('⚠️ RenExtract doit être ouvert pour modifier les exclusions');
                    return false;
                }}
            }}
            
            // Handler pour les checkboxes
            async function handleExcludeCheckbox(checkbox) {{
                const text = checkbox.getAttribute('data-exclusion-text');
                const file = checkbox.getAttribute('data-exclusion-file');  // 🆕
                const line = parseInt(checkbox.getAttribute('data-exclusion-line'));  // 🆕
                const project = window.coherenceSelectionInfo.project_path;  // 🆕
                
                // 🆕 Validation des données avant envoi
                if (!text || !file || !line || !project) {{
                    console.error('❌ Données manquantes:', {{ text: !!text, file: !!file, line: !!line, project: !!project }});
                    alert("⚠️ Erreur: données incomplètes pour l\'exclusion");
                    checkbox.checked = false;
                    return;
                }}
                
                const issueItem = checkbox.closest('.issue-item');
                const statusSpan = checkbox.closest('.exclude-checkbox-container').querySelector('.exclusion-status');
                
                if (checkbox.checked) {{
                    // Ajouter l'exclusion
                    const success = await addExclusion(text, file, line, project);
                    if (success) {{
                        issueItem.classList.add('excluded');
                        statusSpan.textContent = '✓ Ignoré';
                    }} else {{
                        checkbox.checked = false;
                    }}
                }} else {{
                    // Retirer l'exclusion
                    const success = await removeExclusion(text, file, line, project);
                    if (success) {{
                        issueItem.classList.remove('excluded');
                        statusSpan.textContent = '';
                    }} else {{
                        checkbox.checked = true;
                    }}
                }}
            }}
            
            // Fonction pour mettre à jour l'affichage de sélection harmonisé
            function updateSelectionDisplay() {{
                const selectionInfo = window.coherenceSelectionInfo;
                const filterInfo = document.getElementById('filterInfo');
                
                if (filterInfo) {{
                    let displayText = '';
                    if (selectionInfo.isAllFiles) {{
                        displayText = `${{selectionInfo.language}} (${{selectionInfo.totalFiles}} fichiers)`;
                    }} else {{
                        displayText = selectionInfo.selectedFile;
                    }}
                    // Le compteur sera ajouté par updateVisibleStats
                    filterInfo.textContent = displayText;
                }}
            }}

            // ===== NOUVEAU : Gestion de la traduction en ligne =====
            async function translateText(editFieldId) {{
                try {{
                    const editField = document.getElementById(editFieldId);
                    if (!editField) return;
                    
                    const text = editField.value.trim();
                    if (!text) {{
                        showGlobalMessage('⚠️ Veuillez entrer un texte à traduire', 'warning', 3000);
                        return;
                    }}
                    
                    const translator = document.getElementById('translatorSelect').value;
                    const project = window.coherenceSelectionInfo.project_path;
                    
                    // Afficher un indicateur de chargement
                    const translateBtn = document.querySelector(`[data-edit-field="${{editFieldId}}"]`);
                    if (translateBtn) {{
                        translateBtn.disabled = true;
                        translateBtn.textContent = '⏳ Traduction...';
                    }}
                    
                    const response = await fetch(`${{window.RENEXTRACT_SERVER_URL}}/api/coherence/translate`, {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ text, translator, target_lang: 'fr' }})
                    }});
                    
                    if (response.ok) {{
                        const data = await response.json();
                        if (data.ok && data.translation) {{
                            // Insérer la traduction dans le champ
                            editField.value = data.translation;
                            showGlobalMessage(`✅ Traduction réussie avec ${{data.service}}`, 'success', 3000);
                            console.log(`✅ Traduction réussie avec ${{data.service}}`);
                        }} else if (data.url) {{
                            // Ouvrir l'URL du traducteur web
                            window.open(data.url, '_blank');
                            showGlobalMessage(`🌐 Traducteur ${{data.service}} ouvert dans un nouvel onglet`, 'info', 3000);
                            console.log(`🌐 Ouverture de ${{data.service}}`);
                        }} else {{
                            showGlobalMessage('❌ Traduction non disponible pour ce service', 'error', 4000);
                        }}
                    }} else {{
                        showGlobalMessage('❌ Erreur lors de la traduction', 'error', 4000);
                    }}
                    
                    // Restaurer le bouton
                    if (translateBtn) {{
                        translateBtn.disabled = false;
                        translateBtn.textContent = '🌐 Traduire';
                    }}
                    
                }} catch (error) {{
                    console.error('❌ Erreur traduction:', error);
                    showGlobalMessage('⚠️ RenExtract doit être ouvert pour utiliser la traduction', 'error', 5000);
                    
                    // Restaurer le bouton
                    const translateBtn = document.querySelector(`[data-edit-field="${{editFieldId}}"]`);
                    if (translateBtn) {{
                        translateBtn.disabled = false;
                        translateBtn.textContent = '🌐 Traduire';
                    }}
                }}
            }}
            
            // ===== NOUVEAU : Enregistrement d'une modification =====
            async function saveLine(file, line, newContent, statusId) {{
                try {{
                    const project = window.coherenceSelectionInfo.project_path;
                    
                    const response = await fetch(`${{window.RENEXTRACT_SERVER_URL}}/api/coherence/edit`, {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ file, line, new_content: newContent, project }})
                    }});
                    
                    if (response.ok) {{
                        const data = await response.json();
                        if (data.ok) {{
                            // 🆕 Marquer visuellement l'issue comme enregistrée (PERSISTANT)
                            const statusSpan = document.getElementById(statusId);
                            const issueItem = statusSpan ? statusSpan.closest('.issue-item') : null;
                            const issueHeader = issueItem ? issueItem.querySelector('.issue-header') : null;
                            
                            if (issueItem) {{
                                // Ajouter la classe "saved" pour le style persistant
                                issueItem.classList.add('saved');
                                
                                // Ajouter un badge "Enregistré" dans le header (si pas déjà présent)
                                if (issueHeader && !issueHeader.querySelector('.saved-badge')) {{
                                    const badge = document.createElement('span');
                                    badge.className = 'saved-badge';
                                    badge.innerHTML = '✅ Enregistré';
                                    issueHeader.appendChild(badge);
                                }}
                            }}
                            
                            // Afficher le statut de succès temporaire
                            if (statusSpan) {{
                                statusSpan.textContent = '✅ Enregistré';
                                statusSpan.style.display = 'inline';
                                
                                // Masquer après 3 secondes
                                setTimeout(() => {{
                                    statusSpan.style.display = 'none';
                                }}, 3000);
                            }}
                            
                            console.log(`✅ Ligne enregistrée: ${{file}}:${{line}}`);
                            return true;
                        }} else {{
                            alert(`Erreur: ${{data.error || "Échec de l\'enregistrement"}}`);
                            return false;
                        }}
                    }} else {{
                        alert("Erreur lors de l\'enregistrement");
                        return false;
                    }}
                    
                }} catch (error) {{
                    console.error('❌ Erreur enregistrement:', error);
                    alert('⚠️ RenExtract doit être ouvert pour enregistrer les modifications');
                    return false;
                }}
            }}
            
            // ===== NOUVEAU : Enregistrement global =====
            async function saveAll() {{
                try {{
                    const project = window.coherenceSelectionInfo.project_path;
                    
                    // Collecter toutes les modifications
                    const modifications = [];
                    document.querySelectorAll('.edit-field').forEach(field => {{
                        const file = field.getAttribute('data-file');
                        const line = parseInt(field.getAttribute('data-line'));
                        const new_content = field.value.trim();
                        
                        if (file && line && new_content) {{
                            modifications.push({{ file, line, new_content }});
                        }}
                    }});
                    
                    if (modifications.length === 0) {{
                        showGlobalMessage('⚠️ Aucune modification à enregistrer', 'warning', 3000);
                        return;
                    }}
                    
                    // Afficher un indicateur de chargement
                    const saveAllBtn = document.getElementById('saveAllBtn');
                    if (saveAllBtn) {{
                        saveAllBtn.disabled = true;
                        saveAllBtn.textContent = `⏳ Enregistrement (${{modifications.length}})...`;
                    }}
                    
                    const response = await fetch(`${{window.RENEXTRACT_SERVER_URL}}/api/coherence/save_all`, {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ modifications, project }})
                    }});
                    
                    if (response.ok) {{
                        const data = await response.json();
                        if (data.ok) {{
                            const message = `✅ Enregistrement terminé : ${{data.success_count}} succès, ${{data.failed_count}} échec(s)`;
                            showGlobalMessage(message, 'success', 5000);
                            console.log(`✅ Enregistrement global: ${{data.success_count}} succès, ${{data.failed_count}} échecs`);
                            
                            // 🆕 Marquer visuellement TOUTES les lignes comme enregistrées (PERSISTANT)
                            document.querySelectorAll('.edit-field').forEach(field => {{
                                const issueItem = field.closest('.issue-item');
                                const issueHeader = issueItem ? issueItem.querySelector('.issue-header') : null;
                                
                                if (issueItem) {{
                                    // Ajouter la classe "saved" pour le style persistant
                                    issueItem.classList.add('saved');
                                    
                                    // Ajouter un badge "Enregistré" dans le header (si pas déjà présent)
                                    if (issueHeader && !issueHeader.querySelector('.saved-badge')) {{
                                        const badge = document.createElement('span');
                                        badge.className = 'saved-badge';
                                        badge.innerHTML = '✅ Enregistré';
                                        issueHeader.appendChild(badge);
                                    }}
                                }}
                                
                                // Statut temporaire
                                const statusId = issueItem ? issueItem.querySelector('.exclusion-status')?.id : null;
                                if (statusId) {{
                                    const statusSpan = document.getElementById(statusId);
                                    if (statusSpan) {{
                                        statusSpan.textContent = '✅ Enregistré';
                                        statusSpan.style.display = 'inline';
                                        
                                        // Masquer après 3 secondes
                                        setTimeout(() => {{
                                            statusSpan.style.display = 'none';
                                        }}, 3000);
                                    }}
                                }}
                            }});
                        }} else {{
                            showGlobalMessage("❌ Erreur lors de l'enregistrement global", 'error', 5000);
                        }}
                    }} else {{
                        showGlobalMessage("❌ Erreur lors de l'enregistrement global", 'error', 5000);
                    }}
                    
                    // Restaurer le bouton
                    if (saveAllBtn) {{
                        saveAllBtn.disabled = false;
                        saveAllBtn.textContent = '💾 Enregistrer tout';
                    }}
                    
                }} catch (error) {{
                    console.error('❌ Erreur enregistrement global:', error);
                    showGlobalMessage('⚠️ RenExtract doit être ouvert pour enregistrer les modifications', 'error', 5000);
                    
                    // Restaurer le bouton
                    const saveAllBtn = document.getElementById('saveAllBtn');
                    if (saveAllBtn) {{
                        saveAllBtn.disabled = false;
                        saveAllBtn.textContent = '💾 Enregistrer tout';
                    }}
                }}
            }}
            
            // Initialisation
            document.addEventListener('DOMContentLoaded', function() {{
                // Charger les exclusions existantes
                loadExclusions();
                
                // Délégation: clic sur boutons "open in editor"
                document.body.addEventListener('click', function(e) {{
                    const btn = e.target.closest('.open-in-editor');
                    if (!btn) return;
                    const f = btn.getAttribute('data-file');
                    const l = parseInt(btn.getAttribute('data-line') || '0', 10) || 0;
                    if (f && l) window.openInEditor(f, l);
                }});
                
                // Délégation: changement sur checkboxes d'exclusion
                document.body.addEventListener('change', function(e) {{
                    if (e.target.classList.contains('exclude-checkbox')) {{
                        handleExcludeCheckbox(e.target);
                    }}
                }});
                
                // Délégation: clic sur boutons "Traduire"
                document.body.addEventListener('click', function(e) {{
                    if (e.target.classList.contains('translate-btn')) {{
                        const editFieldId = e.target.getAttribute('data-edit-field');
                        if (editFieldId) translateText(editFieldId);
                    }}
                }});
                
                // Délégation: clic sur boutons "Enregistrer"
                document.body.addEventListener('click', function(e) {{
                    if (e.target.classList.contains('save-btn')) {{
                        const editFieldId = e.target.getAttribute('data-edit-field');
                        const file = e.target.getAttribute('data-file');
                        const line = parseInt(e.target.getAttribute('data-line'));
                        const statusId = e.target.getAttribute('data-status');
                        
                        if (editFieldId && file && line) {{
                            const editField = document.getElementById(editFieldId);
                            if (editField) {{
                                saveLine(file, line, editField.value.trim(), statusId);
                            }}
                        }}
                    }}
                }});
                
                // Bouton "Enregistrer tout"
                const saveAllBtn = document.getElementById('saveAllBtn');
                if (saveAllBtn) {{
                    saveAllBtn.addEventListener('click', saveAll);
                }}

                // Bouton thème
                const themeBtn = document.getElementById('themeBtn');
                if (themeBtn) {{
                    themeBtn.textContent = 'Thème: ' + (savedTheme === 'light' ? 'Clair' : 'Sombre');
                    themeBtn.addEventListener('click', toggleTheme);
                }}

                // Fonction pour basculer les sections (inspirée du tutoriel)
                window.toggleSection = function(id) {{
                    const content = document.getElementById('content_' + id);
                    const icon = document.getElementById('icon_' + id);
                    const header = document.querySelector('[onclick*="' + id + '"]');
                    if (!content || !icon) return;
                    
                    const isHidden = content.style.display === 'none' || content.style.display === '';
                    if (isHidden) {{
                        content.style.display = 'block';
                        icon.textContent = '▼';
                        if (header) header.setAttribute('aria-expanded', 'true');
                    }} else {{
                        content.style.display = 'none';
                        icon.textContent = '▶';
                        if (header) header.setAttribute('aria-expanded', 'false');
                    }}
                }};

                // Filtres harmonisés
                const errorTypeFilter = document.getElementById('errorTypeFilter');
                const fileFilter = document.getElementById('fileFilter');
                const resetBtn = document.getElementById('resetFilters');

                function applyFilters() {{
                    const selectedErrorType = errorTypeFilter ? errorTypeFilter.value : 'all';
                    const selectedFile = fileFilter ? fileFilter.value : 'all';

                    let visibleSections = 0;
                    let totalVisibleIssues = 0;

                    document.querySelectorAll('.error-type-section').forEach(section => {{
                        const errorType = section.dataset.errorType;
                        let showSection = selectedErrorType === 'all' || errorType === selectedErrorType;

                        if (showSection) {{
                            // Compter et filtrer les fichiers dans cette section
                            const fileItems = section.querySelectorAll('[data-file]');
                            let visibleFilesInSection = 0;
                            let issuesInSection = 0;

                            fileItems.forEach(fileItem => {{
                                const fileName = fileItem.getAttribute('data-file');
                                const fileMatches = selectedFile === 'all' || fileName === selectedFile;
                                
                                if (fileMatches) {{
                                    fileItem.style.display = 'block';
                                    visibleFilesInSection++;
                                    // Compter les issues dans ce fichier
                                    const issues = fileItem.querySelectorAll('.issue-item');
                                    issuesInSection += issues.length;
                                }} else {{
                                    fileItem.style.display = 'none';
                                }}
                            }});

                            // Si aucun fichier correspondant dans cette section
                            showSection = visibleFilesInSection > 0;
                            if (showSection) {{
                                totalVisibleIssues += issuesInSection;
                            }}
                        }}

                        section.style.display = showSection ? 'block' : 'none';
                        if (showSection) visibleSections++;
                    }});

                    updateVisibleStats(visibleSections, totalVisibleIssues);
                }}

                function updateVisibleStats(sections, issues) {{
                    const filterInfo = document.getElementById('filterInfo');
                    if (filterInfo) {{
                        const selectionInfo = window.coherenceSelectionInfo;
                        let baseText = '';
                        if (selectionInfo.isAllFiles) {{
                            baseText = `${{selectionInfo.language}} (${{selectionInfo.totalFiles}} fichiers)`;
                        }} else {{
                            baseText = selectionInfo.selectedFile;
                        }}
                        filterInfo.textContent = `${{baseText}} - ${{issues}} erreur(s) visible(s)`;
                    }}
                }}

                // Fonction de réinitialisation des filtres (doit être après applyFilters)
                function resetAllFilters() {{
                    if (errorTypeFilter) errorTypeFilter.value = 'all';
                    if (fileFilter) fileFilter.value = 'all';
                    
                    // Réappliquer les filtres pour tout afficher
                    applyFilters();
                    
                    // Refermer toutes les sections collapsibles
                    document.querySelectorAll('.error-type-content').forEach(content => {{
                        if (content.id && content.id.startsWith('content_')) {{
                            const id = content.id.replace('content_', '');
                            const icon = document.getElementById('icon_' + id);
                            const header = document.querySelector('[onclick*="' + id + '"]');
                            content.style.display = 'none';
                            if (icon) icon.textContent = '▶';
                            if (header) header.setAttribute('aria-expanded', 'false');
                        }}
                    }});
                }}

                if (errorTypeFilter) errorTypeFilter.addEventListener('change', applyFilters);
                if (fileFilter) fileFilter.addEventListener('change', applyFilters);
                if (resetBtn) resetBtn.addEventListener('click', resetAllFilters);

                // Tout déplier / Tout replier
                const expandAllBtn = document.getElementById('expandAll');
                if (expandAllBtn) {{
                    expandAllBtn.addEventListener('click', function() {{
                        document.querySelectorAll('.error-type-content').forEach(content => {{
                            if (content.id && content.id.startsWith('content_')) {{
                                const id = content.id.replace('content_', '');
                                const icon = document.getElementById('icon_' + id);
                                const header = document.querySelector('[onclick*="' + id + '"]');
                                content.style.display = 'block';
                                if (icon) icon.textContent = '▼';
                                if (header) header.setAttribute('aria-expanded', 'true');
                            }}
                        }});
                    }});
                }}

                const collapseAllBtn = document.getElementById('collapseAll');
                if (collapseAllBtn) {{
                    collapseAllBtn.addEventListener('click', function() {{
                        document.querySelectorAll('.error-type-content').forEach(content => {{
                            if (content.id && content.id.startsWith('content_')) {{
                                const id = content.id.replace('content_', '');
                                const icon = document.getElementById('icon_' + id);
                                const header = document.querySelector('[onclick*="' + id + '"]');
                                content.style.display = 'none';
                                if (icon) icon.textContent = '▶';
                                if (header) header.setAttribute('aria-expanded', 'false');
                            }}
                        }});
                    }});
                }}

                // Mise à jour initiale des stats et sélection
                updateSelectionDisplay();
                applyFilters();
            }});
        }})();
        </script>
        """
    
    def generate_coherence_report(self, results: Dict[str, Any], project_path: str, 
                                execution_time: str) -> Optional[str]:
        """Génère un rapport HTML interactif pour la cohérence"""
        try:
            # Nom du jeu et timestamp
            game_name = extract_game_name(project_path) if project_path else "Unknown"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # NOUVEAU : Créer la structure hiérarchique complète
            report_type_folder = os.path.join(self.report_dir, game_name, "coherence")
            os.makedirs(report_type_folder, exist_ok=True)
            
            # Chemin du rapport dans la bonne structure
            report_name = f"{game_name}_coherence_interactif_{timestamp}.html"
            report_path = os.path.join(report_type_folder, report_name)
            
            # Vérifier s'il y a des erreurs
            stats = results.get('stats', {})
            total_issues = stats.get('total_issues', 0)
            
            if total_issues == 0:
                return None
            
            with open(report_path, 'w', encoding='utf-8') as f:
                # En-tête HTML
                f.write(self._generate_html_header(game_name, results, execution_time))
                
                # Contenu principal
                f.write(self._generate_summary_section(results))
                f.write(self._generate_filters_section(results))
                f.write(self._generate_error_type_sections(results))
                
                # Pied de page
                f.write(self._generate_footer())
                
                # Toujours utiliser le JS harmonisé (avec dictionnaire par défaut si besoin)
                selection_info = results.get('selection_info', {
                    'project_path': project_path,
                    'language': 'unknown',
                    'is_all_files': True
                })
                f.write(self._get_javascript_harmonized(selection_info))

                f.write("</body></html>")
            
            return report_path
            
        except Exception as e:
            # Utiliser le logger pour une meilleure trace
            from infrastructure.logging.logging import log_message
            log_message("ERREUR", f"Erreur génération rapport HTML cohérence: {e}", "report_generator")
            return None



    def _generate_html_header(self, game_name: str, results: Dict[str, Any], 
                            execution_time: str) -> str:
        """Génère l'en-tête HTML du rapport"""
        title = f"Rapport de Cohérence - {game_name}"
        current_time = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")
        
        stats = results.get('stats', {})
        files_analyzed = stats.get('files_analyzed', 0)
        total_issues = stats.get('total_issues', 0)
        
        return f"""<!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{_html.escape(title)}</title>
            {self._get_css_styles()}
        </head>
        <body>
            <div class="header">
                <h1>🔍 Rapport de Cohérence RenExtract</h1>
                <div class="header-meta">
                    <span>🎮 <strong>{_html.escape(game_name)}</strong></span>
                    <span>📅 {current_time}</span>
                    <span>⏱️ Temps: {_html.escape(execution_time)}</span>
                    <span>📄 Fichiers: {files_analyzed}</span>
                    <span>⚠️ Erreurs: {total_issues}</span>
                    
                    <div class="controls">
                        <label for="translatorSelect" style="margin-right: 5px; font-size: 0.9rem;">Traducteur:</label>
                        <select id="translatorSelect" class="btn" style="margin-right: 15px; padding: 6px 10px;">
                            <option value="Google">Google</option>
                            <option value="DeepL">DeepL</option>
                            <option value="Groq AI">Groq AI</option>
                            <option value="Microsoft">Microsoft</option>
                            <option value="Yandex">Yandex</option>
                        </select>
                        <button id="saveAllBtn" class="btn btn-primary" style="margin-right: 15px;">💾 Enregistrer tout</button>
                        <button id="expandAll" class="btn">Tout déplier</button>
                        <button id="collapseAll" class="btn">Tout replier</button>
                        <button id="themeBtn" class="btn">Thème: Sombre</button>
                    </div>
                </div>
                <div style="background: rgba(255, 193, 7, 0.15); border-left: 4px solid #ffc107; padding: 8px 15px; margin-top: 10px; border-radius: 4px; font-size: 0.85rem;">
                    <em>⚠️ Note : RenExtract doit rester ouvert pour que les modifications soient enregistrées.</em>
                </div>
                <div id="globalMessage" style="display: none; padding: 8px 15px; margin-top: 10px; border-radius: 4px; font-size: 0.9rem; font-weight: 600;"></div>
            </div>
        """
    
    def _generate_summary_section(self, results: Dict[str, Any]) -> str:
        """Génère la section de résumé des erreurs par type"""
        stats = results.get('stats', {})
        issues_by_type = stats.get('issues_by_type', {})
        total_issues = stats.get('total_issues', 0)
        files_analyzed = stats.get('files_analyzed', 0)
        
        # Calculer les statistiques par type
        type_stats = []
        for error_type, count in issues_by_type.items():
            if count > 0:
                percentage = (count / total_issues * 100) if total_issues > 0 else 0
                type_name = self._get_error_type_display_name(error_type)
                type_stats.append({
                    'type': error_type,
                    'name': type_name,
                    'count': count,
                    'percentage': percentage
                })
        
        # Trier par nombre d'erreurs (décroissant)
        type_stats.sort(key=lambda x: x['count'], reverse=True)
        
        # Bannière d'information pour les exclusions et édition interactives
        info_banner = """
        <div class="info-banner">
            💡 <strong>Nouvelles fonctionnalités :</strong>
            <ul style="margin: 5px 0; padding-left: 20px;">
                <li><strong>Édition en ligne :</strong> Modifiez les traductions directement depuis ce rapport ! Corrigez le texte et cliquez sur "Enregistrer".</li>
                <li><strong>Traduction assistée :</strong> Utilisez le bouton "Traduire" pour obtenir une suggestion de traduction automatique.</li>
                <li><strong>Exclusions :</strong> Cochez "✓ Ignoré" pour exclure une ligne des prochaines analyses.</li>
            </ul>
        </div>
        """
        
        html = info_banner + """
        <div class="summary-cards">
            <div class="card">
                <h3>📊 Résumé Global</h3>
                <div class="stat">
                    <span>Fichiers analysés</span>
                    <span class="stat-value">{}</span>
                </div>
                <div class="stat">
                    <span>Total des erreurs</span>
                    <span class="stat-value">{}</span>
                </div>
            </div>
        """.format(files_analyzed, total_issues)
        
        # Cartes par type d'erreur (maximum 4 cartes supplémentaires)
        for i, stat in enumerate(type_stats[:4]):
            css_class = self._get_error_type_css_class(stat['type'])
            html += f"""
            <div class="card">
                <h3>{stat['name']}</h3>
                <div class="stat">
                    <span>Erreurs détectées</span>
                    <span class="stat-value">{stat['count']}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {stat['percentage']:.1f}%"></div>
                </div>
                <small>{stat['percentage']:.1f}% du total</small>
            </div>
            """
        
        html += "</div>"
        return html
    
    def _generate_filters_section(self, results: Dict[str, Any]) -> str:
        """Génère la section des filtres harmonisée - SANS champ de recherche + bouton reset"""
        stats = results.get('stats', {})
        issues_by_type = stats.get('issues_by_type', {})
        results_by_file = results.get('results_by_file', {})
        
        # Options de filtre par type d'erreur
        error_type_options = ''
        for error_type, count in issues_by_type.items():
            if count > 0:
                type_name = self._get_error_type_display_name(error_type)
                error_type_options += f'<option value="{error_type}">{type_name} ({count})</option>'
        
        # Options de filtre par fichier
        file_options = ''
        for file_path in results_by_file.keys():
            file_name = os.path.basename(file_path)
            file_options += f'<option value="{file_name}">{file_name}</option>'
        
        return f"""
        <div class="filters">
            <div class="filter-group">
                <label for="errorTypeFilter">Type d'erreur :</label>
                <select id="errorTypeFilter">
                    <option value="all">Tous les types</option>
                    {error_type_options}
                </select>
            </div>
            
            <div class="filter-group">
                <label for="fileFilter">Fichier :</label>
                <select id="fileFilter">
                    <option value="all">Tous les fichiers</option>
                    {file_options}
                </select>
            </div>
            
            <button id="resetFilters" class="reset-filters-btn">🔄 Réinitialiser</button>
            
            <div class="filter-group" style="margin-left: auto;">
                <span id="filterInfo" style="font-style: italic; opacity: 0.8;"></span>
            </div>
        </div>
        """
    
    def _generate_error_type_sections(self, results: Dict[str, Any]) -> str:
        """Génère les sections détaillées par type d'erreur"""
        stats = results.get('stats', {})
        issues_by_type = stats.get('issues_by_type', {})
        results_by_file = results.get('results_by_file', {})
        
        # Organiser les erreurs par type
        errors_by_type = {}
        for file_path, file_results in results_by_file.items():
            for issue in file_results.get('issues', []):
                error_type = issue['type']
                if error_type not in errors_by_type:
                    errors_by_type[error_type] = []
                
                # Ajouter le nom du fichier à l'issue
                issue_with_file = issue.copy()
                issue_with_file['file_path'] = file_path
                errors_by_type[error_type].append(issue_with_file)
        
        # Ordre de priorité pour l'affichage
        priority_order = [
            'VARIABLE_MISMATCH', 'TAG_MISMATCH', 'PLACEHOLDER_MISMATCH',
            'UNRESTORED_PLACEHOLDER', 'MALFORMED_PLACEHOLDER', 'SPECIAL_CODE_MISMATCH',
            'PARENTHESES_MISMATCH', 'FRENCH_QUOTES_MISMATCH', 'QUOTE_COUNT_MISMATCH',
            'UNTRANSLATED_LINE', 'MISSING_OLD', 'CONTENT_PREFIX_MISMATCH', 
            'CONTENT_SUFFIX_MISMATCH', 'FILE_ERROR', 'ANALYSIS_ERROR'
        ]
        
        # Trier les types d'erreurs
        sorted_error_types = sorted(errors_by_type.keys(), 
                                  key=lambda t: priority_order.index(t) if t in priority_order else len(priority_order))
        
        html = ""
        for error_type in sorted_error_types:
            issues = errors_by_type[error_type]
            if not issues:
                continue
                
            html += self._generate_error_type_section(error_type, issues)
        
        return html
    
    def _generate_error_type_section(self, error_type: str, issues: List[Dict]) -> str:
        """Génère une section pour un type d'erreur spécifique"""
        type_name = self._get_error_type_display_name(error_type)
        type_icon = self._get_error_type_icon(error_type)
        css_class = self._get_error_type_css_class(error_type)
        
        # Grouper par fichier
        issues_by_file = {}
        for issue in issues:
            file_path = issue.get('file_path', 'unknown')
            if file_path not in issues_by_file:
                issues_by_file[file_path] = []
            issues_by_file[file_path].append(issue)
        
        # ID unique pour cette section
        safe_id = error_type.replace('_', '').replace('-', '')
        
        html = f"""
        <div class="error-type-section" data-error-type="{error_type}">
            <div class="error-type-header" onclick="toggleSection('{safe_id}')" style="cursor: pointer;" role="button" tabindex="0" aria-expanded="false">
                <div>
                    <span class="collapsible-toggle" id="icon_{safe_id}">▶</span>
                    {type_icon} <strong>{type_name}</strong>
                    <span class="error-type-badge {css_class}">{len(issues)}</span>
                </div>
                <div class="stats-overview">
                    <span class="mini-stat">{len(issues_by_file)} fichier(s)</span>
                    <span class="mini-stat">{len(issues)} erreur(s)</span>
                </div>
            </div>
            
            <div class="error-type-content" id="content_{safe_id}" style="display: none;">
        """
        
        # Contenu par fichier
        for file_path, file_issues in issues_by_file.items():
            file_name = os.path.basename(file_path)
            html += f"""
                <div class="file-section" data-file="{file_name}">
                    <div class="file-header">
                        📄 {_html.escape(file_name)} ({len(file_issues)} erreur(s))
                    </div>
            """
            
            # Issues dans ce fichier
            for issue in file_issues:
                html += self._generate_issue_item(issue)
            
            html += "</div>"
        
        html += """
            </div>
        </div>
        """
        
        return html
    
    
    def _generate_issue_item(self, issue: Dict) -> str:
        """Génère un élément d'erreur individuel avec édition en ligne"""
        line = int(issue.get('line', 0) or 0)
        file_path = issue.get('file_path', '') or ''
        description = _html.escape(issue.get('description', ''))
        old_content = _html.escape(issue.get('old_content', ''))
        new_content = _html.escape(issue.get('new_content', ''))
        issue_type = issue.get('type', '')

        # Bouton "Ouvrir dans l'éditeur" uniquement si on a un chemin ET une ligne valide
        if file_path and line > 0:
            btn_html = (
                f'<button type="button" class="open-in-editor" '
                f'data-file="{_html.escape(file_path)}" data-line="{line}" '
                f'title="Ouvrir dans l\'éditeur">'
                f'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
                f'<path d="M14 3l7 7-1.5 1.5L16 8.5V20h-2V8.5L8.5 11.5 7 10l7-7z"></path>'
                f'</svg><span>Ouvrir dans l\'éditeur</span></button>'
            )
        else:
            btn_html = ''
        
        # Extraire le chemin relatif depuis tl/langue/
        relative_file = self._get_relative_file_path(file_path)
        escaped_file = _html.escape(relative_file).replace('"', '&quot;')
        
        # Générer un ID unique pour les éléments interactifs
        import hashlib
        unique_id = hashlib.md5(f'{file_path}{line}'.encode()).hexdigest()[:8]
        
        # Checkbox d'exclusion pour les lignes non traduites
        exclude_checkbox_html = ''
        if issue_type == 'UNTRANSLATED_LINE':
            exclusion_key = issue.get('old_content', '')
            if exclusion_key:
                escaped_key = _html.escape(exclusion_key).replace('"', '&quot;')
                
                exclude_checkbox_html = f"""
            <div class="exclude-checkbox-container">
                <input type="checkbox" id="excl-{unique_id}" class="exclude-checkbox" 
                       data-exclusion-text="{escaped_key}"
                       data-exclusion-file="{escaped_file}"
                       data-exclusion-line="{line}"
                       title="Ignorer cette ligne dans les futurs rapports">
                <label for="excl-{unique_id}" class="exclude-label" title="Cliquez pour ignorer cette ligne">
                    <span class="exclusion-text">Cliquer pour ignorer</span>
                    <span class="exclusion-status"></span>
                </label>
            </div>
                """
        
        # 🆕 Interface d'édition en ligne (pour tous les types d'erreurs)
        # Pré-remplir avec le contenu OLD (la version originale à corriger)
        # L'utilisateur corrige OLD pour qu'il devienne conforme
        edit_value = issue.get('old_content', '')
        # Échapper pour l'attribut HTML mais pas pour le contenu du textarea
        escaped_edit_value = _html.escape(edit_value) if edit_value else ''
        
        edit_interface_html = f"""
        <div class="edit-interface" id="edit-{unique_id}" style="margin-top: 15px; padding: 15px; background: rgba(13,110,253,0.08); border-radius: 8px; border: 1px solid rgba(13,110,253,0.3);">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <span class="exclusion-status" id="status-{unique_id}" style="display: none; color: var(--success); font-weight: 500;"></span>
            </div>
            <div style="display: flex; gap: 10px; align-items: flex-start;">
                <textarea 
                    id="editField-{unique_id}" 
                    class="edit-field"
                    data-file="{escaped_file}"
                    data-line="{line}"
                    style="flex: 1; padding: 10px; border: 1px solid var(--sep); border-radius: 6px; background: var(--bg); color: var(--fg); font-family: 'Consolas', 'Monaco', monospace; font-size: 0.9rem; min-height: 80px; resize: vertical;"
                    placeholder="Entrez la traduction corrigée..."
                    title="Modifiez le texte ici puis cliquez sur Enregistrer"
                >{escaped_edit_value}</textarea>
                <div style="display: flex; flex-direction: column; gap: 8px;">
                    <button type="button" class="translate-btn btn" id="translate-{unique_id}"
                        data-edit-field="editField-{unique_id}"
                        style="padding: 8px 12px; background: var(--info); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 0.85rem; white-space: nowrap;"
                        title="Traduire automatiquement avec le service sélectionné">
                        🌐 Traduire
                    </button>
                    <button type="button" class="save-btn btn" id="save-{unique_id}"
                        data-edit-field="editField-{unique_id}"
                        data-file="{escaped_file}"
                        data-line="{line}"
                        data-status="status-{unique_id}"
                        style="padding: 8px 12px; background: var(--success); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 0.85rem; white-space: nowrap;"
                        title="Enregistrer cette modification">
                        💾 Enregistrer
                    </button>
                </div>
            </div>
        </div>
        """

        return f"""
        <div class="issue-item" data-unique-id="{unique_id}">
            <div class="issue-header">
                <div class="issue-line">Ligne {line}</div>
                {btn_html}
            </div>
            <div class="issue-description">{description}</div>
            <div class="content-comparison">
                <div class="content-block old-content">
                    <div class="content-label">Ancien</div>
                    <div>{old_content if old_content else '<em>Vide</em>'}</div>
                </div>
                <div class="content-block new-content">
                    <div class="content-label">Nouveau</div>
                    <div>{new_content if new_content else '<em>Vide</em>'}</div>
                </div>
            </div>
            {exclude_checkbox_html}
            {edit_interface_html}
        </div>
        """

    
    def _get_error_type_display_name(self, error_type: str) -> str:
        """Retourne le nom d'affichage d'un type d'erreur"""
        type_names = {
            "VARIABLE_MISMATCH": "Variables [] incohérentes",
            "TAG_MISMATCH": "Balises {} incohérentes", 
            "PLACEHOLDER_MISMATCH": "Placeholders () incohérents",
            "UNRESTORED_PLACEHOLDER": "Placeholders non restaurés",
            "MALFORMED_PLACEHOLDER": "Placeholder malformé",
            "SPECIAL_CODE_MISMATCH": "Codes spéciaux incohérents",
            "PARENTHESES_MISMATCH": "Parenthèses incohérentes",
            "FRENCH_QUOTES_MISMATCH": "Guillemets français incohérents",
            "QUOTE_COUNT_MISMATCH": "Nombre de guillemets différent",
            "UNTRANSLATED_LINE": "Ligne potentiellement non traduite",
            "MISSING_OLD": "Ligne ANCIENNE manquante",
            "CONTENT_PREFIX_MISMATCH": "Préfixe de contenu incohérent",
            "CONTENT_SUFFIX_MISMATCH": "Suffixe de contenu incohérent",
            "FILE_ERROR": "Erreur de fichier",
            "ANALYSIS_ERROR": "Erreur d'analyse",
            "LENGTH_DISCREPANCY": "Différence de longueur",
            # Nouveaux types fusionnés
            "QUOTES_MISMATCH": "Guillemets incohérents",
            "PERCENTAGE_MISMATCH": "Pourcentages incohérents",
            # Anciens types (compatibilité)
            "ESCAPED_QUOTES_MISMATCH": "Guillemets échappés incohérents",
            "QUOTE_BALANCE_ERROR": "Guillemets non équilibrés",
            "UNESCAPED_QUOTES_MISMATCH": "Guillemets non échappés incohérents",
            "PERCENTAGE_FORMAT_MISMATCH": "Variables % incohérentes",
            "DOUBLE_PERCENT_MISMATCH": "Double % incohérent"
        }
        return type_names.get(error_type, error_type.replace('_', ' ').title())
    
    def _get_error_type_icon(self, error_type: str) -> str:
        """Retourne l'icône d'un type d'erreur"""
        icons = {
            "VARIABLE_MISMATCH": "🔤",
            "TAG_MISMATCH": "🏷️",
            "PLACEHOLDER_MISMATCH": "📝",
            "UNRESTORED_PLACEHOLDER": "🔄",
            "MALFORMED_PLACEHOLDER": "⚠️",
            "SPECIAL_CODE_MISMATCH": "💻",
            "PARENTHESES_MISMATCH": "〔〕",
            "FRENCH_QUOTES_MISMATCH": "「」",
            "QUOTE_COUNT_MISMATCH": "\"\"",
            "UNTRANSLATED_LINE": "🌐",
            "MISSING_OLD": "❌",
            "CONTENT_PREFIX_MISMATCH": "⬅️",
            "CONTENT_SUFFIX_MISMATCH": "➡️",
            "FILE_ERROR": "💥",
            "ANALYSIS_ERROR": "🐛",
            # Nouveaux types fusionnés
            "QUOTES_MISMATCH": "\"\"",
            "PERCENTAGE_MISMATCH": "%%"
        }
        return icons.get(error_type, "⚠️")
    
    def _get_error_type_css_class(self, error_type: str) -> str:
        """Retourne la classe CSS pour un type d'erreur"""
        classes = {
            "VARIABLE_MISMATCH": "badge-variable",
            "TAG_MISMATCH": "badge-tag",
            "PLACEHOLDER_MISMATCH": "badge-placeholder",
            "UNRESTORED_PLACEHOLDER": "badge-placeholder",
            "MALFORMED_PLACEHOLDER": "badge-placeholder",
            "SPECIAL_CODE_MISMATCH": "badge-special",
            "PARENTHESES_MISMATCH": "badge-special",
            "FRENCH_QUOTES_MISMATCH": "badge-special",
            "QUOTE_COUNT_MISMATCH": "badge-special",
            "UNTRANSLATED_LINE": "badge-untranslated",
            "MISSING_OLD": "badge-other",
            "CONTENT_PREFIX_MISMATCH": "badge-other",
            "CONTENT_SUFFIX_MISMATCH": "badge-other",
            "FILE_ERROR": "badge-other",
            "ANALYSIS_ERROR": "badge-other",
            # Nouveaux types fusionnés
            "QUOTES_MISMATCH": "badge-special",
            "PERCENTAGE_MISMATCH": "badge-special"
        }
        return classes.get(error_type, "badge-other")
    
    def _generate_footer(self) -> str:
        """Génère le pied de page"""
        return """
        <div style="text-align: center; padding: 40px 20px; opacity: 0.7; border-top: 1px solid var(--sep);">
            <p>✨ Rapport généré automatiquement par RenExtract</p>
            <p>🔍 Outil de vérification intelligente de cohérence Ren'Py</p>
        </div>
        """
    
    def _get_relative_file_path(self, file_path):
        """Retourne le chemin relatif du fichier depuis le dossier tl"""
        try:
            # Trouver la position de 'tl/' dans le chemin
            if '/tl/' in file_path:
                parts = file_path.split('/tl/')
                if len(parts) > 1:
                    # Retourner ce qui est après tl/langue/
                    sub_parts = parts[1].split('/', 1)
                    if len(sub_parts) > 1:
                        return sub_parts[1].replace('\\', '/')
            elif '\\tl\\' in file_path:
                parts = file_path.split('\\tl\\')
                if len(parts) > 1:
                    sub_parts = parts[1].split('\\', 1)
                    if len(sub_parts) > 1:
                        return sub_parts[1].replace('\\', '/')
            
            # Fallback: retourner le nom du fichier
            return os.path.basename(file_path)
        except Exception:
            return os.path.basename(file_path)


# Fonction utilitaire pour l'intégration
def create_html_coherence_report(results: Dict[str, Any], project_path: str, 
                               execution_time: str) -> Optional[str]:
    """
    Fonction utilitaire pour créer un rapport HTML de cohérence
    
    Args:
        results: Résultats de l'analyse de cohérence
        project_path: Chemin du projet 
        execution_time: Temps d'exécution formaté
        
    Returns:
        Chemin du rapport généré ou None
    """
    generator = HtmlCoherenceReportGenerator()
    return generator.generate_coherence_report(results, project_path, execution_time)