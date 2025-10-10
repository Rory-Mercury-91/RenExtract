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
            --bg: #121212; --fg: #eaeaea; --hdr: #1e1e1e; --sep: #262626;
            --success: #198754; --warning: #FFC107; --danger: #DC3545; --info: #0D6EFD;
            --card-bg: #1f1f1f; --hover-bg: rgba(255,255,255,0.06);
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
            transition: background 0.2s;
          }
          .issue-item:hover { background: var(--hover-bg); }
          .issue-item:last-child { border-bottom: none; }
          
          .open-in-editor {
              display: inline-flex; align-items: center; gap: 6px;
              font-size: 12px; padding: 6px 10px; border-radius: 6px;
              border: 1px solid var(--sep); background: rgba(13,110,253,0.12);
              cursor: pointer; user-select: none;
              color: var(--fg); /* Utilise la couleur de texte du thème */
          }
          .open-in-editor:hover { 
              background: rgba(13,110,253,0.18); 
              color: var(--fg); /* Maintient la couleur au survol */
          }
          .open-in-editor svg { 
              width: 14px; height: 14px; opacity: 0.9; 
              color: inherit; /* L'icône hérite de la couleur du texte */
          }
          .issue-line { font-weight: bold; color: var(--warning); margin-bottom: 8px; }
          .issue-description { margin-bottom: 12px; color: var(--fg); }
          
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
          
          .collapsible-toggle::after {
            content: "▼"; transition: transform 0.2s; font-size: 0.8rem;
          }
          .collapsible-toggle.collapsed::after {
            transform: rotate(-90deg);
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
        </style>
        """
    
    def _get_javascript_harmonized(self, selection_info: Dict[str, Any]) -> str:
        """JavaScript harmonisé SANS recherche textuelle + avec bouton reset"""
        
        # Préparer les données de sélection pour JavaScript
        is_all_files = selection_info.get('is_all_files', True)
        language = selection_info.get('language', '')
        selected_file = selection_info.get('selected_option', '')
        total_files = len(selection_info.get('target_files', []))
        
        return f"""
        <script>
        (function() {{
            // Informations sur la sélection harmonisée
            window.coherenceSelectionInfo = {{
                isAllFiles: {str(is_all_files).lower()},
                language: '{language}',
                selectedFile: '{selected_file}',
                totalFiles: {total_files}
            }};
            
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
                const url = `http://127.0.0.1:8765/open?file=${{encodeURIComponent(filePath)}}&line=${{encodeURIComponent(lineNumber)}}`;

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
            
            // Fonction de réinitialisation des filtres
            function resetAllFilters() {{
                const errorTypeFilter = document.getElementById('errorTypeFilter');
                const fileFilter = document.getElementById('fileFilter');
                
                if (errorTypeFilter) errorTypeFilter.value = 'all';
                if (fileFilter) fileFilter.value = 'all';
                
                // Réappliquer les filtres pour tout afficher
                applyFilters();
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

            // Initialisation
            document.addEventListener('DOMContentLoaded', function() {{
                // Délégation: clic sur boutons "open in editor"
                document.body.addEventListener('click', function(e) {{
                    const btn = e.target.closest('.open-in-editor');
                    if (!btn) return;
                    const f = btn.getAttribute('data-file');
                    const l = parseInt(btn.getAttribute('data-line') || '0', 10) || 0;
                    if (f && l) window.openInEditor(f, l);
                }});

                // Bouton thème
                const themeBtn = document.getElementById('themeBtn');
                if (themeBtn) {{
                    themeBtn.textContent = 'Thème: ' + (savedTheme === 'light' ? 'Clair' : 'Sombre');
                    themeBtn.addEventListener('click', toggleTheme);
                }}

                // Sections repliables
                document.querySelectorAll('.error-type-header').forEach(header => {{
                    header.addEventListener('click', function() {{
                        const content = this.nextElementSibling;
                        const toggle = this.querySelector('.collapsible-toggle');
                        if (!content) return;
                        content.classList.toggle('expanded');
                        if (toggle) toggle.classList.toggle('collapsed');
                    }});
                }});

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

                if (errorTypeFilter) errorTypeFilter.addEventListener('change', applyFilters);
                if (fileFilter) fileFilter.addEventListener('change', applyFilters);
                if (resetBtn) resetBtn.addEventListener('click', resetAllFilters);

                // Tout déplier / Tout replier
                const expandAllBtn = document.getElementById('expandAll');
                if (expandAllBtn) {{
                    expandAllBtn.addEventListener('click', function() {{
                        document.querySelectorAll('.error-type-content').forEach(content => {{
                            content.classList.add('expanded');
                        }});
                        document.querySelectorAll('.collapsible-toggle').forEach(toggle => {{
                            toggle.classList.remove('collapsed');
                        }});
                    }});
                }}

                const collapseAllBtn = document.getElementById('collapseAll');
                if (collapseAllBtn) {{
                    collapseAllBtn.addEventListener('click', function() {{
                        document.querySelectorAll('.error-type-content').forEach(content => {{
                            content.classList.remove('expanded');
                        }});
                        document.querySelectorAll('.collapsible-toggle').forEach(toggle => {{
                            toggle.classList.add('collapsed');
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

    def _get_javascript(self) -> str:
        """Retourne le JavaScript pour l'interactivité du rapport de cohérence"""
        return """
        <script>
        (function() {
            // Gestion du thème
            const savedTheme = localStorage.getItem('renextract_coherence_theme') || 'dark';
            if (savedTheme === 'light') document.body.classList.add('light');

            function toggleTheme() {
                const isLight = document.body.classList.toggle('light');
                localStorage.setItem('renextract_coherence_theme', isLight ? 'light' : 'dark');
                const themeBtn = document.getElementById('themeBtn');
                if (themeBtn) {
                    themeBtn.textContent = 'Thème: ' + (isLight ? 'Clair' : 'Sombre');
                }
            }

            // Fonction pour ouvrir dans l'éditeur
            window.openInEditor = function(filePath, lineNumber) {
                const url = `http://127.0.0.1:8765/open?file=${encodeURIComponent(filePath)}&line=${encodeURIComponent(lineNumber)}`;

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

            // Initialisation
            document.addEventListener('DOMContentLoaded', function() {
                // Délégation: clic sur boutons "open in editor"
                document.body.addEventListener('click', function(e) {
                    const btn = e.target.closest('.open-in-editor');
                    if (!btn) return;
                    const f = btn.getAttribute('data-file');
                    const l = parseInt(btn.getAttribute('data-line') || '0', 10) || 0;
                    if (f && l) window.openInEditor(f, l);
                });

                // Bouton thème
                const themeBtn = document.getElementById('themeBtn');
                if (themeBtn) {
                    themeBtn.textContent = 'Thème: ' + (savedTheme === 'light' ? 'Clair' : 'Sombre');
                    themeBtn.addEventListener('click', toggleTheme);
                }

                // Sections repliables
                document.querySelectorAll('.error-type-header').forEach(header => {
                    header.addEventListener('click', function() {
                        const content = this.nextElementSibling;
                        const toggle = this.querySelector('.collapsible-toggle');
                        if (!content) return;
                        content.classList.toggle('expanded');
                        if (toggle) toggle.classList.toggle('collapsed');
                    });
                });

                // Filtres
                const errorTypeFilter = document.getElementById('errorTypeFilter');
                const fileFilter = document.getElementById('fileFilter');
                const severityFilter = document.getElementById('severityFilter');

                function applyFilters() {
                    const selectedErrorType = errorTypeFilter ? errorTypeFilter.value : 'all';
                    const selectedFile = fileFilter ? fileFilter.value : 'all';
                    const selectedSeverity = severityFilter ? severityFilter.value : 'all';

                    document.querySelectorAll('.error-type-section').forEach(section => {
                        const errorType = section.dataset.errorType;
                        const hasSelectedFile = selectedFile === 'all' ||
                            section.querySelector(`[data-file*="${selectedFile}"]`);

                        let showSection = (selectedErrorType === 'all' || errorType === selectedErrorType) && hasSelectedFile;

                        // (Placeholder) Filtre de gravité si besoin plus tard
                        if (selectedSeverity !== 'all') {
                            // Implémentation à ajouter selon votre logique
                        }

                        section.style.display = showSection ? 'block' : 'none';
                    });

                    updateVisibleStats();
                }

                function updateVisibleStats() {
                    const visibleSections = document.querySelectorAll('.error-type-section:not([style*="display: none"])');
                    let totalVisible = 0;
                    visibleSections.forEach(section => {
                        const badge = section.querySelector('.error-type-badge');
                        if (badge) {
                            const count = parseInt(badge.textContent) || 0;
                            totalVisible += count;
                        }
                    });

                    const filterInfo = document.getElementById('filterInfo');
                    if (filterInfo) {
                        filterInfo.textContent = `${totalVisible} erreur(s) visible(s) sur ${document.querySelectorAll('.error-type-section').length} type(s)`;
                    }
                }

                if (errorTypeFilter) errorTypeFilter.addEventListener('change', applyFilters);
                if (fileFilter) fileFilter.addEventListener('change', applyFilters);
                if (severityFilter) severityFilter.addEventListener('change', applyFilters);

                // Tout déplier / Tout replier
                const expandAllBtn = document.getElementById('expandAll');
                if (expandAllBtn) {
                    expandAllBtn.addEventListener('click', function() {
                        document.querySelectorAll('.error-type-content').forEach(content => {
                            content.classList.add('expanded');
                        });
                        document.querySelectorAll('.collapsible-toggle').forEach(toggle => {
                            toggle.classList.remove('collapsed');
                        });
                    });
                }

                const collapseAllBtn = document.getElementById('collapseAll');
                if (collapseAllBtn) {
                    collapseAllBtn.addEventListener('click', function() {
                        document.querySelectorAll('.error-type-content').forEach(content => {
                            content.classList.remove('expanded');
                        });
                        document.querySelectorAll('.collapsible-toggle').forEach(toggle => {
                            toggle.classList.add('collapsed');
                        });
                    });
                }

                // Recherche
                const searchInput = document.getElementById('searchInput');
                if (searchInput) {
                    searchInput.addEventListener('input', function() {
                        const searchTerm = this.value.toLowerCase();
                        document.querySelectorAll('.issue-item').forEach(item => {
                            const text = item.textContent.toLowerCase();
                            const shouldShow = searchTerm === '' || text.includes(searchTerm);
                            item.style.display = shouldShow ? 'block' : 'none';
                        });
                    });
                }

                // Mise à jour initiale des stats
                updateVisibleStats();
            });
        })();
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
                
                # Utiliser le JS harmonisé si l'info est présente
                selection_info = results.get('selection_info')
                if selection_info:
                    f.write(self._get_javascript_harmonized(selection_info))
                else:
                    f.write(self._get_javascript())

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
                        <button id="expandAll" class="btn">Tout déplier</button>
                        <button id="collapseAll" class="btn">Tout replier</button>
                        <button id="themeBtn" class="btn">Thème: Sombre</button>
                    </div>
                </div>
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
        
        html = """
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
        
        html = f"""
        <div class="error-type-section" data-error-type="{error_type}">
            <div class="error-type-header">
                <div>
                    <span class="collapsible-toggle collapsed"></span>
                    {type_icon} <strong>{type_name}</strong>
                    <span class="error-type-badge {css_class}">{len(issues)}</span>
                </div>
                <div class="stats-overview">
                    <span class="mini-stat">{len(issues_by_file)} fichier(s)</span>
                    <span class="mini-stat">{len(issues)} erreur(s)</span>
                </div>
            </div>
            
            <div class="error-type-content">
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
        """Génère un élément d'erreur individuel"""
        line = int(issue.get('line', 0) or 0)
        file_path = issue.get('file_path', '') or ''
        description = _html.escape(issue.get('description', ''))
        old_content = _html.escape(issue.get('old_content', ''))
        new_content = _html.escape(issue.get('new_content', ''))

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

        return f"""
        <div class="issue-item">
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
            "ESCAPED_QUOTES_MISMATCH": "Guillemets échappés incohérents",
            "QUOTE_BALANCE_ERROR": "Guillemets non équilibrés",
            "UNESCAPED_QUOTES_MISMATCH": "Guillemets non échappés incohérents"
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
            "ANALYSIS_ERROR": "🐛"
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
            "ANALYSIS_ERROR": "badge-other"
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