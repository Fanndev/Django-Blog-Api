from django.urls import path
from .views import get_tags, get_users


urlpatterns = [
    path('users/', get_users, name='get_users'),
    path('tags/', get_tags, name='get_tags'),
]