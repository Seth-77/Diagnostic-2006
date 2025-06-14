import ttkbootstrap as tk
from tkinter import messagebox
from logic import (
    determine_disease,
    save_to_csv,
    crypter_csv,
    load_key,
    delete_temp_file,
    decrypter_csv,
    load_options_from_file,
    resource_path,
    generate_key,
)
import os

LBL_FONT = ("Cambria", 16)
MENU_FONT = ("Calibri", 13)

entry_nom = entry_prenom = entry_age = entry_sex = None
symptome1 = symptome2 = symptome3 = None
entry_login = entry_password = admin_win = diag_win = None


def build_app() -> tk.Window:
    """
    Crée et configure la fenêtre principale de l'application.

    :return: Fenêtre Tkinter principale
    """
    global root
    root = tk.Window(title="Diagnostic 2006", themename="vapor", size=(500, 385))
    build_welcome_message(root)
    build_name_surname(root)
    build_age_sex(root)
    build_symptoms(root)
    build_send(root)
    build_consent_message(root)
    build_admin_button(root)
    root.position_center()
    return root


def build_welcome_message(parent):
    frame = tk.Frame(parent)
    frame.pack(pady=10, fill="x")
    lbl_message = tk.Label(
        frame,
        text="Veuillez remplir vos coordonnées et choisir trois symptômes",
        font=("Calibri", 12),
        justify="center",
        wraplength=400,
    )
    lbl_message.pack()


def build_name_surname(parent):
    """
    Construit la section nom et prénom de l'interface.

    :param parent: Conteneur parent (fenêtre principale)
    """
    global entry_nom, entry_prenom
    frame = tk.Frame(parent)
    frame.pack(pady=10, fill="x")

    lblnom = tk.Label(frame, text="Nom")
    lblnom.grid(row=0, column=0, sticky="w", padx=5)
    entry_nom = tk.Entry(frame)
    entry_nom.grid(row=0, column=1, sticky="ew", padx=5)

    lblprenom = tk.Label(frame, text="Prénom")
    lblprenom.grid(row=0, column=2, sticky="w", padx=5)
    entry_prenom = tk.Entry(frame)
    entry_prenom.grid(row=0, column=3, sticky="ew", padx=5)

    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(3, weight=1)


def build_age_sex(parent):
    """
    Construit la section âge et sexe de l'interface.

    :param parent: Conteneur parent (fenêtre principale)
    """
    global entry_age, entry_sex
    frame = tk.Frame(parent)
    frame.pack(pady=10, fill="x")

    lblage = tk.Label(frame, text="Âge")
    lblage.grid(row=0, column=0, sticky="w", padx=5)
    entry_age = tk.Entry(frame)
    entry_age.grid(row=0, column=1, sticky="ew", padx=5)

    lblsex = tk.Label(frame, text="Sexe")
    lblsex.grid(row=0, column=2, sticky="w", padx=5)
    entry_sex = tk.Combobox(
        frame, values=["Homme", "Femme", "Non-Defini"], state="readonly"
    )
    entry_sex.grid(row=0, column=3, sticky="ew", padx=5)

    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(3, weight=1)


def build_symptoms(parent):
    """
    Construit la section des symptômes avec comboboxes dépendantes.

    :param parent: Conteneur parent (fenêtre principale)
    """
    global symptome1, symptome2, symptome3, all_symptoms

    frame = tk.Frame(parent)
    frame.pack(pady=10, fill="x")

    all_symptoms = load_options_from_file("symptom.txt")

    def update_symptoms_options(event=None):
        selected_1 = symptome1.get()
        selected_2 = symptome2.get()
        selected_3 = symptome3.get()

        values_1 = [s for s in all_symptoms if s not in [selected_2, selected_3]]
        values_2 = [s for s in all_symptoms if s not in [selected_1, selected_3]]
        values_3 = [s for s in all_symptoms if s not in [selected_1, selected_2]]

        symptome1.configure(values=values_1)
        symptome2.configure(values=values_2)
        symptome3.configure(values=values_3)

    lbl1 = tk.Label(frame, text="Symptome 1", font=("Calibri", 10, "bold"))
    lbl1.grid(row=0, column=0, sticky="w", pady=5, padx=5)
    symptome1 = tk.Combobox(frame, values=all_symptoms, state="readonly")
    symptome1.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
    symptome1.bind("<<ComboboxSelected>>", update_symptoms_options)

    lbl2 = tk.Label(frame, text="Symptome 2", font=("Calibri", 10, "bold"))
    lbl2.grid(row=1, column=0, sticky="w", pady=5, padx=5)
    symptome2 = tk.Combobox(frame, values=all_symptoms, state="readonly")
    symptome2.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
    symptome2.bind("<<ComboboxSelected>>", update_symptoms_options)

    lbl3 = tk.Label(frame, text="Symptome 3", font=("Calibri", 10, "bold"))
    lbl3.grid(row=2, column=0, sticky="w", pady=5, padx=5)
    symptome3 = tk.Combobox(frame, values=all_symptoms, state="readonly")
    symptome3.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
    symptome3.bind("<<ComboboxSelected>>", update_symptoms_options)

    frame.columnconfigure(1, weight=1)


def build_send(parent):
    """
    Crée les boutons Envoyer et Annuler.

    :param parent: Conteneur parent (fenêtre principale)
    """
    frame = tk.Frame(parent)
    frame.pack(pady=10)

    send_button = tk.Button(
        frame, bootstyle="success", text="Envoyer", width=15, command=send_info
    )
    send_button.grid(row=0, column=0, padx=10)

    cancel_button = tk.Button(
        frame, bootstyle="warning", text="Réinitialiser", width=15, command=clear_fields
    )
    cancel_button.grid(row=0, column=1, padx=10)

    close_button = tk.Button(
        frame, bootstyle="danger", text="Fermer", width=15, command=root.quit
    )
    close_button.grid(row=0, column=2, padx=10)


def clear_fields():
    """
    Efface les champs du formulaire utilisateur.
    """
    entry_nom.delete(0, tk.END)
    entry_prenom.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_sex.set("")
    symptome1.set("")
    symptome2.set("")
    symptome3.set("")


def build_admin_button(parent):
    """
    Crée le bouton d’accès à l’interface administrateur.

    :param parent: Conteneur parent (fenêtre principale)
    """
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)

    admin_button = tk.Button(
        frame, text="Admin 🔒", bootstyle="dark", command=open_admin_win
    )
    admin_button.pack(side="bottom", anchor="e", padx=5, pady=5)


def build_consent_message(parent):
    """
    Crée et affiche un message de consentement.
    """
    frame = tk.Frame(parent)
    frame.pack()

    lbl = tk.Label(
        frame, text="En cliquant sur Envoyer, vous acceptez la collecte de donnée"
    )
    lbl.pack()


def open_admin_win():
    """
    Ouvre la fenêtre administrateur pour l'accès au CSV déchiffré.
    """
    global entry_login, entry_password, admin_win
    if admin_win is not None and admin_win.winfo_exists():
        admin_win.lift()
        return

    admin_win = tk.Toplevel()
    admin_win.protocol(
        "WM_DELETE_WINDOW", lambda: (delete_temp_file(), admin_win.destroy())
    )
    admin_win.title("Admin panel")
    admin_win.resizable(False, False)
    admin_win.attributes("-topmost", True)
    admin_win.position_center()

    frame = tk.Frame(admin_win)
    frame.pack(pady=10)

    lbl = tk.Label(frame, text="Interface administrateur", font=("Calibri", 18, "bold"))
    lbl.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

    login_label = tk.Label(frame, text="Identifiant", font=("Calibri", 12))
    login_label.grid(row=1, column=0, pady=5, padx=5)
    entry_login = tk.Entry(frame)
    entry_login.grid(row=2, column=0, pady=5, padx=5)

    password_label = tk.Label(frame, text="Mot de passe", font=("Calibri", 12))
    password_label.grid(row=1, column=1, pady=5, padx=5)
    entry_password = tk.Entry(frame, show="*")
    entry_password.grid(row=2, column=1, pady=5, padx=5)

    login_button = tk.Button(
        frame, text="Connexion", bootstyle="primary", command=check_user
    )
    login_button.grid(row=3, column=0, pady=5, padx=5)

    btn_fermer = tk.Button(
        frame, text="Fermer", command=two_actions, bootstyle="secondary"
    )
    btn_fermer.grid(row=3, column=1, pady=5, padx=5)


def two_actions():
    """
    Ferme la fenêtre admin et supprime le fichier temporaire.
    """
    admin_win.destroy()
    delete_temp_file()


def check_user():
    """
    Vérifie les identifiants de l'admin et ouvre le fichier CSV déchiffré.
    """
    username = entry_login.get().strip()
    password = entry_password.get().strip()

    if username == "admin" and password == "1234":
        try:
            cle = load_key()
            decrypter_csv("Patients_info_crypte.csv", "Patients_info_decrypte.csv", cle)
            os.startfile("Patients_info_decrypte.csv")
        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Impossible de décrypter ou d’ouvrir le fichier :\n{e}",
                parent=admin_win,
            )
    else:
        messagebox.showerror(
            "Accès refusé", "Identifiants incorrects.", parent=admin_win
        )


def send_info():
    """
    Récupère les infos du formulaire, diagnostique, enregistre, chiffre et affiche.
    """
    nom = entry_nom.get().strip()
    prenom = entry_prenom.get().strip()
    age = entry_age.get().strip()
    sexe = entry_sex.get().strip()
    s1 = symptome1.get().strip()
    s2 = symptome2.get().strip()
    s3 = symptome3.get().strip()

    if not nom:
        messagebox.showerror("Erreur", "Le champ 'Nom' est obligatoire.")
        return
    if not prenom:
        messagebox.showerror("Erreur", "Le champ 'Prénom' est obligatoire.")
        return
    if not age:
        messagebox.showerror("Erreur", "Le champ 'Âge' est obligatoire.")
        return
    if not age.isdigit():
        messagebox.showerror("Erreur", "Le champ 'Âge' doit être un nombre.")
        return

    age_int = int(age)
    if not (0 < age_int <= 123):
        messagebox.showerror(
            "Erreur",
            "L'âge doit être compris entre 1 et 123 ans.\nSi tu as plus de 123 ans, pense à t'inscrire au Guinness World Records.",
        )
        return

    if not sexe:
        messagebox.showerror("Erreur", "Le champ 'Sexe' est obligatoire.")
        return
    if not s1:
        messagebox.showerror("Erreur", "Veuillez sélectionner le symptôme 1.")
        return
    if not s2:
        messagebox.showerror("Erreur", "Veuillez sélectionner le symptôme 2.")
        return
    if not s3:
        messagebox.showerror("Erreur", "Veuillez sélectionner le symptôme 3.")
        return

    maladie = determine_disease([s1, s2, s3])
    data = [nom, prenom, age, sexe, s1, s2, s3, maladie]
    save_to_csv(data)
    generate_key()
    cle = load_key()
    crypter_csv("Patients_info.csv", "Patients_info_crypte.csv", cle)
    show_diagnostic(maladie)


def show_diagnostic(maladie):
    """
    Affiche une fenêtre avec le diagnostic et le médicament proposé.

    :param maladie: Nom de la maladie détectée
    """
    global diag_win
    if diag_win is not None and diag_win.winfo_exists():
        diag_win.lift()
        return
    diag_win = tk.Toplevel(size=(500, 350))
    diag_win.title("Diagnostic")
    diag_win.resizable(False, False)
    diag_win.position_center()

    frame = tk.Frame(diag_win, padding=20)
    frame.pack(fill="both", expand=True)

    label1 = tk.Label(
        frame,
        text=f"Diagnostic probable :\n\n{maladie}",
        font=("Calibri", 14),
        justify="center",
        wraplength=400,
    )
    label1.pack(pady=(0, 15))

    medicament = "Aucun médicament recommandé"
    with open(resource_path("medicaments.txt"), "r", encoding="utf-8") as f:
        for ligne in f:
            if "=" in ligne:
                nom_maladie, medoc = ligne.strip().split("=", 1)
                if nom_maladie.strip().lower() == maladie.lower():
                    medicament = medoc
                    break

    label_med = tk.Label(
        frame,
        text=f"Médicament conseillé :\n\n{medicament}",
        font=(
            "Calibri",
            14,
        ),
        justify="center",
        wraplength=400,
    )
    label_med.pack(pady=(0, 15))

    label2 = tk.Label(
        frame,
        text="⚠️ ATTENTION ⚠️ \n Ceci est un diagnostic approximatif, il ne remplace pas la consultation d'un médecin.",
        font=("Calibri", 14),
        justify="center",
        wraplength=400,
    )
    label2.pack(pady=(0, 10))

    btn_fermer = tk.Button(
        frame, text="Fermer", command=diag_win.destroy, bootstyle="secondary"
    )
    btn_fermer.pack()
