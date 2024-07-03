from django.db import models
from django_extensions.db.models import TimeStampedModel

from core.models import AmenityOption
from django.contrib.auth import get_user_model

User = get_user_model()

class Property(TimeStampedModel):
    area = models.CharField(max_length=255)
    description = models.TextField()
    header = models.TextField()
    location = models.TextField()
    purpose = models.CharField(max_length=255, default="for sale")
    number_of_bath = models.PositiveSmallIntegerField()
    number_of_bed = models.PositiveSmallIntegerField()
    price = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=255, default="house")
    whatsapp_number = models.CharField(max_length=13)
    
    amenities =models.ManyToManyField("properties.PropertyAmenity", related_name='amenities')
    
    
    def __str__(self):
        return self.title


class PropertyImages(TimeStampedModel):
    image_url = models.TextField()
    image = models.FileField()
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    
    def __str__(self):
        return self.property


class PropertyOffers(TimeStampedModel):
    price = models.PositiveIntegerField()
    
    offered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offers_made")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="offers")
    
    def __str__(self):
        return f"{self.property.title} - {self.offer_price}"


class PropertyAmenity(TimeStampedModel):
    value = models.PositiveIntegerField()
    
    amenity = models.ForeignKey(AmenityOption, on_delete=models.CASCADE, related_name='options')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_amenities')

    def __str__(self):
        return f"{self.property.title} - {self.amenity.amenity}: {self.value}"

