# ui/tutorial/generator.py
"""
Générateur de tutoriel HTML pour RenExtract (version française uniquement)
Fichier unique optimisé sans système multilingue
"""

import os
import sys
import base64
from pathlib import Path
from typing import Optional, Dict
from infrastructure.logging.logging import log_message
from infrastructure.config.constants import FOLDERS


class TutorialGenerator:
    """Générateur de guide HTML simplifié en français"""

    def __init__(self):
        self.tutorial_dir = self._get_tutorial_directory()
        self.images_dir = self._get_images_directory()
        self._ensure_directories()
        
        # Import du cache et du monitor de performance
        from .cache import get_tutorial_cache, clear_tutorial_cache
        from .utils import PerformanceMonitor
        self.cache = get_tutorial_cache()
        self.performance_monitor = PerformanceMonitor()

    def _get_tutorial_directory(self) -> str:
        """Répertoire de sortie du fichier HTML"""
        try:
            return FOLDERS["configs"]
        except Exception:
            return os.path.join(".", "04_Configs")

    def _get_images_directory(self) -> str:
        """Répertoire des images (structure simplifiée sans multilingue)"""
        try:
            if getattr(sys, 'frozen', False):
                # Version exécutable
                base_path = sys._MEIPASS
                images_path = os.path.join(base_path, "tutorial_images")
                if os.path.exists(images_path):
                    log_message("INFO", f"Images trouvées dans l'exe: {images_path}", category="tutorial_generator")
                    return images_path
                # Fallback si pas dans l'exe
                exe_dir = os.path.dirname(sys.executable)
                return os.path.join(exe_dir, "tutorial_images")
            else:
                # Version développement
                return os.path.join(".", "tutorial_images")
        except Exception as e:
            log_message("ERREUR", f"Erreur détermination dossier images: {e}", category="tutorial_generator")
            return os.path.join(".", "tutorial_images")

    def _ensure_directories(self):
        """Création des répertoires nécessaires"""
        try:
            Path(self.tutorial_dir).mkdir(parents=True, exist_ok=True)
            log_message("INFO", f"Répertoire tutoriel configuré: {self.tutorial_dir}", category="tutorial_generator")
        except Exception as e:
            log_message("ATTENTION", f"Erreur configuration répertoires: {e}", category="tutorial_generator")

    def _get_image_html(self, section: str, image_number: str, 
                       alt_text: str = "", caption_text: str = "") -> str:
        """Génère le HTML pour une image collapsible"""
        import time
        start_time = time.time()
        
        # Clé de cache unique
        cache_key = f"{section}_{image_number}"
        
        # Vérifier le cache
        cached_image = self.cache.get_image(cache_key)
        if cached_image:
            self.performance_monitor.cache_stats['cache_hits'] += 1
            return self._generate_collapsible_html(section, image_number, cached_image, 
                                                 alt_text, caption_text)

        self.performance_monitor.cache_stats['cache_misses'] += 1

        # Chercher l'image
        image_path = self._find_image(section, image_number)
        
        if not image_path:
            return self._generate_placeholder_html(section, image_number, alt_text)

        # Encoder l'image en base64
        base64_data = self._encode_image_to_base64(image_path)
        if not base64_data:
            return self._generate_placeholder_html(section, image_number, alt_text)

        # Mettre en cache
        self.cache.set_image(cache_key, base64_data)
        encode_time = time.time() - start_time
        self.performance_monitor.record_image_cache(cache_key, encode_time, len(base64_data))

        return self._generate_collapsible_html(section, image_number, base64_data, 
                                             alt_text, caption_text)

    def _find_image(self, section: str, image_number: str) -> Optional[str]:
        """Cherche une image dans le dossier tutorial_images"""
        # Essayer d'abord .gif, puis .png, puis .webp (pour compatibilité)
        for ext in ['.gif', '.png', '.webp']:
            image_path = os.path.join(self.images_dir, section, f"{image_number}{ext}")
            if os.path.exists(image_path):
                return image_path
        return None

    def _encode_image_to_base64(self, image_path: str) -> Optional[str]:
        """Encode une image en base64"""
        try:
            with open(image_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode('utf-8')
            
            # Déterminer le type MIME selon l'extension
            ext = os.path.splitext(image_path)[1].lower()
            if ext == '.gif':
                mime_type = "image/gif"
            elif ext == '.png':
                mime_type = "image/png"
            elif ext == '.webp':
                mime_type = "image/webp"
            else:
                mime_type = "image/png"  # Fallback
            
            return f"data:{mime_type};base64,{encoded}"
        except Exception as e:
            log_message("ERREUR", f"Erreur encodage image {image_path}: {e}", category="tutorial_generator")
            return None

    def _generate_placeholder_html(self, section: str, image_number: str, alt_text: str) -> str:
        """Génère un placeholder pour image manquante"""
        # Essayer d'abord .gif, puis .png, puis .webp
        for ext in ['.gif', '.png', '.webp']:
            expected_path = os.path.join(self.images_dir, section, f"{image_number}{ext}")
            if not os.path.exists(expected_path):
                continue
            break
        else:
            # Si aucun fichier n'existe, utiliser .png par défaut
            expected_path = os.path.join(self.images_dir, section, f"{image_number}.png")
        
        return f'''
        <div class="image-placeholder">
            <div class="placeholder-content">
                <span class="placeholder-icon">📷</span>
                <div class="placeholder-text">
                    <strong>[Image: {section}/{image_number}]</strong>
                    <br><small>{alt_text}</small>
                    <br><small style="opacity: 0.6;">Placez l'image dans:<br>{expected_path}</small>
                </div>
            </div>
        </div>
        '''

    def _generate_collapsible_html(self, section: str, image_number: str, base64_data: str,
                                 alt_text: str, caption_text: str) -> str:
        """Génère le HTML pour une image collapsible"""
        # ID unique pour éviter les conflits
        safe_id = f"{section}_{image_number}".replace('/', '_').replace('-', '_')
        
        display_text = caption_text if caption_text else alt_text
        
        return f'''
        <div class="image-container collapsible">
            <div class="image-toggle" onclick="toggleImage('{safe_id}')" role="button" tabindex="0" aria-expanded="false">
                <span class="toggle-icon" id="icon_{safe_id}">▶</span>
                <span class="toggle-text">Cliquez pour voir =>  {display_text}</span>
            </div>
            <div class="tutorial-image" id="img_{safe_id}" style="display: none;">
                <img src="{base64_data}" alt="{alt_text}" class="responsive-image" onclick="openLightbox(this.src, '{alt_text}')" style="cursor: zoom-in;" title="Cliquer pour agrandir" />
                {f'<p class="image-caption">{caption_text}</p>' if caption_text else ''}
            </div>
        </div>
        '''

    def generate_tutorial_html(self, version: str = "Unknown") -> Optional[str]:
        """Génère le fichier HTML du guide (français uniquement)"""
        try:
            # Vider le cache d'images pour forcer le rechargement
            from .cache import clear_tutorial_cache, get_tutorial_cache
            clear_tutorial_cache()
            self.cache = get_tutorial_cache()  # Récupérer la nouvelle instance
            log_message("DEBUG", "Cache d'images vidé pour génération fraîche", category="tutorial_generator")
            
            tutorial_name = "renextract_guide_complet.html"
            tutorial_path = os.path.join(self.tutorial_dir, tutorial_name)

            # Générer le contenu HTML
            html_content = self._generate_complete_html(version)
            
            # Écrire le fichier
            with open(tutorial_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            log_message("INFO", f"Guide généré: {tutorial_path}", category="tutorial_generator")
            return tutorial_path

        except Exception as e:
            log_message("ERREUR", f"Erreur génération tutoriel HTML: {e}", category="tutorial_generator")
            return None

    def _generate_complete_html(self, version: str) -> str:
        """Génère le HTML complet (français uniquement)"""
        log_message("INFO", "=== DÉBUT GÉNÉRATION HTML ===", category="tutorial_generator")
        
        try:
            # Charger les modules de contenu
            content_modules = {}
            for i in range(1, 10):
                try:
                    module_name = f"ui.tutorial.content.tab_{i:02d}"
                    content_modules[i] = __import__(module_name, fromlist=[f'tab_{i:02d}'])
                    log_message("INFO", f"✅ Module tab_{i:02d} chargé", category="tutorial_generator")
                except ImportError as e:
                    log_message("ERREUR", f"❌ Module tab_{i:02d} ÉCHEC: {e}", category="tutorial_generator")
                    content_modules[i] = None

            # Générer le contenu par onglet
            tab_contents = {}
            for tab_num in range(1, 10):
                module = content_modules.get(tab_num)
                if module is None:
                    tab_contents[tab_num] = self._get_fallback_tab_content(tab_num)
                else:
                    tab_contents[tab_num] = self._generate_tab_content(tab_num, module)

            # Générer le logo
            logo_html = self._generate_logo_html()

            # Utiliser le template de base
            html_template = self._get_html_template()
            
            # Variables pour le template
            template_vars = {
                'version': version,
                'logo_html': logo_html,
                'css_styles': self._get_complete_css(),
                'javascript': self._get_complete_javascript(),
            }

            # Ajouter les contenus d'onglets
            for i in range(1, 10):
                template_vars[f'tab_content_{i}'] = tab_contents.get(i, self._get_fallback_tab_content(i))
            
            final_html = html_template.format(**template_vars)
            
            log_message("INFO", f"HTML complet généré: {len(final_html)} caractères", category="tutorial_generator")
            log_message("INFO", "=== FIN GÉNÉRATION HTML ===", category="tutorial_generator")
            
            return final_html

        except Exception as e:
            log_message("ERREUR", f"ERREUR génération HTML: {type(e).__name__}: {e}", category="tutorial_generator")
            import traceback
            log_message("ERREUR", f"Traceback: {traceback.format_exc()}", category="tutorial_generator")
            return self._generate_fallback_html(version)

    def _generate_tab_content(self, tab_num: int, content_module) -> str:
        """Génère le contenu d'un onglet (français uniquement)"""
        if content_module is None or not hasattr(content_module, 'generate_content'):
            log_message("ERREUR", f"Module onglet {tab_num} invalide", category="tutorial_generator")
            return self._get_fallback_tab_content(tab_num)
        
        try:
            content = content_module.generate_content(self)
            
            if not content or len(content.strip()) == 0:
                log_message("ATTENTION", f"Contenu vide pour onglet {tab_num}", category="tutorial_generator")
                return self._get_fallback_tab_content(tab_num)
            
            return content
            
        except Exception as e:
            log_message("ERREUR", f"Exception onglet {tab_num}: {e}", category="tutorial_generator")
            import traceback
            log_message("ERREUR", f"Traceback: {traceback.format_exc()}", category="tutorial_generator")
            return self._get_fallback_tab_content(tab_num)

    def _generate_logo_html(self) -> str:
        """Génère le HTML du logo (cliquable vers la section contact)"""
        # Essayer différents noms de fichiers pour le logo
        logo_names = ["logo_192", "001", "logo", "main_logo"]
        
        for logo_name in logo_names:
            logo_path = self._find_image("Logo", logo_name)
            if logo_path:
                logo_base64 = self._encode_image_to_base64(logo_path)
                if logo_base64:
                    log_message("INFO", f"Logo trouvé: {logo_path}", category="tutorial_generator")
                    return f'''<a href="#support-contact" onclick="switchToTabDirect(8); setTimeout(() => {{ document.getElementById('support-contact').scrollIntoView({{ behavior: 'smooth', block: 'start' }}); }}, 300); return false;" style="cursor: pointer; display: block;" title="📧 Contacter l'équipe de développement">
                        <img src="{logo_base64}" alt="RenExtract Logo" class="header-logo">
                    </a>'''
        
        log_message("ATTENTION", "Aucun logo trouvé, placeholder utilisé", category="tutorial_generator")
        return '<a href="#support-contact" onclick="switchToTabDirect(8); setTimeout(() => { document.getElementById(\'support-contact\').scrollIntoView({ behavior: \'smooth\', block: \'start\' }); }, 300); return false;" style="cursor: pointer; display: block;" title="📧 Contacter l\'équipe de développement"><div class="logo-placeholder">RenExtract</div></a>'

    def _get_fallback_tab_content(self, tab_num: int) -> str:
        """Contenu de fallback pour un onglet"""
        return f'''
        <div class="section">
            <h2>Onglet {tab_num}</h2>
            <p>Contenu en cours de développement.</p>
            <p><strong>DEBUG:</strong> Le module tab_{tab_num:02d}.py n'a pas pu être chargé ou a généré une erreur.</p>
        </div>
        '''

    def _get_html_template(self) -> str:
        """Template HTML simplifié (français uniquement)"""
        return """<!DOCTYPE html>
<html lang="fr" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guide Complet {version}</title>
    {css_styles}
</head>
<body>
    <div class="logo-corner">{logo_html}</div>
    
    <header class="header">
        <div class="container">
            <h1>Guide Complet RenExtract</h1>
            <p>Version {version}</p>
        </div>
    </header>

    <nav class="nav-tabs">
        <button class="nav-tab active" data-tab="1">📋 Sommaire</button>
        <button class="nav-tab" data-tab="2">🔄 Workflow</button>
        <button class="nav-tab" data-tab="3">🖥️ Interface</button>
        <button class="nav-tab" data-tab="4">🎮 Générateur</button>
        <button class="nav-tab" data-tab="5">🛠️ Outils</button>
        <button class="nav-tab" data-tab="6">💾 Sauvegardes</button>
        <button class="nav-tab" data-tab="7">⚙️ Paramètres</button>
        <button class="nav-tab" data-tab="8">🔧 Technique</button>
        <button class="nav-tab" data-tab="9">❓ FAQ</button>
    </nav>

    <main class="container">
        <div class="tab-content active" id="tab-1">{tab_content_1}</div>
        <div class="tab-content" id="tab-2">{tab_content_2}</div>
        <div class="tab-content" id="tab-3">{tab_content_3}</div>
        <div class="tab-content" id="tab-4">{tab_content_4}</div>
        <div class="tab-content" id="tab-5">{tab_content_5}</div>
        <div class="tab-content" id="tab-6">{tab_content_6}</div>
        <div class="tab-content" id="tab-7">{tab_content_7}</div>
        <div class="tab-content" id="tab-8">{tab_content_8}</div>
        <div class="tab-content" id="tab-9">{tab_content_9}</div>
    </main>

    <!-- Lightbox pour agrandir les images -->
    <div id="lightbox" class="lightbox" onclick="closeLightbox(event)">
        <span class="lightbox-close" onclick="closeLightbox(event)">&times;</span>
        <img class="lightbox-content" id="lightbox-img" onclick="toggleZoom(event)">
        <div class="lightbox-caption" id="lightbox-caption"></div>
    </div>

    {javascript}
</body>
</html>"""

    def _get_complete_css(self) -> str:
        """CSS simplifié (français uniquement, sans drapeaux ni sommaire)"""
        return """<style>
:root {
  --bg: #1a1f29; --fg: #e2e8f0; --hdr: #2d3748; --sep: #4a5568;
  --accent: #4a90e2; --success: #48bb78; --warning: #ed8936; --danger: #f56565;
  --card-bg: #2d3748; --nav-bg: #1a202c;
}
[data-theme="light"] {
  --bg: #f7fafc; --fg: #2d3748; --hdr: #edf2f7; --sep: #e2e8f0;
  --accent: #3182ce; --success: #38a169; --warning: #d69e2e; --danger: #e53e3e;
  --card-bg: #ffffff; --nav-bg: #f7fafc;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--fg); line-height: 1.6; transition: all 0.3s ease; }

.floating-controls { 
  position: fixed; top: 250px; right: 20px; z-index: 10000; 
  display: flex; flex-direction: column; gap: 12px; transition: top 0.3s ease;
}
.floating-controls.scrolled { top: 80px; }
.theme-toggle { 
  background: var(--card-bg); 
  border: 1px solid var(--sep); 
  border-radius: 12px; 
  padding: 12px; 
  cursor: pointer; 
  transition: all 0.2s; 
  box-shadow: 0 4px 12px rgba(0,0,0,0.3); 
  min-width: 48px; 
  min-height: 48px; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  color: var(--accent); 
  font-size: 1.5em;
}

.back-to-top { 
  position: fixed; bottom: 30px; right: 30px; z-index: 9999; 
  background: var(--accent); color: white; border: none; border-radius: 50%; 
  width: 60px; height: 60px; font-size: 1.5em; cursor: pointer; 
  box-shadow: 0 4px 12px rgba(0,0,0,0.3); transition: all 0.2s; 
  opacity: 0; visibility: hidden; 
}
.back-to-top.visible { opacity: 1; visibility: visible; }
.back-to-top:hover { background: var(--success); transform: translateY(-3px); }

.logo-corner { position: fixed; bottom: 30px; left: 30px; z-index: 9999; }
.logo-corner a { display: block; }
.logo-corner img { 
  width: 70px; height: 70px; border-radius: 12px; 
  box-shadow: 0 4px 12px rgba(0,0,0,0.3); transition: all 0.3s; 
  cursor: pointer;
}
.logo-corner a:hover img { 
  transform: scale(1.15) rotate(5deg); 
  box-shadow: 0 6px 20px rgba(74, 144, 226, 0.5);
}

.header { 
  background: linear-gradient(135deg, var(--hdr), var(--nav-bg)); 
  padding: 40px 0; text-align: center; border-bottom: 2px solid var(--sep); 
}
.header h1 { 
  font-size: 2.5rem; color: var(--accent); 
  text-shadow: 0 2px 4px rgba(0,0,0,0.3); font-weight: 700; 
}

.nav-tabs { 
  background: var(--nav-bg); border-bottom: 2px solid var(--sep); 
  display: flex; position: sticky; top: 0; z-index: 1000; overflow-x: auto; 
}
.nav-tab { 
  flex: 1; min-width: 140px; padding: 16px 20px; border: none; 
  background: transparent; color: var(--fg); cursor: pointer; 
  transition: all 0.3s; white-space: nowrap; border-bottom: 3px solid transparent; 
}
.nav-tab:hover { 
  background: rgba(74, 144, 226, 0.1); transform: translateY(-2px); 
  border-bottom-color: var(--accent); 
}
.nav-tab.active { 
  background: var(--accent); color: white; transform: translateY(-2px); 
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3); 
}

.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
.tab-content { display: none; padding: 40px 0; }
.tab-content.active { display: block; animation: fadeIn 0.3s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.lang-pane { display: none; }
.lang-pane.active { display: block; }

.section { 
  background: var(--card-bg); border-radius: 16px; padding: 30px; 
  margin-bottom: 30px; border: 1px solid var(--sep); 
  box-shadow: 0 4px 12px rgba(0,0,0,0.2); transition: all 0.2s; position: relative; 
  scroll-margin-top: 100px;
}
.section:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.3); }
.section h2 { 
  color: var(--accent); font-size: 1.8rem; margin-bottom: 20px; 
  font-weight: 600; padding-left: 40px; position: relative; 
}
.section h2::before { content: '▶'; position: absolute; left: 10px; color: var(--success); }
.section h3 { color: var(--success); font-size: 1.4rem; margin: 25px 0 15px 0; }

.image-container.collapsible { 
  background: var(--card-bg); border: 1px solid var(--sep); 
  border-radius: 12px; margin: 25px 0; overflow: hidden; 
  box-shadow: 0 2px 8px rgba(0,0,0,0.2); 
}
.image-toggle { 
  padding: 18px 24px; background: var(--nav-bg); cursor: pointer; 
  display: flex; align-items: center; gap: 12px; transition: all 0.2s; 
  border-bottom: 1px solid var(--sep); 
}
.image-toggle:hover { background: rgba(74, 144, 226, 0.1); padding-left: 30px; }
.toggle-icon { 
  font-size: 1.3rem; color: var(--accent); font-weight: bold; transition: all 0.3s; 
}
.image-toggle.expanded .toggle-icon { transform: rotate(90deg); color: var(--success); }
.toggle-text { font-weight: 600; color: var(--fg); }
.tutorial-image { padding: 24px; text-align: center; background: var(--bg); }
.responsive-image { 
  max-width: 100%; height: auto; border-radius: 8px; 
  box-shadow: 0 4px 16px rgba(0,0,0,0.2); transition: all 0.3s; 
}
.responsive-image:hover { transform: scale(1.02); }
.image-caption { margin-top: 15px; font-style: italic; color: var(--success); }

.image-placeholder { 
  background: var(--nav-bg); border: 2px dashed var(--accent); 
  border-radius: 12px; padding: 40px 20px; text-align: center; margin: 25px 0; 
}
.placeholder-content { 
  display: flex; align-items: center; justify-content: center; 
  gap: 20px; flex-wrap: wrap; 
}
.placeholder-icon { font-size: 3rem; opacity: 0.6; color: var(--accent); }
.placeholder-text { color: var(--fg); opacity: 0.8; }

/* Styles pour les boutons de navigation directe */
.nav-link-btn {
  background: none;
  border: none;
  color: var(--accent);
  text-decoration: none;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 8px 0;
  text-align: left;
  width: 100%;
  font-size: inherit;
  font-family: inherit;
  border-bottom: 1px solid transparent;
  line-height: 1.4;
}

.nav-link-btn:hover {
  color: var(--success);
  border-bottom-color: var(--success);
  transform: translateX(8px);
  font-weight: 600;
  background: rgba(74, 144, 226, 0.1);
  border-radius: 4px;
  padding-left: 12px;
}

.nav-link-btn:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
  border-radius: 4px;
}

/* Assurer que les li contiennent bien les boutons */
ul li {
  list-style: none;
  margin: 8px 0;
}

ul {
  padding-left: 0;
}

/* Styles pour les grilles de fonctionnalités */
.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.feature-card {
  background: var(--nav-bg);
  padding: 20px;
  border-radius: 12px;
  border-left: 4px solid var(--accent);
  transition: all 0.2s ease;
}

.feature-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  border-left-color: var(--success);
}

.workflow-step {
  background: var(--nav-bg);
  padding: 20px;
  border-radius: 12px;
  margin: 15px 0;
  border-left: 4px solid var(--success);
  position: relative;
}

.workflow-step[data-step="1"] { border-left-color: #8b5cf6; }
.workflow-step[data-step="2"] { border-left-color: var(--accent); }
.workflow-step[data-step="3"] { border-left-color: var(--success); }

@media (max-width: 768px) {
  .floating-controls { top: 120px; right: 10px; gap: 8px; }
  .floating-controls.scrolled { top: 70px; }
  .theme-toggle, .lang-selector, .nav-home-btn { min-width: 40px; min-height: 40px; padding: 8px; }
  .header h1 { font-size: 2rem; }
  .nav-tab { min-width: 120px; padding: 12px 16px; }
  .section { padding: 20px; }
  .back-to-top { width: 50px; height: 50px; bottom: 20px; right: 20px; }
  .logo-corner { bottom: 20px; left: 20px; }
  .logo-corner img { width: 50px; height: 50px; }
  .feature-grid { grid-template-columns: 1fr; }
}

/* === Boîtes de contenu spécialisées === */
.warning-box, .tip-box, .info-box, .step-box {
  padding: 1.25rem;
  margin: 1.5rem 0;
  border-radius: 12px;
  border-left: 4px solid;
  background: var(--card-bg);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.warning-box {
  border-left-color: var(--danger);
  background: linear-gradient(135deg, var(--card-bg) 0%, rgba(245, 101, 101, 0.05) 100%);
}

.warning-box strong {
  color: var(--danger);
}

.tip-box {
  border-left-color: var(--success);
  background: linear-gradient(135deg, var(--card-bg) 0%, rgba(72, 187, 120, 0.05) 100%);
}

.tip-box strong {
  color: var(--success);
}

.info-box {
  border-left-color: var(--info);
  background: linear-gradient(135deg, var(--card-bg) 0%, rgba(74, 144, 226, 0.05) 100%);
}

.info-box h3, .info-box h4 {
  color: var(--info);
  margin-top: 0;
  margin-bottom: 0.75rem;
}

.step-box {
  border-left-color: var(--accent);
  background: linear-gradient(135deg, var(--card-bg) 0%, rgba(139, 92, 246, 0.05) 100%);
  position: relative;
}

.step-box h4, .step-box h5 {
  color: var(--accent);
  margin-top: 0;
  margin-bottom: 0.75rem;
}

.warning-box ul, .tip-box ul, .info-box ul, .step-box ul {
  margin-bottom: 0;
}

/* === Amélioration des listes === */
.section ul {
  line-height: 1.8;
  margin: 1rem 0;
}

.section li {
  margin-bottom: 0.5rem;
}

.section code {
  background: rgba(139, 92, 246, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 0.9em;
  color: var(--accent);
}

.section pre {
  overflow-x: auto;
}

.section h3 {
  color: var(--accent);
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-size: 1.4em;
}

.section h4 {
  color: var(--fg);
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  font-size: 1.2em;
}

.section h5 {
  color: var(--fg);
  margin-top: 1rem;
  margin-bottom: 0.5rem;
  font-size: 1.1em;
  font-weight: 600;
}

/* === Lightbox pour agrandir les images === */
.lightbox {
  display: none;
  position: fixed;
  z-index: 10000;
  padding-top: 60px;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.95);
  animation: fadeIn 0.3s;
}

.lightbox-content {
  margin: auto;
  display: block;
  max-width: 95%;
  max-height: 85vh;
  object-fit: contain;
  animation: zoomIn 0.3s;
  transition: transform 0.3s ease;
  cursor: zoom-in;
}

.lightbox-close {
  position: absolute;
  top: 20px;
  right: 35px;
  color: #f1f1f1;
  font-size: 50px;
  font-weight: bold;
  transition: 0.3s;
  cursor: pointer;
  z-index: 10001;
}

.lightbox-close:hover,
.lightbox-close:focus {
  color: var(--accent);
  text-decoration: none;
  cursor: pointer;
}

.lightbox-caption {
  margin: auto;
  display: block;
  width: 80%;
  max-width: 700px;
  text-align: center;
  color: #ccc;
  padding: 20px 0;
  font-size: 1.1em;
}

@keyframes zoomIn {
  from { transform: scale(0.8); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

/* Curseur zoom sur les images */
.responsive-image {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.responsive-image:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 16px rgba(0,0,0,0.3);
}
</style>"""

    def _get_complete_javascript(self) -> str:
        """JavaScript simplifié (français uniquement, avec auto-scroll onglets)"""
        return """<script>
(function() {
  let currentTheme = 'dark';
  
  function ready(fn) { if (document.readyState !== 'loading') fn(); else document.addEventListener('DOMContentLoaded', fn); }
  function save(key, value) { try { localStorage.setItem('renextract_' + key, JSON.stringify(value)); } catch(e) {} }
  function load(key, def) { try { const s = localStorage.getItem('renextract_' + key); return s ? JSON.parse(s) : def; } catch(e) { return def; } }
  
  function applyTheme(theme) {
    currentTheme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    const btn = document.getElementById('theme-toggle');
    if (btn) { 
      btn.textContent = theme === 'dark' ? '☀️' : '🌙'; 
      btn.title = theme === 'dark' ? 'Thème clair' : 'Thème sombre'; 
    }
    save('theme', theme);
    positionFloatingControls();
  }
  
  function positionFloatingControls() {
    const controls = document.querySelector('.floating-controls');
    if (!controls) return;
    
    const navTabs = document.querySelector('.nav-tabs');
    const scrollY = window.scrollY;
    let top = 250;
    
    if (navTabs && scrollY > 50) {
      const navRect = navTabs.getBoundingClientRect();
      if (navRect.top <= 0 && navRect.bottom > 0) {
        top = navRect.bottom + 15;
        controls.classList.add('scrolled');
      } else {
        controls.classList.remove('scrolled');
      }
    } else {
      top = 250;
      controls.classList.remove('scrolled');
    }
    
    controls.style.top = top + 'px';
  }
  
  function createFloatingControls() {
    const container = document.createElement('div');
    container.className = 'floating-controls';
    
    const themeBtn = document.createElement('button');
    themeBtn.id = 'theme-toggle';
    themeBtn.className = 'theme-toggle';
    themeBtn.textContent = currentTheme === 'dark' ? '☀️' : '🌙';
    themeBtn.title = currentTheme === 'dark' ? 'Thème clair' : 'Thème sombre';
    themeBtn.addEventListener('click', () => applyTheme(currentTheme === 'dark' ? 'light' : 'dark'));
    
    container.appendChild(themeBtn);
    document.body.appendChild(container);
    
    const backBtn = document.createElement('button');
    backBtn.className = 'back-to-top';
    backBtn.textContent = '↑';
    backBtn.title = 'Remonter en haut';
    backBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    window.addEventListener('scroll', () => {
      backBtn.classList.toggle('visible', window.scrollY > 300);
      positionFloatingControls();
    }, { passive: true });
    document.body.appendChild(backBtn);
  }
  
  function initTabs() {
    const tabs = document.querySelectorAll('.nav-tab');
    const contents = document.querySelectorAll('.tab-content');
    tabs.forEach((tab, i) => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        contents.forEach(c => c.classList.remove('active'));
        tab.classList.add('active');
        if (contents[i]) contents[i].classList.add('active');
        save('activeTab', i);
        // AUTO-SCROLL EN HAUT lors du changement d'onglet
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    });
    const saved = load('activeTab', 0);
    if (tabs[saved] && contents[saved]) { 
      tabs.forEach(t => t.classList.remove('active')); 
      contents.forEach(c => c.classList.remove('active')); 
      tabs[saved].classList.add('active'); 
      contents[saved].classList.add('active'); 
    }
  }
  
  function setupDirectNavigation() {
    document.addEventListener('click', function(e) {
      const navBtn = e.target.closest('.nav-link-btn');
      if (!navBtn) return;
      
      e.preventDefault();
      e.stopPropagation();
      
      const targetTab = parseInt(navBtn.getAttribute('data-target-tab'));
      const targetSection = navBtn.getAttribute('data-target-section');
      
      if (targetTab) {
        switchToTabDirect(targetTab);
        
        if (targetSection) {
          setTimeout(() => {
            const targetElement = document.getElementById(targetSection);
            if (targetElement) {
              targetElement.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start',
                inline: 'nearest'
              });
              
              targetElement.style.transition = 'all 0.5s ease';
              targetElement.style.backgroundColor = 'rgba(74, 144, 226, 0.2)';
              targetElement.style.transform = 'scale(1.01)';
              
              setTimeout(() => {
                targetElement.style.backgroundColor = '';
                targetElement.style.transform = 'scale(1)';
              }, 1500);
            }
          }, 200);
        }
      }
    });
    
    function switchToTabDirect(tabNumber) {
      document.querySelectorAll('.nav-tab').forEach(tab => tab.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
      
      const targetTab = document.querySelector(`.nav-tab[data-tab="${tabNumber}"]`);
      const targetContent = document.getElementById(`tab-${tabNumber}`);
      
      if (targetTab && targetContent) {
        targetTab.classList.add('active');
        targetContent.classList.add('active');
        save('activeTab', tabNumber - 1);
        // AUTO-SCROLL EN HAUT lors de la navigation directe
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }
  }
  
  window.toggleImage = function(id) {
    const img = document.getElementById('img_' + id);
    const toggle = document.querySelector('.image-toggle[onclick*="' + id + '"]');
    if (!img) return;
    const isHidden = img.style.display === 'none' || img.style.display === '';
    if (isHidden) { 
      img.style.display = 'block'; 
      img.style.opacity = '0'; 
      img.offsetHeight; 
      img.style.transition = 'opacity 0.3s ease'; 
      img.style.opacity = '1'; 
    } else { 
      img.style.opacity = '0'; 
      setTimeout(() => img.style.display = 'none', 300); 
    }
    if (toggle) { 
      toggle.classList.toggle('expanded', isHidden); 
      toggle.setAttribute('aria-expanded', isHidden); 
    }
    const states = load('imageStates', {}); 
    states[id] = isHidden; 
    save('imageStates', states);
  };
  
  function initImageToggles() {
    document.querySelectorAll('.image-toggle').forEach(toggle => {
      toggle.setAttribute('role', 'button');
      toggle.setAttribute('tabindex', '0');
      toggle.addEventListener('keydown', e => { 
        if (e.key === 'Enter' || e.key === ' ') { 
          e.preventDefault(); 
          const match = toggle.getAttribute('onclick').match(/toggleImage\\('([^']+)'\\)/); 
          if (match) window.toggleImage(match[1]); 
        } 
      });
    });
    const states = load('imageStates', {});
    Object.entries(states).forEach(([id, open]) => { 
      if (open) { 
        const img = document.getElementById('img_' + id); 
        const toggle = document.querySelector('.image-toggle[onclick*="' + id + '"]'); 
        if (img && toggle) { 
          img.style.display = 'block'; 
          toggle.classList.add('expanded'); 
        } 
      } 
    });
  }
  
  ready(() => {
    currentTheme = load('theme', 'dark');
    applyTheme(currentTheme);
    initTabs();
    initImageToggles();
    createFloatingControls();
    positionFloatingControls();
    setupDirectNavigation();
    console.log('Guide RenExtract initialisé');
  });

  // === Fonction pour l'arborescence collapsible ===
  window.toggleArborescence = function() {
    const content = document.getElementById('arborescence-content');
    const toggle = document.getElementById('arborescence-toggle');
    if (content && toggle) {
      if (content.style.display === 'none') {
        content.style.display = 'block';
        toggle.style.transform = 'rotate(90deg)';
        toggle.style.color = 'var(--success)';
      } else {
        content.style.display = 'none';
        toggle.style.transform = 'rotate(0deg)';
        toggle.style.color = 'var(--accent)';
      }
    }
  };

  // === Fonctions Lightbox pour agrandir les images avec zoom ===
  let currentZoom = 1.0;
  const maxZoom = 2.0;
  const zoomStep = 0.5;

  window.openLightbox = function(src, alt) {
    const lightbox = document.getElementById('lightbox');
    const img = document.getElementById('lightbox-img');
    const caption = document.getElementById('lightbox-caption');
    
    currentZoom = 1.0;
    lightbox.style.display = 'block';
    img.src = src;
    img.style.transform = 'scale(1)';
    img.style.cursor = 'zoom-in';
    caption.textContent = alt + ' - Cliquer pour zoomer';
    document.body.style.overflow = 'hidden'; // Empêcher le scroll
  };

  window.closeLightbox = function(event) {
    // Ne fermer que si on clique sur le fond, pas sur l'image
    if (event && event.target.id === 'lightbox-img') {
      return;
    }
    const lightbox = document.getElementById('lightbox');
    lightbox.style.display = 'none';
    currentZoom = 1.0;
    document.body.style.overflow = 'auto'; // Réactiver le scroll
  };

  window.toggleZoom = function(event) {
    event.stopPropagation(); // Empêcher la fermeture du lightbox
    const img = document.getElementById('lightbox-img');
    const caption = document.getElementById('lightbox-caption');
    
    currentZoom += zoomStep;
    if (currentZoom > maxZoom) {
      currentZoom = 1.0;
    }
    
    img.style.transform = `scale(${currentZoom})`;
    img.style.cursor = currentZoom >= maxZoom ? 'zoom-out' : 'zoom-in';
    
    const zoomPercent = Math.round(currentZoom * 100);
    const baseText = caption.textContent.split(' - ')[0];
    caption.textContent = `${baseText} - Zoom ${zoomPercent}%`;
  };

  // Fermer avec la touche Escape
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      closeLightbox();
    }
  });
})();
</script>"""

    def _generate_fallback_html(self, version: str) -> str:
        """HTML de fallback en cas d'erreur"""
        return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guide {version}</title>
    <style>body{{font-family:Arial,sans-serif;margin:40px;line-height:1.6}}.error{{color:#dc3545;background:#f8d7da;padding:20px;border-radius:8px}}</style>
</head>
<body>
    <h1>Guide {version}</h1>
    <div class="error">
        <h2>Erreur de génération</h2>
        <p>Le contenu complet n'a pas pu être généré. Vérifiez les logs pour plus de détails.</p>
    </div>
</body>
</html>"""