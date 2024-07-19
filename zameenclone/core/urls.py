from django.urls import path
from core.views import simple_views
from core.views.api_views import *

app_name = 'core'
urlpatterns = [
    # simple views
    path('get-amenity-options/', simple_views.get_amenity_options, name='get_amenity_options'),
    
    # api views
    path("amenity/", AmenityListAPIView.as_view(), name="amenity_type"),
    path("amenity-options/<int:id>", AmenityOptionListAPIView.as_view(), name="amenity_options"),
]
