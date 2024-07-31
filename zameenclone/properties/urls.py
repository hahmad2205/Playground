from django.urls import path, include
from rest_framework.routers import DefaultRouter

from properties.views import simple_views
# from properties.views.api_views import *
# from properties.views.generic_api_views import *
from properties.views.view_sets import *

router = DefaultRouter()
urlpatterns = [
    path("marketplace/", PropertyMarketplaceListAPIView.as_view({"get": "list"}), name="marketplace_generic_api"),
    path("", PropertyListAPIView.as_view({"get": "list"}), name="properties"),
    path("offer/create/", PropertyOfferCreateAPIView.as_view(({"post": "create"})), name="create_offer"),
    path("offers/", PropertyOfferListAPIView.as_view({"get": "list"}), name="get_offers_generic_api"),
    path(
        "<int:pk>/offers/",
        PropertyOfferFromPropertyListAPIView.as_view({"get": "list"}),
        name="get_property_offers_generic_api"
    ),
    path("<int:pk>", PropertyDetailAPIView.as_view({"get": "retrieve"}), name="property"),
    path("offers/withdraw/<int:pk>/",
         PropertyOfferWithdrawAPIView.as_view({"patch": "partial_update"}),
         name="withdraw_offer_api"),
    path("add/", PropertyCreateAPIView.as_view({"post": "create"}), name="add_property"),
    path(
        "update-offers/<int:pk>/",
        PropertyOfferUpdateStateAPIView.as_view({"patch": "partial_update"}),
        name="update_state"
    ),
    path(
        "<int:pk>/update/",
        PropertyUpdateAPIView.as_view({"patch": "partial_update"}),
        name="update_property"
    ),
]

# urlpatterns = [
#     # simple views
#     # path("marketplace/", simple_views.marketplace, name="marketplace"),
#     # path("", simple_views.properties, name="properties"),
#     # path("add_property/", simple_views.add_property, name="add_property"),
#     # path("<int:property_id>/", simple_views.property_detail, name="property_detail"),
#     # path("<int:property_id>/create_offer/", simple_views.create_offer, name="create_offer"),
#     # path("offers/", simple_views.view_property_offers, name="view_property_offers"),
#     # path("created-offers/", simple_views.view_created_offer, name="view_created_offer"),
#     # path('offer/<int:offer_id>/state/', simple_views.change_offer_state, name='change_offer_state'),
#     # path("offer/<int:offer_id>/withdraw/", simple_views.withdraw_offer, name="withdraw_offer"),
#
#
#     path("marketplace/", PropertyMarketplaceListAPIView.as_view(), name="marketplace_generic_api"),
#     path("<int:pk>", PropertyDetailAPIView.as_view(), name="property"),
#     path("", PropertyListAPIView.as_view(), name="properties_generic_api"),
#     path("offer/create/", PropertyOfferCreateAPIView.as_view(), name="create_offer_generic_api"),
#     path(
#         "<int:pk>/offers/",
#         PropertyOfferFromPropertyListAPIView.as_view(),
#         name="get_property_offers_generic_api"
#     ),
#     path("offers/", PropertyOfferListAPIView.as_view(), name="get_offers_generic_api"),
#     path("update-offers/<int:pk>/", PropertyOfferUpdateStateAPIView.as_view(), name="update_state"),
#     path("offers/withdraw/<int:pk>/", PropertyOfferWithdrawAPIView.as_view(), name="withdraw_offer_api"),
#     path("<int:pk>/update/", PropertyUpdateAPIView.as_view(), name="update_property"),
#     path("add/", PropertyCreateAPIView.as_view(), name="add_property")
# ]
