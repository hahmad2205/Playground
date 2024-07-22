from django.shortcuts import get_object_or_404

from django.db import transaction
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
        amenity = get_object_or_404(AmenityOption, pk=amenity_data.get("option"))
        validated_data["amenity"] = amenity
        property_amenity = super().create(validated_data)
        return property_amenity
    

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


class PropertyImagesAmenitiesUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    is_active = serializers.BooleanField()

    def update(self, instance, validated_data):
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class PropertyUpdateSerializer(serializers.ModelSerializer):
    new_images = serializers.ListField(child=serializers.URLField(), required=False)
    deleted_images = serializers.ListField(child=serializers.IntegerField(), required=False)
    new_amenities = serializers.ListField(child=PropertyAmenitySerializer(), required=False)
    deleted_amenities = serializers.ListField(child=serializers.IntegerField(), required=False)

    class Meta:
        model = Property
        fields = [
            "id", "new_images", "deleted_images", "new_amenities", "deleted_amenities", "owner",
            "is_active", "area", "description", "header", "location", "purpose", "title", "number_of_bath",
            "number_of_bed", "price", "type", "whatsapp_number", "is_sold"
        ]

    def save_images(self, images, property):
        image_instances = [
            {"property": property.id, "image_url": image}
            for image in images
        ]

        image_serializer = PropertyImageSerializer(data=image_instances, many=True)
        if image_serializer.is_valid(raise_exception=True):
            image_serializer.save()

    def save_amenities(self, amenities, property):
        amenity_instances = []
        for amenity_data in amenities:
            amenity_option = amenity_data.pop("amenity")
            amenity_instances.append(
                {
                    "property": property.id,
                    "amenity": amenity_option,
                    **amenity_data
                }
            )

        amenity_serializer = PropertyAmenitySerializer(data=amenity_instances, many=True)
        if amenity_serializer.is_valid(raise_exception=True):
            amenity_serializer.save()

    def update(self, instance, validated_data):
        new_images = validated_data.pop("new_images", [])
        deleted_images = validated_data.pop("deleted_images", [])
        new_amenities = validated_data.pop("new_amenities", [])
        deleted_amenities = validated_data.pop("deleted_amenities", [])

        with transaction.atomic():
            super().create(validated_data)
            self.save_images(new_images, instance)
            self.save_amenities(new_amenities, instance)
            for image in deleted_images:
                image_serializer = PropertyImagesAmenitiesUpdateSerializer(
                    instance=get_object_or_404(PropertyImages, pk=image, property=instance),
                    data={"is_active": False}
                )
                if image_serializer.is_valid(raise_exception=True):
                    image_serializer.save()

            for amenity in deleted_amenities:
                amenity_serializer = PropertyImagesAmenitiesUpdateSerializer(
                    instance=get_object_or_404(PropertyAmenity, pk=amenity, property=instance),
                    data={"is_active": False}
                )
                if amenity_serializer.is_valid(raise_exception=True):
                    amenity_serializer.save()

        return instance

