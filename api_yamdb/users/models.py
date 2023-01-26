from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.contrib.auth.validators import UnicodeUsernameValidator


CHOICES = (
    ('admin', 'Админ'),
    ('moderator', 'Модератор'),
    ('user', 'Пользователь'),
)


class UsernameValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+\- ]+$'


class User(AbstractUser):

    username = models.CharField(
        unique=True,
        max_length=150,
        null=False,
        blank=False,
        validators=[validators.MaxLengthValidator(limit_value=150), UsernameValidator()]
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        blank=False,
        validators=[
            validators.EmailValidator(message="Invalid Email"),
            validators.MaxLengthValidator(limit_value=254),
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('email', 'username'),
                name="unique_user"
            )
        ]
