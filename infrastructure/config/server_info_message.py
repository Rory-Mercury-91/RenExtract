# infrastructure/config/server_info_message.py
"""
Message d'information sur le serveur persistant pour les utilisateurs
"""

SERVER_INFO_MESSAGE = """
🚀 NOUVEAU : Serveur Éditeur Persistant

RenExtract a démarré un serveur HTTP en arrière-plan qui restera actif
même après la fermeture de l'application.

✨ Avantages :
• Les boutons "Ouvrir dans l'éditeur" des rapports HTML fonctionnent TOUJOURS
• Travaillez sur vos corrections sans garder RenExtract ouvert
• Totalement automatique et transparent

🔒 Sécurité :
• Serveur accessible uniquement sur votre ordinateur (localhost)
• Aucun accès externe possible
• Consommation : ~10-20 Mo de RAM

ℹ️ Gestion :
• Le serveur démarre automatiquement au lancement
• Pour le désactiver : Paramètres → Éditeur → Décocher "Activer le serveur"
• Pour voir son état : Paramètres → Éditeur → Section "Serveur Persistant"

📖 Plus d'infos : Consultez README_SERVEUR_PERSISTANT.md
"""

SERVER_INFO_SHORT = """
✨ Nouveau : Serveur éditeur persistant démarré !
Les boutons "Ouvrir dans l'éditeur" fonctionnent maintenant même après fermeture de l'app.
→ Paramètres → Éditeur pour plus d'infos
"""

def should_show_server_info() -> bool:
    """Détermine si on doit afficher le message d'info sur le serveur"""
    import os
    from pathlib import Path
    
    # Fichier marqueur pour savoir si l'utilisateur a déjà vu le message
    try:
        from infrastructure.config.constants import FOLDERS
        config_dir = FOLDERS.get("configs", "05_ConfigRenExtract")
    except Exception:
        config_dir = "05_ConfigRenExtract"
    
    marker_file = os.path.join(config_dir, ".server_info_shown")
    
    if os.path.exists(marker_file):
        return False  # Déjà affiché
    
    # Créer le fichier marqueur
    try:
        Path(config_dir).mkdir(parents=True, exist_ok=True)
        Path(marker_file).touch()
    except:
        pass
    
    return True  # Première fois


def get_server_info_message(short: bool = False) -> str:
    """Retourne le message d'info approprié"""
    return SERVER_INFO_SHORT if short else SERVER_INFO_MESSAGE

