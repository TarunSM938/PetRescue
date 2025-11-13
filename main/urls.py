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
    
    # Pet search page - browse pets available for adoption
    # Requires user authentication
    path('find-pets/', views.adopt, name='find_pets'),
    
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
    
    # User requests dashboard - view all user's pet reports
    # Requires user authentication
    path('my-requests/', views.user_requests, name='user_requests'),
    path('my-requests/edit/<int:pet_id>/', views.edit_user_request, name='edit_user_request'),
    path('my-requests/delete/<int:pet_id>/', views.delete_user_request, name='delete_user_request'),
    
    # API endpoints for dashboard
    path('api/dashboard/requests/', views.api_user_requests, name='api_user_requests'),
    path('api/requests/<int:pet_id>/', views.api_edit_request, name='api_edit_request'),
    path('api/requests/<int:pet_id>/delete/', views.api_delete_request, name='api_delete_request'),
    path('api/requests/<int:pet_id>/history/', views.api_request_history, name='api_request_history'),
    
    # AJAX endpoint for email validation during registration
    path('validate-email/', views.validate_email, name='validate_email'),
    
    # Report found pet page - allows users to report found pets
    # Requires user authentication
    path('report-found-pet/', views.report_found_pet, name='report_found_pet'),
    
    # Report lost pet page - allows users to report lost pets
    # Requires user authentication
    path('report-lost-pet/', views.report_lost_pet, name='report_lost_pet'),
    
    # Success page after reporting a pet
    path('report-success/', views.report_success, name='report_success'),
    # Success page after reporting a lost pet
    path('report-lost-success/', views.report_lost_success, name='report_lost_success'),
    # Success page after reporting a found pet
    path('report-found-success/', views.report_found_success, name='report_found_success'),
    
    # Admin Dashboard URLs
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/pending-requests/', views.admin_pending_requests, name='admin_pending_requests'),
    path('dashboard/admin/accepted-requests/', views.admin_accepted_requests, name='admin_accepted_requests'),
    path('dashboard/admin/rejected-requests/', views.admin_rejected_requests, name='admin_rejected_requests'),
    path('dashboard/admin/update-request-status/<int:request_id>/', views.update_request_status, name='update_request_status'),
]