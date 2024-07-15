from rest_framework import serializers

from .models import Property, PropertyImages, PropertyOffers, PropertyAmenity
from core.serializers import AmenityOptionSerializer


class PropertyImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PropertyImages
        fields = ["id", "image_url"]


class PropertyOfferSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PropertyOffers
        fields = ["id", "price", "offered_by"]


class PropertyAmenitySerializer(serializers.ModelSerializer):
    amenity = AmenityOptionSerializer()
    
    class Meta:
        model = PropertyAmenity
        fields = ["id", "amenity", "value"]
    

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True)
    offers = PropertyOfferSerializer(many=True)
    amenities = PropertyAmenitySerializer(many=True)
    owner = serializers.CharField(source="owner.get_full_name")
    
    class Meta:
        model = Property
        fields = [
            "id", "images", "offers", "amenities", "owner", "is_active",
            "area", "description", "header", "location", "purpose", "title",
            "number_of_bath", "number_of_bed", "price", "type", "whatsapp_number",
            "is_sold"
        ]

