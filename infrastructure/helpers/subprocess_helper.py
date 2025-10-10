# utils/subprocess_helper.py
# Helper pour subprocess sans fenêtre console sur Windows

"""
Helper pour exécuter des subprocess sans afficher de fenêtre console sur Windows
"""

import sys
import subprocess


def get_subprocess_flags():
    """
    Retourne les flags appropriés pour subprocess.run/Popen selon la plateforme
    
    Sur Windows : subprocess.CREATE_NO_WINDOW pour masquer la console
    Sur autres plateformes : 0 (pas de flags spéciaux)
    
    Returns:
        int: Flags pour subprocess
    """
    return subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0


def run_silent(*args, **kwargs):
    """
    Exécute subprocess.run en masquant la fenêtre console sur Windows
    
    Args:
        *args: Arguments positionnels pour subprocess.run
        **kwargs: Arguments nommés pour subprocess.run
        
    Returns:
        CompletedProcess: Résultat de subprocess.run
    """
    # Ajouter creationflags si non spécifié
    if 'creationflags' not in kwargs:
        kwargs['creationflags'] = get_subprocess_flags()
    
    return subprocess.run(*args, **kwargs)


def Popen_silent(*args, **kwargs):
    """
    Exécute subprocess.Popen en masquant la fenêtre console sur Windows
    
    Args:
        *args: Arguments positionnels pour subprocess.Popen
        **kwargs: Arguments nommés pour subprocess.Popen
        
    Returns:
        Popen: Process Popen
    """
    # Ajouter creationflags si non spécifié
    if 'creationflags' not in kwargs:
        kwargs['creationflags'] = get_subprocess_flags()
    
    return subprocess.Popen(*args, **kwargs)

