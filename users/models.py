from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    tel = models.CharField(max_length=20, unique=True, blank=True, null=True)
    # passwordはAbstractUserで管理するため定義不要
    display_name = models.CharField(max_length=50, blank=True, null=True)
    bio = models.CharField(max_length=160, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    avatar_image = models.ImageField(upload_to='avatar_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
