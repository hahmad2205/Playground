from rest_framework.permissions import BasePermission

from properties.models import Property


class IsNotPropertyOwner(BasePermission):
    def has_permission(self, request, view):
        property_id = view.kwargs.get("id")
        if not property_id:
            return False

        try:
            property = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return False

        return property.owner != request.user


class IsOfferOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.offered_by == request.user


class IsNotOfferOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.offered_by != request.user


class IsPropertyOwner(BasePermission):
    def has_permission(self, request, view):
        property = Property.objects.get(id=view.kwargs.get("id"))

        return property.owner == request.user

