from django.contrib import admin
from django.urls import path, include
from api.views import CreateUserView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('api/v1/auth/register', CreateUserView.as_view(), name='register'),
    path('api/v1/auth/login', CustomTokenObtainPairView.as_view(), name='login'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('api-auth/', include('rest_framework.urls')),
]
