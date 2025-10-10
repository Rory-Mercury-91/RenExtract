# ui/tutorial/generator.py
"""
Générateur de tutoriel HTML multilingue pour RenExtract
Fichier unique avec switch de langue intégré
"""

import os
import sys
import base64
import json
from pathlib import Path
from typing import Optional, Dict, Any
from infrastructure.logging.logging import log_message
from infrastructure.config.constants import FOLDERS


class MultilingualTutorialGenerator:
    SUPPORTED_LANGUAGES = ['fr', 'en', 'de']
    DEFAULT_LANGUAGE = 'fr'
    LANGUAGE_FALLBACK = {'en': 'fr', 'de': 'fr'}

    def __init__(self):
        self.tutorial_dir = self._get_tutorial_directory()
        self.images_dir = self._get_images_directory()
        self._ensure_directories()
        
        # Import du cache et du monitor de performance
        from .cache import get_tutorial_cache
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
        """Répertoire des images avec structure multilingue"""
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

    def load_translations(self, language: str) -> Dict[str, Any]:
        """Charge les traductions avec cache et fallback"""
        import time
        start = time.time()
        
        lang = (language or self.DEFAULT_LANGUAGE).lower()
        if lang not in self.SUPPORTED_LANGUAGES:
            lang = self.DEFAULT_LANGUAGE

        # Vérifier le cache d'abord
        cached = self.cache.get_translation(lang)
        if cached:
            self.performance_monitor.cache_stats['cache_hits'] += 1
            return cached

        self.performance_monitor.cache_stats['cache_misses'] += 1

        def _import_lang(l: str) -> Dict[str, Any]:
            """Import dynamique d'un fichier de traduction"""
            try:
                module_name = f"ui.tutorial.translations.{l}"
                module = __import__(module_name, fromlist=[l])
                return getattr(module, 'TRANSLATIONS', {})
            except ImportError:
                return {}

        # Tentative de chargement avec fallback
        translations = _import_lang(lang)
        
        if not translations:
            log_message("ATTENTION", f"Traductions vides pour {lang}, fallback", category="tutorial_generator")
            fallback_lang = self.LANGUAGE_FALLBACK.get(lang, self.DEFAULT_LANGUAGE)
            if fallback_lang != lang:
                translations = _import_lang(fallback_lang)
                if translations:
                    lang = fallback_lang
                    log_message("INFO", f"Fallback réussi vers {fallback_lang}", category="tutorial_generator")
            
            # Dernier recours vers FR
            if not translations and lang != self.DEFAULT_LANGUAGE:
                translations = _import_lang(self.DEFAULT_LANGUAGE)
                if translations:
                    lang = self.DEFAULT_LANGUAGE

        if translations:
            load_time = time.time() - start
            self.cache.set_translation(lang, translations)
            self.performance_monitor.record_translation_load(lang, load_time, len(str(translations)))
            log_message("INFO", f"Traductions chargées pour {lang}: {len(translations)} entrées en {load_time:.3f}s", 
                       category="tutorial_generator")
        else:
            log_message("ERREUR", f"Impossible de charger les traductions pour {lang}", category="tutorial_generator")
            # Retourner structure minimale pour éviter les crashes
            translations = {
                'ui': {'main_title': 'RenExtract Guide', 'place_image': 'Placez l\'image dans:'},
                'images': {},
                'tabs': {},
                'meta': {'language_name': lang, 'language_code': lang}
            }

        return translations

    def _get_image_html(self, section: str, image_number: str, language: str, 
                       alt_text: str = "", caption_text: str = "") -> str:
        """Génère le HTML pour une image collapsible"""
        import time
        start_time = time.time()

        # Chargement des traductions pour les placeholders
        translations = self.load_translations(language)
        
        # Clé de cache unique
        cache_key = f"{language}_{section}_{image_number}"
        
        # Vérifier le cache
        cached_image = self.cache.get_image(cache_key)
        if cached_image:
            self.performance_monitor.cache_stats['cache_hits'] += 1
            return self._generate_collapsible_html(section, image_number, cached_image, 
                                                 alt_text, caption_text, translations, language)

        self.performance_monitor.cache_stats['cache_misses'] += 1

        # Chercher l'image avec fallback
        image_path = self._find_image_with_fallback(section, image_number, language)
        
        if not image_path:
            return self._generate_placeholder_html(section, image_number, alt_text, language, translations)

        # Encoder l'image en base64
        base64_data = self._encode_image_to_base64(image_path)
        if not base64_data:
            return self._generate_placeholder_html(section, image_number, alt_text, language, translations)

        # Mettre en cache
        self.cache.set_image(cache_key, base64_data)
        encode_time = time.time() - start_time
        self.performance_monitor.record_image_cache(cache_key, encode_time, len(base64_data))

        return self._generate_collapsible_html(section, image_number, base64_data, 
                                             alt_text, caption_text, translations, language)

    def _find_image_with_fallback(self, section: str, image_number: str, language: str) -> Optional[str]:
        """Cherche une image avec fallback vers FR"""
        # Format: tutorial_images/fr/01_interface_principale/001.webp
        
        # Essayer la langue demandée
        image_path = os.path.join(self.images_dir, language, section, f"{image_number}.webp")
        if os.path.exists(image_path):
            return image_path
        
        # Fallback vers FR si différent
        if language != 'fr':
            fallback_path = os.path.join(self.images_dir, 'fr', section, f"{image_number}.webp")
            if os.path.exists(fallback_path):
                log_message("DEBUG", f"Fallback image fr pour {section}/{image_number}", category="tutorial_generator")
                return fallback_path
        
        return None

    def _encode_image_to_base64(self, image_path: str) -> Optional[str]:
        """Encode une image en base64"""
        try:
            with open(image_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode('utf-8')
            return f"data:image/webp;base64,{encoded}"
        except Exception as e:
            log_message("ERREUR", f"Erreur encodage image {image_path}: {e}", category="tutorial_generator")
            return None

    def _generate_placeholder_html(self, section: str, image_number: str, alt_text: str, 
                                 language: str, translations: Dict) -> str:
        """Génère un placeholder pour image manquante"""
        place_text = translations.get('ui', {}).get('place_image', "Placez l'image dans:")
        expected_path = os.path.join(self.images_dir, language, section, f"{image_number}.webp")
        
        return f'''
        <div class="image-placeholder" data-lang="{language}">
            <div class="placeholder-content">
                <span class="placeholder-icon">📷</span>
                <div class="placeholder-text">
                    <strong>[Image: {section}/{image_number}]</strong>
                    <br><small>{alt_text}</small>
                    <br><small style="opacity: 0.6;">{place_text}<br>{expected_path}</small>
                </div>
            </div>
        </div>
        '''

    def _generate_collapsible_html(self, section: str, image_number: str, base64_data: str,
                                 alt_text: str, caption_text: str, translations: Dict, language: str) -> str:
        """Génère le HTML pour une image collapsible"""
        # ID unique pour éviter les conflits
        safe_id = f"{section}_{image_number}".replace('/', '_').replace('-', '_')
        click_text = translations.get('ui', {}).get('click_to_see', 'Cliquez pour voir')
        
        display_text = caption_text if caption_text else alt_text
        
        return f'''
        <div class="image-container collapsible">
            <div class="image-toggle" onclick="toggleImage('{safe_id}')" role="button" tabindex="0" aria-expanded="false">
                <span class="toggle-icon" id="icon_{safe_id}">▶</span>
                <span class="toggle-text">{click_text} {display_text}</span>
            </div>
            <div class="tutorial-image" id="img_{safe_id}" style="display: none;">
                <img src="{base64_data}" alt="{alt_text}" class="responsive-image" />
                {f'<p class="image-caption">{caption_text}</p>' if caption_text else ''}
            </div>
        </div>
        '''

    def generate_tutorial_html(self, version: str = "Unknown", language: str = None) -> Optional[str]:
        """Génère le fichier HTML unique avec switch de langue intégré"""
        try:
            # Ignorer le paramètre language car on génère un fichier unique multilingue
            tutorial_name = "renextract_guide_complet.html"
            tutorial_path = os.path.join(self.tutorial_dir, tutorial_name)
            
            # Charger toutes les traductions
            all_translations = {}
            for lang in self.SUPPORTED_LANGUAGES:
                all_translations[lang] = self.load_translations(lang)
            
            if not any(all_translations.values()):
                log_message("ERREUR", "Impossible de charger les traductions", category="tutorial_generator")
                return None

            # Générer le contenu HTML
            html_content = self._generate_complete_html(version, all_translations)
            
            # Écrire le fichier
            with open(tutorial_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            log_message("INFO", f"Guide généré: {tutorial_path}", category="tutorial_generator")
            return tutorial_path

        except Exception as e:
            log_message("ERREUR", f"Erreur génération tutoriel HTML: {e}", category="tutorial_generator")
            return None

    def _generate_complete_html(self, version: str, all_translations: Dict[str, Dict]) -> str:
        """Génère le HTML complet avec toutes les langues - VERSION DEBUG"""
        log_message("INFO", "=== DÉBUT GÉNÉRATION HTML COMPLET ===", category="tutorial_generator")
        
        try:
            # Charger les modules de contenu avec debug détaillé
            content_modules = {}
            for i in range(1, 10):
                log_message("DEBUG", f"Tentative chargement module tab_{i:02d}", category="tutorial_generator")
                try:
                    module_name = f"ui.tutorial.content.tab_{i:02d}"
                    log_message("DEBUG", f"Import {module_name}", category="tutorial_generator")
                    content_modules[i] = __import__(module_name, fromlist=[f'tab_{i:02d}'])
                    log_message("INFO", f"✅ Module tab_{i:02d} chargé avec succès", category="tutorial_generator")
                except ImportError as e:
                    log_message("ERREUR", f"❌ Module tab_{i:02d} ÉCHEC ImportError: {e}", category="tutorial_generator")
                    content_modules[i] = None
                except Exception as e:
                    log_message("ERREUR", f"❌ Module tab_{i:02d} ÉCHEC Exception: {type(e).__name__}: {e}", category="tutorial_generator")
                    content_modules[i] = None

            # Debug: État des modules chargés
            log_message("INFO", f"Modules chargés: {[i for i, m in content_modules.items() if m is not None]}", category="tutorial_generator")
            log_message("INFO", f"Modules manqués: {[i for i, m in content_modules.items() if m is None]}", category="tutorial_generator")

            # Générer le contenu par onglet et par langue avec debug
            tab_contents = {}
            for tab_num in range(1, 10):
                log_message("INFO", f"--- Génération contenu onglet {tab_num} ---", category="tutorial_generator")
                
                module = content_modules.get(tab_num)
                if module is None:
                    log_message("ATTENTION", f"Module {tab_num} manquant, utilisation fallback", category="tutorial_generator")
                    tab_contents[tab_num] = self._get_fallback_tab_content(tab_num)
                else:
                    log_message("DEBUG", f"Module {tab_num} trouvé: {module}", category="tutorial_generator")
                    tab_contents[tab_num] = self._generate_tab_content(tab_num, module, all_translations)
                
                # Debug: vérifier la longueur du contenu généré
                content_length = len(tab_contents[tab_num])
                log_message("INFO", f"Onglet {tab_num} généré: {content_length} caractères", category="tutorial_generator")
                
                if content_length < 100:
                    log_message("ATTENTION", f"Contenu suspicieusement court pour onglet {tab_num}: {content_length} chars", category="tutorial_generator")

            # Générer le logo
            log_message("DEBUG", "Génération logo HTML", category="tutorial_generator")
            logo_html = self._generate_logo_html()

            # Utiliser le template de base
            log_message("DEBUG", "Récupération template HTML", category="tutorial_generator")
            html_template = self._get_html_template()
            
            # Variables pour le template
            template_vars = {
                'version': version,
                'logo_html': logo_html,
                'css_styles': self._get_complete_css(),
                'javascript': self._get_complete_javascript(),
                'all_translations_json': json.dumps(all_translations, ensure_ascii=False),
            }

            # Ajouter les contenus d'onglets avec debug
            for i in range(1, 10):
                content = tab_contents.get(i)
                if content:
                    template_vars[f'tab_content_{i}'] = content
                    log_message("DEBUG", f"Template: onglet {i} utilisé (contenu réel)", category="tutorial_generator")
                else:
                    template_vars[f'tab_content_{i}'] = self._get_fallback_tab_content(i)
                    log_message("ATTENTION", f"Template: onglet {i} fallback utilisé", category="tutorial_generator")
            log_message("DEBUG", "Formation HTML final avec template", category="tutorial_generator")
            final_html = html_template.format(**template_vars)
            
            log_message("INFO", f"HTML complet généré: {len(final_html)} caractères", category="tutorial_generator")
            log_message("INFO", "=== FIN GÉNÉRATION HTML COMPLET ===", category="tutorial_generator")
            
            return final_html

        except Exception as e:
            log_message("ERREUR", f"ERREUR CRITIQUE génération HTML complet: {type(e).__name__}: {e}", category="tutorial_generator")
            import traceback
            log_message("ERREUR", f"Traceback complet:\n{traceback.format_exc()}", category="tutorial_generator")
            return self._generate_fallback_html(version)

    def _generate_tab_content(self, tab_num: int, content_module: Any, all_translations: Dict[str, Dict]) -> str:
        """Génère le contenu d'un onglet pour toutes les langues - VERSION DEBUG"""
        log_message("DEBUG", f"=== GÉNÉRATION ONGLET {tab_num} DÉBUT ===", category="tutorial_generator")
        
        # Debug: Vérifier le module
        if content_module is None:
            log_message("ERREUR", f"Module content_module est None pour onglet {tab_num}", category="tutorial_generator")
            return self._get_fallback_tab_content(tab_num)
        
        if not hasattr(content_module, 'generate_content'):
            log_message("ERREUR", f"Module onglet {tab_num} n'a pas de fonction generate_content", category="tutorial_generator")
            return self._get_fallback_tab_content(tab_num)
        
        log_message("DEBUG", f"Module onglet {tab_num}: {content_module} - fonction trouvée", category="tutorial_generator")
        
        lang_panes = []
        
        for lang in self.SUPPORTED_LANGUAGES:
            log_message("DEBUG", f"Génération onglet {tab_num} langue {lang}", category="tutorial_generator")
            
            translations = all_translations[lang]
            
            # Debug: Vérifier les traductions
            if not translations:
                log_message("ATTENTION", f"Traductions vides pour onglet {tab_num} langue {lang}", category="tutorial_generator")
            else:
                log_message("DEBUG", f"Traductions onglet {tab_num} langue {lang}: {len(translations)} sections", category="tutorial_generator")
            
            try:
                log_message("DEBUG", f"Appel generate_content pour onglet {tab_num} langue {lang}", category="tutorial_generator")
                content = content_module.generate_content(self, lang, translations)
                log_message("DEBUG", f"Contenu généré pour onglet {tab_num} langue {lang}: {len(content)} caractères", category="tutorial_generator")
                
                # Debug: Vérifier le contenu généré
                if not content or len(content.strip()) == 0:
                    log_message("ATTENTION", f"Contenu vide généré pour onglet {tab_num} langue {lang}", category="tutorial_generator")
                    content = f"<p>Contenu vide pour onglet {tab_num} ({lang})</p>"
                
            except Exception as e:
                log_message("ERREUR", f"EXCEPTION lors génération onglet {tab_num} langue {lang}: {type(e).__name__}: {e}", category="tutorial_generator")
                import traceback
                log_message("ERREUR", f"Traceback complet:\n{traceback.format_exc()}", category="tutorial_generator")
                content = f"<p>Erreur de génération du contenu de l'onglet {tab_num} ({lang}): {e}</p>"
            
            # Chaque langue dans son propre panneau
            lang_panes.append(f'<div class="lang-pane" data-lang="{lang}">{content}</div>')
            log_message("DEBUG", f"Panneau langue {lang} ajouté pour onglet {tab_num}", category="tutorial_generator")
        
        final_content = '<div class="lang-stack">' + ''.join(lang_panes) + '</div>'
        log_message("DEBUG", f"=== ONGLET {tab_num} TERMINÉ - {len(final_content)} caractères ===", category="tutorial_generator")
        return final_content

    def _generate_logo_html(self) -> str:
        """Génère le HTML du logo - CORRIGÉ pour chercher logo_192"""
        # Essayer différents noms de fichiers pour le logo
        logo_names = ["logo_192", "001", "logo", "main_logo"]
        
        for logo_name in logo_names:
            logo_path = self._find_image_with_fallback("06_logos", logo_name, "fr")
            if logo_path:
                logo_base64 = self._encode_image_to_base64(logo_path)
                if logo_base64:
                    log_message("INFO", f"Logo trouvé: {logo_path}", category="tutorial_generator")
                    return f'<img src="{logo_base64}" alt="RenExtract Logo" class="header-logo">'
        
        log_message("ATTENTION", "Aucun logo trouvé, utilisation du placeholder", category="tutorial_generator")
        return '<div class="logo-placeholder">RenExtract</div>'

    def _get_fallback_tab_content(self, tab_num: int) -> str:
        """Contenu de fallback pour un onglet - VERSION DEBUG"""
        log_message("DEBUG", f"Génération fallback pour onglet {tab_num}", category="tutorial_generator")
        
        fallback_content = f'''
        <div class="lang-stack">
            <div class="lang-pane" data-lang="fr">
                <div class="section">
                    <h2>Onglet {tab_num}</h2>
                    <p>Contenu en cours de développement.</p>
                    <p><strong>DEBUG:</strong> Ce contenu est généré par le système de fallback car le module tab_{tab_num:02d}.py n'a pas pu être chargé ou a généré une erreur.</p>
                </div>
            </div>
            <div class="lang-pane" data-lang="en">
                <div class="section">
                    <h2>Tab {tab_num}</h2>
                    <p>Content under development.</p>
                    <p><strong>DEBUG:</strong> This content is generated by fallback system because tab_{tab_num:02d}.py module could not be loaded or generated an error.</p>
                </div>
            </div>
            <div class="lang-pane" data-lang="de">
                <div class="section">
                    <h2>Registerkarte {tab_num}</h2>
                    <p>Inhalt in Entwicklung.</p>
                    <p><strong>DEBUG:</strong> Dieser Inhalt wird vom Fallback-System generiert, da das Modul tab_{tab_num:02d}.py nicht geladen werden konnte oder einen Fehler verursacht hat.</p>
                </div>
            </div>
        </div>
        '''
        
        return fallback_content

    def _get_html_template(self) -> str:
        """Template HTML moderne"""
        return """<!DOCTYPE html>
<html lang="fr" data-lang="fr" data-theme="dark">
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
            <h1 id="main-title">Guide Complet RenExtract</h1>
            <p id="version-text">Version {version}</p>
        </div>
    </header>

    <nav class="nav-tabs">
        <button class="nav-tab active" data-tab="1" id="tab-btn-1">📋 Sommaire</button>
        <button class="nav-tab" data-tab="2" id="tab-btn-2">🔄 Workflow</button>
        <button class="nav-tab" data-tab="3" id="tab-btn-3">🖥️ Interface</button>
        <button class="nav-tab" data-tab="4" id="tab-btn-4">🎮 Générateur</button>
        <button class="nav-tab" data-tab="5" id="tab-btn-5">🛠️ Outils</button>
        <button class="nav-tab" data-tab="6" id="tab-btn-6">💾 Sauvegardes</button>
        <button class="nav-tab" data-tab="7" id="tab-btn-7">⚙️ Paramètres</button>
        <button class="nav-tab" data-tab="8" id="tab-btn-8">🔧 Technique</button>
        <button class="nav-tab" data-tab="9" id="tab-btn-9">❓ FAQ</button>
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

    {javascript}
    <script>window.ALL_TRANSLATIONS = {all_translations_json};</script>
</body>
</html>"""

    def _get_complete_css(self) -> str:
        """CSS complet avec nouveau schéma de couleurs et navigation directe"""
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
.theme-toggle, .lang-selector, .nav-home-btn { 
  background: var(--card-bg); 
  border: 1px solid var(--sep); 
  border-radius: 12px; 
  padding: 12px; 
  cursor: pointer; 
  transition: all 0.2s; 
  box-shadow: 0 4px 12px rgba(0,0,0,0.3); 
  min-width: 120px; 
  min-height: 48px; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
}

.theme-toggle { background: var(--card-bg); color: var(--accent); font-size: 1.5em; min-width: 48px; }
.nav-home-btn { color: var(--accent); font-size: 1.2em; font-weight: bold; min-width: 48px; }

.flag-container {
  display: flex;
  gap: 8px;
  align-items: center;
}

.flag-option {
  font-size: 16px;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
  cursor: pointer;
  opacity: 0.6;
}

.flag-option.active {
  opacity: 1;
  background: rgba(74, 144, 226, 0.2);
}

.flag-option:hover {
  opacity: 1;
  transform: scale(1.1);
}
.lang-dropdown { 
  position: absolute; top: 100%; right: 0; background: var(--card-bg); 
  border: 1px solid var(--sep); border-radius: 8px; padding: 8px; min-width: 120px; 
  box-shadow: 0 8px 24px rgba(0,0,0,0.4); opacity: 0; visibility: hidden; 
  transform: translateY(-10px); transition: all 0.2s; margin-top: 8px; 
}
.lang-selector.open .lang-dropdown { opacity: 1; visibility: visible; transform: translateY(0); }
.lang-option { 
  display: flex; align-items: center; gap: 8px; padding: 8px; border-radius: 6px; 
  cursor: pointer; transition: background 0.2s; 
}
.lang-option:hover, .lang-option.active { background: var(--accent); color: white; }

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
.logo-corner img { 
  width: 70px; height: 70px; border-radius: 12px; 
  box-shadow: 0 4px 12px rgba(0,0,0,0.3); transition: all 0.2s; 
}
.logo-corner:hover img { transform: scale(1.1); }

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
</style>"""

    def _get_complete_javascript(self) -> str:
        """JavaScript complet avec navigation directe par onglets"""
        return """<script>
(function() {
  let currentLanguage = 'fr', currentTheme = 'dark';
  
  function ready(fn) { if (document.readyState !== 'loading') fn(); else document.addEventListener('DOMContentLoaded', fn); }
  function save(key, value) { try { localStorage.setItem('renextract_' + key, JSON.stringify(value)); } catch(e) {} }
  function load(key, def) { try { const s = localStorage.getItem('renextract_' + key); return s ? JSON.parse(s) : def; } catch(e) { return def; } }
  
  function applyTheme(theme) {
    currentTheme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    const btn = document.getElementById('theme-toggle');
    if (btn) { btn.textContent = theme === 'dark' ? '☀️' : '🌙'; btn.title = theme === 'dark' ? 'Thème clair' : 'Thème sombre'; }
    save('theme', theme);
    positionFloatingControls();
  }
  
  function applyLanguage(lang) {
    currentLanguage = lang;
    document.querySelectorAll('.lang-pane').forEach(p => { p.classList.remove('active'); p.style.display = 'none'; });
    document.querySelectorAll('.lang-pane[data-lang="' + lang + '"]').forEach(p => { p.classList.add('active'); p.style.display = 'block'; });
    document.documentElement.setAttribute('lang', lang);
    updateInterfaceTexts(lang);
    updateLanguageSelector(lang);
    save('language', lang);
  }

  function updateLanguageFlags() {
    document.querySelectorAll('.flag-option').forEach(flag => {
      flag.classList.toggle('active', flag.getAttribute('data-lang') === currentLanguage);
    });
  }  

  function updateInterfaceTexts(lang) {
    if (window.ALL_TRANSLATIONS && window.ALL_TRANSLATIONS[lang]) {
      const ui = window.ALL_TRANSLATIONS[lang].ui || {};
      const title = document.getElementById('main-title');
      if (title && ui.main_title) title.textContent = ui.main_title;
      
      const tabs = { 1: ui.tab_summary || '📋 Sommaire', 2: ui.tab_workflow || '📄 Workflow', 3: ui.tab_interface || '🖥️ Interface', 4: ui.tab_generator || '⚙️ Générateur', 5: ui.tab_tools || '🛠️ Outils', 6: ui.tab_backup || '💾 Sauvegardes', 7: ui.tab_settings || '⚙️ Paramètres', 8: ui.tab_technical || '🔧 Technique', 9: ui.tab_faq || '❓ FAQ' };
      Object.entries(tabs).forEach(([n, t]) => { const btn = document.getElementById('tab-btn-' + n); if (btn) btn.textContent = t; });
    }
  }
  
  function updateLanguageSelector(lang) {
    const flag = document.querySelector('.current-flag');
    if (flag) { flag.textContent = { fr: '🇫🇷', en: '🇬🇧', de: '🇩🇪' }[lang] || '🇫🇷'; }
    document.querySelectorAll('.lang-option').forEach(o => o.classList.remove('active'));
    const active = Array.from(document.querySelectorAll('.lang-option')).find(o => o.querySelector('.flag-emoji').textContent === ({ fr: '🇫🇷', en: '🇬🇧', de: '🇩🇪' }[lang] || '🇫🇷'));
    if (active) active.classList.add('active');
  }
  
  // Position avec gestion du scroll
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
    themeBtn.addEventListener('click', () => applyTheme(currentTheme === 'dark' ? 'light' : 'dark'));
    
    const langSelector = document.createElement('div');
    langSelector.className = 'lang-selector';
    const flagContainer = document.createElement('div');
    flagContainer.className = 'flag-container';
    flagContainer.innerHTML = `
      <span class="flag-option ${currentLanguage === 'fr' ? 'active' : ''}" data-lang="fr">🇫🇷</span>
      <span class="flag-option ${currentLanguage === 'en' ? 'active' : ''}" data-lang="en">🇬🇧</span>
      <span class="flag-option ${currentLanguage === 'de' ? 'active' : ''}" data-lang="de">🇩🇪</span>
    `;

    flagContainer.addEventListener('click', (e) => {
      const flagSpan = e.target.closest('.flag-option');
      if (flagSpan) {
        const lang = flagSpan.getAttribute('data-lang');
        applyLanguage(lang);
        updateLanguageFlags();
      }
    });
    
    langSelector.appendChild(flagContainer);
    
    const homeBtn = document.createElement('button');
    homeBtn.className = 'nav-home-btn';
    homeBtn.textContent = '📋';
    homeBtn.title = 'Retour au sommaire';
    homeBtn.addEventListener('click', () => { const tab = document.querySelector('.nav-tab[data-tab="1"]'); if (tab) tab.click(); });
    
    container.append(themeBtn, langSelector, homeBtn);
    document.body.appendChild(container);
    
    const backBtn = document.createElement('button');
    backBtn.className = 'back-to-top';
    backBtn.textContent = '↑';
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
      });
    });
    const saved = load('activeTab', 0);
    if (tabs[saved] && contents[saved]) { tabs.forEach(t => t.classList.remove('active')); contents.forEach(c => c.classList.remove('active')); tabs[saved].classList.add('active'); contents[saved].classList.add('active'); }
  }
  
  // NOUVELLE FONCTION : Navigation directe par onglets
  function setupDirectNavigation() {
    document.addEventListener('click', function(e) {
      const navBtn = e.target.closest('.nav-link-btn');
      if (!navBtn) return;
      
      e.preventDefault();
      e.stopPropagation();
      
      const targetTab = parseInt(navBtn.getAttribute('data-target-tab'));
      const targetSection = navBtn.getAttribute('data-target-section');
      
      console.log(`Navigation vers onglet ${targetTab}, section ${targetSection}`);
      
      if (targetTab) {
        // Changer d'onglet immédiatement
        switchToTabDirect(targetTab);
        
        // Faire défiler vers la section après changement d'onglet
        if (targetSection) {
          setTimeout(() => {
            const targetElement = document.getElementById(targetSection);
            if (targetElement) {
              targetElement.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start',
                inline: 'nearest'
              });
              
              // Effet visuel de surbrillance
              targetElement.style.transition = 'all 0.5s ease';
              targetElement.style.backgroundColor = 'rgba(74, 144, 226, 0.2)';
              targetElement.style.transform = 'scale(1.01)';
              
              setTimeout(() => {
                targetElement.style.backgroundColor = '';
                targetElement.style.transform = 'scale(1)';
              }, 1500);
              
              console.log(`Scroll vers section ${targetSection} effectué`);
            } else {
              console.warn(`Section ${targetSection} non trouvée`);
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
        
        console.log(`Onglet ${tabNumber} activé`);
      } else {
        console.error(`Onglet ${tabNumber} non trouvé`);
      }
    }
  }
  
  window.toggleImage = function(id) {
    const img = document.getElementById('img_' + id);
    const toggle = document.querySelector('.image-toggle[onclick*="' + id + '"]');
    if (!img) return;
    const isHidden = img.style.display === 'none' || img.style.display === '';
    if (isHidden) { img.style.display = 'block'; img.style.opacity = '0'; img.offsetHeight; img.style.transition = 'opacity 0.3s ease'; img.style.opacity = '1'; } else { img.style.opacity = '0'; setTimeout(() => img.style.display = 'none', 300); }
    if (toggle) { toggle.classList.toggle('expanded', isHidden); toggle.setAttribute('aria-expanded', isHidden); }
    const states = load('imageStates', {}); states[id] = isHidden; save('imageStates', states);
  };
  
  function initImageToggles() {
    document.querySelectorAll('.image-toggle').forEach(toggle => {
      toggle.setAttribute('role', 'button');
      toggle.setAttribute('tabindex', '0');
      toggle.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); const match = toggle.getAttribute('onclick').match(/toggleImage\\('([^']+)'\\)/); if (match) window.toggleImage(match[1]); } });
    });
    const states = load('imageStates', {});
    Object.entries(states).forEach(([id, open]) => { if (open) { const img = document.getElementById('img_' + id); const toggle = document.querySelector('.image-toggle[onclick*="' + id + '"]'); if (img && toggle) { img.style.display = 'block'; toggle.classList.add('expanded'); } } });
  }
  
  ready(() => {
    currentTheme = load('theme', 'dark');
    currentLanguage = load('language', 'fr');
    applyTheme(currentTheme);
    applyLanguage(currentLanguage);
    initTabs();
    initImageToggles();
    createFloatingControls();
    positionFloatingControls();
    setupDirectNavigation(); // AJOUT CRUCIAL
    console.log('App initialisée avec navigation directe par onglets');
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