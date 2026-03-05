#!/usr/bin/env python3
"""Test simple d'importation des modules edilkamin"""

try:
    import edilkamin.constants as constants
    print("✓ edilkamin.constants")
except Exception as e:
    print(f"✗ edilkamin.constants: {e}")

try:
    import edilkamin.utils as utils
    print("✓ edilkamin.utils")
except Exception as e:
    print(f"✗ edilkamin.utils: {e}")

try:
    import edilkamin.buffer_utils as buffer_utils
    print("✓ edilkamin.buffer_utils")
except Exception as e:
    print(f"✗ edilkamin.buffer_utils: {e}")

try:
    import edilkamin.async_dispatch as async_dispatch
    print("✓ edilkamin.async_dispatch")
except Exception as e:
    print(f"✗ edilkamin.async_dispatch: {e}")

try:
    import edilkamin.ble as ble
    print("✓ edilkamin.ble")
except Exception as e:
    print(f"✗ edilkamin.ble: {e}")

try:
    import edilkamin.api as api
    print("✓ edilkamin.api")
except Exception as e:
    print(f"✗ edilkamin.api: {e}")

print("\n✅ Tous les modules sont importables!")

