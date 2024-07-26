from django.db.models import Prefetch, Count
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated

from properties.models import Property, PropertyOffers, PropertyAmenity, PropertyImages
from properties.serializers import (
    PropertyListDetailSerializer,
    PropertyOfferSerializer,
    PropertyOfferListSerializer,
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
from properties.enums import MobileState


class PropertyListMixin(ListAPIView):
    serializer_class = PropertyListDetailSerializer
    filterset_class = PropertyFilter
    search_fields = ["title", "location"]
    ordering_fields = ["pk", "price"]
    ordering = ["pk"]


class PropertyMarketplaceListAPIView(PropertyListMixin):
    queryset = (
        Property.objects.active().
        prefetch_related(
            Prefetch("amenities", queryset=PropertyAmenity.objects.active()),
            Prefetch("offers", queryset=PropertyOffers.objects.active())
        ).
        select_related("owner").annotate(offer_count=Count("offers"))
    )


class PropertyListAPIView(PropertyListMixin):
    def get_queryset(self):
        return (
            Property.objects.active().filter(owner=self.request.user).
            prefetch_related(
                Prefetch("amenities", queryset=PropertyAmenity.objects.active()),
                Prefetch("offers", queryset=PropertyOffers.objects.active())
            ).
            select_related("owner").annotate(offer_count=Count("offers"))
        )


class PropertyOfferCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsNotPropertyOwner]
    serializer_class = PropertyOfferSerializer


class PropertyOfferListAPIView(ListAPIView):
    serializer_class = PropertyOfferListSerializer

    def get_queryset(self):
        return PropertyOffers.objects.active().filter(
            property__owner=self.request.user, state=MobileState.PENDING.value
        )


class PropertyOfferFromPropertyListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsPropertyOwner]
    serializer_class = PropertyOfferListSerializer
    queryset = PropertyOffers.objects.active().filter(state=MobileState.PENDING.value)

    def get_queryset(self):
        return (
            PropertyOffers.objects.active().filter(property=self.kwargs["pk"])
        )


class PropertyOfferUpdateStateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsNotOfferOwnerAndPropertyOwner]
    serializer_class = PropertyOfferUpdateSerializer
    queryset = PropertyOffers.objects.active()


class PropertyDetailAPIView(RetrieveAPIView):
    serializer_class = PropertyListDetailSerializer
    queryset = Property.objects.active().annotate(offer_count=Count("offers"))


class PropertyOfferWithdrawAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOfferOwner]
    serializer_class = PropertyOfferWithdrawSerializer
    queryset = PropertyOffers.objects.active()


class PropertyUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsPropertyOwner]
    serializer_class = PropertyUpdateSerializer
    queryset = Property.objects.active()


class PropertyCreateAPIView(CreateAPIView):
    serializer_class = PropertySerializer

