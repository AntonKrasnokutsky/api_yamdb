from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators


CHOICES = (
    ('admin', 'Admin'),
    ('moderator', 'Moderator'),
    ('user', 'User'),
)


class User(AbstractUser):
    username = models.CharField(
        unique=True,
        max_length=150,
        null=False,
        blank=False,
        validators=[
            validators.MaxLengthValidator(limit_value=150),
            validators.RegexValidator(regex=r'^[\w.@+\- ]+$')
        ],
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        blank=False,
        validators=[
            validators.EmailValidator(message='Invalid Email'),
        ]
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
    )
    role = models.CharField(
        max_length=9,
        choices=CHOICES,
        default='user',
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
    )
