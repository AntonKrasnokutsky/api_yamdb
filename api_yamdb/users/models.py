from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core import validators

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

CHOICES = (
    (ADMIN, 'Admin'),
    (MODERATOR, 'Moderator'),
    (USER, 'User'),
)


class User(AbstractUser):
    username = models.CharField(
        unique=True,
        max_length=150,
        null=False,
        blank=False,
        validators=[validators.RegexValidator(regex=r'^[\w.@+\- ]+$')],
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        blank=False,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        default='',
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        default=''
    )
    role = models.CharField(
        max_length=9,
        choices=CHOICES,
        default=USER,
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
    )

    @property
    def is_admin(self):
        return self.is_staff or self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username
