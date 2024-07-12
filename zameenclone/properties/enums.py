from django.db import models
from django.utils.translation import gettext_lazy as _

class MobileState(models.TextChoices):
    PENDING = 'pending', _('Pending')
    ACCEPTED = 'accepted', _('Accepted')
    REJECTED = 'rejected', _('Rejected')