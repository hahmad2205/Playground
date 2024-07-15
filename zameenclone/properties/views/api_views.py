from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Property
from ..serializers import PropertySerializer


class PropertyMarketplaceListAPIView(APIView):
    def get(self, request):
        properties = (
            Property.objects.filter(is_active=True, is_sold=False).
            prefetch_related("images", "amenities", "offers", "owner")
        )
        serializer = PropertySerializer(properties, many=True)
        return Response(data=serializer.data)


class PropertyListAPIView(APIView):
    def get(self, request):
        properties = (
            Property.objects.filter(owner=request.user, is_active=True, is_sold=False).
            select_related("owner").prefetch_related("images", "amenities", "offers")
        )
        serializer = PropertySerializer(properties, many=True)
        return Response(data=serializer.data)

