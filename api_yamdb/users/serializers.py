from rest_framework import serializers
from django.core import validators
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.tokens import default_token_generator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[validators.MaxLengthValidator(limit_value=254)]
    )
    username = serializers.CharField(
        required=True,
        validators=[
            validators.MaxLengthValidator(limit_value=150),
            validators.RegexValidator(regex=r'^[\w.@+\- ]+$')
        ]
    )

    class Meta:
        model = User
        fields = ('email', 'username')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['email', 'username'],
            )
        ]

    def validate(self, attrs):
        if attrs.get('username') == 'me':
            raise serializers.ValidationError('Sorry this nickname is forbidden')
        if User.objects.filter(username=attrs.get('username')).exists():
            raise serializers.ValidationError('Sorry this nickname already exists.')
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError('Sorry this email already exists.')
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code', )

    def validate(self, attrs):
        user = attrs.get('username')
        if not User.objects.filter(username=user).exists():
            raise serializers.ValidationError('Sorry this nickname does not exist.')
        if not default_token_generator.check_token(user, attrs['confirmation_code']):
            raise serializers.ValidationError('sorry, invalid confirmation code')
        return attrs
