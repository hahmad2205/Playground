from django.db import models
from django.db.models import Prefetch
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth import get_user_model

from core.models import AmenityOption

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
    
    amenities = models.ManyToManyField("properties.PropertyAmenity", related_name='amenities')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="properties", null=True, blank=True)

    def get_first_image(self):
        return self.images.first()
    
    @classmethod
    def get_images_from_properties(cls, properties):
        prefetch_images = Prefetch('images', queryset=PropertyImages.objects.all().order_by('pk'))
        
        return [
            {
                "property": property,
                "image_url": property.images.first().image_url if property.images.first() else None
            }
            for property in cls.objects.prefetch_related(prefetch_images).filter(id__in=[p.id for p in properties])
        ]
    
    def __str__(self):
        return self.title
        

class PropertyImages(TimeStampedModel):
    image_url = models.TextField()
    image = models.FileField()
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    
    def __str__(self):
        return self.property.title


class PropertyOffers(TimeStampedModel):
    price = models.PositiveIntegerField()
    
    offered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_offers")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="offers")
    
    def __str__(self):
        return f"{self.property.title} - {self.price}"


class PropertyAmenity(TimeStampedModel):
    value = models.PositiveIntegerField(null=True, blank=True)
    
    amenity = models.ForeignKey(AmenityOption, on_delete=models.CASCADE, related_name='options')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_amenities')

    def __str__(self):
        return f"{self.property} | ID: {self.id}"

