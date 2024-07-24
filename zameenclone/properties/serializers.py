from django.shortcuts import get_object_or_404

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from properties.models import Property, PropertyImages, PropertyOffers, PropertyAmenity
from properties.utils import save_images, save_amenities
from properties.enums import MobileState
from core.serializers import AmenityOptionSerializer
from core.models import AmenityOption
from users.serializers import UserSerializer


class PropertyImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PropertyImages
        fields = ["id", "image_url", "property"]


class PropertyOfferUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyOffers
        fields = ["id", "state"]

    def validate(self, attrs):
        state = attrs.get("state")
        if state not in [MobileState.ACCEPTED, MobileState.REJECTED]:
            raise ValidationError("Invalid state value provided.")

        return attrs

    def update(self, instance, validated_data):
        state = validated_data.get("state")
        if state == MobileState.ACCEPTED:
            message = instance.mark_accepted()
        elif state == MobileState.REJECTED:
            message = instance.mark_rejected()
        else:
            raise ValidationError("Invalid state value provided.")

        instance.save(update_fields=['state', 'modified'])
        return instance


class PropertyOfferSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PropertyOffers
        fields = ["id", "price", "offered_by", "property", "is_active", "state"]
        read_only_fields = ["offered_by", "property"]

    def validate(self, attrs):
        property_id = self.context["view"].kwargs.get("id")
        if not property_id:
            raise serializers.ValidationError("Property ID is required.")

        try:
            property = Property.objects.active().get(id=property_id)
        except Property.DoesNotExist:
            raise serializers.ValidationError("Property does not exist or is not available.")

        attrs["property"] = property
        attrs["offered_by"] = self.context.get("request").user

        return attrs


class PropertyAmenitySerializer(serializers.ModelSerializer):
    amenity = AmenityOptionSerializer()

    class Meta:
        model = PropertyAmenity
        fields = ["id", "amenity", "value", "property"]

    def create(self, validated_data):
        amenity_data = validated_data.pop("amenity")
        amenity = get_object_or_404(AmenityOption, pk=amenity_data.get("option"))
        validated_data["amenity"] = amenity
        property_amenity = super().create(validated_data)
        return property_amenity


class PropertyDetailSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True)
    amenities = PropertyAmenitySerializer(many=True)
    offers = PropertyOfferSerializer(many=True)
    owner = UserSerializer()

    class Meta:
        model = Property
        fields = [
            "id", "images", "amenities", "owner", "is_active", "offers",
            "area", "description", "header", "location", "purpose", "title",
            "number_of_bath", "number_of_bed", "price", "type", "whatsapp_number",
            "is_sold"
        ]


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


class PropertyImagesAmenitiesUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    is_active = serializers.BooleanField()

    def update(self, instance, validated_data):
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance


class PropertyUpdateSerializer(serializers.ModelSerializer):
    new_images = serializers.ListField(child=serializers.URLField(), required=False)
    deleted_images = serializers.PrimaryKeyRelatedField(
        queryset=PropertyImages.objects.filter(is_active=True), many=True, required=False
    )
    new_amenities = serializers.ListField(child=PropertyAmenitySerializer(), required=False)
    deleted_amenities = serializers.PrimaryKeyRelatedField(
        queryset=PropertyAmenity.objects.filter(is_active=True), many=True, required=False
    )

    class Meta:
        model = Property
        fields = [
            "id", "new_images", "deleted_images", "new_amenities", "deleted_amenities", "owner",
            "is_active", "area", "description", "header", "location", "purpose", "title", "number_of_bath",
            "number_of_bed", "price", "type", "whatsapp_number", "is_sold"
        ]

    def update(self, instance, validated_data):
        new_images = validated_data.pop("new_images", [])
        deleted_images = validated_data.pop("deleted_images", [])
        new_amenities = validated_data.pop("new_amenities", [])
        deleted_amenities = validated_data.pop("deleted_amenities", [])

        with transaction.atomic():
            super().update(instance, validated_data)
            save_images(new_images, instance)
            save_amenities(new_amenities, instance)

            for image in deleted_images:
                image_serializer = PropertyImagesAmenitiesUpdateSerializer(
                    instance=image,
                    data={"is_active": False}
                )
                if image_serializer.is_valid(raise_exception=True):
                    image_serializer.save()

            for amenity in deleted_amenities:
                amenity_serializer = PropertyImagesAmenitiesUpdateSerializer(
                    instance=amenity,
                    data={"is_active": False}
                )
                if amenity_serializer.is_valid(raise_exception=True):
                    amenity_serializer.save()

        return instance

