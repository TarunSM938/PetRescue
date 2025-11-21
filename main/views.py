from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, HttpResponseForbidden
from typing import cast
from django.core.paginator import Paginator
from django.db.models import Q
from django.apps import apps
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, FoundPetForm, LostPetForm, PetSearchForm, ContactForm, ReportIssueForm
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
                        q_object = Q(color__icontains=synonym)
                        color_filters.add(q_object, Q.OR)
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


# All Pets page view
# Shows all accepted pets (both lost and found) in a gallery format

def all_pets(request):
    """
    Display all accepted pets (both lost and found) in a gallery format.
    Only pets with accepted requests are shown.
    """
    # Get model classes using apps.get_model to avoid linter issues
    from django.apps import apps
    PetModel = apps.get_model('main', 'Pet')
    RequestModel = apps.get_model('main', 'Request')
    
    # Get all accepted lost pets
    accepted_lost_pets = PetModel.objects.filter(
        status='lost',
        request__status='accepted',
        request__request_type='lost'
    ).select_related('owner')
    
    # Get all accepted found pets
    accepted_found_pets = PetModel.objects.filter(
        status='found',
        request__status='accepted',
        request__request_type='found'
    ).select_related('owner')
    
    # Combine both querysets
    all_accepted_pets = accepted_lost_pets.union(accepted_found_pets).order_by('-created_at')
    
    # Apply pagination
    paginator = Paginator(all_accepted_pets, 12)  # Show 12 pets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'now': timezone.now(),
        'pets': page_obj,
        'paginator': paginator,
        'page_obj': page_obj
    }
    return render(request, 'all_pets.html', context)


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
            messages.success(request, f'Welcome to PetRescue, {username}! Your account is ready to use.')
            return redirect('login')
        else:
            # Form is not valid, but we want to preserve the additional field values
            # Pass the values back to the template
            messages.error(request, 'Please fix the errors shown below and try again.')
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
                messages.success(request, f'Welcome back, {user.username}! You\'re now signed in.')
                return redirect('home')
            else:
                messages.error(request, "The username or password you entered is incorrect. Please check and try again.")
        else:
            messages.error(request, "The username or password you entered is incorrect. Please check and try again.")
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
    messages.info(request, f'Goodbye, {username}! You\'ve been signed out successfully.')
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
    from django.utils import timezone
    ProfileModel = apps.get_model('main', 'Profile')
    profile_obj, created = ProfileModel.objects.get_or_create(user=request.user)
    
    # Calculate impact metrics
    PetModel = apps.get_model('main', 'Pet')
    RequestModel = apps.get_model('main', 'Request')
    
    # Pets Reported - total number of pets the user has reported (both lost and found)
    pets_reported_count = PetModel.objects.filter(owner=request.user).count()
    
    # Pets Helped - total number of pets the user helped (reports accepted and closed as reunited)
    pets_helped_count = RequestModel.objects.filter(
        pet__owner=request.user,
        status='accepted'
    ).count()
    
    # Days Active - number of days the user has been active on the platform
    # Calculate from the user's registration date
    user = request.user
    days_active = (timezone.now().date() - user.date_joined.date()).days

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_obj)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile information has been saved.')
            return redirect('profile')
        else:
            messages.error(request, 'Please fix the errors shown below and try again.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile_obj)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'pets_reported_count': pets_reported_count,
        'pets_helped_count': pets_helped_count,
        'days_active': days_active
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
            # Handle the date_found field
            date_found = form.cleaned_data.get('date_found')
            if date_found:
                # We can store this in the description or create a new field
                # For now, let's add it to the description
                if pet.description:
                    pet.description += f"\n\nFound on: {date_found}"
                else:
                    pet.description = f"Found on: {date_found}"
            pet.save()
            
            # Create a request record linking the pet to the user
            # Using apps.get_model to avoid potential naming conflicts
            from django.apps import apps
            RequestModel = apps.get_model('main', 'Request')
            ActivityLogModel = apps.get_model('main', 'ActivityLog')
            request_obj = RequestModel.objects.create(
                user=request.user,
                pet=pet,
                request_type='found',  # Found pet report
                phone_number=request.user.phone_number or '',  # Use user's phone number if available
                message=f"Found pet report for {pet.pet_type} near {pet.location}"
            )
            
            # Log the creation activity
            ActivityLogModel.objects.create(
                pet=pet,
                activity_type='created',
                actor=f"user-{request.user.username}",
                details=f"Found pet report created by user {request.user.username}"
            )
            
            # Create admin notification
            NotificationModel = apps.get_model('main', 'Notification')
            NotificationModel.objects.create(
                request=request_obj,
                message=f"New found pet report submitted by {request.user.username} for a {pet.pet_type} near {pet.location}",
                notification_type='found_report'
            )
            
            messages.success(request, 'Thank you for reporting this found pet! Our team will review your report shortly.')
            return redirect('report_found_success')  # Redirect to found pet success page
        else:
            # Add form errors to messages for better user feedback
            messages.error(request, 'Please fix the errors shown below and try again.')
    else:
        form = FoundPetForm()
    
    context = {
        'form': form,
        'now': timezone.now()
    }
    return render(request, 'report_found_pet.html', context)


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
            ActivityLogModel = apps.get_model('main', 'ActivityLog')
            pet = PetModel(
                owner=request.user,
                pet_type=form.cleaned_data['pet_type'],
                breed=form.cleaned_data['breed'],
                color=form.cleaned_data['color'],
                location=form.cleaned_data['last_seen_location'],
                description=f"Lost pet named {form.cleaned_data['pet_name']}",
                status='lost'  # Set status to lost
            )
            # Handle image separately
            pet_photo = form.cleaned_data.get('pet_photo')
            if pet_photo:
                pet.image = pet_photo
            pet.save()
            
            # Create a request record linking the pet to the user
            RequestModel = apps.get_model('main', 'Request')
            request_obj = RequestModel.objects.create(
                user=request.user,
                pet=pet,
                request_type='lost',  # Lost pet report
                phone_number=form.cleaned_data['owner_contact'],
                message=f"Lost pet report for {form.cleaned_data['pet_name']} ({form.cleaned_data['pet_type']}) near {form.cleaned_data['last_seen_location']}"
            )
            
            # Log the creation activity
            ActivityLogModel.objects.create(
                pet=pet,
                activity_type='created',
                actor=f"user-{request.user.username}",
                details=f"Lost pet report created by user {request.user.username}"
            )
            
            # Create admin notification
            NotificationModel = apps.get_model('main', 'Notification')
            NotificationModel.objects.create(
                request=request_obj,
                message=f"New lost pet report submitted by {request.user.username} for a {pet.pet_type} near {pet.location}",
                notification_type='lost_report'
            )
            
            messages.success(request, 'Thank you for reporting your lost pet! Our team will review your report and help with the search.')
            return redirect('report_lost_success')  # Redirect to lost pet success page
        else:
            # Add form errors to messages for better user feedback
            messages.error(request, 'Please fix the errors shown below and try again.')
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


# Pet detail view
def pet_detail(request, pet_id):
    """
    Display detailed information about a specific pet.
    """
    # Get model classes using apps.get_model to avoid linter issues
    from django.apps import apps
    PetModel = apps.get_model('main', 'Pet')
    RequestModel = apps.get_model('main', 'Request')
    PetImageModel = apps.get_model('main', 'PetImage')
    
    # Get the pet object
    pet = get_object_or_404(PetModel, id=pet_id)
    
    # Get associated request if it exists
    try:
        pet_request = RequestModel.objects.get(pet=pet)
    except RequestModel.DoesNotExist:
        pet_request = None
    
    # Get all images for this pet
    pet_images = PetImageModel.objects.filter(pet=pet)
    
    # Check if user has permission to view contact information
    show_contact_info = False
    contact_info = None
    
    if request.user.is_authenticated:
        # User is the reporter
        if pet.owner == request.user:
            show_contact_info = True
        # User is admin
        elif request.user.is_superuser:
            show_contact_info = True
        # User has permission (for future implementation)
        # This could be extended with specific permissions
    
    # Prepare contact information if user has permission
    if show_contact_info and pet_request:
        contact_info = {
            'reporter_name': pet.owner.get_full_name() or pet.owner.username,
            'reporter_email': pet.owner.email,
            'reporter_phone': pet_request.phone_number or pet.owner.phone_number
        }
    
    # Determine breadcrumb based on referrer
    referrer = request.GET.get('ref', 'all_pets')  # Default to 'all_pets'
    
    context = {
        'pet': pet,
        'pet_request': pet_request,
        'pet_images': pet_images,
        'show_contact_info': show_contact_info,
        'contact_info': contact_info,
        'now': timezone.now(),
        'referrer': referrer
    }
    return render(request, 'pet_detail.html', context)


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
def admin_notifications(request):
    """
    Display admin notifications page.
    """
    return render(request, 'admin/notifications.html')


@user_passes_test(admin_check, login_url='login')
def update_request_status(request, request_id):
    """Update request status (Pending → Accepted/Rejected)."""
    if request.method == 'POST':
        new_status = request.POST.get('status')
        # Update the request status
        from django.apps import apps
        RequestModel = apps.get_model('main', 'Request')
        ActivityLogModel = apps.get_model('main', 'ActivityLog')
        try:
            req = RequestModel.objects.get(id=request_id)
            # Store the old status for logging
            old_status = req.status
            # Convert status to lowercase to match model choices
            req.status = new_status.lower()
            req.save()
            
            # Log the status change activity
            ActivityLogModel.objects.create(
                pet=req.pet,
                activity_type='status_changed',
                actor=f"admin-{request.user.username}",
                details=f"Status changed from {old_status} to {new_status.lower()}"
            )
            
            messages.success(request, f'Request status has been updated to {new_status}.')
        except RequestModel.DoesNotExist:
            messages.error(request, 'The requested item could not be found.')
        return redirect('admin_pending_requests')
    
    return HttpResponseForbidden(b"Method not allowed")


@login_required
def user_requests(request):
    """
    Display all pet reports (lost and found) submitted by the logged-in user.
    Shows pet details, request status, and allows editing/deleting pending reports.
    """
    # Get model classes using apps.get_model to avoid linter issues
    from django.apps import apps
    PetModel = apps.get_model('main', 'Pet')
    RequestModel = apps.get_model('main', 'Request')
    
    # Get all pets reported by the current user
    user_pets = PetModel.objects.filter(owner=request.user).order_by('-created_at')
    
    # Get requests associated with these pets
    pet_requests = RequestModel.objects.filter(pet__in=user_pets)
    
    # Create a dictionary to map pet IDs to their requests
    pet_request_map = {req.pet.id: req for req in pet_requests}
    
    # Add status messages based on request status
    for pet in user_pets:
        if pet.id in pet_request_map:
            request_obj = pet_request_map[pet.id]
            pet.request_status = request_obj.status
            if request_obj.status == 'pending':
                pet.status_message = "Your report is currently being reviewed."
            elif request_obj.status == 'accepted':
                pet.status_message = "Your report is now visible to other users in search results."
            elif request_obj.status == 'rejected':
                pet.status_message = "This report has been reviewed and was not approved."
            else:
                pet.status_message = "Status unknown."
        else:
            pet.request_status = 'unknown'
            pet.status_message = "No request associated with this pet."
    
    context = {
        'user_pets': user_pets,
        'now': timezone.now()
    }
    return render(request, 'user_requests.html', context)


@login_required
def edit_user_request(request, pet_id):
    """
    Allow users to edit their pet reports if the status is pending.
    """
    # Get model classes using apps.get_model to avoid linter issues
    from django.apps import apps
    PetModel = apps.get_model('main', 'Pet')
    RequestModel = apps.get_model('main', 'Request')
    ActivityLogModel = apps.get_model('main', 'ActivityLog')
    
    # Get the pet object
    pet = get_object_or_404(PetModel, id=pet_id, owner=request.user)
    
    # Check if there's a request associated with this pet
    try:
        pet_request = RequestModel.objects.get(pet=pet)
        # Only allow editing if status is pending
        if pet_request.status != 'pending':
            messages.error(request, "Only reports that are pending review can be edited.")
            return redirect('user_requests')
    except RequestModel.DoesNotExist:
        messages.error(request, "No request record was found for this pet.")
        return redirect('user_requests')
    
    # For editing, we'll use a simple form approach since the existing forms
    # are designed for creation, not editing
    if request.method == 'POST':
        # Track changes for activity log
        changes = []
        
        # Update pet details
        fields_to_update = ['pet_type', 'breed', 'color', 'location', 'description']
        for field in fields_to_update:
            if field in request.POST:
                old_value = getattr(pet, field)
                new_value = request.POST[field]
                if old_value != new_value:
                    setattr(pet, field, new_value)
                    changes.append(f"{field}: {old_value} → {new_value}")
        
        # Handle image upload if provided
        if 'image' in request.FILES:
            pet.image = request.FILES['image']
            changes.append("image: updated")
        
        pet.save()
        
        # Log the edit activity
        if changes:
            ActivityLogModel.objects.create(
                pet=pet,
                activity_type='edited',
                actor=f"user-{request.user.username}",
                details=f"Edited fields: {', '.join(changes)}"
            )
        
        messages.success(request, "Your report has been saved with the updated information.")
        return redirect('user_requests')
    
    context = {
        'pet': pet,
        'now': timezone.now()
    }
    return render(request, 'edit_request.html', context)


@login_required
def delete_user_request(request, pet_id):
    """
    Allow users to delete their pet reports if the status is pending.
    """
    if request.method == 'POST':
        # Get model classes using apps.get_model to avoid linter issues
        from django.apps import apps
        PetModel = apps.get_model('main', 'Pet')
        RequestModel = apps.get_model('main', 'Request')
        ActivityLogModel = apps.get_model('main', 'ActivityLog')
        
        # Get the pet object
        pet = get_object_or_404(PetModel, id=pet_id, owner=request.user)
        
        # Check if there's a request associated with this pet
        try:
            pet_request = RequestModel.objects.get(pet=pet)
            # Only allow deleting if status is pending
            if pet_request.status != 'pending':
                messages.error(request, "Only reports that are pending review can be deleted.")
                return redirect('user_requests')
        except RequestModel.DoesNotExist:
            # If no request exists, we can still delete the pet
            pass
        
        # Log the deletion activity
        ActivityLogModel.objects.create(
            pet=pet,
            activity_type='deleted',
            actor=f"user-{request.user.username}",
            details=f"Report deleted by user {request.user.username}"
        )
        
        # Delete the pet and associated request
        pet_name = pet.breed
        pet.delete()
        messages.success(request, f"The report for {pet_name} has been removed.")
        return redirect('user_requests')
    
    return HttpResponseForbidden(b"Method not allowed")


# API Views for Dashboard

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_user_requests(request):
    """
    API endpoint to return all reports of the logged-in user (found + lost).
    """
    # Get model classes using apps.get_model to avoid linter issues
    from django.apps import apps
    PetModel = apps.get_model('main', 'Pet')
    RequestModel = apps.get_model('main', 'Request')
    ActivityLogModel = apps.get_model('main', 'ActivityLog')
    
    # Get all pets reported by the current user
    user_pets = PetModel.objects.filter(owner=request.user).order_by('-created_at')
    
    # Prepare response data
    reports_data = []
    for pet in user_pets:
        # Get associated request
        try:
            pet_request = RequestModel.objects.get(pet=pet)
            request_status = pet_request.status
            request_type = pet_request.request_type
        except RequestModel.DoesNotExist:
            request_status = 'unknown'
            request_type = 'unknown'
        
        # Get activity log entries for this pet (latest 5)
        activity_logs = ActivityLogModel.objects.filter(pet=pet)[:5]
        timeline = []
        for log in activity_logs:
            timeline.append({
                'activity_type': log.activity_type,
                'timestamp': log.timestamp.isoformat(),
                'actor': log.actor,
                'details': log.details
            })
        
        # Determine status message
        if request_status == 'pending':
            status_message = "Your report is currently being reviewed."
        elif request_status == 'accepted':
            status_message = "Your report is now visible to other users in search results."
        elif request_status == 'rejected':
            status_message = "This report has been reviewed and was not approved."
        else:
            status_message = "Status unknown."
        
        reports_data.append({
            'id': pet.id,
            'pet_type': pet.pet_type,
            'breed': pet.breed,
            'color': pet.color,
            'location': pet.location,
            'description': pet.description,
            'image': pet.image.url if pet.image else None,
            'status': pet.status,
            'request_status': request_status,
            'request_type': request_type,
            'status_message': status_message,
            'created_at': pet.created_at.isoformat(),
            'updated_at': pet.created_at.isoformat(),  # For now, using created_at
            'timeline': timeline
        })
    
    return Response({'reports': reports_data})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def api_edit_request(request, pet_id):
    """
    API endpoint to edit a report (only if Pending and owned by user).
    """
    # Get model classes using apps.get_model to avoid linter issues
    from django.apps import apps
    PetModel = apps.get_model('main', 'Pet')
    RequestModel = apps.get_model('main', 'Request')
    ActivityLogModel = apps.get_model('main', 'ActivityLog')
    
    # Get the pet object
    try:
        pet = PetModel.objects.get(id=pet_id, owner=request.user)
    except PetModel.DoesNotExist:
        return Response({'error': 'Report not found or you do not have permission to edit it.'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    # Check if there's a request associated with this pet
    try:
        pet_request = RequestModel.objects.get(pet=pet)
        # Only allow editing if status is pending
        if pet_request.status != 'pending':
            return Response({'error': 'Only pending reports can be edited or deleted.'}, 
                           status=status.HTTP_403_FORBIDDEN)
    except RequestModel.DoesNotExist:
        return Response({'error': 'No request found for this pet.'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    # Track changes for activity log
    changes = []
    
    # Update pet details
    fields_to_update = ['pet_type', 'breed', 'color', 'location', 'description']
    for field in fields_to_update:
        if field in request.data:
            old_value = getattr(pet, field)
            new_value = request.data[field]
            if old_value != new_value:
                setattr(pet, field, new_value)
                changes.append(f"{field}: {old_value} → {new_value}")
    
    # Handle image upload if provided
    if 'image' in request.FILES:
        pet.image = request.FILES['image']
        changes.append("image: updated")
    
    pet.save()
    
    # Log the edit activity
    if changes:
        ActivityLogModel.objects.create(
            pet=pet,
            activity_type='edited',
            actor=f"user-{request.user.username}",
            details=f"Edited fields: {', '.join(changes)}"
        )
    
    return Response({'message': 'Report updated successfully.'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_delete_request(request, pet_id):
    """
    API endpoint to delete a report (only if Pending and owned by user).
    """
    # Get model classes using apps.get_model to avoid linter issues
    from django.apps import apps
    PetModel = apps.get_model('main', 'Pet')
    RequestModel = apps.get_model('main', 'Request')
    ActivityLogModel = apps.get_model('main', 'ActivityLog')
    
    # Get the pet object
    try:
        pet = PetModel.objects.get(id=pet_id, owner=request.user)
    except PetModel.DoesNotExist:
        return Response({'error': 'Report not found or you do not have permission to delete it.'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    # Check if there's a request associated with this pet
    try:
        pet_request = RequestModel.objects.get(pet=pet)
        # Only allow deleting if status is pending
        if pet_request.status != 'pending':
            return Response({'error': 'Only pending reports can be edited or deleted.'}, 
                           status=status.HTTP_403_FORBIDDEN)
    except RequestModel.DoesNotExist:
        # If no request exists, we can still delete the pet
        pass
    
    # Log the deletion activity
    ActivityLogModel.objects.create(
        pet=pet,
        activity_type='deleted',
        actor=f"user-{request.user.username}",
        details=f"Report deleted by user {request.user.username}"
    )
    
    # Delete the pet
    pet_name = pet.breed
    pet.delete()
    
    return Response({'message': f'Report for {pet_name} has been deleted successfully.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_request_history(request, pet_id):
    """
    API endpoint to return timeline/activity for a report.
    """
    # Get model classes using apps.get_model to avoid linter issues
    from django.apps import apps
    PetModel = apps.get_model('main', 'Pet')
    ActivityLogModel = apps.get_model('main', 'ActivityLog')
    
    # Get the pet object
    try:
        pet = PetModel.objects.get(id=pet_id, owner=request.user)
    except PetModel.DoesNotExist:
        return Response({'error': 'Report not found or you do not have permission to view it.'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    # Get activity log entries for this pet (all, ordered by timestamp)
    activity_logs = ActivityLogModel.objects.filter(pet=pet).order_by('timestamp')
    
    timeline = []
    for log in activity_logs:
        timeline.append({
            'id': log.id,
            'activity_type': log.activity_type,
            'timestamp': log.timestamp.isoformat(),
            'actor': log.actor,
            'details': log.details
        })
    
    return Response({'timeline': timeline})


# Admin Notification API Views
# API endpoints for managing admin notifications

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_admin_notifications(request):
    """
    API endpoint to return all admin notifications (unread + read).
    Only accessible by admin users.
    """
    # Check if user is admin
    if not request.user.is_superuser:
        return Response({'error': 'Access denied. Admin privileges required.'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    # Get model classes using apps.get_model to avoid linter issues
    from django.apps import apps
    NotificationModel = apps.get_model('main', 'Notification')
    
    # Get all notifications ordered by creation time
    notifications = NotificationModel.objects.select_related('request__pet', 'request__user', 'contact_submission__related_pet', 'contact_submission__user').all()
    
    # Prepare response data
    notifications_data = []
    for notification in notifications:
        notification_data = {
            'id': notification.id,
            'message': notification.message,
            'timestamp': notification.created_at.isoformat(),
            'is_read': notification.is_read,
            'notification_type': notification.notification_type,
        }
        
        # Add request data if it's a request-based notification
        if notification.request:
            notification_data['request'] = {
                'id': notification.request.id,
                'request_type': notification.request.request_type,
                'status': notification.request.status,
                'pet': {
                    'id': notification.request.pet.id,
                    'breed': notification.request.pet.breed,
                    'pet_type': notification.request.pet.pet_type,
                    'location': notification.request.pet.location,
                },
                'user': {
                    'username': notification.request.user.username,
                }
            }
            notification_data['link'] = '/dashboard/admin/pending-requests/'
        
        # Add contact submission data if it's a contact-based notification
        if notification.contact_submission:
            contact_sub = notification.contact_submission
            notification_data['contact_submission'] = {
                'id': contact_sub.id,
                'name': contact_sub.name,
                'email': contact_sub.email,
                'subject': contact_sub.subject,
                'submission_type': contact_sub.submission_type,
                'status': contact_sub.status,
            }
            if contact_sub.related_pet:
                notification_data['contact_submission']['pet'] = {
                    'id': contact_sub.related_pet.id,
                    'breed': contact_sub.related_pet.breed,
                    'pet_type': contact_sub.related_pet.pet_type,
                }
            notification_data['link'] = f'/dashboard/admin/contact-submissions/{contact_sub.id}/'
        
        notifications_data.append(notification_data)
    
    return Response({'notifications': notifications_data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_admin_unread_count(request):
    """
    API endpoint to return the count of unread admin notifications.
    Only accessible by admin users.
    """
    # Check if user is admin
    if not request.user.is_superuser:
        return Response({'error': 'Access denied. Admin privileges required.'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    # Get model classes using apps.get_model to avoid linter issues
    from django.apps import apps
    NotificationModel = apps.get_model('main', 'Notification')
    
    # Count unread notifications
    unread_count = NotificationModel.objects.filter(is_read=False).count()
    
    return Response({'unread_count': unread_count})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_admin_mark_read(request, notification_id):
    """
    API endpoint to mark a notification as read.
    Only accessible by admin users.
    """
    # Check if user is admin
    if not request.user.is_superuser:
        return Response({'error': 'Access denied. Admin privileges required.'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    # Get model classes using apps.get_model to avoid linter issues
    from django.apps import apps
    NotificationModel = apps.get_model('main', 'Notification')
    
    # Get the notification
    try:
        notification = NotificationModel.objects.get(id=notification_id)
    except NotificationModel.DoesNotExist:
        return Response({'error': 'Notification not found.'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    # Mark as read
    notification.is_read = True
    notification.save()
    
    return Response({'message': 'Notification marked as read.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_admin_mark_all_read(request):
    """
    API endpoint to mark all notifications as read.
    Only accessible by admin users.
    """
    # Check if user is admin
    if not request.user.is_superuser:
        return Response({'error': 'Access denied. Admin privileges required.'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    # Get model classes using apps.get_model to avoid linter issues
    from django.apps import apps
    NotificationModel = apps.get_model('main', 'Notification')
    
    # Mark all notifications as read
    NotificationModel.objects.filter(is_read=False).update(is_read=True)
    
    return Response({'message': 'All notifications marked as read.'})


# Contact & Communication Module Views

# Contact page view
# Allows users to send messages to admin

def contact(request):
    """
    Handle contact form submissions.
    Auto-fills name and email for logged-in users.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get model classes using apps.get_model
            from django.apps import apps
            ContactSubmissionModel = apps.get_model('main', 'ContactSubmission')
            
            # Create contact submission
            submission = ContactSubmissionModel.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
                submission_type='general',
                user=request.user if request.user.is_authenticated else None,
                status='pending'
            )
            
            # Create admin notification
            NotificationModel = apps.get_model('main', 'Notification')
            submitter_name = request.user.username if request.user.is_authenticated else submission.name
            NotificationModel.objects.create(
                contact_submission=submission,
                message=f"New contact submission from {submitter_name}: {submission.subject}",
                notification_type='contact_submission'
            )
            
            # Send email notification if email is configured
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                
                # Only send if email backend is configured
                if hasattr(settings, 'EMAIL_BACKEND') and settings.EMAIL_BACKEND != 'django.core.mail.backends.console.EmailBackend':
                    admin_email = getattr(settings, 'ADMIN_EMAIL', None)
                    if admin_email:
                        send_mail(
                            subject=f'New Contact Submission: {submission.subject}',
                            message=f'Name: {submission.name}\nEmail: {submission.email}\n\nMessage:\n{submission.message}',
                            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else None,
                            recipient_list=[admin_email],
                            fail_silently=True,
                        )
            except Exception:
                # Email sending is optional, fail silently
                pass
            
            messages.success(request, 'Thank you for contacting us! We\'ll get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please fix the errors shown below and try again.')
    else:
        # Pre-fill form for logged-in users
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                'email': request.user.email
            }
        form = ContactForm(initial=initial_data)
    
    context = {
        'form': form,
        'now': timezone.now()
    }
    return render(request, 'contact.html', context)


# Report issue view
# Allows users to report issues related to specific pets

def report_issue(request, pet_id):
    """
    Handle issue reports related to specific pets.
    """
    # Get model classes using apps.get_model
    from django.apps import apps
    PetModel = apps.get_model('main', 'Pet')
    
    # Get the pet object
    pet = get_object_or_404(PetModel, id=pet_id)
    
    if request.method == 'POST':
        form = ReportIssueForm(request.POST)
        if form.is_valid():
            ContactSubmissionModel = apps.get_model('main', 'ContactSubmission')
            
            # Create contact submission linked to pet
            submission = ContactSubmissionModel.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
                submission_type='issue_report',
                related_pet=pet,
                user=request.user if request.user.is_authenticated else None,
                status='pending'
            )
            
            # Create admin notification
            NotificationModel = apps.get_model('main', 'Notification')
            submitter_name = request.user.username if request.user.is_authenticated else submission.name
            NotificationModel.objects.create(
                contact_submission=submission,
                message=f"Issue report from {submitter_name} for pet {pet.breed} ({pet.pet_type})",
                notification_type='issue_report'
            )
            
            # Send email notification if email is configured
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                
                if hasattr(settings, 'EMAIL_BACKEND') and settings.EMAIL_BACKEND != 'django.core.mail.backends.console.EmailBackend':
                    admin_email = getattr(settings, 'ADMIN_EMAIL', None)
                    if admin_email:
                        send_mail(
                            subject=f'Issue Report for Pet: {pet.breed}',
                            message=f'Name: {submission.name}\nEmail: {submission.email}\nPet: {pet.breed} ({pet.pet_type})\n\nIssue:\n{submission.message}',
                            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else None,
                            recipient_list=[admin_email],
                            fail_silently=True,
                        )
            except Exception:
                pass
            
            messages.success(request, 'Thank you for reporting this issue. We\'ll review it and take appropriate action.')
            return redirect('find_pets')
        else:
            messages.error(request, 'Please fix the errors shown below and try again.')
    else:
        # Pre-fill form for logged-in users
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                'email': request.user.email
            }
        form = ReportIssueForm(initial=initial_data)
    
    context = {
        'form': form,
        'pet': pet,
        'now': timezone.now()
    }
    return render(request, 'report_issue.html', context)


# Admin contact submissions view
# Allows admin to view and manage all contact submissions

@user_passes_test(admin_check, login_url='login')
def admin_contact_submissions(request):
    """
    Display all contact submissions with filtering, searching, and status management.
    Admin-only view.
    """
    from django.apps import apps
    ContactSubmissionModel = apps.get_model('main', 'ContactSubmission')
    
    # Get all submissions
    submissions = ContactSubmissionModel.objects.select_related('user', 'related_pet').all()
    
    # Apply filters
    status_filter = request.GET.get('status')
    if status_filter:
        submissions = submissions.filter(status=status_filter)
    
    submission_type_filter = request.GET.get('submission_type')
    if submission_type_filter:
        submissions = submissions.filter(submission_type=submission_type_filter)
    
    # Apply search
    search_query = request.GET.get('search')
    if search_query:
        submissions = submissions.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(message__icontains=search_query)
        )
    
    # Apply sorting
    sort_by = request.GET.get('sort_by', 'created_at')
    order = request.GET.get('order', 'desc')
    
    if order == 'asc':
        submissions = submissions.order_by(sort_by)
    else:
        submissions = submissions.order_by(f'-{sort_by}')
    
    # Apply pagination
    paginator = Paginator(submissions, 15)  # Show 15 submissions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'submissions': page_obj,
        'status_choices': ContactSubmissionModel.STATUS_CHOICES,
        'submission_type_choices': ContactSubmissionModel.SUBMISSION_TYPES,
        'current_filters': {
            'status': status_filter,
            'submission_type': submission_type_filter,
            'search': search_query,
            'sort_by': sort_by,
            'order': order,
        }
    }
    
    return render(request, 'admin/contact_submissions.html', context)


# Admin view contact submission details
# Allows admin to view full details of a submission

@user_passes_test(admin_check, login_url='login')
def admin_contact_submission_detail(request, submission_id):
    """
    Display detailed view of a contact submission.
    Admin-only view.
    """
    from django.apps import apps
    ContactSubmissionModel = apps.get_model('main', 'ContactSubmission')
    
    submission = get_object_or_404(ContactSubmissionModel, id=submission_id)
    
    context = {
        'submission': submission,
        'status_choices': ContactSubmissionModel.STATUS_CHOICES,
        'submission_type_choices': ContactSubmissionModel.SUBMISSION_TYPES
    }
    
    return render(request, 'admin/contact_submission_detail.html', context)


# Admin update submission status
# Allows admin to change the status of a submission

@user_passes_test(admin_check, login_url='login')
def admin_update_submission_status(request, submission_id):
    """
    Update the status of a contact submission.
    Admin-only action.
    """
    if request.method == 'POST':
        new_status = request.POST.get('status')
        from django.apps import apps
        ContactSubmissionModel = apps.get_model('main', 'ContactSubmission')
        
        try:
            submission = ContactSubmissionModel.objects.get(id=submission_id)
            submission.status = new_status
            submission.save()
            messages.success(request, f'Submission status updated to {new_status}.')
        except ContactSubmissionModel.DoesNotExist:
            messages.error(request, 'Submission not found.')
        
        return redirect('admin_contact_submissions')
    
    return HttpResponseForbidden(b"Method not allowed")
