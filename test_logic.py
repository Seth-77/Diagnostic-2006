import os
import pytest
from logic import (
    determine_disease,
    generate_key,
)

@pytest.fixture
def fake_data():
    return ["Doe", "John", "30", "Homme", "Fievre", "Toux", "Fatigue", "Grippe"]

def test_determine_disease_known_1():
    symptomes = ["Fievre", "Toux", "Fatigue"]
    resultat = determine_disease(symptomes)
    assert resultat.lower() == "grippe"

def test_determine_disease_known_2():
    symptomes = ["Toux", "Fatigue", "Essoufflement"]
    resultat = determine_disease(symptomes)
    assert resultat.lower() == "asthme"

def test_determine_disease_known_3():
    symptomes = ["Fievre", "Maux de tete", "Vomissements"]
    resultat = determine_disease(symptomes)
    assert resultat.lower() == "méningite"

def test_determine_disease_inconnu():
    symptomes = ["Inconnu1", "Inconnu2", "Inconnu3"]
    resultat = determine_disease(symptomes)
    assert "maladie inconnue" in resultat.lower()

def test_generate_and_load_key_manual():
    filepath = "key_test.key"
    if os.path.exists(filepath):
        os.remove(filepath)
    generate_key(filepath=filepath)
    assert os.path.exists(filepath)
    cle = None
    with open(filepath, "rb") as f:
        cle = f.read()
    assert isinstance(cle, bytes)
    os.remove(filepath)

def test_crypter_decrypter_csv(tmp_path):
    fichier_source = tmp_path / "source.csv"
    fichier_crypte = tmp_path / "crypte.csv"
    fichier_decrypte = tmp_path / "decrypte.csv"
    
    contenu = "Nom,Prenom\nAlice,Durand"
    fichier_source.write_text(contenu, encoding='utf-8')
    
    from cryptography.fernet import Fernet
    import logic
    key = Fernet.generate_key()
    
    logic.crypter_csv(str(fichier_source), str(fichier_crypte), key)
    logic.decrypter_csv(str(fichier_crypte), str(fichier_decrypte), key)
    
    contenu_decrypte = fichier_decrypte.read_text(encoding='utf-8')
    assert contenu_decrypte == contenu


def test_save_to_csv(tmp_path, monkeypatch):
    import logic
    fichier = tmp_path / "Patients_info.csv"
    monkeypatch.setattr(logic, "resource_path", lambda x: str(fichier))
    monkeypatch.setattr(logic, "os", __import__("os"))

    old_path = os.path.abspath(".")
    os.chdir(tmp_path)
    logic.save_to_csv(["TestNom", "TestPrenom", "30", "M", "Toux", "Fievre", "Fatigue", "Grippe"])
    os.chdir(old_path)

    assert fichier.exists()
    lignes = fichier.read_text(encoding='utf-8').splitlines()
    assert len(lignes) >= 2

