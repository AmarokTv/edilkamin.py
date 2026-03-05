#!/usr/bin/env python3
"""
Script de comparaison entre votre projet et le dépôt officiel GitHub
Génère un rapport détaillé des différences
"""

import os
import json
from pathlib import Path
from collections import defaultdict

def compare_directories(local_path, official_path):
    """Compare deux répertoires et retourne les différences"""

    local_files = set()
    official_files = set()

    # Fichiers locaux
    for root, dirs, files in os.walk(local_path):
        # Ignorer certains répertoires
        dirs[:] = [d for d in dirs if d not in ['.git', '.idea', '__pycache__', '.pytest_cache', '*.egg-info']]

        for file in files:
            if file.startswith('.'):
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, local_path)
            local_files.add(rel_path.replace('\\', '/'))

    # Fichiers officiels
    for root, dirs, files in os.walk(official_path):
        dirs[:] = [d for d in dirs if d not in ['.git', '.idea', '__pycache__', '.pytest_cache', '*.egg-info']]

        for file in files:
            if file.startswith('.'):
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, official_path)
            official_files.add(rel_path.replace('\\', '/'))

    # Comparaison
    results = {
        'only_in_local': sorted(local_files - official_files),
        'only_in_official': sorted(official_files - local_files),
        'in_both': sorted(local_files & official_files),
        'total_local': len(local_files),
        'total_official': len(official_files),
    }

    return results

def analyze_local_additions(local_path, files):
    """Analyse les fichiers supplémentaires locaux"""
    print("\n📌 FICHIERS SUPPLÉMENTAIRES DANS VOTRE PROJET\n")

    for file in sorted(files):
        file_path = os.path.join(local_path, file)
        size = os.path.getsize(file_path)
        size_kb = size / 1024

        if 'FPO TEST' in file:
            print(f"  ⭐ {file} ({size_kb:.1f} KB)")
            print(f"     Description: Script de diagnostic personnalisé")
        elif '.idea' in file:
            print(f"  🔧 {file} ({size_kb:.1f} KB)")
            print(f"     Description: Configuration IntelliJ IDE (à ignorer)")
        else:
            print(f"  ✨ {file} ({size_kb:.1f} KB)")

def main():
    LOCAL_PATH = r"C:\Users\amaro\Developpement\edilkamin.py-main\edilkamin.py-main"
    OFFICIAL_PATH = r"C:\Users\amaro\Developpement\edilkamin-official"

    print("=" * 70)
    print("📊 COMPARAISON : VOTRE PROJET vs DÉPÔT OFFICIEL")
    print("=" * 70)

    if not os.path.exists(LOCAL_PATH):
        print(f"❌ Chemin local introuvable: {LOCAL_PATH}")
        return

    if not os.path.exists(OFFICIAL_PATH):
        print(f"❌ Chemin officiel introuvable: {OFFICIAL_PATH}")
        print("\nPour cloner le dépôt officiel:")
        print('  git clone https://github.com/AndreMiras/edilkamin.py C:\\Users\\amaro\\Developpement\\edilkamin-official')
        return

    # Comparaison
    results = compare_directories(LOCAL_PATH, OFFICIAL_PATH)

    print(f"\n📈 STATISTIQUES\n")
    print(f"  Fichiers dans votre projet: {results['total_local']}")
    print(f"  Fichiers dans le dépôt officiel: {results['total_official']}")
    print(f"  Fichiers en commun: {len(results['in_both'])}")
    print(f"  Fichiers supplémentaires (local): {len(results['only_in_local'])}")
    print(f"  Fichiers supplémentaires (officiel): {len(results['only_in_official'])}")

    # Fichiers supplémentaires
    if results['only_in_local']:
        analyze_local_additions(LOCAL_PATH, results['only_in_local'])

    if results['only_in_official']:
        print("\n📌 FICHIERS MANQUANTS DANS VOTRE PROJET (DEPUIS LE DÉPÔT OFFICIEL)\n")
        for file in sorted(results['only_in_official']):
            print(f"  ⚠️  {file}")

    # Recommandations
    print("\n" + "=" * 70)
    print("💡 RECOMMANDATIONS")
    print("=" * 70)

    if results['only_in_official']:
        print("\n1️⃣  FICHIERS MANQUANTS À SYNCHRONISER")
        print("   Exécutez pour mettre à jour:")
        print("   git fetch official")
        print("   git merge official/main")

    if 'FPO TEST' in str(results['only_in_local']):
        print("\n2️⃣  VOTRE SCRIPT diagnostic_complet.py EST EXCELLENT!")
        print("   💡 Envisagez un pull request vers le dépôt officiel")
        print("   📝 Ou publiez-le comme outil séparé")

    print("\n3️⃣  INITIALISER GIT POUR VOTRE PROJET")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit'")
    print("   git remote add official https://github.com/AndreMiras/edilkamin.py")

    print("\n" + "=" * 70)
    print("✅ Rapport généré avec succès!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()

