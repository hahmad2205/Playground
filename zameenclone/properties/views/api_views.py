from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Property
from ..serializers import PropertySerializer

class Marketplace(APIView):
    def get(self, request, format=None):
        properties = Property.objects.all().prefetch_related("images", "amenities", "offers", "owner")
        serializer = PropertySerializer(properties, many=True)
        return Response(data=serializer.data, status=200)

class Properties(APIView):
    def get(self, request, format=None):
        properties = Property.objects.filter(owner=request.user).select_related("owner").prefetch_related("images", "amenities", "offers")
        serializer = PropertySerializer(properties, many=True)
        return Response(data=serializer.data, status=200)
