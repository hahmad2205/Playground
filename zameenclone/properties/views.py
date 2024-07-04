from django.shortcuts import render

def marketplace_listings(request):
    return render(request, "properties/marketplace_listing.html", {})
