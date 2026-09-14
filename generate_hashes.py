import json
import random
import re
import bcrypt

MEMBRI_FILE = "membri.json"

def extract_letters_from_email(email):
    """
    Estrae le prime 3 lettere dal nome/cognome nell'email (es. mario.rossi@... -> mar).
    Se l'email ha meno di 3 lettere prima della '@', completa con 'x'.
    """
    username = email.split('@')[0]
    # Rimuove numeri e caratteri speciali per tenere solo lettere
    letters = re.sub(r'[^a-zA-Z]', '', username)
    
    if len(letters) >= 3:
        return letters[:3].lower()
    else:
        # Se ci sono meno di 3 lettere, aggiunge 'x' di riempimento
        return (letters + "xxx")[:3].lower()

def generate_code_and_hash():
    try:
        with open(MEMBRI_FILE, "r", encoding="utf-8") as f:
            members = json.load(f)

        updated = False

        for member in members:
            email = member.get("email", "")
            if not email:
                continue

            # Genera il codice e l'hash solo se la password o l'hash non sono ancora stati definiti
            if not member.get("password") and not member.get("password_hash"):
                # 1. Estrae 3 lettere dall'email
                letters = extract_letters_from_email(email)
                
                # 2. Genera 4 numeri casuali
                numbers = f"{random.randint(0, 9999):04d}"
                
                # 3. Codice finale (3 lettere + 4 numeri)
                generated_password = f"{letters}{numbers}"
                
                # 4. Calcolo Hash con bcrypt
                hashed_bytes = bcrypt.hashpw(generated_password.encode('utf-8'), bcrypt.gensalt())
                
                # 5. Salva sia la password generata che l'hash nel JSON
                member["password"] = generated_password
                member["password_hash"] = hashed_bytes.decode('utf-8')
                
                updated = True
                print(f"[+] Generato per {email}: Password = {generated_password}")

        if updated:
            with open(MEMBRI_FILE, "w", encoding="utf-8") as f:
                json.dump(members, f, indent=4, ensure_ascii=False)
            print("\n[SUCCESS] 'membri.json' aggiornato con successo.")
        else:
            print("\n[INFO] Nessun nuovo membro da aggiornare.")

    except FileNotFoundError:
        print(f"[ERRORE] Il file '{MEMBRI_FILE}' non esiste.")
    except Exception as e:
        print(f"[ERRORE] Si è verificato un problema: {e}")

if __name__ == "__main__":
    generate_code_and_hash()
