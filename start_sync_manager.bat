@echo off
REM Script batch pour accéder rapidement aux outils de synchronisation edilkamin.py
REM À exécuter dans: C:\Users\amaro\Developpement\edilkamin.py-main\edilkamin.py-main

setlocal enabledelayedexpansion
color 0B
cls

:menu
cls
echo.
echo ============================================================================
echo                  🔄 GESTIONNAIRE DE SYNCHRONISATION EDILKAMIN.PY
echo ============================================================================
echo.
echo Version: 1.6.0
echo Projet: edilkamin.py
echo Statut: ✅ Synchronisé 100%%
echo.
echo ============================================================================
echo                              📋 MENU PRINCIPAL
echo ============================================================================
echo.
echo   1️⃣  Gestionnaire Git Interactif (RECOMMANDÉ)
echo   2️⃣  Générer un Rapport de Comparaison
echo   3️⃣  Afficher le Résumé Final
echo   4️⃣  Lancer le Diagnostic API
echo   5️⃣  Ouvrir le Guide de Démarrage
echo   6️⃣  Ouvrir le Rapport Complet
echo   7️⃣  Ouvrir le Guide Git
echo   8️⃣  Ouvrir la Page HTML
echo   9️⃣  Voir l'État Git
echo   0️⃣  Quitter
echo.
echo ============================================================================

set /p choice="Sélectionnez une option (0-9): "

if "%choice%"=="1" goto git_manager
if "%choice%"=="2" goto compare
if "%choice%"=="3" goto resume
if "%choice%"=="4" goto diagnostic
if "%choice%"=="5" goto guide
if "%choice%"=="6" goto rapport
if "%choice%"=="7" goto sync
if "%choice%"=="8" goto html
if "%choice%"=="9" goto status
if "%choice%"=="0" goto quit

echo ❌ Option invalide
timeout /t 2 > nul
goto menu

:git_manager
cls
echo ▶️  Lancement du Gestionnaire Git...
python git_sync_manager.py
pause
goto menu

:compare
cls
echo ▶️  Génération du rapport de comparaison...
python compare_with_official.py
pause
goto menu

:resume
cls
echo ▶️  Affichage du résumé final...
python RESUME_FINAL.py
pause
goto menu

:diagnostic
cls
echo ▶️  Lancement du diagnostic API...
python "FPO TEST\diagnostic_complet.py"
pause
goto menu

:guide
cls
echo ▶️  Ouverture du guide de démarrage...
start notepad GUIDE_DEMARRAGE.md
goto menu

:rapport
cls
echo ▶️  Ouverture du rapport complet...
start notepad RAPPORT_COMPARAISON.md
goto menu

:sync
cls
echo ▶️  Ouverture du guide Git...
start notepad SYNCHRONISATION.md
goto menu

:html
cls
echo ▶️  Ouverture de la page HTML...
start "" INDEX.html
goto menu

:status
cls
echo ▶️  État Git...
"C:\Program Files\Git\bin\git.exe" status
echo.
pause
goto menu

:quit
cls
echo 👋 Au revoir!
echo.
pause
exit /b 0

