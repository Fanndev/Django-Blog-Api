from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import filters

from django.contrib.auth import get_user_model
from api.models import Berita, Tag
from api.permission import IsAdminOrReadOnly
from .serializers import (
    BeritaSerializer, 
    UserSerializer, 
    CustomTokenObtainPairSerializer,
    TagSerializer
)

User = get_user_model()

# Response Export
class BaseResponseMixin:
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

#  Login
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class BeritaListCreateView(BaseResponseMixin, generics.ListCreateAPIView):
    queryset = Berita.objects.all().order_by('-created_at')
    serializer_class = BeritaSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BeritaDetailView(BaseResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Berita.objects.all()
    serializer_class = BeritaSerializer
    permission_classes = [IsAdminOrReadOnly]

#Tag
class TagListCreateView(BaseResponseMixin, generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class TagDetailView(BaseResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
