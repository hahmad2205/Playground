from django.shortcuts import get_list_or_404
from rest_framework import generics

from core.models import Amenity, AmenityOption
from core.serializers import AmenitySerializer, AmenityOptionSerializer


class AmenityListAPIView(generics.ListAPIView):
    queryset = get_list_or_404(Amenity, is_active=True)
    serializer_class = AmenitySerializer


class AmenityOptionListAPIView(generics.ListAPIView):
    queryset = AmenityOption.objects.filter(is_active=True)
    serializer_class = AmenityOptionSerializer
    lookup_url_kwarg = "amenity"
