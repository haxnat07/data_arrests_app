from django.db import models

from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import BaseUserManager

from django.contrib.auth.password_validation import validate_password

from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        # Validate the password
        if password is not None:
            try:
                validate_password(password, user)
            except ValidationError as e:
                raise ValueError(e)
            
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=20)
    law_firm = models.CharField(max_length=20)
    preferred_arrest_location = models.CharField(max_length=20)
    city = models.CharField(max_length=20)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
