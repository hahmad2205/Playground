from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from properties.models import Property, PropertyImages, PropertyOffers, PropertyAmenity
from properties.enums import MobileState
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
        amenity_instance = get_object_or_404(AmenityOption, pk=amenity_data.get("option"))
        validated_data["amenity"] = amenity_instance
        property_amenity = super().create(validated_data)
        return property_amenity


class PropertySerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=PropertyImageSerializer(), write_only=True)
    amenities = serializers.ListField(child=PropertyAmenitySerializer(), write_only=True)
    # images = PropertyImageSerializer(many=True, partial=True, required=False)
    # amenities = PropertyAmenitySerializer(many=True, partial=True, required=False)

    class Meta:
        model = Property
        fields = [
            "id", "images", "amenities", "owner", "is_active",
            "area", "description", "header", "location", "purpose", "title",
            "number_of_bath", "number_of_bed", "price", "type", "whatsapp_number",
            "is_sold"
        ]

    def save_images(self, images, property_instance):
        for image in images:
            image["property"] = property_instance.id
            image_serializer = PropertyImageSerializer(data=image)
            if image_serializer.is_valid():
                image_serializer.save()
            else:
                raise serializers.ValidationError(image_serializer.errors)

    def save_amenities(self, amenities, property_instance):
        for amenity_data in amenities:
            amenity_option = amenity_data.pop("amenity")
            data = {
                "property": property_instance.id,
                "amenity": amenity_option,
                **amenity_data
            }
            amenity_serializer = PropertyAmenitySerializer(data=data)
            if amenity_serializer.is_valid():
                amenity_serializer.save()
            else:
                raise serializers.ValidationError(amenity_serializer.errors)

    def create(self, validated_data):
        images = validated_data.pop("images", [])
        amenities = validated_data.pop("amenities", [])

        property_instance = super().create(validated_data)

        self.save_images(images, property_instance)
        self.save_amenities(amenities, property_instance)

        return property_instance

