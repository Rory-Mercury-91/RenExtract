# 📝 CHANGELOG - RenExtract

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
