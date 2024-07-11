from django.urls import path
from . import views

urlpatterns = [
    path("marketplace/", views.marketplace, name="marketplace"),
    path("", views.properties, name="properties"),
    path("<int:property_id>/", views.property_detail, name="property_detail"),
    path("<int:property_id>/create_offer", views.create_offer, name="create_offer")
]
