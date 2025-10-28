from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.utils import timezone
from .models import User, Profile, Pet
import os

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
                'placeholder': 'Tell us about your experience with pets...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City or area where you live'
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
                'placeholder': 'Enter the breed (if known)'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the primary color'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Where was the pet found?'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Additional details about the pet...'
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
        if not pet_type:
            raise ValidationError("Please select a valid pet type.")
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
