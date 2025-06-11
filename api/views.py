from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

@api_view(['GET'])
def get_users(request):
    dummy_user = {
        "id": 1,
        "username": "johndoe",
        "email": "johndoe@example.com"
    }
    return Response(dummy_user)


@api_view(['GET'])
def get_tags(request):
    return Response(UserSerializer({"name": "John Doe"}).data, status=status.HTTP_200_OK)