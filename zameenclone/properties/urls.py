from django.urls import path
from . import views

urlpatterns = [
    path("", views.marketplace_listings, name="marketplace_listing")
]
