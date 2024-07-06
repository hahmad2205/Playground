from django.shortcuts import render
from .models import Property
from django.contrib.auth.decorators import login_required

def marketplace_listings(request):    
    properties = Property.objects.all()
    properties_with_images = []
    for property in properties:
        images = property.images.all()
        properties_with_images.append({
            "property": property,
            "image_url": images[0].image_url
        })
    context = {"properties": properties_with_images, "path": request.path}
    
    return render(request, "properties/marketplace_listing.html", context)

@login_required
def my_listings(request):
    properties = Property.objects.filter(owner=request.user)
    properties_with_images = []
    for property in properties:
        images = property.images.all()
        if images.exists():
            properties_with_images.append({
                "property": property,
                "image_url": images[0].image_url
            })
    context = {"properties": properties_with_images}

    return render(request, "properties/marketplace_listing.html", context)