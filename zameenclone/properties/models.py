from django.db import models

from core.models import AmenityOption
from users.models import User


# Create your models here.


class Property(models.Model):
    property_title = models.CharField(max_length=100)
    property_header = models.CharField(max_length=100)
    property_type = models.CharField(max_length=50)
    property_price = models.PositiveIntegerField()
    property_location = models.CharField(max_length=50)
    number_of_bath = models.PositiveIntegerField()
    number_of_bed = models.PositiveIntegerField()
    property_area = models.CharField(max_length=50)
    listing_purpose = models.CharField(max_length=50)
    description_text = models.TextField()
    whatsapp = models.CharField(max_length=13)
    
    def __str__(self):
        return self.property_title


class PropertyImages(models.Model):
    image_link = models.TextField()
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="property_images")


class PropertyOffers(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="property_offers")
    offer_price = models.PositiveIntegerField()
    offered_to = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="property_offers_to")
    offered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="property_offers_from")

    
class PropertyAmenity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_amenities')
    amenity_option = models.ForeignKey(AmenityOption, on_delete=models.CASCADE, related_name='property_amenities')
    property_amenity_key = models.CharField(max_length=50)
