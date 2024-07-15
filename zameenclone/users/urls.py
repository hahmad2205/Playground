from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.urls import path
from users.views import simple_views

urlpatterns = [
    # simple views
    path("login", simple_views.login_user, name="login"),
    path("logout/", simple_views.logout_user, name="logout"),
    
    # api views
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
