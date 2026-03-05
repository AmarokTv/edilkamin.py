#!/usr/bin/env python3
"""
Script rapide pour gérer la synchronisation avec GitHub
Utilisation simple et menus interactifs
"""

import subprocess
import os
import sys

PROJECT_PATH = r"C:\Users\amaro\Developpement\edilkamin.py-main\edilkamin.py-main"
GIT_EXE = r"C:\Program Files\Git\bin\git.exe"
OFFICIAL_REPO = "https://github.com/AndreMiras/edilkamin.py"

def run_git(args):
    """Exécuter une commande git"""
    try:
        result = subprocess.run([GIT_EXE] + args, cwd=PROJECT_PATH, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def print_menu():
    """Afficher le menu"""
    print("\n" + "=" * 60)
    print("🔄 SYNCHRONISATION EDILKAMIN.PY")
    print("=" * 60)
    print("\n📋 MENU PRINCIPAL:\n")
    print("1️⃣  Vérifier l'état du projet")
    print("2️⃣  Récupérer les mises à jour du dépôt officiel")
    print("3️⃣  Fusionner les mises à jour")
    print("4️⃣  Voir les différences")
    print("5️⃣  Initialiser Git")
    print("6️⃣  Voir le statut Git")
    print("7️⃣  Faire un commit")
    print("8️⃣  Voir les logs")
    print("0️⃣  Quitter")
    print("\n" + "=" * 60)

def check_git_project():
    """Vérifier si Git est initialisé"""
    returncode, _, _ = run_git(["status"])
    return returncode == 0

def option_1_check_status():
    """Vérifier l'état"""
    print("\n🔍 Vérification de l'état du projet...\n")

    if not check_git_project():
        print("❌ Git n'est pas initialisé")
        print("\nÉxécutez l'option 5 (Initialiser Git)")
        return

    print("✅ Git est initialisé\n")

    # Remotes
    returncode, stdout, _ = run_git(["remote", "-v"])
    if returncode == 0:
        print("📡 REMOTES CONFIGURÉS:")
        print(stdout)

    # Branches
    returncode, stdout, _ = run_git(["branch", "-a"])
    if returncode == 0:
        print("🌳 BRANCHES:")
        print(stdout)

    # Statut
    returncode, stdout, _ = run_git(["status"])
    if returncode == 0:
        print("📊 STATUT GIT:")
        print(stdout)

def option_2_fetch():
    """Récupérer les mises à jour"""
    print("\n⬇️  Récupération des mises à jour...\n")

    if not check_git_project():
        print("❌ Git n'est pas initialisé")
        return

    returncode, stdout, stderr = run_git(["fetch", "official"])

    if returncode == 0:
        print("✅ Mises à jour récupérées\n")
        print(stdout)
    else:
        print("❌ Erreur lors de la récupération")
        print(stderr)

def option_3_merge():
    """Fusionner les mises à jour"""
    print("\n🔀 Fusion des mises à jour...\n")

    if not check_git_project():
        print("❌ Git n'est pas initialisé")
        return

    confirm = input("Êtes-vous sûr? (oui/non): ").lower()
    if confirm != "oui":
        print("❌ Fusion annulée")
        return

    returncode, stdout, stderr = run_git(["merge", "official/main"])

    if returncode == 0:
        print("✅ Fusion effectuée\n")
        print(stdout)
    else:
        print("⚠️  Il y a peut-être des conflits\n")
        print(stdout)
        print(stderr)

def option_4_diff():
    """Voir les différences"""
    print("\n📊 Différences avec le dépôt officiel...\n")

    if not check_git_project():
        print("❌ Git n'est pas initialisé")
        return

    returncode, stdout, stderr = run_git(["fetch", "official"])
    returncode, stdout, stderr = run_git(["diff", "main", "official/main", "--stat"])

    if returncode == 0:
        print(stdout)
    else:
        print("❌ Erreur")
        print(stderr)

def option_5_init():
    """Initialiser Git"""
    print("\n📝 Initialisation de Git...\n")

    if check_git_project():
        print("✅ Git est déjà initialisé")
        return

    # Init
    returncode, stdout, stderr = run_git(["init"])
    if returncode == 0:
        print("✅ Dépôt Git créé")

    # Add remote
    returncode, _, _ = run_git(["remote", "add", "official", OFFICIAL_REPO])
    if returncode == 0:
        print("✅ Remote 'official' ajouté")

    # Add all
    returncode, _, _ = run_git(["add", "."])
    if returncode == 0:
        print("✅ Fichiers ajoutés")

    # Initial commit
    returncode, stdout, stderr = run_git(["commit", "-m", "Initial commit: edilkamin.py with diagnostic tools"])
    if returncode == 0:
        print("✅ Commit initial effectué")
    else:
        print("⚠️  Aucun changement à commiter")

def option_6_status():
    """Voir le statut"""
    print("\n📊 Statut Git\n")

    if not check_git_project():
        print("❌ Git n'est pas initialisé")
        return

    returncode, stdout, stderr = run_git(["status"])
    print(stdout)

def option_7_commit():
    """Faire un commit"""
    print("\n💾 Nouveau Commit\n")

    if not check_git_project():
        print("❌ Git n'est pas initialisé")
        return

    message = input("Message de commit: ").strip()
    if not message:
        print("❌ Message vide")
        return

    # Add
    run_git(["add", "."])

    # Commit
    returncode, stdout, stderr = run_git(["commit", "-m", message])
    if returncode == 0:
        print("✅ Commit effectué")
        print(stdout)
    else:
        print("❌ Erreur")
        print(stderr)

def option_8_logs():
    """Voir les logs"""
    print("\n📜 Derniers commits\n")

    if not check_git_project():
        print("❌ Git n'est pas initialisé")
        return

    returncode, stdout, stderr = run_git(["log", "--oneline", "-20"])
    print(stdout)

def main():
    print("\n🚀 GESTIONNAIRE DE SYNCHRONISATION")
    print("Édilkamin.py - 2026-03-06\n")

    while True:
        print_menu()
        choice = input("Sélectionnez une option (0-8): ").strip()

        if choice == "0":
            print("\n👋 Au revoir!\n")
            break
        elif choice == "1":
            option_1_check_status()
        elif choice == "2":
            option_2_fetch()
        elif choice == "3":
            option_3_merge()
        elif choice == "4":
            option_4_diff()
        elif choice == "5":
            option_5_init()
        elif choice == "6":
            option_6_status()
        elif choice == "7":
            option_7_commit()
        elif choice == "8":
            option_8_logs()
        else:
            print("❌ Option invalide")

        input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Annulé par l'utilisateur\n")
        sys.exit(0)

