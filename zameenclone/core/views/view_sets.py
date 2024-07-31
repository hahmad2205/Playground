from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from core.models import Amenity, AmenityOption
from core.serializers import AmenitySerializer, AmenityOptionListSerializer


class AmenityListAPIView(GenericViewSet):
    serializer_class = AmenitySerializer

    def list(self, request):
        queryset = get_list_or_404(Amenity, is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AmenityOptionListAPIView(GenericViewSet):
    serializer_class = AmenityOptionListSerializer
    pagination_class = None

    def get_queryset(self):
        amenity = get_object_or_404(Amenity, pk=self.kwargs.get('pk'))
        return amenity.options.filter(is_active=True)

    def list(self, request, pk=None):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
