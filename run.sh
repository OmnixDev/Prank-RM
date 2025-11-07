#!/bin/bash

# run.sh
# Vérifie les privilèges sudo
if [ "$EUID" -ne 0 ]; then
    echo "Ce script doit être exécuté avec sudo."
    echo "Exécutez : sudo bash run.sh"
    exit 1
fi

# Définir le répertoire de travail
cd "$(dirname "$0")"

# Vérifier si Python3 est installé
if ! command -v python3 &> /dev/null; then
    echo "Python3 n'est pas installé. Installation..."
    apt update
    apt install -y python3 python3-pip
fi

# Installer pulseaudio pour le son
if ! command -v paplay &> /dev/null; then
    echo "Installation de pulseaudio-utils pour le son..."
    apt install -y pulseaudio-utils
fi

# Installer Tkinter
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "Installation de python3-tk..."
    apt install -y python3-tk
fi

# Mettre à jour pip
echo "Mise à jour de pip..."
python3 -m pip install --upgrade pip

# Installer les dépendances
if [ -f requirements.txt ]; then
    echo "Installation des dépendances depuis requirements.txt..."
    pip3 install -r requirements.txt
else
    echo "Fichier requirements.txt introuvable."
    exit 1
fi

# Lancer main.py
if [ -f main.py ]; then
    echo "Lancement de main.py..."
    python3 main.py
else
    echo "Fichier main.py introuvable."
    exit 1
fi
