from rest_framework import serializers
from .models import Property, PropertyImages, PropertyOffers, PropertyAmenity

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImages
        fields = ["id", "image_url"]

class PropertyOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyOffers
        fields = ["id", "price", "offered_by"]

class PropertyAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyAmenity
        fields = ["id", "amenity", "value"]
    

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    offers = PropertyOfferSerializer(many=True, read_only=True)
    amenities = PropertyAmenitySerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Property
        fields = "__all__"
