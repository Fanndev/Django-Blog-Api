from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import  BeritaDetailView, BeritaListCreateView, TagListCreateView, TagDetailView, CommentListCreateView, CommentDetailView


urlpatterns = [
    path('berita', BeritaListCreateView.as_view(), name='berita-list-create'),
    path('berita/<int:pk>', BeritaDetailView.as_view(), name='berita-detail'),
    path('tag', TagListCreateView.as_view(), name='tag-list-create'),
    path('tag/<int:pk>', TagDetailView.as_view(), name='tag-detail'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)