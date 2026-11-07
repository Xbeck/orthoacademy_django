from django.core.mail import send_mail

from config.celery import app

def send_email(subject, message, recipient_list):
    send_mail(
            subject,
            message,
            "xab60xr@gmail.com",
            recipient_list
    )