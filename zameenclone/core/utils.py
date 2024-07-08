from django.core.paginator import Paginator
# Create your views here.


def get_images_from_property(properties):
    properties_with_images = []
    for property in properties:
        images = property.images.all()
        properties_with_images.append({
            "property": property,
            "image_url": images[0].image_url
        })
        
    return properties_with_images

def create_pagination(properties, request):
    properties_with_images = get_images_from_property(properties)
    paginator = Paginator(properties_with_images, 25)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)
