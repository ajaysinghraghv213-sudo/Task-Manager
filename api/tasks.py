
from celery import shared_task
from django.core.mail import send_mail
@shared_task
def send_email_task(subject,message,recipient):
    send_mail(
        subject,
        message,
        'ajaysinghraghv213@gmail.com',
        recipient
    )

