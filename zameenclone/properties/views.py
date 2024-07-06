from django.shortcuts import render
from .models import Property
from django.contrib.auth.decorators import login_required

def get_images_from_property(properties):
    properties_with_images = []
    for property in properties:
        images = property.images.all()
        properties_with_images.append({
            "property": property,
            "image_url": images[0].image_url
        })
        
    return properties_with_images

def marketplace_listings(request):    
    properties = Property.objects.all()
    context = {"properties": get_images_from_property(properties), "path": request.path}
    
    return render(request, "properties/property_listing.html", context)

@login_required
def my_listings(request):
    properties = Property.objects.filter(owner=request.user)
    context = {"properties": get_images_from_property(properties)}

    return render(request, "properties/property_listing.html", context)