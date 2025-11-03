# 📝 CHANGELOG - RenExtract

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
