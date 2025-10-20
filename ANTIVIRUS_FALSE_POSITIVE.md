# ⚠️ Faux Positif Antivirus

## Le problème

Certains antivirus (notamment **Windows Defender**) peuvent bloquer `RenExtract.exe` en le signalant comme "virus ou logiciel potentiellement indésirable".

**C'est un faux positif.** RenExtract ne contient aucun code malveillant.

## Pourquoi ?

RenExtract est compilé avec PyInstaller, qui empaquette Python et toutes les bibliothèques dans un seul fichier `.exe`. Cette technique est souvent mal détectée par les antivirus qui utilisent la détection heuristique.

**C'est un problème très courant** avec les applications Python compilées.

## RenExtract est sûr

- ✅ **Code open-source** : Tout le code est visible sur [GitHub](https://github.com/Rory-Mercury-91/RenExtract)
- ✅ **Licence MIT** : Licence open-source standard
- ✅ **Pas de collecte de données** : Aucune donnée n'est envoyée
- ✅ **Pas de communication réseau** : Sauf téléchargement des images du tutoriel depuis GitHub
- ✅ **Vérifiable** : Uploadez le fichier sur [VirusTotal.com](https://www.virustotal.com/) → 0-2 détections génériques sur 60+

## Solution

### Ajouter une exception dans votre antivirus

Chaque antivirus a sa propre méthode pour ajouter des exceptions. Consultez la documentation de votre antivirus.

**Pour Windows Defender** :
1. Ouvrez "Sécurité Windows"
2. Allez dans "Protection contre les virus et menaces"
3. Cliquez sur "Gérer les paramètres"
4. Descendez jusqu'à "Exclusions"
5. Cliquez sur "Ajouter ou supprimer des exclusions"
6. Ajoutez le fichier `RenExtract.exe`

### Utiliser la version Python (recommandé si vous avez Python 3.11+)

Cette méthode évite complètement le problème :

```bash
git clone https://github.com/Rory-Mercury-91/RenExtract.git
cd RenExtract
pip install -r requirements.txt
python main.py
```

**Avantages** :
- Aucun problème avec les antivirus
- Code source visible
- Mises à jour faciles avec `git pull`

## Pour les administrateurs réseau

Si vous devez déployer sur plusieurs machines :
1. Ajoutez une exception dans votre solution antivirus d'entreprise
2. Utilisez le hash SHA256 du fichier pour créer une règle d'exception
3. Ou compilez vous-même depuis le code source

## Besoin d'aide ?

- **GitHub Issues** : [Signaler un problème](https://github.com/Rory-Mercury-91/RenExtract/issues)
- **GitHub Discussions** : [Poser une question](https://github.com/Rory-Mercury-91/RenExtract/discussions)
