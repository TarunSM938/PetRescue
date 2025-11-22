from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import User, Profile, Pet
import os
import re

class UserRegisterForm(UserCreationForm):
    """
    Custom user registration form that extends Django's built-in UserCreationForm.
    Includes email field and custom validation.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User  # Make sure this points to your custom User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # Add CSS classes to form fields for better styling
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


# Profile update form for user information
class UserUpdateForm(forms.ModelForm):
    """
    Form for updating basic user information.
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = User  # custom User
        fields = ['username', 'email']
        
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        # Add CSS classes to form fields
        self.fields['username'].widget.attrs.update({
            'class': 'form-control'
        })


# Profile form for additional personal details
class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating additional profile information.
    """
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )

    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience with pets...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your city or area'
            }),
        }


# Form for reporting found pets
class FoundPetForm(forms.ModelForm):
    """
    Form for reporting found pets.
    Includes fields for pet type, breed, color, location, description, and image.
    """
    # Add date found field
    date_found = forms.DateField(
        label="Date Found",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required=True,
        initial=timezone.now().date()
    )
    
    class Meta:
        model = Pet
        fields = ['pet_type', 'breed', 'color', 'location', 'description', 'image']
        widgets = {
            'pet_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'breed': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Breed (if known)'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Primary color'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Location where pet was found'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Any additional details about the pet...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super(FoundPetForm, self).__init__(*args, **kwargs)
        # Make all fields required except image and description
        for field_name in self.fields:
            if field_name not in ['image', 'description']:
                self.fields[field_name].required = True
    
    def clean_pet_type(self):
        """Validate that pet type is selected"""
        pet_type = self.cleaned_data.get('pet_type')
        # Allow blank selection
        return pet_type
    
    def clean_location(self):
        """Validate that location has at least 5 characters"""
        location = self.cleaned_data.get('location')
        if location and len(location) < 5:
            raise ValidationError("Location must contain at least 5 characters.")
        return location
    
    def clean_date_found(self):
        """Validate that date found is not in the future"""
        date_found = self.cleaned_data.get('date_found')
        if date_found and date_found > timezone.now().date():
            raise ValidationError("Date found cannot be in the future.")
        return date_found
    
    def clean_image(self):
        """Validate image file format and size"""
        image = self.cleaned_data.get('image')
        
        if image:
            # Check file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            ext = os.path.splitext(image.name)[1].lower()
            
            if ext not in allowed_extensions:
                raise ValidationError("Only JPG and PNG files are allowed.")
            
            # Check file size (5 MB limit)
            if image.size > 5 * 1024 * 1024:  # 5 MB in bytes
                raise ValidationError("Image file size must be less than 5 MB.")
        
        return image


# Form for reporting lost pets
class LostPetForm(forms.Form):
    """
    Form for reporting lost pets.
    Includes fields for pet name, pet type, breed, color, last seen location, 
    date lost, owner contact, alternate email, and pet photo.
    """
    pet_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your pet\'s name'
        }),
        help_text="Your pet's name"
    )
    
    pet_type = forms.ChoiceField(
        choices=[('', 'Select Pet Type')] + Pet.PET_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        help_text="Type of pet",
        required=True
    )
    
    breed = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the breed (if known)'
        }),
        help_text="Breed of the pet (if known)"
    )
    
    color = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the primary color'
        }),
        help_text="Primary color of the pet"
    )
    
    last_seen_location = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Location where pet was last seen'
        }),
        help_text="Location where pet was last seen"
    )
    
    date_lost = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        help_text="When was the pet lost?"
    )
    
    owner_contact = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your phone number'
        }),
        help_text="Your phone number for contact"
    )
    
    alternate_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Alternate email (optional)'
        }),
        help_text="Alternate email for contact (optional)"
    )
    
    pet_photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        }),
        help_text="Photo of the pet (optional but helpful)"
    )
    
    def clean_pet_name(self):
        """Validate that pet name is provided"""
        pet_name = self.cleaned_data.get('pet_name')
        if not pet_name:
            raise ValidationError("Pet name is required.")
        return pet_name
    
    def clean_pet_type(self):
        """Validate that pet type is selected"""
        pet_type = self.cleaned_data.get('pet_type')
        if not pet_type:
            raise ValidationError("Please select a valid pet type.")
        return pet_type
    
    def clean_last_seen_location(self):
        """Validate that location has at least 5 characters"""
        location = self.cleaned_data.get('last_seen_location')
        if location and len(location) < 5:
            raise ValidationError("Location must contain at least 5 characters.")
        return location
    
    def clean_date_lost(self):
        """Validate that date lost is not in the future"""
        date_lost = self.cleaned_data.get('date_lost')
        if date_lost and date_lost > timezone.now().date():
            raise ValidationError("Date lost cannot be in the future.")
        return date_lost
    
    def clean_owner_contact(self):
        """Validate phone number format"""
        phone = self.cleaned_data.get('owner_contact')
        if phone:
            # Allow common phone formats
            phone_regex = r'^[0-9+\-\s()]{10,15}$'
            if not re.match(phone_regex, phone):
                raise ValidationError("Please enter a valid phone number.")
        return phone
    
    def clean_pet_photo(self):
        """Validate image file format and size"""
        image = self.cleaned_data.get('pet_photo')
        
        if image:
            # Check file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            ext = os.path.splitext(image.name)[1].lower()
            
            if ext not in allowed_extensions:
                raise ValidationError("Only JPG and PNG files are allowed.")
            
            # Check file size (5 MB limit)
            if image.size > 5 * 1024 * 1024:  # 5 MB in bytes
                raise ValidationError("Image file size must be less than 5 MB.")
        
        return image


# Form for searching lost pets
class PetSearchForm(forms.Form):
    """
    Form for searching lost pets with multiple filter options.
    """
    pet_type = forms.ChoiceField(
        choices=[('', 'All Pet Types')] + Pet.PET_TYPES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    breed = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Breed'
        })
    )
    
    color = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Color'
        })
    )
    
    location = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Location'
        })
    )
    
    # New radius field for location-based search
    radius = forms.ChoiceField(
        choices=[
            ('', 'Any Distance'),
            ('5', '5 km'),
            ('10', '10 km'),
            ('25', '25 km'),
            ('50', '50 km')
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'From date'
        }),
        help_text="Start date for search"
    )
    
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'To date'
        }),
        help_text="End date for search"
    )
    
    # New status filter
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + Pet.PET_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    # New sort field
    sort = forms.ChoiceField(
        choices=[
            ('newest', 'Newest first'),
            ('oldest', 'Oldest first'),
            ('updated', 'Most recently updated')
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    def clean(self):
        """
        Validate that start_date is not after end_date
        """
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise ValidationError("Start date cannot be after end date.")
        
        return cleaned_data


# Contact Form
# Form for users to submit contact messages

class ContactForm(forms.Form):
    """
    Form for contact submissions.
    Supports both logged-in users (auto-filled) and guest users.
    """
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your name'
        }),
        help_text="Your full name"
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email address'
        }),
        help_text="Your email address"
    )
    
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'What is this about?'
        }),
        help_text="Brief subject line"
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Tell us how we can help...'
        }),
        help_text="Your message"
    )
    
    def clean_name(self):
        """Validate that name is provided and has reasonable length"""
        name = self.cleaned_data.get('name')
        if name and len(name.strip()) < 2:
            raise ValidationError("Please enter your full name.")
        return name.strip()
    
    def clean_message(self):
        """Validate that message is provided and has minimum length"""
        message = self.cleaned_data.get('message')
        if message and len(message.strip()) < 10:
            raise ValidationError("Please provide more details in your message (at least 10 characters).")
        return message.strip()
    
    def clean_subject(self):
        """Validate that subject is provided"""
        subject = self.cleaned_data.get('subject')
        if subject and len(subject.strip()) < 3:
            raise ValidationError("Please enter a subject for your message.")
        return subject.strip()


# Report Issue Form
# Form for reporting issues related to specific pets

class ReportIssueForm(forms.Form):
    """
    Form for reporting issues related to specific pets.
    Similar to contact form but linked to a pet.
    """
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your name'
        }),
        help_text="Your full name"
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email address'
        }),
        help_text="Your email address"
    )
    
    subject = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Issue subject (optional)'
        }),
        help_text="Brief description of the issue"
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Describe the issue you\'ve noticed...'
        }),
        help_text="Details about the issue"
    )
    
    def clean_name(self):
        """Validate that name is provided"""
        name = self.cleaned_data.get('name')
        if name and len(name.strip()) < 2:
            raise ValidationError("Please enter your full name.")
        return name.strip()
    
    def clean_message(self):
        """Validate that message is provided"""
        message = self.cleaned_data.get('message')
        if message and len(message.strip()) < 10:
            raise ValidationError("Please provide more details about the issue (at least 10 characters).")
        return message.strip()
    
    def clean_subject(self):
        """Set default subject if not provided"""
        subject = self.cleaned_data.get('subject')
        if not subject or len(subject.strip()) < 3:
            return "Issue Report"
        return subject.strip()
