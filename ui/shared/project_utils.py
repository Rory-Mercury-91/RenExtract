# ui/shared/project_utils.py
# Fonctions partagées pour la gestion des projets Ren'Py
# Utilisées par l'interface de cohérence et d'extraction
# VERSION AVEC CACHE INTELLIGENT ET INVALIDATION GRANULAIRE

import os
import glob
from typing import List, Dict, Optional, Tuple
from infrastructure.logging.logging import log_message
from core.models.cache.project_scan_cache import get_project_cache

def validate_renpy_project(project_path: str) -> bool:
    """
    Valide qu'un chemin est un projet Ren'Py valide
    
    Args:
        project_path: Chemin vers le projet à valider
        
    Returns:
        bool: True si le projet est valide
    """
    try:
        if not os.path.isdir(project_path):
            return False
        
        # Vérifier la présence d'au moins un indicateur Ren'Py
        game_dir = os.path.join(project_path, "game")
        has_game_folder = os.path.isdir(game_dir)
        
        # Chercher des fichiers Ren'Py caractéristiques
        has_exe = any(f.endswith('.exe') for f in os.listdir(project_path) 
                     if os.path.isfile(os.path.join(project_path, f)))
        
        # Chercher des fichiers .rpy ou .rpyc
        has_rpy_files = False
        if has_game_folder:
            for root, dirs, files in os.walk(game_dir):
                if any(f.endswith(('.rpy', '.rpyc', '.rpa')) for f in files):
                    has_rpy_files = True
                    break
                # Limiter la recherche à 2 niveaux
                if root.count(os.sep) - game_dir.count(os.sep) >= 2:
                    break
        
        return has_game_folder or has_exe or has_rpy_files
        
    except Exception as e:
        log_message("ATTENTION", f"Erreur validation projet: {e}", category="project_utils")
        return False

def scan_project_languages(project_path: str, force_refresh: bool = False) -> List[Dict[str, any]]:
    """
    Scanne les langues disponibles dans un projet Ren'Py avec cache intelligent
    VERSION AVEC CACHE : Récupère depuis le cache si disponible
    
    Args:
        project_path: Chemin vers le projet
        force_refresh: Si True, ignore le cache et rescanne
        
    Returns:
        Liste des langues avec leurs infos: [{'name': 'french', 'file_count': 12}, ...]
    """
    languages = []
    
    try:
        if not project_path or not os.path.exists(project_path):
            return languages
        
        # Essayer de récupérer depuis le cache
        cache = get_project_cache()
        if not force_refresh:
            cached_languages = cache.get_project_languages(project_path)
            if cached_languages is not None:
                # Cache HIT : Ajouter le path pour compatibilité
                for lang in cached_languages:
                    lang['path'] = os.path.join(project_path, "game", "tl", lang['name'])
                return cached_languages
        
        # Cache MISS ou force_refresh : Scanner normalement
        tl_path = os.path.join(project_path, "game", "tl")
        if not os.path.exists(tl_path):
            return languages
        
        for item in os.listdir(tl_path):
            item_path = os.path.join(tl_path, item)
            if os.path.isdir(item_path) and not item.startswith('.') and item.lower() != 'none':
                # CORRECTION: Utiliser os.walk au lieu de glob pour éviter les problèmes avec les crochets
                rpy_files = []
                try:
                    for root, dirs, files in os.walk(item_path):
                        for file in files:
                            if file.lower().endswith('.rpy'):
                                rpy_files.append(os.path.join(root, file))
                except Exception as e:
                    log_message("DEBUG", f"Erreur scan fichiers dans {item_path}: {e}", category="project_utils")
                    continue
                
                if rpy_files:
                    languages.append({
                        'name': item,
                        'file_count': len(rpy_files),
                        'path': item_path
                    })
        
        # Trier avec french en premier
        languages.sort(key=lambda x: (0 if x['name'].lower() == 'french' else 1, x['name'].lower()))
        
        # Mettre en cache le résultat
        cache.cache_project_languages(project_path, languages)
        
        return languages
        
    except Exception as e:
        log_message("ERREUR", f"Erreur scan langues: {e}", category="project_utils")
        return languages

def scan_language_files(project_path: str, language: str, exclusions: List[str] = None,
                       force_refresh: bool = False) -> List[Dict[str, any]]:
    """
    Scanne les fichiers .rpy dans une langue donnée avec cache intelligent et invalidation granulaire
    VERSION AVEC CACHE : Récupère depuis le cache si la langue n'a pas été modifiée
   
    Args:
        project_path: Chemin vers le projet
        language: Nom de la langue (ex: 'french')
        exclusions: Liste des fichiers à exclure
        force_refresh: Si True, ignore le cache et rescanne
       
    Returns:
        Liste des fichiers: [{'name': 'script.rpy', 'path': '/full/path', 'size': 1234}, ...]
    """
    files = []
   
    try:
        if not project_path or not language:
            return files
           
        if exclusions is None:
            exclusions = []
        
        language_path = os.path.join(project_path, "game", "tl", language)
        if not os.path.exists(language_path):
            return files
        
        # Essayer de récupérer depuis le cache (invalidation granulaire par langue)
        cache = get_project_cache()
        if not force_refresh:
            cached_files = cache.get_language_files(project_path, language, exclusions)
            if cached_files is not None:
                # Cache HIT : La langue n'a pas été modifiée
                # Filtrer selon les exclusions actuelles
                filtered_files = []
                for file_data in cached_files:
                    file_name = file_data['name']
                    should_exclude = any(
                        exclusion.strip().lower() in file_name.lower()
                        for exclusion in exclusions if exclusion.strip()
                    )
                    if not should_exclude:
                        filtered_files.append(file_data)
                return filtered_files
       
        # CORRECTION: Utiliser os.walk au lieu de glob pour éviter les problèmes avec les crochets
        rpy_files = []
        try:
            for root, dirs, files_in_dir in os.walk(language_path):
                for file in files_in_dir:
                    if file.lower().endswith('.rpy'):
                        rpy_files.append(os.path.join(root, file))
        except Exception as e:
            log_message("ERREUR", f"Erreur recherche fichiers dans {language_path}: {e}", category="project_utils")
            return files
       
        for file_path in rpy_files:
            file_name = os.path.basename(file_path)
           
            # Vérifier les exclusions
            should_exclude = False
            for exclusion in exclusions:
                exclusion_clean = exclusion.strip().lower()
                if exclusion_clean and exclusion_clean in file_name.lower():
                    should_exclude = True
                    break
           
            # Exclure aussi les fichiers système générés automatiquement
            system_files = ['99_z_screenpreferences.rpy', '99_z_console.rpy']
            if file_name.lower() in [f.lower() for f in system_files]:
                should_exclude = True
           
            # NOUVEAU : VALIDATION STRICTE DU CONTENU
            if not should_exclude:
                try:
                    from core.services.extraction.validation import validate_file_for_translation_processing
                    validation_result = validate_file_for_translation_processing(file_path)
                    
                    if not validation_result['overall_valid']:
                        # Fichier technique détecté - l'exclure silencieusement
                        log_message("DEBUG", f"Fichier technique exclu: {file_name}", category="project_utils")
                        should_exclude = True
                        
                except Exception as e:
                    log_message("ATTENTION", f"Erreur validation {file_name}: {e}", category="project_utils")
                    # En cas d'erreur de validation, exclure par sécurité
                    should_exclude = True
           
            if not should_exclude:
                try:
                    file_size = os.path.getsize(file_path)
                    files.append({
                        'name': file_name,
                        'path': file_path,
                        'size': file_size,
                        'relative_path': os.path.relpath(file_path, language_path)
                    })
                except OSError:
                    continue
       
        # Trier par nom de fichier
        files.sort(key=lambda x: x['name'].lower())
        
        # Mettre en cache le résultat (tous les fichiers, les exclusions sont appliquées à la lecture)
        cache.cache_language_files(project_path, language, files)
        
        return files
       
    except Exception as e:
        log_message("ERREUR", f"Erreur scan fichiers pour {language}: {e}", category="project_utils")
        return files

def get_project_info_summary(project_path: str) -> str:
    """
    Génère un résumé d'informations sur le projet
    
    Args:
        project_path: Chemin vers le projet
        
    Returns:
        Chaîne d'information formatée
    """
    try:
        if not project_path or not os.path.exists(project_path):
            return "Aucun projet sélectionné"
        
        project_name = os.path.basename(project_path)
        
        # Analyser rapidement le projet
        game_dir = os.path.join(project_path, "game")
        if not os.path.isdir(game_dir):
            return f"Projet: {project_name} (pas de dossier game/)"
        
        # Compter les fichiers rapidement
        rpa_count = 0
        rpy_count = 0
        
        for f in os.listdir(game_dir):
            if f.endswith('.rpa'):
                rpa_count += 1
            elif f.endswith('.rpy'):
                rpy_count += 1
        
        # Chercher des traductions existantes
        languages = scan_project_languages(project_path)
        
        # Construire le message d'info
        info_parts = [f"Projet: {project_name}"]
        
        if rpa_count > 0:
            info_parts.append(f"{rpa_count} RPA")
        if rpy_count > 0:
            info_parts.append(f"{rpy_count} RPY")
        if languages:
            lang_names = [lang['name'] for lang in languages[:3]]
            info_parts.append(f"Traductions: {', '.join(lang_names)}")
            if len(languages) > 3:
                info_parts.append("...")
        
        return " • ".join(info_parts)
        
    except Exception as e:
        log_message("ATTENTION", f"Erreur info projet: {e}", category="project_utils")
        return f"Projet: {os.path.basename(project_path) if project_path else 'Unknown'}"

def parse_exclusions_string(exclusions_str: str) -> List[str]:
    """
    Parse une chaîne d'exclusions en liste
    
    Args:
        exclusions_str: Chaîne avec exclusions séparées par virgules
        
    Returns:
        Liste des exclusions nettoyées
    """
    if not exclusions_str:
        return []
    
    exclusions = [item.strip() for item in exclusions_str.split(',') if item.strip()]
    return exclusions