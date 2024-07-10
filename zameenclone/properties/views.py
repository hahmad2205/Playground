from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import modelformset_factory


from .forms import PropertyForm, PropertyImagesForm, PropertyAmenityForm
from .models import Property, PropertyImages, PropertyAmenity
from core.models import AmenityOption
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
def add_property(request):
    PropertyImageFormSet = modelformset_factory(PropertyImages, form=PropertyImagesForm, extra=1)
    PropertyAmenityFormSet = modelformset_factory(PropertyAmenity, form=PropertyAmenityForm, extra=1)
    
    if request.method == 'POST':
        property_form = PropertyForm(request.POST)
        image_formset = PropertyImageFormSet(request.POST, request.FILES, queryset=PropertyImages.objects.none())
        amenity_formset = PropertyAmenityFormSet(request.POST, queryset=PropertyAmenity.objects.none())
        if property_form.is_valid() and image_formset.is_valid() and amenity_formset.is_valid():
            property_instance = property_form.save(commit=False)
            property_instance.owner = request.user
            property_instance.save()

            for form in image_formset:
                if form.cleaned_data:
                    PropertyImages(property=property_instance, image=form.cleaned_data['image']).save()

            for form in amenity_formset:
                if form.cleaned_data:
                    PropertyAmenity(
                        property=property_instance,
                        value=form.cleaned_data.get('value'),
                        amenity=form.cleaned_data['amenity'],
                    ).save()

            return redirect('properties')
    else:
        property_form = PropertyForm()
        image_formset = PropertyImageFormSet(queryset=PropertyImages.objects.none())
        amenity_formset = PropertyAmenityFormSet(queryset=PropertyAmenity.objects.none())

    return render(request, 'properties/property_form.html', {
        'property_form': property_form,
        'image_formset': image_formset,
        'amenity_formset': amenity_formset
    })
