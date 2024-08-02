from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from properties.models import Property


class IsNotPropertyOwner(BasePermission):
    def has_permission(self, request, view):
        property_id = request.data.get("property")
        property = get_object_or_404(Property, id=property_id)

        return not property.owner == request.user


class IsOfferOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.offered_by == request.user


class IsPropertyOwner(BasePermission):
    def has_permission(self, request, view):
        property = get_object_or_404(Property, pk=view.kwargs.get("pk"), is_active=True, is_sold=False)

        return property.owner == request.user


class IsOfferPropertyOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.property.owner == request.user

