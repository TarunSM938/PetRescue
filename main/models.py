from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


# -----------------------------
#  Custom User Model
# -----------------------------
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    def __str__(self):
        return self.username


# -----------------------------
#  Pet Model
# -----------------------------
class Pet(models.Model):
    PET_STATUS = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pet_type = models.CharField(max_length=50)  # e.g., Dog, Cat
    breed = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='pet_images/', blank=True, null=True)
    status = models.CharField(max_length=5, choices=PET_STATUS, default='lost')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet_type} - {self.breed} ({self.status})"


# -----------------------------
#  Request Model (connects User and Pet)
# -----------------------------
class Request(models.Model):
    REQUEST_TYPE = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPE)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.request_type} - {self.pet.pet_type}"
