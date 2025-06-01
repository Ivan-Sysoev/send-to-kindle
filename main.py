import os
import sys
from convert_to_epub import convert_to_epub
from send_by_SMTP import send_to_kindle 
from dotenv import load_dotenv

if len(sys.argv) < 3:
    print(f"Usage: python {os.path.basename(__file__)} <kindle_email> <epub_file_path>")
    sys.exit(1)

kindle_email = sys.argv[1]
epub_path = sys.argv[2]

load_dotenv()
sender_email = os.getenv("EMAIL")
sender_app_password = os.getenv("PASSWORD")

if sender_email is None or sender_app_password is None:
    raise ValueError("[!] EMAIL and PASSWORD environment variables must be set")
    
try:
    epub_path = convert_to_epub(epub_path)
    with open(epub_path, 'rb') as f:
        epub_bytes = f.read()
    send_to_kindle(epub_bytes, filename=epub_path.split('/')[-1], kindle_email=kindle_email,
                   sender_email=sender_email, sender_app_password=sender_app_password)
    print(f"Successfully sent '{epub_path}' to {kindle_email}")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(0)

