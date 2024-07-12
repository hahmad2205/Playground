from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('get-amenity-options/', views.get_amenity_options, name='get_amenity_options'),
]
