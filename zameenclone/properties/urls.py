from django.urls import path
from . import views

urlpatterns = [
    path("marketplace/", views.marketplace, name="marketplace"),
    path("", views.properties, name="properties"),
    path("add_property/", views.add_property, name="add_property"),
    path("<int:property_id>/", views.property_detail, name="property_detail"),
    path("<int:property_id>/create_offer/", views.create_offer, name="create_offer"),
    path("offers/", views.view_property_offers, name="view_property_offers"),
    path("created-offers/", views.view_created_offer, name="view_created_offer"),
    path('offer/<int:offer_id>/state/', views.change_offer_state, name='change_offer_state'),
    path("offer/<int:offer_id>/withdraw/", views.withdraw_offer, name="withdraw_offer")
]
