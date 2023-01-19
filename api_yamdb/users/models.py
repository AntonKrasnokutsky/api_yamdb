from django.db import models
from django.contrib.auth.models import User


class CustomUser(models.Model):
    USER = 'USER'
    ROLE_CHOICES = [
        ('USER', 'user'),
        ('MODERATOR', 'moderator'),
        ('ADMIN', 'admin'),
    ]
    USER_ROLE = ''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=256)
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
