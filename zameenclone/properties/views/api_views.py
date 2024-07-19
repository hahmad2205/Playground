from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Property
from core.utils import get_serialized_data


class PropertyMarketplaceListAPIView(APIView):
    def get(self, request):
        queryset = (
            Property.objects.active()
            .prefetch_related("images", "amenities", "offers", "owner")
        )
        
        return Response(data=get_serialized_data(request, queryset))


class PropertyListAPIView(APIView):
    def get(self, request):
        queryset = (
            Property.objects.active().filter(owner=request.user).
            prefetch_related("images", "amenities", "offers", "owner")
        )
        
        return Response(data=get_serialized_data(request, queryset))


