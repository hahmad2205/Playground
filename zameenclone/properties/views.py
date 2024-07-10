from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Property, PropertyImages, PropertyAmenity
from core.utils import create_pagination

@login_required
def marketplace(request):
    if request.method == "POST":
        properties = Property.objects.filter(Q(title__contains=request.POST.get("search")) | Q(location__contains=request.POST.get("search")))
    else:  
        properties = Property.objects.all()    
    
    return render(
        request, "properties/property_listing.html",
        {
            "properties": create_pagination(properties, request),
            "path": request.path
        }
    )

@login_required
def properties(request):
    if request.method == "POST":
        if request.POST.get("search"):
            properties = Property.objects.filter(Q(title__contains=request.POST.get("search")) | Q(location__contains=request.POST.get("search")))
        elif request.POST.get("property_id"):
            property_instance = Property.objects.get(pk=request.POST["property_id"])
            property_instance.is_active = False
            property_instance.save()
            properties = Property.objects.filter(owner=request.user, is_active=True) if property_instance else None
    else:
        properties = Property.objects.filter(owner=request.user)
    
    
    return render(
        request, "properties/property_listing.html",
        {
            "properties": create_pagination(properties, request),
            "path": request.path
        }
    )
