from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_blocked = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.get_full_name()
