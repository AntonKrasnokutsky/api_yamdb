from django.db import models
from django.contrib.auth.models import AbstractUser


CHOICES = (
    ('admin', 'Админ'),
    ('moderator', 'Модератор'),
    ('user', 'Пользователь'),
)


class User(AbstractUser):

    username = models.CharField(
        unique=True,
        max_length=150,
        null=True,
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        blank=False,
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
