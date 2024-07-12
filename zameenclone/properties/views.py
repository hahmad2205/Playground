from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import modelformset_factory

from .forms import PropertyForm, PropertyImagesForm, PropertyAmenityForm
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
            property_instance = get_object_or_404(Property, pk=request.POST["property_id"], is_active=True)
            property_instance.is_active = False
            property_instance.save()
            property_instance.images.all().update(is_active=False)
            property_instance.amenities.all().update(is_active=False)
            property_instance.offers.all().update(is_active=False)
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
def add_property(request):
    PropertyImageFormSet = modelformset_factory(PropertyImages, form=PropertyImagesForm, extra=1)
    PropertyAmenityFormSet = modelformset_factory(PropertyAmenity, form=PropertyAmenityForm, extra=1)

    if request.method == 'POST':
        property_form = PropertyForm(request.POST)
        image_formset = PropertyImageFormSet(request.POST, request.FILES, queryset=PropertyImages.objects.none())
        amenity_formset = PropertyAmenityFormSet(request.POST, queryset=PropertyAmenity.objects.none())
             
        if not image_formset.is_valid():
            print(image_formset.errors)
        if property_form.is_valid() and image_formset.is_valid() and amenity_formset.is_valid():
            property_instance = property_form.save(commit=False)
            property_instance.owner = request.user
            property_instance.save()

            for form in image_formset:
                if form.cleaned_data:
                    image_instance = form.save(commit=False)
                    image_instance.property = property_instance
                    image_instance.save()

            for form in amenity_formset:
                if form.cleaned_data:
                    PropertyAmenity(
                        property=property_instance,
                        value=form.cleaned_data.get('value'),
                        amenity=form.cleaned_data['amenity'],
                    ).save()
            
            response = redirect('properties')
    elif request.method == "GET":
        property_form = PropertyForm()
        image_formset = PropertyImageFormSet(queryset=PropertyImages.objects.none())
        amenity_formset = PropertyAmenityFormSet(queryset=PropertyAmenity.objects.none())
        response = render(request, 'properties/property_form.html', {
            'property_form': property_form,
            'image_formset': image_formset,
            'amenity_formset': amenity_formset
        })

    return response
    
@login_required
def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    
    return render(
        request, "properties/property_details.html", {"property": property}
    )
