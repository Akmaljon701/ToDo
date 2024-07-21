from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from user.views import (CustomTokenObtainPairView, create_user, update_current_user, get_current_user)

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='user_token_refresh'),

    path('login/', CustomTokenObtainPairView.as_view(), name='user_login'),
    path('create/', create_user, name='create_user'),
    path('current_update/', update_current_user, name='update_current_user'),
    path('current/', get_current_user, name='get_current_user'),
]
