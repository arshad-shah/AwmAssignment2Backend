from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from MosqueFinder.views import UpdateLocation, RegisterView, UpdatePasswordView, UpdateUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/update-location/', UpdateLocation.as_view(), name='update_location'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/update-password/', UpdatePasswordView.as_view(), name='update_password'),
    path('api/update-user/', UpdateUserView.as_view(), name='update_user'),
]
