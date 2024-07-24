from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from properties.models import Property, PropertyOffers
from properties.serializers import PropertyRetrieveSerializer, PropertyOfferSerializer, PropertyOfferUpdateSerializer
from properties.filters import PropertyFilter
from properties.permissions import IsNotPropertyOwner, IsPropertyOwner, IsNotOfferOwnerAndPropertyOwner
from properties.enums import MobileState


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


class PropertyOfferUpdateStateAPIView(generics.UpdateAPIView):
    queryset = PropertyOffers.objects.all()
    serializer_class = PropertyOfferUpdateSerializer
    permission_classes = [IsAuthenticated, IsNotOfferOwnerAndPropertyOwner]
    lookup_field = "id"

    def patch(self, request, *args, **kwargs):
        offer = self.get_object()
        self.check_object_permissions(request, offer)

        serializer = self.get_serializer(offer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        state = request.data.get("state")

        try:
            if state == MobileState.ACCEPTED:
                message = offer.mark_accepted()
            elif state == MobileState.REJECTED:
                message = offer.mark_rejected()
            else:
                raise ValidationError("Invalid state value provided.")
        except:
            raise ValidationError("Can't switch the state.")

        # Save the updated fields
        offer.save(update_fields=["state", "is_active", "property", "modified"])

        return Response({"message": message})
