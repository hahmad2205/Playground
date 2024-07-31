from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.viewsets import ModelViewSet

from core.models import Amenity
from core.serializers import AmenitySerializer, AmenityOptionListSerializer


class AmenityListAPIView(ModelViewSet):
    serializer_class = AmenitySerializer
    queryset = get_list_or_404(Amenity, is_active=True)


class AmenityOptionListAPIView(ModelViewSet):
    serializer_class = AmenityOptionListSerializer
    pagination_class = None

    def get_queryset(self):
        amenity = get_object_or_404(Amenity, pk=self.kwargs.get("pk"))
        return amenity.options.filter(is_active=True)

