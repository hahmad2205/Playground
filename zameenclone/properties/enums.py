from django.db import models
from django.utils.translation import gettext_lazy as _

class MobileState(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"
