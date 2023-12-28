import os
import sys
from dotenv import load_dotenv
from typing import Dict
import smtplib, ssl

load_dotenv()


def erreur_fatale(code, *msg):
    print(msg, file=sys.stderr)
    send_mail(str(msg), "Erreur Secretary")
    exit(code)


def load_config() -> Dict[str, str]:
    config = {
        'MAIL_USER': os.getenv('MAIL_USER'),
        'MAIL_PASSWORD': os.getenv('MAIL_PASSWORD'),
        'MAIL_HOST': os.getenv('MAIL_HOST'),
        'RECIPIENT': os.getenv('RECIPIENT')
    }
    if config['MAIL_USER'] is None or config['MAIL_PASSWORD'] is None or config['RECIPIENT'] is None\
            or config['MAIL_HOST'] is None :
        print('MAIL_USER ou MAIL_PASSWORD OU RECIPIENT ou MAIL_HOST introuvables', file=sys.stderr)
        exit(1)
    return config


config = load_config()


def send_mail(body: str, subject: str = None) -> bool:
    context = ssl.create_default_context()
    if not subject:
        subject = "Message from your secretary"
    message = f"""From: Secretary <{config['MAIL_USER']}>
Subject: {subject}

{body}
"""
    with smtplib.SMTP_SSL(config['MAIL_HOST'], 465, context=context) as server:
        server.login(config['MAIL_USER'], config['MAIL_PASSWORD'])
        r = server.sendmail(config['MAIL_USER'], config['RECIPIENT'], message.encode())

    print("Message sent")
    return True
