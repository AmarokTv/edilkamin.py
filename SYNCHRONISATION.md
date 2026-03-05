# 🔄 Guide de Synchronisation avec GitHub

## 📋 Étapes pour Synchroniser Votre Projet

### Étape 1 : Configuration Initiale

Si vous n'avez pas encore initialisé Git :

```bash
cd C:\Users\amaro\Developpement\edilkamin.py-main\edilkamin.py-main
git init
git add .
git commit -m "Initial commit: edilkamin.py with diagnostic tools"
```

### Étape 2 : Ajouter le Dépôt Officiel comme Remote

```bash
git remote add official https://github.com/AndreMiras/edilkamin.py
```

Vérifiez les remotes configurés :
```bash
git remote -v
```

Vous devriez voir :
```
official    https://github.com/AndreMiras/edilkamin.py (fetch)
official    https://github.com/AndreMiras/edilkamin.py (push)
```

### Étape 3 : Récupérer les Mises à Jour

```bash
# Récupérer les dernières modifications du dépôt officiel
git fetch official

# Voir les différences
git diff main official/main

# Fusionner les modifications
git merge official/main
```

---

## 🔀 Stratégies de Synchronisation

### Option A : Suivre le Dépôt Officiel

Si vous voulez rester synchronisé avec l'officiel :

```bash
# Configurer main pour suivre official/main
git branch -u official/main main

# À chaque fois, récupérer et fusionner
git pull official main
```

### Option B : Créer Votre Propre Fork

1. Sur GitHub, créez un fork du dépôt officiel
2. Configurez votre projet pour pointer vers votre fork :

```bash
git remote set-url origin https://github.com/VOTRE_USERNAME/edilkamin.py
git branch -u origin/main main
```

3. Maintenir la synchronisation avec l'officiel :

```bash
git remote add upstream https://github.com/AndreMiras/edilkamin.py
git pull upstream main
```

### Option C : Garder Une Branche Personnalisée

```bash
# Créer une branche pour vos modifications
git checkout -b personal/diagnostic-tools

# Ajouter vos fichiers
git add .
git commit -m "Add diagnostic tools"

# Maintenir main synchronisé avec l'officiel
git checkout main
git pull official main

# Fusionner vos outils quand nécessaire
git merge personal/diagnostic-tools
```

---

## 📝 Fichiers Clés à Synchroniser

### ✅ À Garder Synchronisés (depuis l'officiel)

```
edilkamin/__init__.py
edilkamin/api.py
edilkamin/constants.py
edilkamin/async_dispatch.py
edilkamin/buffer_utils.py
edilkamin/utils.py
edilkamin/ble.py
edilkamin/__main__.py
tests/
pyproject.toml
README.md
```

### ⭐ Vos Additions (à garder)

```
FPO TEST/diagnostic_complet.py     # Script de diagnostic
compare_with_official.py           # Script de comparaison
RAPPORT_COMPARAISON.md             # Rapport d'analyse
SYNCHRONISATION.md                 # Ce fichier
```

### 🚫 À Ignorer Toujours

```
.idea/                    # Configuration IntelliJ
__pycache__/              # Fichiers compilés
*.pyc                     # Bytecode Python
.pytest_cache/            # Cache pytest
.egg-info/                # Info installation
```

---

## 🔧 Commandes Utiles

### Vérifier l'État

```bash
# Voir le statut
git status

# Voir les remotes
git remote -v

# Voir les branches
git branch -a

# Voir les modifications à venir
git fetch official && git log HEAD..official/main
```

### Résoudre les Conflits

```bash
# Si des conflits apparaissent lors de la fusion
git status                    # Voir les fichiers en conflit
# Éditer les fichiers en conflit
git add <fichier>            # Marquer comme résolu
git commit -m "Resolve conflicts"
```

### Annuler les Modifications

```bash
# Annuler les modifications non commitées
git checkout -- <fichier>

# Annuler le dernier commit (garder les changements)
git reset --soft HEAD~1

# Annuler le dernier commit (perdre les changements)
git reset --hard HEAD~1
```

---

## 📊 Vérifier la Synchronisation

### État Actuel

**Version de votre projet** : 1.6.0 (identique à l'officiel) ✅

**Fichiers synchronisés** :
- 27 fichiers en commun
- 100% de conformité avec l'officiel

**Fichiers supplémentaires (vos outils)** :
- diagnostic_complet.py (13.8 KB)
- compare_with_official.py (5.0 KB)
- RAPPORT_COMPARAISON.md (6.0 KB)

### Lancer la Vérification

```bash
python compare_with_official.py
```

---

## 🚀 Contribuer au Dépôt Officiel

Si vous voulez contribuer diagnostic_complet.py :

### 1. Créer un Fork

```bash
# Sur GitHub, cliquez "Fork"
git clone https://github.com/VOTRE_USERNAME/edilkamin.py
cd edilkamin.py
```

### 2. Créer une Branche

```bash
git checkout -b feature/diagnostic-script
git add FPO\ TEST/diagnostic_complet.py
git commit -m "Add comprehensive diagnostic script"
```

### 3. Créer un Pull Request

```bash
git push origin feature/diagnostic-script
```

Ensuite sur GitHub :
- Allez à votre fork
- Cliquez "Compare & pull request"
- Remplissez la description
- Cliquez "Create pull request"

---

## 📅 Programmation d'une Mise à Jour Régulière

### Créer un Script de Mise à Jour (Windows Batch)

**Fichier : update_from_official.bat**

```batch
@echo off
cd C:\Users\amaro\Developpement\edilkamin.py-main\edilkamin.py-main
git fetch official
git merge official/main
echo Mise à jour effectuee a %date% %time%
pause
```

### Ou un Script Python

**Fichier : update_from_official.py**

```python
#!/usr/bin/env python3
import subprocess
import os

os.chdir(r"C:\Users\amaro\Developpement\edilkamin.py-main\edilkamin.py-main")
subprocess.run(["git", "fetch", "official"])
subprocess.run(["git", "merge", "official/main"])
print("✅ Mise à jour effectuée!")
```

---

## ❓ Aide et Troubleshooting

### Git n'est pas reconnu

```powershell
# Utiliser le chemin complet
& "C:\Program Files\Git\bin\git.exe" status
```

### Erreur "fatal: not a git repository"

```bash
git init
git remote add official https://github.com/AndreMiras/edilkamin.py
```

### Conflits de fusion

```bash
# Voir les conflits
git status

# Utiliser l'outil de fusion
git mergetool

# Ou éditer manuellement et résoudre
git add <fichier>
git commit -m "Resolve conflicts"
```

---

## 📚 Ressources

- 📖 [Documentation Git](https://git-scm.com/doc)
- 🔗 [Dépôt Officiel](https://github.com/AndreMiras/edilkamin.py)
- 💬 [GitHub Help](https://docs.github.com/)

---

*Dernier mis à jour : 2026-03-06*

