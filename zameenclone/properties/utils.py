from rest_framework.exceptions import ValidationError

from properties.enums import MobileState


def save_images(images, property):
    from properties.serializers import PropertyImageSerializer
    image_instances = [
        {"property": property.id, "image_url": image}
        for image in images
    ]

    image_serializer = PropertyImageSerializer(data=image_instances, many=True)
    if image_serializer.is_valid(raise_exception=True):
        image_serializer.save()


def save_amenities(amenities, property):
    from properties.serializers import PropertyAmenityCreateSerializer
    amenity_instances = []
    for amenity_data in amenities:
        amenity_option = amenity_data.pop("amenity")
        amenity_instances.append(
            {
                "property": property.id,
                "amenity": amenity_option.get("option"),
                **amenity_data
            }
        )
    amenity_serializer = PropertyAmenityCreateSerializer(data=amenity_instances, many=True)
    if amenity_serializer.is_valid(raise_exception=True):
        amenity_serializer.save()


def validate_state(value):
    if value not in [MobileState.ACCEPTED, MobileState.REJECTED]:
        raise ValidationError("State can only be set to accepted or rejected.")
    return value

