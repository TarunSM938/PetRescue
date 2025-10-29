from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from typing import cast
from django.db import models

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, FoundPetForm
from .models import User, Profile, Pet, Request

# Home page view
# Displays the main landing page with featured content and calls to action

def home(request):
    """
    Render the homepage with current datetime for footer copyright.
    """
    context = {
        'now': timezone.now()
    }
    return render(request, 'home.html', context) 


# Adopt page view
# Shows available pets for adoption (requires user authentication)

@login_required
def adopt(request):
    """
    Display pets available for adoption.
    Requires user to be logged in.
    """
    context = {
        'now': timezone.now()
    }
    return render(request, 'adopt.html', context)


# Donate page view
# Information about supporting the pet rescue mission through donations

def donate(request):
    """
    Display donation information to support the pet rescue mission.
    """
    context = {
        'now': timezone.now()
    }
    return render(request, 'donate.html', context)


# User registration view
# Handles new user signups with form validation and profile creation

def register(request):
    """
    Handle user registration with custom form validation.
    Creates user accounts and processes additional profile information.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            
            # Handle additional fields (full name and phone)
            full_name = request.POST.get('full_name', '')
            phone = request.POST.get('phone', '')
            
            # Update user's phone number if provided
            if phone:
                user.phone_number = phone
                user.save()
            
            # Process full name if provided
            if full_name:
                names = full_name.split(' ', 1)
                if len(names) == 2:
                    # If we have both first and last name, we could save them
                    # This is left as an enhancement for future implementation
                    pass
            
            username = cast(User, user).username  # Fix Pyright warning
            messages.success(request, f'Welcome to PetRescue, {username}! Your account has been created successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below to create your account.')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})


# User login view
# Authenticates users and manages session login

def user_login(request):
    """
    Handle user authentication and login.
    Validates credentials and creates user session.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}! You have been successfully logged in.')
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password. Please try again.")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


# User logout view
# Ends user session and redirects to homepage

def user_logout(request):
    """
    Log out the current user and end their session.
    """
    username = request.user.username if request.user.is_authenticated else "User"
    logout(request)
    messages.info(request, f'Goodbye, {username}! You have been successfully logged out.')
    return redirect('home')


# User profile view
# Allows users to view and update their profile information

@login_required
def profile(request):
    """
    Display and update user profile information.
    Requires user to be logged in.
    """
    # Ensure the user has a profile
    from django.apps import apps
    ProfileModel = apps.get_model('main', 'Profile')
    profile_obj, created = ProfileModel.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_obj)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile_obj)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile.html', context)


# Email validation view
# Provides AJAX endpoint for real-time email availability checking

def validate_email(request):
    """
    AJAX endpoint to check if an email address is already taken.
    Used for real-time form validation during registration.
    """
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)


# Report found pet view
# Allows authenticated users to report found pets

@login_required
def report_found_pet(request):
    """
    Handle reporting of found pets.
    Displays form for reporting found pets and processes submissions.
    """
    if request.method == 'POST':
        form = FoundPetForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the pet object
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.status = 'found'  # Set status to found
            pet.save()
            
            # Create a request record linking the pet to the user
            # Using apps.get_model to avoid potential naming conflicts
            from django.apps import apps
            RequestModel = apps.get_model('main', 'Request')
            RequestModel.objects.create(
                user=request.user,
                pet=pet,
                request_type='found',  # Found pet report
                phone_number=request.user.phone_number or '',  # Use user's phone number if available
                message=f"Found pet report for {pet.pet_type} near {pet.location}"
            )
            
            messages.success(request, 'Thank you for reporting this found pet! Our team will review your submission.')
            return redirect('report_success')  # Redirect to success page
        else:
            # Add form errors to messages for better user feedback
            messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = FoundPetForm()
    
    context = {
        'form': form,
        'now': timezone.now()
    }
    return render(request, 'report_found_pet.html', context)


# Success page view
# Shows confirmation after successful pet report submission

def report_success(request):
    """
    Display success page after pet report submission.
    """
    return render(request, 'success.html')
