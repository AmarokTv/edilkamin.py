#!/usr/bin/env python3
"""
Test d'importation pour vérifier que tous les modules peuvent être importés
"""

import sys
from pathlib import Path

def test_imports():
    """Teste que tous les modules peuvent être importés"""
    print("=" * 70)
    print("🧪 Test d'importation des modules")
    print("=" * 70)

    modules_to_test = [
        ("edilkamin.constants", "Constants"),
        ("edilkamin.utils", "Utils"),
        ("edilkamin.buffer_utils", "Buffer utilities"),
        ("edilkamin.async_dispatch", "Async dispatch"),
        ("edilkamin.ble", "BLE functions"),
        ("edilkamin.api", "API"),
    ]

    failed = []

    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✓ {module_name:<35} ({description})")
        except Exception as e:
            print(f"✗ {module_name:<35} ({description})")
            print(f"  Erreur: {e}")
            failed.append((module_name, str(e)))

    print("\n" + "=" * 70)

    if failed:
        print(f"❌ {len(failed)} module(s) ont échoué:")
        for module_name, error in failed:
            print(f"  - {module_name}: {error}")
        return 1
    else:
        print("✅ TOUS LES MODULES S'IMPORTENT CORRECTEMENT!")
        return 0

if __name__ == "__main__":
    sys.exit(test_imports())

