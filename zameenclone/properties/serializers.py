from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from properties.models import Property, PropertyImages, PropertyOffers, PropertyAmenity
from core.serializers import AmenityOptionSerializer
from properties.enums import MobileState


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImages
        fields = ["id", "image_url"]


class PropertyImagesDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImages
        fields = ["id"]


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


class PropertyUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ["id", "title", "description", "property_type", "purpose", "price", "area", "area_unit", "bedrooms", "bathrooms", "kitchens", "floors", "address", "city", "latitude", "longitude", "is_active", "is_verified", "is_featured", "is_premium", "is_deleted", "created_at", "updated_at", "created_by", "updated_by", "property_images", "property_offers", "property_amenities",
        ]