from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User  # Make sure this points to your custom User
        fields = ['username', 'email', 'password1', 'password2']



# Profile update form
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User  # custom User
        fields = ['username', 'email']

# Profile form for additional details
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date']
