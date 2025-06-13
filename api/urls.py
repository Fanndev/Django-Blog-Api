from django.urls import path
from .views import  BeritaDetailView, BeritaListCreateView, TagListCreateView, TagDetailView


urlpatterns = [
    path('berita', BeritaListCreateView.as_view(), name='berita-list-create'),
    path('berita/<int:pk>', BeritaDetailView.as_view(), name='berita-detail'),
    path('tag', TagListCreateView.as_view(), name='tag-list-create'),
    path('tag/<int:pk>', TagDetailView.as_view(), name='tag-detail'),
]