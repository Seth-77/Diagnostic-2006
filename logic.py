import os
import csv
from datetime import datetime
from cryptography.fernet import Fernet
import sys
from tkinter import messagebox

def determine_disease(symptomes):
    symptomes_set = set(symptomes)

    maladies_connues = {}
    with open(resource_path("symptom_maladie.txt"), "r", encoding="utf-8") as f:
        for ligne in f:
            if '=' in ligne:
                partie_symptomes, maladie = ligne.strip().split("=")
                combo = tuple(s.strip() for s in partie_symptomes.split(","))
                maladies_connues[combo] = maladie

    for combo, maladie in maladies_connues.items():
        if set(combo).issubset(symptomes_set):
            return maladie

    return "Maladie inconnue - Veuillez vérifier vos symptômes"

def save_to_csv(data):
    filename = "Patients_info.csv"
    file_exists = os.path.isfile(filename)
    now = datetime.now()
    date_now = now.strftime("%d-%m-%Y")
    time_now = now.strftime("%Hh%M")
    with open(filename, mode="a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        if not file_exists:
            writer.writerow(["Date", "Heure", "Nom", "Prenom", "Age", "Sex", "Symptome 1", "Symptome 2", "Symptome 3", "Maladie"])
        writer.writerow([date_now, time_now] + data)
    if not file_exists and os.name == 'nt':
        import ctypes
        ctypes.windll.kernel32.SetFileAttributesW(filename, 2)

def crypter_csv(fichier_source, fichier_crypte, cle):
    fernet = Fernet(cle)
    with open(fichier_source, 'rb') as f:
        donnees = f.read()
    donnees_cryptees = fernet.encrypt(donnees)
    with open(fichier_crypte, 'wb') as f:
        f.write(donnees_cryptees)

def decrypter_csv(fichier_crypte, fichier_decrypte, cle):
    fernet = Fernet(cle)
    with open(fichier_crypte, 'rb') as f:
        donnees_cryptees = f.read()
    donnees = fernet.decrypt(donnees_cryptees)
    with open(fichier_decrypte, 'wb') as f:
        f.write(donnees)

def load_key():
    with open(resource_path("key.key"), "rb") as f:
        return f.read()
    
def generate_key(filepath="key.key"):
    try:
        if os.path.exists(resource_path(filepath)):
            return
        key = Fernet.generate_key()
        with open(resource_path(filepath), "wb") as key_file:
            key_file.write(key)
    except Exception as e:
        print(f"Erreur lors de la génération de la clé : {e}")
        
def delete_temp_file():
    try:
        if os.path.exists("Patients_info_decrypte.csv"):
            os.remove("Patients_info_decrypte.csv")
    except Exception as e:
        print(f"Erreur lors de la suppression : {e}")


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS 
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_options_from_file(filepath):
    try:
        path = resource_path(filepath)
        with open(path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        messagebox.showerror("Erreur", f"Le fichier {filepath} est introuvable.")
        return []
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de lire {filepath}.\n{e}")
        return []
