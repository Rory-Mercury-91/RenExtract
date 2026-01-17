# utils/html_report_generator.py
# Générateur de rapports HTML interactifs pour le nettoyage - VERSION HARMONISÉE

import os
import json
import html as _html
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from infrastructure.helpers.unified_functions import extract_game_name

class HtmlCleanupReportGenerator:
    """Générateur de rapports HTML interactifs pour le nettoyage des traductions"""
    
    def __init__(self):
        self.report_dir = self._get_report_directory()
        self._ensure_report_directory()
    
    def _get_report_directory(self) -> str:
        """Détermine le répertoire de rapports de nettoyage"""
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
        """Retourne les styles CSS harmonisés pour le rapport"""
        return """
        <style>
          :root {
            --bg: #1a1f29; --fg: #e2e8f0; --hdr: #2d3748; --sep: #4a5568;
            --success: #48bb78; --warning: #ed8936; --danger: #f56565; --info: #4a90e2;
            --card-bg: #2d3748; --hover-bg: rgba(255,255,255,0.06); --nav-bg: #1a202c;
            --button-utility-bg: #6f42c1; --button-copy-success: #48bb78;
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
            position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
            position: sticky; top: 82px; z-index: 95;
            border-bottom: 1px solid var(--sep);
          }
          
          .card {
            background: var(--card-bg); border: 1px solid var(--sep); 
            border-radius: 12px; padding: 20px; transition: transform 0.2s;
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
            height: 100%; background: var(--success); 
            transition: width 0.3s ease;
          }
          
          .language-section {
            margin: 20px; background: var(--card-bg); border-radius: 12px;
            border: 1px solid var(--sep); overflow: hidden; transition: all 0.2s;
          }
          .language-section:hover { transform: translateY(-1px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
          
          .language-header {
            background: var(--hdr); padding: 15px 20px; font-weight: bold;
            cursor: pointer; user-select: none;
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid var(--sep);
          }
          
          .language-content { padding: 20px; display: none; }
          .language-content.expanded { display: block; }
          
          .file-list { margin-top: 15px; }
          .file-item {
            background: var(--bg); border: 1px solid var(--sep); 
            border-radius: 8px; margin: 8px 0; padding: 12px;
            transition: background 0.2s;
          }
          .file-item:hover { background: var(--hover-bg); }
          
          .file-header {
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 10px;
          }
          
          .file-name { font-weight: bold; color: var(--info); }
          
          .open-file-btn {
            padding: 4px 8px; border: 1px solid var(--sep);
            background: var(--button-utility-bg); color: white;
            border-radius: 4px; cursor: pointer; font-size: 0.8rem;
            transition: all 0.2s;
          }
          .open-file-btn:hover { 
            background: #5a2d91; transform: translateY(-1px); 
          }
          
          .block-details { margin-top: 15px; font-size: 0.9rem; }
          
          .copyable-block {
            position: relative; border: 1px solid var(--sep);
            border-radius: 6px; margin: 8px 0; background: var(--card-bg);
            overflow: hidden;
          }
          
          .block-header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 8px 12px; background: var(--hdr);
            border-bottom: 1px solid var(--sep);
          }
          
          .copy-btn {
            padding: 4px 8px; border: 1px solid var(--sep);
            background: var(--button-utility-bg); color: white;
            border-radius: 4px; cursor: pointer; font-size: 0.8rem;
            transition: all 0.2s; user-select: none;
          }
          .copy-btn:hover { background: #5a2d91; }
          .copy-btn.copied { background: var(--button-copy-success); }
          
          .block-content {
            padding: 12px; font-family: 'Consolas', 'Monaco', monospace;
            background: var(--bg); font-size: 0.9rem; line-height: 1.4;
          }
          
          .old-text { color: #ff6b6b; margin-bottom: 4px; }
          .new-text { color: #51cf66; }
          
          .filters {
            padding: 15px 20px; background: var(--hdr); 
            border: 1px solid var(--sep); border-radius: 12px;
            display: flex; gap: 15px; align-items: center; flex-wrap: wrap;
            position: sticky; top: 290px; z-index: 90;
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
          
          .badge {
            padding: 4px 8px; border-radius: 12px; font-size: 0.8rem; font-weight: bold;
          }
          .badge-success { background: var(--success); color: white; }
          .badge-warning { background: var(--warning); color: black; }
          .badge-danger { background: var(--danger); color: white; }
          .badge-info { background: var(--info); color: white; }
          
          .collapsible-toggle::after {
            content: "▼"; transition: transform 0.2s; font-size: 0.8rem;
          }
          .collapsible-toggle.collapsed::after {
            transform: rotate(-90deg);
          }
          
          .reset-filters-btn {
            margin-left: auto; background: var(--danger); color: white;
            border: none; padding: 6px 12px; border-radius: 6px;
            cursor: pointer; font-size: 0.9rem; transition: all 0.2s;
          }
          .reset-filters-btn:hover { 
            background: #b02a37; transform: translateY(-1px); 
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
          }
        </style>
        """
    
    def _get_javascript(self) -> str:
        """JavaScript harmonisé avec filtrage par dropdown uniquement"""
        # Résoudre l'URL du serveur d'édition depuis la configuration
        try:
            from infrastructure.config.config import config_manager
            server_port = int(config_manager.get('editor_server_port', 8765))
        except Exception:
            server_port = 8765
        server_url = f"http://127.0.0.1:{server_port}"

        js_template = """
        <script>
        (function() {
            // URL du serveur d'édition (configurable)
            window.RENEXTRACT_SERVER_URL = '{SERVER_URL}';

            // Gestion du thème
            const savedTheme = localStorage.getItem('renextract_report_theme') || 'dark';
            if (savedTheme === 'light') document.body.classList.add('light');
            
            function toggleTheme() {
                const isLight = document.body.classList.toggle('light');
                localStorage.setItem('renextract_report_theme', isLight ? 'light' : 'dark');
                document.getElementById('themeBtn').textContent = 
                    'Thème: ' + (isLight ? 'Clair' : 'Sombre');
            }
            
            // Fonction pour copier un bloc
            window.copyBlock = function(blockId) {
                const element = document.getElementById(blockId);
                if (!element) return;
                
                const btn = element.parentElement.querySelector('.copy-btn');
                
                // Récupérer le texte old et new depuis les éléments
                const oldTextElement = element.querySelector('.old-text');
                const newTextElement = element.querySelector('.new-text');
                
                let text;
                if (oldTextElement && newTextElement) {
                    // Extraire le texte sans les préfixes "old" et "new"
                    const oldText = oldTextElement.textContent.replace(/^old\\s+"(.*)"$/, '$1');
                    const newText = newTextElement.textContent.replace(/^new\\s+"(.*)"$/, '$1');
                    
                    // Formater avec l'indentation correcte
                    text = `    old "${oldText}"\\n    new "${newText}"`;
                } else {
                    text = element.textContent.trim();
                }
                
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(text).then(() => {
                        showCopySuccess(btn);
                    }).catch(() => {
                        fallbackCopy(text, btn);
                    });
                } else {
                    fallbackCopy(text, btn);
                }
            };
            
            function showCopySuccess(btn) {
                const originalText = btn.textContent;
                btn.textContent = '✅ Copié !';
                btn.classList.add('copied');
                
                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.classList.remove('copied');
                }, 2000);
            }
            
            function fallbackCopy(text, btn) {
                const textarea = document.createElement('textarea');
                textarea.value = text;
                document.body.appendChild(textarea);
                textarea.select();
                try {
                    document.execCommand('copy');
                    showCopySuccess(btn);
                } catch {
                    alert('Impossible de copier automatiquement. Sélectionnez et copiez manuellement.');
                }
                document.body.removeChild(textarea);
            }
            
            // Fonction pour ouvrir dans l'éditeur
            window.openInEditor = function(filePath, lineNumber) {
                const url = `${window.RENEXTRACT_SERVER_URL}/open?file=${encodeURIComponent(filePath)}&line=${encodeURIComponent(lineNumber)}`;

                // Essaye le serveur local d'abord
                fetch(url, { method: 'GET' })
                    .then(async (res) => {
                        if (!res.ok) throw new Error('HTTP ' + res.status);
                        const data = await res.json().catch(() => ({}));
                        const msg = data && (data.message || (data.ok ? "Ouvert dans l'éditeur." : 'Requête envoyée.'));
                        if (msg) {
                            console.log(msg);
                        } else {
                            console.log('Ouverture demandée au gestionnaire local.');
                        }
                    })
                    .catch(() => {
                        // Fallback: copie "fichier:ligne" dans le presse-papiers + instructions
                        const textToCopy = `${filePath}:${lineNumber}`;
                        if (navigator.clipboard && navigator.clipboard.writeText) {
                            navigator.clipboard.writeText(textToCopy).then(() => {
                                alert(
        `Le serveur local n'est pas joignable.
        J'ai copié: ${textToCopy}
        Ouvre ton éditeur et fais "Go to Line".
        • VSCode: Ctrl+G
        • Notepad++: Ctrl+G
        • Sublime: Ctrl+G`
                                );
                            }).catch(() => {
                                prompt('Copiez ce chemin manuellement:', textToCopy);
                            });
                        } else {
                            prompt('Copiez ce chemin manuellement:', textToCopy);
                        }
                    });
            };
            
            // Fonction de réinitialisation des filtres
            function resetAllFilters() {
                const languageFilter = document.getElementById('languageFilter');
                const fileFilter = document.getElementById('fileFilter');
                
                if (languageFilter) languageFilter.value = 'all';
                if (fileFilter) fileFilter.value = 'all';
                
                // Réappliquer les filtres pour tout afficher
                applyFilters();
            }
            
            // Fonction de filtrage harmonisée
            function applyFilters() {
                const selectedLang = document.getElementById('languageFilter')?.value || 'all';
                const selectedFile = document.getElementById('fileFilter')?.value || 'all';
                
                let visibleSections = 0;
                let totalVisibleFiles = 0;
                
                document.querySelectorAll('.language-section').forEach(section => {
                    const langName = section.dataset.language;
                    let showSection = selectedLang === 'all' || langName === selectedLang;
                    
                    if (showSection) {
                        // Compter et filtrer les fichiers dans cette section
                        const fileItems = section.querySelectorAll('.file-item');
                        let visibleFilesInSection = 0;
                        
                        fileItems.forEach(fileItem => {
                            const fileNameElement = fileItem.querySelector('.file-name');
                            if (fileNameElement) {
                                const fileName = fileNameElement.textContent.replace('📄 ', '').trim();
                                
                                // Appliquer le filtre de fichier
                                const fileMatches = selectedFile === 'all' || fileName === selectedFile;
                                
                                if (fileMatches) {
                                    fileItem.style.display = 'block';
                                    visibleFilesInSection++;
                                } else {
                                    fileItem.style.display = 'none';
                                }
                            }
                        });
                        
                        // Afficher la section seulement si elle a des fichiers visibles
                        showSection = visibleFilesInSection > 0;
                        totalVisibleFiles += visibleFilesInSection;
                    }
                    
                    section.style.display = showSection ? 'block' : 'none';
                    if (showSection) visibleSections++;
                });
                
                // Mettre à jour les statistiques de filtrage
                updateFilterStats(visibleSections, totalVisibleFiles);
            }
            
            function updateFilterStats(sections, files) {
                const filterInfo = document.getElementById('filterInfo');
                if (filterInfo) {
                    filterInfo.textContent = `${sections} langue(s), ${files} fichier(s) visible(s)`;
                }
            }
            
            // Initialisation DOM
            document.addEventListener('DOMContentLoaded', function() {
                // Délégation d'événements pour les boutons d'ouverture de fichier
                document.body.addEventListener('click', function(e) {
                    const btn = e.target.closest('.open-file-btn');
                    if (!btn) return;
                    
                    const filePath = btn.getAttribute('data-file');
                    const lineNumber = btn.getAttribute('data-line') || '1';
                    
                    if (filePath) {
                        window.openInEditor(filePath, lineNumber);
                    }
                });
                
                const themeBtn = document.getElementById('themeBtn');
                if (themeBtn) {
                    themeBtn.textContent = 'Thème: ' + (savedTheme === 'light' ? 'Clair' : 'Sombre');
                    themeBtn.addEventListener('click', toggleTheme);
                }
                
                // Sections collapsibles
                document.querySelectorAll('.language-header').forEach(header => {
                    header.addEventListener('click', function() {
                        const content = this.nextElementSibling;
                        const toggle = this.querySelector('.collapsible-toggle');
                        
                        content.classList.toggle('expanded');
                        toggle.classList.toggle('collapsed');
                    });
                });
                
                // Filtres harmonisés
                const languageFilter = document.getElementById('languageFilter');
                const fileFilter = document.getElementById('fileFilter');
                const resetBtn = document.getElementById('resetFilters');
                
                if (languageFilter) languageFilter.addEventListener('change', applyFilters);
                if (fileFilter) fileFilter.addEventListener('change', applyFilters);
                if (resetBtn) resetBtn.addEventListener('click', resetAllFilters);
                
                // Expand all / Collapse all
                document.getElementById('expandAll')?.addEventListener('click', function() {
                    document.querySelectorAll('.language-content').forEach(content => {
                        content.classList.add('expanded');
                    });
                    document.querySelectorAll('.collapsible-toggle').forEach(toggle => {
                        toggle.classList.remove('collapsed');
                    });
                });
                
                document.getElementById('collapseAll')?.addEventListener('click', function() {
                    document.querySelectorAll('.language-content').forEach(content => {
                        content.classList.remove('expanded');
                    });
                    document.querySelectorAll('.collapsible-toggle').forEach(toggle => {
                        toggle.classList.add('collapsed');
                    });
                });
                
                // Initialiser les statistiques
                applyFilters();
            });
        })();
        </script>
        """
        
        return js_template.replace('{SERVER_URL}', server_url)
    
    def generate_cleanup_report(self, results: Dict[str, Any], project_path: str, 
                            execution_time: str) -> Optional[str]:
        """Génère un rapport HTML interactif pour le nettoyage"""
        try:
            # Nom du jeu et timestamp
            game_name = os.path.basename(project_path) if project_path else "Unknown"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Créer la structure hiérarchique complète
            report_type_folder = os.path.join(self.report_dir, game_name, "nettoyage")
            os.makedirs(report_type_folder, exist_ok=True)
            
            # Chemin du rapport dans la bonne structure
            report_name = f"{game_name}_nettoyage_interactif_{timestamp}.html"
            report_path = os.path.join(report_type_folder, report_name)
            
            with open(report_path, 'w', encoding='utf-8') as f:
                # En-tête HTML
                f.write(self._generate_html_header(game_name, results, execution_time))
                
                # Contenu principal
                f.write(self._generate_summary_section(results))
                f.write(self._generate_filters_section(results))
                f.write(self._generate_languages_sections(results))
                
                # Pied de page
                f.write(self._generate_footer())
                
                # Scripts
                f.write(self._get_javascript())
                f.write("</body></html>")
            
            return report_path
            
        except Exception as e:
            return None
    
    def _generate_html_header(self, game_name: str, results: Dict[str, Any], 
                            execution_time: str) -> str:
        """Génère l'en-tête HTML du rapport"""
        title = f"Rapport de Nettoyage - {game_name}"
        current_time = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")
        
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
                <h1>🧹 Rapport de Nettoyage RenExtract</h1>
                <div class="header-meta">
                    <span>🎮 <strong>{_html.escape(game_name)}</strong></span>
                    <span>📅 {current_time}</span>
                    <span>⏱️ Temps: {_html.escape(execution_time)}</span>
                    <span>🌍 Langues: {results.get('total_languages_processed', 0)}</span>
                    <span>📄 Fichiers: {results.get('total_files_processed', 0)}</span>
                    <span>🗑️ Blocs supprimés: {results.get('total_orphan_blocks_removed', 0)}</span>
                    
                    <div class="controls">
                        <button id="expandAll" class="btn">Tout déplier</button>
                        <button id="collapseAll" class="btn">Tout replier</button>
                        <button id="themeBtn" class="btn">Thème: Sombre</button>
                    </div>
                </div>
            </div>
        """
    
    def _generate_summary_section(self, results: Dict[str, Any]) -> str:
        """Génère la section de résumé"""
        summary = results.get('summary', {})
        lint_cleanup = summary.get('lint_cleanup', {})
        string_cleanup = summary.get('string_cleanup', {})
        
        total_blocks = results.get('total_orphan_blocks_removed', 0)
        lint_blocks = lint_cleanup.get('blocks_removed', 0)
        string_blocks = string_cleanup.get('blocks_removed', 0)
        
        # Calculer les commentaires orphelins depuis les résultats des langues
        orphan_comments = 0
        for lang_result in results.get('language_results', {}).values():
            orphan_comments += lang_result.get('orphan_comments_cleanup', {}).get('total_orphan_blocks_removed', 0)
        
        # Calcul des pourcentages
        lint_percent = (lint_blocks / total_blocks * 100) if total_blocks > 0 else 0
        string_percent = (string_blocks / total_blocks * 100) if total_blocks > 0 else 0
        comments_percent = (orphan_comments / total_blocks * 100) if total_blocks > 0 else 0
        
        return f"""
        <div class="summary-cards">
            <div class="card">
                <h3>📊 Résumé Global</h3>
                <div class="stat">
                    <span>Langues traitées</span>
                    <span class="stat-value">{results.get('total_languages_processed', 0)}</span>
                </div>
                <div class="stat">
                    <span>Fichiers traités</span>
                    <span class="stat-value">{results.get('total_files_processed', 0)}</span>
                </div>
                <div class="stat">
                    <span>Blocs supprimés</span>
                    <span class="stat-value">{total_blocks}</span>
                </div>
            </div>
            
            <div class="card">
                <h3>🔍 Nettoyage par LINT</h3>
                <div class="stat">
                    <span>Blocs supprimés</span>
                    <span class="stat-value">{lint_blocks}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {lint_percent:.1f}%"></div>
                </div>
                <small>{lint_percent:.1f}% du total</small>
            </div>
            
            <div class="card">
                <h3>🔗 Nettoyage par Correspondance</h3>
                <div class="stat">
                    <span>Blocs supprimés</span>
                    <span class="stat-value">{string_blocks}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {string_percent:.1f}%"></div>
                </div>
                <small>{string_percent:.1f}% du total</small>
            </div>
            
            <div class="card">
                <h3>💬 Nettoyage des Commentaires Orphelins</h3>
                <div class="stat">
                    <span>Commentaires supprimés</span>
                    <span class="stat-value">{orphan_comments}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {comments_percent:.1f}%"></div>
                </div>
                <small>{comments_percent:.1f}% du total</small>
            </div>
        </div>
        """
    
    def _generate_filters_section(self, results: Dict[str, Any]) -> str:
        """Génère la section des filtres harmonisée avec dropdown de fichiers"""
        languages = list(results.get('language_results', {}).keys())
        
        language_options = ''.join([
            f'<option value="{lang}">{lang.upper()}</option>' 
            for lang in sorted(languages)
        ])
        
        # Extraire tous les fichiers traités pour la dropdown
        all_files = set()
        for lang_result in results.get('language_results', {}).values():
            for file_result in lang_result.get('file_results', []):
                file_path = file_result.get('file_path', '')
                if file_path:
                    file_name = os.path.basename(file_path)
                    all_files.add(file_name)
        
        # Créer les options de fichiers triées
        file_options = ''.join([
            f'<option value="{file_name}">{file_name}</option>' 
            for file_name in sorted(all_files)
        ])
        
        return f"""
        <div class="filters">
            <div class="filter-group">
                <label for="languageFilter">Langue :</label>
                <select id="languageFilter">
                    <option value="all">Toutes les langues</option>
                    {language_options}
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
    
    def _generate_languages_sections(self, results: Dict[str, Any]) -> str:
        """Génère les sections détaillées par langue"""
        html = ""
        
        for language, lang_result in results.get('language_results', {}).items():
            html += self._generate_language_section(language, lang_result)
        
        return html
    
    def _generate_language_section(self, language: str, lang_result: Dict[str, Any]) -> str:
        """Génère une section pour une langue spécifique"""
        total_removed = lang_result.get('total_blocks_removed', 0)
        files_processed = lang_result.get('files_processed', 0)
        
        # Badges de statut
        badges = []
        if lang_result.get('lint_cleanup', {}).get('total_orphan_blocks_removed', 0) > 0:
            badges.append('<span class="badge badge-warning">LINT</span>')
        if lang_result.get('string_cleanup', {}).get('total_orphan_blocks_removed', 0) > 0:
            badges.append('<span class="badge badge-danger">STRING</span>')
        if lang_result.get('orphan_comments_cleanup', {}).get('total_orphan_blocks_removed', 0) > 0:
            badges.append('<span class="badge badge-info">COMMENTS</span>')
        
        badges_html = ' '.join(badges) if badges else '<span class="badge badge-success">Aucune suppression</span>'
        
        # Contenu détaillé des fichiers
        files_content = self._generate_files_content(lang_result.get('file_results', []))
        
        return f"""
        <div class="language-section" data-language="{language}">
            <div class="language-header">
                <div>
                    <span class="collapsible-toggle collapsed"></span>
                    🌍 <strong>{language.upper()}</strong>
                    <small style="margin-left: 10px;">
                        {files_processed} fichiers • {total_removed} blocs supprimés
                    </small>
                </div>
                <div>{badges_html}</div>
            </div>
            
            <div class="language-content">
                {files_content}
            </div>
        </div>
        """
    
    def _generate_files_content(self, file_results: List[Dict[str, Any]]) -> str:
        """Génère le contenu détaillé des fichiers"""
        if not file_results:
            return "<p>Aucun fichier traité.</p>"
        
        html = "<div class='file-list'>"
        
        for file_result in file_results:
            file_path = file_result.get('file_path', '')
            file_name = os.path.basename(file_path)
            
            total_blocks = file_result.get('total_blocks_removed', 0)
            lint_blocks = file_result.get('lint_blocks_removed', 0)
            string_blocks = file_result.get('string_blocks_removed', 0)
            
            if total_blocks == 0:
                continue
            
            # Bouton pour ouvrir le fichier
            open_file_btn = f"""
            <button class='open-file-btn' 
                    data-file="{_html.escape(file_path)}" 
                    data-line="1" 
                    title='Ouvrir le fichier'>
                🔍 Ouvrir le fichier
            </button>
            """ if file_path else ""         
            
            # Détails des blocs string supprimés
            string_details = ""
            if file_result.get('string_blocks_details'):
                string_details = "<div class='block-details'>"
                string_details += "<strong>Blocs supprimés par correspondance :</strong>"
                
                for i, detail in enumerate(file_result['string_blocks_details']):
                    # Créer un ID unique pour ce bloc
                    safe_file_path = file_path.replace('/', '_').replace('\\', '_').replace(':', '_')
                    block_id = f"block_{safe_file_path}_{i}"
                    
                    # Utiliser les lignes complètes avec indentation préservée
                    if 'block_lines' in detail and detail['block_lines']:
                        formatted_content = "\\n".join(detail['block_lines'])
                    else:
                        # Fallback si block_lines n'est pas disponible
                        formatted_content = f"    old \"{detail['old_text']}\"\\n    new \"{detail['new_text']}\""
                    string_details += f"""
                    <div class='copyable-block'>
                        <div class='block-header'>
                            <span>Ligne {detail['line_number']}</span>
                            <button class='copy-btn' onclick='copyBlock("{block_id}")' title='Copier le bloc'>
                                📋 Copier
                            </button>
                        </div>
                        <div class='block-content' id='{block_id}' data-formatted-text="{_html.escape(formatted_content)}">
                            <div class='old-text'>old "{_html.escape(detail['old_text'])}"</div>
                            <div class='new-text'>new "{_html.escape(detail['new_text'])}"</div>
                        </div>
                    </div>
                    """
                
                string_details += "</div>"
            
            html += f"""
            <div class='file-item'>
                <div class='file-header'>
                    <div class='file-name'>📄 {_html.escape(file_name)}</div>
                    {open_file_btn}
                </div>
                <div style='margin-top: 8px;'>
                    <span class='badge badge-info'>Total: {total_blocks}</span>
                    {f'<span class="badge badge-warning">LINT: {lint_blocks}</span>' if lint_blocks > 0 else ''}
                    {f'<span class="badge badge-danger">STRING: {string_blocks}</span>' if string_blocks > 0 else ''}
                </div>
                {string_details}
            </div>
            """
        
        html += "</div>"
        return html
    
    def _generate_footer(self) -> str:
        """Génère le pied de page"""
        return """
        <div style="text-align: center; padding: 40px 20px; opacity: 0.7; border-top: 1px solid var(--sep);">
            <p>✨ Rapport généré automatiquement par RenExtract</p>
            <p>🔧 Outil de nettoyage intelligent des traductions Ren'Py</p>
        </div>
        """


# Fonction utilitaire pour l'intégration
def create_html_cleanup_report(results: Dict[str, Any], project_path: str, 
                             execution_time: str) -> Optional[str]:
    """
    Fonction utilitaire pour créer un rapport HTML de nettoyage
    
    Args:
        results: Résultats du nettoyage
        project_path: Chemin du projet 
        execution_time: Temps d'exécution formaté
        
    Returns:
        Chemin du rapport généré ou None
    """
    generator = HtmlCleanupReportGenerator()
    return generator.generate_cleanup_report(results, project_path, execution_time)
