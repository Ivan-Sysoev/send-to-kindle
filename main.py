#!/usr/bin/env python
import os
import sys
from convert_to_epub import convert_to_epub
from send_by_SMTP import send_to_kindle 
from dotenv import load_dotenv

if len(sys.argv) < 2:
    print(f"Usage: python {os.path.basename(__file__)} <epub_file_path>")
    sys.exit(1)

epub_path = sys.argv[1]

load_dotenv()
kindle_email = os.getenv("KINDLE_MAIL")
sender_email = os.getenv("EMAIL")
sender_app_password = os.getenv("PASSWORD")

if sender_email is None or sender_app_password is None or kindle_email is None:
    raise ValueError("[!] EMAIL and PASSWORD environment variables must be set")
    
try:
    epub_path = convert_to_epub(epub_path)
    with open(epub_path, 'rb') as f:
        epub_bytes = f.read()
    
    filename = os.path.basename(epub_path)
    send_to_kindle(epub_bytes, filename=filename, kindle_email=kindle_email,
                   sender_email=sender_email, sender_app_password=sender_app_password)
    print(f"Successfully sent '{epub_path}' to {kindle_email}")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
