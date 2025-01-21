from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
