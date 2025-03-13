from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'phone_number', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'id': 'Email', 'placeholder':'Entrez votre email'}),
            'name': forms.TextInput(attrs={'id': 'Nome', 'placeholder': 'Entrez votre nom, ex: Jean Paul'}),
            'phone_number': forms.TextInput(attrs={'id': 'Contact', 'placeholder': 'Entrez votre numeros de telephone'}),
            'password1': forms.PasswordInput(attrs={'id': 'Mot de passe', 'placeholder': 'Entrez votre mot de passe'}),
            'password2': forms.PasswordInput(attrs={'id': 'Confirmer', 'placeholder': 'Confirmez votre mot the passe'})
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'id': 'email', 'placeholder': 'Entrez votre email'}),
            'password': forms.PasswordInput(attrs={'id': 'password', 'placeholder': 'Entrez votre mot de passe'})
        }