# Module de surveillance RenExtract pour édition temps réel - VERSION 2
# Langue cible: {language}
# Compatibilité: Ren'Py 7.3.5 et versions antérieures (testés et validés)
# Note: Compatible avec Ren'Py 7.3.5.606 (NoMoreMoney) et versions antérieures
# Pour les versions Ren'Py 8+, utilisez le module v1 correspondant

init python:
    import threading
    import os as _renextract_os  # Alias protégé pour éviter les conflits avec les personnages nommés 'os'

    _FOCUS_URL = "http://127.0.0.1:8765/focus"  # port fixe

    # Compat Ren'Py 7 (py2) sans dépendances externes
    try:
        import urllib2 as _urlreq      # Ren'Py 7 / Python 2
    except Exception:
        _urlreq = None

    def _hit_focus_endpoint():
        if _urlreq is None:
            return
        try:
            req = _urlreq.Request(_FOCUS_URL)
            _urlreq.urlopen(req, timeout=0.5).read()
        except Exception:
            # silence côté joueur
            pass

    def focus_editor_now():
        t = threading.Thread(target=_hit_focus_endpoint)
        t.daemon = True
        t.start()

    def focus_editor_safe():
        """
        Si plein écran -> bascule fenêtré via screen (préférence + force), puis focus.
        Sinon -> focus direct.
        """
        try:
            rp = __import__('renpy')  # import paresseux
        except Exception:
            focus_editor_now(); return

        # Détecte l'état plein écran
        try:
            is_full = rp.get_fullscreen()
        except Exception:
            try:
                is_full = getattr(rp.store.preferences, "fullscreen", False)
            except Exception:
                is_full = False

        if is_full:
            try:
                rp.show_screen("renextract_display_window_then_focus")
            except Exception:
                # fallback ultime
                _renextract_force_window_mode()
                focus_editor_now()
        else:
            focus_editor_now()

    def _renextract_force_window_mode():
        """
        Force le mode fenêtré même si la persistance/le code du jeu tente de rester en plein écran.
        """
        try:
            rp = __import__('renpy')
        except Exception:
            return
        # 1) forcer la fenêtre
        try:
            rp.set_fullscreen(False)
        except Exception:
            pass
        # 2) aligner les préférences (runtime)
        try:
            rp.store.preferences.fullscreen = False
        except Exception:
            pass
        # 3) aligner la persistance si le jeu la lit (certains menus le font)
        try:
            # suivant les projets, _preferences peut ne pas exister : on ignore si c'est le cas
            if hasattr(rp.store, "_preferences") and isinstance(rp.store._preferences, dict):
                rp.store._preferences["fullscreen"] = False
        except Exception:
            pass
        # 4) enregistrer la persistance (au cas où le jeu relit tout de suite)
        try:
            rp.save_persistent()
        except Exception:
            pass
        # 5) relancer l'interaction pour que l'UI prenne l'état (optionnel mais utile)
        try:
            rp.restart_interaction()
        except Exception:
            pass

init -900:
    # Passe en fenêtré (préférence) + force, puis focus ~50 ms après
    screen renextract_display_window_then_focus():
        timer 0.0 action [
            Preference("display", "window"),          # même action que ton menu
            Function(_renextract_force_window_mode),  # force contre la persistance
            Hide("renextract_display_window_then_focus"),
            Show("renextract_focus_timer")
        ]

    # Timer qui déclenche /focus puis se cache
    screen renextract_focus_timer():
        timer 0.05 action [ Function(focus_editor_now), Hide("renextract_focus_timer") ]

# Screen overlay : hotkey + timer
init -900:
    screen renextract_hotkeys():
        key "K_F8" action Function(focus_editor_safe)

init -900 python:
    if "renextract_hotkeys" not in config.overlay_screens:
        config.overlay_screens.append("renextract_hotkeys")


init -999 python:
    import renpy.exports as renpy_exports
    import os as _renextract_os  # Alias protégé pour éviter les conflits avec les personnages nommés 'os'
    import codecs
    import re
    import traceback

    print(u"Démarrage du module surveillance RenExtract v2 (compatible Ren'Py 7)")

    RENEXTRACT_TARGET_LANG = "{language}"
    RENEXTRACT_LOG_FILE = "renextract_dialogue_log.txt"

    # Réinitialisation du fichier de log au démarrage pour une détection propre
    # Cela évite de traiter d'anciens dialogues et garantit un démarrage à zéro
    try:
        if _renextract_os.path.exists(RENEXTRACT_LOG_FILE):
            with codecs.open(RENEXTRACT_LOG_FILE, "w", encoding="utf-8") as f: f.write(u"")
    except Exception as e:
        print(u"Erreur réinitialisation log : {{0}}".format(e))

    def get_translated_dialogue(file_path, line_number, original_text=None):
        try:
            tl_file_path = _renextract_os.path.join("game", "tl", RENEXTRACT_TARGET_LANG, file_path)
            if not _renextract_os.path.exists(tl_file_path):
                tl_file_path = _renextract_os.path.join("game", file_path)
                if not _renextract_os.path.exists(tl_file_path): return original_text or None, tl_file_path, line_number
            with open(tl_file_path, "rb") as f:
                content = f.read()
            if content.startswith(b'\xef\xbb\xbf'): content = content[3:]
            lines = content.decode("utf-8").splitlines()
            for i, line in enumerate(lines):
                line = line.strip()
                if i + 1 == line_number or i + 2 == line_number:
                    if "old" in line.lower():
                        match_old = re.search(r'old\s+"((?:\\.|[^"])*)"', line)
                        if match_old:
                            old_text = match_old.group(1).strip()
                            if original_text and old_text != original_text: continue
                            next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                            match_new = re.search(r'new\s+"((?:\\.|[^"])*)"', next_line)
                            if match_new: return match_new.group(1), tl_file_path, i + 2
                            else: return old_text, tl_file_path, i + 1
                    match = re.search(r'"((?:\\.|[^"])*)"', line)
                    if match and i + 1 == line_number:
                        return match.group(1), tl_file_path, line_number
            return original_text or None, tl_file_path, line_number
        except Exception as e:
            return original_text or None, None, line_number

    # Hook pour les menus - VERSION COMPATIBLE REN'PY 7
    # Utilisation d'un dictionnaire pour éviter les problèmes d'attribution __name__
    _patched_functions = {}
    
    if "menu" not in _patched_functions:
        def make_patched_menu(original):
            def patched_menu(items, *args, **kwargs):
                try:
                    menu_choices = []
                    for item in items:
                        caption = item[0] if isinstance(item, (tuple, list)) and len(item) >= 1 else None
                        if caption and caption != "":
                            # On ne cherche plus la traduction ici, on envoie juste l'original.
                            menu_choices.append(caption)
                    if menu_choices:
                        with codecs.open(RENEXTRACT_LOG_FILE, "a", encoding="utf-8") as f:
                            f.write(u"MENU_START\n")
                            for choice in menu_choices:
                                # Nouveau format de log : juste CHOICE|texte_original
                                f.write(u"CHOICE|{{0}}\n".format(choice))
                            f.write(u"MENU_END\n")
                except Exception as e:
                    print(u"Erreur dans patched_menu : {{0}}".format(e))
                return original(items, *args, **kwargs)
            return patched_menu
        
        _patched_functions["menu"] = True
        renpy.exports.menu = make_patched_menu(renpy.exports.menu)

    # Hook de la fonction say - VERSION COMPATIBLE REN'PY 7
    if "say" not in _patched_functions:
        def make_patched_say(original):
            def patched_say(who, what, *args, **kwargs):
                try:
                    if what and what.strip() and renpy.game.contexts:
                        current_file, line_number = renpy_exports.get_filename_line()
                        current_file = _renextract_os.path.normpath(current_file)
                        if current_file.startswith(_renextract_os.path.normpath("game/")):
                            current_file = current_file[len(_renextract_os.path.normpath("game/")) + 1:]
                        translated_dialogue, tl_file, tl_line = get_translated_dialogue(current_file, line_number, what)
                        display_text = translated_dialogue if translated_dialogue is not None else what
                        with codecs.open(RENEXTRACT_LOG_FILE, "a", encoding="utf-8") as f:
                            f.write(u"{{0}}|{{1}}|{{2}}|{{3}}|{{4}}\n".format(display_text, current_file, line_number, tl_file, tl_line))
                    return original(who, what, *args, **kwargs)
                except Exception as e:
                    print(u"Erreur dans patched_say : {{0}}".format(e))
                    raise
            return patched_say
        
        _patched_functions["say"] = True
        renpy_exports.say = make_patched_say(renpy_exports.say)
