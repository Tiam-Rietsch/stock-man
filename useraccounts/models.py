import uuid
from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin


# Définition des rôles utilisateur sous forme de choix possibles
class Roles(models.TextChoices):
    manager = 'M', 'GESTIONNAIRE'  # Gestionnaire
    admin = 'A', 'ADMINISTRATEUR'  # Administrateur


# Gestionnaire personnalisé pour la création d'utilisateurs
class CustomManager(UserManager):
    def create_user(self, name=None, email=None, password=None, phone_number=None, **extra_fields):
        """
        Méthode pour créer un utilisateur standard.
        Vérifie que l'email est fourni, puis normalise l'email et crée un utilisateur.
        """
        if email is None:
            raise ValueError("Veuillez fournir une adresse e-mail")
        
        email = self.normalize_email(email)  # Normalisation de l'email
        user = self.model(name=name, email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)  # Hash du mot de passe
        return user.save(using=self._db)  # Sauvegarde dans la base de données
    
    def create_superuser(self, name=None, email=None, password=None, phone_number=None, **extra_fields):
        """
        Méthode pour créer un superutilisateur avec les permissions d'administrateur.
        """
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Roles.admin)
        
        return self.create_user(name, email, password, phone_number, **extra_fields)


# Définition du modèle utilisateur personnalisé
class User(AbstractBaseUser, PermissionsMixin):
    """
    Modèle d'utilisateur personnalisé utilisant un UUID comme clé primaire.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Identifiant unique
    name = models.CharField(max_length=255)  # Nom de l'utilisateur
    email = models.EmailField(unique=True)  # Adresse email unique
    phone_number = models.IntegerField()  # Numéro de téléphone
    role = models.CharField(max_length=1, choices=Roles.choices, default=Roles.manager)  # Rôle de l'utilisateur

    # Champs relatifs aux permissions et à l'état du compte
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Associer le gestionnaire personnalisé
    objects = CustomManager()

    # Définition du champ utilisé pour l'authentification
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']  # Champs requis lors de la création d'un superutilisateur

    def __str__(self):
        """
        Représentation textuelle de l'utilisateur.
        Retourne le rôle et les informations de l'utilisateur.
        """
        return f'{self.get_role_display()} | {self.email} : {self.name.capitalize()}'
