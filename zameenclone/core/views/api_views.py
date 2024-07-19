from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import Amenity, AmenityOption
from core.serializers import AmenitySerializer, AmenityOptionSerializer


class AmenityListAPIView(APIView):
    def get(self, request):
        serializer = AmenitySerializer(Amenity.objects.all(), many=True)
        return Response({"amenities": serializer.data})


class AmenityOptionListAPIView(APIView):
    def get(self, request, id):
        serializer = AmenityOptionSerializer(AmenityOption.objects.filter(amenity=id), many=True)
        return Response({"amenity_options": serializer.data})


