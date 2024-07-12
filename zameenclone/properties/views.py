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
            get_object_or_404(Property, pk=request.POST["property_id"], is_active=True).save()
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
        request, "properties/property_details.html", {"property": property, "owner":property.owner==request.user}
    )

@login_required
def create_offer(request, property_id):
    if request.method == "POST":
        property = get_object_or_404(Property, pk=property_id)
        offer_form = OfferForm(request.POST)
        
        if offer_form.is_valid():
            offer = offer_form.save(commit=False)
            offer.save(offered_by=request.user, property=property)

    elif request.method == "GET":
        offer_form = OfferForm()
    
    return render(
        request, "properties/create_offers.html", {"offer_form":offer_form}
    )

@login_required
def view_property_offers(request):
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
        return render(
            request, "properties/view_offers.html",
            {
                "offers": PropertyOffers.objects.filter(
                    is_active=True, offered_by=request.user, state="pending"
                ),
                "path": request.path
            }
        )
        
@login_required
def change_offer_state(request, offer_id):
    offer = get_object_or_404(PropertyOffers, pk=offer_id)
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "accept":
            offer.mark_accepted()
            offer.save()
            messages.success(request, "Offer has been accepted.")
            
        elif action == "reject":
            offer.mark_rejected()
            offer.save()
            messages.success(request, "Offer has been rejected.")
            
    return redirect('view_incoming_offers')

@login_required
def withdraw_offer(request, offer_id):
    if request.method == "POST":
        offer = get_object_or_404(
                    PropertyOffers, pk=offer_id, is_active=True, state="pending"
                )
        offer.is_active = False
        offer.save()
    
    return redirect("view_created_offer")