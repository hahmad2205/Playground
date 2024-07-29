from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from sendgrid.helpers.mail import Mail


@shared_task()
def send_email(to_email, subject, body):
    email = EmailMessage(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to_email,
        subject=subject,
        body=body
    )

    try:
        email.send()
    except Exception as e:
        return e
