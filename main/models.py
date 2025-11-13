from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from typing import cast

# Custom User Model
# Extends Django's AbstractUser to add a phone number field for better user contact

class User(AbstractUser):
    """
    Custom User model for PetRescue application.
    Extends Django's built-in User model with additional fields specific to pet rescue.
    """
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    def __str__(self):
        return self.username


# User Profile Model
# Stores additional information about users that isn't part of the authentication system

class Profile(models.Model):
    """
    User profile model to store additional information about users.
    Each user has one profile created automatically upon registration.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, help_text="Tell us about your experience with pets")
    location = models.CharField(max_length=30, blank=True, help_text="City or area where you live")
    birth_date = models.DateField(null=True, blank=True, help_text="Your birth date (optional)")

    def __str__(self):
        user = cast('User', self.user)
        return f"{user.username}'s Profile"



# Pet Model
# Represents pets in the system, whether they are lost, found, or available for adoption

class Pet(models.Model):
    """
    Pet model to represent animals in the system.
    Can be used for lost/found reports or adoption listings.
    """
    PET_STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
        ('adoptable', 'Available for Adoption'),
    ]

    PET_TYPES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('other', 'Other'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                             help_text="The user who reported this pet")
    pet_type = models.CharField(max_length=50, choices=PET_TYPES, 
                               help_text="Type of pet")
    breed = models.CharField(max_length=50, help_text="Breed of the pet (if known)")
    color = models.CharField(max_length=50, help_text="Primary color of the pet")
    location = models.CharField(max_length=100, help_text="Location where pet was lost/found")
    description = models.TextField(blank=True, help_text="Additional details about the pet")
    image = models.ImageField(upload_to='pet_images/', blank=True, null=True, 
                             help_text="Photo of the pet (optional)")
    status = models.CharField(max_length=10, choices=PET_STATUS_CHOICES, default='lost',
                             help_text="Current status of the pet")
    created_at = models.DateTimeField(auto_now_add=True, 
                                     help_text="When this pet record was created")

    def __str__(self):
        return f"{self.pet_type} - {self.breed} ({self.status})"



# Request Model
# Tracks user requests related to pets (lost/found reports, adoption inquiries)

class Request(models.Model):
    """
    Request model to track user interactions with pets.
    Used for lost/found reports and adoption inquiries.
    """
    REQUEST_TYPES = [
        ('lost', 'Lost Pet Report'),
        ('found', 'Found Pet Report'),
        ('adoption', 'Adoption Inquiry'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                            help_text="User making the request")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE,
                           help_text="Pet this request is related to")
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPES,
                                   help_text="Type of request being made")
    phone_number = models.CharField(max_length=15, 
                                   help_text="Phone number for contact about this request")
    message = models.TextField(blank=True, 
                              help_text="Additional message or information (optional)")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending',
                             help_text="Current status of the request")
    created_at = models.DateTimeField(auto_now_add=True,
                                     help_text="When this request was created")

    def __str__(self):
        user = cast('User', self.user)
        pet = cast('Pet', self.pet)
        return f"{user.username} - {self.request_type} - {pet.pet_type}"


# Activity Log Model
# Tracks all activities related to pet reports for history/timeline functionality

class ActivityLog(models.Model):
    """
    Activity log model to track all activities related to pet reports.
    Records events such as creation, edits, status changes, and deletions.
    """
    ACTIVITY_TYPES = [
        ('created', 'Created'),
        ('edited', 'Edited'),
        ('status_changed', 'Status Changed'),
        ('deleted', 'Deleted'),
    ]
    
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, 
                           help_text="The pet this activity is related to")
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES,
                                   help_text="Type of activity")
    timestamp = models.DateTimeField(auto_now_add=True,
                                   help_text="When this activity occurred")
    actor = models.CharField(max_length=50, 
                            help_text="Who performed the action (user, admin, system)")
    details = models.TextField(blank=True,
                              help_text="Additional details about the activity")
    
    class Meta:
        ordering = ['-timestamp']  # Latest first
    
    def __str__(self):
        pet = cast('Pet', self.pet)
        return f"{pet.breed} - {self.activity_type} - {self.timestamp}"


# Notification Model
# Tracks admin notifications for new pet reports

class Notification(models.Model):
    """
    Notification model to track admin notifications for new pet reports.
    """
    NOTIFICATION_TYPES = [
        ('lost_report', 'Lost Pet Report'),
        ('found_report', 'Found Pet Report'),
    ]
    
    request = models.ForeignKey('Request', on_delete=models.CASCADE,
                               help_text="The request this notification is related to")
    message = models.TextField(help_text="Notification message")
    created_at = models.DateTimeField(auto_now_add=True,
                                    help_text="When this notification was created")
    is_read = models.BooleanField(default=False,
                                 help_text="Whether this notification has been read")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES,
                                       help_text="Type of notification")
    
    class Meta:
        ordering = ['-created_at']  # Latest first
    
    def __str__(self):
        request = cast('Request', self.request)
        return f"Notification for {request.request_type} - {self.created_at}"


# Signal Handlers
# Automatically create and save user profiles when users are created/updated

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a profile for new users.
    """
    if created:
        from django.apps import apps
        ProfileModel = apps.get_model('main', 'Profile')
        ProfileModel.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    Automatically saves the user's profile when the user is saved.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()