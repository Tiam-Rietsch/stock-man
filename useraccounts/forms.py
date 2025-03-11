from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'phone_number', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'id': 'email', 'placeholder':'Enter your email'}),
            'name': forms.TextInput(attrs={'id': 'name', 'placeholder': 'Enter your name'}),
            'phone_number': forms.TextInput(attrs={'id': 'phone', 'placeholder': 'Enter your phone number'}),
            'password1': forms.PasswordInput(attrs={'id': 'password', 'placeholder': 'Enter your password'}),
            'password2': forms.PasswordInput(attrs={'id': 'repeatPassword', 'placeholder': 'Repeat your password'})
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'id': 'email', 'placeholder': 'Enter your email'}),
            'password': forms.PasswordInput(attrs={'id': 'password', 'placeholder': 'Enter your password'})
        }