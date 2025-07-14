from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
import logging

from django.contrib.auth import get_user_model
from api.models import Berita, Tag, Comment
from api.permission import IsAdminOrReadOnly
from .serializers import (
    BeritaSerializer, 
    UserSerializer, 
    CustomTokenObtainPairSerializer,
    TagSerializer,
    CommentSerializer
)

User = get_user_model()

# Response Export
class BaseResponseMixin:
    def permission_denied(self, request, message=None, code=None):
        logging.error(f"Permission denied: {message}, Code: {code}, User: {request.user}")
        raise PermissionDenied(detail="You do not have permission.")
    
    def custom_response(self, data, message="Success", status=True):
        return Response({
            "status": status,
            "message": message,
            "data": data
        })

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return self.custom_response(response.data, message="Created successfully")

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return self.custom_response(response.data, message="Retrieved successfully")

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return self.custom_response(response.data, message="Updated successfully")

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.custom_response(None, message="Deleted successfully")

# Custom Pagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "status": True,
            "message": "Get list successfully",
            "data": data,
            "pagination": {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.page.paginator.count,
                "num_pages": self.page.paginator.num_pages,
            }
        })

# Register User
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    ordering = ['-created_at']

#  Login
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Berita
class BeritaListCreateView(BaseResponseMixin, generics.ListCreateAPIView):
    queryset = Berita.objects.all().order_by('-created_at')
    serializer_class = BeritaSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        # pastikan hanya user login yang boleh create
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            self.permission_denied(self.request, message="Authentication required to create Berita.")

class BeritaDetailView(BaseResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Berita.objects.all()
    serializer_class = BeritaSerializer
    permission_classes = [AllowAny]
    ordering = ['-created_at']

    def update(self, request, *args, **kwargs):
        # batasi update hanya untuk admin
        if not request.user.is_staff:
            self.permission_denied(request, message="Admin privileges required to update Berita.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # batasi delete hanya untuk admin
        if not request.user.is_staff:
            self.permission_denied(request, message="Admin privileges required to delete Berita.")
        return super().destroy(request, *args, **kwargs)

#Tag
class TagListCreateView(BaseResponseMixin, generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    ordering = ['-created_at']

class TagDetailView(BaseResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering = ['-created_at']


# User harus login untuk akses dan buat komentar
class CommentListCreateView(BaseResponseMixin, generics.ListCreateAPIView):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Admin bisa edit/hapus komentar, user biasa tidak bisa
class CommentDetailView(BaseResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]