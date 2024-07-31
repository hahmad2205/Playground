from django.db.models import Prefetch, Count, Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from properties.enums import MobileState
from properties.filters import PropertyFilter
from properties.models import Property, PropertyAmenity, PropertyOffers
from properties.permissions import IsNotPropertyOwner, IsPropertyOwner, IsOfferPropertyOwner, IsOfferOwner
from properties.serializers import (
    PropertyListSerializer,
    PropertyOfferSerializer,
    PropertyOfferListSerializer,
    PropertyOfferUpdateSerializer,
    PropertyDetailSerializer,
    PropertyOfferWithdrawSerializer,
    PropertyUpdateSerializer,
    PropertySerializer
)
from communications.tasks import send_email_on_offer_state_update


class PropertyListMixin(ModelViewSet):
    serializer_class = PropertyListSerializer
    filterset_class = PropertyFilter
    search_fields = ["title", "location"]
    ordering_fields = ["pk", "price"]
    ordering = ["pk"]
    queryset = Property.objects.active()


class PropertyMarketplaceListAPIView(PropertyListMixin):
    def get_queryset(self):
        return Property.objects.active().prefetch_related(
            Prefetch("amenities", queryset=PropertyAmenity.objects.active()),
            Prefetch("offers", queryset=PropertyOffers.objects.active())
        ).select_related("owner").annotate(offer_count=Count("offers"))


class PropertyListAPIView(PropertyListMixin):
    def get_queryset(self):
        return Property.objects.active().filter(owner=self.request.user).prefetch_related(
            Prefetch("amenities", queryset=PropertyAmenity.objects.active()),
            Prefetch("offers", queryset=PropertyOffers.objects.active())
        ).select_related("owner").annotate(
            offer_count=Count(
                "offers",
                filter=Q(offers__is_active=True) & Q(offers__state=MobileState.PENDING)
            )
        )

    def create(self, request, *args, **kwargs):
        serializer = PropertySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PropertyOfferListAPIView(ModelViewSet):
    serializer_class = PropertyOfferListSerializer

    def get_queryset(self):
        return PropertyOffers.objects.filter(property__owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = PropertyOfferSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(offered_by=self.request.user)

    @action(detail=True, methods=["patch"], url_path="withdraw")
    def withdraw(self, request, pk=None):
        offer = get_object_or_404(PropertyOffers, pk=pk, offered_by=self.request.user)
        offer.is_active = False
        offer.save()

        return Response({"detail": "Offer successfully withdrawn."})

    @action(detail=True, methods=["get"], url_path="property_offers")
    def property_offers(self, request, pk=None):
        property = get_object_or_404(Property, pk=pk)
        return Response(property.offers.active())


class PropertyOfferUpdateStateAPIView(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOfferPropertyOwner]
    serializer_class = PropertyOfferUpdateSerializer
    queryset = PropertyOffers.objects.active()

    def perform_update(self, serializer):
        instance = serializer.save()
        send_email_on_offer_state_update.delay(instance)

