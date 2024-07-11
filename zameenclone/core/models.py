from django.db import models
from django_extensions.db.models import TimeStampedModel

class SoftdeleteModelMixin(TimeStampedModel):
    is_active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True


class Amenity(SoftdeleteModelMixin):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name


class AmenityOption(SoftdeleteModelMixin):
    option = models.CharField(max_length=255)
    
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE, related_name="options")
    
    def __str__(self):
        return self.amenity

