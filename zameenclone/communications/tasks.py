from django.template.loader import render_to_string
from django.utils import timezone

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage

from properties.models import Property


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
def send_email_on_offer_state_update(instance):
    email_template = render_to_string(
        "communication/offer_state_update.html",
        context={"property_title": instance.property.title, "state": instance.state}
    )
    email_to = [instance.property.owner.email]
    email_data = {
        "email_to": email_to,
        "email_subject": "Your offer's updates",
        "email_body": email_template
    }
    send_email(**email_data)


@shared_task()
def send_email_to_unsold_property_owner():
    unsold_property_owners = (
        Property.objects.active().filter(
            email_sent_date__lte=timezone.now() - timezone.timedelta(days=30)
        ).values("title", "location", "owner__email")
    )

    for unsold_property_owner in unsold_property_owners:
        email_to = [unsold_property_owner["owner__email"]]
        email_template = render_to_string(
            "communication/unsold_property_remainder.html",
            context={
                "property_title": unsold_property_owner.get("title"),
                "property_location": unsold_property_owner.get("location")
            }
        )
        email_data = {
            "email_to": email_to,
            "email_subject": "Listed Property update",
            "email_body": email_template
        }
        send_email(**email_data)
