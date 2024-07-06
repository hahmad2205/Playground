from django.urls import path
from . import views

urlpatterns = [
    path("", views.marketplace_listings, name="marketplace_listing"),
    path("my_listings/", views.my_listings, name="my_listings")
]
