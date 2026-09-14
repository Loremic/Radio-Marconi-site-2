from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app)

# Configurazione Server Email
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "la-tua-email-radio@gmail.com"
SENDER_PASSWORD = "la-tua-app-password"

# Indirizzi del direttivo e capi reparto da avvisare in caso di allarme
EMAIL_DIRETTIVO = [
    "direttivo@radiomarconi.it",
    "capo.regia@radiomarconi.it",
    "capo.speaker@radiomarconi.it"
]

def invia_email_notifica(destinatario, nome_utente):
    try:
        messaggio = MIMEMultipart('alternative')
        messaggio['From'] = SENDER_EMAIL
        messaggio['To'] = destinatario
        messaggio['Subject'] = "🔒 Notifica di Accesso - Radio Marconi"

        # Link che il direttivo/utente può cliccare per inviare la segnalazione
        # (può puntare a una pagina del sito o alla rotta del server)
        link_allarme = f"http://127.0.0.1:5000/segnala-intrusione-link?email={destinatario}"

        # Corpo email in versione HTML con pulsante rosso d'emergenza
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #1c1c1e; background-color: #f7f9f8; padding: 20px;">
            <div style="max-width: 500px; margin: 0 auto; background: #ffffff; border-radius: 16px; border: 1px solid #e5e7eb; padding: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                <h2 style="color: #2e7d32; font-family: Georgia, serif; margin-top: 0;">Radio Marconi</h2>
                <p style="font-size: 15px;">Ciao <strong>{nome_utente}</strong>,</p>
                <p style="font-size: 14px; color: #4b5563;">
                    È stato appena effettuato un nuovo accesso all'<strong>Area Riservata</strong> con il tuo account.
                </p>
                
                <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">
                
                <div style="background-color: #fff5f5; border: 1px solid #fed7d7; border-radius: 12px; padding: 16px; text-align: center;">
                    <p style="font-size: 13px; color: #c53030; font-weight: bold; margin-bottom: 10px;">
                        ⚠️ Non sei stato tu ad accedere?
                    </p>
                    <p style="font-size: 12px; color: #742a2a; margin-bottom: 14px;">
                        Se sospetti una fuga di dati o un'intrusione non autorizzata, avvisa subito il Direttivo e i Capi Reparto premendo il pulsante sottostante:
                    </p>
                    <a href="{link_allarme}" target="_blank" style="display: inline-block; background-color: #e53e3e; color: #ffffff; text-decoration: none; font-weight: bold; font-size: 13px; padding: 10px 18px; border-radius: 8px; box-shadow: 0 2px 6px rgba(229,62,62,0.3);">
                        🚨 SEGNALA INTRUSIONE AL DIRETTIVO
                    </a>
                </div>
                
                <p style="font-size: 11px; color: #a0aec0; text-align: center; margin-top: 24px;">
                    &copy; Radio Marconi - I.I.S. Guglielmo Marconi
                </p>
            </div>
        </body>
        </html>
        """

        messaggio.attach(MIMEText(html_content, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(messaggio)
        server.quit()
        return True
    except Exception as e:
        print(f"Errore invio email: {e}")
        return False

# Rotta per gestire il clic sul pulsante rosso dell'email
@app.route('/segnala-intrusione-link', methods=['GET'])
def segnala_intrusione_link():
    email_vittima = request.args.get('email', 'Sconosciuta')
    
    # Invio allarme immediato al direttivo
    try:
        messaggio = MIMEMultipart()
        messaggio['From'] = SENDER_EMAIL
        messaggio['To'] = ", ".join(EMAIL_DIRETTIVO)
        messaggio['Subject'] = "🚨 ALLARME INTENSO: Segnalazione abuso da Email"

        corpo = f"""ATTENZIONE DIRETTIVO E CAPI REPARTO,

L'utente con email '{email_vittima}' ha appena cliccato sul pulsante di allarme nell'email di notifica.

Azione richiesta:
1. Verificare l'accesso recente all'Area Riservata.
2. Disattivare o resettare il codice identificativo di {email_vittima}.
3. Verificare eventuali fughe di dati dal sistema.

--
Sistema Automatico di Sicurezza - Radio Marconi
"""
        messaggio.attach(MIMEText(corpo, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(messaggio)
        server.quit()

        return """
        <body style="font-family: sans-serif; text-align: center; padding: 50px; background: #fff5f5;">
            <h1 style="color: #c53030;">🚨 Segnalazione Inviata con Successo!</h1>
            <p>Il Direttivo e i Capi Reparto sono stati informati immediatamente dell'accesso sospetto.</p>
            <p>Prenderemo in carico la verifica del tuo account il prima possibile.</p>
        </body>
        """
    except Exception as e:
        return f"Errore durante l'invio dell'allarme: {e}"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', '').strip().lower()
    codice = data.get('code', '').strip()

    # Controllo temporaneo
    if email == "mario.rossi@marconi.it" and codice == "MAR123":
        invia_email_notifica(email, "Mario Rossi")
        return jsonify({"success": True, "redirect": "https://google.com"})
    else:
        return jsonify({"success": False, "message": "Email o codice identificativo non corretti."})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
