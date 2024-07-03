from django.db import models
from django_extensions.db.models import TimeStampedModel

class Amenity(TimeStampedModel):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class AmenityOption(TimeStampedModel):
    option = models.CharField(max_length=255)
    
    type = models.ForeignKey(Amenity, on_delete=models.CASCADE, related_name="options")
    
    def __str__(self):
        return self.key

