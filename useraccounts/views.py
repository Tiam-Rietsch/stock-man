from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import SignupForm, LoginForm
from .models import User


def login_view(request):
    """
    Vue pour gérer la connexion des utilisateurs.
    Si la méthode de requête est POST, on tente d'authentifier l'utilisateur.
    Si l'authentification réussit, l'utilisateur est connecté et redirigé vers la liste des produits.
    Sinon, le formulaire de connexion est affiché à nouveau.
    """
    login_form = LoginForm()

    if request.method == 'POST':
        # Récupération de l'email et du mot de passe depuis le formulaire
        email = request.POST['email']
        password = request.POST['password']
        
        # Authentification de l'utilisateur avec l'email et le mot de passe
        user = authenticate(request, email=email, password=password)
        
        # Si l'utilisateur existe (authentification réussie)
        if user is not None:
            # Connexion de l'utilisateur
            login(request, user)
            # Redirection vers la page de liste des produits
            return redirect('products_list')

    # Contexte pour le rendu du template (formulaire de connexion)
    context = {
        'form': login_form
    }
    return render(request, 'useraccounts/login.html', context)


def signup_view(request):
    """
    Vue pour gérer l'inscription des nouveaux utilisateurs.
    Si la méthode de requête est POST, on valide le formulaire d'inscription.
    Si le formulaire est valide, l'utilisateur est créé et connecté, puis redirigé vers la liste des produits.
    Sinon, le formulaire d'inscription est affiché à nouveau.
    """
    signup_form = SignupForm()

    if request.method == 'POST':
        # Récupération des données du formulaire
        signup_form = SignupForm(request.POST)
        
        # Vérification de la validité du formulaire
        if signup_form.is_valid():
            # Création de l'utilisateur
            user = signup_form.save()
            # Connexion de l'utilisateur
            login(request, user)
            # Redirection vers la page de liste des produits
            return redirect('products_list')

    # Contexte pour le rendu du template (formulaire d'inscription)
    context = {
        'form': signup_form
    }
    return render(request, 'useraccounts/signup.html', context)


def logout_view(request):
    """
    Vue pour gérer la déconnexion des utilisateurs.
    L'utilisateur est déconnecté et redirigé vers la page de connexion.
    """
    logout(request)
    return redirect('login')


def user_list_view(request):
    """
    Vue pour afficher la liste des utilisateurs.
    Tous les utilisateurs sont récupérés et passés au template pour affichage.
    """
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'useraccounts/users.html', context)


def toggle_activate_user(request, id):
    """
    Vue pour activer ou désactiver un utilisateur.
    Si la méthode de requête est POST, on bascule l'état d'activation de l'utilisateur.
    L'utilisateur est ensuite redirigé vers la liste des utilisateurs.
    """
    if request.method == 'POST':
        # Récupération de l'utilisateur par son ID
        user = User.objects.get(pk=id)
        # Bascule de l'état d'activation (actif/inactif)
        user.is_active = True if not user.is_active else False
        # Sauvegarde des modifications
        user.save()
        # Redirection vers la liste des utilisateurs
        return redirect('user_list')


def delete_user_view(request, id):
    """
    Vue pour supprimer un utilisateur.
    Si la méthode de requête est POST, l'utilisateur est supprimé.
    L'utilisateur est ensuite redirigé vers la liste des utilisateurs.
    """
    if request.method == 'POST':
        # Récupération de l'utilisateur par son ID
        user = User.objects.get(pk=id)
        # Suppression de l'utilisateur
        user.delete()
        # Redirection vers la liste des utilisateurs
        return redirect('user_list')