from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from properties.models import Property, PropertyOffers
from properties.serializers import PropertyDetailSerializer, PropertyOfferSerializer, PropertyOfferUpdateSerializer
from properties.filters import PropertyFilter
from properties.permissions import IsNotPropertyOwner, IsPropertyOwner, IsNotOfferOwnerAndPropertyOwner
from properties.enums import MobileState


class PropertyListMixin(generics.ListAPIView):
    serializer_class = PropertyDetailSerializer
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
    permission_classes = [IsAuthenticated, IsNotPropertyOwner]
    serializer_class = PropertyOfferSerializer


class PropertyOfferListAPIView(generics.ListAPIView):
    def get_queryset(self):
        return PropertyOffers.objects.active().filter(property__owner=self.request.user)

    serializer_class = PropertyOfferSerializer


class PropertyOfferFromPropertyListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsPropertyOwner]
    serializer_class = PropertyOfferSerializer

    def get_queryset(self):
        return get_object_or_404(PropertyOffers, property=self.kwargs["id"], is_active=True)


class PropertyOfferUpdateStateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsNotOfferOwnerAndPropertyOwner]
    queryset = PropertyOffers.objects.active()
    serializer_class = PropertyOfferUpdateSerializer

    def patch(self, request, *args, **kwargs):
        offer = self.get_object()
        self.check_object_permissions(request, offer)
        serializer = PropertyOfferUpdateSerializer(offer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
