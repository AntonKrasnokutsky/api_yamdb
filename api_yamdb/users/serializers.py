from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.core import validators
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from .models import User, UsernameValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[validators.MaxLengthValidator(limit_value=254)])
    username = serializers.CharField(
        required=True,
        validators=[
            validators.MaxLengthValidator(limit_value=150),
            UsernameValidator(),
        ]
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Никнейм "me" недопустим'
            )

    class Meta:
        model = User
        fields = ('email', 'username')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['email', 'username']
            )
        ]


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(user, data['confirmation_code']):
            raise serializers.ValidationError(
                'Некорректный код'
            )
        return data

    class Meta:
        model = User
        fields = ('username', 'confirmation_code', )