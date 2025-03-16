import uuid
from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin


class Roles(models.TextChoices):
    manager = 'M', 'GESTIONNAIRE'
    admin = 'A', 'ADMINISTRATEUR' 


class CustomManager(UserManager):
    def create_user(self, name=None, email=None, password=None, phone_number=None, **extra_fields):
        if email is None:
            raise ValueError('Please insert an email address')
        
        email = self.normalize_email(email)
        user = self.model(name=name, email=email,  phone_number=phone_number, **extra_fields)
        user.set_password(password)
        print('\n\nhello guys this is happenning\n\n')
        return user.save(using=self._db)
    
    def create_superuser(self, name=None, email=None, password=None,phone_number=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Roles.admin)
        return self.create_user(name, email, password, phone_number, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.IntegerField()
    role = models.CharField(max_length=1, choices=Roles.choices, default=Roles.manager)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']

    def __str__(self):
        return f'{self.get_role_display()} | {self.email} : {self.name.capitalize()}'

