from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from properties.models import Property, PropertyOffers
from properties.serializers import PropertyOfferSerializer, PropertySerializer, PropertyUpdateSerializer
from properties.enums import MobileState
from properties.permissions import IsNotPropertyOwner, IsOfferOwner, IsNotOfferOwner
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
    permission_classes = [IsAuthenticated, IsNotPropertyOwner]
    
    def post(self, request, id):
        property = get_object_or_404(Property, pk=id, is_active=True, is_sold=False)
        self.check_object_permissions(request, property)
        data = request.data
        data["offered_by"] = request.user.id
        data["property"] = id
        serializer = PropertyOfferSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class PropertyOfferListAPIView(APIView):
    def get(self, request):
        offers = PropertyOffers.objects.active().filter(property__owner=request.user)
        serializer = PropertyOfferSerializer(offers, many=True)
        
        return Response(data=serializer.data)


class PropertyOfferFromPropertyListAPIView(APIView):
    def get(self, request, id):
        offers = PropertyOffers.objects.active().filter(property=id)
        serializer = PropertyOfferSerializer(offers, many=True)
        
        return Response(data=serializer.data)


class PropertyOfferUpdateStateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsNotOfferOwner]
    
    def patch(self, request, id):
        offer = get_object_or_404(
            PropertyOffers, pk=id, state=MobileState.PENDING,
            is_active=True, property__is_active=True, property__is_sold=False
        )
        self.check_object_permissions(request, offer)

        serializer = PropertyOfferSerializer(offer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data)


class PropertyOfferWithdrawAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOfferOwner]
    
    def patch(self, request, id):
        offer = get_object_or_404(PropertyOffers, pk=id, is_active=True, state=MobileState.PENDING)
        self.check_object_permissions(request, offer)
        data = {"is_active": False}
        serializer = PropertyOfferSerializer(offer, data=data, partial=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = Response({"message": "Your offer is withdrawn"})

        return response


class PropertyCreateAPIView(APIView):
    def post(self, request):
        data = request.data
        data["owner"] = request.user.id
        serializer = PropertySerializer(data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)

        return response


class PropertyRetrieveAPIView(APIView):

    def get(self, request, id):
        property = get_object_or_404(Property, pk=id, is_active=True, is_sold=False)
        serializer = PropertySerializer(property)
        return Response(serializer.data)


class PropertyUpdateAPIView(APIView):

    def patch(self, request, id):
        property = get_object_or_404(Property, pk=id)
        serializer = PropertyUpdateSerializer(property, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

