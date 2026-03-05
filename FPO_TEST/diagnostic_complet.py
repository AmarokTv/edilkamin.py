#!/usr/bin/env python3
"""
Script de diagnostic complet pour l'API Edilkamin
Teste tous les aspects pour identifier où est le problème
"""

import sys
import warnings
import os
import time

# Désactiver tous les avertissements
warnings.filterwarnings('ignore')

# Désactiver la vérification SSL
os.environ["PYTHONHTTPSVERIFY"] = "0"
os.environ["AWS_CA_BUNDLE"] = ""

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import ssl
_orig_ctx = ssl.create_default_context
def _no_verify_ctx(*args, **kwargs):
    ctx = _orig_ctx(*args, **kwargs)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx
ssl.create_default_context = _no_verify_ctx

# Importer les dépendances
from pycognito import Cognito
from edilkamin import constants
import httpx

USERNAME = "amarok38@gmail.com"
PASSWORD = "Fpo140501*"
MAC_ADDRESS = "44:17:93:7a:21:90"


def print_header(title):
    """Afficher un titre formaté"""
    print("\n" + "=" * 70)
    print(f"🔍 {title}")
    print("=" * 70)


def test_ssl_connection():
    """Test la connexion SSL"""
    print_header("TEST 1 : Connexion SSL")

    try:
        print(f"Méthode: GET")
        response = httpx.get("https://the-mind-api.edilkamin.com/", verify=False, timeout=10.0)
        print(f"✅ Connexion SSL OK - Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Erreur SSL: {e}")
        return False


def test_authentication():
    """Test l'authentification Cognito"""
    print_header("TEST 2 : Authentification AWS Cognito")

    try:
        print(f"Authentification de {USERNAME}...")
        cognito = Cognito(constants.USER_POOL_ID, constants.CLIENT_ID, username=USERNAME)
        cognito.authenticate(PASSWORD)
        user = cognito.get_user()
        id_token = user._metadata["id_token"]
        access_token = user._metadata["access_token"]

        print(f"✅ Authentification OK")
        print(f"ID Token: {id_token[:50]}...")
        print(f"Access Token: {access_token[:50]}...")
        return (id_token, access_token)
    except Exception as e:
        print(f"❌ Erreur authentification: {e}")
        return (None, None)


def test_device_info(token):
    """Test la récupération des infos du dispositif"""
    print_header("TEST 3 : Récupération des infos du dispositif")

    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }

        mac_clean = MAC_ADDRESS.replace(":", "").lower()
        url = f"https://the-mind-api.edilkamin.com/device/{mac_clean}/info"

        print(f"Méthode: GET")
        print(f"URL: {url}")
        print(f"Timeout: 60 secondes")
        print(f"Envoi de la requête...")

        start_time = time.time()
        response = httpx.get(url, headers=headers, verify=False, timeout=60.0)
        elapsed = time.time() - start_time

        print(f"✅ Réponse reçue en {elapsed:.2f}s")
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Données valides reçues")

            # Structure des données
            print(f"\n📋 STRUCTURE DES DONNÉES REÇUES:")
            print(f"\n1️⃣  INFORMATIONS COMPOSANTS (component_info):")
            if "component_info" in data:
                comp = data["component_info"]
                print(f"   - Timestamp: {comp.get('timestamp', 'N/A')}")
                if "motherboard" in comp:
                    mb = comp["motherboard"]
                    print(f"   - Carte mère: {mb.get('board_name', 'N/A')}")
                    print(f"   - Version app: {mb.get('application_version', 'N/A')}")

            print(f"\n2️⃣  ÉTAT EN TEMPS RÉEL (status):")
            if "status" in data:
                status = data["status"]
                print(f"   - État du poêle: {status['state']['stove_state']}")
                print(f"   - Puissance actuelle: {status['state']['actual_power']}")
                print(f"   - Alimentation: {'ON' if status['commands']['power'] else 'OFF'}")

                print(f"\n   📊 Températures:")
                temps = status.get("temperatures", {})
                print(f"      - Ambiante (enviroment): {temps.get('enviroment', 'N/A')}°C")
                print(f"      - Thermocouple: {temps.get('thermocouple', 'N/A')}°C")
                print(f"      - Carte électronique: {temps.get('board', 'N/A')}°C")
                print(f"      - Capteur 1 (NTC 1): {temps.get('feeler_ntc_1', 'N/A')}°C")

                print(f"\n   💨 Ventilateurs:")
                fans = status.get("fans", {})
                print(f"      - Ventilateur 1: {fans.get('fan_1_speed', 'N/A')}%")
                print(f"      - Ventilateur 2: {fans.get('fan_2_speed', 'N/A')}%")
                print(f"      - Ventilateur 3: {fans.get('fan_3_speed', 'N/A')}%")

                print(f"\n   ⚙️  Moteurs:")
                engines = status.get("engines", {})
                print(f"      - Vitesse Cochlea: {engines.get('real_cochlea_speed', 'N/A')} tr/min")
                print(f"      - Vitesse ventilateur fumées: {engines.get('real_smokes_fan_speed', 'N/A')} tr/min")

                print(f"\n   🚨 Drapeaux:")
                flags = status.get("flags", {})
                print(f"      - Chat service requis: {flags.get('is_cat_service_required', False)}")
                print(f"      - Pellets en réserve: {flags.get('is_pellet_in_reserve', False)}")
                print(f"      - Mode chrono actif: {flags.get('is_crono_active', False)}")
                print(f"      - Température fumée haute: {flags.get('is_smokes_temperature_high', False)}")

            print(f"\n3️⃣  PARAMÈTRES UTILISATEUR (nvm.user_parameters):")
            if "nvm" in data and "user_parameters" in data["nvm"]:
                user_params = data["nvm"]["user_parameters"]
                print(f"   - Température cible env 1: {user_params.get('enviroment_1_temperature', 'N/A')}°C")
                print(f"   - Température cible env 2: {user_params.get('enviroment_2_temperature', 'N/A')}°C")
                print(f"   - Mode auto: {user_params.get('is_auto', False)}")
                print(f"   - Mode standby: {user_params.get('is_standby_active', False)}")
                print(f"   - Mode relax: {user_params.get('is_relax_active', False)}")
                print(f"   - Puissance manuelle: {user_params.get('manual_power', 'N/A')}")

            print(f"\n4️⃣  COMPTEURS (nvm.total_counters):")
            if "nvm" in data and "total_counters" in data["nvm"]:
                counters = data["nvm"]["total_counters"]
                print(f"   - Mises en marche: {counters.get('power_ons', 'N/A')}")
                print(f"   - Temps P1: {counters.get('p1_working_time', 'N/A')}h")
                print(f"   - Temps P2: {counters.get('p2_working_time', 'N/A')}h")
                print(f"   - Temps P3: {counters.get('p3_working_time', 'N/A')}h")

            print(f"\n5️⃣  ALARMES (nvm.alarms_log):")
            if "nvm" in data and "alarms_log" in data["nvm"]:
                alarms_log = data["nvm"]["alarms_log"]
                print(f"   - Nombre total: {alarms_log.get('number', 'N/A')}")
                print(f"   - Index: {alarms_log.get('index', 'N/A')}")

            print(f"\n💾 PAYLOAD COMPLET:")
            print(data)
            return True
        else:
            print(f"⚠️  Status {response.status_code}")
            print(f"Réponse: {response.text[:200]}")
            return False

    except httpx.TimeoutException as e:
        print(f"❌ TIMEOUT après 60s: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False



def test_mqtt_check_command(token):
    """Test la commande MQTT 'check'"""
    print_header("TEST 4 : Commande MQTT 'check'")

    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "mac_address": MAC_ADDRESS.replace(":", "").lower(),
            "name": "check"
        }

        url = "https://the-mind-api.edilkamin.com/mqtt/command"

        print(f"Méthode: PUT")
        print(f"URL: {url}")
        print(f"Commande: check")
        print(f"MAC: {payload['mac_address']}")
        print(f"Payload envoyé: {payload}")
        print(f"Timeout: 60 secondes")
        print(f"Envoi de la requête...")

        start_time = time.time()
        response = httpx.put(url, json=payload, headers=headers, verify=False, timeout=60.0)
        elapsed = time.time() - start_time

        print(f"Réponse reçue en {elapsed:.2f}s")
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print(f"✅ Commande exécutée")
            print(f"Payload réponse: {response.json()}")
            return True
        elif response.status_code == 504:
            print(f"❌ ERREUR 504 Gateway Timeout")
            print(f"⚠️  C'est un problème du SERVEUR Edilkamin")
            return False
        else:
            print(f"❌ Status {response.status_code}")
            print(f"Payload réponse: {response.text[:200]}")
            return False

    except httpx.TimeoutException as e:
        print(f"❌ TIMEOUT après 60s: {e}")
        print(f"⚠️  Timeout côté client (pas une erreur 504)")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False



def test_mqtt_power_command(token):
    """Test la commande MQTT 'power'"""
    print_header("TEST 5 : Commande MQTT 'power'")

    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "mac_address": MAC_ADDRESS.replace(":", "").lower(),
            "name": "power",
            "value": 1
        }

        url = "https://the-mind-api.edilkamin.com/mqtt/command"

        print(f"Méthode: PUT")
        print(f"URL: {url}")
        print(f"Commande: power ON")
        print(f"MAC: {payload['mac_address']}")
        print(f"Payload envoyé: {payload}")
        print(f"Timeout: 60 secondes")
        print(f"Envoi de la requête...")

        start_time = time.time()
        response = httpx.put(url, json=payload, headers=headers, verify=False, timeout=60.0)
        elapsed = time.time() - start_time

        print(f"Réponse reçue en {elapsed:.2f}s")
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print(f"✅ Commande exécutée")
            print(f"Payload réponse: {response.json()}")
            return True
        elif response.status_code == 504:
            print(f"❌ ERREUR 504 Gateway Timeout")
            print(f"⚠️  C'est un problème du SERVEUR Edilkamin")
            return False
        else:
            print(f"❌ Status {response.status_code}")
            print(f"Payload réponse: {response.text[:200]}")
            return False

    except httpx.TimeoutException as e:
        print(f"❌ TIMEOUT après 60s: {e}")
        print(f"⚠️  Timeout côté client (pas une erreur 504)")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False




def main():
    print("\n" + "=" * 70)
    print("DIAGNOSTIC COMPLET API EDILKAMIN")
    print("=" * 70)

    results = {
        "SSL": False,
        "Authentication": False,
        "Device Info": False,
        "MQTT Check": False,
        "MQTT Power": False,
    }

    try:
        # Test 1 : SSL
        results["SSL"] = test_ssl_connection()

        if not results["SSL"]:
            print("\n⚠️  La connexion SSL échoue, impossible de continuer")
            return

        # Test 2 : Authentification
        id_token, access_token = test_authentication()
        results["Authentication"] = id_token is not None and access_token is not None

        if not id_token or not access_token:
            print("\n⚠️  L'authentification échoue, impossible de continuer")
            return

        # Test 3 : Device Info
        results["Device Info"] = test_device_info(id_token)

        # Test 4 : MQTT Check
        results["MQTT Check"] = test_mqtt_check_command(id_token)

        # Test 5 : MQTT Power
        results["MQTT Power"] = test_mqtt_power_command(id_token)


    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu par l'utilisateur")
        return
    except Exception as e:
        print(f"\n\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        return

    # Résumé final
    print_header("RÉSUMÉ DES RÉSULTATS")

    for test_name, result in results.items():
        status = "✅ OK" if result else "❌ ERREUR"
        print(f"{test_name:20} : {status}")

    print("\n" + "=" * 70)

    # Analyse
    if results["SSL"] and results["Authentication"] and results["Device Info"]:
        if not results["MQTT Check"] or not results["MQTT Power"]:
            print("\n🚨 DIAGNOSTIC : PROBLÈME CÔTÉ SERVEUR EDILKAMIN")
            print("\nLes commandes MQTT échouent (erreur 504) alors que :")
            print("✅ La connexion SSL fonctionne")
            print("✅ L'authentification fonctionne")
            print("✅ La récupération des infos fonctionne")
            print("\n👉 Le problème vient du serveur MQTT d'Edilkamin")
            print("👉 Il faut signaler ce bug à Edilkamin")
        else:
            print("\n✅ TOUT FONCTIONNE !")
    else:
        print("\n⚠️  Il y a des problèmes à corriger")

    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
