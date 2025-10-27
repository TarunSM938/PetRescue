from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import Profile, LostPet, FoundPet
from django.db.models import Q
from .forms import ProfileForm


# -----------------------------
# Home Page
# -----------------------------
def home_view(request):
    query = request.GET.get('query', '')

    # Filter LostPet and FoundPet if search query exists
    if query:
        lost_pets = LostPet.objects.filter(
            Q(name__icontains=query) | Q(species__icontains=query) |
            Q(breed__icontains=query) | Q(last_seen_location__icontains=query)
        ).order_by('-created_at')[:3]

        found_pets = FoundPet.objects.filter(
            Q(name__icontains=query) | Q(species__icontains=query) |
            Q(breed__icontains=query) | Q(last_seen_location__icontains=query)
        ).order_by('-created_at')[:3]
    else:
        lost_pets = LostPet.objects.all().order_by('-created_at')[:3]
        found_pets = FoundPet.objects.all().order_by('-created_at')[:3]

    recent_pets = list(lost_pets) + list(found_pets)

    return render(request, 'pet/home.html', {'recent_pets': recent_pets})


# -----------------------------
# Logout
# -----------------------------
def logout_view(request):
    logout(request)
    return redirect('login')


# -----------------------------
# Register
# -----------------------------
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, 'pet/register.html', {'form': form})


# -----------------------------
# Login
# -----------------------------
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password.')
            print(form.errors)
    else:
        form = AuthenticationForm()

    return render(request, 'pet/login.html', {'form': form})


# -----------------------------
# Profile
# -----------------------------
@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'pet/profile.html', {'profile': profile})
@login_required
def report_lost_pet(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        species = request.POST.get('species')
        breed = request.POST.get('breed')
        last_seen_location = request.POST.get('last_seen_location')
        image = request.FILES.get('image')
        LostPet.objects.create(
            owner=request.user,
            name=name,
            species=species,
            breed=breed,
            last_seen_location=last_seen_location,
            image=image
        )
        messages.success(request, 'Lost pet reported successfully!')
        return redirect('home')
    return render(request, 'pet/report_lost_pet.html')

@login_required
def report_found_pet(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        species = request.POST.get('species')
        breed = request.POST.get('breed')
        found_location = request.POST.get('found_location')
        image = request.FILES.get('image')
        contact_info = request.POST.get("contact_info")
        FoundPet.objects.create(
            finder=request.user,
            name=name,
            species=species,
            breed=breed,
            found_location=found_location,
            contact_info=contact_info,
            image=image
        )
        messages.success(request, 'Found pet reported successfully!')
        return redirect('home')
    return render(request, 'pet/report_found_pet.html')
@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'pet/edit_profile.html', {'form': form})

