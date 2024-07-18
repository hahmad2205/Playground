from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from properties.models import Property, PropertyOffers
from properties.serializers import PropertyOfferSerializer
from properties.enums import MobileState
from properties.permissions import IsOwner, OfferIsActive, OfferedByAuthenticatedUser
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
    permission_classes = [IsAuthenticated, IsOwner]
    
    def post(self, request, property_id):
        property = get_object_or_404(Property, pk=property_id, is_active=True, is_sold=False)
        self.check_object_permissions(request, property)
        data = request.data
        data["offered_by"] = request.user.id
        data["property"] = property_id
        serializer = PropertyOfferSerializer(data=data)
        print(data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
        else: 
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return response


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
    permission_classes = [
        IsAuthenticated, OfferIsActive
    ]
    
    def patch(self, request, offer_id, offer_state):
        offer = get_object_or_404(PropertyOffers, pk=offer_id, state=MobileState.PENDING)
        self.check_object_permissions(request, offer)
        
        if offer_state:
            message = offer.mark_accepted()
        else:
            message = offer.mark_rejected()
        
        offer.save()
        
        serializer = PropertyOfferSerializer(offer)
        return Response({"message": message, "offer": serializer.data})
        

class PropertyOfferWithdrawAPIView(APIView):
    permission_classes = [
        IsAuthenticated, OfferIsActive, OfferedByAuthenticatedUser
    ]
    
    def patch(self, request, offer_id):
        offer = get_object_or_404(PropertyOffers, pk=offer_id)
        self.check_object_permissions(request, offer)
        data = {"is_active": False}
        serializer = PropertyOfferSerializer(offer, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            response = Response({"message": "Your offer is withdrawn"})
        else: 
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return response

