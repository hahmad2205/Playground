from django.core.paginator import Paginator
from properties.models import Property

def create_pagination(properties, request):
    properties_with_images = Property.get_images_from_properties(properties)
    paginator = Paginator(properties_with_images, 25)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)
