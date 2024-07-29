from django.urls import path
from core.views import simple_views
from core.views.generic_api_views import *

app_name = 'core'
urlpatterns = [
    # simple views
    path('get-amenity-options/', simple_views.get_amenity_options, name='get_amenity_options'),
    
    # api views
    # path("amenity/", AmenityListAPIView.as_view(), name="amenities"),
    # path("amenity/<int:id>/options/", AmenityOptionListAPIView.as_view(), name="amenity_options"),

    # generic api views
    path("amenity/", AmenityListAPIView.as_view(), name="amenities"),
    path("amenity/<int:pk>/options/", AmenityOptionListAPIView.as_view(), name="amenity_options"),
]
