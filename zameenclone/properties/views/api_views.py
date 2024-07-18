from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from properties.models import Property, PropertyOffers
from properties.serializers import PropertyOfferSerializer
from core.utils import get_serialized_data


class PropertyMarketplaceListAPIView(APIView):
    def get(self, request):
        queryset = (
            Property.objects.active()
            .prefetch_related("images", "amenities", "offers", "owner")
        )
        
        return Response(data=get_serialized_data(request, queryset))


class PropertyListAPIView(APIView):
    def get(self, request):
        queryset = (
            Property.objects.active().filter(owner=request.user).
            prefetch_related("images", "amenities", "offers", "owner")
        )
        
        return Response(data=get_serialized_data(request, queryset))


class PropertyOfferCreateAPIView(APIView):
    def post(self, request, property_id):
        property = get_object_or_404(Property, pk=property_id)
        
        if property.owner == request.user:
            return Response(
                {'error': 'You cannot make an offer on your own property'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        price = request.data.get("price")
        if price is None:
            return Response(
                {'error': 'Price is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        PropertyOffers.objects.create(
            price=price, offered_by=request.user, property=property
        )
        
        return Response(
            {'message': 'Offer created successfully'},
            status=status.HTTP_201_CREATED
        )
        
        
class PropertyOfferListAPIView(APIView):
    def get(self, request):
        offers = PropertyOffers.objects.active().filter(property__owner=request.user)
        serializer = PropertyOfferSerializer(offers, many=True)
        
        return Response(data=serializer.data)


class PropertyOfferFromPropertyListAPIView(APIView):
    def get(self, request, property_id):
        offers = PropertyOffers.objects.active().filter(property=property_id)
        serializer = PropertyOfferSerializer(offers, many=True)
        
        return Response(data=serializer.data)


class PropertyOfferUpdateAPIView(APIView):
    def patch(self, request, offer_id, offer_state):
        offer = get_object_or_404(PropertyOffers, pk=offer_id)
        
        if offer.property.owner != request.user:
            response = Response(
                {'error': 'You are not authorized to change the state of this offer'},
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            message = offer.mark_accepted() if offer_state else offer.mark_rejected()
            offer.save()
            response = Response({"message": message})
        
        return response


class PropertyOfferWithdrawAPIView(APIView):
    def patch(self, request, offer_id):
        offer = get_object_or_404(PropertyOffers, pk=offer_id)
        if not offer.is_active:
            response = Response(
                {"message": "Offer is already withdrawn"},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            offer.is_active = False
            offer.save(update_fields=['is_active'])
            response = Response(
                {"message": "Your offer is withdrawn"},
                )

        return response