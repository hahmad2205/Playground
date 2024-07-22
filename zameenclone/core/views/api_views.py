from django.shortcuts import get_list_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import Amenity, AmenityOption
from core.serializers import AmenitySerializer, AmenityOptionSerializer


class AmenityListAPIView(APIView):
    def get(self, request):
        amenity = get_list_or_404(Amenity, is_active=True)
        serializer = AmenitySerializer(amenity, many=True)
        return Response({"amenities": serializer.data})


class AmenityOptionListAPIView(APIView):
    def get(self, request, id):
        amenity_option = get_list_or_404(AmenityOption, amenity=id, is_active=True)
        serializer = AmenityOptionSerializer(amenity_option, many=True)
        return Response({"amenity_options": serializer.data})

