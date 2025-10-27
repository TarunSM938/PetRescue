from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

# -----------------------------
# User Registration Form
# -----------------------------
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'phone', 'address', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
            # Only create profile if it doesn't already exist
            Profile.objects.get_or_create(
                user=user,
                defaults={
                    'phone': self.cleaned_data['phone'],
                    'address': self.cleaned_data['address']
                }
            )
        return user

# -----------------------------
# Profile Edit Form
# -----------------------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address']
