from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from typing import cast
from django.db import models
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.apps import apps

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, FoundPetForm, LostPetForm, PetSearchForm
from .models import User, Profile, Pet, Request

# Home page view
# Displays the main landing page with featured content and calls to action

def home(request):
    """
    Render the homepage with current datetime for footer copyright.
    """
    # Get model classes using apps.get_model to avoid linter issues
    PetModel = apps.get_model('main', 'Pet')
    RequestModel = apps.get_model('main', 'Request')
    
    # Get recently reported pets that have accepted requests
    # We'll get pets that have associated accepted requests, ordered by most recent
    recent_pets = PetModel.objects.filter(
        request__status='accepted'
    ).select_related('owner').order_by('-created_at')[:6]  # Limit to 6 most recent
    
    context = {
        'now': timezone.now(),
        'recent_pets': recent_pets
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
    # Get model classes using apps.get_model to avoid linter issues
    PetModel = apps.get_model('main', 'Pet')
    RequestModel = apps.get_model('main', 'Request')
    
    # Initialize the search form
    search_form = PetSearchForm(request.GET or None)
    
    # Initialize pets as empty queryset
    pets = PetModel.objects.none()
    
    # Apply filters only if form is submitted and at least one filter is provided
    if request.GET and search_form and search_form.is_valid():
        # Check if any search criteria were provided
        pet_type = search_form.cleaned_data.get('pet_type')
        breed = search_form.cleaned_data.get('breed')
        color = search_form.cleaned_data.get('color')
        location = search_form.cleaned_data.get('location')
        start_date = search_form.cleaned_data.get('start_date')
        end_date = search_form.cleaned_data.get('end_date')
        
        # Only perform search if at least one filter is provided
        if pet_type or breed or color or location or start_date or end_date:
            # Start with all found pets that have been accepted (for search results)
            pets = PetModel.objects.filter(status='found').select_related('owner')
            
            # Filter by accepted requests
            accepted_requests = RequestModel.objects.filter(status='accepted', request_type='found')
            pets = pets.filter(request__in=accepted_requests)
            
            # Apply pet type filter
            if pet_type:
                pets = pets.filter(pet_type=pet_type)
            
            # Apply breed filter with case-insensitive partial matching
            if breed:
                pets = pets.filter(breed__icontains=breed)
            
            # Apply color filter with case-insensitive partial matching and synonyms
            if color:
                # Define color synonyms
                color_synonyms = {
                    'brown': ['brown', 'tan', 'chocolate'],
                    'black': ['black', 'dark'],
                    'white': ['white', 'light'],
                    'gray': ['gray', 'grey', 'silver'],
                    'golden': ['golden', 'yellow', 'blonde'],
                    'red': ['red', 'orange', 'rust'],
                }
                
                # Check if the color has synonyms
                if color.lower() in color_synonyms:
                    color_filters = Q()
                    for synonym in color_synonyms[color.lower()]:
                        color_filters = color_filters | Q(color__icontains=synonym)
                    pets = pets.filter(color_filters)
                else:
                    pets = pets.filter(color__icontains=color)
            
            # Apply location filter with case-insensitive partial matching
            if location:
                pets = pets.filter(location__icontains=location)
            
            # Apply date range filters
            if start_date:
                pets = pets.filter(created_at__date__gte=start_date)
            if end_date:
                pets = pets.filter(created_at__date__lte=end_date)
    
    # Sort by most recent entries first (only if there are pets)
    if pets.exists():
        pets = pets.order_by('-created_at')
    
    # Get all available pets (explicitly adoptable pets and found pets with accepted requests)
    # First get explicitly adoptable pets
    adoptable_pets = PetModel.objects.filter(status='adoptable').select_related('owner')
    
    # Then get found pets with accepted requests
    accepted_found_pets = PetModel.objects.filter(
        status='found',
        request__status='accepted',
        request__request_type='found'
    ).select_related('owner')
    
    # Combine both querysets
    all_pets = adoptable_pets.union(accepted_found_pets).order_by('-created_at')
    
    context = {
        'now': timezone.now(),
        'search_form': search_form,
        'pets': pets,  # Found pets matching search criteria (empty if no search)
        'all_pets': all_pets  # All available pets
    }
    return render(request, 'find_pets.html', context)


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
            # Form is not valid, but we want to preserve the additional field values
            # Pass the values back to the template
            messages.error(request, 'Please correct the errors below to create your account.')
    else:
        form = UserRegisterForm()

    # Get additional field values to preserve them on validation errors
    full_name = request.POST.get('full_name', '') if request.method == 'POST' else ''
    phone = request.POST.get('phone', '') if request.method == 'POST' else ''

    return render(request, 'registration/register.html', {
        'form': form,
        'full_name': full_name,
        'phone': phone
    })


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
            return redirect('report_found_success')  # Redirect to found pet success page
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


# Report lost pet view
# Allows authenticated users to report lost pets

@login_required
def report_lost_pet(request):
    """
    Handle reporting of lost pets.
    Displays form for reporting lost pets and processes submissions.
    """
    if request.method == 'POST':
        form = LostPetForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a pet object with the form data
            from django.apps import apps
            PetModel = apps.get_model('main', 'Pet')
            pet = PetModel(
                owner=request.user,
                pet_type=form.cleaned_data['pet_type'],
                breed=form.cleaned_data['breed'],
                color=form.cleaned_data['color'],
                location=form.cleaned_data['last_seen_location'],
                description=f"Lost pet named {form.cleaned_data['pet_name']}",
                image=form.cleaned_data['pet_photo'],
                status='lost'  # Set status to lost
            )
            pet.save()
            
            # Create a request record linking the pet to the user
            RequestModel = apps.get_model('main', 'Request')
            RequestModel.objects.create(
                user=request.user,
                pet=pet,
                request_type='lost',  # Lost pet report
                phone_number=form.cleaned_data['owner_contact'],
                message=f"Lost pet report for {form.cleaned_data['pet_name']} ({form.cleaned_data['pet_type']}) near {form.cleaned_data['last_seen_location']}"
            )
            
            messages.success(request, 'Thank you for reporting your lost pet! Our team will review your submission and help in the search.')
            return redirect('report_lost_success')  # Redirect to lost pet success page
        else:
            # Add form errors to messages for better user feedback
            messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = LostPetForm()
    
    context = {
        'form': form,
        'now': timezone.now()
    }
    return render(request, 'report_lost_pet.html', context)


# Success page view
# Shows confirmation after successful pet report submission

def report_success(request):
    """
    Display success page after pet report submission.
    """
    # Get the report type from session
    report_type = request.session.get('report_type', 'found')
    context = {
        'report_type': report_type
    }
    return render(request, 'success.html', context)


# Success page view for lost pet reports
def report_lost_success(request):
    """
    Display success page after lost pet report submission.
    """
    return render(request, 'success_lost.html')


# Success page view for found pet reports
def report_found_success(request):
    """Display success page after found pet report submission."""
    return render(request, 'success_found.html')


# Admin Dashboard Views
# Restricted to admin users only

def admin_check(user):
    """Check if user is a superuser (admin)."""
    return user.is_superuser


@user_passes_test(admin_check, login_url='login')
def admin_dashboard(request):
    """
    Main admin dashboard view.
    Redirects non-admin users or shows access denied message.
    """
    # Get counts for each status
    from django.apps import apps
    RequestModel = apps.get_model('main', 'Request')
    
    pending_count = RequestModel.objects.filter(status='pending').count()
    accepted_count = RequestModel.objects.filter(status='accepted').count()
    rejected_count = RequestModel.objects.filter(status='rejected').count()
    
    # Get recent pending requests (limit to 5 for dashboard preview)
    recent_pending = RequestModel.objects.select_related('user', 'pet').filter(status='pending')[:5]
    
    context = {
        'pending_count': pending_count,
        'accepted_count': accepted_count,
        'rejected_count': rejected_count,
        'recent_pending': recent_pending,
    }
    
    return render(request, 'admin/dashboard.html', context)


@user_passes_test(admin_check, login_url='login')
def admin_pending_requests(request):
    """Display pending requests with filtering, sorting, and pagination."""
    # Get all pending requests
    from django.apps import apps
    RequestModel = apps.get_model('main', 'Request')
    requests = RequestModel.objects.select_related('user', 'pet').filter(status='pending')
    
    # Apply filters
    pet_type = request.GET.get('pet_type')
    if pet_type:
        requests = requests.filter(pet__pet_type=pet_type)
    
    request_type = request.GET.get('request_type')
    if request_type:
        requests = requests.filter(request_type=request_type)
    
    # Apply sorting
    sort_by = request.GET.get('sort_by', 'created_at')
    order = request.GET.get('order', 'desc')
    
    if order == 'asc':
        if sort_by == 'name':
            requests = requests.order_by('user__username')
        elif sort_by == 'date':
            requests = requests.order_by('created_at')
        elif sort_by == 'pet_type':
            requests = requests.order_by('pet__pet_type')
    else:  # desc
        if sort_by == 'name':
            requests = requests.order_by('-user__username')
        elif sort_by == 'date':
            requests = requests.order_by('-created_at')
        elif sort_by == 'pet_type':
            requests = requests.order_by('-pet__pet_type')
    
    # Apply pagination
    paginator = Paginator(requests, 10)  # Show 10 requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get Pet and Request models for choices
    PetModel = apps.get_model('main', 'Pet')
    
    context = {
        'requests': page_obj,
        'pet_types': PetModel.PET_TYPES,
        'request_types': RequestModel.REQUEST_TYPES,
        'current_filters': {
            'pet_type': pet_type,
            'request_type': request_type,
            'sort_by': sort_by,
            'order': order,
        }
    }
    
    return render(request, 'admin/pending_requests.html', context)


@user_passes_test(admin_check, login_url='login')
def admin_accepted_requests(request):
    """Display accepted requests with filtering, sorting, and pagination."""
    # Get all accepted requests
    from django.apps import apps
    RequestModel = apps.get_model('main', 'Request')
    requests = RequestModel.objects.select_related('user', 'pet').filter(status='accepted')
    
    # Apply filters
    pet_type = request.GET.get('pet_type')
    if pet_type:
        requests = requests.filter(pet__pet_type=pet_type)
    
    request_type = request.GET.get('request_type')
    if request_type:
        requests = requests.filter(request_type=request_type)
    
    # Apply sorting
    sort_by = request.GET.get('sort_by', 'created_at')
    order = request.GET.get('order', 'desc')
    
    if order == 'asc':
        if sort_by == 'name':
            requests = requests.order_by('user__username')
        elif sort_by == 'date':
            requests = requests.order_by('created_at')
        elif sort_by == 'pet_type':
            requests = requests.order_by('pet__pet_type')
    else:  # desc
        if sort_by == 'name':
            requests = requests.order_by('-user__username')
        elif sort_by == 'date':
            requests = requests.order_by('-created_at')
        elif sort_by == 'pet_type':
            requests = requests.order_by('-pet__pet_type')
    
    # Apply pagination
    paginator = Paginator(requests, 10)  # Show 10 requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get Pet and Request models for choices
    PetModel = apps.get_model('main', 'Pet')
    
    context = {
        'requests': page_obj,
        'pet_types': PetModel.PET_TYPES,
        'request_types': RequestModel.REQUEST_TYPES,
        'current_filters': {
            'pet_type': pet_type,
            'request_type': request_type,
            'sort_by': sort_by,
            'order': order,
        }
    }
    
    return render(request, 'admin/accepted_requests.html', context)


@user_passes_test(admin_check, login_url='login')
def admin_rejected_requests(request):
    """Display rejected requests with filtering, sorting, and pagination."""
    # Get all rejected requests
    from django.apps import apps
    RequestModel = apps.get_model('main', 'Request')
    requests = RequestModel.objects.select_related('user', 'pet').filter(status='rejected')
    
    # Apply filters
    pet_type = request.GET.get('pet_type')
    if pet_type:
        requests = requests.filter(pet__pet_type=pet_type)
    
    request_type = request.GET.get('request_type')
    if request_type:
        requests = requests.filter(request_type=request_type)
    
    # Apply sorting
    sort_by = request.GET.get('sort_by', 'created_at')
    order = request.GET.get('order', 'desc')
    
    if order == 'asc':
        if sort_by == 'name':
            requests = requests.order_by('user__username')
        elif sort_by == 'date':
            requests = requests.order_by('created_at')
        elif sort_by == 'pet_type':
            requests = requests.order_by('pet__pet_type')
    else:  # desc
        if sort_by == 'name':
            requests = requests.order_by('-user__username')
        elif sort_by == 'date':
            requests = requests.order_by('-created_at')
        elif sort_by == 'pet_type':
            requests = requests.order_by('-pet__pet_type')
    
    # Apply pagination
    paginator = Paginator(requests, 10)  # Show 10 requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get Pet and Request models for choices
    PetModel = apps.get_model('main', 'Pet')
    
    context = {
        'requests': page_obj,
        'pet_types': PetModel.PET_TYPES,
        'request_types': RequestModel.REQUEST_TYPES,
        'current_filters': {
            'pet_type': pet_type,
            'request_type': request_type,
            'sort_by': sort_by,
            'order': order,
        }
    }
    
    return render(request, 'admin/rejected_requests.html', context)


@user_passes_test(admin_check, login_url='login')
def update_request_status(request, request_id):
    """Update request status (Pending → Accepted/Rejected)."""
    if request.method == 'POST':
        new_status = request.POST.get('status')
        # Update the request status
        from django.apps import apps
        RequestModel = apps.get_model('main', 'Request')
        try:
            req = RequestModel.objects.get(id=request_id)
            # Convert status to lowercase to match model choices
            req.status = new_status.lower()
            req.save()
            messages.success(request, f'Request status updated successfully to {new_status}.')
        except RequestModel.DoesNotExist:
            messages.error(request, 'Request not found.')
        return redirect('admin_pending_requests')
    
    return HttpResponseForbidden(b"Method not allowed")
