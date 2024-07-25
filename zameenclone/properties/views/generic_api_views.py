from django.db.models import Prefetch
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
from core.pagination import CustomPagination


class PropertyListMixin(ListAPIView):
    serializer_class = PropertyListDetailSerializer
    filterset_class = PropertyFilter
    pagination_class = CustomPagination
    search_fields = ["title", "location"]
    ordering_fields = ["pk", "price"]
    ordering = ["price"]


class PropertyMarketplaceListAPIView(PropertyListMixin):
    queryset = (
        Property.objects.active().
        prefetch_related(
            Prefetch("images", queryset=PropertyImages.objects.active()),
            Prefetch("amenities", queryset=PropertyAmenity.objects.active()),
            Prefetch("offers", queryset=PropertyOffers.objects.active())
        ).
        select_related("owner")
    )


class PropertyListAPIView(PropertyListMixin):
    def get_queryset(self):
        return (
            Property.objects.active().filter(owner=self.request.user).
            prefetch_related(
                Prefetch("images", queryset=PropertyImages.objects.active()),
                Prefetch("amenities", queryset=PropertyAmenity.objects.active()),
                Prefetch("offers", queryset=PropertyOffers.objects.active())
            ).
            select_related("owner")
        )


class PropertyOfferCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsNotPropertyOwner]
    serializer_class = PropertyOfferSerializer


class PropertyOfferListAPIView(ListAPIView):
    serializer_class = PropertyOfferListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return PropertyOffers.objects.active().filter(property__owner=self.request.user, state=MobileState.PENDING.value)


class PropertyOfferFromPropertyListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsPropertyOwner]
    queryset = PropertyOffers.objects.active().filter(state=MobileState.PENDING.value)
    serializer_class = PropertyOfferListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return (
            PropertyOffers.objects.active().filter(property=self.kwargs["pk"])
        )


class PropertyOfferUpdateStateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsNotOfferOwnerAndPropertyOwner]
    queryset = PropertyOffers.objects.active()
    serializer_class = PropertyOfferUpdateSerializer


class PropertyDetailAPIView(RetrieveAPIView):
    queryset = Property.objects.active()
    serializer_class = PropertyListDetailSerializer


class PropertyOfferWithdrawAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOfferOwner]
    queryset = PropertyOffers.objects.active()
    serializer_class = PropertyOfferWithdrawSerializer


class PropertyUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsPropertyOwner]
    queryset = Property.objects.active()
    serializer_class = PropertyUpdateSerializer


class PropertyCreateAPIView(CreateAPIView):
    serializer_class = PropertySerializer

