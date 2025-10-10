# Créer un fichier common.py dans core/business/
# core/business/common.py

def get_french_common_translations():
    """
    Retourne le contenu complet du fichier common.rpy français
    Basé sur votre fichier traduit fourni
    
    Returns:
        str: Contenu complet du fichier common.rpy
    """
    return """# Fichier common français - Créé avant génération TL par RenExtract
# Traductions des éléments communs de l'interface Ren'Py

translate french strings:

    # renpy/common/00accessibility.rpy:28
    old "Self-voicing disabled."
    new "Voix automatique désactivée."

    # renpy/common/00accessibility.rpy:29
    old "Clipboard voicing enabled. "
    new "Lecture du presse-papiers activée. "

    # renpy/common/00accessibility.rpy:30
    old "Self-voicing enabled. "
    new "Voix automatique activée. "

    # renpy/common/00accessibility.rpy:62
    old "bar"
    new "barre"

    # renpy/common/00accessibility.rpy:63
    old "selected"
    new "sélectionné"

    # renpy/common/00accessibility.rpy:64
    old "viewport"
    new "fenêtre de visualisation"

    # renpy/common/00accessibility.rpy:65
    old "horizontal scroll"
    new "défilement horizontal"

    # renpy/common/00accessibility.rpy:66
    old "vertical scroll"
    new "défilement vertical"

    # renpy/common/00accessibility.rpy:67
    old "activate"
    new "activer"

    # renpy/common/00accessibility.rpy:68
    old "deactivate"
    new "désactiver"

    # renpy/common/00accessibility.rpy:69
    old "increase"
    new "augmenter"

    # renpy/common/00accessibility.rpy:70
    old "decrease"
    new "diminuer"

    # renpy/common/00accessibility.rpy:104
    old "Accessibility Menu. Use up and down arrows to navigate, and enter to activate buttons and bars."
    new "Menu d'accessibilité. Utilise les flèches haut/bas pour naviguer et Entrée pour activer les boutons et barres."

    # renpy/common/00accessibility.rpy:110
    old "Font Override"
    new "Police forcée"

    # renpy/common/00accessibility.rpy:114
    old "Default"
    new "Par défaut"

    # renpy/common/00accessibility.rpy:118
    old "DejaVu Sans"
    new "DejaVu Sans"

    # renpy/common/00accessibility.rpy:141
    old "Here you can choose a font used for text in the game. This is intended to be used to change to a font that is more readable."
    new "Ici, tu peux choisir la police utilisée pour le texte du jeu. C'est prévu pour basculer vers une police plus lisible."

    # renpy/common/00accessibility.rpy:146
    old "Text Size Scaling"
    new "Mise à l'échelle de la taille du texte"

    # renpy/common/00accessibility.rpy:149
    old "Reset"
    new "Réinitialiser"

    # renpy/common/00accessibility.rpy:152
    old "Line Spacing Scaling"
    new "Mise à l'échelle de l'interligne"

    # renpy/common/00accessibility.rpy:161
    old "High Contrast Text"
    new "Texte à fort contraste"

    # renpy/common/00accessibility.rpy:168
    old "Dyslexic Font"
    new "Police dyslexique"

    # renpy/common/00accessibility.rpy:172
    old "OpenDyslexic"
    new "OpenDyslexic"

    # renpy/common/00accessibility.rpy:184
    old "Enable self-voicing by default."
    new "Activer la voix automatique par défaut."

    # renpy/common/00accessibility.rpy:188
    old "Self-Voicing"
    new "Voix automatique"

    # renpy/common/00accessibility.rpy:192
    old "Self-voicing has been enabled."
    new "La voix automatique a été activée."

    # renpy/common/00accessibility.rpy:194
    old "Self-voicing has been disabled."
    new "La voix automatique a été désactivée."

    # renpy/common/00accessibility.rpy:200
    old "Enable self-voicing by holding down the V key."
    new "Maintiens la touche V pour activer la voix automatique."

    # renpy/common/00accessibility.rpy:206
    old "Text-to-speech"
    new "Synthèse vocale"

    # renpy/common/00accessibility.rpy:210
    old "Clipboard"
    new "Presse-papiers"

    # renpy/common/00accessibility.rpy:214
    old "Debug"
    new "Debug"

    # renpy/common/00accessibility.rpy:228
    old "Self-Voicing Volume Drop"
    new "Atténuation du volume pendant la voix auto"

    # renpy/common/00accessibility.rpy:237
    old "The options on this menu are intended to improve access...fonts, try to keep the text size the same as it originally was."
    new "Les options de ce menu visent à améliorer l'accessibilité. Si tu changes de police, essaie de garder la même taille de texte qu'à l'origine."

    # renpy/common/00accessibility.rpy:242
    old "Return"
    new "Retour"

    # renpy/common/00action_file.rpy:26
    old "{#weekday}Monday"
    new "{#weekday}Lundi"

    # renpy/common/00action_file.rpy:26
    old "{#weekday}Tuesday"
    new "{#weekday}Mardi"

    # renpy/common/00action_file.rpy:26
    old "{#weekday}Wednesday"
    new "{#weekday}Mercredi"

    # renpy/common/00action_file.rpy:26
    old "{#weekday}Thursday"
    new "{#weekday}Jeudi"

    # renpy/common/00action_file.rpy:26
    old "{#weekday}Friday"
    new "{#weekday}Vendredi"

    # renpy/common/00action_file.rpy:26
    old "{#weekday}Saturday"
    new "{#weekday}Samedi"

    # renpy/common/00action_file.rpy:26
    old "{#weekday}Sunday"
    new "{#weekday}Dimanche"

    # renpy/common/00action_file.rpy:42
    old "{#month}January"
    new "{#month}Janvier"

    # renpy/common/00action_file.rpy:42
    old "{#month}February"
    new "{#month}Février"

    # renpy/common/00action_file.rpy:42
    old "{#month}March"
    new "{#month}Mars"

    # renpy/common/00action_file.rpy:42
    old "{#month}April"
    new "{#month}Avril"

    # renpy/common/00action_file.rpy:42
    old "{#month}May"
    new "{#month}Mai"

    # renpy/common/00action_file.rpy:42
    old "{#month}June"
    new "{#month}Juin"

    # renpy/common/00action_file.rpy:42
    old "{#month}July"
    new "{#month}Juillet"

    # renpy/common/00action_file.rpy:42
    old "{#month}August"
    new "{#month}Août"

    # renpy/common/00action_file.rpy:42
    old "{#month}September"
    new "{#month}Septembre"

    # renpy/common/00action_file.rpy:42
    old "{#month}October"
    new "{#month}Octobre"

    # renpy/common/00action_file.rpy:42
    old "{#month}November"
    new "{#month}Novembre"

    # renpy/common/00action_file.rpy:42
    old "{#month}December"
    new "{#month}Décembre"

    # renpy/common/00action_file.rpy:59
    old "{#month_short}Jan"
    new "{#month_short}Janv"

    # renpy/common/00action_file.rpy:59
    old "{#month_short}Feb"
    new "{#month_short}Févr"

    # renpy/common/00action_file.rpy:59
    old "{#month_short}Mar"
    new "{#month_short}Mars"

    # renpy/common/00action_file.rpy:59
    old "{#month_short}Apr"
    new "{#month_short}Avr"

    # renpy/common/00action_file.rpy:59
    old "{#month_short}May"
    new "{#month_short}Mai"

    # renpy/common/00action_file.rpy:59
    old "{#month_short}Jun"
    new "{#month_short}Juin"

    # renpy/common/00action_file.rpy:59
    old "{#month_short}Jul"
    new "{#month_short}Juil"

    # renpy/common/00action_file.rpy:59
    old "{#month_short}Aug"
    new "{#month_short}Août"

    # renpy/common/00action_file.rpy:59
    old "{#month_short}Sep"
    new "{#month_short}Sept"

    # renpy/common/00action_file.rpy:59
    old "{#month_short}Oct"
    new "{#month_short}Oct"

    # renpy/common/00action_file.rpy:59
    old "{#month_short}Nov"
    new "{#month_short}Nov"

    # renpy/common/00action_file.rpy:59
    old "{#month_short}Dec"
    new "{#month_short}Déc"

    # renpy/common/00action_file.rpy:76
    old "%b %d, %H:%M"
    new "%d %b, %H:%M"

    # renpy/common/00action_file.rpy:326
    old "Save slot %s: [text]"
    new "Sauvegarde emplacement %s : [text]"

    # renpy/common/00action_file.rpy:331
    old "Load slot %s: [text]"
    new "Charger l'emplacement %s : [text]"

    # renpy/common/00action_file.rpy:387
    old "Delete slot [text]"
    new "Supprimer l'emplacement [text]"

    # renpy/common/00action_file.rpy:768
    old "File page auto"
    new "Page auto"

    # renpy/common/00action_file.rpy:770
    old "File page quick"
    new "Page rapide"

    # renpy/common/00action_file.rpy:769
    old "File page [text]"
    new "Page [text]"

    # renpy/common/00action_file.rpy:816
    old "Next file page."
    new "Page suivante."

    # renpy/common/00action_file.rpy:888
    old "Previous file page."
    new "Page précédente."

    # renpy/common/00action_file.rpy:949
    old "Quick save complete."
    new "Sauvegarde rapide terminée."

    # renpy/common/00action_file.rpy:964
    old "Quick save."
    new "Sauvegarde rapide."

    # renpy/common/00action_file.rpy:983
    old "Quick load."
    new "Chargement rapide."

    # renpy/common/00action_other.rpy:379
    old "Language [text]"
    new "Langue [text]"

    # renpy/common/00action_other.rpy:744
    old "Open [text] directory."
    new "Ouvrir le dossier [text]."

    # renpy/common/00director.rpy:712
    old "The interactive director is not enabled here."
    new "Le directeur interactif n'est pas activé ici."

    # renpy/common/00director.rpy:1511
    old "⬆"
    new "⬆"

    # renpy/common/00director.rpy:1517
    old "⬇"
    new "⬇"

    # renpy/common/00director.rpy:1581
    old "Done"
    new "Terminé"

    # renpy/common/00director.rpy:1591
    old "(statement)"
    new "(instruction)"

    # renpy/common/00director.rpy:1592
    old "(tag)"
    new "(balise)"

    # renpy/common/00director.rpy:1593
    old "(attributes)"
    new "(attributs)"

    # renpy/common/00director.rpy:1594
    old "(transform)"
    new "(transformation)"

    # renpy/common/00director.rpy:1619
    old "(transition)"
    new "(transition)"

    # renpy/common/00director.rpy:1631
    old "(channel)"
    new "(canal)"

    # renpy/common/00director.rpy:1632
    old "(filename)"
    new "(nom de fichier)"

    # renpy/common/00director.rpy:1661
    old "Change"
    new "Changer"

    # renpy/common/00director.rpy:1663
    old "Add"
    new "Ajouter"

    # renpy/common/00director.rpy:1666
    old "Cancel"
    new "Annuler"

    # renpy/common/00director.rpy:1669
    old "Remove"
    new "Supprimer"

    # renpy/common/00director.rpy:1704
    old "Statement:"
    new "Instruction :"

    # renpy/common/00director.rpy:1725
    old "Tag:"
    new "Balise :"

    # renpy/common/00director.rpy:1741
    old "Attributes:"
    new "Attributs :"

    # renpy/common/00director.rpy:1752
    old "Click to toggle attribute, right click to toggle negative attribute."
    new "Clique pour activer/désactiver un attribut, clic droit pour activer/désactiver un attribut négatif."

    # renpy/common/00director.rpy:1764
    old "Transforms:"
    new "Transformations :"

    # renpy/common/00director.rpy:1775
    old "Click to set transform, right click to add to transform list."
    new "Clique pour définir une transformation, clic droit pour l'ajouter à la liste."

    # renpy/common/00director.rpy:1776
    old "Customize director.transforms to add more transforms."
    new "Personnalise director.transforms pour ajouter plus de transformations."

    # renpy/common/00director.rpy:1788
    old "Behind:"
    new "Derrière :"

    # renpy/common/00director.rpy:1799
    old "Click to set, right click to add to behind list."
    new "Clique pour définir, clic droit pour ajouter à la liste arrière-plan."

    # renpy/common/00director.rpy:1811
    old "Transition:"
    new "Transition :"

    # renpy/common/00director.rpy:1821
    old "Click to set."
    new "Clique pour définir."

    # renpy/common/00director.rpy:1822
    old "Customize director.transitions to add more transitions."
    new "Personnalise director.transitions pour ajouter plus de transitions."

    # renpy/common/00director.rpy:1834
    old "Channel:"
    new "Canal :"

    # renpy/common/00director.rpy:1845
    old "Customize director.audio_channels to add more channels."
    new "Personnalise director.audio_channels pour ajouter plus de canaux."

    # renpy/common/00director.rpy:1857
    old "Audio Filename:"
    new "Nom de fichier audio :"

    # renpy/common/00gui.rpy:448
    old "Are you sure?"
    new "Es-tu sûr ?"

    # renpy/common/00gui.rpy:449
    old "Are you sure you want to delete this save?"
    new "Es-tu sûr de vouloir supprimer cette sauvegarde ?"

    # renpy/common/00gui.rpy:450
    old "Are you sure you want to overwrite your save?"
    new "Es-tu sûr de vouloir écraser ta sauvegarde ?"

    # renpy/common/00gui.rpy:451
    old "Loading will lose unsaved progress.\\nAre you sure you want to do this?"
    new "Le chargement fera perdre ta progression non sauvegardée.\\nEs-tu sûr de vouloir continuer ?"

    # renpy/common/00gui.rpy:452
    old "Are you sure you want to quit?"
    new "Es-tu sûr de vouloir quitter ?"

    # renpy/common/00gui.rpy:453
    old "Are you sure you want to return to the main menu?\\nThis will lose unsaved progress."
    new "Es-tu sûr de vouloir revenir au menu principal ?\\nCela fera perdre ta progression non sauvegardée."

    # renpy/common/00gui.rpy:454
    old "Are you sure you want to continue where you left off?"
    new "Es-tu sûr de vouloir reprendre là où tu t'es arrêté ?"

    # renpy/common/00gui.rpy:455
    old "Are you sure you want to end the replay?"
    new "Es-tu sûr de vouloir arrêter la relecture ?"

    # renpy/common/00gui.rpy:456
    old "Are you sure you want to begin skipping?"
    new "Es-tu sûr de vouloir commencer à passer ?"

    # renpy/common/00gui.rpy:457
    old "Are you sure you want to skip to the next choice?"
    new "Es-tu sûr de vouloir passer au prochain choix ?"

    # renpy/common/00gui.rpy:458
    old "Are you sure you want to skip unseen dialogue to the next choice?"
    new "Es-tu sûr de vouloir passer les dialogues non vus jusqu'au prochain choix ?"

    # renpy/common/00gui.rpy:459
    old "This save was created on a different device. Maliciously constructed save files can harm your computer. Do you trust this save's creator and everyone who could have changed the file?"
    new "Cette sauvegarde a été créée sur un autre appareil. Des fichiers de sauvegarde malveillants peuvent endommager ton ordinateur. Fais-tu confiance au créateur de cette sauvegarde et à toute personne qui aurait pu la modifier ?"

    # renpy/common/00gui.rpy:460
    old "Do you trust the device the save was created on? You should only choose yes if you are the device's sole user."
    new "Fais-tu confiance à l'appareil sur lequel la sauvegarde a été créée ? Tu ne devrais répondre oui que si tu es l'unique utilisateur de cet appareil."

    # renpy/common/00keymap.rpy:325
    old "Failed to save screenshot as %s."
    new "Échec de la capture d'écran sous %s."

    # renpy/common/00keymap.rpy:346
    old "Saved screenshot as %s."
    new "Capture d'écran enregistrée sous %s."

    # renpy/common/00library.rpy:248
    old "Skip Mode"
    new "Mode avance rapide"

    # renpy/common/00library.rpy:335
    old "This program contains free software under a number of licenses, including the MIT License and GNU Lesser General Public License. A complete list of software, including links to full source code, can be found {a=https://www.renpy.org/l/license}here{/a}."
    new "Ce programme contient des logiciels libres sous diverses licences, dont la licence MIT et la GNU LGPL. Une liste complète des logiciels, avec liens vers le code source, se trouve {a=https://www.renpy.org/l/license}ici{/a}."

    # renpy/common/00preferences.rpy:290
    old "display"
    new "affichage"

    # renpy/common/00preferences.rpy:310
    old "transitions"
    new "transitions"

    # renpy/common/00preferences.rpy:319
    old "skip transitions"
    new "passer les transitions"

    # renpy/common/00preferences.rpy:321
    old "video sprites"
    new "sprites vidéo"

    # renpy/common/00preferences.rpy:330
    old "show empty window"
    new "afficher une fenêtre vide"

    # renpy/common/00preferences.rpy:339
    old "text speed"
    new "vitesse du texte"

    # renpy/common/00preferences.rpy:347
    old "joystick"
    new "joystick"

    # renpy/common/00preferences.rpy:347
    old "joystick..."
    new "joystick..."

    # renpy/common/00preferences.rpy:354
    old "skip"
    new "passer"

    # renpy/common/00preferences.rpy:357
    old "skip unseen [text]"
    new "passer texte non vu [text]"

    # renpy/common/00preferences.rpy:362
    old "skip unseen text"
    new "passer le texte non vu"

    # renpy/common/00preferences.rpy:364
    old "begin skipping"
    new "commencer à passer"

    # renpy/common/00preferences.rpy:368
    old "after choices"
    new "après les choix"

    # renpy/common/00preferences.rpy:375
    old "skip after choices"
    new "passer après les choix"

    # renpy/common/00preferences.rpy:377
    old "auto-forward time"
    new "délai d'avance auto"

    # renpy/common/00preferences.rpy:391
    old "auto-forward"
    new "avance auto"

    # renpy/common/00preferences.rpy:398
    old "Auto forward"
    new "Avance auto"

    # renpy/common/00preferences.rpy:401
    old "auto-forward after click"
    new "avance auto après clic"

    # renpy/common/00preferences.rpy:410
    old "automatic move"
    new "mouvement automatique"

    # renpy/common/00preferences.rpy:419
    old "wait for voice"
    new "attendre la voix"

    # renpy/common/00preferences.rpy:428
    old "voice sustain"
    new "maintien de la voix"

    # renpy/common/00preferences.rpy:437
    old "self voicing"
    new "voix automatique"

    # renpy/common/00preferences.rpy:440
    old "self voicing enable"
    new "activer la voix auto"

    # renpy/common/00preferences.rpy:442
    old "self voicing disable"
    new "désactiver la voix auto"

    # renpy/common/00preferences.rpy:446
    old "self voicing volume drop"
    new "atténuation volume voix auto"

    # renpy/common/00preferences.rpy:454
    old "clipboard voicing"
    new "lecture presse-papiers"

    # renpy/common/00preferences.rpy:457
    old "clipboard voicing enable"
    new "activer lecture presse-papiers"

    # renpy/common/00preferences.rpy:459
    old "clipboard voicing disable"
    new "désactiver lecture presse-papiers"

    # renpy/common/00preferences.rpy:463
    old "debug voicing"
    new "voix debug"

    # renpy/common/00preferences.rpy:466
    old "debug voicing enable"
    new "activer voix debug"

    # renpy/common/00preferences.rpy:468
    old "debug voicing disable"
    new "désactiver voix debug"

    # renpy/common/00preferences.rpy:472
    old "emphasize audio"
    new "mettre l'audio en avant"

    # renpy/common/00preferences.rpy:481
    old "rollback side"
    new "côté retour"

    # renpy/common/00preferences.rpy:491
    old "gl powersave"
    new "gl économie d'énergie"

    # renpy/common/00preferences.rpy:497
    old "gl framerate"
    new "gl fréquence d'images"

    # renpy/common/00preferences.rpy:500
    old "gl tearing"
    new "gl déchirement"

    # renpy/common/00preferences.rpy:503
    old "font transform"
    new "transformation police"

    # renpy/common/00preferences.rpy:506
    old "font size"
    new "taille police"

    # renpy/common/00preferences.rpy:514
    old "font line spacing"
    new "espacement des lignes"

    # renpy/common/00preferences.rpy:522
    old "system cursor"
    new "curseur système"

    # renpy/common/00preferences.rpy:531
    old "renderer menu"
    new "menu rendu"

    # renpy/common/00preferences.rpy:534
    old "accessibility menu"
    new "menu accessibilité"

    # renpy/common/00preferences.rpy:537
    old "high contrast text"
    new "texte contraste élevé"

    # renpy/common/00preferences.rpy:546
    old "audio when minimized"
    new "audio quand réduit"

    # renpy/common/00preferences.rpy:555
    old "audio when unfocused"
    new "audio quand non focalisé"

    # renpy/common/00preferences.rpy:564
    old "web cache preload"
    new "préchargement cache web"

    # renpy/common/00preferences.rpy:579
    old "voice after game menu"
    new "voix après menu du jeu"

    # renpy/common/00preferences.rpy:588
    old "restore window position"
    new "restaurer position fenêtre"

    # renpy/common/00preferences.rpy:597
    old "reset"
    new "réinitialiser"

    # renpy/common/00preferences.rpy:610
    old "main volume"
    new "volume principal"

    # renpy/common/00preferences.rpy:611
    old "music volume"
    new "volume musique"

    # renpy/common/00preferences.rpy:612
    old "sound volume"
    new "volume effets"

    # renpy/common/00preferences.rpy:613
    old "voice volume"
    new "volume voix"

    # renpy/common/00preferences.rpy:614
    old "mute main"
    new "muet principal"

    # renpy/common/00preferences.rpy:615
    old "mute music"
    new "muet musique"

    # renpy/common/00preferences.rpy:616
    old "mute sound"
    new "muet effets"

    # renpy/common/00preferences.rpy:617
    old "mute voice"
    new "muet voix"

    # renpy/common/00preferences.rpy:618
    old "mute all"
    new "tout muet"

    # renpy/common/00preferences.rpy:701
    old "Clipboard voicing enabled. Press 'shift+C' to disable."
    new "Lecture du presse-papiers activée. Appuie sur 'shift+C' pour désactiver."

    # renpy/common/00preferences.rpy:703
    old "Self-voicing would say \\"[renpy.display.tts.last]\\". Press 'alt+shift+V' to disable."
    new "La voix automatique dirait « [renpy.display.tts.last] ». Appuie sur 'alt+shift+V' pour désactiver."

    # renpy/common/00preferences.rpy:705
    old "Self-voicing enabled. Press 'v' to disable."
    new "Voix automatique activée. Appuie sur 'v' pour désactiver."

    # renpy/common/00speechbubble.rpy:416
    old "Speech Bubble Editor"
    new "Éditeur de bulles de dialogue"

    # renpy/common/00speechbubble.rpy:421
    old "(hide)"
    new "(cacher)"

    # renpy/common/00speechbubble.rpy:432
    old "(clear retained bubbles)"
    new "(effacer bulles conservées)"

    # renpy/common/00sync.rpy:70
    old "Sync downloaded."
    new "Synchronisation téléchargée."

    # renpy/common/00sync.rpy:193
    old "Could not connect to the Ren'Py Sync server."
    new "Impossible de se connecter au serveur de synchronisation Ren'Py."

    # renpy/common/00sync.rpy:195
    old "The Ren'Py Sync server timed out."
    new "Délai dépassé pour le serveur de synchronisation Ren'Py."

    # renpy/common/00sync.rpy:197
    old "An unknown error occurred while connecting to the Ren'Py Sync server."
    new "Erreur inconnue lors de la connexion au serveur de synchronisation Ren'Py."

    # renpy/common/00sync.rpy:213
    old "The Ren'Py Sync server does not have a copy of this sync. The sync ID may be invalid, or it may have timed out."
    new "Le serveur de synchronisation Ren'Py n'a pas de copie de cette synchro. L'ID peut être invalide ou avoir expiré."

    # renpy/common/00sync.rpy:316
    old "Please enter the sync ID you generated.\\nNever enter a sync ID you didn't create yourself."
    new "Entre l'ID de synchro que tu as généré.\\nN'entre jamais un ID que tu n'as pas créé toi-même."

    # renpy/common/00sync.rpy:335
    old "The sync ID is not in the correct format."
    new "L'ID de synchro n'est pas au bon format."

    # renpy/common/00sync.rpy:355
    old "The sync could not be decrypted."
    new "La synchro n'a pas pu être déchiffrée."

    # renpy/common/00sync.rpy:378
    old "The sync belongs to a different game."
    new "La synchro appartient à un autre jeu."

    # renpy/common/00sync.rpy:383
    old "The sync contains a file with an invalid name."
    new "La synchro contient un fichier avec un nom invalide."

    # renpy/common/00sync.rpy:440
    old "This will upload your saves to the {a=https://sync.renpy.org}Ren'Py Sync Server{/a}.\\nDo you want to continue?"
    new "Cela va envoyer tes sauvegardes sur le {a=https://sync.renpy.org}serveur de synchro Ren'Py{/a}.\\nVeux-tu continuer ?"

    # renpy/common/00sync.rpy:472
    old "Enter Sync ID"
    new "Entrer l'ID de synchro"

    # renpy/common/00sync.rpy:483
    old "This will contact the {a=https://sync.renpy.org}Ren'Py Sync Server{/a}."
    new "Cela va contacter le {a=https://sync.renpy.org}serveur de synchro Ren'Py{/a}."

    # renpy/common/00sync.rpy:513
    old "Sync Success"
    new "Synchronisation réussie"

    # renpy/common/00sync.rpy:516
    old "The Sync ID is:"
    new "L'ID de synchronisation est :"

    # renpy/common/00sync.rpy:522
    old "You can use this ID to download your save on another device.\\nThis sync will expire in an hour.\\nRen'Py Sync is supported by {a=https://www.renpy.org/sponsors.html}Ren'Py's Sponsors{/a}."
    new "Tu peux utiliser cet ID pour télécharger ta sauvegarde sur un autre appareil.\\nCette synchronisation expirera dans une heure.\\nRen'Py Sync est soutenu par {a=https://www.renpy.org/sponsors.html}les sponsors de Ren'Py{/a}."

    # renpy/common/00sync.rpy:526
    old "Continue"
    new "Continuer"

    # renpy/common/00sync.rpy:551
    old "Sync Error"
    new "Erreur de synchronisation"

    # renpy/common/00translation.rpy:63
    old "Translation identifier: [identifier]"
    new "Identifiant de traduction : [identifier]"

    # renpy/common/00translation.rpy:84
    old " translates [tl.filename]:[tl.linenumber]"
    new " traduit [tl.filename]:[tl.linenumber]"

    # renpy/common/00translation.rpy:101
    old "\\n{color=#fff}Copied to clipboard.{/color}"
    new "\\n{color=#fff}Copié dans le presse-papiers.{/color}"

    # renpy/common/00iap.rpy:231
    old "Contacting App Store\\nPlease Wait..."
    new "Connexion à l'App Store\\nVeuillez patienter..."

    # renpy/common/00updater.rpy:505
    old "No update methods found."
    new "Aucune méthode de mise à jour trouvée."

    # renpy/common/00updater.rpy:552
    old "Could not download file list: "
    new "Impossible de télécharger la liste des fichiers : "

    # renpy/common/00updater.rpy:555
    old "File list digest does not match."
    new "L'empreinte de la liste des fichiers ne correspond pas."

    # renpy/common/00updater.rpy:765
    old "An error is being simulated."
    new "Une erreur est simulée."

    # renpy/common/00updater.rpy:953
    old "Either this project does not support updating, or the update status file was deleted."
    new "Soit ce projet ne prend pas en charge la mise à jour, soit le fichier d'état de mise à jour a été supprimé."

    # renpy/common/00updater.rpy:967
    old "This account does not have permission to perform an update."
    new "Ce compte n'a pas la permission d'effectuer une mise à jour."

    # renpy/common/00updater.rpy:970
    old "This account does not have permission to write the update log."
    new "Ce compte n'a pas la permission d'écrire dans le journal de mise à jour."

    # renpy/common/00updater.rpy:1050
    old "Could not verify update signature."
    new "Impossible de vérifier la signature de la mise à jour."

    # renpy/common/00updater.rpy:1373
    old "The update file was not downloaded."
    new "Le fichier de mise à jour n'a pas été téléchargé."

    # renpy/common/00updater.rpy:1391
    old "The update file does not have the correct digest - it may have been corrupted."
    new "Le fichier de mise à jour n'a pas la bonne empreinte — il a peut-être été corrompu."

    # renpy/common/00updater.rpy:1541
    old "While unpacking {}, unknown type {}."
    new "Lors de la décompression de {}, type inconnu {}."

    # renpy/common/00updater.rpy:2022
    old "Updater"
    new "Mise à jour"

    # renpy/common/00updater.rpy:2029
    old "An error has occured:"
    new "Une erreur est survenue :"

    # renpy/common/00updater.rpy:2031
    old "Checking for updates."
    new "Vérification des mises à jour."

    # renpy/common/00updater.rpy:2033
    old "This program is up to date."
    new "Ce programme est à jour."

    # renpy/common/00updater.rpy:2035
    old "[u.version] is available. Do you want to install it?"
    new "[u.version] est disponible. Veux-tu l'installer ?"

    # renpy/common/00updater.rpy:2037
    old "Preparing to download the updates."
    new "Préparation du téléchargement des mises à jour."

    # renpy/common/00updater.rpy:2039
    old "Downloading the updates."
    new "Téléchargement des mises à jour."

    # renpy/common/00updater.rpy:2041
    old "Unpacking the updates."
    new "Décompression des mises à jour."

    # renpy/common/00updater.rpy:2043
    old "Finishing up."
    new "Finalisation."

    # renpy/common/00updater.rpy:2045
    old "The updates have been installed. The program will restart."
    new "Les mises à jour ont été installées. Le programme va redémarrer."

    # renpy/common/00updater.rpy:2047
    old "The updates have been installed."
    new "Les mises à jour ont été installées."

    # renpy/common/00updater.rpy:2049
    old "The updates were cancelled."
    new "Les mises à jour ont été annulées."

    # renpy/common/00updater.rpy:2064
    old "Proceed"
    new "Continuer"

    # renpy/common/00updater.rpy:2080
    old "Preparing to download the game data."
    new "Préparation du téléchargement des données du jeu."

    # renpy/common/00updater.rpy:2082
    old "Downloading the game data."
    new "Téléchargement des données du jeu."

    # renpy/common/00updater.rpy:2084
    old "The game data has been downloaded."
    new "Les données du jeu ont été téléchargées."

    # renpy/common/00updater.rpy:2086
    old "An error occured when trying to download game data:"
    new "Une erreur est survenue lors du téléchargement des données du jeu :"

    # renpy/common/00updater.rpy:2091
    old "This game cannot be run until the game data has been downloaded."
    new "Ce jeu ne peut pas être lancé tant que les données n'ont pas été téléchargées."

    # renpy/common/00updater.rpy:2098
    old "Retry"
    new "Réessayer"

    # renpy/common/00gallery.rpy:643
    old "Image [index] of [count] locked."
    new "Image [index] sur [count] verrouillée."

    # renpy/common/00gallery.rpy:663
    old "prev"
    new "précédent"

    # renpy/common/00gallery.rpy:664
    old "next"
    new "suivant"

    # renpy/common/00gallery.rpy:665
    old "slideshow"
    new "diaporama"

    # renpy/common/00gallery.rpy:666
    old "return"
    new "retour"

    # renpy/common/00gltest.rpy:90
    old "Renderer"
    new "Moteur de rendu"

    # renpy/common/00gltest.rpy:94
    old "Automatically Choose"
    new "Choisir automatiquement"

    # renpy/common/00gltest.rpy:101
    old "Force GL Renderer"
    new "Forcer rendu GL"

    # renpy/common/00gltest.rpy:106
    old "Force ANGLE Renderer"
    new "Forcer rendu ANGLE"

    # renpy/common/00gltest.rpy:111
    old "Force GLES Renderer"
    new "Forcer rendu GLES"

    # renpy/common/00gltest.rpy:117
    old "Force GL2 Renderer"
    new "Forcer rendu GL2"

    # renpy/common/00gltest.rpy:122
    old "Force ANGLE2 Renderer"
    new "Forcer rendu ANGLE2"

    # renpy/common/00gltest.rpy:127
    old "Force GLES2 Renderer"
    new "Forcer rendu GLES2"

    # renpy/common/00gltest.rpy:137
    old "Enable (No Blocklist)"
    new "Activer (pas de liste de blocage)"

    # renpy/common/00gltest.rpy:160
    old "Powersave"
    new "Économie d'énergie"

    # renpy/common/00gltest.rpy:174
    old "Framerate"
    new "Fréquence d'images"

    # renpy/common/00gltest.rpy:178
    old "Screen"
    new "Écran"

    # renpy/common/00gltest.rpy:182
    old "60"
    new "60"

    # renpy/common/00gltest.rpy:186
    old "30"
    new "30"

    # renpy/common/00gltest.rpy:192
    old "Tearing"
    new "Déchirement"

    # renpy/common/00gltest.rpy:208
    old "Changes will take effect the next time this program is run."
    new "Les changements prendront effet au prochain lancement du programme."

    # renpy/common/00gltest.rpy:215
    old "Quit"
    new "Quitter"

    # renpy/common/00gltest.rpy:244
    old "Performance Warning"
    new "Avertissement de performance"

    # renpy/common/00gltest.rpy:249
    old "This computer is using software rendering."
    new "Cet ordinateur utilise le rendu logiciel."

    # renpy/common/00gltest.rpy:251
    old "This game requires use of GL2 that can't be initialised."
    new "Ce jeu nécessite l'utilisation de GL2 qui n'a pas pu être initialisé."

    # renpy/common/00gltest.rpy:253
    old "This computer has a problem displaying graphics: [problem]."
    new "Cet ordinateur rencontre un problème d'affichage graphique : [problem]."

    # renpy/common/00gltest.rpy:257
    old "Its graphics drivers may be out of date or not operating correctly. This can lead to slow or incorrect graphics display."
    new "Ses pilotes graphiques peuvent être obsolètes ou ne pas fonctionner correctement. Cela peut entraîner un affichage lent ou incorrect."

    # renpy/common/00gltest.rpy:261
    old "The {a=edit:1:log.txt}log.txt{/a} file may contain information to help you determine what is wrong with your computer."
    new "Le fichier {a=edit:1:log.txt}log.txt{/a} peut contenir des informations pour t'aider à identifier le problème avec ton ordinateur."

    # renpy/common/00gltest.rpy:266
    old "More details on how to fix this can be found in the {a=[url]}documentation{/a}."
    new "Plus de détails sur la façon de corriger ce problème se trouvent dans la {a=[url]}documentation{/a}."

    # renpy/common/00gltest.rpy:271
    old "Continue, Show this warning again"
    new "Continuer, afficher à nouveau cet avertissement"

    # renpy/common/00gltest.rpy:275
    old "Continue, Don't show warning again"
    new "Continuer, ne plus afficher cet avertissement"

    # renpy/common/00gltest.rpy:283
    old "Change render options"
    new "Changer les options de rendu"

    # renpy/common/00gamepad.rpy:33
    old "Select Gamepad to Calibrate"
    new "Sélectionne la manette à calibrer"

    # renpy/common/00gamepad.rpy:36
    old "No Gamepads Available"
    new "Aucune manette disponible"

    # renpy/common/00gamepad.rpy:56
    old "Calibrating [name] ([i]/[total])"
    new "Calibration de [name] ([i]/[total])"

    # renpy/common/00gamepad.rpy:60
    old "Press or move the '[control!s]' [kind]."
    new "Appuie ou bouge le '[control!s]' [kind]."

    # renpy/common/00gamepad.rpy:70
    old "Skip (A)"
    new "Passer (A)"

    # renpy/common/00gamepad.rpy:73
    old "Back (B)"
    new "Retour (B)"

    # renpy/common/_errorhandling.rpym:673
    old "Open"
    new "Ouvrir"

    # renpy/common/_errorhandling.rpym:675
    old "Opens the traceback.txt file in a text editor."
    new "Ouvre le fichier traceback.txt dans un éditeur de texte."

    # renpy/common/_errorhandling.rpym:677
    old "Copy BBCode"
    new "Copier en BBCode"

    # renpy/common/_errorhandling.rpym:679
    old "Copies the traceback.txt file to the clipboard as BBcode for forums like https://lemmasoft.renai.us/."
    new "Copie le fichier traceback.txt dans le presse-papiers en BBCode pour les forums comme https://lemmasoft.renai.us/."

    # renpy/common/_errorhandling.rpym:681
    old "Copy Markdown"
    new "Copier en Markdown"

    # renpy/common/_errorhandling.rpym:683
    old "Copies the traceback.txt file to the clipboard as Markdown for Discord."
    new "Copie le fichier traceback.txt dans le presse-papiers en Markdown pour Discord."

    # renpy/common/_errorhandling.rpym:715
    old "An exception has occurred."
    new "Une exception est survenue."

    # renpy/common/_errorhandling.rpym:738
    old "Rollback"
    new "Retour arrière"

    # renpy/common/_errorhandling.rpym:740
    old "Attempts a roll back to a prior time, allowing you to save or choose a different choice."
    new "Tente un retour arrière à un moment précédent, te permettant de sauvegarder ou de choisir une autre option."

    # renpy/common/_errorhandling.rpym:743
    old "Ignore"
    new "Ignorer"

    # renpy/common/_errorhandling.rpym:747
    old "Ignores the exception, allowing you to continue."
    new "Ignore l'exception, te permettant de continuer."

    # renpy/common/_errorhandling.rpym:749
    old "Ignores the exception, allowing you to continue. This often leads to additional errors."
    new "Ignore l'exception, te permettant de continuer. Cela entraîne souvent des erreurs supplémentaires."

    # renpy/common/_errorhandling.rpym:753
    old "Reload"
    new "Recharger"

    # renpy/common/_errorhandling.rpym:755
    old "Reloads the game from disk, saving and restoring game state if possible."
    new "Recharge le jeu depuis le disque, en sauvegardant et restaurant l'état de la partie si possible."

    # renpy/common/_errorhandling.rpym:758
    old "Console"
    new "Console"

    # renpy/common/_errorhandling.rpym:760
    old "Opens a console to allow debugging the problem."
    new "Ouvre une console pour permettre le débogage du problème."

    # renpy/common/_errorhandling.rpym:773
    old "Quits the game."
    new "Quitte le jeu."

    # renpy/common/_errorhandling.rpym:795
    old "Parsing the script failed."
    new "L'analyse du script a échoué."

    # renpy/common/_developer/developer.rpym:39
    old "Developer Menu"
    new "Menu développeur"

    # renpy/common/_developer/developer.rpym:44
    old "Interactive Director (D)"
    new "Directeur interactif (D)"

    # renpy/common/_developer/developer.rpym:46
    old "Reload Game (Shift+R)"
    new "Recharger le jeu (Shift+R)"

    # renpy/common/_developer/developer.rpym:48
    old "Console (Shift+O)"
    new "Console (Shift+O)"

    # renpy/common/_developer/developer.rpym:50
    old "Variable Viewer"
    new "Visualiseur de variables"

    # renpy/common/_developer/developer.rpym:52
    old "Persistent Viewer"
    new "Visualiseur de persistance"

    # renpy/common/_developer/developer.rpym:54
    old "Image Location Picker"
    new "Sélecteur d'emplacement d'image"

    # renpy/common/_developer/developer.rpym:56
    old "Filename List"
    new "Liste des fichiers"

    # renpy/common/_developer/developer.rpym:60
    old "Show Image Load Log (F4)"
    new "Afficher le journal de chargement d'images (F4)"

    # renpy/common/_developer/developer.rpym:63
    old "Hide Image Load Log (F4)"
    new "Masquer le journal de chargement d'images (F4)"

    # renpy/common/_developer/developer.rpym:66
    old "Image Attributes"
    new "Attributs d'image"

    # renpy/common/_developer/developer.rpym:70
    old "Show Translation Info"
    new "Afficher les infos de traduction"

    # renpy/common/_developer/developer.rpym:73
    old "Hide Translation Info"
    new "Masquer les infos de traduction"

    # renpy/common/_developer/developer.rpym:78
    old "Speech Bubble Editor (Shift+B)"
    new "Éditeur de bulles de dialogue (Shift+B)"

    # renpy/common/_developer/developer.rpym:82
    old "Show Filename and Line"
    new "Afficher nom de fichier et ligne"

    # renpy/common/_developer/developer.rpym:85
    old "Hide Filename and Line"
    new "Masquer nom de fichier et ligne"

    # renpy/common/_developer/developer.rpym:129
    old "Layer [l]:"
    new "Calque [l] :"

    # renpy/common/_developer/developer.rpym:133
    old "    [name] [attributes] (hidden)"
    new "    [name] [attributes] (caché)"

    # renpy/common/_developer/developer.rpym:137
    old "    [name] [attributes]"
    new "    [name] [attributes]"

    # renpy/common/_developer/developer.rpym:190
    old "Nothing to inspect."
    new "Rien à inspecter."

    # renpy/common/_developer/developer.rpym:201
    old "Hide deleted"
    new "Masquer les supprimés"

    # renpy/common/_developer/developer.rpym:201
    old "Show deleted"
    new "Afficher les supprimés"

    # renpy/common/_developer/developer.rpym:352
    old "Rectangle copied to clipboard."
    new "Rectangle copié dans le presse-papiers."

    # renpy/common/_developer/developer.rpym:355
    old "Position copied to clipboard."
    new "Position copiée dans le presse-papiers."

    # renpy/common/_developer/developer.rpym:367
    old "Rectangle: %r"
    new "Rectangle : %r"

    # renpy/common/_developer/developer.rpym:370
    old "Mouse position: %r"
    new "Position de la souris : %r"

    # renpy/common/_developer/developer.rpym:375
    old "Right-click or escape to quit."
    new "Clic droit ou Échap pour quitter."

    # renpy/common/_developer/developer.rpym:425
    old "Type to filter: "
    new "Tape pour filtrer : "

    # renpy/common/_developer/developer.rpym:544
    old "Textures: [tex_count] ([tex_size_mb:.1f] MB)"
    new "Textures : [tex_count] ([tex_size_mb:.1f] Mo)"

    # renpy/common/_developer/developer.rpym:548
    old "Image cache: [cache_pct:.1f]% ([cache_size_mb:.1f] MB)"
    new "Cache d'images : [cache_pct:.1f]% ([cache_size_mb:.1f] Mo)"

    # renpy/common/_developer/developer.rpym:558
    old "✔ "
    new "✔ "

    # renpy/common/_developer/developer.rpym:561
    old "✘ "
    new "✘ "

    # renpy/common/_developer/developer.rpym:566
    old "\\n{color=#cfc}✔ predicted image (good){/color}\\n{color=#fcc}✘ unpredicted image (bad){/color}\\n{color=#fff}Drag to move.{/color}"
    new "\\n{color=#cfc}✔ image prédite (ok){/color}\\n{color=#fcc}✘ image non prédite (erreur){/color}\\n{color=#fff}Glisse pour déplacer.{/color}"

    # renpy/common/_developer/developer.rpym:616
    old "Click to open in editor."
    new "Clique pour ouvrir dans l'éditeur."

    # renpy/common/_developer/inspector.rpym:39
    old "Displayable Inspector"
    new "Inspecteur d'éléments affichables"

    # renpy/common/_developer/inspector.rpym:62
    old "Size"
    new "Taille"

    # renpy/common/_developer/inspector.rpym:66
    old "Style"
    new "Style"

    # renpy/common/_developer/inspector.rpym:72
    old "Location"
    new "Emplacement"

    # renpy/common/_developer/inspector.rpym:124
    old "Inspecting Styles of [displayable_name!q]"
    new "Inspection des styles de [displayable_name!q]"

    # renpy/common/_developer/inspector.rpym:141
    old "displayable:"
    new "affichable :"

    # renpy/common/_developer/inspector.rpym:147
    old "        (no properties affect the displayable)"
    new "        (aucune propriété n'affecte l'affichable)"

    # renpy/common/_developer/inspector.rpym:149
    old "        (default properties omitted)"
    new "        (propriétés par défaut omises)"

    # renpy/common/_developer/inspector.rpym:187
    old "<repr() failed>"
    new "<repr() a échoué>"

    # renpy/common/00console.rpy:538
    old "Press <esc> to exit console. Type help for help.\\n"
    new "Appuie sur <Échap> pour quitter la console. Tape help pour obtenir de l'aide.\\n"

    # renpy/common/00console.rpy:542
    old "Ren'Py script enabled."
    new "Script Ren'Py activé."

    # renpy/common/00console.rpy:544
    old "Ren'Py script disabled."
    new "Script Ren'Py désactivé."

    # renpy/common/00console.rpy:725
    old "The console is using short representations. To disable this, type 'long', and to re-enable, type 'short'"
    new "La console utilise des représentations courtes. Pour désactiver cela, tape 'long', et pour réactiver, tape 'short'"

    # renpy/common/00console.rpy:797
    old "help: show this help\\n help <expr>: show signature and documentation of <expr>"
    new "help : afficher cette aide\\n help <expr> : afficher la signature et la documentation de <expr>"

    # renpy/common/00console.rpy:821
    old "Help may display undocumented functions. Please check that the function or\\nclass you want to use is documented.\\n\\n"
    new "L'aide peut afficher des fonctions non documentées. Vérifie que la fonction ou\\nla classe que tu veux utiliser est bien documentée.\\n\\n"

    # renpy/common/00console.rpy:830
    old "commands:\\n"
    new "commandes :\\n"

    # renpy/common/00console.rpy:840
    old " <renpy script statement>: run the statement\\n"
    new " <instruction de script Ren'Py> : exécuter l'instruction\\n"

    # renpy/common/00console.rpy:842
    old " <python expression or statement>: run the expression or statement"
    new " <expression ou instruction Python> : exécuter l'expression ou l'instruction"

    # renpy/common/00console.rpy:850
    old "clear: clear the console history"
    new "clear : effacer l'historique de la console"

    # renpy/common/00console.rpy:854
    old "exit: exit the console"
    new "exit : quitter la console"

    # renpy/common/00console.rpy:862
    old "stack: print the return stack"
    new "stack : afficher la pile de retour"

    # renpy/common/00console.rpy:884
    old "load <slot>: loads the game from slot"
    new "load <slot> : charger la partie depuis l'emplacement"

    # renpy/common/00console.rpy:897
    old "save <slot>: saves the game in slot"
    new "save <slot> : sauvegarder la partie dans l'emplacement"

    # renpy/common/00console.rpy:908
    old "reload: reloads the game, refreshing the scripts"
    new "reload : recharger le jeu, rafraîchissant les scripts"

    # renpy/common/00console.rpy:916
    old "watch <expression>: watch a python expression\\n watch short: makes the representation of traced expressions short (default)\\n watch long: makes the representation of traced expressions as is"
    new "watch <expression> : surveiller une expression Python\\n watch short : rend la représentation des expressions surveillées courte (par défaut)\\n watch long : garde la représentation des expressions surveillées telle quelle"

    # renpy/common/00console.rpy:953
    old "unwatch <expression>: stop watching an expression"
    new "unwatch <expression> : arrêter de surveiller une expression"

    # renpy/common/00console.rpy:999
    old "unwatchall: stop watching all expressions"
    new "unwatchall : arrêter de surveiller toutes les expressions"

    # renpy/common/00console.rpy:1020
    old "jump <label>: jumps to label"
    new "jump <label> : aller au label"

    # renpy/common/00console.rpy:1036
    old "short: Shorten the representation of objects on the console (default)."
    new "short : raccourcit la représentation des objets dans la console (par défaut)."

    # renpy/common/00console.rpy:1040
    old "long: Print the full representation of objects on the console."
    new "long : affiche la représentation complète des objets dans la console."

    # renpy/common/00console.rpy:1044
    old "escape: Enables escaping of unicode symbols in unicode strings."
    new "escape : active l'échappement des symboles unicode dans les chaînes."

    # renpy/common/00console.rpy:1048
    old "unescape: Disables escaping of unicode symbols in unicode strings and print it as is (default)."
    new "unescape : désactive l'échappement des symboles unicode et les affiche tels quels (par défaut)."

    # renpy/common/_layout/classic_joystick_preferences.rpym:94
    old "Joystick Mapping"
    new "Configuration du joystick"

    # renpy/common/_layout/classic_load_save.rpym:138
    old "Empty Slot."
    new "Emplacement vide."

    # renpy/common/_layout/classic_load_save.rpym:170
    old "a"
    new "a"

    # renpy/common/_layout/classic_load_save.rpym:179
    old "q"
    new "q"

    # renpy/common/00accessibility.rpy:151
    old "Opendyslexic"
    new "Opendyslexic"

    # renpy/common/00accessibility.rpy:183
    old "Enable"
    new "Activer"

    # renpy/common/00accessibility.rpy:187
    old "Disable"
    new "Désactiver"

    # renpy/common/00accessibility.rpy:197
    old "Self-voicing support is limited when using a touch screen."
    new "Le support de la synthèse vocale est limité lors de l’utilisation d’un écran tactile."

    # renpy/common/00accessibility.rpy:201
    old "Off"
    new "Désactivé"

    # renpy/common/00accessibility.rpy:236
    old "The options on this menu are intended to improve accessibility. They may not work with all games, and some combinations of options may render the game unplayable. This is not an issue with the game or engine. For the best results when changing fonts, try to keep the text size the same as it originally was."
    new "Les options de ce menu visent à améliorer l’accessibilité. Elles peuvent ne pas fonctionner avec tous les jeux, et certaines combinaisons d’options peuvent rendre le jeu injouable. Ce n’est pas un problème du jeu ou du moteur. Pour de meilleurs résultats lors du changement de police, essaie de conserver la taille de texte identique à celle d’origine."

    # renpy/common/00action_file.rpy:37
    old "{#weekday_short}Mon"
    new "{#weekday_short}Lun"

    # renpy/common/00action_file.rpy:37
    old "{#weekday_short}Tue"
    new "{#weekday_short}Mar"

    # renpy/common/00action_file.rpy:37
    old "{#weekday_short}Wed"
    new "{#weekday_short}Mer"

    # renpy/common/00action_file.rpy:37
    old "{#weekday_short}Thu"
    new "{#weekday_short}Jeu"

    # renpy/common/00action_file.rpy:37
    old "{#weekday_short}Fri"
    new "{#weekday_short}Ven"

    # renpy/common/00action_file.rpy:37
    old "{#weekday_short}Sat"
    new "{#weekday_short}Sam"

    # renpy/common/00action_file.rpy:37
    old "{#weekday_short}Sun"
    new "{#weekday_short}Dim"

    # renpy/common/_developer/developer.rpym:69
    old "Show Translation Identifiers"
    new "Afficher les identifiants de traduction"

    # renpy/common/_developer/developer.rpym:72
    old "Hide Translation Identifiers"
    new "Masquer les identifiants de traduction"

    # renpy/common/_developer/developer.rpym:612
    old "\\n{color=#fff}Click to copy.\\nDrag to move.{/color}"
    new "\\n{color=#fff}Clique pour copier.\\nGlisse pour déplacer.{/color}"

    # renpy/common/00updater.rpy:419
    old "The Ren'Py Updater is not supported on mobile devices."
    new "Le système de mise à jour Ren'Py n'est pas pris en charge sur les appareils mobiles."

    # renpy/common/_developer/developer.rpym:97
    old "[name] [attributes] (hidden)"
    new "[name] [attributes] (caché)"

    # renpy/common/_developer/developer.rpym:101
    old "[name] [attributes]"
    new "[name] [attributes]"

"""
