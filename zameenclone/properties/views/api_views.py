from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..models import Property
from ..serializers import PropertySerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_marketplace(request):
    properties = (
        Property.objects.all().
        prefetch_related("images", "offers", "amenities", "owner")
        )
    serializer = PropertySerializer(properties, many=True)
    return Response(data=serializer.data, status=200)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_properties(request):
    properties = (
        Property.objects.filter(owner=request.user)
        .select_related("owner")
        .prefetch_related("images", "offers", "amenities")
    )
    serializer = PropertySerializer(properties, many=True)
    return Response(data=serializer.data, status=200)
