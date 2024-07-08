from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Property
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
        properties = Property.objects.filter(Q(title__contains=request.POST.get("search")) | Q(location__contains=request.POST.get("search")))
    else:
        properties = Property.objects.filter(owner=request.user)
    
    return render(
        request, "properties/property_listing.html",
        {
            "properties": create_pagination(properties, request),
            "path": request.path
        }
    )
    
@login_required
def app_property(request):
    if request.method == "POST":
        pass
    else:
        pass
