#!/usr/bin/env python3
"""
Script pour créer un .exe Windows depuis Linux avec Wine
RenExtract - Version simplifiée avec versioning automatique
"""

import os
import subprocess
import sys
import shutil
from datetime import datetime

# ---------------------------
# Versioning automatique
# ---------------------------

def get_build_number_file():
    """Retourne le chemin du fichier build_number.txt"""
    return "build_number.txt"

def read_current_build_number():
    """Lit le build number actuel"""
    build_file = get_build_number_file()
    if os.path.exists(build_file):
        try:
            with open(build_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content.isdigit():
                    return int(content)
        except Exception:
            pass
    return 0

def increment_and_save_build_number():
    """Incrémente et sauvegarde le nouveau build number"""
    # Pas besoin de créer de dossier, fichier à la racine
    
    # Lit le build number actuel
    current_build = read_current_build_number()
    new_build = current_build + 1
    
    # Sauvegarde
    build_file = get_build_number_file()
    try:
        with open(build_file, "w", encoding="utf-8") as f:
            f.write(str(new_build))
        print(f"🔢 Build number: {current_build} -> {new_build}")
        return new_build
    except Exception as e:
        print(f"⚠️ Erreur sauvegarde build number: {e}")
        return current_build + 1

def generate_version():
    """Génère une nouvelle version avec build number incrémenté"""
    build_number = increment_and_save_build_number()
    now = datetime.now()
    version = f"RenExtract {now.year}.{now.month:02d}.{now.day:02d}.v{build_number}"
    print(f"🏷️ Nouvelle version générée: {version}")
    return version

def fix_version_in_constants(version):
    """Modifie le fichier constants.py pour fixer la version"""
    constants_path = "infrastructure/config/constants.py"
    backup_path = "infrastructure/config/constants.py.backup"
    
    print(f"🔧 Fixation de la version dans constants.py: {version}")
    
    # Sauvegarde du fichier original
    if os.path.exists(constants_path):
        shutil.copy2(constants_path, backup_path)
        print(f"💾 Sauvegarde créée: {backup_path}")
    
    try:
        with open(constants_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Remplace la ligne VERSION
        lines = content.splitlines()
        new_lines = []
        
        for line in lines:
            stripped = line.strip()
            if (stripped.startswith("VERSION = get_version()") or 
                stripped.startswith("VERSION=get_version()")):
                # Remplace par une version fixe
                indent = len(line) - len(line.lstrip())
                new_line = " " * indent + f'VERSION = "{version}"'
                new_lines.append(new_line)
                print(f"📝 Ligne modifiée: {stripped} -> {new_line.strip()}")
            else:
                new_lines.append(line)
        
        # Écrit le fichier modifié
        with open(constants_path, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines))
        
        print("✅ Version fixée dans constants.py")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la fixation de la version: {e}")
        # Restaure la sauvegarde en cas d'erreur
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, constants_path)
            print("🔄 Fichier restauré depuis la sauvegarde")
        return False

def restore_constants_backup():
    """Restaure le fichier constants.py depuis la sauvegarde"""
    constants_path = "infrastructure/config/constants.py"
    backup_path = "infrastructure/config/constants.py.backup"
    
    if os.path.exists(backup_path):
        try:
            shutil.copy2(backup_path, constants_path)
            os.remove(backup_path)
            print("🔄 Fichier constants.py restauré")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la restauration: {e}")
    return False

# ---------------------------
# Utilitaires d'exécution
# ---------------------------

def run(cmd, quiet=False):
    """Exécute une commande et retourne le résultat"""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return (result.returncode == 0, result.stdout, result.stderr)

def short_tail(text, lines=40):
    """Retourne les dernières lignes d'un texte"""
    if not text:
        return ""
    parts = text.strip().splitlines()
    return "\n".join(parts[-lines:])

# ---------------------------
# Vérifications
# ---------------------------

def check_project_structure():
    """Vérifie que la structure du projet est correcte"""
    print("🔍 Vérification de la structure du projet...")
    required = ["main.py", "core/", "infrastructure/", "ui/"]
    ok = True
    for f in required:
        if os.path.exists(f):
            print(f"✅ {f}")
        else:
            print(f"❌ Manquant: {f}")
            ok = False
    return ok

def check_wine():
    """Vérifie que Wine est installé et configuré"""
    print("🍷 Vérification de Wine...")
    ok, out, _ = run(["wine", "--version"], quiet=True)
    if not ok:
        print("❌ Wine n'est pas installé/configuré")
        return False
    ver = (out or "").strip() or "wine (version inconnue)"
    print(f"✅ Wine détecté: {ver}")
    return True

def clean_pycache_directories():
    """Nettoie tous les dossiers __pycache__ du projet"""
    print("🧹 Nettoyage des dossiers __pycache__...")
    
    removed_count = 0
    removed_size = 0
    
    # Parcours récursif pour trouver tous les dossiers __pycache__
    for root, dirs, files in os.walk("."):
        # Évite de parcourir les dossiers déjà supprimés
        dirs_to_remove = []
        
        for dir_name in dirs:
            if dir_name == "__pycache__":
                cache_path = os.path.join(root, dir_name)
                try:
                    # Calcule la taille avant suppression
                    size = sum(os.path.getsize(os.path.join(cache_path, f))
                             for f in os.listdir(cache_path)
                             if os.path.isfile(os.path.join(cache_path, f)))
                    
                    # Supprime le dossier
                    shutil.rmtree(cache_path, ignore_errors=True)
                    removed_count += 1
                    removed_size += size
                    
                    rel_path = os.path.relpath(cache_path)
                    print(f"   🗑️ Supprimé: {rel_path}")
                    
                    # Évite de parcourir ce dossier
                    dirs_to_remove.append(dir_name)
                    
                except Exception as e:
                    print(f"   ⚠️ Erreur suppression {cache_path}: {e}")
        
        # Retire les dossiers supprimés de la liste à parcourir
        for dir_name in dirs_to_remove:
            dirs.remove(dir_name)
    
    if removed_count > 0:
        size_mb = removed_size / (1024 * 1024)
        print(f"✅ Nettoyage terminé: {removed_count} dossier(s) supprimé(s), {size_mb:.1f} MB libéré(s)")
    else:
        print("✅ Aucun dossier __pycache__ trouvé")
    
    return True

# ---------------------------
# Installation Python Windows
# ---------------------------

def download_python_windows():
    """Télécharge Python Windows si nécessaire"""
    python_installer = "python-3.11.8-amd64.exe"
    if os.path.exists(python_installer):
        print(f"✅ Python Windows déjà présent: {python_installer}")
        return True
    print("📥 Téléchargement de Python Windows...")
    url = f"https://www.python.org/ftp/python/3.11.8/{python_installer}"
    ok, _, _ = run(["wget", url])
    if not ok:
        print("❌ Échec du téléchargement de Python Windows")
        return False
    print(f"✅ Téléchargé: {python_installer}")
    return True

def install_python_windows():
    """Installe Python Windows via Wine"""
    python_installer = "python-3.11.8-amd64.exe"
    if not os.path.exists(python_installer):
        print("❌ Installeur Python Windows introuvable")
        return False
    
    print("🔧 Installation de Python Windows via Wine...")
    ok, _, _ = run(["wine", python_installer, "/quiet", "InstallAllUsers=1", "PrependPath=1"])
    if ok:
        print("✅ Installation Python Windows - Succès")
    else:
        print("⚠️ Installation Python Windows - Erreur (on continue si python est dispo)")
    
    print("🔄 Test Python Windows...")
    ok, out, _ = run(["wine", "python", "--version"], quiet=True)
    if ok:
        print("✅ Test Python Windows - Succès")
        print("✅ Python Windows installé et fonctionnel")
        return True
    print("⚠️ Python Windows non détecté (on continue quand même)")
    return True

def install_windows_dependencies():
    """Installe les dépendances Python nécessaires"""
    print("📦 Installation des dépendances Windows...")
    
    print("🔄 Mise à jour pip Windows...")
    ok, _, _ = run(["wine", "python", "-m", "pip", "install", "--upgrade", "pip"], quiet=True)
    print("✅ Mise à jour pip Windows - Succès" if ok else "⚠️ Mise à jour pip Windows - Erreur")

    deps = [
        "pyinstaller>=5.0",
        "tkinterdnd2>=0.3.0",
        "requests>=2.0",
    ]
    
    for dep in deps:
        print(f"🔄 Installation {dep}...")
        ok, _, _ = run(["wine", "python", "-m", "pip", "install", dep], quiet=True)
        print(f"✅ Installation {dep} - Succès" if ok else f"⚠️ Installation {dep} - Erreur")

    if os.path.exists("requirements.txt"):
        print("🔄 Requirements.txt...")
        ok, _, _ = run(["wine", "python", "-m", "pip", "install", "-r", "requirements.txt"], quiet=True)
        print("✅ Requirements.txt - Succès" if ok else "⚠️ Requirements.txt - Erreur")
    
    return True

# ---------------------------
# Compilation
# ---------------------------

def create_windows_exe(version):
    """Crée l'exécutable Windows avec PyInstaller"""
    exe_name = version  # Utilise directement la version comme nom
    print(f"🔨 Création de l'exécutable Windows: {exe_name}.exe")
    
    # Nettoyage des dossiers de build précédents
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
            print(f"🧹 Dossier {folder}/ nettoyé")
    
    # Commande PyInstaller de base
    cmd = [
        "wine", "python", "-m", "PyInstaller",
        "--onefile", "--windowed",
        f"--name={exe_name}",
        "--clean", "--noconfirm"
    ]
    
    # Ajout de l'icône si présente
    if os.path.exists("icone.ico"):
        cmd.append("--icon=icone.ico")
        print("🎨 Icône ajoutée: icone.ico")
    
    print("📂 Modules à inclure:")
    
    # Modules principaux obligatoires
    modules = [("core", "core"), ("infrastructure", "infrastructure"), ("ui", "ui"), ("__init__.py", ".")]
    for src, dest in modules:
        if os.path.exists(src):
            cmd.extend(["--add-data", f"{src};{dest}"])
            print(f"   ✅ {src} -> {dest}")
    
    # Fichiers et dossiers optionnels
    optional_files = ["04_Configs", "icone.ico"]
    for item in optional_files:
        if os.path.exists(item):
            cmd.extend(["--add-data", f"{item};."])
            print(f"   ✅ Optionnel: {item}")
    
    # Dossier tutorial_images
    tutorial_images_dir = "tutorial_images"
    if os.path.exists(tutorial_images_dir):
        cmd.extend(["--add-data", f"{tutorial_images_dir};tutorial_images"])
        print(f"   ✅ Images tutoriel: {tutorial_images_dir}")
        
        # Compter les images
        try:
            image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
            image_files = [f for f in os.listdir(tutorial_images_dir) 
                         if f.lower().endswith(image_extensions)]
            if image_files:
                print(f"      📸 {len(image_files)} image(s) détectée(s)")
                total_size = sum(os.path.getsize(os.path.join(tutorial_images_dir, f)) 
                               for f in image_files) / (1024 * 1024)
                print(f"      📊 Taille totale des images: {total_size:.1f} MB")
            else:
                print(f"      📁 Dossier présent mais vide")
        except Exception as e:
            print(f"      ⚠️ Erreur lecture dossier: {e}")
    else:
        print(f"   ⚠️ Dossier images tutoriel non trouvé: {tutorial_images_dir}")
    
    # Autres ressources optionnelles
    other_resources = ["templates", "assets"]
    for resource in other_resources:
        if os.path.exists(resource):
            cmd.extend(["--add-data", f"{resource};{resource}"])
            print(f"   ✅ Ressource: {resource}")
    
    # Fichier principal
    cmd.append("main.py")
    
    print("🔧 Commande PyInstaller Windows:")
    print(f"   {' '.join(cmd[:8])} ... (commande complète)")
    print("⏳ Compilation Windows en cours...")
    
    # Exécution de PyInstaller
    ok, out, err = run(cmd, quiet=True)
    
    if not ok:
        print("❌ Erreur compilation Windows")
        tail = short_tail(err or out, lines=40)
        if tail:
            print("— Derniers messages —")
            print(tail)
        return False
    
    print("✅ Compilation PyInstaller terminée")
    
    # Vérification du résultat
    exe_path = os.path.join("dist", f"{exe_name}.exe")
    if not os.path.exists(exe_path):
        print("❌ Aucun fichier .exe trouvé")
        return False

    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print("=" * 60)
    print("🎉 SUCCÈS - Exécutable Windows .exe créé !")
    print("=" * 60)
    print(f"📁 Fichier: {exe_path}")
    print(f"📊 Taille: {size_mb:.1f} MB")
    print(f"🏷️ Version: {version}")
    print("=" * 60)
    
    return True

# ---------------------------
# Main
# ---------------------------

def main():
    """Fonction principale"""
    print("🏗️ Build automatique avec versioning incrémental")
    print("=" * 60)

    # Vérifications préliminaires
    if not check_project_structure():
        return False
    if not check_wine():
        return False

    # Nettoyage des dossiers __pycache__
    if not clean_pycache_directories():
        return False

    # Génération de la nouvelle version
    version = generate_version()

    # Fixation de la version dans constants.py
    if not fix_version_in_constants(version):
        print("❌ Impossible de fixer la version")
        return False

    try:
        # Installation et compilation
        if not download_python_windows():
            return False
        if not install_python_windows():
            return False
        if not install_windows_dependencies():
            return False

        success = create_windows_exe(version)
        
        if success:
            print(f"🎉 BUILD RÉUSSI - Version: {version}")
        else:
            print("❌ ÉCHEC DE LA COMPILATION")
        
        return success

    except Exception as e:
        print(f"❌ Erreur pendant la compilation: {e}")
        return False
        
    finally:
        # Restauration du fichier original
        print("\n🔄 Restauration du fichier constants.py original...")
        restore_constants_backup()

if __name__ == "__main__":
    try:
        if not main():
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Interruption utilisateur")
        restore_constants_backup()
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        restore_constants_backup()
        sys.exit(1)