from django.db import models
from django.db.models import Prefetch
from django.contrib.auth import get_user_model

import django_filters
from django_fsm import FSMField, transition

from core.models import AmenityOption, SoftdeleteModelMixin

User = get_user_model()

class Property(SoftdeleteModelMixin):
    area = models.PositiveSmallIntegerField()
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
    
    amenities = models.ManyToManyField("properties.PropertyAmenity", related_name="amenities")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="properties", null=True, blank=True)

    def get_first_image(self):
        return self.images.first()
    
    def on_delete(self):
        super().on_delete()
        self.images.all().update(is_active=False)
        self.amenities.all().update(is_active=False)
        self.offers.all().update(is_active=False)
    
    @classmethod
    def get_images_from_properties(cls, properties):
        prefetch_images = Prefetch("images", queryset=PropertyImages.objects.all().order_by("pk"))
        
        return [
            {
                "property": property,
                "image_url": property.images.first().image_url if property.images.first() else None
            }
            for property in cls.objects.prefetch_related(prefetch_images).filter(id__in=[p.id for p in properties])
        ]
    
    def __str__(self):
        return self.title

class PropertyFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    number_of_bed = django_filters.NumberFilter()
    number_of_bed__gt = django_filters.NumberFilter(field_name="number_of_bed", lookup_expr="gt")
    number_of_bed__lt = django_filters.NumberFilter(field_name="number_of_bed", lookup_expr="lt")
    
    number_of_bath = django_filters.NumberFilter()
    number_of_bath__gt = django_filters.NumberFilter(field_name="number_of_bath", lookup_expr="gt")
    number_of_bath__gt = django_filters.NumberFilter(field_name="number_of_bath", lookup_expr="gt")
    
    area = django_filters.NumberFilter()
    area__gt = django_filters.NumberFilter(field_name="area", lookup_expr="gt")
    area__lt = django_filters.NumberFilter(field_name="area", lookup_expr="lt")

    class Meta:
        model = Property
        fields = ["price", "number_of_bed", "number_of_bath", "area"]


class PropertyImages(SoftdeleteModelMixin):
    image_url = models.TextField()
    image = models.FileField()
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    
    def __str__(self):
        return self.property.title


class PropertyOffers(SoftdeleteModelMixin):
    price = models.PositiveIntegerField()
    
    offered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_offers")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="offers")
    state = FSMField(default="pending", protected=True)
    
    def __str__(self):
        return f"{self.property.title} - {self.price}"
    
    @transition(field=state, source="pending", target="accepted")
    def to_state_accepted(self):
        self.property.is_active = False
        return "Offer switched to accepted!"
    
    @transition(field=state, source="pending", target="rejected")
    def to_state_rejected(self):
        return "Offer switched to rejected!"


class PropertyAmenity(SoftdeleteModelMixin):
    value = models.PositiveIntegerField(null=True, blank=True)
    
    amenity = models.ForeignKey(AmenityOption, on_delete=models.CASCADE, related_name="options")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="property_amenities")

    def __str__(self):
        return f"{self.property} | ID: {self.id}"

