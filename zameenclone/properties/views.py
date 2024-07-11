from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Property, PropertyFilter, PropertyOffers
from .forms import OfferForm
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
def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    owner = True if property.owner == request.user else False
    
    return render(
        request, "properties/property_details.html", {"property": property, "owner":owner}
    )

@login_required
def create_offer(request, property_id):
    if request.method == "POST":
        offer_form = OfferForm(request.POST)
        
        if offer_form.is_valid():
            offer_instance = offer_form.save(commit=False)
            offer_instance.offered_by = request.user
            offer_instance.property = Property.objects.get(pk=property_id)
            offer_instance.save()

    elif request.method == "GET":
        offer_form = OfferForm()
    
    return render(
        request, "properties/create_offers.html", {"offer_form":offer_form}
    )

@login_required
def view_incoming_offers(request):
    if request.method == "GET":
        properties = Property.objects.filter(owner=request.user, is_active=True).prefetch_related('offers')
        active_offers = [
            offer 
            for property in properties 
            for offer in property.offers.filter(is_active=True, state="pending")
        ]
        
        return render(
            request, "properties/view_offers.html",
            {"offers": active_offers, "path": request.path}
        )

@login_required
def view_created_offer(request):
    if request.method == "GET":
        response = render(
            request, "properties/view_offers.html",
            {
                "offers": PropertyOffers.objects.filter(
                    is_active=True, offered_by=request.user, state="pending"
                ),
                "path": request.path
            }
        )
    elif request.method == "POST":
        offer_id = request.POST.get("offer_id", None)
        offer = get_object_or_404(
            PropertyOffers, pk=offer_id, is_active=True, state="pending"
        )
        offer.is_active = False
        offer.save()
        response = render(
                request, "properties/view_offers.html",
                {
                    "offers": PropertyOffers.objects.filter(
                        is_active=True, offered_by=request.user
                    ),
                    "path": request.path
                }
            )
    
    return response
        
@login_required
def change_offer_state(request, offer_id):
    offer = get_object_or_404(PropertyOffers, pk=offer_id)
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "accept":
            offer.to_state_accepted()
            offer.save()
            messages.success(request, "Offer has been accepted.")
            
        elif action == "reject":
            offer.to_state_rejected()
            offer.save()
            messages.success(request, "Offer has been rejected.")
            
    return redirect('view_incoming_offers')
