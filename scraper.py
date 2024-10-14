import os
import requests
import pandas as pd
import subprocess
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


def load_env_variables():
    """
    Load environment variables from .env file if running locally.
    """
    if os.getenv("GITHUB_ACTIONS") is None:
        load_dotenv()

    # Load email credentials from environment variables
    return {
        'sender_email': os.getenv("SENDER_EMAIL"),
        'sender_password': os.getenv("PASSWORD"),
        'receiver_email': os.getenv("RECEIVER_EMAIL")
    }


def fetch_job_offers(url):
    """
    Fetch job offers from the specified URL and parse the HTML.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    offers = soup.select('table > tbody > tr')  # Corrected selector to `select`
    all_offers_data = []

    for offer in offers:
        parts = offer.getText().strip().split('\n')
        data = {
            'Código': parts[0],
            'Título': parts[1],
            'Responsable': parts[2],
            'Fecha inicio solicitud': parts[3],
            'Fecha fin solicitud': parts[4],
            'Estado': parts[5]
        }
        all_offers_data.append(data)

    return pd.DataFrame(all_offers_data)


def check_new_offers(df, previous_offers_file):
    """
    Compare the current job offers with the previous ones and return new offers.
    """
    try:
        previous_offers = pd.read_csv(previous_offers_file)
    except FileNotFoundError:
        print("No previous offers found, treating all as new.")
        return df, True

    new_offers = df[~df['Código'].isin(previous_offers['Código'])]
    return new_offers, not new_offers.empty


def send_email(new_offers, sender_email, sender_password, receiver_email):
    """
    Send an email notification with the new job offers.
    """
    smtp_server = "smtp.gmail.com"
    smtp_port = 465

    subject = "🚀 UC3M - Nuevas ofertas de trabajo!"
    offers_html = new_offers.to_html(index=False, justify="center", border=1, classes="table table-striped")

    body = f"""
    <html>
    <body>
        <h2 style="color: #2e6c80;">Nuevas ofertas de trabajo! 🎉</h2>
        <p>Hola,</p>
        <p>Se han detectado las siguientes nuevas ofertas de trabajo:</p>
        {offers_html}
        <br>
        <p>Un saludo,<br>Yo mismo</p>
    </body>
    </html>
    """

    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


def save_and_commit_changes(df, previous_offers_file):
    """
    Save the updated offers to the CSV and push changes to GitHub.
    """
    df.to_csv(previous_offers_file, index=False)
    print(f"The CSV file '{previous_offers_file}' has been updated with new offers.")
    git_push()


def git_push():
    """
    Commit and push changes to GitHub.
    """
    subprocess.run(["git", "add", "job_offers.csv"])
    subprocess.run(["git", "commit", "-m", "Update job offers with new data"])
    subprocess.run(["git", "push"])


def main():
    # Load environment variables (email credentials)
    env_vars = load_env_variables()

    # Fetch job offers
    url = "https://aplicaciones.uc3m.es/atenea/publico/1/listarConvocatorias"
    current_offers = fetch_job_offers(url)

    # Check for new offers
    previous_offers_file = 'job_offers.csv'
    new_offers, has_new_offers = check_new_offers(current_offers, previous_offers_file)

    # If new offers are found, notify and update the CSV
    if has_new_offers:
        print("New offers detected:")
        print(new_offers)

        # Send email notification
        send_email(new_offers, env_vars['sender_email'], env_vars['sender_password'], env_vars['receiver_email'])

        # Save new offers to CSV and commit changes to GitHub
        save_and_commit_changes(current_offers, previous_offers_file)
    else:
        print("No new offers detected :(")


if __name__ == "__main__":
    main()