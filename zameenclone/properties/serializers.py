from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from properties.models import Property, PropertyImages, PropertyOffers, PropertyAmenity
from properties.enums import MobileState
from core.serializers import AmenityOptionSerializer
from core.models import AmenityOption


class PropertyImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PropertyImages
        fields = ["image_url"]


class PropertyOfferSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PropertyOffers
        fields = ["id", "price", "offered_by", "property", "is_active", "state"]

    def validate_state(self, value):
        if value not in [MobileState.ACCEPTED, MobileState.REJECTED]:
            raise ValidationError("State can only be set to accepted or rejected.")
        return value


class PropertyAmenitySerializer(serializers.ModelSerializer):
    amenity = AmenityOptionSerializer()
    
    class Meta:
        model = PropertyAmenity
        fields = ["id", "amenity", "value"]
    

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, partial=True, required=False)
    offers = PropertyOfferSerializer(many=True, partial=True, required=False)
    amenities = PropertyAmenitySerializer(many=True, partial=True, required=False)
    
    class Meta:
        model = Property
        fields = [
            "id", "images", "offers", "amenities", "owner", "is_active",
            "area", "description", "header", "location", "purpose", "title",
            "number_of_bath", "number_of_bed", "price", "type", "whatsapp_number",
            "is_sold"
        ]
        
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        amenities_data = validated_data.pop('amenities', [])
        
        property_instance = Property.objects.create(**validated_data)
        
        for image_data in images_data:
            PropertyImages.objects.create(property=property_instance, **image_data)
        
        for amenity_data in amenities_data:
            amenity_option_data = amenity_data.pop('amenity')
            amenity_option, created = AmenityOption.objects.get_or_create(**amenity_option_data)
            PropertyAmenity.objects.create(property=property_instance, amenity=amenity_option, **amenity_data)
        
        return property_instance

