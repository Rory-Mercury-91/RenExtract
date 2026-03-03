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
            padding: 0; border-bottom: 1px solid var(--sep);
            transition: background 0.2s, opacity 0.3s;
          }
          .issue-item:hover { background: var(--hover-bg); }
          .issue-item:last-child { border-bottom: none; }
          .issue-item .issue-header {
            cursor: pointer; user-select: none; padding: 15px;
            display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
          }
          .issue-item .issue-header .issue-toggle-icon {
            font-size: 0.75rem; transition: transform 0.2s; flex-shrink: 0;
          }
          .issue-item .issue-item-content {
            padding: 0 15px 15px 15px; border-top: 1px solid var(--sep);
          }
          .issue-item.collapsed .issue-item-content { display: none !important; }
          .issue-item.collapsed .issue-header .issue-toggle-icon { transform: rotate(-90deg); }
          .issue-item.excluded {
            opacity: 0.5;
            background: rgba(72, 187, 120, 0.1);
            border-left: 4px solid var(--success);
          }
          
          .exclude-toggle-container {
            display: flex; align-items: center; gap: 8px;
            padding: 8px; margin-top: 10px;
          }
          .exclude-toggle-btn {
            cursor: pointer; user-select: none; font-size: 0.85rem;
            padding: 6px 14px; border-radius: 6px;
            transition: all 0.2s ease;
            border: 1px solid var(--sep);
            background: transparent;
            color: var(--fg);
            font-weight: 500;
            flex-shrink: 0;
          }
          .exclude-toggle-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
          }
          .exclude-toggle-btn.excluded {
            background: var(--success);
            color: white;
            border-color: var(--success);
          }
          .exclude-toggle-btn .toggle-text-include {
            display: inline;
          }
          .exclude-toggle-btn .toggle-text-exclude {
            display: none;
          }
          .exclude-toggle-btn.excluded .toggle-text-include {
            display: none;
          }
          .exclude-toggle-btn.excluded .toggle-text-exclude {
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
          
          /* ✅ CORRECTION : S'assurer que le textarea est toujours visible */
          .edit-interface {
            display: block !important;
          }
          
          .edit-field {
            display: block !important;
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
          
          .bulk-translate-header:hover { background: var(--hover-bg); border-radius: 8px 8px 0 0; }
          
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
        from ui.shared.translator_utils import get_default_translator
        server_host_config = config_manager.get('editor_server_host', '127.0.0.1') or '127.0.0.1'
        try:
            server_port_config = int(config_manager.get('editor_server_port', 8765))
        except Exception:
            server_port_config = 8765
        
        server_host_client = '127.0.0.1' if server_host_config in ('0.0.0.0', '::') else server_host_config
        server_url = f"http://{server_host_client}:{server_port_config}"
        
        # Obtenir le traducteur par défaut et l'option "réutiliser même onglet"
        default_translator = get_default_translator()
        reuse_translate_tab = config_manager.get('coherence_reuse_translate_tab', True)
        
        log_message("DEBUG", f"🎯 Génération JavaScript rapport : server_url={server_url}, default_translator={default_translator}, reuse_translate_tab={reuse_translate_tab}", category="report")
        
        return f"""
        <script>
        (function() {{
            // URL du serveur d'édition (configurable pour support WSL)
            window.RENEXTRACT_SERVER_URL = '{server_url}';
            window.RENEXTRACT_LANGUAGE = '{language}';
            window.RENEXTRACT_REUSE_TRANSLATE_TAB = {str(reuse_translate_tab).lower()};
            
            // Informations sur la sélection harmonisée
            window.coherenceSelectionInfo = {{
                isAllFiles: {str(is_all_files).lower()},
                language: '{language}',
                selectedFile: '{selected_file}',
                totalFiles: {total_files},
                project_path: '{project_path}',  // 🆕
                default_translator: '{default_translator}'  // 🆕 Traducteur par défaut
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
            
            // 🆕 Gestion du traducteur par défaut
            async function loadDefaultTranslator() {{
                try {{
                    const translatorSelect = document.getElementById('translatorSelect');
                    if (!translatorSelect) return;
                    
                    // Charger depuis la config (Google, DeepL, Microsoft, Yandex uniquement)
                    const defaultTranslator = window.coherenceSelectionInfo.default_translator || 'Google';
                    const validTranslators = ['Google', 'DeepL', 'Microsoft', 'Yandex'];
                    const translator = validTranslators.indexOf(defaultTranslator) >= 0 ? defaultTranslator : 'Google';
                    translatorSelect.value = translator;
                    console.log(`✅ Traducteur chargé: ${{translator}}`);
                }} catch (error) {{
                    console.error('❌ Erreur chargement traducteur:', error);
                }}
            }}
            
            async function saveTranslatorChoice(translator) {{
                try {{
                    const response = await fetch(`${{window.RENEXTRACT_SERVER_URL}}/api/coherence/translator`, {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ translator }})
                    }});
                    
                    if (response.ok) {{
                        const data = await response.json();
                        if (data.ok) {{
                            console.log(`✅ Traducteur sauvegardé: ${{translator}}`);
                            // Mettre à jour la valeur par défaut dans window.coherenceSelectionInfo
                            window.coherenceSelectionInfo.default_translator = translator;
                        }}
                    }}
                }} catch (error) {{
                    console.error('❌ Erreur sauvegarde traducteur:', error);
                }}
            }}
            
            // Initialiser le traducteur et ajouter l'event listener au chargement
            document.addEventListener('DOMContentLoaded', function() {{
                const translatorSelect = document.getElementById('translatorSelect');
                if (translatorSelect) {{
                    // Charger la valeur par défaut
                    loadDefaultTranslator();
                    
                    // Sauvegarder quand l'utilisateur change de traducteur
                    translatorSelect.addEventListener('change', function() {{
                        saveTranslatorChoice(this.value);
                    }});
                }}
            }});

            // Fonction pour ouvrir dans l'éditeur
            window.openInEditor = function(filePath, lineNumber) {{
                const url = `${{window.RENEXTRACT_SERVER_URL}}/open?file=${{encodeURIComponent(filePath)}}&line=${{encodeURIComponent(lineNumber)}}`;

                fetch(url, {{ method: 'GET' }})
                    .then(async (res) => {{
                        if (!res.ok) throw new Error('HTTP ' + res.status);
                        const data = await res.json().catch(() => ({{}}));
                        const msg = data && (data.message || (data.ok ? "Ouvert dans l\'éditeur." : 'Requête envoyée.'));
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
                            
                            // 🆕 Log des clés pour débogage
                            if (data.exclusions.length > 0 && data.exclusions.length <= 5) {{
                                data.exclusions.forEach(excl => {{
                                    const key = `${{project}}|${{excl.file}}|${{excl.line}}|${{excl.text}}`;
                                    console.log('  📋 Clé chargée:', key.substring(0, 120) + '...');
                                }});
                            }}
                            
                            updateToggleStates();
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
            
            // Mettre à jour l'état des boutons toggle selon les exclusions
            function updateToggleStates() {{
                const project = window.coherenceSelectionInfo.project_path;
                
                document.querySelectorAll('.exclude-toggle-btn').forEach(btn => {{
                    const text = btn.getAttribute('data-exclusion-text');
                    const file = btn.getAttribute('data-exclusion-file');
                    const line = parseInt(btn.getAttribute('data-exclusion-line'));
                    
                    // Construire la clé complète
                    const cacheKey = `${{project}}|${{file}}|${{line}}|${{text}}`;
                    const isExcluded = window.exclusionsCache.has(cacheKey);
                    
                    // Mettre à jour l'état du bouton
                    if (isExcluded) {{
                        btn.classList.add('excluded');
                    }} else {{
                        btn.classList.remove('excluded');
                    }}
                    
                    // Marquer visuellement la ligne comme exclue
                    const issueItem = btn.closest('.issue-item');
                    if (isExcluded) {{
                        issueItem.classList.add('excluded');
                    }} else {{
                        issueItem.classList.remove('excluded');
                    }}
                }});
            }}
            
            // Ajouter une exclusion
            async function addExclusion(text, file, line, project) {{
                const cacheKey = `${{project}}|${{file}}|${{line}}|${{text}}`;
                console.log('📤 POST /exclude:', {{ 
                    text: text.substring(0, 50), 
                    file, 
                    line, 
                    project: project.substring(0, 50),
                    cacheKey: cacheKey.substring(0, 100) + '...'
                }});
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
                            window.exclusionsCache.add(cacheKey);
                            console.log('✅ Exclusion ajoutée avec clé:', cacheKey.substring(0, 100) + '...');
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
            
            // Handler pour les boutons toggle d'exclusion
            async function handleExcludeToggle(btn) {{
                const text = btn.getAttribute('data-exclusion-text');
                const file = btn.getAttribute('data-exclusion-file');
                const line = parseInt(btn.getAttribute('data-exclusion-line'));
                const project = window.coherenceSelectionInfo.project_path;
                
                // Validation des données avant envoi
                if (!text || !file || !line || !project) {{
                    console.error('❌ Données manquantes:', {{ text: !!text, file: !!file, line: !!line, project: !!project }});
                    alert("⚠️ Erreur: données incomplètes pour l\'exclusion");
                    return;
                }}
                
                const issueItem = btn.closest('.issue-item');
                const isCurrentlyExcluded = btn.classList.contains('excluded');
                
                if (!isCurrentlyExcluded) {{
                    // Ajouter l'exclusion
                    const success = await addExclusion(text, file, line, project);
                    if (success) {{
                        btn.classList.add('excluded');
                        issueItem.classList.add('excluded');
                    }}
                }} else {{
                    // Retirer l'exclusion
                    const success = await removeExclusion(text, file, line, project);
                    if (success) {{
                        btn.classList.remove('excluded');
                        issueItem.classList.remove('excluded');
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

            // ===== NOUVEAU : Gestion du collage depuis le presse-papier =====
            async function pasteText(editFieldId) {{
                const editField = document.getElementById(editFieldId);
                if (!editField) return;
                
                const pasteBtn = document.querySelector(`.paste-btn[data-edit-field="${{editFieldId}}"]`);
                
                // Fallback manuel si le contexte n'est pas sécurisé ou si l'API clipboard est indisponible
                const canUseClipboardApi = window.isSecureContext && navigator.clipboard && navigator.clipboard.readText;
                if (!canUseClipboardApi) {{
                    const manualText = prompt(
                        "Collage manuel requis\\n\\nVotre navigateur bloque l'accès direct au presse-papier dans ce contexte.\\nCollez votre texte ici (Ctrl+V), puis validez pour l'insérer dans le champ :",
                        ""
                    );
                    
                    if (manualText !== null) {{
                        editField.value = manualText;
                        showGlobalMessage('✅ Texte inséré via le mode manuel', 'success', 2500);
                        console.log('✅ Texte collé via le mode manuel (prompt)');
                    }} else {{
                        showGlobalMessage('ℹ️ Collage annulé', 'info', 2000);
                    }}
                    
                    if (pasteBtn) {{
                        pasteBtn.disabled = false;
                        pasteBtn.textContent = '📋 Coller';
                    }}
                    return;
                }}
                
                try {{
                    if (pasteBtn) {{
                        pasteBtn.disabled = true;
                        pasteBtn.textContent = '⏳ Collage...';
                    }}
                    
                    const clipboardText = await navigator.clipboard.readText();
                    
                    if (!clipboardText) {{
                        showGlobalMessage('⚠️ Le presse-papier est vide', 'warning', 3000);
                        return;
                    }}
                    
                    editField.value = clipboardText;
                    showGlobalMessage('✅ Texte collé avec succès', 'success', 2000);
                    console.log('✅ Texte collé depuis le presse-papier (API)');
                }} catch (error) {{
                    console.error('❌ Erreur collage:', error);
                    
                    if (error.name === 'NotAllowedError') {{
                        showGlobalMessage("⚠️ Permission refusée - Autorisez l\'accès au presse-papier", 'error', 4000);
                    }} else if (error.name === 'NotFoundError') {{
                        showGlobalMessage("⚠️ Aucun contenu détecté dans le presse-papier", 'warning', 3000);
                    }} else {{
                        showGlobalMessage('❌ Erreur lors du collage depuis le presse-papier', 'error', 4000);
                    }}
                }} finally {{
                    if (pasteBtn) {{
                        pasteBtn.disabled = false;
                        pasteBtn.textContent = '📋 Coller';
                    }}
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
                    const translateBtn = document.querySelector(`.translate-btn[data-edit-field="${{editFieldId}}"]`);
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
                            // Ouvrir l'URL du traducteur web (réutiliser même onglet si config activée)
                            const targetWindow = (window.RENEXTRACT_REUSE_TRANSLATE_TAB !== false) ? 'ren extract_translate' : '_blank';
                            window.open(data.url, targetWindow);
                            showGlobalMessage(`🌐 Traducteur ${{data.service}} ouvert` + (targetWindow === 'ren extract_translate' ? ' (même onglet)' : ' dans un nouvel onglet'), 'info', 3000);
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
                    const translateBtn = document.querySelector(`.translate-btn[data-edit-field="${{editFieldId}}"]`);
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
                        body: JSON.stringify({{ file, line, new_content: newContent, project, language: window.RENEXTRACT_LANGUAGE }})
                    }});
                    
                    if (response.ok) {{
                        const data = await response.json();
                        if (data.ok) {{
                            // 🆕 Marquer visuellement l'issue comme enregistrée (PERSISTANT)
                            const statusSpan = document.getElementById(statusId);
                            const issueItem = statusSpan ? statusSpan.closest('.issue-item') : null;
                            const issueHeader = issueItem ? issueItem.querySelector('.issue-header') : null;
                            
                            if (issueItem) {{
                                issueItem.classList.add('saved');
                                if (issueHeader && !issueHeader.querySelector('.saved-badge')) {{
                                    const badge = document.createElement('span');
                                    badge.className = 'saved-badge';
                                    badge.innerHTML = '✅ Enregistré';
                                    issueHeader.appendChild(badge);
                                }}
                                const bulkCb = issueItem.querySelector('.bulk-checkbox');
                                if (bulkCb) {{ bulkCb.checked = false; bulkCb.disabled = true; }}
                                const uid = issueItem.getAttribute('data-unique-id');
                                if (uid && typeof collapseIssueItem === 'function') collapseIssueItem(uid);
                            }}
                            document.querySelectorAll('.edit-field').forEach(f => {{
                                if (f.getAttribute('data-file') === file && parseInt(f.getAttribute('data-line'), 10) === line) f._originalValue = f.value;
                            }});
                            if (statusSpan) {{
                                statusSpan.textContent = '✅ Enregistré';
                                statusSpan.style.display = 'inline';
                                setTimeout(() => {{ statusSpan.style.display = 'none'; }}, 3000);
                            }}
                            if (typeof updateBulkUI === 'function') updateBulkUI();
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
            
            // Conserver la valeur initiale de chaque champ pour n'enregistrer que les lignes modifiées
            function initEditFieldsOriginalValue() {{
                document.querySelectorAll('.edit-field').forEach(field => {{
                    if (field._originalValue === undefined) field._originalValue = field.value;
                }});
            }}
            // ===== NOUVEAU : Enregistrement global =====
            async function saveAll() {{
                try {{
                    const project = window.coherenceSelectionInfo.project_path;
                    initEditFieldsOriginalValue();
                    
                    // Collecter uniquement les lignes réellement modifiées
                    const modifications = [];
                    document.querySelectorAll('.edit-field').forEach(field => {{
                        const file = field.getAttribute('data-file');
                        const line = parseInt(field.getAttribute('data-line'));
                        const new_content = field.value.trim();
                        const original = (field._originalValue != null ? field._originalValue : field.value).trim();
                        
                        if (file && line && new_content && new_content !== original) {{
                            modifications.push({{ file, line, new_content }});
                        }}
                    }});
                    
                    if (modifications.length === 0) {{
                        showGlobalMessage('⚠️ Aucune modification à enregistrer (seules les lignes modifiées sont prises en compte)', 'warning', 3000);
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
                            
                            // Mettre à jour _originalValue pour les champs enregistrés (évite de les renvoyer au prochain "Enregistrer tout")
                            const savedFiles = new Set(modifications.map(m => m.file + ':' + m.line));
                            document.querySelectorAll('.edit-field').forEach(field => {{
                                const file = field.getAttribute('data-file');
                                const line = parseInt(field.getAttribute('data-line'));
                                if (file && line && savedFiles.has(file + ':' + line)) field._originalValue = field.value;
                            }});
                            // 🆕 Marquer visuellement les lignes enregistrées et désactiver les cases traduction en lot
                            document.querySelectorAll('.edit-field').forEach(field => {{
                                const file = field.getAttribute('data-file');
                                const line = parseInt(field.getAttribute('data-line'));
                                if (!file || !line || !savedFiles.has(file + ':' + line)) return;
                                const issueItem = field.closest('.issue-item');
                                const issueHeader = issueItem ? issueItem.querySelector('.issue-header') : null;
                                
                                if (issueItem) {{
                                    issueItem.classList.add('saved');
                                    if (issueHeader && !issueHeader.querySelector('.saved-badge')) {{
                                        const badge = document.createElement('span');
                                        badge.className = 'saved-badge';
                                        badge.innerHTML = '✅ Enregistré';
                                        issueHeader.appendChild(badge);
                                    }}
                                    const bulkCb = issueItem.querySelector('.bulk-checkbox');
                                    if (bulkCb) {{ bulkCb.checked = false; bulkCb.disabled = true; }}
                                }}
                                const statusId = issueItem ? issueItem.querySelector('.exclusion-status')?.id : null;
                                if (statusId) {{
                                    const statusSpan = document.getElementById(statusId);
                                    if (statusSpan) {{
                                        statusSpan.textContent = '✅ Enregistré';
                                        statusSpan.style.display = 'inline';
                                        setTimeout(() => {{ statusSpan.style.display = 'none'; }}, 3000);
                                    }}
                                }}
                            }});
                            if (typeof updateBulkUI === 'function') updateBulkUI();
                        }} else {{
                            showGlobalMessage("❌ Erreur lors de l\'enregistrement global", 'error', 5000);
                        }}
                    }} else {{
                        showGlobalMessage("❌ Erreur lors de l\'enregistrement global", 'error', 5000);
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
                initEditFieldsOriginalValue();
                loadExclusions();
                
                // Délégation: clic sur boutons "open in editor"
                document.body.addEventListener('click', function(e) {{
                    const btn = e.target.closest('.open-in-editor');
                    if (!btn) return;
                    const f = btn.getAttribute('data-file');
                    const l = parseInt(btn.getAttribute('data-line') || '0', 10) || 0;
                    if (f && l) window.openInEditor(f, l);
                }});
                
                // Délégation: clic sur boutons toggle d'exclusion
                document.body.addEventListener('click', function(e) {{
                    if (e.target.classList.contains('exclude-toggle-btn') || e.target.closest('.exclude-toggle-btn')) {{
                        const btn = e.target.classList.contains('exclude-toggle-btn') ? e.target : e.target.closest('.exclude-toggle-btn');
                        handleExcludeToggle(btn);
                    }}
                }});
                
                // Délégation: clic sur boutons "Coller"
                document.body.addEventListener('click', function(e) {{
                    if (e.target.classList.contains('paste-btn')) {{
                        const editFieldId = e.target.getAttribute('data-edit-field');
                        if (editFieldId) pasteText(editFieldId);
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

                // ===== Traduction en lot (RENEXTRACT_001, RENEXTRACT_002, …) =====
                function getBulkLimit() {{
                    const sel = document.getElementById('translatorSelect');
                    if (!sel) return 5000;
                    switch (sel.value) {{
                        case 'DeepL': return 1500;
                        case 'Microsoft': return 1000;
                        case 'Yandex': return 10000;
                        default: return 5000;
                    }}
                }}
                function updateBulkUI() {{
                    const limit = getBulkLimit();
                    const countEl = document.getElementById('bulkCharCount');
                    if (!countEl) return;
                    const checkboxes = Array.from(document.querySelectorAll('.bulk-checkbox')).filter(cb => {{
                        const item = cb.closest('.issue-item');
                        return item && item.style.display !== 'none';
                    }});
                    let total = 0;
                    const checked = [];
                    checkboxes.forEach(cb => {{
                        if (cb.checked) {{
                            const len = (cb.getAttribute('data-old-content') || '').length;
                            total += len;
                            checked.push(cb);
                        }}
                    }});
                    const atLimit = total >= limit;
                    checkboxes.forEach(cb => {{
                        if (!cb.checked) cb.disabled = atLimit;
                    }});
                    countEl.textContent = total + ' / ' + limit + ' caractères';
                }}
                function copyBulk() {{
                    const checkboxes = Array.from(document.querySelectorAll('.bulk-checkbox')).filter(cb => {{
                        if (!cb.checked) return false;
                        const item = cb.closest('.issue-item');
                        if (!item) return false;
                        const style = window.getComputedStyle(item);
                        return style.display !== 'none' && style.visibility !== 'hidden';
                    }});
                    if (checkboxes.length === 0) {{
                        showGlobalMessage('⚠️ Cochez au moins une ligne (section Ancien)', 'warning', 3000);
                        return;
                    }}
                    const parts = [];
                    checkboxes.forEach((cb, i) => {{
                        const content = (cb.getAttribute('data-old-content') || '').replace(/\\s+/g, ' ').trim();
                        parts.push('RENEXTRACT_' + String(i + 1).padStart(3, '0') + '\\n' + content);
                    }});
                    const text = parts.join('\\n\\n');
                    const pasteArea = document.getElementById('bulkPasteArea');
                    if (pasteArea) pasteArea.value = text;
                    if (navigator.clipboard && navigator.clipboard.writeText) {{
                        navigator.clipboard.writeText(text).then(() => {{
                            showGlobalMessage('✅ Texte copié (' + checkboxes.length + ' bloc(s)) — collez-le dans Google/DeepL, puis remplacez cette zone par la traduction et cliquez Appliquer', 'success', 5000);
                        }}).catch(() => {{
                            showGlobalMessage('✅ Sélection affichée ci-dessous (' + checkboxes.length + ' bloc(s)) — copiez-la dans Google/DeepL puis remplacez par la traduction et cliquez Appliquer', 'info', 5000);
                        }});
                    }} else {{
                        showGlobalMessage('✅ Sélection affichée ci-dessous (' + checkboxes.length + ' bloc(s)) — copiez-la dans Google/DeepL puis remplacez par la traduction et cliquez Appliquer', 'success', 5000);
                    }}
                }}
                async function pasteBulk() {{
                    const pasteArea = document.getElementById('bulkPasteArea');
                    if (!pasteArea) return;
                    try {{
                        if (navigator.clipboard && navigator.clipboard.readText) {{
                            const text = await navigator.clipboard.readText();
                            pasteArea.value = text;
                            showGlobalMessage('✅ Contenu du presse-papier collé dans la zone', 'success', 3000);
                        }} else {{
                            showGlobalMessage('⚠️ Coller manuellement (Ctrl+V) dans la zone — accès presse-papier non disponible', 'warning', 4000);
                        }}
                    }} catch (err) {{
                        showGlobalMessage('⚠️ Accès au presse-papier refusé. Collez manuellement (Ctrl+V) dans la zone.', 'warning', 4000);
                    }}
                }}
                function toggleIssueItem(uniqueId) {{
                    const issueItem = document.getElementById('issue-' + uniqueId) || document.querySelector('.issue-item[data-unique-id="' + uniqueId + '"]');
                    if (!issueItem) return;
                    const isCollapsed = issueItem.classList.toggle('collapsed');
                    const icon = document.getElementById('icon_issue_' + uniqueId);
                    if (icon) icon.textContent = isCollapsed ? '▶' : '▼';
                    issueItem.querySelector('.issue-header')?.setAttribute('aria-expanded', isCollapsed ? 'false' : 'true');
                }}
                function collapseIssueItem(uniqueId) {{
                    const issueItem = document.getElementById('issue-' + uniqueId) || document.querySelector('.issue-item[data-unique-id="' + uniqueId + '"]');
                    if (!issueItem || issueItem.classList.contains('collapsed')) return;
                    issueItem.classList.add('collapsed');
                    const icon = document.getElementById('icon_issue_' + uniqueId);
                    if (icon) icon.textContent = '▶';
                    issueItem.querySelector('.issue-header')?.setAttribute('aria-expanded', 'false');
                }}
                function applyBulk() {{
                    const textarea = document.getElementById('bulkPasteArea');
                    const text = (textarea && textarea.value) ? textarea.value.trim() : '';
                    if (!text) {{
                        showGlobalMessage('⚠️ Coller d\\'abord les traductions dans la zone ci-dessus', 'warning', 3000);
                        return;
                    }}
                    const checkboxes = Array.from(document.querySelectorAll('.bulk-checkbox:checked')).filter(cb => {{
                        const item = cb.closest('.issue-item');
                        return item && item.style.display !== 'none';
                    }});
                    const regex = /RENEXTRACT_\\d+\\s*([\\s\\S]*?)(?=RENEXTRACT_\\d+|$)/g;
                    const blocks = [];
                    let m;
                    while ((m = regex.exec(text)) !== null) {{
                        blocks.push(m[1].trim());
                    }}
                    if (blocks.length !== checkboxes.length) {{
                        showGlobalMessage('❌ Nombre de blocs incorrect (attendu: ' + checkboxes.length + ', reçu: ' + blocks.length + '). Vérifiez que les marqueurs RENEXTRACT_001, etc. n\\'ont pas été supprimés par le traducteur.', 'error', 8000);
                        return;
                    }}
                    checkboxes.forEach((cb, i) => {{
                        const editId = cb.getAttribute('data-edit-field');
                        const field = document.getElementById(editId);
                        if (field) field.value = blocks[i];
                    }});
                    // Décocher les cases appliquées et fermer les tuiles
                    checkboxes.forEach(cb => {{
                        cb.checked = false;
                        const issueItem = cb.closest('.issue-item');
                        if (issueItem) {{
                            const uid = issueItem.getAttribute('data-unique-id');
                            if (uid) collapseIssueItem(uid);
                        }}
                    }});
                    if (typeof updateBulkUI === 'function') updateBulkUI();
                    showGlobalMessage('✅ ' + blocks.length + ' traduction(s) appliquée(s). Lignes décochées et repliées. Pensez à enregistrer.', 'success', 4000);
                }}
                async function translateBulk() {{
                    const pasteArea = document.getElementById('bulkPasteArea');
                    const text = (pasteArea && pasteArea.value) ? pasteArea.value.trim() : '';
                    if (!text) {{
                        showGlobalMessage('⚠️ Cliquez d\\'abord sur « Copier tout » pour remplir la zone, ou collez le texte à traduire.', 'warning', 4000);
                        return;
                    }}
                    const translatorSelect = document.getElementById('translatorSelect');
                    const translator = (translatorSelect && translatorSelect.value) ? translatorSelect.value : 'Google';
                    const targetWindow = (window.RENEXTRACT_REUSE_TRANSLATE_TAB !== false) ? 'ren extract_translate' : '_blank';
                    const btn = document.getElementById('bulkTranslateBtn');
                    if (btn) {{ btn.disabled = true; btn.textContent = '⏳ Ouverture…'; }}
                    try {{
                        const response = await fetch(window.RENEXTRACT_SERVER_URL + '/api/coherence/translate', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{ text: text, translator: translator, target_lang: 'fr', max_length: getBulkLimit() }})
                        }});
                        const data = response.ok ? await response.json() : null;
                        if (data && data.url) {{
                            window.open(data.url, targetWindow);
                            showGlobalMessage('🌐 ' + (data.service || translator) + ' ouvert avec le contenu de la zone', 'success', 3000);
                        }} else if (data && data.translation) {{
                            if (pasteArea) pasteArea.value = data.translation;
                            showGlobalMessage('✅ Traduction insérée (' + (data.service || translator) + ')', 'success', 3000);
                        }} else {{
                            showGlobalMessage('⚠️ Pour la traduction en lot, choisissez Google ou DeepL dans le menu Traducteur.', 'warning', 4000);
                        }}
                    }} catch (err) {{
                        console.error(err);
                        showGlobalMessage('⚠️ RenExtract doit rester ouvert pour ouvrir le traducteur.', 'error', 4000);
                    }}
                    if (btn) {{ btn.disabled = false; btn.textContent = '🌐 Traduire'; }}
                }}
                function initBulk() {{
                    const translatorSelect = document.getElementById('translatorSelect');
                    if (translatorSelect) translatorSelect.addEventListener('change', updateBulkUI);
                    document.querySelectorAll('.bulk-checkbox').forEach(cb => cb.addEventListener('change', updateBulkUI));
                    updateBulkUI();
                }}
                function toggleBulkSection() {{
                    const content = document.getElementById('content_bulkTranslate');
                    const icon = document.getElementById('icon_bulkTranslate');
                    const header = document.getElementById('bulkTranslateHeader');
                    if (!content || !icon) return;
                    const isHidden = content.style.display === 'none' || !content.style.display;
                    content.style.display = isHidden ? 'block' : 'none';
                    icon.textContent = isHidden ? '▼' : '▶';
                    if (header) header.setAttribute('aria-expanded', isHidden ? 'true' : 'false');
                }}
                function toggleFeaturesSection() {{
                    const content = document.getElementById('content_features');
                    const icon = document.getElementById('icon_features');
                    const header = document.getElementById('featuresHeader');
                    if (!content || !icon) return;
                    const isHidden = content.style.display === 'none' || !content.style.display;
                    content.style.display = isHidden ? 'block' : 'none';
                    icon.textContent = isHidden ? '▼' : '▶';
                    if (header) header.setAttribute('aria-expanded', isHidden ? 'true' : 'false');
                }}
                function focusBulkSection() {{
                    const content = document.getElementById('content_bulkTranslate');
                    const icon = document.getElementById('icon_bulkTranslate');
                    const header = document.getElementById('bulkTranslateHeader');
                    const anchor = document.getElementById('anchorResumeGlobal');
                    if (!header) return;
                    const wasHidden = content && (content.style.display === 'none' || !content.style.display);
                    if (wasHidden) {{
                        content.style.display = 'block';
                        if (icon) icon.textContent = '▼';
                        header.setAttribute('aria-expanded', 'true');
                    }}
                    var target = anchor || header;
                    requestAnimationFrame(function() {{
                        requestAnimationFrame(function() {{
                            target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                        }});
                    }});
                }}
                if (document.readyState === 'loading') {{
                    document.addEventListener('DOMContentLoaded', initBulk);
                }} else {{
                    initBulk();
                }}
                document.body.addEventListener('click', function(e) {{
                    const issueHeader = e.target.closest('.issue-item .issue-header');
                    if (issueHeader && !e.target.closest('button') && !e.target.closest('.open-in-editor')) {{
                        const issueItem = issueHeader.closest('.issue-item');
                        if (issueItem) {{
                            const uid = issueItem.getAttribute('data-unique-id');
                            if (uid) {{ e.preventDefault(); toggleIssueItem(uid); return false; }}
                        }}
                    }}
                    if (e.target.id === 'focusBulkTranslateBtn' || e.target.closest('#focusBulkTranslateBtn')) {{ e.preventDefault(); focusBulkSection(); return false; }}
                    if (e.target.id === 'featuresHeader' || e.target.closest('#featuresHeader')) {{ e.preventDefault(); toggleFeaturesSection(); return false; }}
                    if (e.target.id === 'bulkTranslateHeader' || e.target.closest('#bulkTranslateHeader')) {{ e.preventDefault(); toggleBulkSection(); return false; }}
                    if (e.target.id === 'bulkCopyBtn' || e.target.closest('#bulkCopyBtn')) {{ e.preventDefault(); copyBulk(); return false; }}
                    if (e.target.id === 'bulkPasteBtn' || e.target.closest('#bulkPasteBtn')) {{ e.preventDefault(); pasteBulk(); return false; }}
                    if (e.target.id === 'bulkTranslateBtn' || e.target.closest('#bulkTranslateBtn')) {{ e.preventDefault(); translateBulk(); return false; }}
                    if (e.target.id === 'bulkApplyBtn' || e.target.closest('#bulkApplyBtn')) {{ e.preventDefault(); applyBulk(); return false; }}
                }});

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
                            // ✅ CORRECTION : Utiliser .file-section au lieu de [data-file]
                            const fileItems = section.querySelectorAll('.file-section');
                            let visibleFilesInSection = 0;
                            let issuesInSection = 0;

                            fileItems.forEach(fileItem => {{
                                const fileName = fileItem.getAttribute('data-file');
                                const fileMatches = selectedFile === 'all' || fileName === selectedFile;
                                const issues = Array.from(fileItem.querySelectorAll('.issue-item'));
                                
                                if (fileMatches) {{
                                    fileItem.style.display = 'block';
                                    visibleFilesInSection++;
                                    
                                    issues.forEach(issue => {{
                                        issue.style.display = 'block';
                                        // ✅ CORRECTION : S'assurer que le textarea est toujours visible
                                        const editInterface = issue.querySelector('.edit-interface');
                                        if (editInterface) {{
                                            editInterface.style.display = 'block';
                                        }}
                                        // ✅ CORRECTION : S'assurer que tous les textarea sont visibles
                                        const textareas = issue.querySelectorAll('.edit-field');
                                        textareas.forEach(textarea => {{
                                            textarea.style.display = 'block';
                                        }});
                                    }});
                                    
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
                
                // ✅ NOUVEAU : Fonction pour mettre à jour dynamiquement le filtre par fichier
                function updateFileFilterOptions() {{
                    const selectedErrorType = errorTypeFilter ? errorTypeFilter.value : 'all';
                    const fileFilterSelect = document.getElementById('fileFilter');
                    if (!fileFilterSelect) return;
                    
                    // Récupérer tous les fichiers disponibles pour le type d'erreur sélectionné
                    const availableFiles = new Set();
                    
                    document.querySelectorAll('.error-type-section').forEach(section => {{
                        const errorType = section.dataset.errorType;
                        const matchesErrorType = selectedErrorType === 'all' || errorType === selectedErrorType;
                        
                        if (matchesErrorType) {{
                            section.querySelectorAll('.file-section').forEach(fileSection => {{
                                const fileName = fileSection.getAttribute('data-file');
                                if (fileName) {{
                                    availableFiles.add(fileName);
                                }}
                            }});
                        }}
                    }});
                    
                    // Sauvegarder la sélection actuelle
                    const currentSelection = fileFilterSelect.value;
                    
                    // Vider et remplir le select
                    fileFilterSelect.innerHTML = '<option value="all">Tous les fichiers</option>';
                    
                    // Trier les fichiers par ordre alphabétique
                    const sortedFiles = Array.from(availableFiles).sort();
                    sortedFiles.forEach(fileName => {{
                        const option = document.createElement('option');
                        option.value = fileName;
                        option.textContent = fileName;
                        fileFilterSelect.appendChild(option);
                    }});
                    
                    // Restaurer la sélection si elle existe toujours, sinon "all"
                    if (currentSelection && Array.from(fileFilterSelect.options).some(opt => opt.value === currentSelection)) {{
                        fileFilterSelect.value = currentSelection;
                    }} else {{
                        fileFilterSelect.value = 'all';
                    }}
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
                    
                    // ✅ CORRECTION : Mettre à jour le filtre par fichier avant de réappliquer
                    updateFileFilterOptions();
                    
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

                // ✅ CORRECTION : Mettre à jour le filtre par fichier quand le type d'erreur change
                if (errorTypeFilter) {{
                    errorTypeFilter.addEventListener('change', function() {{
                        updateFileFilterOptions();
                        applyFilters();
                    }});
                }}
                if (fileFilter) fileFilter.addEventListener('change', applyFilters);
                if (resetBtn) resetBtn.addEventListener('click', resetAllFilters);
                
                // Initialiser le filtre par fichier au chargement
                updateFileFilterOptions();

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
                f.write(self._generate_bulk_translate_panel())
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
        
        html = self._generate_features_panel() + """
        <div class="summary-cards">
            <div class="card">
                <h3 id="anchorResumeGlobal">📊 Résumé Global</h3>
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
            <button type="button" id="focusBulkTranslateBtn" class="btn" style="padding: 6px 12px; white-space: nowrap;" title="Aller à la section Traduction en lot et l'ouvrir">📋 Focus Traduction par Lot</button>
            
            <div class="filter-group" style="margin-left: auto;">
                <span id="filterInfo" style="font-style: italic; opacity: 0.8;"></span>
            </div>
        </div>
        """
    
    def _generate_bulk_translate_panel(self) -> str:
        """Panneau traduction en lot : repliable, fermé par défaut ; copier sélection avec RENEXTRACT_001…, coller résultat, appliquer."""
        return """
        <div id="bulkTranslatePanel" class="bulk-translate-panel" style="margin: 15px 20px; background: var(--card-bg); border: 1px solid var(--sep); border-radius: 10px;">
            <div id="bulkTranslateHeader" class="bulk-translate-header" style="display: flex; align-items: center; gap: 8px; padding: 12px 15px; cursor: pointer; user-select: none;" role="button" tabindex="0" aria-expanded="false" title="Cliquer pour ouvrir ou fermer">
                <span id="icon_bulkTranslate" style="font-size: 0.85rem;">▶</span>
                <h3 style="margin: 0; font-size: 1rem;">📋 Traduction en lot</h3>
            </div>
            <div id="content_bulkTranslate" style="display: none; padding: 0 15px 15px 15px;">
            <div id="bulkTranslateConsignes" style="margin: 0 0 10px 0; font-size: 0.85rem; opacity: 0.95; line-height: 1.5;">
                <strong>Étapes :</strong>
                <ol style="margin: 6px 0 0 0; padding-left: 20px;">
                    <li>Sélectionnez votre traducteur dans le bandeau en haut (Google, DeepL, Microsoft ou Yandex).</li>
                    <li>Cochez les lignes à traduire dans les sections <strong>Ancien</strong> (limite selon le traducteur : voir le compteur).</li>
                    <li>Cliquez <strong>« Copier tout »</strong> : le texte apparaît ci-dessous et est copié dans le presse-papier.</li>
                    <li>Collez ce contenu dans votre traducteur (bouton <strong>Traduire</strong> pour ouvrir Google/DeepL, ou un autre outil) et traduisez.</li>
                    <li>Après traduction, cliquez <strong>« Coller tout »</strong> : le contenu de la zone ci-dessous est remplacé par votre traduction (conservez les marqueurs RENEXTRACT_001, etc.).</li>
                    <li>Cliquez <strong>« Appliquer »</strong> pour réinjecter les traductions dans les lignes.</li>
                    <li>Cliquez sur <strong>« Enregistrer tout »</strong> dans le bandeau en haut pour sauvegarder les modifications (évite de sauvegarder ligne par ligne).</li>
                </ol>
            </div>
            <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 10px;">
                <span id="bulkCharCount" style="font-weight: 600; font-size: 0.9rem;">0 / 5000 caractères</span>
                <button type="button" id="bulkCopyBtn" class="btn" style="padding: 6px 12px; background: var(--info); color: white;">📤 Copier tout</button>
                <button type="button" id="bulkPasteBtn" class="btn" style="padding: 6px 12px; background: #6c757d; color: white;" title="Coller le contenu du presse-papier dans la zone">📥 Coller tout</button>
                <button type="button" id="bulkTranslateBtn" class="btn" style="padding: 6px 12px; background: #4a90e2; color: white;" title="Ouvrir Google ou DeepL avec le contenu de la zone ci-dessous">🌐 Traduire</button>
            </div>
            <textarea id="bulkPasteArea" placeholder="Après « Copier tout », le texte à traduire s'affiche ici. Après traduction, remplacez tout par la traduction (en gardant RENEXTRACT_001, RENEXTRACT_002…) puis cliquez Appliquer." style="width: 100%; min-height: 100px; padding: 10px; border-radius: 6px; border: 1px solid var(--sep); background: var(--bg); color: var(--fg); font-family: monospace; font-size: 0.9rem; resize: vertical;"></textarea>
            <p style="margin: 8px 0 10px 0; font-size: 0.8rem; opacity: 0.85;">⚠️ Vérifiez que le nombre de blocs en sortie correspond au nombre de blocs copiés (DeepL/Google ne doivent pas supprimer les marqueurs RENEXTRACT_001, etc.).</p>
            <button type="button" id="bulkApplyBtn" class="btn" style="padding: 8px 16px; background: var(--success); color: white; font-weight: 600;">✅ Appliquer</button>
            </div>
        </div>
        """
    
    def _generate_features_panel(self) -> str:
        """Panneau « Fonctionnalités présentes » : rappel de toutes les fonctionnalités du rapport, repliable, fermé par défaut."""
        return """
        <div id="featuresPanel" class="bulk-translate-panel" style="margin: 15px 20px; background: var(--card-bg); border: 1px solid var(--sep); border-radius: 10px;">
            <div id="featuresHeader" class="bulk-translate-header" style="display: flex; align-items: center; gap: 8px; padding: 12px 15px; cursor: pointer; user-select: none;" role="button" tabindex="0" aria-expanded="false" title="Cliquer pour ouvrir ou fermer">
                <span id="icon_features" style="font-size: 0.85rem;">▶</span>
                <h3 style="margin: 0; font-size: 1rem;">📌 Fonctionnalités présentes</h3>
            </div>
            <div id="content_features" style="display: none; padding: 0 15px 15px 15px;">
                <ul style="margin: 0; padding-left: 20px; line-height: 1.6; font-size: 0.9rem;">
                    <li><strong>Résumé global :</strong> Cartes avec fichiers analysés, total des erreurs et répartition par type.</li>
                    <li><strong>Filtres :</strong> Par type d'erreur, par fichier ; bouton Réinitialiser ; case « Ancien » ; bouton « Focus Traduction par Lot » pour accéder au panneau en lot.</li>
                    <li><strong>Thème :</strong> Bascule entre affichage clair et sombre.</li>
                    <li><strong>Tout déplier / Tout replier :</strong> Ouvrir ou fermer toutes les sections d'erreurs d'un coup.</li>
                    <li><strong>Traducteur :</strong> Choix Google, DeepL, Microsoft ou Yandex (traduction assistée et panneau en lot).</li>
                    <li><strong>Enregistrer tout :</strong> Enregistre les modifications (éditions et exclusions). RenExtract doit rester ouvert.</li>
                    <li><strong>Édition en ligne :</strong> Modifiez le texte directement dans le rapport puis cliquez sur « Enregistrer » sur la ligne.</li>
                    <li><strong>Traduction assistée :</strong> Bouton « Traduire » sur une ligne pour obtenir une suggestion de traduction automatique.</li>
                    <li><strong>Exclusions :</strong> Cochez « ✓ Ignoré » pour exclure une ligne des prochaines analyses.</li>
                    <li><strong>Traduction en lot :</strong> Panneau dédié (Copier tout, traduction externe, Coller tout, Appliquer) pour traduire plusieurs lignes en une fois.</li>
                </ul>
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
            'VARIABLE_MISMATCH', 'TAG_MISMATCH', 'TAG_CONTENT_UNTRANSLATED', 'PLACEHOLDER_MISMATCH',
            'UNRESTORED_PLACEHOLDER', 'MALFORMED_PLACEHOLDER', 'SPECIAL_CODE_MISMATCH',
            'PARENTHESES_MISMATCH', 'QUOTE_COUNT_MISMATCH',
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
    
    
    def _highlight_issues_in_text(self, text: str, issue_type: str) -> str:
        """Surligne les éléments problématiques selon le type d'erreur"""
        import re
        
        if not text:
            return text
        
        # Style de surlignage
        highlight_style = 'background: rgba(255, 193, 7, 0.3); padding: 2px 4px; border-radius: 3px; font-weight: 500;'
        
        if issue_type == 'VARIABLE_MISMATCH':
            # Surligner les variables [...]
            text = re.sub(r'(\[[^\]]*\])', r'<span style="' + highlight_style + r'">\1</span>', text)
        
        elif issue_type == 'TAG_MISMATCH':
            # Surligner les balises {...}
            text = re.sub(r'(\{[^}]*\})', r'<span style="' + highlight_style + r'">\1</span>', text)
        
        elif issue_type == 'QUOTES_MISMATCH':
            # Surligner tous les guillemets (", ', «, », ", ", ', \")
            # Utiliser les codes Unicode pour les guillemets courbes
            text = re.sub(r'(&quot;|&#39;|«|»|\u201c|\u201d|\u2018|\\&quot;)', r'<span style="' + highlight_style + r'">\1</span>', text)
        
        elif issue_type == 'PARENTHESES_MISMATCH':
            # Surligner les parenthèses
            text = re.sub(r'([\(\)])', r'<span style="' + highlight_style + r'">\1</span>', text)
        
        elif issue_type in ['PERCENTAGE_MISMATCH', 'PERCENTAGE_FORMAT_MISMATCH', 'DOUBLE_PERCENT_MISMATCH', 'ISOLATED_PERCENT_MISMATCH']:
            # Surligner les %
            text = re.sub(r'(%[sd%]?)', r'<span style="' + highlight_style + r'">\1</span>', text)
        
        elif issue_type == 'PLACEHOLDER_MISMATCH':
            # Surligner les placeholders (...)
            text = re.sub(r'(\([^)]*\))', r'<span style="' + highlight_style + r'">\1</span>', text)
        
        elif issue_type in ['ELLIPSIS_MISMATCH', 'DEEPL_ELLIPSIS_MISMATCH']:
            # Surligner les ellipses
            text = re.sub(r'(\.{2,}|…|\[…\]|\[\.\.\.\])', r'<span style="' + highlight_style + r'">\1</span>', text)
        
        elif issue_type == 'TAG_CONTENT_UNTRANSLATED':
            # Surligner le contenu non traduit dans les balises Ren'Py
            # Pattern : {tag}contenu{/tag} → surligner "contenu"
            # On capture les balises ouvrantes/fermantes et le contenu entre elles
            def highlight_tag_content(match):
                opening = match.group(1)  # {tag}
                content = match.group(2)   # contenu
                closing = match.group(3)   # {/tag}
                highlighted_content = f'<span style="{highlight_style}">{content}</span>'
                return f'{opening}{highlighted_content}{closing}'
            
            text = re.sub(r'(\{[a-z_]+[^}]*\})([^{]+)(\{/[a-z_]+\})', highlight_tag_content, text)
        
        return text
    
    def _generate_issue_item(self, issue: Dict) -> str:
        """Génère un élément d'erreur individuel avec édition en ligne"""
        line = int(issue.get('line', 0) or 0)
        file_path = issue.get('file_path', '') or ''
        description = _html.escape(issue.get('description', ''))
        old_content_raw = issue.get('old_content', '')
        new_content_raw = issue.get('new_content', '')
        old_content = _html.escape(old_content_raw)
        new_content = _html.escape(new_content_raw)
        issue_type = issue.get('type', '')
        
        # Préparer les versions échappées pour JavaScript (pour les boutons de copie)
        # json.dumps() échappe pour JS, mais pour les template literals on doit aussi échapper ` et ${}
        import json
        
        def escape_for_template_literal(text):
            """Échappe pour les template literals JavaScript (backticks) dans un attribut HTML"""
            # Les template literals acceptent tous les guillemets directement
            # MAIS comme le template literal est dans un attribut HTML onclick="...",
            # les guillemets doubles " cassent l'attribut HTML
            escaped = text
            # 1. Échapper les backslashes AVANT tout (sinon on échapperait nos propres échappements)
            escaped = escaped.replace('\\', '\\\\')
            # 2. Échapper les backticks
            escaped = escaped.replace('`', '\\`')
            # 3. Échapper les interpolations ${} (échapper le ${ ensemble)
            escaped = escaped.replace('${', '\\${')
            # 4. Échapper les guillemets doubles avec entité HTML (sinon ils ferment l'attribut onclick="...")
            escaped = escaped.replace('"', '&quot;')
            # 5. Échapper les retours à la ligne (template literals multi-lignes sont valides mais pas pratiques ici)
            escaped = escaped.replace('\n', '\\n')
            escaped = escaped.replace('\r', '\\r')
            escaped = escaped.replace('\t', '\\t')
            return escaped
        
        old_content_js_escaped = escape_for_template_literal(old_content_raw)
        new_content_js_escaped = escape_for_template_literal(new_content_raw)
        
        # Appliquer le surlignage si le type d'erreur le nécessite
        old_content_highlighted = self._highlight_issues_in_text(old_content, issue_type)
        new_content_highlighted = self._highlight_issues_in_text(new_content, issue_type)

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
        
        # Bouton toggle d'exclusion pour les types d'erreurs configurables
        # Note : Les placeholders ne sont PAS excludables (contrôle obligatoire critique)
        exclude_button_html = ''
        excludable_types = [
            # Groupe 1 : Détection de contenu
            'UNTRANSLATED_LINE',                      # coherence_check_untranslated
            'TAG_CONTENT_UNTRANSLATED',               # coherence_check_tags_content
            'DASH_TO_ELLIPSIS_TRANSFORMATION',        # coherence_check_ellipsis
            'ELLIPSIS_TO_DASH_TRANSFORMATION',        # coherence_check_ellipsis
            'PERCENTAGE_MISMATCH',                    # coherence_check_percentages
            'QUOTE_COUNT_MISMATCH',                   # coherence_check_quotations
            'QUOTES_MISMATCH',                        # coherence_check_quotations
            # Groupe 2 : Structure et syntaxe
            'PARENTHESES_MISMATCH',                   # coherence_check_parentheses
            'DEEPL_ELLIPSIS_MISMATCH',                # coherence_check_deepl_ellipsis
            'ISOLATED_PERCENT_MISMATCH',              # coherence_check_isolated_percent
            # Groupe 3 : Avertissements indicatifs
            'LENGTH_DIFFERENCE_WARNING'               # coherence_check_length_difference
        ]
        
        if issue_type in excludable_types:
            exclusion_key = issue.get('old_content', '')
            if exclusion_key:
                escaped_key = _html.escape(exclusion_key).replace('"', '&quot;')
                
                exclude_button_html = f"""
                    <button type="button" class="exclude-toggle-btn" 
                        data-exclusion-text="{escaped_key}"
                        data-exclusion-file="{escaped_file}"
                        data-exclusion-line="{line}"
                        style="padding: 8px 12px; border: 1px solid var(--sep); background: transparent; color: var(--fg); border-radius: 6px; cursor: pointer; font-size: 0.85rem; white-space: nowrap; transition: all 0.2s ease;"
                        title="Basculer l'état d'exclusion">
                        <span class="toggle-text-include">❌ Ignorer</span>
                        <span class="toggle-text-exclude">✅ Inclure</span>
                    </button>"""
        
        # 🆕 Interface d'édition en ligne (pour tous les types d'erreurs)
        # Pré-remplir avec le contenu NEW (la version traduite à corriger)
        edit_value = new_content_raw
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
                    {exclude_button_html}
                    <button type="button" class="paste-btn btn" id="paste-{unique_id}"
                        data-edit-field="editField-{unique_id}"
                        style="padding: 8px 12px; background: #6c757d; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 0.85rem; white-space: nowrap;"
                        title="Coller le contenu du presse-papier (remplace tout le texte)">
                        📋 Coller
                    </button>
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

        # Case à cocher "traduction en lot" pour lignes non traduites / contenu balise non traduit
        bulk_checkbox_html = ''
        if issue_type in ('UNTRANSLATED_LINE', 'TAG_CONTENT_UNTRANSLATED'):
            old_content_attr_escaped = _html.escape(old_content_raw).replace('"', '&quot;').replace('\n', ' ').replace('\r', ' ')
            bulk_checkbox_html = f'''
                    <div class="bulk-checkbox-wrap" style="margin-bottom: 8px;">
                        <label style="display: inline-flex; align-items: center; gap: 6px; cursor: pointer; font-size: 0.85rem;">
                            <input type="checkbox" class="bulk-checkbox" data-edit-field="editField-{unique_id}" data-file="{escaped_file}" data-line="{line}" data-old-content="{old_content_attr_escaped}" style="cursor: pointer;">
                            <span>Inclure dans traduction en lot</span>
                        </label>
                    </div>'''
        
        return f"""
        <div class="issue-item" data-unique-id="{unique_id}" data-issue-type="{issue_type}" id="issue-{unique_id}">
            <div class="issue-header" role="button" tabindex="0" aria-expanded="true" title="Cliquer pour ouvrir ou fermer">
                <span class="issue-toggle-icon" id="icon_issue_{unique_id}">▼</span>
                <div class="issue-line">Ligne {line}</div>
                {btn_html}
            </div>
            <div class="issue-item-content" id="content_issue_{unique_id}">
                <div class="issue-description">{description}</div>
                <div class="content-comparison">
                    <div class="content-block old-content">
                        <div class="content-label" style="display: flex; justify-content: space-between; align-items: center;">
                            <span>Ancien</span>
                            <button type="button" class="copy-btn btn" onclick="navigator.clipboard.writeText(`{old_content_js_escaped}`).then(() => {{ const btn = this; const orig = btn.innerHTML; btn.innerHTML = '✅ Copié'; setTimeout(() => btn.innerHTML = orig, 1500); }}).catch(() => {{ alert('Erreur lors de la copie'); }})" 
                                style="padding: 4px 8px; background: var(--info); color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.75rem;"
                                title="Copier le texte original">
                                📋 Copier
                            </button>
                        </div>
                        {bulk_checkbox_html}
                        <div>{old_content_highlighted if old_content_highlighted else '<em>Vide</em>'}</div>
                    </div>
                    <div class="content-block new-content">
                        <div class="content-label" style="display: flex; justify-content: space-between; align-items: center;">
                            <span>Nouveau</span>
                            <button type="button" class="copy-btn btn" onclick="navigator.clipboard.writeText(`{new_content_js_escaped}`).then(() => {{ const btn = this; const orig = btn.innerHTML; btn.innerHTML = '✅ Copié'; setTimeout(() => btn.innerHTML = orig, 1500); }}).catch(() => {{ alert('Erreur lors de la copie'); }})" 
                                style="padding: 4px 8px; background: var(--info); color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.75rem;"
                                title="Copier le texte traduit">
                                📋 Copier
                            </button>
                        </div>
                        <div>{new_content_highlighted if new_content_highlighted else '<em>Vide</em>'}</div>
                    </div>
                </div>
                {edit_interface_html}
            </div>
        </div>
        """

    
    def _get_error_type_display_name(self, error_type: str) -> str:
        """Retourne le nom d'affichage d'un type d'erreur"""
        type_names = {
            "VARIABLE_MISMATCH": "Variables [] incohérentes",
            "TAG_MISMATCH": "Balises {} incohérentes",
            "TAG_CONTENT_UNTRANSLATED": "Contenu de balise non traduit",
            "PLACEHOLDER_MISMATCH": "Placeholders () incohérents",
            "UNRESTORED_PLACEHOLDER": "Placeholders non restaurés",
            "MALFORMED_PLACEHOLDER": "Placeholder malformé",
            "SPECIAL_CODE_MISMATCH": "Codes spéciaux incohérents",
            "PARENTHESES_MISMATCH": "Parenthèses incohérentes",
            "QUOTE_COUNT_MISMATCH": "Nombre de guillemets différent",
            "UNTRANSLATED_LINE": "Ligne potentiellement non traduite",
            "MISSING_OLD": "Ligne ANCIENNE manquante",
            "CONTENT_PREFIX_MISMATCH": "Préfixe de contenu incohérent",
            "CONTENT_SUFFIX_MISMATCH": "Suffixe de contenu incohérent",
            "FILE_ERROR": "Erreur de fichier",
            "ANALYSIS_ERROR": "Erreur d'analyse",
            # Nouveaux types fusionnés
            "QUOTES_MISMATCH": "Guillemets incohérents",
            "PERCENTAGE_MISMATCH": "Pourcentages incohérents",
            # Anciens types (compatibilité)
            "ESCAPED_QUOTES_MISMATCH": "Guillemets échappés incohérents",
            "UNESCAPED_QUOTES_MISMATCH": "Guillemets non échappés incohérents",
            "PERCENTAGE_FORMAT_MISMATCH": "Variables % incohérentes",
            "DOUBLE_PERCENT_MISMATCH": "Double % incohérent",
            # Avertissements indicatifs
            "LENGTH_DIFFERENCE_WARNING": "Différence de longueur importante"
        }
        return type_names.get(error_type, error_type.replace('_', ' ').title())
    
    def _get_error_type_icon(self, error_type: str) -> str:
        """Retourne l'icône d'un type d'erreur"""
        icons = {
            "VARIABLE_MISMATCH": "🔤",
            "TAG_MISMATCH": "🏷️",
            "TAG_CONTENT_UNTRANSLATED": "🔖",
            "PLACEHOLDER_MISMATCH": "📝",
            "UNRESTORED_PLACEHOLDER": "🔄",
            "MALFORMED_PLACEHOLDER": "⚠️",
            "SPECIAL_CODE_MISMATCH": "💻",
            "PARENTHESES_MISMATCH": "〔〕",
            "QUOTE_COUNT_MISMATCH": "\"\"",
            "UNTRANSLATED_LINE": "🌐",
            "MISSING_OLD": "❌",
            "CONTENT_PREFIX_MISMATCH": "⬅️",
            "CONTENT_SUFFIX_MISMATCH": "➡️",
            "FILE_ERROR": "💥",
            "ANALYSIS_ERROR": "🐛",
            # Nouveaux types fusionnés
            "QUOTES_MISMATCH": "\"\"",
            "PERCENTAGE_MISMATCH": "%%",
            # Avertissements indicatifs
            "LENGTH_DIFFERENCE_WARNING": "📏"
        }
        return icons.get(error_type, "⚠️")
    
    def _get_error_type_css_class(self, error_type: str) -> str:
        """Retourne la classe CSS pour un type d'erreur"""
        classes = {
            "VARIABLE_MISMATCH": "badge-variable",
            "TAG_MISMATCH": "badge-tag",
            "TAG_CONTENT_UNTRANSLATED": "badge-untranslated",
            "PLACEHOLDER_MISMATCH": "badge-placeholder",
            "UNRESTORED_PLACEHOLDER": "badge-placeholder",
            "MALFORMED_PLACEHOLDER": "badge-placeholder",
            "SPECIAL_CODE_MISMATCH": "badge-special",
            "PARENTHESES_MISMATCH": "badge-special",
            "QUOTE_COUNT_MISMATCH": "badge-special",
            "UNTRANSLATED_LINE": "badge-untranslated",
            "MISSING_OLD": "badge-other",
            "CONTENT_PREFIX_MISMATCH": "badge-other",
            "CONTENT_SUFFIX_MISMATCH": "badge-other",
            "FILE_ERROR": "badge-other",
            "ANALYSIS_ERROR": "badge-other",
            # Nouveaux types fusionnés
            "QUOTES_MISMATCH": "badge-special",
            "PERCENTAGE_MISMATCH": "badge-special",
            # Avertissements indicatifs
            "LENGTH_DIFFERENCE_WARNING": "badge-info"
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
        """
        Retourne le chemin relatif du fichier depuis le dossier tl
        NORMALISÉ pour garantir la cohérence entre rapports globaux et reconstruction
        """
        try:
            # Normaliser les séparateurs de chemin d'abord
            normalized_path = file_path.replace('\\', '/')
            
            # Trouver la position de 'tl/' dans le chemin
            if '/tl/' in normalized_path:
                parts = normalized_path.split('/tl/')
                if len(parts) > 1:
                    # Retourner ce qui est après tl/langue/
                    sub_parts = parts[1].split('/', 1)
                    if len(sub_parts) > 1:
                        # Format final: "script.rpy" ou "subfolder/script.rpy"
                        return sub_parts[1]
                    else:
                        # Si pas de sous-dossier, retourner juste le nom de fichier
                        return os.path.basename(normalized_path)
            
            # Si 'tl/' n'est pas trouvé mais le chemin contient 'game/'
            if '/game/' in normalized_path:
                # Extraire depuis game/ (cas reconstruction)
                parts = normalized_path.split('/game/')
                if len(parts) > 1:
                    game_relative = parts[1]
                    # Si ça commence par tl/langue/, extraire la partie après
                    if game_relative.startswith('tl/'):
                        sub_parts = game_relative.split('/', 2)
                        if len(sub_parts) > 2:
                            return sub_parts[2]
            
            # Fallback: retourner le nom du fichier uniquement
            return os.path.basename(normalized_path)
        except Exception as e:
            from infrastructure.logging.logging import log_message
            log_message("DEBUG", f"Erreur normalisation chemin '{file_path}': {e}", category="report")
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