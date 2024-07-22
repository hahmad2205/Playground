from django.db.models import Q

from django.core.paginator import Paginator

from properties.models import Property
from properties.filters import PropertyFilter
from properties.serializers import PropertySerializer, PropertyImageSerializer, PropertyAmenitySerializer


def create_pagination(properties, request):
    properties_with_images = Property.get_images_from_properties(properties)
    paginator = Paginator(properties_with_images, 25)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


def get_serialized_data(request, queryset):
    query = request.query_params.get("search")
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(location__icontains=query)
        )

    filterset = PropertyFilter(request.GET, queryset=queryset)
    if filterset.is_valid:
        queryset = filterset.qs

    serializer = PropertySerializer(queryset, many=True)
    return serializer.data

