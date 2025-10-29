"""
URL configuration for the main application.

This module defines the URL patterns for all views in the PetRescue application,
including authentication, pet listings, user profiles, and support pages.
"""

from django.urls import path
from . import views

# URL patterns for the main application
urlpatterns = [
    # Home page - the main landing page for the site
    path('', views.home, name='home'),
    
    # Pet adoption page - browse pets available for adoption
    # Requires user authentication
    path('adopt/', views.adopt, name='adopt'),
    
    # Donation page - information about supporting the rescue mission
    path('donate/', views.donate, name='donate'),
    
    # User authentication URLs
    # Registration page for new users
    path('register/', views.register, name='register'),
    
    # Login page for existing users
    path('login/', views.user_login, name='login'),
    
    # Logout endpoint to end user sessions
    path('logout/', views.user_logout, name='logout'),
    
    # User profile page - view and update personal information
    # Requires user authentication
    path('profile/', views.profile, name='profile'),
    
    # AJAX endpoint for email validation during registration
    path('validate-email/', views.validate_email, name='validate_email'),
    
    # Report found pet page - allows users to report found pets
    # Requires user authentication
    path('report-found-pet/', views.report_found_pet, name='report_found_pet'),
    
    # Success page after reporting a found pet
    path('report-success/', views.report_success, name='report_success'),
]