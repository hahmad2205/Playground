from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Property

def get_images_from_property(properties):
    properties_with_images = []
    for property in properties:
        images = property.images.all()
        properties_with_images.append({
            "property": property,
            "image_url": images[0].image_url
        })
        
    return properties_with_images

def create_pagination_of_properties(properties, request):
    properties_with_images = get_images_from_property(properties)
    paginator = Paginator(properties_with_images, 25)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)

def marketplace_listings(request):    
    properties = Property.objects.all()    
    return render(
        request, "properties/property_listing.html",
        {
            "properties": create_pagination_of_properties(properties, request),
            "path": request.path
        }
    )

@login_required
def my_listings(request):
    properties = Property.objects.filter(owner=request.user)
    return render(
        request, "properties/property_listing.html",
        {
            "properties": create_pagination_of_properties(properties, request),
            "path": request.path
        }
    )