# accounts/models.py
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin , User
from django.conf import settings


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Vous devez entrer un email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Le superutilisateur doit avoir is_admin=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superutilisateur doit avoir is_staff=True.')

        return self.create_user(email, password, **extra_fields)


class CustomerUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False, max_length=250)
    Nom = models.CharField(max_length=50, blank=False, null=False)
    Prenom = models.CharField(max_length=100, blank=False, null=False)
    age = models.IntegerField(blank=True, null=True)
    Telephone = models.CharField(max_length=15, blank=False, null=False)
    Pays = models.CharField(max_length=50, blank=True, null=True)
    ville = models.CharField(max_length=50, blank=True, null=True)
    cond_ut = models.BooleanField(default=False)

    # Permissions fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["Nom", "Prenom", "age", "Telephone", "Pays", "ville", "cond_ut"]

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Task(models.Model):
    CATEGORY_CHOICES = [
        ('Personnel', 'Personnel'),
        ('Travail', 'Travail'),
        ('Autre', 'Autre'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=[('Haute', 'Haute'), ('Moyenne', 'Moyenne'), ('Basse', 'Basse')])
    completed = models.BooleanField(default=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Autre')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
