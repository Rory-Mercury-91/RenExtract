
# 📝 CHANGELOG - RenExtract

## 2026-03-03 (v1.2.25)

### Interface : barres de défilement par onglet
- **Outils de maintenance** (Nettoyage, Éditeur temps réel, Vérification cohérence) : contenu de chaque onglet dans une zone scrollable ; barre de défilement affichée **uniquement si le contenu dépasse** la zone visible ; molette (Windows + Linux) sur toute la zone.
- **Générateur de traductions** et **Paramètres** : même logique appliquée à tous les onglets (scroll par onglet, barre seulement si nécessaire, molette).
- Module partagé `ui/shared/scrollable_tab.py` pour éviter la duplication de code.

### Rapport de cohérence : tuiles et enregistrement
- **Tuiles réductibles** : chaque ligne d’erreur est une tuile ouvrable/fermable (ouverte par défaut) ; clic sur l’en-tête (Ligne X) pour replier ou déplier.
- **Appliquer tout** : après application des traductions en lot, les cases sont **décochées** et les tuiles concernées **fermées** automatiquement.
- **Enregistrer tout** (bandeau) : ne sauvegarde **que les lignes réellement modifiées** (comparaison avec la valeur initiale).
- **Bouton Enregistrer** (par ligne) : après enregistrement, la tuile se **ferme** et la case « Inclure dans traduction en lot » est **désactivée**.
- **Lignes enregistrées** : la case « Inclure dans traduction en lot » est **décochée et désactivée** (enregistrement ligne par ligne ou via Enregistrer tout).

### Interface des onglets
- **Bouton « À quoi ça sert ? »** aligné sur la **même ligne** que la phrase descriptive dans les onglets Nettoyage, Éditeur temps réel et Vérification cohérence.

---

## 2026-03-02 (v1.2.24)

### Nouvelle fonctionnalité : Traduction par lot
- **Système de traduction par lot** dans le rapport de cohérence : panneau dédié (repliable, fermé par défaut) pour traduire plusieurs lignes en une fois.
- Étapes : choix du traducteur, sélection des lignes (case « Ancien », limites selon traducteur), **Copier tout** → traduction externe (Google/DeepL, etc.) → **Coller tout** → **Appliquer** → **Enregistrer tout** dans le bandeau (évite de sauvegarder ligne par ligne).
- Bouton **Focus Traduction par Lot** dans les filtres : ouvre le panneau et scroll jusqu’à « Résumé Global » pour l’afficher.

### Paramètres (Cohérence / Traduction)
- **Seuil de similarité (lignes non traduites)** : alerter si au moins X % des mots sont inchangés entre ancien et nouveau (réglable 50–100 %, ex. 87 %).
- **Réutiliser le même onglet navigateur** pour la traduction (Google/DeepL) lors de traduction consécutive multiple.

### Modification : Bloc Fonctionnalités du rapport
- **Bloc « Fonctionnalités présentes »** : panneau repliable (fermé par défaut) listant toutes les fonctionnalités du rapport (résumé, filtres, thème, édition en ligne, traduction assistée, exclusions, traduction en lot).
- **Lignes non traduites** : dans le rapport, affichage du pourcentage de contenu inchangé pour les lignes partiellement non traduites (ex. « Ligne partiellement non traduite (X % du contenu inchangé) »).

### Corrections
- **Extraction** : distinction entre la directive Ren'Py `old "..."` et un locuteur dont le nom contient « old » (ex. `oldman "..."`). Seules les lignes commençant par `old ` (avec espace) sont ignorées comme directive, afin de ne pas exclure les dialogues de personnages comme « oldman ».
- **Démarrage Windows** : correction de l’erreur « Descripteur non valide » (WinError 6 / SystemError) lors de la vérification du verrou singleton (processus déjà en cours).
- **Fenêtres CMD en flash** : tous les appels subprocess au démarrage et à l’usage (git, netstat, taskkill, explorer, test éditeur) utilisent désormais `CREATE_NO_WINDOW` sous Windows pour ne plus afficher de console.

---

## 2026-01-21 (v1.2.23-Fix2)

### 🚨 Fix urgent téléchargement v2 unrenpyc
- **Problème** : Erreur critique lors du téléchargement de la version v2 de unrenpyc.
- **Correction** : Mise à jour de la logique de téléchargement dans `core/services/translation/rpa_extraction_business.py` pour pointer vers la bonne version.
- **Mise à jour** : Changement de la version dans les constantes concernées.

**Fichiers modifiés :**
- `core/services/translation/rpa_extraction_business.py`
- `infrastructure/config/constants.py`

**Impact** : Téléchargement de la version correcte de unrenpyc v2, extraction RPA fonctionnelle à nouveau.

---

## 2026-01-17 (v1.2.23-Fix)

### 🐛 Corrections de linting
- **Correction f-string JavaScript** : Résolution des erreurs de linting dans `html_report_generator.py` causées par l'interprétation incorrecte des accolades JavaScript dans une f-string Python.
- **Solution** : Remplacement de la f-string par une chaîne normale avec injection de variable via `.replace()`, permettant de conserver toutes les accolades JavaScript sans conflit avec le parser Python.
- **Suppression guillemet orphelin** : Nettoyage d'un guillemet restant qui cassait la syntaxe de la f-string.

**Fichiers modifiés :**
- `core/services/reporting/html_report_generator.py`

**Impact** : Résolution de toutes les erreurs de linting liées aux expressions f-string, amélioration de la maintenabilité du code JavaScript généré.

## 2026-01-10 (v1.2.23)

### 🛡️ Sécurité & Stabilité des ports (Configurables)
- **Correction Critique** : RenExtract ne tue plus d'autres applications au démarrage. L'outil vérifie désormais le **nom du processus** et la **ligne de commande** avant d'exécuter un `kill` ; les processus non identifiés sont ignorés et loggés.
- **Ports Configurables** : Lecture des ports depuis la configuration (`editor_server_port`, `hotkey_server_port`, `orphaned_ports`).
- **Nouveau Standard** : Port hotkey par défaut modifié en **45000** (toujours modifiable via `config.json`).
- **Amélioration Logs** : Journalisation explicite lorsque le nettoyage d'un port est sauté (ex: `Saut nettoyage port 8766 (PID 8448, proc: electron.exe)`).
- **Tests & Docs** : Ajout de tests unitaires pour la détection de processus et mise à jour du `README.md` avec un exemple de `04_Configs/config.json`.

**Fichiers modifiés :**
- `main.py`, `ui/shared/hotkey_manager.py`, `ui/shared/editor_manager_server.py`
- `infrastructure/config/constants.py`, `infrastructure/helpers/server_utils.py`
- `core/services/reporting/html_report_generator.py`, `ui/tab_tools/realtime_editor_tab.py`
- `README.md`, `scripts/git_push_fix.sh`, `Z_Ne_Pas_supprimer/tests/`

**Impact** : Empêche la fermeture involontaire d'applications tierces (ex: Le Nexus) et permet une personnalisation totale de l'infrastructure réseau de l'outil.

## 2025-12-23 (v1.2.22)

### 🔒 Fusion contrôlée pour `textes_manquants.rpy`
- Limitation : la proposition de fusion est désormais effectuée **uniquement** depuis le flux d'extraction (export), et **n'est plus** déclenchée automatiquement par les helpers d'écriture.
- Avant toute fusion automatique, une sauvegarde est créée via le type de backup **BEFORE_FUSION**.
- Le dialogue natif de confirmation "Remplacer le fichier" a été désactivé (`confirmoverwrite=False`) pour laisser l'application gérer la logique de fusion proprement.

### ✅ Nettoyage et tests locaux
- Suppression des scripts temporaires utilisés pendant le debug.
- Ajout de tests automatisés couvrant : fusion pour `textes_manquants.rpy` et écriture normale pour les autres cas.
- Les tests sont conservés **localement** dans `Z_Ne_Pas_supprimer/tests/` et exclus du dépôt distant pour éviter d'exposer du code de test dans le repo principal.

### 🧹 Petits nettoyages
- Simplification de `_safe_write_file` : comportement par défaut = écriture simple, paramètre inutile retiré.

**Fichiers modifiés :**
- `core/services/translation/text_extraction_results_business.py` (gestion fusion + backup)
- `core/services/translation/translation_generation_business.py` (écriture sûre par défaut)
- `ui/tab_generator/extraction_results_tab.py` (suppression confirmation native `Save As`)
- `core/models/backup/unified_backup_manager.py` (usage de `BEFORE_FUSION`)


## 2025-12-15 (v1.2.21)

### 🐛 Corrections et améliorations

#### 🧹 Nettoyage intelligent – correction du système d'exclusion de fichiers
- **Problème résolu** : Les fichiers ajoutés dans le champ "Fichiers à exclure du nettoyage" étaient quand même nettoyés
- **Solution** :
  - Ajout de logs détaillés pour diagnostiquer les exclusions (chaîne brute, liste finale, vérification par fichier)
  - Amélioration de la vérification des exclusions avec logging de chaque étape
  - Affichage clair des fichiers exclus (système ou utilisateur) dans les logs
  - Vérification insensible à la casse pour les exclusions utilisateur
- **Impact** : Les exclusions de fichiers fonctionnent maintenant correctement, permettant de protéger les fichiers personnalisés du nettoyage automatique
- **Fichiers modifiés** :
  - `core/services/tools/cleaning_business.py` : Amélioration du logging dans `_should_exclude_file()`, `_get_excluded_files()` et `_clean_language_folder_unified()`

---

## 2025-11-28 (v1.2.20)

### ✨ Améliorations

#### 🔄 Système d'extraction – détection et rechargement d'extraction existante
- **Nouveauté** : Détection automatique d'une extraction existante avant de lancer une nouvelle extraction
- **Détails** :
  - Vérification automatique de l'existence d'une extraction précédente pour le fichier chargé
  - Affichage d'une boîte de dialogue avec 3 options : Recharger l'extraction existante / Refaire une extraction complète / Annuler
  - Rechargement intelligent de l'extraction existante sans refaire le processus complet
  - Affichage de la date de l'extraction existante pour information
  - Support des fichiers multiples (dialogue, doublons, astérisques)
  - Ouverture automatique des fichiers si l'option est activée
- **Impact** : Permet de reprendre une traduction interrompue sans perdre le travail déjà effectué, évite les extractions inutiles
- **Fichiers modifiés** :
  - `core/app_controller.py` : Ajout de `_check_existing_extraction()` et `_load_existing_extraction()`, modification de `extract_texts()`
  - `core/services/extraction/extraction.py` : Sauvegarde des compteurs dans `positions.json` pour permettre le rechargement

#### 🎭 Éditeur temps réel – modification du locuteur
- **Nouveauté** : Possibilité de modifier le locuteur d'un dialogue directement depuis l'éditeur temps réel
- **Détails** :
  - Affichage du nom du locuteur au-dessus du texte (VO et VF) avec son nom réel depuis les définitions de personnages
  - Combobox déroulante listant tous les locuteurs trouvés dans le jeu (scan automatique des fichiers .rpy)
  - Modification du fichier source Ren'Py : remplacement de la lettre du locuteur (ex: `jessica "texte"` → `madison "texte"`)
  - Préservation du contenu du dialogue lors du changement de locuteur
  - Backup automatique avant modification du fichier source
  - Cache des locuteurs scannés pour améliorer les performances
- **Impact** : Correction rapide des inversions de noms de personnages directement depuis l'éditeur, sans avoir à modifier manuellement les fichiers source
- **Fichiers modifiés** :
  - `ui/tab_tools/realtime_editor_tab.py` : Interface avec combobox, scan des locuteurs, modification du fichier source

### 🐛 Corrections et améliorations

#### 💾 Générateur de traductions – extension correcte pour les backups screen preferences
- **Problème résolu** : Le fichier de backup du fichier `99_Z_ScreenPreferences.rpy` était créé avec une extension incorrecte
- **Solution** : Le backup est maintenant créé avec l'extension `.rpy.backup` au lieu de `.rpy`, évitant toute confusion avec les fichiers source
- **Impact** : Les fichiers de backup sont clairement identifiables et ne risquent plus d'être confondus avec les fichiers source Ren'Py
- **Fichier modifié** : `core/services/translation/translation_generation_business.py`

---

## 2025-11-25 (v1.2.19.5)

### 🐛 Corrections et améliorations

#### 🧾 Éditeur temps réel – menu de choix lisible
- **Problème résolu** : le conteneur scrollable des menus ne s'adaptait pas à la largeur disponible, coupant les textes VO/VF lorsque plusieurs choix étaient présents
- **Solution** : synchronisation automatique de la largeur du `Canvas` avec le contenu interne pour que les zones VO/VF s'étendent correctement
- **Impact** : les dialogues et traductions des menus restent pleinement visibles, même avec beaucoup de texte
- **Fichier modifié** : `ui/tab_tools/realtime_editor_tab.py`

---
## 2025-11-24 (v1.2.19)

### ✨ Améliorations

#### 🌐 Rapport de cohérence – mémorisation du choix du traducteur
- **Nouveauté** : Le choix du traducteur dans le rapport de cohérence est maintenant mémorisé entre les sessions
- **Détails** :
  - Le traducteur sélectionné (Google, DeepL, Groq AI, Microsoft, Yandex) est automatiquement sauvegardé dans la configuration
  - Au chargement d'un nouveau rapport, le dernier traducteur utilisé est automatiquement sélectionné
  - Le choix est partagé entre tous les rapports de cohérence (même configuration globale que l'éditeur temps réel)
- **Impact** : Plus besoin de re-sélectionner le traducteur à chaque ouverture de rapport, gain de temps et meilleure expérience utilisateur
- **Fichiers modifiés** :
  - `ui/shared/editor_manager_server.py` : Ajout des endpoints API `/api/coherence/translator` (GET/POST)
  - `core/services/reporting/coherence_html_report_generator.py` : Chargement et sauvegarde automatique du choix du traducteur

#### ⚡ Éditeur temps réel – tests de compatibilité module v2
- **Nouveauté** : Les utilisateurs peuvent forcer l'installation du module `v2.rpy` pour tester la compatibilité lorsqu'une version Ren'Py n'est pas encore répertoriée
- **Détails** :
  - Bouton **« Tester module v2 »** ajouté dans l'onglet temps réel pour installer manuellement v2 sans modifier la détection automatique
  - Popups dédiés expliquant la procédure de test et demandant de remonter la version Ren'Py utilisée + résultat afin d'actualiser le tableau de compatibilité
  - Aide intégrée mise à jour (workflow + prérequis) pour documenter cette nouvelle possibilité
  - Le backend accepte un paramètre `force_module_version` afin d'imposer v1 ou v2 lors de la génération du module de surveillance
- **Impact** : Les utilisateurs peuvent valider eux‑mêmes la compatibilité de nouvelles versions Ren'Py et nous transmettre les résultats rapidement
- **Fichiers modifiés** :
  - `ui/tab_tools/realtime_editor_tab.py` : bouton dédié, popups contextualisées et guide mis à jour
  - `core/services/tools/realtime_editor_business.py` : support de l’option `force_module_version` et journalisation des tests

### 🐛 Corrections et améliorations

#### 🎯 Gestionnaire d'exclusions – filtre par projet corrigé
- **Problème résolu** : Le filtre par projet ne se mettait pas à jour correctement lors de la sélection d'un projet
- **Solution** :
  - Correction de la logique de filtrage pour utiliser les clés normalisées de projet au lieu des noms d'affichage
  - Amélioration de la mise à jour du filtre de fichiers selon le projet sélectionné
  - Utilisation d'ensembles (`set`) pour une correspondance plus fiable entre projets et fichiers
- **Impact** : Le filtre par projet fonctionne maintenant correctement et met à jour automatiquement la liste des fichiers disponibles
- **Fichier modifié** : `ui/dialogs/exclusions_manager_dialog.py`

---
## 2025-11-22 (v1.2.18)

### 🐛 Corrections et améliorations

#### 🎨 Générateur de traductions – sauvegarde persistante des choix de police
- **Problème résolu** : Les préférences de police individuelles (checkbox et sélection de police) n'étaient pas sauvegardées de manière persistante entre les sessions
- **Solution** :
  - Ajout du chargement automatique des préférences de police au démarrage de l'interface
  - Ajout de la sauvegarde automatique des préférences de police à la fermeture de la fenêtre
  - Les préférences sont maintenant sauvegardées à chaque modification ET à la fermeture (double sécurité)
- **Impact** : Les choix de police (checkbox activées/désactivées et polices sélectionnées) sont maintenant conservés entre les sessions
- **Fichiers modifiés** : `ui/dialogs/translation_generator_interface.py`

---
## 2025-11-16 (v1.2.17)

### ✨ Améliorations

#### 🧭 Éditeur Temps Réel – menus à nombreux choix (sandbox)
- **Nouveauté** : Conteneur scrollable avec ascenseur vertical pour l’interface des choix
- **Détails** :
  - Canvas + Scrollbar verticale, mise à jour automatique de la zone de scroll
  - Défilement à la molette (Windows/Linux), y compris en fenêtre détachée
  - Boutons “Ouvrir” et “Enregistrer Tous les Choix” toujours accessibles via le défilement
- **Fichier modifié** : `ui/tab_tools/realtime_editor_tab.py`

### 🐛 Corrections et compatibilité

#### 🎯 Module de surveillance temps réel – compat et nettoyage du log
- **Compatibilité** :
  - Ren’Py 7.4.4 → module `v2` (validé: Between Salvation and Abyss)
  - Ren’Py 8.2.3 → module `v2` (v1 incompatible, v2 OK partiel)
  - Fallback amélioré pour versions inconnues: `v2` privilégié pour 7.x et 8.0/8.2
- **Nettoyage du log** :
  - Filtrage des placeholders hérités `{0}|{1}|{2}|{3}|{4}`
  - Déduplication des doublons consécutifs du même dialogue
- **Fichier modifié** : `core/services/tools/realtime_editor_business.py`

#### 📊 Rapport de cohérence – contrôle des pourcentages amélioré
- **Problème résolu** : Les variables Ren'Py `%(lettres)s`, `%(nom)d`, etc. étaient incorrectement signalées comme des erreurs "Pourcentages incohérents"
- **Solution** : Le contrôle ignore désormais les variables Ren'Py valides et ne compte que les pourcentages littéraux isolés (qui doivent être échappés en `%%`)
- **Pattern ignoré** : `%\([a-zA-Z0-9_]+\)[a-zA-Z]` (ex: `%(fa)s`, `%(nom)d`)
- **Impact** : Plus de faux positifs sur les variables Ren'Py dans les dialogues traduits
- **Fichier modifié** : `core/services/tools/coherence_checker_business.py`

#### 🎯 Générateur de traductions – génération simple protégée
- **Problème résolu** : Le bouton "Générer les traductions" générait automatiquement des fichiers supplémentaires (`99_Z_ScreenPreferences.rpy`, `common.rpy`, `screens.rpy`) même si aucune option n'était cochée, écrasant les fichiers existants
- **Solution** :
  - Détection automatique des générations simples (toutes les options à `False`)
  - Génération simple : ignore complètement les options de la config et ne génère QUE les fichiers de traduction
  - Protection backup : si un fichier est écrasé lors d'une génération avec options explicites, un backup avec timestamp est créé automatiquement
- **Impact** : Le bouton "Générer les traductions" ne génère plus que les fichiers `.rpy` de traduction, sans écraser les fichiers de configuration existants
- **Fichier modifié** : `core/services/translation/translation_generation_business.py`

---
## 2025-11-16 (v1.2.16)

### 🐛 Corrections et améliorations

#### 🖼️ Icône application – support multi-plateforme amélioré
- **Problème résolu** : L'icône ne s'affichait pas correctement dans la barre des tâches Windows et sur l'exécutable
- **Solution** :
  - Ajout de `SetCurrentProcessExplicitAppUserModelID()` pour Windows afin que l'icône s'affiche correctement dans la barre des tâches
  - Support amélioré pour Linux/macOS avec `iconphoto()` utilisant PIL/Pillow
  - Inclusion de l'icône dans le bundle PyInstaller via `--add-data` pour Windows et Linux
- **Impact** : L'icône personnalisée s'affiche maintenant correctement dans la fenêtre, la barre des tâches et sur l'exécutable
- **Fichiers modifiés** :
  - `ui/main_window.py` : Support multi-plateforme avec AppUserModelID pour Windows
  - `.github/workflows/build-releases.yml` : Inclusion de l'icône dans les builds PyInstaller

#### 🪟 Masquage des fenêtres de commande sur Windows
- **Problème résolu** : Les fenêtres de commande (cmd.exe) s'affichaient et faisaient clignoter l'écran lors de l'exécution de certaines actions
- **Solution** : Ajout systématique de `subprocess.CREATE_NO_WINDOW` sur tous les appels `subprocess.run()` et `subprocess.Popen()` sur Windows
- **Impact** : Plus de clignotement d'écran, toutes les commandes s'exécutent en arrière-plan de manière silencieuse
- **Fichiers modifiés** :
  - `core/services/tools/cleaning_business.py` : Masquage lors de la génération lint.txt
  - `core/services/translation/translation_generation_business.py` : Masquage pour les générations embedded et SDK
  - `core/tools/python_manager.py` : Masquage pour les tests Python
  - `main.py` : Masquage pour les commandes netstat/taskkill

---
## 2025-11-15 (v1.2.15)

### 🐛 Corrections et améliorations

#### 💾 Système de sauvegarde/restauration – normalisation des chemins
- **Problème résolu** : Après le nettoyage du dossier `tl`, le chemin d'accès était mal enregistré, empêchant la restauration de fonctionner correctement
- **Cause** : Les chemins n'étaient pas normalisés (absolus et normalisés) avant d'être enregistrés dans les métadonnées
- **Solution** : Normalisation systématique des chemins avec `os.path.abspath(os.path.normpath())` lors de la création et de la restauration des sauvegardes
- **Impact** : Les sauvegardes ZIP créées lors du nettoyage peuvent désormais être restaurées correctement, même avec des chemins contenant des espaces ou des caractères spéciaux
- **Fichiers modifiés** :
  - `core/models/backup/unified_backup_manager.py` : Normalisation dans `create_backup()` et `create_zip_backup()`
  - `ui/dialogs/unified_backup_interface.py` : Normalisation dans `restore_selected()`, `_get_zip_source_path_smart()` et `_extract_zip_backup()`

#### 📝 Rapport de cohérence HTML – améliorations du filtrage
- **Problème résolu 1** : Le bloc textarea n'apparaissait pas lors du filtrage par type d'erreur + fichier
- **Problème résolu 2** : Le filtre par fichier affichait tous les fichiers au lieu de seulement ceux contenant des erreurs du type sélectionné
- **Solution** :
  - Correction du sélecteur dans `applyFilters()` pour utiliser `.file-section` au lieu de `[data-file]`
  - Ajout de la fonction `updateFileFilterOptions()` qui met à jour dynamiquement le filtre par fichier selon le type d'erreur sélectionné
  - Ajout de règles CSS pour garantir la visibilité du textarea et de l'interface d'édition
- **Impact** :
  - Le textarea est maintenant toujours visible, même lors du filtrage
  - Le filtre par fichier s'actualise automatiquement et n'affiche que les fichiers pertinents
  - Le bloc d'édition (textarea + boutons) est présent sur tous les types d'erreur
- **Fichier modifié** : `core/services/reporting/coherence_html_report_generator.py`

### 🔄 Compatibilité

#### 🎯 Module de surveillance temps réel – nouvelles validations
- **Ren'Py 7.5.1** : Module `v2` validé sur le jeu "Corrupted Love"
- **Ren'Py 8.0.1** : Module `v2` validé sur le jeu "Motherless"
- **Conséquence** : Sélection automatique du module adéquat pour ces versions sans réglage manuel
- **Fichier modifié** : `core/services/tools/realtime_editor_business.py`

---
## 2025-11-12 (v1.2.14)

### ✨ Améliorations

#### 🕒 Génération TL tolérante
- **Contexte** : certains projets volumineux mettaient plus de deux minutes avant d’écrire un nouveau fichier et la génération se coupait prématurément
- **Action** : relevé du seuil d’inactivité à **10 minutes** (et 5 minutes pour le tout premier fichier) pour laisser le temps aux projets lourds de progresser
- **Impact** : plus de coupure intempestive tant que le répertoire `tl/` continue de recevoir des fichiers, même lentement
- **Fichier modifié** : `core/services/translation/translation_generation_business.py`

### 🐛 Corrections et améliorations

#### 📝 Rapport de cohérence – éditeur inline toujours visible
- **Problème résolu** : la zone de saisie et ses boutons disparaissaient lorsqu’on filtrant par « Tous les fichiers »
- **Solution** : le filtrage affiche désormais l’éditeur pour chaque erreur conservée, quel que soit le filtre actif
- **Impact** : on peut corriger ou coller des traductions sans devoir cibler un fichier particulier
- **Fichier modifié** : `core/services/reporting/coherence_html_report_generator.py`

### 🔄 Compatibilité

#### 🎯 Module de surveillance temps réel
- **Validation** : le module `v2` est désormais certifié sur **Ren’Py 7.6.1** (jeu “Girl Scout Island”)
- **Conséquence** : sélection automatique du module adéquat pour cette version sans réglage manuel
- **Fichier modifié** : `core/services/tools/realtime_editor_business.py`

---

## 2025-11-10 (v1.2.13)

### ✨ Améliorations

#### ⚙️ Fenêtre Paramètres de cohérence
- **Nouveauté** : Ajout de l'option `🔖 Contenu balises non traduit ({b}text{/b})` dans la fenêtre de configuration des vérifications
- **Impact** : Cohérence totale entre l’onglet principal et la fenêtre de paramètres, l’option reste configurable quelle que soit l’interface utilisée
- **Fichier modifié** : `ui/dialogs/settings_interface.py`

#### 🧵 Extraction des lignes narrateur vides
- **Problème résolu** : Les lignes reconstruites utilisant `RENPY_EMPTY_NARRATOR` perdaient le texte après reconstruction
- **Solution** : Harmonisation de l’extraction pour traiter `RENPY_NARRATOR` et `RENPY_EMPTY_NARRATOR` de la même manière
- **Impact** : Les narrations reconstruites conservent correctement leur contenu même lorsqu’elles étaient vides lors de l’extraction
- **Fichier modifié** : `core/services/extraction/extraction.py`

---

## 2025-11-10 (v1.2.12)

### 🐛 Corrections et améliorations

#### 📂 Gestionnaire d'exclusions cohérent
- **Problème résolu** : Le gestionnaire d'exclusions affichait le dossier parent (`capis`) au lieu du vrai projet (`AHA-pc`)
- **Solution** : Normalisation des chemins pour remonter jusqu'à la racine Ren'Py (segment `game`) et afficher le nom du projet
- **Impact** : L'interface reflète correctement le projet, quel que soit l'outil ayant créé l'exclusion
- **Fichier modifié** : `ui/dialogs/exclusions_manager_dialog.py`

---

## 2025-11-08 (v1.2.11)

### 🐛 Corrections et améliorations

#### 🔍 Détection des langues dans l'onglet cohérence
- **Problème résolu** : L'onglet de cohérence ne détectait pas tous les dossiers de langue comme les autres fenêtres
- **Solution** : Ajout du paramètre `force_refresh=True` lors de l'initialisation et lors des changements de projet
- **Impact** : Toutes les langues disponibles sont maintenant correctement détectées dans l'onglet de cohérence
- **Fichiers modifiés** : 
  - `ui/shared/project_widgets.py` : Ajout paramètre `force_refresh` à `_validate_and_set_project()` et méthode `refresh_languages()`
  - `ui/tab_tools/coherence_tab.py` : Utilisation de `force_refresh=True` lors de l'initialisation
  - `ui/dialogs/maintenance_tools_interface.py` : Utilisation de `force_refresh=True` lors des changements de projet

#### ⏱️ Timeout adaptatif pour la génération de traductions
- **Problème résolu** : Le système arrêtait la génération après 2 minutes même si elle progressait encore
- **Solution** : Implémentation d'un système de timeout adaptatif basé sur l'activité réelle
- **Fonctionnement** :
  - **Timeout initial** : 1 minute avant le premier fichier généré (détection problème de démarrage)
  - **Timeout d'inactivité** : 2 minutes sans nouveau fichier une fois qu'au moins un fichier a été généré
  - **Détection de progression** : Réinitialisation automatique du timer à chaque nouveau fichier détecté
- **Impact** : Les projets volumineux peuvent maintenant prendre 5-10 minutes sans être interrompus, tant que des fichiers continuent d'être générés régulièrement
- **Fichier modifié** : `core/services/translation/translation_generation_business.py`

#### 🌐 Rapport de cohérence servi en HTTPS local
- **Problème résolu** : Le bouton “Coller” du rapport HTML n'avait pas accès au presse-papiers quand le rapport était ouvert en `file://`
- **Solution** : Ajout d'un endpoint `http://localhost:8765/coherence/report` pour servir le rapport via le serveur intégré
- **Impact** :
  - Accès au presse-papiers autorisé dans Firefox/Chrome
  - Le bouton `📋 Coller` fonctionne sans mode manuel
  - Compatibilité WSL assurée (serveur binding `0.0.0.0`)
- **Fichiers modifiés** :
  - `ui/shared/editor_manager_server.py` : nouvelle route HTTP et sécurisation lecture fichier
  - `core/services/tools/coherence_checker_business.py` : ouverture auto via l'URL locale avec fallback
  - `core/services/reporting/coherence_html_report_generator.py` : normalisation host côté client

#### 🔧 Correction syntaxe Ren'Py
- **Correction** : Erreur de syntaxe dans l'appel à `scr_prf_btn()` pour la sélection de langue
- **Changement** : `use scr_prf_btn('English', action Language(None))` → `use scr_prf_btn('normal', 'English', Language(None))`
- **Fichier modifié** : `Z_Ne_Pas_supprimer/essai.rpy`

#### 🧩 Module de surveillance Ren'Py v2 fiable
- **Problème résolu** : L'installation du module v2 échouait avec l'erreur `Replacement index 0 out of range for positional args tuple`
- **Cause** : Le template `v2.rpy` contient des `.format()` internes qui entraient en conflit avec la génération dynamique
- **Solution** : Remplacement direct du placeholder `{language}` sans utiliser `str.format`
- **Validation** : Testé et validé sur Ren'Py 7.3.5 (dialogues et menus sans récursion)
- **Fichiers modifiés** :
  - `core/services/tools/realtime_editor_business.py`
  - `core/services/tools/renpy_modules/v2.rpy`

### 📊 Impact
- **Détection langues** : Cohérence entre tous les onglets de l'application
- **Génération fiable** : Plus d'interruptions prématurées pour les projets volumineux
- **Code propre** : Syntaxe Ren'Py correcte et maintenable

---

## 2025-11-03 (v1.2.10)

### 🛡️ Surveillance traceback.txt étendue
- **Détection erreurs Ren'Py** : Surveillance automatique de `traceback.txt` lors de la génération des traductions
- **Génération embedded** : Surveillance en temps réel (vérification toutes les 500ms) avec arrêt immédiat si erreur détectée
- **Génération SDK** : Même protection pour les générations via SDK Ren'Py
- **Messages clairs** : Erreurs Ren'Py clairement identifiées comme provenant du jeu, pas de RenExtract
- **Prévention** : Suppression automatique de `traceback.txt` existant avant génération pour éviter les faux positifs
- **Plus d'échecs silencieux** : Les erreurs Ren'Py sont maintenant détectées et signalées immédiatement

### 🐛 Correction sauvegarde rapport cohérence
- **Guillemets échappés** : Correction du pattern regex pour gérer les guillemets échappés `\"` dans les dialogues
- **Texte après guillemets** : Support du texte après le guillemet fermant (ex: `"dialogue" with speechfade.`)
- **Échappement automatique** : Les guillemets dans le nouveau contenu sont automatiquement échappés lors de la sauvegarde
- **Pattern robuste** : Utilisation de `(?:\\.|[^\"])*` pour capturer correctement le contenu entre guillemets même avec échappements

### 📊 Impact
- **Détection proactive** : Erreurs Ren'Py identifiées avant la fin de la génération
- **Diagnostic amélioré** : Messages d'erreur explicites pointant vers `traceback.txt` pour le diagnostic
- **Protection utilisateur** : Plus de confusion entre erreurs RenExtract et erreurs Ren'Py
- **Sauvegarde fiable** : Les modifications dans le rapport de cohérence fonctionnent désormais avec tous les formats de dialogues Ren'Py

---

## 2025-10-29 (v1.2.9)

### 🐛 Correctifs critiques rapport HTML
- **Sections collapsibles bloquées** : Correction apostrophes françaises non échappées (`l'éditeur`, `l'enregistrement`, `l'accès`)
- **Bouton Copier défaillant** : Correction échappement guillemets doubles dans attributs HTML `onclick="..."`
- **Bouton Coller → Traduire** : Correction sélecteur trop générique transformant "Coller" en "Traduire" après traduction Groq
- **JavaScript robuste** : Entités HTML `&quot;` pour guillemets dans template literals (onclick)
- **0 erreur JavaScript** : Tous les rapports de cohérence fonctionnent parfaitement

### 🎨 Amélioration contrôle balises non traduites
- **Surlignage visuel** : Contenu non traduit dans balises Ren'Py surligné en jaune/orange
- **Pattern avancé** : Détection `{tag}contenu{/tag}` avec mise en évidence du contenu uniquement
- **Cohérence visuelle** : Même style que variables `[...]` et balises `{...}` existantes
- **Priorité affichage** : `TAG_CONTENT_UNTRANSLATED` positionné après `TAG_MISMATCH`

### 📊 Impact
- **100% fonctionnel** : Rapports HTML sans erreurs JavaScript
- **UX améliorée** : Identification instantanée des zones problématiques
- **0 faux négatif** : Sections collapsibles et copie toujours opérationnelles

---

## 2025-10-29 (v1.2.8)

### 🔄 Système de contrôle des guillemets unifié
- **1 seul contrôle** pour tous les types de guillemets (vs 3 contrôles redondants)
- Support de **10 formats** : droits `"`, échappés `\"`, simples `'`, français `« »`, typographiques `" "`, apostrophes `'`, chevrons `<< >>`
- **Substitutions intelligentes** acceptées : `'simple'` → `\"échappé\"` / `"double"` / `« français »` / `"typographique"`
- **Ignore les élisions françaises** : `l'`, `d'`, `c'`, `n'`, etc.
- Compte le **nombre total** de guillemets (permet transformations de style)
- **Plus de faux positifs** sur substitutions valides
- Code **3× plus propre** et maintenable

### 🎨 Amélioration visuelle des boutons de navigation
- **Nouveau système sans `disabled`** : état "inactif" bien plus visible
- **Bouton actif** : Fond vert, texte noir gras, bordure épaisse, curseur main
- **Bouton inactif** : Fond **gris foncé `#4a4a4a`**, texte **blanc**, relief plat, curseur normal
- Messages dynamiques : "◀️ Précédent (3)" / "⏹ Premier fichier" / "▶️ Suivant (5)" / "⏹ Dernier fichier"
- **Contraste élevé** pour état désactivé (plus de confusion possible)

### 🧹 Nettoyage et optimisations
- Suppression fonction obsolète `_is_excluded_by_content()` (code mort)
- Suppression vérifications redondantes dans `_is_untranslated_line()`
- **Système d'exclusion 100% précis** : projet + fichier + ligne + texte
- Commentaires explicites pour tous les types de guillemets
- Documentation enrichie des fonctions de cohérence

### 🔧 Améliorations du workflow Discord
- **Section "Points Clés"** : résumé automatique des 3 principales catégories
- **Présentation enrichie** : description mise à jour, footer avec icône
- **Liens utiles** : ajout du lien "Signaler un Bug" vers GitHub Issues
- **Affichage optimisé** : changelog complet + résumé rapide
- Message de remerciement dans le footer

---

## 2025-10-28 (v1.2.7)

### 🛡️ Améliorations anti-détection antivirus (Version 1)
- **Métadonnées enrichies** : `version_info.txt` avec auteur, copyright, licence, site web
- **Manifest Windows** : `manifest.xml` pour compatibilité Windows 7-11 et déclaration privilèges
- **PyInstaller optimisé** : `--noupx` (désactive UPX), `--log-level=WARN`, imports explicites (`groq`, `tkinter`, `tkinterdnd2`, `PIL`, `requests`)
- **Génération hash automatique** : SHA256 + MD5 dans `virustotal_info.txt` pour vérification
- **Script mise à jour version** : `update_version_info.py` (MAJ automatique numéro de version)
- **Script vérification** : `verify_setup.py` (validation configuration anti-détection)
- **Workflow GitHub Actions** : Intégration complète des optimisations dans CI/CD

### 📊 Impact
- Réduction attendue : **5-10 détections AV → 2-3 détections AV** (~70% de réduction)
- Résultat réel VirusTotal : **3/72 détections** (objectif atteint ✅)

---

## 2025-10-27 (v1.2.6)

### 🐛 Corrections
- **Fix critique** : Erreur f-string avec backslash dans `coherence_html_report_generator.py`
- Correction échappement des caractères spéciaux dans les rapports HTML

---

## 2025-10-27 (v1.2.5)

### 📝 Édition cohérence en ligne
- Modification directe depuis le rapport HTML
- Pré-remplissage intelligent avec valeur NOUVEAU
- Surlignage visuel des éléments problématiques
- Boutons copie (ANCIEN/NOUVEAU)
- Boutons toggle d'exclusion (❌ Ignorer / ✅ Inclure)
- Traduction assistée (Groq AI, DeepL, Google, Microsoft, Yandex)
- Validation syntaxique Ren'Py automatique
- Backup automatique avant modification
- Détection intelligente de chemins et langue
- Messages globaux dans header du rapport

### 🔧 Configuration des éditeurs
- Détection automatique Windows 10/11 (registre UserChoice)
- Extraction dynamique des chemins d'installation
- Test de l'éditeur (bouton 🧪, fichier test ligne 7)
- Support VSCode, Sublime Text, Notepad++, Atom, Pulsar
- Persistance éditeur personnalisé

### 🛡️ Contrôles de cohérence
- Contrôle de longueur unifié (seuil 250%, minimum 10 caractères)
- Guillemets intelligents (ignore apostrophes françaises)
- Support guillemets calligraphiés (" " ' ')
- Terminologie française (ANCIEN/NOUVEAU)
- Interface optimisée (grille 4×3)
- 12 types de vérifications configurables

### 🔑 Test et validation API
- Test clé API Groq avec bouton 🔍
- Notifications toast pour résultats
- Thread séparé non-bloquant

### 📦 Optimisation exécutable
- Suppression Pillow (réduction 25 MB → 16 MB Windows / 18 MB Linux)
- Installation temporaire polices sans dépendance lourde
- Gestion intelligente des polices

---

## 2025-10-20 (v1.2.0)

### 🔍 Rapport de cohérence interactif
- Exclusions interactives avec checkboxes cliquables
- Serveur HTTP local (communication temps réel, port dynamique 8000-8099)
- Persistence dans config.json (par projet/fichier/ligne)
- Feedback visuel avec animations (fade-out, ☐ → ✓)
- Labels cliquables ("Cliquer pour ignorer" / "✓ Ignoré")
- Cache JavaScript pour performances
- Support WSL (binding 0.0.0.0)

### 🗂️ Gestionnaire d'exclusions
- Interface modale Tkinter thématisée
- Treeview multi-colonnes avec tri (Projet | Fichier | Ligne | Texte | Date)
- Sélection multiple (checkboxes par ligne + header global)
- Double filtrage cascadé (projet + fichier)
- Filtre intelligent dynamique
- Suppression batch avec feedback progressif

### 🎨 Améliorations UX
- Flèches animées sections collapsibles (rotation ↓ → ↑)
- Reset global filtres + fermeture sections
- Stats dynamiques avec compteurs
- Support WSL/Windows

### 📖 Tutoriel
- Tab 03 validée (ton formel)
- Images téléchargées depuis GitHub (au lieu d'embarquées)
- Build optimisé (-tutorial_images)

---

## 2025-10-15 (v1.1.0)

### 🎯 Groq AI Contextualisé
- Définition de personnages (genre, nom) pour traductions précises
- Profils de prompts (sauvegarde/rechargement configurations)
- Scanner de personnages (détection `Character()` dans .rpy)
- Contexte conversationnel (dialogue précédent envoyé à l'IA)
- Interface collapsible (sections pliables)

### 🛠️ Module Ren'Py Multi-versions
- Système modulaire (support 8.1.2, 8.2.1+)
- Détection automatique version projet
- Protection robuste (conflits de noms, récursion)
- Installation simplifiée (module .rpy prêt à l'emploi)

### 💾 Gestionnaire de Sauvegardes Amélioré
- Sauvegarde ZIP complète (dossiers entiers + métadonnées)
- Restauration intelligente (emplacement origine/choisi)
- Suppression par lot (sélection multiple checkboxes)
- Nettoyage automatique (dossiers vides)
- Types de sauvegardes (combinaison, édition, nettoyage)

### 🚀 Navigation & Interface
- Navigation rapide (boutons Précédent/Suivant)
- Compteurs de fichiers (passés/restants)
- Synchronisation bidirectionnelle entre fenêtres
- Chargement automatique premier fichier

### 🧹 Nettoyage de Code
- Suppression ~320 lignes code obsolète
- Unification modes (Simple/Optimisé)
- Documentation mise à jour

---

## 2025-10-10 (v1.0.0)

### 🎮 Version Initiale - Production Ready

#### Architecture MVP
- 114 fichiers Python organisés
- 24 packages avec système de santé
- Logs intelligents et cache persistant
- Interface moderne avec tutoriel intégré

#### Fonctionnalités Principales
- Extraction intelligente dialogues depuis .rpy
- Génération fichiers traduction Ren'Py
- Reconstruction intelligente fichiers traduits
- Décompilation .rpa et .rpyc
- Screen preferences personnalisables
- Système sauvegarde hiérarchique
- Vérification cohérence avec rapports HTML

#### Structure
- `core/models/` : État et données (backup, files, cache)
- `core/services/` : Logique métier (extraction, translation, reporting, tools)
- `infrastructure/` : Services d'infrastructure (config, logging, helpers)
- `ui/dialogs/` : Interfaces modales
- `ui/tab_*/` : Onglets de l'interface

#### Production
- Workflow CI/CD automatisé (Windows + Linux)
- Documentation complète
- 0 warning parasite
- Cache persistant multi-session
