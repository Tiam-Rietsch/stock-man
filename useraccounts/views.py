from django.shortcuts import render


def login_view(request):
    return render(request, 'useraccounts/login.html')

def signup_view(request):
    return render(request, 'useraccounts/signup.html')