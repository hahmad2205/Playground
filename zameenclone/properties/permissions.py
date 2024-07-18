from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner != request.user


class OfferIsActive(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_active == True
    
class OfferedByAuthenticatedUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.offered_by == request.user