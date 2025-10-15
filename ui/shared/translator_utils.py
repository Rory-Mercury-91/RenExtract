"""
Utilitaires pour les traducteurs en ligne
Gère Google Translate, Yandex Translate, DeepL et Microsoft Translator
"""

import webbrowser
import urllib.parse
from infrastructure.logging.logging import log_message


def get_translator_url(translator, text, source_lang="auto", target_lang="fr"):
    """
    Génère l'URL pour le traducteur spécifié
    
    Args:
        translator: Nom du traducteur ("Google", "Yandex", "DeepL", "Microsoft")
        text: Texte à traduire
        source_lang: Langue source (par défaut "auto")
        target_lang: Langue cible (par défaut "fr")
    
    Returns:
        str: URL complète du traducteur avec le texte pré-rempli
    """
    try:
        # Nettoyer le texte
        clean_text = (text or "").strip()
        if not clean_text:
            return None
        
        # Encoder le texte selon le traducteur
        if translator == "Google":
            # Limiter pour Google (URLs très longues peuvent poser problème)
            max_length = 500
            if len(clean_text) > max_length:
                clean_text = clean_text[:max_length] + "..."
            encoded_text = urllib.parse.quote(clean_text, safe='')
            return f"https://translate.google.com/?sl={source_lang}&tl={target_lang}&text={encoded_text}&op=translate"
            
        elif translator == "Yandex":
            # Limiter pour Yandex
            max_length = 500
            if len(clean_text) > max_length:
                clean_text = clean_text[:max_length] + "..."
            encoded_text = urllib.parse.quote(clean_text, safe='')
            return f"https://translate.yandex.com/?lang={source_lang}-{target_lang}&text={encoded_text}"
            
        elif translator == "DeepL":
            # DeepL utilise le format #source/target/texte
            # Limiter à 500 caractères pour éviter les URLs trop longues
            max_length = 500
            if len(clean_text) > max_length:
                clean_text = clean_text[:max_length] + "..."
            # Encoder en préservant les antislashs (comme la version qui marchait)
            encoded_text = urllib.parse.quote(clean_text, safe='\\')
            # DeepL préfère 'en' à 'auto' pour la détection automatique
            deepl_source = 'en' if source_lang == 'auto' else source_lang
            return f"https://www.deepl.com/translator#{deepl_source}/{target_lang}/{encoded_text}"
            
        elif translator == "Microsoft":
            # Limiter pour Microsoft
            max_length = 500
            if len(clean_text) > max_length:
                clean_text = clean_text[:max_length] + "..."
            encoded_text = urllib.parse.quote(clean_text, safe='')
            return f"https://www.bing.com/translator?from={source_lang}&to={target_lang}&text={encoded_text}"
            
        elif translator == "Groq AI":
            # Groq AI - Utiliser l'API si clé disponible, sinon playground
            from infrastructure.config.config import config_manager
            api_key = config_manager.get('groq_api_key', '')
            if api_key and api_key.strip():
                # API disponible - retourner None pour déclencher l'API directe
                return None
            else:
                # Pas d'API - utiliser le playground
                encoded_text = urllib.parse.quote(clean_text, safe='')
                return f"https://console.groq.com/playground"
            
        else:
            log_message("ERREUR", f"Traducteur non supporté: {translator}", category="translator_utils")
            return None
            
    except Exception as e:
        log_message("ERREUR", f"Erreur génération URL {translator}: {e}", category="translator_utils")
        return None


def translate_with_groq_api(text, source_lang="auto", target_lang="fr", tone="informel", 
                           speaker=None, previous_dialogue=None, characters_def=None):
    """
    Traduit directement via l'API Groq avec pré-remplissage et contexte enrichi
    Nécessite une clé API (gratuite, 6000 req/jour)
    
    Args:
        text: Texte à traduire
        source_lang: Langue source (auto pour détection auto)
        target_lang: Langue cible (fr, en, es, etc.)
        tone: Ton de traduction ('informel' ou 'formel')
        speaker: Locuteur du dialogue actuel (ex: 'p', 'a')
        previous_dialogue: Dict avec 'speaker' et 'text' du dialogue précédent
        characters_def: Dict des définitions de personnages {locuteur: {'genre': ..., 'prenom': ...}}
    """
    try:
        from groq import Groq
        from infrastructure.config.config import config_manager
        
        # Récupérer la clé API depuis la config
        api_key = config_manager.get('groq_api_key', '')
        
        if not api_key or not api_key.strip():
            log_message("ATTENTION", "Pas de clé API Groq configurée", category="translator_utils")
            return None
        
        # Initialiser le client Groq
        client = Groq(api_key=api_key)
        
        # Créer le prompt spécialisé pour traduction
        lang_names = {
            "fr": "français", "en": "anglais", "es": "espagnol", "de": "allemand",
            "it": "italien", "pt": "portugais", "ru": "russe", "ja": "japonais", "zh": "chinois"
        }
        
        source_name = lang_names.get(source_lang, source_lang)
        target_name = lang_names.get(target_lang, target_lang)
        
        # Récupérer les configurations avancées
        style = config_manager.get('groq_translation_style', 'Naturel')
        game_context = config_manager.get('groq_game_context', 'Général')
        temperature = float(config_manager.get('groq_temperature', 0.3))
        custom_instr = config_manager.get('groq_custom_instructions', '').strip()
        
        # Instructions de ton selon la sélection
        tone_instruction = ""
        if tone == "formel":
            tone_instruction = "\n4. Utilise un ton FORMEL (vouvoiement, registre soutenu)"
        elif tone == "neutre":
            tone_instruction = "\n4. Utilise un ton NEUTRE (ni tutoiement ni vouvoiement)"
        else:  # informel par défaut
            tone_instruction = "\n4. Utilise un ton INFORMEL (tutoiement, registre courant)"
        
        # Instructions de style
        style_instruction = ""
        if style == "Littéral":
            style_instruction = "\n5. Traduis de manière LITTÉRALE en respectant au maximum la structure originale"
        elif style == "Créatif":
            style_instruction = "\n5. Traduis de manière CRÉATIVE en adaptant idiomes et expressions culturelles"
        else:  # Naturel par défaut
            style_instruction = "\n5. Traduis de manière NATURELLE en équilibrant fidélité et fluidité"
        
        # Instructions de contexte
        context_instruction = ""
        if game_context != "Général":
            context_instruction = f"\n6. Contexte du jeu : {game_context.upper()} - adapte le vocabulaire en conséquence"
        
        # Instructions personnalisées
        custom_instruction = ""
        if custom_instr:
            custom_instruction = f"\n7. Instructions supplémentaires : {custom_instr}"
        
        # ✅ NOUVEAU : Contexte des personnages
        characters_context = ""
        if characters_def and isinstance(characters_def, dict) and len(characters_def) > 0:
            chars_lines = []
            for char_key, char_info in characters_def.items():
                if isinstance(char_info, dict):
                    genre = char_info.get('genre', 'Neutre')
                    prenom = char_info.get('prenom', '')
                    if prenom:
                        chars_lines.append(f"[{char_key}] est un(e) {genre} du nom de {prenom}")
                    else:
                        chars_lines.append(f"[{char_key}] est un(e) {genre}")
            
            if chars_lines:
                characters_context = "\n\nCONTEXTE DES PERSONNAGES :\n" + "\n".join(chars_lines)
                characters_context += "\nNote : Ces lettres entre crochets peuvent aussi apparaître comme variables dans le texte. Ne les supprime jamais."
        
        # ✅ NOUVEAU : Contexte conversationnel (dialogue précédent)
        conversation_context = ""
        if previous_dialogue and isinstance(previous_dialogue, dict):
            prev_speaker = previous_dialogue.get('speaker', '')
            prev_text = previous_dialogue.get('text', '')
            if prev_speaker and prev_text:
                conversation_context = f"\n\nCONTEXTE DE CONVERSATION (dialogue précédent) :\n{prev_speaker} \"{prev_text}\""
        
        # Construction du prompt enrichi
        prompt = f"""Tu es un traducteur professionnel pour jeux vidéo Ren'Py. Traduis ce texte du {source_name} vers le {target_name}.

RÈGLES STRICTES :
1. Préserve TOUTES les balises Ren'Py : {{i}}, {{/i}}, [p], [tooltip], \\", etc.
2. Retourne UNIQUEMENT la traduction finale, SANS notes, SANS explications, SANS commentaires
3. Ne modifie que le texte visible, jamais les balises ou la structure
4. NE RETOURNE JAMAIS LES GUILLEMETS (" ") dans ta réponse - seulement le texte traduit brut{tone_instruction}{style_instruction}{context_instruction}{custom_instruction}{characters_context}{conversation_context}

Texte à traduire :
{speaker + ' ' if speaker else ''}"{text}"

Traduction (UNIQUEMENT le texte traduit, SANS locuteur, SANS guillemets) :"""
        
        # Appeler l'API Groq
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Meilleur modèle pour traduction
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,  # Température configurable
            max_completion_tokens=2048
        )
        
        result = completion.choices[0].message.content.strip()
        
        # ✅ NETTOYAGE : Supprimer les notes explicatives si présentes
        # Exemples de patterns à supprimer :
        # - "Note : ..."
        # - "Note: ..."
        # - Tout ce qui suit "Note" sur une nouvelle ligne
        import re
        
        # Supprimer les lignes commençant par "Note" (avec ou sans deux-points)
        result = re.sub(r'\n\s*Note\s*[:：].*', '', result, flags=re.IGNORECASE | re.DOTALL)
        
        # ✅ NETTOYAGE : Supprimer les guillemets au début et à la fin
        # Enlever les guillemets doubles ou simples qui encadrent toute la traduction
        if result.startswith('"') and result.endswith('"'):
            result = result[1:-1]
        elif result.startswith("'") and result.endswith("'"):
            result = result[1:-1]
        
        # Supprimer les lignes vides multiples
        result = re.sub(r'\n\n+', '\n\n', result).strip()
        
        log_message("INFO", f"Traduction Groq réussie : {len(result)} caractères", category="translator_utils")
        return result
        
    except ImportError:
        log_message("ERREUR", "Module groq non installé. Installez avec : pip install groq", category="translator_utils")
        return None
    except Exception as e:
        log_message("ERREUR", f"Erreur API Groq : {e}", category="translator_utils")
        return None

def open_translator(translator, text, context="", main_interface=None, target_lang="fr", tone="informel",
                   speaker=None, previous_dialogue=None, characters_def=None):
    """
    Ouvre le traducteur spécifié avec le texte pré-rempli
    
    Args:
        translator: Nom du traducteur ("Google", "Yandex", "DeepL", "Microsoft", "Groq AI")
        text: Texte à traduire
        context: Contexte pour les logs (optionnel)
        main_interface: Interface principale pour notifications (optionnel)
        target_lang: Langue cible (par défaut "fr")
        tone: Ton de traduction ('informel' ou 'formel') - uniquement pour Groq AI
        speaker: Locuteur du dialogue actuel (ex: 'p', 'a') - uniquement pour Groq AI
        previous_dialogue: Dict avec 'speaker' et 'text' du dialogue précédent - uniquement pour Groq AI
        characters_def: Dict des définitions de personnages - uniquement pour Groq AI
    
    Returns:
        bool: True si succès, False sinon
    """
    try:
        # Nettoyer le texte
        clean_text = (text or "").strip()
        if not clean_text:
            log_message("ATTENTION", "Aucun texte à traduire", category="translator_utils")
            return False
        
        # Copier le texte dans le presse-papier comme backup
        if main_interface:
            main_interface.window.clipboard_clear()
            main_interface.window.clipboard_append(clean_text)
        
        # Générer l'URL du traducteur
        url = get_translator_url(translator, clean_text, source_lang="auto", target_lang=target_lang)
        
        # Gestion spéciale pour Groq AI avec API (vérifier AVANT la vérification générale)
        if translator == "Groq AI" and url is None:
            # Utiliser l'API Groq directement avec contexte enrichi
            translation_result = translate_with_groq_api(
                clean_text, 
                target_lang=target_lang, 
                tone=tone,
                speaker=speaker,
                previous_dialogue=previous_dialogue,
                characters_def=characters_def
            )
            
            if translation_result and main_interface:
                # Pré-remplir la zone de traduction
                from ui.tab_tools.realtime_editor_tab import fill_translation_area, _find_vf_widgets_recursively
                
                # ✅ CORRECTION : Chercher directement dans main_interface (qui est maintenance_tools_interface)
                target_interface = main_interface
                
                # Vérifier si main_interface a des zones VF (noms corrects de l'éditeur temps réel)
                has_vf_zones = (
                    hasattr(main_interface, 'vf_text_widget') or 
                    hasattr(main_interface, 'vf_text_widget_2') or 
                    hasattr(main_interface, 'vf_text') or 
                    hasattr(main_interface, 'txt2') or 
                    hasattr(main_interface, 'vf_dialogue_widget') or
                    hasattr(main_interface, 'vf_multiple_widget') or
                    hasattr(main_interface, 'vf_choice_widget')
                )
                
                if has_vf_zones:
                    log_message("DEBUG", f"Zones VF trouvées directement dans main_interface", category="translator_utils")
                else:
                    # Si pas de zones VF dans main_interface, essayer de trouver l'interface principale
                    if hasattr(main_interface, '_get_main_window'):
                        try:
                            main_window = main_interface._get_main_window()
                            if main_window:
                                target_interface = main_window
                                log_message("DEBUG", "Interface principale trouvée via _get_main_window", category="translator_utils")
                        except:
                            pass
                    
                    # ✅ AJOUT : Essayer via parent_window (pour MaintenanceToolsInterface)
                    if target_interface == main_interface and hasattr(main_interface, 'parent_window'):
                        try:
                            target_interface = main_interface.parent_window
                            log_message("DEBUG", "Interface principale trouvée via parent_window", category="translator_utils")
                            
                            # ✅ AJOUT : Si c'est MainWindow, essayer de trouver les composants avec zones VF
                            if hasattr(target_interface, 'components') and hasattr(target_interface, 'root'):
                                # Chercher dans les composants pour trouver celui qui a des zones VF
                                for component_name, component in target_interface.components.items():
                                    # Vérifier si le composant a des zones VF (plus flexible)
                                    has_vf_zones = (
                                        hasattr(component, 'vf_text') or 
                                        hasattr(component, 'txt2') or 
                                        hasattr(component, 'vf_dialogue_widget') or
                                        hasattr(component, 'vf_multiple_widget') or
                                        hasattr(component, 'vf_choice_widget')
                                    )
                                    
                                    if has_vf_zones:
                                        target_interface = component
                                        log_message("DEBUG", f"Composant avec zones VF trouvé: {component_name}", category="translator_utils")
                                        break
                                    else:
                                        # ✅ AJOUT : Essayer de chercher récursivement dans le composant
                                        try:
                                            if hasattr(component, 'winfo_children'):
                                                # C'est un widget Tkinter, on peut chercher dedans
                                                test_widgets = _find_vf_widgets_recursively(component, depth=0)
                                                if test_widgets:
                                                    target_interface = component
                                                    log_message("DEBUG", f"Composant avec zones VF trouvé via recherche récursive: {component_name}", category="translator_utils")
                                                    break
                                        except:
                                            continue
                        except:
                            pass
                
                # Essayer via l'import global
                if target_interface == main_interface:
                    try:
                        from main import app_instance
                        if app_instance and hasattr(app_instance, 'main_window'):
                            target_interface = app_instance.main_window
                            log_message("DEBUG", "Interface principale trouvée via app_instance", category="translator_utils")
                    except:
                        pass
                
                fill_translation_area(target_interface, translation_result, context)
                if main_interface and hasattr(main_interface, '_update_status'):
                    status_msg = f"Groq AI traduit{' (' + context + ')' if context else ''}"
                    main_interface._update_status(status_msg)
                log_message("INFO", f"Traduction Groq réussie{' (' + context + ')' if context else ''}: {len(translation_result)} caractères", category="translator_utils")
                return True
            elif main_interface:
                # Erreur de traduction, ouvrir le playground comme fallback
                webbrowser.open("https://console.groq.com/playground")
                if hasattr(main_interface, '_update_status'):
                    status_msg = f"Groq AI playground ouvert{' (' + context + ')' if context else ''}"
                    main_interface._update_status(status_msg)
                log_message("ATTENTION", "Erreur API Groq, ouverture du playground comme fallback", category="translator_utils")
                return True
            else:
                return False
        
        # Vérification générale pour les autres traducteurs
        elif not url:
            log_message("ERREUR", f"Erreur génération URL {translator}", category="translator_utils")
            return False
        elif url:
            # Ouvrir le traducteur web normal
            webbrowser.open(url)
            
            # Messages de statut (pas de notification popup pour ne pas être intrusif)
            if main_interface and hasattr(main_interface, '_update_status'):
                status_msg = f"{translator} ouvert{' avec ' + context if context else ''}"
                main_interface._update_status(status_msg)
        
        log_message("INFO", f"Texte envoyé à {translator}{' (' + context + ')' if context else ''}: {len(clean_text)} caractères", category="translator_utils")
        return True
        
    except Exception as e:
        log_message("ERREUR", f"Erreur {translator}{' (' + context + ')' if context else ''}: {e}", category="translator_utils")
        return False


def get_default_translator():
    """
    Retourne le traducteur par défaut
    
    Returns:
        str: Nom du traducteur par défaut
    """
    from infrastructure.config.config import config_manager
    return config_manager.get('default_online_translator', 'Google')


def set_default_translator(translator):
    """
    Définit le traducteur par défaut
    
    Args:
        translator: Nom du traducteur à définir par défaut
    """
    from infrastructure.config.config import config_manager
    config_manager.set('default_online_translator', translator)
    log_message("INFO", f"Traducteur par défaut changé vers: {translator}", category="translator_utils")
