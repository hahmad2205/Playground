from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from properties.models import Property, PropertyOffers
from properties.serializers import PropertyRetrieveSerializer, PropertyOfferSerializer
from properties.filters import PropertyFilter
from properties.permissions import IsNotPropertyOwner, IsPropertyOwner


class PropertyListMixin(generics.ListAPIView):
    serializer_class = PropertyRetrieveSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = PropertyFilter
    search_fields = ["title", "location"]


class PropertyMarketplaceListAPIView(PropertyListMixin):
    queryset = (
        Property.objects.active()
        .prefetch_related("images", "amenities", "offers", "owner")
    )


class PropertyListAPIView(PropertyListMixin):
    def get_queryset(self):
        return (
            Property.objects.active().filter(owner=self.request.user)
            .prefetch_related("images", "amenities", "offers").
            select_related("owner")
        )


class PropertyOfferCreateAPIView(generics.CreateAPIView):
    serializer_class = PropertyOfferSerializer
    permission_classes = [IsAuthenticated, IsNotPropertyOwner]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["property_id"] = self.kwargs.get("id")
        return context


class PropertyOfferListAPIView(generics.ListAPIView):
    def get_queryset(self):
        return PropertyOffers.objects.active().filter(property__owner=self.request.user)

    serializer_class = PropertyOfferSerializer


class PropertyOfferFromPropertyListAPIView(generics.ListAPIView):
    serializer_class = PropertyOfferSerializer
    permission_classes = [IsAuthenticated, IsPropertyOwner]

    def get_queryset(self):
        return PropertyOffers.objects.active().filter(property=self.kwargs["id"])

