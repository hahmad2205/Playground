from properties.serializers import PropertyImageSerializer


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

