# 🎮 RenExtract

[![Build & Release](https://github.com/Rory-Mercury-91/RenExtract/actions/workflows/build-releases.yml/badge.svg)](https://github.com/Rory-Mercury-91/RenExtract/actions/workflows/build-releases.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

**Outil professionnel d'extraction, préparation et reconstruction de traductions pour Ren'Py**

RenExtract est un outil complet qui simplifie l'extraction de textes et la génération de fichiers de traduction pour les jeux Ren'Py. Il **prépare** vos fichiers pour la traduction (extraction intelligente), puis **reconstruit** les fichiers traduits dans le format Ren'Py. La traduction elle-même se fait avec vos outils préférés (DeepL, ChatGPT, Google Translate, etc.). Avec une architecture MVP professionnelle et un système de monitoring intelligent, RenExtract offre une solution robuste et extensible pour tous vos besoins de localisation.

---

## ✨ Fonctionnalités Principales

### 🎯 Extraction & Génération
- **📄 Extraction intelligente** des dialogues depuis fichiers `.rpy`
- **🔧 Génération de fichiers de traduction** Ren'Py (pas besoin du SDK !)
- **🛡️ Protection automatique** des codes spéciaux et variables
- **🔄 Reconstruction intelligente** des fichiers traduits au format Ren'Py
- **📦 Décompilation** des archives `.rpa` et scripts `.rpyc`

### 🌍 Personnalisation Avancée (Optionnel)
- **🔧 Générateur screen preferences** pour jeux avec structure standard
  - 🎛️ Contrôle taille de police dynamique
  - 🎨 Textbox personnalisé (opacité, offset, contour)
  - 🌐 Sélecteur de langue intégré au jeu
  - 🎯 Détection automatique du style Ren'Py (`label`/`text`/`textbutton`)
- **✅ Validation stricte** : fonctionne uniquement sur `screens.rpy` standard

### 🔧 Outils de Maintenance
- **🧹 Nettoyage intelligent** des fichiers et traductions
- **📊 Vérification de cohérence** avec rapports HTML détaillés
- **💾 Système de sauvegarde hiérarchique** :
  - `SECURITY` : Avant opérations critiques
  - `CLEANUP` : Avant nettoyage
  - `RPA_BUILD` : Avant compilation
  - `REALTIME_EDIT` : Sauvegarde automatique (rotation 10 max)
- **📈 Rapports de génération** professionnels

### 🎨 Interface Moderne
- **🖼️ Interface graphique intuitive** avec Tkinter
- **🌙 Thèmes personnalisables** (sombre/clair)
- **📖 Tutoriel intégré** interactif multi-langues
- **⚡ Drag & Drop** et copier-coller
- **🔄 Édition temps réel** avec serveur HTTP intégré
- **📊 Statistiques live** et compteurs de performance

### 🏗️ Architecture Professionnelle
- **MVP 10/10** : Séparation claire Models-Views-Presenters
- **Système de santé** : Monitoring automatique de 24 packages
- **Logs intelligents** : 1 ligne si tout va bien, détails si problème
- **Cache persistant** : Performance optimale multi-session
- **Modular & Extensible** : Architecture orientée services

---

## 📥 Installation

### 💻 Téléchargement Direct (Recommandé)

Téléchargez la dernière version depuis les [**Releases**](https://github.com/Rory-Mercury-91/RenExtract/releases) :

- 🪟 **Windows** : `RenExtract-vX.X.X-Windows.zip`
- 🐧 **Linux** : `RenExtract-vX.X.X-Linux.tar.gz`

### 🚀 Installation Windows

```bash
# 1. Téléchargez le fichier .zip
# 2. Extrayez l'archive
# 3. Double-cliquez sur RenExtract.exe
```

### 🐧 Installation Linux

```bash
# Télécharger et extraire
tar -xzf RenExtract-vX.X.X-Linux.tar.gz

# Rendre exécutable
chmod +x RenExtract

# Lancer
./RenExtract
```

### 🐍 Installation depuis le Code Source

```bash
# Cloner le repository
git clone https://github.com/Rory-Mercury-91/RenExtract.git
cd RenExtract

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python main.py
```

---

## 🎯 Utilisation Rapide

### Workflow Standard

> **💡 Important** : RenExtract **ne traduit pas automatiquement** ! Il extrait les dialogues, vous les traduisez avec vos outils préférés, puis RenExtract reconstruit les fichiers Ren'Py traduits.

#### 🎬 Partir d'un Jeu Vierge

1. **Chargez** votre projet Ren'Py dans l'interface principale :
   - Drag & Drop du dossier `game/`
   - Bouton "📁 Ouvrir Dossier"
   - Sélectionnez la racine du projet

2. **Ouvrez** l'interface du générateur de traductions :
   - Cliquez sur "🎮 Générateur" dans l'interface principale

3. **Décompressez** les archives Ren'Py (si nécessaire) :
   - Décompression des `.rpa` (archives de ressources)
   - Décompilation des `.rpyc` (scripts compilés)
   - ⚠️ Les fichiers `.rpy` doivent être visibles dans `game/`

4. **Générez** la structure de fichiers de traduction Ren'Py :
   - Cliquez sur "🔧 Générer les traductions"
   - **RenExtract crée automatiquement** la structure de fichiers `.rpy` vides dans `tl/[langue]/`
   - Sélectionnez les options désirées (langue, screen preferences optionnel...)
   - Pas besoin du SDK Ren'Py !

5. **Naviguez** vers le fichier à traduire :
   - Dans l'interface principale, utilisez les boutons de navigation
   - Sélectionnez le fichier `.rpy` souhaité

6. **Extrayez** les dialogues :
   - Cliquez sur **"⚡Extraire"**
   - Les fichiers `.txt` sont créés dans `01_Temporaires/[NomDuJeu]/`

7. **Traduisez** les fichiers `.txt` générés :
   - Ouvrez les fichiers `*_dialogue.txt` avec votre éditeur
   - Utilisez vos outils de traduction préférés :
     - 🤖 **DeepL, ChatGPT, Google Translate** (traduction automatique)
     - ✍️ **Traduction manuelle** (pour plus de qualité)
     - 🔄 **Combinaison** des deux approches
   - Sauvegardez les fichiers traduits

8. **Reconstruisez** le fichier traduit :
   - Cliquez sur **"🔧 Reconstruire"**
   - Le fichier `.rpy` traduit est créé dans `tl/[langue]/`

9. **Vérifiez** la cohérence (si nécessaire) :
   - Cliquez sur **"🔄 Revérifier"**
   - Consultez le rapport HTML dans `03_Rapports/`
   - Corrigez les problèmes détectés

10. **Testez** dans votre jeu Ren'Py :
    - Lancez votre jeu
    - Changez de langue dans les préférences
    - C'est parti ! 🎉

> **💡 Note** : RenExtract intègre son propre **générateur de fichiers de traduction Ren'Py**, vous n'avez pas besoin du SDK Ren'Py !

### Pourquoi cette Approche ?

RenExtract adopte une philosophie **"Prépare → Traduis → Reconstruit"** :

✅ **Flexibilité totale** : Utilisez vos outils de traduction préférés  
✅ **Qualité contrôlée** : Vous gardez le contrôle sur la traduction  
✅ **Protection des codes** : Les variables et codes spéciaux Ren'Py sont automatiquement protégés  
✅ **Contrôle de cohérence** : Vérification automatique des balises cassées et erreurs de format  
✅ **Format simple** : Fichiers `.txt` faciles à traduire, manipuler ou partager  
✅ **Intégration IA** : Compatible avec DeepL, ChatGPT, Claude, etc.  

> 🔮 **Futur** : Une traduction automatique intégrée est envisagée, mais la flexibilité actuelle reste prioritaire !

### Options Avancées

#### Générateur Screen Preferences

Accédez aux options avancées via **⚙️ Options Avancées** :

- ✅ **Sélecteur de langue** : Bouton toggle dans les préférences
- ✅ **Contrôle taille de police** : Slider dynamique
- ✅ **Opacité textbox** : Transparence personnalisable
- ✅ **Décalage vertical** : Ajustement position textbox
- ✅ **Contour texte** : Amélioration lisibilité

Le système détecte automatiquement le style de votre `screens.rpy` et génère un code cohérent !

---

## 📚 Structure du Projet

### Architecture MVP 10/10

```
RenExtract/
├── main.py                           # Point d'entrée
├── infrastructure/                   # Services d'infrastructure
│   ├── config/
│   │   ├── config.py                # Configuration globale
│   │   └── constants.py             # Constantes et thèmes
│   ├── i18n/                        # Internationalisation
│   ├── logging/                     # Système de logs
│   └── helpers/                     # Fonctions utilitaires
├── core/                            # Logique métier
│   ├── models/                      # État & Données
│   │   ├── backup/                  # Modèle sauvegarde
│   │   ├── files/                   # Modèle fichiers
│   │   └── cache/                   # Modèle cache
│   ├── services/                    # Services métier
│   │   ├── extraction/              # Extraction textes
│   │   ├── translation/             # Génération traductions
│   │   ├── reporting/               # Rapports HTML
│   │   ├── tools/                   # Outils maintenance
│   │   └── common/                  # Services communs
│   ├── tools/                       # Gestionnaires externes
│   └── app_controller.py            # Contrôleur principal
├── ui/                              # Interface graphique
│   ├── dialogs/                     # Fenêtres modales
│   ├── shared/                      # Composants partagés
│   ├── tab_generator/               # Onglet génération
│   ├── tab_settings/                # Onglet paramètres
│   ├── tab_tools/                   # Onglet outils
│   ├── widgets/                     # Composants custom
│   ├── tutorial/                    # Tutoriel interactif
│   └── main_window.py               # Fenêtre principale
├── 04_Configs/                      # Configuration utilisateur
├── tutorial_images/                 # Images du tutoriel
└── requirements.txt                 # Dépendances Python
```

### Dossiers de Travail

```
01_Temporaires/                     # 📁 Fichiers temporaires d'extraction
└── <game_name>/
    ├── <file_name>/
    │   ├── fichiers_a_traduire/
    │   │   ├── <file_name>_dialogue.txt           # Dialogues extraits
    │   │   └── <file_name>_doublons.txt          # Textes en double
    │   └── fichiers_a_ne_pas_traduire/
    │       ├── <file_name>_positions.json         # Positions originales
    │       ├── <file_name>_with_placeholders.rpy  # Script avec placeholders
    │       ├── <file_name>_invisible_mapping.txt  # Mapping codes invisibles
    │       └── <file_name>_empty.txt              # Lignes vides
    └── translation_progress/
        └── <langue>.json                           # Progression traduction

02_Sauvegardes/                     # 💾 Sauvegardes automatiques
└── <game_name>/
    └── <file_name>/
        ├── security/                               # Avant opérations critiques
        │   └── <file_name>_YYYYMMDD_HHMMSS.rpy
        ├── cleanup/                                # Avant nettoyage
        │   └── <file_name>_YYYYMMDD_HHMMSS.rpy
        ├── rpa_build/                              # Avant compilation
        │   └── <file_name>_YYYYMMDD_HHMMSS.rpy
        └── realtime_edit/                          # Édition temps réel (rotation 10 max)
            └── <file_name>_YYYYMMDD_HHMMSS.rpy

03_Rapports/                        # 📊 Rapports HTML interactifs
└── <game_name>/
    ├── coherence/
    │   └── <game_name>_coherence_interactif_YYYYMMDD_HHMMSS.html
    └── nettoyage/
        └── <game_name>_nettoyage_interactif_YYYYMMDD_HHMMSS.html

04_Configs/                         # ⚙️ Configuration et cache
├── config.json                                     # Configuration utilisateur
├── renextract_log_YYYY-MM-DD__HH-MM-SS.html       # Logs session
├── project_scan_cache.pkl                          # Cache projets (persistant)
├── backup_cache.pkl                                # Cache sauvegardes (persistant)
├── windows_state.json                              # État fenêtres (backup interface)
└── tutorial_shown.flag                             # Tutoriel déjà vu
```

---

## 🏗️ Architecture Technique

### Système de Santé Intelligent

RenExtract intègre un système de monitoring automatique qui surveille **24 packages** en temps réel :

- **100% de santé** : Log simplifié (1 ligne)
  ```
  ✅ Système opérationnel : 3/3 packages OK
  ```

- **< 100% de santé** : Logs détaillés avec modules problématiques
  ```
  🟢 Package Extraction Services santé excellente: 85% (5/6 modules)
  ❌ Modules non chargés: legacy_parser
  ⚠️  Système partiellement opérationnel : 2/3 packages OK
  ```

### Cache Persistant

- **Cache mémoire** pour les sauvegardes (chargement instantané)
- **Cache granulaire** pour les scans de projet (invalidation intelligente)
- **Persistance multi-session** (survit aux redémarrages)
- **Réinitialisation propre** via interface paramètres

### Système de Sauvegarde

- **Hiérarchie intelligente** : `Game/File/Type/Backups`
- **Types multiples** : SECURITY, CLEANUP, RPA_BUILD, REALTIME_EDIT
- **Rotation automatique** pour REALTIME_EDIT (max 5)
- **Métadonnées JSON** : timestamp, taille, hash, description
- **Interface dédiée** avec restauration en un clic

---

## 🔧 Configuration Requise

### Minimale
- **OS** : Windows 10+ (64-bit) ou Linux (GTK3+)
- **Python** : 3.11+ (si exécution depuis source)
- **RAM** : 4 GB
- **Disque** : ~100 MB d'espace libre

### Recommandée
- **OS** : Windows 11 ou Linux moderne
- **RAM** : 8 GB
- **Disque** : ~500 MB (pour projets volumineux)

### Dépendances Python

```txt
tkinterdnd2>=0.3.0      # Support Drag & Drop
requests>=2.0           # Téléchargements
pyinstaller>=5.0        # Compilation (dev)
```

---

## 🛠️ Développement

### Cloner et Configurer

```bash
# Cloner le repository
git clone https://github.com/Rory-Mercury-91/RenExtract.git
cd RenExtract

# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer en mode développement
python main.py
```

### Compiler l'Exécutable

```bash
# Avec le script de compilation (Linux + Wine)
python create_windows_exe.py

# Avec PyInstaller directement (Windows)
pyinstaller --onefile --windowed \
  --name "RenExtract" \
  --icon icone.ico \
  --add-data "core;core" \
  --add-data "infrastructure;infrastructure" \
  --add-data "ui;ui" \
  main.py
```

### Contribuer

1. **Fork** le projet
2. **Créer** une branche feature :
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commiter** vos changements :
   ```bash
   git commit -m 'Add: AmazingFeature'
   ```
4. **Pousser** vers la branche :
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Ouvrir** une Pull Request

---

## 🐛 Résolution de Problèmes

### Problèmes Courants

#### ❌ Fichier screens.rpy non trouvé
**Solution** : Le fichier `screens.rpy` doit exister dans `game/` ou ses sous-dossiers (hors `tl/`)

#### ❌ Validation screen preferences échouée
**Solution** : Vérifiez que `screen preferences():` existe au début d'une ligne dans `screens.rpy`

#### ❌ Fichiers .rpa détectés
**Solution** : Décompilez d'abord les archives `.rpa` avec un outil comme `unrpa` ou `rpatool`

#### ❌ Application lente au démarrage
**Solution** : Le cache se construit au premier lancement, ensuite c'est instantané

### Diagnostic

- **Logs détaillés** : `04_Configs/renextract_log_[date].html`
- **Mode debug** : Activez dans Paramètres > Mode debug
- **Réinitialisation** : Paramètres > Réinitialiser l'application

---

## 📊 Statistiques du Projet

- **114 fichiers** Python (core, ui, infrastructure)
- **24 packages** surveillés avec système de santé
- **Architecture MVP** 10/10
- **Cache persistant** multi-session
- **0 warning** parasite dans les logs
- **100% production-ready**

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🤝 Support & Contact

- **Issues** : [GitHub Issues](https://github.com/Rory-Mercury-91/RenExtract/issues)
- **Discussions** : [GitHub Discussions](https://github.com/Rory-Mercury-91/RenExtract/discussions)
- **Releases** : [GitHub Releases](https://github.com/Rory-Mercury-91/RenExtract/releases)

---

## ⭐ Remerciements

Merci à tous ceux qui utilisent et contribuent à **RenExtract** !

Si ce projet vous aide, n'hésitez pas à lui donner une ⭐ sur GitHub !

---

<div align="center">

**[⬇️ Télécharger la dernière version](https://github.com/Rory-Mercury-91/RenExtract/releases)**

_Fait avec ❤️ pour la communauté Ren'Py_

</div>

