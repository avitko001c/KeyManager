from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Profile, User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('ssh_key', 'role', 'location', 'company')
