from rest_framework.permissions import BasePermission


class IsNotPropertyOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner != request.user
    
class IsOfferOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.offered_by == request.user

class IsNotOfferOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.offered_by != request.user

