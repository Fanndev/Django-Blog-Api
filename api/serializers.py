from tokenize import Comment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # type: ignore
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Berita, Tag, User
from django.contrib.auth import get_user_model

User = get_user_model()

# user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
# custom user
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        user = self.user

        data = {
            "token": data["access"],
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role,
                "last_login": user.last_login,
            }
        }

        return data
    
# Tag
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

# berita
class BeritaSerializer(serializers.ModelSerializer):
    tags_data = TagSerializer(source='tags', many=True, read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Berita
        fields = [
            'id', 'title', 'isi', 'created_at', 'updated_at',
            'tags_data', 'author_username', 'author', 'tags'
        ]

# Comment
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'