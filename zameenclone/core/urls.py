from django.urls import path

from rest_framework.routers import DefaultRouter

from core.views import simple_views
# from core.views.api_views import *
# from core.views.generic_api_views import *
from core.views.view_sets import *

app_name = 'core'
router = DefaultRouter()
router.register(r'amenity', AmenityListAPIView, basename='amenity-list')
router.register(r'amenity/(?P<pk>\d+)/options', AmenityOptionListAPIView, basename='amenity-options')

urlpatterns = router.urls


# urlpatterns = [
#     # simple views
#     path('get-amenity-options/', simple_views.get_amenity_options, name='get_amenity_options'),
#
#     path("amenity/", AmenityListAPIView.as_view(), name="amenities"),
#     path("amenity/<int:pk>/options/", AmenityOptionListAPIView.as_view(), name="amenity_options"),
# ]



