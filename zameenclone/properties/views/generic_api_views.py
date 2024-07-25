from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from properties.models import Property, PropertyOffers
from properties.serializers import (
    PropertyListDetailSerializer,
    PropertyOfferSerializer,
    PropertyOfferUpdateSerializer,
    PropertyOfferWithdrawSerializer,
    PropertyUpdateSerializer,
    PropertySerializer
)
from properties.filters import PropertyFilter
from properties.permissions import (
    IsNotPropertyOwner,
    IsPropertyOwner,
    IsNotOfferOwnerAndPropertyOwner,
    IsOfferOwner
)


class PropertyListMixin(generics.ListAPIView):
    serializer_class = PropertyListDetailSerializer
    filterset_class = PropertyFilter
    search_fields = ["title", "location"]


class PropertyMarketplaceListAPIView(PropertyListMixin):
    queryset = (
        Property.objects.active().
        prefetch_related("images", "amenities", "offers").
        select_related("owner")
    )


class PropertyListAPIView(PropertyListMixin):
    def get_queryset(self):
        return (
            Property.objects.active().filter(owner=self.request.user).
            prefetch_related("images", "amenities", "offers").
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
    queryset = PropertyOffers.objects.active()
    serializer_class = PropertyOfferSerializer
    lookup_url_kwarg = "property"


class PropertyOfferUpdateStateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsNotOfferOwnerAndPropertyOwner]
    queryset = PropertyOffers.objects.active()
    serializer_class = PropertyOfferUpdateSerializer

    def partial_update(self, request, *args, **kwargs):
        offer = self.get_object()
        self.check_object_permissions(request, offer)
        serializer = PropertyOfferUpdateSerializer(offer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PropertyDetailAPIView(generics.RetrieveAPIView):
    queryset = Property.objects.active()
    serializer_class = PropertyListDetailSerializer


class PropertyOfferWithdrawAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOfferOwner]
    queryset = PropertyOffers.objects.active()
    serializer_class = PropertyOfferWithdrawSerializer


class PropertyUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsPropertyOwner]
    queryset = Property.objects.active()
    serializer_class = PropertyUpdateSerializer


class PropertyCreateAPIView(generics.CreateAPIView):
    serializer_class = PropertySerializer

