from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from properties.models import Property, PropertyImages, PropertyOffers, PropertyAmenity
from core.serializers import AmenityOptionSerializer
from properties.enums import MobileState


class PropertyImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PropertyImages
        fields = ["id", "image_url"]


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
    new_images = PropertyImageSerializer(many=True, partial=True, required=False)
    deleted_images = PropertyImageSerializer(many=True, partial=True, required=False)

    class Meta:
        model = Property
        fields = [
            "id", "images", "offers", "amenities", "owner", "is_active",
            "area", "description", "header", "location", "purpose", "title",
            "number_of_bath", "number_of_bed", "price", "type", "whatsapp_number",
            "is_sold", "new_images", "deleted_images"
        ]

    def update(self, instance, validated_data):
        new_images = validated_data.pop("new_images", [])
        deleted_images = validated_data.pop("deleted_images", [])
        # new_amenities = validated_data.pop("new_amenities", [])
        # deleted_amenities = validated_data.pop("deleted_amenities", [])

        Property.objects.create(**validated_data)

        for image in new_images:
            PropertyImages.objects.create(property=instance, **image)

        for image in deleted_images:
            print(image)
            PropertyImages.objects.filter(id=image.get("id")).delete()

        # for amenity in new_amenities:
        #     PropertyAmenity.objects.create(property=instance, **amenity)
        #
        # for amenity in deleted_amenities:
        #     PropertyAmenity.objects.filter(property=instance, id=amenity["id"]).delete()

        instance.save()

        return instance

