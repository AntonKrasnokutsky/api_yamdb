from django.contrib.auth.models import AbstractUser
from django.db import models
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
        default='user',
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
    )

    @property
    def is_admin(self):
        return self.is_staff or self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def __str__(self):
        return self.username
