import os
import smtplib
import random
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("BOT_EMAIL")
EMAIL_PASSWORD = os.getenv("BOT_EMAIL_PASSWORD")

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    raise ValueError("EMAIL or EMAIL_PASSWORD is not set in environment variables")


def generate_code(length=6):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


def send_verification_code(to_email, code):
    message = MIMEMultipart()
    message["From"] = EMAIL_ADDRESS
    message["To"] = to_email
    message["Subject"] = "Vention Bot: Your Verification Code"

    body = (
        f"Hello!\n\n"
        f"Thank you for registering.\n"
        f"Your verification code is: {code}\n\n"
        f"If you didn't request this, please ignore this message.\n\n"
        f"Best regards,\n"
        f"Vention Bot Team"
    )

    message.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(message)

        logging.info(f"[INFO] Verification code sent to {to_email}")
        return True

    except Exception as e:
        logging.error(f"[ERROR] Failed to send verification code to {to_email}: {e}")
        return False
