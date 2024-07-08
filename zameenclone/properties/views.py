from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Property, PropertyFilter
from core.utils import create_pagination

@login_required
def marketplace(request):
    if request.method == "POST":
        search_item = request.POST.get("search", "")
        if search_item:
            properties = Property.objects.filter(
                Q(title__icontains=search_item) |
                Q(location__icontains=search_item)
            )
        else:
            properties = Property.objects.all()
    else:  
        properties = PropertyFilter(request.GET, queryset=Property.objects.all()).qs
    
    return render(
        request, "properties/property_listing.html",
        {
            "properties": create_pagination(properties, request),
            "path": request.path,
            "filter": PropertyFilter(request.GET, queryset=Property.objects.all())
        }
    )

@login_required
def properties(request):
    if request.method == "POST":
        search_item = request.POST.get("search", "")
        if search_item:
            properties = Property.objects.filter(
                Q(title__icontains=search_item) |
                Q(location__icontains=search_item)
            )
        else:
            properties = Property.objects.filter(owner=request.user)
    else:  
        properties = PropertyFilter(request.GET, queryset=Property.objects.filter(owner=request.user)).qs
        
    return render(
        request, "properties/property_listing.html",
        {
            "properties": create_pagination(properties, request),
            "path": request.path,
            "filter": PropertyFilter(request.GET, queryset=Property.objects.filter(owner=request.user))
        }
    )
