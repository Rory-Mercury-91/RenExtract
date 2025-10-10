# Créer un fichier screens.py dans core/business/
# core/business/screens.py

def get_french_screen_content():
    """
    Retourne le contenu complet du fichier common.rpy français
    Basé sur votre fichier traduit fourni
    
    Returns:
        str: Contenu complet du fichier common.rpy
    """    
    return """# Fichier screens français - Créé avant génération TL par RenExtract
# Traductions des éléments screens de l'interface Ren'Py

translate french strings:

    # game/screens.rpy:285
    old "Back"
    new "Retour"

    # game/screens.rpy:286
    old "History"
    new "Historique"

    # game/screens.rpy:287
    old "Skip"
    new "Passer"

    # game/screens.rpy:288
    old "Auto"
    new "Auto"

    # game/screens.rpy:289
    old "Save"
    new "Sauvegarde"

    # game/screens.rpy:290
    old "Q.Save"
    new "Sauv R."

    # game/screens.rpy:291
    old "Q.Load"
    new "Charg R."

    # game/screens.rpy:292
    old "Prefs"
    new "Options"

    # game/screens.rpy:333
    old "Start"
    new "Démarrer"

    # game/screens.rpy:341
    old "Load"
    new "Charger"

    # game/screens.rpy:343
    old "Preferences"
    new "Préférences"

    # game/screens.rpy:347
    old "End Replay"
    new "Terminer la relecture"

    # game/screens.rpy:351
    old "Main Menu"
    new "Menu principal"

    # game/screens.rpy:353
    old "About"
    new "À propos"

    # game/screens.rpy:358
    old "Help"
    new "Aide"

    # game/screens.rpy:593
    old "Version [config.version!t]\\n"
    new "Version [config.version!t]\\n"

    # game/screens.rpy:599
    old "Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\\n\\n[renpy.license!t]"
    new "Fait avec {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\\n\\n[renpy.license!t]"

    # game/screens.rpy:635
    old "Page {}"
    new "Page {}"

    # game/screens.rpy:635
    old "Automatic saves"
    new "Sauvegardes automatiques"

    # game/screens.rpy:635
    old "Quick saves"
    new "Sauvegardes rapides"

    # game/screens.rpy:677
    old "{#file_time}%A, %B %d %Y, %H:%M"
    new "{#file_time}%A %d %B %Y, %H:%M"

    # game/screens.rpy:677
    old "empty slot"
    new "emplacement vide"

    # game/screens.rpy:697
    old "<"
    new "<"

    # game/screens.rpy:700
    old "{#auto_page}A"
    new "{#auto_page}A"

    # game/screens.rpy:703
    old "{#quick_page}Q"
    new "{#quick_page}R"

    # game/screens.rpy:709
    old ">"
    new ">"

    # game/screens.rpy:713
    old "Upload Sync"
    new "Envoi synchro"

    # game/screens.rpy:717
    old "Download Sync"
    new "Téléch. synchro"

    # game/screens.rpy:776
    old "Display"
    new "Affichage"

    # game/screens.rpy:777
    old "Window"
    new "Fenêtre"

    # game/screens.rpy:778
    old "Fullscreen"
    new "Plein écran"

    # game/screens.rpy:783
    old "Unseen Text"
    new "Texte non vu"

    # game/screens.rpy:784
    old "After Choices"
    new "Après les choix"

    # game/screens.rpy:785
    old "Transitions"
    new "Transitions"

    # game/screens.rpy:798
    old "Text Speed"
    new "Vitesse du texte"

    # game/screens.rpy:802
    old "Auto-Forward Time"
    new "Délai avance auto"

    # game/screens.rpy:809
    old "Music Volume"
    new "Volume musique"

    # game/screens.rpy:816
    old "Sound Volume"
    new "Volume effets"

    # game/screens.rpy:822
    old "Test"
    new "Test"

    # game/screens.rpy:826
    old "Voice Volume"
    new "Volume voix"

    # game/screens.rpy:837
    old "Mute All"
    new "Tout muet"

    # game/screens.rpy:956
    old "The dialogue history is empty."
    new "L’historique des dialogues est vide."

    # game/screens.rpy:1024
    old "Keyboard"
    new "Clavier"

    # game/screens.rpy:1025
    old "Mouse"
    new "Souris"

    # game/screens.rpy:1028
    old "Gamepad"
    new "Manette"

    # game/screens.rpy:1041
    old "Enter"
    new "Entrée"

    # game/screens.rpy:1042
    old "Advances dialogue and activates the interface."
    new "Fait avancer le dialogue et active l’interface."

    # game/screens.rpy:1045
    old "Space"
    new "Espace"

    # game/screens.rpy:1046
    old "Advances dialogue without selecting choices."
    new "Fait avancer le dialogue sans sélectionner de choix."

    # game/screens.rpy:1049
    old "Arrow Keys"
    new "Flèches"

    # game/screens.rpy:1050
    old "Navigate the interface."
    new "Permet de naviguer dans l’interface."

    # game/screens.rpy:1053
    old "Escape"
    new "Échap"

    # game/screens.rpy:1054
    old "Accesses the game menu."
    new "Accède au menu du jeu."

    # game/screens.rpy:1057
    old "Ctrl"
    new "Ctrl"

    # game/screens.rpy:1058
    old "Skips dialogue while held down."
    new "Passe le dialogue tant que la touche est maintenue."

    # game/screens.rpy:1061
    old "Tab"
    new "Tab"

    # game/screens.rpy:1062
    old "Toggles dialogue skipping."
    new "Active/désactive le passage de dialogues."

    # game/screens.rpy:1065
    old "Page Up"
    new "Page Haut"

    # game/screens.rpy:1066
    old "Rolls back to earlier dialogue."
    new "Revient à un dialogue précédent."

    # game/screens.rpy:1069
    old "Page Down"
    new "Page Bas"

    # game/screens.rpy:1070
    old "Rolls forward to later dialogue."
    new "Avance vers un dialogue suivant."

    # game/screens.rpy:1074
    old "Hides the user interface."
    new "Masque l’interface utilisateur."

    # game/screens.rpy:1078
    old "Takes a screenshot."
    new "Prend une capture d’écran."

    # game/screens.rpy:1082
    old "Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}."
    new "Active/désactive la {a=https://www.renpy.org/l/voicing}voix automatique{/a}."

    # game/screens.rpy:1086
    old "Opens the accessibility menu."
    new "Ouvre le menu accessibilité."

    # game/screens.rpy:1092
    old "Left Click"
    new "Clic gauche"

    # game/screens.rpy:1096
    old "Middle Click"
    new "Clic milieu"

    # game/screens.rpy:1100
    old "Right Click"
    new "Clic droit"

    # game/screens.rpy:1104
    old "Mouse Wheel Up"
    new "Molette vers le haut"

    # game/screens.rpy:1108
    old "Mouse Wheel Down"
    new "Molette vers le bas"

    # game/screens.rpy:1115
    old "Right Trigger\\nA/Bottom Button"
    new "Gâchette droite\\nA/Bouton bas"

    # game/screens.rpy:1119
    old "Left Trigger\\nLeft Shoulder"
    new "Gâchette gauche\\nGâchette haute gauche"

    # game/screens.rpy:1123
    old "Right Shoulder"
    new "Gâchette haute droite"

    # game/screens.rpy:1127
    old "D-Pad, Sticks"
    new "Croix directionnelle, sticks"

    # game/screens.rpy:1131
    old "Start, Guide, B/Right Button"
    new "Start, Guide, B/Bouton droit"

    # game/screens.rpy:1135
    old "Y/Top Button"
    new "Y/Bouton haut"

    # game/screens.rpy:1138
    old "Calibrate"
    new "Calibrer"

    # game/screens.rpy:1203
    old "Yes"
    new "Oui"

    # game/screens.rpy:1204
    old "No"
    new "Non"

    # game/screens.rpy:1250
    old "Skipping"
    new "Passage en cours"

    # game/screens.rpy:1562
    old "Menu"
    new "Menu"

"""