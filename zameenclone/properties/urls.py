from django.urls import path
from . import views

urlpatterns = [
    path("marketplace/", views.marketplace, name="marketplace"),
    path("", views.properties, name="properties"),
    path("add_property/", views.add_property, name="add_property"),
    path("<int:property_id>/", views.property_detail, name="property_detail")
]
