import logging
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv('BOT_EMAIL')
EMAIL_PASSWORD = os.getenv("BOT_EMAIL_PASSWORD")


def generate_code(length=6):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def send_verification_code(to_email, code):
    message = MIMEMultipart()
    message["From"] = EMAIL_ADDRESS
    message["To"] = to_email
    message["Subject"] = "Your Verification Code"

    body = f"Your registration verification code is: {code}"
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(message)
            return True

    except Exception as e:
        logging.info(f"[ERROR] Failed to send verification code to {to_email}: {e}")
        return False

