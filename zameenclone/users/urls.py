from django.urls import path
from users.views import simple_views

urlpatterns = [
    # simple views
    path("login", simple_views.login_user, name="login"),
    path("logout/", simple_views.logout_user, name="logout")
    
    # api views
]
