from django.urls import path
from . import views

urlpatterns = [
    path("marketplace/", views.marketplace, name="marketplace"),
    path("properties/", views.properties, name="properties"),
    path("propertydetails/<int:property_id>/", views.property_detail, name="property_detail")
]
