from rest_framework import serializers

from .models import Amenity, AmenityOption

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["name"]

class AmenityOptionSerializer(serializers.ModelSerializer):
    amenity = AmenitySerializer(read_only=True)
    
    class Meta:
        model = AmenityOption
        fields = ["amenity", "option"]
