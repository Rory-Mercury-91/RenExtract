# infrastructure/helpers/subprocess_helper.py
# Helper pour subprocess sans fenêtre console sur Windows
# Évite WinError 50 / WinError 6 sous applications windowed (PyInstaller)

"""
Helper pour exécuter des subprocess sans afficher de fenêtre console sur Windows.

Sous une app --windowed (pas de console valide, éventuellement après AllocConsole/FreeConsole),
hériter de stdin/stdout/stderr provoque souvent :
  OSError: [WinError 50] The request is not supported
  OSError: [WinError 6] The handle is invalid

Ce module force la redirection des flux manquants et des flags silencieux.
"""

import sys
import subprocess
from typing import Any, Dict


def get_subprocess_flags() -> int:
    """
    Retourne les flags appropriés pour subprocess.run/Popen selon la plateforme.

    Sur Windows : subprocess.CREATE_NO_WINDOW pour masquer la console
    Sur autres plateformes : 0 (pas de flags spéciaux)
    """
    return subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0


def get_hidden_startupinfo():
    """
    STARTUPINFO Windows pour masquer la fenêtre (sans STARTF_USESTDHANDLES).

    STARTF_USESTDHANDLES sans handles valides peut provoquer WinError 50.
    Les redirections stdin/stdout/stderr sont gérées par subprocess lui-même.
    """
    if sys.platform != "win32":
        return None
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    return startupinfo


def apply_windows_subprocess_safety(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Applique les défauts sécurisés pour Windows (windowed / sans console).

    - CREATE_NO_WINDOW + STARTUPINFO masqué
    - Redirection des flux std non fournis vers DEVNULL (évite l'héritage de handles invalides)
    """
    if sys.platform != "win32":
        return kwargs

    safe = dict(kwargs)

    if "creationflags" not in safe:
        safe["creationflags"] = get_subprocess_flags()

    if "startupinfo" not in safe:
        safe["startupinfo"] = get_hidden_startupinfo()

    capture = bool(safe.get("capture_output"))

    # capture_output force stdout/stderr=PIPE dans subprocess.run : seul stdin reste à sécuriser
    if capture:
        if "stdin" not in safe:
            safe["stdin"] = subprocess.DEVNULL
        return safe

    has_stdin = "stdin" in safe
    has_stdout = "stdout" in safe
    has_stderr = "stderr" in safe

    if has_stdin or has_stdout or has_stderr:
        if not has_stdin:
            safe["stdin"] = subprocess.DEVNULL
        if not has_stdout:
            safe["stdout"] = subprocess.DEVNULL
        if not has_stderr:
            safe["stderr"] = subprocess.DEVNULL
    else:
        safe["stdin"] = subprocess.DEVNULL
        safe["stdout"] = subprocess.DEVNULL
        safe["stderr"] = subprocess.DEVNULL

    return safe


def run_silent(*args, **kwargs):
    """
    Exécute subprocess.run en masquant la fenêtre console sur Windows
    et en sécurisant les handles std (anti WinError 50/6).
    """
    kwargs = apply_windows_subprocess_safety(kwargs)
    return subprocess.run(*args, **kwargs)


def Popen_silent(*args, **kwargs):
    """
    Exécute subprocess.Popen en masquant la fenêtre console sur Windows
    et en sécurisant les handles std (anti WinError 50/6).
    """
    kwargs = apply_windows_subprocess_safety(kwargs)
    return subprocess.Popen(*args, **kwargs)


def check_output_silent(*args, **kwargs):
    """subprocess.check_output sécurisé pour Windows windowed."""
    kwargs = apply_windows_subprocess_safety(kwargs)
    # check_output impose stdout=PIPE : retirer un éventuel stdout DEVNULL du helper
    kwargs.pop("stdout", None)
    if "stderr" not in kwargs:
        kwargs["stderr"] = subprocess.DEVNULL
    return subprocess.check_output(*args, **kwargs)
