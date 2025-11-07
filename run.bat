@echo off
setlocal EnableDelayedExpansion

:: Vérifier les privilèges administrateur
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Ce script doit etre execute en tant qu'administrateur.
    echo Veuillez faire un clic droit sur run.bat et selectionner "Executer en tant qu'administrateur".
    pause
    exit /b 1
)

:: Définir le répertoire de travail
cd /d "%~dp0"

:: Vérifier si Python est installé
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo Python n'est pas installe. Installation de Python...
    :: Télécharger et installer Python (version 3.12, modifiez si besoin)
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe -OutFile python-installer.exe"
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
)

:: Vérifier si pip est à jour
echo Mise a jour de pip...
python -m pip install --upgrade pip

:: Installer les dépendances depuis requirements.txt
if exist requirements.txt (
    echo Installation des dependances depuis requirements.txt...
    pip install -r requirements.txt
) else (
    echo Fichier requirements.txt introuvable.
    pause
    exit /b 1
)

:: Lancer main.py
if exist main.py (
    echo Lancement de main.py...
    python main.py
) else (
    echo Fichier main.py introuvable.
    pause
    exit /b 1
)

:: Pause pour voir les résultats
pause
