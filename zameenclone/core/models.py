from django.db import models

# Create your models here.


class Amenity(models.Model):
    amenity_name = models.CharField(max_length=50)

    
class AmenityOption(models.Model):
    amenity_type = models.ForeignKey(Amenity, on_delete=models.CASCADE, related_name="amenities")
    amenity_key = models.CharField(max_length=50)

