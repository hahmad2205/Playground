from django.urls import path

from properties.views import simple_views
from properties.views.api_views import *

urlpatterns = [
    # simple views
    path("marketplace/", simple_views.marketplace, name="marketplace"),
    path("", simple_views.properties, name="properties"),
    path("add_property/", simple_views.add_property, name="add_property"),
    path("<int:property_id>/", simple_views.property_detail, name="property_detail"),
    path("<int:property_id>/create_offer/", simple_views.create_offer, name="create_offer"),
    path("offers/", simple_views.view_property_offers, name="view_property_offers"),
    path("created-offers/", simple_views.view_created_offer, name="view_created_offer"),
    path('offer/<int:offer_id>/state/', simple_views.change_offer_state, name='change_offer_state'),
    path("offer/<int:offer_id>/withdraw/", simple_views.withdraw_offer, name="withdraw_offer"),
    
    # api views
    path("api/marketplace/", PropertyMarketplaceListAPIView.as_view(), name="marketplace_api"),
    path("api/", PropertyListAPIView.as_view(), name="properties_api"),
    path("api/offers/<int:id>/", PropertyOfferCreateAPIView.as_view(), name="create_offer_api"),
    path("api/offers/", PropertyOfferListAPIView.as_view(), name="get_offers_api"),
    path("api/<int:id>/offers/", PropertyOfferFromPropertyListAPIView.as_view(), name="get_property_offers_api"),
    path("api/update-offers/<int:id>/", PropertyOfferUpdateStateAPIView.as_view(), name="update_state"),
    path("api/offers/withdraw/<int:id>/", PropertyOfferWithdrawAPIView.as_view(), name="withdraw_offer_api"),
]
