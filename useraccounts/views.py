from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import SignupForm, LoginForm

from .models import User

def login_view(request):
    login_form = LoginForm()

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        
        print('user', user)

        if user is not None:
            login(request, user)
            return redirect('products_list')

    context = {
        'form': login_form
    }
    return render(request, 'useraccounts/login.html', context)

def signup_view(request):
    signup_form = SignupForm()

    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            return redirect('products_list')

    context = {
        'form': signup_form
    }
    return render(request, 'useraccounts/signup.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')


def user_list_view(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'useraccounts/users.html', context)


def toggle_activate_user(request, id):
    if request.method == 'POST':
        user = User.objects.get(pk=id)
        user.is_active = True if not user.is_active else False
        user.save()
        return redirect('user_list')
    

def delete_user_view(request, id):
    if request.method == 'POST':
        user = User.objects.get(pk=id)
        user.delete()
        return redirect('user_list')