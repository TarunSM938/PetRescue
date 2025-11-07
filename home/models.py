from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Custom User Model

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username



# Pet Model

class Pet(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
        ('adopted', 'Adopted'),
        ('available', 'Available'),
    ]

    TYPE_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('other', 'Other'),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    breed = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='pets/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')

    def __str__(self):
        return f"{self.type.capitalize()} - {self.breed}"



# Request Model

class Request(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('lost', 'Lost Report'),
        ('found', 'Found Report'),
        ('adoption', 'Adoption Request'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='requests')
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.pet.breed} ({self.request_type})"


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username
