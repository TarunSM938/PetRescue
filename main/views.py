from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from typing import cast
from django.db import models

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import User, Profile


# -----------------------------
# Home page
# -----------------------------
def home(request):
    context = {
        'now': timezone.now()
    }
    return render(request, 'home.html', context) 


# -----------------------------
# Register new user
# -----------------------------
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            username = cast(User, user).username  # Fix Pyright warning
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})


# -----------------------------
# Login user
# -----------------------------
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# -----------------------------
# Logout user
# -----------------------------
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


# -----------------------------
# Profile view
# -----------------------------
@login_required
def profile(request):
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
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile_obj)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile.html', context)


# -----------------------------
# Email validation (for AJAX)
# -----------------------------
def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)
