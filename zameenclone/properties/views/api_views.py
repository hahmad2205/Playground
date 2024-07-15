from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from ..models import Property, PropertyFilter
from ..serializers import PropertySerializer


class PropertyMarketplaceListAPIView(APIView):
    def get(self, request):
        query = request.GET.get("search")
        queryset = (
            Property.objects.filter(is_active=True, is_sold=False)
            .prefetch_related("images", "amenities", "offers", "owner")
        )
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(location__icontains=query)
            )
            
        serializer = PropertySerializer(queryset, many=True)
        return Response(data=serializer.data)


class PropertyListAPIView(APIView):
    def get(self, request):
        query = request.GET.get("search")
        queryset = (
            Property.objects.filter(is_active=True, is_sold=False, owner=request.user).
            prefetch_related("images", "amenities", "offers", "owner")
        )
        if query:
            properties = (
                queryset.filter(
                    Q(title__icontains=query) | Q(location__icontains=query)
                )
            )
        else:
            properties = queryset
            
        serializer = PropertySerializer(properties, many=True)
        return Response(data=serializer.data)

