import os
import sys
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

def send_to_kindle(epub_bytes: bytes, filename: str, kindle_email: str, sender_email: str, sender_app_password: str):    
    msg = EmailMessage()
    msg['Subject'] = filename
    msg['From'] = sender_email
    msg['To'] = kindle_email
    msg.set_content('')

    msg.add_attachment(epub_bytes, maintype='application', subtype='epub+zip', filename=filename)

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
        smtp.login(sender_email, sender_app_password)
        smtp.send_message(msg)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <kindle_email> <epub_file_path>")
        sys.exit(1)

    kindle_email = sys.argv[1]
    epub_path = sys.argv[2]

    with open(epub_path, 'rb') as f:
        epub_bytes = f.read()

    load_dotenv()

    sender_email = os.getenv("EMAIL")
    sender_app_password = os.getenv("PASSWORD")

    if sender_email is None or sender_app_password is None:
        raise ValueError("[!] EMAIL and PASSWORD environment variables must be set")

    send_to_kindle(epub_bytes, filename=epub_path.split('/')[-1], kindle_email=kindle_email,
                   sender_email=sender_email, sender_app_password=sender_app_password)
