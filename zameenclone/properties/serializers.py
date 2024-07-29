from django.db import transaction
from rest_framework import serializers

from properties.models import Property, PropertyImages, PropertyOffers, PropertyAmenity
from properties.utils import save_images, save_amenities
from properties.enums import MobileState
from core.serializers import AmenityOptionSerializer
from users.models import User


class PropertyImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PropertyImages
        fields = ["id", "image_url", "property"]


class PropertyOfferUpdateSerializer(serializers.ModelSerializer):
    state = serializers.ChoiceField(
        choices=[MobileState.ACCEPTED, MobileState.REJECTED]
    )

    class Meta:
        model = PropertyOffers
        fields = ["id", "state"]

    def update(self, instance, validated_data):
        state = validated_data.get("state")
        instance.mark_accepted() if state == MobileState.ACCEPTED else instance.mark_rejected()
        instance.save(update_fields=["state", "modified"])
        return instance


class PropertyOfferWithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyOffers
        fields = ["id", "is_active"]

    def update(self, instance, validated_data):
        instance.is_active = False
        return super().update(instance, validated_data)


class PropertyOfferListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyOffers
        fields = ["id", "price", "offered_by", "property", "is_active", "state"]


class PropertyOfferSerializer(serializers.ModelSerializer):
    property = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.active()
    )
    offered_by = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.filter(is_active=True),
    )

    class Meta:
        model = PropertyOffers
        fields = ["id", "price", "offered_by", "property", "is_active", "state"]


class PropertyAmenityCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyAmenity
        fields = ["id", "amenity", "value", "property"]


class PropertyAmenitySerializer(serializers.ModelSerializer):
    amenity = AmenityOptionSerializer()

    class Meta:
        model = PropertyAmenity
        fields = ["id", "amenity", "value", "property"]
        read_only_fields = ["property", "amenity"]


class PropertyDetailSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True)
    amenities = PropertyAmenitySerializer(many=True)
    offers = PropertyOfferSerializer(many=True)
    owner = serializers.CharField(source="owner.get_full_name")
    offer_count = serializers.IntegerField()

    class Meta:
        model = Property
        fields = [
            "id", "images", "amenities", "owner", "is_active", "offers",
            "area", "description", "header", "location", "purpose", "title",
            "number_of_bath", "number_of_bed", "price", "type", "whatsapp_number",
            "is_sold", "offer_count"
        ]


class PropertyListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    amenities = PropertyAmenitySerializer(many=True)
    offers = PropertyOfferSerializer(many=True)
    owner = serializers.CharField(source="owner.get_full_name")
    offer_count = serializers.IntegerField()

    class Meta:
        model = Property
        fields = [
            "id", "amenities", "owner", "is_active", "offers",
            "area", "description", "header", "location", "purpose", "title",
            "number_of_bath", "number_of_bed", "price", "type", "whatsapp_number",
            "is_sold", "offer_count", "image_url"
        ]

    def get_image_url(self, obj):
        image = obj.images.first()
        return image.image_url if image else None


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

