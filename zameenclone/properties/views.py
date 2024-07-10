from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Property, PropertyImages, PropertyAmenity, PropertyFilter
from core.utils import create_pagination

@login_required
def marketplace(request):
    queryset = Property.objects.filter(is_active=True)
    if request.method == "POST":
        search_item = request.POST.get("search", "")
        properties = queryset.filter(
            Q(title__icontains=search_item) |
            Q(location__icontains=search_item),
            is_active=True
        ) if search_item else queryset
    elif request.method == "GET":  
        properties = PropertyFilter(request.GET, queryset=queryset).qs
    
    return render(
        request, "properties/property_listing.html",
        {
            "properties": create_pagination(properties, request),
            "path": request.path,
            "filter": PropertyFilter(request.GET, queryset=queryset)
        }
    )

@login_required
def properties(request):
    queryset = Property.objects.filter(owner=request.user, is_active=True)
    search_item = request.POST.get("search", "")
    if request.method == "POST":
        if search_item:
            properties = queryset.filter(
                Q(title__contains=search_item) |
                Q(location__contains=search_item)
            )
        elif request.POST.get("property_id"):
            property_instance = get_object_or_404(Property, pk=request.POST["property_id"])
            property_instance.is_active = False
            property_instance.save()
            property_instance.images.all().update(is_active=False)
            property_instance.amenities.all().update(is_active=False)
            properties = queryset
    elif request.method == "GET":
        properties = PropertyFilter(request.GET, queryset=queryset).qs if request.GET.get("price") else queryset
        
    return render(
        request, "properties/property_listing.html",
        {
            "properties": create_pagination(properties, request),
            "path": request.path,
            "filter": PropertyFilter(request.GET, queryset=queryset)
        }
    )
    
@login_required
def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    
    return render(
        request, "properties/property_details.html", {"property": property}
    )
