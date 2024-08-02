from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import generics

from core.models import Amenity, AmenityOption
from core.serializers import AmenitySerializer, AmenityOptionListSerializer


class AmenityListAPIView(generics.ListAPIView):
    queryset = Amenity.objects.filter(is_active=True)
    serializer_class = AmenitySerializer
    pagination_class = None


class AmenityOptionListAPIView(generics.ListAPIView):
    serializer_class = AmenityOptionListSerializer
    pagination_class = None

    def get_queryset(self):
        amenity = get_object_or_404(Amenity, pk=self.kwargs.get(self.lookup_field))
        return amenity.options.filter(is_active=True)

