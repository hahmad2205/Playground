import requests
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter

from properties.models import Property
from properties.serializers import PropertyRetrieveSerializer
from properties.filters import PropertyFilter


class PropertyMarketplaceListGenericView(generics.ListAPIView):
    queryset = (
        Property.objects.active()
        .prefetch_related("images", "amenities", "offers", "owner")
    )
    serializer_class = PropertyRetrieveSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = PropertyFilter
    search_fields = ["title", "location"]


class PropertyListGenericView(generics.ListAPIView):
    serializer_class = PropertyRetrieveSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = PropertyFilter
    search_fields = ["title", "location"]

    def get_queryset(self):
        return (
            Property.objects.active().filter(owner=self.request.user)
            .prefetch_related("images", "amenities", "offers").
            select_related("owner")
        )

