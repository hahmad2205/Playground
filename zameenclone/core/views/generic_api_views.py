from django.shortcuts import get_list_or_404
from rest_framework import generics

from core.models import Amenity, AmenityOption
from core.serializers import AmenitySerializer, AmenityOptionListSerializer


class AmenityListAPIView(generics.ListAPIView):
    queryset = get_list_or_404(Amenity, is_active=True)
    serializer_class = AmenitySerializer


class AmenityOptionListAPIView(generics.ListAPIView):
    serializer_class = AmenityOptionListSerializer

    def get_queryset(self):
        return AmenityOption.objects.filter(
            is_active=True, amenity=self.kwargs.get(self.lookup_field)
        ).select_related("amenity")

