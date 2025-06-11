from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# User Models
class User(AbstractUser):
    pass

# Tag Models
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Berita Models
class Berita(models.Model):
    title = models.CharField(max_length=255)
    isi = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='berita')
    tags = models.ManyToManyField(Tag, related_name='berita')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Comment Models
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    berita = models.ForeignKey(Berita, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.berita.title[:20]}"
