from django.template.loader import render_to_string

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage


def send_email(**kwargs):
    email = EmailMessage(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=kwargs.get("email_to"),
        subject=kwargs.get("email_subject"),
        body=kwargs.get("email_body")
    )

    try:
        email.send()
    except Exception as e:
        return e


@shared_task()
def send_email_on_offer(instance, state):
    email_template = render_to_string(
        "communication/offer_state_update.html",
        context={"property_title": instance.property.title, "state": state}
    )
    email_data = {
        "email_to": [instance.property.owner.email],
        "email_subject": "Your offer's updates",
        "email_body": email_template
    }
    send_email(**email_data)

    pass
