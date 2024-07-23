from rest_framework import serializers

from .models import Amenity, AmenityOption


class AmenitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Amenity
        fields = ["id", "name"]


class AmenityOptionSerializer(serializers.ModelSerializer):    
    amenity = serializers.SlugRelatedField(queryset=Amenity.objects.all(), slug_field="name")
    
    class Meta:
        model = AmenityOption
        fields = ["id", "amenity", "option"]

