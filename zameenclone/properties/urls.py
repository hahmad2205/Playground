from django.urls import path
from . import views

urlpatterns = [
    path("marketplace/", views.marketplace, name="marketplace"),
    path("properties/", views.properties, name="properties"),
    path("add_property/", views.app_property, name="add_property")
]
