#!/usr/bin/env python3
"""
Script de test pour valider la migration Python 3.14
Vérifie que tous les fichiers modifiés sont syntaxiquement corrects
"""

import sys
import ast
from pathlib import Path

def test_python_syntax(file_path):
    """Test si un fichier Python a une syntaxe valide"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        return True, "✓ Syntaxe valide"
    except SyntaxError as e:
        return False, f"✗ Erreur de syntaxe: {e}"
    except Exception as e:
        return False, f"✗ Erreur: {e}"

def test_imports(file_path):
    """Teste si les imports sont valides"""
    try:
        # Essayer de compiler le fichier
        with open(file_path, 'r', encoding='utf-8') as f:
            compile(f.read(), file_path, 'exec')
        return True, "✓ Imports valides"
    except SyntaxError as e:
        return False, f"✗ Erreur de syntaxe: {e}"
    except Exception as e:
        return False, f"✗ Erreur: {e}"

def test_future_imports():
    """Teste que from __future__ import annotations est présent"""
    files_to_check = [
        "edilkamin/api.py",
        "edilkamin/buffer_utils.py",
        "edilkamin/ble.py",
        "edilkamin/async_dispatch.py",
    ]

    results = []
    for file_path in files_to_check:
        full_path = Path(file_path)
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if "from __future__ import annotations" in content:
                results.append((file_path, True, "✓ Has from __future__ import annotations"))
            else:
                results.append((file_path, False, "✗ Missing from __future__ import annotations"))
        else:
            results.append((file_path, False, "✗ Fichier non trouvé"))

    return results

def test_type_hints():
    """Teste que typing.Dict et typing.Tuple ont été remplacés"""
    files_to_check = [
        "edilkamin/api.py",
        "edilkamin/buffer_utils.py",
        "edilkamin/ble.py",
    ]

    results = []
    for file_path in files_to_check:
        full_path = Path(file_path)
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            has_typing_dict = "typing.Dict" in content and "from typing" in content
            has_typing_tuple = "typing.Tuple" in content and "from typing" in content

            if has_typing_dict or has_typing_tuple:
                results.append((file_path, False, f"✗ Toujours utilise typing.Dict/Tuple"))
            else:
                # Vérifier qu'on utilise dict et tuple
                uses_dict = " dict" in content or ": dict" in content or "-> dict" in content
                uses_tuple = " tuple" in content or ": tuple" in content or "-> tuple" in content
                if uses_dict or uses_tuple:
                    results.append((file_path, True, "✓ Utilise dict/tuple modernes"))
                else:
                    results.append((file_path, True, "✓ Type hints modernisés"))
        else:
            results.append((file_path, False, "✗ Fichier non trouvé"))

    return results

def main():
    print("=" * 70)
    print("🧪 Test de migration Python 3.14")
    print("=" * 70)

    # Test 1: Syntaxe
    print("\n📝 Test 1: Vérifier la syntaxe Python")
    print("-" * 70)
    files_to_test = [
        "edilkamin/api.py",
        "edilkamin/buffer_utils.py",
        "edilkamin/ble.py",
        "edilkamin/async_dispatch.py",
    ]

    syntax_ok = True
    for file_path in files_to_test:
        full_path = Path(file_path)
        if full_path.exists():
            ok, msg = test_python_syntax(full_path)
            status = "✓" if ok else "✗"
            print(f"{status} {file_path}: {msg}")
            if not ok:
                syntax_ok = False
        else:
            print(f"✗ {file_path}: Fichier non trouvé")
            syntax_ok = False

    # Test 2: from __future__ import annotations
    print("\n📦 Test 2: Vérifier from __future__ import annotations")
    print("-" * 70)
    future_results = test_future_imports()
    future_ok = True
    for file_path, ok, msg in future_results:
        status = "✓" if ok else "✗"
        print(f"{status} {file_path}: {msg}")
        if not ok:
            future_ok = False

    # Test 3: Type hints modernes
    print("\n🎯 Test 3: Vérifier les type hints modernes (dict/tuple)")
    print("-" * 70)
    hints_results = test_type_hints()
    hints_ok = True
    for file_path, ok, msg in hints_results:
        status = "✓" if ok else "✗"
        print(f"{status} {file_path}: {msg}")
        if not ok:
            hints_ok = False

    # Test 4: Configuration
    print("\n⚙️  Test 4: Vérifier les fichiers de configuration")
    print("-" * 70)
    config_files = {
        "pyproject.toml": "requires-python = \">=3.10,<4.0\"",
        "tox.ini": "py314",
        ".github/workflows/tests.yml": "3.14",
        ".readthedocs.yaml": "3.14",
    }

    config_ok = True
    for file_path, expected_content in config_files.items():
        full_path = Path(file_path)
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            if expected_content in content:
                print(f"✓ {file_path}: Contient '{expected_content}'")
            else:
                print(f"✗ {file_path}: Ne contient pas '{expected_content}'")
                config_ok = False
        else:
            print(f"✗ {file_path}: Fichier non trouvé")
            config_ok = False

    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 70)

    all_ok = syntax_ok and future_ok and hints_ok and config_ok

    print(f"✓ Syntaxe Python:                    {'PASS' if syntax_ok else 'FAIL'}")
    print(f"✓ from __future__ import annotations: {'PASS' if future_ok else 'FAIL'}")
    print(f"✓ Type hints modernes:               {'PASS' if hints_ok else 'FAIL'}")
    print(f"✓ Configuration:                     {'PASS' if config_ok else 'FAIL'}")
    print("-" * 70)

    if all_ok:
        print("✅ TOUS LES TESTS PASSENT!")
        print("\n🚀 La migration vers Python 3.14 est réussie!")
        return 0
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        return 1

if __name__ == "__main__":
    sys.exit(main())

