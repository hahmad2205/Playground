from django.urls import path
from core.views import simple_views

app_name = 'core'
urlpatterns = [
    # simple views
    path('get-amenity-options/', simple_views.get_amenity_options, name='get_amenity_options'),
    
    # api views
]
