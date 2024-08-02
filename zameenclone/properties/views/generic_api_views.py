from django.db.models import Prefetch, Count, Q
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated

from properties.models import Property, PropertyOffers, PropertyAmenity
from properties.serializers import (
    PropertyListSerializer,
    PropertyDetailSerializer,
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
    IsOfferOwner,
    IsOfferPropertyOwner
)
from properties.enums import MobileState
from communications.tasks import send_email_on_offer_state_update


class PropertyListMixin(ListAPIView):
    serializer_class = PropertyListSerializer
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
            select_related("owner").annotate(
                offer_count=
                Count(
                    "offers",
                    filter=(
                        Q(offers__is_active=True) &
                        Q(offers__state=MobileState.PENDING)
                    )
                )
            )
        )


class PropertyOfferCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsNotPropertyOwner]
    serializer_class = PropertyOfferSerializer


class PropertyOfferListAPIView(ListAPIView):
    serializer_class = PropertyOfferListSerializer
    filterset_fields = ("state",)

    def get_queryset(self):
        return PropertyOffers.objects.filter(
            property__owner=self.request.user
        )


class PropertyOfferFromPropertyListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsPropertyOwner]
    serializer_class = PropertyOfferListSerializer

    def get_queryset(self):
        property = get_object_or_404(Property, pk=self.kwargs["pk"])
        return property.offers.active()


class PropertyOfferUpdateStateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOfferPropertyOwner]
    serializer_class = PropertyOfferUpdateSerializer
    queryset = PropertyOffers.objects.active()

    def perform_update(self, serializer):
        instance = serializer.save()
        send_email_on_offer_state_update.delay(instance)


class PropertyDetailAPIView(RetrieveAPIView):
    serializer_class = PropertyDetailSerializer
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
