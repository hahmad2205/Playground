from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from ..models import Property, PropertyFilter
from ..serializers import PropertySerializer
from core.utils import get_filtered_data


class PropertyMarketplaceListAPIView(APIView):
    def get(self, request):
        queryset = (
            Property.objects.filter(is_active=True, is_sold=False)
            .prefetch_related("images", "amenities", "offers", "owner")
        )
        
        return Response(data=get_filtered_data(request, queryset))


class PropertyListAPIView(APIView):
    def get(self, request):
        queryset = (
            Property.objects.filter(
                is_active=True, is_sold=False, owner=request.user
            ).
            prefetch_related("images", "amenities", "offers", "owner")
        )
        
        return Response(data=get_filtered_data(request, queryset))
