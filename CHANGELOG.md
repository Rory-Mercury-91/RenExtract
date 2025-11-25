# 📝 CHANGELOG - RenExtract

## 2025-11-25 (v1.2.19.5)

### 🐛 Corrections et améliorations

#### 🧾 Éditeur temps réel – menu de choix lisible
- **Problème résolu** : le conteneur scrollable des menus ne s’adaptait pas à la largeur disponible, coupant les textes VO/VF lorsque plusieurs choix étaient présents
- **Solution** : synchronisation automatique de la largeur du `Canvas` avec le contenu interne pour que les zones VO/VF s’étendent correctement
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
