from django.db import models
from django_extensions.db.models import TimeStampedModel

from core.models import AmenityOption
from users.models import User

class Property(TimeStampedModel):
    area = models.CharField(max_length=255)
    description_text = models.TextField()
    header = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    listing_purpose = models.CharField(max_length=255)
    number_of_bath = models.PositiveIntegerField()
    number_of_bed = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    whatsapp = models.CharField(max_length=13)
    
    def __str__(self):
        return self.title


class PropertyImages(TimeStampedModel):
    image_link = models.TextField()
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="property_images")
    
    def __str__(self):
        return self.property.title


class PropertyOffers(TimeStampedModel):
    offer_price = models.PositiveIntegerField()
    
    offered_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offers_received")
    offered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offers_made")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="property_offers")
    
    def __str__(self):
        return f"{self.property.title} - {self.offer_price}"


class PropertyAmenity(TimeStampedModel):
    value = models.PositiveIntegerField()
    
    key = models.ForeignKey(AmenityOption, on_delete=models.CASCADE, related_name='amenity_options')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_amenities')

    def __str__(self):
        return f"{self.property.title} - {self.key.key}: {self.value}"

