from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Amenity(TimeStampedModel):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class AmenityOption(TimeStampedModel):
    key = models.CharField(max_length=50)
    
    type = models.ForeignKey(Amenity, on_delete=models.CASCADE, related_name="options")
    
    def __str__(self):
        return self.key

