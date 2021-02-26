from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.TextChoices):
    """Роли пользователей."""
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ANON = 'anon'


class CustomUser(AbstractUser):
    """ Модель кастомного пользователя."""
    bio = models.CharField(max_length=200, blank=True)
    confirmation_code = models.CharField(max_length=24, blank=True)
    description = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=60, unique=True)

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USER
    )
