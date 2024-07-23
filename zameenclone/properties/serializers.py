from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from properties.models import Property, PropertyImages, PropertyOffers, PropertyAmenity
from properties.enums import MobileState
from properties.utils import save_images, save_amenities
from core.serializers import AmenityOptionSerializer
from core.models import AmenityOption


class PropertyImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PropertyImages
        fields = ["id", "image_url", "property"]


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
        fields = ["id", "amenity", "value", "property"]

    def create(self, validated_data):
        amenity_data = validated_data.pop('amenity')
        amenity = get_object_or_404(AmenityOption, pk=amenity_data.get("option"))
        validated_data["amenity"] = amenity
        property_amenity = super().create(validated_data)
        return property_amenity


class PropertySerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.URLField(), write_only=True)
    amenities = serializers.ListField(child=PropertyAmenitySerializer(), write_only=True)

    class Meta:
        model = Property
        fields = [
            "id", "images", "amenities", "owner", "is_active",
            "area", "description", "header", "location", "purpose", "title",
            "number_of_bath", "number_of_bed", "price", "type", "whatsapp_number",
            "is_sold"
        ]

    def create(self, validated_data):
        images = validated_data.pop("images", [])
        amenities = validated_data.pop("amenities", [])

        with transaction.atomic():
            property = super().create(validated_data)

            save_images(images, property)
            save_amenities(amenities, property)

        return property

