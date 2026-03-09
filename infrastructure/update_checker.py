# infrastructure/update_checker.py
# Vérification des mises à jour via GitHub Releases

"""
Vérifie les mises à jour disponibles sur GitHub (Rory-Mercury-91/RenExtract).
Permet de ne télécharger que les assets nécessaires (lien vers la release ou asset zip).
"""

import re
from typing import Optional, Tuple, List, Dict, Any

GITHUB_REPO = "Rory-Mercury-91/RenExtract"
GITHUB_API_LATEST = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
GITHUB_RELEASES_PAGE = f"https://github.com/{GITHUB_REPO}/releases"


def _normalize_version(version_str: str) -> Tuple[int, ...]:
    """Convertit une chaîne de version en tuple d'entiers pour comparaison (ex: 'v1.2.28' -> (1, 2, 28))."""
    if not version_str or not isinstance(version_str, str):
        return (0,)
    s = version_str.strip()
    # Enlever préfixes courants
    for prefix in ("RenExtract ", "v", "V"):
        if s.startswith(prefix):
            s = s[len(prefix):].strip()
    # Extraire les nombres (ex: "1.2.28" ou "2026.03.09.v1" -> 2026, 3, 9, 1)
    parts = re.findall(r"\d+", s)
    if not parts:
        return (0,)
    return tuple(int(p) for p in parts)


def get_current_version() -> str:
    """Retourne la version actuelle de l'application."""
    try:
        from infrastructure.config.constants import VERSION
        return (VERSION or "").strip()
    except Exception:
        return ""


def fetch_latest_release() -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Récupère la dernière release depuis l'API GitHub.
    Returns:
        (release_dict, error_message). release_dict contient tag_name, name, html_url, assets, body.
    """
    try:
        import urllib.request
        req = urllib.request.Request(
            GITHUB_API_LATEST,
            headers={"Accept": "application/vnd.github.v3+json"},
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            import json
            data = json.loads(resp.read().decode("utf-8"))
            return (data, None)
    except Exception as e:
        return (None, str(e))


def has_update(current: str, latest_tag_or_name: str) -> bool:
    """Retourne True si latest est considéré comme plus récent que current."""
    cur = _normalize_version(current)
    lat = _normalize_version(latest_tag_or_name)
    # Comparaison par tuples (remplir avec des 0 si longueurs différentes)
    max_len = max(len(cur), len(lat))
    cur_pad = cur + (0,) * (max_len - len(cur))
    lat_pad = lat + (0,) * (max_len - len(lat))
    return lat_pad > cur_pad


def get_update_assets(release: Dict[str, Any]) -> List[Dict[str, str]]:
    """Retourne la liste des assets de la release (name, browser_download_url, size)."""
    assets = release.get("assets") or []
    return [
        {"name": a.get("name", ""), "url": a.get("browser_download_url", ""), "size": a.get("size", 0)}
        for a in assets
    ]


def check_for_updates() -> Tuple[bool, str, str, List[Dict[str, str]]]:
    """
    Vérifie s'il existe une mise à jour.
    Returns:
        (has_update, latest_version_str, release_url, list_of_assets)
        Si erreur: has_update=False, latest_version_str="", release_url="", assets=[]
    """
    current = get_current_version()
    release, err = fetch_latest_release()
    if err or not release:
        return (False, "", "", [])

    tag = release.get("tag_name") or ""
    name = release.get("name") or tag
    html_url = release.get("html_url") or GITHUB_RELEASES_PAGE
    assets = get_update_assets(release)

    latest_display = name or tag or "inconnue"
    if not has_update(current, latest_display):
        return (False, latest_display, html_url, assets)

    return (True, latest_display, html_url, assets)


def download_update_zip(dest_dir: str = None, release_tag: str = None) -> tuple:
    """
    Télécharge le zip de la dernière release Windows dans le dossier de l'exe (ou dest_dir).
    Returns:
        (success: bool, path_or_error: str) — en cas de succès, chemin du fichier zip ; sinon message d'erreur.
    """
    import urllib.request
    import os
    release, err = fetch_latest_release()
    if err or not release:
        return (False, err or "Impossible de récupérer la release")
    assets = get_update_assets(release)
    # Chercher un asset .zip Windows
    zip_asset = None
    for a in assets:
        name = (a.get("name") or "").lower()
        if name.endswith(".zip") and ("windows" in name or "win" in name):
            zip_asset = a
            break
    if not zip_asset:
        for a in assets:
            if (a.get("name") or "").lower().endswith(".zip"):
                zip_asset = a
                break
    if not zip_asset or not zip_asset.get("url"):
        return (False, "Aucun fichier zip Windows trouvé dans la release")
    url = zip_asset["url"]
    name = zip_asset.get("name") or "RenExtract-update.zip"
    if dest_dir is None:
        try:
            from infrastructure.config.constants import BASE_DIR
            dest_dir = BASE_DIR
        except Exception:
            dest_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, name)
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/octet-stream"}, method="GET")
        with urllib.request.urlopen(req, timeout=120) as resp:
            with open(dest_path, "wb") as f:
                f.write(resp.read())
        return (True, dest_path)
    except Exception as e:
        return (False, str(e))
