# utils/logging.py — HTML-only logger + filtres + badges + panneau catégories + debug idempotent + AUTO-REFRESH
import os, glob, datetime, threading, html as _html
from pathlib import Path
from queue import Queue, Empty
import atexit, time

# ====== CONFIG PAR DÉFAUT (surchargée par config_manager si présent) ======
MAX_LOG_FILES = 5               # nombre max de fichiers HTML conservés
MAX_FILE_SIZE_MB = 50            # rotation quand on dépasse cette taille (Mo)
LOG_ENCODING = "utf-8"

# HTML options
HTML_FLUSH_MS = 200             # flush batch toutes X ms
HTML_MAX_SIZE_MB = 50           # coupe l'HTML runtime s'il dépasse cette taille (Mo)
HTML_THEME = "dark"             # "dark" | "light" (défaut dark)

# ⬇️ Nouveautés: auto-refresh
HTML_AUTO_REFRESH = False       # auto-refresh OFF par défaut (peut être surchargé par config.json)
HTML_AUTO_REFRESH_SECONDS = 30   # intervalle en secondes

# ====== NIVEAUX ======
LOG_LEVELS = {"ERROR":1,"ERREUR":1,"WARNING":2,"ATTENTION":2,"INFO":3,"DEBUG":4,"TRACE":5}

# Palette primaire cohérente (Bootstrap-like)
_HTML_LEVEL_COLORS = {
    "DEBUG":     "#0D6EFD",  # Bleu primaire
    "INFO":      "#198754",  # Vert succès
    "ATTENTION": "#FFC107",  # Jaune alerte
    "WARNING":   "#FFC107",
    "ERREUR":    "#DC3545",  # Rouge danger
    "ERROR":     "#DC3545",
    "TRACE":     "#6F42C1",  # Violet primaire
}

def _css_common() -> str:
    return """
    <style>
      :root{
        --bg:#121212; --fg:#eaeaea; --hdr:#1e1e1e; --sep:#262626;
        --fg-dim:rgba(234,234,234,.85); --fg-muted:rgba(234,234,234,.6);
        --badge-bg:#1f1f1f;
      }
      .light{
        --bg:#fafafa; --fg:#222; --hdr:#fff; --sep:#ddd;
        --fg-dim:rgba(34,34,34,.85); --fg-muted:rgba(34,34,34,.6);
        --badge-bg:#f1f1f1;
      }
      body{font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Arial; background:var(--bg); color:var(--fg); margin:0}
      .hdr{display:flex; gap:12px; align-items:center; padding:12px 16px; background:var(--hdr); border-bottom:1px solid var(--sep); position:sticky; top:0; z-index:10; flex-wrap:wrap}
      .hdr .title{font-weight:700}
      .hdr .right{margin-left:auto; display:flex; gap:8px; align-items:center}
      .btn{cursor:pointer; padding:6px 10px; border-radius:8px; border:1px solid var(--sep); background:transparent; color:var(--fg)}
      .btn:hover{background:rgba(255,255,255,.06)}
      .field{display:flex; gap:6px; align-items:center}
      .field input,.field select{background:var(--bg); color:var(--fg); border:1px solid var(--sep); padding:6px 8px; border-radius:8px; outline:none}
      select option{ background:var(--hdr); color:var(--fg); }

      .badges{display:flex; gap:6px; align-items:center; flex-wrap:wrap}
      .badge{display:inline-flex; gap:6px; align-items:center; padding:4px 8px; border-radius:999px; background:var(--badge-bg); border:1px solid var(--sep); font-size:.9rem; color:var(--fg);}  /* <-- fg adapté au thème */

      .b-info{border-left:6px solid #198754}
      .b-warn{border-left:6px solid #FFC107}
      .b-err{ border-left:6px solid #DC3545}
      .b-debug{border-left:6px solid #0D6EFD}
      .b-trace{border-left:6px solid #6F42C1}

      .logs{padding:0 0 24px}
      .log{padding:10px 16px; border-bottom:1px solid var(--sep); white-space:pre-wrap; word-break:break-word}
      .dense .log{padding:6px 12px}
      .ts{opacity:.7; margin-right:6px}
      .lvl{font-weight:700; margin-right:6px}
      .cat{color:var(--fg-dim); margin-right:6px}
      .src{color:var(--fg-muted); margin-right:6px}
      .lvl-DEBUG{color:#0D6EFD}
      .lvl-INFO{color:#198754}
      .lvl-ATTENTION,.lvl-WARNING{color:#FFC107}
      .lvl-ERREUR,.lvl-ERROR{color:#DC3545}
      .lvl-TRACE{color:#6F42C1}

      /* Panneau catégories */
      .catpanel-wrap{width:100%; display:none}
      .catpanel{margin:8px 16px 0; padding:10px; border:1px dashed var(--sep); border-radius:12px; background:rgba(0,0,0,.04)}
      .catlist{display:flex; flex-wrap:wrap; gap:6px}
      .pill{cursor:pointer; padding:4px 8px; border-radius:999px; border:1px solid var(--sep); background:var(--badge-bg); color:var(--fg);} /* <-- fg adapté au thème */
      .pill:hover{background:rgba(255,255,255,.06)}
      .pill.active{outline:2px solid #0D6EFD}

      /* Deux lignes dans l'en-tête */
      .hdr-row{display:flex; gap:12px; align-items:center; width:100%;}
      .hdr-row.bottom{margin-top:8px}
      
      /* Badge auto-refresh */
      #autoBadge{ opacity:.45; border-left:6px solid var(--sep); }
      #autoBadge.on{ opacity:1; border-left-color:#0D6EFD; }
    </style>
    """

def _header_html(theme_default: str, debug_default: bool, known_categories_json: str = "[]") -> str:
    theme_label = "Sombre" if theme_default == "dark" else "Clair"
    return f"""
    <div class="hdr">
      <!-- Ligne 1: titre + filtres + actions -->
      <div class="hdr-row top">
        <div class="title">RenExtract – Journal HTML</div>

        <div class="field">
          <label for="levelFilter">Niveau mini</label>
          <select id="levelFilter">
            <option value="0">Tous</option>
            <option value="3">INFO+</option>
            <option value="2">ATTENTION+</option>
            <option value="1">ERREUR+</option>
            <option value="4">DEBUG seulement</option>
            <option value="5">TRACE seulement</option>
          </select>
        </div>

        <div class="field">
          <label for="catFilter">Catégories</label>
          <input id="catFilter" placeholder="ex: init_ui,ui_main">
          <button id="catInfoBtn" class="btn" title="Voir toutes les catégories">ℹ️</button>
        </div>

        <div class="right">
          <button id="densityToggle" class="btn">Densité</button>
          <span class="badge autoBadge" id="autoBadge" title="Auto-refresh actif">AUTO</span>
          <button id="autoRefreshToggle" class="btn">Auto-refresh: OFF</button>
          <button id="themeToggle" class="btn">Thème: {theme_label}</button>
        </div>
      </div>

      <!-- Ligne 2: compteurs + sauts rapides -->
      <div class="hdr-row bottom">
        <div class="badges" id="counters">
          <span class="badge b-info">INFO <strong id="c-info">0</strong></span>
          <span class="badge b-warn">ATTENTION <strong id="c-warn">0</strong></span>
          <span class="badge b-err">ERREUR <strong id="c-err">0</strong></span>
          <span class="badge b-debug">DEBUG <strong id="c-debug">0</strong></span>
          <span class="badge b-trace">TRACE <strong id="c-trace">0</strong></span>
          <button id="jumpWarn" class="btn">↪ 1er WARNING</button>
          <button id="jumpErr"  class="btn">↪ 1re ERREUR</button>
        </div>
      </div>

      <!-- Panneau catégories -->
      <div class="catpanel-wrap" id="catPanelWrap">
        <div class="catpanel">
          <div style="margin-bottom:6px;opacity:.8">Catégories disponibles (clic = ajouter/retirer du filtre) :</div>
          <div class="catlist" id="catList"></div>
        </div>
      </div>
    </div>

    <!-- Liste injectée par Python (connue côté app) -->
    <script>window.__RENEX_KNOWN_CATEGORIES__ = {known_categories_json};</script>

    <script>
      (function() {{
        const byId = (x)=>document.getElementById(x);
        let   levelSel = byId('levelFilter');
        const catInp   = byId('catFilter');
        const body     = document.body;
        const rows     = () => document.querySelectorAll('.log');
        const keyTheme = 'renextract_html_log_theme';

        function repaintSelect() {{
          try {{
            const v = levelSel.value;
            const n = levelSel.cloneNode(true);
            n.value = v;
            levelSel.parentNode.replaceChild(n, levelSel);
            levelSel = n;
            levelSel.addEventListener('change', applyFilter);
          }} catch(e) {{}}
        }}

        // Thème initial (localStorage > valeur par défaut)
        const savedTheme = localStorage.getItem(keyTheme);
        const initial = savedTheme || '{theme_default}';
        if (initial === 'light') body.classList.add('light');

        function setTheme(t) {{
          if (t==='light') body.classList.add('light'); else body.classList.remove('light');
          localStorage.setItem(keyTheme, t);
          byId('themeToggle').textContent = 'Thème: ' + (t==='dark' ? 'Sombre' : 'Clair');
          repaintSelect();
        }}
        byId('themeToggle').addEventListener('click', ()=> {{
          setTheme(body.classList.contains('light') ? 'dark' : 'light');
        }});

        // Densité compacte
        byId('densityToggle').addEventListener('click', ()=> {{
          document.querySelector('.logs')?.classList.toggle('dense');
        }});

        // Initialisation du filtre niveau mini
        const savedMin = localStorage.getItem('renextract_min_level');
        levelSel.value = savedMin ? String(savedMin) : '0';

        function updateCounters() {{
          const visible = Array.from(rows()).filter(r => r.style.display !== 'none');
          const get = lvl => visible.filter(r => r.dataset.level === lvl).length;
          byId('c-info').textContent  = get('INFO');
          byId('c-warn').textContent  = get('ATTENTION') + get('WARNING');
          byId('c-err').textContent   = get('ERREUR') + get('ERROR');
          byId('c-debug').textContent = get('DEBUG');
          byId('c-trace').textContent = get('TRACE');
        }}

        function applyFilter() {{
          const min  = parseInt(levelSel.value || '0', 10);
          const cats = (catInp.value||'').trim().toLowerCase().split(',').map(s=>s.trim()).filter(Boolean);

          document.querySelectorAll('.log').forEach(row => {{
            const prio = parseInt(row.dataset.levelprio||'3',10);
            const cat  = (row.dataset.category||'').toLowerCase();
            let show = true;

            if (min === 4)       show = (row.dataset.level === 'DEBUG');
            else if (min === 5)  show = (row.dataset.level === 'TRACE');
            else if (min > 0)    show = (prio <= min);

            if (show && cats.length) show = cats.some(f => cat.includes(f));
            row.style.display = show ? '' : 'none';
          }});

          localStorage.setItem('renextract_min_level', levelSel.value);
          updateCounters();
        }}

        // Sauts rapides
        function jumpTo(pred) {{
          const el = Array.from(rows()).find(r => r.style.display !== 'none' && pred(r));
          if (el) el.scrollIntoView({{behavior:'smooth', block:'center'}});
        }}
        byId('jumpWarn').addEventListener('click', ()=> jumpTo(r => r.dataset.level==='ATTENTION' || r.dataset.level==='WARNING'));
        byId('jumpErr') .addEventListener('click', ()=> jumpTo(r => r.dataset.level==='ERREUR'   || r.dataset.level==='ERROR'));

        // Panneau catégories
        function collectCategories() {{
          const injected = Array.isArray(window.__RENEX_KNOWN_CATEGORIES__) ? window.__RENEX_KNOWN_CATEGORIES__ : [];
          const set = new Set(injected.map(s => String(s)));
          rows().forEach(r=>{{ const c=r.dataset.category||''; if(c) set.add(c); }});
          return Array.from(set).sort((a,b)=>a.localeCompare(b));
        }}

        function renderCatPanel() {{
          const list = byId('catList'); list.innerHTML='';
          const selected = new Set((catInp.value||'').toLowerCase().split(',').map(s=>s.trim()).filter(Boolean));
          collectCategories().forEach(cat => {{
            const pill = document.createElement('button');
            pill.className = 'pill' + (selected.has(cat.toLowerCase()) ? ' active' : '');
            pill.textContent = cat;
            pill.title = 'Ajouter/retirer au filtre';
            pill.addEventListener('click', ()=>{{
              const arr = (catInp.value||'').split(',').map(s=>s.trim()).filter(Boolean);
              const idx = arr.findIndex(x=>x.toLowerCase()===cat.toLowerCase());
              if (idx>=0) arr.splice(idx,1); else arr.push(cat);
              catInp.value = arr.join(', ');
              applyFilter();
              renderCatPanel();
            }});
            list.appendChild(pill);
          }});
        }}
        const wrap = byId('catPanelWrap');
        byId('catInfoBtn').addEventListener('click', ()=> {{
          wrap.style.display = (wrap.style.display==='block' ? 'none' : 'block');
          if (wrap.style.display==='block') renderCatPanel();
        }});

        // === Auto-refresh INTELLIGENT ===
        const arCfg = window.__RENEX_AUTO_REFRESH__ || {{enabled:false, seconds:30}};
        const keyAR = 'renextract_auto_refresh';
        const keyScroll = 'renextract_scroll_' + location.pathname;

        let autoRefresh = (localStorage.getItem(keyAR) ?? (arCfg.enabled ? '1':'0')) === '1';
        let arTimer = null;
        let autoStoppedReason = null; // Raison de l'arrêt automatique

        function updateARBtn(){{
          const b  = byId('autoRefreshToggle');
          const ab = byId('autoBadge');
          
          if (b) {{
            let text = 'Auto-refresh: ';
            if (autoStoppedReason) {{
              text += 'ARRÊTÉ (' + autoStoppedReason + ')';
            }} else {{
              text += (autoRefresh ? 'ON' : 'OFF');
            }}
            b.textContent = text;
            
            // Changer la couleur du bouton si arrêté automatiquement
            if (autoStoppedReason) {{
              b.style.background = '#FFC107';
              b.style.color = '#000';
            }} else {{
              b.style.background = '';
              b.style.color = '';
            }}
          }}
          
          if (ab) {{
            const isActive = autoRefresh && !autoStoppedReason;
            ab.classList.toggle('on', isActive);
            ab.style.opacity = isActive ? '1' : '.45';
            
            // Mettre à jour le title avec la raison d'arrêt
            if (autoStoppedReason) {{
              ab.title = 'Auto-refresh arrêté: ' + autoStoppedReason;
            }} else {{
              ab.title = 'Auto-refresh actif';
            }}
          }}
        }}

        function stopAR(reason){{ 
          if (arTimer) {{ 
            clearInterval(arTimer); 
            arTimer = null; 
          }}
          if (reason) {{
            autoStoppedReason = reason;
            console.log('[RenExtract Log] Auto-refresh arrêté: ' + reason);
          }}
        }}

        // Vérification intelligente avant chaque refresh
        function shouldContinueAutoRefresh() {{
          const allLogs = rows();
          if (allLogs.length === 0) {{
            stopAR("Aucun log présent");
            return false;
          }}

          // Récupérer le timestamp du dernier log
          const lastLog = allLogs[allLogs.length - 1];
          const lastTimestamp = lastLog.querySelector('.ts');
          
          if (!lastTimestamp) {{
            stopAR("Impossible de lire le timestamp");
            return false;
          }}

          try {{
            // Parser le timestamp (format: "YYYY-MM-DD HH:MM:SS.mmm")
            const timestampText = lastTimestamp.textContent.trim();
            const lastLogTime = new Date(timestampText.replace(/\\.\\d{{3}}$/, '')); // Enlever les millisecondes
            const now = new Date();
            const diffMinutes = (now - lastLogTime) / (1000 * 60);

            // Arrêter si le dernier log est trop vieux (> 5 minutes)
            const maxInactivityMinutes = 5;
            if (diffMinutes > maxInactivityMinutes) {{
              const roundedMinutes = Math.round(diffMinutes);
              stopAR('Inactif depuis ' + roundedMinutes + ' min');
              return false;
            }}

          }} catch(e) {{
            console.warn('[RenExtract Log] Erreur parsing timestamp:', e);
            // En cas d'erreur, on continue mais on log l'avertissement
          }}

          // Vérifier la présence d'un log de fermeture d'application
          const shutdownPatterns = [
            /fermeture.*application/i,
            /application.*fermée/i, 
            /fin.*session/i,
            /session.*terminée/i,
            /arrêt.*programme/i,
            /programme.*arrêté/i,
            /shutdown/i,
            /exit/i,
            /quit/i
          ];

          // Vérifier les 10 derniers logs pour un message de fermeture
          const recentLogs = Array.from(allLogs).slice(-10);
          for (let i = 0; i < recentLogs.length; i++) {{
            const logRow = recentLogs[i];
            const msgElement = logRow.querySelector('.msg');
            if (msgElement) {{
              const msgText = msgElement.textContent.toLowerCase();
              for (let j = 0; j < shutdownPatterns.length; j++) {{
                const pattern = shutdownPatterns[j];
                if (pattern.test(msgText)) {{
                  stopAR("Application fermée");
                  return false;
                }}
              }}
            }}
          }}

          return true;
        }}

        function startAR(){{
          stopAR(); // Clear any existing timer
          autoStoppedReason = null; // Reset la raison d'arrêt
          
          if (!autoRefresh) return;

          // Vérification initiale
          if (!shouldContinueAutoRefresh()) {{
            updateARBtn();
            return;
          }}

          const every = Math.max(1, parseInt(arCfg.seconds||30, 10)) * 1000;
          arTimer = setInterval(function() {{
            // Vérification avant chaque refresh
            if (!shouldContinueAutoRefresh()) {{
              updateARBtn();
              return; // Le timer sera nettoyé par stopAR()
            }}

            try {{ 
              localStorage.setItem(keyScroll, String(window.scrollY||0)); 
            }} catch(e) {{}}
            
            location.reload();
          }}, every);
        }}

        // Gestionnaire de clic sur le bouton
        byId('autoRefreshToggle').addEventListener('click', function() {{
          if (autoStoppedReason) {{
            // Si c'était arrêté automatiquement, permettre le redémarrage manuel
            autoRefresh = true;
            autoStoppedReason = null;
            console.log('[RenExtract Log] Auto-refresh redémarré manuellement');
          }} else {{
            // Toggle normal
            autoRefresh = !autoRefresh;
          }}
          
          try {{ 
            localStorage.setItem(keyAR, autoRefresh ? '1' : '0'); 
          }} catch(e) {{}}
          
          updateARBtn();
          startAR();
        }});

        levelSel.addEventListener('change', applyFilter);
        catInp.addEventListener('input', function() {{ applyFilter(); renderCatPanel(); }});

        window.addEventListener('load', function() {{
          // Restaurer la position de scroll si on vient d'un auto-refresh
          const sy = parseInt(localStorage.getItem(keyScroll) || '0', 10);
          if (sy > 0) {{ window.scrollTo(0, sy); localStorage.removeItem(keyScroll); }}

          updateARBtn();
          startAR();
          applyFilter();
          renderCatPanel();
        }});
      }})();
    </script>
    """

class HtmlOnlyLogger:
    def __init__(self, app_version="inconnue"):
        self.app_version = app_version
        self._lock = threading.Lock()
        self.log_dir = self._get_log_directory()
        self.log_prefix = "renextract_log"
        self.current_html_file = None
        self.current_txt_file = None  # ✅ NOUVEAU
        self.debug_enabled = False
        self.log_level = 3
        self.log_format = "html"  # ✅ NOUVEAU : format des logs
        self._html_q = Queue()
        self._html_thread = None
        self._html_running = False
        self._html_disabled_runtime = False
        self._load_config()
        self._ensure_log_directory()
        self._initialize_logging()

    # --- API ---
    def set_app_version(self, app_version): 
        with self._lock: self.app_version = app_version

    def _resolved_version(self):
        v = self.app_version or "inconnue"
        if v == "inconnue":
            try:
                from .constants import VERSION as _V
                if _V: v = str(_V)
            except Exception:
                pass
        return v

    def set_debug(self, enabled: bool, level: int = None):
        prev = self.debug_enabled
        
        # Vérifier si l'utilisateur a activé le mode debug
        user_debug_enabled = False
        try:
            import json
            config_path = os.path.join(self._get_config_dir(), "config.json")
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                user_debug_enabled = bool(config.get('debug_mode', False))
        except Exception:
            pass
        
        # Si l'utilisateur a activé le debug, ne pas le désactiver
        if not enabled and user_debug_enabled:
            return  # Ne pas désactiver le debug si l'utilisateur l'a activé
        
        self.debug_enabled = bool(enabled)
        self.log_level = int(level if level is not None else (5 if self.debug_enabled else 3))
        if self.debug_enabled != prev:
            self.log_message("INFO", "Mode debug {s}", s=("activé" if self.debug_enabled else "désactivé"),
                            category="utils_logging")

    # compat
    def enable_debug_mode(self, categories=None): self.set_debug(True, 5)
    def disable_debug_mode(self): self.set_debug(False, 3)

    def log_message(self, level, message, *args, **kwargs):
        exception    = kwargs.pop("exception", None)
        category     = kwargs.pop("category", None)
        custom_color = kwargs.pop("color", None)
        if not self._should_log_message(level, category): return
        with self._lock:
            try:   final = str(message).format(*args, **kwargs) if (args or kwargs) else str(message)
            except (IndexError, KeyError): final = f"{message} (Erreur de formatage des arguments)"
            self._rotate_if_needed()
            
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            debug_src = ""
            if self.debug_enabled and LOG_LEVELS.get((level or '').upper(), 3) >= 4:
                try:
                    import inspect
                    frame = inspect.currentframe()
                    while frame and frame.f_code.co_filename == __file__: frame = frame.f_back
                    if frame: debug_src = f"{os.path.basename(frame.f_code.co_filename)}:{frame.f_lineno}"
                except Exception: pass
            
            # ✅ FORMAT TXT : Logger en .txt
            if self.log_format == "txt" and self.current_txt_file:
                try:
                    txt_line = self._format_txt_row(ts, level, category or "general", debug_src, final, exception)
                    with open(self.current_txt_file, "a", encoding=LOG_ENCODING) as tf:
                        tf.write(txt_line)
                except Exception: pass
            
            # ✅ FORMAT HTML : Logger en .html
            elif self.log_format == "html" and self.current_html_file and not self._html_disabled_runtime:
                try:
                    line = self._format_html_row(ts, level, category or "general", debug_src, final, custom_color, exception)
                    self._html_q.put(line)
                except Exception: pass

    # --- internes ---
    def _get_log_directory(self):
        try:
            from .constants import FOLDERS
            return FOLDERS["configs"]
        except Exception:
            try:
                import sys
                base_dir = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(sys.argv[0]))
                return os.path.join(base_dir, "04_Configs")
            except Exception:
                return "."

    def _load_config(self):
        global MAX_LOG_FILES, MAX_FILE_SIZE_MB, HTML_FLUSH_MS, HTML_MAX_SIZE_MB, HTML_THEME, HTML_AUTO_REFRESH, HTML_AUTO_REFRESH_SECONDS
        
        try:
            # ✅ CORRECTION : Charger directement depuis le fichier JSON pour éviter la circularité
            import json
            config_dir = self._get_config_dir()
            config_path = os.path.join(config_dir, "config.json")
            
            # ✅ CORRECTION : S'assurer que le dossier existe
            os.makedirs(config_dir, exist_ok=True)
            
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                self.debug_enabled = bool(config.get("debug_mode", False))
                self.log_level     = int(config.get("debug_level", 5) or (5 if self.debug_enabled else 3))
                self.log_format    = str(config.get("log_format", "html")).lower()
                MAX_LOG_FILES      = int(config.get("max_log_files", MAX_LOG_FILES))
                MAX_FILE_SIZE_MB   = float(config.get("max_file_size_mb", MAX_FILE_SIZE_MB))
                HTML_FLUSH_MS      = int(config.get("html_log_flush_ms", HTML_FLUSH_MS))
                HTML_MAX_SIZE_MB   = float(config.get("html_log_max_size_mb", HTML_MAX_SIZE_MB))
                HTML_THEME         = str(config.get("html_log_theme", HTML_THEME)).lower()
                HTML_AUTO_REFRESH  = bool(config.get("html_auto_refresh", HTML_AUTO_REFRESH))
                HTML_AUTO_REFRESH_SECONDS = int(config.get("html_auto_refresh_seconds", HTML_AUTO_REFRESH_SECONDS))
                if HTML_THEME not in ("dark","light"): HTML_THEME = "dark"
                if self.log_format not in ("txt", "html"): self.log_format = "html"
        except Exception:
            pass

    def _should_log_message(self, level, category=None):
        prio = LOG_LEVELS.get((level or "").upper(), 3)
        if prio <= 2:  # ATTENTION/ERREUR toujours logués
            return True
        return prio <= self.log_level

    def _ensure_log_directory(self):
        try: Path(self.log_dir).mkdir(parents=True, exist_ok=True)
        except Exception: self.log_dir = "."

    def _get_timestamp(self): return datetime.datetime.now().strftime("%Y-%m-%d__%H-%M-%S")

    def _get_existing_html_logs(self):
        try:
            return sorted(glob.glob(os.path.join(self.log_dir, f"{self.log_prefix}_*.html")), key=os.path.getmtime, reverse=True)
        except Exception:
            return []
    
    def _extract_categories_from_log_file(self, html_path):
        """
        Extrait dynamiquement toutes les catégories présentes dans le fichier de logs HTML
        
        Args:
            html_path: Chemin vers le fichier HTML de logs
            
        Returns:
            list: Liste triée des catégories uniques trouvées
        """
        categories = set()
        
        try:
            # Si le fichier existe déjà, le scanner
            if os.path.exists(html_path):
                import re
                
                with open(html_path, 'r', encoding=LOG_ENCODING) as f:
                    content = f.read()
                    
                    # Pattern pour extraire les catégories : data-category="nom_categorie"
                    pattern = r'data-category="([^"]+)"'
                    matches = re.findall(pattern, content)
                    
                    categories.update(matches)
            
            # Toujours inclure au minimum la catégorie "session" pour le premier log
            if not categories:
                categories.add("session")
                categories.add("utils_logging")
                categories.add("main")
        
        except Exception as e:
            # En cas d'erreur, retourner quelques catégories de base
            categories = {"session", "utils_logging", "main", "general"}
        
        # Retourner la liste triée
        return sorted(list(categories))

    def _write_html_header(self, html_path):
        try:
            # Extraction dynamique des catégories depuis le fichier de logs existant
            categories_from_file = self._extract_categories_from_log_file(html_path)
            
            import json
            known_categories_json = json.dumps(categories_from_file, ensure_ascii=False)

            with open(html_path, "w", encoding=LOG_ENCODING) as hf:
                title = f"RenExtract Log {datetime.datetime.now():%Y-%m-%d %H:%M:%S}"
                hf.write(f"<!doctype html><html><head><meta charset='utf-8'><title>{_html.escape(title)}</title>{_css_common()}</head>")
                body_class = " class=\"light\"" if HTML_THEME == "light" else ""
                hf.write(f"<body{body_class}>")
                # ⬇️ Injection config auto-refresh pour le JS
                hf.write(f"<script>window.__RENEX_AUTO_REFRESH__={{\"enabled\":{str(HTML_AUTO_REFRESH).lower()},\"seconds\":{int(HTML_AUTO_REFRESH_SECONDS)}}};</script>")
                # ⬇️ on passe: thème, état debug et TOUTES les catégories connues
                hf.write(_header_html(HTML_THEME, self.debug_enabled, known_categories_json=known_categories_json))
                hf.write('<div class="logs">')
        except Exception:
            pass

    def _append_html_session_block(self, html_path, new_session=False):
        try:
            with open(html_path, "a", encoding=LOG_ENCODING) as hf:
                if new_session:
                    v = self._resolved_version()
                    info_color = _HTML_LEVEL_COLORS.get("INFO", "#198754")
                    hf.write(
                        f'<div class="log" data-level="INFO" data-levelprio="3" data-category="session" '
                        f'style="opacity:.8;border-left:4px solid {info_color}">'
                        f'<span class="ts">{datetime.datetime.now():%Y-%m-%d %H:%M:%S}</span> '
                        f'<span class="lvl lvl-INFO" style="color:{info_color}">[INFO]</span> '
                        f'<span class="cat">[session]</span> '
                        f'<span class="msg">Nouvelle session — Version: {_html.escape(v)}</span>'
                        f'</div>\n'
                    )
        except Exception:
            pass

    def _format_html_row(self, ts, level, category, src, message, custom_color, exception):
        safe_msg = _html.escape(str(message))
        lvl = (level or "INFO").upper()
        color = custom_color or _HTML_LEVEL_COLORS.get(lvl, "#eaeaea")
        src_part = f'<span class="src">{_html.escape(src)}</span> ' if src else ""
        exc_part = ""
        try:
            if exception: exc_part = f"<br><code>{_html.escape(str(exception))}</code>"
        except Exception: pass
        prio = LOG_LEVELS.get(lvl, 3)
        return (f'<div class="log" data-level="{_html.escape(lvl)}" data-levelprio="{prio}" data-category="{_html.escape(category)}" '
                f'style="border-left:4px solid {color}">'
                f'<span class="ts">{_html.escape(ts)}</span> '
                f'<span class="lvl lvl-{_html.escape(lvl)}" style="color:{color}">[{_html.escape(lvl)}]</span> '
                f'<span class="cat">[{_html.escape(category)}]</span> '
                f'{src_part}<span class="msg">{safe_msg}</span>{exc_part}</div>\n')

    def _create_new_html(self):
        filename = f"{self.log_prefix}_{self._get_timestamp()}.html"
        html_path = os.path.join(self.log_dir, filename)
        try:
            self._write_html_header(html_path)
            self._append_html_session_block(html_path, new_session=True)
            return html_path
        except Exception:
            return None

    def _cleanup_old_html(self):
        try:
            existing = self._get_existing_html_logs()
            if len(existing) > MAX_LOG_FILES:
                for old_html in existing[MAX_LOG_FILES:]:
                    try: os.remove(old_html)
                    except Exception: pass
        except Exception: pass

    def _should_rotate(self):
        try:
            # ✅ Vérifier le bon fichier selon le format
            current_file = self.current_txt_file if self.log_format == "txt" else self.current_html_file
            if not current_file or not os.path.exists(current_file): return True
            return (os.path.getsize(current_file)/(1024*1024)) >= MAX_FILE_SIZE_MB
        except Exception:
            return True

    def _rotate_if_needed(self):
        if self._should_rotate():
            # ✅ FORMAT TXT : Créer nouveau .txt
            if self.log_format == "txt":
                txt_path = self._create_new_txt()
                if txt_path:
                    self.current_txt_file = txt_path
                    self._cleanup_old_txt()
            # ✅ FORMAT HTML : Créer nouveau .html
            else:
                html_path = self._create_new_html()
                if html_path:
                    self.current_html_file = html_path
                    self._cleanup_old_html()

    def _start_html_flusher(self):
        if self._html_thread or not self.current_html_file: return
        self._html_running = True
        def _worker():
            interval = max(50, int(HTML_FLUSH_MS)) / 1000.0
            while self._html_running:
                try:
                    try:
                        if self.current_html_file and os.path.exists(self.current_html_file):
                            if (os.path.getsize(self.current_html_file)/(1024*1024)) >= HTML_MAX_SIZE_MB:
                                self._html_disabled_runtime = True
                                try:
                                    while True: self._html_q.get_nowait()
                                except Empty: pass
                                time.sleep(interval); continue
                    except Exception: pass

                    buf = []
                    try:
                        line = self._html_q.get(timeout=interval); buf.append(line)
                        while True: buf.append(self._html_q.get_nowait())
                    except Empty: pass

                    if buf and not self._html_disabled_runtime:
                        with open(self.current_html_file, "a", encoding=LOG_ENCODING) as hf:
                            hf.writelines(buf)
                except Exception:
                    time.sleep(interval)
        self._html_thread = threading.Thread(target=_worker, name="HtmlLogFlusher", daemon=True)
        self._html_thread.start()
        atexit.register(self._stop_html_flusher)

    def _stop_html_flusher(self):
        self._html_running = False
        try:
            remaining = []
            while True: remaining.append(self._html_q.get_nowait())
        except Empty: pass
        try:
            if remaining and self.current_html_file and not self._html_disabled_runtime:
                with open(self.current_html_file, "a", encoding=LOG_ENCODING) as hf:
                    hf.writelines(remaining)
        except Exception: pass

    def _initialize_logging(self):
        try:
            # ✅ FORMAT TXT : Initialiser .txt
            if self.log_format == "txt":
                self.current_txt_file = self._create_new_txt()
                self._cleanup_old_txt()
                self.log_message("INFO", "Format de log : TXT", category="utils_logging")
            # ✅ FORMAT HTML : Initialiser .html
            else:
                existing = self._get_existing_html_logs()
                if existing and not self._should_rotate():
                    self.current_html_file = existing[0]
                    self._append_html_session_block(self.current_html_file, new_session=True)
                else:
                    self.current_html_file = self._create_new_html()
                    self._cleanup_old_html()
                self._start_html_flusher()
                self.log_message("INFO", "Format de log : HTML", category="utils_logging")
        except Exception: pass

    def _format_txt_row(self, ts, level, category, src, message, exception):
        """Formate une ligne de log pour fichier .txt"""
        lvl = (level or "INFO").upper()
        src_part = f" [{src}]" if src else ""
        exc_part = f"\n  Exception: {exception}" if exception else ""
        return f"{ts} [{lvl}] [{category}]{src_part} {message}{exc_part}\n"

    def _create_new_txt(self):
        """Crée un nouveau fichier de log .txt"""
        filename = f"{self.log_prefix}_{self._get_timestamp()}.txt"
        txt_path = os.path.join(self.log_dir, filename)
        try:
            with open(txt_path, "w", encoding=LOG_ENCODING) as tf:
                v = self._resolved_version()
                tf.write("=" * 80 + "\n")
                tf.write(f"RENEXTRACT LOG - Version {v}\n")
                tf.write(f"Session démarrée: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}\n")
                tf.write("=" * 80 + "\n\n")
            return txt_path
        except Exception:
            return None

    def _cleanup_old_txt(self):
        """Nettoie les anciens fichiers .txt"""
        try:
            existing_txt = sorted(glob.glob(os.path.join(self.log_dir, f"{self.log_prefix}_*.txt")), 
                                 key=os.path.getmtime, reverse=True)
            if len(existing_txt) > MAX_LOG_FILES:
                for old_txt in existing_txt[MAX_LOG_FILES:]:
                    try: os.remove(old_txt)
                    except Exception: pass
        except Exception: pass

# ====== INSTANCE GLOBALE + API PUBLIQUE ======
_logger_instance = None
_logger_lock = threading.Lock()

def get_logger(app_version="inconnue"):
    global _logger_instance
    if _logger_instance is None:
        with _logger_lock:
            if _logger_instance is None:
                _logger_instance = HtmlOnlyLogger(app_version=app_version)
    else:
        if app_version and app_version != "inconnue":
            _logger_instance.set_app_version(app_version)
    return _logger_instance

def initialize_log(app_version="inconnue"): get_logger(app_version=app_version)
def log_message(level, message, *args, **kwargs): get_logger().log_message(level, message, *args, **kwargs)

def log_performance(operation, file_name, duration, details=None):
    try:
        msg = f"[PERFORMANCE] {operation} - {file_name} - {duration:.2f}s"
        if details: msg += " | " + " | ".join([f"{k}: {v}" for k, v in details.items()])
        log_message("INFO", msg, category="performance")
    except Exception as e:
        log_message("ATTENTION", "Impossible de logger la performance: {e}", e=e, category="performance")
