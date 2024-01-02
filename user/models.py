from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class MyAccountManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None):
        if not email:
            raise ValueError("O usuário deve possuir um email")

        user: Account = self.model(
            email=self.normalize_email(email),
            username=self.normalize_email(email),
            name=name,
            surname=surname,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, surname, password):
        if not email:
            raise ValueError("O usuário deve possuir um email")

        user: Account = self.model(
            email=self.normalize_email(email),
            username=self.normalize_email(email),
            name=name,
            surname=surname,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=30, null=False, blank=False)
    surname = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=250, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return f"{self.name} {self.surname}"

    def has_perm(self, perm, obj=None):
        return self.is_admin
