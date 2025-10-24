from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from typing import cast

# -----------------------------
# Custom User Model
# -----------------------------
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    def __str__(self):
        return self.username


# -----------------------------
# Profile Model
# -----------------------------
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        user = cast('User', self.user)
        return f"{user.username}'s Profile"


# -----------------------------
# Pet Model
# -----------------------------
class Pet(models.Model):
    PET_STATUS = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pet_type = models.CharField(max_length=50)
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
# Request Model
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
        user = cast('User', self.user)
        pet = cast('Pet', self.pet)
        return f"{user.username} - {self.request_type} - {pet.pet_type}"


# -----------------------------
# Signals
# -----------------------------
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
